# Claude to Codex Port Checklist

## Hard Failures

A Codex port is not clean if any of these remain in the target package:

- `.codex-plugin/plugin.json` has a `hooks` field.
- A `hooks/` directory is present.
- Hook event names are active setup instructions: `SessionStart`, `PostToolUse`, `PreCompact`, `Stop hook`, `PreToolUse`.
- Runtime variables remain: `CLAUDE_PLUGIN_ROOT`, `CLAUDE_CONFIG_DIR`.
- Hook approval or trust instructions remain.
- Trigger descriptions say to load for all work in a repo.

## Usually Remove

- `CLAUDE.md` and `GEMINI.md` shim templates.
- `sync_to_cache.ps1` and local cache publishing scripts.
- Generated zip/tar distribution artifacts.
- Claude transcript/token usage scripts.
- `__pycache__` and `.pyc` files.

## Replacement Patterns

- `SessionStart` -> `startup`, `status`, or `doctor` skill.
- `PostToolUse` -> explicit validation step in the write skill.
- `PreCompact` -> `wrapup` or handoff skill.
- `Stop hook` -> explicit closeout check.
- `CLAUDE_PLUGIN_ROOT/scripts/foo.py` -> relative path from `SKILL.md` to `scripts/foo.py`.

## Trigger Wording Pattern

Good descriptions use this shape:

`Use when <specific external user task>. Do not use for <nearby repo/app work that is outside scope>.`

Avoid:

`Use whenever working on <project>.`
