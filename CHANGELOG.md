# Changelog

All notable changes to Universe24, the reference implementation of Reality
Theory (Universe24). Versions are tags on `main`; each is archived on Zenodo.

## Unreleased

### The label along the unit vector of the direction (2026-09-19)

- The momentum label of a ray is along the unit vector u_d of its
  direction at the flight table's scale Q = 64, the integer vector
  nearest Q D / |D| computed once in the world's direction table by the
  physics-rule reviewer's exact integer rule (`nature_beam.unit_label`,
  the flight table's `labels`), in place of the integer direction D whose
  length grew with the declaration ([RAY_LAW section 2](docs/RAY_LAW.md#2-the-record-of-a-ray-and-the-world-file)
  and [note 23](docs/RAY_LAW.md#10-implementation-notes-2026-09-19-the-implementation);
  the model owner, "go for it", on the reviewer's verdict: the D-label was
  the right direction and the wrong magnitude). Every unit carries one
  length of momentum, Q per unit of weight, for every direction within
  1.35 %, exactly Q e_d on a heading; every conservation stays exact.
  The four corrections of the verdict are implemented: the rounding rule
  in integers only; the step rule `by_clock(age, |p|, Q x S x M + |p|)`
  (`_move`, every registered step bit-identical); the parser's and
  `label_weights`' bound at Q x content x amount <= 2^62 - 1, refused
  loudly with the number; the reading's vector and tensor moments on u_d
  (a fan's flow reads Q x q direction-blind). Every momentum of a world
  file and of the record is now in label units, x 64 for a heading
  ([migration](docs/MIGRATION.md#the-label-along-the-unit-vector-of-the-direction-on-2026-09-19-the-momentum-units-change-by-q--64)).
  Re-registered: series C (every push and momentum x 64 exactly, the
  tool dividing by Q where it compares with q; 392 criteria, 0 failed,
  19 readings inside and 9 outside as before), Bell (unchanged, S = 2,
  326 criteria) and series D re-derived with L = 1 in label units under
  the Q S M rule and re-run (p = 3, 5, 9 units of the probe's content,
  192, 320, 576 in label units; no orbit closes by the criterion, the
  S = 32 probes now bound for many turns; [EXPERIMENTS](docs/EXPERIMENTS.md#d-the-orbit-under-the-law-of-the-ray-on-the-plane-2026-09-19),
  [validation](docs/VALIDATION.md)). Tests: `test_ray_label` (new),
  `test_ray_readings` (f), every momentum pin x 64 (the fan fixtures on
  u_d), the bound-edge worlds at 1/64 of their amounts, the detector's
  beyond-register row 2^52 -> 2^49 ([expectations](docs/TEST_EXPECTATIONS.md)).

### The detector's record exact, never refused (2026-09-19, after the batching)

- The night's affordable amount (`RECORD_AMOUNT_BOUND` = 261123, the
  amount a detector Node or a face could click of one family in one
  interval) refused a lawful world: `examples/events/two_contents.json`,
  which had run 200 intervals before the bound, was refused at its 20th
  interval when its two +y beams of 2^17 left through `face:+y` together
  (262144). The record is a host reading, not the law's local work, so it
  is now exact and never refused ([RAY_LAW section 5](docs/RAY_LAW.md#5-the-detectors-record-the-re-emission-the-face-detectors)
  and [note 19](docs/RAY_LAW.md#10-implementation-notes-2026-09-19-the-implementation)):
  the coherent pointer (X, Y) is summed in the int64 register while the
  clicked amount is within `POINTER_AMOUNT_BOUND` = (2^62 - 1) // (32 x
  257) = 560759486676481 and in Python integers beyond it
  (`nature_beam.coherent_pointer`); the square and the cumulative record
  are Python integers always (`Measured.record`, `Ledger.face_record`).
  `RECORD_AMOUNT_BOUND`, `check_record_amount`, `record_amount` and the
  refusal are deleted. The `record` of `events.jsonl`, `run.json` and
  `state.json` can exceed 2^63 and is parsed as an arbitrary-precision
  integer. Bit-exact on every world that ran: 44 of the 45 example worlds
  byte-identical before and after, `two_contents` completing its 200
  intervals with the books closed, its first 19 intervals' `events.jsonl`
  the byte prefix of the new one ([validation](docs/VALIDATION.md)).
  Tests: `test_ray_detector` (e) rewritten, `test_ray_worlds` (e) new
  ([expectations](docs/TEST_EXPECTATIONS.md),
  [migration](docs/MIGRATION.md#the-detectors-record-exact-never-refused-on-2026-09-19-after-the-batching)).

### The host's batching of the law of the ray (2026-09-19)

- Five optimizations of how the host runs the law, none of the law
  ([RAY_LAW section 10](docs/RAY_LAW.md#10-implementation-notes-2026-09-19-the-implementation),
  note 22): step 4 taken in bulk across the measured events
  (`FamilyPlan`); the dense readings of the board decomposed on request
  for the active Nodes (`Readings`, `ArrivalRows`); the merge by one
  packed key with the lexsort as the fallback (`RayStore.merge_key`); the
  books as running ledger lines (`Ledger.transit_momentum`,
  `RaySimulation.recount`, `books(recount=True)`) and the collision table
  cached per process; the clocks' frame in bulk (`_frame_all`), the
  self-creations visiting only the emitters, `events.jsonl` buffered.
  Bit-exact: the 45 example worlds' `events.jsonl` and `state.json`
  byte-identical to the base and the tools' outputs the same
  ([validation](docs/VALIDATION.md)); the plane source of series C 2.97 ->
  1.61 ms per interval, two slits 12.4 -> 3.5 ms, the suite 16.8 -> 5.5 s.
  Tests: `test_ray_books` (new), `test_ray_bijection` (the merge),
  `test_ray_readings` (e), `test_ray_push` (i)
  ([expectations](docs/TEST_EXPECTATIONS.md)).

### The push as one form, the one label and the affordable amount (2026-09-19, the night)

- The physics-rule review of the law of the ray and the model owner's
  proposal 2 ([RAY_LAW section 10](docs/RAY_LAW.md#10-implementation-notes-2026-09-19-the-implementation),
  notes 18 to 21). Every momentum the law reads or moves is the one label
  of the rows (`nature_beam.momentum_labels`): the push's moment, the
  click's momentum, the face click's, the recoil, what comes home and the
  transit line; no collision at a Node that holds a measured event (rays
  meet the table, not each other); the push is one bilinear form
  `push_A = sum kappa(A, B) . V_B` (`push_form`) with the emitter's factor
  (q_B, M_B) carried on a free family's record as two integer columns
  `charge` and `mass`, the lookup by number and the lcm deleted; the
  amount a detector Node or a face clicks in one interval bounded by the
  affordable amount 261123 before the record's products are formed
  (`RECORD_AMOUNT_BOUND`), every reduction exact. The series C, series 7
  and Bell runs are unchanged record by record; series D is re-registered
  with the momenta re-derived for the label's magnitude (no orbit closes;
  the open question of the label's magnitude for the owner,
  [PROJECT_STATUS](docs/PROJECT_STATUS.md)). Tests: `test_ray_push` (new),
  `test_ray_collision` (d), `test_ray_detector` (e)
  ([migration](docs/MIGRATION.md#the-push-as-one-form-the-one-label-and-the-affordable-amount-on-2026-09-19-the-night),
  [expectations](docs/TEST_EXPECTATIONS.md), [validation](docs/VALIDATION.md)).

### Cleanup after the law of the ray (2026-09-19)

- The contributor instructions and the definitions that still sent a reader
  to the deleted generic disturbance contract (docs/DISTURBANCES.md, deleted
  on 2026-09-19) carry the history marker with the date and the pointer to
  [the law of the ray](docs/RAY_LAW.md) and [the engine](docs/ENGINE.md):
  the four skills and the shared workflow that named DISTURBANCES.md as the
  active contract; SIMULATOR_DEFINITIONS "Active generic disturbance model"
  (now "Historical ... (deleted on 2026-09-19)") and its display section's
  pointer; POSTULATES "Active initialization-defined model" and its "Active
  contract: disturbance transfers ..." line; TERMINOLOGY "Ray-event terms";
  DETECTOR_REQUIREMENTS' status line; PHYSICAL_FEATURES' schema pointer.
  No physics text was rewritten; the sections are marked, not deleted.
- `core/integer.py` loses the component arithmetic of the deleted engines
  (`signed_divrem`, `ceil_div`, `checked_sum`, `add_components`,
  `subtract_components`, `dot_product`, `cross_product`, `reduced_ratio`:
  no caller left) and `core/lattice.py` loses `MIXING_OPPOSITE` (no caller);
  their 13 tests go with them, and `test_integer_arithmetic.py` pins the
  primitives the ray law uses (`checked_work`, `integer_root`, `bounded_gcd`)
  ([migration](docs/MIGRATION.md#cleanup-after-the-law-of-the-ray-on-2026-09-19)).
- `pyproject.toml` declares numpy (`numpy>=2.5.3,<3`, the version of the
  validated environment as the floor) as a dependency of the package: the
  engine imports it at module level, and `pip install -e .` installed
  nothing before; the render extra keeps matplotlib, Pillow and playwright.
- `event_universe.__version__` is 0.3.1, the version of `pyproject.toml`,
  `CITATION.cff` and the 0.3.1 release of 2026-09-15 (the string read 0.3.0
  since then); `run.json` records `package_version` 0.3.1 from now on.
- `import event_universe` loads the engine (numpy) on the first read of
  `RaySimulation`, as the `events` package promised: the package, the world
  parser and the preflight import only the generic physics.
### The table from the keys and the moments (2026-09-19, the night)

- Two decisions of the model owner on the mathematician's review of the
  table of the physical entities (Highlights 5.4, "I approve 1 and 3";
  [RAY_LAW section 10](docs/RAY_LAW.md#10-implementation-notes-2026-09-19-the-implementation),
  notes 15 and 16), generic replacing generic. The table of a measured
  event is generated from the families' keys (`world.default_table`: a
  free family read, a paid one measured, no window) and a world declares
  only what differs (a window, a rule off the default, a `reads`
  component; `rule` optional in the object form; an entry equal to the
  default accepted and changing nothing); the kind of a family is derived
  from its `quantum` (0 free, 1 or more paid; `quantum` required) and the
  key `kind` is refused naming MIGRATION. The one reading `read_arrivals`
  is the amount-weighted moments of order 0, 1 and 2 of the arrivals'
  direction vectors (the count split outside / here, the flow, the
  traceless tensor `3 x sum amount x D (x) D - tr I`, exact integers,
  bounded), valid for a fan as for the six headings, in place of the
  seven-slot decomposition; on the six headings it reads exactly as
  before, on a fan a ray enters with its own vector. The example worlds
  are rewritten by `tools/migrate_ray_worlds.py` (new) to declare only
  what differs; every example world parses as before and the Bell and
  coupling runs are unchanged record by record
  ([validation](docs/VALIDATION.md)). Tests: `test_default_table` (new),
  `test_ray_readings` (a) re-pinned
  ([migration](docs/MIGRATION.md#the-table-from-the-keys-and-the-moments-on-2026-09-19-the-night),
  [expectations](docs/TEST_EXPECTATIONS.md)).
### The width of the push (2026-09-19)

- The world key `width` (S, an integer from 1; the model owner's D1,
  2026-09-19, Highlights 5.4, "try D1"): a free measured event of content M
  with the momentum component p on an axis steps one Link per
  (S x M + p) / p self-creations on that axis, `by_clock(age, |p|, S x M +
  |p|)` in `RaySimulation._move` in place of `M + |p|`, no remainder kept.
  S = 1 is the default and the rule as it was (one Link per (M + p) / p),
  so every existing world file reads the same and no migration note is
  needed; the parser refuses 0, a negative width, a string and a fraction
  naming the key; `run.json` records `width`. One unit of net flow gives
  any body p = M, so the speed it gives is 1 / (S + 1) for every content:
  the equivalence principle is kept and a world can declare slow motion
  ([RAY_LAW section 3](docs/RAY_LAW.md#3-the-nodes-interval-nature_beam)
  step 5 and note 15, [the engine](docs/ENGINE.md),
  [terminology](docs/TERMINOLOGY.md)). Test: `tests/test_push_width.py`
  ([expectations](docs/TEST_EXPECTATIONS.md#the-width-of-the-push)).
- The orbit series D on the plane (`examples/events/orbit/`, six worlds by
  `make_worlds.py`, `tools/orbit_readings.py`): a fixed source releasing
  one shell every 10 intervals on a fan of 120 primitive in-plane
  directions and a free probe of content 1 at r = 12 or 24 with the
  tangential momentum derived for a circular orbit under the measured push
  law, at `width` 1, 8 and 32. Registered in
  [D, the orbit under the law of the ray, on the plane](docs/EXPERIMENTS.md#d-the-orbit-under-the-law-of-the-ray-on-the-plane-2026-09-19):
  one orbit closes by the criterion (S = 32, r = 12: 346 intervals against
  343 derived, an eccentric loop), no other closing, the mean push as
  derived (C 1.1), the grain of the push the reason. No test pins the
  registered run (the owner's rule of 2026-09-17).

### The law of the ray (2026-09-19)

- The engine of the law of the ray, `rays-v1` (the model owner, 2026-09-19,
  Highlights 5.4, "DECIDED: the law of the ray"; the design
  [docs/RAY_LAW.md](docs/RAY_LAW.md)): the record `NatureBeam` and the one
  function `nature_beam` (`src/event_universe/events/nature_beam.py`), a
  Node's whole interval for the rays present; the flight table at
  1 / sqrt 3 on the digital line of every direction (at most one Link per
  interval, the age modulo the period); the eight-slot collision table
  generated from its rule and checked at load (a bijection inside invariant
  classes); the one reading `read_arrivals` (two scalars, the flow, the
  tensor; every coupling selects its component by `reads`); the detector's
  squared coherent record per interval (`record`); the re-emission on
  declared directions; the inverse interval (`inverse_step`) on a board
  without a measured event; the store of records per family. The world
  selects it with `"law": "rays"` and gains `directions`,
  `direction_bound`, `phase_per_link`, a measured event's `directions`, a
  table entry's `reads`, a ray's `direction` and `age`. `events-v1` is
  deleted with `mixing.py`, `transit.py`, `reversible.py`, the
  `reversible-detector-v1` candidate and fourteen test modules; every rule
  the ray law keeps is re-pinned in the ten `test_ray_*` modules
  ([migration](docs/MIGRATION.md#the-law-of-the-ray-on-2026-09-19-rays-v1),
  [expectations](docs/TEST_EXPECTATIONS.md)). The example worlds, the Bell
  and coupling generators and the detector definitions are ray worlds; the
  Bell run A2 and the coupling series C are re-registered under `rays-v1`
  ([experiments](docs/EXPERIMENTS.md)). Package version 0.3.1 (the
  `__version__` string read 0.3.0 until the cleanup above).

### The engine of the law of events (2026-09-19)

- The ray is `NatureBeam` and its one function `nature_beam` (module
  `events/nature_beam.py`), the model owner's name of 2026-09-19 replacing
  GonenBeam given earlier the same day; a mechanical rename, nothing else
  changed ([migration](docs/MIGRATION.md#the-ray-is-naturebeam-on-2026-09-19-the-night)).
- The three reversible corrections that every path shares (the model
  owner, 2026-09-19, Highlights 5.4; the architect's D2 and D3). No merge:
  a measured event's step onto a Node that holds a measured event is
  refused, the stepping event staying where it is with its momentum, the
  resident untouched and the step counted (the `merged` record and the
  merge branch of `_move` deleted; a world where two bodies met and merged
  now keeps both). An open face is a detector: every escape through an open
  face, in transit or a measured event's step, is a `click` on the face
  detector named by the face (`face:+x` ... `face:-z`), recorded with the
  tick, the Node, the number, the amount, the phase, the momentum and the
  content, the face detectors listed in the run's `detectors` after the
  declared ones, and the books' escaped lines their sums; nothing physical
  changes at the face (the `escaped` record of a measured event becomes
  that click). The clock's count read off the clock: the count a measured
  event owes after its self-creation is `by_clock(age, k x n, d)` from the
  presence k, like every other rate, no remainder kept, so the mean slowing
  is k n / d (a presence of 1 at [1, 4] slows the clock by 1 / 4 where
  `k x n // d` gave none; exact multiples unchanged)
  ([the engine](docs/ENGINE.md),
  [migration](docs/MIGRATION.md#no-merge-a-step-onto-a-measured-event-is-refused-on-2026-09-19)).
  Tests: `test_border_and_clock_corrections` (new); `test_event_boundaries`
  (the wrapped target held: the refusal), `test_phase_window` (a) (two face
  clicks among its records) re-pinned; `test_event_suspension` unchanged;
  the Bell worlds unchanged
  ([expectations](docs/TEST_EXPECTATIONS.md#the-border-and-the-clocks-count)).
- One reading set for every coupling (the model owner, 2026-09-19, on the
  mathematician's list: "everything present at the Node but the reader's
  own number, including here"). The presence at a Node counts, beside the
  arrivals and the units waiting there as arrivals, the content of the
  measured event at the Node under its number (`EventSimulation.step`), so
  a transit bundle of another number reads it (a unit of light passing a
  content of 2^10 at `suspension` [1, 4] now carries 256 where it read 0)
  and the measured event, reading every number but its own, does not; a
  detector's threshold is met by the family's amount summed over every
  number but the Node's own, and a phase window reads the phase of their
  coherent sum (`Transit.phase_at(position, ranks)` over a sequence of
  ranks), one verdict for the set, the record per number with the set's
  phase (`_meet`, split into `_home` and `_respond`); the push was already
  the sum over the numbers of each number's flow (the emitter's electric
  factor its own) with the own number home, and now follows the set's gate.
  What came home is not content and not presence ([the engine](docs/ENGINE.md),
  [terminology](docs/TERMINOLOGY.md),
  [migration](docs/MIGRATION.md#one-reading-set-for-every-coupling-on-2026-09-19)).
  Test: `test_one_reading_set` (new;
  [expectations](docs/TEST_EXPECTATIONS.md#one-reading-set));
  `test_event_suspension` (e) reads 17 where it read 16, its counts
  unchanged; no other pin moves. The Bell worlds run unchanged (326
  criteria of `tools/bell_chsh.py`, S = 2).
- The integer bounds of the measured line and of the emission (the
  architect's review of 2026-09-19, findings F2, F4 and F9). `engine.bounded`
  checks a measured event's momentum after a push, a recoil or a merge, the
  push taken and its terms, its content after a click or a merge, and what
  waits to be created again with its content against 2^62 - 1
  (`transit.MOMENTUM_BOUND`, the bound of a declared and of a carried
  momentum) before they are assigned; beyond it the run is refused with
  `OverflowError` naming the measured event, its Node and the quantity
  (until now `Measured.momentum` and `pushed` were unbounded Python
  integers). The parser refuses a measured event of a free family whose
  release per Port per self-creation, amount x n // d at the world's
  `release`, times 3 exceeds the mixing's cell bound 2^30 - 1
  (`world.EMISSION_CELL_BOUND`, `EMISSION_MARGIN`: a neighbour's slot holds
  up to about 2.3 x the release per Port), naming the Node, the amount, the
  release and the bound, where until now the preflight certified a content
  of 2^36 at [1, 128] and the first crowded mixing refused the run at
  interval 4 to 14; every shipped example passes (the largest free emission,
  2^24 at [1, 128], is 3 x 131072 = 393216). The four refusals of
  `mixing.py` that said "value exceeds the disturbance integer bound" (the
  retired engine's word) now name the quantity: the amount in a cell, the
  momentum carried by a departure, the amount placed on a departure, and the
  coherent sum's component ([the engine](docs/ENGINE.md),
  [migration](docs/MIGRATION.md#the-emission-bound-at-parsing-and-the-bounded-measured-line-on-2026-09-19)).
  Test: `test_integer_bounds_of_measured_and_emission` (new;
  [expectations](docs/TEST_EXPECTATIONS.md#the-integer-bounds-of-the-measured-line-and-of-the-emission)).
- A release costs the emitter by its phase rate (the model owner,
  2026-09-19, "I approve the proposal"): at a self-creation whose turn is
  s = `by_clock(age, content, K)` phase steps, each unit a lamp releases
  costs it `quantum` x s content, carries that content and the momentum
  `quantum` x s along its heading, and gives it to the measured event that
  measures it, so the content of a click is proportional to the emitter's
  frequency, E = h f with h the declared `quantum` (the content of one unit
  per phase step). A turn of 0 releases nothing (no quanta of zero content).
  The content is carried per slot in transit (`Transit.arr_con`, `fly_con`)
  and goes with the units at every Node exactly as the momentum does; the
  books carry a content line balanced at every interval; measurement
  records and `state.json` carry the content. A free family's release costs
  nothing and its units carry no content, so `measure` on a free family adds
  nothing ([the engine](docs/ENGINE.md#a-release-costs-the-emitter-by-its-phase-rate),
  [migration](docs/MIGRATION.md#a-release-costs-the-emitter-by-its-phase-rate-on-2026-09-19-e--h-f)).
  Tests: `test_release_costs_by_phase_rate` (new); `test_event_clock` (c)
  at K 82, `test_detector_sensitivity` (c) at K 24, `test_phase_window` (a)
  records with `content`, `test_event_suspension` (c) re-pinned,
  `test_event_worlds` (d) the screen's content
  ([expectations](docs/TEST_EXPECTATIONS.md#a-release-costs-the-emitter-by-its-phase-rate)).
  The Bell worlds run unchanged (326 criteria of `tools/bell_chsh.py`).
- One rule of the Node: the phase-less scatter is the diagonal of the
  coherent sum inside `mix_arrivals` (the model owner, 2026-09-19:
  "everything generic must be replaced by generic"; the physics-rule
  reviewer's identity: with c_h = S - 3 a_opp(h), dropping every cross term
  of |c_h|^2 between mutually incoherent arrivals leaves
  weight_h = 32^2 x (the number's amount over the six Ports + 3 x its
  amount through the side's own Port), 4 : 1 : 1 : 1 : 1 : 1 for a lone
  arrival, exact integers, no root). `mixing.scatter_arrivals` and
  `SCATTER_BACK`, `SCATTER_TOTAL` are removed; `mix_arrivals` reads the
  family's `phased` and takes its weights from `coherent_weights` or
  `diagonal_weights`, the placement, the group with no whole by its
  momentum, `apportion_carried` and the leaving phase (0 without a phase
  circle) the same code for every family; `Transit.cycle` calls it for
  every family. The shares agree with the scatter in the mean exactly; the
  rounding and the momentum labels fall once per group where they fell once
  per Port, and a number's weights are its own (no cross term between
  numbers: another number's field does not steer its labels). About four
  times faster than the scatter on 29^3 ([the engine](docs/ENGINE.md),
  [migration](docs/MIGRATION.md#one-rule-of-the-node-the-phase-less-scatter-folded-into-mix_arrivals-on-2026-09-19)).
  Tests: `test_phaseless_family` (b) re-pinned (the labels of two opposite
  9s 0 each, old -3 and 3; the edge [4, 2, 2, 1, 1, 1], old
  [6, 1, 1, 1, 1, 1]), (d) the identity of the weights added;
  `test_event_worlds` (a) to (c) unchanged within their bands
  ([expectations](docs/TEST_EXPECTATIONS.md#a-family-without-a-phase-circle)).
- The coherent sum at a Node runs over all the arrivals present, whatever
  their number (node-mixing-v3, the model owner's decision of 2026-09-19:
  "the Node reads what is present"; the number is a label for the detector,
  not a kind). `mixing.mix_arrivals` sums the amplitude vectors over the
  number axis per Port before the coherent sum; the leaving amplitude of
  each side is the common sum less three times what came in through its
  Port over all numbers; the weights per side are common to every number at
  the Node and each number places its own units by them (the largest
  remainder with the tick's ties, per number; a number with no whole by its
  own momentum); the leaving phase of a side is the common one; every unit
  keeps its number and the momenta are apportioned per number as before.
  Two numbers' crowds at one Node now interfere (in antiphase nothing leaves
  sideways) where before they passed through each other; a family with one
  number at every Node, every example world, runs as before, and
  `Transit.sizes` and `phase_at` stay per number ([the engine](docs/ENGINE.md),
  [migration](docs/MIGRATION.md#the-coherent-sum-at-a-node-over-all-numbers-present-on-2026-09-19-node-mixing-v3)).
  Test: `test_node_mixing_numbers` (new; `test_node_mixing` is the control
  of one number, unchanged; [expectations](docs/TEST_EXPECTATIONS.md#the-coherent-sum-over-the-numbers)).
  With the field of matter phase-less (the next entry) the pair world of
  `test_event_worlds` (c) reads as that entry's pins say: its `m` never
  enters `mix_arrivals`, so v3 does not act on it.
- The field of matter without phase, the suspension as presence with a
  fractional width, and the push as the net flow (the model owner,
  2026-09-19, three decisions implemented together, to be reverted if the
  physics-rule reviewer's numbers say otherwise): a family may declare
  `"phase": false` (its events carry phase 0 and never turn, its measured
  events never turn, and at a Node each Port's arrival scatters on its own,
  four ninths back and one ninth each other way, `mixing.scatter_arrivals`,
  its momentum apportioned per Port); `suspension` is `[n, d]` and a reader
  owes `presence x n // d` intervals, the presence being the amount that
  arrived at its Node this interval over every family and every number but
  its own (an integer w reads as `[w, 1]`; the sizes no longer feed it); a
  free family's push is the content times the net flow of the bundle
  (amount times travel heading over the six Ports), the electric part
  likewise, a paid family's push its carried momentum as before. The example
  worlds `one_content` and `two_contents` declare `"phase": false` for `m`;
  `run.json` records `suspension` as a list and `phase` per family
  ([the engine](docs/ENGINE.md),
  [migration](docs/MIGRATION.md#the-field-of-matter-without-phase-the-suspension-as-presence-with-a-fractional-width-and-the-push-as-the-net-flow-on-2026-09-19)).
  Tests: `test_phaseless_family` new; `test_event_suspension` (a) to (c)
  re-pinned at `[1, 4]`, (d) and (e) added; `test_event_worlds` re-pinned
  ([expectations](docs/TEST_EXPECTATIONS.md)).
- A periodic axis as a declared run parameter of the world, the model
  owner's approved exception to the open board (2026-09-19): `boundary`
  accepts, beside `"open"`, an object with any of `x`, `y`, `z` set to
  `"open"` or `"periodic"`, the missing axes open. On a periodic axis the
  departures that would leave through one face are created at the first Node
  of the opposite face (`Transit.walk`), nothing escapes on that axis and the
  momentum they carry stays on the board; with an extent of 1 the two
  departures on that axis return to the same Node in the next interval as
  its arrivals through those Ports (a four-Port node with a one-interval
  stub). Open stays the default; `"closed"` and every other word stay
  refused. `run.json` and `state.json` carry `boundary` as declared; the
  preflight's summary shows the boundary per axis ([the engine](docs/ENGINE.md),
  [migration](docs/MIGRATION.md#a-periodic-axis-as-a-declared-run-parameter-of-the-world-on-2026-09-19-boundary-per-axis)).
  Test: `test_periodic_axis` ([expectations](docs/TEST_EXPECTATIONS.md#a-periodic-axis)).
- A measured event's step wraps on a periodic axis, one rule for the board
  (the model owner, 2026-09-19): its step by its momentum (`_move`, step 6)
  lands on the first Node of the opposite face as the departures do, and
  with an extent of 1 on its own Node, no move and no merge with itself, the
  momentum untouched and the step counted in `steps`; through an open face
  it escapes with its content and momentum as before (the first periodic
  axis escaped a measured event on every face; [the engine](docs/ENGINE.md),
  [migration](docs/MIGRATION.md#a-periodic-axis-as-a-declared-run-parameter-of-the-world-on-2026-09-19-boundary-per-axis)).
  Test: `test_periodic_axis` (d) ([expectations](docs/TEST_EXPECTATIONS.md#a-periodic-axis)).
- A measured event is created again first and then reads its suspension:
  the count it owes, `suspension` intervals per whole unit of the other
  numbers' sizes at its Node, is read after its self-creation from this
  interval's sizes and paid before the next, so in a steady size of k whole
  units its clock is slowed by 1 / (k + 1), never frozen (Highlights 5.4:
  "releases and turns slower"). The first `events-v1` read before the
  self-creation and froze the clock of every measured event in a steady
  field of one whole unit or more (found by the physics-rule review of
  2026-09-19); worlds with `suspension` 0 are unchanged
  (`EventSimulation.step`, `_release`, `_suspend`, [the engine](docs/ENGINE.md),
  [migration](docs/MIGRATION.md#the-suspension-of-a-measured-event-read-after-its-self-creation-on-2026-09-19)).
  Test: `test_event_suspension` (b) re-pinned, (c) added
  ([expectations](docs/TEST_EXPECTATIONS.md#the-suspension)).
- The engine of the law of events (`events-v1`, `src/event_universe/events/`)
  is the one engine: one thing, the event, created at every interval at its
  next place from its record, at a neighbour or here; a measured event's clock
  the count of its self-creations and every rate read off it (`by_clock`); the
  suspension a count the event carries; the sides from the vectors in whole
  units, a single quantum whole by its momentum; no turn in transit; no
  register, remainder, parked share or draw; detectors by sensitivity
  ([the engine](docs/ENGINE.md), [migration](docs/MIGRATION.md)). The engine of
  the law of the shadow (`field-only-v1`) is deleted with its tests and worlds;
  the world file's keys are renamed (`measured`, `in_transit`, `suspension`,
  `detectors`; `phase_turn` gone). Tests: `test_node_mixing` (node-mixing-v2),
  `test_event_transit`, `test_event_suspension`, `test_event_clock`,
  `test_event_worlds` ([expectations](docs/TEST_EXPECTATIONS.md)).
- A detector's threshold gates every response of a detector's Node (`read`,
  `measure`, `rerelease`), receivers and re-emitters alike, by the model
  owner's instruction of 2026-09-19 that every kind of external apparatus
  works with the sensitivity: a bundle of one number below the threshold
  passes with no push and mixes on; a release reads no threshold
  (`EventSimulation._meet`, [the engine](docs/ENGINE.md)). Test:
  `test_detector_sensitivity` ([expectations](docs/TEST_EXPECTATIONS.md#a-detectors-sensitivity)).
- The phase window, `phase_window`, by the model owner's decision of
  2026-09-19 ("Approve the phase window as a declared width of a detector,
  and of the emitter too"; [Highlights 5.4](docs/HIGHLIGHTS.md#54-the-detector)):
  a setting on the circle of N steps and the half circle centred on it. On a
  table entry (`{"rule": ..., "phase_window": s}`, any rule but `pass`; the
  string form still accepted) the response, after the threshold, only to a
  bundle whose phase at the Node falls in the window, a bundle outside it
  passing with a `pass` record; on a lamp a release only at the
  self-creations whose clock phase falls in it, the clock and the phase
  turning regardless; the phase read on every measurement record
  (`Transit.phase_at`, `engine.in_window`, [the engine](docs/ENGINE.md),
  [migration](docs/MIGRATION.md#the-phase-window-on-2026-09-19-phase_window)).
  Test: `test_phase_window` ([expectations](docs/TEST_EXPECTATIONS.md#the-phase-window)).

### The law of events recorded (2026-09-19)

- The model owner's law of events, after the one engine and `phase_turn`
  ("there are no registers"; "there are no fields; a field is an event";
  "there is no matter either; matter is a measured event"; "a single quantum
  does not split; in the space of events the quantum leaves in one
  direction"; "there is no shadow and no real; on the board there are only
  events"), is recorded in [Highlights 5.4](docs/HIGHLIGHTS.md#54-the-detector)
  after "One speed, and what is seen", in the owner's words with the
  orchestrator's readings flagged, and the paragraphs it changes carry a dated
  sentence. Nothing of it is implemented: [Highlights coverage](docs/HIGHLIGHTS_IMPLEMENTATION.md),
  [ENGINE.md](docs/ENGINE.md), [PROJECT_STATUS.md](docs/PROJECT_STATUS.md) and the
  README say so. No code changes. The same day: every event carries momentum
  from birth ("By the momentum"); no return to the source; the suspension is a
  count the event carries; fifteen principles recorded after the law with the
  owner's decision on each, the fixing mechanism of their points 8 to 12 not
  adopted; what follows for Highlights and the engine, and the tests of the
  engine of events in 5.5.

### One engine (2026-09-19)

- The engine of the law of the shadow (`field-only-v1`, feature 20) is the one
  engine, by the model owner's decision of 2026-09-19 ("The field is, in fact,
  a field of events. No confrontations are needed. Only tests that everything
  is as designed."; [Highlights 5.4](docs/HIGHLIGHTS.md#54-the-detector)). The
  old engine of the law of the bit, its worlds, catalog, tools and tests are
  deleted ([migration](docs/MIGRATION.md#one-engine-on-2026-09-19-the-old-engine-deleted)).
  The substrate the new engine took from the old one moved to
  `core/lattice.py`, `core/phase.py` and `shadow/mixing.py`, byte-identical in
  what it does; the Node's mixing has its own isolated test again,
  `tests/test_node_mixing.py`, on one Node of the engine's layer.
- The runner takes `--init`, `--output` and `--ticks` only; the preflight
  checks world files only; the workspace lists the worlds of `examples/shadow/`
  and runs headless.
- The same day, earlier: the three pending decisions of the morning's status
  line (`transmitted_number`, the wait's unit, ε_g) were withdrawn ("We do not
  need these three things at all"), so the gate of feature 20b is not written;
  the wait is the delayed clock and `wait_per_quantum` stays a declared width
  of the world; and the owner's reading "A quantum passes, like everything, at
  the speed of light between Nodes" is recorded in 5.4 ("One speed, and what
  is seen").

- `families[i].phase_turn` (features 21 and 23; the owner's "what can be put
  as a parameter, put" and "constant frequency for light? Yes, make it the
  default for light. That is, per family."): how a family's quanta turn their
  phase per Link walked. `"quantum"`, the default for a paid family: by the
  family's quantum over K, the same for every quantum of the family wherever it
  is, the remainder carried per family, so light keeps the frequency it was
  born with (round 8, S5); `"none"`, the default for a free family; `"amount"`,
  the old rule by the amount in the cell, which slowed as the field thinned and
  stopped a few Links from a lamp, kept as a choice. Replaces the key
  `turns_in_flight` of the same morning ([migration](docs/MIGRATION.md#the-phase-turn-in-flight-per-family-on-2026-09-19-phase_turn));
  `tests/test_family_turns.py`.

- `families[i].quantum` (the owner's "put it in, without an experiment"): the
  units of a family that make one event at a holder that absorbs them (`keep`,
  the click; `rerelease`), per number, the rest waiting in the holder's
  register (`pending` in the content's state and on the held line of the
  books, `events` per family); 1 by default, every unit its own event as
  before; the derivation's q_γ as a declared width; `tests/test_family_quantum.py`.

### The law of the shadow, the field-only engine (`field-only-v1`, feature 20, 2026-09-18)

- A new engine mode beside the old one, `event_universe/shadow/`, selected by
  a world's `"law": "shadow"` key ([the law of the shadow](docs/MIGRATION.md)):
  only shadows and events. Matter is content held at Nodes; every ray is a
  shadow, a whole quantum in flight that moves one Link per interval and
  spreads by the Node's mixing, the dense layer's kernels by import; an event
  is a whole quantum at a Node with content, absorbed, held or released again
  by the holder's table (the free families read at a holder and passed on,
  the push by the holder's content and charge; light kept, the click, or
  re-released; the own number sunk for its amount and pushing nothing); a
  held content releases its field at the world's rate, a lamp spends its
  light; the wait reads the size; the step is the accumulator's, at most
  once in two intervals (round 8's Node rule, DERIVATIONS.md sections 51 to
  56); the books per family close at every tick. The old engine, its worlds and its
  tests are untouched ([migration](docs/MIGRATION.md#the-law-of-the-shadow-a-new-engine-mode-on-2026-09-18-field-only-v1)).
- The worlds `examples/shadow/` (one content, two contents, two slits and
  the one-slit control) and the isolated test `tests/test_field_only.py`
  ([expectations](docs/MIGRATION.md)), the
  numbers from DERIVATIONS.md round 7.

### Charge per thing (`charge-per-thing-v1`, feature 16g, 2026-09-18)

- The charge of a thing is one declared number of its family, whatever its
  content (the model owner, Highlights 5.4 point 16 as amended): a family's
  `charge` and a body's are the charge of one thing, whole, never a charge
  per quantum. The electricity reading multiplies the shadow's message (its
  owner's charge over its content, unchanged) by the whole charge of what is
  pushed; the worked example of point 16 holds exactly, a body of 1000 quanta
  with charge 1 is pushed by nine units and not nine thousand, and the
  catalog's electron of 20 does not turn at its first push.
- The charge readout, the ledger's charge line and the local audit count the
  whole charge of things: a merged ray of k things carries k times the
  family's charge (the identities a merge keeps), a record's stock the things
  it has not yet emitted, a shadow none; every table conserves it (the
  appended invariant sums the things' charges; a join keeps every identity).
- `run.json` records `charge_per_thing`; the refusal of a pushed body whose
  charge was not a multiple of its amount is gone. No example world's
  declaration changes; the tests whose bodies declared `-amount` to mean -1
  per quantum re-declare it ([migration](docs/MIGRATION.md#charge-per-thing-on-2026-09-18-charge-per-thing-v1)).

## 0.3.1 - 2026-09-15

Concept DOI 10.5281/zenodo.22738746 (the version DOI is listed on the Zenodo
record).

### Redshift from delay growth (second manuscript)

- `redshift_sweep.py`: a train of twelve rays crosses closed rows of 16 to 96
  Nodes under `ray_delay` to an absorbing eye that counts its own cycles;
  `1 + z = k_o / k_e` on the eye's clock, durations stretch by the same
  ratio, `z` from 0.07 to 2.81 with the distance, the slope scaling with the
  emission; the wave's frequency follows the gaps under the default phase
  rule by construction (the phase difference between rays is conserved along
  the path), read over the span it is measured on and converging with the
  tick resolution; a single source emitting at a fixed interval of its own
  clock (`--labels "single source"`) gives the same law. Moving bodies stall the
  clocks of the Nodes they wait at and are
  not used (report (`examples/relativity-probes/`, deleted on 2026-09-17)).
- `redshift_hubble.py`: the law's shapes against the Pantheon+ Hubble-flow
  sample, with the diagonal errors and (`--covariance`) the release's full
  covariance, the exponent fitted under each error model with its interval
  (refined in steps of 0.001 around the minimum) and the reading-A family
  bounded by its `n -> infinity` limit; the model's own load histories are
  behind LambdaCDM, and the best power law by nine units of chi-square with
  one fitted parameter each, as preferences between models (the shapes pass
  a goodness-of-fit test on their own); the Tolman exponent is the
  discriminating test, an indication against the lattice until the data
  are reduced under its own distance relations. Manuscript in `paper/redshift/` ([hypotheses](docs/HYPOTHESES.md)).


A review pass on the paper's Bell narrative. No engine change; the Bell probe
gains two modes and the framework's claims are narrowed to what is measured.

### Bell's test

- The bonded value carries its statistics: `--sweep` re-measures the bonded
  CHSH value with fresh pairs for every setting pair, 64 to 4096 pairs per
  correlation on the lattice with four replicas each and the registry alone
  to a million pairs, with binomial standard errors; every lattice outcome
  equals the registry's answer from the same seed, and `S` converges to the
  table expectation `724/256 = 2.828125`. The first run's 2.889 was sampling
  spread on correlated samples (report: `examples/bell-chsh/README.md`, deleted on 2026-09-17).
- Which assumption of Bell's theorem each candidate breaks is measured at
  fixed hidden variable by `--causal`: the lottery and the threshold are
  parameter independent; the bonded pair is deterministic and
  measurement-independent and breaks parameter independence (Bob's answer
  moves with Alice's setting for 0.72 of the hidden variables at
  `b'`); the quantum owner breaks outcome independence
  (report: `examples/bell-chsh/README.md`, deleted on 2026-09-17;
  coupling (`docs/QUANTUM_CLASSICAL_COUPLING.md`, deleted on 2026-09-17)).
- The door of postulate 22 is measured half by half: `--source agreement`
  keeps the coin even and fixes the agreement half, giving S = 4 (the
  Popescu-Rohrlich box) with even marginals and no signal; no-signalling
  bounds the coin, not the correlation (report: `examples/bell-chsh/README.md`, deleted on 2026-09-17).
- Postulates 4 and 22 name the broken assumption: the registry is a nonlocal
  resource in Bell's sense, its unmoved plus rates are no-signalling and not
  locality, and how a number is read (one end, both ends, or correlated with
  the settings) decides which assumption is at stake ([POSTULATES](POSTULATES.md)).

### Paper

- The manuscript is reframed as a finite-integer causal-lattice testbed: the
  configured laws are named as inputs, the Bell section carries errors and the
  causal analysis, "what is new" and "what is not claimed" are explicit, and
  the bonded pair is stated not to be a local explanation of the Bell value
  ([paper](paper/main.tex)).

## 0.3.0 - 2026-09-14

153 commits since 0.2.0. Zenodo DOI 10.5281/zenodo.22749342. Every number
below is recorded with its source fingerprint in [validation](docs/VALIDATION.md).

### Framework

- The framework is named Reality Theory (Universe24); the simulator stays
  Universe24 ([README](README.md)).
- Postulate 4 is split: energy, momentum, matter and every controllable
  message move at most one Node per step; the joint outcome of a bonded pair is
  the one declared exception, answered by a bounded registry that carries
  nothing physical ([POSTULATES](POSTULATES.md)).
- Postulate 22: every uncertain interaction consumes exactly one bounded
  integer; a bonded pair draws one number, whichever end asks first; the
  sequence is the only door for outside information and is bound by
  no-signalling.
- A [hypotheses page](docs/HYPOTHESES.md) keeps the questions the framework
  raises apart from measured results.

### Quantum and classical coupling (causal source candidate)

- Two-arm interference on the canonical runner: exact capture weights, a
  balanced Hadamard splitter, which-path decoherence, causal termination
  (report (`examples/quantum/causal_interference.md`, deleted on 2026-09-17)).
- Opt-in null notices restore the exact conditional Born weights after Link
  transit; crossing nulls are corrected locally by the later Node
  (crossing nulls (`examples/quantum/crossing_nulls.md`, deleted on 2026-09-17)).
- Opt-in field-dependent phase: an external classical field on one arm shifts
  the fringe by an exact configured phase per field unit.
- Opt-in funded emission: the wave pays for its own field from its conserved
  stock; totals constant; the retarded emission after a capture is the measured
  residual.
- Emission-scale sweep: the integer field follows `amount x |psi|^2` within one
  unit per tick at every scale.
- Two-wing Bell CHSH on the finite quantum owner: 14/5 exact, no-signalling
  marginals, dephased control 6/5 (report (`examples/quantum/bell_chsh.md`, deleted on 2026-09-17)).

### Straight and phased rays (Kerengonen candidate)

- Kerengonen phased rays with a fixed-point cosine table: double slit, Huygens
  slits, single-quantum lottery, de Broglie advance from momentum, mirror
  standing waves, matter-wave dissolution, Euclidean pace, claim and gather,
  bonded pairs.
- Bell's test on the ray with five captures on one scale: share 1.40 exact,
  lottery 1.48 and 1.38, threshold 2.00 exactly, bonded 2.89 against the
  quantum 2.83, plain field 2 (`examples/kerengonen-bell/` and `examples/bell-chsh/`,
  both deleted on 2026-09-17).
- An outside number source for bonded pairs: uniform is invisible, biased is
  a measured signal.
- Signed-quanta gravity with a closed ledger, gathered gravity (no dark-matter
  substitute from focusing), isotropy probe, relativity probes (lensing,
  redshift without recession, flat curves from a compressed closed dimension,
  gravitational phase in an interferometer, replay).

### Engine

- Local Focus scheduling (opt-in), ray ownership guards, carried allocation
  phases, ray delay and ray phase per tick, bounded prepared tables, 24-slot
  envelope output banks.

### Repository

- MIT license, `CITATION.cff`, Zenodo DOI 10.5281/zenodo.22738746 (0.2.0);
  named-particle gallery; documentation cleaned of process noise.

## 0.2.0 - 2026-09-14

First archived version: the integer lattice simulator with configured
disturbances, spatial fields, the finite quantum owner and the causal source
candidate. Zenodo DOI 10.5281/zenodo.22738746.
