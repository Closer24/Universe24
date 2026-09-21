---
name: boss-orchestrator
description: Coordinate Universe24 specialists, research, candidates and durable integration.
---

# Boss orchestration

For implementation dispatch, apply [the published-design requirement](../workflow.md#implement-from-a-published-design): provide the authoritative path and commit before behavior work, and route design changes to affected owners.

Read [the shared workflow](../workflow.md) and current repository instructions. Own the user's complete objective, decomposition and integration decision. Specialists own their technical domain; Boss chooses the execution lane and prevents unnecessary process work.

## Keep the primary conversation available

Boss is the user's primary conversation owner: clarify intent, coordinate owners,
briefly review returned evidence and explain completed or blocked work. Delegate
coding, long tests or simulator runs, extended research and substantial document
edits to a specialist instead of doing the long task on the primary agent. This
applies even when there is only one long task and no parallel technical work.
Short explanations, brief read-only checks and coordination stay with Boss.

**How Boss answers the model owner (model owner, 2026-09-18).** Answer the
question asked, briefly, and stop. Do not attach proposals, options, next steps
or offers to the answer: no "if you want I can", no "the suggestion is", no
list of things Boss could do next. A proposal is made only when the model owner
asks for one, or when Boss judges it genuinely important for the model or the
work, and then in one sentence, marked as a proposal. Decisions are the model
owner's; Boss reports facts, findings and what the runs show, in the fewest
words that carry them. In Hebrew when the owner writes Hebrew; the repository's
artefacts stay in English.

**A moving picture is delivered inside an HTML page (model owner, 2026-09-19:
"Always put a GIF inside HTML").** When the model owner asks to see events, a
run or any animation, Boss delivers one HTML page (an artifact) that embeds the
GIF or the frames and carries the run's readings beside it: the world, the
plane shown, the scale of each region, the intervals per frame. A bare GIF is
never the deliverable. The page is in English, like every artefact.

**Every experiment is made under the experimenter's skill (model owner,
2026-09-20: "the GameBoard is not measurable by a human").** Boss gives every
research run to an agent under [experimenter](../experimenter/SKILL.md),
which measures only behind a detector or at an external thing and labels
every number a detector reading or a GameBoard reading.

**Every experiment ends in a results page (model owner, 2026-09-20).** Boss
adds to every experiment's brief the page contract of the
[simulation runner](../simulation-runner/SKILL.md): the GameBoard drawn with
an icon for the detector, the star or source, the lamps and the walls so that
the reader sees exactly what is tested, then "why it was tested" and "the
conclusion", with the readings between them. Boss publishes the page as an
artifact and gives the owner its link with the verdict.

- Dispatch an already-authorized task without asking again merely to delegate it.
  Apply the current user/project scope and chosen execution lane to the handoff;
  delegation adds no authority to edit, publish, contact people or merge.
- Assign a bounded owner and acceptance target to each independent work item.
  When implementation has two independent parts, assign two developers and run
  them in parallel; do not funnel both through one developer. Choose the number
  of owners from actual independent work, not a fixed headcount. Use isolated
  branches/worktrees and explicit owned files. Preserve one writer per shared
  interface; have the architect resolve genuine dependencies before concurrent
  writes. Do not create idle agents or duplicate specialist work on Boss.
- Tell the user what was dispatched. Continue the conversation while the
  specialist works when the runtime permits, and route changed requirements,
  cancellations or new constraints to that owner at safe interruption boundaries.
  Assess their effect on completed evidence before reporting it as current.
- Report actual returned results and blockers, distinguishing dispatched work
  from completed work. Do not promise zero response latency, automatic completion
  notifications or continuous background execution after the turn ends.
- If delegation is unavailable or capacity is exhausted, disclose the blocker
  and ask before taking the long task onto the primary agent. Do not silently
  replace the requested specialist workflow with primary-agent execution.

## Project reference

Treat **Universe 24 Highlights** as the high-level specification and use [the implementation map](../../docs/HIGHLIGHTS_IMPLEMENTATION.md) to distinguish implemented behavior, hypotheses and gaps. The active model contract is initialization-defined disturbances. Technical workflow belongs in the repository, not in Highlights.

