# The hostile mathematician (THIRD pair) on THIRD8, 2026-10-31

(Written by the Boss from the reader's hand-back at 08:1x UTC, the reader's harness refusing the write; the text is
the reader's, word for word.)

(The harness refuses report files from subagents, as it did for THIRD7, so here is the whole report for the Boss to write into S/third8_math/REPORT.md. ASCII only.)

**What I read**
- THIRD8.md whole: 669 lines; sha256 712acaeb37e3fbd8..., and all 28 sums in FROZEN.sha256 check OK.
- My THIRD7 report as the Boss wrote it, and the physicist's THIRD7 report with the Boss's 07:3x answers.
- MATH1's physicist (B1 to B3), ALG1 section 4.3 with its twinD outputs, and the schema of node-all's 1.4 record (nodeall_h).
- The brief's last three sections (364 lines).

**How I ran** (all in S/third8_math/; whole numbers, the carry the one division, python -I under nice 19, one process at a time, the load under 8 at every start):
- Reruns from copy/ (a copy of the frozen folder):
  - arith8.py, dec8.py and per8.py are byte-identical to arith8.txt, dec8_200.txt and per8.txt.
- My own probes:
  - mine8.py (mine8.txt): the round's fixed points, the twin's unread third, and exact per-period counts.
  - twin8.py (twin8_20000.txt): the twin held on the dial D at the file's key, with its run back.
  - mine8_board.py (mine8_board_200.txt): my own writing of the member on the board, recounting the batch's numbers.

**VERDICT on THIRD8: NOT PASSED.** One BLOCKING item, in section 4 and the batch's item 1, with a few lines to fix. Everything I pressed on otherwise holds, and is re-measured.

## BLOCKING

**B1. The twin needs only the dial D. The batch's item 1 states its cost on G D, and section 4 misreads the 3-to-1.**
- Where: section 4, "60 shares the factor 3 with the dial, so three pairs share each (u(t), u(t+1)): the residue mod 3 is kept apart ((f))"; section 2 item 2; section 13 item 1, "Each a count on the triangle's dial G D".

**Derivation.**
- Every shear that moves tau adds G eta mod G D, and that reads eta only mod D.
- eta += G tau descends to D.
- The birth (G D - 1)/2 is congruent to (D - 1)/2 mod D.
- The flip descends to D.
- So (tau mod G D, eta mod D) is closed and fixes every landing.
- The kernel of (tau, eta) -> (u(t), u(t+1)) is {(0, 0), (0, D), (0, 2D)}: an eta shifted by D.
- D = 0 mod 3, so the three pairs sharing (u(t), u(t+1)) have the same residue mod 3. What they differ in is a conserved Z/3 that no landing reads, not "the residue mod 3".

**MEASURED at the file's key.**
- mine8 B, 20,000 rounds at (20, 30, 25) m from the stand-in:
  - eta and eta + D give landings 0 rounds apart;
  - both ends have eta mod 3 = 0 and 0;
  - the ends still differ by exactly D;
  - the twin held on D lands 0 rounds apart from the full pair.
- twin8, 20,000 rounds of a walk with y in [-30 m, 30 m), from the birth and from the stand-in:
  - landings 1,978 and 2,066, the same for both forms, 0 rounds apart;
  - the run back from the end alone (the same round on the mirrored pair, the twin flipped on its own dial, the passings negated and reversed) reaches the start, with the landings negated and reversed, for both forms from both lays.
- This agrees with ALG1 4.3, which measured toy dials only (3D = 15, 63, 255, with the run back on 63 and 255). Mine is on the file's dial.

**The coordinator's question: is 3D needed, or D for the twin and 3D only for the edges?**
- 3D = 9K is needed for tau. It carries y at G D, and each landing books c_e w on edges whose quanta are D of passing. At D the edges would book y (G - 1)/(G D) too many.
- 3D = 9K is needed for the triangle's three edges. Their share G x_e - c_e y is whole only at G times the passing; carried at D it books G quanta per quantum (THIRD7 section 5, forced).
- The dial D suffices for the twin.
- So items 1 and 2 are consistent once item 1 holds the twin on D. Item 2 stands as written.

**Fix.**
- Section 13 item 1 should read:
  - tau, a count on G D = 457,302,861, born 228,651,430;
  - the twin, a count on D = 152,434,287, born (D - 1) div 2 = 76,217,143;
  - still 2 entries per Node-clock and 54 in all, but 3D x D states per triangle instead of (3D)^2, log2(3) bits fewer.
- Section 4: the three pairs differ by eta + D, a never-read Z/3. With the twin on D, the map to (u(t), u(t+1)) is one-to-one onto the reachable pairs, so "the landing coordinate's now and before" becomes exact.
- The change of the twin's dial goes to the owner (Sofer's rule), as the coordinator says, with ALG1 4.3 and these two measurements.

