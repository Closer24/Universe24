# Relativity probes: gravity from the computation field, twin clocks, quantum transport

## Bottom line (2026-09-14)

Finite observations under supplied JSON couplings and declared engine transport,
capture and phase policies follow. These are candidate measurements, not a
derivation of gravity, relativity or cosmology. Names in the table identify the
questions being probed rather than established physical laws.

| | result | probe |
| --- | --- | --- |
| **light** | one link per tick in every direction, independent of the source; classical Doppler; no kinematic time dilation | earlier session, twins (2) |
| **gravity** | one coupling (momentum += mass × flux, sign supplied) gives attraction, the Newtonian velocity law exactly (4.00), escape speed ∝ √M, and on signed quanta a closed ledger where the pulled body pays | 1, 4, Kerengonen |
| **lensing** | what a local observer sees: the lamp displaced away from the mass, double images from opposite sides, late arrival, a caustic (focal distance ∝ b^2.5-3) — a gravitational lens, not a glass one | 1 (from the side) |
| **cosmology** | expansion is only an initial condition; there is no repulsive term; a closed universe is bound by its size, its field never leaves, and the growing load makes all light slow with age: a distance-proportional redshift without recession, in whole steps | 4, 5 |
| **gravitational phase** | absent on the fixed field clock; present with `ray_delay` + `ray_phase_per_tick` (an engine rule, opt-in): the interferometer fringe beside a mass shifts by the waits — the COW signature | 8 |
| **dark matter** | the same 1/r² transport gives radius-independent outward losses in every closed box tried (period 3 and period 9, R = 3-15): a flat curve from a compressed third dimension, no extra mass. **Pending:** the open-3D control with the identical metric; until it lands this is a candidate, not a result | 4, 6 |
| **dark energy** | not needed for a redshift-distance relation (closure supplies one); nothing here accelerates it | 5, 6 |
| **time** | the eight-tick example replays its exposed snapshots; a restarted equal-mass collision returns positions and reversed momenta | 9 |
| **quantum** | a localized domain does not feel the field's delay (6 → 13 ticks for the carrier, unchanged for the click); main's `field_phase` gives it a phase, not a fall | 3 |

What needed a declared rule, all generic and opt-in: self-field policies,
carried allocation phases, the computation field as delay (isotropic,
directional, least-delay), a ray field as computation field, ray delay and
phase per interval. What does not emerge: Lorentz dilation, accelerated
expansion, quantum matter that gravitates.

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

### With straight rays instead of octant populations (`... default 30 rays`)

Main's `isotropic-ray-field-v1` (`"transport": "ray"`) moves the field as
straight rays along integer headings, so the far field is not concentrated on
the lattice axes. The same probe with the mass emitting rays (4096 golden-spiral
headings, 512 rays per tick, 47 units per ray, balanced routing, default clock):

| body | b | angle (+ side) | angle (− side) |
| --- | --- | --- | --- |
| light | 3 | 0.117 | 0.164 |
| light | 5 | 0.033 | 0.074 |
| light | 7 | 0.033 | 0.017 |
| slow | 3 | 0.397 | 0.385 |
| slow | 5 | 0.136 | 0.150 |
| slow | 7 | 0.083 | 0.083 |

- b = 3 / b = 7: light 5.6, slow 4.7 (Newton 2.33) — down from 18 with the
  octant far field. slow/light at b = 5: 2.7 (Newton 4.0). The remaining
  scatter is ray quantization: a body meets a whole ray or none, and momentum is
  exchanged in units of 47/80 with a carried remainder.
- Two configuration lessons on the way, both about sampling, not physics:
  512 headings at 64 rays per tick (375 units per ray) left b = 7 without a
  single hit in 30 ticks; and the golden-spiral index runs pole to pole, so
  consecutive rays per tick formed one latitude band per tick and the equatorial
  plane saw rays only in bursts every eight ticks (b = 7 light again at zero
  while b = 5 outscored b = 3). A stride coprime to the heading count spreads
  each tick's rays over the sphere and restores the monotonic b-dependence.
- The ray field activates only the nodes rays cross, so these runs take a
  fraction of the octant runs' time.

