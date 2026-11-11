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
| D — Convergence | Separate and joint space/time/quantization refinement at fixed physical domain and endpoint; stable constraints and valid geometry | Projective integer refinement is now constructive; general spatial convergence, stability and efficient bit growth remain unresolved. |
| E — Shared clocks and motion | Moving and stationary apparatus, null propagation and free fall using the same geometry; redshift/tidal and held-out controls | No accepted in-budget operational apparatus model. |
| F — Detector physics | Coupled source/apparatus interaction, complete trials, calibrated response, interference and separately justified Born/Bell statistics | No derived real-world detector law from the present Engine. |

Reports distinguish `passed`, `failed`, `partial`, `not_tested` and `blocked`. A code test
that confirms a known physical counterexample has passed as a regression test;
the physical gate that the counterexample refutes remains failed. Passing
schema/replay checks cannot set C–F to passed. Evidence must identify the seed,
tensor, protocol, source revision, raw results and domain of its claim.

## Results and limitations of inherited and concurrent proposals

The source-only [projective refinement follow-up](TEAM48_REFINEMENT.md) replaces
the sign phase with a retained denominator in 41/44 channels. It proves the
decoded update identity, supports rational physical time/space steps, and
retains the unchanged fixed-six Engine and bundle interface. The protected
cubic44 preparation has an exact positive-frame invariant with a vanishing
physical memory perturbation. Actual sourced homogeneous and plane-symmetric
tests show decreasing errors in specified refinement series. Several original
spatial/joint sequences fail their declared comparison test and remain in the
evidence. Integer bit length grows exponentially; no general physical gate or
apparatus default is promoted. The historical limitations below refer to their
original pinned laws, not to this changed projective integrator.

The baseline for this consolidation is commit
`7d238e84a2167a4d3fe7bc7942da0cbf97bd29b2`. Concurrent proposals #42 and #43
were inspected separately at the source pins below; their audit results are
not a claim that those branches have been merged into this execution package.

| Construction | Retained channels per node | Established result and limiting failure |
| --- | ---: | --- |
| Historical default ADM plus communication | 4,825 at its documented one-step setting | Coupled discretized scalar/dust gravity and exact replay; fails the cap and retains finite-horizon work. |
| Fixed-six reference control | 48 | Mechanical control; no demonstrated general Einstein or physical detector interpretation. |
| Frame48 | 48 | Exact repeated vacuum frame lift; no room in this allocation for matter/apparatus, and explicit constraint/degeneracy/refinement failures. |
| Compact null profile | 2 | Restricted prepared geometry; no general sourced dynamics or operational clocks. |
| Compact sourced FLRW | 8 | Exact prepared homogeneous polynomial sector and proper-time/affine counters; no general spatial dynamics or physical detector apparatus. |
| Coupled frame proposal #39 | 70 | Scalar/dust/frame backreaction and exact lift; exceeds cap in this older representation and retains constraint, refinement and stability failures. |
| Sign-compressed frame proposal #42 | 36 | Same 35 physical fields and both time slices as #39 through a proved phase encoding; different retained arrays and unchanged integrator limitations. |
| Triangular charged-frame proposal #42 | 41 | Geometry, charged scalar, Maxwell, squared dust and one computational phase; actual coupling within budget, but constraint/refinement failures and no apparatus. |
| Positive-frame proposal #42 | 44 | The coupled system with diagonal amplitude pairs and a proved positive-determinant sector; a computational temporal mode and explicit physical failures remain. |
| Joint history/sensor/rotor proposal #43 | 31 | Local retained history changes routing and message density; no shared-metric apparatus, and all 16 declared growth/persistence cases fail. |

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
trials and nondetection controls are necessary.

