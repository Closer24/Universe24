# The quantum Zeno world: the blind and the reading

The paper's S.59 (the mathematician's 146 and 148; the advisor's 5949173532 column A; the owner's
words of 2026-10-02, 12:38, "Yes, both of them", and of 2026-10-03, 03:25, "Both Zeno and
anticoincidence must be obtained"): one record of two parts (g, e) of the near-flat pair [1, 1299]
declared an instrument at the centre Node of a periodic box of 8 x 8 x 4, its six Link factors 0 so
that it stays; one drive, the holder of the sign `pulse`, a plane wave at k = pi / 2 and the amplitude 308, read into the record's
phase at the weight 1 in both directions, so that the accumulated turn over the run of 48 intervals
is a pi pulse in the labels (48 x (2 / pi) x 308 / 6000 = 1.568 against pi / 2 = 1.571); one world
per probe count n in {1, 2, 4, 8, 16}, the record's own window 48 / n, so that it reads its own
parts n times over the run and the null window writes at each. The blind is `expectation.json`,
written by `build_world.py` from the design before any run and never edited after; the reading is
appended here after the night's run; every number a click (the part the record stands in at the
end, as its last write left it, over the trials; `tools/meeting_trials.py`); a reading that misses
the blind is a finding, written as such and never adjusted.

## The blind (expectation.json, Itano's column A)

P(e at T_pi) = (1 - cos^n(pi / n)) / 2 = 1.0000, 0.5000, 0.3750, 0.2346, 0.1334 at n = 1, 2, 4, 8,
16; column B (the click writing, the null window leaving the record) 1, 0.625, 0.154, 0.005, 0.000
and column C (no write) 1 at every n beside it, what the law would give without the clause.

## The reading (branch ion-world, the night of 2026-10-03, 120 trials per world, the seeds 1 to 120)

The tree at the reading: the one draw over the records reading one arriving record
(`meeting.took`) and the erasing front (`front.py`); the trials `tools/meeting_trials.py`, the
part each record stands in at the end and its `jump` lines labelled DETECTOR.

| n | window | trials ending in e | P(e at T_pi) | blind | column B | column C |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 48 | 120 of 120 | 1.000 | 1.000 | 1 | 1 |
| 2 | 24 | 61 of 120 | 0.508 | 0.500 | 0.625 | 1 |
| 4 | 12 | 46 of 120 | 0.383 | 0.375 | 0.154 | 1 |
| 8 | 6 | 26 of 120 | 0.217 | 0.235 | 0.005 | 1 |
| 16 | 3 | 15 of 120 | 0.125 | 0.133 | 0.000 | 1 |

The standard error of a fraction over 120 trials is about 0.045 at the middle and 0.03 at the ends.
Every n reads column A within one standard error: PASS at n = 1, 2, 4, 8 and 16 against the blind;
column C, 1 at every n, is excluded at every n above 1, and column B at n = 8 and 16, 0.005 and
0.000, is excluded. The jumps: at n = 2, 95 transfers g to e and 34 e to g over the 120 trials; at
n = 4, 64 and 18; at n = 16, 16 and 1. The front changes no number here: the pulse's count in the
books is 413 whole quanta and no taking brings it to 0, so no front begins (checked on eight seeds,
the front on and off, the jumps identical); an earlier table in this file, 0.408 and 0.292 at n = 2
and 4, was read on the build before the one draw over the outcomes entered (the per-record draw) and
is replaced by this one, the build that shipped at bd300d4c reading as above on the same seeds.
Named beside it, a GameBoard matter and no adjustment of the blind: the engine's turn per window is
the size of the drive's level at the Node summed over the window's intervals, whose mean over the
drive's period of 7.47 intervals is 2 / pi of the amplitude, and a window of 24 or 12 intervals
holds 3.2 or 1.6 periods, so the angle per window varies with the drive's phase at the window's
start; Itano's formula takes the angle per window as pi / (2 n) exactly; the pi pulse itself is
tuned to 1.568 against 1.571.

