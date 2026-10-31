<!-- Boss note, 2026-10-31 09:36 UTC (first labelled ~09:5x, ahead of the clock): written by the Boss from the reader's hand-back (the harness refuses report files from readers); the text below is the reader's, whole. Reader of DECODE3g (frozen 083032b0), the hostile physicist (the HALF pair's physicist). -->

This session's harness refuses report files from subagents, as it did for my earlier REPORT.md writes. So the whole report is below; the Boss can write it to S/decode3g_phys/REPORT.md.

# The hostile physicist (HALF pair) on DECODE3g (the decoder's readings of the three clicks, seventh text), 2026-10-31

**What I read:** BRIEF_PAIRS.md to its end (the 08:4x to 10:1x rulings, the owner's word of about 09:05); DECODE3g.md whole (574 lines); my DECODE3f report. FROZEN.sha256 checks OK throughout. I did not look in decode3g_math/.

**Reruns.** From a copy of the frozen folder at S/decode3g_phys/rerun/, one process at a time, nice 19, each started with the load under 8, the live venv's Python 3.14.6 -I. cuts3g.py, grain_ca.py, gate_open.py and decode3g.py (164 s) all reproduce their frozen run1 byte for byte. The deriver ran 3.13.17; the 08:5x ruling asks for 3.14; the outputs agree.

**My probe:** S/decode3g_phys/r2_gate.py. It reuses decode3g.py's own two_sides, no_pair_chance_ok and r2_own, unchanged. Run twice; r2_gate_run1.txt and r2_gate_run2.txt agree byte for byte. Whole numbers; Rule3's carry the one division.

VERDICT on DECODE3g: NOT PASSED

Every item of my DECODE3f report is met, and sections 0 and 6 are well made. Two BLOCKING items stand, each in the "settled, to be built" list. Since a passed rule becomes a build item, both must be fixed before the list is built.

## BLOCKING

**B1. R2's gate reads the board's passing, so R2 is not a click reading as it is to be built** (section 1, lines 177-191; section 6 item 1).
- **The conflict.** The 09:5x ruling: "A click reading uses the clicks alone, with no board premise." DECODE3g calls the gate "a board check beside the click reading". But the gate decides whether R2 is read at all, so R2's verdict is a function of each side's passing per round, which is a board field.
- **The rest of the text gates differently.** R4's ladders ((e) and the joint past) are gated "from the half's own counts", click-only.
- **MEASURED (r2_gate.py), a gate from the clicks alone.** I set beside the board gate the exchangeable chance, given the half's N clicks of the clock and the n of them with side 1, that no two side-1 clicks stand in a row: C(N - n + 1, n) / C(N, n), read where it is at most 1/20. On the text's five section-B cases, 200 fair draws each:
  - the two gates decide alike on 2,000 of 2,000 halves;
  - R2's verdicts are identical: SHOWN 200 on each of the four read cases, NOT READ 200 on the gate's no (side 1 at 8, side 2 at 300).
- **Fix:** gate R2 on the clock's own counts, as above, and keep the passing-given chance beside it, named as a board check.

**B2. The settled list builds R3 on W and (3p), but the 10:1x rule 5 withdraws W from the record** (section 2 and section 6 item 2; DECODE3f's "W, carried at the triangle ... writer C's click-world field", kept by DECODE3g, which does not replace it).
- **The ruling.** 10:1x: "Rule 5 (the record has two levels, lines and sides) withdraws NATURE1's writer item 6 (W in the record apart from the sides). The third click is read only by a reading the first click's record fails: OPEN, Big Pic's."
- **What this blocks.** R3 on W and (3p), the member's period at a steady stretch, read a W that no record will carry.
- **Fix:**
  - Move R3 on W and (3p) to the open list, as bench readings of the member, Big Pic's.
  - Strike DECODE3f's W field from writer C's list.
  - Keep section 2's measurement of THIRD7's order-2 memory as a bench measurement.

## MINOR

1. **The free-lay control is not the ruled one, and it cannot fail where it matters** (section 3, line 353; table row; section 6 item 4).
   - The rulings name it "the member born at the middle" (08:4x, 08:5x). rec_free_lay is a stand-in instead: the toy's teeth born from a shared lay.
   - It reads S 143 to 279 per mille, far below 2. A reading that inflated S would still pass it.
   - Fix: lay the ruled member at both places, and add a local act at the bound (S = 2 exactly), so the control is "a test that can fail" (Big Pic's condition).
2. **Under (C), the order readings constrain the seeds' law** (section 3).
   - The five 2 x 2 tests, the two own-past tests and the joint past read the settings against past outcomes and the outcomes against past settings.
   - So a seeds' law whose dependence reaches across pair events would be refused by them.
   - Name the constraint they set on the law (dependence within each pair event only), for Big Pic.
3. **C-d's "deeper" reads "counts less at rest"** (section 4, lines 453-455; the D table).
   - With the own count read as a clock's lines, a quieter clock at one depth reads deeper. The well's depth beside it is what tells them apart.
   - My own configurations, which the table cites, were mislabelled by me: my "two depths" (A at 2 of every 3 rounds, B at 3 of every 4) are two line rates, not depths. I correct it here.
   - Fix: name the premise as clocks of one kind with one activity, and relabel the rows "two rates".
4. **The interval rule's premise holds only for steady clocks** (section 4). "Each own count is the true count within one" holds for a balanced (steady) line word; with moving passings the true count is undefined. Name it.
5. **R3's union bound is DERIVED only given each test's level** (section 7). (3b)'s cut is not at its level: 21 to 30 per 1,000 against its share of 16.7. State R3's family-wise level as MEASURED, 44 to 64 per 1,000, with the union bound conditional (as section 2 already names the excess).
6. **The chain rule** (section 3, NATURE3). The text names both variants and decides neither, as asked; but say what the rulings in force read.
   - The 07:5x rule as DECODE3f quotes it ("each next link ... at a strictly later round") reads variant (i).
   - So does the 08:5x islands ruling's own split, 114 / 62 / 187, which section 0 quotes.
   - There is also a physics reason: within a round no click depends on another (each passing reads the round's board window, and a click writes nothing into the gears), so a same-round chain links no cause to an effect.
7. **The click-form pair record** (section 3, lines 316-323; to_clicks and from_clicks).
   - Each meeting is written as one line, with no mirror line at the partner, so E's guard (sides.paired) would refuse every line as a broken mate.
   - The bearing meeting sits in a side table, not in lines. from_clicks reads each pair's source from that table, so "read back from the lines alone" is not so.
   - The toy's bearing meeting stands in the outcomes' own round, at a third place.
   - Fix: write both sides of every meeting, the bearing meeting included (the record's two levels), and name the toy's round trip a format test.
8. **The interpreter.** Lines 19-20 name Python 3.13.17 against the 08:5x ruling's 3.14. My 3.14 reruns agree byte for byte; name it.

## SOUND

- **Section 0 quotes the rulings verbatim** (09:1x), and section 6 splits settled from open, with each open item named as Big Pic's.
- **R2 per clock in its own count:**
  - a one-sided clock reads NOT READ by name (DERIVED);
  - the transfer recursion is exact;
  - the gate's no works: the chance is 665 thousandths there, and without the gate the ladder refuses 181 of 200 right records.
  - The carried swing-plus-steady clock reads R2 SHOWN, named so, refused by R3 beside it.
- **R3:** the three cuts sit in the readings file and are checked; the carried no holds at the moved gate; the two-values rule is used only at ten; R3's rate is named and (3b)'s cuts are OPEN.
- **R4 under (C):**
  - it reads NOT READ by name until the seeds' law exists;
  - (c) is gated on a click reading, with R3 beside it;
  - every row says where its settings come from.
  - My "two back" and "parity of two" are refused by the joint past ([8, 0, 0, 0]).
  - Lines 257 and 239 are struck.
  - The rate is honest: 22 NOT SHOWN and 978 NOT READ of 1,000 right records at 2,000 a half; the gate opens near 2,400.
- **D4's no is computed:** a mutant C-a on rounds reads 11 against 7 and is refused.
- **The interval rule:** 0 false refusals on my 2,700 configurations. C-c's reciprocity fails truly where the rates differ. C-e takes the tolerance form.
- **Also sound:**
  - the Mesh meeting is named a departure from "at one place", for the owner's batch;
  - NATURE3's board-coupling gap is named on both worlds;
  - one key per record runs through D = (kappa div senses) K;
  - one precedence holds at every level;
  - no click reading reads a tooth, and no sentence puts light or matter on the board.

## DERIVED / MEASURED / OVERCLAIMED

- **DERIVED (sound):**
  - R2 NOT READ on a one-sided clock;
  - the exact transfer recursion;
  - the carried no at the moved gate;
  - the interval rule never refusing a right steady record;
  - CHSH at most 2 with settings independent of the hidden part;
  - C-e's exact equalities having no whole solution.
- **MEASURED:** the text's sections 1 to 5, reproduced byte for byte. The reader's own: the clicks-only gate agrees with the board gate on 2,000 of 2,000 halves.
- **OVERCLAIMED:**
  - R2 as "the click reading" behind a board gate (B1);
  - R3 on W as a settled build item (B2);
  - "read back from the lines alone" (MINOR 7);
  - "deeper" from own counts (MINOR 3);
  - R3's union bound as unconditionally DERIVED (MINOR 5).

## My DECODE3f items, one by one

| DECODE3f item | met? | where in DECODE3g |
|---|---|---|
| B1, drawless forms | met | the joint past (section 3) |
| B2, Bell in the clicks | met | (c) gated on a click reading; settings and pairs as clicks, format per MINOR 7; road (C); line 239 struck |
| B3, D4 and R2 | met | D4 by computation; R2 in its own count (its gate per B1 above) |
| B4, the grain | met | the interval rule |
| MINOR 1, (b)'s two names | met | |
| MINOR 2, C-a's premise | met | |
| MINOR 3, the across field | met | |
| MINOR 4, the Mesh meeting | met | |
| MINOR 5, line 213's reach | met | |
| MINOR 6, the split-click column | met | |
| My five questions | ruled at 08:4x | folded |

## Questions for the Boss

1. Is R2's gate taken from the clock's own counts (B1), so that R2 is a click reading by the 09:5x rule?
2. Does R3 on W, with (3p), leave the settled list for Big Pic's bench under the 10:1x rule 5?
3. Is the free-lay control the ruled member born at the middle, with a local act at the bound beside it?
4. Do the rulings in force (07:5x, "a strictly later round"; the 08:5x split) already read NATURE3's chain-rule variant (i)?

## Solution24 (the reader's line)

DECODE3g settles most of the decoder's rules. Three things remain:
- R2 must read the clicks alone, which its own counts allow;
- R3 on W must go to Big Pic's bench with the third click's reading;
- under road (C), the pair record must be written as meetings on both sides, with a control that can fail at the bound.
