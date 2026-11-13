# Independent-link delays and Einstein compatibility controls

Date: 2026-11-13. Source base: `e582960`; local additions are identified by
the SHA-256 entries in `runs/link-propagation-20261113/results.json`.
This is a reproducible research experiment, not a discrete Einstein solver.

## Questions and result

Can an independent shared link carry retained state, accept inputs from both
endpoints and produce a length-dependent transit delay through the unchanged
Engine? **Yes, in the prepared frozen-length sector constructed here.**

Does that construction already reproduce general relativistic spacetime?
**No.** The shortest-edge-path spatial metric fails an isotropy/refinement
control, and spatial lengths do not distinguish the observer/clock geometries
in an independent flat Einstein example. No dynamical Regge or Einstein
equations are implemented by the delay construction.

## Link semantics

A link is an independent entity, not property of an endpoint. There is one
state and one simultaneous update for the link. The positive-axis base is only
an array-storage address (`Link.storage_node`), preserving the existing
`GearType.link` layout. Both endpoints read and can influence that same state.
The two propagation directions are fields of one link, not separate links.

The existing four-channel mechanical fixture directly checks endpoint symmetry.
For a link initially `a=b=1`, one update gives `b_next=1+(q_right-q_left)^2`:

| Left endpoint | Right endpoint | Updated link value |
| --- | --- | --- |
| 0 | 0 | 1 |
| 1 | 0 | 2 |
| 0 | 1 | 2 |
| 1 | 1 | 1 |

This demonstrates a joint update, not a gravitational law. Sequential writes
by nodes would be a different and order-dependent algorithm and are not used.

## Why changing a coupling was insufficient

Matched first-step interventions in `validation.network_smoke` gave:

| Initial length | First affected-neighbor update | Neighbor field value |
| --- | --- | --- |
| 1 | 1 | 1 |
| 2 | 1 | 2 |
| 4 | 1 | 4 |

Length changed the coupling amplitude, not the first arrival. Multiplying a
field by a variable called length does not implement length/c transit time.

## Native delay construction

`validation.link_propagation` compiles one tensor, with degree two and zero
strict-support violations, for all tested lengths, axes and directions.

| Retained allocation | Channels per array cell |
| --- | --- |
| Six node payload ports | 6 |
| One node reference oscillator | 1 |
| Two selectors on each of three stored links | 6 |
| Three payload stages per direction on each of three stored links | 18 |
| Total | 31 |

Every channel retains all three integers, so this is93 retained integers per
node-sized array cell. Length is decoded as `1+select2+3*select4`, with the
stationary prepared pairs `(0,0)`, `(1,0)`, `(0,1)`. These select paths with
one, two or four transfer stages. Inactive buffers are fixed points that retain
their contents; they are not cleared. Oppositely moving payloads use separate
fields of the same shared link. Each field still uses exactly the standard
Rule3 update. The reference oscillator has period four and is not a calibrated
proper-time apparatus.

For the independently defined prepared routing permutation P, the carrier
tensor implements

```
u = 3(P + P^-1)b
a_next = b
b_next = (P + P^-1)b - a
```

With complete initial history `a=P^-1 b`, this gives `b_next=P b` exactly.
The retained selector equations keep the declared geometry frozen. Any valid
remainders are preserved in this prepared sector. Outside the preparation
chart the Engine remains reversible; the pure routing interpretation is no
longer asserted. The precursor in the old history is explicitly prepared,
not injected or reset during a run.

The permutation is an external preparation/validation oracle. It is not
called to evolve the actual experiment. Actual state evolution is through
`run_bundle`, `Engine.step` and saved-run verification. Conditional routing
has been expanded into fixed integer monomials of selector and payload
channels, each supported on one physical face edge.

## Actual measurements

All18 uniform cases (three lengths, three axes, two directions) and two mixed
cases passed. All used the same tensor. Every saved run was replayed, compared
against an independent scalar recurrence and permutation oracle, inverted
step-by-step, and rewound to the complete seed. The saved single-payload runs
had a maximum integer width of3 bits, including carries. Separate tests also
checked arbitrary80-bit payloads and unprepared inverse behavior.

| Selected length | Measured first arrival, all six directions | Earlier receiving-node payload |
| --- | --- | --- |
| 1 | Update1 | None |
| 2 | Update2 | None |
| 4 | Update4 | None |

For successive links with lengths1,2,4, measured arrivals were updates1,3,7.
Traversing the same three edges in reverse gave updates4,6,7.

