from __future__ import annotations

import sys
import unittest
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = PLUGIN_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from audit import audit_path


class PackageTests(unittest.TestCase):
    def test_converter_package_is_a_conforming_agent_plugin(self) -> None:
        report = audit_path(PLUGIN_ROOT)

        self.assertTrue(report.conforming, [item.to_dict() for item in report.findings])
        self.assertEqual(("agent-plugin", "codex"), report.source_types)
        self.assertEqual("rad-plugin-converter", report.plugin_name)


if __name__ == "__main__":
    unittest.main()
