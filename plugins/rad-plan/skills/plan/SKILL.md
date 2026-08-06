---
name: plan
description: >
  Use when the user wants a structured, risk-first implementation plan before
  coding: plan a project or feature, architect a decided build, break work into
  executable tasks, or map the work. Runs an evidence-backed interview, checks
  the relevant code surface, builds a Now/Next/Later release map, writes one
  maintained plan, validates it, and routes confirmed follow-ups without writing
  application code. Do not use it to rescue a project whose current state is unclear.
---

# Plan

Produce an approved implementation plan that a solo owner can read and a fresh coding agent can execute.

Do not write application code or source files. Planning artifacts are the only allowed output.

## Resolve paths

Resolve the plugin root as the directory two levels above this `SKILL.md`. Convert each referenced plugin path to an absolute path before reading or running it.

Read `references/plan-template.md` as the authority for the plan contract. A repository `AGENTS.md` document model overrides its default names and headings.

## Write boundary

- Write the current plan at the detected plan path. Use `docs/plan.md` for a new plan.
- Create `docs/prd.md` only when it is missing or skeletal, only from confirmed interview answers, and only after section approval.
- Append confirmed decisions or ideas only when `docs/decisions.md` or `docs/ideas.md` already exists.
- Put other confirmed document changes in the plan's optional `## Durable follow-ups` section.
- Do not create decisions, ideas, architecture, API, status, roadmap, timeline, or update-prompt files.
- Propose an `AGENTS.md` stack block in chat when useful. Write it only after separate owner approval.

## Companion-skill rule

Name a RAD Repo or RAD Brainstorm skill only when all conditions are true:

1. Current evidence needs that exact workflow.
2. The exact skill appears in the current available-skill list.
3. Using it would add clear value for this project.

When a companion is absent, report the need in plain language. Never invoke a companion from a suggestion unless the owner asks for it or accepts the suggestion.

The public brainstorming plugin namespace is `rad-brainstorm:*`.

## 1. Understand the work

Read `references/discovery-interview.md`.

### Route first

- Use `rescue` when the project goal or current state is unclear.
- Use `replan` when a real plan exists and work has changed or shipped since it was written.
- Continue here for greenfield work or a clear next effort.

If the idea is still undecided, explain which product or design questions must be settled. Suggest an exact `rad-brainstorm:*` skill only under the companion-skill rule.

If a bare repository has no `AGENTS.md` and no `docs/`, explain that a small repository contract would help. Suggest `rad-repo:repo-init` only under the companion-skill rule. Continue with built-in defaults when it is unavailable or declined.

### Read evidence before questions

For an existing repository, read in one batch when present:

- `docs/prd.md`, `docs/handoff.md`, the current plan, and `AGENTS.md`;
- `README.md`, the manifest, and top-level configuration;
- dated `docs/*-spec.md` and `docs/*-design.md`, newest first;
- the top-level directory shape.

Treat the PRD as product authority. Confirm facts from the repository instead of asking the owner to repeat them. Surface contradictions as questions.

### Choose depth

Ask once whether the owner wants quick or full planning. Recommend:

- **Quick:** one known change in one system with no new service, deployment target, auth, payment, personal-data, or schema risk.
- **Full:** a new product, unclear architecture, cross-system work, migration, auth, payment, personal data, or new deployment target.

The owner decides.

### Run discovery

Full planning uses the eight coverage areas, mirror-back step, and no more than three question rounds from `discovery-interview.md`.

Quick planning uses:

- one evidence pass;
- one batch of no more than five unresolved questions;
- one mirror-back;
- one assumption confirmation;
- no PRD draft unless the owner asks.

Anything still open becomes an explicit assumption or risk.

For full planning, offer the PRD gap check from `discovery-interview.md`. Confirm each proposed section before writing.

### Check the implementation surface

After scope is settled and before task paths are written, inspect the likely implementation surface.

1. Find the entry point, affected module, nearest tests, and relevant configuration.
2. Read only those files and their direct callers or imports when needed.
3. Use a budget of 12 files for quick and 30 files for full.
4. Mark every planned path as `[existing]` or `[new]`.
5. When a path remains uncertain, make bounded discovery part of the task instead of inventing a path.

