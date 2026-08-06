# AGENTS.md — <PROJECT_NAME>

<ONE_LINE_IDENTITY — what this repo is and its current status; agents read this line first.>

Remote: <REMOTE_URL_OR_TBD>
deploy: <none — set to e.g. `coolify` or `vercel` when a deploy target exists; /ship reads this>

## Stack & commands

- Stack: <LANGUAGE / FRAMEWORK — the planner proposes this block; you apply it>
- Build: `<command>` · Test: `<command>` · Lint: `<command-or-none>` · Run: `<command>`

## Doc model (authoritative for doc structure in this repo)

- Docs live on a fixed shelf under `docs/`: decisions.md, ideas.md, lessons.md,
  design.md, architecture.md, api.md, handoff.md, prd.md, plan.md — each created
  only when first needed — plus `docs/initiatives/` for approved finite migrations
  and `docs/archive/` for history. Nothing else gets written.
- Units of work: Goal → Release (Now/Next/Later) → Milestone (M1…) → Task (T1…).
  Never phase, slice, sprint, epic, stage, or "step" as a tracked unit.
- One writer per file: the planner writes prd.md/plan.md; wrapup/ship overwrite
  handoff.md; anyone appends to decisions/ideas/lessons (no one edits them);
  design.md is the sole source of the design system.
- Full contract: rad-repo `references/shelf-spec.md`.

## How we work

1. Hard-gate (stop and ask) only the irreversible or expensive: prod data, auth,
   payments, deletes, publishing, plus the owner's protected-changes list. Nothing else blocks.
2. Challenge once, then commit: on any pivot or risky choice, one short honest
   assessment; if the owner confirms, log it to docs/decisions.md, execute fully, never relitigate.
3. Mid-session ideas append one line to docs/ideas.md and block nothing — they get
   a fair hearing at /rad-plan:replan.
4. Before proposing a change to anything in docs/decisions.md or docs/design.md,
   read it. To overturn an entry, ask the owner explicitly — never silently re-decide.
5. Root instructions are defaults. The closest scoped `AGENTS.md` may add or override
   rules only for its subtree; do not duplicate root facts in an overlay.

## Hard rules (max 7)

1. <PROJECT_RULE — a rule earns a slot here by being violated twice; keep ≤7>
