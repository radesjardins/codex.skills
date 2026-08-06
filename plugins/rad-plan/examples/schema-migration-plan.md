# Plan: Add Account Status Safely

**Status:** APPROVED
**Updated:** 2026-08-06
<!-- rad-plan-contract: 7.1 -->

## Objective

Add account status without locking the accounts table or losing current values.

**End goal:** Account access rules use an explicit, audited lifecycle state.

## Release map

- **Now - Status foundation (this plan):** Add, backfill, read, and safely reverse the new field.
- **Next - Access rules:**
  - Apply status to sign-in and administration flows
- **Later - the end goal:**
  - Audited account lifecycle transitions

## Scope

**In scope:**
- Nullable column, bounded backfill, read path, and tested down migration

**Out of scope / non-goals:**
- Sign-in blocking
- Administration user interface

## Key assumptions

- [2026-08-06] The approved deployment system can run expand and contract migrations separately.
- [2026-08-06] A current production backup exists before release approval.

## Stack

Keep the current PostgreSQL and application migration tools.

## Outcome coverage

| Outcome | Covered by | Final proof |
|---|---|---|
| O1 - Current accounts receive the approved active status without a long table lock | T1 | `npm test -- account-status-migration.test.ts` |
| O2 - The application reads accounts before, during, and after the migration | T2 | `npm test -- account-status-compat.test.ts` |
| O3 - The pre-migration schema and row count can be restored in a disposable database | T1 | `npm run test:migration-down -- 014-account-status` |

## Milestones

| # | Milestone | Ships | Key artifacts |
|---|---|---|---|
| M1 | Reversible migration | Expand, backfill, and down proof | Migration pair and migration tests |
| M2 | Compatible read path | Application support for both schema states | Account mapper and compatibility test |

## Tasks

### M1 - Reversible migration

*After this ships: The database change has direct forward and recovery proof in a disposable environment.*

- **T1 - Add and prove the migration pair**
  - **Objective:** Add a nullable status column, backfill in bounded batches, and prove the down migration restores the prior schema and row count.
  - **Files:** [new] `db/migrations/014-account-status.sql`; [new] `db/migrations/014-account-status.down.sql`; [new] `test/account-status-migration.test.ts`
  - **Depends on:** none
  - **Done when:** A production-size fixture migrates without the approved lock limit, every row receives `active`, and the down run restores the original schema and count.
  - **Validate:** `npm test -- test/account-status-migration.test.ts && npm run test:migration-down -- 014-account-status`
  - **Rollback:** Before application writes use status, run the tested down migration. After status writes begin, stop for owner approval and use the documented backup or forward-fix procedure.

### M2 - Compatible read path

*After this ships: The application can read accounts during the staged database change.*

- **T2 - Read both schema states**
  - **Objective:** Make the account mapper return the approved default before the column appears and the stored value after it appears.
  - **Files:** [existing] `src/accounts/mapper.ts`; [new] `test/account-status-compat.test.ts`
  - **Depends on:** T1
  - **Done when:** The compatibility test passes against the schema before expansion, after expansion, and after backfill.
  - **Validate:** `npm test -- test/account-status-compat.test.ts`
  - **Rollback:** Revert the isolated application task commit while the database column remains nullable and unused by write paths.

## Checkpoints

### After M1

- **Gate:** Forward and down migration checks pass on the production-size fixture.
- **Validate:** `npm test -- test/account-status-migration.test.ts && npm run test:migration-down -- 014-account-status`
- **Rollback:** Use the tested down migration before any application status writes.

### After M2

- **Gate:** T2 passes against all three schema states.
- **Validate:** `npm test -- test/account-status-compat.test.ts`
- **Rollback:** Revert the M2 task commit and leave the nullable database field unused.

## Risks & mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Backfill locks the table | Medium | High | Use bounded batches and test the lock limit on a production-size fixture |
| Recovery loses status writes | Low | High | Stop automatic rollback after status writes begin |

## Validation

- `npm test -- test/account-status-migration.test.ts test/account-status-compat.test.ts` - forward and compatibility checks pass.
- `npm run test:migration-down -- 014-account-status` - prior schema and row count return in a disposable database.

## Stop conditions

- Stop if the current production backup cannot be confirmed.
- Stop if the migration exceeds the approved lock duration.
- Stop before any application path writes status in this release.