## The reading through the one click act with the face (the tree at 84f0352d and after, 120 trials per world)

| n | window | trials ending in e | P(e at T_pi) | blind | column B | column C |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 48 | 120 of 120 | 1.000 | 1.000 | 1 | 1 |
| 2 | 24 | 61 of 120 | 0.508 | 0.500 | 0.625 | 1 |
| 4 | 12 | 44 of 120 | 0.367 | 0.375 | 0.154 | 1 |
| 8 | 6 | 28 of 120 | 0.233 | 0.235 | 0.005 | 1 |
| 16 | 3 | 16 of 120 | 0.133 | 0.133 | 0.000 | 1 |

PASS at every n within one standard error of column A (0.045 at the middle, 0.03 at the ends); columns
B and C excluded as above. The jumps: n = 2, 95 g to e and 34 e to g; n = 4, 62 and 18; n = 8, 32 and
4; n = 16, 16 and 0. The generic act writes the taking as its list (the pulse's record at -1 by the
face, the atom's parts at +1 and -1 by the lay) and the null window as its list at the change 0.

## What is not built, by name

The record's own detector region around its Node (the mathematician's 180); the booking of the
share's difference at a giving (no giving in this world); the trials' seeds as a key of the world
file (one world file holds one seed; the trials set each record's generator from the design's
seeds, the host's declaration, `tools/meeting_trials.py`).

## On the own quantum, 2026-10-03 (branch own-quantum, 8382b8b9)

The round of the detector's own quantum (the mathematician's 213, 214, 220, 221 and 223 and the
advisor's seconds, the ids in `examples/events/resonance/blind_and_reading.md`) declares the atom's two
transitions at the resonance [2, 3] (the pulse's rotation at k = pi / 2) and lays no light here (the
atom has no rates); the worlds declare no region detector. Re-run by `tools/meeting_trials.py` on
8382b8b9 over the 120 seeds: P(e at T_pi) 1.000, 0.508, 0.367, 0.233, 0.133 at n = 1, 2, 4, 8, 16, the
jumps 120; 95 and 34; 62 and 18; 32 and 4; 16 and 0, bit for bit the readings through the one click
act above. PASS against column A at every n and unchanged.

## The readings' sources (the owner's word of 2026-10-03, 10:08 Israel)

P(e at T_pi) is the part the record stands in at the trial's end, read by `tools/meeting_trials.py`
from the instrument's own books on the board object (`meeting.NodeBooks.part`, the detector's own
content, not a written line; the same part is the last `jump` line's `realised`). The jumps per kind
are the `jump` lines labelled by the detector. The pulse's count of 413 in the books, the turn per
window named beside the blind and the pi pulse's tuning are GameBoard matters. The lines carry the
board's `tick` and the `window` in board intervals; the turn itself is taken per proper interval at the
record's Node (`meeting.turned_labels`) and no line carries that clock.

## On the resonant act, 2026-10-03 (branch resonant-act)

The resonant two-mode act (the mathematician's 223 (c) and 224 (2)(c), #1572 comments 5965727937 and 5966081562; the advisor's
seconds, 5965918924 and 5966129376 with #1563 comment 5966129628; the hands' precisions of the
morning, #1572 comments 5966338551 and 5966387795; the form in `examples/events/resonance/blind_and_reading.md`)
turns the labels once per window by k isqrt(X^2 + Y'^2) div R, A W / 2 at resonance, where the
magnitude form it replaces accumulated (2 / pi) A W per window; the design's drive amplitude is
rescaled once by 4 / pi, 308 to 392, a file number by name in `design.json` with the hands' ids, so
that the pi pulse stands where T9 has it (48 x 392 / (2 x 6000) = 1.568 against pi / 2), the five
worlds and their mode files rebuilt by `build_world.py --modes`, the blind's column untouched. Re-run
by `tools/meeting_trials.py` over the 120 seeds:

| n | window | trials ending in e | P(e at T_pi) | blind | the shipped act | the form's own number |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 48 | 113 of 120 | 0.942 | 1.000 | 120 of 120 | 0.943 (the angle 1.330 per window) |
| 2 | 24 | 67 of 120 | 0.558 | 0.500 | 61 of 120 | 0.497 (the angle 0.747 per window) |
| 4 | 12 | 44 of 120 | 0.367 | 0.375 | 44 of 120 | 0.369 (the angle 0.387 per window) |
| 8 | 6 | 32 of 120 | 0.267 | 0.235 | 28 of 120 | 0.233 (the angle 0.195 per window) |
| 16 | 3 | 15 of 120 | 0.125 | 0.133 | 16 of 120 | 0.133 (the angle 0.098 per window) |

PASS at n = 4 within one standard error of column A (0.045), the same count as the shipped act's 44
of 120, the jumps 61 g to e and 17 e to g against 62 and 18; PASS at n = 16 (0.125 against 0.133)
and at n = 8 (0.267 against 0.235, 0.032 off, within one standard error of 0.039); n = 2 reads 0.558
against 0.500, 0.058 off, within two standard errors (0.046) and not one; n = 1 reads 0.942 against
1.000, 113 of 120, 7 trials ending in g where the blind and the shipped act had none: a MISS and a
FINDING by name, named in this section before the four other probe counts were run and read as
predicted. Named, a GameBoard matter and
no adjustment of the blind: the window's turn is the plane's size over the window whatever the drive's
phase at the window's start (the hands' A W / 2 at every arrival phase), so the angle per window no
longer varies with that phase as the magnitude form's did; and the one turn per window passes through
the engine's turn, 2 arctan of the numerator over 2 Gamma, so a window carrying a quarter turn in one
application (n = 1, the numerator 9,408 against 12,000) turns by 1.33 and not 1.57, a compression of
the tangent half-angle at large turns, 1.4 percent at n = 4 and 15 percent at n = 1; the form's own
number per world under that angle and the null window's write stands in the last column (0.943 at
n = 1 against the read 0.942), so the n = 1 miss is the engine's turn form and not the draw. The
jumps: n = 1, 113 g to e; n = 2, 91 and 24; n = 8, 38 and 6; n = 16, 15 and 0.
## On the sub-turn form, 2026-10-03: the blind, written before the run

The advisor's second on the first build (d12a4f51, read from the diff): the window's turn is an angle
and the engine's turn (`features/rotation`, `turned`) takes a tangent half-angle, tan(theta / 2) = the
numerator over 2 Gamma, so one shear of the whole window's sum compresses a large turn, 2 arctan(9,408
/ 12,000) = 1.332 at n = 1 against 1.568, sin^2(1.332) = 0.9435, the 113 of 120 above exactly; at n = 2
the per-window angle 2 arctan(0.392) = 0.744 against pi / 4 = 0.785. The misses at n = 1 and 2 and the
passes at n = 4, 8 and 16 are one cause, the tangent, not statistics. The fix, one line of the act
(`meeting.sheared`): the window's turn applied at the close as W equal sub-turns, each sub-turn's
numerator (turn + carry) div W with the remainder carried across the W shears (the carried division,
the write's own act), so the sub-turns sum to the turn exactly and the angles add as the proper
intervals' did: 48 x 2 arctan(9,408 / (12,000 x 48)) = 1.5680 at n = 1 (pi / 2 = 1.5708, the 0.003 the
design's rounding of 392), the per-window angle pi / (2 n) at every n within 0.001; the labels
untouched inside the window, the resonance read by the plane's size, the root once per window; no
amplitude recalibration (2 arctan is not linear in W, no one amplitude fits every n). The blind for the
re-read, the advisor's, written here before the run: n = 1 at 1.000 (120 of 120); n = 2 at 0.500
within one standard error (0.046); n = 4, 8 and 16 as read above (44, 32 and 15 of 120) within one
standard error; the resonance world's detuned and four-phase readings unchanged (they read the turn's
numerator, not the angle). A reading that misses this blind is a finding by name, not adjusted.

