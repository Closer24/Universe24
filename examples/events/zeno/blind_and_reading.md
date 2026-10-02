# The quantum Zeno world: the blind and the reading

The paper's S.59 (the mathematician's 146 and 148; the advisor's 5949173532 column A; the owner's
words of 2026-10-02, 12:38, "Yes, both of them", and of 2026-10-03, 03:25, "Both Zeno and
anticoincidence must be obtained"): one record of two parts (g, e) of the near-flat pair [1, 1299]
declared an instrument at the centre Node of a periodic box of 8 x 8 x 4, its six Link factors 0 so
that it stays; one drive, a plane wave at k = pi / 2 and the amplitude 308, read into the record's
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

| n | window | trials ending in e | P(e at T_pi) | blind | column B | column C |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 48 | 120 of 120 | 1.000 | 1.000 | 1 | 1 |
| 2 | 24 | 49 of 120 | 0.408 | 0.500 | 0.625 | 1 |
| 4 | 12 | 35 of 120 | 0.292 | 0.375 | 0.154 | 1 |
| 8 | 6 | 26 of 120 | 0.217 | 0.235 | 0.005 | 1 |
| 16 | 3 | 15 of 120 | 0.125 | 0.133 | 0.000 | 1 |

The standard error of a fraction over 120 trials is about 0.045 at the middle and 0.03 at the ends.
The suppression by the record's own window is read: the fraction in e falls from 1 at n = 1 to
0.125 at n = 16, Itano's curve in form, column A against columns B and C by name (column C, 1 at
every n, is excluded at every n above 1; column B at n = 8 and 16, 0.005 and 0.000, is excluded).
Against column A's numbers: n = 1, 8 and 16 PASS within one standard error; n = 2 and n = 4 read
0.09 and 0.08 below the blind, about two standard errors each, a deficit of the same sign at both.
Named beside it, a GameBoard matter and no adjustment of the blind: the engine's turn per window is
the size of the drive's level at the Node summed over the window's intervals, whose mean over the
drive's period of 7.47 intervals is 2 / pi of the amplitude, and a window of 24 or 12 intervals
holds 3.2 or 1.6 periods, so the angle per window varies with the drive's phase at the window's
start and the transfer per window, sin^2 of that angle, varies with it; Itano's formula takes the
angle per window as pi / (2 n) exactly; the pi pulse itself is tuned to 1.568 against 1.571. The
jumps: at n = 2, 84 transfers g to e and 35 e to g over the 120 trials; at n = 16, 16 and 1.

## What is not built, by name

The record's own detector region around its Node (the mathematician's 180); the booking of the
share's difference at a giving (no giving in this world); the trials' seeds as a key of the world
file (one world file holds one seed; the trials set each record's generator from the design's
seeds, the host's declaration, `tools/meeting_trials.py`).
