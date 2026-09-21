---
name: pr-review-and-merge
description: Reconcile and review Universe24 PRs against current main, verify required evidence, and perform authorized merges or already-integrated closures.
---

# PR review and merge

Read [the shared workflow](../workflow.md), [AGENTS.md](../../AGENTS.md), and the
Git workflow in [CONTRIBUTING.md](../../CONTRIBUTING.md).
Input is the PR, current head/base, user authorization
and specialist handoffs; output is an evidence-backed merge, closure or blocker.
Use local Git and the available connected GitHub tools.

Apply [standing Git publication authorization](../workflow.md#tools-and-authority).
Publish requested corrections and Skill updates without a new approval prompt.
Verify merge scope and required gates using existing authorization; do not treat
publication or green software checks as closure of unresolved physical findings.

When assigned as Git publishing owner, apply [publication and revision sharing](../workflow.md#publish-corrections-and-share-revisions).
Accept an explicit specialist handoff, publish the exact scoped revision, keep
pending review or validation visible in a draft PR, and verify its remote head
and contents. Return canonical links and SHAs to Boss for dependent-agent handoffs.

Check that the PR identifies affected contracts, providers, consumers, tests and
documentation. Reconcile those changes as one unit. Refresh the restart snapshot
when integration changes a fact it records, without copying the entire PR history.

Read the current PR/diff and main. Identify missing functionality, overlapping
branches and stale test results before resolving conflicts. Preserve newer code,
English documentation, model identity and all retained requirements. For a
superseded PR, reconcile every changed feature/file before closing it as already
included; an open state alone does not mean its code is missing.

For physics-engine behavior changes require independent physics-rule review,
necessary tests, affected simulation evidence and regression checks. Architecture
and visual reviews cover changed interfaces/output. A green CI is not proof that
an acknowledged physical acceptance failure was fixed.

Verify the submitted source and required CI results; distinguish actual logs from
author claims. If main advanced, inspect the prospective combined tree and recheck
affected risks. Record exact tree equality when reusing existing verification.
Inspect diff-check, file list and unintended/generated files before publishing.

Merge only with existing user authorization and passing required gates, using an
expected-head guard when available. Do not force-push shared branches, bypass a
failed check, or close a genuinely unfinished physical proposal to clear the list.
Preserve current work when refreshing a branch. Verify the resulting main commit
and PR state, then hand Boss the merged/closed items, tested evidence and remaining
blockers. This skill does not provide authorization for unrelated messages or
repository administration.

## Notation (the owner, 2026-09-21, record 184)

Every symbol is named in English at its first use (never a Greek letter alone: "gamma (the Lorentz factor)"), and its kind is shown by its type: a scalar plain, a vector in bold lowercase (**p**), a tensor, matrix or operator in bold uppercase (**C**); skills/workflow.md, "Notation".
