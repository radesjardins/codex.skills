# RAD Plugin Converter Design

Date: 2026-08-06  
Status: Approved design, pending written review  
Target standard: Agent Plugins 1.0.0 Working Draft

## Purpose

Replace `claude-to-codex-plugin-port` with `rad-plugin-converter`.

The new plugin will:

- audit Agent Plugin and Agent Skill conformance;
- convert Claude Code plugins to Agent Plugins 1.0.0;
- convert current Codex plugins to Agent Plugins 1.0.0;
- repair safe skill format errors;
- retain working client files when the portable standard has no replacement;
- report behavior that needs a human decision.

The first release will support Agent Plugins 1.0.0 only. It will state that the standard is a working draft.

## Selected Package Strategy

Use an additive portable core.

Each converted Codex package will contain:

- root `plugin.json` for Agent Plugins 1.0.0;
- `skills/<skill-name>/SKILL.md` for portable Agent Skills;
- root `mcp.json` when the package has portable MCP servers;
- `.codex-plugin/plugin.json` while current Codex packaging still needs it;
- other client files only when their owner and use are known.

The root manifest will contain only these Agent Plugins fields:

- `$schema`
- `name`
- `version`
- `description`
- `author`
- `homepage`
- `repository`
- `license`
- `keywords`
- `extensions`

The converter will not put `skills`, hooks, agents, commands, UI data, or marketplace policy in the portable manifest. It will not invent a client extension namespace.

## Plugin Contents

`rad-plugin-converter` will use version `1.0.0` and an MIT license.

It will contain two skills:

1. `audit-plugin`
   - Read-only.
   - Use when the user asks whether a plugin or skill meets the standard.
   - Classify the source format and report errors, warnings, and client-only files.

2. `convert-plugin`
   - Writes only after it has completed the audit and shown the change map.
   - Use for Claude, Codex, mixed, or older Agent Plugin packages.
   - Keep a Claude source unchanged when writing to a separate target.
   - Use additive in-place changes for an existing Codex package.

Both skills will use one standard-library Python tool. Planned commands:

```text
python scripts/rad_plugin_converter.py audit <path> [--json]
python scripts/rad_plugin_converter.py convert <path> --in-place
python scripts/rad_plugin_converter.py convert <source> --target <target>
python scripts/rad_plugin_converter.py marketplace <marketplace-root> [--apply]
```

`marketplace` will be read-only unless `--apply` is present. The tool will return exit code 0 for a conforming result, 1 for conformance findings, and 2 for invalid use or a fatal read error.

## Source Detection

The audit will detect these inputs:

- Agent Plugin: root `plugin.json` has the Agent Plugins 1.0.0 schema.
- Codex plugin: `.codex-plugin/plugin.json` exists.
- Claude Code plugin: `.claude-plugin/plugin.json` exists or Claude package files are present.
- Standalone Agent Skill: the target directory contains `SKILL.md`.
- Mixed package: more than one client format is present.

Detection will use package evidence. It will not classify a package from its name alone.

## Conversion Rules

### Plugin manifest

The converter will create or update root `plugin.json` with the exact 1.0.0 schema URL. It will copy portable metadata from a known manifest. It will keep the source version and license unless the user asks for a change.

An invalid or ambiguous plugin name will stop conversion and ask for a target name. The tool will not silently rename marketplace identities.

### Agent Skills

The audit will check:

- `SKILL.md` is in an immediate child of `skills/`;
- YAML frontmatter exists and closes;
- `name` and `description` exist;
- `name` follows the Agent Skills rules and matches its directory;
- `description` is between 1 and 1024 characters;
- optional `license`, `compatibility`, `metadata`, and `allowed-tools` fields have valid types;
- local Markdown references resolve inside the skill directory;
- skill files do not escape the plugin root through a symlink, junction, or reparse point.

