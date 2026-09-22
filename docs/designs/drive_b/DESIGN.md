# drive-b-v1: the directional drive of a body, form B in its integer form (c), under its own key, off by default

The Drive Builder's design note, 2026-09-22, on the model owner's approval of
form B ("Form B is approved, go on it", record 652 of
[docs/LOG_2026-09-20.md](../../LOG_2026-09-20.md), through the Boss). Design
before build: the physics-rule reviewer read the note at 6e245ddd and found it
ADMISSIBLE WITH CORRECTIONS (the Boss, 2026-09-22, 04:15Z); his must-fix M1
(section 7) and should-fixes S1 (section 3), S2 (section 4) and S3 (section
2) are folded in here, in the build's first commit. Every number below is a HOST computation
of the count rule ([drive_b_map.py](drive_b_map.py), its output
[drive_b_map.out](drive_b_map.out)) or a derived pin, labelled GAMEBOARD or
DETECTOR where it names a reading; no run of the engine was made.

## The six lines

1. **The information.** A body's step moves its own record from its Node to
   the neighbour through the Port of one axis, at most one Link per interval,
   at the rate its momentum earns: per axis `p_a Q` label units per
   self-creation against ONE wall `W = Q^2 S M + |p|_1 T_h` on the body's own
   record. Kept: three signed residues `drive_a` on the record (the rows
   the counts table already has). Lost: nothing; a fire that coincides with
   another axis's fire is deferred to the next self-creation, where `main`
   drops it (DERIVATIONS_BEAM 1.3 item 7).
