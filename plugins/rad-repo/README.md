# rad-repo

Repository context, contract, and lifecycle management for Codex. The plugin keeps
agent-facing documentation authoritative, discovers scoped instructions, validates
finite initiatives, and gates shipping on reviewed changes and repository-declared
checks.

## Context stack

| Level | Source | Purpose |
|---|---|---|
| L0 | root and scoped `AGENTS.md` | Repository defaults plus non-duplicative subtree overlays |
| L1 | `docs/handoff.md` | Current state, next action, validation evidence, watchouts |
| L2 | `docs/decisions.md`, `docs/lessons.md` | Durable constraints and proven lessons |
| L3 | `docs/prd.md`, `docs/plan.md`, `docs/design.md`, `docs/initiatives/*.md` | Intent, approved change, and finite migration packets |
| L4 | `docs/archive/` | Historical context, read only when deliberately retrieved |

The canonical contract is `references/shelf-spec.md`. Authority is domain-specific:
instructions and ADRs govern constraints, the PRD governs product intent,
architecture/API/code describe current state, the plan and active initiatives govern
approved future work, and handoff records session state.

## Skills

| Skill | Purpose |
|---|---|
| `startup` | Read-only orientation, instruction map, trust report, mechanical scans |
| `wrapup` | Refresh handoff with Git evidence and validation results |
| `ship` | Review and stage intended paths, run the pre-ship gate, commit, push, verify |
| `repo-init` | Create the minimal greenfield context container |
| `adopt` | Archaeology-first brownfield onboarding without code edits |
| `repo-align` | Deep context, instruction, initiative, vocabulary, and drift correction |

## Repository contract

Validation commands come from labeled backtick commands in applicable `AGENTS.md`
files and optional `.rad-repo.json` entries. Root instructions are defaults;
the closest scoped `AGENTS.md` adds commands and constraints for changed paths.

Start from `templates/repo.json` when configuration is useful. It supports:

- vocabulary modes `advisory`, `strict`, and `off`, with `all` or `headings` scope;
- global and path-scoped validation commands;
- an explicit empty-validation exception for repositories with nothing executable;
- protected paths, generated-directory rules, and a staged-file size limit.

`ship` never uses `git add -A`. It stages reviewed paths and runs:

```bash
python scripts/pre_ship.py . --run-validation --json
```

The gate blocks secrets, protected paths, unexpected generated output, large files,
failed checks, and missing validation declarations. Contract changes require staged
diff review plus `--allow-contract-change`; unstaged contract edits always block.

## Active initiatives

Use `docs/initiatives/<slug>.md` only for an approved, finite migration too detailed
for `docs/plan.md`. Copy `templates/initiative.md`; every initiative must name its
owner, status, baseline, linked plan, retirement condition, archive target,
acceptance criteria, and rollback strategy. Archive it when its retirement trigger
fires.

## Scripts and tests

Scripts use only the Python standard library and Git CLI. See `scripts/README.md` for
their exact enforcement boundaries.

```bash
python scripts/tests/run_all.py
```

The regression suite covers mechanical scanning, scoped contracts, staged-change
safety, vocabulary profiles, Git-aware freshness, locked-constraint conflicts,
redundancy heuristics, Unicode paths, symlink boundaries, missing history, and the
user-owned instruction audit.

## Interaction contract

- Ask before destructive actions, contract changes, or unresolved structural edits.
- Preserve user-owned instruction content unless explicitly authorized to rewrite it.
- Challenge once with evidence, then commit to the owner's decision.
- Do not present heuristic findings as semantic proof.
- Never commit secrets, force-push, or push/deploy unless the invoked workflow grants
  that authorization.
