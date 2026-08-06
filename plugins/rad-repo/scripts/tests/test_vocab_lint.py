#!/usr/bin/env python3
"""Regression tests for configurable vocabulary linting."""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "vocab-lint.py"


def run(files, config=None):
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        for relative, content in files.items():
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        if config is not None:
            (root / ".rad-repo.json").write_text(
                json.dumps(config), encoding="utf-8"
            )
        result = subprocess.run(
            [sys.executable, str(SCRIPT), str(root), "--json"],
            capture_output=True,
            text=True,
            check=False,
        )
        return result.returncode, json.loads(result.stdout)


code, report = run({"docs/plan.md": "## Phase 1\nThis phase is exploratory.\n"})
assert code == 0, report
assert {finding["kind"] for finding in report["findings"]} == {"advisory_synonym"}, report
assert all(finding["severity"] == "advisory" for finding in report["findings"]), report

code, report = run(
    {"docs/plan.md": "## Phase 1\nThis phase is ordinary prose.\n"},
    {"vocabulary": {"mode": "strict", "scope": "headings", "banned_terms": ["phase"]}},
)
assert code == 1, report
assert report["count"] == 1, report
assert report["findings"][0]["kind"] == "banned_synonym", report
assert report["findings"][0]["line"] == 1, report

code, report = run(
    {"docs/plan.md": "## Phase 1\n"},
    {"vocabulary": {"mode": "off"}},
)
assert code == 0 and report["count"] == 0, report

code, report = run({"docs/prd.md": "## M1\n"})
assert code == 0, report
assert report["findings"][0]["kind"] == "wrong_doc", report
assert report["findings"][0]["severity"] == "advisory", report

print("vocab-lint regression tests passed")
