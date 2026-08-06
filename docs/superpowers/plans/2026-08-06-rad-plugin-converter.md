# RAD Plugin Converter Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the Claude-only porting plugin with a tested Agent Plugins 1.0.0 converter, then use it to migrate the public and private Codex marketplaces without breaking current Codex packages.

**Architecture:** A small Python command line tool will separate source detection, conformance checks, and safe file conversion. Two Agent Skills will expose read-only audit and writing conversion workflows. Portable root manifests will be additive, while current `.codex-plugin/plugin.json` files remain as Codex compatibility files.

**Tech Stack:** Python 3 standard library, `unittest`, JSON, YAML frontmatter subset parser, Markdown links, PowerShell, Git.

## Global Constraints

- Target Agent Plugins version is exactly `1.0.0`.
- Root manifest schema is exactly `https://agent-plugins.org/schemas/1.0.0/plugin.schema.json`.
- Root MCP schema is exactly `https://agent-plugins.org/schemas/1.0.0/mcp.schema.json`.
- The converter makes no network calls and has no third-party Python dependency.
- Existing `.codex-plugin/plugin.json` files remain for current Codex compatibility.
- Claude source packages remain unchanged unless the user approves removal.
- Marketplace batch conversion is read-only unless `--apply` is present.
- Existing plugin versions, licenses, and third-party credits remain unchanged.
- A `SKILL.md` over 500 lines is advisory only.
- Tests run with `PYTHONDONTWRITEBYTECODE=1`.
- Only focused converter tests and focused RAD Repo scanner tests may run.

---

## File Structure

### New public converter package

- `plugins/rad-plugin-converter/plugin.json`: portable Agent Plugins manifest.
- `plugins/rad-plugin-converter/.codex-plugin/plugin.json`: Codex compatibility and interface data.
- `plugins/rad-plugin-converter/skills/audit-plugin/SKILL.md`: read-only audit workflow.
- `plugins/rad-plugin-converter/skills/convert-plugin/SKILL.md`: conversion workflow and user gates.
- `plugins/rad-plugin-converter/scripts/models.py`: findings, reports, and JSON output types.
- `plugins/rad-plugin-converter/scripts/frontmatter.py`: Agent Skills frontmatter parsing, checks, and safe name repair.
- `plugins/rad-plugin-converter/scripts/audit.py`: package detection, manifest checks, skill discovery, link checks, and containment checks.
- `plugins/rad-plugin-converter/scripts/convert.py`: atomic manifest creation and safe conversion actions.
- `plugins/rad-plugin-converter/scripts/rad_plugin_converter.py`: command line parsing and exit codes.
- `plugins/rad-plugin-converter/scripts/tests/test_frontmatter.py`: skill format tests.
- `plugins/rad-plugin-converter/scripts/tests/test_audit.py`: plugin audit and path tests.
- `plugins/rad-plugin-converter/scripts/tests/test_convert.py`: conversion and repeat-run tests.
- `plugins/rad-plugin-converter/scripts/tests/test_cli.py`: command output and exit-code tests.
- `plugins/rad-plugin-converter/references/agent-plugins-v1.md`: short pinned contract and source links.
- `plugins/rad-plugin-converter/references/conversion-map.md`: portable and client-only artifact mapping.
- `plugins/rad-plugin-converter/README.md`: honest scope, commands, limits, and examples.
- `plugins/rad-plugin-converter/LICENSE`: MIT license.

### Public marketplace files

- `marketplace.json`: replace the old converter name and path.
- `.agents/plugins/marketplace.json`: mirror the converter entry.
- `README.md`: replace the old plugin listing and install command.
- `plugins/*/plugin.json`: add portable manifests to the four other public plugins.

### Private marketplace files

