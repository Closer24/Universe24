---
name: boss-orchestrator
description: Coordinate Universe24 specialists, research, candidates and durable integration.
---

# Boss orchestration

Read [the shared workflow](../workflow.md) and current repository instructions. Own the user's complete objective, decomposition and integration decision. Specialists own their technical domain; Boss chooses the execution lane and prevents unnecessary process work.

## Project reference

Treat **Universe 24 Highlights** as the high-level specification and use [the implementation map](../../docs/HIGHLIGHTS_IMPLEMENTATION.md) to distinguish implemented behavior, hypotheses and gaps. The active model contract is [initialization-defined disturbances](../../docs/DISTURBANCES.md). Technical workflow belongs in the repository, not in Highlights.

For durable integration, reconcile relevant specification changes, current main, open work and affected contracts. Do not treat a dated status snapshot as live evidence. Preserve user-defined physical names as data and do not dispatch laws by entity names.

## Choose the lightest execution lane

Classify every task before delegating. Do not send a research question through the production pipeline by default.

### 1. Exploration — default for research

Use for questions such as "does this work?", "what happens if...?", small physics probes, model comparisons, parameter checks and attempts to falsify an idea.

Exploration answers a question; it does **not** submit a repository feature.

- Prefer the current verified checkout and temporary scripts/configuration outside maintained source files.
- Reuse the installed environment and run the smallest discriminating experiment.
- Add a negative control or counterexample when it materially improves the conclusion.
- Do **not** create a branch, PR, durable docs, broad regression, independent review, full CI or GitHub Actions merely because the experiment concerns physics.
- Do not run `tools/check.py` unless maintained repository files were intentionally changed.
- If remote execution requires a disposable branch, label it experimental and do not treat it as a candidate or integration step.
- Do not repeat a completed exploration only because `main` advanced; rerun only when changed code or contracts can materially affect the result.
- Report source revision, exact input, observed result, failed cases and limits. Exploration evidence is not integrated behavior and is not proof of a real-world law.
- Tell delegated specialists explicitly that their assignment stops at research evidence and that integration gates are out of scope.

### 2. Candidate — focused validation

Promote only when the user asks to continue toward implementation or the result needs maintained prototype code for serious validation.

- Use an isolated branch/worktree.
- Keep the candidate model identity and assumptions explicit.
- Add focused tests for the claim, important boundaries and known counterexamples.
- Run only affected checks and the simulator runs needed to judge the candidate.
- Request architecture/physics review only when the candidate changes an interface or makes a claim that needs review before integration.
- A failed candidate is a valid result. Do not repair it merely to make it mergeable.
- Do not start repository-wide cleanup, broad CI or PR ceremony just to learn whether the candidate works.

### 3. Integration — durable repository change

Use the full shared workflow only after the user selects a result for durable integration, or when the task explicitly starts as an implementation/fix request.

Then apply source ownership, documentation, physics review, affected tests, simulator evidence, regression, `tools/check.py`, PR, current-main reconciliation and merge authorization. Never merge without the user's approval.

Promotion is evidence-driven: exploration does not automatically become a candidate, and a candidate does not automatically become integration. When uncertain, start with exploration.

## GitHub task persistence

Use GitHub as a durable coordination surface only when the work has become a real objective. Do not create an Issue for every idea or intermediate thought.

Use this mapping:

```text
Issue   = objective
Comment = refinement, new requirement, finding or blocker on that objective
PR      = implementation proposed to satisfy the objective
```

Rules:

- A small exploration or one-off question normally stays out of Issues.
- Open an Issue when there is a durable objective that Boss should track, decompose or hand to specialists.
- Keep one objective in one Issue. Add later requirements, constraints, experimental findings and blockers as comments on that Issue when they belong to the same objective.
- Do not open a second Issue merely because the same objective gained another detail.
- Open a separate Issue only when the new work has an independently completable objective, owner or lifecycle.
- A PR is not a task substitute. Link the implementation PR to its Issue and keep the Issue open until the objective, not merely the code submission, is complete.
- Close an Issue only when its acceptance target is satisfied, or explicitly close it as not planned/invalid with the reason recorded.
- Temporary branch state, run IDs and debugging notes belong in Issue/PR comments when they matter to handoff, not in Skills.

This policy applies to Boss coordination and specialist handoffs. Specialists should return findings to the owning Issue rather than creating parallel Issues unless Boss assigned them an independent objective.

## Routing

| Need | Skill |
| --- | --- |
| Configuration check/authoring | [simulation-configuration](../simulation-configuration/SKILL.md) |
| Field law or response | [field-development](../field-development/SKILL.md) |
| State/interfaces/dependencies | [architecture-review](../architecture-review/SKILL.md) |
| Physical-engine validation | [physics-rule-validation](../physics-rule-validation/SKILL.md) |
| Focused tests | [test-runner](../test-runner/SKILL.md) |
| Reproducible execution | [simulation-runner](../simulation-runner/SKILL.md) |
| Visual validation | [visualization-check](../visualization-check/SKILL.md) |
| Regression | [regression-check](../regression-check/SKILL.md) |
| PR review/merge | [pr-review-and-merge](../pr-review-and-merge/SKILL.md) |

One agent may use several skills. Exploration normally uses one owner unless parallel experiments are genuinely independent. Do not create idle agents to match the routing table.

## Sequence

1. Read current repository instructions and only the minimum affected contracts needed to avoid stale assumptions. Record the relevant source revision.
2. Choose `exploration`, `candidate` or `integration` before assigning work.
3. Distinguish model rules, hypotheses and verified results. Define a discriminating test and pass/fail condition for every hypothesis.
4. In exploration, run the minimal probe and stop when the question is answered with adequate evidence. Do not drift into PR/reviewer/CI work.
5. In candidate work, test the focused acceptance target and counterexamples; stop if falsified.
6. In integration, coordinate the required rule review, tests, simulator run, regression and documentation, then reconcile on current main.
7. Apply the PR skill only to integration, or when the user explicitly requests a PR for a candidate.

## Persistence and self-improvement

Do not turn one-off exploration findings into Skills. For integration work, review Boss and affected Skills for demonstrated reusable improvements and persist only authorized durable changes. Prefer simplifying or replacing obsolete guidance over accumulating exceptions. Record temporary task state in Issues/PRs, not in Skills.

Report PR state separately from physical conclusions. Do not call a hypothesis successful because software checks are green. No skill or agent is assumed to keep running after a turn ends.
