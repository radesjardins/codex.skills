from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from audit import MCP_SCHEMA, PLUGIN_SCHEMA, audit_path, detect_source_types


class AuditTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.root = Path(self.temp_dir.name) / "sample"
        self.root.mkdir()

    def write_json(self, relative: str, value: object) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
        return path

    def write_skill(
        self,
        relative_dir: str,
        name: str,
        description: str = "Check a sample package. Use when testing plugin conformance.",
        body: str = "# Sample\n",
    ) -> Path:
        skill_dir = self.root / relative_dir
        skill_dir.mkdir(parents=True, exist_ok=True)
        (skill_dir / "SKILL.md").write_text(
            f"---\nname: {name}\ndescription: {description}\n---\n\n{body}",
            encoding="utf-8",
        )
        return skill_dir

    def write_portable_manifest(self, **overrides: object) -> None:
        manifest: dict[str, object] = {
            "$schema": PLUGIN_SCHEMA,
            "name": "sample",
            "version": "1.0.0",
            "description": "Sample plugin.",
            "author": {"name": "RAD"},
            "license": "MIT",
        }
        manifest.update(overrides)
        self.write_json("plugin.json", manifest)

    def codes(self) -> set[str]:
        return {item.code for item in audit_path(self.root).findings}

    def test_codex_plugin_without_root_manifest_is_detected(self) -> None:
        self.write_json(".codex-plugin/plugin.json", {"name": "sample", "skills": "./skills/"})
        self.write_skill("skills/check", "check")

        report = audit_path(self.root)

        self.assertEqual(("codex",), report.source_types)
        self.assertIn("missing-portable-manifest", {item.code for item in report.findings})

    def test_agent_claude_and_codex_sources_form_a_mixed_package(self) -> None:
        self.write_portable_manifest()
        self.write_json(".codex-plugin/plugin.json", {"name": "sample"})
        self.write_json(".claude-plugin/plugin.json", {"name": "sample"})

        self.assertEqual(("agent-plugin", "codex", "claude"), detect_source_types(self.root))

    def test_nested_skill_is_reported_as_undiscoverable(self) -> None:
        self.write_portable_manifest()
        self.write_skill("skills/group/deploy", "deploy")

        self.assertIn("nested-skill", self.codes())

    def test_unknown_manifest_field_is_an_error(self) -> None:
        self.write_portable_manifest(skills="./skills")

        self.assertIn("manifest-unknown-field", self.codes())

    def test_invalid_manifest_author_field_is_an_error(self) -> None:
        self.write_portable_manifest(author={"name": "RAD", "company": "Example"})

        self.assertIn("manifest-author-field", self.codes())

    def test_broken_local_skill_link_is_an_error(self) -> None:
        self.write_portable_manifest()
        self.write_skill("skills/check", "check", body="See [missing](references/missing.md).\n")

        self.assertIn("skill-link-missing", self.codes())

    def test_skill_link_cannot_escape_skill_directory(self) -> None:
        self.write_portable_manifest()
        self.write_skill("skills/check", "check", body="See [outside](../../outside.md).\n")

        self.assertIn("skill-link-escape", self.codes())

    def test_skill_over_500_lines_is_advisory(self) -> None:
        self.write_portable_manifest()
        self.write_skill("skills/check", "check", body="\n".join(["line"] * 501))

        report = audit_path(self.root)

        matching = [item for item in report.findings if item.code == "skill-length"]
        self.assertEqual(1, len(matching))
        self.assertEqual("warning", matching[0].severity)
        self.assertTrue(report.conforming)

    def test_mcp_command_must_be_one_executable_token(self) -> None:
        self.write_portable_manifest()
        self.write_json(
            "mcp.json",
            {
                "$schema": MCP_SCHEMA,
                "mcpServers": {
                    "bad": {"type": "stdio", "command": "python server.py"},
                },
            },
        )

        self.assertIn("mcp-command", self.codes())

    def test_remote_http_mcp_url_is_rejected(self) -> None:
        self.write_portable_manifest()
        self.write_json(
            "mcp.json",
            {
                "$schema": MCP_SCHEMA,
                "mcpServers": {
                    "bad": {"type": "streamable-http", "url": "http://example.com/mcp"},
                },
            },
        )

        self.assertIn("mcp-url-https", self.codes())

    def test_secret_header_is_rejected(self) -> None:
        self.write_portable_manifest()
        self.write_json(
            "mcp.json",
            {
                "$schema": MCP_SCHEMA,
                "mcpServers": {
                    "bad": {
                        "type": "streamable-http",
                        "url": "https://example.com/mcp",
                        "headers": {"Authorization": "Bearer secret"},
                    },
                },
            },
        )

        self.assertIn("mcp-secret-header", self.codes())

    def test_client_only_directory_is_informational(self) -> None:
        self.write_portable_manifest()
        hooks = self.root / "hooks"
        hooks.mkdir()
        (hooks / "hooks.json").write_text("{}\n", encoding="utf-8")

        report = audit_path(self.root)
        matching = [item for item in report.findings if item.code == "client-only-artifact"]

        self.assertEqual(1, len(matching))
        self.assertEqual("info", matching[0].severity)
        self.assertTrue(report.conforming)

    def test_symlink_cannot_escape_plugin_root(self) -> None:
        self.write_portable_manifest()
        outside = Path(self.temp_dir.name) / "outside.txt"
        outside.write_text("outside\n", encoding="utf-8")
        link = self.root / "outside-link.txt"
        try:
            os.symlink(outside, link)
        except OSError as exc:
            self.skipTest(f"Symlink creation is unavailable: {exc}")

        self.assertIn("package-path-escape", self.codes())


if __name__ == "__main__":
    unittest.main()
