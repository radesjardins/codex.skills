# Idea Evaluation Frameworks

Read only the selected section. Define criteria before scoring. The user scores first.

## Router

| Situation | Method |
| --- | --- |
| Ten or more ideas | Impact and Effort |
| Three to five ideas with major unknowns | Assumption Mapping |
| Product options tied to an outcome | Opportunity Solution Tree |
| High-risk choice | Pre-Mortem, then Assumption Mapping |
| Two or three finalists | Weighted Scoring |
| Unclear user need | Jobs-to-be-Done |

## Impact and Effort

Use for a large idea set after clustering.

1. Define impact for the current success measure.
2. Define effort in terms the user can estimate.
3. Let the user place each cluster or idea.
4. Review high-impact, low-effort options first.

Treat uncertain placements as assumptions. Avoid precise scores when evidence is weak.

## Assumption Mapping

Use when uncertainty drives the decision.

List the claims that must be true under desirability, feasibility, viability, and adaptability. Rate each claim by importance and evidence. The highest-importance, lowest-evidence claim becomes the riskiest assumption.

End with one cheap proof, a pass threshold, and a stop signal.

Source: [Strategyzer Assumption Mapping](https://www.strategyzer.com/library/how-assumptions-mapping-can-focus-your-teams-on-running-experiments-that-matter).

## Opportunity Solution Tree

Use when ideas should connect to one measurable outcome.

Map:

```text
Outcome
  -> Opportunity or user need
     -> Candidate solution
        -> Test
```

Keep opportunities separate from solutions. Compare ideas that address the same opportunity before comparing across branches.

## Pre-Mortem

Use for a serious choice before commitment. Assume the choice failed, then list plausible causes. Rank causes by effect and preventability. Convert the top cause into a mitigation or test.

The method helps people voice concerns that normal planning may suppress. Do not attach a fixed improvement percentage to it.

Sources:

- [Performing a Project Premortem](https://hbr.org/2007/09/performing-a-project-premortem)
- [Back to the Future](https://onlinelibrary.wiley.com/doi/abs/10.1002/bdm.3960020103)

## Weighted Scoring

Use for two or three finalists when the user can define meaningful criteria.

1. Define three to five criteria.
2. Set weights that total 100.
3. Let the user score each idea on one common scale.
4. Multiply scores by weights.
5. Discuss close results and evidence gaps.

Example:

| Criterion | Weight | Idea A | Idea B |
| --- | ---: | ---: | ---: |
| User value | 50 | 4 | 3 |
| Time to proof | 30 | 2 | 5 |
| Fit with constraints | 20 | 5 | 3 |

The total informs the discussion. It does not replace judgment.

## Jobs-to-be-Done

Use when the user need is unclear or an idea may solve the wrong problem.

Frame the job as: `When <situation>, the user wants to <motivation>, so they can <result>.`

Test each idea against the same job. Ask what the user does now, what causes a switch, and what outcome signals progress.

## Framework rules

- Cluster exact and near duplicates before choosing a framework.
- Preserve original idea text and source labels.
- Ask before merging ideas that differ in audience, mechanism, channel, cost, or risk.
- Record user scores separately from AI comments.
- End with a recommendation, strong alternative, riskiest assumption, cheap proof, pass threshold, and stop signal.
- Use one framework unless a second framework answers a different decision question.
