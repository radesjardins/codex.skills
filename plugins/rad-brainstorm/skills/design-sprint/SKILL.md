---
name: design-sprint
description: Use when the user has chosen what software to build and wants a reviewable technical design or design spec before implementation planning. Do not use for open-ended ideation, code implementation, project scaffolding, or brand and visual design.
---

# Software Design Sprint

Turn one chosen software approach into a clear design spec. Do not write code, scaffold a project, or start implementation.

Resolve the plugin root as the directory two levels above this `SKILL.md`. Read `references/facilitation-principles.md` before asking design questions.

## Companion-skill rule

Name an exact RAD Plan or RAD Repo skill only when the exact skill is installed, appears in the current available-skill list, current evidence needs it, and it would add clear value. Never invoke it until the user asks or accepts.

## 1. Confirm the prerequisite

The user must have chosen what to build. Restate the chosen approach and ask for confirmation.

If the product direction is still open, route to `rad-brainstorm:brainstorm-session`.

## 2. Read project evidence

For an existing repository, inspect relevant docs, related code, tests, configuration, and recent Git history. Read `docs/design.md` when it exists and treat it as the brand and interface direction. Never overwrite it.

Keep this phase read-only.

## 3. Settle design decisions

Ask one question per turn. Prefer a short choice when the answer space is known.

Cover only decisions that affect the design:

- scope and exclusions;
- system boundaries;
- component responsibilities and interfaces;
- data model and flow;
- API behavior when relevant;
- error and recovery behavior;
- security, privacy, performance, and accessibility when relevant;
- test approach;
- migration and deployment when relevant.

Follow existing repository patterns unless a current pattern blocks the chosen outcome.

## 4. Design for isolation

Each unit needs one clear purpose, a defined interface, known dependencies, and a focused way to test it. Avoid new abstraction layers without a current need.

## 5. Present sections for approval

Present one section at a time and wait for the user's response:

1. Architecture overview
2. Components and interfaces
3. Data model and flow
4. API behavior when needed
5. Errors and recovery
6. Quality and test strategy
7. Migration and deployment when needed

Revise a section before continuing when the user finds a problem.

## 6. Deliver one spec

Ask where to save the result:

- In the current project, suggest `docs/YYYY-MM-DD-<topic>-spec.md`.
- Before a repository exists, suggest a dated Markdown file in a personal folder chosen by the user.
- The user may keep it in the conversation only.

Mark an in-project spec as transient when a planning workflow will consume it. Never write to `docs/design.md`. Never auto-commit.

The spec must include:

- selected approach and scope;
- architecture and components;
- interfaces and data flow;
- errors and recovery;
- relevant quality requirements;
- focused tests;
- migration or deployment details when needed;
- considered and rejected options with one-line reasons;
- confirmed deferrals with reasons.

Do not use TBD, TODO, "handle errors as needed," or similar placeholders.

If `docs/ideas.md` exists, offer to append rejected or parked options. Append only after the user accepts. Do not create the file.

## 7. Review the spec

First run an inline review:

- placeholder scan;
- contradiction scan;
- scope scan;
- ambiguity scan;
- missing error or recovery behavior;
- unneeded complexity.

Fix confirmed issues.

Then run one bounded, read-only spec review when subagents are available. Use `references/subagent-prompts/spec-review.md`, require JSON-first output, and validate it with `scripts/validate-json.py` and `spec-review.schema.json`. When subagents are unavailable, run the same checks directly.

If blocking issues remain, explain them and update the spec after user approval. A second subagent review happens only when the user asks.

## 8. Close and hand off

Ask the user to approve the spec. Do not begin implementation.

For implementation sequencing, name `rad-plan:plan` only under the companion-skill rule. When it is unavailable or adds no value, describe the next step as implementation planning without naming a plugin.