### On Kerengonen signed quanta (`kerengonen_lensing.py`)

Main's [funded emission and absorption](../../docs/SPATIAL_FIELDS.md#funded-emission-and-absorption)
replaces the momentum reservoir: the mass is a funded source of negative
quanta rays (mirrored golden headings, 512 rays per tick, 4096 quanta each),
credited with what it emits; a passing body absorbs the share mass / 256 of
every ray crossing its Node, pays it from its own quanta and gains the share's
momentum toward the source. Momentum scale 65536 = one hop per tick.

| body | b | angle (+ side) | angle (− side) | quanta paid |
| --- | --- | --- | --- | --- |
| light | 3 | 0.169 | 0.263 | 567, 938 |
| light | 5 | 0.116 | 0.088 | 363, 284 |
| light | 7 | 0.075 | 0.060 | 249, 188 |
| slow | 3 | 0.489 | 0.652 | 909, 1076 |
| slow | 5 | 0.282 | 0.339 | 418, 496 |
| slow | 7 | 0.178 | 0.136 | 261, 199 |

- b = 3 / b = 7 for light: **3.2** (Newton 2.33) — the closest of all the
  transports (octants 18, spread rays 5.6). slow/light at b = 5: 3.0
  (Newton 4.0); the slow body spends twice as long in the field but the
  absorbed share per crossing ray is the same, and the crossing count is what
  the lattice quantizes.
- The ledger closes exactly: quanta in the world 27,340,041 + escaped
  −24,194,313 = the initial stock 3,145,728; momentum in the world plus
  escaped = (589,824, 0, 0), the twelve launches. Every body paid a few
  hundred quanta for its deflection — attraction with the pulled body paying.
- The two sides differ by ray quantization (which rays happen to cross which
  Node); nothing in the configuration distinguishes them.

### Seen from the side (`lensing_from_the_side.py`)

A lamp column at x = 2 sends one light body per row past the mass to a column of
held eyes at x = 34. Each eye is a local observer: it reports only the tick, the
entry port and the arriving momentum of what lands on its own node, and traces
the ray back along −p to where the lamp appears to be.

With the default *cyclic* routing every eye still received its own row's light
at tick 32 through −x, carrying transverse momentum up to (120, ±75, 0) that
had never turned into transverse motion: cyclic routing walks the raw weight
cycle, so weights 120:75 spend the first 120 moves on x. That is a transport
artifact of large momentum scales, not a physical statement; the momentum-based
angles above are unaffected (they were measured with cyclic routing, bodies
staying in their rows), positions are. `"routing": "balanced"` reduces the
weights by their gcd and interleaves lanes (20:3 for (120, 18, 0)). Both
scripts now default to balanced routing. What the eyes then report:

| eye y | tick | via | arriving p | lamp row | apparent lamp y |
| --- | --- | --- | --- | --- | --- |
| 3 | 32 | −x | (120, 4, 0) | 3 | 1.9 |
| 5 | 33 | −x | (120, 9, 0) | 4 | 2.6 |
| 6 | 33 | −x | (120, 18, 0) | 5 | 1.2 |
| 6 | 36 | −x | (120, −37, 0) | 10 | 15.9 |
| 7 | 34 | −y | (120, 18, 0) | 5 | 2.2 |
| 9 | 34 | +y | (120, −18, 0) | 11 | 13.8 |
| 10 | 33 | −x | (120, −18, 0) | 11 | 14.8 |
| 10 | 36 | −x | (120, 37, 0) | 6 | 0.1 |
| 1 | 40 | −x | (119, −74, 0) | 9 | 20.9 |
| 15 | 40 | −x | (119, 74, 0) | 7 | −4.9 |

Without the mass every eye sees its own row at tick 32. With it, from the eye's
own node alone: light arrives later (33-40 ticks, the bent path is longer),
sometimes through a ±y port, the traced-back lamp is displaced away from the
mass (row 5 appears at 1.2, row 11 at 14.8), rows 6/7 and 9/10 cross the axis
and land on the far side, and an eye at y = 6 or y = 10 receives two images at
different ticks from opposite sides of the mass. Everything here is what a
local observer can know: arrival tick, entry port and the arriving record. The
lamp-position inference is the observer's own post-processing, not engine
state.

