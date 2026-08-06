#!/usr/bin/env python3
"""Regression tests for staged-change pre-ship safety."""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "pre_ship.py"


def git(root, *args):
    return subprocess.run(
        ["git", *args], cwd=root, capture_output=True, text=True, check=True
    )


def scan(files, config=None, extra_args=None, unstaged_files=None):
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        git(root, "init", "-q")
        git(root, "config", "user.email", "test@example.com")
        git(root, "config", "user.name", "Test")
        for relative, content in files.items():
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        if config:
            (root / ".rad-repo.json").write_text(json.dumps(config), encoding="utf-8")
        git(root, "add", "-f", "--", ".")
        for relative, content in (unstaged_files or {}).items():
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(SCRIPT), str(root), "--json", *(extra_args or [])],
            capture_output=True, text=True, check=False,
        )
        return result.returncode, json.loads(result.stdout)


code, report = scan({".env": "SECRET=value\n"})
assert code == 1 and report["blocking"], report
assert report["findings"][0]["kind"] == "protected_path", report

code, report = scan({".env.example": "SECRET=placeholder\n", "src/app.py": "print('ok')\n"})
assert code == 0 and not report["findings"], report

code, report = scan({"dist/bundle.js": "generated\n"})
assert code == 1, report
assert report["findings"][0]["kind"] == "generated_output", report

code, report = scan({"cert.txt": "-----BEGIN PRIVATE KEY-----\nsecret\n"})
assert code == 1, report
assert report["findings"][0]["kind"] == "secret_content", report

code, report = scan(
    {"large.txt": "x" * 32},
    {"shipping": {"large_file_bytes": 16}},
    ["--allow-contract-change"],
)
assert code == 1, report
assert report["findings"][0]["kind"] == "large_file", report

code, report = scan(
    {"AGENTS.md": "# Instructions\n\n- Test: `echo safe`\n"},
    extra_args=["--run-validation"],
)
assert code == 1, report
assert report["findings"][0]["kind"] == "contract_change", report
assert report["validation"] == [], "blocked contract commands must never execute"

code, report = scan(
    {"safe.txt": "safe"},
    extra_args=["--run-validation"],
    unstaged_files={"AGENTS.md": "# Instructions\n\n- Test: `echo unsafe`\n"},
)
assert code == 1, report
assert any(item["kind"] == "contract_dirty" for item in report["findings"]), report
assert report["validation"] == [], "unstaged contract commands must never execute"

code, report = scan(
    {"AGENTS.md": "# Instructions\n\n- Test: `echo safe`\n"},
    extra_args=["--allow-contract-change"],
)
assert code == 0, report

code, report = scan({"README.md": "docs only\n"}, extra_args=["--run-validation"])
assert code == 1, report
assert report["findings"][0]["kind"] == "validation_missing", report

code, report = scan(
    {"README.md": "docs only\n"},
    {"validation": {"allow_empty": True}},
    ["--allow-contract-change", "--run-validation"],
)
assert code == 0, report

print("pre-ship regression tests passed")
