# Ryan's Codex Skills

A public marketplace of Codex workflow plugins by Ryan DesJardins.

The plugins add written procedures, templates, and small local checks. They help Codex handle work in a repeatable way. Installing this marketplace does not add a hosted service, database, account system, or background worker.

The current catalog has 5 plugins and 25 skills. All packages use the MIT License.

## Choose a plugin

| Plugin | Version | Best fit | What it adds |
| --- | ---: | --- | --- |
| [RAD Plugin Converter](plugins/rad-plugin-converter/) | 1.0.0 | Authors auditing or converting Claude Code, Codex, mixed, or older plugin packages | A read-only standards audit and a deterministic converter for the Agent Plugins 1.0.0 Working Draft |
| [RAD Brainstorm](plugins/rad-brainstorm/) | 4.1.0 | One person who wants guided idea work before planning | User-first ideation, separate evaluation, idea-source labels, and a small proof step |
| [RAD Plan](plugins/rad-plan/) | 7.1.0 | Solo builders and small teams planning one bounded release | Repository-backed planning, rescue, replan, plan review, and a mechanical plan check |
| [RAD Repo](plugins/rad-repo/) | 3.1.0 | Repositories used across many coding-agent sessions | A small document model, handoffs, local command trust, shipping checks, and an optional code-hotspot review |
| [RAD PARA](plugins/rad-para/) | 1.1.1 | People who keep notes and projects in a PARA system | PARA setup and review guidance, layered summaries, note-to-output help, handoffs, and a narrow folder scanner |

## What is familiar and what is specific

These plugins use known practices. They do not claim to invent PARA, Five Whys, SCAMPER, implementation plans, handoff notes, or pre-ship checks.

Their value comes from how those practices are joined and limited:

- RAD Plugin Converter uses a standard migration inventory and validation process. It adds the portable root manifest while retaining supported client files, and it checks skill and MCP configuration before writing changes.
- RAD Brainstorm uses familiar idea methods. Its specific focus is idea ownership: the user starts, each contribution has a source label, judgment happens later, and the result ends with a test threshold and stop signal.
- RAD Plan resembles other planning assistants and spec templates. It adds bounded repository reading, one maintained plan, outcome coverage, safe recovery fields, rescue and replan paths, plus separate mechanical and judgment checks.
- RAD Repo uses common repository instructions, handoffs, and Git checks. Its main difference is a small authority model and clone-local approval for repository validation commands.
- RAD PARA applies established second-brain methods. It puts setup, review, distillation, output assembly, and session continuity in one plugin, with approval required before a real folder reorganization.

## Important limits

Skills are instructions for an AI agent. They can improve consistency, but they cannot guarantee a correct plan, diagnosis, design, file placement, or release.

The bundled scanners use rules and heuristics. Their findings are evidence to review. They are not proof of code quality, document meaning, or personal productivity.

Some workflows can edit files. RAD Repo can commit and push when the user invokes its ship workflow. RAD PARA can move files after a full move plan receives approval. Each plugin README states its write boundary.

The local Python scripts have no required third-party packages. The JSON validators can use the optional jsonschema package when it is already installed.

## Add the marketplace

Use a Codex CLI build that provides the plugin commands:

~~~powershell
codex plugin marketplace add radesjardins/codex.skills
~~~

The marketplace name is radesjardins-codex-skills.

## Install plugins

Install only the plugins you want:

~~~powershell
codex plugin add rad-plugin-converter@radesjardins-codex-skills
codex plugin add rad-brainstorm@radesjardins-codex-skills
codex plugin add rad-plan@radesjardins-codex-skills
codex plugin add rad-repo@radesjardins-codex-skills
codex plugin add rad-para@radesjardins-codex-skills
~~~

The plugins do not require each other. RAD Brainstorm, RAD Plan, and RAD Repo mention a companion only when its exact skill is available and the current work needs it. RAD PARA can share a handoff with RAD Repo when both apply.

## Example requests

- "Audit this Codex plugin for Agent Plugins 1.0.0, then convert it in place."
- "Run a quick brainstorm and let me give my ideas first."
- "Create a full implementation plan from this repository."
- "Run RAD Repo startup and show the next task."
- "Audit this PARA folder without changing anything."

The plugin pages list every skill, its output, and its limits.

## Source and contributions

Everything that installs is visible under [plugins](plugins/). Issues and pull requests should include the plugin name, the request that triggered the problem, what happened, and what the user expected.

## License

MIT. See [LICENSE](LICENSE).
