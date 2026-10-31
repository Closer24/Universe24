<!-- Boss note, 2026-10-31 11:24 UTC: written by the Boss from the reader's hand-back (the harness refuses report files from readers); the text below is the reader's, whole. Reader of Big Pic's Bell from the end (bigpic-3clicks 2a839f25f, three_clicks/bellend.py), the hostile mathematician (the HALF pair's mathematician). -->

Reader of Big Pic's Bell from the end (bigpic-3clicks 2a839f25f, frozen), the hostile mathematician (the HALF pair's mathematician). My harness does not let me write report files, so the whole report is below. Please file it as S/bp_bell_math/REPORT.md.

My probes and their outputs are in S/bp_bell_math/:
- p_exact, p_board and p_record, each a .py with its .txt;
- bellend_mine.txt and pairbell_mine.txt;
- rerun/, the copy, with node-all's src extracted.

# The hostile mathematician (HALF pair) on Big Pic's Bell from the end, 2026-10-31

**Read:**
- BRIEF_PAIRS.md to its end (line 1179), including the 11:06 rulings on my DECODE3i questions.
- In three_clicks/: bellend.py and bellend.txt, pairbell.py and pairbell.txt, README.md (stage 4c) and PICTURE.md section 11.

**Checks:**
- FROZEN.sha256: 149 of 149 OK.
- The tar's 27 files are node-all 9d75a4904's src blob for blob, and the bench's 148 tool files are 2a839f25f's (git hash-object against git rev-parse).
- The click world's key on node-all is 50,811,429, odd and 1 mod 4.

**Reruns:** from the copy, under the live venv's Python 3.14.6 -I -B, nice 19, with the load 2 to 7. bellend.py and pairbell.py each reproduce their .txt byte for byte. No bytecode appeared.

I touched no repository or worktree (git show, archive, hash-object and rev-parse only). I did not open the other reader's folder, and I posted nothing.

VERDICT on Big Pic's Bell from the end: PASSED

(as a counted law: no BLOCKING; seven MINOR)

## What the law is, exactly (DERIVED here; MEASURED exactly in p_exact)

- **The A end alone.**
  - A's outcome is +1 or -1, one count each way.
  - The hand is then a, or a-perp.
  - B lands +1 with probability s(h, b) = (h . b)^2 / ((h . h)(b . b)).
  - In the plane, s(a-perp, b) = 1 - s(a, b). So P_A(oA, oB) = (1 + oA oB cos 2 theta) / 4.
- **The B end gives the same law,** because s is symmetric.
- **So every weight w_A : w_B gives one law,** even a weight that reads the settings. Its marginals are 1/2 and its correlation is E = cos 2 theta.
- **CHSH** is a sum of cos 2 theta terms with signs. Its supremum is 2 sqrt 2 (Tsirelson), and the triangle's settings give 5/2.
- **It is the collapse rule with Malus's square, laid on the triangle's plane.**
- **MEASURED exactly** on all 144 ordered pairs of the 12 lattice directions, at the weights 1:0, 0:1, 1:1, 1:2 and 3:7:
  - every joint count equals (1 + oA oB cos 2 theta) / 4: 0 off;
  - every +1 share is 1/2: 0 off;
  - 1:0 equals 0:1 as fractions: 0 off.
- **Over all 12^4 setting choices on the 30-degree lattice,** the largest CHSH is 5/2.
- **The free lay** reads exactly half: E_free = (1/2) cos 2 theta on all 144 pairs, with +1 shares of 1/2.
  - The reason: averaged over 12 hands 30 degrees apart, cos(4h - 2a - 2b) is 0, since 4h steps by 120 degrees.

## BLOCKING

None.

## MINOR

1. **Tsirelson is approached on the lattice, not reached** (bellend lines 158-189; README "which is Tsirelson's 2 r2").
   - At z = 13 + 5w, the turn's share is 147/172 and CHSH = 449,753 / 159,014 = 6c - 4c^3, with c = cos 2 phi = 61/86 (MEASURED).
   - In millionths that is 2,828,386, against 2 sqrt 2's 2,828,427: 41 millionths below. Squared, it is strictly below 8.
   - Both round to 2,828 per mille.
   - At z = 57 + 22w the value is 43,089,809,330 / 15,234,548,239, which matches 2 sqrt 2 to the millionth and is still below it.
   - Every lattice reading is rational, so none equals 2 sqrt 2.
   - The settings z^k are picked to near 22.5 degrees.
   - Fix: write "a lattice point 41 millionths below Tsirelson's 2 sqrt 2, the law's supremum".
2. **"From the end" is not read.**
   - Part (ii) is not computed. The hand goes from A's branch straight into B's share (end_law_on, lines 75-81).
   - The same numbers would come from A's collapse reaching B directly.
   - The weight is idle by the identity above, so no pair reading can tell which end fixed the hand.
   - So "at every weight read" is one identity read four times.
   - README stage 4c names the board's act OPEN. Fix: name the identity, and say that (ii) is untested.