### The reading under the sub-turn form (branch resonant-act, 2026-10-03, about 07:35 UTC, 120 trials per world)

| n | window | trials ending in e | P(e at T_pi) | the blind above | the first build |
| --- | --- | --- | --- | --- | --- |
| 1 | 48 | 120 of 120 | 1.000 | 1.000 (120 of 120) | 113 of 120 |
| 2 | 24 | 68 of 120 | 0.567 | 0.500 within 0.046 | 67 of 120 |
| 4 | 12 | 45 of 120 | 0.375 | 0.375, as read (44) | 44 of 120 |
| 8 | 6 | 33 of 120 | 0.275 | 0.235, as read (32) | 32 of 120 |
| 16 | 3 | 15 of 120 | 0.125 | 0.133, as read (15) | 15 of 120 |

PASS at n = 1 (120 of 120, the blind's), at n = 4 (0.375, the column exactly), at n = 8 and at n = 16
(as read, within one count). n = 2 reads 0.567 against 0.500, 0.067 off, 1.46 standard errors, beyond
the blind's one standard error: a MISS by name, not adjusted; the same 120 seeds read 0.558 on the
first build at the per-window angle 0.747 and 0.567 here at 0.784 (pi / 4 = 0.785, the form's own
number 0.500), so the excess is the seeds' draw and not the angle, named and left standing. The
jumps: n = 1, 120 g to e; n = 2, 95 and 27; n = 4, 63 and 18; n = 8, 39 and 6; n = 16, 15 and 0.
The one shear's angle at n = 1 is 2 arctan(9,408 / 12,000) = 1.3298 exactly, the blind's 1.332 its
rounding; the sub-turn form's 48 x 2 arctan(196 / 12,000) = 1.5679. The resonance world's detuned and
four-phase readings: the four-phase turns are the dedicated test's and unchanged (they read the turn's
numerator); the detuned taker is read on the tree that also holds main's dark grain, which moved the
givings, so its number stands in `examples/events/resonance/blind_and_reading.md` against the blinds
there and not against this line. The function named `meeting.sheared` in the blind lives in
`src/event_universe/resonance.py` as `sheared`, called by `meeting.turned_labels`.

