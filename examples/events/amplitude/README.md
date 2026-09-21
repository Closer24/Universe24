# Series L: the amplitude law

The worlds of series L, written by `make_worlds.py`; the register entry is
[L, the amplitude law (2026-09-20)](../../../docs/EXPERIMENTS.md#l-the-amplitude-law-2026-09-20).
The decision, in the model owner's words (Highlights 5.4, 2026-09-20):
"go for it with the four recommendations and the unifications"; the design
is the physicist's and the mathematician's `docs/designs/amplitude-v1/DESIGN.md`,
every integer below from its check scripts (`mz.py`, `mz.txt`), written
before any run. In a recorded world (a lamp declared; the key `amplitude` of
the law's first stages is deleted since the one click) the GameBoard is unchanged
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
intervals. The source at (0, 0), a lamp of `light` of content 2^20 at K
2^20 whose turn is one phase step per self-creation, paying 2 per birth:
since the fraction-free law (2026-09-20, BEAM_LAW note 41) its exact
clock stalls once, at tick 2 (the content 2^20 - 2 short of one turn),
so the record of ordinal n >= 2 is born at tick n + 1 with the birth
phase u = n - 1 (until then the record born at tick t had u = t - 1):
the lamp's first 64 records, read by ordinal, span the circle once and
complete by tick 76 (the ports click eleven or twelve intervals after a
birth on the flight table); the 11 born after are open at the end. The
pair lamps of L3 (content 15 x 2^20) stall once at tick 3. Each birth is one record of two rows of
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
| `mz_balanced` | (1, 1) | equal | 0 | D1 64, D2 0 (D2's rows cancel on the GameBoard) |
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

**What the GameBoard does** (GAMEBOARD, `tests/test_amplitude_split.py`): on
`mz_equal` the two rows toward D1 merge in phase (amount 41, multiplicity
1682) and the two toward D2 cancel to 1 in antiphase; on `mz_balanced`
the rows toward D2 cancel entirely. **What the world reads** (DETECTOR):
the clicks per port over the 64 births in the table above, the ladder at
each record's completion normalised by the sum of its offers with the
rungs at the nearest integer, `b_k = (2 N C_k + Total) // (2 Total)`
(`expectations.json` under `mach_zehnder`). Since 2026-09-21 (the
trimming's part 2: a test holds no literal of a world's number) the same
file registers what the tests read of the GameBoard and of the layer: the
birth's and the split's rows with the cancels, the first gather, the last
tick of the gathers and the totals' spread under `mach_zehnder`; the first
gather and the last tick under `two_slits`; the pair's birth, the
choosers' early records and the far worlds' least flight under `pair`;
the rotate and gate lines, the rows after the gates and the rotation's
multiplicity under `gate`. The runs and their readings
are in the register's L1 entry. **Under the exact phase at the click
(2026-09-21, [BEAM_LAW note 45](../../../docs/BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)):**
every port's clicks in the table stand (the unequal arms 64 / 0, 32 / 32
and 0 / 64 included); the unequal arms' records read their two paths at
the exact time of their last Links, so their weights and totals moved
(eight totals per world as before); the equal arms are bit-identical.

## L2: the two slits at a low rate

**The world** `slits_low` (the design's test 2): the shipped
`examples/events/two_slits.json` under the record form, the lamp's rate [1, 1] and
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
weights per set (coherent within a Node, incoherent across the Nodes of a
set: a face is one cell of the sum of its Nodes' squares), the ladder's
clicks over the 64 births, the shares, the pixels and the correlations
(the register's L2 entry has the numbers and the run). **Under the exact
phase at the click (2026-09-21,
[BEAM_LAW note 45](../../../docs/BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)):**
the reference declares the frequency and the reading takes each row's
phase from the `exact` of its click line; the reading and the run agree on
every one of the 80 sets: wall 34 (11, 12, 11), screen 15 on fourteen
pixels (y = 11, 29, 36, 40, 50, 56, 59, 60 twice, 61, 70, 77, 84, 90, 107),
faces 15 (8, 7); the total 4834019/4259840, the shares 0.529 / 0.244 /
0.227, the weights' Pearson with the two-source cosine 0.382 (0.368 under
the phase of the whole intervals), the histogram's with the weights 0.722
(0.655); the design's map (wall 34, screen 16, faces 14) carried the lamp
leg's exact fraction across the re-emission and evaluated on a table of
4096 floats, which the engine does not.

**The fan by angle** `slits_huygens` (L2b; the mathematician's
[TWO_SLITS.md section 7](../../../docs/designs/fraction_free/TWO_SLITS.md),
run on the Boss's order of 2026-09-20 under the owner's standing
authorization, as the evidence for the decision on P as a width of the
law): `slits_low`'s geometry, lamp and frequency, each opening's
re-emission the Farey fan of width 48 (every primitive direction (a, b, 0)
with a >= 1 and a + |b| <= 48, 1423 in angle order, consecutive
directions Farey neighbours) restricted to |b| <= 13 a by the freed band
(1327 directions; the 96 steeper ones would walk into the wall or through
the other opening, 3.5 percent of the angle), each direction's split
weight the angle it covers (half the gap to each neighbour, the gap
3 Q^2 / (T_D T_D') at the grain 2^18: the weights 123 to 5619, A = sum
of squares 714 364 777, the multiplicity 5 A within 2^32; the load-time
ceiling multiplies both openings' A, so A stays within 2^31), 420
intervals (at least 256 births completed). **Pinned before the run, from
`docs/designs/fraction_free/two_slits_map.py`'s walk with these integer
weights (the built phase, the click as built):** the first record's total
2.677 of the birth norm (the rows of one opening meet at a pixel nearly
in phase), the shares wall 0.224, screen 0.410, faces 0.366; the screen
WEIGHTS with Young's fringes, Pearson 0.895 with the Euclidean two-source
cosine (the pace 64/110, the wavelength 4.654 Links), visibility 0.954
between the cosine's bright pixels (y = 35 to 38, 59 to 61, 82 to 85) and
its dark ones (13 to 20, 48 to 50, 70 to 72, 100 to 107), the peak at y =
59 to 61 at 0.012 of the total against the rung 1 / 2N = 0.0078; the
CLICKS over the 64 births of u = 0 .. 63: wall 14 (4, 5, 5), screen 27 on
27 pixels one each (y = 2, 25, 31, 33, 35, 37, 39, 41, 43, 47, 56, 57, 59,
60, 61, 63, 64, 74, 77, 79, 81, 83, 85, 87, 89, 97, 119: the cumulative
rungs fall where the weights are, 7 of the 11 bright pixels hit and none
of the 22 dark, the histogram's Pearson 0.499 with the cosine), faces 23
(11, 12); 32 distinct cells over the 64 births and the same cells for
every later birth (u repeats with the period 64). Refutation: a Pearson of
the weights below 0.85 or a visibility below 0.9, a click at a dark
pixel, or a click cell outside the 64-birth list after tick 64.

**Run (2026-09-20, `slits_huygens`, 420 intervals, 76.3 s, main f89884f9,
completed and conserved; 271 records gathered, 149 open at the end;
DETECTOR).** Every pinned number reproduced: the first record's total
2.6771, the shares 0.224 / 0.410 / 0.366, the weights' Pearson 0.895 and
visibility 0.954 with the peak at y = 59 (0.01204 of the total); the
first 64 births' clicks wall 14, screen 27 on the pinned 27 pixels, faces
23; no click at a dark pixel in 271; 32 distinct cells in the first 64
births and 32 in all 271 (every u clicked its one cell at every birth);
the histogram's Pearson 0.493 at 271. The fringes are in the record's
weights and not in the clicks: TWO_SLITS.md section 7, the page
<https://claude.ai/artifact/6pyy8C62muHshZ7iMDCUx9>.

**Re-registered under the birth wheel (2026-09-21; the model owner's
decision, record 180; [BEAM_LAW note 46](../../../docs/BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation);
the run that shows the wheel).** The world declares the golden rate
`wheel` [2531, 4096] (u = ordinal x 2531 mod 4096, the rungs on 4096;
every other registered lamp [1, N]) and runs 4300 intervals for 4096
births, under the exact phase at the click (note 45). **Pinned before the
run:** as ordered, the map's section 8 at 4096 births (the screen's fan of
121 directions with the wheel and the exact phase): the bright pixels
about 28 to 29 clicks, the dark 0 to 3, the Pearson of the counts with the
two-source cosine about 0.96; and, for this world's own fan, the wheel's
own statement, every cell's count within one click of 4096 x its weight
over the total, the rungs being the first record's (the tables' eight
totals at u mod 64, a part in 276, note 37 (xii), move a rung by at most
one more). **Run (2026-09-21, `slits_huygens`, the run, 4300 intervals in 1334 s (0.31 s per interval), completed and
conserved at every tick, 4299 records born, 4150 gathered and 149 open at the
end, every one of the records 1 to 4096 gathered; the
branch `click`; DETECTOR):** over the records 1 to 4096 the clicks are
wall 882, screen 1711 on 107 pixels, faces 1503, on 112 of the 116 cells
with weight; at the cosine's dark pixels 0 to 3 (3, 1, 0, 0, 0, 0, 0, 0,
3, 0, 1, 1, 0, 3, 0, 0, 0, 0, 0, 1, 0, 2; the mean 0.68), as pinned; at
its bright pixels 41, 19, 42, 38, 51, 49, 51, 39, 42, 20, 40 (the mean
39.3), not the map's 28 to 29: the map's number is the screen's fan's,
whose screen share is 0.35 with a flatter peak, where this world's Farey
fan puts 0.418 of the total on the screen with its peak at y = 59 to 61
at 0.012 (51 clicks each), and the two bright pixels at 19 and 20 (y = 36
and 84) are the weights' own widths 20 and 21 (the digital line's landing);
the counts' Pearson with the cosine 0.891 against the weights' registered
0.895, the visibility 0.966 (the weights' 0.954); against the first
record's own rungs (its cells' widths in 1/4096 of the total, the expected
counts) the histogram's Pearson is 1.000 over the 126 cells and 0.998 over
the screen, every cell's count within 2 of its width (within 2 and not one: the rungs are per record, the tables' eight totals at u mod 64, a part in 276, note 37 (xii), so the counts are compared with the first record's rungs): the wheel turns the
weights into counts, and the counts y = 40 .. 80 are 29 41 28 27 19 15 8 6
3 0 1 5 7 15 18 20 36 45 51 51 49 51 51 45 36 20 18 15 7 5 1 0 3 6 9 14 19
26 29 42 28. The first 64 births: wall 14, screen 27 on 27 pixels, faces
23, 32 distinct cells (as under [1, 64]); by 256 births 69 distinct cells,
by 1024 101. Verdict: Young's fringes are in the clicks as they were in
the weights (the Pearson 0.891 against 0.895, the fan's own discreteness,
TWO_SLITS.md section 7); the map's 0.96 was the screen's fan's and is not
this world's pin. The run's record: `run.json` source sha256
aa52ecb3168d4353..., initialization sha256 b75b611959ec3dfe...

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

## L5: the gate between records

`cnot_pair_<a>_<b>` (a plane of 16 x 11: the control's lamp at (2, 5)
through the Hadamard at (4, 5), a `rerelease` whose `rotate` turns the
label bit 0 by N/4, into the gate at (8, 5), a `rerelease` with `gate`
{cnot, hold, 2 parties, control [1, 0, 0]: the direction the control's
rows arrive on} sending the control on +y to Alice at (8, 8) and
the target, born at (14, 5), on -y to Bob at (8, 2), his window -b);
`cnot_twice` (the gate's outputs into one gate per arm, the identity);
`cnot_ghz_<basis>` (three lamps into one gate of three parties on a board
of 11 x 11 x 3); `rotations_3` and `rotations_4` (three, then four, label
rotations in series: the register's ceiling, the fourth refused at load;
`rotations_4` is built by the generator for the test and not shipped as
a file, a refused world being no run).
The expectations under `gate` are the design's `gate.py`; the register's
L5 entry has the numbers and the runs.

## L6: the pair at N = 1024 and 4096

`bell_n1024_<a>_<b>` and `bell_n4096_<a>_<b>` at the CHSH labels 0, N/8,
N/4, 3N/8 on the A2 board, N + 20 intervals, one birth per u: S as the
integer ratio at each N against the design's 2896/1024 and the bound
|E - cos| <= 1/N (`expectations.json` under `pair_n`; the register's L6
entry). `bell_n512_<a>_<b>`, the same at N = 512, added on 2026-09-21
for the pin of 24.4 (the section below).

## Bell at N = 512 and 4096 under the click and the wheel: the pin of 24.4

The run the law owes before the pin of
[DERIVATIONS_BEAM section 24.4](../../../docs/DERIVATIONS_BEAM.md#244-the-one-prediction-the-paper-can-carry)
is final (the Boss's order of 2026-09-21 under the model owner's record
337): the registered Bell geometry of L6 (the A2 bar of 21, the lamp at
x = 10 on two arms with the labels 00 and 11, Alice's counters at x = 7
and 4, Bob's at 17 and 18, the four counters reading `sum`) under the one
click and the wheel [1, N], at N = 512 (`bell_n512_<a>_<b>`, the CHSH
labels 0, 64, 128, 192; 532 intervals; added by the generator on
2026-09-21, every other shipped world byte-identical) and at N = 4096
(the registered `bell_n4096_<a>_<b>`, 4116 intervals). **Pinned before
the run (`expectations.json` under `bell_24_4`, the counts per cell under
`pair_n`; the derivation: the design's joint weights on the half-angle
tables of 2N and the ladder's rungs b_k = (2 W C_k + T) // (2 T) on the
wheel W = N, BEAM_LAW notes 37 (iii) and 46):** S = 181 / 64 = 2.828125
exactly at both N (1448 / 512 and 11584 / 4096) over the quadruple
E(0, N/8) - E(0, 3N/8) + E(N/4, N/8) + E(N/4, 3N/8); the marginals W / 2
exactly (256 / 512 and 2048 / 4096) on every world; every count over the
W births within one of W x its cell's weight over the total; the cells
(++, +-, -+, --) at N = 512: 219, 37, 37, 219 (E x 512 = 364) at (0, 64),
37, 219, 219, 37 (-364) at (0, 192), 218, 38, 38, 218 (360) at (128, 64)
and at (128, 192); at N = 4096 the registered 1749, 299, 299, 1749
(2900), 299, 1749, 1749, 299 (-2900), 1747, 301, 301, 1747 (2892) twice.
What refutes: any count outside its rung by more than one, a marginal off
W / 2, or S off 181 / 64; no number moves after the run.

**Run (2026-09-21, main a625ec9f, the runner headless one world at a
time, `python -m event_universe --init <world> --output <dir>`; the
source sha256 `47fffbefe2d222b7...`, the families' `438444b1cec9eb47...`,
the initialization shas per world in the register's run block;
completed and conserved at every tick, the books balanced; DETECTOR,
the gathers of the first W records by ordinal):** every pin met on the
eight worlds: the counts per cell equal to the pinned counts to the
unit, E x W 364, -364, 360, 360 at N = 512 and 2900, -2900, 2892, 2892
at 4096, S = 1448 / 512 and 11584 / 4096, both exactly 181 / 64;
Alice's and Bob's + counts 256 of 512 and 2048 of 4096 on every world;
every count within one of W x its weight (the widths 218.62 / 37.38 and
218.40 / 37.60 at 512, 1748.96 / 299.04 and 1747.20 / 300.80 at 4096);
the rungs on every gather of a world one list, the pinned one (the
records' totals take 57 distinct values at N = 512 and 139 at 4096, the
tables' rounding by u of note 37 (xii), and move no rung); one gather per
record, W of W gathered (531 born in 532 intervals, 519 gathered and 12
open at the end at N = 512; 4113, 4101 and 12 at 4096: the lamp's clock
stalls as the births spend its content). GAMEBOARD: conserved at every
completed tick, the books balanced at every tick. The host: the runner's
wall time 1.50 to 1.54 s per world at N = 512 and 9.32 to 9.64 s at
4096 on a loaded host (the engine's own 1.24 to 1.27 s and 8.74 to
9.05 s), reported apart from the model's cost, the bar's 21 Nodes at
fixed local work per interval over 532 or 4116 intervals and one
record's offers held at the layer until its completion. Verdict: PASS,
the pin of 24.4 stands as written; `tests/test_amplitude_bell_24_4.py`
derives the pin from the worlds and the ladder and replays the eight
worlds bit-exact against the registered counts.

## L7: the cone, which length a row's phase counts

`cone_links` and `cone_intervals`: one geometry, two lamps of `light` (at
(0, 0) on +x to a counter 17 Links away; at (0, 3) on the plane diagonal
(1, 1, 0) to a counter at (12, 15), 24 Links on the staircase, the same
Euclidean distance to one percent), N = 64, 96 intervals; the integer form
of `phase_per_link` (3 per Link stepped) against the pair form [3, 1] (3
per interval of age). The flight table puts both rows at their counters at
the age 29; the path phase at the click is 51 and 8 under the integer form
(the Links) and 23 and 23 under the pair form (the intervals)
(`expectations.json` under `cone`; the register's L7 entry). The question
of issue #376 (the paper session): the cone is Euclidean by the flight
table; the phase's metric is the declared form's. Under the exact phase at
the click (2026-09-21, BEAM_LAW note 45) the pair form's click lines carry
`exact` and `remainder`: 3 x 17 x 110 = 5610 = 87 x 64 + 42 at the axis and
3 x 24 x 156 = 11232 = 87 x 128 + 96 at the diagonal, the whole part 87 =
23 mod 64 at both as the walk's 3 x 29, the remainders 42 / 64 and 96 / 128
(`expectations.json` under `cone.exact`); the integer form writes none.

## A12 under the click: Malus's law from the table entries in force

**The order.** The model owner's go on Malus (record 330 of
docs/LOG_2026-09-20.md, on the programs of record 300, item 11); the
mathematician's note [docs/designs/malus/NOTE.md](../../../docs/designs/malus/NOTE.md)
(the verdict: a polariser is built from the entries in force, no feature
11; the three worlds of its section 2; the pin of its section 3 from its
`malus_map.py`) is the pin. No `src/` change, no new key; the register's
entry is [A12](../../../docs/EXPERIMENTS.md#a12-maluss-law-and-the-three-polarizer-chain-after-feature-11).

**The worlds** (the note's section 2; the generator's `malus_worlds`):
one bar `[7, 1, 1]`, N = 256 (the half-angle tables of 2N = 512 exist), K
and the lamp's content as `rotations_3`'s (2^50), `release` [0, 1], 300
intervals (256 births at the rate [1, 1], six Links of flight, the
completions). The lamp at x = 0: `light`, the rate [1, 1], the wheel
[159, 256] (159 the odd integer nearest to 0.618 x 256; u = ordinal x 159
mod 256 runs over every residue once), the direction +x, no `branches`
(every row born on the label 0, along y). World `malus_c` alone: at x = 2
a measured event of `light` with `{light: {rule: rerelease, rotate:
{setting: 64}}}` on +x, the first polariser at 45 degrees (in `malus_a`
and `malus_b` the polariser at 0 degrees is the born axis). At x = 4 a
counter with `{light: {rule: read}}` and the detector `first` reading
`sum`: the projection, the pass label 0 and the absorbed label 1, whose
rows go on to the end and click in their own cells (no body sinks them;
the detector counts them). At x = 6 a counter with `{light:
{phase_window: s}}` and the detector `second` reading `sum`, the last
polariser: s = 64 in `malus_a` (one polariser at 45 degrees), 128 in
`malus_b` (two crossed), 64 in `malus_c` (a third at 45 degrees between
two crossed). A chain of rotations without a read composes to one
rotation (`rotations_3`); the read is what carries the intermediate angle.

**The reading, named before the run.** The `gather` lines' `chosen`
[set, arm, channel] per record: the cell named by the read's label and
the end's channel (`0+`, `0-`, `1+`, `1-`), the pass the cell `0+`; the
counts over the records of the ordinals 1 .. 256 (DETECTOR). The books
(GAMEBOARD) at every interval. The `split` lines at x = 2 in `malus_c`,
for whether the rotate keeps the record's u or counts a rebirth (BEAM_LAW
note 46): the re-emitter's record lines.

**Pinned before the run** (the note's section 3; `expectations.json`
under `malus`, the cells' weights the products of the tables' entries,
C'[64] = S'[64] = 181, C'[128] = 0, S'[128] = 256, the counts the click's
rungs b_k = (2 W C_k + T) // (2 T) over W = 256 births, the amount and
the read's factor cancelling in the rungs):

| world | the entries | the cells' weights | the rungs | the counts (DETECTOR, expected) | Malus |
| --- | --- | --- | --- | --- | --- |
| `malus_a` | the read, the window 64 | 0+ 181^2, 0- 181^2 | 0, 128, 256 | 0+ 128, 0- 128 | 1/2: 128 of 256, exact |
| `malus_b` | the read, the window 128 | 0+ 0, 0- 256^2 | 0, 0, 256 | 0+ 0, 0- 256 | 0: exact |
| `malus_c` | the rotate 64, the read, the window 64 | 0+, 0-, 1+, 1- 181^4 each | 0, 64, 128, 192, 256 | 0+ 64, 0- 64, 1+ 64, 1- 64 | 1/4 of the births, 1/2 of the 128 the first passed: exact |

The fail clauses, A12's as the note states them: `malus_c` passing 0 or
128 in the cell 0+ (the intermediate angle not carried); `malus_a`
passing other than 128; `malus_b` passing other than 0; any cell off its
rung width; the books not conserved at every tick; a `split` line off
the design's two rows per row.

**Run (2026-09-21, each world once through the runner, 300 intervals,
1.4 to 1.7 s each, the source `e81a378ceec0b7f8...`, the initializations
`eab7bb354b3459ac...`, `1075554cf04a7ee2...`, `f6a2dc74887ffdb5...`;
completed and conserved at every tick).**

    PYTHONPATH=src python -m event_universe --init examples/events/amplitude/malus_a.json --output artifacts/malus_a

and the same for `malus_b` and `malus_c`; the run's `world` holds the
gathers. DETECTOR: over the records 1 .. 256 (u over every residue once in
each world; one cell list per world, the registered rungs on every
gather) `malus_a` 0+ 128, 0- 128; `malus_b` 0+ 0, 0- 256; `malus_c` 0+
64, 0- 64, 1+ 64, 1- 64: every pin met exactly, none moved; over every
record gathered by the end (299 born, 289 gathered, 10 open at the end;
the first gather at tick 11) 145 / 144, 0 / 289 and 73 / 72 / 72 / 72,
every cell within its rung width. GAMEBOARD: the books balanced at every
one of the 300 intervals. The u question: the rotate keeps the record's
u and counts no rebirth; the 592 `split` lines at x = 2 of `malus_c` (two
per arriving row, 296 records) carry `rebirth` False, the record's own
identity and its birth u; the `rotate` line 2 rows, the record's units 1
to 362 (181 + 181 at the multiplicity 65536); the `read` line at x = 4
sees the record's two rows, the labels 0 and 1 at the amount 181, the
phases 0 and 128 (the set bit a half turn on). Note 46's rebirth is a
re-emitter chosen by a click, not a rotate on the GameBoard. **Verdict:
PASS** on every clause in the three worlds. **The limit:** one which-path
read per arm with a rotation before it; the four-polariser chain of A12
at 22.5-degree steps needs a second read after a rotate and is not
covered (the note's section 1); the tables' rounding shows at 22.5
degrees (219 of 256 against cos^2 = 0.8536, the note's section 3), not
run here. `tests/test_amplitude_malus.py` derives the pin from the worlds
and the engine's tables and replays the three worlds against the register.

## The pages with a moving picture (2026-09-21)

The folder `pages/` holds two pages for the model owner (visualisation
requested, 2026-09-21), each one file with its frame player and its GIF
inside: `click.html`, one record of `slits_low` from its birth to its
click and its deletion ([E15](../../../docs/EXPERIMENTS.md#e15-the-click-of-one-record-shown-2026-09-21)),
and `bell.html`, the pair of the four CHSH worlds with the register's
correlations and S ([E16](../../../docs/EXPERIMENTS.md#e16-the-pairs-two-clicks-shown-2026-09-21)).
`pages/build_pages.py` rebuilds them: it runs the registered worlds with
the runner, steps them again in-process for the frames (the rows of one
record and its offers in the layer, read through the engine's own
`Layer.cells` and `rungs`), checks the replay's gathers against the run
and writes the pages beside itself:

    PYTHONPATH=src python examples/events/amplitude/pages/build_pages.py --runs artifacts/pages

Every number on a page is the run's or the register's, and the page names
its source; the runs stay outside the tree.
