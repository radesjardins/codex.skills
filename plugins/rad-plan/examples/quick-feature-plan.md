# Plan: Settings Theme Toggle

**Status:** APPROVED
**Updated:** 2026-08-06
<!-- rad-plan-contract: 7.1 -->

## Objective

Add a saved light and dark theme choice to the existing settings screen.

**End goal:** Users can control appearance across every signed-in session.

## Release map

- **Now - Theme toggle (this plan):** Add one saved setting and apply it at startup.
- **Next - Appearance options:**
  - Follow system setting
- **Later - the end goal:**
  - Shared appearance rules across all product surfaces

## Scope

**In scope:**
- Light and dark choices
- Saved preference for signed-in users

**Out of scope / non-goals:**
- Custom colors
- Anonymous-user persistence

## Key assumptions

- [2026-08-06] The existing settings store supports one string preference.

## Outcome coverage

| Outcome | Covered by | Final proof |
|---|---|---|
| O1 - A signed-in user can select a theme and see it after a reload | T1, T2 | `npm test -- theme-toggle.test.tsx` |

## Milestones

| # | Milestone | Ships | Key artifacts |
|---|---|---|---|
| M1 | Theme choice | Saved toggle and startup application | Settings component and theme helper |

## Tasks

### M1 - Theme choice

*After this ships: A signed-in user can choose light or dark mode and keep the choice after a reload.*

- **T1 - Save the theme choice**
  - **Objective:** Add the theme field to the existing settings store and expose its current value.
  - **Files:** [existing] `src/settings/store.ts`; [existing] `src/settings/store.test.ts`
  - **Depends on:** none
  - **Done when:** The store saves `light` or `dark`, rejects other values, and returns the saved value on reload.
  - **Validate:** `npm test -- src/settings/store.test.ts`
  - **Rollback:** Revert the isolated task commit and confirm the previous settings tests pass.
- **T2 - Add and apply the toggle**
  - **Objective:** Add the control to settings and apply the saved class during startup.
  - **Files:** [existing] `src/settings/Appearance.tsx`; [existing] `src/app/theme.ts`; [new] `src/settings/theme-toggle.test.tsx`
  - **Depends on:** T1
  - **Done when:** Selecting either option changes the theme, reload keeps it, and a save error leaves the prior choice visible.
  - **Validate:** `npm test -- src/settings/theme-toggle.test.tsx`
  - **Rollback:** Revert the isolated task commit and confirm the settings screen still loads with its prior controls.

## Checkpoints

### After M1

- **Gate:** T1 and T2 focused tests pass.
- **Validate:** `npm test -- src/settings/store.test.ts src/settings/theme-toggle.test.tsx`
- **Rollback:** Revert the two task commits in reverse order and confirm the previous settings test remains green.

## Risks & mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Startup flashes the wrong theme | Medium | Medium | Apply the saved class before the main screen renders |

## Validation

- `npm test -- src/settings/store.test.ts src/settings/theme-toggle.test.tsx` - save, reload, invalid value, and error behavior pass.

## Stop conditions

- Stop if the existing store cannot save a new field without a schema migration.
