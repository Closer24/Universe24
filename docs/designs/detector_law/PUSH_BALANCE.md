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

and the force on emitter 2 is its mirror, F_2 = -2 A^2 cos(k L), so the
RELATIVE force is F_2 - F_1 = -4 A^2 cos(k L) cos(delta) for a declared
relative phase delta between the clocks (section 10, the chain reading
both emitters: +3.96 at 80, +2.40 at 84, -0.59 at 88, within 3 percent).
Second correction (12:16Z; the first version of this paragraph read
the parity from F_1 alone and had it backwards, and read a binding
into a quarter-period phase that has none): for IN-PHASE clocks the
stable separations are L = (m' + 3 / 4) lambda_0 (87.3 Links at 31.75;
88 at lambda_0 = 32) and the unstable ones (m' + 1 / 4) lambda_0 (71.4,
103.2); for ANTIPHASE clocks the reverse; a QUARTER-PERIOD phase gives
zero relative force at every L (the chain: 0.000 at all six L) and
pushes the pair as a whole by 4 A^2 sin(k L) sin(delta), a phased
array, not a binding. L_0 = 80 = 2.52 lambda_0 is an equilibrium for no
phase: the maximal repulsion in phase, the maximal attraction in
antiphase. The fixed points of a coherent pair are never at whole
numbers of lambda_0 / 2 (DESIGN.md 8b (iv)): they are at odd quarter
wavelengths, the parity by the sign of cos(delta). So what section 2
needs is not a resonance: it is the object's own coherent emission at
a FIXED relative phase (two declared clocks) overlapping the partner's
arrival at its Node, and a push read from the TOTAL field. The relay
of section 3 is excluded from this binding after all: its phase
re-locks to the arriving wave at every L, so its relative force -2 A^2
(k_f^2 + k_b^2) cos(phi) has no dependence on L (section 10.3), a
collapse, a drift or a separation by the declared shift phi, never an
equilibrium; the paragraphs above this correction stand for it. Read with the two records kept as
separate fields and the stress summed per field, the chain gives 0.000
at every L: the cross term is gone and only the scatterer's own
reflection pushes, always apart (2 R A^2, R = 0.086 for a thin
scatterer at n_o = 2). The chief physicist's finding 2 of 11:25Z
(the pair separating at rest on the chain under DESIGN.md 5.1 (a) and
(b) as declared) had two causes, both in the closed form and neither a
missing resonance: in-phase clocks at L_0 = 80 = 2.52 lambda_0 sit at
the maximal repulsion, and 2-period trains of 110 intervals never
overlap the partner's arrival at L / c = 139. (The first version of
this sentence named the push per field as a third cause; his section
already pushed by the total field, the two records kept separate only
for the own-record reading, so that cause is withdrawn, 12:22Z.) Section 2's force and section 5's
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
frequency with a FIXED relative phase (two declared clocks), and never
for a receiver that does not emit nor for a relay whose phase follows
the arriving wave (section 1 with its corrections; section 10).
COMPUTATION.

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
| (i) The declared clock: f_0 ticks in the lattice's intervals, the pair held by the coherent force at a fixed relative phase (section 10; the first version of this row put the pair at the retarded pattern's nodes, 1 / gamma_m^2, which is the pattern's geometry and not the force's equilibrium) | 1 | 1 - beta_c (0.423; 0.567), the equilibrium continued from rest by a slow ramp, section 10.2 | the across case not computed on the chain (the pattern's 1 / gamma_m is the geometry, not the equilibrium) | along: (1 - beta_c) gamma_m^2 = 1 / (1 + beta_c) = 0.634 at k = 3 by the round trip at the contracted L; across not computed | not 1 and 1 by the round trip: 0.634 along at k = 3, across not computed | 1 against 1.225 (k = 3), 1 against 1.109 (k = 4): FAIL |
| (ii) The relay: no clock in motion, the inserted train continuing the received oscillation; carried rigidly to beta_c (section 3) | 1 / gamma_m^2 (0.667; 0.812) | 1 | gamma_m (1.225; 1.109) | gamma_m^2 and gamma_m^2 | k = 3: 1.500 and 1.500; k = 4: 1.231 and 1.231: FAIL of five | gamma_m^2 against gamma_m: 1.500 against 1.225, 1.231 against 1.109: FAIL |
| (iii) The covariant object: the rest frequency itself a bound cycle of the Inside (section 4) | 1 / gamma_m (0.816; 0.901) | 1 / gamma_m (0.816; 0.901) | 1 | gamma_m and gamma_m | 1.000 and 1.000 at both k | gamma_m against gamma_m: PASS |

The two numbers in each cell are k = 3 then k = 4. In case (i) and case
(iii) five reads 1 and 1; only case (iii) also reads the lab's dilation.
In case (ii) the relay is not bound at any separation (section 10.3:
its phase re-locks to the arriving wave, its relative force has no
dependence on L), so "carried rigidly" is an assumption about the
pushes, as the first version said; a free relay pair collapses, drifts
or separates by its declared shift phi, and five then has no reading.
In case (i) the pair IS bound, at the odd quarter wavelengths, and in
motion its separation follows L_0 (1 - beta_c) (section 10.2), so the
row's "1 and 1" of the first version is withdrawn: five's along ratio
under (A) is set by the contracted separation, not by the pattern; f /
f_0 = 1.000 still names the member. A pair whose records are pushed as
separate fields, or whose trains never overlap, drifts apart in every
case: that reading names the push's form, not the member.

## 6. What the chain script must read, and the candidate clock rule

The balance is degenerate in L at every order and is not degenerate in
f. The one reading that names the member is the pair's oscillation
frequency in the lattice's intervals (the zero crossings of the wave
between the objects) after a rest pair is pushed to beta_c by clicks
and settles, read beside its separation:

