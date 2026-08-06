# Plan: URL Shortener Service

**Status:** APPROVED
**Updated:** 2026-08-06
<!-- rad-plan-contract: 7.1 -->

> **How to read this plan:** The Release map shows where this work fits. Milestones
> are shippable parts of Now. Each task gives a coding agent the exact outcome,
> files, dependencies, proof, and recovery need. Stop conditions require owner input.

## Objective

Ship a single-tenant URL shortener with stable codes and an atomic click counter. An internal tool needs shared short links this month.

**End goal:** The team's default internal link service provides short links and useful click analytics through an API.

## Release map

- **Now - MVP (this plan):** Shorten and redirect links with a click counter in one container.
- **Next - V1:**
  - Custom short codes
  - A small click-count endpoint
  - Token access for a second internal team
- **Later - the end goal:**
  - A small analytics view
  - Multi-tenant isolation when a second heavy user appears

## Scope

**In scope:**
- Return one stable short code for the same URL.
- Redirect a short code and increment its click count atomically.

**Out of scope / non-goals:**
- Custom codes
- Multi-tenant isolation
- Analytics user interface

## Key assumptions

- [2026-08-06] There are no production users before M3.
- [2026-08-06] The first release has one trusted internal user.
- [2026-08-06] Development data can be rebuilt from migrations.

## Stack

Keep the approved Node, Fastify, Drizzle, and PostgreSQL stack. It supports the required atomic database operations without a new service.

## Outcome coverage

| Outcome | Covered by | Final proof |
|---|---|---|
| O1 - Repeated URLs return one stable code under concurrent requests | T1, T2 | `npm test -- test/shorten.test.ts` |
| O2 - A short code redirects and records exactly one click per request | T3 | `npm test -- test/redirect.test.ts` |
| O3 - The service builds and answers its health check in one container | T4 | `npm run smoke:container` |

## Milestones

| # | Milestone | Ships | Key artifacts |
|---|---|---|---|
| M1 | Idempotency proof | Stable codes under concurrency | Schema and focused spike test |
| M2 | Core service | Shorten and redirect endpoints | Service and route handlers |
| M3 | Container | Runnable image with a health check | Container and smoke command |

## Tasks

### M1 - Idempotency proof

*After this ships: The hardest database behavior has direct proof before endpoint work starts.*

- **T1 - Prove the concurrent insert rule**
  - **Objective:** Prove one database row and one code result from 100 concurrent inserts of the same URL.
  - **Files:** [existing] `src/db/schema.ts`; [new] `test/spike/idempotency.test.ts`
  - **Depends on:** none
  - **Done when:** The focused test records one row and one returned code across 100 concurrent inserts.
  - **Validate:** `npm test -- test/spike/idempotency.test.ts`
  - **Rollback:** Revert the isolated task commit and confirm the original schema migration still applies to a disposable database.

### M2 - Core service

*After this ships: A local user can create and open short links.*

- **T2 - Add the shorten endpoint**
  - **Objective:** Make `POST /shorten` return the stable code proven in T1.
  - **Files:** [new] `src/shortener.ts`; [new] `src/routes/shorten.ts`; [new] `test/shorten.test.ts`
  - **Depends on:** T1
  - **Done when:** Repeated valid requests return the same code and invalid URLs return the approved error response.
  - **Validate:** `npm test -- test/shorten.test.ts`
  - **Rollback:** Revert the isolated task commit and confirm the pre-task route list still starts.
- **T3 - Add redirect and click count**
  - **Objective:** Make `GET /:code` redirect and increment the click count in one database statement.
  - **Files:** [new] `src/routes/redirect.ts`; [new] `test/redirect.test.ts`
  - **Depends on:** T2
  - **Done when:** Valid codes return the approved redirect, unknown codes return 404, and concurrent requests increase the count by the request total.
  - **Validate:** `npm test -- test/redirect.test.ts`
  - **Rollback:** Revert the isolated task commit and confirm shorten requests still pass their focused test.

### M3 - Container

*After this ships: The service can run from one repeatable image.*

- **T4 - Add the container smoke path**
  - **Objective:** Build one image, start it, and prove the health endpoint responds.
  - **Files:** [new] `Dockerfile`; [existing] `package.json`; [new] `scripts/smoke-container.mjs`
  - **Depends on:** T3
  - **Done when:** The smoke command builds the image, starts one temporary container, checks `/health`, and removes the temporary container.
  - **Validate:** `npm run smoke:container`
  - **Rollback:** Revert the isolated task commit and confirm the existing local start command remains unchanged.

## Checkpoints

### After M1

- **Gate:** T1 passes with the approved database version.
- **Validate:** `npm test -- test/spike/idempotency.test.ts`
- **Rollback:** Revert the M1 commit before endpoint work starts.

### After M2

- **Gate:** T2 and T3 pass their focused tests.
- **Validate:** `npm test -- test/shorten.test.ts test/redirect.test.ts`
- **Rollback:** Revert M2 task commits in reverse order and confirm the M1 proof remains green.

### After M3

- **Gate:** T4 passes and leaves no temporary container.
- **Validate:** `npm run smoke:container`
- **Rollback:** Revert the M3 task commit and use the prior approved local start command.

## Risks & mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Concurrent inserts create different codes | Medium | High | Prove the database rule in M1 before endpoints |
| Concurrent redirects lose click updates | Medium | High | Use one atomic statement and a focused concurrent test |

## Validation

- `npm test -- test/spike/idempotency.test.ts test/shorten.test.ts test/redirect.test.ts` - all current behavior checks pass.
- `npm run smoke:container` - the image starts, answers health, and cleans up.

## Stop conditions

- Stop if the design needs authentication or a second tenant.
- Stop before a destructive schema change.
- Stop if validation needs a new service or paid account.
