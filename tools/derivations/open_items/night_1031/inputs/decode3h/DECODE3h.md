# DECODE3h: the decoder's readings of the three clicks, eighth text

The Boss's deriver for the decoder, 2026-10-31, 09:4x to 10:1x UTC. **Status: DRAFTED, for DECODE3's pair.**
- It folds both NOT PASSED reports on DECODE3g:
  - scratchpad/decode3g_math/REPORT.md, two BLOCKING;
  - scratchpad/decode3g_phys/REPORT.md, two BLOCKING.
- It applies the Boss's rulings of 09:3x (second part), 09:5x (both parts), 10:0x (both parts) and 10:1x UTC, and the
  owner's answers of about 09:4x UTC. Section 0 quotes each verbatim with its source.
- The decoder's rules are ours to build (the 10:0x ruling, second part). This text states them settled. What stays open
  is named Big Pic's, under the owner's word of about 09:05 UTC.
- DECODE3g.md (574 lines, sha256 083032b01ac5ada0...) stands as frozen, with its section 0. This text replaces only the
  lines it names, by DECODE3g's line numbers. Every other rule of DECODE3g, DECODE3f and the texts beneath them is kept.

**Files** (scratchpad/decode3h/).
- The copies: bp/, nl/, st1/, st2run_1/, st2run_2/, and decode3e.py, pair_order.py, decode3f.py and decode3g.py, all
  copied from decode3g/.
