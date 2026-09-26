# The crossing rule: a row and a body meet once, at the crossing of their world lines

The physicist, 2026-09-20, read-only, on main `e8963014` (docs after
`0b45aa53`; `src` unchanged since). Integers only. The offline check of the
rule on the experimenter's streams is `crossing_sim.py` beside this file (no
engine code; the stream of `doppler_test/make_and_run.py`, the rows at
`m(tau) = (2 tau Q + T) // (2 T)`, Q 64, T 110, the reader one Link per k
intervals). The finding it answers: record 151's test
(`doppler_test/REPORT.md`): the reader reads k rows per k intervals in both
senses because the Node reads arrivals only (`nature_beam.py:2741`,
`met = ~own & arrived & (rule != PASS_RULE)`; `arrived` at 2644 from the
walk's mark at 2412) and the step comes after the reading
(`engine.py:383` the law, `engine.py:401` `_move`; the reader placed at
`engine.py:636`, the `step` line at 649).

## 1. The principle

The reading is a crossing of world lines, not an arrival at a Node. A row's
world line is its sequence of Nodes by the flight table; a body's is its
sequence of Nodes by the drive. The two meet where the lines cross, ONCE per
crossing, wherever the crossing falls: at a Node they share, or on a Link
they cross in opposite senses in the same interval.

- A body at rest meets a row when the row arrives at its Node (the rule as
  built, `nature_beam.py:2741`). Nothing changes for a body at rest.
- A body that steps into a Node X from its origin O meets, in the interval
  of the step, the rows resident at X whose motion is toward it (the unit
  vector of their direction against the step, `u . e < 0`): they will not
  arrive at it later (they leave X to O's side while the body is at X), and
  they were not met before (they never passed O while the body was there).
  It also meets the rows that crossed its own Link (O, X) in the opposite
  sense in the same interval (the swap: the row X -> O, the body O -> X;
  they share no Node in any interval, the crossing is on the Link).
- A body that steps does NOT meet the rows resident at X moving with it
  (`u . e > 0`): on the axis they came over the Link (O, X) after being met
  at O, or will be met by nobody twice; and it does not meet again a row it
  met at O that comes over the same Link behind it, in the interval of the
  step (the row and the body arrive at X together from O) or one interval
  later (the row rested at O during the step, then moved): the leapfrog
  re-read of the away sense.

So the readings of a body are: every arrival at its Node that is a first
encounter, plus, in the interval of a step, the rows it meets by the step
itself. The count of a row is one, at its crossing.

## 2. The local criterion

The order of one interval becomes: the frame (`_frame_all`,
`engine.py:382`), then the body's step (`_move`, today at 401, moved before
the law: the body's departure becomes its arrival, as a row's does in the
walk), then the law (`nature_beam`, 383: the walk, the readings, the
collision, the tables, the self-creations, the merge). The reading of the
destination happens in the SAME interval as the step, after it. The body's
step is an arrival mark on its own record, `Measured.step_port` (the Port it
entered through this interval, -1 when it did not step), set by `_move` and
read by step 4 of the law; it is the fact e_step of THIS interval, kept for
one more interval as `Measured.last_step_port` (the previous interval's
step), the same kind of one-interval fact as a row's `arrival` (set at the
walk 2412, cleared at the merge 1230/1236). No memory of past rows exists
anywhere; the two marks are the body's own two last Links, as the drive is
its own distance. (The drive's phase encodes the same fact at a constant
one-signed momentum, `drive < |p|` after a step and `drive < 2 |p|` one
interval later, `by_drive`, `core/integer.py:70`; but not the axis and not
the sign after a reversal or a lost coincident fire, so the mark is the
exact and generic form, and it is what a step IS: a Link crossed.)

The facts a Node X can know at the reading of interval t, all of them on
the records present at X and at its neighbour O through the body's own Port:

- for every row at X: its direction d, its unit vector u_d (`unit`), the
  step it made this interval s_1 = `flight.steps[d, (age - 1) mod L_d]`
  (the walk took `steps[d, age mod L_d]` at 2399 before advancing the age
  at 2498; a zero step is a rest at X this interval, `arrival == NO_ARRIVAL`)
  and the step it made the interval before s_2 = `steps[d, (age - 2) mod
  L_d]`: both off the row's own record and the table, nothing kept;
