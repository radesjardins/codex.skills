# Session Output

Use one stable result shape. Scale the detail to the session.

## Result contract

```markdown
# <Topic>

## Frame
- Goal:
- Primary user:
- Success:
- Hard constraint:

## Ideas considered
- I1 [user]:
- I2 [AI]:
- I3 [research]:

## Mechanism groups
- <mechanism>: <idea IDs>
- Missing or weak mechanism:

## Decision
- Recommended direction:
- Strong alternative:
- Parked or rejected:

## Proof
- Riskiest assumption:
- Cheapest proof:
- Pass threshold:
- Stop signal:

## Open point
- Next useful decision or action:
```

Omit an idea source type when it did not contribute. Preserve original idea IDs when ideas are clustered.

## Optional checkpoint

Offer one checkpoint only during a full session that may be interrupted. Get approval and a destination before writing it. Quick sessions remain file-free.

```markdown
# RAD Brainstorm Checkpoint
- Topic:
- Session tier: full
- Working mode:
- Session phase:
- Frame:
- Ideas with idea source labels:
- Mechanism groups:
- Decisions made:
- Open questions:
- Next question:
- User approval status:
```

Resume from the recorded phase and next question. Confirm the checkpoint with the user before continuing.

## Example 1

Quick personal choice:

```markdown
Recommended direction: Try the two-week class [user].
Strong alternative: Use a self-guided course [AI].
Riskiest assumption: The class schedule is sustainable.
Cheapest proof: Attend the first two sessions.
Pass threshold: Both sessions fit without missed obligations.
Stop signal: Either session creates a conflict that cannot move.
```

## Example 2

Product idea evaluation:

```markdown
Mechanism groups: reminders [I1, I4], progress visibility [I2], social support [I3].
Recommended direction: I2 [user], because it tests value with the least build work.
Strong alternative: I3 [AI], if interviews show accountability is the main need.
Pass threshold: Four of six users return without a reminder in week two.
Stop signal: Fewer than two users return.
```

## Example 3

Full software session:

```markdown
Recommended direction: Add a read-only preview before import [user + research].
Strong alternative: Import into a temporary workspace [AI].
Riskiest assumption: Users can detect bad mappings in the preview.
Cheapest proof: Test a clickable preview with five target users.
Pass threshold: Four users find the seeded mapping error.
Stop signal: Two or more approve the bad mapping.
Next action: Use software-design to settle preview data and error recovery.
```

## Visual summary

Offer a Mermaid flow or mind map only when it makes three or more relationships easier to understand. Keep the text result as the source of truth. Do not add a visual when the result is already clear as a short list.
