# The engine

The one engine of Universe24 is the engine of the law of events (`events-v1`;
[Highlights 5.4](HIGHLIGHTS.md#54-the-detector), "The law of events" and "The
principles of the law of events", the model owner's decisions of 2026-09-19:
"There is no shadow, no real. There are only events on the event board. There
are detectors by sensitivity. That is it. Everything must be generic in the
engine, without registers. There are no draws. There are only opening events
that spread by the physics of the engine."). This document is its contract as
implemented: the world file, the interval's steps, the suspension, the
measurements, the books, the record and the preflight. The engines before it,
the law of the shadow (`field-only-v1`, 2026-09-18 to 2026-09-19) and the law
of the bit, are in git ([migration](MIGRATION.md)); Highlights 5.4 records the
road to this law with a dated sentence on every earlier rule.

The code: `src/event_universe/events/` (`world.py` the world file and its
refusals, `transit.py` the arrays of one family's events in transit and the
walk, `mixing.py` the Node's computation of the sides, `engine.py` the
interval, the measured events and the books, `run.py` the artifacts of a run)
on `src/event_universe/core/` (`integer.py`, `lattice.py`, `phase.py`). The
tests: `tests/test_node_mixing.py`, `tests/test_event_transit.py`,
`tests/test_event_suspension.py`, `tests/test_event_clock.py`,
`tests/test_detector_sensitivity.py`, `tests/test_phase_window.py`,
`tests/test_periodic_axis.py`, `tests/test_phaseless_family.py`,
`tests/test_event_worlds.py`
([expectations](TEST_EXPECTATIONS.md)). The worlds:
[examples/events/](../examples/events/README.md).

## The law of events (`events-v1`)

**One thing.** An event, with a place (a Node), a time (an interval) and a
record: an amount (whole units), a phase (a step of the circle of N), a number
(the measured event whose continuation it is, the last emitter), a momentum
(three integers, given at birth: the family's `quantum` times the amount along
the release heading, and afterwards carried and apportioned), a heading, and
its counts (the suspension it carries; for a measured event its age, the
count of its self-creations). At every interval every event is created at its
next place from its record, and the next place is one of seven: the six
neighbours or here. An event in transit is created at a neighbour; a suspended
event is created here for its count; a measured event is created here without
end. Nothing is kept at a Node: no register, no remainder, no parked share, no
draw. The seven slots per Node and number, six lanes and here, are the whole
state.

**The board.** Open on every face by default (`boundary` `"open"`: the
edge is infinity, what leaves is booked as escaped with the momentum it
carried; a closed board is refused). The declared exception (the model owner,
2026-09-19), a run parameter of the world file, each experiment deciding what
to run: an axis may be declared periodic (`boundary` an object with any of
`x`, `y`, `z` set to `"open"` or `"periodic"`, the missing axes open, for
example `{"z": "periodic"}`). On a periodic axis the departures that would
leave the board through one face are created at the first Node of the
opposite face, the wrap (`Transit.walk`, a roll of the departures along that
axis: fixed local work per Node and Port, integers only), each in the slot of
its travel heading; nothing escapes on that axis and the momentum they carry
stays on the board, so `escaped` and the momentum escaped count only what
leaves through the open faces and the books balance with nothing lost on a
periodic axis. With an extent of 1 on a periodic axis the two departures on
that axis return to the same Node in the next interval as its arrivals
through those Ports (a unit leaving +z at the last Node arrives at the first
Node in the +z slot; with an extent of 1, at the same Node in the +z slot):
the Node behaves as a four-Port node with a one-interval stub, as a
two-dimensional transmission-line-matrix (TLM) node with a stub does. The
periodic axis is a rule of the walk (step 1); a measured event's step (step
6) off the board escapes with its content as before, on every face. Open
stays the default and the meaning of "the edge is infinity"; `"closed"` and
every other word are refused. Per family the
arrays of `Transit` with the axes (x, y, z, number, Port): the arrivals of the
interval (`arr_*`: amount, phase, momentum), the departures (`fly_*`), and per
Node and number the count the arrivals there carry (`suspended`). Per Node with
a measured event, the measured event (`Measured`: an amount per family, a
momentum, a phase, a number, a whole charge, a table, its age and its count;
what came home this interval, created again at its next self-creation). The
nearest phase step of a sum is computed exactly over a bounded window of
candidates (`transit.nearest_step`, `step_window`).

**The interval** (`EventSimulation.step`, in this order):

1. Every departure is created one Link on (`Transit.walk`), its record
   unchanged: an event in transit does not turn, a transfer is not a tick of
   its clock, so light's frequency is its emitter's clock stamped on the stream
   and constant in flight. The escapes through the open faces are booked; on
   a periodic axis the departures wrap. Arrivals into a slot that
   holds events waiting there are one amplitude per Port (the amounts added,
   the phase of the coherent sum, the momenta added).
2. At every Node the presence of each number is formed: the amount that
   arrived there this interval, over every family (the model owner,
   2026-09-19: the suspension reads presence, of everything, with one
   fractional width; no amplitude, no square root). This interval's
   presence is what a measured event reads at its self-creation (step 5)
   for the count it owes: the presence at its Node of every number but its
   own, times the world's `suspension` `[n, d]`, the whole part,
   `count = presence x n // d`. The events of a paid family that arrived
   this interval read the same presence at their Node, of every family and
   every number but their own, and carry the same count (`Transit.suspend`,
   written once on arrival; what joins a waiting slot waits with it, the
   larger count kept: the next event is delayed); a free family's events
   are not suspended, as before. The size of the coherent sum
   (`Transit.sizes`, in 32nds of one unit's amplitude) is still formed, a
   reading (the shell means) and the sum the phase window reads; it no
   longer feeds the suspension (until 2026-09-19 the transit read the free
   families' sizes and a measured event every family's sizes, whole units
   of amplitude; [migration](MIGRATION.md#the-field-of-matter-without-phase-the-suspension-as-presence-with-a-fractional-width-and-the-push-as-the-net-flow-on-2026-09-19)).
   The presence read is the Node's, formed from the arrivals per Port and
   the same for the six exits, and the wait is the seventh exit, here:
   after the count the Node computes the held arrivals again with what
   joined them. Nothing is read per exit Port: the free family's leaving
   shares are directed (four ninths back toward its source for a lone
   arrival), so a count read at an exit would slow an event by its heading,
   which no detector reads of a static field; the same count on every exit
   is the isotropic index a detector reads (Highlights 5.4, 2026-09-19, the
   rule proposed and withdrawn).
3. A measured event meets the events that arrive at its Node (`_meet`): its
   own number's are home, taken to be created again at its next self-creation,
   pushing nothing and not counted as content (the reading that keeps a
   content constant); another number's are met by its table, at a detector's
   Node only a bundle of one number at or above the detector's `threshold` in
   one interval: a smaller bundle passes whatever the table says (no push,
   the units mix on as at an empty Node), and the threshold gates every
   response, `read`, `measure` and `rerelease` alike, a receiver's and a
   re-emitter's; a release (step 5) reads no threshold. After the
   threshold, the window: where the table entry declares a `phase_window`
   s, the bundle's phase at the Node is read (the nearest step of the
   coherent sum of its arrivals over the six Ports, `Transit.phase_at`,
   the sum whose size `sizes` reports) and only a bundle whose phase falls
   in the half circle centred on s is met, d = (phase - s) mod N below
   N / 4 or from 3 N / 4 (exactly N / 2 steps; for N = 2 the one step
   d = 0; `engine.in_window`, integer arithmetic on N); a bundle outside it
   passes as a small one does, no push, the units mixing on, and a `pass`
   record is written. The rules: `read`
   (the default for a free family: the push taken and the units left to mix
   on as at an empty Node), `measure` (the default for a paid family, the
   click: the push taken and the amount joining the content, one click per
   unit), `rerelease` (the push taken, the amount taken to be created again
   like what came home, with the measured event's number and phase) or
   `pass` (no push, the units mix on). At a click the bundle's phase is the
   detector's reading and nothing else: it is compared with the window and
   written on the click record, and it does not enter the measured event,
   whose phase is its own clock (step 5) and takes nothing from what it
   measures, or its rates off the clock would depend on what fell on it;
   the amount joins and the momentum enters, and those two the board keeps.
   A click is the border between the board and the detector, one way: the
   run's record is the detector's measurement, not a history outside the
   model, and the board after a click does not tell the phase measured
   (Highlights 5.4, 2026-09-19, issue #338).
4. At every Node the arrivals of one number that are not suspended mix
   (`Transit.cycle`, node-mixing-v2, `mixing.mix_arrivals`): the events that
   arrived on each heading are one amplitude, sqrt(amount) in 32nds at their
   phase; the leaving amplitude of each heading is the coherent sum less three
   times the arrival that came in through its Port (point 24's third and
   minus, what six equal Ports and exact conservation allow); the total is
   shared by the squared leaving amplitudes in whole units, the floors and the
   units left to the largest remainders, the ties broken in Port order counted
   from the interval's tick so that no heading is favoured over time; a group
   with no whole for any side, fewer units than a side's whole share, goes
   whole to one side, the heading nearest the momentum it carries (on a tie
   the largest share, then the tick's order): a single unit leaves whole by
   its momentum. Each leaving share carries the phase of its leaving
   amplitude, and the momentum the group carries goes with the units placed,
   exact per axis (`apportion_carried`). A family that declares no phase
   circle (`"phase": false`; the model owner, 2026-09-19, the field of
   matter without phase) does not sum coherently: at every Node each Port's
   arrival scatters on its own (`mixing.scatter_arrivals`, chosen by
   `Transit.cycle` from the family's declaration) with the shares of a lone
   arrival, four ninths back out through the Port it came in by and one
   ninth to each of the other five sides, whole units by the largest
   remainder with the ties in the tick's Port order, per Port; a Port's
   arrival with no whole share for any side (one or two units) goes whole to
   the heading nearest its own momentum (on a tie the largest share, back,
   then the tick's order); its momentum is apportioned over its own six
   departures exactly per axis (`apportion_carried` per Port), and the six
   Ports' departures and momenta are added per heading. Two arrivals of 9
   through opposite Ports leave 5 and 5 along the axis (4 back and 1
   forward each) and 2 on each transverse side (1 + 1), never cancelling;
   every phase leaving is 0. Fixed local work, 64-bit integers. A suspended
   slot stays as arrivals, its count paid by one.
5. A measured event that owes a count pays it by one (`_release`): it is
   created here without a self-creation, no release and no turn, and `waited`
   counts the interval (age + waited is the intervals completed, for every
   measured event at every interval). One that owes nothing is created here
   again, the self-creation:
   its age advances by one, and off its clock (`by_clock`: what the whole part
   of age x rate gained by this self-creation, no remainder anywhere) it
   releases, per free family it holds, content x the world's `release` per
   Port; a lamp its declared rate on its headings, spending its content and
   taking the recoil (a lamp with a `phase_window` only at the
   self-creations whose clock phase, the phase before this self-creation's
   turn, the one its release is stamped with, falls in its window); and
   what came home or is re-released on the six headings
   in equal whole shares, the units below six going whole to the heading its
   clock points at (the age modulo six); every release stamped with its number
   and phase and carrying its momentum from birth. Its phase turns by its
   content over K off its clock (refused when a step would reach half the
   circle) at every self-creation, whether or not it released: a lamp whose
   phase leaves its window keeps turning and comes round to it again; a
   measured event of a family without a phase circle (`"phase": false`)
   never turns, its phase 0, and K does not apply to its content. After
   its self-creation it reads the presence at its Node of every number but
   its own, this interval's (step 2), and owes `presence x n // d`
   intervals at the world's `suspension` `[n, d]` (`_suspend`,
   `Measured.owed`, written once per self-creation, never accumulated),
   paid one per interval before its next self-creation. So a measured
   event in a steady presence whose count reads k is created again once
   every k + 1 intervals: its clock is slowed by 1 / (k + 1), the redshift
   (Highlights 5.4: "a measured event that reads a large size releases and
   turns slower"), and never stopped; with `suspension` 0 it is created
   again every interval. The read follows the self-creation and never
   precedes it: the first `events-v1` read before it, and in a steady size
   of one whole unit or more the count was owed again every time it was
   spent, so the clock stood still ([migration](MIGRATION.md#the-suspension-of-a-measured-event-read-after-its-self-creation-on-2026-09-19),
   2026-09-19).
6. A measured event steps by its momentum off its clock (`_move`) when it
   owes nothing: in the interval of its self-creation when that read no
   count, else in the interval the last unit of its count is paid (the
   self-creation is then the last one made), so a suspended event is
   created here for its count and each self-creation's step is read once.
   On an axis
   with momentum p and content M, one Link per (M + p) / p self-creations, at
   most one step per interval, x before y before z, the momentum untouched;
   a step onto a measured event merges the two into the resident (amounts,
   what came home, momentum and charge added, the resident's number, phase and
   table kept), a step off the board escapes with its content; `fixed` never
   steps.

**The push** (Highlights 5.4, the law of events, the third law corrected the
same day; the model owner, 2026-09-19, the push of a free family reads the
net flow): for the units of one number of a free family arriving at a
measured event's Node, c is their NET FLOW, the sum over the six Ports of
amount times travel heading (the arrival slot's heading, what `Transit.flow`
sums per Node), not the momentum labels they carry: they push the measured
event by -M c (the gravity reading, toward the emitter, the content M the
cross-section) and by (q_A / M_A) q c (the electric reading, the emitter's
whole charge over its declared content times the measured event's whole
charge, the whole part off the clock, D the least common multiple of the
charged events' declared amounts, the flow in place of the carried
momentum). The momentum from birth of a free family's events stays on their
record, apportioned with the units at every Node, and in the momentum book,
unread by the push (until 2026-09-19 the push read the carried momentum;
[migration](MIGRATION.md#the-field-of-matter-without-phase-the-suspension-as-presence-with-a-fractional-width-and-the-push-as-the-net-flow-on-2026-09-19)).
A free family's release costs nothing and takes no recoil, and the third
law is the symmetry of the two fields with what escapes. A group of a paid
family pushes by +c, its own carried momentum (light's pressure), and its
emitter took the recoil. The own number pushes nothing.

**The books** (`EventSimulation.books`, the runner's `audit` per tick), exact
at every interval: per family the measured line, initial + measured (the
clicks) = current + spent (the lamps) + escaped (measured events off the
board); the transit line, initial (the declared `in_transit`) + released (the
releases, the lamps, what came home or was re-released and left again) =
current (the arrivals and the departures) + escaped + absorbed (home, the
clicks, the re-releases; what came home is on the absorbed line until it
leaves again); the momentum reported on the measured events, in transit and
escaped, and the charge summed. The momentum book is a report, not a
balance: the measured line is the sum of the pushes taken (a free family's
by the flow, a paid family's by the carried momentum) and the recoils; the
transit line the momentum labels from birth, apportioned exactly with the
units at every Node, so a free family's labels in flight sum to what its
releases carried and what escaped carries them off; the two lines are not
each other's negatives. At the fixed point of a content at rest,
released - absorbed = escaped = the emission.

**The world** (`events/world.py`). `law` "events"; `model_id`; `shape`;
`boundary` "open" (the default) or an object with any of `x`, `y`, `z` set
to "open" or "periodic", the missing axes open; `ticks`; `K`; `N` (64 by
default, a power of two from 2
through 4096); `release` `[n, d]` per Port heading per self-creation per unit
of content of a free family; `suspension` `[n, d]`, the fractional width
of the suspension, a reader owing `presence x n // d` intervals (an integer
w is accepted as `[w, 1]`; `[1, 1]` by default; 0 or `[0, d]` for none,
recorded as `[0, 1]`); `families` (`name`, `kind` `free` or `paid`,
`charge` of a measured event of a free family, `quantum` the content of one
unit of a paid family, 1 by default and 1 for a free family, `phase` true
by default, false for a family without a phase circle: its events carry
phase 0 and never turn, its measured events never turn and K does not apply
to their content, no `phase_window` on its lamps or on a table entry for
it, no `phase` but 0 on its measured events and its events in transit, and
its arrivals scatter per Port instead of mixing); `measured` (`position`,
`family`, `amount` with 2 x amount < K x N for a family with a phase,
`phase`, `charge`, `momentum`, `fixed`,
`table` family name to `read` | `measure` | `rerelease` | `pass`, or to
`{"rule": ..., "phase_window": s}` with s a step of the circle from 0
through N - 1 on any rule but `pass`, with `read` the default for a free
family and `measure` for a paid one, `lamp`
`{rate: [n, d], headings, phase_window}` on a measured event of a paid
family); `in_transit`
(optional: `position`, `family`, `number`, `heading`, `amount`, `phase`);
`detectors` (optional: `name`, `positions` of measured events, each in at most
one detector, `threshold` 1 by default). Refused, naming the law: any key of
the earlier engines (`contents`, `initial_shadows`, `wait_per_quantum`, the
old engine's), `phase_turn` as any unknown key, a closed board or any
boundary but "open" and an axis object of "open" | "periodic", a lamp on a
free family, a charge or a quantum where the kind forbids it, two measured
events at one Node, a table naming an unknown family or rule, a content at or
past K x N / 2 of a family with a phase, N not a power of two, a repeated
lamp heading, a detector on a Node without a measured event, a Node in two
detectors, a `phase_window` not an integer from 0 through N - 1 on a table
entry or a lamp, a window on `pass`, a table entry object without `rule` or
with any other key, a family `phase` that is not true or false, a
`phase_window` on a lamp of a family without a phase circle or on a table
entry for one, a nonzero `phase` on a measured event or an event in transit
of such a family, a `suspension` denominator of 0.
`event_universe.configuration_validation` reports a world of the law as kind
`events`.

**The record.** `run.json` carries `law` "events-v1", the world's keys
(`boundary` as declared, the string or the object per axis, so that the
record says what the board was; `suspension` as `[n, d]`; per family its
`phase`),
`numbers` (the measured events' numbers, positions and families), the books
per completed tick (`audit`) with `conserved_at_every_completed_tick`, the
per-tick `measured_content`, `transit_content` and `momentum` lines, the
measured events' final states (`measured`: position, held per family, content,
phase, charge, momentum, its phase windows per family, its detector, age,
count and what waits to be created again, intervals suspended, phase steps,
steps, what each met per family by rule, the clicks, the push taken), the
detectors' measurements (`detectors`: name, Nodes, threshold, per family the
amount measured and the clicks) and the escapes; `events.jsonl` (the
detectors' measurement of the board, step 3) one record
per event (`home`, `read`, `click`, `rerelease`, `step`, `merged`,
`escaped`) with the tick, the Node, the measured event, its detector, the
family, the number, the amount and the push, the four measurements with the
`phase` read at the Node (`Transit.phase_at`), and a `pass` record for a
bundle outside a window (the tick, the Node, the measured event, its
detector, the family, the number, the amount, the `phase` read and the
`window`); `state.json`, through `snapshot_writer.write_snapshot`, the
`boundary` as declared, the measured events,
the detectors and every Node with events in transit (arrivals with their
count, departures, per number and heading, with phases and momenta).
`tools/run_series.py` runs these worlds as any. The readings the tests make
are the engine's (`shell_readings`: the shell mean of the count, the radial
flow and the size; `cube_flux`: Gauss's flux through a closed surface),
read-only.

**A detector's sensitivity** (Highlights 5.4, "a kind of detector
sensitivity"; "every detector must state what its sensitivity is"): a
detector is a named set of measured events with one table; its Nodes, its
threshold and its phase windows are its sensitivity. The threshold, the
smallest bundle of one
number the detector measures in one interval, gates every response of a
detector's Node, `read`, `measure` and `rerelease` alike, so that every kind
of external apparatus, a receiver or a re-emitter, works by its sensitivity:
a smaller bundle passes, no push taken and the units mixing on. It gates
responses only: a release, a lamp's or a free family's, and what a measured
event creates again after a re-release, read no threshold, and the own
number's arrivals are home and not a response
(`tests/test_detector_sensitivity.py`). One Node measures one quantum at one
place; a detector over a region measures many, and its statement, "an event
in this region", is read off the record (the run's measurements per detector
and per Node with their intervals, numbers, amounts, pushes and phases). What
reached no Node of it is unknowable.

The phase window is the second part of the sensitivity, with the threshold
(Highlights 5.4, the model owner, 2026-09-19: "Approve the phase window as a
declared width of a detector, and of the emitter too"): one generic key,
`phase_window`, a setting s on the circle of N steps and the half circle
centred on it. On a table entry (any rule but `pass`) the response is made,
after the threshold, only to a bundle whose phase at the Node (the nearest
step of the coherent sum of its arrivals, `Transit.phase_at`) falls in the
window, and a bundle outside it passes as one below the threshold does,
recorded as `pass` with the phase read and the setting; it is decided at the
Node from the arriving record and the local setting, no draw and no register.
Two Nodes whose settings differ by N / 2 divide the circle exactly between
them. On a lamp the same key makes an emitter of a declared phase: it
releases only at the self-creations whose clock phase falls in its window,
each release stamped with that phase, while a lamp without one cycles through
the circle with its clock; its clock advances and its phase turns at every
self-creation either way (`tests/test_phase_window.py`).

**What does not exist here**: no shadow and no real, no bit, no register, no
remainder, no parked share, no pool that counts as content, no return to the
source, no confirmation, no candidate, no turn in transit, no `phase_turn`, no
`wait_per_quantum`, no draw. Every rate is read off a clock the event carries,
and every tie is broken by the interval's tick or by the vectors. Whole units
without parked shares ripple more than the shadow engine's ninths did: the
pair's pushes agree within a few per cent, not one (the expectations say how
much).

## Preflight

`python -m event_universe.configuration_validation WORLD.json [--json]`
decodes a world file strictly (`json_documents`) and parses it with the
engine's own parser without running it; the report names the key at fault, or
summarizes the world (its model, law, shape, ticks, families, measured events
and detectors). A valid report certifies the configuration only, not a run or
any physics. The workspace ([WORKSPACE.md](WORKSPACE.md)) uses the same
preflight and runner.
