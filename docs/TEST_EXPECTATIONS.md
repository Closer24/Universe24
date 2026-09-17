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

## Suite inventory of 2026-09-17

Decision of the model owner, 2026-09-17: the engine is generic, so the suite
keeps one module per generic rule, each exercising that rule in isolation on a
minimal board, and one module per feature of the
[ray-event model](RAY_EVENT_MODEL.md) (issue #169). Before the reduction the
suite had 108 modules and 2,194 tests (2,191 passed, 3 visual-only skipped) in
622 seconds single-process on the recording host; after it, 40 modules and
1,009 tests in 35 seconds on the same host. Seconds are the recorded
durations of the run in the [validation entry](VALIDATION.md#test-suite-reduced-to-one-test-per-rule---2026-09-17)
(tests under five milliseconds are not recorded). The deleted modules and the
deleted example studies are named in the
[migration note](MIGRATION.md#test-suite-reduced-on-2026-09-17-one-test-per-rule).
Feature tests of issue #169 join this table as they land.

| Module | Tests | Seconds | Rule isolated |
| --- | --- | --- | --- |
| `test_architecture.py` | 28 | 0.34 | Static gate: layer dependency direction, formula-free API assembly and the integer audit of every physical module |
| `test_boundary_configuration.py` | 89 | 0.00 | Topology: the six-face neighbor function under periodic and open boundaries, as a pure function and at the schema |
| `test_check_scope.py` | 27 | 0.10 | Changed-code test selection of `tools/check.py`; every resource row names a kept test |
| `test_configuration_validation.py` | 99 | 2.40 | Read-only configuration preflight, format ownership and its CLI, over every shipped input |
| `test_detector_mark.py` | 1 | 0.18 | Issue #169 feature 2: a marked Node draws one bit per arriving ray (`detector-mark-v1`; feature test, untouched) |
| `test_detector_return.py` | 6 | 0.40 | Issue #169 feature 3: a draw of 0 returns the ray reversed on its line, through no coupling, to rest at its event Node (`detector-return-v1`) |
| `test_detector_sampling_contract.py` | 18 | 0.00 | Detector-only sampling admission (running branch, untouched) |
| `test_disturbance_application.py` | 14 | 0.29 | Runner record: headless run files, the saved initialization and source fingerprint that replay a run, explicit CLI opt-ins |
| `test_disturbance_engine.py` | 23 | 0.02 | Carrier Node cycle: budget wait, fixed Link time, split and whole-record transport, exchange remainders, capacity-failure atomicity |
| `test_energy_audit.py` | 9 | 0.31 | Funded ray emission with recoil and absorption under the audit (running branch, untouched) |
| `test_field_spreading.py` | 10 | 0.80 | Issue #169 feature 12: every Node that field content reaches releases it again by the family's split table, amounts adding per heading, the phase of the coherent sum, whole quanta and the remainder through the entry the phase selects; the source sign on the field ray; a returned field quantum walking back until something takes it (`field-spreading-v1`) |
| `test_initialization.py` | 42 | 0.00 | Initialization parser: one fixed schema, resolved references, no physics from names, bounded expression language |
| `test_integer_arithmetic.py` | 75 | 0.00 | Bounded integer arithmetic: signed and ceiling division, remainders, component operations, overflow before cancellation |
| `test_json_documents.py` | 52 | 0.00 | Documentation gate: strict JSON decoding shared by inputs, editor fragments and observer files |
| `test_kerengonen.py` | 19 | 6.88 | Phased rays: phase advance, coherence, capture, slit, mirror and pace (running branch, untouched) |
| `test_local_conservation.py` | 18 | 0.01 | Passive local energy/momentum audit across Node events and Link flux |
| `test_local_conversions.py` | 17 | 0.00 | Two-to-two record conversion (`output_types`) as an atomic inventory transfer with declared balances; record `outputs` rejected |
| `test_local_field_rules.py` | 11 | 0.13 | Local field rule: six-Port reads, retained and outgoing owners, guarded joint proposals |
| `test_local_focus.py` | 31 | 1.28 | Local Focus scheduler equals the ordinary scheduler tick by tick, serial and parallel |
| `test_locality.py` | 7 | 0.00 | Static gate: no world reads or shadow replay in generic field code |
| `test_native_ray_coupling.py` | 33 | 0.04 | Ray interactions, the generic coupling (running branch, untouched) |
| `test_nature_catalog.py` | 4 | 0.12 | Data gate: `catalog/nature.json` parses, every record and reference resolves, every undecided entry names its decider and is tabled in `CATALOG.md`, the register's entries agree, and every runnable ray and decided coupling is built from the file and run for two ticks (pinned below) |
| `test_node_conservation.py` | 13 | 0.00 | Pre-commit conservation readout guard and its bounded readout cache |
| `test_node_rule_contract.py` | 37 | 0.00 | Node profile contract: explicit k*h duration, indexed vector rules, aggregation policies |
| `test_node_state_contract.py` | 9 | 0.31 | Node-state contract: evolving state is formula-free |
| `test_payload_validation.py` | 26 | 0.00 | Signed and unsigned integer codes (zigzag) validate exactly as the decoding reference, without decoding |
| `test_plan_reuse.py` | 8 | 0.16 | Exact transition plan reuse (running branch, untouched) |
| `test_rational_particles.py` | 16 | 0.47 | Opt-in bounded rational ratios: balanced routes, fractional credit, local checks |
| `test_ray_coupling_evidence.py` | 3 | 0.00 | Evidence helper of the ray coupling (running branch, untouched) |
| `test_ray_delay.py` | 6 | 12.78 | Output clocks: rays wait at a loaded Node and the phase per interval shows the wait |
| `test_ray_event_audit.py` | 3 | 0.90 | Issue #169 feature 10: the world ledger per completed tick, exact for amount, momentum and charge through a return, an inverse split, a release, an escape and an external body's sink (`ray-event-audit-v1`) |
| `test_ray_field.py` | 22 | 0.31 | Straight ray transport: DDA heading, emission sweep and shares, shell stock, slots, escape |
| `test_ray_hidden_state.py` | 1 | 0.19 | Issue #169 feature 1: every ray carries its event and its steps (`ray-event-state-v1`) |
| `test_ray_integration_guards.py` | 22 | 0.36 | Ray integration boundaries (running branch, untouched) |
| `test_ray_layers.py` | 2 | 0.28 | Issue #169 feature 5: rules of different layers fire in one interval and an unruled family crosses (`ray-layers-v1`) |
| `test_ray_meeting_conversion.py` | 6 | 0.25 | Issue #169 feature 6: a meeting replaces its rays by declared outputs, an amount split by a declared table, every family's stock exact (`ray-meeting-conversion-v1`) |
| `test_ray_merge_contracts.py` | 16 | 0.04 | Ray merge and ownership boundaries (running branch, untouched) |
| `test_ray_viewer.py` | 1 | 0.15 | Tooling: `tools/ray_viewer/extract.py` reads a runner record into rays, events and captions, pinned below (no browser) |
| `test_repository_hygiene.py` | 6 | 0.05 | Documentation gate: one canonical copy of every file and configuration |
| `test_repository_language.py` | 14 | 5.37 | Documentation gate: English repository text, ASCII paths and identifiers |
| `test_repository_navigation.py` | 8 | 0.09 | Documentation gate: Markdown links and Skill routes resolve |
| `test_retention.py` | 48 | 0.78 | Generated-output retention: 24-hour expiry, writer leases, protected paths |
| `test_spatial_coupling.py` | 53 | 1.01 | Outward-field coupling to carriers: signed rotation, exchange and the equal-and-opposite field reaction |
| `test_spatial_decay.py` | 10 | 0.00 | Finite decay: integer extinction and signed dissipation |
| `test_spatial_interactions.py` | 16 | 0.05 | Atomic carrier/local-field exchange with delayed-commit guards |
| `test_spatial_transport.py` | 23 | 0.00 | Outward field transport: signed octant partitions, weights and remainders |

## Native complete-ray coupling

`test_native_ray_coupling.py` uses the canonical
[finite residence input](../examples/generic-ray-coupling/finite-residence.json).
Two funded axial rays of amount five arrive with phase zero at tick one; after
the next two intervals both are resident with `(phase, delay)` equal to `(1,1)`
then `(2,0)`. Tick four places them at opposite adjacent Nodes with phase three.
Energy ten and total momentum zero remain owned across emission and residence.
Absent coupling, wrong phase, unequal amounts and a missing partner escape
immediately. Declared momentum failure in a later local group publishes no
partial replacements. Duplicate heading entries preserve the original index
and DDA when the semantic vector is unchanged. Delay participates in ray merge
identity, integer bounds and selection; unsupported clock/sampling domains fail
for JSON and typed callers. Label renaming preserves observed motion and cost.
The unchanged carrier false-guard path returns its original records. These
checks establish the interface and finite residence only, not nuclear binding.
Native JSON and typed entry points also reject N-to-M carrier `outputs`; the
shared same-owner evaluator rejects either conversion form before charging or
changing values. The separate family-conversion suite retains its one-to-six,
six-to-one, conservation, capacity, Port and delayed-owner coverage.

## Kerengonen integration guards

The Kerengonen integration regressions in `test_ray_integration_guards.py` cover
ordinary runner momentum accounting through absorption and escape, frozen phase
tables after host-cache eviction (a 32-step world), independent trigonometric
reference entries (3 and 37 through the table builders, 4096 through a field:
a field declares a power of two, [wave-ray families](#wave-ray-families)),
distinguishable external phases and advances under self-exclusion, frozen
departure metadata after emitter changes, largest-share carried advance with
explicit-zero and field-fallback cases, per-field threshold captures that
draw nothing, whole negative threshold rays with insufficient/exact stock, delayed-owner
rejection before stale commits, immutable carrier routing/unrelated fields,
expired emission metadata and conflicting momentum or unsupported response
bindings. `test_kerengonen.py` retains the actual recoil configuration through
the ordinary runner identity test. Coherence work is quadratic in the configured
local phase/ray count; it is bounded relative to world size for fixed capacities,
not a claim of linear host work.

## Active contract coverage and shared execution
Shared builders live in the narrowly scoped `tests/support/disturbances.py`. Its
imports remain dependencies of every consuming test, and it contains no
alternate simulation engine. The bounded-work regressions of
`test_active_node_contracts.py` and the label and declaration-order baselines of
`test_generic_identity.py` (with its helper `tests/support/identity.py`) were
deleted on 2026-09-17 with the suite reduction; `test_initialization.py` keeps
the rule that names and declaration order select no physics.

`test_check_scope.py` requires empty selections to avoid source/dependency scans
while honoring explicit `--tests`. Prior source reads use two Git processes and
preserve exact blobs, including empty files and deleted providers. Old and current
dependency selections, dynamic resource consumers and failure evidence remain
part of the gate; batching does not authorize dropping related tests.

## Source envelopes and null notices (deleted on 2026-09-17)

`test_source_envelope.py` (the exact 3:4 mixing and inverse interference,
signed full emission, rational complex vacuum normalization,
changing-denominator residue, finite allowance exhaustion and overflow
rejection) and `test_null_notices.py` (the Node-level null-notice arithmetic,
notice transport, the applied bank and crossing-null corrections) were deleted
on 2026-09-17 with the source-envelope modules under Highlights section 3.5
(issue #164, bucket B.3); their integration acceptance had gone with the
integration layer on the same day. The dated results stay in
[validation](VALIDATION.md).

## Integer Node execution
`test_node_rule_contract.py` checks six-record frozen permutations, generic vector
widths, explicit fired-rule duration, nonadditive policy rejection and independent
arrival presence. `test_node_conservation.py` checks complete-owner readouts and
rejects nonlinear merge drift (13 becomes 25), unequal momentum, overflow and
capacity errors without modifying inputs. These are correctness contracts for the
[selected model](NODE_VECTOR_PROCESSOR.md), not proofs of quantum dynamics. The
configuration, runtime, joint-reaction, guard-boundary and example modules of
this profile were deleted on 2026-09-17 as duplicates of these two.

## Property coupling and passive local conservation
`test_local_conservation.py` covers local changes and actual packet flux,
pending originals, periodic/open transit, all momentum components, nonlinear
arrival cancellation, passive observation and saved failure reports. These
measurements use explicit candidate quantities, not inferred physical energies.
The property-coupling and entity-profile modules were deleted on 2026-09-17.

## Configuration preflight

The [validation contract](CONFIGURATION_VALIDATION.md) is covered by
`test_json_documents.py` and `test_configuration_validation.py`
(`test_profile_validation.py` was deleted on 2026-09-17). Shipped runnable configurations must pass;
unknown/ambiguous formats, duplicate keys, nonfinite numbers, invalid references,
bad placements and missing/mismatched dependencies must fail. All 46 classical
profiles are checked independently, including unselected rows; subsets remain
valid. Tests forbid world construction
and implicit filesystem access, preserve supplied objects and verify CLI batch
exit/report behavior and rejection before runner artifacts are created. Existing
UI and runner tests retain accepted output and physical execution contracts.
The native event-program validation and the spatial causal-event suites were
deleted on 2026-09-17 with the `event_program` member.

## Local record operations

Deleted on 2026-09-17 (issue #164, bucket B.6): `test_record_operations.py`
(19 tests) covered the merge of delivered records by type and channel, the
reserved slots and the capacity policy of `fields/record_operations.py`. A
delivered record now takes the first spare slot outside the pending lock and
nothing is merged; the receiving-capacity failure and its atomicity stay
covered by `test_disturbance_engine.py`, and the activity predicate and the
cost reporter moved unchanged into `core/disturbance_node.py` (`carrier_work`,
`report_cost`), exercised by every carrier test through the Node.

## Bounded rational particle candidates

`tests/test_rational_particles.py` independently checks: scaled directions
(1,1,0) and (1000,1000,0) give identical alternating hops; coprime (1000,999)
interleaves; direction changes reset fixed routing counters; maximum legal weights
remain bounded through JSON and world transport; credit 1/3 followed by 1/2 then
1/2 produces one hop and 1/3 remaining; mixed -7/3 and 1/2 use whole (-2,0) and
denominator six with remainders (-2,3); finite exact arithmetic rejects overflows
and zero denominators. Rational comparison keys cannot nest or feed arithmetic.
Configured unequal-mass contacts are compared with an independent Fraction
center-of-mass reflection and preserve decoded momentum/energy for 180 ticks.
Zero-mass axis and 3:4 directions cover the same Euclidean distance at c=1/2;
invalid mass-shell data rejects. Even a held zero record executes local checks.
A local reservoir exchanges kinetic energy and opposite momentum, including
carrier transit; insufficient energy and invalid denominators reject atomically.
Existing integer regressions retain their original paths. The headless
`tools/audit_particle_contracts.py` runs longer instances with per-tick exact
diagnostics; supplied formulas are reference benchmarks, not emergence claims.
See [the contract](RATIONAL_PARTICLES.md).

## Generic local field rules

These are focused acceptance requirements for
[LOCAL_FIELD_RULES.md](LOCAL_FIELD_RULES.md), not claims that a particular tree
passed. Reuse the affected run and tests when collecting integration evidence.

| Suite | Independent inputs and required outcomes |
| --- | --- |
| `test_local_field_rules.py` | Two-vector exchange/rotation reads one frozen rule snapshot and preserves its named invariant; existing outward 216-unit pulse still sends 36 to each axial neighbor; retained and six outgoing owners count stock once and wait a full link; signed counterflows remain separately observable; cross-field changes appear as transformations rather than sources; invalid shapes, bounds, schema 2 rules and broken invariants fail before local commit |
| `test_spatial_interactions.py` | Multiple field/carrier assignments commit together; conserved combined components hold; delayed field evolution is preserved when a frozen delta commits; an invariant invalidated by live field changes rejects the whole transaction; pending source bookkeeping is not restored from old carrier state |

Check both a nonzero baseline with no dynamic work and actual received channels
whose net stock is zero. The first must stay quiescent; the second must activate
the local rule. Field-only and carrier-coupled checks must distinguish sampled
input, retained stock, outgoing ownership and actual delayed-commit views.
Generic labels do not establish electromagnetic behavior, and these tests do not
claim a Maxwell, Lorentz or quantum result.

## Generated-output lifetime

These are host filesystem contracts; they do not change simulated time or costs.
See [RETENTION.md](RETENTION.md) for ownership and expiry policy.

| Suite | Independent expectations |
| --- | --- |
| `test_retention.py` | Registered generations expire at 24 hours; later writes extend age; active and dependent writer locks survive future cleanup; unregistered, protected, linked and replaced files survive; interrupted quarantine resumes without deleting replacement data; expected adoption identity rejects stale inventory; concurrent catalog use waits; duplicate watchers share one lock |
| `test_check_scope.py` | Explicit non-import edges retain the kept resource consumers and every row names an existing test; the exact scope report expires while unrelated files survive; dry-run creates no output |

Ordinary test execution leases its JUnit report. Neither test collection nor
cleanup enables rendering.

## Configured boundaries and dormant spatial work

| Suite | Independent expectations |
| --- | --- |
| `test_boundary_configuration.py` | Periodic default under both schemas; exact open/periodic setting; every positive and negative face of a 3x4x5 world; single-node extents; invalid names, coordinates, faces and bounds rejected |
| `test_disturbance_application.py` | Open example records carried escape 72, spatial escape 20 and 52 localized deposits with zero dissipation; no carrier reentry; zero-tick edge case has empty events and zero escape; runner and snapshot agree |

## Finite spatial candidate, schema 2

The law is specified in [SPATIAL_FIELDS.md](SPATIAL_FIELDS.md) and
[SPATIAL_COUPLINGS.md](SPATIAL_COUPLINGS.md). These tests retain the schema 1
conservative expectations and add separate finite attenuation expectations. The
historical dissipative cases select `"residue": "dissipate"` explicitly; omitting
the key selects the default localizing residue.

| Suite | Independent inputs and required outcomes |
| --- | --- |
| `test_spatial_decay.py` | Half retention maps 20 through 10, 5, 2, 1 to 0; both signed one-unit tails vanish even at retention `(MAX_VALUE-1)/MAX_VALUE`; unsigned invalid input cannot be erased by decay |
| `test_ray_field.py` | DDA rays return to their heading after one period with bounded accumulators; emission shares 5 over 2 rays as 3 and 2 and cycles the cursor, and a stock below the sweep count fills the next headings in turn (2 over 4 headings gives 0 and 1, then 2 and 3, then 0 and 1) while a stock that covers the sweep still advances by the whole count; a 64-unit ray source keeps totals at 64 per tick and 64 on every Manhattan shell; a receiver gains 15 momentum from three ticks of 5-unit ray flux; retention 1/2 deposits 4, 2, 1, 1 along a ray or dissipates 8; a third ray phase at a two-slot Node fails explicitly; open boundaries count escaped rays; invalid keys, zero headings, vector fields, octant seeds and the shared clock are rejected; the runner records `isotropic-ray-field-v1`; a ray passes a Node whose receiver reacts to it and reaches the Nodes beyond |
| `test_energy_audit.py` | Funded emission along (1,0,0) and (0,2,0) debits the emitter by 2 per tick and recoils by (-1,-2,0) per tick with the audit closed; a stock of 5 emits 2, 2, 1, 0; `source: true` is still rejected and `recoil_field` needs funding; escaped quanta are measured escape; an absorber banks five quanta with momentum (5,0,0) while quanta beyond it vanish and the audit stays closed; a moving absorber-emitter never eats the wake of the cycle it departed on, and since `ray-event-state-v1` the quantum of the cycle before, a distinct event travelling with it, is absorbed back from the third tick on (38, 36, 35, 34, 33, formerly 38, 36, 34, 32, 30 when the two cycles merged); absorb validation rejects a scalar momentum field and an amount key; a fraction 1/4 absorbs one quantum of each 4-quantum ray and forwards 3; negative quanta pull an absorber with stock 3 by (-2, -1, 0, 0) and credit the emitter 16 with recoil (16, 0, 0); a ray field cannot be both absorbed and exchanged |
| `test_kerengonen.py` | A phase advances by the field's step on every link and wraps, a plain field leaves it alone, and rays merge only with equal phase; the cosine table for four steps is (256, 0, -256, 0), equal phases give coherence exactly one, opposite equal amounts exactly zero and a quarter turn one half; two lamps three links from a Node fire 2-quantum rays at each other and the sampled values along the line are 4, 0, 4, 0, 4 with four steps and 4, 2, 0 with eight, while the plain field reads 4 everywhere and the audit closes on 800 quanta; an absorber between the lamps takes 4 quanta before the opposite pair arrives and nothing after, takes 20 at the in-phase Node, and 20 at the dark Node when the second lamp is offset two steps; the runner records `kerengonen-ray-field-v1` and rejects one phase step, an advance equal to the steps, a missing advance, an emission phase beyond the steps, a phase without the key and the key without ray transport; the double-slit probe composes and closes; the bounded ticket rule advances and squares as specified and no absorber draws from it, the share rule takes 2 whole single quanta at a quarter turn where a half share truncates to nothing (closed on 800 quanta), and an unknown capture, the deleted lottery capture and a capture seed are rejected; a slit that re-emits the phase it absorbed makes a lamp's wave arrive at a Node three links on opposite to a second lamp's (reading 0), equal with that lamp offset four steps (4), and partial at a fixed re-emission phase (3), and a carried phase without an absorb rule is rejected; a ray with its own advance ignores the field's, rays of different advance do not merge, beams of momentum 16 and 32 at advance |p|/4 carry advances 4 and 8 with phases in ratio two after the same links, a negative advance and one without the key are rejected, and a slit re-emits the absorbed advance so readings are 2, 4, 0 for lamp offsets 0, 16, 48 on a 64-step field; a mirror sends a lamp's wave back along -x with the carried phase, holds 4 quanta and the reversed momentum, closes on 400 quanta, and the line reads 0, 2, 5, 7, 7, 5, 2, 0, 0, 2, 5 at advance 4 (period 8) and 6, 1, 1, 6 repeating at advance 8 (period 4); a mirror without every image heading, without a recoil field, on an unknown axis or without an absorb rule is rejected; a three-layer screen's first layer absorbs exactly what a one-layer screen does and the layers behind add to it, both worlds closed; a dissolving record of 10 quanta with after 3 and over 4 holds 10, 10, 10, 7, 4, 1, 0 and a moving one flies while it holds quanta and stops at x = 2 when empty, both closed; dissolution on a sourced emission, an emission without amount or dissolve, and over_ticks 0 are rejected; on the Euclidean metric the integer square root is exact at 0, 1, 2, 3, 4, 15, 16, 17 and a million, the paces of an axis, face and body diagonal are 2364/4096, 2364/2896 and equal, twelve ticks carry the first axis ray 6 links, the face diagonal 9 and the body diagonal 12, the world closes on 400 quanta and an unknown metric is rejected; a diagonal `xy` mirror returns the +x ray along +y with nothing back along -x, and a quarter-fraction mirror passes 3 of every 4 quanta and returns 1, closed; a directed emitter with `heading` fires every ray along -x and closes, and a heading outside the field's list or combined with a mirror is rejected |
| `test_ray_hidden_state.py` | Every ray carries its event and its steps ([ray hidden state](#ray-hidden-state)): a sweeping lamp's six rays carry mask 63 and shares (3, 3, 3, 2, 2, 2) with steps and phase equal to the tick; rays of two events with one heading and phase stay two rays (7t rays after t ticks); a returning ray walks steps 5 to 0 and phase 1 to 4 backward, is kept resident at steps 0 and is refused a Link beyond its event Node; 1200 quanta and zero momentum every tick, the audit passed, the runner recording `ray-event-state-v1` |
| `test_detector_mark.py` | A marked Node draws one bit per arriving ray ([Node Detector bit](#node-detector-bit)): six lamps around one marked Node with setting 1/2 and seed 3 arrive in one interval and draw (0, 0, 0, 1, 1, 0) in Port order, exactly two clicks (Ports 3 and 4, amounts 4 and 5), the two rays that drew 1 leave with `detector` 2 and continue unchanged while the four that drew 0 leave with `detector` 1 reversed and rest at their lamps from tick 2 on, the marked and the unmarked control world agree on totals, momentum and lamps at every tick, the control consumes no ticket, a replay writes the same events and run record, the runner records `detector-mark-v1`, and a mark without a setting, a setting above 1, a zero denominator, a seed at the modulus, a duplicate or outside position and a world without an admitted ray field are rejected |
| `test_detector_return.py` | A draw of 0 returns the ray ([Detector return](#detector-return)): for each of the six unit-axial headings a lamp's ray of 8 is halved by an absorber one Link before the marked Node, drawn 0 there at tick 3 (seed 3, setting 1/2), reversed with `outbound` 0 and no click, walks back one Link per tick with steps 3, 2, 1, 0 and phase 3, 2, 1, 0, crosses the absorber untouched, reaches the lamp at tick 6 with the phase it left with and, since `inverse-split-v1`, is restored to the lamp (a one-line event has no sibling line; the lamp holds 4 and momentum -4u after tick 7) and emitted again by it as a new event of 4 after tick 8, 8 quanta and zero momentum every tick, one `detector_return` and one `inverse_split` event, the runner recording `detector-return-v1` and `inverse-split-v1`, and a returning ray at an open boundary refused |
| `test_inverse_split.py` | A returned ray at its event Node performs the inverse split by the world's `return_mode` ([Inverse split](#inverse-split)): a pair lamp at X sends 4 quanta each way on one line, arm A's ray is returned at a marked Node three Links out and reaches X at tick 6; at tick 7 in `siblings` and `straight` a transmission of 4 with A's phase 0 and bit 0 leaves X on arm B's line and never shares a Node with B (B is 6 Links ahead, the round trip), the lamp holding 0 quanta and momentum 8u; in `annul` the share ends at X, the lamp unchanged and `annulled_totals()` 4 quanta and momentum 4u; totals, momentum, the spatial accounting and the conservation report exact at every tick, one `inverse_split` event, the runner recording `inverse-split-v1` and the mode, and an unknown mode rejected |
| `test_ray_layers.py` | Rules of different layers fire in one interval and an unruled family crosses ([ray layers](#ray-layers)): five rays of families a, a, b, b, c meet at one Node after tick 2; after tick 3 the a rays have swapped headings (mask 3, shares (5, 5, 0, 0, 0, 0), steps 1), the b rays have turned to +Z and -Z at phase 7 (mask 48, shares (0, 0, 0, 0, 5, 5), steps 1) and the c ray is one Link past the Node unchanged (mask 16, steps 3, phase 3); the derived layers are (a), (b), (c) whether or not the b rule is declared, and without it the b rays cross like c; totals 10, 10, 5 and zero momentum every tick with the audit passed, the runner recording `ray-layers-v1` and the layer families |
| `test_ray_meeting_conversion.py` | A meeting replaces its rays by declared outputs ([ray meetings with outputs](#ray-meetings-with-outputs)): two rays of 5 meet at one Node after tick 2; with four declared outputs the meeting returns four new rays on Ports 2 to 5 with amounts 2, 2, 3, 3, steps 0, mask 60 and shares (0, 0, 2, 2, 3, 3), and nothing stays at the Node; with the table [8, 7, 4, 1, 0, 1, 4, 7] the shared 10 goes 10:0, 0:10, 5:5 and 8:2 to the two Ports at phase differences 0, 4, 2 and 1, the rest output owning the remainder and the moved momentum booked as a source; outputs that break the amount or the momentum invariant are rejected before any owner changes, malformed tables at initialization; the runner records `ray-meeting-conversion-v1` |

The runner must distinguish actual physical conservation from balanced loss
accounting. It checks tracked combined quantities and every spatial owner,
including a nonconserved computation field. The public examples
`finite_fields.json` and `three_mass_finite.json` require no visualization.

## Active generic disturbance contracts

The primary Simulation follows [DISTURBANCES.md](DISTURBANCES.md). Schema and
engine tests must use independent examples for the contracts below. These are
acceptance requirements, not a statement that a particular source tree passed.

| Input or boundary | Required outcome |
| --- | --- |
| Complete JSON initialization; renamed field/type labels | Equivalent declared behavior with no physical-name branches |
| Unknown/duplicate names or keys, wrong components, floats, unsupported expressions | Validation error before simulation |
| Whole-record move with scalar amounts and a vector attribute | One owner and unchanged carried values in free transport |
| 12 units, weights `[2,0,1,0,0,0]` | 8 through +X, 4 through +Y |
| Signed vector splitting and indivisible amounts | Component totals exact; bounded retained allocation state |
| Conserved-field assignment without source flag | Rejection; explicit source change included only when committed |
| Local exchange from donor to receiver | Equal-and-opposite component changes; both sides commit together |
| Exchange drives unsigned field negative | Failure before either proposed record is committed |
| `B=10`, costs 10, 11, 21 | Total earliest arrival after cycle start is `tau`, `2*tau`, `3*tau` |
| Delayed local cycle with later arrivals | Frozen original proposal; arrivals cannot overwrite locked records |
| Waiting originals and in-flight packets | Each conserved amount counted exactly once at every completed tick |
| Receiving/outgoing capacity or arithmetic bound exceeded | Explicit stopped run with retained ownership, no hidden queue or dropped record |
| Missing CLI `--init` | Error without implicit built-in physics |
| Ordinary headless run | Input, event, metadata and final-state files; no frame capture/render import |

`test_initialization.py` covers the parser and examples;
`test_disturbance_engine.py` covers generic ownership, timing and arithmetic;
`test_disturbance_application.py` covers required initialization, headless output
and run metadata. Standard checks are headless. Only
`pytest --visualize-runs` enables rendered run reports and presentation-only
checks; physical invariants remain active without it.

The remaining scalar, source, stream, collision, link and turning expectations
are retained for explicitly selected historical research APIs. Their results do
not establish those laws for arbitrary configured disturbances.

## Configured spatial fields

`test_spatial_transport.py` checks independent signed scalar/vector partitions,
octant signs, bounded phases, odd weights and overflow rejection.

`test_spatial_coupling.py` checks all signed rotation axes, explicit noncommuting
axis order, carried fractions, exact carrier norm, equal-and-opposite field
reaction, pre-emission local samples, frozen delayed proposals, reaction
overflow atomicity, field/type renaming, scalar flux and headless execution.
The exact contract is [SPATIAL_COUPLINGS.md](SPATIAL_COUPLINGS.md). In the
straight cardinal flux-driven isolation case, own flux is parallel to the carried
vector and changes neither it nor its fractional turn state. A transverse-source
control must still turn the carrier. This does not establish arbitrary self
attribution after a turn or through periodic boundaries.

## Tests by responsibility

| Test file | Responsibility | Expected outcome |
| --- | --- | --- |
| `test_integer_arithmetic.py` | Shared integer arithmetic | Exact quotient and remainder for either sign; bounded working register; component operations reject overflow before cancellation |
| `test_architecture.py` | Layer separation | Reject forbidden imports and adapter formulas; audit integer physics |
| `test_repository_language.py` | English repository text | Reject legacy non-English scripts in project prose; preserve mathematical notation |

Paths are relative to `tests/`. The dependency rules live in
`tests/architecture_rules.py`. Allowed and rejected examples test the rules
including relative imports and aliases.

## Exact numerical examples

| Calculation | Input | Expected result |
| --- | --- | --- |
| Signed division | 7 and -7 by 3 | Quotients 2 and -2 with remainders 1 and -1; the identity `n == q*d + r` holds for every sign at denominators 1, 12 and 64 |
| Ceiling division | 15 by 7 | 3; a negative numerator or a nonpositive denominator is rejected |
| Scaled division with carried remainder | Value 5, numerator 2, denominator 3, remainder 1 | Quotient 3, remainder 2; value -5 with remainder -1 gives -3, -2 |
| Intermediate overflow | Product exceeds 64-bit work bound, even with a cancelling remainder | OverflowError at multiplication |
| Cross product | `(2,-3,4)` and `(-1,5,2)` | `(-26,-8,7)`; parallel vectors give `(0,0,0)` |

These are independently fixed expectations. Conservation tests also use identities
such as the sum of carrier and field quantities before and after an exchange.
Regression assertions use independently specified physical outcomes rather than
copying the tested formula. Historical engine/API and old-Python compatibility
are not acceptance targets.

## Calculation ownership

Shared bounded arithmetic lives in `core/integer.py`; `core/state.py` and its
register and scaling helpers were deleted on 2026-09-17 with their last quantum
consumers.

API assembly contains no independent arithmetic. Architecture checks reject
runtime formulas in that module. Configuration and initial conditions are
intentionally specific and tested through the behavior they produce. The
framework remains constrained to 3D, six neighbors and the declared fixed
node schema.

## Running and validating changes

The suite reuses world runs when their inputs and required observations coincide.
The historical scalar, stream, link, collision and balanced regressions were
deleted with their engines on 2026-09-17 (issue #164, bucket A), and the same
day the suite was reduced to one module per generic rule and one per feature
of the ray-event model ([inventory](#suite-inventory-of-2026-09-17),
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
- A generic field module importing an engine through `from ..core import
  disturbance_engine`, or model state such as `Config`, must be rejected,
  including aliased and relative forms.
- API assembly containing `x + 1` or `source * count` must fail the assembly
  gate; literal configuration such as `DisturbanceLaw(100, 1, 2)` and type
  annotations must pass, because selecting parameters is composition while the
  reusable component owns the formula.
- These tests do not run worlds and do not prove that an agent in another
  conversation has read the instructions.

## Locality and bounded local work

`test_locality.py` creates no world and advances no time. Negative source
examples in generic field modules must reject global node or particle access,
occupancy/history reads and shadow step/run calls. The normal architecture test
scans all production modules with the same guard.
LOCALITY-1 also requires manual end-to-end provenance and loop-bound review;
passing these finite checks alone does not establish general O(1) complexity.

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

## Causal event ledger

`test_event_links.py` and the ledger it checked were deleted on 2026-09-17
under issue #164 bucket B.4 (Highlights 3.20: there is no register), after the
quantum event network, the origin cells and their suites went the same day.

## Local field impulse and node ownership
`tests/test_node_state_contract.py` verifies formula-free evolving state on the
[local field impulse input](../examples/local_lorentz_field.json) and rejects
injected ASTs, laws, callbacks and formula strings. The pulse-behavior modules
`test_local_lorentz_field.py` and `test_lorentz_response_physics.py` were
deleted on 2026-09-17; see [the scoped candidate contract](LOCAL_LORENTZ_FIELD.md).

## Executable entity and conversion expectations
`tests/test_local_conversions.py` checks two-to-two ownership, ignored output
defaults, causal/delayed commits and rejected invalid balances or carried progress
on the [catalog conversion input](../examples/known-entities/conversion.json),
and that an `interactions` entry with `outputs` (the N-to-M conversion of
records, deleted on 2026-09-17 with issue #164 bucket B.6) is rejected at
initialization. The catalog compiler, profile and family-conversion modules were
deleted on 2026-09-17; the conversion rule is covered here alone.

## Repository consistency and canonical references

`test_repository_hygiene.py` rejects nonempty byte-identical files and JSON copies
that differ only in formatting or object-key order. Negative cases insert a real
copy; controls retain different array order and allow empty package markers.
The duration guard also rejects initialization copies distinguished only by
`ticks`; the ordinary runner already supports an explicit duration override.
Distinct operation-budget and boundary controls remain separate experimental
inputs. These checks do not detect arbitrary semantic duplication or replace
ownership review.

`test_repository_language.py` covers source paths, Python identifiers and prose,
including PowerShell and interpreter-selection files. Paths and identifiers use
ASCII names; scientific notation remains allowed in prose. Deliberate escaped
multilingual negative fixtures verify rejection. Latin-script English still needs
human review; a script check cannot certify natural-language meaning.

`test_repository_navigation.py` scans Markdown throughout the source tree,
including nested example READMEs, and requires the documentation index to route
every document. Missing-file and missing-heading examples must fail.

## Shared integer arithmetic

`test_integer_arithmetic.py` covers decoded scalar/vector addition and
subtraction, ordered sums, dot/cross products and integer rounding. Independent
examples include (3,-4,2) dot (-1,7,-2) = -35, (2,-3,4) cross (-1,5,2) =
(-26,-8,7), and (3,4,0) squared norm = 25. Empty reductions, unequal component
counts, cross-product orientation/parallel vectors, signed limits and overflow
before cancellation are separate boundaries. Ceiling 15/7 is 3; signed division
-7/3 returns (-2,-1). Ceiling division rejects an overflowing adjusted numerator
even when the quotient would fit, preserving existing timing behavior.

Existing expression, spatial transaction, rotation, engine timing and link
transport suites remain the integration coverage for callers and operation costs.

## Ray integration and local Focus

`test_ray_merge_contracts.py` independently covers funded inventory during a
load wait, waiting-time absorption, retained-owner capacity and shape, full ray
packet validation before residents merge, exact 100005/3 share capture, unfundable
negative threshold capture, directed self-exclusion and maximum pace inputs.
`test_local_focus.py` checks per-tick inventory, snapshots, ordered events and
modeled cost against the unchanged ordinary scheduler, including six-Port
revisits, pending delays, failure timing, parallel execution and explicit fallback.
Host visit reduction is distinct from physical O(1) local work.

## Exact transition reuse

`test_plan_reuse.py` checks all carrier and spatial planning arguments, including
local phases, resident rays, computation cost and time; hash collisions; bounded
LRU eviction; retry after failure; independent configurations; and default reuse
of repeated moving patterns in serial and parallel execution. Each tick retains
identical inventory, snapshots, ordered events, operation cost and local clocks.
The Focus, field, delay and formula-free state tests remain consumers of this
host-only optimization; `test_active_ports.py` was deleted on 2026-09-17.
Timing is measured outside CI assertions with identical inputs; no speed threshold replaces physical equality.

## Payload validation and readout reuse

`test_node_runtime.py` was deleted on 2026-09-17.
`test_payload_validation.py` tables signed, unsigned,
negative-in-unsigned, largest, zero, above-bound, negative, float and bool
codes and wrong component counts for field and spatial-state validation
against the original decoding reference, with identical messages in the same
order, and confirms that validation decodes no component.
`test_node_conservation.py` also checks that repeated readouts of equal
payloads reuse host evaluations with identical results, that changed values,
bundles or quantities miss the bounded cache while bookkeeping outside the
values hits it, and that failed readouts are requested again and never retained.

## Ray hidden state

`test_ray_hidden_state.py` builds its board inline under the shared Detector
admission (schema 1, `link_ticks` 1, `metric: "links"`, pace 1/1, no decay,
the six unit-axial headings in Port order, closed under negation) on a
periodic 15^3 lattice with an 8-step phase advancing 1 per Link
([ray state](SPATIAL_FIELDS.md#ray-state-ray-event-state-v1)). Lamp A at
(5,7,7) holds 600 quanta and emits 15 per tick, funded, swept over the six
headings from cursor 0 with emission phase 0: six rays of amounts 3, 3, 3,
2, 2, 2 through +X, -X, +Y, -Y, +Z, -Z, so every ray of one emission carries
mask 63 and shares (3, 3, 3, 2, 2, 2). Lamp B at (7,7,7), on A's +X line two
Links on, holds 600 and emits 4 per tick through +X only (`heading` +X) with
emission phase 2, the phase A's ray carries when it passes B: mask 1, shares
(4, 0, 0, 0, 0, 0). Each lamp recoils into its own momentum. Pinned before
the first run:

- (a) after tick t (1 to 4) the Node t Links from A along each Port holds
  exactly one ray of A's first emission: heading index equal to the Port,
  amount 3, 3, 3, 2, 2, 2 by Port, `steps` t, phase t, `outbound` 1,
  `detector` 0, `event_ports` 63, `event_shares` (3, 3, 3, 2, 2, 2); `steps`
  equals the Links walked at every tick;
- (b) `merge_rays` keeps two rays of heading 0, accumulators (0,0,0) and phase
  3 apart when their events differ (amount 3, steps 3, mask 63 against amount
  4, steps 1, mask 1) and sums two copies of the first to amount 6; in the
  world, after tick 3 the Node (8,7,7) holds two rays, A's of tick 1 (amount
  3, steps 3) and B's of tick 3 (amount 4, steps 1), both phase 3, and after
  tick 4 they are at (9,7,7) with steps 4 and 2 while (8,7,7) holds the next
  pair with steps 3 and 1, `ray_count` 2 where the former merge rule held one
  ray of amount 7; the world holds 7t rays after tick t: 7, 14, 21, 28;
- (c) a ray constructed with `outbound` 0, `steps` 5 and phase 1 on the +X
  heading, forwarded five times, leaves through Port 0 each time with `steps`
  4, 3, 2, 1, 0 and phase 0, 7, 6, 5, 4; a sixth forwarding keeps it
  resident with `steps` 0 and phase 4 and sends nothing (`detector-return-v1`,
  updated 2026-09-17: a returned ray at its event Node is resident and
  inert), and `advance_ray` refuses it a Link ("event Node"); `validate_rays`
  rejects `steps` -1, `outbound` 2, `event_ports` 64, a share where the mask
  bit is zero, and `detector` 3;
- (d) totals stay at 1200 quanta with audited momentum (0, 0, 0) every tick:
  after tick 4 lamp A holds 540 with momentum (0, -4, 0), lamp B 584 with
  momentum (-16, 0, 0), and the rays 76 with momentum (16, 4, 0); the
  conservation report passes and the spatial accounting balances; the runner
  records `ray_state: "ray-event-state-v1"` beside `sampling_profile:
  "detector-only-v1"`, `conserved_at_every_completed_tick` true and final
  quanta 1200.

Existing worlds keep their amounts, phases, totals and audits; the one pinned
change is the moving absorber-emitter of `test_energy_audit.py` above, whose
earlier-cycle wake is a distinct event and no longer merges with the excluded
one.

## Node Detector bit

`test_detector_mark.py` builds its board inline under the shared Detector
admission (schema 1, `link_ticks` 1, `metric: "links"`, pace 1/1, no decay,
the six unit-axial headings in Port order, closed under negation) on a
periodic 15^3 lattice with an 8-step phase advancing 1 per Link
([Detector mark](DETECTOR_SAMPLING.md#the-detector-mark-detector-mark-v1)).
The Node C = (7,7,7) carries the one mark, setting `[1, 2]` and seed 3. Six
lamps stand one Link from C, one on each side, each aimed at C through a
directed emission (`heading`) and holding exactly the amount it emits, funded,
so each fires once at tick 0 and holds 0 afterwards: by the Port of C the ray
comes in through, Port 0 (+X) the lamp at (8,7,7) emitting -X with amount 1,
Port 1 (-X) the lamp at (6,7,7) emitting +X with amount 2, Port 2 (+Y) the
lamp at (7,8,7) emitting -Y with amount 3, Port 3 (-Y) the lamp at (7,6,7)
emitting +Y with amount 4, Port 4 (+Z) the lamp at (7,7,8) emitting -Z with
amount 5, Port 5 (-Z) the lamp at (7,7,6) emitting +Z with amount 6; 21
quanta in all, every emission at phase 0, every lamp recoiling into its own
momentum. The control world is the same document without `detectors`. Pinned
before the first run from the published rule (`state = (state x 48271 + 1)
mod 1073741789`, `number = state^2 mod 1073741789`, bit 1 when
`2 x number < 1073741789`):

- (a) the six rays arrive at C at tick 1, one per Port, and are drawn in Port
  order from seed 3: ticket states 144814, 547865861, 846455051, 135470005,
  185116346, 71969709; numbers 570000605, 726844321, 834939851, 327526431,
  382336536, 965202535; bits (0, 0, 0, 1, 1, 0). Exactly two clicks, both at
  tick 1 and position (7,7,7): Port 3, family `quanta`, amount 4, bit 1, and
  Port 4, family `quanta`, amount 5, bit 1; a draw of 0 records nothing.
  After tick 1 C holds six rays (`ray_count` 6): the ray that came in through
  Port p has heading index `p ^ 1` (it travels toward the opposite side),
  amount p + 1, `steps` 1, phase 1, `event_ports` `1 << (p ^ 1)` and
  `event_shares` its amount on that Port; the rays of Ports 3 and 4 carry
  `detector` 2 and `outbound` 1, and (`detector-return-v1`, updated
  2026-09-17) the rays of Ports 0, 1, 2 and 5 carry `detector` 1 and are
  returned: heading index p (reversed on their line), `outbound` 0, amount,
  steps and phase as they arrived; four `detector_return` events at tick 1
  and position (7,7,7), Ports 0, 1, 2 and 5, family `quanta`, amounts 1, 2, 3
  and 6, after the two clicks in the event stream;
- (b) after tick t (2 to 4) the passed ray that came in through Port p (3
  and 4) is t - 1 Links beyond C on the opposite side, at C minus (t - 1)
  times the unit vector of Port p, with `steps` t, phase t, its amount and
  its bit unchanged: after tick 2 at (7,8,7) and (7,7,6); the returned ray
  of Port p (0, 1, 2 and 5) leaves C at tick 2 through Port p, the Port it
  came in through, reaches its lamp's Node C plus the unit vector of Port p
  ((8,7,7), (6,7,7), (7,8,7), (7,7,6)) with `steps` 0 and phase 0 and stays
  there resident and unchanged through tick 4 (after tick 2 the Nodes
  (7,8,7) and (7,7,6) each hold two rays, a passing and a resident returned
  one, which never merge); the six rays are the whole ray inventory of the
  world at every tick;
- (c) the marked world and the control world agree at every tick 1 to 4 on
  the totals (21 quanta, momentum (0, 0, 0): a returned ray's momentum reads
  as its share on the event's heading), on the audited energy and momentum,
  and on every lamp's stock and recoil (0 quanta each; momentum (1,0,0),
  (-2,0,0), (0,3,0), (0,-4,0), (0,0,5), (0,0,-6)); the control's six rays all
  continue, at C minus (t - 1) times the unit vector of Port p after tick t
  with `steps` t and phase t, and carry `detector` 0 everywhere, its Nodes
  carry no mark and it records no click and no return; neither world's
  unmarked Nodes call the ticket rule, and the control world never does (a
  monkeypatched `next_ticket` fails the test if called);
- (d) the runner run twice on the same document writes the same
  `events.jsonl` byte for byte, including exactly two `detector_click`
  lines and four `detector_return` lines, and the same `run.json` apart from
  `elapsed_seconds`, recording `detector_mark: "detector-mark-v1"` and
  `detector_return: "detector-return-v1"` beside `sampling_profile:
  "detector-only-v1"` and `ray_state: "ray-event-state-v1"`, with
  `conserved_at_every_completed_tick` true and final quanta 21;
- (e) `parse_initial_state` rejects a mark without `setting`, a setting
  `[3, 2]`, `[1, 0]` or `[-1, 2]`, a seed of 1073741789 or -1, two marks at
  one position, a mark outside the shape, marks on a world without a ray
  field, and marks on a Euclidean-metric ray field; `validate_configuration`
  reports the same documents invalid.

## Detector return

`test_detector_return.py` builds its board inline under the shared Detector
admission (schema 1, `link_ticks` 1, `metric: "links"`, pace 1/1, no decay,
the six unit-axial headings in Port order, closed under negation) on a
periodic 15^3 lattice with an 8-step phase advancing 1 per Link
([Detector return](DETECTOR_SAMPLING.md#the-return-detector-return-v1)), one
world per heading p (Port index 0 to 5, unit vector u). The Node M = (7,7,7)
carries the one mark, setting `[1, 2]` and seed 3. The lamp stands three
Links before M at L = M - 3u, holds 8 quanta and emits them once at tick 0
through a directed emission on heading u, funded, with emission phase 0,
recoiling into its own momentum. A sail stands one Link before M at
N = M - u, holds 0 quanta and absorbs half of every resident ray
(`fraction` 1, `fraction_denominator` 2) into its quanta and `share x
heading` into its momentum. Pinned before the first run from the published
ticket rule (one draw, seed 3: state 144814, number 570000605, bit 0, as the
first draw of [Node Detector bit](#node-detector-bit)):

- (a) exact tick table of the one ray of the world (position, heading index,
  amount, `steps`, `outbound`, phase, `detector`) after each tick, for
  p = 0 (u = +X, L = (4,7,7), N = (6,7,7)); for another p the positions are
  L + t u, N and M and the heading indices p and p ^ 1:
  tick 1: (5,7,7), 0, 8, 1, 1, 1, 0;
  tick 2: (6,7,7), 0, 8, 2, 1, 2, 0;
  tick 3: (7,7,7), 1, 4, 3, 0, 3, 1 (the sail took 4 on the cycle after the
  ray's arrival at N, the ray reached M with 4, drew 0 and was returned in
  that interval: heading negated, `outbound` 0, amount, steps and phase as
  they arrived);
  tick 4: (6,7,7), 1, 4, 2, 0, 2, 1;
  tick 5: (5,7,7), 1, 4, 1, 0, 1, 1 (it crossed N on the cycle after tick 4
  without absorption: the sail still holds 4);
  tick 6: (4,7,7), 1, 4, 0, 0, 0, 1 (at L, its event Node, with phase 0, the
  phase it left with);
  ticks 7 and 8: (4,7,7), 1, 4, 0, 0, 0, 1, resident and unchanged, the lamp
  beside it emitting nothing; the ray's accumulators are (0,0,0), `wait` 0
  and `interaction_delay` 0 at every tick, its `event_ports` `1 << p` and
  `event_shares` 8 on Port p throughout;
- (b) the sail holds 0 quanta and momentum (0,0,0) after ticks 1 and 2 and
  4 quanta with momentum 4u after every tick from 3 to 8; the lamp holds 0
  quanta and momentum -8u from tick 1 on; the totals are 8 quanta and
  momentum (0,0,0) at every tick, the conservation report passes and the
  spatial accounting balances; the momentum read from the rays in the world
  (`ray_momentum`) is 8u after ticks 1 and 2 and 4u after every tick from 3
  on, the returning ray reading as its share on the event's heading; the
  world holds exactly one ray at every tick, and `ray_count` at M after tick
  3 and at N after tick 4 is 1;
- (c) no `detector_click` is recorded, and exactly one `detector_return`:
  tick 3, position (7,7,7), Port p ^ 1 (the Port the ray came in through and
  leaves by), family `quanta`, amount 4; the mark's ticket state after the
  draw is 144814;
- (d) the runner on the same document records `detector_return:
  "detector-return-v1"` beside `detector_mark: "detector-mark-v1"`,
  `sampling_profile: "detector-only-v1"` and `ray_state:
  "ray-event-state-v1"`, `conserved_at_every_completed_tick` true, final
  quanta 8 and final momentum (0, 0, 0); a second run writes the same
  `events.jsonl` byte for byte;
- (e) on an open boundary, a packet holding a returning ray that would
  escape is refused by the engine with a validation error ("event Node")
  and records no escape.

## Inverse split

`test_inverse_split.py` builds its board inline under the shared Detector
admission (schema 1, `link_ticks` 1, `metric: "links"`, pace 1/1, no decay,
the six unit-axial headings in Port order, closed under negation) on a
periodic 15^3 lattice with an 8-step phase advancing 1 per Link
([Inverse split](DETECTOR_SAMPLING.md#the-inverse-split-inverse-split-v1)),
one world per `return_mode` (`siblings`, `straight`, `annul`). The pair
lamp stands at X = (7,7,7), holds 8 quanta and emits them once at tick 0 as
a sweep of two headings (`rays_per_tick` 2, cursor 0: +X and -X), funded,
emission phase 0, recoiling into its own momentum: one event with mask 3 and
shares (4, 4, 0, 0, 0, 0), arm A the ray on +X (u = (1,0,0)) and arm B the
ray on -X. The Node M = (10,7,7) on arm A carries the one mark, setting
`[1, 2]` and seed 3 (one draw: state 144814, bit 0, as in [Detector
return](#detector-return)); arm B is free. Pinned before the first run:

- (a) the rays of the world after each tick (position, heading index,
  amount, `steps`, `outbound`, phase, `detector`), the same in every mode
  through tick 6: arm A at (7 + t, 7, 7), 0, 4, t, 1, t, 0 after ticks 1 and
  2, returned at M after tick 3 as (10,7,7), 1, 4, 3, 0, 3, 1, then
  (9,7,7), 1, 4, 2, 0, 2, 1 after tick 4, (8,7,7), 1, 4, 1, 0, 1, 1 after
  tick 5 and (7,7,7), 1, 4, 0, 0, 0, 1 after tick 6, at X; arm B at
  (7 - t mod 15, 7, 7), 1, 4, t, 1, t mod 8, 0 after every tick t from 1 to
  10 (at (0,7,7) after tick 7, (14,7,7) after tick 8), never sharing a Node
  with the transmission; every ray's `event_ports` is 3 and `event_shares`
  (4, 4, 0, 0, 0, 0) through tick 6;
- (b) at tick 7, in the cycle after arm A's ray reached X, the inverse
  split: in `siblings` (arm A's own Port is 0, the one sibling Port is 1)
  and in `straight` (the one Port opposite Port 0 is 1) one transmission
  leaves X on arm B's line and is at (7 - (t - 6), 7, 7), 1, 4, t - 6, 1,
  t - 6, 1 after every tick t from 7 to 10, a new event ray with
  `event_ports` 2 and `event_shares` (0, 4, 0, 0, 0, 0), arm A's phase 0
  at X and its bit 0; in `annul` no ray is at X and none leaves;
- (c) the lamp holds 0 quanta and momentum (0,0,0) after ticks 1 to 6 in
  every mode (its two recoils cancel); from tick 7 it holds 0 quanta and
  momentum (8,0,0) in `siblings` and `straight` (the returned share
  restored, 4u, then the transmission funded from it, another 4u) and 0
  quanta and momentum (0,0,0) in `annul` (restored, then paid into the
  sink); the lamp keeps nothing of the returned share in any mode;
- (d) the totals are 8 quanta and momentum (0,0,0) at every tick in
  `siblings` and `straight`; in `annul` 8 quanta and (0,0,0) through tick 6
  and 4 quanta and momentum (-4,0,0) from tick 7, with `annulled_totals()`
  4 quanta and (4,0,0) from tick 7 (zero before), so initial = current +
  escaped + annulled; the spatial accounting balances and the conservation
  report passes at every tick in every mode, its `annulled` entry reading
  energy 4 and momentum (4,0,0) from tick 7 in `annul`;
- (e) exactly one `inverse_split` event, in the cycle labelled tick 6 (the
  cycle whose packets arrive at tick 7; the lamp's emission cycle is
  labelled 0), position (7,7,7),
  family `quanta`, the mode, `ports` (1,) and `amounts` (4,) in `siblings`
  and `straight` and () and () in `annul`, `amount` 4, `bit` 0, `restored`
  true, `annulled` {} in `siblings` and `straight` and {quanta: (4,),
  momentum: (4,0,0)} in `annul`; one `detector_return` at tick 3 and no
  click;
- (f) the runner on the same document records `inverse_split:
  "inverse-split-v1"` and `return_mode` beside `detector_return`,
  `annulled_totals` (quanta 4 and momentum (4,0,0) in `annul`, zero
  otherwise), `accounting_balanced_at_every_completed_tick` true in every
  mode and `conserved_at_every_completed_tick` true in every mode (since
  `ray-event-audit-v1`, 2026-09-17: the flag is the world ledger's identity,
  initial + sourced = current + escaped + annulled + absorbed, and the
  annulled sink is a ledger line, not a loss; the pin of the same day
  before feature 10 read false in `annul`, from the earlier flag that
  compared only what stayed in the world); a second run writes the same
  `events.jsonl` byte for byte; a document with `return_mode` `"none"` is
  rejected before a world exists.

Pinned consequences in existing tests: the returned ray of
`test_detector_return.py` (a one-line event, no sibling line) is restored
to its lamp in the cycle labelled 6: after tick 7 no ray is in the world and
the lamp holds 4 quanta and momentum -4u (recoil for 8, 4u back with the
restore); the lamp, a source that emits what it holds, then emits the 4
again as a new one-line event on the cycle after the restored record
reaches the field plan: after tick 8 the ray is one Link out with steps 1,
phase 1, `event_shares` 4 on Port p and no Detector bit, the lamp at 0
quanta and momentum -8u; totals and momentum unchanged; the four returned rays
of `test_detector_mark.py` are restored to their lamps in the cycle
labelled 2, the lamps holding their share again with its recoil undone from
tick 3 ([Node Detector bit](#node-detector-bit)), and that test runs three
ticks, because at the fourth the restored lamps would emit again into the
mark and draw again.
## Ray layers

`test_ray_layers.py` builds its board inline under the shared Detector
admission (schema 1, `link_ticks` 1, `metric: "links"`, pace 1/1, no decay,
the six unit-axial headings in Port order, closed under negation) on a
periodic 15^3 lattice: three ray families `a`, `b` and `c`, each its own
conserved scalar field with an 8-step phase advancing 1 per Link, and one
signed `momentum` vector ([layers](SPATIAL_FIELDS.md#layers-ray-layers-v1)).
Five lamps around the Node N = (7,7,7) each hold 5 of their family and emit
it once, funded, directed at N with recoil into `momentum`: `a` from (5,7,7)
along +X and from (9,7,7) along -X, `b` from (7,5,7) along +Y and from
(7,9,7) along -Y, `c` from (7,7,5) along +Z. Two rules are declared, both
guarded by equal amounts and opposite headings with energy and momentum
invariants: `a_swap`, two `a` rays exchange headings; `b_turn`, two `b` rays
turn by the cyclic axis permutation (x, y, z) to (z, x, y) and take phase 6.
No rule selects `c`. The test is parametrized over the declared rules: both,
or `a_swap` alone. Pinned before the first run:

- (a) the derived layers are ((0,), (1,), (2,)) by field index and (("a",),
  ("b",), ("c",)) by name in both worlds, since an unruled field is its own
  layer; a rule whose roles select `a` and `b` would give (("a", "b"),
  ("c",)), and a world with no rule gives one layer per field;
- (b) after tick 1 each lamp holds 0 of its family and the recoil of its ray
  ((-5,0,0), (5,0,0), (0,-5,0), (0,5,0), (0,0,-5)); after tick 2 N holds all
  five rays, two of `a` (headings 0 and 1, masks 1 and 2), two of `b`
  (headings 2 and 3, masks 4 and 8) and one of `c` (heading 4, mask 16),
  every one with steps 2, phase 2, `outbound` 1 and `detector` 0;
- (c) after tick 3, with both rules, N is empty and the six neighbors hold:
  at (6,7,7) one `a` ray, heading 1, phase 3, steps 1, `event_ports` 3,
  `event_shares` (5, 5, 0, 0, 0, 0); at (8,7,7) the same with heading 0; at
  (7,7,8) one `b` ray, heading 4, phase 7, steps 1, mask 48, shares
  (0, 0, 0, 0, 5, 5), beside the `c` ray, heading 4, phase 3, steps 3, mask
  16, shares (0, 0, 0, 0, 5, 0), unchanged from its emission; at (7,7,6) one
  `b` ray, heading 5, phase 7, steps 1, mask 48, shares (0, 0, 0, 0, 5, 5);
  nothing at (7,6,7) and (7,8,7): two events at one Node in one interval,
  and a third family crossing;
- (d) after tick 3 with `a_swap` alone, the `a` rays and the `c` ray are
  exactly as in (c), (7,7,8) holds the `c` ray only, and the `b` rays cross:
  at (7,8,7) heading 2, phase 3, steps 3, mask 4, shares (0, 0, 5, 0, 0, 0);
  at (7,6,7) heading 3, phase 3, steps 3, mask 8, shares (0, 0, 0, 5, 0, 0);
- (e) after tick 4, with both rules, (7,7,9) holds the `b` ray (heading 4,
  phase 0, steps 2) and the `c` ray (heading 4, phase 4, steps 4) on one
  line without meeting, and the `a` rays are at (5,7,7) and (9,7,7) with
  steps 2 and phase 4;
- (f) at every tick 1 to 4 the world holds exactly five rays; the totals are
  `a` 10, `b` 10, `c` 5 and `momentum` (0, 0, 0); the conservation report
  passes with energy 25 and momentum (0, 0, 0); the spatial accounting
  balances; the runner records `ray_layers: "ray-layers-v1"`,
  `ray_layer_families` [["a"], ["b"], ["c"]], `ray_state`
  "ray-event-state-v1", `conserved_at_every_completed_tick` true and final
  totals `a` [10], `b` [10], `c` [5].

Existing worlds keep their amounts, phases, totals, audits and charges: a
world whose rules select one layer meets the same owners in the same order.
## Ray viewer extraction

`test_ray_viewer.py` builds its board inline under the shared Detector
admission (schema 1, `link_ticks` 1, `metric: "links"`, pace 1/1, no decay,
the six unit-axial headings) on an open 5 x 3 x 3 board with an 8-step phase
advancing 1 per Link, runs it for six ticks through `run_initialization`
headless, and reads the record back with `tools/ray_viewer/extract.py`
([ray viewer](../tools/ray_viewer/README.md)), which never imports the
simulator. Lamp A at (1,1,1) holds 3 quanta and emits 3 through +X with phase
0; lamp B at (3,1,1) holds 3 and emits 3 through -X with phase 4; each
recoils into its own momentum. The one declared coupling, `swap_headings`,
typed to two `quanta` participants, fires when two rays with opposite
headings whose phases sum to 6 meet (1 and 5, what the lamps' phases are
after one Link), exchanges their headings and sets `delay` 1 on both; energy
6 and momentum (0,0,0) are its invariants. The phase condition is what makes
it fire once: a first draft conditioned on opposite headings alone stayed true
after the swap, re-fired every interval and held both rays at (2,1,1) for the
whole run, which is the engine's binding behavior (a rule that keeps setting
`delay` on its participants), not a defect. The Node (4,1,1) carries a
Detector mark with setting 1/1 and seed 0, so every arrival there draws 1.
Since 2026-09-17 (feature 7 merged) the world also declares `G`, the field of
`quanta` with `release` 1/3 and phase advance 0
([released field](SPATIAL_FIELDS.md#field-as-the-rays-information-released-field-v1)):
every Node a quanta ray crosses releases, in the interval it departs, one G
ray of amount floor(3/3) = 1 on each of the five other headings, booked as a
source, and a ray held at a Node by the coupling's `delay` is resident
content there and releases on all six headings every interval it is held
(Highlights 3.5, feature 8, `ray-binding-v1`). Pinned before the first run,
from the event stream alone (no per-tick recording, so no phase):

- (a) the rays: four, each of family `quanta` and amount 3. Ray 0 leaves
  (1,1,1) through +X at tick 0 and ray 1 leaves (3,1,1) through -X at tick
  0, one segment each with `steps` 1, both ending at tick 1 at (2,1,1) in
  the meeting; rays 2 and 3 start at (2,1,1) at tick 2 (the meeting's
  outputs, `delay` 1 held them one interval): the +X ray walks (2,1,1),
  (3,1,1), (4,1,1) and leaves the board through +X, the -X ray walks (2,1,1),
  (1,1,1), (0,1,1) and leaves through -X, three segments each with `steps`
  1, 2, 3 and `outbound` 1, escaped at tick 5;
- (b) the events, in board order: two emissions at tick 0 with one spoke
  each (+X at (1,1,1), -X at (3,1,1)); one meeting at tick 1 at (2,1,1) with
  inputs rays 0 and 1, outputs rays 2 and 3, spokes +X and -X, `output_tick`
  2, `held_ticks` 1, amount in `quanta` 6, momentum in (0,0,0), amount out
  6, momentum out (0,0,0), coupling `swap_headings`; one Detector PASS click
  at tick 4 at (4,1,1) through Port -X (family `quanta`, amount 3, bit 1)
  on the +X ray (the only click of family `quanta`; with `G` declared the
  marked Node clicks five times, see (e)); two escapes at tick 5, at (0,1,1)
  through -X and at (4,1,1) through +X; no crossing, split, deflection or
  return;
- (c) the captions: tick 0 names both emissions, tick 1 the meeting with the
  coupling and both invariants, tick 2 the outputs leaving, tick 4 the
  Detector PASS with its bit (and, with `G` declared, the G clicks of ticks
  3, 4 and 6 beside the field escapes, see (e)), tick 5 the escapes;
  `in_world` quanta stays 6
  through tick 4 and is 0 from tick 5, when `escaped` is 6; the run's
  conservation line reads `passed` (the world declares the `conservation`
  block again since `ray-event-audit-v1`, 2026-09-17: the local audit's
  residual momentum (1, 0, 0) at lamp A's Node in the tick-3 cycle, reported
  by the viewer as a suspected defect, was the momentum of the release the
  single held ray made there, five field rays whose net momentum is minus
  its own heading, booked as a source with no owner paying and unknown to
  the local audit; the audit now reads every release as a `sourced` line at
  its Node, [the world ledger](LOCAL_CONSERVATION.md#the-world-ledger-ray-event-audit-v1)),
  with `accounting_balanced_at_every_completed_tick` true and
  `conserved_at_every_completed_tick` true (since `ray-event-audit-v1`: the
  flag is the world ledger's identity and the 6 escaped quanta are its
  `escaped` line, not a loss; the pin of the same day before feature 10 read
  false, from the earlier flag that counted only what stayed in the world),
  and the extracted `conservation` carries the recorded `audit` ledger; the
  record carries `ray-event-state-v1`, `detector-mark-v1` and no unknown
  event kind;
- (d) tolerance: the same record with one appended event of an unknown kind
  (`field_release` at tick 3 at (2,1,1)) extracts to the same rays and
  events plus one generic marker of that kind at that Node and tick (drawn,
  not listed in the caption, which names only the kinds of the caption rule),
  and the record reports `{"field_release": 1}` as unknown;
- (e) the field (pinned 2026-09-17 before the first run with `G`, corrected
  after it, and corrected again on 2026-09-17 after #204, see below): the
  four quanta rays walk exactly as in (a), their trails unbroken through the
  Nodes where they release; six `release` events, each flagged `field`, each
  with the departing quanta rays as inputs and one G ray of amount 1 per
  spoke and per releasing ray as outputs: at (2,1,1) at tick 1 with six
  spokes, from the two rays held there by the coupling's `delay` (content
  held at a Node is resident and releases on all six headings, Highlights
  3.5, feature 8), so every spoke carries G 2 and the release sources G 12
  (the two held rays' G rays on one spoke leave in one packet, which the
  record holds as one `spatial_received` reading of G 2, so the extractor
  reads one G ray of amount 2 per spoke; the tick-1 release has no
  departing input); at (2,1,1) at tick 2 with six spokes, the departure
  release of both meeting outputs (each releases on the five headings other
  than its own, so the four shared transverse G rays carry 2 each and the
  +X and -X ones 1 each, G 10); at (3,1,1) and (1,1,1) at tick 3 with five
  spokes each (all but the ray's own +X, respectively -X; G 5 each), and at
  (4,1,1) and (0,1,1) at tick 4 likewise; 32 G rays in all, so 36 rays; no
  `split`, `crossing` or `deflection` event; the marked Node (4,1,1) draws
  for G too, once per ray in the arriving packet, so the clicks are five:
  tick 3 G 1 twice (the two +X G rays of the tick-1 release, one per held
  ray, both read against the one extracted G ray of amount 2), tick 4
  quanta 3 and tick 4 G 1 (the +X G of the tick-2 release, arriving with
  the quanta ray) and tick 6 G 1 (the +X G released at (1,1,1) at tick 3);
  field escapes, each flagged `field`: four at tick 3 (G 2 each, the
  transverse rays of tick 1, G 8), six at tick 4 (the two axial packets of
  tick 1, G 2 each, and the four transverse of tick 2, G 12), ten at tick 5
  (the eight transverse rays of tick 3 and the two riding out with the
  quanta rays, G 10) and eight at tick 6 (the transverse rays of tick 4, G
  8), G 38 in all; the run's `source_totals` G 42, `escaped_totals` G 38,
  `final_totals` G 4 (the four axial G rays still inside at tick 6), and the
  derived per-tick `in_world` G, initial plus the sources through the
  previous tick minus the escapes, is 0, 0, 12, 14, 12, 12, 4 for ticks 0 to
  6; captions never name a release and list at most three events, so tick 3
  reads the two G clicks and "field escaped: G 8", tick 4 the two Detector
  PASS lines and "field escaped: G 12", tick 5 "escaped: quanta 6" and
  "field escaped: G 10", tick 6 the G click and "field escaped: G 8";
  `record.released_field` is `released-field-v1`. The first pin had one
  release at (2,1,1), at tick 2 only, from the released-field text ("in the
  interval it departs"): the first run showed the engine also releasing at
  tick 1, while both rays were held at (2,1,1) by the coupling's `delay`
  (source G 40, not 30; a fourth click at tick 3). That difference between
  the text and the implementation for a retained ray was reported with this
  fixture as the reproduction and is settled by feature 8; this test pins
  what the record holds and what the extractor reads from it, not the
  release rule. Corrected 2026-09-17 after #204 (feature 8,
  `ray-binding-v1`): the pin of #205 was taken before #204 merged, with the
  tick-1 release on five headings per held ray (the shared transverse
  spokes G 2, the axial spokes G 1, G 10); content held at a Node releases
  on all six headings (Highlights 3.5, feature 8), so the tick-1 release
  sources G 12 (was 10) with G 2 on every spoke (the axial spokes were 1),
  the marked Node clicks twice at tick 3 (was once; five clicks, not four),
  the tick-4 field escapes carry G 12 (was 10), `source_totals` G 42 (was
  40), `escaped_totals` G 38 (was 36), `in_world` G 12 and 14 at ticks 2
  and 3 (was 10 and 12), and the tick-3 and tick-4 captions read as above
  (tick 3 named one G click, tick 4 ended "field escaped: G 10"); the
  tick-2 departure release, the tick-3 and tick-4 releases, the escape
  counts, the ray count and `final_totals` are unchanged;
- (g) external bodies (`external-body-v1`, pinned 2026-09-17 before the
  first run): a `run.json` listing one body of family `star`, amount 4096,
  coupling `sink`, field `G`, with `positions` rows (0, 7,7,7), (1, 7,7,7)
  and (2, 8,7,7), extracts to one body at (7,7,7) carrying those rows, so
  the page draws its picture (chosen by family in `style.json`, `star` by
  default) at (7,7,7) through tick 1 and at (8,7,7) from tick 2;
- (f) the style: `tools/ray_viewer/style.json` is a `ray-viewer-style-v1`
  object whose sections and keys are exactly the documented ones (the
  renderer's `validate_style` accepts it and rejects an unknown key), the
  page's built-in default equals it, and a style whose `ray_width_px` is 9
  reaches the inlined page's `style` block while the default one stays in
  its `style-default` block; its defaults (model owner, 2026-09-17) are
  `trail_links` 10 with `trail_fade` [0.35, 0.0] and `colors.trail`
  `#ffffff` (the ray bright at its Link in its family colour and a faint
  white wake fading to nothing over ten Links, one opacity per Link, no hard
  cut), `trail_width_px` 6, a small head (`ray_width_px` 3 over
  `head_links` 0.5, half a Link from the ray's Node along its heading) and
  `draw.momentum_arrow` true with `momentum_arrow_px_per_quantum` 1.75,
  `momentum_arrow_width_px` 1.5, `arrowhead_px` 5 and `colors.momentum_arrow`
  `#7fd7ff` (a tiny arrow at the head in the ray's heading, amount x 1.75 px
  long, 14 px for an electron of 8, carrying the arrowhead), a fixed matter
  colour with `hue_by_phase` on the arrowhead only, `draw.marker_shape`
  `sphere` with empty `shape_overrides` (sources, Detector marks, external
  bodies and ray heads as smooth spheres, a head of `head_radius_px` 4),
  `draw.glow`, `draw.vignette` and `draw.field_additive` true, every event
  marker shape but `escape` a `ring`, `lattice_alpha` 0.07, `colors.scene`
  `#0b1730` fading to `scene_edge` `#03060b`, `gif_supersample` 2,
  `camera_fit` `rays` with `camera_fit_margin_links` 1 (the camera and the
  lattice fit the box around every matter ray path, source, Detector mark and
  body over the run, padded by one Link; `board` fits the whole board), and
  fixed colours for the families `electron`, `light`, `proton` and `neutron`, of the `page_text` flags
  only `header` (the run's title) and `tick_counter` true, every `labels`
  flag false, and `autoplay` and `loop` true.

The runs document is `ray-viewer-runs-v1`. A GIF or page rendered from it is
a rendering of the fingerprinted record, not evidence by itself.

## Ray meetings with outputs

`test_ray_meeting_conversion.py` builds its board inline under the shared
Detector admission (schema 1, `link_ticks` 1, `metric: "links"`, pace 1/1,
no decay, the six unit-axial headings in Port order) on a periodic 15^3
lattice: one ray family `a`, a conserved scalar with an 8-step phase
advancing 1 per Link, and one signed `momentum` vector
([meetings with outputs](SPATIAL_FIELDS.md#meetings-with-outputs-ray-meeting-conversion-v1)).
Two lamps each hold 5 of `a` and emit it once, funded, directed at
N = (7,7,7) with recoil into `momentum`: lamp 0 from (5,7,7) along +X at
phase 0, lamp 1 from (9,7,7) along -X at the emission phase d of the case.
One rule is declared, guarded by equal amounts and opposite headings, with
per-ray readout invariants summed over inputs and outputs. The test is
parametrized over the cases `four` (d = 0), `table_0`, `table_4`, `table_2`,
`table_1` (d = 0, 4, 2, 1) and `broken`. Pinned before the first run:

- at ticks 1 and 2 the world holds two rays; after tick 2 both are at N:
  heading 0, phase 2, mask 1, shares (5, 0, 0, 0, 0, 0) and heading 1, phase
  (2 + d) mod 8, mask 2, shares (0, 5, 0, 0, 0, 0), both steps 2, amount 5,
  `outbound` 1, `detector` 0; after tick 1 the lamps hold 0 of `a` and the
  recoils (-5, 0, 0) and (5, 0, 0);
- (a) `four`: the rule's outputs are four rays of `a` on Ports 2, 3, 4 and 5
  with amounts 2, 2, 3 and 3 and phases "same" (input 0), input 1, offset 3
  from input 0 and input 1 plus 7, invariants energy (`amount`) and
  momentum (`amount x heading`). Applied to the two residents, the meeting
  returns one bundle of exactly these four rays, in declared order, each
  with steps 0, `outbound` 1, `detector` 0, accumulators (0, 0, 0), mask 60
  (0b111100) and shares (0, 0, 2, 2, 3, 3): heading 2 amount 2 phase 2,
  heading 3 amount 2 phase 2, heading 4 amount 3 phase 5, heading 5 amount
  3 phase 1. After tick 3 N is empty, (6,7,7) and (8,7,7) are empty, and
  the four neighbors hold one ray each with steps 1: (7,8,7) heading 2
  amount 2 phase 3, (7,6,7) heading 3 amount 2 phase 3, (7,7,8) heading 4
  amount 3 phase 6, (7,7,6) heading 5 amount 3 phase 2; after tick 4, with
  steps 2, (7,9,7) phase 4, (7,5,7) phase 4, (7,7,9) phase 7, (7,7,5) phase
  3. The world holds four rays at ticks 3 and 4;
- (b) `table_d`: output 0 on Port 2 takes the sum of the inputs split by the
  table [8, 7, 4, 1, 0, 1, 4, 7] at the phase difference d of inputs 0 and
  1, output 1 on Port 3 takes the rest and owns the remainder, invariant
  energy. The shared content is 10. Applied to the residents the meeting
  returns: d = 0, one ray, heading 2 amount 10 phase 2, mask 4, shares
  (0, 0, 10, 0, 0, 0); d = 4, one ray, heading 3 amount 10 phase 6, mask 8,
  shares (0, 0, 0, 10, 0, 0); d = 2, heading 2 amount 5 phase 2 and heading
  3 amount 5 phase 4, mask 12, shares (0, 0, 5, 5, 0, 0); d = 1, 10 x 7 / 8
  is 8 whole quanta with 6/8 left and 10 x 1 / 8 is 1 with 2/8 left, so the
  rest output owns the quantum the two floors leave: heading 2 amount 8
  phase 2 and heading 3 amount 2 phase 3, mask 12, shares (0, 0, 8, 2, 0, 0).
  An output of amount 0 is no ray and no Port. After tick 3 N, (6,7,7) and
  (8,7,7) are empty and the products are at (7,8,7) (phase 3) and (7,6,7)
  (phase (3 + d) mod 8) with steps 1, at (7,9,7) and (7,5,7) after tick 4
  with steps 2 and phases 4 and (4 + d) mod 8; the world holds one ray at
  ticks 3 and 4 for d = 0 and d = 4, two rays for d = 2 and d = 1. A split
  between two Ports moves ray momentum whose owner, the recoil of the field
  ray, is feature 7; the move is booked as an explicitly accounted source
  of `momentum` (Highlights 3.15): after ticks 3 and 4 the `momentum` total
  and the `momentum` source total are both (0, 10, 0) for d = 0,
  (0, -10, 0) for d = 4, (0, 0, 0) for d = 2 and (0, 6, 0) for d = 1, and
  (0, 0, 0) at ticks 1 and 2. The table worlds declare no local
  energy/momentum audit (its per-Node residual read no source term until
  `ray-event-audit-v1`, which reads every release as a source) and
  their conservation report reads `not_configured`; the `four` world
  declares it and its meeting keeps the rays' momentum at (0, 0, 0);
- in every case, at every tick 1 to 4, the `a` total is 10 with source 0,
  the spatial accounting balances, in `four` the totals and sources of
  `momentum` are (0, 0, 0) and the conservation report passes with energy
  10 and momentum (0, 0, 0), and the runner records `ray_meeting:
  "ray-meeting-conversion-v1"` beside `ray_state` "ray-event-state-v1" and
  `ray_layers` "ray-layers-v1", with `conserved_at_every_completed_tick`
  true, final totals `a` [10] and `momentum` as above, and the same
  `momentum` in `source_totals`;
- (c) `broken`: the `four` rule with amounts 2, 2, 3 and 4 (11 out of 10 in)
  is rejected by the meeting ("violates conservation of amount") both when
  applied to the residents directly and at tick 3 of the run, before any
  owner changes; the `four` rule with amounts 2, 2, 3, 3 on Ports 2, 2, 4, 5
  (momentum (0, 4, 0) out of (0, 0, 0) in) is rejected for its momentum
  invariant; at initialization a table of 7 entries under 8 phase steps
  ([7, 4, 1, 0, 1, 4, 7]), a `rest_of` naming an output without a table,
  and a heading Port 6 are rejected before any run.

Existing worlds with the single-output rules are byte-identical: the suite
is the regression.

## Released field

`test_released_field.py` builds its boards inline under the shared Detector
admission (schema 1, `link_ticks` 1, `metric: "links"`, pace 1/1, no decay,
the six unit-axial headings in Port order) on a periodic 15^3 lattice
([released field](SPATIAL_FIELDS.md#field-as-the-rays-information-released-field-v1)).
The family `electron` is a conserved scalar with an 8-step phase advancing 1
per Link; `G` is its field, `field_of: "electron"` with `release: [1, 4]`,
an 8-step phase advancing 0 (a field ray delivers its emitter's phase
unchanged). Every lamp holds 5 of its family and emits it once, funded and
directed, at phase 0. The test is parametrized over `straight`, `meeting`
and `rejected`. Pinned before the first run:

- (a) `straight`: one lamp at (5,7,7) emits the electron along +X. After
  tick t (1 to 5) the electron is at (5+t,7,7) with heading 0, amount 5,
  phase t, steps t, mask 1 and shares (5, 0, 0, 0, 0, 0): unchanged by its
  field. In the interval of tick t (t from 2) it departs (4+t,7,7) and
  releases five G rays there, one per Port heading except its own +X, each
  of amount floor(5 x 1 / 4) = 1 (the fraction is not released), phase
  t - 1 (the electron's phase at the release), steps 0, mask 0 and shares
  all zero; after tick t they are at (3+t,7,7) heading 1, (4+t,8,7)
  heading 2, (4+t,6,7) heading 3, (4+t,7,8) heading 4 and (4+t,7,6)
  heading 5, each with steps 1, and every earlier release has walked one
  more Link along its heading. `release_field` applied to the electron's
  ray returns exactly these five rays. The G total and the G source total
  after tick t are both 5 (t - 1): 0, 5, 10, 15, 20; the electron total is
  5 with source 0; the lamp holds 0 after tick 1 and, holding nothing,
  releases nothing. At every tick no Node holds the electron and a G ray
  together: the released rays leave away from the line or behind, and the
  ray's own line ahead of it is the ray itself. The spatial accounting
  balances at every tick;
- (b) `meeting`: lamp 0 at (5,7,7) emits an electron along +X, lamp 1 at
  (8,8,7) an electron along -X on the parallel line one Node above, and a
  lamp of the uncoupled family `c` at (6,7,10), holding and emitting 3, a
  `c` ray along -Z. The G field has 16 ray slots. One
  rule `turn` is declared, `electron x G` without a guard, with outputs
  the electron on the G ray's heading (`"same"` of input 1, amount of input
  0, phase of input 0) and the G ray reversed (`"reversed"` of input 1,
  amount of input 1), invariant energy. After tick 2 the electrons are at
  (7,7,7) (heading 0, phase 2, steps 2) and (6,8,7) (heading 1, phase 2,
  steps 2), the `c` ray at (6,7,8) (heading 5, phase 2, steps 2, amount 3)
  beside a G ray of heading 4, and the ten G rays released in the interval
  of tick 2 (amount 1, phase 1, steps 1, mask 0) are at (5,7,7) heading 1,
  (6,8,7) heading 2, (6,6,7) heading 3, (6,7,8) heading 4, (6,7,6) heading
  5, (8,8,7) heading 0, (7,9,7) heading 2, (7,7,7) heading 3, (7,8,8)
  heading 4 and (7,8,6) heading 5; no electron has turned. The first
  meetings are at tick 3, at (7,7,7) and at (6,8,7). Applied to the
  residents of (7,7,7) the meeting returns the electron on heading 3,
  amount 5, phase 2 and the G ray on heading 2, amount 1, phase 1, both
  steps 0, mask 12 and shares (0, 0, 1, 5, 0, 0): the electron is turned
  away from the source line y = 8, toward -Y. At (6,8,7) it returns the
  electron on heading 2, amount 5, phase 2 and the G ray on heading 3,
  amount 1, phase 1, mask 12, shares (0, 0, 5, 1, 0, 0): turned toward +Y,
  away from y = 7. After tick 3 the turned electrons are at (7,6,7)
  (heading 3, phase 3, steps 1, mask 12, shares (0, 0, 1, 5, 0, 0)) and
  (6,9,7) (heading 2, phase 3, steps 1, mask 12, shares (0, 0, 5, 1, 0, 0));
  the recoils walk back: the reversed G ray of (7,7,7) is at (7,8,7)
  (heading 2, amount 1, phase 1, steps 1, mask 12, shares (0, 0, 1, 5, 0,
  0)) and after tick 4 at (7,9,7) with steps 2; the reversed G ray of
  (6,8,7) is at (6,7,7) (heading 3, phase 1, steps 1, mask 12, shares
  (0, 0, 5, 1, 0, 0)) and after tick 4 at (6,6,7) with steps 2. The turned
  electrons release at the meeting Node in the same interval, on every
  heading but their new one (phase 2): from (7,7,7) to (8,7,7), (6,7,7),
  (7,8,7), (7,7,8), (7,7,6) and from (6,8,7) to (7,8,7), (5,8,7), (6,7,7),
  (6,8,8), (6,8,6), each amount 1, steps 1 after tick 3;
- (c) after tick 3 the `c` ray is at (6,7,7) (heading 5, phase 3, steps 3,
  amount 3) with three G rays: the reversed one above, and the released
  rays of heading 1 and heading 3 with phase 2 and mask 0. After tick 4 it
  is at (6,7,6) with heading 5, phase 4, steps 4, amount 3, mask 32 and
  shares (0, 0, 0, 0, 0, 3): a family with no coupling to G crosses it,
  as it crossed the G ray at (6,7,8) after tick 2;
- in `meeting` the totals after ticks 1 to 4 are `electron` 10, `c` 3 and
  `G` 0, 10, 20, 30, with `source_totals` `electron` 0, `c` 0 and `G` the
  same 0, 10, 20, 30 (ten rays released per interval from tick 2: five per
  electron); the spatial accounting balances; the derived layers are
  (("G", "electron"), ("c",)); the runner records `released_field:
  "released-field-v1"` and `released_fields` `[{"field": "G", "field_of":
  "electron", "release": [1, 4]}]` beside `ray_meeting`, with
  `conserved_at_every_completed_tick` true, final totals `electron` [10],
  `G` [30], `c` [3] and `source_totals` `G` [30];
- (d) `rejected`, at initialization: `field_of` without `release` ("declares
  field_of and release together"), `release` [5, 4] ("must not exceed the
  source's amount"), a `field_of` naming the field itself ("not its own
  field"), a field of a field ("a field has no field"), a G field without
  the -Z heading ("six Port headings") and a G field with 4 phase steps
  under an 8-step source ("its source's phase steps").

A world that declares no `field_of` runs byte-identically: the suite is the
regression, and its run record carries `released_fields: []`.

## External body

`test_external_body.py` builds its boards inline under the shared Detector
admission (schema 1, `link_ticks` 1, `metric: "links"`, pace 1/1, no decay,
the six unit-axial headings in Port order) on a periodic 15^3 lattice
([external body](SPATIAL_FIELDS.md#the-external-body-external-body-v1)). The
family `star` is a conserved scalar with an 8-step phase advancing 0 and
`G`, where declared, is its field, `field_of: "star"`; `light` advances 0 and
`electron` 1 per Link; every lamp holds its amount and emits it once, funded
and directed, at phase 0. A tick n is one `step()`: the cycle of interval
n - 1 (release, meetings, accumulators, departures) and the delivery of tick
n (arrivals, the sink). The test is parametrized over `sink`, `stars`,
`uniform`, `mirror` and `rejected`. Pinned before the first run:

- (a) `sink`: a star at (7,7,7) of amount 4096 at rest, momentum table
  `{"G": -1}`, `G` released at `[1, 2048]`: floor(4096 x 1 / 2048) = 2 per
  heading, six headings, 12 per tick, booked as a source. A light lamp at
  (8,5,7) emits 5 along +Y, an electron lamp at (7,7,4) emits 3 along +Z;
  the rule `turn`, light x G with outputs the light on the G ray's heading
  and the G ray reversed. After tick n the released G ray of heading h at
  distance d (1 to n) from the star is at the star plus d x h with amount 2,
  phase 0, steps d, no event; the light is at (8, 5+n, 7) after ticks 1 and
  2 with heading 2, steps n, mask 4 and shares (0, 0, 5, 0, 0, 0). In the
  interval of tick 3 the light meets the +X ray released in the interval of
  tick 2 at (8,7,7): the light leaves on +X (heading 0, mask 3, shares (5,
  2, 0, 0, 0, 0), steps n - 2 after tick n, at (6+n, 7, 7)) and the G ray
  returns reversed, arrives at the star at tick 3 and ends in its sink:
  sink G 2, momentum (2, 0, 0) (-1 x 2 x (-1, 0, 0), toward the light), so
  the +X ray at distance n - 1 is missing from tick 3 on. The electron
  arrives at the star at tick 3 and ends in the sink: sink electron 3, no
  momentum (the table does not name it). Totals after tick n: G 12n minus
  2 from tick 3, electron 3 then 0 from tick 3, light 5; source G 12n;
  `external_body_totals` G 2 and electron 3 from tick 3; the body at (7,7,7)
  throughout with accumulators (2(n - 3), 0, 0) from tick 3 (2 per interval
  over 4096: no Link); the bodies' momentum line (2, 0, 0) from tick 3;
  two `external_body_absorbed` records at tick 3 and no step. The runner
  writes `external_body: "external-body-v1"`, `external_body_totals` G [2]
  and electron [3], `external_body_momentum` [2, 0, 0], final totals G 70,
  and the body's positions [[t, 7, 7, 7] for t = 0..6], final momentum
  [2, 0, 0] and accumulators [6, 0, 0];
- (b) `stars`: three stars, `G` released at `[1, 8]`, no lamps and no rule.
  Star 0 at (4,7,7) and star 1 at (10,7,7), amount 16 (2 per heading, 12
  per tick), at rest; star 2 at (7,7,2), amount 8 (1 per heading), initial
  momentum heading +X at pace 1/4, momentum (2, 0, 0); every table
  `{"G": -1}`. Star 2's accumulator x after tick n is 2n mod 8: 2, 4, 6, 0,
  2, 4, 6, 0; it steps +X in the intervals of ticks 4 and 8 (`external_body_step`
  at ticks 3 and 7, Port 0) and is at (7,7,2) through tick 3, (8,7,2)
  through tick 7 and (9,7,2) at tick 8; in a stepping interval it releases
  five rays, not the +X one (its own line ahead). Star 0's +X ray and star
  1's -X ray of the first interval arrive at the other star at tick 6, and
  one more each tick: from tick 6 each sink holds 2(n - 5), star 0's
  momentum is (2(n - 5), 0, 0) and star 1's the opposite; accumulators
  after ticks 6, 7 and 8: 0, 2, 6 for star 0 and 0, -2, -6 for star 1 (no
  Link over 16). Source G after tick n: 30n - [n >= 4] - [n >= 8], that is
  30, 60, 90, 119, 149, 179, 209, 238; absorbed 4(n - 5) from tick 6: 4, 8,
  12; current G: 30, 60, 90, 119, 149, 175, 201, 226. The bodies' momentum
  line is (2, 0, 0) at every tick and the rays' momentum, amount x heading
  summed over every G ray, is (-[n >= 4] - [n >= 8], 0, 0), the momentum
  of the releases (the two skipped +X rays) less that of the absorbed rays
  (equal and opposite): exact at every tick. No star's Node holds a G ray
  after any tick;
- (c) `uniform`: a body at (3,7,7) of amount 6, no field declared, initial
  momentum heading +Y at pace 1/2: momentum (0, 3, 0). Accumulator y after
  tick n: 3, 0, 3, 0, 3, 0; steps in the intervals of ticks 2, 4 and 6
  (`external_body_step` at ticks 1, 3 and 5, Port 2, arrival ticks 2, 4 and
  6); position (3, 7 + floor(n / 2), 7); totals and sources 0;
- (d) `mirror`: a body at (7,7,7) of amount 4, family `star` with no field,
  coupling `mirror`, light x star with outputs the light reversed on its own
  line and the star returned unchanged; a light lamp at (7,7,3) emits 5
  along +Z. After ticks 1 to 4 the light is at (7,7,3+n) with heading 4,
  steps n, mask 16 and shares (0, 0, 0, 0, 5, 0), at tick 4 resident at the
  body's Node; in the interval of tick 5 the rule fires and the light
  leaves on -Z (heading 5), amount 5, phase 0, steps n - 4 at (7, 7, 11 - n)
  after tick n, a new event whose record counts the body's token as one
  quantum on +X: mask 33 and shares (1, 0, 0, 0, 0, 5). The body is
  unchanged at every tick (momentum 0, sink empty), no `star` ray exists at
  any Node, light stays 5 with source 0 and nothing absorbed;
- (e) `rejected`: amount 0, a family that is a field (`G`), a coupling
  that names no declared rule, a momentum-table sign 2, two bodies at one
  Node, a coupling naming a rule in which no role is the body, and a pace
  above one Link per interval are each rejected at initialization.

A world without `external_bodies` is unchanged: no body Node exists, no
token is added, no source is booked and the sink line is zero.

## Field spreading

`test_field_spreading.py` builds its boards inline under the shared Detector
admission (schema 1, `link_ticks` 1, `metric: "links"`, pace 1/1, no decay,
the six unit-axial headings in Port order) on an open 13^3 lattice
([field spreading](SPATIAL_FIELDS.md#field-spreading-field-spreading-v1)).
The family `light` is a conserved scalar with an 8-step phase advancing 0
and the table `spread: [6, 1, 1, 1, 1, 1]`, total 11: forward 6/11, backward
1/11, each transverse 1/11. Every lamp holds its amount and emits it once,
funded and directed, with its recoil into the lamp's `momentum` field, so
the `momentum` total is the lamps' recoils plus the rays' amount x heading
and the `momentum` source is what the spreads moved. At eight phase steps
and total 11 the remainder entry the phase selects is: phases 0 to 4
forward, 5 backward, 6 the second transverse (-Y for content on +X or -X,
-X for content on any other heading), 7 the third transverse (+Z for
content on +X, -X, +Y or -Y, +Y for content on +Z or -Z);
`spread_remainder_entry` over phases 0 to 7 returns 0, 0, 0, 0, 0, 1, 3, 4,
and `relative_ports` gives (0, 1, 2, 3, 4, 5) for Port 0 and (3, 2, 0, 1, 4, 5)
for Port 3. The test is parametrized over `single`, `superposition`,
`cancelled`, `quantum`, `sign`, `returned`, `source`, `resident`, `rejected`
and `unchanged`. Pinned before the first run:

- (a) `single`: a lamp at (5,7,7) emits 12 along +X at phase 6, four ticks.
  After tick 1 the ray is at (6,7,7) (heading 0, amount 12, phase 6, steps
  1, mask 1, shares (12, 0, 0, 0, 0, 0)). The spread at (6,7,7) in the
  interval of tick 2 (the `field_spread` record of tick 1): floor(12 x 6 /
  11) = 6 forward, floor(12 / 11) = 1 on each of the other five, the
  remainder 1 through -Y: `arrived` (12, 0, 0, 0, 0, 0), `amounts` per Port
  (6, 1, 1, 2, 1, 1), `remainders` (0, 0, 0, 1, 0, 0), `phase` 6,
  `coherence` [1, 1], `amount` 12. After tick 2 the rays, as (position,
  heading, amount), are (7,7,7) 0 6; (5,7,7) 1 1; (6,8,7) 2 1; (6,6,7) 3 2;
  (6,7,8) 4 1; (6,7,6) 5 1, each phase 6, steps 1, no event, and no other
  Node holds light. In the interval of tick 3 every one spreads again (six
  records of tick 2, in position order): (5,7,7) arrived (0, 1, 0, 0, 0, 0)
  gives (0, 0, 0, 1, 0, 0), the remainder; (6,6,7) arrived (0, 0, 0, 2, 0,
  0) gives (0, 1, 0, 1, 0, 0), 1 forward and the remainder 1 through -X;
  (6,7,6), (6,7,8) and (6,8,7), each arrived 1, give (0, 1, 0, 0, 0, 0), the
  remainder through -X; (7,7,7) arrived (6, 0, 0, 0, 0, 0) gives (3, 0, 0,
  3, 0, 0), 3 forward and the remainder 3 through -Y. After tick 3: (8,7,7)
  0 3; (7,6,7) 3 3; (5,6,7) 1 1 and 3 1; (5,8,7) 1 1; (6,5,7) 3 1; (5,7,8)
  1 1; (5,7,6) 1 1. The seven records of tick 3: (5,6,7) arrived (0, 1, 0,
  1, 0, 0), amount 2, phase 6, gives (0, 1, 0, 1, 0, 0), both remainders;
  (5,7,6), (5,7,8) and (5,8,7) arrived (0, 1, 0, 0, 0, 0) give (0, 0, 0, 1,
  0, 0); (6,5,7) arrived (0, 0, 0, 1, 0, 0) gives (0, 1, 0, 0, 0, 0);
  (7,6,7) arrived (0, 0, 0, 3, 0, 0) gives (0, 2, 0, 1, 0, 0), remainders
  (0, 2, 0, 0, 0, 0); (8,7,7) arrived (3, 0, 0, 0, 0, 0) gives (1, 0, 0, 2,
  0, 0), remainders (0, 0, 0, 2, 0, 0). After tick 4: (9,7,7) 0 1; (8,6,7)
  3 2; (7,5,7) 3 1; (6,6,7) 1 2; (4,6,7) 1 1; (5,5,7) 1 1 and 3 1; (5,7,7)
  3 1; (5,6,8) 3 1; (5,6,6) 3 1. The light total is 12 at every tick with
  source 0; the rays' momentum after ticks 1 to 4 is (12, 0, 0), (5, -1, 0),
  (-1, -5, 0), (-3, -7, 0) and the lamp's recoil (-12, 0, 0), so the
  `momentum` total is (0, 0, 0), (-7, -1, 0), (-13, -5, 0), (-15, -7, 0)
  and equals `source_totals` at every tick; the spatial accounting balances
  and the local audit passes. The runner records `field_spreading:
  "field-spreading-v1"`, `spreading_fields` `[{"field": "light", "spread":
  [6, 1, 1, 1, 1, 1]}]`, fourteen `field_spread` records (ticks 1 to 3),
  `conserved_at_every_completed_tick` true, `local_conservation` passed,
  final totals `light` [12] and `momentum` [-15, -7, 0], `source_totals`
  `light` [0] and `momentum` [-15, -7, 0];
- (b) `superposition` and `cancelled`: lamp 0 at (5,7,7) emits 23 along +X
  at phase 0 and lamp 1 at (7,7,7) emits 23 along -X at phase 6
  (`superposition`) or 4 (`cancelled`), two ticks. Both rays arrive at
  (6,7,7) at tick 1, where the coherent stock a reader sees
  (`spatial_values`) is 23 (coherence 1/2) or 0 (coherence 0/1). The spread
  in the interval of tick 2 combines them: `amount` 46, `arrived` (23, 23,
  0, 0, 0, 0), the phase of the coherent sum 7 (`superposition`) or 0
  (`cancelled`, a cancelled sum); each heading's 23 gives floor(23 x 6 / 11)
  = 12 forward and floor(23 / 11) = 2 on each other heading, the remainder
  1 through the third transverse, +Z, at phase 7 or forward at phase 0:
  `amounts` (14, 14, 4, 4, 6, 4) with `remainders` (0, 0, 0, 0, 2, 0), or
  (15, 15, 4, 4, 4, 4) with (1, 1, 0, 0, 0, 0). After tick 2 the rays are
  at (7,7,7) heading 0, (5,7,7) heading 1, (6,8,7) heading 2, (6,6,7)
  heading 3, (6,7,8) heading 4 and (6,7,6) heading 5 with those amounts,
  the combined phase, steps 1 and no event; the light total is 46, and the
  `momentum` total, the lamps' recoils cancelling, equals the source:
  (0, 0, 2) in `superposition`, (0, 0, 0) in `cancelled`;
- (c) `quantum`: a lamp at (5,7,7) emits 1 along +X at phase 7, six ticks.
  The quantum never waits: after tick 1 at (6,7,7) heading 0, and then, its
  remainder leaving through the third transverse relative to its heading at
  every Node, after ticks 2 to 6 at (6,7,8) heading 4, (6,8,8) heading 2,
  (6,8,9) heading 4, (6,9,9) heading 2 and (6,9,10) heading 4, amount 1,
  phase 7 and steps 1 throughout, one Link per interval and alone on the
  board; the `momentum` total and source after ticks 1 to 6 are (0, 0, 0),
  (-1, 0, 1), (-1, 1, 0), (-1, 0, 1), (-1, 1, 0), (-1, 0, 1), the lamp's
  recoil (-1, 0, 0) included in the total;
- (f) `sign`: an electron lamp at (5,7,7) (family `electron`, charge -3,
  rest rate 1) emits 4 along +X at phase 0; `light` is its field at
  `release: [1, 4]` with the table; three ticks. The electron is at (8,7,7)
  after tick 3 (heading 0, amount 4, phase 3, steps 3, mask 1). It releases
  five light rays of 1 at (6,7,7) in the interval of tick 2 (phase 1) and at
  (7,7,7) in the interval of tick 3 (phase 2), every one with `source_sign`
  -1, the sign of the electron's charge; phases 1 and 2 select forward, so
  after tick 3 they are at (4,7,7) heading 1, (6,9,7) 2, (6,5,7) 3, (6,7,9)
  4, (6,7,5) 5 (phase 1) and (6,7,7) 1, (7,8,7) 2, (7,6,7) 3, (7,7,8) 4,
  (7,7,6) 5 (phase 2), amount 1, steps 1, sign -1, and nothing else holds
  light; the five `field_spread` records of tick 2 carry `signs` (-1,);
  light 10 with source 10, electron 4 with source 0. `release_field` on the
  electron's ray gives the five rays with sign -1; `merge_rays` keeps a ray
  of sign 1 and one of sign -1 on one line as two rays; `spread_content`
  over 3 of sign 1 and 3 of sign -1 arriving on +X at phase 0 gives two
  departures on Port 0 of 3 each (1 by the table and 2 as the remainder,
  per sign), sign -1 first, and a record with `arrived` (6, 0, 0, 0, 0, 0),
  `amounts` (6, 0, 0, 0, 0, 0), `remainders` (4, 0, 0, 0, 0, 0) and `signs`
  (-1, 1); `transmit` in `siblings` mode of a returned ray of sign -1 on -X
  (mask 3, shares (2, 2, 0, 0, 0, 0), amount 2) gives one transmission of 2
  on -X with sign -1;
- (g) `returned` (the orchestrator's proposal of Highlights 5.5, pending the
  model owner's decision): the lamp world with a lamp at (5,7,7) emitting 1
  along +X at phase 0 and a Detector at (8,7,7) with setting 0/1 (every
  draw 0), seven ticks. After tick 1 the quantum is at (6,7,7) (emitted,
  mask 1); after tick 2 at (7,7,7), a spread departure with no event (the
  spreads of ticks 1 and 2 send it forward); at tick 3 it arrives at the
  Detector and is returned: at (8,7,7) heading 1, outbound 0, steps 1,
  Detector bit 0; after tick 4 at (7,7,7) with steps 0, the Node that spread
  it, where it neither rests nor performs an inverse split; after tick 5 at
  (6,7,7) and after tick 6 at (5,7,7), steps 0 throughout; in the cycle of
  tick 6 the lamp, the record that emitted the family, takes it back: after
  tick 7 no light ray is on the board and the lamp holds light 1 and
  momentum (0, 0, 0). The light total is 1 and the `momentum` total
  (0, 0, 0) at every tick, both sources 0; the records are `field_spread`
  at ticks 1 and 2, `detector_return` at tick 3 and `field_returned` at
  tick 6 (position (5,7,7), family light, amount 1, port 1, by none,
  restored true); the local audit passes and the runner's ledger is exact
  with final totals light [1] and momentum [0, 0, 0];
- (h) `source` (the same proposal): a record holding 4 electrons at (5,7,7)
  with no emission (its Node cycles for the release, (i)), `light` its field at
  `release: [1, 4]` with the table, the Detector at (8,7,7) with setting
  0/1, eight ticks. Every interval the record releases six light quanta (1
  per heading, phase 0, sign -1), which go straight (phase 0 selects
  forward). On the +X line the quantum released in the cycle of tick k
  reaches the Detector at tick k+3, is returned, and walks back to (5,7,7)
  at tick k+6, where the cycle of tick k+6 ends it at the record, content of
  the family the field is the field of, its release unbooked as a negative
  source (`field_returned` of tick k+6, port 1, by `electron`, restored
  false). The -X, +Y and +Z quanta escape at tick k+6, the -Y and -Z quanta
  at tick k+8. After tick t the light total is 6t - 3 max(0, t-5) - 2 max(0,
  t-7) - max(0, t-6), the source 6t - max(0, t-6) and the escaped 3 max(0,
  t-5) + 2 max(0, t-7): after tick 8 the total is 35, the source 46 and 11
  escaped, the ledger balanced at every tick. The +X line after tick 8 holds
  at (5,7,7) a returning quantum with steps 0, at (6,7,7) an outbound
  quantum (steps 1) and a returning one (steps 0), at (7,7,7) the same, and
  at (8,7,7) a returning quantum with steps 1, every one of sign -1;
  `detector_return` records at ticks 3 to 8, `field_returned` at ticks 6 and
  7; the local audit passes;
- (i) `resident` (a defect fixed on 2026-09-17: a record holding stock of a
  family with a released field released nothing, because the Node's cycle
  returned early as idle before the release; `plan_cycle` now cycles for
  it): a record holding 8 electrons at (5,7,7) with no emission, `light` its
  field at `release: [1, 4]` with the table, four ticks. Every interval the
  record releases six light rays of floor(8 x 1 / 4) = 2, phase 0, sign -1,
  booked as a source, twelve per interval; each spreads whole forward at
  the next Node (2 gives 1 by the table and the remainder 1 at phase 0).
  After tick t the light total and source are 12t, the electron total 8
  with source 0 and the record unchanged; the rays are at distance 1 to t
  from (5,7,7) on each of the six lines, one ray of 2 per Node, phase 0,
  steps 1, sign -1, no event; the ledger is balanced at every tick and the
  local audit passes;
- (d) `rejected`, at initialization: a table of five entries and a negative
  weight ("spread"), a zero backward weight `[6, 0, 1, 1, 1, 1]` ("backward
  heading"), unequal transverse weights `[6, 1, 1, 1, 1, 2]` ("one weight"),
  `spread` on an outward field ("require ray transport"), a spreading family
  with `phase_bits` 13 ("twelve bits") and a spreading family without the -Z
  heading ("six Port headings");
- (e) `unchanged`: the released-field world of feature 7 without `spread`, an
  electron lamp at (2,3,3) emitting 5 along +X with `G` its field at
  `release: [1, 4]` and 16 slots, on an open 9 x 7 x 7 lattice for 6 ticks,
  runs byte-identically: the sha256 of its `events.jsonl` is
  `8ab9901a4e5c2da7b4571e7438e674e528050c5fb61e894fbb7d18703adb8fa5` and of
  its `state.json` `c13cd23158e5e461f171a8e2241ff793a24ccea531bd25ef54b28cfb2623e560`,
  both taken on main `f3809be` before this feature (final totals `G` 16 and
  `electron` 5, `G` 9 escaped), and its run record carries no
  `field_spreading` key.

## Ray-event audit

`test_ray_event_audit.py` builds its board inline under the shared Detector
admission (schema 1, `link_ticks` 1, `metric: "links"`, pace 1/1, no decay,
the six unit-axial headings in Port order, closed under negation) on an open
9 x 5 x 5 lattice, one world per `return_mode` (`annul`, `siblings`) and a
third, `body`, in `annul` with one external body, nine ticks
([audits](SPATIAL_FIELDS.md#audits-ray-event-audit-v1), [the world
ledger](LOCAL_CONSERVATION.md#the-world-ledger-ray-event-audit-v1)). The
charged pair lamp stands at X = (4,2,2) holding 1 quantum of `plus` (charge
+1) and 1 of `minus` (charge -1), and emits them once at tick 0 as two
funded one-line events recoiling into its `momentum`: the plus arm on +X
(u = (1,0,0)) and the minus arm on -X. The Node M = (7,2,2) on the plus arm
carries the one mark, setting `[1, 2]` and seed 3 (one draw: state 144814,
bit 0, as in [Detector return](#detector-return)). The electron lamp stands
at the corner E = (0,4,0) holding 4 quanta of `electron` (charge 0), emitted
once at tick 0 on +Z, funded, recoiling into the same `momentum`; the family
`G` (charge 0) is the field of `electron` with release `[1, 4]`, so every
crossing releases five G rays of amount 1, one per Port heading but +Z. Every
family has an 8-step phase with rest rate 0 and emission phase 0. Pinned
before the first run:

- (a) before the first tick `charge_totals()` reads `plus` 1, `minus` -1,
  `electron` 0 and `G` 0 (the stock a record holds of a charged family
  counts, as its amount counts in `totals()`), `escaped_charge_totals()`
  zero for every family, and the ledger at tick 0 has every line's current
  equal to its initial: `plus` (1), `minus` (1), `electron` (4), `G` (0),
  `momentum` (0,0,0), charge `plus` 1, `minus` -1, `electron` 0, `G` 0;
- (b) the ledger after each tick t from 1 to 9, every line balanced with
  sourced, escaped, annulled and absorbed 0 unless stated: `plus` initial 1,
  current 1 (in `annul` current 0 and annulled 1 from tick 7, the share
  annulled in the cycle labelled 6 after the plus arm, returned at M at tick
  3, reached X at tick 6; in `siblings` the one-line event has no sibling
  line, the share is restored to the lamp in that cycle and emitted again in
  the cycle labelled 7, one Link out after tick 8, two after tick 9, so
  current stays 1); `minus` initial 1, current 1 through tick 4, then
  current 0 and escaped 1 (at (0,2,2) after tick 4, out through -X at tick
  5); `electron` initial 4, current 4 through tick 4, then current 0 and
  escaped 4 (at (0,4,4) after tick 4, out through +Z at tick 5); `G` initial
  0, sourced 0, 5, 10, 15, 20, 20, 20, 20, 20 (five per crossing of
  (0,4,1), (0,4,2), (0,4,3) and (0,4,4), released in the cycles labelled 1
  to 4), escaped 0, 2, 5, 7, 10, 11, 13, 14, 16 (at every crossing the -X
  and +Y rays leave the world in the next tick; the -Z ray of the crossing
  at z = c walks back to E and out at tick 2c + 1; the -Y ray walks to y = 0
  and out at tick c + 5; the four +X rays are still in the world after tick
  9) and current sourced minus escaped: 0, 3, 5, 8, 10, 9, 7, 6, 4;
  `momentum` initial (0,0,0), current (0,0,0) through tick 4 (the two lamps'
  recoils against their rays), (1,0,-4) after ticks 5 and 6 (the plus arm
  reads +1u while returning, its share on the event's heading; the electron
  lamp keeps (0,0,-4)), then in `annul` (0,0,-4) with annulled (1,0,0) from
  tick 7 (the sink takes the share's reading, the lamp is unchanged) and in
  `siblings` (1,0,-4) (the restored share's recoil undone in the lamp, then
  the re-emitted ray), with escaped (-1,0,4) from tick 5; charge `plus`
  initial 1, current 1 (in `annul` current 0 and annulled 1 from tick 7),
  `minus` initial -1, current -1 through tick 4, then current 0 and escaped
  -1, `electron` and `G` every line 0; `escaped_charge_totals()` reads
  `minus` -1 from tick 5 and 0 otherwise; the spatial accounting balances at
  every tick;
- (c) one `detector_return` at tick 3 at M for family `plus`, no click, and
  one `inverse_split` in the cycle labelled 6 at X with the mode, its
  `annulled` {plus: (1,), momentum: (1,0,0)} in `annul` and {} in
  `siblings`;
- (d) the runner on the same document records `ray_event_audit:
  "ray-event-audit-v1"` and `audit`, the nine ledgers of (b) as written by
  `json`, `conserved_at_every_completed_tick` true and
  `accounting_balanced_at_every_completed_tick` true in both modes,
  `completed_ticks` 9, `audit_failure` none; a second run writes the same
  `events.jsonl` and `run.json` (but `elapsed_seconds`);
- (e) the recorded ledger with the plus line's current charge at tick 3
  raised by 1 is reported as `{"tick": 3, "readout": "charge", "line":
  "plus"}`, and with G's escaped amount at tick 9 set to 15 as `{"tick": 9,
  "readout": "fields", "line": "G"}`, from the integers alone;
- (f) the document with a `ray_interactions` rule `flip` (participants
  `plus` and `minus`, outputs `plus` of input 0 and `plus` of input 1) is
  rejected at validation with "would change the total charge";
- (g) the pair alone (no electron lamp, no G) under a `conservation` block
  (carriers: energy `plus` + `minus`, momentum `momentum`; spatial: energy
  the two fields' right sides added, momentum (0,0,0)) runs nine ticks with
  the local audit `passed`, its ledger the lines of (b) for `plus`, `minus`
  and `momentum` (momentum current (1,0,0) from tick 5, (0,0,0) in `annul`
  from tick 7), and the local audit's `initial`, `current`, `escaped` and
  `annulled` read the ledger's lines summed over the two families: energy
  2, 0 (`annul`) or 1 (`siblings`), 1, 1 or 0; momentum (0,0,0), (0,0,0)
  or (1,0,0), (-1,0,0), (1,0,0) or (0,0,0); charge 0, 0 or 1, -1, 1 or 0;
  the report's `sourced` line is 0 there;
- (i) the whole `annul` world (the electron lamp and G included) under a
  `conservation` block (a second carrier row for the electron lamp, the
  spatial energy the four families' right sides added) runs nine ticks with
  the local audit `passed`, since the audit reads every release as a source
  at its Node (the five field rays a crossing releases have net momentum
  minus the ray's own heading, (0,0,-1) here, and no owner pays for them):
  its report at tick 9 reads initial energy 6, momentum (0,0,0), charge 0;
  sourced 20, (0,0,-4), 0; current 4, (4,0,-4), 0 (the four +X field rays
  and the electron lamp's recoil); escaped 21, (-5,0,0), -1 (the minus arm,
  the electron and sixteen field rays); annulled 1, (1,0,0), 1;
- (h) every ledger carries the bodies' own lines beside the identity:
  `count`, `momentum` (the exact sum over the bodies), `charge` (the sum of
  their declared charges) and `sink` (their sinks per field, the `absorbed`
  line of every field); without a body count 0, momentum (0,0,0), charge 0
  and every sink 0. The `body` world is the `annul` world with a fifth
  family `star` (charge 0, no lamp) and one external body at B = (1,2,2) of
  family `star`, amount 100, charge 3, coupling `sink`, at rest, no momentum
  table: the minus arm arrives at B at tick 3 and ends in the sink, so from
  tick 3 `minus` reads current 0 and absorbed 1 (never escaped), charge
  `minus` current 0 and absorbed -1, `momentum` absorbed (-1,0,0) with
  current (1,0,0) after ticks 3 and 4, (1,0,-4) after 5 and 6 and (0,0,-4)
  from tick 7, escaped (0,0,4) from tick 5 (the electron alone) and annulled
  (1,0,0) from tick 7; `star` every line 0; `escaped_charge_totals()` reads
  0 for every family; `external_bodies()` lists the one body at B, not
  stepping, momentum (0,0,0), accumulators (0,0,0), sink {} through tick 2
  and {minus: 1} from tick 3; the bodies' lines read count 1, momentum
  (0,0,0), charge 3 and sink `minus` (1,) and `momentum` (-1,0,0) from tick
  3; every other line as in (b) to (f), and the runner's
  `external_body_totals` equals the last ledger's sink.

Pinned consequences in existing tests (2026-09-17, `ray-event-audit-v1`):
`conserved_at_every_completed_tick` is the world ledger's identity, so it
reads true wherever content left through an open boundary or into the
annulled sink and every line balances: `test_inverse_split.py` in `annul`
([Inverse split](#inverse-split)), the two escapes of the
[ray viewer extraction](#ray-viewer-extraction), the five escaped +y rays of
`test_ray_integration_guards.py` (funded momentum through absorption and
escape) and the open world of `test_disturbance_application.py` (escape
without dissipation, 72 `strength` and 16 `radiation` escaped, localized
stock counted in the totals); each of those pins read false before feature
10. `charge_totals()` counts the stock a record holds of a charged family,
so the charge case of `test_wave_ray_families.py` reads `plus` 3 and
`minus` -5 before the first tick as well as after it (it read 0 and 0 before
feature 10, over rays alone).

## Detector-owned sampling admission

[Detector sampling tests](../tests/test_detector_sampling_contract.py) accept only
`detector-only-v1` under the [Detector-only contract](DETECTOR_SAMPLING.md): the
deleted `historical-autonomous-v1` profile, the deleted lottery capture (with
`capture_seed` and `capture_salt`) and the deleted bond-registry and claim-gather
keys (`bond`, `bond_field`, `bond_setting`, `claim`, `train_field`) are rejected
at parsing, at direct typed construction and at `SpatialLaw` before any ticket is
consumed; a record named Detector or an observer grants no draw authority; and
the share and threshold captures parse and draw nothing. The historical seed-7
lottery fixture was deleted on 2026-09-17 with the lottery capture, and the native
instrument/contact fixtures with the integration layer. PASS and the draw are
implemented by the Detector mark (`detector-mark-v1`,
[Node Detector bit](#node-detector-bit)) and the return on 0 by
`detector-return-v1` ([Detector return](#detector-return)); the inverse split
and output-clock composition remain blocked by the contract's
owner/acceptance table.

## Wave-ray families

`test_wave_ray_families.py` builds four boards inline under the shared Detector
admission (schema 1, `link_ticks` 1, `metric: "links"`, pace 1/1, no decay, the
six unit-axial headings in Port order, closed under negation), periodic, one
conserved scalar per family and one holding lamp per family that pays its
whole stock into one directed or swept emission
([wave-ray families](SPATIAL_FIELDS.md#wave-ray-families-wave-ray-family-v1)).
Pinned before the first run:

- (a) on 7^3 a lamp at (3,3,3) with stock 30 sweeps 15 per tick over the six
  headings at emission phase 5, on a plain field with `phase_bits` 3 and on the
  same field with `kerengonen` `phase_steps` 8, `phase_advance` 0 (both width
  3, modulus 8, rate 0), each world held to the same integers (no world is
  compared with another, [Highlights 5.5](HIGHLIGHTS.md#55-acceptance-tests-and-open-decisions)):
  after tick t (1 to 4) the first emission's six rays are at (3,3,3) + t x
  unit, modulo 7, one per Port, amounts 3, 3, 3, 2, 2, 2, phase 5, steps t,
  mask 63, shares (3, 3, 3, 2, 2, 2), alone at their Nodes except after tick
  4, when each such Node also holds the second emission's ray coming the
  opposite way (steps 3), the two meeting around the 7-ring; the world holds
  6, 12, 12, 12 rays, all of phase 5 and no own advance, steps t and t - 1,
  totals 30 and the accounting balanced; Node (4,3,3),
  one Link from the lamp along +X, reads value 3 after ticks 1 and 2 and 0
  after ticks 3 and 4 (the pin first written as 3 after tick 4 was a
  derivation slip corrected before the expectation was held). Rejected at
  parsing: phase 5 on a plain field
  without a width, `phase_bits` 4 beside `phase_steps` 8, `phase_steps` 12,
  `phase_advance` 8 at width 3, `capture` without a table, a carried phase
  without a table, `phase_bits` -1, and `charge` on an outward field;
- (b) on 25 x 5 x 5 a light family (plain, `phase_bits` 8) and a massive
  family (`phase_steps` 256, `phase_advance` 13), each with a lamp of stock 4
  emitting 4 along +X at phase 77, from (2,2,2) and (2,3,3): after tick t (1
  to 20) the light ray at (2 + t, 2, 2) has phase 77, steps t, mask 1, shares
  (4, 0, 0, 0, 0, 0); the massive ray at (2 + t, 3, 3) has phase (77 + 13 t)
  mod 256: 90, 103, 116, 129, 142, 155, 168, 181, 194, 207, 220, 233, 246, 3,
  16, 29, 42, 55, 68, 81; totals 4 and 4;
- (c) on 9 x 5 x 5 the families `plus` (charge 1) and `minus` (charge -1),
  lamps of stock 3 at (2,2,2) emitting along +X and stock 5 at (6,2,2)
  emitting along -X, and a `ray_interactions` rule `reflect` that negates both
  headings with a declared `amount` invariant: the `RAY_PROPERTIES` names are
  amount, heading, phase, advance, delay, family, charge; the parsed rule's
  invariants are `amount` then `charge`, and the charge invariant evaluates
  to -2 over the views (3, +X, family 0, charge 1) and (5, -X, family 1,
  charge -1); `ray_charge` of amounts 3 and 4 at charge -1 is -7;
  `charge_totals()` is {plus 0, minus 0} before the first tick and {plus 3,
  minus -5}, sum -2, after every tick 1 to 6, with totals 3 and 5; the rays
  meet at (4,2,2) in tick 3, and after tick 6 the plus ray is at (0,2,2) on
  -X and the minus ray at (8,2,2) on +X, both steps 4, mask 3, shares
  (5, 3, 0, 0, 0, 0). Rejected at parsing: an assignment to `charge` or
  `family` (read-only) and a declared invariant named `charge`;
- (d) on 7 x 5 x 5 a family with `phase_bits` 128 and `phase_advance` 2^70
  (modulus 2^128, mask 2^128 - 1, no coherence table, Kerengonen identity), a
  lamp at (2,2,2) of stock 2 emitting 2 along +X at phase 2^128 - 3 x 2^70 =
  340282366920938459921599745279534301184: after tick t (1 to 100) the one ray,
  at ((2 + t) mod 7, 2, 2) with steps t and amount 2, has phase (t - 3) x 2^70
  mod 2^128: after tick 1 2^128 - 2^71 = 340282366920938461102191365996945604608,
  after tick 2 2^128 - 2^70, after tick 3 exactly 0, after tick 4 2^70, after
  tick 100 97 x 2^70 = 114517387209588896432128; totals 2 and accounting
  balanced at every tick. The ray reversed on its line (`outbound` 0),
  forwarded 100 times, leaves through Port 0 each time with steps 99 down to
  0 and the phase it had at the same step count on the way out, ending at
  2^128 - 3 x 2^70 with steps 0; a 101st forwarding keeps it resident with
  that phase and sends nothing, and `advance_ray` refuses it a Link ("event
  Node"; `detector-return-v1`, merged 2026-09-17); the case runs in about one
  second (the test allows twenty).
  Rejected: a modulus of 12 in `advance_ray`, `self_exclusion` or a ray
  interaction on the wide family (`phase_bits` at most 30), `phase_steps` 8
  beside `phase_bits` 128, and an emission phase of 2^128. The runner completes
  100 ticks of the wide world and records `wave_ray: "wave-ray-family-v1"`
  beside `ray_state: "ray-event-state-v1"`, `spatial_policy:
  "kerengonen-ray-field-v1"`, `conserved_at_every_completed_tick` true and
  final matter 2.

Existing worlds keep their amounts, phases, totals and audits: a plain field
has width 0 and rate 0, a Kerengonen field the width of its `phase_steps`. Two
test adaptations: `test_kerengonen.py` sets a nonzero emission phase before
expecting the rejection on a plain field without a width (phase 0 is admissible
there), and the odd table sizes 3 and 37 of `test_ray_integration_guards.py`
are checked through `phase_cosines` and `phase_sines` directly, a field
admitting only a power of two (the table-construction guard world uses 32
phase steps instead of 37).

## Ray binding

`test_ray_binding.py` builds its boards inline under the shared Detector
admission (schema 1, `link_ticks` 1, `metric: "links"`, pace 1/1, no decay,
the six unit-axial headings in Port order) on an open 21^3 lattice
([binding](SPATIAL_FIELDS.md#binding-and-gravity-by-delay-ray-binding-v1)).
The family `n` has rest rate 1 on a 3-bit phase (8 steps); `G` is its
field, `field_of: "n"` with `release: [1, 4]`, rate 0, 16 ray slots;
`light`, `x` and `p` are families of rate 0 with 8 ray slots. Two lamps at
(9,10,10) and (11,10,10) hold 8 of `n` each and emit it once, funded and
directed, toward each other at phase 0, so the two rays meet at the center
(10,10,10) after tick 1. The binding rule `bind` is `n x n` without outputs,
assigning `delay` 1 to both participants, invariant energy. The test is
parametrized over `binding`, `unbinding`, `ray_delay`, `gravity` and
`criterion`. Pinned before the first run:

- (a) `binding`: after tick 1 the two `n` rays are at the center with
  headings 0 and 1, amount 8, phase 1, steps 1, masks 1 and 2 and shares
  (8, 0, 0, 0, 0, 0) and (0, 8, 0, 0, 0, 0). From tick 2 the rule fires
  every interval: after tick t (2 to 6) both rays are at the center with
  steps 0, delay 0, phase t (advanced once per interval by the rest rate
  1), mask 3 and shares (8, 8, 0, 0, 0, 0), the group's tick being one event
  on both Ports; `bound_group` reads them, and the snapshot's
  `bound_groups` is one entry, position (10,10,10), families
  `["n", "n"]`, amounts `[8, 8]`, phases `[t, t]`, `ray_delay` 0. In the
  interval of every tick t from 2 the held rays release on all six
  headings: two rays of amount floor(8 x 1 / 4) = 2 per heading with equal
  phase merge to one G ray of amount 4 per heading, phase t - 1, steps 0,
  mask 0, so after tick t the G ray released at tick s (2 to t) is at
  distance t - s + 1 from the center along every axis with steps t - s + 1
  and phase s - 1. The G total and the G source total after tick t are both
  24 (t - 1): 0, 24, 48, 72, 96, 120; the `n` total is 16 with source 0;
  the spatial accounting balances. The runner records
  `ray_binding: "ray-binding-v1"` beside `released_field`, and a run of 6
  ticks writes four `bound_tick` events, one per cycle of ticks 2 to 5 (a
  cycle record carries the tick it started at; the cycle of tick t completes
  tick t + 1; the cycle of tick 1 is the meeting that forms the group, not a
  tick), each with position (10,10,10), families `["n", "n"]`, amounts
  `[8, 8]`, phases `[t + 1, t + 1]` and `ray_delay` 0;
- (b) `unbinding`: the rule `ionize`, declared before `bind`, is
  `n x n x x` with outputs `n` on Port 2 (amount and phase of input 0), `n`
  on Port 3 (of input 1) and `x` on `"same"` of input 2, invariant energy.
  A lamp at (10,6,10) emits an `x` ray of amount 3 along +Y: it is at
  (10,6+t,10) after tick t (1 to 4) and at the center after tick 4, the
  group intact through tick 4 (G total 72). At tick 5 `ionize` fires and
  `bind` has no participants left: after tick 5 the `n` rays are at
  (10,11,10) (heading 2) and (10,9,10) (heading 3), amount 8, phase 5,
  steps 1, mask 12, shares (0, 0, 11, 8, 0, 0); the `x` ray is at
  (10,11,10), heading 2, amount 3, phase 0, steps 1, the same mask and
  shares; `bound_groups` is empty from tick 5 and nothing is left at the
  center. The departing `n` rays release five headings each in the interval
  of tick 5 and after: the G total after tick t (5 to 8) is 72 + 20 (t - 4):
  92, 112, 132, 152, equal to the source; the `n` total is 16 and `x` 3;
- (c) `ray_delay`: `bind` declares `ray_delay` 2. A lamp at (10,7,10) emits
  a `p` ray of amount 3 along +Y (a family with no rule, its own layer). It
  reaches the center after tick 3 with `interaction_delay` 2 and steps 3,
  is still there after ticks 4 (delay 1) and 5 (delay 0), leaves at tick 6
  and is at (10,11,10) after tick 6 with steps 4 and at (10,14,10) after
  tick 9 with steps 7: every departure from the Node waits the declared two
  intervals. `bound_groups` reports `ray_delay` 2 from tick 2. Without the
  key the `p` ray is at (10,11,10) after tick 4;
- (d) `gravity`: the rule `gravity`, declared before `bind`, is `light x G`
  with outputs `light` (amount of input 0, heading `"same"`, phase
  `"same"`, `delay` `{"of": 1, "table": [4, 4, 4, 4, 4, 4], "per": 1}`)
  and `G` (amount of input 1, heading `"reversed"` of input 1), invariant
  energy. A lamp at (4,14,10) emits a light ray of amount 6 along +X at
  impact parameter b = 4 above the center. The light is at (4+t,14,10)
  after tick t (1 to 6), heading 0, steps t, phase 0, mask 1, shares
  (6, 0, 0, 0, 0, 0), lag (0, 0, 0). At tick 7 it meets at (10,14,10) the G
  ray released at tick 3 (amount 4, phase 2, steps 4, heading 2, which
  came in through Port 3): the delay is floor(4 x 4 / 1) = 16 phase steps
  on the -Y side, 2 full intervals at N = 8. After tick 7 the light is at
  (11,14,10), steps 1, mask 9, shares (6, 0, 0, 4, 0, 0), lag (0, -16, 0),
  having left its event Node through its event's Port; after tick 8 at
  (11,13,10), steps 2, lag (0, -8, 0); after tick 9 at (11,12,10), steps 3,
  lag (0, 0, 0): turned toward the group by 2 Links; after ticks 10 and 11
  at (12,12,10) and (13,12,10), steps 4 and 5, on its new line. The recoil,
  the G ray reversed (heading 3, amount 4, phase 2, mask 9, shares
  (6, 0, 0, 4, 0, 0)), is at (10,13,10) after tick 7 with steps 1,
  (10,12,10) after 8, (10,11,10) after 9, at the group's Node (10,10,10)
  after tick 10 with steps 4, and, crossing it (no coupling of `n` with `G`
  is declared), at (10,9,10) after tick 11. The G total and source are
  24 (t - 1) after every tick t of the 11 (the first release of tick 2
  reaches the open boundary at tick 12); the light total is 6, `n` 16; the
  accounting balances;
- (e) `criterion`: the board of (d) with the phase width N = 2^8, 2^10,
  2^12 and 2^16 (`phase_bits` 8, 10, 12, 16 on every family, no coherence
  table), the rest rate of `n` scaled to N / 8 so that the group's mass in
  phase units, M = 2 x N / 8 = N / 4 (the sum of its participants' rates in
  units of m_0 = 1 phase step per interval), is the same fraction of N:
  M = 64, 256, 1024, 16384. Everything else is fixed: the light ray, b = 4,
  the release, the table. After tick 8 the light is at (12,14,10), steps 2,
  heading 0, with lag (0, -16, 0): the delay is 16 phase steps at every N,
  below the modulus, so no Link is completed and the lag stays on the ray
  as its owner. The bending is alpha = 16 / N (Links of shift per Node of
  passage, exact), G_eff = alpha x b / (4 M) = 64 / N^2 (1/1024, 1/16384,
  1/262144, 1/67108864), and G_eff x N^2 = 64 for all four N, exactly.

## Catalog of nature

`test_nature_catalog.py` reads [`catalog/nature.json`](../catalog/nature.json)
([catalog of nature](CATALOG.md)) through the strict decoder and builds its
boards inline from the file under the shared Detector admission (schema 1,
`link_ticks` 1, `metric: "links"`, pace 1/1, no decay, the six unit-axial
headings in Port order) on a periodic 15^3 lattice at the reference width
(`phase_bits` 3, N = 8): every ray's `phase_advance` and `charge` are its
catalog record's `rest_rate` and `charge`, a field ray's `field_of` and
`release` are its record's, every rule's `participants`, `outputs` and
`invariants` are its coupling record's, and an external-body rule has the
met family written for `"any"` and `"same"`, the body's family for the
apparatus role and `"body"`, and 3 for `"setting"`. The test is parametrized
over `records`, `undecided`, `experiments` and `worlds`. Pinned before the
first run:

- `records`: the twelve sections, `phase_bits` without a real-N value and
  `lag_bits` open, its world key undecided and its engine (feature 8b) not
  landed; 12 rays and 16 couplings; `light` a field ray of `field_of`
  electron, positron and proton with release `[1, 4]`, its `spread`
  `[6, 1, 1, 1, 1, 1]` and its `source_sign` `releaser` (feature 12,
  `field-spreading-v1`, 2026-09-17; in `worlds` the light lamp's ray is
  therefore released again at (8,7,7) and is at (9,7,7) after two ticks as
  a fresh field ray with no event, steps 1, whole since phase 3 selects the
  forward entry), `light` in the `field` of the three charged
  families (the proton's since the helium-ion run, E4, whose fixed nucleus
  radiates it) and neither `electron_field` nor `positron_field` a ray
  (Highlights 3.5, 2026-09-17); every ray with
  `kind`, `rest_rate`, `charge`, `phase_bits`, `field` and `note`, a field ray
  with rest rate 0, charge 0 and no field, listed by every ray in its
  `field_of` and listing each of them, a bound group's charge the sum over its
  members (the proton +3 from up 2 and down 1, the neutron 0 from up 1 and
  down 2) and its binding a coupling that `binds`; every coupling with
  `status`, `engine`, `participants` (one to six, each a ray id, a list of
  ray ids, `"any"` or the external body), `invariants` and one of `outputs`,
  `binds`, `sink`; a decided coupling with nothing undecided in its result and
  its engine landed; the external body listing exactly the couplings that
  name it, `absorber` its default, its declaration exactly the eight keys of
  `external-body-v1` and its apparatus family of rest rate 0, charge 0 and no
  field, not a ray of the catalog; the Detector's declaration exactly
  `position`, `setting`, `seed`; the Detector's two couplings on the bit,
  `on_bit_1` and `on_bit_0`, open, their world key undecided and decided by
  feature 2b, their engine not landed, their defaults pass without a draw
  and transmission without a draw (Highlights 5.4, 2026-09-17); both
  apparatus kinds landed;
- `undecided`: 30 entries, every decider one of A1, A2, A3, A5, A6, A8, A9,
  A10, A12, hypothesis 12, hypothesis 13, feature 2b, feature 8b, read from
  the
  `### A<n>.` and `### B<n>.` headings of the register, the `## <n>.` headings
  of the hypotheses page and the `feature <n>` names of the ray-event model;
  the table of `CATALOG.md` equal to the file, path for path and decider for
  decider;
- `experiments`: the ids equal to the `### A<n>.` headings of the register,
  14 of them, every listed ray, coupling and apparatus resolving and none
  repeated; A1's first coupling `born_steering`, A5's `electron_field_turn`;
- `worlds`: the rays a world can select today are `light`, `electron` and
  `positron`, in that order, and the releases a world can declare today are
  `light` by the electron and `light` by the positron, in that order
  (Highlights 3.5, 2026-09-17). For each ray, one lamp at (7,7,7) holding 5
  emits along +X at phase 3: after tick 2 the emitted ray is at (9,7,7),
  heading 0, amount 5, steps 2, mask 1, shares (5, 0, 0, 0, 0, 0) and phase
  3 + 2 × rate mod 8, that is 3 for light and 5 for the electron and the
  positron. For each release, the world holds the releaser and `light`
  declared `field_of` the releaser with its release, the same lamp emitting
  the releaser: the releaser's departure from (8,7,7) at tick 2 releases five
  rays of amount floor(5 × 1 / 4) = 1, phase 4 (the releaser's phase at the
  release), steps 1 and no event, at (7,7,7) heading 1, (8,8,7) heading 2,
  (8,6,7) heading 3, (8,7,8) heading 4 and (8,7,6) heading 5; the totals are
  5 for the releaser and 5 for light with a light source total of 5; the
  charge totals are 5 × charge, −15 for the electron and +15 for the
  positron, 0 for light; the accounting balances at every tick. The
  couplings the engine runs today are `born_steering`, `electron_field_turn`, `absorber`, `mirror` and
  `phase_plate`, in that order. `born_steering`: two light lamps holding 8,
  at (6,7,7) emitting along +X at phase 0 and at (8,7,7) along −X at phase
  d, meet at (7,7,7) after tick 1 and are steered at tick 2: at d = 0, 1, 2,
  4 the +Y output at (7,8,7) is 16, 14, 8, 0 with phase 0 and the −Y output
  at (7,6,7) is 0, 2, 8, 16 with phase d, each an event of mask 4, 12, 12, 8
  and shares (0, 0, +Y amount, −Y amount, 0, 0) with steps 1, an output of 0
  being no ray; nothing is left at (7,7,7); the total is 16 and the source
  total 0. `electron_field_turn`: an electron lamp holding 5 at (6,7,7)
  emitting along +X at phase 0 and a `light` lamp holding 1 at (7,8,7)
  emitting along −Y at phase 0, light declared `field_of` the electron, meet
  at (7,7,7) after tick 1; at tick
  2 the electron leaves on the field ray's heading −Y to (7,6,7) with amount
  5, phase 2, steps 1, mask 12 and shares (0, 0, 1, 5, 0, 0), the field ray
  returns reversed to (7,8,7) with amount 1, phase 0, steps 1 and the same
  mask and shares, and the electron's departure from (7,7,7) releases five
  field rays of amount 1, phase 1, steps 1 and no event, at (8,7,7) heading
  0, (6,7,7) heading 1, (7,8,7) heading 2 (beside the reversed ray), (7,7,8)
  heading 4 and (7,7,6) heading 5; the totals are electron 5 and
  `light` 6, the source totals 0 and 5, the charge totals −15 and
  0; nothing is left at (7,7,7). The three external-body couplings share one
  light lamp holding 5 at (7,7,7) emitting along +X at phase 1 and one body
  at (8,7,7) of amount 4096 at rest. `absorber`: the body is of the electron
  family, charge −3, coupling `"sink"`; the ray ends in its sink in its
  arrival interval, tick 1: after ticks 1 and 2 no ray is on the board, the
  totals are light 0 and electron 0, `external_body_totals` light 5 and
  electron 0, the one body at (8,7,7) with momentum and accumulators zero,
  not stepping, sink light 5, and the bodies' momentum (0, 0, 0). `mirror`
  and `phase_plate`: the body is of the apparatus family; after tick 1 the
  ray is resident at (8,7,7) and at tick 2 the rule fires over it and the
  body's token: under the mirror the ray is at (7,7,7) after tick 2, heading
  1, amount 5, phase 1, steps 1, mask 3 and shares (1, 5, 0, 0, 0, 0), the
  token's quantum on +X beside its own; under the phase plate with setting 3
  it is at (9,7,7), heading 0, amount 5, phase 4, steps 1, mask 1 and shares
  (6, 0, 0, 0, 0, 0); nothing is left at (8,7,7), the totals are light 5 and
  apparatus 0, the body's sink is empty and `external_body_totals` is 0 per
  family. A `detectors` mark at (9,7,7) with setting [1, 1] and seed 0 parses
  on the light world. The accounting balances at every tick of every world.
