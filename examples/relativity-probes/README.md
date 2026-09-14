# Relativity probes: gravity from the computation field, twin clocks, quantum transport

Three configuration-only probes of what the generic engine does with a mass whose
`computation` field is the local cost of computing (Highlights 4.4), run on
2026-09-14 on branch `feat/self-field-policies-and-carried-phase` after merging
main `1c78239`. Every physical rule below is supplied in JSON; the engine holds
no gravitational, relativistic or quantum-matter formula.

```sh
python examples/relativity-probes/gravity_lensing.py 24000 80 300 1 default
python examples/relativity-probes/gravity_lensing.py 24000 80 300 1 along 44
python examples/relativity-probes/twins_dilation.py
python examples/relativity-probes/quantum_gravity.py
```

## 1. Deflection by a mass (`gravity_lensing.py`)

A held mass emits the conserved scalar `computation` field outward. Twelve bodies
(mass 1) pass it at impact parameters b = 3, 5, 7 on both sides: "light" with
momentum 120 (speed c) and "slow" with momentum 60 (c/2). Each body exchanges
momentum with the delivered flux of that field times its own mass through the
generic `spatial_couplings` exchange rule; the attractive sign is supplied (`+1`
under the delivered-flux convention; `-1` repels, as the first run showed).
Momentum is an outward spatial field, so carrier plus field momentum is exact.

Default clock (no delay), emission 24000, denominator 80, 30 ticks:

| body | b | final momentum | angle toward the mass |
| --- | --- | --- | --- |
| light | 3 | (120, ∓18, 0) | 0.150 |
| light | 5 | (120, ∓4, 0) | 0.033 |
| light | 7 | (120, ∓1, 0) | 0.008 |
| slow | 3 | (62, ∓28, 0) | 0.452 |
| slow | 5 | (60, ∓8, 0) | 0.133 |
| slow | 7 | (60, ∓2, 0) | 0.033 |

- Velocity law: slow/light at b = 5 is **4.00**, exactly the Newtonian 1/v².
- Impact-parameter law: b = 3 / b = 7 is 18 for light against the Newtonian 2.33.
  The bodies cross the mass's own axis column, where the `straight` allocation
  phase concentrates far-field units into axis rays, so the sampled flux falls
  much faster than 1/r². This is the lattice far field, not a supplied law.
- Both sides deflect symmetrically; the control with emission 0 does not deflect.

Shared clock (`spatial_computation_delay`): with the load defined as the stock
present at a node, the source node's own emission (24000 per tick) is its own
load, so the source forwards once per 80 intervals at budget 300 and the far
field never forms within the run; no body was deflected or delayed. The shared
clock therefore needs a load definition that excludes a node's own emission
before it can serve as a gravitational clock for this probe.

Directional delay (`delay_direction`, default clock, budget 300) delays each
departure by the load delivered through its port, so the source does not
throttle itself. `along` and `against` give identical trajectories here because
a body's ±x ports see the same delivered load on the axis column. After 44
ticks (light at b = 3 needed 14 extra intervals beside the mass):

| body | b | angle, no delay | angle, directional delay |
| --- | --- | --- | --- |
| light | 3 | 0.150 | 0.149 |
| light | 5 | 0.033 | 0.033 |
| light | 7 | 0.008 | 0.008 |
| slow | 3 | 0.452 | 0.385 (still passing at tick 44) |

The delay slows the passage but adds no deflection: a delayed departure is a
wait at the node, not another sampling of the field, so the impulse per hop is
unchanged. Time dilation alone therefore does not supply the "second half" of
the relativistic deflection in this engine; that would need the wait itself to
count as interaction time (a declared coupling choice), or spatial curvature,
which no lattice quantity represents yet.

## 2. Twin clocks (`twins_dilation.py`, `observer_twins.py`)

A traveller (momentum 30..120 out of 120) goes to a mirror 12 links away and
returns; both twins count completed local cycles in a `clock` field.

| budget | v = 0.25 c | 0.5 c | 0.75 c | 1.0 c | Lorentz √(1−v²) |
| --- | --- | --- | --- | --- | --- |
| unlimited | 1.000 | 1.000 | 1.000 | 1.000 | 0.968 / 0.866 / 0.661 / 0 |
| 24 | 1.000 | 1.000 | 1.000 | 1.000 | |
| 20 | 0.990 | 0.980 | 0.970 | 0.960 | |

No kinematic time dilation emerges. Only a budget below the moving cycle's cost
(about 21-24 units) slows the traveller, and then linearly in the number of
moves, not as √(1−v²). The engine clock is Galilean; velocity-dependent
dilation is not implied by the fixed link time.

## 3. Quantum transport under the field (`quantum_gravity.py`)

`localized-contact-quantum-v1` converts a charge into a one-excitation domain at
x = 1 and hops it by configured swap gates one Link per tick to a detector at
x = 7. A mass beside the chain emits `computation`; `delay_direction: "along"`
delays classical departures (the contact program rejects the shared clock). A
classical carrier runs the same six links on a parallel row.

| | emission 0 | emission 6000 |
| --- | --- | --- |
| classical runner, 6 links | arrives tick 6 | arrives tick 13 |
| quantum excitation, 6 links | captured tick 6 | captured tick 6 |

Read by a local observer instead of the host report
(`quantum_from_the_side.py`: the observer at the detector node knows only when a
localized charge first sits in its own records and when the runner, launched on
the same row, is received at its node): click at tick 7 and runner at tick 7
without the mass; click at tick 6 and runner at tick 20 with it.

The field delays the classical carrier but the quantum gate schedule advances
one Link per world tick regardless of local load. In this profile the quantum
domain does not feel the computation field: an equivalence-principle gap that a
configuration cannot close, because gate admissibility reads only the fixed
Link time, never the node's delay.

## What these probes do not show

They do not derive gravity, the 1/b lensing law, the factor two of general
relativity, Lorentz dilation or quantum matter in a gravitational field. They
locate exactly which parts follow from the generic engine (exact momentum
bookkeeping, the 1/v² velocity law, directional delay) and which need a new
declared rule (a self-excluding load, a delay-aware gate clock).