### The n = 2 row at 480 seeds, a finding by name (the advisor's re-read, #1572 comment 5966923475)

The advisor read the shipped Zeno worlds at 954c4a75 over the fresh seeds 121 to 600 with
`tools/meeting_trials.py` (a scratch worktree, nothing written to the repository):

| world | ends in e | fraction | Itano | standard error | the jumps g to e / e to g |
| --- | --- | --- | --- | --- | --- |
| n = 2 | 295 of 480 | 0.615 | 0.500 | 0.023 | 380 / 85 |
| n = 2, the first window alone (24 intervals) | 221 of 480 | 0.460 | 0.500 | 0.023 | 221 / 0 |
| n = 4 | 193 of 480 | 0.402 | 0.375 | 0.022 | 251 / 58 |
| n = 8 | 99 of 480 | 0.206 | 0.235 | 0.019 | 109 / 10 |

n = 4 and n = 8 within 1.5 standard errors; n = 2 five standard errors high, the branch's 68 of 120
and the first build's 67 of 120 on the seeds 1 to 120 the same bias at a quarter of the statistics
and not the draw. The two windows separated: the first window alone flips 221 of 480 (0.460, within
2 standard errors); in the second window 159 of the 259 left in g flipped to e (0.61) and only 85 of
the 221 in e flipped back to g, 0.385 against 0.5, 3.5 standard errors low. The asymmetry is the
finding by name: after a taking, the return e to g is suppressed. The cause by one hand, the
advisor's reading: the taking's write is the hole, the arriving record's levels at the Node to 0 by
the face with its count down by one, and the Zeno drive at A = 392 holds at the instrument's Node
the share 3 den A^2 sin^2 omega = 1.54 x 10^9 against one quantum's W_c sin omega = 4.40 x 10^8 at
T = 32,768, 3.5 quanta's share per Node, so the hole of one taking removes three and a half quanta's
worth of the drive at the Node, which Rule3 refills from the neighbours over the following intervals,
and the second window's sum at that Node is short; not the resonant act's (the magnitude form had the
same hole, 120 trials hid it) and not statistics; the one-quantum records of the gates are untouched
by it, a dense drive is the case. The hole of a dense record (the Node's share down by one quantum,
W_rec, and not to 0, the record re-laid at its share less W_rec with the count down by one) is a line
asked of the mathematician, a round of its own and not tonight's. The advisor's word for the gate:
the trials 480 per world from now, 120 reads and does not prove; a design change for the next round,
the five worlds' trials untouched tonight.

