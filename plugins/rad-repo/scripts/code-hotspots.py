#!/usr/bin/env python3
"""Rank code maintenance hotspots from tracked files and recent Git history."""

from __future__ import annotations

import argparse
import json
import math
import shutil
import subprocess
from collections import defaultdict
from pathlib import Path

SOURCE_SUFFIXES = {
    ".c", ".cc", ".cpp", ".cs", ".css", ".dart", ".ex", ".exs", ".go",
    ".h", ".hpp", ".html", ".java", ".js", ".jsx", ".kt", ".kts", ".lua",
    ".php", ".pl", ".py", ".rb", ".rs", ".scala", ".sh", ".sql", ".svelte",
    ".swift", ".ts", ".tsx", ".vue",
}
EXCLUDED_PARTS = {
    ".git", ".next", ".venv", "build", "coverage", "dist", "fixtures",
    "generated", "node_modules", "target", "vendor",
}
TOOL_NAMES = ("lizard", "radon", "eslint", "ruff", "golangci-lint", "clippy")
REPORT_NAMES = (
    "sonar-project.properties",
    ".codeclimate.yml",
    ".qlty/qlty.toml",
    "coverage.xml",
    "lcov.info",
)


def run_git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-c", "core.quotepath=false", *args],
        cwd=root,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def tracked_source_files(root: Path) -> list[str]:
    output = subprocess.run(
        ["git", "-c", "core.quotepath=false", "ls-files", "-z"],
        cwd=root,
        capture_output=True,
        check=True,
    ).stdout
    files: list[str] = []
    for raw in output.split(b"\0"):
        if not raw:
            continue
        relative = raw.decode("utf-8", errors="replace")
        path = Path(relative)
        if path.suffix.lower() not in SOURCE_SUFFIXES:
            continue
        if any(part.lower() in EXCLUDED_PARTS for part in path.parts[:-1]):
            continue
        files.append(path.as_posix())
    return files


def line_count(path: Path) -> int | None:
    try:
        content = path.read_bytes()
    except OSError:
        return None
    if b"\0" in content or len(content) > 2 * 1024 * 1024:
        return None
    return content.count(b"\n") + (1 if content and not content.endswith(b"\n") else 0)


def history_signals(root: Path, months: int) -> tuple[dict[str, int], dict[str, int], dict[str, set[str]]]:
    output = run_git(
        root,
        "log",
        f"--since={months} months ago",
        "--no-renames",
        "--numstat",
        "--format=@@RAD_AUTHOR:%ae",
    )
    changes: dict[str, int] = defaultdict(int)
    lines_changed: dict[str, int] = defaultdict(int)
    authors: dict[str, set[str]] = defaultdict(set)
    author = "unknown"
    for line in output.splitlines():
        if line.startswith("@@RAD_AUTHOR:"):
            author = line.removeprefix("@@RAD_AUTHOR:").strip() or "unknown"
            continue
        parts = line.split("\t", 2)
        if len(parts) != 3 or not parts[0].isdigit() or not parts[1].isdigit():
            continue
        added, deleted, relative = int(parts[0]), int(parts[1]), Path(parts[2]).as_posix()
        changes[relative] += 1
        lines_changed[relative] += added + deleted
        authors[relative].add(author)
    return changes, lines_changed, authors


def detected_signals(root: Path) -> dict:
    tools = [name for name in TOOL_NAMES if shutil.which(name)]
    reports = [name for name in REPORT_NAMES if (root / name).exists()]
    return {"tools": tools, "reports": reports}


def build_report(root: Path, months: int, limit: int) -> dict:
    source_files = tracked_source_files(root)
    changes, changed_lines, authors = history_signals(root, months)
    findings: list[dict] = []
    for relative in source_files:
        lines = line_count(root / relative)
        if lines is None or lines == 0:
            continue
        change_count = changes.get(relative, 0)
        priority_index = round((change_count + 1) * math.log2(lines + 1), 2)
        findings.append({
            "path": relative,
            "lines": lines,
            "changes": change_count,
            "lines_changed": changed_lines.get(relative, 0),
            "authors": len(authors.get(relative, set())),
            "priority_index": priority_index,
            "confidence": "git-history" if change_count else "size-only",
        })
    findings.sort(
        key=lambda item: (item["priority_index"], item["changes"], item["lines"]),
        reverse=True,
    )
    return {
        "root": str(root),
        "months": months,
        "tracked_source_files": len(source_files),
        "method": "(changes + 1) * log2(lines + 1); review priority, not code quality",
        "findings": findings[:limit],
        "available_signals": detected_signals(root),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--months", type=int, default=12)
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.months < 1 or args.limit < 1:
        parser.error("--months and --limit must be positive")

    root = Path(args.root).resolve()
    try:
        report = build_report(root, args.months, args.limit)
    except (OSError, subprocess.CalledProcessError) as error:
        report = {"root": str(root), "error": str(error), "findings": []}
        if args.json:
            print(json.dumps(report, indent=2))
        else:
            print(f"ERROR: {error}")
        return 1

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"Code hotspots: {len(report['findings'])} shown from {report['tracked_source_files']} source files")
        for index, item in enumerate(report["findings"], 1):
            print(
                f"{index}. {item['path']} | {item['lines']} lines | "
                f"{item['changes']} changes | priority {item['priority_index']}"
            )
        print("Priority ranks review value. It does not prove poor code quality.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
