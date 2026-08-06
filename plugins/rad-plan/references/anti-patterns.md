# Planning Risk Checks

Use these eight checks during risk review. They concern plan quality. Code-review and style concerns belong to later workflows.

## 1. Unclear outcome

The plan cannot state what the user can do or what observable result changes.

**Fix:** Rewrite the outcome and final proof before task decomposition.

## 2. Missing owner decision

The plan chooses product behavior, risk acceptance, cost, or an irreversible action that the owner has not approved.

**Fix:** Ask one clear question and record the answer or mark the item unknown.

## 3. Unbounded investigation

A task says to explore, research, audit, or inspect without paths, questions, evidence limits, or a stop rule.

**Fix:** Set the target, file or source budget, required output, and stop condition.

## 4. Unjustified new system

The plan adds a service, framework, database, dependency, or abstraction without naming the approved requirement that needs it.

**Fix:** Use the current stack or record the requirement and score the smallest plausible choices.

## 5. Unsafe state change

A migration, deployment, delete, payment, auth, or external action lacks a safe recovery path or owner gate.

**Fix:** Add a focused check, safe rollback strategy, backup or prior artifact, and stop condition.

## 6. Weak proof

Done when or Validate can pass while the user outcome is still broken.

**Fix:** Use an observable result and a focused positive, negative, or recovery check as risk requires.

## 7. Work unit too large

A task cannot fit one bounded work session, a milestone has more than five tasks without reason, or the live plan has more than 20 tasks.

**Fix:** Split by a shippable outcome or reduce the current release.

## 8. Authority conflict

The plan contradicts an approved PRD, architecture choice, repository instruction, or current code fact without surfacing the conflict.

**Fix:** Resolve the conflict with the owner or record a durable follow-up before approval.

## Mechanical and judgment boundary

`plan-lint.py` checks section shape, task fields, IDs, dependencies, outcome links, duplicate sections, path labels for 7.1 plans, vague phrases, and unsafe rollback command forms.

The risk assessor judges outcome quality, owner decisions, investigation bounds, new-system need, rollback meaning, task size, tests, and authority conflicts.

An issue must cite the exact plan text, state the effect, and give the smallest useful fix.