With the ray field (`... 24000 80 rays`) the eyes see the same signature
without the axis structure: every row's traced-back lamp is displaced away from
the mass, monotonically from the outer rows inward (row 1 → 0.5, row 2 → 1.2,
row 4 → 1.1, row 5 → 1.8; row 11 → 14.7, row 13 → 13.8, row 14 → 15.3,
row 15 → 16.1), arrivals are late (33-36) and cross-overs land on the far side
(row 10 → eye 6 and 7, row 6 → eye 9). Rows 7 and 9 (b = 1) reach no eye: they
pass through the mass node and leave the plane. The isotropic field lenses the
outer rows too, which the octant field could not.

### Does the beam converge? (from the ray-field observer data)

A glass lens brings parallel rays to one focus; a gravitational lens does not
(its deflection falls with impact parameter, so the focal distance grows with
b and the beam forms a caustic, the Einstein-ring geometry). Tracing each
observed ray back to where it crosses the mass's axis, focal distance =
b × p_x / |p_y| behind the mass:

| b | 2 | 3 | 4 | 5 | 6 | 7 |
| --- | --- | --- | --- | --- | --- | --- |
| side + | 7.9 | 18.4 | 33.1 | 67.8 | 240 | 420 |
| side − | 8.9 | 26.1 | 44.4 | 87.1 | 143 | 210 |

The focal distance grows roughly as b^2.5-3: the lattice mass is a
gravitational-type lens with a caustic, not a focusing lens, and the two sides
agree within the ray quantization. There is no converging-beam or inward-ray
mode in the engine; rays are straight lines from a source, and convergence
here is what the momentum coupling does to them.

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

## 4. Expansion or recollapse (`cosmic_expansion.py`)

Four equal masses on the axes at R = 5 in an open 29 × 29 × 3 slab, each
emitting the octant `computation` field (24000 per tick) and exchanging
momentum with its flux (attractive, denominator 80, balanced routing), are
launched outward at a common speed v0. The configuration holds no expansion
term, pressure or cosmological constant.

| v0 (c) | control, no field | with the field |
| --- | --- | --- |
| 0 | at rest | recollapse: all four moving inward from tick 20, mean distance 5 → 4.5 |
| 0.125 | | turned around at distance 6 by tick 10 |
| 0.25 | | turned around at distance 5 by tick 10 |
| 0.375 | | turned around at distance 6 by tick 10 |
| 0.5 | escaped the slab by tick 20 | still expanding at tick 60, mean distance 5 → 6, nothing escaped |
| 0.75 | | turned around at distance 7 by tick 10 |
| 1.0 | | turned around at distance 8 by tick 10 |

At this field strength nothing escapes, not even bodies launched at c: the
momentum coupling removes more than 120 units within ten ticks. This is a
bound, black-hole-like configuration — the escape speed of the four-body
system exceeds the link speed — and the bodies then oscillate within one or two
links of their turning radius. The universe here is attraction plus initial
motion, and the initial motion loses. Weaker fields locate the critical speed:

| emission | v0 = 0 | 0.125 c | 0.25 c | 0.375 c | 0.5 c | 0.75 c | 1 c |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 24000 | recollapse | bound | bound | bound | bound (5 → 6) | bound | bound |
| 2400 (÷10) | falling in | turned around at 8 | expanding, decelerating (5 → 10.5) | expanding, decelerating (5 → 13) | escaped by tick 38 | escaped by 20 | escaped by 14 |
| 600 (÷40) | falling in | expanding, decelerating (5 → 10) | escaped by tick 51 | escaped by 31 | escaped by 22 | escaped by 15 | escaped by 11 |

The critical speed lies between 0.125 c and 0.25 c at emission 600 and between
0.375 c and 0.5 c at 2400: four times the source, about twice the speed. Ten
times more again puts it near 1-1.4 c, which is what the 24000 run shows
(nothing escapes at c). So the configuration has an ordinary escape speed that
grows as the square root of the field strength — the Newtonian scaling again,
read off a four-body lattice universe — and an open universe of this kind
expands forever only when launched above it, decelerating all the way; nothing
in it accelerates the expansion.

