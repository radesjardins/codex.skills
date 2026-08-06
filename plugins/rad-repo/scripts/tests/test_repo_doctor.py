#!/usr/bin/env python3
"""Regression test for contract diagnosis and local command approval."""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "repo-doctor.py"


def git(root, *args):
    return subprocess.run(
        ["git", *args], cwd=root, capture_output=True, text=True, check=True
    )


def doctor(root, *args):
    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(root), *args, "--json"],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode, json.loads(result.stdout)


with tempfile.TemporaryDirectory() as temporary:
    root = Path(temporary)
    git(root, "init", "-q")
    git(root, "config", "user.email", "test@example.com")
    git(root, "config", "user.name", "Test")
    (root / "AGENTS.md").write_text(
        "<!-- rad-repo-doc-model: 1 -->\n# Repo\n\n- Test: `echo safe`\n",
        encoding="utf-8",
    )
    (root / "app.py").write_text("print('ok')\n", encoding="utf-8")
    git(root, "add", ".")

    code, report = doctor(root)
    assert code == 1 and report["approval_required"], report
    assert report["commands"][0]["source"] == "AGENTS.md", report
    assert report["doc_model"]["status"] == "current", report

    code, report = doctor(root, "--approve")
    assert code == 0 and report["ready"] and report["validation_trusted"], report

    (root / "AGENTS.md").write_text(
        "<!-- rad-repo-doc-model: 1 -->\n# Repo\n\n- Test: `echo changed`\n",
        encoding="utf-8",
    )
    code, report = doctor(root)
    assert code == 1 and report["approval_required"], report

print("repo-doctor regression test passed")
