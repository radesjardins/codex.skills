# Deep Research: RAD Repo Plugin Evaluation

**Date:** 2026-08-06
**Scope:** Public `rad-repo` plugin in `radesjardins/codex.skills`
**Research depth:** Thorough
**Repository state reviewed:** Local public marketplace source at the time of this report

## Executive Summary

RAD Repo has a clear and useful purpose. It keeps repository instructions, current work state, decisions, lessons, and release checks in a small Git-native system. It does this without a database, background service, vector store, task tracker, or generated wiki.

Its best feature is the authority model. Each type of fact has one approved home. The plugin says which document wins, when a document can be created, who can write it, and when old material must move to the archive. Most memory tools focus on saving more context. RAD Repo focuses on keeping less context and making it trustworthy.

RAD Repo is strongest for one person or a small team that uses coding agents across many sessions. It is also a good fit for an existing repository with mixed or stale documents. The `adopt` and `repo-align` skills respect existing work and require confirmation before judgment-based changes.

The main weakness is that RAD Repo manages prose, state, and ship policy better than it manages the code itself. It has no symbol-aware repository map, code hotspot view, or complexity audit. Contract discovery has also failed in real use when normal validation commands could not be inferred from repository instructions. That failure can block shipping until a config file is added.

I recommend five near-term changes:

1. Add a `doctor` check that explains the contract, commands, resource paths, and trust decisions before another skill runs them.
2. Offer a lean `core` profile and the current `full` profile. Keep one code path and use a small config choice.
3. Make `adopt` and `repo-align` read by priority and by budget. They should not load every document into agent context by default.
4. Remove stale shim wording, remove the silent mirror-test pass, and stop first ship from starting an unrelated fit-out interview.
5. Add an explicit, read-only `complexity-audit` skill. It should rank a few maintenance hotspots by code churn, size, and existing quality signals. It must stay out of normal startup, wrapup, and ship.

The complexity audit is a good idea. Its value will come from priority and evidence. RAD Repo should use existing language tools when they are present and use a small Git-based scan as the common baseline. It should not invent a new universal complexity engine.

## Product Definition

RAD Repo is a repository control and continuity plugin. Its current package contains six user workflows:

- `startup` restores the active task from Git and the handoff.
- `wrapup` records a short, evidence-based resume point.
- `ship` reviews staged work, runs repository checks, commits, pushes, and records ship facts.
- `repo-init` creates the document contract for a new repository.
- `adopt` maps an existing repository into the model without flattening useful local structure.
- `repo-align` audits and repairs drift after explicit confirmation.

The document model has five levels:

| Level | Purpose | Main examples |
|---|---|---|
| L0 | Binding instructions | Root and scoped `AGENTS.md` files |
| L1 | Current session state | `docs/handoff.md` |
| L2 | Durable knowledge | Decisions and lessons |
| L3 | Product and execution truth | PRD, plan, design, active initiatives |
| L4 | Historical record | Archive |

The design also includes a closed shelf, lazy document creation, one writer per file, domain authority rules, vocabulary rules, and a small pre-ship gate. The implementation uses Python standard-library code and Git. This keeps installation simple.

## Key Findings

### 1. The authority model is the main advantage

The shelf answers a question that most agent-memory systems leave open: where does the final truth live?

RAD Repo assigns product truth to the PRD, execution truth to the plan, session truth to the handoff, settled choices to the decision log, and reusable rules to lessons. It also defines conflict order and write ownership. This reduces duplicate facts and prevents several agents from rewriting the same file for different reasons.

Cline's Memory Bank uses six required files and reads them at the start of every task. Roo's public Memory Bank uses a similar multi-file pattern. These systems can preserve useful context, but `activeContext.md`, `progress.md`, project briefs, technical context, and product context can repeat the same state in several places. RAD Repo's smaller L0 and L1 working set is easier to inspect and less likely to become a second documentation project. See the [Cline Memory Bank guide](https://docs.cline.bot/improving-your-prompting-skills/cline-memory-bank) and [Roo Code Memory Bank](https://github.com/GreatScottyMac/roo-code-memory-bank).

### 2. It treats handoff as repository evidence