The diagnostic the advisor asked, run before any change, labelled GAMEBOARD (a reading of the board
and no measurement): `zeno_2.json` at the seed 2 (the record's generator at the state 2, as the trials
set it), whose record takes at the first window's close, the interval 24, g to e, and ends in e; beside
it the same seed with the taking suppressed (`meeting.took` returning no taking, so the record writes
its null window at 24 and ends in g, the drive untouched). The drive's level at the instrument's Node
[4, 4, 2] (`meeting.arriving`, the pulse's time line) at the intervals 22 to 48, with the taking and
with it suppressed: 22: 361, 361; 23: 337, 337; 24: 82, 82; 25: 0, -234; 26: 0, -400; 27: -384, -305;
28: -147, -14; 29: 312, 279; 30: 433, 379; 31: 230, 219; 32: -74, -95; 33: -340, -353; 34: -368,
-384; 35: -170, -168; 36: 144, 152; 37: 381, 362; 38: 352, 322; 39: 104, 58; 40: -182, -255; 41:
-348, -407; 42: -203, -298; 43: -10, 0; 44: 269, 287; 45: 479, 372; 46: 376, 198; 47: -118, -118;
48: -368, -367. The face holds the level at 0 over the intervals 25 and 26, Rule3 refills the Node from
its neighbours from 27 on, and the wave at the Node differs from the untouched run by up to 180 levels
through the window; over the second window, the intervals 25 to 48, the plane's size SUM a_t
e^(i Omega t) reads 4,428 with the taking against 4,765 without (A W / 2 = 4,704), 7 percent short,
and SUM |a_t| 5,792 against 6,026. No number of the blind is adjusted.

## On the partial hole, 2026-10-03

The hole of a dense record (the mathematician's 237, #1572 comment 5967012316, with the advisor's
second, 5967123679, two hands; branch partial-hole): where the arriving record's share at the Node
exceeds its own quantum W_rec, the taking's face writes the record's two time levels scaled by
isqrt((s - W_rec) x 2^(2m)) div (isqrt(s) x 2^m) instead of 0, the phase and the sense at the Node
standing and one quantum's share leaving; where the share is at most W_rec the hole to 0 as before.
The trials from now 480 per world, the design's seeds 1 to 480 (the advisor's word), `tools/meeting_trials.py`.

The blind, written by the two hands before the build (237): n = 2 at 480 seeds 0.500 within 0.023;
n = 1, 4, 8 and 16 unchanged within 1.5 standard errors from the shipped act's 480 of 480, 0.402 and
0.206 at 480 seeds; the column within one standard error of 480 seeds.

| world | ends in e | fraction | Itano | standard error | against the column | the shipped act at 480 seeds | the jumps g to e / e to g |
| --- | --- | --- | --- | --- | --- | --- | --- |
| n = 1 | 480 of 480 | 1.000 | 1.000 | 0.000 | the column exactly | 480 of 480 | 480 / 0 |
| n = 2 | 251 of 480 | 0.523 | 0.500 | 0.023 | 1.00 standard errors, within the blind's 0.023 | 0.615 | 381 / 130 |
| n = 4 | 196 of 480 | 0.408 | 0.375 | 0.022 | 1.50 standard errors, beyond one | 0.402 (unchanged, 0.3) | 256 / 60 |
| n = 8 | 109 of 480 | 0.227 | 0.235 | 0.019 | 0.41 standard errors | 0.206 (unchanged, 1.1) | 121 / 12 |
| n = 16 | 57 of 480 | 0.119 | 0.133 | 0.016 | 0.90 standard errors | 15 of 120 at 120 seeds | 60 / 3 |

