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
`tests/test_periodic_axis.py`, `tests/test_event_worlds.py`
([expectations](TEST_EXPECTATIONS.md)). The worlds:
[examples/events/](../examples/events/README.md).

## Opt-in physical detector candidate

The default contract below remains `events-v1`. The explicitly selected
`dynamics: "reversible-detector-v1"` extends the same engine with a restricted
reversible contact/transport path. Its authoritative schema, local operator,
inverse, state domain, clock reference, capacity, atomic refusal and physical
readout are in [the detector contract](DETECTOR_REQUIREMENTS.md#implementation-contract-reversible-detector-v1).
This assumed nondestructive transduction candidate does not call the default
absorption/mixing rules and does not establish a Heisenberg relation. It uses
ordinary measured and transit Events and no extra detector memory.

## Per-axis board topology (2026-09-19 implementation amendment)

The owner approved periodic axes as an experiment parameter in
[Highlights 5.4](HIGHLIGHTS.md#54-the-detector), published in
`c43c5789f761647229792590c368bbc9328ec214`. This amendment is the implementation
contract for both `events-v1` and `reversible-detector-v1`; its publication
precedes the behavior change. It changes the declared graph, not a local contact,
clock, suspension or mixing law. Earlier dated open-only results retain their
original configuration and source identity.

### Configuration and public interfaces

**Compatibility revision after main `ddb4470a4fe05ccc54b9d097b4c4bf9f51ed2550`
(PR #345).** That revision independently implemented the owner-approved periodic
transit and is now the canonical provider. Its actual API supersedes the stricter
all-axes draft published in `eacc96834819a10ad68c7cbbaeb0ceab0dff7eb3`.
Reuse it rather than replacing working transit or adding a second boundary schema.

`shape` remains exactly three integers from 1 through 4096. An omitted `boundary`
or the string `"open"` means three open axes. The additional form is an object
with any subset of `x`, `y`, `z`, each equal to `"open"` or `"periodic"`;
omitted axes are open. Thus `{}` and `{"z":"periodic"}` are supported. Unknown
axes, other modes and standalone `"closed"` or `"periodic"` are refused.
No axis, extent, physical family or apparatus name implies a topology.

Keep main's `EventWorld.boundary: str | dict[str, str]` as the declared record,
`periodic: tuple[bool, bool, bool]` as its x/y/z flags and `boundary_per_axis`
as the normalized dictionary property. These required fields stay in main's
constructor order; candidate-specific fields remain trailing defaults. Snapshot
and `run.json` retain `world.boundary`, including a declared partial object.
Preflight always reports `world.boundary_per_axis`, including all-open, as main
now does. The earlier proposed `Boundary3`, `OPEN_BOUNDARY`, `boundary_record()`
and omission of all-open preflight metadata are withdrawn. Preserve the original
initialization bytes and adapt any direct constructor consumers to this one API.

Main's `Transit` accepts `periodic: tuple[bool, bool, bool] = (False, False, False)`
after `clock`; retain that signature and its `numpy.roll` periodic transport.
The candidate's independent `exact_transport` option remains keyword-only.
`EventSimulation` passes `world.periodic` for both dynamics.

The missing scalar transport paths share one small provider in `core/lattice.py`:

```
adjacent_node(position: Address3, port: int, shape: Address3,
              periodic: tuple[bool, bool, bool] = (False, False, False))
    -> Address3 | None
```

This pure fixed-work function accepts exact three-tuples, exact integer extents
in 1..4096, an in-board integer address and a Port in 0..5 (integer booleans are
refused). Periodic flags are exactly three booleans. Invalid input raises
`ValueError`; coordinate arithmetic uses existing bounded integer operations.
It returns one neighboring address, or `None` only for a transfer through an
open outer face. It neither reads state nor advances time. Candidate proposals
and default measured movement use it. Verify its addresses against the native
bulk transport on seam, extent-one and extent-two cases; do not rewrite the
already correct bulk operation merely to call the scalar helper.

### One Link and one interval

For a Port, add its signed unit heading on its axis. An in-range target is the
ordinary neighbor. If that coordinate exits a periodic axis, choose zero after
the positive face or `extent - 1` after the negative face; other coordinates are
unchanged. The same record crosses once: family, owner, amount, phase, signed
Port and momentum survive transport unchanged. Never derive momentum from the
large wrapped coordinate difference. This is adjacency in the declared graph.

The existing interval order remains binding. A departure reaches its neighbor
only in the following transport interval, including when a periodic extent is
one and the target equals its origin. Positive and negative Ports remain distinct
channels when their destinations coincide at extent one or two. No same-step
relay, extra contact, repeated drain, copy or new signal is allowed. The initial
seeded arrivals may contact on tick 1 as before; they are not a prior wrap.

The default `Transit.walk` retains main's existing `numpy.roll` periodic branch
and open-axis bulk slices. The scalar neighbor helper supplies the same graph
semantics to material movement and the separate candidate proposal scheduler.
Open faces keep the existing escaped amount and momentum accounting. A periodic
face books no escape. Existing local reception/mixing remains separate from
transport, so phase preservation of the transfer alone does not assert unchanged
phase after a later default interaction.

Default measured movement uses the same neighbor provider. Existing timing,
self-creation/suspension order, open escape and collision/merge policy are kept.
A self-loop movement retains its one original Event and inventory, counts one
completed step and preserves momentum; it never merges the Event with itself,
deletes it, or doubles its content. A wrapped target occupied by a different
Event follows the existing merge law. This does not make that law reversible.

The candidate uses the same provider while building immutable local proposals.
A periodic transfer is admitted subject to its existing slot, integer and output
capacity constraints. An open exit still refuses the entire interval before
mutation. Wrapping itself is bijective on coordinate-plus-signed-Port channels;
it needs no history or hidden state. All three axes may be periodic. Finite
storage and local work remain fixed for the declared capacities. Repeated
encounters can exhaust a physical pointer: a return counts another crossing of
the same carrier, not a newly created quantum.

### Diagnostic scope and acceptance

`cube_flux` currently defines a clipped Euclidean cube and cannot silently omit
periodic seam Links. In this amendment it explicitly raises `ValueError` for a
world with any periodic axis or for `reversible-detector-v1` on any topology.
Only all-open default `events-v1` behavior remains unchanged. Its legacy
cached arrivals include seeded and suspended arrivals, and the candidate does not
populate those caches; changing seam coordinates alone would not measure executed
transfers. A future transfer audit must record actual directed Links and define
region membership R, with amount flux `sum(q * (in_R(source) - in_R(target)))`.
An open outside target has membership zero, and a self-loop contributes zero.
This is an amount diagnostic, not an energy law or physical detector result.
Other coordinate-based spatial summaries retain their declared coordinate
meaning and do not become shortest-periodic-distance observables.

A thin periodic Z board is a compact graph with return Links. It reduces the
number of allocated Nodes, but neither establishes measured wall-time speedup
nor substitutes for arbitrary unbounded 3D matter, a star or resolved microscopic
information. It changes boundary-dependent predictions and requires its own
experiment configuration.

Independent expectations, fixed before implementation:

| Isolated case | Expected result |
| --- | --- |
| Shape `(3,2,1)`, periodic X/Z, open Y; `(2,1,0)` on +X | `(0,1,0)` after one transport interval; inverse predecessor `(2,1,0)` |
| Same graph; `(0,1,0)` on -X | `(2,1,0)` after one interval |
| Same graph; +Z and -Z at `(1,1,0)` | Same Node next interval in distinct Ports 4 and 5; no immediate second contact |
| +Z carrier `q=2`, phase 16, momentum `(0,0,2)` through an extent-one periodic Z Link | Same payload and Port; escaped amount and momentum zero |
| +Y from `(1,1,0)` on the same mixed graph | Default transport books the existing escape; candidate refuses atomically |
| One candidate output, identity route, `N=8`, `K=1024`, content 1, initial displacement 0, `q=1`, capacity 2, periodic Z | Accepted ticks 1 and 2 read 1 and 2; tick 3 refuses with complete state and tick unchanged |
| Default movable material at an extent-one periodic axis, otherwise valid one-step state | One retained Event with unchanged inventory and momentum; one completed move |
| `cube_flux` on a periodic world or on any candidate world | `ValueError`, never an apparent zero from an unpopulated cache |
| All-open input omitted, string, or explicit/empty axis object | Same periodic flags; raw declared boundary retained in artifacts, normalized all-open dictionary in preflight |

The integration/schema owner reconciles main's `world.py` and preflight with the
candidate additions; main's boundary parser and serialization remain authoritative.
The engine owner adds only the scalar neighbor helper, missing candidate/material
paths and the unsupported-flux guard, preserving native bulk transit and metadata.
The schema owner supplies parser compatibility checks and data examples. Independent behavior tests belong to
`tests/test_event_boundaries.py`; architecture owns this contract and cross-links.
The 9-by-9-by-1 periodic example is a separate dated run, not an example-output
unit test. Physics review and affected regression evidence are required before
claiming implementation completion.

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
periodic axis was initially implemented only for the walk (step 1) in main
`ddb4470`. The [compatibility amendment](#per-axis-board-topology-2026-09-19-implementation-amendment)
extends the same declared graph to measured movement (step 6) and the opt-in
detector path; escape remains on open faces. Open
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
2. At every Node the size of the coherent sum of each number's arrivals is
   formed (`Transit.sizes`, in 32nds of one unit's amplitude): this interval's
   sizes, what a measured event reads at its self-creation (step 5) for the
   count it owes, `suspension` intervals per whole unit of the other numbers'
   sizes at its Node. The events of a paid family that arrived this interval
   read the free families' sizes at their Node and carry the same count
   (`Transit.suspend`, written once on arrival; what joins a waiting slot waits
   with it, the larger count kept: the next event is delayed). The size read is the
   Node's, formed from the arrivals per Port and the same for the six exits,
   and the wait is the seventh exit, here: after the count the Node computes
   the held arrivals again with what joined them. Nothing is read per exit
   Port: the free family's leaving shares are directed (four ninths back
   toward its source for a lone arrival), so a count read at an exit would
   slow an event by its heading, which no detector reads of a static field;
   the same count on every exit is the isotropic index a detector reads
   (Highlights 5.4, 2026-09-19, the rule proposed and withdrawn).
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
   exact per axis (`apportion_carried`). A suspended slot stays as arrivals,
   its count paid by one.
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
   phase leaves its window keeps turning and comes round to it again. After
   its self-creation it reads the sizes of the other numbers at its Node,
   this interval's (step 2), and owes `suspension` intervals per whole unit
   read (`_suspend`, `Measured.owed`, written once per self-creation, never
   accumulated), paid one per interval before its next self-creation. So a
   measured event in a steady size of k whole units is created again once
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
   table kept); under the topology amendment, a step through a periodic face
   wraps, a self-loop preserves its one Event, and an open exit escapes with
   its content; `fixed` never
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
`boundary` "open" (the default) or an object with any of `x`, `y`, `z` set
to "open" or "periodic", the missing axes open; `ticks`; `K`; `N` (64 by
default, a power of two from 2
through 4096); `release` `[n, d]` per Port heading per self-creation per unit
of content of a free family; `suspension` (an integer, 1 by default, 0 for
none); `families` (`name`, `kind` `free` or `paid`, `charge` of a measured
event of a free family, `quantum` the content of one unit of a paid family,
1 by default and 1 for a free family); `measured` (`position`, `family`,
`amount` with 2 x amount < K x N, `phase`, `charge`, `momentum`, `fixed`,
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
past K x N / 2, N not a power of two, a repeated lamp heading, a detector on a
Node without a measured event, a Node in two detectors, a `phase_window` not
an integer from 0 through N - 1 on a table entry or a lamp, a window on
`pass`, a table entry object without `rule` or with any other key.
`event_universe.configuration_validation` reports a world of the law as kind
`events`.

**The record.** `run.json` carries `law` "events-v1", the world's keys
(`boundary` as declared, the string or the object per axis, so that the
record says what the board was),
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