- for the body at X: e = `PORT_HEADINGS[step_port]` (the signed axis unit
  of its step this interval; 0 without a step), e' the same for
  `last_step_port`;
- for the rows at O = X - e (only when e != 0): their step this interval
  s_1; the Link (O, X) is the body's own transit this interval, and the
  rows that crossed it are the Link's traffic (the walk records it already:
  `crossed_node, crossed_port` at `nature_beam.py:2504-2510`, the per-Port
  flux diagnostic). LOCALITY-1: a Link owns what crossed it this interval;
  the body reads its own Link.

The rule (per row r of another number at a table entry that is not `pass`):

    C1  (the swap)      e != 0, r at O, s_1(r) == -e            -> met
    C2  (the entered)   e != 0, r at X, s_1(r) == 0, u_r . e < 0 -> met
    C2' (with the step) e != 0, r at X, s_1(r) == 0, u_r . e >= 0 -> not met
    C3  (the arrival)   r at X, s_1(r) != 0                       -> met, unless
    C3' (came with the body over its Link) e != 0 and s_1(r) == e  -> not met
    C3'' (the leapfrog after a rest) e == 0, e' != 0, s_1(r) == e',
                                     s_2(r) == 0                   -> not met

C3 with e = 0 and no C3'' is the reading as built. A rest row (direction 0
or 1, u = 0) is met by nobody's step (C2 with u . e = 0: not met), as today.
Own-number rows (home) and the collision are untouched; a body on a set
(`span`) applies the rule per Node of its moved set, e the set's step, O of
each Node its own origin; C1 on the trailing face only (an origin Node not
in the new set), C2 on the entered Nodes (the leading face); an interior
Node reads its arrivals as today.

### The proof on the experimenter's runs

