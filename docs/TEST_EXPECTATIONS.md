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

Decision of the model owner, 2026-09-19 ([Highlights 5.4](HIGHLIGHTS.md#54-the-detector),
the status line of the law of the shadow): the field-only engine is the one
engine and the old engine is deleted without the confrontation runs; "only
tests that everything is as designed". The suite keeps one module per generic
rule of the engine, on a minimal board, and the repository gates. The deleted
modules are named in the [migration note](MIGRATION.md#one-engine-on-2026-09-19-the-old-engine-deleted).

| Module | Rule isolated |
| --- | --- |
| `test_field_only.py` | The law of the shadow on minimal boards: the books, the fixed point and Gauss's flux, the shell means, the pair's pushes and the product law, the slits, the wait, the refusals, the nearest step, the step by the accumulators ([below](#the-law-of-the-shadow)) |
| `test_node_mixing.py` | The Node's mixing on one Node of the engine's layer: the 3B_h rule, the coherent sum, the largest remainder, the parked ninths and their release, the momentum carried ([below](#the-nodes-mixing-on-one-node)) |
| `test_family_turns.py` | A family's phase turn in flight as a declared rule: by the quantum uniformly (light's default), by the cell's amount, or none; the default by kind, the engine's wiring, one Link of the walk, the remainder per family ([below](#the-phase-turn-in-flight)) |
| `test_family_quantum.py` | A family's quantum as a declared width: the event at an absorbing holder is one whole quantum per number, the rest waiting in the holder's register ([below](#the-quantum-of-a-family)) |
| `test_configuration_validation.py` | The read-only preflight of a world file: the report, the refusals named by the parser, the command line |
| `test_json_documents.py` | The strict decoder shared by world files and the workspace's fragments |
| `test_integer_arithmetic.py` | The shared bounded integer primitives |
| `test_retention.py` | Generated-output ownership, lifetime and cleanup |
| `test_check_scope.py` | The affected-check's selection |
| `test_architecture.py`, `test_locality.py` | The dependency direction (`core` imports only `core`, the engine imports no host module, no physical module imports output or storage), the integer audit of `core/`, and LOCALITY-1 documented without an exception |
| `test_repository_language.py`, `test_repository_hygiene.py`, `test_repository_navigation.py` | The repository gates: English, one canonical copy, navigable links |

## The Node's mixing on one Node

`tests/test_node_mixing.py` isolates `node-mixing-v1` (Highlights 5.4, point
24) and the remainder rule (point 22) on one Node of the engine's layer
(`ShadowLayer` of shape (1, 1, 1), one number, N = 8, no phase turn in
flight), through the kernels of `event_universe/shadow/mixing.py`. The
integers, written down before the first run, are those the old suite pinned
on 2026-09-18 through the old engine's scalar rule, which the kernels
reproduce byte for byte:

| Case | Arrivals (Port, amount, phase) | Departures per Port [+X, -X, +Y, -Y, +Z, -Z] | Phases | Parked ninths |
| --- | --- | --- | --- | --- |
| (a) a lone arrival | +X 9 at 0 | 1, 4, 1, 1, 1, 1 | 0, 4, 0, 0, 0, 0 | none |
| (b) two equal, in phase | +X 9 at 0; -X 9 at 0 | 1, 1, 4, 4, 4, 4 | 4, 4, 0, 0, 0, 0 | none |
| (c) two equal, in antiphase | +X 9 at 0; -X 9 at 4 | 9, 9, 0, 0, 0, 0 | 0, 4, 0, 0, 0, 0 | none |
| (d) two on one heading | +X 9 at 0 and 9 at 2 | 2, 8, 2, 2, 2, 2 | 1, 5, 1, 1, 1, 1 | none |
| (e) unequal | +X 24 at 0; -X 8 at 2 | 6, 11, 3, 3, 3, 3 | 7, 4, 1, 1, 1, 1 | 2, 5, 5, 5, 5, 5 at those phases |
| (f) the remainder rule | +X 5 at 0, twice | 0, 2, 0, 0, 0, 0 each time | 0, 4, 0, 0, 0, 0 | 5, 2, 5, 5, 5, 5 then 10, 4, 10, 10, 10, 10; the release 1, 0, 1, 1, 1, 1 leaves 1, 4, 1, 1, 1, 1 |
| (g) the momentum carried | +X 9 at 0 carrying (9, 0, 0) | 1, 4, 1, 1, 1, 1 | | none; the x momentum 1, 4, 1, 1, 1, 1 with the departures, the sum (9, 0, 0) |

## The phase turn in flight

`tests/test_family_turns.py` isolates `families[i].phase_turn` (the model
owner, 2026-09-19: light turns by its message, the same everywhere, "the
default for light, that is, per family"; DERIVATIONS.md round 8, S5): per
Link walked, `"quantum"` turns every quantum of the family by the family's
quantum over K, the remainder carried per family, whatever the amount in the
cell; `"amount"` turns by the amount in the cell over K, the old rule;
`"none"` turns nothing. Expected, written down first:

| Case | Input | Expected |
| --- | --- | --- |
| (a) the default by kind and the wiring | a free family; a paid one with quantum 16; a free one declared `"amount"`; a paid one declared `"none"`; `phase_turn: true` | none, quantum, amount, none; refused naming `families[0].phase_turn`; the engine's layers carry the same rules and quanta 1, 16, 1, 1 |
| (b) one Link of the walk, K = 16, N = 64, a departure at phase 5 carrying (3, 0, 0) on +X | `"amount"`: 128 quanta; 5 quanta. `"quantum"` with quantum 16: 128; 5. `"none"`: 128; 5 | the arrival at the neighbour at phase 13 (8 steps); 5 (0 steps). 6; 6 (one step whatever the amount). 5; 5. The amount and the momentum (3, 0, 0) unchanged in every case |
| (c) the remainder per family | `"quantum"` with quantum 8, K = 16: the departure walked on the first, the second or the third interval of the layer | at phase 5, 6, 5: a step every second interval, the family's clock advancing whether or not anything was in flight before |

## The quantum of a family

`tests/test_family_quantum.py` isolates `families[i].quantum` (the model owner,
2026-09-19, "put it in, without an experiment"; DERIVATIONS.md round 8, S5 and
S6): at a holder that absorbs a family, the units of one number wait in the
holder's register until a whole quantum is there, then one event of the whole.
One world, three marks of a free family `m` (content 8, fixed, no release) and
two held contents of the paid family `light` (numbers 4 and 5) at the corners,
light's quantum 3, the arrivals given with the board at the marks' Nodes, one
interval. Expected, written down first:

| Case | Input | Expected |
| --- | --- | --- |
| (a) the default and the refusals | no key; 3; 0, -1, 2.5, "3" | 1; 3; refused naming `families[1].quantum` |
| (b) the click, per number, and the books | mark A gets 2 units of number 4 on +X and 2 of number 5 on +Y; mark B 4 of number 4; mark C (`rerelease`) 7 | A: 0 events, pending {4: 2, 5: 2}, push (2, 2, 0); B: 1 click, 3 absorbed and held, 1 pending, push (4, 0, 0); C: 2 events, 6 pooled and released again in the same interval with C's number, 1 pending, push (7, 0, 0); the books balanced, light's shadows absorbed 15, released 6, current 6, held absorbed 3, pending 6 |
| (c) the default | quantum 1, mark B gets 4 | 4 events, 4 absorbed and held, nothing pending |

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
  `core`; the engine (`shadow`) imports only `core` and `shadow`, except
  `shadow/run`, which writes the artifacts; no physical module imports an
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


## The law of the shadow

`tests/test_field_only.py` is the isolated test of `field-only-v1`
([the law of the shadow](ENGINE.md#the-law-of-the-shadow-field-only-v1);
Highlights 5.4, "The law of the shadow: only shadows and events", the model
owner's decision of 2026-09-18, the evening; feature 20), pinned here on
2026-09-18 before its first run, as Highlights 5.5 requires, from
DERIVATIONS.md round 7 (sections 46 to 50: the fixed point of an emitting
thing on the open board, the fixed point in whole quanta, the tests under it,
the run plan) and the readings of the engine's exploratory runs of the same
day (the standing content of the integer rule, the per-Node ripple, the
regime the two-slit needs). The worlds are built as data: one family `m`
(free, charge 0) whose content of 2^24 at rest releases 1/128 of its content
per Port heading per interval (q = 786 432 quanta per interval, the wave
regime q >= 1740 r^2 out to r = 21), N = 64, K = 2^22 (four phase steps per
interval, the period 16), an open cube, the content held in place (`fixed`).

- (a) one content (29^3, 300 intervals): at every tick the books close, the
  held line reads current = initial = 2^24 with nothing absorbed, spent or
  escaped, the shadows' line reads released = current + escaped + absorbed
  with initial 0, and every momentum line is zero (a content at rest carries
  none, its field none). The fixed point within the transit: Gauss's flux
  through the closed surface about the cube of half-width 4 (`cube_flux`)
  is the emission within 2 % over ticks 101 to 200 (2 sqrt 3 H = 48; the
  derivation's "within 2 % by about 2 sqrt 3 H"), and over ticks 201 to 300
  through the cubes of half-width 4, 8 and 12 (the derivation's 1.000 q;
  the integer rule's 0.985 to 0.999); the escape per interval is the
  emission within 3 % (0.983: the remainder rule sheds about 1.5 % of the
  emission per interval into standing content, section 47 (ii)'s residue,
  measured the same at N = 256 in this engine, where the parked release's
  phase and not the circle's width is the source).
- (b) the shell means over ticks 201 to 300 at r = 4, 6, 8, 10 and 12 (the
  Nodes within a half Link of r, `shell_readings`): the count (the amount
  that arrived per Node per interval) times r^2 / q between 0.14 and 0.20
  (the derivation's 0.147 with the standing excess of the integer rule, 0.16
  to 0.17 after 200 intervals); the push (the radial flow, amount x heading
  on the radial unit vector) times 4 pi r^2 / q within 20 % of 1 (the edge's
  ripple per shell, 1.00 to 1.15 measured); the size (the coherent sum in
  32nds over 32) times r / sqrt(q) within 5 % of 3 x 0.2143 = 0.643 (the
  engine reads 3|u|, wait-reads-v1's note; 0.62 to 0.66 measured); the
  log-log slopes over the five radii: the count -2.00 +- 0.10, the push
  -2.00 +- 0.15, the size -1.00 +- 0.10 (the derivation's -2.00 +- 0.03 and
  -1.00 +- 0.03 in the mean field; the integers' -2.00, -1.89, -1.05).
- (c) two contents (21^3, d = 8 on the x axis symmetric about the centre,
  no wait, 200 intervals, the pushes taken over ticks 101 to 200; each
  content reads the other's field and passes it on, round 8 section 54
  (ii): a sink would read the gradient, 1/r^3): the first content (at the
  lower x) is pushed toward +x and the second toward -x, the two axial
  pushes equal within 5 % (the third law by symmetry, round 8 section 55
  (ii): 0.3 to 1.9 % in the mean field, and the rounding of whole units per
  window at N = 64, round 7 section 47 (ii)'s 4 %), the transverse parts
  below 3 % of the axial; the held momentum is the sum of the pushes at
  every tick (no ledger of the field's momentum, S8); the axial push against
  M_B rho M_A / (4 pi d^2) with rho = 6/128 between 0.4 and 1.6 (the free
  flux read on the axis at d = 8 is 1.08 of the law in the mean field with a
  sponge edge, section 55 (i); on this open board the edge's mirror ripples
  the per-Node push by +-2 R r / (2 H - r), +-36 % at r = 8 on 21^3, with the
  anisotropy on top, round 7 section 46 (iii); the law is read in the shell
  mean of (b)); the product law: the
  pair with both contents doubled and K doubled (the same period) is pushed
  four times as much within 5 % (the emission and the cross-section each
  double). An unequal pair is not pinned: the clock is the content, so its
  two fields have two periods with two anisotropies and two transients.
- (d) the two-slit reading (23 x 41 x 9, 200 intervals): a lamp of light (a
  paid family, 2^36 quanta, 2^22 per interval on every heading, its clock
  four steps per interval) at x = 2; a wall at x = 8 of held contents of the
  paid family `wall` (content 1, holding light, the click) with two slits 14
  apart, openings of 3 x 3 Nodes in the wall (a held content that transmits
  stamps its own number on the light, and two numbers are two fields that
  never interfere, point 24: two re-emitting slits give two humps and no
  fringes; and an opening of one Node is far below the wavelength and
  transmits almost nothing; both measured before this pin); a screen of
  marks at x = 17. The marks' light counts by y, summed over z and smoothed
  over three marks, are symmetric about the axis (within 5 % of the axis
  value plus one: the largest-remainder rule's ties to the lower Port break
  the mirror symmetry by a few per cent); with two slits the lowest smoothed
  count 2 to 5 from the axis is exceeded by the highest 6 to 11 from it by
  at least 10 % (the first minimum of two sources 14 apart read 9 behind
  them at the wavelength 16 / sqrt 3 = 9.2 Links lies near 4 from the axis
  and the next maximum near 8.5); with one slit on the axis it is not (the
  control falls from the axis outward). A reading, not a law: the lamp is
  six-fold (a lamp on one heading sheds two thirds of its light into
  standing content beside it), the period 16 (at period 8 the lattice
  anisotropy of a transmitted wave, (15/8) w^2 K_4, cuts the axis by half),
  the light in flight reads no wait.
- (e) the wait (29^3, 300 intervals, the fraction of intervals waited over
  ticks 101 to 300): the content of (a) with nine probes of a paid family
  (content 1, held in place, passing the mass's quanta so that they neither
  push nor mirror) at E11's Nodes about it, (4, 0, 0), (8, 0, 0), (12, 0,
  0), (3, 3, 0), (6, 6, 0), (9, 9, 0), (2, 2, 2), (5, 5, 5), (7, 7, 7), the
  wait one interval per 512 whole units of size read. The mass waits never
  (it reads only its own field, which it does not read) and its phase makes
  four steps per interval; a probe's phase never turns (1 / K) and it
  re-releases nothing; each probe's fraction is between 0.03 and 0.5 (the
  size 3 x 0.2143 sqrt(q) / r in 32nds at 1 / 512 per unit: 0.28 at r = 4,
  0.14 at 8, 0.09 at 12, rippled per Node), and the log-log slope of the
  fraction against r over the nine probes lies between -1.5 and -0.5,
  nearer -1 than -2 (the amplitude, not the flux; -0.85 to -0.94 measured).
- (f) the refusals: the old parser refuses a world of the law for its
  unknown key `law`; the new parser refuses `examples/nature/ring.json` and
  every old key (`schema_version`, `dense_field`, `initial_field`,
  `wait_reads`, `shadow_wait`) naming the law and the key, a closed board, a
  world without `"law": "shadow"`, an unknown key, a content at or past
  K x N / 2, a lamp on a free family, two contents at one Node, a table rule
  outside `rerelease` | `hold` | `pass` | `transmit`, an N that is not a
  power of two; the parsed world of (a) has one owner of `m`, the wait 1 and
  the release 1/128. The runner runs a 4-interval world of (a) into
  `run.json` (`law` "field-only-v1", completed, four ticks, four books,
  conserved), `state.json` (the law, tick 4, Nodes with content) and
  `events.jsonl`, and refuses `--dense-field` on it.
- (h) the step (a bar of 41 x 9 x 9, a content of 2^24 at x = 4 free to
  step, no wait, 60 intervals): given p = (M/16, 0, 0) it steps at ticks 16,
  33 and 50 (the sixteenth interval fills the accumulator; the interval
  after a step is the event's, T2, round 8 section 53), three steps to x = 7;
  given p = (M, 0, 0) it steps at ticks 1, 3, 5, ..., thirty steps to x = 34,
  the cap of a half Link per interval; in both its momentum stays what it was
  given and its push is zero (the accumulator gives back the content; its
  own number pushes nothing, section 54 (i)), its content 2^24 and nothing
  read.
- (g) the layer's nearest phase step (`layer.nearest_step`, over the window
  `step_window` bounds: 1 up to N = 64, 4 at 256, 69 at 4096) equals the
  engine's argmax over the whole circle, the first on a tie, at N = 2, 8,
  64, 256 and 4096 on 4000 random sums per scale (1, 100, 10^9) and on
  directions exactly on and between the steps, and the zero sum.
