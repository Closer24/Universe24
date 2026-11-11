# Universe24: one system, specification and research status

## Question and scope

Can one fixed, local integer tensor and a complete seed generate a reversible
spacetime dynamics with at most 48 retained channels per node, whose operational
clock and detector records agree with Einstein gravity and the stated matter
model?

This release consolidates the execution and evidence interfaces. It does not
supply an accepted general Einstein tensor within that budget. A compatible
bundle can be executed and checked without declaring its fields to be physical
geometry. Mechanical success and physical validation are separate results.
The coordination and acceptance contract is [issue #40](https://github.com/Closer24/Universe24/issues/40).

## Assumptions and exact law

A node retains at most 48 channels. Each channel contains its complete integer
triple `(a,b,r)`, with `0 <= r < 6`; consequently the cap permits at most 144
integer entries per node. Integers have unbounded bit length. Geometry, matter,
clock, detector, scheduler and workspace state all count. A recorded trace is
an output, never an additional state bank read during evolution.

For each channel, the immutable tensor evaluates an integer polynomial `u`
from the same complete old snapshot. The input degree is at most three. Every
monomial is supported on its target and at most one physical face edge;
old-`a` dependencies must be acyclic. The only evolution rule is

```text
ell, r_next = divmod(2*u + r, 6)
a_next = b
b_next = ell - a
```

No runtime numerical solve, hidden normalization, projection, clipping, external
forcing callback or trajectory lookup supplies a future state. The full state
is reversible. The passive click observation can discard information; this is
not a derivation of quantum collapse.

## Closed module interfaces

| Module | Inputs and outputs | Responsibility |
| --- | --- | --- |
| Construction and preparation | Declared model and initial data → tensor and complete seed | All coefficients, apparatus and calibration are fixed before execution; any initial-data solve is disclosed. |
| `system.bundle` | Tensor, seed, ownership and protocol → versioned, hashed bundle | Reject invalid integers, allocation above 48, locality violations, incompatible schema and corrupted components. |
| `core.engine` | Tensor plus complete old state → complete next state | Apply the unchanged fixed-six update; exact arbitrary-precision fallback and inverse. |
| `system.decoder` | Declared transition records → canonical arithmetic clicks | Passive extraction with event identity, node/channel/tick, quotient sign and C0/C1/C2 classification. |
| `system.runtime` | Valid bundle plus finite run request → trace, clicks and validation report | One execution/replay path; provenance and exact complete-state reconstruction. |
| Independent validation | Saved products plus reference calculation → scoped evidence | Never feeds back into evolution and never upgrades physical claims from mechanical tests. |

The dependency direction is preparation → bundle → Engine → transition records
→ decoder/readouts. Independent validation may inspect those products. No
observer is a state updater. There is one supported execution interface, not a
selector among ADM, FLRW, Frame48 and reference universes. Historical
constructors and independent equation checks are research/validation material.
Runnable audit harnesses live under `validation/`, including the historical ADM
reference in `validation/adm_reference.py` and controls in `validation/demos/`.
They are not installed product entry points and are catalogued in
[the proposal index](proposals/INDEX.md).

A bundle declares the model identity, version and supported domain, full channel
ownership, static protocol, complete tensor and complete seed. Integrity hashes
bind the components. The model declaration is provenance, not certification of
Einstein equations. Users cannot establish physics by calling a model
`Einstein` or changing a channel's label to `official`.

## Event and measurement definitions

An arithmetic click requires a nonzero quotient `ell = after.b + before.a` and
a changed retained triple under the existing Engine definition. The classes
are computed from `(r_next-r) mod 6`: C0 for 0 or 3, C1 for 1 or 2, and C2 for
4 or 5. These classes do not by themselves identify particles, spin outcomes,
Born probabilities or measured spacetime intervals.

The decoder operates on declared records. Complete replay uses all retained
information; the click stream need not determine that information. Event counts
and quotient weights are different observables. A future physical detector
must be represented in the retained budget, couple to the same accepted
geometry as matter and clocks, and expose a protocol that records no-detection
trials as well as detections. Postselected coincidences are not the full trial
population.

Physical lengths, angles, proper times and stress-energy must eventually have
one declared metric authority. A passive formula for proper time is not an
independently ticking apparatus. A computational face-neighbor causal bound is
not yet the physical null cone.

## Methods and acceptance gates

| Gate | Required evidence | Present interpretation |
| --- | --- | --- |
| A — Mechanical | Exact integers, immutable tensor, ≤48 channels, strict locality, complete forward/inverse replay, scalar oracle and causality controls | Checked for an actual bundle/run only; not a physical theorem. |
| B — Decoder | Online/offline equality, identity and class/sign checks, missing/duplicate/corrupt-record rejection, observer passivity and no-source controls | Arithmetic click semantics can be validated without assuming a detector model. |
| C — Einstein geometry | Independent four-metric curvature; vacuum and sourced cases; six evolution equations, four constraints, metric signature and matter conservation | No accepted general ≤48 coupled model. |
| D — Convergence | Separate and joint space/time/quantization refinement at fixed physical domain and endpoint; stable constraints and valid geometry | The compact general encoding has unresolved integrality, constraint and stability gates. |
| E — Shared clocks and motion | Moving and stationary apparatus, null propagation and free fall using the same geometry; redshift/tidal and held-out controls | No accepted in-budget operational apparatus model. |
| F — Detector physics | Coupled source/apparatus interaction, complete trials, calibrated response, interference and separately justified Born/Bell statistics | No derived real-world detector law from the present Engine. |

Reports distinguish `passed`, `failed`, `partial`, `not_tested` and `blocked`. A code test
that confirms a known physical counterexample has passed as a regression test;
the physical gate that the counterexample refutes remains failed. Passing
schema/replay checks cannot set C–F to passed. Evidence must identify the seed,
tensor, protocol, source revision, raw results and domain of its claim.

## Results and limitations of the inherited constructions

The baseline for this consolidation is commit
`7d238e84a2167a4d3fe7bc7942da0cbf97bd29b2`.

| Construction | Retained channels per node | Established result and limiting failure |
| --- | ---: | --- |
| Historical default ADM plus communication | 4,825 at its documented one-step setting | Coupled discretized scalar/dust gravity and exact replay; fails the cap and retains finite-horizon work. |
| Fixed-six reference control | 48 | Mechanical control; no demonstrated general Einstein or physical detector interpretation. |
| Frame48 | 48 | Exact repeated vacuum frame lift; no room in this allocation for matter/apparatus, and explicit constraint/degeneracy/refinement failures. |
| Compact null profile | 2 | Restricted prepared geometry; no general sourced dynamics or operational clocks. |
| Compact sourced FLRW | 8 | Exact prepared homogeneous polynomial sector and proper-time/affine counters; no general spatial dynamics or physical detector apparatus. |
| Coupled frame proposal #39 | 70 | Scalar/dust/frame backreaction and exact lift; exceeds cap before apparatus and retains constraint, refinement and stability failures. |

Frame48's two individually constrained time slices can evolve to Hamiltonian
residual 4. The coupled proposal records residual 34 for its corresponding
counterexample. These are limitations of those constructions, not a no-go
theorem for every possible integer model. The independent continuum checks and
restricted exact solutions remain useful references, but cannot be substituted
for a general in-budget derivation.

[PR #38](https://github.com/Closer24/Universe24/pull/38) is an independent audit
proposal. Its reported zero cross-owner couplings explain why merely combining
several components into one Engine does not produce one interacting physical
system. Its selected-click Bell result also illustrates why complete emission
trials and nondetection controls are necessary. At inspection on 2026-11-11,
#38 was open and #39 was an open draft; their results are proposal evidence,
not current-release integration claims.

## Remaining derivation, without adding another runtime

A physical replacement must fit the same bundle/Engine/decoder interfaces and
pass the same gates. The next mathematical work is an explicit reversible
encoding of coupled geometry, matter and apparatus that can be repeatedly
updated in a fixed allocation. Reusing `(a,b)` as two time slices is not by
itself a compression proof: the recurrence fixes `a_next=b`, and the proposed
first-order map must be shown to inhabit an invariant encoding under that
recurrence, including every remainder.

The frame equations provide a useful polynomial reference, but neither their
component count nor their low degree proves discrete constraint propagation.
A proposed splitting or retimed construction must budget its scheduler and
workspace, preserve invertibility and single-edge support, supply compatible
initial data and a refinable physical readout, then pass independent sourced
Einstein and apparatus tests. No such accepted construction is supplied here.
The consolidation makes these missing pieces explicit and testable; it does
not resolve them by renaming a control or weakening the 48-channel cap.

## Sources and reproduction

The mathematical source ledger and derivations are preserved in
[Frame48 research](FRAME48_RESEARCH.md), [integer ADM](INTEGER_ADM.md),
[compact FLRW](COMPACT_FLRW_CLOCKS.md), [compact null wave](COMPACT_NULL_WAVE.md)
and the [coupled-frame proposal](https://github.com/Closer24/Universe24/blob/35344a1ba5c12c857404115e893911411ece7d35/docs/FRAME_MATTER.md).
These documents distinguish cited continuum results from repository-specific
integer constructions. Their historical command lines describe their pinned
versions, not additional supported runtime modes in this release.

Run the current mechanical, bundle, decoder and runtime tests through the
repository test suite. Use the supported command's `--help` for bundle
execution and verification; retain every emitted report and its hashes under
`runs/`. Physical acceptance requires separate evidence for C–F, not merely a
green software test suite.
