# RAD Brainstorm scripts

`validate-json.py` runs JSON Schema validation on output from optional Codex research and review subagents.

```text
python scripts/validate-json.py references/subagent-prompts/domain-research.schema.json result.json
python scripts/validate-json.py references/subagent-prompts/idea-challenge.schema.json - --extract-from-markdown
python scripts/validate-json.py references/subagent-prompts/spec-review.schema.json result.json --json
```

The script uses Python 3.8 or later and has no required third-party packages.