- `R:\Dev\skills\codex\marketplace.json`: remove the obsolete converter entry.
- `R:\Dev\skills\codex\.agents\plugins\marketplace.json`: mirror the removal.
- `R:\Dev\skills\codex\plugins\*/plugin.json`: add portable manifests to all remaining private plugins.
- `R:\Dev\skills\codex\plugins\claude-to-codex-plugin-port\`: remove the approved obsolete duplicate after exact target review.

### RAD Repo files

- `plugins/rad-repo/scripts/repo-scan.py`: report size bands without changing trust from size alone.
- `plugins/rad-repo/scripts/tests/test_repo_scan.py`: prove long current docs remain green.
- `plugins/rad-repo/references/shelf-spec.md`: state preferred and review size bands.
- `plugins/rad-repo/skills/startup/SKILL.md`: report line counts.
- `plugins/rad-repo/skills/wrapup/SKILL.md`: preserve useful detail and offer reduction only with content evidence.
- `plugins/rad-repo/skills/repo-align/SKILL.md`: remove size-only audit triggers.
- `plugins/rad-repo/skills/repo-init/SKILL.md`: replace hard line caps.
- `plugins/rad-repo/templates/AGENTS.md`: replace the hard budget note.
- `plugins/rad-repo/templates/handoff.md`: replace the hard target note.

---

### Task 1: Agent Skill frontmatter contract

**Files:**
- Create: `plugins/rad-plugin-converter/scripts/models.py`
- Create: `plugins/rad-plugin-converter/scripts/frontmatter.py`
- Create: `plugins/rad-plugin-converter/scripts/tests/test_frontmatter.py`

**Interfaces:**
- Produces: `Finding(severity, code, path, message, line=None)`.
- Produces: `parse_frontmatter(path: Path) -> FrontmatterDocument`.
- Produces: `audit_frontmatter(skill_dir: Path, plugin_root: Path) -> list[Finding]`.
- Produces: `repair_skill_name(skill_dir: Path) -> bool`.

- [ ] **Step 1: Write failing frontmatter tests**

```python
def test_valid_folded_description_matches_directory(self):
    skill = self.make_skill("audit-plugin", "name: audit-plugin\ndescription: >\n  Audit plugins. Use when checking conformance.")
    self.assertEqual([], audit_frontmatter(skill, self.root))

def test_name_mismatch_is_reported(self):
    skill = self.make_skill("audit-plugin", "name: wrong-name\ndescription: Use when auditing plugins.")
    self.assertIn("skill-name-mismatch", {item.code for item in audit_frontmatter(skill, self.root)})

def test_metadata_values_must_be_strings(self):
    skill = self.make_skill("audit-plugin", "name: audit-plugin\ndescription: Use when auditing.\nmetadata:\n  count: 3")
    self.assertIn("skill-metadata-value", {item.code for item in audit_frontmatter(skill, self.root)})
```

- [ ] **Step 2: Run the focused tests and confirm failure**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest discover -s plugins/rad-plugin-converter/scripts/tests -p 'test_frontmatter.py' -v
```

Expected: import failure because the new modules do not exist.

- [ ] **Step 3: Implement the narrow frontmatter parser and checks**

Implement support for inline scalars, quoted scalars, folded and literal blocks, and one-level `metadata` string maps. Reject missing delimiters, duplicate or unsupported top-level fields, invalid names, name mismatch, invalid field types, empty descriptions, descriptions over 1024 characters, and compatibility text over 500 characters.

Use the exact name rule:

```python
SKILL_NAME_RE = re.compile(r"^(?!.*--)[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$")
```

- [ ] **Step 4: Run the frontmatter tests and confirm they pass**

Run the command from Step 2. Expected: PASS.

- [ ] **Step 5: Commit Task 1**

```powershell
git add -- plugins/rad-plugin-converter/scripts/models.py plugins/rad-plugin-converter/scripts/frontmatter.py plugins/rad-plugin-converter/scripts/tests/test_frontmatter.py
git commit -m "feat(converter): validate agent skill frontmatter"
```

### Task 2: Package audit and source detection

**Files:**
- Create: `plugins/rad-plugin-converter/scripts/audit.py`
- Create: `plugins/rad-plugin-converter/scripts/tests/test_audit.py`

**Interfaces:**
- Consumes: `Finding`, `audit_frontmatter`.
- Produces: `AuditReport(root, source_types, findings, plugin_name=None)`.
- Produces: `detect_source_types(root: Path) -> tuple[str, ...]`.
- Produces: `audit_path(root: Path) -> AuditReport`.

- [ ] **Step 1: Write failing audit tests**

```python
def test_codex_plugin_without_root_manifest_is_detected(self):
    self.write_json(".codex-plugin/plugin.json", {"name": "sample", "skills": "./skills/"})
    report = audit_path(self.root)
    self.assertEqual(("codex",), report.source_types)
    self.assertIn("missing-portable-manifest", {item.code for item in report.findings})

def test_nested_skill_is_not_discoverable(self):
    self.write_skill("skills/group/deploy", "deploy")
    report = audit_path(self.root)
    self.assertIn("nested-skill", {item.code for item in report.findings})

def test_unknown_manifest_field_is_an_error(self):
    self.write_json("plugin.json", {"$schema": PLUGIN_SCHEMA, "name": "sample", "skills": "./skills"})
    report = audit_path(self.root)
    self.assertIn("manifest-unknown-field", {item.code for item in report.findings})
```

