import importlib.util
import json
import sys
import unittest
from unittest import mock
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = PLUGIN_ROOT / "scripts" / "validate-json.py"
SCHEMAS = PLUGIN_ROOT / "references" / "subagent-prompts"


def load_validator():
    spec = importlib.util.spec_from_file_location("rad_brainstorm_validate_json", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


validator = load_validator()


class ValidateJsonTests(unittest.TestCase):
    def test_valid_domain_research(self):
        payload = {
            "research_complete": True,
            "topic": "Example topic",
            "answer": "The current constraint is clear.",
            "common_approaches": ["Existing approach"],
            "key_constraints": ["Current rule"],
            "pain_points": ["Manual work"],
            "recent_developments": ["A current change"],
            "failed_approaches": [{"approach": "Old attempt", "why_it_failed": "Poor fit"}],
            "opportunity_signals": ["Unmet need"],
            "transferable_patterns": [{
                "source_domain": "Adjacent field",
                "pattern": "Small batches",
                "applicability": "Reduces risk",
            }],
            "contested_or_uncertain": [],
            "surprises": [],
            "sources": [{"title": "Primary source", "url": "https://example.com", "date": "2026-08-06"}],
            "confidence": "high",
            "searches_used": 6,
        }
        self.assertEqual([], validator.validate(payload, self.schema("domain-research.schema.json")))

    def test_valid_idea_challenge(self):
        payload = {
            "challenge_complete": True,
            "research_used": True,
            "sources": [{
                "title": "Primary source",
                "url": "https://example.com",
                "date": "2026-08-06",
                "supports": "Current demand evidence",
            }],
            "ideas": [{
                "id": "I1",
                "description": "Example idea",
                "assessment": "promising_with_gaps",
                "confidence": "medium",
                "riskiest_assumptions": [{
                    "assumption": "Users need it",
                    "category": "desirability",
                    "evidence_level": "untested",
                    "matters_because": "Demand is unknown",
                }],
                "pre_mortem": [{
                    "scenario": "Users ignore it",
                    "likelihood": "M",
                    "preventable": "Y",
                    "mitigation": "Test demand first",
                }],
                "blind_spots": ["New users"],
                "strengths": ["Small scope"],
                "recommendations": ["Run a demand test"],
                "cheapest_proof": {
                    "test": "Ask five target users to try the workflow",
                    "pass_threshold": "At least three complete it without help",
                    "stop_signal": "Fewer than two can state the value",
                },
            }],
            "cross_idea_notes": "One idea was supplied.",
        }
        self.assertEqual([], validator.validate(payload, self.schema("idea-challenge.schema.json")))

    def test_valid_spec_review(self):
        payload = {
            "review_complete": True,
            "iteration": 1,
            "status": "approved",
            "blocking_issues": [],
            "advisory_recommendations": [],
            "assessment": "The spec is ready for planning.",
            "escalation_required": False,
            "unresolved_issues": [],
        }
        self.assertEqual([], validator.validate(payload, self.schema("spec-review.schema.json")))

    def test_invalid_challenge_rejects_unknown_assessment(self):
        payload = {
            "challenge_complete": True,
            "research_used": False,
            "sources": [],
            "ideas": [{
                "id": "I1",
                "description": "Example idea",
                "assessment": "perfect",
                "confidence": "high",
                "riskiest_assumptions": [],
                "pre_mortem": [],
                "blind_spots": [],
                "strengths": [],
                "recommendations": [],
                "cheapest_proof": {
                    "test": "Run a small trial",
                    "pass_threshold": "One clear success",
                    "stop_signal": "No useful result",
                },
            }],
            "cross_idea_notes": "",
        }
        errors = validator.validate(payload, self.schema("idea-challenge.schema.json"))
        self.assertTrue(any("assessment" in error["path"] for error in errors), errors)

    def test_extracts_json_code_block(self):
        raw = "before\n```json\n{\"valid\": true}\n```\nafter"
        self.assertEqual('{"valid": true}', validator.extract_json_from_markdown(raw))

    def test_builtin_rejects_missing_field_and_extra_property(self):
        schema = {
            "type": "object",
            "additionalProperties": False,
            "required": ["name"],
            "properties": {"name": {"type": "string"}},
        }
        with mock.patch.object(validator, "HAS_JSONSCHEMA", False):
            errors = validator.validate({"unexpected": True}, schema)
        messages = {error["message"] for error in errors}
        self.assertIn("required field missing", messages)
        self.assertIn("additional property not allowed", messages)

    def test_builtin_rejects_empty_sources_when_research_was_used(self):
        schema = self.schema("idea-challenge.schema.json")
        payload = {
            "challenge_complete": True,
            "research_used": True,
            "sources": [],
            "ideas": [],
            "cross_idea_notes": "No ideas supplied.",
        }
        with mock.patch.object(validator, "HAS_JSONSCHEMA", False):
            errors = validator.validate(payload, schema)
        self.assertTrue(any("sources" in error["path"] for error in errors), errors)

    def test_builtin_rejects_empty_required_text_and_zero_searches(self):
        schema = {
            "type": "object",
            "required": ["answer", "searches_used"],
            "properties": {
                "answer": {"type": "string", "minLength": 1},
                "searches_used": {"type": "integer", "minimum": 1},
            },
        }
        with mock.patch.object(validator, "HAS_JSONSCHEMA", False):
            errors = validator.validate({"answer": "", "searches_used": 0}, schema)
        self.assertEqual(2, len(errors), errors)

    @staticmethod
    def schema(name):
        return json.loads((SCHEMAS / name).read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
