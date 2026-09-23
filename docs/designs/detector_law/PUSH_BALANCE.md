# The push balance of a free pair on the continuum pace: the four derivations behind five's three outcomes (the physics-rule reviewer, 2026-09-23; docs only, COMPUTATION)

Written on the Boss's word of about 11:15Z, after the reviewer's six
lines of 11:05Z on the free pair (record 1352's candidate clock rule and
the gate of [DESIGN.md](DESIGN.md) section 8b). It stands beside the
chief physicist's design and is cited by it; it edits nothing of his.
Every number here is a COMPUTATION on the continuum pace of the rule
(the scalar wave at the pace c = 1 / sqrt 3 Links per interval, the pair
[1, 3] of DESIGN.md section 2), never a measurement, never a lattice
run; the lattice's own residual at a given wavelength (DESIGN.md 6.0 A:
0.8, 0.4, 0.2 percent of c at 12, 16, 24 Links) is stated apart where it
matters. No pin moves; the pins of five stay as
[PINS.md](PINS.md) declares them, rows (e) and (f).

## 0. Symbols and the question

- c (the rule's pace): 1 / sqrt 3 Links per interval, a scalar.
- beta_c (the object's pace over c): an object stepping one Link every
  k intervals has beta_c = 1 / (k c); 0.5774 at k = 3, 0.4330 at k = 4.
- gamma_m (the medium's Lorentz factor): 1 / sqrt(1 - beta_c^2); 1.2247
  at k = 3 (gamma_m^2 = 1.5000), 1.1094 at k = 4 (gamma_m^2 = 1.2308).
- f_0 (the declared rest frequency of an object's clock, periods per
  interval), lambda_0 = c / f_0 (its rest wavelength), k_0 = 2 pi /
  lambda_0 (the rest wave number), all scalars.
- L (the pair's separation, Links), L_0 its rest value, m (the count of
  half wavelengths between the objects, a whole number the pair keeps).
- N_0 (the rest cycle) = 2 L_0 / c intervals: the round trip of a
  record from one object to the other and back.
- h (the quantum); a click hands the receiving object the momentum h k
  along the arriving direction (DESIGN.md section 5), a vector along
  the Link of arrival.
- r and phi (the object's re-emission: the fraction of the arriving
  amplitude it re-inserts and the phase it adds), the fourth value of
  the re-emission parameter of DESIGN.md 1.1 (the phased partial
  re-emission).
- I (an intensity, the wave's energy flux, in the offer's units), a
  scalar; I / c is its momentum flux.

The question of five: a pair of foreign objects, free to step, set in
motion at beta_c: does the wave law between them hold their separation,
at what shape, at what frequency, and what does the pair's own clock
then read along and across its motion against Einstein's 1 and 1?

## 1. The radiation pressure on a scatterer: a relay pair is not bound

A wave of intensity I arriving at an object along one Link carries the
momentum flux I / c. The object transmits I_t, reflects I_r (re-emits
backward) and absorbs I_a (books it as its offer), with I = I_t + I_r +
I_a. The momentum the object keeps per interval is what arrived less
what left:

    F = (I - I_t + I_r) / c = (2 I_r + I_a) / c >= 0,

directed away from the source, at every separation, with equality only
for an object that neither reflects nor absorbs. In three dimensions
the same holds with the object's scattering cross-section in place of
I_r and I_a. This is the whole push on an object that only relays (one
with no clock of its own: it re-inserts what it receives, at the
arrival's phase shifted by phi): a push away from its partner.

The other force a wave can put on a small object is the gradient force
F_g = -(1 / 2) Re(alpha) grad(I), alpha (the object's response, the
re-emitted amplitude per unit arriving amplitude, a complex number
whose real part is the reactive response and whose imaginary part the
dissipative one). In one dimension a travelling wave has grad(I) = 0,
and the standing pattern that forms from the arriving wave and the
object's own reflection has, at the object's position, a phase locked
to the object's own phi, not to L: with the arriving amplitude a and
the reflected r a e^(i phi), the intensity near the object is a^2 (1 +
r^2) + 2 a^2 r cos(2 k (x - x_object) + phi), whose gradient at the
object is -4 a^2 r k sin(phi), a constant set by the declaration, the
same at every L. So a relay pair feels a push apart of (2 I_r + I_a) / c
and a constant of its own phi, and no restoring force: it is not bound,
and its loop frequency adjusts as it drifts to keep the round-trip
condition. COMPUTATION; this answers DESIGN.md 8b (i) and (iv): the
first rung's ordering is not a force, and a pure receiver or relay in a
symmetric standing pattern is pushed, not held.

**Correction (2026-09-23, 11:40Z, the reviewer's own line; the chain's
closed form in `check_pair_force.py` of the reviewer's scratchpad,
HOST 1.5 s, floats, two soft sources emitting continuously at the clock
[64, 55], lambda_0 = 31.75 Links, the force read as the total field's
stress T = 3 (motion)^2 + (strain)^2 four Links to the left of emitter 1
less four to its right).** The paragraphs above hold for an object that
does not emit coherently with its partner. An object that inserts its
own train at the pair's frequency with a fixed phase (a declared clock,
or the relay of section 3, which re-inserts the received train at a
locked phase) is a coherent emitter, and two such emitters ARE bound by
the interference of the own emission with the partner's arriving wave,
the cross term of the stress: in one dimension, for two in-phase
emitters of travelling-wave stress A^2 each,

    F_1 = 2 A^2 cos(k L)     (toward the partner; the chain reads it within 2 percent at every L from 64 to 108 Links: +1.99 at 64, -1.98 at 80, +1.97 at 96, the continuum +1.99, -1.99, +1.98),

zero and stable at L = (m' + 1 / 4) lambda_0 (71.4 and 103.2 Links),
zero and unstable at (m' + 3 / 4) lambda_0 (87.3), maximal repulsion at
(m' + 1 / 2) lambda_0: L_0 = 80 = 2.52 lambda_0 is that point for
in-phase clocks. With the second clock a quarter period behind the
force is 2 A^2 cos(k L - pi / 2), zero and stable at 79.4 Links: L_0 =
80 at m = 5 holds with that phase declared. So what section 2 needs is
not a resonance: it is the object's own coherent emission overlapping
the partner's arrival at its Node, at a declared relative phase, and a
push read from the TOTAL field. Read with the two records kept as
separate fields and the stress summed per field, the chain gives 0.000
at every L: the cross term is gone and only the scatterer's own
reflection pushes, always apart (2 R A^2, R = 0.086 for a thin
scatterer at n_o = 2). That is the chief physicist's finding 2 of
11:25Z (the pair separating at rest on the chain under DESIGN.md 5.1
(a) and (b) as declared: the records pushed per field, and 2-period
trains of 110 intervals that never overlap the partner's arrival at L /
c = 139), not a missing resonance. Section 2's force and section 5's
case (ii) are read with this correction. COMPUTATION.

## 2. The coupled-oscillator force: an object with a resonance is bound at every half wavelength

An object with a natural frequency of its own (an oscillator at omega_0
= 2 pi f_0 whose re-emission is resonant, its reactive part set by the
declared phase) is a different thing. Two such objects coupled through
the wave between them have collective modes: the field of A at B is A's
oscillation delayed by L / c, so the pair's normal frequencies are

    omega_(+-) = omega_0 +- g cos(k L)     (one dimension; g proportional to r omega_0),
    omega_(+-) = omega_0 +- g cos(k L) / (k L)     (three dimensions),

the in-phase and antiphase modes, g (the coupling) proportional to the
re-emission strength r. The energy of the pair in a mode depends on L
through the cosine, and the force on each object is the gradient of
that energy:

    F = -dE / dL = +- h_bar g k sin(k L)     (one dimension),

with equilibria wherever sin(k L) = 0, that is at L = m lambda_0 / 2
for every whole m, alternately stable (dF / dL < 0) and unstable: for
the in-phase mode the stable set is one parity of m, for the antiphase
mode the other, so the declared phase phi (which mode the pair's
re-emission selects) fixes whether the pair sits at the pattern's nodes
or antinodes. What fixes the equilibrium, then: m (an initial
condition the pair keeps, the count of half wavelengths), f_0 (the
scale, lambda_0 / 2 per count) and phi (which parity is stable). In one
dimension (the chain) the coupling does not fall with L and every
count m binds alike; in three dimensions it falls as 1 / (k L) and the
binding weakens with m. This is the coupled-dipole binding of two
resonant scatterers (the form known in optics as optical binding), and
it is the restoring force that DESIGN.md 8b (iv) asserted and lacked:
it exists for every object that emits coherently at the pair's
frequency with a fixed phase (a declared clock, or the relay that
re-inserts at a locked phase), and never for a receiver that does not
emit (section 1 with its correction). COMPUTATION.

## 3. The relay's Doppler integral through the acceleration: f_0 / gamma_m^2

Take the candidate clock rule read literally: in motion the object has
no clock of its own, and the train it inserts continues the oscillation
it received (a relay at the arrival's phase). At a constant pace the
pair reads each other unshifted (DESIGN.md 8b (iv)), so a relay pair
keeps whatever frequency it has. During the acceleration from rest to
beta_c it does not. Along the motion, with the pair carried rigidly by
equal pushes (each object gaining the same increment dv per leg), the
front object receives the rear's wave with the factor (c - v_r) / (c -
v_e) (the source at v_e emits ahead at f c / (c - v_e) in the medium;
the receiver at v_r reads that times (1 - v_r / c)), and the rear then
receives the front's return with (c + v_r') / (c + v_e'); with v_r =
v_e + dv on each leg the round trip multiplies the frequency by

    (1 - dv / (c - v)) (1 + dv / (c + v)) = 1 - 2 v dv / (c^2 - v^2) + O(dv^2),

and the same factor holds across the motion (there the wave travels
tilted by sin theta = v / c and the receiver's velocity projects on it
as v^2 / c, which gives 1 - dv v / (c^2 - v^2) per leg, the same per
round trip). Summing the legs over the acceleration,

    ln(f / f_0) = - integral from 0 to v of 2 v dv / (c^2 - v^2) = ln(1 - v^2 / c^2),

so f = f_0 (1 - beta_c^2) = f_0 / gamma_m^2, along and across alike.
The standing condition of 8b (iv) then gives the shape at that
frequency: L_along = m (lambda / 2) / gamma_m^2 with lambda = lambda_0
gamma_m^2, so L_along = L_0 (no contraction), and L_across = m
(lambda / 2) / gamma_m = gamma_m L_0 (an expansion across); the round
trips 2 L_0 gamma_m^2 / c along and 2 (gamma_m L_0) gamma_m / c across
are both gamma_m^2 N_0. COMPUTATION. A relay pair carried rigidly ends
with its cycle gamma_m^2 N_0 in both arms: the Michelson-Morley null,
and neither of five's "1 and 1" outcomes.

## 4. The boost of the rest pair: the covariant object gives Lorentz's member

The rule of DESIGN.md section 2 is, on the continuum pace, the wave
equation d^2 u / dt^2 = c^2 (d^2 u / dx^2 + d^2 u / dy^2 + d^2 u /
dz^2), which is invariant under the Lorentz transformation with the
pace c: if u(x, t) is a solution, so is u(gamma_m (x - v t), y, z,
gamma_m (t - v x / c^2)). The rest pair (two objects at rest at L_0,
oscillating at f_0, the standing pattern between them) mapped by that
transformation is therefore an exact solution moving at v, with the
separation L_0 / gamma_m along and L_0 across, the oscillation at f_0 /
gamma_m in the medium's time, and the round trips 2 (L_0 / gamma_m)
gamma_m^2 / c = gamma_m N_0 along and 2 L_0 gamma_m / c = gamma_m N_0
across: the two arms equal (the null), the pair's clock slow by gamma_m
in the lab's time (the muon in flight, Ives and Stilwell), Lorentz's
member, nature's. This holds provided the objects' own laws are also
invariant under the same transformation: an object whose rest frequency
is itself a bound cycle of the same waves (an object made of the
Inside) transforms with the pattern; an object whose clock is a
declaration ticking in the lattice's intervals does not, and that
object selects section 5's member (i) instead. COMPUTATION; the
statement is the wave equation's covariance, not a fit.

## 5. The members' table at k = 3 and k = 4

The standing condition alone (DESIGN.md 8b (iv) and (v)) is a
one-parameter family: for the pair's frequency f in the lattice's
intervals the round trip is m / f along and across for any f, so the
shape and the cycle are fixed only once the law of the object's
frequency is. Four cases, each self-consistent at a constant pace:

| Case (the law of the object's frequency) | f / f_0 | L_along / L_0 | L_across / L_0 | The cycle over N_0, along and across | Five's ratios N_par / N_0, N_perp / N_0 (in the object's own count, the lattice's intervals) | The lab's dilation read against nature's gamma_m |
| --- | --- | --- | --- | --- | --- | --- |
| The medium (no binding; the pair held rigidly at L_0; the fixed-separation clock of DESIGN.md 6.5) | 1 | 1 | 1 | gamma_m^2 along, gamma_m across | k = 3: 1.500 and 1.225; k = 4: 1.231 and 1.109 | no clock of the pair's own to read |
| (i) The declared clock: f_0 ticks in the lattice's intervals, the re-emission resonant (section 2's force holds the pair at the retarded pattern's nodes) | 1 | 1 / gamma_m^2 (0.667; 0.812) | 1 / gamma_m (0.816; 0.901) | 1 and 1 (N_0 in both arms) | 1.000 and 1.000 at both k | 1 against 1.225 (k = 3), 1 against 1.109 (k = 4): FAIL |
| (ii) The relay: no clock in motion, the inserted train continuing the received oscillation; carried rigidly to beta_c (section 3) | 1 / gamma_m^2 (0.667; 0.812) | 1 | gamma_m (1.225; 1.109) | gamma_m^2 and gamma_m^2 | k = 3: 1.500 and 1.500; k = 4: 1.231 and 1.231: FAIL of five | gamma_m^2 against gamma_m: 1.500 against 1.225, 1.231 against 1.109: FAIL |
| (iii) The covariant object: the rest frequency itself a bound cycle of the Inside (section 4) | 1 / gamma_m (0.816; 0.901) | 1 / gamma_m (0.816; 0.901) | 1 | gamma_m and gamma_m | 1.000 and 1.000 at both k | gamma_m against gamma_m: PASS |

The two numbers in each cell are k = 3 then k = 4. In case (i) and case
(iii) five reads 1 and 1; only case (iii) also reads the lab's dilation.
In case (ii) the relay is bound too, at the parity its locked phase
sets (section 1's correction), so "carried rigidly" is what its binding
gives; five then reads 1.500 and 1.500, its FAIL. A pair whose records
are pushed as separate fields, or whose trains never overlap, drifts
apart in every case: that reading names the push's form, not the
member.

## 6. What the chain script must read, and the candidate clock rule

The balance is degenerate in L at every order and is not degenerate in
f. The one reading that names the member is the pair's oscillation
frequency in the lattice's intervals (the zero crossings of the wave
between the objects) after a rest pair is pushed to beta_c by clicks
and settles, read beside its separation:

| Reading at k = 3 | Case (i) | Case (ii) | Case (iii) |
| --- | --- | --- | --- |
| f / f_0 | 1.000 | 0.667 | 0.816 |
| L_along / L_0 | 0.667 | 1.000 | 0.816 |
| L_across / L_0 | 0.816 | 1.225 | 1.000 |

The three are far apart and the band +- 0.03 of PINS.md rows (e) and
(f) separates them.

The candidate clock rule of record 1352 (the declaration a rest value
only; in motion no declared clock; the insert follows the receive of
the object's own record; the clock is the cycle of that record in the
object's own count) passes the three tests as a sentence: generic (no
family name, no kind), vector (a comparison of the record's age against
the train and the closed count, no arithmetic on the state vector),
local (the object's own record at its own Nodes). As written it makes
the object a relay, case (ii), and the line it needs names the object's
resonance in motion. Two lawful completions: (A) "the rest value stays
the object's resonance in motion, ticking in the lattice's intervals"
(case (i); buildable now; the lab's dilation FAIL by design, honestly
predicted), or (B) "the object's resonance is itself a bound cycle of
the Inside, so that it transforms as the pair does" (case (iii); five
and the lab's dilation both by the wave equation's own covariance;
every foreign object then a composite of the law, the atom's route: a
program, not a sentence). A third candidate, the model owner's (his
record 1366 of docs/LOG_2026-09-20.md: a foreign object is a Node of
the same law with a declared coefficient; its cycle time is determined
by the Inside): (C) "the object's clock is the bound mode of the wave
at its own Node under its declared coefficient pair; its rest period a
computation of the pair, not a declaration", the one form under which
the frequency law would be a computation and not a declaration; section
8 computes what it gives. The choice is the model owner's; nothing here
enters the law.

## 7. The kinds, and what is not here

Every number above is a COMPUTATION on the continuum pace; the
declared inputs are f_0, m, phi, r, k and L_0 (DECLARATION). No pin of
PINS.md moves: rows (e) and (f) keep 1 +- 0.03 and the outcomes named
before the run; the lab's dilation row keeps its predicted FAIL under
case (i). What this file does not do: it does not run the engine (the
closed-form checks on the chain of section 1's correction and of
section 8 are float scripts of seconds in the reviewer's scratchpad,
named where their numbers appear), it does not carry the lattice's
dispersion into the numbers of sections 1 to 6 (the shifts at 24 to 32
Links are about one percent, DESIGN.md 8b as gated; the band's phase
pace at lambda_0 = 31.75 is 0.99891 c), and does not
decide the push-to-cadence rule (how the pair reaches beta_c), which
sets the path and not the member; the frequency's law sets the member.

## 8. The third candidate (C): the object's clock as the bound mode of its own Node

Written on the Boss's order of about 11:20Z after the model owner's
challenge (about 11:20Z: neither (A) nor (B) follows from the push
balance), his record 1366. Agreed, and sharper: the balance proves that
under the rule as it stands the frequency law is a DECLARATION whatever
its form; (C) asks whether the rule itself can supply it. Every number
a COMPUTATION on the chain (the closed forms and two float scripts of
about one second each, `check_bound_mode.py` and
`check_massive_well.py` in the reviewer's scratchpad); nothing enters
the law; no pin moves.

**8.1 The coefficient form and its band.** A foreign object's Node runs
the rule with the pair q = [num, den] in the form the pins script
implements (DESIGN.md 4.1 and 5.1 (b), `chain_step`): 3 den a_next + r'
= num (the six-neighbour sum) + 6 (den - num) a_now - 3 den a_before +
r, that is a_next - 2 a_now + a_before = (q / 3)(the six-neighbour sum -
6 a_now), the Laplacian at the local pace c / n_o, n_o = sqrt(den /
num), with no on-site term (the sentence "the pair on the six-neighbour
term" without the compensation 6 (den - num) a_now would add the
on-site term 2 (1 - q) a_now, a local mass: a barrier for q < 1, a
growing instability for q > 1; the script is right, the sentence must
carry the compensation). The free rule's band is acoustic: 4 sin^2
(omega / 2) = (4 / 3) sin^2 (k / 2) on the chain, from omega = 0 with
no gap to the top omega_max = 2 arcsin(1 / sqrt 3) = 1.231 per
interval, the period 5.10 intervals at the lattice's shortest wave (two
Links). A pair with q >= 3 is unstable (the local pace at or above one
Link per interval).

**8.2 One Node: no bound mode below the band, one above it.** A
localized mode a_j = A e^(-kappa |j|) e^(i omega t) needs, away from
the Node, -4 sin^2 (omega / 2) = (2 / 3)(cosh kappa - 1) > 0 for real
kappa, which no real omega satisfies: below an acoustic band there is
no bound state for any q < 1 (n_o > 1, the slower Node). A slow Node is
a scatterer with a leaky resonance of quality about one: the Fresnel
reflection ((n_o - 1) / (n_o + 1))^2 = 1 / 9 at n_o = 2, and with the
grain floor lambda_0 / n_o >= 12 Links (DESIGN.md 6.7) the index is
capped at 2.6 for lambda_0 = 32 and the reflection at 0.21. Above the
band the staggered mode a_j = A (-1)^j e^(-kappa |j|) satisfies, from
the free Nodes, 4 sin^2 (omega / 2) = (2 / 3)(1 + cosh kappa), and from
the object's Node 4 sin^2 (omega / 2) = (2 q / 3)(1 + e^(-kappa)), so

    q (1 + e^(-kappa)) = 1 + cosh kappa,

with a root kappa > 0 for every q > 1 on the chain (the one-dimensional
result: any faster Node binds one mode) and none for q <= 1:

| q (n_o) | kappa (the extent 1 / kappa, Links) | omega_b per interval | the period, intervals |
| --- | --- | --- | --- |
| 1.1 (0.95) | 0.182 (5.5) | 1.237 | 5.08 |
| 1.5 (0.82) | 0.693 (1.4) | 1.318 | 4.77 |
| 2.0 (0.71) | 1.099 (0.9) | 1.460 | 4.31 |
| 4.0 (0.50) | 1.946 (0.5) | 2.122 | 2.96 |
| 9.0 (0.33) | 2.833 (0.35) | none real | the mode grows (q >= 3) |

On the three-dimensional GameBoard the same mode needs q above a
threshold greater than 1 (the lattice Green's function is finite at the
band's edge in three dimensions; the threshold not computed here).
Every such mode is faster than the band's top, 4 to 7 times faster than
the design's floor N >= 21 intervals (DESIGN.md 1.2 (b)), and it cannot
be carried by the band (omega_b above omega_max: no wave at its
frequency, only an evanescent tail). Under the rule as it stands, (C)
names no lawful object. COMPUTATION.

**8.3 The moving well, two separate points.** (i) A coefficient is a
medium and has a rest frame. The rule with the pair applied at the
object's moving Nodes is, on the continuum pace, the Galilean form
d^2 a / dt^2 = (c^2 / n^2 (x - v t)) d^2 a / dx^2, not the Lorentz
boost of the resting object (the boosted operator carries the cross
term d_t d_x, the Fresnel drag, first order in v). So an index
structure of any extent in motion (a slab; a Bragg cavity of about 240
Links at n_o alternating 1 and 2, which would hold a mode of high
quality at a lawful period N = 55) transforms as the rigid cavity of
section 3, the relay's member f_0 / gamma_m^2, unless its pair carries
the drag term by declaration, which is (B) under another name. The
band's dispersion at lambda_0 = 31.75 (the phase pace 0.99891 c, 0.11
percent) is not the issue. (ii) A mass term is a scalar and boosts as
one. Under a rule WITH a gap (a scratch variant, not the law), a_next =
2 a_now - a_before + (1 / 3)(a_E + a_W - 2 a_now) - mu^2 a_now, a well
of strength g at one Node (+ g a_now on-site) holds a true bound mode
below the gap at rest,

    omega_b^2 = mu^2 - 3 g^2 / 4,     the extent 2 / (3 g) Links     (c^2 = 1 / 3),

and the same strength g at the moving Node is the boost of a resting
well of strength gamma_m g (the delta's boost: g delta(x') = g
delta(gamma_m (x - v t)) = (g / gamma_m) delta(x - v t)), so the clock
read at the object is

    f / f_0 = (1 / gamma_m) sqrt((1 - gamma_m^2 eps) / (1 - eps)),     eps = 3 g^2 / (4 mu^2) (the binding depth),

Lorentz's member as eps -> 0, the deviation eps (gamma_m^2 - 1) / 2 =
eps / 4 at k = 3, a computation from the pair with no declared factor.
The chain confirms it to 0.1 percent (mu = 0.05; the well pushed from
rest to k = 3 over 6000 intervals by the accumulator of DESIGN.md 5.1
(a), the frequency read at the well's own Node by zero crossings over
3000 intervals):

| eps | g | the extent, Links | the rest period, predicted / read | f / f_0 at k = 3, read / predicted |
| --- | --- | --- | --- | --- |
| 0.04 | 0.0115 | 58 | 128.3 / 128.2 | 0.8077 / 0.8079 |
| 0.10 | 0.0183 | 37 | 132.5 / 132.4 | 0.7936 / 0.7935 |
| 0.25 | 0.0289 | 23 | 145.1 / 145.0 | 0.7460 / 0.7454 |

Lorentz's member 1 / gamma_m = 0.8165, the relay's 1 / gamma_m^2 =
0.6667. So (C) gives Lorentz's member without a composite and without a
declared factor, within five's band +- 0.03 for eps <= 0.1, on a rule
with a gap. COMPUTATION.

**8.4 Two such wells.** Below the gap the mode cannot radiate into the
band (omega_b < mu), so there is no coupled force of section 2 between
two wells; they bind only by the evanescent overlap of their modes (a
bonding and an antibonding pair, a molecule's form) at separations of
the order of the extent (37 Links at eps = 0.10), never at m lambda_0 /
2, and no light passes between them. (C) binds the pair and selects
Lorentz's member, but the bound pair is not five: it is not a light
clock, the standing pattern of DESIGN.md 8b does not exist for it, and
(C)'s object emits nothing a partner can click on. The light clock's
binding (section 1's correction) needs the massless band and the
object's own coherent emission; that force and (C)'s clock live on
different fields.

**8.5 The three tests, 1.1's existence condition, and the price.** The
sentence "the object's clock is the bound mode of its own Node's
coefficient; its rest period a computation of the pair, not a
declaration" passes the three tests as a sentence (one pair; the rule's
own verbs; its own Node and six neighbours), but it has a referent only
under a rule with a gap (8.2). Under such a rule it removes the lone
object's exception of DESIGN.md section 8: the self-click is the mode's
own oscillation at the Node, a return every period without a partner,
and 1.1's existence condition is met by the mode. Its price: the gap is
in the same field as light unless a second field is declared; a gap mu
moves light's pace by mu^2 / (2 c^2 k^2), one percent at lambda_0 = 32
for a clock of N = 400 intervals and ten percent for N = 130; so a
lawful (C) needs either a slow clock (N >= 400 at one percent on every
light pin) or a second, massive record kind with its own rule and a
declared coupling to light, a composite by another name. Either is a
change of the law: the model owner's word, outside the design and
outside this file.

**8.6 What the reduced run can carry, and the recommendation.** Not
(C) as a variant of five: on the massless rule there is no lawful bound
mode to declare, and the gapped rule is not the law. What the chain can
show as a scratch COMPUTATION for the owner's decision is 8.3 (ii)
itself (one well, pushed to k = 3, the clock read by zero crossings
against the closed form), in seconds; what it cannot show is the
three-dimensional threshold and the two-field coupling. The evening's
run carries (A) and the relay, re-formed by section 1's correction (the
total-field push, the declared relative phase, continuous emission or
trains spanning the round trip, the frequency read by zero crossings),
with the predictions of section 6 named before it; "separates" is
already excluded for a coherent pair at a stable parity by the closed
form and, if read, names the push's form. Recommendation, one line: the
design declares its frequency law for five as (A) with the FAIL of the
lab's row stated beside it, carries the relay as the control, states
(B) as the program nature demands, and records (C) as the model owner's
candidate for the law itself, the one form under which the clock is a
computation, with its two prices named (a gap, and a clock that is not
the light clock); the run decides between (A) and the relay, nothing
decides (C) but the owner's word on the gap. Lorentz's member "matches
nature", never "is nature".

**8.7 The gap's algebraic name and its integer form; the price of its
two placements** (the model owner's question of 11:56Z, record 1375,
through the Boss). The gapped rule of 8.3 (ii) is the discrete
Klein-Gordon rule: the wave rule with ONE self term, a declared pair
[p, q] on the Node's own present record, subtracted, mu^2 = p / q. On
the continuum pace it is d^2 a / dt^2 = c^2 (Laplacian of a) - mu^2 a;
on the lattice, with the six-neighbour sum S_6 and the remainder kept,

    3 a_next + r' = S_6 - 3 a_before + r - (3 p / q) a_now,

and in integers, the whole scaled by q so that the division is exact
with its remainder (as the coefficient form of 4.1 divides by 3 den),

    3 q a_next + r' = q S_6 - 3 q a_before - 3 p a_now + r,     r' in [0, 3 q),

the Boss's coefficient right, the division by 3 q rather than 3 the one
correction. It uses the six verbs only: the sum of the six, a multiply
by a declared pair, a subtract on the own record, the division with the
remainder kept; no seventh verb (the owner's rule of record 642). The
three tests as a rule: generic (one primitive with the declared
integers p, q; no family name, no kind), vector (the verbs above on the
state vector; no root, no float), local (the self term reads a_now at
the Node itself; the rest the six neighbours). A foreign object under
it is a Node with its OWN self pair [p', q'] in place of [p, q], the
well's strength g = p / q - p' / q' > 0 (a locally lighter Node), the
object's one declared parameter. What then follows by itself, on the
continuum pace with c^2 = 1 / 3: the bound mode omega_b^2 = mu^2 - 3
g^2 / 4 (real, that is bound and not growing, for g < 2 mu / sqrt 3),
its extent 2 / (3 g) Links, its rest period 2 pi / omega_b, the
Lorentz member of 8.3 (ii) by the rule's covariance (the KG operator
is invariant under the boost with c; the self term is a scalar), and
the bound pair's evanescent binding of 8.4. The integers stay bounded
as the massless rule's do: the dispersion 4 sin^2 (omega / 2) = (4 / 3)
sin^2 (k / 2) + mu^2 is stable for mu^2 <= 8 / 3, the conserved energy
is E of DESIGN.md section 2 with the term 3 mu^2 (sum of a_now
a_before) added, and the remainder's drift is the same as the wave
rule's; the scale q multiplies every intermediate (q S_6 at A = 2^20 and
q = 3600 is 2.3 x 10^10, inside int64 with room to q about 2^30). On
the lattice the closed forms hold for an extent well above one Link
(the chain's 0.1 percent at 23 to 58 Links, 8.3); the three-dimensional
GameBoard adds a threshold on g for one Node (the lattice Green's
function is finite at the gap's edge; not computed here); the chain
has none.

The two placements, priced for the owner's choice. (i) The gap in
light's own record, one kind: every light pin moves by the pace shift
mu^2 / (2 c^2 k^2), and the clock it allows is SLOWER than the gap
(omega_b < mu): at one percent on light at lambda_0 = 32 Links (c^2 k^2
= 0.0131), mu = 0.0162 and the gap's period is 388 intervals, so the
fastest clock is about 390 intervals and the run's forty cycles are
about 16,000 intervals; at lambda_0 = 48 the same mu shifts light by
2.25 percent; the flight table of the ray law (T_D = isqrt(3 |D|^2
Q^2), massless) and PINS (d) move by the same one percent (2 intervals
on 207, at the band's edge); every other row's band is wider than the
shift. (ii) A second, massive record kind beside the massless one: light
untouched, every light pin as declared; the price is two declarations
that the presence of the massive record does NOT supply by itself: (a)
what light sees, the index pair of 5.1 (b) on light's record at the
Nodes where the massive mode stands (its extent, 37 Links at eps =
0.10, a slab, not one Node; a rung on the mode's amplitude declaring
which Nodes), and (b) what the object feels, the push of light's stress
at those Nodes on the massive record's momentum (5.1 (a)'s form on the
mode). Neither coupling is in the rules of the two records; both are
the design's, and (b) is where the light clock's binding (section 1's
correction) would act on a (C) object. The Boss's recommendation of
(ii) as the direction to design under its own key: I recommend the
same, for the one reason that it keeps light and its pins whole; and
its first check is on the chain, in seconds, before any coupling: the
resting mode's period against 2 pi / omega_b and its member at k = 3
against 8.3's closed form, then the two couplings declared and gated.
Nothing here enters the law; the owner's word twice, on the gap and on
the placement. COMPUTATION for the numbers, DECLARATION candidates for
the rule and the couplings.

## 9. The model owner's form of (B): the object as the set of Nodes at which its own record is identical

Written on the Boss's orders of 11:40Z and 11:46Z (the owner's records
1370 and 1371: a foreign object is not one Node; a Node holds bounded
integers, so a mass above the bound is several Nodes, and they are one
body by one record held identically at all of them; its declared N
gives its extent at rest, s = N c / 2 = lambda_0 / 2 Links, the Nodes
its own record crosses in one cycle; its click in the Outside is the
agreement of its cells). Every number a COMPUTATION on the continuum
pace or from the tables above; the owner's words DECLARATION candidates;
nothing enters the law.

**9.1 Which of (A) and (B) gives Lorentz.** Section 5's table: only
case (iii), the covariant object, reads both five's 1 and 1 and the
lab's dilation gamma_m; case (i), (A), reads five's 1 and 1 and fails
the lab's row; case (ii) fails both. So (B) is the only candidate for
Lorentz and (A) is its control, as the Boss answered the owner; and (B)
gives Lorentz by construction (the covariance it declares), which is
why its wall is the question: what makes the object covariant.

**9.2 Two objects hide in "identical".** (B1) Contiguous Nodes holding
the identical record (the owner's 11:44Z form: several Nodes, each
returning and receiving the same thing): a block with no gradient
inside, one Node replicated, moved as one by one momentum integer.
(B2) Separated cells at the like points of the object's own standing
pattern (the Boss's reading), lambda_0 / 2 apart at rest (the pattern's
sign alternating between them, identical up to the sign; lambda_0 apart
if the sign is required too), each a Node that re-inserts the record it
receives at the identical phase. Both satisfy the sentence; they are
different objects with different pushes, and the sentence must name
which.

**9.3 The three tests on the sentence** ("a foreign object is the set
of Nodes at which its own record is identical; its mass is their count;
its clock is the cycle of that record across them; nothing else
declared"). Generic: PASS (no family name, no kind; one record, one
count). Vector: PASS (a comparison of identity, the rule's own verbs,
no root). Local: NOT as it stands for (B2), because "identical" between
Nodes lambda_0 / 2 apart is a comparison across non-neighbours that no
Node can make; its local form is the phase lock at each cell (a cell
belongs to the object when the record arriving at its own Node is
identical in phase with the one it holds and re-inserts), and that
form is a relay's condition, met at any separation the pattern allows;
PASS for (B1), where the identity is between neighbours. The mass as
the count is a declaration of the design (the local integer contract's
reason for it agreed); the clock as the record's cycle across the
cells is section 6's candidate rule restated for an extended object.

**9.4 Does the sentence contain the resonance.** No. A cell that
re-inserts the identical record at the identical phase has no
restoring term of its own: its frequency is the received one, whatever
that is; it is a relay, the phase-continuous kind of section 3, not a
driven oscillator (a driven oscillator needs a natural frequency to be
driven against). The binding it can have is section 1's correction:
two cells that re-insert coherently at a locked phase are bound by the
cross term at the parity the phase sets; so relay ends CAN be bound,
and section 2's condition (each end resonating) is not needed for the
binding. It is needed for the member: the frequency the bound pair
settles to is set by the cells' law of frequency, and a relay's is the
round trip's. A pure mirror pair (the cells reflecting without
inserting outward) is not bound: the cavity's light pushes the mirrors
apart and nothing pulls.

**9.5 What the sentence predicts for the pair's frequency after the
push at k = 3.** For (B2), the cells relaying with the phase
continuous: section 3's Doppler integral, f / f_0 = 1 / gamma_m^2 =
0.667, the pattern's like points then lambda / 2 = (lambda_0 gamma_m^2 /
2) / gamma_m^2 = lambda_0 / 2 apart, so L_along / L_0 = 1.000 and L_across
/ L_0 = 1.225: the extent does not contract, the cycle is gamma_m^2 N_0
in both arms, five reads 1.500 and 1.500, its FAIL. For (B1), the block
moved as one: the medium row, the cycle gamma_m^2 N_0 along and gamma_m
N_0 across, five's 1.500 and 1.225, and the wave inside the block reads
f / f_0 = 0.667 as the rigid cavity's round trip. Neither is 0.816. The
Boss's (B2) argument (the boosted pattern's like points are 1 /
gamma_m closer, so the identity condition places the cells contracted)
holds for the boost of the rest solution, whose frequency at the cells
is f_0 / gamma_m; but the cells do not carry that frequency unless
their own law gives it: with relay cells the pattern they generate is
the one at f_0 / gamma_m^2, whose like points are not contracted, and
the identity condition places them there. The identity condition is
degenerate exactly as the standing condition of section 5: it is
satisfied at every L for whatever frequency the cells hold, and the
member is selected by the frequency law alone. The only cell that holds
f_0 / gamma_m is one whose rest frequency is a covariant bound cycle of
its own: (C) at the bottom (8.3 (ii)), which on the massless rule does
not exist (8.2). So (B) as the owner's sentence is (B2) with the
relay's member, and Lorentz's member needs (C), that is a gap.

**9.6 The confirmations and the variant.** (B1) rigid in motion is the
medium row, no Lorentz: confirmed. (B2) "the extent the wave's own" is
Lorentz's member only with the cells at f_0 / gamma_m; with relay cells
it is the relay's member and the extent stays L_0; its bottom is (C),
whose wall on the massless rule is not the dispersion near the band's
top but the absence of a gap (8.2: the single Node's only mode sits
above the band, and a slow Node has none). The added variant (the two
ends as one body with one shared momentum, the control against finding
2) has its outcome in the algebra already: the block moves at the
cadence of 5.1 (a), the wave inside reads f / f_0 = 0.667 at k = 3 and
five reads 1.500 and 1.225; it is worth seconds on the chain as the
calibration of the transport and of the zero-crossing reading, not as
a variant of five. Kinds: every number COMPUTATION; (B1), (B2) and the
sentence DECLARATION candidates for the owner; nothing entered.
