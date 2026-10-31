<!-- Boss note, 2026-10-31 10:12 UTC: written by the Boss from the reader's hand-back (the harness refuses report files from readers); the text below is the reader's, whole. Reader of DECODE3h (frozen 7f7d3d63), the hostile physicist (the HALF pair's physicist). -->

This session's harness refuses report files from subagents, as it did with my earlier REPORT.md writes. The whole report is below, for the Boss to write to S/decode3h_phys/REPORT.md.

# The hostile physicist (HALF pair) on DECODE3h (the decoder's readings of the three clicks, eighth text), 2026-10-31

**Read:** BRIEF_PAIRS.md from 08:4x to its end, including:
- the owner's answers of 09:30;
- his law of 09:04;
- DECODER-CUT (09:59);
- the coordinator's added press from the owner's question to David: Bell "from the past and also from the future".

Also read: DECODE3h.md whole (461 lines; FROZEN.sha256 80 of 80 OK) and my DECODE3g report. I did not look in decode3h_math/.

**Reruns:** from a copy of the frozen folder at S/decode3h_phys/rerun/. One process at a time, nice 19, each run started with the load under 8, the live venv's Python 3.14.6 -I. Both reproduce byte for byte:
- cuts3h.py rewrites readings3h.json identically. My first call passed it no output name and exited 1; rerun properly.
- decode3h.py matches run1 (130 s).

**My probe:** S/decode3h_phys/future.py, run twice (future_run1.txt = future_run2.txt). It runs decode3h.py's own definitions unchanged: its head, its R3, and section C's to_lines, mates, from_lines, order_e, joint_past, r4h and ladder_once. Whole numbers only, Rule3's carry the one division.

VERDICT on DECODE3h: NOT PASSED

It meets every item of my DECODE3g report. Two new BLOCKING items: R4 reads the past side only, and R3 has no passing to read in a record of q alone.

## BLOCKING

**B1. R4 presumes a law that writes clicks from the past side only** (section 3, lines 284-296 and 328-330; section 6 item 4).
- **What R4 reads back only:**
  - its lag tests read each outcome against its own setting and outcome L pair events back;
  - its joint past reads the place's last L settings and outcomes;
  - only the five 2 x 2 tests touch a later setting, and only at lag 1.
- **What it must read.** The owner's law of the choice reads "not its past and not the future". His question to David asks whether Bell's correlation may come "from the past and also from the future". So R4 must read a law that writes clicks from the start, from the end, or from both.
- **MEASURED (future.py)**, on two forms with no draw, mirrored in time, each with the hand unturned and B as the toy's:

| form | R3 beside | S per half | click parts | R4 |
|---|---|---|---|---|
| "two ahead": A's outcome is its own setting two pair events later (a function of A's own teeth now, so a local act) | SHOWN at both places | 2,499, 2,499 | SHOWN | NOT READ, as the third click |
| "parity of the next two settings" | SHOWN at both places | 2,499, 2,499 | SHOWN | NOT READ |

- **Fix:** mirror the order readings.
  - Add each outcome against its own setting L pair events ahead (L = 1, 2, 4, 8). It refuses "two ahead": z^2 19,998,000 at A's setting 2 ahead.
  - Add a joint-future ladder: the next L settings and outcomes, with the present setting. MEASURED: [8, 0, 0, 0] at A on both future forms, refused.
  - On the toy's third click both pass: the largest lag-ahead z^2 is 4,542 against 11,452; the joint future reads [8, 32, 512, 750].
  - Count the added tests in N_T.

