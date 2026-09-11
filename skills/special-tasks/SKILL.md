---
name: special-tasks
description: Diagnose and resolve a bounded Universe24 blocker or unusual cross-component task assigned by Boss, with independent acceptance review.
---

# Special tasks

Read [the shared workflow](../workflow.md) and the current repository contracts.
Boss assigns this role to a separate agent when an unresolved failure or unusual
task needs focused investigation across normal ownership boundaries.

## Assignment

Before diagnosing a blocker, fetch and read the current
[Universe24 Highlights](https://docs.google.com/document/d/1IkhSyqZZMBSgbJV-PMMwcXG0D_Rlfg4FrLy2jXBMUSs/edit).
Record its revision and the applicable assumptions in the handoff. Compare them
with the implementation and repository contracts. Explicitly distinguish a model
hypothesis, an architectural requirement and a verified result. If the document
cannot be read, report that gap rather than claiming the assumptions are current.

Require an exact base commit, the failing behavior or desired result, existing
evidence, an acceptance condition and owned files. Read the current failure report;
do not assume that a remembered blocker still exists. Examples include moving
self-field response and same-tick contention between competing arrivals.

## Diagnose and solve

1. Reuse the smallest existing reproducer and trace the causal origin of its inputs.
2. State the root cause and distinguish an implementation defect from a missing
   or contradictory physical rule. Label a new hypothesis explicitly.
3. Coordinate shared interfaces with architecture and the affected field owner.
   Implement a focused candidate in an isolated worktree with one writer per file.
4. Preserve flux accounting, directional ratios and the applicable local-state,
   causal and bounded-integer contracts. Do not hide failures with special cases,
   weaker assertions, altered frozen references or global physical corrections.
5. Run only checks needed to evaluate the candidate. Reuse captured worlds and
   report results from the exact candidate commit. A failed hypothesis must leave
   its counterexample and useful findings available for the next attempt.

## Independent acceptance

Hand the patch, root cause, reproduced failure, expected correction and remaining
risks to Boss. The test owner independently verifies the acceptance condition;
the physics-rule owner reviews physical changes, and architecture reviews changed
interfaces. Reuse simulation and visual evidence when it covers the affected run.
The implementing special-task agent cannot approve its own physical correction
or merge it. Boss owns integration under the existing workflow and authorization.

If blocked, state the exact unresolved rule or missing evidence and the next
bounded investigation. A handoff is not a claim that the blocker was resolved.