These are **native update counts**, not independently measured physical proper
times. Setting the elementary length unit divided by c equal to one reference
transfer duration supplies a kinematic calibration, not an experimental proof
of a universal relativistic clock. No turning/scattering, dynamic length
backreaction, photon detector or universal Born rule is supplied by these
directional rails. The finite stage allocation does not implement arbitrary
unbounded delays inside the same31-channel construction.

## Spatial geometry negative control

On a cubic six-neighbor graph with equal edge length1/N, an axial displacement
of one unit has shortest-path length1; displacement `(1,1,0)` has length2,
instead of the Euclidean square root of2. Refinements N=4,8,16,32 all retain
the same relative diagonal error, approximately41.4214%.

This is an independent graph-distance calculation, not a simulated diagonal
payload trajectory: the present routing law has no turning mechanism. It
rules out identifying this particular shortest-face-path distance with an
isotropic Euclidean metric by refinement alone. It does not rule out other
wave-based or collective effective geometries on the same graph.

## Einstein clock/observer negative control

The independent reference uses a flat Rindler metric, with c=1:

```
ds^2 = -(1+a*x)^2 dt^2 + dx^2 + dy^2 + dz^2, 1+a*x>0.
```

Christoffel symbols, Ricci and the Einstein tensor were calculated directly
from this metric; all16 Einstein components are exactly zero. For a=1,
stationary observers at x=0 and x=1 have spatial separation1 on a slice, but
their proper-time rates relative to t have ratio2. A null ray takes coordinate
time log(2), approximately0.693147, to travel between them. Uniform-lapse
inertial observers with the same spatial edge lengths instead give time1.

The comparison is between **different observer congruences**, not a claimed
failure of coordinate invariance for an already calibrated physical apparatus.
The source at x=0 has proper time t. Its radar round trip is therefore
`2*log(2)`, approximately1.386294, rather than the length-only prediction2.
This round-trip comparison does not require synchronizing two remote clocks.

| Cells between x=0 and x=1 | Length-only one-way prediction | Independent reference using the lapse | Reference absolute error |
| --- | --- | --- | --- |
| 4 | 1 | 0.6912198912 | 0.0019272893 |
| 8 | 1 | 0.6926605540 | 0.0004866265 |
| 16 | 1 | 0.6930252143 | 0.0001219662 |
| 32 | 1 | 0.6931166695 | 0.0000305111 |

The reference is midpoint quadrature of `dx/(1+x)` and is **not Engine
evolution**. It illustrates the missing time/observer identification. The
length-only prediction has a nonvanishing error of0.3068528194 under all these
refinements. Additional clock/observer information could arise from retained
dynamics rather than being introduced as a fundamental lapse register. This
experiment does not prove that every lengths-first emergent theory is impossible.

## Decision and next experiment

Keep the independent-link representation and the complete local reversible
transfer construction. Replace the amplitude-weighting interpretation with
actual retained transport when testing first-arrival claims. Do not promote
this31-channel fixed-background law into an Einstein model.

The next physical gate is an operational round-trip clock comparison on a
declared observer geometry, alongside an effective spatial-isotropy test.
Choose one metric reconstruction from actual retained records and test it
across directions and resolutions. Then derive and test a reciprocal geometric
law, rather than appending an arbitrary length-growth rule. Changing length
selectors during a transfer is a separate unsolved construction: it can change
the permutation and invalidate the prepared-history proof above.

For Einstein-Regge acceptance, a spacetime cell complex, valid Lorentzian
geometry, a defined matter action/source and the discrete field equations are
still needed. Passing graph-delay tests is only a kinematic result. No new
default model, runtime selector, hidden scheduler or external state updater
has been introduced.

## Reproduce

```
python -m unittest universe24.tests.test_network universe24.tests.test_link_propagation -v
python -m validation.link_propagation --out runs/new-link-propagation
python -m universe24 verify --run runs/new-link-propagation/L4-axis0-right
```

See `results.json` for all run IDs, complete source hashes, measured arrivals,
refinements and passed/failed/not_tested gate distinctions.

Primary reference: Jercher and Steinhaus, *Cosmology in Lorentzian Regge
calculus: causality violations, massless scalar field and discrete dynamics*,
https://arxiv.org/abs/2312.11639. Its restricted model includes spatial lengths
and temporal cell geometry and qualifies its continuum results. It is an
external comparison, not a theorem that the new Rule3 construction satisfies
Regge's equations.
