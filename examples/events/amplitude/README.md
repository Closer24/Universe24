# Series L: the amplitude law

The worlds of series L, written by `make_worlds.py`; the register entry is
[L, the amplitude law (2026-09-20)](../../../docs/EXPERIMENTS.md#l-the-amplitude-law-2026-09-20).
The decision, in the model owner's words (Highlights 5.4, 2026-09-20):
"go for it with the four recommendations and the unifications"; the design
is the physicist's and the mathematician's `scratchpad/amplitude/DESIGN.md`,
every integer below from its check scripts (`mz.py`, `mz.txt`), written
before any run. Under the world key `amplitude` the lattice is unchanged
(the flight, the collision, the meeting, the books over every row), the
rows carry a record, a branch and a multiplicity, a re-emission may split a
row by integer weights, antiphase rows of one record cancel at the merge,
and the apparatus's layer reads every record's offers at its completion and
chooses one by the record's birth phase u on a ladder of rungs at the
nearest integer ([BEAM_LAW note 37](../../../docs/BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)).
A research run, made once, never a test; a reading outside its expectation
is reported with its numbers, never moved. Every number is one of two kinds
([the register](../../../docs/EXPERIMENTS.md), "Two kinds of readings"): a
DETECTOR reading (a gather, a click) or a GAMEBOARD reading (a row, a
cancel).

## L1: the Mach-Zehnder interferometer and Elitzur-Vaidman

**The world** (the design's section 3.4): a plane of 5 x 5 with z periodic,
K 2^20, N 64, `release` [0, 1], `suspension` 0, `amplitude` true, 75
intervals. The source at (0, 0), a lamp of `light` of content 2^20 whose
turn is one phase step per self-creation for far more births than the run
holds, so the record born at tick t has the birth phase u = t - 1: the 64
births of the ticks 1 .. 64 span the circle once and complete by tick 75
(the ports click eleven intervals after a birth on the flight table); the
11 born after are open at the end. Each birth is one record of two rows of
amount 1 with the multiplicity 2: +x (arm 1) and +y (arm 2, the
reflection's quarter turn 16 on the row: the source's own splitter).
Mirror 1 at (3, 0) re-emits +x arrivals on +y and mirror 2 at (0, 3)
re-emits +y arrivals on +x (`rerelease` on one direction: the equal split
with one weight). The splitter at (3, 3) is a `rerelease` whose split table
is selected by the arrival (`inputs`): a row arriving along +y (arm 1) is
transmitted on +y toward D2 with the weight a and reflected on +x toward D1
with the weight b and the quarter turn 16; a row arriving along +x (arm 2)
is transmitted on +x toward D1 with a and reflected on +y toward D2 with b
and 16; A = a^2 + b^2. D1 at (4, 3) and D2 at (3, 4) are one-Node detectors
reading `sum`.

| world | the splitter | arm 2 | `phase_per_link` | the design's integers over the 64 births |
| --- | --- | --- | --- | --- |
| `mz_equal` | (20, 21) | equal | 0 | D1 64, D2 0 (the offers 1681/1682, 1/1682) |
| `mz_half` | (20, 21) | a half turn 32 on the row | 0 | D1 0, D2 64 |
| `mz_quarter` | (20, 21) | a quarter turn 16 on the row | 0 | D1 32, D2 32 |
| `mz_balanced` | (1, 1) | equal | 0 | D1 64, D2 0 (D2's rows cancel on the lattice) |
| `mz_345` | (3, 4) | equal | 0 | D1 63, D2 1 (the rung moved: u = 63 falls in D2) |
| `mz_unequal_f0` | (20, 21) | longer by two intervals | 0 | D1 64, D2 0 (the rows accumulate in phase) |
| `mz_unequal_f8` | (20, 21) | longer by two intervals | [8, 1] | D1 32, D2 32 (two intervals at 8 steps per interval: a quarter turn) |
| `mz_unequal_f16` | (20, 21) | longer by two intervals | [16, 1] | D1 0, D2 64 |
| `ev_29` | (20, 21), arm 2 absorbed at (0, 3) | equal | 0 | absorber 32, D1 17, D2 15 |
| `ev_169` | (119, 120), arm 2 absorbed | equal | 0 | absorber 32, D1 16, D2 16 |

"Arm 2 longer by two intervals" is made on the flight table: arm 1 carries
two pass-through re-emitters at (3, 1) and (3, 2); a re-born row starts a
fresh digital line whose first step is at its first interval, so each
advances arm 1 by one interval, and arm 2 reaches the ports two intervals
after arm 1. The phase per interval of age (the pair form of
`phase_per_link`, carried through every re-emission) reads the delay as the
design's f x 2. The absorber of Elitzur-Vaidman is a measured event of
`light` at (0, 3) in place of mirror 2, declared as the detector `absorber`
reading `sum`.

**What the lattice does** (GAMEBOARD, `tests/test_amplitude_split.py`): on
`mz_equal` the two rows toward D1 merge in phase (amount 41, multiplicity
1682) and the two toward D2 cancel to 1 in antiphase; on `mz_balanced`
the rows toward D2 cancel entirely. **What the world reads** (DETECTOR):
the clicks per port over the 64 births in the table above, the ladder at
each record's completion normalised by the sum of its offers with the
rungs at the nearest integer, `b_k = (2 N C_k + Total) // (2 Total)`
(`expectations.json` under `mach_zehnder`).
