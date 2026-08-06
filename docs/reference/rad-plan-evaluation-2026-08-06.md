# Deep Research: RAD Plan Plugin Evaluation

**Date:** 2026-08-06
**Scope:** Public `rad-plan` plugin in `radesjardins/codex.skills`
**Research depth:** Thorough
**Repository state reviewed:** Local public marketplace source at the time of this report

## Executive Summary

RAD Plan has a strong place in the market. It sits between a short chat plan and a full spec-driven development system. Its best user is a solo builder who wants one clear implementation plan, wants the agent to ask hard questions first, and does not want a new task database or a large tree of planning files.

The plugin does five things especially well. It gathers evidence before it asks questions. It uses a capped interview that a non-engineer can answer. It keeps future work coarse through a Now, Next, and Later release map. It has separate rescue and replan paths for existing projects. It also combines a deterministic linter with an adversarial review. That is a rare mix among small planning skills.

RAD Plan is stronger than simple Plan modes because it creates a durable artifact and checks it. It is easier to live with than Spec Kit, OpenSpec, BMAD, GSD Core, Kiro Specs, and Task Master because it does not require their full file trees, command sets, state stores, or execution loops. Among the tools reviewed, RAD Plan has one of the clearest planner-only boundaries.

The main problems are inside the plugin. Its rules do not fully agree with each other. The TDD reference requires a test strategy in every task, while the template and linter define only six task fields. The anti-pattern reference says the linter checks rules that the code does not check. The risk prompt can lint the wrong path. The sample rollback commands can erase unrelated local work. These are product defects, not minor wording issues.

The package also carries more opinion than it needs. The Golden Path matrix makes TypeScript a fixed default and contains vendor and framework choices that age fast. Several anti-patterns concern code review or infrastructure design instead of plan quality. The quick path still runs most of the full workflow. Public documentation links to `rad-brainstormer`, which is absent from this marketplace.

I recommend a focused 7.1 release:

1. Replace unsafe rollback examples and rules.
2. Make the template, TDD rules, risk prompt, and linter agree.
3. Add small tests for both validator scripts.
4. Apply the active-plugin suggestion rule to RAD Repo and RAD Brainstormer references.
5. Add a bounded implementation-surface check before the planner names files.
6. Add a small outcome-to-task coverage table inside `plan.md`.
7. Make the quick path truly short.
8. Replace the stack matrix with a neutral decision scorecard.
9. Cut planning-irrelevant anti-patterns and extra document creation.

RAD Plan should avoid an execution engine, task database, MCP server, complexity score, model router, or multi-repo coordinator. Those features would erase its main advantage.

## Research Method and Limits

This review used four evidence groups:

- The complete public RAD Plan package, including all four skills, references, scripts, schemas, examples, and plugin metadata.
- Direct runs of `plan-lint.py` against the included sample plan. The sample returned zero issues.
- Primary sources from the official repositories and documentation for the compared tools.
- Recent research about spec-driven development and machine-checked planning.

The local package has 23 files, 147,714 bytes, about 3,022 lines, and about 20,281 words. The main `plan` skill alone has 346 lines and about 2,745 words. These counts describe package weight. Codex loads references on demand, so the whole package does not enter one prompt at once.

The Firecrawl interface was unavailable in this session. The review used live web search as the allowed fallback. I did not install or run the compared products. Claims about their behavior come from their official docs, source repositories, and selected public issues. Product comparisons are therefore design comparisons, not a controlled benchmark.

## Product Definition

RAD Plan 7.0.0 contains four user workflows:

| Skill | Main job | Durable result |
|---|---|---|
| `plan` | Interview, plan, validate, review, and approve new work | `docs/plan.md`, plus conditional planning documents |
| `rescue` | Rebuild intent and direction from an unclear existing project | A new plan and, when approved, a missing PRD |
| `replan` | Reconcile the plan with Git evidence and changed direction | Updated plan with shipped history preserved |
| `review-plan` | Audit an existing plan without implementation | Review report, with plan edits only after approval |

The core model uses one vocabulary:

- Goal: the end state.
- Release: Now, Next, or Later.
- Milestone: a shippable part of the current release.
- Task: one bounded work item.

Each live task has six fields: Objective, Files, Depends on, Done when, Validate, and Rollback. The planner writes task detail only for Now. This prevents false precision for distant work.

The public description calls RAD Plan a strict planner. That is mostly accurate. It does not write application code. It can still create or update several planning and repository documents, including a new PRD, decisions, ideas, architecture, API, and an update-prompt. The clearer claim is: **RAD Plan writes planning artifacts only and never implements application code.**

## Key Findings

### 1. RAD Plan has a clear middle position

