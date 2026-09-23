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