3. **Exact no signal holds on the counting, not on a fixed dial** (p_board; exact fractions).
   - The setup, as pairwhole.py does it: the end click at HALF/D with HALF = (D - 1) div 2, and the far click at ((n D) div d)/D.
   - On the key's dial D = 50,811,429, the far +1 share moves with the near setting.
     - At B 90 it moves by (5D - 1) / (4D^2) = 63,514,286 / 2,581,801,317,022,041. The A end at B 90 and the B end at A 0 give the same figure.
     - CHSH there is 2,499,999 per million.
   - On the even dial D - 1, 3/4 and 1/4 are exact, but HALF is still one short. The signal is then 3/(2D), and CHSH is 5/2.
   - Exact no signal needs an exact half and 4 | D.
   - pairwhole's docstring says "the dial is odd so the birth is the centre", so the two needs conflict on one dial.
4. **"Every seed is counted" is not what makes the law fair.**
   - Each branch is scaled to a common total (lines 82-86), so the end's two outcomes weigh one each.
   - If every seed of both branches counted alike instead, A's +1 share at A 0, B 30 would be 1/4 (p_exact).
   - B's +1 share at B 90 would then be 3/4 under A 0 and 3/8 under A 60: a signal.
   - The scales' exactness holds by construction (each total contains its divisor), but no assert checks it.
   - The far denominators are 4, 12, 36 and 108. The comment at lines 72-73 says "36, 12 or 4".
5. **The free lay is a weak control.**
   - It is the share rule's local case, half the law's correlation.
   - The local bound to compare with 5/2 is 2, which Big Pic's own sign rule reaches (twoends.py, PICTURE section 11).
   - 1,250 bounds nothing.
6. **R4 and the end law's records.**
   - bellend counts seeds and writes no record, so R4 has no order to read there. README names it OPEN.
   - I wrote the law as records (p_record): the toy's frame, the key's dial, 40,000 pair events. R4 in the ruled DECODE3j form read them as DECODE3i's r4i plus the two-sided ladder plus the joint of both places both ways:
     - E1, the A end throughout: S 2,543 and 2,502; SHOWN;
     - E2, the end set by the pair's tooth: S 2,519 and 2,486; SHOWN;
     - E3, a late hand (B reads the previous pair event's hand): S -37 and 23; NOT SHOWN;
     - E4, the late hand at 1 pair event in 10: S 2,257 and 2,271; NOT SHOWN.
   - These verdicts are right, but E3 and E4 fall only to (a), the curve and (e).
   - Every order part passes the late hand, because it runs through the far place's outcome, which no order part reads.
   - A far-outcome lag sum on 16 degrees refuses E3 (329,134 and 281,287, against the cut 39,697) and passes E1 and E2. It also passes E4.
   - For DECODE3j: add that sum, or name the reach.
7. **pairbell.py, beside the bench.**
   - It uses random, float, Fraction, divmod, % and //, which is outside the whole-number rule.
   - Its exact value, 13,651,918 / 4,826,809 = 6c - 4c^3 at c = 119/169, is also below 2 sqrt 2: 2,828,352 millionths.

## SOUND, with numbers

- **Exact fractions:** integers throughout. The CHSH is exactly 5/2 at every weight read (for example 48,521,024,904,413,357,015,040 / 19,408,409,961,765,342,806,016).
- **Seed enumeration:** complete. Every far seed of every branch is counted, and both of the end's outcomes.
- **(iii):** at multiples of 30 degrees every share is one of the triangle's squares 1, 3/4, 1/4, 0 (every 2E is whole).
  - Elsewhere on the lattice a share is rational but not one of those squares (147/172 at z).
  - Off the lattice no whole share exists.
  - On the key's odd dial even 3/4 and 1/4 are not whole: floor(3D/4)/D = 3/4 - 3/(4D).
- **The curve:** E = cos 2 theta on every lattice pair.
- **No signal:** exact at every weight and every pair, not only the four read.

## DERIVED / MEASURED / OVERCLAIMED

- **DERIVED, sound:** the joint law (1 + oA oB cos 2 theta)/4 for either end; the weight's invisibility; the no-signal identity; the free lay's half; the supremum 2 sqrt 2.
- **MEASURED:** bellend's tables, reproduced. Mine:
  - the 144-pair exact checks;
  - the lattice maximum of 5/2;
  - the Tsirelson fractions;
  - the uniform-seed counts;
  - the fixed-dial signal;
  - the end law's records under ruled R4, and the far-outcome sum.
- **OVERCLAIMED:**
  - "Tsirelson's 2 r2" for 449,753/159,014;
  - "every seed is counted" as the source of fairness;
  - "Bell from the end" and "at every weight", read as tested;
  - exact no signal, read as holding on the board.

## Questions for the Boss

1. Does Tsirelson's line become "a lattice point 41 millionths below 2 sqrt 2, its supremum"?
2. For the board form: the end needs an exact half and the far shares need 4 | D, but the key is odd. Which comes first: a dial that holds the half, or a fair end by another act?
3. No pair reading can tell the end, the weight, or a direct far transfer apart. Should the owner's "Bell's weight" be read some other way, or named idle in this law?
4. For DECODE3j: does R4 add the far-outcome lag sum, or name the far outcome's reach?

## Solution24 (the reader's line)

As a counted law, Bell from the end is right and exact. The collapse rule on the triangle's plane gives cos 2 theta, 5/2 with no signal, and Tsirelson's bound as a supremum. What is left is the board: an odd dial cannot hold the fair end, and no pair reading tells the end from a direct far influence.
