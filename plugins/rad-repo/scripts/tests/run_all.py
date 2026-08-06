#!/usr/bin/env python3
"""Run every rad-repo regression test without external dependencies."""

import subprocess
import sys
from pathlib import Path

TEST_DIR = Path(__file__).resolve().parent
tests = sorted(TEST_DIR.glob("test_*.py"))

for test in tests:
    print(f"==> {test.name}", flush=True)
    result = subprocess.run([sys.executable, str(test)])
    if result.returncode:
        raise SystemExit(result.returncode)

print(f"All {len(tests)} regression tests passed")
