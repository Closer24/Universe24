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
