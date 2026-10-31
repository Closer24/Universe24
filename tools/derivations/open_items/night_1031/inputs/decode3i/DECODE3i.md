# DECODE3i: the decoder's readings of the three clicks, ninth text

The Boss's deriver for the decoder, 2026-10-31, 10:1x to 10:4x UTC. **Status: DRAFTED, for DECODE3's pair.**
- It folds both NOT PASSED reports on DECODE3h:
  - scratchpad/decode3h_math/REPORT.md, one BLOCKING;
  - scratchpad/decode3h_phys/REPORT.md, two BLOCKING.
- It applies the Boss's rulings of 10:13 and 10:16 UTC, with DECODER-CUT (09:59 UTC). Section 0 quotes each verbatim
  with its source.
- DECODE3h.md (461 lines, sha256 7f7d3d63367c4690...) stands as frozen. This text replaces only the lines it names, by
  DECODE3h's line numbers, and keeps every other rule of DECODE3h and the texts beneath it.

**Files** (scratchpad/decode3i/).
- The copies: bp/, nl/, st1/, st2run_1/, st2run_2/; decode3e.py, pair_order.py, decode3f.py, decode3g.py, decode3h.py
  and cuts3h.py, copied from decode3h/ with every __pycache__ removed.
- **The pin, of sources only** (replaces DECODE3h line 17).
  - nl_sources.sha256: 35 source files, no __pycache__. The file's own sha256 is c7aeafde6109e3ff....
  - The command: `find nl -type f | LC_ALL=C sort | xargs sha256sum > nl_sources.sha256`, run with no bytecode
    present.
  - Every run here uses python3 -I -B, so no run writes into the tree: after every run, no .pyc file exists in the
    folder, and `sha256sum -c nl_sources.sha256` reads OK on all 35.
  - DECODE3h's nl.sha256 failed on 3 bytecode files its own runs rewrote, which is the readers' finding.
- **The interpreter:** the live venv's Python 3.14.6, under -I -B.
- **The probes:**
  - cuts3i.py writes readings3i.json once: readings3h's entries, with CUT_FW at 58 and 74 tests and the lag sums'
    cuts (chi-square on 16 and on 8 degrees, by the Poisson sum).
  - decode3i.py reads every cut from readings3i.json.
  - Both were run twice. decode3i_run1.txt = decode3i_run2.txt, and readings3i.json = readings3i_run2.json, byte for
    byte.
- **Conduct:** whole numbers only, with Rule3's carry the one division. No //, %, float, true division, math or random.
  Paths go by joinpath, one process at a time under nice -n 19, with the load read first.

Stand-ins, test records and formats test a rule's logic and are never a world. No sentence here puts light or matter on
the board, and no reading here reads a tooth or a passing.

## 0. The rulings this text applies, verbatim, with their sources

DECODE3g's and DECODE3h's section 0 stand. These are added:

From the brief, "The Boss's rulings, 10:16 UTC (from DECODE3h's mathematician, with its physicist: both NOT PASSED on one point)":

> - R4 reads the order both ways, in the mathematician's smaller form, which suits DECODER-CUT: per place and per half,
>   three sums of the lag z^2 (the outcome against its own settings at lags -8 to -1 and 1 to 8, on 16 degrees; against
>   its own outcomes at lags 1 to 8, on 8; against the far place's settings at lags -8 to 8 but 0, on 16), each cut at
>   the chi-square on its degrees from the readings file; and a joint future beside the joint past (the same function
>   on the reversed record), which the physicist measured refusing the parity form the lag sums alone would pass. All
>   counted in N_T. Both readers' future forms must be refused, and the toy's third click must still pass.

From the brief, "The Boss's rulings, 10:16 UTC (from DECODE3h's mathematician, with its physicist: both NOT PASSED on one point)":

> - The NOT READ: R4's click parts can first read SHOWN between 2,000 and 3,000 events a half (the summed gate opens
>   there); the text names that length, calls R4 "refusing only" below it, and cites its rate where it is read (37 per
>   1,000 at 3,000 events a half, MEASURED). On the worlds we have, no world hosts Bell, so R4 reads NOT READ by name.

From the brief, "The Boss's rulings, 10:16 UTC (from DECODE3h's mathematician, with its physicist: both NOT PASSED on one point)":

