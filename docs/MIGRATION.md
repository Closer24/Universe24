# API and repository migration

Install from the extracted project first:

```bash
python -m pip install -e '.[render,dev]'
```

## The host's batches and memos, on 2026-09-21 (host only, bit-exact)

The model owner's order of 2026-09-21 ("optimization and simplify"), part
(b): the runner profiled on the gate set's worlds (`cProfile`, the time by
function), then the measured hot spots of the host made to compute the same
integers once. No rule, no register, no run moved: the gate set's digests
read as before (`tests/test_amplitude_click.py` (d)); the expected results
are in `tests/test_host_batches.py`.

- The store's rows born in an interval were appended one call per
  measured event and family, each call a copy of the whole store (the cost
  of a run quadratic in the rows: on `heisenberg/w27_beam` at 40
  intervals the appends were 46 s of 111 s under the profiler). Step 5
  collects the born rows per family in the order of the measured events
  and the families and appends them once (`NatureBeamStore.extend`, one
  concatenation per field; `append` is `extend` of one batch): the same
  rows in the same order.
- A body's charges (`Measured.charges`, the exact rational sum over what
  it holds per column, reduced) were computed at every read: by the frame
  once per interval and by the books once per interval per body (on
  `weak/j3_deuteron` at 700 intervals, 1.45 million computations, 14 s of
  83 s under the profiler over four worlds). The last result is kept on
  the body with its inputs (what is held, the units per paid family) and
  returned again while they are the same: the same pairs, computed once
  per change.
- The world's `handed` (a scan of every family, transit row and measured
  event) is a cached property of the frozen world, read once.

Candidates measured and not changed here: `_measured_arrays` (the measured
events' tables rebuilt as arrays every interval, 8 s of 83), the
snapshot's rows materialized one object per row (`NatureBeamStore.rows`,
`record_line`; 23 s at the end of `w27_beam` at 40 intervals), the per-row
Python loop over a body's pending rows in `_release_family`, the JSON
encoding of the record (`run.record`, 6 s of 83; its bytes are pinned by
the digests).

## The interval in named steps, on 2026-09-21 (host only, bit-exact)

The model owner's order of 2026-09-21 ("optimization and simplify"). The
interval `nature_beam` was one function of 2,091 lines; it is now the
orchestrator of its six steps, each a function of the same module called
by `nature_beam` alone, every line of the law's text moved and not
changed: `interval_frame` reads the frame `Interval` once (the world's
constants, the measured events in number order with the index of the one
at each Node, the crossing marks of note 48); `_walk` (step 1),
`_collide` (step 3, the closure `collide` before), `_measure` (step 4:
`_measured_arrays` reads `MeasuredArrays`, the measured events' tables in
array form; `_family_plan` the closure `family_plan` before; `_apply_plans`
and `_apply_plan` the record loop per measured event and family;
`_refuse` the closure `refuse`); `_release` (step 5) with
`_release_family` per family; `_border` (step 6); `_merge`;
`_inverse_interval` the inverse branch. `heading_port` is a module
function. The unused read of the world's `release` pair at step 5 is
deleted (the release is the counts table's row since the fraction-free
law). No rule, no register, no run moved: the gate set's digests
(`tests/test_amplitude_click.py` (d)), the worlds, the bijection, the
books and the detectors read as before. References by the old names
(`family_plan`, `collide`) in the documentation are renamed; a dated log
record keeps its wording.

## The paper-writer skill folded into paper-coordinator, on 2026-09-21 (docs only)

`skills/paper-writer/SKILL.md` (the manuscript's method: equations first,
one source per number, the four labels, the referee round before any
material enters) is deleted; its content is the method section of
[skills/paper-coordinator/SKILL.md](../skills/paper-coordinator/SKILL.md),
the one skill of the role (the model owner, record 309), and the Boss's
routing table carries paper-coordinator alone. The manuscript's own plan
(`paper/general_formula/PLAN.md`) keeps the rounds' history under the old
name where it was written.

## The one count primitive in its array form, on 2026-09-21 (host only, bit-exact, no law change)

The model owner's word on the flight's accumulator (record 299: "yes,
with this it is beautiful and generic"): the same verb, the Euclidean
division with the remainder kept, was written twice, as
`core.integer.by_drive` on a body's record and as the flight's own array
expression on the rows. One implementation of the law's count, in two
forms.

- `events.nature_beam.by_drive_rows(drive, rate, denominator, at_most)`:
  `by_drive` over numpy int64 rows, the same integers row by row (signed
  rates, the cap, the remainder kept; a denominator below 1 refused, the
  accumulator plus the rate bounded to the working register before the
  sum is formed). It lives beside `by_clock_rows`, the array form of the
  other count, since `core/` stays standard-library integers.
- `Flight.walk_step` takes the interval's step as the count
  `by_drive_rows` gains at the row's residue over the wall; the residue
  and the step are the verb's two outputs. `Flight.accumulator` is
  unchanged in form and named as the verb's constant-rate identity
  (the pair off the age, tau applications from T_d).
- Bit-exact: the gate set's state, books and events digests unchanged
  (`tests/test_amplitude_click.py` (d)); `tests/test_nature_beam_flight.py`
  (g) the walk on every direction of the register's fans over a full
  period against the closed form and the verb iterated;
  `tests/test_fraction_free.py` (j) the array form against `by_drive` on
  a grid of 111 996 cases with the named edges.
- BEAM_LAW note 41 (viii) and TERMINOLOGY's "Flight table" line say so.

## The quark families defined once, on 2026-09-21 (host only, no law change)

The families `u` (`quantum` 0, `charge` 1224, `phase` false) and `glue`
(`quantum` 0, `columns` `{"strong": {"value": 10000, "sign": -1}}`,
`lifetime` 3, `phase` false) that the seven worlds of series R declare
([the quarks](../examples/events/quarks/README.md), the design
[QUARKS.md](designs/quarks/QUARKS.md)) are defined once in
`examples/events/entities/families.json` (written by `make_definitions.py`:
the definitions `up_quark` and `glue_family`, the rows of
[the catalog](ENTITY_CATALOG.md#the-family-names-of-the-register)), so
that `tests/test_entity_definitions.py` (v2-f), every family of the
register defined once, holds again on main after the series' registration
(PR #463). The worlds keep their families inline as before, and the two
whose keys differ stay so (the down quark `d` shares its name with the
detector material's `d`, whose definition `detector_material_d` stays; the
dressed world's `glue` is at the pair `[10000, 606]`); no world file and
no law changed.

## The crossing rule, on 2026-09-21: the step before the law, a row and a body met once, the key `doppler` and the grain deleted

The model owner's record 158 of 2026-09-20 ("the step reads the crossed
Link") on the experimenter's finding of record 151; the physicist's design
[docs/designs/crossing/DESIGN.md](designs/crossing/DESIGN.md); the branch
`crossing`; [BEAM_LAW note 48](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation).
The identity `beam-v1` is kept.

- The order of the interval: the frame, the measured events' steps
  (`_move`), the law, the clocks' turn and count (until then the frame,
  the law, the turn and count, the steps). The step at a self-creation
  advances the drive by the momentum after the previous interval's push;
  under a suspension the step no longer waits for the interval that pays
  the count owed (`_move` runs at every self-creation, before this
  interval's owed count: a timing of the step changed, stated in note 48
  and in note 17; `test_push_width` (c)'s steps 18, 36, 54
  became 17, 35, 53); a contact, a give and an escape happen before the
  law. What moves: a
  fire under a push falls one interval later than it did (the contact
  pairs, the binding worlds, a body pushed by a click), a given row makes
  its first Link in the interval of the give, the rows released in the
  interval of a step carry the phase turned at the Link (`action`), a
  body escaping in the interval of its self-creation carries the phase
  before that interval's clock turn, and a body reads its own rows home
  at its destination in the interval of the step. At a constant momentum
  the Links fall at the same self-creations.
- `Measured.step_port` and `last_step_port` (the body's own two last
  Links, -1 without) in `state.json` beside `drive` and on the `step`
  line (`step_port`, `last_step_port`): `state.json` of every world with
  a measured event gains the two keys; a test-level resume restores them.
- The reading (step 4): `met` is the crossing (C1 the swap on the body's
  Link, C2 the entered Node's residents against the step, C3 the
  arrivals, with the exclusions C2', C3' and C3''); a met row is read on
  its own direction; the presence stays the rows at the set plus the
  swap rows. A body at rest and a fixed body read as before, to the byte.
- Deleted: the world key `doppler` (`DOPPLER_KEY`, `DOPPLER_RULE`
  `doppler-v1`, `NatureBeamWorld.doppler`, the parse, the identity under
  `hypotheses`, `run.json`'s `doppler`; a world that declares the key is
  refused, "unknown keys: doppler"), the grain G (`world.SPEED_GRAIN`),
  `nature_beam.quantised_speed`, `flux_pair`, `weighted_flow`,
  `flux_bound_error`, `speed_bound_error`, `world.weighted_flow_factor`
  and `_column_budget`'s factor, `Measured.frame_momentum`, the `flow`
  rows of `counts_table` (its `directions` argument) and
  `Measured.acc_flow` (`acc.flow` in the record), the nine worlds
  `examples/events/hubble_stars/doppler/*.json` with `expectations.json`
  (the third run's readings stay as history in EXPERIMENTS, VALIDATION
  and the series README), `make_worlds.py --doppler`, `doppler_worlds`
  and `quantised`, `tools/hubble_stars_readings.py`'s `under_doppler` and
  `doppler/` prefix, `tests/test_doppler.py` (its (a) and (c) live on as
  `test_crossing` (b) and the contact tests, its (b), (f), (g), (h) as
  counts in `test_crossing` (a) and (c) and in the G2 session's run; (d)
  and (e) went with the key), BEAM_LAW note 38 (a tombstone stays),
  ENGINE's paragraph on the key and TEST_EXPECTATIONS' section.
- Re-pinned under the order (the old integers kept as history in each
  test's docstring): `test_contact` (a) and (d), `test_nucleus_readings`,
  `test_binding` (a), (b), (c), (d), (f), `test_paid_charge` (d),
  `test_nature_beam_body` (a) and (d), `test_nature_beam_reemission` (b)
  (the escaping body's phase before its interval's clock turn),
  `test_push_width` (c) (the step at the self-creation under a
  suspension), `test_orbit_readings` (c) (a probe that crosses the stream;
  the one on +y from (7, 4, 0) met nothing under the rule) and the gate
  set's digests of every lamp-free world (`gate_set.json`: the state's for
  the two marks, the events' and the books' where a body stepped or fired
  under a push). `run.json` gains `fast_steps`, the Links crossed right
  after another of the same body (the rule's count not proved there, note
  48: a report). The registered worlds with a
  completed step or a fire under a push move (VALIDATION, the dated
  table of this change): series G2 (the run under the rule is the G2
  session's), the hubble worlds, D, H, the catalog's `sun_planet`, the
  nucleus, binding and weak pairs; every world whose measured events are
  all fixed reads the same records, and its `state.json` differs by the
  two marks alone.

## The weak register re-pinned under the fraction-free law, on 2026-09-21 (host only, no law change)

The architect's root cause (record 254) of the J1 `become` counts: the
fraction-free law's batch (241fc7ac, PR #412) re-read the runs of series
J in the weak README and left `examples/events/weak/expectations.json`'s
`become` entries as the first registration's warm run had written them
(the first commit whose warm run differs is e7ba13c6, the owed count on
its accumulator, BEAM_LAW note 41; a law reviewed and decided, records
148 and 174). The re-pin is its owed consequence; no rule changes.

- `examples/events/weak/make_worlds.py`: `count_ranges` in place of
  `steady_counts`: the warm run is `WARM_TICKS` = 120 intervals and the
  count of each neutron's clock is pinned as its range over the dwell
  period `DWELL` = (61, 120) (the lesson of the first registration: the
  count a clock reads under a fan's dwells is not one number over its
  history); the register's `become` entries carry `counts` and `ticks` as
  pairs [lo, hi], `earliest`, `latest`, `slack`, `dwell` and `warm_ticks`,
  and `derivations.become` states the dwell period and the range's source.
- `tools/weak_readings.py`: `tick_range`; the trigger criterion reads a
  pinned tick as a range [lo, hi] or as one integer (lo = hi), inside when
  the neutron fires within it or up to `slack` intervals before.
- `tests/test_weak_readings.py` (e): the generator's warm run on the
  shipped J1 and J3 worlds against the register entry by entry;
  `tools/check.py` names the test as the consumer of the weak generator
  and register.
- The old integers are history in `examples/events/weak/README.md`
  ("Re-pinned under the fraction-free law"); the rule's sentence in
  `docs/TEST_EXPECTATIONS.md` (a law change re-registers every register
  its runs feed, every generator has its comparing test).

## The readings by type and the registers' derivations, on 2026-09-21 (host only, no law change)

The owner's two principles of the experiments (record 205: "a formula
gives, a run proves"; "after the detector, name the vector to read"),
built as documentation and register annotation; no run moved, every
registered number unchanged.

- `docs/ENGINE.md` gains the table "The detector's readings by type":
  every quantity the record exposes, by type (scalar, vector, tensor,
  pair) with its line or field, its unit and its kind (detector or
  GameBoard); `docs/EXPERIMENTS.md` points to it from the two kinds of
  readings. The coherent pointer (X, Y) was already on the `record` line;
  nothing new is exposed.
- Every register (`examples/events/expectations.json`, `bell/`,
  `amplitude/`, `hubble_stars/` and its `record/` and `doppler/`,
  `weak/`) gains a `derivations` map, one entry per key: the formula or
  the section of `docs/DERIVATIONS_BEAM.md`, or `measured` with the
  target. The generators (`amplitude/make_worlds.py`,
  `hubble_stars/make_worlds.py`, `weak/make_worlds.py`) write it; the
  amplitude generator also reproduces the register split's hand-added
  entries (`REGISTERED_RUN_READINGS`), so the shipped file equals the
  generator's again. The rule is in `docs/TEST_EXPECTATIONS.md` beside the
  register rule.
- Three tests derive and compare where a closed form exists:
  `tests/test_nature_beam_worlds.py` (b) the Bell plus offset (the first
  birth's tick plus the flight table's age at 8 Links),
  `tests/test_hubble_stars_readings.py` (a) the star worlds' c (Q / T_D
  off the flight table) and the new `tests/test_weak_readings.py` (d),
  the register of series J2 from the five shipped worlds, the flight table
  and `window_admits`.
- `docs/THREE_WORLDS.md`'s software column corrected against `main`
  (`Moments` for `Reading`, `execute_nature_beam_run` for `execute_run`,
  `core/game_board.py` for a `GameBoard` class, the `hand` column int64,
  the flight table for an accumulator, the `Split` row for a fan's
  weights, the Count rows for `acc_turn` and `acc_owed`, `met` marked as
  not on `main`, `apply_gate` and `rotate_rows` named) with the modules
  added; the rows of the reading, the click and the record point to the
  readings table.

## The group structure named, on 2026-09-21 (host only, no law change)

The architect's item 3 of the proposal on the runs (record 203; the vector
program, record 191, "everything represented in vectors and matrices, from
group theory"): the three group objects of the law named and typed, bit-exact
under the gate set; BEAM_LAW note 42. No rule changed; every registered
integer the same.

- `core.game_board.cube_symmetries()`: the cube's group of 48 (the signed
  axis permutations as images of the six Ports), with `IDENTITY_SYMMETRY`,
  `compose_symmetries`, `inverse_symmetry` and `symmetry_hand` (+1 a
  rotation, -1 a reflection). The collision test's local `cube_group()`
  is deleted; it enumerated the same 48 maps.
- `core.phase.PhaseCircle` and `phase_circle(N)`: the world's circle of N
  steps as the cyclic group of the phase (`turn`, `difference`,
  `opposite`, `mask`, `half`) with its unit vectors (`vector`, the tables'
  (C, S)) and the tables themselves (`cosines`, `sines`). The engine's
  tables carry it (`NatureBeamTables.circle`, a new field; `cosines` and
  `sines` stay as arrays), the engine's two scalar turns read it
  (`circle.turn` in place of `& phase_mask`, the same integers for N a
  power of two), and the layer holds it (`Layer.circle`, with `steps`,
  `cosines` and `sines` as before).
- `nature_beam.CollisionTable` gains `orbit` (the class index per code)
  and `period` (the class's size per code) and the method `act(code,
  backward)`, the shift the engine's collision step calls; `forward`,
  `inverse`, `singles` and `powers` are unchanged.
- `tests/test_nature_beam_collision.py` (b) states the orbits as
  properties (the orbit-stabilizer and Burnside counts) in place of the
  counted sizes; `tests/test_group_structure.py` is new (the group, the
  circle, the action). TERMINOLOGY gains the cube group, the phase circle
  and the collision action; ARCHITECTURE's and the README's rows for
  `core/game_board` and `core/phase` name them.

## The trimming's part 2, the register split, on 2026-09-21 (host only, no law change)

The Boss's decision under the owner's rule (records 169 and 184 of
2026-09-20 and 2026-09-21; the architect's audit item 10): a test reads a
world's numbers from the register. Every number a test pinned of a shipped
world (a world file of `examples/events/` or one its generator writes)
moved to the register beside the world, one source per number, and the
test asserts equality with the value read from there; no test body holds
a literal of a world's number. The gate set stays the replay mechanism;
the numbers themselves are unchanged (bit-exact: no run moved).

- `examples/events/gate_set.json`: each lamp-free world carries `digests`
  (`state_sha256`, `audit_sha256`, `events_sha256` at its cap), the table
  `PINNED_DIGESTS` of `tests/test_amplitude_click.py` (d), deleted there.
- `examples/events/bell/expectations.json` (new, `bell-expectations-v1`):
  the ten A2 worlds read by `tools/bell_chsh.py` under the one click (the
  criteria, the count failed, the tick offsets, the CHSH sum, the primed
  sum, three correlations), the literals of
  `tests/test_nature_beam_worlds.py` (b).
- `examples/events/expectations.json` (new,
  `root-worlds-expectations-v1`): `two_contents`'s face records at its
  20th interval, the literals of `tests/test_nature_beam_worlds.py` (e).
- `examples/events/amplitude/expectations.json`: under `mach_zehnder` the
  gathers' last tick and the totals' spread, `mz_equal`'s `birth`,
  `split` and `first_gather`, `mz_balanced`'s `split`, `mz_345`'s
  `pythagorean_5`, the two splits' tick of `mz_quarter` and
  `mz_unequal_f8`; under `two_slits` the last gather's tick, the face
  gathers and the first gather; under `pair` the `birth`, the
  `choosers_early` records and `far_min_flight`; under `gate` the
  `rotate_line`, the `gate_line`, the `pair_rows`, `twice` (an object now:
  `identity`, `later_gates`, `rows`; it was `true`), the `ghz_gate_line`
  and the `rotation_multiplicity`. The literals of
  `tests/test_amplitude_split.py`, `test_amplitude_layer.py`,
  `test_amplitude_pair.py` and `test_amplitude_gate.py` read there; a
  register value restated as a literal beside its read (the CHSH sum 176,
  the sums 88, 2896 and 11584, the correlations 724 and 2900, the total
  847181/745472, the clicks by kind) is dropped, the read alone remaining.
- `tests/test_amplitude_cone.py`: the register's pins (the Links, the age
  at the click, the path phases) are derived from the two worlds and the
  flight table and compared, the literals gone.
- `tests/test_hubble_stars_readings.py`: the literal ranges on the
  registered fits (0.85 .. 0.87, 0.24 .. 0.25) are the register's own
  `q_bracket` of each run.
- Left, with the reason: a test's own minimal world keeps its expected
  integers in the test (the owner's rule of 2026-09-17): the two-slit
  world `tests/test_nature_beam_worlds.py` (a) builds, the Bell choosers'
  fixed-phase case of `tests/test_bell_choosers.py`, the K record world of
  `tests/test_amplitude_click.py` (f) (the registered `lensing/mass_meeting`
  altered by the test: the lamp's turns 0, every pixel reading `sum`, 300
  intervals) and the bars of the twelve `*_readings` modules, which read
  no shipped world. Whether those reproduce a known experiment is the
  owner's question (the audit's item 10, Q5), untouched.
- `tools/check.py`'s resource map names the registers' readers.
## The architecture audit's three items, on 2026-09-21 (host only, no law change)

The architect's audit of genericity and locality (the model owner's request
of 2026-09-21; the Boss's assignment of its three host-only items as one
pull request), bit-exact by construction: no physical function changed.

- `NatureBeamSimulation.shell_readings` (the shell means of the readings,
  the one floating-point calculation of the package) is moved out of the
  engine class to `diagnostics/shell_readings.py`: `simulation.shell_readings(
  family, centre, radius)` -> `shell_readings(simulation, family, centre,
  radius)` from `event_universe.diagnostics.shell_readings`, the same
  dictionary. Its readers moved: `tests/test_nature_beam_worlds.py` (c) and
  `tools/coupling_readings.py`. `cube_flux` (integers) stays on the engine.
- The static numeric audit covers both physical layers
  (`diagnostics.numeric_audit.audit_physical_modules`): `core/` by
  `static_integer_audit` as before (integers only, no numeric library) and
  `events/` by the new `static_events_audit` (integer numpy permitted;
  refused: a float or complex literal, true division, a float dtype or
  constant, `sqrt`, the means, the transcendental functions and the modules
  `cmath`, `decimal`, `fractions`, `random`, `scipy`). `events/run.py`, the
  artifacts' writer (path joins with `/`, no physics), is outside it as the
  import gate exempts it. `tests/test_architecture.py` asserts both layers
  audited and clean; SIMULATOR_DEFINITIONS' gate line says what each audit
  checks. `tools/check.py` selects `test_architecture.py` for every change
  under `src/`, as before.
- `tests/test_locality.py` runs the six-read test (LOCALITY-1's executable
  form, gone since the scalar candidate's deletion on 2026-09-17): on a bar
  of 13 x 1 x 1, rows placed beyond one Link of a Node change nothing of
  its interval (its rows, its readings, the collision there, the click and
  the push at a detector), and a change at k Links reaches a Node no sooner
  than the flight's first arrival (1, 3, 5 intervals for k = 1, 2, 3). The
  layer of `amplitude-v1` is outside the claim (the one non-local operation
  the model owner decided, records 72 and 74 of 2026-09-20).

## No registers at Nodes, no tables, on 2026-09-20: the last counts join the table, the flight as the position's accumulator, no remainder discarded

The model owner's record 155 of 2026-09-20 ("go for it: no registers at
Nodes, no tables") on the fraction-free law below; the branch
`no-tables`. The identity `beam-v1` is kept.

- The turn by momentum under `action` ([BEAM_LAW note 30 (ii)](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation),
  note 41 (i)) is the `action` row of the body's table of counts, per
  axis: the row gains |p_a| x N at every Link the step rule counts on the
  axis and the whole part over h turns the phase at the Link crossed (a
  count at a Link lost or refused is discarded, as before); the same
  integers as `by_clock(k0, |p| N, h)` at a constant momentum, the exact
  sum where the momentum changes along the path. `run.json` and
  `state.json` carry `acc.action` (three integers) on a turning body.
  Series H re-read: the register's dated line. The parser's bound on
  `ticks x |p| x N` stays as declared; at run time only |p| N is formed.
- The flight table is retired: `nature_beam.Flight` (was `FlightTable`;
  `direction_flight(vectors)` was `flight_table`) keeps the direction
  set's constants (v, S_1, T_d, the direction's line, the period L_d, the
  labels) and the Link a ray crosses at an age is `Flight.walk_step`, the
  position's accumulator on the row written out (the accumulator starts at
  T_d, gains 2 S_1 Q per interval over 2 T_d; the count m(tau) picks the
  unit step of the line): a ray's rate never changes over its flight, so
  the accumulator and the count are read off the age and the row carries
  no new field. The per-direction step table over the period and the age
  read modulo the period are gone; `period` stays as the fact the readers
  use for c. Bit-identical on every registered world (the gate set
  replayed: 17 of 17 identical, VALIDATION). The name "flight table" is
  retired in the code and in BEAM_LAW, ENGINE and TERMINOLOGY ("the flight
  rule"); the readings tools and the generators import `direction_flight`.
- No remainder discarded at run time (record 155 (3); [BEAM_LAW note
  41 (viii)](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)):
  `nature_beam.share_of` keeps a record row's undelivered push on the row
  (the store columns `share_x`, `share_y`, `share_z`, 0 on every row that
  never pushed, summed at a merge, written to `state.json` as `share` on
  a row that holds one), so a row read at every interval of a passage
  pushes the exact sum and the books' `remainder` line reads only what
  left with absorbed rows; a set's release over its Nodes is placed by the
  Nodes' claims, the `place` rows of the body's table of counts
  (`nature_beam.place_over_nodes`, `acc.place` in the record), every Node
  within one unit of its equal share of all the body has released, in
  place of the leftover to the Node `age mod w` reset at every row. The
  other two uses of `apportion_whole` (a re-release over the admitted
  directions, the contact's hand-over over the occupants) are exact within
  their event and keep their declared tie rule. The candidate worlds
  replayed in one batch (VALIDATION, the register's dated lines): of the
  95 (the 48 of L, the 9 of K, the 7 of H, the 4 of the catalog, the 27
  of G2) only the set worlds moved, series H and the catalog's
  `sun_planet` (`clock_near_mass` in its `state.json` alone, the `place`
  claims of a body that releases nothing); every world whose record rows
  are read on their way (K under the record click, the which-path worlds
  of L, G2's age worlds) is identical, a row being read once or twice
  before it leaves, fewer times than its remainder needs to make a unit;
  record 144's cone and every fan world are identical (the flight's form
  above checked on them too). Note 41 (viii) lists every remaining `//` of
  the law's runtime with its class, and the inventory's findings 7 to 10
  left as built.
- The register's pins are detector readings; the tools label every host
  reading of the GameBoard (the shell readings, the cube flux, the probes'
  counts) GAMEBOARD (record 163 (2)): the heads of EXPERIMENTS and of
  `examples/events/README.md`, `tools/coupling_readings.py`,
  `tools/redshift_readings.py`.

## The birth wheel at a declared rate, on 2026-09-21: `wheel` [r, W] required on every lamp

The model owner's decision, record 180 of 2026-09-20's log (on record 163
(3)); the mathematician's [TWO_SLITS.md section 8](designs/fraction_free/TWO_SLITS.md);
[BEAM_LAW note 46](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation).
The identity `beam-v1` is kept.

- Every lamp declares `wheel` [r, W] (`LampDefinition.wheel`, required, no
  default): one `Count` row `wheel` of the lamp's counts table
  (`Measured.lamp_wheel`, `counts_table(lamp_wheel=...)`), advanced at every
  birth; u = ordinal x r mod W is the record's coordinate on the ladder,
  whose rungs are on W (`LiveRecord.wheel`, `Layer.birth(..., wheel)`,
  `Layer.complete`). `state.json` and `run.json` carry the row under `acc`
  as `wheel` on lamps. `nature_beam.birth_coordinate` is new.
- Every registered lamp declares [1, N] (the count of births mod N as
  built): the world files regenerated by their generators, the entity
  definitions (`entities/apparatus.json`), the hand-written `masses`
  worlds and the tests' lamps; their events are byte-identical, their
  `state.json` gains the accumulator. A rebirth at a re-emitter that is no
  lamp keeps u = its count mod N and the rungs on N.
- `slits_huygens` (L2b) declares the golden rate [2531, 4096] and runs to
  4096 births; re-registered as the run that shows the wheel (its entry in
  `examples/events/amplitude/README.md` and EXPERIMENTS).
- `tools/amplitude_path.py` reads a record's wheel from the world's lamp
  (`wheel_of`); `Layer.birth` takes the wheel as its last argument.


## The exact phase at the click, on 2026-09-21: the phase read at the exact time of the row's last Link

The model owner's decision, record 163 (2) of 2026-09-20's log; the
mathematician's [TWO_SLITS.md section 2](designs/fraction_free/TWO_SLITS.md);
[BEAM_LAW note 45](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation).
The identity `beam-v1` is kept; the pins that moved were re-registered once.

- A record's row ends (a click, a `sum` re-emitter, a face, the border) at
  the phase of the exact time of its last Link, `nature_beam.exact_phase`,
  from its phase per interval (the pair form) and the Links the flight
  table counts; the click line of every row of a family with the pair form
  carries `exact` and `remainder` (new keys; the row's `phase` unchanged).
  `FamilyPlan.t_exact` is new.
- `slits_low` (L2) re-registered: the 64 clicks stay wall 34 (11, 12, 11),
  screen 15, faces 15 (8, 7); the fifteen screen clicks land at y = 11, 29,
  36, 40, 50, 56, 59, 60 (twice), 61, 70, 77, 84, 90, 107 in place of 11,
  29, 36, 43, 50, 56, 59, 60, 61 (twice), 70, 77, 82, 90, 107; the reading's
  total 4834019/4259840 in place of 847181/745472, the shares 0.529 / 0.244
  / 0.227 in place of 0.528 / 0.244 / 0.228, the weights' Pearson with the
  cosine 0.382 in place of 0.368 and the histogram's 0.722 in place of
  0.655 (`expectations.json` under `two_slits`, regenerated; the reference
  world `slits_one` now declares the frequency and the reading takes each
  row's `exact`). The design's map expected wall 34, screen 16, faces 14
  (note 45 says why the engine differs).
- The Mach-Zehnder worlds (L1) keep every click; the unequal arms' weights
  and totals moved. The cone worlds (L7) keep their pins; `expectations.json`
  under `cone` gains `exact`. Bell, GHZ and the gate are bit-identical.


## The click without amplitudes, on 2026-09-21: the layer keeps phase-count vectors

The model owner's decision, record 188 of 2026-09-20's log; the derivation
mathematician's proof (DERIVATIONS_BEAM.md section 6.7);
[BEAM_LAW note 37 (xii)](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation).
The identity `beam-v1` is kept: the same integers on every registered cell.

- `events.amplitude.Offer.pointers` (the complex pointer per Node and
  label) is `Offer.counts`, the phase-count vector **f** per Node and label
  (`Counts`, a sparse map from the phase step to the count at the amplitude
  scale 32); `Offer.residuals` holds vectors of the same kind per channel in
  place of complex residuals. The pointer is a report, `Layer.evaluate(f)`
  (the `record` line's `pointer`, `run.json`'s open records), and the click's
  weight is `Layer.gram_form(f)`, the bilinear form with the Gram matrix of
  the tables (`core.phase.phase_gram`, new; `GRAM_STORED_STEPS` its storage
  bound), for one arm; for several arms the pointers' product as before.
- `events.amplitude.cadd` is deleted (the counts add, `add_counts`);
  `Layer.rotation` returns per channel (a scalar, a shift) in place of a
  complex entry; `ring_product`, `add_count`, `add_counts`, `scale_counts`
  and `Layer.arm_element` are new. `cmul` stays as the several-arm
  factorisation's product.
- The turn of a rotation's bit 1 is a shift of the phases: the same integers
  as the former product of table entries at a turn that is a multiple of
  N / 4 (every registered turn), one rounding in place of two at any other
  turn (`tests/test_amplitude_gram.py` (d)); no registered pin moves.

## The fraction-free law, on 2026-09-20: every count an accumulator on the body's record

The model owner's records 147 and 148 of 2026-09-20 on the mathematician's
read-only [FORM.md](designs/fraction_free/FORM.md) and the physics-rule
reviewer's read-only [REVIEW_COUNTS.md](designs/fraction_free/REVIEW_COUNTS.md);
[BEAM_LAW note 41](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation).
The identity `beam-v1` is kept: an integer form of the same counts, one
primitive in place of two.

- `core.integer.by_drive` is the count of every count of a body: the owed
  count (`engine.count_owed`), the free release per family, a lamp's rate,
  the turn, the push per column and axis, the doppler weight per direction
  and axis, and the step's drive as built. Each is one bounded integer on
  the body's record, `Measured.acc_owed`, `acc_release`, `acc_lamp`,
  `acc_turn`, `acc_push`, `acc_flow` and `drive`, gaining the count's rate
  at the self-creation and keeping the remainder below the denominator:
  the remainder owner the local integer operation contract asks for.
  `by_clock` stays in `core.integer` as the constant-rate identity of a
  count (from an empty accumulator at age 0 the two give the same integers,
  `tests/test_fraction_free.py` (a)) and for the reads of an age against a
  key (`nature_beam.ages_at_key`: the lifetime, the age bound, the clock
  trigger); the turn by momentum under `action` (note 30) still reads
  `by_clock(k0, |p| N, h)` off the Links stepped, named in note 41 as the
  one count of a changing rate left as built.
- Why the count moves where the rate changes (the reviewer, record 148):
  the whole part off the clock at the current rate re-prices the whole
  age at today's rate; a paid lamp pays at every birth, so its turn's rate
  falls, and a clock on a fan reads a crowd that changes at every
  interval, so on the register every lamp world and every crowd world
  moves, and the accumulator's count is the law's under E = h f (the
  integral of the rate). FORM.md's "the constant-rate worlds are
  bit-identical" describes the primitive, not the register's worlds.
- The push per column is counted over the column's one denominator
  Lambda_c^2 (`NatureBeamWorld.column_scales`, the least common multiple
  of the families' value denominators in the column); Lambda is 1 on
  gravity and on charge wherever the charges are whole, so no registered
  push moves at this stage (the nine gate worlds' audit and events
  unchanged); the lifted product is tested by division and refused naming
  the column where it does not fit (`tests/test_columns.py` (a)); since
  the physics-rule review of the branch (`docs/designs/fraction_free/REVIEW.md`,
  section 4) a column whose Lambda_c^2 leaves the register (Lambda_c
  above 2^31 - 1) is refused at load naming the column and the bound
  (`tests/test_fraction_free.py` (g)), where before it loaded and was
  refused at its first push; no registered world reaches it (every
  Lambda_c is 1 or a few tens). Under
  `doppler` the weighted flow is counted per direction at G Q |v_d|^2.
- The counts are ONE table on the body's record (the model owner's table
  of 2026-09-20): `Measured.counts`, a `CountTable` of `Count` rows built
  by `measured.counts_table` from the world's rates (per row the name, the
  numerator's source, the index and axis, the rate's factor, the
  denominator, the cap `at_most`, 1 on the drive, and the accumulator),
  and one loop, `CountTable.advance`, runs the rows of a count through
  `by_drive` and hands the whole parts to the count's consumer at the
  stage where its numerator exists (the frame, `_suspend`, step 5,
  `_move`, the reading); `Measured.acc_owed`, `acc_release`, `acc_lamp`,
  `acc_turn`, `acc_push`, `acc_flow` and `drive` read and write that
  table, and `engine.step_axis` and `engine.count_owed` remain as the
  readings tools' forms of the same rule. Bit-identical to the law before
  the table on every test and on the gate set (the digests of the
  register replay above unchanged).
- `run.json` and `state.json` carry the accumulators per measured event
  under `acc` by name (`owed`, `release`, `lamp`, `turn`, `push` per
  column, `flow` under the key), beside `drive`; a declared `acc` in a
  world file is refused as an unknown key; a run resumed from a state is
  the unbroken run (`tests/test_fraction_free.py` (c)). Every digest of a
  `state.json` moves for the new field.
- The readers by record. A paid lamp's exact clock stalls where its
  content has fallen below K (the Bell lamps of content K + 2, paying 2
  per birth, once at tick 4; the L worlds' lamps of 2^20 at tick 2 and its pair lamps at tick 3), so the tick of a
  birth is not the age of the lamp's clock: the `pass` line carries
  `record` and `u` as the `click` line does; `tools/bell_chsh.py` and
  `tools/bell_choosers.py` pair a row by its record (the age its birth
  ordinal less one) and report the tick offsets as the flight's, the
  smallest tick - age at each Node; `tests/test_amplitude_pair.py`,
  `tests/test_amplitude_layer.py` and `tests/test_hand.py` take a lamp's
  first 64 records by ordinal. Every correlation is alignment-independent
  (S = 176/64 and 156/64, the cells, the ports, the GHZ triples read by
  ordinal on both counts). A lamp keeps one birth per interval over T
  intervals with the content K + c (T - 1) or more, c its cost per birth.
- The ladder at the click is spelled as the comparison of products
  (`amplitude.cell_of`: the first k with 2 T u + T <= 2 N C_k), the same
  integers as the rungs' cell, the rungs a report (`tests/test_fraction_free.py` (f)).
- The register, re-registered once in one batch on the head of the branch
  against the base a2120413's tree (the scratchpad driver: every world run
  with `--wall-seconds 1200 --memory-mb 4096`, one run per worker at a
  time, its digests and counts kept; `heisenberg/w27_beam` skipped as
  ordered, and `heisenberg/w27_wave`, `buildup/w27_rate1`, `w27_rate47`,
  `w27_rate8` not compared: beyond the wall on both trees): what moved and
  by how much, the old integers kept as history in the READMEs and the
  dated lines of EXPERIMENTS; nothing tuned.

| world | what moved | births | waits | steps | clicks | ages |
| --- | --- | --- | --- | --- | --- | --- |
| `amplitude/bell_0_24.json` | events, books | 80 -> 79 | 0 | 0 | 286 -> 282 | same |
| `amplitude/bell_0_8.json` | events, books | 80 -> 79 | 0 | 0 | 286 -> 282 | same |
| `amplitude/bell_16_24.json` | events, books | 80 -> 79 | 0 | 0 | 286 -> 282 | same |
| `amplitude/bell_16_24_far.json` | events, books | 300 -> 299 | 0 | 0 | 768 -> 764 | same |
| `amplitude/bell_16_8.json` | events, books | 80 -> 79 | 0 | 0 | 286 -> 282 | same |
| `amplitude/bell_choosers.json` | events, books | 1000 -> 999 | 0 | 0 | 5894 -> 5890 | same |
| `amplitude/bell_n1024_0_128.json` | events, books | 1044 -> 1043 | 0 | 0 | 4142 -> 4138 | same |
| `amplitude/bell_n1024_0_384.json` | events, books | 1044 -> 1043 | 0 | 0 | 4142 -> 4138 | same |
| `amplitude/bell_n1024_256_128.json` | events, books | 1044 -> 1043 | 0 | 0 | 4142 -> 4138 | same |
| `amplitude/bell_n1024_256_384.json` | events, books | 1044 -> 1043 | 0 | 0 | 4142 -> 4138 | same |
| `amplitude/bell_n4096_0_1536.json` | events, books | 4113 | 0 | 0 | 16418 | same |
| `amplitude/bell_n4096_0_512.json` | events, books | 4113 | 0 | 0 | 16418 | same |
| `amplitude/bell_n4096_1024_1536.json` | events, books | 4113 | 0 | 0 | 16418 | same |
| `amplitude/bell_n4096_1024_512.json` | events, books | 4113 | 0 | 0 | 16418 | same |
| `amplitude/cnot_ghz_xxx.json` | events, books | 270 -> 267 | 0 | 0 | 484 -> 478 | same |
| `amplitude/cnot_ghz_xyy.json` | events, books | 270 -> 267 | 0 | 0 | 484 -> 478 | same |
| `amplitude/cnot_ghz_yxy.json` | events, books | 270 -> 267 | 0 | 0 | 484 -> 478 | same |
| `amplitude/cnot_ghz_yyx.json` | events, books | 270 -> 267 | 0 | 0 | 484 -> 478 | same |
| `amplitude/cnot_pair_0_24.json` | events, books | 180 -> 178 | 0 | 0 | 300 -> 296 | same |
| `amplitude/cnot_pair_0_8.json` | events, books | 180 -> 178 | 0 | 0 | 300 -> 296 | same |
| `amplitude/cnot_pair_16_24.json` | events, books | 180 -> 178 | 0 | 0 | 300 -> 296 | same |
| `amplitude/cnot_pair_16_8.json` | events, books | 180 -> 178 | 0 | 0 | 300 -> 296 | same |
| `amplitude/cnot_twice.json` | events, books | 180 -> 178 | 0 | 0 | 284 -> 280 | same |
| `amplitude/cone_intervals.json` | events, books | 192 -> 190 | 0 | 0 | 134 -> 132 | same |
| `amplitude/cone_links.json` | events, books | 192 -> 190 | 0 | 0 | 134 -> 132 | same |
| `amplitude/ev_169.json` | events, books | 80 -> 79 | 0 | 0 | 213 -> 210 | same |
| `amplitude/ev_29.json` | events, books | 80 -> 79 | 0 | 0 | 213 -> 210 | same |
| `amplitude/ghz_xxx.json` | events, books | 80 -> 79 | 0 | 0 | 450 -> 444 | same |
| `amplitude/ghz_xyy.json` | events, books | 80 -> 79 | 0 | 0 | 450 -> 444 | same |
| `amplitude/ghz_yxy.json` | events, books | 80 -> 79 | 0 | 0 | 450 -> 444 | same |
| `amplitude/ghz_yyx.json` | events, books | 80 -> 79 | 0 | 0 | 450 -> 444 | same |
| `amplitude/ghz_yyy.json` | events, books | 80 -> 79 | 0 | 0 | 450 -> 444 | same |
| `amplitude/mz_345.json` | events, books | 80 -> 79 | 0 | 0 | 138 -> 136 | same |
| `amplitude/mz_balanced.json` | events, books | 80 -> 79 | 0 | 0 | 69 -> 68 | same |
| `amplitude/mz_equal.json` | events, books | 80 -> 79 | 0 | 0 | 138 -> 136 | same |
| `amplitude/mz_half.json` | events, books | 80 -> 79 | 0 | 0 | 138 -> 136 | same |
| `amplitude/mz_quarter.json` | events, books | 80 -> 79 | 0 | 0 | 276 -> 272 | same |
| `amplitude/mz_unequal_f0.json` | events, books | 80 -> 79 | 0 | 0 | 280 -> 276 | same |
| `amplitude/mz_unequal_f16.json` | events, books | 80 -> 79 | 0 | 0 | 280 -> 276 | same |
| `amplitude/mz_unequal_f8.json` | events, books | 80 -> 79 | 0 | 0 | 280 -> 276 | same |
| `amplitude/path_0_24.json` | events, books | 80 -> 79 | 0 | 0 | 286 -> 282 | same |
| `amplitude/path_0_8.json` | events, books | 80 -> 79 | 0 | 0 | 286 -> 282 | same |
| `amplitude/path_16_24.json` | events, books | 80 -> 79 | 0 | 0 | 286 -> 282 | same |
| `amplitude/path_16_24_far.json` | events, books | 300 -> 299 | 0 | 0 | 768 -> 764 | same |
| `amplitude/path_16_8.json` | events, books | 80 -> 79 | 0 | 0 | 286 -> 282 | same |
| `amplitude/rotations_3.json` | events, books | 110 -> 109 | 0 | 0 | 196 -> 194 | same |
| `amplitude/slits_low.json` | events, books | 230 -> 229 | 0 | 0 | 22302 -> 22117 | same |
| `bell/a0_b0.json` | events, books | 160 -> 159 | 0 | 0 | 294 -> 292 | same |
| `bell/a0_b12.json` | events, books | 160 -> 159 | 0 | 0 | 294 -> 292 | same |
| `bell/a0_b16.json` | events, books | 160 -> 159 | 0 | 0 | 294 -> 292 | same |
| `bell/a0_b24.json` | events, books | 160 -> 159 | 0 | 0 | 292 -> 290 | same |
| `bell/a0_b32.json` | events, books | 160 -> 159 | 0 | 0 | 292 -> 290 | same |
| `bell/a0_b8.json` | events, books | 160 -> 159 | 0 | 0 | 294 -> 292 | same |
| `bell/a16_b24.json` | events, books | 160 -> 159 | 0 | 0 | 292 -> 290 | same |
| `bell/a16_b8.json` | events, books | 160 -> 159 | 0 | 0 | 294 -> 292 | same |
| `bell/a4_b12.json` | events, books | 160 -> 159 | 0 | 0 | 294 -> 292 | same |
| `bell/a4_b8.json` | events, books | 160 -> 159 | 0 | 0 | 294 -> 292 | same |
| `bell/fixed.json` | events, books | 148 -> 147 | 0 | 0 | 503 -> 501 | same |
| `bell/one_clock.json` | events, books | 1940 -> 1939 | 0 | 0 | 7671 -> 7669 | same |
| `bell/read.json` | events, books | 1940 -> 1939 | 0 | 0 | 7669 -> 7667 | same |
| `bell/written_a0_b29.json` | events, books | 141 -> 140 | 0 | 0 | 474 -> 472 | same |
| `bell/written_a0_b8.json` | events, books | 141 -> 140 | 0 | 0 | 475 -> 473 | same |
| `bell/written_a25_b29.json` | events, books | 141 -> 140 | 0 | 0 | 469 -> 467 | same |
| `bell/written_a25_b8.json` | events, books | 141 -> 140 | 0 | 0 | 470 -> 468 | same |
| `binding/proton_bond_lamp.json` | events, books | 3000 | 0 | 0 | 1735769 | same |
| `catalog/lamp_mirror_screen.json` | events, books | 104 | 0 | 0 | 636 -> 668 | same |
| `catalog/neutron_star.json` | events, books | 0 | 109 -> 97 | 176 -> 186 | 684 -> 708 | 14 of 14 bodies, by -1 to 1 |
| `catalog/sun_planet.json` | events, books | 50 | 0 | 10 | 209 | same |
| `hubble/pushing_age.json` | events, books | 0 | 145 -> 146 | 1429 -> 1426 | 8351 -> 8358 | 25 of 31 bodies, by -3 to 3 |
| `hubble/pushing_scalar.json` | events, books | 0 | 639 -> 617 | 1408 -> 1411 | 8200 -> 8204 | 24 of 31 bodies, by -4 to 8 |
| `hubble_stars/coasting_age.json` | events, books | 9538 -> 9521 | 62 -> 55 | 1521 -> 1525 | 15389 -> 15405 | 18 of 25 bodies, by -2 to 4 |
| `hubble_stars/coasting_none.json` | events, books | 9600 -> 9576 | 0 | 1536 | 15483 -> 15459 | same |
| `hubble_stars/coasting_scalar.json` | events, books | 9517 -> 9504 | 97 -> 90 | 1524 -> 1523 | 15355 | 22 of 25 bodies, by -4 to 6 |
| `hubble_stars/doppler/coasting_age.json` | events, books | 9538 -> 9521 | 62 -> 55 | 1521 -> 1525 | 15389 -> 15405 | 18 of 25 bodies, by -2 to 4 |
| `hubble_stars/doppler/coasting_none.json` | events, books | 9600 -> 9576 | 0 | 1536 | 15483 -> 15459 | same |
| `hubble_stars/doppler/coasting_scalar.json` | events, books | 9517 -> 9504 | 97 -> 90 | 1524 -> 1523 | 15355 | 22 of 25 bodies, by -4 to 6 |
| `hubble_stars/doppler/double_age.json` | events, books | 9485 -> 9464 | 115 -> 112 | 1281 -> 1277 | 15248 | 17 of 25 bodies, by -3 to 5 |
| `hubble_stars/doppler/double_none.json` | events, books | 9600 -> 9576 | 0 | 1296 | 15388 -> 15364 | same |
| `hubble_stars/doppler/double_scalar.json` | events, books | 9435 -> 9410 | 200 -> 195 | 1281 | 15141 -> 15138 | 19 of 25 bodies, by -4 to 7 |
| `hubble_stars/doppler/gravity_age.json` | events, books | 9558 -> 9523 | 42 -> 53 | 1420 -> 1418 | 15377 -> 15347 | 19 of 25 bodies, by -2 to 3 |
| `hubble_stars/doppler/gravity_none.json` | events, books | 9600 -> 9576 | 0 | 1426 | 15419 -> 15395 | same |
| `hubble_stars/doppler/gravity_scalar.json` | events, books | 9526 -> 9504 | 94 -> 90 | 1415 | 15316 -> 15303 | 20 of 25 bodies, by -3 to 2 |
| `hubble_stars/double_age.json` | events, books | 9474 -> 9469 | 126 -> 107 | 1070 -> 1069 | 15276 -> 15256 | 18 of 25 bodies, by -3 to 6 |
| `hubble_stars/double_none.json` | events, books | 9600 -> 9576 | 0 | 1082 | 15387 -> 15362 | same |
| `hubble_stars/double_scalar.json` | events, books | 9449 -> 9408 | 179 -> 197 | 1072 -> 1070 | 15156 -> 15144 | 18 of 25 bodies, by -3 to 3 |
| `hubble_stars/gravity_age.json` | events, books | 9534 -> 9525 | 66 -> 51 | 1310 -> 1314 | 15345 -> 15339 | 15 of 25 bodies, by -2 to 5 |
| `hubble_stars/gravity_none.json` | events, books | 9600 -> 9576 | 0 | 1319 | 15403 -> 15379 | same |
| `hubble_stars/gravity_scalar.json` | events, books | 9512 -> 9504 | 107 -> 90 | 1311 -> 1312 | 15295 -> 15284 | 22 of 25 bodies, by -1 to 4 |
| `hubble_stars/record/coasting_age.json` | events, books | 9538 -> 9521 | 62 -> 55 | 1521 -> 1525 | 15389 -> 15405 | 18 of 25 bodies, by -2 to 4 |
| `hubble_stars/record/coasting_none.json` | events, books | 9600 -> 9576 | 0 | 1536 | 15483 -> 15459 | same |
| `hubble_stars/record/coasting_scalar.json` | events, books | 9517 -> 9504 | 97 -> 90 | 1524 -> 1523 | 15355 | 22 of 25 bodies, by -4 to 6 |
| `hubble_stars/record/double_age.json` | events, books | 9474 -> 9469 | 126 -> 107 | 1070 -> 1069 | 15276 -> 15256 | 18 of 25 bodies, by -3 to 6 |
| `hubble_stars/record/double_none.json` | events, books | 9600 -> 9576 | 0 | 1082 | 15387 -> 15362 | same |
| `hubble_stars/record/double_scalar.json` | events, books | 9449 -> 9408 | 179 -> 197 | 1072 -> 1070 | 15156 -> 15144 | 18 of 25 bodies, by -3 to 3 |
| `hubble_stars/record/gravity_age.json` | events, books | 9534 -> 9525 | 66 -> 51 | 1310 -> 1314 | 15345 -> 15339 | 15 of 25 bodies, by -2 to 5 |
| `hubble_stars/record/gravity_none.json` | events, books | 9600 -> 9576 | 0 | 1319 | 15403 -> 15379 | same |
| `hubble_stars/record/gravity_scalar.json` | events, books | 9512 -> 9504 | 107 -> 90 | 1311 -> 1312 | 15295 -> 15284 | 22 of 25 bodies, by -1 to 4 |
| `masses/cavity_equal.json` | events, books | 1200 | 0 | 0 | 1176 | same |
| `masses/cavity_unequal.json` | events, books | 12000 | 0 | 0 | 11976 | same |
| `weak/j1_lattice.json` | events, books | 0 | 1592 -> 1536 | 0 | 231224 -> 231008 | 56 of 4234 bodies, by 1 to 1 |
| `weak/j1_source.json` | events, books | 0 | 2848 -> 2708 | 0 | 405620 -> 406292 | 220 of 4235 bodies, by -2 to 4 |
| `weak/j3_deuteron.json` | events, books | 0 | 1110 -> 1149 | 62 -> 64 | 707078 -> 718743 | 115 of 764 bodies, by -2 to 11 |
| `weak/j3_deuteron_crowd.json` | events, books | 0 | 1111 -> 1149 | 66 -> 69 | 705380 -> 718741 | 115 of 764 bodies, by -2 to 12 |

- The re-pinned tests, the old integers kept as history in each module's
  docstring: TEST_EXPECTATIONS "The fraction-free counts".
- Nothing deleted: `by_clock`, `by_clock_rows` and every key stay.

## The series the one click re-pinned reference the family definitions, on 2026-09-20 (host only, no law change)

The third pull request of the model owner's decision of 2026-09-20
(record 113; the built form in
[entity definitions](ENTITY_DEFINITIONS.md#families-in-definitions-event-entities-v2-2026-09-20)),
after the one click of `amplitude-v1` landed (PR #395):

- The amplitude series (44 of 47 worlds), the lensing series (9), the
  build-up series (3), `catalog/sun_planet`, `catalog/lamp_mirror_screen`,
  `two_slits` and `heisenberg/w3_beam` reference
  `../entities/families.json` (the root world `entities/families.json`),
  written by their generators through `families_by_definition`; the two
  inline exceptions of the root and Heisenberg generators are gone.
  `amplitude/slits_low` keeps `light` inline (its `phase_per_link` a pair,
  the definition's an integer), `amplitude/mz_unequal_f8` and
  `mz_unequal_f16` stay inline whole for the same reason.
- Every migrated world's expanded document equals its former inline
  document and its `events.jsonl`, `state.json` and books are identical
  (the 62 worlds in scope replayed on `main` at e4b649a0 and on the branch,
  the long ones capped at 200 intervals, `two_slits`, the build-up and the
  N = 4096 Bell worlds at 40).
- No world of the register declares `families` for a family the
  definitions define; the catalog's rows are unchanged.
- Nothing deleted.

## The binding that costs content, on 2026-09-20 (`binding-v1`, no key)
## The architecture cleanup, phase 2: removals after the one click, on 2026-09-20 (host only, no law change)

The architect's phase 2 ([the plan](designs/architecture_2026-09-20/PLAN_PHASE2.md),
the Boss's assignment under record 137), bit-exact on the gate set against
`main` at e4b649a0 (the one click merged). Deleted, each with its reader
moved or gone:

- `tools/migrate_nature_beam_worlds.py` (242 lines): the rewrite of the
  first NatureBeam worlds to the form of 2026-09-20; no world declares
  `"law": "rays"` or a family `kind`. The parser's refusal of `"law":
  "rays"` still names the tool, in git before e4b649a0. Its row in the
  README's tool table removed; the catalog README's sentence dated.
- `nature_beam.pointer_units` and `POINTER_UNIT`: the `wave` threshold on
  the pointer's square, deleted at the one click; no caller was left. The
  assertions of `tests/test_nature_beam_detector.py` (i) and (j) on them
  removed; the one integer kept as `26 x (32 x 256)^2`.
- `amplitude.isqrt` (Newton's integer square root): `math.isqrt`, the
  same integers.
- `Layer.origin` (an identity function with one caller, which now reads
  the row's record) and the alias `measured.Pending` (no reader).
- `AMPLITUDE_SCALE` defined once (`events/amplitude`, imported by
  `events/nature_beam`); `amplitude.IDENTITY` renamed `ROTATION_IDENTITY`
  (the rotation's 256^2; `nature_beam.IDENTITY` is the 3 x 3 identity).
- Renamed for what they are: `nature_beam.AMPLITUDE_DEFAULTS` ->
  `NO_RECORD_COLUMNS`; `world._amplitude_load_checks` ->
  `_record_load_checks`; `DetectorSet.wave` -> `DetectorSet.pointer`
  (true for `wave` and `sum`, the readings of the crowd's pointer) with
  `st_wave` -> `st_pointer` and `wave_rows` -> `pointer_rows` in
  `nature_beam`; the books' local `amplitude` -> `recorded`. Twenty-four
  comments and docstrings naming the deleted world key as live now say a
  record's row, a recorded world or a row of no record.
- `NatureBeamSimulation.layer` is typed `Layer` (always built);
  `run.json`'s `world`, `open` and `layer` are written for a recorded
  world (`world.recorded`), the layer guard being dead. The `layer:
  Layer | None` of `nature_beam` and `rotate_rows` and their guards stay:
  the engine's inverse pass (`nature_beam(..., inverse=True)`, the check
  of the bijective steps) runs without a layer.
- ARCHITECTURE's dependency table gains the rows `events/amplitude` and
  `events/meeting` and names them in `events/nature_beam`'s and
  `events/engine`'s; TERMINOLOGY's record, branch, multiplicity, layer
  and click's-Node entries, the amplitude README and the catalog's photon
  row no longer say "under the key".
- Kept, with the reason in the plan: the raw-document lamp scan at parse
  (its place gives the lamp's refusal precedence over the measured
  events'); `world.event_charges` (the import direction: `events/measured`
  imports `events/world`); the two derivations scripts and the four
  world-pinning tests (the owner's and the test owner's call, Q5);
  `amplitude/expectations.json` beside its worlds; the optimizations
  (O1 to O4) and the unifications (U2, U3, U5) of phase 1, not removals.


binding-v1 (2026-09-20): at a contact under `measure` the refused body gives
its held paid content to the flight on the reversed heading; `contact`
records gain `given`; `run.json` carries `binding-v1` when a body holds a
paid family; no registered world changes by a byte. The model owner's
records 115 and 137 of [the log](LOG_2026-09-20.md), the physicist's design
`docs/designs/binding_v1/DESIGN.md` (record 132),
[BEAM_LAW note 40](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation),
`engine._give`, `world.BINDING_RULE` and `NatureBeamWorld.binding`,
`tests/test_binding.py`; the worlds of series N under
`examples/events/binding/` ([the register](EXPERIMENTS.md#n-the-binding-that-costs-content-2026-09-20)).
The `given` key is written on `contact` records from the moment the run
holds the fact (`NatureBeamSimulation.binding`: at load when a body holds a
paid family other than its own, the parser's `binding`; else from the first
give on), and `run.json`'s `hypotheses` carries `binding-v1` from the same
fact (`NatureBeamSimulation.hypotheses`): a body that takes paid content
under the keys' `measure` gives it at its next contact, and the record and
the identity follow that run-time fact. Every world in which no body holds
or takes paid content is unchanged; a paid body's own content is never
given.

## The hand, on 2026-09-20 (`hand-v1`)

The model owner's decision of 2026-09-20 (record 128 of
[the log](LOG_2026-09-20.md), "the hand's three choices confirmed"; the
physicist's design hand/DESIGN.md, record 122, with the mathematician's
integer form, record 120; [BEAM_LAW note 39](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation);
`tests/test_hand.py`; the worlds of series P, `examples/events/hand/`):

- The row's column `hand` (-1, 0, +1; 0 everywhere without a declaration),
  the helicity relative to the row's direction, a pseudoscalar under the
  48 symmetries, carried unchanged through every re-creation (a mirror, a
  split, a rotation, a gate, a meeting, a collision, a home, the inverse
  interval) and an identity field of the merge (opposite hands never merge
  or cancel). `NatureBeam.hand`, `PendingRow.hand`, the store's field
  `hand`, `BornRow`'s ninth entry.
- The keys `hand` on a family (the catalog's home of the hand, as `charge`
  is), on a lamp (circular light), on a transit row and on a table entry
  (the parity filter, refused on `pass`), a third entry per branch of a
  lamp's `branches` (the hand as a label bit's meaning, one or the other
  per family; on such a family the parity filter reads the label's hand,
  `nature_beam.read_hands`, the which-path click on the label) and
  `axis` on a measured event (one of the six headings as
  a vector). `FamilyDefinition.hand`, `LampDefinition.hand` and
  `label_hands`, `TransitDefinition.hand`, `MeasuredDefinition.axis` and
  `hands`, `Measured.axis`, `hands`, `lamp_hand`, `lamp_label_hands`.
- The right-hand rule in `become` (`nature_beam`, step 5; `world.axis_sign`):
  a product's hand is its family's; at a parent with an axis a handed
  product leaves only on the directions with sign(A . u_d) = h (a
  left-handed product against the axis), an unhanded product is stamped
  the sign of its direction; an empty set refused at load
  (`world._handed_products`).
- The record: `hand` on the `click`, `pass`, `read`, `rerelease`, face and
  border lines, a fifth entry on the `become` line's products, `left` and
  `right` per family in the books (`Ledger.taken_left`, `taken_right`),
  `hand` per family and `axis` per number in `run.json`, `hand` on the
  rows of `state.json`, all only in a world that declares a hand or an
  axis (`NatureBeamWorld.handed`); the identity `hand-v1` under
  `hypotheses`, last.
- `_table_entry` returns a sixth value, the hand the entry admits;
  `_branches` returns the branches and the label hands; `_lamp` takes
  `family_hand`; `NatureBeam.record_line` takes `handed`.
- Every world without a hand byte-identical: the gate set replayed
  identical ([VALIDATION](VALIDATION.md)); `hand/wu.json` added to the
  gate set as the first world declaring the keys. Nothing deleted.

## The reading's weight at the relative speed, on 2026-09-20 (`doppler-v1`, a world key, absent by default)

The model owner's decision of 2026-09-20 (record 119 of
[the log](LOG_2026-09-20.md): "a body TAKES a message at the rate at which
it and the message meet"; the mathematician's admissible form, FORM.md
section 6 of `docs/designs/push_relative_speed/` on the branch
`claude/series-m-masses`, record 110, and its grain and flux form, GRAIN.md
beside it, after the physics-rule review of the first build; series G2's
finding, record 107;
[BEAM_LAW note 38](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)).
A hypothesis beside the law with its own identity: `beam-v1` is unchanged
without the key.

- The world key `doppler`, true or false, false by default, refused on any
  other value; `run.json` carries it and the identity `doppler-v1` under
  `hypotheses` when it is true. Under it a free measured event reads the
  rows that arrived at its Node for the push (step 4) with each direction's
  label flow weighted by the flux of its rows through the body, one scalar
  per (direction, body), the pair `(|G Q |v|^2 - T_d sum_a s_a w_a v_a|,
  G Q |v|^2)` at the body's speed quantised to the grain, off the reader's
  clock per component, before the columns (`nature_beam.weighted_flow`,
  `flux_pair`, `quantised_speed`; `push_form` untouched). The product
  |V_d| x num_d is tested by division before it is formed and refused
  naming the body and the direction.
- `world.SPEED_GRAIN`, G = 2^12, a constant of the law beside Q: the grain
  of a body's speed, `w_a = G x |p_a| // D_a`, the remainder discarded each
  interval (a declared grain, nothing accumulating; note 38 states the bias
  below 1 / G in v). `world.step_divisor(momentum, content, width)`, D = Q
  x S x M + |p|, is the one function of the step rule's divisor:
  `engine.step_axis` reads it and the quantised speed reads it.
- `Measured.frame_momentum`: the momentum the frame read at the start of
  the interval, beside `frame_content` and `frame_charges` (not in the
  record: a snapshot of the record's own momentum for the interval's
  weight, one speed for every group of the interval).
- No load-time bound is new: the parser's static budget of the columns
  (`_column_budget`) takes the largest release flow times the weight's
  largest factor on the table under the key (`weighted_flow_factor`, 3
  on the headings). The registered G2 star worlds fit as registered (the
  weighted flow's product 2^29, today's push 2^34) and one of them runs
  under the key in `tests/test_doppler.py` (h) from
  `examples/events/hubble_stars/gravity_scalar.json` (the example's own
  path). Deleted on the series G2 branch when it merged doppler-v1
  (2026-09-20): `tests/data/g2_gravity_scalar.json`, the reviewer's
  temporary copy of that world, byte-identical to it; the hygiene gate
  keeps one canonical copy of every nonempty file, and the test reads the
  example. The first build's per-axis
  pair, its load check of the pair (`_doppler_load_checks`,
  `relative_speed_bound`, `axis_pace`, `FlightTable.pace`) and its
  "per-direction floors only on an axis where the reader moves" rule
  never reached main and are gone: the per-axis weight was wrong on every
  fan direction (GRAIN.md section 2).
- The pair is taken in absolute value (a body outrunning its source's rows
  takes them from behind at |c - v|, the push keeping the flow's sign); a
  fixed body reads at the weight 1; a free body at rest reads today's
  integers by an exact division, on a fan as on a heading.
- Nothing re-registers: the key is absent in every shipped world, the
  gate set's fifteen worlds replay byte-identical, and nothing is re-run
  under the key in this change. Nothing deleted.
## The worlds reference the family definitions, on 2026-09-20 (host only, no law change)

The second pull request of the model owner's decision of 2026-09-20
(record 113 of [the log](LOG_2026-09-20.md); the built form in
[entity definitions](ENTITY_DEFINITIONS.md#families-in-definitions-event-entities-v2-2026-09-20)):

- `entity_definitions` may climb by leading `..` components; the loader
  confines the resolved file to `root` when the caller gives one
  (`load_world(source, base_dir=, root=)`; the workspace passes its
  configurations directory), else to `base_dir` as before, or to its parent
  for a reference climbing by one `..`; a longer climb is refused without a
  root. A world in its own directory, without a climb, loads as before;
  the runner and the validator are untouched.
- `families_by_definition(document, reference, definitions_source)`, the
  authoring helper of the generators: the tail of a world's inline families
  that the definitions tile becomes instances, the head stays inline, the
  expansion is the inline world in order.
- The shipped worlds of every series but the ones stage (vii) of
  `amplitude-v1` re-pins reference `../entities/families.json` (the list in
  the entity definitions document); `examples/events/make_worlds.py` writes
  the four root worlds; `hubble/make_worlds.py` writes its files as shipped
  (the default separators); `families.json` lists the 24 thrown sources in
  the Hubble worlds' order. Every migrated world's `events.jsonl`,
  `state.json` and books are identical to the inline world's; `run.json`
  gains `initialization_resolution`.
- The catalog's rows name the definition of each entity; the register's
  family names are read from the loaded worlds
  (`tests/test_entity_catalog.py`, `tests/test_entity_definitions.py`).
- Nothing deleted.

## Families in entity definitions, on 2026-09-20 (`event-entities-v2`; host only, no law change)

The model owner's decision of 2026-09-20 (record 113 of
[the log](LOG_2026-09-20.md): one canonical definition per family,
referenced by the worlds instead of copying `families`; the architect's
proposal in [entity definitions](ENTITY_DEFINITIONS.md#families-in-definitions-event-entities-v2-2026-09-20)):

- A definitions document may declare `"format": "event-entities-v2"`; a
  definition of that format may carry `families`, a list in the world's
  family schema (`FAMILY_KEYS`), merged into the expanded world by name:
  the inline families first, then each instance's in declaration order; a
  name already present is kept when every key agrees and refused when one
  differs, naming the family and the key. A definition of a family alone
  (an empty `measured`) is admitted in the second format.
- `event-entities-v1` is unchanged: `families` on a definition is refused
  as an unsupported key, `measured` must hold an Event, and a world placing
  a first-format definition expands to the same bytes as before (the gate
  set replayed byte-identical, [validation](VALIDATION.md)).
- Shipped: `examples/events/entities/families.json` (every family the
  registered worlds declare, once, in the catalog's canonical form) and
  `examples/events/entities/apparatus.json` (the external things and the
  sources of `amplitude-v1` with the material family each is made of),
  written by `make_definitions.py` beside them. No world references them
  yet: the migration of the worlds per series follows stage (vii) of
  `amplitude-v1` (the owner's order in record 113).
- The loader's structural check of a definition's table entry no longer
  requires `rule` in an object entry: the world parser has taken a window
  alone (`{"phase_window": ...}`) since `amplitude-v1`, the rule being the
  family's default, and a definition may now say what a world says (the
  chooser's counter of `apparatus.json`). Both formats.
- Nothing deleted.

## The step drive, on 2026-09-20: the count of Links as the whole part of the driven distance

The model owner's decision of 2026-09-20 on series G2's finding ("1 and 2
are very important for a solution and a new run"; record 107 the findings,
record 108 the owner's decision, "yes; let him give a generic solution if
he can"; change 2 not built as proposed, record 110; the physicist's design RULES.md section 1 (docs/designs/hubble_stars/ on branch `claude/series-g2-stars`);
[BEAM_LAW note 17](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)
as amended). The identity `beam-v1` is kept: the rule is the same count
where the momentum is constant and a repair of it where it changes.

- `core.integer.by_drive(drive, rate, denominator)`, the count primitive
  (record 108): the whole part of an accumulated SIGNED rate on the
  reader's own record, (the count gained, -1, 0 or +1, and the drive
  after), `by_clock` where the rate is constant and of one sign. Signed
  since record 126 of the same day: the first form took |p| and the
  direction from the momentum's sign at the fire, so a momentum reversed
  by a hand-over discharged the distance driven toward the partner as a
  Link away (the deuteron under a suspension); `drive` on the record now
  carries the sign of the momentum that drove it (a body under a
  negative momentum reads a negative drive; its steps are the same).
  Every world whose momenta keep one sign on every axis steps as before;
  a world whose momentum reverses on an axis (an orbit, a turning body, a
  pair under a hand-over) changes: of the 33 example worlds with a free
  body, run at their registered length under the unsigned and the signed
  drive and compared, 16 change (the orbit `s8_r12`, `s8_r24`,
  `s32_r12`, `s32_r24`; Bohr `r2` to `r16`; the nucleus `alpha_line`,
  `alpha_square`, `deuteron_1_kick`; the weak `j3_deuteron`,
  `j3_deuteron_crowd`) and 17 read the same (the coupling `1b_*`, the
  Hubble four, `deuteron_1`, `deuteron_3`, `pp_1`, `pp_1_weak`, `pp_3`,
  `neutron_star`, `sun_planet`, `s1_*`, `j3_neutron_free`). The changed
  registered entries (D, H, I, J) carry a dated line "Re-read under the
  signed drive (2026-09-20)", D and H with their verdicts re-read once
  more in the same form; the old numbers kept as history. `engine.step_axis(drive, momentum, content, width)` reads
  it and returns the sign of the Link stepped (or None) and the drive
  after it, in place of `step_axis(age, momentum, content, width)`
  returning the sign: the rule reads the body's record, not its age. The
  clock's turn, the owed count, the release and the lamp keep `by_clock`
  (their rate is one no push changes). A readings tool that replayed the
  rule off the clock (`tools/coupling_readings.py`, `steps_by_rule`) calls
  the engine's function with a drive.
- `Measured.drive` and `Measured.axis_steps` (three integers each);
  `run.json` and `state.json` carry them per measured event; the `step`
  line carries `drive`. A declared `drive` on a measured event is refused
  as an unknown key. The turn by momentum reads its k0 off `axis_steps`,
  the count of the rule's fires on the axis (a lost or refused step
  counted, as the count off the clock counted it).
- The drive of every axis advances at every self-creation in which the
  body may step; the frame's order stands (one Link per interval, x
  before y before z, a later axis's coincident Link lost), so a body with
  momentum on two axes steps where it did.
- Every world whose bodies take no push replays byte-identical in
  `events.jsonl` (the `step` line's new field aside) and in the positions,
  momenta and books of `state.json`; the gate set's compare names the
  worlds that change (the coupling `1b_m16`, Bohr `r2`, the nucleus
  `alpha_square`, the weak `j3_deuteron`: bodies under a push or a
  hand-over, each stepping one self-creation later than the count off
  the clock stepped it). Of the 33 example worlds with a free body, 30
  change at their registered length (every body under a push, a
  hand-over or a lamp's recoil): the coupling `1b_m1`, `1b_m4`, `1b_m16`;
  the orbit `s8_r12`, `s8_r24`, `s32_r12`, `s32_r24`; the Hubble
  `coasting_scalar`, `coasting_age`, `pushing_scalar`, `pushing_age`;
  Bohr `r2` to `r16`; the nucleus's eight; the weak `j3_deuteron`,
  `j3_deuteron_crowd`; the catalog's `sun_planet` and `neutron_star` (no
  number registered there); `s1_r12`, `s1_r24` and `j3_neutron_free` read
  the same modulo those fields. Each registered entry (C, D, G, H, I, J in
  EXPERIMENTS.md and the series READMEs) carries a dated "Re-read under
  the step drive" line with the new numbers, the old kept as history.
- Re-registered tests, the old integers kept as history in
  TEST_EXPECTATIONS.md: `test_contact` (a), (d), (e),
  `test_nature_beam_clock` (d), `test_paid_charge` (d),
  `test_nucleus_readings` (bodies pushed or handed a momentum).

## The amplitude law, on 2026-09-20, (i): the world key `amplitude`, the record on the row and the normal form (`amplitude-v1`)

The model owner's decision of 2026-09-20 (Highlights 5.4, "DECIDED:
`amplitude-v1` is built, with the four recommendations and the four
unifications"), on the physicist's and the mathematician's design
(docs/designs/amplitude-v1/DESIGN.md); [BEAM_LAW note 37](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation).
The first commit, no behaviour change without the key:

- The world key `amplitude` (true or false, false by default; the identity
  `amplitude-v1` under `hypotheses` and the key in `run.json` when true;
  refused with N below 4 and with a lamp's `rate` other than [1, 1]).
- The store gains the three int64 columns `record`, `branch` and
  `multiplicity` (`nature_beam.FIELDS`, `IDENTITY_FIELDS`; `NatureBeam`
  carries them with the defaults 0, 0, 1; `NatureBeam.record` is renamed
  `record_line`, since `record` is now the row's field, and `state.json`
  writes the three only under the key). A row of no record (every row
  without the key, a declared ray in transit under it) carries 0, 0, 1,
  which add no bit to the packed merge key.
- `NatureBeamStore.merge(modulus)`: under the key the normal form with the
  cancel (antiphase rows of one record subtract; what it removed returned
  per (record, direction)); `Ledger.cancelled_amount`, `cancelled_content`
  and `cancelled_momentum`, the books' `cancelled` lines and
  `momentum.cancelled`, written under the key only.
- Nothing deleted. Every example world replays byte-identical in
  `events.jsonl` and `state.json` without the key; `run.json` gains
  `amplitude` false ([validation](VALIDATION.md)).

## The amplitude law, on 2026-09-20, (ii): the split, the birth of a record and the phase per interval of age

The second commit of `amplitude-v1` (the design's sections 2.1, 2.3 and
3.1; the owner's unifications (1) and (2)); no change without the key:

- The split is `rerelease` with weights (`world.Split`, one rule): a
  `rerelease` entry may declare `weights`, `turns` and `inputs` (the rows
  of weights selected by the arrival direction; the design's single
  vector cannot make a beam splitter, whose transmitted and reflected
  weights depend on the side a row comes from, so the table gained its
  `inputs`); under the key every re-emitted row (w, m, p) becomes the rows
  (w a_i, m x A, p + t_i), the equal split where nothing is declared; the
  apportioning as it was without the key. `PendingRow` carries `record`,
  `branch`, `multiplicity`, `split` and `arrival`; `FamilyPlan` the taken
  rows' columns.
- The birth of a record: a lamp under the key (the rate [1, 1] alone)
  births one record per self-creation with a release, one row of amount 1
  per direction with the multiplicity the directions' count, the identity
  the lamp's number x 2^32 + the birth's ordinal (`Measured.births`,
  `nature_beam.record_identity`); a lamp may declare `turns` per direction.
- The phase per interval of age: `phase_per_link` accepts the pair
  `[n, d]` under the key (`FamilyDefinition.phase_per_age`; the record
  carries the key as declared, `declared_phase_per_link`): the row turns
  `by_clock(age, n, d)` at every walk that advances its age, in the
  inverse walk back; the integer form is per Link crossed as it was. The
  two forms are not one number on the flight table (the design's
  premise "one Link per interval" does not hold on it), which the report
  to the owner names.
- The reading `sum` is accepted on a detector under the key (its record
  the layer's, the next commit).
- Nothing deleted. The gate set replays byte-identical without the key.
  (Commit (i) alone was not runnable on a record alone: its merge kept the
  signed sum where nothing cancelled, a lone far-half row reading a
  negative amount; (ii) takes the magnitude on every group.)

## The amplitude law, on 2026-09-20, (iii): the layer, the reading `sum` and the ladder

The third commit of `amplitude-v1` (the design's sections 3, 5 and 7;
the owner's decisions (a) the ladder normalised by the total with the
rungs at the nearest integer and (c) a branched row pushes matter by its
amount; the review of (i) and (ii)); no change without the key:

- `events/amplitude.py`, the layer: a host register beside the GameBoard
  that reads every record's ends (the clicks at the sets, the faces and
  the border, the reads and re-emissions at `sum` sets), accumulates the
  pointer per (set, arm, label), and at the record's completion (its live
  units 0) takes the ladder over its cells, `b_k = (2 N C_k + Total) //
  (2 Total)`, the cell of the birth phase u and the `gather` line (the
  world's row); `run.json` gains `world`, `open` and `layer`;
  `tools/amplitude_path.py` replays the register through it.
- A split is not a click (the decision on the review's B1): under the
  key a `rerelease` entry takes no pointer gate and no window, and a
  `sum` set no pointer gate; the amount gate stays. Without the key the
  gate is what it was. `PendingRow.offered`: the units a `sum`
  re-emitter absorbed ended there; every other re-emitter's stay live
  until the split re-creates them.
- The reading `sum` is the pointer's reading at the record's scope
  (`DetectorSet.scope`, the owner's unification (4)); its `record` line
  is written at the gather with the scope.
- `NatureBeamStore.merge` returns the units cancelled per (record,
  direction, content per unit), no division in the booking (S3); the
  pair form of `phase_per_link` is bounded at the parse by (age_bound +
  1) x n <= 2^62 - 1 (S1); a lamp short of one quantum per direction
  refuses the birth (S4); the `split` line carries the entry's phase
  `u`; a rotated `sum` re-emitter's line carries `window` and `turn`.
- Series L gains `slits_low` and its reference `slits_one`
  (`examples/events/amplitude/`), the two slits at a low rate.
- Nothing deleted.

## The amplitude law, on 2026-09-20, (iv): the pair, the rotation at the window and the label click

The fourth commit of `amplitude-v1` (the design's section 4); no change
without the key:

- A lamp under the key declares `branches` (the joint labels of a birth
  with their weights) and `arms` (the directions that are separate
  quanta); the birth is one row per label per direction, the branch
  packing the arm and the label (`amplitude.branch_of`), the
  multiplicity the paths per arm times the norm.
- A table entry declares `turn` under the key: the rotation a `sum` set
  reads at its window's setting turns the label-1 column by it
  (`MeasuredDefinition.label_turns`, `Measured.label_turns`). The window
  of a `sum` set is the rotation's setting, declared or read from a
  reading (the choosers' form), never a gate; the layer's `Offer.setting`
  and the gather's `windows` carry it.
- A `read` entry on a `sum` set is a which-path factor: the labels are
  its channels, the joint a product per label (`Offer.read`).
- Series L gains L3 (`bell_choosers`, `bell_<a>_<b>`, `path_<a>_<b>`,
  `bell_16_24_far`, `path_16_24_far`) and L4 (`ghz_<basis>`).
- Nothing deleted.

## The amplitude law, on 2026-09-20, (v): the gate, the label rotation and the review of (iii)

The fifth commit of `amplitude-v1` (the design's section 10; the review
of (iii)); no change without the key:

- A `rerelease` entry declares `rotate` (the rotation of one label bit on
  the GameBoard, `world.Rotation`) and `gate` (the CNOT between the records
  of distinct lamps pending at the entry, `world.Gate`; the layer's
  `join`, the identities aliased); the `gate` and `rotate` lines. The
  register's ceiling is checked at load: the multiplicity through every
  re-emitter of the world within 2^62 - 1 (S6).
- Interference is coherent within one Node only (the decision on the
  owner's point 5): the layer's offers are per Node, a set's cell weight
  the sum over its Nodes of the per-Node squares, the click's Node chosen
  by the rungs over the Nodes; the gather names the Node, the content and
  the momentum of the chosen rows (S1). The two-slit expectations are
  re-pinned (wall 34, screen 15, faces 15 of the 64 births).
- One birth per rebirth at a chosen `sum` re-emitter, every re-created
  row's units by its split (B1); a free family's rows keep the unkeyed
  apportioning and gates at every entry (B2); a `phase_window` on a
  `rerelease` whose Node reads no `sum` set is refused at load (S3); a
  detector's name may not use the layer's prefix `measured:` (S5); the
  reading tool completes on the `gather` lines (S2); the design is cited
  at `docs/designs/amplitude-v1/DESIGN.md` (S4).
- The half-angle tables at N = 4096: an even setting reads the 4096 table
  at s / 2 (`amplitude.half_angle`), an odd one is refused.
- Series L gains L5 (`cnot_pair_<a>_<b>`, `cnot_twice`, `cnot_ghz_<basis>`,
  `rotations_3`, `rotations_4`) and L6 (`bell_n1024_<a>_<b>`,
  `bell_n4096_<a>_<b>`).
- Nothing deleted.

## The amplitude law, on 2026-09-20, (v-fix): the gate's copies booked, the control declared, the hold local, a record elsewhere refused

The gate review of (iv) and (v) (three blocking findings, one should fix;
no pinned integer of the 46 keyed worlds moves; the gate set byte-identical
without the key):

- A `rerelease` entry's `gate` declares `control`, the direction the
  control record's rows arrive on: required for two parties or more,
  refused for one; the shipped CNOT worlds carry it (the pair's [1, 0, 0],
  GHZ's [0, 1, 0]). Until now the control was the earliest-declared lamp,
  and the `measured` list reversed turned the pair into a product (S1).
- The gate acts when rows of `parties` distinct emitters are pending at
  the entry, read from the rows alone (the design's local hold); the
  layer's live count is no longer read by the GameBoard (B3).
- The units the gate's copies add are booked on the layer's live count
  (the `gate` line's `added`; the reading tool books it too): every
  gathered record of the CNOT worlds ends at live 0 where it ended at -1
  (B1).
- A record that reaches a gate with units elsewhere or with an offer
  already made is refused naming the record, the units and the sets: the
  lazy relabelling of the design's section 10 is not built (B2).
- Nothing deleted.

## The amplitude law, on 2026-09-20, (vi): the one click, not landed; the key stays

The design's section 6 (the record form the default, the key `amplitude`
and its parsing deleted, the crowd-threshold path of the `wave` reading
deleted) was tried after (v) as the model owner's half-hour version on
the gate set of seventeen worlds ([validation](VALIDATION.md)): the key
forced true and the `wave` pointer gate off, the replay compared with
stage (v)'s digests. Worlds outside the crowd-threshold series change, so
by the owner's rule the stage stopped there and nothing of it is
committed:

- Refused at load: `two_slits` (the lamp's rate [64, 1]),
  `catalog/lamp_mirror_screen` ([4, 1]) and `heisenberg/w3_beam`
  ([47, 1]): under the record form a lamp births one record per
  self-creation and the rate [1, 1] alone is accepted.
- Failed in the run: `catalog/sun_planet` (the record 8589934593 at the
  set `screen` with the multiplicities 9 and 36: one multiplicity per
  offer).
- Changed clicks: `bell/read`, `bell/a0_b8` (the old A2, in the series)
  and `lensing/mass_meeting` (outside it): their lamps at [1, 1] birth
  records, read by the ladder in place of the crowd's threshold.
- Changed bytes with no value changed: `coupling/7_pp`, `one_content`,
  `redshift/age`, `hubble/coasting_age`, `weak/j2_filter`,
  `weak/w_exchange` and `detector/periodic_z_node` (the columns `record`,
  `branch` and `multiplicity` written on every click line, `rows` on the
  read lines and the rows of `state.json`); `nucleus/deuteron_1`,
  `weak/j3_neutron_free` and `bohr/r2` changed by their digests, their
  lines not kept (no lamp in any of them).

What the one click needs before it can be the default: the lamp's rate
under the record form (r units per direction as r paths of one birth or
as r births), a set's offer of several multiplicities of one record, the
columns written only where a record is, and the design's test 7 restated
as identity on the worlds without a lamp. Until then the key `amplitude`
stays as (i) declared it, false by default, and the crowd's `wave`
threshold stays; nothing deleted, nothing added. Stage (vii) builds the
four, below.

## The amplitude law, on 2026-09-20, (vii-1): the one click's prerequisites under the key

Stage (vii), step 1 (the model owner's order after the landing): nothing
changes without the key, and a world without a lamp now reads the same
with it.

- A lamp's `rate` [n, d] is accepted under the key: a self-creation
  births as many records as the rate says units per direction
  (`by_clock(age, n, d)`), as many as the lamp can pay whole, each with
  its own ordinal, the birth phase of the j-th record of a self-creation
  the clock's phase advanced by j strides (the design's 2.1, the
  extension). Until now the rate [1, 1] alone was accepted.
- Rows of one record at one offer with multiplicities that differ by a
  square factor add at the common denominator (the held pointers
  rescaled by the root of the ratio, `amplitude.common_denominator`); a
  ratio that is not a square is refused naming the record, the set and
  the two multiplicities (the integer form has no cross term over the
  square root of their product). Until now two multiplicities at one
  offer were refused.
- The columns `record`, `branch` and `multiplicity` (and `age` on a
  click line, `rows` on a group line) are written on the rows of a
  record alone, in `events.jsonl` and in `state.json`; the books'
  `cancelled` lines are written in a recorded world alone (the key and a
  lamp, `NatureBeamWorld.recorded`). A world without a lamp reads the
  same with the key and without it (`tests/test_amplitude_click.py` (d)
  on the gate set's lamp-free worlds at their caps); the gate set is
  byte-identical without the key as before.
- Nothing deleted.

## The amplitude law, on 2026-09-20, (vii-2): u the record's own field, unread by the GameBoard

Stage (vii), step 2 (the K finding of 2026-09-20, the first of its two
changes; nothing changes without the key):

- The row's column `birth`: the birth phase u of the row's record, the
  lamp's count of births less one, mod N (the record's ordinal at its
  lamp; a rebirth's u the re-emitter's own count), carried through every
  re-creation, split, rotation and gate copy; 0 on a row of no record;
  `u` on the rows of `state.json` and on the `click` lines of a record.
  Until now u was the lamp's clock phase at the birth, so a lamp whose
  clock turns 8 steps per interval gave u on 8 rungs and a rebirth's u
  was always the re-emitter's phase (the layer's test (k) re-pinned: the
  rebirths now go a 32, b 32 where every one went to a).
- Every rule of the GameBoard that reads a record row's phase reads the
  path phase, phase - u: the meeting's register (the wraps counted on
  the path, the running phase restored after), the crowd's pointer of a
  `wave` set and its window, a window read from a reading, the `beam`
  pairing, the phase a set returns, the faces' and the border's
  pointers. The layer's offers read the running phase as designed and u
  enters at the click alone. A row of no record reads its phase itself:
  nothing registered changes.
- The Mach-Zehnder, Elitzur-Vaidman, two-slit, pair, GHZ, gate and
  N = 1024 / 4096 integers are unchanged (the lamps of series L turn one
  step per birth, so u was the ordinal already).
- Nothing deleted.

## The amplitude law, on 2026-09-20, (vii-3): the push by share, the remainder on the books

Stage (vii), step 3 (the K finding of 2026-09-20, the second of its two
changes; nothing changes without the key):

- A record's row pushes matter with its share amount^2 / m of the
  quantum's unit label (the record's norm in m: a record's shares sum to
  one), the integer form label x amount // m floored toward zero
  (`nature_beam.share_of`): at its absorption at a measured event (the
  click's push, the entry's momentum), at a home, at the push of a `read`
  and at the recoil of a paid re-creation (the born rows' shares: one
  quantum's label over a record's rows, a lamp's birth and a split
  alike). Until now every row pushed by its whole label, so a record of
  k rows gave k labels to matter (the owner's (c), the sum over the
  branches; note 37 (ix)); a row of no record pushes by its label as it
  did, and the meeting's turn stays on the transit and `turned` lines.
- The books' `remainder` line per family and in total, in a recorded
  world: the labels less the shares at an absorption or a home, less the
  born labels less the recoil at a re-creation, so that the momentum
  books close with the transit line carrying the rows' whole labels
  (`Ledger.remainder_momentum`). The click line of a record carries
  `share` beside `push`.
- Nothing deleted.

## The amplitude law, on 2026-09-20, (vii-4): the one click, the record form the law

Stage (vii), step 4 (the design's section 6; the model owner's order
after the landing, under the stop rule of stage (vi)): the record form is
the only form. Deleted, each with its consequence:

- The world key `amplitude` and its parsing: a world that declares it
  (true or false) is refused naming this entry; remove the key. The
  parser's refusals "needs the world key `amplitude`" of the pair form of
  `phase_per_link`, a lamp's `turns`, `arms` and `branches`, a table
  entry's `turn`, `rotate`, `gate`, `weights`, `turns` and `inputs`, and
  the reading `sum`: every one of them is accepted on any world.
- The crowd form of a lamp (its rate's units per direction as rows of no
  record): every lamp births records (the rate's count of records per
  self-creation, (vii-1)), so every world with a lamp is a recorded world
  (`NatureBeamWorld.recorded`), its rows read by the ladder, the identity
  `amplitude-v1` under `hypotheses` (`run.json`'s key `amplitude` is
  gone). A lamp is refused with N below 4 (a record's circle holds the
  quarter turn of a reflection); the refusal of the key with N below 4
  is gone with the key.
- The crowd's `wave` threshold on the square of the coherent pointer
  (issue #359 step A, BEAM_LAW note 32): the threshold is the amount
  summed over the set under both readings; the crowd's pointer gives the
  set's phase (the window under `wave`) and its record, not a gate. Rays
  that cancel at a `wave` set no longer pass by the gate; a record's rows
  in antiphase cancel at the merge before any set reads them.
- The load-time ceiling of the multiplicity (the review's S6) multiplies
  the declared `weights`, `rotate` and `gate` factors alone; a plain
  `rerelease` (the equal split by the directions' count) is bounded by
  the split's own check when the multiplicity is formed, since a path's
  count of re-emissions is not known at load (the check now runs on
  every world with a lamp).
- The apparatus's layer exists on every world (`NatureBeamSimulation.layer`),
  the merge is always the normal form, `tools/amplitude_path.py` replays
  any run with a lamp; the design's test 7 is the pinned digests of the
  gate set's lamp-free worlds (`tests/test_amplitude_click.py` (d)).
- The 46 shipped worlds of series L no longer carry the key (regenerated
  by `examples/events/amplitude/make_worlds.py`, the expectations
  unchanged).

What follows for every world with a lamp (the changed worlds of the gate
set, re-run and marked "re-run under the one click; the verdict to be
re-read", the old numbers kept as dated history): a lamp's rows are
records born at u, the lamp's count of births, with the direction's turn
as their path phase, so the phase returned to a lamp by a click no longer
enters its births and a lamp's `phase_window` gates the release by the
clock's phase but the row born carries u; a window on a table entry reads
the path phase of a record's row, so the crowd form's phase correlations
(the Bell worlds of series A2 in phase form, the choosers) read E = 1
with every pair in (-1, -1) and their tools' checks fail: the pair is the
record's (`branches`, `arms`, the reading `sum`, series L3 and L5); a
lamp's birth recoils by its rows' shares and a re-emitter by the shares
in and out, the rest on the `remainder` line; the crowd's clicks are the
records' rows (k rows per record at k directions), so the clicked amounts
of a lamp's crowd multiply by the directions' count and the click's
momentum is the row's share. A high-rate lamp is a host cost: the records
of `heisenberg/w27_beam` (47 per interval on 27 opening Nodes) run at
seconds per interval where the crowd form ran in milliseconds, the
layer's offers being kept per record until its completion; on a host of
16 GB the run was killed at 7.1 GB after 68 minutes at interval 211 of
350 (the gate set's world is not re-run to its length). After the gate
review of the one click the layer's table releases a record at its
completion (its offers with it, the identity kept for the lazy deletion
of its rows; a completion visits the records whose live count reached 0
alone; every reading byte-identical on the gate set at its caps and on
the K worlds): the layer holds no offer open on this world and the cost
is the GameBoard's rows, which do not merge across records (1457 records
born per interval, 1.8 million rows and 2.75 s per interval at interval
40; 3.3 GB at 20 minutes, interval 136). Series G2 (`examples/events/hubble_stars/`,
registered after the gate set) is a lamp series too: its 18 worlds of
`record/` and `doppler/` are carried without the key (their diff the key
alone), its base worlds' stars birth records, and the acoustic reading
rule (the slope of a `wave` set's phase) reads no turn under the record
form; the record worlds' `source` rule is the record form's reading, the
verdict to be re-read.

## The weak force, on 2026-09-20, (iv): the W world (no key added)

The model owner's decision of 2026-09-20 ([Highlights 5.4](HIGHLIGHTS.md#54-the-detector),
"DECIDED: go on everything", item (3): the W world after the
transformation; [BEAM_LAW note 36](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation) (iv)).
No key, no refusal and no record line is added: the W is a paid family
with a whole charge per unit of amount (D-1, (ii)) and the family key
`lifetime` 1 ([the lifetime](#the-columns-of-the-one-coupling-the-lifetime-the-held-content-and-the-contact-through-the-table-on-2026-09-20-columns-and-lifetime-per-family-held-per-measured-event-columns-v1-the-contact-record)), thrown as
a product of a `become` ((iii)) and measured by the keys' rule one Link
away; L = 0 is no family at all (a lifetime of 0 is refused, as before),
the contact form being the `become` entry itself. The source is
byte-identical to (iii)'s, so every example world replays as under (iii)
(VALIDATION). `examples/events/weak/w_exchange.json` (written by
`make_worlds.py`, its integers under `w` in `expectations.json`),
`tools/weak_readings.py` reads it (the things' `content`, `charge`,
`momentum` and `click_ticks` off the record, the border `lifetime`'s
clicks per family), `tests/test_w_world.py` (a) to (d) and
`tests/test_weak_readings.py` (c).

## The weak force, on 2026-09-20, (iii): the transformation `become`, the identity `weak-v1`

The model owner's decision of 2026-09-20 ([Highlights 5.4](HIGHLIGHTS.md#54-the-detector),
"DECIDED: go on everything", item (1): "the transformation `become` with
the identity `weak-v1`", after the neutrino; [BEAM_LAW note 36](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)
(iii)). Identities: no world file changes; no registered world declares a
transformation, so every example world replays byte-identical in
`events.jsonl`, and `state.json` and `run.json` equal but for the added
`became` and `become` (VALIDATION).

- **The keys.** The measured-event key `become` (the clock trigger),
  `{"at": a, "into": family, "products": [[family, amount, content per
  unit], ...], "crowd": c}`: at the self-creation whose clock reaches `at`
  (the age against the key by the one `by_clock`, `nature_beam.ages_at_key`:
  first at `at`, then at every multiple of it), while the count the clock
  read is below `crowd` (optional, an integer from 0; absent, no gate), the
  event becomes an event of `into`, the products are paid from what it
  holds of its own family (R = the sum of amount x content per unit, at
  most its `amount`), the rest moves to `into`, the products are born as a
  re-release is (the parent's phase, product k on the direction counted
  from (clock age + k) mod n) with the recoil over all of them, and the
  key is consumed. The table rule `become` (the click trigger), the
  fifth beside `read`, `measure`, `rerelease` and `pass`: an entry
  `{"rule": "become", "phase_window": s, "phase_width": w, "into": ...,
  "products": [...]}` clicks an arrival as `measure` does and fires the
  same transformation, its products born at the reader's next
  self-creation; the entry is consumed. A free product's content is 0, a
  paid product's from 1; the charges must balance at load (rho_into x
  (amount - R) plus the paid products' whole charges against rho_from x
  amount).
- **The refusals, naming the key.** `become` without `into` or
  `products`; `into` naming an unknown family or the event's own; a
  product naming an unknown family, an amount below 1, a free product's
  content other than 0, a paid product's content below 1, a label beyond
  the bound; `at` below 1 or absent on the clock trigger; `at` or `crowd`
  on a table entry; `crowd` negative or not an integer; `into` or
  `products` on an entry whose rule is not `become`; the products' content
  above the `amount`; the charges unbalanced; `become` on a family. At run
  time an event that holds less than its products need at the trigger
  refuses the run naming itself.
- **The definitions.** `world.Transformation` (new: `into`, `products`,
  `at`, `crowd`, `needed`), `world.BECOME_RULE`, `world.WEAK_RULE`,
  `world.TABLES` gains `become`; `world._table_entry` returns five values,
  (rule, window, reads, width, transformation), and takes the families,
  the event's family and amount, the direction table and its directions;
  `MeasuredDefinition.become` and `.transforms` (new, the clock trigger
  and per family the click trigger); `NatureBeamWorld.transformations`
  (new); `hypotheses` gains `weak-v1`; the contact under a `become` entry
  is the default `measure`. `measured.PendingRow` (new: amount, content,
  phase, first, thrown), `Measured.become`, `.transforms`, `.became`,
  `.transformed` (new), `Ledger.held_became` (new, the `became` line);
  `nature_beam.transform` (new, the one function of the two triggers),
  `nature_beam.TRANSFORM_RULE`, `RULE_NAMES`, `MEASURE_RULE_NAME`.
- **The record.** `hypotheses` carries `weak-v1`; `run.json`'s `numbers`
  per measured event carry `become` (the declaration by names or None);
  the measured events' states carry `became` and their `family` after; the
  books' measured line per family gains `became` (initial + measured +
  became = current + spent + escaped); `events.jsonl` gains one `become`
  line per transformation at the products' birth (`trigger`, `triggered`,
  `from`, `into`, `products` with their directions, `recoil`, `counted`);
  the tally of a `become` entry's clicks is under `measure`. A test or
  tool that pins a measured event's `numbers` or the books' measured line
  adds the keys (`tests/test_nature_beam_body.py` and
  `tests/test_nature_beam_clock.py` do).
- **Series J1 and J3** under `examples/events/weak/` (`j1_lattice`,
  `j1_source`, `j3_deuteron`, `j3_deuteron_crowd`, `j3_neutron_free`, the
  expectations in `expectations.json` written by `make_worlds.py` before
  the runs, a file with the `format` `weak-expectations-v1` that the tests
  reading every JSON under `examples/events/` as a world skip, as they
  skip an entity definitions file: a world declares `law`, never
  `format`), read by `tools/weak_readings.py`; `tests/test_become.py` (a)
  to (f) pins the rule, `tests/test_weak_readings.py` (b) the tool.

## The weak force, on 2026-09-20, (ii): a paid family's charge per unit of amount (D-1)

The model owner's decision of 2026-09-20 ([Highlights 5.4](HIGHLIGHTS.md#54-the-detector),
"DECIDED: go on everything", item (2): "D-1, a paid family may declare a
whole charge per unit of amount, read on the charge line only, the push
untouched"; [BEAM_LAW note 36](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)
(ii)). Identities: no world file changes; no registered world declares a
charge on a paid family, so every example world replays byte-identical in
`events.jsonl`, `state.json` and `run.json` (VALIDATION).

- **The refusal lifted.** "A paid family (quantum h) carries no charge" is
  gone: the family key `charge` on a paid family is accepted as an
  integer, the whole charge per unit of amount, and refused as a pair
  with a denominator other than 1 ("a paid family's charge is per unit of
  amount and whole"). The wording of the law: the charge of a measured
  event is rho times its content for a free family and the declared whole
  charge times the amount for a paid family. `tests/test_default_table.py`
  (c) and `tests/test_nature_beam_world_parsing.py` (a) re-pin the lifted
  refusal as the fractional one.
- **Where it is read.** `FamilyDefinition.column_charge` (new): the value
  of the family's `charge` column, rho for a free family and (0, 1) for a
  paid one, so `FamilyDefinition.values`, the push (`push_form`), the
  parser's budget and the frame's `frame_charges` never see a paid charge.
  `Measured.unit_charges` (new, per family), `Measured.units(family)`
  (new: the units clicked plus the units pending) and
  `Measured.charges(for_push=False)` (the keyword new: the report and the
  books include the paid units' charge in the `charge` column; the frame
  passes `for_push=True`). `Ledger.units_escaped` (new, per family): the
  clicked units of a body that stepped off through a face. The books'
  `charge` pair (`NatureBeamSimulation.books`) adds, per charged paid
  family, c x the transit line's current and c x (the escaped amount plus
  the units escaped).
- **A new refusal.** A lamp on a measured event of a charged paid family
  ("its releases would create charge from nothing").

## The weak force, on 2026-09-20, (i): the window's width `phase_width` (no change of law)

The model owner's decision of 2026-09-20 ([Highlights 5.4](HIGHLIGHTS.md#54-the-detector),
"DECIDED: go on everything; just make sure again that it is good and
generic", item (1): the neutrino first with the table-entry key
`phase_width` and no change of law; [BEAM_LAW note 36](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)
(i)). Identities: no world file changes; every example world replays
byte-identical in `events.jsonl`, and `state.json` and `run.json` equal
but for the added `widths` (VALIDATION).

- **The key.** A table entry's object form and a lamp accept
  `phase_width`, an integer w from 1 through N: the window is the w
  consecutive steps of the circle centred on its setting,
  [s - floor(w / 2), s - floor(w / 2) + w), inside when
  (d + floor(w / 2)) mod N < w with d = (phase - s) mod N
  (`nature_beam.window_admits(distance, width, modulus)`, new: the one floor
  of the window and its width, rows or one value). Without the key the
  width is N / 2 (`world.default_width(N)`, new): the half circle as it
  was on every (phase, setting) pair, so every registered world is
  bit-identical. Refused naming the key: a width outside 1 .. N, on `pass`,
  on a family without a phase circle, and without a `phase_window` (a width
  is the width of a window); a lamp's the same.
- **The window table is deleted.** `NatureBeamTables.window` (the boolean
  table over the distances of the half circle) is gone; `nature_beam_tables`
  no longer builds it. A test or tool that read `tables.window[d]` reads
  `window_admits(d, default_width(N), N)` (`tests/test_nature_beam_window.py`
  (a) does). `beam`'s pairing by opposite phase reads the row's entry width
  as its arc.
- **The definitions and the record.** `world._table_entry` returns four
  values, (rule, window, reads, width); `MeasuredDefinition.widths` (new,
  per family, None where none is declared) and `LampDefinition.width`
  (new, None by default); `Measured.widths` and `Measured.lamp_width`
  (new); the measured events' states and `state.json` carry `widths`
  beside `windows`. `run.json` is otherwise unchanged.
- **Series J2** under `examples/events/weak/` with `tools/weak_readings.py`
  and `tests/test_weak_readings.py`; `tests/test_window_width.py` (a) to
  (e) pins the rule.
## The meeting, on 2026-09-20 (`meeting` per world; `meeting-v1`; the `turned` line of the books)

The model owner's decision of 2026-09-20 ([Highlights 5.4](HIGHLIGHTS.md#54-the-detector),
"DECIDED: the meeting, M-R: an event in transit reads the crowd as a body
does, a report, not a balance"; [BEAM_LAW section 3 step 3 and note 35](BEAM_LAW.md#3-the-nodes-interval-nature_beam);
[expectations](TEST_EXPECTATIONS.md#the-meeting)). No world file changes:
the key is absent by default, and every example world replays
byte-identical in `events.jsonl` and `state.json`.

- **Added, the world key `meeting`** (true or false; false by default):
  under it every paid unit in transit reads the free crowd of the other
  numbers at every free-space Node after the collision (the one reading
  set, the vector moment V with the labels as weights, the column sum
  kappa of its family against theirs) and turns toward t = kappa V by k
  steps of the arc permutation of the direction table, k read off its
  phase register (the crowd met in whole units of Q added to the phase,
  one grain step per wrap of the circle). Refused, naming the register,
  with a paid family without a phase circle; refused when not true or
  false. The new module `src/event_universe/events/meeting.py`
  (`ArcTable`, `arc_table`, `arc_shift`, `column_sum`, `register`,
  `register_inverse`, `crowd_flow`, `meet`); `nature_beam` calls `meet`
  once after the collision and once before the inverse collision;
  `NatureBeamTables` gains the field `arcs` (built by `nature_beam_tables`;
  a caller that builds the tables by hand passes `arc_table(flight.labels)`).
- **Added, the identity `meeting-v1`** under `hypotheses` in `run.json`
  when the key is true (`world.MEETING_RULE`; `NatureBeamWorld.meeting`,
  `NatureBeamWorld.hypotheses`), and the key itself in `run.json`
  (`meeting`, as declared).
- **Added, the `turned` line of the books**: `Ledger.turned_momentum` per
  family and `Ledger.turned_momentum_total()`; `books()` carries
  `families[<name>].turned` and `momentum.turned` (so every audit line of
  `run.json` gains them, zero without the key). Under the key the running
  transit momentum line is moved by the same delta, so `books(recount=True)`
  equals `books()` and the momentum book of a paid family reads
  measured + transit + escaped - turned constant. Re-pinned with the new
  line written first: `tests/test_lifetime.py` (b) and
  `tests/test_nature_beam_flight.py` (the periodic axis and the open
  face), whose exact momentum blocks gain `"turned": [0, 0, 0]`.
- **The readings tool of series K** (`tools/lensing_readings.py`) reads the
  meeting worlds too (the model ids `beam-lensing-<name>-meeting-v1`
  beside `rays-lensing-<name>-space-v1`), the phase offset per pixel, the
  `turned` line and, with two lamps, the centroid per lamp and the
  crossing; `examples/events/lensing/make_worlds.py` writes the four
  worlds under the key (`<name>_meeting.json`) and `lens_meeting.json`.
## A table entry's window read from a reading, on 2026-09-20 (`phase_window` as `{"reads": ..., "offset": ...}`; issue #363)

An additive key of the world file ([BEAM_LAW note 34](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation);
[ENGINE, the world](ENGINE.md#the-beam-law-beam-v1);
[expectations](TEST_EXPECTATIONS.md#a-window-read-from-a-reading)): a
measured event's table entry may declare `"phase_window": {"reads":
"<family>", "offset": s}` in place of the number. The centre of the window
is then the phase of the coherent pointer of the named family's rows
present at the set in the interval (every row at the set but the reader's
own number) plus the offset in phase steps (0 by default); the width is
the law's. With no such row at the set, or a zero pointer, the entry
passes with a `pass` record naming `window` None and `reads`; every
`click` of such an entry carries the `window` used. Refused naming the
key: an unknown family, a family without a phase circle, the entry's own
family, the form on `pass` or on a lamp, an `offset` outside 0 .. N - 1,
an object with other keys or without `reads`.

- **No world file changes**: the number form and the string form of a
  table entry mean what they meant; a lamp's window stays a number. Every
  world without the key replays byte-identical in `events.jsonl`,
  `state.json` and `run.json` (21 example worlds compared,
  [validation](VALIDATION.md)).
- **The API**: `world.WindowReading` (the declared form, resolved by the
  parser), `MeasuredDefinition.window_reads` and `Measured.window_reads`
  (per family the `(family index, offset)` read, or None; a definition
  made without the field reads no window), `nature_beam.setting_steps`
  (per detector set the nearest step of the pointer of a family's rows
  present at it, None without one), `FamilyPlan.t_window` (the window
  used per taken row of such an entry). `_table_entry` returns the window
  as `int | WindowReading | None`.
- **The record**: the `pass` line of such an entry carries `reads`; its
  `click` line carries `window`. Other lines are unchanged.
- **The run**: `examples/events/bell/make_chooser_worlds.py`,
  `tools/bell_choosers.py`, `tests/test_bell_choosers.py`, the entry
  [A2 with the choosers on the GameBoard](EXPERIMENTS.md#a2-with-the-choosers-on-the-gameboard-2026-09-20).

## The four unifications of the formulas, on 2026-09-20 (the pointer as the first moment; `by_clock` on every age against a key; one moment table over one set; the columns at the clock age)

The model owner's decision of 2026-09-20 ([Highlights 5.4](HIGHLIGHTS.md#54-the-detector),
"DECIDED: the four unifications of the formulas"; [BEAM_LAW note 33](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)):
the places where the code spelled the one moment or the one `by_clock`
twice are spelled once. Identities: no world file changes and every
example world replays byte-identical in `events.jsonl` and `state.json`
except where a section below says.

- **(1) The pointer is the first moment of the one reading over the
  circle.** `nature_beam.coherent_pointer(amount, phase, starts, cosines,
  sines)` takes the moment table on the circle's unit vectors
  `(C[phase], S[phase], 0)` (`nature_beam.circle_vectors`) with the
  weights `32 x amount` and returns its first moment per contiguous
  group; the `totals` argument (the exact clicked amount per group, the
  former gate of the int64 path) is removed from the signature: the
  callers `tools/buildup_readings.py`, `tools/bohr_readings.py` and
  `tests/test_bohr_readings.py` drop it. `nature_beam.POINTER_AMOUNT_BOUND`
  is deleted: the register path of the pointer is the reading's own
  bound, `nature_beam.reading_fits(amounts, vectors, ages, widest)` (new;
  the one test `read_arrivals` refuses by and `first_reading_overflow`
  looks per group by), and beyond it the pointer is the same table in
  Python integers, `nature_beam.moment_table(v, a, ages, exact=True)`
  (new keyword; the dtype `object`). `nature_beam.read_groups(vectors,
  weights, starts, ages, exact)` (new) is the one reading per contiguous
  group of rows (the taken rows of step 4 and the pointer alike). A world
  whose detector set clicks a row of an amount between 2^41 and 2^48 in
  one interval now takes the Python path for that pointer where it took
  the register (the same integer, slower); no registered world does.
- **(2) Every age against a key is the one `by_clock`; the turn is the
  release at the rate [1, K].** The world key `K` keeps its name and
  accepts, beside the integer K (the content per phase step per
  self-creation, read as the pair `[1, K]`: every example world, bit for
  bit), a pair `[n, d]` of phase steps per unit of content per
  self-creation like `release`; the turn is `by_clock(age, content x n,
  d)` (`NatureBeamWorld.turn(age, content)`, new; `NatureBeamWorld.turn_rate`,
  new, the pair), refused at half the circle as before, the parser's
  static bound `2 x content x n < d x N`. `NatureBeamWorld.K` is the key
  as declared (`int | tuple[int, int]`; `run.json` carries it as declared,
  so an integer world's record is unchanged); the frame, the tools of the
  readings (`tools/lensing_readings.py`, `tools/buildup_readings.py`,
  `tools/heisenberg_readings.py`, `tools/hubble_readings.py`) and the
  parser's own bounds read the rate through `turn` and `turn_rate`, not
  `K`. `nature_beam.by_clock_rows(age, numerator, denominator)` (new) is
  `by_clock` over rows (the frame's turns in one array; the inline floor
  difference of `_frame_all` is deleted) and `nature_beam.ages_at_key(age,
  key)` (new) the rows whose walk brought their age to the key,
  `by_clock(age - 1, 1, key) = 1`: the lifetime's click (`store.age >=
  lifetime` deleted) and the world's age bound (`store.age.max() >
  age_bound` deleted; the key age_bound + 1) read it. Identities on every
  reachable state (a row never lives past its key); no world file changes.
- **(3) One set object shared by a body and a detector; one moment table
  over the set.** The data: `DetectorSet.nodes` (new, `dict[Address3,
  int]`) maps every Node of the set to the number of the measured event
  there, a body one event, a declared detector several; `Measured.nodes`
  is a property read from the body's set (the dataclass field and the
  `nodes=` argument of `Measured(...)` are removed); the engine's index
  `NatureBeamSimulation.at` is `dict[Address3, DetectorSet]` (until now
  `dict[Address3, int]`, the number), with `NatureBeamSimulation.occupant(node)`
  (new) the number of the measured event whose body holds the Node or
  None, and `_place(entry, nodes)` (new) moving a body's Nodes in its
  set's map and in the index (a test that read `simulation.at[node]` as
  a number reads `simulation.occupant(node)`). A detector stays a
  detector and a body a body: the rule unification (a detector as one
  measured event) is not taken. The table: `family_plan` takes one
  `moment_table` per family over the rows at the set with the two masks
  (present, admitted); the presence and the age moment are its zeroth
  and age moments over the present rows (the two `np.add.at` sums are
  deleted), the record's component and the push's flow its moments over
  the admitted rows, the flow with the label's weight (the separate
  `labels = u x weight` product is deleted); `beam`'s pairing enters the
  table as a split of the paired row into the units that go on (present)
  and the units that click (admitted). `nature_beam.moments_of_groups(table,
  starts)` (new) sums a moment table per contiguous group;
  `read_groups` calls it. No world file changes; every example world
  replays byte-identical.
- **(4) The columns floored at the clock age like every other rate.**
  `push_form` takes the reader's clock age (`Measured.clock_age`, the age
  before the interval's self-creation) where it took `Measured.age` (the
  age after the frame's advance), so the columns' `by_clock` is read at
  the same age as the turn, the release, the owed count and the step
  ([BEAM_LAW note 33](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)
  (4); note 20's exception is closed). A world whose product `V x E_c x
  n_c` is not a multiple of `D_c x d_c` reads the floor's extra unit on
  other ticks than before, the sum over the ticks unchanged; no world
  file changes and every example world replays byte-identical. Re-pinned
  with the new integers written first: `tests/test_columns.py` (b) ((-67,
  -67, 0) then (-68, -68, 0) at the ticks 1 and 2, and the sign and
  `extra` cases with them) and (e) (-43, -43, -42, -43 at the ticks 1 to
  4), `tests/test_nature_beam_push.py` (k) (`by_clock(tick - 1, 1280,
  25)`); the new test (m).

## The `wave` threshold on the pointer's square and the escaped momentum per family, on 2026-09-20 (issues #359 step A, #360, #361)

The model owner's decision of 2026-09-20 ([BEAM_LAW note 32](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation);
[expectations](TEST_EXPECTATIONS.md#the-detectors-record)). No world file
changes: the keys `threshold` and `reading` keep their spelling and their
defaults (`threshold` 1, `reading` `wave`).

- **Changed, the threshold under `wave`**: a `wave` detector set clicks in
  an interval when the square of the coherent pointer of its arrivals
  (every number but each Node's own), read in units of one ray, is at
  least its `threshold`, and passes otherwise with `pass` records naming
  `threshold`; the unit is the square of one unit's pointer at phase 0,
  (32 x 256)^2 = 2^26, and the reading the nearest integer
  (`nature_beam.pointer_units(X, Y) = (X^2 + Y^2 + 2^25) // 2^26`): one
  unit at any phase reads 1, a rays in phase a^2 (exactly through a = 11
  at N = 64), two opposite rays 0. Until now the threshold under both
  readings was the amount summed over the set, so a pair in antiphase
  clicked and added 0 to the record; now it passes (whether or not a
  window is declared) and adds nothing. Under `beam` the threshold is the
  amount as before. No memory between intervals.
- **Which registered runs change**: of the 66 example worlds 65 are
  byte-identical in `events.jsonl` (`two_slits`, `one_slit`, the Bell ten
  with S = 2 exactly, and `w1_wave`, `w3_wave`, `w9_wave` among them: no
  set of theirs ever read a pointer below its threshold with an amount
  at it); `w27_wave` alone changes, 2312 rays passing a screen pixel in
  antiphase where they clicked with the pointer 0 and going on to other
  pixels and the faces (38 of 161 pixels' records differ, the screen's
  clicks 150 187 -> 148 131), and the three worlds of A10 at a low rate
  (`examples/events/buildup/`, merged after the runs: the clicks in the
  window 172 753 -> 169 855, 171 871 -> 158 878, 171 742 -> 158 622,
  every verdict the same), re-registered old against new in
  [EXPERIMENTS A10](EXPERIMENTS.md#a10-the-width-of-an-opening-and-the-spread-behind-it-under-the-beam-law-2026-09-20)
  and [validation](VALIDATION.md#the-wave-threshold-on-the-pointers-square-the-66-example-worlds-compared-a10-and-bell-re-read---2026-09-20). A
  world whose `wave` detector reads several rays of one phase at a
  threshold above 1 reads their square (a^2) where it read their amount
  (a): declare the threshold in units of the square (`threshold` 4 for
  two rays in phase where 2 was meant).
- **Changed, the escaped momentum per family**: `Ledger.face_momentum`
  is `dict[port, list[list[int]]]` (per family) and `lifetime_momentum`
  `list[list[int]]`; `Ledger.escaped_momentum(family)` is the family's
  own and `escaped_momentum()` the world's total; `face_momentum_total`
  and `lifetime_momentum_total` the sums. `run.json`'s `escaped` line per
  family carries the family's own momentum (until now the world's total
  was written into every line: a reader that summed the lines counted the
  total once per family); the face and border reports (`detectors` in
  `run.json`, `face_detectors()`) carry `momentum` per family beside
  their total. The books' escaped line is the total, unchanged.
- **The API**: `nature_beam.POINTER_UNIT`, `nature_beam.pointer_units`;
  `Ledger.escaped_momentum(family=None)`, `face_momentum_total`,
  `lifetime_momentum_total`.

## The columns of the one coupling, the lifetime, the held content and the contact through the table, on 2026-09-20 (`columns` and `lifetime` per family; `held` per measured event; `columns-v1`; the `contact` record)

The model owner's decision of 2026-09-20 ("one mechanism for all the laws
on the GameBoard", [Highlights 5.4](HIGHLIGHTS.md#54-the-detector); the
physicist's design of the strong force and the mathematician's verified
form, "correct and working"; [BEAM_LAW note 31](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation);
[expectations](TEST_EXPECTATIONS.md#the-columns)). No existing world needs
rewriting: every world of the repository parses to the two built-in
columns and runs the same integer by integer (the 66 example worlds:
`events.jsonl` byte-identical, [validation](VALIDATION.md)).

- **Added, per family**: `columns`, an object of column name to
  `{"value": n or [n, d], "sign": 1 or -1}`. The push is the signed inner
  product over the columns: per column the whole part off the reader's
  clock of V x (the reader's charge in the column) x (the arriving
  family's value), floored on its own. `gravity` is the built-in first
  column of every family (the value [1, 1], the sign minus: the law's
  -M_A V_B) and `charge` the built-in second (the sign plus): the family
  key `charge` stays as the shorthand for the value of the column
  `charge`, and `"columns": {"charge": {"value": v, "sign": 1}}` is an
  optional equivalent spelling (the migration tool does not rewrite it).
  A name's sign is the column's, one per name across the world; a family
  that does not name a column carries [0, 1] there; a paid family's
  values must be 0; at most 8 columns in all; the world's column order is
  gravity, charge, then the names in the order of their first
  declaration.
- **Refused, naming the key**: a column named `gravity`; `charge` declared
  both as the key and under `columns`; `columns.charge` with the sign
  -1; a `sign` other than 1 or -1 (a boolean included); a value with a
  denominator of 0 or a part that is not an integer; a column object with
  other keys or without `sign` or `value`; `columns` that is not an
  object; one name with two signs on two families; a nonzero value on a
  paid family; more than 8 columns; and the parser's static budget: a
  declared reader whose push over a column from the largest release of
  one self-creation of a free family (over the other events' directions,
  read over the reader's Nodes) could pass 2^62 - 1, per column and as
  the sum over the columns. At run time every column's product |V| x
  |E n| is tested by division before it is formed and refused naming the
  measured event and the column ("the push of measured event N at [...]
  exceeds the integer bound ... in the column '...'"), the partial sum
  after every column naming the push; a reader's charge in a column
  beyond 2^62 - 1 (rho x M itself) is refused at the frame naming the
  event and the column (the landed form never formed rho x M alone; a
  world of such a charge was accepted with gravity alone). The charge
  column's product is tested on the reduced pair, so a run the landed
  form refused at |V n_A n_B M_A| may be accepted where the reduced
  |V E n| is within the bound; every accepted integer is the same.
- **The record**: `run.json` carries `columns` (the world's, name and
  sign, in order), per family `columns` (name, value, sign, aligned with
  the world's) beside `charge`, and `columns-v1` under `hypotheses` when
  a column beyond `charge` is declared (after `bohr-v1` when both);
  `state.json` and the measured events' states carry `charges`, the
  charge in every column by name (a reader of the state sees one more
  key per measured event). A measured event's `charge` is the `charge`
  column's pair, the exact rational sum over the families it holds of
  their charge per unit of content times their content (the physicist's
  D-1): for an event of one family rho x its content, as it was; for a
  charged free event that absorbed paid content it is rho times its own
  family's content, where it read rho times the total (no registered
  world has such an event).
- **The API**: `world.Column` (name, value, sign), `FamilyDefinition.columns`
  and `.values`, `world.built_in_columns`, `NatureBeamWorld.columns`,
  `.declared_columns` and `.hypotheses`, `world.COLUMNS_RULE`,
  `world.COLUMN_LIMIT`, `world.event_charges`; `measured.column_charges`,
  `Measured.charges()`, `.column_names`, `.family_values` and
  `.frame_charges`; `nature_beam.push_form(free, moment, charges,
  values, columns, age, entry)` takes the reader's charges per column
  and the arriving family's values in place of the two pairs and the
  content (`push_form(free, moment, content, reader, emitter, age,
  entry)` is gone); `core.integer.reduced` and `rational_sum` (the
  `measured` module re-exports them).
- **Added, per family: `lifetime`** (the model owner, 2026-09-20, "the
  strong force's range is a lifetime, L: the event whose age reaches L
  makes no next event but an escape click in the ledger, as at an open
  face"; [BEAM_LAW note 31](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)
  (vii); [expectations](TEST_EXPECTATIONS.md#the-lifetime-and-the-held-content)):
  an integer L from 1, one scalar; absent, the family lives forever, as
  every family did. A ray of the family whose whole age is at or beyond L
  at the end of the interval's walk (after that interval's reads, before
  the merge) clicks on the border `lifetime`, a detector without Nodes
  listed after the faces: its amount, content and label are booked as an
  open face books an escape and summed into the escaped lines, one
  `click` record per row naming the border (`"detector": "lifetime"`,
  `measured` None, the Node the ray was on). The reach is the flight
  table's: L = 1 the six neighbours, 2 the face diagonals too, 3 the cube
  diagonals and the second Link of a heading.
- **Added, per measured event: `held`** (the physicist's D-1; note 31
  (viii)): an object of family name to content, an integer from 1 each,
  the content the event holds of families other than its own beside its
  `amount`. Its content is the sum, its charge in every column the exact
  rational sum over what it holds, every free family it holds is
  released at the world's rate beside its own, and it counts under the
  owners of every family it holds. The register's proton is
  `{"family": "p", "amount": 1836, "held": {"nuclear": 1}}`.
- **Refused, naming the key**: a `lifetime` that is not an integer from 1
  (0, -1, 1.5, "3"), a list (one integer, a scalar), a lifetime beyond
  the world's `age_bound`; a declared ray in transit whose `age` is at or
  beyond its family's lifetime; a detector named `lifetime` (the border's
  name, as a face's); `held` naming the event's own family or an unknown
  one, a held content that is not an integer from 1, `held` that is not
  an object; and the inverse interval on a GameBoard with a family of a
  lifetime (the border has no inverse, as a face has none), naming the
  family and its lifetime.
- **The record**: `run.json`'s `detectors` carry the border after the
  faces when a family declares a lifetime (`name` "lifetime", `nodes` 0,
  `threshold` 1, per family `measured`, `clicks`, `content`, `record`,
  `measured_content` 0, and `momentum`), the `escaped` lines sum the
  faces and the border, every family carries its `lifetime` (None
  without one), and `hypotheses` carries `columns-v1` when a lifetime is
  declared (the range of a column shares the columns' identity; no third
  identity). `events.jsonl` gains `click` records with `"detector":
  "lifetime"`. The books gain nothing: the border's lines are inside the
  escaped lines (`Ledger.escaped_amount`, `escaped_content`,
  `escaped_momentum` sum the faces and the border; `lifetime_amount`,
  `lifetime_content`, `lifetime_record`, `lifetime_momentum` are the
  border's own). No existing world declares a lifetime or `held`: every
  registered run is unchanged.
- **The API**: `FamilyDefinition.lifetime`, `NatureBeamWorld.lifetimes`,
  `world.LIFETIME_NAME`; `MeasuredDefinition.held` (aligned with the
  families, the own amount under the own family); `NatureBeamSimulation.face_detectors()`
  ends with the border when a family declares a lifetime.
- **The contact through the table** (the model owner, 2026-09-20, on the
  physicist's design of the strong force, section 4.4; [BEAM_LAW note 31](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)
  (ix); [expectations](TEST_EXPECTATIONS.md#the-contact-through-the-table)):
  no key. A body whose step on an axis is refused because the
  destination holds another measured event has arrived at that occupant,
  and the occupant's table entry for the body's family decides as it
  decides for a ray: `measure` hands the body's momentum component on
  that axis to the occupant (the body's 0, the occupant's raised by it,
  the sum of the momenta on the measured events unchanged), `rerelease`
  returns it (the body's component reversed, the occupant's raised by
  twice it), `pass` and a `read` declared against the keys leave the
  step refused and the labels as they were (the behaviour until
  2026-09-20). **Where the entry is the keys' own rule for the body's
  family, declared or not, the contact is `measure`** (a body arriving at
  a body is a paid arrival, its momentum its own label, and the keys' rule
  for a paid arrival is `measure`; `world.CONTACT_DEFAULT`,
  `MeasuredDefinition.contact` per family: the entry's rule where it
  differs from `default_rule`, `measure` otherwise, so that an entry equal
  to the default changes nothing and the migration tool's trimming is
  safe): a world that wants the accumulation as it was declares `pass`
  for the arriving body's family on the occupant (or `read` for a paid
  family), which is the same rule for that family's rays; on a free family
  `read` is the keys' own and the contact stays the hand-over. A body on a
  set of Nodes hands
  the component apportioned whole over the occupants of its destination
  set by their contents (`core.integer.apportion_whole`); an occupant of
  content 0 takes nothing.
- **The record**: `events.jsonl` gains `contact` records (the tick, the
  body's `number`, its `node` and the destination `to`, the `occupant`,
  the body's `family`, the occupant's `rule` for it, the `axis`, the
  signed `component` the occupant gained and the body's `momentum`
  after), one per occupant that took a hand-over, none under `read` or
  `pass`; the measured events' states in `run.json` and `state.json`
  carry `contacts`, the hand-overs taken per family of the arriving body.
- **Which registered runs change**: of the 66 example worlds 60 are
  byte-identical in `events.jsonl` (no body of theirs ever stepped onto
  another); six change from the first refused step of a body on, their
  numbers registered old against new in [validation](VALIDATION.md#the-columns-the-lifetime-the-held-content-and-the-contact-through-the-table-the-66-example-worlds-compared---2026-09-20):
  the coupling `1b_m1`, `1b_m4`, `1b_m16` (the free probe at the Node
  beside its source from tick 31: until now its momentum grew under every
  read, -2 260 249 792 on `1b_m1` at tick 200; now every refused step hands
  the x component to the fixed source, 169 hand-overs, the probe's
  momentum 0), Bohr `r2` and `r4` (the electron beside the proton: `r2`
  now turns twice and leaves through face:+x at tick 688 instead of
  face:-x at tick 254, `r4` leaves at tick 600 instead of 540) and the
  orbit `s8_r12` (one hand-over at tick 174, the angle no longer closing,
  out at tick 260 instead of 271). The registered entries of series C, D
  and H keep the numbers of their date and carry a note. Every world
  without a body arriving at a body, the Bell, slit, detector, redshift,
  Hubble and Heisenberg worlds included, reads the same integer by
  integer.
- **The API**: `world.CONTACT_DEFAULT`, `MeasuredDefinition.contact`,
  `Measured.contact` and `.contacts`, `NatureBeamSimulation._contact`.

## The names NatureBeam and GameBoard and the glossary's single names, on 2026-09-20

The model owner's decisions of 2026-09-20 ([Highlights 5.4](HIGHLIGHTS.md#54-the-detector):
"the ray is to be called NatureBeam in the code everywhere", "DECIDED: the
name of the board is GameBoard", "there is no ray, there is only an event";
[Highlights 5.6](HIGHLIGHTS.md#56-the-glossary-of-the-names-and-how-each-is-computed-2026-09-20),
the 23 redundancies with the one name recommended). A mechanical rename in
three commits; no rule, integer, record key or artifact changed: the whole
suite passes with the same test bodies. The ray is the record of an event in
transit, `NatureBeam` in the code; on the GameBoard there are only events
([the law of the ray](BEAM_LAW.md)).

- **NatureBeam, the law's things in code**: `RayWorld` -> `NatureBeamWorld`,
  `RaySimulation` -> `NatureBeamSimulation`, `RayStore` -> `NatureBeamStore`,
  `RayTables` -> `NatureBeamTables`, `parse_ray_world` ->
  `parse_nature_beam_world`, `execute_ray_run` -> `execute_nature_beam_run`,
  `is_ray_world` -> `is_nature_beam_world`, `ray_tables` ->
  `nature_beam_tables`; the test modules `tests/test_ray_{age, bijection,
  body, books, clock, collision, detector, flight, label, push, readings,
  reemission, window, world_parsing, worlds}.py` ->
  `tests/test_nature_beam_*.py`; `tools/migrate_ray_worlds.py` ->
  `tools/migrate_nature_beam_worlds.py`; the locals `ray`/`rays` ->
  `beam`/`beams`, `fan_ray` -> `fan_beam`, `back_ray` -> `back_beam`,
  `fixed_rays` -> `fixed_beams`, `ray_speed` -> `beam_speed`; the prose
  "ray world" -> "NatureBeam world". Imports of `RaySimulation`,
  `RayWorld` and `parse_ray_world` from `event_universe` or
  `event_universe.events` must use the new names. Unchanged: the refusal
  tables that name the deleted keys (`ray_interactions`, `ray_delay`,
  ...), the dated records of deleted tests, and the word "ray" in prose
  (the owner's reading rule: a ray is the record of an event in transit).
- **The Beam Law** (the model owner, 2026-09-20, the fourth step): the
  law itself is renamed from "the law of the ray" to the Beam Law.
  `docs/RAY_LAW.md` -> [`docs/BEAM_LAW.md`](BEAM_LAW.md) (git mv; its
  title "The Beam Law"; its section headings and note numbers unchanged,
  so every `BEAM_LAW.md#...` anchor is the old one; nothing stays at the
  old path: Highlights, which this rename does not edit, names it in prose
  and links nothing there); every link and mention "RAY_LAW", "the law
  of the ray", "the ray law" -> "BEAM_LAW", "the Beam Law" across the
  documents, skills, README, AGENTS, CONTRIBUTING, examples, tools, tests
  and docstrings (the quoted record title "DECIDED: the law of the ray"
  and the history sections of this file and of the changelog keep their
  wording; the anchors of the retitled headings of TERMINOLOGY,
  EXPERIMENTS and TEST_EXPECTATIONS follow their new titles). The law's
  identity: `RAYS_LAW = "rays-v1"` -> `BEAM_LAW = "beam-v1"`
  (`events.world`, re-exported by `event_universe` and
  `event_universe.events`; `run.json` and `state.json` record `"law":
  "beam-v1"`); the world key `"law": "rays"` -> `"law": "beam"`
  (`LAW_VALUE`), every world file in the repository rewritten by
  `tools/migrate_nature_beam_worlds.py` (extended: `rays` -> `beam`; the
  old name, `world.OLD_LAW_VALUE`, is accepted by the tool alone), the
  parser refusing `"law": "rays"` naming this section (no implicit
  default; `tests/test_nature_beam_world_parsing.py` (a)), the
  preflight's kind `rays` -> `beam` (`DOCUMENT_KINDS`, `--kind beam`,
  `report.kind`); the run records of the registered runs stay as they
  were: rays-v1 is beam-v1, the same law; the hypothesis identities
  (`bohr-v1` and the ones in flight) are untouched. The prose word "ray"
  for the law's event in transit stays allowed as the informal name; the
  documents' first mentions say "beam (the record of an event in
  transit)"; no mass replacement of "ray" in prose.
- **GameBoard**: `src/event_universe/core/lattice.py` ->
  `src/event_universe/core/game_board.py` (imports of
  `event_universe.core.lattice` must become
  `event_universe.core.game_board`; `Address3`, `Heading`, `MAX_VALUE`,
  `PORT_HEADINGS` and `adjacent_node` unchanged); the `grid` local of
  `shell_readings` -> `node_offsets`; the test helpers `board(simulation)`
  -> `game_board(simulation)` and the test names
  `test_the_board_is_unchanged_*` -> `test_the_game_board_is_unchanged_*`,
  `*_respect_the_board_symmetries` -> `*_respect_the_game_board_symmetries`;
  in `tools/derivations_round7.py` `board_hist`, `hist_board`,
  `board_over_q`, `final_board_over_q`, `board_samples`,
  `board_over_q_samples`, `on_board` and the result key `"board"` ->
  `game_board_hist`, `hist_game_board`, `game_board_over_q`,
  `final_game_board_over_q`, `game_board_samples`,
  `game_board_over_q_samples`, `on_game_board`, `"game_board"`; the
  refusals and messages "is outside the board" -> "is outside the
  GameBoard", "a closed board is refused" -> "a closed GameBoard is
  refused", "leaves the board through an open face" -> "leaves the
  GameBoard through an open face", "age_bound is required on a board
  periodic on every axis" -> "... on a GameBoard periodic ...", "adjacency
  requires an in-board integer position" -> "adjacency requires an integer
  position on the GameBoard", "cube_flux supports only the all-open board"
  -> "... the all-open GameBoard", "(declare a larger age_bound or a
  smaller board)" -> "(... or a smaller GameBoard)", "the inverse interval
  is defined on a board without measured events" -> "... on a GameBoard
  ..." (a reader matching the old text must match the new); the prose
  "the board", "the game board", "the lattice", "the grid" -> "the
  GameBoard" in every document, README, skill, example README and
  docstring, with the two anchors `#per-axis-board-topology-...` ->
  `#per-axis-gameboard-topology-...` ([ENGINE](ENGINE.md)) and
  `#13-what-the-lattice-says-...` -> `#13-what-the-gameboard-says-...`
  ([DERIVATIONS](DERIVATIONS.md)) and the headings "Events board topology"
  of POSTULATES.md and SIMULATOR_DEFINITIONS.md -> "GameBoard topology";
  the canonical entry in [TERMINOLOGY](TERMINOLOGY.md) and the rule in
  AGENTS.md. What stays: a "board" that is not the GameBoard ("on-board
  information retention"), the drawing's grid spacing, the CSS layout
  grids, the integer encoding grid, a numerical evaluation grid and a
  parameter scan grid, `KeyboardInterrupt`, and "cubic lattice of Nodes"
  inside the definition only. The world key `shape` is unchanged.
- **The glossary's single names (Highlights 5.6), in code**: (1)
  `Reading.scalar` -> `Moments.presence`, `Readings.count` ->
  `GameBoardDiagnostics.arrived`, `NatureBeamSimulation.count` ->
  `NatureBeamSimulation.arrived`, the key `count` of `shell_readings` ->
  `arrived`; (2) `Reading.vector` -> `Moments.flow`, the label moment V is
  "the label flow" (`test_the_expected_push_is_the_engines_label_moment`
  -> `..._label_flow`); (3) the pointer (X, Y) is "the pointer" where the
  documents said "the coherent sum" or "the coherent reading" of the
  detector's record (the owner's "the Node holds no coherent sum" is kept
  as said); (4) `nature_beam.HERE` -> `NO_ARRIVAL` (the arrival code; the
  rest directions keep the indices 0 and 1, the reading keeps `here`); (5)
  the state is `owed` (TERMINOLOGY: "Suspension, owed", "Owed (the
  count)"); (7) `configuration_validation.KINDS` -> `DOCUMENT_KINDS`; (9)
  "Interval (tick)" defined once in TERMINOLOGY (`tick` in every key and
  identifier, "interval" the prose noun); (10) `FlightTable.turns` ->
  `FlightTable.resolution` (T_d), `Measured.phase_steps` ->
  `Measured.turned` (the cumulative turn; `NatureBeamWorld.phase_steps` is
  N and unchanged); (11) `RayWorld.clock` -> `NatureBeamWorld.K` (the
  parser's parameter too); (12) "Extent (of a detector)" in TERMINOLOGY,
  the phase window is "the window", the suspension's fraction is "the
  rate"; (13) "Carried" documented once in TERMINOLOGY as `amount x
  content` (the column `mass` was already gone with charge per unit of
  content, 2026-09-20); (14) `Ledger.face_units` -> `Ledger.face_amount`,
  `Ledger.escaped_units` -> `Ledger.escaped_amount`, "the transit line (in
  amount)"; (15) `Measured.events` -> `Measured.clicks`; (18)
  `Measured.measured` -> `Measured.taken` (the tally by rule;
  `NatureBeamSimulation.measured` and the world's `measured` list
  unchanged); (19) `measured.RULES` -> `measured.TALLIES`; (20)
  `nature_beam.Reading` -> `nature_beam.Moments`, `nature_beam.Readings`
  -> `nature_beam.GameBoardDiagnostics`. Nothing to change for (8)
  `heading` (used only for the six unit vectors), (21) `push_form` (the
  function exists since the push as one product; the documents are
  right), (22) the leftovers (the refusal tables stay, naming the law in
  the refusal).
- **Deferred, the keys the register's worlds and fingerprints depend on**
  (not changed; each a world-file or run-record key, to be migrated with a
  rewrite of the worlds and a dated note): (1) `reads: "scalar"` ->
  `"presence"` and `"outside"` -> `"arrived"`; (2) `reads: "vector"` ->
  `"flow"`; (6) `push` on a `click` line -> `momentum`; (13) the
  measured-event key `amount` -> `content`; (16) `position` -> `node` in
  `state.json`, in `run.json` `numbers` and in the world; (17) `run.json`
  `model` -> `model_id`; (18) the event line's `measured` -> `reader` and
  `number` -> `emitter`; (20) the record field `reading` -> `component`;
  (10), (15), (18) the keys `phase_steps`, `events` and `measured` of
  `Measured.state()` (their attributes are `turned`, `clicks` and
  `taken`); (23) refusing a detector named as a face (`face:*`) is a
  behaviour change with a test of its own, not made here.

## The turn by momentum, Bohr as parameters outside the board, on 2026-09-20 (`action`, `phase_by_momentum`; `bohr-v1`)

The model owner's decision of 2026-09-20 ("On Bohr, go, and put it as
parameters outside the board like the age"; [Highlights 5.4](HIGHLIGHTS.md#54-the-detector);
[RAY_LAW note 30 (ii)](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation);
[expectations](TEST_EXPECTATIONS.md#a-body-on-a-set-and-the-turn-by-momentum)).

- **Added**: the world key `action` (h, an integer from 1, in the units
  of the momentum label times Links; absent by default) and the
  measured-event key `phase_by_momentum` (true; false by default): at the
  Link a body steps on an axis whose momentum component is p its phase
  turns by `by_clock(k0, |p| x N, h)`, k0 the count of Links the step
  rule gives on that axis at its age before the self-creation (the
  difference of two floors of k x |p| x N / h; no register, no
  remainder); the axes compose. A rule of the measured event, the
  external thing (`RaySimulation._move`); the rays' flight and collision
  are untouched; without `action` nothing turns and every world reads
  the same integer by integer (`tests/test_ray_body.py` (e)).
- **Refused, naming the key**: `action` below 1 or not an integer;
  `phase_by_momentum` without `action`, on a `fixed` measured event, on
  a family without a phase circle, or not a boolean; a turning body whose
  `ticks x |p| x N` exceeds 2^62 - 1 for its declared momentum (the
  count of Links within the run is at most `ticks`); at run time the
  product (k0 + 1) x |p| x N beyond the bound (`OverflowError` naming the
  body and "turn by momentum").
- **The record**: `run.json` carries `action` (h, or None) and
  `hypotheses` (`["bohr-v1"]` when `action` is declared, the identity of
  the turn by momentum as a physical hypothesis beside the law, whose
  identity stays `rays-v1`; `[]` otherwise) and per measured event under
  `numbers` its `phase_by_momentum`; the `step` line of `events.jsonl`
  gains `phase`, the measured event's phase after the step (a reader that
  compared step lines whole sees one more key on every stepping world;
  the integers are unchanged).
- **The tools**: `tools/bohr_readings.py` reads series H (the orbit from
  the step lines, the phase per turn, the coherent record of the face
  detectors from the click lines through the engine's own
  `coherent_pointer`); the worlds are `examples/events/bohr/`.

## A body on a set of Nodes with one record, on 2026-09-20 (`span`)

The model owner's decision of 2026-09-20 on Bohr ("go, and put it as
parameters outside the board like the age"; the body on a set taken with
it as the condition for a closed orbit, the physicist's proposal 1, "the
electron of width 3"; [RAY_LAW note 30](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation);
[expectations](TEST_EXPECTATIONS.md#a-body-on-a-set-and-the-turn-by-momentum)).

- **Added**: the measured-event key `span`, three odd integers from 1
  (`[1, 1, 1]` by default): the measured event is a body on the block of
  Nodes centred on its `position`, one record on all of them; its
  threshold, its clock's count and its push read the one reading set
  summed over its Nodes; its releases are apportioned whole over its
  Nodes; the step moves the whole set as one; no collision acts at any of
  its Nodes; a detector names it by its `position`. `world.body_nodes`,
  `Measured.span`, `Measured.nodes`, `RaySimulation.at` over every Node of
  every body; `engine.step_axis` and `engine.count_owed`, the step rule of
  one axis and the owed count as public functions the methods call (the
  readings tools read them; no integer changes).
- **Refused, naming the key**: a `span` that is not three odd integers
  from 1 or larger than its axis; a body whose Nodes leave the board on an
  open axis at the start; two measured events sharing a Node; a detector
  naming a Node of a body that is not its `position`.
- **The record**: `run.json` carries `span` per measured event under
  `numbers` and in the measured events' states, `state.json` the same key
  (a reader of the state sees one more key per measured event, `[1, 1,
  1]` on every world that declares none). Every world without the key
  reads the same integer by integer (`tests/test_ray_body.py` (a): every
  record, row and state equal with the key absent and with `[1, 1, 1]`
  declared).

## `wave` is the default reading of a detector, on 2026-09-20

The model owner's decision of 2026-09-20 ("on the board a ray, in the world
a wave"; [RAY_LAW section 5](BEAM_LAW.md#5-the-detectors-record-the-re-emission-the-face-detectors)
and note 29): `world.DETECTOR_READINGS` is `("wave", "beam")`, so a
detector without a `reading` key, and every measured event outside a
declared detector, reads `wave` (the coherent pointer over the set, its
square the record, the window reading the set's phase); a world that wants
the pairing rule declares `"reading": "beam"`. A world whose detector
declared no reading and was met by rays of different phases in one
interval (a windowed counter, a wall) reads differently: `tests/
test_ray_readings.py` (d) is re-pinned, `tests/test_ray_collision.py` (d)
declares `beam`. The Bell worlds are unchanged (one ray per interval per
counter: S = 2, 326 criteria), the two-slit screens and the Heisenberg
worlds declare their reading, series C and D have no detector; the
two-slit wall records the square of what it absorbs.

## Charge per unit of content, on 2026-09-20 (the family's `charge` a pair; no `charge` on a measured event; the record's two columns gone)

The model owner's decision of 2026-09-20 (Highlights 5.4: charge is per
unit of content of a family, and the push one product;
[RAY_LAW section 2](BEAM_LAW.md#2-the-record-of-a-ray-and-the-world-file),
step 4 and note 28; [validation](VALIDATION.md)). What a user of the engine
must know:

- **The family key `charge` is the charge per unit of content**, rho, an
  integer c (the pair `[c, 1]`) or a pair `[n, d]` with d from 1, as
  `suspension` is declared; a denominator of 0 or a part that is not an
  integer is refused naming the key. A measured event's charge is rho
  times its content. **The key `charge` on a measured event is refused**
  naming this entry: a world that gave two events of one family different
  whole charges on different contents (the series 7 worlds: 2^23 on 2^24
  and 2 on 1) must split them into two families, one charge per unit of
  content per family (`examples/events/coupling/make_worlds.py`: `q` the
  source with `charge` [1, 2], `p` the probe with [2, 1]; [1, 2] on the
  content-4 probe of `7_pp_m4`). `tools/migrate_ray_worlds.py` moves a
  per-event `charge` to its family as the reduced pair and refuses a
  family whose events imply two pairs, naming both events.
- **The push is one product per arriving free ray**, `push_A = M_A x (rho_A
  rho_B - 1) x V_B` (`nature_beam.push_form`), the electric part off the
  reader's clock by the declared pairs, `sign x by_clock(age_A, |V n_A n_B
  M_A|, d_A d_B)`: equal integer by integer to the earlier `sign x
  by_clock(age_A, |V q_A q_B|, M_B)` wherever q_A = rho_A M_A and q_B =
  rho_B M_B were integers, so every registered reading is unchanged
  (series 7's 181 or 185 `read` records per world, `pushed` and the
  momenta equal on all six worlds). M_A is the content the frame read at
  the start of the interval (`Measured.frame_content`; the architect's
  B3): a click of the interval pushes from the next interval on.
- **The record's columns**: `NatureBeam`, the store and `state.json` lose
  `charge` and `mass` (the emitter's charge and content at birth of the
  night of 2026-09-19); a row of `state.json` is `direction`, `age`,
  `phase`, `number`, `amount`, `content`; `RayStore.append` takes the
  seven columns with `arrival`; the merge's identity is the six fields
  node, direction, age, phase, number, content. A re-emitted free ray
  keeps its family and takes the re-emitter's number (the orchestrator's
  D2), so it pushes by its family's rho; the architect's B2 (a division
  by the re-emitter's held content of another family, 0) cannot arise.
- **The records**: `run.json`'s `families[].charge` is the pair `[n, d]`;
  `measured[].charge` in `run.json` and `state.json` is the pair rho x
  content, reduced (was an integer); the books' `charge` line is the
  exact rational sum of the measured events' charges as a reduced pair
  `[n, d]` (was an integer). `Measured.charge` is a property (the pair);
  `Measured.rho` the family's pair; `MeasuredDefinition` has no `charge`.
- **Names**: `FACE_NAMES` lives in `events/world.py` (the schema refuses a
  detector named as a face is); `engine.by_clock` and `engine.FACE_NAMES`
  re-exports are gone: import `by_clock` from `core.integer` and
  `FACE_NAMES` from `events.world`.
- **Tests**: `test_ray_push` (a) to (e), (i) re-fixtured on two free
  families with the same integers; (k) the re-emitted ray, (l) the
  equivalence principle for the electric push; `test_ray_world_parsing`
  (a) the refusals; `test_default_table` (c); `test_ray_bijection` (the
  rows of seven fields).

## The age of a ray kept whole and read by the measured event, on 2026-09-20

The model owner's "go for it" of 2026-09-19 on the clock beside a mass
([Highlights 5.4](HIGHLIGHTS.md#54-the-detector); [RAY_LAW section 10](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation),
note 25; [validation](VALIDATION.md)): the clock's count may read the
amount-weighted age of the rays at its Node, M / r in space, while the
push keeps the flow, M / r^2.

- **The age is no longer reduced modulo the direction's period.**
  `RayStore.age` and the `age` of every row in `state.json` are the whole
  count of intervals since the ray's birth or re-emission; the flight
  reads `age mod L_d` (`flight.steps[direction, age % period[direction]]`)
  and the board's step is unchanged. A reader of `state.json` that
  compared ages modulo the period must compare them whole. The seeding of
  a declared ray no longer reduces its `age`.
- **The store's rows.** Rows of different ages no longer merge: the
  store's bound is `len(D) x age_bound x N x numbers x contents` in place
  of `sum_d L_d x N x numbers x contents` (the host cost); on the
  registered worlds the row counts are unchanged in practice.
- **Added**: the world key `age_bound` (an integer from 1; by default
  twice `world.flight_bound(shape, D)` on a board with an open axis;
  required on a board periodic on every axis, refused if absent), recorded
  in `run.json`; a declared `in_transit[].age` beyond it is refused; a row
  whose age passes it refuses the run with `OverflowError` naming the key
  (the world must be small enough or declare its bound). **Worlds periodic
  on every axis must now declare `age_bound`** (the test worlds of the
  bijection, the flight, the collision and the push do); every other
  registered world parses and runs as before.
- **Added**: the value `age` of a table entry's `reads`; `Reading.age`,
  `Reading.age_outside`, `Reading.age_here` and the `ages` argument of
  `read_arrivals` (zero without it; `moment_table`, `reading_of`,
  `moment_bound`); `measured.count_component`; `Measured.counted` (what
  the clock counts; `Measured.presence` stays the presence); the constant
  `Q` of the flight table now lives in `world.py` (`nature_beam.Q` is the
  same object).
- **Changed**: `RaySimulation._suspend` owes `by_clock(age, counted x n,
  d)`; with no entry reading `age` this is the presence, integer by
  integer, so every world without the key reads the same. The inverse walk
  of a ray at age 0 is refused (its birth has no inverse).
## The label along the unit vector of the direction, on 2026-09-19 (the momentum units change by Q = 64)

The model owner's decision of 2026-09-19 (Highlights 5.4, "go for it") on
the physics-rule reviewer's verdict on the magnitude of a fan ray's label
([RAY_LAW section 2](BEAM_LAW.md#2-the-record-of-a-ray-and-the-world-file)
and note 23; [validation](VALIDATION.md)): the momentum label of a unit is
along the unit vector u_d of its direction at the flight table's scale,
the integer vector nearest Q D / |D| with Q = 64 (`nature_beam.unit_label`,
the flight table's `labels`; exactly Q e_d on a heading), in place of the
integer direction D itself. What a user of the engine must know:

- **The momentum units change by Q.** Every declared `momentum` in a world
  file and every momentum in `run.json`, `state.json` and `events.jsonl`
  (`momentum`, `push`, `pushed`, the momentum lines of the books, the
  face detectors' `momentum`, the `step` records) is now in label units:
  x 64 for a heading (the label of one unit of amount along +X is
  (64, 0, 0), of one unit of content 8 along +X (512, 0, 0)) and the
  unit vector's components for a fan direction (one unit along (7, 5, 0)
  carries (52, 37, 0), not (7, 5, 0)). A world that declared `momentum`
  [0, 23, 0] meaning 23 units of momentum now declares [0, 1472, 0]; a
  reader of the record divides by 64 to recover the old units of a
  heading. The zeroth moment of the reading (the count, the presence,
  the threshold, the clock's count), the amounts, the contents, the
  phases, the record and Gauss's flux off the Port crossings
  (`per_port`, `cube_flux`) are unchanged.
- **The step rule carries Q**: `by_clock(age, |p|, Q x S x M + |p|)` in
  place of `S x M + |p|` (`RaySimulation._move`), so a declared momentum
  x 64 steps exactly as before (`by_clock(age, Q n, Q k) = by_clock(age,
  n, k)`); a world whose `momentum` was not rescaled steps 64 times
  slower.
- **The bound**: the parser refuses a declared ray, a free release or a
  lamp's release with `Q x content x amount` beyond 2^62 - 1 (content x
  amount at most 2^56 - 1 per row), naming the numbers, and
  `label_weights` refuses the same at every product the law forms (a
  free family's rows included); on the six headings the bound tightens
  from 2^62 to 2^56 per row, on the default direction bound it is the
  same number as before. The reading's second-moment bound, amount x
  Q^2 x rows, refuses a set of one number above 2^50 units at a measured
  event's Node (a row of 2^52 at a detector, once a test fixture, is
  refused; 2^49 is not).
- **The reading's vector and tensor moments** are taken on u_d (`Readings`,
  the reading at a measured event, `shell_readings`' flow): a fan's flow
  reads Q x q direction-blind, a heading's Q x q; a `reads` component
  `vector` or `tensor` on a record is x 64 and x 4096.
- **The tools**: `tools/coupling_readings.py` divides the labels by Q
  where it compares with the emission q or an amount (the registered
  expectations of RAY_LAW section 8 keep their meaning; every criterion
  and reading is the same as registered); `tools/orbit_readings.py`
  reads C against m q L / (2 pi r) with the push in units of Q and L the
  fan's mean |u_d| / Q (1.0000); `examples/events/orbit/make_worlds.py`
  derives p in units of one free unit's label (Q x m) and declares
  `momentum` = p x 64 (192, 320, 576 at S = 1, 8, 32).
- **Names**: `world.LABEL_SCALE` (= `nature_beam.Q`), `nature_beam.unit_label`,
  `FlightTable.labels`, `nature_beam.first_moment_overflow`;
  `momentum_labels` and `RayStore.labels` take the unit-vector table in
  place of the direction vectors; `first_label_overflow` takes `free`.
- **Tests**: every momentum integer of the pinned tests is x 64 (the fan
  fixtures on u_d), the bound-edge worlds of `test_ray_world_parsing`
  (d) are at 1/64 of their amounts, `test_ray_label.py` is new;
  [TEST_EXPECTATIONS](TEST_EXPECTATIONS.md) lists every re-pin.
## The detector as a set with one record, the reading key and the phase returned, on 2026-09-19

The model owner's three decisions of 2026-09-19 ([RAY_LAW section 5](BEAM_LAW.md#5-the-detectors-record-the-re-emission-the-face-detectors),
note 24; [changelog](../CHANGELOG.md)): a detector is a set of Nodes with
ONE record; after a click the set's phase is returned to its measured
events; a detector declares its `reading`, `beam` (the default) or `wave`.

- **Removed**: `Measured.record` (the record per Node) and the `record`
  key of a measured event's state in `run.json` (`measured[]`) and
  `state.json`; the per-Node threshold field of `Measured` (`threshold`
  is now a property of the set's).
- **Added**: `events.measured.DetectorSet` (index, name, reading,
  threshold, numbers, record per family, phase per family) and
  `RaySimulation.detector_sets` (the declared detectors first, then a
  detector of one Node per measured event outside them);
  `Measured.detector_set`; `DetectorDefinition.reading` and the world key
  `detectors[].reading` (`world.DETECTOR_READINGS`, refused outside
  `beam` and `wave`); `nature_beam.pointer_phases` and
  `POINTER_STEP_BOUND`; `FamilyPlan.count`, `set_phase`, `cancelled`
  (`pointer` now keyed by the set).
- **The record's form**: the run's `detectors[]` carry `reading` and per
  family `phase` beside the one `record`; the `record` line of
  `events.jsonl` is one per detector set per family per interval, its
  `node` and `measured` None for a set of several Nodes, with `phase`
  (the set's) and, under `wave` only, `pointer`; a `pass` line of a
  paired ray under `beam` carries `cancelled` true and neither `window`
  nor `threshold`; the `click` line keeps the ray's own `phase`.
- **Worlds**: a detector that relied on the squared record must declare
  `"reading": "wave"` (the default `beam` counts and pairs); the
  two-slit worlds declare their screen as 121 one-Node `wave` detectors
  `screen_<y>` (one detector of 121 Nodes would read one record with no
  resolution in y). The Bell worlds need no change: one ray per interval
  per detector reads the same under `beam`, the `record` lines carrying
  the count instead of the square. The detector definitions of
  `examples/events/detector/` read `beam` by default (their registered
  runs of the square are history). A measured event outside every
  detector counts (the two-slit wall).
- **Tests**: `test_ray_detector` (a), (b), (e) declare `wave`; (f), (g),
  (h) are new; `test_ray_readings` (d) reads the `record` line's phase;
  `test_ray_worlds` (a) reads the record per pixel from the detector
  sets.

## The detector's record exact, never refused, on 2026-09-19 (after the batching)

The night's affordable amount refused `examples/events/two_contents.json`
at its 20th interval (262144 units on `face:+y` in one interval, above
261123), a world that had run 200 intervals before the bound; a report
of the host is exact and is neither refused nor wrapped
([RAY_LAW section 5](BEAM_LAW.md#5-the-detectors-record-the-re-emission-the-face-detectors),
note 19; [validation](VALIDATION.md)).

- **Deleted**: `nature_beam.RECORD_AMOUNT_BOUND`, `check_record_amount`,
  `record_amount` and the refusal "the amount ... clicked at ... exceeds
  the affordable amount"; the `record` line of `events.jsonl` and the
  detectors' reports are unchanged in form.
- **Added**: `nature_beam.POINTER_AMOUNT_BOUND` = (2^62 - 1) // (32 x 257)
  = 560759486676481, the clicked amount up to which the coherent pointer
  is summed in the int64 register, and `nature_beam.coherent_pointer`,
  the pointer per group of clicked rows, in the register within the bound
  and in Python integers beyond it; `FamilyPlan.pointer` holds (X, Y).
- **The record's value**: `Measured.record` and `Ledger.face_record` are
  exact Python integers with no bound; the `record` of `run.json` (the
  detectors' reports) and of `state.json` (the measured events) can
  exceed 2^63. A reader must parse it as an arbitrary-precision integer
  (Python's `json` does; a reader that loads it into int64 must not).
- **Worlds**: every world that ran before runs byte for byte the same;
  a world the bound refused now completes.

## The push as one form, the one label and the affordable amount, on 2026-09-19 (the night)

The physics-rule review of the law of the ray (its findings F1, F2, F3, F7)
and the model owner's proposal 2 ("2 with the physicist"), implemented on
the branch `claude/universe24-new-3ytqde` ([RAY_LAW section 10](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation),
notes 18 to 21). Nothing physical changes on the registered runs (the
series C, series 7 and Bell records are identical byte for byte,
[validation](VALIDATION.md)); what changes is where the momentum is read
and what the record carries.

- **The record of a free family's ray gains two columns**, `charge` and
  `mass` (the emitter's charge and its held content of the family at the
  ray's birth, the factor of the electric push), on `NatureBeam`, in the
  store (`RayStore.append` requires them; the merge compares them) and in
  `state.json` (on a free family's rows only). A paid family's rows carry
  0 and 0. A declared ray in transit of a free family takes the charge and
  the declared amount of the measured event its number names.
- **The lookup of the emitter by number is deleted**: `push_of` (the three
  branches and `world.measured[number - 1]`) is replaced by `push_form`,
  the one bilinear form over the arriving rays; `RayWorld.content_lcm` and
  the refusal "the charged events' denominator exceeds the bounded integer"
  are gone (no lcm: the electric part is `sign x by_clock(age_A, |V q_A
  q_B|, M_B)` per emitter factor, equal integer by integer to the lcm
  form).
- **No collision at a Node that holds a measured event** (`nature_beam`
  step 3, forward and inverse). A world in which rays of one number met
  head-on exactly at a measured event's Node collided there before; now
  they meet the table with their directions as they arrived.
- **The one label**: the click's momentum, the face click's, the recoil of
  a release and of a re-emission and the transit line are all
  `momentum_labels` (`RayStore.labels` calls it); the `home` record's
  `push` is the labels' sum of what came home for a paid family (was
  `[0, 0, 0]`), and the emitter's momentum takes it in at the home and
  gives it back at the re-creation.
- **The affordable amount**: `RECORD_AMOUNT_BOUND` (261123) bounds the
  amount a detector Node or a face clicks of one family in one interval;
  a larger set refuses the run with `OverflowError` naming the Node or the
  face and the sum (before, the record's int64 products wrapped silently
  beyond 2^50). Every reduction of the law is exact (`exact_sum`,
  `exact_column_sums`; the merged amounts; `label_weights` checked before
  its product).
- **Tests**: `tests/test_ray_push.py` (new: the form, the sign, the
  cancellation, the fractional floor, a paid emitter, a fan emitter, the
  one label), `test_ray_collision.py` (d), `test_ray_detector.py` (e).
- **Series D** is re-registered under this engine with the momenta
  re-derived for the label's magnitude (`examples/events/orbit/`, p = 11,
  15, 23 in place of 3, 5, 9; `tools/orbit_readings.py` measures C
  against m q L / (2 pi r), L the fan's mean |D|).

## The ray is NatureBeam, on 2026-09-19 (the night)

The model owner renamed the ray's record and its one function: the record
`GonenBeam` is `NatureBeam`, the function `gonen_beam` is `nature_beam`, and
the module `src/event_universe/events/gonen_beam.py` is `nature_beam.py`. A
mechanical rename of every token in the code, the tests, the tools and the
documents; no rule, integer, record or artifact changed. Highlights 5.4 keeps
the earlier name in its record of the day. Imports of
`event_universe.events.gonen_beam` must become
`event_universe.events.nature_beam`.

## The table from the keys and the moments, on 2026-09-19 (the night)

The model owner's decisions of the night of 2026-09-19 (Highlights 5.4, on
the mathematician's review of the table of the physical entities: "I
approve 1 and 3"; [RAY_LAW section 10](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation),
notes 15 and 16): generic replaces generic, nothing physical changes on the
six headings.

- **`kind` is removed from the family schema.** A family declares its
  `quantum` (now required): 0 is a free family (matter; its release costs
  nothing, its rays carry no content, its label is `amount x D`, it is read
  for gravity and electricity, it may carry a `charge`), 1 or more a paid
  one (light; released by a lamp at the cost `quantum` x turn per unit, a
  click measures it, no charge). `"kind": "free"` becomes `"quantum": 0`
  and `"kind": "paid"` becomes `"quantum": 1` (or the declared quantum);
  a world that still declares `kind` is refused naming this entry, since
  the owner's rule is one canonical form. `FamilyDefinition.kind` is gone,
  `FamilyDefinition.free` is `quantum == 0`, `FamilyDefinition.unit_label`
  is the content one declared unit carries for its label (1 for a free
  family); `world.KINDS` is gone; `RayStore.labels(rows, vectors, free)`
  takes no quantum. `run.json` carries `quantum` per family and no `kind`.
- **The table is generated from the keys.** `world.default_table(families)`
  gives every measured event its table: `read` for a free family, `measure`
  for a paid one, no window, the rule's component (`vector` on `read`,
  `scalar` otherwise). A declared `table` overrides only the entries it
  names; every entry that equals the default is optional (still accepted;
  it changes nothing) and the object form may omit `rule`, so a window
  alone (`{"light": {"phase_window": 32}}`) is a lawful entry. The shipped
  worlds were rewritten to declare only what differs by
  `tools/migrate_ray_worlds.py` (which also converts `kind`; run it on
  your own worlds: `PYTHONPATH=src python tools/migrate_ray_worlds.py
  WORLD.json`); the Bell and coupling generators emit the trimmed form.
  Every example world parses to the same `RayWorld` as before, and the
  Bell and coupling runs are unchanged record by record
  ([validation](VALIDATION.md)).
- **The one reading is the moments.** `read_arrivals(vectors, amounts,
  keys=None, size=None)` replaces `read_arrivals(slots)`: it takes the
  amount-weighted moments of order 0, 1 and 2 of the arrivals' direction
  vectors (the count split outside / here, the net flow `sum amount x D`,
  the traceless tensor `3 x sum amount x D (x) D - tr I`, exact integers)
  in place of the decomposition of the seven Port slots over an orthogonal
  basis; `READING_BASIS`, `READING_SLOTS` and the seven-slot form are gone;
  `Reading.tensor` is a symmetric traceless 3 x 3 integer matrix (was two
  components; the old pair is `-T_zz` and `(T_xx - T_yy) / 3`), so a
  record with `"reads": "tensor"` carries three rows of three integers;
  `Reading.second` holds the six entries of the second moment. The store's
  `port` column is `arrival` (the direction the ray arrived on this
  interval, `HERE` = 0, the first rest direction, for a ray that did not
  step); `Readings.per_port` is (nodes, 6), the amount that crossed into
  each Node through each Port this interval, a diagnostic of the walk that
  `cube_flux` and `tools/coupling_readings.py` read for Gauss's flux. On
  the six headings every reading is unchanged; on a fan a ray enters the
  reading with its own vector `D[direction]` instead of the unit Link of
  its last step, so the push a measured event takes from a fan ray is its
  label (the two-slit worlds' wall momentum changes; their screen record
  still fringes, `tests/test_ray_worlds.py` (a)). A reading whose second
  moment could pass 2^62 - 1 is refused with `OverflowError`.
- **Tests.** `test_ray_readings.py` (a) re-pinned on the moments;
  `test_default_table.py` new; every test world declares `quantum` in
  place of `kind`.

## The law of the ray, on 2026-09-19 (`rays-v1`)

The model owner's decision of 2026-09-19 (Highlights 5.4, "DECIDED: the law
of the ray"; the design [the law of the ray](BEAM_LAW.md), published before
the engine changed): the Node holds no wave; a unit is a ray with a record
on the digital line of its momentum at one speed, 1 / sqrt 3; rays that meet
are permuted by the collision table; the interval is a bijection and the
click its only one-way border; the ray's law is one generic function,
`nature_beam`, and every piece of logic exists once. The engine of the law of
events (`events-v1`, the evening of the same day) is deleted with everything
it computed at the Node. Base `ce0b22af` (the merge of the three reversible
corrections into `claude/universe24-new-3ytqde`); the last commit holding
`events-v1` is that one.

- **The law selected.** `"law": "rays"` selects `rays-v1`; `run.json`
  carries `"law": "rays-v1"`; `configuration_validation` reports the kind
  `rays`. `"law": "events"` is refused naming the law of the ray and this
  entry. The package is `event_universe` 0.3.1 (its `__version__` string
  read 0.3.0 until the cleanup of the same day, below).
- **Deleted modules.** `src/event_universe/events/mixing.py` (the coherent
  sum, `coherent_weights`, `diagonal_weights`, `mix_arrivals`,
  `place_departures`, `apportion_carried`, `tie_order`; `integer_root` and
  `apportion_whole` move to `core/integer.py`, `by_clock` joins them);
  `src/event_universe/events/transit.py` (the per-Port arrays, `receive`,
  `suspend`, `cycle`, `sizes`, `phase_at`, `nearest_step`, `step_window`,
  `frozen`, `take`, `place`, `walk`: the suspension of transit bundles is
  deleted, a ray never waits, the seventh exit is the rest slot of the
  collision, a measured event's delay is the owed count off its clock);
  `src/event_universe/events/reversible.py` and the `reversible-detector-v1`
  candidate (the `dynamics` key, `port_map`, `output`, `capacity`,
  `reference_phase`, `groups`, `max_active_owners`, `_validate_reversible_world`,
  `_reversible_*` and `_pointer` in `engine.py`, `detector_readouts`; its
  pointer is the detector's record, its `transduce` the re-emission on
  declared directions, its refusal of an open face the face detector); in
  `engine.py` the coherent phase read in `_meet`, `EMISSION_CELL_BOUND` and
  `EMISSION_MARGIN` (no cell). Nothing of these is re-exported.
- **New modules.** `src/event_universe/events/nature_beam.py` (`NatureBeam`,
  `read_arrivals` and `READING_BASIS`, `flight_table`, `collision_table`,
  `ray_tables`, `RayStore`, `nature_beam`, `bounded`, `segment_sums`);
  `src/event_universe/events/measured.py` (`Measured`, `Ledger`, `RULES`,
  `FACE_NAMES`); `engine.py` and `world.py` rewritten in place.
- **Renames.** `EVENTS_LAW` -> `RAYS_LAW` ("rays-v1"); `EventWorld` ->
  `RayWorld`; `parse_event_world` -> `parse_ray_world`; `is_event_world` ->
  `is_ray_world`; `EventSimulation` -> `RaySimulation`; `execute_event_run`
  -> `execute_ray_run`; `Transit.walk` -> the walk inside `nature_beam`;
  `world.EMISSION_CELL_BOUND` -> gone (`world.MOMENTUM_BOUND`,
  `world.AMOUNT_BOUND` 2^62 - 1 remain).
- **The world file.** Added: `directions` and `direction_bound` at the
  world, `phase_per_link` per family, `directions` per measured event, the
  lamp's `directions` (in place of `headings`), a table entry's `reads`
  (`scalar`, `outside`, `here`, `vector`, `tensor`), a ray's `direction` (a
  vector or a rest index) and optional `age` in `in_transit` (in place of
  `heading`). Refused: `dynamics`, `max_active_owners`, `port_map`,
  `output`, `capacity`, `groups`, `reference_phase`, `headings`, `heading`.
  `"phase": false` stays as "never turns, phase 0, no window"; its mixing
  semantics (the diagonal weights) are gone with the mixing.
- **The record.** `run.json` gains `directions`, per family
  `phase_per_link`, per detector and per face the cumulative `record`, and
  `escaped` per family (amount, content, momentum); `events.jsonl` gains the
  `record` line (per interval, per detector Node and family, the pointer and
  its square) and the `pass` record's `threshold` field, and its `pass` for
  a window keeps `window`; `state.json` carries the rays per Node (rows)
  in place of the arrival and departure slots.
- **The books.** The transit line is in amount (rays), the content line
  amount x content per unit, the momentum in transit amount x content x
  D[direction]; the escaped lines the faces' sums as before.
- **Tests deleted** (their rules re-pinned in the module named; the pins
  that name a mixing, a scatter, a bundle's suspension or a diagonal weight
  are deleted with the rule): `test_node_mixing.py` and
  `test_node_mixing_numbers.py` (the sides; deleted, no rule remains);
  `test_event_transit.py` -> `test_ray_flight.py` (a); `test_periodic_axis.py`
  -> `test_ray_flight.py` (d); `test_event_boundaries.py` ->
  `test_ray_flight.py` (e) and `test_ray_clock.py` (d);
  `test_event_suspension.py` -> `test_ray_clock.py` (e) and
  `test_ray_readings.py` (c) (the transit suspension's cases deleted);
  `test_phaseless_family.py` -> `test_ray_readings.py` (b) (the diagonal
  weights deleted); `test_event_clock.py` -> `test_ray_clock.py` (a, b, d)
  and `test_ray_reemission.py` (c); `test_release_costs_by_phase_rate.py` ->
  `test_ray_clock.py` (c); `test_detector_sensitivity.py` ->
  `test_ray_detector.py` (b to d); `test_phase_window.py` ->
  `test_ray_window.py`; `test_one_reading_set.py` -> `test_ray_readings.py`
  (a to d) and `test_ray_detector.py` (b); `test_border_and_clock_corrections.py`
  -> `test_ray_clock.py` (d, e) and `test_ray_reemission.py` (b);
  `test_integer_bounds_of_measured_and_emission.py` ->
  `test_ray_world_parsing.py` (d) (the mixing's cell bound and its refusals
  deleted); `test_event_worlds.py` -> `test_ray_world_parsing.py` (a to c)
  and `test_ray_worlds.py` (the coherent field's shell pins and the
  diffusive field's flux pins deleted; the two slits re-pinned on the
  record); `test_reversible_detector.py`, `test_reversible_detector_world.py`,
  `test_physical_detector.py` (the candidate; deleted). New without a
  predecessor: `test_ray_collision.py`, `test_ray_bijection.py`,
  `test_ray_readings.py` (a), `test_ray_detector.py` (a),
  `test_ray_reemission.py` (a). Consumers patched: `test_entity_definitions`,
  `test_entity_loading_consumers`, `test_configuration_validation`,
  `test_check_scope`, `test_architecture`, `test_json_documents`.
- **Examples.** `examples/events/one_content.json`, `two_contents.json`,
  `two_slits.json`, `one_slit.json` rewritten as ray worlds; the `bell/`
  and `coupling/` generators re-emit `"law": "rays"` (the Bell worlds run
  160 intervals for the flight table's pace, the model ids
  `rays-bell-a{a}-b{b}-v1` and `rays-coupling-<name>-plane-v1`); the
  `detector/` worlds and `entities/detectors.json` are plain ray apparatus
  (measured events measuring the carrier, detectors with thresholds, the
  single Node reading `tensor`), no `dynamics`.
- **Tools.** `tools/bell_chsh.py` and `tools/coupling_readings.py` read
  the ray record; the coupling tool's 1b merge criteria are the refusal,
  its far-field bounds are readings against RAY_LAW section 8, printed
  inside or outside the expectation and never a failure.
- **Documents.** ENGINE.md is the bookkeeping around BEAM_LAW.md;
  DETECTOR_REQUIREMENTS drops its implementation contract; the registered
  readings of `events-v1` (series C, Bell A2) keep their scope in
  EXPERIMENTS.md and VALIDATION.md and are re-registered under `rays-v1`
  there.

## Cleanup after the law of the ray, on 2026-09-19

The model owner's request of 2026-09-19 ("check what code can be cleaned"),
applied from the cleanup audit of the same day. No integer the law produces
changes.

- **Deleted, `core/integer.py`:** `signed_divrem`, `ceil_div`, `checked_sum`,
  `add_components`, `subtract_components`, `dot_product`, `cross_product` and
  `reduced_ratio`, the component arithmetic of the deleted engines, with no
  caller left in `src`, `tools` or `examples` (a grep of the repository found
  only their definitions, their tests and the PHYSICAL_FEATURES example). The
  ray law's integer primitives stay: `checked_work`, `bounded_gcd`,
  `integer_root`, `by_clock`, `apportion_whole`. Their 13 tests in
  `tests/test_integer_arithmetic.py` are deleted with them; the module pins
  `checked_work`, `integer_root` and `bounded_gcd`, and `by_clock` and
  `apportion_whole` stay pinned in `test_ray_clock`. The TEST_EXPECTATIONS
  paragraph and the PHYSICAL_FEATURES example name the live primitives.
- **Deleted, `core/lattice.py`:** `MIXING_OPPOSITE` (the opposite Port of a
  heading, read by the deleted mixing; no caller). The docstring names
  `MAX_VALUE` as what it is under the ray law, the bound of a declared charge
  and quantum in the world file (no cell, no mixing).
- **Packaging.** `pyproject.toml` declares `numpy>=2.5.3,<3` in
  `dependencies` (the engine imports numpy at module level; the render extra
  no longer repeats it). `event_universe.__version__` is 0.3.1, the version
  of `pyproject.toml` and `CITATION.cff`; the string read 0.3.0 since the
  0.3.1 release of 2026-09-15, so every `run.json` recorded
  `package_version` 0.3.0 beside a 0.3.1 source digest, and records 0.3.1
  from now on. `event_universe.RaySimulation` is a lazy attribute: the
  package imports the world parser only, and the engine (numpy) loads on
  the first read of the name, as `events/__init__.py` promises. Nothing in
  `__all__` changes.

## No merge: a step onto a measured event is refused, on 2026-09-19

The model owner's decision of 2026-09-19 (Highlights 5.4, "three reversible
corrections that every path shares"; the architect's D3): a measured event's
step by its momentum (`_move`, step 6) onto a Node that already holds a
measured event is refused. The stepping event stays where it is, its
momentum untouched, the resident untouched, and `steps` counts the step made
(as for a wrapped step onto its own Node); no record is written. Until then
the two merged into the resident (amounts, what came home, momentum and
charge added) and a `merged` record was written; the architect's finding F1
(the absorbed number's units in flight pushing their former body)
disappears with the merge.

- **A world where two bodies met and merged now keeps both**, each with its
  own content, momentum and number. The coupling worlds `1b_m1`, `1b_m4`,
  `1b_m16` (`examples/events/coupling/`) run to a probe that reaches the
  Node next to the source and stays there, its steps onto the source
  refused; their `merged` record and the source's content 2^24 + m are gone
  from a rerun, so the 1b criteria of `tools/coupling_readings.py` that read
  a merge fail on the new engine. The registered result of the series
  (fingerprint `06a050c9...`, 2026-09-19) keeps its own scope and is not
  relabelled. `test_event_worlds` asserts no merge; no pin there moves.
- **The record.** `events.jsonl` has no `merged` record; `engine.bounded`
  no longer guards a merge (nothing is added to a resident).
- **Tests.** `tests/test_border_and_clock_corrections.py` (a) (new);
  `tests/test_event_boundaries.py`, the wrapped target held by a different
  Event: the refusal (both remain, the mover at (2, 1, 0) with momentum
  (1, 0, 0), one step) where it read the merge (one Event of content 2 at
  (0, 1, 0)) ([expectations](TEST_EXPECTATIONS.md#the-border-and-the-clocks-count)).

## An open face is a detector, on 2026-09-19

The model owner's decision of 2026-09-19 (the second of the three
reversible corrections): an event that leaves the board through an open
face, a bundle in transit in the walk (step 1) or a measured event's step
(step 6), is a click on that face, recorded like a detector's click under
the face detector named by the face (`face:+x`, `face:-x`, `face:+y`,
`face:-y`, `face:+z`, `face:-z`). Nothing physical changes: the amount, the
momentum and the content leave the board as before and the books'
escaped lines read the same numbers; the escape is a measurement at the
border, not a loss. No world key changes.

- **The record.** `events.jsonl` gains `click` records with `detector`
  `"face:..."`: for a bundle in transit `measured` None, the edge Node it
  left from, the family, the number, the amount, the `phase`, the
  `momentum` and the `content` (one record per interval, edge Node, family
  and number; no `push`); for a measured event that stepped off, `measured`
  its number, the amount and the content its content, its phase and
  momentum, and its `held`, `home` and `home_content`. The `escaped` record
  of a measured event is replaced by that click (a consumer reading
  `"event": "escaped"` reads `"event": "click"` with a `"face:"` detector).
  `run.json`'s and `state.json`'s `detectors` list the face detectors after
  the declared ones, one per open face in Port order (`name`, `nodes` the
  Nodes of the face, `threshold` 1, per family `measured` and `clicks` the
  units that clicked there in transit, `content` what they carried,
  `measured_content` the content of the measured events that stepped off,
  and `momentum`); a consumer that expected `detectors` to hold only the
  declared detectors filters by name. `run.json`'s `escaped` list and every
  books key are unchanged.
- **The API.** `Transit(..., face_observer=...)` (keyword-only, None by
  default) reports each escape; `EventSimulation.face_detectors()` and the
  counters `face_units`, `face_content`, `face_measured_content`,
  `face_momentum`, `open_faces`.
- **Tests.** `tests/test_border_and_clock_corrections.py` (b) (new);
  `tests/test_phase_window.py` (a): six records where there were four, the
  two passers' escapes clicking on `face:+x` at ticks 4 and 5. The Bell
  worlds (nothing escaped) are unchanged.

## The clock's count read off the clock, on 2026-09-19

The model owner's decision of 2026-09-19 (the third of the three reversible
corrections; the architect's D2): the count a measured event owes after its
self-creation is read off its clock like every other rate,
`by_clock(age, k x n, d)` with k the presence read and `[n, d]` the world's
`suspension` (what the whole part of age x k n / d gained by this
self-creation; `_suspend`, `Measured.owed`, written once per self-creation,
never accumulated, no remainder kept: the age owns it, as for the release,
the turn and the step). Until then the count was `k x n // d` written
whole, so the smallest slowing was 1 / 2 and a presence below d / n gave no
slowing at all. Now a measured event in a steady presence k is created
again on average every 1 + k n / d intervals: a presence of 1 at [1, 4]
slows its clock by 1 / 4 (four self-creations in five intervals) where it
was not slowed. Where k n / d is a whole number, and at the first
self-creation (age 0), the count is what it was. No world key and no record
key changes. The events in transit keep their count `presence x n // d`
(`Transit.suspend`): they carry no clock.

- **What changes in a run.** A world with `suspension` `[n, d]` whose
  measured events read a presence that is not a multiple of d / n ages
  differently: slower where k n < d gave 0, and by the exact mean
  elsewhere. Worlds with `suspension` 0 (the Bell worlds), with d = 1
  (`one_content.json`, the coupling world 6: `suspension` 1) or whose
  reads are exact multiples are unchanged.
- **Tests.** `tests/test_border_and_clock_corrections.py` (c) (new).
  `tests/test_event_suspension.py` (b), (c) and (e) read 16 x 1 // 4 on age
  0, 16 x 1 // 4 at every self-creation and 17 x 1 // 4, 17 x 1 // 16 on
  age 0, where the two rules agree: unchanged
  ([expectations](TEST_EXPECTATIONS.md#the-border-and-the-clocks-count)).
## One reading set for every coupling, on 2026-09-19

The model owner's decision of 2026-09-19 ([Highlights 5.4](HIGHLIGHTS.md#54-the-detector),
on the mathematician's list: "ONE READING SET FOR EVERY COUPLING, 'everything
present at the Node but the reader's own number, including here'"): one
generic law replaces two reading rules. Until then the suspension read the
presence of every family and every number but the reader's own while the
push, the size and a detector's threshold read one number, and the seventh
exit was counted inconsistently: a waiting unit counted as presence, a
measured event's content did not. No world file changes; nothing here is
evidence of a physical law. What a world reads differently:

- **A unit of a paid family passing a measured event of another number
  reads its content as presence.** The presence at a Node counts the
  content of the measured event there under its number (`EventSimulation.step`),
  so at `suspension` `[n, d]` a transit bundle of another number arriving
  there carries `(arrivals + content) x n // d` where it carried
  `arrivals x n // d`: a unit of light passing a content of 2^10 at [1, 4]
  is held 256 intervals where it passed unheld; at the default [1, 1],
  1024. A measured event's own read is unchanged (its content is its own
  number and is subtracted; the units waiting at its Node were counted
  before and are counted now). What came home waits in the measured
  event's record, is not content and is not presence. A world with a width
  above 0, paid units and a measured event of another number on their path
  reads a longer suspension there; every shipped world with a width
  (`one_content.json`, coupling world 6) has one number per Node or free
  streams only and reads as before.
- **A detector's threshold is met by the set.** The amount of a family
  arriving at a Node in one interval, summed over every number but the
  Node's own, is compared with the threshold (`_meet`); until now each
  number's bundle was compared alone, so two numbers' units arriving
  together, each below the threshold and at it in sum, passed, and are now
  met, pushed, clicked or re-released, the record per number as before. At
  threshold 1 without a window nothing changes (the set is at 1 exactly
  when some number is).
- **A phase window reads the set's phase.** `Transit.phase_at(position,
  ranks)` takes a sequence of ranks and reads the nearest step of the
  coherent sum over them; the engine passes the set (every number but the
  measured event's own) for a response and `[own]` for the home record. Two
  numbers arriving at a windowed Node in one interval are gated by the phase
  of their coherent sum, one verdict for both, and their `read`, `click`,
  `rerelease` and `pass` records carry that phase; a `home` record carries
  its own number's. A consumer that called `phase_at(position, rank)` passes
  `[rank]`. `Transit.sizes` is unchanged, a reading per Node and number.
- **The push** already summed the numbers' pushes (each number's flow, the
  emitter's own electric factor) and excluded the own number, which is home;
  what changed for it is the gate before it, the set's threshold and window.
  The `_meet` of the engine is split into `_home` (the own number) and
  `_respond` (one number of the set), the records' order at a Node being
  home first, then the set in rank order.
- **Tests.** `tests/test_one_reading_set.py` (new;
  [expectations](TEST_EXPECTATIONS.md#one-reading-set)).
  `test_event_suspension` (e) reads the presence 17 where it read 16 (the
  content counted), its counts 4 and 1 unchanged; no other pin moves. The
  Bell worlds read unchanged (326 criteria of `tools/bell_chsh.py`, S = 2).
  Series C moves no reading: its streams are free families, never suspended,
  and its probes read at threshold 1 without windows.

## The emission bound at parsing and the bounded measured line, on 2026-09-19

The architect's review of 2026-09-19 (findings F2, F4 and F9) found the
measured line unbounded and the emission bound enforced only at the first
crowded mixing. No physical law changes; a world that ran to its end runs
unchanged. What changes:

- **A previously valid world file can be refused at parsing.** A measured
  event of a free family must keep 3 x (amount x n // d), three times what
  it releases per Port per self-creation at the world's `release` `[n, d]`,
  at most 2^30 - 1, the mixing's cell bound (`world.EMISSION_CELL_BOUND`,
  `EMISSION_MARGIN` 3: a neighbour's slot holds up to about 2.3 x the
  release per Port). Until now the parser accepted any amount up to
  2^62 - 1, so the preflight certified a world of 2^36 at `release`
  [1, 128] that the mixing refused at interval 14 ("value exceeds the
  disturbance integer bound"); now the parser and the preflight refuse it,
  naming the Node, the amount, the release per Port, the `release` and the
  bound. Every shipped example passes (the largest free emission, 2^24 at
  [1, 128], is 3 x 131072 = 393216 against 1073741823); a world of a larger
  free content lowers its `release` or its content. A paid family's lamp
  and a world with `release` [0, d] are not affected.
- **A run can be refused where it silently continued.** `engine.bounded`
  checks a measured event's momentum after a push, a recoil or a merge, the
  push taken and its terms, its content after a click or a merge, and what
  waits to be created again with its content against 2^62 - 1
  (`transit.MOMENTUM_BOUND`) before assignment, and raises `OverflowError`
  naming the measured event, its Node and the quantity ("the momentum of
  measured event 2 at [1, 0, 0] exceeds the integer bound
  4611686018427387903"). Until now `Measured.momentum` and `pushed` grew as
  unbounded Python integers (two fixed events of 2^20 one Link apart reached
  5 x 10^12 in 120 intervals; stars of 2^35 passed 2^63 with no refusal).
- **The mixing's refusals are renamed.** "value exceeds the disturbance
  integer bound" (four messages of `mixing.py`) becomes "the amount in a
  cell exceeds the integer bound of the mixing (1073741823)", "the momentum
  carried by a departure exceeds the integer bound of the mixing (...)" and
  "the amount placed on a departure exceeds the integer bound of the mixing
  (1073741823)"; the coherent sum's "64-bit intermediate range exceeded"
  becomes "the coherent sum's component at a Node exceeds the integer bound
  of the mixing (2147483647: its square must fit the 64-bit register)". A
  consumer matching the old text updates its match.
- **Tests.** `tests/test_integer_bounds_of_measured_and_emission.py` (new;
  [expectations](TEST_EXPECTATIONS.md#the-integer-bounds-of-the-measured-line-and-of-the-emission)).
  No existing pin changes.

## A release costs the emitter by its phase rate, on 2026-09-19 (E = h f)

The model owner's decision of 2026-09-19 ("I approve the proposal"): until
then a unit of a paid family cost its emitter one unit of content whatever
the emitter's clock, so a blue lamp's click and a red lamp's carried the
same content. Now, at a self-creation whose turn is s = `by_clock(age,
content, K)` phase steps (the content before that self-creation's releases),
each unit a lamp releases costs it `quantum` x s content, carries that
content and the momentum `quantum` x s along its heading, and gives it to the
measured event that measures it ([the engine](ENGINE.md#a-release-costs-the-emitter-by-its-phase-rate)).
Nothing here is evidence of a physical law.

- **The record.** `Transit` carries the content per slot (`arr_con`,
  `fly_con`, `escaped_content`, `Transit.content()`), set at birth, added
  when arrivals join a slot, kept through the suspension and apportioned with
  the units at every Node exactly (`apportion_carried` on one component);
  `Transit.take` returns a fourth array, `Transit.place` and `Transit.receive`
  take an optional content (0 or none by default). `Measured.home_content`
  holds the content of what came home or is re-released until it leaves
  again (`state()` lists it). The engine's `_momentum` is replaced by
  `_birth(family, amount, port, steps)`, returning the content and the
  momentum a release carries; `apportion_whole` shares the content of a
  re-release over its six headings.
- **The books.** `books()["families"][name]` gains a `content` line
  (`initial`, `released`, `current`, `escaped`, `absorbed`, `balanced`),
  part of `balanced`; the measured line's `measured` and `spent` are in
  content (the clicks' content, the lamps' cost), the transit line stays in
  units. `EventSimulation.content_initial`, `content_released`,
  `content_absorbed` and `home_content_pending` are the counters.
- **The record of a run.** Measurement records (`home`, `read`, `click`,
  `rerelease`) carry `content`; `state.json` Node entries carry `content`
  per arrival and departure; `run.json`'s `measured` entries carry
  `home_content`. The `quantum` key is now the content of one unit per
  phase step (h); worlds parse unchanged.
- **What changes in a run.** A lamp whose turn is 0 at a self-creation
  releases nothing there (a lamp of content below K / (age + 1) at K 2^20
  releases nothing for a long time; a lamp of a family without a phase
  circle never); the turn of a lamp is read from its content before it
  spends (until now after). A free family's release costs nothing and its
  units carry no content, so `measure` on a free family takes the units and
  adds nothing to the content (until now the amount). The declared
  `in_transit` units of a paid family carry one phase step of content each.
  The Bell worlds (content K + 2 at K 2^20: s = 1) and `test_phase_window`'s
  lamps (K + 2 at K 2^14) run as before; the slit worlds' lamp (2^36 at
  K 2^34) spends 4 per unit at the start and the screen's content grows by
  the turn per click, the click counts unchanged.
- **Tests.** `tests/test_release_costs_by_phase_rate.py` (new);
  `test_event_clock` (c) at K 82 (the same 82 pin; at K 2^20 the lamp
  would release nothing), `test_detector_sensitivity` (c) at K 24 (the
  same 18 and 12), `test_phase_window` (a) records with `content` 1,
  `test_event_suspension` (c) the probe's content [0, 1] (was [464, 1]),
  `test_event_worlds` (d) the screen's content between 3 and 4 times its
  clicks ([expectations](TEST_EXPECTATIONS.md#a-release-costs-the-emitter-by-its-phase-rate)).
## One rule of the Node: the phase-less scatter folded into `mix_arrivals`, on 2026-09-19

The model owner, 2026-09-19: "everything generic must be replaced by
generic". The physics-rule reviewer showed that the per-Port scatter of a
family without a phase circle is the diagonal of the coherent sum: with
c_h = S - 3 a_opp(h), |c_h|^2 = |S|^2 - 6 Re(S conj(a_opp)) + 9 |a_opp|^2,
and dropping every cross term between mutually incoherent arrivals leaves
weight_h = 32^2 x (the number's amount over the six Ports + 3 x its amount
through the side's own Port), 4 : 1 : 1 : 1 : 1 : 1 for a lone arrival.
`mixing.scatter_arrivals` and its constants `SCATTER_BACK`, `SCATTER_TOTAL`
are removed; `mixing.mix_arrivals` computes every family, reading
`phased` from the family's arrays (`MixingArrays.phased`, `Transit.phased`),
its weights `mixing.coherent_weights` for a family with a phase circle and
`mixing.diagonal_weights` for one without; `Transit.cycle` calls it for
every family. The same expectation: the shares per side agree in the mean
exactly, the leaving phase is 0 and the units keep their number. What
moves is the rounding and the labels: the largest-remainder placement and
the momentum's apportionment fall once per group (one number at the Node)
where the scatter placed once per Port, so `test_phaseless_family` (b)
re-pinned two integers (the labels of two opposite 9s, 0 each where each
Port's own gave -3 and 3; the edge of 2 with 9, [4, 2, 2, 1, 1, 1] where
the 2 went whole and the 9 mirrored, [6, 1, 1, 1, 1, 1]) and the pinned
worlds of `test_event_worlds` (a) to (c) stay within their bands. A
number's weights are its own: no cross term survives between numbers
either, so another number's field at the Node does not steer its labels
(the diagonal over all numbers present would, measured at 4 to 10 times
the pair world's push; the sides' total is the same either way). The
kernel runs about four times faster than the per-Port scatter on 29^3.

## The field of matter without phase, the suspension as presence with a fractional width, and the push as the net flow, on 2026-09-19

Three decisions of the model owner, 2026-09-19, implemented together after
the physics-rule review of that day found that a coherent field gives a
clock slowing as sqrt(M) / r while nature's is M / r, and that no reading at
a point of a coherent field gives M / r; the owner decided to implement now
and to revert if the reviewer's numbers say otherwise. Nothing here is
evidence of a physical law.

1. **A family may declare no phase circle**: `"phase": false` in its
   `families` entry (true by default, as before; `FamilyDefinition.phase`,
   `Transit(..., phased=...)`). Its events carry phase 0 and never turn, its
   measured events' phase never turns (K does not apply to their content,
   so the K x N / 2 bound is not checked for them), a `phase_window` is
   refused on its lamps and on a table entry for it, and its measured
   events and events in transit may declare no `phase` but 0. At a Node its
   arrivals do not sum coherently: each Port's arrival scattered on its own
   (`mixing.scatter_arrivals`, chosen by `Transit.cycle`) with the shares of
   a lone arrival, four ninths back out through the Port it came in by and
   one ninth to each of the other five sides, whole units by the largest
   remainder per Port, its momentum apportioned over its own departures,
   the six Ports' departures added per heading; later the same day the
   scatter was folded into the one kernel as the diagonal of the coherent
   sum (the section above). The example worlds
   `one_content.json` and `two_contents.json` now declare `"phase": false`
   for `m`; the slit worlds' light keeps its phase. `run.json` lists
   `phase` per family.
2. **The suspension reads presence with a fractional width.** `suspension`
   is `[n, d]` (an integer w is accepted as `[w, 1]`, so a world declaring
   `1` still parses, but it now means one interval per unit of presence
   rather than per whole unit of amplitude; 0 or `[0, d]` is none, recorded
   as `[0, 1]`; `EventWorld.suspension` is a pair and `run.json` records it
   as a list). What is read is the presence at the Node, the amount that
   arrived this interval over every family and every number but the
   reader's own (a transit bundle of a paid family reads everything at its
   Node but its own number; a measured event reads everything but its own
   number), no amplitude and no square root: `count = presence x n // d`.
   Until now the transit read the free families' sizes and the measured
   event every family's sizes, in whole units of amplitude (32 sqrt(amount)
   in 32nds). `Transit.sizes` stays as a reading and as the phase window's
   sum; it no longer feeds the suspension. `Transit.suspend` takes the pair;
   `EventSimulation._suspend` reads the presence. A world with `suspension`
   1 and a steady arrival of 16 units per interval now suspends 16
   intervals per self-creation where it suspended 4: declare `[1, 4]` for
   the old count at that amount.
3. **The push of a free family reads the net flow.** For the units of one
   number of a free family arriving at a measured event, the push is the
   content times the net flow of those arrivals, the sum over the six Ports
   of amount times travel heading (what `Transit.flow` sums per Node),
   toward the emitter as before (push = -flow x content), and the electric
   part likewise with the flow in place of the carried momentum. A paid
   family's push stays its carried momentum (light's pressure). The momentum
   from birth of a free family's events stays on their record and in the
   momentum book (the transit line still reports the labels in flight,
   apportioned exactly at every Node; the measured line reports the pushes
   taken, now by the flow; the two are a report, not a balance).

The tests: `test_event_suspension` (a), (b) and (c) re-pinned at
`suspension` [1, 4] (16 x 1 // 4 = 4, the same ages and counts as before),
(d) light on light and (e) one presence, two readers, added;
`test_phaseless_family` new; `test_event_worlds` re-pinned for the
phase-less `m` and the flow push ([expectations](TEST_EXPECTATIONS.md)).
The other tests declare `suspension` 0 and families with a phase and are
unchanged.

## The coherent sum at a Node over all numbers present, on 2026-09-19 (node-mixing-v3)

The model owner's decision of 2026-09-19, for genericity: "the Node reads
what is present"; the number is a label for the detector, not a kind. Until
now `mix_arrivals` computed the Node's sides per number, one number one
group: the coherent sum, the leaving amplitudes and the sides' shares were
formed from one number's arrivals alone, and two emitters' crowds passed
through each other without interfering (two lamps twenty Links apart read a
screen profile equal to the sum of the two single lamps' within 1 %). Now
the coherent sum at a Node runs over all the arrivals present, whatever
their number: the amplitude vectors are summed over the number axis per
Port before the coherent sum, the leaving amplitude of each side is the
common sum less three times what came in through that Port over all
numbers, the weights per side (the squared leaving amplitudes) are common to
every number at the Node, and each number then places its own units by the
common weights (whole units by the largest remainder, ties in the tick's
Port order, per number), a number with no whole for any side going whole to
its own momentum's heading; the momenta are apportioned per number as
before; the leaving phase of a side is the common leaving amplitude's phase
for every number; every unit keeps its number. Nothing else changes: a
family's units never mix with another family's (each family is its own
transit), and `Transit.sizes` and `Transit.phase_at` read per number as
before (what a measured event reads for its suspension and its window is a
bundle of one number). A world whose family has one number at every Node,
every example world and every existing test, runs as before; with one
number the sum over the numbers is that number's own, so the integers of
`test_node_mixing` are unchanged. New: `tests/test_node_mixing_numbers.py`
(two numbers at one Node in phase, 1, 0, 2, 2, 2, 2 each at tick 0; in
antiphase 5, 4, 0, 0, 0, 0 each, nothing sideways; a number with no whole
whole by its own momentum at the common phase; a number alone as before).
No key of the world file or of the record changes; `MixingArrays` keeps its
fields, with the number axis next to the Port axis
([the engine](ENGINE.md#the-law-of-events-events-v1),
[expectations](TEST_EXPECTATIONS.md#the-coherent-sum-over-the-numbers)).

The pair of `test_event_worlds` (c), two contents of one free family 8
Links apart, does not change its reading: with the field of matter
phase-less (the note above) its `m` never enters `mix_arrivals`, so v3
does not act on it and the pins are the field of matter's (the axial
pushes equal within 0.5 %, 0.02 % measured; the axial push against
M_B rho M_A / (4 pi d^2) 1.449; the product law 3.9993;
[expectations](TEST_EXPECTATIONS.md#the-worlds-of-the-law-of-events)).
The one-content world, the two-slit worlds (one lamp, the wall's number
releasing nothing) and every other test read as before.

## A periodic axis as a declared run parameter of the world, on 2026-09-19 (`boundary` per axis)

The declared exception to the open board, approved by the model owner on
2026-09-19: the board of `events-v1` is open on every face ("the edge is
infinity, what leaves is booked as escaped with the momentum it carried; a
closed board is refused"), and a world file may now declare an axis
periodic, each experiment deciding what to run. Additive: `boundary` accepts,
beside the string `"open"`, an object with any of the keys `x`, `y`, `z`,
each `"open"` or `"periodic"`, the missing axes open (`{"z": "periodic"}`);
`"closed"`, the bare word `"periodic"` and every other value are refused as
before, naming the closed board. On a periodic axis the departures that would
leave the board through one face are created at the first Node of the
opposite face (`Transit.walk`), nothing escapes on that axis and the momentum
they carry stays on the board; `escaped` counts only what leaves through the
open faces; with an extent of 1 the two departures on that axis return to
the same Node in the next interval as its arrivals through those Ports (a
four-Port node with a one-interval stub). On 2026-09-19, later the same
day, the model owner ruled one rule for the board: a measured event's step
by its momentum (`_move`, step 6) wraps on a periodic axis too, the last
Node's step along +axis landing on the first and the first's along -axis on
the last, with an extent of 1 on its own Node (no move, no merge with itself,
the momentum untouched, the step counted in `steps`); through an open face
it escapes with its content and momentum as before (the first periodic axis
escaped a measured event on every face; `test_periodic_axis` (d)). New:
`EventWorld.boundary` (the declared value)
and `EventWorld.periodic` (per axis), `EventWorld.boundary_per_axis`,
`Transit(..., periodic=...)`; `run.json` and `state.json` carry `boundary` as
declared (the string or the object) in place of the constant `"open"`; the
preflight's summary gains `boundary` per axis. A world with `"open"` or
without the key runs as before ([the engine](ENGINE.md#the-law-of-events-events-v1),
[expectations](TEST_EXPECTATIONS.md#a-periodic-axis),
`tests/test_periodic_axis.py`).

## The suspension of a measured event, read after its self-creation, on 2026-09-19

A bug of the first `events-v1`, found by the physics-rule review of
2026-09-19 and verified in a probe run: the engine read a measured event's
suspension before its self-creation, so in a steady field (the sizes at its
Node at or above one whole unit at every interval) the count was owed again
every time it was spent, and the clock of a measured event with
`suspension` 1 stood still: no self-creation, no release, no phase turn, no
step (probes of content 1 at r = 4 to 14 from a content of 2^24 aged 4 to
17 in 60 intervals while the source aged 60). The law says slower, not
still (Highlights 5.4: "a measured event that reads a large size releases
and turns slower"; the transit's rule, a count k written on arrival, held k
intervals, then one Link). Now a measured event that owes nothing is
created again first, and then reads this interval's sizes of the other
numbers at its Node and owes `suspension` intervals per whole unit read,
paid one per interval before its next self-creation: in a steady size of k
whole units it is created again once every k + 1 intervals, its clock
slowed by 1 / (k + 1) and never frozen. Its step by its momentum is made
when it owes nothing, in the self-creation's interval when that read no
count, else in the interval the last unit is paid. `age + waited` is the
intervals completed, as before. Worlds with `suspension` 0 are unchanged;
`test_event_suspension` (b) is re-pinned (ages 1, 1, 1, 1, 1, 2 after
intervals 1 to 6) and (c), a measured event in a steady field, is added
([the engine](ENGINE.md), [expectations](TEST_EXPECTATIONS.md#the-suspension)).
No key of the world file or of the record changes.

## The phase window, on 2026-09-19 (`phase_window`)

The model owner's decision of 2026-09-19 ([Highlights 5.4](HIGHLIGHTS.md#54-the-detector),
"Approve the phase window as a declared width of a detector, and of the
emitter too"). Additive: a table entry of a measured event may be an object
`{"rule": ..., "phase_window": s}` beside the string form, which is still
accepted and means the same; a lamp may declare `phase_window`; s is a step
of the circle, 0 through N - 1, and is refused otherwise, on `pass`, in an
object without `rule` or with any other key. New in the record: the
measurement records `home`, `read`, `click` and `rerelease` of `events.jsonl`
carry `phase`, the bundle's phase at the Node; a `pass` record (tick, node,
measured, detector, family, number, amount, phase, window) is written for a
bundle outside a window; the measured events' states in `run.json` and
`state.json` list `windows` per family. `MeasuredDefinition.windows`,
`LampDefinition.window`, `Measured.windows`, `Measured.lamp_window`,
`Transit.phase_at` and `engine.in_window` are new. A world without the key
runs as before ([the engine](ENGINE.md), [expectations](TEST_EXPECTATIONS.md#the-phase-window)).

## The engine of the law of events, on 2026-09-19, the evening (`events-v1`)

Decision of the model owner, 2026-09-19 ([Highlights 5.4](HIGHLIGHTS.md#54-the-detector),
"The law of events" and "The principles of the law of events"): "There is no
shadow, no real. There are only events on the event board. There are
detectors by sensitivity. That is it. Everything must be generic in the
engine, without registers. There are no draws." The engine of the law of the
shadow (`field-only-v1`, `src/event_universe/shadow/`) is replaced by the
engine of the law of events (`src/event_universe/events/`) and deleted, with
what it kept that the law removes: the parked ninths of the mixing and their
release at nine, the wait as intervals owed and held per Node and number, the
phase turn's remainder per family, the register of units below a family's
`quantum` at a holder, and every remainder of a held content (its release,
pool, push, lamp and clock). Nothing of the old engine survives by name:
`ShadowSimulation`, `ShadowWorld`, `ShadowLayer`, `Holder`,
`parse_shadow_world`, `execute_shadow_run` and `SHADOW_LAW` are gone;
`EventSimulation`, `EventWorld`, `Transit`, `Measured`, `parse_event_world`,
`execute_event_run` and `EVENTS_LAW` take their places.

The world file: `"law": "events"` in place of `"law": "shadow"`; `measured`
in place of `contents`; `in_transit` in place of `initial_shadows`;
`suspension` (an integer of intervals per whole unit of size read) in place of
`wait_per_quantum`; the table rule `measure` in place of `keep`; the family
key `phase_turn` is gone (an event in transit does not turn); `quantum` means
the content of one unit of a paid family (its momentum from birth), no longer
a threshold assembled at a holder; `detectors` is new. A world with any old
key is refused naming the law and the key. `run.json` carries `law`
"events-v1", `suspension`, `measured`, `detectors`, `measured_content` and
`transit_content` in place of `wait_per_quantum`, `contents`, `held_content`
and `shadow_content`; its books name the lines `measured` and `transit` in
place of `held` and `shadows`; `state.json` lists `measured` and `detectors`
and its Nodes' arrivals carry `suspended` in place of `waiting`, with no
`parked` list. The examples moved from `examples/shadow/` to
`examples/events/`, converted key for key (the slit worlds gained the detector
`screen`).

The tests: `test_field_only.py`, `test_family_turns.py` and
`test_family_quantum.py` are deleted with the features they isolated;
`test_node_mixing.py` now isolates node-mixing-v2; `test_event_transit.py`,
`test_event_suspension.py`, `test_event_clock.py` and `test_event_worlds.py`
are new ([expectations](TEST_EXPECTATIONS.md)). The readings of the worlds are
re-pinned from the new engine (the escape 0.989 of the emission, the pair's
pushes within 8 %, the product law within 10 %).

## The phase turn in flight per family, on 2026-09-19 (`phase_turn`)

The model owner's decision of the evening (Highlights 5.4, the status line:
light turns by its message, the same everywhere, "the default for light, that
is, per family"). The family key `turns_in_flight` (true or false, feature 21
of the same morning, never in a merged world file but in the record) is
replaced by `phase_turn`: `"quantum"` (the default for a paid family: by the
family's `quantum` over K per Link walked, the same for every quantum of the
family, a remainder carried per family), `"amount"` (the old rule, by the
amount in the cell over K) or `"none"` (the default for a free family). A
world declaring `turns_in_flight` is refused as any unknown key; one that
declared nothing changes its light from the old rule to the uniform one, which
at the default quantum of 1 turns 1/K per interval: declare the light's
`quantum` for a frequency. `run.json` lists `phase_turn` per family in place of
`turns_in_flight`; `ShadowLayer` takes `turn` and `quantum` in place of
`rotates`.

## One engine, on 2026-09-19: the old engine deleted

Decision of the model owner, 2026-09-19, the evening ([Highlights 5.4](HIGHLIGHTS.md#54-the-detector),
the status line of the law of the shadow): "The field is, in fact, a field of
events. No confrontations are needed. Only tests that everything is as
designed." The engine of the law of the shadow (`field-only-v1`, feature 20)
is the one engine; the old engine of the law of the bit is deleted without the
confrontation runs the morning had made a condition. Nothing of the new
engine's behaviour changes: `tests/test_field_only.py` passes with the same
pinned integers before and after.

What moved (the substrate the new engine had imported from the old one,
byte-identical in what it does):

- `core/lattice.py`: `Address3`, `Heading`, `PORT_HEADINGS`, `MIXING_OPPOSITE`
  and `MAX_VALUE` (from `core/disturbance_state.py` and `core/spatial_state.py`);
- `core/phase.py`: `phase_cosines`, `phase_sines`, `PHASE_COSINE_SCALE` and
  `MAX_PHASE_STEPS` (from `core/spatial_state.py`);
- `shadow/mixing.py`: the Node's mixing kernels `mix_arrivals`,
  `apportion_carried`, `release_parked`, `merge_departures`, `place_departures`,
  the `MixingArrays` protocol, `LAYERS`, `MIXING_DENOMINATOR`,
  `MIXING_AMPLITUDE_SCALE` and `MIXING_WEIGHT_BITS` (from `dense_field.py` and
  `core/spatial_state.py`); the isolated test of the rule is the new
  `tests/test_node_mixing.py`, on one Node of the engine's layer.

What was deleted:

- the old engine: `core/` except `integer.py` and the two modules above
  (`conservation_state`, `coupling_selectors`, `disturbance_engine`,
  `disturbance_node`, `disturbance_state`, `event_resolution`, `node_boundary`,
  `node_conservation`, `node_execution`, `node_ports`, `node_services`,
  `plan_reuse`, `ray_event_audit`, `spatial_engine`, `spatial_node`,
  `spatial_state`, `topology`, `validation`), the whole of `fields/`,
  `dense_field.py`, `prefill.py`, `initialization.py`, `disturbance_api.py`,
  `entities.py`, `entity_catalog.py`, `node_conservation_configuration.py`,
  `observer_configuration.py`, `reference_units.py`, and of `diagnostics/`
  everything but `numeric_audit.py` (`disturbance_render`, `local_conservation`,
  `local_observer`, `node_conservation`, `node_contract`); with them the
  `Simulation` and `InitialState` names of the package;
- the old worlds: every file under `examples/` except `examples/shadow/`
  (`basic.json`, the four numbered examples, `exchange`, `finite_fields`,
  `isotropic_rays`, `local_field_rules`, `local_lorentz_field`,
  `moving_source`, `open_world`, `spatial_computation_delay`,
  `spatial_turning`, `three_mass_finite`, `coupled-excitations/`,
  `directional-wave/`, `known-entities/`, `node-vector/`,
  `particle-contracts/` and the 25 world directories of `examples/nature/`
  with their pages, scripts and records) and `catalog/nature.json`;
- the tools of the old engine: `tools/ray_viewer/` (the 3D viewer and GIF
  renderer of the old record), `tools/audit_particle_contracts.py`,
  `tools/benchmark_focus.py` and `tools/profile_node_vectors.py`;
- the tests of the old engine, 41 modules (`test_bit_law`,
  `test_boundary_configuration`, `test_charge_per_thing`, `test_clock_readings`,
  `test_dense_field`, `test_detector_absorb`, `test_detector_mark`,
  `test_detector_return`, `test_disturbance_application`,
  `test_disturbance_engine`, `test_external_body`, `test_initialization`,
  `test_inverse_split`, `test_lanes`, `test_local_conservation`,
  `test_local_conversions`, `test_local_focus`, `test_loop_binding`,
  `test_mean_field_gauss`, `test_nature_catalog`, `test_node_conservation`,
  `test_node_is_ports`, `test_node_state_contract`, `test_payload_validation`,
  `test_perf_arrays`, `test_plan_reuse`, `test_rational_particles`,
  `test_ray_event_audit`, `test_ray_field`, `test_ray_hidden_state`,
  `test_ray_layers`, `test_ray_meeting_conversion`, `test_ray_momentum_turn`,
  `test_ray_polarization`, `test_ray_viewer`, `test_return_field`,
  `test_shadow_wait`, `test_wait_reads`, `test_wait_rule`,
  `test_wave_ray_families`, `tests/support/`), and the old versions of
  `test_node_mixing`, `test_configuration_validation`, `test_json_documents`,
  `test_architecture` and `test_locality`, rewritten for the one engine.

What changed for a user:

- `python -m event_universe --init WORLD --output OUT [--ticks N]` runs a
  world of the law (`"law": "shadow"`) and nothing else; the switches
  `--visualize`, `--frame-stride`, `--observer`, `--node-workers`,
  `--dense-field` and `--standing-field` are gone with the engine they drove;
- `python -m event_universe.configuration_validation WORLD [--json]` checks a
  world file; the kinds `initialization`, `catalog`, `profiles` and `observer`
  are gone, `--catalog` and `--initialization` with them;
- the workspace (`python -m event_universe.ui`) lists the worlds of
  `examples/shadow/` as its templates and runs headless; "Run & watch" is
  refused;
- `tools/run_series.py` is unchanged; `tools/check.py` no longer knows the
  deleted resource consumers;
- the record of a run is the engine's `run.json` as before (`law`
  "field-only-v1"), unchanged.

The dated evidence of the old engine stays where it was recorded
([experiments](EXPERIMENTS.md), [validation](VALIDATION.md),
[derivations](DERIVATIONS.md), [hypotheses](HYPOTHESES.md)); the contracts of
the old engine under `docs/` stay as history, each marked at its head. The
old engine is in git: `git log --first-parent main` reads the day by PRs, and
any earlier state can be checked out.

Later the same day, by the owner's "delete what needs deleting; everything in
git, in order, if everything works": the documents of the old engine went too.

- deleted under `docs/`: `CATALOG`, `COMPUTATIONAL_RESPONSE`,
  `CONFIGURATION_VALIDATION` (the live preflight is a section of `ENGINE.md`),
  `COUPLED_EXCITATIONS`, `DETECTOR_SAMPLING`, `DIRECTIONAL_WAVE`,
  `DISTURBANCES`, `ENTITY_CATALOG`, `LOCAL_CONSERVATION`, `LOCAL_CONVERSIONS`,
  `LOCAL_FIELD_RULES`, `LOCAL_FOCUS`, `LOCAL_LORENTZ_FIELD`, `LOCAL_OBSERVER`,
  `LOOP_BINDING`, `NODE_VECTOR_PROCESSOR`, `PERFORMANCE`, `PHYSICAL_ENTITIES`,
  `PROPERTY_COUPLINGS`, `RATIONAL_PARTICLES`, `RAY_EVENT_MODEL`,
  `REFERENCE_UNITS`, `SHARED_RAY_COUPLING`, `SPATIAL_COMPUTATION_DELAY`,
  `SPATIAL_COUPLINGS` and `SPATIAL_FIELDS`, whose last section, the law of the
  shadow, is now `ENGINE.md` (the anchor
  `#the-law-of-the-shadow-field-only-v1` unchanged); every link to a deleted
  document or to a section of the old engine became plain text;
- trimmed to the one engine: `PROJECT_STATUS.md` (the restart guide, the
  checkout table, how to resume), `TEST_EXPECTATIONS.md` (the suite of
  2026-09-19 and the repository gates), `HIGHLIGHTS_IMPLEMENTATION.md` (one
  table, Highlights section by section) and `ARCHITECTURE.md` (the integer
  contract, ownership, the dependency direction); the dated versions before
  are in git;
- deleted under `skills/`: `simulation-configuration` (the old schema's
  authoring guide and template) and `visualization-check` (no renderer);
- the workspace reduced to the world file: the JSON editor, **Check**,
  **Run**, **Stop**, the record and the files; the forms of the old schema,
  the placement preview and the movie (`ui_assets/playback.html`) deleted;
  `/api/runs` takes the source alone.

## The law of the shadow, a new engine mode, on 2026-09-18 (`field-only-v1`)

Feature 20 ([the law of the shadow](MIGRATION.md);
Highlights 5.4, the model owner's decision of 2026-09-18, the evening): the
field-only engine, `event_universe/shadow/`, beside the old one. Nothing of
the old engine is deleted or changed in behaviour:

- a world with `"law": "shadow"` runs on the new engine; every other world
  runs as before, byte for byte. The old parser refuses `law` as an unknown
  key; the new parser refuses every key of the old schema by name
  (`schema_version`, `fields`, `disturbance_types`, `seeds`, `spatial_fields`,
  `emissions`, `spatial_seeds`, `detectors`, `external_bodies`,
  `initial_field`, `ray_interactions`, `couplings`, `interactions`,
  `dense_field`, `standing_field`, `wait_reads`, `shadow_wait`,
  `slots_per_node`, `link_ticks`, `normal_budget`, `operation_costs`) and a
  closed board;
- the runner's switches `--observer`, `--visualize`, `--dense-field`,
  `--standing-field` and `--node-workers` above 1 are refused for a world of
  the law; `tools/run_series.py` runs such worlds as any;
- `event_universe.configuration_validation` gains the kind `shadow`
  (discriminated by `law`), `--kind shadow` on its command line;
- `event_universe.dense_field`: the mixing kernels `DenseField._mix`,
  `_apportion`, `_release`, `_departures` and `_place_departures` are the
  module-level `mix_arrivals`, `apportion_carried`, `release_parked`,
  `merge_departures` and `place_departures` over a `MixingArrays` protocol
  (the methods delegate; a caller of the methods is unaffected);
- `event_universe.snapshot_writer.write_snapshot` takes any `SnapshotSource`
  (an object with `snapshot_stream`), the engine as before;
- `run.json` of a world of the law has its own keys (`law`, `numbers`,
  `audit` of the new books, `held_content`, `shadow_content`, `momentum`,
  `contents`, `escaped`) and none of the old engine's markers; `state.json`
  its own layout (`law`, `contents`, `nodes`); `events.jsonl` its own kinds
  (`home`, `read`, `click`, `rerelease`, `step`, `merged`, `escaped`);
- a content's `table` maps a family to `read`, `keep`, `rerelease` or
  `pass` (round 8's fates): a free family is read and passes on, a paid one
  is kept (the click) or re-released pooled with the holder's release.

## Charge per thing, on 2026-09-18 (`charge-per-thing-v1`)

Feature 16g (charge per thing;
Highlights 5.4 point 16 as amended by the model owner, 2026-09-18). No world
key is added or removed; the meaning of one changes:

- `spatial_fields[i].charge` is the charge of one thing of the family, whole,
  whatever its content (an electron -3 in thirds of e on 1 quantum or on 64),
  no longer a charge per quantum. A world whose family charge meant "per
  quantum" on things of more than one quantum (a family of charge -1 whose
  things are 100 quanta, meant as -100 whole) declares the whole charge it
  means; the example worlds and the catalog declare the charge of a thing
  already and change nothing (the A5 worlds' electrons of 64 quanta were read
  as -192 whole before and are -3 now, their pushes 64 times smaller: the
  decided physics, the product of the charges).
- `external_bodies[i].charge` is the body's whole charge, as before, and it
  is what the body multiplies an electric message by: a body a table pushes
  is no longer refused when its charge is not a multiple of its amount, and a
  body of 1000 quanta declaring 1000 to mean 1 per quantum now means 1000
  whole and is pushed a thousandfold; declare the charge the body has (the
  tests' bodies of 100 that meant -1 per quantum declare -10, so that their
  shadows' message, -10 / 100, times the charge is what they pinned; those
  of 1000 pushed by a body of 81 declare -1; `tests/test_perf_arrays.py`
  declares -4096 on 2^24).
- readouts: `charge_totals()`, `escaped_charge_totals()`, the ledger's
  `charge` lines, `conservation_report()["charge"]` and `ray_charge` count
  the whole charge of things (a merged ray of k things k times the family's
  charge, a record's stock the things it has not yet emitted, `record_things`)
  instead of charge x amount; a run's `audit` and the runner's conservation
  flag read these. `run.json` gains `charge_per_thing`.
- `RAY_PROPERTIES.charge`, the view a coupling reads, is the whole charge of
  the thing the ray is; the appended `charge` invariant of a meeting is the
  per-ray readout `{"field": "charge"}` summed over inputs and outputs
  (`charge x amount` before); `InteractionDefinition` gains
  `output_identities`; a meeting's outputs carry their source input's further
  owners, a join (the plain sum of the inputs) every input's; a Born product
  that took the whole content of a corner carries the other thing's identity.
- `SpatialPlan` gains `charge_delta`; `SpatialAccounting` gains
  `sourced_charge`, `absorbed_charge` and `absorbed_charge_by_marks`;
  `SpatialEngine` the same lists and `sourced_charge_totals()`,
  `absorbed_charge_totals()`, `marks_charge_totals()`; the reception record's
  `absorbed_by_mark` entries carry `charge`; `ExternalBody` and
  `SpatialFieldDefinition` keep their `charge` fields with the new meaning;
  `push_of` takes the pushed thing's whole charge (`thing_charge`).
- tests re-pinned, each with a dated reason: `test_wave_ray_families` (c),
  `test_lanes` (h), `test_nature_catalog` (the charge readouts and the
  electron's push), `test_bit_law` ((a)'s charge line, the pushed bodies of
  (b) and (c')), `test_return_field`, `test_shadow_wait`, `test_perf_arrays`
  (declarations), `test_loop_binding` (identities stripped from the lines it
  reads), `test_clock_readings` (a docstring); new module
  `tests/test_charge_per_thing.py`.

## The engine clean under the law of the bit, on 2026-09-18 (`cleanup-law-v1`)

The cleanup lane of 2026-09-18 (the engine clean),
on the model owner's instruction. Keys and code deleted, not kept behind an
option; a world that writes a deleted key is refused:

- world keys: `return_mode` (unknown key), `sampling_profile` (unknown key),
  `ray_delay` and `ray_phase_per_tick` (unknown keys); `phase_bits` on a
  spatial field (refused naming the definitions of the law); the output
  form `delay: {of, table, per}` of a meeting (an integer delay only);
- world key added: `N`, the number of steps of the world's one phase circle,
  64 by default, a power of two from 2 through 4096; a coherence table's
  `kerengonen.phase_steps` must equal it;
- `run.json`: `N` beside `K`; no `return_mode`, `sampling_profile`,
  `annulled_totals`, `ray_binding`, `ray_delay`; no `annulled` line on the
  ledgers; the `inverse_split` record without `mode` and `annulled`;
  `line_balanced` reads an `annulled` line of an older record as a loss;
- `InitialState`: `phase_steps` added; `return_mode`, `sampling_profile`,
  `ray_delay`, `ray_phase_per_tick` removed; `InteractionDefinition.lags`,
  `LagTable`, `Ray.lag`, `SpatialNodeState.ray_wait` removed;
  `SpatialNodeState.detector_ticket` is `arrivals`, `ticket_bit` /
  `detector_draw` / `TICKET_MODULUS` are `table_catch` / `mark_catch` /
  `ARRIVAL_MODULUS`; the planner's `ray_hold` argument and `hold_rays` are
  gone; `SpatialPlan.annulled`, `InverseSplit.mode` and `.annulled`,
  `annulled_totals()`, `record_annulled` are gone; `core/sampling_contract.py`
  is deleted; `split_ports` and `transmit` take no mode;
- the catalog: no `phase_bits`, `lag_bits`, `field`, `field_of`, `kind:
  field`, `source_sign`; `release` on every ray record; `recoil_return`
  deleted; `electron_field_turn` a momentum table (catalog);
- examples: `examples/nature/bit_law_migration.py` gains `migrate_n` (one N)
  and the drop of orphan field families; 96 worlds gain `N`, 32 lose an
  orphan family, the 23 `delay_*` worlds and the `turn_n14` / `turn_n16`
  worlds of A6 are deleted;
- tests deleted: the `straight` / `annul` cases of `test_inverse_split`, the
  `annul` worlds of `test_ray_event_audit`, the two sampling tests of
  `test_native_ray_coupling` and its `second_clock` and `ray_delay` cases,
  the ticket assertions of `test_kerengonen`, the 128-bit wide phase of
  `test_wave_ray_families`; re-pinned with dated reasons: `test_detector_mark`,
  `test_detector_return`, `test_nature_catalog` (the worlds case runs),
  `test_return_field` (a), `test_perf_arrays`, `test_wave_ray_families`,
  `test_kerengonen`, `test_loop_binding`, and every module that declared a
  width now declares `N`.

Part 2, the same day (`cleanup/law-of-the-bit-2`):

- keys refused, each naming its rule: `ray_slots` on a spatial field
  (`lanes-v1`: the lanes bound the Node, no budget per family; the
  definition has no `ray_slots`, `rays_per_tick` is at most 4096 on its
  own); `self_exclusion` on a spatial field, `kerengonen.capture` and
  `kerengonen_mirror` on an emission (the record-as-owner field program,
  Highlights 5.4 point 22 and the settled rule (v)); the `capture` and
  `self_exclusion` fields of `SpatialFieldDefinition` and the `mirror` field
  of `EmissionDefinition` are gone, `participant_groups` takes a `capacity`;
- the record-as-owner program's test modules deleted (`test_kerengonen`,
  `test_energy_audit`, `test_ray_integration_guards`,
  `test_ray_merge_contracts`, `test_native_ray_coupling`,
  `test_spatial_coupling`, `test_spatial_interactions`,
  `test_spatial_transport`, `test_spatial_decay`,
  `test_ray_coupling_evidence`, `test_local_field_rules`,
  `test_node_rule_contract`) with `examples/generic-ray-coupling/` and
  `examples/kerengonen-double-slit/`; the slot budget's case of
  `test_ray_field`;
- the ledger: the `shadow_sources` line (always zero since
  `node-is-ports-v1`) is gone with `record_shadow_sources`; a body under a
  table takes the recoil on its own line, booked on `returned`; the prefill
  merges a third phase on one lane by the coherence rule; "home" is the
  generic push and its zero-step return, booked as `home_pushes`;
- `examples/nature/bit_law_migration.py` drops `ray_slots` and no longer
  scales slots per layer; every world of the repository lost the key;
- a body at rest claims no lane (`LaneClaims.at_rest`,
  `SpatialLaw.body_things`; its token never departs); the electricity
  reading of the whole charge (the field lane's finding) is measured and on
  the list, a declaration of the charge per thing being the model owner's;
  the record-as-owner
  program's engine (the outward octant field, the record couplings, the load
  delay of departures, `node_execution`, the record's self-exclusion rows) and
  the corner turn's sourced line remain on the pull request's list.

## A click is an absorption, landed on 2026-09-18 (`detector-absorb-v1`)

Issue #169, feature 2c (a click is an absorption;
Highlights 5.4 "A click is an absorption", model owner, 2026-09-18). One new
key, one new default, no existing key changes:

- `detectors[].on_click`: `"absorb"` or `"pass"` for every ray family, or a
  mapping of ray family name to one of them; a family not named keeps the
  default, absorb for a field family (one declared `field_of` another) and
  pass for matter. The default changes what a mark does with a field quantum
  that draws 1: it is absorbed into the mark's counter with its momentum, and
  nothing of it is delivered or spread on; a world that wants the former
  behaviour writes `on_click: "pass"` on its marks. Matter that draws 1, a
  draw of 0 and a ray carrying a bit are unchanged.
- `DetectorMark` gains `on_click` (per spatial field: `CLICK_PASS` 0,
  `CLICK_ABSORB` 1, `CLICK_DEFAULT` -1; empty for all defaults), `click_keys`,
  `counter` (one exact entry per spatial field, empty until the first
  absorption) and `momentum`; `click_coupling`, `detector_absorb` and
  `field_family` in `core/spatial_state.py`; `SpatialAccounting` and
  `SpatialEngine` an `absorbed_by_marks` line; `Simulation` gains
  `detector_marks()`, `detector_mark_totals()` and `detector_mark_momentum()`;
  `ledger_line` takes the seventh value and `world_ledger` the marks' lines.
- Records: a `detector_click` that absorbed carries `absorbed`, the amount; a
  `spatial_received` record of a Node whose mark absorbed carries
  `absorbed_by_mark` (per family the amount and its momentum); `run.json`
  carries `detector_absorb: "detector-absorb-v1"`, `detector_marks`,
  `detector_mark_totals` and `detector_mark_momentum`; every ledger line under
  `audit` reads `absorbed_by_marks` and every ledger carries `marks` (count,
  momentum, counter); `line_balanced` reads a recorded line without the entry
  as zero, so the records of earlier runs re-check as before; the spatial
  accounting reads `absorbed_by_marks`; the local audit's report reads
  `absorbed_by_marks`. A world without marks, or with marks that only draw 0
  or meet rays carrying a bit, writes the same events and states.
- The viewer: a click that absorbed reads "Detector PASS, absorbed" with the
  amount, ends the ray at the mark (`end.kind` `absorbed`) and is counted in
  `eye.counts`; each `eye.clicks` entry carries `absorbed`; `ticks_data` rows
  carry `absorbed` and `in_world` takes both sinks off; `conservation` carries
  `external_body_totals` and `detector_mark_totals`.
- Pins rewritten on 2026-09-18 ([expectations](TEST_EXPECTATIONS.md)):
  `test_ray_viewer.py` (the G clicks absorb) and `test_screen_loop.py` (the
  light line's current and the spreads); `test_ray_event_audit.py` reads the
  new line and block; `test_dense_field.py` gains the `counter` identity
  case; `test_nature_catalog.py` reads the third coupling; the rule's test is
  `test_detector_absorb.py`.
- The catalog decides `apparatus.detector.couplings.on_click`. E9 is
  repeated under the rule (`examples/nature/screen_loop.json`, unchanged):
  265 clicks in 240 ticks, all absorbed, no pass, the count growing to the
  last tick ([E9](EXPERIMENTS.md#e9-the-screen-with-a-loop-source-the-ring-radiating-on-seven-marks)).

## Polarization landed on 2026-09-17 (`ray-polarization-v1`)

Issue #169, feature 11 (polarization;
Highlights 3.26 and 3.19). New keys, no existing key changes:

- `spatial_fields[].polarization_bits` (ray transport only): the family's
  polarization circle, 2^bits steps per half turn; absent, the phase width.
- `emissions[].polarization`: `"none"` (the default) or a step of the
  field's circle, the polarization of every ray the lamp emits.
- `polarization` on a ray meeting's output: `"same"` (the default, the
  source input's), `{"of": i}`, `"none"` or a step.
- `external_bodies[].coupling` takes `"polarizer"`, with
  `external_bodies[].polarizer` (`family`, `angle`, `pass`, `table`,
  `unpolarized`).
- `Ray.polarization` (-1 none) on every ray, last in `ray_merge_key`;
  `RAY_PROPERTIES` gains the read-only view `polarization` (index 8) and
  `InteractionDefinition` the fields `polarization_declared` and
  `output_polarization`; `ExternalBody` gains `polarizer`, `held` and
  `held_phases`; `emit_rays` takes `polarization`.
- Records: a `polarizer` event per arriving ray at a polarizer body, the
  body's `held` and `held_phases` in `external_bodies()`, its `polarizer`
  declaration in the runner's `external_bodies` entry, and
  `ray_polarization: "ray-polarization-v1"` in `run.json` when the world
  declares the property anywhere. The viewer's `runs.json` segments carry
  `polarization`. A world that declares none is byte-identical, its costs
  included: a rule that does not name the property reads the view it read
  before and its outputs carry their source input's polarization without an
  assignment.
- The catalog decides `rays.light.polarization` (`transverse`, with
  `polarization_bits` `"default"`), the electron's and the positron's
  `polarization_bits` 1 (spin), and the `polarizer` coupling with its
  reference table; the undecided table loses those two rows. A12 is
  measured (`examples/nature/a12_malus/`).

## A spatial plan is validated once, when it is made, on 2026-09-17

The second of the two levers scheduled in
Run performance:
the Node boundary's `validate_spatial_plan` runs once per evaluated plan, at
the execution, before the plan is returned or retained, so a plan-reuse hit
is served a plan validated at its miss and the Node validates only what it
changes after planning (an external body's part, whose registers are outside
the key). Host work only; every run record is byte for byte the same (the
measurement is recorded in
Run performance).

- `NodeExecution` (`core/node_execution.py`) takes `spatial_validator`, a
  `SpatialValidator` (`Callable[[SpatialPlanningInput, SpatialPlan], None]`),
  and calls it on every spatial plan it evaluates, serial or batched;
  `DisturbanceEngine` installs the Node boundary's check.
- `SpatialEngine` takes `planner_validates` and `SpatialServices` carries it
  (default `False`): `True` when `planner` validates every plan it returns
  (the execution's reuse adapter, or parallel execution, whose batches serve
  every request); a law installed on the services directly does not
  validate, and the Node validates each of its plans as before.

## The spatial plan key drops the world tick on 2026-09-17

The first of the two levers scheduled in
Run performance:
the spatial law reads nothing from the clock, so the tick left the plan-reuse
key and the law's signature, and a Node whose local input repeats reuses its
plan across ticks. Host work only; every run record is byte for byte the same
(the measurement is recorded in
Run performance).

- `SpatialPlanningInput` (`core/node_execution.py`) has no `tick` field; its
  fields are `states`, `records`, `received`, `node_cost`, `rays`, `ray_hold`,
  `remainders` and `remainder_phases`.
- `SpatialLaw.__call__` (`fields/spatial_plan.py`), the `SpatialPlanner`
  callable and `NodeExecution.spatial` take no `tick` argument; `rays` is
  followed by `ray_hold`. The Node's clock check (`node clock must be
  nonnegative`) stays in `SpatialNode.plan_cycle`.

## A push keeps the walk on 2026-09-17 (`ray-momentum-turn-v2`)

Issue #169, feature 8b ([a free ray turns by
momentum](SPATIAL_FIELDS.md#a-free-ray-turns-by-momentum-ray-momentum-turn-v2),
"a push keeps the walk"), the fix the helium-orbit run
([E8](EXPERIMENTS.md#e8-the-helium-ion-with-the-field-spreading-and-the-momentum-turn)) asked
for: under `ray-momentum-turn-v1` `pushed_ray` reset the DDA's three
accumulators to (0, 0, 0) at every push, so a ray pushed at every interval,
every ray in a spreading field, stepped along its register's dominant axis
and never turned gradually, against the feature's own statement. Engine and
identity only; no schema key, record field or world file changes:

- `pushed_ray` keeps the accumulators through a push (`continued_walk` in
  `spatial_state`): the walk's progress, the momentum-intervals banked per
  axis toward the next Link, continues against the new register, so a ray
  pushed at every interval walks the DDA line of its running register. A
  first push lifts the progress of the default walk by the amount (zero on
  a unit-axial heading); a push back to the default, and a push that
  shrinks the register below the banked progress (an accumulator outside
  (-length, length] of the new length), start the walk over at (0, 0, 0),
  as every push did under v1.
- `RAY_MOMENTUM_TURN` is `ray-momentum-turn-v2`, and the runner records
  `ray_momentum_turn: "ray-momentum-turn-v2"` when any push happened. A
  record made under v1 in which a pushed ray had progress banked when a
  push arrived is not reproduced: E8's escape and the A5 runs of that day
  were recorded under v1 and are not repeated with this note. A world where
  no push happens, and a push that finds the accumulators at zero (the
  first push of a ray on a unit-axial line, every push of
  `test_ray_momentum_turn.py`), are byte-identical.
- `test_momentum_turn_walk.py`
  (expectations) pins
  the staircases of a push of 1 and of 8 per interval on a ray of 64, the
  flip, the cancel, the shrink and the lift by hand, and two boards where a
  field ray meets the ray at every Node. `test_helium_orbit.py`'s pins were
  re-read under v2 and are unchanged, the kept walk taking the same -X
  Links on that board (expectations).

## Binding as a loop landed on 2026-09-17 (`loop-binding-v1`)

Issue #169, feature 14 ([binding as a
loop](SPATIAL_FIELDS.md#binding-as-a-loop-loop-binding-v1), [loop
binding](LOOP_BINDING.md); Highlights 3.4, "Binding is a periodic orbit of the
meeting rule", model owner, 2026-09-17). A ray never stops: a bound group is a
set of rays in motion on a ring of Nodes whose corner meetings, under an
ordinary `ray_interactions` rule with outputs, reproduce the rays that entered
them; nothing holds and nothing registers. Removed from the engine and the
schema, as the design's section 9 lists:

- The binding form of a rule without outputs (assignments of `delay` 1 as a
  hold): a rule meets only rays that arrived at the Node, so the output of a
  rule waiting its declared delay at its event Node (an event ray with
  `steps` 0) is met by nothing there and leaves; no rule can hold its
  participants by meeting them again (`_meet` in `fields/ray_interactions.py`).
  A `delay` assignment or output is a wait, as the
  shared coupling always said.
- The `ray_delay` key of a rule and the Node's `bound_delay` wait,
  `bound_group`, `held_ray`, the snapshot's `bound_groups`, the `bound_tick`
  record, and the six-heading release of a held ray in `release_field` (a
  ray waiting under a delay releases the five headings other than its own in
  every interval it is there, as any ray).
- All of `bound-group-motion-v1`: `BoundMotion`, `SpatialNodeState.bound_motion`,
  `SpatialPlan.bound_delay`, `bound_port` and `bound_push`,
  `SpatialPacket.group`, `InventoryNode.group`, `InventoryPacket.group`,
  `SpatialPlanningInput.bound_port`, `group_step`, `group_content`,
  `group_momentum`, `group_momentum_field`, `carry_rays`, `free_rays`,
  `bound_group_step`, the escape's `bound_group` entry, `momentum_table` on a
  rule that assigns, the ledgers' reading of a group by its register, and the
  runner's `bound_group_motion` key; `BOUND_GROUP_MOTION` is gone,
  `motion_step` stays for the external body.
- A world that declares `ray_delay` on a rule, or `momentum_table` beside
  `assignments`, is rejected at initialization with a message naming this
  note. The world key `ray_delay` of the computation-field hold is a
  different rule and is unchanged.

What stays, unchanged: the outputs rule and its `delay` output as an
output-clock wait, the delay table and the lag register (`ray-binding-v1`
keeps its identity for gravity by delay; `test_ray_binding.py` keeps the
`gravity` and `criterion` cases with resident content, a record holding
stock, as the mass), the momentum register of a free ray and `momentum_table`
on a coupling of free rays and on the external body, the released field with
its spreading and remainder, the external body, and the Node's five-step law.
New: `LOOP_BINDING = "loop-binding-v1"`, recorded by the runner as
`loop_binding` beside `ray_binding`; the reading of a group from the record in
the ray viewer's extractor (`periodic_groups`: a run document's `groups`, each
ray's `group`, each tick row's `bound`; `phase_steps` read from `phase_bits`);
`tests/test_loop_binding.py`. Re-pinned with dated notes: the `state.json`
digests of `test_ray_momentum_turn.py` (`meeting`) and
`test_field_spreading.py` (`unchanged`), whose snapshots lost the
`bound_groups` key; the viewer test's release lines (five headings from a
waiting ray). Deleted: `tests/test_bound_group_motion.py`, the
`binding`, `unbinding` and `ray_delay` cases of `test_ray_binding.py`, the
`group` world of `test_ray_momentum_turn.py`, the screen geometry test of
`test_ray_viewer.py`. The catalog's `binds` entries are corner tables
(`outputs` with a `closes` note; catalog). The nature examples
`absorption.json`, `absorption_emission.json` and `photofission.json` are
rewritten as loops (E1 to E3 measured again); `screen.json` and
`screen_spread.json` are retired with their records kept (E6).

## A free ray turns by momentum on 2026-09-17 (`ray-momentum-turn-v1`)

Issue #169, feature 8b ([a free ray turns by
momentum](SPATIAL_FIELDS.md#a-free-ray-turns-by-momentum-ray-momentum-turn-v2)),
the second gap the helium-ion run found (E4, "the missing rules", ii): a
free ray's heading changed only by whole Ports or by the lag of feature 8,
so no curved path of a free ray was expressible. The momentum register of
feature 8c now belongs to every ray:

- `Ray.momentum`, three integers or `None` for the default amount x
  heading; every existing ray and record is unchanged where no push
  happens. `ray_vector` is what the DDA walks (`forward_rays`, the lag
  spending, the event stamp of a rule's outputs), `ray_line` the unit-axial
  line the release geometry skips (`release_field`), `ray_momentum_vector`
  what the ledgers read (`ray_momentum`, the local audit), `pushed_ray` the
  push, `turn_receiver` the role a free-ray table pushes; `dda_step` walks
  any nonzero bounded vector (`vector_length`); `return_ray` negates the
  register; `ray_merge_key` includes it and `merge_rays` sums it; a rule
  that assigns a new heading clears it (`_replacement`).
- A `ray_interactions` entry without outputs and without assignments may
  declare `momentum_table` naming a participant family
  (disturbances); the parser
  admits it without `assignments` and `validate_ray_participants` requires
  exactly one unnamed role. `apply_ray_interactions` takes a `turns` list
  beside `bound` and `pushes`; `_table_pushes` is the shared scan of the
  field rays a table meets (the group's push reuses it).
- New record `ray_push` (family, amount, the register before and after, the
  field family, its amount and heading), published before the cycle's
  record from `SpatialPlan.ray_pushes` (`RayPush` in the Node state
  contract); the runner records `ray_momentum_turn: "ray-momentum-turn-v1"`
  when any push happened, and a free-ray table alone no longer marks
  `bound_group_motion`. `test_ray_momentum_turn.py` pins the digests of two
  worlds without a free-ray table (case (d)).
- The ray viewer's segments carry `momentum` (the register when the
  recording has one, else amount x heading), `momentum_in` and
  `momentum_out` of an event sum it, and the viewer's momentum arrow points
  along it (`tools/ray_viewer/extract.py`, `viewer.html`).
- Not in this slice: absorption of the field ray into the ray, a push and
  an assignment or a delay table on one rule, the lag's own modulus for the
  delay on the ray's own axis (`lag_bits` stays open), the local audit's
  source term for the push (booked to the world ledger only, as the
  group's), and two receivers at one Node in one interval (the first in
  slot order takes every field ray the table names).

## Binding as a loop designed on 2026-09-17 (`loop-binding-v1`, design only)

Issue #169, feature 14 (loop binding; Highlights 3.4,
"Binding is a periodic orbit of the meeting rule", model owner,
2026-09-17). Documents and two world files only; no module, schema key,
record or test changes with this note:

- `docs/LOOP_BINDING.md` states the rule, the unit-square corner table in
  today's schema, the closure condition (`L r = 0 (mod N)`, the presence
  condition, the amounts by the table), dispersal, mass and clock, the
  field of a loop, the ladder count for A10, the motion of a loop and the
  mapping of the interim forms; `examples/nature/ring.json` and
  `ring_open.json` are the unit-square electron and its dispersing control,
  registered as E5 (planned) and in the nature README; the expected
  integers of the future `tests/test_loop_binding.py` are pinned in
  test expectations.
- When the feature is implemented, after feature 8b, the following are
  removed with their own dated note here: the binding form of a
  `ray_interactions` rule without outputs (assignments of `delay` 1 as a
  hold), the `ray_delay` key and the Node's `bound_delay`, `bound_group`,
  the snapshot's `bound_groups`, the `bound_tick` record, the six-heading
  release of a held ray in `release_field`, and all of
  `bound-group-motion-v1` (`BoundMotion`, `bound_motion`, `group_step`,
  `carry_rays`, `bound_group_step`, `momentum_table` on binding rules,
  `SpatialPacket.group`, the ledger's reading of a group by its register).
  A `ray_interactions` rule with outputs, its `delay` output, the delay
  table and the lag, the released field with `spread`, and the external
  body are unchanged; the catalog's `binds` entries become corner tables,
  and the nature examples that use the held form are rewritten as loops or
  retired with their dated records kept.
- The two world files run on today's engine unchanged (the check of
  2026-09-17 on `main` at `c21e03e` agreed with every pinned line); the
  run record's `ray_binding` identity and empty `bound_groups` are written
  for them as for any world.

## Bound groups that move on 2026-09-17 (`bound-group-motion-v1`)

Issue #169, feature 8c ([bound group
motion](SPATIAL_FIELDS.md#bound-group-motion-bound-group-motion-v1)), the gap
the helium-ion run found (E4): a bound group was held at its Node and could
not move, while Highlights 3.28 gives a group moving one Link every k
intervals the speed 1/k. The external body's motion rule now applies to
matter, the same integers:

- A bound group carries a momentum register with three accumulators
  (`BoundMotion`, `SpatialNodeState.bound_motion`, `SpatialPacket.group`,
  `InventoryNode.group`, `InventoryPacket.group`), set at its formation as
  the sum of amount x heading of its rays; it steps one Link when a whole
  content has accumulated on an axis (`group_step`, sharing `motion_step`
  with `body_step`). The planner takes the step Port as an eighth argument
  (`SpatialLaw.__call__(..., bound_port=-1)`, `SpatialPlanningInput.bound_port`),
  reports `SpatialPlan.bound_port` and `SpatialPlan.bound_push`, and a
  held ray released nothing on the heading its group is carried through
  (`release_field(..., carried)`); `carry_rays` in `fields/rays.py`.
- A binding rule may declare `momentum_table` (`InteractionDefinition.momentum_table`,
  disturbances); the named families join
  the rule's layer (`ray_layers`), and `apply_ray_interactions` takes a
  `pushes` list beside `bound`.
- The world ledger and the local conservation audit read a bound group's
  momentum by its register (`held_ray`, `free_rays`, `group_momentum_field`);
  the push is booked as a source of the momentum field the group's families
  bind; a group leaving an open boundary is booked as escaped with its
  content and register (`spatial_escaped` carries `bound_group`). A group
  whose families bind two momentum fields fails closed at formation.
- New record `bound_group_step` (position left, Port, arrival tick, momentum,
  accumulators, content) after the `bound_tick` of that cycle; the
  snapshot's `bound_groups` entries carry `momentum` and `accumulators`
  (`test_ray_binding.py`'s pin updated with a dated note); the runner records
  `bound_group_motion: "bound-group-motion-v1"` when any group stepped or any
  rule declares a table. Events and the run record of a world where no group
  ever has a nonzero register are byte for byte what they were
  (`test_bound_group_motion.py`, case `rest`); `state.json` gains the two
  zero vectors per group. The output-clock delay `bound_delay` of a Node
  returns to 0 when its group departs.
- Not in this slice: two bound groups at one Node (a group arriving at a
  Node that holds one fails closed), absorption of a field ray into a group
  (the table returns it reversed), and the local audit's source term for
  the push (booked to the world ledger only, as the momentum a split moves).
## The Node owns the sub-quantum remainder on 2026-09-17 (`field-remainder-v1`)

Feature 12b of the ray-event model,
the model owner's decision of 2026-09-17 in Highlights 3.5 and 3.17 (the
split and the remainder in [field
spreading](SPATIAL_FIELDS.md#field-spreading-field-spreading-v1)), which
supersedes the phase-selected heading of `field-spreading-v1`:

- In the spread step the whole quanta per heading leave as before; the share
  below one quantum, content x weight mod S in units of 1/S (S the table's
  total), goes to the Node's remainder register of that family, source sign
  and Port, eighteen per spreading family, the register's phase combined
  with the share's by `phase_of_sum` weighted by amount; a register that
  reaches S releases the whole quanta it holds (k for kS) through its Port
  in the same interval, with the register's phase and sign, as a fresh
  eventless field ray, and keeps the rest. A Node with a nonzero register
  stays active until it is empty. A quantum of amount 1 no longer turns by
  its phase: it fills the forward register by 6/11 per arrival and the
  others by 1/11.
- New in `core/spatial_state.py`: `FIELD_REMAINDER`, `REMAINDER_SIGNS`,
  `REMAINDER_SLOTS`, the type `Remainders`, `remainder_slot`,
  `blank_remainders`, `validate_remainders` and `remainder_stock`;
  `SpatialNodeState.remainders` and `remainder_phases` (one block of
  eighteen per spreading family, `()` for the rest), `SpatialPlan.remainders`
  and `remainder_phases`, `SpatialPlanningInput.remainders` and
  `remainder_phases` (part of the plan-reuse key), `InventoryNode.remainders`;
  `spread_content` takes the registers and their phases and returns the
  departures, the record and both after the step; `spread_remainder_entry`
  is deleted. `FieldSpread` and the `field_spread` record replace
  `remainders` by `released` (the quanta the registers released per Port),
  `stored` (the whole quanta the registers gained net of the releases) and
  `registers` and `register_phases` (the eighteen after the step,
  sign-major -1, 0, 1 then Port); `amounts` includes the releases.
- The snapshot (`state.json`, the viewer's frames) carries `field_remainders`
  when a family spreads: every nonzero block, with `position`, `family`,
  `sign`, six `registers`, six `phases` and `total`. The world ledger counts
  the registers as current content: `totals` and `charge_totals` add a
  Node's registers of a family as their sum over S, exact because the
  weights sum to S (`remainder_stock` rejects any other block), with no
  momentum; the local audit reads the same registers and the record's
  `stored`, so its residual stays zero. A register never escapes.
- The runner records `field_remainder: "field-remainder-v1"` beside
  `field_spreading` only when a family declares `spread`; a world that
  declares none runs byte-identically (the `unchanged` case still pins the
  hashes of main `f3809be`). `test_field_spreading.py` is repinned
  (expectations): the `quantum` case
  becomes `stream` (a ray of amount 1 fills the forward register by 6/11 per
  arrival and the transverse by 1/11; the second quantum releases forward
  after two arrivals, a transverse quantum after eleven), the Detector of
  the `returned` case moves to (7,7,7), and every case checks the ledger at
  every tick. The screen run `examples/nature/screen_spread.json` was rerun
  (E6): see the
  README.

## Field spreading added on 2026-09-17 (`field-spreading-v1`)

Feature 12 of the ray-event model,
the model owner's decision of 2026-09-17 in Highlights 3.5 ("Light is the
field, and the field spreads"; [field
spreading](SPATIAL_FIELDS.md#field-spreading-field-spreading-v1)):

- `spatial_fields[i].spread`, ray transport only: six nonnegative integer
  weights in Port order relative to the arriving heading (forward, backward,
  the four transverse in Port order), the backward one positive and the four
  transverse equal; the sum is the denominator. Every Node that content of
  the family reaches releases it again by the table, after the marks and
  the meetings of the interval and before the departures: amounts add per
  arriving heading, the phase is the phase of the coherent sum, whole quanta
  by the table, the remainder whole through the entry the phase selects
  (until `field-remainder-v1`, above). A
  world that declares no `spread` runs byte-identically, its run record
  included (`test_field_spreading.py`, `unchanged`, pins the record hashes of
  the released-field world on main `f3809be`).
- New in `core/spatial_state.py`: `FIELD_SPREADING`, the definition key
  `spread`, `FieldSpread` (the plan's record, in `STATE_RECORDS`),
  `validate_spread_table`, `validate_spread_fields`,
  `validate_spread_admission`, `relative_ports`, `spread_remainder_entry`
  (deleted by `field-remainder-v1`),
  `spread_phase`, `spread_content` and `spreading_field_names`;
  `SpatialPlan.spreads`. The spatial law's `_spread` runs per ray field after
  the inverse split and before forwarding.
- A new record kind, `field_spread`, per Node, interval and family (`family`,
  `amount`, `arrived`, `amounts`, `remainders`, `phase`, `coherence`;
  `remainders` replaced by `field-remainder-v1`),
  published before the cycle's `spatial_cycle` record; the ray viewer's
  extractor lists it among its silent kinds and shows the spread as a
  release. The momentum a spread moves is an explicitly accounted source of
  the family's momentum field, so `source_totals` and the ledger's `sourced`
  line carry it and `conserved_at_every_completed_tick` stays the identity;
  the local conservation audit reads the record and reports the same term.
- The runner records `field_spreading: "field-spreading-v1"` and
  `spreading_fields` only when a family declares `spread`.
- `Ray.source_sign` (Highlights 3.5, the field is matter's message about
  itself): -1, 0 or 1, the sign of the releasing family's charge (a body's
  declared charge), set by `release_field`, `release_stock` (which now takes
  the origin definition) and `body_release`, part of `ray_merge_key`, kept
  by the return, copied by `transmit`, carried by a meeting's output from the
  input of its own family and by the spread per sign; 0 on every ray of an
  existing world, so nothing else changes. `FieldSpread.signs` and the
  record's `signs` list the signs the spread took.
- A returned field quantum of a spreading family (the orchestrator's
  proposal of Highlights 5.5, pending the model owner's decision,
  implemented exactly): it walks back past the Node that spread it with its
  steps at 0 (`advance_ray` and `forward_rays` walk an eventless returning
  ray on, `_inverse_split` skips it), is restored to the record that emitted
  its family or ended at content of its origin family or of a family a rule
  couples with it (`SpatialLaw._returned`, a negative source of the field
  and its momentum field), may escape (`SpatialEngine._escape` lets an
  eventless returning ray of a spreading family out); `ReturnedField` (in
  `STATE_RECORDS`), `SpatialPlan.returned` and the record `field_returned`,
  which the local audit and the viewer read.
- A spreading family needs a phase width of at most twelve bits, not a
  declared coherence table: the coherent sum uses the table of the modulus
  (`spread_tables`, `spread_phase`, `spread_coherence`).
- The catalog: `rays.light.spread` is declared, `[6, 1, 1, 1, 1, 1]`, and
  `rays.light.source_sign` is `releaser`; the undecided table loses the
  spread row and `test_nature_catalog.py` builds the light family with its
  table.
- A defect fixed: a record holding stock of a family with a released field
  released nothing, because `SpatialNode.plan_cycle` returned early as idle
  before `SpatialLaw._release` ran (`SpatialEngine.begin` scheduled the Node
  through `holds_source_stock`, the cycle then left); the resident-content
  sentence of `released-field-v1` (Highlights 3.5) was not honoured and no
  test covered `release_stock`. The idle exit now counts such a record as
  active, so resident stock releases every interval on all six headings,
  booked as a source; a world whose records hold stock of such a family
  changes accordingly (none of the shipped worlds and tests does, the lamps
  emitting their whole stock at once), pinned by the `resident` case.
- Tests: `tests/test_field_spreading.py` (single, superposition, cancelled,
  quantum, sign, returned, source, resident, rejected, unchanged;
  expectations).
## The Detector's bit as a property on 2026-09-17 (`detector-bit-property-v1`)

Issue #169, feature 2b (the bit as a property,
the bit read;
Highlights 5.4, model owner, 2026-09-17):

- A marked Node reads the bit a ray carries before it draws: a ray carrying
  1 passes without a draw and a ray carrying 0 (a transmission) is never
  drawn, each recorded as a `detector_pass` event (position, tick, Port,
  family, amount, `bit`), and only a ray carrying no bit is drawn. A mark
  that wants the draw of `detector-mark-v1` on such arrivals writes
  `on_bit_1` or `on_bit_0` as `"draw"` on its `detectors[]` entry; the
  default is `"pass"`, and any other value is rejected. `DetectorMark`
  gained `on_bit_1`, `on_bit_0` (`BIT_PASS` 0, `BIT_DRAW` 1) and `bit_keys`,
  all defaulted, so a typed mark of three or four arguments parses and
  compares as before.
- The outputs of every ray interaction that fires, with outputs or with
  assignments, inherit the Detector bit of its inputs: the highest by the
  order 1 over 0 over none, unless the rule declares `bit` (`"highest"`,
  `"none"` or `{"of": i}`); `stamp_event` takes the bit as a third argument
  and `inherited_bit` is the rule. Before, a meeting's outputs carried no
  bit; a world in which a marked ray met another ray changes there. An
  external body's coupled token inherits the bit and is stripped as before;
  a release carries none.
- `RAY_PROPERTIES` gained the read-only view `detector` (0 none, 1 a draw
  of 0, 2 a draw of 1), readable by a `when` guard or an invariant as
  `charge` is; an assignment to it is rejected. A world with ray
  interactions reads one more view component per participant (`read` cost
  10 instead of 9, the cost line of its `spatial_cycle` records and its
  `computation` report accordingly), as `wave-ray-family-v1` added two; the
  pin of `RAY_PROPERTIES` in `test_wave_ray_families.py` lists it.
- The runner records `detector_bit_property: "detector-bit-property-v1"`
  when a mark writes either coupling key or a rule writes `bit`; a world
  that declares neither is recorded as before, and its `events.jsonl` and
  `run.json` are byte for byte what they were unless a marked ray reaches a
  second mark or meets another ray (checked on the worlds of
  `test_detector_mark.py`, `test_detector_return.py` and
  `test_inverse_split.py`).
- `tools/ray_viewer/extract.py` reads `detector_pass` as the event kind
  `pass` (a marker like a click, in the captions) and carries each ray's
  `bit` (`null`, 0 or 1) in `runs.json`; `style.json` and the page's default
  style gained the kind.
- `catalog/nature.json`: the Detector's couplings `on_bit_1` and `on_bit_0`
  are decided, with their world keys and the engine identity, and
  `docs/CATALOG.md` lists two undecided entries fewer (29).

## Ray-event audits on 2026-09-17 (`ray-event-audit-v1`)

Issue #169, feature 10 (audits,
the world ledger):

- `Simulation.audit()` returns the world ledger at the current tick; the
  runner records one per completed tick under `audit` and
  `ray_event_audit: "ray-event-audit-v1"`, and `tools/ray_viewer/extract.py`
  carries `audit` in its `conservation` entry.
- `conserved_at_every_completed_tick` changed meaning: it is the ledger's
  identity, initial + sourced = current + escaped + annulled + absorbed, for
  amount, momentum and charge at every completed tick. It read false after
  an escape or an annulment before; escaped and annulled content are ledger
  lines, not losses, so an open world with escapes now reads true, and a
  dissipative world (schema 2) still reads false. Pins updated with a dated
  note: `test_inverse_split.py` (`annul`), `test_ray_viewer.py`,
  `test_ray_integration_guards.py`, `test_disturbance_application.py`
  (expectations).
- `charge_totals()` counts the stock a record holds of a charged family,
  the owners `totals()` reads, beside the rays; `escaped_charge_totals()` is
  a new readout, and the ledger's `absorbed` line is `external_body_totals()`
  (`external-body-v1`), with the bodies' own count, momentum, charge and
  sinks under `bodies`. The charge case of `test_wave_ray_families.py` reads
  the lamps' charge before the first tick.
- The local conservation audit measures charge as a fifth quantity when a
  family declares one, reported as `charge` beside `energy` and `momentum`;
  a world without a charged family reports as before. It reads every field
  release as a source at its Node and reports the sum as `sourced`, so a
  world with a `field_of` family may declare `conservation` (the viewer's
  world declares it again; its residual momentum (1, 0, 0) of 2026-09-17
  was the momentum of a single held ray's release, not a packet defect).
- A `ray_interactions` rule with outputs whose family's charge differs from
  the charge of the inputs its amount comes from is rejected at validation.

## Historical particle candidates deleted on 2026-09-17

The model owner's instruction of 2026-09-17, recorded in
[HIGHLIGHTS.md](HIGHLIGHTS.md) sections 3.3, 3.4, 3.5, 3.19, 3.20, 5.1 and 5.4
and in RAY_EVENT_MODEL.md section 6, is that everything
not used is deleted. Issue #164, bucket A, removed the unused historical
particle candidates from the package, tests, tools and documents:

- `core/scalar_engine.py`, `core/linked_engine.py`, `core/streaming_engine.py`,
  `core/streams.py`, `core/links.py`, `core/lattice.py`, `core/contracts.py`,
  the `models/` and `dynamics/` packages, `fields/scalar.py`, `fields/policies.py`,
  `fields/halo.py`, `fields/geometry.py`, `fields/streaming.py`, `particle_api.py`,
  `particle_scenarios.py`, `legacy_runner.py`, `compat.py`, `diagnostics/render.py`,
  `diagnostics/live.py`, `diagnostics/frames.py`, `diagnostics/measurements.py`,
  `diagnostics/recorder.py` and `diagnostics/invariants.py`;
- the notebook facade `src/persistent_source_field.py`, the diagonal-motion tool
  `tools/check_diagonal_motion.py` and the frozen archive `tests/reference/`;
- the public names `ScalarSimulation`, `LinkedSimulation`, `BalancedSimulation`,
  `CausalStreamSimulation`, `Config`, `NodeState`, `ParticleState`, `LinkConfig`
  and `CausalStreamConfig` from the `event_universe` package;
- their tests, the historical run-capture, live-display and renderer tests, and
  the documents `SCALAR_FIELDS.md`, `BALANCED_MOTION.md` and `CAUSAL_STREAM_FIELD.md`.

There is no replacement API: the active `Simulation` is initialization-defined
(DISTURBANCES.md), shared bounded arithmetic is
`core/integer.py`, and `pytest --visualize-runs` now only enables the
visualization-marked tests. `core/state.py` was deleted in the next step,
below. Dated validation records keep their original scope.

## Shared quantum resource and integration layer deleted on 2026-09-17

Under the same instruction, issue #164 buckets B.1 and B.2 removed the shared
quantum resource and the integration layer built on it, following
[HIGHLIGHTS.md](HIGHLIGHTS.md) sections 3.18 (deleted), 3.19, 3.20 and 5.4
and RAY_EVENT_MODEL.md section 6, steps 3 and 4: no
owner answers at a distance, the Detector is a marked Node and every
alternative is an event on the board.

- The `quantum/` package (`deferred`, `event_network`, `event_rules`, `focus`,
  `mixed`, `state`, `query`, `terminal`, `postulates`, `wave_origins`,
  `operations`, `contact_outcomes`, `contact_rules`) and the `integration/`
  package (`event_program`, `event_runtime`, `contact_program`,
  `contact_runtime`, `causal_contact_runtime`, `recurrent_contact_runtime`,
  `quantum_entities`, `quantum_bridge`, `quantum_contact_trial`,
  `quantum_event_trial`) are gone.
- The `event_program` initialization member and `InitialState.event_program`
  are gone: a document that still carries the member is rejected as an unknown
  key, no configuration selects a native program, a quantum profile or the
  classical `causal-events-v1` ledger, and `causal-events.jsonl` is no longer
  written. `Simulation` no longer refuses `node_workers > 1` for a program.
- `event_universe.entities` compiles classical profiles only: the
  `representation` argument, the `--representation` option, the
  `quantum_profile` binding key and the `quantum` count of `validate_profiles`
  are gone, and the 46 `quantum_profile` members left
  `examples/known-entities/representation-probes.json`.
- `core/state.py` and `tests/test_integer_contract.py` are gone;
  `fields/source_envelope.py` imports `bounded_gcd` from `core/integer.py`.
- `examples/quantum/`, `examples/quantum-classical/`,
  `examples/catalog-contact/`, `examples/spatial_causal_events.json`, the
  relativity probes `quantum_gravity.py`, `quantum_from_the_side.py` and
  `time_symmetry.py`, the three quantum entity-audit inputs and the
  contact-fields experiment of the named-particle gallery are gone;
  `examples/spatial_computation_delay.json` lost its `event_program` member.
- The twelve quantum documents named in the [documentation index](README.md),
  the `quantum-contact-trial` workflow, 36 test modules and the fixtures
  `tests/quantum_detector_fixture.py`, `tests/support/quantum.py` and
  `tests/support/contact.py` are gone; the Node-level source-envelope and
  event-ledger cases of `test_causal_contact_fields.py`,
  `test_null_notices.py` and `test_native_event_runtime.py` moved to
  `test_active_node_contracts.py`, `test_null_notices.py` and
  `test_event_links.py`.

There is no replacement API. `core/event_space.py`, `core/event_links.py`,
`core/event_resolution.py`, the source-envelope modules, the bond registry,
claim/gather and `fields/record_operations.py` stay until buckets B.3 to B.6
of the same issue. The source-envelope modules, the causal event ledger and
the bond registry were deleted in the next steps, below.

## Source envelopes deleted on 2026-09-17

Under the same instruction, issue #164 bucket B.3 removed the source
envelopes, following [HIGHLIGHTS.md](HIGHLIGHTS.md) section 3.5 and
RAY_EVENT_MODEL.md section 5 (row R5) and section 6,
step 7: a field is the ray's own information spreading in ray form to the
Nodes around it, and no Node retains a source envelope.

- `core/source_envelope_node.py`, `core/source_envelope_state.py`,
  `core/source_emission.py`, `core/source_emission_node.py`,
  `fields/source_envelope.py` and `fields/source_emission.py` are gone, with
  the `CausalSourceResolver` protocol of `core/event_resolution.py`,
  `SpatialEngine.commit_source` and its `spatial_envelope_source` event, the
  `source_envelope` member of the disturbance NodeState and the envelope
  records of the formula-free state audit in `diagnostics/node_contract.py`.
- `tests/test_source_envelope.py` and `tests/test_null_notices.py` are gone;
  the envelope cases of `test_active_node_contracts.py` and
  `test_node_state_contract.py` and the envelope rows of the architecture
  gate went with them. No example declared an envelope source, so no example
  or `tools/check.py` consumer row changed.

## Causal event ledger deleted on 2026-09-17

`core/event_space.py`, `core/event_links.py` and `tests/test_event_links.py`
were deleted on 2026-09-17 under issue #164 bucket B.4, following
[HIGHLIGHTS.md](HIGHLIGHTS.md) section 3.20 and the "Where is state stored"
row of RAY_EVENT_MODEL.md: all the information is on
the rays, the origin Node keeps nothing and there is no register.

- `DisturbanceEngine` and `SpatialEngine` no longer accept `event_space=`.
  `NodeEvents(observer)` takes the observer alone; `message()` builds the
  observer message that `publish()` sends, and `record()`, `require_room()`
  and `enabled` are gone. Observer messages carry no `event_id` or `parents`.
- `Packet`, `LocalPlan`, `PendingCycle`, `SpatialPacket` and
  `PendingSpatialCycle` lost `cause_id`; `SpatialNodeState` lost `cause_id`,
  `sample_cause_id` and `cost_cause_id`; `DisturbanceNodeState` lost
  `cause_id`, `event_cursors` and `event_references`; `NodeView` lost
  `event_heads` and `event_origins`; `LocalContext` lost `cause`.
- `computation_report()` no longer reports `causal_events`,
  `causal_event_capacity`, `event_ledger_cost` or
  `carrier_model_operations_cost`; `state.json` and recorded frames carry no
  `event_support`, and the playback page draws none. The profile tool reports
  no `event_history_enabled`.

There is no replacement API. `core/event_resolution.py` and
`fields/record_operations.py` stay until bucket B.6 of the same issue.

## Bond registry, claim-gather, lottery capture and occupied-links guard deleted on 2026-09-17

Under the same instruction, issue #164 bucket B.5 removed the last owners that
answered at a distance, kept a register at a Node or made a ray wait for room
([Highlights](HIGHLIGHTS.md) 3.18 deleted, 3.19, 3.20, 5.1 and 5.4;
ray-event model section 5 and section 6 step 5):

- `fields/bonds.py` (`BondRegistry`), the ray fields `bond`, `train` and
  `homing`, the `Claim` record, the spatial-field keys `bond` and `claim`, the
  emission keys `bond_field` and `train_field`, the absorb-rule keys
  `bond_setting`, `claim` and `capture_salt`, the Kerengonen
  `"capture": "lottery"` and `capture_seed`, the record rows `absorb_tickets`
  and `absorbed_trains`, the runner metadata `spatial_claims` and
  `spatial_bonds`, the sampling profile `historical-autonomous-v1` and the
  planner argument `claims`: the spatial planner now takes states, records,
  received count, node cost, rays, tick and ray hold;
- the pre-planning refusal "outgoing spatial links are occupied": there is no
  occupied channel and no capacity rule, rays leaving on one Link in one
  interval travel in one packet, and
  `SpatialNode.require_free_links` rejects at commit a departure that would
  overwrite a packet still in transit, a host scheduling error rather than a
  physical rule;
- the examples `bell-chsh/`, `kerengonen-bell/`, `claim-gather/`,
  `gathered-gravity/`, `research/bell-postulate-22/` and the ray-gallery
  panels `4-bonded-pair`, `5-claim-gather` and `8-lottery-detector`; the
  double-slit probe's lottery columns; the redshift sweep reads its train by
  arrival order instead of a claim-stamped label;
- the tests `test_bonds.py`, `test_ray_bell_chsh.py`, `test_kerengonen_bell.py`,
  `test_claim_gather.py`, `test_research_sampling_admission.py` and
  `test_gathered_gravity.py`, and the lottery cases of `test_kerengonen.py`,
  `test_ray_integration_guards.py` and `test_detector_sampling_contract.py`.

There is no replacement API: `capture` is `share` or `threshold`, and the
Detector mark of Highlights 3.19 (issue #169, feature 2) will own the ticket
sequence that `core/spatial_state.py` keeps (`TICKET_MODULUS`, `next_ticket`,
`ticket_draw`, `phase_cosines`). `core/event_resolution.py` and
`fields/record_operations.py` stay until bucket B.6; the source-envelope
modules went with bucket B.3 and the causal event ledger with bucket B.4 on
the same day.

## Ray hidden state added on 2026-09-17 (`ray-event-state-v1`)

Issue #169, feature 1, the first implementation step of the
ray-event model (step 2) under
[Highlights](HIGHLIGHTS.md) 3.3, 3.19, 3.20 and 5.1: every ray carries the
number of steps it has made since its event and the information of that
event, as hidden variables that no rule reads
(ray state).

- `Ray` (`core/spatial_state.py`) gains `steps`, `outbound`, `event_ports`,
  `event_shares` (six bounded entries in Port order) and `detector`, all with
  defaults, so a `Ray(heading, accumulators, amount, ...)` call still
  constructs; `validate_rays` bounds them; `advance_ray` counts `steps` up
  while outbound and down on the walk back and moves the phase the same way;
  `merge_rays` keys on them, so rays of different events never merge;
  `emit_rays`, a mirror's reflection and a firing `ray_interactions` group
  stamp every ray they create with the event's mask and shares.
- The runner records `ray_state: "ray-event-state-v1"` in `run.json` beside
  `sampling_profile`.
- Behavior of existing worlds is unchanged except where rays of different
  events used to merge: `ray_count` and slot use count events, and one-Link
  self-exclusion excludes exactly the departure cycle's rays, so a moving
  absorber-emitter absorbs its earlier cycle's quantum back
  (`test_energy_audit.py`, expectations).
- Tests that construct rays or compare emitted or interacted rays directly
  include the stamp (`test_ray_field.py`, `test_native_ray_coupling.py`,
  `test_ray_merge_contracts.py`, `test_ray_integration_guards.py`).

No initialization key changes. No rule, coupling, absorber, readout or
Detector reads the new fields in this step.

## Node Detector bit added on 2026-09-17 (`detector-mark-v1`)

Issue #169, feature 2, migration step 3 of the
ray-event model under
[Highlights](HIGHLIGHTS.md) 3.19, 3.20 and 5.4: a Node marked in the
initialization draws one bit per arriving ray from its own ticket stream and
is otherwise an ordinary Node
(Detector mark).

- New optional initialization key `detectors`: a list of marks, each with
  `position`, `setting` `[n, d]` and `seed`, all required, no default rate,
  one mark per position, admitted only under the shared Detector admission
  (schema 1, `link_ticks` 1, ray fields on the links metric at pace 1/1
  without decay, unit-axial headings closed under negation)
  (schema).
- `DetectorMark(position, pass_numerator, pass_denominator, seed)`,
  `DETECTOR_MARK`, `MAX_DETECTORS`, `detector_draw` and `ray_merge_key` in
  `core/spatial_state.py`; `InitialState.detectors`;
  `SpatialNodeState.detector` and `detector_ticket`, installed by
  `SpatialEngine` when a marked Node is created.
- `SpatialNode.receive` draws once per arriving ray, unsalted
  (`next_ticket(state, 0)`, `ticket_draw`, bit 1 when
  `number x d < n x TICKET_MODULUS`), in Port then merge-key order, sets the
  ray's `detector` to 2 on 1 and 1 on 0, and records a `detector_click` event
  (position, tick, Port, family, amount, bit 1) on 1 only. Until
  `detector-return-v1` (below) the ray continued unchanged on both outcomes.
- The runner records `detector_mark: "detector-mark-v1"` in `run.json`
  beside `sampling_profile` and `ray_state`.
- The ticket rule keeps its signature (`next_ticket(state, salt)`); the mark
  passes salt 0 and no other caller exists. `stamp_event` still stamps every
  created ray with Detector bit 0.
- `DetectorMark` is a registered formula-free state record of the Node
  contract audit (`diagnostics/node_contract.py`, `STATE_RECORDS`): a
  position and three bounded integers, no law and no reading of any ray.

A document without `detectors` has no marked Node, calls the ticket rule
nowhere and runs exactly as before.

## Detector return added on 2026-09-17 (`detector-return-v1`)

Issue #169, feature 3, the first half of migration step 4 of the
ray-event model under
[Highlights](HIGHLIGHTS.md) 3.19, 3.20 and 5.4: a draw of 0 at a marked Node
returns the arriving ray, the same wave ray reversed on its line, unchanged,
walking back the number of steps it has made since its event
(the return,
transport).

- `return_ray(ray, definition)` and `DETECTOR_RETURN` in
  `core/spatial_state.py`: heading index replaced by the negated heading's
  index, `outbound` 0, accumulators, wait and interaction delay reset,
  amount, phase, steps, event record and family unchanged.
- `SpatialNode.receive`: a ray whose draw is 0 is returned in its arrival
  interval, records a `detector_return` event (position, tick, Port, family,
  amount) and no click, and is left out of the per-Port delivered readings;
  a ray that arrives already returning is not drawn for and not counted in
  those readings either. The `detector_click` list is what it was.
- A returning ray enters no coupling: `_absorb` leaves it untouched and
  takes the coherence over the outbound rays, `apply_ray_interactions` gives
  it no participant view, and the value and flux samples couplings read are
  taken over the outbound rays (`SpatialNode.coupling_rays`).
- `forward_rays` keeps a returning ray with `steps` 0 resident, inert, with
  its phase unchanged; `advance_ray` still refuses it a Link. A resident
  returned ray waits for the inverse split (feature 4).
- `ray_momentum` reads a ray with `outbound` 0 as amount times its heading
  negated, its share on the event's heading, so a return leaves the momentum
  total unchanged and every audit exact (issue #169: the Detector takes no
  recoil).
- `SpatialEngine._escape` refuses a packet holding a returning ray with a
  validation error: its event Node is not in the world.
- The runner records `detector_return: "detector-return-v1"` in `run.json`
  beside `detector_mark`.

Pinned consequences in existing tests: the four rays of
`test_detector_mark.py` that draw 0 now return to their lamps and rest there,
and the returning ray of `test_ray_hidden_state.py` is kept resident at
`steps` 0 instead of failing the forwarding (expectations).
A document without `detectors` has no returning ray and runs byte for byte
as before.

## Inverse split added on 2026-09-17 (`inverse-split-v1`)

Issue #169, feature 4, the second half of migration step 4 of the
ray-event model under
[Highlights](HIGHLIGHTS.md) 3.20 and 5.4 and the model owner's decisions of
2026-09-17: a returned ray at its event Node performs the inverse split of
its own share by the world's `return_mode`
(the inverse split,
transport and bookkeeping).

- The initialization key `return_mode` (`siblings`, the default, `straight`
  or `annul`; any other value rejected), `InitialState.return_mode`,
  `SpatialLaw.return_mode`, `RETURN_MODES` and `INVERSE_SPLIT` in
  `core/spatial_state.py`.
- `transmit`, `split_ports`, `split_amounts`, `event_port` and
  `port_heading` in `core/spatial_state.py`: the transmission as new event
  rays with the returned ray's phase, advance and Detector bit, the mask of
  the lines transmitted to and the amount per line, remainder by Highlights
  3.17.
- `SpatialLaw._inverse_split` and `_refund` in `fields/spatial_plan.py`,
  after absorption and before forwarding: the returned share restored to
  the event's input (a record with a funded emission rule into the field)
  and the transmission funded from it in the same interval, both booked in
  `transfer_delta`; with no input, the momentum booked in the source ledger;
  `annul` into `SpatialPlan.annulled`.
- `SpatialPlan.inverse_splits` and `annulled`, `InverseSplit`, the
  `inverse_split` event (position, tick, family, mode, ports, amounts,
  amount, bit, restored, annulled) published before the cycle's
  `spatial_cycle`, `SpatialAccounting.record_annulled`,
  `SpatialEngine.annulled`, the `annulled` entry of the spatial accounting,
  `annulled_totals()` on the engine, and the local conservation audit
  reading the annulled content of a Node into its residual and reporting
  `annulled`.
- The runner's conservation line: initial + sources = current + dissipated
  + escaped + annulled at every completed tick
  (`accounting_balanced_at_every_completed_tick`), `annulled_totals`,
  `inverse_split: "inverse-split-v1"` and `return_mode` in `run.json`.

Pinned consequences in existing tests: the returned ray of
`test_detector_return.py` (a one-line event) is restored to its lamp and
emitted again by it, and the four returned rays of `test_detector_mark.py`
are restored to their lamps, which then hold their share with its recoil
undone, that test running three ticks
(expectations). A world without a mark
has no returned ray and runs byte for byte as before.
## Ray layers added on 2026-09-17 (`ray-layers-v1`)

Issue #169, feature 5, under [Highlights](HIGHLIGHTS.md) 5.1 and the
ray-event model: event spacetime
has layers, a layer is a set of families that couple, and a meeting exists
only inside a layer (layers).

- `ray_layers` (`core/spatial_state.py`) derives the layers from the catalog
  as the connected components of the ray fields over the participants of the
  declared `ray_interactions`; a ray field that no rule selects is its own
  layer. `SpatialLaw` derives them once when it is built (`layers`) and
  `apply_ray_interactions` (`fields/ray_interactions.py`) meets the resident
  rays of a Node layer by layer: each layer's rules fire over that layer's
  rays alone, in declared order, and a ray of a layer without a firing rule
  crosses unchanged. Rules of different layers fire independently in one
  interval.
- The 32-slot participant capacity of `validate_ray_participants` is now a
  bound per layer with a rule (the `ray_slots` of that layer's fields sum to
  at most 32) instead of over every selected field (retired with `ray_slots`
  on 2026-09-18, `lanes-v1`: the lanes bound the Node).
- The runner records `ray_layers: "ray-layers-v1"` and `ray_layer_families`
  (the derived layers as sorted lists of field names) in `run.json` beside
  `ray_state`.
- A world with a single layer runs byte-identically to before: the same
  owners, rules, charges and events. No initialization key changes; no
  draw, absorber, readout or Detector is touched.

## Test suite reduced on 2026-09-17: one test per rule

Decision of the model owner, 2026-09-17: the engine is generic, so the test
suite keeps one module per generic rule, each exercising that rule in isolation
on a minimal board, and one module per feature of the
ray-event model (issue #169); modules that pin the numbers
of an example world, combine several rules to reach a pinned number, duplicate a
kept rule under another world, or exist for a study, a gallery, a probe, a
comparison of worlds, rendering or playback were deleted, and so were the dated
research studies and every `examples/` directory that no kept test loads and
`tools/check.py` does not need. Before: 108 modules, 2,194 tests (2,191 passed,
3 visual-only skipped) in 622 seconds single-process on the recording host
(about 15 minutes in CI). After: 40 modules with `test_detector_mark.py` of
the merged PR #186, 1,009 tests, 35 seconds on the same host. The kept
modules and the rule each isolates are the
suite inventory.

Deleted test modules (69):

- world-specific probes and studies:
  `test_atomic_interactions.py`, `test_computational_response.py`,
  `test_coupled_excitations.py`, `test_de_broglie.py`,
  `test_directional_wave.py`, `test_euclidean_pace.py`,
  `test_family_conversion.py`, `test_generic_identity.py`,
  `test_gravity_probe.py`, `test_inverse_square_experiments.py`,
  `test_isotropy_probe.py`, `test_kerengonen_mirror.py`,
  `test_local_lorentz_field.py`, `test_lorentz_response_physics.py`,
  `test_matter_wave.py`, `test_maxwell_configuration.py`,
  `test_particle_gallery.py`, `test_particle_interactions.py`,
  `test_radiation_scattering.py`, `test_ray_heading_flux.py`,
  `test_redshift_sweep.py`, `test_reference_examples.py`,
  `test_small_space_experiments.py`;
- computational curvature and self-field scenarios:
  `test_arrival_port_blind.py`, `test_carried_allocation_phase.py`,
  `test_computation_field_delay.py`, `test_delay_direction.py`,
  `test_field_phase_first.py`, `test_least_delay_routing.py`,
  `test_node_work_emission.py`, `test_rotation_self_interaction.py`;
- catalog and profile data:
  `test_entity_catalog.py`, `test_entity_compiler.py`,
  `test_physical_entities.py`, `test_profile_validation.py`,
  `test_property_couplings.py`, `test_property_entity_profiles.py`,
  `test_reference_units.py`;
- duplicates of a kept rule:
  `test_active_node_contracts.py`, `test_active_ports.py`,
  `test_dissipative_initialization.py`, `test_emission_residuals.py`,
  `test_exchange_residuals.py`, `test_field_commit_guards.py`,
  `test_finite_spatial_engine.py`, `test_generic_vector_lab.py`,
  `test_interaction_spatial_integration.py`, `test_joint_node_reactions.py`,
  `test_joint_reaction_configuration.py`,
  `test_node_conservation_configuration.py`, `test_node_guard_boundaries.py`,
  `test_node_runtime.py`, `test_node_terminology.py`,
  `test_node_vector_examples.py`, `test_node_vector_integration.py`,
  `test_open_boundaries.py`, `test_parallel_node_execution.py`,
  `test_spatial_computation_delay.py`, `test_spatial_coupling_budget.py`,
  `test_spatial_engine.py`, `test_spatial_scheduling.py`,
  `test_spatial_seed_bounds.py`, `test_zero_carrier.py`;
- observer, playback, workspace and visualization:
  `test_local_observer.py`, `test_observer_playback.py`,
  `test_recorded_movie.py`, `test_workspace.py`,
  `test_workspace_integration.py`, `test_workspace_retention.py`.

The helper `tests/support/identity.py` went with `test_generic_identity.py`.
Deleted example directories (20), with their READMEs, configurations, scripts
and recorded results: `examples/charged-pair/`, `examples/collisions/`, `examples/computational-curvature/`, `examples/computational-response/`, `examples/de-broglie/`, `examples/euclidean-pace/`, `examples/family-conversion/`, `examples/gallery/`, `examples/gravity-probe/`, `examples/inverse-square/`, `examples/isotropy-probe/`, `examples/kerengonen-mirror/`, `examples/matter-wave/`, `examples/maxwell/`, `examples/observer/`, `examples/particle-interactions/`, `examples/radiation-scattering/`, `examples/relativity-probes/`, `examples/research/`, `examples/small-space/`.
The six research studies of 2026-09-16 under `examples/research/` (Bell and
postulate 22, already deleted with bucket B.5; anomalies; ray form; entity
audit; electron-photon scatter; ray gallery) are among them. Links to the
deleted paths in the documents became plain text with this date; the
hypotheses they informed stay stated in [HYPOTHESES.md](HYPOTHESES.md) and
their dated results in [VALIDATION.md](VALIDATION.md).

`tools/check.py` `RESOURCE_CONSUMERS` lost the rows of deleted examples and of
deleted consumers, except the rows that `tests/test_check_scope.py` (edited on
a running branch, left untouched) asserts: those rows still name
`test_ray_heading_flux.py`, `test_local_lorentz_field.py`,
`test_directional_wave.py`, `test_coupled_excitations.py`,
`test_property_entity_profiles.py`, `test_entity_catalog.py`,
`test_entity_compiler.py`, `test_physical_entities.py`,
`test_profile_validation.py`, `test_small_space_experiments.py`,
`test_reference_examples.py` and `test_generic_identity.py`, and the selector
still names `test_generic_vector_lab.py`, `test_workspace.py` and
`test_recorded_movie.py`; `main()` skips a selected test that does not exist.
The examples those rows name (`examples/directional-wave/`,
`examples/coupled-excitations/`, `examples/known-entities/`,
`examples/generic-ray-coupling/field-sampling.json` and the root example
inputs) stay for that reason and for the kept tests that load them (the rows
and `field-sampling.json` went with bucket B.6 later the same day, see
[records as owners deleted](#records-as-owners-deleted-on-2026-09-17)). The
modules of running feature branches (`test_energy_audit.py`,
`test_kerengonen.py`, `test_ray_integration_guards.py`,
`test_native_ray_coupling.py`, `test_ray_merge_contracts.py`,
`test_plan_reuse.py`, `test_ray_coupling_evidence.py`,
`test_detector_sampling_contract.py`, `test_check_scope.py`) were left as they
were; `test_ray_delay.py` and `test_local_focus.py` stay as their import
dependencies and as the output-clock and Local Focus modules. There is no
replacement: a rule that needs a new check gets one focused module.

## Experiments register added on 2026-09-17

By the model owner's decision of 2026-09-17, the research runs of the
ray-event model are listed in one register,
[docs/EXPERIMENTS.md](EXPERIMENTS.md): section A, the confrontations with
known measurements in which the model can be falsified (A1 to A13); section
B, the demonstrations the manuscript needs (B1 to B12); section C, the order
in which the features of issue #169 unlock them; section D, what the register
replaces. Every entry names the features it needs, its run design and its
pass or fail criterion before the run, and runs once at one runtime source
fingerprint under [Highlights](HIGHLIGHTS.md) 5.5; none is a test of the test
suite. The register replaces the historical example worlds and study
directories removed the same day; their dated results stay in the
[validation log](VALIDATION.md) with their original scope. The
[documentation index](README.md) routes to the register and the
[hypotheses page](HYPOTHESES.md) points to it. No initialization key, API or
runtime behavior changes.
## Meeting of rays with N-to-M outputs added on 2026-09-17 (`ray-meeting-conversion-v1`)

Issue #169, feature 6, under [Highlights](HIGHLIGHTS.md) 3.15, 3.17, 3.26
and 5.1 and step 6 of the
ray-event model: a rule of
`ray_interactions` with declared `outputs` replaces its participants by one
to six new event rays at the meeting Node
(meetings with outputs).

- `convert_values` (`fields/disturbances.py`) is the arithmetic of the record
  conversion's `_convert_group` factored into one pure function over bounded
  integers (guard, outputs from the frozen inputs, table splits, conserved
  sums, invariant sums, returning the outputs and the remainder), used
  unchanged by the record path and by the meeting of rays.
- `InteractionDefinition.outputs` names spatial fields for a ray rule and
  `InteractionDefinition.splits` holds its `TableSplit` entries
  (`core/disturbance_state.py`); `_ray_meeting` (`initialization.py`)
  compiles each output's `field`, `amount`, `heading`, `phase`, `delay` and
  `input` to assignments and splits; `apply_ray_interactions`
  (`fields/ray_interactions.py`) removes the participants, stamps the outputs
  as the events of the meeting (`steps 0`, the mask and shares of the
  outputs' Ports) and checks every family's stock; `ray_layers` puts a rule's
  output fields in its layer; `validate_ray_participants` admits outputs and
  still rejects `output_types` and `k`.
- The momentum a split by a table moves between two Ports is booked by the
  spatial law as an explicitly accounted source of the momentum field until
  the field ray of feature 7 owns it as recoil; `source_totals` shows it.
- With `wave-ray-family-v1` every output carries its field's `family` and
  `charge`, and a meeting's appended `charge` invariant is the per-ray readout
  `charge x amount` summed over its inputs and over its outputs.
- The runner records `ray_meeting: "ray-meeting-conversion-v1"` beside
  `ray_layers`.
- The ray path no longer needs `fields/record_operations.py` and
  `core/record_policy.py`: a meeting of rays converts without a resident
  record. Both stayed for the record path until step 6 of issue #164 (bucket
  B.6) deleted them the same day, see
  [records as owners deleted](#records-as-owners-deleted-on-2026-09-17).
- Existing worlds with single-output rules run byte-identically. The
  native-ray coupling tests that asserted `outputs` are rejected now assert
  that the carrier output form (`{"type": ...}`) and malformed meeting outputs
  are rejected.
## Wave-ray families added on 2026-09-17 (`wave-ray-family-v1`)

Issue #169, feature 9, the wave-ray part of
ray-event model migration step 6
under [Highlights](HIGHLIGHTS.md) 3.3 and 5.1: every ray is a wave ray, a
plain ray the special case with rest rate 0, light a family with rest rate 0
that carries its emitter's phase unchanged, and the phase the one value with
its own declared width
(wave-ray families).

- `spatial_fields[i]` (ray transport) admits `phase_bits` (the phase width;
  default 0, or log2 of `kerengonen.phase_steps`) and `charge` (per quantum,
  default 0). In the `kerengonen` object `phase_advance` (the rest rate) is
  required and `phase_steps` (the coherence table) optional; `phase_steps`
  must be a power of two (every existing world's is: 4, 8, 64), and
  `phase_advance` is bounded by the width, not by `MAX_VALUE`.
- `SpatialFieldDefinition` (`core/spatial_state.py`) gains `phase_bits`,
  `charge` and the properties `coherent`, `phase_modulus` and `phase_mask`;
  `kerengonen` now means a declared phase rule (a table or a nonzero rate);
  `advance_ray(ray, heading, phase_modulus, phase_advance)` takes the modulus,
  a power of two (a Kerengonen world's `phase_steps`), and masks; `phase_mask`,
  `ray_charge`, `charge_invariant`, `RAY_WRITABLE`, `RAY_VIEW_COMPONENTS`,
  `CHARGE_INVARIANT`, `WAVE_RAY_FAMILY`, `MAX_TABLE_BITS` and
  `MAX_STORED_PHASE_BITS` are added. Every `% phase_steps` in the engine became
  a mask.
- `RAY_PROPERTIES` gains read-only `family` and `charge`; a ray interaction's
  view reads nine components per participant (`read` cost 9 instead of 7), and
  the parser appends the `charge` invariant to every `ray_interactions` rule.
  `Simulation.charge_totals()` reads `charge x amount` per ray field.
- `kerengonen_phase` on an emission requires a ray field of sufficient width,
  not the `kerengonen` key (a plain field without a width admits phase 0
  only); a carried phase and `kerengonen_mirror` require the coherence table;
  `ray_phase_per_tick` and `hold_rays` follow the declared phase rule.
- Not admitted in this slice: `self_exclusion` or `ray_interactions` on a
  family wider than 30 bits, a coherence table wider than 12 bits
  (`phase_steps` above 4096), and a non-power-of-two `phase_steps` in a field
  definition (the table builders `phase_cosines` and `phase_sines` still take
  any count from 2 to 4096).
- The runner records `wave_ray: "wave-ray-family-v1"` beside `ray_state`.

Existing worlds run unchanged: a plain field has width 0 and rate 0, a
Kerengonen field the width of its `phase_steps`; the metered `read` cost of a
ray interaction is the one recorded difference. Tests adapted:
`test_kerengonen.py` (a nonzero phase before the plain-field rejection) and
`test_ray_integration_guards.py` (odd table sizes through the builders, 32
phase steps in the table-construction guard).

## Fixed body renamed external body on 2026-09-17

Fixed body renamed external body, 2026-09-17, same specification extended.
By the model owner's statement of that day, the declared element named
"fixed body" earlier the same day is the external body: a Node declared to
hold a family with an amount, if wanted a charge, and an initial momentum
(`initial_momentum`, in place of the declared trajectory of the first
statement: its motion is caused by fields only, model owner, 2026-09-17),
standing for a star, a neutron star, a fixed proton, a large charge or a
piece of apparatus; it radiates by the one field rule, does not spread and
is not pushed by matter. [Highlights](HIGHLIGHTS.md) 3.19 is the only authoritative
text; the [postulates](../POSTULATES.md) section 23, the
ray-event model section 1 and its
migration step 7b (`external-body-v1`, after feature 7), the
[experiments register](EXPERIMENTS.md) (A1, A2, A3, A6, A8, A12, A13 and
section C), the [terminology](TERMINOLOGY.md) (External body, Apparatus)
and section 14 of the [hypotheses page](HYPOTHESES.md) restate it. What the
extension adds: the amount is finite and of any width, since it enters no
sum; absorption into an explicitly accounted sink is the default coupling of
the body's family and the other couplings make the apparatus (a reversed
heading a mirror, a split by a declared table a beam splitter, a phase
offset a phase plate, a polarization read a polarizer once feature 11
exists; a wall, a screen and a beam stop the default); on the Node the body
is bounded metadata like the Detector mark, with one exact counter, the
sink totals per family; and where the back-reaction is wanted an ordinary
bound group with a large amount is declared instead. No initialization key,
API or runtime behavior changes; `external-body-v1` is not yet in the code.
## Ray viewer added on 2026-09-17 (`tools/ray_viewer/`)

The model owner's visualization requirement of 2026-09-17 (issue #169) is
implemented as a repository tool, ready before feature 7 lands: a Renderer
under [Highlights](HIGHLIGHTS.md) 3.29 and 3.30 that reads the runner's
record and never the engine (ray viewer).

- `tools/ray_viewer/extract.py` turns one or more records (`run.json`,
  `events.jsonl`, `initialization.json`, an optional `ray-recording.json`)
  into `runs.json` (`ray-viewer-runs-v1`): rays chained from the Link
  transits with their trails, every event as a marker with its Ports, and
  a caption per tick with the coupling, the invariants and the totals from
  the record; an event kind it does not know becomes a generic marker.
- `tools/ray_viewer/viewer.html` is the self-contained page (Three.js r128
  from cdnjs): dark, rays as segments with arrowheads and trails, hue by
  phase, field rays faint, markers that stay, Detector marks with their
  bits, lattice, axes and bounding box, a tick slider, play, a rotation
  toggle and a run selector.
- `tools/ray_viewer/render_gif.py` renders a GIF and a contact sheet with
  Playwright, headless Chromium and Pillow; `playwright` joins the `render`
  extra in `pyproject.toml`.
- `tests/test_ray_viewer.py` pins the extraction of a two-lamp, six-tick
  world (expectations);
  `tools/check.py` selects it for any change under `tools/ray_viewer/`.

No engine, schema or record change. The prototype under the session
scratchpad (`gif-electrons-3d`) is superseded by the tool.

## Binding and gravity by delay added on 2026-09-17 (`ray-binding-v1`)

Issue #169, feature 8 (binding;
Highlights 3.4 and 3.28). A `ray_interactions` rule without outputs whose
assignments set `delay` 1 binds its participants as a bound group: the rays
stay at the Node, the rule fires again every interval (the group's tick,
published as the `bound_tick` record), each phase advances once per interval
by its rest rate, and a held ray releases its field on all six headings. An
earlier declared outputs rule naming a bound participant and an arriving ray
unbinds the group. New keys: `ray_delay` on a binding rule, the Node's
output-clock delay while it holds the group (every arrival of matter waits
it, a field ray never, one Node-wide wait for the six per-face clocks), and
a meeting output's `delay`
as `{"of": i, "table": [six], "per": u}`, a delay per the Port input i came
through, carried as the ray's new `lag` field (three signed integers, part
of the merge key, reset by a return) and spent one Link toward the lagging
side per phase modulus: gravity as bending by delay. New registers:
`SpatialPlan.bound_delay`, `SpatialNodeState.bound_delay`; the snapshot lists
`bound_groups`; the runner records `ray_binding: "ray-binding-v1"`.
`test_ray_binding.py` pins the acceptance criterion G_eff x N^2 = 64 over
N = 2^8, 2^10, 2^12, 2^16. Worlds without a binding rule, a `ray_delay` or a
delay table run byte-identically.

## Field as the ray's information added on 2026-09-17 (`released-field-v1`)

Issue #169, feature 7, under [Highlights](HIGHLIGHTS.md) 3.5, 3.14, 3.15,
3.17 and 3.28 and step 7 of the
ray-event model: a ray field
declared with `field_of` and `release` is the field of that family, released
at every Node a ray of the family crosses
(released field).

- `SpatialFieldDefinition.field_of`, `release_numerator` and
  `release_denominator` (`core/spatial_state.py`) carry the declaration;
  `_spatial_fields` (`initialization.py`) parses `field_of` (a family name,
  resolved once every spatial field is parsed) and `release` (`[n, d]`,
  `1 <= n <= d`), declared together; `validate_released_fields` and
  `validate_released_field_admission` admit a world at `SpatialLaw` and
  `InitialState`.
- `release_field` and `release_stock` (`core/spatial_state.py`) are the pure
  release: one ray per Port heading except the source ray's own (all six for
  resident content), amount `floor(amount x n / d)` with the fraction not
  released, the source's phase, no event stamp. `SpatialLaw._release`
  (`fields/spatial_plan.py`) calls them after the interval's emissions, adds
  the rays to the departures and books their amount, and their momentum when
  a momentum field is bound, as an explicitly accounted source. A Node whose
  record holds stock of a source family runs its cycle every interval
  (`holds_source_stock`, `core/spatial_node.py`, `core/spatial_engine.py`).
- The recoil is the declared rule: a `ray_interactions` rule with outputs that
  returns the field ray with heading `"reversed"`. No engine mechanism was
  added for it.
- The runner records `released_field: "released-field-v1"` and
  `released_fields` beside `ray_meeting`.
- Existing worlds without `field_of` run byte-identically; their run record
  carries `released_fields: []`.

## External body added on 2026-09-17 (`external-body-v1`)

Issue #169, feature 7b, Highlights 3.19 (model owner, 2026-09-17; the
"fixed body" of earlier that day): the world key `external_bodies` declares
the second apparatus element beside the Detector mark, a Node holding a
family with an amount of any width, a charge, a phase, an initial momentum
(heading and pace), a coupling (`"sink"` or a declared ray interaction) and
a momentum table ([external
body](SPATIAL_FIELDS.md#the-external-body-external-body-v1)).

- `ExternalBody` in `core/spatial_state.py` (position, family, amount,
  charge, field, coupling, phase, signs, momentum, accumulators, sink), with
  `body_release`, `body_absorb`, `body_step`, `body_token`,
  `body_coupled_families`, `validate_external_bodies` and
  `external_body_names`; `InitialState.external_bodies`;
  `SpatialNodeState.body`, `SpatialPlan.body` and `body_port`,
  `SpatialPacket.body`; the record type registered in `STATE_RECORDS`.
- `core/spatial_node.py`: a body Node stays active; the body's cycle
  (`_body_cycle`) strips a coupled body's token, releases its field on six
  headings booked as a source and steps it by its accumulators; arrivals at
  a body are met by its coupling (`_body_meet`), the sink by default; the
  new records `external_body_absorbed` and `external_body_step`.
- The audit: `SpatialAccounting.record_absorbed`, the engine's
  `absorbed_by_bodies` line, `external_body_totals()`, `external_bodies()`
  and `external_body_momentum()` on the engine; the runner's conservation
  line gains `+ absorbed_by_bodies` and the run record `external_body`,
  `external_bodies` (with positions per tick), `external_body_totals` and
  `external_body_momentum`; a body cannot leave an open world.
- Worlds without `external_bodies` are byte-identical. New test module
  `tests/test_external_body.py` (sink, stars, uniform, mirror, rejected),
  pinned in TEST_EXPECTATIONS.md.

## Records as owners deleted on 2026-09-17

Issue #164 bucket B.6, the last deletion bucket, following
[HIGHLIGHTS.md](HIGHLIGHTS.md) sections 3.20 (all the information is on the
rays; the origin Node keeps nothing and there is no register) and 5.1 (no
occupied channel and no capacity rule) and row R1 and migration step 6 of
RAY_EVENT_MODEL.md: an interaction is a property of the
meeting of rays, and since `ray-meeting-conversion-v1` the N-to-M arithmetic
lives at the meeting (`convert_values`), not on a resident record.

- `fields/record_operations.py` (`RecordOperations`, 139 lines),
  `core/record_policy.py` (`RecordPolicy`, 25 lines) and
  `tests/test_record_operations.py` (19 tests, 177 lines) are gone.
  `DisturbanceEngine` no longer takes `record_policy=`; `NodeServices` carries
  `spatial_types` (the carrier types a spatial coupling or interaction selects)
  in its place, and `disturbance_api.Simulation` composes nothing for it.
- A delivered record takes the first spare slot outside the pending lock and
  nothing is folded into a resident: the merge of split arrivals of one type
  and channel by summing their values (records as owners) is deleted. The
  receiving-capacity failure is unchanged ("local receiving capacity
  exhausted; no disturbance was discarded"): a bounded-state error, not a rule
  that makes anything wait. The activity predicate and the cost reporter moved
  unchanged into `core/disturbance_node.py` as the pure functions
  `carrier_work` and `report_cost` over the immutable run definition, so a
  world in which no two arrivals of one type and channel reach one Node in one
  tick runs byte-identically.
- The N-to-M conversion of records is gone: `_convert_group` and the
  `outputs` branch of `DisturbanceLaw.__call__` (`fields/disturbances.py`),
  `_conversion_interaction` (`initialization.py`) and the one-role admission
  of `core/coupling_selectors.py` (a group has two to six roles). An
  `interactions` entry with `outputs` is rejected with a dated message;
  `outputs` in `ray_interactions` is unchanged and `convert_values` stays as
  the arithmetic of the meeting. The two-to-two `output_types` rule of
  local conversions is unchanged.
- The carrier commit's guard "outgoing links still occupied; no implicit
  packet queue is allowed" (`core/disturbance_node.py`) is gone, as the
  spatial pre-planning refusal went with bucket B.5.
- `tools/check.py` `RESOURCE_CONSUMERS` lost the rows of the consumers
  deleted with the test-suite reduction (`test_ray_heading_flux.py`,
  `test_property_entity_profiles.py`, `test_coupled_excitations.py`,
  `test_directional_wave.py`, `test_local_lorentz_field.py`,
  `test_entity_catalog.py`, `test_profile_validation.py`,
  `test_entity_compiler.py`, `test_physical_entities.py`,
  `test_small_space_experiments.py`, `test_reference_examples.py`,
  `test_generic_identity.py`) and the selector names
  `test_generic_vector_lab.py`, `test_workspace.py` and
  `test_recorded_movie.py`; every remaining row names a kept test, which
  `tests/test_check_scope.py` (27 tests, from 47) now asserts.
  `examples/generic-ray-coupling/field-sampling.json`, kept only for that
  table, is gone; `examples/directional-wave/`, `examples/coupled-excitations/`
  and `examples/known-entities/` stay because kept tests
  (`test_configuration_validation.py`, `test_local_conversions.py`) and
  documented tools load them.

There is no replacement API. Every deletion bucket of issue #164 is done.

## Catalog of nature added on 2026-09-17 (`catalog/nature.json`)

By the model owner's decision of 2026-09-17 under [Highlights](HIGHLIGHTS.md)
3.26 and 3.30, the families of nature and their couplings are data on the one
generic engine: `catalog/nature.json`, described in
the catalog of nature. The catalog is exactly two things, the
rays of nature with their couplings and the apparatus; the engine only reads
it, a world file selects rays from it and places apparatus, and nothing else
exists on the board.

- The file declares the rays (light, the electron and the positron with their
  fields, the muon, the neutrinos, up and down with colour, the gluon, the
  proton and the neutron as bound groups, the mass field), the couplings (the
  Born steering table, the electron's turn at its field, the recoil, the
  mass-field delay, the electron-proton and quark bindings, the gluon-gluon
  binding, the weak conversion, Pauli exclusion, the transmission meeting its
  held share, and the external-body couplings absorber, mirror, beam splitter,
  phase plate, slit and polarizer), the two apparatus kinds and, per register
  entry A1 to A14, the ids it uses, and the lag width of feature 8b as an
  open entry (Highlights 3.28: `phase_bits` is the family's resolution
  choice, the N of hypothesis 14 the lag modulus). Twenty-eight values are
  `"undecided"`, each with the experiment, hypothesis or feature that decides
  it.
- No engine code changed: no module, key or rule was added, and the parser
  accepts exactly what it did. A world file is still written by hand from the
  catalog; there is no loader.
- `tests/test_nature_catalog.py` is the gate: it parses the file, checks every
  record and reference, holds every undecided entry to the register and the
  hypotheses and to the table in `CATALOG.md`, builds a world from the file
  for every ray a world can select and every decided coupling the engine runs
  today and runs it for two ticks against pinned integers, an external body
  under each of its decided couplings among them. `tools/check.py` selects it
  when the catalog, its document, the register or the hypotheses change;
  `MANIFEST.in` ships the catalog with the tests.
- Written against features 7b (`external-body-v1`) and 8 (`ray-binding-v1`),
  which landed the same day: the absorber, the mirror and the phase plate are
  decided and run, the external body's record states the eight keys of its
  declaration, its coupling form and the apparatus family a coupled body
  needs, and the binding and gravity couplings name `ray-binding-v1` as their
  engine with their tables open.
- Documentation: the catalog of nature, a row in the
  [documentation index](README.md), a sentence in the
  [register](EXPERIMENTS.md), the expectations in
  test expectations.
## Ray viewer: releases, fields, style file and sidecar, 2026-09-17

The first render of a feature 7 run and the model owner's reading of the
page on a phone (2026-09-17) changed what the ray viewer
draws; the record is unchanged.

- `extract.py` resolves rays per family: a field family (`field_of`) passes
  Nodes in silence, leaves a Node with a departing matter ray as a `release`
  (its own event kind, flagged `field`, never a marker or a caption line, the
  source ray's trail unbroken), and makes a meeting only where it leaves a
  Node changed; escapes and field-only events carry a `field` flag; a body's
  `external_body_absorbed` ends the rays it took; the per-tick `in_world`
  figure now adds the sources recorded by `spatial_cycle` through the
  previous tick, which equals a recording's totals tick by tick (the earlier
  figure ignored sources and could fall below the amount on the Links);
  captions list only meetings, Detector events and inverse splits, at most
  three per tick, then the escapes once; `--sidecar` names a recording per
  record, and a recording whose fingerprints differ from the run's is refused;
  `external_bodies` are read from `run.json` with their `positions` per tick.
- `viewer.html` draws no text on the board except one `family amount` label
  per matter ray, placed only where it is at least 24 px from every other
  label and overlaps none; rays about 4 px wide with a 10 px arrowhead and a
  trail fading over six Links; event kinds by marker shape and colour with a
  legend under the canvas; matter escapes as a dot, field escapes as
  nothing; sources, Detector marks and external bodies as shapes without
  text, a body's picture chosen by family and moving with its recorded
  position; captions clamped to two lines at phone width.
- `style.json` (`ray-viewer-style-v1`) holds every colour, size, drawing,
  caption and motion rule, by the model owner's decision that a change of
  look is a file edit and a re-render; the page inlines or fetches it,
  `render_gif.py --style` inlines it and takes its defaults from it.
- `record_sidecar.py` writes `ray-recording.json` beside a record by
  replaying it on the run's own source tree, refusing any other.
- `tests/test_ray_viewer.py` pins the widened world (a released field, the
  body positions and the style file); the fixture no longer declares a
  `conservation` block, because the local audit failed on a field ray at a
  lamp Node (reported, not worked around), and its pins record that the
  engine released from two rays held by a coupling in the interval they were
  held, which the released-field text does not say (reported to feature 7).

## Ray viewer: clear matter lines, textless autoplay page, 2026-09-17

Model owner's feedback on the second render, applied as defaults of
`tools/ray_viewer/style.json` so that no change of look needs a code change
(ray viewer); the record is unchanged.

- `sizes.trail_links` 0 means the whole path since the ray's event; the
  default is 10 with `trail_fade` [1.0, 0.0]: the ray bright at its Link
  and a trail as wide (6 px) fading smoothly to nothing over ten Links, one
  opacity per Link, so the path reads without a hard cut; matter families
  have a fixed high-contrast colour (`colors.families.default`, `electron`
  as the example override) and `draw.hue_by_phase` (`arrowhead`, `ray` or
  `none`) says where the phase hue shows; field rays stay faint.
- `draw.page_text` holds one boolean per block of text around the board
  (`header`, `record`, `legend`, `captions`, `totals`, `tick_counter`,
  `controls`); by default only `header` (one line, the run's title from the
  record) and `tick_counter` are on, and the ray labels (`draw.labels.rays`)
  are off, so the published page shows the board with its title and tick
  and nothing else that reads as text; markers keep their shapes.
- `motion.autoplay` and `motion.loop`, both true by default: playback starts
  on load with the slow rotation and wraps at the end; the space key pauses
  and resumes, undocumented on the page.
- `render_gif.py` validates the new keys; the page's built-in default stays
  equal to the file, checked by `tests/test_ray_viewer.py`, which pins these
  defaults.

## Ray viewer: faint white wake and momentum arrow, 2026-09-17

Model owner's feedback on the fourth render, applied as defaults of
`tools/ray_viewer/style.json` (ray viewer);
the record is unchanged.

- `colors.trail` `#ffffff` (a family may override it with `trail` in its
  `colors.families` entry) and `trail_fade` [0.35, 0.0]: the path behind a
  ray is a faint white wake fading to nothing over `trail_links` Links, and
  the ray's head keeps its family colour.
- `draw.momentum_arrow` true, `sizes.momentum_arrow_px_per_quantum` 6,
  `sizes.momentum_arrow_width_px` 2 and `colors.momentum_arrow`: at the
  ray's head an arrow in its heading whose length is the ray's amount times
  the pixels per quantum (the momentum, amount x heading; 48 px for an
  electron of 8), carrying the arrowhead; with the flag off the small
  arrowhead of `arrowhead_px` returns. `viewer.html` gains that one drawing
  path; `render_gif.py` validates the keys; the test pins the defaults.

## Ray viewer: small head and small momentum arrow, 2026-09-17

Model owner's feedback on the fifth render, applied as defaults of
`tools/ray_viewer/style.json` (ray viewer);
the record is unchanged.

- `sizes.head_links` 0.5 (new key: the bright head is a short segment from
  the ray's Node along its heading, that fraction of a Link; 1 draws the
  whole Link) and `ray_width_px` 3: a small head in the family colour.
- `sizes.momentum_arrow_px_per_quantum` 1.75, `momentum_arrow_width_px` 1.5
  and `arrowhead_px` 5: a tiny arrow, 14 px for an electron of 8, that still
  reads as an arrow of the momentum; the faint white wake is unchanged.
- `viewer.html` draws the head over `head_links`; `render_gif.py` validates
  the key; the test pins the defaults.

## Ray viewer: spheres and a softer look, 2026-09-17

Model owner's feedback on the sixth render, applied as defaults of
`tools/ray_viewer/style.json` (ray viewer);
the record is unchanged.

- No cubes: `draw.marker_shape` `sphere` (with `cube` as an option and
  per-kind `shape_overrides` for `source`, `detector`, `body` and `head`)
  draws sources, Detector marks, external bodies and ray heads as smooth
  spheres with a soft specular (`sphere_roughness`, `sphere_metalness`), a
  little emissive light of their colour (`sphere_emissive`) and an additive
  glow behind them (`draw.glow`, `glow_scale`, `glow_alpha`); bodies differ
  by colour and size, not by polygon; a head is `head_radius_px` on screen;
  a Detector mark is a translucent sphere (`detector_alpha`).
- The picture: `draw.vignette` with `colors.scene` fading to `scene_edge`
  behind a transparent canvas; `lattice_alpha` 0.07, `node_dot_alpha` 0.22,
  `box_alpha` 0.35; field rays as faint cyan-white hairlines
  (`families.field` `#bfefff`, alpha 0.35, `field_width_px` 1) with additive
  blending (`draw.field_additive`); event markers as thin rings
  (`marker_ring_thickness` 0.06, `marker_alpha`) with a soft glow; escape
  dots small and dim (`escape_dot_radius` 0.09, `escape_alpha` 0.45);
  `elevation_deg` 30, `start_angle_deg` -40, `gif_degrees_per_frame` 4;
  `motion.gif_supersample` 2 renders a GIF at twice the size and scales it
  down for gentle anti-aliasing.
- `motion.camera_fit` `rays` (default; `board` as before) with
  `camera_fit_margin_links` 1: the camera, the lattice and the thin box fit
  the region around every matter ray path, source, Detector mark and body
  over the whole run, padded by the margin and clamped to the board, with the
  board's own edges drawn fainter around it, so a small action on a large
  board fills the frame; `colors.families` gains fixed colours for `light`,
  `proton` and `neutron` beside `electron`, so the families of a run are told
  apart by colour.
- `viewer.html` gains the sphere, glow, vignette, additive and camera-fit
  drawing paths; `render_gif.py` the supersampled capture and the keys; the
  test pins the defaults.

## Ray viewer: the eye view of clicks beside the board, 2026-09-17

By the model owner's decision on [Highlights](HIGHLIGHTS.md) 5.4
("everything begins and is realized at a marked Node"), the physical
picture is the list of PASS clicks and the board rendering is the record's
view (ray viewer); the record is unchanged.

- `extract.py` adds an `eye` block to every run: the marked Nodes, the
  list of PASS clicks (tick, Node, family, amount, bit, Port) and the hits
  per Node.
- `style.json` gains `draw.view` (`board`, the default, everything as
  before; `eye`, only the marked Nodes as dim spheres and each click as a
  flash of its family's colour at its Node, sized by amount, fading over
  `click_flash_ticks` and leaving a persistent dim dot, like a screen
  accumulating hits; no rays, fields or other markers; title, tick and the
  camera fit as before) with `click_flash_px_per_quantum`,
  `click_flash_min_px`, `click_dot_px`, `click_dot_alpha` and `mark_alpha`.
- `render_gif.py` gains `--view` (overrides the style) and
  `--side-by-side` (the board view and the eye view as two panels, left and
  right, in one GIF and one contact sheet); `viewer.html` gains the eye
  drawing path and a runtime `window.__setStyle` hook the renderer uses to
  switch views. The test pins the eye extraction and the defaults.
- In the eye view a mark is drawn without depth writing and without glow,
  the flash and the dot on top of it, so hits inside a mark's sphere show;
  the persistent dot's area grows with the hits at its Node (radius
  `click_dot_px` x the square root of the count), a spot on a screen.
- `examples/nature/screen.json` (Highlights 5.5, a demonstration made once,
  never a test; its section of the
  nature README
  holds the record's fingerprints and the render lines): an electron at
  rest, the bound group of two `electron` rays of 4, releasing `light` on
  its six axis lines, and a screen of seven Detector marks at distance 6
  along +X. Before feature 12 one mark clicks, the on-axis one, eighteen
  times; after it the whole screen. The test pins the world file's
  integers, not its run.

## Ray viewer: several runs on one page, the eye toggle, a tick cap, 2026-09-17

The model owner wants one HTML page with the nature runs, no GIF
(ray viewer); the record is unchanged.

- `style.json` gains `draw.page_text.runs` (the run buttons above the
  board when the document holds several runs; a button starts its run
  from tick 0 in the board view, playing when the style autoplays) and
  `draw.page_text.eye_toggle` (an `eye view` button for a run with marked
  Nodes, switching the page between the board and the eye view), both
  true by default; the run buttons no longer depend on `controls`.
- `extract.py --ticks N` caps a large record at N ticks: only the events
  through N are read, the run's `ticks` is N and
  `record.ticks_capped_from` keeps the recorded length. The test pins the
  cap and the flags.

## Ray viewer: phone GIF preset, 2026-09-17

The model owner's GIFs do not always open on the phone, and he wants GIFs
only (ray viewer); the record is
unchanged.

- `style.json` gains `motion.gif_preset` (`phone`, the default) and
  `motion.gif_presets`. `phone` renders 640 px wide (480 px per panel side
  by side), at most 20 frames spread evenly over the run (`tick_schedule`:
  the run still reaches its end, at most a quarter of the frames hold the
  last tick with the camera still, `gif_hold_still`, so the hold is stored
  once; the 24 frames the model owner allowed left the two-panel screen
  GIF at 1.05 MB, 20 bring every GIF under the target), 128 colours, no
  supersampling, a frame duration that makes
  the GIF read in about six seconds (`gif_seconds`), a target of under 1 MB
  (`gif_target_bytes`), no contact sheet and no stills. `full` holds the
  earlier numbers: every tick and twelve hold frames, supersampled, 120 ms
  a frame, a contact sheet of 16 stills.
- `render_gif.py --preset phone|full` chooses one; `--frames N` now spreads
  the run over N frames instead of cutting it. The summary records the byte
  size, the preset and the tick of every frame, and the renderer prints the
  size, with a note when it is above the target; it refuses nothing. The
  nature README's render lines are unchanged and make phone GIFs now.
- The test pins the presets and the schedule.

## Primary initialization-based API

`Simulation` now requires a validated `InitialState`; it no longer accepts an
implicit scalar Config or built-in particle semantics. Initialize the active
model with a strict JSON file:

```bash
python -m event_universe --init examples/basic.json --output artifacts/basic
```

Programmatic users import `Simulation` from `event_universe` and
`load_initial_state` from `event_universe.initialization`. Field/type names,
transport, updates, coupling and costs are data. Read
DISTURBANCES.md for the complete schema and limits.

Runs are headless. Visualization requires `--visualize`; standard tests do not
produce animation reports. `pytest --visualize-runs` explicitly enables them.
The active runner requires an empty output directory and preserves the original
initialization, events, final state and metadata.

## Version history

Use Git commits and tags for source versions. Each run records
a SHA-256 fingerprint of the active package files, so source identity survives
installation from a ZIP or wheel without a Git checkout.

## Explicit historical component names

The 2026-09-12 consistency cleanup made the active generic engine distinct from
historical particle models. These were source/import/command renames, not new
physical laws. The rows whose renamed target was deleted on 2026-09-17 (the
historical API, engine, model, scenario and test modules and the scalar-field
document) are omitted; the remaining rows still locate a current owner.

| Previous internal path or name | Canonical replacement |
| --- | --- |
| `examples/known-entities/run.py` | `examples/known-entities/run_reference_checks.py` |
| `examples/known-entities/run.ps1` | `examples/known-entities/run_reference_checks.ps1` |
| `examples/known-entities/collision.json` | `examples/04-unequal-mass-collision.json` |
| `examples/particle-contracts/build.py` | `examples/particle-contracts/build_reference_configurations.py` |
| `examples/maxwell/run.py` | `examples/maxwell/run_experiments.py` |
| `examples/small-space/run.py` | `examples/small-space/run_experiments.py` |

The removed collision file was byte-identical to the canonical workspace example.
The reference command resolves its logical `collision` experiment to that file;
other reference inputs retain their separate configuration and expectations.
Earlier validation records retain their original paths and hashes; use this
table to locate the current owner.

## Duration-only reference configuration

The reference three-mass case now reads `examples/three_mass_finite.json` and
passes `ticks=120` to the existing runner rather than keeping a second JSON
initialization. Replace the former `examples/known-entities/three-masses.json`
command with:

```sh
python -m event_universe --init examples/three_mass_finite.json --ticks 120 --output artifacts/three-masses
```

The original initialization retains its 100-tick default and is copied unchanged
into the output. Actual execution length is recorded separately. The reference
wrapper preserves its 120-tick numerical checks; physical coefficients, budgets
and laws are unchanged.

## The dated Highlights logs and the gate set, on 2026-09-20 (documentation and tools only)

The model owner's decision of 2026-09-20 ([Highlights 5.4, record 87](LOG_2026-09-20.md#87-decided-the-trimming-pull-request-after-amplitude-v1-lands)).
No law, no key, no integer, no run and no test expectation changes. This
entry is appended at the end of this file, apart from the newest-first order
above, so that the register split of the same decision lands beside it
without a merge. Moved, verbatim, one canonical copy each: the 153 records of
Highlights 5.4 (30 of 2026-09-17 and 2026-09-18, 29 of 2026-09-19, 94 of
2026-09-20) to `docs/LOG_2026-09-18.md`, `docs/LOG_2026-09-19.md` and
`docs/LOG_2026-09-20.md`, each under a numbered `###` heading (`NN. <the
record's title>`; a number is never reused or moved; a record is never
edited), 5.4 keeping its introduction, one line per decision with a link to
its record, and the sentence that stands where two records of a day
conflict. A reference to "Highlights 5.4" that names a record links to the
record's anchor in its log (`docs/LOG_<date>.md#NN-<title>`: the coverage
table's 5.4 cells, the documentation index, the Boss skill and the workflow);
a reference to the section as the law's home is unchanged, since the heading
`HIGHLIGHTS.md#54-the-detector` still exists. The four rows repeated in the
coverage table are removed, and its row on the detector as a set with one
record says `wave` is the default reading since 2026-09-20. Added:
`examples/events/gate_set.json`, the gate set of fifteen worlds chosen by
measured coverage (record 91 of the same log), replayed at every commit of an
integration through `tools/run_series.py --list examples/events/gate_set.json`
(`--fast` runs each world to the interval by which its coverage is complete;
`--compare SUMMARY.json` gives the verdict per world on the state, the ledger
and the events, whose digest the summary now carries as `events_sha256`); the
whole register replays only under `--full` or on demand. The contributor
rule: a record goes to the day's log, a decision to 5.4 as one line linked to
its record, nothing written twice (AGENTS.md, CONTRIBUTING.md item 8,
`skills/workflow.md`, the Boss skill). The register's split per series, item
(2) of the decision, and the references to 5.4 in the documents the
`amplitude-v1` landing edits are not in this change.
