# The hostile mathematician on the coupling family (G3.md, the whole-speed part)

The report as the reader gave it, 2026-10-30, filed by the Boss. All measurements on the real act (engine/step.tick and
untick), whole numbers, Rule3's carry the one division, trains read from world files (none declared in code). Notes
00_notes.md (the analysis, with the reader's own corrections), 01_findings.md (every item with its probe); probes
q1_turn.py .. q11_ring.py with their .out; mybench.py; worlds/*.json; run_all.sh (reruns all; run_all.log). Gamma 1000,
den 1, g 1 unless said.

VERDICT on the coupling family (whole-speed part): NOT PASSED.

## The items

1. BLOCKING. The plan is laid by hand three times and no law lays it. Place: G3 2.1-2.3, 2.6, Open 1 ("the probes lay
   the tie by hand"), every probe (own_turn(0), square_tie(1, 0)). Measured (q8): a hand of kind A1, A2, T1 or T2 tied
   through K x K -> A1 beats alike (period 266 at A 4); light untied stands, light tied on purpose beats 266; J of the
   whole plan is kept by 200 of 200 random signed permutations of the 8 tied rows ACROSS the four trains and 200 of 200
   of k's two rows: the whole-speed plan is one norm of a 10-row vector, invariant under 2^8 8! x 8 signed
   permutations, far beyond the 24, telling no kind and no train (FAMILIES4's finding holds here). Which train is held
   (gets the spring 2W), which tie, which is light are three names in disguise (law lines 84, 96). The pair rule (K
   with A2 x K) is of the held hand's own shape (A1, A2): under it the held hand ties to its own square g f |k|^4 (q8 c:
   laid, harmless by the slack, refused by nothing), so the plan exempts it by hand. Fix: derive a loader rule from the
   files' shapes alone (as trains_of derives the square flag) or keep the status OPEN; a text whose Open 1 says "laid by
   hand" is not READY.

2. BLOCKING. Within the room the held hand IS the spring on the unit that section 0 says the law refuses. Measured (q2):
   the tied T1 hand's (a, b, r) with the held hand against the same hand with the monomial (g f |k|^2 C; y, z, 1, 1) and
   no held hand: 0 of 3000 rounds differ in all seven cases (A, g, k) = (4,1,(1,0)), (10,1,(1,0)), (15,1,(1,0)),
   (4,3,(1,0)), (4,1,(1,1)), (4,1,(2,0)), (6,1,(3,0)); 8 monomials against 3; past the room they part from round 2. The
   tie adds only its back-reaction, which the room REQUIRES to be invisible; every tied mass is g f times the setting
   file's |k|^2 (decisions 35 and 37 kept in letter, broken in substance). Fix: show a regime where the held hand does
   what a unit spring cannot while the turn is exact (none exists in the whole-speed part), or name it a declared mass.

3. BLOCKING. Decision 40 (g) ("one quantum per Node-clock, from the law and not from a file") is not met. Measured
   (q3 a): every (re, im) laid is a fixed point of the turn, |k|^2 = 1, 4, 2, 25, 100, 58, 0 each held 1000 rounds; no
   push restores |k|^2. (q1 b, c): at K = 2W every row ALONE goes (a, b) -> (-b, a), period 4, now^2 + before^2 held
   per row; the two rows are independent; re^2 + im^2 at the now slots is constant only for the quadrature SEED: a (1,1)
   b (0,0) gives |k|^2 = 2, 0, 2, 0; a (1,0) b (0,0) gives 1, 0, 1, 0. (q1 d): the tied beat follows the seed: 266,
   268, 516. (q3 b): the room exists only for a held tooth born near W/2; at the loader's default 0 the turn is off at
   round 1 for any tied matter. So magnitude, quadrature, phase, sense and tooth of the held hand are all setting-file
   numbers at every Node-clock; the text's Clock layer states "D ... is one: one quantum per Node-clock" as a result.
   Fix: derive a restoring force on |k|^2 (a whole-number quartic on k with the unit is a direction, not derived here),
   or take 40 (g) back to the owner as unmet.

4. BLOCKING. The whole-speed part cannot be certified apart from the half-speed part: both ties share k. Measured (q7):
   the square-tied T1 hand beats 266 alone; with G3's own rocking tie Re(conj(L) k R) on the same k and L = R at 1, 2,
   4: |k|^2 wanders {0,1,2} .. up to 16, periods 366, 37.5, 14.5; with L = (a,0), R = (0,a) (push on k_im alone): 270,
   48.7, 35.2. Any push on k not along k breaks the quadrature and every whole-speed spring 2 g f |k|^2 wanders: no
   fixed beat. Fix: derive both ties together on one k, or state the whole-speed results hold only where no half-speed
   matter stands.

5. MINOR. Theorem of the turn, 2.1: "bounded iff |2 - c| <= 2" is false at equality (c = 0 and 4: double root, linear
   growth; q1 a: |a| = 401 in 400 rounds at both; the text's own p6 (i) shows it and 2.4 calls the edge "bounded ...
   with a linear growth"). Window is 0 < K/W < 4 (q10: 3.999 bounded 18 of 18 lays, 4.000 grows 1201x, 4.001 runs away
   10 of 18). Fix: strict inequality.

6. MINOR. "The act commutes with all 24 bit for bit" was tested on J and F only (p4, p4b). On the full act (q6, 3x3x3,
   held (A1, A2), T1 and light unalike): sources 24 of 24; tick^1, ^5, ^50 agree 24 of 24 ONLY with a negated gear's
   tooth flipped (carry(-n, W, W-1-r) = (-q, W-1-r')); unflipped 3 of 24 (the three turns negating no row), counts
   parting at round 1. tests/frame.turned permutes sites only, so no gate covers it. Fix: state the image of a gear as
   (-a, -b, W-1-r); line 94.

7. MINOR. "The turn stays exact for |00 slot| below rest/2" (section 3) is false on the negative side. Derived and
   measured (q5 a): exact iff -rest/4 <= c < rest/2 (off at -0.26 and 0.50, exact at -0.25 and 0.49); a moving slot
   (q5 c) breaks it crossing -0.25 (round 251) and 0.5 (round 260). Deeper: "its own spring is its teeth" holds at c = 0
   only; the factor is the loader's constant rest, not W; in a deeper clock the turn lives on the floor's slack, and
   tracking W would need a leg on the 00 slot, which 2.3 refuses. Fix: state the window and the constant; decide with
   G2.

8. MINOR. "The tooth walks by exactly one round's push" (2.5): at A 12, 14 the walk is 0.336, 0.448 of W against 0.288,
   0.392 (G3's own p6 (iv); q3 c: 0.448 at 14, 0.450 at 15, stable over 20,000 rounds). The edge Gamma/4 stands within
   the sampled points (exact 225, off 256). Fix: "about".

9. MINOR. "One matter quantum sits at the room's edge" (2.5): the number holds in the integer wind, the route does not.
   Measured (q4): the mean per-round wind x^2 - x_next x_before is 0.944 at A 15 (exact turn) and 1.000 at A 16 with
   the unit spring; by the text's own harmonic form D_x = A^2 sin^2 omega with the mean x.x, the quantum sits at A^2 =
   500, twice the room. The swing is a relaxation there, not harmonic. (I first derived the factor 2 as an error of the
   text; my measurement overturned my derivation, not the text's number.) Fix: derive the quantum in the wind the click
   reads.

10. MINOR. The relaxation period P = Gamma/(g|k|^2 A) + 4A is right (q4 b: to a round for A 1..24) and derivable (stand
    W/(KA), fall 2A, stand, rise); its +4A branch fails above A ~ 30 (A 40: 136 vs 185; A 100: 142 vs 410; the
    harmonic 140.5). The text's 3/pi at A_q (134; measured 134 at A 22-23) holds only with the unit spring: the held
    hand bends at round 1 at A_q (period 122). Fix: state the range.

11. MINOR. The beat's redshift "as every beat does": at A 10 and c/rest 0, 0.1, 0.25, 0.4 the periods are 140, 150,
    166, 180 (q5 b), the relaxation law 2W'/(KA) + 4A, not sqrt(W'/W) (147, 157, 166). Below the quantum's amplitude
    the redshift law differs. Fix: say the regime.

12. MINOR. "The spectrum of one plan is wide" (section 4): g is CHOSEN 1 alike for every train and every K x K -> A1
    row is 1 or the dot product, so every tied train has ONE mass, the time gear's own beat (2 pi sqrt(Gamma/2) =
    140.5); a g per train is a coupling declared in a file (decision 35). Fix: strike.

13. MINOR. "The one drive serves every row (40 (d)) as built": at T_d = 1 the drive is the identity, q_d = J, r_d = 0
    always (q2: the drive's tooth stayed 0 in every run); term 7's DERIVED rests on a no-op.

14. MINOR. Section 3's dispersion "probe 4 runs it": p4 measures no dispersion. I measured it (q11, ring of 64, the
    mode's projection): light 156.94 against 156.8, the tied wave 104.70 against 104.6: it HOLDS to 0.1 per cent. Fix:
    cite a measurement.

15. MINOR. Large |k| near the window's top (q9 a): the held hand at (44, 0), K/W = 3.872, with a tied hand at A 1 runs
    away in 16 rounds (the turn bends first), where the unit spring at 3.875 is bounded 18 of 18 (q10): the top is
    softer for the held hand; "g up to 2 Gamma spans masses up to the window's top" is not reachable through |k|^2.

16. MINOR. The probes' own rule: lab.py declares the trains in code, uses // and % outside the carry (ratio, blank,
    p4's site map), round and np.linalg.det in p4b.

## On the three questions put to the reader

(a) FAMILIES4: the tie through re^2 + im^2 ties every kind alike and tells no train (items 1, q8). (b) The contraction
group: G3's tie table is the generic K x K -> A1 norm, trivially I-invariant and in fact invariant under all signed
permutations of the tied rows; the group question bites only the half-speed linear tie, which is not in this part. (c)
G5's physicist: his description applies verbatim (q1 e: the mirror reverses the sense, (1,0)->(0,1) forward, the
mirrored (0,-1)->(-1,0)); the whole-speed tie is blind to the sense (0 of 2000 rounds differ), and the held hand is
invisible exactly where it is the unit (item 2) and visible exactly where the turn bends (q3 b: the room depends on the
lattice phase through the born tooth). Its own energy (rest |k|^2 per Node-clock) touches nothing on the square in this
text: declared invisible to the metric, the physicist's to weigh.

## Derived, measured, overclaimed

WHAT IS DERIVED: the exact integer leapfrog v+ = v + J, a+ = a + floor(v+/W) with v = W(a - b) + r; J = -grad V with a
leg standing twice pushed twice; the turn at K = 2W per row; the beat 4 sin^2(omega/2) = K/W in the real-count limit;
the relaxation period (item 10); the 00-slot window (item 7); the tooth flip (item 6). WHAT IS MEASURED: the room's edge
225 < g A^2 < 256 at k (1,0), stable 20,000 rounds; the beats 266 (A 4), 140 (A 10); the window's top; the bend past the
room; the dispersion. WHAT IS OVERCLAIMED: items 2, 3, 6-15 as stated, and "ready for a pair" (section 8).

## Sound, with numbers

The turn (a, b) -> (-b, a) exact at K = 2W for every whole (a, b), on one Node-clock and on 3x3x3, at den 1, 7,
1.5 x 10^16 (G3's p1; q1); the plan's J and F turn with the 24, 24 of 24 (q6; the engine's T1 matrix is the turn itself
at 24 of 24 candidates); the full act's 24 with the flip, 24 of 24 at 1, 5, 50 rounds; the run back exact in every
bounded run (q2, q5, q9, q11); the step's window 0 < K/W < 4 (q10); the tied beat 266/140 against the relaxation law to
a round; the dispersion 156.94/156.8 and 104.70/104.6 (q11); the tooth's walk bounded [-0.450, +0.002] of W over 20,000
rounds at A 15.

## A side finding beyond G3 (q11)

A smooth light wave of amplitude 50 on the ring heats by the act's rounding (the force reads rounded neighbour counts):
size sum x^2 80,180 -> 4,035,064 and max |x| 50 -> 324 in 3000 rounds, the tied wave only 80,180 -> 86,851; G3's p4
amplitudes "up to 16" from lays within 1 and 3 are this heating. It bears on light's claims elsewhere.

## Questions for the Boss

Does decision 40 (g) allow a seed-laid |k|^2 (item 3), and is a per-site setting lay of the held hand's tooth at
3 den Gamma^2 acceptable; does line 94's "carried by its kind" include the tooth flip (item 6); is the held hand to read
the 00 slot at G2 (item 7).

## Solution24

Step 1 failed on items 1-3 (the plan does not follow by itself and was declared by hand), step 3 on item 2 (a declared
mass under another name), step 9 is this reading; add to step 8 that a probe reports which lays it chose by hand and why
no rule chose them.
