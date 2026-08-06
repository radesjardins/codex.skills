# Safe Recovery and Failure States

A plan must explain how to detect failure and return the changed system to a known state. Recovery instructions must protect unrelated user work.

## Task contract

Each task uses the six fields in `plan-template.md`. Failure handling lives in three of them:

- **Done when:** the observable result.
- **Validate:** the focused pass or fail check.
- **Rollback:** the safe recovery strategy.

Use `## Stop conditions` for failures that need owner input instead of automatic recovery. Use milestone checkpoints for release-level gates.

## Safe rollback rules

1. Name the state that must be restored: code, data, configuration, deployment, or external service state.
2. Prefer a new revert commit when the task has its own commit.
3. For data changes, name the tested down migration, backup restore, or approved forward fix.
4. For external systems, name the compensating action and the evidence that confirms it worked.
5. Use `manual recovery required` when no safe automatic rollback exists.
6. Stop if unrelated local changes, an unknown base commit, a missing backup, or a locked resource makes recovery unsafe.

Never put these commands in a generated rollback instruction:

- `git reset --hard`
- `git checkout --`
- `git restore`
- recursive delete commands

Those commands can erase work outside the task. A plan can describe the intended state without prescribing a destructive command.

## Example

```markdown
- **T3 - Add the account migration**
  - **Objective:** Add the nullable account status column and backfill current rows.
  - **Files:** [existing] `db/schema.sql`; [new] `db/migrations/014-account-status.sql`; [new] `db/migrations/014-account-status.down.sql`
  - **Depends on:** T2
  - **Done when:** Existing accounts have a valid status and new accounts receive the default status.
  - **Validate:** Run the migration against a disposable database, run the account migration tests, then run the down migration and confirm the original schema and row count.
  - **Rollback:** Use the tested down migration before production data is accepted. After production data is accepted, stop for owner approval and use the documented backup or forward-fix procedure.
```

## Failures that need stop conditions

Add a stop condition when the task can affect:

- authentication or authorization;
- payments;
- personal or regulated data;
- destructive schema changes;
- an external service with no safe compensating action;
- a production deployment that cannot be restored from a known artifact.

## Review questions

- Does Validate test the stated outcome?
- Does Rollback restore the real state, including data and external effects?
- Can the recovery touch unrelated local work?
- Is the required backup or prior artifact known to exist?
- Does the plan stop when recovery needs an owner decision?
