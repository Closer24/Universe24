# Research proposals and retained evidence

The supported system is specified in [ONE_SYSTEM.md](../ONE_SYSTEM.md).
The entries below are mathematical proposals, restricted-sector results or
independent validation references. They are not selectable production
universes and none is an accepted general ≤48-channel Einstein model.
Historical results keep their original source revision and limitations.

| Work | Reference | Use in current research | Integration blocker |
| --- | --- | --- | --- |
| Integer ADM | [Derivation](../INTEGER_ADM.md), [baseline](https://github.com/Closer24/Universe24/tree/7d238e84a2167a4d3fe7bc7942da0cbf97bd29b2) | Independent coupled equation and geometric source reference | 4,771 Einstein channels plus historical communication; finite-horizon workspace. |
| Vacuum frame | [Frame48](../FRAME48_RESEARCH.md), [PR #36](https://github.com/Closer24/Universe24/pull/36) | Polynomial frame evolution and exact reversible lift | 48 channels consumed by vacuum alone; constraints, nondegeneracy and refinement unresolved. |
| Coupled frame | [PR #39](https://github.com/Closer24/Universe24/pull/39), [pinned derivation](https://github.com/Closer24/Universe24/blob/35344a1ba5c12c857404115e893911411ece7d35/docs/FRAME_MATTER.md) | Scalar/dust backreaction, stress signs and independent spacetime checks | 70 channels; constraint drift, refinement and stability; no apparatus. |
| Sourced homogeneous geometry | [Compact FLRW](../COMPACT_FLRW_CLOCKS.md), [PR #35](https://github.com/Closer24/Universe24/pull/35) | Exact sampling/refinement benchmark in a prepared symmetry sector | No arbitrary spatial geometry, streaming matter or detector dynamics. |
| Null geometry | [Compact null wave](../COMPACT_NULL_WAVE.md), [PR #34](https://github.com/Closer24/Universe24/pull/34) | Restricted geometry and strict-locality benchmark | Restricted profiles; not general sourced gravity. |
| Fixed-six reference | [Pinned source](https://github.com/Closer24/Universe24/blob/7d238e84a2167a4d3fe7bc7942da0cbf97bd29b2/universe24/layers/reference_model.py) | Mechanical fixture and scalar-oracle control | No established physical metric, apparatus or Born law. |
| Clock/click/Born/Bell/complexity audits | [PR #38](https://github.com/Closer24/Universe24/pull/38) | Negative controls and independent acceptance criteria | Audits identify missing coupling and physical laws; they do not supply them. |

At inspection on 2026-11-11, #38 remained open and #39 remained an open draft.
The table does not assert that either branch has been merged or that its
historical test counts apply to the current source.

A proposal can replace the physical construction only after review against
[issue #40](https://github.com/Closer24/Universe24/issues/40). It must use the
same execution interface, count every retained channel, include exact
seed/tensor/protocol provenance, disclose failed gates and supply independent
physical validation. An additional runtime switch or a metric/readout label
is not an integration argument.
