#!/usr/bin/env python3
"""Regression tests for shelf-wide, boilerplate-resistant redundancy checks."""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "doc-redundancy.py"

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    (root / "docs" / "initiatives").mkdir(parents=True)
    (root / "docs" / "architecture.md").write_text(
        "# Current status and next actions\n\n- Requests use the signed gateway authentication boundary.\n",
        encoding="utf-8",
    )
    (root / "docs" / "initiatives" / "gateway.md").write_text(
        "# Current status and next actions\n\n- Requests use the signed gateway authentication boundary.\n",
        encoding="utf-8",
    )
    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(root), "--json"],
        capture_output=True,
        text=True,
    )
    report = json.loads(result.stdout)
    assert "docs/initiatives/gateway.md" in report["docs_scanned"]
    assert len(report["duplicates"]) == 1, report["duplicates"]
    assert report["duplicates"][0]["text_a"].startswith("Requests use")

print("doc-redundancy regression tests passed")
