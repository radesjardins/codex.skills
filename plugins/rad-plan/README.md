# rad-plan

Plan a project before you write code — and re-plan it as reality unfolds. rad-plan is built for solo developers who aren't formally trained engineers: it interrogates you until it actually understands what you're building, then produces a plan that a moderately experienced vibe coder can read **and** a coding agent can execute. It is **strictly a planner** — it never writes implementation code.

## What makes it more than a generic planner

Codex can already write a plan. rad-plan adds an **interview-driven, risk-first, adversarially-reviewed, and mechanically-validated** workflow — passes a single-shot plan does not get:

- **The grilling** — a structured discovery interview: eight coverage areas (end goal, users, MVP, success criteria, constraints, assets, exclusions, danger zones), each driven to *settled* or *explicitly unknown*; the project mirrored back for correction; assumptions proposed for confirm/deny instead of asking you to invent them. Capped at 3 rounds so it stays fast. Pre-fills from the repo **and from dated spec docs** (`docs/*-spec.md`, `docs/*-design.md`, newest first) — a brainstorm or design spec gets confirmed ("the spec says X — still true?"), never re-asked.
- **One vocabulary** — the naming ladder: **Goal** (the end state, in the PRD) → **Release** (Now / Next / Later horizons) → **Milestone** (M1…) → **Task** (T1…). No phases, sprints, epics, slices, or stages as units of work. The PRD speaks Goal/Release; plan.md speaks Milestone/Task. When the repo's AGENTS.md carries a doc-model block, that block is authoritative; the planner's defaults match it.
- **The release ladder in practice** — every plan anchors to your end goal via the Now / Next / Later release map. Detail decays with distance by design: only "Now" gets task specs; speccing distant versions is fake precision.
- **The seed packet** — `rad-plan:plan` ends by routing planning's structured leftovers onto the repo's doc shelf: stack choice + why appended to `docs/decisions.md`, cut features and stray interview ideas appended to `docs/ideas.md`, an AGENTS.md stack block *proposed* (you apply it), `docs/architecture.md` / `docs/api.md` seeded only when their triggers fire. It never creates docs for "Later" work, status/roadmap files, or empty scaffolds.
- **Written for two readers** — a plain-language layer (how-to-read note, release map, *After this ships* lines per milestone) for you; six-field task blocks for the coding agent.
- **Codegen-aware stack evaluation** — `stack-advisor` picks tech for how accurately an LLM can implement it (the AI-native Golden Path matrix), not just general fit.
- **Goal-backward decomposition + risk-first sequencing** — solve the hardest unknown first; small shippable milestones (size discipline).
- **Mechanical validation** — `plan-lint.py` is a real pass/fail check on the plan (required sections, per-task fields, dependency resolution + cycles, vague language), not the model grading its own homework.
- **Adversarial review** — the `risk-assessor` agent checks the plan against 14 documented anti-patterns and architecture concerns, returns APPROVE / REVISE / RETHINK, iterates, and escalates to brainstorming when the architecture itself is broken.
- **Failure-state rigor** — every task carries a rollback, not just a happy path.

## Output

The plan lives in a single file, `docs/plan.md` — objective + end goal, release map, scope, assumptions, stack, milestones, tasks, checkpoints, risks, validation, stop conditions. No strategic-doc tree. At re-plan, shipped work moves to a `## Shipped` section — history is preserved, never deleted.

Alongside it, the **seed packet** (end of `rad-plan:plan`) appends the planning leftovers to their shelf homes — `docs/decisions.md`, `docs/ideas.md` — and seeds `docs/architecture.md` / `docs/api.md` only when their triggers fire (more than one moving part; an API in the first milestone).

**The PRD exception:** when `docs/prd.md` is missing or a skeleton, the planner offers to draft it — each section written from *your own interview answers* and applied only on your per-section confirmation. After that birth, the PRD is yours (and rad-repo keeps it fresh); the planner never edits an existing PRD. Changes to docs the planner doesn't own (an existing PRD, `docs/design.md`) are never written directly — they go into a paste-ready `docs/[date]-update-prompt.md` you run in Codex, with a pointer in `plan.md`.

## Skills — two doors in, one maintained plan

| Skill | Trigger | What it does |
|---|---|---|
| `rad-plan:plan` | "plan my project", "create an implementation plan", "break this into tasks" | **Door 1 — greenfield or clear next effort.** The six-step conversation: interview → stack → build → validate & risk → review → export + seed packet. Offers a quick path (single feature: skip the stack subagent, single risk pass) or full path — your choice, asked once. On a bare repo (no AGENTS.md, no `docs/`) it recommends `rad-repo:repo-init` first — and degrades gracefully when that isn't installed. |
| `rad-plan:rescue` | "this repo is a mess", "help me out of this", "I don't know where this stands" | **Door 2 — project in an unclear state.** Read-only archaeology (code + git evidence) → evidence-led interview (keep/cut/unknown per piece) → PRD from your answers → a fresh release-map plan starting from where the project actually is. Runs after `rad-repo:adopt` when structure is the mess: adopt is *structure* archaeology, rescue is *intent* archaeology. Assesses and plans; never fixes, runs, or deletes code. |
| `rad-plan:replan` | "update the plan", "we shipped the MVP — what's next", "the plan is out of date" | **The single deliberate direction-change moment.** Marks shipped work from git + handoff (moved to `## Shipped`, never deleted), gives every parked idea in `docs/ideas.md` a fair hearing (pull in / keep parked / reject with a recorded why), re-baselines the rest, pulls the next horizon into detail when "Now" ships. Single risk pass; your approval gates everything. |
| `rad-plan:review-plan` | "review my plan", "audit this plan", "is this plan complete" | Two-layer quality audit of an existing plan: mechanical lint + adversarial risk review. |