- **The tree**, nl/, is pinned by its per-file sums, nl.sha256: 41 files, the file's own sha256 18ecd64044cd25d2....
  - The command: `find nl -type f | LC_ALL=C sort | xargs sha256sum > nl.sha256`.
  - DECODE3g's archive digest (255fa1b9...) came from `tar --sort=name --mtime=@0 --owner=0 --group=0
    --numeric-owner -cf - nl | sha256sum` (GNU tar). The mathematician could not reproduce it; the per-file sums pin
    the tree in its place.
  - Its commit is still not named in the frozen texts: OWED.
- **The interpreter:** the live venv's Python 3.14.6 (scratchpad/live/.venv/bin/python -I), as the 08:5x ruling asks.
  DECODE3g's runs were under 3.13.17; both readers' 3.14 reruns of them were byte for byte.
- **The probes:**
  - cuts3h.py writes readings3h.json, the readings file. It holds (3b)'s per-K cuts, CUT_FW for 46, 58, 70 and 82
    tests, C2 and C4, and the readings' constants. It is computed once, never at read time.
  - decode3h.py (decode3h_run1.txt = decode3h_run2.txt, byte for byte) reads every cut from readings3h.json and checks
    them in its section G.
- **Conduct:** whole numbers only, with Rule3's carry the one division. No //, %, float, true division, math or random.
  Paths go by joinpath; one process at a time under nice -n 19; the load was read first.

Stand-in numbers are a stand-in's; board numbers are board runs; hand-built and test formats test a rule's logic, never
a world. No sentence here puts light or matter on the board, and no click reading here reads a tooth.

## 0. The rulings this text applies, verbatim, with their sources (the 09:4x and 09:1x rules)

DECODE3g's section 0 stands, its eight quotations unchanged. These are added:

From the brief, "The Boss's rulings, 09:5x UTC, second part (from DECODE3g's physicist; the owner's word on ALG2)":

> - R2's gate is taken from the clock's own counts (the exchangeable chance, given the half's N clicks and the n with side
>   1, that no two side-1 clicks stand in a row), so R2 is a click reading by the 09:5x rule; the passing-given chance
>   stays beside it, named a board check.

From the brief, "The Boss's rulings, 09:5x UTC, second part (from DECODE3g's physicist; the owner's word on ALG2)":

> - R3 on W, with (3p), leaves the settled list (10:1x, rule 5): a bench reading of the member, Big Pic's. DECODE3f's W
>   field is struck from the writers' list.

From the brief, "The Boss's rulings, 09:5x UTC, second part (from DECODE3g's physicist; the owner's word on ALG2)":

> - The free-lay control is the ruled member born at the middle, with a local act at the bound (S = 2 exactly) beside it,
>   so that the control is a test that can fail.

From the brief, "The Boss's rulings, 09:5x UTC, second part (from DECODE3g's physicist; the owner's word on ALG2)":

> - The chain rule in force is variant (i), "strictly later" (09:3x, second part).

From the brief, "The Boss's rulings, 09:5x UTC, second part (from DECODE3g's physicist; the owner's word on ALG2)":

> - A significance level (a chi-square point, a family-wise level) is a convention of the test, named before the reading,
>   fixed for every reading and never moved to get a result; it is no number of the act or the world, and no pick.

From the brief, "The Boss's rulings, 09:5x UTC, second part (from DECODE3g's physicist; the owner's word on ALG2)":

> - With the teeth out of the record, the checks that read teeth (K1's birth check, F1's teeth ranges, the twins' board
>   halves) read the board's own state, as code checks (writer I, node-rec).

From the brief, "The Boss's rulings, 10:0x UTC, second part (from DECODE3g's mathematician, with its physicist)":

> - R2's gate is read from the clock's own counts and covers every context rung 1 needs: the exact chance of no "11" and
>   of no "00", by the transfer recursion on the clock's own counts, summed and read where the sum is at most 1/20; the
>   higher rungs bounded as (e)'s ladder gate; R2 read for every side. The passing-given chance stays beside it, a board
>   check.

From the brief, "The Boss's rulings, 10:0x UTC, second part (from DECODE3g's mathematician, with its physicist)":

> - R4 adds each place's outcome against its own settings and against its own outcomes at lags 2, 4 and 8, beside lag 1,
>   each a 2 x 2 counted in N_T; the reach sentence is corrected (a partial dependence at depth 2 is refused).

From the brief, "The Boss's rulings, 10:0x UTC, second part (from DECODE3g's mathematician, with its physicist)":

> - (3b)'s per-K cuts (two tails, whole numbers, Poisson sums for even K) are a test's convention computed from its law:
>   the decoder's writer tabulates them now. They are not Big Pic's.

From the brief, "The Boss's rulings, 10:0x UTC, second part (from DECODE3g's mathematician, with its physicist)":

> - A ladder's share is spent once: the rungs' bounds sum against the share.

From the brief, "The Boss's rulings, 10:1x UTC (from ALG2's physicist, MIRACLE_B2's mathematician and UNC2's physicist)":

> - Rule 5 (the record has two levels, lines and sides) withdraws NATURE1's writer item 6 (W in the record apart from the
>   sides). The third click is read only by a reading the first click's record fails: OPEN, Big Pic's.

From the brief, "The Boss's rulings, 09:3x UTC, second part (from NATURE3's physicist)":

> - The click world's order is "strictly later" (rule (t), the 07:5x words): two meetings of one clock in one round are
>   simultaneous in its own lines and unordered. Rule (s), a chain passing within one round, is a board check of the
>   act's one-round reach (at most two Meshes in one round, AUDIT2's B7), named so. On the mesh world the split is
>   114 / 62 / 187 under (t).

From the brief, "The Boss's rulings, 09:5x UTC (from UNC2's and MASS2's mathematicians)":

> - A reading that fixes a board quantity under a board premise (a steady passing, a known lay) is a board check beside
>   the click reading, never a click reading. A click reading uses the clicks alone, with no board premise.

From the brief, "The Boss's rulings, 10:0x UTC (from LIGHT3's physicist, MASS2's physicist and STOP1)":

> - An observer of the echo needs own meetings: a clock with no own meeting in the whole record has no count (FACE2), so
>   it is no A and no B. The echo rule requires own meetings of A and B, or names per train that it admits clocks with no
>   count.

From the brief, "The owner's answers, about 09:4x UTC", the Boss's rulings with them:

> - The echo rule is not built to print SHOWN: at the file's key on 250 rounds it reads SHOWN with no reflector, from the
>   uniform relay (LIGHT3's mathematician, B1). Rule L and the per-clock cone are settled build items for the decoder.
>   A cut on the sizes of q is lawful only when it comes from the structure; any other cut is a pick (Big Pic's).

From the brief, "The owner's answers, about 09:4x UTC", the Boss's rulings with them:

> - A text cites every ruling verbatim with its source: the brief's section, a post's number on the thread, or "the
>   owner's word relayed by the Boss at HH:MM".

From the owner's answers, about 09:4x UTC (the Boss's translation), in the brief:

> 1. "Approved": a clock reads only its own clicks (Q10). Its sides and the board are not "what a clock can read".

From the owner's answers, about 09:4x UTC (the Boss's translation), in the brief:

> 2. The teeth go out of the record entirely (Q11): the record writes lines and sides, q alone; no tooth, birth or end
>    tooth is written. The engine keeps its teeth; the code checks that read them read the board's own state.

From the owner's answers, about 09:4x UTC (the Boss's translation), in the brief:

> 4. The three silent worlds (the bang, the live world, the well) "out".

## What changed

- **R2's gate is read from the clock's own counts**, so R2 is a click reading (phys B1).
  - The gate covers every context rung 1 needs: the exact exchangeable chances of no "11", no "00", no "10" and no
    "01", by the transfer recursion's closed forms.
  - The higher rungs' first-order bounds are added in. R2 is read where the sum is at most 1/20 (math B1).
  - R2 is read for every side. The passing-given chances stand beside it, a board check.
- **(3b) is read against the chi-square on K degrees**, two tails per K, from the readings file.
  - R3's rate on 1,000 right records a case is now 33 to 51 per 1,000.
  - R3 on W, with (3p), leaves the settled list for Big Pic's bench (phys B2). (3p) no longer touches R3's verdict, in
    the code too (math MINOR 1).
- **R4 reads each place's outcome against its own settings and its own outcomes at lags 1, 2, 4 and 8**, each a 2 x 2
  counted in N_T. "Two back" flipped one time in ten or two in ten is refused (math B2).
- **R4's free-lay control is the member born at the middle**, with a local act at S = 2 exactly beside it.
- **The pair record is written as meetings on both sides**, the bearing meeting included, in lines and sides alone.
- **A ladder's share is spent once**, its rungs' bounds summed.
- **D4 is a static check**, with the mutant as its no.
- **The interval rule takes its click-world reason**, and "deeper" is read as "two rates" with its premise named.
- **The chain rule in force is (i)**, "strictly later".
- **The owner's 09:4x answers are placed against the decoder's rules** (section 5).

## Each reader item, with DECODE3g's line, and how it is met

| Item | DECODE3g's line | How it is met |
|---|---|---|
| Math B1: R2's gate guards one of rung 1's contexts | 177-191 | the gate sums no "11", no "00", no "10" and no "01", exact, plus the higher rungs' bounds; every side read (section 1) |
| Math B2: a partial two-back passes R4 | 338-345 | 2 x 2 tests at lags 1, 2, 4 and 8 on own settings and own outcomes; flipped 1 in 10 and 2 in 10 refused; the reach sentence corrected (section 3) |
| Phys B1: R2's gate reads the board | 177-191 | the gate from the clock's own counts; the passing-given chance beside it, a board check (section 1) |
| Phys B2: R3 on W and (3p) settled against rule 5 | section 2; section 6 item 2 | R3 on W and (3p) moved to Big Pic's bench; DECODE3f's W field struck; the order-2 memory kept as a bench measurement (section 2) |
| Math MINOR 1: (3p) appends to R3 in the code | 256 | the code's R3 takes no (3p); the bench prints (3p) beside, measured (section 2) |
| Math MINOR 2: (3b)'s level | 265-284 | per-K two-tailed cuts tabulated; rate 33 to 51 per 1,000 (section 2) |
| Math MINOR 3: the ladder's share per rung | 376-381 | the rungs' bounds summed against one share (section 3) |
| Math MINOR 4: the interval rule's reason | 430 | an event lies between two of the clock's own lines (section 4) |
| Math MINOR 5: D4's check | 418-427 | a static check, the mutant as its no (section 4) |
| Math MINOR 6, phys MINOR 7: the pair record's side table | 316-323 | meetings on both sides in lines and sides; the guard's mates read; a format test, named (section 3) |
| Math MINOR 7: the curve's reach | 328-330 | named: two angle differences, 30 and 90 degrees (section 3) |
| Math MINOR 8: one side read per half | 181 | per half from the record (section 1) |
| Math MINOR 9: the digest and the interpreter | 17-20 | per-file sums with the command; Python 3.14.6 (Files) |
| Math MINOR 10, phys MINOR 1: the free-lay control | 353 | the member born at the middle; a local act at S = 2 exactly (section 3) |
| Phys MINOR 2: the seeds' law's constraint | section 3 | named: dependence within each pair event only (section 3) |
| Phys MINOR 3: "deeper" | 453-455 | relabelled "two rates", its premise named (section 4) |
| Phys MINOR 4: the interval rule's premise | 429-434 | the click-world reason needs no steady rate (section 4) |
| Phys MINOR 5: R3's union bound | section 7 | R3's level stated MEASURED; the union bound conditional (section 2) |
| Phys MINOR 6: the chain rule | 361-370 | (i) in force, by the 09:3x and 09:5x rulings (section 5) |
| Phys MINOR 8: the interpreter | 19-20 | Python 3.14.6 (Files) |

## 1. R2: the gate from the clock's own counts (math B1, phys B1)

**Replaces** DECODE3g's section 1 gate (lines 177-191) and its "for a side s" (one side read).

**The rule.**
- R2 is read for every side s of a clock (a site and a train). The clock's own count is its clicks in the record's
  order.
- In each half (the record's halves, by its order), the side's sequence is its 0 or 1 at each of the clock's clicks.
  N is the clicks in the half and n those with s.
- R2's ladder is as before: at L = 1, 2, 4 and 8, at least AMBIG = 2 pasts followed by both values.
- **NOT READ by name where the clock has one side in that half**, read from the record per half (math MINOR 8). Its own
  count there is its landings.

**The gate, from the clock's own counts alone** (a click reading, by the 09:5x rule).
- Given N and n, every placement of the n is equally likely to a reading that knows the counts alone (the exchangeable
  chance).
- Rung 1 needs both pasts, "1" and "0", each followed by both values. So it lacks a context exactly where the half
  holds no "11", no "10", no "00" or no "01".
- **The exact chances, closed forms of the transfer recursion, over C(N, n):**
  - no "11": C(N - n + 1, n);
  - no "00": C(n + 1, N - n);
  - no "10": 1, and no "01": 1 (for 0 < n < N);
  - a constant sequence (n = 0 or n = N) has chance 1.
- MEASURED: the transfer recursion on the clock's own counts equals these closed forms for every N from 2 to 16 and
  every n, with 0 disagreements.
- The rungs L = 2, 4 and 8 take (e)'s ladder gate's first-order bounds (section 3), on the half's own counts.
- **R2 is read where rung 1's sum and the higher rungs' bounds total at most 1/20, in both halves.** Else it is NOT READ.
  The 1/20 is a convention of the test, named before the reading (09:5x).

**Beside it, a board check:** the passing-given exact chances of no "11" and of no "00" for the side, by the transfer
recursion over the rounds (DECODE3g's, with the mathematician's recursion for "00"). They are printed, and never gate.

**MEASURED** (decode3h B; 200 fair draws a case, halves of 2,000 rounds; R2 per side):

| clock | side 1 | side 2 | carried, sides 1 and 2 | the board check beside: side 1's no "11", no "00" a half (thousandths) |
|---|---|---|---|---|
| steady 175 and 175 | SHOWN 200 | SHOWN 200 | NOT SHOWN, NOT SHOWN | below 1, below 1 |
| side 1 alternating 350 and 0, side 2 steady 175 | SHOWN 200 | SHOWN 200 | NOT SHOWN, NOT SHOWN | below 1, below 1 |
| side 1 the swing, side 2 steady 100 | SHOWN 200 | SHOWN 200 | SHOWN, SHOWN | below 1, below 1 |
| side 1 steady 8, side 2 steady 300 | NOT READ 200 | NOT READ 200 | NOT READ, NOT READ | 665, below 1 |
| side 1 steady 300, side 2 steady 30 (the mathematician's) | NOT READ 200 | NOT READ 92, SHOWN 108 | NOT READ, NOT SHOWN | below 1, 75 |
| side 1 steady 300, side 2 steady 8 (the mathematician's) | NOT READ 200 | NOT READ 200 | NOT READ, NOT READ | below 1, 817 |
| both 175, side 2 at 0 in the second half (the mathematician's) | NOT READ 200 | NOT READ 200 | NOT SHOWN, NOT SHOWN | below 1, below 1; below 1, 1,000 |
| one side (side 2 never passing) | NOT READ 200 | NOT READ 200 | NOT READ, NOT READ | below 1, 1,000 |

- On the mathematician's three rows, R2 had refused 34, 197 and 200 of 200 right records. It now refuses none: each is
  read behind the gate, or NOT READ by it, or by name.
- The rare side of the gate's own no (8 beside 300) and its common side both read NOT READ.
- A carried two-sided clock can still read SHOWN (the swing beside 100). R2 is necessary only, and R3 beside it refuses
  the clock.
- **Where Q10 touches R2** (the owner, 09:4x: a clock reads only its own clicks). R2 is the decoder's reading of the
  record's sides at the clock's clicks. Whether its context should be the clock's own lines alone is named for Big Pic.

## 2. R3: (3b) against the chi-square on K degrees; R3 on W to the bench (phys B2; math MINORs 1 and 2; phys MINOR 5)

**(3b)'s per-K cuts** (the 10:0x ruling, second part; replaces C1 in (3b)).
- Z is the floored sum of the windows' z_k, and K the windows read (20 to 39).
- Z is read against the chi-square on K degrees, at two tails of 5/12 per cent each: the half's 5/6 per cent.
  - NOT SHOWN where Z < lo_K or Z > hi_K; SHOWN else.
  - hi_K is the least whole thousandth whose upper tail is at most the level.
  - lo_K is the greatest whose lower tail is at most it, less K, since each z_k is floored.
- The cuts are computed once, in whole numbers:
  - for even K, by the Poisson sum, P(X <= x) = 1 - e^(-x/2) SUM_(j < K/2) (x/2)^j / j!;
  - for odd K = 2m + 1, by P(X <= x) = sqrt(2x / pi) [T - e^(-x/2) SUM_(j=1..m) x^(j-1) / (2j - 1)!!], with T erf's
    series, compared squared so that no root is taken.
- Examples: K = 20 gives [7,216, 40,621]; K = 21 [7,806, 42,034]; K = 30 [13,475, 54,383]; K = 39 [19,609, 66,253].
- Section G checks each end: True at the cut, False one thousandth past it.
- **The carried bound's gate is now the lower cut.** (3b) is read only where the carried bound B is at most lo_K. A
  carried side has Z < B (DERIVED in DECODE3e), so it reads NOT SHOWN wherever (3b) is read.
- (3d) and (3e) keep C2 9,575 and C4 13,696, and the two-values rule only where every cell expects ten.

**MEASURED** (decode3h A; 1,000 fair draws a case, halves of 2,000):

| passing | R3 NOT SHOWN of 1,000 | first refused by (3b), (3d), (3e) | two-values halves |
|---|---|---|---|
| steady 175 | 50 | 16, 19, 15 | 0 |
| steady 300 | 40 | 16, 13, 11 | 0 |
| the swing (moving) | 51 | 19, 13, 19 | 0 |
| the step (moving) | 33 | 13, 9, 11 | 0 |

- (3b) now takes 13 to 19 per 1,000 against its share of 16.7. Steady 175's excess (64 in DECODE3g) is gone.
- Carried sides read 0 SHOWN:
  - steady 300, 175 and 190, 313 at halves of 480, the swing and the step: NOT SHOWN 20 of 20 each;
  - the three-level family (972): NOT READ 182, NOT SHOWN 790.
- **R3's level is stated MEASURED** (phys MINOR 5): 33 to 51 per 1,000 on these four cases. The union bound gives 5 per
  cent only given each test's own level, so it is named conditional.

**R3 on W, with (3p), leaves the settled list** (the 10:1x rule 5; the 09:5x ruling, second part).
- It is a bench reading of the member, Big Pic's: no record carries W apart from the sides.
- DECODE3f's W field is struck from writer C's list, and the decoder's R3 reads single, one-way sides only.
- The order-2 memory of THIRD7's member stays a bench measurement, as DECODE3g measured it: (3e) X^2 27,383 and 17,444;
  24,432 and 30,405; 800,000 rounds.
- **(3p) in the code** (math MINOR 1): decode3h's r3 takes no (3p). The bench function prints (3p) beside R3's verdict
  and never appends it.
  - MEASURED: THIRD7's member with y swinging from 80 to 120 thousandths of 3D, halves of 8,000, three lays, reads R3
    SHOWN, with (3p) beside it reading NOT READ (no steady stretch).
  - DECODE3g's code read NOT READ there.

## 3. R4: the lags, the free-lay control, the record as meetings, the seeds' law's constraint (math B2; MINORs)

**The 2 x 2 tests at lags 1, 2, 4 and 8** (the 10:0x ruling, second part; replaces DECODE3g line 344's reach).
- Per half, each place's outcome is read against its own setting L pair events back, and against its own outcome L back.
  Lag 1 on own outcomes is (e)'s lag-1.
- Each is a 2 x 2 at CUT_FW, counted in N_T.
- Per half R4 now holds 29 + 6 S parts:
  - (a), the limit, the four curve tests, the four no-signal tests, the five 2 x 2 tests, the fourteen lag tests and
    2 S lag-1 tests, all at CUT_FW;
  - and 4 S ladders.
- So N_T = 2 (29 + 6 S): 70 for one source and 82 for two. CUT_FW is 11,452 and 11,746, from the readings file and
  checked.
- **The reach, corrected.** The joint past refuses an outcome that its context of at most eight events fixes exactly.
  The lag tests refuse a partial dependence on one past setting or outcome at lags 1, 2, 4 or 8. A partial dependence
  at the other lags, deeper than 8, or only on a joint of several past values, passes both. That reach is named.

**A ladder's share is spent once** (the 10:0x ruling, second part; math MINOR 3).
- The four rungs' first-order bounds are summed against the ladder's one share, 5 / N_T per cent. A ladder whose sum
  passes the share reads NOT READ.
- MEASURED: the summed gate reads at 20,000 pair events a half (the toy's records), and not at 2,000 (the rate's
  records). DECODE3g measured the top rung alone opening between 2,300 and 2,400.

**The pair record, as meetings on both sides** (rule 5; math MINOR 6, phys MINOR 7; replaces DECODE3g lines 316-323).
- Per pair event, every meeting is written on both of its sides, in lines and sides alone, with no side table:
  - **the bearing meeting:** the source clock at its place gives one quantum to each place's outcome clock, by across
    sides, and each outcome clock takes it there by the mirror;
  - **the setting meeting:** the place's setting clock gives one quantum to the partner that names the setting, which
    takes it;
  - **the outcome's sign:** the outcome clock's own-place meeting with its partner.
- A pair is read as the bearing meeting an outcome's across side names (its round, place and clock). The sides carry q
  alone, with no tooth (the owner's Q11 answer).
- MEASURED on every record: 360,000 lines for 40,000 pair events. The guard's mates (a stand-in of E's sides.paired)
  read, and 40,000 pairs are read back from the lines.
- **The toy's round trip is named a format test.** The toy's source place and its one round are a format's, not a
  world's.

**The free-lay control, as ruled** (the 09:5x ruling, second part; math MINOR 10, phys MINOR 1; replaces line 353).
- **The member born at the middle at each place**: THIRD7's form at the click world's dial, y half of 3D, local to its
  place.
  - Each place's setting, from its own turned teeth, chooses which reading of the place's own record is its outcome:
    the landing this round, or whether it changed since the last.
  - MEASURED: S -27 and 7 per mille, so (a) reads NOT SHOWN.
- **A local act at the bound**: both places' outcome is one shared reading, whatever the settings, so S = 2 exactly.
  - MEASURED: S 2,000 and 2,000, and (a) reads NOT SHOWN.
  - This tests (a)'s cut at its edge: a control that can fail.

**The seeds' law's constraint** (phys MINOR 2). Under (C), the order readings refuse any dependence across pair events:
the 2 x 2 tests, the lag tests, (e) and the joint past. So the seeds' law may couple the settings to the hand within each
pair event only. The constraint is named for Big Pic.

**The curve's reach** (math MINOR 7). The pair's curve is read only at the two angle differences the settings give, 30
and 90 degrees.

**MEASURED** (decode3h C; 40,000 pair events, 20,000 a half; every record's settings from each place's own turned teeth,
the toy's alice and bob):

| record | the parts that fail | the largest lag z^2 (CUT_FW 11,452) | R4 |
|---|---|---|---|
| the toy's third click (a format and reading test) | none; the click parts SHOWN | 5,829 (B's outcome 8 back) | NOT READ, by name |
| the first click | (e), the lags, the joint past | 19,998,000 (A's outcome 2 back) | NOT SHOWN |
| two first clicks interleaved (N_T 82, CUT_FW 11,746) | (e), the lags, the joint past | 19,998,000 | NOT SHOWN |
| the parity first click | (e), the lags, the joint past | 19,998,000 | NOT SHOWN |
| a fixed order of period four | (e), the lags, the joint past | 19,998,000 | NOT SHOWN |
| A's outcome its own previous setting | the lags, the joint past | 19,999,000 (A's setting 1 back) | NOT SHOWN |
| two back | the lags, the joint past | 19,998,000 (A's setting 2 back) | NOT SHOWN |
| parity of two | the joint past alone | 5,088 | NOT SHOWN |
| two back, flipped 100 per 1,000 (the mathematician's B2) | the lags alone; S 2,499 | 12,883,246 (A's setting 2 back) | NOT SHOWN |
| two back, flipped 200 per 1,000 | the lags alone; S 2,499 | 7,137,608 | NOT SHOWN |
| the free-lay control: the member born at the middle | (a): S -27 and 7; the curve | 4,574 | NOT SHOWN |
| a local act at the bound | (a): S 2,000 and 2,000; the curve | 5,109 | NOT SHOWN |

- The flipped forms keep the joint past SHOWN ([8, 32, 320, 1,110] and [8, 32, 475, 1,463] at A in the first half) and
  every other part SHOWN. The lag tests are what refuse them.
- **The rate**, on 1,000 right pair records (a stand-in draw of the pattern, 2,000 events a half, its settings fair at
  each place, read on the trials, the format tested above):
  - the click parts read NOT SHOWN on 34 of 1,000, within 5 per cent: the lags 22, the 2 x 2 7, the curve 3, (e) 2;
  - NOT READ on 966, since the summed ladder gate does not open at 2,000 a half, and (c) is gated on it.

## 4. D4, the interval rule's reason, and "two rates" (math MINORs 4 and 5; phys MINORs 3 and 4)

**D4 is a static check** (replaces DECODE3g lines 418-427).
- D4 reads each conversion's code: every difference it takes must be a difference of own counts (calls of own()),
  never of a round or a face field.
- Its no is the mutant. MEASURED (decode3h D):
  - C-a on own counts is allowed;
  - the mutant C-a on rounds is refused, at its first difference of a round field.
- The computed 11 against 7 (DECODE3g) stands as the mutant's effect, a mutation test of the code.

**The interval rule's click-world reason** (replaces line 430; math MINOR 4, phys MINOR 4).
- An event lies between two of a clock's own lines. So the clock's own-count reading of it is within one of the event's
  own time in that clock, with no steady rate needed.
- The products' intervals follow, and so does the DERIVED rule that a right record never reads NOT SHOWN.
- The board premise (a balanced line word) is struck.

**"Two rates"** (replaces lines 453-455 and the D table's labels; phys MINOR 3).
- The HALF physicist's "two depths" configurations (A at 2 of every 3 rounds, B at 3 of every 4) are two line rates,
  and are relabelled "two rates".
- "A deeper than B" (p >= q + 2) reads "A counts less at rest". Its premise is clocks of one kind with one activity.
- A quieter clock at one depth also counts less. The well's depth beside it, a board check, is what tells them apart.
- DECODE3g's table holds as measured, under the new labels.

**C-a's observers** (the 10:0x ruling, first part). A clock with no own meeting in the whole record has no count, so it
is no A and no B. C-a reads only clocks with own meetings.

## 5. The chain rule, and the owner's 09:4x answers against the decoder's rules

- **The chain rule in force is (i), "strictly later"** (the 09:3x and 09:5x rulings, second parts; phys MINOR 6).
  - Two meetings of one clock in one round are simultaneous in its own lines, and unordered.
  - Rule (s), a chain passing within one round, is a board check of the act's one-round reach, named so.
  - On the mesh world the split is 114 / 62 / 187 under (i).
  - Rule L and the per-clock cone are settled build items for the decoder (09:4x).
- **The teeth go out of the record** (the owner's Q11 answer). Where it touches the decoder's rules:
  - no click reading here reads a tooth;
  - the pair record's sides carry q alone;
  - the sides guard drops its tooth rules (writer I, node-rec);
  - the board checks that read teeth (L2 and L3's books, the lone edge's exact recomputation from its birth, the key's
    birth check) read the board's own state, as code checks;
  - R2's passing-given chance beside the gate reads the board's own state too.
- **A clock reads only its own clicks** (the owner's Q10 answer).
  - R2's context is the decoder's reading of a side at the clock's clicks (section 1); its form under Q10 is named for
    Big Pic.
  - R4's joint past reads the place's setting clock's and outcome clock's own clicks, each clock's own, as the
    decoder's reading of the place.
  - "Nothing a clock can read before its click" is read through those clicks.
- **The silent worlds go out** (the owner's answer 4).
  - The key check's case with no edges (dial = key) leaves the decoder.
  - The decoder reads worlds with clicks. No other rule here changes.
- **A significance level is a convention** (09:5x, second part). R3's 5 per cent, R4's 5 per cent and R2's 1/20 are
  named before the reading, fixed for every reading, and never moved.
- **No cut on the sizes of q** is taken by any reading here (09:4x).

## 6. Settled, to be built; open, Big Pic's

**Settled** (the decoder's, to be built by our writers):
1. R2 per clock and per side, in its own count, gated from its own counts, with the passing-given chance beside it
   (section 1).
2. R3 on single, one-way sides: (3b) per K from the readings file, (3d), (3e), and its rate named (section 2).
3. The pair record as meetings on both sides, in lines and sides alone (section 3).
4. R4's parts read in the click world:
   - the pair's curve, (a) and the limit;
   - no signal gated on the click reading, R3 beside;
   - the order per source and the joint past;
   - the lags at 1, 2, 4 and 8;
   - the free-lay control and the local act at S = 2.
   R4 is NOT READ by name until the seeds' law exists.
5. D4 as a static check; one key per record; one precedence; one cut convention.
6. The interval rule for C-a to C-e's checks.
7. Rule L and the per-clock cone (09:4x).

**Open, Big Pic's:**
- the seeds' law (the end form first, the owner's 09:4x word), with its constraint named in section 3;
- R3 on W and (3p), the member's bench reading;
- R2's context under Q10;
- the third click's reading that the first click's record fails (10:1x);
- the uncertainty principle from two click observables;
- light and the echo (his item 5);
- what a place of the click world is, with the Mesh meeting (the owner's batch).

**OWED:**
- nl/'s commit;
- the joint past's rate on 1,000 right records long enough to read it;
- C-b;
- the click-form record and the key check in node-all's decoder.

## 7. Statuses

**DERIVED:**
- the rung-1 closed forms (the transfer recursion's);
- the carried no at the lower cut (Z < B <= lo_K);
- the chi-square CDF forms for even and odd K;
- the lag tests' reach;
- the interval rule on the click-world reason.

**MEASURED** (decode3h twice, alike, under Python 3.14.6; cuts3h once): sections 1 to 4.

**Conventions, named before the reading:** R3 at 5 per cent, R4 at 5 per cent, R2's gate at 1/20.

**Board checks:** R2's passing-given chance; R3; (d); the well's depth beside "two rates".

**Code checks:** D4 (static); the guard's mates; one key per record.
