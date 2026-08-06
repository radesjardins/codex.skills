# Stack Decision Scorecard

Use this reference only when the work needs a real technology choice. Keep the existing stack when it can meet the approved requirement.

The stack advisor must make one recommendation. It must use current primary sources for versions, compatibility, maintenance, security notices, licensing, pricing, and deployment support.

## Decision criteria

| Criterion | Question | Evidence |
|---|---|---|
| Existing fit | Can the current stack meet the requirement without a new system? | Repository code, architecture, and current deployment |
| User fit | Can the owner maintain and pay for it? | Confirmed skills, budget, accounts, and constraints |
| Agent accuracy | Do current docs, types, schemas, and error messages give the coding agent clear feedback? | Primary docs and a small proof when needed |
| Test support | Can the important behavior and failures be checked locally or in CI? | Official test guidance and repository patterns |
| Deployment fit | Does it work on the approved target without a new operating burden? | Current platform documentation |
| Maintenance | Is the project active and is the selected version supported? | Release and support policy |
| Compatibility | Do the selected versions work together? | Primary compatibility tables and release notes |
| Security and license | Are current advisories and license terms acceptable? | Official advisory and license sources |
| Cost | What new recurring cost, service, or operational work appears? | Current pricing and service limits |
| Need | Which approved requirement fails without this addition? | PRD, interview answer, or plan outcome |

## Decision rules

1. Prefer the current stack when it meets the requirement.
2. Add the fewest new tools and services.
3. Treat user skill, deployment limits, and paid services as hard constraints.
4. Compare only plausible options.
5. Pin versions only when the repository uses pins or compatibility requires one.
6. State uncertainty. Do not invent benchmark claims about agent accuracy.
7. Stop when requirements conflict or no supported option fits.

## Output

Return:

- recommended choice and version;
- one short reason tied to the requirement;
- current-stack fit;
- alternatives considered and why they lost;
- new dependencies, services, cost, and operating work;
- compatibility notes;
- primary verification sources and check date;
- confidence and any owner decision still required.

## When live research is required

Use current primary sources when:

- a new framework, service, or deployment target is proposed;
- a version or compatibility claim affects the plan;
- pricing or service limits affect scope;
- a security advisory can change the decision;
- the repository uses a version that may be outside support.

Skip stack research when the stack is settled and the work adds no new platform, service, or dependency.
