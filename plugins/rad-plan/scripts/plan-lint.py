#!/usr/bin/env python3
"""
plan-lint.py — Mechanical validation for docs/plan.md.

Validates the single-file plan rad-plan emits against the structure in
references/plan-template.md. It checks sections, the six task fields, outcome
coverage, path labels, dependencies, concrete proof, and unsafe rollback forms.

The 7.1 contract targets one plan.md whose tasks each carry Objective, Files,
Depends on, Done when, Validate, and Rollback. It also maps each observable
outcome to its live tasks and final proof.

Usage:
  python3 plan-lint.py docs/plan.md
  python3 plan-lint.py docs/plan.md --json

Output:
  Default — human-readable text. Exit 1 if CRITICAL or HIGH issues, else 0.
  --json   — single JSON object on stdout for skill consumption.
  Exit 2  — script errors (file not found, parse failure beyond recovery).

MEDIUM and LOW issues surface but do not fail the validator.

No third-party dependencies. Python 3.8+.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path

# Required H2 sections per references/plan-template.md. "Stack" is conditional.
# "Shipped" (re-plan history) is optional and deliberately not linted. Its task
# blocks live outside ## Tasks so history is never re-validated.
REQUIRED_SECTIONS = (
    "Objective",
    "Release map",
    "Scope",
    "Key assumptions",
    "Milestones",
    "Tasks",
    "Checkpoints",
    "Risks & mitigations",
    "Validation",
    "Stop conditions",
)

CONTRACT_MARKER = "<!-- rad-plan-contract: 7.1 -->"
OUTCOME_SECTION = "Outcome coverage"

# The six fields every task in ## Tasks must carry.
REQUIRED_TASK_FIELDS = (
    "Objective",
    "Files",
    "Depends on",
    "Done when",
    "Validate",
    "Rollback",
)

# Fields whose values must be concrete (no hand-waving).
VAGUE_SCAN_FIELDS = ("Done when", "Validate")

FILE_LABELS = ("[existing]", "[new]")

UNSAFE_ROLLBACK_PHRASES = (
    "git reset --hard",
    "git checkout --",
    "git restore",
    "rm -rf",
    "remove-item -recurse",
)

VAGUE_PHRASES = (
    "verify it works",
    "verify that it works",
    "check that it works",
    "make sure it runs",
    "make sure it works",
    "ensure functionality",
    "ensure it works",
    "confirm it's working",
    "confirm it is working",
    "test it manually",
    "looks right",
    "looks good",
    "should work",
    "tbd",
    "to be determined",
)

PLACEHOLDER_PATTERNS = (
    re.compile(r"^\s*\[[A-Za-z][^]]*\]\s*$"),  # [Single clear outcome]
    re.compile(r"^\s*\.\.\.\s*$"),               # ...
)

SECTION_HEADING = re.compile(r"^##\s+(.+?)\s*$")
# Task header bullet: `- **T1 — title**` (em-dash or hyphen; title optional).
TASK_HEADER = re.compile(
    r"^\s*-\s*\*\*\s*(?P<id>T\d+(?:\.\d+)?)\b[^*]*\*\*\s*$"
)
# Field bullet under a task: `  - **Objective:** value`.
FIELD_BULLET = re.compile(
    r"^\s*-\s*\*\*(?P<label>[^*:]+?):\*\*\s*(?P<value>.*?)\s*$"
)
BULLET = re.compile(r"^\s*-\s+(?P<text>.+?)\s*$")
TASK_REF = re.compile(r"\bT\d+(?:\.\d+)?\b")
OUTCOME_ID = re.compile(r"^O\d+(?:\.\d+)?\b", re.IGNORECASE)


@dataclass
class Section:
    name: str
    line: int  # 1-indexed line of the heading
    body_lines: list[str] = field(default_factory=list)

    @property
    def body(self) -> str:
        return "\n".join(self.body_lines).strip()

    @property
    def is_empty(self) -> bool:
        body = self.body
        if not body:
            return True
        non_empty = [ln for ln in body.splitlines() if ln.strip()]
        if not non_empty:
            return True
        return all(
            any(p.match(ln) for p in PLACEHOLDER_PATTERNS) for ln in non_empty
        )


@dataclass
class Task:
    task_id: str
    line: int
    fields: dict[str, str] = field(default_factory=dict)  # lowercased label -> value


@dataclass
class Outcome:
    outcome_id: str
    line: int
    covered_by: str
    final_proof: str


@dataclass
class Issue:
    severity: str   # CRITICAL | HIGH | MEDIUM | LOW
    category: str   # sections | tasks | dependencies | vague
    section: str | None
    message: str
    fix: str

    def to_dict(self) -> dict:
        return asdict(self)


# ---------- parsing ----------


def parse_sections(text: str) -> dict[str, Section]:
    """Parse plan.md into named sections keyed by H2 heading."""
    sections: dict[str, Section] = {}
    current: Section | None = None
    for lineno, raw in enumerate(text.splitlines(), start=1):
        m = SECTION_HEADING.match(raw)
        if m:
            current = Section(name=m.group(1).strip(), line=lineno)
            sections.setdefault(current.name, current)
            continue
        if raw.startswith("# ") and current is not None:
            current = None
            continue
        if current is not None:
            current.body_lines.append(raw)
    return sections


def find_duplicate_sections(text: str) -> list[tuple[str, int]]:
    """Return repeated H2 section names and the line of each repeat."""
    seen: set[str] = set()
    duplicates: list[tuple[str, int]] = []
    for lineno, raw in enumerate(text.splitlines(), start=1):
        match = SECTION_HEADING.match(raw)
        if not match:
            continue
        name = match.group(1).strip()
        if name in seen:
            duplicates.append((name, lineno))
        else:
            seen.add(name)
    return duplicates


def parse_tasks(section: Section) -> list[Task]:
    """Parse tasks from the ## Tasks section body. A task starts at a `- **Tn**`
    header bullet; subsequent `- **Field:** value` bullets are its fields until
    the next task header."""
    tasks: list[Task] = []
    current: Task | None = None
    for i, raw in enumerate(section.body_lines):
        lineno = section.line + i + 1
        header = TASK_HEADER.match(raw)
        if header:
            current = Task(task_id=header.group("id"), line=lineno)
            tasks.append(current)
            continue
        if current is None:
            continue
        fm = FIELD_BULLET.match(raw)
        if fm:
            current.fields[fm.group("label").strip().lower()] = fm.group("value").strip()
    return tasks


def parse_outcomes(section: Section) -> list[Outcome]:
    """Parse data rows from the Outcome coverage Markdown table."""
    outcomes: list[Outcome] = []
    for index, raw in enumerate(section.body_lines):
        stripped = raw.strip()
        if not (stripped.startswith("|") and stripped.endswith("|")):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) < 3:
            continue
        if cells[0].lower() == "outcome":
            continue
        if all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells[:3]):
            continue
        outcome_id = cells[0].split(" ", 1)[0].upper()
        outcomes.append(Outcome(
            outcome_id=outcome_id,
            line=section.line + index + 1,
            covered_by=cells[1],
            final_proof=cells[2],
        ))
    return outcomes


# ---------- checks ----------


def check_sections(sections: dict[str, Section], contract_71: bool) -> list[Issue]:
    issues: list[Issue] = []
    for req in REQUIRED_SECTIONS:
        if req not in sections:
            issues.append(Issue(
                "CRITICAL", "sections", req,
                f"Missing required section: '## {req}'",
                f"Add a '## {req}' section per references/plan-template.md",
            ))
        elif sections[req].is_empty:
            issues.append(Issue(
                "HIGH", "sections", req,
                f"Required section '## {req}' is empty or placeholder-only",
                f"Populate '## {req}' with project-specific content",
            ))
    if OUTCOME_SECTION not in sections:
        issues.append(Issue(
            "HIGH" if contract_71 else "MEDIUM", "outcomes", OUTCOME_SECTION,
            "Missing '## Outcome coverage' section",
            "Map each observable outcome to at least one live task and one final proof",
        ))
    elif sections[OUTCOME_SECTION].is_empty:
        issues.append(Issue(
            "HIGH", "outcomes", OUTCOME_SECTION,
            "The '## Outcome coverage' section is empty",
            "Add at least one O1 row with a live task and final proof",
        ))
    return issues


def check_duplicate_sections(duplicates: list[tuple[str, int]]) -> list[Issue]:
    return [
        Issue(
            "HIGH", "sections", name,
            f"Duplicate section '## {name}' at line {line}",
            "Keep one authoritative section with this heading",
        )
        for name, line in duplicates
    ]


def _scan_vague(text: str) -> str | None:
    lower = text.lower()
    for phrase in VAGUE_PHRASES:
        if phrase in lower:
            return phrase
    return None


def check_tasks(tasks: list[Task], has_tasks_section: bool, contract_71: bool) -> list[Issue]:
    issues: list[Issue] = []
    if has_tasks_section and not tasks:
        issues.append(Issue(
            "CRITICAL", "tasks", "Tasks",
            "The '## Tasks' section has no parseable tasks",
            "Add tasks as '- **T1 — title**' with the six required field bullets",
        ))
        return issues

    seen_ids: set[str] = set()
    for task in tasks:
        tag = task.task_id
        if task.task_id in seen_ids:
            issues.append(Issue(
                "HIGH", "tasks", tag,
                f"Duplicate task ID '{task.task_id}' (line {task.line})",
                "Give each task a unique ID (T1, T2, ...)",
            ))
        seen_ids.add(task.task_id)

        for req in REQUIRED_TASK_FIELDS:
            key = req.lower()
            if key not in task.fields:
                issues.append(Issue(
                    "HIGH", "tasks", tag,
                    f"Task {task.task_id} missing required field: '{req}'",
                    f"Add '- **{req}:** <value>' under task {task.task_id}",
                ))
                continue
            value = task.fields[key]
            if not value or value in ("-", "TBD", "tbd", "...", "[ ]"):
                issues.append(Issue(
                    "HIGH", "tasks", tag,
                    f"Task {task.task_id} field '{req}' is empty or placeholder",
                    f"Populate '- **{req}:** <value>' for task {task.task_id}",
                ))

        for fld in VAGUE_SCAN_FIELDS:
            value = task.fields.get(fld.lower(), "")
            phrase = _scan_vague(value)
            if phrase:
                issues.append(Issue(
                    "HIGH", "vague", tag,
                    f"Task {task.task_id} field '{fld}' contains vague phrase: '{phrase}'",
                    "Replace with a concrete, verifiable command or condition",
                ))

        if contract_71:
            files_value = task.fields.get("files", "")
            for entry in [part.strip() for part in files_value.split(";") if part.strip()]:
                if not entry.lower().startswith(FILE_LABELS):
                    issues.append(Issue(
                        "HIGH", "tasks", tag,
                        f"Task {task.task_id} file entry lacks [existing] or [new]: '{entry}'",
                        "Prefix each semicolon-separated Files entry with [existing] or [new]",
                    ))

    if len(tasks) > 20:
        issues.append(Issue(
            "MEDIUM", "tasks", "Tasks",
            f"The live plan has {len(tasks)} tasks; the review threshold is 20",
            "Reduce the current release or split it into a smaller plan",
        ))
    return issues


def check_dependencies(tasks: list[Task]) -> list[Issue]:
    """Referenced task IDs must exist (no phantoms); the graph must be acyclic."""
    issues: list[Issue] = []
    ids = {t.task_id for t in tasks}
    graph: dict[str, list[str]] = {}

    for task in tasks:
        raw = task.fields.get("depends on", "")
        refs = TASK_REF.findall(raw)
        if refs and re.search(r"\bnone\b", raw, re.IGNORECASE):
            issues.append(Issue(
                "HIGH", "dependencies", task.task_id,
                f"Task {task.task_id} says 'none' and also names a dependency",
                "Use 'none' or live task IDs, not both",
            ))
        deps: list[str] = []
        for ref in refs:
            if ref == task.task_id:
                issues.append(Issue(
                    "HIGH", "dependencies", task.task_id,
                    f"Task {task.task_id} depends on itself",
                    f"Remove the self-reference in task {task.task_id}'s 'Depends on'",
                ))
                continue
            if ref not in ids:
                issues.append(Issue(
                    "HIGH", "dependencies", task.task_id,
                    f"Task {task.task_id} depends on '{ref}', which is not a defined task",
                    f"Reference an existing task ID or remove '{ref}'",
                ))
                continue
            deps.append(ref)
        graph[task.task_id] = deps

    # Cycle detection (DFS with colors).
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {tid: WHITE for tid in graph}
    cycle_reported: set[frozenset] = set()

    def visit(node: str, stack: list[str]) -> None:
        color[node] = GRAY
        stack.append(node)
        for dep in graph.get(node, []):
            if color.get(dep) == GRAY:
                cyc = stack[stack.index(dep):] + [dep]
                key = frozenset(cyc)
                if key not in cycle_reported:
                    cycle_reported.add(key)
                    issues.append(Issue(
                        "CRITICAL", "dependencies", node,
                        "Dependency cycle: " + " -> ".join(cyc),
                        "Break the cycle — tasks cannot mutually depend on each other",
                    ))
            elif color.get(dep) == WHITE:
                visit(dep, stack)
        stack.pop()
        color[node] = BLACK

    for tid in graph:
        if color[tid] == WHITE:
            visit(tid, [])

    return issues


def check_outcomes(outcomes: list[Outcome], tasks: list[Task], has_section: bool) -> list[Issue]:
    issues: list[Issue] = []
    if not has_section:
        return issues
    if not outcomes:
        return [Issue(
            "HIGH", "outcomes", OUTCOME_SECTION,
            "The Outcome coverage table has no parseable rows",
            "Add rows such as '| O1 - outcome | T1 | `focused check` |'",
        )]

    task_ids = {task.task_id for task in tasks}
    seen: set[str] = set()
    for outcome in outcomes:
        if not OUTCOME_ID.match(outcome.outcome_id):
            issues.append(Issue(
                "HIGH", "outcomes", outcome.outcome_id,
                f"Outcome row at line {outcome.line} lacks an O-number ID",
                "Start the Outcome cell with O1, O2, and so on",
            ))
            continue
        if outcome.outcome_id in seen:
            issues.append(Issue(
                "HIGH", "outcomes", outcome.outcome_id,
                f"Duplicate outcome ID '{outcome.outcome_id}'",
                "Give each outcome a unique O-number ID",
            ))
        seen.add(outcome.outcome_id)

        refs = TASK_REF.findall(outcome.covered_by)
        if not refs:
            issues.append(Issue(
                "HIGH", "outcomes", outcome.outcome_id,
                f"Outcome {outcome.outcome_id} has no live task reference",
                "Add at least one task ID in the Covered by column",
            ))
        for ref in refs:
            if ref not in task_ids:
                issues.append(Issue(
                    "HIGH", "outcomes", outcome.outcome_id,
                    f"Outcome {outcome.outcome_id} references undefined task '{ref}'",
                    "Reference a live task from the Tasks section",
                ))

        proof = outcome.final_proof.strip().strip("`")
        if not proof or proof.lower() in ("tbd", "...", "[focused final check]"):
            issues.append(Issue(
                "HIGH", "outcomes", outcome.outcome_id,
                f"Outcome {outcome.outcome_id} has no concrete final proof",
                "Name a focused final command or exact review condition",
            ))
        else:
            phrase = _scan_vague(proof)
            if phrase:
                issues.append(Issue(
                    "HIGH", "outcomes", outcome.outcome_id,
                    f"Outcome {outcome.outcome_id} proof contains vague phrase: '{phrase}'",
                    "Replace it with a concrete command or observable condition",
                ))
    return issues


def check_unsafe_rollbacks(text: str) -> list[Issue]:
    issues: list[Issue] = []
    for lineno, raw in enumerate(text.splitlines(), start=1):
        if "**rollback:**" not in raw.lower():
            continue
        lower = raw.lower()
        for phrase in UNSAFE_ROLLBACK_PHRASES:
            if phrase in lower:
                issues.append(Issue(
                    "HIGH", "safety", "Rollback",
                    f"Unsafe rollback command form '{phrase}' at line {lineno}",
                    "Describe a safe recovery strategy without a destructive Git or recursive-delete command",
                ))
    return issues


# ---------- output ----------


def render_text(report: dict) -> str:
    lines = [
        f"plan-lint: file={report['file']}",
        f"contract: {report['contract_version']}  sections: {report['section_count']}  "
        f"tasks: {report['task_count']}  outcomes: {report['outcome_count']}",
    ]
    issues = report["issues"]
    if not issues:
        lines += ["", "OK — no issues found."]
        return "\n".join(lines)

    by_sev: dict[str, list[dict]] = {}
    for i in issues:
        by_sev.setdefault(i["severity"], []).append(i)
    summary = ", ".join(
        f"{sev}: {len(by_sev[sev])}"
        for sev in ("CRITICAL", "HIGH", "MEDIUM", "LOW") if sev in by_sev
    )
    lines += ["", f"Issues: {len(issues)} total — {summary}"]
    for sev in ("CRITICAL", "HIGH", "MEDIUM", "LOW"):
        for i in by_sev.get(sev, []):
            tag = f"[{i['section']}]" if i["section"] else "[plan-level]"
            lines.append(f"  {sev} {tag} ({i['category']}) {i['message']}")
            lines.append(f"      fix: {i['fix']}")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("path", help="Path to docs/plan.md")
    p.add_argument("--json", action="store_true", help="Emit a single JSON object instead of text")
    args = p.parse_args(argv)

    file_path = Path(args.path)
    if not file_path.exists():
        print(f"error: file not found: {file_path}", file=sys.stderr)
        return 2
    try:
        text = file_path.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        print(f"error: failed to read {file_path}: {e}", file=sys.stderr)
        return 2

    sections = parse_sections(text)
    duplicates = find_duplicate_sections(text)
    tasks = parse_tasks(sections["Tasks"]) if "Tasks" in sections else []
    outcomes = parse_outcomes(sections[OUTCOME_SECTION]) if OUTCOME_SECTION in sections else []
    contract_71 = CONTRACT_MARKER in text

    issues: list[Issue] = []
    issues.extend(check_sections(sections, contract_71))
    issues.extend(check_duplicate_sections(duplicates))
    issues.extend(check_tasks(tasks, "Tasks" in sections, contract_71))
    issues.extend(check_dependencies(tasks))
    issues.extend(check_outcomes(outcomes, tasks, OUTCOME_SECTION in sections))
    issues.extend(check_unsafe_rollbacks(text))

    report = {
        "file": str(file_path),
        "contract_version": "7.1" if contract_71 else "legacy",
        "section_count": len(sections),
        "section_names": list(sections.keys()),
        "task_count": len(tasks),
        "outcome_count": len(outcomes),
        "issues": [i.to_dict() for i in issues],
    }

    print(json.dumps(report, indent=2) if args.json else render_text(report))

    return 1 if any(i.severity in ("CRITICAL", "HIGH") for i in issues) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