Stop the read when the task boundary is clear. Do not build a permanent code map.

## 2. Decide the stack only when needed

Skip this step when the current stack can meet the requirement and the work adds no new platform, service, or dependency.

When a real choice exists, read `references/golden-path-matrix.md` and dispatch one bounded, read-only `stack_advisor` subagent using `references/subagent-prompts/stack-eval.md`. Require JSON-only output and no file edits. Pass the project context, current stack, mode, and absolute plugin root.

Validate the result:

```bash
python <plugin-root>/scripts/validate-json.py \
  <plugin-root>/references/subagent-prompts/stack-eval.schema.json - --extract-from-markdown
```

Use `python3` when that is the repository command. Re-prompt once on schema failure. Stop for the owner when requirements conflict or no supported option fits.

Record only the final choice and short reason in the plan. Put any confirmed durable change in `## Durable follow-ups` or append it to an existing decisions file after approval.

## 3. Build the plan

Read these references in one batch:

- `references/plan-template.md`;
- `references/failure-state-template.md`;
- `references/tdd-constraints.md`;
- `references/context-management.md`;
- `references/anti-patterns.md`.

Build in this order:

1. Write the Now, Next, and Later release map. Only Now receives tasks.
2. Define observable outcomes for Now.
3. Map each outcome to at least one task and one final proof in `## Outcome coverage`.
4. Decompose Now goal-backward into shippable milestones.
5. Put the hardest unknown first when it can invalidate later work.
6. Aim for two or three tasks per milestone. Warn above five.
7. Warn and ask for a smaller current release when the live plan exceeds 20 tasks.
8. Give every task the six fields from the plan contract.
9. Use `[existing]` and `[new]` labels in Files.
10. Add a checkpoint after each milestone.
11. Use safe recovery rules from `failure-state-template.md`.
12. Put task-specific test detail in Validate using `tdd-constraints.md`.

Write the draft with `**Status:** DRAFT` and the 7.1 contract marker.

## 4. Check the plan

Run the mechanical check against the detected plan path:

```bash
python <plugin-root>/scripts/plan-lint.py <plan-path> --json
```

Fix CRITICAL and HIGH findings before judgment review.

Dispatch one bounded, read-only `risk_assessor` subagent with the detected plan path and `references/subagent-prompts/risk-assessment.md`. Require JSON-only output and no file edits. Validate it with `validate-json.py` and the risk schema.

- **Quick:** run one risk pass. Fix blocking issues once and surface anything unresolved.
- **Full:** run one first pass. Repeat only after a `REVISE` result and only after the plan changes. Stop after three total passes.
- **RETHINK:** stop and explain the product, scope, or architecture decision that needs more work. Suggest an exact `rad-brainstorm:*` skill only under the companion-skill rule.

## 5. Review with the owner

Present in this order:

1. Four to six plain sentences about the product, Now release, next horizon, and largest risk.
2. The release map.
3. The outcome coverage table.
4. Three to five decisions inside the plan.
5. Milestones and After this ships lines.
6. Task detail, lint result, and risk result.

Ask: "Does this match what you are trying to build? What should change before I approve it?"

The plan stays DRAFT until the owner approves it. Challenge one risky choice once with its cost and your recommendation. If the owner confirms it, record the decision and continue without repeating the objection.

## 6. Approve and finish

After approval:

1. Change the status to APPROVED and update the date.
2. Append confirmed decisions and ideas only to shelf files that already exist.
3. Keep absent-shelf entries and other document changes in `## Durable follow-ups`.
4. Propose a useful `AGENTS.md` stack block in chat when needed.
5. Run `plan-lint.py` once on the final plan and report the result.

## Plan location

Detect the current plan in this order:

1. `docs/plan.md`
2. `docs/planning/current-execution.md`
3. `docs/planning/current.md`
4. `PLAN.md`

Use `replan` when real work happened after the current plan. Update a stub in place. Create a new plan at `docs/plan.md`.

## Context use

Batch independent reads. Keep user approvals and workflow steps in order. Load only references required by the current step.
