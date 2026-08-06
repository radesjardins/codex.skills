# RAD Plan scripts

Both scripts use Python 3.8 or later and the standard library. Use `python3` or the repository's approved Python command.

## plan-lint.py

```bash
python scripts/plan-lint.py docs/plan.md
python scripts/plan-lint.py docs/plan.md --json
```

Checks:

- required sections and empty sections;
- duplicate H2 sections;
- the six task fields;
- duplicate task IDs;
- missing, self, contradictory, and cyclic dependencies;
- Outcome coverage task links and final proof;
- `[existing]` and `[new]` labels in 7.1 plans;
- vague Done when, Validate, and outcome proof phrases;
- more than 20 live tasks;
- unsafe rollback command forms.

Plans without `<!-- rad-plan-contract: 7.1 -->` use legacy compatibility. Missing Outcome coverage is advisory for them. It is blocking for 7.1 plans.

Exit codes:

- `0`: no CRITICAL or HIGH issue;
- `1`: at least one CRITICAL or HIGH issue;
- `2`: script error.

## validate-json.py

```bash
python scripts/validate-json.py <schema.json> <data.json>
python scripts/validate-json.py <schema.json> - --extract-from-markdown
```

Checks stack-advisor and risk-assessor output against their JSON schemas. It uses `jsonschema` when installed and a built-in subset otherwise.

## Focused tests

```bash
python -m unittest discover -s tests -p "test_*.py"
```

The tests cover clean examples, duplicate sections, outcome links, path labels, unsafe rollback, contradictory dependencies, and both JSON contracts.
