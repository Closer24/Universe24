# FACE, the hostile mathematician's report, 2026-10-31

(Written by the Boss from the reader's hand-back, the reader's harness having refused the write; the text is the
reader's, shortened in layout. Read: sections 0, 1, 2 and 7, the frozen probes and outputs, the engine's carry.py,
step.py and kinds.py. In fc_math/: copies of face_lib.py, face_p1_gear.py (its .txt rerun identical to the frozen),
face_p2_act.py; the reader's fm_probe.py (fm_probe.log: M1 face against reader, M2 E, M3 one clock on 1, 2 and 3 rows,
M4 partial), fm_touch.py, fm_room.py, fm_units.py, fm_back.py, each with its output. Whole numbers, Rule3's carry the
one division, the senses read as step.halves reads them, trains read by name from the shipped files.)

VERDICT on FACE: NOT PASSED. Section 2 (the quaternion) has two DERIVED claims that fail, on paper and in whole-number
algebra (B1, B2). The clock fix itself (section 1, T1 to T4) is SOUND as a gear on the board, with minors. T6 is an
estimate; the reader's scan supports its form but puts its constant about 4 times lower.

## BLOCKING

B1. The face counts the train's gear crossings, not the clock's beats; beyond the two-row held hand it is no unit's
exponent (section 0 "L_i for the held hand, R_j for the line hand ... the face is the unit's exponent lifted to the
integers, z_t = i^f z_0"; Q2 "the face counts the units"; Q3 "the face mod 4 is the hand's phase"; Q4 "f = the
quotient of the phase by the half turn"; Q5 "the integer lift of the hand's unit part").
- Paper: C is a sum over rows; a lay that lights n rows in phase books n crossings per half beat. Q2's identity
  |s+t| + |t-s| = 2 is about one pair of components, so it gives one count per step only for a hand of exactly two
  rows that turn into each other. The held hand (A1 + A2) is two rows, each at the quarter mode a+ = -b, laid in
  quadrature; Q2's "line hand at the quarter mode" is the same per-row step on one row. The face reads 1 per i on the
  first and 1/2 per j on the second, and Q2 says so itself ("by 1 per j^2"), so section 0's "R_j ... the unit's
  exponent" contradicts Q2. Q3 reads the face in quarter turns and Q4 in half turns: two different units.
- MEASURED (algebra, fm_units.txt): L_i on a 4-gear Lipschitz hand gives 4 per turn at (1,0,0,0) and (3,2,0,0), but 8
  per turn at (1,1,1,1) and (2,-1,5,3): 2 counts per i wherever both complex halves are nonzero.
- MEASURED ON THE BOARD (fm_probe.log M3; the click world's law at a lone Node-clock, the held hand as shipped, rounds
  1 to 1,500; the giver laid at about one |x|^2): lay (40,0,0) face 8; (28,28,0) 12; (23,23,23) 18. The held hand keeps
  its cycle in all three; the 24 keep the face, but no symmetry of the law joins these lays: one clock's count depends
  on how many of its rows the lay lights. So D6 between two clocks "of one kind" compares unlike units unless the lays
  match row for row; the header's rest beat [g, W] does not record this.
- Fix: state what the face is (the train's gear crossings, counted with the number of rows that cross); keep Q2 for a
  two-row hand turned by one unit (the held hand); put the line hand's "1 per j^2" into section 0; drop "the face
  counts the units" as a general statement; give the header the lay's crossing multiplicity, or the lay itself; OPEN:
  a face that counts a clock's beats whatever its row structure.

B2. Q3's half-speed count ("8 units per return, the face mod 8 its phase") is marked DERIVED but is false on the one
integer carrier where the 48 act by signed permutations.
- Paper: Q1 names the 24-gear train (Z[2O] with -1 = -1). There left multiplication by an order-8 unit u acts freely on
  the 24 pairs, u^4 = -1: six signed 4-cycles (x1,x2,x3,x4) -> (-x4,x1,x2,x3), up to a re-signing of the gears the face
  cannot see. On a 4-gear Hurwitz hand no order-8 unit is whole (the Hurwitz units 2T, orders 1, 2, 3, 4 and 6), so Q3
  has no other carrier.
- MEASURED (algebra, fm_units.txt), C per step on the order-8 4-cycle (face per return of 8 steps): (1,0,0,0) 4 (8);
  (1,1,0,0) 4 (8); (1,-1,0,0) 8 (16); (1,-1,1,-1) 12 (24); (3,-2,5,-7) 12 (24). At 16 per return the face mod 8 reads
  the step only mod 4.
- Fix: take the half-speed count out of DERIVED and state it OPEN, with this counterexample.

## MINOR

1. Touches: T1 is sound but books a touch of 0 as a crossing ((+, 0, +) gives V = 2, while 1.1's half beat is a sign
   change). Expected at small lays, not borne out: 0 touches on the lone gear in 169 lays ([-6,6]^2) x 4 springs x
   3,000 rounds (fm_touch.txt). Say so in T1.
2. The reader's first reading overturned: fm_probe.log M1 shows the face differing from SHADOW's reader at 24, 22 and
   20 of 49 lays, first read as touches; it is not (the touch count is 0): every difference is 1, the booking at the
   lay's end (a lay pair that is itself a crossing, tooth 2), T1's "within one half beat at each end".
3. T2's notation: "a tooth kept would need r + r' to be constant" should read r + phi(r) constant, for the tooth's
   mirror phi (the flip gives 3; the identity 2r, not constant).
4. The full act's run back: the text checks 40 rounds; the reader ran 200 rounds of the click world as shipped, round
   by round: the face 0 of 200 misses (faces at site 0 [0, 0, 200, 1, 0]); m1 200 of 200 misses (fm_back.txt). m3 on
   the full act and the whole 5,000 rounds still open (OPEN 11 and 12 stand).
5. An if: face_lib.gear_face line 92, "vary = varied if sign is None else sign", is an if inside a function section 8
   says has none; a mutant hook: move it into the probe.
6. The dial: 4 = senses x senses is read from the star by value only; its first 2 is the sign's two values (a crossing
   is |1 - (-1)|), its second the window's two pairs (the passing's X(S) + X(S+)), not the star's senses. The engine
   reads all its 2's from step.halves the same way: its convention, not a new breach. Name it.
