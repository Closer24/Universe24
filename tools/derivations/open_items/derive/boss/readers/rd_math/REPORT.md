# The hostile mathematician on the root dial (W = L^2, the dial L(b) + L(a), the push divided once at L(now))

The report as the reader gave it, 2026-10-30, filed by the Boss. Files beside it: probe_rd1_rounding.py to
probe_rd6_defs.py with their .txt, 02_derivations.md (the paper derivations D1-D7), 03_findings.md, rerun/. Whole
numbers, tensor24.algebra.carry.carry the one division, no float, root, round, math, random; paths by joinpath; no
train declared. probe_rd3, rd5 and rd6 import the FROZEN copies in scratchpad/rootdial_read. The three frozen probes
rerun byte-identical (probe_root 0.7 s, probe_root_generic 26 s, probe_rootdial 1.3 s), so the derivers' numbers
stand; what follows is about what they mean.

VERDICT on the root dial: NOT PASSED

Not as "the three conditions met". The algebra is right and reproducible; the conditions are met only with prices
that are law changes, one against a law sentence as written (K-S3), and condition 3 stands on an item ONE_ALGEBRA
itself leaves OPEN (the frame train). The texts name some of the prices and not all.

## Items

1. BLOCKING (condition 1, "Rule3 the one division"; ROOT.md section 1 rows 3 and 5; EDGE2 section 3). The push's
   division at L(now) drops its remainder. Rule3's carry keeps it (carry.py: "q leaves, r' stays"; line 100: "a
   division outside Rule3's carry is a hidden remainder"); ROOT.md itself: "(ii) covers it only read as the lapse's
   coefficient", "does not follow from (ii) without a clause". Measured cost the texts do not name (probe_rd3_board.txt
   B): the row's total momentum SUM_sites P, exact to the bit under the built act and the edge on the same board (SUM
   F = 0 enters unrounded; drift 0 over 40 rounds), drifts under the root dial at 40 of 40 rounds on a UNIFORM
   STANDING clock L = 9: per-row drift over 40 rounds -60 to +44 teeth of P, one-round drift up to 16 (= 4 q_F units),
   since SUM odd(F_i / L) != 0 while SUM F_i = 0 (D4: F = (3, -1, -1, -1), L = 2 gives -1). An exact book of the board
   is lost (Solution24 step 6: "the carry keeps its sum exactly"). Size: immaterial at the calibre (drop <= L/2 ~
   1.5e11 against pushes ~ 1.5e22); the standard is exactness. Fix: write (ii)'s clause and this loss into the price
   list for the owner; or round the push per Mesh end at a dial common to both ends (keeps SUM = 0 on a uniform
   clock); or keep the W dial.