## Codex subagents

| Agent | Role |
|---|---|
| **stack-advisor** | Tech-stack evaluation for codegen accuracy; live version and compatibility checks against current primary documentation. |
| **risk-assessor** | Adversarial plan review — anti-patterns, architecture, rollback quality, checkpoint placement, TDD. Runs `plan-lint.py` first to skip mechanical checks. |

## The planning conversation

```
1  Discovery        — evidence pre-fill (PRD/handoff/repo + dated spec docs, confirmed
                      not re-asked), then the structured interview: eight coverage
                      areas, mirror-back, ≤3 rounds, proposed assumptions. Closes with
                      the speed fork (quick vs full — you choose) and the PRD gap
                      check (draft it from your answers, per-section confirmed)
2  Stack Evaluation — stack-advisor + Golden Path matrix (full path, when a stack decision is in play)
3  Build the Plan   — release map (Now/Next/Later), goal-backward decomposition within "Now",
                      risk-first sequencing + size discipline, every task specced to
                      execution-readiness (six fields), plain-language layer for the human
4  Validate & Risk  — plan-lint.py (mechanical) then risk-assessor (adversarial; iterative
                      on the full path, single-pass on the quick path)
5  Review           — plain summary + release map + the embedded decisions first, detail after;
                      human approves; never self-approves. Challenge once, then commit.
6  Export           — write plan.md; emit the seed packet (decisions/ideas appends,
                      trigger-gated architecture/api seeds, proposed AGENTS.md stack
                      block); surface other durable changes into the update-prompt
```

If the idea is still fuzzy, the planner stops and routes you to `rad-brainstormer` when installed — planning assumes the *what* is decided and plans the *how* and *order*. If the *project* exists but its state is the mystery, that's `rad-plan:rescue`.

## Boundary with rad-repo

[`rad-repo`](../rad-repo/) owns the doc model; the planner conforms to it. When a repo's `AGENTS.md` carries a doc-model block (shelf list, vocabulary ladder, one-writer table), the planner reads it at runtime and writes in its headings and vocabulary; without one, the planner's built-in defaults match the same model. Handshakes: bare repo → `repo-init` before `rad-plan:plan`; drifted existing repo → `adopt` before `rad-plan:rescue`. Between plans, the repo-manager maintains what the planner produces: its `wrapup` makes one-line status touches to `plan.md` ("M2 shipped") and keeps the PRD fresh after the planner births it. When the divergence is structural — milestones obsolete, scope shifted, the next version due — that's `rad-plan:replan`. The repo-manager maintains; the planner restructures.

## Mechanical validators (scripts/)

Pure-stdlib Python 3.8+. Human-readable text by default, `--json` on request. Exit 0 clean, 1 issues found, 2 script error.

| Script | What it checks |
|---|---|
| `plan-lint.py` | `plan.md` — required sections, per-task field presence (Objective, Files, Depends on, Done when, Validate, Rollback), dependency resolution + cycles, vague-language detection. |
| `validate-json.py` | JSON Schema validator for the `stack-advisor` / `risk-assessor` output contracts; re-prompts the agent once on schema failure. |

## Pipeline with rad-brainstormer

`rad-plan` and [`rad-brainstormer`](../rad-brainstormer/) own different parts of the pipeline. A spec describes *what* and *why*; sequencing belongs to `plan.md` alone — the planner reads dated specs as settled input and confirms rather than re-asks.

| Part | Plugin | Output |
|---|---|---|
| **Ideation** (divergent) | `rad-brainstormer` | A decided idea + rough direction |
| **Design** (post-ideation) | `rad-brainstormer:design-sprint` | A reviewable design spec |
| **Planning** (pre-code) | `rad-plan:plan` | An approved `plan.md` |
| **Code** | your tools of choice | Working software |

Clear idea → start with `rad-plan:plan`. Fuzzy idea → start with `rad-brainstormer:brainstorm-session` when installed.

## Relationship to Codex Plan mode

Codex Plan mode can structure the interactive decision process; rad-plan adds the interview, release-map method, subagent contracts, durable plan artifact, and mechanical validation. The full `rad-plan:plan` workflow writes only its approved planning artifacts under `docs/`.

## Reference files

Loaded on demand by the skills and agents:

| Reference | Content |
|---|---|
| `discovery-interview.md` | The grilling protocol — eight coverage areas, mirror step, round caps, the speed fork and PRD gap check |
| `plan-template.md` | The `plan.md` structure (incl. release map + Shipped rules) + update-prompt template + enforced rules |
| `golden-path-matrix.md` | AI-native proficiency tiers + project-type stack recommendations |
| `anti-patterns.md` | Documented planning anti-patterns (some are opinions with thresholds — marked) |
| `failure-state-template.md` | Triple-component validation (Action → Validation → Rollback) |
| `tdd-constraints.md` | Per-task test-strategy requirements |
| `context-management.md` | Document & Clear triggers and milestone-boundary discipline |
| `subagent-prompts/stack-eval.md` + `.schema.json` | `stack-advisor` dispatch template + JSON Schema |
| `subagent-prompts/risk-assessment.md` + `.schema.json` | `risk-assessor` dispatch template + JSON Schema |

A real, lint-clean example plan lives in `examples/plan.md` (with a companion `examples/2026-06-06-update-prompt.md`).

## Requirements

- **Python 3.8+** for the validator scripts (`python3`, or `python` on Windows). Without it, the skills fall back to manual review against the documented checklists — honestly, "validators" reduce to "templates the model is asked to follow."
- Optional: `pip install jsonschema` for fuller draft-07 coverage in `validate-json.py`. A pure-stdlib subset is used otherwise.

## License

MIT
