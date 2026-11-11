# Research proposals and retained evidence

The supported system is specified in [ONE_SYSTEM.md](../ONE_SYSTEM.md).
The entries below are mathematical proposals, restricted-sector results or
independent validation references. They are not selectable production
universes and none is an accepted general ≤48-channel Einstein model.
Historical results keep their original source revision and limitations.

| Work | Reference | Use in current research | Integration blocker |
| --- | --- | --- | --- |
| Projective sourced refinement | [Report](../TEAM48_REFINEMENT.md), `validation/geometry/team48/` | Actual 41/44-channel rational-step integer encoding; positive-frame invariant; sourced temporal and exploratory joint convergence evidence | General Einstein/spatial stability unestablished; several refinement groups fail; exponential integer bit growth; no apparatus. Same supported bundle/runtime only. |
| Integer ADM | [Derivation](../INTEGER_ADM.md), [baseline](https://github.com/Closer24/Universe24/tree/7d238e84a2167a4d3fe7bc7942da0cbf97bd29b2) | Independent coupled equation and geometric source reference | 4,771 Einstein channels plus historical communication; finite-horizon workspace. |
| Vacuum frame | [Frame48](../FRAME48_RESEARCH.md), [PR #36](https://github.com/Closer24/Universe24/pull/36) | Polynomial frame evolution and exact reversible lift | 48 channels consumed by vacuum alone; constraints, nondegeneracy and refinement unresolved. |
| Paired coupled frame | [PR #39](https://github.com/Closer24/Universe24/pull/39), [pinned derivation](https://github.com/Closer24/Universe24/blob/35344a1ba5c12c857404115e893911411ece7d35/docs/FRAME_MATTER.md) | Scalar/dust backreaction, stress signs and independent spacetime checks | 70 channels; constraint drift, refinement and stability; no apparatus. |
| Compact coupled frame | [PR #42](https://github.com/Closer24/Universe24/pull/42), [pinned report](https://github.com/Closer24/Universe24/blob/49b896c795203914a939e465d6d39e5b99343259/docs/TEAM48_RESEARCH.md) | Exact 70→36 physical-trajectory compression; 32/38/41-channel triangular coupled models; 44-channel positive-frame variant | Constraint drift, coefficient-integrality refinement barrier and computational temporal mode; no apparatus. Four remaining slots in the 44-channel allocation are not a detector. |
| Sourced homogeneous geometry | [Compact FLRW](../COMPACT_FLRW_CLOCKS.md), [PR #35](https://github.com/Closer24/Universe24/pull/35) | Exact sampling/refinement benchmark in a prepared symmetry sector | No arbitrary spatial geometry, streaming matter or detector dynamics. |
| Null geometry | [Compact null wave](../COMPACT_NULL_WAVE.md), [PR #34](https://github.com/Closer24/Universe24/pull/34) | Restricted geometry and strict-locality benchmark | Restricted profiles; not general sourced gravity. |
| Fixed-six reference | [Pinned source](https://github.com/Closer24/Universe24/blob/7d238e84a2167a4d3fe7bc7942da0cbf97bd29b2/universe24/layers/reference_model.py) | Mechanical fixture and scalar-oracle control | No established physical metric, apparatus or Born law. |
| Clock/click/Born/Bell/complexity audits | [PR #38](https://github.com/Closer24/Universe24/pull/38) | Negative controls and independent acceptance criteria | Audits identify missing coupling and physical laws; they do not supply them. |
| Local history and phase mechanisms | [PR #43](https://github.com/Closer24/Universe24/pull/43), [pinned synthesis](https://github.com/Closer24/Universe24/blob/3a02ade62f09db68e2c78d7b0eb7db8f88f81304/docs/COMPLEXITY_MECHANISMS.md) | 31-channel sensor/rotor with retained-history-dependent routing; phase/intensity checks | All 16 declared growth/persistence cases fail; no shared-metric apparatus or Born law. Adding it to 44 geometry/matter channels would require 75. |

At inspection on 2026-11-11, #38 and #43 remained open; #39 and #42 remained
open drafts. #42 reports passing CI for its pinned head. These are proposal
results, not claims that the branches are merged or that their historical test
counts apply to the current source.

The source-only adapter `validation/team48_contract.py` now imports #42's
pinned `charged_positive` tensor and complete first-sector staggered audit seed
through `create_bundle`, `run_bundle` and `verify_run`. It checks all 44 retained
channels against the pinned Engine and independent scalar oracle, including
nonzero remainders, without promoting a physical default. CI fetches only the
explicit source pin for this audit. See [the adapter contract and remaining
physical handoff](../ONE_SYSTEM.md#concrete-handoff-for-the-44-channel-law).

[Issue #41](https://github.com/Closer24/Universe24/issues/41) coordinates the
shared-metric apparatus proposal. Its older unbounded-allocation suggestion is
superseded by #40's cap. A complete apparatus allocation and independent clock,
transport, conservation and refinement evidence remain required.

A proposal can replace the physical construction only after review against
[issue #40](https://github.com/Closer24/Universe24/issues/40). It must use the
same execution interface, count every retained channel, include exact
seed/tensor/protocol provenance, disclose failed gates and supply independent
physical validation. An additional runtime switch or a metric/readout label
is not an integration argument.
