# Rows 8b and 8c by the algebra: the steps between clicks, the redeclared J2 world, the pins before the run (the FAIL Runner B, 2026-09-23)

The order (the Boss, 2026-09-23, one bounded task under the owner's word of
record 1128 of `docs/LOG_2026-09-20.md`, "start putting all the FAILs in
order by the algebra", and the reviewer's read AE of record 1126): turn the
paper's Table 2 rows 8b (the neutrino's passage: 16 of 1024 at the first
reader, 0 behind it, the far detector 699 of 711, series J2, DETECTOR;
nature about 1) and 8c (the massless neutrino: the `nu` family with no
content, an input; nature's heaviest neutrino mass state above 9.8 x 10^-8
of the electron's) by the one DECLARATION that section 1.9 of
`docs/designs/fail_rows/WHAT_IS_MISSING.md` (branch `fail-rows`, head
`2252bbd`) names for both: the `nu` family's quantum 1 under the world key
`massive_rows`, the reader's window reading the turned phase (mode D of the
clicks). Before any run the algebra must confirm that the run's steps are
exactly the steps between click and click (section 1); the world is
declared (section 2); the pins are written by kind with their arithmetic
(section 3); the cost and the command (section 4). STEP 1 is this file: no
run, no law change, no engine line, no default changed, nothing under a new
key. STEP 2, on the Boss's GO after the physics-rule reviewer's read of
section 1, is the run and its readings in section 5 of this file.

