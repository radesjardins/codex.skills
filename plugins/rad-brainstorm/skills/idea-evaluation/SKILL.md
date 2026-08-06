---
name: idea-evaluation
description: Use when the user already has two or more ideas and wants to compare, rank, test, or select among them with a clear evaluation method. Do not use to generate the first idea set, find a root cause, or create an implementation plan.
---

# Idea Evaluation

Evaluate an existing idea set without restarting unrestricted ideation.

Resolve the plugin root as the directory two levels above this `SKILL.md`. Read `references/facilitation-principles.md` and the relevant part of `references/evaluation-frameworks.md`.

## Companion-skill rule

Name `rad-council:convene` only when that exact skill is installed, appears in the current available-skill list, the decision is high-stakes, opposed expert views would add clear value, and the user accepts. Otherwise keep the evaluation here.

## Hard rule

The user scores, ranks, or rates first. Share your view after theirs, then discuss why the scores differ.

## 1. Confirm the idea set

List and number every candidate. Ask whether the set is complete. If the user still needs more options, route to `rad-brainstorm:brainstorm-session` before evaluation.

## 2. Select one framework

Recommend the smallest method that fits and let the user choose.

| Situation | Good method |
| --- | --- |
| Ten or more ideas | Impact and Effort |
| Three to five ideas with major unknowns | Assumption Mapping |
| Product ideas tied to an outcome | Opportunity Solution Tree |
| A high-risk choice | Pre-Mortem plus Assumption Mapping |
| Two or three finalists | Weighted Scoring |
| Unclear user need | Jobs-to-be-Done |

Define every criterion before scoring. Avoid false precision when totals are close.

## 3. Apply the method

Use one question at a time. Keep the user's scores separate from yours.

For each leading idea, capture:

- evidence-backed strengths;
- key trade-offs;
- riskiest assumption;
- cheapest useful test;
- failure or stop signal.

## 4. Challenge only when useful

For the top two or three ideas, offer a deeper challenge only when the stakes justify the time and the result could change the choice.

If accepted:

1. Use `references/subagent-prompts/idea-challenge.md`.
2. Spawn one bounded, read-only subagent when available, or run the same review directly.
3. Require JSON-first output and validate it with `scripts/validate-json.py` and `idea-challenge.schema.json`.
4. Re-prompt once on schema failure.
5. Use the critique to strengthen the decision. Do not let it add unrelated ideas.

## 5. Present the decision

Use this shape:

### Recommended: <idea>

- Why it leads
- Riskiest assumption
- Cheapest next proof
- Stop signal

### Strong alternative: <idea>

- Why it remains credible
- Main trade-off against the recommendation

### Parked or rejected

- Idea and one-line reason

Ask whether the ranking matches the user's judgment. The user makes the final choice.

For a chosen software idea, offer `rad-brainstorm:design-sprint`. Do not start implementation.
