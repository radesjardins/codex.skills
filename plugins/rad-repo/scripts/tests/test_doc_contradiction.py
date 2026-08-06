#!/usr/bin/env python3
"""Regression tests for domain constraint contradiction checks."""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "doc-contradiction.py"

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    (root / "docs").mkdir()
    (root / "docs" / "decisions.md").write_text(
        "# Decisions\n\n## ADR 0002\n"
        "- **Status:** locked\n"
        "- **Constraint:** Never import the Google GenAI SDK outside the Gemini agent boundary.\n",
        encoding="utf-8",
    )
    (root / "docs" / "plan.md").write_text(
        "# Plan\n\n- **Objective:** Import the Google GenAI SDK into the service wrapper outside the Gemini agent boundary.\n",
        encoding="utf-8",
    )
    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(root), "--json"],
        capture_output=True,
        text=True,
        check=True,
    )
    report = json.loads(result.stdout)
    assert "locked_constraint_vs_plan" in report["checks_run"]
    assert any(f["category"] == "locked_constraint_vs_plan" for f in report["findings"])

print("doc-contradiction regression tests passed")
