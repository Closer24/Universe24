# Row 10 by the algebra: the steps between clicks, the single opening under the one click, the pins before the run (the chief physicist, 2026-09-23)

The order (the Boss, 2026-09-23, one bounded task on the paper's Table 2
row 10, NATURE row 10, the single-opening spread `w x Delta(sin theta) /
lambda`, NOT YET under the one click: "the chain of steps between the
lamp's click and the screen's clicks with every step's kind; the two
worlds (w = 27 with the dense fan by angle, w = 9) as world files
validated at load, existing keys only; the pins before any run (0.92 +-
0.03 at w = 27 from DERIVATIONS_BEAM 22.2, the far-field 0.886, the
reading w x FWHM(sin theta) / lambda from the screen's clicks, the w = 9
pin, the falsifiers, the cost)"). STEP 1 is this file: no run, no law
change, no engine line, no default changed, nothing under a new key,
nothing in the paper. STEP 2, on the Boss's GO after the physics-rule
reviewer's read of section 1, is the run and its readings in section 5.

Base commit `e3eadecc` (`origin/main`, "Merge pull request #976"). The
files beside this one: `opening_w27.json` and `opening_w9.json` (the
worlds, section 2, validated by the configuration validator at load, never
run), `run_10_worlds.py` (the generator: the legs and the turns from the
engine's own flight table, the fan by selection), `run_10_pins.py` and its
output `run_10_pins.out` (the pins of section 3 computed from the engine's
own tables and ladder on the declared worlds, no run).

**The kinds of every number** (HIGHLIGHTS 5.4): DETECTOR, a click or a
record line of a declared detector, the only kind compared with nature or
pinned; GAMEBOARD, the host's view (a tick, the flight table's arrivals, a
row's columns, a re-emitter's line), a diagnostic, never pinned or compared
with nature; COMPUTATION, arithmetic on readings or a number the algebra
gives in closed form with no run; CONVERSION, an Outside number from a
detector's counts by a named reading; HOST, a cost of the machine. Every
result is stated as matching nature, never as how nature is; nature's 0.886
(the Fraunhofer constant, Nairz, Arndt and Zeilinger 2002) is the thing
compared with.

**The symbols, named once.** N the phase circle's grain, 64; Q the label's
scale, 64; K the clock's rate, the world key `K`, 2^30; W the birth wheel's
modulus, 4096, and u the record's birth coordinate on it (the wheel [2531,
4096], the golden wheel); n / d the phase per interval of age of the family
`light` (`phase_per_link` [8591334592, 2^30], 8.001304 steps); **D** = (a, b,
0) a direction of the table, S_1 = a + |b| its Manhattan length, T_D =
isqrt(3 |**D**|^2 Q^2) its flight table's resolution, m(tau) = (2 tau S_1 Q
+ T_D) // (2 T_D) the Links it has made at the age tau; c the pace on the
axis, S_1 Q / T_(1,0) = 64 / 110 Links per interval; lambda the wavelength
in Links, (N d / n) x c = 4.6538; w the opening's width in Nodes, L the
screen's distance in Links, 108; theta the angle behind the opening, s =
sin theta; FWHM the full width at half maximum of the screen's profile in
s, the half-maximum crossings interpolated linearly between pixels.

## 0. The verdict of the trace, at the top

Under the one click the single opening is one record per birth: the
lamp's w rows on w directions reach the w opening Nodes in phase (the
lamp's `turns` cancel each leg's whole phase, section 1 step 5), every
opening Node re-emits the record's row on the fan of 601 directions by the
equal split (step 6), every re-emitted row ends on a screen pixel or a face
at the exact phase of BEAM_LAW note 45 (step 7), and the record's
completion chooses ONE cell by the ladder on u (step 9): one click per
record, on a screen pixel or a face. The screen's counts over the records
are the DETECTOR reading (as the register reads `slits_huygens`: the
gathers of the records 1 to 4096); the FWHM of the counts in s and the
product w x FWHM / lambda are COMPUTATION on them; lambda is COMPUTATION
from the declared integers. Nothing is measured inside the board: the
opening Nodes are read by no detector, the profile is the detectors'
lines.

