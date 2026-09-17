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
| `test_check_scope.py` | 47 | 0.10 | Changed-code test selection of `tools/check.py` (running branch, untouched) |
| `test_configuration_validation.py` | 99 | 2.40 | Read-only configuration preflight, format ownership and its CLI, over every shipped input |
| `test_detector_mark.py` | 1 | 0.18 | Issue #169 feature 2: a marked Node draws one bit per arriving ray (`detector-mark-v1`; feature test, untouched) |
| `test_detector_sampling_contract.py` | 18 | 0.00 | Detector-only sampling admission (running branch, untouched) |
| `test_disturbance_application.py` | 14 | 0.29 | Runner record: headless run files, the saved initialization and source fingerprint that replay a run, explicit CLI opt-ins |
| `test_disturbance_engine.py` | 23 | 0.02 | Carrier Node cycle: budget wait, fixed Link time, split and whole-record transport, exchange remainders, capacity-failure atomicity |
| `test_energy_audit.py` | 9 | 0.31 | Funded ray emission with recoil and absorption under the audit (running branch, untouched) |
| `test_initialization.py` | 42 | 0.00 | Initialization parser: one fixed schema, resolved references, no physics from names, bounded expression language |
| `test_integer_arithmetic.py` | 75 | 0.00 | Bounded integer arithmetic: signed and ceiling division, remainders, component operations, overflow before cancellation |
| `test_json_documents.py` | 52 | 0.00 | Documentation gate: strict JSON decoding shared by inputs, editor fragments and observer files |
| `test_kerengonen.py` | 19 | 6.88 | Phased rays: phase advance, coherence, capture, slit, mirror and pace (running branch, untouched) |
| `test_local_conservation.py` | 18 | 0.01 | Passive local energy/momentum audit across Node events and Link flux |
| `test_local_conversions.py` | 16 | 0.00 | N-to-M record conversion as an atomic inventory transfer with declared balances |
| `test_local_field_rules.py` | 11 | 0.13 | Local field rule: six-Port reads, retained and outgoing owners, guarded joint proposals |
| `test_local_focus.py` | 31 | 1.28 | Local Focus scheduler equals the ordinary scheduler tick by tick, serial and parallel |
| `test_locality.py` | 7 | 0.00 | Static gate: no world reads or shadow replay in generic field code |
| `test_native_ray_coupling.py` | 33 | 0.04 | Ray interactions, the generic coupling (running branch, untouched) |
| `test_node_conservation.py` | 13 | 0.00 | Pre-commit conservation readout guard and its bounded readout cache |
| `test_node_rule_contract.py` | 38 | 0.00 | Node profile contract: explicit k*h duration, indexed vector rules, record policies |
| `test_node_state_contract.py` | 9 | 0.31 | Node-state contract: evolving state is formula-free |
| `test_payload_validation.py` | 26 | 0.00 | Signed and unsigned integer codes (zigzag) validate exactly as the decoding reference, without decoding |
| `test_plan_reuse.py` | 8 | 0.16 | Exact transition plan reuse (running branch, untouched) |
| `test_rational_particles.py` | 16 | 0.47 | Opt-in bounded rational ratios: balanced routes, fractional credit, local checks |
| `test_ray_coupling_evidence.py` | 3 | 0.00 | Evidence helper of the ray coupling (running branch, untouched) |
| `test_ray_delay.py` | 6 | 12.78 | Output clocks: rays wait at a loaded Node and the phase per interval shows the wait |
| `test_ray_field.py` | 22 | 0.31 | Straight ray transport: DDA heading, emission sweep and shares, shell stock, slots, escape |
| `test_ray_hidden_state.py` | 1 | 0.19 | Issue #169 feature 1: every ray carries its event and its steps (`ray-event-state-v1`) |
| `test_ray_integration_guards.py` | 22 | 0.36 | Ray integration boundaries (running branch, untouched) |
| `test_ray_layers.py` | 2 | 0.28 | Issue #169 feature 5: rules of different layers fire in one interval and an unruled family crosses (`ray-layers-v1`) |
| `test_ray_merge_contracts.py` | 16 | 0.04 | Ray merge and ownership boundaries (running branch, untouched) |
| `test_ray_viewer.py` | 1 | 0.15 | Tooling: `tools/ray_viewer/extract.py` reads a runner record into rays, events and captions, pinned below (no browser) |
| `test_record_operations.py` | 19 | 0.00 | Record merge by type and channel, reserved slots and capacity policy |
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

