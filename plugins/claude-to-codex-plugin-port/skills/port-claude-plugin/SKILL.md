---
name: port-claude-plugin
description: Use when converting a Claude Code plugin or skill into a Codex plugin marketplace package, especially when hooks, CLAUDE_PLUGIN_ROOT, CLAUDE.md/GEMINI.md shims, sync scripts, or overbroad trigger descriptions may cause Codex errors or unwanted skill loading.
---

# Port Claude Code Plugin to Codex

Use this skill only for migration work: converting a Claude Code plugin, Claude skill set, or mixed Claude/Codex package into a clean Codex plugin marketplace entry. Do not use it for ordinary feature work inside the app or repo the plugin supports.

## Goal

Produce a Codex-native package that:

- has a valid `.codex-plugin/plugin.json` manifest;
- is registered in the target Codex `marketplace.json` when requested;
- contains Codex skills with narrow trigger descriptions;
- does not ship unsupported Claude hook wiring;
- replaces hook behavior with explicit Codex skills, scripts, or validation steps;
- avoids Claude runtime variables such as `CLAUDE_PLUGIN_ROOT` and `CLAUDE_CONFIG_DIR`;
- validates cleanly before handoff.

## Required Inputs

Identify these paths before editing:

- Source Claude plugin or skill root.
- Target Codex marketplace root.
- Target plugin root, usually `<marketplace-root>/plugins/<plugin-name>`.
- Optional old marketplace manifest to remove the source from.

If any path is ambiguous, inspect the directory layout first. Do not assume `R:\Dev` itself is the project.

## Migration Procedure

1. Inventory the source package.
   - Read source manifest, README, skill descriptions, scripts, references, templates, and marketplace files.
   - Run `python ../../scripts/audit_claude_port.py <source-root>` from this skill, or run the same script by absolute path.
   - Treat findings as blockers until they are either removed or intentionally rewritten.

2. Create the Codex package.
   - Ensure `.codex-plugin/plugin.json` exists and validates.
   - Keep `skills` as `./skills/` unless the package has a specific reason not to.
   - Do not include unsupported manifest fields such as `hooks`.
   - Add or update the target `marketplace.json` with `source.path` set to `./plugins/<plugin-name>`.

3. Remove unsupported hook assets.
   - Delete `hooks/` directories from the Codex package.
   - Delete hook-only scripts such as `hook_sessionstart.py`, `hook_postwrite.py`, or equivalents unless they are rewritten as ordinary explicit validators.
   - Remove docs that ask the user to approve or trust hooks that Codex will not run.

4. Replace hook behavior with Codex behavior.
   - SessionStart behavior becomes an explicit `startup`, `status`, or `doctor` skill.
   - PostToolUse write guards become explicit validation scripts called by the relevant skill.
   - PreCompact behavior becomes an explicit `wrapup` or handoff skill.
   - Stop nudges become explicit closeout/status checks.

5. Scrub Claude-specific assumptions.
   - Replace `CLAUDE_PLUGIN_ROOT` paths with paths relative to the active `SKILL.md` file.
   - Remove `CLAUDE_CONFIG_DIR`, Claude transcript readers, cache sync scripts, and generated zip artifacts from the Codex package.
   - Remove `CLAUDE.md` and `GEMINI.md` shims unless the user explicitly asks for cross-agent templates.
   - Rewrite references to Claude slash commands as Codex skill names or plain skill invocations.

6. Fix trigger descriptions.
   - Descriptions must name the task, not merely the repo.
   - Reject descriptions like `Use whenever working on <repo>`.
   - For domain plugins whose name collides with an app repo, explicitly say when not to use the skill.
   - Example: `Use only for Faunero place-curation data work, not for general Faunero app development.`

7. Validate.
   - Run `validate_plugin.py <plugin-root>`.
   - If standalone skills are created, run `quick_validate.py <skill-root>`.
   - Run relevant package tests directly with `PYTHONDONTWRITEBYTECODE=1` so no `__pycache__` files are created.
   - Re-run `audit_claude_port.py <target-plugin-root>` and resolve remaining high-risk findings.
   - Confirm there are no `hooks/`, `__pycache__`, or `.pyc` artifacts in the target package.

8. Sync and publish only after validation.
   - Review `git status` in each affected repo.
   - Commit marketplace additions and removals separately when they are in different repos.
   - Push only when requested or when the task explicitly includes syncing the marketplace.

## Required Final Report

Report:

- source and target paths;
- whether hooks were removed or rewritten;
- marketplace files changed;
- validation commands and results;
- any remaining intentional Claude references;
- commits or push status if publishing was requested.

## Safety Notes

- In long or previously corrupted Codex threads, avoid custom patch tooling if it has already caused replay errors. Use structured shell edits and validators instead.
- Never delete the source Claude package unless the user explicitly asks. Copy first, validate the Codex package, then remove old marketplace registration if requested.
