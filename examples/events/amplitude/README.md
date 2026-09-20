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
K 2^20, N 64, `release` [0, 1], `suspension` 0, `amplitude` true, 80
intervals. The source at (0, 0), a lamp of `light` of content 2^20 whose
turn is one phase step per self-creation for far more births than the run
holds, so the record born at tick t has the birth phase u = t - 1: the 64
births of the ticks 1 .. 64 span the circle once and complete by tick 76
(the ports click eleven or twelve intervals after a birth on the flight
table); the 11 born after are open at the end. Each birth is one record of two rows of
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
(`expectations.json` under `mach_zehnder`). The runs and their readings
are in the register's L1 entry.

## L2: the two slits at a low rate

**The world** `slits_low` (the design's test 2): the shipped
`examples/events/two_slits.json` under the key, the lamp's rate [1, 1] and
content K (one phase step per interval: the birth at tick t has u = t - 1,
64 births span the circle), the family's `phase_per_link` the pair
[8591334592, 2^30] (the shipped lamp's turn per interval), the 121 pixels
reading `sum`, the wall freed within 6 of each opening (a steep direction
walks along y inside the wall's plane before its first step in x, so the
shipped wall absorbs 88 of the 182 fan rows beside the openings; freed,
every fan row leaves the plane) and the lamp's three rows that miss the
openings absorbed by wall Nodes at (7, 58), (7, 60), (7, 62) on their
paths (a lamp row and a fan row at one set would carry the multiplicities
5 and 455, refused). 230 intervals. **The reference** `slits_one`: one
birth through the same geometry without the key, the lamp's five rows
declared as rays of amount 91 (one row per direction at each opening's
re-emission, m = 5 x 91 = 455), the screen reading the age; the generator
runs it in-process and reads it by the design's `slits_read.py` into
`expectations.json` under `two_slits` before the run of `slits_low`: the
weights per set, the ladder's clicks over the 64 births, the shares, the
pixels and the correlations (the register's L2 entry has the numbers and
the run).

## L3: the pair, the which-path world and no maintenance

The registered A2 world `examples/events/bell/read.json` (a bar of 21, the
lamp at x = 10, Alice's counters at 7 and 4 reading the chooser `sa`,
Bob's at 17 and 18 reading `sb`) under the key: the lamp's `arms` 2 and
`branches` [[0, 1], [3, 1]] (the pair, the joint labels 00 and 11; the
directions ordered so that Alice's arm is arm 0) and the four counters
reading `sum`, whose windows are the rotation's settings. `bell_choosers`
(1000 intervals: the 960 births from tick 8 see the choosers' 15 setting
pairs with every u); `bell_0_8`, `bell_0_24`, `bell_16_8`, `bell_16_24`
(the chooser sources removed, the windows the integers, 80 intervals);
`path_<a>_<b>` (a `read` entry of the counter family at x = 9 on Alice's
arm, the detector `path` reading `sum`: the which-path world);
`bell_16_24_far` and `path_16_24_far` (Bob's counters 116 Links farther,
300 intervals: no maintenance). The expectations (`expectations.json`
under `pair`) are the design's `bell.py` in the generator: the rotation
on the half-angle tables of 2N, the joint amplitude the sum over the
labels of the products of the arms' entries, the cells (oA, oB) over the
64 births; the register's L3 entry has the numbers and the runs.

## L4: GHZ

A plane of 7 x 7, the lamp at (3, 3) on three arms (+x, -x, +y;
`branches` [[0, 1], [7, 1]]), a counter on each arm at (6, 3), (0, 3),
(3, 6) with the setting 16 and the turn 0 (X) or 16 (Y): `ghz_xxx`,
`ghz_xyy`, `ghz_yxy`, `ghz_yyx`, `ghz_yyy`, 80 intervals; the
expectations under `ghz`.
