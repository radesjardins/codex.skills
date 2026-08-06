# Focused Test and Validation Rules

The plan uses six task fields. Test detail belongs in **Validate**. Do not add a seventh Test Strategy field.

## Default rule

Use the smallest check that proves the changed behavior. Name the command, test file, or observable condition. Run wider checks only when the repository contract requires them or the change crosses shared boundaries.

For new behavior or a bug fix:

1. Name the focused test that must fail before the change when practical.
2. Name the focused command that must pass after the change.
3. Include the main negative or error case when it can cause user harm or silent failure.
4. Preserve existing test intent. A task must not weaken an assertion only to make a check pass.

Documentation and simple configuration tasks can use a static check or exact review condition. They do not need invented unit tests.

## Higher-risk changes

Validate must name positive, negative, and recovery checks when a task changes:

- authentication or authorization;
- payments;
- personal or regulated data;
- database schemas or destructive data operations;
- external integrations;
- core business rules;
- concurrency or retry behavior.

For these tasks, state which boundaries use real services, disposable services, fixtures, or mocks.

## Coverage

Do not set a universal coverage percentage. Use the repository's approved threshold when one exists. Otherwise require tests for the changed behavior and important failure cases.

## Review questions

- Does the check fail when the planned behavior is absent or broken?
- Does it cover the task's main error case?
- Is the command scoped to the changed behavior?
- Does a broader check have a clear contract reason?
- Can a fresh agent run the check without guessing?
