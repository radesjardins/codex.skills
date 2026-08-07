import json
import unittest
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]


class PluginContractTests(unittest.TestCase):
    def read(self, relative_path):
        return (PLUGIN_ROOT / relative_path).read_text(encoding="utf-8")

    def test_manifest_and_public_skill_name_match_4_1(self):
        manifest = json.loads(self.read(".codex-plugin/plugin.json"))
        self.assertEqual("4.1.1", manifest["version"])
        self.assertTrue((PLUGIN_ROOT / "skills" / "software-design" / "SKILL.md").is_file())
        self.assertFalse((PLUGIN_ROOT / "skills" / "design-sprint" / "SKILL.md").exists())

        package_text = self.read(".codex-plugin/plugin.json") + self.read("README.md")
        self.assertNotIn("design-sprint", package_text)
        self.assertIn("rad-brainstorm:software-design", package_text)

    def test_public_scope_is_one_person_and_text_first(self):
        readme = self.read("README.md").lower()
        self.assertIn("one-person", readme)
        self.assertIn("text-first", readme)

    def test_brainstorm_workflow_has_4_1_quality_controls(self):
        skill = self.read("skills/brainstorm-session/SKILL.md").lower()
        for phrase in (
            "goal",
            "primary user",
            "success",
            "hard constraint",
            "[user]",
            "[ai]",
            "[research]",
            "mechanism",
            "cluster",
            "checkpoint",
            "mermaid",
            "session-output.md",
        ):
            self.assertIn(phrase, skill)

    def test_evaluation_workflow_protects_distinctions_and_sets_proof_thresholds(self):
        skill = self.read("skills/idea-evaluation/SKILL.md").lower()
        self.assertIn("cluster", skill)
        self.assertIn("preserve", skill)
        self.assertIn("pass threshold", skill)
        self.assertIn("stop signal", skill)

    def test_references_are_smaller_and_have_one_source_of_truth(self):
        references = PLUGIN_ROOT / "references"
        self.assertFalse((references / "domain-research-guide.md").exists())

        facilitation = self.read("references/facilitation-principles.md")
        methods = self.read("references/methodology-catalog.md")
        unblocking = self.read("references/creative-unblocking.md")
        evaluation = self.read("references/evaluation-frameworks.md")

        self.assertLess(len(facilitation.split()), 900)
        self.assertLess(len(methods.split()), 2200)
        self.assertNotIn("## Convergent Techniques", methods)
        self.assertNotIn("### 9. 5 Whys", methods)
        self.assertNotIn("## 7. SWOT", evaluation)
        self.assertNotIn("Barry Schwartz", unblocking)
        self.assertNotIn("consistently shows", facilitation.lower())

    def test_result_contract_has_three_examples_and_checkpoint_fields(self):
        result_contract = self.read("references/session-output.md").lower()
        for heading in ("## result contract", "## example 1", "## example 2", "## example 3"):
            self.assertIn(heading, result_contract)
        for field in ("session phase", "next question", "idea source", "user approval"):
            self.assertIn(field, result_contract)


if __name__ == "__main__":
    unittest.main()
