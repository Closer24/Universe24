# Universe24: one system, specification and research status

## Installed native light component

`universe24/light.py` belongs to the installed main package. The supported
`python -m universe24 prepare-light` command constructs one complete bundle;
existing `run` and `verify` perform all evolution and replay. This is a
preparation entry point, not another Engine, mode or callback.

All 48 channels have a fixed one-face transport polynomial. With quaternion
label g, define n_g=R_g e_x, e_g=R_g e_y and m_g=R_g e_z. The input is
u_g(x)=3[b_g(x-n_g)+b_g(x+n_g)]. There are 96 linear integer monomials,
no old-a dependencies, no idle padding and 144 retained integers per node.
The exact candidate contract `2O-left-regular-cube/1` passes on the entire
polynomial, including the central group element and all three retained banks.
The bundle declares `role=universe-candidate` and the checked symmetry.

Preparation sets a_g(x)=b_g(x+n_g). With arbitrary retained remainders in
0…5, unchanged Rule3 gives b_next,g(x)=b_g(x-n_g) and r_next=r at every tick.
The relation is invariant for unlimited integer time: no finite-precision
preparation scale, reset or external updater is used. For the prepared
transverse plane profiles, E=sum_g e_g b_g and B=sum_g m_g b_g are passive
vector readouts of flat axis-aligned Maxwell waves. Coordinate units h=dt=1
give exact null displacement. This does not derive a material clock.

The component supplies six signed propagation axes and two physical transverse
polarizations per axis. It is not arbitrary-direction Maxwell convergence,
dynamic Einstein backreaction, an operational detector or a quantum photon
model. Full physical acceptance remains blocked despite algebraic candidate
acceptance. Raw clicks are still arithmetic records.

[Component documentation](research/light_packet/README.md) preserves the
original 18-channel optical experiment, pinned to e582960, separately. Its
speed errors, finite-grid tails and identical-background click maps are not
results of this new tensor. Historical bytes are not relabeled. Core tests
cover the installed input/output and algebra contracts. The passive observer
`validation/light_runtime.py` inspects saved schema-3 light runs; the archived
central research collector is not a supported schema-3 execution path.

## Reviewed execution and acceptance

The current-schema [light/link resonance audit](research/light_link_resonance/README.md)
tests restoring motion and optical coupling without changing the installed
light component. It constructs exact 48-channel, 2O-covariant research
tensors in the existing saved-run interface. A homogeneous central-contrast
oscillator can be completely invisible to light. A matched-phase cubic
control gives exact alternating move/hold plane transport with positive
integer histories; nonuniform clock and reciprocal-source controls retain
their failures. This restricted transport construction is not a measured
shared edge length, an operational clock or dynamic Einstein geometry.
No channel ownership or installed interface is added: central-pair sums and
contrasts are passive readouts of the existing 144 retained integers.

The installed `universe24/detection.py` adds a prepared 48-channel light/memory
exchange law through `prepare-detector`, followed by the same `run` and `verify`.
Its 624 quadratic-or-linear monomials pass mandatory 2O covariance and strict
one-face support. The retained selector and counterpropagating arming pulse
are complete input state. A captured amplitude is stored locally and is
released when the arming pulse revisits; the exact quadratic excitation
account is conserved. The passive `detect` command reads capture, release,
exchange and no-transfer records after full replay. It does not relabel raw
arithmetic clicks as photons. [The detector contract](DETECTOR.md) specifies
the polynomial, allocation, invariant sector, finite memory lifetime and open
quantization, clock, recoil and Born gates. No physical default is introduced.

**Current admission boundary:** bundle schema 3 requires 48 explicitly supplied
node channels and exact 2O covariance for every model. There is no research
exemption or automatic padding. Research constructions and commands documented
below record the pre-schema-3 snapshot at commit
`e281f7e7b251641a741d185116656fedaa5396f8`; their smaller or non-equivariant
bundles cannot execute through the current supported runtime. Historical
receipts remain evidence of their original source version.

