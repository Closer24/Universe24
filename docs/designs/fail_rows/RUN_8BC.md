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
own tables of the loaded world, no run).

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

## 5. The readings (STEP 2, after the Boss's GO)

Not run. This section is written by the run's step, PASS / FAIL against the
pins A of section 3, under the declaration `massive-rows-v1` with the `nu`
quantum 1, every number by kind; nothing enters the paper from this file.

## 6. Links

- `docs/designs/fail_rows/WHAT_IS_MISSING.md` (branch `fail-rows`), sections
  0b, 1.9 and 2 item 2: the chain, the class filter, the pins 16 / 1.000 /
  the far detector by the classes covered.
- [massive_rows/DESIGN.md](../massive_rows/DESIGN.md) sections 1 to 3: the
  identity's keys, the flight and the turn of a massive row, the completion.
- [BEAM_LAW.md note 36 (i)](../../BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation):
  the window's width, the filter that is not an attenuation.
- [examples/events/weak/README.md](../../../examples/events/weak/README.md),
  J2: the registered worlds and their expectations.
- The paper's Table 2 rows 8b and 8c (`paper/general_formula/main.tex`);
  [CRITERIA.md](../paper_criteria/CRITERIA.md) rows 8b and 8c.
- Records 1126 and 1128 of `docs/LOG_2026-09-20.md` (branch
  `claude/universe24-new-3ytqde` until merged): read AE's correction of the
  8b pins; the owner's word on the FAILs by the algebra.
