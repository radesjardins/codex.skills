# Deep Research: RAD Brainstorm Plugin Evaluation

**Date:** 2026-08-06
**Scope:** Public `rad-brainstorm` plugin in `radesjardins/codex.skills`
**Research depth:** Thorough
**Repository state reviewed:** Local public marketplace source at the time of this report

## Executive Summary

RAD Brainstorm has a strong product idea. It protects the user's own thinking before Codex offers answers. It keeps idea generation apart from judgment. It then turns the strongest ideas into assumptions, cheap tests, and stop signals. This makes it more useful than a prompt that returns twenty ideas and ends.

The best user is a solo builder, creator, or owner who wants a skilled thinking partner inside Codex. The user wants more structure than normal chat, and less process than BMAD, Arc, Miro, or a full product discovery system. The plugin also works outside software, which gives it a wider use case than Superpowers and Arc.

Its strongest features are:

1. The user contributes first, which protects idea ownership and can reduce early AI anchoring.
2. Quick and full tiers set a visible cost limit.
3. Generation and evaluation have separate rules.
4. The user scores first during evaluation.
5. Optional research has consent, source, scope, and JSON checks.
6. Each leading idea gets a risky assumption, a cheap proof, and a stop signal.
7. The plugin never starts implementation or commits an output.

Recent research supports the human-led design. A 2026 controlled study found that reflective, human-led AI help improved idea quality while keeping more diversity and ownership than model-led rewriting. A 2025 experiment found that early AI ideas raised creativity and anchoring at the same time, while later AI ideas caused a wider change in direction. These findings fit the plugin's user-first rule. See [Maier, Schneider, and Feuerriegel](https://arxiv.org/abs/2510.23324) and [Fan and others](https://www.ijcai.org/proceedings/2025/1142).

The plugin overstates this evidence in its references. Research does not show that AI suggestions always reduce creativity. Several studies found that AI increased individual creativity or idea breadth. Other studies found greater fixation or lower group-level diversity. The safe claim is: **early AI ideas can anchor the session, so RAD Brainstorm starts with the user's thinking and adds AI ideas later.**

The main weakness is internal weight. The package has 21 files, 3,737 lines, and about 25,164 words. Its reference set repeats methods and rules. A quick session can need the main skill, a 2,587-word facilitation guide, and part of a 6,446-word method catalog. One 2,498-word research guide is not called by any skill. The package is light in software needs and heavy in reading cost.

Two scope issues also need attention:

- `design-sprint` writes a software design spec. The established Design Sprint method maps a problem, sketches, decides, prototypes, and tests with users. Rename this skill to `software-design` or `design-spec`.
- `five-whys` is root-cause analysis. It has good guardrails, yet it sits outside the main ideation job. Keep it as a small problem-framing tool and remove its duplicate catalog entry.

I recommend a focused 4.1 release:

1. Keep the user-first rule and narrow its research claim.
2. Add a short goal, audience, success, and hard-constraint intake before idea generation.
3. Track idea origin as user, AI, or research.
4. Add one diversity check based on different underlying mechanisms.
5. Cluster large idea sets before scoring, while preserving the original ideas.
6. Add one small, stable result template.
7. Rename `design-sprint` to `software-design`.
8. Remove the unused research guide and repeated method text.
9. Correct unsupported or wrong source claims.
10. Add an optional visual summary only when a current visual tool is available and useful.

RAD Brainstorm should avoid a large method contest, mandatory files, a local browser server, group voting software, AI creativity scores, or a multi-agent panel by default. Its best position is a lean, evidence-aware thinking partner that protects user ownership and ends with a decision that can be tested.

## Research Method and Limits

This review used five evidence groups:

- The complete public RAD Brainstorm package, including all four skills, references, scripts, schemas, tests, README, and plugin metadata.
- The prior RAD Plan evaluation format in this repository.
- Current source files and official documents for Superpowers, Arc, and BMAD.
- Current official product documents for Miro, FigJam, Whimsical, and Mural.
- Primary research and official method sources about brainstorming, human-AI ideation, root-cause analysis, assumption tests, and Design Sprints.

The local package has 21 files, 172,083 bytes, 3,737 lines, and about 25,164 words. The five large reference files contain about 19,431 words. These counts describe package weight. Codex reads reference files as needed, so all content does not enter every session.

The Firecrawl command and API key were unavailable in this session. Live web search was the allowed fallback. I did not install or run the compared products. Product findings come from current official documents, source files, and selected research. This is a design and source review. It is not a controlled user test.

## Product Definition

RAD Brainstorm 4.0.0 contains four user workflows:

| Skill | Main job | Current result |
|---|---|---|
| `brainstorm-session` | Generate and narrow ideas in a quick or full session | Two or three approaches, a recommendation, rejected ideas, assumptions, and a next action |
| `idea-evaluation` | Compare an existing idea set | A recommendation, strong alternative, risky assumption, cheap proof, and stop signal |
| `five-whys` | Run a user-led root-cause interview | A causal chain, likely cause, untested branches, and needed evidence |
| `design-sprint` | Turn one chosen software approach into a design spec | A dated software spec, with review and user approval |

The main session has three working modes:

- Facilitator: the user generates first and the agent guides.
- Partner: both add ideas after the user's initial thinking.
- Generator: the agent proposes ideas and the user reacts.