The installed interface remains `python -m universe24`, with one fixed Rule3
Engine, one saved-bundle runtime and one passive canonical decoder. The
source-only command `python -m validation.system_acceptance --out NEW_DIRECTORY`
executes a fixed evidence sequence through that runtime. It is not a physical
model selector and does not combine different laws into one certificate.

The complete disposition of retained ideas is
`docs/research/system_acceptance/idea_ledger.md`; independent architecture
review, physical-domain limits, the massive-encoding attempt and exhaustive
burst/growth evidence are in the same directory. Current algebra is
`docs/MODEL.md`. All saved receipts bind the complete seed, tensor, model,
protocol, horizon, trace, observations and repository-owned Python sources.
The collector rejects source changes during execution and requires fresh
output, preserving historical evidence.

Two distinct six-channel constructions now satisfy restricted physical gates:
the native massless scalar/dust law gives exact sourced homogeneous sampling;
the massive spinor law gives an exact decoded constraint and a finite-time
convergence theorem on its prepared expanding domain. Neither repairs or
inherits the old massive45 trajectory. The eight-channel massless Bianchi I
extension adds conserved shear, a shared anisotropic metric and a source-based
comoving proper-time invariant. Its moving probes remain passive diagnostics;
its homogeneous acceptance does not extend to spatial momentum closure.
General spatial geometry, operational
apparatus, a justified Born measure and a joint recurrent-burst/complexity
model remain unestablished. The generic runtime therefore retains blocked
general physical acceptance and no default physical model.

The repeated-activity search keeps one existing Boolean selector tensor and
enumerates its complete ring domain. Recurrent event peaks are present,
while no preparation passes the unchanged sustained structural-growth gate.
For the separate massless homogeneous Einstein source, positive dust/scalar matter
implies decreasing density and deceleration, excluding a bounce within that
declared model. Neither result is relabeled as cosmological completion.

The [central source ledger](research/central_integration/README.md) connects
the board, completion, node-clock and retained-apparatus sources. The executable
`validation.integration_contract.massive45` gate proves their shared massive45
builder/state identity while retaining the first-step and tick-two constraint
failures. This source integration changes no production law or physical status.

## Question and scope

### Mandatory algebra contract

Every supported model must pass exact coefficient covariance under all 48
joint channel/cube actions of `2O-left-regular-cube/1`, at preparation, save,
load and execution boundaries. Roles are descriptive only: `research`,
`universe-candidate` and an omitted role all face the same check. Omitted
symmetry selects the mandatory action; explicit null or an unknown action
fails. The action permutes all of `(a,b,r)` and uses one regular orbit of 48
node channels with invariant passive labels. No invariant seed is required.
This algebra certificate is not physical acceptance. See
[the exact action and limitations](COUPLING_ALGEBRA.md).

The automated suite and CI cover engine, tensor algebra and supported
input/output contracts only: exact arithmetic, scalar-oracle agreement,
locality, invertibility, 48-channel allocation, mandatory 2O covariance,
ownership, decoding and complete saved-run replay. Research unit tests and
research CI jobs are removed. The source research programs and their saved
historical evidence remain available, but their physical claims are not
revalidated by the current CI. Ordinary unittest discovery runs the whole
remaining suite; there is no extra suite selector.

### Physical target

Can one fixed, local integer tensor and a complete seed generate a reversible
spacetime dynamics with at most 48 retained channels per node, whose operational
clock and detector records agree with Einstein gravity and the stated matter
model?

