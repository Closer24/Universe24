---
name: boss-orchestrator
description: Coordinate Universe24 specialist agents, dependencies, completion evidence and PR integration for multi-part project work.
---

# Boss orchestration

Read [the shared workflow](../workflow.md). Own the user's complete objective,
task allocation and integration decisions; specialist logic stays in its skill.

Use the shared [critical review](../workflow.md#critical-review-of-proposed-changes)
before committing to a substantial approach. Challenge assumptions with evidence,
compare relevant successes and failures, and carry the resulting acceptance or
disproof conditions into specialist handoffs. Preserve user scope and proportionality.

## Persistent project reference

Treat **Universe 24 Highlights** as the high-level project specification:
https://docs.google.com/document/d/1IkhSyqZZMBSgbJV-PMMwcXG0D_Rlfg4FrLy2jXBMUSs/edit

Use the versioned [implementation coverage map](../../docs/HIGHLIGHTS_IMPLEMENTATION.md)
to reconcile entities and laws with their source contracts and tests. When an
authorized change adds or changes a durable entity or rule, include its Highlights
reconciliation in the same PR: identify the live document revision, update the
coverage map, and distinguish implemented behavior from hypotheses and gaps.
Do not claim the live document changed from a repository edit alone.
Use the [regression skill](../regression-check/SKILL.md#daily-genericity-audit)
for the daily engine/result-consumer audit and schedule restoration.

At the start of relevant work, reconcile the applicable project rules and hypotheses with this document. When the user changes a durable project rule, update the relevant repository Skill(s) as part of the same work when authorized, so the rule does not depend on chat history.

The primary model contract is [initialization-defined disturbances](../../docs/DISTURBANCES.md).
Scope historical scalar/particle assumptions to their explicitly named APIs.
Preserve user-defined field names as data and use headless execution by default;
do not route ordinary simulation work into mandatory visualization.

Use the shared workflow's rule/hypothesis/result distinction. Keep accepted
contracts locally readable and record the relevant Highlights revision/date in
the PR. Technical workflow belongs in this repository, not in Highlights.
Check the restart guide against the current checkout and live work; never treat
a dated snapshot or an unavailable source as current evidence.

## Mandatory persistence and self-improvement review

Before completion, review Boss itself and every participating or affected Skill.

- Retain demonstrated improvements to routing, decomposition, handoffs, validation
  and persistence. Apply authorized useful updates in the same task; otherwise
  report the proposed update without exceeding the user's scope.
- Put shared lessons in one authoritative reference and link affected Skills.
  Keep technical workflow here and physics/specification changes synchronized
  with their authorized contracts and Highlights.
- Keep the Skill set small and adaptable. Merge overlap, safely retire obsolete
  instructions, and split only when a distinct responsibility warrants it.
  Do not create a Skill solely for a one-off task.
- Rewrite superseded guidance; do not accumulate chat history, transient branch
  state or debugging logs in Skills.
- Record which Skills changed, or why no change is needed, in the task handoff.
  Persist authorized updates in the repository so another AI can continue.

## Route the work

| Need | Skill | Expected handoff |
| --- | --- | --- |
| Check or author space, entities, fields, run or display configuration | [simulation-configuration](../simulation-configuration/SKILL.md) | Validation report for checks; validated input, reusable definitions and exact invocation for authoring |
| Field law or response implementation | [field-development](../field-development/SKILL.md) | Explicit candidate contract and focused change |
| State, interfaces or dependency boundaries | [architecture-review](../architecture-review/SKILL.md) | Compatible ownership/schema assessment |
| Any physical-engine behavior change | [physics-rule-validation](../physics-rule-validation/SKILL.md) | Rule-by-rule acceptance or concrete blockers |
| Necessary tests, failures or redundant coverage | [test-runner](../test-runner/SKILL.md) | Minimal sufficient checks and actual results |
| Reproducible world execution | [simulation-runner](../simulation-runner/SKILL.md) | Identified initialization, metadata and trace; visual evidence only when requested |
| Rendering or visual interpretation | [visualization-check](../visualization-check/SKILL.md) | Faithful, inspected output |
| Unintended change to current physical behavior | [regression-check](../regression-check/SKILL.md) | Contract-focused regression evidence |
| Review, reconcile, close or merge PRs | [pr-review-and-merge](../pr-review-and-merge/SKILL.md) | Current-head integration decision |

For configuration requests, apply the shared
[task scope](../workflow.md#configuration-tasks-and-implementation-scope) before
assigning an implementation owner. Route data corrections, capability gaps and
suspected code defects separately; a failed validation report alone does not
request a code-changing subtask.

This routing table is a current default, not a permanent taxonomy. Change it when repeated task evidence shows that a smaller or clearer Skill set works better.

One agent may use multiple skills when no independent review is needed. Launch
agents only when delegation is authorized and independent tasks justify it.
Give implementation and required independent review to different owners where
practical. Do not create idle agents merely to match the table.

## Sequence and finish

1. Read current repository instructions, Universe 24 Highlights, open work and user scope. Record the base and identify conflicting files before assigning owners.
2. Classify new durable ideas as model rules, hypotheses to test, or verified results. For each hypothesis, define the test and pass condition before calling it successful.
3. Define the acceptance target and handoff for each task. Resolve shared schema and interface dependencies before parallel changes build on them.
4. For physics changes, obtain the rule contract/review and coordinate tests, simulation and regression evidence. Checks may share identical run outputs.
5. Reconcile completed branches on current main. Route changed interfaces or behavior back to the affected specialist; do not restart unrelated checks.
6. Run the mandatory persistence and self-improvement review. Review Boss itself, every affected child Skill, and whether the overall Skill set should be merged, split, simplified, replaced, or retired.
7. Apply all justified and authorized Skill and specification updates before completion. Prefer rewriting/removing obsolete guidance over adding layers of exceptions.
8. Apply the PR skill using the combined result. Complete a task only when its actual requirements pass, the Skill review is complete, and the authorized result is in the intended branch.

Report completed PRs separately from physical or operational blockers. Do not
close a failing proposal just because an alternative candidate works. If a new
user instruction arrives, incorporate it without dropping the earlier objective.
No skill or agent is assumed to keep running after a turn ends.