Quick is the default for small topics. It uses one method, no subagents, three strong options, one recommendation, no file unless asked, and a target of five user turns.

Full is for open, uncertain, or high-stakes work. It can add current research, one idea challenge, a fuller result, and a software spec review.

The current public promise is mostly accurate. A clearer short promise is:

> RAD Brainstorm helps you form, expand, and test your own ideas before Codex plans or builds anything.

## Key Findings

### 1. Human ownership is the strongest feature

Most AI ideation tools lead with generated content. Whimsical adds five AI nodes from a selected mind-map node. Miro can generate ideas from a prompt or selected board objects. These actions are fast, but the first model output can shape the rest of the session. See [Whimsical AI mind maps](https://whimsical.com/learn/get-started/ai-mind-maps) and [Miro AI](https://help.miro.com/hc/en-us/articles/28765406244498-Miro-AI-overview).

RAD Brainstorm asks what the user has already considered, what direction feels appealing, and what has been ruled out. This protects the owner's language and judgment before model suggestions arrive.

The 2026 human-led study gives this rule direct support. Reflective question and suggestion modes improved idea quality while keeping more idea diversity and perceived ownership than a model-led rewrite. The result was repeated in a second experiment. See [Partnering with Generative AI](https://arxiv.org/abs/2510.23324).

This is a useful public difference. State it as an ownership and timing choice. Avoid a universal scientific claim.

### 2. The research evidence is mixed, and the plugin says it is settled

The facilitation guide says research “consistently” shows that AI suggestions cause fixation and lead to fewer, less varied, and less original ideas. That sentence is too broad.

Evidence that supports caution includes:

- A CHI 2024 visual design study found more fixation, fewer ideas, lower variety, and lower originality with AI-generated image support. See [The Effects of Generative AI on Design Fixation and Divergent Thinking](https://arxiv.org/abs/2403.11164).
- A 2025 Nature response found that ChatGPT improved the average idea while reducing the diversity of the idea pool. See [ChatGPT decreases idea diversity in brainstorming](https://www.nature.com/articles/s41562-025-02173-x).
- A Science Advances study found higher individual story quality and greater similarity across AI-assisted stories. See [Generative AI enhances individual creativity but reduces collective diversity](https://doi.org/10.1126/sciadv.adn5290).

Evidence that supports AI help includes:

- Five experiments found higher creativity with ChatGPT than with no tool or a web search, with the largest gain in incremental ideas. See [An empirical investigation of the impact of ChatGPT on creativity](https://www.nature.com/articles/s41562-024-01953-1).
- Two design experiments found large creativity gains during ideation. The effect changed during implementation and depended on expertise. See [The Double-Edged Roles of Generative AI in the Creative Process](https://pubsonline.informs.org/doi/10.1287/isre.2024.0937).
- The timing study found that early AI input could raise creativity while also raising anchoring. Later AI input caused more change in direction. See [Creative Momentum Transfer](https://www.ijcai.org/proceedings/2025/1142).

The plugin's sequence remains sound. The source claim needs more care:

> AI can improve idea quality and can also narrow ownership or diversity. RAD Brainstorm starts with the user's ideas, then adds AI help at a deliberate point.

### 3. Generation and evaluation are separated well

IDEO asks teams to delay judgment, seek many ideas, and build on other ideas during generation. RAD Brainstorm follows the same phase rule, then announces the switch to evaluation. See [IDEO Brainstorm Rules](https://www.designkit.org/methods/brainstorm-rules.html).

The plugin improves this for one person working with an AI:

- It draws out the user's ideas first.
- It stops judgment during generation.
- It asks the user to score first during evaluation.
- It narrows to two or three candidates.
- It ends with an assumption and a cheap proof.

Many prompt collections mix generation, praise, critique, ranking, and implementation in one answer. RAD's phase rule gives the session a clear mental change and helps prevent the first polished idea from winning by default.

### 4. The evaluation close is better than most competing skills

The `idea-evaluation` skill does more than rank ideas. Each leading idea needs:

- evidence-backed strengths;
- trade-offs;
- the riskiest assumption;
- the cheapest useful test;
- a stop signal.

This is one of the best parts of the package. Strategyzer's Assumption Mapping also asks what must be true, how important it is, and how much evidence exists. Its Test Card adds a measure and success threshold. RAD Brainstorm already has most of this model. See [Assumption Mapping](https://www.strategyzer.com/library/how-assumptions-mapping-can-focus-your-teams-on-running-experiments-that-matter).

The small missing part is a pass threshold. “Run a landing page test” is weaker than “Run a landing page test; continue only if 20 qualified visitors join the waitlist.” Add a clear result threshold when the domain allows it.

### 5. Quick and full tiers are a strong control, with hidden quick-mode cost

Quick is a real product advantage. It promises a small number of turns, no subagents, and no file unless asked. Superpowers requires its full design process for every creative software task. Arc requires at least three answered questions before it proposes approaches. BMAD aims past 100 ideas and changes methods through a long session. See [Superpowers brainstorming](https://github.com/obra/superpowers/blob/main/skills/brainstorming/SKILL.md), [Arc ideate](https://github.com/howells/arc/blob/main/plugins/arc/skills/ideate/SKILL.md), and [BMAD brainstorming](https://github.com/bmad-code-org/BMAD-METHOD/blob/main/src/core-skills/bmad-brainstorming/SKILL.md).

The hidden cost is reference loading. `brainstorm-session` always tells the agent to read the 2,587-word facilitation guide. Method selection can then pull from a 6,446-word catalog. This is too much reading for a five-turn quick session.

A better quick path needs a short core card inside the skill:

- six common methods;
- one line on when to use each;
- one small output shape;
- no large reference unless the user asks for a named method.

### 6. Optional research is rare and well bounded

Current research can enter only after the user agrees. The research task is read-only, has a 6 to 10 search target, uses primary sources first, separates facts and inference, records uncertainty, and returns checked JSON.

This is better than a normal brainstorm that guesses about a current market or law. It is also lighter than BMAD's separate deep-research workflow.

Three issues reduce the value:

1. `domain-research-guide.md` is not linked from a skill or subagent prompt. It is unused package weight.
2. That guide ranks paid market reports above official documents, while the active subagent prompt says primary sources first.
3. The guide defines three research depths, while the active prompt uses one fixed 6 to 10 search range.

Remove the unused guide. Put any essential source and stop rules in the subagent prompt. This keeps one source of truth.

### 7. The method library is broad, repeated, and no longer a market advantage

RAD Brainstorm has 19 named methods. The count looks strong until compared with BMAD's catalog of more than 60 methods. A method-count contest will favor the larger system and will add more maintenance work. See [BMAD method catalog](https://github.com/bmad-code-org/BMAD-METHOD/blob/main/src/core-skills/bmad-brainstorming/assets/brain-methods.csv).

RAD should compete on method choice and session quality. Six reliable generation methods and five reliable evaluation methods are enough for the main path.

The current files repeat content:

- The convergent section in `methodology-catalog.md` repeats methods in `evaluation-frameworks.md`.
- `creative-unblocking.md` repeats Worst Possible Idea, random stimulus, opposite prompts, time shifts, and analogies.
- Five Whys appears in its own skill and the method catalog.
- The main skill and `facilitation-principles.md` repeat user-first, one-question, phase, research, and close rules.

Consolidation can cut several thousand words without removing a workflow.

### 8. Some research and source claims need correction

The package contains source names and precise claims without links. Public distribution raises the need for clean attribution.

Examples:

- `creative-unblocking.md` treats choice overload as a general rule and cites Barry Schwartz. A meta-analysis across 50 experiments found an average effect near zero with strong variation by setting. The sentence needs a condition or removal. See [Can There Ever Be Too Many Options?](https://ideas.repec.org/a/oup/jconrs/v37y2010i3p409-425.html).
- `evaluation-frameworks.md` says Klein's research showed about 30 percent better risk identification. Klein described the premortem. The 30 percent figure is tied to earlier prospective-hindsight research by Mitchell, Russo, and Pennington. See [Klein's HBR article](https://hbr.org/2007/09/performing-a-project-premortem) and [Back to the Future](https://onlinelibrary.wiley.com/doi/abs/10.1002/bdm.3960020103).
- The anti-anchoring claim is too broad, as described above.
- Several method origins have author and book names without source links.

Add a short “Method sources” section. Remove claims that do not change the workflow. A skill does not need to prove every common method. It must avoid using a weak claim to justify a hard rule.

### 9. `design-sprint` is a good workflow with the wrong name

The skill reads project evidence, asks one question at a time, covers architecture and behavior, presents sections for approval, writes one spec, reviews it, and stops before implementation. That is a useful software design workflow.

The established Design Sprint is a four or five-day team process that maps a problem, sketches solutions, decides, makes a realistic prototype, and tests it with users. The current RAD skill does not prototype or test with users. See [The Sprint Book method](https://www.thesprintbook.com/stories/nyt).

The name can cause three problems:

- Users can expect the established method.
- The skill can trigger on visual or product design requests that it rejects.
- It overlaps with Superpowers brainstorming and Arc ideate under a vague software design label.

Rename it to `software-design`. Keep its current scope. A future real Design Sprint should be a separate product only if users ask for it.

### 10. Five Whys has better guardrails than the usual version

The skill treats five as a guide, allows branches, separates evidence from belief, avoids blame, and does not force one cause onto a multi-cause problem. These rules fix common Five Whys failures.

ASQ also says the method may take fewer or more than five questions and notes that complex issues can have more than one root cause. See [ASQ Five Whys](https://asq.org/quality-resources/five-whys).

Keep the skill with a narrow role:

- user-led process or operating problems;
- repeated symptoms with enough facts to discuss;
- problem framing before solution ideas.

Keep code diagnosis in debugging or repository tools. Remove the duplicate Five Whys method text from the catalog.

### 11. The JSON checks protect shape, with limited quality checks

The validator checks required fields, object shapes, enums, arrays, and extra properties. The three bounded subagent prompts have clear read-only rules. Five unit tests cover valid output for each schema, one invalid enum, and JSON extraction.

Limits:

- Source URLs can be empty strings and source arrays can be empty.
- `searches_used` has no minimum.
- The idea challenge can use web research, but its schema has no source field.
- A valid response can contain empty strengths, risks, or recommendations.
- The fallback validator does not support many JSON Schema rules that could enforce non-empty values.
- Tests do not force the fallback path or check missing required fields and extra properties.

These are normal limits for a small port. The public wording should say “schema checked” instead of “quality checked.” Add a top-level source list to the idea challenge if it can make current web claims.

### 12. Output control is safe, and continuity is weak

The user chooses conversation, a personal file, or a dated project file. The plugin never writes to `docs/design.md`, never creates `docs/ideas.md`, and never commits. This protects user control and works well with RAD Repo and RAD Plan.

Long sessions have no checkpoint or resume state. BMAD writes a session log with authorship and can resume. Miro keeps board history and comments. RAD can lose a long idea trail after context loss or interruption.

Do not copy BMAD's full state system. Add one optional checkpoint for full sessions:

- save only after user consent;
- use one dated Markdown file;
- record topic, goal, constraints, ideas, source, current phase, decisions, and next question;
- keep quick sessions file-free.

## Strengths and Weaknesses

### Strengths

| Strength | Why it matters |
|---|---|
| User-first protocol | Protects ownership and delays early AI anchoring. |
| Three working modes | Supports guided, shared, and agent-led sessions without mixing them. |
| Quick and full tiers | Lets the user control time and agent cost. |
| One question at a time | Keeps the session easy to answer. |
| Separate generation and evaluation | Reduces early judgment and first-idea bias. |
| User scores first | Prevents the model's ranking from setting the user's view. |
| Multi-domain use | Works for software, business, content, travel, creative work, and personal choices. |
| Evidence before software design | Existing code and documents shape technical ideas. |
| Gated current research | Adds facts only when they can change the ideas. |
| Bounded subagents | Research and review have narrow read-only jobs. |
| JSON contracts | Malformed subagent output can be rejected before use. |
| Assumption and proof close | Ideas end with a cheap learning action. |
| Stop signals | Weak ideas can die before they consume more time. |
| Rejected-idea record | The user can see what was considered and why it was parked. |
| No implementation | Brainstorming cannot silently become a coding run. |
| No automatic commit | The owner controls durable output and Git history. |
| Companion-skill rule | Sibling skills are named only when installed, available, needed, and useful. |
| Low software needs | The plugin needs only Markdown and Python for optional validation. |

### Weaknesses

| Weakness | Effect |
|---|---|
| 25,164-word package | A small plugin carries a large instruction and maintenance cost. |
| Large quick-mode references | A short session can load thousands of words before generating three options. |
| Repeated method text | Changes can drift across files and raise review cost. |
| Unused domain research guide | The package carries a 2,498-word file that no workflow calls. |
| Overstated AI research claim | Public reasoning appears more settled than the evidence. |
| Wrong premortem attribution | A precise number is tied to the wrong research source. |
| Broad choice-overload claim | A disputed general effect is presented as a fixed rule. |
| Weak intake for goal and success | The session can generate good ideas for the wrong outcome. |
| No idea-source labels | User, AI, and research contributions can blend together. |
| No diversity check | Three options can be minor forms of one mechanism. |
| No clustering step | Ten or more ideas can enter scoring as a noisy, repeated set. |
| No stable result template | Saved outputs can vary between runs and hand off poorly. |
| No resume support | A long full session can lose state after interruption. |
| No visual summary | Complex relationships remain in linear text. |
| No group support | It cannot match live boards, voting, private input, or parallel entry. |
| Misnamed design-sprint skill | Users can expect prototyping and user tests that the workflow does not perform. |
| Root-cause scope inside a brainstorm plugin | Five Whys widens trigger and product boundaries. |
| Schema checks only | Valid JSON can still contain weak or empty evidence. |
| No behavior examples | Users cannot quickly see a good quick, full, or evaluation result. |

## Comparison With Similar Tools

| Tool | Main job | What it does better | Where RAD Brainstorm is better |
|---|---|---|---|
| Superpowers brainstorming | Turn a software idea into an approved design and hand it to planning | Strong compliance gates, section approvals, visual companion, and direct plan handoff | Broader domains, explicit user-first ownership, quick tier, separate idea evaluation, optional research, and no auto-commit |
| Arc ideate | Turn a code-aware idea into a reviewed feature spec | Deep code context, strict interview format, reference capture, specialist reviews, and UI requirements | Less system weight, broader domains, clear generation phase, user scores first, and no required three-question gate |
| BMAD brainstorming | Run a long creative session with many methods and durable state | More than 60 methods, visual method picker, authorship log, resume, headless mode, and long divergence | Faster default, smaller workflow, stronger evaluation contract, cheap tests, stop signals, and no installed project system |
| Miro AI | Visual team ideation and synthesis | Live and async group work, canvas, clustering, comments, voting, diagrams, and history | Better one-to-one facilitation, user-first timing, evidence-aware research, and no account or board |
| FigJam AI | Visual workshops and sticky-note synthesis | Team participation, theme sorting, summaries, diagrams, and editable visual grouping | Better causal and evaluation dialogue, research, stop signals, and repository-aware software work |
| Whimsical AI | Fast AI mind-map expansion | Five-node visual branches, quick repeated expansion, diagrams, and current Codex MCP support | Protects user ownership, separates phases, tests assumptions, and records rejected ideas |
| Mural AI | Team canvas, clustering, and summaries | Group workshops, theme clusters, mind maps, and Microsoft 365 links | Smaller setup, clearer owner conversation, evidence checks, and no enterprise workspace need |
| IDEO brainstorm rules | Group idea generation with phase discipline | Simple group rules, visual work, quantity, and shared energy | AI timing rules, user ownership, evaluation, current research, and durable decision close |

### Superpowers

Superpowers is a close software rival. It reads project context, asks one question at a time, proposes two or three approaches, presents the design in sections, writes a design file, reviews it, and moves to planning. It now has an optional browser companion for visual questions.

RAD Brainstorm gives the user more control over the front of the process. It supports non-software work, offers a five-turn quick path, asks the user for ideas before adding model content, separates idea evaluation into its own skill, and does not commit the result.

Superpowers has stronger workflow enforcement. RAD rules are clear, yet they use fewer hard format checks. Copying its large visual server would add too much code. An optional Mermaid or current visualization output is enough.

### Arc

Arc's ideate skill is a senior software design interview. It enforces a short message format during intake, requires at least three answered questions, reads code facts instead of asking the user, presents two or three approaches, and can call specialist reviewers. It also captures UI source links and reference material.

RAD is better for open ideation and solo owner agency. Arc is better after the work is clearly a software feature. RAD should adopt Arc's five intake facts: problem, user, success, scope, and hard constraints. It should also capture source links in a saved result.

### BMAD

BMAD is the closest general brainstorming system. It has facilitator, partner, and autonomous stances, which closely match RAD's three modes. It adds a browser method picker, more than 60 techniques, session logs, authorship labels, resume, headless operation, and a goal of more than 100 ideas.

RAD should not copy BMAD's size. It should adopt two small ideas:

- label who supplied each idea;
- offer one optional checkpoint for long full sessions.

BMAD's source also shows a good context rule: query a method catalog for the chosen method instead of loading the whole library. RAD can do this with a compact index and exact section reads.

### Visual applications

Miro, FigJam, Whimsical, and Mural win when several people need to add content, see it at once, cluster it, vote, comment, or return later. Their canvas is the shared object.

RAD's shared object is the conversation. This is enough for one owner and a modest idea set. It becomes weak with more than ten ideas, several contributors, or spatial relationships.

The lean answer is a text-first cluster and an optional visual summary. A full canvas, voting engine, and collaboration service belong outside this plugin.

## What RAD Brainstorm Does Better

### It protects the owner's voice before model output

This is the clearest difference from AI-first generators. The user can state instincts, rejected paths, and half-formed ideas without responding to a polished model list.

### It works from thought to proof

The result includes the risky assumption, cheapest proof, and stop signal. This helps the user learn before planning or building.

### It keeps judgment in the right phase

Generation, evaluation, and software design have clear boundaries. The user knows when judgment begins.

### It makes the user rank first

This small rule protects independent judgment. Most AI tools rank their own ideas and ask the user to accept the result.

### It adds current facts without turning every session into research

The research gate is specific: use it only when a current fact can change the idea set. The user must agree first.

### It has a practical small-session mode

Three options and one recommendation can be enough. BMAD's long divergence and Superpowers' full design gate fit different needs.

### It keeps file and implementation control with the user

The plugin does not create a repo tree, project database, hidden board, implementation branch, or commit. A saved result remains plain Markdown.

## Where RAD Brainstorm Falls Short

### It does not settle the target before generating

The anti-anchoring intake asks about current ideas, preferred direction, and rejected paths. It does not always settle the problem, user, success signal, and hard constraints first. This can produce diverse ideas that solve the wrong problem.

Add a short frame before the user's idea list:

1. What result do you want?
2. Who is it for?
3. What would count as success?
4. Which constraint cannot move?

Ask only missing items. Keep one question per turn.

### It counts options without checking their underlying difference

Three “strong options” can share the same mechanism. Different colors, formats, or feature bundles do not create real option diversity.

Add a diversity pass before evaluation:

- group ideas by underlying mechanism;
- name repeated forms;
- check actor, channel, timing, business model, and technical approach when relevant;
- run one extra generation pass if all leading ideas share one mechanism.

Research on LLM idea variance found that stepwise prompts and distinct ordinary personas can increase diversity. Use ordinary stakeholder views, such as a new user, support worker, buyer, operator, or maintainer. Avoid celebrity personas. See [Prompting Diverse Ideas](https://arxiv.org/abs/2402.01727) and [Examining and Addressing Barriers to Diversity in LLM-Generated Ideas](https://arxiv.org/abs/2602.20408).

### Large idea sets enter evaluation without cleanup

`idea-evaluation` routes ten or more ideas to Impact and Effort. It does not first remove exact duplicates, group near duplicates, or preserve parent-child relations.

Borrow the safe part of FigJam and Miro clustering:

1. Keep every original idea.
2. Propose theme clusters.
3. Mark near duplicates.
4. Ask the user to approve merges.
5. Score cluster leaders or distinct candidates.

### The saved result has no fixed contract

The skill lists required content, but it has no template or version marker. RAD Plan and RAD Repo will receive outputs that can vary in headings and detail.

Add one small template with:

- topic and desired result;
- user and hard constraints;
- ideas with source labels;
- distinct mechanisms covered;
- recommended and strong alternative;
- rejected or parked ideas;
- risky assumptions;
- cheapest proof and pass or stop threshold;
- open evidence gaps;
- next decision;
- status and transient note.

### The method references are harder to maintain than the workflows

Five large guides contain more text than the four skill files and validator combined. The current duplication has already caused source drift and conflicting research rules.

### Group and visual use is weak

One-question dialogue works for one owner. It does not collect independent ideas from several people at once, hide authors during scoring, or show relationships on a canvas. State this limit in the README.

### The validator result can sound stronger than it is

Schema validation proves structure. It does not prove that claims are true, ideas are diverse, or a spec is good. Public text should make this boundary clear.

## Elements Worth Adopting

### From Arc: a five-fact intake

Before generation, settle only missing facts about the problem, user, success, scope, and hard constraints. Repository facts should come from files when available.

### From BMAD: idea authorship and one optional checkpoint

Mark ideas as `user`, `AI`, or `research`. In partner mode, this keeps ownership visible. For a long full session, offer one small checkpoint file that can resume the phase and next question.

### From visual boards: clustering with preserved originals

Group large idea sets by theme or mechanism. Keep the original text and let the user correct groups before scoring.

### From human-AI research: deliberate AI timing

Keep the user-first rule. Add AI ideas after the user's first pass. If the user asks for generator mode, state that choice and use a wider diversity prompt.

### From diversity research: ordinary viewpoints and staged passes

Use two or three normal stakeholder views when an idea set is narrow. Generate in separate passes by problem mechanism. Do not ask the model to show private reasoning.

### From Strategyzer: a proof threshold

Add a measure and a pass or stop threshold to the cheapest proof when possible.

### From Superpowers and Whimsical: optional visual output

At the end, offer a mind map, decision tree, or comparison diagram only when the current tool list supports it and the relationships are easier to see than read. Use Mermaid or the available visual skill. Do not bundle a server.

### From the Agent Skills standard: smaller focused references

The Agent Skills specification recommends focused reference files that load only when needed. Keep the main skill under 500 lines and make small references available on demand. See the [Agent Skills specification](https://agentskills.io/specification).

## Elements to Remove or Reduce

### Remove now

- `domain-research-guide.md`, after any essential source rule moves into the active research prompt.
- The duplicate convergent-method section from `methodology-catalog.md`.
- The duplicate Five Whys catalog entry.
- Repeated unblocking method descriptions that already exist in the method catalog.
- The unsupported broad choice-overload statement.
- The misattributed premortem percentage, unless it receives correct source text and careful wording.
- The claim that AI ideation research has one consistent result.

### Rename

- `design-sprint` to `software-design`.
- “validation” wording to “schema validation” where it refers to the JSON script.

### Reduce

- Compress `facilitation-principles.md` to the rules that are not already in `brainstorm-session`.
- Keep a short core method set in the normal router.
- Reduce TRIZ to a small, cited technical card or make it an optional named method.
- Remove SWOT from the default evaluation set. It is broad, weak for selection, and does not appear in the main routing table.
- Replace long origin stories and examples with source links and one practical example.

### Keep

- All three working modes.
- Quick and full tiers.
- User-first anti-anchoring sequence.
- One question at a time.
- Separate generation and evaluation phases.
- User scores first.
- Assumption Mapping, Pre-Mortem, Weighted Scoring, Impact and Effort, Jobs-to-be-Done, and Opportunity Solution Tree.
- Research consent and source rules.
- One bounded idea challenge.
- One bounded spec review.
- JSON-first subagent contracts.
- File destination choice.
- No implementation and no auto-commit rules.
- Companion-skill availability rule.
- Five Whys guardrails, with a narrow problem-framing position.

## Recommended 4.1 Change Order

### P0: product truth and naming

1. Rename `design-sprint` to `software-design`.
2. Narrow the public AI anchoring claim.
3. Correct or remove the premortem and choice-overload claims.
4. State the one-person, text-first limit in the README.

### P1: better idea quality

5. Add the short goal, user, success, and constraint frame.
6. Track user, AI, and research idea sources.
7. Add the mechanism diversity pass.
8. Add clustering before evaluation for large sets.
9. Add a result threshold to cheap proofs when useful.

### P2: lower reading and maintenance cost

10. Remove the unused research guide.
11. Remove repeated convergent and unblocking content.
12. Compress the facilitation guide.
13. Use a small core method index and exact section reads.

### P3: continuity and proof

14. Add one result template and three short examples.
15. Add optional full-session checkpoint and resume fields.
16. Add a source list to the idea-challenge schema.
17. Add focused validator tests for missing fields, extra properties, non-empty sources, and the fallback path.
18. Offer a visual summary only when an available tool and current content justify it.

## Suggested Lean Workflow

```text
User asks to brainstorm
  -> Confirm brainstorm intent when unclear
  -> Choose quick or full
  -> Settle missing goal, user, success, and hard constraint
  -> Choose facilitator, partner, or generator
  -> Capture the user's ideas first
  -> Add current research only when it can change the idea set and the user agrees
  -> Generate with one core method or a small full-session batch
  -> Label each idea source
  -> Check for distinct underlying mechanisms
  -> Cluster large sets and preserve originals
  -> Switch to evaluation
  -> User scores first
  -> Select a recommendation and strong alternative
  -> Name the risky assumption, cheap proof, threshold, and stop signal
  -> Deliver one stable result
  -> Save only where the user chooses
  -> Suggest an installed companion only when it is needed and useful
```

For a root-cause request:

```text
Observed symptom
  -> User-led Why chain
  -> Branch when more than one cause is credible
  -> Separate evidence, belief, and inference
  -> Confirm the likely cause
  -> Brainstorm solutions only after user agreement
```

For a chosen software idea:

```text
Chosen approach
  -> Read current repo evidence
  -> Settle design decisions one at a time
  -> Approve sections
  -> Write one software design spec
  -> Run inline and bounded schema-checked review
  -> User approves
  -> Offer installed planning skill only when needed and useful
```

## Suggested Public Positioning

> RAD Brainstorm is a Codex thinking partner for solo builders and creators. It draws out your ideas before it adds its own, keeps idea generation separate from judgment, and ends with a clear choice, risky assumption, and cheap next test. Quick sessions stay short. Full sessions can add current research and a focused challenge. It writes or commits nothing unless you choose a destination.

Short comparison line:

> More guided than normal chat, lighter than a full discovery system, and more protective of your own thinking than an AI idea generator.

## What Would Make It Stand Out

The standout feature should be a visible **idea ownership and diversity check**.

For every full session and any quick session with AI-generated options:

1. Mark each idea as user, AI, or research.
2. Group ideas by their underlying mechanism.
3. Show which mechanisms are missing or repeated.
4. Run one extra pass from distinct normal stakeholder views when the set is narrow.
5. Let the user rank before the model.
6. End with a cheap proof and a pass or stop threshold.

This is small enough to understand in one minute. It addresses the current research risk of AI idea similarity. It also gives the plugin a clear public result that Superpowers, Arc, BMAD, and visual boards do not combine in the same lean workflow.

## Features to Avoid

- A library larger than BMAD's method set.
- A built-in whiteboard or browser server.
- Mandatory multi-agent panels.
- Automatic market research for every topic.
- AI creativity, novelty, or confidence scores presented as objective facts.
- A database or hidden session state.
- Automatic file creation in quick mode.
- Automatic commits.
- Planning or implementation inside the brainstorm skill.
- A real-time deploy or execution monitor.

## Contrarian Views and Risks

### User-first can slow blank-slate users

Some users want AI examples because they have no starting idea. Research also shows that AI can improve individual creativity. Keep generator mode and the progressive unblocking ladder. State the mode so the user understands that AI is setting the first anchors.

### Three options can be enough

A diversity pass can become process for its own sake. Run it only when the options share one mechanism or the stakes justify a wider search.

### Source labels can feel mechanical

Use simple labels in the running ledger and saved result. The conversation does not need to announce a label after every sentence.

### Clustering can erase useful differences

Preserve originals and ask before merging. AI-proposed groups are suggestions.

### Removing method text can hurt named-method users

Keep concise, cited cards for named modes. Remove duplicate explanations and long origin stories.

### A checkpoint file can violate the low-file promise

Make it optional, full-session only, and one file. Quick stays file-free.

### Renaming a skill can break existing prompts

If the public marketplace has users, keep a one-release alias or migration note from `design-sprint` to `software-design`.

### Research changes quickly

Human-AI creativity results vary by task, model, timing, user skill, and measure. The plugin should state a careful design reason and avoid claiming one settled law.

## Open Questions for Ryan

1. Should the next release rename `design-sprint` to `software-design`, with a short compatibility note?
2. Should Five Whys stay as a public skill, or move to a later problem-framing plugin?
3. Do you want full sessions to offer one optional checkpoint file for resume?
4. Should saved idea lists show short source labels: `user`, `AI`, and `research`?
5. Should the plugin offer an optional Mermaid mind map when a result has useful relationships?
6. Is the desired core method set six generation methods and six evaluation methods, with the rest available only by name?

## Sources

### RAD Brainstorm source reviewed

- [RAD Brainstorm README](../../plugins/rad-brainstorm/README.md): public promise, tiers, outputs, and companion rules.
- [Brainstorm session](../../plugins/rad-brainstorm/skills/brainstorm-session/SKILL.md): user-first intake, research, generation, evaluation, output, and close.
- [Idea evaluation](../../plugins/rad-brainstorm/skills/idea-evaluation/SKILL.md): user-first scoring, framework selection, challenge, and decision output.
- [Five Whys](../../plugins/rad-brainstorm/skills/five-whys/SKILL.md): causal interview and guardrails.
- [Software design](../../plugins/rad-brainstorm/skills/software-design/SKILL.md): technical design workflow, renamed during the 4.1 work.
- [Facilitation principles](../../plugins/rad-brainstorm/references/facilitation-principles.md): anti-anchoring and conversation rules.
- [Creative unblocking](../../plugins/rad-brainstorm/references/creative-unblocking.md): blank-page ladder and current research claims.
- [Methodology catalog](../../plugins/rad-brainstorm/references/methodology-catalog.md): 19 generation and evaluation methods.
- [Evaluation frameworks](../../plugins/rad-brainstorm/references/evaluation-frameworks.md): current comparison and risk methods.
- `domain-research-guide.md`: unused research depth and source rules identified for removal during the 4.1 work.
- [Subagent prompts](../../plugins/rad-brainstorm/references/subagent-prompts): bounded research, idea challenge, and spec review contracts.
- [JSON validator](../../plugins/rad-brainstorm/scripts/validate-json.py): implemented schema checks.
- [Validator tests](../../plugins/rad-brainstorm/tests/test_validate_json.py): current five-test coverage.

### Comparable skills and systems

- [Superpowers brainstorming](https://github.com/obra/superpowers/blob/main/skills/brainstorming/SKILL.md): software design gate, section approval, visual companion, output, and plan handoff.
- [Arc ideate](https://github.com/howells/arc/blob/main/plugins/arc/skills/ideate/SKILL.md): strict question loop, code-aware feature design, reviewer roles, and spec output.
- [BMAD brainstorming](https://github.com/bmad-code-org/BMAD-METHOD/blob/main/src/core-skills/bmad-brainstorming/SKILL.md): modes, long divergence, catalog selection, session log, and resume.
- [BMAD workflow map](https://github.com/bmad-code-org/BMAD-METHOD/blob/main/docs/reference/workflow-map.md): brainstorming, idea challenge, research, and product workflow boundaries.
- [BMAD method catalog](https://github.com/bmad-code-org/BMAD-METHOD/blob/main/src/core-skills/bmad-brainstorming/assets/brain-methods.csv): current method breadth and method metadata.
- [Agent Skills specification](https://agentskills.io/specification): progressive disclosure and focused reference guidance.

### Visual brainstorming applications

- [Miro AI](https://help.miro.com/hc/en-us/articles/28765406244498-Miro-AI-overview): idea generation, summaries, diagrams, and clustering.
- [Miro clustering](https://help.miro.com/hc/en-us/articles/4409706795410-Clustering): keyword, sentiment, author, and manual groups.
- [FigJam AI sorting and summaries](https://help.figma.com/hc/en-us/articles/18711926790423-Sort-and-summarize-stickies-with-FigJam-AI): copied clusters, theme sorting, and summaries.
- [Whimsical AI mind maps](https://whimsical.com/learn/get-started/ai-mind-maps): five-node AI expansion and repeat branching.
- [Mural AI](https://www.mural.co/mural-ai): team mind maps, summaries, and clustering.

### Official method sources

- [IDEO Brainstorm Rules](https://www.designkit.org/methods/brainstorm-rules.html): delayed judgment, quantity, focus, and shared generation rules.
- [The Sprint Book method](https://www.thesprintbook.com/stories/nyt): map, sketch, decide, prototype, and user-test sequence.
- [ASQ Five Whys](https://asq.org/quality-resources/five-whys): variable question count, cause depth, and use with other root-cause tools.
- [Strategyzer Assumption Mapping](https://www.strategyzer.com/library/how-assumptions-mapping-can-focus-your-teams-on-running-experiments-that-matter): importance, evidence, and four assumption types.
- [Performing a Project Premortem](https://hbr.org/2007/09/performing-a-project-premortem): Klein's premortem method and dissent purpose.
- [Back to the Future](https://onlinelibrary.wiley.com/doi/abs/10.1002/bdm.3960020103): Mitchell, Russo, and Pennington's prospective-hindsight research.

### Research

- [Partnering with Generative AI](https://arxiv.org/abs/2510.23324): human-led and model-led effects on quality, diversity, and ownership.
- [Creative Momentum Transfer](https://www.ijcai.org/proceedings/2025/1142): effects of early and late AI ideas and source labels.
- [An empirical investigation of the impact of ChatGPT on creativity](https://www.nature.com/articles/s41562-024-01953-1): individual creativity gains across five experiments.
- [ChatGPT decreases idea diversity in brainstorming](https://www.nature.com/articles/s41562-025-02173-x): average creativity and idea-pool diversity trade-off.
- [Generative AI enhances individual creativity but reduces collective diversity](https://doi.org/10.1126/sciadv.adn5290): story quality gains and similarity risk.
- [The Effects of Generative AI on Design Fixation and Divergent Thinking](https://arxiv.org/abs/2403.11164): visual design fixation, idea count, variety, and originality.
- [The Double-Edged Roles of Generative AI in the Creative Process](https://pubsonline.informs.org/doi/10.1287/isre.2024.0937): ideation gains and implementation effects by expertise.
- [Prompting Diverse Ideas](https://arxiv.org/abs/2402.01727): LLM idea variance and staged prompt effects.
- [Examining and Addressing Barriers to Diversity in LLM-Generated Ideas](https://arxiv.org/abs/2602.20408): fixation, knowledge partitioning, structured passes, and ordinary personas.
- [Can There Ever Be Too Many Options?](https://ideas.repec.org/a/oup/jconrs/v37y2010i3p409-425.html): choice-overload meta-analysis and setting-dependent effects.
- [Productivity loss in brainstorming groups](https://doi.org/10.1037/0022-3514.53.3.497): classic group-brainstorming losses and production blocking.

## Rerun Inputs

```text
workflow: firecrawl-deep-research
topic: Evaluate the public RAD Brainstorm Codex plugin against current brainstorming skills, AI ideation systems, visual brainstorming applications, and human-AI creativity research
depth: thorough
output: markdown
constraints: Prefer primary sources and official product documents; inspect all local plugin source and validation files; focus on solo builders and creators; recommend small changes that protect user ownership and reduce package weight; identify removal and rename candidates; do not implement plugin changes
fallback_used: live web search because the Firecrawl command and API key were unavailable
```