- [ ] **Step 2: Run the audit tests and confirm failure**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest discover -s plugins/rad-plugin-converter/scripts/tests -p 'test_audit.py' -v
```

Expected: import failure because `audit.py` does not exist.

- [ ] **Step 3: Implement package audit**

Validate the closed root manifest, exact schema, plugin name, optional field types, immediate skill discovery, nested `SKILL.md` files, local Markdown links, `mcp.json` top fields, MCP transport shapes, secret-looking headers, and resolved-path containment. Classify hooks, commands, agents, LSP, UI, and marketplace files as client-only information unless source evidence shows they are skill resources.

- [ ] **Step 4: Run the audit tests and confirm they pass**

Run the command from Step 2. Expected: PASS.

- [ ] **Step 5: Commit Task 2**

```powershell
git add -- plugins/rad-plugin-converter/scripts/audit.py plugins/rad-plugin-converter/scripts/tests/test_audit.py
git commit -m "feat(converter): audit agent plugin packages"
```

### Task 3: Safe conversion and command line interface

**Files:**
- Create: `plugins/rad-plugin-converter/scripts/convert.py`
- Create: `plugins/rad-plugin-converter/scripts/rad_plugin_converter.py`
- Create: `plugins/rad-plugin-converter/scripts/tests/test_convert.py`
- Create: `plugins/rad-plugin-converter/scripts/tests/test_cli.py`

**Interfaces:**
- Consumes: `audit_path`, `AuditReport`, portable field constants.
- Produces: `convert_in_place(root: Path) -> ConversionResult`.
- Produces: `convert_to_target(source: Path, target: Path) -> ConversionResult`.
- Produces: `convert_marketplace(root: Path, apply: bool) -> list[ConversionResult]`.
- Produces: CLI commands `audit`, `convert`, and `marketplace`.

- [ ] **Step 1: Write failing conversion tests**

```python
def test_codex_conversion_is_additive_and_repeatable(self):
    self.make_codex_plugin("sample")
    first = convert_in_place(self.root)
    second = convert_in_place(self.root)
    self.assertTrue((self.root / "plugin.json").is_file())
    self.assertTrue((self.root / ".codex-plugin" / "plugin.json").is_file())
    self.assertEqual([], second.changed_files)

def test_marketplace_is_read_only_without_apply(self):
    self.make_marketplace_plugin("sample")
    convert_marketplace(self.root, apply=False)
    self.assertFalse((self.root / "plugins" / "sample" / "plugin.json").exists())
```

- [ ] **Step 2: Run the conversion tests and confirm failure**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest discover -s plugins/rad-plugin-converter/scripts/tests -p 'test_convert.py' -v
python -m unittest discover -s plugins/rad-plugin-converter/scripts/tests -p 'test_cli.py' -v
```

Expected: import failure because conversion modules do not exist.

- [ ] **Step 3: Implement safe conversion**

Build the portable manifest from allowed metadata fields. Infer `stdio` only from a command entry. Use a same-directory temporary file plus `os.replace` for writes. Refuse target overwrite when the target contains unrelated files. Return a nonzero result when errors remain.

- [ ] **Step 4: Implement the command line interface**

```python
parser.add_subparsers(dest="command", required=True)
# audit PATH [--json]
# convert PATH (--in-place | --target TARGET) [--json]
# marketplace ROOT [--apply] [--json]
```

- [ ] **Step 5: Run the conversion and CLI tests and confirm they pass**

Run the command from Step 2. Expected: PASS.

- [ ] **Step 6: Commit Task 3**

```powershell
git add -- plugins/rad-plugin-converter/scripts/convert.py plugins/rad-plugin-converter/scripts/rad_plugin_converter.py plugins/rad-plugin-converter/scripts/tests/test_convert.py plugins/rad-plugin-converter/scripts/tests/test_cli.py
git commit -m "feat(converter): add safe plugin conversion commands"
```

### Task 4: Public converter package and rename

**Files:**
- Create: `plugins/rad-plugin-converter/plugin.json`
- Create: `plugins/rad-plugin-converter/.codex-plugin/plugin.json`
- Create: `plugins/rad-plugin-converter/skills/audit-plugin/SKILL.md`
- Create: `plugins/rad-plugin-converter/skills/convert-plugin/SKILL.md`
- Create: `plugins/rad-plugin-converter/references/agent-plugins-v1.md`
- Create: `plugins/rad-plugin-converter/references/conversion-map.md`
- Create: `plugins/rad-plugin-converter/README.md`
- Create: `plugins/rad-plugin-converter/LICENSE`
- Modify: `marketplace.json`
- Modify: `.agents/plugins/marketplace.json`
- Modify: `README.md`
- Delete: `plugins/claude-to-codex-plugin-port/**`