The newer [PR #42](https://github.com/Closer24/Universe24/pull/42), inspected at
`49b896c795203914a939e465d6d39e5b99343259`, resolves an important allocation
problem: one computational sign phase replaces the second explicit field bank.
The quadratic encoding compresses #39 from 70 to 36 channels while preserving
its physical trajectory; triangular gauge reduction then gives 32 scalar/dust,
38 independent-Maxwell and 41 charged-scalar/Maxwell channels. A separately
proved staggered phase assignment permits the cubic positive-frame variant
within 44 channels. These are substantive algebraic results, not merely a
new count for the old 48-channel vacuum allocation.

The 44-channel variant uses 23 geometric fields, 10 scalar fields, one signed
dust amplitude, six Maxwell fields, three spatial potentials and one phase.
Its massless tensor has 585 monomials; every channel retains `(a,b,r)`. The
remaining four slots are unallocated capacity, not an implemented detector or
physical clock. Positivity follows from nonzero discrete pair Wronskians;
exact continuum auxiliary time pairs have zero Wronskians, so the protecting
seed introduces a computational temporal mode. That mode can grow in a
contracting control. A separately constrained fixture has first-step
Hamiltonian residual 2624, momentum component 144 and torsion defect 4 while
the determinant stays positive. Raw joint steps 1/2, 1/4 and 1/8 fail integer
coefficient checks. Neither exact reversal nor determinant positivity resolves
these constraint, stability and refinement gates.

[PR #43](https://github.com/Closer24/Universe24/pull/43), inspected at
`3a02ade62f09db68e2c78d7b0eb7db8f88f81304`, demonstrates local-history-dependent
routing in a 31-channel composition. It reports 16 of 16 original
growth/persistence cases failing and no independent reference-board burst.
Its clock-phase intensity identities assume harmonic coupling; the tested
detector law remains `min(1,q/3)`, not exclusive Born sampling. Appending its
31 channels to the 44-channel frame would require 75 channels and is rejected
by the system cap; no such integration is made.

At inspection on 2026-11-11, #38 and #43 were open, and #39 and #42 were open
drafts. PR #42 reports CI passing at its pinned head. This establishes its
reported software/audit status, not accepted Einstein or detector physics.

## Remaining derivation, without adding another runtime

A physical replacement must fit the same bundle/Engine/decoder interfaces and
pass the same gates. The sign/staggered constructions in #42 now supply an
explicit fixed-allocation reversible encoding for coupled geometry and the
stated classical matter. The remaining derivation concerns a compatible,
stable and refinable physical update, constraints, readouts and actual apparatus.
The phase is synchronized computational state, not proper time. Its initial
uniformity and per-field phase offsets belong in the preparation certificate.

The frame equations remain a polynomial reference, but neither their component
count nor their low degree proves discrete constraint propagation. A changed
splitting or retimed construction must preserve the existing inverse and
single-edge contracts, account for scheduler/workspace, supply compatible
initial histories and demonstrate decreasing physical error at a fixed final
time. A purported nonlinear solution must keep the published H/M/torsion and
computational-mode controls instead of substituting continuum product rules
into discrete diagnostics.

### Concrete handoff for the 44-channel law

A **source-only research adapter is implemented** in
`validation/team48_contract.py`. It imports the pinned #42 law and seed into
this bundle/Engine/decoder pipeline; it adds no installed model selector.

```bash
# SOURCE is a clean checkout of the exact pinned #42 commit above.
python -m validation.team48_contract --source "$SOURCE" --out runs/team48-contract
python -m universe24 verify --run runs/team48-contract/run
```

The adapter checks the source commit and clean tracked bytes, then invokes an
isolated Python subprocess. It reproduces the first `(1,1)` phase sector from
`integer_staggered_audit.check_candidate`, including RNG 4439, diagonal-pair
initialization and every remainder draw. The preparation is an unconstrained
mechanical audit seed, not an Einstein continuum solution pair.

The imported law has **44 channels, 132 retained integer entries per node and
593 monomials** for `mass_squared=1`, `dt=dx=coupling=1` and zero cosmological
constant. The cited 585-term figure above belongs to the massless variant.
All 44 channel ownership records and the exact arithmetic decoder protocol
are sealed in the bundle. Three updates on 27 nodes are compared entry by
entry, including every remainder, with both the isolated proposal Engine and
its independent scalar oracle. The saved generic trace replays and rewinds
exactly. All emitted arithmetic clicks retain their audit labels; no physical
detection is inferred from their count or from the empty official stream.

CI checks out the explicit proposal commit solely for this compatibility
audit; its code is not installed with Universe24. Generated input, complete
trace, clicks and `integration.json` remain in the run evidence. Reported
physical failures are attributed to the pinned proposal; the adapter itself
does not rerun a physical convergence or apparatus study.

The passive `validation.team48_observables` reader now reconstructs the same
saved states into exact rational metric/link diagnostics, energy, momentum,
stress, electric charge/current and literal sampled constraint defects. It
checks the fixed source/phase/tensor identities and never supplies an Engine
input. An independent pinned oracle agrees on all 108 node snapshots of this
three-step audit. Charge conjugation preserves stress and reverses current in
the independent tests. The preparation's constraint defects grow strongly;
this is exposed in `validation.team48_board` rather than presented as Einstein
acceptance. The displayed curvature uses the retained frame connection and is
not yet an independent reconstruction from the metric.

The next physical handoff must supply compatible constrained temporal data,
controlled refinement and a shared-metric apparatus within the same budget.
Keep all phase-sector, nonzero-remainder, Wronskian and independent
constraint/torsion controls. A future proposal integration must preserve these
interfaces and cannot overwrite the mechanical report with an overall
physical success claim.

The shared-metric apparatus handoff belongs in
[issue #41](https://github.com/Closer24/Universe24/issues/41), subject to #40's
hard total cap. Issue #41's older suggestion not to promise a bounded channel
count does not relax that cap. A detector/clock proposal must reuse declared
coupled matter or prove a complete allocation in the four remaining slots,
including memory and any scheduler. It must compare independently generated
ticks and actual transported signals with the same metric, without importing
#43's separate 31-channel dynamics or an independent coframe. No accepted
apparatus implementation or complete physical solution is supplied here.

## Complexity, bursts and local selection

The owner's growth/selection objective is coordinated in
[issue #45](https://github.com/Closer24/Universe24/issues/45). A structural
complexity statistic and burst predicate must be declared before optimizing
or selecting results. Integer magnitude, elapsed time and an external log are
not substitutes for demonstrated structural novelty.

A deterministic reversible map on a finite state space has periodic orbits;
a fixed state function cannot strictly increase at every indefinitely recurring
burst on such an orbit. This does not rule out growth in Universe24's unbounded
integer state space. A proposal must specify whether it claims finite-window,
statistical or unbounded-trajectory growth and test that actual claim.

A global complexity score may be a passive diagnostic. Any complexity-based
choice that changes evolution must live in retained local state and the fixed
tensor, with influence propagated through face neighbors. All comparison,
memory and scheduling state counts toward 48. No runtime argmax, discarded
losing branch, hidden optimizer or relabeling of a density peak is introduced.
The #43 history/routing evidence narrows this task but does not establish the
requested growth between bursts. This gate remains open.

## Sources and reproduction

The mathematical source ledger and derivations are preserved in
[Frame48 research](FRAME48_RESEARCH.md), [integer ADM](INTEGER_ADM.md),
[compact FLRW](COMPACT_FLRW_CLOCKS.md), [compact null wave](COMPACT_NULL_WAVE.md),
the [coupled-frame proposal](https://github.com/Closer24/Universe24/blob/35344a1ba5c12c857404115e893911411ece7d35/docs/FRAME_MATTER.md),
the [compact coupled-frame report](https://github.com/Closer24/Universe24/blob/49b896c795203914a939e465d6d39e5b99343259/docs/TEAM48_RESEARCH.md)
and the [history/complexity proposal](https://github.com/Closer24/Universe24/blob/3a02ade62f09db68e2c78d7b0eb7db8f88f81304/docs/COMPLEXITY_MECHANISMS.md).
These documents distinguish cited continuum results from repository-specific
integer constructions. Their historical command lines describe their pinned
versions, not additional supported runtime modes in this release.

Run the current mechanical, bundle, decoder and runtime tests through the
repository test suite. Use the supported command's `--help` for bundle
execution and verification; retain every emitted report and its hashes under
`runs/`. Physical acceptance requires separate evidence for C–F, not merely a
green software test suite.
