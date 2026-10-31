<!-- Boss note, 2026-10-31 11:06 UTC: written by the Boss from the reader's hand-back (the harness refuses report files from readers); the text below is the reader's, whole. Reader of DECODE3i (frozen cf5e6eed), the hostile mathematician (the HALF pair's mathematician). -->

Reader of DECODE3i (frozen cf5e6eed...), the hostile mathematician (the HALF pair's mathematician). My harness does not let me write report files, so the whole report is below. Please file it as S/decode3i_math/REPORT.md.

The probes are in S/decode3i_math/, each p_*.py with its .txt output. That folder also holds rerun/ (the copy of the frozen folder) and nf/ (node-fold's decoder/, taken by git archive).

# The hostile mathematician (HALF pair) on DECODE3i, 2026-10-31

**Read:**
- BRIEF_PAIRS.md to its end (line 1139). I read the 10:42 ruling last; see B1.
- DECODE3i.md, all 369 lines. Its sha256 is cf5e6eed21e131c7..., as named.
- decode3i.py, cuts3i.py, readings3i.json and nl_sources.sha256.
- My DECODE3h report as filed.

**Checks of the frozen folder:**
- FROZEN.sha256: 78 of 78 OK.
- nl_sources.sha256: 35 of 35 OK. Its own sha256 begins c7aeafde6109e3ff, as cited. Remade by the text's command, it gives the same bytes.
- After every one of my runs, no .pyc or __pycache__ appeared in the frozen folder or in mine, and the copy still read 35 of 35.
- Section 0's 12 quoted blocks are verbatim in the brief (checked mechanically).

**Reruns:** from the copy, under the live venv's Python 3.14.6 -I -B, nice 19, with the load between 1.7 and 3.3.
- decode3i.py reproduces decode3i_run1.txt (= run2), 12,272 bytes, byte for byte, in 4 min 38 s.
- cuts3i.py reproduces readings3i.json byte for byte.

I touched no repository or worktree (git show, git archive and git log only). I did not open the other reader's folder, and I posted nothing.

VERDICT on DECODE3i: NOT PASSED

(one BLOCKING)

## BLOCKING

**B1. R4 does not read a law that fixes an outcome from both sides at once, or through the far place's settings jointly.** Four exact laws pass every click part. This touches section 1 (the joints, the reach, the seeds' law's constraint) and the "What changed" line "R4 reads the order both ways".

- **Why it breaks.**
  - The joint past and the joint future each read the place's own context on one side only. Neither holds the setting before and the setting after together.
  - The far place's settings enter one at a time (the far lag sum). No joint holds two of them.
  - A parity of two fair settings is uncorrelated with each one, so the lag sums cannot see it, by design.
- **MEASURED (p_r4both.py, p_r4far.py).**
  - Both probes run decode3i's own r4i, rec_by_settings and joints, executed from the copy.
  - 40,000 pair events, 20,000 a half, settings from the turned teeth.
  - These are test records, never an act.
  - In the table, the joints' numbers are the ambiguous contexts per rung, with AMBIG 2.

| A's outcome is (exact, no draw) | R4's click parts | largest lag sum, first half (cut 39,697) | the probe's joints |
|---|---|---|---|
| the parity of its own setting 1 event before and 1 after | SHOWN, every part | A far settings 22,939 | both ways at the place: NOT SHOWN [0, 0, 0]; both places both ways: NOT SHOWN [0, 0] |
| the same, 4 before and 4 after | SHOWN, every part | A own settings 32,012 | both ways at the place: NOT SHOWN [32, 512, 0] |
| the parity of B's two previous settings | SHOWN, every part | A own settings 21,174 | both ways at the place: SHOWN; both places: NOT SHOWN [128, 0] |
| the parity of B's setting 1 before and 1 after | SHOWN, every part | A far settings 14,178 | both ways at the place: SHOWN; both places: NOT SHOWN [0, 0] |
| control: the toy's third click | SHOWN | B own settings 18,512 | both SHOWN ([32, 512, 733]; [256, 3431]) |

  - On the first row, the joint past and the joint future at A both read [8, 16, 64, 1024], SHOWN.
- **The far-place laws are signals.** B's choice of two equal settings sets A's next outcome. (c) reads the same event only, and the order readings miss the joint.
- **So these sentences are false:**
  - "R4 reads the order both ways", read as the 10:13 ruling's "so that it reads a law from the start, the end or both".
  - The constraint: "the order readings now refuse, within that reach and both ways, any dependence of an outcome on another pair event's settings or outcomes. So the seeds' law may couple the settings to the hand within each pair event only, as far as eight events either way can tell."
  - The reach names partial joints only, not exact two-sided or two-place ones.
- **Why it matters now.**
  - The owner's 10:37 line ("the start point and the end are fixed in advance") is a law laid at both ends.
  - The coordinator's press point: R4 must read a law from the start, the end or both.
- **The brief, to its end.** I measured these four laws before I read the brief's last section. That section is the 10:42 ruling, from the physicist's DECODE3i report (Q1: the two-sided joint ladder at L = 1, 2 and 4). My joint_both is that form:
  - It refuses rows 1 and 2 and passes the toy.
  - Its summed gate first opens at 2,500 a half, as the one-sided gates do (p_fixrate.py).
  - It reads SHOWN on 200 of 200 right records at 3,000 a half (p_fixrate.py).
  - But it passes both far-place laws: SHOWN at both places in both halves (p_ruled.py).
  - So the ruling meets B1's first half, not its second.
- **Fix for the second half, either:**
  - **Add a joint of both places both ways.**
    - Per place, the context is the L events before and the L events after. Each event carries its own setting, its own outcome and the far place's setting, with the present own and far settings beside them.
    - L = 1 and 2, 8 symbols an event, the same summed gate (qexp 6L + 3), counted in N_T.
    - MEASURED: it refuses rows 1, 3 and 4 and passes the toy. It reads SHOWN on 200 of 200 right records at 3,000 a half, and its gate first opens at 900 a half (p_fixrate.py).
    - With the ruled ladder, both counted per source and place, N_T = 2 (21 + 12 S): 66 or 90.
  - **Or name it:** say that an exact law on the far place's settings jointly passes, and correct the constraint to match.
- **The reach still to be named, either way.** Every partial joint passes. So does any exact law on a joint deeper than these windows: 8 events one way, 4 both ways at the place, 2 both ways across the places. MEASURED:
  - the one-each-way parity, flipped 100 per 1,000, passes every part and both probe joints ([32, 339, 1125]);
  - the physicist's parity of the next two, flipped 100 per 1,000, passes every part (lag sum 36,179).

## MINOR

1. **The NOT READ length is a single number only for one source with fair settings** (sections 2 and 7).
   - MEASURED (p_gate.py, decode3i's own ladder_gate; the joint ladders' summed gate first opens at):
     - one source, fair, N_T 58: 2,500 a half (the text's, reproduced);
     - two sources, N_T 74, each source's sub-record half the events: 5,000;
     - settings 700 / 300 at each place: 1,300;
     - settings 900 / 100: 500 or less.
   - MEASURED (p_skew.py, decode3i's own r4i; 200 right records of the pattern each, at 1,300 a half):
     - settings 700 / 300: click parts SHOWN 16, NOT SHOWN 32, NOT READ 152;
     - fair settings: SHOWN 0, NOT SHOWN 9, NOT READ 191.
   - So "Below that length R4 is 'refusing only' ... never SHOWN" fails for skewed settings.
   - The rate where R4 reads is not one number either: 32 of 200 there, 30 of them from (a).
     - (a)'s reach is cut at the gap 2 sqrt 2 - 2: it reads where its radius is under 828 thousandths.
     - It is not cut at the pattern's own S of 2.5.
   - Fix:
     - read "refusing only" per record, from the gate on the record's own counts;
     - name 2,500 (one source, fair) and 5,000 (two sources) as cases;
     - cite the skewed case's early opening and its rate.
2. **D4 can be evaded four ways, and it refuses one honest form** (section 5).
   - MEASURED (p_d4.py: decode3i's own d4_static, unchanged, read on that file's conversions).
   - The test record: A's clicks [1, 4, 9], give 2, take 11; B's clicks [3, 5], b1 1, b2 8.
   - C-a on own counts gives 0; C-a on rounds gives 2.
   - The evasions, each allowed and each returning the rounds' value 2:
     - `own(range(BIG), take) - own(range(BIG), give) - (own(range(BIG), b2) - own(range(BIG), b1))`. own() of a made-up sequence returns the round itself.
     - the fields read through `locals()`;
     - the fields taken as `*f`;
     - the fields keyword-only.
   - The honest C-a written as `own(A_lines, r=take) - ...` is refused ("take reaches a keyword node"), though its value is 0.
   - Fix (a few lines over 15):
     - take every parameter kind;
     - let own()'s first argument be a lines parameter and its second a round parameter, positional or r=;
     - refuse every other name but own (a whitelist).
3. **R2 per clock shows its no only where no right record reads, and its many-valued form is not built** (section 4).
   - The carried 300 / 30 reads NOT SHOWN, but at 300 / 30 the fair draws are NOT READ 200 of 200.
   - MEASURED (p_r2.py, decode3i's own r2_lines and own_lines). I took the same 200 draws at 175 / 175, which reproduce SHOWN 124, NOT READ 76:
     - made refractory (a double never follows a double), they read NOT SHOWN 166, NOT READ 34. Of the 124 SHOWN, 116 now read NOT SHOWN and 8 NOT READ;
     - a double exactly every tenth click (640 clicks, 64 doubles a half) reads NOT SHOWN, with both halves read.
   - So R2 per clock can fail where it reads. The text should carry such a row.
   - "A clock whose q takes more values is read by the same ladder, its gate by the ladder bound alone" is not built.
     - r2_lines counts n = sum(seq).
     - ladder_gate takes a two-valued outcome (plus, minus).
     - Name it not built, or build it.
4. **The DECODER-CUT sizes are Sofer's rule on the probe's own functions, without the helpers they call** (section 6).
   - MEASURED (p_count.py, p_sizes.py). Counting lines that are neither blank, nor a comment alone, nor in a docstring reproduces Sofer's count on node-fold c360851c2's decoder/ to the file: records 254, shadow 205, sides 92, clicks 39, measure 15.
   - The same rule gives the text's six sizes exactly: 9, 6, 15, 67, 134 and 30.
   - R4's 134 leaves out chi2x2 (4), th (2), order_z2 (7) and ambiguous (5): 18 lines.
   - Its ladder gate (29 + 7) is counted under R2.
   - So R4 entering alone is about 188 lines in the probe's style, and R2 about 72.
   - B1's ladders add about 20 to 25 lines each.
   - Fix: name the sizes as estimates of the build, as the 10:42 MINOR 3 asks, with the helpers included.
5. **For DECODE3j: the brief moved after the freeze.**
   - Section 0 quotes the 10:13 strengths law line ("or is laid once at the start for each clock"). The owner's 10:34 word replaces it ("None is laid, not even once at the start for a clock").
   - The source heading for the owner's 09:33 word is shortened from the brief's; the quote itself is verbatim.

## SOUND, with numbers

- **The cuts.** My series, written apart from cuts3i and cuts3h:
  - even degrees: h_cuts's positive Poisson tail against the whole series of e^(x/2), bracketed;
  - one degree: the Kummer form with Euler's pi.
  - All six new cuts are the least whole thousandth (True at C, False at C - 1), 0 of 6 off:
    - 39,697 and 26,501 at N_T 58;
    - 40,421 and 27,114 at 74;
    - CUT_FW 11,103 and 11,555.
  - readings3h's entries are kept unchanged; CUT_FW gains 74 only.
- **The degrees are right for a right record.**
  - Each lag's z^2 is N r_L^2. For an outcome that leans on no other event, Bartlett's formula gives two covariances:
    - against the settings, Cov(r_L, r_M) = rho_xx(L - M) / N;
    - between a lag and its mirror, Cov(r_L, r_-L) = rho_0^2 / N, where rho_0 is the same-event correlation. rho_0 is 0 by fair marginals (own settings) and by no signal (far settings).
  - The teeth's settings are white in pairs. Their own lag sums at lags 1 to 16 are 18,120 and 11,281 at A, and 7,038 and 13,889 at B, against the cut 39,697.
  - The rate run's lag sums refused 12 of 1,000, against about 10.3 expected.
- **N_T** = 21 + 8 S per half, counted part by part against r4i.
- **The refusals,** all reproduced against the cut 39,697:
  - two ahead 20,011,437; four ahead 20,008,745;
  - two ahead flipped 12,874,224; three back flipped 12,737,663;
  - joint futures [8, 0, 0, 0] and [8, 32, 0, 0].
  - The toy's third click passes every click part, and R4 reads NOT READ by name.
- **The parity of the next two** is refused by the joint future alone. Its lag sum of 38,963 comes from the teeth's chance, not from the law:
  - A's first half has 9,849 ones in 20,000 settings, so the parity leans on each setting by 2p - 1 = -0.0151. Lags -1 and -2 read 4,624 and 4,534, against N (2p - 1)^2 of about 4,560.
  - Lag 7 reads 12,613. That matches the settings' largest three-at-a-time z^2 in that half (12,616), which does not recur in the second half (its largest is 5,357).
- **The joint future** is the joint past on the reversed record, with the same gate.
- **The rate at 3,000 a half** reproduces: 969 SHOWN, 31 NOT SHOWN, 0 NOT READ.
- **R2 per clock:** 0 NOT SHOWN in 1,600, reproduced.
- **D4:** the three named mutants are refused and C-a is allowed, in my harness too.
- **R3:** r4i reads no R3, and the record carries no passing.

## DERIVED / MEASURED / OVERCLAIMED

- **DERIVED, sound:**
  - the lag sums' cuts;
  - their degrees, under the two conditions above;
  - the joint future as the joint past on the reversed record;
  - N_T = 2 (21 + 8 S).
- **MEASURED:** the text's tables, reproduced. Mine:
  - B1's four laws (p_r4both, p_r4far);
  - the ruled ladder on the far-place laws (p_ruled);
  - the two probe joints on right records (p_fixrate);
  - the gate lengths (p_gate, p_skew);
  - R2's refractory and periodic rows (p_r2);
  - D4's four evasions (p_d4);
  - the cuts (p_cuts);
  - Sofer's rule and the sizes (p_count, p_sizes).
- **OVERCLAIMED:**
  - "R4 reads the order both ways", read as both ends at once;
  - the constraint "within each pair event only";
  - "refusing only below 2,500" as a general length;
  - the many-valued R2;
  - D4 read as holding a conversion to its own counts.

## My DECODE3h items

- **B1 (R4 reads the past only): met, as I asked it.**
  - The lag sums now read both ways, and the joint future stands beside the joint past.
  - All four of my forms are refused, and the toy passes.
  - My own fix was not enough: its joints read one side and one place at a time. That gap is B1 here.
- **The coordinator's 966 question: met.** The length is named only for one source with fair settings (MINOR 1).
- **MINOR 1 (D4 reads subtraction only): met.** Four other evasions remain (MINOR 2).
- **MINOR 2 (the pin): met.**
- **MINOR 3 (R3's place): met.**
- **MINOR 4 (the free-lay control's shared past): met.**
- **MINOR 5 (DECODER-CUT sizes): met.** The helpers are left out of the counts (MINOR 4).
- **My three questions:** ruled at 10:16, and applied.
- **Still OWED, as section 7 names:**
  - nl/'s commit. Its blobs enter git only in the Boss's input pushes (first 04b7385dd, 09:20 UTC), and node-fold c360851c2's records.py is a different blob;
  - C-b;
  - the click-form record and the key check in node-all's decoder.

## Questions for the Boss

1. B1's second half: should R4 add the joint of both places both ways (L = 1 and 2) beside the ruled two-sided ladder? Or should the text name that an exact law through the far place's settings jointly passes (a delayed signal), and correct the constraint to match?
2. Should "refusing only" be the gate's reading on each record's own counts, with 2,500 and 5,000 named as cases?
3. D4: the whitelist form, covering every parameter kind?
4. R2 per clock for a q of three or more values: build it in DECODE3j, or name it not built?

## Solution24 (the reader's line)

R4 now reads the past and the future, but only one side and one place at a time. An outcome tied to both ends at once, or to the far place's settings jointly, still passes. The cuts, the counts and the sizes are right. Once the joints reach both sides and both places, R4 can read Bell from the start, from the end, or from both.