The tool will repair a name mismatch when the directory name is valid and the change has no collision. It will report a missing or weak description for agent review because automatic text could make a false claim. Unsupported Claude frontmatter will be removed only from a separate portable copy. In a shared package, the converter will preserve client behavior or require a user choice.

A `SKILL.md` over 500 lines will be an advisory finding. Size alone is not a conformance failure.

### MCP servers

The converter will place portable MCP data in root `mcp.json` with the exact 1.0.0 schema URL.

It may infer `stdio` when an entry has one executable command and separate arguments. It will not infer whether a URL uses Streamable HTTP or legacy SSE. That choice must come from source evidence or the user.

The audit will reject command strings that contain a shell command, package paths that escape the plugin root, remote non-HTTPS URLs, embedded URL credentials, and secret-looking fixed headers.

### Client-only files

Hooks, custom agents, commands, LSP data, UI data, and marketplace files are outside the portable v1 core.

The conversion report will assign each such file to one of these results:

- retained client compatibility file;
- converted to a skill because on-demand instructions keep the behavior;
- replaced by a portable MCP server;
- left in the unchanged source package;
- removed after its replacement is tested and the user has approved removal.

Unknown files will stay in place and receive a review finding.

## Safety and Failure Handling

- Audit is the default action.
- In-place conversion requires `--in-place`.
- Marketplace writes require `--apply`.
- Target conversion will refuse to overwrite a nonempty unrelated directory.
- The tool will use temporary files and atomic replacement for JSON and frontmatter writes.
- It will make no network calls.
- It will not delete a source Claude package.
- It will report all modified files and unresolved findings.
- A conversion with unresolved errors will return a nonzero exit code.

## Tests

Implementation will start with failing tests for:

1. A Codex plugin receives a portable root manifest and keeps its Codex manifest.
2. A Claude plugin maps portable files and records client-only behavior.
3. A valid Agent Plugin stays unchanged after repeat conversion.
4. A nonconforming skill is detected and safely repaired.
5. A nested skill is reported as undiscoverable.
6. Unknown root manifest fields fail the portable manifest check.
7. A path escape through a symlink or reparse point is rejected.
8. Marketplace audit is read-only without `--apply`.
9. JSON output and exit codes remain stable.

After the focused tests pass, the converter will audit its own package.

## Marketplace Migration

### Public repository

In `R:\Dev\skills\codex.public`:

- rename the plugin directory and marketplace entry to `rad-plugin-converter`;
- update its README and the marketplace README;
- add a portable root manifest to every public plugin;
- audit all public skills;
- keep all public licenses as MIT.

### Private repository

In `R:\Dev\skills\codex`:

- remove the obsolete `claude-to-codex-plugin-port` entry and package;
- use the public `rad-plugin-converter` as the maintained converter;
- add a portable root manifest to each remaining plugin;
- audit all private skills;
- preserve each existing license and third-party credit;
- classify Faunero's root `agents/` files before changing their location or wording.

The migration will not rename private plugins. It will not copy public improvements into private packages unless conformance requires the same change.

## Verification and Handoff

Focused verification will include:

- converter unit tests;
- a clean converter self-audit;
- a clean audit of each converted plugin;
- official Agent Skills validation when the reference tool is available;
- JSON parsing of both marketplace files;
- a Codex marketplace listing check for the retained compatibility packages;
- clean `git status` review in both repositories before handoff.

The final report will list converted plugins, retained compatibility files, skill fixes, unresolved client-only items, tests, and uncommitted changes. Publishing and installation are separate actions unless the user asks for them.

## Sources

- Agent Plugins Specification: https://agent-plugins.org/specification
- Agent Plugins manifest guide: https://agent-plugins.org/plugin-authors/manifest
- Agent Plugins skill guide: https://agent-plugins.org/plugin-authors/skills
- Agent Skills Specification: https://agentskills.io/specification
- Canonical migration example: https://github.com/agentplugins/agent-plugins-example
