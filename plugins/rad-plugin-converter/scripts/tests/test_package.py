from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[2]
REPOSITORY_ROOT = PLUGIN_ROOT.parents[1]
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

    def test_public_marketplaces_point_to_converter_package(self) -> None:
        marketplace_paths = (
            REPOSITORY_ROOT / "marketplace.json",
            REPOSITORY_ROOT / ".agents" / "plugins" / "marketplace.json",
        )
        catalogs = [json.loads(path.read_text(encoding="utf-8")) for path in marketplace_paths]

        self.assertEqual(catalogs[0], catalogs[1])
        entries = catalogs[0]["plugins"]
        names = [entry["name"] for entry in entries]
        self.assertNotIn("claude-to-codex-plugin-port", names)

        converter = next(entry for entry in entries if entry["name"] == "rad-plugin-converter")
        self.assertEqual("./plugins/rad-plugin-converter", converter["source"]["path"])
        self.assertTrue((REPOSITORY_ROOT / "plugins" / "rad-plugin-converter").is_dir())


if __name__ == "__main__":
    unittest.main()
