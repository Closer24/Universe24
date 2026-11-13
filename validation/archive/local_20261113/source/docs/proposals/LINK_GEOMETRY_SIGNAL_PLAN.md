# Link geometry and geometry-sensitive signal propagation

Status: passage-ticks-first interpretation under investigation. Generic shared-link infrastructure is
implemented locally; physical propagation and gravity are not accepted models.
Source inspected: `e582960f6c9d2d134d3d6b28c08494e8bfafa86a`.
Prepared: 2026-11-13.

The latest node-centered interpretation is implemented as the
[coupled face processor](../FACE_PROCESSOR_MODEL.md): six oriented port
views, fixed adjacency and one 25-channel law for changing local phase,
bidirectional feedback and actual one/two-update passage. Its scalar-delay
and Einstein limitations remain explicit. The [Hebrew model overview](../FACE_PROCESSOR_MODEL_HE.md)
connects the retained implementation with the clock/gear analogy.

## Passage ticks as the primary operational link variable

The latest proposed interpretation chooses a positive integer `N_e` as the
link's passage cost, measured against a declared reference tick. For a static
calibrated chart, `Delta_tau_e=N_e*tau0` and `L_operational=c*N_e*tau0`.
The constant `c` converts time and length units; it does not determine `tau0`
or make an Engine update a physical proper-time interval. A clock cycle can
supply a reference only with a declared counting/calibration procedure.

This supersedes length as the preferred *primary interpretation* for the next
transport experiment. The historical positive-b length adapter and its tests
remain unchanged. `N_e` is not necessarily a literal single-register value:
the current finite prototype encodes N=1,2,4 in two selector fields per link.
There is still exactly one independent link state shared by its endpoints.

The positive static passage experiment in
`runs/dynamic-link-review-20261113/time_link_naturals.py` affinely recodes the
existing frozen transport law. It uses 31 channels, degree two, and no new
runtime behavior. All 21 saved runs (204 forward updates) preserve strictly
positive retained integers, nonzero carries and exact inverse. Measured
neighbor arrivals are 1,2,4 updates in all six directions; mixed paths add
their delays in either direction. A 128-update case checks repeated transit.
This is a separate tensor from the dynamic ten-channel scatterer.

The exact recoding is `A=a+K`, `B=b+K`,
`u_new(A,B)=u_old(A-K,B-K)+6K`, with K=1 except K=2 for the four-phase
reference clock. Rule3 then gives the same old evolution plus K. The clock
phase is fully retained, but counting elapsed cycles in this experiment is a
passive trace measurement, not a demonstrated material elapsed-time device.

An arbitrary or changing N still needs native reversible transport/storage;
no external wait, arrival queue or reset is authorized by the interpretation.
Changing N while information is in flight must preserve that information and
have a derived passage law. In a curved or time-dependent spacetime,
operational signal distance need not equal a spatial slice's proper length.
Shared-clock/metric calibration, angular information and source equations
remain independent acceptance gates.

## Einstein representation target after the dynamic and spring controls

The lengths-first adapter remains a generic allocation, not a restriction
that all of spacetime must be determined by one positive scalar per face.
The direct geometric reference for length-based Einstein discretization is
**Lorentzian Regge calculus**: compatible four-dimensional cells carry
signed squared intervals and a causal type; angles and curvature follow
from the cell geometry, and a gravitational-plus-matter action determines
the equations. A collection of Hooke springs does not establish that action.