7. Typed counts in the probes: face_p1_gear line 29 types SENSES = 2 (the lone gear's dial typed, not read from the
   star); face_p2_act types the train indices 2, 3 and 4 (lines 66, 174-176, 201), against "no train named in code".
8. Values aimed at a root or an angle (tonight's ruling), in the probes only (the face's own functions type none): aimed
   at a root, g/W = 1/400 is a square (whole root 20, "a beat of about 126 rounds"), and the depths 1, 4, 16 are
   squares (from the Boss's brief); aimed at the quarter turn, the quarter mode 2 W and the "rest's quarter spring"
   2 rest. See question 1.
9. Two new layout fields: the face multiplies each train's sum by the loader's matter flag (0 on the square) and needs a
   row-to-train map; neither is in the act's layout today (face_act takes them as arguments); both are part of the act
   change (OPEN 10).
10. T3's 24 at a lone Node-clock only: A2 never exercises the 24's permutation of the 27 sites; the derivation covers it
    by locality (A4); one turned 3x3x3 run would close it.
11. E: its failure is stated (section 0 "all but E", T3, OPEN 2). MEASURED (fm_probe.log M2): 8 of the 24 E matrices in
    kinds.py are signed permutations; on an E window C changes under 8 of the 24 turns (2 against 4; 3 against 4). No
    change of basis fixes it (the 24 act on E through S3, not a subgroup of the signed permutations of 2 rows, of order
    8). Tonight it does not matter (no E matter train is laid; the metric's E sits in the square's monomial tensor
    basis; the face gives the square the factor 0); it matters for the act change (the loader lays E, so the face would
    break "the 24 act on everything" on any world with an E matter train). Repair: an E hand on three rows that sum to
    0 (like the square's diagonal), or restrict the face by the owner's word.
12. Q1 is right only as a relabeling: C = ||sg q_t - sg q_t+1||_1 holds for a two-part hand, q = z_now + z_before j a
    quaternion of two TIME slots, while the 24's sandwiches act on the SPACE quaternion h = a + xi + yj + zk (A1 + T1):
    Q1 joins two different quaternions. The face's keeping needs only "a signed permutation of a train's rows" (T3); no
    proof uses the quaternion product. The left and right multiplication claims (Q8 monomial; the halves not; the
    24-gear train is) are correct.
13. Q4: the crystallographic restriction is correct (orders 6, 4 and 3 at k/W = 1, 2 and 3; parabolic at 0 and 4).
    "That is Rule3's carry on the phase" is overclaimed: the face's carry has the crossings as dividend and the dial 4
    as divisor; its tooth books a half-seen crossing, not "the hand within its half turn"; no phase is a number of the
    state.
14. Q5 is an interpretation, not a theorem (the shared window and parity bookkeeping true and well put); "the integer
    lift of the hand's unit part" inherits B1.
15. T6: neither proved nor measured as stated. "DERIVED by scaling" is accurate, but the bold no-go reads as a theorem
    and is an order-of-magnitude estimate (the room is "the tie's push rounds away", the stride the beat times |x|).
    A5, one world 25,000 times out, tests neither the room's size nor the sqrt(|k|) cap. The reader's scan
    (fm_room.txt; the click world's law at a lone Node-clock, the giver at (n,0,0), the held hand in quadrature, 1,200
    rounds): held |k|^2 1: keeps its cycle to |x|^2 |k| 2,025, leaves at 2,500 (round 289), the giver's largest
    stride in the room 1 (sqrt|k| 1); |k|^2 9: 1,875, leaves at 2,700 (round 1), stride 1 (1.7); |k|^2 25: 1,125,
    leaves at 3,125 (round 1), stride 2 (2.2). The form holds (the room's |x|^2 goes as 1/|k|, the stride at most
    about sqrt(|k|)); the constant is about 4 times smaller than T6's W/(hold f |k|) = 10^4/|k| (the room about
    W/(4 hold f |k|)); the edge is not sharp (at |k|^2 = 25 the held hand leaves at round 991 at |x|^2 |k| = 500 and at
    round 714 at 2,000, yet 1,125 holds for all 1,200 rounds). Fix: "ESTIMATED by scaling; MEASURED by the scan", the
    constant given, and the edge's dependence on the run's length said.
16. "The 48's -1 measured on the tied hands' sign (A3, G6)" measures the law's evenness x -> -x on whole-speed hands;
    no half-speed hand is laid. Name it so.
17. T4's "x^2 + 1 and the 4 are read from the star's senses": only the 4 is read from the star; x^2 + 1 is made from
    the count and the 1.

## SOUND

- T1's identity 4f + r = 2V + v(lay) - v(last), derived again on paper (every pair read twice except the lay's and the
  last; the carry's identity sums); G1 holds it at all three depths; face_p1_gear rerun byte-identical (637, 318, 159,
  reader equal, identity True).
