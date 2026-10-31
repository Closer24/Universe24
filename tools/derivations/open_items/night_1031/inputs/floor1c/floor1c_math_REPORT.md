<!-- Boss note, 2026-10-31 12:45 UTC: the ALG mathematician's report on FLOOR1c (toys-5 cfedc44e4, text e061b814), handed back whole; filed by the Boss -->

# The hostile mathematician on FLOOR1c (David's "The floor's balance: masses against bands", third text), 2026-10-31

(The harness refuses report files from subagents, so here is the whole report for S/floor1c_math/REPORT.md. ASCII only.)

**What I read**
- **FLOOR1c**, frozen at S/floor1c_frozen (toys-5 cfedc44e4). All 10 sums check OK, before and after my runs.
  - The text, DAVID-FLOOR-BALANCE.md: 438 lines, sha256 e061b814.
  - The probes and their outputs are unchanged since FLOOR1b: floor_balance.py 6b57b724, floor_balance.txt e9aeed9d, ring_balance.py 08ca35c9, ring_balance.txt a4bcf1d9.
  - The README (d17979d5), and the two inputs beside them.
  - I did not open held_cells.py or its output.
- **The brief to 12:38 UTC.** This includes the 12:4x ruling on my FLOOR1b report, the owner's words 12:23 to 12:30, and the 12:38 ruling on FLOOR1c's physicist. I did not open S/floor1c_phys.
- **G3's passed text** (toys-5 ff921b0ed, "G3 PASSED by both end readers (the fifteenth text)"), read by git show into S/floor1c_math/g3_ff921b0ed.md. FLOOR1c cites its two bounds.

