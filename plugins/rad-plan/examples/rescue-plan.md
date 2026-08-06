# Plan: Rescue the Local Notes CLI

**Status:** APPROVED
**Updated:** 2026-08-06
<!-- rad-plan-contract: 7.1 -->

## Objective

Return the abandoned notes CLI to a known state and finish the kept add and list commands.

**End goal:** One dependable local CLI stores, lists, searches, and exports plain-text notes.

## Release map

- **Now - Known baseline (this plan):** Prove current storage, finish add and list, and record the local command.
- **Next - Search and export:**
  - Search note text
  - Export all notes to Markdown
- **Later - the end goal:**
  - Reliable local note use without a hosted service

## Scope

**In scope:**
- Keep the existing JSON storage format
- Finish add and list
- Add focused behavior tests

**Out of scope / non-goals:**
- Cut the unfinished sync service
- No accounts, cloud storage, or mobile client

## Key assumptions

- [2026-08-06] Existing local note files must remain readable.
- [2026-08-06] The owner chose to remove sync from current direction.

## Stack

Keep the existing Python standard-library CLI and JSON storage.

## Outcome coverage

| Outcome | Covered by | Final proof |
|---|---|---|
| O1 - Current note files load without data loss | T1 | `python -m unittest tests.test_storage` |
| O2 - A user can add and list notes from the CLI | T2, T3 | `python -m unittest tests.test_cli` |

## Milestones

| # | Milestone | Ships | Key artifacts |
|---|---|---|---|
| M1 | Verified baseline | Known storage behavior and fixture | Storage test |
| M2 | Core CLI | Add and list commands | Command handlers and CLI tests |

## Tasks

### M1 - Verified baseline

*After this ships: The owner knows which current note files are safe to keep.*

- **T1 - Lock the current storage contract**
  - **Objective:** Add fixtures for two real, owner-approved note-file shapes and prove they load without mutation.
  - **Files:** [existing] `notes/storage.py`; [new] `tests/fixtures/notes-v1.json`; [new] `tests/test_storage.py`
  - **Depends on:** none
  - **Done when:** Both approved fixtures load with the same note IDs, text, and dates.
  - **Validate:** `python -m unittest tests.test_storage`
  - **Rollback:** Revert the isolated test commit. Keep the approved source fixtures outside generated output.

### M2 - Core CLI

*After this ships: The user can add a note and list saved notes from the terminal.*

- **T2 - Finish add**
  - **Objective:** Complete the existing add handler using the locked storage contract.
  - **Files:** [existing] `notes/commands/add.py`; [existing] `tests/test_cli.py`
  - **Depends on:** T1
  - **Done when:** A valid note receives one ID and persists, while empty text returns the approved error without changing the file.
  - **Validate:** `python -m unittest tests.test_cli.AddTests`
  - **Rollback:** Revert the isolated task commit and confirm the storage contract test stays green.
- **T3 - Finish list and remove sync entry point**
  - **Objective:** Complete list ordering and remove the owner-rejected sync command from CLI registration.
  - **Files:** [existing] `notes/commands/list.py`; [existing] `notes/cli.py`; [existing] `tests/test_cli.py`
  - **Depends on:** T2
  - **Done when:** List prints newest notes first and help output contains no sync command.
  - **Validate:** `python -m unittest tests.test_cli.ListTests tests.test_cli.HelpTests`
  - **Rollback:** Revert the isolated task commit and restore the prior approved CLI registration from its task commit.

## Checkpoints

### After M1

- **Gate:** T1 proves both approved file shapes.
- **Validate:** `python -m unittest tests.test_storage`
- **Rollback:** Revert the test commit and leave user note files unchanged.

### After M2

- **Gate:** Add, list, and help behavior pass.
- **Validate:** `python -m unittest tests.test_cli`
- **Rollback:** Revert M2 task commits in reverse order and confirm M1 remains green.

## Risks & mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Existing note files have an unknown third shape | Medium | High | Stop on unknown fields and ask before migration |

## Validation

- `python -m unittest tests.test_storage tests.test_cli` - approved storage and core commands pass.

## Stop conditions

- Stop on an existing note file that does not match an approved fixture.
- Stop before deleting any sync code outside CLI registration.

## Durable follow-ups

- `docs/prd.md`: Record the owner decision that hosted sync is outside the product goal.