**Interfaces:**
- Consumes: CLI commands from Task 3.
- Produces: marketplace plugin name `rad-plugin-converter` and skill names `audit-plugin`, `convert-plugin`.

- [ ] **Step 1: Write the two focused Agent Skills**

The audit skill must stay read-only. The conversion skill must require an audit, an artifact map, explicit write mode, validation, and a final change report. Both must point to the bundled script by a path resolved from their own `SKILL.md`.

- [ ] **Step 2: Create matching portable and Codex manifests**

Use version `1.0.0`, MIT, repository `https://github.com/radesjardins/codex.skills`, and homepage path `plugins/rad-plugin-converter`. Keep Codex-only `skills` and `interface` fields only in `.codex-plugin/plugin.json`.

- [ ] **Step 3: Replace marketplace and README names**

Change only the old converter name, path, install command, and description. Keep all other plugin entries unchanged.

- [ ] **Step 4: Remove the old public package after exact file review**

Confirm every old file has a replacement, then remove only `plugins/claude-to-codex-plugin-port`.

- [ ] **Step 5: Run the converter package tests and self-audit**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest discover -s plugins/rad-plugin-converter/scripts/tests -p 'test_*.py' -v
python plugins/rad-plugin-converter/scripts/rad_plugin_converter.py audit plugins/rad-plugin-converter
```

Expected: tests PASS and audit exit code 0.

- [ ] **Step 6: Commit Task 4**

```powershell
git add -- README.md marketplace.json .agents/plugins/marketplace.json plugins/rad-plugin-converter plugins/claude-to-codex-plugin-port
git commit -m "feat: replace Claude port with RAD plugin converter"
```

### Task 5: Convert the public marketplace

**Files:**
- Create: `plugins/rad-brainstorm/plugin.json`
- Create: `plugins/rad-plan/plugin.json`
- Create: `plugins/rad-repo/plugin.json`
- Create: `plugins/rad-para/plugin.json`

**Interfaces:**
- Consumes: `marketplace <root> --apply` from Task 3.
- Produces: five conforming public Agent Plugin packages, including the converter.

- [ ] **Step 1: Run a read-only public marketplace audit**

```powershell
python plugins/rad-plugin-converter/scripts/rad_plugin_converter.py marketplace . --json
```

Expected: four missing portable manifest findings and no writes.

- [ ] **Step 2: Apply the public conversion**

```powershell
python plugins/rad-plugin-converter/scripts/rad_plugin_converter.py marketplace . --apply --json
```

- [ ] **Step 3: Audit the public marketplace again**

Run Step 1 again. Expected: all five plugins conform.

- [ ] **Step 4: Commit Task 5**

```powershell
git add -- plugins/rad-brainstorm/plugin.json plugins/rad-plan/plugin.json plugins/rad-repo/plugin.json plugins/rad-para/plugin.json
git commit -m "chore: add portable manifests to public plugins"
```

### Task 6: Convert the private marketplace and remove the duplicate

**Files:**
- Modify: `R:\Dev\skills\codex\marketplace.json`
- Modify: `R:\Dev\skills\codex\.agents\plugins\marketplace.json`
- Create: `R:\Dev\skills\codex\plugins\*/plugin.json` for each remaining plugin.
- Delete: `R:\Dev\skills\codex\plugins\claude-to-codex-plugin-port\**`.

**Interfaces:**
- Consumes: public converter CLI by absolute path.
- Produces: eight conforming private Agent Plugin packages and no private converter duplicate.

- [ ] **Step 1: Run a read-only private marketplace audit**

```powershell
python R:\Dev\skills\codex.public\plugins\rad-plugin-converter\scripts\rad_plugin_converter.py marketplace R:\Dev\skills\codex --json
```

Expected: missing portable manifest findings and no writes.

- [ ] **Step 2: Classify Faunero root agents**

Search every reference to `plugins/faunero/agents`. Keep the files if active skills or scripts use them. Record them as package resources rather than portable Agent Plugin components.

- [ ] **Step 3: Apply the private conversion**

```powershell
python R:\Dev\skills\codex.public\plugins\rad-plugin-converter\scripts\rad_plugin_converter.py marketplace R:\Dev\skills\codex --apply --json
```

- [ ] **Step 4: Remove the exact obsolete converter files and both entries**

Review resolved paths, confirm the target is `R:\Dev\skills\codex\plugins\claude-to-codex-plugin-port`, remove its known files, and edit only its marketplace entries.

- [ ] **Step 5: Audit the private marketplace again**

Run Step 1 again. Expected: all eight remaining plugins conform.

- [ ] **Step 6: Commit Task 6 in the private repo**

```powershell
git add -- marketplace.json .agents/plugins/marketplace.json plugins/cli-anything-hub/plugin.json plugins/cli-anything-notebooklm/plugin.json plugins/faunero/plugin.json plugins/human-review/plugin.json plugins/rad-para-second-brain/plugin.json plugins/rad-planner/plugin.json plugins/rad-repo-manager/plugin.json plugins/site-ux-audit/plugin.json
git add -u -- plugins/claude-to-codex-plugin-port
git commit -m "chore: adopt Agent Plugins 1.0.0"
```

### Task 7: Cross-marketplace verification

**Files:**
- No production file changes expected.

**Interfaces:**
- Consumes: both converted marketplaces.
- Produces: verification evidence for tests, manifests, marketplace parity, and working tree state.

- [ ] **Step 1: Run the focused converter tests once**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest discover -s plugins/rad-plugin-converter/scripts/tests -p 'test_*.py' -v
```