**How I ran** (in S/floor1c_math/; the live venv's Python 3.14.6, -I -B, nice 19, one process at a time, load 3 to 5)
- copy/ is a copy of the freeze, and src/ is its tar extracted.
- The inputs against git, read only:
  - git rev-parse 9d75a4904:src gives 83c9e3eb...;
  - git archive 9d75a4904 src hashes to 0881d3f0...;
  - 9771a49a4's miracle/equil.py hashes to 0c4c936d....

  All three match section 5.
- Reruns:
  - every measured line of floor_balance.txt;
  - ring_balance.py 3 10;
  - the new fall-bits rows (8 to 20);
  - the lam 1 control at the 32-bit line.
- rest_check.py checks press point 3's formulas in whole numbers, with the carry as the one division.

**VERDICT on FLOOR1c: PASSED.** There is no BLOCKING item.
- The algebra and the board readings stand as in FLOOR1b, and every measured line reruns byte for byte.
- The text folds most items, and the floor line is quoted whole.
- There are nine MINOR items.
- Two corrections are my own, and I withdraw my earlier wording:
  - the floor line's "On any structure" and "exactly half" need their scope;
  - the steady rest's window does not "close as the pair widens".

## BLOCKING

None.

## MINOR

**1. The floor line's scope words.** They are my FLOOR1b Q1 wording, now in the 12:4x line and in the 12:38 line, and I correct them.
- "On any structure the edge is at -lambda_min(A) t/2" is 2.3's result for equal springs and equal bands, within 2.3's scope. Two cases fall outside:
  - 2.3's own counterexample: a band to a held hand, where V >= -(t - 2s)^2/(4c) at every s >= 0;
  - unequal springs, where the edge is at diag(s) + (t/2)A singular and non-negative.

  Read: "on any structure with equal springs and equal bands (2.3's scope)".
- "On one band, exactly half the band gives the edge, and more than half holds the form" is the equal-spring case. For unequal springs the edge is s1 s2 = (t/2)^2, and the hold is s1 s2 > (t/2)^2 with s1, s2 > 0 (2.1); one spring may sit below half.
- The form beside the edge clause (my FLOOR1b MINOR 3(e)) is now ruled in the 12:38 line ("Under the two laid ties ... under David's cell it lends nothing"). FLOOR1c, frozen before that ruling, does not name it.

**2. 2.5 misreads G3's two bounds.**
- **(a) Which form is necessary.**
  - G3 says: "The frozen bound is a guide, only its form at the rest, 2 SUM_6 g + 8 hat n < 4 W, being necessary (for the linearization there), and it is not sufficient".
  - FLOOR1c says: "the frozen guide, 20 hat R^2 below 4 W, necessary at the rest and not sufficient".
  - The 20 hat n form is the stiffness at the far turn of a hand that rolls from the top. It is not the rest's form.
- **(b) What the measured bound covers.**
  - G3 calls 20 hat n <= W "the window for swings that reach the top".
  - It was measured Mesh-less at R = 244 and 3,125 only, and "At small R it fails" (R = 4 to 40), with the frame's lower bound on R OPEN.
  - A hand held still at its rest makes no swing to the top, so this bound cannot exclude a still rest beside S.
  - So "no rest exists beside S on the click world" (2.5) and "none under the measured one" (section 6) do not follow.
  - The physicist's 0 of 40 at the bound's largest hat checks the condition 2 hat n > S at 2 hat n = W/10. It does not test a rest inside G3's window.
- **(c) The window and its closing:** see press point 3.

**3. Two routes are stated as facts in the letters.**
- **"The band's route is the one cell's 2 f h^2 (CELLS1)."**
  - CELLS1 is a first text, not passed by a pair.
  - Its own README row gives 2 f h^2 = 120,000 at h^2 = 1, with "the laid 96,000 is 4/5 of it".
  - The 12:2x ruling names the move from 96,000 to 2 f h^2 "a change of the act, the owner's".
  - Read: "a candidate route".
- **"S: ... the grip at rest, den Gamma^2."** The value is right. But on the probe's src (node-all 9d75a4904) the click world's file chooses it ("chosen": spring 100000000, hold 1, tie 96000, key 50811429). The loader's route is node-short's (the 11:3x ruling).
- Right by the code:
  - W = 6 grips (load.teeth: Spokes x den Gamma^2);
  - c = hold x (rest div Gamma) (plans.holding) = 60,000;
  - the key's middle, 25,405,714.

**4. The owner's words since FLOOR1b.**
- **12:23:** section 4's "the clicks choosing the path" should read "the third click chooses the path". This is the one place where FLOOR1c reads against an owner's word. It is now ruled at 12:38 (Q2).
- **12:25 with 12:27:** FLOOR1c's floor is the board's form. The OPEN list should carry Big Pic's check: whether the third click's triangle gives the floor that keeps the run. Without it, the floor line can be read as the clicks' floor. The physicist's M3 at 12:38 covers this.
- Nothing contradicts 12:23, 12:25, 12:28 or 12:30:
  - no click is read;
  - nothing is laid for the floor;
  - every row is the board run with no click writing, "the path without the choices" (12:28).

**5. My FLOOR1b MINOR 6, remainder.** 2.4's "A reversed odd loop sits at the edge, and a reversed even loop holds" is unchanged. It is right for one band reversed, and wrong if every band is reversed: an even loop with all its bands reversed sits at the edge. Read: "with one band reversed".

**6. My FLOOR1b MINOR 7, remainder.**
- The heading now reads "The fall from round 818 to 824", but the second part still says "at round 818 the returning swing kicks the held count to 371.97 units". The count is 51.13 at round 818 and 371.97 from round 824.
- The new fall-bits line reruns exactly: 8 bits at round 824; 10, 12 and 14 at 825; 16 and 18 at 826; 20 at 827.

**7. My FLOOR1b MINOR 8 (FLOOR1 MINOR 6), not met.**
- node-all's own falls are still not named beside section 4's "shipped fall", which is the triangle's:
  - the shipped runner's round 3,752 at lam 1;
  - under road B on node-all's act, round 9,582, a count past 32 bits (the MIRACLE physicist, 12:2x; the model equals the act in 38 of 38 windows).
- New, MEASURED: FLOOR1c's own lam 1 control falls at round 9,581 at its 27-bit line, and at round 9,582 at the 32-bit line (fall bits 26). So 9,581 and 9,582 are one fall, read at two widths.
- Still not said: whether node-all's tied trains meet 2.3's scope. The lend is diagonal by Schur on the signed-permutation kinds; a kind-E train lends off the diagonal.

**8. My FLOOR1b MINOR 9, remainder.** The inputs are now frozen by path and sum, and they match git. The control's reference, split_bedge_x100_5000.txt, and equil_5000.txt are still cited by name only. They are frozen at S/bigpic_2a839f25f_frozen/.../miracle/.

**9. Small items.**
- Section 5: "S/floor1b_mat" should read "S/floor1b_math".
- "Held lays from 90 up" (sections 1, 4 and 5) should be "the lays read". At lam 100 those were 90 to 400 falling, with 20 to 80 holding over 5,000 rounds. At lam 1 a held lay of 20 already fells s = t (round 2,751).
- The README's floor row still says "below the edge a held swing holds the pair only for a while". That goes against section 5's rule ("no fall over N rounds" at or below the edge; "hold" for s > t/2).
- Section 7's "the report's other two are owed by the Boss's inputs pack" should name the two. They are my MINOR 2 and 3, ruled at 12:4x and folded through the floor line and 2.5.

## The press points

**1. My nine FLOOR1b MINOR items**

| Item | Status | Where |
|---|---|---|
| 1. "Whatever the held hand does" | MET | Sections 1, 4 and 5: the form's hold DERIVED, the run MEASURED, the wide held hand cited |
| 2. The statement's scope | MET through the scoped line | New MINOR 1 for its words |
| 3. The steady rest | MET in substance | Set aside, its condition 2 hat n > S + c(g^2 + u^2) named, "even s = 0" withdrawn, the local hold named. G3's bounds are misread (new MINOR 2), and the form is now ruled at 12:38 |
| 4. "Held exactly while that lend stays positive" | MET | Withdrawn in 2.5; section 1 |
| 5. The header's DERIVED | MET | "DERIVED given the springs ... a candidate" |
| 6. Wording | PARTLY | "an odd loop of plain bands" and the ring-joining clock fact are done; "a reversed even loop holds" remains (new MINOR 5) |
| 7. The fall account and naming | PARTLY | Every reader is named by his pair, and the heading is fixed; the sentence is not (new MINOR 6) |
| 8. node-all's falls; the scope versus the kinds | NOT MET | New MINOR 7 |
| 9. The freeze | MET for the inputs | The references are not named by path (new MINOR 8) |

**2. Is the scoped floor line quoted whole and used rightly?**
- It is quoted whole: the text's quote and the 12:4x ruling are equal to the character (616 characters, whitespace aside).
- It is used rightly as the Boss's words. Each clause is derived in its place: one band in 2.1, a network in 2.3, the square form in 2.4, the board in section 5.
- Two words need scope, both from my own wording: "On any structure", and "exactly half" on one band (MINOR 1).

**3. The local window for a rest beside S (S/2 < hat n < 6S/5) under G3's frozen guide**
- **As arithmetic it is right:** it is G3's bound read as a strength bound, 20 hat n < 4W with W = 6S, together with the rest's existence at the pair's rest, 2 hat n > S.
- **It is not G3's guide as G3 reads it** ("only its form at the rest ... being necessary"). Write A = S + c(g^2 + u^2).
  - The true rest is at h^2 = n - A/(2 hat).
  - The stiffness there is 4(2 hat n - A).
  - So the guide's necessary form is 2 hat n < A + W. With existence, A < 2 hat n < A + W.
  - At the pair's rest that is S/2 < hat n < 7S/2.
  - The window does not close as the pair widens: both ends rise with A.
- **The far-turn reading does not close either.** With S beside the hat, a hand rolling from the top turns at h^2 = 2n - A/hat, where the stiffness is 20 hat n - 10A. Then A/2 < hat n < A/2 + W/5: a band of width 6S/5 at every A.
- Checked in whole numbers by rest_check.py at (A, hat, n) = (100, 50, 3):
  - the stiffness at the rest is 800;
  - at the far turn it is 2,000;
  - the height above the rest is 200.
- **I withdraw my FLOOR1b Q3 claim** that the window "closes as the pair widens, about 41 to 48 units". It added S and the lend to the hat-alone far turn at 2n, or took 20 hat n < 4W with no S. That over-counts, and FLOOR1c's 2.5 and the 12:4x ruling repeat it.
- **What stands:** whatever the window, the rest holds the free swing only locally. Its height is (2 hat n - A)^2/(4 hat) above the rest, with the swing flat at hat n^2 along h = 0. None of this binds road B's dialed held hand, and under "no hat" the question rests.

**4. New overclaims**
- G3's "necessary" attached to the 20 hat n form, and "no rest exists beside S on the click world" (MINOR 2).
- The band's route through CELLS1, and S's route on node-all (MINOR 3).
- "The clicks choosing the path" (MINOR 4).
- "Held lays from 90 up" (MINOR 9).

## SOUND (rerun or re-derived)

**Reruns**
- All 58 measured lines of floor_balance.txt (55 rows and 3 window lines) rerun byte for byte, and so does ring_balance.
- The fall-bits rows reproduce.
- The lam 1 control falls at round 9,581 (27 bits) and at round 9,582 (32 bits).

**Unchanged from FLOOR1b, and still sound**
- 2.1: the bound, the hold of the form, the kernel, and the drift exact at every round.
- 2.2: 315 and 2,139.
- 2.3: within its scope.
- 2.4: Harary under the square form, and the ring rule. Earlier I checked all 44 rings from 3 to 24 against the closed form.
- Section 3: the decomposition and the states.

**New in FLOOR1c and right**
- The letters' code facts: W, c, and the key's middle.
- The inputs' paths and sums.
- The fall's rounds by bits.
- The rest's condition, 2 hat n > S + c(g^2 + u^2).
- The withdrawals: "even s = 0", and "held while the lend stays positive".
- "No fall over N rounds" at or below the edge.
- The clock fact for joined rings.

## DERIVED / MEASURED / OVERCLAIMED

- **DERIVED** (re-derived): as in FLOOR1b. My additions here:
  - the stiffness at a rest beside S, 4(2 hat n - A);
  - its window, A < 2 hat n < A + W;
  - the far turn 2n - A/hat, with stiffness 20 hat n - 10A.
- **MEASURED:** the 58 lines; the ring rule; the fall-bits rows; the 32-bit fall at round 9,582.
- **OVERCLAIMED:** MINOR 1 to 4 and 9 above.

## Questions for the Boss

1. **The floor line (12:38) for Sofer: add the scope words?** Proposed: "On one band with equal springs (the click world's giver and taker), exactly half the band gives the edge, and more than half holds the form; on any structure with equal springs and equal bands (2.3's scope) the edge is at -lambda_min(A) t/2." I withdraw my earlier wording.
2. **The 12:4x ruling's steady-rest sentence rests on my withdrawn closing.** Should it read "a rest beside S needs A < 2 hat n < A + W at the rest (S/2 < hat n < 7S/2 at the pair's rest), and holds only locally, below its height"? And should "no rest exists beside S on the click world" go, since G3's measured bound is for swings that reach the top?
3. **Do my items go to FLOOR1d with the physicist's six?** His M2 (the form) and M3 (the owner's words) overlap my MINOR 1 and 4.

## Solution24 (the reader's line)

FLOOR1c keeps FLOOR1b's algebra and board readings, all rerun. The floor is DERIVED given the springs, on a candidate square form. The hold above half is the form's, and the edge's lend does not hold for good. Under the square form the click world's one band sits at the floor's edge, and a still rest beside S would hold it only locally. A floor that keeps the run is not here; by the owner's 12:25 word it is to come from the clicks' own structure, the third click's triangle, which is Big Pic's check.
