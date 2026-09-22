# Series R: the quarks

Since 2026-09-22 the law's drive of a body is the line drive (the model
owner, record 972; [docs/designs/drive_b/DEFAULT.md](../../../docs/designs/drive_b/DEFAULT.md)),
and the seven worlds declare no drive key (the transient `per_axis_drive`
of the flip day left them at the series' re-pin, DEFAULT.md section (c)).
The rows of 2026-09-21 below were read under the per-axis drive of history
and stand as history: `expectations.json` names the drive (`drive`), pins
the kicked u's pace under both (`kick_pace`, GAMEBOARD: 0.1635 on a
heading, a Link every 6.1 intervals; 0.1853 and 5.4 per axis) and keeps
every world's replay block of 2026-09-21 under `former`, replayed
bit-exact under the world key `per_axis_drive` by the test's (f); the
`replay` blocks are the engine's under the law's drive, written by
`replay_register.py` before the run. The pushes are the design's integers
under either drive (a push is a row's label); what the drive moves is the
ticks of the steps and the hand-overs.

Seven worlds of one base, written by `make_worlds.py`; the register entry
is [R, the quarks (2026-09-21)](../../../docs/EXPERIMENTS.md#r-the-quarks-2026-09-21)
and the design is [the quarks as families of the family table](../../../docs/designs/quarks/QUARKS.md)
(the physicist, read-only, 2026-09-21, on the model owner's direction of
records 249, 251 and 256 of the log of 2026-09-20; the run on the owner's
standing go, record 264). The question, in the owner's words (translated):
"try to add the quarks too: model them and bring them in, so that we try
to give their masses and their properties as well; bring them into our
groups; ... check how it converges"; "the quarks get the same binding we
have, the ordinary binding; they just need to be another family". Nothing
was added to the law: the quarks are rows of the family table with the
keys it has, and the binding is series I's (the strong column of a held
unit of a strong family, the contact through the table, the lifetime as
the range; [BEAM_LAW note 31](../../../docs/BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)).
A research run, made once, never a test; the expectations were written
before the run (the design's section 4.7; `expectations.json` beside the
worlds, derived by the design's `quark_numbers.py` and compared by
`tests/test_quarks_expectations.py`); a reading outside its expectation
is reported with its numbers, never moved. Every number is a DETECTOR
reading (the bodies' own `read` and `contact` records, the border's
clicks, the content the bodies hold) or a GAMEBOARD reading (the bodies'
steps and separations) ([the register](../../../docs/EXPERIMENTS.md),
"Two kinds of readings"). No detector is declared on these GameBoards.

## The base

Series I's ([the nucleus](../nucleus/README.md)): an open cube of 21^3
Nodes, `"law": "beam"`, K 2^20, N 64, `suspension` 0, `release` [1, 1],
the fan of the 290 primitive directions with |a| + |b| + |c| <= 6, 3000
intervals; the width S = 2^37 (W = 64 S M = 4.4 x 10^13 label units on a
body of 5 units against a push of 4 x 10^11 per interval: series I's slow
regime, the first attempt at a step about sixteen intervals after the
pushes begin), 2^30 in the dressed world. Three free families without a
phase circle: `u` (4 units of content, the charge per unit 1224: the whole
charge 4896 = 2/3 of the register's proton 7344), `d` (9 units, -272: the
whole charge -2448) and `glue` (the column `strong`, the value 10000 per
unit with the sign minus, `lifetime` 3; in the dressed world the pair
[10000, 606], so that 606 units held carry the strong charge 10000 as one
unit does). A quark is a body of `u` or `d` holding one unit of `glue`
(606 or 607 in the dressed world): the charges (M, Q, G) = (5, 4896,
10000) for u and (10, -2448, 10000) for d. Every body releases one row of
its held content per direction of the fan per interval. The push per
interval between two bodies within the reach is `(Q_A Q_B - G_A G_B -
M_A M_B) x U(r)` per unit per direction (U(1) = 3008 on the x axis, 2598
on y, 2336 on z: the flight table's tie, x first); u d binds electrically
already, u u needs sigma above 4895, d d above 2447, so the register's
10000 binds every pair. Under the contact through the table every refused
step hands the momentum component to the occupant.

| World | What |
| --- | --- |
| `q1_proton_line` | u d u on the x axis (the odd quark in the middle) |
| `q2_neutron_line` | d u d on the x axis |
| `q3_proton_triangle` | u u d on the face-diagonal sublattice, mutual sqrt 2 (the shape whose stabiliser in the cube's 48 is S_3) |
| `q4_deuteron_rectangle` | u d u over d u d at one Link (two lines side by side on y) |
| `q5_deuteron_line` | u d u d u d on the x axis (two triples end to end) |
| `q6_proton_kick` | q1 with the end u kicked -x by 10^13 label units (what the law does not confine) |
| `q7_proton_dressed` | q1 with the glue 606, 607, 606 held at [10000, 606] (the read mass 1836 by declaration), S = 2^30 |

## The expectations, pinned before the run (the design's section 4.7; `expectations.json`)

The push per body is derived (the one coupling over the columns with the
fan's delivery from the flight table), the border's rows and the read
mass are derived (290 rows of glue per body per interval; the exact sum of
the declared contents), the fates are the strong design's toy (the fan's
steady delivery with the step drive and the contact rule over 3000
intervals: a line holds, a corner, a triangle and a side-by-side rectangle
shear), which the engine decides. Since 2026-09-21 every world's `replay`
block pins the engine's record of its first 100 intervals by kind (the
steps with their Nodes and the hand-overs, GAMEBOARD; the face clicks of
the bodies that left, DETECTOR), written from the engine as shipped by
`replay_register.py` and replayed bit-exact by
`tests/test_quarks_expectations.py` (e); the fate's `engine_first_step`
is the replay's first step. The crossing rule (BEAM_LAW note 48, PR #468)
moved these readings after the register was written: the kicked u of
`q6_proton_kick` steps at 6, 12, 19, 25, 32, 38, 45, 51, 58 (6 and 7
intervals alternating; before the rule every 7: 6, 13, ..., 62) and clicks
through `face:-x` at tick 64 (69 before); the first hand-over of
`q1_proton_line` is at tick 18 (17 before), of `q2_neutron_line` at 23
(22), of `q7_proton_dressed` at 17 (16); the pushes at the reference tick
are unchanged ([MIGRATION](../../../docs/MIGRATION.md)). The 3000-interval
readings of the table below are of the run before the rule.

| World | Expected (kind) |
| --- | --- |
| `q1_proton_line` | the push per interval at tick 20 on the ends +-416 530 868 696 on x, on the middle 0 (DETECTOR); no step in 3000 intervals, hand-overs from about tick 17, the label 0 after each (GAMEBOARD, DETECTOR); 870 glue rows on the border `lifetime` per interval from tick 4, no `u` or `d` row on it (DETECTOR); the read mass 20 units at every tick (DETECTOR) |
| `q2_neutron_line` | the ends +-435 372 008 672; no step; hand-overs from about tick 22; 870 rows; the read mass 25 |
| `q3_proton_triangle` | the pushes at tick 20 (-46 833 992 744, -55 544 787 168, 126 813 807 239), (148 740 759 524, -116 576 861 778, -66 677 616 293), (-101 906 766 780, 172 121 648 946, -60 136 190 946) (DETECTOR); disperses: the first step by tick 25 to 60, the three beyond three Links of each other (GAMEBOARD); 870 rows; the read mass 20 |
| `q4_deuteron_rectangle` | the pushes at tick 20 (514 900 489 024, 384 064 524 729, 0), (0, 486 661 618 356, 0), (-514 900 489 024, 384 064 524 729, 0), (550 101 777 180, -402 779 816 516, 0), (0, -449 231 033 022, 0), (-550 101 777 180, -402 779 816 516, 0); the sum over the proton's three 1 254 790 667 814 on y (DETECTOR); disperses: the first step at about tick 160 (GAMEBOARD); 1740 rows; the read mass 45 |
| `q5_deuteron_line` | the pushes 419 551 209 892, 101 923 625 280, 3 787 403 148, -3 787 401 568, -81 931 883 236, -439 542 951 616 on x; the sum over a triple +-525 262 238 320 (DETECTOR); no step, about 950 hand-overs (GAMEBOARD); 1740 rows; the read mass 45 |
| `q6_proton_kick` | the push at tick 2 on the ends +-336 852 257 664 (the one-Link lines alone; DETECTOR); the kicked u steps -x at tick 6 and then every 6 or 7 intervals (the replay's exact ticks), its push falling to the electric residual beyond the reach, out through `face:-x` at tick 64 (the toy's about 70 to 90; GAMEBOARD, DETECTOR); the other two a bound pair; 870 rows per interval from tick 4; the read mass 20 |
| `q7_proton_dressed` | the ends 418 547 308 612 (or 613, the accumulator's one unit on the d's non-whole strong charge); no step; the read mass 1836 |

The criteria of the readings tool (`tools/quarks_readings.py`): a record
check (every run completed, the books balanced at every tick) fails the
tool; every reading above is registered inside or outside and never
moved.

## The worlds

```bash
python examples/events/quarks/make_worlds.py
PYTHONPATH=src python tools/run_series.py --jobs 2 --out artifacts/quarks examples/events/quarks/q*.json
PYTHONPATH=src python tools/quarks_readings.py artifacts/quarks
```

## What was measured (2026-09-21)

`tools/run_series.py --jobs 2`, the seven worlds at 3000 intervals on the
worktree `quarks-design` (the pins committed at `eba635dd` before the
run, the design's base main `25a62924`), the project's environment
(Python 3.14.0rc2, numpy 2.5.3), four cores, two jobs: every run
completed with the books balanced at every tick, 10 min 37 s of wall
time for the seven (the runner's seconds per world in the table, 20 min
in all), the peak resident set below 1.8 GB. `tools/quarks_readings.py`:
0 record checks failed, 55 readings inside, 0 outside among the tool's
pins (the pushes, the border, the read mass, the fates, the books);
two of the page's pins on the kicked world read outside (the table) and
are reported, not moved. The records stay under `artifacts/` (not
committed; the events files deleted after the reading, the summary and
`readings.txt` kept).

| World | Expected (kind: DETECTOR unless a step or a separation, GAMEBOARD) | Measured | Verdict |
| --- | --- | --- | --- |
| `q1_proton_line` | the ends +-416 530 868 696, the middle 0; no step; hand-overs from tick 17, the label 0 after each; 870 glue rows, no `u` or `d`; the read mass 20 | the ends +-416 530 868 696 exactly, the middle 0; no step in 3000 intervals; 411 hand-overs (398 from the left u from tick 17, 13 from the right u from tick 242; the toy's 412), the largest 6 664 493 899 136 (the toy's integer); 870 glue rows at tick 20, no other family on the border; the read mass 20; the books balanced; 186 s | inside (7 of 7) |
| `q2_neutron_line` | the ends +-435 372 008 672; no step; hand-overs from tick 22; 870 rows; the read mass 25 | +-435 372 008 672 exactly; no step; 318 hand-overs (290 from tick 22, 28 from tick 126; the toy's 319), the largest 9 142 812 182 112 (the toy's); 870 rows; the read mass 25; 183 s | inside (7 of 7) |
| `q3_proton_triangle` | the three push vectors of the design; disperses, the first step by tick 25 to 60, the three beyond three Links, out through the faces; 870 rows; the read mass 20 | the three vectors exactly; disperses: the first step at tick 27 (the second u; the toy's 25), 51 steps in all, 4 hand-overs, the largest separation 21.2, all three out through the faces (the board empty by the end, the last on (7, 7, 20), (20, 11, 6), (8, 14, 0)); 870 rows; the read mass 20 with what left through the faces; 20 s | inside (7 of 7) |
| `q4_deuteron_rectangle` | the six pushes of the design, the sums +-1 254 790 667 814 on y; disperses, the first step at about tick 160; 1740 rows; the read mass 45 | the six pushes exactly; disperses: the first step at tick 176 (the upper middle u; the toy's 161), 127 steps, 279 hand-overs, the largest separation 25.3, all six out through the faces; 1740 rows; the read mass 45; 123 s | inside (10 of 10) |
| `q5_deuteron_line` | the six pushes of the design, the sum over a triple +-525 262 238 320; no step; about 950 hand-overs; 1740 rows; the read mass 45 | the six pushes exactly; no step in 3000 intervals; 963 hand-overs (200, 316, 301 and 146 on the four inner bodies from ticks 17 to 27; the toy's 954), the largest 12 931 222 766 152 (the toy's 13 452 697 595 604); 1740 rows; the read mass 45; 420 s | inside (10 of 10) |
| `q6_proton_kick` | the push at tick 2 +-336 852 257 664; the kicked u steps -x at tick 6 and every seven intervals, out through `face:-x` at about tick 70 to 90 with its 2/3 e; the other two a bound pair; 870 rows; the read mass 20 | +-336 852 257 664 exactly at tick 2; the kicked u steps -x at ticks 6, 13, 20, 27, 34, 41, 48, 55 and 62 (every seven exactly), reaches the face at 62 and leaves through `face:-x` at tick 69 (the register's commit eba635dd replayed; this row's earlier run read 63) with its content 4 + 1 glue (the face's `measured_content`), OUTSIDE the pinned 70 to 90 by one interval (the toy's steady delivery begins one tick late and reached nine Links at 78); the other two drift -x as a pair at one Link (the d steps at 358, 618 and 1081, the u follows eleven to thirteen ticks later; 67 hand-overs on the d) and BREAK at about tick 1190 (the d steps +z at 1166, the u then steps -x from 1179 and the separation grows from 1 to 3.2 by tick 1200), the u out through `face:-x` at 1253 and the d through `face:-z` at 1434: OUTSIDE the pin "a bound pair" (a u d pair alone drifts by the third-law gap of unequal contents and breaks off the axis); 870 rows; the read mass 20 with what left; 61 s | inside (5 of 7); OUTSIDE 2 (the exit tick, the remaining pair), reported, not moved |
| `q7_proton_dressed` | the ends 418 547 308 612 or 613; no step; the read mass 1836 | 418 547 308 613 (the accumulator's one unit on the d's non-whole strong charge, as pinned); no step; 435 hand-overs (408 from tick 16, 27 from tick 119; the toy's 437), the largest 6 278 209 629 195 (the toy's 6 278 209 629 180); 870 rows; the read mass 1836; 233 s | inside (7 of 7) |

**The verdict (R).** The engine's push on every body at the reference
tick equals the design's integer exactly in every world (the dressed
world to the accumulator's one unit, as pinned): the formula gave, the
run proved. Three quark bodies under the strong column sigma alone, the
contact rule and the lifetime converge to a bound set in a LINE and in no
other shape: the proton line u d u and the neutron line d u d hold 3000
intervals with no step, their hand-over counts and largest labels the
toy's integers; the face-diagonal triangle (the shape that carries S_3)
shears from tick 27 and the side-by-side rectangle from tick 176 (the
toy's 25 and 161), every body out through the faces. The tower composes
in the collinear shape: the line of six u d u d u d holds 3000 intervals
(963 hand-overs) while two lines side by side do not. The law binds and
does not confine: the kicked u walks off at one Link per seven intervals
and leaves through the face at tick 63 with its charge 2/3 e, and the u d
pair it leaves behind drifts and breaks at about tick 1190, a finding
outside the page's pin (a pair of unequal contents drifts by the
third-law gap of the fans and breaks once off the axis). The mass a
detector reads of the bound set is the exact sum of the declared
contents in every world (20, 25, 20, 45, 45, 20 and, dressed, 1836):
nothing in the run raises a bound set's mass above its parts, the
proton's 99 % binding is not in the law. Nothing was tuned; no law
changed. The design's verdict of section 5 stands with two readings
outside on the kicked world, reported.