Simple Plan modes let an agent inspect a repository and discuss an approach without editing source. Claude Plan mode and Cline Plan mode use this model. They are fast, but the plan can remain inside the session unless the user asks for a file. See [Claude Code Plan mode](https://code.claude.com/docs/en/permission-modes) and [Cline Plan and Act mode](https://docs.cline.bot/core-workflows/plan-and-act).

Full spec systems create several linked artifacts and often continue into implementation. Spec Kit uses constitution, spec, plan, checklist, tasks, analysis, implementation, and convergence. OpenSpec uses proposal, specs, design, tasks, apply, verify, sync, and archive. GSD Core adds research, state, execution waves, verification, and shipping. These systems can manage larger work, but they ask the user to adopt a full method.

RAD Plan offers more control than a chat plan and less process than a spec suite. That is its best product position.

### 2. The interview is the strongest feature

The discovery protocol has eight coverage areas, a mirror-back step, no more than three rounds, and explicit assumptions for anything still unknown. It also reads repository evidence and dated spec documents before asking questions. See the [discovery interview](../../plugins/rad-plan/references/discovery-interview.md).

Several competitors ask questions. GSD Core gathers project context before it builds a roadmap. Kiro Quick Spec asks clarifying questions before it creates requirements, design, and tasks. Spec Kit has a dedicated clarify command. RAD Plan goes further for a non-engineer because it defines what a settled answer looks like and proposes assumptions for confirmation.

The round cap matters. GSD says it asks until it understands the idea. That can work well, but it has no clear cost bound in the top-level workflow. RAD Plan makes the stopping rule visible.

### 3. The release map prevents false precision

The Now, Next, and Later model is simple. Only Now receives task detail. Replan pulls the next horizon into detail after current work ships. This is easier to maintain than a large roadmap that gives equal detail to work many months away.

Spec Kit, BMAD, GSD Core, and Task Master can model more work and more states. RAD Plan is better for a solo owner who needs the next release to be executable and the rest to stay flexible.

### 4. Rescue and replan are major advantages

Many tools are good at starting a feature from a clean request. RAD Plan also has an intent-recovery workflow. Rescue reads code, Git history, unfinished work, and surviving documents, then asks the owner what to keep, cut, or leave unknown. It plans the repair without changing code. See the [rescue skill](../../plugins/rad-plan/skills/rescue/SKILL.md).

Replan has a separate purpose. It classifies shipped, partial, unstarted, obsolete, and unplanned work from evidence. It preserves shipped tasks and records changed assumptions. See the [replan skill](../../plugins/rad-plan/skills/replan/SKILL.md).

GSD Core has brownfield onboarding and codebase mapping. OpenSpec has delta specs for changes to existing behavior. RAD Plan has the better human recovery model for a solo owner who returns to an abandoned or confused project. OpenSpec has the better change model after requirements shift because its Added, Modified, and Removed sections show the exact delta.

### 5. Mechanical checks are useful, but narrower than the product claims

`plan-lint.py` checks required sections, six task fields, duplicate task IDs, dependency references, cycles, and a short list of vague phrases. The included sample plan passes. The code is small, readable, uses the Python standard library, and returns clear exit codes. See the [plan linter](../../plugins/rad-plan/scripts/plan-lint.py).

`validate-json.py` checks the two subagent output contracts. It uses the `jsonschema` package when present and a built-in subset when absent. This is a good failure boundary. The caller can reject malformed agent output before it changes the plan. See the [JSON validator](../../plugins/rad-plan/scripts/validate-json.py).

The limits are important:

- Duplicate H2 section names overwrite earlier sections during parsing.
- Vague-language checks use a fixed phrase list and scan only Done when and Validate.
- The linter does not check milestone coverage, checkpoint count, safe rollback, file existence, requirement coverage, or test strategy.
- The risk prompt hard-codes `docs/plan.md` for its linter command even when `review-plan` found a legacy plan elsewhere.
- There are no automated tests for either validator in the public package.

This is still valuable mechanical validation. The public claims should match the checks it actually performs.

### 6. Rollback guidance is unsafe

The sample plan uses `git restore` for task rollback and `git reset --hard` for milestone rollback. The failure-state reference uses `git checkout --` as its example. See the [sample plan](../../plugins/rad-plan/examples/plan.md) and [failure-state reference](../../plugins/rad-plan/references/failure-state-template.md).

These commands can erase unrelated uncommitted work. They also assume that every task starts from a clean, known commit. The planner does not prove that condition.

Rollback is a good task field. Keep it. Change its meaning to a safe recovery description:

- Name the data, file, config, or deployment state that must return to its prior state.
- Prefer a new revert commit after a task commit.
- For database work, name the down migration, backup, or forward-fix rule.
- Refuse any destructive Git command when the worktree is dirty or the target is not exact.
- Use `manual recovery required` when no safe automatic rollback exists.

This is the first fix to make.

### 7. The package is light at runtime and heavy in instruction content

RAD Plan needs only Python 3.8 for its scripts. It has no service, account, MCP server, Node package, task database, or index. This is a real strength.

Its instruction set is still large for four skills. The package repeats the same rules across the README, skill files, plan template, TDD reference, failure reference, anti-pattern list, context guide, and subagent prompts. Some repetition protects critical boundaries. Some creates drift, as the current contradictions show.

The right fix is consolidation. The plan template should own the plan contract. The linter README should describe only implemented checks. The risk prompt should link to short policy files. The skills should state workflow and gates without restating every field rule.

## Strengths and Weaknesses

### Strengths

| Strength | Why it matters |
|---|---|
| Evidence-first interview | The agent confirms repository facts instead of making the owner repeat them. |
| Clear user fit | The workflow is written for solo builders and non-engineers. |
| Capped discovery | Three rounds prevent an open-ended interview. |
| Mirror-back step | Owners can correct a wrong summary more easily than an abstract plan. |
| One vocabulary | Goal, Release, Milestone, and Task reduce naming confusion. |
| Detail decay | Future work stays flexible while current work is exact. |
| Single main plan | Users avoid a separate spec file for every feature. |
| Six-field task blocks | A fresh coding agent receives files, dependencies, checks, and recovery needs. |
| Risk-first order | Hard unknowns can be tested before dependent work grows. |
| Mechanical lint | Basic plan defects produce deterministic findings. |
| JSON contracts | Subagent output has a machine-checked boundary. |
| Human approval | The plan stays DRAFT until the owner approves it. |
| Rescue workflow | Unclear projects get intent archaeology without code changes. |
| Replan workflow | Shipped work and changed assumptions remain visible. |
| Planner-only boundary | The skill cannot silently become an implementation run. |
| Small dependency footprint | Git, Markdown, and Python are enough. |

### Weaknesses

| Weakness | Effect |
|---|---|
| Unsafe rollback examples | A future executor could erase unrelated local work. |
| TDD contract mismatch | Plans can pass lint while missing a rule the risk agent treats as required. |
| Overstated linter coverage | Users can trust checks that the code does not perform. |
| Hard-coded risk lint path | Legacy or custom plan paths can receive the wrong mechanical result. |
| No validator tests | Parser and schema changes can break without warning. |
| No outcome traceability | A clean plan can still omit a success criterion. |
| Weak file grounding | The planner can name files after reading only the repo shape and top-level context. |
| Quick path still has much of the full flow | Small work can receive too many questions and document actions. |
| Prescriptive stack matrix | Fixed technology opinions can override project fit and age quickly. |
| Broad anti-pattern list | Code-review and infrastructure opinions dilute plan review. |
| Extra writing surface | A single-plan product can create several other documents. |
| Missing plugin checks | Skills can name RAD Repo or RAD Brainstormer when those skills are unavailable. |
| Dead public link | The README links to a sibling `rad-brainstormer` plugin that is absent here. |
| Single example | A URL shortener does not test rescue, replan, migration, or tiny-feature behavior. |
| Codex-only | Users of other agents cannot use the package directly. This is acceptable for this marketplace. |

## Comparison With Similar Tools

| Tool or method | Main job | What it does better | Where RAD Plan is better |
|---|---|---|---|
| Claude Plan mode | Read-only research and proposal before editing | Very low setup and direct switch into implementation | Durable plan, interview method, lint, rescue, and replan |
| Cline Plan and Act | Separate discussion from file changes | Clear task-size guidance, checkpoints, and easy return to planning | One maintained plan and stronger planning contract |
| Aider architect mode | Use a reasoning model to propose changes and an editor model to apply them | Fast two-model handoff into code | Human approval artifact, long-term plan, and planner-only safety |
| Superpowers | Design, detailed plans, TDD, and subagent execution | Tight execution link, small coding steps, and code review loop | Better discovery, release horizons, rescue, replan, and mechanical plan lint |
| GitHub Spec Kit | Spec, plan, checklist, tasks, analysis, and implementation | Requirement quality checks, cross-artifact analysis, many agent integrations, and extensions | Much smaller file model and lower daily process cost |
| OpenSpec | Change-centered specs with apply, verify, sync, and archive | Delta specs, artifact dependency graph, update flow, and implementation-to-spec checks | One plan, less setup, clearer solo-owner interview, and strict planner boundary |
| Kiro Specs | Requirements, design, tasks, execution, and pull request | Polished interface, bug specs, requirements analysis, and multi-repo sessions | Open Markdown plan in the repo and no IDE or hosted workflow dependency |
| BMAD Method | Full product and engineering method with specialist skills | Deep product, UX, architecture, story, and review workflows | Far fewer roles, documents, and owner decisions |
| GSD Core | Discuss, plan, execute, verify, and ship in fresh contexts | Codebase mapping, requirement IDs, research, execution waves, state, and verification | Smaller scope, less agent activity, and no autonomous execution |
| Task Master | PRD-to-task graph and live task management | Task status, next-task selection, research, dependencies, tags, and complexity reports | No MCP server, API key, task store, or large tool surface |

### Simple planning modes

Claude and Cline use permission or mode boundaries to keep planning read-only. Cline also gives clear small, medium, and large task guidance. RAD Plan should borrow the size guidance, while keeping its durable plan and approval flow. See [Claude Plan mode](https://code.claude.com/docs/en/permission-modes) and [Cline task-size guidance](https://docs.cline.bot/core-workflows/plan-and-act).

### Superpowers

Superpowers writes plans with exact file paths, small TDD steps, commands, and frequent commits, then routes into plan execution or subagent development. It is a close skill-level rival because it is also available in Codex. Its plan can be more immediately executable for a known feature. RAD Plan is better at deciding what should be built, setting release boundaries, and recovering project intent. See [Superpowers writing-plans](https://github.com/obra/superpowers/blob/main/skills/writing-plans/SKILL.md) and the [Superpowers workflow](https://github.com/obra/superpowers).

### GitHub Spec Kit

Spec Kit has the strongest requirement quality loop in this group. `clarify` finds underspecified areas, `checklist` creates tests for requirement quality, and `analyze` checks the spec, plan, and tasks for conflicts and missing links. It also supports many coding agents and an extension system. See the [Spec Kit agentic workflow](https://github.com/github/spec-kit/blob/main/docs/reference/agentic-sdd.md) and [Spec Kit overview](https://github.github.com/spec-kit/).

Its cost is a larger method and more artifacts. Spec Kit also leaves teams to choose how specs change over time. Its own docs describe flow-back, flow-forward, and living-spec models. RAD Plan already chooses a simpler rule: keep one current plan and preserve shipped history. See [Spec Kit persistence models](https://github.github.com/spec-kit/concepts/spec-persistence.html).

### OpenSpec

OpenSpec is the strongest source for a better replan model. Its delta specs show Added, Modified, and Removed requirements. Reviewers see the change instead of rereading the full contract. OpenSpec also has a configurable artifact graph and a verify command that compares implementation evidence with requirements, tasks, and design. See [OpenSpec delta specs](https://github.com/Fission-AI/OpenSpec/blob/main/docs/concepts.md), [OpenSpec commands](https://github.com/Fission-AI/OpenSpec/blob/main/docs/commands.md), and [OpenSpec](https://github.com/Fission-AI/OpenSpec).

The extra artifacts can drift. An OpenSpec issue reports cross-artifact contradictions, scope drift, duplicate work, and file bloat after one-pass generation. This supports RAD Plan's single-file choice. See [OpenSpec issue 783](https://github.com/Fission-AI/OpenSpec/issues/783).

### Kiro Specs

Kiro provides feature, bug, and quick specs. It writes requirements, design, and tasks, can analyze requirements for gaps, and can run the task list. Its web product can plan across several repositories. See [Kiro Specs](https://kiro.dev/docs/web/specs/), [Kiro Quick Spec](https://kiro.dev/docs/specs/quick-spec/), and [Kiro requirement analysis](https://kiro.dev/docs/specs/analyze-requirements/).

RAD Plan does not need these product surfaces. It should borrow one idea: make risk depth depend on the work type. A data migration, auth change, external integration, or unclear bug needs more questions than a known UI feature.

### BMAD Method

BMAD covers product discovery, PRDs, UX, architecture, stories, sprint readiness, implementation, and code review. This is useful for a team that wants a full method. Its official workflow shows how many documents and roles can appear. See the [BMAD workflow map](https://github.com/bmad-code-org/BMAD-METHOD/blob/main/docs/reference/workflow-map.md).

A public brownfield report praises BMAD's elicitation and specialist agents while describing coordination and context friction. RAD Plan should keep the strong interview and avoid the role count. See [BMAD issue 446](https://github.com/bmad-code-org/BMAD-METHOD/issues/446).

### GSD Core

GSD Core is the strongest full-loop rival. It discusses a phase, researches it, creates plans, checks them, runs independent plans in waves, verifies outcomes, and ships. It also gives every executor a fresh context and keeps state in `.planning/`. See [GSD Core](https://github.com/open-gsd/gsd-core), [GSD commands](https://github.com/open-gsd/gsd-core/blob/next/docs/COMMANDS.md), and the [GSD first-project tutorial](https://github.com/open-gsd/gsd-core/blob/next/docs/tutorials/your-first-project.md).

GSD's requirement IDs and plan checker are worth studying. Its execution system, model profiles, state files, and many agents are outside RAD Plan's purpose.

### Task Master

Task Master parses a PRD into tasks, tracks status, finds the next task, manages dependencies and tags, runs research, and can generate complexity reports. It can load 7, 15, or 36 MCP tools. Its own README estimates about 5,000 tokens for the core tools and about 21,000 for all tools. See [Task Master](https://github.com/eyaltoledano/claude-task-master).

RAD Plan should avoid a live task manager and numeric complexity scores. A plan-quality linter can check structure and coverage without creating another state system.

## What RAD Plan Does Better

### It plans for a human owner and a coding agent

The release map and After this ships lines explain the work in product terms. The task blocks give the coding agent exact instructions. Many tools focus on one reader. RAD Plan treats both as first-class readers.

### It makes unknowns visible

Every discovery area must become settled or explicitly unknown. The planner proposes assumptions instead of asking the owner to invent them. This is more useful for the target user than a blank PRD form.

### It keeps the active artifact set small

One plan is easier to review than proposal, spec, design, tasks, state, roadmap, and research files. RAD Plan still preserves a durable history through the Shipped section.

### It has two good brownfield doors

Rescue answers, "What was this project trying to become?" Replan answers, "How did reality change this approved plan?" This split is clear and uncommon among the reviewed tools.

### It separates deterministic and judgment checks

The linter finds structural errors. The risk assessor reviews architecture, sequencing, rollback quality, context size, and tests. This division is sound. The contract needs repair, but the design is good.

### It refuses to implement

Many planning systems continue into code. RAD Plan stops at an approved plan. That gives Ryan a clean decision point and lets any coding workflow execute later.

## Where RAD Plan Falls Short

### The plan is not grounded deeply enough in the target code

The planner reads high-level repository evidence before discovery. It does not require a bounded trace of the exact implementation surface before it writes task file paths. A task can therefore name a plausible file that does not exist, miss an existing helper, or plan around the wrong boundary.

Add a short implementation-surface check after scope is settled and before task blocks are written:

1. Identify the likely entry point, affected module, nearest tests, and relevant config.
2. Read only those files and their direct imports or callers.
3. Mark each planned path as existing or new.
4. Record any uncertain path as an explicit task discovery step.
5. Stop after a small file budget, such as 12 files for quick and 30 for full.

This adds evidence without a codebase index or a separate map.

### The plan can pass while missing a product outcome

The linter checks task shape and dependencies. It does not prove that every MVP success criterion has a task and a final check. Spec Kit's `analyze` and GSD's requirement IDs handle this better.

Add a compact table inside `plan.md`:

| Outcome | Covered by | Final proof |
|---|---|---|
| O1: user can shorten a URL | T2 | API test command |

Use 3 to 10 outcomes. The linter can check that every outcome has at least one live task and one proof. This is enough traceability for a solo project.

### Internal contracts disagree

The [TDD reference](../../plugins/rad-plan/references/tdd-constraints.md) says every code task must include a Test Strategy block. The [plan template](../../plugins/rad-plan/references/plan-template.md) and linter require six fields without that block. The sample plan has no Test Strategy fields and still passes.

The [anti-pattern reference](../../plugins/rad-plan/references/anti-patterns.md) says the linter checks AGENTS.md line count and validation or rollback presence. The code does not read AGENTS.md and does not judge rollback content.

Choose one contract. My recommendation is to keep six fields. Put task-specific test detail in Validate. Require deeper test detail only for code that changes auth, payments, personal data, schemas, external integrations, or core business logic. Remove universal coverage percentages, mutation testing for every task, and full-suite runs after each refactor step.

### Quick is still too close to full

Quick skips the stack subagent and limits risk review to one pass. It still has eight discovery areas, up to three rounds, a PRD gap check, a full plan, review, and seed packet.

Set a real quick contract:

- One evidence pass.
- One question batch, no more than five questions.
- One mirror and assumption confirmation.
- No PRD draft unless the user asks.
- No stack review unless a new dependency or platform appears.
- One lint pass and one risk pass.
- Write only `plan.md` by default.

The full path keeps the current interview depth.

### The stack policy can bias good projects toward the wrong stack

The Golden Path matrix calls TypeScript a non-negotiable default and ranks frameworks by maintainer experience. The file honestly states that the tiers are not based on a published benchmark. It also includes product and platform choices that change often.

Replace the technology list with a decision scorecard:

- Fit with the existing repository.
- Fit with user skill and paid services.
- Quality of current primary documentation.
- Type or compiler feedback.
- Test support.
- Deployment fit.
- Maintenance status and license.
- Cost and operating burden.
- Evidence that a new tool solves a stated requirement.

Default to the existing stack when it can meet the requirement. Use live primary sources only when a real stack decision exists.

### The anti-pattern list is too broad

The current list includes vector database thresholds, MCP design, comments, fallbacks, stale APIs, test editing, and AGENTS.md length. Several are useful engineering opinions. They are not all plan-quality rules.

Keep a shorter planning risk list:

- Unclear outcome or missing user decision.
- Unbounded investigation.
- New service or dependency without a stated need.
- Unsafe data or deployment change.
- Validation that does not prove the outcome.
- Rollback that cannot restore state.
- Task or milestone too large for one bounded run.
- Plan choice that conflicts with approved product or architecture facts.

Security and technology checks can activate only when the plan touches those areas.

### The document boundary is wider than the product promise

The main skill says it produces one thing, then its export can write a PRD, decisions, ideas, architecture, API, and an update-prompt. The gated writes are careful, but the surface weakens the single-plan position and overlaps RAD Repo.

Keep the PRD birth because the interview already contains the needed answers. Keep append-only decisions and ideas when their files already exist. Remove default creation of architecture and API documents. Put pending durable-document changes in one small section inside `plan.md` instead of creating a temporary update-prompt file. When RAD Repo is present and the need is real, offer that workflow after approval.

### Plugin references need the same availability rule as RAD Repo

RAD Plan names `rad-repo` and `rad-brainstormer` in skill instructions. The public README also links to a sibling RAD Brainstormer folder that does not exist in this marketplace.

Use this rule:

> Name a companion RAD skill only when current evidence needs that exact workflow and the skill appears in the current available-skill list. When it is unavailable, report the need in plain language. Never invoke it from a suggestion unless the owner asks for it or accepts the suggestion.

Remove the dead README link until RAD Brainstormer is public.

### The validators need tests

The scripts are part of the product's strongest claim. They need a small fixture suite. Keep it narrow:

- One clean plan.
- Missing field.
- Duplicate section.
- Missing dependency.
- Dependency cycle.
- Vague validation.
- Unsafe rollback phrase.
- Custom plan path.
- Valid and invalid JSON for each schema.

No large test framework is needed. Standard-library `unittest` is enough.

## Elements Worth Adopting

### From Spec Kit: outcome coverage and requirement quality

Add the small Outcome coverage table and have the risk review check whether outcomes are clear, measurable, and consistent. Do this inside the current plan. Avoid a separate spec, checklist, and tasks file.

### From OpenSpec: delta thinking for replan

Before replan changes the file, show three groups:

- Added: new outcomes, milestones, tasks, or assumptions.
- Modified: changed scope, order, validation, or task meaning.
- Removed: obsolete work, with a reason and preserved history.

This can stay in the approval preview. Add one dated plan change note only when the owner approves it.

### From GSD Core: code-grounded planning

Use the bounded implementation-surface check. RAD Plan does not need a permanent codebase map, research folder, or four research agents.

### From Cline and Kiro: size and risk routing

Keep only quick and full. Improve the recommendation:

- Recommend quick for a known change in one system with no data, auth, payment, schema, or new-service risk.
- Recommend full for new products, unclear architecture, cross-system work, migrations, auth, payments, personal data, or a new deployment target.

The user still chooses.

### From Superpowers: exact existing and new file labels

Task paths should be concrete. Mark planned paths as `[existing]` or `[new]`. This small label reduces hallucinated file work and helps a fresh agent start faster.

### From Task Master: selectable depth without the task manager

RAD Plan already has the right surface with quick and full. Add no more tool profiles. The useful lesson is to keep expensive review optional and visible.

## Elements to Remove or Reduce

### Remove now

- `git reset --hard`, `git checkout --`, and unqualified `git restore` rollback examples.
- Claims that `plan-lint.py` checks AGENTS.md length or rollback quality.
- The dead `rad-brainstormer` repository link.
- Hard-coded `docs/plan.md` from the risk prompt when a plan path is supplied.
- Universal claims that every task needs mutation testing, fixed coverage targets, and full-suite runs after each refactor.

### Replace

- Replace the Golden Path technology table with the neutral stack scorecard.
- Replace the 14-item anti-pattern list with the short planning risk list.
- Replace the temporary update-prompt file with a section in `plan.md`.
- Replace automatic architecture and API seeds with an owner-approved companion workflow when needed.

### Keep

- Four skills. Do not merge rescue and replan.
- One current plan file.
- Now, Next, and Later detail decay.
- The eight discovery coverage areas for full planning.
- Mirror-back and proposed assumptions.
- Six task fields.
- Linter plus risk review.
- Human approval before APPROVED status.
- Shipped history.
- PRD birth from confirmed interview answers.
- Codex-only packaging for this marketplace.

## Recommended 7.1 Change Order

### P0: safety and contract truth

1. Replace unsafe rollback guidance and the sample commands.
2. Make six task fields the only task contract. Move risk-based test detail into Validate.
3. Correct the anti-pattern and README claims about linter coverage.
4. Pass the detected plan path into every linter call.
5. Apply the active-plugin suggestion rule.
6. Add validator fixtures for current and fixed behavior.

### P1: plan quality

1. Add the bounded implementation-surface check.
2. Add the Outcome coverage table and simple linter checks.
3. Add Added, Modified, and Removed preview groups to replan.
4. Mark task files as existing or new.
5. Give quick mode a one-round, five-question cap and a plan-only default.

### P2: reduce weight

1. Replace the Golden Path matrix with the stack scorecard.
2. Cut the anti-pattern list to planning risks.
3. Remove automatic architecture and API seeds.
4. Move pending durable-document changes into `plan.md`.
5. Remove repeated contract text from skills after the template becomes authoritative.

### P3: proof and examples

Add three small examples:

- A one-file feature using quick mode.
- A brownfield rescue with keep, cut, and unknown choices.
- A risky schema migration with safe recovery and outcome coverage.

These examples will show the product range better than adding another skill.

## Suggested Lean Workflow

The six-step shape can remain:

1. **Understand:** read authority docs and relevant code, then settle scope.
2. **Choose depth:** quick or full, with a clear recommendation.
3. **Decide stack only if needed:** use the neutral scorecard and current primary sources.
4. **Build:** release map, outcome coverage, milestones, and six-field tasks.
5. **Check:** deterministic lint, then one risk review by default. Full mode can repeat up to the current cap.
6. **Approve and write:** owner approval, one current plan, and small durable follow-ups inside it.

Rescue starts with intent archaeology before step 1. Replan starts with Git evidence and a delta preview before step 4. Review-plan runs step 5 against an existing plan.

## Suggested Public Positioning

> RAD Plan is a planning skill for solo builders who want one honest, executable plan without adopting a full spec system. It asks the questions you may not know to ask, checks the real repository, maps the current release in detail, and keeps future work flexible. It can also rescue an unclear project, replan from Git evidence, and audit a plan before coding begins. It writes planning artifacts and never implements application code.

This position is specific. It separates RAD Plan from chat-only planners and from full delivery systems.

## Contrarian Views and Risks

### One file can still become large

A single plan can become hard to read after many releases. Keep only live Now tasks in the main Tasks section. Move shipped work to history. If live work exceeds 20 tasks, split the release into a smaller plan instead of adding more nesting.

### Outcome mapping can become checkbox work

The coverage table should stay small. Three to ten product outcomes is enough. Do not create one outcome ID for every technical detail.

### Removing universal TDD rules can weaken some plans

Risk-based tests need clear triggers. Auth, payments, personal data, migrations, external integrations, and core business rules should receive explicit positive, negative, and recovery checks.

### A neutral stack guide can produce less decisive advice

The scorecard should still make a recommendation. It should prefer the current stack when it fits and name one best option when a new choice is required.

### More linter rules can recreate the same problem

The linter should check cheap facts only: structure, IDs, links, path labels, coverage links, duplicate sections, and unsafe command forms. Architecture and test quality remain judgment calls.

### Planner-only scope can feel incomplete

Competitors can move from idea to pull request. RAD Plan ends at approval. That stop is valuable for owners who want control. Public wording should make the boundary clear before installation.

### Research does not prove one universal planning method

Recent SDD papers support explicit specifications, validation, and different rigor levels. They do not prove that one artifact model works for every project. PlanBench also shows why machine checks matter, but it studies formal planning tasks rather than software project plans. RAD Plan should treat research as design input, not product proof.

## Owner Decisions and Implementation Status

Ryan approved the focused 7.1 changes with these decisions:

1. Keep RAD Plan Codex-only and planner-only. Keep all four skills and the six-field task contract.
2. Use `rad-brainstorm` as the future public plugin name and `rad-brainstorm:*` as its skill namespace.
3. Mention a RAD Brainstorm or RAD Repo skill only when the exact skill is installed, appears in the current available-skill list, fits the evidence, and adds clear value. Ask before invoking it.
4. Append confirmed choices or ideas only when `docs/decisions.md` or `docs/ideas.md` already exists. Keep other follow-ups in `## Durable follow-ups` inside the plan.
5. Set 20 live tasks as the warning point for one plan.
6. Run one risk pass by default. In full mode, repeat only after a `REVISE` result and a plan change, with three passes at most.
7. Keep PRD creation from confirmed answers in full mode or when the owner asks. Quick mode is plan-only by default.

The 7.1 implementation now includes outcome coverage, `[existing]` and `[new]` file labels, safe recovery rules, bounded research, a neutral stack scorecard, focused planning risks, corrected linter claims, and three small examples. It removes automatic architecture and API document creation and the temporary update-prompt example.

## Sources

### RAD Plan source reviewed

- [RAD Plan README](../../plugins/rad-plan/README.md): public promise, workflow, integrations, and requirements.
- [Plan skill](../../plugins/rad-plan/skills/plan/SKILL.md): discovery, stack, plan, review, export, and write boundaries.
- [Rescue skill](../../plugins/rad-plan/skills/rescue/SKILL.md): brownfield intent recovery.
- [Replan skill](../../plugins/rad-plan/skills/replan/SKILL.md): evidence-based plan changes and shipped history.
- [Review-plan skill](../../plugins/rad-plan/skills/review-plan/SKILL.md): mechanical and judgment audit flow.
- [Plan template](../../plugins/rad-plan/references/plan-template.md): required plan structure and task contract.
- [Plan linter](../../plugins/rad-plan/scripts/plan-lint.py): implemented deterministic checks.
- [JSON validator](../../plugins/rad-plan/scripts/validate-json.py): subagent contract checks.
- [TDD constraints](../../plugins/rad-plan/references/tdd-constraints.md): current test rules and contract mismatch.
- [Failure-state template](../../plugins/rad-plan/references/failure-state-template.md): current rollback guidance.
- [Golden Path matrix](../../plugins/rad-plan/references/golden-path-matrix.md): current stack opinions and stated limits.
- [Anti-patterns](../../plugins/rad-plan/references/anti-patterns.md): current risk list and overstated linter claims.

### Primary product and platform sources

- [GitHub Spec Kit](https://github.github.com/spec-kit/): current product scope, integrations, and extension model.
- [Spec Kit agentic SDD](https://github.com/github/spec-kit/blob/main/docs/reference/agentic-sdd.md): clarify, checklist, tasks, analyze, implement, and converge.
- [Spec Kit persistence models](https://github.github.com/spec-kit/concepts/spec-persistence.html): flow-back, flow-forward, and living-spec choices.
- [Spec Kit issue 1191](https://github.com/github/spec-kit/issues/1191): friction when refining existing specs.
- [OpenSpec](https://github.com/Fission-AI/OpenSpec): product scope and tool support.
- [OpenSpec concepts](https://github.com/Fission-AI/OpenSpec/blob/main/docs/concepts.md): artifact graph and delta specs.
- [OpenSpec commands](https://github.com/Fission-AI/OpenSpec/blob/main/docs/commands.md): propose, update, verify, sync, and archive behavior.
- [OpenSpec issue 783](https://github.com/Fission-AI/OpenSpec/issues/783): reported cross-artifact drift and missing semantic review.
- [OpenSpec issue 684](https://github.com/Fission-AI/OpenSpec/issues/684): questions and guidance for updating artifacts during implementation.
- [BMAD workflow map](https://github.com/bmad-code-org/BMAD-METHOD/blob/main/docs/reference/workflow-map.md): product, planning, architecture, and implementation phases.
- [BMAD issue 446](https://github.com/bmad-code-org/BMAD-METHOD/issues/446): brownfield user report about elicitation value and coordination cost.
- [GSD Core](https://github.com/open-gsd/gsd-core): discuss, plan, execute, verify, and ship loop.
- [GSD command reference](https://github.com/open-gsd/gsd-core/blob/next/docs/COMMANDS.md): current planning, onboarding, and fast-path commands.
- [GSD first-project tutorial](https://github.com/open-gsd/gsd-core/blob/next/docs/tutorials/your-first-project.md): requirement mapping, research, plan checking, and execution waves.
- [Task Master](https://github.com/eyaltoledano/claude-task-master): task graph, research, status, complexity, and selectable MCP tool sets.
- [Superpowers writing-plans](https://github.com/obra/superpowers/blob/main/skills/writing-plans/SKILL.md): small TDD tasks and execution-ready plans.
- [Superpowers](https://github.com/obra/superpowers): full design, plan, execution, and review workflow.
- [Kiro Specs](https://kiro.dev/docs/web/specs/): requirements, design, tasks, multi-repo planning, implementation, and pull requests.
- [Kiro Quick Spec](https://kiro.dev/docs/specs/quick-spec/): front-loaded clarification and faster artifact generation.
- [Kiro requirement analysis](https://kiro.dev/docs/specs/analyze-requirements/): ambiguity, conflict, and gap review.
- [Cline Plan and Act](https://docs.cline.bot/core-workflows/plan-and-act): planning boundaries and size-based routing.
- [Claude Code Plan mode](https://code.claude.com/docs/en/permission-modes): read-only planning and owner approval.
- [Aider chat modes](https://aider.chat/docs/usage/modes.html): ask, code, and architect-editor workflows.

### Research

- [From Prompt to Process](https://arxiv.org/abs/2606.04967): taxonomy and comparison of six AI software development frameworks.
- [Spec-Driven Development: From Code to Contract](https://arxiv.org/abs/2602.00180): spec-first, spec-anchored, and spec-as-source rigor levels.
- [PlanBench](https://arxiv.org/abs/2206.10498): machine-evaluated planning benchmark and limits of subjective plan review.
- [Comprehensive Evaluation of LLMs on Software Engineering Tasks](https://arxiv.org/abs/2602.07079): large efficiency differences across models and weak link between tool-call count and success.

## Rerun Inputs

```text
workflow: firecrawl-deep-research
topic: Evaluate the public RAD Plan Codex plugin against current planning skills, spec-driven development systems, task planners, and built-in planning modes
depth: thorough
output: markdown
constraints: Prefer primary sources; inspect local plugin source and validators; focus on solo and small-project use; recommend small changes that preserve planner-only scope; identify removal candidates; do not implement changes
fallback_used: live web search because the Firecrawl interface was unavailable
```
