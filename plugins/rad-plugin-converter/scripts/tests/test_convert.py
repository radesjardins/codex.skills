from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from audit import MCP_SCHEMA, PLUGIN_SCHEMA, audit_path
from convert import convert_in_place, convert_marketplace, convert_to_target


class ConversionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.base = Path(self.temp_dir.name)

    def write_json(self, root: Path, relative: str, value: object) -> Path:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
        return path

    def write_skill(self, root: Path, directory: str = "check", name: str = "check") -> None:
        skill = root / "skills" / directory
        skill.mkdir(parents=True, exist_ok=True)
        (skill / "SKILL.md").write_text(
            "---\n"
            f"name: {name}\n"
            "description: Check plugins. Use when testing conversion.\n"
            "---\n\n"
            "# Check\n",
            encoding="utf-8",
        )

    def make_codex_plugin(self, name: str = "sample") -> Path:
        root = self.base / name
        root.mkdir()
        self.write_json(
            root,
            ".codex-plugin/plugin.json",
            {
                "name": name,
                "version": "2.3.4",
                "description": "Sample Codex plugin.",
                "author": {"name": "RAD"},
                "license": "MIT",
                "skills": "./skills/",
                "interface": {"displayName": "Sample"},
            },
        )
        self.write_skill(root)
        return root

    def test_codex_conversion_is_additive_and_repeatable(self) -> None:
        root = self.make_codex_plugin()
        compatibility_before = (root / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")

        first = convert_in_place(root)
        second = convert_in_place(root)
        portable = json.loads((root / "plugin.json").read_text(encoding="utf-8"))

        self.assertTrue(first.successful)
        self.assertEqual(["plugin.json"], first.changed_files)
        self.assertEqual([], second.changed_files)
        self.assertEqual(PLUGIN_SCHEMA, portable["$schema"])
        self.assertEqual("2.3.4", portable["version"])
        self.assertEqual("MIT", portable["license"])
        self.assertNotIn("skills", portable)
        self.assertNotIn("interface", portable)
        self.assertEqual(
            compatibility_before,
            (root / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"),
        )
        self.assertTrue(audit_path(root).conforming)

    def test_safe_skill_name_mismatch_is_repaired(self) -> None:
        root = self.make_codex_plugin()
        skill_path = root / "skills" / "check" / "SKILL.md"
        skill_path.write_text(
            skill_path.read_text(encoding="utf-8").replace("name: check", "name: wrong"),
            encoding="utf-8",
        )

        result = convert_in_place(root)

        self.assertTrue(result.successful)
        self.assertIn("skills/check/SKILL.md", result.changed_files)
        self.assertIn("name: check", skill_path.read_text(encoding="utf-8"))

    def test_invalid_plugin_name_blocks_conversion(self) -> None:
        root = self.make_codex_plugin("sample")
        manifest_path = root / ".codex-plugin" / "plugin.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["name"] = "Bad Name"
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

        result = convert_in_place(root)

        self.assertFalse(result.successful)
        self.assertFalse((root / "plugin.json").exists())
        self.assertIn("conversion-plugin-name", {item.code for item in result.findings})

    def test_claude_stdio_mcp_is_converted_without_changing_source_file(self) -> None:
        root = self.make_codex_plugin()
        source_mcp = {
            "mcpServers": {
                "local": {
                    "command": "python",
                    "args": ["${CLAUDE_PLUGIN_ROOT}/server.py"],
                    "env": {"CONFIG": "${CLAUDE_PLUGIN_ROOT}/config.json"},
                }
            }
        }
        source_path = self.write_json(root, ".mcp.json", source_mcp)
        before = source_path.read_text(encoding="utf-8")

        result = convert_in_place(root)
        portable_mcp = json.loads((root / "mcp.json").read_text(encoding="utf-8"))

        self.assertTrue(result.successful)
        self.assertEqual(before, source_path.read_text(encoding="utf-8"))
        self.assertEqual(MCP_SCHEMA, portable_mcp["$schema"])
        self.assertEqual("stdio", portable_mcp["mcpServers"]["local"]["type"])
        self.assertEqual(
            ["${PLUGIN_ROOT}/server.py"],
            portable_mcp["mcpServers"]["local"]["args"],
        )

    def test_url_mcp_without_transport_requires_a_choice(self) -> None:
        root = self.make_codex_plugin()
        self.write_json(
            root,
            ".mcp.json",
            {"mcpServers": {"remote": {"url": "https://example.com/mcp"}}},
        )

        result = convert_in_place(root)

        self.assertFalse(result.successful)
        self.assertFalse((root / "mcp.json").exists())
        self.assertIn("conversion-mcp-transport", {item.code for item in result.findings})

    def test_target_conversion_keeps_claude_source_unchanged(self) -> None:
        source = self.base / "source"
        source.mkdir()
        self.write_json(
            source,
            ".claude-plugin/plugin.json",
            {"name": "sample", "version": "1.0.0", "license": "MIT"},
        )
        self.write_skill(source)
        source_snapshot = {
            path.relative_to(source).as_posix(): path.read_bytes()
            for path in source.rglob("*")
            if path.is_file()
        }
        target = self.base / "target"

        result = convert_to_target(source, target)

        self.assertTrue(result.successful)
        self.assertTrue((target / "plugin.json").is_file())
        self.assertTrue((target / ".claude-plugin" / "plugin.json").is_file())
        self.assertEqual(
            source_snapshot,
            {
                path.relative_to(source).as_posix(): path.read_bytes()
                for path in source.rglob("*")
                if path.is_file()
            },
        )

    def test_nonempty_target_is_not_overwritten(self) -> None:
        source = self.make_codex_plugin()
        target = self.base / "occupied"
        target.mkdir()
        sentinel = target / "keep.txt"
        sentinel.write_text("keep\n", encoding="utf-8")

        result = convert_to_target(source, target)

        self.assertFalse(result.successful)
        self.assertEqual("keep\n", sentinel.read_text(encoding="utf-8"))
        self.assertIn("conversion-target-not-empty", {item.code for item in result.findings})

    def test_marketplace_is_read_only_without_apply(self) -> None:
        marketplace = self.base / "marketplace"
        plugin = marketplace / "plugins" / "sample"
        plugin.mkdir(parents=True)
        self.write_json(plugin, ".codex-plugin/plugin.json", {"name": "sample"})
        self.write_skill(plugin)
        self.write_json(
            marketplace,
            "marketplace.json",
            {
                "name": "sample-marketplace",
                "plugins": [
                    {"name": "sample", "source": {"source": "local", "path": "./plugins/sample"}}
                ],
            },
        )

        dry_results = convert_marketplace(marketplace, apply=False)
        self.assertFalse((plugin / "plugin.json").exists())
        self.assertEqual(1, dry_results[0].error_count)

        applied_results = convert_marketplace(marketplace, apply=True)
        self.assertTrue((plugin / "plugin.json").is_file())
        self.assertTrue(applied_results[0].successful)


if __name__ == "__main__":
    unittest.main()
