# Bounded Context Rules

Plans should let a fresh coding agent start one milestone without loading the full project history.

## Plan rules

- Aim for two or three tasks per milestone.
- Warn when a milestone exceeds five tasks.
- Warn when a plan exceeds 20 live tasks.
- Keep each task within one bounded work session when practical.
- Put the outcome, paths, dependencies, proof, and recovery need in the task block.
- Keep completed work in `## Shipped` outside the live Tasks section.

## Milestone checkpoint

Each milestone checkpoint names:

- the tasks and owner checks that form the gate;
- the focused proof that the milestone works;
- the safe recovery strategy;
- the next milestone or owner decision.

The plan does not commit, clear a task, or start a new task. The execution workflow follows repository rules for commits and task boundaries.

## Fresh-context handoff

When the runtime or owner starts a fresh task, load:

1. repository instructions;
2. the plan objective, release map, and Outcome coverage;
3. the current milestone and its live tasks;
4. the relevant code and tests;
5. the latest verified handoff when one exists.

Do not load every shipped task or every repository document by default.

## Review questions

- Can a fresh agent explain what the current milestone ships?
- Are the relevant paths and proof inside each task?
- Can the milestone finish in one bounded run?
- Does the checkpoint state what happens next?
- Is context limited to current work and its direct evidence?