What the algebra reads before the run (COMPUTATION, section 3, from
`run_10_pins.out`): at w = 27 the counts per pixel as printed there (the
peak at y = 79 with 197 of 4096, screen 4052, faces 44) and from them w x
FWHM / lambda = 0.925, inside 22.2's pin 0.92 +- 0.03 (the Euclidean exact
sum at this Fresnel number, 1.45, gives 0.916; the far field 0.887); at w
= 9 the counts (the peak at y = 75 with 77, screen 4026, faces 70) and
0.879, inside 22.2's 0.886 +- 0.03 (the far field at w = 9, 0.891; the
Fresnel number 0.16). The product falls toward the far field as the
Fresnel number falls, as 22.2 expects.

**The finding of this file, before the run: the fan's grain at the axis.**
The register's Farey fan of width 48 (`slits_huygens`, A10's fan of width
12 before it) has no direction between (1, 0) and (47, 1): a hole of +-
1.22 degrees around every emitter's axis, 2.3 pixels at L = 108. With that
fan selected at 0.25 degrees the same algebra gives 0.880 at w = 27
(outside the band by 0.01) and 0.360 at w = 9, where the profile is a dip
on the axis between two humps (the first record's weights at y = 76 .. 84
half of those at y = 73 and 87), a shape of the fan and not of the
opening. The worlds therefore declare the fan of width 330 (the world key
`direction_bound`, existing) selected one direction per 0.15 degree, the
spacing of 22.2's own premise (record 155's fan by angle, 0.0026 in s):
the grain 0.126 .. 0.174 degrees everywhere, 0.0030 in s at the axis, a
third of the pixel's 0.0093. The products of every fan tried are in
section 3 (the product among the fans without a hole moves from 0.877 to
0.925 at w = 27 with the grain: the fans at 0.25 degree below the band,
the fans at 0.15 degree 0.916 to 0.925 inside it, a spread the size of
the band's width): the fan is chosen by the premise, the pin is 22.2's as
written, and the run confirms the integers of the chosen fan or refutes
the chain. No number moves after a run.

**The row's word, declared by the physics-rule reviewer before the run
(the gate of 2026-09-23 on this file at f8791203, GO subject to this
line), verbatim so that nothing moves after it:** "P1 and P3 bit for bit
is the chain CONFIRMED (not a pass against nature); against nature the
compared number is 22.2's near-field pin at each Fresnel number (0.92 +-
0.03 at w = 27, 0.886 +- 0.03 at w = 9; nature's 0.886 the far-field
constant the products fall toward); P2 inside its band AND P4 inside its
band AND P4 nearer 0.886 than P2 is the row's agrees: matches nature
within 22.2's band under the one click, the fan 22.2's premise (0.15
degree), the crowd form's 1.08 history; either outside its band is
disagrees with the number; below 0.85 is 22.2 refuted by its own words."
The status words are those of record 1166 (agrees / disagrees); "matches
nature", never "is nature". The reviewer's HOST note, taken: the ticks
are declared 8800 (w = 27) and 4700 (w = 9), so that the 4096th record,
born by the tick 8194 or 4097 and complete within about 260 intervals,
has a margin of about 340 intervals; no pin depends on the tick (the
worlds' sha changes, the pins do not).

## 1. The steps between clicks

Each step is tagged click (a detector's or a clock's count), declaration (a
world integer or key) or computation (one of the six verbs on declared
integers, exact). Every code line is the head of `origin/main` at
`e3eadecc`; `nature_beam.py` is `src/event_universe/events/nature_beam.py`,
`amplitude.py`, `world.py` and `engine.py` beside it; `two_slits_map.py`
is `docs/designs/fraction_free/two_slits_map.py`, whose walk of the
engine's digital line and flight table reproduced the registered runs of
`slits_low` and `slits_huygens` bit for bit.

1. **declaration: the world** (section 2). The family `light` with the
   pair form `phase_per_link` [8591334592, 2^30] (n / d) and `quantum` 1;
   the family `wall`, `quantum` 1. One lamp of `light` at (2, 80) holding
   K = 2^30, `rate` [1, 2] (w = 27) or [1, 1] (w = 9), `wheel` [2531,
   4096], w `directions` and w `turns`. The wall at x = 8: 161 measured
   events of `wall`, amount 1, fixed; the w opening Nodes (8, 80 - w // 2
   .. 80 + w // 2) carry `table {"light": "rerelease"}` and the fan as
   their `directions`. The screen at x = 116: 161 measured events of
   `wall`, each read by one `sum` detector `screen_y`, threshold 1. The
   direction table: `direction_bound` 330, the lamp's directions and the
   fan. K, N, `release` [1, 128], `suspension` 0, the plane 120 x 161 x 1
   with z periodic, as the register's `w27_wave`.
2. **computation: the family's tables at load** (`family_flight`,
   `nature_beam.py` :1137; `FamilyFlight.accumulator` :1078). The row of a
   massless family on the direction **D** makes m(tau) = (2 tau S_1 Q +
   T_D) // (2 T_D) Links by the age tau along the digital line of **D**
   (`world.py` :1690, `bresenham_line`; the two-slit map's `bresenham`,
   `resolution`, `manhattan_steps`): on the axis 64 / 110 Links per
   interval, c; on every heading the Euclidean pace |**D**| / S_1 x S_1 Q
   / T_D, within the isqrt of 1 / sqrt 3. The phase per interval of age
   is by_clock(age, n, d) (`_walk` :4381-4382, `by_clock_rows`), the whole
   part of age x n / d gained at each interval (`core/integer.py` :60),
   added to the row's phase column at every walk (:4391) after the age
   advances (:4390).
3. **the lamp's count (GAMEBOARD; nothing pinned from it).** At every
   self-creation of the lamp its count row gains 1 against the wall 2 (w
   = 27) or 1 (w = 9) (`entry.counts.advance("lamp")`, :6274): one record
   every second self-creation, or every one. The lamp's self-creation is
   its turn, by_clock over its held content at [1, K]: 1 at every tick
   while the held content is K, and the remainder after a birth's spending
   (w units per record) skips one tick near the start, as RUN_8BC read it
   (section 5 there: the count of the first tick has no remainder to
   carry); the deficit over the run, about w x (records)^2 / 2 against K,
   is 5.2 x 10^8 (w = 27, 8800 intervals) and 9.9 x 10^7 (w = 9), below
   K = 1.07 x 10^9: no other tick is skipped. The births by ordinal, the
   only count the pin uses: 4399 records in 8800 intervals at [1, 2], 4699
   in 4700 at [1, 1]; the records 1 to 4096 (one turn of the wheel) are
   the pin's, the 4096th born by the tick 8194 (w = 27) or 4097 (w = 9)
   and complete within about 260 intervals (step 7), inside the run with
   a margin of about 340 intervals (the reviewer's HOST note).
4. **computation: the birth.** The record's identity is the lamp's number
   x 2^32 + the birth's ordinal (`record_identity` :2530); u = ordinal x
   2531 mod 4096 (`birth_coordinate` :714, "u = ordinal x r mod W, the
   ordinal from 0"): over 4096 births every u once. The lamp births one
   record of w rows, one per direction, amount 1, content 1, multiplicity
   w (`paths x norm`, w x 1: the pair's default [[0, 1]]), each born with
   the phase (u + turn_j) mod N (:6089, `lamp_turn` the j-th entry of the
   lamp's `turns`, :6025) and the column `birth` = u, and the `birth` line
   (:6066, `u`, `units` w, `multiplicity` w).
5. **computation: the leg to the opening, in phase.** The j-th row walks
   its digital line (step 2) from (2, 80) and first reaches x = 8 at the
   Node the generator searched for it (`run_10_worlds.py`, `lamp_legs`:
   the primitive **D** of the smallest S_1, then the earliest arrival,
   whose walk lands on (8, 80 + j); the Euclidean vector (6, j) reduced does
   not do, since on the digital line (1, -1) and (6, -5) both land on (8,
   75) and (8, 67) is reached by no vector of that form). At its arrival
   age its phase column holds (u + turn_j + floor(age n / d)) mod N, and
   turn_j = -floor(age n / d) mod N by construction (the legs table in
   `run_10_pins.out`: the ages 10 .. 25, the whole phases 80 .. 200, the
   turns 48 .. 56, the sum 0 mod 64 on every leg), so every row of the
   record reaches its opening Node at the phase u: a plane front across
   the opening from one point lamp, by one existing key. The leg's
   remainder below n / d is the walk's own (note 45's second division)
   and is not carried across the re-emission: the re-emitted row starts
   its own count (step 6), as `slits_huygens_pin.py` models it and the
   registered run confirmed.
6. **the re-emission at the opening Node (GAMEBOARD: the re-emitter's
   `rerelease` and `split` lines; no detector reads the opening).**
   `_family_plan` (:4543) reads the arrived row at the wall event's Node;
   its rule for `light` is `rerelease` (:5413): the row goes to the
   entry's pending list with its phase, record, branch and multiplicity
   (:5414-5430, `PendingRow`), and the `rerelease` line is written
   (:5460). At the next tick the Node self-creates for its pending rows
   (:6241-6249, `any(entry.pending)`), and `_release_family` (:5812)
   splits each pending row over the entry's declared directions with
   every weight 1 and every turn 0 where no split is declared (:5864-5866,
   `(1,) * ways, (0,) * ways`): one row per fan direction, amount 1 x 1,
   the phase (row.phase + 0) mod N = u (:5897), the multiplicity w x 601
   (the norm, the sum of the squared weights, :5876), the `split` line
   (:5922, `born` 601, `multiplicity` 16227 or 5409). A plain
   `rerelease` is not in the load-time product of the record form
   (`world.py` :3295, `_record_load_checks`: "a plain rerelease is not in
   the product"); the run-time bound at the split (:5877-5882, the
   multiplicity times the norm against 2^62 - 1) holds 16227 with room.
7. **computation: the fan row's flight and its exact phase at its end.**
   Each re-emitted row walks its digital line from its opening Node until
   it steps onto a screen Node (x = 116) or leaves the GameBoard at a y
   face; within +- 45 degrees no fan row steps first in y, so no row is
   blocked at the wall (the pins script's `blocked` 0). Its phase at that
   end is note 45's: phi = phase - floor(terms n / d) + floor(n made T_D /
   (d S_1 Q)) mod N (`exact_phase` :637), with phase - floor(terms n / d)
   = u the re-emission's phase, so phi = u + floor(n made T_D / (d S_1 Q))
   mod N, `made` the Links of the row's own walk: the phase at the exact
   time of the last Link, the Euclidean length of the digital walk within
   the isqrt. The ages: the row on (1, 0) makes 108 Links in 186
   intervals; the longest screen rows (about 188 Links at 37 degrees)
   about 233; with the leg (25) and the re-emission (1) a record is
   complete within about 260 intervals of its birth.
8. **click: the row's end at the screen or a face.** The wall event at
   (116, y) measures the row (`measure`, :5488-5536): its units join the
   wall (:5499, the whole row at once, f_F = 1 for a family without
   `massive`), the `sum` set of `screen_y` takes the row's end with the
   exact phase (`layer.end` :5518-5531, `plan.t_exact[k][0]` :5525), and
   the `click` line is written (:5536, `phase`, `exact`, `remainder`). A
   row that leaves at a face is read before that walk's turn (note 45,
   the open face) and ends in the face's cell. A click of a row is an
   offer to the record, not yet the record's click.
9. **click: the record's completion, the one click.** When every row of
   the record has ended (`Layer.complete`, `amplitude.py` :901), the cells
   are weighed: per `sum` set the bilinear form over its Nodes, |sum of
   amount x (C, S)[phi]|^2 summed over the set's Nodes (`gram_form` :788;
   the pointer E f reported per set on the `record` line, `gather_records`
   `nature_beam.py` :6537-6600), the faces the same over their ends; the
   ladder on the record's wheel W = 4096 (`rungs` :241, b_k = (2 W C_k +
   T) // (2 T)) and the cell of u by the comparison of products (`cell_of`
   :275, called at :924): the `gather` line (:964) with `chosen` (:971) the
   set's name, one click per record on the screen pixel or the face
   chosen; `_place_completion` (:6616) places q_F = 0 for `light` (no
   `massive` flag: today's bytes) and cancels the rest of the record's
   waiting. The DETECTOR reading of row 10 is the count of `gather` lines
   per `screen_y` over the records 1 to 4096 (the register's reading of
   `slits_huygens`, the amplitude README: "the gathers of the records 1 to
   4096 equal to the pin bit for bit").
10. **computation: the reading.** From the counts per pixel: the peak, the
   half-maximum crossings on each side interpolated linearly between
   pixels in s = (y - 80) / sqrt(L^2 + (y - 80)^2), FWHM their
   difference, and w x FWHM / lambda with lambda = (N d / n) x c = 7.99870
   x 64 / 110 = 4.6538 Links (COMPUTATION from the declared integers;
   22.2's 8 c = 4.655 takes the period as 8). The pixel's grain in s at
   the axis is 1 / L = 0.0093, 6 percent of the FWHM at w = 27 and 2
   percent at w = 9 (the interpolation's own limit, inside the band).

**Measured inside the board: NO.** The opening Nodes are read by no
detector; the profile is the `gather` lines of the declared screen sets;
the product is arithmetic on them. The three tests on the declarations:
generic (the lamp's `turns` and the plain `rerelease` are values of
existing keys, no branch on a name; the family's tables are the massless
form of the same `family_flight`), vector (the turn at birth is one
addition mod N; the phase per interval `by_clock`; the click one floor),
local (the row's own age and phase, the re-emitter's pending list, nothing
kept at a Node beyond the events there). No rule enters the law by this
file.

## 2. The worlds: `opening_w27.json` and `opening_w9.json`

The register's A10 geometry (`examples/events/heisenberg/w27_wave.json`,
the crowd form: 27 lamps at x = 2 on (1, 0), a `wave` detector on the
opening, the 47-direction fan of width 12) in the record form of
`examples/events/amplitude/slits_huygens.json` (one lamp, the golden
wheel, `rerelease` openings, `sum` pixels). Both worlds are written by
`run_10_worlds.py` and differ in w, the lamp's rate and the run's length
only:

| key | `opening_w27` | `opening_w9` | why |
| --- | --- | --- | --- |
| `model_id` | `beam-row10-opening-w27-v1` | `beam-row10-opening-w9-v1` | worlds of this design, not of the register |
| `shape`, `boundary`, `K`, `N`, `release`, `suspension` | [120, 161, 1], z periodic, 2^30, 64, [1, 128], 0 | the same | the register's A10 plane and clock, as `w27_wave` declares them |
| `ticks` | 8800 | 4700 | the records 1 to 4096 born by the tick 8194 (the rate [1, 2]) or 4097 ([1, 1]) and complete within about 260 intervals (section 1 step 7), a margin of about 340 intervals |
| `direction_bound` | 330 | 330 | the fan's width (section 0: the hole at the axis of a width-48 fan); an existing key, 64 by default, at most 4096 |
| `directions` | 620 vectors: the fan's 600 off-axis directions and the 20 lamp directions not among them | 604: the fan's 600 and 4 | every vector a lamp or an opening names, once; (1, 0, 0) is a heading of the table already |
| `families` | inline: `light` quantum 1 `phase_per_link` [8591334592, 1073741824]; `wall` quantum 1 | the same | `entities/families.json` declares `light` with these keys; the entity file is outside this folder's reach at load, as `j2_massive.json` declares its families |
| the lamp | at (2, 80), `light`, amount 2^30, `rate` [1, 2], `wheel` [2531, 4096], 27 `directions` (the primitive vectors of section 3's legs table, (3, -7) .. (1, 0) .. (3, 7)), 27 `turns` (56, 8, 16, 32, 40, 56, 0, 8, 24, 32, 40, 40, 48, 48, 48, 40, 40, 32, 24, 8, 0, 56, 40, 32, 16, 8, 56) | the same at `rate` [1, 1] with the 9 middle directions ((3, -2) .. (3, 2)) and turns (32, 40, 40, 48, 48, 48, 40, 40, 32) | one record per birth on the whole opening; the turns cancel the legs' whole phases (section 1 step 5) |
| the wall at x = 8 | 161 `wall` events, amount 1, fixed; the 27 at y = 67 .. 93 with `table {"light": "rerelease"}` and the fan as `directions` | the same with the 9 at y = 76 .. 84 | the opening; a `wall` event with no table absorbs (`measure`) |
| the fan | 601 primitive directions, one per 0.15 degree from -45 to +45 degrees, each the nearest of the full fan a + \|b\| <= 330; unweighted | the same | uniform in angle by selection (22.2's premise); the plain equal split is outside the load-time product (section 1 step 6) |
| the screen at x = 116 | 161 `wall` events, amount 1, fixed; 161 `sum` detectors `screen_0` .. `screen_160`, threshold 1 | the same | the pixels, as `slits_huygens` declares them |

The validator accepts both at load (`PYTHONPATH=src python -m
event_universe.configuration_validation docs/designs/fail_rows/opening_w27.json
docs/designs/fail_rows/opening_w9.json --json`: valid, 2 families, 323
measured events, 161 detectors, 0 issues each). Nothing is under a new
key; no default is changed; the engine is untouched.

## 3. The pins before the run, by kind, with the arithmetic

All from `run_10_pins.py` on the declared worlds (COMPUTATION; the
engine's own `by_clock`, `phase_cosines`, `phase_sines`, `rungs` and
`cell_of`; no run). The constants: n / d = 8.001304 steps per interval,
the period 7.99870 intervals, c = 64 / 110 = 0.58182 Links per interval,
lambda = 4.6538 Links; the Fresnel number w^2 / (lambda L) 1.450 at w = 27
and 0.161 at w = 9.

**The legs** (GAMEBOARD, the flight table; the phases COMPUTATION on the
tables), w = 27, the j-th row for the Node (8, 80 + j): the direction, the
arrival age, the leg's whole phase mod 64, the turn:

| j | **D** | age | phase | turn | j | **D** | age | phase | turn |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| -13 | (3, -7) | 25 | 8 | 56 | 1 | (4, 1) | 10 | 16 | 48 |
| -12 | (4, -9) | 23 | 56 | 8 | 2 | (3, 1) | 11 | 24 | 40 |
| -11 | (1, -2) | 22 | 48 | 16 | 3 | (2, 1) | 11 | 24 | 40 |
| -10 | (4, -7) | 20 | 32 | 32 | 4 | (3, 2) | 12 | 32 | 32 |
| -9 | (3, -5) | 19 | 24 | 40 | 5 | (1, 1) | 13 | 40 | 24 |
| -8 | (2, -3) | 17 | 8 | 56 | 6 | (6, 7) | 15 | 56 | 8 |
| -7 | (3, -4) | 16 | 0 | 0 | 7 | (3, 4) | 16 | 0 | 0 |
| -6 | (6, -7) | 15 | 56 | 8 | 8 | (2, 3) | 17 | 8 | 56 |
| -5 | (1, -1) | 13 | 40 | 24 | 9 | (3, 5) | 19 | 24 | 40 |
| -4 | (3, -2) | 12 | 32 | 32 | 10 | (4, 7) | 20 | 32 | 32 |
| -3 | (2, -1) | 11 | 24 | 40 | 11 | (1, 2) | 22 | 48 | 16 |
| -2 | (3, -1) | 11 | 24 | 40 | 12 | (4, 9) | 23 | 56 | 8 |
| -1 | (4, -1) | 10 | 16 | 48 | 13 | (3, 7) | 25 | 8 | 56 |
| 0 | (1, 0) | 10 | 16 | 48 | | | | | |

The sum phase + turn is 0 mod 64 on every leg; every opening Node is
reached by exactly one row (asserted by the script). At w = 9 the legs are
the rows j = -4 .. 4 of this table.

**The fan** (COMPUTATION): 601 directions from -45 to +45 degrees, the
grain 0.126 .. 0.174 degrees (0.0030 in s at the axis); per record 16227
rows at w = 27 (13227 end on the screen, 3000 on the faces) and 5409 at w
= 9 (4419 and 990); 0 blocked.

**The first record (u = 0)** (COMPUTATION): the shares screen 0.989 /
faces 0.011 (w = 27), 0.983 / 0.017 (w = 9); the screen weights per mille
of the total at w = 27 rise from 2.6 at y = 60 to 48.2 at y = 79 and 81
(47.8 at y = 80) and fall to 2.6 at y = 100: the half-maximum crossings at
s = -0.0796 and +0.0796, FWHM 0.1593, the product 0.924; at w = 9 the
weights are 12.2 .. 18.8 per mille over y = 60 .. 100, a broad lobe with
the crossings at s = -+ 0.2267, FWHM 0.4534, the product 0.877.

**The pins of the run** (what the detectors read: the `gather` lines per
`screen_y` and per face over the records 1 to 4096, the ladder being
deterministic on the same 4096 u):

| pin | the reading | kind | the arithmetic |
| --- | --- | --- | --- |
| P1 | w = 27: the count of every screen pixel as printed in `run_10_pins.out` section 5 ("every screen pixel's count"), bit for bit; screen 4052 on 142 pixels, faces 44 (22, 22); the peak at y = 79 with 197 | DETECTOR (the `gather` lines' `chosen`) | the cell of u by `cell_of` on the 64 ladders (one per u mod 64), u = ordinal x 2531 mod 4096 over the ordinals 0 .. 4095; the counts within 1 of the first record's rungs |
| P2 | w = 27: w x FWHM(sin theta) / lambda = 0.925 | COMPUTATION on P1 | the half-maximum crossings at s = -0.0797 and +0.0797, FWHM 0.1595, x 27 / 4.6538; 22.2's pin 0.92 +- 0.03: inside; the Euclidean exact sum over 27 emitters at L = 108 on the 161 pixels 0.916 (22.2's (C)), the far-field array factor 0.887 |
| P3 | w = 9: the counts per pixel as printed there, bit for bit; screen 4026 on 127 pixels, faces 70 (35, 35); the peak at y = 75 with 77 | DETECTOR | the same ladder on the w = 9 record |
| P4 | w = 9: w x FWHM / lambda = 0.879 | COMPUTATION on P3 | the crossings at s = -0.2277 and +0.2269, FWHM 0.4546, x 9 / 4.6538; 22.2's pin 0.886 +- 0.03: inside; the Euclidean sum 0.891, the far field 0.891 |
| P5 | the books balanced at every completed tick | GAMEBOARD (`run.json`, `conserved_at_every_completed_tick`) | the ledger |
| P6 | the record's lines: per record one `birth` (`units` w, `multiplicity` w), w `rerelease` lines at the ages 10 .. 25 after the birth, w `split` lines (`born` 601, `multiplicity` 16227 or 5409, `rebirth` false), one `gather` with `chosen` one set; 4399 births in 8800 intervals at w = 27, 4699 in 4700 at w = 9 | GAMEBOARD (a diagnostic of the chain, never compared with nature) | section 1 steps 3, 4, 6, 9 |

PASS / FAIL for the run against the pins: PASS if every count of P1 and
P3 equals the printed integer and P5 holds; a differing count refutes the
chain of section 1 or finds a rule it forgot (the leg's remainder carried
across the re-emission, the exact phase read otherwise, the ladder's
order), and the number is never moved to it. Against nature (0.886, the
row's claim): P2 reads 0.925 at the Fresnel number 1.45 (4.4 percent above
the far field: the near field's 3.4 percent, 22.2, and the fan's grain) and
P4 reads 0.879 at 0.16 (0.8 percent below); the row's word after the run
(NOT YET to a reading under the one click, and whether "inside 22.2's
band" is the row's PASS) is the reviewer's and the Boss's, not this
file's; the NATURE row is not moved here.

**The fan's grain, a finding before the run** (COMPUTATION, the same
script on the same worlds with the fan alone changed; the products of the
clicks over 4096 records):

| the fan: width, grain, directions | w = 27 | w = 9 | note |
| --- | --- | --- | --- |
| 48, 0.25 deg, 337 | 0.880 | 0.360 | the register's width: no direction within 1.22 degrees of the axis; at w = 9 a dip on the axis between two humps |
| 110, 0.5 deg, 181 | 0.918 | 0.808 | the grain about one pixel |
| 220, 0.25 deg, 361 | 0.877 | 0.872 | no hole; the grain 0.186 .. 0.315 degrees |
| 220, 0.15 deg, 601 | 0.916 | 0.872 | 22.2's spacing; the grain 0.038 .. 0.262 degrees |
| 330, 0.15 deg, 601 (declared) | 0.925 | 0.879 | 22.2's spacing at a uniform grain, 0.126 .. 0.174 degrees |

Among the fans without a hole the product at w = 27 moves from 0.877 to
0.925 with the grain (the fans at 0.25 degree below the band, the fans at
0.15 degree 0.916 to 0.925 inside it), a spread the size of the band's
width: the reading of row 10 under the one click is of the opening AND of
the fan's grain at the level of +- 0.03, which is what 22.2's band says. The declared fan is the one that
meets the pin's premise (the spacing 0.0026 in s) at a uniform grain; the
pin is not chosen by the number. The reviewer may prefer another fan of
this table before the run; after it none moves.

**The FAIL conditions of the run** (against the pins): a count of P1 or
P3 off its printed integer; a `gather` whose `chosen` is a wall cell at x
= 8 (a lamp row that missed its opening: the legs wrong); a `split` line
with `born` other than 601 or `multiplicity` other than 16227 (w = 27) or
5409 (w = 9); a `rerelease` line at an age other than the leg's; a record
open at the end among the records 1 to 4096; the books not balanced. What
refutes 22.2 by its own words: a product below 0.85 at either width, or
the w = 9 product farther from 0.886 than the w = 27 product.

## 4. The cost and the command

HOST, scaled from the registered `slits_huygens` run (4300 intervals in
1334 s, 0.31 s per interval, about 2654 rows per record and about 100
records in flight: about 1.2 microseconds per row-interval). At w = 27:
16227 rows per record, a record complete within about 260 intervals, about
130 records in flight at the rate [1, 2]: about 2.1 million rows on the
GameBoard per interval, about 2.5 s per interval, 8800 intervals: about 6
h on one core, a few hundred MB for the row store. At w = 9: 5409 rows per
record, about 260 in flight at [1, 1]: 1.4 million rows, about 1.7 s per
interval, 4700 intervals: about 2 h. The two in parallel on two cores:
about 6 h wall; in series about 8 h. These are estimates from one
registered rate; the walk's cost per row at ten times the store may
differ, and a run may be stopped and restarted from nothing (no pin
depends on the tick). The runs, headless, through the shipped runner:

```bash
PYTHONPATH=src .venv/bin/python -m event_universe --init docs/designs/fail_rows/opening_w27.json --output artifacts/fail_rows/opening_w27
PYTHONPATH=src .venv/bin/python -m event_universe --init docs/designs/fail_rows/opening_w9.json --output artifacts/fail_rows/opening_w9
```

The readings for section 5 (STEP 2): the `gather` lines of `events.jsonl`
(`record`, `u`, `chosen`, `node`) over the records 1 to 4096, counted per
`screen_y` and per face (DETECTOR: P1 and P3), the FWHM and the product
from them (P2 and P4); `conserved_at_every_completed_tick` of `run.json`
(P5); the `birth`, `rerelease` and `split` lines (P6). A reader script
beside this file is written in STEP 2 and its output committed with the
readings.

## 5. The readings (STEP 2, on the Boss's GO after the reviewer's gate)

Not run. Written in STEP 2 against the pins of section 3 as they stand;
no pin moves after the run; a differing integer is a FAIL with its cause
named beside it.

## 6. Links

- [DERIVATIONS_BEAM.md section 22.2](../../DERIVATIONS_BEAM.md#222-the-pin-for-a10-under-the-one-click-nature-row-10-before-any-run):
  the pin 0.92 +- 0.03 at w = 27, 0.886 +- 0.03 at w = 9, the far field
  0.886, the exact sum 0.916, what refutes; its script
  `docs/designs/derivations_beam/uncertainty_lattice.py` and output.
- [NATURE.md](../../NATURE.md) row 10: the single-opening spread, NOT YET
  under the one click; the register's crowd-form 1.08 kept as history.
- examples/events/heisenberg/README.md (`examples/events/heisenberg/README.md`, deleted 2026-09-26):
  A10, the registered geometry and its readings (`w27_wave`).
- examples/events/amplitude/README.md (`examples/events/amplitude/README.md`, deleted 2026-09-26):
  `slits_huygens`, the record-form two-slit world, its run of 2026-09-21
  (4300 intervals in 1334 s) and the pin it met bit for bit;
  slits_huygens_pin.py (`docs/designs/paper_criteria/slits_huygens_pin.py`, deleted 2026-09-26), the
  machinery reused here.
- [BEAM_LAW.md note 45](../../BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation):
  the exact phase at the click; note 46, the birth wheel.
- two_slits_map.py (`docs/designs/fraction_free/two_slits_map.py`, deleted 2026-09-26): the walk on the
  engine's digital line and flight table.
- [RUN_8BC.md](RUN_8BC.md): the form of this file (rows 8b and 8c by the
  algebra) and the lamp's skipped tick (its section 5).