Primary references:
[Jercher and Steinhaus, sections 2 and 4](https://arxiv.org/html/2312.11639v2)
give the Lorentzian geometry, spatial and temporal variables, restricted
Regge equations and continuum-limit qualifications.
[Bahr and Dittrich](https://arxiv.org/abs/0907.4325) discuss length and angle
formulations. These are references for the physical target, not installed
runtime algorithms or proofs that the target fits the engine contract.

Our six face neighbors can remain the communication graph. They do not
automatically supply all cell geometry. Two positive spatial metrics,
`I` and `[[1,1/2,0],[1/2,1,0],[0,0,1]]`, give the same six unit axial lengths
but different xy angles. Declaring the axes permanently orthogonal restricts
the represented spatial metrics. Angles need not be independent registers,
but their information must be represented or recovered. Under triangulation,
enough compatible edge intervals determine this information; the bare cubic
face skeleton lacks those extra measurements.

The existing `observe.simplex_metric` gives an exact passive target:
in a declared basis, the ten signed squared intervals of a nondegenerate
four-dimensional tangent simplex reconstruct the symmetric metric through
the polarization identity. This includes time-space cross terms and checks
signature (-,+,+,+). It does not add diagonal Engine reads, a new state bank
or a finite-cell Regge solver. A spatial positive length and a signed
spacetime interval are different observables; a null interval is zero.

Recommended implementation boundary:

| Object | Intended meaning | Current obligation |
| --- | --- | --- |
| Node plus retained history | Local degrees of freedom and ordered updates | Define a physical event through records; do not identify updates with proper time by name |
| One independent shared link | Geometric state with both-endpoint response | Declare a positive length readout and a valid prepared domain |
| Relations among local directions | Cell shape / spatial metric cross terms | Represent or derive missing shear/angle information within counted state |
| Same local Lorentzian geometry | Signal cones and clock readings | Derive both from the same histories and test actual retained apparatus |
| Fixed coupling tensor | Geometry/matter evolution | Match a declared Einstein source and constraints with convergence, within degree/locality/budget |

The strongest already executed spatial Einstein reference in this repository
is the restricted twelve-channel null-source chart in
`validation/local_unification/`; the eight-channel Bianchi I sector provides
an exact homogeneous anisotropic/source-clock reference. Neither is the new
link scatterer. Use their independently derived metric/source identities as
benchmarks, and test the existing lack of geometry-sensitive apparatus rather
than assuming those references already provide it.

Rest length 1 may define the flat reference preparation. The isolated spring
test proves it can be a fixed point of unchanged Rule3, but stretched seeds
reach zero or negative raw length. A physically admissible constitutive law
and natural-state domain remain required. Cyclic restoring motion alone does
not establish a cosmological bounce or repeated bangs. A natural-integer
encoding may reconstruct signed/rational geometry; it must disclose and
preserve that encoding rather than treat every raw register as a length.

The actual new results, positive-domain theorem, countercontrols and full
execution evidence are in
[DYNAMIC_LINK_NATURALS_EXPERIMENT.md](../DYNAMIC_LINK_NATURALS_EXPERIMENT.md).
No general Regge-to-cubic-tensor compiler is claimed. Regge variations can
involve several cells, inverse trigonometric functions and nonlinear solves;
the fixed cubic single-edge Engine cannot simply execute such a solver.

## Goal and first deliverable

Use the existing nodes and six face neighbors, with link lengths as primitive
geometric data. Derive temporal observations from signal passage and internal
processes; do not add independent angle variables or assume Engine ticks are
physical proper time. Infer angles and an effective spacetime metric only where
the resulting observations support such a reconstruction.
The eventual target is reciprocal matter/geometry evolution with the same
operational metric. A finite graph with geometric labels is not by itself an
Einstein solution. Agreement is to be demonstrated on a declared domain and,
where approximate, by a controlled continuum limit.

The generic construction/readout adapter is now `universe24.core.network`;
see [NETWORK.md](../NETWORK.md). It preserves the existing tensor, State and
Engine and counts each independent link field only once. The source-only
`validation.network_smoke` fixture demonstrates mechanical two-way coupling,
not physical propagation at c. The exact prepared delay construction is now recorded in
[LINK_PROPAGATION_EXPERIMENT.md](../LINK_PROPAGATION_EXPERIMENT.md):31 channels,
lengths1,2,4, with failed spatial-isotropy and general clock-identification
controls. It does not complete the physical gates below. The first physical
deliverable remains a **restricted geometry-sensitive
signal bundle**: two complete seeds differing in geometry, the same immutable
tensor and signal preparation, independently predicted arrival times, actual
Engine histories, scalar-oracle checks and exact rewind. It is a fixed-background
propagation control, not yet dynamical gravity or a physical clock.

## What already exists

| Existing source | Reuse | Limitation |
| --- | --- | --- |
| `universe24/core/lattice.py` | Fixed spatial face-neighbor graph | A graph offset is not a physical distance |
| `universe24/core/tensor.py` | Immutable polynomial law, link ownership metadata, strict physical support | Metadata alone does not affect propagation |
| `universe24/observe/simplex_metric.py` | Exact conversion between a local Lorentzian metric and ten signed squared tangent-simplex intervals | No finite-cell Regge evolution; tangent intervals need not equal finite curved geodesic distances |
| `universe24/observe/metric_clocks.py` | Independent proper-time-rate calculation | Passive readout, not a retained material clock |
| `validation/local_unification/` | Saved source/chart, packet balance and record controls | Geometry profile channels do not enter packet updates; unchanged packet records can coexist with different proper-time rates |
| `universe24/system/` | Complete bundles, passive decoding, saved replay and validation | Does not certify a physical interpretation |

The specific existing counterexample is documented in
`docs/research/local_unification/10_limits.md`: shifting geometry profiles can
leave all packet histories unchanged while changing metric proper times.
The new construction must address this missing coupling, not rename it.

## Event and link semantics

1. Keep the current spatial graph. A computational spacetime location is
   `(node, Engine tick)`, not a node without a time label. A physical event
   requires a declared readout and calibration; an arithmetic click alone is
   not a detector event. If several microticks form a physical step, declare
   that mapping and all retained scheduling state.
2. A spatial link joins adjacent nodes on a slice. Signal influence connects
   a location to a later location through Engine updates; it cannot travel
   instantaneously along a spatial link on the same slice.
3. A link's squared length is geometric data. An angle is a relation between
   two incident directions at a node/cell, not an independent property of a
   single edge. Do not store redundant angle values that can disagree with
   the lengths/metric.
4. Each link is an independent entity with one shared state. Its base node
   supplies a canonical storage address only, not ownership. Both endpoints
   may contribute to its synchronous update. All fields count in the budget. No separate uncounted edge-state bank or in-flight queue.
5. A null spacetime interval can be zero despite a nonzero spatial separation
   and travel time. Never use `sqrt(abs(spacetime_interval))` as a universal
   distance or delay.

## Canonical geometry representation

The revised choice is **lengths first**, superseding the initial metric-first
proposal. One scalar link field requires three stored channels per array cell, each
with full `(a,b,r)` history. The optional current reader uses positive `b` as
length. Other exact encodings require an explicit versioned interpretation;
they must not silently introduce another state bank or runtime division.

For a fixed positive-length snapshot, define the intrinsic graph distance as
the minimum sum of edge lengths over paths. The frozen-edge travel-time target
is `length/c`. These are definitions/diagnostics, not an external shortest-path
algorithm that advances the Engine. An evolving edge requires a separate
declared passage law; applying a frozen length/c formula at each tick does not
establish that law.

No independent angle, lapse or shift registers are introduced by the generic
adapter. The axis labels are topology addresses. If a continuum description
emerges, infer metric/clock relations from the physical records and compare
with independently declared relativistic benchmarks. The existing simplex
reader remains an optional validation reference, not the source of link data.
Nearest-face shortest-path distances on a cubic graph are generally anisotropic
(an elementary face diagonal costs two equal edge lengths). Euclidean local
geometry, Lorentz symmetry and null-cone convergence are obligations to test,
not consequences of labeling each edge's target speed c.

Both incident nodes reference the exact same length triple. No positivity
projection or state repair is allowed during evolution. A physical reader
reports domain failure without altering the reversible integer state.

## Propagation target and implementation boundary

Begin with a massless scalar wave as a causal propagation probe. It is not yet
electromagnetism, a photon detector or a universal matter model. The independent
continuum target is

```
partial_mu(sqrt(-g) g^{mu nu} partial_nu phi) = 0.
```

In the geometric-optics regime its wave covectors satisfy
`g^{mu nu} k_mu k_nu = 0`; rays follow the corresponding null geometry.
Finite-wavelength diffraction and discrete dispersion are separate effects.

For the first static one-dimensional chart, set shift to zero and use

```
ds^2 = -alpha(x)^2 dt^2 + h(x) dx^2
dx/dt = +/- alpha(x)/sqrt(h(x))
coordinate travel time = integral sqrt(h(x))/alpha(x) dx.
```

This predicts coordinate arrival time. Locally measured light speed remains
one in units `c=1`; a coordinate delay is not a variable local speed of light.
Choosing the special relation `alpha^2=h` alone would hide the very propagation
response this first experiment is intended to test.

The continuum metrics above are independent benchmark targets, not additional
fundamental state in the lengths-first proposal. A reconstruction/calibration
connecting network observations to each target must be declared and tested.
The Engine must generate the signal trajectory using retained geometry
variables in its fixed polynomial inputs. A term such as `C * geometry * phi`
illustrates permitted variable-state coupling with fixed coefficients; it does
not by itself implement the wave equation. The independent metric calculation
must never route a signal, select a shortest path, schedule an arrival or update
the Engine.

Compiler feasibility is a real gate:

- Metric inverses, roots and variable divisions in the target equations do
  not automatically fit a degree-at-most-three integer tensor. Derive a valid
  encoding or restrict the proposed domain. Do not insert a runtime solver.
- Off-diagonal spatial terms can involve two face directions. A monomial
  cannot read both neighbors at once under strict one-face support. Any
  staged transport must use counted retained registers, obey the acyclic
  old-`a` condition and include its physical-time and dispersion effects.
- Changing coupling strengths may change long-wavelength group velocity while
  leaving the microscopic graph dependency cone unchanged. Measure the actual
  earliest influence as well as the pulse peak. Do not hide small precursors
  behind a detection threshold or call group-speed agreement exact causality.

## Reciprocal geometry and clocks

After propagation passes, derive a coupled geometry/matter update from a
declared discrete variational formulation or an equivalent independently
validated field-equation construction. Matter stress must be derived from the
same signal/matter law, rather than identified with a convenient click count.
Test all relevant Einstein components and Hamiltonian/momentum constraints,
not only one scalar residual. A generic reciprocal interaction is insufficient.

Use independent Regge/continuum calculations as external references. A Regge
solver with nonpolynomial operations and multi-cell constraints cannot simply
be placed inside the current Engine. Replacing the runtime contract would be
a separate architectural proposal, not part of this plan.

Then introduce retained oscillators/detectors with finite preparation resources
and reciprocal coupling. Compare their records against passive proper-time
and geodesic predictions. Changing geometry must affect appropriately prepared
apparatus; changing apparatus must contribute to the source where claimed.
Compare coordinate changes with the apparatus transformed too. A passive
integral of proper time is not itself the material clock being validated.

## Work sequence and acceptance gates

| Stage | Deliverable | Required checks before advancing |
| --- | --- | --- |
| 0. Encoding and locality | Written equations, complete integer allocation, immutable tensor candidate and initial-domain construction for the restricted probe | At most 48 total channels, degree at most three, one-face physical support, acyclic old-`a`, no hidden scale/division/queue; independent scalar oracle and exact inverse with nonzero carries |
| 1. Static 1+1 propagation | Same-tensor paired geometry preparations, flat reference and spatially varying lapse/length case | Predicted arrival-time changes, exact retained-state replay, stability, earliest-influence audit and at least three matched physical refinements; disclose fixed-background approximation |
| 2. Angles in 2+1 | Nonzero off-diagonal spatial geometry and a spatially varying chart | Correct directional null cone, coordinate-shear negative control, actual refraction/deflection where predicted, and no forbidden two-neighbor read; a constant sheared flat metric is not curvature |
| 3. Reciprocal source | One coupled candidate including geometry and matter | Source interventions change geometry, geometry interventions change signals, constraint propagation and conservation checks, independent Einstein residuals and refinement on the same histories |
| 4. Operational measurements | Retained clock and receiving apparatus in that same candidate | Clock comparisons, round-trip signaling, detector resource account and source effects; independent predictions from the same metric |
| 5. Generalization | Larger three-dimensional preparations, multiple directions and independent matter probes | Held-out seeds/geometries, longer horizons, stability and precision costs; no general acceptance from a symmetry-restricted success |

A different tensor at a later research stage is a different versioned candidate.
Do not pool its positive results with an earlier tensor into one physical
certificate. Prefer refinement through declared preparation/calibration with
the same tensor. If that is impossible, state and justify the discretization
family before claiming convergence of one theory.

Before each run, fix physical domain, seed family, duration, detector protocol,
expected numerical order and tolerances. Report actual errors and observed
order over at least three resolutions; growing precision alone is not spatial
or temporal convergence. Exact arithmetic replay and physical approximation
error are separate measurements.

Mandatory negative controls include disconnected geometry-to-signal terms,
wrong length/time normalization, diagonal-only geometry for an off-diagonal
case, mismatched source histories, invalid metric signature, corrupted evidence
and finite-resource exhaustion. No failed physical gate becomes a software
success claim by being an expected negative control.

## Channel and execution contract

The complete allocation must satisfy

```
geometry + matter + clocks + detectors + scheduling + workspace <= 48
retained integer entries per node = 3 * allocated channels.
```

Three length channels do not establish this bound for the full implementation.
Map every retained quantity to an actual channel, including geometric momentum
if the chosen encoding needs it. Do not assume that old/current length histories
already supply a validated gravitational phase space. Report peak
integer bit length and total retained bit cost as well as channel count.

Preserve the Rule3 update exactly, synchronous old-state reads, complete carries,
and the existing prepare/run/verify pipeline. Geometry-sensitive coefficients
are implemented as products of evolving channels in one immutable tensor,
not by mutating the tensor between ticks.

## Proposed repository work

Future implementation belongs first in source-only
`validation/link_geometry/`: `encoding.py`, `signal.py`, `prepare.py`,
`oracle.py`, `acceptance.py` and `run_all.py`, with focused tests under
`universe24/tests/`. These paths are planned, not created implementations.
Reuse the current simplex/clock readers and saved-bundle runtime. Independent
oracles must not be imported by the evolution/compiler path.

Fresh evidence goes to a new `runs/link-geometry-*` directory. Record tensor,
seed, interpretation, full ownership, source hashes, complete histories and
status for each gate: passed, failed, not_tested or blocked. Register any eventual
accepted mathematical/interface change in `docs/ONE_SYSTEM.md` and
`docs/RESEARCH_AGENDA.md`; this proposal changes neither contract nor default.

The first practical decision is whether stage 0 can produce the restricted
geometry-sensitive scalar law within the existing rules. Until it does, no
channel budget, evolution equation or equivalence to Einstein dynamics is
claimed as solved.

## Primary physics references

- Sam R. Dolan, *Geometrical optics for scalar, electromagnetic and gravitational
  waves in curved spacetime*, https://arxiv.org/abs/1806.08617. Null-ray transport
  is a geometric-optics result, not an exact arbitrary-wavelength lattice rule.
- Alexander F. Jercher and Sebastian Steinhaus, *Cosmology in Lorentzian Regge
  calculus: causality violations, massless scalar field and discrete dynamics*,
  https://arxiv.org/abs/2312.11639. Demonstrates the importance of temporal cells,
  causal restrictions and qualified continuum limits in a restricted model;
  it supplies no ready-made Rule3 construction.
