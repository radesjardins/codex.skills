---
name: wrapup
description: >
  This skill should be used when the user says "wrapup", "wrap up", "end of
  session", "save state", "handoff", "leave a clean stopping point", "I'm done for
  now", or "before I close". Quick by default (target under a minute): overwrites
  docs/handoff.md (≤60 lines) from git evidence — not chat memory — carrying the
  Deferred ledger forward, then asks exactly two questions: any decisions settled
  this session (append to docs/decisions.md)? anything blow up worth remembering
  (append to docs/lessons.md)? The deeper reconcile pass — checking whether the
  session left plan/prd/AGENTS.md stale and drafting per-edit-confirmed fixes —
  runs only with --full (weekly use). No status/roadmap files, no auto-commit or
  push, never runs tests.
allowed-tools: Read Glob Grep Bash Write Edit AskUserQuestion
---

# Wrapup — leave a clean handoff, fast

End the session at a spot a fresh chat (or a post-compaction continuation) can resume
from cold. **Quick is the default** — the observed alternative to a fast wrapup is no
wrapup. `--full` adds the reconcile pass; the whole-repo audit stays in
`repo-align`.

**Two hard rules:**

- **The one required output is an overwritten `docs/handoff.md`.** Always write it —
  even if nothing changed this session (then it just snapshots the current resting
  state). Never finish `wrapup` without having written it.
- **Do not run tests, builds, linters, or any command beyond the read-only git
  inspection in step 1.** `wrapup` only *records* validation that already ran this
  session; it never runs validation itself.

## Quick path (default)

### 1. Gather evidence (not memory)

In one batch:

```bash
git status --short
git diff --stat
git log --oneline -10
```

Determine what changed from the working tree, staged files, and recent commits — not
from a chat summary. For the Validation line, report only what *already* ran this
session (do **not** re-run), including applicable contract commands resolved from
root/scoped `AGENTS.md` and `.rad-repo.json`: take it from the conversation, or — after compaction —
from what the compaction summary preserved. If neither source has it, write
"Not recorded this session" — never invent a result.

### 2. Overwrite the handoff snapshot

Read the current `docs/handoff.md` first — **its `## Deferred — do not re-raise`
section carries forward verbatim** (prune an item only if its wake condition visibly
fired; say so when you do). Then overwrite the file from
`../../templates/handoff.md` relative to this skill file. Create `docs/` first if it
doesn't exist. Keep the whole
file **≤60 lines** (its L1 budget). Stamp `**Updated:**` with today's date (failing
that, `git log -1 --format=%cs` — don't ask). The shape:

- **Last completed** — 1–3 bullets grounded in the diff / commits / test output.
- **Current focus** — the current milestone or active task from `docs/plan.md`, if present.
- **Next action** — the single next step to pick up.
- **Validation** — commands run this session and their result, or "Not run this session."
- **Watchouts** — only material gotchas; omit if none.
- **Deferred — do not re-raise** — carried forward, plus anything the owner parked
  this session, each as `- <item> (wake: <condition or never>)`.

### 3. The two questions

Ask both in one AskUserQuestion round (or `ask_question` on Antigravity), then stop:

1. **"Any decisions get settled this session?"** — for each one the user names,
   **append** one dated line to `docs/decisions.md` (create it with a `# Decisions`
   header if absent): `- YYYY-MM-DD · <decision> (<one-line why>)`. Settled
   *visual/design* decisions go to `docs/design.md` instead (it's the sole
   design-system source) — propose that edit and apply on the user's OK.
2. **"Anything blow up that's worth remembering?"** — for each, **append** one dated
   line to `docs/lessons.md` (create with a `# Lessons` header if absent).

Appends only — never edit existing entries (see
`../../references/shelf-spec.md`). A "no" to both means write nothing.

That's the quick path. Report the handoff is written and stop — no scans, no
reconcile, no commit. (If the latest `startup` trust report was red — handoff
>10 commits behind — mention once that `--full` or `repo-align` is worth it
soon.)

## `--full` — the reconcile pass (weekly)

Everything above, plus:

### 4. Reconcile the core docs with this session

Check whether *this session's changes* left `AGENTS.md`, `docs/prd.md`, or
`docs/plan.md` stale — scoped to what actually changed (the diff/commits above),
**not** a whole-repo audit (that's `repo-align`). Split by ownership:

- **Docs this plugin owns — `AGENTS.md` operational sections.** Offer the specific,
  scoped update (one line each: what's stale → what it should say) and apply on the
  user's OK. Respect the 40-line budget — if a needed addition would blow it, that's
  a rules-audit signal for `repo-align`, not a reason to overflow.
- **`docs/plan.md` — the planner's file.** Status-level touches only (a task shipped,
  the current milestone advanced) on the user's OK, refreshing its `**Updated:**`
  stamp. **If the divergence is structural** — milestones obsolete, scope shifted,
  the "Now" release essentially shipped — don't restructure: recommend
  the planning workflow.
- **Docs the user owns — `docs/prd.md`, `docs/design.md`.** Draft the exact edit
  (old → new) and ask per doc via AskUserQuestion: **apply / skip / let me reword**.
  Apply only on an explicit "apply" for that specific edit — never bundle user-owned
  edits into a blanket OK. A skipped edit is restated in one line at the end so it
  isn't silently lost.

### 5. Hygiene pulse — one line, no audit

Run the cheap mechanical scan (`python3`, or `python` on Windows):

```bash
PLUGIN_ROOT="../../"
python3 "$PLUGIN_ROOT/scripts/repo-scan.py" . --json --no-record
```

If green, say nothing. If loose ends exist, add **one line** naming them and pointing
at `repo-align` — do not file, move, or fix anything here. (Skip silently if Python
is unavailable.)

## Commit

Do **not** auto-commit or push. Tell the user the handoff is written and they can
commit via their normal flow — or run `ship`, which is the skill
whose invocation *is* commit-and-push authorization. If they explicitly ask here,
commit on the current branch with a short message — otherwise leave it.

## What this skill does NOT do

- No whole-repo audit, contradiction scan, or doc filing — that's `repo-align`. Even
  `--full`'s reconcile is scoped to this session's changes.
- Does not run tests, builds, linters, or validators — it only records validation
  that already ran.
- Does not edit `docs/prd.md` or `docs/design.md` without an explicit per-edit
  "apply"; does not edit existing `decisions.md`/`ideas.md`/`lessons.md` entries —
  those files are append-only.
- Does not create `docs/status.md`, `docs/roadmap.md`, `docs/implementation-plan.md`,
  loose root-level handoff/status/audit docs, or redundant scoped agent files.
- No appending to the handoff (overwrite only); no auto-commit or push.

## References

- `../../templates/handoff.md` — the snapshot shape, incl. the Deferred section
- `../../references/shelf-spec.md` — the shelf, entry formats, budgets, one-writer table
