#!/usr/bin/env python3
"""
vocab-lint.py — vocabulary-ladder lint for managed docs.

The shelf spec (references/shelf-spec.md) recommends one vocabulary for units of
work: Goal → Release (Now/Next/Later) → Milestone (M1…) → Task (T1…). This script
scans managed docs using a repository-selectable vocabulary profile:

  1. Profile-configured synonyms used as a tracked unit of work: phase, slice, sprint, epic,
     stage, and "step N". Ordinary prose is exempt where mechanically detectable
     (fenced code blocks are skipped); the rest are CANDIDATES — judgment decides
     which are real. Skill/workflow prose isn't scanned at all (only managed docs
     are), so "Step 2: run the scan" in a how-to never gets here.
  2. Ladder terms in the wrong doc: milestone/task identifiers (M1, T3, the word
     "milestone") inside docs/prd.md — the PRD speaks only Goal/Release; plan.md
     owns Milestone/Task.

The default profile is advisory. Repositories can set vocabulary.mode to "strict"
or "off" and vocabulary.scope to "all" or "headings" in
.rad-repo.json. Strict findings exit 1; the script never auto-fixes.

Usage:
  python3 vocab-lint.py <project-dir>
  python3 vocab-lint.py <project-dir> --json

No third-party dependencies. Python 3.8+.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

MANAGED_DOCS = (
    "docs/prd.md", "docs/plan.md", "docs/handoff.md",
    "docs/decisions.md", "docs/ideas.md", "docs/lessons.md",
    "docs/architecture.md", "docs/api.md",
)

DEFAULT_TERMS = ("phase", "slice", "sprint", "epic", "stage", "step")
DEFAULT_PROFILE = {
    "mode": "advisory",
    "scope": "all",
    "banned_terms": list(DEFAULT_TERMS),
    "enforce_wrong_doc": True,
}

# PRD speaks only Goal/Release — milestone/task language there is a wrong-doc finding.
PRD_WRONG_DOC = re.compile(r"\bmilestones?\b|\bM\d+\b|\bT\d+\b", re.IGNORECASE)

FENCE = re.compile(r"^\s*(```|~~~)")


def load_profile(root: Path, config_path: Path | None = None) -> dict:
    profile = dict(DEFAULT_PROFILE)
    path = config_path or root / ".rad-repo.json"
    if path.is_file():
        payload = json.loads(path.read_text(encoding="utf-8"))
        configured = payload.get("vocabulary", {})
        if not isinstance(configured, dict):
            raise ValueError("vocabulary config must be an object")
        profile.update(configured)
    if profile["mode"] not in {"advisory", "strict", "off"}:
        raise ValueError("vocabulary.mode must be advisory, strict, or off")
    if profile["scope"] not in {"all", "headings"}:
        raise ValueError("vocabulary.scope must be all or headings")
    if not isinstance(profile["banned_terms"], list) or not all(
        isinstance(term, str) and term.strip() for term in profile["banned_terms"]
    ):
        raise ValueError("vocabulary.banned_terms must be a list of non-empty strings")
    return profile


def term_pattern(terms: list[str]) -> re.Pattern:
    ordinary = [term for term in terms if term.casefold() != "step"]
    parts = [rf"\b{re.escape(term)}s?\b" for term in ordinary]
    if any(term.casefold() == "step" for term in terms):
        parts.append(r"\bsteps?\s+\d+\b")
    return re.compile("|".join(parts) or r"(?!)", re.IGNORECASE)


def lint_file(root: Path, rel: str, profile: dict) -> list[dict]:
    path = root / rel
    if not path.is_file() or profile["mode"] == "off":
        return []
    findings: list[dict] = []
    banned = term_pattern(profile["banned_terms"])
    severity = "error" if profile["mode"] == "strict" else "advisory"
    synonym_kind = "banned_synonym" if profile["mode"] == "strict" else "advisory_synonym"
    in_fence = False
    for i, ln in enumerate(
            path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if FENCE.match(ln):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if profile["scope"] == "all" or ln.lstrip().startswith("#"):
            for m in banned.finditer(ln):
                findings.append({
                    "path": rel, "line": i, "term": m.group(0),
                    "kind": synonym_kind, "severity": severity,
                    "text": ln.strip()[:120],
                })
        if rel == "docs/prd.md" and profile["enforce_wrong_doc"]:
            for m in PRD_WRONG_DOC.finditer(ln):
                findings.append({
                    "path": rel, "line": i, "term": m.group(0),
                    "kind": "wrong_doc", "severity": severity,
                    "text": ln.strip()[:120],
                })
    return findings


def render_text(report: dict) -> str:
    if not report["findings"]:
        return "Vocabulary is clean — ladder terms only, each in its own doc."
    lines = []
    for f in report["findings"]:
        lines.append(f"[{f['kind']}] {f['path']}:{f['line']} — \"{f['term']}\" in: {f['text']}")
    lines.append(f"{len(report['findings'])} candidate(s) under the {report['profile']['mode']} profile.")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("path", help="Project directory to scan")
    p.add_argument("--json", action="store_true", help="Emit a single JSON object")
    p.add_argument("--config", type=Path, help="Override .rad-repo.json path")
    args = p.parse_args(argv)

    root = Path(args.path)
    if not root.is_dir():
        print(f"error: not a directory: {root}", file=sys.stderr)
        return 2

    try:
        profile = load_profile(root, args.config)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"error: invalid vocabulary config: {error}", file=sys.stderr)
        return 2

    findings: list[dict] = []
    for rel in MANAGED_DOCS:
        findings.extend(lint_file(root, rel, profile))

    report = {
        "profile": {key: profile[key] for key in DEFAULT_PROFILE},
        "findings": findings,
        "count": len(findings),
    }
    print(json.dumps(report, indent=2) if args.json else render_text(report))
    return 1 if any(finding["severity"] == "error" for finding in findings) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