| Reading at k = 3 | Case (i) | Case (ii) | Case (iii) |
| --- | --- | --- | --- |
| f / f_0 | 1.000 | 0.667 | 0.816 |
| L_along / L_0 | 0.423 (section 10.2; the first version's 0.667 withdrawn) | no equilibrium (section 10.3) | 0.816 |
| L_across / L_0 | not computed | no equilibrium | 1.000 |

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
driven against). It has no binding at a separation (section 10.3, correcting the first
version of this paragraph): a cell whose phase follows the arriving
wave re-locks at every L, so the cross term's force loses its
dependence on L and becomes a collapse (phi = 0), a drift (pi / 2) or a
separation (pi) by the declared shift; binding needs a FIXED relative
phase between two declared clocks (section 1's corrections). Section
2's condition is then right in substance: each end must carry its own
clock. A pure mirror pair (the cells reflecting without
inserting outward) is not bound: the cavity's light pushes the mirrors
apart and nothing pulls.

**9.5 What the sentence predicts for the pair's frequency after the
push at k = 3.** For (B2), the cells relaying with the phase
continuous: section 3's Doppler integral, f / f_0 = 1 / gamma_m^2 =
0.667 for whatever separation the pair has, and no equilibrium
separation at all (10.3): the pair collapses, drifts or separates by
its declared shift, and five has no reading; if it were held rigidly
by something else it would read L_along / L_0 = 1.000, L_across / L_0 =
1.225, the cycle gamma_m^2 N_0 in both arms, five's 1.500 and 1.500. For (B1), the block
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
Lorentz's member only with the cells at f_0 / gamma_m and the
simultaneity phase between them (10.4); with relay cells it is the
relay's member with no equilibrium extent; its bottom is (C),
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

## 10. The coherent pair in motion: the closed forms, the tearing, the recoil

Written 12:16Z on the Boss's question of 12:05Z (the chief physicist's
finding of 11:52Z: an (A) pair carried rigidly to v = 0.27 and then
torn, the leading object run away by the trailing one's compressed
wave) and as the second correction of section 1. The chain check
`check_pair_motion.py` (the reviewer's scratchpad; floats; soft
sources emitting continuously at the clock [64, 55]; the total field's
stress read four Links outside each emitter; the sources stepping one
Link every K intervals) reads BOTH emitters, at rest and at K = 3;
`track_root.py` follows the equilibrium as beta_c ramps. COMPUTATION
throughout; T_0 is one emitter's travelling-wave stress at rest.

**10.1 The closed forms.** Object 1 behind, object 2 ahead, F positive
toward +x; k_f = 1 / (1 - beta_c) and k_b = 1 / (1 + beta_c) in units
of k_0 (the emitter's forward and backward wave numbers in the lab, its
frequency f_0 in the lattice's intervals, its amplitude unchanged by
the motion in one dimension); delta = phi_2 - phi_1 the declared
relative phase:

    F_1 = (k_b^2 - k_f^2) T_0 + 2 k_b^2 T_0 cos(k_b k_0 L - delta),
    F_2 = (k_b^2 - k_f^2) T_0 - 2 k_f^2 T_0 cos(k_f k_0 L + delta).

The first term is each object's own recoil (10.5); the second is the
cross term of its own emission with the partner's wave arriving in the
same direction (the counter-propagating pair has no cross term under
c^2 = 1 / 3: 3 omega_1 omega_2 - k_1 k_2 = 0). At rest F_2 - F_1 = -4
T_0 cos(k_0 L) cos(delta) and F_1 + F_2 = 4 T_0 sin(k_0 L) sin(delta).
The chain at rest agrees within 3 percent at every L from 72 to 92 for
delta = 0, pi / 2 and pi (in phase: the relative force +0.48, +3.16,
+3.96, +2.40, -0.59, -3.23 at 72, 76, 80, 84, 88, 92; a quarter period:
0.000 at every L with F_1 = F_2; antiphase: the signs reversed). At K =
3 the chain agrees in sign and in the spacing of the fixed points, the
stepping source adding sidebands (its stress ahead 5.95 T_0 against the
closed 5.60, behind 1.04 against 0.40; the own recoil -4.9 against
-5.2).

**10.2 The equilibrium in motion.** The forward term dominates (k_f^2 =
5.6, k_b^2 = 0.40 at k = 3), so the fixed points in motion are spaced
lambda_0 (1 - beta_c) / 2 = 6.7 Links at k = 3 and the binding's
amplitude is 2 (k_f^2 + k_b^2) T_0 = 12 T_0. The stable point continued
from the rest point L_0 = 2.75 lambda_0 by a slow ramp (the root of
k_f^2 cos(k_f k_0 L) + k_b^2 cos(k_b k_0 L) = 0 tracked in steps of 0.001
in beta_c, stable throughout) is

    L* = L_0 (1 - beta_c):   0.900 at beta_c 0.1, 0.792 at 0.2, 0.597 at 0.4, 0.423 at 0.577 (k = 3),

36.9 Links at k = 3, where the forward wavelength lambda_0 (1 - beta_c)
= 13.4 Links sits just above the floor of 12. This is what the (A) pair
reads for L_along / L_0, and section 5's first version (1 / gamma_m^2,
0.667, the retarded pattern's node spacing) was the pattern's geometry
and not the force's equilibrium. The covariant object (iii) keeps L_0 /
gamma_m: with its frequency f_0 / gamma_m and the simultaneity phase
delta = -k_0 beta_c L_0 between the two boosted clocks (10.4), L = L_0 /
gamma_m is an exact root of both cosines at once, the boost of the rest
pair. An impulsive start does not by itself break a pair under the
total-field push (the same kick on both), but the wells in motion are
6.7 Links wide at k = 3, so the ramp over ten to thirty cycles is the
right form and the settling band in motion is +- lambda_0 (1 - beta_c)
/ 4, not +- lambda_0 / 4.

