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
`tests/test_event_worlds.py` ([expectations](TEST_EXPECTATIONS.md)). The
worlds: [examples/events/](../examples/events/README.md).

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

**The board.** Open (a closed board is refused: the edge is infinity, what
leaves is booked as escaped with the momentum it carried). Per family the
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
   and constant in flight. The escapes are booked. Arrivals into a slot that
   holds events waiting there are one amplitude per Port (the amounts added,
   the phase of the coherent sum, the momenta added).
2. At every Node the size of the coherent sum of each number's arrivals is
   formed (`Transit.sizes`, in 32nds of one unit's amplitude). A measured event
   whose count is spent reads the sizes of the other numbers at its Node and
   is suspended for `suspension` intervals per whole unit read (`Measured.owed`,
   written when the count is spent, never accumulated; while it counts, its
   clock does not tick). The events of a paid family that arrived this interval
   read the free families' sizes at their Node and carry the same count
   (`Transit.suspend`, written once on arrival; what joins a waiting slot waits
   with it, the larger count kept: the next event is delayed).
3. A measured event meets the events that arrive at its Node (`_meet`): its
   own number's are home, taken to be created again at its next self-creation,
   pushing nothing and not counted as content (the reading that keeps a
   content constant); another number's are met by its table: `read` (the
   default for a free family: the push taken and the units left to mix on as
   at an empty Node), `measure` (the default for a paid family, the click: the
   push taken and the amount joining the content, one click per unit; a
   detector measures only a bundle of one number at or above its `threshold`
   in one interval, a smaller one passes), `rerelease` (the push taken, the
   amount taken to be created again like what came home, with the measured
   event's number and phase) or `pass` (no push, the units mix on).
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
   exact per axis (`apportion_carried`). A suspended slot stays as arrivals,
   its count paid by one.
5. A measured event whose count is spent is created here again (`_release`):
   its age advances by one, and off its clock (`by_clock`: what the whole part
   of age x rate gained by this self-creation, no remainder anywhere) it
   releases, per free family it holds, content x the world's `release` per
   Port; a lamp its declared rate on its headings, spending its content and
   taking the recoil; and what came home or is re-released on the six headings
   in equal whole shares, the units below six going whole to the heading its
   clock points at (the age modulo six); every release stamped with its number
   and phase and carrying its momentum from birth. Its phase turns by its
   content over K off its clock (refused when a step would reach half the
   circle). One whose count runs pays it by one and neither releases nor turns.
6. A measured event steps by its momentum off its clock (`_move`): on an axis
   with momentum p and content M, one Link per (M + p) / p self-creations, at
   most one step per interval, x before y before z, the momentum untouched;
   a step onto a measured event merges the two into the resident (amounts,
   what came home, momentum and charge added, the resident's number, phase and
   table kept), a step off the board escapes with its content; `fixed` never
   steps.

**The push** (Highlights 5.4, the law of events, the third law corrected the
same day): the momentum an arriving group of a free family carries, from birth
along its release heading, pushes a measured event by -M c (the gravity
reading, toward the emitter, the content M the cross-section) and by
(q_A / M_A) q c (the electric reading, the emitter's whole charge over its
declared content times the measured event's whole charge, the whole part off
the clock, D the least common multiple of the charged events' declared
amounts); a free family's release costs nothing and takes no recoil, and the
third law is the symmetry of the two fields with what escapes. A group of a
paid family pushes by +c, its own momentum, and its emitter took the recoil.
The own number pushes nothing.

**The books** (`EventSimulation.books`, the runner's `audit` per tick), exact
at every interval: per family the measured line, initial + measured (the
clicks) = current + spent (the lamps) + escaped (measured events off the
board); the transit line, initial (the declared `in_transit`) + released (the
releases, the lamps, what came home or was re-released and left again) =
current (the arrivals and the departures) + escaped + absorbed (home, the
clicks, the re-releases; what came home is on the absorbed line until it
leaves again); the momentum reported on the measured events, in transit and
escaped, and the charge summed. At the fixed point of a content at rest,
released - absorbed = escaped = the emission.

**The world** (`events/world.py`). `law` "events"; `model_id`; `shape`;
`boundary` "open"; `ticks`; `K`; `N` (64 by default, a power of two from 2
through 4096); `release` `[n, d]` per Port heading per self-creation per unit
of content of a free family; `suspension` (an integer, 1 by default, 0 for
none); `families` (`name`, `kind` `free` or `paid`, `charge` of a measured
event of a free family, `quantum` the content of one unit of a paid family,
1 by default and 1 for a free family); `measured` (`position`, `family`,
`amount` with 2 x amount < K x N, `phase`, `charge`, `momentum`, `fixed`,
`table` family name to `read` | `measure` | `rerelease` | `pass` with `read`
the default for a free family and `measure` for a paid one, `lamp`
`{rate: [n, d], headings}` on a measured event of a paid family); `in_transit`
(optional: `position`, `family`, `number`, `heading`, `amount`, `phase`);
`detectors` (optional: `name`, `positions` of measured events, each in at most
one detector, `threshold` 1 by default). Refused, naming the law: any key of
the earlier engines (`contents`, `initial_shadows`, `wait_per_quantum`, the
old engine's), `phase_turn` as any unknown key, a closed board, a lamp on a
free family, a charge or a quantum where the kind forbids it, two measured
events at one Node, a table naming an unknown family or rule, a content at or
past K x N / 2, N not a power of two, a repeated lamp heading, a detector on a
Node without a measured event, a Node in two detectors.
`event_universe.configuration_validation` reports a world of the law as kind
`events`.

**The record.** `run.json` carries `law` "events-v1", the world's keys,
`numbers` (the measured events' numbers, positions and families), the books
per completed tick (`audit`) with `conserved_at_every_completed_tick`, the
per-tick `measured_content`, `transit_content` and `momentum` lines, the
measured events' final states (`measured`: position, held per family, content,
phase, charge, momentum, its detector, age, count and what waits to be created
again, intervals suspended, phase steps, steps, what each met per family by
rule, the clicks, the push taken), the detectors' measurements (`detectors`:
name, Nodes, threshold, per family the amount measured and the clicks) and the
escapes; `events.jsonl` one record per event (`home`, `read`, `click`,
`rerelease`, `step`, `merged`, `escaped`) with the tick, the Node, the
measured event, its detector, the family, the number, the amount and the push;
`state.json`, through `snapshot_writer.write_snapshot`, the measured events,
the detectors and every Node with events in transit (arrivals with their
count, departures, per number and heading, with phases and momenta).
`tools/run_series.py` runs these worlds as any. The readings the tests make
are the engine's (`shell_readings`: the shell mean of the count, the radial
flow and the size; `cube_flux`: Gauss's flux through a closed surface),
read-only.

**A detector's sensitivity** (Highlights 5.4, "a kind of detector
sensitivity"): a detector is a named set of measured events with one table;
its Nodes and its threshold are its sensitivity. One Node measures one
quantum at one place; a detector over a region measures many, and its
statement, "an event in this region", is read off the record (the run's
measurements per detector and per Node with their intervals, numbers,
amounts, pushes and phases). What reached no Node of it is unknowable.

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
