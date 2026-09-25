# The engine

The one engine of Universe24 is the engine of the Beam Law (`beam-v1`;
[Highlights 5.4](HIGHLIGHTS.md#54-the-detector), "DECIDED: the law of the
ray", the model owner, 2026-09-19). Its design and implementation contract is
[the Beam Law](BEAM_LAW.md): the row (the record of an event in transit,
`NatureBeam` in the code; "ray" its name until the rows-and-bodies decision
of 2026-09-21, record 183; [the glossary](TERMINOLOGY.md)), the one
function `nature_beam`, the flight rule at 1 / sqrt 3, the eight-slot
collision table and its inverse, the detector's squared record, the
re-emission, the deletions and the expectations. This document is the
bookkeeping around that law as implemented: the code, the GameBoard, the frame of
an interval, the books, the world file's refusals, the record and the
preflight. It repeats no rule of the law; where the two would overlap, BEAM_LAW
is the owner. The engines before it (the law of events, `events-v1`, of the
evening of 2026-09-19; the law of the shadow; the law of the bit) are in git
([migration](MIGRATION.md#the-law-of-the-ray-on-2026-09-19-rays-v1)).

The physical path (`nature_beam.py`, `meeting.py`, `engine.py`, `world.py`,
`amplitude.py` on `core/integer.py` and `core/phase.py`) is the six verbs on
bounded integers and nothing else (the model owner, records 181, 202 and
929; every coupling of the atom worlds and the light worlds read against
the six in [COUPLINGS.md](designs/couplings_algebra/COUPLINGS.md)), gated by
`tests/test_integer_algebra.py` (the Register Architect's, record 920 (A));
beneath it two integer roots are taken at run time, each declared by its
design: the meeting's norm under the key `meeting` (`meeting.py:359-361`,
BEAM_LAW note 35) and the pushed row's pair under the key `optical`
(`nature_beam.py:3549`, EVERY_FAMILY.md; being replaced on PR #855).

The code: `src/event_universe/events/` (`world.py` the world file and its
refusals, `measured.py` the measured event's record and the ledger,
`nature_beam.py` the law (the record, the one reading `read_arrivals`, the
flight rule, the collision table, the store of records per family and the
function `nature_beam`), `meeting.py` the meeting (since 2026-09-20: the arc
permutation of the direction table, the reading of the free crowd by a paid
unit in transit, the turn by its phase register and the inverse, under the
world key `meeting`; [BEAM_LAW section 3 step 3 and note 35](BEAM_LAW.md#3-the-nodes-interval-nature_beam)),
`engine.py` the frame (`NatureBeamSimulation`: the clocks,
the owed count, the steps, the books, the readings, the snapshot), `run.py`
the artifacts of a run) on `src/event_universe/core/` (`integer.py`,
`game_board.py`, `phase.py`). The tests: `tests/test_nature_beam_readings.py`,
`tests/test_nature_beam_flight.py`, `tests/test_nature_beam_collision.py`,
`tests/test_nature_beam_bijection.py`, `tests/test_nature_beam_detector.py`,
`tests/test_nature_beam_reemission.py`, `tests/test_nature_beam_clock.py`,
`tests/test_nature_beam_window.py`, `tests/test_window_width.py`, `tests/test_nature_beam_window_reads.py`,
`tests/test_nature_beam_world_parsing.py`,
`tests/test_nature_beam_worlds.py`, `tests/test_nature_beam_push.py`, `tests/test_nature_beam_age.py`,
`tests/test_meeting.py`, `tests/test_amplitude_record.py`,
`tests/test_amplitude_split.py`, `tests/test_amplitude_layer.py`,
`tests/test_amplitude_pair.py`, `tests/test_amplitude_gate.py`
([expectations](TEST_EXPECTATIONS.md)). The
worlds: [examples/events/](../examples/events/README.md).

## Per-axis GameBoard topology (2026-09-19 implementation amendment)

The owner approved periodic axes as an experiment parameter in
[Highlights 5.4](HIGHLIGHTS.md#54-the-detector). The GameBoard is open on every
face by default (`boundary` `"open"`: the edge is infinity; a closed GameBoard is
refused), and an axis may be declared periodic (`boundary` an object with any
of `x`, `y`, `z` set to `"open"` or `"periodic"`, the missing axes open, for
example `{"z": "periodic"}`). The declared graph changes; no local law does.

**One Link.** `core.game_board.adjacent_node(shape, periodic, node, port)` is
the one provider of adjacency: for a Port, add its signed unit heading on
its axis; an in-range target is the ordinary neighbour; a coordinate that
exits a periodic axis wraps to 0 after the positive face or to `extent - 1`
after the negative face; `None` only for a transfer through an open outer
face. It neither reads state nor advances time. The flight rule decides
when a row crosses a Link (at most one per interval; BEAM_LAW section 3) and
`adjacent_node` says where the Link leads; the row crosses it whole, its
record unchanged, so with an extent of 1 a row on a periodic axis lands on
its own Node at every interval the table moves it (the one-interval stub
of a two-dimensional GameBoard with `{"z": "periodic"}`). A measured event's
step by its momentum uses the same provider and wraps the same way; with
an extent of 1 it lands on its own Node, no move, the step counted. A
wrapped or plain target that holds another measured event refuses the step
(no merge, the model owner, 2026-09-19: both remain, the mover where it was,
the step counted) and, since 2026-09-20, the refused step is a **contact
read through the occupant's table** (the model owner, on the physicist's
design of the strong force; [BEAM_LAW note 31](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)
(ix)): the occupant's table entry for the body's family decides as it
decides for a row, `measure` (the keys' rule for a paid arrival, the body's
momentum its own label; the rule wherever the entry is the keys' own for
the body's family, declared or not) handing the body's momentum component
on that axis to the occupant (the body's 0, the occupant's raised by it,
the sum unchanged), `rerelease` returning it (the body's component
reversed, the occupant's raised by twice it), `pass` and a `read` declared
against the keys (on a paid family) leaving the labels as they were (the
rule as it was, no record). A body on a set whose destination set holds several
occupants hands the component apportioned whole over them by their
contents. Each hand-over is a `contact` record. **The contact's give**
(since 2026-09-20, `binding-v1`,
[BEAM_LAW note 40](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation);
`engine._give`): at the first hand-over under `measure` of a contact the
refused body also gives the paid content it carries (`held` of a paid
family other than its own; a lamp's own content is not carried) to the
flight, per such family with the quantum h `held // h` units of content h
as one row at its Node on the heading opposite to the refused step (the
step's sign, not the momentum's), the recoil (minus the row's label) on
the body, `held mod h` kept, the content
booked on the family's `spent` line and the row on its transit and content
lines as a lamp's release is; the rows then have the law's fates by the
tables and the border. A body that carries nothing gives nothing, and the
contact is the hand-over alone, bit for bit.

**An open face is a detector** (the model owner, 2026-09-19). Every escape
through an open face, a row in the walk or a measured event's step, is a
`click` on the face detector named by the face (`face:+x`, `face:-x`,
`face:+y`, `face:-y`, `face:+z`, `face:-z`), recorded like a detector's
click and counted in the run's detector record with the face's squared
record of what left; the books' escaped lines are the faces' sums. Nothing
physical changes at the face: the amount, the content and the momentum
leave the GameBoard as before. A periodic axis has no faces.

**The border `lifetime`** (the model owner, 2026-09-20, "the event whose
age reaches L makes no next event but an escape click in the ledger, as at
an open face"). A family that declares a `lifetime` L has a detector
without Nodes named `lifetime`, listed after the faces: a row of the family
whose age reaches L at the end of its walk (after the reads of that
interval, before the merge; read by the one primitive, `nature_beam.ages_at_key`,
`by_clock(age - 1, 1, L)` = 1 at the walk that brought the age to L, as
the world's `age_bound` is read against the key age_bound + 1 and the
clock reads the turn; the four unifications (2)) is a `click` on it, recorded like a face click
(the tick, the Node the row was on, `measured` None, the family, the
number, the amount, the phase, the momentum, the content), booked as an
escape in the ledger's lifetime lines and summed into the escaped lines
beside the faces. The inverse interval is refused on such a GameBoard.

### Diagnostic scope and acceptance

`cube_flux(family, centre, half)` sums the amount of the rows that cross
the six faces of the cube of the given half-width around the centre on an
all-open GameBoard, read off the Links crossed per Port (`per_port`, a
diagnostic of the walk, not the reading's moments), read-only; on a world
with any periodic axis it raises `ValueError` (a periodic seam is not a
face). `diagnostics.shell_readings.shell_readings(simulation, family, centre,
radius)` (a host diagnostic outside the engine since 2026-09-21; before, the
engine's method) gives the shell means of the count (the amount that
arrived, the zeroth moment outside), the presence (every row at the Node)
and the radial flow (the first moment), read-only, in floating point.
`tools/click_readings/coupling.py` sums the four in-plane faces itself on the
plane. A thin periodic GameBoard is a
compact graph with return Links; it establishes no equivalence with
unbounded three-dimensional space and requires its own experiment
configuration. The independent expectations of the topology are pinned in
[test expectations](TEST_EXPECTATIONS.md#the-flight) (`test_nature_beam_flight` (d)
and (e)).

## The Beam Law (`beam-v1`)

**One thing.** A row, with a place (a Node) and a record: a direction (an
index into the world's direction table D), an age (the count of intervals
since the measured event that created it, whole since 2026-09-20; the
flight reads it modulo the direction's period, a measured event reads it
whole), a phase (a step of the circle of N), a number (the
last emitter), an amount (whole units) and a content per unit; its momentum
is not stored, it is amount x content x u_d for a paid family and
amount x u_d for a free one (its unit carries no content), u_d the unit
vector of the direction at the flight's scale Q = 64 (the integer
vector nearest Q D / |D|, exactly Q e_d on a heading; the model owner's
decision of 2026-09-19, [BEAM_LAW section 2](BEAM_LAW.md#2-the-record-of-a-ray-and-the-world-file)
and note 23), so every momentum of the record is in label units, Q per
unit of amount along a heading. The Node holds nothing
between intervals but the rows present at it and the measured event there.
The law of one interval at one Node is `nature_beam` ([BEAM_LAW section 3](BEAM_LAW.md#3-the-nodes-interval-nature_beam)):
the walk by the flight rule, the one reading, the collision by the table
(at the Nodes of free space: none at a Node that holds a measured event),
the measured event's table (`read`, `measure`, `rerelease`, `pass` and,
since 2026-09-20, `become`, the transformation, each
gated by the detector's threshold and its window; the push one bilinear
form over the arriving rows' labels, `push_form`: one product per
arriving free row, `M_A x (rho_A rho_B - 1) x V_B` with the families'
charges per unit of content, nothing on the record but the row's number
and nothing looked up by number), the
self-creations (the release, the lamp, what came home and what is
re-emitted) and the merge of identical records. Every piece of logic exists once: one reading
(`read_arrivals`) takes the amount-weighted moments of order 0, 1 and 2 of
the direction vectors of a Node's arrivals (the model owner, 2026-09-19:
valid for a fan as for the six headings; a row that did not step has the
direction (0, 0, 0) and enters the zeroth moment alone): two scalars
(outside, here), the net flow (sum amount x u_d, on the unit vectors at
the scale Q) and the traceless tensor (3 x sum amount x u (x) u less its
trace, exact integers), and every
coupling selects its component by the declared key `reads` of its table
entry (`scalar` by default: the clock's count and the threshold read the
presence, the push reads the flow, a detector may declare `tensor`); the
detector's coherent record is the square of the first moment of the same
reading over the clicked rows, taken on the circle's unit vectors
(C[phase], S[phase], 0) with their amplitudes 32 x amount as weights
(`nature_beam.coherent_pointer` through `read_groups`, the one table;
[BEAM_LAW section 3](BEAM_LAW.md#3-the-nodes-interval-nature_beam),
step 2, and section 10, notes 16 and 33).

**The frame** (`NatureBeamSimulation.step`, `engine.py`; the bodies are
moved one after another in number order, a declared tie: when two bodies
step in one interval and one's destination is the other's Node, the lower
number steps first, [BEAM_LAW note 31 (ix)](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)):
for every measured
event, its clock (its age, the turn, the count of its accumulator `acc_turn`
at the rate `content x n` over d, the clock's rate `K` = [n, d], an integer K
being [1, K] (`NatureBeamWorld.turn`; the four unifications (2), 2026-09-20:
the turn is the free release's own form at the rate [1, K]; since the
fraction-free law of the same day, [BEAM_LAW note 41](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation),
every count of the clock is `by_drive` on the body's own accumulator, the
same integers as `by_clock(age, content x n, d)` at a constant content
from age 0; the counts are one table on the record, `Measured.counts`,
whose one loop `CountTable.advance` runs every row through `by_drive` and
hands the whole part to the count's consumer, the turn here, the owed
count at `_suspend`, the release and the lamp at step 5, the drive and
the turn by momentum at `_move`, the push at the reading), its
release rate, its lamp's rate and window, its owed count) and its content
(`frame_content`, read once before the law: M_A of the interval's push,
the same whatever the order in which the families' clicks join `held`
within the interval; [BEAM_LAW note 27](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation))
are read; since the crossing rule (2026-09-21; [BEAM_LAW note 48](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation),
the model owner's record 158) the measured events then STEP by their
momentum (`_move`, below: a body's departure becomes its arrival as a
row's does in the walk, so the law reads a body at its destination and
reads there what it met by the step itself; until then the step was the
interval's last act and the destination was read one interval later),
and the stores are handed to `nature_beam`, which returns the readings
(the count, the flow and the presence per Node, dense arrays read-only, and
`per_port`, the amount that crossed into each Node through each Port this
interval, a diagnostic of the walk for Gauss's flux); the frame turns the
phases of the measured events that
self-created, reads the owed count as the count of the body's accumulator
`acc_owed` at the rate k x n over d from what the clock
counted (`_suspend`, `count_owed`; the same integers as `by_clock(age, k x n, d)` at a constant crowd from age 0, k the age moment
`sum amount x age` over the same set since `clock-age-v1` (2026-09-21, the
model owner's word, record 394), or for a family whose table entry reads
`presence` the presence, `measured.count_component`, `Measured.counted`;
the age word's shape one wall function of the crowd, `core.integer.age_wall`,
the rate r x d against the wall w x (d + c k n) over the declared set
`measured.AGE_WALL_SET` of accumulators with a coefficient c each, today the
clock at c = 1, the owed count the excess of its stretched wall over its
stretched rate in units of d, integer for integer as before, and the row's
flight at c = 1 + gamma (the law's own since 2026-09-22, the generic entry
of the bending, the model owner's word of record 847; gamma the
world's declared `optical`, 0 by default), the phase per age never
(`AGE_WALL_NEVER`);
[BEAM_LAW section 10](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation),
note 25) and books the interval. The step of a measured event
by its momentum (`_move`, before the law: on an axis whose momentum component is p in
label units, one Link per (Q x S x M + p) / p self-creations, M the
content, S the world's `width`, 1 by default, and Q = 64 the label's
scale; since 2026-09-20 the step drive, [BEAM_LAW note 17](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)
as amended: the body's record carries per axis `drive`, the signed
distance the momentum has driven since the last step, `drive += p` at
every self-creation in which it may step and a step on the + side when
`drive >= Q x S x M + |p|` or on the - side when `drive <= -(Q x S x M +
|p|)`, that much subtracted with the sign (record 126: signed, so a
reversal first cancels what was driven the other way), so the count of
Links is the whole part of the driven distance, bit-identical at a constant momentum to
`by_clock(age, |p|, Q x S x M + |p|)` and never two Links in one
interval, the count primitive `core.integer.by_drive` (record 108: the
whole part of an accumulated rate on the reader's record; the clock's
turn, the owed count, the release and the lamp keep `by_clock`, the same
count where the rate is constant); the drive of every axis advances at every such self-creation,
and a later axis whose drive reaches its D in the interval of an earlier
axis's step loses that Link, its D subtracted, as the frame lost it
before; the model owner's D1 of 2026-09-19 and the label along the unit
vector of the same day,
[BEAM_LAW section 3](BEAM_LAW.md#3-the-nodes-interval-nature_beam) step 5
and notes 15 and 23; one unit of net flow, the label Q M, gives the speed
1 / (S + 1); at most one Link per interval, x before y before z, at a
self-creation (an interval where nothing was owed at the frame), the
drive advanced by the momentum after the previous interval's push (the
step precedes the law: at a constant momentum the same Links at the same
self-creations, under a push a fire can fall one interval later than it
did before the crossing rule); the rule of one axis is
`engine.step_axis`, the owed count `engine.count_owed`, each the one place
its rule lives and what the readings tools read; under the world key
`drive_b` (`drive-b-v1`, 2026-09-22, off by default,
[BEAM_LAW note 49](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation))
the three drives gain `p_a Q` each against the one wall `world.drive_wall`
(Q^2 S M + |p|_1 T_h, T_h = 110) and the axis furthest over it steps
(`core.integer.by_line`): the line of the momentum, the coincident fire
deferred and never lost, the record's fields unchanged; `run.json`, `state.json`
and the `step` line carry `drive` and the state `axis_steps`, and since
the crossing rule the body's two marks `step_port` and `last_step_port`,
the Ports of its own two last Links, -1 without one (a refused step, an
escape, no fire), which the reading reads as the headings e and e' of
the rule) is a contact when its destination holds another measured
event, an escape when it leaves through an open face, both before the
law: a row given at a contact makes its first Link in the interval of
the give, and the rows a body releases in the interval of a step are
born at its destination with the phase turned at the Link.
A measured event on a set of Nodes (`span`, [BEAM_LAW note 30](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation);
`Measured.span`, `Measured.nodes`, `world.body_nodes`) is one record on
all of them, and since the four unifications (2026-09-20, (3),
[BEAM_LAW note 33](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation))
its set is the one set object a detector is too: `DetectorSet.nodes` maps
every Node of the set to the measured event there (a body one event, a
declared detector several), `Measured.nodes` reads a body's Nodes from its
set, `NatureBeamSimulation.at` maps every occupied Node to its set
(`occupant` to the event's number) and `_place` moves a body's Nodes in
both as it steps; the step
moves the whole set as one (refused when a Node of the moved set holds
another measured event; the whole body clicks on the face when any of its
Nodes would leave; every Node wraps on a periodic axis), and `nature_beam`
reads its arrivals over the set (one moment table per family over the
rows at the set, the presence and the age moment its zeroth and age
moments over the present rows, the record's component and the push's flow
its moments over the admitted rows; since the crossing rule the admitted
rows are the crossings, [BEAM_LAW note 48](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation):
the arrivals but for a row that came over the body's own Link behind it,
the entered Nodes' residents against the step and the rows that crossed
the trailing face's Links the other way, each read on its own direction)
and apportions its releases over it.
The turn by momentum (the world key `action`, h, and the measured-event
key `phase_by_momentum`; [BEAM_LAW note 30 (ii)](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation);
the model owner's decision of 2026-09-20 on Bohr, "put it as parameters
outside the GameBoard like the age") is applied in `_move` at the Link a
body steps: since the model owner's record 155 of 2026-09-20 (no tables;
[BEAM_LAW note 41 (i) and (viii)](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation))
it is the `action` row of the body's table of counts, one row per axis:
at every Link the step rule counts on an axis whose momentum component is
p (a Link crossed, a Link lost to an earlier axis's step in the same
self-creation, a Link refused at a contact) the row gains |p| x N (N the
phase circle's steps) over h (the world's `action`), and the whole part
the row then holds turns the phase at the Link crossed; at a Link not
crossed that whole part is discarded and the residue kept (note 41
(viii), the owner's item 9, pinned by `tests/test_step_drive.py` (e)); at
a constant momentum the same integers as the retired `by_clock(k0, |p| x
N, h)`, the difference of two floors at k0 the count of the rule's fires
on the axis, and the exact sum of the momentum's history where it
changes; the axes compose; the product |p| x N is bounded before it is
formed; without `action` there are no rows and nothing turns. `run.json`
and `state.json` carry the three accumulators as `acc.action` beside
`drive` and `axis_steps`. A rule of the measured event, the external
thing, read from its own record; the rows' flight and collision are
untouched.
`inverse_step` runs the
inverse collision and the inverse walk on a GameBoard without a measured event
(the bijection of [BEAM_LAW section 3](BEAM_LAW.md#3-the-nodes-interval-nature_beam);
with a measured event on the GameBoard it refuses: the click is the one-way
border). The frame computes no physics of the row; the measured event's
clock rules (the turn, the owed count, the step rule with the width) are
its own, placed in the frame by design ([BEAM_LAW section 9](BEAM_LAW.md#9-implementation-plan-one-pr-one-agent-and-risks)).

**Families from a definitions file** (2026-09-20, `event-entities-v2`,
[entity definitions](ENTITY_DEFINITIONS.md#families-in-definitions-event-entities-v2-2026-09-20)):
a world that places entity definitions may take its `families` from them,
merged by name into the expanded world before this parser reads it (the
inline families first, then the instances' in declaration order, a
differing key refused naming the family and the key); the parser sees one
ordinary `families` list and applies every rule above to it. The shipped
definitions are `examples/events/entities/families.json` and
`apparatus.json`; since 2026-09-20 the registered worlds of every series
reference `families.json` (`../entities/families.json`, a climb of one
level the loader admits), their generators writing the reference in place
of the families it defines; a world whose family differs from its
definition keeps that family inline.

### A release costs the emitter by its phase rate

Unchanged in form from the law of events (the model owner, 2026-09-19, "I
approve the proposal"; E = h f): at a self-creation whose turn is
s = `by_clock(age, content x n, d)` at the clock's rate `K` = [n, d] (an
integer K is [1, K]) each unit a lamp releases costs it
`quantum` x s content, carries that content per unit and the momentum
`quantum` x s x u_d along its direction (u_d the unit vector at the scale
Q = 64), and gives it to the
measured event that measures it; a turn of 0 releases nothing; a free
family's release costs nothing and its rows carry no content, and it goes
whole on every declared direction (n directions, n rows each of the count
the family's release accumulator gained; a paid family's pending rows are
apportioned whole over them). The recoil of
a release is the negative of the momentum released, summed over the
directions. What comes home (the own number's arrivals) is taken whole and
created again at the next self-creation on the declared directions with
the arriving phase and content, apportioned whole (`apportion_whole`, the
leftover to the direction `age mod n` on); a `rerelease` entry does the
same with another number's rows, stamped with the re-emitter's number.

**The books** (`NatureBeamSimulation.books`, the runner's `audit` per tick), exact
at every interval: per family the measured line, in content, initial +
measured (the clicks' content) = current + spent (the lamps' cost) +
escaped (measured events off the GameBoard); the transit line, in amount,
initial (the declared `in_transit`) + released (the releases, the lamps,
what came home or was re-released and left again) = current (the rows in
the store) + escaped + absorbed (home, the clicks, the re-releases; what
came home is on the absorbed line until it leaves again); the content line
(`content`), the content carried in transit (amount x content per unit),
the same identity; and the momentum lines: the measured line the sum of
the pushes taken, the labels of what clicked or came home and the recoils,
the transit line the sum over the store of the one label of every row
(`nature_beam.momentum_labels`: amount x content x u_d for a paid family,
amount x u_d for a free family, whose unit carries no content; u_d the
unit vector of the direction at the scale Q, the flight's
`labels`), the escaped line the faces' sums, every line in label units, and, since
2026-09-20, the `turned` line (`Ledger.turned_momentum`, per family under
`families[<name>].turned` and the world's total under `momentum.turned`):
what the meetings of the family's units in transit moved the transit
momentum line by, `weight x (u_d' - u_d)` summed over the turns
([BEAM_LAW section 3](BEAM_LAW.md#3-the-nodes-interval-nature_beam) step 3,
the meeting under the world key `meeting`; zero without it), and, since
stage (vii) step 3 of the amplitude law (the K finding of 2026-09-20),
the `remainder` line in a recorded world (`Ledger.remainder_momentum`,
per family and under `momentum.remainder`): a record's row pushes a body
with its share amount^2 / m of the quantum's unit label (the record's
norm in m, a record's shares summing to one), since the model owner's
record 155 of 2026-09-20 ([BEAM_LAW note 41 (viii)](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation))
the whole part of the row's own accumulator plus label x amount in units
of m, toward zero, with the remainder kept on the row
(`nature_beam.share_of`; the store's `share_x`, `share_y`, `share_z`,
written as `share` on the row's line of `state.json`), so that a row
read at every interval of a passage pushes the exact sum over the
passage and the push of a `read` moves the remainder line by nothing;
the residue leaves with the row when it is absorbed (the click's push,
the entry's momentum; the `share` beside the `push` on the click line)
or comes home, to the remainder line with the rest of the label, and the
line gives the born labels less the recoil at the recoil of a paid
re-creation (the born rows' shares, a lamp's birth and a split alike),
while the transit line carries the rows' whole labels; so measured +
transit + escaped + cancelled + remainder moves only by the pushes, the
turns and the escapes, and the remainder line reads what left with
absorbed rows and homes, nothing of a row that lives; a row of no record
pushes by its label as it did. A body on a set of Nodes places its
releases over its Nodes by their claims, the `place` rows of its table of
counts (`nature_beam.place_over_nodes`, every Node within one unit of its
equal share of all the body has released; `acc.place` in `run.json` and
`state.json`). For a paid family the three
lines close over the click, the re-emission and the home (measured +
transit + escaped constant; a `read` of a paid row is a report of its
label, the row going on), and under the meeting the transit line moves
by the `turned` line, a report as the free push on a body is (measured +
transit + escaped - turned constant); for a free family the push is the form of
[BEAM_LAW section 3](BEAM_LAW.md#3-the-nodes-interval-nature_beam) step 4
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
quantity ([expectations](TEST_EXPECTATIONS.md#the-world-file-of-the-beam-law));
the detector's record is not a quantity of the law but a report of the
host and is never refused: the coherent pointer (X, Y), the first moment
of the one reading over the circle, is taken in the int64 register where
the reading's bound holds for its table (`nature_beam.reading_fits`:
32 x amount x 256^2 x the rows of the group within 2^62 - 1) and in
Python integers beyond it (`nature_beam.coherent_pointer`,
`moment_table(exact=True)`); the square and the cumulative
record (`DetectorSet.record`, `Ledger.face_record`) are exact Python
integers that can exceed 2^63 in `run.json` and `state.json`, parsed as
arbitrary-precision integers ([BEAM_LAW section 5](BEAM_LAW.md#5-the-detectors-record-the-re-emission-the-face-detectors)).
**The detector is a set of Nodes with one record** (the model owner,
2026-09-19): `NatureBeamSimulation.detector_sets` holds one `DetectorSet` per
declared detector (its name, its `reading`, its threshold, its measured
events, its record per family and its phase at the last click) and one
per measured event outside every declared detector (a detector of one
Node with the default reading); every measured event points to its set
(`Measured.detector_set`; `Measured.threshold` is the set's). The
threshold (the amount summed over the set under both readings; the gate
on the square of the coherent pointer under `wave`, issue #359 step A of
2026-09-20 and [BEAM_LAW note 32](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation),
is deleted at stage (vii) step 4, the one click: a record's click is its
ladder's, and the crowd's pointer gives the set's phase and its record,
not a gate), the window under `wave`, the pointer, the record and the
pairing under `beam` are taken over the set by `nature_beam` step 4; the
click's content, momentum and re-emission stay at the Node the row
reached ([BEAM_LAW section 5](BEAM_LAW.md#5-the-detectors-record-the-re-emission-the-face-detectors)).
After a click the set's phase is written on every measured event of the
set before the frame adds the turn (`step`: the click sets the phase in
the law, the frame turns it by `turn` after).

**The world** (`events/world.py`; the keys of [BEAM_LAW section 2](BEAM_LAW.md#2-the-record-of-a-ray-and-the-world-file)).
`law` "beam"; `model_id`; `shape`; `boundary`; `ticks`; `K` (the clock's
rate: an integer K, the content per phase step per self-creation, read as
the pair `[1, K]`, or since 2026-09-20 a pair `[n, d]` of phase steps per
unit of content per self-creation like `release`, the turn `by_clock(age,
content x n, d)`, refused at half the circle, `NatureBeamWorld.turn_rate`;
the record carries the key as declared; every example world declares the
integer); `N` (64 by
default, a power of two from 2 through 65536, the tables' one bound
`core.phase.MAX_PHASE_STEPS`, raised from 4096 on 2026-09-20 by the model
owner so that a table at 2N exists for every N up to 32768); `release` `[n, d]` per
direction per self-creation per unit of content of a free family;
`suspension` `[n, d]` (an integer w as `[w, 1]`; 0 or `[0, d]` for none,
recorded as `[0, 1]`); `width` (S, the width of the push, an integer from
1; 1 by default, the step rule as it was); `action` (h, the quantum of
action of the turn by momentum, an integer from 1; absent by default:
nothing turns by momentum); `age_bound` (the largest age a
row may carry, an integer from 1; twice the flight bound by default on a
GameBoard with an open axis, required on a GameBoard periodic on every axis; a run
in which a row on the GameBoard carries an age beyond it is refused); `meeting`
(since 2026-09-20, true or false, false by default: under it every paid
unit in transit reads the free crowd of the other numbers at every
free-space Node after the collision and turns toward it by its phase
register, [BEAM_LAW section 3](BEAM_LAW.md#3-the-nodes-interval-nature_beam)
step 3 and note 35; refused with a paid family without a phase circle,
and refused when it is not true or false; the record carries it and the
identity `meeting-v1` under `hypotheses` when it is true); `optical`
(since 2026-09-21 `optical-v1` in its generic form under its key, the
model owner's "go" of record 303 and "clearly, in the generic form",
records 421 to 428, docs/designs/one_wall/NOTE.md; since 2026-09-22 the
law's own for every world, the generic entry of the bending, the model
owner's word of record 847, "bring it back immediately": gamma,
the post-Newtonian parameter, a non-negative integer, 0 by default, the
time part alone, the law's own number; nature's 1 a declaration per world
and never a default, record 817; the row's flight is a member of the age
wall's declared set at the coefficient f = 1 + gamma (`measured.age_wall_set`: the rate 2 S_1 Q d against the
wall 2 T_D (d + f n A), A the crowd's age moment at the row's Node read
before step 1, one interval retarded, the accumulator a field of the row
with its residue, `nature_beam.optical_walk_step`, one Link per interval
by the primitive's own cap with the surplus kept; the click's exact
phase reads the stored accumulator), and after the collision every row
of content in free space is pushed by the interval's arrival flow at its
Node (the interval's own arrivals, read after the walk and the
collision, the crossing rule's set), **W** -= n (1 + gamma) content e_D
**V**, and its label follows the line of its whole momentum **P** =
Q d content **u**_D + **W** by Bresenham (the model owner's GO of record
536): the row's error accumulator **c** = the sum of **h** x **P** over
its walked Links (the fields `cross`, read from the first push on), the
label chosen among D and its fan neighbours as the one whose next Link
**h** advances along **P** and keeps |**c** + **h** x **P**|^2 smallest,
ties to D, the momentum conserved across the turn; a pushed row's pace
is its momentum's (the chief physicist's word of 2026-09-21, DERIVED:
the flight's one rule is the Euclidean pace 1 / sqrt 3 along the line
walked, and the line walked is **P**'s): the pair in its wall is the
primitive **P**'s (**P** over the gcd of its components), S_1(P) and
T(P) = isqrt(3 |P|^2 Q^2), the rate 2 S_1(P) Q d against the wall
2 T(P) (d + f n A) (`nature_beam.momentum_pair`), and its residue is
rescaled by S_1(P') / S_1(P) at every push, the label's S_1 before the
first, floor, the sub-unit remainder dropped (record 496's rule for the
time of the last Link, generalised: the pace's direction changed), not
at the label's turn; the label D is then the phase's, the click's
momentum label and the books' alone (records 494 and 496;
`nature_beam.optical_turn`, the books' `turned` line); refused with gamma out of range; at
`suspension` 0 nothing is stretched and nothing pushed; under `meeting`
the meeting's turn keeps the heading and this turn does not act (one turn
verb per row); a direction without a neighbour within a right angle turns
to nothing (the three refusals of optical-v1 lifted on 2026-09-22); with the key `massive_rows` admitted
since 2026-09-22 (every family under one wall,
[docs/designs/one_wall/EVERY_FAMILY.md](designs/one_wall/EVERY_FAMILY.md):
every row walks by its own family's table under the one wall, a pushed
row by the pair of its momentum with the family's rest term,
`nature_beam.row_pairs` and `momentum_pair`, the wall's square refused
naming the rule before it is formed, and is pushed at the weight per
unit (E'_D^2 + 3 gamma p_D . p_D) // E'_D on the family's labels,
`nature_beam.unit_weights`; the refusal of record 510 lifted); the
inverse interval refused at a pair with n > 0 (a row's wall reads the
crowd of the interval before, which the after-state does not hold); the
record carries the block `optical` {gamma, flight_coefficient} for every
world and no identity (`optical-v1` names no hypothesis since
2026-09-22); a world at [0, d] or with no crowd walks integer for integer
as before, its record and its state byte for byte: the stretch is n / d
times the crowd's age moment and the push n times its flow, and the
snapshot writes a row's flight accumulator only where a crowd moved it
off the table's own count at its age, the value the walk seeds from
(`tests/test_optical.py` (e), the gate set's digests), and by the same
test the click's exact time is the count's own on a row no crowd moved
and the accumulator's where one did, in ONE form for every row of every
world, (age r - s + T d) / r with T the half wall of the row's present
pair, the start its accumulator was seeded from (`optical_last_link`, the
walk's `last_link`; the physics-rule reviewer's line on PR #855: a row no
crowd moved reads the count's own floor, made T_d / (S_1 Q), by identity,
and no row reads two forms; the amplitude worlds' clicks byte for byte);
the pushed row's wall T(P) is a comparison ladder of squares, no root in
the interval (`nature_beam.square_ladder`; since the ring worlds of
flow-link-v1, 2026-09-22, the split ladder `nature_beam.split_ladder`:
the wall's square X = R^2 + 3 |P|^2 is bounded, X Q^2 never formed, T = Q a
+ b reached by a ladder on X and a ladder on the remainder, the same
floor; the physics-rule reviewer's route (b)); a row
whose direction a collision or the meeting changed reads its age on its
present line, its accumulator the table's own count there
(`nature_beam.reseed_flight`, the crowd's carry on the old line dropped
with the old line), so two rows alike on the new line are alike in the
merge; the inverse interval at n = 0 returns the rows fresh, the store
bit for bit (`tests/test_nature_beam_bijection.py`, `tests/test_meeting.py`
(e)); at the register's
crowd worlds at a pair with n > 0 the light is stretched by the crowd's
age moment as the clocks are, which is the law and their inputs' number
(the standing of the 32 registered crowd worlds at such a pair: the
model owner's word of record 871, not needed, not in the paper, the
Register Architect's to remove; series T's four stay with NATURE row
12 and are redeclared in the weak field); with the key `drive_b`
beside it (the body's drive under the one wall, step 3, 2026-09-22,
[docs/designs/one_wall/BODY_DRIVE.md](designs/one_wall/BODY_DRIVE.md))
the body's directional drive is a member of the age wall's set at the
coefficient gamma (`measured.age_wall_set`: the clock 1, the flight
1 + gamma, the drive gamma, at gamma 0 declared at 0 and unstretched;
the rates x d against the wall x (d + gamma n A) in `engine._move`), a
moving body's gravity charge is (w, Q S), the rows' weight on its
momentum over the label scale (`world.body_weight`, gravity's Lambda
Q S), and a moving body at gamma > 0 without `drive_b` is refused at
load (the per-axis drive is never a member));
`flow_link` (since 2026-09-22,
`flow-link-v1`, the model owner's decision of record 915 on the Flow
Weight Designer's design
[docs/designs/flow_weight/DESIGN.md](designs/flow_weight/DESIGN.md), the
physics-rule reviewer's ADMISSIBLE of record 902; true or false, false by
default, any other type refused: under it the arrival flow every reader
sums counts each arriving row of direction D with the flow label f_D, the
integer vector nearest |p_D| D / S_1 (the label per Euclidean Link of the
line, S_1 = |a| + |b| + |c|; per component sign(D_i) x (2 |p_D| |D_i| +
S_1) // (2 S_1), one Euclidean division per component at load,
`nature_beam.flow_label`, the one product tested by division before it is
formed), in place of the unit label u_D nearest |p_D| D / |D| (the label
per Node); |p_D| is Q for the photon (`Flight.flow_labels`) and a massive
family's `momentum_magnitude` (`FamilyFlight.flow_labels`, each family's
from its own labels); read by the flow's sums alone, the rows' push
(`nature_beam.CrowdMoments`, `optical_turn`) and a body's push through
the group moment of a free family's rays (`_family_plan`, `push_form`);
the age moment, the wall, the flight, the collision, the phase and the
momentum a click moves (a paid family's push, the label Q per unit, note
18) untouched; the push's shell mean then carries no L1 factor (the
fan's mean of S_1 / |D|, 1.4355 on series K's 290 directions) and the
push's constant of gravity is the clock's; the record carries `flow_link:
true` and the identity `flow-link-v1` under `hypotheses`; the first world
that declares it is `examples/events/flow_link/` (the ring of starts at
b = 6); without the key the flow labels ARE the labels and every world
reads as it did, byte for byte, `tests/test_flow_link.py` (a)); the amplitude law
(`amplitude-v1`, [BEAM_LAW note 37](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation); the record form is the law since stage (vii)
step 4, the one click, MIGRATION (vii-4), and the world key `amplitude`
of stages (i) to (vii-3) is deleted, a world that declares it refused
naming MIGRATION): every lamp births records (under the detector law, since
BUILD.md section 26, the lamp is refused and an emitter body of a massive
kind births them, its excited record clicking at its own rung); every row of a record
carries a `record`, a `branch`, a `multiplicity` and its birth phase `u`
(a row of no record carries none: a declared row, a free family's rows);
the merge is the normal form that cancels antiphase rows of one record
(`NatureBeamStore.merge` with the circle's N; what it removed on the
ledger's `cancelled` lines); the apparatus's layer reads every record's
offers; the identity `amplitude-v1` is under `hypotheses` when the world
declares a lamp (`NatureBeamWorld.recorded`); a lamp is refused with N
below 4 (a record's circle holds the quarter turn of a reflection); a
world without a lamp reads as it did before the law, byte for byte
(`tests/test_amplitude_click.py` (d): the gate set's lamp-free worlds at
their caps against their pinned digests); the massive rows (since
2026-09-21, `massive-rows-v1`, [BEAM_LAW section 2](BEAM_LAW.md#2-the-record-of-a-ray-and-the-world-file);
the model owner's yes, record 332; the design
docs/designs/massive_rows/DESIGN.md): the world key `massive_rows` (true
or false, false by default; `age_bound` declared with it), the family key
`massive` under it (a paid family with a phase circle and no
`phase_per_link`) and the lamp key `momentum_magnitude` (p, an integer
from 1, required on the lamp of a massive family and refused elsewhere);
every family gets at load, beside `Flight`, its tables over the world's
directions (`nature_beam.FamilyFlight`, `NatureBeamTables.family_flights`):
the flight triple (the rate, the wall, the start) read by `walk_step` in
place of Flight's pair, the labels `momentum_labels` multiplies, the
turn's numerator per direction and axis over one denominator read by
`by_drive_rows` on the row's `acc_turn` at every Link crossed, and the
completion's pair (f_F, q_F); a family without the flag carries Flight's
numbers, u_D, (`phase_per_link`, 1) and (1, 0) by value, a massive family
p_D, (2 abs(p_D)_1, 2 E'_D, E'_D), (abs(p_{D,a}) N, h) and (0, M); at an
end (a `measure` click, a face, the border) f_F x the units, the content
and the labels go where they went and (1 - f_F) x them wait in the
record's offer (`amplitude.Offer.waiting_*`) under the books' `absorbed`
line, and at the record's completion (`nature_beam.gather_records`, after
step 4 and after the merge) every chosen end takes q_F into the measured
event's `held` at the chosen Node, one unit into its `clicks` and q_F x
the label-table entry of the chosen row's direction into its momentum (a
chosen face or the border: the face's `clicks`, `content` and `momentum`,
no body formed), the chosen row read by the ladder's rungs over the
waiting units per direction at the Node (`amplitude.node_choice`, the
same rungs that chose the Node within the cell), and the rest of the
record's waiting goes to the `cancelled` lines; a row of no record has no
completion and is placed at its arrival; the `gather` line's `content`
and `momentum` are f_F x what the chosen rows brought plus q_F and the
one label, the `click` line as today; a massive birth whose turn is not 1
is refused naming the lamp; the inverse interval is refused with the key;
`run.json` carries `massive_rows` as declared, the identity under
`hypotheses` when it is true and per family `massive` and
`momentum_magnitude` only then; without the key every world reads as it
did, byte for byte (`tests/test_massive_rows.py`); the clock stamp (2026-09-22,
the moving detector, docs/designs/moving_detector/DESIGN.md section 7): the
world key `clock_stamp` (true or false, false by default), under which every
line a measured event writes carries `clock`, its own count of
self-creations (the readings table below); `run.json` carries the key only
when true; no hypothesis, no rule, no verb, and without the key every
record is byte identical (`tests/test_moving_detector.py`); `doppler` (the reading's
weight at the relative speed of 2026-09-20, `doppler-v1`, deleted on
2026-09-21 with the crossing rule,
[BEAM_LAW note 48](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation):
a moving reader's Doppler is the count of the rows it crosses; a world
that declares the key is refused as an unknown key, MIGRATION); the keys of the hand (since 2026-09-20, `hand-v1`,
[BEAM_LAW note 39](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation):
`hand`, -1 or +1, on a family (every row born of it carries it), on a
lamp (a circularly polarised lamp of a family without a hand; a chiral
family's lamp may repeat the family's value only), on a transit row (a
row of a family without one) and on a table entry (the parity filter:
the entry's rule applies to arrivals of that hand only, the rest passed
as outside a window; refused on `pass`), a third entry per branch of a
lamp's `branches` (the hand the label means; a family carries its hand as
the row's column or as a label bit's meaning, never both) and `axis` on
a measured event (one of the six headings as a vector, the axial record
the right-hand rule reads at the birth of every product of its
`become`: a product of hand h leaves only on the event's directions with
sign(A . u_d) = h, a left-handed product against the axis; an empty set
refused at load); absent everywhere, no row carries a hand and every
world reads as it did, byte for byte); the binding that costs content, `binding-v1`
(since 2026-09-20, [BEAM_LAW note 40](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)),
has no key: the record carries its identity under `hypotheses` when a
measured event holds a paid family other than its own at load (`held`) or
took one during the run and gave it (the fact of the run,
`NatureBeamSimulation.binding` and `hypotheses`), the content a body carries
and gives at its contact; without such a body every world reads as it did,
byte for byte; `directions` (the declared primitive vectors beyond
the six headings, each with components in -P .. P, P = `direction_bound`,
64 by default, at most 4096 entries; the table D is the two rest vectors,
the six headings in Port order and these, in that order); `families`
(`name`, `quantum` (required; 0 a free family, 1 or more a paid one: the
kind is derived, never declared), `charge` (a free family: the charge per
unit of content, an integer or `[n, d]`, since 2026-09-20; a paid family,
since the same day (D-1, [BEAM_LAW note 36](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)
(ii)): the whole charge per unit of amount, an integer, read on the
charge line of the books only, the push untouched: the charge of a
measured event is rho times its content for a free family and the
declared whole charge times the amount for a paid family),
`columns` (since 2026-09-20, [BEAM_LAW note 31](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation):
an object of column name to `{"value": n or [n, d], "sign": 1 or -1}`,
the further columns of the one coupling; `gravity` built in with the
value [1, 1] and the sign minus, `charge` built in with the sign plus
and the family key `charge` as its value; one sign per name across the
world; [0, 1] where a family names no value; 0 on a paid family; at most
8 columns in all; the record carries `columns-v1` when a column beyond
`charge` is declared), `lifetime` (since 2026-09-20, an integer L from 1,
one scalar; absent, forever: a row of the family whose age reaches L at
the end of its walk clicks on the border `lifetime`, booked as a face
books an escape; refused beyond `age_bound`; the record carries
`columns-v1` when a lifetime is declared),
`phase` true by default, `phase_per_link` 0 .. N - 1, or (the amplitude law)
a pair `[n, d]`, the phase per interval of age (the design's frequency,
the owner's unification (1): a row of the family turns `by_clock(age, n,
d)` at every walk that advances its age, carried through a re-emission,
so that two paths of one record read their difference in intervals at the
click (the row's own floor per segment from its age 0 at its birth or
re-emission, sum_j floor(A_j n / d) over a path's segments, the design's
one floor at the click when d = 1 and within one step per segment
otherwise; the default stays the integer 0, not the lamp's own turn: a
family that turns in transit declares it); the integer form turns per
Link crossed as it did, and on the
flight rule the two are not the same number: a heading crosses 32 Links
in 55 intervals; refused on a family without a phase
circle; the record carries the key as declared)); `measured`
(`position`, `family`, `amount`, `phase`, `momentum`, `fixed`, `span`
(three odd integers from 1, `[1, 1, 1]` by default: a body on the set of
Nodes centred on `position`, one record on all of them),
`phase_by_momentum` (true: the body turns its phase by its momentum label
at every Link it steps, over the world's `action`; false by default),
`held` (since 2026-09-20, an object of family name to content, an integer
from 1 each: the content the event holds of families other than its own;
its content the sum, its charge in every column the rational sum over
what it holds, every free family held released at the world's rate
beside its own), `become` (since 2026-09-20, the transformation's clock
trigger, [BEAM_LAW note 36](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)
(iii): `{"at": a, "into": family, "products": [[family, amount, content per
unit], ...], "crowd": c}`, fired at the self-creation whose clock reaches
`at` (the age against the key, first at `at`, then at every multiple of
it) while the count the clock read is below `crowd` (optional, an integer
from 0; absent, no gate): the event becomes an event of `into`, the
products, paid from what it holds of its own family, are born as a
re-release is with the recoil over all of them, and the key is consumed),
`directions` (the
directions it releases and re-emits on, by vector or by index into D; the
six headings by default), `table` family name to `read` | `measure` |
`rerelease` | `pass` | `become` or to `{"rule": ..., "phase_window": s, "phase_width":
w, "reads": component}` (`phase_width` since 2026-09-20, [BEAM_LAW note 36](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)
(i): the width of the window in steps, 1 through N, N / 2 by default, the
w consecutive steps centred on s by the one floor `nature_beam.window_admits`)
with `reads` one of `scalar`, `outside`, `here`, `vector`,
`tensor`, `age` (the age moment; the entry's clock then counts it in place
of the presence), and on a `become` entry (the click trigger of the
transformation, since 2026-09-20, [BEAM_LAW note 36](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation) (iii)) its `into` and `products`: the
arrival clicked as `measure` clicks it and the same transformation fired,
its products born at the reader's next self-creation, the entry consumed;
the table generated from the keys by `world.default_table` (a
free family read, a paid one measured, no window) and the world declaring
only the entries that differ, `rule` optional in the object form, an entry
equal to the default accepted and changing nothing; since 2026-09-20
(issue #363, [BEAM_LAW note 34](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation))
the entry's `phase_window` may be an object `{"reads": "<family>",
"offset": s}` in place of the number: the centre of the window is then the
phase of the coherent pointer (`nature_beam.coherent_pointer`, the first
moment over the circle, its nearest step `pointer_phases`) of the named
family's rows present at the set in the interval, every row at the set but
the reader's own number, rest and moving alike, as the presence counts
them (`nature_beam.setting_steps`, read once per named family from the
rows after the walk and the collision, before any table acts), plus the
offset in phase steps (0 by default), the width the entry's `phase_width`,
N / 2 by default;
with no such row at the set, or a zero pointer, the entry passes with a
`pass` record naming `window` None and `reads`; every `click` of such an
entry carries the `window` used (`MeasuredDefinition.window_reads`,
`Measured.window_reads`: per family the (family, offset) read, None for a
number or none); since 2026-09-20 a `rerelease` entry
may declare the split (`world.Split`, the owner's unification (2): the
split is `rerelease` with a vector of integer weights and the
multiplicity, one rule): `weights`, one integer from 0 per declared
direction of the measured event (at least one positive), `turns`, one
phase step per direction (0 by default), and `inputs`, arrival directions
that select the row of weights and turns (`weights` and `turns` then
lists of one row per input: a beam splitter transmits and reflects by the
side a row comes from), a row arriving on a direction the `inputs` do not
name refusing the run naming the Node; an arriving row (w, m, p) is
re-emitted as the rows (w a_i, m x A, p + t_i) on the directions, A = sum
a_i^2, every weight 1 where none is declared (the equal split; a row of
no record apportioned as it was), the multiplicity bounded before it
is formed and refused naming the Node (the load-time ceiling multiplies
the declared `weights`, `rotate` and `gate` factors alone and no longer
a plain `rerelease`'s, since a path's count of re-emissions is not known
at load: a bound moved from load to run, so a world may run before the
split's own check refuses it; two guards, then: the static path ceiling
at load, an acyclic count of the splits, rotations and gates on a path,
and the run-time bound at the split, a cycle among re-emitters, two
openings feeding each other, caught by the run-time bound alone and
outside the register's ceiling); refused on a rule
other than `rerelease` and on a free family's entry; a split is not a
click: a `rerelease` entry takes every arriving row of its
family on its own, with no pointer gate and no window, the amount gate
alone, whose default 1 admits every row (the decision of 2026-09-20 on
the design's 2.1 and 3.1); the units it absorbs stay live in the layer
until it re-creates them, and a `rerelease` entry on a `sum` set ends
them there with an offer, the re-creation a new record when the record
chose that set; a row of a record taken home is re-created with its
columns and its multiplicity kept, apportioned whole as a row of no
record is, no split at the home); `lamp` `{rate: [n, d], wheel: [r, W],
directions, phase_window, phase_width}` on a measured event of a paid
family, its window a number, its `wheel` the birth wheel's rate (required
since 2026-09-21, [BEAM_LAW note 46](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation):
u = ordinal x r mod W the record's coordinate on the ladder, [1, N] the
count of births mod N); also `turns`, a phase step
per direction the born row carries beyond the clock's phase; a
self-creation with a release births as many records as the rate says
units per direction (`by_clock(age, n, d)`, the crowd form's count, as
many as the lamp can pay whole; stage (vii); until then the rate [1, 1]
alone), each one row of amount 1 per direction with the multiplicity the
directions' count, the record's identity the lamp's number x 2^32 + the
birth's ordinal at the lamp, `nature_beam.record_identity`, the birth
phase u the lamp's count of births less one, mod N (the record's own
field on its rows, the column `birth`, uniform over births whatever the
lamp's turn; a rebirth's u the re-emitter's own count; the K finding of
2026-09-20, stage (vii) step 2), the born rows' phase u plus the
direction's turn; and `branches`, the joint labels
of the birth with their integer weights (`[[label, weight], ...]`, the
labels distinct and below 2^arms, the bit k of a label its value on arm
k; [[0, 1]] by default) and `arms`, the count of directions that are
separate quanta (1 by default, dividing the directions, which the arms
share in order): per direction one row per label of amount the label's
weight, the multiplicity the paths per arm times the norm (the sum of
the squared weights), the row's `branch` its arm x 2^32 + its label; a
lamp that cannot pay every label's weight on every direction refuses the
birth naming the lamp); a table entry's `turn`
(0 by default, 0 .. N - 1, refused on `pass`): the
phase step on the label-1 column of the rotation a `sum` set reads at
its window's setting s, `U_s = [[C'[s], S'[s] v(t)], [-S'[s], C'[s]
v(t)]]` on the half-angle tables of 2N (the channels + and -; the design's
2.2 and 4.1), the setting declared or read from a reading (at N = 4096 the
tables of 2N do not exist and an even setting reads the 4096 table at
s / 2, an odd one refused); a `rerelease` entry's `rotate` `{setting,
bit, turn}`, the rotation of one label bit on the
GameBoard (the design's 2.2): every row of a record at the entry becomes two
rows on the bit cleared and set, the amounts w C'[s] and w S'[s] of the
half-angle tables, the multiplicity m x 65536, the phases as the matrix's
signs say (from a clear bit the set bit takes a half turn; from a set bit
both take the turn t), not a click; a `rerelease` entry's `gate` `{kind:
"cnot", hold, parties, control}` (the design's section
10): the rows of `parties` records of distinct lamps pending at the entry
(one per emitter, the earliest born; with `hold`, true by default, held
until rows of `parties` distinct emitters are pending, read from the
rows alone; without it the rows present) join into the record of the
control, the record whose rows arrive on the `control` direction (a
vector of the table, required for two parties or more, refused for one;
refused at the gate unless exactly one record arrives on it), the joint
labels the product of their label sets (the control's bits first, one
bit per arm) permuted by the CNOT from the control's bit 0 to the bit of
every other arm, every row replicated over the other records' labels
with its multiplicity times the copies (the units added booked on the
layer's live count; the `gate` line's `added`), the others' identities
aliased in the layer; a record that reaches a gate with units elsewhere
or with an offer already made is refused (the lazy relabelling of the
design is not built); a gate of one party relabels the rows present and
joins nothing; the `gate` and `rotate` record lines; the multiplicity a
row can reach through every re-emitter of the world (the splits' norms,
65536 per rotation, 2^parties per gate) is bounded at load by 2^62 - 1
(the register's ceiling: three label rotations on a path fit, Grover's
six do not); two paths of one record that the GameBoard's geometry
brings to one set with multiplicities whose ratio is not a square (an
aperture two Nodes wide under a fan with the direction along it: the
norm of the second opening between the siblings) are refused at load,
naming the rule, the multiplicities and the aperture's width (issue
#714; the loader walks the record's paths through the openings per arm,
a world with a gate left to the run's check at the offer); a
`phase_window` on a `rerelease` entry whose Node reads no
`sum` set is dead (a split takes no gate) and refused at
load; a free family's rows (no record) keep the apportioning and
gates of a row of no record at every entry;
`in_transit` (`position`, `family`, `number`,
`direction` (a vector of D, or a rest index 0 or 1), `amount`, `phase`,
optional `age`); `detectors` (`name`, `positions`, `threshold` 1 by
default, `reading` `wave` by default (since 2026-09-20) or `beam`, or
`sum`, the one pointer's reading at the record's scope
(rows of one record at one offer with multiplicities that differ by a
square factor add at the common denominator, the held pointers rescaled,
`amplitude.common_denominator`; a ratio that is not a square is refused
naming the record and the set, the integer form having no cross term
over its square root; stage (vii), the design's 2.5);
a detector's name may not use the layer's reserved prefix `measured:`
nor a face's or the border's name
(the owner's unification (4), `DetectorSet.scope`: `crowd` under `wave`,
the interval's arrivals of every number with the pointer gate and the
record per interval; `record` under `sum`, one record's rows over its
lifetime, no pointer gate, a window the rotation's setting and not a
gate, the record the square of the record's pointer per label added at
the record at its completion; interference is coherent within one Node
only: a set of several Nodes, a face included, offers one cell whose
weight is the sum over its Nodes of the per-Node squares, and the click
lands at the Node of the set that u's position within the cell selects by
the same rungs over the Nodes, `c_j = (2 W D_j + T) // (2 T)` with W the
cell's width, D_j the cumulative Node weight and T the cell's weight; the
decision of 2026-09-20 on the owner's point 5)). Refused, naming the key and the law: `"law": "events"` (pointing
to MIGRATION), `dynamics`, `max_active_owners`, `port_map`, `output`,
`capacity`, `groups`, `reference_phase`, `headings` on a lamp, `heading` on
a row, the earlier engines' keys (`contents`, `initial_shadows`,
`wait_per_quantum`, `schema_version`, `dense_field`), `phase_turn` as an
unknown key, a closed GameBoard, a non-primitive direction, a component beyond
P, a direction the world does not declare, a rest direction on a lamp or a
re-emitter, a repeated direction, a momentum label Q x content x amount
beyond 2^62 - 1 on a declared row or a lamp's release (content x amount
below 2^56), `phase_per_link` outside 0 .. N - 1 or on
a family without a phase circle, a content at or past K x N / 2 of a family
with a phase (2 x content x n at or past d x N at the rate [n, d]), a lamp
on a free family, `kind` on a family (pointing to
MIGRATION: the quantum decides the kind), a family without `quantum`, a
negative quantum, a fractional charge on a paid family (whole per unit of
amount, D-1), a lamp on a measured event of a charged paid family (its
releases would create charge from nothing), a `become` without `into` or
`products`, `into` naming an unknown family or the event's own, a product
naming an unknown family, a product's amount below 1, a free product's
content other than 0, a paid product's content below 1, a product's label
beyond the bound, `at` below 1 or absent on the clock trigger, `at` or
`crowd` on a table entry, `crowd` negative or not an integer, `into` or
`products` on an entry whose rule is not `become`, a `become` whose
products' content exceeds the event's `amount` or whose charges do not
balance, `become` on a family, and at run time an event that holds less
than its products need at the trigger ([the transformation](TEST_EXPECTATIONS.md#the-transformation)), `charge` on a measured event
(pointing to MIGRATION: the charge is the family's per unit of content), a
family `charge` with a denominator of 0 or a part that is not an integer, a
column named `gravity`, `charge` declared both as the key and under
`columns`, a column's `sign` other than 1 or -1, a column value with a
denominator of 0 or a part that is not an integer, a column object with
other keys, one name with two signs, a nonzero column value on a paid
family, more than 8 columns, a declared reader whose push over a column
from the largest release of a family could pass 2^62 - 1 (the parser's
static budget; [the columns](TEST_EXPECTATIONS.md#the-columns)), a
`lifetime` that is not an integer from 1 or is a list, a lifetime beyond
`age_bound`, a declared row in transit at or beyond its family's
lifetime, a detector named `lifetime`, `held` naming the event's own
family or an unknown one, a held content that is not an integer from 1,
`held` that is not an object ([the lifetime and the held content](TEST_EXPECTATIONS.md#the-lifetime-and-the-held-content)), a
detector named as a face detector is, two measured events at one
Node, an unknown table rule, N not
a power of two, a detector on a Node without a measured event, a Node in
two detectors, a `phase_window` outside 0 .. N - 1 or on `pass` or for a
family without a phase circle, a `phase_width` outside 1 .. N, on `pass`,
for a family without a phase circle or without a `phase_window` (on a
table entry and on a lamp alike; [the width of a window](TEST_EXPECTATIONS.md#the-width-of-a-window)),
a `phase_window` read from a reading that
names an unknown family, a family without a phase circle or the entry's
own family, whose `offset` is outside 0 .. N - 1, whose object has an
unknown key or lacks `reads`, or that is declared on a lamp
([a window read from a reading](TEST_EXPECTATIONS.md#a-window-read-from-a-reading)),
a table entry object with an unknown key (one
without `rule` takes the family's default rule), a `reads` outside the
reading's components, a detector `reading` outside `beam` and `wave`, a `suspension`
denominator of 0 ([expectations](TEST_EXPECTATIONS.md#the-world-file-of-the-beam-law)),
a `width` below 1 or not an integer ([the width of the push](TEST_EXPECTATIONS.md#the-width-of-the-push)),
an `age_bound` below 1 or absent on a GameBoard periodic on every axis, a
declared row's `age` beyond it, and at run time a row on the GameBoard whose
age passes it ([the age](TEST_EXPECTATIONS.md#the-age)), a `span` that is
not three odd integers from 1 or larger than its axis, a body whose Nodes
leave the GameBoard on an open axis, two measured events sharing a Node, a
detector naming a Node of a body that is not its `position`, an `action`
below 1 or not an integer, `phase_by_momentum` without `action`, on a
`fixed` measured event or on a family without a phase circle, and a
turning body whose `ticks x |p| x N` exceeds 2^62 - 1 for its declared
momentum ([a body on a set and the turn](TEST_EXPECTATIONS.md#a-body-on-a-set-and-the-turn-by-momentum)).
`event_universe.configuration_validation` reports a world of the law as
kind `beam`.

**The massive record kind** (`massive-record-v1`, 2026-09-23, the world
key `massive_record`, false by default, needing `detector_law: true`;
docs/designs/detector_law/MASSIVE_RECORD.md, the build's plan BUILD.md):
under it a family declares its `pair` `[num, den]` on the six-neighbour
term of the local detector law's rule (den > num a massive kind, its rest
frequency the gap cos omega_0 = num / den, no `phase_per_link` and no lamp
on it; every family without the key reads light's `[1, 1]`) and its
`faces` (the kind's own faces per axis, periodic by default, an open face a
zero face; light's faces the world's `boundary`); a measured event with
`side` is a BLOCK, the foreign object: its cells the cube of `side` at its
`position` (the lower corner), its `pair` at the cells (a well of the
massive kind's pair, or a gap on light's kind, the (M) wall), its
`coupling` `{"G": [n, d], "g": [n, d]}` (the dielectric of section 7, the
first difference both ways on the same Node, each rational folded into
the row's one division: the massive wall `3 den g_d`, light's `3 L` with L
the least common multiple of the blocks' `G_d`; `[0, 1]` each by default), its `seed` (its own record's
amplitude on its cells at interval 0, 2^20 by default, 0 silent; or, with
`margin` declared, a list of one integer per Node of the board in x-major
order, the bound mode's integer profile the generator writes into the file
at the world's amplitude, the record seeded so over the whole board at both
levels, a standing start on the mode, the load-time check against the margin
module's mode printed as GAMEBOARD; MASSIVE_RECORD.md section 11 item 7),
`cavity` (its own record held at 0 outside its
cells), `ramp` (the momentum reached from 0 over that many intervals, the
pushing agent's declaration), `start` (the interval its drive begins, 0 by
default, the ramp counted from it: the same agent's declaration), `margin` (`"pin"` or `"control"`, the margin
rule's kind of world) and `emits` (the light family its record sources,
one record per cycle of its clock, paid from its `held`); `probes` a list
of Nodes whose light amplitude the record writes per interval; SINCE BUILD.md section 26 item 15 the keys `wheel`, `own_grace`, `take`, `absorbing`, `residue_order` and `residue_seed` below are RETIRED and refused by name (the residue and the wheel are the law's, ALGEBRA.md 9.22 (4): u the clicking record's rule remainder at the birth cell and W = 3 den / gcd(num, 3 den) the record's own, carried on the birth line as `u` and `W`; the take is gone, 9.19 (3)), and this paragraph is their history; `wheel` (an integer from 1, under `detector_law`) the detector sets' rung W where no lamp declares a larger birth wheel (a world whose records a block emits); `amplitude_bound` (required on a world with a massive family) the amplitude A every row stays below, MUST 3's load bound at that A and the rows' run-time assertion (BUILD.md section 14); a face declared `"closed"` (under `detector_law`) a zero face for light without the take; an emitter block's or a lamp's `own_grace` (the intervals after its train during which a set bound to the emitter takes nothing of its own record, N_s, required on every emitter; a light lamp without it keeps two periods), an absorbing block's `take` [n, d] (its Ports' take pair, required on an absorbing block of a massive kind; light's kind takes with the law's [-15, 56]) and a detector set bound to a block (`"block": n` with its own `wheel`: a receiver whose Nodes are the block's current cells, or ONE declared free Node under `positions`; the click stamped with the block's count; a set on a body is `positions` with its own `wheel`); the order channel's two keys on a PAIR lamp (a lamp with `arms` above 1; DECLARATIONS.md section 2 item 8): `residue_order`, REQUIRED there with no default, "ordinal" (the counter form, u = (ordinal - 1) r mod W) or "seed" (u = order[(ordinal - 1) mod W], the order a Fisher-Yates permutation of the wheel's Z_W driven by the SplitMix64 mixing hash from `residue_seed`, `core.integer.keyed_permutation`, the stride r 1), and `residue_seed`, an integer in [0, 2^64) required under "seed" and refused under "ordinal", an input of kind 1 drawn once per world and written to no line; neither key admitted on a lamp without arms; the gather line's `u` and the `records` reading's `u` are HOST (the input of the diagnostic E_N), the reader of record reads `click`, `birth` and `chosen`; item 10 THE RULE (DECLARATIONS.md section 10 item 10, BUILD.md section 18; the model owner's records 1694 and 1711): every emitter's own Nodes take its record's remnant from the first interval after its train (no key, no load-time integer), in the record's kind's pair (the family key `take` [n, d] on a massive kind, required where a lamp of the kind exists; light's kind the law's [-15, 56]), booked onto no pointer and not into `absorbed`: the ledger's HOST row `taken_by_emitter` (the content of a record its emitter took wholly; `transit.taken_by_emitter` in the books), the gather line's `taken_by_emitter` and the records reading's `emitter_taking`; a detector-law world with a set and no lamp declares `wheel` (refused absent); THE RECEIVER BY NAME (DECLARATIONS.md section 13 item 7, BUILD.md section 21; Nature24's eight decisions of 2026-09-24 12:40Z through the Boss; `tests/test_receiver_by_name.py`): an emitting block's `receiver`, the name of a declared detector set, REQUIRED on every emitting block (refused absent, no default; refused on a block that emits nothing; refused naming no declared set, the names listed; the set may be the one bound to the block itself), makes that set's one cell the LADDER of every record the block emits (one cell whatever the set's Node count, its rung the set's own `wheel`, the record's u 0 choosing nothing): the faces and every other set are SINKS for it (their take into `absorbed`, the completion's measure, and onto the record's HOST `escaped`, never onto a pointer), the gather line is written at the receiver's first rung after the record's train (the law's sentence: at the first interval at which the record's cell is final, after the train and when the block is not sourcing it; `click` the rung's interval, `tick` the line's, equal to `click` unless the rung fell inside the train, then the birth plus the train), the content moves with the line to the receiver's body (0 for a block's record, born at content 0), and the record lives on with content 0 (field energy the sinks absorb, booked to the escaped row at its close) to close with NO second line, counted on the ledger's HOST row `closed_after_click` (`transit.closed_after_click` in the books; the records reading's `clicked` and `escaped`, the sinks' take in the pointer's unit; the gather line's `escaped`; all written on a world with a receiver alone); a record whose receiver crosses no rung within the ticks writes NO line and closes to the row of the take that ended it (`taken_by_emitter` where its own emitter took it, the escaped row where a face or a set did; 0 for a block's record) or stays open at the run's end; the emitter's own cells take on no pointer at every age (item 10 at T = 0 as merged; the hop's take of the block's own record booked nowhere), so a block naming the set at its own cells never clicks; a lamp's record (several cells) keeps the close and the cell by u; the five registered emitting worlds carry the key (sagnac_k3 and sagnac_rest: A at_b and B at_a; light_clock_60: A at_a; redshift_k3 and redshift_control: A light_detector); `mode_axis`
(`"x"`, `"y"` or `"z"`) the axis along which the record writes a `mode`
line per interval, the three sums of light's total field over the Nodes of
each residue class of that coordinate modulo 3 (the content of the mode
k = 2 pi / 3, the hop pump's signature of MASSIVE_RECORD.md section 7, a
GAMEBOARD reading; the reading tool forms abs(S_0 + w S_1 + w^2 S_2)^2 with
w the cube root of unity). The record
under the key: `massive_record`, per family `pair` and `faces`, and
`margin` (the margin rule's readings per block, MASSIVE_RECORD.md section
11 item 4: a load-time check made before the world runs by
`diagnostics/massive_record_margin`, the block's bound mode by a Lanczos
iteration on the world's own board, its extent in the medium and the
margin per axis, two extents for a `"pin"` world and one for a
`"control"`, a declaration below the margin refusing the run; a HOST
computation of the declaration, printed and recorded, never read by the
state; a cavity is skipped, and so is a folded axis, a periodic extent
below the block's side, a layer's or a chain's) in `run.json`; the books' `form` per family (the conserved form I of section
3, GAMEBOARD); in `events.jsonl` the block's `click` line per cycle of its
own record (`clock` its count), a `block` line per interval (its record's
sum across its cells, its corner, its count, its steps), a `probe` line
per interval and the emitted records' `birth` lines; in `state.json` the
`blocks` with the rows of each block's own record. Without the key every
record is byte for byte as it was (`tests/test_massive_record.py`).

**The record.** `run.json` carries `law` "beam-v1", the world's keys
(`boundary` as declared; `suspension` as `[n, d]`; `width`; `age_bound`; `directions`, the table
D beyond the rest vectors and the headings; per family its `quantum`,
`charge` (the pair `[n, d]`), `phase`, `phase_per_link` and `lifetime`
(None without one), no `kind`),
`numbers` (per measured event its `position`, `family`, `span`,
`phase_by_momentum` and, since 2026-09-20, `become`, the clock trigger as
declared, by names, or None; the measured events' states carry `span` too, as
`state.json` does), `action` (h, or None), `meeting` (the key as declared,
false by default), `optical` (`gamma` and `flight_coefficient` 1 + gamma, for every world
since 2026-09-22), `fast_steps` (since the crossing rule of 2026-09-21,
[BEAM_LAW note 48](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation):
the count of Links a body crossed in the interval right after another of
its Links, where the rule's one-per-crossing count is not proved; a
report, no refusal), `hypotheses` (`bohr-v1` when `action` is
declared, the identity of the turn by momentum beside the law;
`columns-v1` when a column beyond `charge` or a lifetime is declared,
the identity of the one mechanism of the columns and their range;
`weak-v1` when a measured event declares `become` or a table entry's rule
is `become`, the identity of the transformation; `meeting-v1` when
`meeting` is true, after it; `amplitude-v1` when a lamp is declared (a
recorded world); `massive-rows-v1` when the world declares
`massive_rows`, after it; `hand-v1` when a hand or an axis is declared anywhere;
`covariant-readings-v1` when the world declares `covariant_readings`
(2026-09-21, the model owner's record 270; the record then carries the
key's block `covariant_readings`: the pair `c2`, the `grain`, `books`, the
paid families off 3 h n = Q S d as `off_identity`, the most `comparisons`
one frame took and `waited`, the intervals each body owed to proper time),
`optical-v1` when the world declares `optical`, `drive-b-v1` when the world
declares `drive_b` (2026-09-22, the directional drive of a body; the record
then carries `drive_b: true`, under the key alone), `flow-link-v1` when
the world declares `flow_link` (2026-09-22, the flow label per Euclidean
Link; the record then carries `flow_link: true`, under the key alone),
last; `[]` without any; in a world with a hand every family carries
its `hand` and every number its `axis`, the heading's vector or None),
`columns` (the
world's, name and sign, in order: gravity, charge, the declared names)
and per family `columns` (name, value, sign, aligned with the world's),
the books per completed tick (`audit`, the `charge` line the
exact rational sum of the measured events' charges as a reduced pair: the
free families' rho x content held and, since 2026-09-20 (D-1), the paid
families' whole charge per unit of amount times the units each holds,
plus per paid family the charge of its rows in transit and of its units
escaped, a line conserved through a click, a home, an escape and a
transformation; and since 2026-09-20 the `turned` line per family and
in the momentum block) with
`conserved_at_every_completed_tick`, the measured events' final states
(`measured`: position, held per family, content, phase, charge (the pair
rho x content, reduced), `charges` (the charge in every column by name,
the exact rational sum over the families held, since 2026-09-20), momentum,
windows and, since 2026-09-20, `widths` (the width of each entry's window,
None where none is declared), `became` (the transformations fired, since
2026-09-20, the `family` then the one become), detector, age, owed, what waits to be created again (`home`,
`home_content`), `waited`, phase steps, steps, what each met per family by
rule, the clicks and the push taken, and `contacts`, the hand-overs it
took per family of the arriving body; no record of its own since
2026-09-19, the record being the detector set's), the detectors
(`detectors`: name, Nodes, threshold, `reading`, per family the amount
measured, the clicks summed over its Nodes, the set's one cumulative
`record` (the square under `wave`, the count under `beam`) and its
`phase` at the last click; then the face detectors, one per open face in Port order, with what
clicked there in transit, the `measured_content` of the measured events
that stepped off, the `record` and the `momentum` that left, the last
per family too since 2026-09-20; then, when a family declares a lifetime,
the border `lifetime`, `nodes` 0, with the same fields) and the `escaped`
per family (amount, content and, since 2026-09-20, the family's own
momentum: the faces and the border summed; until then the world's total
momentum was written into every family's line). `events.jsonl` holds one
record per event: `home`, `read`, `click`, `rerelease` (per number and
tick, with the amount, the phase, the push and the content; a `click` of
an entry whose window is read from a reading carries the `window` used),
`pass` (a row
below the threshold, with `threshold`, or outside the window, with
`window`, or paired under `beam`, with `cancelled` true; on an entry whose
window is read from a reading also `reads`, the family read, and `window`
None where no setting row was present), `step` (the
measured event's number, its Node before and after, its momentum and,
since 2026-09-20, its `phase` after the step: what the turn by momentum
turned it to, the phase it had otherwise), `contact` (since 2026-09-20:
the body's `number`, its `node` and the destination `to`, the `occupant`,
the body's `family`, the occupant's `rule` for it, the `axis` and the
signed `component` the occupant gained, since 2026-09-20 from the moment
the run holds a body with paid content (at load, or from the first give
on) `given`, the content the body gave to the flight at this hand-over
(`binding-v1`; 0 on a later hand-over), and the body's `momentum` after;
one per occupant that took a hand-over), `become` (since 2026-09-20, one
per transformation at its products' birth: the `tick`, `node` and
`measured`, the `trigger` "clock" or "click" and `triggered` the tick of
the trigger, `from` and `into` the families, `products` as [family,
amount, content, direction], `recoil` and `counted` the count the clock
read at the trigger), and per
interval per detector set and family a `record` line with the set's
`record` (under `wave` the square with the `pointer` (X, Y); under `beam`
the count), the set's `phase` and, for a set of one Node, its `node` and
`measured` (None for a set of several Nodes: the click says "here, in one
of these"); a `click` on a face detector names the face, `measured` None
for a row or the number of the measured event that stepped off. `state.json`, through
`snapshot_writer.write_snapshot`, carries `"law": "beam-v1"`, the
`boundary`, the measured events, the detectors and every Node with rows
(its rows: direction, age, phase, number, amount, content per family, and
nothing of the emitter but the number: the columns `charge` and `mass` of
the night of 2026-09-19 are gone since 2026-09-20, the factor of the
electric push being the family's charge per unit of content,
[BEAM_LAW section 2](BEAM_LAW.md#2-the-record-of-a-ray-and-the-world-file)
and note 28; a row of a record also its `record`, `branch`,
`multiplicity` and `u`, written on the rows of a record alone: a row of
no record carries none; in a world that declares `massive_rows`
also the row's `acc_turn`, the turn's remainder, written only then; in a world that
declares a hand or an axis (`hand-v1`) also the row's `hand`, written
only then, and the `click`, `pass`, `read`, `rerelease` and face lines
carry `hand`, the `become` line's products a fifth entry, the product's
hand, and the books' measured line per family `left` and `right`, the
units clicked of each hand). The birth phase u
is the record's own field beside the running phase (the K finding of
2026-09-20; stage (vii) step 2): every rule of the GameBoard that reads
a record row's phase reads the path phase, phase - u (the meeting's
register, the crowd's pointer of a `wave` set and its window, a window
read from a reading, the `beam` pairing, the phase a set returns, the
faces' and the border's pointers), a row of no record reading its phase
itself; the layer's offers read the running phase (a common rotation of
a record's rows, the rotation at a `sum` set's window acting on the
labels) and u enters at the click alone, the ladder. In a recorded world (a
lamp declared) the books gain the `cancelled` lines (per family the units the merge's
cancel removed on the transit line, the content carried on the content
line and their labels beside the `turned` line, and the world's total
under `momentum.cancelled`): initial + released = current + escaped +
absorbed + cancelled, the identity as it was where nothing cancels; the
units a split creates, sum (a_i - 1) w per row, enter `released` as every
re-creation does (the design's `split` line is not a line of the books).
In a world that declares `massive_rows` (`massive-rows-v1`) the transit
and content lines gain the sub-line `waiting` under `absorbed` and the
momentum lines the `waiting` line (per family under
`families[<name>].waiting` and the world's total under
`momentum.waiting`; `Ledger.waiting_amount`, `waiting_content`,
`waiting_momentum`): what the open records' rows brought where they
ended and was not placed at the arrival, (1 - f_F) x the units, the
content and the labels, kept in the records' offers; an arrival moves
them from `current` to `waiting` (f_F = 0) or to `measured` (f_F = 1), a
completion moves q_F from `waiting` to `measured` (or to `escaped` at a
face or the border) and the rest to `cancelled`, so that `absorbed` =
what the clicks placed + `waiting` on a world without a re-emitter, and
measured + transit + escaped + cancelled + remainder + waiting moves only
by the pushes, the turns and the escapes; absent (every f_F 1) the lines
are zero and not written.
In a recorded world the record gains the lines of the layer
(`events/amplitude.py`, the design's sections 3 and 5): `birth` (a lamp's
record: `record`, `u`, `labels`, `arms`, `units`, `multiplicity`, and
`clock` under the world key `clock_stamp`, the emitter's own count), the
`click`, `read` and `rerelease` lines carry the rows' `record`, `branch`,
`multiplicity`, `u`, `share` (the row's push on a body) and `age` where
the row is a record's (`rows` on a group
line, the rows of a record among the group's, absent where none is;
`window` and `turn` at a rotated `sum` set), `split` (per re-created row: `absorbed`, `born`,
`multiplicity`, `rebirth`, the entry's phase `u`), `cancel` (per record,
direction and content per unit: `amount`, `content`), the `record` line
of a `sum` set at a gather (`scope` `record`, `of` the record, `arm`,
`label`, `pointer`, the square `record`, `multiplicity`) and `gather`
(the world's row: `tick`, `arrived`, `family`, `record`, `u`, `born`,
`chosen` [set, arm, channel], `node` (the Node of every chosen end),
`windows` [set, setting, turn] of the rotated sets among the chosen,
`content` and `momentum` (what the chosen rows brought and gave at their
Nodes: the books' line of the click), `weight` and `total` as pairs in
the unit 2^58 (`unit`), `T`, `before`, `after`, `cells` with the rungs),
`gate` (`survivor`, `joined`, `present` per record, `labels`, `arms`,
`rows`) and `rotate` (`setting`, `bit`, `turn`, `rows`, `records` with
the units before and after); what follows a click at a chosen `sum`
re-emitter is one new record of all its re-created rows; `run.json`
gains `world` (the gathers), `open` (the records not gathered, with their
offers) and `layer` (the sets in order, the unit, the counts). A gather
is taken after step 4 (before the self-creations) and after the merge.
The layer's table holds a record until its completion and no longer: at
the gather the record leaves the table with its offers (its identity kept
for the lazy deletion of its rows, which resolve to nothing at their next
set; a gathered record reaching a gate is refused by name), and a
completion visits only the records whose live count reached 0, so the
host's work and memory per interval follow the open records, not every
record born.
`tools/amplitude_path.py` replays a run's register through the layer and
checks it against `world`. `tools/run_series.py` runs these worlds as any.

**The trimmed record** (2026-09-23, the host's default; no key of the
world, the record's verbosity being the host's and not the law's). In a
long run of a detector world the per-row `click` lines of the measured
events, one per clicked row (the lines the measure rule writes, about 355
bytes each), are nearly the whole of `events.jsonl` by count and by bytes
(a row 10 run of docs/designs/fail_rows at w = 9: 97 percent of the lines
and 98 percent of the 7.4 GB); the detector's reading of those rows is the
set's `record` line per interval and, in a recorded world, the `gather`
line per record, and the per-row lines are a GameBoard diagnostic. By the
model owner's word (2026-09-23, record 1296 of docs/LOG_2026-09-20.md: "if
we record the click, we do not need it for the experiment... only if you
need to keep the click, keep it") the runner leaves those lines out by
default and writes `omit_row_clicks` true into `run.json` on every such
record, so that a reader knows the record is trimmed; the option
`--keep-row-clicks` (`python -m event_universe` and `tools/run_series.py`,
which passes it to every child; `run_initialization(...,
keep_row_clicks=True)` and `execute_nature_beam_run(...,
keep_row_clicks=True)`; `NatureBeamSimulation(world, observer,
keep_row_clicks=True)` keeps its in-process observer whole) writes them
and no such field, the record as it was before the option, byte for byte.
Every other line (the face and border clicks, the `gather`, `record`,
`birth`, `split`, `cancel`, `read`, `pass`, `rerelease`, `step`,
`contact`, `home`, `become` and `energy` lines, the stamps) is written
either way, in order, and `state.json` and the books are the same. Every
registered digest is of the whole record: the digest tests, the register's
replayers and the gate replay keep the lines explicitly, so the three
digests per world of `gate_set.json` replay byte for byte under the
option (`tests/test_record_trim.py`, `tests/test_amplitude_click.py`);
a default record's `events_sha256` differs by the omitted lines alone. At
the start of a default run of a world whose rows can click (a detector
set, or a measured event with a `measure`, `read` or `pass` entry or a
window; the parser's default table makes every world with a measured
event one) the runner prints one line to stderr naming the world file,
`--keep-row-clicks` and the readers that need the lines, and runs on. A
reading tool that reads the per-row click lines
(`tools/click_readings/hubble.py`, `tools/click_readings/weak.py`,
`tools/moving_detector_readings.py` and the others that call
`event_universe.trimmed_record.refuse_trimmed_record`) stops on a trimmed
record with a plain sentence naming the option to re-run with instead of
reading zero; a record older than the field, written whole, is read as
before; the readers of the `gather` and `record` lines
(`tools/click_readings/covariant.py`, `tools/click_readings/quarks.py`)
read a trimmed record as any.

### The detector's readings by type

The model owner, 2026-09-21 (record 205): "after the detector, name the
vector to read": an experiment names, before its run, the quantity of the
record it will read and its type. This table lists every quantity the
record (`run.json`, `events.jsonl`, `state.json`) exposes, by type, with
the symbol of the notation rule (record 184: a scalar plain, a vector in
bold lowercase, a tensor in bold uppercase, a component plain with its
index), the line or field that carries it, its unit, and its kind under
[the two kinds of readings](EXPERIMENTS.md): a **detector** reading is the
record of a detector's set or of a measured event, the only kind reality
has; a **GameBoard** reading is the host's view of the deterministic
GameBoard. Every value is an integer or a reduced pair of integers; no
formula is applied on the way out. The coherent pointer (X, Y) is already
on the `record` line (a `wave` set's line under `pointer`, and the `sum`
set's line at a gather, per label); nothing further is exposed. The
things themselves, one row each in the three worlds, are in
[THREE_WORLDS.md](THREE_WORLDS.md).
A detector's reading is the record of an action of the law: the click ends
the record at the detector and changes the detector's own record, and only
that action measures; the host's readings of the board only read
(the model owner, 2026-09-23, record 1139; [POSTULATES.md](../POSTULATES.md) section 10).

| The reading | Type and symbol | Where the record carries it | Unit | Kind |
| --- | --- | --- | --- | --- |
| the clicks | scalar | `clicks` per family on a `detectors` entry of `run.json`, summed over the set's Nodes; the `click` lines of `events.jsonl` (`amount` per row group; on a face, the face's name as `detector`); `events` of a measured event's state. A face keeps two kinds of escape on two lines: a row's escape is a click booked on the face's `clicks`, `content` and `record`, while a measured event's escape by its step is booked on the face's `measured_content` and `momentum` and on the books' `measured.escaped`, never on `clicks` or `record`, and its `click` line writes `amount` = its content beside `measured` (its number) and `held` (issue #614; `tests/test_face_click_summary.py`). Under a lamp (a recorded world) a detector entry's `clicks` counts the units of every row that ended at the set, the offers, while the record's one click is the gather's `chosen` in the `world` list of `run.json` (one entry per record at its completion): the two differ (a lamp on an open face reads `clicks` 88 on `face:-x` and 81 on D against 32 and 49 gathers; `mz_345` reads D1 476 and D2 68 against the registered 63 and 1); the record's click is the `world` list's | units of amount | detector |
| the amount measured | scalar | `measured` per family on a `detectors` entry (the units taken by `measure`); `measured` in a measured event's state (per rule) | units of amount | detector |
| the record (the square) | scalar, the norm of the pointer | `record` per family on the set (`wave`: X^2 + Y^2 of the coherent pointer, accumulated; `beam`: the count clicked); `record` on the `record` line at each click; the same square on a face and the border `lifetime` | (32 x 256)^2 per unit of amount squared (X = sum 32 x amount x C[phase], C on the circle at the scale 256) | detector |
| the pointer (X, Y) | a vector of the phase plane (Z^2), not of the GameBoard | `pointer` on the `record` line of a one-Node `wave` set, and per label on the `sum` set's `record` line at a gather | 32 x 256 per unit of amount | detector |
| the phase | scalar on the circle Z_N | `phase` on the set at its last click; `phase` on a `click`, `record`, `home` or `rerelease` line; `phase` of a measured event's state | steps of the circle (N per turn) | detector |
| the wheel value u | scalar on the circle Z_N | `u` on a `birth` line ((births - 1) mod N at the lamp) and on the `click`, `read`, `rerelease` and `split` lines of a record's rows | steps of the circle | detector |
| the age of a row | scalar | `age` on the `click` line of a record's row; the age moment `reading` when the entry reads `age` (sum amount x age) | intervals (the moment: units x intervals) | detector (read whole only by a measured event) |
| the content | scalar M | `content` on a `click`, `read`, `home` or `rerelease` line (amount x content per unit); `content` and `held` of a measured event's state; `content` and `measured_content` on a face | units of content | detector |
| the clock of a measured event | scalars | `age` (its intervals), `phase_steps` (its turns), `owed` (the count owed in a crowd), `waited`, `steps` of its state | intervals, steps, units | detector |
| the clock stamp of a measured event (the world key `clock_stamp`, false by default; the moving detector, 2026-09-22, docs/designs/moving_detector/DESIGN.md section 7) | scalar | `clock` on every line the measured event writes (its `click`, `read`, `rerelease` and `become` lines, its face click and, the fifth line stamped, the `birth` line of its lamp, the emitter's own count at the birth, what the light clock's N(j) = clock(return) - clock(birth) of one ordinal subtracts): its own count of self-creations at that interval, the `age` of its state, not the row's `age` on the same line and not `clock_age`; a record field and no physics, entering neither the model identity nor the hypothesis list; without the key no line carries it and every record is byte identical | intervals of its own count | detector (the detector's own count, record 768) |
| the reading of the moments, order 0 | scalar | `reading` on a `click` or `read` line when the entry reads `scalar` (the presence), `outside` (the rows that arrived) or `here` (the rows that did not step) | units of amount | detector |
| the net flow **f** | vector, 3 components | `reading` on a `click` or `read` line when the entry reads `vector`: sum amount x **u**_d over the arrivals, on the unit vectors of the directions | Q = 64 per unit of amount along a heading | detector |
| the traceless second moment **T** | tensor, 3 x 3 symmetric of trace zero | `reading` on a `click` or `read` line when the entry reads `tensor`: 3 sum amount x **u**_d **u**_d^T less its trace on the diagonal | Q^2 per unit of amount | detector |
| the momentum **p** of a measured event | vector | `momentum` of its state (`measured` of `run.json` and `state.json`); `pushed` (the push taken, summed) and `drive` (the drive's count per axis) beside it | label units: Q = 64 per unit of amount along a heading | detector |
| the energy E' of a body (`covariant-readings-v1`, the world key `covariant_readings`; DERIVATIONS_BEAM 17.6) | scalars: E' / g the energy, E'_0 / g = (Q S / g) M the rest energy, W / g^2 = (E'_0 / g)^2 + d (**p** / g) . (**p** / g) its exact square, at the identity's grain g and the declared c^2 = [1, d] | the `energy` line of `events.jsonl` per body per interval (`energy`, `rest`, `square`, `creating`, `owed` the intervals the proper-time gate charged, `comparisons`); `energy` on the `step` line beside `drive`; the `covariant` block of a body's state (`energy`, `rest`, `square`, `waited` the intervals owed to proper time, `counted_sum`, `comparisons` the most in one frame) and `acc.tau` its proper-time accumulator; the run's `covariant_readings` block (the declaration, the paid families off 3 h n = Q S d, the comparisons, `waited` per body); written under the key alone, on bodies that are not `fixed` | E' in units of Q S per unit of content (E' = 3 E at c^2 = 1 / 3), at the grain g | GameBoard (a diagnostic: the host's view of the body's record; the detector's readings under the identity are the products' face clicks and the centre's pointer, series S) |
| the label **p** of a row | vector | `push` on a `click` or `read` line (the row group's label, what the reader took); `momentum` on a face `click`; `momentum` on a `gather` line (what the chosen rows gave); `recoil` on a `become` line; `momentum` per family on a face and the border | label units | detector |
| the share of a record's row | vector | `share` on the `click` line of a record's row: the row's push on matter, label x amount // m | label units | detector |
| the placed quantum of a completion | scalar M and a vector | `content` and `momentum` on a `gather` line: under `massive-rows-v1` the family's q_F (its `quantum`, M) and q_F x the label-table entry of the chosen row's direction, what the chosen set took at the completion (for every other family what the chosen rows brought, as before; the `click` line reports what arrived, `content` and `push`, for both); after it `held`, `events` and `momentum` of the measured event at the chosen Node, or a face's `content`, `clicks` and `momentum` | units of content; label units | detector |
| the waiting | scalars and a vector | the `waiting` sub-line under `absorbed` of the transit and content lines and the `waiting` line of the momentum block (`audit` of `run.json`), in a world that declares `massive_rows`: what the open records' rows brought where they ended and was not placed at the arrival ((1 - f_F) x the units, the content and the labels), resolved at the completion (q_F placed, the rest cancelled) | units, units of content, label units | GameBoard |
| the tick of a line | scalar | every line | intervals | GameBoard (the record's ordering; a duration or rate is read off a clock's clicks) |
| a Node as a position | vector of Links (x, y, z) | `node` on every line; `position` of a measured event's state; `to` on a `step` line | Links | GameBoard |
| the step of a measured event | scalars and a vector | `steps` and `axis_steps` of its state; the `step` line | Links | GameBoard |
| the level of a closure (`atom-level-v1`, the world key `atom_level`; docs/designs/atom_levels/LEVELS.md section 2 (b)) | scalars | the `level` line of `events.jsonl` at a body's return: `action` (the action gained over the loop, the sum of the body's give rows), `count` (its self-creations since the last return), `level` (the whole part of `n_l x action / (2 h d_l x count)`), `last` (the level at the last release, null at the first return), `released` (the rise released), `content` and `momentum` after; the released rows' `turn` (their own phase rate, steps per interval) on their `state.json` rows | steps of h d_l / (N n_l); label units x Links; intervals | GameBoard (the host's view of the body's store: the level a detector reads is the same arithmetic on two counts of the faces, LEVELS.md section 5 (d), R3) |
| the charge | a reduced pair (n, d) | `charge` of a measured event's state (rho x content, reduced) and `charges` per column by name; the `charge` line of the books | the family's charge per unit of content (a paid family: a whole charge per unit of amount) | detector (the state); GameBoard (the books) |
| the gather's weight and total | reduced pairs | `weight` and `total` on a `gather` line, `T` the norm, `cells` the rungs | the unit 2^58 (`unit`) | detector (the one click) |
| the click of a block's record at its named receiver (`detector-law-v1`, the block key `receiver`; DECLARATIONS.md section 13 item 7) | scalars | the `gather` line written at the receiver's first rung after the record's train: `click` the rung's interval, `tick` the line's (equal to `click`, or the birth plus the train where the rung fell inside the train), `click_at` "rung", `chosen` the receiver, `clock` the receiving block's count where the receiver is a set bound to a block (`clock_source`); `cells` the receiver alone (the sinks on no pointer), `T` the receiver's pointer with the sinks' take, `escaped` the sinks' take by the line (HOST, the pointer's unit); a record whose receiver crosses no rung writes no line | intervals; the unit 2^58 | detector (the one click; the interval from `birth` to `click` is the row's reading); `closed_after_click` of the books and `clicked` and `escaped` of the records reading are HOST |
| a non-absorbing read of a record's rows | a deferred offer, not an outcome | the `read` line of a record's rows that went on: the layer stores a residual selector keyed by the record's current label set (`amplitude.Layer.end`, the read branch) and the rows continue; a later rotation replaces that label set (`Layer.rotate`, `nature_beam.rotate_rows`) and the record's one click gathers at its far completion, so a read followed by a rotation and a second read is not a sequential measurement and is out of the register's contract (sequential-instrument use is unsupported under `amplitude-v1`; issue #584, 2026-09-21) | units of amount | detector (deferred to the gather) |
| the books | scalars and vectors, exact at every tick | `audit` of `run.json` per completed tick: per family the sums, the `momentum` block (`measured`, `transit`, `escaped`, `turned`), the `charge` line, `balanced` | units, label units, pairs | GameBoard |
| the `become` and `contact` lines of a measured event | scalars and vectors | the `become` line of `events.jsonl` (`triggered`, the tick its clock fired; `counted`, the count read at the trigger; `into`, `products` with their directions and hands, `recoil`); the `contact` line (the hand-over: `occupant`, the label handed) | intervals, units, label units | detector (the event's own record; the audit of record 567, F6, F8 and F14: never GameBoard) |
| a replay's or a store's reading | scalars and vectors | the world replayed through the API (`NatureBeamSimulation`) or `state.json` read Node by Node: the shell means and the ring means (`diagnostics/shell_readings.py`), the cube flux, a Node's presence or age moment (a clock's k from the store), a row's push, a body's steps and positions, the periods and separations built from them | as the quantity | GameBoard, a diagnostic: printed with its expectation, never pinned, never compared with nature, never the ground of a PASS/FAIL (the model owner, 2026-09-22, records 562 and 564; the audit of record 567); the detector reading behind it is named as not yet read |
| the flow and the counts at a Node, the shell means | scalars and vectors | `state.json` Node by Node (the rows' columns); `diagnostics/shell_readings.py` | units, label units | GameBoard |

## The law of events (`events-v1`)

Deleted on 2026-09-19 with the Beam Law (the model owner's rule, one
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
any physics.
