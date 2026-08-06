#!/usr/bin/env python3
"""Regression tests for evidence-aware doc freshness."""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "doc-freshness.py"


def git(root, *args):
    subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True)


with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    git(root, "init", "-q")
    git(root, "config", "user.email", "tests@example.com")
    git(root, "config", "user.name", "Tests")
    (root / "docs").mkdir()
    (root / "src").mkdir()
    (root / "src" / "api.py").write_text("VERSION = 1\n", encoding="utf-8")
    (root / "docs" / "architecture.md").write_text(
        "---\ntracks:\n  - src/api.py\n  - src/missing.py\n---\n# Architecture\n",
        encoding="utf-8",
    )
    (root / "AGENTS.md").write_text("# Instructions\n", encoding="utf-8")
    git(root, "add", ".")
    git(root, "commit", "-qm", "initial")
    (root / "src" / "api.py").write_text("VERSION = 2\n", encoding="utf-8")
    git(root, "add", "src/api.py")
    git(root, "commit", "-qm", "change api")

    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(root), "--json"],
        capture_output=True,
        text=True,
        check=True,
    )
    report = json.loads(result.stdout)
    findings = report["findings"]
    assert any(f.get("category") == "tracked_path_missing" for f in findings)
    assert any(f.get("category") == "tracked_path_changed" for f in findings)
    state = report["docs"]["docs/architecture.md"]
    assert state["tracked_paths"] == ["src/api.py", "src/missing.py"]
    assert state["tracked_commits_since"] == 1

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    (root / "docs").mkdir()
    (root / "docs" / "handoff.md").write_text("# Handoff\n", encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(root), "--json"],
        capture_output=True,
        text=True,
        check=True,
    )
    report = json.loads(result.stdout)
    assert report["git_history"] is False
    assert report["docs"]["docs/handoff.md"]["tracked"] is False

print("doc-freshness regression tests passed")