`crossing_sim.py` replays the stream and the rule (the body steps at the
start of the interval of its k-th self-creation; the engine's drive fires at
the same self-creation, `step_axis`, `engine.py:85`, so the ticks of the
`step` lines are the experimenter's, 4, 8, .. and 8, 16, ..). Rows are named
by birth tick as in `REPORT.md`.

Toward, k = 4 (32 intervals): 45 reads = 32 + 13, the windows
[5, 6, 6, 5, 6, 6, 6, 5]; no row twice, none missed (a row behind the reader
at one tick and ahead at a later one is read exactly once). Per step (the
reads the rule adds; every other tick reads its one arrival as today):

| tick | Link | C1 swap on the Link | C2 resident at X, against the step | C3 both arrived at X |
| --- | --- | --- | --- | --- |
| 4 | 40 -> 39 | -64 | - | -63 |
| 8 | 39 -> 38 | -59 | -58 | -57 |
| 12 | 38 -> 37 | -53 | -52 | -51 |
| 16 | 37 -> 36 | -47 | - | -46 |
| 20 | 36 -> 35 | -42 | -41 | -40 |
| 24 | 35 -> 34 | -36 | -35 | -34 |
| 28 | 34 -> 33 | -30 | -29 | -28 |
| 32 | 33 -> 32 | -24 | - | -23 |

The 13 rows the experimenter listed as "on the destination, never read"
(REPORT.md section 3: -63; -58, -57; -52, -51; -46; -41, -40; -35, -34;
-29, -28; -23) are exactly the C2 and C3 columns; the C1 column (-64, -59,
-53, -47, -42, -36, -30, -24) is the row the experimenter's order read at
the origin before the step and the design's order meets on the Link, the
same row once. Toward, k = 8 (48 intervals): 58 = 48 + 10, windows
[9, 10, 10, 9, 10, 10]; the steps read (C1, C2, C3): tick 8 (-60, -, -59),
16 (-51, -50, -49), 24 (-41, -40, -39), 32 (-31, -, -30), 40 (-22, -21,
-20), 48 (-12, -11, -10); the experimenter's ten never-read rows are the C2
and C3 entries.

Away, k = 4: 19 reads in 32 = 32 - 13, windows [3, 2, 2, 2, 3, 2, 2, 3];
no row twice, none missed. What the rule skips, per step:

| tick | Link | C2' resident at X, with the step | C3' came with the body over the Link | C3'' rested at O during the step, arrives one interval later |
| --- | --- | --- | --- | --- |
| 4 | 40 -> 41 | -67 | -66 | -65 (at tick 5) |
| 8 | 41 -> 42 | -65 | -64 | -63 (at 9) |
| 12 | 42 -> 43 | - | -62 | -61 (at 13) |
| 16 | 43 -> 44 | -60 | -59 | - |
| 20 | 44 -> 45 | -58 | -57 | -56 (at 21) |
| 24 | 45 -> 46 | - | -55 | -54 (at 25) |
| 28 | 46 -> 47 | -53 | -52 | - |
| 32 | 47 -> 48 | -51 | -50 | - |

Every skipped row was read before at its first arrival. The experimenter's
re-reads "1 or 2 intervals after the step" (-65 at 3 and 5, -64 at 4 and 6,
...) are these skips seen in the order as built: the design keeps the
`step` line at tick 4 and reads at 41 in the same tick, so the re-read one
interval after the step is C3' (the row came over the Link with the body)
and the re-read two intervals after it is C3'' (the row rested at the
origin during the step). Away, k = 8: 38 in 48 = 48 - 10, windows
[7, 6, 6, 6, 7, 6]; the skips at ticks 8 (-63, -62, -61), 16 (-57, -56,
-55), 24 (-, -50, -49), 32 (-44, -43, -), 40 (-38, -37, -36), 48 (-, -31, -).

The sum over a period (the reader crossing 32 Links = 32 k intervals, the
stream 55 rows per 32 Links exactly, `m(tau + 55) = m(tau) + 32`): toward
183 = 128 + 55 at k = 4 and 311 = 256 + 55 at k = 8, exactly; away 74 and
202 against 128 - 55 = 73 and 256 - 55 = 201, the one extra the row
co-located with the reader at the first interval of the window (a boundary
of the window, not of the rule: over the next window it is not counted
again). Rate: 1 + v / c toward and 1 - v / c away with v = 1 / k and
c = 32 / 55, the pinned k +- 1.72 per k intervals, as a COUNT and not as a
weight. The reader at rest: 48 in 48, byte-identical.

Why each row is read once (a heading stream, the body at |p| <= Q S M, i.e.
at most one Link per two intervals, never two steps in a row: `by_drive`
after a step leaves `drive < |p| <= D - |p|`; a moving row never rests two
intervals in a row on any direction of the table, |v| Q / T_d = 1 / sqrt 3
per interval): let d = (r - R) . u, the row's place relative to the body
along its own motion. Toward: d never decreases (both motions raise it), so
the two share Nodes in one contiguous run entered either by the row's step
(C3, the body at rest that interval), the body's step (C2), both (C3 with
e != 0, s_1 = -e... the row from X - u, the body from X + e: met), or by a
swap without a shared Node (C1); each row once. Away: d changes by -1, 0 or
+1 per interval and gains at least 0 over any two; from d < 0 it reaches 0
only by the row's step onto a resting body (C3: read); after that, d can
only go 0 -> -1 -> 0 by the body's step during a rest of the row and the
row's step the next interval, which is C3'' exactly, or stay 0 by both
stepping together, which is C3' exactly; the chain ends when the row moves
twice in a row and d > 0 for ever. A row ahead of the body (d > 0) that the
body enters (C2', the row came over the body's Link) was met at the origin
by the same argument one Node back, and a row ahead that never shared a
Node with the body never crossed it.