- [ ] **Step 2: Parse all JSON files changed by conversion**

Use `Get-Content -Raw | ConvertFrom-Json` for both marketplace files and every root `plugin.json`.

- [ ] **Step 3: Check Codex marketplace listing**

Run `codex plugin list` and confirm compatibility packages remain visible. Do not install, remove, or upgrade plugins in this task.

- [ ] **Step 4: Review both worktrees**

Run `git status -sb` and `git diff --check` in both repositories. Stop after clean verification output.

### Task 8: RAD Repo soft size policy

**Files:**
- Modify: `plugins/rad-repo/scripts/repo-scan.py`
- Modify: `plugins/rad-repo/scripts/tests/test_repo_scan.py`
- Modify: `plugins/rad-repo/references/shelf-spec.md`
- Modify: `plugins/rad-repo/skills/startup/SKILL.md`
- Modify: `plugins/rad-repo/skills/wrapup/SKILL.md`
- Modify: `plugins/rad-repo/skills/repo-align/SKILL.md`
- Modify: `plugins/rad-repo/skills/repo-init/SKILL.md`
- Modify: `plugins/rad-repo/templates/AGENTS.md`
- Modify: `plugins/rad-repo/templates/handoff.md`

**Interfaces:**
- Produces: preferred 50 to 100 line band, informational 101 to 250 band, and review note above 250 lines.
- Produces: trust verdicts based on stale, repeated, misleading, or misplaced content rather than size alone.

- [ ] **Step 1: Write a failing focused scanner test**

```python
def test_long_current_handoff_does_not_lower_trust_by_size_alone(self):
    self.write_handoff(lines=251, current=True)
    result = scan_repo(self.root)
    self.assertEqual("green", result["trust"])
    self.assertEqual("review", result["documents"]["handoff"]["size_band"])
```

- [ ] **Step 2: Run only the focused test and confirm failure**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest discover -s plugins/rad-repo/scripts/tests -p 'test_repo_scan.py' -k test_long_current_handoff_does_not_lower_trust_by_size_alone -v
```

Expected: FAIL because size still creates a loose-end finding.

- [ ] **Step 3: Change scanner size findings to document facts**

Report `preferred` for 50 to 100 lines, `informational` for 101 to 250, and `review` above 250. Do not add a loose-end issue from size alone.

- [ ] **Step 4: Update skill and shelf wording**

State that the agent reports counts, checks content quality, offers keep, tighten, or split above 250 lines, and waits for the user before editing useful content.

- [ ] **Step 5: Run the focused scanner test and confirm it passes**

Run the command from Step 2. Expected: PASS. Stop testing after green.

- [ ] **Step 6: Commit Task 8**

```powershell
git add -- plugins/rad-repo/scripts/repo-scan.py plugins/rad-repo/scripts/tests/test_repo_scan.py plugins/rad-repo/references/shelf-spec.md plugins/rad-repo/skills/startup/SKILL.md plugins/rad-repo/skills/wrapup/SKILL.md plugins/rad-repo/skills/repo-align/SKILL.md plugins/rad-repo/skills/repo-init/SKILL.md plugins/rad-repo/templates/AGENTS.md plugins/rad-repo/templates/handoff.md
git commit -m "fix(rad-repo): make document size guidance flexible"
```
