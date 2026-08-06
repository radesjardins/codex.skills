import importlib.util
import json
import sys
import unittest
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = PLUGIN_ROOT / "scripts" / "validate-json.py"
SCHEMAS = PLUGIN_ROOT / "references" / "subagent-prompts"


def load_validator():
    spec = importlib.util.spec_from_file_location("rad_plan_validate_json", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


validator = load_validator()


class ValidateJsonTests(unittest.TestCase):
    def test_valid_stack_payload(self):
        schema = self.schema("stack-eval.schema.json")
        payload = {
            "evaluation_complete": True,
            "project_type": "existing web app",
            "summary": "Keep the current stack.",
            "current_stack_fit": "fits",
            "recommendation": [{
                "layer": "Application",
                "choice": "Current stack",
                "version": "repository versions",
                "requirement": "Add one settings field",
                "rationale": "No new system is required.",
            }],
            "compatibility_verified": True,
            "confidence": "high",
            "escalation_required": False,
        }
        self.assertEqual([], validator.validate(payload, schema))

    def test_stack_payload_requires_requirement(self):
        schema = self.schema("stack-eval.schema.json")
        payload = {
            "evaluation_complete": True,
            "project_type": "new app",
            "summary": "Choose one option.",
            "current_stack_fit": "no_current_stack",
            "recommendation": [{
                "layer": "Database",
                "choice": "PostgreSQL",
                "version": "18",
                "rationale": "Fits the data model.",
            }],
            "compatibility_verified": True,
            "confidence": "medium",
            "escalation_required": False,
        }
        errors = validator.validate(payload, schema)
        self.assertTrue(any("requirement" in error["path"] for error in errors), errors)

    def test_valid_risk_payload(self):
        schema = self.schema("risk-assessment.schema.json")
        payload = {
            "assessment_complete": True,
            "iteration": 1,
            "verdict": "APPROVE",
            "summary": {
                "critical_count": 0,
                "high_count": 0,
                "medium_count": 0,
                "low_count": 0,
            },
            "blocking_issues": [],
            "advisory_issues": [],
            "escalation_required": False,
        }
        self.assertEqual([], validator.validate(payload, schema))

    def test_extracts_json_code_block(self):
        raw = "before\n```json\n{\"valid\": true}\n```\nafter"
        self.assertEqual('{"valid": true}', validator.extract_json_from_markdown(raw))

    @staticmethod
    def schema(name: str) -> dict:
        return json.loads((SCHEMAS / name).read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