## 5. Redshift without recession (`redshift_without_expansion.py`)

Twelve light bodies one link apart run at c along a row past a mass whose
emission of the `computation` field grows by 600 every cycle (a universe still
filling with field). `delay_direction: "along"`, budget 40, cyclic routing
(balanced routing would price 512 route operations per cycle and dominate the
budget). The eye at the end of the row records only arrival ticks.

| | arrival ticks of bodies 1..12 | gaps |
| --- | --- | --- |
| growth 0 (control) | 21, 22, …, 32 | all 1 |
| growth 600 | 35, 36, 39, 51, 52, 52, 53, 56, 56, 59, two not yet arrived by 60 | 1, 3, 12, 1, 0, 1, 3, 0, 3 |

With the field growing, the train arrives late and stretched: ten bodies span
24 ticks instead of nine, mean spacing 2.7 links per tick, z ≈ 1.7 averaged —
a redshift produced by delay growth along the path, with no recession and no
expansion term. The stretch is not smooth: the departure delay is an integer
number of extra cycles, so bodies bunch (gap 0) and separate (gap 12) as the
load crosses each budget multiple. Durations stretch with the spacing, since
the same delay acts on every part of a signal. This is the model's own
candidate for a distance-redshift relation; it does not by itself give an
accelerating relation, and its statistical form is quantized.

### Escape speed against radius: the model's rotation-curve test (`... open rays`)

Flat rotation curves — the dark-matter signature — mean a force falling as 1/r,
so the escape speed would hardly depend on radius; Newton's 1/r² gives
v_esc ∝ 1/√R. The same four-body sweep at emission 2400 with the masses
emitting rays (isotropic far field), at R = 3, 5 and 9:

| R | 0.125 c | 0.25 c | 0.375 c | 0.5 c | 0.75 c | critical speed |
| --- | --- | --- | --- | --- | --- | --- |
| 3 | expanding | expanding | expanding | expanding, one escaped | escaped | ≈ 0.5-0.75 c |
| 5 | turned around | expanding | expanding | escaped by 39 | escaped | ≈ 0.375-0.5 c |
| 9 | turned around | expanding, one escaped | escaped by 25 | escaped | escaped | ≈ 0.25-0.375 c |

The octant-field controls give the same brackets (R = 3: 0.5 c still
expanding, 0.75 c escaped by tick 26; R = 9: 0.25 c still expanding with two
escapes, 0.375 c escaped by tick 24): the bodies sit on the axes, where the
octant field is strongest, so the two transports agree there.
Bracket midpoints 0.62, 0.44 and 0.31 c: the ratios 0.71 (R 3→5) and 0.70
(R 5→9) sit at Newton's √(3/5) = 0.77 and √(5/9) = 0.75 within the sweep's
resolution, if anything slightly steeper. The curve is Newtonian, not flat.
The model therefore has no dark-matter substitute of its own: a flat rotation
curve would need an explicitly extended source, which is dark matter by
another name, or a force law that no local integer transport here produces.

### Closed four-body universe (`cosmic_expansion.py 600 80 5 80 periodic`)

In the 29 × 29 × 3 periodic box every launched body meets the images of the
others within fourteen links: even the field-free control "turns around" at
distance 14 (the minimal-image distance peaks at half the box), so the
open-box labels do not apply. What survives the wrap: v0 = 0 recollapses
(5 → 3.5), v0 = 0.125 c is still expanding at tick 80 (5 → 10.5, decelerating),
and every faster launch reaches the half-box and comes back through the
images. A closed universe this small is bound by construction — its size is
below the distance a free body covers in the run — which is the general point:
in a closed Universe24 "escape" does not exist, only the size of the box
against the launch speed and the accumulating field.

### A compressed third dimension (`... 50 periodic rays 61`)

The hypothesis: dark matter is what a 1/r² law looks like when the far
region is represented with one dimension fewer. The test needs nothing new:
the same reservoir coupling and ray field as the 3D sweep, in a 61 × 61 × 3
box that is periodic — closed in z, so the field cannot leave the plane and
spreads in two dimensions — with the box wide enough that no body meets its
image in 50 ticks (the field-free control at 0.5 c reaches its free path,
28-30 links, with nothing turning around).

