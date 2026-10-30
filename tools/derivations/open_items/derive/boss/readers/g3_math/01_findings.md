# g3_math: findings on G3.md (term 6 at G3, the coupling family, whole-speed part)

Hostile mathematician, new to the project, 2026-10-30. Everything below is measured on the real act (engine/step.tick and
untick) by the probes q1..q11 in this folder (whole numbers; Rule3's carry the one division; trains read from ./worlds/*.json,
none declared in code; outputs in the .out files; run_all.sh reruns them). Where G3 and I disagree the number is from my run,
and G3's own .out is cited where it already shows the same.

## VERDICT: NOT PASSED (the whole-speed part is not ready for code)

## The blocking items

B1. The plan is laid by hand three times, and no law of the act or the loader lays it (the owner's law: only generic laws).
    Place: G3 2.1-2.3, 2.6, section 7 item 1 ("the probes lay the tie by hand"), every probe (own_turn(0), square_tie(1, 0)).
    Measured: (q8 a) a hand of kind A1, A2, T1 or T2 tied through K x K -> A1 beats alike, period 266 at A 4, g 1, Gamma 1000;
    light (A1 part 2) untied stands, tied on purpose beats 266: the act ties whatever is laid. (q8 b) J of the whole-speed plan is
    kept by 200 of 200 random signed permutations of the 8 tied rows ACROSS the four trains (k fixed), and by 200 of 200 of k's
    two rows: the plan is a norm of a 10-row vector, invariant under 2^8 8! x 8 signed permutations, far beyond the 24; it tells
    no kind and no train (FAMILIES4's finding holds here: the norm tells no kind). So which train is "held" (gets the own spring
    2W), which trains tie, and which is light are three names in disguise (line 84, 96). The pair rule (K with A2 x K) is itself
    of the held hand's shape (A1, A2): under it the held hand ties to its own square, V = g f |k|^4 (q8 c: laid, the turn holds by
    the slack, nothing refuses it), so the plan exempts the held hand from its own rule by hand.
    Fix: derive a loader rule from the files' shapes alone (as trains_of derives the square flag), or declare the status OPEN; a
    text whose own Open 1 says "laid by hand" cannot be READY.