**10.3 The relay has no equilibrium.** An object whose insert follows
its receive with the received phase continued (plus a declared shift
phi) re-locks its phase to the arriving wave at whatever L the pair
has, so its cosines are cos(phi) at every L: F_2 - F_1 = -2 T_0 (k_f^2 +
k_b^2) cos(phi), a collapse for phi = 0, a drift for pi / 2, a
separation for pi, never a restoring force. Section 1's first
correction ("the relay binds at its parity") is withdrawn; its first
statement ("a relay pair is not bound") stands with the reason
corrected: not the absence of a cross term, but the absence of its
L-dependence. The chief physicist's finding 2 (11:25Z) was therefore,
for the owner's candidate, a relay, and for (A) the parity and the
trains (section 1's correction); his push was the total field's
throughout.

**10.4 The tearing.** The scatterer's asymmetric radiation pressure
in motion is 2 R (k_f^2 - k_b^2) T_0 forward on the leading object (R
= 0.086 for the thin scatterer at n_o = 2; k_f^2 - k_b^2 = 4 beta_c
gamma_m^4 = 5.2 at k = 3), 0.9 T_0, against the coherent binding's 2
(k_f^2 + k_b^2) T_0 = 12 T_0 at k = 3: there is no beta_c below 1 at
which a thin scatterer's pressure beats the coherent binding, and k = 3
is above no threshold of the FORCE. The physicist's "breaks above v =
0.27" (12:22Z, under the total-field push, E'_0 = 300, a ramp of ten
to thirty cycles) is not the force's limit but the ramp's: 10.7.

**10.5 The recoil.** An emitter at the lattice-time frequency f_0
radiates asymmetrically in motion and is braked by its own emission,
(k_f^2 - k_b^2) T_0 = 4 beta_c gamma_m^4 T_0 per interval, 5.2 T_0 at k =
3 (the chain 4.9), the same on both objects. Against a momentum of
about 127,000 T_0 (E'_0 = 1000 trains of two periods = 220,000 T_0 c,
P = E'_0 beta_c / c) that is 1.1 percent of the pace per cycle of 277
intervals, about 45 percent over forty cycles: an (A) pair pushed to k
= 3 does not stay at k = 3 under a push that includes its own record.
The local form of DESIGN.md 5.1 (a)'s "a body's own insert adds
nothing to P", exact in motion too because the own record is a
separate field: the push is the stress of the total field LESS the
stress of the object's own record alone at its six Ports (the cross
terms and the partner's terms). Its price: no recoil, no momentum
conservation with the object's own emission; the rocket's physics kept
here as a COMPUTATION. Recommended for the reduced run; the owner's
word on which the design keeps.

**10.6 For the run, in one paragraph.** In-phase clocks at L_0 = 88
(m = 5.5 at lambda_0 = 32), or antiphase at 72, or the clock N = 50
(lambda_0 = 28.87, MUST I's floor at k = 3 exactly) in phase at 79.4;
never L_0 = 80 and never a quarter period; the total-field push less
the own record (10.5, 10.7: with the own record in the push the brake
is 3.8 percent of the pace per cycle at E'_0 = 300 and 38 percent at
30); continuous emission; the rest control showing the pair holding at
the declared phase before any push; light objects and a slow ramp
(10.7: E'_0 = 30 to 100 trains and a ramp of at least 20 to 30 cycles,
so that the pair follows its well); the readings f / f_0 (1.000 names (A), 0.816 Lorentz,
0.667 the relay) and L_along / L_0 (0.423 for (A) at k = 3, 0.816 for
Lorentz, no equilibrium for the relay), the settling band in motion +-
lambda_0 (1 - beta_c) / 4. Every number COMPUTATION; no pin moved by
this file; the declarations the design's and the owner's.

**10.7 The ramp's adiabaticity: why a pushed pair falls out of its
well, and what the run must declare.** The stable separation moves as
the pace grows, L* = L_0 (1 - beta_c) (10.2), a sweep of 50 Links = 7.5
well spacings at k = 3 and 25 Links = 2.2 spacings at k = 6, and the
pair follows its well only if the well moves slowly against the pair's
own oscillation in it. The well's curvature at the leading object is
F' = 2 k_f^3 k_0 T_0 per Link (the derivative of 10.1's second term);
the pair's mass in these units is M = E'_0 / c^2 with E'_0 = n trains
x 110 intervals x 2 T_0 c (the flux both ways), so the oscillation in
the well has the period T_osc = 2 pi sqrt((M / 2) / F'): 207, 379, 656,
1198 intervals at E'_0 = 30, 100, 300, 1000 trains at k = 3 (453, 827,
1432, 2615 at k = 6). Over a ramp of T_ramp intervals the well moves
L_0 beta_c T_osc / T_ramp Links per oscillation; adiabatic when that is
under a third of the spacing (2.2 Links at k = 3, 3.8 at k = 6). At E'_0
= 300 and a ramp of ten cycles (2770 intervals) the well moves 11.9
Links per oscillation at k = 3 and 13.0 at k = 6, two spacings: the
pair cannot follow, falls out of its well and reads as "breaks" or
"drifts", exactly the physicist's 12:22Z readings (v = 0.27 at k = 3;
80 to 95 at k = 6); at E'_0 = 1000 it is worse (21.8 Links). The ramp
needed: about 17, 31, 53, 97 cycles at E'_0 = 30, 100, 300, 1000 at k =
3 (11, 20, 35, 63 at k = 6). Against this stands the own recoil (10.5),
which with the own record in the push brakes the pace by 38, 11, 3.8
and 1.1 percent per cycle at those masses: the light objects that
follow the well are the ones the recoil stops, and the heavy ones that
coast cannot follow. The two together leave no regime under the push
as implemented; with the push declared as the total field LESS the
own record (10.5) the brake is gone and the run is E'_0 = 30 to 100
trains with a ramp of 20 to 30 cycles, reading after the ramp. Named
before the run as its outcomes, by kind: "falls out of its well during
the ramp" reads the ramp (COMPUTATION above, a control), "slows" reads
the push's form (the own record in it), and only a pair that follows
its well reads the member: f / f_0 = 1.000 with L_along / L_0 = 1 -
beta_c for (A). COMPUTATION; the declarations the design's.