| R | 0 | 0.125 c | 0.25 c | 0.375 c | 0.5 c | 0.75 c | c |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 3 | recollapse → 0.5 | turned at 4.2 | 7.5 (free 15.5) | 10.5 (free 21.8) | 13.8 (free 28) | 22.5 (free 40.5) | 29.5 (free 53) |
| 5 | recollapse → 4 | 7.2 (free 11.3) | 10.0 (free 17.5) | 12.8 (free 23.8) | 16.0 (free 30) | 24.0 (free 42.5) | half-box |
| 9 | at rest | 11.2 (free 15.3) | 14.0 (free 21.5) | 16.5 (free 27.8) | 19.8 (free 34) | 27.8 (half-box) | half-box |

Read the loss against the free path:

| launch | loss from R = 3 | from R = 5 | from R = 9 |
| --- | --- | --- | --- |
| 0.25 c | 8.0 | 7.5 | 7.5 |
| 0.375 c | 11.3 | 11.0 | 11.3 |
| 0.5 c | 14.2 | 14.0 | 14.2 |

The momentum lost along an outward path is the same from R = 3, 5 and 9. In
the open 3D box the same coupling and the same ray field gave a critical speed
falling as 1/√R (Newton, ×2 between R = 3 and 9); for a 1/r² force the loss
along an outward path scales as 1/R, so R = 9 should have lost three times
less than R = 3. A loss independent of the starting radius means a force whose
outward integral does not depend on where the body starts — at least as flat
as the logarithmic potential of two-dimensional gravity, i.e. a flat rotation
curve, and by this measure flatter. Nothing in the law changed between the two
sweeps; only the third dimension was closed. What remains to pin the exponent
is a direct force reading (held bodies at several radii in the slab, as in
main's gravity probe) rather than an integrated loss.

Taken together with probe 6, this is the model's own answer to dark matter:
the same 1/r² transport looks Newtonian in three open dimensions and flat when
one dimension is closed or compressed. Whether real galaxies' far fields are
carried in a lower-dimensional representation is a hypothesis this lattice
cannot decide; what it can say is that the flat curve needs no extra mass
here, only a change in how the far region is represented.

### Solved from the model: the short closed dimension sets the transition radius

Universe24 is closed. If one of its dimensions is closed with a short period
L, the field of a mass spreads in three dimensions while r < L and in two once
r > L: the same 1/r² transport gives Newton inside L and a flat curve outside
it, and the transition radius is L itself — a prediction with no parameter
beyond the shape of the universe. Real rotation curves are Newtonian in the
bright inner disc and flat beyond it; in this reading the radius where they
flatten measures the size of the short closed dimension.

The test (`... 50 periodic rays 61 9`): the 61 × 61 slab with the third
dimension closed at period 9 instead of 3, the same coupling and field, at
R = 3, 5 (inside the period), 9 and 15 (beyond it). Newton predicts the loss
along an outward path falling as 1/R at R = 3 and 5; the compressed regime
predicts equal losses at 9 and 15. Measured losses against the free path
(launches whose free path exceeds the half-box are omitted):

| launch | R = 3 | R = 5 | R = 9 | R = 15 |
| --- | --- | --- | --- | --- |
| 0.25 c | 7.5 | 7.5 | 7.5 | 7.5 |
| 0.375 c | 11.3 | 11.0 | 10.75 | 10.75 |
| 0.5 c | 14.8 | 14.8 | 14.8 | — |

The loss is the same at every radius, inside and beyond the period, to the
resolution of the lattice — the same as in the period-3 slab. The prediction's
second half (flat beyond L) holds; its first half (Newton inside L, a 1/R
fall from R = 3 to 5) does not appear. Either the outward integral is
dominated by the long two-dimensional part of the path in both cases, or the
radius independence is a property of this four-body coupling rather than of
closure. Only the open-3D box with the identical metric decides that; it is
the control the whole section rests on and is recorded below when it lands.

### Four masses on Kerengonen signed quanta (`kerengonen_universe.py`)

The same radius sweep with every mass a funded source of negative quanta
(mirrored headings, 128 rays per tick per mass, 16384 quanta per ray) that
absorbs the share mass / 256 of every ray from the others, paying from its own
stock; open 41 × 41 × 3 slab, 60 ticks:

| R | 0 | 0.125 c | 0.25 c | 0.375 c | 0.5 c | 0.75 c |
| --- | --- | --- | --- | --- | --- | --- |
| 3 | recollapse → 1 | recollapse | recollapse | recollapse | recollapse → 0 | still expanding at 3.5 |
| 5 | recollapse → 4 | recollapse | recollapse | recollapse | expanding, 5 → 5.5 | turned around at 6 |
| 9 | at rest | 9 → 9 | recollapse | 9 → 10 | 9 → 10 | turned around at 11.5 |

At this strength nothing escapes at any radius up to 0.75 c: the escape speed
is above the sweep at R = 3, 5 and 9 alike, so this sweep cannot separate
1/√R from flat. Two things are already visible. The pull is much stronger
than the reservoir version at emission 2400 (the closed ledger transfers
about 24 momentum per quantum), and the thin open slab (z = 3) keeps rays
with a small z heading in the plane for tens of links while the octant field
leaked out of the plane every hop — so the ray density here falls closer to
1/r than 1/r², a compressed third dimension arising from straight-ray
transport in a thin universe. The eight-times weaker sweep (2048 quanta per
ray, everything else equal):

| R | 0.125 c | 0.25 c | 0.375 c | 0.5 c | 0.75 c | critical speed |
| --- | --- | --- | --- | --- | --- | --- |
| 3 | turned at 4 | turned at 7 | expanding, slowed to 9.5 | expanding, slowed to 12 | turned around at 17 | above 0.75 c |
| 5 | turned at 7 | expanding, slowed to 9.5 | turned at 12.5 | expanding, slowed to 14 | turned around at 19 | above 0.75 c |
| 9 | expanding slowly | turned at 14 | turned at 16.5 | expanding, slowed to 18 | escaped by tick 32 | 0.5-0.75 c |

("Slowed to" compares with the free path: at 0.5 c a free body is 30 links
further out after 60 ticks.) Between R = 3 and R = 9 the critical speed drops
by a factor between 1 and 1.5, where the three-dimensional reservoir sweep
gave Newton's 2.0 (0.62 → 0.31 c). Flatter than 1/√R, as the in-plane ray
density of the thin slab predicts — but the six-speed sweep resolves the
bracket only to "above 0.75 c" at R = 3 and 5, so this is a lean, not a
measurement; a finer sweep between 0.75 c and c, and the same coupling in a
thick box, are what would settle it. The kicks are discrete (a body meets a
whole ray or none), which is why 0.5 c can still be expanding while 0.75 c has
turned.

### In a closed universe (`... periodic ...`)

Universe24 is closed. With a periodic boundary the field never leaves, so the
load grows with the age of the universe under a *constant* source, and the
train laps the row: the eye sees the same signal at successive epochs. First
attempt (37 × 25 × 5 periodic, mass twelve rows from the path, constant
emission 18000, `straight` phases): the first seven bodies arrived at ticks
21-27 with gaps of one, the other five never arrived in 110 ticks and nobody
completed a second lap. The stall is the axis-ray artifact of `straight`
phases: the mass's y-axis ray runs down the column x = 18, crosses the train's
row and (with its wrapped images) piles load on that one node, so every body
reaching it after tick 27 waits there. With `rotate` phases (Manhattan-isotropic
field) all twelve bodies complete lap 1 at ticks 21-32 with gaps of one, and
then nobody completes a second lap within 110 ticks: the accumulated load
crossed the budget everywhere at about the same age, so every hop slowed
together. That is the closed universe's signature — a uniform slowdown of all
light with age, not a local one — and to read it as a redshift the eye must
compare laps, which needs a source weak enough for the slowdown to deepen
gradually. With `rotate` phases at emission 6000 and budget 20 the field
reached the row at tick ~30 (axial propagation is c/3 under `rotate`) and then
cost 80-189 per hop: the wrapped Manhattan-shaped field piles up at the
diagonals and the antipode (stock 152 at x = 0 and 36, zero at x = 20), so the
train crawled at one hop per nine ticks and never lapped.

With the mass emitting **rays** as the computation field (a ray field may now
be the computation field; its delivered ray arrivals per travel port are the
load) the closed box finally shows the stretch inside one lap:

| body | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arrival tick | 21 | 22 | 23 | 24 | 25 | 26 | 27 | 33 | 93 | 93 | 105 | 131 |
| gap | | 1 | 1 | 1 | 1 | 1 | 1 | 6 | 60 | 0 | 12 | 26 |

Seven bodies pass before the accumulated ray density (512 rays per tick with
nowhere to go) crosses the budget; the later ones meet one or two extra
cycles per hop and the train stretches to z ≈ 9 over the lap, in bunches. For a
load growing linearly with age, a train emitted with unit spacing and crossing
D links arrives with spacing 1 + D × (growth rate per hop): the redshift is
proportional to distance at a fixed reception epoch — a Hubble-like relation
from closure alone, with no recession — and the same delay stretches durations.
What the lattice adds is quantization: nothing until the load crosses a budget
multiple, then whole extra cycles at once.

## 6. Dark matter and dark energy: what the model does and does not offer

Dark energy stands in for a distance-redshift relation that recession alone
does not fit. Probe 5 shows the model has a relation of its own: delay growth
along the path stretches signals without any recession or expansion term. It is
quantized and it does not accelerate by itself; whether it can match an observed
Hubble relation is a question of how the field fills space over time, which the
configuration sets.

Dark matter stands in for rotation curves that stay flat: a force falling as
1/r, i.e. an enclosed source growing with r. Nothing in the generic transport
produces that. The octant far field falls faster than 1/r² on the lattice axes
(probe 1), the ray field as 1/r², and a field that re-radiates from every node
reaches a diffusive steady state whose flux is again 1/r². A self-sourcing
field (stock creating stock, a "field gravitates" rule) either decays away
(Yukawa, steeper) or grows without bound; neither is a 1/r force. The
unlocalized quantum sector is the opposite of dark matter: it neither attracts
nor falls (probe 3). The escape-speed-against-radius sweep in probe 4 is the
model's own rotation-curve test and comes out Newtonian in three open
dimensions (v_esc ∝ 1/√R within resolution) — and flat when the third
dimension is closed: in the 61 × 61 × 3 periodic slab the momentum lost along
an outward path is the same from R = 3, 5 and 9 under the identical coupling.
So the model does have a dark-matter substitute, and it is not extra mass: a
1/r² law whose far field is represented in one dimension fewer. That is a
representation hypothesis about galaxies, not a derivation; the lattice shows
only that the flat curve follows from the compression alone.

## 8. Gravity in an interferometer (`kerengonen_interferometer.py`)

Does the model's gravity leave a phase? The two-lamp Kerengonen interferometer
of main's double-slit probe (lamps in phase at y = ±3, a screen of absorbers
eight links on) with a mass emitting an outward computation field beside lamp
B's rays to the upper screen. The lower wing is lit by rays that never pass
the mass and is the control. Four worlds, same lamps and screen; two of them
use the new opt-in engine rules `ray_delay` (rays wait at a loaded Node the
intervals its load alone prices) and `ray_phase_per_tick` (a waiting
Kerengonen ray advances its phase per waiting interval as well as per link):