B2. Within the room the held hand IS the spring on the unit the text says the law refuses.
    Place: G3 section 0 ("a pull toward a rest written on the unit (the monomial f x x 1 1) is a mass laid by hand, which the law
    refuses"), 2.3, 2.4.
    Measured: (q2) the tied T1 hand's (a, b, r) with the held hand against the same hand with the monomial (g f |k|^2 C; y, z, 1, 1)
    and no held hand: 0 of 3000 rounds differ, for (A, g, k) = (4,1,(1,0)), (10,1,(1,0)), (15,1,(1,0)), (4,3,(1,0)), (4,1,(1,1)),
    (4,1,(2,0)), (6,1,(3,0)); 8 monomials against 3; the run back exact. Past the room (A 16 (1,0); A 12 (2,0)) they part from round 2.
    So the whole-speed tie adds nothing to a declared mass but its back-reaction, which the room REQUIRES to be invisible
    (absorbed in r_k). The mass of every tied train is g f times the SETTING file's |k|^2: decision 35 ("no mass ... declared in
    any file") and 37 ("a train's spring is never an input") are met in letter and broken in substance.
    Fix: either show a regime where the held hand does something a unit spring cannot while the turn stays exact (there is none
    in the whole-speed part: q2), or name the tie for what it is.

B3. Decision 40 (g) is not met: nothing in the law fixes |k|^2 = 1, nor the quadrature that makes re^2 + im^2 stand.
    Place: G3 section 1 ("Its stored winding D ... is one: one quantum per Node-clock"), 2.1, 2.2, 3; Open 3 half-says it.
    Measured: (q3 a) every (re, im) laid is a fixed point of the turn: |k|^2 = 1, 4, 2, 25, 100, 58, 0 each held for 1000 rounds;
    no restoring push on |k|^2 exists in the plan. (q1 b, c) at K = 2W every row ALONE goes (a, b) -> (-b, a), period 4, with
    now^2 + before^2 held per row; the two rows are independent (no monomial couples them). re^2 + im^2 at the now slots is
    constant only for the quadrature SEED (im laid as re's before): the in-phase seed a (1, 1) b (0, 0) gives |k|^2 = 2, 0, 2, 0;
    a (1, 0) b (0, 0) gives 1, 0, 1, 0. (q1 d) the tied hand's beat follows the seed: period 266 (quadrature), 268 (in phase),
    516 (half laid, the mean spring halved). (q3 b) the room exists only for a held tooth born near W/2: born at 0, the loader's
    default (load.lay), the turn is off at round 1 for any tied matter (A 4 and A 10); born at W/8 it fails at A 10.
    So the magnitude, the quadrature, the phase, the sense and the fine tooth of the held hand are all the setting file's
    numbers at every Node-clock (2 x sites gear lines, each with 3 den Gamma^2), not the law's. "The held hand is a turning
    hand" is the act's (one row suffices); "its square stands still", "one quantum", "D = 1" are the seed's.
    Fix: derive a restoring force on |k|^2 (a Mexican hat in whole numbers, e.g. a quartic on k with the unit, is a direction,
    not derived here), or state that the vev is a seed number and take 40 (g) back to the owner.

B4. The whole-speed part cannot be certified apart from the half-speed part: both ties share k, and the named half-speed tie
    destroys the whole-speed beat.
    Place: G3 2.6 ("the whole-speed part is built here on the act"), section 8 ("ready for the pair").
    Measured: (q7) the square-tied T1 hand at A 4 beats 266 alone; with G3's rocking tie Re(conj(L) k R) laid on the same k and
    L = R at rest at 1: |k|^2 wanders {0, 1, 2}, the period 366; at 2: |k|^2 up to 16, period 37.5; at 4: period 14.5. With
    L = (a, 0), R = (0, a) (the push on k_im alone): 270, 48.7, 35.2. G3's own p5 (b), (c) show the same wandering. Any push on k
    not along k breaks the quadrature of B3, and every whole-speed spring 2 g f |k|^2 wanders with it: no fixed beat, no mass.
    Fix: the two ties must be derived together on one k, or the whole-speed part must say its results hold only where no
    half-speed matter stands at the Node-clock.

## The minor items (each true as measured by G3 at its points, false or overclaimed as stated)

M1. The theorem of the turn, 2.1: "bounded iff |2 - c| <= 2" is false at equality: c = 0 and c = 4 are a double root with a
    Jordan block, linear growth (q1 a: |a| reaches 401 in 400 rounds at both; G3's own p6 (i) shows it and 2.4 calls the edge
    "bounded ... marginal with a linear growth", a contradiction). The window is open: 0 < K/W < 4. (q10: the unit spring at
    K/W = 3.5 .. 3.999 bounded in 18 of 18 lays, 4.000 grows to 1201 x, 4.001 runs away 10 of 18.)
    Fix: write the strict inequality; "periodic iff 2 - c in {-1, 0, 1}, periods 3, 4, 6" stands.

M2. "The act commutes with all 24 (line 94)", "the 24 hold": tested on J and F only (p4, p4b). On the full act the images hold
    bit for bit only when a negated gear's fine tooth is flipped, carry(-n, W, W-1-r) = (-q, W-1-r'): (q6, 3x3x3, held (A1, A2),
    T1 and light unalike) sources 24 of 24; tick^1, tick^5, tick^50 with the teeth flipped on negated rows 24 of 24; unflipped
    3 of 24 (the three turns that negate no row), the counts parting at round 1. tests/frame.turned permutes sites only, so no gate
    covers it. Fix: state the image of a gear as (-a, -b, W-1-r) and say so in the law's line 94.

M3. "The turn stays exact for |00 slot| below rest/2 (probe 1)" (section 3): false on the negative side. Derived and measured
    (q5 a): with the own spring fixed at 2 rest and r at rest/2, the cycle is exact iff -rest/4 <= c < rest/2 (off at -0.26 and
    0.50; exact at -0.25 and 0.49); a moving slot (q5 c) breaks the turn where it crosses -0.25 (round 251 at -0.001 rest a
    round) and 0.5 (round 260 at +0.002). Deeper: "its own spring is its teeth" holds at c = 0 only; the factor is the loader's
    constant rest, not W, and in a deeper clock the turn is held by the floor's slack. To track W the spring needs a leg on the
    00 slot, which 2.3 refuses. Fix: state the window and the constant; decide with G2 whether the held hand reads the clock.

M4. "The tooth walks by exactly one round's push" (2.5, p6 (iv)): 2 g A^2 / Gamma = 0.288 and 0.392 at A 12 and 14, the walk
    measured 0.336 and 0.448 (G3's own numbers; q3 c: -0.448 at A 14, -0.450 at A 15, stable over 20,000 rounds). The edge
    Gamma/4 stands within the sampled points (exact at 225, off at 256) by accident of the 15 per cent. Fix: "about".

M5. "One matter quantum sits at the room's edge" (2.5): right in the integer wind, wrong by the route written. Measured (q4):
    the mean per-round wind D_x = x^2 - x_next x_before is 0.944 at A 15 (exact turn) and 1.000 at A 16 with the unit spring
    (the held hand is off at round 1 there); the text's own form D_x = A^2 sin^2 omega with "its mean x.x is half that" puts
    D_x = 1 at A^2 = 500, twice the room. The relaxation swing is not harmonic there. Fix: derive the quantum in the wind the
    click will read (G5's key), not in the harmonic form.

M6. The relaxation period P = Gamma/(g |k|^2 A) + 4 A: measured right (q4 b: to a round for A 1..24), and derivable: v falls
    from ~W to 0 by K A a round (W/(K A) rounds), falls one count a round (2A), stands (W/(K A)), rises (2A). It holds while
    K A < W; the +4A branch fails above A ~ 30 (A 40: 136 against 185; A 100: 142 against 410, the harmonic 140.5). The text's
    minimum 4 sqrt(Gamma/g) at A^2 = Gamma/4g (126.5; measured 126 at A 15..18) and 3/pi of the harmonic at A_q (134.2;
    measured 134 at A 22..23 with the unit spring) stand, but A_q is outside the room (the held hand bends at round 1 there,
    period 122). Fix: say the range; say the held hand does not reach A_q exactly.

M7. The beat's redshift (section 3, "redshifts with W as every beat does"): at A 10, c/rest = 0, 0.1, 0.25, 0.4 gives periods
    140, 150, 166, 180 (q5 b), the relaxation law 2W'/(K A) + 4A (150, 165, 180), not the harmonic sqrt(W'/W) (147, 157, 166).
    Below the quantum's amplitude the redshift law is another law. Fix: say which regime.

M8. "The spectrum of one plan is wide" (section 4): g is CHOSEN 1 and alike for every train, and every K x K -> A1 row is 1 or
    the dot product, so every tied train has ONE mass, the time gear's own beat at |k|^2 = 1 (2 pi sqrt(Gamma/2) = 140.5). A g
    per train is a coupling declared in a file (decision 35). Fix: strike "wide"; one mass for all tied matter is the result.

M9. "The one drive serves every row (decision 40 (d)) as built" (2.4): at T_d = 1 the drive is the identity, q_d = J, r_d = 0
    always (q2: the drive's tooth stayed 0 in every run). Term 7's "DERIVED (G3)" rests on a no-op. Fix: say so.

M10. "The modes of a board obey 4 sin^2(omega/2) = 2 g |k|^2/Gamma + (1/6) sum 4 sin^2(q_i/2) ... probe 4 runs it" (section 3):
    p4 measures no dispersion (images and boundedness only). Measured here (q11, a ring of 64, the mode's projection): light
    156.94 against 156.8, the tied wave 104.70 against 104.6: the relation HOLDS to 0.1 per cent. Fix: cite a measurement.

M11. Large |k| near the window's top (q9 a): the held hand at (44, 0), K/W = 3.872, with a tied hand at A 1 runs away in 16
    rounds (the turn bends first: the tied hand's swing near the top grows, the room Gamma/(4 q) = 5.7 is passed, |k|^2 moves),
    where the unit spring at K/W = 3.875 is bounded in 18 of 18 lays (q10). The text's "g up to 2 Gamma spans masses up to the
    window's top" is not reachable through |k|^2 with an exact turn. Fix: the top is softer than the window for the held hand.

M12. The probes' own rule: lab.py declares the trains in code (TRAINS), uses // and % outside the carry (ratio, blank, p4's
    site map), and `round` and `np.linalg.det` in p4b. Fix: carry only; trains from files.

## What is SOUND (re-derived or re-measured here)

S1. The act is the exact integer leapfrog v_{t+1} = v_t + J_t, a_{t+1} = a_t + floor(v_{t+1}/W) with v = W (a - b) + r; J = -grad V
    exactly, a leg standing twice pushed twice (q2, q8 b: the pushes as written in 2.1, 2.3).
S2. At K = 2W one row turns (a, b) -> (-b, a) exactly, period 4, now^2 + before^2 held, for every whole (a, b) (q1 a, b; G3 p1 at
    den 1, 7 and 1.5 x 10^16).
S3. The beat 4 sin^2(omega/2) = K/W = 2 g |k|^2 / Gamma in the real-count limit; measured 266 (A 4), 140 (A 10) against the
    relaxation law to a round; the step's window 0 < K/W < 4 (q10: 3.999 bounded, 4.001 runs away).
S4. The plan's J and F turn with the 24 (q6: 24 of 24, with the engine's own kinds' matrices at each candidate; KS.t1[g] is the
    turn itself at 24 of 24), and the full act with the teeth flipped (24 of 24 at 1, 5, 50 rounds).
S5. The run back is exact in every bounded run (q2, q5, q9, q11), the drive's tooth 0.
S6. The dispersion on the ring holds to 0.1 per cent (M10).
S7. The room's edge for k (1, 0), g 1, Gamma 1000 is between g A^2 = 225 (exact 20,000 rounds) and 256 (off at round 1), the
    walk bounded and not drifting at Gamma 1000 (q3 c).
S8. The mirror reverses the sense (q1 e: (1, 0) -> (0, 1) forward; the mirrored state (0, -1) -> (-1, 0)); the whole-speed tie
    is blind to the sense (0 of 2000 rounds differ). G5's physicist's description applies verbatim: a medium at rest in the
    lattice's frame with a sense, reversed by the mirror; here it is invisible exactly where it is the unit (B2) and visible
    exactly where the turn bends (q3 b: the room depends on the lattice phase through the born tooth).

## A side finding for the Boss, beyond G3
    A smooth light wave on the ring (no spring) heats: size sum x^2 80,180 -> 4,035,064 and max |x| 50 -> 324 in 3000 rounds,
    while the tied wave heats slowly (80,180 -> 86,851); the mode's period is clean in both (q11). The force reads rounded
    neighbour counts, so the rounding errors do not cancel across sites and pump the short waves. G3's p4 amplitudes "up to 16"
    from lays within 1 and 3 are this heating. It is the act's, not G3's; it bears on light's claims elsewhere.
