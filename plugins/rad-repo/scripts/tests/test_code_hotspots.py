#!/usr/bin/env python3
"""Regression test for Git-based code hotspot ranking."""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "code-hotspots.py"


def git(root, *args):
    return subprocess.run(
        ["git", *args], cwd=root, capture_output=True, text=True, check=True
    )


with tempfile.TemporaryDirectory() as temporary:
    root = Path(temporary)
    git(root, "init", "-q")
    git(root, "config", "user.email", "test@example.com")
    git(root, "config", "user.name", "Test")
    (root / "src").mkdir()
    (root / "dist").mkdir()
    (root / "src" / "hot.py").write_text("\n".join(f"x{i} = {i}" for i in range(80)), encoding="utf-8")
    (root / "src" / "stable.py").write_text("print('stable')\n", encoding="utf-8")
    (root / "dist" / "bundle.js").write_text("\n".join("x();" for _ in range(300)), encoding="utf-8")
    git(root, "add", ".")
    git(root, "commit", "-qm", "initial")
    for index in range(3):
        with (root / "src" / "hot.py").open("a", encoding="utf-8") as handle:
            handle.write(f"\nchange_{index} = True")
        git(root, "add", "src/hot.py")
        git(root, "commit", "-qm", f"change {index}")

    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(root), "--json"],
        capture_output=True,
        text=True,
        check=True,
    )
    report = json.loads(result.stdout)
    assert report["findings"][0]["path"] == "src/hot.py", report
    assert all(item["path"] != "dist/bundle.js" for item in report["findings"]), report
    assert report["findings"][0]["changes"] == 4, report

print("code-hotspots regression test passed")
