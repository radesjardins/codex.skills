from __future__ import annotations

import tempfile
import unittest
from pathlib import Path


import sys


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from sync_check import compare_marketplaces


class SyncCheckTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.left = Path(self.temp_dir.name) / "left"
        self.right = Path(self.temp_dir.name) / "right"
        (self.left / "plugins").mkdir(parents=True)
        (self.right / "plugins").mkdir(parents=True)

    @staticmethod
    def write_plugin(root: Path, name: str, content: str) -> None:
        package = root / "plugins" / name
        package.mkdir(parents=True)
        (package / "plugin.json").write_text(content, encoding="utf-8")

    def test_shared_drift_fails_without_writing_files(self) -> None:
        self.write_plugin(self.left, "shared", '{"version":"1.0.0"}')
        self.write_plugin(self.right, "shared", '{"version":"1.1.0"}')
        left_before = (self.left / "plugins" / "shared" / "plugin.json").read_bytes()
        right_before = (self.right / "plugins" / "shared" / "plugin.json").read_bytes()

        report = compare_marketplaces(self.left, self.right)

        self.assertFalse(report.in_sync)
        self.assertEqual(("plugin.json",), report.shared[0].different_files)
        self.assertEqual(left_before, (self.left / "plugins" / "shared" / "plugin.json").read_bytes())
        self.assertEqual(right_before, (self.right / "plugins" / "shared" / "plugin.json").read_bytes())

    def test_unique_packages_are_reported_without_failing(self) -> None:
        self.write_plugin(self.left, "shared", '{"version":"1.0.0"}')
        self.write_plugin(self.right, "shared", '{"version":"1.0.0"}')
        self.write_plugin(self.left, "left-only", "left")
        self.write_plugin(self.right, "right-only", "right")

        report = compare_marketplaces(self.left, self.right)

        self.assertTrue(report.in_sync)
        self.assertEqual(("left-only",), report.left_only)
        self.assertEqual(("right-only",), report.right_only)
        self.assertEqual((), report.shared[0].different_files)

    def test_generated_python_cache_does_not_create_drift(self) -> None:
        self.write_plugin(self.left, "shared", '{"version":"1.0.0"}')
        self.write_plugin(self.right, "shared", '{"version":"1.0.0"}')
        cache = self.left / "plugins" / "shared" / "scripts" / "__pycache__"
        cache.mkdir(parents=True)
        (cache / "module.pyc").write_bytes(b"generated")

        report = compare_marketplaces(self.left, self.right)

        self.assertTrue(report.in_sync)
        self.assertEqual((), report.shared[0].different_files)

    def test_line_ending_differences_do_not_create_drift(self) -> None:
        self.write_plugin(self.left, "shared", "placeholder")
        self.write_plugin(self.right, "shared", "placeholder")
        (self.left / "plugins" / "shared" / "plugin.json").write_bytes(b"line one\r\nline two\r\n")
        (self.right / "plugins" / "shared" / "plugin.json").write_bytes(b"line one\nline two\n")

        report = compare_marketplaces(self.left, self.right)

        self.assertTrue(report.in_sync)
        self.assertEqual((), report.shared[0].different_files)

    def test_directory_without_plugin_manifest_is_not_a_package(self) -> None:
        self.write_plugin(self.left, "shared", '{"version":"1.0.0"}')
        self.write_plugin(self.right, "shared", '{"version":"1.0.0"}')
        orphan = self.left / "plugins" / "retired" / "scripts" / "__pycache__"
        orphan.mkdir(parents=True)
        (orphan / "module.pyc").write_bytes(b"generated")

        report = compare_marketplaces(self.left, self.right)

        self.assertNotIn("retired", report.left_only)


if __name__ == "__main__":
    unittest.main()
