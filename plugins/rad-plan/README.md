# RAD Plan

RAD Plan is an Agent Plugins 1.0.0 package that creates and maintains implementation plans for Codex. It is for a solo builder or small team that wants one checked plan without adding a task database or a large set of spec files. Its checks can find plan defects, but they cannot prove that the planned architecture will work.

The plugin writes planning documents. It does not implement application code.

## Skills

| Skill | Use it for | Main result |
| --- | --- | --- |
| [rad-plan:plan](skills/plan/SKILL.md) | A new project, feature, or clear next effort | An owner-approved implementation plan |
| [rad-plan:rescue](skills/rescue/SKILL.md) | A project with unclear status, stale documents, abandoned work, or uncertain intent | An evidence-labeled state report and a new plan based on what exists |
| [rad-plan:replan](skills/replan/SKILL.md) | A plan made inaccurate by shipped work, changed scope, or new evidence | A plan reconciled with Git and repository evidence |
| [rad-plan:review-plan](skills/review-plan/SKILL.md) | A readiness and risk check on an existing plan | A mechanical report, a risk verdict, and proposed edits |

## How planning works

RAD Plan reads repository evidence before it asks the owner to repeat facts. For an existing project, it checks authority documents, the current plan, top-level configuration, recent design files, and a bounded part of the likely code surface.

The owner chooses quick or full depth.

Quick mode is for one known change in one system without a new service, deployment target, authentication, payment, personal-data, or schema risk. It uses one evidence pass and one batch of up to five questions.

Full mode is for new products, unclear architecture, work across systems, migrations, authentication, payments, personal data, or a new deployment target. It uses up to three interview rounds and can add bounded stack and risk reviews.

Both modes create a Now, Next, and Later release map. Only Now receives detailed tasks.

## The plan contract

The default current plan is docs/plan.md. Every live task has six fields:

- Objective
- Files, marked existing or new
- Depends on
- Done when
- Validate
- Rollback

The plan maps each current outcome to live tasks and final proof. It warns when the current release grows past 20 live tasks.

The mechanical linter checks required sections, task fields, duplicate IDs, dependency errors and cycles, outcome links, file labels, vague proof phrases, task count, and unsafe rollback command forms.

The risk review is separate. It looks for product, architecture, sequencing, validation, and recovery problems that a rule-based linter cannot decide.

## What is specific about it

RAD Plan shares familiar parts with chat planning, spec templates, and task breakdown tools.

Its specific combination is:

- repository evidence before the interview;
- quick and full depth with stated limits;
- one maintained plan with coarse future work;
- outcome-to-task coverage;
- a six-field task contract with recovery;
- separate rescue and replan paths for existing projects;
- deterministic lint followed by one bounded judgment review.

This keeps the workflow smaller than systems that add a task database, execution engine, model router, or multi-repository coordinator.

## Write boundary

RAD Plan can write the current plan. It can create a missing or skeletal PRD only from confirmed answers and only after section approval.

It may append an approved decision or idea when the matching file already exists. Other confirmed document work stays in a Durable follow-ups section in the plan.

The plugin does not create architecture, API, status, timeline, or temporary update-prompt files.

## Limits

- The linter checks document structure and selected wording. It cannot prove that an architecture will work.
- The risk review is model judgment. The owner still decides whether a risk is real and what trade-off to accept.
- File inspection is bounded. Uncertain paths become discovery work instead of invented paths.
- Rescue does not run or repair the application. Unknown runtime behavior stays unknown or becomes a plan task.
- Replan treats work as shipped only when repository evidence supports it.
- The plugin is best used for one repository and one bounded current release.
- Plan approval does not authorize implementation.

RAD Plan can work alone. It names a RAD Repo or RAD Brainstorm skill only when the exact skill is available, the evidence needs it, and it would add clear value. It waits for owner acceptance before invoking a companion.

## Install

~~~powershell
codex plugin add rad-plan@radesjardins-codex-skills
~~~

Example requests:

- "Create a quick implementation plan for this known change."
- "Rescue this project. Use repository evidence and do not run the app."
- "Replan docs/plan.md from the work that has shipped."
- "Review this plan for outcome coverage, dependency errors, and unsafe recovery."

## Scripts

The plugin includes:

- scripts/plan-lint.py for the plan contract;
- scripts/validate-json.py for optional stack and risk review output.

Both work without a required third-party package. See [scripts/README.md](scripts/README.md) for commands and exit codes.

## License

MIT. See [LICENSE](LICENSE).
