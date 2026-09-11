---
name: regression-check
description: Check Universe24 current physical contracts for unintended changes using minimal reproductions and existing evidence.
---

# Regression check

Read [the shared workflow](../workflow.md) and the regression expectations in
[test expectations](../../docs/TEST_EXPECTATIONS.md). Run independently or accept
an exact old/new tree and expected-change contract from Boss.

Select the smallest comparison that covers the changed behavior. Use identical
configurations, seeds, update counts and observation points. Compare physical
records, occupancy, active frontier and events when the contract promises exact
equivalence; final momentum or a similar-looking image is not enough.

Historical API/frozen-v10 equality and older-Python compatibility are not required
gates. The source under `tests/reference/` remains an untouched archive. Use
current physical invariants and explicit numerical expectations; reuse an existing
world when it already exercises the required behavior. New state defaults need
evidence when their values affect a current contract.

For an intentional new law, retain a separate model identity and report what is
expected to differ. An old known defect is evidence, not physical approval; a
different candidate's success cannot erase it. Finite test fixtures do not prove
that every other correction is mathematically impossible.

Use read-only source/trace comparisons and the existing Python tests. Output the
first divergent tick/state, whether it was expected, and the minimum reproduction.
Send unintended drift to the implementation owner and physical-contract changes
to the rule reviewer. Completion requires the promised physical regression checks to
pass, with unresolved differences explicitly handed back to Boss.