## 11. Direction (ii), designed to its ends: a second, massive record kind under the discrete Klein-Gordon rule, beside massless light

Written on the model owner's word of 12:15Z (record 1381: direction
(ii), "to design and to close ALL its ends, including the algebra that
follows from our own formulas, to see that it closes"; the Boss's order
of 12:18Z). This section widens 8.7 and is written for a reader with
the design's formulas only: every step is shown. Kinds: the rule and
the couplings are DECLARATION candidates for the owner's second word;
every number is a COMPUTATION (the closed forms, and the scratch
scripts `check_massive_well.py` and `check_kg_board.py` of the
reviewer's scratchpad, seconds, floats); nothing enters the law by
this section. Light stays the massless record of DESIGN.md section 2
and every light pin stays as declared.

**11.1 The rule and its integer form.** The design's wave rule at a
free Node (DESIGN.md section 2), with S_6 the sum of the six
neighbours' present records, is

    3 a_next + r' = S_6 - 3 a_before + r,

that is, a_next - 2 a_now + a_before = (1 / 3)(S_6 - 6 a_now), the
leapfrog form of d^2 a / dt^2 = c^2 (Laplacian of a) at c^2 = 1 / 3.
The massive record kind keeps the same rule with ONE self term, a
declared pair [p, q] on the Node's own present record, subtracted:

    3 a_next + r' = S_6 - 3 a_before + r - (3 p / q) a_now,

the leapfrog form of d^2 a / dt^2 = c^2 (Laplacian of a) - mu^2 a with
mu^2 = p / q (the discrete Klein-Gordon rule; the check: divide by 3
and compare the two forms term by term). In integers the whole is
scaled by q so that the one division is exact with its remainder
kept, as the coefficient form of DESIGN.md 4.1 divides by 3 den:

    3 q a_next + r' = q S_6 - 3 q a_before - 3 p a_now + r,     r' in [0, 3 q),

the remainder r' of the Euclidean division by 3 q carried to the next
interval exactly as r is in the wave rule. A foreign object of this
kind is a Node (or a set of Nodes) whose self pair is its own, [p', q]
with p' < p on the same denominator: the well's strength is

    g = (p - p') / q > 0     (a locally lighter Node),

the object's one declared parameter beside its place. Verbs: the sum
of the six (one verb), a multiply by a declared pair, a subtract on
the own record, the division with the remainder kept; no root, no
float, no seventh verb (the owner's rule of record 642). The three
tests as a rule: generic (one primitive with the declared integers p,
q, p'; no family name, no kind), vector (the verbs above on the state
vector), local (the self term reads a_now at the Node itself, the rest
its six neighbours; nothing else). The Boss's coefficient of 11:58Z
is right; the one correction is the division by 3 q rather than by 3.

**11.2 What follows at rest, from the pair and the well alone.** On
the chain (the y and z neighbours equal to the row itself, S_6 = a_E +
a_W + 4 a_now) look for a mode localized at the object's Node j = 0,

    a_j(t) = A e^(-kappa |j|) cos(omega t).

Away from the Node the rule gives, with cos(omega t) common to every
term, 4 sin^2(omega / 2) = mu^2 - (2 / 3)(cosh kappa - 1) (insert the
mode into a_next - 2 a_now + a_before = (1 / 3)(a_E + a_W - 2 a_now) -
mu^2 a_now, and use e^kappa + e^-kappa = 2 cosh kappa). At the Node
itself both neighbours are e^-kappa A, so 4 sin^2(omega / 2) = mu^2 - g
- (2 / 3)(e^-kappa - 1). Equating the two:

    (2 / 3)(cosh kappa - e^-kappa) = g,   that is   sinh kappa = 3 g / 2,

which has exactly one root kappa > 0 for every g > 0: on the chain
every well binds one mode. Its frequency and extent:

    4 sin^2(omega_b / 2) = mu^2 - (2 / 3)(cosh kappa - 1),     the extent 1 / kappa Links,

and for a small well (kappa small) these are the continuum's
omega_b^2 = mu^2 - 3 g^2 / 4 and 1 / kappa = 2 / (3 g) (expand sinh
and cosh to second order). The mode is bound and not growing when
omega_b is real, that is (2 / 3)(cosh kappa - 1) < mu^2, for a small
well g < 2 mu / sqrt 3. Its period in intervals is N_b = 2 pi /
omega_b, ABOVE the gap's period 2 pi / mu and so above the floor N >=
21 (DESIGN.md 1.2) whenever mu <= 0.3; the mode lies below the band
(the massive band starts at omega = mu) and cannot radiate into it: a
true bound state. Numbers at mu = 0.05 (COMPUTATION, the exact lattice
forms above against the continuum and against the chain script's
zero-crossing reading):

| eps = 3 g^2 / (4 mu^2) | g | kappa (exact; continuum) | the extent, Links | the period N_b (exact; continuum; read on the chain) |
| --- | --- | --- | --- | --- |
| 0.04 | 0.0115 | 0.01732; 0.01732 | 58 | 128.24; 128.25; 128.2 |
| 0.10 | 0.0183 | 0.02738; 0.02739 | 37 | 132.45; 132.46; 132.4 |
| 0.25 | 0.0289 | 0.04329; 0.04330 | 23 | 145.08; 145.10; 145.0 |

The owner's "how many cells": the object is the well's Nodes plus the
mode's extent 1 / kappa around them, derived and not declared; a
one-Node well on the chain holds a mode of 23 to 58 Links at these
strengths.

**11.3 The integers stay bounded.** The massive rule's dispersion on
the chain is 4 sin^2(omega / 2) = (4 / 3) sin^2(k / 2) + mu^2 (insert a
plane wave), real for every k when (4 / 3) + mu^2 <= 4, that is mu^2 <=
8 / 3: no growing mode of the free rule. The conserved energy is the
design's E (DESIGN.md section 2, the leapfrog energy 3 (sum of the
motions squared) + (sum over Links of the strain now times the strain
before)) with one term added,

    E_m = E + 3 mu^2 (sum over Nodes of a_now a_before) - 3 g (a_now a_before at the well's Node),

conserved by the same telescoping that conserves E (for one Node the
identity (a_next - a_now)^2 + K a_next a_now - (a_now - a_before)^2 - K
a_now a_before = (a_next - a_before)(a_next - 2 a_now + a_before + K
a_now) shows that the product form is what the leapfrog conserves);
the mode's amplitude is therefore bounded by its energy at birth, the
remainder's drift is the wave rule's, and the scale q multiplies every
intermediate (q S_6 at the amplitude 2^20 and q = 3600 is 2.3 x 10^10,
inside int64 with room to q about 2^30; mu = 1 / 60 is [1, 3600]).

**11.4 The Lorentz member, from the rule's own covariance.** Four
steps. (a) On the continuum pace the operator d^2 / dt^2 - c^2 d^2 /
dx^2 + mu^2 is invariant under the boost x' = gamma_m (x - v t), t' =
gamma_m (t - v x / c^2) (a direct substitution; the self term mu^2 a is
a scalar and needs no transformation). (b) A well of strength g at the
moving Node is, on the continuum pace, the term g delta(x - v t) a; in
the well's rest frame delta(x - v t) = delta(x' / gamma_m) = gamma_m
delta(x'), so the moving well of strength g is a RESTING well of
strength gamma_m g. (c) The resting well's bound mode has omega' =
sqrt(mu^2 - 3 gamma_m^2 g^2 / 4) by 11.2 and oscillates as cos(omega'
t'); at the well x' = 0 the rest time is t' = t / gamma_m, so the
oscillation read at the moving well in lab intervals has omega =
omega' / gamma_m. (d) Divide by the rest value:

    f / f_0 = (1 / gamma_m) sqrt((1 - gamma_m^2 eps) / (1 - eps)),     eps = 3 g^2 / (4 mu^2),

Lorentz's member 1 / gamma_m as eps -> 0, the deviation eps (gamma_m^2 -
1) / 2 to first order, eps / 4 at k = 3 (gamma_m^2 - 1 = 1 / 2). The
lattice keeps this because the mode's extent is many Links (the
dispersion error at the mode's wave numbers is of order kappa^2 / 12,
below 10^-3 at kappa = 0.04) and the well hops one Node per k
intervals, many times per period (the mode follows adiabatically).
The chain script (mu = 0.05, the well pushed from rest to k = 3 by the
accumulator of DESIGN.md 5.1 (a) over 6000 intervals, the frequency
read at the well's own Node by zero crossings over 3000 intervals)
reads 0.8077, 0.7936, 0.7460 at eps = 0.04, 0.10, 0.25 against the
closed form's 0.8079, 0.7935, 0.7454; Lorentz's 0.8165, the relay's
0.6667. Within five's band +- 0.03 for eps <= 0.1. Every step above
uses the design's formulas and the boost only; nothing declared but
the pair and the well.

**11.5 The self-click.** The mode's record at the object's Node
oscillates at omega_b: its motion crosses the rung 1 / W every period
without any partner, so 1.1's existence condition (an object always
produces clicks) is met by the object's own mode, and the lone
object's exception of DESIGN.md section 8 is not needed. One
declaration this needs, named: the object's own massive record is
READ at its Node (the count of its zero crossings) and never TAKEN by
it (no damping pair on its own mode), else the clock consumes itself;
the take of section 5 stays light's.

**11.6 The board.** Three dimensions differ from the chain in one
thing: a single Node's well binds a mode only above a threshold. For a
mode below the gap write s = mu^2 - 4 sin^2(omega_b / 2) > 0; the
mode's equation is (s - (1 / 3) Laplacian) a = g delta a, whose
localized solution exists when g G_00(s) = 1 with G_00 the lattice
Green's function of the simple cubic six-neighbour rule, G_00(s) =
the average over the Brillouin zone of 1 / (s + (2 / 3)(3 - cos k_x -
cos k_y - cos k_z)); at the gap's edge s -> 0 this is (3 / 2) W_3 with
W_3 = 0.505462 the Watson integral of the simple cubic lattice, so

    g_c = 1 / ((3 / 2) W_3) = 1.319 per interval squared     (the numeric quadrature on a 240^3 grid: 1.322),

independent of mu. Above it the binding grows fast: at mu = 0.05, g =
1.35 gives a lawful mode (period 229 intervals, extent 14 Links) and g
= 1.40 already s > mu^2, omega_b^2 < 0, a growing mode: the lawful
window for a one-Node well on the board is about 3 percent wide and
needs a self term p' / q = mu^2 - g of about -1.32, a strongly
anti-restoring Node. The lawful object on the board is therefore
EXTENDED: a ball of Nodes with the self term reduced (not reversed),
bound when g R^2 >= pi^2 c^2 / 4 = 0.822 (the spherical well on the
continuum pace, c^2 = 1 / 3), so with g <= mu^2 = 0.0025 a radius R >=
18 Links (the lattice's correction to this radius not computed; a
scratch board of 60^3 Nodes for a few thousand intervals, minutes,
would give it). "How many cells" on the board is then thousands, the
mass an extended object, as the owner's record 1371 says for another
reason. The dispersion cost of the gap falls on the MASSIVE record's
own waves only (their group pace below c, their band from mu up): it is
irrelevant to light under (ii), which keeps the massless rule and its
pins.

**11.7 The coupling to light.** The presence of the massive record at
a Node does not by itself act on light's record (two records, two
rules, no shared term): (ii) needs its couplings DECLARED, three
lines, each within the six verbs. (a) What light sees: the object's
Nodes carry the index pair of DESIGN.md 5.1 (b) for light's record (or
the mirror q = 0, or the take), declared on the well's Nodes, so the
object is a scatterer, a mirror or a detector for light as any
foreign object is; and, for a light SOURCE, a linear source term:
light's record at the object's Node receives + [s_n, s_d] x a_m (the
massive amplitude there) per interval, so light is emitted at the
mode's frequency omega_b with the mode's phase; the object's light is
its own clock's. (b) What the object feels: light's stress at its
Ports pushes its momentum P by 5.1 (a) (the total field of LIGHT's
records less nothing, since the massive mode is not light), and light's
arrival may drive the massive record by the same pair [s_n, s_d]
(the symmetric coupling; then the total energy E_light + E_m - 3 (s_n /
s_d) (sum over the object's Nodes of a_light a_m) is the conserved
quantity, by the same product-form identity as 11.3). (c) The click:
light's record ends at the detector's Port (the take of section 5, on
light's record), and the detector's own record that changes is the
massive object's: its momentum P (the push) and its count; its mode's
amplitude is not fed by the take (a declaration, else a click detunes
the clock). What the light clock built on two such objects reads: at
rest, each object emits light at omega_b in phase with its mode; two
objects whose modes are in phase (the bonding configuration) are two
in-phase coherent emitters and are bound by section 10's force at L =
(m' + 3 / 4) lambda_b (lambda_b = N_b c, 74 Links at N_b = 128), the
evanescent attraction of their modes (11.2, e^(-kappa L), 0.09 at L =
88 for the extent 37) a small inward shift of that point; the pins at
rest are light's as declared, (d) 208 / 207 / 207 in intervals and,
in the object's own count, 2 L / (c N_b) periods. In motion the boost
of this rest solution is again a solution (11.4 for the modes,
section 4 for light): the modes at omega_b / gamma_m with the
simultaneity phase between them, light emitted at that frequency, the
separation L_0 / gamma_m an exact root (section 10.2), the light round
trip gamma_m N_0 lab intervals and gamma_m N_b per mode period, so the
clock reads 1 and 1 in its own count and the lab's row reads gamma_m:
Lorentz's member from the rule and the couplings, no declared factor.
The one caveat: the objects' light must be sourced by the mode (line
(a)); a declared light clock f_0 on a massive object is (A) again.

**11.8 The price list.** (i) The gap in light's record: every light
pin moves by mu^2 / (2 c^2 k^2) (one percent at lambda_0 = 32 for mu =
0.0162), and the lawful clock is slower than the gap, about 390
intervals at that mu; PINS (d) moves by two intervals at its band's
edge. (ii) Light untouched, every light pin as declared; the costs (i)
does not have: a second rule at every Node (the massive record's
a_now, a_before and remainder beside light's: the memory and the work
per interval doubled, the host's cost, not the model's local cost,
which stays fixed per Node), the three coupling declarations of 11.7,
and the object's birth as its mode (an initial condition, the mode's
profile at its Nodes, or a kick and a settling time before any
reading).

**11.9 What the design does not yet have, named, and the first
checks.** Formulas to add before any build: the integer form of the
source term [s_n, s_d] (11.7 (a)) and its energy identity; the rule
for which Nodes are the object's when the mode is extended (a rung on
the massive amplitude, declared); the board's radius R for the ball
(11.6, a scratch board); the massive pair's own attraction and its
shift of the light binding's point (a closed form from 11.2 and
section 10, not done). The first checks, each in seconds on the chain
before any coupling: the mode's period against 11.2's exact form (done
above, 0.1 percent), its member at k = 3 against 11.4 (done, 0.1
percent), then one object emitting light from its mode (11.7 (a)) and
its light's frequency read at rest and at k = 3 against omega_b and
omega_b / gamma_m, then the pair. Each a COMPUTATION; the owner's
second word before any of it enters the design's world files.

