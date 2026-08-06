---
name: five-whys
description: Use when the user wants root-cause analysis for a repeated problem, failure, delay, defect, or other symptom. Do not use for open-ended ideation, option ranking, or a request to diagnose code from evidence without a user-led causal interview.
---

# Five Whys

Help the user trace a stated symptom to an actionable root cause. The user supplies the causal answers. Ask one question at a time and do not suggest the answer.

## Process

1. Restate the observed problem in concrete terms.
2. Ask why it happened.
3. Use the user's answer as the subject of the next why question.
4. Continue until the chain reaches an actionable system, process, policy, resource, or design cause.

Five is a guide. Stop at three when the root cause is clear. Continue past five when the chain is still at a symptom.

When the chain branches, list the branches and ask which one has the greatest effect. Explore that branch first. Return to another branch only when it could change the conclusion.

## Guardrails

- Separate direct evidence, user belief, and inference.
- Avoid blame. Look for system causes.
- Do not force one simple cause onto a multi-cause problem.
- Stop when another why would only repeat the same fact.
- Do not propose solutions before the user confirms the root cause.
- Do not edit files or start implementation.

## Close

Present:

- the original symptom;
- the causal chain;
- the likely root cause;
- important branches that were not explored;
- evidence that would confirm or disprove the conclusion.

Ask whether the user agrees with the root cause. If yes, offer to brainstorm solutions with `rad-brainstorm:brainstorm-session` and select a method from `references/methodology-catalog.md`.
