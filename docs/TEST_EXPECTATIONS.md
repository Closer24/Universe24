# Test inputs and expected results

Since 2026-09-17, by the model owner's decision in
[Highlights 5.5](HIGHLIGHTS.md#55-acceptance-tests-and-open-decisions), a test
exercises one generic rule in isolation on a minimal GameBoard and nothing else: one
test module per rule, one per feature of the ray-event model, with the expected
integers written down here before the first run. No test pins the numbers of an
example world, compares two worlds or reproduces a known experiment; those are
research runs, made once and recorded with a fingerprint and a date in
[validation evidence](VALIDATION.md), never repeated as tests. Entries recorded
before that date describe the suite as it was and are brought under the rule
when their tests change.

## Suite inventory of 2026-09-19: one engine, the Beam Law

Decision of the model owner, 2026-09-19 ([Highlights 5.4](HIGHLIGHTS.md#54-the-detector),
"DECIDED: the law of the ray"; [the Beam Law](BEAM_LAW.md)): one engine,
`beam-v1`, the law of events of the same day deleted with its modules. The
suite keeps one module per generic rule of the engine, on a minimal GameBoard,
and the repository gates. Every rule the Beam Law kept from the law of events
is re-pinned in a new module with the timing of the flight table; the
deleted modules and their rules are named in the
[migration notes](MIGRATION.md#the-law-of-the-ray-on-2026-09-19-rays-v1).
The sections of the deleted modules stay below as history (their headings
kept, their pins the law of events').

| Module | Rule isolated | Re-pins |
| --- | --- | --- |
| `test_nature_beam_readings.py` | The one reading: the moments of order 0, 1 and 2 of the arrivals' direction vectors, taken once; equal to the slot decomposition on the six headings, the moments of the fan on a fan, covariant under the 48 GameBoard symmetries, bounded; the push by the flow of every number but the reader's own; the presence over rest and moving rays; the threshold over the set and the window per ray; the dense readings of the GameBoard decomposed on request for the active Nodes ([below](#the-one-reading)) | `test_one_reading_set` (a to d), `test_phaseless_family` (c), `test_detector_sensitivity` (b), `test_event_suspension` (e) |
| `test_default_table.py` | The table generated from the keys: a free family read, a paid one measured, no window; explicit defaults change nothing; what differs is kept; the kind derived from the quantum and `kind` refused; every example world equal to itself with the defaults written back ([below](#the-table-generated-from-the-keys)) | new |
| `test_nature_beam_flight.py` | The flight: the table at 1 / sqrt 3 with its periods, a lone unit straight and unchanged, the isotropy, the periodic axis and the stub, the open face's click, `adjacent_node` ([below](#the-flight)) | `test_event_transit` (a), `test_periodic_axis` (a to c), `test_event_boundaries` |
| `test_nature_beam_push.py` | The push as one bilinear form over the arriving rays' labels, the emitter's factor on the record, and the one momentum label the click, the re-emission, the home and the transit line move ([below](#the-push-as-one-form)) | new (2026-09-19, the night: the physics-rule review's F1 and the model owner's proposal 2) |
| `test_columns.py` | The one coupling as a signed inner product over the columns: the two built-in columns equal to the landed form integer by integer and refusal by refusal on a grid, at the register's scale and on the replay of the series 7 worlds' `read` records; a third column with the sign minus giving the design's integers and the sign as a key; the refusals and the alignment; the bounds at parsing and at the push; every column floored on its own ([below](#the-columns)) | new (2026-09-20, the model owner's "one mechanism for all the laws on the GameBoard"; the mathematician's verified form) |
| `test_lifetime.py` | The lifetime of a family and the held content: the click on the border `lifetime` booked as a face books an escape (the record 2^26, the ledger lines, the run's record), a ray read at the age L and then booked, the reach of L = 1, 2, 3 on the flight table (the six neighbours, the face diagonals, the cube diagonals and two Links), the inverse refused, the refusals; a measured event holding content of two families (the charges as rational sums, the push, the release of both, the record) and the register's proton ([below](#the-lifetime-and-the-held-content)) | new (2026-09-20, the model owner's "the strong force's range is a lifetime, L"; the physicist's D-1) |
| `test_contact.py` | The contact through the table: the design's pair on the six headings (+128 per interval; under the step drive the labels 128, 256, 0, 0, 128, 0, 128 and the hand-overs 384, -128, 256, -256, 128, ..., the sum 0, no step; at three Links the pair separates at tick 7), the isolated hand-over under `measure`, `rerelease`, `read` and `pass` and the derived default, the apportioning over the occupants of a body's set, the register's proton and neutron over 1000 intervals (998 hand-overs from tick 3, the first 621 934 561 280, the rest 310 967 280 640, the labels 0), the frame's order as a declared tie ([below](#the-contact-through-the-table)) | new (2026-09-20, the model owner on the physicist's design, section 4.4); (a), (d), (e) re-registered on 2026-09-20 under the step drive, the old integers kept as history |
| `test_nucleus_readings.py` | The nucleus readings tool (series I) reads the runner's record: on the design's pair on the six headings, run through the runner, the pushes per body (128, 0, 0) from the `p` rows' -7936 and the `g` rows' +8064, the hand-overs 384 at tick 4, -128 at 5, 256 at 7, -256 at 9 and 128 at 10 under the step drive (256, 128, 640 by p1 alone as the rule was), the border `lifetime` clicking 12 rows per interval from tick 4, no step, the separation 1.00, pinned to the events file | new (2026-09-20, series I); re-registered on 2026-09-20 under the step drive |
| `test_nature_beam_label.py` | The label along the unit vector of the direction at the flight table's scale: the table u_d by the exact integer rule (the pinned vectors, the length within 1.35 % of Q, antisymmetry, equivariance under the 48, no tie, the float agreement over every primitive direction within the bound), every label content x u_d with the recoil, the transit line and the books closing through clicks, a mirror and the open faces, the bound at Q x content x amount ([below](#the-label-along-the-unit-vector)) | new (2026-09-19, the model owner's decision on the physics-rule reviewer's verdict; every momentum pin of the suite re-pinned x 64, listed in its section) |
| `test_nature_beam_collision.py` | The collision table: the classes, the bijection on all 3^8 states, the conservation, the 20 orbits, a head-on pair parking and a crowd passing; no collision at a Node that holds a measured event ([below](#the-collision-table)) | new |
| `test_nature_beam_bijection.py` | The bijection: 50 intervals forward and 50 inverse return the store bit-exact; the merge by one packed key and by the lexsort alike ([below](#the-bijection)) | new |
| `test_nature_beam_detector.py` | The detector's record: two rays in phase and in antiphase (the antiphase pair passing since 2026-09-20); the threshold gating a receiver and a re-emitter over the set (under `wave` on the pointer's square in units of one ray since 2026-09-20, (i)); a release reading no threshold; the record exact and never refused (the pointer in the register up to its bound, the square in Python integers); the detector a set of Nodes with one record (the record, the threshold and the window over the set); the phase returned to the set's events after a click; the `beam` reading (the pairing by opposite phase, the count) ([below](#the-detectors-record)) | `test_detector_sensitivity` (a to c), `test_one_reading_set` (c) |
| `test_nature_beam_reemission.py` | The re-emission on declared directions with the phase and the content kept; the face click; what comes home created again ([below](#the-re-emission)) | `test_border_and_clock_corrections` (b), `test_event_clock` (c) |
| `test_nature_beam_clock.py` | The clock under the Beam Law: `by_clock` and `apportion_whole`; the release, the phase, the lamp's cost and recoil, the step and the refused step, the count off the clock ([below](#the-clock-under-the-beam-law)) | `test_event_clock` (a, b, d), `test_release_costs_by_phase_rate` (a to c), `test_border_and_clock_corrections` (a, c), `test_event_suspension` (b, c) |
| `test_push_width.py` | The width of the push: the world key `width` S in the step rule, one Link per (S x M + p) / p self-creations; S = 1 the rule as it was; the step off the clock with no remainder (since the step drive of 2026-09-20 the same integers, the remainder now the drive on the body's record); the key's default and refusals ([below](#the-width-of-the-push)) | new (2026-09-19, the model owner's D1) |
| `test_step_drive.py` | The step drive (2026-09-20, BEAM_LAW note 17 as amended): the count of Links as the whole part of the distance the momentum has driven, one bounded integer per axis on the body's record: the identity at a constant momentum with `by_clock(n - 1, \|p\|, D)` over 4000 self-creations and twelve momenta; the identity on two axes (the coincident step lost as before); the integrated distance under a halving momentum (38 within 1, 37 to 39, where the rule as it was made 1); never two Links in one interval under a random momentum over 10 000 intervals with the drive in [0, 2 D - 1); the record (`drive`, `axis_steps`, the `step` line) and a declared `drive` refused; the turn by momentum unchanged; the signed drive under a reversal (no Link until the drive cancels and reaches -D) and the bound pair under a suspension holding for 3000 intervals ([below](#the-step-drive)) | new (2026-09-20, series G2's finding, record 107; the owner's decision, record 108); the drive signed the same day (record 126) |
| `test_doppler.py` | The reading's weight at the relative speed (`doppler-v1`, 2026-09-20, BEAM_LAW note 38; the flux at the grain G = 2^12): a fixed body and a free body at rest reading byte-identically with and without the key over 200 intervals (the same records, the same books); the bar of the finding (a fixed source's steady beam, a free body of content 2^20 at an exact speed, the push the weighted flow in label units) reading 200 rows in every case and taking 12800 at rest, 6204 receding at 0.30, 2901 receding at 0.45, 19395 approaching at 0.30, 0 co-moving at c, 3700 outrunning at 0.75 (the map's rates 96.9, 45.3, 303.1, 0, 57.8 rows to the label unit); the bar with rows of 64 running; the third law on two fixed bodies unchanged; the refusals, the weighted flow's R1 and the budget's factor; the grain, the pair on the headings and the fan (0.5938, 0.7771, 0.8666) and the record; the fan over three intervals (5130 of 8640 on the face diagonal at 1/3; 4326, 8504 on (1, 2, 0) and 2828, 8485, 5656 on (1, 3, 2) at the star's speed; the heading 5249 of 12288; the transverse exact) and the fan reader at rest byte-identical; a body on a set reading two groups from the one frame snapshot; a registered G2 star world running 20 intervals under the key ([below](#the-readings-weight-at-the-relative-speed)) | new (2026-09-20, the model owner's record 119; the mathematician's form, record 110, and GRAIN.md after the physics-rule review) |
| `test_nature_beam_age.py` | The age of a ray kept whole and read by a measured event: the age whole through the flight, a collision, a re-emission and a birth; the age moment of the one reading and its symmetries; the clock counting it on an entry that reads `age`; the world key `age_bound`, its default, its refusals and the run-time refusal; the GameBoard unchanged by the whole age ([below](#the-age)) | new (2026-09-20, the model owner's "go for it" on the clock beside a mass) |
| `test_nature_beam_body.py` | A body on a set of Nodes with one record (`span`): a set of one Node bit-identical to the measured event as it was; the reading, the threshold, the clock's count and the push summed over the set; the step of the whole set, the refusal and the click on a face; the releases apportioned over the set with the books balanced; and the turn by momentum (`action`, `phase_by_momentum`): the phase after k Links floor(k x \|p\| x N / h) mod N for three (p, h, N) including a remainder each step, composed over axes, today's phase without `action`; the GameBoard unchanged by the two keys; the refusals and the record ([below](#a-body-on-a-set-and-the-turn-by-momentum)) | new (2026-09-20, the model owner's decision on Bohr, "put it as parameters outside the GameBoard like the age") |
| `test_nature_beam_window.py` | The phase window under the Beam Law: the centred half circle on a table entry and on a lamp, the complement covering the circle, the refusals ([below](#the-phase-window-under-the-beam-law)) | `test_phase_window` (a to c) |
| `test_paid_charge.py` | A paid family's charge per unit of amount (D-1): the books' charge line conserved through the click of a charged paid row, its escape, its home and the escape of the body that holds it; the push untouched (the label alone, with the charge -1 and 0 alike); the refusals and the record ([below](#a-paid-familys-charge)) | new (2026-09-20, the model owner's "go on everything", item (2)) |
| `test_window_width.py` | The width of a window, `phase_width`: the one floor `window_admits` equal to the half circle at the default width on every pair, the admitted fraction w / N against the source's stride (10, 20, 40, 320 of 640; the stride 2's coset), `beam`'s pairing arc, a lamp's width, the refusals ([below](#the-width-of-a-window)) | new (2026-09-20, the model owner's "go on everything", the neutrino first) |
| `test_weak_readings.py` | The weak-force readings tool (series J) reads the runner's record and the flight table: on a short bar run through the runner, the first reader's 3 clicks of 192 arrivals, the far detector's 151, the first-arrival ages 13 and 51; on the toy of the transformation with a shell of 62 readers, the `become` line and the shell's one click ([below](#the-width-of-a-window), [the transformation](#the-transformation)) | new (2026-09-20, series J2; (b) with series J1) |
| `test_become.py` | The transformation `become`, `weak-v1`: the clock trigger at the self-creation whose clock reaches `at`, the products born as a re-release is with the recoil over all of them, the `became` line and the charge line exact; the click trigger within a window and the entry consumed; the crowd slowing the trigger and the gate holding it; the charge line through the click of the product; the refusals and the run refused when the event cannot pay ([below](#the-transformation)) | new (2026-09-20, the model owner's "go on everything", item (1)) |
| `test_w_world.py` | The W world, the exchange at one Link: the W (paid, charge -7344 per unit, lifetime 1) thrown at the neutron's key and measured by the proton one interval later, its content and charge a neutron's; the W into empty space on the border; the click trigger on the proton refused with the design's sketch and balanced with a positive product; the refusals ([below](#the-w-world)) | new (2026-09-20, the model owner's "go on everything", item (3)) |
| `test_nature_beam_window_reads.py` | A table entry's window read from a reading (`phase_window` `{"reads": ..., "offset": ...}`): the centre the setting ray's phase plus the offset, a ray inside clicking with the `window` on its record and a ray outside passing with `window` and `reads`; the edge case of no setting ray (a `pass` naming `window` None) and of an antiphase pair; the parsing and the refusals ([below](#a-window-read-from-a-reading)) | new (2026-09-20, issue #363) |
| `test_bell_choosers.py` | The reader of the Bell run with the choosers on the GameBoard (`tools/bell_choosers.py`) reads the engine on a minimal case run through the runner: the offsets off `FlightTable.manhattan_steps`, one bin at fixed settings with E the triangle exactly, the written windows reading the same and merging, the CHSH sums on synthetic bins ([below](#a-window-read-from-a-reading)) | new (2026-09-20, issue #363) |
| `test_nature_beam_world_parsing.py` | The world file of the Beam Law: the refusals by name, the direction table, the runner's record, the integer bounds of the measured line ([below](#the-world-file-of-the-beam-law)) | `test_event_worlds` (e), `test_integer_bounds_of_measured_and_emission` (a) |
| `test_nature_beam_worlds.py` | The worlds of the Beam Law: the two slits fringing in the record and not in the count, the Bell worlds, one content streaming with the books closed, the example worlds parsing, `two_contents` not refused with its face records exact ([below](#the-worlds-of-the-beam-law)) | `test_event_worlds` (a, d) |
| `test_nature_beam_books.py` | The books as running ledger lines: the transit, content and momentum lines of `books()` equal the recount over the store at every interval of a world that exercises every way a row comes or goes; an empty world ([below](#the-books)) | new (2026-09-19, the optimizations) |
| `test_configuration_validation.py` | The read-only preflight of a world file: the report, the refusals named by the parser, the command line |
| `test_entity_definitions.py`, `test_entity_loading_consumers.py` | The entity definitions loader and its consumers (the placement, the bundles, the refusals at runtime) |
| `test_entity_catalog.py` | The worlds of the entity catalog (`examples/events/catalog/`; the model owner's decision of 2026-09-20): each is the one its generator writes, parses through the canonical loader with `quantum` on every family and `reading` on every detector, runs its 20 to 50 intervals with the books balanced at every interval, and its readings exist (a record per declared detector, a clock's identity age + waited = the intervals on every probe); since 2026-09-20 the catalog against the parser (every key a row names is the parser's) and the register against the catalog (every declared family named); no number of a world pinned ([below](#the-entity-catalog)) |
| `test_json_documents.py` | The strict decoder shared by world files and the workspace's fragments |
| `test_integer_arithmetic.py` | The shared bounded integer primitives |
| `test_retention.py` | Generated-output ownership, lifetime and cleanup |
| `test_check_scope.py` | The affected-check's selection |
| `test_coupling_readings.py`, `test_orbit_readings.py`, `test_heisenberg_readings.py`, `test_hubble_readings.py` | The tools read the engine (the architecture review of 2026-09-20; the experimenter skill): each reading of `tools/coupling_readings.py`, `tools/orbit_readings.py`, `tools/heisenberg_readings.py` and `tools/hubble_readings.py` equals the engine's own function on a minimal GameBoard (the front off `manhattan_steps`, the step rule and the release off `by_clock`, the push off `unit_label`, the fan's labels off `flight_table`, the detector records off `DetectorSet`, the declared charge per unit of content; the Hubble tool's c = 32 / 55 and m(age) off `flight_table`, its `record` lines and click ages off the run of a bar of 61 x 1 x 1, its z within the digital step's grain of 1 + v / c); the expected integers are in each module's docstring |
| `test_hubble_stars_readings.py` | The series G2 tool (`tools/hubble_stars_readings.py`) reads the engine (the experimenter's rule): the shipped worlds of `examples/events/hubble_stars/` equal their generator's and `expectations.json` declares its format; on a bar of 61 x 1 x 1 run through the runner (a star of a paid family holding a mass of 2^22 and shining one unit per self-creation toward a detector of one Node, the speed 1 / 2 Link per self-creation) the tool's `record` lines, click ages, steps (30 in 60 intervals), homes (its outward rows taken home, 64 units each) and final momentum are the engine's, z within the digital step's grain of 1 + v / c, the reading's formula within 2 % and the luminosity within 5 %; the fits read the exact coasting form as q = 0 with H (t_0 + T_0) = 1 to 1e-6 and the exact Einstein-de Sitter form as q = +0.5 to 1e-3; the expected integers are in the module's docstring | new (2026-09-20, series G2) |
| `test_bohr_readings.py` | The series H tool reads the engine (the experimenter's rule, 2026-09-20): the flight time from the centre's plane to a face off `FlightTable.manhattan_steps` (5 Links at the age 8, 6 at 10, 1 at 1), the pointer per turn and the coherence ratio off `nature_beam.coherent_pointer` with the circle's tables ((16384, 0) and (-8192, 0) for two units at phase 0 and one at 32, C = 0.2; 1.8 with the third at 0; the slope of [1, 4, 9] is 2), and `read_run` on a run written by the runner (a proton of `p` at (5, 5, 1) of an 11 x 11 x 3 GameBoard on the four in-plane headings, an electron of `e` of span [1, 1, 3] at (8, 5, 1) with the momentum [0, 320, 0], `pass` for `p`, `action` 65536, 20 intervals: the radius 3, j = 0.05859375, the flights 8, the clicks per face equal to the record's, no read, the steps' phases 5, 5, 5, 6 at the ticks 5, 9, 13, 17, the first -x click at tick 16); the expected integers are in the module's docstring |
| `test_architecture.py`, `test_locality.py` | The dependency direction (`core` imports only `core`, the engine imports no host module, no physical module imports output or storage), the integer audit of `core/`, and LOCALITY-1 documented without an exception |
| `test_meeting.py` | The meeting: the arc permutation of the direction table (a permutation for 1034 targets on K's table, the rest fixed, the chain from +x, the k-fold shift), the phase register (61, 62, 63, 0, 1, 2 with the turn at the fourth; the inverse), the sign of the turn and the `turned` line, the crowd and the record untouched, the bijection with the meeting (50 forward, 50 inverse) and the refusals ([below](#the-meeting)) | new (2026-09-20, the model owner's "DECIDED: the meeting, M-R"; the physicist's and the mathematician's design) |
| `test_amplitude_record.py` | The record on the row (`amplitude-v1`): the world key `amplitude` deleted and refused, the identity `amplitude-v1` on a world with a lamp alone; the four columns `record`, `branch`, `multiplicity` and `birth` at their defaults on every row of no record and the merge's packed key unchanged by them; the merge's normal form, antiphase rows of one record cancelling and every other pair staying ([below](#the-amplitude-law-the-record)) | new (2026-09-20, the model owner's "DECIDED: `amplitude-v1` is built"; the design's sections 1 and 2.3) |
| `test_amplitude_split.py` | The split, the birth of a record and the phase per interval of age: a lamp's birth of one record of k rows with the multiplicity k and the identity number x 2^32 + ordinal; the (20, 21) splitter's rows (41 in phase toward D1, 1 in antiphase toward D2, the multiplicity 1682) and the balanced split's cancel on the GameBoard with the `cancelled` lines; the pair form of `phase_per_link` (40 at [8, 1], 26 at [16, 3], 24 at the integer 8 after 5 intervals; the inverse bit-exact); the refusals ([below](#the-amplitude-law-the-split)) | new (2026-09-20; the design's sections 2.1, 2.3, 3.1 and 3.4; the owner's unifications (1) and (2)) |
| `test_amplitude_layer.py` | The layer: the reading `sum` at the record's scope, the offers, the ladder at completion and the gathers, on series L: the ten Mach-Zehnder and Elitzur-Vaidman worlds click as the design's table over the 64 births (tests 1, 3), the same list twice and the moved rung (8), a split takes no click gate (the review's B1), the two slits at a low rate against the generator's reading of one birth (2: 78 of 80 sets exact, one rung moved by the tables' rounding), the gate set parses without the key (7), the reading tool's replay equals `run.json`'s `world` (10), the pair form bounded at the parse (S1), the cancel booked per content (S3), a lamp short of one quantum per direction refused (S4), the `record` line's scope ([below](#the-amplitude-law-the-layer)) | new (2026-09-20; the design's sections 3, 5 and 7; the decision on the split's gate) |
| `test_amplitude_pair.py` | The pair, the which-path world, no maintenance and GHZ: a lamp's `branches` and `arms` (the birth of four rows on two arms with the labels 0 and 3), the CHSH labels (E x 64 = 44, -44, 44, 44; S = 176/64; the marginals 32/64), the choosers (the 15 setting pairs' E; S = 156/64 on the registered quadruple), the which-path `read` (E = 44, -44, 0, 0; S = 88/64), Bob's counters 116 Links farther (E unchanged), GHZ's allowed triples and products, the refusals ([below](#the-amplitude-law-the-pair)) | new (2026-09-20; the design's section 4 and its `bell.py`) |
| `test_amplitude_gate.py` | The gate between records and the pair at N = 1024 and 4096: the Hadamard and the CNOT on the GameBoard (|00> - |11>), the pair by the gate at the CHSH labels (S = 176/64), CNOT twice the identity, GHZ by one gate of three parties, the register's ceiling (three rotations run, four refused at load), the refusals, S = 2896/1024 with |E - cos| <= 1/N, S = 11584/4096 with the bound failing at the tables' rounding; the review of (v): the gate's copies booked on the live count (every gathered record at live 0), a record with an offer or units elsewhere refused at the gate, the control by its declared arrival direction (the `measured` list reversed gives the same outcomes), the control's refusals ([below](#the-amplitude-law-the-gate)) | new (2026-09-20; the design's section 10 and its `gate.py`; the owner's paper numbers; the review of (v)) |
| `test_amplitude_click.py` | The one click (stage (vii)): a lamp's rate births as many records as it says with the ordinals and the birth phases in order, two multiplicities of one record at one offer take the common denominator or are refused, the columns are written only where a record is, and every gate-set world without a lamp reads as it did before the law at its cap (its pinned digests); step 2: u the record's own field (a narrow window admits every record's row, the K record world's clicks within one rung of its offers); step 3: the push by share (the mass's momentum the sum of the shares, the remainder line, the unkeyed bar as it was) ([below](#the-amplitude-law-the-one-click)) | new (2026-09-20; the design's sections 2.1, 2.5 and 6; the K finding) |
| `test_repository_language.py`, `test_repository_hygiene.py`, `test_repository_navigation.py` | The repository gates: English, one canonical copy, navigable links |

## The one reading

`tests/test_nature_beam_readings.py` (docs/BEAM_LAW.md, section 3 step 2 and section
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
  decomposition of the first NatureBeam worlds exactly (its (p_x + p_y - 2 p_z,
  p_x - p_y) = (-19, -1) being -T_zz and (T_xx - T_yy) / 3); for 64 fixed
  random integer amounts on the seven slots the moments equal that slot
  decomposition through the same relations; on a fan (2 on (1, 1, 0), 3 on
  (2, -1, 0), 1 on (3, 1, 2), 4 on (1, 0, 0), 5 here) the flow is
  (15, 0, 2) and the tensor [[44, -3, 18], [-3, -19, 6], [18, 6, -25]]
  (3 x the second moment [[27, -1, 6], [-1, 6, 2], [6, 2, 4]] less its
  trace 37), traceless; under each of the 48 signed axis permutations R of
  the GameBoard the scalars are fixed, the flow is R x flow and the tensor
  R T R^T, on the fan as on the headings; the shortest reading, one unit on
  one heading e, reads outside 1, here 0, the flow e and the tensor
  3 e e^T - I; the keyed form over Nodes equals the readings Node by Node; a
  reading whose second moment could pass 2^62 - 1 (an amount above
  2^62 / 4096 on (64, 0, 0)) is refused with `OverflowError` before any
  product is formed, and the amount at the bound is accepted.
- (b) the push reads the flow of every number but the reader's own: a free
  reader of content 4 met by 9 rays of number 1 arriving on +X and 9 of
  number 2 arriving on -X is pushed by (0, 0, 0) and reads 18; by the 9 of
  number 1 alone (-2304, 0, 0) (re-pinned from (-36, 0, 0) on 2026-09-19:
  the label of a unit along a heading is 64 e_d, the label along the unit
  vector, [BEAM_LAW note 23](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation));
  with 5 of its own number arriving too the own add nothing (5 home,
  created again at the same interval's self-creation on its first
  declared direction).
- (c) the presence counts every ray at the Node of another number, rest and
  moving alike, and never the own: a measured event at `suspension` [1, 4]
  beside 64 rays of number 2 that arrived and 16 rays of number 3 at rest
  owes `by_clock(0, 80, 4)` = 20 after its first self-creation; with 8 of
  its own number among the arrivals still 20.
- (d) a detector's threshold reads the set of every number but its own and
  the window the set's phase by default (re-pinned on 2026-09-20, `wave`
  the default reading): a receiver at threshold 3 met by 2 rays of number
  2 and 1 of number 3 clicks all three, one ray of number 2 alone passes
  with a `pass` record (`threshold` 3; since 2026-09-20 the threshold
  under `wave` reads the pointer's square, so two rays in phase would
  read 4 and click); at threshold 1 with the window 32, the 2
  units at phase 0 and the 1 at phase 32 point to phase 0, outside the
  window, and all three pass (`pass` 2 at phase 0 and `pass` 3 at phase
  32, both `window` 32; nothing held, no `record` line) [under the
  default `beam` of 2026-09-19 the two at phase 0 passed and the one at
  32 clicked]; the same gate declared as a `beam` detector reads each
  ray's own phase: the two at phase 0 pass and the ray at phase 32 clicks
  (`pass`, `click`, `record` at phase 32).
- (e) the dense readings of the GameBoard are decomposed on request from the
  rows of the walk, for the active Nodes only (added 2026-09-19 with the
  optimizations of BEAM_LAW section 10, note 22): on the open 9 x 3 x 3
  GameBoard with no measured event, 9 units arriving at (4, 1, 1) on +X and 9
  on -X, 3 arriving at (2, 1, 1) on +Y and 2 at rest at (6, 1, 1): after
  one interval the count is 18, 3 and 0 at those Nodes (21 over the
  GameBoard), the flow (0, 0, 0), (0, 192, 0) (3 x 64 on the unit vector of
  +Y; re-pinned from (0, 3, 0) on 2026-09-19) and (0, 0, 0), the presence
  18, 3 and 2 (23 over the GameBoard), the Links crossed per Port (9, 9, 0,
  0, 0, 0) at (4, 1, 1) and (0, 0, 3, 0, 0, 0) at (2, 1, 1) (21 over the
  GameBoard); before the first interval, and on an empty GameBoard, every array
  is zero with its shape.
- (f) a fan's flow reads Q per unit direction-blind (added 2026-09-19 with
  the label along the unit vector): a free reader of content 1 met by 5
  units on (7, 5, 0) (declared one Link before its Node with age 0, so
  they arrive on the first step of their line, +X) and 5 on +X is pushed
  by -(5 x (52, 37, 0) + 5 x (64, 0, 0)) = (-580, -185, 0) and reads 10,
  the dense flow at its Node (580, 185, 0), |5 x (52, 37, 0)|^2 within
  (63 x 5)^2 .. (65 x 5)^2; by the 5 on (7, 5, 0) and 5 on (-7, -5, 0)
  (arriving on -X) the push is (0, 0, 0) exactly (u_{-D} = -u_D) and the
  reading 10.

## The table generated from the keys

`tests/test_default_table.py` (docs/BEAM_LAW.md, section 2 and section 10
note 15; the model owner, 2026-09-19, "I approve 1 and 3": the tables are
generated from the keys and a world declares only what differs, `kind`
derived from `quantum`).

- (a) the default: for the families m (quantum 0) and light (quantum 3)
  `default_table` is (("read", None, "vector"), ("measure", None,
  "scalar")); a measured event without `table` parses to exactly that, and
  so does one that writes the default out as strings, as objects with
  `reads`, as empty objects, or for one family only: the `NatureBeamWorld`s are
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
  the key; a negative quantum is refused; a fractional charge on a paid
  family is refused (since 2026-09-20, D-1: a paid family's charge is
  whole per unit of amount; until then any charge on a paid family was
  refused naming its quantum); a charge on a free family (-3 parsed as the
  pair (-3, 1), [1, 2] as (1, 2); since 2026-09-20 the charge per unit of
  content, no `charge` on the measured event) and a lamp on a paid family
  are accepted, and a lamp on a free family is refused.
- (d) the example worlds: every world of `examples/events/` (the ten Bell
  and twenty-one coupling worlds, the four top-level worlds, the four
  detector worlds through the entity loader) parses equal, field by field,
  to the same document with the generated default written back into every
  measured event's table; no shipped world writes a default entry out.

## The flight

`tests/test_nature_beam_flight.py` (docs/BEAM_LAW.md, section 3): one speed for
every direction, 1 / sqrt 3, on the digital line of the momentum, at most
one Link per interval, the age modulo the direction's period.

- (a) the flight table: for every direction T_d >= S_1 Q and m(tau + 1) -
  m(tau) in {0, 1}; the periods (1, 0, 0) T 110, L 55; (1, 1, 0) T 156,
  L 39; (1, 1, 1) T 192, L 3; (3, 1, 0) T 350, L 175; a rest direction never
  moves; the first arrival of a heading ray at m Links, m = 1..11, in the
  intervals 1, 3, 5, 7, 8, 10, 12, 13, 15, 17, 19.
- (b) the lone unit: every heading and every declared direction of the
  two-slit example, 150 intervals on a periodic 61^3 GameBoard: the ray's
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

`tests/test_nature_beam_collision.py` (docs/BEAM_LAW.md, section 4): eight slots per
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
- (c) on the GameBoard: two rays of amount 1 meeting head-on at the middle Node
  of a 5 x 1 x 1 bar (x and z periodic) become the two rest rays at that
  Node in the interval they meet, and stay; two rays of amount 2 (a crowd)
  pass each other; over the six orientations of a head-on pair on a periodic
  5^3 cube the x pair parks, the y pair turns onto x and the z pair onto y,
  and after the second collision the rest pair leaves on z, the x pair
  parks and the y pair turns onto x: the one cycle of the class, the tie by
  Port order.
- (d) no collision at a Node that holds a measured event (the windowed
  taker declared as a `beam` detector since 2026-09-20, the window then
  reading each ray's own phase; under the default `wave` the pair's
  pointer is zero, has no phase, and both rays pass) (the model owner's
  decision of 2026-09-19 on the physics-rule reviewer's F1(c); BEAM_LAW
  section 3 step 3 and note 18): the head-on pair of (c) (one number,
  amount 1, phases 0 and 32) meeting at the Node of a measured event of `m`
  whose table passes `light` keeps its directions +x and -x (no rest ray),
  dwells the two intervals of its line there and parts at the third (x = 5
  and x = 3 on a 9 x 1 x 1 bar); at a measured event whose table measures
  `light` in the window 32 the ray at phase 32 clicks with its label
  (-64, 0, 0) (re-pinned from (-1, 0, 0) on 2026-09-19, the label along
  the unit vector), the ray at phase 0 passes and goes on to x = 5, the
  transit line is (64, 0, 0) and no ray is stranded at rest; measured +
  transit = (0, 0, 0), the labels' sum before the interval.

## The bijection

`tests/test_nature_beam_bijection.py` (docs/BEAM_LAW.md, section 3): a periodic
8 x 8 x 4 GameBoard (`age_bound` 128 declared, as a GameBoard periodic on every
axis must since 2026-09-20), 300 records of fixed arrays (rays on every heading, both
rest slots and two fan directions, head-on pairs among them, amounts 1 and
2, phases over the circle), 50 forward then 50 inverse intervals with no
measured event: the sorted store equal to the start in every field (the
ages whole, up to 72 at the turning point); the
state at the turning point differs from the start; the collision moved at
least one ray on the way.

The merge (step 6; added 2026-09-19 with the optimizations of BEAM_LAW
section 10, note 22): 82 fixed rows (60 distinct over 200 Nodes, 10
directions, 23 ages, the circle, 3 numbers, 3 contents; 20 of them
repeated; two extremes; since 2026-09-20 the identity is the six fields
node, direction, age, phase, number, content, the columns `charge` and
`mass` being gone) merged by the packed key of the identity fields equal
the Python sort of the identity tuples with the amounts of equal tuples
added, 62 rows, every arrival reset to here; the same rows with every
other content raised by 2^61 (the key does not fit the register,
`merge_key` is None) merged by the lexsort fallback equal their Python
sort likewise; the empty store merges to the empty store.

## The amplitude law: the record

`tests/test_amplitude_record.py` (docs/BEAM_LAW.md note 37; the model
owner, 2026-09-20, Highlights 5.4, "DECIDED: `amplitude-v1` is built"; the
design, docs/designs/amplitude-v1/DESIGN.md, sections 1 and 2.3). A 5 x 5
plane, K 16, N 64, `release` [0, 1], `suspension` 0, a lamp of `light` of
content 16 releasing one row per self-creation on +x and +y at the turn 1
(eight births of two quanta; since the review's S4 a lamp must pay one
quantum per direction at a birth), and a detector of one Node. The
expected integers, written down before the first run:

- (a) the key is deleted (stage (vii) step 4): a world with a lamp is
  recorded and `hypotheses` is ["amplitude-v1"], `run.json` carries no
  `amplitude`; the same world without its lamp is not recorded and
  `hypotheses` is empty; `amplitude` declared true or false is refused
  naming MIGRATION; a lamp with N 2 is refused (a record's circle holds
  the quarter turn), the world without the lamp at N 2 parses; N 4 with a
  lamp of content 1 at [1, 1] is accepted; a lamp's rate [2, 1] parses;
- (b) the columns: after 5 intervals every row of the store carries record
  0, branch 0 and multiplicity 1; `state.json`'s rows carry none of the
  three keys without the world key and all three under it; the packed
  merge key of a store whose three columns are at their defaults equals
  the key packed from the six fields of the law as it was (the three add 0
  bits), so the merge's order is unchanged;
- (c) the normal form (`NatureBeamStore.merge` with N = 64): rows of one
  record and multiplicity equal in every field but a phase difference of
  exactly 32 cancel: 3 at 5 and 2 at 37 leave 1 at 5 (4 units cancelled),
  1 at 9 and 1 at 41 leave nothing (2), 1 at 40 and 2 at 8 leave 1 at 8
  (2, the larger side's phase); rows of no record at 9 and 41 stay two
  rows, as do two rows of one record a quarter turn apart and two of one
  record at one phase with the multiplicities 2 and 4; two of one record
  at one phase merge to amount 2; with the modulus 0 (a store of no
  record) the antiphase pair stays; the units cancelled are returned per (record,
  direction, content per unit), {(7, 2, 1): 4, (8, 2, 1): 2, (9, 2, 1): 2}
  (the review's S3: the content carried is units x content, no division).

## The amplitude law: the split

`tests/test_amplitude_split.py` (docs/BEAM_LAW.md note 37; the design,
sections 2.1, 2.3, 3.1 and 3.4; the owner's unifications (1) and (2)),
on the Mach-Zehnder world of series L built by
`examples/events/amplitude/make_worlds.py` (a 5 x 5 plane, K 2^20, N 64,
the source of content 2^20 releasing one record per self-creation on +x
and +y with the turn 16 on +y, mirrors at (3, 0) and (0, 3), the splitter
at (3, 3) with the inputs +y and +x and the weight rows [b, a], [a, b] with
the turns [16, 0], [0, 16], D1 at (4, 3) and D2 at (3, 4)). The expected
integers, written down before the first run:

- (a) the birth: at tick 1 the record 2^32 + 1 of two rows at (0, 0),
  (+x, age 0, phase 0, amount 1, content 1, branch 0, multiplicity 2) and
  (+y, phase 16); at tick 2 the record 2^32 + 2 with the phases 1 and 17;
  the lamp's `births` 2;
- (b) the split on the (20, 21) splitter: at tick 11 the record's rows at
  (3, 3) are (+x, age 0, phase 16, amount 41, multiplicity 1682) and (+y,
  phase 32, amount 1, 1682): the reflected 21 and the transmitted 20 merge
  in phase toward D1 and cancel to 1 toward D2 (the design's offers
  1681/1682 and 1/1682); the `cancelled` lines 40 units, 40 content, the
  labels (0, 2560, 0); the balanced (1, 1) split leaves (+x, 16, amount 2,
  multiplicity 4) alone with 2 units cancelled, the books balanced at
  every tick and the row's multiplicity in `state.json`; a row arriving on
  a side the `inputs` do not name refuses the run naming the Node;
- (c) the phase per interval of age on a 9 x 1 x 1 bar with a declared
  ray on +x: after 5 intervals the phase 40 at [8, 1], 26 at [16, 3] and
  24 at the integer 8 (3 Links crossed: the integer turns per Link, the
  pair per interval of age; not one number on the flight table); a rest
  row turns nothing; `run.json` carries the pair; 5 forward and 5 inverse
  intervals on a periodic bar return the row bit-exact; the pair refused
  on a family without a phase circle;
- (d) the refusals of the split: `weights` on `measure`,
  on a free family's entry, of a wrong length, all zero, a turn beyond
  N - 1, `inputs` naming an undeclared direction; a pending row of multiplicity 2^61 split by (20, 21) (A = 841)
  refuses the run naming the Node (3, 3).

## The amplitude law: the layer

`tests/test_amplitude_layer.py` (docs/BEAM_LAW.md note 37; the design,
sections 3, 5 and 7; the decision of 2026-09-20 that a split is not a
click), on the worlds of series L (`examples/events/amplitude/make_worlds.py`,
`expectations.json` written by the generator before the runs). The
expected integers, written down before the first run:

- (a) tests 1 and 3: over the 64 births of the ticks 1 .. 64 the gathers
  per port are the design's table (`mz_equal` D1 64, D2 0; `mz_half` 0,
  64; `mz_quarter` 32, 32; `mz_balanced` 64, 0; `mz_345` 63, 1;
  `mz_unequal_f0` 64, 0; `mz_unequal_f8` 32, 32; `mz_unequal_f16` 0, 64;
  `ev_29` absorber 32, D1 17, D2 15; `ev_169` 32, 16, 16), one gather per
  birth, all complete by tick 76; the record's `total` in the unit 2^58
  takes 8 values between 65448/65536 and 65773/65536 on every world (the
  tables' rounding depends on u; unitarity: the sum over the ports does
  not see the split), so the design's bound 0.0019 holds for u = 0 alone
  and is pinned marked failing beside the measured bound 237/65536; the
  first gather of `mz_equal` names `light`, the record 2^32 + 1, u 0, D1
  on arm 0 channel "0", the weight 1681/1682 of the total, the cells D1,
  D2 with the rungs 64, 64;
- (b) test 8: the same world twice gives the same list; on `mz_345`
  u = 63 falls in D2 (the rungs 63, 64) where `mz_equal` sends it to D1;
- (c) B1: on `mz_quarter` at tick 11 one record's two arms reach the
  splitter a half turn apart (the crowd's pointer 0) and both split (two
  `split` lines of absorbed 1, born 41); on `mz_unequal_f8` at tick 11 the
  rows of two records both split; no `pass` line at the splitter or at a
  `sum` port on any of the ten worlds;
- (d) test 2 on `slits_low`: the first record's cells are the reading's 80
  sets in the layer's order with the reading's rungs, its chosen cell
  (`measured:223`, the Node (7, 58, 0), the content 1) has the reading's
  weight and its `total` the reading's 847181/745472 (a face of 24 Nodes
  hit sums its Nodes' squares: coherent within a Node, incoherent across
  Nodes); the 64 births gather by tick 213; the clicks per set equal the
  reading's on every one of the 80 sets: the wall 11, 12, 11 (34), fourteen
  pixels (15, screen_61 twice), the faces 8, 7 (15, each click at a Node
  of the face's edge); 3 distinct cell lists, 32 records with u = 0's (the
  tables' rounding by u, no rung moved);
- (e) test 7: the seventeen worlds of the gate set parse with the key
  deleted, the identity `amplitude-v1` on the lamp worlds alone;
- (f) test 10: `tools/amplitude_path.replay` on 30-interval runs of
  `mz_equal` and `ev_29` returns `run.json`'s `world`, at least 18
  gathers, the open count of `run.json`'s `layer`;
- (g) S1: `phase_per_link` [2^61, 5] on the bar of age_bound 100 is
  refused at the parse naming (age_bound + 1) x n; the largest admitted
  numerator (2^62 - 1) // 101 reads n mod 64 after 5 intervals;
- (h) S3: two antiphase pairs of one record at two Nodes with the contents
  1 and 3 return {(7, 2, 1): 2, (7, 2, 3): 4} and leave (5, amount 2,
  content 1);
- (i) S4: a lamp of content 1 at K 2 on two directions refuses its birth at
  tick 2 naming the lamp; content 2 births the record 2^32 + 1 of two rows;
- (j) the `record` line of a `sum` set at a gather carries `scope`
  `record`, `of` the record, the pointer whose square is the record and
  the multiplicity 1682; `DetectorSet.scope` is `record` for D1 and
  `crowd` for the splitter's set;
- (k) the review's B1: a lamp into a `sum` re-emitter of two directions
  (`gate`) and two absorbers a, b: every record gathers at the re-emitter
  (its one offer) and what it re-creates is one new record of two rows
  (one `split` line with `rebirth`, born 2; one birth in the layer) that
  gathers once with the cells a, b and the rungs 32, 64, chosen a for
  u below 32 and b above (the rebirth's u the re-emitter's count of
  births, 0 .. 63 over the first 64 rebirths: a 32, b 32; until stage
  (vii) step 2 every rebirth had the re-emitter's phase 0 and went to a);
- (l) the review's B2: a free family's source of amount 3 into a
  `rerelease` on two directions comes out 1 + 2 with the key as without
  it, the rows and the `rerelease` lines the same;
- (m) the review's S3 and S5: a `phase_window` on a `rerelease` entry
  whose Node reads no `sum` set is refused at load ("dead"),
  as is a detector named `measured:3` (reserved);
- (n) the record's total re-pinned at the tables (the reviewer): on
  `mz_equal` the total of the record u is (1681 q[u + 16] + q[u + 32]) /
  (1682 x 65536), q[p] = C[p]^2 + S[p]^2, exactly for every u (the 8
  values within 237/65536 of 1; the design's 0.0019 held for u = 0
  alone); its first gather carries the content 41, the momentum [2624,
  0, 0] and the Node (4, 3, 0) of its click.

## The amplitude law: the one click

`tests/test_amplitude_click.py` (docs/BEAM_LAW.md note 37; the design,
sections 2.1, 2.5 and 6; MIGRATION (vii-1)). The expected integers,
written down before the first run:

- (a) a lamp at the rate [3, 1] on two directions (K 2^20, content 2^20:
  the stride 1) births three records per self-creation: the ordinals 1,
  2, 3 at tick 1 and 4, 5, 6 at tick 2 with u = 0 .. 5 (the ordinal less
  one, the rows' column `birth`), each two rows of amount 1 with the
  multiplicity 2, six births counted at the lamp;
- (b) `common_denominator(2, 8)` = (2, 1, 8), (8, 2) = (1, 2, 8), (9, 36)
  = (2, 1, 36), (1682, 1682 x 25) = (5, 1, 1682 x 25), and (2, 4) none;
  two paths of one record, one through a re-emitter of weight [1] (m 2,
  amount 1) and one through a re-emitter of weight [2] (m 8, amount 2),
  both five Links, meet in phase at one `sum` set: the offer's
  multiplicity 8, its units 3, the record's one cell the set with the
  rung 64, its total and weight 2 x 2^58 (the two paths add: a re-meeting
  is not unitary, the design's 2.5); with the second re-emitter of
  weights [1, 1] on two directions (m 4 against 2) the run is refused:
  "record 4294967297 at the set end carry the multiplicities 2 and 4";
- (c) a keyed bar of 6 Nodes with a lamp on +x, a declared row of light
  of no record at x = 3 and a counter at x = 5: after one interval
  `state.json` holds one row with the three columns and one without;
  over 16 intervals the counter's `click` lines carry `record`, `branch`,
  `multiplicity` and `age` all together or not at all, and both kinds
  occur;
- (d) every world of `examples/events/gate_set.json` without a lamp
  (`weak/j3_deuteron`, `bohr/r2`, `detector/grouped_12_nodes`,
  `weak/j2_ladder`, `weak/j3_deuteron_crowd`, `nucleus/alpha_square`,
  `hubble/pushing_age`, `coupling/1b_m16`), run at its `cap` with the key
  and without it: `events.jsonl` and `state.json` equal byte for byte,
  the books (`audit`) equal, `run.json`'s `amplitude` false and true
  (step 1); since step 4 (the key deleted) the run at the cap gives the
  base tree's `state.json`, books and `events.jsonl`, pinned by their
  sha256 (the trimming's fast pass of 2026-09-20: `weak/j3_deuteron`
  b9e0613b21af..., 431cc87afa9f..., 15450ef9d5d0...; `bohr/r2`
  3d6b27e299af..., 51c74ad753d8..., f5dfd739878e...; the six others in
  the module);
- (e) step 2: a bar of 12 Nodes with a lamp at the stride 1 and a counter
  whose `measure` entry has the window 0 of width 8: no `pass` line at
  the counter over 80 intervals and at least 60 clicks, every click's `u`
  its record's ordinal less one and its `phase` equal to `u` (the path
  phase 0), the rows' `birth` the same;
- (f) step 2, the K record world (`lensing/mass_meeting` with
  every pixel `sum`, the lamp's `turns` 0, 300 intervals): the 64
  records of the ordinals 129 .. 192 carry u = 0 .. 63 once each; per
  set their clicks are within one rung of the sum of their cells' widths
  over N; the click centroid in y is within 0.25 pixels of the
  expectation's; the light's `turned` line is not zero;
- (g) step 3, the push by share: a plane of 9 x 3 with a lamp on +x at
  (0, 1), a splitter of the weights [1, 1] on +x and +y at (3, 1) and a
  mass (a free family of content 4096) at (7, 1), 60 intervals: at least
  20 clicks at the mass and 20 re-releases at the splitter; every click
  at the mass carries `push` [64, 0, 0] and `share` [32, 0, 0] (amount 1,
  m 2); the mass's momentum [32 x clicks, 0, 0]; the splitter's
  [64 x re-releases - 32 x splits, -32 x splits, 0]; the books balanced,
  the `remainder` line [32 x clicks - 32 x splits, -32 x splits, 0] for
  the world and for the light.

## The amplitude law: the gate

`tests/test_amplitude_gate.py` (docs/BEAM_LAW.md note 37; the design,
section 10 and `gate.py`, section 4.3 and `bell.py`), on the worlds of
series L5 and L6 (`examples/events/amplitude/make_worlds.py`,
`expectations.json` under `gate` and `pair_n`, written before the runs).
The expected integers, written down before the first run:

- (a) on `cnot_pair_0_8` the Hadamard re-emitter turns the control's row
  into two rows on the label bit 0, the amounts 181 (C'[16] of the 128
  tables) at the phases u and u + 32, the multiplicity 65536 (the
  `rotate` line: 2 rows, the record's units 1 to 362); at the gate the
  control (2^32 + 1, the survivor) joins the target (the lamp of number
  4): the `gate` line names them, the labels [[0, 1], [3, 1]], 2 arms, 4
  rows; the rows after: on +y the labels 0 (181 at u) and 3 (181 at
  u + 32) at m 65536, on -y the labels 0 and 3 of amount 1 at m 2, the
  design's |00> - |11>;
- (b) the pair by the gate at the CHSH labels with Bob at -b: the cells'
  counts the reading's, E x 64 = 44, -44, 44, 44, S = 176/64, Alice's
  marginal 32/64;
- (c) `cnot_twice`: three `gate` lines for the record, the second and
  third (one per arm, at (11, 5) and (8, 8), no record joined) with the
  labels [[0, 1], [1, 1]]; the rows after on +y: the labels 0 and 1 at
  181 (phases u, u + 32; m 65536) and at 1 (m 2), H|0> x |0> again; 64
  gathers at the absorbers;
- (d) `cnot_ghz_*`: XXX allows ++-, +-+, -++, --- (the product -1, this
  convention's H) and XYY, YXY, YYX allow +++, +--, -+-, --+ (+1), 16
  births each; the `gate` line's labels [[0, 1], [7, 1]], 3 arms, 6 rows
  (at most 3 x 2^3 after 3 records; the pair's 4 at most 2 x 2^2);
- (e) `rotations_3` runs (the clicked rows' multiplicity 2^48, 64 gathers);
  `rotations_4` is refused at load, the multiplicity through its
  re-emitters 2^64 beyond 2^62 - 1, naming the fourth rotation's Node
  (8, 0, 0); Grover's six rotations are not a world of the GameBoard;
- (f) the refusals: `rotate` and `gate` on `measure`;
  a gate kind other than `cnot`; `hold` not a boolean; `parties` 0; a
  rotation's bit beyond 31; `half_angle(1, 4096)` refused, `half_angle(512,
  4096)` the 4096 table's entry at 256, `half_angle(16, 64)` (181, 181);
- (i) the review of (v), B1: the `gate` line's `added` is 1 on every gate
  of `cnot_pair_0_8` (the target's row of amount 1 into two copies) and
  every gathered record of the run ends at live 0 (before the fix, -1);
- (j) B2: `cnot_pair_0_8` with the control's path split (1, 1) at (6, 5)
  between the Hadamard and the gate and the second output into an
  absorber reading `sum` is refused at the gate naming the record
  2^32 + 1, its units elsewhere and its offers;
- (k) S1 and B3: `cnot_pair_0_8` with its `measured` list reversed gives
  the same multiset of outcomes over the run, E positive either way;
- (l) the control's refusals: a gate of 2 parties without `control`
  ("declares its control"), a gate of one party with one, and a control
  direction [0, 1, 0] no record arrives on ("finds 0 records arriving");
- (g) `bell_n1024_*` (one birth per u, the births counted by the record's
  ordinal: a lamp's clock skips a step as the births spend its content):
  the counts the reading's, E x 1024 = 724, -724, 724, 724, S = 2896/1024
  (the design's), |E - cos| <= 1/N on every pair;
- (h) `bell_n4096_0_512`: the counts the reading's, E x 4096 = 2900 (the
  four pairs 2900, -2900, 2892, 2892), S = 11584/4096 = 2.828125 below
  2 sqrt 2; the design's bound |E - cos| <= 1/N fails at this N (the
  tables' entries in 1/256 round E by 0.0009 against 1/4096 = 0.00024),
  pinned as the design's value marked failing.

## The amplitude law: the pair

`tests/test_amplitude_pair.py` (docs/BEAM_LAW.md note 37; the design,
section 4 and `bell.py`), on the worlds of series L3 and L4
(`examples/events/amplitude/make_worlds.py`, `expectations.json` under
`pair` and `ghz`, the design's reading written by the generator before the
runs: the rotation on the half-angle tables of 2N, the joint amplitude the
sum over the labels of the products of the arms' entries, its square the
weight, the cells in the arms' order, the rungs at the nearest integer).
The expected integers, written down before the first run:

- (a) the birth of a pair on `bell_0_8`: at tick 1 the record 2^32 + 1 of
  four rows of amount 1 and multiplicity 2 at (10, 0, 0), the labels 0
  and 3 on arm 0 (-x, Alice) and arm 1 (+x, Bob), the branch arm x 2^32 +
  label; the `birth` line: labels [[0, 1], [3, 1]], 2 arms, 4 units,
  multiplicity 2;
- (b) the CHSH labels (the design's test 4): over the 64 births the cells
  (oA, oB) count 27, 5, 5, 27 on `bell_0_8` (E x 64 = 44), 5, 27, 27, 5
  on `bell_0_24` (-44), 27, 5, 5, 27 on `bell_16_8` and `bell_16_24`
  (44); S = 176/64; Alice's outcome + for u < 32 and - for u >= 32 on
  every world, both marginals 32/64; every gather's `windows` are
  [alice_plus, a, 0], [bob_plus, b, 0]; alice_minus and bob_minus click
  nothing;
- (c) the choosers (`bell_choosers`, the 960 births from tick 8; the 7
  born before click at alice_minus): the gathers grouped by the settings
  give the 15 pairs (0, 12, 25, 38, 51) x (8, 29, 51), 64 records each
  with every u, the counts per pair the reading's and E x 64 = 44, -60,
  20, 60, -8, -48, -8, 60, -52, -64, 40, 20, -28, -36, 64 in that order,
  every marginal 32/64, S on (0, 25) x (8, 29) 156/64 (2 under the
  register's window gate);
- (d) the which-path worlds (`path_*`, the design's test 6): eight cells
  (label, oA, oB) per record, E x 64 = 44, -44, 0, 0, S = 88/64;
- (e) no maintenance (`bell_16_24_far`, `path_16_24_far`; the design's
  test 9): E x 64 = 44 and 0 as at the labels, every record gathering at
  least 200 intervals after its birth;
- (f) GHZ (the design's test 5): XXX allows +++, +--, -+-, --+ (the
  product +1) and XYY, YXY, YYX allow ++-, +-+, -++, --- (the product
  -1), 16 births each, eight cells per record; YYY allows all eight, 8
  each;
- (g) the refusals: `arms`
  beyond the directions or not dividing them; a label at or above 2^arms;
  a label twice; a weight 0; `turn` on `pass` and beyond N - 1; a `turn`
  of 16 parsed into `label_turns`.

## The meeting

`tests/test_meeting.py` (docs/BEAM_LAW.md, section 3 step 3 and section 10
note 35; the model owner, 2026-09-20, "DECIDED: the meeting, M-R: an event
in transit reads the crowd as a body does, a report, not a balance"; the
physicist's and the mathematician's design of the same day, section 6
item 3; `events/meeting.py`). K 2^20, N 64, `suspension` 0, `release`
[0, 1]. The expected integers, written down before the first run:

- (a) the arc permutation on the 296-entry direction table of series K
  (the two rest vectors, the six headings, the 288 primitive directions
  with |a| + |b| + |c| <= 6 beyond them and the lamp's (24, +-1, 0),
  (12, +-1, 0)): for 1034 fixed targets (the 342 integer vectors in
  [-3, 3]^3 but 0, the 294 unit labels of the moving directions and the
  first 398 nonzero sums of the label pairs (i, (37 i + 11) mod 294) for
  i from 0) pi_t is a permutation, the two rest directions are fixed, the
  cached inverse returns the identity and pi_t^3 = pi_t o pi_t o pi_t;
  (1, 0, 0) under t = (0, -1, 0) goes (24, -1, 0), (12, -1, 0), (5, -1, 0),
  (4, -1, 0), and under t = (0, -64, 0) (one crowd unit's flow) the same
  four, one cache entry per target (the sector boundary |u . e1| = |u . e2|
  lies at the angle 1 / |t| off the e1 axis, so the sectors depend on |t|:
  the design's rule as flown offline); on the six headings alone +x under
  t = (0, -1, 0) is fixed (a sector of one) and the on-line pair +y, -y
  swaps ([0, 1, 2, 3, 5, 4, 6, 7]).
- (b) the register: a unit of phase 60 meeting one crowd unit (|t| = 64)
  per interval reads the phases 61, 62, 63, 0, 1, 2 with k = 1 at the
  fourth alone; meeting two units (|t| = 128, adv 2) it wraps at the second
  (62, then 0 with k = 1); the inverse (adv - phase' + 63) // 64 gives the
  same k and the phase before for every case; |t| = 31 advances by 0 and
  |t| = 32 by 1 (the nearest whole unit of Q); no crowd leaves the phase
  alone; on the GameBoard (the world of (c) with the phase 60) the same six
  phases and the turn at the fourth interval.
- (c) the sign: a paid unit of `light` on +x at phase 63 on the line
  y = 0, z = 0 of a 4 x 1 x 2 GameBoard (x and y periodic, z open; the two
  measured events the numbers name parked on the plane z = 1, which
  nothing visits, releasing nothing) with one free unit of `m` of another
  number on +y at every Node of the line (V = (0, 64, 0), kappa = -1,
  t = (0, -64, 0)) turns to (24, -1, 0) in the first interval on K's
  table, its label (64, 0, 0) -> (64, -3, 0), the `turned` line (0, -3, 0)
  (the family's and the world's), the transit momentum line (64, 253, 0)
  (its label and the four crowd units' (0, 256, 0)), the running line
  equal to the recount; on the plane fan of the primitive (a, b, 0) with
  a >= 1 and a + |b| <= 13 (whose finest step off +x is (12, +-1, 0); the
  shipped two-slit fan stops at a + |b| <= 12, whose first step would be
  (11, -1, 0)) it turns to (12, -1, 0), the `turned` line (0, -5, 0);
  kappa of a paid family whose columns beyond gravity are 0 against a
  charged free family is (-1, 1), a reader whose charge column reads 2
  against a crowd of charge 1 has kappa (1, 1) and its +x turns toward
  t = +V = (0, 64, 0) to (24, +1, 0), and the pair (1, 2) against (1, 3)
  reads (-5, 6); the world's `hypotheses` ["meeting-v1"], `run.json`
  carrying `meeting` true and the `turned` line in its audit; without the
  key nothing turns, the phase stays 63 and the `turned` line is zero.
- (d) untouched: the free rows of the world of (c) are equal at every one
  of six intervals to the free rows of the same world without the key
  (Node, direction, age, phase, number, amount, content); the paid unit's
  age 6, number 1, amount 1 and content 1 after the six intervals; two
  paid units of two families (`light` of content 1 and `photon` of content
  2) at one Node with the crowd both turn to (24, -1, 0) (the same V; the
  `turned` line (0, -9, 0), the photon's (0, -6, 0)), and at a Node without
  a free unit neither turns nor advances its phase (they never read each
  other); a free unit of the paid unit's own number on +y is not read (no
  turn, the phase 63 kept).
- (e) the bijection: the periodic 8 x 8 x 4 world of the bijection test
  (`age_bound` 128) with its 300 fixed records split into 240 of the free
  family `m` (given the number 2 on the record before the first interval:
  the GameBoard of rays alone names no emitter, and what the meeting reads
  is the number on the record) and 60 of the paid family `light` (every
  fifth record, the number 1, `phase_per_link` 5), `meeting: true`; the
  stores hold 259 and 65 rows after the merge; 50 forward then 50 inverse
  intervals: the sorted stores of both families bit-exact, the paid store
  at the turning point differing, the `turned` line of `light` nonzero at
  the turning point (at least one turn on the way) and `m`'s zero, both
  zero again at the end, the running transit momentum line equal to the
  recount at every interval both ways; the refusals, naming the key: a
  phase-less paid family under the key (naming the register), `meeting`
  that is not true or false.
- (f) the bit-identity of the register is a replay, not a test:
  [validation](VALIDATION.md), every example world without the key
  byte-identical in `events.jsonl` and `state.json`, and the ten
  registered worlds the design names byte-identical with the key declared.

Re-pinned with the new line written first: `tests/test_lifetime.py` (b)
and `tests/test_nature_beam_flight.py` (the periodic axis and the open
face), the books' momentum block gaining `"turned": [0, 0, 0]`.

## The books

`tests/test_nature_beam_books.py` (docs/BEAM_LAW.md, section 10, note 22; added
2026-09-19 with the optimizations): `books()` reports the transit line,
the content line and the transit momentum as the running lines of the
ledger (what was released less what left: escaped, home, absorbed;
O(families), no pass over the store) and `recount()` counts the same
three lines from the rows of the store. On a 12 x 1 x 3 GameBoard with y
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

`tests/test_nature_beam_detector.py` (docs/BEAM_LAW.md, section 5). K 2^20,
`suspension` 0, `release` [0, 1], the families `m` (free) and `light`
(paid), every measured event `fixed`; the detector `d` of (a) to (e)
declares the reading `wave` (the default since 2026-09-20; from
2026-09-19 to 2026-09-20 the default was `beam`).

- (a) two rays of amount 1 arriving in one interval at a counter of
  threshold 1, in phase (0 and 0): the record 4 x 32^2 x 256^2 = 268435456,
  the amount 2 and two clicks; in antiphase (0 and 32): the pointer 0,
  both click and the record is 0 (the threshold is the amount since stage
  (vii) step 4, the one click; from 2026-09-20 to that step the pointer's
  square gated the set and both passed naming `threshold` 1; re-run under the one click (stage (vii) step 4); the verdict to be re-read); one
  ray alone: 32^2 x 256^2 = 67108864; the
  `record` line of `events.jsonl` carries the pointer (X, Y) and the
  square; the run's detector report carries the cumulative record.
- (b) a receiver (a measured event of `m`, content 4, measuring light) at
  threshold 3 (re-pinned from `test_detector_sensitivity` (a); since
  2026-09-20 the threshold under `wave` reads the pointer's square, so the
  smaller set is one ray, 1 < 3, where two rays in phase read 4): 1 ray of
  another number passes with a `pass` record (`threshold` 3), no click, no
  push, the ray going on whole; 3 rays are measured: 3 clicks, `held`
  [4, 3], the momentum (192, 0, 0) (three labels of 64 along +X;
  re-pinned from (3, 0, 0) on 2026-09-19, the label along the unit
  vector), nothing left in the store, the report 3 measured, 3 clicks,
  the record 9 x 32^2 x 256^2 (a row of three identical rays is one
  coherent amplitude).
- (c) a re-emitter at threshold 3: 1 ray passes; 3 rays are taken
  (re-released 3, no click, the push (192, 0, 0), the recoil at the
  re-emission -(64, 64, 64) leaving the momentum (128, -64, -64); re-pinned
  from (3, 0, 0), -(1, 1, 1) and (2, -1, -1)) and created again at the
  same interval's self-creation, one per declared direction (+X, +Y, +Z),
  with the re-emitter's number, the arriving phase 20, content 1, age 0.
- (d) an emitter inside a detector reads no threshold: a lamp of light
  (content 24, K 24, rate [1, 1]) in a detector of threshold 5 releases one
  unit per heading per interval, its content 18 then 12; a reader of `m`
  (content 4) at threshold 4 passes 3 rays and reads 4, pushed by
  -M x 64 x 4 = (-1024, 0, 0): a `read` keeps the amount gate under both
  readings (re-pinned on 2026-09-20 to the pointer gate, 1 passed and 2
  read, (-512, 0, 0), and pinned back the same day by the closing gate's
  finding F1, test (k); before that from (-16, 0, 0)).
- (k) the pointer gate is the click's (the closing gate's finding F1,
  2026-09-20; BEAM_LAW note 32): two free rays of one number, amount 1
  each, into a fixed reader of content 5 with the keys' own `read` push it
  by -5 x 2 x 64 = (-640, 0, 0) in antiphase under the default `wave` set,
  in antiphase under a declared `beam` set and in phase under `wave`, with
  no `pass` record and the rays going on (two identical records at one
  Node one record of amount 2); the amount gate still holds on a `read`
  (one ray at a threshold of 2 passes); the same rays into a `measure`
  counter under `wave` pass (test (i)).
- (e) the record is exact and never refused (BEAM_LAW section 5 and note
  19; the night's bound refused `two_contents`): every entry (C, S) of the
  1/256 tables is shorter than 257 for every N from 2 through 4096 (the tables'
  bound is 65536 since 2026-09-20, the phase circle's test at the end of
  `tests/test_nature_beam_world_parsing.py`: 65536 accepted, the eighth turn 181,
  every entry within 256, 131072 refused; the
  largest C^2 + S^2 is 65897), so each component of the pointer is within
  32 x 257 x the clicked amount; since the four unifications (2026-09-20,
  (j)) the pointer is the first moment of the one reading over the
  circle, taken in the int64 register where the reading's bound holds for
  its table (`reading_fits`: 32 x amount x 256^2 x the rows of a group
  within 2^62 - 1, so one row of an amount below 2^41 and 2^41 - 1 rows
  of amount 1 fit, 2^41 do not; until then `POINTER_AMOUNT_BOUND` =
  (2^62 - 1) // (32 x 257) = 560759486676481 on the clicked amount) and in
  Python integers beyond it (`moment_table(exact=True)`); the square and
  the record are Python integers always. Every case is compared with the Python-int
  computation X = sum 32 x amount x C[phase], Y = sum 32 x amount x
  S[phase] over the clicked rows of the record through the tables: a row
  of 261123 (the old bound) records 2139119616^2 with the pointer
  (2139119616, 0); a row of 261124 (one past the old bound) records
  2139127808^2; a row of 2^18 (what `two_contents` sends to a face)
  records 2^62 exactly, one past the law's bound 2^62 - 1; two rows of
  130561 and 130563 (two numbers, +X and -X, a quarter turn apart) record
  (2^13 x 130561)^2 + (2^13 x 130563)^2; a row of 2^49 (beyond the
  pointer's register bound, as the reviewer's silent int64 wrap at 2^52
  was; re-pinned from 2^52 on 2026-09-19, when the reading's second-moment
  bound on the unit vectors, amount x 64^2 x rows, began to refuse a row
  above 2^50 at a measured event's Node before any record) records 2^124
  with the pointer (2^62, 0); two rows of 2^18 clicking in the intervals 1
  and 3 accumulate
  2^63, beyond int64, in the measured event's record, its state and the
  report, round-tripped through JSON; a ray of 2^18 stepping off the open
  face +x records 2^62 on `face:+x`.
  (2^13 x 130561)^2 + (2^13 x 130563)^2; a row of 2^52 (the reviewer's
  silent int64 wrap, once refused) records 2^130 with the pointer
  (2^65, 0); two rows of 2^18 clicking in the intervals 1 and 3 accumulate
  2^63, beyond int64, in the detector's record and the report,
  round-tripped through JSON; a ray of 2^18 stepping off the open face +x
  records 2^62 on `face:+x`.
- (f) the set (the model owner's principle, 2026-09-19): a `wave`
  detector `d3` of three Nodes, (4, 0, 1), (4, 1, 1) and (4, 2, 1), each a
  counter of `m` (content 4) measuring light: one ray of amount 1 arriving
  at any one of the three gives one `record` line naming `d3` (its `node`
  and `measured` None), the record 32^2 x 256^2 the same whichever Node
  it reached, and the click at the Node it reached (that counter holds
  [4, 1], the other two [4, 0]); at threshold 2 one ray of amount 1 at
  one Node passes (`threshold` 2) while two rays of amount 1 at two
  different Nodes in the same interval both click and record 4 x 32^2 x
  256^2 (one pointer over the set); the window reads the set's phase: two
  rays at the phases 0 and 16 at two Nodes have the set's phase 8, and
  with the window 20 on every counter both click (the phase 0 alone would
  be outside) while with the window 56 both pass with `window` 56 (the
  phase 0 alone would be inside).
- (g) the phase returned (the model owner, 2026-09-19): a click of one ray
  of phase 40 at a one-Node `wave` detector whose counter is at phase 0
  leaves the counter at phase 40 (the report's and the `record` line's
  `phase` 40), the turn of K 2^20 being 0; a lamp of light (content 24,
  K 24, rate [1, 1]) in a `wave` detector that clicks a ray of phase 40
  at tick 1 is at phase 41 after the interval (the frame's turn 1 added
  after the click) and at 42 after the next, and its births are records
  born at u = 0 then 1 with the direction's turn 0 (the returned phase
  no longer enters a lamp's rows since stage (vii) step 4; until then the
  six rays of tick 1 carried 40 and the next 41; re-run under the one click (stage (vii) step 4); the verdict to be re-read); the set of three
  Nodes of (f) with the rays at 0 and 16 puts all three counters at phase
  8; a ray below the threshold leaves the counter at phase 0, and a
  `read` of `m` (a ray of phase 40) leaves the reader at phase 0.
- (h) the reading `beam` (declared; the default until 2026-09-20): at a one-Node beam detector, two
  rays of amount 1 in phase (0 and 0, +X and -X) both click, the record
  (the count) 2, the `record` line without a pointer and with `phase` 0;
  opposite (0 and 32) both pass with `cancelled` true, no click, the two
  rays going on whole, the record 0 and no `record` line; a quarter turn
  apart (0 and 16) with the window 16 on the counter both are admitted by
  the gate and paired (the arc the half circle centred on the opposite
  phase), both pass cancelled; without a window they are not paired and
  both click; three rays at the phases 0 (+X), 32 (-X) and 0 (+Y) in the
  order of their numbers: the first pairs with the second, the third
  clicks alone (1 click, record 1); rows of 3 (phase 0) and 2 (phase 32):
  2 units pair and pass, 1 unit clicks (the click line's amount 1, the
  two `cancelled` lines 2 and 2, the rows of 2 and 2 in the store); the
  books balanced in every case; `"reading": "field"` is refused naming
  the key.
- (i) the threshold on the pointer's square under `wave` (the model owner,
  2026-09-20, issue #359 step A; the integers written first): one unit at
  any of the 64 phases reads 1 unit (`pointer_units`, the nearest integer
  to (X^2 + Y^2) / 2^26), a rays in phase a^2 exactly through a = 11 (the
  tables' C^2 + S^2 within 237 of 65536 at N = 64), two opposite 0, two a
  quarter turn apart 2; on the engine one ray (phase 8) clicks at
  threshold 1; two rays in phase (0 and 0) click at threshold 4 (the
  square 4) and pass at 5; two opposite rays (0 and 32) pass at threshold
  1 with `threshold` 1, whether or not the counter declares a window (the
  window 0: still `threshold`, not `window`); three rays a third of a turn
  apart (0, 21, 43) pass at threshold 1 (their pointer's square 200704,
  0.003 of a unit); under `beam` the threshold is the amount as before:
  two rays in phase at threshold 3 pass (the amount 2 < 3) where `wave`
  clicks them (4 >= 3); no memory between intervals: the two opposite
  rays passing at tick 1 do not add to the next tick's set.
- (j) the pointer is the first moment of the one reading over the circle
  (the four unifications, the model owner, 2026-09-20, (1); BEAM_LAW note
  33; the integers written first): rows of amounts 3, 5, 2 at the phases
  0, 16, 32 of N = 64 (the entries (256, 0), (0, 256), (-256, 0)) read the
  pointer (8192, 40960) = 32 x (768 - 512, 1280), equal to
  `read_arrivals` on the circle's unit vectors (C, S, 0) with the weights
  32 x amount (its flow; its presence 320 = 32 x 10), the record 8192^2 +
  40960^2 = 1744830464 = 26 units exactly ((3 - 2)^2 + 5^2), the set's
  phase 14 (the nearest step to atan 5 = 78.69 degrees, 14 x 5.625 =
  78.75); two groups (the rows 0 to 1 and 2) read (24576, 40960) and
  (-16384, 0); one row of 2^42 at phase 5 is beyond the reading's
  register bound (32 x 2^42 x 256^2 = 2^63), so `read_arrivals` refuses
  it while the pointer reads 2^47 x (C[5], S[5]) = 2^47 x (226, 121)
  exactly on its Python path; one row of 2^49 (beyond the former pointer
  bound 2^48) reads (2^62, 0), one of 2^60 (whose amplitude would not fit
  the register) (2^73, 0): the record is never refused.

## The push as one form

`tests/test_nature_beam_push.py` (docs/BEAM_LAW.md, section 3 step 4, section 5 and
section 10 notes 18 to 20 and 28; the model owner's proposal 2 of
2026-09-19 with the physics-rule reviewer's two corrections, and the
decision of 2026-09-20 that charge is per unit of content of a family):
for a free family's rays ONE product, push_A = M_A x (rho_A rho_B - 1) x
V_B, with V_B the label flow of the arriving rays, M_A the reader's
content as the frame read it and rho_A, rho_B the families' charges per
unit of content as the pairs [n, d] (the gravity -M_A V_B plus the
electric part off the reader's clock, sign x by_clock(age_A, |V n_A n_B
M_A|, d_A d_B)); for a paid family's rays V_B itself; nothing on the
record but the number; every momentum the law reads or moves the one
label. K 2^20, N 64, `suspension` 0, the free families `m` (the source's)
and `p` (the probe's, a second family since 2026-09-20: one charge per
unit of content is one family, and the reviewer's world gives the source
and the probe different ratios) and `light` paid, every measured event
`fixed`, a 12 x 1 x 1 bar with y and z periodic unless said otherwise.
Re-pinned on 2026-09-19 for the label along the unit vector ([BEAM_LAW note 23](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)):
every integer of the six-heading cases is the first pin times 64 (the
label of a unit along a heading is 64 e_d), the fan cases read u_(2, 1, 0)
= (57, 29, 0); the first pins are named in brackets. Re-pinned on
2026-09-20 for the charge per unit of content: the whole charges of the
fixtures become the same numbers as pairs (a source of content 4 and
charge 3 is the family `m` of charge [3, 4]; a probe of content 5 and
charge 1 the family `p` of charge [1, 5]) and every integer is unchanged.

- (a) the reviewer's isolated world: a source of content 4 and charge 3
  (`m`, [3, 4]) at x = 0 releasing on +X at `release` [1, 1] (4 rays per
  interval, one row of amount 4), a probe of content 5 and charge 1 (`p`,
  [1, 5]) at x = 6; on (1, 0, 0) a ray born at tick t is at x = 6 at tick
  t + 10, so the probe reads one row of amount 4 at every tick 11 through
  30: 20 `read` records, each the label flow V = 4 x 64 = 256 and the
  push -5 V + by_clock(age, 3 V, 4) = -1280 + 192 = (-1088, 0, 0) [was
  (-17, 0, 0)], the same integer as by_clock(age, |256 x 3 x 1 x 5|, 4 x
  5) = by_clock(age, 3840, 20), `pushed` (-21760, 0, 0) [was (-340, 0, 0)]
  (64 x 80 x (-5 + 3/4) exactly); the store's columns are the seven of
  the record (no `charge`, no `mass`); the source's `charge` reads (3, 1)
  and the probe's (1, 1).
- (b) the sign (the source's charge -3, [-3, 4]): every push (-1472, 0, 0)
  [was (-23, 0, 0)], `pushed` (-29440, 0, 0) [was (-460, 0, 0)]. (c) An
  uncharged probe (charge 0): every push (-1280, 0, 0) [was (-20, 0, 0)],
  `pushed` (-25600, 0, 0) [was (-400, 0, 0)].
- (d) rho_A rho_B = 1 (the series 7 cancellation): the probe of content 1
  and charge 2 ([2, 1]), the source of charge 2 and content 4 ([1, 2]):
  every push -256 + by_clock(age, 256 x 2 x 1 x 1, 2) = 0 exactly,
  `pushed` (0, 0, 0).
- (e) the fractional floor (the reviewer's F6): `release` [1, 2] gives
  V = 128, |V n_A n_B M_A| = 1920 over d_A d_B = 20 (3 V / 4 = 96 as
  before), and by_clock(t, 1920, 20) = by_clock(t, 384, 4) is 96 at every tick
  t (the floor resolves 1 / Q per unit; on labels of length 1 it was 2 at
  odd t and 1 at even t, 30 over the twenty ticks); over the ticks 11
  through 30 the electric part sums to 1920 and the gravity to -12800:
  `pushed` (-10880, 0, 0) [was (-170, 0, 0)].
- (f) a paid emitter: a lamp of `light` (content 2^23 at K 2^20, the turn
  8 at every age below 362, `rate` [1, 1] on +X) releases one unit of
  content 8 per interval with the recoil (-512, 0, 0) [was (-8, 0, 0)];
  the probe (content 5, `table` {"light": "read"}, `release` [0, 1]) reads
  (512, 0, 0) at every tick 11 through 30, `pushed` (10240, 0, 0) [was
  (160, 0, 0)]; the lamp's momentum (-512 x its releases, -15360 after
  30) plus the transit line plus the escaped line is (0, 0, 0) at every
  tick.
- (g) a fan emitter: a source of content 4 at (0, 0, 0) of a 9 x 5 x 1
  GameBoard releasing on (2, 1, 0) at `release` [1, 1], the probe of content 5
  at (4, 2, 0) on its line (the sixth Manhattan step; the first read at
  tick 9): every push -5 x 4 x (57, 29, 0) = (-1140, -580, 0) [was
  (-40, -20, 0)], 22 reads, `pushed` (-25080, -12760, 0) [was (-880,
  -440, 0)]: the push of a fan ray is its label along u_d, of length 64
  within 1.35 % (sqrt 4090 = 63.95), not |D| = sqrt 5 per unit.
- (h) the one label moves: a ray of `light` of amount 3 on (2, 1, 0)
  (content 1; at (3, 2, 0) with age 7, one Link before (4, 2, 0)) clicking
  at a `measure` event at (4, 2, 0): the click's `push` (171, 87, 0) [was
  (6, 3, 0)], the event's momentum (171, 87, 0), the transit line
  (171, 87, 0) before and (0, 0, 0) after; the same ray at a `rerelease`
  event whose one direction is (2, 1, 0): the momentum (0, 0, 0) after the
  interval (in (171, 87, 0), out the same), the transit line (171, 87, 0)
  before and after; a paid ray coming home on a periodic 4 x 1 x 1 bar:
  the `home` record's `push` is its label (64, 0, 0) [was (1, 0, 0)] and
  the emitter's momentum (0, 0, 0) after the re-creation.
- (i) the rows met decide (added 2026-09-19 with the bulk step 4): the
  world of (a) with two bystander rays of the probe's number and family
  parked on the stub of the y axis at x = 2 and 3, rows before the probe's
  in the store: every push (-1088, 0, 0) and `pushed` (-21760, 0, 0) as in
  (a), the bystanders untouched.
- (j) M_A is the content the frame read (the architect's B3, the
  orchestrator's D1, 2026-09-20; [BEAM_LAW note 27](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)):
  a 13 x 1 x 1 bar (y, z periodic), K 1024, `release` [1, 1], the
  families A (free, no phase circle) and B (paid, quantum 1); a source of
  A (content 3) at x = 0 releasing on +X, a reader P of A (content 5) at
  x = 6 measuring B by default, a lamp of B (content 4000, `rate` [1, 1]
  on -X) at x = 12: a B click and an A read land at P in one interval.
  With the families declared [A, B] and [B, A] alike: P's reads at the
  ticks 11 to 16 push (-960, 0, 0), (-1536, 0, 0), (-2304, 0, 0),
  (-3072, 0, 0), (-3840, 0, 0), (-4608, 0, 0) (V = 192; M_P = 5, 8, 12,
  16, 20, 24, the clicks of the intervals before), `held` {5, 114} and
  `pushed` = momentum = (-356544, 0, 0) after 40 intervals [the order
  [B, A] read (-1536, 0, 0) at tick 11 and (-378432, 0, 0) before the
  pin]. No other pin moves: no registered world has a paid click and a
  free read at one reader in one interval.
- (k) a re-emitted free ray is its family's ray (the architect's B2, the
  orchestrator's D2, 2026-09-20; [BEAM_LAW note 28](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)):
  a source of the free family B (content 4, charge [1, 4]) at x = 0
  releasing on +X, a mirror of the free family A (content 4, charge
  [1, 5], `table` {"B": "rerelease"}, `directions` [+X]) at x = 4, a
  reader of A (content 5) at x = 8: the reader reads number 2's rays of
  the family B at every tick 15 through 30 (16 reads, amount 4) with the
  push -1280 + by_clock(age, |256 x 1 x 1 x 5|, 5 x 4) = -1280 + 64 =
  (-1216, 0, 0) (the ray's family's rho 1/4; the re-emitter's 1/5 would
  read 51 or 52), and the mirror's own free release of A under the
  family A from tick 8 with -1280 + by_clock(age, 1280, 25), the age
  the reader's clock age, tick - 1 (re-pinned on 2026-09-20 for the four
  unifications (4) from the age after the frame's advance, tick: the sum
  over the 23 reads moves by -1); no error
  (until 2026-09-20 the re-emitted rows carried the re-emitter's held
  content of B, 0, and the charged reader divided by it); the mirror
  re-released 92 units and is pushed; the mirror's `charge` (4, 5), the
  reader's (1, 1).
- (l) the equivalence principle for the electric push (the model owner,
  2026-09-20): the source of `m` (content 4, charge [1, 4]) and a probe of
  `p` (charge [2, 1]) of content M = 1, 4, 16: the electric part
  by_clock(age, 256 x 1 x 2 x M, 4) = 128 M exactly and the gravity -256
  M, so every read pushes (-128 M, 0, 0), `pushed` (-2560, 0, 0),
  (-10240, 0, 0), (-40960, 0, 0) after 20 reads; the probe's `charge`
  (2 M, 1) and the books' `charge` [2 M + 1, 1].
- (m) the columns are floored at the clock age like every other rate
  (the four unifications, the model owner, 2026-09-20, (4); BEAM_LAW note
  33, the one exception of note 20 removed; the integers written first):
  the fan world of (g) with the source's `release` [1, 4] (one ray of
  amount 1 per interval, the flow V = u_(2, 1, 0) = (57, 29, 0), odd on
  both axes), the source's charge [1, 2] and the probe's [1, 1] (content
  5): the probe reads at every tick t from 9 through 30 the push (-285 +
  by_clock(t - 1, 285, 2), -145 + by_clock(t - 1, 145, 2), 0), that is
  (-143, -73, 0) at an odd tick and (-142, -72, 0) at an even one (until
  2026-09-20 the floor was read at the age after the frame's advance, t,
  which put the extra unit on the other parity: every tick moves by
  exactly one unit per axis), and `pushed` after the 22 reads (-3135,
  -1595, 0), the same sum under both clocks (the floors telescope; the
  mathematician's clock_checks 3); (e)'s pin does not move (1920 / 20 =
  96 exactly) and (k)'s is re-pinned.

## The columns

`tests/test_columns.py` (docs/BEAM_LAW.md, section 3 step 4 and section 10
note 31; the model owner, 2026-09-20, "one mechanism for all the laws on
the GameBoard"; the mathematician's verified form, scratchpad/columns/
COLUMNS.md): the push a measured event A takes from a group of a free
family B's rays with the label moment V is, per axis, the sum over the
columns c of epsilon_c x sign(V E_c n_c) x by_clock(age_A, |V E_c n_c|,
D_c d_c), (E_c, D_c) the reader's charge in the column (the rational sum
over what it holds of the value times the content), (n_c, d_c) the arriving
family's value, every column floored on its own; `gravity` the built-in
first column (the value [1, 1], the sign minus), `charge` the second (rho,
the sign plus), a declared column (`"columns": {"<name>": {"value": n or
[n, d], "sign": 1 or -1}}`) a further term. K 2^20, N 64, `suspension` 0,
`release` [0, 1] (the rays declared in transit), an open 5 x 5 x 1 board
with z periodic unless said. The expected integers, written down before
the first run (the physicist's DESIGN.md, test (a), and the
mathematician's counterexample):

- (a) bit-exactness: the two built-in columns equal the push form as
  landed on 2026-09-20 (`M_A x (rho_A rho_B - 1) x V_B`, the electric
  part `sign x by_clock(age, |V n_A n_B M_A|, d_A d_B)`) integer by
  integer and refusal by refusal on the grid V in -5 .. 5 (three axes
  with different signs), M_A 0 .. 3, n_A and n_B in -2 .. 2, d_A and d_B
  in 1 .. 3, the age 0 .. 4 (49 500 cases, on the reduced and on the
  unreduced pair alike) and on 3 000 random cases at the register's
  scale (V to 2^62, M_A to 2^40, n and d to 2^30 - 1, the age to 2^31:
  the unreduced pair refuses with the landed form; the frame's reduced
  pair refuses a charge rho_A M_A beyond the register on its own and
  otherwise at most where the landed form refused, the same integers
  where both accept); and the replay of the six series 7 worlds: every
  `read` record's push equals the landed form recomputed from the record
  alone (its `reading` is V, the fixed reader's declared amount M_A, the
  tick its age), every record compared and none unequal.
- (b) the third column: the families `a` (charge [1, 2], strong [3, 2])
  and `b` (charge 2, strong 1) under `"strong": {"sign": -1}`; a reader
  of `a` of amount 1 (M 1, Q 1/2, G 3/2) met by one `b` ray of amount 1
  on (1, 1, 0) (u = (45, 45, 0)) reads (-67, -67, 0) at tick 1 (the
  reader's clock age 0; the ray at (2, 1, 0) with the age 1) and (-68,
  -68, 0) at tick 2 (the clock age 1; the ray at (1, 1, 0) with the age
  3): gravity -45, charge +45, strong -by_clock(clock age, 135, 2)
  (re-pinned on 2026-09-20 for the four unifications (4), the columns
  floored at the clock age like every other rate, from (-68, -68, 0) then
  (-67, -67, 0) at the age after the frame's advance); a reader of `c`
  (charge 1, strong [4, 3]) of amount 6 (M 6, Q 6, G 8): a `b` ray of
  amount 1 on +x (-128, 0, 0), an `a` ray of amount 1 on +x (-960, 0, 0),
  an `a` ray of amount 3 on -x (2880, 0, 0); a reader of `d` (charge 0,
  no strong value) met by a `b` ray on +x (-64, 0, 0); with the sign +1
  the same cases read (67, 67, 0), (68, 68, 0), (896, 0, 0), (576, 0, 0),
  (-1728, 0, 0); a third declared column `extra` (sign +1, the value 1 on
  `a` and `b`) adds +45 per axis: (-22, -22, 0) and (-23, -23, 0); a
  reader of `q` (charge [1, 2]) of content 3 met by a `b` ray on the
  diagonal reads (0, 0, 0) at both ages (the landed parity case, -135 +
  135); the reader of `c` reports the charges gravity [6, 1], charge
  [6, 1], strong [8, 1]; two fixed bodies at mirror Nodes of a bar of 4,
  `p` (content 3) at x = 0 and `q` (content 5) at x = 3, both families
  with the charge [1, 3] and the strong value [2, 3], releasing at
  `release` [1, 1] toward each other, read from tick 6 (three Links at
  the age 5) equal and opposite pushes at every tick, on `p` 960 -
  by_clock(tick, 320, 3) + by_clock(tick, 1280, 3), and `pushed` equal
  and opposite after 12 intervals; `run.json` carries `hypotheses`
  ["columns-v1"], `columns` [gravity -1, charge 1, strong -1], per family
  the aligned columns and per measured event `charges`; without a
  declared column `hypotheses` [] and two columns; with `action` 64 the
  identities are ["bohr-v1", "columns-v1"].
- (c) the refusals, naming the key: a `sign` 0, 2, "-1" or true; a
  column named `gravity`; `charge` declared as the key and under
  `columns`; `columns.charge` with the sign -1 (with the sign 1 accepted
  as the family's charge [3, 4]); a nonzero value on a paid family (0
  accepted, the values ((1, 1), (0, 1), (0, 1))); one name with two signs
  on two families; a value [1, 0], 1.5 or "1/2"; a column object with
  the key `range` or without `sign`; `columns` a list; seven declared
  columns (nine in all); accepted: a family without a declared column
  carries [0, 1] there (`Column("s", (0, 1), -1)`), the world's order is
  gravity, charge, then the names as first declared (`s`, then `t`).
- (d) the bounds: at parsing a reader of content 2^40 met by a family
  with the strong value 2^20 on both (|E n| = 2^80) is refused naming
  `measured[0]`, the column `strong` and the family `b`; a reader of
  content 2^30 with the strong value 1 met by a family of content 2^25
  released on one heading at `release` [1, 1] (gravity 2^30 x 2^31 = 2^61,
  strong the same, the sum 2^62 + 2) is refused naming the sum
  4611686018427387906 and accepted without the family's strong value;
  at the push `push_form` refuses |V| x |E n| = 64 x 2^56 in the column
  `strong` naming the measured event and the column, accepts the gravity
  product 64 x (2^56 - 2) = 2^62 - 128 as the push -(2^62 - 128), and
  refuses two such columns whose partial sum passes the bound naming the
  push.
- (e) the order of flooring: a reader of content 1 met by one free unit
  on a heading (V = 64), rho_A = [1, 3], rho_B = [1, 1]: per column -64 +
  by_clock(age, 64, 3) = -43, -43, -42, -43 at the ages 0 .. 3, the sum
  -128 / 3 floored once -42, -43, -43, -42; on the engine (four `b` rays
  of amount 1 on +x, two at (1, 2, 0) with the ages 0 and 1, two at
  (0, 2, 0) with the ages 0 and 1, arriving one per tick) the reader's
  clock ages 0 .. 3 (the ticks 1 .. 4) read -43, -43, -42, -43, the
  per-column list itself (re-pinned on 2026-09-20 for the four
  unifications (4) from -43, -42, -43, -43 at the ages after the frame's
  advance, 1 .. 4).

## The lifetime and the held content

`tests/test_lifetime.py` (docs/BEAM_LAW.md, section 2, section 3 step 6,
section 5 and section 10 note 31 (vii) and (viii); the model owner,
2026-09-20, "the strong force's range is a lifetime, L: the event whose
age reaches L makes no next event but an escape click in the ledger, as
at an open face"; the physicist's D-1, a measured event holding content
of several families). K 2^20, N 64, `suspension` 0, every family without
a phase circle unless said. The expected integers, written down before
the first run:

- (b) the lifetime click: a lone ray of the free family `s` (lifetime 3)
  on +x from (2, 2, 2) on an open 7^3 GameBoard at `release` [0, 1] is at
  (3, 2, 2) at the ages 1 and 2 (the heading steps at the ages 0, 2, 4,
  ...) and at (4, 2, 2) at the age 3, booked at the end of tick 3: the
  store empty, the border's escaped amount 1, momentum (64, 0, 0),
  content 0, one click record (tick 3, node (4, 2, 2), detector
  `lifetime`, measured None, family `s`, number 1, amount 1, phase 0,
  momentum [64, 0, 0], content 0), the border's record 67 108 864 (2^26,
  (32 x 256)^2 for one unit at phase 0), the books closed at every tick
  (the escaped line 1, the momentum line (64, 0, 0) escaped),
  `face_detectors()` ending with the border (`nodes` 0), `detectors()`
  ending `face:-z`, `lifetime`, the run's record listing the border after
  the faces, `lifetime` 3, 3, None per family, `columns-v1` under
  `hypotheses` and the escaped line {family s, amount 1, content 0,
  momentum [64, 0, 0]}; a ray of amount 5 of the paid family `light`
  (quantum 2) with the lifetime 3: escaped content 10 and momentum
  (640, 0, 0) on the border, the books' escaped content 10; a ray that
  arrives at a `read` Node (a reader of `m`, content 1, at (4, 2, 2)) at
  the age 3 is read (the push (-64, 0, 0), the record `read` before
  `click` at tick 3) and then booked; the same world without lifetimes
  keeps the ray (age 4 at (4, 2, 2) after tick 4, no record, `hypotheses`
  []).
- (c) the reach on the flight table: the 26 directions (the six headings,
  the twelve face diagonals, the eight cube diagonals) from a source of
  content 1 at the centre of a 9^3 GameBoard, one row per direction per
  interval (`release` [1, 1]), read by fixed probes of content 1 of a paid
  family (gravity alone: the push -V) at (5, 4, 4), (5, 5, 4), (5, 5, 5)
  and (6, 4, 4): with the lifetime 1 the six neighbours alone are
  reached, (5, 4, 4) reading 9 lines at every tick from 2 (the heading
  and the eight diagonals whose first step is x), the push (-392, 0, 0)
  = -(64 + 4 x 45 + 4 x 37); with 2 the face diagonals too, (5, 5, 4)
  reading 3 lines from tick 3 ((1, 1, 0), (1, 1, 1) and (1, 1, -1) at
  their second step), the push (-119, -119, 0); with 3 the cube diagonals
  and the second Link, (5, 5, 5) reading the (1, 1, 1) line at tick 4 with
  (-37, -37, -37) and (6, 4, 4) the heading at tick 4 with (-64, 0, 0);
  26 rows click on the border at every tick from L + 1 on (78 after four
  ticks at L = 1, the border's amount 26 after four ticks at L = 3), and
  no row of the family carries an age at or beyond L after any tick.
- (d) the inverse interval is refused on a GameBoard with a family of a
  lifetime, naming the family and its lifetime ("refused with the family
  's' of lifetime 3").
- (e) the refusals, naming the key: `lifetime` 0, -1, 1.5, "3" (an
  integer from 1), [3, 3, 3] (one integer, a scalar), 11 with
  `age_bound` 10 (beyond the age bound; 10 accepted); a declared ray of
  the family with the age 3 at the lifetime 3 (the age 2 accepted); a
  detector named `lifetime`; `held` naming the event's own family, an
  unknown family, a content 0 or 1.5, or not an object; a held total
  breaking the phase-turn bound (K 16, N 64: 300 + 300 >= 512). The held
  content: a measured event of `a` (charge [1, 2], strong [3, 2]) of
  amount 4 holding `b` (charge 2, strong 1) 2 reads the charges gravity
  (6, 1), charge (6, 1), strong (8, 1) (the reader `c` of
  `tests/test_columns.py` (b) built from two families) and the push
  (-128, 0, 0) from a `b` ray of amount 1 on +x at tick 1, releases both
  families at the world's rate (rows of amount 4 of `a` and 2 of `b` per
  direction per self-creation at `release` [1, 1]; released after two
  ticks 8 of `a` and 6 of `b`, an emitter of `b` adding 1 per tick),
  reports `held` [4, 2], the content 6 and the `charges` by name in the
  run's record, counts under the owners of `b` (`owners(1)` = (1, 2)),
  and the books balance; the register's proton, 1836 of `p` (charge 4)
  holding one unit of `nuclear` (strong 10000, lifetime 3), reads the
  charges (1837, 1), (7344, 1), (10000, 1), and `hypotheses`
  ["columns-v1"].

## The contact through the table

`tests/test_contact.py` (docs/BEAM_LAW.md, section 3 step 5 and section 10
note 31 (ix); the model owner, 2026-09-20, on the physicist's design of
the strong force, section 4.4): a body whose step on an axis is refused
because the destination holds another measured event has arrived at that
occupant, and the occupant's table entry for the body's family decides
as it decides for a ray: `measure` hands the body's momentum component
on that axis to the occupant, `rerelease` returns it, `read` and `pass`
leave the labels as they were; `measure` where the entry is the keys'
own rule for the body's family, declared or not (a paid arrival, the
body's momentum its own label; `read` accumulates only where declared
against the keys, on a paid family). K 2^20, N 64,
`suspension` 0, `width` 1, every family without a phase circle. The
expected integers, written down before the first run (the physicist's
DESIGN.md test (f) and section 4.4):

- (a) the pair on the six headings: two protons of `p` (amount 4, charge
  3) holding one unit of `g` (strong 11 with the sign minus, lifetime 3),
  the charges Q 12, G 11 and the content M 5, at one Link on an open 9^3
  GameBoard, `release` [1, 1]: from tick 2 each reads per interval the
  `p` row of amount 4 as -7936 (gravity +1280, electric -9216) and the
  `g` row as +8064 (gravity +320, strong +7744), the push +128 toward the
  other, (Q^2 - G^2 - M^2) x (-64); under the contact and the step drive
  (2026-09-20, [below](#the-step-drive): D = 320 + |p| on the content 5,
  the drive gaining p at every self-creation, signed since record 126,
  one sign here) the momentum of p1 over
  ticks 2 .. 8 reads 128, 256, 0, 0, 128, 0, 128 (the mirror on p2): p1's
  drive 128, 384, 768 >= 704 fires at tick 4 and hands 384; p2's drive
  128, 384, then nothing at tick 4 (its label 0 at its turn), 512 >= 448
  at tick 5, when it hands -128 back; the hand-overs over 30 intervals at
  ticks 4 (384), 5 (-128), 7 (256), 9 (-256), 10 (128), 13 (384), 14
  (-128), 16 (256), 18 (-256), 19 (128), 22 (384), 23 (-128), 24 (128),
  27 (384), 28 (-128) and 30 (256), each a `contact` record (the family
  `p`, the rule `measure`, the axis 0; p1's from (3, 4, 4) to (4, 4, 4)
  and p2's the other way), 10 by p1 and 6 by p2 (p2's `contacts` [10, 0],
  p1's [6, 0]), no step in 30 intervals, the largest component 384 (after
  a tick no label is beyond 256), the sum of the two momenta 0 after
  every tick, the books balanced. The rule as it was (the count off the
  clock, registered on 2026-09-20 and kept as history): the labels 128,
  0, 0, 128, 256, 384, 512, the hand-overs at ticks 3 (256), 4 (128), 9
  (640), 13 (512), 14 (128), 16 (256), 18 (256), 21 (384), 23, 25, 27
  (256), 28 (128) and 30 (256), all by p1, the largest 640, p2's
  `contacts` [13, 0]. With `read` declared for `p` on both, the keys' own
  rule, the same hand-overs (384 at tick 4 in four intervals); with
  `pass` declared the `p` rows are passed too and the `g` rows alone
  push, 8064 x (tick - 1). At three Links (x 2 and x 5) no `g` row
  reaches either body (the border takes it at the age 3), the `p` row's
  -7936 is read at ticks 6 and 7 (at tick 6 the drive 7936 is below D =
  8256 and the body stands), and at tick 7 p1 steps to x 1 with (-15872,
  0, 0) and p2 to x 6 with (15872, 0, 0), the drive 23808 - 16192 = 7616
  on the `step` line with the momentum's sign, -7616 and +7616 (the
  signed drive of record 126; the rule as it was stepped them at tick 6
  with 7936): the pair separates, no contact.
- (b) the isolated hand-over (`release` [0, 1], no rays): p1 of `p`,
  content 5, momentum (256, 0, 0) at (1, 2, 2) and p2 of `q`, content 5,
  fixed, at (2, 2, 2) on an open 5^3 GameBoard: the step rule fires at
  tick 3 (`by_clock(2, 256, 576)` = 1) and is refused; under `measure`
  (the default) p1 reads (0, 0, 0) and p2 (256, 0, 0), one `contact`
  record {tick 3, number 1, node (1, 2, 2), to (2, 2, 2), occupant 2,
  family `p`, rule `measure`, axis 0, component 256, momentum (0, 0, 0)},
  p2's `contacts` [1, 0], the books' measured momentum line (256, 0, 0)
  before and after; under `rerelease` p1 (-256, 0, 0) and p2 (512, 0, 0),
  the component 512; under `pass` both unchanged, no record, the step
  counted (p1's `steps` 1); an entry that declares no rule (`{"reads":
  "scalar"}`) or the keys' own rule (`{"p": "read"}`) leaves the default;
  a body of the paid family `h` (quantum 1, content 5, the same momentum)
  hands 256 by the keys (`measure`, the record naming `h`) and keeps it
  under `read` declared against the keys and under `pass`; the parser
  derives `contact` ("measure", "measure", "measure") from an empty
  table and from `{"p": "read"}`, ("measure", "measure", "read") from
  `{"h": "read"}` and ("pass", "measure", "measure") from `{"p": "pass"}`.
- (c) the apportioning: a body of span [1, 3, 1] (content 5, momentum
  (300, 0, 0) at (1, 2, 2)) whose destination set holds q1 (content 1)
  at (2, 1, 2) and q2 (content 3) at (2, 3, 2): 75 to q1 and 225 to q2,
  the body 0, two records; with 301, 75 and 226 (the unit left to the
  largest remainder); with q1 declaring `pass` for the body's family q1
  takes nothing and the body keeps its 75; a body of span [1, 3, 1]
  against one occupant of content 4 hands it the whole 300.
- (d) the register's pair: a proton (1836 of `p`, charge 4, holding one
  unit of `nuclear`, strong 10000 with the sign minus, lifetime 3) and a
  neutron (1839 of `n` holding one unit of `nuclear`) at one Link on an
  open 5^3 GameBoard, both releasing on the 290 primitive directions with
  |a| + |b| + |c| <= 6, `release` [1, 1]: the pushes on the proton per
  interval 10 161 754 944 from the neutron's `n` rows (1837 x 1839 x
  3008, the x components of the 57 unit vectors whose first step is -x
  summing to 3008) and 300 805 525 696 from its `nuclear` rows (10000 x
  10000 x 3008 + 1837 x 3008), the sum 310 967 280 640; on the neutron
  10 161 745 920 (1840 x 1836 x 3008) and 300 805 534 720 (300 800 000
  000 + 1840 x 3008), the same sum, the mirror; under the contact and
  the step drive the labels after 1000 intervals (0, 0, 0) and (0, 0, 0),
  998 hand-overs by the proton at the ticks 3 to 1000 (its drive of one
  interval's push is below D = 64 x 1836 + |p| at tick 2 and at or beyond
  it at tick 3 and at every interval after), the first of two intervals'
  pushes, 621 934 561 280, the largest, every later one 310 967 280 640,
  the neutron never handing (its label 0 at its turn), no step, the books
  balanced at every tick (the rule as it was: 999 hand-overs from tick 2,
  the largest one interval's push); with `pass` declared on each for the
  other's family (that family's rows passed too, the `nuclear` rows alone
  read) the labels after 40 intervals 39 x 300 805 525 696 =
  11 731 415 502 144 on the proton and -39 x 300 805 534 720 =
  -11 731 415 854 080 on the neutron, no record.
- (e) the frame's order, a declared tie (the closing gate's genericity
  probe, 2026-09-20, G1): two phase-less free bodies of content 1 at
  (2, 1, 1) with momentum (64, 0, 0) and at (3, 1, 1) with (-192, 0, 0),
  `width` 1, `release` [0, 1], four intervals on an open 6 x 3 x 3
  GameBoard (three until the step drive). Declared in that order (a is 1,
  b is 2): at tick 2 a steps onto b (its drive 64, 128 >= D = 128) and
  hands 64 (a 0, b -128), then b steps onto a (its drive 192, then 320 >=
  D = 192 with the -128 it holds) and hands -128 (b 0, a -128), and a
  steps to (1, 1, 1) at tick 4 (its drive 128 of D = 192 at tick 3, 256
  at tick 4): a ends at (1, 1, 1) with (-128, 0, 0), b at (3, 1, 1) with
  0, two `contact` records at tick 2. Declared the other way round (b is
  1, a is 2): b steps onto a and hands -192 (b 0, a -128), one `contact`;
  a's drive +64 from its own momentum is cancelled to -64 by the -128 it
  now holds at tick 2 (the signed drive, record 126), reaches -192 = -D
  at tick 3, when a steps to (1, 1, 1), and is -128 at tick 4: a ends at
  (1, 1, 1) with (-128, 0, 0). The sum of the momenta is (-128, 0, 0)
  and the books balanced in both; the holder and the positions follow
  the declaration order. History: the unsigned drive (the first form of
  2026-09-20) stepped a at ticks 2 and 4 in the second order, to (0, 1,
  1); the rule as it was (the count off the clock) at tick 3 in the first
  order and at ticks 2 and 3 in the second.

## The re-emission

`tests/test_nature_beam_reemission.py` (docs/BEAM_LAW.md, section 5). K 2^20,
`suspension` 0, `release` [0, 1], the families `m` (free) and `light`
(paid).

- (a) one ray of amount 3 (content 1 per unit, phase 20) into a `rerelease`
  Node of `m` (content 4) with the three directions +X, (1, 1, 0) and
  (2, 1, 0): three rays of amount 1 at the Node after the interval, one per
  direction, phase 20, age 0, the re-emitter's number 1, content 1; the
  push (192, 0, 0) taken, the recoil -(1 x (64, 0, 0) + 1 x (45, 45, 0) +
  1 x (57, 29, 0)) = (-166, -74, 0), the momentum (26, -74, 0) (re-pinned
  on 2026-09-19 for the label along the unit vector from (3, 0, 0),
  (-4, -2, 0) and (-1, -2, 0)); the books closed (absorbed 3, released 3;
  the content line absorbed 3, released 3); a ray of amount 4 on the same
  Node: 2, 1, 1 (the leftover to the direction `age mod 3` = 0, the
  first), the push (256, 0, 0), the recoil (-230, -74, 0), the momentum
  (26, -74, 0).
- (b) the face click (re-pinned from `test_border_and_clock_corrections`
  (b)): a ray of amount 1, phase 5, content 1 at (2, 0, 0) on +X of a
  3 x 1 x 1 bar steps off the GameBoard at the first interval: one `click` on
  `face:+x` (tick 1, Node (2, 0, 0), `measured` None, number 1, amount 1,
  phase 5, momentum (64, 0, 0) [was (1, 0, 0)], content 1), the escaped
  amount 1, the face's record 32^2 x (C[5]^2 + S[5]^2), the books' escaped
  lines the faces' sums; the same bar with {"x": "periodic"}: no click,
  the ray at x = 0; a measured event of `m` (content 16, momentum
  (1024, 0, 0) [was (16, 0, 0)]: one unit of net flow in label units) at
  x = 2 steps off at interval 2: one `click` on `face:+x` with `measured`
  1, amount 16, phase 2 (K 16), momentum (1024, 0, 0), `held` [16, 0],
  `home` [0, 0], the measured line's escaped 16.
- (c) home: a lamp's ray (content 1, phase 7) returning to its lamp on a
  periodic 4 x 1 x 1 bar is home after 4 Links (the intervals 7, 14, ...)
  and leaves again on the lamp's one direction with phase 7 and content 1,
  the books closed.

## The clock under the Beam Law

`tests/test_nature_beam_clock.py` (docs/BEAM_LAW.md, section 3, step 5; re-pinned
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
  content 37, its momentum (-768, 0, 0) (the labels 4 x 64 and 8 x 64
  along +X and -X; re-pinned on 2026-09-19 for the label along the unit
  vector from (-12, 0, 0); A's recoil (-2048, 0, 0) and B's (4096, 0, 0),
  from (-32, 0, 0) and (64, 0, 0)), each click record with `content` 4 or
  8, 10 rays in flight carrying 60, the books balanced; a lamp of turn 0
  releases nothing.
- (d) the step: content 16 with momentum 1024 (16 x 64, one unit of net
  flow in label units; was 16) on +x steps once per two self-creations
  (three after six intervals); with momentum 64 (was 1) none after 16 and
  one after 17; the momentum untouched; a step onto a Node that holds a
  measured event is refused and, since 2026-09-20, is a contact read
  through the occupant's table (`measure` by the keys; [the contact](#the-contact-through-the-table)):
  on a bar of 3 x 1 x 1 the mover's step of interval 2 onto the resident
  hands it the 1024 (one `contact` record, the mover's momentum 0 and
  its step counted), the resident's drive is 1024 at that interval and
  2048 = D at the next (the step drive, 2026-09-20), so it steps to x = 2
  at interval 3 with the 1024 and leaves through face:+x at interval 5
  (the escaped momentum (1024, 0, 0), the measured line 16 after), the
  mover at x = 0 with one step for the rest (the rule as it was, the
  count off the clock, stepped the resident in the interval of the
  hand-over, 2, and out at 4; until 2026-09-20 both remained with their
  momenta, the mover's steps counted at 2, 4 and 6).
- (e) the count off the clock: a source of `m` of content k at x = 0 of a
  2 x 1 x 1 bar releasing k rays per direction per self-creation at
  `release` [1, 1] and a probe of `light` (content 1, measuring `m`) at
  x = 1 at `suspension` [1, 4]: the probe reads the presence k every
  interval from the second on, and with k = 1 owes `by_clock(age, 1, 4)`,
  1 at the self-creations from the ages 3, 7, 11, 15: its age after
  intervals 1 to 20 is 1, 2, 3, 4, 4, 5, 6, 7, 8, 8, 9, 10, 11, 12, 12, 13,
  14, 15, 16, 16; with k = 8 it owes 2 at every self-creation: 1, 2, 2, 2,
  3, 3, 3, 4, 4, 4.
- (f) every age against a key is the one `by_clock` (the four
  unifications, the model owner, 2026-09-20, (2); BEAM_LAW note 33; the
  integers written first): the clock's rate `K` as a pair equal to its
  integer: the world of (b) with `"K": [1, 2]` turns 1, 3, 4, 6 as with
  `K` 2 and its snapshot after ten intervals is the same, the record
  carrying `K` as declared (2, and [1, 2] as the pair); the pair [3, 8] on
  the content 3 (the turn `by_clock(age, 9, 8)`) turns 1, 2, 3, 4, 5, 6,
  7, 9 over eight intervals, `world.turn(7, 3)` = 2; the static bound at
  the rate: the content 86 at [3, 8] is refused (2 x 86 x 3 = 516 >= 8 x
  64), 85 is accepted (the turn 31); the frame's refusal at half the
  circle kept: the content 63 at [1, 2] passes the parser (126 < 128) and
  is refused at the second interval (the turn `by_clock(1, 63, 2)` = 32);
  `K` 0, [0, 8], [3, 0], "8" and [1, 2, 3] are refused naming `K`;
  `by_clock_rows` over the ages 0 to 9 at 3 / 10 is `by_clock`'s 0, 0, 0,
  1, 0, 0, 1, 0, 0, 1, and with a numerator per row; `ages_at_key`
  (`by_clock(age - 1, 1, key)` = 1 for a walked row): the ages 0, 1, 2, 3,
  4, 6 against the key 3 read no, no, no, yes, no, yes, against 1 every
  age from 1, against 4 the age 4 and not 3; on the GameBoard a family of
  lifetime 3 with a row at rest (the direction index 0) at the age 2 and a
  moving row at the age 0 (7^3, open, no measured event): the moving row
  clicks on the border at the third interval at (3, 3, 3) with the age 3,
  the rest row keeps the age 2 for twenty intervals and never clicks; a
  family without a lifetime under `age_bound` 3: the fourth interval's
  walk (the age 3 to 4) refuses the run naming the bound, the third does
  not.

## The width of the push

`tests/test_push_width.py` (docs/BEAM_LAW.md, section 3, step 5 and
implementation note 15; the model owner's D1, 2026-09-19). One rule in
isolation: an open bar of 12 x 1 x 1, K 1024, N 64, `release` [0, 1] (no
push arrives), a free measured event of content M with the momentum p on
+x; the step rule `by_clock(age, |p|, Q x S x M + |p|)` with S the
world's `width` and Q = 64 the label's scale (since 2026-09-19, the label
along the unit vector, [BEAM_LAW note 23](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation):
the declared momenta below are the first pins times 64 and every position
is unchanged, `by_clock(age, Q n, Q k) = by_clock(age, n, k)`). The
expected integers, written down before the first run:

- (a) S = 1 reads exactly as the rule was: content 16 with momentum 1024
  (was 16) from x = 4 steps at the ages 2, 4, 6 (x after intervals 1 to 6:
  4, 5, 5, 6, 6, 7; `steps` 0, 1, 1, 2, 2, 3), with `width` 1 declared and
  with the key absent alike; with momentum 64 (was 1) none after 16
  intervals and one after 17.
- (b) S = 8 with p = Q M: content 16 with momentum 1024 steps once per 9
  self-creations, at the ages 9, 18, 27 (x 4 through interval 8, 5 from 9,
  6 from 18, 7 at 27; `steps` 0, 1, 2, 3); content 3 with momentum 192
  (was 3) steps at the same ages (the speed a unit of flow gives,
  1 / (S + 1), is the same for every content).
- (c) off the clock, no remainder: the probe of (b) at x = 3 with
  `suspension` [1, 4] and a crowd of 4 rays of another number (a fixed
  anchor of content 1 at x = 11) at rest on x = 3 to 7 owes one interval
  after every self-creation (age after interval n is ceil(n / 2), waited
  floor(n / 2)); the step of the ages 9, 18, 27 lands on the interval that
  pays the count (a measured event steps only in an interval where it owes
  nothing), the intervals 18, 36, 54: x after intervals 17, 18, 35, 36,
  53, 54, 60 is 3, 4, 4, 5, 5, 6, 6; age 30, waited 30, `steps` 3 after
  60; after every paying interval `steps` = age x 1024 // 9216 (= age x 16
  // 144) and after every self-creation (age - 1) x 16 // 144; the momentum
  (1024, 0, 0) untouched; the books
  balanced at every interval. (The first run corrected the interval of the
  step from 17 to 18: the order of the frame, not the rule.)
- (d) a world without `width` parses to 1; `width` 8 parses to 8 and the
  runner's `run.json` carries `width` 8; 0, -1, `"8"` and 1.5 are refused
  with "width must be an integer from 1".

Since the step drive (2026-09-20, below) the remainder of the division
`age x |p| / D` is kept on the body's record as `drive`; every integer of
(a) to (d) is unchanged, the identity the step drive's test (a) proves.

## The step drive

`tests/test_step_drive.py` (docs/BEAM_LAW.md section 3 step 5 and note 17
as amended on 2026-09-20; the physicist's design RULES.md section 1 (docs/designs/hubble_stars/ on branch `claude/series-g2-stars`);
the model owner on series G2's finding, "1 and 2 are very important for a
solution and a new run"; record 107 the findings, record 108 the owner's
decision).
The count of Links a free measured event has made on an axis is the whole
part of the SIGNED distance its momentum has driven: one bounded integer
per axis on its record, `drive += p` at every self-creation in which it
may step, on every axis, a step on the + side and `drive -= D` when
`drive >= D`, a step on the - side and `drive += D` when `drive <= -D`,
D = Q x S x M + |p| (the signed drive of record 126, 2026-09-20; the
first form accumulated |p| and took the direction from the sign at the
fire, a defect under a reversal); at most one Link per interval, x
before y before z, as before: a
later axis whose drive reaches its D in the interval of an earlier axis's
step loses that Link (its D subtracted, nothing carried, the rule's count
on the axis, `axis_steps`, raised as the count off the clock was). The
expected integers, written down before the first run:

- (a) the identity at a constant momentum: over 4000 self-creations, for
  p in {1, 7, 64, 1000, 1024, 4095, 9215} at D = 9216 (content 16, width
  8) and p in {1, 5, 63, 64, 127} at content 1 and width 1, the drive
  fires exactly where `by_clock(n - 1, |p|, D)` is 1 and the drive after
  the n-th self-creation is n x |p| mod D; the negative momentum the same
  with the sign -1 and the drive -(n x |p| mod D); the count primitive
  `core.integer.by_drive` (record 108) the same identity over 400
  self-creations, at the rate 7 against 3 a count of 1 at every
  self-creation with the drive 30 x 4 after 30 and at -7 a count of -1
  with the drive -120 (the primitive's count is -1, 0 or 1; below the
  denominator it is `by_clock`'s with the sign), a denominator of 0
  refused;
  `test_push_width` (a) to (c) unchanged. On two axes
  (the physics-rule review's counterexample): content 16, width 1,
  momentum (1024, 320, 0) from (4, 4, 0), D = (2048, 1344): x steps at
  the even self-creations, y at 5, 9, 13, 17, 21 (y's drive after n
  self-creations 320 n mod 1344: 1600 >= 1344 at n = 5, then 1536, 1472,
  1408, 1344 at 9, 13, 17, 21), the body at (16, 9, 0) after 24 with
  `axis_steps` [12, 5, 0] and `steps` 17, the drives (0, 960, 0); and the
  coincidence: content 1, width 1, momentum (64, 64, 0),
  D = 128 on both, both rules fire at the even self-creations, x steps
  and y loses every one: after 10 intervals x has moved 5 and y 0,
  `axis_steps` [5, 5, 0], `steps` 5, the drives (0, 0, 0), the same
  positions as `by_clock` on each axis with the coincidence lost.
- (b) the integrated distance: content 16, width 8, the momentum halved
  from outside after every 50th interval from 4096 down to 32; after 400
  intervals the body has made the Links of its integrated speed, the sum
  over the intervals of |p| / (Q x S x M + |p|) = 38.0, within 1 (37 to
  39, by the drives at the two ends), where the rule as it was made
  floor(400 x 32 / 8224) = 1; no stall longer than 257 intervals
  (ceil(8224 / 32)), the smallest momentum's own period; the drive within
  [0, D) after every interval (one sign: the signed drive never negative).
- (c) never two Links in one interval: content 3, width 4, a 41^3
  periodic cube with `age_bound` 64, the momentum on every axis drawn at
  every interval from `random.Random(20260920)` in [-(D - 1), D - 1] with
  Q x 4 x 3 = 768; over 10 000 intervals every step moves the body by
  exactly one Link on one axis, `steps` counts them (more than 1000),
  |drive| on every axis below 2 x 768 - 1 after every interval (the
  largest D of the draw: a residual earned at a larger momentum fires at
  the following self-creations, one Link each, never two in one).
- (d) the record: content 16, width 8, momentum 1024, 27 intervals through
  the runner: the steps at the ticks 9, 18, 27 with `drive` [0, 0, 0] on
  each `step` line (27 x 1024 = 3 x 9216), `run.json`'s measured state
  and `state.json` carrying `drive` [0, 0, 0] and `axis_steps` [3, 0, 0],
  `steps` 3; a measured event declaring `drive` refused with "unknown
  keys: drive".
- (e) the turn by momentum at a constant momentum: content 16, momentum
  320, `action` 7, phase 5: the turns at the first five Links 2925, 2926,
  2926, 2925, 2926 (mod 64) as `test_nature_beam_body` (d) pins, and
  `axis_steps` [5, 0, 0] after 24 intervals.
- (f) the signed drive under a reversal (record 126): content 16, width 8,
  D = 9216, the momentum +1024 for eight self-creations (the drive 8192,
  no Link) and -1024 from the ninth: the first form stepped -x at the
  ninth (8192 + 1024 = 9216); the signed drive reads 8192 - 1024 k and
  steps -x first at the twenty-fifth (8192 - 17 x 1024 = -9216), the body
  at x = 4 until then, its drive 0 after the step and -5120 after 30
  intervals, `steps` 1, `axis_steps` [1, 0, 0]; the primitive alone at
  8192 with the rate -1024 counts 0; the same body under +1024 for eight
  and 0 after keeps its drive 8192 and its Node.
- (g) the bound pair under a suspension holds (the Boss's W1 of record
  126): the register's `deuteron_1` under `amplitude` with `suspension`
  [1, 134217728], a paid family `light` and a lamp of it (content
  8388608, rate [1, 1], turns [8]) on +y beside the proton at (10, 11,
  10) and a control lamp at (10, 10, 16), each read by a `sum` set of one
  `counter` Node four Links up +y: over 3000 intervals no `step` record
  (the nucleons at (10, 10, 10) and (11, 10, 10) throughout), every
  attempted step a `contact` (their count the two bodies' `steps`), the
  books balanced; under the first form the same world holds for 2092
  intervals and the neutron steps to (12, 10, 10) at tick 2093 with a
  positive momentum (the physics-rule reviewer's measurement on main:
  the |p| accumulated toward the proton discharged away from it). The
  hold is the rule's consequence given the pair's symmetry (mirror
  pushes, a hand-over zeroing both, the neutron's signed drive never
  above 0), not a theorem for every pair.

## The reading's weight at the relative speed

`tests/test_doppler.py` (docs/BEAM_LAW.md section 3 step 4 and note 38;
the model owner's record 119; the mathematician's admissible form, FORM.md
section 6 of docs/designs/push_relative_speed/ on branch
`claude/series-m-masses`, record 110, and its grain and flux form GRAIN.md
after the physics-rule review of the first build; series G2's finding,
RULES.md section 2, record 107). Under the world key `doppler` a free
measured event reads the rows that arrived at its Node for the push with
each direction's label flow V_d weighted by the flux of its rows through
the body, (|G Q |v|^2 - T_d sum_a s_a w_a v_a|, G Q |v|^2), w_a = G |p_a|
// D_a the body's speed at the grain G = 2^12, D_a = Q S M + |p_a|, v the
direction's vector and T_d its resolution; V'_d = sign(V_d) x
by_clock(age_A, |V_d| x num_d, G Q |v|^2) per component, summed over the
directions, then the columns as today. The expected integers, written down
before the first run:

- (a) a fixed body reads byte-identically with and without the key on the
  bar of (b) over 200 intervals (the same records line by line, the same
  books, the same momentum and push taken, 12800 label units); a free body
  at rest whose push the charge column cancels (rho 1 on both families, no
  third column) the same, its push 0.
- (b) the bar of the finding: a fixed source at x = 0 on a bar of 400
  Nodes releasing one row per interval on +x, the steady beam declared in
  transit (the row of age tau at the Node m(tau) = (2 tau Q + 110) // 220),
  a free body of content 2^20 with `width` S and momentum p, reading the
  beam (`read`) with a third column `probe` (the value 1 on the beam, [1,
  2^20] on the body, the sign plus, the divisor 1) so that each read's push
  is the weighted flow itself, 64 label units per row: over 200 intervals
  the body reads 200 rows in every case (the finding) and takes, under the
  key, at rest (S 1, p 0) 12800; receding at 0.30 (S 7, p 3 x 2^26, D 10 x
  2^26, w 1228, the pair 127064 / 262144) 6204; receding at 0.45 (S 11, p
  9 x 2^26, w 1843, 59414 / 262144) 2901; approaching at 0.30 (S 7, p -3 x
  2^26, from x = 200, 397224 / 262144) 19395; co-moving at c = 32 / 55 (S
  23, p 2^31, w 2383, 14 / 262144: below one label unit per row) 0;
  outrunning at 0.75 (S 1, p 3 x 2^26, w 3072, 75776 / 262144, the
  absolute value) 3700; in rows 200, 96.94, 45.33, 303.05, 0, 57.81
  against FORM.md's map 200, 97, 45, 303, 0, 58 and its exact rates 96.9,
  45.3, 303.1, 0, 57.8; without the key 12800 in every case. The bar as
  posed, rows of amount 64: runs under the key, receding at 0.30 the push
  396673 (96.84 rows of 4096 units), within a row of the amount-1 line.
- (c) the third law on two fixed bodies (the mirror world of
  `test_columns.py` (b), `p` of content 3 and `q` of content 5 with the
  charge [1, 3] and the strong value [2, 3], `doppler` true): the same
  records as without the key, equal and opposite pushes at the ticks 6 to
  12, 960 - by_clock(tick - 1, 320, 3) + by_clock(tick - 1, 1280, 3) on
  `p`, the push taken opposite; `hypotheses` ["columns-v1", "doppler-v1"].
- (d) the refusals: `doppler` 1, "true", null or [true] refused "must be
  true or false"; `weighted_flow` on one +x label of 64 at the outrunning
  speed 0.75 of a body of content 2^20 at width 1 (w 3072, the pair 75776
  / 262144) gives 18 (by_clock(0, 64 x 75776, 262144)), on a label of 2^50
  at the same pair it is refused naming measured event 2, its Node and
  the direction 2 under doppler;
  `weighted_flow_factor` 3 on the six headings, 1 on a table of rest
  directions, 4 with (1, 1, 1); a free reader of content 2^30 releasing on
  -x met by a fixed source of content 2^25 releasing on +x (charge 0 on
  both) parses without the key (each budget 2^61) and is refused under it
  naming "x 3 the largest label flow ... times the largest weight of
  doppler".
- (e) `quantised_speed`: (1365, 1) at p 2^25 on a body of content 2^20 at
  width 1 (v = 1 / 3), (1183, 1) at p 26 x 2^20 (v = 26 / 90 = 0.28889,
  the G2 star's), (0, 0) at rest, (1365, -1) on -y, (1365, 1) for content 1
  at p 32; `flux_pair`: on +x (262144, 262144) at rest, (111994, 262144)
  at 1 / 3, on -x (262144 + 110 x 1365, 262144), on +y at a motion on x
  (262144, 262144); co-moving (S 23, p 2^31: w 2383) (14, 262144); on
  (1, 1, 0) (T 156) at 1 / 3 (311348, 524288) = 0.5938; on (1, 2, 0) (T
  247) at the star's speed (1018519, 1310720) = 0.7771; on (1, 3, 2) (T
  414) (3180254, 3670016) = 0.8666 (GRAIN.md section 2's flux against the
  per-axis form's 0.1875, -0.11 and -0.87); the flight table's resolutions
  110, 156, 247, 414. The record: `run.json` carries `doppler` true and
  `hypotheses` ["columns-v1", "doppler-v1"] on the bar. The gate set's
  fifteen worlds parse with `doppler` false and without the identity.
- (f) the fan over three intervals: a free reader of content 2^20 at
  (4, 6, 4) of a 9 x 12 x 9 open GameBoard with the three declared directions
  (1, 1, 0), (1, 2, 0), (1, 3, 2), the push the weighted flow as in (b);
  one row of amount 64 of the direction placed on the flight table's line
  to step into the reader's Node at each of the ticks 1, 2, 3 from number
  2; the reader's clock ages 0, 1, 2, its first step after the third
  reading (its drive fires at the third self-creation at 1 / 3, so it
  stands at (5, 6, 4) after the third interval, and at the fourth at 26 /
  90, still at (4, 6, 4)): on (1, 1, 0) at 1 / 3 (p 2^25) the sum of the
  pushes (5130, 5130, 0) of the flow (8640, 8640, 0); on (1, 2, 0) at 26 /
  90 (p 26 x 2^20) (4326, 8504, 0) of (5568, 10944, 0); on (1, 3, 2) at
  26 / 90 (2828, 8485, 5656) of (3264, 9792, 6528); on +x at 1 / 3 (5249,
  0, 0) of (12288, 0, 0); on +y at 1 / 3 (0, 12288, 0) exactly; the reader
  stays at (4, 6, 4) through the third reading; without the key the flow
  itself. The three fan directions together at 1 / 3, one row of each per
  interval in one group of number 2 (the reads of amount 192): (5130 +
  4135 + 2761, 5130 + 8128 + 8284, 5522), each direction's flow at its
  own pair ((1, 2, 0) at 1 / 3 the pair 973565 / 1310720 = 0.743, (1, 3,
  2) 3104906 / 3670016 = 0.846). The same fan reader at rest with rows of
  amount 1: the same records with and without the key over the three
  intervals, the pushes the flows (273, 459, 102) (the unit labels (45,
  45, 0), (29, 57, 0), (17, 51, 34) per read), its momentum after them
  below D / G = 16384 (it still reads as at rest); with rows of 64 the
  first two reads identical and the third apart, the momentum after two
  reads (11648, 19584, 4352) past D / G on y (w_y = 1, the grain): (5821,
  9788, 2175) against the flow (5824, 9792, 2176).
- (g) a body on a set: `span` [1, 1, 3] at (4, 0, 1) of an 8 x 1 x 3
  periodic bar, content 1, the momentum (32, 0, 0) (D = 96, w = 1365, the
  pair 111994 / 262144), met at tick 1 by one +x row of amount 1 at
  (4, 0, 0) from number 2 and one at (4, 0, 2) from number 3: two `read`
  lines, each pushing (-27, 0, 0) (by_clock(0, 64 x 111994, 262144); the
  live momentum after the first group, 5, w 296, would give 56), the
  momentum after the interval -22, the set (4, 0, 0), (4, 0, 1),
  (4, 0, 2); without the key -64 each.
- (h) the registered G2 star world
  `examples/events/hubble_stars/gravity_scalar.json` (the example's own
  path; the reviewer's temporary copy `tests/data/g2_gravity_scalar.json`
  was deleted when series G2 merged doppler-v1, MIGRATION: 24 free stars of
  content 2^22 + 4096 at width 2^20, one detector) parses with `doppler`
  true and the identity
  and runs 20 intervals without a refusal, its books balanced and a star
  pushed. Its table is the eight headings, where the flux equals the
  heading pair, so (h) is the stars' fit and not the fan's integers,
  which rest on (f); the temporary copy is gone since series G2's merge
  of doppler-v1 (one canonical copy per world).

## The age

`tests/test_nature_beam_age.py` (docs/BEAM_LAW.md, section 2 the age and its bound,
section 3 steps 2 and 5, section 10 note 25; the model owner, 2026-09-19,
"the clock beside a mass ... go for it"): the age is the count of intervals
since the measured event that created the ray, kept whole on the record;
the flight reads it modulo the direction's period and the collision never
reads it; a measured event, the external thing, reads it whole as the age
moment of the one reading (`reads: "age"`), which its clock counts in place
of the presence; the GameBoard's step is unchanged by the whole age.

- (a) the age whole: a ray on +x from x = 0 of an open 301 x 1 x 1 bar
  carries the age 200 after 200 intervals (200 mod 55 = 35 until
  2026-09-20) at x = m(200) = 116; a head-on pair at the ages 59 on an open
  9 x 1 x 1 bar (`age_bound` 128; x = 3 on +x, x = 5 on -x) meets at x = 4
  at the first interval with the ages 60, parks in the rest slots with the
  ages kept (60, 60), turns onto +z and -z at the second interval still at
  60, ages to 61 at the third without a step (m(61) = m(60) = 35) and,
  still meeting, turns onto +y and -y (the class cycle +z-z -> +y-y), then
  steps at the fourth (m(62) = 36) and clicks on the y faces; a ray of age
  59 met by a `rerelease` Node is created again at age 0 with the arriving
  phase 20 and the re-emitter's number 2; a release is born at age 0 (six
  rays).
- (b) the age moment: three rays of amounts 1, 2, 4 at the ages 3, 5, 7 on
  (1, 0, 0), (2, -1, 0), (1, 1, 1) read the age moment 3 + 10 + 28 = 41
  and the scalar 7; with a ray that did not step (amount 2, age 10) the
  here part is 20 and the whole 61; each of the 48 signed axis permutations
  leaves it 41 while rotating the flow; the keyed form over two Nodes reads
  82 and 41; without ages the moment is 0; an amount 2^40 at the age 2^23
  is refused with `OverflowError` before any product is formed and at
  2^22 - 1 accepted; `count_component` selects `age` for `age` and
  `scalar` for the five other keys.
- (c) the clock: a source of `m` (content 1) at x = 0 of an open 5 x 1 x 1
  bar at `release` [1, 1] and a fixed reader of `light` (content 1) at
  x = 3 whose entry for `m` reads `age`, `suspension` [1, 4]: a ray born at
  tick b is at x = 3 at the ages 5 and 6 (ticks b + 5 and b + 6), so from
  tick 7 the reader counts the age moment 5 + 6 = 11 over a presence of 2
  (at tick 6: 5 over 1) and owes `by_clock(age, 11, 4)` = 3, 3, 2, 3, 3 at
  the self-creations of the ages 6 through 10 (`by_clock(5, 5, 4)` = 1 at
  the age 5): its age after the intervals 1 to 24 is 1, 2, 3, 4, 5, 6, 6,
  7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 10, 10, 10, 10, 11, 11, its
  self-creations at the ticks 1 to 6, 8, 12, 16, 19, 23 with (presence,
  counted) = (1, 5) at tick 6 and (2, 11) from tick 8; its 19 `read`
  records carry the reading 5 (the arrival's age moment); the same reader
  without the key counts the presence and owes `by_clock(age, 2, 4)`: 1,
  2, 3, 4, 5, 6, 7, 8, 8, 9, 10, 10, 11, 12, 12, 13, 14, 14, 15, 16, 16,
  17, 18, 18 (unchanged by the change), counted equal to the presence at
  every self-creation, its `read` records carrying the flow [1, 0, 0].
- (d) the parsing: `flight_bound` of an open 11^3 GameBoard over the six
  headings is 54 (D_M = 31 Links, ceil(31 x 110 / 64)) and 111 with the
  direction (1, 0, 64) declared (T 7095, one period, ceil(7095 / 64));
  `age_bound` defaults to twice it (108; 222 with that direction) and
  parses as declared (100); 0, -1, "8" and 1.5 are refused naming
  `age_bound`; a GameBoard periodic on every axis without it is refused
  naming `age_bound`, and accepted with 7; a declared ray's age 109 on the
  11^3 GameBoard is refused ("from 0 through 108") and 108 accepted; the
  runner's record carries `age_bound` 108; a ray on +z of an open
  3 x 1 x 1 bar with z periodic (the stub; default 12) carries the age 12
  after 12 intervals and its 13th interval is refused with `OverflowError`
  naming `age_bound 12`.
- (e) the GameBoard is unchanged by the whole age: 324 fixed rays on the
  periodic 8 x 8 x 4 GameBoard (`age_bound` 128; every heading, both rest
  slots, two fan directions, head-on pairs, ages up to 22, `phase_per_link`
  5) run 40 intervals with the ages whole, and again with every moving
  ray's age reduced modulo its direction's period after each interval from
  outside the law: the sorted (Node, direction, phase, amount, content)
  rows are identical at every interval, the ages' sums differ, and the
  collision moved rays on the way.

## A body on a set and the turn by momentum

`tests/test_nature_beam_body.py` (docs/BEAM_LAW.md, section 3 step 5 and section 10
note 30; the model owner, 2026-09-20, "On Bohr, go, and put it as
parameters outside the GameBoard like the age"): a measured event that
declares `span` is a body on the set of Nodes centred on its position,
one record on all of them; its threshold, its clock's count and its push
read the one reading set summed over its Nodes, its releases are
apportioned whole over them, the step moves the whole set, no collision
acts at any of its Nodes. A measured event that declares
`phase_by_momentum` in a world with `action` (h) turns its phase at every
Link it steps on an axis whose momentum component is p by the difference
of two floors of k x |p| x N / h, k the count of Links the step rule gives
at its age. Every rule is on the measured-event side; the rays' flight
and collision are untouched. K 2^20, N 64, `suspension` 0 and `release`
[0, 1] unless said, the families `m` (free) and `light` (paid). The
expected integers, written down before the first run:

- (a) a set of one Node is the measured event as it was, bit for bit: a
  free body of `m` (content 16, momentum [256, 0, 0], phase 5) at
  (3, 1, 1) of an open 12 x 3 x 3 GameBoard at `release` [1, 4] (4 rays per
  heading per self-creation), a fixed counter of `light` at (9, 1, 1)
  measuring `m` in the `wave` detector `d`, a head-on pair of number 2
  on +-y at x = 6 (the phases 3 and 40) that parks at (6, 1, 1) at the
  first interval and leaves on +-z; 30 intervals, the integers of the
  engine of 2026-09-20 before the change: the body's x per interval 3
  (4 times), 4 (5), 5 (5), 6 (5), 7 (5), 8 (6); the body at (8, 1, 1),
  age 30, phase 5, 6 steps, held [16, 0]; the counter held [0, 4], 99
  units clicked, momentum (-25344, 0, 0), the record 37348285440 at the
  phase 5; 152 clicks, 20 record lines, 5 steps and 5 homes (the body
  stepping onto its own +x ray in the same interval); 28, 28, 27, 27 and
  18 clicks on face:-z, face:+z, face:-y, face:+y and face:-x, 24 clicks
  and 20 record lines at `d`; the pair's clicks at tick 6 on face:-z
  (phase 40) and face:+z (phase 3); 25 rows of 101 units in the store;
  the transit line 2 + 740 = 101 + 522 + 119 with 74, 111, 111, 113,
  113 units through the faces -x, +y, -y, +z, -z; every record, every
  row and both states equal with `span` [1, 1, 1] declared.
- (b) a set of three Nodes: a fixed body of `light` (content 4) at
  (4, 0, 1) of an open 9 x 1 x 3 bar with `span` [1, 1, 3] (the Nodes
  (4, 0, 0), (4, 0, 1), (4, 0, 2), all held by number 1 in `at`)
  measuring `m` in the `wave` detector `d` of threshold 3 at
  `suspension` [1, 1]: three rays of `m` (number 2, amount 1, phase 0)
  arriving in one interval, one at each Node, are one set: 3 clicks (the
  events [3, 0], held [0, 4]: a free ray carries no content), the push
  (-768, 0, 0) = -4 x 3 x 64, one `record` line naming `d` with the
  record (3 x 32)^2 x 256^2 = 9 x 67108864 and every click line's `node`
  the body's position (4, 0, 1), the presence 3, the count 3, the owed
  count `by_clock(0, 3, 1)` = 3, the set's phase 0 returned; one ray at
  one of the Nodes passes with `threshold` 3 (since 2026-09-20 the
  threshold under `wave` reads the pointer's square: two rays in phase at
  two Nodes would read 4 and click), no click, no push, the row still in
  the store. The step: a free body of `m` (content 16,
  momentum [1024, 0, 0]) of span [1, 1, 3] at (2, 0, 1) of an open
  6 x 1 x 3 bar steps at the ages 2, 4, 6 with all three Nodes (x per
  interval 2, 3, 3, 4, 4, 5, 5; `at` holds its three Nodes and nothing
  else); with a fixed anchor at (5, 0, 0), a Node of the moved set at
  the age 6, the step is refused: x per interval 2, 3, 3, 4, 4, 4, three
  steps counted, `at` of four Nodes, and since 2026-09-20 the refusal is
  a contact, the body's 1024 handed to the anchor (its momentum 0, the
  anchor's (1024, 0, 0), the anchor's `contacts` [1, 0]); without it the step of the age 8
  leaves the GameBoard and the whole body clicks on face:+x (three `step`
  lines with the phase 0 before it, one click line with node (5, 0, 1),
  measured 1, amount 16; no measured event and no Node in `at` after;
  the measured line's escaped 16); with x periodic the body wraps to
  (0, 0, 1) with the Nodes (0, 0, 0), (0, 0, 1), (0, 0, 2); `body_nodes`
  of (2, 0, 0) with span (1, 1, 3) on a 6 x 1 x 3 bar with z periodic is
  ((2, 0, 2), (2, 0, 0), (2, 0, 1)) in that order, None with z open, and
  ((2, 0, 1),) for the span (1, 1, 1).
- (c) the books balance with a set that releases: a free body of `m`
  (content 16) of span [1, 1, 3] at (3, 1, 2) of an open 7 x 3 x 5 GameBoard
  at `release` [1, 4] on the four headings +-X, +-Y (no ray of its own
  enters its set): 4 units per heading per self-creation apportioned
  whole over the three Nodes, [2, 1, 1] at the age 0 (the leftover to
  the Node `age mod 3`), [1, 2, 1] at the age 1, [1, 1, 2] at the age 2:
  the rows born at the first interval sum to 8, 4, 4 units at (3, 1, 1),
  (3, 1, 2), (3, 1, 3), 16 released in 12 rows, at the second 4, 8, 4
  (32 released); the books balance at every one of 20 intervals and
  equal their recount; the body's momentum stays 0 (a free release takes
  no recoil). A lamp of `light` (content 24, K 24, rate [1, 1]) on +Y of
  span [3, 1, 1] at (1, 0, 0) of a 3 x 6 x 1 GameBoard releases its one unit
  per self-creation at the Nodes x = 0, 1, 2 in turn (the ages 0, 1, 2):
  after 3 intervals the rows (0, 1, 0) age 2 phase 0, (1, 1, 0) age 1
  phase 1, (2, 0, 0) age 0 phase 2 (content 1 each), held [0, 21], the
  recoil (0, -192, 0), the transit momentum (0, 192, 0), the books
  balanced.
- (d) the turn: a free body of `m` (content 16, phase 5, K 2^20: the
  clock's turn 0) with the momentum [1024, 0, 0] at x = 20 of an open
  40 x 1 x 1 bar steps at the ages 2, 4, 6, ... (k = age // 2, x = 20 +
  k): with `action` 65536 (|p| N / h = 1 per Link) its phase after the
  intervals 1 to 12 is 5 + tick // 2, 11 after 12, and at `release`
  [1, 16] on -X (away from its path) the rays born at tick 3 carry the
  phase 6 and those born at tick 2 the phase 5 (the release of an interval
  carries the phase before its step); with `action` 4096 (16 per Link)
  the phase after 12 intervals is (5 + 96) mod 64 = 37; with the momentum
  [320, 0, 0] and `action` 7 (`by_clock(k, 20480, 7)` = 2925, 2926, 2926,
  2925, 2926 for k = 0 .. 4: a remainder each step; the steps at the
  intervals 5, 9, 13, 17, 21, x = 21 .. 25) the phase after the intervals
  4, 5, 9, 13, 17, 21, 24 is 5, 50, 32, 14, 59, 41, 41 (the floors 2925,
  5851, 8777, 11702, 14628 of k x 20480 / 7 added to 5, mod 64);
  composed over axes, the momentum [1024, 320, 0] with `action` 65536
  from (4, 4, 0) on a 40 x 40 x 1 GameBoard (the x steps at the even ages,
  the y steps at 5, 9, 13, 17, 21, no step lost, the body at (16, 9, 0)
  after 24): the y turns floor(0.3125 k) - floor(0.3125 (k - 1)) = 0, 0,
  0, 1, 0, so the phase after 17 intervals is 5 + 8 + 1 = 14 and after
  24 it is 5 + 12 + 1 = 18; the same worlds without `action` keep the
  phase 5 at every interval.
- (e) the GameBoard is unchanged by the two keys: the 324 fixed rays of
  `light` of `test_nature_beam_age` (e) on the periodic 8 x 8 x 4 GameBoard (number
  1, an anchor of `light` at (7, 7, 3) their home) with a free body of
  `m` (content 16, phase 5, momentum [1024, 320, 0], span [1, 1, 3] at
  (0, 0, 0), `pass` for `light`, no release) run 40 intervals with
  `action` 7 and `phase_by_momentum` and again without them: the rays'
  sorted (Node, direction, phase, amount, content) rows are identical at
  every interval, the body's Nodes and steps are identical, its phase
  differs (and is 5 without the keys), the collision moved rays on the
  way and the body's presence read rays.
- (f) the refusals, naming the key: `action` 0, -1, "8" and 1.5 ("action
  must be an integer from 1"); `phase_by_momentum` without `action`
  ("needs the world's `action`"), on a fixed measured event ("refused on
  a fixed measured event"), on a family without a phase circle ("without
  a phase circle"), 1 ("must be true or false"); `span` "3" and [2, 1, 1]
  ("three odd integers"), [0, 1, 1] ("from 1 through 12"), [1, 5, 1] on
  an axis of 3 ("from 1 through 3"), a body of span [3, 1, 1] at x = 0 of
  an open axis ("leaves the GameBoard"), two bodies of span [3, 1, 1] at
  x = 4 and 6 ("share the Node [5, 1, 1]"), a detector naming (5, 1, 1)
  of a fixed body of span [3, 1, 1] at (4, 1, 1) ("a Node of a body on a
  set ... not its position"); the turn's bound: `ticks` 2^40 with the
  momentum 2^20 and N 64 (2^66, "beyond the integer bound"); accepted:
  `span` [3, 1, 1] at x = 0 of a periodic axis (the body wraps), `span`
  absent parsing to (1, 1, 1) and `phase_by_momentum` absent to false,
  `action` absent to None; the record: `run.json` of a turning world
  carries `action` 64, `hypotheses` ["bohr-v1"] and per measured event
  under `numbers` its `span` ([1, 3, 1]) and `phase_by_momentum` (true),
  the measured events' states and `state.json` the `span`; without the
  key `action` None, `hypotheses` [], `span` [1, 1, 1] and
  `phase_by_momentum` false.
- (g) one set object shared by a body and a detector, and one moment table
  over the set (the four unifications, the model owner, 2026-09-20, (3),
  the data only; BEAM_LAW note 33; the integers written first): the body
  of (b) is a set with one measured event, its `DetectorSet.nodes` the
  map of its three Nodes to its number 1 and `Measured.nodes` the three in
  the fixed order, the source outside every detector a set of one Node
  mapped to 2, the engine's index mapping every Node to its set
  (`occupant` 1 at (4, 0, 2), None at (5, 0, 0)), two sets in all; two
  such bodies at (4, 0, 1) and (6, 0, 1) declared in one detector `d` are
  one set of six Nodes mapped to 1 and 2, each body's `nodes` its own
  three: three rays of `m` (number 3, phase 0) arriving at (4, 0, 0),
  (6, 0, 1) and (6, 0, 2) read the threshold 3 over the set (the pointer
  9 units) and click 1 at the first body and 2 at the second, the
  presence 1 and 2, the pushes (-256, 0, 0) and (-512, 0, 0), one `record`
  line naming `d` with the record 9 x 32^2 x 256^2 and no Node; the step
  of the body of (b) moves its Nodes in the set's map and in the index
  (x = 3 after two intervals, the three Nodes there), its escape empties
  both; the presence over a body without arrivals 0; the one table with
  the two masks: a reader of `m` (content 4) reading a row of 3 units of
  a paid family of quantum 2 (content 2 per unit) on +x reads the flow 192
  (3 x 64, the amount's weight) and the push (384, 0, 0) (3 x 2 x 64, the
  label's weight), the content 6; under `beam` at threshold 1 and
  `suspension` [1, 1] the rows of 3 (phase 0) and 2 (phase 32) at two
  Nodes of the body pair 2 units and click 1: the presence and the count
  5 (the units that go on are present), the owed count `by_clock(0, 5,
  1)` = 5, the events [1, 0], the momentum (-256, 0, 0), the record 1, the
  store's rows 2 and 2.

## The phase window under the Beam Law

`tests/test_nature_beam_window.py` (re-pinned from `test_phase_window` under the
flight table: a ray released at tick t first walks at t + 1; 10 Links take
17 walks, 11 Links 19). Bars of 1 x 1 in y and z, N 64, `suspension` 0,
`release` [0, 1], the families `light` (paid) and `counter` (paid).

- (a) the boundary of the window at N = 64: a counter at x = 6 of a
  7 x 1 x 1 bar measuring `light` through the window 20; four rays of
  number 1 on +X at x = 5 with phase 35 (d = 15), x = 4 with 36 (d = 16),
  x = 3 with 3 (d = 47) and x = 2 with 4 (d = 48), reaching x = 6 in
  intervals 1, 3, 5 and 7. d = 15 and d = 48 click (`click` records at
  ticks 1 and 7 with `phase` 35 and 4, the push (64, 0, 0), `content` 1;
  re-pinned on 2026-09-19 for the label along the unit vector from
  (1, 0, 0)); d = 16 and d = 47 pass (`pass` records at ticks 3 and 5 with
  the phase and `window` 20), go on and click on `face:+x` at their next
  step (ticks 5 and 7). After 7 intervals `events` [2, 0], `held` [2, 1],
  the momentum (128, 0, 0) (was (2, 0, 0)), 2 escaped, nothing in the
  store, the books balanced;
  `in_window` at N = 64 admits d in [0, 16) and [48, 64), at N = 2 the step
  0, at N = 4 the steps 0 and 3 (since 2026-09-20 read off the one floor
  `window_admits` at the default width N / 2, the window table being
  deleted; the same steps).
- (b) the complement covers the circle exactly: a bar of 12 x 1 x 1,
  K 2^14, a lamp of `light` (content K + 2, phase 0, rate [1, 1] on +X
  only) at x = 0; a counter at x = 10 measuring through the window 40 and
  its complement at x = 11 through the window 8. The release of age a
  (tick a + 1) reaches x = 10 at tick a + 18 and x = 11 at tick a + 20.
  Since stage (vii) step 4 (the one click) every release is a record born
  at u = a with the path phase 0, and a window reads the path phase: after
  83 intervals x = 10 clicked none and x = 11 all 64 (the running phases
  0 .. 63, `u` on every click line), 66 `pass` records at x = 10 (the 64
  and two more at ticks 82 and 83) with the window 40 and none at x = 11,
  nothing escaped; the lamp at age 83, phase 19, content K + 2 - 83,
  momentum (-5312, 0, 0) (re-run under the one click (stage (vii) step 4); the verdict to be re-read). Until that step the rows carried the
  clock's phase and the two counters clicked 32 times each, x = 10 the
  phases 24..55 and x = 11 the phases 0..23 and 56..63, 34 `pass` records
  at x = 10 (83 labels of 64; was (-83, 0, 0) before the label).
- (c) a lamp with a window: the lamp of (b) with `phase_window` 8 and a
  plain counter at x = 10: at each of the first 64 intervals t its age is
  t, its phase t mod 64, and it released one ray when t - 1 is in the
  window (the ages 0..23 and 56..63) and none otherwise, the ray a record
  born at u = its count of births less one (0 .. 31; until stage (vii)
  step 4 the ray carried the clock's phase t - 1; re-run under the one click (stage (vii) step 4); the verdict to be re-read): after 64
  intervals 32 released, content K + 2 - 32, momentum (-2048, 0, 0) (was
  (-32, 0, 0)), phase 0;
  after 81 the counter clicked 32 times (the phases 0 .. 31) and the lamp
  released 17 more, 49 in all. The refusals, naming the key: a window of 64 at N = 64, a window
  on `pass`, an object entry with an unknown key, a lamp window of -1, a
  `reads` key outside the reading's components; an object entry without
  `rule` takes the family's default rule (since the night of 2026-09-19: a
  window alone on a paid family measures in the window 8).

## The transformation

`tests/test_become.py` (docs/BEAM_LAW.md, section 2 and section 10 note
36 (iii); the model owner, 2026-09-20, "go on everything", item (1): the
transformation `become` with the identity `weak-v1`; the physicist's
design, WEAK.md sections 2 and 4.3). The toy of the design: `n` (free, no
phase circle, content 7, charge 0), `p` (free, charge [1, 5]: +1 on a
content of 5), `beta` (paid, quantum 1, charge -1 per unit of amount),
`nu` (free, a phase circle, charge 0), `w` (free, the absorber, charge 0);
an open 5^3 GameBoard, K 2^20, N 64, `release` [1, 4096], `suspension` 0
unless said; the `become` of `n`: into `p`, the products `[["beta", 1,
2], ["nu", 1, 0]]` (R = 2; the charges +1 on `p`'s 5 and -1 on the beta
unit against 0 on `n`). The six headings in Port order are +x, -x, +y,
-y, +z, -z; a heading row born at tick t is m(tau) Links on at tick
t + tau, m(tau) = (128 tau + 110) // 220. The expected integers, written
down before the first run:

- (a) the clock trigger: `n` fixed at (2, 2, 2) with `at` 3: nothing at
  the ticks 1 and 2 (`held` [7, 0, 0, 0, 0]); at tick 3 `held` [0, 5, 0,
  0, 0] and the family `p`; the rows born at tick 3 with the age 0 and the
  phase 0: `beta` on +y (the heading (2 + 0) mod 6 = 2), amount 1,
  content 2, label (0, 128, 0); `nu` on -y (the next heading), amount 1,
  content 0, label (0, -64, 0); the recoil and the event's momentum
  (0, -64, 0); the `become` record at tick 3: trigger "clock", triggered
  3, from `n`, into `p`, the products [["beta", 1, 2, [0, 1, 0]], ["nu",
  1, 0, [0, -1, 0]]], recoil [0, -64, 0], counted 0; the books at every
  tick: `n` `became` -7, `p` `became` +5, `beta` released 1 unit with
  the content 2, `nu` 1 unit with the content 0 (-7 + 5 + 2 = 0), the
  charge line [0, 1] at every tick; the beta row at (2, 3, 2) at the ticks
  4 and 5, (2, 4, 2) at 6 and 7, `face:+y` at tick 8 (escaped content 2,
  momentum (0, 128, 0)), the nu row `face:-y` at tick 8 (amount 1,
  momentum (0, -64, 0)), the store empty after; `hypotheses` ["weak-v1"];
  the state's `became` 1 and `family` 1; `run.json`'s
  `numbers["1"]["become"]` the declaration by names. With `at` 10^6 over
  20 intervals: `held` unchanged, no record, `became` 0, the board's rows
  identical to the world without the key.
- (b) the click trigger: a bar of 9 x 1 x 1, K 4096, `release` [1,
  4096]; a fixed `nu` source of content 4096 at x = 0 (the turn 1) and
  the reader `n` (content 7) fixed at x = 3 with the entry `nu: {rule
  become, phase_window 0, phase_width 1, into p, products as (a)}`: a row
  born at tick t arrives at tick t + 5 (m(5) = 3) with the phase t - 1;
  the ray of phase 0 clicks at tick 6 (the push (-448, 0, 0)), the
  products born in step 5 of tick 6 (the clock age 5): `beta` on -z (the
  heading 5), label (0, 0, -128), `nu` on +x (the heading 0), label (64,
  0, 0), the recoil (-64, 0, 128), the momentum (-512, 0, 128); the
  `become` record at tick 6 with triggered 6; the beta row through
  `face:-z` at tick 7, the nu product through `face:+x` at tick 16
  (m(10) = 6); the entry consumed: the reader, now `p` (content 5), reads
  every later arrival by the keys' `read` (the push (-320, 0, 0) each, 69
  reads at the ticks 7 .. 75, none clicked or passed; the momentum
  (-512 - 69 x 320, 0, 128) at the end). With the window 5: the phases
  0 .. 4 pass (`pass` lines naming the window 5 at the ticks 6 .. 10) and
  the phase 5 clicks at tick 11, the transformation at tick 11.
- (c) the crowd slows the trigger and the gate holds it: `p` fixed at
  (1, 2, 2) of content 64 releasing 64 units per heading per
  self-creation (`release` [1, 1]) and `n` fixed at (2, 2, 2) with `at` 3
  and `suspension` [1, 128]: `n` counts 64 at tick 2 and 128 from tick 3
  on, owes 1 after every self-creation from tick 2, and fires at tick 4
  (the age 3), against tick 3 alone; the record's `counted` 128. With
  `crowd` 64 it never fires in 40 intervals (the count 128 at every pulse
  of the key, the ages 3, 6, 9, ...); with `crowd` 129 at tick 4.
- (e) the charge line through the click of the product: the world of (a)
  with a fixed absorber `w` (content 1) at (2, 4, 2) measuring `beta` by
  the keys: the click at tick 6 (the age 3, m(3) = 2): the absorber's
  `held` [0, 0, 2, 0, 1], content 3, clicks [0, 0, 1, 0, 0], charge
  (-1, 1); the charge line [0, 1] at every tick; the measured lines per
  family `p` 5, `w` 1 and `beta` 2 (8 in all = 7 + 1 initial), the `beta`
  line initial 0 + measured 2 + became 0 = 2; the books balanced at every
  tick.
- (f) the refusals, naming the key: `become` without `into` or
  `products`; `into` unknown or the event's own; a product's family
  unknown; a product's amount 0; a free product's content 1; a paid
  product's content 0; a label beyond the bound (an amount of 2^57 of
  `beta`); `at` 0, absent, or on a table entry; `crowd` on a table entry,
  -1 or 1.5; `into` on a `measure` entry; the products' content 8 above
  the amount 7; the charges unbalanced (the products `[["nu", 1, 0]]`
  alone: 0 to +1; the beta charge 0; the `p` charge [1, 4]); `become` on a
  family; and at run time a lamp of `light` (paid, content 20, K 20, one
  unit on +x per turn of 1) with `become` at 10 into `w` and the product
  `[["light", 1, 15]]` holds 13 at tick 10 and refuses the run naming the
  event and the 13 it holds.

`tests/test_nature_beam_body.py` re-pins `numbers` with `"become": None`
and `tests/test_nature_beam_clock.py` the books' measured line with
`"became": 0` (the added keys of the record).

`tests/test_weak_readings.py` (b), the tool on the transformation: the toy
of (a) with the beta content 3 in an open 9^3 GameBoard, K 2^20,
`suspension` [1, 2^20], a shell of `d` at r = 2 (62 Nodes within a half
Link of 2) as one `beam` set measuring `beta` with `reads` `age`, 12
intervals: the `become` line at tick 3 with the count 0, the beta product
on +y at (4, 6, 4) at tick 6 (the age 3, m(3) = 2), the shell's clicks
{6: 1}, the contents {3: 1}, the ages [3], the nu product passing the
shell; the tool's criteria against the pinned tick 3 all inside (the
tick, the content, the count 1 of 1, the step: one click), a `never`
expectation outside.

## The W world

`tests/test_w_world.py` (docs/BEAM_LAW.md, section 10 note 36 (iv); the
model owner, 2026-09-20, "go on everything", item (3): the W world after
the transformation; the physicist's design, WEAK.md 1.1 and 4.5). A bar
of 7 x 1 x 1, K 2^20, N 64, `release` [1, 2^20] (no free release of 1839
before the age 570), `suspension` 0; `n` (free, content 1839, charge 0),
`p` (free, charge 4 per unit of content: 7344 on 1836), `w` (paid,
quantum 1, a phase circle, charge -7344 per unit of amount, `lifetime` 1),
`beta` (paid, charge -7344) and `positron` (paid, charge +7344); the
neutron of 1839 fixed at x = 2 with `become` at 3 into `p` with the one
product `[["w", 1, 3]]` on `directions` `[[1, 0, 0]]`, the proton of 1836
fixed at x = 3; the W row's label 64 x 1 x 3 = 192. The expected
integers, written down before the first run:

- (a) the exchange: at tick 3 the neutron becomes `p` (`held` [0, 1836,
  0, 0, 0], charge (7344, 1)) and throws the W on +x (the `become` record
  with [["w", 1, 3, [1, 0, 0]]], the recoil [-192, 0, 0]); at tick 4 the
  W (age 1) at x = 3 is measured by the keys' rule (a `click` naming the
  measured event 2, `w`, amount 1, content 3, the push (192, 0, 0)): the
  proton's `held` [0, 1836, 3, 0, 0], content 1839, clicks [0, 0, 1, 0,
  0], charge (0, 1), momentum (192, 0, 0); the store empty after tick 4,
  no click on the border; the charge line [7344, 1] at every tick of 8;
  the `w` lines released 1, measured 3 (the content), current 0, the
  lifetime line 0; the run's `hypotheses` ["columns-v1", "weak-v1"]; the
  record's states and the border `lifetime` with 0 clicks of `w`.
- (b) the W into empty space (`directions` `[[-1, 0, 0]]`): at tick 4
  the W at x = 1 is booked on the border `lifetime` (a `click` naming
  the detector `lifetime`, amount 1, content 3, momentum [-192, 0, 0]);
  the proton untouched; the escaped amount of `w` 1; the charge line
  [7344, 1] at every tick.
- (c) the click trigger on the proton: the design's sketch `w: {rule
  become, phase_window 0, phase_width 64, into n, products [["beta", 1,
  3]]}` refused at load ("charges do not balance"); with the product
  `[["positron", 1, 3]]` accepted: at tick 4 the W clicks and the proton
  becomes `n`, the positron born on -y (the clock age 3), label (0,
  -192, 0), the recoil (0, 192, 0), the momentum (192, 192, 0); the
  `become` record at tick 4 with the trigger "click", triggered 4, the
  products [["positron", 1, 3, [0, -1, 0]]], counted 1; `held` [1833, 0,
  3, 0, 0], content 1836, charge (-7344, 1); the positron through
  `face:-y` at tick 5; the charge line [7344, 1] at every tick; the
  `became` lines `p` 0 and `n` -6, the `w` line measured 3, the
  `positron` line released 1; the entry consumed.
- (d) the refusals, naming the key: `lifetime` 0 on `w`; the W's charge
  [-7344, 2].

`tests/test_weak_readings.py` (c), the tool on the W world: the bar of
(a) run through the runner with the model `beam-weak-w_exchange-v1`: the
neutron's `become` line at tick 3 with [["w", 1, 3, [1, 0, 0]]], its
momentum (-192, 0, 0); the proton's click of `w` at tick 4, its content
1839, charge (0, 1), momentum (192, 0, 0); the border 0; the five
criteria inside against the pinned integers (the kinds GAMEBOARD,
DETECTOR, DETECTOR, DETECTOR, GAMEBOARD), the click tick pinned at 5
outside.

## The hand

`tests/test_hand.py` (docs/BEAM_LAW.md, section 10 note 39; the model
owner, 2026-09-20, record 128, "the hand's three choices confirmed"; the
physicist's design hand/DESIGN.md with the mathematician's FORM.md). One
column `hand` on the row (-1, 0, +1), one axial record `axis` on the
measured event, the right-hand rule at the birth of a `become` product
(a product of hand h on the directions with sign(A . u_d) = h, a
left-handed product against the axis), the parity filter `hand` on a
table entry. The expected integers, written down before the first run:

- (a) the carriage: a transit row of `light` of hand -1 on +x from x = 1
  into a mirror at x = 3 re-emitting on -x (a second measured event of
  `d` at x = 6 so that the row is another number's arrival): one
  `rerelease` line at tick 3 with `hand` -1, the one row of the store
  hand -1, the books balanced; the amplitude generator's `cnot_pair_0_8`
  with both lamps given `hand` -1 for 40 intervals: every row of `light`
  hand -1 at every interval, `rotate`, `gate` and `split` lines written,
  every click line `hand` -1; the meeting test's form (a paid unit of
  phase 63 on +x circling a periodic line of four free units, the
  declared directions (24, 1, 0) and (24, -1, 0), two intervals): the
  unit turned to a declared direction with its phase advanced and its
  hand -1, the `turned` line nonzero; two singles of one class at x = 3
  on +x and -x, both -1, after one interval two rows of hand -1; the
  merge of two rows equal in every field but the hand: two rows, and
  with a third row of hand +1 the amounts 1 and 3; under the amplitude
  key two rows of the record 5 at the phases 0 and 32 with opposite
  hands: nothing cancelled, two rows;
- (b) the giving: a free source of `nu` with the family `hand` -1 at
  `release` [1, 4096] over 3 intervals: 3 rows, every hand -1; a lamp
  with `hand` +1 (K 64 on 1024: the turn 16) over 3 intervals: 3 rows,
  every hand +1; a transit row with `hand` -1: the row -1; on an open 5^3
  GameBoard the neutron (1839) at the centre with `axis` [1, 0, 0], the six
  headings and `become` at 3 into `p` (charge 4) with the products
  `beta` (1, 3; charge -7344, hand -1) and `nubar` (1, 0; hand +1): the
  `become` line at tick 3 with the products [["beta", 1, 3, [-1, 0, 0],
  -1], ["nubar", 1, 0, [1, 0, 0], 1]], the recoil [128, 0, 0], the
  event's momentum (128, 0, 0); the product `beta` (6, 3; charge -1214,
  no hand) alone at the same parent: six rows of amount 1, one per
  heading, stamped +1 on [1, 0, 0], -1 on [-1, 0, 0] and 0 on the four
  others; the parent's `directions` [[1, 0, 0]] alone with the handed
  products refused at load, "become.products[0] ('beta', hand -1) has no
  direction"; the same handed products at a parent without an axis on
  [[1, 0, 0]]: both born on [1, 0, 0] with the hands -1 and +1;
- (c) the taking: a reader with `light: {rule measure, hand -1}` met in
  one interval by three rows of hand -1, +1 and 0: one click with `hand`
  -1, two `pass` lines with the hands 0 and +1 (`window` None, no
  `threshold`), the books' `left` 1 and `right` 0, two rows left in the
  store; a `beam` reader with the window 0 of width 1 and `hand` -1 met
  by the rows (-1, phase 5), (+1, phase 0) and (-1, phase 0): one click
  (hand -1, phase 0), the passes (-1, 5) and (+1, 0); the W world of
  series P with the W family `hand` +1 (a phase circle), the neutron's
  axis +x and the proton at x = 3 with `w: {rule become, phase_window 0,
  phase_width 64, hand -1, into n, products [["positron", 1, 3]]}`: the
  `become` line's product [["w", 1, 3, [1, 0, 0], 1]], one `pass` line
  (tick 9, measured 3, hand +1), one border click (tick 9, at x = 3,
  hand +1), the proton `became` 0 and still `p`, its clicks of `w` 0,
  the books' `left` and `right` of `w` 0;
- (d) the parity test on the worlds of series P (`nu_hand` at 60
  intervals), the design's 1.3: every polar thing by g, the axis as an
  axial vector det(g) g A, every hand verbatim, mapped back; under the
  mirror in x (where the axial transform and a verbatim copy of the axis
  coincide): `w_hand` different, the click (9, measured 3, x = 3, push [192,
  0, 0], hand -1) against (9, measured 1, x = 1, push [-192, 0, 0], hand
  -1), the `become` line's product [1, 0, 0] with the recoil (-192, 0,
  0) against [-1, 0, 0] with (192, 0, 0), the charge line and the `w`
  lines of the books equal; `w_two_sides` equal; `wu` different, the
  beta's click (21, measured 1, x = 0, push [-192, 0, 0]) against (21,
  measured 3, x = 16, push [192, 0, 0]), the antineutrino's face `face:+x`
  against `face:-x`; `nu_hand` equal; over all 48 signed axis
  permutations the parity image differs under exactly the 24 improper
  elements and no proper one on `w_hand` and `wu` and under none on
  `w_two_sides` and `nu_hand`, and the full transform (hands by det too)
  is equal under all 48 on all four;
- (e) `weak/w_exchange` for 16 intervals: no line carries `hand`, no
  `left` in the books, no `hand-v1`, no `hand` on a family and no `axis`
  on a number of `run.json`, no `hand` in `state.json`; the packed merge
  key of three rows equal to the key over the identity fields without the
  hand;
- (f) the refusals, naming the key: `hand` 0 and 2 on a family; a lamp's
  `hand` +1 against the family's -1; `axis` [1, 1, 0]; `hand` on a `pass`
  entry; a transit `hand` +1 against the family's -1; branches naming
  hands on a family with a hand; a hand on some labels only; the bit
  value 1 given two hands ([[1, 1, 1], [3, 1, -1]]); both values one
  hand ([[0, 1, 1], [3, 1, 1]]); and [[0, 1, 1], [3, 1, -1]] accepted with
  the label hands (1, -1) and `hand-v1` last under `hypotheses`;
- (g) the four CHSH worlds of series L3 with the lamp's `branches`
  [[0, 1, 1], [3, 1, -1]]: E x 64 = 44, -44, 44, 44, S = 176/64, every
  marginal 32/64, every row's `hand` column 0, every click line of
  `light` carrying (1, -1)[the bit of its label on its arm]; the full
  mirror of `bell_0_8`: the same outcome per u; the parity filter on the
  label-hand family reads the label (`bell_0_8` with the rotations removed
  and `hand` +1 on the two plus counters, 64 births): 32 records gathered
  at (alice_plus, bob_plus) and 32 at (alice_minus, bob_minus), none
  mixed, every click line at a plus counter `hand` +1 and every `pass`
  line there `hand` -1; with the settings (0, 8) kept and the same
  filters, 32 of 64 chosen at alice_plus and 32 at bob_plus.

## A paid family's charge

`tests/test_paid_charge.py` (docs/BEAM_LAW.md, section 2 and section 10
note 36 (ii); the model owner, 2026-09-20, "go on everything", item (2),
D-1: a paid family may declare a whole charge per unit of amount, read on
the charge line only, the push untouched). Bars of 7 x 1 x 1, K 2^20,
N 64, `release` [0, 1], `suspension` 0; `p` (free, charge [1, 5]: +1 on a
content of 5), `beta` (paid, quantum 1, charge -1 per unit of amount), `w`
(free, charge 0); a beta row of amount 1 declared at x = 1 on +x is at
x = 2 at the ages 1, 2; 3 at 3, 4; 4 at 5, 6; 5 at 7; 6 at 8, 9; off the
bar at 10 (m(tau) = (128 tau + 110) // 220). The expected integers,
written down before the first run:

- (a) `p` of content 5 fixed at x = 0 and the absorber `w` fixed at x = 4:
  the books' charge line [0, 1] at every tick of 6 (p +1, the row -1;
  then p +1, the absorber's unit -1); the click at tick 5: the absorber's
  `held` [0, 1, 1], content 2, `clicks` [0, 1, 0], `units` of beta 1,
  charge (-1, 1), `charges()` [(2, 1), (-1, 1)], `charges(for_push=True)`
  [(2, 1), (0, 1)], momentum (64, 0, 0) (the label); with the beta charge
  0 the same momentum and the line [1, 1]; a charged free reader (`p`
  at x = 4 with `read` for beta) takes the label alone, the push
  (64, 0, 0), its charge (1, 1).
- (b) without the absorber the row leaves through `face:+x` at tick 10;
  the line [0, 1] at every tick of 12; the escaped amount 1,
  `units_escaped` [0, 0, 0].
- (c) the absorber at x = 3 releasing on +x with the row of its own
  number: `home` at tick 3, the row created again on +x in the same
  interval, `face:+x` at tick 10; the line [-1, 1] at every tick of 12;
  the absorber's momentum (0, 0, 0) and `units` 0 after; `transit_released`
  [0, 1, 0].
- (d) the absorber free: after the click (content 2, momentum (64, 0, 0))
  it steps at the ticks 7, 10 and 13 (the step drive, 2026-09-20: the
  drive 64 at the click's interval 5, 192 = D at 7; the rule as it was,
  `by_clock(age - 1, 64, 192)`, stepped it at 6, 9 and 12), to x = 5, 6
  and off the bar: the face click at tick 13 with `held` [0, 1, 1];
  `units_escaped` [0, 1, 0]; `held_escaped` [0, 1, 1]; the line [0, 1] at
  every tick of 15.
- (e) the refusals, naming the key: `charge` [-1, 2] on a paid family; a
  lamp on a measured event of a charged paid family. The record: the
  family's `charge` (-1, 1), its `charge` column value (0, 1), `values`
  ((1, 1), (0, 1)), `hypotheses` []; `run.json`'s family `charge` [-1, 1]
  and column value [0, 1], the audit's `charge` [0, 1] at every tick, the
  absorber's `charge` and `charges.charge` [-1, 1].

## The width of a window

`tests/test_window_width.py` (docs/BEAM_LAW.md, section 2 and section 10
note 36 (i); the model owner, 2026-09-20, "go on everything": the neutrino
first with the table-entry key `phase_width` and no change of law; the
physicist's design, WEAK.md 1.2). The expected integers, written down
before the first run:

- (a) the one floor `window_admits` at the default width N / 2 is the half
  circle on every (phase, setting) pair, d < N / 4 or d >= 3 N / 4, at
  N = 2, 4, 64 and 4096 (for N = 2 the one step d = 0); at N = 64 the
  width 1 centred on s admits {s}, 2 admits {s - 1, s}, 3 admits {s - 1,
  s, s + 1}, 4 admits {s - 2, s - 1, s, s + 1} (the arc starts at
  s - floor(w / 2)), the width 64 every step.
- (b) the admitted fraction w / N against the source's stride: a bar of
  9 x 1 x 1, K 4096, N 64, `release` [1, 4096], `suspension` 0; a fixed
  source of the free family `nu` of content 4096 at x = 0 releasing one
  ray per self-creation on +x (the turn 1: the stride 1), the ray born at
  tick t carrying the phase (t - 1) mod 64 and arriving at the fixed
  reader `r` (free, no phase circle, content 1) at x = 5 at tick t + 8
  (m(8) = 5); over 648 intervals 640 arrivals (the ticks 9 .. 648). The
  reader's entry `nu: {measure, phase_window 0}`: with the width absent
  320 click and 320 pass (the phases 0 .. 15 and 48 .. 63); with
  `phase_width` 1: 10 clicks at the phase 0 alone, at the ticks 9 + 64 k;
  2: 20 (the phases 63, 0); 4: 40 (62, 63, 0, 1); 32: 320 with the `click`
  and `pass` records identical line by line to the width absent. With
  K 2048 (the turn 2, the stride 2) the width 1 centred on 0 admits 20 of
  640 (the even coset) and centred on 1 admits 0 (640 passes). The reader
  declared as a `beam` detector reads the same counts. Each click of a
  free ray takes the columns' push, gravity -M_A V = -64 on the reader of
  content 1 (a free ray's label never joins), so the momentum after c
  clicks is (-64 c, 0, 0). The reader's state carries `widths` [w, None];
  a world without the key has every width None.
- (c) `beam`'s pairing arc is the entry's width: two rays of `light` at
  x = 5 with the phases 0 and 30 (and 0 and 10) arriving together at a
  `beam` counter at x = 6 whose entry has the window 16: with the width
  40 the pair (0, 30) is paired (d = 62, (62 + 20) mod 64 = 18 < 40: two
  `pass` records with `cancelled`, no click) and the pair (0, 10) clicks
  twice ((42 + 20) mod 64 = 62 < 40 false); with the width 64 every pair
  is paired; with the default width (0, 30) pairs and (0, 10) clicks, as
  until 2026-09-20.
- (d) a lamp's window has the same width: the lamp of the window test (c)
  (K 2^14, content K + 2, one ray per self-creation on +x) with
  `phase_window` 8 and `phase_width` 4 releases at the self-creations
  whose clock phase falls in [6, 10): over 64 intervals 4 rays, records
  born at u = 0, 1, 2, 3 (their phases; until stage (vii) step 4 the
  clock's 6, 7, 8, 9; re-run under the one click (stage (vii) step 4); the verdict to be re-read), the content K + 2 - 4, the momentum
  (-256, 0, 0); 32 with the width absent.
- (e) the refusals, naming the key: `phase_width` 0, 65 at N = 64, 1.5 and
  "4"; on `pass`; for a family without a phase circle; without
  `phase_window`; on a lamp without its window and at 0; `phase_width`
  beside `phase_window` alone on a paid family takes the default rule
  `measure`.

`tests/test_weak_readings.py` (series J2's tool, `tools/weak_readings.py`,
reads the runner's record and the flight table): a bar of 40 x 1 x 1 with
the source of (b), three readers of `d` at x = 8, 9, 10 in the window 0
of width 1 and a far detector at x = 30 without a window, 205 intervals,
run through the runner: the first-arrival ages 13 at 8 Links and 51 at 30
off `flight_table`; the first reader 192 arrivals, 3 clicks (the phases 0
of the rays born at the ticks 1, 65, 129), 189 passes; the readers at 9
and 10 no click; the far detector 151 clicks (154 rays reach it, less the
three of phase 0); the stride 1; the three criteria of `j2_filter` inside.
## A window read from a reading

`tests/test_nature_beam_window_reads.py` (issue #363, 2026-09-20;
[BEAM_LAW note 34](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)).
A bar of 7 x 1 x 1, N 64, K 2^20, `suspension` 0, `release` [0, 1], the
families `light` (paid), `counter` (paid) and `s` (free, the setting),
every measured event `fixed`; a counter at x = 3 measuring `light` through
`{"reads": "s", "offset": 4}` and passing `s`; a measured event of `s` at
x = 6 (the number the setting rays carry; it passes `light`) and one of
`light` at x = 0 (the number the pair rays carry).

- (a) the centre is the setting ray's phase plus the offset: a ray of `s`
  (number 3, phase 20) and a ray of `light` (number 1, phase 30) both at
  x = 2 on +X reach x = 3 in the first interval; the centre is 24 and
  d = 6 is inside, so the light ray clicks at tick 1 with `window` 24 on
  its click record, `held` [1, 1, 0], the push (64, 0, 0); a second light
  ray of phase 45 (d = 21, outside) at x = 2 with the age 1 arrives at
  tick 2, the setting ray still present (its second interval at x = 3: the
  presence counts it), and passes with `window` 24 and `reads` "s", no
  `threshold` key; the setting ray meets `pass` with no record and goes on
  (the store holds it, the counter measured none of `s`); the numeric
  window 24 on the same world gives the same click and pass, without
  `window` on the click and without `reads` on the pass, the same `held`.
- (b) no setting ray present: a light ray of phase 24 alone at x = 2
  passes at tick 1 with `window` None and `reads` "s", no `threshold`
  key, no click, and clicks on `face:+x` at tick 8 (five Links, m(8) = 5);
  two setting rays in antiphase (20 and 52) arriving with the light ray at
  tick 1 give a zero pointer, no centre, and the light ray passes the same
  way.
- (c) the parsing: on the `light` entry `windows` None and `window_reads`
  (2, 4) (the family `s` at index 2, the offset 4; the other entries None),
  the offset 0 by default, a numeric window leaving `window_reads` None;
  refused naming the key: `reads` naming an unknown family, the entry's
  own family (`light`) or a family without a phase circle, the form on
  `pass`, an `offset` of 64 at N = 64, an object with the key `width`, an
  object without `reads`, and the form on a lamp (`lamp.phase_window must
  be an integer`).

`tests/test_bell_choosers.py` (the reader of the run, the experimenter's
rule): the design of `examples/events/bell/make_chooser_worlds.py`
(`base`) with the two setting streams at fixed phases (the lamps' contents
3 and 5 at `release` [1, 1], the turn 0: every `sa` row carries 20 and
every `sb` row 44; the offsets 0 and 32) run through the runner for the
warm-up 7 plus 64 pairs: (a) the offsets read off the record (tick - phase
mod N, one value per counter) equal 1 + the flight age at which the pair
ray reaches each counter off `FlightTable.manhattan_steps`, 6, 11, 13, 14;
(b) one bin (20, 44) of 64 pairs: since stage (vii) step 4 (the one
click) the pair lamp's rows are records with the path phase 0 and the
counters' windows read the path phase, so every pair lands in (-1, -1),
the counts 0, 0, 0, 64, E = 1, both marginals 0 and 3 of the tool's
criteria failed (the record kinds, every click inside its window, E on
the triangle), the tool's expectation -1/2 being the crowd form's (re-run under the one click (stage (vii) step 4); the verdict to be re-read;
until that step the counts were 8, 24, 24, 8, E = -1/2 the triangle's
1 - 4 x 24 / 64, both marginals 1/2, 0 criteria failed); (c) the windows
written in the file (20, 52, 44, 12) read the same bin and counts, the
two runs merged one bin of 128 with E 1, the command line on both exit 1
(its checks fail; was exit 0); (d) on synthetic bins whose E are the triangle's for 0/25
and 8/29, `chsh_sum` 2 (None with a bin missing), `best_quadruple` 2 on
that quadruple with the triangle 2, `signed_sums` the minus sign on each
term in turn, `in_window` the engine's half circle.

## The world file of the Beam Law

`tests/test_nature_beam_world_parsing.py` (docs/BEAM_LAW.md, sections 2 and 7;
re-pinned from `test_event_worlds` (e) and
`test_integer_bounds_of_measured_and_emission` (a)).

- (a) refused, naming the key: `"law": "events"` (naming the Beam Law
  and MIGRATION), `dynamics`, `max_active_owners`, `headings` on a lamp,
  `heading` on a ray, `port_map`, `groups` on a detector, a non-primitive
  direction (2, 2, 0), a component beyond P (65 at the default bound), a
  direction the world does not declare, a rest direction on a lamp, a
  repeated direction, a momentum label beyond 2^62 - 1 on a declared ray
  and on a lamp's release, `phase_per_link` outside 0 .. N - 1 or on a
  family without a phase circle, the earlier engines' keys, `phase_turn`, a
  closed GameBoard, an unknown key, a content at K x N / 2, a lamp on a free
  family, two measured events at one Node, an unknown table rule, N not a
  power of two, a detector on a Node without a measured event, a Node in
  two detectors, `kind` on a family (naming MIGRATION: the quantum decides
  the kind), a family without `quantum`, a negative quantum, a fractional
  charge on a paid family (D-1, since 2026-09-20; until then any), `charge`
  on a measured event (naming the removal of
  2026-09-20 and MIGRATION), a family `charge` of [1, 0] (the denominator
  from 1), [1.5, 2] (the numerator an integer), "1/2" and [1, 2, 3] (an
  integer or [numerator, denominator]), a detector named `face:+x` (the
  name of a face detector), a `suspension` denominator of 0, a window for
  a family without a phase circle.
- (b) accepted: the direction table of a world with `directions`
  [[1, 1, 0]] is the two rest vectors, the six headings and (1, 1, 0); a
  measured event's `directions` by vector or by index; a ray at rest (index
  0); `suspension` 1 as (1, 1), [1, 4], [0, 4] as (0, 1); `reads` per entry.
- (c) the runner: a 4-interval world into `run.json` (`law` "beam-v1",
  completed, four ticks, four books, conserved, the measured events, the six
  face detectors of the open GameBoard with their `record`, the directions
  table, `suspension` [1, 1]), `state.json` (the law, tick 4, the Nodes with
  rays) and `events.jsonl`; a negative tick count and a used output
  directory refused.
- (d) the bounds (re-pinned on 2026-09-19 at 1/64 of their amounts, the
  label of a unit along a heading being 64 e_d since the label along the
  unit vector, [BEAM_LAW note 23](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)):
  two measured events of content 1 (were 64) one Link apart at `release`
  [1, 1] read each other's one ray from interval 2 on and are pushed by
  1 x 64 x 1 = 64 (was 64 x 64 = 4096) toward each other; the second,
  declared with the momentum -(2^62 - 1) + 64 on x, reaches the bound
  exactly and is accepted; one unit nearer it is refused with
  `OverflowError` naming the measured event, its Node and the momentum; a
  reader of content 2^56 - 1 met by one ray (was 64) takes the push
  -(2^56 - 1) x 64 = -(2^62 - 64), the same number, and at 2^56 the push
  -2^62 is refused naming the push.

## The label along the unit vector

`tests/test_nature_beam_label.py` (docs/BEAM_LAW.md, section 2 and section 10, note
23; the model owner's decision of 2026-09-19 on the physics-rule
reviewer's verdict, Highlights 5.4): the label of one unit on the
direction D is u_d, the integer vector nearest Q D / |D| with Q = 64, by
the exact integer rule k(|a|) = (isqrt((2 Q |a|)^2 // |D|^2) + 1) // 2
with the sign restored (`nature_beam.unit_label`, the flight table's
`labels`); a row's label is content x amount x u_d (paid) or amount x u_d
(free). The expected integers, written down before the first run:

- (a) the table: u_(1, 1, 0) = (45, 45, 0), u_(1, 1, 1) = (37, 37, 37),
  u_(2, 1, 0) = (57, 29, 0), u_(3, 1, 0) = (61, 20, 0), u_(7, 5, 0) =
  (52, 37, 0), u_(11, 1, 0) = (64, 6, 0), u_(1, 2, 3) = (17, 34, 51),
  u_(63, 46, 46) = (45, 33, 33); the six headings exactly 64 e_d; the rest
  vectors (0, 0, 0); 63^2 < |u_d|^2 < 65^2 for every direction of the
  table; u_{-D} = -u_D exactly; u_{gD} = g u_D for the 48 signed axis
  permutations; over every primitive direction with components in -64 ..
  64 (1780418 of them, at once) the integer rule equals the float rounding
  of Q |a| / |D|, no component passes Q, no exact tie occurs (a tie needs
  (2 m + 1)^2 |D|^2 = (4 Q |a|)^2, impossible below |D| = 256) and |u_d|
  is within sqrt 3 / (2 Q) = 1.35 % of Q.
- (b) the labels on the GameBoard: a 31^3 open GameBoard with the six headings and
  the eight fan directions above and their negatives; a lamp of `light`
  (quantum 1, content 3 x 2^18 at K 2^18: the turn 3 at every age of the
  run, so the content per unit is 3) at (15, 15, 15) releasing one unit
  per interval on the six headings and the eight fan directions (14 rows
  per release, amount 1, content 3): every row's label 3 x u_d, |label|^2
  within (63 x 3)^2 .. (65 x 3)^2; the release is one record of 14 rows
  (m 14) since stage (vii) step 4, so the lamp's recoil after the first
  release is the rows' shares, label // 14 each, (-77, -48, -24), the
  transit line the whole labels' sum 3 x (378, 241, 121) = (1134, 723,
  363) and the books' `remainder` line (-1057, -675, -339), measured +
  transit + escaped + remainder = 0 at every interval; the mirror takes
  each row's share and recoils by the re-created row's, (22, 14, 0) per
  reflection; the screen's momentum the sum of the shares (13, 0, 0) and
  (13, 1, 0) of its clicks (re-run under the one click (stage (vii) step 4); the verdict to be re-read; until stage (vii) step 3 the recoil
  was the whole labels, (-1134, -723, -363), and the screen's momentum
  the sum of the pushes);
  through 60 intervals with a screen of `m` at (21, 15, 15) measuring
  `light` (each click moves the ray's label 3 x u_d: the +X rays
  (192, 0, 0), the (11, 1, 0) rays, whose line passes the screen's Node
  too, (192, 18, 0); the screen's momentum their sum), a mirror at
  (22, 20, 15) on the line of (7, 5, 0) re-emitting on (-7, -5, 0) (its
  momentum exactly 2 x 3 x (52, 37, 0) = (312, 222, 0) times the rays it
  reflected, the label out being minus the label in) and the open faces
  (the escaped line the sum of the face clicks' momenta): measured +
  transit + escaped = (0, 0, 0) at every interval, the books balanced, the
  running transit line equal to the recount, every label in the store 3 x
  u_d at every interval.
- (c) the bound (re-pinned on 2026-09-20, the architect's B1: the
  product is checked per row before it is formed, the weight times the
  largest component of the row's u_d): a declared ray of `light` (quantum
  1) of amount 2^56 is refused by the parser naming "64 x 1 x
  72057594037927936 = 4611686018427387904" and the bound; amount 2^56 - 1
  is accepted; a free family's declared ray likewise; `momentum_labels`
  refuses a paid row of content 2^28 and amount 2^28 on a heading, and a
  free row of amount 2^56, naming "amount 268435456 and content 268435456
  at Node [2, 2, 2] ... 72057594037927936 times the largest component 64 =
  4611686018427387904" (the free row "amount 72057594037927936 and content
  0"), and accepts the same rows on (1, 1, 0) with the label 2^56 x (45,
  45, 0) [was: `label_weights` refusing at 64 x 2^56 for every direction];
  `label_weights` refuses a row whose content x amount cannot be formed
  (amount 2^32, content 2^31) naming the amount and accepts the paid row
  of content 2^28 - 1 and amount 2^28 + 1 (2^56 - 1), the free row of
  2^56 - 1 and the free row of 2^56 (the weight fits; the label decides);
  MOMENTUM_BOUND // 64 = 2^56 - 1.
- (d) the wrap that passed (B1): two declared rays of `light` of amount
  2^55 at (2, 2, 2) on (1, 1, 0) merge at construction into one row of
  2^56, accepted: the transit line 2^56 x (45, 45, 0) counted and running
  alike, the books balanced and the running line equal to the recount
  through three intervals; the same two rays on (1, 0, 0) are refused at
  construction (the recount forms the label) naming "amount
  72057594037927936 and content 1 at Node [2, 2, 2] along [64, 0, 0], its
  weight 72057594037927936 times the largest component 64 =
  4611686018427387904"; a mirror of `wall` at (5, 5, 0) on a 12 x 12 x 1
  GameBoard re-emitting on (64, 1, 0) what two rays of `light` (quantum 2^25)
  of amount 2^30 and of the numbers 2 and 3 bring it in one interval (from
  (4, 5, 0) on +X and (5, 4, 0) on +Y): two `rerelease` records of 2^30
  with the pushes (2^61, 0, 0) and (0, 2^61, 0), two born rows of weight
  2^55 within the bound, merged into one row of amount 2^31 and content
  2^25, and the recount refused naming "amount 2147483648 and content
  33554432 at Node [5, 5, 0] along [64, 1, 0], its weight
  72057594037927936 times the largest component 64 = 4611686018427387904".

## The worlds of the Beam Law

`tests/test_nature_beam_worlds.py` (docs/BEAM_LAW.md, section 7): the worlds of
`examples/events/` on minimal GameBoards, pinned as a check that the engine
does what the law says and not as a result.

- (a) the two slits (the example world's design, 60 x 121 x 1, z periodic,
  500 intervals): a lamp at (2, 60) of turn 8 per self-creation (K 2^30,
  content 8 K + 1 400 000, 64 rays per self-creation on five directions), a
  wall at x = 8 measuring light with the openings at y = 55 and 65
  re-emitting on the fan of the 91 primitive directions (a, b, 0) with
  a >= 1 and a + |b| <= 12, a screen at x = 52 read as 121 one-Node
  `wave` detectors `screen_<y>` (the screen's pixels; since 2026-09-19 a
  detector is a set with one record, so one detector of 121 Nodes would
  read one record with no resolution in y, and a pixel one Node wide
  reads what the Node read before).
  Three runs, both openings and each alone: the plain count is additive to
  the unit (count_both = count_55 + count_65 at every screen Node) and the
  interference term V(y) = (I_both - I_55 - I_65) / (2 sqrt(I_55 I_65)) of
  the record correlates with the two-source Euclidean cosine at lambda =
  c x period = 8 / sqrt 3 above 0.85 over the Nodes both openings reach
  (the design pinned 0.9 for a fan of 203 directions; measured 0.893 with
  the 91 of this world), and the correlation at the periods 4 and 16 is
  below 0.5.
- (b) Bell (the ten A2 worlds under `"law": "beam"`, `tools/bell_chsh.py`):
  S = 2 exactly, S' = 3/2 exactly, the controls +1, -1, 0, no-signalling
  exact, 0 criteria failed.
- (c) one content of 2^24 at the centre of an open 11^3 GameBoard at `release`
  [1, 128], 40 intervals: the books close at every tick, the content is
  2^24 at every tick, the momentum on the measured events zero, the flux
  through the cube of half-width 2 equals the emission q = 6 x 2^17 at
  every interval once the front has passed (six beams on the six headings,
  a ballistic stream: Gauss exact); the shell means once steady: the count
  at r = 3 and r = 4 is 6 x 2^17 over the shell's Nodes, the presence at
  r = 3 twice the count and at r = 4 equal to it.
- (d) every example world (`examples/events/*.json`, `bell/`, `coupling/`,
  `detector/` through the entity loader) parses as a NatureBeam world. The orbit
  worlds of series D are research runs registered in
  [EXPERIMENTS](EXPERIMENTS.md#d-the-orbit-under-the-beam-law-on-the-plane-2026-09-19)
  and pinned by no test (the model owner's rule of 2026-09-17; the pin of
  the first registration, `test_orbit_world.py`, went with its numbers
  when the engine changed).
- (e) `two_contents` (the example world: two contents of 2^24 eight Links
  apart on the open 21^3 GameBoard, `release` [1, 128], no suspension) for 20
  intervals: not refused (the night's bound refused it at the 20th
  interval, when the two +y beams of 2^17 click `face:+y` together, 2^18
  in one interval); the books close at every tick; every face's record
  grows at every tick by the Python-int square of the pointer of the rows
  that clicked there (X = sum 32 x amount x C[phase], Y the same with S,
  from the click lines through the tables); at the 20th interval `face:+y`
  records 2^62 exactly, one past the law's bound 2^62 - 1, and `face:+x`,
  clicked 2^17 per interval since the 13th, holds 2^63, beyond int64 and
  round-tripped through JSON; the two pushes are equal and opposite along
  x, toward each other (the third law on lone beams).

## The entity catalog

`tests/test_entity_catalog.py` ([the catalog of the entities](ENTITY_CATALOG.md);
the model owner's decision of 2026-09-20, Highlights 5.4): the four worlds
of `examples/events/catalog/` are placements of external things, not
experiments, so the module pins no number of any world (the model owner's
rule of 2026-09-17) and checks that each world is what its page says it
is, the expectations written down first:

- (a) the shipped files equal the documents `make_worlds.worlds()` writes,
  world by world; each parses through the canonical loader as a world of
  the Beam Law (its `law` the value `world.LAW_VALUE` names, `beam`, never
  a literal in the test; its `model_id` naming the catalog), declares
  `ticks` from 20 through 50, `quantum` on
  every family and `reading` on every declared detector, and its parsed
  measured events are as many as declared;
- (b) each runs its declared intervals headless with the books balanced
  at every interval and the tick at the end equal to the intervals;
- (c) the readings the catalog names exist: every declared detector is in
  the run's detector report with the reading `wave` and an integer
  `record` per family; at least one declared detector of a world that
  declares detectors wrote a `record` line; every probe (a measured event
  whose table passes a family, the clock the catalog reads; the neutron
  star and the clock near the mass declare them) ends with its clock's
  identity, age + waited equal to the intervals run, its owed count a
  non-negative integer.
- (d) the catalog against the parser (2026-09-20): every key a row names in
  an "Its keys today" cell (a backticked identifier, the identifier before
  a colon, the string keys of a backticked JSON object) is a key or a value
  word of `world.py` (`WORLD_KEYS`, `FAMILY_KEYS`, `MEASURED_KEYS`,
  `LAMP_KEYS`, `TABLE_ENTRY_KEYS`, `TRANSIT_KEYS`, `DETECTOR_KEYS`,
  `COLUMN_KEYS`, `BECOME_KEYS`, `WINDOW_READING_KEYS`, the nested keys of
  `rotate` and `gate`, `TABLES`, `READS`, the readings, the faces, the
  border, the boundaries, the gate kinds) or a family or column name a
  registered world declares (the keys of a table object are family names);
  the nested key sets the test spells are checked against the parser (it
  accepts exactly them and refuses one more); at least thirty cells read;
- (e) the register against the catalog: every family name a world under
  `examples/events/` declares (at least twenty names) is named in
  `docs/ENTITY_CATALOG.md` in backticks, in a row or in the family-name
  table, so that a new family cannot enter the register without a row or
  a gap row.

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
Beam Law uses: the working register (`checked_work` accepts +-(2^63 - 1),
refuses one beyond and a boolean); the exact integer square root
(`integer_root`: 0, 1, 2, 3, 4, 15, 16, 17, 2^62 and 2^63 - 1 give 0, 1, 1, 1,
2, 3, 4, 4, 2^31 and 3037000499, each the floor with the next square above the
input; a negative value, a float and an overflow are refused); the bounded gcd
(`bounded_gcd`: 12 and 18 give 6, 0 and 5 give 5, 5 and 0 give 5, -4 and 6
give 2, 0 and 0 give 0, 2^63 - 1 and 1 give 1; an overflow and a boolean are
refused). `by_clock` and `apportion_whole` are pinned where the clock uses
them (`test_nature_beam_clock`, `test_nature_beam_readings`). The component arithmetic of the
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
GameBoard (the model owner, 2026-09-19: an axis may be declared periodic as a run
parameter of the world file, `boundary` `{"z": "periodic"}`; open stays the
default and "closed" and every other word stay refused): on a periodic axis
the departures that would leave the GameBoard through one face are created at
the first Node of the opposite face (`Transit.walk`), nothing escapes on that
axis, the momentum they carry stays on the GameBoard, and with an extent of 1 the
two departures on that axis return to the same Node in the next interval as
its arrivals through those Ports (a four-Port node with a one-interval stub).
One rule for the GameBoard (the model owner, 2026-09-19): a measured event's step
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
| (c) the refusals and the record | `"closed"`, `{"z": "closed"}`, `{"w": "periodic"}`, `{"z": 1}`, `"periodic"`; `{"z": "periodic"}`; no key; the bar of (a) run 3 intervals through `execute_event_run` | each of the five refused by `parse_event_world` naming the closed GameBoard and by `validate_configuration` (valid false, code `validation`); `periodic` (False, False, True), `boundary` `{"z": "periodic"}`, the preflight's summary `{"x": "open", "y": "open", "z": "periodic"}`; without the key `"open"` and (False, False, False); `run.json` with `boundary` `{"z": "periodic"}`, 3 completed ticks, conserved, escaped `[{"family": "light", "amount": 0, "momentum": [0, 0, 0]}]`, `state.json` with the same boundary at tick 3 |
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
| (c) a steady field | a bar of 2 x 1 x 1, `suspension` [1, 4], `release` [1, 128]; a content of 2048 of the free family at the corner x = 0 (five of its six exits off the open GameBoard), a measured event of light (content 1, measuring the free family) at x = 1; 30 intervals | the source is created again every interval (age 30; nothing of another number reaches it) and 16 units reach the probe every interval from the second on (464 taken after 30; since 2026-09-19 a free family's units carry no content, so the probe's content stays [0, 1] where it read [464, 1] before), the presence 16, k = 16 x 1 // 4 = 4; the probe's age after intervals 1 to 7: 1, 2, 2, 2, 2, 2, 3 (a self-creation in interval 2 owing 4, paid in 3 to 6, the next in 7), then once every 5 intervals (12, 17, 22, 27): after 10, 20 and 30 the ages 3, 5, 7, waited 23, 1 owed; age + waited = the interval at every interval; the age after 30 exceeds the age after 10 (slowed by 1 / 5, not frozen) |
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
exceeded, not the retired engine. Bars of 2 x 1 x 1 and a 3^3 GameBoard,
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
resident; since 2026-09-20 the refused step is a contact read through the
occupant's table and the momentum component is handed over,
[the contact](#the-contact-through-the-table)); an open face is a detector, every escape through it a click on
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
minimal GameBoards (Highlights 5.5, "The engine of the law of events: what the
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
  the field fills the GameBoard (0.861, 0.463, 0.174 measured; old 0.995,
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
  engines' keys), `phase_turn` as an unknown family key, a closed GameBoard, a
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
  open GameBoard, `face:+x` ... `face:-z`, since 2026-09-19), `suspension`
  [1, 1], the family's `phase`
  false), `state.json` (the law,
  tick 4, the measured events, Nodes with events) and `events.jsonl`, keeps
  the input as read, and refuses a negative tick count and a used output
  directory.
