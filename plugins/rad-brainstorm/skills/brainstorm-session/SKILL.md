---
name: brainstorm-session
description: Use when the user explicitly wants to brainstorm, generate or expand ideas, explore alternatives, use SCAMPER or another named creative method, or work from a blank or vague starting point. Do not use for a request that only needs a direct answer, root-cause analysis, idea ranking, or implementation planning.
---

# Brainstorm Session

Help the user develop ideas without anchoring them on an AI list.

Do not write code, scaffold a project, invoke an implementation workflow, or start implementation. Finish the thinking process and get the user's approval first.

Resolve the plugin root as the directory two levels above this `SKILL.md`. Read `references/facilitation-principles.md` before facilitating. Read only the other references needed for the chosen method.

## Companion-skill rule

Name an exact RAD Plan, RAD Repo, or RAD Council skill only when:

1. The exact skill is installed and appears in the current available-skill list.
2. Current evidence needs that workflow.
3. It would add clear value.

Never invoke a suggested companion until the user asks or accepts. The public namespaces are `rad-plan:*`, `rad-repo:*`, and `rad-council:*`.

## 1. Confirm what the user wants

Some prompts such as "help me think through this" may ask for a direct answer. When intent is unclear, ask one short question: "Do you want a quick take or a brainstorm session?"

Continue with this workflow only when the user wants a brainstorm.

## 2. Select the tier

Use quick for a small, bounded topic or when the user asks for speed. State that choice and offer full.

Quick tier:

- Ask for the user's starting thoughts.
- Use one suitable technique.
- Produce three strong options and one recommendation.
- Use no subagents.
- Create no file unless asked.
- Aim to finish within five user turns.

Use full for an open, uncertain, or high-stakes topic. Full follows the complete flow below.

## 3. Select the working mode

When it is unclear who should generate, ask: "Do you want to generate while I guide, generate together, or react to ideas I generate?"

- Facilitator is the default. The user generates first.
- Partner means both contribute after the user shares initial thinking.
- Generator uses the quick flow and lets the user react.

## 4. Detect the starting state

Choose one:

- Blank slate
- Vague idea
- Clear idea that needs alternatives
- Existing idea that needs improvement
- Existing ideas that need evaluation

If the user already has a complete idea set and wants to choose, route to `rad-brainstorm:idea-evaluation`.

If the request covers several independent systems, help split it and brainstorm one part first.

For software topics, read relevant repository docs, related code, and recent Git history before proposing designs. Keep this read-only.

## 5. Run the anti-anchoring check

Before offering ideas, ask the user what they have already considered. Ask one question at a time.

Cover only what is needed:

1. Existing thoughts, including half-formed ones.
2. The direction that feels appealing.
3. Anything already ruled out and why.

Capture the user's ideas before adding yours. Build from their language and constraints.

If the user has no ideas, use the progressive engagement ladder in `references/creative-unblocking.md`. Start with the situation or frustration. Do not answer a blank page with a long idea list.

## 6. Add research only when it helps

Current research is useful when the topic depends on a market, regulation, recent technology, or unfamiliar domain. Do not offer it as an opening menu item.

When the conversation reaches a question that research could answer, explain the exact value and ask permission. If accepted:

1. Use `references/subagent-prompts/domain-research.md` with the topic and session context.
2. When subagents are available, spawn one bounded, read-only research subagent. It may search the web and read supplied files. It must not edit files.
3. When subagents are unavailable, do the same bounded research directly.
4. Require JSON-first output and validate it with `scripts/validate-json.py` and `domain-research.schema.json`.
5. Re-prompt once if validation fails. If it still fails, use the reliable parts only and state the limit.
6. Cite current sources and weave two or three useful findings into the questions. Do not dump the research brief into the session.

## 7. Generate without evaluating

Announce that idea generation has started. Keep judgment out of this phase.

Use a named method when the user asks for one. Otherwise select from `references/methodology-catalog.md`:

| Starting state | Good first sequence |
| --- | --- |
| Blank slate | Creative unblock, starbursting, How Might We |
| Vague idea | Clarify, SCAMPER, reverse brainstorming |
| Clear idea | Six Thinking Hats, morphological analysis |
| Improving existing | SCAMPER, Five Whys, TRIZ when technical |
| Stuck | Worst Possible Idea, random entry, Crazy 8s |

Named modes include `scamper`, `six-hats`, `reverse`, `hmw`, `starburst`, and `unblock`.

Keep a running idea list. When ideas repeat or become minor variations, ask to switch to evaluation.

## 8. Evaluate in a separate phase

Announce the switch. Read `references/evaluation-frameworks.md` and choose the smallest useful method.

The user scores or ranks first. Then share your view and discuss differences. Narrow to two or three candidates.

For a high-stakes choice, offer one focused idea challenge only when it would change the decision. If accepted:

1. Use `references/subagent-prompts/idea-challenge.md`.
2. Spawn one bounded, read-only subagent when available, or run the same review directly.
3. Validate the JSON with `idea-challenge.schema.json`.
4. Use the findings to strengthen the candidates. Do not let the challenge restart unrestricted ideation.

## 9. Present the result

Present two or three approaches with trade-offs and a recommendation. Scale the result to the domain.

For software, cover architecture, components, data flow, error handling, and testing only after the user selects an approach. If the chosen approach needs more technical work than the session can settle, offer `rad-brainstorm:design-sprint`.

When a full software session produces a complete spec, review it here before delivery:

1. Scan for placeholders, contradictions, scope growth, ambiguity, missing recovery behavior, and unneeded complexity.
2. Fix confirmed issues.
3. When subagents are available, run one bounded, read-only review with `references/subagent-prompts/spec-review.md`.
4. Validate the JSON with `scripts/validate-json.py` and `spec-review.schema.json`.
5. Explain and address blocking findings. Run another subagent review only when the user asks.

Every delivered result includes:

- the chosen direction;
- the strongest alternative;
- considered and rejected ideas with one-line reasons;
- assumptions that still need proof;
- the next useful decision or action.

Do not use placeholders such as TBD or TODO. State a clear deferral and reason when a point cannot be settled.

## 10. Ask where the output goes

Offer these choices:

1. Keep it in the conversation.
2. Save one dated Markdown file in a personal folder chosen by the user.
3. Save one dated Markdown file under the current project's `docs/` folder when the topic is that project.

For project output, suggest `docs/YYYY-MM-DD-<topic>-spec.md`. Mark it as transient when a later planning workflow will consume it. Never write to `docs/design.md`.

If `docs/ideas.md` already exists, offer to append rejected or parked ideas. Do so only after the user accepts. Do not create that shelf file.

Never commit the output.

## 11. Close the session

Ask whether the result meets the user's need. Get clear approval before suggesting a next workflow.

For software sequencing, name `rad-plan:plan` only under the companion-skill rule. When it is absent or unhelpful, say that implementation planning is the next general step without naming a plugin.
