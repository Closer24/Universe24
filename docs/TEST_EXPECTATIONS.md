# Test inputs and expected results

Since 2026-09-17, by the model owner's decision in
[Highlights 5.5](HIGHLIGHTS.md#55-acceptance-tests-and-open-decisions), a test
exercises one generic rule in isolation on a minimal board and nothing else: one
test module per rule, one per feature of the ray-event model, with the expected
integers written down here before the first run. No test pins the numbers of an
example world, compares two worlds or reproduces a known experiment; those are
research runs, made once and recorded with a fingerprint and a date in
[validation evidence](VALIDATION.md), never repeated as tests. Entries recorded
before that date describe the suite as it was and are brought under the rule
when their tests change.

## Suite inventory of 2026-09-19: one engine, the law of the ray

Decision of the model owner, 2026-09-19 ([Highlights 5.4](HIGHLIGHTS.md#54-the-detector),
"DECIDED: the law of the ray"; [the law of the ray](RAY_LAW.md)): one engine,
`rays-v1`, the law of events of the same day deleted with its modules. The
suite keeps one module per generic rule of the engine, on a minimal board,
and the repository gates. Every rule the ray law kept from the law of events
is re-pinned in a new module with the timing of the flight table; the
deleted modules and their rules are named in the
[migration notes](MIGRATION.md#the-law-of-the-ray-on-2026-09-19-rays-v1).
The sections of the deleted modules stay below as history (their headings
kept, their pins the law of events').

| Module | Rule isolated | Re-pins |
| --- | --- | --- |
| `test_ray_readings.py` | The one reading: the moments of order 0, 1 and 2 of the arrivals' direction vectors, taken once; equal to the slot decomposition on the six headings, the moments of the fan on a fan, covariant under the 48 board symmetries, bounded; the push by the flow of every number but the reader's own; the presence over rest and moving rays; the threshold over the set and the window per ray; the dense readings of the board decomposed on request for the active Nodes ([below](#the-one-reading)) | `test_one_reading_set` (a to d), `test_phaseless_family` (c), `test_detector_sensitivity` (b), `test_event_suspension` (e) |
| `test_default_table.py` | The table generated from the keys: a free family read, a paid one measured, no window; explicit defaults change nothing; what differs is kept; the kind derived from the quantum and `kind` refused; every example world equal to itself with the defaults written back ([below](#the-table-generated-from-the-keys)) | new |
| `test_ray_flight.py` | The flight: the table at 1 / sqrt 3 with its periods, a lone unit straight and unchanged, the isotropy, the periodic axis and the stub, the open face's click, `adjacent_node` ([below](#the-flight)) | `test_event_transit` (a), `test_periodic_axis` (a to c), `test_event_boundaries` |
| `test_ray_push.py` | The push as one bilinear form over the arriving rays' labels, the emitter's factor on the record, and the one momentum label the click, the re-emission, the home and the transit line move ([below](#the-push-as-one-form)) | new (2026-09-19, the night: the physics-rule review's F1 and the model owner's proposal 2) |
| `test_ray_collision.py` | The collision table: the classes, the bijection on all 3^8 states, the conservation, the 20 orbits, a head-on pair parking and a crowd passing; no collision at a Node that holds a measured event ([below](#the-collision-table)) | new |
| `test_ray_bijection.py` | The bijection: 50 intervals forward and 50 inverse return the store bit-exact; the merge by one packed key and by the lexsort alike ([below](#the-bijection)) | new |
| `test_ray_detector.py` | The detector's record: two rays in phase and in antiphase; the threshold gating a receiver and a re-emitter over the set; a release reading no threshold; the affordable amount bounded before the record's products ([below](#the-detectors-record)) | `test_detector_sensitivity` (a to c), `test_one_reading_set` (c) |
| `test_ray_reemission.py` | The re-emission on declared directions with the phase and the content kept; the face click; what comes home created again ([below](#the-re-emission)) | `test_border_and_clock_corrections` (b), `test_event_clock` (c) |
| `test_ray_clock.py` | The clock under the ray law: `by_clock` and `apportion_whole`; the release, the phase, the lamp's cost and recoil, the step and the refused step, the count off the clock ([below](#the-clock-under-the-ray-law)) | `test_event_clock` (a, b, d), `test_release_costs_by_phase_rate` (a to c), `test_border_and_clock_corrections` (a, c), `test_event_suspension` (b, c) |
| `test_push_width.py` | The width of the push: the world key `width` S in the step rule, one Link per (S x M + p) / p self-creations; S = 1 the rule as it was; the step off the clock with no remainder; the key's default and refusals ([below](#the-width-of-the-push)) | new (2026-09-19, the model owner's D1) |
| `test_ray_window.py` | The phase window under the ray law: the centred half circle on a table entry and on a lamp, the complement covering the circle, the refusals ([below](#the-phase-window-under-the-ray-law)) | `test_phase_window` (a to c) |
| `test_ray_world_parsing.py` | The world file of the ray law: the refusals by name, the direction table, the runner's record, the integer bounds of the measured line ([below](#the-world-file-of-the-ray-law)) | `test_event_worlds` (e), `test_integer_bounds_of_measured_and_emission` (a) |
| `test_ray_worlds.py` | The worlds of the ray law: the two slits fringing in the record and not in the count, the Bell worlds, one content streaming with the books closed, the example worlds parsing ([below](#the-worlds-of-the-ray-law)) | `test_event_worlds` (a, d) |
| `test_ray_books.py` | The books as running ledger lines: the transit, content and momentum lines of `books()` equal the recount over the store at every interval of a world that exercises every way a row comes or goes; an empty world ([below](#the-books)) | new (2026-09-19, the optimizations) |
| `test_configuration_validation.py` | The read-only preflight of a world file: the report, the refusals named by the parser, the command line |
| `test_entity_definitions.py`, `test_entity_loading_consumers.py` | The entity definitions loader and its consumers (the placement, the bundles, the refusals at runtime) |
| `test_json_documents.py` | The strict decoder shared by world files and the workspace's fragments |
| `test_integer_arithmetic.py` | The shared bounded integer primitives |
| `test_retention.py` | Generated-output ownership, lifetime and cleanup |
| `test_check_scope.py` | The affected-check's selection |
| `test_architecture.py`, `test_locality.py` | The dependency direction (`core` imports only `core`, the engine imports no host module, no physical module imports output or storage), the integer audit of `core/`, and LOCALITY-1 documented without an exception |
| `test_repository_language.py`, `test_repository_hygiene.py`, `test_repository_navigation.py` | The repository gates: English, one canonical copy, navigable links |

## The one reading

`tests/test_ray_readings.py` (docs/RAY_LAW.md, section 3 step 2 and section
10 note 16; the model owner, 2026-09-19: every piece of logic once; "the one
reading function is the amount-weighted moments of order 0, 1 and 2 of the
direction vectors, valid for fans as for the six headings, here entering the
zeroth moment alone"): `read_arrivals` takes once, over one reading set, the
moments of the arrivals' direction vectors weighted by their amounts (the
count split outside / here, the net flow sum amount x D, the traceless
tensor 3 x sum amount x D (x) D less its trace), and every coupling selects
its component by key.

- (a) the moments: on the six headings the amounts [3, 1, 4, 1, 5, 9] and 2
  here read outside 23, here 2, the flow (2, 3, -4) and the tensor
  diag(-11, -8, 19) (3 x diag(4, 5, 14) - 23 I), which is the slot
  decomposition of the first ray worlds exactly (its (p_x + p_y - 2 p_z,
  p_x - p_y) = (-19, -1) being -T_zz and (T_xx - T_yy) / 3); for 64 fixed
  random integer amounts on the seven slots the moments equal that slot
  decomposition through the same relations; on a fan (2 on (1, 1, 0), 3 on
  (2, -1, 0), 1 on (3, 1, 2), 4 on (1, 0, 0), 5 here) the flow is
  (15, 0, 2) and the tensor [[44, -3, 18], [-3, -19, 6], [18, 6, -25]]
  (3 x the second moment [[27, -1, 6], [-1, 6, 2], [6, 2, 4]] less its
  trace 37), traceless; under each of the 48 signed axis permutations R of
  the board the scalars are fixed, the flow is R x flow and the tensor
  R T R^T, on the fan as on the headings; the shortest reading, one unit on
  one heading e, reads outside 1, here 0, the flow e and the tensor
  3 e e^T - I; the keyed form over Nodes equals the readings Node by Node; a
  reading whose second moment could pass 2^62 - 1 (an amount above
  2^62 / 4096 on (64, 0, 0)) is refused with `OverflowError` before any
  product is formed, and the amount at the bound is accepted.
- (b) the push reads the flow of every number but the reader's own: a free
  reader of content 4 met by 9 rays of number 1 arriving on +X and 9 of
  number 2 arriving on -X is pushed by (0, 0, 0) and reads 18; by the 9 of
  number 1 alone (-36, 0, 0); with 5 of its own number arriving too the own
  add nothing (5 home, created again at the same interval's self-creation
  on its first declared direction).
- (c) the presence counts every ray at the Node of another number, rest and
  moving alike, and never the own: a measured event at `suspension` [1, 4]
  beside 64 rays of number 2 that arrived and 16 rays of number 3 at rest
  owes `by_clock(0, 80, 4)` = 20 after its first self-creation; with 8 of
  its own number among the arrivals still 20.
- (d) a detector's threshold reads the set of every number but its own and
  the window each ray's own phase: a receiver at threshold 3 met by 2 rays
  of number 2 and 1 of number 3 clicks all three, the 2 alone pass with a
  `pass` record each (`threshold` 3); at threshold 1 with the window 32,
  the two rays at phase 0 pass (`window` 32) and the ray at phase 32
  clicks.
- (e) the dense readings of the board are decomposed on request from the
  rows of the walk, for the active Nodes only (added 2026-09-19 with the
  optimizations of RAY_LAW section 10, note 22): on the open 9 x 3 x 3
  board with no measured event, 9 units arriving at (4, 1, 1) on +X and 9
  on -X, 3 arriving at (2, 1, 1) on +Y and 2 at rest at (6, 1, 1): after
  one interval the count is 18, 3 and 0 at those Nodes (21 over the
  board), the flow (0, 0, 0), (0, 3, 0) and (0, 0, 0), the presence 18, 3
  and 2 (23 over the board), the Links crossed per Port (9, 9, 0, 0, 0, 0)
  at (4, 1, 1) and (0, 0, 3, 0, 0, 0) at (2, 1, 1) (21 over the board);
  before the first interval, and on an empty board, every array is zero
  with its shape.

## The table generated from the keys

`tests/test_default_table.py` (docs/RAY_LAW.md, section 2 and section 10
note 15; the model owner, 2026-09-19, "I approve 1 and 3": the tables are
generated from the keys and a world declares only what differs, `kind`
derived from `quantum`).

- (a) the default: for the families m (quantum 0) and light (quantum 3)
  `default_table` is (("read", None, "vector"), ("measure", None,
  "scalar")); a measured event without `table` parses to exactly that, and
  so does one that writes the default out as strings, as objects with
  `reads`, as empty objects, or for one family only: the `RayWorld`s are
  equal field by field.
- (b) what differs is kept: a window alone ({"phase_window": 8}) keeps the
  default rule `measure`, the window 8 and the component `scalar`; `pass`
  and `rerelease`, `read` on a paid family and `measure` on a free one are
  kept with their components (`vector` on `read`, `scalar` otherwise);
  `reads` `tensor` and `here` are kept with the default rule; a `read`
  entry with the window 3 and `reads` `outside` on a paid family is kept
  whole.
- (c) the derived kind: quantum 0 is free, 1 and 2^30 paid; the unit label
  is 1 for a free family and the quantum for a paid one; `kind` is refused
  naming the removal of 2026-09-19 and docs/MIGRATION.md for the values
  `free`, `paid` and `other`; a family without `quantum` is refused naming
  the key; a negative quantum is refused; a charge on a paid family is
  refused naming its quantum; a charge on a free family and a lamp on a
  paid family are accepted, and a lamp on a free family is refused.
- (d) the example worlds: every world of `examples/events/` (the ten Bell
  and twenty-one coupling worlds, the four top-level worlds, the four
  detector worlds through the entity loader) parses equal, field by field,
  to the same document with the generated default written back into every
  measured event's table; no shipped world writes a default entry out.

## The flight

`tests/test_ray_flight.py` (docs/RAY_LAW.md, section 3): one speed for
every direction, 1 / sqrt 3, on the digital line of the momentum, at most
one Link per interval, the age modulo the direction's period.

- (a) the flight table: for every direction T_d >= S_1 Q and m(tau + 1) -
  m(tau) in {0, 1}; the periods (1, 0, 0) T 110, L 55; (1, 1, 0) T 156,
  L 39; (1, 1, 1) T 192, L 3; (3, 1, 0) T 350, L 175; a rest direction never
  moves; the first arrival of a heading ray at m Links, m = 1..11, in the
  intervals 1, 3, 5, 7, 8, 10, 12, 13, 15, 17, 19.
- (b) the lone unit: every heading and every declared direction of the
  two-slit example, 150 intervals on a periodic 61^3 board: the ray's
  position is the table's digital line, its direction and phase unchanged
  (`phase_per_link` 0), one row at every interval, at most one Link per
  interval; with `phase_per_link` 3 the phase turns 3 per Link crossed.
- (c) isotropy: 1000 intervals on (1, 0, 0), (1, 1, 0), (1, 1, 1),
  (3, 1, 0), (5, 2, 1): the Euclidean distance^2 within 2 % of 1000^2 / 3.
- (d) the periodic axis (re-pinned from `test_periodic_axis`): a ray on +Z
  at (2, 0, 0) of a 5 x 1 x 1 bar with {"z": "periodic"} steps onto its own
  Node at every interval the table moves it and never escapes, its phase 5
  kept; on the open bar it clicks on `face:+z` at the first interval (every
  ray steps at its first interval); on a 1 x 1 x 4 bar with {"z":
  "periodic"} the ray at z = 3 on +Z is at z = 0 after the first interval
  and the ray at z = 0 on -Z at z = 3, the ray on +X escapes on `face:+x`;
  the refusals of the boundary and the record.
- (e) `adjacent_node` on (3, 2, 1) with x and z periodic (re-pinned from
  `test_event_boundaries`): (2, 1, 0) +X -> (0, 1, 0), (0, 1, 0) -X ->
  (2, 1, 0), (1, 1, 0) +Y -> None, +Z and -Z -> (1, 1, 0) itself.

## The collision table

`tests/test_ray_collision.py` (docs/RAY_LAW.md, section 4): eight slots per
Node, the six headings in Port order and two rest slots; a slot empty,
single or a crowd; the class of a state (the crowd mask, the number of
singles, their headings' sum); inside a class the forward map is the cyclic
shift by +1 and the inverse by -1, generated from the rule.

- (a) 3^8 = 6561 states, 5440 classes, 2132 moving states, 202 of the 256
  binary states; INV[FWD[s]] = s for every state; the class of FWD[s] is
  the class of s; a crowd slot never changes; the amount and the heading sum
  are conserved by every move.
- (b) the 20 orbits of the (six-heading pattern, here flag) under the 48
  signed axis permutations, with the sizes 1, 6, 3, 12, 12, 3, 8, 12, 6, 1
  (here 0) and the same with here 1; a lone unit is fixed; the head-on pair
  +x -x parks in the two rest slots, and ha hb becomes +z -z.
- (c) on the board: two rays of amount 1 meeting head-on at the middle Node
  of a 5 x 1 x 1 bar (x and z periodic) become the two rest rays at that
  Node in the interval they meet, and stay; two rays of amount 2 (a crowd)
  pass each other; over the six orientations of a head-on pair on a periodic
  5^3 cube the x pair parks, the y pair turns onto x and the z pair onto y,
  and after the second collision the rest pair leaves on z, the x pair
  parks and the y pair turns onto x: the one cycle of the class, the tie by
  Port order.
- (d) no collision at a Node that holds a measured event (the model owner's
  decision of 2026-09-19 on the physics-rule reviewer's F1(c); RAY_LAW
  section 3 step 3 and note 18): the head-on pair of (c) (one number,
  amount 1, phases 0 and 32) meeting at the Node of a measured event of `m`
  whose table passes `light` keeps its directions +x and -x (no rest ray),
  dwells the two intervals of its line there and parts at the third (x = 5
  and x = 3 on a 9 x 1 x 1 bar); at a measured event whose table measures
  `light` in the window 32 the ray at phase 32 clicks with its label
  (-1, 0, 0), the ray at phase 0 passes and goes on to x = 5, the transit
  line is (1, 0, 0) and no ray is stranded at rest; measured + transit =
  (0, 0, 0), the labels' sum before the interval.

## The bijection

`tests/test_ray_bijection.py` (docs/RAY_LAW.md, section 3): a periodic
8 x 8 x 4 board, 300 records of fixed arrays (rays on every heading, both
rest slots and two fan directions, head-on pairs among them, amounts 1 and
2, phases over the circle), 50 forward then 50 inverse intervals with no
measured event: the sorted store equal to the start in every field; the
state at the turning point differs from the start; the collision moved at
least one ray on the way.

The merge (step 6; added 2026-09-19 with the optimizations of RAY_LAW
section 10, note 22): 82 fixed rows (60 distinct over 200 Nodes, 10
directions, 23 ages, the circle, 3 numbers, 3 contents, charges 0 and -1,
5 masses; 20 of them repeated; two extremes) merged by the packed key of
the identity fields equal the Python sort of the identity tuples with the
amounts of equal tuples added, 62 rows, every arrival reset to here; the
same rows with every other mass raised by 2^61 (the key does not fit the
register, `merge_key` is None) merged by the lexsort fallback equal their
Python sort likewise; the empty store merges to the empty store.

## The books

`tests/test_ray_books.py` (docs/RAY_LAW.md, section 10, note 22; added
2026-09-19 with the optimizations): `books()` reports the transit line,
the content line and the transit momentum as the running lines of the
ledger (what was released less what left: escaped, home, absorbed;
O(families), no pass over the store) and `recount()` counts the same
three lines from the rows of the store. On a 12 x 1 x 3 board with y
periodic and every other face open (K 2^20, N 64, `release` [1, 4], the
fan direction (2, 1, 0)): a lamp of `light` (content 2^23) at (1, 0, 1)
releasing 3 units per self-creation on +X, (2, 1, 0) and +Y (the +Y unit
home next interval, created again on the six headings), a re-emitter of
`light` at (5, 0, 1) on +X and -X, the detector `screen` at (9, 0, 1), a
free source `m` (content 2^19) at (10, 0, 1), beyond the screen, releasing
2^17 per heading (escapes through the z and x faces, homes on +-Y, reads
at the screen, the re-emitter and the lamp), and a head-on pair of `light` meeting at
(4, 0, 0) in free space, parked at rest by the collision in the interval
they meet (the table moves them on later): at every one of 40 intervals
the running lines equal the recount, `books(recount=True)` equals
`books()` and the books balance; the momentum line is nonzero at some
tick; the two rest rays sit at (4, 0, 0) after the first interval; the
records hold a home of each family, a re-release, a read, a click at the
screen, a click at the lamp and face clicks (`m` on +z, +x and -x, `light`
on -z). An empty world counts zero both ways.

## The detector's record

`tests/test_ray_detector.py` (docs/RAY_LAW.md, section 5). K 2^20,
`suspension` 0, `release` [0, 1], the families `m` (free) and `light`
(paid), every measured event `fixed`.

- (a) two rays of amount 1 arriving in one interval at a counter of
  threshold 1, in phase (0 and 0): the record 4 x 32^2 x 256^2 = 268435456,
  the amount 2 and two clicks; in antiphase (0 and 32): the record 0, the
  amount 2 and two clicks; one ray alone: 32^2 x 256^2 = 67108864; the
  `record` line of `events.jsonl` carries the pointer (X, Y) and the
  square; the run's detector report carries the cumulative record.
- (b) a receiver (a measured event of `m`, content 4, measuring light) at
  threshold 3 (re-pinned from `test_detector_sensitivity` (a)): 2 rays of
  another number pass with a `pass` record (`threshold` 3), no click, no
  push, the rays going on whole; 3 rays are measured: 3 clicks, `held`
  [4, 3], the momentum (3, 0, 0), nothing left in the store, the report 3
  measured, 3 clicks, the record 9 x 32^2 x 256^2 (a row of three identical
  rays is one coherent amplitude).
- (c) a re-emitter at threshold 3: 2 rays pass; 3 rays are taken
  (re-released 3, no click, the push (3, 0, 0), the recoil at the
  re-emission -(1, 1, 1) leaving the momentum (2, -1, -1)) and created again
  at the same interval's self-creation, one per declared direction (+X, +Y,
  +Z), with the re-emitter's number, the arriving phase 20, content 1,
  age 0.
- (d) an emitter inside a detector reads no threshold: a lamp of light
  (content 24, K 24, rate [1, 1]) in a detector of threshold 5 releases one
  unit per heading per interval, its content 18 then 12; a reader of `m`
  (content 4) at threshold 4 passes 3 rays and reads 4, pushed by -M c =
  (-16, 0, 0).
- (e) the affordable amount (the physics-rule reviewer's F2; RAY_LAW
  section 5 and note 19): every entry (C, S) of the 1/256 tables is
  shorter than 257 for every N from 2 through 4096 (the largest C^2 + S^2
  is 65897), so the pointer is at most 32 x 257 x the clicked amount long
  and the record fits 2^62 - 1 up to isqrt(2^62 - 1) // (32 x 257) =
  261123 units per detector Node per family per interval
  (`RECORD_AMOUNT_BOUND`; 2^17 inside, 2^18 refused): a row of 261123 at
  phase 0 records 2139119616^2 with the pointer (2139119616, 0); a row of
  261124 is refused with `OverflowError` naming the Node [4, 1, 1] and the
  sum 261124; two rows of 130561 and 130563 (two numbers, +X and -X) are
  refused naming the sum 261124; a row of 2^52 (the reviewer's silent int64
  wrap, admitted by the label bound) is refused naming the sum; a ray of
  261124 stepping off an open face is refused naming `face:+x`.

## The push as one form

`tests/test_ray_push.py` (docs/RAY_LAW.md, section 3 step 4, section 5 and
section 10 notes 18 to 20; the model owner's proposal 2 of 2026-09-19 with
the physics-rule reviewer's two corrections): push_A = sum kappa(A, B) . V_B
with V_B the label moment of the arriving rays and kappa = -M_A (a free
family's ray), + q_A x q_B / M_B (a charged one, the whole part off the
reader's clock, sign x by_clock(age_A, |V q_A q_B|, M_B)), + 1 (a paid
ray); the emitter's factor (q_B, M_B) on the record from birth; every
momentum the law reads or moves the one label. K 2^20, N 64, `suspension`
0, `m` free and `light` paid, every measured event `fixed`, a 12 x 1 x 1 bar
with y and z periodic unless said otherwise.

- (a) the reviewer's isolated world: a source of content 4 and charge 3 at
  x = 0 releasing on +X at `release` [1, 1] (4 rays per interval, one row of
  amount 4), a probe of content 5 and charge 1 at x = 6; on (1, 0, 0) a ray
  born at tick t is at x = 6 at tick t + 10, so the probe reads one row of
  amount 4 at every tick 11 through 30: 20 `read` records, each the flow
  V = 4 and the push -5 V + by_clock(age, 3 V, 4) = (-17, 0, 0), `pushed`
  (-340, 0, 0) (80 x (-5 + 3/4) exactly); the record's `mass` 4 and
  `charge` 3.
- (b) the sign (the source's charge -3): every push (-23, 0, 0), `pushed`
  (-460, 0, 0). (c) An uncharged probe: every push (-20, 0, 0), `pushed`
  (-400, 0, 0).
- (d) q_A q_B = M_B with M_A = 1 (the series 7 cancellation): the probe of
  content 1 and charge 2, the source of charge 2 and content 4: every push
  0 exactly, `pushed` (0, 0, 0).
- (e) the fractional floor (the reviewer's F6): `release` [1, 2] gives
  V = 2, |V q_A q_B| = 6, and by_clock(t, 6, 4) is 2 at odd t and 1 at
  even t from t = 11; over the ticks 11 through 30 the electric part sums
  to 30 and the gravity to -200: `pushed` (-170, 0, 0).
- (f) a paid emitter: a lamp of `light` (content 2^23 at K 2^20, the turn
  8 at every age below 362, `rate` [1, 1] on +X) releases one unit of
  content 8 per interval with the recoil (-8, 0, 0); the probe (content 5,
  `table` {"light": "read"}, `release` [0, 1]) reads (8, 0, 0) at every
  tick 11 through 30, `pushed` (160, 0, 0); the lamp's momentum (-8 x its
  releases) plus the transit line plus the escaped line is (0, 0, 0) at
  every tick.
- (g) a fan emitter: a source of content 4 at (0, 0, 0) of a 9 x 5 x 1
  board releasing on (2, 1, 0) at `release` [1, 1], the probe of content 5
  at (4, 2, 0) on its line (the sixth Manhattan step; the first read at
  tick 9): every push -5 x 4 x (2, 1, 0) = (-40, -20, 0), 22 reads,
  `pushed` (-880, -440, 0): the push of a fan ray is its label, |D| =
  sqrt 5 per unit.
- (h) the one label moves: a ray of `light` of amount 3 on (2, 1, 0)
  (content 1; at (3, 2, 0) with age 7, one Link before (4, 2, 0)) clicking
  at a `measure` event at (4, 2, 0): the click's `push` (6, 3, 0), the
  event's momentum (6, 3, 0), the transit line (6, 3, 0) before and
  (0, 0, 0) after; the same ray at a `rerelease` event whose one direction
  is (2, 1, 0): the momentum (0, 0, 0) after the interval (in (6, 3, 0),
  out the same), the transit line (6, 3, 0) before and after; a paid ray
  coming home on a periodic 4 x 1 x 1 bar: the `home` record's `push` is
  its label (1, 0, 0) and the emitter's momentum (0, 0, 0) after the
  re-creation.
- (i) the factor is read off the rows met (added 2026-09-19 with the bulk
  step 4): the world of (a) with two bystander rays of the probe's number
  (charge 1, mass 5 on their record) parked on the stub of the y axis at
  x = 2 and 3, rows before the probe's in the store: every push (-17, 0, 0)
  and `pushed` (-340, 0, 0) as in (a), the bystanders untouched.

## The re-emission

`tests/test_ray_reemission.py` (docs/RAY_LAW.md, section 5). K 2^20,
`suspension` 0, `release` [0, 1], the families `m` (free) and `light`
(paid).

- (a) one ray of amount 3 (content 1 per unit, phase 20) into a `rerelease`
  Node of `m` (content 4) with the three directions +X, (1, 1, 0) and
  (2, 1, 0): three rays of amount 1 at the Node after the interval, one per
  direction, phase 20, age 0, the re-emitter's number 1, content 1; the
  push (3, 0, 0) taken, the recoil -(1 x (1, 0, 0) + 1 x (1, 1, 0) + 1 x
  (2, 1, 0)) = (-4, -2, 0), the momentum (-1, -2, 0); the books closed
  (absorbed 3, released 3; the content line absorbed 3, released 3); a ray
  of amount 4 on the same Node: 2, 1, 1 (the leftover to the direction
  `age mod 3` = 0, the first).
- (b) the face click (re-pinned from `test_border_and_clock_corrections`
  (b)): a ray of amount 1, phase 5, content 1 at (2, 0, 0) on +X of a
  3 x 1 x 1 bar steps off the board at the first interval: one `click` on
  `face:+x` (tick 1, Node (2, 0, 0), `measured` None, number 1, amount 1,
  phase 5, momentum (1, 0, 0), content 1), the escaped amount 1, the face's
  record 32^2 x (C[5]^2 + S[5]^2), the books' escaped lines the faces'
  sums; the same bar with {"x": "periodic"}: no click, the ray at x = 0; a
  measured event of `m` (content 16, momentum (16, 0, 0)) at x = 2 steps
  off at interval 2: one `click` on `face:+x` with `measured` 1, amount 16,
  phase 2 (K 16), momentum (16, 0, 0), `held` [16, 0], `home` [0, 0], the
  measured line's escaped 16.
- (c) home: a lamp's ray (content 1, phase 7) returning to its lamp on a
  periodic 4 x 1 x 1 bar is home after 4 Links (the intervals 7, 14, ...)
  and leaves again on the lamp's one direction with phase 7 and content 1,
  the books closed.

## The clock under the ray law

`tests/test_ray_clock.py` (docs/RAY_LAW.md, section 3, step 5; re-pinned
from `test_event_clock`, `test_release_costs_by_phase_rate` and
`test_border_and_clock_corrections` (a, c) with the flight table's timing).

- (a) `by_clock`: at rate 3 / 10 the gains over ages 0 to 9 are 0, 0, 0, 1,
  0, 0, 1, 0, 0, 1; 70 over 30 ages at 7 / 3; `apportion_whole`: 7 over
  [3, 3, 0, 0, 0, 1] from 0 is [3, 3, 0, 0, 0, 1], 5 over [2, 2, 2, 0, 0,
  0] from 2 is [2, 1, 2, 0, 0, 0].
- (b) a measured event of content 3 at `release` [1, 10] releases one ray
  per declared direction (the six headings) at its self-creations to ages
  4, 7 and 10: 18 released after 10 intervals, 0 after 3; at K 2 its phase
  steps after four intervals are 1, 3, 4, 6.
- (c) a lamp of content 100 at rate [1, 3] on six headings, K 82: 18 rays
  after 9 intervals, each of content 1, the content 82, 9 phase steps, the
  recoil zero; two lamps of turns 4 and 8 (K 4096, contents 4 K + 32 and
  8 K + 64, one ray per self-creation toward a counter 3 Links away on a
  7 x 1 x 1 bar): after 8 intervals A spent 32 and B 64, the releases of
  intervals 1 to 3 clicked in intervals 6 to 8 (a ray created at tick t
  first walks at t + 1 and 3 Links take 5 walks): 6 clicks, the counter's
  content 37, its momentum (-12, 0, 0), each click record with `content` 4
  or 8, 10 rays in flight carrying 60, the books balanced; a lamp of turn 0
  releases nothing.
- (d) the step: content 16 with momentum 16 on +x steps once per two
  self-creations (three after six intervals); with momentum 1 none after 16
  and one after 17; the momentum untouched; a step onto a Node that holds a
  measured event is refused, both remain, the step counted.
- (e) the count off the clock: a source of `m` of content k at x = 0 of a
  2 x 1 x 1 bar releasing k rays per direction per self-creation at
  `release` [1, 1] and a probe of `light` (content 1, measuring `m`) at
  x = 1 at `suspension` [1, 4]: the probe reads the presence k every
  interval from the second on, and with k = 1 owes `by_clock(age, 1, 4)`,
  1 at the self-creations from the ages 3, 7, 11, 15: its age after
  intervals 1 to 20 is 1, 2, 3, 4, 4, 5, 6, 7, 8, 8, 9, 10, 11, 12, 12, 13,
  14, 15, 16, 16; with k = 8 it owes 2 at every self-creation: 1, 2, 2, 2,
  3, 3, 3, 4, 4, 4.

## The width of the push

`tests/test_push_width.py` (docs/RAY_LAW.md, section 3, step 5 and
implementation note 15; the model owner's D1, 2026-09-19). One rule in
isolation: an open bar of 12 x 1 x 1, K 1024, N 64, `release` [0, 1] (no
push arrives), a free measured event of content M with the momentum p on
+x; the step rule `by_clock(age, |p|, S x M + |p|)` with S the world's
`width`. The expected integers, written down before the first run:

- (a) S = 1 reads exactly as the rule was: content 16 with momentum 16 from
  x = 4 steps at the ages 2, 4, 6 (x after intervals 1 to 6: 4, 5, 5, 6,
  6, 7; `steps` 0, 1, 1, 2, 2, 3), with `width` 1 declared and with the key
  absent alike; with momentum 1 none after 16 intervals and one after 17.
- (b) S = 8 with p = M: content 16 with momentum 16 steps once per 9
  self-creations, at the ages 9, 18, 27 (x 4 through interval 8, 5 from 9,
  6 from 18, 7 at 27; `steps` 0, 1, 2, 3); content 3 with momentum 3 steps
  at the same ages (the speed a unit of flow gives, 1 / (S + 1), is the
  same for every content).
- (c) off the clock, no remainder: the probe of (b) at x = 3 with
  `suspension` [1, 4] and a crowd of 4 rays of another number (a fixed
  anchor of content 1 at x = 11) at rest on x = 3 to 7 owes one interval
  after every self-creation (age after interval n is ceil(n / 2), waited
  floor(n / 2)); the step of the ages 9, 18, 27 lands on the interval that
  pays the count (a measured event steps only in an interval where it owes
  nothing), the intervals 18, 36, 54: x after intervals 17, 18, 35, 36,
  53, 54, 60 is 3, 4, 4, 5, 5, 6, 6; age 30, waited 30, `steps` 3 after
  60; after every paying interval `steps` = age x 16 // 144 and after every
  self-creation (age - 1) x 16 // 144; the momentum untouched; the books
  balanced at every interval. (The first run corrected the interval of the
  step from 17 to 18: the order of the frame, not the rule.)
- (d) a world without `width` parses to 1; `width` 8 parses to 8 and the
  runner's `run.json` carries `width` 8; 0, -1, `"8"` and 1.5 are refused
  with "width must be an integer from 1".

## The phase window under the ray law

`tests/test_ray_window.py` (re-pinned from `test_phase_window` under the
flight table: a ray released at tick t first walks at t + 1; 10 Links take
17 walks, 11 Links 19). Bars of 1 x 1 in y and z, N 64, `suspension` 0,
`release` [0, 1], the families `light` (paid) and `counter` (paid).

- (a) the boundary of the window at N = 64: a counter at x = 6 of a
  7 x 1 x 1 bar measuring `light` through the window 20; four rays of
  number 1 on +X at x = 5 with phase 35 (d = 15), x = 4 with 36 (d = 16),
  x = 3 with 3 (d = 47) and x = 2 with 4 (d = 48), reaching x = 6 in
  intervals 1, 3, 5 and 7. d = 15 and d = 48 click (`click` records at
  ticks 1 and 7 with `phase` 35 and 4, the push (1, 0, 0), `content` 1);
  d = 16 and d = 47 pass (`pass` records at ticks 3 and 5 with the phase
  and `window` 20), go on and click on `face:+x` at their next step (ticks
  5 and 7). After 7 intervals `events` [2, 0], `held` [2, 1], the momentum
  (2, 0, 0), 2 escaped, nothing in the store, the books balanced;
  `in_window` at N = 64 admits d in [0, 16) and [48, 64), at N = 2 the step
  0, at N = 4 the steps 0 and 3.
- (b) the complement covers the circle exactly: a bar of 12 x 1 x 1,
  K 2^14, a lamp of `light` (content K + 2, phase 0, rate [1, 1] on +X
  only) at x = 0; a counter at x = 10 measuring through the window 40 and
  its complement at x = 11 through the window 8. The release of age a
  (tick a + 1) reaches x = 10 at tick a + 18 and x = 11 at tick a + 20:
  after 83 intervals the two counters clicked 32 times each, x = 10 the
  phases 24..55, x = 11 the phases 0..23 and 56..63, every one of the first
  64 releases exactly once; 34 `pass` records at x = 10 and none at x = 11,
  nothing escaped; the lamp at age 83, phase 19, content K + 2 - 83,
  momentum (-83, 0, 0).
- (c) a lamp with a window: the lamp of (b) with `phase_window` 8 and a
  plain counter at x = 10: at each of the first 64 intervals t its age is
  t, its phase t mod 64, and it released one ray at phase t - 1 when t - 1
  is in the window (the ages 0..23 and 56..63) and none otherwise: after 64
  intervals 32 released, content K + 2 - 32, momentum (-32, 0, 0), phase 0;
  after 81 the counter clicked 32 times and the lamp released 17 more, 49
  in all. The refusals, naming the key: a window of 64 at N = 64, a window
  on `pass`, an object entry with an unknown key, a lamp window of -1, a
  `reads` key outside the reading's components; an object entry without
  `rule` takes the family's default rule (since the night of 2026-09-19: a
  window alone on a paid family measures in the window 8).

## The world file of the ray law

`tests/test_ray_world_parsing.py` (docs/RAY_LAW.md, sections 2 and 7;
re-pinned from `test_event_worlds` (e) and
`test_integer_bounds_of_measured_and_emission` (a)).

- (a) refused, naming the key: `"law": "events"` (naming the law of the ray
  and MIGRATION), `dynamics`, `max_active_owners`, `headings` on a lamp,
  `heading` on a ray, `port_map`, `groups` on a detector, a non-primitive
  direction (2, 2, 0), a component beyond P (65 at the default bound), a
  direction the world does not declare, a rest direction on a lamp, a
  repeated direction, a momentum label beyond 2^62 - 1 on a declared ray
  and on a lamp's release, `phase_per_link` outside 0 .. N - 1 or on a
  family without a phase circle, the earlier engines' keys, `phase_turn`, a
  closed board, an unknown key, a content at K x N / 2, a lamp on a free
  family, two measured events at one Node, an unknown table rule, N not a
  power of two, a detector on a Node without a measured event, a Node in
  two detectors, `kind` on a family (naming MIGRATION: the quantum decides
  the kind), a family without `quantum`, a negative quantum, a charge on a
  paid family, a `suspension` denominator of 0, a window for a family
  without a phase circle.
- (b) accepted: the direction table of a world with `directions`
  [[1, 1, 0]] is the two rest vectors, the six headings and (1, 1, 0); a
  measured event's `directions` by vector or by index; a ray at rest (index
  0); `suspension` 1 as (1, 1), [1, 4], [0, 4] as (0, 1); `reads` per entry.
- (c) the runner: a 4-interval world into `run.json` (`law` "rays-v1",
  completed, four ticks, four books, conserved, the measured events, the six
  face detectors of the open board with their `record`, the directions
  table, `suspension` [1, 1]), `state.json` (the law, tick 4, the Nodes with
  rays) and `events.jsonl`; a negative tick count and a used output
  directory refused.
- (d) the bounds: two measured events of content 64 one Link apart at
  `release` [1, 1] read each other's 64 rays from interval 2 on and are
  pushed by 64 x 64 = 4096 toward each other; the second, declared with the
  momentum -(2^62 - 1) + 4096 on x, reaches the bound exactly and is
  accepted; one unit nearer it is refused with `OverflowError` naming the
  measured event, its Node and the momentum; a reader of content 2^56 - 1
  met by 64 rays takes the push -(2^62 - 64), and at 2^56 the push -2^62 is
  refused naming the push.

## The worlds of the ray law

`tests/test_ray_worlds.py` (docs/RAY_LAW.md, section 7): the worlds of
`examples/events/` on minimal boards, pinned as a check that the engine
does what the law says and not as a result.

- (a) the two slits (the example world's design, 60 x 121 x 1, z periodic,
  500 intervals): a lamp at (2, 60) of turn 8 per self-creation (K 2^30,
  content 8 K + 1 400 000, 64 rays per self-creation on five directions), a
  wall at x = 8 measuring light with the openings at y = 55 and 65
  re-emitting on the fan of the 91 primitive directions (a, b, 0) with
  a >= 1 and a + |b| <= 12, a screen at x = 52 as the detector `screen`.
  Three runs, both openings and each alone: the plain count is additive to
  the unit (count_both = count_55 + count_65 at every screen Node) and the
  interference term V(y) = (I_both - I_55 - I_65) / (2 sqrt(I_55 I_65)) of
  the record correlates with the two-source Euclidean cosine at lambda =
  c x period = 8 / sqrt 3 above 0.85 over the Nodes both openings reach
  (the design pinned 0.9 for a fan of 203 directions; measured 0.893 with
  the 91 of this world), and the correlation at the periods 4 and 16 is
  below 0.5.
- (b) Bell (the ten A2 worlds under `"law": "rays"`, `tools/bell_chsh.py`):
  S = 2 exactly, S' = 3/2 exactly, the controls +1, -1, 0, no-signalling
  exact, 0 criteria failed.
- (c) one content of 2^24 at the centre of an open 11^3 board at `release`
  [1, 128], 40 intervals: the books close at every tick, the content is
  2^24 at every tick, the momentum on the measured events zero, the flux
  through the cube of half-width 2 equals the emission q = 6 x 2^17 at
  every interval once the front has passed (six beams on the six headings,
  a ballistic stream: Gauss exact); the shell means once steady: the count
  at r = 3 and r = 4 is 6 x 2^17 over the shell's Nodes, the presence at
  r = 3 twice the count and at r = 4 equal to it.
- (d) every example world (`examples/events/*.json`, `bell/`, `coupling/`,
  `detector/` through the entity loader) parses as a ray world. The orbit
  worlds of series D are research runs registered in
  [EXPERIMENTS](EXPERIMENTS.md#d-the-orbit-under-the-law-of-the-ray-on-the-plane-2026-09-19)
  and pinned by no test (the model owner's rule of 2026-09-17; the pin of
  the first registration, `test_orbit_world.py`, went with its numbers
  when the engine changed).

## Generated-output lifetime

These are host filesystem contracts; they do not change simulated time or costs.
See [RETENTION.md](RETENTION.md) for ownership and expiry policy.

| Suite | Independent expectations |
| --- | --- |
| `test_retention.py` | Registered generations expire at 24 hours; later writes extend age; active and dependent writer locks survive future cleanup; unregistered, protected, linked and replaced files survive; interrupted quarantine resumes without deleting replacement data; expected adoption identity rejects stale inventory; concurrent catalog use waits; duplicate watchers share one lock |
| `test_check_scope.py` | Explicit non-import edges retain the kept resource consumers and every row names an existing test; the exact scope report expires while unrelated files survive; dry-run creates no output |

Ordinary test execution leases its JUnit report. Neither test collection nor
cleanup enables rendering.

## Running and validating changes

The suite reuses world runs when their inputs and required observations coincide.
The historical scalar, stream, link, collision and balanced regressions were
deleted with their engines on 2026-09-17 (issue #164, bucket A), and the same
day the suite was reduced to one module per generic rule and one per feature
of the ray-event model (inventory,
[migration note](MIGRATION.md#test-suite-reduced-on-2026-09-17-one-test-per-rule));
the dated records in `VALIDATION.md` keep their original scope.

Run `python tools/check.py` from the installed project. It checks style, types and
behavior. Pure-function unit tests do not run a world. See `VALIDATION.md` for
recorded validation and tool versions.

A new law requires inputs, expected outputs and edge cases before implementation.
Test its generic calculation and engine integration independently. Static checks
enforce known boundaries; they do not replace behavioral tests.

## Repository navigation

`test_repository_navigation.py` checks local Markdown destinations in root
documents, docs and Skills against the actual tree. It also checks that every
specialist is reachable from Boss and references the shared workflow. Synthetic
valid and missing file/heading links exercise rejection independently. No world
runs are added. External URL reachability and instruction quality still require
review; this check does not certify physical acceptance.

## Shared instructions and architecture boundaries

- Repository input: AGENTS.md must exist, be linked by README, contribution and
  architecture documents, and be included in MANIFEST.in. Referenced documents
  must exist. CI runs the same validation command used locally.
- The dependency direction (`tests/architecture_rules.py`): `core` imports only
  `core`; the engine (`events`) imports only `core` and `events`, except
  `events/run`, which writes the artifacts; no physical module imports an
  output or storage library; synthetic upward and output imports are rejected
  and the legal ones pass. Every module of `core/` passes the static integer
  audit (no float literal, division, `sqrt` or numpy).
- These tests do not run worlds and do not prove that an agent in another
  conversation has read the instructions.

## Locality and bounded local work

`test_locality.py` creates no world and advances no time: it checks that
LOCALITY-1 is documented in SIMULATOR_DEFINITIONS.md and AGENTS.md without an
exception (end-to-end provenance, fixed work and storage for fixed K).
LOCALITY-1 also requires manual end-to-end review of every input of a physical
rule; passing this check alone does not establish it.

## Repository language

The English-only rule is authoritative in AGENTS.md and linked from the
architecture guide. The language test scans project source, tests (including
frozen references), tools, docs, root text files and workflow configuration.
Generated artifacts, installed dependencies and Git history are outside its scope.

Examples contain escaped test data: a Hebrew comment, docstring or heading must
be rejected; English prose and mathematical notation must pass. The script check
also rejects Arabic, Cyrillic, CJK, Hiragana, Katakana and Hangul letters. It is a
guard against non-English scripts, not a language classifier: Latin-script prose
still requires review. No physical calculation changes as part of translation.

## Shared integer arithmetic

`test_integer_arithmetic.py` pins the primitives of `core/integer.py` that the
ray law uses: the working register (`checked_work` accepts +-(2^63 - 1),
refuses one beyond and a boolean); the exact integer square root
(`integer_root`: 0, 1, 2, 3, 4, 15, 16, 17, 2^62 and 2^63 - 1 give 0, 1, 1, 1,
2, 3, 4, 4, 2^31 and 3037000499, each the floor with the next square above the
input; a negative value, a float and an overflow are refused); the bounded gcd
(`bounded_gcd`: 12 and 18 give 6, 0 and 5 give 5, 5 and 0 give 5, -4 and 6
give 2, 0 and 0 give 0, 2^63 - 1 and 1 give 1; an overflow and a boolean are
refused). `by_clock` and `apportion_whole` are pinned where the clock uses
them (`test_ray_clock`, `test_ray_readings`). The component arithmetic of the
deleted engines (signed and ceiling division, ordered sums, component addition
and subtraction, dot and cross products, reduced ratios) was deleted with its
pins on 2026-09-19
([migration](MIGRATION.md#cleanup-after-the-law-of-the-ray-on-2026-09-19)).


## The rules of the law of events, as pinned until 2026-09-19 (history)

The sections below belong to the modules deleted with the law of events on
2026-09-19 (`test_node_mixing`, `test_node_mixing_numbers`,
`test_event_transit`, `test_periodic_axis`, `test_event_suspension`,
`test_phaseless_family`, `test_release_costs_by_phase_rate`,
`test_event_clock`, `test_detector_sensitivity`, `test_phase_window`,
`test_one_reading_set`, `test_integer_bounds_of_measured_and_emission`,
`test_border_and_clock_corrections`, `test_event_worlds`). Their headings
are kept for the links of the dated records; their pins are the law of
events' and are not the engine's ([migration](MIGRATION.md#the-law-of-the-ray-on-2026-09-19-rays-v1)).

## The Node's computation of the sides

`tests/test_node_mixing.py` isolates the Node's computation with one number
present (node-mixing-v3, the control of one number; Highlights 5.4, point 24
read under the law of events, the model owner, 2026-09-19) on one Node of the
engine's transit (`Transit` of shape (1, 1, 1), one number, N = 8) through the
kernels of `event_universe/events/mixing.py`: the events that arrived on each
heading are one amplitude, sqrt(amount) in 32nds at their phase; the leaving
amplitude of a heading is the coherent sum less three times the arrival that
came in through its Port; the total is shared by the squared leaving
amplitudes in whole units, the floors and the units left to the largest
remainders (ties in the tick's Port order); a group with no whole for any side
goes whole to the heading nearest the momentum it carries; nothing parks, the
Node keeps nothing. With one number the sum over the numbers is that number's
own, so these integers are those of node-mixing-v2 unchanged. Written down
before the first run:

| Case | Arrivals (Port, amount, phase, momentum) | Departures per Port [+X, -X, +Y, -Y, +Z, -Z] | Phases and momenta |
| --- | --- | --- | --- |
| (a) a lone arrival | +X 9 at 0 | 1, 4, 1, 1, 1, 1 | 0, 4, 0, 0, 0, 0 |
| (b) two equal, in phase | +X 9 at 0; -X 9 at 0 | 1, 1, 4, 4, 4, 4 | 4, 4, 0, 0, 0, 0 |
| (c) two equal, in antiphase | +X 9 at 0; -X 9 at 4 | 9, 9, 0, 0, 0, 0 | 0, 4, 0, 0, 0, 0 |
| (d) two on one heading | +X 9 at 0 and 9 at 2 (one amplitude, 18 at step 1) | 2, 8, 2, 2, 2, 2 | 1, 5, 1, 1, 1, 1 |
| (e) unequal, carrying | +X 24 at 0 carrying (24, 0, 0); -X 8 at 2 carrying (-8, 0, 0) | all 32 placed, each heading within one unit of its share 6.22, 11.56 and 3.56 (four times) | 7, 4, 1, 1, 1, 1; the momentum (16, 0, 0) shared by the units, exact in total, each heading's within a unit of its share |
| (f) a single unit | +X 1 at 5 carrying (1, 0, 0); +X 1 at 5 carrying nothing; +X 2 at 0 carrying nothing | 1, 0, 0, 0, 0, 0; 0, 1, 0, 0, 0, 0; 0, 2, 0, 0, 0, 0 | phase 5 kept and (1, 0, 0) on +X; phase 1 on -X |
| (g) the momentum carried | +X 9 at 0 carrying (9, 0, 0) | 1, 4, 1, 1, 1, 1 | the x momentum 1, 4, 1, 1, 1, 1, the sum (9, 0, 0) |

(h) After every cycle the arrivals are empty, the counts zero and the
departures sum to what arrived.

## The coherent sum over the numbers

`tests/test_node_mixing_numbers.py` isolates the rule of node-mixing-v3 (the
model owner, 2026-09-19: the Node reads what is present; the number is a
label for the detector, not a kind) on one Node of the engine's transit
(`Transit` of shape (1, 1, 1), the numbers 1 and 2, N = 8, the tick 0 unless
stated): the amplitude vectors of every number are summed per Port before
the coherent sum; the leaving amplitude of each side is the common sum less
three times what came in through its Port over all numbers; the weights per
side are common to every number at the Node; each number places its own
units by the common weights (the largest remainder, ties in the tick's Port
order, per number), a number with no whole for any side going whole to its
own momentum's heading; the leaving phase of a side is the common leaving
amplitude's phase for every number; every unit keeps its number. With
a = 32 sqrt 9 = 96, the amplitude of 9 units in 32nds, written down before
the first run:

| Case | Arrivals (number: Port, amount, phase, momentum) | Common sum and leaving amplitudes | Departures per number [+X, -X, +Y, -Y, +Z, -Z] | Phases |
| --- | --- | --- | --- | --- |
| (a) two numbers in phase | 1: +X 9 at 0; 2: -X 9 at 0 | 2a; -a on each x side, 2a on each transverse side; the weights 1 : 1 : 4 : 4 : 4 : 4 of 18, each number's 9 units 1/2, 1/2, 2, 2, 2, 2 | 1, 0, 2, 2, 2, 2 for each number (the unit left to the tie of +X and -X goes to +X at tick 0); at tick 1, 0, 1, 2, 2, 2, 2 for each | 4 on +X, 0 across (at tick 1, 4 on -X) |
| (b) two numbers in antiphase | 1: +X 9 at 0; 2: -X 9 at 4 | 0; 3a on +X, -3a on -X, 0 on the transverse sides; the weights 1 : 1, each number's 9 units 4.5 each way | 5, 4, 0, 0, 0, 0 for each number (the tie to +X at tick 0); at tick 1, 4, 5, 0, 0, 0, 0 for each; nothing sideways | 0 on +X, 4 on -X |
| (c) a number with no whole | 1: +X 9 at 0 carrying (9, 0, 0); 2: -X 1 at 0 carrying (-1, 0, 0) | 128 in 32nds; 32 on +X, -160 on -X, 128 across; the weights 1024 : 25600 : 16384 (four times) of 92160, number 1's 9 units 0.1, 2.5, 1.6, 1.6, 1.6, 1.6 | number 1: 0, 2, 2, 2, 2, 1 (the three left to the transverse tie at 0.6, +Y, -Y, +Z at tick 0), its momentum 0, 2, 2, 2, 2, 1 on x; number 2: 0, 1, 0, 0, 0, 0, whole on -X by its momentum, carrying (-1, 0, 0) | 4 on -X for both, 0 elsewhere |
| (d) a number alone | +X 9 at 0 for either number | as `test_node_mixing` (a) | 1, 4, 1, 1, 1, 1; the other number nothing | 0, 4, 0, 0, 0, 0 |

(e) After every cycle the arrivals are empty, the counts zero and every
number's departures sum to what arrived of it.

## An event in transit

`tests/test_event_transit.py` isolates the motion of an event in transit
(Highlights 5.4, the law of events): a single quantum goes whole in one
direction, by its momentum, and does not turn. Written down first:

| Case | Input | Expected |
| --- | --- | --- |
| (a) a single quantum | a bar of 7 x 3 x 3, K 16, no release; one unit of a paid family with quantum 3 in transit at x = 1 on +X at phase 5 | at intervals 1 to 6 the only departure is at x = 1 to 6 on +X, amount 1, phase 5, momentum (3, 0, 0); at interval 7 it escapes with (3, 0, 0) |
| (b) a part turned back | 9 units at x = 3 on +X carrying (9, 0, 0) at quantum 3; then 2 units alone carrying (6, 0, 0) | interval 1: 4 back on -X with (12, 0, 0); interval 2 at x = 2: 2 back toward +X (one by the share, one by the largest remainder), 2 transverse, none on -X, nothing kept; the 2 units go whole to +X with (6, 0, 0) |
| (c) a lone free unit | a measured event of content 1 at the centre of 7^3 releasing at rate 1 per Port | interval 1: one unit on each of the six Ports; interval 3: the first six are at distance two, one each way, created outward, the books closed |

## A periodic axis

`tests/test_periodic_axis.py` isolates the declared exception to the open
board (the model owner, 2026-09-19: an axis may be declared periodic as a run
parameter of the world file, `boundary` `{"z": "periodic"}`; open stays the
default and "closed" and every other word stay refused): on a periodic axis
the departures that would leave the board through one face are created at
the first Node of the opposite face (`Transit.walk`), nothing escapes on that
axis, the momentum they carry stays on the board, and with an extent of 1 the
two departures on that axis return to the same Node in the next interval as
its arrivals through those Ports (a four-Port node with a one-interval stub).
One rule for the board (the model owner, 2026-09-19): a measured event's step
by its momentum (`_move`, step 6) wraps on a periodic axis as the departures
do, escapes through an open face as before, and with an extent of 1 lands on
its own Node, no move; `steps` counts every step made off the clock,
wherever it lands (a step onto a measured event is refused since
2026-09-19, [the corrections](#the-border-and-the-clocks-count)). Bars of
K 16, N 64, `release` [0, 1], `suspension`
0; in (a) to (c) one paid family `light` (quantum 1), one measured event of
it held in place off the units' path, every unit number 1; in (d) one free
family `m` and one measured event of it that steps. Written down first:

| Case | Input | Expected |
| --- | --- | --- |
| (a) the stub of extent 1 | a bar of 5 x 1 x 1 with `{"z": "periodic"}`; one unit in transit at (2, 0, 0) on +Z at phase 5, momentum (0, 0, 1); six intervals | after interval 1 the unit is a departure at (2, 0, 0) on +Z, and the next walk creates it at the same Node as its arrival in the +Z slot, phase 5 and momentum (0, 0, 1) unchanged, nothing else in the slots, nothing in flight, escaped 0; after each of intervals 1 to 6 the only departure is at (2, 0, 0) on +Z, amount 1, phase 5, momentum (0, 0, 1), escaped 0 with momentum (0, 0, 0), the books balanced, the momentum in flight (0, 0, 1); the edge case, the same world with `"boundary": "open"`: after interval 1 the same departure, after interval 2 nothing in flight, escaped 1 with momentum (0, 0, 1), the books balanced |
| (b) the wrap and the open faces | a bar of 1 x 1 x 4 with `{"z": "periodic"}`; units at z = 3 on +Z (phase 5), at z = 0 on -Z (phase 6) and at z = 2 on +X (phase 7) | after interval 1 the departures (0, 0, 0) -Z, (0, 0, 2) +X, (0, 0, 3) +Z, escaped 0; after interval 2 the departures (0, 0, 0) +Z with (0, 0, 1) at phase 5 and (0, 0, 3) -Z with (0, 0, -1) at phase 6, escaped 1 with momentum (1, 0, 0), 2 in flight of the initial 3, the momentum in flight (0, 0, 0), the books balanced |
| (c) the refusals and the record | `"closed"`, `{"z": "closed"}`, `{"w": "periodic"}`, `{"z": 1}`, `"periodic"`; `{"z": "periodic"}`; no key; the bar of (a) run 3 intervals through `execute_event_run` | each of the five refused by `parse_event_world` naming the closed board and by `validate_configuration` (valid false, code `validation`); `periodic` (False, False, True), `boundary` `{"z": "periodic"}`, the preflight's summary `{"x": "open", "y": "open", "z": "periodic"}`; without the key `"open"` and (False, False, False); `run.json` with `boundary` `{"z": "periodic"}`, 3 completed ticks, conserved, escaped `[{"family": "light", "amount": 0, "momentum": [0, 0, 0]}]`, `state.json` with the same boundary at tick 3 |
| (d) a measured event's step wraps | a bar of 1 x 1 x 4 with `{"z": "periodic"}`; a measured event of `m`, content 16, momentum (0, 0, 16), at z = 3 (one step per (M + p) / p = 2 self-creations, as `test_event_clock` (d) derives); six intervals; the same bar with `"boundary": "open"`; a bar of 3 x 1 x 1 with `{"z": "periodic"}` (extent 1) and the same measured event at (1, 0, 0) | after intervals 1 to 6 at z = 3, 0, 0, 1, 1, 2, `steps` 1, 2, 3 after intervals 2, 4, 6, the momentum (0, 0, 16) untouched and (0, 0, 16) on the measured events, escaped 0 with momentum (0, 0, 0), the books balanced at every interval; the open bar: at z = 3 after interval 1, escaped after interval 2 (the measured line's escaped 16, the momentum escaped (0, 0, 16), no measured event left, the books balanced); the extent of 1: at (1, 0, 0) through six intervals, the one measured event still (not escaped), content 16, momentum (0, 0, 16), `steps` 3 (the steps made off the clock, each landing on its own Node), the books balanced |

## The suspension

`tests/test_event_suspension.py` isolates the suspension (the model owner,
2026-09-19: "The event carries it; note that the next event is delayed"; the
same day, the suspension reads presence, of everything, with one fractional
width): a reader derives its suspension from the presence at its Node,
everything present this interval over every family and every number but
its own (the arrivals and, since the one reading set of 2026-09-19, the
content of a measured event there), times the world's `suspension` `[n, d]`, the whole part
(`presence x n // d`; no amplitude, no square root); the event carries the
count and counts down on itself, what arrives behind it waits with it, and
a measured event reads the presence k after its self-creation and owes the
count read off its clock, `by_clock(age, k x n, d)` (since 2026-09-19, the
clock's count read off the clock; until then `k x n // d` whole), paid
before its next one, so a steady presence k slows its clock to one
self-creation per 1 + k n / d intervals on average and never stops it ("a
measured event that reads a large size releases and turns slower"); the
pins below read on age 0 or exact multiples (16 x 1 // 4, 17 x 1 // 4,
17 x 1 // 16), where the two rules agree, and are unchanged by it
([the corrections](#the-border-and-the-clocks-count) pin the fractional
case). K 2^20
so that no phase moves; `suspension` [1, 4], so that 16 units read as
16 x 1 // 4 = 4 and the integers of (a) to (c) are those pinned when the
read was 4 whole units of amplitude (32 sqrt 16 = 128 in 32nds). Written
down first ((b) re-pinned and (c) added on 2026-09-19, when the first
`events-v1` was found to read before the self-creation and to freeze the
clock in a steady field; (a) to (c) re-pinned for the presence and (d), (e)
added the same day):

| Case | Input | Expected |
| --- | --- | --- |
| (a) an event in transit | a bar of 9 x 3 x 3, `suspension` [1, 4]; at x = 4 a unit of light and 16 units of a free family both in transit on +X; a second unit of light at x = 3 on +X | the light at x = 4 reads the presence 16 and carries 16 x 1 // 4 = 4: held for intervals 1 to 4, its count after each interval 3, 2, 1, 0; the second unit arrives in interval 2 and waits with it; in interval 5 the two leave together on +X, amount 2, nothing left in the arrivals |
| (b) a measured event | a measured event of light (content 1, measuring the free family) at x = 4 where the 16 units arrive in interval 1 | interval 1: nothing owed, a self-creation (age 1), then the read of the presence 16, 16 x 1 // 4 = 4 owed; intervals 2 to 5 pay them (3, 2, 1, 0 left), no self-creation; interval 6 a self-creation (age 2) reading an empty Node; its age after intervals 1 to 6: 1, 1, 1, 1, 1, 2; intervals waited 4, nothing owed, phase 0; age + waited = 6 |
| (c) a steady field | a bar of 2 x 1 x 1, `suspension` [1, 4], `release` [1, 128]; a content of 2048 of the free family at the corner x = 0 (five of its six exits off the open board), a measured event of light (content 1, measuring the free family) at x = 1; 30 intervals | the source is created again every interval (age 30; nothing of another number reaches it) and 16 units reach the probe every interval from the second on (464 taken after 30; since 2026-09-19 a free family's units carry no content, so the probe's content stays [0, 1] where it read [464, 1] before), the presence 16, k = 16 x 1 // 4 = 4; the probe's age after intervals 1 to 7: 1, 2, 2, 2, 2, 2, 3 (a self-creation in interval 2 owing 4, paid in 3 to 6, the next in 7), then once every 5 intervals (12, 17, 22, 27): after 10, 20 and 30 the ages 3, 5, 7, waited 23, 1 owed; age + waited = the interval at every interval; the age after 30 exceeds the age after 10 (slowed by 1 / 5, not frozen) |
| (d) light on light | the bar with two measured events of light (numbers 1 and 2); at x = 4 in transit on +X 16 units of light of number 1 and one unit of light of number 2; `suspension` [1, 4], then [1, 4096] | at [1, 4] the unit reads the crowd's 16 (another number of the same family) and carries 16 x 1 // 4 = 4: its count after intervals 1 to 5 is 3, 2, 1, 0, 0, no departure of it before interval 5 and one unit on +X after it; the crowd reads 1, 1 x 1 // 4 = 0, and leaves whole in interval 1 (16 departures); at [1, 4096] the unit reads 16 x 1 // 4096 = 0, its counts 0, 0, 0, 0, 0, and it leaves on +X in interval 1 with the crowd |
| (e) one presence, two readers | a measured event of light (content 1, number 2, measuring the free family and passing light) at x = 4; 16 units of the free family (number 1) and one unit of light of a third measured event (number 3) in transit there on +X; one interval at `suspension` [1, 4], then at [1, 16] | the unit reads every number but its own, 16 + 1 = 17 (the 16 units and the measured event's content, here; until the one reading set of 2026-09-19 it read 16, the content unread) and carries 17 x 1 // 4 = 4 (3 after interval 1 pays one); the measured event, after its self-creation (age 1), reads every number but its own, 16 + 1 = 17, and owes 17 x 1 // 4 = 4: the same count from the same presence; at [1, 16] the unit's count 1 (0 after the payment) and the measured event's 1; the counts are those pinned before (16 // 4 = 17 // 4 and 16 // 16 = 17 // 16) |

## A family without a phase circle

`tests/test_phaseless_family.py` isolates a family declared without a phase
circle (`"phase": false`; the model owner, 2026-09-19, the field of matter
without phase) and the push as the net flow (the same day): the one kernel
of `event_universe/events/mixing.py` (`mix_arrivals` with the weights of
`diagonal_weights`, 32^2 x (the number's amount over the six Ports + 3 x
its amount through the side's own Port), the diagonal of the coherent sum)
on one Node of the engine's transit (`Transit` of shape (1, 1, 1), one
number, N = 8, tick 1, `phased=False`), and the engine on a bar of 9 x 3 x 3
(K 2^20, `release` [0, 1], `suspension` 0, one free family `m` without a
phase, a source of content 16 at x = 0 as number 1 and a reader of content
4 at x = 4 as number 2). Derived by hand first; the integers that moved on
2026-09-19 when the per-Port scatter (`scatter_arrivals`) was folded into
the one kernel are given with the old value in brackets (the placement and
the momentum fall once per group where they fell once per Port; the shares
agree in the mean exactly):

| Case | Input | Expected |
| --- | --- | --- |
| (a) a lone arrival | 9 on +X carrying (9, 0, 0) | the weights 9 x 1024 x [1, 4, 1, 1, 1, 1]: 4 back on -X and 1 to each other side, [1, 4, 1, 1, 1, 1]; every phase 0; the x momentum 1, 4, 1, 1, 1, 1 with the units, the sum (9, 0, 0); nothing kept |
| (b) two opposite arrivals | 9 on +X carrying (9, 0, 0) and 9 on -X carrying (-9, 0, 0); the edge: 2 on +X carrying (2, 0, 0) with the 9 on -X | the weights 1024 x [45, 45, 18, 18, 18, 18], 18 units as w / 9 exactly, [5, 5, 2, 2, 2, 2], no cancellation (the coherent rule in antiphase would leave 9 and 9 along x, `test_node_mixing` (c)); every phase 0; the group's momentum the net (0, 0, 0), every label 0, 0, 0, 0, 0, 0 (old -3, 3, 0, 0, 0, 0, each Port's own), the sum (0, 0, 0); the edge: the weights 1024 x [38, 17, 11, 11, 11, 11], the floors [4, 1, 1, 1, 1, 1] with the remainders [22, 88, 22, 22, 22, 22], the two left to -X and to the first tied 22 from tick 1, +Y: [4, 2, 2, 1, 1, 1] (old [6, 1, 1, 1, 1, 1], the 2 whole on +X and the 9 mirrored); the momentum (-7, 0, 0) over [4, 2, 2, 1, 1, 1]: the floors [2, 1, 1, 0, 0, 0] with the remainders [6, 3, 3, 7, 7, 7], the three left to the 7s, -2, -1, -1, -1, -1, -1 (unchanged), the sum (-7, 0, 0) |
| (c) the push reads the flow | at the reader's Node 9 units of number 1 on +X travel and 9 on -X travel, the labels rewritten to (9, 0, 0) and (-3, 0, 0), one interval; then a lone 9 on +X travel | the flow (0, 0, 0): the push (0, 0, 0), the reader's momentum (0, 0, 0), 18 read, its phase 0 and no phase step, while the labels sum to (6, 0, 0); the departures [5, 5, 2, 2, 2, 2]; the momentum book: in transit (6, 0, 0) (the labels apportioned exactly), on the measured events (0, 0, 0); the lone 9: the flow (9, 0, 0), the push -4 x (9, 0, 0) = (-36, 0, 0), the reader's momentum (-36, 0, 0) |
| (d) the identity of the weights | 7 on +X, 5 on +Y and 3 on -Z (15 present); the bundle three times over (21, 15, 9); the same 15 with a second number's 1000 on -X at the Node; a lone 9 on +X of a family with a phase circle | the weights 1024 x [15, 36, 15, 30, 24, 15] = 32^2 x (15 + 3 x the amount through the side's own Port) exactly; 45 units placed as w / 3, [5, 12, 5, 10, 8, 5], every phase 0; the second number changes nothing of the first's weights and weighs its own 1000 x 1024 x [4, 1, 1, 1, 1, 1], leaving [445, 111, 111, 111, 111, 111]; the coherent weights of the lone 9 are 256^2 x its diagonal ones, 1024 x [9, 36, 9, 9, 9, 9] (no cross term exists for one arrival) |

## A release costs the emitter by its phase rate

`tests/test_release_costs_by_phase_rate.py` isolates the rule of 2026-09-19
(the model owner: "I approve the proposal"; [the engine](ENGINE.md#a-release-costs-the-emitter-by-its-phase-rate)):
at a self-creation whose turn is s = `by_clock(age, content, K)` phase steps,
each unit a lamp releases costs it `quantum` x s content, carries that
content and the momentum `quantum` x s along its heading, and gives
`quantum` x s content to the measured event that measures it (E = h f); a
turn of 0 releases nothing; a free family's release costs nothing and its
units carry no content; the content carried goes with the units at every
Node exactly and the books carry a content line. Bars, `suspension` 0,
every measured event `fixed`. Written down first:

| Case | Input | Expected |
| --- | --- | --- |
| (a) two lamps, s = 4 and s = 8 | a bar of 7 x 1 x 1, K 4096, N 64, `light` (paid, quantum 1) and `counter` (paid); lamp A at x = 0 with content 4 K + 32 = 16416 releasing one unit per self-creation on +X, lamp B at x = 6 with content 8 K + 64 = 32832 releasing one on -X (each content keeps (age + 1) x (content - s K) below K through the run, so the turns stay 4 and 8), a counter of content 1 at x = 3 measuring `light`, the detector `d` of threshold 1; 8 intervals | A spent 8 x 4 = 32 (content 16384, 32 phase steps, phase 32, momentum (-32, 0, 0)), B spent 8 x 8 = 64 (content 32768, 64 phase steps, phase 0, momentum (64, 0, 0)); the releases of intervals 1 to 5 clicked in intervals 4 to 8 (three Links): 10 clicks, the counter's content 1 + 5 x 4 + 5 x 8 = 61, its momentum (-20, 0, 0), each click record with `content` 4 (number 1) or 8 (number 3); 6 units in transit carrying 36, every slot of A content 4 x amount and momentum (4, 0, 0) per unit, of B 8 x amount and (-8, 0, 0); the content line released 96 = current 36 + absorbed 60, spent 96 = measured 60 + in transit 36, the books balanced at every interval; `apportion_whole`: 7 over [3, 3, 0, 0, 0, 1] from 0 is [3, 3, 0, 0, 0, 1], 5 over [2, 2, 2, 0, 0, 0] from 2 is [2, 1, 2, 0, 0, 0], 0 is zeros |
| (b) the free family costs nothing | a bar of 9 x 3 x 3, `release` [1, 1]; a source of `m` (free, content 16) at x = 0, a reader of `m` (content 4, `read`) at x = 4, 9 units of number 1 arriving at the reader on +X in interval 1; `m` without a phase circle at K 2^20, then with one at K 16 (the source turning one step) | after one interval 96 + 24 = 120 released (the source's and the reader's, both free), nothing spent, the contents 16 and 4, content 0 in transit and a content line of zeros, the reader pushed by the flow -4 x (9, 0, 0) = (-36, 0, 0) and 9 read, the momentum in transit the labels' sum (9, 0, 0); the phased source's phase steps 1 |
| (c) a turn of 0 releases nothing | a bar of 5 x 1 x 1, K 64, N 256; a source lamp S of `light` (content 60 K = 3840, rate [1, 4] on +X) at x = 0; a lamp L (content 4, rate [1, 1] on +X, measuring `light`) at x = 2; 7 intervals | intervals 1 to 5: L's turn 0 ((age + 1) x 4 < 64), L at content 4 with no phase step and nothing of its number in transit, no record; S releases at age 3 (interval 4) one unit costing 60 (content 3780, momentum (-60, 0, 0)) carrying content 60 and momentum (60, 0, 0): after intervals 4 and 5 spent 60, 60 carried, 1 unit in transit; interval 6: the click (content 60, L at 64 = K, push (60, 0, 0)), L's turn by_clock(5, 64, 64) = 1 and one unit released costing 1 with content 1 and momentum (1, 0, 0); interval 7: another (by_clock(6, 63, 64) = 1). After 7: L's content 62, 2 phase steps, momentum (58, 0, 0), one click record with `content` 60; S at age 7 with 60 x 4 + 59 x 3 = 417 phase steps; spent 62, measured 60, 2 carried in transit with the momentum (2, 0, 0), the books balanced at every interval |

## The clock of a measured event

`tests/test_event_clock.py` isolates the clock (the model owner, 2026-09-19:
"every clock tick there is self-creation, that is, no transfer to the next
Port"): the age is the count of self-creations, and every rate is read off it
by whole division (`by_clock(age, n, d)`, the gain of the whole part of
age x n / d at the self-creation from `age` to `age + 1`), no remainder
anywhere. Written down first:

| Case | Input | Expected |
| --- | --- | --- |
| (a) `by_clock` | rate 3 / 10 over ages 0 to 9; rate 7 / 3 over 30 ages | 0, 0, 0, 1, 0, 0, 1, 0, 0, 1; the sum 70 |
| (b) the release and the phase | a measured event of content 3 at `release` [1, 10], K 2^20; then at K 2 | 6 units released after intervals 4, 7 and 10 (18 in all), none after 3; at K 2 the phase steps after intervals 1 to 4 are 1, 3, 4, 6 |
| (c) a lamp | content 100 at rate [1, 3] on six headings, no release; K 82 since 2026-09-19 (a release costs the emitter by its phase rate: the content 100, 94, 88 keeps (age + 1) x (content - K) below K, so the turn is 1 at every self-creation and each unit costs quantum x 1; at the K 2^20 of the other cases the turn is 0 and the lamp releases nothing) | 18 units after 9 intervals (at 3, 6 and 9), the content 82 (the same pin: 100 - 18 x 1), 9 phase steps, 18 content released, each unit in transit carrying content 1, the recoil zero over six headings |
| (d) the step | content 16 with momentum 16 on +x, 6 intervals; momentum 1, 16 then 17 intervals | three steps (one per two self-creations, 16 / 32); no step after 16, one after 17 (1 / 17); the momentum untouched |

## A detector's sensitivity

`tests/test_detector_sensitivity.py` isolates a detector's sensitivity
(Highlights 5.4, the model owner, 2026-09-19: "There are detectors by
sensitivity"; "every detector must state what its sensitivity is"): a
detector's threshold, the smallest amount of a family it measures at a Node
in one interval (since the one reading set of 2026-09-19 summed over every
number but the Node's own; every case below arrives as one number, so the
pins are unchanged), gates every response of its Nodes (`read`, `measure`,
`rerelease`), a receiver's and a re-emitter's alike, and a smaller bundle
passes with no push and mixes on; a release reads no threshold. A bar of
9 x 3 x 3, K 2^20 so that no phase moves, `suspension` 0, `release` [0, 1],
the families `m` (free) and `light` (paid), the detector `d` on the Node
x = 4, every arrival a bundle of one number seeded at that Node on +X and
met in interval 1. Written down first:

| Case | Input | Expected |
| --- | --- | --- |
| (a) a receiver | a measured event of `m` (content 4) measuring `light`, threshold 3; 2 units of light of another number; then 3 | 2 units pass: no click, no push, the content 4, the 2 leaving whole on +X (the departures at x = 4 after interval 1, at x = 5 after interval 2); 3 units are measured: 3 clicks, `held` [4, 3], the momentum (3, 0, 0), nothing left in transit, the detector's report 3 measured and 3 clicks |
| (b) a re-emitter | the same Node re-releasing `light` at phase 9, threshold 3; 2 units at phase 20; then 3 | 2 units pass as in (a), no re-release recorded; 3 units are taken: re-released 3, no click, the push (3, 0, 0) taken, `home` [0, 3] when the record is written, then created again at the same interval's self-creation on +X as number 1 (the detector's), 3 units at phase 9 with momentum (3, 0, 0), the recoil leaving the momentum (0, 0, 0), released 3 and absorbed 3; after interval 2 the 3 leave x = 5 as number 1 and nothing of number 2 is in transit |
| (c) an emitter inside a detector; a reading | a lamp of `light` (content 24, rate [1, 1]) in a detector with threshold 5, its world at K 24 since 2026-09-19 (the turn is 1 at both self-creations, content 24 then 18, so each unit costs quantum x 1; at K 2^20 the turn is 0 and nothing leaves); a measured event of `m` (content 4) reading `m` with threshold 4, 3 units of another number, then 4 | the lamp releases one unit per heading per interval as before: after intervals 1 and 2 its departures [1, 1, 1, 1, 1, 1] each carrying content 1, its content 18 then 12, spent 6 then 12, the momentum zero, nothing measured; 3 units pass with no push and mix on (3 departures at x = 4, none of the detector's number); 4 units push by -M c = (-16, 0, 0), read 4, and mix on. The seeded units of (a) and (b) carry one phase step of content each, so the receiver's content grows by 3 and the re-released 3 carry content 3 and momentum (3, 0, 0), as before |

## The phase window

`tests/test_phase_window.py` isolates the phase window (Highlights 5.4, the
model owner, 2026-09-19: "Approve the phase window as a declared width of a
detector, and of the emitter too"): one generic key, `phase_window`, a
setting s on the circle of N steps and the half circle centred on it, with
d = (phase - s) mod N, d < N / 4 or d >= 3 N / 4 (exactly N / 2 steps; for
N = 2 the one step d = 0; `engine.in_window`). On a table entry the response
is made, after the threshold, only to a set (every number at the Node but
its own, the one reading set of 2026-09-19; one number in every case below,
so the pins are unchanged) whose phase at the Node
(`Transit.phase_at`) falls in the window, a set outside it passing (no
push, the units mixing on, a `pass` record per number with the phase and the window);
on a lamp a release only at the self-creations whose clock phase falls in
it, the clock and the phase turning either way; every measurement record
carries the phase read. Bars of 1 x 1 in y and z, N 64, `suspension` 0,
`release` [0, 1], the families `light` (paid) and `counter` (paid) in that
order, every measured event `fixed`. Written down first:

| Case | Input | Expected |
| --- | --- | --- |
| (a) the boundary of the window | a bar of 7 x 1 x 1, K 2^20; a source of `light` (content 8, number 1) at x = 0; a counter (content 1, number 2) at x = 6 measuring `light` through the window 20; four units of number 1 in transit on +X, at x = 5 with phase 35 (d = 15), x = 4 with 36 (d = 16), x = 3 with 3 (d = 47), x = 2 with 4 (d = 48), each reaching x = 6 alone in intervals 2 to 5 | d = 15 and d = 48 click (`click` records at ticks 2 and 5 with `phase` 35 and 4, the push (1, 0, 0) and, since 2026-09-19, `content` 1: a seeded unit carries one phase step of content); d = 16 and d = 47 pass (`pass` records at ticks 3 and 4 with the phase and `window` 20, no push), escaping in the next interval's walk; after 5 intervals `events` [2, 0], `held` [2, 1], the momentum (2, 0, 0), 2 escaped, nothing in transit, exactly those four records, the books balanced at every interval; `in_window` at N = 64 admits d in [0, 16) and [48, 64), at N = 2 the step 0, at N = 4 the steps 0 and 3 |
| (b) the complement covers the circle | a bar of 12 x 1 x 1, K 2^14; a lamp of `light` (content K + 2, phase 0, rate [1, 1] on +X only) at x = 0, whose release of age a carries the phase a mod 64 exactly while 2 a (a + 1) < K; counters at x = 10 (window 8) and x = 11 (window 40 = 8 + 32); 64 + 10 intervals (the release of age a, interval a + 1, reaches x = 10 in interval a + 11 and x = 11 in a + 12) | 32 clicks at each counter: x = 10 the phases 0..23 and 56..63 (d in [0, 16) or [48, 64)), x = 11 the phases 24..55, each of the first 64 releases exactly once, the 64 click records' phases 0..63 each once, a click's tick its phase plus 11 (plus 12 at x = 11); 32 `pass` records at x = 10 (the phases 24..55, window 8), none at x = 11; nothing escaped; the lamp at age 74, phase 10, 74 phase steps, content K + 2 - 74, momentum (-74, 0, 0); in the 75th interval the release of age 64 (phase 0 again) clicks at x = 10 |
| (c) a lamp with a window; the refusals | the lamp of (b) with `phase_window` 8; a plain counter (`measure`, no window) at x = 10; 64 intervals, then 10 more | after each interval t of the first 64: age t, phase t mod 64, phase steps t, the departure on +X one unit at phase t - 1 when t - 1 is in the window (the ages 0..23 and 56..63) and none otherwise; after 64: 32 released, content K + 2 - 32, momentum (-32, 0, 0), phase 0; after 74: 32 clicks at the counter, once at each of those phases, and 42 released (the ages 64..73, phases 0..9, released again); refused naming the key: a window of 64 at N = 64, a window on `pass`, an object entry without `rule`, an object entry with an unknown key, a lamp window of -1 |

## One reading set

`tests/test_one_reading_set.py` isolates the model owner's decision of
2026-09-19 (Highlights 5.4, on the mathematician's list: "ONE READING SET FOR
EVERY COUPLING, 'everything present at the Node but the reader's own number,
including here'"): the presence a reader reads, the flow a measured event is
pushed by, the amount a detector's threshold gates and the phase its window
reads are formed over one set, every number at the Node but the reader's
own, and the seventh exit counts in it, the units waiting at a Node (as
arrivals, as before) and the content of the measured event at the Node under
its number (new); a measured event's own content and its own number's units
coming home are never read. K 2^20 so that no phase moves, `release` [0, 1],
the families `m` (free, without a phase circle) and `light` (paid), every
measured event `fixed`. Written down first:

| Case | Input | Expected |
| --- | --- | --- |
| (a) presence: the waiting units and the content here | a bar of 9 x 1 x 1 at `suspension` [1, 4]; lamps of light (content 1) at x = 0, 8, 7 as the numbers 1, 2, 3; at x = 4 64 units of number 1 on +X and 16 of number 2 on -X, at x = 3 one unit of number 3 on +X; two intervals. Then a measured event of `m` (content 2^10, number 1, passing light) at x = 4, a lamp of light (content 1, number 2) at x = 8, one unit of light of number 2 at x = 3 on +X; two intervals | interval 1: number 1 reads 16 and carries 16 x 1 // 4 = 4, number 2 reads 64 and carries 16, the counts at x = 4 after the payment [3, 15, 0]; interval 2: the lone unit of number 3 arrives beside the 80 waiting units and reads them, 80 x 1 // 4 = 20, the counts [2, 14, 19], the arrivals [64, 16, 1] (as before this change). The passing unit reads the measured content, here: 1024 x 1 // 4 = 256, its count 255 after interval 2, the unit held at x = 4 on +X and nothing in flight; the measured event at age 2 owes 0 (it reads the unit, 1 x 1 // 4 = 0; its own content unread), its content [1024, 0]; the books balanced (until this change the unit read 0) |
| (b) the push over the set | 9 x 3 x 3, `suspension` 0, one free family `m`; sources of content 16 at x = 0 (number 1) and x = 8 (number 2), a reader of content 4 at x = 4 (number 3, `read`); at the reader 9 units of number 1 on +X, 9 of number 2 on -X and 5 of number 3 on +X; then the 9 of number 1 alone; then the 9 of number 1 with the 5 of number 3 | -4 x (9, 0, 0) + -4 x (-9, 0, 0) = (0, 0, 0): the push taken and the momentum (0, 0, 0), 18 read, 5 home, the content 4, the 5 created again whole on +X at the same interval's self-creation (age 0 mod 6), the other numbers' departures 18, nothing left in the arrivals; alone: (-36, 0, 0), 9 read; with the own 5: (-36, 0, 0), 9 read, 5 home, the 5 on +X (the own number adds nothing) |
| (c) the threshold and the window read the set | 9 x 3 x 3, `suspension` 0; a receiver of `m` (content 4, number 1) measuring light in the detector `d` of threshold 3, lamps of light (content 4) at x = 0 (number 2) and x = 8 (number 3); 2 units of number 2 on +X and 1 unit of number 3 on -X arriving in interval 1; then the 2 alone; then the receiver measuring light through the window 32 at threshold 1 with the 2 units at phase 0 and the unit of number 3 at phase 32; then that unit alone | the set of 3 clicks: `events` [0, 3], `held` [4, 3] (a seeded unit carries one phase step of content), the push (2, 0, 0) + (-1, 0, 0) = (1, 0, 0) on the momentum and `pushed`, `measure` 3, the detector's report 3 measured and 3 clicks, nothing in transit, two `click` records at tick 1 in rank order, number 2 (amount 2, push (2, 0, 0), content 2) and number 3 (amount 1, push (-1, 0, 0), content 1), each with the set's `phase` 0; the 2 alone pass, no record, leaving whole on +X; the window: the set's phase is that of 45 at step 0 and 32 at step 32 (32nds, isqrt(2 x 1024) = 45), 13 x 256 on the cosine axis, step 0, outside the window 32 (d = 32): two `pass` records (number 2 amount 2, number 3 amount 1, `phase` 0, `window` 32), no click, the 3 units mixing on; the unit of number 3 alone clicks with `phase` 32 (`events` [0, 1], `held` [4, 1]) |
| (d) the own number excluded everywhere | the bar at `suspension` [1, 1], one family `light`; a measured event of light (content 2^10, number 1, passing light) at x = 4, a lamp of light (content 1, number 2) at x = 8; at x = 4 one unit of number 1 on +X and one of number 2 on -X arriving in interval 1. Then the detector of (c) with 2 units of number 2 on +X and 5 units of the receiver's own number 1 on -X | the measured event (age 1) owes 1, the unit of number 2 alone (its content 1024 and its homing unit excluded), `held` [1024], 1 home and created again on +X; the unit of number 2 reads 1024 + 1 = 1025, its count 1024 after the payment, held on -X; the homing unit's count 0. At the detector the set is 2, below 3: no click, `held` [4, 0], no push, 5 home and created again whole on +X carrying their content 5, the 2 mixing on, 7 in flight |

Re-pins: none. `test_event_suspension` (e) reads the presence 17 where it read
16 (the measured event's content counted), the counts 4 and 1 unchanged
(16 // 4 = 17 // 4, 16 // 16 = 17 // 16); `test_detector_sensitivity`,
`test_phase_window` and `test_release_costs_by_phase_rate` arrive as one
number or at threshold 1, where the set's gate is the number's;
`test_event_worlds` has one number per Node. The Bell worlds read unchanged
(326 criteria of `tools/bell_chsh.py`, S = 2, S' = 3/2).

## The integer bounds of the measured line and of the emission

`tests/test_integer_bounds_of_measured_and_emission.py` isolates the bounds
the architect's review of 2026-09-19 found missing (findings F2, F4 and F9;
ARCHITECTURE.md, the local integer operation contract: "check intermediates
before cancellation, scaling or assignment"): a measured event's momentum,
the push taken and its terms, its content and what waits to be created
again are checked against `transit.MOMENTUM_BOUND` (2^62 - 1) before they
are assigned (`engine.bounded`); a free measured event's release per Port
per self-creation, amount x n // d, times 3 must not exceed the mixing's
cell bound 2^30 - 1 (`world.EMISSION_CELL_BOUND`, `EMISSION_MARGIN`),
refused at parsing; and the mixing's refusals name the quantity that
exceeded, not the retired engine. Bars of 2 x 1 x 1 and a 3^3 board,
`suspension` 0, every measured event `fixed`. Written down first:

| Case | Input | Expected |
| --- | --- | --- |
| (a) the momentum after a push | the free family `m`, K 1024, `release` [1, 1]: two measured events of content 64 at x = 0 and x = 1, the second with the momentum -(2^62 - 1) + 4096 on x; two intervals; then the second with -(2^62 - 1) + 4095 | interval 1 releases 64 per Port; interval 2 each reads the other's 64 and is pushed by -M c = 64 x 64 = 4096 toward the other: the second's momentum exactly -(2^62 - 1), the bound, accepted, its push taken (-4096, 0, 0), the first's (4096, 0, 0), the books balanced; one unit nearer: `OverflowError` at interval 2, "the momentum of measured event 2 at [1, 0, 0]" |
| (a) the push itself | `m` without a phase circle, `release` [0, 1]: a reader of content 2^56 - 1 at x = 1, 64 units of number 1 arriving on +X at its Node; then content 2^56 | the push -64 x (2^56 - 1) = -(2^62 - 64) fits: the momentum (-(2^62 - 64), 0, 0), 64 read; at 2^56 the push -2^62 is refused at interval 1, "the push of measured event 2 at [1, 0, 0]" |
| (b) the emission bound at parsing | one free measured event at the centre of 3^3, K 2^40, N 64: 2^36 at `release` [1, 128]; 2^33; the edge 357913941 x 128 + 127; one more; 2^29 at [1, 1]; 2^36 at [0, 1]; a lamp of a paid family of 2^36 at [1, 128] (K 2^34) | 2^36 refused by the parser and the preflight: "measured[0].amount 68719476736 at [1, 1, 1] releases 536870912 units per Port per self-creation at release [1, 128]; 3 x that, 1610612736, exceeds the mixing's cell bound 1073741823"; 2^33 accepted (3 x 2^26 = 201326592); the edge releases 357913941 per Port, 3 x that = 1073741823 = the bound, accepted; one more releases 357913942, refused; 2^29 at [1, 1] refused (536870912 per Port); nothing released ([0, 1]) accepted at any content; the lamp accepted (not a free release) |
| (c) the mixing's refusals | a cell of 2^30 in the arrivals; 9 on +X carrying (100, 0, 0) with a momentum bound of 10; a departure of 2^30 placed; a departure carrying 11 with a bound of 10; six arrivals of 2^34 at phase 0 in the coherent sum | "the amount in a cell exceeds the integer bound of the mixing (1073741823)"; "the momentum carried by a departure exceeds the integer bound of the mixing (10)" (the largest apportioned label, 44, above 10); "the amount placed on a departure exceeds the integer bound of the mixing (1073741823)"; the same momentum refusal; "the coherent sum's component at a Node exceeds the integer bound of the mixing (2147483647 ...)" (an amplitude of 2^22 x 256 = 2^30 per Port, the leaving component 3 x 2^30); none says "disturbance" |

## The border and the clock's count

`tests/test_border_and_clock_corrections.py` isolates the three reversible
corrections of the model owner of 2026-09-19 (Highlights 5.4, "three
reversible corrections that every path shares"; the architect's D2 and D3
of the same day): a measured event's step onto a Node that holds a measured
event is refused, the stepping event staying where it is with its momentum
and the step counted (no merge; until then the two merged into the
resident); an open face is a detector, every escape through it a click on
the face detector named by it, recorded like a detector's click, and the
books' escaped lines the sums of the face clicks (nothing physical changes
at the face); and the count a measured event owes is read off its clock,
`by_clock(age, k x n, d)`, like every other rate (until then `k x n // d`
whole, the smallest slowing 1 / 2 and none below d / n). Bars, N 64, the
families `m` (free) and `light` (paid). Written down first:

| Case | Input | Expected |
| --- | --- | --- |
| (a) no merge | a bar of 3 x 1 x 1, K 16, `release` [0, 1], `suspension` 0; a measured event of `m`, content 16, momentum (16, 0, 0), at x = 0 (one step per two self-creations) and one of content 16 at rest at x = 1; six intervals | the steps of intervals 2, 4 and 6 onto x = 1 refused: after every interval both remain, the first at x = 0 with momentum (16, 0, 0) and `steps` = interval // 2 (3 after six), the second at x = 1 with momentum (0, 0, 0) and `steps` 0, each of content 16, the measured line's current 32 and the momentum on the measured events (16, 0, 0), no record written (no `step`, no `merged`), the books balanced at every interval; until 2026-09-19 one measured event of content 32 at x = 1 after interval 2 |
| (b) an open face is a detector | the bar of `light`, a measured event of it at x = 1; one unit of number 1 in transit at x = 2 on +X at phase 5 (content 1, momentum (1, 0, 0)); two intervals; the same bar with `{"x": "periodic"}`; the bar with a measured event of `m`, content 16, momentum (16, 0, 0), at x = 2 | interval 1 no record, the unit a departure on +X; interval 2 one `click` record on `face:+x` (tick 2, Node (2, 0, 0), `measured` None, `light`, number 1, amount 1, phase 5, momentum (1, 0, 0), content 1), escaped 1 with content 1; the six face detectors in Port order, `face:+x` with 1 Node, threshold 1, `light` measured 1, clicks 1, content 1, measured_content 0, momentum (1, 0, 0), every other entry 0; `detectors()` lists them; the books' escaped lines equal the faces' sums (transit, content, measured, momentum); the periodic bar: no record, escaped 0, the unit a departure at x = 0 on +X after interval 2, four face detectors (no `face:+x`, `face:-x`); the measured event: no record after interval 1, after interval 2 no measured event left and one `click` on `face:+x` (tick 2, Node (2, 0, 0), `measured` 1, `m`, number 1, amount 16, phase 2 (K 16, two turns of one step), momentum (16, 0, 0), content 16, `held` [16, 0], `home` [0, 0], `home_content` [0, 0]), the measured line's escaped 16, the momentum escaped (16, 0, 0), `face:+x` reading measured_content 16 and momentum (16, 0, 0) for `m`, the faces' sums the books' |
| (c) the count read off the clock | a bar of 2 x 1 x 1, K 2^20, `release` [1, 1], `suspension` [1, 4]; a source of `m` of content k at x = 0 (fixed) and a probe of `light` (content 1, fixed, measuring `m`) at x = 1; k = 1 over 20 intervals, then k = 8 over 10 | the source created again every interval (age = interval) and k units reaching the probe every interval from the second on; k = 1: `by_clock(age, 1, 4)` is 1 at the self-creations from the ages 3, 7, 11, 15 and 0 otherwise, the probe's age after intervals 1 to 20 is 1, 2, 3, 4, 4, 5, 6, 7, 8, 8, 9, 10, 11, 12, 12, 13, 14, 15, 16, 16 (16 self-creations in 20 intervals, 4 in 5; until 2026-09-19 1 x 1 // 4 = 0 and the age was 20), waited 4, nothing owed, age + waited = the interval throughout; k = 8: `by_clock(age, 8, 4)` = 2 at every self-creation as 8 x 1 // 4 was, the age after intervals 1 to 10 is 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, waited 6, nothing owed |

Re-pinned the same day for these corrections: `test_event_boundaries`'s
wrapped movement onto a different resident (the refusal in place of the
merge, above) and `test_phase_window` (a), whose two passers escape through
+x in the walks of intervals 4 and 5 and now leave two `click` records on
`face:+x` (phases 36 and 3, momentum (1, 0, 0), content 1) among the four
measurement records, six records in all where there were four.
`test_event_suspension` (b), (c) and (e) read the count on age 0 or on an
exact multiple and are unchanged; the Bell worlds (`suspension` 0, nothing
escaped) are unchanged (326 criteria of `tools/bell_chsh.py`).

## The worlds of the law of events

`tests/test_event_worlds.py` runs the worlds of `examples/events/` as data on
minimal boards (Highlights 5.5, "The engine of the law of events: what the
tests show"), pinned here on 2026-09-19 from the engine's first readings as a
check that it does what the law says and not as a result, and re-pinned the
same day when the free family lost its phase, the suspension read presence
and the push read the flow (the model owner's three decisions,
[migration](MIGRATION.md#the-field-of-matter-without-phase-the-suspension-as-presence-with-a-fractional-width-and-the-push-as-the-net-flow-on-2026-09-19)).
One family `m` (free, charge 0, `"phase": false`: the sides weighed by
the diagonal of the coherent sum, a lone arrival four ninths back, and
nothing turns) whose measured
event of 2^24 at rest releases 1/128 of its content per Port per
self-creation (q = 786 432 units per interval), N 64, K 2^22 (no phase
step: K does not apply to a phase-less family), an open cube, the measured
event held in place (`fixed`). The phase-less field is diffusive, and 300
intervals on 29^3 (or 200 on 25^3, the example world) is not its steady
state: what is pinned is what the engine read, a check and not a result.
The readings of the coherent field before the change, from the same
designs, are given in brackets as (old ...).

- (a) one measured event (29^3, 300 intervals): at every tick the books
  close, the measured line reads current = initial = 2^24 with nothing
  measured, spent or escaped (what comes home is created again and never
  counts as content), the transit line reads released = current + escaped +
  absorbed with initial 0, and the measured events' momentum is zero. Gauss's
  flux through the cube of half-width 4 (`cube_flux`) over ticks 101 to 200
  is 0.74 of the emission, within 0.04 (0.736 measured; old 0.995), and
  over ticks 201 to 300 through the cubes of half-width 4, 8 and 12 it is
  0.86, 0.46 and 0.17, each within 0.05 and falling with the half-width as
  the field fills the board (0.861, 0.463, 0.174 measured; old 0.995,
  0.990, 0.985); the escape per interval is 0.13 of the emission, within
  0.03 (0.131 measured; old 0.983).
- (b) the shell means over ticks 201 to 300 at r = 4, 6, 8, 10 and 12
  (`shell_readings`): the count times r^2 / q reads 2.00, 1.93, 1.63, 1.11,
  0.70, each within 10 % (old 0.157 to 0.172, flat as 1 / r^2); the radial
  flow times 4 pi r^2 / q reads 2.78, 2.38, 2.00, 1.43, 0.99, each within
  10 % (old 0.997 to 1.16; the shell's mean radial arrival counts what
  enters the shell from inside less what enters from outside and is not
  Gauss's flux where the field turns back on itself, `cube_flux` is); the
  size times r / sqrt(q) reads 3.44, 3.38, 3.10, 2.56, 2.03, each within
  10 % (old 0.622 to 0.661, within 5 % of 3 x 0.2143); the log-log slopes
  over the five radii: the count -2.90 +- 0.15 (-2.898; old -1.99), the
  radial flow -2.90 +- 0.15 (-2.898; old -2.11), the size -1.46 +- 0.15
  (-1.455; old -0.95). The runtime of the one kernel on 29^3 is about
  0.07 s per interval for the phase-less family (the per-Port scatter it
  replaced on 2026-09-19 took 0.29 s, its six apportionments per Node; the
  coherent rule 0.11 s), a host cost.
- (c) two measured events (21^3, d = 8 on the x axis, no suspension, 200
  intervals, the pushes over ticks 101 to 200): the first (at the lower x)
  pushed toward +x and the second toward -x, each by its content times the
  net flow of the other's field at its Node; the axial pushes equal within
  0.5 % (0.02 % measured, 2 376 912 076 800 against -2 376 509 423 616: the
  flow of a diffusive field is symmetric where the momentum labels were
  not; old 2.5 to 5 %; with the scatter folded into the one kernel the same
  day 2 376 576 532 480 against -2 376 375 205 888, 0.01 %, a change of
  0.014 % in the push, the rounding per group), the transverse parts below
  0.1 % of the axial (old below 0.3 %); the measured events' momentum is
  the sum of the pushes at every tick; the axial push against
  M_B rho M_A / (4 pi d^2) with rho = 6/128 between 1.3 and 1.6 (1.449
  measured, 1.4486 with the one kernel; old 0.615); the product law: both
  contents doubled with K doubled pushed four times as much within 2 %
  (3.9993 measured, 3.99996 with the one kernel; old 4.22). The one kernel
  is the diagonal per number: the diagonal over all numbers present would
  let the reader's own dense field steer the other number's labels near
  it, and read 5.96 against the law here (10 times the scatter's push at
  60 intervals), the sides' total the same. Node-mixing-v3 (the coherent sum over
  all numbers present, the same day) does not act on this world: with
  `m` phase-less its units never enter `mix_arrivals`, so the pins are
  the field of matter's.
- (d) the two-slit detector (23 x 41 x 9, 200 intervals): a lamp of light
  (paid, 2^36 units, 2^22 per self-creation on every heading, K 2^34) at
  x = 2; a wall at x = 8 of measured events of the paid family `wall`
  (content 1, measuring light) with two openings of 3 x 3 Nodes 14 apart; a
  screen at x = 17 of the same, declared as the detector `screen`, threshold
  1. The detector's clicks by y, summed over z and smoothed over three, are
  symmetric about the axis (within 5 % of the axis value plus one); with two
  openings the lowest smoothed count 2 to 5 from the axis is exceeded by the
  highest 6 to 11 from it by at least 10 %; with one opening on the axis it
  is not. The fringes come from the lamp's clock stamping the release phases;
  an event in transit does not turn. The detector's report names `screen`
  and counts the clicks the Nodes counted. Since 2026-09-19 a release costs
  the emitter by its phase rate: the lamp's turn is 4 steps at the start
  (2^36 over K 2^34) and falls as it spends (toward 3 and below during the
  run), so the screen's content grows by more than 3 and at most 4 times
  its clicks (each click one unit whatever it carries; the counts
  unchanged).
- (e) the refusals, naming the law: `contents`, `initial_shadows`,
  `wait_per_quantum`, `schema_version` and `dense_field` (the earlier
  engines' keys), `phase_turn` as an unknown family key, a closed board, a
  world without `"law": "events"`, an unknown key, a content at or past
  K x N / 2 of a family with a phase (the same content of the phase-less
  `m` parses: K does not apply), a lamp on a free family, two measured
  events at one Node, a table rule outside `read` | `measure` | `rerelease`
  | `pass`, an N that is not a power of two, a detector on a Node without a
  measured event, a Node in two detectors, a quantum on a free family, a
  `suspension` denominator of 0, a family `phase` that is not true or false,
  a `phase_window` on a table entry for the phase-less family, a `phase` of
  5 on a measured event of it, a `phase_window` on a lamp of a phase-less
  paid family; the parsed world of (a) has one owner of `m`, the suspension
  (1, 1) (an integer 1 read as [1, 1]; [1, 4] read as (1, 4); [0, 4] as
  (0, 1)) and the release 1/128, and a declared detector with threshold 3.
  The runner runs a 4-interval world of (a) into `run.json` (`law`
  "events-v1", completed, four ticks, four books, conserved, the measured
  events and the detectors (none declared: the six face detectors of the
  open board, `face:+x` ... `face:-z`, since 2026-09-19), `suspension`
  [1, 1], the family's `phase`
  false), `state.json` (the law,
  tick 4, the measured events, Nodes with events) and `events.jsonl`, keeps
  the input as read, and refuses a negative tick count and a used output
  directory.
