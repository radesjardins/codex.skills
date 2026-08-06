<!-- The ~10-line doc-model block /rad-repo:repo-init (and /adopt) stamps
     into a repo's AGENTS.md. Anything that writes docs in the repo reads this block
     and conforms — the contract travels with the repo. Keep it verbatim. -->

<!-- rad-repo-doc-model: 1 -->

## Doc model (authoritative for doc structure in this repo)

- Docs live on a fixed shelf under `docs/`: decisions.md, ideas.md, lessons.md,
  design.md, architecture.md, api.md, handoff.md, prd.md, plan.md — each created
  only when first needed — plus `docs/initiatives/` for approved finite migrations
  and `docs/archive/` for history. Nothing else gets written.
- Units of work: Goal → Release (Now/Next/Later) → Milestone (M1…) → Task (T1…).
  Never phase, slice, sprint, epic, stage, or "step" as a tracked unit.
- One writer per file: the planner writes prd.md/plan.md; wrapup/ship refresh
  handoff.md; anyone appends to decisions/ideas/lessons (no one edits them);
  design.md is the sole source of the design system.
- Root `AGENTS.md` contains repo-wide defaults; scoped overlays contain only
  materially different subtree commands, constraints, ownership, or generated-code rules.
- Full contract: rad-repo `references/shelf-spec.md`.
