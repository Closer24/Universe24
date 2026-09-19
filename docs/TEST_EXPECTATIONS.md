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

## Reversible detector candidate (2026-09-19, before implementation)

The [candidate contract](DETECTOR_REQUIREMENTS.md#invariants-examples-and-independent-checks)
fixes the numerical contact, clock, readout and finite-domain expectations before
implementation. `tests/test_reversible_detector.py` owns the generic operator and
3240-input inverse/injectivity check; `tests/test_physical_detector.py` owns local
transport, output causality, observer independence and atomic refusal;
`tests/test_reversible_detector_world.py` owns schema, generic grouping and
candidate/default compatibility. Example worlds are research configurations,
not tests with pinned experiment outputs. The standalone 9-by-9 HTML demonstration
needs its own dated source/configuration identity. None is a Heisenberg proof.

## Per-axis topology (2026-09-19, before implementation)

[The engine amendment](ENGINE.md#diagnostic-scope-and-acceptance) fixes the
independent seam, extent-one, distinct-Port, no-escape, capacity and material
self-movement expectations. `tests/test_event_boundaries.py` isolates those
rules and serialization; schema checks cover the strict per-axis form and old
all-open compatibility. A periodic example is a dated research run, not a pinned
example-output test. No closed-3D equivalence or timing speedup is inferred.
Since 2026-09-19 its wrapped-movement case onto a different resident expects
the refusal (both Events remain, the mover at (2, 1, 0) with momentum
(1, 0, 0) and one counted step) where it expected the merge (one Event of
content 2 at (0, 1, 0)); [the corrections](#the-border-and-the-clocks-count).


## Suite inventory of 2026-09-19: one engine

Decision of the model owner, 2026-09-19 ([Highlights 5.4](HIGHLIGHTS.md#54-the-detector)):
one engine, the engine of the law of events since the evening of that day
("Everything must be generic in the engine, without registers"; "only tests
that everything is as designed"). The suite keeps one module per generic rule
of the engine, on a minimal board, and the repository gates. The deleted
modules are named in the [migration notes](MIGRATION.md).

| Module | Rule isolated |
| --- | --- |
| `test_node_mixing.py` | The Node's computation of the sides on one Node of the engine's transit, one number: the 3B_h rule, the coherent sum, the largest remainder with the tick's ties, a group with no whole going by its momentum, the momentum carried, nothing kept ([below](#the-nodes-computation-of-the-sides)) |
| `test_node_mixing_numbers.py` | The coherent sum over the numbers: two numbers at one Node share one common sum and common weights, each placing its own units by them; a number with no whole by its own momentum at the common phase; a number alone as before ([below](#the-coherent-sum-over-the-numbers)) |
| `test_event_transit.py` | An event in transit: a single quantum whole by its momentum, no turn in transit, a part turned back apportioned again, a lone free unit straight from its release ([below](#an-event-in-transit)) |
| `test_periodic_axis.py` | A periodic axis as a declared run parameter of the world: the departures through one face created at the first Node of the opposite face, nothing escaping on that axis, the momentum kept on the board; with an extent of 1 the one-interval stub; the other faces open; the refusals and the record; a measured event's step wrapping too, escaping through an open face, and landing on its own Node with an extent of 1 ([below](#a-periodic-axis)) |
| `test_event_suspension.py` | The suspension the event carries: the count derived on arrival from the presence at the Node times `[n, d]`, the next event delayed, a measured event's clock slowed by the count it reads after its self-creation, never frozen; light on light; one presence read by a unit in transit and by a measured event ([below](#the-suspension)) |
| `test_phaseless_family.py` | A family without a phase circle: the sides weighed by the diagonal of the coherent sum, 32^2 x (the amount present + 3 x the amount through the side's own Port), a lone arrival four ninths back and one ninth each other way, two opposite arrivals never cancelling, the group's momentum apportioned over its departures; the identity of the weights; the push of a free family reads the net flow and not the labels ([below](#a-family-without-a-phase-circle)) |
| `test_event_clock.py` | The clock of a measured event: every rate off its age by whole division, the release, the phase, the lamp's recoil, the step ([below](#the-clock-of-a-measured-event)) |
| `test_release_costs_by_phase_rate.py` | A release costs the emitter by its phase rate: each unit `quantum` x s content and momentum at a turn of s, a click measuring it (E = h f); a free family costing nothing and pushing by the flow; a turn of 0 releasing nothing ([below](#a-release-costs-the-emitter-by-its-phase-rate)) |
| `test_event_worlds.py` | The worlds of the law of events on minimal boards: the books, the constant content, the flux, the shell means, the pair's pushes and the product law, the two-slit detector, the refusals and the runner ([below](#the-worlds-of-the-law-of-events)) |
| `test_detector_sensitivity.py` | A detector's sensitivity: its threshold gates every response of its Nodes, a receiver's and a re-emitter's alike, a smaller bundle passing; a release reads no threshold ([below](#a-detectors-sensitivity)) |
| `test_phase_window.py` | The phase window: a table entry's window gates the response after the threshold, a bundle outside it passing with a `pass` record; a window and its complement cover the circle exactly; a lamp's window selects its releases while its clock turns regardless; the refusals ([below](#the-phase-window)) |
| `test_integer_bounds_of_measured_and_emission.py` | The integer bounds of the measured line and of the emission: a measured event's momentum, push, content and what waits checked against 2^62 - 1 before assignment, refused naming the Node and the quantity; a free measured event's release per Port times 3 at most the mixing's cell bound 2^30 - 1, refused at parsing; the mixing's refusals naming the quantity ([below](#the-integer-bounds-of-the-measured-line-and-of-the-emission)) |
| `test_border_and_clock_corrections.py` | The three reversible corrections of 2026-09-19: a step onto a measured event refused (no merge, both remain, the step counted); an open face a detector (an escape a click on the face, the books' escaped lines the faces' sums, a periodic axis without faces); the clock's count read off the clock (`by_clock(age, k x n, d)`: a presence of 1 at [1, 4] slows the clock by 1 / 4, a presence of 8 owes 2 as before) ([below](#the-border-and-the-clocks-count)) |
| `test_configuration_validation.py` | The read-only preflight of a world file: the report, the refusals named by the parser, the command line |
| `test_json_documents.py` | The strict decoder shared by world files and the workspace's fragments |
| `test_integer_arithmetic.py` | The shared bounded integer primitives |
| `test_retention.py` | Generated-output ownership, lifetime and cleanup |
| `test_check_scope.py` | The affected-check's selection |
| `test_architecture.py`, `test_locality.py` | The dependency direction (`core` imports only `core`, the engine imports no host module, no physical module imports output or storage), the integer audit of `core/`, and LOCALITY-1 documented without an exception |
| `test_repository_language.py`, `test_repository_hygiene.py`, `test_repository_navigation.py` | The repository gates: English, one canonical copy, navigable links |

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
width): a reader derives its suspension from the presence at its Node, the
amount that arrived this interval over every family and every number but
its own, times the world's `suspension` `[n, d]`, the whole part
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
| (e) one presence, two readers | a measured event of light (content 1, number 2, measuring the free family and passing light) at x = 4; 16 units of the free family (number 1) and one unit of light of a third measured event (number 3) in transit there on +X; one interval at `suspension` [1, 4], then at [1, 16] | the unit reads every number but its own, 16, and carries 16 x 1 // 4 = 4 (3 after interval 1 pays one); the measured event, after its self-creation (age 1), reads every number but its own, 16 + 1 = 17, and owes 17 x 1 // 4 = 4: the same count; at [1, 16] the unit's count 1 (0 after the payment) and the measured event's 1 |

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
detector's threshold, the smallest bundle of one number it measures in one
interval, gates every response of its Nodes (`read`, `measure`,
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
is made, after the threshold, only to a bundle whose phase at the Node
(`Transit.phase_at`) falls in the window, a bundle outside it passing (no
push, the units mixing on, a `pass` record with the phase and the window);
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

`test_integer_arithmetic.py` covers decoded scalar/vector addition and
subtraction, ordered sums, dot/cross products and integer rounding. Independent
examples include (3,-4,2) dot (-1,7,-2) = -35, (2,-3,4) cross (-1,5,2) =
(-26,-8,7), and (3,4,0) squared norm = 25. Empty reductions, unequal component
counts, cross-product orientation/parallel vectors, signed limits and overflow
before cancellation are separate boundaries. Ceiling 15/7 is 3; signed division
-7/3 returns (-2,-1). Ceiling division rejects an overflowing adjusted numerator
even when the quotient would fit, preserving existing timing behavior.


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
  events and the detectors, `suspension` [1, 1], the family's `phase`
  false), `state.json` (the law,
  tick 4, the measured events, Nodes with events) and `events.jsonl`, keeps
  the input as read, and refuses a negative tick count and a used output
  directory.
