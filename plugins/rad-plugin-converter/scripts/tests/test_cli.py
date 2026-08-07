from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "rad_plugin_converter.py"


class CliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.root = Path(self.temp_dir.name) / "sample"
        (self.root / ".codex-plugin").mkdir(parents=True)
        (self.root / ".codex-plugin" / "plugin.json").write_text(
            json.dumps({"name": "sample", "version": "1.0.0"}),
            encoding="utf-8",
        )

    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        environment = os.environ.copy()
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            text=True,
            capture_output=True,
            encoding="utf-8",
            env=environment,
            check=False,
        )

    def test_audit_json_exit_code_tracks_conformance(self) -> None:
        before = self.run_cli("audit", str(self.root), "--json")
        before_data = json.loads(before.stdout)

        converted = self.run_cli("convert", str(self.root), "--in-place", "--json")
        after = self.run_cli("audit", str(self.root), "--json")
        after_data = json.loads(after.stdout)

        self.assertEqual(1, before.returncode)
        self.assertFalse(before_data["conforming"])
        self.assertEqual(0, converted.returncode)
        self.assertEqual(0, after.returncode)
        self.assertTrue(after_data["conforming"])

    def test_marketplace_json_output_is_an_array(self) -> None:
        marketplace = Path(self.temp_dir.name) / "marketplace"
        plugin = marketplace / "plugins" / "sample"
        (plugin / ".codex-plugin").mkdir(parents=True)
        (plugin / ".codex-plugin" / "plugin.json").write_text(
            json.dumps({"name": "sample"}),
            encoding="utf-8",
        )
        (marketplace / "marketplace.json").write_text(
            json.dumps(
                {
                    "name": "market",
                    "plugins": [
                        {"name": "sample", "source": {"source": "local", "path": "./plugins/sample"}}
                    ],
                }
            ),
            encoding="utf-8",
        )

        result = self.run_cli("marketplace", str(marketplace), "--json")
        output = json.loads(result.stdout)

        self.assertEqual(1, result.returncode)
        self.assertIsInstance(output, list)
        self.assertEqual("sample", output[0]["root"].replace("\\", "/").rsplit("/", 1)[-1])

    def test_create_command_writes_a_conforming_plugin(self) -> None:
        target = Path(self.temp_dir.name) / "created-plugin"

        result = self.run_cli(
            "create",
            "created-plugin",
            "--target",
            str(target),
            "--description",
            "Create sample output.",
            "--author",
            "RAD",
            "--skill",
            "create-sample",
            "--skill-description",
            "Use when creating a sample.",
            "--json",
        )
        output = json.loads(result.stdout)
        portable = json.loads((target / "plugin.json").read_text(encoding="utf-8"))

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertTrue(output["successful"])
        self.assertEqual("created-plugin", portable["name"])
        self.assertTrue((target / "skills" / "create-sample" / "SKILL.md").is_file())


if __name__ == "__main__":
    unittest.main()
