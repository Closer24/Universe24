# Analysis before the probes (pen and paper on the act as built)

## A. What the "held hand" is, mechanically
Own spring K = 2W on each of two gears: a+ = 2a - b + floor((r - 2W a)/W) = -b exactly. Each part is an ordinary
leapfrog oscillator at 4 sin^2(omega/2) = K/W = 2, omega = pi/2, period 4 rounds. Two parts "in quadrature" = two
oscillators 90 degrees apart. |k|^2 = re^2 + im^2 constant is the ONE oscillator's energy being constant.
The conserved leapfrog energy of a+ - 2a + b = -(K/W) a is 2E = W (a - b)^2 + K a b. With K = 2W: 2E = W (a^2 + b^2)
per part, so E = (W/2)|k|^2 per part, E = W |k|^2 per Node-clock. The potential V = rest |k|^2 + g f (x.x) |k|^2 >= 0
has its MINIMUM at k = 0. The "vacuum" |k|^2 = 1 is an EXCITED state (a rotor held up by its quadrature), not a
minimum of anything: no restoring force on |k|^2 (any (re, im) is steady; p1 shows D held at any whole (re, im)).
=> Nature: the Higgs vev is the minimum of V; fluctuations of |phi| cost m_H^2. Here the radial direction is FLAT
(a zero mode) and the phase turns at the top of the band (omega = pi/2), the reverse of nature (massive radial,
massless/eaten phase).

## B. Equation of state (G5's physicist's point, quantified)
Per part at (a, b) = (1, 0): T = (W/2)(a-b)^2 = W/2, V = (K/2) a b = 0 -> p = T - V = +W/2 = +rho (stiff, w = +1) in
the leapfrog-symmetric reading; in the now-slot reading V = (K/2) a^2: p alternates -W/2, +W/2, mean 0 (dust, w = 0).
Either way w >= 0, never w = -1. A vacuum with a rest frame and energy W per Node-clock = 2 matter quanta (a matter
quantum at D_x = 1 has E = W/2, see D). If G2 sources the lapse by rho + 3p of every train (decision 40 (a), the
owner's law), the held hand is a dust/stiff background at rest in the lattice frame, in every Node-clock.

## C. The pair rule / genericity
- Probes 1-6 use the held hand (A1) x 2: IDENTICAL kinds to light (A1, part 2). No kind-based rule can tie one and
  not the other. p6 (ii): light tied beats like T1. So in the probes' own universe, the exemption of light is a
  declaration by omission.
- The probes' tied train is ("m", [T1], part 1): ONE hand. The text's pair rule (K with A2 x K) needs two hands
  (T1, T2). So the text's own rule, applied to the text's own probes, ties NOTHING that was probed. The rule's pairs:
  (A1, A2) = the held hand itself (so the held hand ties to itself: |k|^4, which the text omits), (T1, T2), (E, E)
  (refused by the loader outside the square). The example universe has light (A1 x 2) and the metric only: nothing
  for the rule to tie.
- The ONLY generic plan (every train through its K x K -> A1 row at one g) ties light, the metric and the held hand
  alike: light gets the notch's beat; the metric's 00 slot gets J = -2 f |k|^2 c = -(2W/Gamma) c, i.e. D/W = 2/Gamma,
  EXACTLY the time gear's spring (the owner's law). The unit f was CHOSEN to make that coincidence. So:
  generic => light massive at the time gear's beat; non-generic => a list of tied trains = a declaration.

## D. The quantum vs the room: they do not overlap
Tied hand: 4 sin^2(omega/2) = 2 g |k|^2/Gamma; D_x = A^2 sin^2(omega) ~ (A omega)^2 = (peak velocity in counts per
round)^2. So D_x = 1 <=> the hand moves 1 count per round at its peak: BELOW the quantum the hand moves 0 or 1 count
a round (the text's "relaxation", P = Gamma/(gA) + 4A); the harmonic beat (the "mass") exists only at and above the
quantum. The room (peak push 2 g f x^2 < W/2) is g A^2 < Gamma/4, i.e. A^2 < A_q^2 / 2: HALF a quantum at peak.
Text's "about one matter quantum per held quantum" uses the MEAN x.x; by the text's own p7, A = 16 (g A^2 = 256,
0.51 quantum) is off from round 1 and A = 20 (0.8 quantum) too. So: wherever the mass is a mass, the held hand is bent.

## E. The 24 and "chirality"
A2 of the cube group is the sign of the AXES' PERMUTATION: it is -1 on 12 PROPER rotations (90-degree face turns,
180-degree edge turns). A sense flipped by a proper rotation is not a chirality (a chirality flips under
reflections only); it is a cubic-anisotropic object (A2 of O is the l = 3 harmonic xyz in the continuum). The vacuum
breaks O to T: 12 of the lattice's own 24 turns change the vacuum. Matter tied through |k|^2 (A1) does not see it;
the named half-speed linear tie to k_im (A2) would: a fermion mass term carrying a cubic-anisotropic sign.

## F. The 00 slot's tolerance "exact to +-rest/2" (p1)
With the own push -2 rest a and teeth W = rest + c, the step is NOT the linear map (K/W != 2): the turn survives by the
fine tooth's room. At their lay r = rest/2: exact iff -rest/4 <= c < rest/2 (round 2 needs r >= -2c... see probe).
At the natural mid tooth r = W/2: exact iff -rest/5 <= c < rest/3. Either way not +-rest/2, and the room is shared
with the matter's push, so gravity shrinks the matter room.

## G. The theorem of the turn presumes the Euclidean norm
K = W gives period 6 with a^2 - a b + b^2 (the Eisenstein norm, the E table's own row (2, -1, -1, 2) halved) held
exactly; K = 3W gives period 3 with a^2 + a b + b^2 held. The text measured re^2 + im^2 for those and found it moving:
the wrong invariant. "Only W turns it with its square still" is "only K = 2W holds the GAUSSIAN square": the factor 2
is the choice of ring, CHOSEN, not derived.

## H. Clicks
No click exists on main (G5 OPEN). Every "what the clicks read" sentence is a prediction about an unbuilt part;
"the held hand never clicks" rests on an owner's word about a click that does not exist. Not measured.

## I. Probes in the text that breach the brief's rules
p4b_a1a2.py: `int(round(np.linalg.det(np.abs(m))))` = float determinant + round in a probe. lab.py uses // and
divmod and % directly, not the carry. Minor (probes, not engine), but the text says "every probe is whole numbers".