**B2. R3 has no input in a record of q alone** (section 2; section 6 item 2; R3 beside (c) in item 4; section 5, lines 393-399).
- **The owner's answer (Q11):** "the record writes lines and sides, q alone; no tooth, birth or end tooth is written ... the code checks that read them read the board's own state."
- **What R3 needs.** (3b), (3d) and (3e) read each side's passing per round. R3 beside (c) reads each place's passing per pair event. Neither field is in a q-alone record (DECODE3f's writer-C board field cannot be written).
- **What section 5 covers.** It sends the teeth checks, and R2's passing-given chance, to the board's own state. It does not send R3 there.
- **Fix:**
  - R3 and R3 beside (c) leave the decoder's settled list. They become board checks of the run tool, reading the board's own state.
  - The pair record carries no passing.
  - Name every passing reader so.

## MINOR

1. **R2 per side under Q10** (section 1, lines 234-235; section 5).
   - The owner: "a clock reads only its own clicks ... Its sides and the board are not 'what a clock can read'."
   - The per-side R2 reads a side at the clock's clicks. Rename it the decoder's reading of a side, not "the clock's own click past".
   - The per-clock form needs no new law: R2's ladder and own-count gate on the clock's own lines' q per own click. It can be built now, not left to Big Pic.
   - Likewise, the joint past reads the place (two clocks). The outcome clock's own past under Q10 is (e) and its outcome lags. Section 5's "'nothing a clock can read' is read through those clicks" should name the two readings apart.
2. **The rate's NOT READ is honest but measurable now** (section 3, lines 355-358; OWED at 442).
   - MEASURED (future.py, decode3h's own ladder_once at N_T 70, fair counts): the summed joint-past gate is 14,099 per million against its share of 714 at 2,000 pair events a half, and it opens by 2,500.
   - So a stand-in record of 5,000 pair events gives the OWED rate today, with no world needed. Name the threshold.
   - On the worlds we have, no world hosts Bell (09:4x), so R4 reads NOT READ there by name, whatever the gate.
3. **The seeds' law's constraint is overclaimed** (lines 328-330). The text says the order readings "refuse any dependence across pair events". They refuse the past side, and the future side's settings only at lag 1 (B1). After the mirror, the constraint holds both ways.
4. **A start-only phrase in a quoted ruling.** The 08:5x phrase in (b), quoted from DECODE3g's section 0, reads "the law named in the initialization": a start. The 08:4x ruling leaves the law's place OPEN (the start, the end or the pair events), and the owner's 09:33 word puts the end form first on Big Pic's bench. Flag it for the Boss.
5. **The free-lay control's laying** (lines 318-326). Laid at the start (born at the middle), it reads the same bound as a member laid at the end (ending at the middle), by the exact run back (L7). Say so, so that the control serves an end-form law too.
6. **The pin fails on its own folder.** The frozen folder fails its own nl.sha256 on 3 of 41 files: the 3.14 bytecode under nl/src/.../__pycache__, rewritten at 09:45:37, 24 s after the pin (09:45:13). The sources all pass. Pin the sources only, or run with -B.
7. **DECODER-CUT (09:59, after the freeze; travels as a note).** The seven settled items are new decoder readings. Each enters the build only within the decoder's target or with a reading cut of its size. R4 alone holds 70 to 82 tests a record. Name each item's size or its cut.

## SOUND

- **R2:**
  - the gate is taken from the clock's own counts, and the passing-given chance stands beside it and never gates;
  - the rung-1 closed forms (no "11", no "00", no "10", no "01") are checked against the recursion for N up to 16, with 0 disagreements;
  - every side is read;
  - the mathematician's three rows now refuse none.
- **R3:**
  - (3b) is read against the chi-square on K degrees at two tails per K, with the cuts from the readings file, checked;
  - the carried no holds at the lower cut, Z < B <= lo_K (DERIVED);
  - the rate is 33 to 51 per 1,000, MEASURED, with the union bound named conditional.
- **R3 on W and (3p)** are moved to Big Pic's bench; the W field is struck; the order-2 memory stays a bench measurement.
- **R4:**
  - the lags at 1, 2, 4 and 8, back, refuse "two back" flipped one in ten and two in ten;
  - the free-lay control as ruled (the member born at the middle: S -27 and 7) with the local act at S = 2 exactly beside it, so (a) is tested at its edge;
  - the pair record is written as meetings on both sides, the bearing meeting included. The guard's mates read, and 40,000 pairs are read back from lines and sides alone; my probe confirmed both.
- **The rest:**
  - the chain rule (i), "strictly later", in force, with (s) a board check;
  - "two rates", and the interval rule on its click-world reason;
  - D4 a static check, with the mutant as its no;
  - the teeth and the silent worlds out;
  - no cut on the sizes of q;
  - the significance levels named as conventions.

## DERIVED / MEASURED / OVERCLAIMED

- **DERIVED (sound):** the rung-1 closed forms; the carried no at the lower cut; the chi-square CDF forms; the interval rule on its click-world reason.
- **MEASURED:** the text's sections 1 to 4, reproduced byte for byte. The reader's own:
  - "two ahead" and "parity of the next two" pass R4's click parts;
  - the mirrored readings refuse both;
  - the summed gate opens between 2,000 and 2,500 pair events a half.
- **OVERCLAIMED:**
  - the lag tests' reach (back only);
  - the seeds' law's constraint ("any dependence");
  - R3 as a decoder reading after Q11;
  - the per-side R2 named "the clock's own click past".

## My DECODE3g items, one by one

| DECODE3g item | met? | where in DECODE3h |
|---|---|---|
| B1, R2's gate | met | section 1 |
| B2, R3 on W and (3p) | met | section 2 |
| MINOR 1, the free-lay control | met | section 3 |
| MINOR 2, the seeds' law's constraint | met | named, with its scope per MINOR 3 above |
| MINOR 3, "deeper" | met | "two rates" |
| MINOR 4, the interval rule's premise | met | |
| MINOR 5, R3's level | met | |
| MINOR 6, the chain rule | met | (i) in force |
| MINOR 7, the record as meetings | met | |
| MINOR 8, the interpreter | met | |

## Questions for the Boss

1. Does R4 read the order both ways, with lags ahead and a joint future, counted in N_T, so that it reads a law from the start, from the end or from both?
2. Do R3 and R3 beside (c) leave the decoder for the run tool, reading the board's own state, now that the record holds q alone?
3. Under Q10, is R2 on the clock's own lines the per-clock form, built now, with the per-side R2 renamed?
4. Does "the law named in the initialization" read "where it is laid: the start, the end or both"?

## Solution24 (the reader's line)

DECODE3h settles the decoder's rules nearly whole. Two things remain. R4 must read the future as it reads the past, because the owner's law and his question to David name both; mirrored, it refuses every drawless form built so far and passes the third click. And R3, a board check, goes to the run tool, since the record now holds q alone.