The handoff workflow checks Git state, changed paths, validation, commit status, and push status. It does not rely on a chat summary alone. The short length cap also forces the writer to keep only the facts needed for the next session.

Small handoff skills often create a chat artifact or a long catch-all file. `armory` uses a larger handoff with a 200-line cap, while `claude-session-handoff` focuses on a seven-section transfer. RAD Repo has stronger repository integration and tighter document control. The two comparison projects are [Armory](https://github.com/Mathews-Tom/armory) and [Claude Session Handoff](https://github.com/thenguyenvn90/claude-session-handoff).

The 60-line limit can be too small for a long repair or a staged migration. RAD Repo should keep the short handoff and link to one active initiative or one resume packet when more evidence is required. The handoff should not grow into a project history.

### 3. The ship workflow has unusually good Git discipline

The ship skill uses reviewed paths, stages only approved work, inspects staged blobs, and fails closed when required checks are missing. It checks protected paths, common high-confidence secret forms, generated output, large files, contract changes, and repository validation.

This is stronger than a simple `commit and push` helper. It also prevents an agent from using a broad stage operation that includes unrelated user work.

The current scanner should describe its secret check as a high-confidence pattern check. It is not a full secret detector. RAD Repo should detect an existing tool such as [Gitleaks](https://github.com/gitleaks/gitleaks) and offer to run it. The plugin should not install or bundle that tool.

### 4. Brownfield adoption is careful and practical

The `adopt` skill maps current documents to roles before it proposes moves. It preserves useful local structure, asks for confirmation, and uses satellite documents for valid material that does not belong in the core shelf. This is much safer than creating a new file set and copying old content into it.

OpenSpec and Spec Kit are good at creating a structured change process. Their main path starts from a spec or change request. RAD Repo handles a different problem: ongoing care for repository state and policy. See [OpenSpec](https://github.com/Fission-AI/OpenSpec) and [GitHub Spec Kit](https://github.com/github/spec-kit).

### 5. Its context policy matches current platform direction

GitHub Copilot supports repository-wide instructions, path-specific instructions, and nearest-scope `AGENTS.md` files. OpenAI also describes `AGENTS.md` as the place for repository rules, business logic, quirks, and dependencies. RAD Repo's root-plus-scoped instruction model fits these platform conventions. See [GitHub repository instructions](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions?tool=webui&trk=public_post_comment-text), the [GitHub customization guide](https://docs.github.com/en/copilot/reference/customization-cheat-sheet), and [How OpenAI uses Codex](https://openai.com/business/guides-and-resources/how-openai-uses-codex/).

The plugin also applies progressive disclosure. Startup reads a small core set and loads deeper documents only when the task requires them. That is a sound design. Aider uses a compact repository map with a token budget and ranks symbols by relevance. Cline also advises users to provide the right context instead of more context. See the [Aider repository map](https://aider.chat/docs/repomap.html), [Aider FAQ](https://aider.chat/docs/faq.html), and [Cline file context guide](https://docs.cline.bot/core-workflows/working-with-files).

### 6. The instruction research is mixed, which supports RAD Repo's restraint

One 2026 study linked the presence of `AGENTS.md` files with 28.64 percent lower median runtime and 16.58 percent fewer output tokens across its sample. Another study found no measurable correctness gain from context files. A larger evaluation found that context files often increased cost and could reduce success, especially when generated files contained too many requirements. A later study found that refined guidance improved issue resolution when it helped agents reach the correct files.

These results do not support bigger instruction files. They support short, human-reviewed rules that point an agent to the right evidence. RAD Repo already follows that direction. It should measure and remove rules that cause work without preventing real failures. Sources: [AGENTS.md efficiency study](https://arxiv.org/abs/2601.20404), [Do Context Files Help Coding Agents?](https://arxiv.org/abs/2607.27250), [Evaluating AGENTS.md](https://arxiv.org/abs/2602.11988), and [Probe-and-Refine Tuning](https://arxiv.org/abs/2606.20512).

## Strengths and Weaknesses

### Strengths

| Strength | Why it matters |
|---|---|
| Clear source-of-truth rules | Agents and people can resolve document conflicts without guessing. |
| Small active context | Startup can restore work without loading a full project wiki. |
| Git-evidenced handoff | Resume state is tied to files, checks, commits, and push status. |
| Confirmation gates | Judgment-based moves, merges, and archives require owner approval. |
| One writer per file | Workflows have clear write boundaries and create fewer merge conflicts. |
| Reviewed staging | The ship flow protects unrelated local changes. |
| Path-scoped checks | The nearest repository instructions can define checks for each changed area. |
| Brownfield support | Existing repositories can keep useful local structure. |
| No service dependency | The plugin works with Git and Python. There is no account, server, or index to maintain. |
| Bounded documents | Length and retention rules resist slow growth. |
| Deferred-work rule | Rejected or postponed ideas do not return as active work without new evidence. |

### Weaknesses

| Weakness | Effect |
|---|---|
| Validation discovery is brittle | A normal repository can reach `validation_missing` even when its checks are documented. |
| No command trust preview | A skill can run commands found in repository instructions or config before the user sees the resolved command set. |
| Strict shelf can feel intrusive | Teams with ADRs, issue trackers, or feature-spec folders may think RAD Repo wants to replace them. |
| No code map | The plugin can find document drift but cannot find the symbols that matter to a task. |
| No code-health view | Complex, frequently changed code stays outside the plugin's view. |
| Full-document adoption reads | Large `docs/` trees can use too much agent context. |
| First ship can trigger fit-out | A release action can turn into an unrelated setup interview. |
| No profile choice | Small repositories get the same conceptual model as large ones. |
| Heuristic maintenance surface | Six document scanners and several parsing rules create long-term test work. |
| Weak version migration | Stamped repository instructions have no clear template version and upgrade check. |
| Misleading mirror test | The public package can report a pass when the private mirror does not exist and no comparison ran. |
| Stale shim wording | Some skill descriptions still mention cross-agent shims after the body stopped creating them. |

## Comparison With Similar Tools

| Tool or method | Main job | What it does better | Where RAD Repo is better |
|---|---|---|---|
| Cline or Roo Memory Bank | Persistent multi-file project memory | Familiar project context with broad coverage | Smaller active set, clearer authority, less repeated state |
| Spec Kit | Spec-driven feature delivery | Strong spec, plan, task, and implementation flow with wide agent support | Ongoing repository care, handoff, ship safety, brownfield document control |
| OpenSpec | Lightweight change artifacts | Good propose, apply, archive cycle and shared spec stores | Stronger session continuity and repository contract |
| BMAD Method | Adaptive planning with specialist agent roles | Rich guided delivery for complex products | Much smaller process and lower context cost |
| GSD Core | Discuss, plan, execute, verify, ship loop | Clear execution loop and fresh-context task work | Better document authority and staged repository safety |
| Agent OS | Project standards and spec shaping | Strong standards injection into feature work | Better lifecycle care after the feature plan exists |
| Task Master | PRD-to-task graph and complexity analysis | Task decomposition, dependencies, and selectable tool profiles | No task database and much less operating weight |
| Beads | Distributed issue graph and agent memory | Dependencies, concurrent task claims, sync, and compaction | Simpler setup and no tracker to maintain |
| Serena | Symbol-aware code access and editing | Semantic code retrieval across many languages | Repository policy, documents, handoff, and release checks |
| Aider | Compact task-relative code map | Ranked symbols with a strict token budget | Persistent repo policy and cross-session state |
| Entire CLI | Full agent-session capture linked to commits | Forensic replay and checkpoint history | Smaller records and fewer privacy or storage concerns |
| Superpowers | Coding discipline skills | TDD, debugging, review, worktrees, and evidence rules | Narrower repository-care purpose with less workflow pressure |
| gstack | Large suite of agent development commands | Wide command coverage, reviews, learning, and context recovery | Small surface and clearer limits |
| Repo hygiene skills | Broad health audits | Dependencies, CI, code quality, security, and baseline scores | Stronger durable contract and day-to-day continuity |

Reference projects: [BMAD Method](https://github.com/bmad-code-org/BMAD-METHOD), [GSD Core](https://github.com/open-gsd/gsd-core), [Agent OS](https://github.com/buildermethods/agent-os), [Task Master](https://github.com/eyaltoledano/claude-task-master), [Beads](https://github.com/gastownhall/beads), [Serena](https://github.com/oraios/serena), [Aider](https://github.com/Aider-AI/aider), [Entire CLI](https://github.com/entireio/cli), [Superpowers](https://github.com/obra/superpowers), and [gstack](https://github.com/garrytan/gstack).

## What RAD Repo Does Better

### It reduces memory instead of collecting it

Many systems save chats, tasks, specs, context files, issue graphs, embeddings, or code indexes. Those features can help a large team. They also create another system that needs cleanup.

RAD Repo has a better default for personal and small-team work. Keep binding rules, one current handoff, durable decisions, durable lessons, and the product documents that already matter. Archive the rest. This is the right answer to the user's goal of avoiding a complicated second brain.

### It joins human governance with agent action

The confirmation gates are a real product feature. The plugin separates deterministic facts from owner judgment. It can detect a duplicate or contradiction, but a person decides whether to merge, move, or archive it. That boundary is rare in agent workflow packages.

### It treats ship state as part of repository memory

Most context tools stop after planning or implementation. RAD Repo includes staged review, validation, commit, push, and optional deployment proof. The handoff can then record an exact delivery state. This closes the session loop.

### It can fit an existing repository without erasing local practice

The satellite rule is useful. It lets a team keep an ADR folder, API reference, runbook, or domain guide while the nearest core document links to it. RAD Repo should explain this feature early because it reduces the fear caused by the closed-shelf language.

## Where It Falls Short

### Contract discovery needs a first-class diagnostic

The ship gate can stop with `validation_missing` when repository checks exist but the parser cannot find them. This is a high-cost failure because it appears at the end of work.

Add a `doctor` command or skill with read-only output:

- Show each changed path.
- Show the nearest `AGENTS.md` file.
- Show the validation commands found for that scope.
- Show the config source and rule precedence.
- Show commands that need trust approval.
- Explain why any path has no validation.
- Check that every packaged skill can resolve its scripts and references.
- Check the installed plugin version against the stamped document-model version.

Run this during adoption and when the contract changes. Keep it available before ship.

### Repository commands need a trust gate

The pre-ship runner can execute shell commands read from repository instructions or `.rad-repo.json`. A repository is code from a trust point of view. A public or newly adopted repository could contain a harmful command.

On first use, show the resolved commands and require approval. Record a hash of the approved contract. Ask again only when the contract changes. This is small and has high safety value.

### The current model needs a smaller entry point

Task Master reports large token differences between its full, standard, and core tool sets. Aider also treats context as a budget. RAD Repo can use the same lesson without adding many modes.

Use one config field:

```json
{
  "profile": "core"
}
```

Suggested profiles:

| Profile | Includes |
|---|---|
| `core` | `AGENTS.md`, handoff, startup, wrapup, contract check, ship |
| `full` | Core plus PRD, plan, decisions, lessons, initiatives, vocabulary, alignment checks |

The files and scripts can stay shared. The profile controls which rules apply and which questions appear. This lowers first-use friction without creating a second product.

### Adoption and alignment need a context budget

The current adoption instructions can lead an agent to read a full documentation tree. A large repository can contain hundreds of Markdown files.

Use this order:

1. Inventory names, sizes, dates, and Git activity without loading bodies.
2. Read root instructions and likely authority files.
3. Read files tied to the current task or detected conflicts.
4. Process the remaining files in bounded batches.
5. Report the unread count and ask before a deep pass.

This keeps the audit honest. It also follows the same task-relative rule used by Aider and Cline.

### The public package has small quality defects

Fix these before adding a major feature:

- Remove cross-agent shim wording from `repo-init` and `adopt`.
- Change the mirror regression test to an explicit skip when the mirror is absent, or remove it from the public package.
- Move fit-out out of the first ship flow. Adoption or an explicit setup action is the correct place.
- State that the built-in secret scan finds a short set of high-confidence patterns.
- Add a template version to stamped instructions and a read-only upgrade report.
- Preserve a detailed existing handoff when it contains resume-critical facts. Replace it only when the new handoff carries equal or better evidence.

## Elements Worth Adopting

### From Aider and Cline: task-relative context budgets

Adopt bounded reads, clear token or file limits, and a report of what was left unread. Do not add a permanent code index as a required service.

### From Task Master: selectable surface size

Adopt one `core` and one `full` profile. Avoid a long list of profile variants.

### From CodeScene: hotspot priority

CodeScene treats a hotspot as code that deserves attention because it changes often and is large. It does not claim that every hotspot is bad code. This distinction is right for an agent report. See [CodeScene hotspots](https://docs.enterprise.codescene.io/versions/4.2.2/guides/technical/hotspots.html) and [CodeScene terminology](https://codescene.io/docs/terminology/codescene-terminology.html).

### From small maintainability skills: confidence and evidence

Several public maintainability skills rank findings and require file-and-line evidence. Adopt the evidence rule and a confidence field. Avoid a universal 1-to-10 repository score. Code Climate warns that a repository-wide maintainability rating can correlate with repository size, which can mislead users. See [Code Climate maintainability](https://docs.codeclimate.com/docs/maintainability).

### From existing code tools: adapters instead of reimplementation

SonarQube defines cyclomatic and cognitive complexity, duplication, size, and issue measures. Lizard provides multi-language complexity and size measures with a small command-line tool. Radon provides Python measures. Use these tools when a repository already has them or the user approves their use. See [SonarQube metrics](https://docs.sonarsource.com/sonarqube-server/user-guide/code-metrics/metrics-definition), [Lizard](https://github.com/terryyin/lizard), and [Radon](https://radon.readthedocs.io/en/stable/).

### From Entire and Cline checkpoints: optional forensic history

Some teams need full session recovery. Entire links agent sessions to commits, and Cline keeps shadow-Git checkpoints. RAD Repo should support a link or integration note when those tools are present. It should not store full transcripts by default. See [Entire CLI](https://github.com/entireio/cli) and [Cline checkpoints](https://docs.cline.bot/core-workflows/checkpoints).

## Elements to Avoid

Do not add these to the core plugin:

- A database, vector store, or knowledge graph.
- Full chat transcript capture.
- A task graph or issue tracker.
- Automatic project wiki generation.
- A background service or MCP server.
- A required semantic code index.
- Automatic installation of quality tools.
- A single repository health score.
- Complexity checks on every startup, wrapup, or ship.
- Automatic refactoring from an audit.
- More permanent status documents.

Beads, Graphiti, Serena, and Entire solve valid problems. Their storage, indexing, or tracking features would change RAD Repo into a different product. Graphiti is at [getzep/graphiti](https://github.com/getzep/graphiti).

## Proposed Complexity Audit

### Decision

Add it as a separate, explicit, read-only skill named `complexity-audit`.

Good trigger phrases include:

- "Audit code complexity."
- "Find hard-to-maintain code."
- "Where should this repository be simplified?"
- "Find technical debt hotspots."
- "Run a code health review."

The skill must not run during normal startup, wrapup, adoption, alignment, or ship. The user must ask for it.

### Product purpose

The audit should answer one question: which few code areas deserve human review now?

It should not try to prove that code is bad. A large stable parser can be fine. A small file changed every day can also be a risk. The report needs both relevance and quality evidence.

### Two-stage design

#### Stage 1: common Git hotspot scan

Use Git and Python standard-library code only.

- Read tracked source files.
- Respect ignored, generated, vendor, build, fixture, and lock-file rules.
- Measure file size.
- Measure recent change frequency and contributor count.
- Detect repeated edits to the same lines when practical.
- Rank the top 10 to 20 maintenance hotspots.
- Keep the time window configurable, such as the last 6 or 12 months.

This stage works in most repositories and adds no dependency.

#### Stage 2: existing quality signals

Detect tools and reports that the repository already uses:

- SonarQube or SonarCloud
- Code Climate or Qlty
- Lizard
- Radon
- ESLint complexity rules
- TypeScript or JavaScript duplicate-code tools
- Python lint reports
- Rust Clippy
- Go lint tools
- .NET analyzers
- test coverage reports

Show the proposed commands before first use. Ask before installing any tool.

### Ranking method

Use separate evidence columns instead of one magic score:

| Signal | Meaning |
|---|---|
| Churn | The file or symbol changes often. |
| Size | The code area is large enough to be hard to review. |
| Complexity | Existing tools report hard control flow or nesting. |
| Coupling | A change can affect many callers or dependencies. |
| Duplication | Similar logic exists in several places. |
| Test support | The area has strong, weak, or unknown test evidence. |
| Confidence | The finding is direct, inferred, or tool-dependent. |

The final rank can combine these signals, but the report must show the raw reasons. A hotspot needs code-quality review before it becomes a refactor recommendation.

### Output

Chat output should be the default. Write a repository document only when the user asks.

Each finding should contain:

1. File and symbol, when a symbol can be identified safely.
2. Evidence and time window.
3. Why this area matters now.
4. A small simplification idea.
5. Main change risk.
6. Tests or checks needed before a change.
7. Confidence level.

Limit the main list to 5 to 10 items. Put the full machine output in a temporary artifact or optional JSON file.

### Minimum useful version

The first version needs only:

- `skills/complexity-audit/SKILL.md`
- `scripts/code-hotspots.py`
- Git churn and file-size ranking
- Optional detection of existing code-quality reports
- JSON and human-readable output
- One focused regression test

Do not create custom parsers for many languages in the first version. Usage will show which adapters have real value.

### Why this can help RAD Repo stand out

Memory banks remember project facts. Spec systems shape work. Code indexers retrieve symbols. Quality tools produce metrics.

RAD Repo can connect these areas with a small workflow: restore the true repository state, identify the few risky code areas that change often, record an approved decision, plan the work, and ship with the repository's own checks. The differentiator is the connection and the restraint. The metric formulas are already common.

## Recommended Change Order

### P0: fix trust and first-use problems

1. Add contract and resource `doctor` output.
2. Add first-use approval for resolved repository commands.
3. Fix validation discovery and explain missing validation by path.
4. Remove stale shim text and the silent mirror-test pass.
5. Move fit-out out of first ship.

### P1: cut context and setup cost

1. Add `core` and `full` profiles.
2. Give adoption and alignment a read budget.
3. Add a document-model version and upgrade report.
4. Preserve complex handoff evidence through a linked active initiative or resume packet.

### P2: add the complexity audit

1. Ship the Git hotspot scan.
2. Parse existing quality reports when found.
3. Add baseline and delta output only after repeated use proves it is useful.

### P3: optional integrations

1. Detect Gitleaks for deeper secret scans.
2. Link to Serena or an existing repository map when symbol-aware context is needed.
3. Link to Entire or checkpoint tools when a team requires full session history.

## Suggested Public Positioning

> RAD Repo keeps coding-agent repositories clear between sessions. It uses a short instruction contract, one current handoff, durable decisions, and Git-based ship checks. It works with the repository you already have and needs no database, server, or generated knowledge base.

Short claim:

> Repository memory without the second-brain maintenance.

This claim is credible if the core profile stays small and the plugin does not absorb task tracking, session storage, code indexing, or broad quality tooling.

## Contrarian Views and Risks

### More guidance can reduce agent performance

The research does not show that more repository guidance always helps. Large or generated context files can increase cost and lead agents through extra work. RAD Repo must keep its rules short, tested, and tied to observed failures.

### Strict document control can create process work

A closed shelf is useful when a repository has document drift. It can feel excessive in a small library with a README and one design note. The core profile should be the normal answer for that repository.

### Complexity reports can create low-value refactors

Metric thresholds are easy to misuse. A high cyclomatic score can be acceptable in stable, tested code. The audit must rank areas for review and avoid automatic cleanup advice based on one number.

### Churn data can reflect healthy work

Frequently changed code can be a product center, a generated boundary, or an active migration. Churn is a relevance signal. Human review must decide whether it is a maintenance problem.

### Optional integrations can become hidden requirements

Tool detection is useful. The core result must still work when those tools are absent. Every optional tool should have a clear reason, command preview, and skip path.

## Owner Decisions

1. `core` is the routine default. A first `adopt` recommends one full pass. The user can choose core or full at any time.
2. Command approval stays in local Git settings. It does not enter repository files or commits.
3. The first complexity audit does not write a baseline. A later optional baseline will stay under `.git/rad-repo/` unless the user asks to share it.
4. Adoption supports small and medium projects through read budgets. Small means up to 50 candidate docs and 10,000 Markdown lines. Medium means up to 250 docs and 50,000 lines. Larger sets get an inventory and a narrowed first pass.
5. RAD Repo is Codex-only. Cross-agent shim wording will be removed.
6. Long recovery detail belongs in the active initiative. The handoff links to it and stays the short current snapshot.
7. Normal ship stops after push. Deploy checking requires an explicit `ship and verify deploy` request and uses one bounded read-only check.
8. Normal wrapup does not commit. `wrapup and commit` creates one local documentation commit. `wrapup and ship` uses ship.
9. RAD Repo names a RAD Plan skill only when that exact skill is available and current evidence shows a planning need. It invokes the skill only after the user asks or accepts the suggestion.

## Sources

### Primary platform and product sources

- [GitHub Copilot repository instructions](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions?tool=webui&trk=public_post_comment-text)
- [GitHub Copilot customization guide](https://docs.github.com/en/copilot/reference/customization-cheat-sheet)
- [OpenAI Codex AGENTS.md](https://github.com/openai/codex/blob/main/AGENTS.md)
- [How OpenAI uses Codex](https://openai.com/business/guides-and-resources/how-openai-uses-codex/)
- [GitHub Spec Kit](https://github.com/github/spec-kit)
- [OpenSpec](https://github.com/Fission-AI/OpenSpec)
- [BMAD Method](https://github.com/bmad-code-org/BMAD-METHOD)
- [GSD Core](https://github.com/open-gsd/gsd-core)
- [Agent OS](https://github.com/buildermethods/agent-os)
- [Task Master](https://github.com/eyaltoledano/claude-task-master)
- [Beads](https://github.com/gastownhall/beads)
- [Serena](https://github.com/oraios/serena)
- [Aider repository map](https://aider.chat/docs/repomap.html)
- [Aider FAQ](https://aider.chat/docs/faq.html)
- [Entire CLI](https://github.com/entireio/cli)
- [Superpowers](https://github.com/obra/superpowers)
- [gstack](https://github.com/garrytan/gstack)
- [Cline Memory Bank](https://docs.cline.bot/improving-your-prompting-skills/cline-memory-bank)
- [Cline file context](https://docs.cline.bot/core-workflows/working-with-files)
- [Cline checkpoints](https://docs.cline.bot/core-workflows/checkpoints)
- [Roo Code Memory Bank](https://github.com/GreatScottyMac/roo-code-memory-bank)
- [Anthropic memory tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool?s=15)

### Code quality sources

- [CodeScene hotspots](https://docs.enterprise.codescene.io/versions/4.2.2/guides/technical/hotspots.html)
- [CodeScene terminology](https://codescene.io/docs/terminology/codescene-terminology.html)
- [SonarQube metric definitions](https://docs.sonarsource.com/sonarqube-server/user-guide/code-metrics/metrics-definition)
- [Code Climate maintainability](https://docs.codeclimate.com/docs/maintainability)
- [Lizard](https://github.com/terryyin/lizard)
- [Radon](https://radon.readthedocs.io/en/stable/)
- [Gitleaks](https://github.com/gitleaks/gitleaks)

### Research papers

- [On the Impact of AGENTS.md Files on the Efficiency of AI Coding Agents](https://arxiv.org/abs/2601.20404)
- [Do Context Files Help Coding Agents?](https://arxiv.org/abs/2607.27250)
- [Evaluating AGENTS.md](https://arxiv.org/abs/2602.11988)
- [Probe-and-Refine Tuning of Repository Guidance](https://arxiv.org/abs/2606.20512)

## Rerun Inputs

```yaml
workflow: firecrawl-deep-research
topic: Deep evaluation of the public RAD Repo plugin against repository memory, specification, agent workflow, handoff, ship, code context, and code quality tools
depth: thorough
output: markdown
date: 2026-08-06
```
