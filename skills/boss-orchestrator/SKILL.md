---
name: boss-orchestrator
description: Coordinate Universe24 specialist agents, dependencies, completion evidence and PR integration for multi-part project work.
---

# Boss orchestration

Read [the shared workflow](../workflow.md). Own the user's complete objective,
task allocation and integration decisions; specialist logic stays in its skill.

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
| Unresolved blocker or unusual cross-component task | [special-tasks](../special-tasks/SKILL.md) | Root cause, focused candidate and independent acceptance evidence |

One agent may use multiple skills when no independent review is needed. Launch
agents only when delegation is authorized and independent tasks justify it.
Give implementation and required independent review to different owners where
practical. Do not create idle agents merely to match the table.

For an unresolved blocker, assign a separate special-task agent with a concrete
acceptance condition, exact source and owned files. Keep tests and physics review
independent from that agent's implementation. When concurrency is full, finish or
release a completed assignment before starting it; do not displace an active owner
silently. Track the blocker until independent checks establish its resolution.

## Sequence and finish

1. Read current repository instructions, open work and user scope. Record the
   base and identify conflicting files before assigning owners.
2. Define the acceptance target and handoff for each task. Resolve shared schema
   and interface dependencies before parallel changes build on them.
3. For physics changes, obtain the rule contract/review and coordinate tests,
   simulation and regression evidence. Checks may share identical run outputs.
4. Reconcile completed branches on current main. Route changed interfaces or
   behavior back to the affected specialist; do not restart unrelated checks.
5. Apply the PR skill using the combined result. Complete a task only when its
   actual requirements pass and the authorized result is in the intended branch.

Report completed PRs separately from physical or operational blockers. Do not
close a failing proposal just because an alternative candidate works. If a new
user instruction arrives, incorporate it without dropping the earlier objective.
No skill or agent is assumed to keep running after a turn ends.