2. BLOCKING (condition 1, "nothing declared"; line 100 "no condition is typed on the integers"; ROOT.md A3 and section
   1 row 6). L_rest whole needs 6 den a square, so den = 6 k^2 (6 is squarefree) or a new file key k: a condition
   typed on den that no symmetry gives, and it puts the prime 3 (= 3 mod 4) into den against K-S3 (line 110): "den is
   chosen by its structure, the primes 1 mod 4 and their powers". Measured (probe_rd4_den.txt): none of the law's dens
   runs the root dial: the example's 15162856759112389 (6 den = 2 mod 4), the hand's 3311818282 and the cheap 697786
   (6 den = 6 mod 9, no square). With den = 6 k^2 every lift (num, s) on den's circle is 6 times a lift of k^2 (k <=
   30: every lift divisible by 6; 20 of 30 k have no lift at all, those without a prime 1 mod 4): the gears' pairs
   carry a dead factor 6 and the rates' group law runs at den' = k^2. ROOT.md's "line 110 calls den's parity a
   finding" is right about parity and silent about the factor 3. Fix: the owner's word on a new K-S3 (den = 6 k^2 with
   k holding a prime 1 mod 4, two lifts), or a teeth law whose rest is a square by construction (a new derivation of
   line 100's W; nothing cheap).
3. BLOCKING (condition 1, "one carry": the summary's "divided once at L(now) by a carry", EDGE2 section 3 "carried
   once at the pivot's root"; ROOT.md A2). DERIVED (D3): the one-carry quotient half_up(F, L) = floor((2F + L)/(2L))
   is odd under F -> -F iff L is odd; at an even L it fails at every tie F = L/2 mod L. Measured (probe_rd1_rounding.txt
   A): 148 misses of 1452, all at even L, 0 at odd; L in [1, 60]: every even L misses, no odd L. L = 6 k Gamma + c00
   is even at rest and takes c00's parity. On the board (probe_rd3_board.txt A) the 24 fall to 3 at standing L = 8,
   12, 16, 20, 24 and hold at 9, 10, 11, 14, 18: there the push is 6 m (grip 6, J = 0) and the tie 12 m = L mod 2L
   needs 4 | L; with the kick or moving grips every even L has its tie. Line 100: "A rule that holds at one parity only
   is not a rule of the law." The cure, (iv)'s odd rounding, is 5 carries in ROOT.md (3 suffice: probe_rd1 B, 0
   differences of 16040) and reads the SIGN of a state quantity in the Node-clock every round; today src reads a sign
   and lit() at the load alone (load.tables, load.first), the act's gear is one carry. So "one carry" is overclaimed:
   the push's quotient is a signed rounding, a new primitive of the act, lawful under (iv) as written. D's parity is
   irrelevant: the half-open split at the dial 2D is odd with -1 - s at every D (D1); L's parity decides. Fix: name the
   primitive (the old rates.odd_rounded) as the one signed read in the act, with its carries; strike "one carry".
4. BLOCKING (condition 3; ONE_ALGEBRA Answer R "YES", section "The root dial", Measured 10, the table row). What is
   shown is that any 4-vector's symmetric square v v^T has 00 = v_0^2: Re(Phi conj e_mu) is the component itself (300
   of 300, probe_rd5_quat.txt A); the Hamilton product enters the dial nowhere. W = N(Phi) for the pure-time frame
   alone (0 of 300 frames with a space leg). The reading needs ALL ten slots to be the frame's square; the proposal
   roots the 00 slot alone and leaves the ii slots (grips) linear: its own lay on the derivers' board, diag(81, 6, 6,
   6), has 6 of 36 minors not 0, rank 4, no frame's square (probe_rd5 B). ONE_ALGEBRA says the rest itself: the act
   keeps no square (27 -> 0), the step is no unit on a moving clock, the frame train is OPEN. Condition 3 is met only
   with the frame train (4 gears, the ten slots read): a law change of the metric family, the owner's. Fix: "yes, with
   the frame train" in place of "YES"; the row moves from Answer to Open.
5. MINOR (ROOT.md section 2 row 3, EDGE2 section 3, probe_root C). "The books per gear P_(t+1) - P_t = 4 q_F, 0
   misses" is an identity: N = P_t + 4 q_F = P_(t+1) by definition (D4). It tests the code. Say so; measure the row's
   SUM (item 1) instead.