Beyond the axis: a stream on a heading transverse to the step (rows +y, the
body +x) is read at exactly the rest rate (C2 with u . e = 0: the entered
Node's rows are not met, they neither arrived from the origin's side nor
will leave to it; each column's arrivals read as they come), the "exactly 1
for a transverse motion" of note 38. A stream on a face diagonal against
the step (u = (-1, 1, 0) / |.|, the body +x) is read at 1 + rho v with rho
the rows at a Node of the line (T_d / Q = 156 / 64 = 2.44 for one row per
interval per line: 6 or 7 per 4 intervals at k = 4), and one with the step
((1, 1, 0), C2') at exactly the rest rate: the lattice's encounter count on
a fan direction is not the continuum flux of GRAIN.md (1 + 1.22 / k and
1 - 1.22 / k at (-1, 1, 0) and (1, 1, 0)); it is what the GameBoard does,
sign-correct, exact on the axis and on the transverse, and it is a limit to
state, not to tune (the flux weight is deleted, section 4). The alternative
criterion "met unless the row's last Link was the body's Link in the body's
sense" (the row's path in place of u . e) reads the entered Node's rows in
every sense, a sign-blind sweep of +rho v even transverse; it is rejected.
A body faster than one Link per two intervals (|p_a| > Q S M, possible
under pushes, the "outrunning" cases of `test_doppler.py` (b)) can step
twice in a row, and then the one-interval mark cannot tell a leapfrog of lag
two from a first arrival: the rule stays local and generic there but the
one-per-crossing count is not proved; `_move` reports it once per run in
the run's report (`fast_steps`), no refusal.

## 3. The integer form: one place, generic

1. `engine.py:378-401` `step()`: `_frame_all()`, then the `_move` loop
   (today at 401) for every measured event in number order, then
   `nature_beam(...)` (383), then the turns and `_suspend` as today. The
   step uses the momentum after the previous interval's push, the drive
   advanced at this interval's self-creation (`entry.creating` from the
   frame): the same fires at the same self-creations, the body at its
   destination for this interval's reading instead of the next one's. The
   contact (`engine.py:626-631`, `_contact` at 661) and the face click stay
   inside `_move`: a refused step is the body's arrival at the occupant
   (note 31 (ix)), a crossing read at the step already.
2. `Measured` (`measured.py`) gains `step_port: int` and `last_step_port:
   int` (-1 at rest); `_move` sets `last_step_port = step_port` at its
   entry and `step_port` to the Port of the Link crossed at
   `engine.py:636` (or -1: no step, a refused step, an escape); both in
   `state.json` beside `drive` and on the `step` line. `frame_momentum`
   (`engine.py:424`, `measured.py:347`) leaves with the key (section 4).
3. `nature_beam.py` step 4, the one reading: at 2636-2644 add per row
   `s_1 = flight.steps[direction, (age - 1) % period]` and `s_2 = ... (age
   - 2) % period` (vector rows from the table, `int8`, no product), and per
   entry `e = PORT_HEADINGS[entry.step_port]`, `e' = ...last_step_port`;
   at 2741 replace `arrived` in `met` by `crossing`:

       stepped_in = s_1 != 0                              (arrived, as today)
       against    = (u[direction] . e) < 0
       met  = ~own & (rule != PASS_RULE) & (
                (stepped_in & ~(e != 0 & s_1 == e)            # C3, C3'
                            & ~(e == 0 & e' != 0 & s_1 == e' & s_2 == 0))   # C3''
              | (~stepped_in & e != 0 & against))            # C2, C2'

   and add the swap rows C1 to the group of the entry: the rows at O = X - e
   (the origin's flat index, `adjacent_node` through the body's Port) with
   s_1 == -e, gathered with the rows `at` the set (the group of the entry
   is then rows at its Nodes plus rows at its origin Nodes that crossed its
   Links backward: the same `first_reading_overflow` bound at 2652-2658
   over the larger group, fixed work: at most the rows at two Nodes per Node
   of the set). The moments of C1 rows are taken on their arrival vector
   as every arrival's (they arrived, at O). The `read` line at 3278 is
   unchanged in form; its `rows` name the C1 rows with their Node O. The
   detector's threshold, window and click read the same `met`: a
   detector at rest is unchanged; a detector that steps clicks the rows it
   crosses.
4. Nothing else: no key, no weight, no grain, no identity. The rule is a
   rule of the frame's step and the Node's reading, as the contact is. A
   world without a completed step is byte-identical (section 4).

Bounds: the group grows by at most the rows at the origin Node per Node of
the set; the products are the reading's own. Reversibility: the walk and
the collision keep their inverses (`inverse_step`, no measured event); the
reading was the one-way border before and is after.

## 4. The consequences

Registered worlds with moving readers (`examples/events/`, from the
declared momenta and the recorded steps):

- Series G2, `hubble_stars/` (24 free stars at |p| ~ 10^13 on the six
  headings and the twelve face diagonals, `coasting_*`, `double_*`,
  `gravity_*` with `_none`, `_scalar`, `_age`, and the same nine under
  `record/`; the nine under `doppler/` are deleted with the key).
- The hubble worlds `hubble/coasting_age`, `coasting_scalar`,
  `pushing_age`, `pushing_scalar` (24 movers each).
- The deuteron pair and its crowd: `nucleus/deuteron_1_kick`,
  `deuteron_3` (p and n at -+10^12 stepping toward each other, width
  2^28: one Link per ~32 self-creations), `nucleus/pp_3` if a step
  completes; `weak/j3_deuteron`, `j3_deuteron_crowd`, `j3_neutron_free`
  and `binding/deuteron_bond`, `alpha_square_bond`, `alpha_line`,
  `alpha_square`, `deuteron_1`, `pp_1`, `pp_1_weak`, `coupling/1b_m*`
  only where a `step` line exists in the registered run (an adjacent pair
  whose every fire is a refused step is a contact, no Link crossed:
  byte-identical).
- Series D orbits `orbit/s1_r12 .. s32_r24` (the mass at p_y 192 .. 576),
  Bohr's series H `bohr/r2 .. r16` (the electron on a set of 3 with
  `action`), the catalog's `sun_planet` (the planet on a 3 x 3 x 1 set).
