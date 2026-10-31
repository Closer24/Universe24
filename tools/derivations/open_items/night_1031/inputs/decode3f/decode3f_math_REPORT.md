# The hostile mathematician (HALF pair) on DECODE3f, 2026-10-31

(Written by the Boss from the reader's hand-back at 08:4x UTC, the reader's harness refusing the write; the text is
the reader's, word for word. The reader's probes are in this folder.)

**Read:**
- BRIEF_PAIRS.md, including its three newest sections.
- DECODE3f.md (599 lines; sha256 14c9d7951d62179b... matches; every file in FROZEN.sha256 OK).
- decode3f.py and its run.
- Both DECODE3e reports, with the Boss's answers.

**Reruns:** from a copy of the frozen folder in decode3f_math/rerun/, using python3 -I under nice -n 19 with the load checked first. decode3f.py's output is byte for byte equal to the frozen run1, and run1 equals run2. The frozen folder's decode3e and pair_order reruns equal frozen_out/. Nothing was touched in /home/user/Universe24 or in the frozen folder.

## VERDICT on DECODE3f: NOT PASSED (one BLOCKING; every DECODE3e item of mine is met)

## BLOCKING

**B1. R2 fails a right record where the passing moves** (line 89: "R2's gate stays (3b) SHOWN and E2 >= M2"; lines 516-523, M2's chance).

- **Why it breaks.** Since DECODE3e, (3b) is passing-given, so its SHOWN no longer means a steady passing. The Boss's 05:3x ruling gated R2 "on a steady passing ((3b) SHOWN)". So R2 now reads where the passing moves.
  - E2 = th(n (n - 1), H) and C(H - n + 1, n) / C(H, n) both hold only at a steady passing, where placements are exchangeable given n.
  - Where the passing moves, the pairs expected are SUM p_r p_(r+1). The gate's E2 can overstate that without bound.
- **MEASURED (r2_moving.py).** decode3e.py's own (3b) and r2, fair stand-in draws, halves of 2,000, 100 draws a case:

| passing | R2 NOT SHOWN, of records read | the gate's E2 (thousandths) | the passing's own expected pairs | chance of no pair a half (thousandths) |
|---|---|---|---|---|
| alternating 350 and 0 | 87 of 87 | 70,500 | 0 | 1,000 |
| alternating 348 and 2 | 54 of 94 | 60,378 | 1,391 | 316 |
| alternating 345 and 5 | 8 of 86 | 66,795 | 3,448 | 57 |
| alternating 340 and 10 | 0 of 85 | 71,253 | 6,796 | 3 |
| steady 175 (control) | 0 of 95 | 62,835 | 61,219 | 0 |

- **This is mine to own.** I missed it in my DECODE3e reading, and the text quotes my formula, which is right only at a steady passing.
- **Fix:** read R2 where the passing-given chance that a half holds no landing twice in a row is at most 1/20.
  - Compute that chance exactly from the passing alone, by the transfer recursion f0 = (D - x)(f0 + f1), f1 = x f0, in whole numbers over D^H. r2_moving.py does this.
  - A gate of th(SUM x_r x_(r+1), D^2) >= M2 is not enough. At 345 and 5 it reads 3,448 against an exact chance of 57 thousandths, because one landing at a low round makes two pairs at once.
  - Or restore the steady gate of the 05:3x ruling.

## MINOR

1. **(3p) and R3 on W** (lines 80, 121-127).
   - R3's rule lists only (3b), (3d) and (3e). But (3p) says "NOT READ where no period is carried. R3 on W is then NOT READ."
   - No period exists where y moves, so as written R3 on W is NOT READ on every moving passing.
   - decode3f's r3 never takes (3p). A3's R3 NOT SHOWN on W carries no period.
   - Fix: (3p) applies on a steady stretch only. Put it in R3's rule for W, and carry P = 1,585,440 into A3.
2. **The cuts are on two conventions** (lines 109, 219-220; G's own line "N_T 1 ... cited 3,841").
   - cuts_check.py uses a different method: erf's positive (Kummer) series, and pi from atan(1/2) + atan(1/3). It confirms that each of CUT_FW 8,948, 9,141, 9,622, 9,885 and 10,116 (N_T 18, 20, 26, 30, 34), and CUT4 9,488, is the least whole thousandth whose tail is at most its level (True at C, False at C - 1).
   - CUT 3,841 and CUT2 5,991 sit one thousandth below the least (3,842 and 5,992).
   - Both are valid: the statistics are floored, so NOT SHOWN needs at least C + 1. The floor's cut is the tightest at the level, and the least is one thousandth conservative.
   - Name one convention. The decoder takes its cuts from the readings file; G's bisection checks the citations, and r4f should not compute CUT_FW at read time.
3. **C-e's check can never hold** (lines 507-511).
   - (2r_f)^2 m^2 = 2 n^2 (2r_a)^2 has no solution in positive whole numbers; one would make the root of 2 a ratio of whole numbers. The same goes for 3 l^2. As written, every record reads NOT SHOWN.
   - C-c's and C-d's exact cross-multiplications likewise fail a right record wherever the counts' grain enters.
   - Fix: read each check within the grain, as C-a's "within one count" does. For example, C-e reads SHOWN where (2r_f - 1)^2 m^2 <= 2 n^2 (2r_a + 1)^2 and 2 n^2 (2r_a - 1)^2 <= (2r_f + 1)^2 m^2.
4. **R4's (c) gate inherits R3's family** (lines 187-188). R3 reads a right place SHOWN about 3 times in 4, so R4 reads NOT READ on about 4 in 10 right pair records. Name it. Under a family-wise R3 it falls to about 1 in 10.
5. **The ladder's cost** (lines 221-222).
   - The gate's figures are right: E8 = n p_maj^7 p_min^2 is the second likeliest past of length 8 followed by the rarer outcome, and n p_min^2 >= 5 is lag-1's cells.
   - But "below e^(-M2) a rung" (5 per cent) is too weak a bound to keep R4's family at 5 per cent.
   - The true cost is far below alpha / N_T: eight pasts of that likeliness serve, and so does the likeliest past. Give that bound, or count the ladder.
6. **D4's no is a typed table that cannot fail** (decode3f E's READINGS). D4 is a rule on which inputs a reading may take, a code check; name it so. "81 of 81 clocks" is the reason for D4, not its check.
7. **One key per record** (lines 434-440). The probe compares each card's key with the header's dial, and its stand-in sets each card's "key" to the dial. On node-all the dial is (kappa div senses) K (KEY3). Name the field, and compare through that relation.
8. **Precedence across halves.** decode3e's (3b) reads NOT READ first; R3, (3e) and R4 read NOT SHOWN first. Use one precedence at every level.
9. **(3e)'s SHOWN is mis-named** as "no past of length 2 fixed the next landing" (line 132). It reads that the landing rates given the last two outcomes match the passing, which is R2's claim and more. Name it so.

## The Boss's open item: R3 at one family-wise level

**Sound, with four conditions.**

- **The union bound holds whatever the dependence.** The three tests share one record's landings, so Sidak's independence form does not hold within a half, but Bonferroni needs no independence. P(any false NOT SHOWN) <= 6 x 5/6 per cent = 5 per cent, as accurate as each test's own large-sample law.
- **The cuts, in whole numbers (cuts_check.py):** one degree 6,961, two degrees 9,575, four degrees 13,696.
- **MEASURED (family_r3.py, decode3f's R3 with every cut moved):** a right record reads NOT SHOWN 16 of 300 (steady 175), 15 of 300 (the swing) and 8 of 200 (steady 300), about 5 per cent. At the 5 per cent cuts the same draws read 60, 70 and 44 (20 to 23 per cent).
- **Condition 1: the carried bound's gate moves with the (3b) cut.** Otherwise the theorem breaks.
  - The theorem is z^2 (carried) >= the bound's own z^2 > the cut, with one cut for both.
  - With the verdict at 6,961 and the gate left at 3,841, a carried steady side at 100 a round (halves of 1,000, K_MIN 15) reads SHOWN 20 of 20. With the gate at 6,961 it reads NOT READ.
  - The cost: at K_MIN 15 the bound's own z^2 falls below 6,961 on 10 of my 11 passings (NOT READ). At K_MIN 20 it does so on 4 (the short halves, and 100 a round at 1,000). So K_MIN goes to 20.
  - The balanced-word bound passes 6,961 only at K = 21: 7,073 there, 6,735 at K = 20.
- **Condition 2: the structural NOT SHOWNs come inside the budget.** The two-values rule costs at most 3 e^(-E_min) a half, to first order. At E_min = 5 that is 20 per 1,000, more than the 8.3 share. Give it a share, raise its cells, or cite its measured rate (0 of 6,000 halves). (3p) on a draw costs nothing that matters.
- **Condition 3: one cut convention, and the rate measured and named.** Measure on at least 1,000 right records a case, steady and moving. Where the rate exceeds 5 per cent beyond its error, take the cuts from the measured tails, never moved for an outcome.
- **Condition 4: R2 stays out of R3's family,** with its own gate (B1).

## My DECODE3e items, each

- **B1 (3d) passes carried moving sides: met.** R3 is gated on (3b); line 203 is corrected; the general claim is struck. My families read 3,528 NOT READ, and 182 NOT READ with 790 NOT SHOWN.
- **B2 (e) passes a fixed order: met.**
  - (e) is read per source, by lag-1 and R2's ladder.
  - The own-past-settings tests are added, and (c) keeps its gate with each place's passing carried.
  - (e) is named necessary only.
  - The six drawless forms are each refused by a named part, and the section 2 table matches the run.
  - The no is DERIVED for a source carried at a steady passing: Morse-Hedlund holds on a finite record, and r1 = -p/(1 - p).
- **MINOR 1 (M2): met.** m2_check.py enumerates every H from 2 to 16 and every n, with 0 disagreements, and m2_exact.py reruns byte for byte. Its scope is steady only (B1).
- **MINORs 2 to 7: met.** Line 278 is struck, with the twin's structural no and NOT READ on different headers. The power words are fixed. The bound reads 5,042 at K = 15 (4,025 at K = 12). The text and code agree. K = 3 I and section 8 are in. The lone edge is recomputed exactly: a moved landing reads NOT SHOWN at round 2, where the old check passed at 690.

## SOUND, with numbers

- The reruns match byte for byte, and the checksums hold.
- G's cuts are confirmed by an independent method, and so are 9,488 and 5,042.
- R3's gate, and the carried no through (3b)'s bound.
- (3e)'s law: martingales on predictable classes, four degrees. Its power is 5/p^3: 930, 5,000, 7,900 and 14,600.
- N_T = 2 (13 + 2 S): 30 and 34.
- c . q to within one: at K = 3 I, 3D (c . Q) = c . (g_before - g_after), so |c . Q| <= 2 and SUM W is one of two values.
- THIRD7's (3e) reading: 658 against 809; the fair draw reads 1,555 and 2,348.
- One finding overturned by my own measurement: I suspected (3b) ran high on alternating passings, but 300 records give 27 and 24 NOT SHOWN against 29 at steady 175. My first 100 (13 to 15) were sampling.

## DERIVED / MEASURED / OVERCLAIMED

- **DERIVED, sound:** R3's gate; line 203; (3e)'s law and power; (e)'s carried no; (ii)'s twin no; K = 3 I; c . q; the cuts.
- **MEASURED:** the text's tables, reproduced. Mine: R2 failing where the passing moves; the family-wise cuts and rates; the carried bound at a raised cut; M2 by enumeration.
- **OVERCLAIMED:**
  - R2's gate "stays", with M2's steady chance as its level where the passing moves;
  - C-e as a check "that can fail";
  - D4's typed no;
  - the ladder's e^(-M2) as holding R4's family.

## Questions for the Boss

1. Should R2 take the passing-given exact chance as its gate, or the steady gate again?
2. Does K_MIN rise to 20 with R3's family-wise cut?
3. Are R3's gate costs and the ladder counted in R4's family, or named beside it?

## Solution24 (the reader's line)

The carried no stands by (3b)'s theorem, and R4's order now refuses every drawless form named. R2 must read the passing it now admits. R3's family-wise cut is sound once the carried bound's gate moves with it.
