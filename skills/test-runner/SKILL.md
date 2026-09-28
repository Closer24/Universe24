---
name: test-runner
description: Run and maintain the minimum sufficient Universe24 test suite, diagnose failures and consolidate redundant coverage without weakening requirements.
---

# Necessary tests

Own delegated long checks through completion: run, monitor, inspect failures and
return evidence for the actual source revision. Route each failure under
[defect ownership and closure](../workflow.md#defect-ownership-and-closure) to
its component owner with a reproduction, then verify the correction. Reuse
completed evidence when its relevant source and inputs match; do not repeatedly
run an unchanged long suite or send Boss a sequence of waiting messages.

Apply [the published-design requirement](../workflow.md#implement-from-a-published-design): cite the design revision and derive independent acceptance cases from its contract. A mismatch is evidence to report, not permission to rewrite behavior or expectations.

Read [the shared workflow](../workflow.md) and
test expectations. Input is the changed
behavior/risk and exact tree; output is actual commands/results, retained coverage,
failure evidence, metadata and traces. Visual reports are optional output only
when visualization has been explicitly requested.

Choose tests for independent numerical outcomes, distinct bounds/errors,
component replacement, causal timing, local conservation and known regressions.
Do not add a test merely because a function was added, or derive the expected
answer by repeating the implementation. Do not add old-Python, historical API or
frozen-engine compatibility gates. Keep the archived frozen source untouched.

For a request to check an existing configuration, apply the
[configuration task scope](../workflow.md#configuration-tasks-and-implementation-scope)
and return the existing validator's report. The coverage work below applies when
implementing or changing validation software, not to a check-only request.

For configuration implementation work, follow the
preflight contract. Cover valid and invalid
inputs through their real entry points, explicit dependency failures, whole-profile
coverage and rejection before runtime/output creation. Keep semantic cases in the
format owner's tests and cross-entry consistency in adapter tests. Syntax success,
run completion and physical acceptance need separate assertions.

When reducing tests, map each removed assertion or parameter regime to retained
evidence before deletion. Combine identical model/config/seed/tick runs and keep
their useful assertions together. Preserve distinct low-rate, saturated, signed,
boundary and failure regimes when they exercise different behavior. Reduce actual
duplicate computation rather than hiding cases inside one counted test.

Run focused checks while resolving a concrete failure. For submission run the
existing `python tools/check.py` gate on the submitted version. Standard tests
are headless. Use `pytest --visualize-runs` and inspect visual artifacts only when
visual checks were requested; preserve physical assertions in ordinary tests.
Report pass/fail counts, not-run checks and the source tree. Reuse results
for an unchanged tree; do not repeat unrelated worlds merely for reassurance.

Local Git/Python and available CI log tools are sufficient. Changes to tests are
allowed within the assigned scope; changing physics or weakening a requirement is
not a way to fix a red gate. Keep original acceptance failures visible even when
a different candidate passes. Hand behavior failures to fields/architecture,
unexpected physical drift to physics-rule-validation, and the final evidence to the Closer's PR review.

## Notation (the owner, 2026-09-21, record 184)

Every symbol is named in English at its first use (never a Greek letter alone: "gamma (the Lorentz factor)"), and its kind is shown by its type: a scalar plain, a vector in bold lowercase (**p**), a tensor, matrix or operator in bold uppercase (**C**); skills/workflow.md, "Notation".

## The three tests of every rule (the owner, 2026-09-21, record 202)

A rule enters the law only if it is generic (one primitive with declared integers, no family name or kind), vector (one of the six verbs on the state vector, its rate at most bilinear, no root, no float) and local (its own record and the six neighbours, fixed work, nothing kept at a Node); state the three verdicts, one line each; skills/workflow.md, "The three tests of every rule".