6. MINOR (ROOT.md section 2, "the 24, the run back ... yes"). The run back is DERIVED here (D2, three lines) under the
   hypothesis that the clock row's own dial stands (the cut), which makes the provisional split at 2 D_in the final
   one for the 00 row, so L(a + q1') = L(b). Measured (probe_rd3 C): 0 gears of the 00 row with q1 != q at every
   round, against 29 to 184 of 324 on the other rows. When the 00 row gets its own law (OPEN, not mine) the run back
   must be re-derived. Name the dependence.
7. MINOR (EDGE2 section 3; ROOT.md "the clocks' read into L"). L at or below 0 (probe_rd2_onegear.txt B, probe_rd3 D):
   the root dial's state admits L < 0 with W = L^2 > 0 (a negative lapse the W dial cannot hold); D_in = 0 is a dial
   0 (ZeroDivisionError in the act, no if to stop it); a standing L = -2 on the board runs 5 rounds and does not
   rewind; the derivers' promise_root divides at L(now) before checking L >= 1 and itself raises at L = 0. The 00
   slot's unit changes (D7): the law's c = 2 L_rest c00 + c00^2, one count of c00 = 2 L_rest + 1 teeth (13 at L_rest
   6; 603,312,000,001 at the calibre) while one count of c_ii stays one grip count: the metric's ten rows no longer
   share a unit (00 in root counts, ii in teeth); the loader's geared, the lays and the record's units change; the
   domain is c00 > -L_rest, not c > -rest. Fix: state the unit change and the domain as prices.
8. MINOR (ROOT.md section 2 row 2, "the kick T_k q_d enters the push and is divided at the root with it"). A whole
   quantum of the drive moves nothing unless T_k |q_d| >= L/2: at L = 9, T_k = 2, 4 of 10 kicks q_d in [-5, 5] drop
   wholly; at L = 73 and at the calibre's L_rest ~ 3e11, 10 of 10 (probe_rd1 C). The click's path through the push is
   cut unless T_k scales with L. For the physicist and G5.
9. MINOR (EDGE2 section 3 / probe_root.py against ROOT.md / probe_root_generic.py). Two definitions of the push's
   quotient: EDGE2's probe uses edge_lib.split (ties to the EVEN quotient, two carries and lit(), the mirror -s: the
   tie-even convention the owner did not choose); ROOT.md uses (iv)'s odd rounding (half away from zero). They differ
   at 370 of 720 ties, L in [1, 40], F in [-200, 200] (probe_rd6_defs.txt); both are odd under negation. EDGE2's
   one-gear numbers (1000 to 1008 permille; 0 misses of 30,000) are tie-even's. Redone with (iv) and -1 - s (probe_rd2
   C): v^2 W 1000, 1000, 1000, 1000, 1005 permille over L 100 -> 200; the run back 0 misses of 2000 on standing,
   rising, falling, drawn L in [5, 200], alternating 1/1000 and L = 1 courses, with a hairspring and with a crooked
   push. Name one rounding: (iv).
10. MINOR (condition 2 wording; ROOT.md section 2 row 2, EDGE2 section 1). "One dial law for every carry" is one
    MIRROR law ((iii), r -> m - 1 - r), not one dial: the gear's tooth on the moving edge dial 2 (L(b) + L(a)), the
    drive's on the standing T_d, the push's remainder on no dial. Say "one law of the mirror".
11. MINOR (ONE_ALGEBRA "The root dial", DERIVED paragraph). "Dividing the push by L at the pivot and by L again at the
    dial is ... exactly what the act as built does in one carry at W" holds on a standing clock alone (q ~ v + F/L^2);
    on a moving clock the two differ by the redshift D_in / D_out, the whole point of the dial.

## Sound, with numbers

- D1: the half-open split is odd with the tooth -1 - s at every parity of D (the dial 2D is even by construction).
- D2: the run back exact under the cut, derived in three lines; measured by the derivers 40 of 40 on four lays, 4 of 4
  with J through the tables (reruns byte-identical); here 0 misses of 2000 on six one-gear courses; the within-round
  map injective (0 collisions of 1464 valid states at D_in = 12, D_out = 9).
- D5: the 24 with the odd rounding, 24 of 24 at every round on every lay and at standing L = 8 to 24 (the turns are
  signed permutations on every lawful train: the square's block 24 of 24 checked; E alone is refused by the loader,
  SYM24).
- The kept push tooth: runs back within the round (the drive's lemma, derived here) and fails across rounds on a
  falling clock (their 2 of 40, 446 teeth outside the dial): the derivers' reason is right.
- Nature's test: sqrt(W) v kept within 5 permille (here), 8 (theirs) over W x 4; A/A0 999 to 1000.
- The dropped force 1 to 6 permille at L 9 to 73 (theirs, reproduced); the drop <= L div 2 (probe_rd1 D).
- DERIVED: D1-D5, D7 (02_derivations.md). MEASURED: everything the derivers list, reproduced byte for byte.
  OVERCLAIMED: "one carry"; "books 0 misses" as evidence; "both conditions hold"; "natural in the quaternion: YES";
  "nothing typed once the file holds k"; "one dial law"; EDGE2 section 3's root numbers as the proposal's (they are
  tie-even's).

## Solution24

Step 3 (nothing typed; a form CHOSEN with its reason and window) and step 6 (the books of the board, not of the gear)
were not closed by the derivers' own hostile pass: a price list must name every law sentence the change touches
(K-S3, line 100's parity and typed-condition sentences, (ii)) and every exact book it loosens.