`test_record_operations.py` verifies that reserved empty slots cannot receive
new records: select the first unlocked spare, or reject the entire proposal
without mutation when capacity is insufficient. It checks generic vector
merging with independent expected components, separation by type/channel/pending lock and whole-record
transport, all-or-nothing failure for overflow and capacity, zero-state activity
(including held zero records with configured local checks),
and configured cost reporting without repricing. Direct engine composition tests
prove that the injected activity policy is used and that a capacity-changing
arrival proposal fails before packets are cleared. Existing timing, generic-name,
spatial-response and native-event tests retain the cross-owner contracts.

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
| `test_check_scope.py` | Explicit non-import edges retain identity-example and reference-script consumers; the exact scope report expires while unrelated files survive; dry-run creates no output |

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
| `test_ray_hidden_state.py` | Every ray carries its event and its steps ([ray hidden state](#ray-hidden-state)): a sweeping lamp's six rays carry mask 63 and shares (3, 3, 3, 2, 2, 2) with steps and phase equal to the tick; rays of two events with one heading and phase stay two rays (7t rays after t ticks); a returning ray walks steps 5 to 0 and phase 1 to 4 backward and is refused a Link beyond its event Node; 1200 quanta and zero momentum every tick, the audit passed, the runner recording `ray-event-state-v1` |
| `test_detector_mark.py` | A marked Node draws one bit per arriving ray ([Node Detector bit](#node-detector-bit)): six lamps around one marked Node with setting 1/2 and seed 3 arrive in one interval and draw (0, 0, 0, 1, 1, 0) in Port order, exactly two clicks (Ports 3 and 4, amounts 4 and 5), the six rays leave with `detector` 1 or 2 matching the bits and continue unchanged, the marked and the unmarked control world agree on totals, momentum, lamps and rays at every tick, the control consumes no ticket, a replay writes the same events and run record, the runner records `detector-mark-v1`, and a mark without a setting, a setting above 1, a zero denominator, a seed at the modulus, a duplicate or outside position and a world without an admitted ray field are rejected |
| `test_ray_layers.py` | Rules of different layers fire in one interval and an unruled family crosses ([ray layers](#ray-layers)): five rays of families a, a, b, b, c meet at one Node after tick 2; after tick 3 the a rays have swapped headings (mask 3, shares (5, 5, 0, 0, 0, 0), steps 1), the b rays have turned to +Z and -Z at phase 7 (mask 48, shares (0, 0, 0, 0, 5, 5), steps 1) and the c ray is one Link past the Node unchanged (mask 16, steps 3, phase 3); the derived layers are (a), (b), (c) whether or not the b rule is declared, and without it the b rays cross like c; totals 10, 10, 5 and zero momentum every tick with the audit passed, the runner recording `ray-layers-v1` and the layer families |

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
on the [catalog conversion input](../examples/known-entities/conversion.json).
The catalog compiler, profile and family-conversion modules were deleted on
2026-09-17; the conversion rule is covered here alone.

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
  4, 3, 2, 1, 0 and phase 0, 7, 6, 5, 4; a sixth Link is refused ("event
  Node"); `validate_rays` rejects `steps` -1, `outbound` 2, `event_ports` 64,
  a share where the mask bit is zero, and `detector` 3;
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
  amount p + 1, `steps` 1, phase 1, `outbound` 1, `event_ports` `1 << (p ^ 1)`
  and `event_shares` its amount on that Port, and `detector` 2 for Ports 3 and
  4 and 1 for Ports 0, 1, 2 and 5;
- (b) after tick t (2 to 4) the ray that came in through Port p is t - 1
  Links beyond C on the opposite side, at C minus (t - 1) times the unit
  vector of Port p, with `steps` t, phase t, its amount and its bit unchanged:
  after tick 2 at (6,7,7), (8,7,7), (7,6,7), (7,8,7), (7,7,6), (7,7,8) for
  Ports 0 to 5; the six rays are the whole ray inventory of the world at
  every tick;
- (c) the marked world and the control world agree at every tick 1 to 4 on
  the totals (21 quanta, momentum (0, 0, 0)), on the audited energy and
  momentum, on every lamp's stock and recoil (0 quanta each; momentum
  (1,0,0), (-2,0,0), (0,3,0), (0,-4,0), (0,0,5), (0,0,-6)), and on every ray's
  position, heading, amount, steps and phase; the control's rays carry
  `detector` 0 everywhere, its Nodes carry no mark and it records no click;
  neither world's unmarked Nodes call the ticket rule, and the control world
  never does (a monkeypatched `next_ticket` fails the test if called);
- (d) the runner run twice on the same document writes the same
  `events.jsonl` byte for byte, including exactly two `detector_click`
  lines, and the same `run.json` apart from `elapsed_seconds`, recording
  `detector_mark: "detector-mark-v1"` beside `sampling_profile:
  "detector-only-v1"` and `ray_state: "ray-event-state-v1"`, with
  `conserved_at_every_completed_tick` true and final quanta 21;
- (e) `parse_initial_state` rejects a mark without `setting`, a setting
  `[3, 2]`, `[1, 0]` or `[-1, 2]`, a seed of 1073741789 or -1, two marks at
  one position, a mark outside the shape, marks on a world without a ray
  field, and marks on a Euclidean-metric ray field; `validate_configuration`
  reports the same documents invalid.

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
the two unit-axial headings +X and -X) on an open 5 x 3 x 3 board with an
8-step phase advancing 1 per Link, runs it for six ticks through
`run_initialization` headless, and reads the record back with
`tools/ray_viewer/extract.py` ([ray viewer](../tools/ray_viewer/README.md)),
which never imports the simulator. Lamp A at (1,1,1) holds 3 quanta and
emits 3 through +X with phase 0; lamp B at (3,1,1) holds 3 and emits 3
through -X with phase 4; each recoils into its own momentum. The one declared
coupling, `swap_headings`, fires when two rays with opposite headings whose
phases sum to 6 meet (1 and 5, what the lamps' phases are after one Link),
exchanges their headings and sets `delay` 1 on both; energy 6 and momentum
(0,0,0) are its invariants. The phase condition is what makes it fire once:
a first draft conditioned on opposite headings alone stayed true after the
swap, re-fired every interval and held both rays at (2,1,1) for the whole run,
which is the engine's binding behavior (a rule that keeps setting `delay` on
its participants), not a defect. The Node (4,1,1) carries a Detector mark with
setting 1/1 and seed 0, so every arrival there draws 1. Pinned before the
first run, from the event stream alone (no per-tick recording, so no phase):

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
  on the +X ray; two escapes at tick 5, at (0,1,1) through -X and at (4,1,1)
  through +X; no crossing, split, deflection or return;
- (c) the captions: tick 0 names both emissions, tick 1 the meeting with the
  coupling and both invariants, tick 2 the outputs leaving, tick 4 the
  Detector PASS with its bit, tick 5 the escapes; `in_world` quanta stays 6
  through tick 4 and is 0 from tick 5, when `escaped` is 6; the run's
  conservation line reads `passed`, with
  `accounting_balanced_at_every_completed_tick` true and
  `conserved_at_every_completed_tick` false because the 6 quanta left through
  the open boundary and the runner's escaped totals hold them (the first
  draft of this pin expected true there and had misread that flag, which
  counts only what stays in the world); the record carries
  `ray-event-state-v1`, `detector-mark-v1` and no unknown event kind;
- (d) tolerance: the same record with one appended event of an unknown kind
  (`field_release` at tick 3 at (2,1,1)) extracts to the same rays and
  events plus one generic marker of that kind at that Node and tick, and the
  record reports `{"field_release": 1}` as unknown.

The runs document is `ray-viewer-runs-v1`. A GIF or page rendered from it is
a rendering of the fingerprinted record, not evidence by itself.

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
[Node Detector bit](#node-detector-bit)); the return on 0 and output-clock
composition remain blocked by the contract's owner/acceptance table.

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
  balanced at every tick. The ray reversed on its line (`outbound` 0, the
  return of feature 3 not being on main), forwarded 100 times, leaves through
  Port 0 each time with steps 99 down to 0 and the phase it had at the same
  step count on the way out, ending at 2^128 - 3 x 2^70 with steps 0; a 101st
  Link is refused; the case runs in about one second (the test allows twenty).
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
