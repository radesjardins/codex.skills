# Plan Contract 7.1

This file is the authority for the RAD Plan output. New plans use one maintained file: `docs/plan.md`. A detected legacy plan can stay at its current path.

RAD Plan may create a missing PRD from confirmed interview answers. It may append confirmed choices or ideas to existing `docs/decisions.md` and `docs/ideas.md`. It does not create those shelf files, architecture or API documents, or a temporary update-prompt. Other durable changes go in `## Durable follow-ups` inside the plan.

## Vocabulary

- **Goal:** one product end state, stored in the PRD.
- **Release:** Now, Next, or Later.
- **Milestone:** a shippable part of Now.
- **Task:** one bounded work item.

Use Goal and Release in the PRD. Use Milestone and Task in the plan. A repository `AGENTS.md` document model can replace these defaults.

## Plan template

```markdown
# Plan: [Project Name]

**Status:** [DRAFT | APPROVED | IN PROGRESS | COMPLETED]
**Updated:** [YYYY-MM-DD]
<!-- rad-plan-contract: 7.1 -->

> **How to read this plan:** The Release map shows where this work fits. Milestones
> are shippable parts of Now. Each task gives a coding agent the exact outcome,
> files, dependencies, proof, and recovery need. Stop conditions require owner input.

## Objective

[What this builds and why it matters now.]

**End goal:** [The confirmed product end state.]

## Release map

- **Now - [name] (this plan):** [Current release outcome]
- **Next - [name]:** [Three to six outline bullets, no task blocks]
  - [Outline]
- **Later - the end goal:** [Theme bullets]
  - [Theme]

## Scope

**In scope:**
- [Committed capability]

**Out of scope / non-goals:**
- [Deliberate exclusion]

## Key assumptions

- [YYYY-MM-DD] [Confirmed assumption]

## Stack

[Include only when a stack decision ran. State the choice and short reason.]

## Outcome coverage

| Outcome | Covered by | Final proof |
|---|---|---|
| O1 - [Observable user or system outcome] | T1, T2 | `[Focused final check]` |

## Milestones

| # | Milestone | Ships | Key artifacts |
|---|---|---|---|
| M1 | [Theme] | [Shippable result] | [Files or components] |

## Tasks

### M1 - [Theme]

*After this ships: [What the user can do or see.]*

- **T1 - [title]**
  - **Objective:** [One clear outcome]
  - **Files:** [existing] `path/to/current.file`; [new] `path/to/new.file`
  - **Depends on:** [none | T2, T3]
  - **Done when:** [Observable and measurable result]
  - **Validate:** `[Focused command or exact review condition]`
  - **Rollback:** [Safe recovery strategy. Name manual recovery when no safe automatic path exists.]

## Checkpoints

### After M1

- **Gate:** [Tasks and owner checks complete]
- **Validate:** `[Milestone check]`
- **Rollback:** [Safe milestone recovery strategy]

## Risks & mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| [Risk] | [Low/Med/High] | [Low/Med/High] | [Action] |

## Validation

- `[Final command]` - [Expected result]

## Stop conditions

- [Condition that requires owner input]

## Durable follow-ups

- [Target document and confirmed change, or omit this section when none exist]
```

## Enforced rules

1. New plans include `<!-- rad-plan-contract: 7.1 -->`.
2. Every live task has the six fields shown above.
3. Each Files entry starts with `[existing]` or `[new]` and entries use semicolons.
4. Existing paths are checked during the bounded implementation-surface read. New paths are marked `[new]`.
5. Every Outcome coverage row names at least one live task and one final proof.
6. Task dependencies resolve and contain no cycles.
7. Done when and Validate use concrete checks.
8. Rollback follows `failure-state-template.md` and contains no destructive Git or recursive-delete command.
9. A checkpoint follows every milestone.
10. Only Now has task detail.
11. A milestone over five tasks and a live plan over 20 tasks require a split warning and owner review.
12. Shipped work moves to `## Shipped` and remains outside `## Tasks`.
13. An invalidated assumption is struck through and kept.

## Durable follow-ups

Use this optional section when planning changes an existing PRD, design, architecture, API contract, or repository instruction that RAD Plan does not own.

Each line names:

- the target file;
- the confirmed change;
- why it changed;
- the skill or owner who should apply it, when known and available.

If `docs/decisions.md` or `docs/ideas.md` already exists, RAD Plan can append confirmed entries there after approval. If either file is absent, keep the entry in this section. Do not create a shelf file.

## Compatibility

Plans without the 7.1 marker are legacy plans. The linter checks their current structure and reports the missing Outcome coverage section as advisory. It enforces Outcome coverage and file labels for 7.1 plans.
