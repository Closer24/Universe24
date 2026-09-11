---
name: boss-orchestrator
description: Coordinate Universe24 specialist agents, dependencies, completion evidence and PR integration for multi-part project work.
---

# Boss orchestration

Read [the shared workflow](../workflow.md). Own the user's complete objective,
task allocation and integration decisions; specialist logic stays in its skill.

## Persistent project reference

Treat **Universe 24 Highlights** as the high-level project specification:
https://docs.google.com/document/d/1IkhSyqZZMBSgbJV-PMMwcXG0D_Rlfg4FrLy2jXBMUSs/edit

At the start of relevant work, reconcile the applicable project rules and hypotheses with this document. When the user changes a durable project rule, update the relevant repository Skill(s) as part of the same work when authorized, so the rule does not depend on chat history.

Keep three states distinct:
- **Model rule** — a rule currently defining the simulator.
- **Hypothesis to test** — an unverified proposal with a test and pass condition.
- **Verified result** — a result supported by a completed defined test.

Never promote a hypothesis to a verified result because it sounds plausible or because an implementation exists. The Focus algorithm is a hypothesis to test until its defined tests pass.

## Mandatory persistence review for every task

Every task must include a persistence review before it is considered complete.

1. Ask which participating agent Skills learned a durable rule, procedure, invariant, failure mode, test requirement, handoff contract, or project convention from the task.
2. Inspect every affected Skill, not only the Boss Skill.
3. If future work by that agent would be improved or corrected by retaining the lesson, update that agent's Skill in the same task.
4. If a lesson applies to several agents, update every relevant Skill or place the shared rule in an authoritative shared reference and make each affected Skill point to it.
5. Do not copy temporary debugging details, one-off outputs, branch names, or transient implementation state into Skills.
6. Keep durable project physics/specification knowledge synchronized with Universe 24 Highlights as well as the relevant Skills.
7. Record the Skill updates in the repository so the behavior can be reconstructed even if all chat history is unavailable.
8. A task is not complete until the persistence review has either produced the required Skill updates or explicitly concluded that no Skill change is needed.

The goal is persistent operational knowledge, not duplication. Skills should remain small, authoritative, and scoped to the agents that need the rule.

## Route the work

| Need | Skill | Expected handoff |
| --- | --- | --- |
| Field law or response implementation | [field-development](../field-development/SKILL.md) | Explicit candidate contract and focused change |
| State, interfaces or dependency boundaries | [architecture-review](../architecture-review/SKILL.md) | Compatible ownership/schema assessment |
| Any physical-engine behavior change | [physics-rule-validation](../physics-rule-validation/SKILL.md) | Rule-by-rule acceptance or concrete blockers |
| Necessary tests, failures or redundant coverage | [test-runner](../test-runner/SKILL.md) | Minimal sufficient checks and actual results |
| Reproducible world execution | [simulation-runner](../simulation-runner/SKILL.md) | Identified run, trace and HTML evidence |
| Rendering or visual interpretation | [visualization-check](../visualization-check/SKILL.md) | Faithful, inspected output |
| Compatibility with an earlier result | [regression-check](../regression-check/SKILL.md) | Independent baseline comparison |
| Review, reconcile, close or merge PRs | [pr-review-and-merge](../pr-review-and-merge/SKILL.md) | Current-head integration decision |

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
6. Run the mandatory persistence review across every participating/affected Skill. Apply all durable Skill and specification updates before completion.
7. Apply the PR skill using the combined result. Complete a task only when its actual requirements pass, persistence review is complete, and the authorized result is in the intended branch.

Report completed PRs separately from physical or operational blockers. Do not
close a failing proposal just because an alternative candidate works. If a new
user instruction arrives, incorporate it without dropping the earlier objective.
No skill or agent is assumed to keep running after a turn ends.
