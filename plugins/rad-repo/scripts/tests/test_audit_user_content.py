#!/usr/bin/env python3
"""Regression tests for root and scoped instruction auditing."""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "audit-user-content.py"

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    scoped = root / "src" / "café"
    scoped.mkdir(parents=True)
    (root / "AGENTS.md").write_text(
        "# Root\n\n## Documentation rules\n- See `docs/missing.md`.\n",
        encoding="utf-8",
    )
    (scoped / "AGENTS.md").write_text(
        "# Scoped\n\n## Component constraints\n- Preserve `src/café/missing.py`.\n",
        encoding="utf-8",
    )
    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(root), "--json"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    report = json.loads(result.stdout)
    assert len(report["files_audited"]) == 2
    assert any(
        finding["category"] == "dead-path" and "café" in finding["message"]
        for finding in report["findings"]
    )
    assert not any("docs/missing.md" in finding["message"] for finding in report["findings"])

print("audit-user-content regression tests passed")