- T2, the run back: the mirror (f, r) -> (-f, 3 - r) an involution inverting the face's round, the carry lemma checked
  on paper; C even under the window's reversal; the backward window (a+, a, b), negated on an odd row, matches
  step.mirror. Round by round the face misses 0 times: lone gear above a notch 4,000 rounds; lone gear at the click
  world's stride 4,000; full act 40 (the text) and 200 (the reader). The mutants fail round by round on the lone gear
  (m1 at 64 and 20, m2 at 128 and 60, m3 at 128 and 40). The text's own correction is right: a whole-run return passes
  m2 and m3, their errors cancelling over a run that starts and ends at tooth 0.
- The sign test: carry.py's floor (0 <= r' < d) makes x div (x^2 + 1) equal -1 for x < 0 and 0 otherwise (the loader
  uses the same test); v = |sg x - sg y| by the two squares, checked.
- No if, loop, mask or bound in below, varied, crossed, face_act, face_mirror, face_untick or gear_mirror (gear_face
  aside, minor 5). The face pushes nothing into the act.
- The 24 and the 48's -1 on A1, A2, T1 and T2 (signed permutations): derived. A2 holds 24 of 24 in both windows, A3 is
  kept, G6 keeps (18, 1) while m6 does not. Q2's identity holds in all eight cases.

## DERIVED / MEASURED / OVERCLAIMED

- DERIVED: T1; T2; T3 on the monomial kinds; T4 (with minors 5 and 9); Q2 for the two-row held hand; Q4's orders.
- MEASURED ON THE BOARD: the frozen G1-G6 (rerun identical) and A1-A5; the reader's M3, M4 and M6 (the act) and M1 (the
  lone gear). MEASURED as algebra: M2 (E) and M5 (the unit steps).
- OVERCLAIMED: "the face counts the units" and "the unit's exponent" in general (B1); Q3's half-speed count, false
  (B2); "Rule3's carry on the phase" (minor 13); T6's no-go stated as a theorem (minor 15); Q5's "one structure"
  (minor 14).

## Questions for the Boss

1. Does tonight's ruling (a value aimed at an angle or a root) cover the shipped held hand's spring 2 rest, its exact
   quarter turn? T5, T6, A1-A5 and Q2's held hand all rest on it.
2. A clock whose lay lights n rows gets a face that books n crossings per half beat: acceptable as "a clock's own count"
   for D6, or must the face count a clock's beats whatever its row structure?
3. For the act change: may the face carry E on three rows that sum to 0, or does the owner's word restrict it to the
   monomial kinds?

## Solution24

The gear of section 1 is a sound clock fix on the board and can stand as DRAFTED until the owner rules on the act
change. Section 2 should be cut back to what holds (Q1 as a relabeling, Q2 for the two-row held hand, Q4's restriction)
before anyone cites it.