| screen y | no mass | A fixed clock | B ray_delay | C phase per tick |
| --- | --- | --- | --- | --- |
| −12 … 8 | fringe | identical | identical | identical |
| 9 | 416 | 416 | 506 | 388 |
| 10 | 552 | 552 | 485 | **211** |
| 11 | 528 | 528 | 613 | 366 |
| 12 | 436 | 436 | 556 | 427 |
| lower wing total | 6176 | 6176 | 6176 | 6176 |
| upper wing total | 6176 | 6176 | 6404 | 5636 |

- **A, the rules as they stood:** every screen Node identical to the world
  without the mass. Rays on the fixed field clock ignore computation load
  entirely; the model's gravity was invisible to interference — the clock
  composition gap of main's curvature probe, as a fringe.
- **B, rays delayed, phase per link:** only the rows whose lamp-B rays cross
  the loaded region change, and they gain quanta (6404 against 6176): a
  delayed ray arrives when its partner from lamp A has passed, meets no
  coherent opposition, and is absorbed whole. Delay without phase is
  decoherence — the fringe is washed out, not moved.
- **C, phase advancing on waits as well:** the same rows now darken (y = 10
  from 552 to 211, the wing from 6176 to 5636): the waited intervals carry
  phase into the recombination and the fringe shifts by the waits, in whole
  steps. This is the gravitational phase — the COW signature — and it appears
  only when the wait counts as phase.