2. **The generic solution.** One primitive for every family: three
   accumulators translated by their rates and one argmax carry over one
   wall, the rows' own line rule (BEAM_LAW note 41 (viii), the deficits'
   argmax; the flight's `lines`) applied to the body's momentum, so that the
   body walks the digital line of **p** at the pace `|p|_1 Q / W` Manhattan.
   The wall's second term `|p|_1 T_h` is the cap, with `T_h = isqrt(3 Q^2) =
   110` the flight table's resolution on a heading, a constant of the law
   formed at load. Under `covariant_readings` the cap term is keyed off, as
   `step_divisor` keys it off today, and the wall is `Q^2 S M`.
3. **Why it works.** On a heading the rule is form B's count exactly
   (`|p| Q / (Q^2 S M + |p| T_h)` = `|p| x 64 / (Q S M x 64 + 110 |p|)`,
   FORM.md section 3.1 (c)); off the headings the three accumulators with one
   wall are Bresenham's line of **p**: every Node within one Link of the line
   (GAMEBOARD, the map's (A): 0.707 on the plane diagonal, 0.816 on the
   cube's), one Link per interval, the Manhattan pace `|p|_1 Q / W` on every
   direction. The reading that shows it (DETECTOR): the plane-diagonal body
   of the deciding world, `p = (3000, 3000, 0)`, M = 64, S = 1, from the
   centre of an open 41^3 box, clicks on face +x at tick 101 from the Node
   (40, 40, 20). The reading that refutes it: the same world on `main`'s
   per-axis drive clicks on +x at tick 50 from the Node (40, 20, 20), its y
   never moved (21 coincident fires lost); a click from a Node with y below
   39, or a tick outside 101 +- 1, refutes the rule as built.
4. **Why do it.** (i) The owner's route to the law (record 642) needs two
   worlds off the one axis (the J4 muon's momentum on the plane and the cube
   diagonals, 17.6 M8), which `covariant_readings` refuses today at load and
   at the frame because the per-axis base has no pace off an axis; the key
   lifts the refusal with the pace `p_a / (Q S M)` per self-creation on every
   axis, Euclidean `|p|_2 / (Q S M)`, times `E'_0 / E'` per lattice interval
   (the map's (E): the same E' and the same Euclidean pace 0.2481 on the
   axis, the plane and the cube at `|p|_2 = 3640`). (ii) Newton D3's pins
   (record 630) assumed this drive's pace on an axis (0.2033 against the
   per-axis 0.238 at n = 10); the orbit register's lamp worlds carry the
   same assumption. (iii) Record 301's registered defect: on `main` a body
   at `|p|_1 = 6000`, M = 64 runs at 0.594 Links per interval, above its own
   rows' 0.582; under the key 0.416, and no body outruns its rows on any
   line (the map's (C)). Not done, the covariant worlds stay refused, D3
   stays outside, and a diagonal body on `main` moves along one axis only.
5. **The Highlights kept.** Record 183's line (one motion primitive for a
   body as for a row) and 301's (form B built on the conditional yes) are
   the ones this build realises, in the integer form (c) the mathematician
   recommended after the review of record 348 (FORM.md 3.1); 202 (the three
   tests) holds, the three verdicts below; 281 (only a detector's reading is
   a measurement) holds, every pin a face click; 270 (the covariant readings
   beside the law) holds, the key composes with it by one term keyed off.
   One line should later change, on the owner's word and not here: 183 and
   301 describe the cap as the flight table's on the body's line (form B's
   Euclidean-isotropic cap), which FORM.md 3.1 proves unreachable exactly
   with a line-independent unit; the cap built is `64 / 110` on every
   direction, Manhattan-isotropic, below the rows' pace on every line and
   equal to it on the headings. 17.6 M8's sentence ("form B lands and
   re-registers its 47 moving-body worlds first") is superseded by the key:
   nothing is re-registered; its writer amends it when the build lands.
6. **The implementation.** The engine: one branch on the world key in
   `_move` (the key present: the line rule; absent: the code as it is, byte
   for byte); one primitive `core.integer.by_line` (three accumulators, one
   wall, the argmax carry) and its table method beside `advance`; the wall
   in `world.py` beside `step_divisor`; the key `drive_b: true` parsed
   beside `covariant_readings` and `optical`; the one-axis refusals of
   `_covariant` and `covariant_frame` lifted when the key is declared. The
   register: `examples/events/drive_b/` by a generator, three worlds under
   the key and three controls without it, the pins in `expectations.json`
   before the first run; the first world under the key enters the gate set.
   Documents: BEAM_LAW's note (the key's rule), ENGINE.md's key and
   hypotheses list, HYPOTHESES.md entry 28, TEST_EXPECTATIONS, EXPERIMENTS
   and VALIDATION rows, the covariant README's base sentence. Time, a host
   estimate: the design one hour (this note); the build four hours (the
   primitive and its test, the engine branch, the parser, the generator and
   the six runs of seconds each, the gate set's digests, the documents); the
   review one hour. Danger: low. The key is off by default and every
   registered world runs unchanged (the gate set's byte identity in
   `tools/check.py` guards it, with a test that replays one gate world to
   its digests); what can break is a body under the key whose wall passes
   the working bound (refused by name before the product) or an
   accumulator growing past the bound (checked before every addition). The
   key stays off; making it the default is the owner's later decision.

## 1. What the tree says, and where this note stands

- **Form B** is one of the two forms of the one motion primitive (records
  183, 186, 191, 201): a body walks the digital line of its momentum's
  direction with the rows' flight accumulator at the fraction its momentum
  earns, `rate = |p|_1 S_1 Q`, `wall = Q S M S_1 Q + |p|_1 T_D`
  ([light_speed/FORM.md section 3](../light_speed/FORM.md#3-the-vector-form-that-inserts-c-into-the-bodies-one-flight-primitive-for-rows-and-bodies)).
- **It was built once** as the default drive (PR #526, branch
  `directional-drive`, record 342: 61 movers re-registered) and **BLOCKED**
  by the physics-rule review (record 348, M1): the rate and the wall carry
  the line's `S_1` and `T_D`, so the accumulator's unit changes with the
  line, and a residue carried across lines discharges as consecutive Links
  above the pace the momentum earns (a body at 0.006 Links per interval
  making six Links in six intervals). The reviewer named three corrections,
  (a), (b), (c).
- **The mathematician's correction** (FORM.md 3.1): (a) closes M1 and leaves
  the deficits' unit (M1b); (b) needs unbounded storage or a declared
  rounding; **(c) is recommended**: three signed accumulators `drive_a`,
  the rate `p_a Q`, ONE wall `W = Q^2 S M + |p|_1 T_h`, one Link per
  interval on the axis furthest over the wall. No direction read, no bound
  P, no deficits, no root at run time. An exact form with form B's
  Euclidean-isotropic cap and one line-independent unit does not exist
  (3.1, "Why no accumulator..."); (c) changes the cap off the headings. The
  Boss's answer to the owner of record 385: form B merges "only after the
  rebuild on FORM.md 3.1 (c) and its review".
- **The Bresenham line of PR #702** (`nature_beam.py`, verb 3 of optical-v1:
  the walk along **P** by the error accumulator `c += h x P`, the pace by
  `momentum_pair`) is the same geometry built for light, under its own
  identity: its pair takes `isqrt(3 |P|^2 Q^2)` at run time per pushed row,
  a root the law does not admit (record 631, S5). Form B's analogue for a
  body is (c): the same digital line by three accumulators and one argmax,
  with a count against a wall and no root.
- **This note builds (c) under its own key**, off by default, as the Boss's
  rule (b) orders; the register is not re-registered. It differs from the
  Boss's phrase "the pace along P predicted from the flight table" in one
  respect stated plainly: the wall carries the flight table's heading
  resolution `T_h = 110` only, not the line's `T_D`; the flight table's row
  of the line enters the pins as the cap the body stays below (section 4).

## 2. The rule

**The key.** The world key `drive_b: true` (a boolean; absent or false, the
drive of BEAM_LAW note 17 runs unchanged; any other type refused at load
naming the key). The identity `drive-b-v1` is listed under `hypotheses`
when the key is declared, as `covariant-readings-v1` and `optical-v1` are.

**The integers.** Q = 64 the label's scale; S the world's `width`; M the
body's content at the self-creation (`frame_content`, as `_move` reads it);
`p_a` the momentum's component on axis a, `|p|_1 = sum |p_a|`; `T_h =
isqrt(3 Q^2) = 110`, the flight table's resolution on a heading, formed at
load (the one root, declared at load, not at run time).

**The wall.** `W = Q^2 S M + |p|_1 T_h`; under `covariant_readings` and the
key together, `W = Q^2 S M` (the cap term keyed off: the one primitive with
one term selected off, exactly as `step_divisor(cap=False)` today; the
pace per lattice interval is then `p_a / (Q S M) x E'_0 / E'`). The two
products are tested by division against the working bound before they are
formed, at load and at every push; a wall past it refuses the run naming
the rule (the neutron star's refusal of record 342 is of this kind).

**The step, at every self-creation of a body with content above 0
(`creating`; `fixed` never steps).**

    for every axis a with p_a != 0:  drive_a += p_a Q        (bounded before the addition: |drive_a| + |p_a| Q <= 2^62 - 1, else refused naming the rule)
    over = the axes a with p_a != 0 and |drive_a| >= W
    if over is empty: no step this interval
    else: a* = the axis of `over` with the largest |drive_a| (the lowest axis on a tie)
          the body steps one Link on axis a* toward sign(drive_a*)
          drive_a* -= sign(drive_a*) W
          the other accumulators keep their overflow for the following self-creations

- A component of 0 leaves its accumulator as it is and never steps (note
  17's rule: a momentum of 0 never steps); **p** = 0 never steps. Kept so
  for byte identity in form with `main`'s rule (S3): on one axis the key's
  count is `main`'s `by_drive` with both the rate and the wall scaled, the
  same fires from an empty accumulator, and an idle axis is idle in both.
- The signed accumulator cancels a reversal first (record 126): a momentum
  reversed by a hand-over discharges nothing toward the partner.
- The refused step (a contact) and the escape are the chosen axis's step
  refused or clicked, as today: W is subtracted (the step counted), the
  body does not move at a contact, the click on the face at an escape.
- The turn by momentum (`action`, `phase_by_momentum`): the `action` row of
  the stepped axis gains `|p_a| N` at every self-creation in which that axis
  is chosen (crossed or refused), and its whole part over h is delivered to
  the phase at the Link crossed, as today on the stepped axis; nothing is
  counted on an axis that did not step (no Link, no count: note 30 (ii)),
  so no count is discarded, since no fire is lost.
- The crossing rule (note 48) reads the body's step by its own Link as
  today: the line's next step is one Link on one axis per interval.

**The primitive in the code.** `core.integer.by_line(drives, rates, wall)
-> (axis | None, sign, drives)`: the translation of three accumulators by
their rates, the comparison with one wall, the argmax carry, one Euclidean
division with the remainder kept (`drive -= sign W` is `by_drive` with
`at_most` 1 on the chosen row). The counts table gains one method beside
`advance` that runs the three `drive` rows through it; the rows are the
ones the table has (`Count("drive", "momentum", ...)`, the accumulators
`entry.drive`), so the record's fields do not change. `_move` branches on
`world.drive_b` once, at its head; without the key the code as it is.

## 3. The three tests

1. **Generic: PASS.** One primitive with the declared integers `p_a`, M, S
   and the constants Q, `T_h`; no family name, no kind; the same primitive
   for every measured event; a body of no content never steps (the branch
   to state `content <= 0` as today); the engine branches on the world key,
   not on a name. The rows' line rule and the body's are one argmax carry.
2. **Vector: PASS.** The translation of three accumulators by their rates
   (verb T), the rate `p_a Q` linear in the state, the wall `Q^2 S M + |p|_1
   T_h` bilinear in (M, **p**) with declared constants; one comparison for
   the order; one Euclidean division with the remainder kept. No root at run
   time (`T_h` at load), no float, no direction read, no table beyond the
   counts table's rows.
Newton's limit (S1): `|p|_2 / (Q S M)`, isotropic, holds to zeroth order in
`v = |p|_2 / (Q S M)`; the Manhattan cap makes a first-order anisotropy, the
pace's ratio to Newton's being `1 / (1 + (|p|_1 / |p|_2) (T_h / Q) v)`, so
that two bodies of one `|p|_2` differ by `(|p|_1 / |p|_2 - 1) x 1.72 v`, at
most `0.73 x 1.72 v` between a heading and the cube diagonal (the map's (D)
at `v = 1 / 64`: 0.97385 on the heading against 0.97067 on the cube's).

3. **Local: PASS.** Reads the body's own record (**p**, M, the three
   accumulators) and the world's constants; writes its own record; the
   destination's occupant read as today (`_contact`); fixed work (three
   additions, three comparisons, one subtraction) and fixed storage (three
   integers already on the record) per self-creation; nothing at a Node;
   every host reading labelled GAMEBOARD.

LOCALITY-1 kept; the integer contract kept (the accumulator checked before
every addition, the wall's products by division before they are formed).

## 4. The deciding worlds and their pins, written before any run

`examples/events/drive_b/`, by `make_worlds.py`, never by hand. Six worlds:
three under the key, three controls without it, each `"law": "beam"`, an
open box `[41, 41, 41]`, K 2^20, N 64, `release` [1, 2^20] (no row within
the run), `suspension` 0 (nothing owed), `width` 1, 200 intervals; one
family `body` (quantum 0, no charge, `phase` false); one measured event of
`amount` 64 (M = 64, Q S M = 4096) at the centre (20, 20, 20) with the
momentum below and `directions` the six headings; the six open faces the
detectors. `|p|_1 = 6000` on all three, so the wall is one number, `W =
262144 + 660000 = 922144`.

| World | **p** | The key | The pin (DETECTOR: the face click's tick, face and Node) | The refuting reading (main's per-axis drive, HOST) |
| --- | --- | --- | --- | --- |
| `axis_b` | (6000, 0, 0) | on | tick 51 (+- 1 for the tick's numbering convention), face +x, from Node (40, 20, 20): the pace 0.4164 Links per interval | tick 36 from (40, 20, 20): 0.594, above the rows' 0.582 |
| `plane_b` | (3000, 3000, 0) | on | tick 101 (+- 1), face +x, from Node (40, 40, 20): 21 Links on x and 20 on y, the line of **p** within one Link, the pace per axis 0.2082 | tick 50 from (40, 20, 20): y never moved, 21 coincident fires lost |
| `cube_b` | (2000, 2000, 2000) | on | tick 152 (+- 1), face +x, from Node (40, 40, 40): 21, 20, 20 Links, the pace per axis 0.1388 | tick 65 from (40, 20, 20): y and z never moved, 42 fires lost |
| `axis_main`, `plane_main`, `cube_main` | the same | off | the refuting readings above as the controls' own DETECTOR pins: 36, 50, 65 from (40, 20, 20), byte for byte the drive `main` runs | |

The derivation of each pin ([drive_b_map.py](drive_b_map.py) (A)): the k-th
fire on axis x is at the first n with `n |p_x| Q >= k W`; the 21st x Link
(the escape from x = 40) is at `ceil(21 W / (|p_x| Q))` = 51, 101, 152; on
the diagonals x wins every tie (the lowest axis) and is never deferred, y
and z trail by one Link, so the click's Node is (40, 40, 20) and (40, 40,
40). The tolerance of one interval covers only the engine's tick numbering
(the drive's first advance at tick 1); the face and the Node are exact. A
run outside the pin is reported with its numbers and its cause, and moves
no number.

GAMEBOARD readings declared beside the pins (diagnostics, never compared
with nature): every `step` line's Node within one Link of the line of **p**
(0.707 on the plane, 0.816 on the cube); the `drive` accumulators after
every step below `3 W` (S2, proved: let E be the sum over the axes of the
excess `max(|drive_a| - W, 0)`; a self-creation's additions raise E by at
most `|p|_1 Q < W` (since `T_h > Q`); if an axis is then over the wall the
largest excess e* fires, and E falls by W when `e* >= W`, or to at most
`2 e* < 2 W` when `e* < W` (the other two excesses are each at most e*);
so from E = 0, E < 2 W after every self-creation and every `|drive_a| <
3 W`), and observed below `W + 2 max_a |p_a| Q` (the map's (F): 1.275 W at
most on the cube); the working-bound check before every addition is the
declared guard in the code; `fast_steps` 0 on the axis world.

The flight table's rows enter as the cap the body stays below (the map's
(C)): the rows' Euclidean pace on the line of D, `|D| Q / T_D`, is 0.5818,
0.5802, 0.5774 on (1, 0, 0), (1, 1, 0), (1, 1, 1); the body's cap on the
same lines `|D| Q / (S_1 T_h)` is 0.5818, 0.4114, 0.3359, the ratio 1 on
the headings and at least 0.5774 (the cube diagonal) over every direction;
the deciding bodies run at 0.4164, 0.2945, 0.2404 Euclidean, below both.

**The reviewer's two pins of record 348**, as tests on a minimal GameBoard
(a host replay against the engine, no world of the register): (1) a body at
a constant `|p|_1 = 6000` whose direction cycles every 50 intervals through
(6000, 0, 0), (3000, 1000, 2000), (0, 6000, 0), (2000, 2000, 2000),
(-3000, -1000, 2000): the Links on every axis after 1000 intervals 112, 112,
83 against the whole parts `floor(sum_t p_a(t) Q / W)` 111, 111, 83, within
2 at every n (the map's (B) equals the mathematician's
[drive_residue_map.out](../light_speed/drive_residue_map.out) (B) integer
for integer); (2) a hand-over transient of -720 on y for one interval,
cancelled the next, leaves the residue -46080 = -0.050 Link on y (at most
`|delta_y| Q / W`) and fires no y Link in the 100 intervals after.

## 5. The tests, written first and failing on `main`

`tests/test_drive_b.py`, one rule on a minimal GameBoard, the integers
written here:

- (a) the key absent computes nothing: every registered world outside
  `drive_b/` parses with `drive_b` false and the identity absent; the gate
  set's `detector/grouped_12_nodes` replays to `gate_set.json`'s digests
  byte for byte (the pattern of `test_covariant_readings.py` (a));
- (b) `by_line` against `by_drive` on one axis: from an empty accumulator
  at a constant `p = (6000, 0, 0)`, M = 64, S = 1, the fires at the
  self-creations where `floor(n x 384000 / 922144)` rises, the 21st at n =
  51; the accumulator `n x 384000 mod 922144` with the sign;
- (c) the plane and the cube of section 4 on the engine (a 41^3 box, 200
  intervals): the click at 101 and 152 on +x from (40, 40, 20) and (40, 40,
  40); every step's Node within one Link of the line; the drive's fields
  present, no new field;
- (d) the reviewer's pins (1) and (2) of section 4 on the engine against the
  host replay, integer for integer over 1000 and 150 intervals;
- (e) the edges: **p** = 0 never steps and leaves the accumulators; a
  reversal (6000, 0, 0) to (-6000, 0, 0) at n = 30 cancels first (the next
  Link on -x at the n where the signed sum reaches -W); a component of 0
  with a residue neither advances nor steps; the contact pays W and does
  not move the body; the escape clicks with the body's momentum on the face;
- (f) the wall and the accumulator refused by name: a body whose `|p|_1
  T_h` passes the working bound at load; an accumulator that would pass it;
  `drive_b` of a type other than a boolean;
- (g) under `covariant_readings` and the key: the J4 muon's family at `p =
  (2574, 2574, 0)` and (2101, 2101, 2101) admitted at load and at the frame
  (refused without the key, as today: the refusal's text unchanged), the
  wall `Q^2 S M`, the pace per self-creation per axis `p_a / (Q S M)`,
  E' 14671 and 14670 as on the axis (the map's (E)); with `action` the key
  composes as today's rule per stepped axis (one Link turns by
  `by_clock(k0, |p_a| N, h)` with k0 the Links crossed on the axis).

Each fails on `main` (no key, no primitive) and passes on the build.

## 6. What changes in the tree, and what does not

- `src/event_universe/core/integer.py`: `by_line`.
- `src/event_universe/events/measured.py`: the table's method for the three
  `drive` rows through `by_line`; no new row, no new field.
- `src/event_universe/events/world.py`: the key parsed; `drive_wall(momentum,
  content, width, cap)` beside `step_divisor`; `_covariant`'s one-axis
  refusal lifted when the key is declared (its text otherwise unchanged);
  `NatureBeamWorld.drive_b`.
- `src/event_universe/events/engine.py`: `_move`'s branch on the key;
  `covariant_frame`'s one-axis refusal lifted under the key; the `step`
  line unchanged in its fields; `hypotheses` lists `drive-b-v1`.
- `examples/events/drive_b/` (generator, six worlds, `expectations.json`,
  README with the pins and, after the runs, the readings by kind);
  `examples/events/gate_set.json` gains `drive_b/plane_b`; the digests.
- `tests/test_drive_b.py`; `docs/TEST_EXPECTATIONS.md`'s row.
- Documents: BEAM_LAW (one note, the key's rule, beside note 17), ENGINE.md
  (the key, the hypotheses list, `run.json`), HYPOTHESES.md entry 28,
  EXPERIMENTS.md and VALIDATION.md rows, the covariant README's base
  sentence and `_covariant`'s docstring ("until form B lands" becomes
  "unless the world declares `drive_b`"), docs/README.md's index.
- Not changed: the flight, the collision, the meeting, the push, the click,
  every registered world's bytes, the register's digests, MIGRATION (nothing
  moves), the default drive. Not built: form B's line-of-D accumulator
  (M1), the direction read and its grain (S1, S2, S7 closed by removal, FORM.md
  3.1), lorentz-v1, any re-registration of the movers, the covariant
  off-axis worlds (the chief physicist's, record 642 (c)).

## 7. The relation to the rows' triple (`momentum_pair`, the massive rows), the reviewer's M1

Two dispersions are in the tree, both rung 1, and they are NOT one
construction. The rows' triple (`nature_beam.momentum_pair`, optical-v1's
verb 3 of PR #702 and the massive rows' pace) takes the wall `2 T(P) d`
with `T(P) = isqrt(3 |P|^2 Q^2)`, a root of a quadratic form of the state
taken at run time per pushed row, admitted under optical-v1's identity
alone (record 631, S5); its body-side reading is the pace `|p|_2 / E'`
Euclidean with `E' = isqrt(E'_0^2 + 3 p . p)`, isotropic, capped at
`1 / sqrt 3 = 0.5774` on every direction. drive-b's wall is linear in
`|p|_1` with no root (form B's `v = p / (m + p / c)`, DERIVATIONS_BEAM
4.4, the law's letter), capped at `64 / 110 = 0.5818` Euclidean on a
heading and Manhattan-isotropic off it (0.4114 on the plane diagonal,
0.3359 on the cube's). The two agree at Newton's limit (the ratio 0.974 at
`|p|_2 / (Q S M) = 1 / 64`) and at the cap on a heading (0.5818 against
0.5774), and differ between (the map's (G), M = 64, S = 1, HOST): the
Euclidean pace 0.4164 against 0.5372 on the axis at `|p|_1 = 6000` (the
ratio 0.775), 0.2945 against 0.5044 on the plane (0.584), 0.2404 against
0.4769 on the cube (0.504); at `|p|_2 = 6000` on the plane 0.3212 against
0.5372. Under `covariant_readings` and the key together they agree: the cap
off gives `p_a / (Q S M)` per self-creation and the gate's `E'_0 / E'` per
interval makes `|p|_2 / E'` Euclidean on every direction, the triple's pace
exactly (the map's (E): 0.2481 on the axis, the plane and the cube). The
choice this leaves, the body's pace under the law alone (form B's, as the
owner approved, or the rows' triple, which needs the root), is the chief
physicist's and the owner's, not the builder's; this build lands form B
under its key and changes nothing of the triple.

## 8. What stays with the owner and the reviewer

- The cap off the headings is Manhattan-isotropic (`64 / 110` Euclidean on
  every direction), not the flight table's on the body's line: a fast body
  on the cube diagonal is slower than its rows by up to `1 / sqrt 3`
  (FORM.md 3.1 (c)'s stated price). Records 183 and 301 describe the other
  cap; whether their line is superseded by a new one is the owner's word,
  proposed here with the map's (C) as its evidence.
- Whether an axis with a component of 0 and a residue over the wall should
  step (this note: no, note 17's rule) is a choice the reviewer may
  overturn; it changes no pin of section 4.
- The accumulators' bound `W + 2 max_a |p_a| Q` is observed, not proved; the
  build checks every addition against the working bound and refuses by
  name, so the run is exact or refused either way.