The reading: n = 2 moves from 0.615 to 0.523, the finding this line answered, within the blind's
0.023 at exactly one standard error; n = 1, 8 and 16 within one standard error of the column; n = 4
reads 0.408, unchanged from the shipped act's 0.402 as the blind asked and 1.5 standard errors above
Itano's 0.375, beyond the column's one standard error, a finding by name and not adjusted (the same
row read 0.402 under the hole to 0, so the excess is not the partial hole's). The second window's
return e to g at n = 2: 130 of the 381 that flipped g to e flipped back (0.34 against the hole to 0's
85 of 380, 0.22), the suppression of the return lifted in part and not whole, by name. The gates bit
for bit (the two slits' and Bell's four and the GHZ's four output files byte-identical to main's at
7033a6aa, their records below one quantum per Node at every click, so the hole to 0 stands there).
A GameBoard diagnostic beside the run, labelled so (the seed 2 of n = 2, the drive's first line at
the instrument's Node): at the click the twin's share at the Node reads 2.564 quanta; after the
face's two intervals the levels are the twin's scaled by 0.781 (-183 and -313 against -234 and -400),
their ratio the twin's within 0.001, and the share at the Node reads 0.975 of a quantum against the
twin's 2.674, more than one quantum gone at the Node itself, since the booked form's cross term with
the six neighbours' levels scales by the factor alone and not by its square, Rule3 refilling the Node
from 2.784 at the second interval after; a finding by name for the hands, no number adjusted.

### The reading on main after round A's merge (the Boss, 2026-10-03, 11:30 to 11:36 UTC)

The experiment on main at 7732b5ff (the engine of the squash 08c092a9, pull request #1724, the partial
hole and the empty-origin unit), the five shipped worlds over the design's seeds 1 to 480 by
`tools/meeting_trials.py`, each world as four processes of 120 seeds (the owner's rule of the day: a
run under a minute; 25 to 27 s per world on four cores), the counts summed over the four; the blind
rows above copied before the run (n = 2 at 0.500 within 0.023; n = 1, 4, 8 and 16 unchanged within
1.5 standard errors from the shipped act's 480 of 480, 0.402 and 0.206; the column within one
standard error).

| world | ends in e | fraction | Itano | standard error | against the column | the jumps g to e / e to g |
| --- | --- | --- | --- | --- | --- | --- |
| n = 1 | 480 of 480 | 1.000 | 1.000 | 0.000 | the column exactly | 480 / 0 |
| n = 2 | 251 of 480 | 0.523 | 0.500 | 0.023 | 1.00 standard errors, within the blind's 0.023: PASS | 381 / 130 |
| n = 4 | 196 of 480 | 0.408 | 0.375 | 0.022 | 1.51 standard errors; unchanged from the shipped act's 0.402 within 1.5 as the blind asked; against the column a finding by name (the branch's reading the same) | 256 / 60 |
| n = 8 | 109 of 480 | 0.227 | 0.235 | 0.019 | 0.41 standard errors | 121 / 12 |
| n = 16 | 57 of 480 | 0.119 | 0.133 | 0.015 | 0.92 standard errors | 60 / 3 |

The reading on main is the branch's reading bit for bit (the same seeds, the same engine after the
squash): n = 2 PASS at one standard error; n = 4 the finding by name that stands (the hands' 244 and
the quadratic factor's branch, pull request #1730, where it reads 0.415 at 480 seeds; the advisor's
line: 960 seeds before any cause is named); n = 1, 8 and 16 within one standard error of the column.
Nothing adjusted.