The single-ray test (`tests/test_ray_delay.py`) fixes the rule exactly: a
ray delayed 11 intervals arrives with the undelayed phase under B and with
phase +11 mod 8 = 3 under C. Both keys are declared timing rules; the probe
shows which one puts the computation clock and the wave in the same
measurement.

## 9. Forward replay and a collision restart (`time_symmetry.py`)

**One number.** The seeded quantum world (`examples/quantum/native_quantum.json`,
seed 17) drew one ticket, 16, in eight ticks. Logged aside and supplied back as
an explicit `tickets` stream in place of the seed, the world reproduces the
same exposed snapshot at every tick (digests `d73f16ddc584`, `10bc49bba7f7`,
… identical); run again from the seed alone, identical again; seed 18 diverges
at tick 5, the first draw. Any earlier point of the history — ticks 2, 4, 6 —
is reached by restarting the original configuration and executing forward.
This example uses one ticket; other runs can require more. Snapshot equality
does not compare every private queue or counter and is not inverse evolution.

**Reversal.** The elastic collision of two equal masses at link speed, run 12
ticks forward (they meet at x = 10 on tick 5 and swap on tick 6), then a fresh
world starts at the final positions with negated momenta and runs 12 ticks:

| | Body A | Body B |
| --- | --- | --- |
| start | x = 5, p = +120 | x = 15, p = −120 |
| tick 12 forward | x = 3, p = −120 | x = 17, p = +120 |
| 12 ticks after reversal | x = 5, p = −120 | x = 15, p = +120 |

