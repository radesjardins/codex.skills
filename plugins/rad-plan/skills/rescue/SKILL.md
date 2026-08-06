---
name: rescue
description: >
  Use when an existing project has unclear status, missing or stale documents,
  abandoned work, or uncertain intent: rescue this project, get it back on track,
  untangle it, or determine where it stands. Performs read-only project archaeology,
  asks evidence-led keep/cut/unknown questions, can draft a missing PRD from approved
  answers, and creates a checked release-map plan. It never fixes or runs application code.
---

# Rescue

Recover project intent from repository evidence, then create an approved plan from the state that exists now.

Do not modify, run, build, test, delete, or clean up application code. Needed repairs become plan tasks.

## Resolve paths and write boundary

Resolve the plugin root as the directory two levels above this `SKILL.md`. Read `references/discovery-interview.md` and `references/plan-template.md`.

Allowed writes:

- the detected plan path or new `docs/plan.md`;
- a missing or skeletal `docs/prd.md`, only from confirmed answers and after section approval;
- append-only entries in existing decisions or ideas files after owner approval.

Put other confirmed document changes in `## Durable follow-ups`. Do not create architecture, API, decisions, ideas, status, roadmap, or update-prompt files.

## Companion-skill rule

Name a RAD Repo or RAD Brainstorm skill only when current evidence needs the exact workflow, the exact skill appears in the current available-skill list, and it would add clear value. Report the need in plain language when absent. Never invoke a suggested companion unless the owner asks or accepts.

If repository structure is also unclear, explain the structure problem. Suggest `rad-repo:adopt` only under this rule. Continue with built-in defaults when it is absent or declined.

## 1. Build the state report

Read in bounded batches:

- manifests, top-level config, entry points, and directory shape;
- the latest 30 commits, last activity date, and current worktree status;
- README, `AGENTS.md`, and current Markdown documents;
- TODO, FIXME, HACK, and XXX markers;
- likely half-built routes, exports, components, tests, and configuration.

Do not run the project. Label every conclusion as evidence, inference, or unknown.

Present:

```text
State of the project:
Likely goal: <evidence-backed inference>
Looks complete: <artifacts and evidence>
Half-built: <artifacts and missing link>
Unknown without running: <items>
Last activity: <date and final work>
Document state: <missing, stale, or conflicting>
```

## 2. Recover intent

Use the discovery interview with an evidence-led form. Start questions with what the repository suggests.

For each major existing part, ask the owner to choose:

- keep;
- cut;
- unknown.

Use quick or full depth under the `plan` skill rules. Quick uses one batch of no more than five unresolved questions. Full uses up to three rounds. Mirror the project back and propose assumptions for confirmation.

For full rescue, offer to draft a missing or skeletal PRD from confirmed answers. For quick rescue, draft it only when the owner asks.

## 3. Check the implementation surface

After scope is settled, inspect the entry point, affected modules, nearest tests, and relevant config. Use a budget of 12 files for quick and 30 for full. Mark plan paths `[existing]` or `[new]`. Keep uncertain paths inside a bounded discovery task.

## 4. Plan from current reality

Build the plan with the contract in `references/plan-template.md`:

1. Start Now from the current project state.
2. Make the first milestone stabilize and verify when current behavior is unknown.
3. Put kept half-built parts into exact tasks.
4. Put cuts in non-goals and preserve the owner decision.
5. Map every live outcome to tasks and final proof in `## Outcome coverage`.
6. Use two or three tasks per milestone when practical.
7. Warn above five tasks in a milestone or 20 live tasks in the plan.
8. Use safe recovery rules and focused validation.
9. Set Status to DRAFT and include the 7.1 contract marker.

## 5. Check and approve

Run `plan-lint.py` against the detected plan path. Fix CRITICAL and HIGH findings.

Run the risk process for the chosen depth:

- Quick: one pass, then surface unresolved blocking issues.
- Full: one first pass, then repeat only after REVISE and plan changes, with three total passes maximum.
- RETHINK: stop for the owner. Suggest an exact `rad-brainstorm:*` skill only under the companion-skill rule.

Present the state report, release map, outcome coverage, decisions, milestones, tasks, and check results. Keep the plan DRAFT until owner approval. After approval, set it to APPROVED, append only to existing shelf files, and run the linter once on the final plan.

## Boundaries

- Treat inference as inference.
- Let the owner decide what to salvage.
- Keep source changes and project execution outside rescue.
- Do not invoke companion skills without owner acceptance.