## MINOR

1. **The period** (section 2 item 1.3; section 6 "The period"; section 13 item 6).
   - "The period is N when 3 divides y, and 3N otherwise" derives the round's order. Every orbit's period divides it, and some lays sit on shorter orbits.
   - mine8 A: at 3 | y the round has 9 fixed points on the dial, at both (20, 30, 25) and (9, 9, 12) m. Each returns after one round. At (20, 30, 25) m one of them lands every round.
   - From the birth and the stand-in the period is the full order. per8 reruns byte-identical: 1,585,440 at (2, 3, 2) m from both lays, 528,480 at the other two rows.
   - Fix: say "the round's order is N or 3N; the birth's and the stand-in's orbits reach it". Name the fixed points beside item 7's drift.
2. **The "per period" z^2 are z^2 / 1.892, not counts per period.** Counted over exactly one period (cyclic, mine8 C):

   | passings | lay | after two a third | derived | exact z^2 | THIRD8's z^2 / 1.892 |
   |---|---|---|---|---|---|
   | (20, 30, 25) m | birth | 374 of 5,298 | 418 | 5.1 | 5.8 |
   | (20, 30, 25) m | stand-in | 354 of 4,797 | 378 | 1.75 | 1.6 |
   | (40, 40, 45) m | birth | 13,578 of 47,082 | 13,629 | 0.27 | 0.20 |
   | (40, 40, 45) m | stand-in | 14,067 of 48,140 | 13,935 | 1.75 | 2.2 |

   - The claims stand: 2.25 and 1.3 SE below the derived value at a = 0.1, within 1.5 SE at a = 0.3.
   - Fix: give the exact counts, or call the figures approximations.
3. **The exact value's margin** (section 6, "a whole number of dials in (18 (y - 1), 20 (y - 1)]").
   - floor(38a)/(38a) holds at every u0 by margins of 242 units at a = 0.1 and 686 at a = 0.3, on a dial of 457,302,861. The passings are whole m = D div 50, just below 0.1 and 0.3.
   - At a = 0.1, y only 13 units larger lets a partial lift appear, and the value then moves with u0.
   - Fix: name the margin, and say the value is exact at these passings.
4. **dec8 R4 is a code check.**
   - c . (G D q + k_after - k_before) = G (G D) w is an identity of the carry with c . p = 0, so it is DERIVED, and the 200 of 200 can fail only by a code bug, like the per-edge books.
   - The condition "the record writes the edges' teeth" is met by node-all's 1.4 form: wherever a side at the Node-clock carried, every side of a clock is written, q 0 included, with both teeth. In the other rounds w = 0, since |c . Q| <= 2.
   - When the third click is built, 1.4's sentence "x = K q_tu + k_after - k_before is the side's passing" reads p_e + G D c_e w on a triangle's edge, not its passing. Name this with question 11.
5. **Letters.** K is the key in sections 4 and 13 (D = 3K, G D = 9K, K = 2 middle + 1) and the coupling in section 3 (the palindrome "at K = G"), and David's K is his edge dial. Align them (the physicist's d2).
6. **Section 13 item 2, "4,644 of the lines differ".** These are (round, Node-clock, train) places where the two forms' values differ; my recount gives 4,644. The symmetric difference of line entries is 8,856. Say "places".

## My THIRD7 items, folded

- **B1: met** (sections 0, 2 and 6; arith8 items 4, 6, 7 and 9, rerun byte-identical).
  - The constant is 18 (y + 1) on the dial and 18 y centred. The frames read 0 at the round's start, +18 y before the carry and -18 y after it (centred), matching the Boss's ruling. I re-derived each: (H2 H1 - 37 I) H2 v = (0, 6y); (L - I) v = (18y, 6y); (L - 37 I) v = (-18y, 6y).
  - floor(38a)/(38a) is 789, 964 and 986 per mille.
  - I hand-checked the derived counts 792, 716, 25,780, 26,358, 499 and 503, and the z^2 over the run, 10.9, 3.1, 0.37, 4.2, 0.10 and 0.00.
  - The widening sentence is struck, and the deficit is named the orbit's.