The bodies retrace their paths, swap back at the same Node and arrive at their
starting positions with their starting momenta reversed in this supplied
equal-mass, link-speed example. The restart does not preserve or invert arbitrary
private queues, counters, fields or fractional routing state. The outward field
has no tested inward law and truncated absorption is not a bijection. Forward
replay and this finite collision return are separate claims.

## 7. Focus and computing less

The repository's [Focus](../../docs/QUANTUM_FOCUS.md) is an octree over
regions used to narrow one ticket to one quantum event; it is
probability-preserving by contract and never touches field transport, so it
cannot by itself make the field cheaper or flatter. What already computes
less is the ray transport (only the Nodes a ray crosses are active: the ray
lensing runs took minutes where the octant runs took most of an hour), and
main's [isotropy probe](../isotropy-probe/README.md) shows why the octant
field is the wrong thing to make cheap anyway: its stock falls exponentially
along an axis and only the shell mean is 1/r².

The Focus region machinery (`Region3D`, `split_region`) is, however, exactly
the data structure a far-field compression would use: represent the field
beyond a radius L from each source at block resolution (blocks of side
growing with distance, six ports per block, populations aggregated by the
same integer split), let a carrier inside a block read the block's flux, and
refine only the blocks that carriers occupy. Two things follow at once. The
active-node count for a filling field drops from the volume to roughly the
surface of the refined region, which is the computing-less the probes need;
and beyond L the field is carried in a lower-dimensional representation, which
probes 4 and 6 show yields a flat rotation curve with the transition at L.
This is an engine change (a multi-resolution lattice with conserved
integer aggregation), not a configuration; it is the natural next PR, and it
is the point at which "compute less" and "dark matter" become the same
mechanism.

## What these probes do not show

They do not derive gravity, the 1/b lensing law, the factor two of general
relativity, Lorentz dilation or quantum matter in a gravitational field. They
locate exactly which parts follow from the generic engine (exact momentum
bookkeeping, the 1/v² velocity law, directional delay) and which need a new
declared rule (a self-excluding load, a delay-aware gate clock).
