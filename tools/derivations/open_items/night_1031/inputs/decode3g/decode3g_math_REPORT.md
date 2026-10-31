<!-- Boss note, 2026-10-31 09:40 UTC (first labelled ~09:5x, ahead of the clock): written by the Boss from the reader's hand-back (the harness refuses report files from readers); the text below is the reader's, whole. Reader of DECODE3g (frozen 083032b0), the hostile mathematician (the HALF pair's mathematician). -->

My harness does not let me write report files, so the whole report is below for the Boss to file as S/decode3g_math/REPORT.md. My probes and their outputs are in that folder: g_r2r3, g_r4 and g_cuts, each a .py with its .txt, plus rerun/ with its math_*_run.txt files.

# The hostile mathematician (HALF pair) on DECODE3g, 2026-10-31

**Read:**
- BRIEF_PAIRS.md: the 08:1x to 10:1x sections and the owner's word of about 09:05.
- DECODE3g.md, all 574 lines. Its sha256 is 083032b0..., as named.
- decode3g.py, cuts3g.py, grain_ca.py and gate_open.py, with their outputs.
- My DECODE3f report as filed. No Boss's answers are appended to it; the rulings are the brief's.

**Checks of the frozen folder:**
- All 88 files check against FROZEN.sha256.
- Section 0's eight quoted rulings are verbatim against the brief (checked mechanically).
- nl/ holds no symlink.

**Reruns:** from a copy of the frozen folder (decode3g_math/rerun/), under the live venv's Python 3.14 -I with nice 19 and the load below 8. decode3g.py, cuts3g.py, grain_ca.py and gate_open.py all reproduce the frozen outputs byte for byte.

Nothing was touched in any repository or worktree, I did not open the other reader's folder, and nothing was posted.

## VERDICT on DECODE3g: NOT PASSED (two BLOCKING)

## BLOCKING

**B1. R2's gate guards one of the contexts its ladder needs, so R2 fails right records behind its own gate** (section 1, lines 177-191; settled item 1).

- **Why it breaks.**
  - The gate is the chance of no two clicks in a row *with* s passing.
  - But at L = 1 the ladder needs both pasts followed by both values. So it also needs two clicks in a row *without* s, the past 0 followed by 0.
  - Nothing guards that.
- **MEASURED (g_r2r3.py).** decode3g.py's own no_pair_chance_ok and r2_own, lifted by name; side s = 1; 200 fair draws a case; halves of 2,000. Beside the gate, my "unguarded chance" is the chance of no two clicks in a row without s, by the same recursion with that state forbidden:

| clock | R2 NOT SHOWN | the gate | the unguarded chance a half (thousandths) |
|---|---|---|---|
| s at 175, the other at 175 (control) | 0 of 200 | reads (0) | 0 |
| s at 300, the other at 30 | 34 of 200 | reads (0) | 75 |
| s at 300, the other at 8 | 197 of 200 | reads (0) | 817 |
| s at 175, the other at 175, then 0 in the second half | 200 of 200 | reads (0) | 1,000 in the second half |

- **The text's own case shows the gap.** Its "gate's no" (s at 8, the other at 300) is the same clock read from its rare side. Read from its common side, it falls into the third row.
- **Also unsettled:** which sides of a clock R2 reads is not stated, and the code reads side 1 only.
- **Fix:**
  - Gate on every context rung 1 needs. Take the exact chance of no "11" plus the exact chance of no "00", both by the transfer recursion (mine for "00": a' = (e + a + b) m1 + a n0, b' = (e + a) m2 + b n0). Read R2 where the sum is at most 1/20.
  - Bound the higher rungs as (e)'s ladder gate does.
  - Say that R2 is read for every side.

**B2. R4's click parts pass an outcome fixed nine times in ten by the place's own setting two events back** (section 3, lines 338-345; settled item 4).

- **Why it breaks.** The joint past (R2's ladder) refuses only an outcome that its context fixes exactly. The own-past-settings 2 x 2 reads lag 1 only.
- **MEASURED (g_r4.py).** decode3g.py's own r4c, to_clicks and from_clicks, lifted by name; 40,000 pair events; the toy's hand. The record is "two back" as decode3g.py makes it, with A's outcome flipped at each event with chance 100 per 1,000:
  - the click parts read SHOWN, and every part is SHOWN except the three named NOT READs;
  - the joint past reads [8, 32, 328, 1,038] and [8, 32, 341, 1,110] at A;
  - S is 2,499; R4 reads NOT READ, only by the seeds' law;
  - yet A's outcome against its setting two back has counts [2,016, 17,873, 18,210, 1,899], z^2 25,870,898 against CUT_FW 10,674.
  - Flipped 200 per 1,000 it reads the same way, with z^2 14,670,076.
  - Unflipped, the joint past refuses it, as the text says.
- **So line 344 is false:** "its reach ... a dependence deeper than 8 pair events passes it". A partial dependence at depth 2 passes it too.
- **This blocks because** R4's click parts are settled for the build. Once the seeds' law exists, R4 would read the choice on such a record.
- **Fix:**
  - Read each place's outcome against its own settings, and against its own outcomes, at lags 2, 4 and 8, beside lag 1, each a 2 x 2 counted in N_T.
  - Correct the reach sentence.

## MINOR

1. **(3p): the code against the text** (line 256; my DECODE3f MINOR 1).
   - The text says (3p) reads NOT READ where y moves, "with no effect on R3". But decode3g.py's r3 appends that NOT READ.
   - MEASURED (g_r2r3.py, part 2): THIRD7's member at the click world's dial, y swinging between 80 and 120 thousandths of 3D, halves of 8,000, three lays. R3 reads NOT READ with (3b), (3d) and (3e) all SHOWN, and SHOWN without (3p).
   - Met in the text, not in the code. Fix the code before the build.
2. **(3b)'s level at steady 175** (64 per 1,000, two errors above). Named OPEN, so a rule marked settled does not yet meet its level. Its per-K cuts are routine whole-number work: chi-square on K degrees, upper and lower tails apart, Poisson sums for even K. The Boss may let the deriver do it.
3. **The ladder's share is spent per rung** (lines 376-381; my DECODE3f MINOR 5).
   - order_e and joint_past gate each of the four rungs at the full share 5/N_T. To first order a ladder can then cost four shares, not one.
   - Sum the rungs' bounds against the share, or give each rung a quarter. In practice the L = 8 rung dominates.
4. **The interval rule's reason reads rounds** (line 430). "Within one of its rate times the window, a balanced word" is a board premise, under the 09:5x ruling.
   - The click-world reason is that an event lies between two of the clock's own lines, so each own-count reading is within one of the event's own time.
   - The DERIVED no-false-refusal holds on that reason, with no steady rate needed. State it so.
5. **D4's check** (lines 418-427; my DECODE3f MINOR 6). Its "allowed" case compares C-a's own-count form with itself, so it cannot fail. The computed no (11 against 7) is a mutation test of the code. Name D4 a static check that no reading takes a round or face field, with the mutant as its no.
6. **The pair record** (lines 316-323).
   - The probe's lines carry a "pair" field that points into a separate table of bearing meetings, and no side joins that meeting to any line.
   - Under rule 5 (two levels, lines and sides), say how the naming sits in lines and sides, or name the field for writer C and the owner.
   - "Read back from the lines alone" also reads that table.
7. **The pair's curve** (lines 328-330) is read only at the two angle differences the settings give, 30 and 90 degrees. Name that reach.
8. **"A clock with one side"** is read from the board's passing over the whole record. Read it from the record per half. A side that stops in one half is caught by B1's fix.
9. **The tree's archive digest and the interpreter.**
   - 255fa1b9 is not reproduced by GNU tar or Python tarfile under any variant of "sorted by name, mtime 0, owner 0". Name the exact command, or cite FROZEN.sha256's per-file sums, which do pin the tree.
   - The probes ran under 3.13.17, not the ruled 3.14. My 3.14 reruns are byte for byte, so this is immaterial here; name it.
10. **The free-lay control** reads S 0.14 to 0.28. A deterministic local control at S = 2 would test (a)'s cut at its edge (optional).

## SOUND, with numbers

- **The cuts.** By my independent method (erf's Kummer series, Euler's pi, each value bracketed), every cut is the least whole thousandth whose tail is at most its level: True at C, False at C - 1.
  - C1 6,961, C2 9,575, C4 13,696;
  - CUT_FW 10,674 at N_T 46 and 11,103 at 58.
  - One convention; the cuts come from READINGS; none is computed at read time.
- **R3's family.**
  - The union bound holds whatever the dependence.
  - The carried bound's gate sits at C1, so the theorem holds with one cut, and K_MIN is 20.
  - The two-values share is 3 e^(-10) = 0.14 per 1,000 a half.
  - The rates on 1,000 records a case are 64, 44, 54 and 45 per 1,000 (one error is 6.9). Carried sides read 0 SHOWN. THIRD7's member reads NOT SHOWN by (3e) at C4.
- **R2.** Its transfer recursion is exact for its own event (n0 + m1 + m2 = D^2 a round). NOT READ on one side is DERIVED.
- **R4 under (C).**
  - It reads NOT READ by name until the seeds' law exists.
  - All nine of DECODE3g's drawless rows are refused by named parts.
  - The free-lay control reads at most 2.
  - N_T = 2 (17 + 6 S) = 46 and 58.
  - The gate's (P) bound is sound: e^(-E) (1 + 3 E) covers P(N <= 1) <= e^(-E) (1 + e E) for independent or negatively associated indicators. exp_neg_up is a valid upper bound.
  - The gate opens between 2,300 and 2,400 a half.
- **The conversions.**
  - The interval rule's logic holds: a right record's true products lie in both intervals.
  - "Deeper" read only past the grain (p >= q + 2) is sound.
  - C-e's interval form is as I gave it.
  - The configuration table is reproduced.
- **The rest.** One key per record through D = (kappa div senses) K, and one precedence (worst) at every level.

## DERIVED / MEASURED / OVERCLAIMED

- **DERIVED, sound:** R2 NOT READ on one side; the recursion for its event; R3's union bound and the carried no at the moved gate; the two-values share; the interval rule (on the click-world reason); C-e having no whole solution.
- **MEASURED:** the text's tables, reproduced. Mine:
  - R2 refusing right records behind its gate (34, 197 and 200 of 200);
  - R4's click parts passing a nine-in-ten two-back;
  - R3 on a moving W reading NOT READ in the code;
  - the cuts.
- **OVERCLAIMED:**
  - the gate as R2's power ("the gate reads that from the passing");
  - the joint past's reach;
  - "(3p) ... with no effect on R3" (in the code);
  - "read back from the lines alone".

## My DECODE3f items

- **B1 (R2 where the passing moves): met in its measured form.** One side reads NOT READ, and two sides sit behind an exact gate. But the gate is one-sided: B1 here.
- **MINOR 1 ((3p)): met in the text, not in the code** (MINOR 1 here).
- **MINORs 2, 3, 4, 7, 8 and 9: met.**
  - 4: (c) is gated on a click reading, with its cost named (978 NOT READ at 2,000 a half).
  - 3: C-e is in the interval form.
- **MINOR 5: met in form,** with the per-rung share left (MINOR 3 here).
- **MINOR 6: met in part** (MINOR 5 here).
- **The four conditions on R3's family: met.** Steady 175's excess is named.

## Questions for the Boss

1. Should R2's gate be the two exact chances ("11" and "00") summed to at most 1/20, or (e)'s ladder gate on R2's own-count contexts?
2. Should R4 add lags 2, 4 and 8 to the own-past 2 x 2s, counted in N_T, or name partial dependence as beyond R4's reach?
3. May the deriver tabulate (3b)'s per-K two-tailed cuts in whole numbers now, or are they Big Pic's?

## Solution24 (the reader's line)

The decoder's settled rules now read in the clicks, with one cut convention and one precedence. Two of them still misread records their names exclude: R2's gate and R4's joint past. Each has a counted, whole-number fix before the build.