- Series K (`lensing/`, `*_meeting.json` under the key `meeting`): the
  beam's paid rows meet the crowd; the mass is fixed: unchanged by this
  rule (section 6).
- I7 (the clock beside the nucleus, `binding/proton_bond_lamp` and the
  nucleus README's I7 line): the lamp and the proton are at rest: unchanged.

What moves in them: the read flux of every mover changes at first order in
v / c at the intervals of its steps only (C1, C2 add rows against its
motion; C2', C3', C3'' remove the re-reads behind it), so its push and its
clock's count (the presence over the same `met`) both change; between
steps nothing changes. Pins that stay to the byte: every world whose
measured events are all `fixed` (the whole of `amplitude/`, `bell/`,
`detector/`, `gate_set.json`'s sixteen but the two with a mover, `hand/`,
`heisenberg/`, `lensing/`, `redshift/`, `buildup/`, `two_slits`, `one_slit`,
`catalog/lamp_mirror_screen`, `neutron_star` (8 free at rest, no step),
`weak/` beta worlds) and every free body that never completes a step
(the adjacent pairs above): their `met` is `arrived` exactly, and the
frame's reorder gives the same self-creations and the same reading order.
The order change alone (the step before the reading) is bit-identical for a
body at rest and changes a mover's world line by nothing (the same Link at
the same self-creation), only the interval in which its destination is
read.

The third-law pair: record 143's gap (+270 720 on B1's x, 6 x 3008 x 15
pushes: the held paid content that counts in M_A and is never released) is
a gap of the reader's content, not of the reading, and stays as it is; the
pair's exchanges change only at completed steps, where the stepping body
now reads the partner's rows on its Link (toward: more; away: fewer) with
no counterpart on the partner in that interval: the pair's momentum sum
moves by the rows read at the step times the push per row, first order in
v / c, sign toward the partner when closing, away when opening. B1, B2, B3
re-pin where a step completes; an adjacent pair that only contacts keeps
its integers.

