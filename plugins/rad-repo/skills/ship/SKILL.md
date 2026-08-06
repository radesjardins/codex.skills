---
name: ship
description: >
  This skill should be used when the user says "ship", "ship it", "close out and
  push", "wrap and ship", "send it", "commit and push everything", or "end the
  session and push". It refreshes the handoff, stages reviewed paths, checks the
  local repository contract, runs approved validation, commits, pushes, and reports
  the exact state. Normal ship stops after push. "Ship and verify deploy" adds one
  bounded deployment check with no polling loop. Invoking ship authorizes commit and
  push. It does not authorize a force-push, merge, deploy action, or deletion.
allowed-tools: Read Glob Grep Bash Write Edit AskUserQuestion
---

# Ship

Close the work with reviewed Git state and repository checks. Invoking `ship` authorizes the commit and push. Do not ask again for those two actions.

## 1. Mechanical context check

Run the cheap repository and freshness scans. Report findings. They do not block ship unless they expose a real safety or contract problem.

```powershell
python ../../scripts/repo-scan.py . --json --no-record
python ../../scripts/doc-freshness.py . --json
```

## 2. Quick wrapup

Run the normal wrapup steps inline. Preserve useful handoff detail. Ask about a decision or lesson only when session evidence gives a real candidate.

Suggest a RAD Plan skill only when a real planning need exists and the exact skill
appears in the current available-skill list. When it is unavailable, report the need
without naming RAD Plan. Do not invoke it unless the owner asks or accepts the
suggestion.

## 3. Review and stage

```powershell
git status --short
git diff --stat
git add -- <reviewed-paths>
git diff --cached --stat
git diff --cached --check
```

Never use `git add -A`. Stage only requested work and wrapup documents. Stop for unrelated paths, conflict markers, or whitespace errors.

## 4. Explain and trust the contract

Run:

```powershell
python ../../scripts/repo-doctor.py . --json
```

If validation is missing, fix the declaration with owner approval. If command approval is required, show the exact commands and sources. After explicit approval, run:

```powershell
python ../../scripts/repo-doctor.py . --approve --json
```

The approval stays in local Git settings. A changed command requires new approval.

## 5. Run the pre-ship gate

```powershell
python ../../scripts/pre_ship.py . --run-validation --json
```

The gate checks staged blobs, high-confidence secret patterns, protected paths, generated output, file size, reviewed contract changes, local command trust, and validation results.

If `AGENTS.md` or `.rad-repo.json` is staged, show its staged diff and ask the owner to approve that contract change. Then rerun with `--allow-contract-change`. This flag does not bypass other findings.

## 6. Commit and push

Create a conventional commit message from the staged diff. Use the user's message hint when supplied.

Push the current branch. If it is not `main`, state the branch name. Stop on a rejected push. Never force-push, merge, or switch branches without a separate request.

## 7. Optional deploy check

Skip deployment checks during normal ship.

Run one check only when the original request includes `ship and verify deploy`, `check deploy after ship`, or an equally clear request. Read the declared `deploy:` target. Use one available read-only status or health check. Do not poll, wait for completion, restart a service, or start a deploy.

If the deployment is still running, report `running` and stop. If no read-only tool is available, report `unverified` and stop.

## 8. Report local leftovers

List merged local branches and worktrees. Do not delete them without a separate owner approval.

## Final report

```text
Shipped: <commit> pushed to <remote/branch>
Handoff: <fresh / size note>
Validation: <commands and result>
Deploy: <not requested / live / failed / running / unverified>
Working tree: <clean / remaining paths>
Local leftovers: <count>
```

Stop after this report. First-use fit-out belongs in `adopt` or an explicit fit-out request. It never runs inside ship.