Base commit `e404baa1` (`origin/main`, "Merge pull request #965"). The files
beside this one: `j2_massive.json` (the world, section 2, validated by the
configuration validator at load, never run), `run_8bc_pins.py` and its
output `run_8bc_pins.out` (the pins of section 3 computed from the engine's
own tables of the loaded world, no run); `run_8bc_readings.py` and its
output `run_8bc_readings.out` (STEP 2: the run's record read against the
pins, section 5); `j2_reemit.json` and `j2_reemit_control.json` (STEP 3a,
the re-emitter world and its control, validated at load, never run) with
`run_8bc_reemit_pins.py` and its output `run_8bc_reemit_pins.out` (the
pins of section 6 from the engine's own tables); `run_8bc_reemit_readings.py`
and its output `run_8bc_reemit_readings.out` (STEP 3b: the two runs read
against those pins, section 6.3).

**The kinds of every number** (HIGHLIGHTS 5.4): DETECTOR, a click or a
record line of a declared detector, the only kind compared with nature or
pinned; GAMEBOARD, the host's view (a tick, the flight table's arrivals, a
row's columns), a diagnostic, never pinned or compared with nature;
COMPUTATION, arithmetic on readings or a number the algebra gives in closed
form with no run; CONVERSION, an Outside number from a detector's counts by
a named reading; HOST, a cost of the machine. Every result is stated as
matching nature, never as how nature is; nature's "about 1" is the thing
compared with.

**The symbols, named once.** N the phase circle's grain, 64; Q the label's
scale, 64; S_w the width of the push, the world key `width`, 1; M a row's
content in units, the family key `quantum`; h the action per Link of the
turn, the world key `action`; p the momentum label's magnitude, the lamp's
`momentum_magnitude`; **p**_D the integer label of one unit on the direction
D at the scale p (`scaled_label`); E'_0 = Q S_w M the rest energy; E'_D =
isqrt(E'_0^2 + 3 **p**_D . **p**_D) the pace wall; x the Node's coordinate
along the bar in Links; u the record's birth coordinate, the wheel's value
written on the row at its birth; K the clock's rate, the world key `K`; w a
window's width in steps of the circle (`phase_width`), 1 at every reader; c
the pace of a light row on a heading, 64 / 110 Links per interval.

## 0. The verdict of the trace, at the top

The window reads the turned phase: the row's phase column after the walk's
turn at every Link (section 1, steps 5 and 6, the lines quoted). But for a
row of a RECORD it reads the turned phase LESS u, the record's birth
coordinate (`nature_beam.py` :4633, `path = (phase - store.birth[at]) %
modulus`, "what every rule of the GameBoard reads of a record row's phase";
u is the ladder's selector, never a phase a window reads). A massive family
births records and nothing else (`world.py` :3751, "the massive family has
no lamp" is a refusal; the release form's row has the rate 0 on a paid
family, `measured.py` :433). The registered J2 source has no lamp: its rows
are rows of no record, `birth` 0, and its window reads the raw phase, the
clock's stride plus the turn; that is the class filter of section 1.9 and
0b (16 of 1024, 0 behind). Under `massive_rows` every row of the beam
carries the same path phase at a Node, floor(55 x / 4) mod 64 for the
declared p = 220 and h = 1024, whatever its u: a reader is not a class
filter over u but an all-or-nothing gate per Node. What the run reads
(COMPUTATION, section 3, reading A): the first reader (x = 8) 0 of 1024, the
second (x = 9) 0, the reader at x = 14 the whole beam that reaches it (1014
of 1014, the path phase 192 = 3 x 64 steps), every reader behind it 0, the
far detector 0. Section 1.9's pins (16, 1.000, the far detector 0 by the
64 classes covered) are computed beside it as reading B, with the class
arithmetic the Boss ordered, and are NOT what this run reads: the wheel's
16 rows per class exist on the record (the `u` field of every `pass` and
`click` line, a diagnostic) and no window reads them. The pins of the run
are reading A; the difference between A and B is on record before the run,
and the physics-rule reviewer decides whether the run is worth its seconds
or the row's word moves from DECLARATION to a READING the click does not
make. The reviewer's word (2026-09-23, the gate of record 1129, GO subject
to two lines): the run is worth its seconds as the first click reading of a
massive row's turn per Link (A3, the beat at h / p = 4.65 Links); the row
8b stays FAIL under the declaration by the law's design of the path phase
(BEAM_LAW stage (vii) step 2), its word a READING under existing keys (the
re-emitter arrangement of section 3) beside the DECLARATION, and a window
on a record's raw phase a RULE outside the law, not needed.

## 1. The steps between clicks

Each step is tagged click (a detector's or a clock's count), declaration (a
world integer or key) or computation (one of the six verbs on declared
integers, exact). Every code line is the head of `origin/main` at
`e404baa1`; `nature_beam.py` is `src/event_universe/events/nature_beam.py`,
`world.py` and `measured.py` beside it.

1. **declaration: the source's rows are born with the declared content.**
   The world declares `massive_rows: true`, `action: 1024` (h), `width: 1`
   (S_w), `N: 64`; the family `nu` declares `quantum: 1` (M, the minimal
   mass, record 243: one unit and not free) and `massive: true`; the
   family `d` (the readers and the far detector) `quantum: 1`, no phase
   circle, as registered. The source is a `lamp` of `nu` at x = 0 with
   `momentum_magnitude: 220` (p), `directions [[1, 0, 0]]`, `rate [1, 1]`
   (one record per self-creation), `wheel [1, 64]` (u), its held content
   2^30 at K = 2^30 (the turn 1, section 2). A lamp is the only birth of a
   massive family's rows: `world.py` :3751 refuses a massive family with no
   lamp, and the release row of a paid family has the rate 0
   (`measured.py` :433, `release[0] if is_free else 0`).
2. **computation: the family's tables at load.** `nature_beam.py`
   :1187-1189 (`family_flight`): `rest = Q * width * definition.quantum`
   (E'_0 = 64 x 1 x 1 = 64); `rate, wall, start = flight_triple(labels,
   rest)` on the label **p**_D = (220, 0, 0) of the heading: the triple
   (440, 772, 386), E'_D = isqrt(64^2 + 3 x 220^2) = isqrt(149296) = 386;
   `turn = np.abs(labels) * modulus`, the numerator |p_x| N = 220 x 64 =
   14080 over the denominator h = 1024 (the `action` handed to
   `FamilyFlight` as `turn_denominator`). The loaded world prints these
   (`run_8bc_pins.out`, "THE WORLD"). The shift per Link is 14080 / 1024 =
   55 / 4 = 13.75 steps, not 0 mod 64: the edge case p = 2^12 with h a
   power of two (256 steps per Link, 0 mod 64, every reader at the first's
   class) is named and avoided.
3. **the lamp's count (GAMEBOARD; nothing pinned from it) and computation:
   one record per interval, u by the wheel.** The lamp's turn is the count row `Count("turn",
   "content", 0, 0, turn_rate[0], turn_rate[1])` (`measured.py` :429):
   `by_clock` over its held content at the rate [1, K]; at held K it is 1
   at every self-creation (`nature_beam.py` :6002, `cost =
   definition.quantum * turn` = 1, and :6013 refuses a massive birth whose
   turn is not 1). The record's coordinate u = ordinal x r mod W with the
   wheel [r, W] = [1, 64] (`birth_coordinate`, :714: "u = ordinal x r mod
   W, the ordinal from 0"): the j-th birth carries u = j mod 64, so 1024
   births put 16 rows in each of the 64 classes (COMPUTATION). The row is
   born with the phase `(u + lamp_turn) % modulus` (:6089, `lamp_turn` 0:
   the lamp's `turns` key absent) and the column `birth` = u: its path
   phase at birth is 0.
4. **computation: the flight.** `FamilyFlight.accumulator` (:1084, `held =
   age * self.rate[direction] + self.start[direction]`, the count `held //
   wall`): the row has made floor((440 tau + 386) / 772) Links at the age
   tau, one Link per count on the x axis. The ages: 14 at 8 Links (the
   photon's 13), 15 at 9, 24 at 14, 333 at 190 (the photon's 326)
   (GAMEBOARD, the flight table; `run_8bc_pins.out`, "THE ARRIVALS"). The
   pace 220 / 386 = 0.56995 Links per interval, 2.04 percent below c on the
   heading (COMPUTATION).
5. **computation: the turn at every Link crossed.** In `_walk`
   (`nature_beam.py` :4189, called at :3427 before the step-4 plans of
   :5703), :4376-4380: `count, after = table.turned(store.acc_turn[crossed_rows],
   store.direction[crossed_rows], port[crossed_rows] >> 1)` and
   `store.acc_turn[crossed_rows] = after`, where `FamilyFlight.turned`
   (:1110) is `return by_drive_rows(accumulator, self.turn[direction, axis],
   self.turn_denominator)`: ONE accumulator per row over the whole path,
   the count to the phase, the remainder kept on the row. Then :4391,
   `store.phase = (store.phase + turned) % modulus`. After x Links on the x
   axis the count is floor(14080 x / 1024) = floor(55 x / 4) exactly
   (`run_8bc_pins.py` asserts it Link by Link against `by_drive_rows`): 110
   at x = 8 (46 mod 64), 123 at x = 9 (59), 192 at x = 14 (0), 1856 at x =
   135 (0), 2612 at x = 190 (52).
6. **click: the reader's window.** Step 4, `_family_plan` (:4543), reads
   the rows at the measured events after the walk of the same interval:
   :4633, `path = (phase - store.birth[at]) % modulus`; in `admit()`,
   :4801, `read_phase = path[met].copy()` (the one-Node `wave` set's
   pointer of one row of amount 1 is that row's path phase, the nearest
   step of `coherent_pointer`); :4826, `inside = (window < 0) |
   ((read_phase >= 0) & window_admits((read_phase - window) % modulus,
   width_m, modulus))`; :4842, `passing = below | ~inside`: a row outside
   the window writes a `pass` line and walks on, a row inside is taken (the
   click; under `massive-rows-v1` the record's completion places q_F = M =
   1 into the reader's `held`, the tables' `placed` 0 and `quantum` 1 as
   loaded). So the window reads the TURNED phase (step 5's column), less
   u. The reader at x with the window (centre 0, width 1) admits a row
   when (floor(55 x / 4) mod 64) is 0, every row of the beam alike: x =
   14 (192 = 3 x 64) and x = 135 (1856 = 29 x 64) among the 128 readers;
   every other reader admits nothing (COMPUTATION, `window_admits` itself
   over the 128 shifts, `run_8bc_pins.out`, "READING A"). What the run reads
   if the window read the raw phase instead, as the registered J2's rows of
   no record are read: reading B of section 3, the class filter.
7. **computation: the count at a reader, the ratio of two counts.** The
   first reader's count is its clicks over its arrivals (its `click` and
   `pass` lines, DETECTOR); the second reader's count over the first's is a
   ratio of two DETECTOR counts (COMPUTATION), nature's about 1 the thing
   compared with.
8. **click: the far detector.** The entry at x = 190 measures `nu` with no
   window: `inside` is true by `window < 0` (:4826), every arriving row is
   taken; its count is the beam that passed all 128 readers (DETECTOR).

**Measured inside the board: NO.** The readers' own lines are the reading
(8b); the content is an input (8c), as section 1.9 says. The three tests
on the declaration: generic (the quantum and the turn table are values of
the family's table, no branch on a name; the photon's table is the same
form at E'_0 = 0), vector (the turn is `by_drive_rows`, the translation of
an accumulator by its rate with the remainder kept; the window one floor),
local (the row's own accumulator and phase, nothing kept at a Node). No
rule enters the law by this file.

## 2. The world: `j2_massive.json`, the J2 world redeclared under `massive_rows`

The registered `examples/events/weak/j2_filter.json` (model
`beam-weak-j2_filter-v1`) with these declarations and nothing else moved:

| key | `j2_filter` | `j2_massive` | why |
| --- | --- | --- | --- |
| `model_id` | `beam-weak-j2_filter-v1` | `beam-fail-rows-j2_massive-v1` | a world of this design, not of the register |
| `massive_rows`, `width`, `action` | absent | `true`, 1, 1024 | the identity's key; S_w = 1; h = 1024, the massive register's pin (55 / 4 steps per Link at p = 220) |
| `families` | `nu` (quantum 0) and `d` from `entities/families.json` | inline: `nu` quantum 1 `massive`; `d` quantum 1, `phase` false | the declaration of 1.9; the entity file is outside this folder's reach, the families are the same two |
| the source | a measured event of `nu`, amount 4096, `directions [[1, 0, 0]]` (the release form, rows of no record) | a `lamp` of `nu`: `rate [1, 1]`, `wheel [1, 64]`, `directions [[1, 0, 0]]`, `momentum_magnitude 220`; amount 2^30 | a massive family births only by a lamp (`world.py` :3751); u = j mod 64 gives 16 rows per class over 1024 births |
| `K` | 4096 | 2^30 = 1073741824 | the lamp's turn is `by_clock` over its held content at [1, K] and a massive birth needs the turn 1 at every birth (`nature_beam.py` :6013); each birth spends 1 unit, so the lag of the count after t births is about t^2 / (2 K): with K 4096 it passes 1 by the 91st birth and births are skipped, with K 2^30 it is 5 x 10^-4 after 1038 births, no birth skipped. K sets no stride here: u is the wheel's, the window reads no clock |
| `ticks` | 1037 | 1038 | the age at 8 Links is 14 for the massive row (13 for the photon), so the births at the ticks 1 .. 1024 reach the first reader within the run: 1024 arrivals, sixteen turns of the wheel exactly, as registered |
| `age_bound` | the default | 1024 | declared, as the massive register declares it (the row's pace below the flight's); the longest row of the run, born at tick 1, reaches x = 190 at the age 333 |
| `release`, `suspension`, `N`, `shape`, `boundary` | [1, 4096], 0, 64, [200, 1, 1], open | the same | unread by a paid family's lamp (`release`); nothing else moved |
| the 128 readers at x = 8 .. 135 | `d`, amount 1, fixed, `measure` on `nu` with `phase_window 0`, `phase_width 1` | the same, byte for byte | the readers in line, as registered |
| the far detector at x = 190 | `d`, `measure` on `nu`, no window | the same | counts every row that reaches it |

The validator accepts the world at load (`python -m
event_universe.configuration_validation docs/designs/fail_rows/j2_massive.json
--json`: valid, 2 families, 130 measured events, 0 issues); the tables the
engine forms for it are those of section 1 step 2 (`run_8bc_pins.out`, "THE
WORLD"). The edge case named by the reviewer, p = 2^12 with h a power of two
(the shift 256 per Link, 0 mod 64, every reader the first's class, 0 behind
again), is avoided by p = 220, h = 1024.

## 3. The pins before the run, by kind, with the arithmetic

All from `run_8bc_pins.py` on the loaded world (COMPUTATION; the engine's
tables, `by_drive_rows` and `window_admits` themselves; no run).

**The arrivals** (GAMEBOARD, the flight table): one record per interval at
the ticks 1 .. 1038; the age at 8 Links 14, so the births 1 .. 1024 reach
the first reader: 1024 arrivals; at 9 Links 15: 1023 reach the second
reader if none is taken before; at 14 Links 24: 1014 reach x = 14; at 190
Links 333: the births 1 .. 705 reach the far detector within the run (the
registered photon world's 711 at the age 326).

**Reading A, the pins of this run** (what the code reads: the path phase,
section 1 step 6). The reader at x admits the whole beam that reaches it
when floor(55 x / 4) mod 64 = 0, else nothing:

| pin | the reading | kind | the arithmetic |
| --- | --- | --- | --- |
| A1 | the first reader (x = 8): 0 clicks of 1024 arrivals | DETECTOR (its `click` and `pass` lines; `events` of its state) | floor(55 x 8 / 4) = 110, 110 mod 64 = 46, not in [0, 1) |
| A2 | the second reader (x = 9): 0 of 1023; the ratio second over first 0 / 0, undefined | DETECTOR; the ratio COMPUTATION | floor(123.75) = 123, 123 mod 64 = 59 |
| A3 | the reader at x = 14: 1014 clicks of 1014 arrivals, the whole beam that reaches it | DETECTOR | floor(192.5) = 192 = 3 x 64, the path phase 0, inside the window; the births 1 .. 1014 reach x = 14 by the tick 1038 |
| A4 | every other reader 0; the far detector at x = 190: 0 of the 705 that would reach it | DETECTOR | the only other shift that is 0 mod 64 is x = 135 (1856 = 29 x 64) and nothing reaches it; the far detector's `inside` is true for every row that arrives, and none does |
| A5 | the raw phase on the `pass` lines of the readers at x = 8 .. 13: `phase` = (u + shift(x)) mod 64, `u` = (j - 1) mod 64 for the j-th birth, 16 of each value over the 1024 rows at x = 8 | GAMEBOARD (the row's columns on the record; a diagnostic of the class structure no window reads) | `phase - u` = 46 on every `pass` line at x = 8, 59 at x = 9 |

PASS / FAIL for the run against the pins: PASS if every reading equals A1
to A4 (the algebra of the path phase confirmed, one remainder over the whole
path); a differing count refutes the chain of section 1 or finds a rule it
forgot, and the number is never moved to it. Against nature ("about 1",
the row's claim): A1 and A2 read 0 and 0, A3 the whole beam at one Node, so
the row stays FAIL under the declaration, in a new form: not a filter that
takes 1 / 64 once and nothing behind, but a plane wave whose phase returns
to the window every 256 / 55 = 4.65 Links (h / p, the de Broglie length)
and is taken whole at the first reader whose Node lands on a whole turn
(x = 14, 192 steps). Nature's two detectors in line read the same rate;
this world's read 0 and 0 and then everything.

**Reading B, the pins of section 1.9 as the Boss ordered them** (the class
filter: what a window reading the raw phase u + shift would take; NOT what
this run reads, since `path` subtracts u): the reader at x takes the class
u = -floor(55 x / 4) mod 64 whole if no reader before it took that class:

| pin | the reading | kind | the arithmetic |
| --- | --- | --- | --- |
| B1 | the first reader: 16 of 1024 | COMPUTATION (would be DETECTOR under a window on the raw phase) | 1024 / 64 = 16 rows per class; x = 8 takes the class -110 mod 64 = 18 |
| B2 | the second reader at a fresh class: 16; the ratio 1.000 exactly | COMPUTATION | x = 9 takes the class -123 mod 64 = 5; 16 / 16 = 1.000; nature about 1 the thing compared with |
| B3 | the far detector: 1024 - 16 per distinct class among the 128 readers' shifts: the 64 classes are all covered (by the reader at x = 127), 1024 - 16 x 64 = 0; within the run 0 of 705 | COMPUTATION | the shifts floor(55 x / 4) mod 64 over x = 8 .. 135 take all 64 residues (55 / 4 per Link, 128 Nodes) |
| B4 | the readers behind x = 127: 0 | COMPUTATION | no fresh class remains |

Under reading B the second reader over the first would match nature's about
1 and the far detector 0 would not match a beam that passes: the row would
turn on the ratio and fail on the depth. No window reads the raw phase of a
record's row under the keys as they stand (the birth column on every lamp's
row, the window subtracting it; the lamp's `turns` a constant per
direction). Reading B's class filter is reachable by one more click: a
re-emitter between the lamp and the readers, whose rebirth keeps the
running phase and writes a new u from its own wheel (`nature_beam.py`
:5847-5872), declared with the wheel [2, 64] against the lamp's [1, 64] so
that the path phase behind it is -j mod 64 over the births; that world is
STEP 3 if ordered, its pins B1 to B4 with the re-emitter's clicks counted,
validated at load before any pin (the physics-rule reviewer's line (i) of
2026-09-23). That is the finding of this file; it moves no number of
section 1.9 and no word of the law.

**The FAIL conditions of the run** (against the pins A): a click at x = 8
or x = 9 (the path phase read as the raw phase, or the turn not the plane
wave's); the reader at x = 14 reading fewer than 1014 (a class filter after
all, or the turn's remainder split across rows); any click at a reader
other than x = 14; the far detector above 0; the books not balanced at every
tick; a `pass` line at x = 8 whose `phase - u` is not 46 (the turn not
floor(55 x / 4)).

**Row 8c, the comparison side** (COMPUTATION, no run). The `nu` quantum 1
is the minimal mass, one unit. Nature's bound m_nu / m_e >= 9.8 x 10^-8
(the paper's row 8c, PDG 2024 and KATRIN 2022) puts the electron's content
at M_e >= 1 / (9.8 x 10^-8) = 10204082 units, 1.02 x 10^7; its rest energy
E'_0 = Q S_w M_e = 64 x 1 x 10204082 = 653061248, 6.53 x 10^8, whose square
4.27 x 10^17 is inside the working bound 2^63 - 1 = 9.22 x 10^18 and the
label bound 2^62 - 1 = 4.61 x 10^18 (the split ladder never forms X Q^2;
section 1.9). The register's electron today is the free family `e` (quantum
0, its measured event's amount its content: ENTITY_CATALOG.md, the
electron's row); this file declares the quantum 1 on `nu` alone and moves
no content of the electron. 8c turns on the declaration alone (the input
is no longer 0) and asks the electron's declaration for 1.02 x 10^7 units
when the two are declared in one world; no run reads it.

## 4. The cost and the command

HOST: the registered J2 worlds run in about 3 s each (200 x 1 x 1, 1037
intervals, at most about 200 rows in flight); this world adds the record
form (one record per interval, the layer's bookkeeping) and one interval:
about 10 s, under a minute, one core. The run:

```bash
PYTHONPATH=src .venv/bin/python -m event_universe --init docs/designs/fail_rows/j2_massive.json --output artifacts/fail_rows/j2_massive
```

The readings for section 5 (STEP 2): per reader its `events` of `run.json`
(the units clicked, DETECTOR) and its `pass` lines of `events.jsonl` (the
arrivals not taken, DETECTOR), with the `u` and `phase` fields of those
lines (GAMEBOARD, the diagnostic of pin A5); the far detector's `events`;
`conserved_at_every_completed_tick` of `run.json` (the books). A reader
script beside this file is written in STEP 2 and its output committed with
the readings.

## 5. The readings (STEP 2, on the Boss's GO of 2026-09-23, the reviewer's gate)

The run of `j2_massive.json` as declared in section 2, headless, through
the shipped runner (the command of section 4): status completed, 1038
intervals, the engine's own elapsed 4.02 s and 6.1 s wall on one core
(HOST); source sha256 `5166dbe90169655d`, world sha256 `ad26eddd321fc3d6`
(`run.json`; the run's folder under `artifacts/` expires by the retention
policy, the readings are kept here). Read by `run_8bc_readings.py` beside
this file, its output `run_8bc_readings.out`, against the pins A1 to A5 of
section 3 as written before the run; no pin is moved, a differing integer
is a FAIL, its cause named beside it. The declaration under which every
number is read: `massive-rows-v1` with the `nu` quantum 1 at p = 220, h =
1024 (the run's `hypotheses`: `amplitude-v1`, `massive-rows-v1`, and
`bohr-v1` carried by the world key `action` as the record writes it).

| pin | as written | read | kind | verdict |
| --- | --- | --- | --- | --- |
| A1 | the first reader (x = 8): 0 clicks of 1024 arrivals | 0 clicks of 1023 arrivals (1023 `pass` lines, `events` [0, 0]) | DETECTOR | the clicks PASS; the arrivals FAIL by one |
| A2 | the second reader (x = 9): 0 clicks of 1023 arrivals; the ratio 0 / 0 | 0 clicks of 1022 arrivals; the ratio 0 / 0, undefined | DETECTOR; the ratio COMPUTATION | the clicks PASS; the arrivals FAIL by one |
| A3 | the reader at x = 14: 1014 clicks of 1014 arrivals, the whole beam that reaches it | 1013 clicks of 1013 arrivals, 0 passes: the whole beam that reaches it, every record completed there (1013 `gather` lines, every `chosen` at (14, 0, 0); the reader's `held` [1013, 1], q_F = 1 per completion) | DETECTOR | the whole beam PASS; the integer FAIL by one |
| A4 | every other reader 0; the far detector 0 | no click at any of the other 125 readers; the far detector (x = 190) 0 clicks, 0 passes | DETECTOR | PASS |
| A5 | the `pass` lines at x = 8 carry `phase - u` = 46, at x = 9 59; 16 rows per u value at x = 8 | `phase - u` = 46 on all 1023 lines at x = 8, 59 on all 1022 at x = 9; at x = 8 the 64 u values with 15 or 16 rows each (the class of the missing birth 15); the `click` lines at x = 14 `phase - u` = 0 on all 1013, the age 24 on every one, the 64 u values with 15 or 16 rows each: every class taken, no class filter | GAMEBOARD (the row's columns on the reader's line) | PASS |
| the books | balanced at every tick | `conserved_at_every_completed_tick` true over 1038 intervals | GAMEBOARD | PASS |

**The cause of the one-birth deficit, named and confirmed** (COMPUTATION;
no pin moved). The lamp's `birth` lines: 1037 records at the ticks 1 and 3
to 1038, none at the tick 2. The lamp's count row (`measured.py` :429,
`Count("turn", "content", ...)`: the accumulator gains the held content
each interval against the wall K = 2^30, the count taken, the remainder
kept) replayed by `by_drive_rows` in `run_8bc_readings.py`: at the tick 1
the accumulator gains 2^30, the count 1, the remainder 0, and the birth
spends one unit; at the tick 2 it gains 2^30 - 1, below the wall by one,
the count 0; from the tick 3 the remainder 2^30 - 1 carries every later
count to 1 (the deficit t^2 / (2 K) of section 2 stays below 1 through
the tick 1038). Section 2's arithmetic took the lag as a running sum and
missed that the very first count has no remainder to carry: the births are
1, 3 .. 1038, so the arrivals at x = 8 are the births 1, 3 .. 1024, 1023 of
them, at x = 9 the births 1, 3 .. 1023, 1022, and at x = 14 the births 1,
3 .. 1014, 1013, exactly as read. This is a rule of the lamp's count that
the chain of section 1 step 3 (the lamp's count, GAMEBOARD) forgot, not a
rule of the row: the turn per Link (A5, the `phase - u` of every line),
the all-or-nothing gate at the Node of the whole turn (A3's "whole beam",
A4) and the far detector are as the algebra of the path phase gave them.
A run whose lamp held K + 1 at the start would birth at every interval and
read 1024 / 1023 / 1014; that world is not run here, since no pin moves
after a run.

**The falsifiers of section 3, checked.** A click at x = 8 or 9: none. The
reader at x = 14 reading fewer than 1014: 1013, tripped by one, the cause
above (a class filter would have taken 16 rows of one u value; the reader
took 15 or 16 of every one of the 64). A click at any other reader: none.
The far detector above 0: 0. The books not balanced: balanced. A `pass`
line at x = 8 whose `phase - u` is not 46: none. The rows in transit at the
end: 24, at x = 0 .. 13, the births that had not reached x = 14 by the last
interval (GAMEBOARD, `state.json`).

**The verdict of the run.** Against the pins as written: A1 FAIL, A2 FAIL,
A3 FAIL (each by the one missing birth of the tick 2), A4 PASS, A5 PASS,
the books PASS. Against the chain of section 1: the window reads the turned
phase less u, exactly as traced (the `phase - u` of every line the reader
wrote, 46, 59 and 0, are floor(55 x / 4) mod 64 at x = 8, 9 and 14), and
the reader at the Node of a whole turn takes the whole beam: the first click
reading of a massive row's turn per Link, the beat at h / p = 256 / 55 =
4.65 Links, confirmed at x = 14. Against nature (row 8b, two detectors in
line reading the same rate, about 1): the first and the second reader read
0 and 0 and the reader at x = 14 everything, so the row stays FAIL under
the declaration `massive-rows-v1` with the `nu` quantum 1, in the form
section 0 states, by the law's design of the path phase (BEAM_LAW stage
(vii) step 2); the row's word is a READING under existing keys (the
re-emitter arrangement of section 3, STEP 3 if ordered) beside the
DECLARATION. Row 8c is unchanged by the run: a computation (section 3),
the input no longer 0. Nothing enters the paper from this file.

## 6. STEP 3a: the re-emitter world, the chain, the pins before the run (the owner's word, record 1150; the Boss's order of 2026-09-23, 01:00Z)

The reviewer's line of section 3, built as a world: between the lamp and
the readers a re-emitter whose rebirth keeps the running phase and writes a
new u from its own wheel, so that the readers behind it are class filters
and reading B is read. Docs and the world files only; the run (STEP 3b) on
the Boss's GO after the reviewer's gate; no pin moves after a run. The
files: `j2_reemit.json` (the world), `j2_reemit_control.json` (the
control, the same wheel at both), both accepted by the validator at load
(2 families, 5 measured events, 1 detector set, 0 issues), never run;
`run_8bc_reemit_pins.py` and its output, every number below from the
engine's own tables of the loaded worlds, `by_drive_rows` and
`window_admits` themselves.

### 6.1 The steps between clicks, each tagged

1. **declaration: the world.** `j2_massive.json` of section 2 with the 128
   readers replaced by the registered arrangement of series J2: the first
   reader at x = 8, a second reader at x = 9, the far detector at x = 190
   (the `d` family, `measure` on `nu`, the readers' window 0 of width 1,
   the far detector without a window, byte for byte as registered); the
   lamp at x = 0 as in section 2 (`nu` quantum 1 `massive`, p = 220, h =
   1024, the wheel [1, 64], `rate [1, 1]`), holding K + 1024 = 1073742848
   (why, step 3); and the re-emitter at x = 4: a fixed `d` event with the
   table entry `nu: {rule: rerelease, weights: [1]}` on `directions [[1,
   0, 0]]`, its Node the one-Node `sum` set `reemit` (a `rerelease` entry
   on a `sum` set ends the arriving units there with an offer and
   re-creates them as a new record when the record chose that set:
   ENGINE.md, the world file's table entries; `tests/test_amplitude_layer.py`
   (k), the registered rebirth world), and a `lamp` block `{rate: [1, 1],
   wheel: [2, 64], directions: [[1, 0, 0]]}` whose only work is the wheel:
   at held 1 against K = 2^30 its turn is 0 at every interval and it births
   nothing of its own (`nature_beam.py` :5990, `turn > 0`); the
   rebirth's u is read from `entry.lamp_wheel` (`birth_coordinate`, :714:
   "on a lamp, u is the accumulator of the `wheel` row of its counts table
   before this birth advances it by the declared rate r over W"; without a
   lamp "u is its count of births less one mod N and W is N, the case [1,
   N] as built", the control). The keys are existing keys, the families
   the same two.
2. **the lamp's count (GAMEBOARD; nothing pinned from it) and computation:
   one record per interval, u = j.** The reviewer's line at M3
   (massive_rows/DESIGN.md): a lamp holding exactly K births at the first
   self-creation and not at the second. Holding K + d it births at every
   interval while the count row's remainder d t - t (t - 1) / 2 stays
   above 0 (COMPUTATION, the row replayed by `by_drive_rows` in
   `run_8bc_reemit_pins.py`: at held K the interval 2 has no birth, at K +
   1 the interval 4, at K + 1024 none through 1038, and none through
   2049); so the j-th birth (j from 0) is at the tick j + 1, u = j mod 64,
   16 births per class among the first 1024 (COMPUTATION). The turn is
   never 2 (the gain is below 2 K), so every birth is at the turn 1 (M3).
3. **computation: the flight and the turn to the re-emitter.** As section
   1 steps 4 and 5: the row born at the tick t reaches x = 4 at the age 7
   (the tick t + 7; GAMEBOARD, the flight table) with the phase u + 55
   (floor(55 x 4 / 4) = 55, the remainder 0) and the path phase 55.
4. **click: the re-emitter's own.** Step 4 takes the row at the `sum` set
   `reemit` (a `rerelease` entry: no window, the amount gate alone,
   `inside |= (rule == RERELEASE_RULE) & (record != NO_RECORD)`, :4832),
   the row goes pending with `offered` (:5430) and its units end in the
   layer with the record's one offer; the completion is read after step 4
   (`nature_beam` docstring: "its completions are read after step 4 and
   after the merge"), the ladder chooses the one offer, the `gather` line
   names `reemit`, the completion places q_F = 1 into the re-emitter's
   `held` (section 3 of massive_rows/DESIGN.md), and the pending row is
   marked `rebirth` (:6606-6610). This is the re-emitter's click: every
   record clicks there once (DETECTOR, its `gather` lines and its state).
5. **computation: the rebirth.** Step 5 of the same interval re-releases
   the pending row (:5856-5872: `row_record` a new identity of this
   emitter, `row_birth` = the new u from `birth_coordinate`, the
   `rebirth` flag on the `split` line) as one new record of one row on
   [1, 0, 0] at the age 0 with the running phase kept, `(row.phase +
   turn_i) % modulus`, :5897, with `turn_i` 0, and,
   for a massive family, its direction's p_D and E'_D and `acc_turn` 0
   (massive_rows/DESIGN.md section 2, the re-release). The registered
   rebirth world confirms the timing (the record born at the tick 1
   gathers at the gate at the tick 4 and its rebirth's `split` line is at
   the tick 4). The new u = 2 k mod 64 with k the re-emitter's ordinal
   from 0; the records arrive in birth order at one per interval, so k =
   j. The path phase of the reborn row at its birth is (j + 55) - 2 j =
   55 - j mod 64 (COMPUTATION).
6. **computation: the turn behind the re-emitter.** A fresh accumulator
   from x = 4: shift(y) = floor(55 y / 4) after y Links, 55 at y = 4 (x =
   8), 68 at y = 5 (x = 9), 2557 at y = 186 (x = 190); the path phase at
   x is 55 + shift(x - 4) - j mod 64: 46 - j at x = 8, 59 - j at x = 9,
   52 - j at x = 190.
7. **click: the readers' windows.** As section 1 step 6 (`path = (phase -
   birth) % N`, :4633; `window_admits`, :4826): the reader at x = 8 admits
   the row when 46 - j = 0 mod 64, the one class j = 46 mod 64; the reader
   at x = 9 the class j = 59 mod 64, a fresh class; every other row
   passes. The window empties a class (section 0b's theorem, now on a
   record's rows): the reader is a class filter over the births, by the
   two wheels.
8. **click: the far detector.** No window: every row that reaches it is
   taken (DETECTOR).

Measured inside the board: NO. The re-emitter's gather lines, the readers'
and the far detector's lines are the readings; the content is an input.
The three tests: nothing enters the law; the re-emitter, the `sum` set,
the lamp block and the wheel are registered keys of amplitude-v1 and
massive-rows-v1, declared, and every step above is one of their verbs.

### 6.2 The pins before the run, by kind, with the arithmetic

The flight (GAMEBOARD, the flight table): the row born at the tick t is at
x = 4 at t + 7, at x = 8 at t + 14, at x = 9 at t + 15, at x = 190 at t +
333; over 1038 intervals the births 1 .. 1031 reach the re-emitter, 1 ..
1024 the first reader, 1 .. 1023 the second, 1 .. 705 the far detector.

| pin | the reading | kind | the arithmetic |
| --- | --- | --- | --- |
| B0 | the re-emitter: 1031 completions (one `gather` line each, chosen `reemit`) and 1031 rebirths (one `split` line with `rebirth` each, the new u the 32 even values) | DETECTOR | the births 1 .. 1031 reach x = 4 by the tick 1038; u = 2 k mod 64, k = 0 .. 1030 |
| B1 | the first reader (x = 8): 16 clicks of 1024 arrivals | DETECTOR | the class j = 46 mod 64 among j = 0 .. 1023: j = 46, 110, ..., 1006, sixteen; 1024 = 16 x 64, 16 per class |
| B2 | the second reader (x = 9): 16 clicks of 1007 arrivals; the ratio second over first 16 / 16 = 1.000 exactly | DETECTOR; the ratio COMPUTATION, nature's about 1 the thing compared with | 1023 births reach x = 9 less the 16 the first reader took; the fresh class j = 59 mod 64: j = 59, ..., 1019, sixteen |
| B3 | the far detector (x = 190): 683 clicks of the 705 that reach it | DETECTOR | 705 births (1 .. 705) less 11 of the class 46 (j = 46 .. 686) and 11 of the class 59 (j = 59 .. 699); 683 / 705 = 0.9688, the limit 62 / 64 = 0.9688; nature's near-total passage the thing compared with |
| B4 | the `pass` lines at x = 8 carry `phase - u` = (46 - j) mod 64, the 64 values 16 times each over the 1024 arrivals, the admitted rows those at 0; at x = 9 (59 - j) mod 64 | GAMEBOARD (the row's columns on the reader's line: the class filter visible) | u on those lines the rebirth's, 2 j mod 64; `phase` the running phase, j + 55 + shift(y) |
| the books | balanced at every tick | GAMEBOARD | the completion's q_F = 1 placed at the re-emitter and the re-released row's content 1 must balance through the `waiting` and `cancelled` lines; if they do not, the world is refused as a reading and the cause reported, not patched. The books are the admissibility gate (the physics-rule reviewer's line (i), 2026-09-23): balanced, the arrangement is a READING under existing keys and the pins are read; unbalanced, the completion of a massive row at a re-emitter is its click and no rebirth carries the quantum on, the world is refused as a reading, reading B is readable by no arrangement under existing keys for a massive row (it stays readable for light, whose pair is (1, 0)), and row 8b's word for the class filter returns to a RULE outside the law |

The control (`j2_reemit_control.json`, the re-emitter without a lamp
block: u_new = k = j): the path phase behind the re-emitter is 55 +
shift(y) for every row, the plane wave of section 3 again. C1 the first
reader 0 of 1024 (the path phase 46); C2 the second reader 0 of 1023 (59);
C3 the far detector 705 of 705 (the path phase 52 at x = 190 is not read:
no window); the re-emitter 1031 completions and rebirths as B0 (DETECTOR).
Cheap: seconds.

**The edge cases.** The same wheel at both: the control above. The shift
per Link 0 mod N (p = 2^12 at h = 2^10, the case the reviewer named): the
path phase behind the re-emitter is -j mod 64 with no turn, so the readers
are still class filters, every reader at x > 4 the class j = 0 mod 64, the
first taking 16 and every one behind it 0: the classes come from the two
wheels, the turn only fixes which class each reader takes; not run, named.
The second reader at a class the first took (shift(x - 4) equal mod 64 at
the two readers): 0 at the second; avoided at x = 8, 9 (55 and 68 differ
mod 64).

**The falsifiers.** A click count other than 16 at x = 8 or at x = 9 (the
window not a class filter, or the wheels not [1, 64] and [2, 64] in
effect); the same class at both readers (the second 0); the far detector
other than 683 (a class taken twice or none); the re-emitter's
completions other than 1031, or a `split` line without `rebirth` (the
re-emitter not a `sum` set in effect); a `pass` line at x = 8 whose
`phase - u` is not (46 - j) mod 64 for its birth's j; a birth missing
among the ticks 1 .. 1038 (the count row's remainder); the books not
balanced. A FAIL is written as FAIL and the pin stays. The books are the
admissibility gate (the reviewer's line (i)): balanced, the arrangement is
a READING under existing keys and the pins are read; unbalanced, the
completion of a massive row at a re-emitter is its click and no rebirth
carries the quantum on, the world is refused as a reading, reading B is
readable by no arrangement under existing keys for a massive row (it
stays readable for light, whose pair is (1, 0)), and row 8b's word for
the class filter returns to a RULE outside the law.

**The row's wording, conditional on the pins met, both halves** (the
reviewer's line (ii), written before the run): under massive-rows-v1 with
the nu quantum 1 AND a re-emitter declared between the source and the
readers (an arrangement of the law, not nature's), the second reader's
rate over the first's is 1.000 exactly (nature's about 1 the thing
compared with) and the depth is the filter's: one class of 64 lost at
each reader with a window, 62 / 64 at the far detector behind two,
nothing behind 64; the law's filter, not a cross-section; the registered
J2 (no re-emitter) reads 16 and 0 behind, the row FAIL for the law as
built; the re-emitter reading beside it a declared arrangement's, not a
pass against nature. The counts-table rate is the owner's second
declaration of the compared number; his word on it is pending, and this
file says so.

**The cost (HOST) and the commands.** About 6 s wall each on one core (the
world of section 5 took 6.1 s; the same size, one detector set and 1031
rebirths added):

```bash
PYTHONPATH=src .venv/bin/python -m event_universe --init docs/designs/fail_rows/j2_reemit.json --output artifacts/fail_rows/j2_reemit
PYTHONPATH=src .venv/bin/python -m event_universe --init docs/designs/fail_rows/j2_reemit_control.json --output artifacts/fail_rows/j2_reemit_control
```

The readings (STEP 3b, section 7 when run): per reader its `events` and
its `pass` lines (DETECTOR), the far detector's `events`, the re-emitter's
`gather` and `split` lines with their `u` (DETECTOR), the `phase - u` of
the pass lines (GAMEBOARD), the books; PASS / FAIL per pin B0 to B4 and C1
to C3, under the declaration `massive-rows-v1` with the `nu` quantum 1.

### 6.3 The readings (STEP 3b, on the Boss's GO of 2026-09-23, 01:3xZ, the reviewer's gate with lines (i) and (ii) above)

The two runs, headless, through the shipped runner (the commands above):
`j2_reemit` completed, 1038 intervals, 2.42 s the engine's own, 2.9 s wall
(HOST); `j2_reemit_control` completed, 1038 intervals, 2.50 s, 2.7 s wall;
source sha256 `5166dbe90169655d`, the worlds' sha256 `26fa288b15be89f6`
and `de9045f45b79d42e`. Read by `run_8bc_reemit_readings.py` beside this
file, its output `run_8bc_reemit_readings.out`, against the pins of 6.2 as
written; no pin moved.

**The books first, the admissibility gate** (GAMEBOARD): balanced at every
completed tick in both runs (`conserved_at_every_completed_tick` true).
The reviewer's open point, decided by the run: the completion of a massive
record at the re-emitter places nothing (every `gather` line chosen
`reemit` carries `content` 0 and `momentum` [0, 0, 0]; the re-emitter's
`held` of `nu` is 0 at the end, its own `events` 0), and the rebirth
carries the quantum on (each `split` line with `rebirth` born 1, the reborn
row of content 1, which the readers and the far detector then hold: `held`
16, 16 and 683). One unit where one was born; the arrangement is a READING
under existing keys and the pins are read.

| pin | as written | read | kind | verdict |
| --- | --- | --- | --- | --- |
| the lamp's births | one per interval, 1038 | 1038 `birth` lines over 1038 intervals, none skipped (held K + 1024) | GAMEBOARD | PASS |
| B0 | the re-emitter: 1031 completions and 1031 rebirths, u the 32 even values | 1031 `gather` lines chosen `reemit`; 1031 `split` lines with `rebirth`, 0 without; the rebirths' u the 32 even values 0, 2, ..., 62 | DETECTOR | PASS |
| B1 | the first reader (x = 8): 16 clicks of 1024 arrivals, the class j = 46 mod 64 | 16 clicks of 1024 arrivals (`events` [16, 0], 1008 `pass` lines); the clicked rows' u all 28 = 2 x 46 mod 64, the one class | DETECTOR | PASS |
| B2 | the second reader (x = 9): 16 clicks of 1007 arrivals, the fresh class j = 59 mod 64; the ratio 1.000 | 16 clicks of 1007 arrivals; the clicked rows' u all 54 = 2 x 59 mod 64; the ratio second over first 16 / 16 = 1.000 exactly | DETECTOR; the ratio COMPUTATION | PASS |
| B3 | the far detector (x = 190): 683 clicks; 705 births reach it within the run (GAMEBOARD) less 22 taken before | 683 clicks of 683 arrivals, 0 passes; the 22 rows the two readers took all among the births 1 .. 705 (their reborn records' ordinals), 705 - 22 = 683; the fraction 683 / 705 = 0.9688 | DETECTOR; the 705 GAMEBOARD | PASS |
| B4 | the lines at x = 8 carry `phase - u` = (46 - j) mod 64, the 64 values 16 times each, the clicked rows at 0 | the 64 values, 16 rows each over the 1024 lines; the 16 clicked rows all at 0 | GAMEBOARD (the row's columns on the reader's line) | PASS |
| C1 | the control, the first reader: 0 of 1024 | 0 clicks of 1024 arrivals; `phase - u` = 46 on all 1024 lines (the plane wave, one value) | DETECTOR; the phase GAMEBOARD | PASS |
| C2 | the control, the second reader: 0 of 1023 | 0 clicks of 1023 arrivals | DETECTOR | PASS |
| C3 | the control, the far detector: 705 of 705 | 705 clicks of 705 arrivals, 0 passes | DETECTOR | PASS |
| the control's re-emitter | 1031 completions and rebirths as B0 | 1031 and 1031, the rebirths' u the 64 values 0 .. 63 (the wheel [1, N] as built) | DETECTOR | PASS |

**The falsifiers, checked.** No count other than 16 / 16 / 683 / 1031; the
two readers at distinct classes (u 28 and 54); no `split` line without
`rebirth`; every line at x = 8 with `phase - u` = (46 - j) mod 64 (the 64
values 16 each, the clicked ones 0); no birth missing; the books balanced.
None tripped.

**The verdict, in the wording written before the run (line (ii)).** Under
massive-rows-v1 with the nu quantum 1 AND a re-emitter declared between
the source and the readers (an arrangement of the law, not nature's), the
second reader's rate over the first's is 1.000 exactly (nature's about 1
the thing compared with) and the depth is the filter's: one class of 64
lost at each reader with a window, 62 / 64 at the far detector behind two
(683 of 705, read), nothing behind 64; the law's filter, not a
cross-section; the registered J2 (no re-emitter) reads 16 and 0 behind,
the row FAIL for the law as built; the re-emitter reading beside it a
declared arrangement's, not a pass against nature. The counts-table rate
is the owner's second declaration of the compared number; his word on it
is pending. Row 8b's word after this run: a READING under existing keys
(this arrangement) beside the DECLARATION, as section 0 states; the
control confirms that the reading is the two wheels' and not the turn's
(the same wheel at both gives the plane wave, 0 and 0 and 705). Nothing
enters the paper from this file.

## 7. Links

- `docs/designs/fail_rows/WHAT_IS_MISSING.md` (branch `fail-rows`), sections
  0b, 1.9 and 2 item 2: the chain, the class filter, the pins 16 / 1.000 /
  the far detector by the classes covered.
- [massive_rows/DESIGN.md](../massive_rows/DESIGN.md) sections 1 to 3: the
  identity's keys, the flight and the turn of a massive row, the completion.
- [BEAM_LAW.md note 36 (i)](../../BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation):
  the window's width, the filter that is not an attenuation.
- examples/events/weak/README.md (`examples/events/weak/README.md`, deleted 2026-09-26),
  J2: the registered worlds and their expectations.
- The paper's Table 2 rows 8b and 8c (`paper/general_formula/main.tex`);
  [CRITERIA.md](../paper_criteria/CRITERIA.md) rows 8b and 8c.
- Records 1126 and 1128 of `docs/LOG_2026-09-20.md` (branch
  `claude/universe24-new-3ytqde` until merged): read AE's correction of the
  8b pins; the owner's word on the FAILs by the algebra.
