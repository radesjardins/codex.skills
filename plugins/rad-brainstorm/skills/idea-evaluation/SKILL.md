---
name: idea-evaluation
description: Use when the user already has two or more ideas and wants to compare, rank, test, or select among them. Do not use to create the first idea set, conduct a root-cause interview, produce a technical design, or plan implementation.
---

# Idea Evaluation

Evaluate an existing idea set without restarting broad ideation. The user scores first and makes the final choice.

Resolve the plugin root as the directory two levels above this `SKILL.md`. Read only the selected section in `references/evaluation-frameworks.md`.

## Companion-skill rule

Name `rad-council:convene` only when it is installed, appears in the current available-skill list, the decision is high-stakes, opposed expert views would add clear value, and the user accepts.

## 1. Prepare the idea set

List every candidate with a stable ID. Label ideas supplied in this session as `[user]`, `[AI]`, or `[research]`. Ask whether the set is complete. Route back to `rad-brainstorm:brainstorm-session` only when more options are needed.

For ten or more ideas, or obvious duplicates:

1. Cluster exact and near duplicates by underlying mechanism.
2. Preserve each original ID, wording, and source.
3. Ask before merging ideas that differ in audience, mechanism, channel, cost, or risk.

## 2. Select one framework

Recommend the smallest method that answers the decision question:

| Situation | Method |
| --- | --- |
| Ten or more ideas | Impact and Effort |
| Major unknowns | Assumption Mapping |
| Ideas tied to one product outcome | Opportunity Solution Tree |
| High-risk choice | Pre-Mortem, then Assumption Mapping |
| Two or three finalists | Weighted Scoring |
| Unclear user need | Jobs-to-be-Done |

Define criteria before scoring. Avoid false precision when results are close.

## 3. Apply the method

Ask one question at a time. Record user scores separately from AI comments. For each leader, capture:

- evidence-backed strength;
- main trade-off;
- riskiest assumption;
- cheapest useful proof;
- pass threshold;
- stop signal.

Use a threshold that can be observed. If a useful threshold cannot yet be set, name the missing evidence and the decision needed to set it.

## 4. Challenge only when useful

Offer one deeper challenge only when the stakes justify it and the result could change. If accepted, use `references/subagent-prompts/idea-challenge.md`. Run it with one bounded, read-only subagent when available, or perform the same check directly. Require JSON-first output and run schema validation with `scripts/validate-json.py` and `idea-challenge.schema.json`. Re-prompt once on failure.

## 5. Present the result

Use `references/session-output.md` and keep the result concise:

- recommended idea and why it leads;
- strong alternative and its main trade-off;
- parked or rejected ideas;
- riskiest assumption;
- cheapest proof, pass threshold, and stop signal.

Ask whether the result matches the user's judgment. For a chosen software idea that needs technical design, offer `rad-brainstorm:software-design`. Do not start implementation.
