---
name: test-runner
description: Run and maintain the minimum sufficient Universe24 test suite, diagnose failures and consolidate redundant coverage without weakening requirements.
---

# Necessary tests

Apply [the published-design requirement](../workflow.md#implement-from-a-published-design): cite the design revision and derive independent acceptance cases from its contract. A mismatch is evidence to report, not permission to rewrite behavior or expectations.

Read [the shared workflow](../workflow.md) and
[test expectations](../../docs/TEST_EXPECTATIONS.md). Input is the changed
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
[preflight contract](../../docs/CONFIGURATION_VALIDATION.md). Cover valid and invalid
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
unexpected physical drift to regression-check, and the final evidence to Boss/PR review.
