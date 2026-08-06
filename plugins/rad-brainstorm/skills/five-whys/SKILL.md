---
name: five-whys
description: Use when the user wants a user-led root-cause interview for a repeated problem, failure, delay, defect, or other observed symptom. Do not use for open ideation, option ranking, or evidence-led code diagnosis.
---

# Five Whys

Use Five Whys as a small problem-framing tool. Ask one question at a time. The user supplies causal answers.

## Process

1. Restate the observed symptom, timing, and effect in concrete terms.
2. Ask why it happened.
3. Use the answer as the subject of the next why question.
4. Mark each answer as direct evidence, user belief, or inference.
5. Stop when the chain reaches an actionable system, process, policy, resource, or design cause.

Five is a guide. Stop sooner when the cause is clear. Continue when the answer still describes a symptom.

When more than one cause is credible, list the branches. Ask which branch has the greatest effect or strongest evidence. Explore that branch first. Return to another branch only when it could change the conclusion.

## Guardrails

- Look for system causes and avoid personal blame.
- Keep multiple causes when evidence supports them.
- Stop when another why would repeat the same fact.
- State uncertainty when evidence is missing.
- Wait for the user to confirm the likely cause before discussing solutions.
- Do not edit files, start implementation, or commit output.

## Close

Present the symptom, causal chain, likely root cause, untested branches, and evidence that would support or disprove the result. Ask whether the user agrees. After agreement, offer `rad-brainstorm:brainstorm-session` for solutions.
