# The hostile mathematician on ONE_ALGEBRA (the act on whole quaternions and the double Node-clock)

The report as the reader gave it, 2026-10-30, filed by the Boss. Files beside it: 00_plan.md, 01_reading_notes.md,
02_findings.md, qa_lib.py (the harness), qa2_units.py, qa3_wall.py, qa4_double.py, qa5_train24.py, qa6_misc.py with
their .txt; worlds/spin4 and worlds/spin8 (world files for a 4- and an 8-gear A1 hand, so no train is declared in
code); rerun/ (the text's nine probes rerun). Everything rebuilt in whole numbers with Rule3's carry as the one
division.

VERDICT on ONE_ALGEBRA: NOT PASSED

The algebra the text states is right wherever I recomputed it, and its central theorem is correctly proved for what it
assumes. What is wrong is what the text makes of it: the "iff gcd(W, 6) = 1" and the "wall at the load's teeth" hold
only for a carry whose remainder set is one fundamental domain for every quotient, and the text asserts that this
assumption "is what makes the act bijective and the run back a mirror". It is not. A carry whose remainder set depends
on the quotient, the kind the project's own edge draft already uses in rank 1, is bijective, runs back by the mirror
and turns with every lift at every W, measured on the act at W = 2, 3, 6 and 9.

## Items

1. BLOCKING. Finding 1: Answer 1 (lines 54-75), the theorem (237-299), the Clock layer's third bullet (158-163), the
   Board's second (448-452), the Clicks' second (464-467), the table's fourth row (546), "Open". Claim: "a carry on the
   hand that turns with the lifts exists iff gcd(W, 6) = 1"; "r in a set D of coset representatives ... that is what
   makes the act bijective and the run back a mirror".
   - Measurement (qa3_wall.txt). (i) Inside its framework the theorem is right: fixed nonzero cosets of H/WH by my own
     brute force at W = 1..13 and Smith form at 25, 35, 49, 77, 1001, 1003, 14, 15, 27, 1002; of Lambda/W Lambda by
     brute force at W = 2, 3 and Smith at 5..13, 25, 1001, 1002: exactly where 2 or 3 divides W; indices |det(g-1)|
     16, 9, 4, 1 on H and 256, 81, 16, 1, 4 on Lambda; the orbit domain at W = 5, 7 (625 and 2401 representatives,
     invariant, D = -D, 26 and 100 free orbits), conflicts 97 and 64 at W = 6, 9. (ii) Outside it: let g u be the least
     of the 24 images of the dividend u (a unit g != 1 fixes no nonzero point of H, so g is unique) and
     Q(u) = conj(g) [centred box quotient of g u]. Then Q(g u) = g Q(u) (0 misses of 1440 at each of W = 2, 3, 5, 6, 7,
     9), Q(-u) = -Q(u) (0 of 60), and the remainder r = u - W Q(u) has 4 N(r) at most 12, 12, 56, 116, 116, 224 over
     the whole cell of the quotient 0 against 4 N(W) = 16, 36, 100, 144, 196, 324: a division with the remainder below
     the divisor's norm. Its remainder set is no fundamental domain: the cell of the quotient 0 holds 73 dividends at
     W = 2 against 16, and exactly the 15 cosets the theorem calls fixed by -1 carry two or more remainders there (168
     of 625 at W = 5, 1768 of 6561 at W = 9); the quotient decides which serves. With a state valid iff
     Q(W (a - b) + r) = a - b (the tooth is its own remainder, as the edge's |s| = D only at an even velocity), the
     state map (a, b, r) -> (a + q, a, r') is a bijection on valid states and (b, a, -r) inverts it: DERIVED in three
     lines (a = b+; m = Q(u - push(a)); r = u - push(a) - W m), and MEASURED on the act (worlds/spin4, a lone
     Node-clock, J = -2 psi through the engine's pushes, s = T_k = T_d = 1): turned run == run turned over 6 rounds for
     the 24 lifts x 20 drawn valid starts, 480 of 480 at W = 2, 3, 5, 6, 7, 9 alike, the tooth moving in 18 to 20 of 20
     runs, the run back exact 20 of 20; the act as built on the same slots 40 of 480 (53 at W = 2). On Lambda under the
     48 (worlds/spin8): 240 of 240 lifts x starts and the run back 5 of 5 at W = 2 and 9; Q equivariant and odd on
     Lambda at W = 2, 3, 6, 9 (0 misses of 576 each). (iii) The project's own edge form is of this kind:
     edge_lib.split at the dial 2D has cells of sizes 2D - 1 and 2D + 1 by the parity of q (D = 3: sizes 3, 5, 7 among
     the quotients -4..4; D = 4: 4, 7, 9), and the class D mod 2D, fixed by -1, carries both remainders -D and D. The
     hypothesis the theorem needs excludes the Boss's own draft of the tooth.
   - What stands: no fundamental domain (one dial of W^4 or W^8 teeth, the same at every velocity) turns with the
     lifts where 2 or 3 divides W; no per-gear carry in any basis (fam_math); H^1 = 0 inside that framework. What
     falls: "iff"; "that is what makes the act bijective"; "at such W the hand's teeth cannot be kept in any dial that
     turns"; "no domain exists" read as "no carry"; the Clicks' trilemma (teeth coprime to 6, or a formula for the
     orbit domain, or no per-teeth carry), which omits the fourth way the edge draft already takes. Condition (c), free
     of table and comparison, stays OPEN at every W (the canonical rule compares 24 images; the orbit domain is a
     table).
   - Fix: open the theorem with its hypothesis ("the remainder set the same for every quotient: the cells translates
     of one tile") and carry it into Answer 1, the Clock, Board and Clicks layers and the table; strike "that is what
     makes the act bijective"; add the quotient-dependent carries with their numbers and name them the edge's kind;
     restate the wall as a wall for fixed dials, with the open item at every W being a rule free of a table or a
     comparison.

2. MINOR (a false reason). Answer 0's second paragraph (lines 52-53), the double Node-clock section (413-416),
   probe_double.py's last line, NOTES: "the group ring escapes the gcd(W, 6) wall (it has fixed vectors, the orbit
   sums, where the division algebra has none)".
   - Measurement (qa5_train24.txt): L(-1) = -I and R(-1) = -I on the 24-gear train, so a common fixed vector is 0 and
     SUM_g L(g) is the zero matrix: no fixed vectors, every orbit sum vanishes. |det(L(g) - I)| = 256 for the order-6
     lifts (16777216, 0, 4096, 64 for orders 2, 3, 4, 8): g - 1 is no unit on the train, so the text's H^1 argument
     does not run there; the flip twist c_g = (W - 1)[negated rows] is a cocycle (0 misses of 576 pairs) and a
     coboundary iff W is odd (48 a = -192 at W = 9, whole; -216 at W = 10, not). The train rides the per-gear carry
     because every L(g), R(g) is a signed permutation and the box with the flip is every signed permutation's
     invariant domain (the carry's lemma).
   - Fix: replace the parenthesis by that reason.

3. MINOR (scope). The double Node-clock, MEASURED paragraph (lines 399-402), probe_double's conclusion: "the slot
   quaternion's unit step is the lone clock's or the uniform hand's".
   - Measurement (qa4_double.txt), the example universe on the act as built: a cube of side 3 with the light hand an
     eigen-hand of the pull (patterns (2, -1, -1) and (0, 1, -1) along x with drawn amplitudes, uniform in y, z:
     F = -3 grip v, not 0) and the spring tuned to k = 2 W - 3 grip = 3 W / 2: q+ = q j at all 27 sites for 12 rounds,
     N(q) kept, the teeth still; the same hand at k = 2 W fails at once. Even boards of sides 2 and 4, the checkerboard
     hand (-1)^(x+y+z), NO spring: q+ = q j at every site for 12 rounds.
   - Fix: "the step is q j wherever the round's push is -2 W now: for an eigen-hand of the pull with eigenvalue
     -lambda, k + s lambda grip = 2 W; the lone clock and the uniform hand are lambda = 0, the checkerboard on an even
     board lambda = 12 with no spring".

4. MINOR (weight). Answer 0 (lines 24-45), the table's row 11: "the double Node-clock IS Hamilton's quaternion of the
   slots"; "the forward-backward difference is the j slot of q (1 - j), the velocity".
   - Measurement (qa4_double.txt): the phase (re, im) -> (-im, re) with the flip commutes with the act as built 12 of
     12 rounds at k = W, 2 W and 3 W alike; (i q i^-1) j is the slot swap and q (1 - j) has the slots now + before and
     before - now at every mode: identities of the reading, not of the act. Only two things are the quarter mode's:
     the step is right multiplication by j and N(q) is kept. And at every exact mode (W | k with a spring alone, or the
     tuned eigen-hands of item 3) the dividend is -W (now + before) + r, the quotient exact, the tooth still: the carry
     is inert wherever the quaternion reading holds, so the reading touches none of the act's one non-trivial
     operation. A strengthening of "at no other mode": for t = +-1 the step is a unit quaternion's right
     multiplication in NO whole basis of the two slots (the Q(i)-rational S_t-invariant Hermitian form is
     c [[1, -t/2], [-t/2, 1]], Gram determinant 3 c^2 / 4, never 1; 0 of 1184 small GL_2(Z[i]) bases, against 32 at
     t = 0). The j slot of q (1 - j) is before - now, the velocity negated (the body says so, the Answer does not).
   - Fix: call the slot quaternion a reading (as the text does for pi), list what is mode-dependent, carry the
     strengthening, fix the sign.

5. MINOR (hygiene). probe_double.py does not run against the edge_lib.py beside it.
   - Measurement (rerun/): eight probes rerun byte-identical; probe_double.py exits 1 with TypeError: turned_edge()
     missing 'wd' (edge/edge_lib.py was rewritten at 16:33:19, four minutes after probe_double.txt). With the one
     argument added (rerun/probe_double_fixed.py passes layout.gearing.drive) the output is byte-identical to the
     stored one, so the numbers stand.
   - Fix: patch the call, rerun, re-save, and note the edge_lib revision the probe reads.

6. MINOR (non-invariant numbers). The metric section (lines 323-333), probe_square: "determinant -48", "minor -16",
   "determinant -128".
   - Measurement (qa6_misc.txt): the ten forms' determinant is -48 with Im(h h) written 2 a v and -6 with a v; the
     invariant content is rank 5 (Smith diagonal [1,1,1,1,1,1,2,2,2,6]) and that E, T2 lie outside. The -128 is an
     index: Smith diagonal [1,1,1,1,2,2,2,2,2,4], so the inverse needs denominators dividing 4 ("halves and quarters"
     is right).
   - Fix: state ranks and Smith diagonals.

7. MINOR (wording). "(a) a bijective division with remainder" (line 56; fam_math's "a bijection (n, r) <-> (q, r')"):
   the map (n, r) -> (q, r') is |D| to 1, the bijection is the state map. "A determinant W'/W" (316-321) names the
   scale of a non-linear map; W p' = W' (p + push + r - r+) is the carry's definition rearranged (0 misses with W rising
   60 -> 66, qa6). The theorem's (i) assumes the tooth turns by a map of the tooth alone and the quotient linearly; say
   so.

## Sound, with numbers (DERIVED where it follows on paper, MEASURED where it is a count)

- Finding 2 (DERIVED, trivially): every operation of the round is a sum, a whole scalar times a row, or a carry by a W
  the load lays alike on a train's rows, so reading rows as a quaternion changes nothing; the probe's tick_Q is a
  re-implementation of the same arithmetic (18 of 18 on rerun), a consistency check rather than an independent test.
  The tables are Hamilton's product exactly (MEASURED entry by entry, qa2_units.txt): C[T1 T1 -> A1] = delta,
  C[T1 T1 -> T1] = the Levi-Civita symbol with eps[0,1,2] = +1, the A1 channels 1, e_a e_b = -delta_ab + SUM eps e_x on
  9 of 9 pairs; the -> E and -> T2 channels (6 entries each) outside the product.
- Finding 3 (DERIVED and MEASURED from the quaternion side, qa2): the 24 Hurwitz units and the 24 Lipschitz
  quaternions of norm 2 give exactly the engine's 24 turns, two to a turn (g, -g), every sandwich / N(g) whole,
  determinant 1; N(g) = 1 iff A2 = +1 on 24 of 24; 1 + 3 + 8 Hurwitz, 6 + 6 of norm 2; parity then the turn 0 misses
  of 72.
- Finding 1 inside its framework (DERIVED, each step checked on paper; MEASURED as in item 1 (i)): the cocycle
  argument, H^1 = 0 by the order-6 unit (N(g - 1) = 2 - tr g = 1), the fixed-coset criterion and the indices
  N(g-1)^2 and Nm(N(g-1))^2.
- Finding 5 (DERIVED; qa6): S_t keeps v^2 - t v u + u^2 at every whole t, orders 6, 4, 3 at t = 1, 0, -1 and none at
  2, -2, 3, one ring per mode; O_48's double farthest point recomputed in halves, 16 Nm N(r) = 256 against 256 by
  "nearest in each part" and 128 by another quotient; Hurwitz's two quotients at n = 1, W = 2 (4 N(r) = 4 and 12, both
  below 16); the covering radii are the literature's, as the text says.
- The units as gears (MEASURED, qa5): SUM tr(L)^2 = 1152, SUM tr(L L) = -384, both sides signed permutations, pi of
  rank 8 (det pi pi^T = 104976) onto O_48 since every basis element is a unit, kernel rank 16, the carry not
  descending (the text's 100 of 100, rerun).
- The lone clock (MEASURED, qa4): at k = 2 W, q+ = q j, N(q) and the wind kept, teeth still; at k = W, 3 W the wind
  kept and N(q) not; at k = 2 W + 2 the teeth move within 6 rounds; W (a+ - 2a + b) = push + r - r+ at 0 misses.
- Reruns: eight of nine probes byte-identical; the ninth after item 5's one-line patch.

## Solution24 (one line)

Step 3 was not met and step 9 did not catch it: the theorem's hypothesis ("one dial for every count of the velocity")
is a declaration the deriver's own check never listed, though the Boss's own edge draft already breaks it; a
derivation should open with its hypotheses and read them against the project's other drafts before it names a wall.
