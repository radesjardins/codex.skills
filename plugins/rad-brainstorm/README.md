# RAD Brainstorm

RAD Brainstorm helps you develop your own thinking before Codex adds ideas. It avoids the common failure where an AI gives a long list first and anchors the rest of the session.

The core rules are simple:

- Your ideas come first.
- Idea generation and evaluation stay separate.
- One question is asked at a time.
- Quick sessions stay quick.
- No code or project scaffolding happens during brainstorming.

## Install

```powershell
codex plugin add rad-brainstorm@radesjardins-codex-skills
```

## Skills

| Skill | Use it for |
| --- | --- |
| `rad-brainstorm:brainstorm-session` | A quick or full brainstorm on software, business, content, travel, creative work, or personal choices. |
| `rad-brainstorm:idea-evaluation` | Compare ideas you already have with a clear evaluation method. |
| `rad-brainstorm:five-whys` | Trace a repeated problem from its symptom to a root cause. |
| `rad-brainstorm:design-sprint` | Turn a chosen software approach into a reviewable design spec. |

Technique modes for `brainstorm-session` include SCAMPER, Six Thinking Hats, reverse brainstorming, How Might We, starbursting, and creative unblocking.

## Quick and full sessions

Quick is the default for a small or bounded topic. It uses one technique, aims for three strong options and one recommendation, uses no subagents, and normally finishes within five user turns.

Full is for an open, uncertain, or high-stakes topic. It can add current domain research, a challenge of the strongest ideas, and a fuller output review. Optional research or review work stays bounded.

## Output control

The user chooses whether the result stays in the conversation, goes to a personal folder, or becomes one dated file in the current project. Project files are marked as transient when another workflow will consume them. RAD Brainstorm never writes to `docs/design.md` and never commits its output.

## Companion skills

RAD Brainstorm works alone. It names an exact RAD Plan, RAD Repo, or RAD Council skill only when all of these conditions are true:

1. The exact skill is installed and appears in the current available-skill list.
2. Current evidence needs that workflow.
3. Using it would add clear value.

It never invokes a suggested companion until the user asks or accepts.

## Claude port notes

This Codex package preserves the four workflows from `rad-brainstormer` 4.0.0. Claude agent files were replaced with bounded Codex subagent prompts and JSON validation contracts. Claude manifests, empty skill folders, and Windows metadata are excluded.

## License

MIT. See [LICENSE](LICENSE).
