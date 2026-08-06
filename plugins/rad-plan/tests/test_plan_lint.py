import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Tuple


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
LINTER = PLUGIN_ROOT / "scripts" / "plan-lint.py"
EXAMPLES = PLUGIN_ROOT / "examples"


def run_lint(path: Path) -> Tuple[int, dict]:
    result = subprocess.run(
        [sys.executable, str(LINTER), str(path), "--json"],
        check=False,
        capture_output=True,
        text=True,
    )
    return result.returncode, json.loads(result.stdout)


class PlanLintTests(unittest.TestCase):
    def test_all_examples_are_clean(self):
        for path in sorted(EXAMPLES.glob("*.md")):
            with self.subTest(path=path.name):
                code, report = run_lint(path)
                self.assertEqual(0, code, report["issues"])
                self.assertEqual("7.1", report["contract_version"])

    def test_duplicate_section_is_high(self):
        source = (EXAMPLES / "quick-feature-plan.md").read_text(encoding="utf-8")
        report = self._lint_text(source + "\n## Scope\n\nDuplicate.\n")
        self.assert_issue(report, "HIGH", "Duplicate section")

    def test_undefined_outcome_task_is_high(self):
        source = (EXAMPLES / "quick-feature-plan.md").read_text(encoding="utf-8")
        changed = source.replace("| T1, T2 |", "| T99 |", 1)
        report = self._lint_text(changed)
        self.assert_issue(report, "HIGH", "references undefined task 'T99'")

    def test_missing_file_label_is_high(self):
        source = (EXAMPLES / "quick-feature-plan.md").read_text(encoding="utf-8")
        changed = source.replace("[existing] `src/settings/store.ts`", "`src/settings/store.ts`", 1)
        report = self._lint_text(changed)
        self.assert_issue(report, "HIGH", "lacks [existing] or [new]")

    def test_unsafe_rollback_is_high(self):
        source = (EXAMPLES / "quick-feature-plan.md").read_text(encoding="utf-8")
        changed = source.replace(
            "Revert the isolated task commit and confirm the previous settings tests pass.",
            "Run `git reset --hard HEAD`.",
            1,
        )
        report = self._lint_text(changed)
        self.assert_issue(report, "HIGH", "Unsafe rollback command form")

    def test_none_with_dependency_is_high(self):
        source = (EXAMPLES / "quick-feature-plan.md").read_text(encoding="utf-8")
        changed = source.replace("**Depends on:** T1", "**Depends on:** none and T1", 1)
        report = self._lint_text(changed)
        self.assert_issue(report, "HIGH", "says 'none' and also names a dependency")

    def _lint_text(self, text: str) -> dict:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "custom-plan.md"
            path.write_text(text, encoding="utf-8")
            _, report = run_lint(path)
            return report

    def assert_issue(self, report: dict, severity: str, message: str):
        self.assertTrue(
            any(issue["severity"] == severity and message in issue["message"] for issue in report["issues"]),
            report["issues"],
        )


if __name__ == "__main__":
    unittest.main()