- **B2: met as the round's order** (S = D I; per8). The wording is MINOR 1 above.
- **MINOR 1: met.** The involution argument, u -> u + (1 + lambda) y, is correct, and the 8 roots are listed.
- **MINOR 2: met in substance.** b' = 27a - 14b between carries, and -27a - 14b at the round's edge (re-derived). The new 3-to-1 reading is B1 above.
- **MINORs 3, 4 and 6: met.**
- **MINOR 5: met as approximations** (MINOR 2 above).
- **MINOR 7: met.** per8 and arith8 read the edges, C and G from the world (I checked per8.py). mat7 is named under OPEN 11.

## The physicist's items and section 12

- **The physicist's B1 and m1 to m10: met.** Spot-checked:
  - dec8 R3: 54 places on each of the three edges, 162 in all, from round 12, and 0 lines;
  - R2: c . q right in 197 of 200 rounds, the running |c . Q - 3W| at most 1, 3 of 145 landings as whole circulations;
  - R1's side pairs: 1 of 48, 12 of 23 and 5 of 44.
- **Section 12, items 1 to 13: met.**
  - NATURE1: 4, 85 and 67 rounds times 27 give 108, 2,295 and 1,809 of 4,212 places.
  - MATH1's physicist B3 (the frames, N or 3N, floor) and B1(c) (the teeth in the record).
  - MIN1's frame: H2 H1 = [[19, 6], [60, 19]] on (tau, eta), which is L on (eta, tau).
  - KEY3's m2: D = 3K and G D = 9K are odd for every middle.
  - "Bell is in the clicks": outcomes are the record's c . q; settings and pairs are clicks.
  - Big Pic's fork: roads A, B and C are named, none picked. Section 8's local bound is correct: a mixture of the sixteen strategies.

## SOUND (with numbers)

- **My own writing of the member on the board** (200 rounds, 27 Node-clocks):
  - mode 11's digest d49a09c277769a4e and the first click's 1d221a1be329f42a;
  - each clock's identity at 0 of 81 ends;
  - the lines differ at 4,644 places;
  - each clock's total less floor(swept / D) is +3, -4, +3.
- **The batch's arithmetic:**
  - G D = 9K = 457,302,861, born 228,651,430;
  - D = 3K = 152,434,287, born 76,217,143;
  - 2 entries times 27 Node-clocks = 54;
  - a fresh walk's variance over one period at a = 0.1 is 528,480 x 0.1 x 0.9, about 47,600, so 1,808 is 8.3 SE.
- **Fully met:** the period's order (N = 528,480 = lcm(9, 160, 2,936); 3N = 1,585,440); the frames; L = H1 H2; the local CHSH bound; the 1.4 record holding w exactly.

## DERIVED / MEASURED / OVERCLAIMED

**DERIVED (re-derived):**
- sections 3, 4 (bar B1), 6 and 7;
- the twin's descent to D;
- the fixed points at 3 | y;
- the exact value's margin condition.

**MEASURED (rerun):**
- arith8, dec8 and per8 from my copy, byte-identical;
- mine8, twin8 and mine8_board, as above.

**OVERCLAIMED:**
- "the residue mod 3 is kept apart" (B1);
- "Each a count on the triangle's dial G D" for the twin (B1);
- "the period is N ... 3N" for every lay (MINOR 1);
- "per period" z^2 given as counts (MINOR 2);
- dec8 R4 labelled MEASURED (MINOR 4).

## Questions for the Boss

1. Does the owner's batch carry the twin on D (ALG1 4.3, measured here at the file's key with its run back) in place of item 1's G D? Item 2's 3D = 9K stays, for tau and the triangle's edges.
2. Should the batch's period be stated as the round's order (N or 3N), with every orbit's period dividing it, the birth's orbit reaching it, and fixed points at 3 | y?

## Solution24 (the reader's line)

THIRD8 folds every THIRD7 item correctly and its numbers stand, re-measured. The one item left is that the twin needs only the dial D. That makes the owner's cost smaller and the landing coordinate's now and before exact, and it goes to the owner as one changed line in item 1.

