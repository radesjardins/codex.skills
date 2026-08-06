#!/usr/bin/env python3
"""Audit a Claude-to-Codex plugin port for common migration leftovers."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Iterable

TEXT_EXTS = {
    ".md",
    ".txt",
    ".json",
    ".toml",
    ".yaml",
    ".yml",
    ".py",
    ".ps1",
    ".js",
    ".mjs",
    ".ts",
    ".tsx",
}

PATTERNS = [
    ("error", "claude-plugin-root", "CLAUDE_PLUGIN_ROOT"),
    ("error", "claude-config-dir", "CLAUDE_CONFIG_DIR"),
    ("error", "hooks-dir-ref", "hooks/"),
    ("error", "sessionstart", "SessionStart"),
    ("error", "posttooluse", "PostToolUse"),
    ("error", "precompact", "PreCompact"),
    ("error", "stop-hook", "Stop hook"),
    ("warning", "claude-md", "CLAUDE.md"),
    ("warning", "gemini-md", "GEMINI.md"),
    ("warning", "claude-code", "Claude Code"),
    ("warning", "sync-to-cache", "sync_to_cache"),
    ("warning", "usage-guard", "usage_guard"),
    ("warning", "broad-trigger", "whenever working on"),
    ("warning", "broad-trigger", "Use whenever"),
]

HOOK_SCRIPT_NAMES = {
    "hook_sessionstart.py",
    "hook_postwrite.py",
    "usage_guard.py",
}

GENERATED_EXTS = {".pyc", ".pyo"}
GENERATED_NAMES = {"__pycache__"}


def iter_files(root: Path) -> Iterable[Path]:
    for current, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in {".git", "node_modules", ".venv", "venv"}]
        current_path = Path(current)
        for filename in files:
            yield current_path / filename


def text_lines(path: Path) -> Iterable[tuple[int, str]]:
    try:
        content = path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return []
    return enumerate(content.splitlines(), 1)


def add_findings_for_text(root: Path, path: Path, findings: list[dict]) -> None:
    if path.suffix.lower() not in TEXT_EXTS:
        return
    for line_no, line in text_lines(path):
        for severity, code, pattern in PATTERNS:
            if pattern.lower() in line.lower():
                findings.append(
                    {
                        "severity": severity,
                        "code": code,
                        "path": str(path.relative_to(root)).replace("\\", "/"),
                        "line": line_no,
                        "match": pattern,
                    }
                )


def audit(root: Path) -> dict:
    findings: list[dict] = []

    manifest = root / ".codex-plugin" / "plugin.json"
    if not manifest.exists():
        findings.append({"severity": "error", "code": "missing-plugin-json", "path": ".codex-plugin/plugin.json"})
    else:
        try:
            data = json.loads(manifest.read_text(encoding="utf-8-sig"))
            if "hooks" in data:
                findings.append({"severity": "error", "code": "manifest-hooks-field", "path": ".codex-plugin/plugin.json"})
            if data.get("skills") and not (root / str(data["skills"])).exists():
                findings.append({"severity": "error", "code": "missing-skills-dir", "path": str(data["skills"])})
        except json.JSONDecodeError as exc:
            findings.append({"severity": "error", "code": "invalid-plugin-json", "path": ".codex-plugin/plugin.json", "detail": str(exc)})

    for path in iter_files(root):
        rel = str(path.relative_to(root)).replace("\\", "/")
        parts = set(path.relative_to(root).parts)
        if "hooks" in parts:
            findings.append({"severity": "error", "code": "hooks-directory-file", "path": rel})
        if path.name in HOOK_SCRIPT_NAMES:
            findings.append({"severity": "error", "code": "hook-only-script", "path": rel})
        if path.suffix.lower() in GENERATED_EXTS:
            findings.append({"severity": "warning", "code": "generated-bytecode", "path": rel})
        add_findings_for_text(root, path, findings)

    for current, dirs, _files in os.walk(root):
        for dirname in dirs:
            if dirname in GENERATED_NAMES:
                p = Path(current) / dirname
                findings.append({"severity": "warning", "code": "generated-cache-dir", "path": str(p.relative_to(root)).replace("\\", "/")})

    error_count = sum(1 for f in findings if f["severity"] == "error")
    warning_count = sum(1 for f in findings if f["severity"] == "warning")
    return {
        "root": str(root),
        "error_count": error_count,
        "warning_count": warning_count,
        "findings": findings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit Claude-to-Codex plugin port leftovers.")
    parser.add_argument("root", help="Plugin root to audit")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    result = audit(root)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Audited: {result['root']}")
        print(f"Errors: {result['error_count']}  Warnings: {result['warning_count']}")
        for finding in result["findings"]:
            loc = finding["path"]
            if "line" in finding:
                loc += f":{finding['line']}"
            print(f"{finding['severity'].upper()} {finding['code']} {loc}")
    return 1 if result["error_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
