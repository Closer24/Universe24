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

## Suite inventory of 2026-09-19: one engine

Decision of the model owner, 2026-09-19 ([Highlights 5.4](HIGHLIGHTS.md#54-the-detector)):
one engine, the engine of the law of events since the evening of that day
("Everything must be generic in the engine, without registers"; "only tests
that everything is as designed"). The suite keeps one module per generic rule
of the engine, on a minimal board, and the repository gates. The deleted
modules are named in the [migration notes](MIGRATION.md).

| Module | Rule isolated |
| --- | --- |
| `test_node_mixing.py` | The Node's computation of the sides on one Node of the engine's transit: the 3B_h rule, the coherent sum, the largest remainder with the tick's ties, a group with no whole going by its momentum, the momentum carried, nothing kept ([below](#the-nodes-computation-of-the-sides)) |
| `test_event_transit.py` | An event in transit: a single quantum whole by its momentum, no turn in transit, a part turned back apportioned again, a lone free unit straight from its release ([below](#an-event-in-transit)) |
| `test_event_suspension.py` | The suspension the event carries: the count derived on arrival, the next event delayed, a measured event's clock waiting ([below](#the-suspension)) |
| `test_event_clock.py` | The clock of a measured event: every rate off its age by whole division, the release, the phase, the lamp's recoil, the step ([below](#the-clock-of-a-measured-event)) |
| `test_event_worlds.py` | The worlds of the law of events on minimal boards: the books, the constant content, the flux, the shell means, the pair's pushes and the product law, the two-slit detector, the refusals and the runner ([below](#the-worlds-of-the-law-of-events)) |
| `test_configuration_validation.py` | The read-only preflight of a world file: the report, the refusals named by the parser, the command line |
| `test_json_documents.py` | The strict decoder shared by world files and the workspace's fragments |
| `test_integer_arithmetic.py` | The shared bounded integer primitives |
| `test_retention.py` | Generated-output ownership, lifetime and cleanup |
| `test_check_scope.py` | The affected-check's selection |
| `test_architecture.py`, `test_locality.py` | The dependency direction (`core` imports only `core`, the engine imports no host module, no physical module imports output or storage), the integer audit of `core/`, and LOCALITY-1 documented without an exception |
| `test_repository_language.py`, `test_repository_hygiene.py`, `test_repository_navigation.py` | The repository gates: English, one canonical copy, navigable links |

## The Node's computation of the sides

`tests/test_node_mixing.py` isolates node-mixing-v2 (Highlights 5.4, point 24
read under the law of events, the model owner, 2026-09-19) on one Node of the
engine's transit (`Transit` of shape (1, 1, 1), one number, N = 8) through the
kernels of `event_universe/events/mixing.py`: the events that arrived on each
heading are one amplitude, sqrt(amount) in 32nds at their phase; the leaving
amplitude of a heading is the coherent sum less three times the arrival that
came in through its Port; the total is shared by the squared leaving
amplitudes in whole units, the floors and the units left to the largest
remainders (ties in the tick's Port order); a group with no whole for any side
goes whole to the heading nearest the momentum it carries; nothing parks, the
Node keeps nothing. Written down before the first run:

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

## An event in transit

`tests/test_event_transit.py` isolates the motion of an event in transit
(Highlights 5.4, the law of events): a single quantum goes whole in one
direction, by its momentum, and does not turn. Written down first:

| Case | Input | Expected |
| --- | --- | --- |
| (a) a single quantum | a bar of 7 x 3 x 3, K 16, no release; one unit of a paid family with quantum 3 in transit at x = 1 on +X at phase 5 | at intervals 1 to 6 the only departure is at x = 1 to 6 on +X, amount 1, phase 5, momentum (3, 0, 0); at interval 7 it escapes with (3, 0, 0) |
| (b) a part turned back | 9 units at x = 3 on +X carrying (9, 0, 0) at quantum 3; then 2 units alone carrying (6, 0, 0) | interval 1: 4 back on -X with (12, 0, 0); interval 2 at x = 2: 2 back toward +X (one by the share, one by the largest remainder), 2 transverse, none on -X, nothing kept; the 2 units go whole to +X with (6, 0, 0) |
| (c) a lone free unit | a measured event of content 1 at the centre of 7^3 releasing at rate 1 per Port | interval 1: one unit on each of the six Ports; interval 3: the first six are at distance two, one each way, created outward, the books closed |

## The suspension

`tests/test_event_suspension.py` isolates the suspension (the model owner,
2026-09-19: "The event carries it; note that the next event is delayed"): an
exit derives its suspension from the sizes read at the Node, the event
carries the count and counts down on itself, what arrives behind it waits
with it, and a measured event whose count is spent reads again. K 2^20 so
that no phase moves. Written down first:

| Case | Input | Expected |
| --- | --- | --- |
| (a) an event in transit | a bar of 9 x 3 x 3, `suspension` 1; at x = 4 a unit of light and 16 units of a free family (the size 32 sqrt 16 = 128 in 32nds, 4 whole units) both in transit on +X; a second unit of light at x = 3 on +X | the light at x = 4 is held for intervals 1 to 4, its count after each interval 3, 2, 1, 0; the second unit arrives in interval 2 and waits with it; in interval 5 the two leave together on +X, amount 2, nothing left in the arrivals |
| (b) a measured event | a measured event of light (content 1, measuring the free family) at x = 4 where the 16 units arrive in interval 1 | its age after intervals 1 to 6: 0, 0, 0, 0, 1, 2; intervals waited 4, count spent, phase 0 |

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
| (c) a lamp | content 100 at rate [1, 3] on six headings, no release | 18 units after 9 intervals (at 3, 6 and 9), the content 82, the recoil zero over six headings |
| (d) the step | content 16 with momentum 16 on +x, 6 intervals; momentum 1, 16 then 17 intervals | three steps (one per two self-creations, 16 / 32); no step after 16, one after 17 (1 / 17); the momentum untouched |

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
check that it does what the law says and not as a result. One family `m`
(free, charge 0) whose measured event of 2^24 at rest releases 1/128 of its
content per Port per self-creation (q = 786 432 units per interval), N 64,
K 2^22 (four phase steps per self-creation), an open cube, the measured event
held in place (`fixed`).

- (a) one measured event (29^3, 300 intervals): at every tick the books
  close, the measured line reads current = initial = 2^24 with nothing
  measured, spent or escaped (what comes home is created again and never
  counts as content), the transit line reads released = current + escaped +
  absorbed with initial 0, and the measured events' momentum is zero. Gauss's
  flux through the cube of half-width 4 (`cube_flux`) is the emission within
  2 % over ticks 101 to 200 (0.995 measured) and over ticks 201 to 300
  through the cubes of half-width 4, 8 and 12 (0.996, 0.992, 0.990); the
  escape per interval is the emission within 3 % (0.989: nothing stands, the
  1.5 % the shadow engine shed into parked shares is gone).
- (b) the shell means over ticks 201 to 300 at r = 4, 6, 8, 10 and 12
  (`shell_readings`): the count times r^2 / q between 0.14 and 0.20 (0.157 to
  0.169 measured); the push times 4 pi r^2 / q within 20 % of 1 (0.997 to
  1.16); the size times r / sqrt(q) within 5 % of 3 x 0.2143 = 0.643 (0.622
  to 0.660); the log-log slopes over the five radii: the count -2.00 +- 0.10
  (-2.03), the push -2.00 +- 0.15 (-2.11), the size -1.00 +- 0.10 (-0.95).
- (c) two measured events (21^3, d = 8 on the x axis, no suspension, 200
  intervals, the pushes over ticks 101 to 200): the first (at the lower x)
  pushed toward +x and the second toward -x, the axial pushes equal within
  8 % (2.5 to 5 measured over three windows: whole units without parked
  shares ripple more than the shadow engine's ninths), the transverse parts
  below 3 % of the axial; the measured events' momentum is the sum of the
  pushes at every tick; the axial push against M_B rho M_A / (4 pi d^2) with
  rho = 6/128 between 0.4 and 1.6 (0.62); the product law: both contents
  doubled with K doubled pushed four times as much within 10 % (4.1 to 4.2:
  the far field of the smaller pair is more of beams, single units going by
  their momentum, so the doubled pair reads a few per cent more of what
  comes back).
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
  and counts the clicks the Nodes counted.
- (e) the refusals, naming the law: `contents`, `initial_shadows`,
  `wait_per_quantum`, `schema_version` and `dense_field` (the earlier
  engines' keys), `phase_turn` as an unknown family key, a closed board, a
  world without `"law": "events"`, an unknown key, a content at or past
  K x N / 2, a lamp on a free family, two measured events at one Node, a
  table rule outside `read` | `measure` | `rerelease` | `pass`, an N that is
  not a power of two, a detector on a Node without a measured event, a Node
  in two detectors, a quantum on a free family; the parsed world of (a) has
  one owner of `m`, the suspension 1 and the release 1/128, and a declared
  detector with threshold 3. The runner runs a 4-interval world of (a) into
  `run.json` (`law` "events-v1", completed, four ticks, four books,
  conserved, the measured events and the detectors), `state.json` (the law,
  tick 4, the measured events, Nodes with events) and `events.jsonl`, keeps
  the input as read, and refuses a negative tick count and a used output
  directory.