## 12. The foreign object in the algebra's own terms, and the square block: the one law, claim by claim

Written on the model owner's words of 12:28Z and 12:35Z (records 1385
and 1386: one big generic law, physical, algebraic and vector, that
solves the foreign object completely, so that a SQUARE block of cells
can be placed, three by three or twelve by twelve; and "we do not
create the laws of physics anew, we derive everything algebraically
and then implement in the engine to test; check whether a foreign
object is a kind of group, or something of that kind, like the rest";
the Boss's orders of 12:32Z and 12:40Z). Every claim below is numbered
for a line-by-line comparison with the Algebra Mathematician's
independent derivation from [docs/ALGEBRA.md](../../ALGEBRA.md) alone;
each names its kind and the formula of ALGEBRA.md it rests on; where a
step needs something the algebra does not have it is named as a
DECLARATION and not filled. The scratch scripts are `check_block.py`
(the chain operator's lowest eigenvector and eigenvalue for a block of
width s) and `check_block_motion2.py` (the block pushed to k = 3, its
clock read by the spectral peak at its centre), seconds each.

**12.1 The object's place in the structure (ALGEBRA.md chapter 1).**

- C1 (DECLARATION of the design, the Boss's answer confirmed): the
  foreign object is not a fifth group object. The four are the cube P
  with G_48, the phase circle Z_N with its ring Z[Z_N], the translation
  group of the torus, and the collision's Z_m (1.1); the object adds
  none. Its self pair [p, q] is a scalar content of a Node, like the
  content M and like the index pair of DESIGN.md 4.1, on which G_48
  acts trivially (1.1: "trivially on every scalar"); its place is one
  row of the dictionary 1.2, "the rest mass of a massive record: the
  self pair [p, q] on its own present record", beside the row "mass: a
  body's content M", never a new object.
- C2 (COMPUTATION): the wave rule of DESIGN.md section 2 is the
  central formula of ALGEBRA.md chapter 2 with the rate a bilinear form:
  the accumulator is the remainder r, its rate S_6 - 3 a_before, its
  wall 3, the whole part the new record a_next, the remainder kept; in
  the six verbs, (B) the rate (a declared matrix over the neighbourhood's
  records: +1 on each of the six neighbours' present records, -3 on the
  own record before), (T) the translation of the accumulator by it, (D)
  the division by the wall with the remainder kept. The self term of
  11.1 is ONE MORE ENTRY of (B)'s declared matrix, the diagonal entry
  -3 p on the own present record, with the wall scaled to 3 q; no verb
  is added, none of the six is altered, and the term is inside the same
  (B), (T), (D) as the rule's own. In the six-operation inventory of
  2.9 the massive record's line is "the hop: B, T, D" with one more
  matrix entry.
- C3 (COMPUTATION): the rule with the self term commutes with G_48
  exactly as the rule without it: the six neighbours enter with equal
  coefficients (a G_48-invariant form on the cube), and the self term
  acts on the Node's own record, a scalar under the 48 (1.1). The test
  "generic" of 2.8 (commuting with the 48, made of the six operations,
  reading the neighbourhood alone) holds; "vector" holds (the rate is
  linear in the state, below bilinear; no root, no float, no rounding
  at run time beyond the declared wall); "local" holds (the own record
  and the six neighbours; fixed work and storage per Node).
- C4 (DECLARATION): the block's shape is world data, as a wall's
  placement is: a cube of cells is G_48-invariant about its centre, a
  square on a one-layer world is invariant under the layer's D_4 and
  not under the 48, lawfully so (the world breaks the symmetry, the
  rule does not; the rule never asks the shape).

**12.2 What follows by algebra alone (ALGEBRA.md chapters 2 and 5).**

- C5 (COMPUTATION, the energy): ALGEBRA.md's E is a bilinear form
  (2.2) of the state; the massive record's is the same form with one
  more diagonal block, E_m = E + 3 (p / q) (sum over Nodes of a_now
  a_before) - 3 g (sum over the block's cells of a_now a_before),
  conserved by the leapfrog's product identity (11.3, written out) and
  bounded below for p / q < 8 / 3, so every record stays bounded by its
  energy at birth; the remainder's drift is the wave rule's. In
  integers the form's entries are 3 p and 3 (p - p') over q.
- C6 (COMPUTATION, the block's lowest mode at rest): on the chain the
  one-interval operator is the symmetric tridiagonal H with H_jj = p / q
  - g_j + 2 / 3 and H_j,j+1 = -1 / 3, and a mode is H a = 4 sin^2(omega
  / 2) a; the lowest eigenvalue lam of H with g_j = g on the block's s
  cells and 0 elsewhere gives omega_b = 2 arcsin(sqrt(lam) / 2), bound
  iff lam < p / q, its extent the eigenvector's 1 / e width. On the
  continuum pace the same is the even solution of the finite well
  (c^2 = 1 / 3): inside k_in^2 = (omega^2 - mu^2 + g) / c^2, outside
  kappa^2 = (mu^2 - omega^2) / c^2, matched by

      k_in tan(k_in s / 2) = kappa,

  the lowest root the mode; for s -> 1 it is 11.2's one-Node well
  (sinh kappa = 3 g / 2), for s -> large it is the cavity's omega^2 ->
  mu^2 - g + c^2 pi^2 / s^2. So "the frequency computed from the pair
  and the size" is right, this is its formula, and the lattice and the
  continuum agree to 0.1 percent at every width tried (mu = 0.05):

  | g | s | the period N_b (lattice; continuum) | bound | the extent, Links | the binding depth eps |
  | --- | --- | --- | --- | --- | --- |
  | 0.5 mu^2 | 1 / 3 / 12 / 48 | 125.7 / 125.9 / 129.4 / 151.3 (the same) | yes | 1049 / 359 / 102 / 70 | 0.000 / 0.004 / 0.057 / 0.310 |
  | mu^2 | 1 / 3 / 12 / 24 / 48 / 96 | 125.8 / 126.7 / 140.6 / 172.8 / 250.2 / 413.9 (the same) | yes | 533 / 181 / 58 / 46 / 56 / 90 | 0.002 / 0.017 / 0.201 / 0.471 / 0.748 / 0.908 |
  | 4 mu^2 | 1 / 3 / 6 / 12 | 127.6 / 145.1 / 286.8 / grows | yes / yes / yes / NO | 133 / 47 / 28 / - | 0.030 / 0.250 / 0.808 / - |

  On the chain every block binds at every g > 0 (one dimension); the
  mode grows (lam < 0, unlawful) once the block is wide and its self
  term reversed (g = 4 mu^2 at s >= 12). Two regimes, by the block's
  width against the one-Node extent 2 / (3 g): the WELL regime (s much
  smaller: the mode extends far beyond the block, its frequency near
  the gap's, eps small) and the CAVITY regime (s comparable or larger:
  the mode sits inside the block, its frequency the block's own
  standing wave). The rest period is above the gap's period 2 pi / mu
  in both, so above the floors N >= 21 and N >= 6 for mu <= 0.3
  (DESIGN.md 1.2).
- C7 (COMPUTATION, the board): for a one-Node well the three-dimensional
  threshold is g_c = 1 / ((3 / 2) W_3) = 1.319 (11.6); for a block it
  falls with the side as the spherical well's g R^2 >= pi^2 c^2 / 4 =
  0.822 with R the block's half-side: a 3 x 3 x 3 block needs g >= 0.37,
  a 12 x 12 x 12 block g >= 0.023, a 36-side block g >= 0.0025 = mu^2
  (the inside massless); so a wide enough block binds at any g, as the
  Boss expects, and a small block only with its self term reversed and
  then inside a narrow window (11.6). The cube's exact threshold
  against the sphere's is not computed (a scratch board of 60^3 Nodes,
  minutes).
- C8 (COMPUTATION, the Lorentz member; ALGEBRA.md 1.2's Lorentz row and
  2.7): no boost is among the 48 and no root is in the rule; the
  factor 1 / gamma_m is not a verb, it is a reached number, a ratio of
  two readings of the same record (the mode's period at rest and in
  motion), exactly the kind of relation 1.2 says Lorentz's forms are
  ("reached Outside as relations among counts between clicks, the
  algebra first and the comparison after"). Its derivation is 11.4 on
  the continuum pace of the operator (the map's ds / dt = r(s) limit of
  ALGEBRA.md section 0): the KG operator is boost-invariant, a moving
  well of strength g is a resting well of strength gamma_m g, the
  mode's phase at the well advances at omega' / gamma_m. For the block
  the same argument makes the moving block of width s a RESTING block
  of width gamma_m s with the same g (the boost widens the block in its
  own frame, since the lattice does not contract the declared cells),
  and the member follows the regime: in the WELL regime f / f_0 = (1 /
  gamma_m) sqrt((1 - gamma_m^2 eps) / (1 - eps)) with the block's eps
  (Lorentz to first order, the deviation eps / 4 at k = 3); in the
  CAVITY regime the block is the rigid cavity of section 3 and reads
  toward 1 / gamma_m^2. The chain (the block's exact lowest mode pushed
  to k = 3 by the accumulator over 8000 intervals, the clock read by
  the spectral peak at the block's centre):

  | s | g | eps at rest | f / f_0 read at k = 3 | the well formula | 1 / gamma_m | 1 / gamma_m^2 |
  | --- | --- | --- | --- | --- | --- | --- |
  | 1 | 0.0183 | 0.100 | 0.7949 | 0.7934 | 0.8165 | 0.6667 |
  | 12 | 0.5 mu^2 | 0.057 | 0.8060 | 0.8040 | 0.8165 | 0.6667 |
  | 12 | mu^2 | 0.201 | 0.7796 | 0.7635 | 0.8165 | 0.6667 |
  | 24 | mu^2 | 0.471 | 0.7461 | (the formula outside its range) | 0.8165 | 0.6667 |
  | 48 | mu^2 | 0.748 | 0.7107 | (the cavity regime) | 0.8165 | 0.6667 |

  So the massive block is Lorentz's clock within five's band only in
  the well regime (s small against 2 / (3 g), eps under about 0.1: a
  twelve-cell block at g = mu^2 / 2 reads 0.806 against 0.817), and
  slides toward the rigid cavity's member as it widens: the size and
  the pair are not free for a clock, and this is the one condition the
  block form adds. (The zero-crossing count is fragile for this
  reading; the spectral peak is the reading used, and 11.4's numbers
  re-read by it are 0.7949 at eps = 0.10 against the closed form's
  0.7934, 0.2 percent.)
- C9 (COMPUTATION, the self-click): the block's own mode oscillates at
  omega_b at every cell; its motion crosses the rung 1 / W each period
  with no return, no partner and no timer, so the clock sentence of
  DESIGN.md section 8 is NOT needed for a massive block (its clock is
  its mode, a computation from the pair and the side by C6); what
  remains of the sentence is the light-clock objects on the massless
  rule alone (the one-Node emitters of the reduced run, variant (A)'s
  declared period, and the relay), where it stands as declared without
  a timer (my gate of 84db9247). The one declaration C9 needs is
  11.5's: the own massive record is read at its cells, never taken.
- C10 (DECLARATION, the two couplings as bilinear forms of chapter
  2's kind): (a) what light sees at the block's cells is the index pair
  of DESIGN.md 5.1 (b) on light's record there (the coefficient form,
  itself (B), (T), (D)) and, for a source, an off-diagonal entry of
  (B)'s matrix between the two records at one Node, light's record
  receiving [s_n, s_d] x a_m per interval; symmetric, it is one
  bilinear coupling with the conserved total of 11.7 (b). (b) What the
  block feels from light: the push of 5.1 (a), light's stress at the
  block's OUTER Ports, a form quadratic in light's state (the terms of
  E, 2.2's "the click's weight is this form": nothing squared as a step
  of its own beyond the form), its rate bilinear as 2.8 allows, then (T)
  on the momentum and (D) the drive. Neither is in ALGEBRA.md today;
  both are declarations of the design, and the algebra has the verbs
  for them.
- C11 (the block's momentum, one line each under the three tests): ONE
  integer per axis for the whole block ("one body") needs the sum of
  the stresses over the block's outer Ports, a sum over Nodes that are
  not neighbours for any block wider than one cell: NOT local as it
  stands; lawful only as a declared tie of the kind 1.1 names ("up to
  the two declared ties"), a third tie, named as such. One integer per
  CELL, each cell pushed by the stress at its own Ports (light's, and
  the massive record's own, whose gradient at the block's edge cells
  points inward), is generic, vector and local; whether the block then
  holds together by its own mode's stress or needs the tie is a
  COMPUTATION not done (a chain of two cells under their mode, seconds,
  named for the next check). The lawful form is the second; the owner's
  "one body" is the first with its tie declared.

**12.3 What the algebra does not have, named (not filled).** The
source term's integer pair [s_n, s_d] and its wall; the rule that names
a cell as the object's when the mode is wider than the block (a rung
on the massive amplitude); the block's rigidity or its self-binding
(C11); the cube's threshold on the board (C7); the massive pair's own
attraction beside the light binding (11.9). Each a declaration or a
computation to come, none a change of the law before the owner's second
word. Every number above is a COMPUTATION on the chain or the continuum
pace; no pin moves; nothing enters the law by this section.