This release consolidates the execution and evidence interfaces. It does not
supply an accepted general Einstein tensor within that budget. A compatible
bundle can be executed and checked without declaring its fields to be physical
geometry. Mechanical success and physical validation are separate results.
The coordination and acceptance contract is [issue #40](https://github.com/Closer24/Universe24/issues/40).

The source-only [sourced complete-history map](research/sourced_map/README.md)
implements an exact sampled expanding homogeneous massless-scalar plus dust
FLRW solution in six retained channels. Its physical constraint includes both
volume histories; one immutable linear tensor preserves that constraint and
all carries. The existing runtime saves and verifies these research bundles.
Passive root/log field reconstruction is explicitly bound to the physical
coordinate chart and is distinct from canonical arithmetic clicks. This is a
different research tensor from massive45; massive, spatial and operational
clock extensions remain open. General physical gates and the default model
are unchanged. The construction is tracked in [issue #58](https://github.com/Closer24/Universe24/issues/58).

The [six-researcher conservation continuation](research/conservation_closure/README.md)
extends that exact native massless sector to diagonal anisotropic Bianchi I in
eight retained channels. Conserved mixed shear density, scalar momentum and
dust charge join one complete-history constraint and one independently derived
metric/source. All16 Einstein-component identities hold on the declared
homogeneous domain. Conservation plus proper-time midpoint kinematics and a
positive branch uniquely selects this restricted exact map; conservation alone
does not select a physical law. Actual4096-step execution, scalar oracles and
rewind use at most26 bits, with a logarithmic retained-bit theorem.

A source-clock invariant reads elapsed comoving proper time from the volume
history and dust; moving covector/geodesic calculations remain passive probes.
Arithmetic clicks, scalar values and operational detector records are distinct.
A separate face-interaction tensor proves carry-aware local continuity, while
a nonhomogeneous same-Bianchi-tensor negative preserves local Hamiltonian
constraints and violates momentum constraints. General spatial dynamics,
operational detectors and efficient massive-source encoding remain open.
The massive spinor result below is preserved as a different physical model.
No default, Engine or installed-runtime change is introduced. Reproduce the
six joined audits with `python -m validation.conservation_closure.run_all`.

The source-only [node, clock and Einstein audit](research/einstein_node/README.md)
separates identities of every valid Rule3 tensor from physical properties of a
selected law. It adds exact clock-geometry and host-workload countercontrols,
independently reproduces the published scalar/Maxwell common kinetic metric,
and specifies a still-untested transported-field/phase experiment. No runtime
model or physical acceptance gate is changed by that investigation.
The source-only [generic interaction and proof structure](research/generic_structure/README.md)
adds a reusable reciprocal-interaction compiler, counted native schedule,
complete-history constraint examples, an exact homogeneous-sector extractor
and a restricted massive packet/phase control. The packet uses a distinct
three-channel linear law, not the common45 Einstein candidate. These are
scoped constructions and falsifiers; no production law, physical gate or
operational-clock interpretation is promoted by their mechanical success.

## Assumptions and exact law

Every supported prepared bundle retains exactly 48 channels per node. Each
channel contains its complete integer triple `(a,b,r)`, with `0 <= r < 6`,
so every node retains exactly 144 integer entries. Integers have unbounded bit length. Geometry, matter,
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
| `system.bundle` | Tensor, seed, ownership and protocol → versioned, hashed bundle | Require exactly 48 explicit channels and exact 2O covariance; reject invalid integers, locality violations, incompatible schema and corrupted components. |
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

### One saved massive45 run and geodesic board

The [integrated geodesic-board report](research/geodesic_board/README.md)
connects the corrected full-frame, explicitly massive 45-channel tensor to the
existing bundle/runtime, saved metric, homogeneous geodesic readout and offline
board. Run `python -m validation.geodesic_board --out runs/geodesic-board`.
All retained dynamics still use the unchanged Engine. The readout adds zero
retained channels and cannot feed the Engine. Older #47–#50 source proposals
are consolidated as validation evidence; they are not concatenated into this
tensor or installed as competing physical models.

The finite default run has 889 quadratic terms, 27 nodes and four updates.
Independent complete-state replay and scalar-oracle checks accompany a
continuum-derived first-step counterexample: from the constrained massive
FLRW seed, the Hamiltonian residual becomes exactly `-7*dt**2`. The flat
control remains zero, and the massless control gives `-3*dt**2`. Therefore
continuum constraint additions and flat-symbol hyperbolicity do not by
themselves repair this temporal discretization. Refinement evidence is limited
to the stated homogeneous finite-time family, with explicit integer bit cost.

Null/timelike curves use conserved spatial momenta in the same saved homogeneous
metric with lapse one and shift zero. Floating quadrature is confined to passive
readout, independently checked against analytic flat and expanding controls.
It is not operational motion or an extra source inside the tensor. Clock
intensity/phase and complete-trial quantum controls retain their failed or
unimplemented physical gates. General acceptance C–F remains open.

### Eight-review algebra and formulation follow-up

The source-only [eight-review report](research_eight/README.md) investigates
the two remaining #47 costs and the underlying evolution formulation. It
proves the current positive projective denominator's exponential bit-length
lower bound, records exact shifted-product/native-lattice identities, and
adds executable positive and negative controls. None is an installed model.

An exact principal-symbol audit of the actual full and triangular frame RHS
finds off-constraint Jordan chains around flat space. A separately compiled
full-frame constraint-added proposal has a square-free all-direction flat
principal-symbol identity and fits the stated matter in **45 projective
channels**. This is a new research law, not an equivalence assertion about
the old off-constraint trajectories. Its three-step complete-state audit
does not establish nonlinear constraint propagation, general metric
positivity, stable time discretization or efficient integer growth; the old
projective denominator cost remains. The triangular protected44 determinant
proof cannot be transferred to this full-frame allocation.

Native Rule3 coordinates expose an alternative denominator-free kick/drift
search space without adding retained state. Generic nonseparable kinetics,
rational refinement and a budgeted multi-tick compiler remain unimplemented.
The matter clock work establishes a gauge-invariant diagnostic port and
global phase-equivariance checks, not operational proper-clock or click-only
acceptance. General gates C–F remain open.

Run `python -m validation.research_eight.run_all` for the eight independent
audits. Fresh logs, source hashes and expected physical failures remain in
`runs/research_eight/`. The complete proposal and its precise domains are
coordinated in #40, with apparatus-specific results in #41.
The follow-up [integration synthesis](research/synthesis/08-interface-synthesis.md)
connects the projective refinement proposal to held-out geometry, exact bit-growth,
gauge/readout, reversible comparison, compatible-identity and reciprocal-matter
controls. These are source-only research programs, not additional installed
universes or a concatenated physical tensor. Their independently reproduced
successes and failures are retained; no acceptance gate is promoted by their
execution. Run `python -m validation.synthesis.run_all --out runs/synthesis`.
### Clock-link observer follow-up

[The staged clock/observer plan](CLOCK_LINK_OBSERVER_PLAN.md) implements a
source-only construction on the pinned 44-channel bundle: four retained
local/face coherent-intensity responses bring its total to 48. It uses the
same Engine, complete trace, ownership ledger and canonical decoder. The
added polynomial inputs are `u=3F`, with `F=|z|²` or a coherent face sum,
so `ell=F` and each remainder is retained. The complete source44 projection
is unchanged; this is one-way test apparatus, without supplied stress or
backreaction, proper-time calibration or local gauge-covariant transport.

The construction is a model change for the additional retained responses,
not a default physical model. History-sensitive event suppression and exact
interference records pass. Binary Born frequencies fail; there is no
apparatus-to-carrier selection or recurrent structural-growth evidence.
The combined audit preserves these failures and rejects mixed run/source
identities. See the plan for the next reciprocal-interaction, pointer,
probability-measure and shared-metric acceptance sequence.

The [November eight-researcher continuation](completion/README.md) supplies a
shared **massive full45** builder, complete seed and ordinary system-bundle
handoff for clock/stress and signal/metric observations. Its exact tensor and
seed identity closes the earlier massless-full45 versus massive-triangular44
handoff gap. The continuum principal certificate now covers arbitrary
invertible frames and matter backgrounds; continuous linear constraint
propagation is proved along a homogeneous massive scalar/dust family.

Three distinct constructions must remain separate. The original projective
time map has a proved wave-CFL instability and a constrained metric-singularity
counterexample. A cubic full45 modification preserves full-frame
nondegeneracy for every finite tick on its prepared memory domain, but adds a
verified finite-h torsion defect and retains exponential bit growth. A separate
three-channel native linear-wave tensor uses the unchanged fixed-six carries,
has a uniform Fourier bound, and converges at fixed physical time with
logarithmic per-integer bit cost. It has not been compiled into the nonlinear
coupled full45 system. Native nonlinear arithmetic and a reduced sourced
constraint target provide further building blocks, with their retained-history
and workspace limitations explicitly tested.

The massive clock audit now includes an actual sampled oscillation on a
separately fingerprinted coarse-step tensor. Its Hamiltonian defect remains
nonzero, and its fourteen-step cost reaches 174,385 bits. The exact phase
formula includes an expansion correction; phase divided by mass is not a
universal proper-time reading. Same-metric characteristic cones and conditional
geodesic oracles do not establish moving material packets or an operational
detector. No general physical gate is promoted by these results.

Run `python -m validation.completion.run_all` for the shared runtime handoff,
eight research audits and independent cross-law review. Fresh evidence belongs
under `runs/completion/`; the published integration evidence is
`docs/evidence/completion_nov12.json`. The unchanged Engine, one supported
runtime and unresolved general physical acceptance remain part of this contract.
### Retained preference and reciprocal apparatus follow-up

[The eight-lane construction](RETAINED_SELECTION_PLAN.md) supplies a prepared
three-channel reversible Boolean carrier with local preferred-port routing
and retained origin memory. If `F` is the local collision plus one streamed
lane, `u=3(F(b)+F^-1(b))` and complete preparation `a=F^-1(b)` make unchanged
Rule3 follow `F` exactly, including every remainder. This is a native research
control. It is not a physical encoding of the earlier 44-channel carrier.

A separate corrected full-frame45 source, pinned to PR50
`62202fdccdd9a40d5dbbec104de6f97d9587a999`, gains neutral `q,p` for 47 channels.
The declared massive carrier uses `W=omega²*q²/2+g*q*(phi²+chi²)`, reciprocal
forces, `rho_app=p²/2+W`, isotropic pressure `p²/2-W`, diagonal K source `-W`
and Hamiltonian source `-2*rho_app`. Its homogeneous energy exchange cancels
exactly at the continuum equation level. This cubic construction leaves one
record slot. It has globally unbounded interaction energy, finite-step
constraint drift and no general spatial apparatus momentum completion.

Actual48 raw-record feedback changes later carrier positions and, on the
declared textured fixture, normalized fixed-gauge phase links. Matched
homogeneous controls preserve their phase despite amplitude response.
The raw record has no supplied stress or continuum calibration; that48 result
cannot inherit the47 homogeneous conservation identity. The native sorter,
native pulse pointer, sourced47 and raw-feedback48 have separate model/seed
identities through the same runtime, not interchangeable physical claims.

All 36 declared native growth cases fail or lack enough episodes. Conditional
exclusive routing is proved for single occupancy, but the unrestricted pointer
retains double outcomes. Distinct stationary one-particle ensembles give
different output measures. Born probabilities, physical Bell outcomes,
shared-metric clocks and growing complexity between physical bursts remain
unestablished. The joint runner checks shared truth tables, exact47-to48 bundle
lineage, report/source hashes and independent replay of all19 saved runs;
complete measure-control trials retain another4,080 transitions.

The [seven-researcher unified-law continuation](research/unified_law/README.md)
adds a single shared **six-channel homogeneous spinor/log-frame candidate**.
Its quadratic physical decoder satisfies the sourced Hamiltonian constraint
identically. An independently checked cubic proper-time vector field pushes
forward to the existing full44 homogeneous Einstein–massive-scalar–dust source,
and beta_dot=k supplies the same nondegenerate metric B=exp(beta). The actual
retained-history map, ordinary runtime, source/stress and clock observations
are joined by exact tensor/seed identities. Three fixed-proper-time resolutions
pass physical-field, phase and dust-mass convergence; a finite-time first-order
convergence/domain theorem covers the declared prepared family.

This is a restricted new physical coordinate interpretation, not arbitrary-state
compression of full45 or a solution of the general spatial problem. The old
Euler and cross-history failures remain controls. Exact decoded constraint does
not make finite-step source conservation exact: dust-mass drift is still
nonzero and decreases with refinement. Exponential projective bit growth,
spatial modes and operational clock/detector construction remain open. A
separate native arithmetic bridge is not attributed to this tensor. No accepted
default model or runtime mode is introduced. Reproduce the joint evidence with
`python -m validation.unified_law.run_all`.

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

### Generic coupling integration and exact sector reconstruction

[Generic coupling controls](GENERIC_COUPLINGS.md), implemented in
`validation/generic_couplings/`, make the seven-specialist #40/#41 audit
reproducible in the central source and CI. The current massive45 board builder
is restricted by exact coefficient identities to six complete channels and
14 terms on a declared homogeneous isotropic neutral scalar/dust invariant
domain. Guarded embedding and projection preserve both histories and carries;
projection rejects out-of-domain states rather than repairing them. The
independently declared small tensor is compared against the extracted one.

Both full and restricted bundles execute through `system.runtime.run_bundle`.
The audit reconstructs each saved full transition from the six-channel state
and verifies its complete canonical click stream after reconstruction. It does
not identify raw six-channel event identities with full45 event identities.
Code/tensor/seed/run provenance and integer growth are reported together.

The same package checks generic carry/class identities, silent mechanical
cycles, exact native packing with its old-history polynomial obstruction,
reciprocal single-edge ports and clock/covector negative controls. It changes
neither Engine nor default allocation. The six-channel sector retains the
original constraint/time-stability defects and excludes transported/charged
and anisotropic modes; the three-channel reciprocal example is separate.
Operational-clock, nonlinear Einstein, detector and quantum gates remain open.

## Local carrier–record source construction

The source-only package `validation/local_unification/` extends the research
contract without changing the Engine, bundle, canonical decoder or physical
acceptance gate. It uses one bounded four-rail collision,
`1001 <-> 0110`, where the rails are record+/record-/carrier+/carrier-.
Its cubic polynomial preserves positive packet energy and signed propagation
momentum, with equal and opposite record/carrier recoil.

A paired-bank first-order map `F(A,B)=(G(B),S(A))` is compiled using
`u=3(F+F^-1)` and complete prepared history `a=F^-1(b)`. The resulting
eight-channel invariant sector is Boolean for all time with every legal
remainder retained. Two Engine microticks form one streaming macro; neither
the two staggered populations nor their records are hidden workspace.

The joined twelve-channel tensor retains four additional characteristic
geometry profiles and includes actual packet-source terms in their update.
On a plane-symmetric causal interior, `Delta²F=-n+` and `Delta²G=-n-`
are preserved. Cubic cardinal B-spline reconstruction converts these exact
difference identities into `f''=-sum(n+ B1)` and `g''=-sum(n- B1)`.
For `R=f(u)+g(v)>0`, the metric
`ds²=-2R^(-1/2)du dv+R(dy²+dz²)` has only
`G_uu=-f''/R` and `G_vv=-g''/R` nonzero, supplying a restricted spatial
null-source Einstein chart from the same retained run. The physical
coordinates are `u=t-x,v=t+x`; packet-count invariants and local orthonormal
stress are distinguished.

This is not a globally periodic positive-source solution: summing the
periodic discrete Laplacian proves that such a global profile is impossible
for nonzero nonnegative source. The finite chart has an explicit causal and
spline-support margin, a continuous positivity bound and even-microtick
readout. Its exterior seam defects remain in the complete invertible state.
Wrong-source, unsafe-readout and mixed-source evidence controls must fail.

The package distinguishes finite repeated routing, record retention, full
source replay and exact restricted physical identities from the still-open
targets of massive localization, material proper-time clocks and sustained
structural growth. The standard general physical gate remains blocked.
Proofs, registered experiments and reproduction commands are indexed in
[the local construction report](research/local_unification/README.md).

### Finite gauge loops and complete connection histories

[Gauge-loop research](research/gauge_loop/README.md), tracked in issue #66,
adds two source-only constructions through the same bundle/Engine/runtime:
a seven-channel static Z4 wave with a neutral retained intensity reader, and
a separate ten-channel dynamic Z2 connection-exchange sector. Both use
degree-two strict single-edge tensors and count all histories and carries.

The static law proves a same-tensor two-path response to independent loop
flux (intensities four and zero), and full-state invariance of physical
readouts under time-independent local Z4 transformations. Its links are
stationary on the declared preparation; its homogeneous matter mode grows
as `1,3,11,41`, so it is not a stable Maxwell or probability evolution.

The dynamic law uses `F(chi,eta,U)=(eta,U*Y,chi*Y)` with stationary neighboring
sign `Y`. Preparing `a=F^-1(b)` and compiling `u=3(F+F^-1)` gives exact native
evolution with all carries retained. It preserves group-valued links and
supports complete-history charged-register/link feedback and changing
plaquettes. The complete period divides three; evolving information stays
within edge triplets. No electric Gauss law, propagating wave, energy-stress
source, material clock or sustained complexity follows.

The two tensor identities remain separate in saved evidence. Historical
unit-norm drift, carry-source charge balance, multi-edge support rejection
and raw C1/C2 gauge dependence remain explicit falsification controls.
Run `python -m validation.gauge_loop.audit --out runs/gauge-loop` in a fresh
directory. This extends mathematical validation, not physical acceptance
or the supported runtime interface.

## Exact allocation and symmetry (bundle schema 3)

`create_bundle` requires exactly 48 source channels and every integer in their
complete seed. It neither adds idle channels nor changes a polynomial. The
same strict support, degree, remainder, ownership and acyclic-dependency checks
remain. Every role passes the exact 2O coefficient certificate before a bundle
is returned. Save, load and execution repeat validation even for directly
constructed dataclasses or rehashed input files.

The manifest records `law.symmetry`; CLI status reports the required action.
The tests reject every allocation 1..47 and 49, test all 144 retained registers
against a scalar oracle, reject asymmetric research and omitted-declaration
bypasses, and exercise saved replay and the full nonlinear symmetry action.
The lower-level Tensor/Engine algebra primitives remain generic so independent
oracle, integer-boundary and inverse tests can exercise them directly.

Schema-1/2 evidence remains pinned historical evidence. Compatible tensor and
seed inputs must be freshly prepared as schema 3 and run in a new directory.
A non-equivariant law requires a new mathematical construction; changing its
role or adding zero channels is not a migration. Padding helpers remain pure
construction utilities for historical source code and are never an admission
exception. The old research acceptance collector is not a supported schema-3
smoke; use `python -m validation.system_smoke --out NEW_DIRECTORY`.

## GitHub merge policy

`.github/main-protection.json` records the intended main-branch policy:
require both `universe24 (3.11)` and `universe24 (3.12)` checks, a branch up to
date with main, pull requests, and enforcement for administrators. No approving
human review is required. Force pushes and branch deletion are disabled.
This file is a configuration payload, not evidence that GitHub has applied it.
An authenticated repository administrator can apply it with:

```bash
gh api --method PUT repos/Closer24/Universe24/branches/main/protection --input .github/main-protection.json
```

Verify the live branch protection after applying it. CI alone does not enforce
the merge policy.
