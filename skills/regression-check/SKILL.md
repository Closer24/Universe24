---
name: regression-check
description: Compare Universe24 candidate or refactored behavior with recorded baselines and distinguish intended model changes from unintended regressions.
---

# Regression check

Read [the shared workflow](../workflow.md) and the regression expectations in
[test expectations](../../docs/TEST_EXPECTATIONS.md). Run independently or accept
an exact old/new tree and expected-change contract from Boss.

Select the smallest comparison that covers the changed behavior. Use identical
configurations, seeds, update counts and observation points. Compare physical
records, occupancy, active frontier and events when the contract promises exact
equivalence; final momentum or a similar-looking image is not enough.

The frozen source under `tests/reference/` is an independent oracle, never a file
to edit to obtain a pass. Keep its identity check and original projection contract
when schemas append fields. New state defaults need their own relevant evidence.
Reuse a matching frozen run for additional independent acceptance assertions
instead of executing the identical world again.

For an intentional new law, retain a separate model identity and report what is
expected to differ. An old known defect is evidence, not physical approval; a
different candidate's success cannot erase it. Do not claim that a finite frozen
fixture set makes every other correction mathematically impossible.

Use read-only source/trace comparisons and the existing Python tests. Output the
first divergent tick/state, whether it was expected, and the minimum reproduction.
Send unintended drift to the implementation owner and physical-contract changes
to the rule reviewer. Completion requires the promised compatibility checks to
pass, with unresolved differences explicitly handed back to Boss.
