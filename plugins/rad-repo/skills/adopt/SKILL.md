---
name: adopt
description: >
  This skill should be used when the user says "adopt this repo", "bring this repo
  onto the doc model", "this repo predates the system", "onboard this existing
  project", "migrate this repo's docs", or when startup found an established repo
  without the doc model. Brownfield archaeology, read-only toward code: reads git
  history + docs + code, drafts AGENTS.md/handoff/decisions from evidence
  (verifying build/test commands by actually running them), triages every existing
  doc onto the shelf (keep / merge / satellite / archive — proposing each move, never
  silently deleting), asks only what evidence can't answer, stamps dormant repos, runs
  fit-out, and hands plan reconstruction to the planner rescue skill. Never changes
  code.
allowed-tools: Read Glob Grep Bash Write Edit AskUserQuestion
---

# Adopt — bring an existing repo onto the doc model

`repo-init`'s sibling for repos that already have a life: code, history, and a pile
of docs written before the shelf existed. Archaeology first, questions second,
writes last — and **never a code change**. The target model is
`../../references/shelf-spec.md`.

**Boundaries:** evidence before questions (never ask what git can answer); propose
every doc move (never silently delete — `git mv` preserves history); the only
commands you run are read-only git/inspection plus the build/test commands in step 2
(to verify them, not to fix anything).

**Non-destructive by contract** — state this up front if the migration looks scary
(to the owner or to you): every move is `git mv`, every write is confirm-gated,
nothing is ever deleted. And a repo that already has a *working* doc model (homegrown
or an older version of this one) gets **mapped, not flattened** — apply "Conformance
without loss" from the shelf spec: rich existing content becomes a linked satellite,
shelf formats govern only new entries. Don't balk at the conversion; shrink it.

## 1. Archaeology — read everything, change nothing

In parallel batches:

```bash
git log --oneline -30
git log --format="%cs" -1          # last activity — the dormancy signal
git shortlog -sn --since="6 months ago"
git remote get-url origin
git branch -a && git worktree list
```

Glob the tree; read `README.md`, every root or scoped `AGENTS.md`, everything under
`docs/`, the manifest (`package.json` / `pyproject.toml` / …), CI config, and enough
code entry points to know what the thing *is*. Build an instruction map from root
defaults to closest-scope overlays and preserve overlays that carry materially
different subtree commands, constraints, ownership, or generated-code rules. Note
the candidate build/test/run commands the evidence suggests.

## 2. Verify the commands by running them

The one write-nothing exception to "read-only": actually run the candidate build and
test commands (not deploys, not migrations — nothing with side effects beyond a
build dir). Record what really works; a drafted AGENTS.md must never claim a command
you didn't see pass. If a command fails, record it as "documented but currently
failing" — that's evidence, not something to fix here.

## 3. Draft L0–L2 from evidence

Draft — show the user before writing:

- **`AGENTS.md` (L0, ≤40 lines)** from `templates/AGENTS.md`: identity line from
  what the code actually does; verified commands from step 2; the doc-model block
  stamped verbatim from `templates/doc-model-block.md`; `deploy:` only if a target
  is evidenced. Existing AGENTS.md content is triaged, not clobbered: rules worth
  keeping go to the hard-rule slots (≤7 — if there are more, run the rules-audit
  classification from `repo-align` and propose promote/keep/demote), the rest to the
  step-4 triage. If another agent manual already exists, treat it as an existing doc
  to route, fold, or archive; do not create a new shim.
- **`docs/handoff.md` (L1)** from the template: last completed from recent commits,
  next action from wherever the evidence points (or "unknown — owner to confirm"),
  an empty Deferred section.
- **`docs/decisions.md` (L2)** — only if the archaeology surfaced clearly settled
  decisions (in old ADRs, READMEs, commit messages). Append one dated line each,
  marked with their source. Don't invent decisions.

## 4. Triage every existing doc onto the shelf

For **every** doc in the repo (root `.md`s beyond the standard furniture, everything
under `docs/`), read it and propose exactly one disposition — the same closed set as
`repo-align`: **route** (append content to decisions/ideas/lessons/design), **fold**
(merge into a shelf doc), **keep** (it already is a shelf doc — rename/move into
place with `git mv` if needed), **satellite** (no shelf slot but still useful — stays
in `docs/`, linked from the nearest core doc, per the shelf spec's satellite rule),
**archive** (`git mv` to `docs/archive/` + banner).

After any moves, grep the repo (code, CI, scripts, remaining docs) for the old paths
and fix every reference in the same pass — a triage that ships dead links isn't done.
Present the whole triage as a table, get the owner's call per row, then execute the
approved rows. Never silently delete anything.

An approved finite migration with a plan link, baseline, owner, acceptance criteria,
rollback strategy, and retirement trigger may become `docs/initiatives/<slug>.md`
from the initiative template. It is a temporary execution packet, not a second plan;
anything without that lifecycle metadata remains a routing candidate.

## 5. Ask only what evidence can't answer

5–10 questions, one AskUserQuestion round where possible. Always include:

- **Active or dormant?** Dormant → stamp `Status: dormant — maintenance only` in
  AGENTS.md's identity line and skip fit-out extras that only matter for active work.
- The genuinely unanswerable: current goal still true? which of two conflicting old
  docs was right? deploy target? who else works here (agent scope for shims)?

## 6. Fit-out

Run the fit-out step (`../../references/fit-out.md`): detect traits from the
code you just read, propose the equipment menu once, install what's approved, record
the fit-out line in AGENTS.md.

## 7. Hand off

If the repo needs its plan reconstructed — no trustworthy `docs/plan.md`, unclear
state, half-built direction — **hand off to the planner rescue skill**: adopt built
the container and shelf (structure archaeology); rescue rebuilds intent and the
plan (content archaeology). If a usable plan exists, the planner replan skill
re-baselines it instead.

## Output format

```text
Adopt:
Repo:               <name — what it is, from evidence>
Activity:           <active / dormant (last commit <date>)>
Commands verified:  <build/test results — ran and passed / ran and failed / not found>
L0-L2 written:      <AGENTS.md, handoff.md, decisions.md (N entries) — after approval>
Doc triage:         <N docs: N routed, N folded, N kept, N archived, N skipped by owner>
Fit-out:            <installed items | declined | skipped (dormant)>
Next step:          <planner rescue | planner replan | none needed>
```

## What this skill does NOT do

- Never changes, formats, or "fixes" code — archaeology only.
- Never deletes a doc — every removal is a `git mv` to `docs/archive/`, confirmed.
- Never invents decisions, goals, or commands that evidence didn't show.
- Never writes `docs/prd.md` or `docs/plan.md` — that's the planner's lane
  (rescue/plan birth them from the owner's own answers).
- No commits, no pushes.

## References

- `../../references/shelf-spec.md` — the target model
- `../../references/fit-out.md` — trait table + menu procedure
- `../../templates/` — AGENTS.md skeleton, doc-model block, handoff stub, shims
