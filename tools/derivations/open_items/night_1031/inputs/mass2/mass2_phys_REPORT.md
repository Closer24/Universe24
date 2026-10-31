<!-- Boss note, 2026-10-31 09:23 UTC (first labelled ~09:5x, ahead of the clock): written by the Boss from the reader's hand-back (the harness refuses report files from readers); the text below is the reader's, whole. Reader of MASS2 (frozen c41cbea6), the hostile physicist (MASS1's physicist). -->

(My harness refuses report files, so this is the whole report for the Boss to write into S/mass2_phys/REPORT.md. S = S.)

# The hostile physicist on MASS2 (the beats the structure fixes, and the mass reading in clicks), node-all 9d75a4904, 2026-10-31

**Read:** MASS2.md whole (618 lines, sha256 c41cbea6... matches); the brief's 08:3x, 08:4x, 08:5x and 09:0x rulings; the five probes and their outputs; my MASS1 report (S/mass1_phys/REPORT.md). I did not open the other reader's folder.

**Reruns, from a copy of the frozen folder** (S/mass2_phys/copy/, checked against FROZEN.sha256):
- lone.py: byte for byte the frozen out/lone_1.txt.
- beat_long.py: byte for byte the frozen out/beat_long_1.txt.

**My probe:** S/mass2_phys/p_m1_phase.py, run twice, byte-identical (sha256 1f040d7c80a8e7e1).

Every run was one process at nice 19 and started at a load of 8 or below.

VERDICT on MASS2: NOT PASSED

MASS2 meets every item of my MASS1 report. Two new items block:
- **B1:** the designs' thresholds are labelled DERIVED as necessary conditions, and MASS2's own runs show they are not necessary while the held count flickers. The owner's-batch question and a build item rest on that reading.
- **B2:** M1's calibre is a strictly periodic count's. Its pair verdicts flip with the window's start, so 1.3's "M1 fails for most pairs" holds at one start only, and MASS3 would build that calibre.

Both fixes are a paragraph each. The rest is sound, including the reading's new form (side by side at one Node-clock, one quantum per taker, the swap) and the measured beat.

## BLOCKING

**B1. The thresholds are necessary only for a held count held fixed** (verdict bullet 5: "needs |k|^2 > 0", "needs 2 c |k|^2 > tie"; 4.4: "that the thresholds are necessary is DERIVED"; Statuses).

What is derived:
- At k = 0 for good, the lone member is free.
- At a fixed 2c|k|^2 < tie, the pair falls (lone.py's (a) and (c)).

MASS2's own runs contradict "needs" on a flickering held count:
- **(b):** the lone member stays within -43 to 44 over 2,000 rounds while the held count is 0 in 558 of them.
- **The shipped pair** (beat_long.py, in its rounds 751 to 1,750), per 250 rounds:

| rounds | sum of held |k|^2 | 2c x mean |k|^2 (tie = 96,000) | most |v| |
|---|---|---|---|
| 751 to 1,000 | 189 | 90,720 | 10 |
| 1,001 to 1,250 | 191 | 91,680 | 6 |
| 1,251 to 1,500 | 189 | 90,720 | 6 |
| 1,501 to 1,750 | 180 | 86,400 | 11 |

The pair's difference v stays small while the mean curvature is below the tie in every window. So a threshold crossed round by round, or on the mean, unbinds neither design over the rounds read.

DERIVED here, which settles the necessary part exactly:
- The set "both held rows at 0, now and before" is invariant under the act: at k = 0 the force on k is 0, and with no force the carry gives q = 0 for any tooth.
- It is also invariant under the run back, since the mirror keeps it.
- The act is one-to-one (08:4x), so no other birth ever reaches that set, and none born there leaves it.
- So |k|^2 stays 0 for good exactly when the held hand is born there. Every other birth keeps it off 0 for good.

Consequences:
- 5.3's build item, "the held hand kept away from 0", needs no mechanism. A mechanism keeping |k|^2 > 0 at every round would be a bound in the act, which is unlawful.

Fix:
- State the thresholds as "held below them for good, the design falls" (DERIVED).
- Name the flicker's binding OPEN, with (b) and the shipped pair as the measured counter-cases.
- Strike 5.3's item.
- Reword the owner's-batch question as the held hand's birth (weighed below).

**B2. M1's calibre makes the pair verdicts depend on where the window starts** (1.2's M1, "each check's no DERIVED"; 1.3 and verdict bullet 4, "M1 fails for most pairs at the counts' calibre").

MEASURED (p_m1_phase, twice alike, the shipped lay on one Node-clock):
- The held hand's fast swing has half-periods of 4 to 5 rounds (187 of them in rounds 842 to 1,623).
- Shifting the start of beat_long's 391-round window by 0 to 39 rounds moves a window's own lines by 1 to 3: held 168 to 169, giver 166 to 167, taker 163 to 166.

M1 over those 40 starts:

| reading | at beat_long's start | at the 40 starts |
|---|---|---|
| held : giver | FAILS | holds at 33 |
| held : taker | holds | holds at 38 |
| giver : taker | FAILS | holds at 20 |
| held against its rounds | FAILS | fails at 34 |
| taker against its rounds | FAILS | fails at 38 |
| giver against its rounds | holds | holds at all 40 |

What this shows:
- "Fails for most pairs" is a reading at one start. At most starts most pairs hold.
- What stands is a drift that the held and taker clocks share against the board's rounds (their ratio holds at 38 of 40 starts). That is the shared drift MASS2's per-clock test was built to show, and it shows it.
- The calibre "each count +-1" fits a count whose window ends cut no faster swing. For clocks with a fast swing, M1's FAILS no longer implies a moving rate, so its no is not derived.
- "Each window holds whole beats" would also mean picking S's lays by the clocks' beat, which is a lay picked for a check's outcome.

Fix:
- Derive M1's calibre for a clock with a fast swing: each count +- its lines in one swing and one partial beat. Or read many beats with the calibre scaled.
- Report verdicts over the starts.
- Restate 1.3's conclusion as the per-clock drift.
- MASS3 builds this calibre, with a steady two-frequency test clock as the mutant that must pass.

## MINOR

- **m1 (1.2).** At one Node-clock the two designs share one held hand. Every tied train's curvature is 2c|k|^2 with one |k|, and the held curvature 2(s + c SUM|x|^2) reads every tied train's swing. So the one-Node-clock reading is of one coupled system: for alike members over the lone member, the ratio reads 1 + tie/(c|k|^2). Say which reading is the mass reading: two Node-clocks with the swap, or this one.
- **m2 (1.2, M2).** At one Node-clock the swap is the identity and cannot fail. Name it a check by construction, not a guard.
- **m3 (1.2, M3).** A clock that moves is not the decoder's (site, train) clock: a moving pattern is at no one site (FACE2 5.3). Until a moving clock's identity is owed and built, M3 is NOT READ by structure. Say so.
- **m4 (1.2).** "S lays one quantum per taker, to X at s1, to Y at s1'": a source does not address its taker; the act's edges do. The reading selects, in the record, the quanta S passed to X and to Y.
- **m5 (1.2).** "In the record's order": under 08:5x causal order is chains of meetings, so say "in X's own order (its chain)". For one clock's lines the two agree.
- **m6 (3.3).** The 561,909 comparison (MASS1 B1's sub-point, still standing) is of the held curvature over the tied one, which is neither named design's ratio. If any ratio sits beside 1,836, make it the two designs' ratio, 3.2(c)'s 1 + 3/(2f|k|^2 - 1), about 25 ppm. Or strike the comparison.
- **m7 (1.3; 08:5x).** Name that the shipped click world declares 5,000 ticks, runs 3,751, and gets no record from the runner. 1.3's lines are the probe's, as the record would write them for a prefix world.
- **m8 (1.2).** A three-member design's own count is undefined: X and Y are clocks (a site and a train each), and the proton's design is three clocks. MASS3 should name which count is the design's, for example its members' lines on its outer edges (the circulation's sides cancel, B C = 0).

## SOUND

- Every mass sentence now carries "only in a fit click form (OPEN)". "The board's mass" and the Yukawa analogy are struck. plans.py line 4 goes to the clean-up. Section 3 is clock facts.
- The reading's fix for depth is right:
  - side by side at one Node-clock gives one depth and one motion;
  - one quantum per taker;
  - the swap's two readings, (m_X/m_Y)(r_a/r_b) and its inverse, agree only if r_a = r_b;
  - each clock is also read against the links, so a shared drift shows (and it does, B2).
- **The beat (MEASURED, my rerun alike):**
  - u = x_g + x_t has five half-beats of 195 and 196 rounds (rounds 645 to 1,623, within 0.5%) while the held count is 0 or 1;
  - it walks to 77 to 93 at count 3, 55 to 56 at count 6, and 27 near count 7;
  - a count passes the width after round 3,751.
- **The lone member and the pair (MEASURED, alike):**
  - (a) at k = 0 the member runs 41 to 1,041 with V = 0;
  - (b) it stays within 44 over 2,000 rounds;
  - (c) the pair's v grows from 40 to 5,131,968 by round 1,000, about 3.5 times per 100 rounds, at root(tie/W) = 0.0126 per round.
- **Arithmetic checked:**
  - the (held, giver) minor: 392e6 x 120,000 - (9.6e6)^2 = -4.512e13, indefinite;
  - with every strength at 1, held over tied = 1,600 + 2/120,000;
  - 6 x 561,909 = 3,371,454, within 4 parts in 10^7 of nature's ratio, barred only by fake form 4;
  - 50,811,429 = 3 x 641 x 26,423.
- **Group theory (MEASURED, characters):** Frobenius-Schur is -1 for E1/2, E5/2 and G3/2, so the 8-gear train takes 1 beat, the 24-gear train at most 4, and the hand gives a, b, b.
- **Classical citations are right:** McMillan and QRT; the Neron-Tate height and Northcott; Mazur's 12; KAM.
- chance.py prints no product.

## The owner's-batch question, weighed: must the electron's design lay the held hand away from 0?

1. **The necessary part needs nothing from the owner but a birth.** By B1's derivation, the held hand stays at 0 for good exactly when it is born at 0, now and before. Any other birth stays off that state for ever, with no build item.
2. **Away from 0 does not bind the member by itself.** The held count passes through 0 in 16 to 81 of every 250 rounds on the shipped world, and binding under that flicker is OPEN (measured bound for 2,000 rounds).
3. **The value is not innocent.** Every tied train's curvature is 2c|k|^2, so the held count sets every tied train's beat scale, and at one Node-clock it sets the designs' ratio through 1 + tie/(c|k|^2).
   - A count picked for a beat or a ratio is fake form 4.
   - A count picked so that a lump holds is a number set for an outcome (08:5x).
   - If the owner names one, the lawful candidate is the unit the click world already lays (1, at rest), named as an initialization number like the key, with that weight stated.

## DERIVED / MEASURED / OVERCLAIMED

- **DERIVED:**
  - the checks' noes: M1 for a strictly periodic count only (B2), M2 at two Node-clocks, M3;
  - the Frobenius-Schur and Schur beat counts; one beat per tied train;
  - the triangle's split; B C = 0;
  - the line k = 0 invariant, and (mine) unreachable from any other birth.
- **MEASURED:** beat_long and lone, rerun alike from the copy; p_m1_phase (mine).
- **OVERCLAIMED:**
  - the thresholds as necessary on a flickering held count (B1);
  - "M1 fails for most pairs" (B2);
  - M2 at one Node-clock as a guard (m2);
  - 5.3's "held hand kept away from 0" (B1).

## My MASS1 items: met or not

| item | status | where |
|---|---|---|
| B1, board read as mass | met | 0, 3, 5.4 |
| B1 sub-point: the held-vs-tied pair is no design's | not met | m6 |
| B2, depth; a quantum taken twice | met | 1.2 |
| B3, the beat exists | met | 1.3; M1 over whole beats, with B2's residual |
| B4, the lone member bound at every size | met | 4.4; "sorts the designs" struck; B1's residual |
| m1 | met | 3.5 |
| m2 | met | 3.3 |
| m3 | met | 1.2, 1.3 |
| m4 | met | 2.2, 2.3 |
| m5 | met | 5.2 |
| m6 | met | 1.1 |
| Q1 | met | 5.4 |
| Q2 | met | 1.2 |
| Q3 | met | 4.3 |

## Questions for the Boss

1. Should the owner's-batch item read "the held hand's birth off its one invariant state, at the unit", with its weight (it sets every tied train's beat scale)?
2. Is M1's calibre for a clock with a fast swing MASS3's to derive, with its passing mutant?
3. Which is the mass reading: one Node-clock (one coupled system through the shared held hand), or two Node-clocks with the swap?

## Solution24

Keep MASS2's form: beats as clock facts with the bridge to masses OPEN, the reading side by side with the swap, and the beat read as it walks. Before MASS3 builds it:
- state the designs' thresholds as "held below for good" (the birth decides the necessary part);
- give M1 a calibre that carries the fast swing;
- send the held hand's birth to the owner as an initialization number, with its weight stated.
