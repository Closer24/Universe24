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
