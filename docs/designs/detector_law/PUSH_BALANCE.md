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
it exists only for an object with a resonance, never for a relay
(section 1). COMPUTATION.

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
In case (ii) the relay is not bound (section 1), so "carried rigidly" is
an assumption about the pushes, and a free relay pair drifts apart
instead: five then has no reading at all.

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
program, not a sentence). The choice is the model owner's; nothing here
enters the law.

## 7. The kinds, and what is not here

Every number above is a COMPUTATION on the continuum pace; the
declared inputs are f_0, m, phi, r, k and L_0 (DECLARATION). No pin of
PINS.md moves: rows (e) and (f) keep 1 +- 0.03 and the outcomes named
before the run; the lab's dilation row keeps its predicted FAIL under
case (i). What this file does not do: it does not run the chain, does
not carry the lattice's dispersion into the numbers (the shifts at 24
to 32 Links are about one percent, DESIGN.md 8b as gated), and does not
decide the push-to-cadence rule (how the pair reaches beta_c), which
sets the path and not the member; the frequency's law sets the member.
