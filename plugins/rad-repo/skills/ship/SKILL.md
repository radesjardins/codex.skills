---
name: ship
description: >
  This skill should be used when the user says "ship", "ship it", "close out and
  push", "wrap and ship", "wrap it up and push", "send it", "close-out", "commit
  and push everything", or "end the session and push". The one-command close-out
  chain: align-lite → quick wrapup → reviewed staging → contract validation →
  conventional commit → push → deploy-verify (only when AGENTS.md declares a deploy:
  target) → stray branch/worktree sweep → one-line report. Invoking `ship` is the
  owner's authorization to commit and push — no re-asking. Target: under three
  minutes including deploy verification.
allowed-tools: Read Glob Grep Bash Write Edit AskUserQuestion
---

# Ship — the close-out chain

The hand-typed ritual (align → wrapup → commit → push → "did it deploy?") as one
workflow. **Invoking `ship` is the owner's commit-and-push authorization** — do not
ask again before committing or pushing; that consent is the point of the skill. Ask
only when something is genuinely wrong (a conflict, a failed push, a red scan the
owner should see before publishing).

Run the chain in order; each link is cheap. Resolve plugin resources relative to this
skill file.

## 1. Align-lite — mechanical scans only

```bash
PLUGIN_ROOT="../../"
python3 "$PLUGIN_ROOT/scripts/repo-scan.py" . --json --no-record
python3 "$PLUGIN_ROOT/scripts/doc-freshness.py" . --json
```

(`python` on Windows; skip silently if Python is unavailable.) No judgment passes, no
proposals, no fixes — this is a smoke check, not `repo-align`. Red findings go into
the final report as one line each; nothing here blocks the ship unless the owner
says so.

## 2. Quick wrapup

Run the quick path of `wrapup` inline: overwrite `docs/handoff.md`
(≤60 lines) from git evidence, carry the `## Deferred — do not re-raise` section
forward, ask the two questions (decisions settled? → append `docs/decisions.md`;
lessons? → append `docs/lessons.md`). This is the only interactive moment on a green
ship.

## 3. Reviewed staging

```bash
git status --short
git diff --stat
git add -- <reviewed-paths>
git diff --cached --stat
git diff --cached --check
```

Never use `git add -A`. Stage only paths verified as part of the requested change.
Inspect the staged summary and stop if unrelated files, conflict markers, or
whitespace errors appear. If the tree is clean and the handoff did not change,
skip the remaining commit-and-push steps and say so.

## 4. Pre-ship contract gate

Run the staged safety and validation gate:

```bash
python3 "$PLUGIN_ROOT/scripts/pre_ship.py" . --run-validation --json
```

(`python` on Windows.) This blocks protected paths, likely secrets, generated
output, oversized files, failed commands, and a repository with no declared
validation. Validation comes from `.rad-repo.json` plus the root and
applicable scoped `AGENTS.md` files. A repository with no mechanical check must
declare `validation.allow_empty: true` explicitly.

If `AGENTS.md` or `.rad-repo.json` is staged, show its staged diff and ask
the owner to approve the contract change. Only then rerun with
`--allow-contract-change`. Any unstaged root or scoped contract edit remains blocking;
stage and review it or restore it. Never bypass any other finding.

## 5. Commit — conventional message

```bash
git commit -m "<type>(<scope>): <summary from the staged diff>"
```

Use conventional-commit style (`feat:`, `fix:`, `docs:`, `chore:`…), grounded in
the staged diff. Use the user's message hint if supplied.

## 6. Push

```bash
git push origin main
```

If the current branch isn't `main`, push the current branch and say so plainly —
don't silently merge or switch branches. If the push is rejected (diverged), stop
and surface it; never force-push.

## 7. Deploy-verify — only when declared

Read `AGENTS.md` for a `deploy:` line. **No `deploy:` target (or `deploy: none`) →
skip this step silently.**

When a target is declared (e.g. `deploy: coolify`):

- If the rad-coolify-orchestrator MCP tools are available, poll the deployment
  (`coolify_list_running_deployments` / `coolify_get_deployment` for the app) until
  it reports live or failed — report the outcome *before* asking the owner to test
  anything.
- If the MCP tools are not available (not installed, not authenticated, or a
  non-Coolify target with no tooling), degrade gracefully: say plainly "pushed —
  deploy target `<target>` declared but I can't verify it from here; check it
  manually" and move on. Never claim a deploy succeeded that you did not observe.

## 8. Stray branch / worktree sweep

```bash
git branch --merged main
git worktree list
```

Report merged local branches and leftover worktrees; delete only on the owner's
one-word OK (deletion is the one irreversible act in the chain, so it stays gated).

## 9. One-line report

```text
Shipped: <commit hash> pushed to origin/main · deploy <live/failed/skipped/unverified> · handoff fresh · <N> scan note(s) · <N> stray branch(es)
```

Anything yellow/red from step 1 gets one extra line each, pointing at `repo-align`.

## What this skill does NOT do

- No deep alignment pass, no doc filing, no reconcile — mechanical scans only
  (that's `repo-align` / `wrapup --full`).
- Never force-pushes, never merges branches, never deletes branches/worktrees
  without the owner's explicit OK.
- Never stages unreviewed paths or bypasses a pre-ship blocking finding.
- Never claims a deploy result it didn't observe.
- On the **first** `ship` in a repo whose AGENTS.md has no fit-out record: run the
  fit-out step first (`../../references/fit-out.md`) — detect traits, propose
  the equipment menu once, install what's approved, then continue the chain.

## References

- `../../references/shelf-spec.md` — budgets, Deferred ledger, entry formats
- `../../references/fit-out.md` — trait detection + equipment menu (first ship)
