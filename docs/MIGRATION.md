# API and repository migration

Install from the extracted project first:

```bash
python -m pip install -e '.[render,dev]'
```

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
approve 1 and 3"; [RAY_LAW section 10](RAY_LAW.md#10-implementation-notes-2026-09-19-the-implementation),
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
of the ray"; the design [the law of the ray](RAY_LAW.md), published before
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
  entry. The package is `event_universe` 0.3.0.
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
- **Documents.** ENGINE.md is the bookkeeping around RAY_LAW.md;
  DETECTOR_REQUIREMENTS drops its implementation contract; the registered
  readings of `events-v1` (series C, Bell A2) keep their scope in
  EXPERIMENTS.md and VALIDATION.md and are re-registered under `rays-v1`
  there.

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