G2 without the key: 1 + z = (1 + k)(1 + v / c) (`hubble_stars/README.md`
"The redshift"), k the star's owed count per self-creation, v its speed at
emission. Two terms move: (i) the push a receding star takes from the
centre's rows, which come from behind on its axis, falls by v / c (the
leapfrog re-reads gone), so the deceleration is smaller and v at emission
higher: z HIGHER, the sign of record 138 under the key ("every star's
redshift higher, every momentum spared"), with the fan rows of the crowd
adding the entered-Node term of section 2 (against the motion only); (ii)
the clock's count, which the key never touched, now counts the same
crossings: a receding star's presence falls by v / c of its axis rows, k
falls, z LOWER by k v / c / (1 + k). In the `_none` worlds only (i): z up;
in `_scalar` and `_age` the sign is that of (1 + k) Delta v / c against
k v / c on the star's own numbers, to pin by the G2 session before the run
from its registered k and v per star; the expectation of q moves toward
the key's +0.345 from the source rule's +0.922 in `_none`, the clock
worlds are new expectations.

The deletion list of doppler-v1 (record 151: "in both cases the key leaves
the code"): the world key `doppler` (`world.py:444` `DOPPLER_KEY`, 443
`DOPPLER_RULE`, 1013 the field, 1096 the identity under `hypotheses`,
2930-2932 the parse, 2961 the budget's factor and `weighted_flow_factor`
458), `SPEED_GRAIN` (`world.py:351`), `quantised_speed`
(`nature_beam.py:2038`), `flux_pair` (2061), `weighted_flow` (2090),
`speed_bound_error` (2026), the guard at 3227 (`if world.doppler and free
and not entry.fixed`) with `frame_momentum` (`engine.py:424` the docstring,
`_frame_all`'s line, `measured.py:347`), `run.py:109-111` (`doppler` in
`run.json`), the doppler row of the counts table (record 150, the
fraction-free branch), the nine worlds `hubble_stars/doppler/*.json` with
their `expectations.json` and the `doppler/` prefix of
`tools/hubble_stars_readings.py` (238-281, 533 `doppler_part` stays as the
reading's Doppler part of the fit, a name of nature, not of the code;
720, 921) and `tests/test_hubble_stars_readings.py:182-204`, the
`test_doppler.py` row of TEST_EXPECTATIONS.md (46, 1664-1778), note 38's
paragraphs and the step-4 pointer to it (BEAM_LAW.md 447-451), ENGINE's
mention, MIGRATION gains the entry. What each test of `test_doppler.py`
becomes under the crossing rule:

- (a) a fixed body and a free body at rest byte-identical with and without
  the key -> (5b): a reader at rest byte-identical before and after the
  rule (the same records, the same books).
- (b) the bar: 200 rows read in every case, the push weighted 12800 / 6204
  / 2901 / 19395 -> the COUNT itself: at rest 200; receding at 0.30
  (v / c = 0.30 x 55 / 32 = 0.516) 97 +- 1; receding at 0.45 (0.773) 45 +-
  1; approaching at 0.30 303 +- 1 (the map's exact rates 96.9, 45.3, 303.1
  emerge as counts, the push 64 x the count exactly, no floor); the
  co-moving at c and the outrunning at 0.75 are beyond the proved regime
  (|p| > Q S M): run and recorded, not pinned as law.
- (c) the third law on two fixed bodies unchanged -> unchanged (no step).
- (d) the refusals and the budget -> deleted with the key; the reading's
  own bound covers the larger group (a test that the swap rows are inside
  `first_reading_overflow`).
- (e) the grain, the pair and the record -> deleted.
- (f) the fan over three intervals (the flux weights 0.594, 0.777, 0.867)
  -> (5c) the diagonal and transverse streams as counts.
- (g) a body on a set reads every group from the one frame snapshot ->
  a body on a set reads C1 on its trailing face and C2 on its leading face
  once per step, each row once over the set.
- (h) a registered G2 star world runs under the key -> the star world
  runs without it and its stars step with the crossing reads (20 intervals
  balanced).

## 5. The tests for the implementer, integers pinned before the run

(a) The experimenter's five worlds (`doppler_test/out/*.json`, the key
absent) under the rule: `toward_k4` 45 reads in 32 intervals, windows
[5, 6, 6, 5, 6, 6, 6, 5], the added rows per step the table of section 2;
`toward_k8` 58 in 48, [9, 10, 10, 9, 10, 10]; `away_k4` 19 in 32,
[3, 2, 2, 2, 3, 2, 2, 3]; `away_k8` 38 in 48, [7, 6, 6, 6, 7, 6]; `rest` 48
in 48; every `read` line's `amount` 1, 2 or 3; no birth tick read twice in
any run (the trace of `make_and_run.py`); the books balanced; the momentum
constant to the unit. The comparison pair: `toward_k4_probe_off` reads 45
rows and pushes 64 x 45 = -2880 on x in all (against -2048 today and the
key's -2928 = 5.72 rows-equivalent per window); `toward_k4_probe_on` is
refused at parsing ("unknown key doppler").
(b) A reader at rest unchanged: the control above and the gate set of
sixteen byte-identical in `events.jsonl` and `state.json` but for its
worlds with a completed step, named by their `step` lines.
(c) A diagonal stream: the experimenter's bar turned to the face diagonal,
one row per interval on (1, 1, 0) from a lamp at (0, 0, 0) on a GameBoard
[64, 64, 1], the stream pre-filled (the row of age tau at (m'(tau),
m'(tau), 0), m' with T = 156), the reader at (40, 40, 0) stepping +x at
k = 4 for 32 intervals: 32 reads in 32 (the rest rate, C2' skips the
entered Node's rows: 2 or 3 at every step, listed); the same with the
stream on (-1, 1, 0) from (63, 0, 0) and the reader stepping +x: 32 + the
rows at the entered Nodes (2 or 3 each, 19 or 20 in 8 steps, T_d / Q =
2.4375 per Link on average) reads; a transverse heading stream (one lamp
per column, rows +y, the reader +x at k = 4): 32 in 32 exactly. No row
twice in any of the three.
(d) One row met once when the reader steps into it, and once only when it
catches the reader up: worlds with ONE row in transit on +x, age 0, and a
reader of the experimenter's content at k = 4 (the row's Node at tick t is
x_0 + m(t), m(0 .. 13) = 0, 1, 1, 2, 2, 3, 3, 4, 5, 5, 6, 6, 7, 8):
  - toward: the row at x_0 = 30, the reader at 40 stepping -x (39, 38, 37
    after ticks 4, 8, 12): at tick 12 the row moves 36 -> 37 and the reader
    enters 37 from 38: C3 with both arrived, ONE `read` line, tick 12,
    `amount` 1; at tick 13 the row moves on to 38 (nothing);
  - away, the leapfrog after a rest (C3''): the row at x_0 = 30, the reader
    at 32 stepping +x (33 after tick 4): tick 3 the row arrives at 32, the
    reader at rest: `read` at tick 3; tick 4 the reader steps 32 -> 33 while
    the row rests at 32; tick 5 the row moves 32 -> 33 into the reader's
    Node, e' = +x from 32 and s_2 = 0: NOT met; tick 8 the reader steps
    33 -> 34 as the row moves 34 -> 35: nothing. Exactly one `read` line,
    tick 3;
  - away, the entered Node with the step (C2'): the row at x_0 = 31, the
    same reader: tick 1 the row arrives at 32: `read` at tick 1; tick 3 it
    moves to 33; tick 4 the reader enters 33 while the row rests there,
    u . e > 0: NOT met; exactly one `read` line, tick 1.
  Each world: the `read` lines of the row's number count 1; the books
  balanced.
(e) The sum over a period: the reader crossing 32 Links on a GameBoard
[512, 1, 1] with the stream pre-filled over its length, 32 k intervals:
toward 128 + 55 = 183 reads at k = 4 and 256 + 55 = 311 at k = 8, exactly;
away 128 - 55 + b and 256 - 55 + b with b in {0, 1} the boundary row of
the first interval, stated by the trace.

## 6. The contact rule and the meeting

The contact (`engine.py:626-631`, `_contact` 661; note 31 (ix)) already
reads at the crossing: a body whose Link is blocked at its far end by an
occupant has arrived at the occupant in the interval of its fire, once per
fire, and the hand-over is taken there; nothing is read at an arrival
later, so the crossing principle holds for it as built, and the reorder of
section 3 leaves it inside the step. The meeting (`meeting-v1`,
`meeting.py:282` `meet`, `crowd_flow` 244; note 35) is not a crossing count
by design: a paid row reads, at every free-space Node it occupies after the
collision, the flow of every free row present there this interval, resident
or arrived (`store.node[rows]` at 304-311, no arrival mark), and turns by
it; a free row co-moving with the paid row is read at every interval they
share, a dwell reading, the design's phase delay by the crowd (M-R: "a
report, not a balance"). It reads at co-location, not at the arrival only,
so it has neither the miss nor the leapfrog of the body's reading; whether a
co-moving crowd should turn a ray less (the crossing count would say so)
is series K's question, not this rule's, and nothing of it changes here.

## Verdict

A row and a body meet once, at the crossing of their world lines: the body
reads every first arrival at its Node, and in the interval of a step, the
rows on its Link against it and the rows at the entered Node against it,
never the rows that came over its Link behind it, in that interval or the
next after a rest. Admissible: local (the body's own two last Links and the
rows' own last two steps off the flight table, nothing kept at a Node),
generic (every body, every family, every set, the same `met`), bounded (the
reading's own bound over at most one more Node per Node of the set),
reversible where the law was (the walk and the collision untouched; the
reading the one-way border as before); exact on the axis and transverse,
a sign-correct encounter count on a fan direction, one row per crossing for
a body at most one Link per two intervals.

> The scripts of this folder (`crossing_2d.py`, `crossing_sim.py`) were deleted on 2026-09-26 (the model owner's word, record 2229: code not in use goes); git history keeps them at `6d2a92e2` (`git checkout 6d2a92e2 -- docs/designs/crossing/<script>`).