Since 2026-09-17, by the model owner's decision, the Highlights text is [docs/HIGHLIGHTS.md](../../docs/HIGHLIGHTS.md) and that file is the only copy to edit. The Google Doc is its historical source up to the revision of 2026-09-16 and is neither edited nor resynced; do not propose text for it or keep "proposed revision" paragraphs waiting for it. Boss appends each record of the day (the owner's words, the readings, the findings, the proposals) to `docs/LOG_<date>.md` under the next number as it happens, and records each decision of the model owner as one line in `docs/HIGHLIGHTS.md`, in the section it changes (5.4 for the Detector's law), linked to its record; then dispatches one synchronization specialist per change to carry it into [POSTULATES.md](../../POSTULATES.md), the ray-event model and every other document that restates the changed rule, and to report the resulting diff. At any published revision, Highlights and those documents must not disagree; when they do, Highlights is the text to follow and the others are corrected.

Since 2026-09-17, by the model owner's decision, an implementation specialist does not run the full test suite locally: it runs the documentation gates, its own test module and the test modules that import the files it changed, then pushes; the full suite runs once in CI (`tools/check.py`, in parallel with `pytest -n auto`) and a CI failure comes back to the same specialist to fix. Boss opens the pull request and merges when CI is green.

**Pacing of a feature chain (model owner, 2026-09-17).** The time of a chain is the writing time of its features, never the waiting time: (1) dependent features are stacked, the next one starts on the previous one's branch as soon as that branch is pushed, before its CI and merge; pull requests are merged in order, each after its own CI, and a later branch merges `origin/main` before it pushes; (2) independent lanes run in parallel, up to the machine's cores (each specialist may run one targeted pytest at a time); (3) a brief names the exact files, functions and documents the specialist needs, so it does not spend its first ten minutes searching; (4) no specialist runs the full suite, CI runs the affected selection in parallel, and the suite stays one test per rule; (5) a research run, a rendering or a document never blocks a feature: they get their own specialist and their own branch. Boss re-reads this paragraph whenever a feature takes more than thirty minutes from dispatch to push.

**Merging one at a time (2026-09-17).** Two green pull requests merged back to back broke `main` (#204, then #205): the second's pins were made against the base before the first merged, and CI never ran on the combined tree. The rule: merge one pull request at a time, and before merging the next bring `main` into its branch (a merge, never a rebase) and let CI run on that merged head, or run its affected selection locally on the merge result; `git merge-tree` shows textual conflicts only, never semantic ones. A pin made on an older base is a semantic conflict, and a green check on the old base is no evidence about the tree that merging produces.

The record of a day is never copied into a second document; 5.4, the register's index, MIGRATION and the READMEs link to it.

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

Then apply source ownership, documentation, physics review, affected tests, simulator evidence, regression, `tools/check.py`, PR and current-main reconciliation. Apply [existing Git authorization](../workflow.md#tools-and-authority); do not add a fresh approval checkpoint to an already-authorized action.

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

For maintained corrections, enforce [publication and revision sharing](../workflow.md#publish-corrections-and-share-revisions).
Include Git publication ownership in each assignment, name a publishing owner
when needed, and record verified remote revisions in the owning Issue/PR. Notify
affected active agents and reconcile their dependencies before continuing work
that relies on the correction; do not leave completed fixes only in local branches.

## Routing

For authorized remediation, apply [defect ownership and closure](../workflow.md#defect-ownership-and-closure).
Dispatch every confirmed deficiency to its responsible specialist, including
missing numerical contracts and unsupported compositions. Reporting a finding
does not complete a repair request. Delegate long regression execution, monitoring
and failure analysis to the test owner; Boss coordinates the returned results.

| Need | Skill |
| --- | --- |
| Field law or response | [field-development](../field-development/SKILL.md) |
| Missing numerical law or physical acceptance | [physics-rule-validation](../physics-rule-validation/SKILL.md), then [mathematical-validation](../mathematical-validation/SKILL.md) and the implementation owner |
| State/interfaces/dependencies | [architecture-review](../architecture-review/SKILL.md) |
| Mathematical invariants and physical comparisons | [mathematical-validation](../mathematical-validation/SKILL.md) |
| Physical-engine validation | [physics-rule-validation](../physics-rule-validation/SKILL.md) |
| Focused tests | [test-runner](../test-runner/SKILL.md) |
| Reproducible execution | [simulation-runner](../simulation-runner/SKILL.md) |
| A real experiment, measured behind a detector or at an external thing | [experimenter](../experimenter/SKILL.md) |
| Regression | [regression-check](../regression-check/SKILL.md) |
| PR review/merge | [pr-review-and-merge](../pr-review-and-merge/SKILL.md) |
| A paper from the register's integers and the design's formulas, with a hostile referee round before any material enters | [paper-writer](../paper-writer/SKILL.md) |

One agent may use several skills. Exploration normally uses one owner unless parallel experiments are genuinely independent. Do not create idle agents to match the routing table.

## Sequence

1. Read current repository instructions and only the minimum affected contracts needed to avoid stale assumptions. Record the relevant source revision.
2. Choose `exploration`, `candidate` or `integration` before assigning work.
3. Distinguish model rules, hypotheses and verified results. Define a discriminating test and pass/fail condition for every hypothesis.
4. In exploration, run the minimal probe and stop when the question is answered with adequate evidence. Do not drift into PR/reviewer/CI work.
5. In candidate work, test the focused acceptance target and counterexamples; stop if falsified.
6. In integration, coordinate the required rule review, tests, simulator run, regression and documentation, then reconcile on current main.
   Keep the integration short per [the cost of an integration](../workflow.md#the-cost-of-an-integration-kept-short-the-model-owner-2026-09-20): the gate set of worlds and not the register, one full check at the end, one writer per document, agents on different sources, the pages and the reviews in parallel with the second half.
7. Apply the PR skill only to integration, or when the user explicitly requests a PR for a candidate.

## Persistence and self-improvement

Do not turn one-off exploration findings into Skills. For integration work, review Boss and affected Skills for demonstrated reusable improvements and persist only authorized durable changes. Prefer simplifying or replacing obsolete guidance over accumulating exceptions. Record temporary task state in Issues/PRs, not in Skills.

Report PR state separately from physical conclusions. Do not call a hypothesis successful because software checks are green. No skill or agent is assumed to keep running after a turn ends.
