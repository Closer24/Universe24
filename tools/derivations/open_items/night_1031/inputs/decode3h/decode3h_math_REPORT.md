<!-- Boss note, 2026-10-31 10:16 UTC: written by the Boss from the reader's hand-back (the harness refuses report files from readers); the text below is the reader's, whole. Reader of DECODE3h (frozen 7f7d3d63), the hostile mathematician (the HALF pair's mathematician). -->

My harness does not let me write report files, so the whole report is below for the Boss to file as S/decode3h_math/REPORT.md. My probes and their outputs are in that folder: h_r4, h_cuts, h_b3low and h_d4, each a .py with its .txt, plus rerun/ with its math_* files.

# The hostile mathematician (HALF pair) on DECODE3h, 2026-10-31

**Read:**
- BRIEF_PAIRS.md from the 08:4x section to its end, including the owner's answers of 09:30, his law of 09:04, DECODER-CUT, and the coordinator's added point (#2187, 6541948938 and 6541964934).
- DECODE3h.md, all 461 lines; sha256 7f7d3d63..., as named.
- decode3h.py, cuts3h.py, readings3h.json, nl.sha256.
- My DECODE3g report as filed.

**Checks of the frozen folder:**
- All 80 files check against FROZEN.sha256.
- Section 0's 19 quoted rulings are all verbatim against the brief (checked mechanically).

**Reruns:** from a copy of the frozen folder (decode3h_math/rerun/), under the live venv's Python 3.14 -I with nice 19 and the load near 3. decode3h.py reproduces decode3h_run1.txt byte for byte, and cuts3h.py reproduces readings3h.json byte for byte.

I touched no repository or worktree, did not open the other reader's folder, and posted nothing.

## VERDICT on DECODE3h: NOT PASSED (one BLOCKING)

## BLOCKING

**B1. R4's order readings presume a law from the start: an outcome fixed by the place's own later setting passes every click part** (section 3: the lag tests, lines 284-296; the seeds' law's constraint, lines 328-330; settled item 4).

- **Why it breaks.** Every R4 test that crosses pair events looks backward, except one.
  - The 14 lag tests pair each outcome with the place's own setting 1, 2, 4 or 8 events *before*, and with its own outcomes, which pair the same either way.
  - The joint past reads only earlier contexts.
  - The five 2 x 2s reach one event *ahead* (setting t + 1 against outcome t), and no further.
  - Nothing pairs an outcome with a setting 2, 4 or 8 events later, and nothing pairs it with the far place's settings beyond one event in either direction.
- **MEASURED (h_r4.py).** decode3h.py's own r4h, lifted by name; 40,000 pair events; settings from the toy's own turned teeth; the hand carried at the triangle's share as in "two back". These are test records, never an act.

| A's outcome is | the click parts | A's outcome against the named setting, z^2 (CUT_FW 11,452) |
|---|---|---|
| its own setting 1 event later | NOT SHOWN, by the 2 x 2 | 39,992,000 |
| its own setting 2 events later | SHOWN, every part | 39,992,000 |
| its own setting 4 events later | SHOWN, every part | 39,992,000 |
| 2 events later, flipped 1 in 10 | SHOWN | 25,854,959 |
| 2 events before ("two back", control) | NOT SHOWN, as the text has it | - |

- **Two of the text's sentences are therefore false.**
  - The seeds' law's constraint: "the order readings refuse any dependence across pair events ... within each pair event only".
  - The corrected reach: it names deeper past lags and past joints, but not later settings, which pass even when they fix the outcome.
- **Why it matters now.** The owner put the end form first ("Bell from the end feels closer to nature", 09:33). He also asks of Bell "from the past and also from the future", and his own definition of the choice is "not its past and not the future".
- **Fix:** read the order both ways.
  - Read each place's outcome against its own settings L events later as well as before, at L = 1, 2, 4 and 8.
  - Read it against the far place's settings at lags beyond one, both ways, or name that reach.
  - Read a joint future beside the joint past: the same function run on the reversed record.
  - Count all of it in N_T.
  - A smaller form suits DECODER-CUT. Per place and per half, replace the 14 lag 2 x 2s with three sums of the lag z^2:
    - the outcome against its own settings at lags -8 to -1 and 1 to 8, on 16 degrees;
    - against its own outcomes at lags 1 to 8, on 8 degrees;
    - against the far place's settings at lags -8 to 8 except 0, on 16 degrees.
    Each sum is cut at the chi-square on its degrees from the readings file (the Poisson sum, as for (3b)). That is fewer tests and fewer lines, and it covers every lag both ways, lags 3, 5, 6 and 7 included. Today "three back" flipped 1 in 10 still reads SHOWN (h_r4.py), at the reach the text names.

## The coordinator's question: is a reading that is NOT READ on 966 of 1,000 right records a reading that can fail?

- **At 2,000 events a half it can fail, but it cannot pass.**
  - worst() over R4's parts gives NOT READ whenever the summed ladder gate is closed, and the gate is closed on every record of that length.
  - So the click parts there read only NOT READ (966) or NOT SHOWN (34). Its NOT SHOWN side works at any length; its SHOWN side does not exist there.
  - The text's "34 of 1,000, within 5 per cent" is therefore the rate of four parts that are read, not the rate of the reading.
- **Where the gate opens, it is a two-sided reading.**
  - MEASURED (h_r4.py, decode3h's own right_pairs and r4h, 1,000 right records at 3,000 events a half): SHOWN 963, NOT SHOWN 37, NOT READ 0.
  - The 37 by part: own past at the lags 20, the curve 6, (c) 5, the 2 x 2s 4, (e) 2.
  - The summed gate opened on every record; (c) went unread only where (e) failed first (2 records).
  - So the owed rate now stands at 37 per 1,000, within the 5 per cent family.
- **Fix:** name the length where R4's click parts can first read SHOWN (the summed gate opens between 2,000 and 3,000 a half). Below it, call R4 "refusing only". Cite the rate where it is read.

## MINOR

1. **D4's static check reads only subtraction nodes** (section 4). MEASURED (h_d4.py, decode3h's own d4_static): a round difference written as `take + -give + -b2 + b1` reads "allowed", and so does `sum((take, -give, -b2, b1))`. Read D4 on the conversions' inputs (no round or face field reaches one), or on every arithmetic node over such a field. Let its no include the negated mutant.
2. **nl.sha256 does not verify on the frozen folder.**
   - `sha256sum -c nl.sha256` fails 3 of 41. The failures are the 3.14 .pyc files in nl/'s __pycache__, which the probes' own runs rewrote after the pin; FROZEN.sha256, made later, matches.
   - The same cause explains DECODE3g's irreproducible archive digest.
   - Fix: pin the sources only (no __pycache__), and run with -B, so that no run writes into the frozen tree.
3. **R3's place under the owner's Q11 answer.**
   - The record holds lines and sides, q alone, so the board's passing that (3b), (3d) and (3e) read is not in it.
   - R3 is named a board check (section 7), yet it is listed among the decoder's settled items (6.2).
   - Fix: build it with the board checks that read the board's own state, as section 5 does for R2's passing-given chance, not in the record's decoder. That also takes its lines out of the decoder's count.
4. **The free-lay control.** Both places read one member's W, with alike births: a shared past, the strongest local case. Say so.
5. **DECODER-CUT: which rules are small enough to build.** Sizes are counted in the probes' own functions, with blank, comment and docstring lines left out. The decoder is at 605 lines against a target of 338 (the Node-clock).

| rule | probe lines | weight |
|---|---|---|
| one precedence (worst, halves) | 9 | build now; likely a net cut, replacing per-reading precedence |
| one key per record | 6 | build now |
| one cut convention and the readings file | data, a few lines | build now; removes computed cuts |
| D4 | 10 | a test of the decoder's code; no decoder lines |
| R2 | 82, of which 41 are the ladder gate shared with R4 | buildable only with a cut of its size |
| R3 | 95 | goes to the board checks (MINOR 3); zero decoder lines |
| R4's click parts | 138 | hold: NOT READ by name until the seeds' law, and B1 is open |
| R4's record parse and mates | 30 | hold, with R4 |
| the interval rule | 7 | hold: C-a to C-e are OWED, so it has no caller |

   - The settled readings total about 367 lines, more than the whole target. So nothing beyond the first four rows enters before the decoder's cut.
   - B1's sum form shrinks R4 when it does enter.

## SOUND, with numbers

- **R2's gate is exact.**
  - Over C(N, n): no "11" is C(N - n + 1, n), no "00" is C(n + 1, N - n), and no "10" and no "01" are 1 each.
  - Their sum bounds rung 1's failure, since rung 1 fails exactly where one of the four is missing. The higher rungs are added in. It is read at 1/20, for every side, and per half from the record.
  - The text's 0 disagreements against the transfer recursion are reproduced.
  - My rows that refused 34, 197 and 200 of 200 now refuse none.
- **R3 at the per-K cuts.**
  - My independent method (even K: the Poisson tail series; odd K: the Kummer form P = sqrt(2x/pi) e^(-x/2) SUM_(n >= m) x^n/(2n+1)!!, squared; Euler's pi) gives every [lo_K, hi_K] for K = 20 to 39 as cited, 0 of 20 off, and CUT_FW 11,452 and 11,746 likewise.
  - The rates are 50, 40, 51 and 33, and (3b)'s share is 13 to 19 against 16.7.
  - My worry that the chi-square's per-window variance of 2 is light where few landings fall was overturned by measurement (h_b3low.py). The exact variances are 2.156, 2.117 and 2.091, yet (3b) reads 18, 18 and 16 per 1,000 at 5.1 landings, 6.4 misses and 7.7 landings a window.
  - The carried no at the lower cut holds: Z < B <= lo_K. Carried sides read 0 SHOWN.
  - R3 on W and (3p) are off the settled list, and the code's r3 takes no (3p).
- **R4.**
  - The partial "two back" flipped 1 in 10 and 2 in 10 is refused (z^2 12,883,246 and 7,137,608).
  - A ladder's share is spent once.
  - The local act at the bound reads S 2,000 and (a) NOT SHOWN, so the control can fail.
  - The pair record is written in lines and sides alone, and the mates read.
- **The rest.** The interval rule has its click-world reason. "Two rates" is right. Chain rule (i) is in force. R2's context under Q10 is named for Big Pic.

## DERIVED / MEASURED / OVERCLAIMED

- **DERIVED, sound:** rung 1's closed forms and their sum; the carried no at the lower cut; the chi-square CDF forms; the interval rule.
- **MEASURED:** the text's tables, reproduced. Mine:
  - R4's click parts SHOWN on outcomes fixed 2 and 4 events ahead;
  - R4's rate where the gate opens (963 and 37);
  - (3b) at few expected landings a window;
  - D4's evasion;
  - nl.sha256's 3 failures.
- **OVERCLAIMED:**
  - "the order readings refuse any dependence across pair events";
  - the reach sentence, which omits later settings;
  - "34 of 1,000" read as R4's rate;
  - "nl/ is pinned by nl.sha256".

## My DECODE3g items

- **B1 (R2's one-sided gate): met.** All four rung-1 contexts are covered, exactly, every side is read, and my rows refuse none.
- **B2 (the partial two-back): met.** The lag tests refuse it. B1 here is its mirror, the future.
- **MINORs 1 to 8 and 10: met:**
  - (3p) is out of the code's R3;
  - (3b) has per-K cuts;
  - the ladder's share is spent once;
  - the interval rule has its click-world reason;
  - D4 is static (MINOR 1 here);
  - the pair record is in lines and sides;
  - the curve's reach is named;
  - one side per half;
  - the control at S = 2.
- **MINOR 9: met in form.** The per-file sums replace the archive digest, and the interpreter is 3.14.6, but the pin is stale (MINOR 2 here).

## Questions for the Boss

1. Should R4 read the order both ways, by the three sums on 16, 8 and 16 degrees, or by forward 2 x 2s at 2, 4 and 8 plus a joint future?
2. Does R3 leave the decoder for the board checks, the record holding q alone?
3. Under DECODER-CUT, should the precedence, the key and the readings file go in now, with R2 waiting on a cut of its size?

## Solution24 (the reader's line)

R2 and R3 now stand at their levels, and R4 refuses every drawless form named from the past. It must read the future too, as the owner's Bell from both ends asks. The decoder's cut decides which settled rules enter first.
