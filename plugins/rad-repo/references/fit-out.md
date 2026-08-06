# Fit-out — equip the repo for what it actually is

Run during `/adopt` or when the owner explicitly asks for fit-out, after the repo has
enough code to show its traits. Never run at `repo-init` or inside `/ship` because
those workflows have a different job.

## Procedure

1. **Detect traits** — mechanical reads only (configs, lockfiles, route files, git
   remotes). Say what evidence produced each detection.
2. **Propose the matching equipment as one menu** — every detected trait with its
   install, plain language, one line each. The owner approves once (pick any subset).
3. **Install only what was approved.** Record the outcome in AGENTS.md as one line
   (example: `fit-out: 2026-07-02, deploy-target, api.md`) so fit-out never re-runs
   uninvited.
4. **Fit the executable contract.** Infer build, test, lint, type-check, and deploy
   commands from package scripts, CI, and existing instructions. Propose root defaults
   plus scoped overlays only where a subtree materially differs. Never invent a
   command; leave it undeclared and surface the gap when evidence is absent.

## The trait table

| Trait detected | Evidence | Installs (on approval) |
|---|---|---|
| Coolify/Vercel deploy target | coolify config / vercel.json / owner says so | `deploy: <target>` line in AGENTS.md enables one check for `/ship and verify deploy` |
| API routes | route files/patterns in code | `docs/api.md` seeded from the actual routes → activates the route-diff in `repo-align` |
| UI-heavy | substantial frontend tree (components/, pages/, styles) | visual-verify-before-done rule in AGENTS.md (render at desktop + 375 px before claiming done) |
| TypeScript | tsconfig.json | a typecheck reminder rule in AGENTS.md |
| CMS-backed content | CMS config/SDK in dependencies | content-field ↔ CMS-config lockstep rule in AGENTS.md |
| >1 moving part | multiple services/apps/workers in the tree | `docs/architecture.md` seeded (1 page: the parts and how they talk) |
| Subtree-specific commands or constraints | package-local scripts, generated code, ownership, or runtime boundary | closest scoped `AGENTS.md`, containing only the differing rules and commands |
| Executable code | verified package/CI commands | labeled validation commands in applicable `AGENTS.md`; optional `.rad-repo.json` path scopes |
| Approved finite migration | accepted plan with multiple milestones or rollback needs | `docs/initiatives/<slug>.md` from the initiative template, linked from `docs/plan.md` |

Rules that land in AGENTS.md count against the ≤7 hard-rule slots — if the menu
would blow the budget, say so and let the owner choose what earns a slot.

Nothing on the menu is mandatory; a declined item can be added later by re-running
fit-out on request.
