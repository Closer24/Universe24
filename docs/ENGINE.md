# The engine

The one engine of Universe24 is the engine of the law of the ray (`rays-v1`;
[Highlights 5.4](HIGHLIGHTS.md#54-the-detector), "DECIDED: the law of the
ray", the model owner, 2026-09-19). Its design and implementation contract is
[the law of the ray](RAY_LAW.md): the ray's record `NatureBeam`, the one
function `nature_beam`, the flight table at 1 / sqrt 3, the eight-slot
collision table and its inverse, the detector's squared record, the
re-emission, the deletions and the expectations. This document is the
bookkeeping around that law as implemented: the code, the board, the frame of
an interval, the books, the world file's refusals, the record and the
preflight. It repeats no rule of the law; where the two would overlap, RAY_LAW
is the owner. The engines before it (the law of events, `events-v1`, of the
evening of 2026-09-19; the law of the shadow; the law of the bit) are in git
([migration](MIGRATION.md#the-law-of-the-ray-on-2026-09-19-rays-v1)).

The code: `src/event_universe/events/` (`world.py` the world file and its
refusals, `measured.py` the measured event's record and the ledger,
`nature_beam.py` the law (the record, the one reading `read_arrivals`, the
flight table, the collision table, the store of records per family and the
function `nature_beam`), `engine.py` the frame (`RaySimulation`: the clocks,
the owed count, the steps, the books, the readings, the snapshot), `run.py`
the artifacts of a run) on `src/event_universe/core/` (`integer.py`,
`lattice.py`, `phase.py`). The tests: `tests/test_ray_readings.py`,
`tests/test_ray_flight.py`, `tests/test_ray_collision.py`,
`tests/test_ray_bijection.py`, `tests/test_ray_detector.py`,
`tests/test_ray_reemission.py`, `tests/test_ray_clock.py`,
`tests/test_ray_window.py`, `tests/test_ray_world_parsing.py`,
`tests/test_ray_worlds.py`, `tests/test_ray_push.py`
([expectations](TEST_EXPECTATIONS.md)). The
worlds: [examples/events/](../examples/events/README.md).

## Per-axis board topology (2026-09-19 implementation amendment)

The owner approved periodic axes as an experiment parameter in
[Highlights 5.4](HIGHLIGHTS.md#54-the-detector). The board is open on every
face by default (`boundary` `"open"`: the edge is infinity; a closed board is
refused), and an axis may be declared periodic (`boundary` an object with any
of `x`, `y`, `z` set to `"open"` or `"periodic"`, the missing axes open, for
example `{"z": "periodic"}`). The declared graph changes; no local law does.

**One Link.** `core.lattice.adjacent_node(shape, periodic, node, port)` is
the one provider of adjacency: for a Port, add its signed unit heading on
its axis; an in-range target is the ordinary neighbour; a coordinate that
exits a periodic axis wraps to 0 after the positive face or to `extent - 1`
after the negative face; `None` only for a transfer through an open outer
face. It neither reads state nor advances time. The flight table decides
when a ray crosses a Link (at most one per interval; RAY_LAW section 3) and
`adjacent_node` says where the Link leads; the ray crosses it whole, its
record unchanged, so with an extent of 1 a ray on a periodic axis lands on
its own Node at every interval the table moves it (the one-interval stub
of a two-dimensional board with `{"z": "periodic"}`). A measured event's
step by its momentum uses the same provider and wraps the same way; with
an extent of 1 it lands on its own Node, no move, the step counted. A
wrapped or plain target that holds another measured event refuses the step
(no merge, the model owner, 2026-09-19: both remain, the mover where it was
with its momentum, the step counted, no record).

**An open face is a detector** (the model owner, 2026-09-19). Every escape
through an open face, a ray in the walk or a measured event's step, is a
`click` on the face detector named by the face (`face:+x`, `face:-x`,
`face:+y`, `face:-y`, `face:+z`, `face:-z`), recorded like a detector's
click and counted in the run's detector record with the face's squared
record of what left; the books' escaped lines are the faces' sums. Nothing
physical changes at the face: the amount, the content and the momentum
leave the board as before. A periodic axis has no faces.

### Diagnostic scope and acceptance

`cube_flux(family, centre, half)` sums the amount of the rays that cross
the six faces of the cube of the given half-width around the centre on an
all-open board, read off the Links crossed per Port (`per_port`, a
diagnostic of the walk, not the reading's moments), read-only; on a world
with any periodic axis it raises `ValueError` (a periodic seam is not a
face). `shell_readings` gives the shell means of the count (the amount that
arrived, the zeroth moment outside), the presence (every ray at the Node)
and the radial flow (the first moment), read-only.
`tools/coupling_readings.py` sums the four in-plane faces itself on the
plane. A thin periodic board is a
compact graph with return Links; it establishes no equivalence with
unbounded three-dimensional space and requires its own experiment
configuration. The independent expectations of the topology are pinned in
[test expectations](TEST_EXPECTATIONS.md#the-flight) (`test_ray_flight` (d)
and (e)).

## The law of the ray (`rays-v1`)

**One thing.** A ray, with a place (a Node) and a record: a direction (an
index into the world's direction table D), an age (the flight phase, modulo
the direction's period), a phase (a step of the circle of N), a number (the
last emitter), an amount (whole units) and a content per unit; its momentum
is not stored, it is amount x content x u_d for a paid family and
amount x u_d for a free one (its unit carries no content), u_d the unit
vector of the direction at the flight table's scale Q = 64 (the integer
vector nearest Q D / |D|, exactly Q e_d on a heading; the model owner's
decision of 2026-09-19, [RAY_LAW section 2](RAY_LAW.md#2-the-record-of-a-ray-and-the-world-file)
and note 23), so every momentum of the record is in label units, Q per
unit of amount along a heading. The Node holds nothing
between intervals but the rays present at it and the measured event there.
The law of one interval at one Node is `nature_beam` ([RAY_LAW section 3](RAY_LAW.md#3-the-nodes-interval-nature_beam)):
the walk by the flight table, the one reading, the collision by the table
(at the Nodes of free space: none at a Node that holds a measured event),
the measured event's table (`read`, `measure`, `rerelease`, `pass`, each
gated by the detector's threshold and its window; the push one bilinear
form over the arriving rays' labels, `push_form`, the emitter's factor
read off the rays' records, nothing looked up by number), the
self-creations (the release, the lamp, what came home and what is
re-emitted) and the merge of identical records. Every piece of logic exists once: one reading
(`read_arrivals`) takes the amount-weighted moments of order 0, 1 and 2 of
the direction vectors of a Node's arrivals (the model owner, 2026-09-19:
valid for a fan as for the six headings; a ray that did not step has the
direction (0, 0, 0) and enters the zeroth moment alone): two scalars
(outside, here), the net flow (sum amount x u_d, on the unit vectors at
the scale Q) and the traceless tensor (3 x sum amount x u (x) u less its
trace, exact integers), and every
coupling selects its component by the declared key `reads` of its table
entry (`scalar` by default: the clock's count and the threshold read the
presence, the push reads the flow, a detector may declare `tensor`); the
detector's coherent record is the same moments over the clicked rays with
their amplitudes as weights (32 x amount at cos and sin over 256), the
scalar squared ([RAY_LAW section 3](RAY_LAW.md#3-the-nodes-interval-nature_beam),
step 2, and section 10, note 16).

**The frame** (`RaySimulation.step`, `engine.py`): for every measured
event, its clock (its age, the turn `by_clock(age, content, K)`, its
release rate, its lamp's rate and window, its owed count) is read and
handed to `nature_beam` with the stores; `nature_beam` returns the readings
(the count, the flow and the presence per Node, dense arrays read-only, and
`per_port`, the amount that crossed into each Node through each Port this
interval, a diagnostic of the walk for Gauss's flux); the frame turns the
phases of the measured events that
self-created, reads the owed count off the clock from the presence
(`_suspend`, `by_clock(age, presence x n, d)`), moves the measured events
by their momentum (`_move`: on an axis whose momentum component is p in
label units, one Link per (Q x S x M + p) / p self-creations,
`by_clock(age, |p|, Q x S x M + |p|)`, M the content, S the world's
`width`, 1 by default, and Q = 64 the label's scale; the model owner's
D1 of 2026-09-19 and the label along the unit vector of the same day,
[RAY_LAW section 3](RAY_LAW.md#3-the-nodes-interval-nature_beam) step 5
and notes 15 and 23; one unit of net flow, the label Q M, gives the speed
1 / (S + 1); at most one Link per interval, x before y before z, only in
an interval where nothing is owed) and books the interval.
`inverse_step` runs the
inverse collision and the inverse walk on a board without a measured event
(the bijection of [RAY_LAW section 3](RAY_LAW.md#3-the-nodes-interval-nature_beam);
with a measured event on the board it refuses: the click is the one-way
border). The frame computes no physics.

### A release costs the emitter by its phase rate

Unchanged in form from the law of events (the model owner, 2026-09-19, "I
approve the proposal"; E = h f): at a self-creation whose turn is
s = `by_clock(age, content, K)` each unit a lamp releases costs it
`quantum` x s content, carries that content per unit and the momentum
`quantum` x s x u_d along its direction (u_d the unit vector at the scale
Q = 64), and gives it to the
measured event that measures it; a turn of 0 releases nothing; a free
family's release costs nothing and its rays carry no content. The recoil of
a release is the negative of the momentum released, summed over the
directions. What comes home (the own number's arrivals) is taken whole and
created again at the next self-creation on the declared directions with
the arriving phase and content, apportioned whole (`apportion_whole`, the
leftover to the direction `age mod n` on); a `rerelease` entry does the
same with another number's rays, stamped with the re-emitter's number.

**The books** (`RaySimulation.books`, the runner's `audit` per tick), exact
at every interval: per family the measured line, in content, initial +
measured (the clicks' content) = current + spent (the lamps' cost) +
escaped (measured events off the board); the transit line, in amount,
initial (the declared `in_transit`) + released (the releases, the lamps,
what came home or was re-released and left again) = current (the rays in
the store) + escaped + absorbed (home, the clicks, the re-releases; what
came home is on the absorbed line until it leaves again); the content line
(`content`), the content carried in transit (amount x content per unit),
the same identity; and the momentum lines: the measured line the sum of
the pushes taken, the labels of what clicked or came home and the recoils,
the transit line the sum over the store of the one label of every row
(`nature_beam.momentum_labels`: amount x content x u_d for a paid family,
amount x u_d for a free family, whose unit carries no content; u_d the
unit vector of the direction at the scale Q, the flight table's
`labels`), the escaped line the faces' sums, every line in label units. For a paid family the three
lines close over the click, the re-emission and the home (measured +
transit + escaped constant; a `read` of a paid ray is a report of its
label, the ray going on); for a free family the push is the form of
[RAY_LAW section 3](RAY_LAW.md#3-the-nodes-interval-nature_beam) step 4
(gravity and electricity) and its release takes no recoil, so its lines
are a report and not a balance. Every escaped line is the sum over the
open faces of the face detectors' clicks (`face_detectors`). Every sum of
the books is exact (`nature_beam.exact_sum`, `exact_column_sums`: in the
register when no partial sum can leave it, in Python integers otherwise).
The measured line is bounded before assignment (`nature_beam.bounded`): a
measured event's momentum after a push or a recoil, the push taken, its
content after a click and what waits to be created again are checked
against 2^62 - 1 (`world.MOMENTUM_BOUND`), and a value beyond it refuses
the run with `OverflowError` naming the measured event, its Node and the
quantity ([expectations](TEST_EXPECTATIONS.md#the-world-file-of-the-ray-law));
the detector's record is not a quantity of the law but a report of the
host and is never refused: the coherent pointer (X, Y) is summed in the
int64 register while the amount a detector Node or a face clicks of one
family in one interval is within `nature_beam.POINTER_AMOUNT_BOUND`
((2^62 - 1) // (32 x 257) = 560759486676481) and in Python integers
beyond it (`nature_beam.coherent_pointer`); the square and the cumulative
record (`Measured.record`, `Ledger.face_record`) are exact Python
integers that can exceed 2^63 in `run.json` and `state.json`, parsed as
arbitrary-precision integers ([RAY_LAW section 5](RAY_LAW.md#5-the-detectors-record-the-re-emission-the-face-detectors)).

**The world** (`events/world.py`; the keys of [RAY_LAW section 2](RAY_LAW.md#2-the-record-of-a-ray-and-the-world-file)).
`law` "rays"; `model_id`; `shape`; `boundary`; `ticks`; `K`; `N` (64 by
default, a power of two from 2 through 4096); `release` `[n, d]` per
direction per self-creation per unit of content of a free family;
`suspension` `[n, d]` (an integer w as `[w, 1]`; 0 or `[0, d]` for none,
recorded as `[0, 1]`); `width` (S, the width of the push, an integer from
1; 1 by default, the step rule as it was); `directions` (the declared primitive vectors beyond
the six headings, each with components in -P .. P, P = `direction_bound`,
64 by default, at most 4096 entries; the table D is the two rest vectors,
the six headings in Port order and these, in that order); `families`
(`name`, `quantum` (required; 0 a free family, 1 or more a paid one: the
kind is derived, never declared), `charge` (a free family only), `phase`
true by default, `phase_per_link` 0 .. N - 1); `measured` (`position`, `family`,
`amount`, `phase`, `charge`, `momentum`, `fixed`, `directions` (the
directions it releases and re-emits on, by vector or by index into D; the
six headings by default), `table` family name to `read` | `measure` |
`rerelease` | `pass` or to `{"rule": ..., "phase_window": s, "reads":
component}` with `reads` one of `scalar`, `outside`, `here`, `vector`,
`tensor`, the table generated from the keys by `world.default_table` (a
free family read, a paid one measured, no window) and the world declaring
only the entries that differ, `rule` optional in the object form, an entry
equal to the default accepted and changing nothing; `lamp` `{rate: [n, d],
directions, phase_window}` on a measured event of a paid family);
`in_transit` (`position`, `family`, `number`,
`direction` (a vector of D, or a rest index 0 or 1), `amount`, `phase`,
optional `age`); `detectors` (`name`, `positions`, `threshold` 1 by
default). Refused, naming the key and the law: `"law": "events"` (pointing
to MIGRATION), `dynamics`, `max_active_owners`, `port_map`, `output`,
`capacity`, `groups`, `reference_phase`, `headings` on a lamp, `heading` on
a ray, the earlier engines' keys (`contents`, `initial_shadows`,
`wait_per_quantum`, `schema_version`, `dense_field`), `phase_turn` as an
unknown key, a closed board, a non-primitive direction, a component beyond
P, a direction the world does not declare, a rest direction on a lamp or a
re-emitter, a repeated direction, a momentum label Q x content x amount
beyond 2^62 - 1 on a declared ray or a lamp's release (content x amount
below 2^56), `phase_per_link` outside 0 .. N - 1 or on
a family without a phase circle, a content at or past K x N / 2 of a family
with a phase, a lamp on a free family, `kind` on a family (pointing to
MIGRATION: the quantum decides the kind), a family without `quantum`, a
negative quantum, a charge on a paid family, two measured events at one
Node, an unknown table rule, N not
a power of two, a detector on a Node without a measured event, a Node in
two detectors, a `phase_window` outside 0 .. N - 1 or on `pass` or for a
family without a phase circle, a table entry object with an unknown key (one
without `rule` takes the family's default rule), a `reads` outside the
reading's components, a `suspension`
denominator of 0 ([expectations](TEST_EXPECTATIONS.md#the-world-file-of-the-ray-law)),
a `width` below 1 or not an integer ([the width of the push](TEST_EXPECTATIONS.md#the-width-of-the-push)).
`event_universe.configuration_validation` reports a world of the law as
kind `rays`.

**The record.** `run.json` carries `law` "rays-v1", the world's keys
(`boundary` as declared; `suspension` as `[n, d]`; `width`; `directions`, the table
D beyond the rest vectors and the headings; per family its `quantum`,
`charge`, `phase` and `phase_per_link`, no `kind`), `numbers`, the books
per completed tick (`audit`) with
`conserved_at_every_completed_tick`, the measured events' final states
(`measured`: position, held per family, content, phase, charge, momentum,
windows, detector, age, owed, what waits to be created again (`home`,
`home_content`), `waited`, phase steps, steps, what each met per family by
rule, the clicks, the push taken and the detector's cumulative `record`),
the detectors (`detectors`: name, Nodes, threshold, per family the amount
measured, the clicks, the content and the cumulative squared `record`;
then the face detectors, one per open face in Port order, with what
clicked there in transit, the `measured_content` of the measured events
that stepped off, the `record` and the `momentum` that left) and the
`escaped` per family (amount, content, momentum). `events.jsonl` holds one
record per event: `home`, `read`, `click`, `rerelease` (per number and
tick, with the amount, the phase, the push and the content), `pass` (a ray
below the threshold, with `threshold`, or outside the window, with
`window`), `step`, and per interval per detector Node and family a `record`
line with the pointer (X, Y) and its square; a `click` on a face detector
names the face, `measured` None for a ray or the number of the measured
event that stepped off. `state.json`, through
`snapshot_writer.write_snapshot`, carries `"law": "rays-v1"`, the
`boundary`, the measured events, the detectors and every Node with rays
(its rows: direction, age, phase, number, amount, content per family, and
on a free family's rows `charge` and `mass`, the emitter's factor of the
electric push carried on the record since the night of 2026-09-19,
[RAY_LAW section 2](RAY_LAW.md#2-the-record-of-a-ray-and-the-world-file)).
`tools/run_series.py` runs these worlds as any.

## The law of events (`events-v1`)

Deleted on 2026-09-19 with the law of the ray (the model owner's rule, one
engine). Its contract, the sides computed from the coherent sum, the
per-Port scatter, the suspension of transit bundles and the phase-less
family's diagonal weights, is in git at any commit before the deletion
(`ce0b22af` the last), summarized in
[migration](MIGRATION.md#the-law-of-the-ray-on-2026-09-19-rays-v1); the
readings registered under it keep their scope in
[EXPERIMENTS.md](EXPERIMENTS.md). The clock, the tables, the phase window,
the release priced by the turn, the face detectors, the refused step and
the one reading set carry over unchanged in form.

## Preflight

`python -m event_universe.configuration_validation WORLD.json [--json]`
decodes a world file strictly (`json_documents`) and parses it with the
engine's own parser without running it; the report names the key at fault, or
summarizes the world (its model, law, shape, ticks, families, measured events
and detectors). A valid report certifies the configuration only, not a run or
any physics. The workspace ([WORKSPACE.md](WORKSPACE.md)) uses the same
preflight and runner.
