# Findings on the root dial (hostile mathematician), 2026-10-30

Probes in this folder (whole numbers, carry the one division): probe_rd1_rounding, probe_rd2_onegear, probe_rd3_board
(relies on the FROZEN rootdial_read/edge/edge_lib.py and probe_root_generic.py), probe_rd4_den, probe_rd5_quat
(relies on the frozen q_lib.py), probe_rd6_defs; each with its .txt. Reruns of the derivers' probes in rerun/.

## Verdict: NOT PASSED as "all three conditions met". Met with prices that are law changes, one of them against a
## law sentence, and condition 3 stands on an OPEN item.

## BLOCKING

B1. Condition 1, "Rule3 the one division": the push's division at L(now) DROPS its remainder. Rule3's carry keeps it
    ("q leaves, r' stays", carry.py; line 100: "a division outside Rule3's carry is a hidden remainder"). ROOT.md
    itself: "(ii) covers it only read as the lapse's coefficient" and "the dropped remainder does not follow from (ii)
    without a clause". So condition 1 holds only by a new clause of (ii). Its measurable cost (probe_rd3 B): the
    row's total momentum SUM_sites P, exact to the bit under the built act and the edge (SUM F = 0 enters unrounded:
    drift 0 over 40 rounds), drifts under the root dial at 40 of 40 rounds on a uniform standing clock (L = 9: rows
    drift by -60 to +44 teeth of P over 40 rounds, one-round drift up to 16 = 4 x 4 q_F units), because
    SUM odd(F_i / L) != 0 when SUM F_i = 0. An exact conservation of the board is lost (Solution24 step 6: "the carry
    keeps its sum exactly"). Immaterial in size at the calibre (the drop <= L/2 ~ 1.5e11 against pushes ~ 1.5e22), but
    exactness is the project's standard, and the text does not name this loss (it names only "the dropped force").
    Fix: write the clause into (ii) and the loss of the row's exact book into the proposal's price list; or round the
    push per Mesh end at a dial common to both ends (keeps SUM = 0 on a uniform clock); or keep the W dial.

B2. Condition 1, "nothing declared", line 100 "no condition is typed on the integers": L_rest whole needs 6 den a
    square, i.e. den = 6 k^2 (6 squarefree), or a new file key k. That is a typed condition on den that no symmetry
    gives, and it puts the prime 3 (= 3 mod 4) into den against K-S3 (line 110): "den is chosen by its structure, the
    primes 1 mod 4 and their powers". None of the law's dens runs the root dial (probe_rd4 A): the example's
    15162856759112389 (6 den = 2 mod 4), the hand's 3311818282 and the cheap 697786 (6 den = 6 mod 9). With den =
    6 k^2 every lift (num, s) on den's circle is 6 times a lift of k^2 (probe_rd4 B, k <= 30: every lift divisible
    by 6; k without a prime 1 mod 4 has no lift at all, 20 of 30): the gears' pairs all carry a dead factor 6 and the
    rates' group law runs at den' = k^2. Fix: either the owner's word on a new K-S3 (den = 6 k^2, k with a prime 1 mod
    4, two lifts), or a teeth law whose rest is a square by construction (e.g. the Spokes' count outside the root:
    W = 6 L'^2 is not a square either; nothing cheap), or no root dial.

B3. Condition 1, "one carry", and line 100 "a rule that holds at one parity only is not a rule of the law": the
    push's quotient by ONE carry (half up, (ii)'s words) is odd under F -> -F iff L is odd (probe_rd1 A: misses 148 of
    1452 all at even L, 0 at odd L; DERIVED D3). L = 6 k Gamma + c00 is even at rest and has c00's parity. On the
    board (probe_rd3 A) the 24 fall to 3 at standing L = 8, 12, 16, 20, 24 and hold at 9, 10, 11, 14, 18: on that
    board the push is 6 m and the tie 12 m = L mod 2L needs 4 | L; with the kick or moving grips every even L has its
    tie. The cure, the odd rounding (iv), is 5 carries in ROOT.md (3 suffice: probe_rd1 B, 0 differences of 16040)
    and needs the SIGN of a state quantity in the Node-clock every round; src has the sign test and lit() at the
    load alone (load.tables, load.first), the act one carry per gear. "The push divided once at L(now) by a carry"
    is overclaimed: it is a signed rounding, a new primitive of the Node-clock. Fix: say so; name the primitive (the
    law's odd rounding, rates.odd_rounded of the old engine) as the one place a sign is read in the act, and its cost.

B4. Condition 3, "natural in the quaternion": what is shown is that any 4-vector's symmetric square v v^T has
    00 = v_0^2 (probe_rd5 A: Re(Phi conj e_mu) is the component itself, 300 of 300; the Hamilton product reads off
    entries and enters the dial nowhere); W = N(Phi) only for the pure-time frame (0 of 300 drawn frames with a space
    leg). The reading needs ALL ten slots to be the frame's square; the proposal roots the 00 slot alone and leaves the
    ii slots (grips) linear: the proposal's own lay, diag(81, 6, 6, 6) on the derivers' board, has 6 of 36 minors not 0
    (rank 4), no frame's square (probe_rd5 B). The derivers say it themselves: the act keeps no square (27 -> 0), the
    frame train is OPEN, the step is no unit on a moving clock. So condition 3 is met only if the frame train (4
    gears, the ten slots read) is adopted: a law change of the metric family, OPEN by ONE_ALGEBRA's own word. "YES"
    is overclaimed; "yes, with the frame train" is the honest line.

## MINOR

M1. ROOT.md and EDGE2: "the books per gear P_(t+1) - P_t = 4 q_F, 0 misses" is an identity (D4): N = P_t + 4 q_F
    = P_(t+1) by definition. It tests the code, not the physics. Say "an identity" and measure the row's SUM instead.

M2. The run back's exactness is DERIVED (D2) under the hypothesis that the clock row's own dial stands (the cut), which
    makes the provisional split at 2 D_in the final one for the 00 row (probe_rd3 C: 0 gears of the 00 row with
    q1 != q, against 29 to 184 of 324 on the other rows at every round). When the 00 row gets its own law (OPEN, not
    mine), L(a + q1') = L(b) is no longer given and the run back must be re-derived. The genericity claim stands on
    the cut; name the dependence.

M3. L at or below 0 (probe_rd2 B, probe_rd3 D): the root dial's state admits a negative L with W = L^2 > 0 (a
    negative lapse the W dial cannot hold); D_in = 0 is a dial 0 (ZeroDivisionError in the act, no if to stop it);
    a standing L = -2 on the board runs 5 rounds and does not rewind (rewound False); the derivers' own promise_root
    divides at L(now) before it checks L >= 1 and raises at L = 0. The domain is c00 > -L_rest (about -3e11 at the
    calibre), the W dial's c > -rest (about -1e23): the 00 slot's unit has changed (D7): one count of c00 is
    2 L_rest + 1 teeth (13 at L_rest = 6; 603,312,000,001 at the calibre), while one count of c_ii stays one grip
    count: the metric's ten rows no longer share a unit (00 in root counts, ii in teeth). The loader's geared, the
    lays and the record's units all change. Fix: state the unit change and the domain as the proposal's price.

M4. The drive's kick T_k q_d is divided at L with the force (ROOT.md): a whole quantum of the drive moves nothing
    unless T_k |q_d| >= L/2 (probe_rd1 C: at L = 9, T_k = 2, 4 of 10 kicks q_d in [-5, 5] drop wholly; at L = 73 and at
    the calibre's L_rest ~ 3e11, 10 of 10). The click's path through the push is cut unless T_k scales with L. For the
    physicist and the click law (G5); name it.

M5. Two definitions of the push's quotient in the two frozen texts (probe_rd6): EDGE2 section 3 / probe_root.py use
    edge_lib.split (ties to the EVEN quotient, 2 carries + lit(), the mirror -s, the tie-even convention the owner did
    not choose); ROOT.md / probe_root_generic.py use (iv)'s odd rounding (half away from zero). They differ at half
    the ties (F/L = k + 1/2, k odd); both are odd under negation. EDGE2's one-gear numbers (1000 to 1008 permille,
    0 misses of 30000) are tie-even's; redone with (iv) and -1 - s (probe_rd2 C): v^2 W 1000, 1000, 1000, 1000, 1005
    permille, the run back 0 misses of 2000 on standing, rising, falling, drawn [5, 200], alternating 1/1000 and L = 1
    courses. The proposal should name ONE rounding: (iv).

M6. "One dial law for every row, the drive and click teeth included" is one MIRROR law ((iii), r -> m - 1 - r), not
    one dial: the gear's tooth on the moving edge dial 2 (L(b) + L(a)), the drive's on the standing T_d, the push's
    remainder on no dial (dropped). Three treatments of three remainders. Wording; say "one law of the mirror".

M7. ONE_ALGEBRA's "dividing the push by L at the pivot and by L again at the dial is dividing by L conj(L) = N(L) = W
    ... exactly what the act as built does in one carry at W" holds on a standing clock alone (q ~ v + F/L^2); on a
    moving clock the two differ by the whole physics (the redshift D_in / D_out), which is the point of the dial.

## SOUND (DERIVED on paper here, MEASURED by the derivers and reproduced)

- The half-open split is odd with the tooth -1 - s at every parity of D (D1): the dial 2D is even by construction.
- The run back is exact under the cut (D2): three lines; measured 40 of 40 on four lays, 4 of 4 with J through the
  tables (their reruns byte-identical), 0 misses of 2000 on six one-gear courses here, the within-round map injective
  (0 collisions of 1464 valid states at D_in = 12, D_out = 9).
- The 24 hold with the odd rounding (D5): 24 of 24 at every round on every lay, standing L = 8 to 24 (probe_rd3 A).
- The kept push tooth: runs back within the round (the drive's lemma, derived) and fails across rounds on a falling
  clock (2 of 40, 446 teeth outside their dial): the derivers' reason is right.
- Nature's test: sqrt(W) v kept within 5 permille over L 100 -> 200 (here), 8 (theirs); A/A0 999 to 1000.
- The three frozen probes rerun byte-identical (rerun/).
- The dropped force 1 to 6 permille at L 9 to 73 (their numbers, reproduced); the drop <= L div 2 (probe_rd1 D).
- E has no whole basis and the loader refuses it alone (SYM24): the per-row roundings' covariance rests on that rule,
  as the carry's does; the square's block is a signed permutation on 24 of 24 (checked).