> - R3 and R3 beside (c) leave the decoder for the run tool's board checks, reading the board's own state; the pair
>   record carries no passing (both readers; the owner's Q11).

From the brief, "The Boss's rulings, 10:16 UTC (from DECODE3h's mathematician, with its physicist: both NOT PASSED on one point)":

> - Under Q10, R2 on the clock's own lines is the per-clock form, built now; the per-side R2 is renamed the decoder's
>   reading of a side (the physicist's Q3).

From the brief, "The Boss's rulings, 10:16 UTC (from DECODE3h's mathematician, with its physicist: both NOT PASSED on one point)":

> - "The law named in the initialization" reads "where it is laid: the start, the end or both" (the physicist's Q4).

From the brief, "The Boss's rulings, 10:16 UTC (from DECODE3h's mathematician, with its physicist: both NOT PASSED on one point)":

> - DECODER-CUT: the precedence (worst, halves), one key per record and the readings file enter now; D4 is a test of
>   the decoder's code (its static check reads every arithmetic node over a round or face field, its no including the
>   negated mutant); R2 waits on a cut of its size; R3 goes to the board checks; R4 and its record parse hold until the
>   seeds' law and this fold; the interval rule holds (no caller yet).

From the brief, "The Boss's rulings, 10:16 UTC (from DECODE3h's mathematician, with its physicist: both NOT PASSED on one point)":

> - The pin: nl.sha256 pins the sources only (no __pycache__), and every run uses -B, so that no run writes into a
>   frozen tree. The free-lay control names its shared past (one member's W, alike births: the strongest local case),
>   and that it serves an end-form law too (the exact run back).

From the brief, "The Boss's rulings, 10:13 UTC (Sofer's 6541979903 and 6542051011; DECODE3h's physicist; ALG3)":

> - Law lines (Sofer): the owner's Q10 and the strengths law stand as law lines of their own, in the words of
>   6541741909: "A clock reads only its own clicks. Its sides and the board are not 'what a clock can read'." and
>   "Every strength comes from the structure, or is laid once at the start for each clock; never searched, and never one
>   choice for the whole universe." The owner's "There is no floor in the law." enters whole beside them.

From the brief, "The Boss's rulings, 10:13 UTC (Sofer's 6541979903 and 6542051011; DECODE3h's physicist; ALG3)":

> - DECODE3h's physicist (S/decode3h_phys/REPORT.md): NOT PASSED on two BLOCKING items. His questions:
>   - Q1: yes, R4 reads the order both ways: lags ahead at 1, 2, 4 and 8 and a joint-future ladder, counted in N_T, so
>     that it reads a law from the start, the end or both (the owner's law of the choice; his question to David).
>   - Q2: yes, R3 and R3 beside (c) leave the decoder for the run tool as board checks reading the board's own state;
>     the pair record carries no passing (the owner's Q11: the record holds q alone).
>   - Q3: yes, under Q10 R2 on the clock's own lines is the per-clock form, built now; the per-side R2 is renamed the
>     decoder's reading of a side.
>   - Q4: yes, "the law named in the initialization" reads "where it is laid: the start, the end or both" (the 08:4x
>     ruling; the owner's word of 09:33).
>   - DECODE3i folds both readers once the mathematician hands back.

From the brief, DECODER-CUT (09:59 UTC), "In force":

> - DECODER-CUT is an OPEN item of the Decoder part, with the runner's: one guard by the schema's own fields (no rule
>   per key), the click world's readings each read from q alone after node-rec.

From the brief, DECODER-CUT (09:59 UTC), "In force":

> - Its target: the decoder no larger than the Node-clock it decodes, by Sofer's count on the same head. No line is
>   packed to meet it. A new reading (DECODE3g's settled rules, LIGHT3's rule L and the per-clock cone) enters only
>   within the target or with a reading cut of its size.

From the brief, "The owner's word, about 09:4x UTC, on (C)'s two forms":

> - "I answered you... Bell from the end feels closer to nature..." Of Big Pic's two forms for (C)'s seeds' law, the end
>   form (a tie of the two wings' ends, with no signal) comes first on Big Pic's bench; the start form stays derived
>   beside it.

## What changed

- **R4 reads the order both ways** (both readers' B1).
  - Three lag sums per place and half, on 16, 8 and 16 degrees, replace the fourteen lag 2 x 2s.
  - A joint future reads beside the joint past.
  - N_T = 2 (21 + 8 S): 58 or 74.
  - Every future form both readers built is refused, so are "three back" flipped one in ten and every earlier form, and
    the toy's third click passes.
- **The NOT READ is named.**
  - The summed gate opens at 2,500 pair events a half, and R4 is "refusing only" below it.
  - Its rate where it is read is 31 per 1,000 at 3,000 a half, with no NOT READ.
- **R3 and R3 beside (c) leave the decoder** for the run tool's board checks (phys B2). The pair record carries no
  passing.
- **R2:**
  - per clock on its own lines (Q10), built now;
  - the per-side R2 renamed the decoder's reading of a side;
  - the joint past and the outcome clock's own past named apart.
- **(b)'s law** is read "where it is laid: the start, the end or both".
- **The rest:**
  - DECODER-CUT's entry list, with sizes;
  - D4 over every arithmetic node, with three mutants;
  - the free-lay control's shared past, and its use for an end-form law;
  - the pin of sources only, under -B.

## Each reader item: met or not, and where

| Item | DECODE3h's line | Met? Where |
|---|---|---|
| Math B1 / phys B1: R4 reads the past side only | 284-296, 328-330 | met: section 1 (the lag sums both ways, the joint future; every future form refused; the toy passes) |
| Phys B2: R3 has no input in a q-alone record | 145-153, 245-268, 418 | met: section 3 (R3 and R3 beside (c) go to the run tool's board checks; no passing in the record) |
| The coordinator's question: the NOT READ on 966 | 355-358, 442 | met: section 2 (the length named; "refusing only" below it; the rate where read) |
| Math MINOR 1: D4 reads subtraction only | 362-368 | met: section 5 (every node; three mutants refused) |
| Math MINOR 2, phys MINOR 6: the pin fails | 17-21 | met: Files (sources only; -B; 35 of 35 OK) |
| Math MINOR 3: R3's place | 418 | met: section 3 |
| Math MINOR 4: the free-lay control's shared past | 318-326 | met: section 1 |
| Math MINOR 5, phys MINOR 7: DECODER-CUT | (new) | met: section 6 (each item with its size) |
| Phys MINOR 1: R2 under Q10 | 234-235, 400-404 | met: section 4 (per clock on its own lines, built; the per-side renamed; the two pasts named apart) |
| Phys MINOR 2: the NOT READ measurable | 355-358 | met: section 2 |
| Phys MINOR 3: the constraint overclaimed | 328-330 | met: section 1 (corrected, both ways, within its reach) |
| Phys MINOR 4: "the law named in the initialization" | DECODE3g section 0 and line 331 | met: section 1 |
| Phys MINOR 5: the control serves an end-form law | 318-326 | met: section 1 |

## 1. R4: the order both ways (both readers' B1; phys MINORs 3, 4 and 5; math MINOR 4)

**Replaces** DECODE3h lines 284-296 (the fourteen lag 2 x 2s, N_T and the reach) and 328-330 (the constraint).

**The lag sums**, per place and per half, each one test cut at the chi-square on its degrees from the readings file.
- **Own settings both ways:** the outcome against the place's own setting at lags -8 to -1 and 1 to 8, the sum of the
  sixteen 2 x 2 z^2, on 16 degrees.
- **Own outcomes:** against the place's own outcome at lags 1 to 8, on 8 degrees.
- **The far place's settings both ways:** against the far place's setting at lags -8 to 8 but 0, on 16 degrees.
- A sum with a degenerate table reads NOT READ. The precedence then takes the part that refuses first.
- Cuts (readings3i.json, the least whole thousandth whose upper tail is at most 5 / N_T per cent, by the Poisson sum):
  - 39,697 on 16 degrees and 26,501 on 8 at N_T 58;
  - 40,421 and 27,114 at 74.

**The joint future**, beside the joint past: the same function on the reversed record (per source and place). It reads
the next L settings and outcomes with the present setting, at L = 1, 2, 4 and 8, AMBIG 2, behind the same summed gate.
(c)'s gate is now (e), the joint past and the joint future, SHOWN at both places.

**N_T.** Per half there are:
- (a), the limit, the four curve tests, the four no-signal tests, the five 2 x 2 tests and 2 S lag-1 tests, all at
  CUT_FW;
- the six lag sums;
- 6 S ladders: (e), the joint past and the joint future, at both places.

So N_T = 2 (21 + 8 S): 58 for one source and 74 for two. CUT_FW is 11,103 and 11,555, from the readings file.

**The reach, corrected.**
- The lag sums refuse a dependence, whole or partial, of the outcome on one own setting or the far place's setting
  within eight events either way, or on one own outcome within eight events before.
- The joint past and the joint future refuse an outcome that its context of at most eight events, before or after,
  fixes exactly.
- A partial dependence deeper than eight events either way, or one only on a joint of several values, passes them.
  That reach is named.

**The seeds' law's constraint, corrected** (phys MINOR 3).
- Under (C) the order readings now refuse, within that reach and both ways, any dependence of an outcome on another pair
  event's settings or outcomes.
- So the seeds' law may couple the settings to the hand within each pair event only, as far as eight events either way
  can tell.
- The constraint is named for Big Pic.

**(b)'s law, where it is laid** (the 10:13 ruling, Q4; phys MINOR 4). The 08:5x phrase "the law named in the
initialization" (DECODE3g section 0, quoted there verbatim, and its line 331) reads "the law named where it is laid: the
start, the end or both".

**The free-lay control** (math MINOR 4, phys MINOR 5; adds to DECODE3h lines 318-326).
- Both places read one member's W, born alike at the middle: a shared past, the strongest local case. It reads S at
  most 2 all the same.
- Laid at the start (born at the middle), it reads the same bound as a member laid to end at the middle, by the exact
  run back (L7). So it serves an end-form law too.

**MEASURED** (decode3i C; 40,000 pair events, 20,000 a half). Every record's settings come from each place's own turned
teeth (the toy's alice and bob). Every record is written as meetings on both sides; the mates read, and 40,000 pairs
are read back. Test records, never an act:

| record | the parts that fail | the largest lag sum, first half (cuts 39,697 on 16 and 26,501 on 8 at N_T 58; 40,421 and 27,114 at 74) | R4 |
|---|---|---|---|
| the toy's third click (a format and reading test) | none: the click parts SHOWN | B's own settings 18,512; the joint future [8, 32, 512, 750] at A | NOT READ, by name |
| the first click | lag sums, (e), joint past, joint future | A's own outcomes 159,820,039 | NOT SHOWN |
| two first clicks interleaved | lag sums, (e), joint past, joint future | A's own outcomes 79,900,043 | NOT SHOWN |
| the parity first click | lag sums, (e), joint past, joint future | 79,940,008 | NOT SHOWN |
| a fixed order of period four | lag sums, (e), joint past, joint future | 79,980,000 | NOT SHOWN |
| A's outcome its own previous setting | lag sums, joint past | A's own settings 20,014,098 | NOT SHOWN |
| two back | lag sums, joint past | 20,011,348 | NOT SHOWN |
| parity of two | the joint past alone | 18,747 | NOT SHOWN |
| two back, flipped 100 per 1,000 | the lag sums alone | 12,686,456 | NOT SHOWN |
| two back, flipped 200 per 1,000 | the lag sums alone | 7,104,406 | NOT SHOWN |
| **two ahead** (both readers') | lag sums, joint future | A's own settings 20,011,437 | NOT SHOWN |
| **four ahead** (the mathematician's) | lag sums, joint future ([8, 32, 0, 0]) | 20,008,745 | NOT SHOWN |
| **parity of the next two settings** (the physicist's) | the joint future alone ([8, 0, 0, 0]) | 38,963, under the cut | NOT SHOWN |
| **two ahead, flipped 100 per 1,000** (the mathematician's) | the lag sums alone | 12,874,224 | NOT SHOWN |
| **three back, flipped 100 per 1,000** (the mathematician's) | the lag sums alone | 12,737,663 | NOT SHOWN |
| the free-lay control: the member born at the middle | (a): S -27 and 7; the curve | 18,690 | NOT SHOWN |
| a local act at the bound, S = 2 exactly | (a): S 2,000 and 2,000; the curve | 25,299 | NOT SHOWN |

- "Parity of the next two settings" passes the lag sums (38,963 under 39,697) and is refused by the joint future alone,
  as the ruling foresaw.
- "Three back" flipped one in ten, at a lag DECODE3h did not read, is refused by the lag sums.
- In every row but the two controls, S reads 2,456 to 2,522 a half.

## 2. The NOT READ: R4 "refusing only" below its length (the coordinator's question; phys MINOR 2)

**Replaces** DECODE3h lines 355-358 and the OWED line 442.
- R4's click parts can read SHOWN only where every ladder's summed gate opens.
- MEASURED (decode3i C, the gate's own bounds at N_T 58, one source, fair marginals, in steps of 100 from 2,000): the
  joint ladder's summed gate first opens at **2,500 pair events a half**.
- **Below that length R4 is "refusing only":** it reads NOT SHOWN or NOT READ, never SHOWN. DECODE3h's 34 of 1,000 at
  2,000 a half was the rate of the parts that are read, not of the reading.
- **Where it is read, MEASURED:** 1,000 right pair records of the pattern (a stand-in draw, 3,000 events a half, its
  settings fair at each place, read on the trials, the format tested above).
  - The click parts read SHOWN 969, NOT SHOWN 31, NOT READ 0.
  - The 31 by part: the lag sums 12, (c) 7, (e) 6, the curve 5, the 2 x 2 tests 4. That is within the 5 per cent
    family.
  - The mathematician measured 37 per 1,000 there under DECODE3h's form.
- On the worlds we have, no world hosts Bell, so R4 reads NOT READ by name there, whatever the gate (10:16).

## 3. R3 and R3 beside (c) leave the decoder (phys B2; math MINOR 3)

**Replaces** DECODE3h's settled item 2 (line 418) and every "R3 beside" in R4 (section 3's parts and table).
- The record holds lines and sides, q alone (the owner's Q11 answer). So the passing that (3b), (3d) and (3e) read, and
  each place's passing that R3 beside (c) read, are in no record.
- **R3 and R3 beside (c) become the run tool's board checks,** reading the board's own state, as R2's passing-given
  chance already does.
- **The pair record carries no passing.** decode3i's R4 reads no R3 and no passing.
- Every passing reader is named a board check: R3 ((3b), (3d), (3e)) and R2's passing-given chance.
- R3's rules, cuts and rates stand as DECODE3h measured them, now as the run tool's: rate 33 to 51 per 1,000, carried 0
  SHOWN, (3b) per K from the readings file.

## 4. R2 under Q10 (phys MINOR 1; the 10:13 ruling, Q3)

**Replaces** DECODE3h lines 234-235 and 400-404.
- **R2 per clock, on the clock's own lines, built now.**
  - In each half, R2 reads the q of each of the clock's own clicks, in the record's order.
  - It runs the ladder at L = 1, 2, 4 and 8, AMBIG 2, behind the own-count gate: rung 1's exact closed forms and the
    higher rungs' bounds, summed against 1/20.
  - It is NOT READ by name in a half where the clock's q takes one value.
  - It reads only the clock's own clicks: "a clock reads only its own clicks" (Q10).
  - The stand-ins' clocks write q in {1, 2}; a clock whose q takes more values is read by the same ladder, its gate by
    the ladder bound alone.
- **The per-side R2 is renamed "the decoder's reading of a side"**: the decoder's reading of the record's sides at the
  clock's clicks, never "the clock's own click past". It stands as DECODE3h measured it.
- **The joint past and the outcome clock's own past are named apart.**
  - The joint past (and the joint future) read the place: its setting clock's and outcome clock's clicks, two clocks.
  - The outcome clock's own past under Q10 is (e) and its own-outcome lag sum.
  - "Nothing a clock can read before its click" is read through the outcome clock's own past.

**MEASURED** (decode3i B; 200 fair draws a case, halves of 2,000; R2 per clock):

| clock | R2 per clock | carried |
|---|---|---|
| steady 175 and 175 | SHOWN 124, NOT READ 76 | NOT READ |
| side 1 alternating 350 and 0, side 2 steady 175 | SHOWN 122, NOT READ 78 | NOT READ |
| side 1 the swing, side 2 steady 100 | NOT READ 200 | NOT READ |
| side 1 steady 8, side 2 steady 300 | NOT READ 200 | NOT READ |
| side 1 steady 300, side 2 steady 30 | NOT READ 200 | NOT SHOWN |
| side 1 steady 300, side 2 steady 8 | NOT READ 200 | NOT READ |
| both 175, side 2 at 0 in the second half | NOT READ 200 | NOT READ |
| one side passing, side 2 never | NOT READ 200 | NOT READ |

- R2 per clock refuses no right record (0 NOT SHOWN in 1,600).
- Its power is named: a clock's own lines carry its second value only where two sides pass in one round (q = 2). Its
  gate opens where that value comes often enough: about 6 in 10 records at 175 and 175, never at the rarer pairs.
- The carried clock at 300 and 30 reads NOT SHOWN. The others are NOT READ: one value, or the gate.

## 5. D4 over every arithmetic node (math MINOR 1)

**Replaces** DECODE3h lines 362-368.
- D4 is a static check of each conversion's code: every record field it takes (each parameter) reaches its arithmetic
  only as an argument of own(). No field may stand in any other node: a difference, a sum, a negation, a tuple or a call.
- MEASURED (decode3i D):
  - C-a on own counts: allowed;
  - the mutant on rounds, `(take - give) - (b2 - b1)`: refused (take reaches a BinOp);
  - the negated mutant, `take + -give + -b2 + b1`: refused;
  - the summed mutant, `sum((take, -give, -b2, b1))`: refused (take reaches a Tuple).
- D4 is a test of the decoder's code and adds no decoder lines.

## 6. DECODER-CUT: the entry list, with sizes (the 10:16 ruling; math MINOR 5, phys MINOR 7)

The decoder stands at 605 active lines on node-fold, against its target, the Node-clock's 338 (DECODER-CUT). A new
reading enters only within the target or with a reading cut of its size. Sizes are counted in this probe's own
functions, with blank, comment and docstring lines left out (decode3i D), and the mathematician's for R3:

| item | size (lines) | entry |
|---|---|---|
| one precedence (worst, halves) | 9 | now; likely a net cut, replacing per-reading precedence |
| one key per record | 6 | now |
| the readings file and one cut convention | data, a few lines to load | now; removes computed cuts |
| D4 | 15 | a test of the decoder's code; no decoder lines |
| R2 per clock, with its gate | 67, of which the ladder gate is shared with R4 | waits on a reading cut of its size |
| R3 and R3 beside (c) | 95 (the mathematician's count) | to the run tool's board checks; no decoder lines |
| R4's click parts (both ways) | 134 | holds until the seeds' law and this fold |
| R4's record parse and mates | 30 | holds, with R4 |
| the interval rule | 7 (the mathematician's count) | holds: no caller until C-a to C-e |

- What enters now is about 15 lines and the readings file's data.
- Rule L and the per-clock cone (09:4x) enter only within the target, or with their cut.

## 7. Settled, to be built; open, Big Pic's; statuses

**Settled** (the decoder's, to be built), by the DECODER-CUT order of the table above:
- the precedence, one key per record and the readings file, now;
- D4 as a test;
- R2 per clock, when its cut is found;
- R4 both ways and its record parse, when the seeds' law exists (it reads NOT READ by name until then, and "refusing
  only" below 2,500 events a half);
- the interval rule, with C-a to C-e;
- Rule L and the per-clock cone.

**The run tool's board checks:** R3 and R3 beside (c); R2's passing-given chance.

**Open, Big Pic's:**
- the seeds' law, laid at the start, the end or both (the end form first), with its constraint named in section 1;
- R3 on W and (3p), the member's bench reading;
- the third click's reading that the first click's record fails;
- the uncertainty principle from two click observables;
- light and the echo;
- what a place of the click world is, with the Mesh meeting (the owner's batch).

**OWED:**
- nl/'s commit;
- C-b;
- the click-form record and the key check in node-all's decoder.

**DERIVED:**
- the lag sums' cuts on even degrees (the Poisson sum);
- the joint future as the joint past on the reversed record;
- D4's rule over every node;
- the reach both ways.

**MEASURED** (decode3i twice, alike, under Python 3.14.6 -I -B; cuts3i twice, alike): sections 1, 2, 4, 5 and 6.
