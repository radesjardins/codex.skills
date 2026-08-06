# rad-plan

RAD Plan creates, rescues, updates, and audits implementation plans for Codex. It is built for solo developers who want one clear plan without adopting a full spec system.

It writes planning artifacts. It never implements application code.

## What it adds

- An evidence-first interview that confirms repository facts before asking questions.
- Eight discovery areas for full planning, with no more than three rounds.
- A quick path with one batch of no more than five questions.
- A Now, Next, and Later release map. Only Now receives task detail.
- A bounded read of the real implementation surface before task paths are named.
- One plan contract for a human owner and a fresh coding agent.
- Outcome-to-task coverage with final proof.
- Risk-first milestones and safe recovery rules.
- Mechanical lint plus one adversarial risk pass.
- Separate rescue, replan, and review workflows.

## Skills

| Skill | Use it for | Result |
|---|---|---|
| `rad-plan:plan` | A new project, feature, or clear next effort | An approved current plan |
| `rad-plan:rescue` | An abandoned, unclear, or poorly documented project | Evidence-led intent recovery and a new plan |
| `rad-plan:replan` | Shipped work, changed scope, obsolete tasks, or a new release | A plan reconciled with Git evidence |
| `rad-plan:review-plan` | An audit before execution | Mechanical findings and one risk verdict |

## Quick and full planning

The owner chooses the depth.

**Quick** is for one known change in one system with no new service, deployment target, auth, payment, personal-data, or schema risk.

- One evidence pass
- One question batch, with five questions maximum
- One mirror and assumption check
- No PRD draft unless requested
- One risk pass
- `plan.md` only by default

**Full** is for new products, unclear architecture, cross-system work, migrations, auth, payments, personal data, or a new deployment target.

- Up to three discovery rounds
- Optional stack review when a real choice exists
- One first risk pass
- Another pass only after REVISE and a plan change, with three passes maximum

## Plan contract

The current plan normally lives at `docs/plan.md` and uses this model:

- Goal: one product end state in the PRD.
- Release: Now, Next, or Later.
- Milestone: a shippable part of Now.
- Task: one bounded work item.

Each task has six fields:

- Objective
- Files, with `[existing]` or `[new]` labels
- Depends on
- Done when
- Validate
- Rollback

The plan also maps every current outcome to live tasks and final proof. A live plan above 20 tasks gets a split warning.

See [Plan Contract 7.1](references/plan-template.md).

## Safe recovery

Rollback describes how to restore code, data, configuration, deployment, or external state. Generated plans do not use destructive Git or recursive-delete commands as rollback steps. When no safe automatic path exists, the plan says that owner-led recovery is required.

## Planning documents

RAD Plan keeps the write surface small:

- It writes the current plan.
- It can create a missing PRD from confirmed interview answers and section approval.
- It can append confirmed entries to decisions or ideas files that already exist.
- It records other confirmed document changes inside `## Durable follow-ups` in the plan.
- It does not create architecture, API, decisions, ideas, status, roadmap, timeline, or temporary update-prompt files.

## Companion plugins

RAD Plan can work alone.

It names a RAD Repo or RAD Brainstorm skill only when the exact skill is installed and appears in the current available-skill list, current evidence needs that workflow, and using it would add clear value. It never invokes a suggested companion until the owner asks or accepts.

The public brainstorming companion will use the `rad-brainstorm:*` namespace.

## Stack decisions

RAD Plan keeps the current stack when it can meet the requirement. When a real choice exists, the stack advisor checks existing fit, user constraints, current documentation, test support, deployment, maintenance, compatibility, security, license, cost, and operating burden.

There is no fixed language or framework default. See the [Stack Decision Scorecard](references/golden-path-matrix.md).

## Mechanical checks

`scripts/plan-lint.py` checks:

- required sections;
- the six task fields;
- duplicate sections and task IDs;
- missing, self, contradictory, and cyclic dependencies;
- Outcome coverage links and final proof;
- 7.1 file labels;
- vague Done when, Validate, and outcome proof phrases;
- more than 20 live tasks;
- unsafe rollback command forms.

`scripts/validate-json.py` checks stack-advisor and risk-assessor output against their JSON schemas.

Both scripts use Python 3.8 or later and require no package. The optional `jsonschema` package gives fuller draft-07 support.

## Fit

RAD Plan is a good fit for one person or a small team working in one repository. A current release should stay below 20 live tasks when practical.

Larger programs can still use it by planning one bounded release at a time. RAD Plan does not add a task database, execution engine, model router, MCP server, background process, or multi-repository coordinator.

## Relationship to Codex Plan mode

Codex Plan mode can structure a planning conversation. RAD Plan adds the evidence protocol, quick/full depth, release map, durable plan contract, outcome coverage, rescue, replan, and mechanical checks.

## License

MIT
