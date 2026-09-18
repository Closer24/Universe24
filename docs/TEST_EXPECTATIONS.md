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
| `test_a5_static.py` | 5 | 10.8 | Experiment A5s (`examples/nature/a5_static/`): the fifteen worlds byte for byte what `make_worlds.py` writes and the pinned geometry, the r = 4 like-charge world's first eight ticks (the registers, the ledger, no step), the committed record of the measured series (the window sums, the exponent, the diagonal, the control, the verdicts), and Run 2's six dense worlds with the mean field's predictions written before it, pinned below |
| `test_a6_bending.py` | 4 | 40 | Experiment A6 (`examples/nature/a6_bending/`): the forty-six worlds of the two forms byte for byte what `make_worlds.py` writes and the pinned geometry, the small world of each form re-run for 40 ticks (the turn form's register per tick and first push, the delay form's lag per tick on the ray's own axis alone and no heading change), the mean field's predictions written before the series, and the committed record of the measured series (the registers, the exponent, the N scan, the diagonal, the verdicts), pinned below |
| `test_architecture.py` | 28 | 0.34 | Static gate: layer dependency direction, formula-free API assembly and the integer audit of every physical module |
| `test_boundary_configuration.py` | 89 | 0.00 | Topology: the six-face neighbor function under periodic and open boundaries, as a pure function and at the schema |
| `test_check_scope.py` | 27 | 0.10 | Changed-code test selection of `tools/check.py`; every resource row names a kept test |
| `test_configuration_validation.py` | 99 | 2.40 | Read-only configuration preflight, format ownership and its CLI, over every shipped input |
| `test_decay_draw.py` | 1 | 1.05 | Issue #169 feature 13: a decaying group draws at its corner meetings; a rule with outputs that declares `draw: [n, d]` and `seed` draws once per meeting of its participants from the Node's ticket stream, the unsalted draw of `detector-mark-v1`, fires on 1 and yields to the next rule on 0, the ring surviving with the law (1 - n/d)^k over k meetings, the draws recorded and the tickets consumed equal to the meetings, a world without `draw` never calling the ticket rule (`decay-draw-v1`) |
| `test_dense_field.py` | 4 | 1.0 | The dense mode for boards that a field fills (`dense-field-v1`, [performance](PERFORMANCE.md#the-dense-mode-measured-before-adoption-2026-09-17)): the pure-field Nodes cycled as one vectorized step, one split step equal to `spread_content` (the registers, the releases, the phases, the bit), the hand-over of rays between the region and the engine's Nodes both ways, the same `state.json` and ledger as the engine alone, the unsupported worlds rejected, pinned below |
| `test_detector_bit_property.py` | 13 | 0.44 | Issue #169 feature 2b: a marked Node reads the bit a ray carries and passes it without a draw unless the mark declares `draw`, the outputs of a meeting inherit the bit, a guard reads it (`detector-bit-property-v1`) |
| `test_detector_mark.py` | 1 | 0.18 | Issue #169 feature 2: a marked Node draws one bit per arriving ray (`detector-mark-v1`; feature test, untouched) |
| `test_detector_return.py` | 6 | 0.40 | Issue #169 feature 3: a draw of 0 returns the ray reversed on its line, through no coupling, to rest at its event Node (`detector-return-v1`) |
| `test_detector_sampling_contract.py` | 18 | 0.00 | Detector-only sampling admission (running branch, untouched) |
| `test_disturbance_application.py` | 14 | 0.29 | Runner record: headless run files, the saved initialization and source fingerprint that replay a run, explicit CLI opt-ins |
| `test_disturbance_engine.py` | 23 | 0.02 | Carrier Node cycle: budget wait, fixed Link time, split and whole-record transport, exchange remainders, capacity-failure atomicity |
| `test_energy_audit.py` | 9 | 0.31 | Funded ray emission with recoil and absorption under the audit (running branch, untouched) |
| `test_field_spreading.py` | 10 | 0.90 | Issue #169 feature 12: every Node that field content reaches releases it again by the family's split table, amounts adding per heading, the phase of the coherent sum, whole quanta leaving and the shares below one quantum owned by the Node's remainder registers until they reach one (`field-spreading-v1`, `field-remainder-v1`); the source sign on the field ray; a returned field quantum walking back until something takes it |
| `test_helium_orbit.py` | 1 | 7.6 | The helium orbit of E8 in isolation on a 7^3 board: a proton-family body releasing its spreading light (`field-spreading-v1`, `field-remainder-v1`), an electron held at a launcher body by an output delay and released into that field, pushed at every Node by the momentum-table coupling (`ray-momentum-turn-v2`), the recoils, the transparent nucleus and its sink, the world ledger exact |
| `test_initialization.py` | 42 | 0.00 | Initialization parser: one fixed schema, resolved references, no physics from names, bounded expression language |
| `test_integer_arithmetic.py` | 75 | 0.00 | Bounded integer arithmetic: signed and ceiling division, remainders, component operations, overflow before cancellation |
| `test_json_documents.py` | 52 | 0.00 | Documentation gate: strict JSON decoding shared by inputs, editor fragments and observer files |
| `test_kerengonen.py` | 19 | 6.88 | Phased rays: phase advance, coherence, capture, slit, mirror and pace (running branch, untouched) |
| `test_local_conservation.py` | 18 | 0.01 | Passive local energy/momentum audit across Node events and Link flux |
| `test_local_conversions.py` | 17 | 0.00 | Two-to-two record conversion (`output_types`) as an atomic inventory transfer with declared balances; record `outputs` rejected |
| `test_local_field_rules.py` | 11 | 0.13 | Local field rule: six-Port reads, retained and outgoing owners, guarded joint proposals |
| `test_local_focus.py` | 31 | 1.28 | Local Focus scheduler equals the ordinary scheduler tick by tick, serial and parallel |
| `test_locality.py` | 7 | 0.00 | Static gate: no world reads or shadow replay in generic field code |
| `test_loop_binding.py` | 7 | 0.70 | Issue #169 feature 14: a bound group is a periodic orbit of the ordinary meeting rule on a ring of Nodes, nothing at a Node names it, the record reads it, and the held form's keys are rejected (`loop-binding-v1`) |
| `test_mean_field_gauss.py` | 3 | 0.01 | The mean-field kernel of `examples/nature/a5_static/mean_field_gauss.py` (the computation after experiment A5s): the split of one heading's content at one Node by the table [6, 1, 1, 1, 1, 1] relative to its heading, the conservation of the transport (the total kept until the front reaches the open boundary, the source's own sink taking the backward shares, the mirrored octant equal to the full box), and the beam 4096 x (6/11)^(r-1) as the push at ticks r and r + 1 on a sink at r = 1 to 4, pinned below |
| `test_momentum_turn_walk.py` | 4 | 7.8 | The fix of `ray-momentum-turn-v2`: a push keeps the DDA's accumulators, so a ray pushed at every interval walks the DDA line of its running register; the staircases of a push of 1 and of 8 per interval on a ray of 64, the flip, the cancel, the shrink and the lift by hand, and two boards where a field ray meets the ray at every Node |
| `test_native_ray_coupling.py` | 33 | 0.04 | Ray interactions, the generic coupling (running branch, untouched) |
| `test_nature_catalog.py` | 4 | 0.12 | Data gate: `catalog/nature.json` parses, every record and reference resolves, every undecided entry names its decider and is tabled in `CATALOG.md`, the register's entries agree, and every runnable ray and decided coupling is built from the file and run for two ticks (pinned below) |
| `test_node_conservation.py` | 13 | 0.00 | Pre-commit conservation readout guard and its bounded readout cache |
| `test_node_rule_contract.py` | 37 | 0.00 | Node profile contract: explicit k*h duration, indexed vector rules, aggregation policies |
| `test_node_state_contract.py` | 9 | 0.31 | Node-state contract: evolving state is formula-free |
| `test_payload_validation.py` | 26 | 0.00 | Signed and unsigned integer codes (zigzag) validate exactly as the decoding reference, without decoding |
| `test_plan_reuse.py` | 10 | 0.37 | Exact transition plan reuse: every argument of a law is its key, the world tick is not (a Node in a steady field reuses its plan across ticks, a lamp whose stock counts down does not), and a plan is validated once, when it is made, a hit being served without a second check, pinned below |
| `test_rational_particles.py` | 16 | 0.47 | Opt-in bounded rational ratios: balanced routes, fractional credit, local checks |
| `test_ray_binding.py` | 2 | 1.43 | Issue #169 feature 8, gravity by delay: a light ray is delayed by a declared table per Port at the field of a mass and turns toward it, G_eff x N^2 one integer over four widths (`ray-binding-v1`; its held form removed on 2026-09-17 by feature 14) |
| `test_ray_coupling_evidence.py` | 3 | 0.00 | Evidence helper of the ray coupling (running branch, untouched) |
| `test_ray_delay.py` | 6 | 12.78 | Output clocks: rays wait at a loaded Node and the phase per interval shows the wait |
| `test_ray_event_audit.py` | 3 | 0.90 | Issue #169 feature 10: the world ledger per completed tick, exact for amount, momentum and charge through a return, an inverse split, a release, an escape and an external body's sink (`ray-event-audit-v1`) |
| `test_ray_field.py` | 22 | 0.31 | Straight ray transport: DDA heading, emission sweep and shares, shell stock, slots, escape |
| `test_ray_hidden_state.py` | 1 | 0.19 | Issue #169 feature 1: every ray carries its event and its steps (`ray-event-state-v1`) |
| `test_ray_integration_guards.py` | 22 | 0.36 | Ray integration boundaries (running branch, untouched) |
| `test_ray_layers.py` | 2 | 0.28 | Issue #169 feature 5: rules of different layers fire in one interval and an unruled family crosses (`ray-layers-v1`) |
| `test_ray_meeting_conversion.py` | 6 | 0.25 | Issue #169 feature 6: a meeting replaces its rays by declared outputs, an amount split by a declared table, every family's stock exact (`ray-meeting-conversion-v1`) |
| `test_ray_merge_contracts.py` | 16 | 0.04 | Ray merge and ownership boundaries (running branch, untouched) |
| `test_ray_polarization.py` | 7 | 0.30 | Issue #169 feature 11: polarization as a ray property, a transverse direction modulo a half turn in steps of the family's polarization circle or none, declared by a lamp, part of the merge identity, carried by a meeting's outputs from their source input unless declared, by a spread as the axial mean and by the return; the polarizer, an external body's coupling splitting an arriving ray by its declared table at the difference between the body's angle and the ray's polarization, the pass share on the pass Port with the body's angle, the rest in the sink, the shares below one quantum in the body's registers (`ray-polarization-v1`) |
| `test_ray_momentum_turn.py` | 5 | 0.90 | Issue #169 feature 8b: a free ray's direction is its momentum register, walked by the DDA one Link per interval, pushed by the field rays a coupling's `momentum_table` names, the field ray returned reversed (`ray-momentum-turn-v1`; the walk kept through a push since `ray-momentum-turn-v2`, [the walk kept through a push](#the-walk-kept-through-a-push)) |
| `test_ray_viewer.py` | 4 | 0.15 | Tooling: `tools/ray_viewer/extract.py` reads a runner record into rays, events and captions, the style file, its GIF presets and the compressed inline page, pinned below (no browser) |
| `test_repository_hygiene.py` | 6 | 0.05 | Documentation gate: one canonical copy of every file and configuration |
| `test_repository_language.py` | 14 | 5.37 | Documentation gate: English repository text, ASCII paths and identifiers |
| `test_repository_navigation.py` | 8 | 0.09 | Documentation gate: Markdown links and Skill routes resolve |
| `test_retention.py` | 48 | 0.78 | Generated-output retention: 24-hour expiry, writer leases, protected paths |
| `test_ring_self_field.py` | 1 | (first run) | The ring under its own field of E10 in isolation: the nine worlds byte for byte what `make_worlds.py` writes, and the content-32 worlds for 16 ticks: the coupling `electron_field_turn` (`ray-momentum-turn-v2`) declared beside the corner table (`loop-binding-v1`), the corner-first record the control's event for event with no push, the turn-first record's eight pushes at tick 2 with their registers, the ring off its Nodes at tick 3, the group readings and the world ledger exact |
| `test_screen_loop.py` | 1 | 7.7 | The screen with a loop source of E9 in isolation: the unit-square ring of `loop-binding-v1` with rays of amount 4 releasing its light (`released-field-v1`) that spreads by the catalog's table with the Node-owned remainder (`field-spreading-v1`, `field-remainder-v1`) onto seven Detector marks, the ring read as one group of content 32 while it radiates, the first clicks and the world ledger exact |
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
local phases, resident rays and computation cost; hash collisions; bounded
LRU eviction; retry after failure; independent configurations; and default reuse
of repeated moving patterns in serial and parallel execution. Each tick retains
identical inventory, snapshots, ordered events, operation cost and local clocks.
The Focus, field, delay and formula-free state tests remain consumers of this
host-only optimization; `test_active_ports.py` was deleted on 2026-09-17.
Timing is measured outside CI assertions with identical inputs; no speed threshold replaces physical equality.

Since 2026-09-17 the spatial key does not hold the world tick, which the
spatial law never reads (the Node checks its clock before it plans; see
[Local Focus](LOCAL_FOCUS.md)). Pinned before the first run on a 7 x 3 x 3
open board: one `hold` lamp at x = 1 pays one quantum of `light` per interval
from a stock of 12 into a ray field with the single heading +X and a constant
phase (`phase_advance` 0), and the ray walks x = 2 to 6 and escapes. The Node
at x = k receives the same ray (amount 1, phase 0, k - 1 steps) every interval
from tick k on, so it evaluates once and hits from its second arrival; the
lamp's stock counts down in its record, so every interval presents a new key
and the lamp never hits. Over eight ticks the lamp plans 8 times, the Nodes at
x = 2 to 6 plan 7, 6, 5, 4 and 3 times: 33 requests, 13 evaluations, 20 hits,
cumulative per tick 0, 0, 1, 3, 6, 10, 15, 20; 9 quanta remain and 3 have
escaped. The same rule makes a lamp whose record does not change (an external
source without a budget) a steady Node that reuses its plan too; its plan is
the same plan.

Since 2026-09-17 a spatial plan is validated by the Node boundary
(`validate_spatial_plan`) once, when the execution evaluates it, before it is
returned or retained, and a reuse hit is served that plan without a second
check; the Node validates only what it changes after planning, an external
body's part, whose registers are outside the key. Pinned before the first run:
at the execution, two equal requests and a third with one more received packet
validate twice and hit once. On the lamp line above, eight ticks with Focus
on: 13 validations at the execution (one per evaluation) and none at the Node;
with Focus off the law itself serves the Nodes and each validates its own
plan, 33 at the Node and none at the execution; the two worlds agree at every
tick. The sink body of `test_external_body.py` alone (`release` [1, 2048])
for four ticks: the body's Node validates after each of its four cycles, the
execution once per evaluation (19 of 40 requests, 21 hits), and every hit is a
plan validated at its miss.

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
## Detector bit as a property

`test_detector_bit_property.py` builds its boards inline under the shared
Detector admission (schema 1, `link_ticks` 1, `metric: "links"`, pace 1/1,
no decay, the six unit-axial headings in Port order, closed under negation)
on a periodic 15^3 lattice with an 8-step phase advancing 1 per Link
([the bit read](DETECTOR_SAMPLING.md#the-bit-read-detector-bit-property-v1),
[the bit as a property](SPATIAL_FIELDS.md#the-detectors-bit-as-a-property-detector-bit-property-v1)).
Every lamp holds exactly what it emits once at tick 0, funded, at phase 0,
recoiling into its own momentum. Pinned before the first run from the
published ticket rule (`state = (state x 48271 + 1) mod 1073741789`,
`number = state^2 mod 1073741789`, bit 1 when `number x d < n x
1073741789`): one draw from seed 3 at setting 1/2 gives state 144814 and bit
0 (as in [Node Detector bit](#node-detector-bit)); one draw from seed 0 at
1/1 gives state 1 and bit 1; one draw from seed 5 at 1/1 gives state 241356
and bit 1, a second 913077587 and bit 1; seed 7 undrawn stays 7.

- (a) a lamp at (4,7,7) sends 8 quanta along +X (one directed emission).
  Mark A at (5,7,7), setting 1/1 and seed 0, draws the ray at tick 1: one
  `detector_click` (position (5,7,7), Port 1, family `quanta`, amount 8, bit
  1), the ray's `detector` 2, A's ticket 1 for the rest of the run. Mark B
  at (9,7,7), setting 1/2 and seed 3, receives the ray at tick 5 carrying
  bit 1. With no `on_bit_1` key, and with `on_bit_1: "pass"`, B does not
  draw: its ticket stays 3 through tick 6, one `detector_pass` (position
  (9,7,7), tick 5, Port 1, `quanta`, 8, `bit` 1) follows the click in the
  event stream, and after every tick t from 1 to 6 the one ray of the world
  is at (4 + t, 7, 7), heading index 0, amount 8, `steps` t, phase t,
  `outbound` 1, `detector` 2. With `on_bit_1: "draw"` B draws at tick 5,
  seed 3 at 1/2 drawing 0: one `detector_return` (position (9,7,7), tick 5,
  Port 1, `quanta`, 8) instead of the pass, B's ticket 144814, and after
  ticks 5 and 6 the ray is at (14 - t, 7, 7), heading index 1, amount 8,
  `steps` 10 - t, phase 10 - t, `outbound` 0, `detector` 1. In every case
  the totals are 8 quanta and momentum (0,0,0) and the conservation report
  passes at every tick; the runner writes the same two `detector_` lines
  and records `detector_bit_property: "detector-bit-property-v1"` exactly
  when the key was written (absent with no key), with
  `conserved_at_every_completed_tick` true and final quanta 8;
- (b) a pair lamp at X = (7,7,7) holds 8 and emits a sweep of two headings
  (`rays_per_tick` 2, cursor 0: +X and -X), 4 each way, one event with mask
  3 and shares (4, 4, 0, 0, 0, 0); X itself carries mark C, setting 1/1 and
  seed 7 (a source is a Detector); mark A at (10,7,7), setting 0/1 and seed
  3; mark D at (4,7,7), setting 1/1 and seed 5; ten ticks, `return_mode`
  siblings. Arm B (-X) reaches D at tick 3: one `detector_click` (position
  (4,7,7), Port 0, `quanta`, 4, bit 1), D's ticket 241356, and arm B is at
  ((7 - t) mod 15, 7, 7), heading index 1, amount 4, `steps` t, phase t mod
  8, `outbound` 1, `detector` 0 through tick 2 and 2 from tick 3, after
  every tick t. Arm A (+X) reaches A at tick 3: one `detector_return`
  (position (10,7,7), Port 1, `quanta`, 4), A's ticket 144814, and arm A is
  at (7 + t, 7, 7), 0, 4, t, t, 1, 0 after ticks 1 and 2 and at (13 - t, 7,
  7), 1, 4, 6 - t, 6 - t, 0, 1 after ticks 3 to 6; it walks back through no
  other mark and arrives at X, mark C, at tick 6 undrawn: C's ticket is 7 at
  every tick, C clicks, passes and returns nothing. One `inverse_split` in
  the cycle labelled 6 (position (7,7,7), `quanta`, `siblings`, `ports`
  (1,), `amounts` (4,), `amount` 4, `bit` 0, `restored` true, `annulled`
  {}) transmits 4 on arm B's line with bit 0, undrawn by C: the transmission
  is at (13 - t, 7, 7), 1, 4, t - 6, t - 6, 1, 1 after ticks 7 and 8 and
  reaches D at tick 9 carrying bit 0. With no `on_bit_0` key D does not
  draw: one `detector_pass` (position (4,7,7), tick 9, Port 0, `quanta`, 4,
  `bit` 0), D's ticket 241356 through tick 10, the transmission at (3,7,7),
  1, 4, 4, 4, 1, 1 after tick 10. With `on_bit_0: "draw"` D draws it at
  tick 9, seed 5's second draw at 1/1 giving 1: a `detector_click`
  (position (4,7,7), tick 9, Port 0, `quanta`, 4, bit 1) instead, D's
  ticket 913077587, the transmission's `detector` 2 from tick 9. The event
  stream is the D click, the A return, the split, then the D event; the
  totals are 8 quanta and momentum (0,0,0) and the conservation report
  passes at every tick;
- (c) lamp 0 at (5,7,7) sends 5 quanta along +X, lamp 1 at (9,7,7) sends 5
  along -X; mark M at (6,7,7), setting 1/1 and seed 0, realizes lamp 0's ray
  at tick 1 (one `detector_click`, position (6,7,7), Port 1, `quanta`, 5,
  bit 1; `detector` 2); the declared rule `meeting` (two `quanta`
  participants, no guard, energy and momentum invariants) replaces the two
  rays that meet at (7,7,7) at tick 2 by two outputs of 5: `{"of": 0}` on
  Port 2 (+Y) and `{"of": 1}` on Port 3 (-Y) with `input` 1. After tick 1
  the rays are at (6,7,7), 0, 5, 1, 1, 1, 2 and (8,7,7), 1, 5, 1, 1, 1, 0;
  after tick 2 both at (7,7,7) with `steps` 2 and phase 2; after ticks 3
  and 4 the outputs are at (7, 5 + t, 7), 2, 5, t - 2, t, 1, b and (7, 9 -
  t, 7), 3, 5, t - 2, t, 1, b with `event_ports` 12 and `event_shares` (0,
  0, 5, 5, 0, 0), where b is the inherited bit: 2 with no `bit` key, with
  `bit: "highest"` and with `bit: {"of": 0}` (lamp 0's ray, heading index 0,
  is participant 0 in merge order); 0 with `bit: "none"` and with `bit:
  {"of": 1}`. The parsed rule carries `bit` -1 (`BIT_HIGHEST`) and
  `bit_declared` false with no key, -1 and true for `"highest"`, -2
  (`BIT_NONE`) and true for `"none"`, 0 or 1 and true for `{"of": i}`. The
  totals are 10 quanta and momentum (0,0,0) at every tick, the report
  passes, and the runner records the identity exactly when the key was
  written;
- (d) the meeting of (c) guarded by `when` equal to 1 when the `max` of the
  two participants' `detector` equals 2: with the mark it fires and after
  tick 3 the outputs are at (7,6,7), 3, 5, 1, 3, 1, 2 and (7,8,7), 2, 5, 1,
  3, 1, 2 with one click recorded; without the mark the guard is false, no
  event is recorded and the rays cross: after tick 3 at (6,7,7), 1, 5, 3, 3,
  1, 0 and (8,7,7), 0, 5, 3, 3, 1, 0; 10 quanta and momentum (0,0,0) in both;
- (e) `parse_initial_state` rejects `on_bit_1: "maybe"`, `on_bit_0: 1`,
  `bit: "sometimes"`, `bit: {"of": 2}` on a two-role rule, `bit: {"of":
  -1}` and an assignment to `detector`; `validate_configuration` reports
  the same documents invalid; `DetectorMark` with `on_bit_1` 5 is rejected
  and a mark of four arguments equals one with the three defaults 0;
  `inherited_bit` gives 2 for (0, 2), 1 for (1, 0), 2 for (2, 1) by default,
  0 for (2, 1) under `BIT_NONE`, 1 for (2, 1) with rule 1, 0 for no inputs,
  and rejects a role index beyond the inputs and a bit of 3.

Pinned consequences in existing tests: none change. The worlds of
`test_detector_mark.py`, `test_detector_return.py` and
`test_inverse_split.py` write the same `events.jsonl` and `run.json` as
before the feature (no marked ray reaches a second mark or meets another
ray there); the worlds of `test_ray_viewer.py` and
`test_ray_meeting_conversion.py` differ in their recorded cost alone (one
more view component per participant, `read` 10 instead of 9), and
`test_wave_ray_families.py` pins `detector` as the eighth ray property.

## Ray polarization

`test_ray_polarization.py` builds its boards inline under the shared
Detector admission (schema 1, `link_ticks` 1, `metric: "links"`, pace 1/1,
no decay, the six unit-axial headings in Port order) on a periodic 15^3
lattice ([polarization](SPATIAL_FIELDS.md#polarization-ray-polarization-v1)).
The family `light` has an 8-step phase advancing 0 and, unless a case says
otherwise, `polarization_bits` 3: a polarization circle of eight steps per
half turn, 22.5 degrees each, step 0 the first transverse lattice axis of
the heading (+Y for a ray on +X) and step 4 the second (+Z); `apparatus` is
the polarizer body's family, its circle the default of its phase width,
eight steps too. Every lamp emits along +X or -X at phase 0, its whole
stock at once unless it holds several pulses; a polarizer body at (7,7,7)
has amount 1, its pass Port +X and the reference table `[8, 7, 4, 1, 0, 1,
4, 7]`, cos^2(d x 22.5 degrees) in eighths, rounded, its unpolarized share
the table's mean, 4. A tick n is one `step()`. Written before the first run,
from the rule of the section: an arriving ray of amount a and polarization
p at a body of angle theta passes floor(a x T[d] / 8) with polarization
theta and sinks floor(a x (8 - T[d]) / 8), d = (theta - p) mod 8, the two
shares below one quantum going to the body's pass and sink registers of the
ray's sign (units of 1/8), which release a whole quantum when they reach 8;
the pass ray is a fresh event of the body's Node on +X, resident there at
its arrival tick and one Link on at every later tick.

- (a) `lamp`: a lamp at (4,7,7) emits 8 along +X with `polarization` 2:
  after tick n the ray is at (4 + n, 7, 7), heading index 0, amount 8,
  phase 0, steps n, mask 1, shares (8, 0, 0, 0, 0, 0), polarization 2;
  totals light 8. Two lamps at (4,7,7) each emitting 4 along +X at
  polarization 2 are two identical events and merge: after tick 1 one ray
  of 8 at (5,7,7) with shares (4, 0, 0, 0, 0, 0) and polarization 2; at
  polarizations 2 and 6 they stay two rays of 4, the one at 2 first in
  merge order; with no `polarization` key both are unpolarized (-1) and
  merge. `merge_rays` over two rays of that event with amounts 3 and 5 at
  polarization 2 gives one of 8; with the 5 unpolarized, two rays, the
  unpolarized first;
- (b) `polarizer`: a lamp at (4,7,7) emitting `amount` per interval along
  +X at polarization 0 (along +Y) for `pulses` intervals, a polarizer at
  (7,7,7) of angle theta; the ray arrives at tick 3 and the pass ray of
  pulse k is at (10 - k, 7, 7) after tick 6 with steps 3 - k, mask 1, its
  amount as its share, phase 0, no bit, polarization theta. After tick 6:
  theta 0, one pulse of 8: 8 passed at (10,7,7), nothing sunk, totals
  light 8; theta 2 (45 degrees): 4 passed, sink light 4 (`external_body_totals`
  light 4); theta 4 (90 degrees): nothing passed, no ray anywhere, sink 8;
  theta 1 (22.5 degrees): 7 passed, sink 1; theta 1 with one pulse of 5:
  5 x 7 = 35 = 4 x 8 + 3, so 4 passed and 3/8 to the pass register, 5 x 1
  = 5 to the sink register, nothing sunk, the body's `held` [0, 0, 3, 5, 0,
  0] (sign-major -1, 0, 1, then pass, sink: the sign-0 pair holds one
  whole quantum), totals light 5 (4 on the ray and 1 held), sink empty;
  theta 1 with three pulses of 5 (a stock of 15): pulses at ticks 3, 4, 5
  give pass registers 3, 6, 9 -> 1 (a quantum released on the third) and
  sink registers 5, 10 -> 2 (a quantum sunk on the second), 7: after tick
  6 the pass rays are 4 at (10,7,7), 4 at (9,7,7) and 5 at (8,7,7) (the
  third pulse's 4 merged with the released 1, one event of 5), sink light
  1, `held` [0, 0, 1, 7, 0, 0], totals light 14; the three `polarizer`
  records (position (7,7,7), body 0, Port 1, `light`, amount 5,
  polarization 0, sign 0, angle 1, difference 1, share 7, steps 8) carry
  (tick, passed, sunk, held, released, registers) = (3, 4, 0, [3, 5], [0,
  0], [0, 0, 3, 5, 0, 0]), (4, 4, 0, [3, 5], [0, 1], [0, 0, 6, 2, 0, 0]),
  (5, 4, 0, [3, 5], [1, 0], [0, 0, 1, 7, 0, 0]), and one
  `external_body_absorbed` (tick 4, `light`, 1) books the released sink
  quantum. In every world the body's momentum stays (0, 0, 0), it never
  steps, and every accounting line balances at every tick. An unpolarized
  lamp of 8 at theta 1 passes the table's mean, 4, with polarization 1,
  sink 4, its record's polarization and difference `null` and share 4;
  `polarizer_share` at angle 1 gives (-1, 4) for none and (1, 7), (0, 8),
  (6, 4), (4, 0) for polarizations 0, 1, 3, 5. The runner records
  `ray_polarization: "ray-polarization-v1"`, the body's `coupling`
  `"polarizer"` with its declaration (`family` light, `angle` 1, `pass`
  [1, 0, 0], `steps` 8, `unpolarized` 4) and, for the one pulse of 5, a
  `final.held` of [0, 0, 3, 5, 0, 0], `external_body_totals` light [0],
  final light 5, `conserved_at_every_completed_tick` true;
- (c) `return`: theta 2 and a mark at (9,7,7) of setting 0/1 (every
  arrival returned): the pass ray of 4 reaches the mark at tick 5 and is
  returned, one `detector_return`; after tick 5 it is at (9,7,7) with
  heading index 1, steps 2, `outbound` 0, polarization 2, bit 1 (a draw of
  0), mask 1 and shares (4, 0, 0, 0, 0, 0); after tick 6 at (8,7,7) with
  steps 1; at tick 7 it reaches the polarizer's Node and ends in its sink
  as every returning ray at a body does: no ray anywhere, sink light 8,
  no `inverse_split`;
- (d) `meeting`: lamps of 5 at (5,7,7) (+X, polarization 1) and (9,7,7)
  (-X, polarization 3) meet at (7,7,7) at tick 2 under `meeting` (two
  `light` roles, outputs `{"of": 0}` on +Y and `{"of": 1}` on -Y with
  `input` 1). After tick 3 the outputs are at (7,8,7) (heading 2) and
  (7,6,7) (heading 3), 5 each, steps 1, with polarizations (1, 3) when the
  outputs declare none and when both declare `"same"`, (3, -1) for
  `{"of": 1}` and `"none"`, (5, 1) for the value 5 and `{"of": 0}`;
  totals light 10. The parsed rule's `polarization_declared` is false in
  the first two and true in the last two, and the cycle of (7,7,7) at
  tick 2 costs 4 more in the last two (one more view component per
  participant, one update per output) and the same in the first two. A
  guard `eq(polarization of participant 0, 1)` fires with lamp 0 at
  polarization 1 (the outputs as above with (1, 3)) and not at 2 (the rays
  cross: after tick 3 at (8,7,7), heading 0, steps 3, polarization 2 and
  (6,7,7), heading 1, steps 3, polarization 3), and marks the rule as
  naming the property;
- (e) `spread`: light with `spread` [6, 1, 1, 1, 1, 1]. A lamp of 11 at
  (4,7,7) along +X at polarization 2 spreads at (5,7,7) in the cycle of
  tick 1: after tick 2 fresh field rays of 6 at (6,7,7), 1 at (4,7,7) and
  1 on each transverse neighbour, steps 1, no event, every one at
  polarization 2. Lamps of 11 at (4,7,7) (+X, polarization 0) and (6,7,7)
  (-X, polarization 4, crossed) meet at (5,7,7) and spread as one content:
  7 at (6,7,7), 7 at (4,7,7), 2 on each transverse neighbour, every
  departure unpolarized (the axial sum of two equal crossed lines
  cancels); at polarizations 0 and 2 (45 degrees) every departure is at
  step 1 (22.5 degrees, the axial mean). Totals light 11 per lamp.
  `combined_polarization` over (5, 2), (3, 2) gives 2; (5, 0), (5, 4)
  gives -1; (5, 0), (5, 2) gives 1; two unpolarized terms -1; (5, none),
  (3, 6) gives 6; no terms -1;
- (f) `identity`: the lamp of (a) unpolarized, without `polarization_bits`,
  at a plain sink body at (7,7,7): the run record has no `ray_polarization`
  key, the body's entry no `polarizer` and its `final` no `held`, the sink
  light [8], and `events.jsonl` holds no `polarizer` record and the word
  `polarization` nowhere; the parsed light has a polarization modulus of 8
  (its phase width) and `polarization_declared` false. The same lamp with
  `polarization_bits` 3 on light records the identity; `polarization_bits`
  1 gives a modulus of 2;
- (g) `rejected`: `parse_initial_state` rejects an emission polarization 8
  or -2 at three bits ("from 0 below 8"), a polarizer without `angle`
  ("requires an angle"), a body with coupling `polarizer` and no
  declaration ("requires its polarizer declaration"), an angle of 8, a
  table of seven entries ("one entry per step"), an entry 9 ("from 0
  through 8"), a pass heading [1, 1, 0] ("unit-axial"), an unpolarized
  share 9, a polarizer of its own family ("other than its own"), a
  `polarizer` declaration under coupling `sink` ("requires coupling"),
  `polarization_bits` -1, an output `polarization` `{"of": 2}` on a
  two-role rule ("exceeds the declared roles"), 8 or `"left"` ("from 0
  below 8"), an assignment to `polarization` ("read-only") and
  `polarization_bits` on an outward field ("require ray transport");
  `validate_rays` rejects a ray at polarization 8 and `Polarizer` a table
  of seven entries and an angle of 8.

Pinned consequences in existing tests: none change. `test_wave_ray_families.py`
pins `polarization` as the ninth ray property. The byte-identity digests of
`test_ray_momentum_turn.py` (`identical`) and `test_field_spreading.py`
(`unchanged`) hold: a rule that does not name the property reads the view it
read before (`read` 10 per participant) and its outputs carry their source
input's polarization without an assignment, so the recorded costs of every
existing world are unchanged. `test_nature_catalog.py` runs the polarizer as
a decided coupling ([catalog of nature](#catalog-of-nature)).

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
  `record.released_field` is `released-field-v1`. Since 2026-09-17 (feature
  14, `loop-binding-v1`), the six-heading release of a held ray gone, a ray
  waiting under the coupling's `delay` releases the five headings other than
  its own like any ray: the tick-1 release sources G 10 (the four transverse
  spokes G 2, the +X and -X spokes G 1, one from each waiting ray, read as
  G rays of 2, 2, 2, 2, 1, 1), the tick-3 clicks are one G 1 (the +X G ray
  of the ray heading -X), the clicks are four, the field escapes are G 8,
  10, 10, 8 (the two axial packets of tick 1 carrying 1 each), the
  `source_totals` G 40, `escaped_totals` G 38 becomes 36, `in_world` G 0, 0,
  10, 12, 12, 12, 4, and tick 3's caption reads one Detector PASS and tick
  4's ends "field escaped: G 10"; everything else as pinned, at the first
  run on the new engine. The screen geometry test was deleted with the
  retired `screen.json` (E6). The first pin had one release at (2,1,1), at
  tick 2 only, from the released-field text ("in the interval it departs"):
  the first run showed the engine also releasing at tick 1, while both rays
  were held at (2,1,1) by the coupling's `delay`
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
- (h) the eye view (Highlights 5.4, "everything begins and is realized at
  a marked Node"): the run's `eye` block lists the marked Nodes (`marks`,
  (4,1,1) with setting 1/1) and every PASS click (`clicks`: the same five
  ticks, families and amounts as the click markers, each at (4,1,1) through
  Port -X with bit 1) and counts the hits per Node (`hits`: five at
  "4,1,1"); the page's eye view draws only these;
- (i) the screen example (`examples/nature/screen.json`, the eye view's
  demonstration of 2026-09-17 under Highlights 5.5, made once and never
  repeated as a test): the world file's integers are pinned, not its run:
  board [12, 11, 11], open, 24 ticks; two `electron` lamps of amount 4 at
  (0,5,5) heading +X and (2,5,5) heading -X; `light` the field of
  `electron` with release [1, 4]; seven Detector marks at (7, 2..8, 5),
  every one with setting [1, 1] and seed 0; one rule, `bind`, with
  `ray_delay` 1. The on-axis mark (7,5,5) is the one that clicks before
  feature 12;
- (j) the phone GIF preset (model owner, 2026-09-17: GIFs only, small enough
  for the phone): `motion.gif_preset` is `phone` and `gif_presets` holds
  `phone` and `full`; `phone` is 640 px wide, 480 px per panel side by
  side, at most 20 frames (24 left the two-panel GIF above the target), 12
  hold frames with the camera still (`gif_hold_still`), 128 colours,
  supersample 1, six seconds, a target of 1000000 bytes and no stills;
  `full` is uncapped, its hold turning on, supersample 2, 120 ms a frame,
  16 stills. The frame schedule of a 24-tick
  run capped at 24 frames is the ticks 0, 1, 3, 4, 6, 7, 8, 10, 11, 13, 14,
  16, 17, 18, 20, 21, 23, 24 and then six frames holding 24 (the run reaches
  its end, a quarter of the frames hold); an uncapped 6-tick run is 0..6 and
  twelve holds; 24 frames in six seconds is 250 ms a frame (the style's 120
  ms when no seconds are set). An unknown preset name, a preset with an
  unknown key and a `gif_preset` naming no preset are refused;
- (k) a tick cap (`extract_record(..., ticks=3)` on the six-tick fixture):
  the run's `ticks` is 3, `record.ticks_capped_from` is 6, no event is
  later than tick 3 and `ticks_data` has four rows; a cap at or above the
  recorded length (9) leaves `ticks_capped_from` None. The page's
  `page_text` gains `runs` and `eye_toggle`, both true by default (the run
  buttons for a document with several runs, the eye-view button for a run
  with marked Nodes);
- (g) external bodies (`external-body-v1`, pinned 2026-09-17 before the
  first run): a `run.json` listing one body of family `star`, amount 4096,
  coupling `sink`, field `G`, with `positions` rows (0, 7,7,7), (1, 7,7,7)
  and (2, 8,7,7), extracts to one body at (7,7,7) carrying those rows, so
  the page draws its picture (chosen by family in `style.json`, `star` by
  default) at (7,7,7) through tick 1 and at (8,7,7) from tick 2;
- (h) the ray's bit (`detector-bit-property-v1`, pinned 2026-09-17 before
  the first run): every ray of `runs.json` carries `bit`, `null` for none,
  0 or 1, set by a click, a pass or a Detector RETURN and inherited by the
  outputs of an event from its inputs (the highest); here rays 0 and 1 and
  the -X output carry `null` and the +X output, clicked at (4,1,1) at tick
  4, carries 1, and no event of kind `pass` exists, since no ray carrying a
  bit reaches a second mark;
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
  fixed colours for the families `electron`, `light`, `proton` and `neutron`,
  `draw.view` `board` (`eye` draws the marked Nodes and the PASS clicks alone,
  a flash of `click_flash_ticks` 4 sized by amount leaving a dim dot),
  `motion.gif_preset` `phone` ((j) above), of the `page_text` flags
  only `header` (the run's title), `tick_counter`, `runs` and `eye_toggle`
  true ((k) above), every `labels` flag false, and `autoplay` and `loop`
  true.

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
and the table `spread: [6, 1, 1, 1, 1, 1]`, total S = 11: forward 6/11,
backward 1/11, each transverse 1/11. Every lamp holds its amount and emits
it, funded and directed, with its recoil into the lamp's `momentum` field,
so the `momentum` total is the lamps' recoils plus the rays' amount x
heading and the `momentum` source is what the spreads moved. The Node owns
the sub-quantum remainder (`field-remainder-v1`, Highlights 3.5 and 3.17,
model owner, 2026-09-17): a `field_spread` record carries `arrived` (per
heading), `amounts` (departures per Port, the register releases included),
`released` (per Port, from the registers), `stored` (the whole quanta the
registers gained net of releases), `registers` and `register_phases`
(eighteen each, sign-major -1, 0, 1 then Port, in units of 1/11), `phase`,
`coherence` and `signs`; the snapshot's `field_remainders` lists every
nonzero block. `relative_ports` gives (0, 1, 2, 3, 4, 5) for Port 0 and
(3, 2, 0, 1, 4, 5) for Port 3. The test is parametrized over `single`,
`superposition`, `cancelled`, `stream`, `sign`, `returned`, `source`,
`resident`, `rejected` and `unchanged`. Pinned before the first run:

- (a) `single`: a lamp at (5,7,7) emits 12 along +X at phase 6, four ticks.
  After tick 1 the ray is at (6,7,7) (heading 0, amount 12, phase 6, steps
  1, mask 1, shares (12, 0, 0, 0, 0, 0)). The spread at (6,7,7) in the
  interval of tick 2 (the record of tick 1): 12 x 6 = 72 = 6 x 11 + 6, so 6
  leave forward and 6/11 stay; 12 x 1 = 12 = 11 + 1 on each other heading,
  so 1 leaves and 1/11 stays: `amounts` (6, 1, 1, 1, 1, 1), `released` all
  zero, `stored` 1, `registers` of sign 0 (6, 1, 1, 1, 1, 1) at phase 6,
  `coherence` [1, 1]. After tick 2 the rays are (7,7,7) heading 0 amount 6,
  (5,7,7) 1 1, (6,8,7) 2 1, (6,6,7) 3 1, (6,7,8) 4 1, (6,7,6) 5 1, each
  phase 6, steps 1, no event, and (6,7,7) holds one quantum in its
  registers. In the interval of tick 3 (six records of tick 2, in position
  order): (5,7,7) arrived (0, 1, 0, 0, 0, 0) sends nothing and stores 1,
  registers (1, 6, 1, 1, 1, 1); (6,6,7), (6,7,6), (6,7,8) and (6,8,7) the
  same with the 6 on their own heading's Port; (7,7,7) arrived (6, 0, 0, 0,
  0, 0) sends (3, 0, 0, 0, 0, 0) and stores 3, registers (3, 6, 6, 6, 6, 6).
  After tick 3 the one ray is (8,7,7) heading 0 amount 3 and the registers
  hold 9 quanta. In the interval of tick 4 (one record, at (8,7,7)): arrived
  (3, 0, 0, 0, 0, 0) sends (1, 0, 0, 0, 0, 0) and stores 2, registers (7, 3,
  3, 3, 3, 3); after tick 4 the one ray is (9,7,7) heading 0 amount 1 and
  the registers hold 11 quanta at eight Nodes. The light total is 12 at
  every tick with source 0; the rays' momentum after ticks 1 to 4 is (12, 0,
  0), (5, 0, 0), (3, 0, 0), (1, 0, 0) and the lamp's recoil (-12, 0, 0), so
  the `momentum` total is (0, 0, 0), (-7, 0, 0), (-9, 0, 0), (-11, 0, 0) and
  equals `source_totals` at every tick; eight records in all; the spatial
  accounting balances and the local audit passes. The runner records
  `field_spreading: "field-spreading-v1"`, `field_remainder:
  "field-remainder-v1"`, `spreading_fields` `[{"field": "light", "spread":
  [6, 1, 1, 1, 1, 1]}]`, eight `field_spread` records,
  `conserved_at_every_completed_tick` true, `local_conservation` passed,
  final totals `light` [12] and `momentum` [-11, 0, 0], `source_totals`
  `momentum` [-11, 0, 0], and `field_remainders` with eight entries in its
  final state;
- (b) `superposition` and `cancelled`: lamp 0 at (5,7,7) emits 23 along +X
  at phase 0 and lamp 1 at (7,7,7) emits 23 along -X at phase 6
  (`superposition`) or 4 (`cancelled`), two ticks. Both rays arrive at
  (6,7,7) at tick 1, where the coherent stock a reader sees
  (`spatial_values`) is 23 (coherence 1/2) or 0 (coherence 0/1). The spread
  in the interval of tick 2 combines them: `amount` 46, `arrived` (23, 23,
  0, 0, 0, 0), the phase of the coherent sum 7 (`superposition`) or 0
  (`cancelled`, a cancelled sum); each heading's 23 gives 23 x 6 = 138 = 12
  x 11 + 6 forward and 23 = 2 x 11 + 1 on each other heading: `amounts`
  (14, 14, 4, 4, 4, 4), `released` zero, `stored` 2, `registers` of sign 0
  (7, 7, 2, 2, 2, 2) at the combined phase. After tick 2 the rays are at
  (7,7,7) heading 0, (5,7,7) heading 1, (6,8,7) heading 2, (6,6,7) heading
  3, (6,7,8) heading 4 and (6,7,6) heading 5 with those amounts, the
  combined phase, steps 1 and no event; the light total is 46 (44 in rays,
  2 in the registers), the `momentum` total (0, 0, 0) equal to the source
  in both cases;
- (c) `stream`: a lamp at (5,7,7) holding 12 emits 1 along +X at phase 0
  every interval, twelve ticks, so one quantum arrives at (6,7,7) at every
  tick 1 to 12. A ray of amount 1 fills the forward register by 6/11 per
  arrival and the backward and transverse ones by 1/11: in the interval of
  tick n + 1 (the record of tick n) the forward register of (6,7,7) reads,
  after the release it triggers, 6, 1, 7, 2, 8, 3, 9, 4, 10, 5, 0 for n = 1
  to 11 and the five others n for n up to 10 and 0 at 11; the second quantum
  releases forward after two arrivals, again after 4, 6, 8, 10 and 11
  arrivals, and a backward or transverse quantum leaves after eleven, so the
  record of tick n has `released` (1, 0, 0, 0, 0, 0) at n = 2, 4, 6, 8, 10,
  (1, 1, 1, 1, 1, 1) at n = 11 and zero otherwise, `stored` 1 at odd n
  below 11, 0 at even n and -5 at 11, and `amounts` equal to `released`.
  The forward quanta reach (7,7,7) at ticks 3, 5, 7, 9, 11, 12 and fill its
  registers the same way, releasing forward in the intervals of ticks 6 and
  10; (8,7,7) releases in the interval of tick 11; nineteen records in all.
  After tick 12 the rays are (6,7,7) heading 0 (the twelfth emission, mask
  1), (7,7,7) 0, (5,7,7) 1, (6,8,7) 2, (6,6,7) 3, (6,7,8) 4, (6,7,6) 5
  (the six released in the interval of tick 12), each amount 1, phase 0,
  steps 1, and the registers hold (8, 5, 5, 5, 5, 5) at (7,7,7), (1, 2, 2,
  2, 2, 2) at (8,7,7) and (6, 1, 1, 1, 1, 1) at (9,7,7), none at (6,7,7):
  7 quanta in rays and 5 in registers, the lamp empty. The light total is
  12 and the ledger balanced at every tick; the local audit passes;
- (f) `sign`: an electron lamp at (5,7,7) (family `electron`, charge -3,
  rest rate 1) emits 4 along +X at phase 0; `light` is its field at
  `release: [1, 4]` with the table; three ticks. The electron is at (8,7,7)
  after tick 3 (heading 0, amount 4, phase 3, steps 3, mask 1). It releases
  five light rays of 1 at (6,7,7) in the interval of tick 2 (phase 1) and at
  (7,7,7) in the interval of tick 3 (phase 2), every one with `source_sign`
  -1, the sign of the electron's charge. In the interval of tick 3 the five
  rays of phase 1 enter the registers of sign -1 of the Nodes around
  (6,7,7), 6/11 on their own heading and 1/11 on the others (the records of
  tick 2 carry `signs` (-1,) and `stored` 1), so after tick 3 the rays on
  the board are the five of phase 2 at (6,7,7) heading 1, (7,8,7) 2,
  (7,6,7) 3, (7,7,8) 4 and (7,7,6) 5, amount 1, steps 1, sign -1, and the
  registers of sign -1 hold one quantum at each of (5,7,7) (1, 6, 1, 1, 1,
  1), (6,8,7) (1, 1, 6, 1, 1, 1), (6,6,7) (1, 1, 1, 6, 1, 1), (6,7,8) (1,
  1, 1, 1, 6, 1) and (6,7,6) (1, 1, 1, 1, 1, 6), at phase 1; light 10 with
  source 10, electron 4 with source 0. `release_field` on the electron's
  ray gives the five rays with sign -1; `merge_rays` keeps a ray of sign 1
  and one of sign -1 on one line as two rays; `spread_content` over 3 of
  sign 1 and 3 of sign -1 arriving on +X at phase 0 with empty registers
  sends 1 forward per sign (3 x 6 = 18 = 11 + 7) and stores 2 per sign, a
  record with `arrived` (6, 0, 0, 0, 0, 0), `amounts` (2, 0, 0, 0, 0, 0),
  `released` zero, `stored` 4, the registers (7, 3, 3, 3, 3, 3) for each
  sign and `signs` (-1, 1); and over one ray of amount 1 on +X with the
  forward register of sign 0 at 10 it releases one quantum forward, the
  register left at 5, the others at 1, `released` (1, 0, 0, 0, 0, 0) and
  `stored` 0; `transmit` in `siblings` mode of a returned ray of sign -1 on
  -X (mask 3, shares (2, 2, 0, 0, 0, 0), amount 2) gives one transmission
  of 2 on -X with sign -1;
- (g) `returned` (the orchestrator's proposal of Highlights 5.5, pending the
  model owner's decision): a lamp at (5,7,7) holding 2 emits 1 along +X at
  phase 0 in each of the intervals of ticks 1 and 2, a Detector at (7,7,7)
  with setting 0/1 (every draw 0), six ticks. After tick 1 the first
  quantum is at (6,7,7) (emitted, mask 1); in the interval of tick 2 it
  enters the registers of (6,7,7), (6, 1, 1, 1, 1, 1), and the second
  quantum arrives; in the interval of tick 3 the second fills the forward
  register to 12 and one quantum is released forward, the registers left at
  (1, 2, 2, 2, 2, 2): at tick 3 it arrives at the Detector and is returned,
  at (7,7,7) heading 1, outbound 0, steps 1, Detector bit 0; after tick 4
  at (6,7,7) with steps 0, where it neither rests nor performs an inverse
  split; after tick 5 at (5,7,7); in the cycle of tick 5 the lamp, the
  record that emitted the family, takes it back: after tick 6 no light ray
  is on the board, the lamp holds light 1 and momentum (-1, 0, 0), and the
  registers of (6,7,7) hold one quantum. The light total is 2 at every tick
  with source 0; the `momentum` total is (0, 0, 0) after tick 1 and (-1, 0,
  0) from tick 2, equal to the source (the first spread stored a quantum
  that carried +1); the records are `field_spread` at ticks 1 and 2 at
  (6,7,7), `detector_return` at tick 3 and `field_returned` at tick 5
  (position (5,7,7), family light, amount 1, port 1, by none, restored
  true); the local audit passes and the runner's ledger is exact with final
  totals light [2] and momentum [-1, 0, 0];
- (h) `source` (the same proposal): a record holding 4 electrons at (5,7,7)
  with no emission (its Node cycles for the release, (i)), `light` its
  field at `release: [1, 4]` with the table, the Detector at (8,7,7) with
  setting 0/1, twelve ticks. Every interval the record releases six light
  quanta (1 per heading, phase 0, sign -1); at each neighbour they fill the
  registers as in (c), so (6,7,7) releases forward in the intervals of
  ticks 3, 5, 7, 9, 11 and 12, (7,7,7) in the intervals of ticks 6 and 10,
  and the Detector returns a quantum at ticks 6 and 10. The first returned
  quantum walks back to (5,7,7) at tick 9, where the cycle of tick 9 ends
  it at the record, content of the family the field is the field of, its
  release unbooked as a negative source (`field_returned` of tick 9, port
  1, by `electron`, restored false); nothing reaches an open face in twelve
  ticks. After tick t the light total and source are 6t, less 1 from tick
  10, escaped 0, the ledger balanced at every tick; after tick 12 the
  registers of sign -1 at (7,7,7) hold (8, 5, 5, 5, 5, 5); the local audit
  passes;
- (i) `resident` (a defect fixed on 2026-09-17: a record holding stock of a
  family with a released field released nothing, because the Node's cycle
  returned early as idle before the release; `plan_cycle` now cycles for
  it): a record holding 8 electrons at (5,7,7) with no emission, `light` its
  field at `release: [1, 4]` with the table, four ticks. Every interval the
  record releases six light rays of floor(8 x 1 / 4) = 2, phase 0, sign -1,
  booked as a source, twelve per interval. At a Node beside the record, 2
  gives 2 x 6 = 12 = 11 + 1 forward, so 1 leaves and 1/11 stays, and 2/11
  on each other heading: one quantum on to the next Node and one into the
  registers per arrival; at the next Node the 1 fills the registers and the
  forward one releases at the second arrival. After tick t the light total
  and source are 12t, the electron total 8 with source 0 and the record
  unchanged; after tick 4 the rays are one of 2 at distance 1 on each of
  the six lines, one of 1 at distance 2 and one of 1 at distance 3, phase 0,
  steps 1, sign -1, no event, and the registers of sign -1 hold (3, 6, 6, 6,
  6, 6) at (6,7,7) (the 3 on the arriving heading's Port at each distance-1
  Node) and (1, 2, 2, 2, 2, 2) at (7,7,7) (likewise at distance 2): 24
  quanta in rays and 24 in registers; the ledger is balanced at every tick
  and the local audit passes;
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
  both taken on main `f3809be` before feature 12 (final totals `G` 16 and
  `electron` 5, `G` 9 escaped), and its run record carries no
  `field_spreading` key. Since 2026-09-17 (feature 14, `loop-binding-v1`)
  the `state.json` digest is `026ac5ed...`, the snapshot having lost the
  empty `bound_groups` key; `events.jsonl` is unchanged.

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

**Since 2026-09-17 (feature 14, `loop-binding-v1`).** The held form was
removed ([binding as a loop](SPATIAL_FIELDS.md#binding-as-a-loop-loop-binding-v1)),
so the cases `binding`, `unbinding` and `ray_delay` below are deleted and
the test is parametrized over `gravity` and `criterion` alone, with the
mass no longer a held pair but resident content: one record `mass` at
(10,10,10) holding 16 of `n` and emitting nothing, whose stock releases
floor(16 / 4) = 4 of `G` on every heading every interval from the cycle of
tick 0, with phase 0 (released-field-v1, "resident content"); the two `n`
lamps and `bind` are gone. The lines of (d) and (e) hold with three
changes, pinned before the first run on the new engine: the G total and
source after tick t are 24 t (24, 48, ..., 264 after tick 11, the first
releases of the cycle of tick 0 escaping at tick 11, so the G total plus
the G escaped equals the source); the G ray met at (10,14,10) after tick 6
and the recoil have phase 0, not 2 (a record releases with phase 0); and in
(e) the G total after tick 8 is 192, the mass M = N / 4 being the
criterion's fraction rather than a sum of rates. The `n` total is 16 as
before. The text of (a) to (c) stays below for the record of what the held
form was.

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

## Bound group motion (deleted on 2026-09-17)

`test_bound_group_motion.py` was deleted on 2026-09-17 with
`bound-group-motion-v1` by feature 14, `loop-binding-v1`
([binding as a loop](SPATIAL_FIELDS.md#binding-as-a-loop-loop-binding-v1)):
a bound group is rays in motion on a ring, and its motion as a whole is its
corners shifting, which is open. The pins below stay for the record of what
the register-driven motion was.

`test_bound_group_motion.py` built its boards inline under the shared
Detector admission (schema 1, `link_ticks` 1, `metric: "links"`, pace 1/1,
no decay, the six unit-axial headings in Port order) on an open 21^3 lattice
([bound group motion](SPATIAL_FIELDS.md#bound-group-motion-bound-group-motion-v1)).
The family `n` has rest rate 1 on a 3-bit phase (8 steps), 8 ray slots; `G`,
where declared, is its field, `field_of: "n"` with `release: [1, 4]`, rate 0,
16 ray slots; `f` is a plain family of rate 0 (the field ray of (c) with no
release around it). A vector field `momentum` (three signed components) is
bound to every ray family through `recoil_field` on every emission, so the
world ledger carries a momentum line and every lamp keeps the recoil of what
it emits. Every lamp holds its amount and emits it once, funded and directed,
at phase 0, in the cycle of tick 0. The binding rule `bind` is `n x n`
without outputs, assigning `delay` 1 to both participants, invariant energy,
with `"momentum_table": {family: -1}` where a case says so. A tick t is one
`step()`: the cycle of interval t - 1 and the delivery of tick t; a record
carries the tick its cycle started at. The test is parametrized over
`uniform`, `push`, `escape`, `rest` and `rejected`. Pinned before the first
run:

- (a) `uniform`: lamps at (9,10,10) and (11,10,10) emit `n` 6 along +X and
  `n` 2 along -X; the rays meet at the center (10,10,10) after tick 1
  (headings 0 and 1, phase 1, steps 1). The cycle of tick 1 forms the group:
  register (4, 0, 0) (6 x (1,0,0) + 2 x (-1,0,0)), accumulators (0, 0, 0),
  content 8, one event on both Ports (mask 3, shares (6, 2, 0, 0, 0, 0)).
  From the cycle of tick 2 the accumulator x adds 4 per interval: 4 after
  the cycle of tick 2, 8 in the cycle of tick 3, a step through Port 0 with
  the accumulator back to 0, and so on: the group steps in the cycles of
  ticks 3, 5, 7, 9 and 11 (`bound_group_step` at those ticks, Port 0,
  arrival ticks 4, 6, 8, 10, 12, momentum (4, 0, 0), accumulators (0, 0, 0),
  content 8), one Link every two intervals, speed 1/2. After tick t (2 to
  12) the group is at (10 + floor((t - 2) / 2), 10, 10) with accumulators
  (4 x ((t - 2) mod 2), 0, 0), its rays at steps 0, delay 0, phases t mod 8
  (advanced once per interval by the rest rate on the move as at rest),
  mask 3 and shares (6, 2, 0, 0, 0, 0); the snapshot's `bound_groups` is
  that one entry with `momentum` (4, 0, 0). `bound_tick` is published at
  every tick 2 to 11, at the Node the group was at (ticks 2 and 3 at
  x = 10, 4 and 5 at x = 11, ..., 10 and 11 at x = 14). The held 6-ray
  releases G of amount floor(6 / 4) = 1 per heading (the 2-ray releases
  0), six headings in a resting interval and five in a stepping one (not
  +X, its line ahead): G sourced after tick t is 6 (t - 1) - floor((t - 2)
  / 2) for t from 2 (6, 12, 17, 23, 28, 34, 39, 45, 50, 56, 61), the six
  rays of the cycle of tick 1 escaping at tick 12 (current 55, escaped 6).
  `n` stays 8. The momentum line reads (0, 0, 0) initial, sourced and
  current at every tick, the lamps holding (-6, 0, 0) and (2, 0, 0) against
  the register (4, 0, 0); every ledger balances, and the runner's
  `conserved_at_every_completed_tick` is true with `bound_group_motion:
  "bound-group-motion-v1"`;
- (b) `push`: lamps at (9,10,10) and (11,10,10) emit `n` 4 along +X and
  along -X (a head-on pair at rest, register (0, 0, 0), content 8), and a
  lamp at (5,10,10) emits a `G` ray of amount 2 along +X, the field ray from
  the -X side; `bind` declares `momentum_table` `{"G": -1}`. The G ray is
  at (5 + t, 10, 10) after tick t and resident at the center after tick 5
  (steps 5, mask 1, shares (2, 0, 0, 0, 0, 0)). In the cycle of tick 5 the
  rule fires and the table meets it: the register becomes (-2, 0, 0) (-1 x
  2 x (1, 0, 0), toward the source) with accumulators (0, 0, 0), and the G
  ray returns reversed as a new event: heading 1, amount 2, phase 0, mask
  2, shares (0, 2, 0, 0, 0, 0), at (15 - t, 10, 10) after tick t from 6
  with steps t - 5. The accumulator x then adds -2 per interval and reaches
  -8 in the cycles of ticks 9 and 13: the group steps through Port 1 at
  those ticks (`bound_group_step`, momentum (-2, 0, 0), accumulators
  (0, 0, 0), content 8, arrival ticks 10 and 14), one Link every four
  intervals toward the source, speed 1/4. After tick t (6 to 14) the group
  is at (10 - floor((t - 6) / 4), 10, 10) with accumulators (-2 x ((t - 6)
  mod 4), 0, 0). The momentum line: sourced (-6, 0, 0) after tick 6 (the
  reversal of the G ray, -4, and the push, -2), then +2 at each stepping
  cycle (the release skips -X, two rays of amount 1 merged): (-4, 0, 0)
  after tick 10, (-2, 0, 0) after tick 14; the current line equals it at
  every tick (the lamps (-4, 0, 0), (4, 0, 0), (-2, 0, 0), the register and
  the rays), every ledger balanced. G: initial 2 (the lamp's stock), 12
  released per cycle from the cycle of tick 1 (2 per heading), 10 in a
  stepping cycle, the six rays of a resting cycle at the center escaping
  together from tick 12 (12 per tick): current after tick t is 2 + 12 (t -
  1) - 2 [t >= 10] - 2 [t >= 14] - 12 max(0, t - 11), that is 118 after
  tick 14, escaped momentum (0, 0, 0) through tick 14;
- (c) `escape`: lamps at (17,10,10) and (19,10,10) emit `n` 4 along +X and
  along -X, meeting at (18,10,10) after tick 1, and a lamp at (20,10,10)
  emits an `f` ray of amount 3 along -X; no G; `bind` declares
  `momentum_table` `{"f": -1}`. The f ray is resident at the group's Node
  after tick 2, and the cycle of tick 2 pushes the group to (3, 0, 0)
  (toward the +X side it came from) and returns the f ray reversed
  (heading 0, amount 3, mask 1, shares (3, 0, 0, 0, 0, 0)): at (19,10,10)
  after tick 3, (20,10,10) after tick 4, escaped at tick 5. The
  accumulator x adds 3 per interval over content 8 from the cycle of tick
  3 (the step decision of the push cycle reads the register before the
  push): 3, 6, 9 -> step (cycle of tick 5, accumulator 1), 4, 7, 10 -> step
  (cycle of tick 8, accumulator 2), 5, 8 -> step (cycle of tick 10,
  accumulator 0), that is 0, 0, 3, 6, 1, 4, 7, 2, 5 after ticks 2 to 10; the
  group is at (18,10,10) through tick 5, (19,10,10) through tick 8,
  (20,10,10) through tick 10, and the step of the cycle of tick 10 leaves
  the world: `spatial_escaped` at tick 11 from (20,10,10), Port 0, escaped
  `n` (8,) and `momentum` (3, 0, 0), `bound_group` families `["n", "n"]`,
  amounts `[4, 4]`, content 8, momentum (3, 0, 0); `bound_groups` empty
  after tick 11. Escaped totals after tick 11: `n` 8, `f` 3, momentum
  (6, 0, 0) (the f ray's 3 and the group's 3); sourced momentum (9, 0, 0)
  from tick 3 (the reversal 6 and the push 3); current (3, 0, 0) after tick
  11, the lamps' recoil; every ledger balanced, the runner's flag true;
- (d) `rest`: the head-on pair of `ray-binding-v1` (8 and 8 at (9,10,10)
  and (11,10,10), no table) for 6 ticks: register (0, 0, 0) and
  accumulators (0, 0, 0) at every tick, the group at the center, no
  `bound_group_step` record, `bound_tick` at ticks 2 to 5 with exactly the
  keys of `ray-binding-v1`, the runner writing no `bound_group_motion`
  key: byte for byte the events and run record of the feature 8 case, the
  snapshot's entries carrying the two zero vectors;
- (e) `rejected`: a `momentum_table` on a rule with outputs, one naming a
  participant family, one naming an unknown family, a sign of 2 and a table
  on a rule that assigns no delay are each rejected at initialization.

## A free ray turns by momentum

`test_ray_momentum_turn.py` builds its boards inline under the shared
Detector admission (schema 1, `link_ticks` 1, `metric: "links"`, pace 1/1,
no decay, the six unit-axial headings in Port order) on an open 21^3 lattice
([a free ray turns by momentum](SPATIAL_FIELDS.md#a-free-ray-turns-by-momentum-ray-momentum-turn-v2)).
The family `m` has rest rate 1 on a 3-bit phase (8 steps); `f` is a plain
family of rate 0, the field ray, with no release around it; both have 8 ray
slots. A vector field `momentum` (three signed components) is bound to both
through `recoil_field` on every emission, so the world ledger carries a
momentum line and every lamp keeps the recoil of what it emits. Every lamp
holds its amount and emits it once, funded and directed, at phase 0, in the
cycle of tick 0. The coupling `turn` is `m x f` without outputs and without
assignments, with `"momentum_table": {"f": sign}`: the table names the
field family, and `m`, the one role it does not name, is the ray it pushes.
A tick t is one `step()`: the cycle of interval t - 1 and the delivery of
tick t; a record carries the tick its cycle started at. The test is
parametrized over `turn`, `cancel`, `steep`, `identical` and `rejected`.
Pinned before the first run:

- (a) `turn`: a lamp at (4,10,10) emits `m` 8 along +X and a lamp at
  (10,4,10) emits `f` 2 along +Y, the field ray from the -Y side; `turn`
  declares `{"f": -1}`. After tick t (1 to 6) the m ray is at (4 + t, 10,
  10) with phase t mod 8, steps t, mask 1, shares (8, 0, 0, 0, 0, 0), no
  register, and the f ray at (10, 4 + t, 10) with phase 0, steps t, mask 4,
  shares (0, 0, 2, 0, 0, 0); both are resident at the center (10,10,10)
  after tick 6. In the cycle of tick 6 the coupling fires: the push is -1 x
  2 x (0, 1, 0) = (0, -2, 0), toward the source, and the register becomes
  (8, 0, 0) + (0, -2, 0) = (8, -2, 0), the accumulators (0, 0, 0), kept
  from the walk on the line (zero on a unit-axial heading; `ray-momentum-turn-v2`); the
  amount, phase, steps, heading index 0, mask and shares are untouched, and
  no event is stamped; `ray_push` at tick 6 at the center: family `m`,
  amount 8, before (8, 0, 0), after (8, -2, 0), field `f`, field amount 2,
  field heading (0, 1, 0). The f ray returns reversed as a new event:
  heading 3, amount 2, phase 0, mask 8, shares (0, 0, 0, 2, 0, 0), at (10,
  16 - t, 10) after tick t from 7 to 16 with steps t - 6, escaping through
  Port 3 at tick 17 (escaped `f` 2, momentum (0, -2, 0)). The m ray walks
  the DDA on (8, -2, 0), Manhattan length 10, one Link per interval: the
  accumulators add (8, 2, 0), the axis furthest ahead steps and loses 10,
  so from (0, 0, 0) the Ports are 0, 0, 3, 0, 0 and repeat (x x y x x, four
  +X per one -Y over ten Links), the accumulators after each step (-2, 2,
  0), (-4, 4, 0), (4, -4, 0), (2, -2, 0), (0, 0, 0). Positions after ticks
  7 to 18: (11,10,10), (12,10,10), (12,9,10), (13,9,10), (14,9,10),
  (15,9,10), (16,9,10), (16,8,10), (17,8,10), (18,8,10), (19,8,10),
  (20,8,10), the ray with register (8, -2, 0), phase t mod 8, steps t and
  its lamp's event record at every tick. The momentum line: initial
  (0, 0, 0); sourced (0, 0, 0) through tick 6 and (0, -6, 0) from tick 7
  (the push, -2, and the reversal of the f ray, -4, booked as the
  meeting's momentum change); escaped (0, -2, 0) from tick 17; current
  (0, -6, 0) from tick 7 and (0, -4, 0) from tick 17 (the lamps (-8, 0, 0)
  and (0, -2, 0), the m ray's register, the f ray's -2 while on the board);
  every ledger balanced, `m` 8 and `f` 2 throughout (`f` 0 and escaped 2
  from tick 17), the runner's `conserved_at_every_completed_tick` true with
  `ray_momentum_turn: "ray-momentum-turn-v2"` and no `bound_group_motion`
  key; final totals `m` 8, `f` 0, momentum (0, -4, 0);
- (b) `cancel`: the lamps of (a) and a third lamp at (12,18,10) emitting `f`
  2 along -Y, the field ray from the +Y side, `{"f": -1}`, 14 ticks. The
  first push at tick 6 is that of (a): after ticks 7 and 8 the m ray is at
  (11,10,10) and (12,10,10) with register (8, -2, 0) and accumulators
  (-2, 2, 0), (-4, 4, 0). The second f ray is at (12, 18 - t, 10) after
  tick t (heading 3, mask 8, shares (0, 0, 0, 2, 0, 0)) and resident with
  the m ray at (12,10,10) after tick 8: in the cycle of tick 8 the push is
  -1 x 2 x (0, -1, 0) = (0, 2, 0) and the register (8, 0, 0), the default
  amount x heading, so it is cleared and the accumulators reset: from tick
  9 the m ray is at (4 + t, 10, 10) with no register, accumulators
  (0, 0, 0), phase t mod 8, steps t, mask 1, shares (8, 0, 0, 0, 0, 0),
  the ray it was; `ray_push` at tick 8 at (12,10,10): before (8, -2, 0),
  after (8, 0, 0), field heading (0, -1, 0). The second f ray returns
  reversed (heading 2, mask 4, shares (0, 0, 2, 0, 0, 0)) at (12, t + 2,
  10) after tick t from 9 with steps t - 8; the first recoil as in (a).
  The momentum line: sourced (0, -6, 0) after ticks 7 and 8, (0, 0, 0)
  from tick 9 (the second push +2 and the second reversal +4), current the
  same, nothing escaped through tick 14; `m` 8 and `f` 4 throughout; final
  totals `m` 8, `f` 4, momentum (0, 0, 0);
- (c) `steep`: a lamp at (4,10,10) emits `m` 2 along +X and a lamp at
  (10,4,10) emits `f` 3 along +Y, `{"f": 1}` (repulsion, away from the
  source), 16 ticks. In the cycle of tick 6 the push is 1 x 3 x (0, 1, 0) =
  (0, 3, 0) and the register (2, 3, 0), past 45 degrees; `ray_push` at tick
  6: before (2, 0, 0), after (2, 3, 0), field heading (0, 1, 0). The DDA on
  (2, 3, 0), length 5, from (0, 0, 0): the Ports 2, 0, 2, 0, 2 and repeat
  (y x y x y, three +Y per two +X), the accumulators after each step
  (2, -2, 0), (-1, 1, 0), (1, -1, 0), (-2, 2, 0), (0, 0, 0). Positions after
  ticks 7 to 16: (10,11,10), (11,11,10), (11,12,10), (12,12,10),
  (12,13,10), (12,14,10), (13,14,10), (13,15,10), (14,15,10), (14,16,10);
  the ray keeps heading index 0 (+X, its line for the rules that read it)
  while `ray_line` reads (0, 1, 0), the dominant axis of its register, the
  line the release geometry skips. The recoil (heading 3, amount 3, mask
  8, shares (0, 0, 0, 3, 0, 0)) is at (10, 16 - t, 10) after tick t from
  7. The momentum line: sourced (0, -3, 0) from tick 7 (the push +3 and the
  reversal -6), current the same, nothing escaped; `m` 2 and `f` 3
  throughout;
- (d) `identical`: two worlds without a momentum table on a coupling of
  free rays run byte for byte as before this feature: the lamps of (a)
  under the outputs meeting `deflect` of `released-field-v1` (the m ray
  leaves on the field ray's heading, the f ray reversed), 12 ticks, and the
  bound group of `bound-group-motion-v1` (lamps at (9,10,10) and (11,10,10)
  emitting `m` 4 along +X and -X, a lamp at (5,10,10) emitting `f` 2 along
  +X, the binding rule with `{"f": -1}`), 14 ticks. The SHA-256 digests of
  `events.jsonl` and `state.json`, computed on the source before the
  feature (main `c21e03e`), are pinned in the test (`IDENTICAL`); no
  `ray_push` record and no `ray_momentum_turn` key, every ledger balanced.
  Since 2026-09-17 (feature 14, `loop-binding-v1`) the bound group world
  is gone with the held form and only the `meeting` world remains, its
  `events.jsonl` digest unchanged and its `state.json` digest re-pinned
  (`d824629b...`), the snapshot having lost the `bound_groups` key;
- (e) `rejected`: a table naming a participant family on a rule that
  assigns (`delay` 1) or declares `ray_delay` (both since 2026-09-17 the
  held form removed by `loop-binding-v1`, rejected with a message naming
  the migration note), a table with two unnamed roles (`m x m x f`), a
  sign of 2, and a rule with neither assignments, outputs nor table are
  each rejected at initialization; a role that mixes
  a named and an unnamed family gives `turn_receiver` no receiver (-1, the
  admission's refusal); and a push that would leave a ray with no
  direction fails the cycle: `m` 2 along +X from (4,10,10) meets `f` 2
  along -X from (16,10,10) at the center after tick 6 under `{"f": 1}`,
  the push 1 x 2 x (-1, 0, 0) = (-2, 0, 0) would make the register
  (0, 0, 0), and the seventh `step()` raises ("cannot stop a ray").

## The walk kept through a push

`test_momentum_turn_walk.py` is the test of `ray-momentum-turn-v2`
([a free ray turns by momentum](SPATIAL_FIELDS.md#a-free-ray-turns-by-momentum-ray-momentum-turn-v2),
"a push keeps the walk"), the fix the helium-orbit run
([E8](EXPERIMENTS.md#e8-the-helium-ion-with-the-field-spreading-and-the-momentum-turn))
asked for: a push moves the register and keeps the DDA's three
accumulators, the momentum-intervals each axis has banked toward its next
Link, so that under a push at every interval the ray walks the DDA line of
its running register. The DDA per interval: every axis adds the register's
component (its absolute value), the axis furthest ahead steps and loses the
register's Manhattan length, ties to the lowest axis; a push before the
departure moves the register and leaves the accumulators as they are. Two
cases walk the engine's own functions (`pushed_ray`, then `advance_ray` on
`ray_vector`, the order of the Node cycle) from (0, 0, 0); two build a
board. Every integer below is computed by hand from the rule and pinned
before the first run. The test is parametrized over `running`, `kept`,
`board` and `board_8`.

- (a) `running`: a ray of amount 64 heading +X, the default register
  (64, 0, 0), pushed by (0, 1, 0) before every departure has the register
  (64, t, 0) at its t-th Link, of Manhattan length 64 + t. From (0, 0, 0)
  the accumulators after Links 1 to 8 are (-1, 1, 0), (-3, 3, 0),
  (-6, 6, 0), (-10, 10, 0), (-15, 15, 0), (-21, 21, 0), (-28, 28, 0),
  (-36, 36, 0), the x axis ahead each time (the tie at Link 8, 36 against
  36, to x); at Link 9 the y axis is ahead, 45 against 28, the Link is +Y
  and the accumulators (28, -28, 0); then +X five times ((18, -18, 0),
  (7, -7, 0), (-5, 5, 0), (-18, 18, 0), (-32, 32, 0)), +Y at Link 15
  ((32, -32, 0)), +X four times ((16, -16, 0), (-1, 1, 0), (-19, 19, 0),
  (-38, 38, 0)), +Y at Link 20 ((26, -26, 0)), +X three times ((5, -5, 0),
  (-17, 17, 0), (-40, 40, 0)) and +Y at Link 24 ((24, -24, 0)): the Ports
  x x x x x x x x y x x x x x y x x x x y x x x y, the +Y Links at 9, 15,
  20 and 24, closer as the register turns (the parabola of a constant
  push), and the positions from (0, 0, 0): (1,0,0), (2,0,0), (3,0,0),
  (4,0,0), (5,0,0), (6,0,0), (7,0,0), (8,0,0), (8,1,0), (9,1,0), (10,1,0),
  (11,1,0), (12,1,0), (13,1,0), (13,2,0), (14,2,0), (15,2,0), (16,2,0),
  (17,2,0), (17,3,0), (18,3,0), (19,3,0), (20,3,0), (20,4,0). Under v1,
  the accumulators reset at every push, the same 24 Links were all +X.
  Pushed by (0, 8, 0) before every departure, the register (64, 8t, 0) of
  length 64 + 8t: the accumulators after each Link (-8, 8, 0),
  (-24, 24, 0), (40, -40, 0), (8, -8, 0), (-32, 32, 0), (32, -32, 0),
  (-24, 24, 0), (40, -40, 0), (-32, 32, 0), (32, -32, 0), (-56, 56, 0),
  (8, -8, 0), (72, -72, 0), (-40, 40, 0), (24, -24, 0), (88, -88, 0),
  (-48, 48, 0), (16, -16, 0), (80, -80, 0), (-80, 80, 0), (-16, 16, 0),
  (48, -48, 0), (112, -112, 0), (-80, 80, 0); the Ports
  x x y x x y x y x y x y y x y y x y y x y y y x; the positions (1,0,0),
  (2,0,0), (2,1,0), (3,1,0), (4,1,0), (4,2,0), (5,2,0), (5,3,0), (6,3,0),
  (6,4,0), (7,4,0), (7,5,0), (7,6,0), (8,6,0), (8,7,0), (8,8,0), (9,8,0),
  (9,9,0), (9,10,0), (10,10,0), (10,11,0), (10,12,0), (10,13,0), (11,13,0):
  eleven +X and thirteen +Y Links, the staircase of the running register
  from along x to past 45 degrees (the register (64, 64, 0) at Link 8 and
  (64, 192, 0) at Link 24). One push (0, 1, 0) before the first Link and
  none after is the static register (64, 1, 0) from (0, 0, 0), length 65:
  +Y at Links 33, 98 and 163 of 200 (the y accumulator 33 against x's 32
  at Link 33, then one +Y Link per 65), the DDA of the static register
  exactly, as under v1;
- (b) `kept`: the register (64, 1, 0) walked 20 Links from (0, 0, 0),
  accumulators (-20, 20, 0), pushed by (0, 1, 0) is (64, 2, 0) with the
  accumulators kept, (-20, 20, 0) (under v1 (0, 0, 0)), and its next Link
  is +X with (-22, 22, 0) (44 against 22, length 66). The flip: the
  register (64, 10, 0) with accumulators (-20, 20, 0) pushed by (0, 90, 0)
  is (64, 100, 0), length 164, the accumulators kept; its next five Links
  are +Y, +X, +Y, +Y, +X (Ports 2, 0, 2, 2, 0) with the accumulators
  (44, -44, 0), (-56, 56, 0), (8, -8, 0), (72, -72, 0), (-28, 28, 0): the
  whole Port turns at once when the dominant axis flips, then the
  staircase of the new register; pushed by (-128, 0, 0) instead it is
  (-64, 10, 0), length 74, the accumulators kept, and the next Link is -X
  (Port 1) with (-30, 30, 0). The cancel: the default ray of amount 64
  heading +X pushed by (0, 1, 0) and then by (0, -1, 0) is the ray it was,
  equal field by field (no register, accumulators (0, 0, 0)); the register
  (64, 1, 0) with accumulators (-20, 20, 0) pushed by (0, -1, 0) is the
  default with (0, 0, 0), the walk starting over when the register returns
  to the default. The shrink: the register (64, 30, 0) with accumulators
  (-30, 30, 0) pushed by (-30, 0, 0) is (34, 30, 0), length 64, the
  accumulators kept (they lie within (-64, 64]); pushed by (-62, -28, 0)
  it is (2, 2, 0), length 4, which cannot hold them, and the accumulators
  are (0, 0, 0). The lift: a ray of amount 5 on the table heading
  (7, -1, 0) walked three Links from (0, 0, 0) has the accumulators
  (-3, 3, 0) at the table's scale (length 8); pushed by (0, 0, 1) its
  register is (35, -5, 1), length 41, and the accumulators are lifted by
  the amount to (-15, 15, 0), the same fraction of a Link against the
  default register's length 40; its next Link is +X (the tie of 20 against
  20 to x) with (-21, 20, 1), as the unpushed walk's next Link is +X (4
  against 4);
- (c) `board`: an open 28 x 56 x 5 lattice under the shared Detector
  admission (schema 1, `link_ticks` 1, `metric: "links"`, pace 1/1, no
  decay, the six unit-axial headings in Port order), the families `m`
  (rest rate 1, 3-bit phase), `f` and `g` (rate 0, the field rays), 8 ray
  slots each, a vector field `momentum` bound through `recoil_field` on
  every emission; every lamp holds its amount and emits it once, funded, at
  phase 0 in the cycle of tick 0. Two couplings without outputs: `above`
  over `[m, f]` with `{"f": -1}` and `below` over `[m, g]` with
  `{"g": 1}`, so an `f` ray coming down (-Y) and a `g` ray coming up (+Y)
  each push the m ray by (0, 1, 0) and return reversed. A lamp at
  (2, 26, 2) emits `m` 64 along +X; after tick t the m ray is at P(t) =
  (3, 26, 2) plus the position after t - 1 Links of (a) (P(1) = (3, 26, 2),
  P(9) = (11, 26, 2), P(10) = (11, 27, 2), P(16) = (16, 28, 2), P(21) =
  (20, 29, 2), P(25) = (23, 30, 2)). A lamp of `f` 1 along -Y stands at
  P(t) + (0, t, 0) for every t from 1 to 24 whose Link is +X, and a lamp of
  `g` 1 along +Y at P(t) - (0, t, 0) for t = 9, 15, 20 and 24, the +Y
  Links (a delivery from below for the tick after a +Y Link would reach the
  ray's Node a tick early, two pushes in one cycle, and a delivery from
  above at a +Y Link would send its recoil along with the ray): the f lamps
  at (3,27,2), (4,28,2), (5,29,2), (6,30,2), (7,31,2), (8,32,2), (9,33,2),
  (10,34,2), (11,37,2), (12,38,2), (13,39,2), (14,40,2), (15,41,2),
  (16,44,2), (17,45,2), (18,46,2), (19,47,2), (20,50,2), (21,51,2),
  (22,52,2) and the g lamps at (11,17,2), (16,12,2), (20,8,2), (23,5,2).
  So exactly one field ray is resident with the m ray at every tick from 1
  to 24, none after, and no recoil (walking +Y from an f push, -Y from a g
  push) meets the ray again; 27 ticks. In the cycle of tick t (1 to 24) the
  push is (0, 1, 0), `ray_push` at P(t): family `m`, amount 64, before
  (64, t - 1, 0), after (64, t, 0), field `f` with heading (0, -1, 0), or
  `g` with (0, 1, 0) at 9, 15, 20 and 24, field amount 1; the departure of
  that cycle is Link t of (a). After tick t from 2 to 25 the m ray is at
  P(t) with register (64, t - 1, 0), the accumulators after Link t - 1 of
  (a), phase t mod 8, steps t, heading index 0, mask 1, shares
  (64, 0, 0, 0, 0, 0); after tick 1 it has no register and accumulators
  (0, 0, 0). Without a push the walk continues on the static (64, 24, 0),
  length 88: after tick 26 the ray is at (24, 30, 2) with (0, 0, 0) (88
  against 0), after tick 27 at (25, 30, 2) with (-24, 24, 0). The momentum
  line: sourced = current = (0, 3a - b, 0) after every tick, a the f pushes
  of the cycles before it (each the push +1 and the reversal +2; the push
  of the cycle of tick u is booked with the delivery of tick u + 1) and b
  the g pushes (+1 and -2), nothing escaped through tick 27 (the first recoil reaches a face at
  tick 31); every ledger balanced; `m` 64, `f` 20 and `g` 4 throughout;
  the runner records `ray_momentum_turn: "ray-momentum-turn-v2"`,
  `conserved_at_every_completed_tick` true;
- (d) `board_8`: the board of (c) on an open 16 x 32 x 5 lattice, the lamp
  at (2, 14, 2) emitting `m` 64 along +X, the field lamps of amount 8, so
  every push is (0, 8, 0): after tick t the m ray is at P(t) = (3, 14, 2)
  plus the position after t - 1 Links of the (0, 8, 0) walk of (a), the f
  lamps (along -Y) at P(t) + (0, t, 0) for t = 1, 2, 4, 5, 7, 9 and 11, the
  +X Links, ((3,15,2), (4,16,2), (5,19,2), (6,20,2), (7,23,2), (8,26,2),
  (9,29,2)) and the g lamps (along +Y) at P(t) - (0, t, 0) for t = 3, 6,
  8, 10 and 12, the +Y Links ((5,11,2), (7,9,2), (8,8,2), (9,7,2),
  (10,6,2)); 17 ticks. Links 13 and 12 are both +Y, and Link 13 can be
  served from neither side, so the pushes stop after tick 12 and the walk
  goes on with the static register (64, 96, 0), length 160: positions
  after ticks 1 to 17: (3,14,2), (4,14,2), (5,14,2), (5,15,2), (6,15,2),
  (7,15,2), (7,16,2), (8,16,2), (8,17,2), (9,17,2), (9,18,2), (10,18,2),
  (10,19,2), (10,20,2), (11,20,2), (11,21,2), (12,21,2); the register
  (64, 8(t - 1), 0) after tick t from 2 to 13 and (64, 96, 0) after, the
  accumulators after tick t from 2 to 13 those after Link t - 1 of the
  (0, 8, 0) walk, then (72, -72, 0), (-24, 24, 0), (40, -40, 0),
  (-56, 56, 0) after ticks 14 to 17 (+Y, +X, +Y, +X: 72 against 88, 136
  against 24, 40 against 120, 104 against 56). `ray_push` at tick t (1 to
  12) at P(t): before (64, 8(t - 1), 0), after (64, 8t, 0), field amount
  8. The momentum line: sourced = current = (0, 24a - 8b, 0), nothing
  escaped through tick 17 (the first recoil reaches a face at tick 18);
  every ledger balanced; `m` 64, `f` 56, `g` 40 throughout.

## Loop binding

`tests/test_loop_binding.py` is the test of feature 14, binding as a loop
(`loop-binding-v1`, [loop binding](LOOP_BINDING.md)), pinned here on
2026-09-17 before the module exists, as Highlights 5.5 requires, and written
the same day when the feature landed, after feature 8b (the cases `record`
and `rejected` below were pinned then, before their first run). It builds the
unit-square ring of `examples/nature/ring.json` and `ring_open.json`
inline (and does not load the example files): an open 12 x 12 x 11 board,
`link_ticks` 1, `metric: "links"`, pace 1/1, the six unit-axial headings in
Port order, the family `electron` (charge -3, 8 ray slots) on a 3-bit phase
(8 steps) with rest rate 2, a vector field `momentum` bound through
`recoil_field` on every emission, and eight lamps, two at each corner of
the square P0 = (5,5,5), P1 = (6,5,5), P2 = (6,6,5), P3 = (5,6,5), each
holding 1 quantum and emitting it once, funded and directed, at phase 0 in
the cycle of tick 0: the R lamps on +X at P0, +Y at P1, -X at P2, -Y at P3
and the L lamps on +Y at P0, -X at P1, -Y at P2, +X at P3. The one rule
`corner` is `electron x electron` with two outputs, each input's amount and
phase through the Port the other input came in by (`heading` `"reversed"`
of the other `input`), invariant energy; the `born` cases replace the
amounts by the catalog's Born table on the sum (`[8, 7, 4, 1, 0, 1, 4, 7]`,
`"of": "sum"`, `"index": "phase_difference"`) and `{"rest_of": 0}`. A tick
t is one `step()`; the state after tick t is read from `inventory_view()`;
a ray is written as (Node, heading index, amount, phase, steps, mask,
shares). The test is parametrized over `ring`, `open`, `slow`, `half`,
`quadrature`, `record` and `rejected`. The engine of `main` at `c21e03e`
was run once on every case after the pins were written (the check the design
allows): its column is identical to the hand column below in every line, so
one column is given; on the landed engine every line of (a) to (e) held at
the first run. Pinned before the first run:

- (a) `ring` (`ring.json`, the Port form, r = 2): after tick 1 each corner
  holds two rays of amount 1, phase 2, steps 1, each carrying its lamp's
  emission stamp (mask `1 << h`, share 1 at Port h): P0 headings 1 (mask 2,
  shares (0,1,0,0,0,0)) and 3 (mask 8, (0,0,0,1,0,0)); P1 headings 0 (mask
  1) and 3 (mask 8); P2 headings 0 (mask 1) and 2 (mask 4); P3 headings 1
  (mask 2) and 2 (mask 4). In the cycle of every tick t from 1 the rule
  fires at all four corners and books the momentum the two quarter turns
  move as the corner's source (`source_delta` of its `spatial_cycle`
  record): (2, 2, 0) at P0, (-2, 2, 0) at P1, (-2, -2, 0) at P2,
  (2, -2, 0) at P3, summing to (0, 0, 0). After every tick t from 2 to 16
  the same eight lines hold with phase 2t mod 8 (4, 6, 0, 2, 4, ...) and
  steps 1: at P0 heading 1, mask 6, shares (0,1,1,0,0,0) and heading 3,
  mask 9, (1,0,0,1,0,0); at P1 heading 0, mask 5, (1,0,1,0,0,0) and
  heading 3, mask 10, (0,1,0,1,0,0); at P2 heading 0, mask 9, (1,0,0,1,0,0)
  and heading 2, mask 6, (0,1,1,0,0,0); at P3 heading 1, mask 10,
  (0,1,0,1,0,0) and heading 2, mask 5, (1,0,1,0,0,0) (the stamp of the
  corner each ray last left: P0's meeting is one event on Ports 0 and 2,
  P1's on 1 and 2, P2's on 1 and 3, P3's on 0 and 3, share 1 each). The
  state after tick t + 4 equals the state after tick t for every t from 2:
  the loop closes in one circuit, 4 x 2 = 8 = 0 (mod 8). At every tick:
  electron 8 in the world, none escaped, momentum (0, 0, 0) in the world
  and in the sources (the lamps hold minus their rays' momentum, (-1,0,0),
  (0,-1,0), (0,-1,0), (1,0,0), (1,0,0), (0,1,0), (0,1,0), (-1,0,0)), the
  charge line electron -24, every ledger line balanced,
  `conserved_at_every_completed_tick` true; the snapshot has no
  `bound_groups` key (the design's "empty at every tick", the key itself
  gone with the held form) and no `bound_tick` is written; the runner
  records `ray_meeting: "ray-meeting-conversion-v1"`;
- (b) `open` (`ring_open.json`, the Born form in phase, d = 0): after tick
  1 exactly the lines of (a). In the cycle of tick 1 input 0 at each corner
  is the resident ray with the lower heading index (the L ray at P0 and P2,
  the R ray at P1 and P3), d = 0 and the table output takes floor(2 x 8 /
  8) = 2 through the Port input 1 came in by, the rest output being no ray:
  P0 sends 2 on +Y (Port 2), P1 2 on +Y, P2 2 on -Y (Port 3), P3 2 on -Y;
  the corners book (1, 3, 0), (-1, 3, 0), (-1, -3, 0), (1, -3, 0), summing
  to zero. After tick 2 each corner holds one ray of amount 2, phase 4,
  steps 1: heading 3, mask 8, shares (0,0,0,2,0,0) at P0 and P1, heading 2,
  mask 4, (0,0,2,0,0,0) at P2 and P3. No rule fires again. After tick t
  from 3 to 7 the four rays are at (5, 7 - t, 5) and (6, 7 - t, 5) heading
  3 and at (5, 4 + t, 5) and (6, 4 + t, 5) heading 2, amount 2, phase 2t
  mod 8, steps t - 1, the same masks and shares; after tick 8 and every
  later tick the board is empty: electron 0 in the world, 8 escaped,
  momentum (0, 0, 0), every ledger line balanced,
  `conserved_at_every_completed_tick` true, `bound_groups` empty;
- (c) `slow` (the Port form at the catalog's rate, r = 1): the Nodes,
  headings, amounts, steps, masks and shares of (a) at every tick, with
  phase t mod 8; the state after tick t + 8 equals the state after tick t
  for every t from 2, and after tick t + 4 it differs in every phase by 4:
  4 x 1 = 4 is not 0 (mod 8), the loop closes in two circuits, and nothing
  disperses (electron 8, none escaped, through tick 9);
- (d) `half` (the Port form, r = 2, the four rays of the two lamps at P0
  and at P2 only): after tick 1 P1 holds headings 0 (mask 1) and 3 (mask 8)
  and P3 headings 1 (mask 2) and 2 (mask 4), amount 1, phase 2, steps 1, P0
  and P2 empty; after every even tick t from 2 the four rays are at P0
  (headings 1 and 3, masks 6 and 9) and P2 (headings 0 and 2, masks 9 and
  6) and after every odd tick from 3 at P1 (headings 0 and 3, masks 5 and
  10) and P3 (headings 1 and 2, masks 10 and 5), with the shares of (a),
  phase 2t mod 8, steps 1; two corners meet in every interval, the state
  after tick t + 4 equals the state after tick t from t = 2, electron 4 in
  the world, none escaped, momentum (0, 0, 0): the smallest loop, content
  4;
- (e) `quadrature` (the Born form with the four L lamps at phase 2, d = 2):
  the Nodes, headings, amounts, steps, masks and shares of (a) at every
  tick, the R rays with phase 2t mod 8 and the L rays with 2t + 2 mod 8
  (after tick 1 the L rays, headings 1 at P0, 3 at P1, 0 at P2 and 2 at
  P3, read 4 and the R rays 2); at every corner d = 2 or 6, T[d] = 4, the
  table output takes floor(2 x 4 / 8) = 1 and the rest output 1, so the
  amounts are reproduced and the corner bookings are those of (a); the
  state after tick t + 4 equals the state after tick t from t = 2, electron
  8, none escaped, through tick 6;
- (f) `record`: the worlds of (a) and (b) through `run_initialization` for
  16 ticks. The run record carries `loop_binding: "loop-binding-v1"` and
  `ray_meeting: "ray-meeting-conversion-v1"`, no `bound_group_motion` key,
  `conserved_at_every_completed_tick` true; no `bound_tick` and no
  `bound_group_step` event exists; the `spatial_cycle` records of the
  corners carry the momentum of the two quarter turns as their
  `source_delta`: in every cycle of ticks 1 to 15 of (a) (2, 2, 0) at P0,
  (-2, 2, 0) at P1, (-2, -2, 0) at P2, (2, -2, 0) at P3, and in the cycle
  of tick 1 of (b) (1, 3, 0), (-1, 3, 0), (-1, -3, 0), (1, -3, 0) with no
  momentum booked at any corner in the cycle of tick 2; the final totals
  are electron 8 and momentum (0, 0, 0) for (a), electron 0 with 8 escaped
  for (b). The ray viewer's extractor
  ([ray viewer](../tools/ray_viewer/README.md)), reading the record of (a)
  with its phase recording (`record_sidecar.py`), reports exactly one
  group: ring `[P0, P1, P2, P3]` (the closed walk from the lowest Node
  through the lowest Port), ring size 4, content 8, families
  `{"electron": 8}`, period 4, clock `{"electron": 2}` on phase steps
  `{"electron": 8}`, read from tick 1 to tick 15 (the emissions of tick 0
  carry no recorded phase), over 120 rays, each of which carries `group` 0
  and every other ray `group` None; the tick rows carry `bound`
  `{"electron": [8]}` at ticks 1 to 15 and nothing at ticks 0 and 16.
  Without the phase recording the reading is the same group with period 1
  (the pattern of Nodes, headings and amounts is the same every interval)
  and clock None. The record of (b) reads no group and no `bound` content;
- (g) `rejected`: `ray_delay` 1 on the held rule of feature 8 (`n x n`
  without outputs assigning `delay` 1 to both), `ray_delay` 1 on the
  corner rule, and `{"electron": -1}` as `momentum_table` on the held rule
  are each rejected at initialization with a message that says "removed by
  loop-binding-v1" and names `docs/MIGRATION.md`. The held rule alone
  parses and is a wait, not a hold: on the board of (a) with it in place of
  `corner`, the two rays at each corner after tick 1 wait one interval at
  their event Node (after tick 2 they are still there with steps 0 and
  delay 0), are met by nothing, leave in the cycle of tick 2 on their
  unchanged headings, off the square, and after tick 7 the eight rays are
  at the board's edge, at (0,5,5), (0,6,5), (5,0,5), (5,11,5), (6,0,5),
  (6,11,5), (11,5,5) and (11,6,5), the corners empty from tick 3, electron
  8, none escaped, momentum (0, 0, 0), charge -24, every line balanced.

## Decay draw

`tests/test_decay_draw.py` is the test of feature 13, a decaying group draws
(`decay-draw-v1`, [a decaying group
draws](SPATIAL_FIELDS.md#a-decaying-group-draws-decay-draw-v1); Highlights
3.26 and 3.19 in the loop form of feature 14), pinned here on 2026-09-17
before the module's first run, as Highlights 5.5 requires. It builds the
unit-square ring of E5 (`examples/nature/ring.json`) inline as
`test_loop_binding.py` does (the same open 12 x 12 x 11 board, `link_ticks`
1, `metric: "links"`, pace 1/1, the family `electron` with charge -3 and
rest rate 2 on a 3-bit phase, the eight corner lamps of amount 1, the `corner`
rule of the Port form), with one more ray family `p` (the same width, rate
and charge -3, its momentum bound through an emission of a lamp type that is
never seeded) and the rule `decay` declared before `corner`:
`[electron, electron]`, `"draw": [1, 64]`, `"seed": 6`, two outputs of `p`
with each input's amount and phase on the input's own heading
(`"heading": "same"`), invariant energy, the charge invariant appended. A
tick t is one `step()`; the state after tick t is read from
`inventory_view()`; a ray is written as (heading index, amount, phase, steps,
mask, shares) as in the loop-binding section. The run is 36 ticks.

**The structure, a priori.** Every corner meets two electrons in the cycle of
every tick t from 1 while the ring is whole, the `decay` rule is met first,
so every corner meeting draws once at 1/64 from that corner's stream, and on
0 the meeting continues to `corner`, which reproduces the ring: the lines of
the loop-binding case (a) hold after every tick through the first draw of 1.
The eight-ray ring is two interleaved four-ray orbits: orbit A (the lamps of
P0 and P2) meets at P1 and P3 in the cycles of odd ticks and at P0 and P2 of
even ticks, orbit B the other way round. The first 1, at corner C in the
cycle of tick T, converts the pair that met there into two `p` rays leaving
C on the headings they arrived by, momentum unchanged; the same orbit's
other pair meets its corner as usual that cycle and its two rays arrive alone
at the two neighbouring corners after tick T + 1, where a corner with one
electron fires nothing, so they cross off the ring and off the open board;
the other orbit keeps circulating as the four-ray ring, content 4, two
corners drawing per tick, until its own 1 at tick T2, after which its other
pair disperses the same way and nothing is left. The survival law of the
whole ring is (1 - 1/64)^k over its k corner meetings, four per tick. Every
corner's stream starts at the rule's seed salted once by each coordinate of
the corner (`decay_ticket_seed`) and advances one unsalted step per meeting;
the tickets a corner consumed are its meetings that drew, and no other Node
draws.

**The integers, by hand from the published ticket rule** (`state = (state x
48271 + salt + 1) mod 1073741789` with the salt 0 for a draw and the
coordinate for the seeding, `number = state^2 mod 1073741789`, bit 1 when
`64 x number < 1073741789`; the seed 6 was chosen by this rule so that the
first 1 falls after two periods of the ring, which the group reader needs,
and the second inside the run):

- the streams start at 276043064 (P0), 458648927 (P1), 458697198 (P2),
  276091335 (P3); the first draws, in the cycle of tick 1, leave them at
  812882644, 1034149616, 143013690, 995488507, all bits 0;
- (a) the first 1 is at P1 in the cycle of tick 11 (T = 11), its ticket
  470793086; the other corners draw 0 that cycle at 724645537 (P0),
  866042076 (P2), 46152738 (P3). After every tick 1 to 11 the corners hold
  the loop-binding lines (the lamp lines after tick 1, the ring lines
  after 2 to 11, phase 2t mod 8), electron 8, p 0, momentum (0, 0, 0),
  charge electron -24, every ledger line balanced. Orbit A's pair at P1
  (headings 0 and 3, the R ray input 0) becomes two p rays of amount 1,
  phase 6, one event on Ports 0 and 3 (mask 9, shares (1, 0, 0, 1, 0, 0)),
  leaving on +X and -Y: after tick t from 12 to 16 they are at (6 + (t - 11),
  5, 5) heading 0 and (6, 5 - (t - 11), 5) heading 3 with steps t - 11 and
  phase 2t mod 8, and they leave the board at tick 17 (escaped p 2). The
  cycle of tick 11 books at P1 the family change as that corner's source,
  `electron -2, p 2`, and no momentum; P0, P2 and P3 book their corner
  momentum (2, 2, 0), (-2, -2, 0), (2, -2, 0) as before;
- (b) after tick 12 P1 and P3 hold orbit B's pairs (the ring lines of P1
  and P3, phase 0) while P0 holds one electron, heading 3, mask 9, shares
  (1, 0, 0, 1, 0, 0), and P2 one, heading 0, mask 9, the same shares (orbit
  A's other pair, sent by P3's corner rule in the cycle of tick 11); no rule
  fires at P0 or P2 in the cycle of tick 12, and after tick t from 13 to 17
  those two are at (5, 5 - (t - 12), 5) heading 3 and (6 + (t - 12), 6, 5)
  heading 0, steps t - 11, phase 2t mod 8, leaving the board at tick 18
  (escaped electron 2). From tick 12 orbit B holds: after even ticks its
  pairs are at P1 and P3 and after odd ticks at P0 and P2, with the ring
  lines of those corners and phase 2t mod 8, and only those two corners
  draw and book their corner momentum in each cycle; electron 6 and p 2
  after ticks 12 to 16, p 0 from tick 17, electron 4 from tick 18, content
  4 on the ring;
- (c) the second 1 is at P1 in the cycle of tick 26 (T2 = 26), ticket
  549671329, P3 drawing 0 at 758084520 that cycle; orbit B's pair at P1
  becomes two p rays as in (a), at (6 + (t - 26), 5, 5) and (6, 5 - (t -
  26), 5) after tick t from 27 to 31, escaped at tick 32; its other pair is
  alone at P0 (heading 3) and P2 (heading 0) after tick 27, at (5, 5 - (t -
  27), 5) and (6 + (t - 27), 6, 5) after tick t from 28 to 32, escaped at
  tick 33. From tick 27 no corner meets and no draw is made; after tick 36
  the board holds no ray: electron 0, p 0, escaped electron 4 and p 4,
  momentum (0, 0, 0) in the world and (4, -4, 0) escaped and sourced (the
  corner bookings of the cycles of ticks 11 and 26 that had no partner
  corner: (2, -2, 0) each), the sources electron -4 and p 4, the charge
  lines electron -24 = 0 + 12 (sourced) - 12 (escaped) and p 0 - 12 = -12,
  every ledger line balanced at every tick;
- (d) the momentum of the world after tick t is (1, -1, 0) per pair off
  the ring still in the world: (2, -2, 0) after ticks 12 to 16 and 27 to
  31, (1, -1, 0) after 17 and 32, (0, 0, 0) otherwise;
- (e) the draws: 74 `decay_draw` lines in `events.jsonl`, each with the
  rule `decay`, the setting `[1, 64]`, the ticket and the bit: four per tick
  at ticks 1 to 11 (every corner), then P1 and P3 at the even ticks 12 to 26
  and P0 and P2 at the odd ticks 13 to 25; the bits 1 at (11, P1) and
  (26, P1) only; per corner P0 18 draws ending at tick 25 with ticket
  334272102, P1 19 ending at tick 26 with 549671329, P2 18 ending at 25
  with 758871333, P3 19 ending at 26 with 758084520, and after the run each
  corner's `detector_ticket` is that last ticket while every other Node's
  is its salted seed, untouched; the whole ring survived 40 draws of 0
  (ticks 1 to 10), and in the cycle of tick 11 the second draw, P1's after
  P0's, the 42nd of the run, fired;
- (f) the run record carries `decay_draw: "decay-draw-v1"` beside
  `loop_binding` and `ray_meeting`, `conserved_at_every_completed_tick`
  true, final totals electron 0, p 0, momentum (0, 0, 0), escaped electron
  4, p 4, momentum (4, -4, 0), sources electron -4, p 4, momentum
  (4, -4, 0); the runner run twice on the same document writes the same
  `events.jsonl` byte for byte and the same `run.json` apart from
  `elapsed_seconds`. The ray viewer's extractor with the phase recording
  reads exactly one group on the square, ring `[P0, P1, P2, P3]`, content 8,
  families `{"electron": 8}`, period 4, clock 2 on the 8-step circle, from
  tick 1, read until the conversion breaks the recurrence (`to_tick`
  measured after the first run: see below);
- (g) the world with `corner` alone (the family `p` declared and unused)
  runs the ring of the loop-binding case (a) through tick 16 with electron
  8 and p 0 at every tick, calls the ticket rule nowhere (a monkeypatched
  `next_ticket` fails the test if called), every Node's `detector_ticket`
  stays 0, and its record has no `decay_draw` line and no `decay_draw` key;
- (h) `parse_initial_state` rejects, naming the reason: `draw` on a rule
  without outputs (the held rule of feature 8 with `draw` and `seed`), the
  settings `[3, 2]` (n above d), `[1, 0]` (a zero denominator), `[-1, 2]`,
  `[1, 2.5]` and `[1]`, a `draw` without `seed`, a `seed` without `draw`, a
  seed of 1073741789 and of -1; `validate_configuration` reports each
  document invalid.

**Measured on the first run (2026-09-17).** Every integer of (a) to (h)
held at the first run: the states after every tick, the loose rays, the
ledger and the charge lines at every tick, the tickets, the 74 draws with
their tickets and bits, the corner bookings and the family sources, the
record's totals, the identical replay, the control and the rejections. Two
readings were measured, not pinned: within one tick the `decay_draw` lines
come in the record's order of Nodes, sorted by position, P0, P3, P1, P2
(the test compares the sorted corners); and the group reader's window is
`from_tick` 1 to `to_tick` 10, the last state before the conversion's cycle,
the tick rows carrying `bound` `{"electron": [8]}` at ticks 1 to 10 and
nothing at tick 0 or from tick 11 (the four-ray orbit that circulates on
after the first conversion is not read as a group, since the reader takes
the first window of the rays that share the ring). The module ran in 1.05
seconds.

## The screen with a loop

`tests/test_screen_loop.py` is the isolated test of the demonstration E9
([the screen with a loop](../examples/nature/README.md#the-screen-with-a-loop-the-ring-radiating-on-seven-marks),
[E9](EXPERIMENTS.md#e9-the-screen-with-a-loop-source-the-ring-radiating-on-seven-marks)),
pinned here on 2026-09-17 before its first run, as Highlights 5.5 requires. It
builds the world of `examples/nature/screen_loop.json` inline (and does not
load the file): an open 12 x 11 x 11 board, `link_ticks` 1, `metric:
"links"`, pace 1/1, the six unit-axial headings in Port order, the family
`electron` (charge -3, 8 ray slots, rest rate 1) and the family `light`
(charge 0, rest rate 0, 24 ray slots) declared `field_of` `electron` with
`release` [1, 4] and `spread` [6, 1, 1, 1, 1, 1], both on a 3-bit phase (8
steps), a vector field `momentum` bound through `recoil_field` on every
emission; eight lamps, two at each corner of the unit square P0 = (1,5,5),
P1 = (2,5,5), P2 = (2,5,6), P3 = (1,5,6) in the plane y = 5, each holding 4
quanta and emitting them once, funded and directed, at phase 0 in the cycle
of tick 0: the R lamps on +X at P0, +Z at P1, -X at P2, -Z at P3 and the L
lamps on +Z at P0, -X at P1, -Z at P2, +X at P3 (the lamps of `ring.json`
with Y read as Z); the one rule `corner`, the Port form of the loop-binding
expectations above; seven Detector marks at (7, 2, 5) through (7, 8, 5),
setting [1, 1], seed 0. One test, run through the runner for 32 ticks (24 if
the first run shows 32 to be slow: a shorter run of the same world is a
prefix of the same record, so the integers pinned at the earlier ticks are
those of the first run either way), read from `run.json`, `events.jsonl`
and the ray viewer's extractor with the recording of `record_sidecar.py`.

Written before the first run (the structure, all of it computed from the
rules): the run record carries `loop_binding: "loop-binding-v1"`,
`released_field: "released-field-v1"`, `field_spreading:
"field-spreading-v1"`, `field_remainder: "field-remainder-v1"`,
`released_fields` `[{"field": "light", "field_of": "electron", "release":
[1, 4]}]`, `spreading_fields` `[{"field": "light", "spread": [6, 1, 1, 1,
1, 1]}]` and `ray_layer_families` with `light` in a layer of its own (no
rule names it, so it crosses the ring's Nodes unmet and spreads there like
at any Node); `conserved_at_every_completed_tick` is true and every audit
line is balanced at every completed tick; the electron line reads initial
32, sourced 0, current 32, escaped 0, annulled 0, absorbed 0 at every tick
(the source stays bound while it radiates: a release is booked as a source
of `light`, not paid by the ray, Highlights 3.15), the charge line electron
-96; the light line reads sourced 40 (t - 1) after tick t (the lamps' rays
are fresh at tick 0 and release nothing; from the cycle of tick 1 each of
the eight ring rays, amount 4, releases floor(4 / 4) = 1 on the five Port
headings other than the one it departs on, 40 per interval, 1240 by tick 32),
current + escaped = sourced with the registers counted as current, annulled
and absorbed 0; the momentum line reads (0, 0, 0) sourced and current at
every tick (`light` binds no momentum field, so a spread books none, and
the two quarter turns of every corner are booked as that corner's source in
its `spatial_cycle` record, (8, 0, 8) at P0, (-8, 0, 8) at P1, (-8, 0, -8)
at P2, (8, 0, -8) at P3 in the cycle of every tick from 1, summing to zero);
the corners' cycle records book `light` 10 each per interval (the two
departing rays' five headings). No event of the kinds `bound_tick`,
`bound_group_step`, `ray_push`, `inverse_split`, `detector_return`,
`field_returned` or `external_body_absorbed` exists; the event kinds are
those of the host's cycle, `spatial_cycle`, `spatial_sent`,
`spatial_received`, `spatial_escaped`, `field_spread`, `detector_click` and
`detector_pass` only. The extractor, reading the record with its recording,
reports exactly one group: ring `[P0, P1, P2, P3]` (the closed walk from the
lowest Node through the lowest Port: (1,5,5), (2,5,5), (2,5,6), (1,5,6)),
ring size 4, content 32, families `{"electron": 32}`, period 8 (the
catalog's rate 1 closes the square in two circuits, 4 x 1 = 4 is not 0 mod
8, E5's `slow` case), clock `{"electron": 1}` on phase steps `{"electron":
8}`, from tick 1 to tick T - 1 for a run of T ticks (the emissions of tick 0
carry no recorded phase); every tick row from 1 to T - 1 carries `bound`
`{"electron": [32]}`; the group's rays are electron chains only, since the
light that crosses the corners is a field family. Every `detector_click` is
of family `light`, amount 1 (the field is whole quanta released where the
registers fill), bit 1, at one of the seven marks; the first click is at the
on-axis mark (7, 5, 5), fed by the axis line from P1 (two fresh quanta per
interval, the merged +X releases of P1's two departing rays, and P1's
register releases), before E6's tick 19 (E6's beam was 2 per interval from
(1, 5, 5), one Node farther and without a corner's registers behind it);
within the run's few dozen ticks no mark off the axis clicks (a transverse
release takes eleven arrivals at one Node, E6 saw the first pair at tick
82), and if one does, its mirror mark (7, 10 - y, 5) clicks in the same tick
with the same amount, the world being symmetric under y -> 10 - y.

Read from the record of the first run of this board (2026-09-17, 32 ticks,
2.9 s for the run and 4.9 s for the recording and the reading, so 32 ticks
stay) and pinned then, as the run's integers rather than computed by hand
(the field's integer state at a mark is the sum of many spreads): seven
clicks, all at the on-axis mark (7, 5, 5), family light, amount 1, bit 1,
through Port 1 (the -X face, the axis line's arrival), at ticks 11, 15, 18,
22, 27, 27 and 31 (two quanta of different phases in the same interval at
tick 27), no click off the axis and no `detector_pass`; the light line after
tick 32: sourced 1240, current 1016 (rays and registers), escaped 224
(after tick 2: 40, 40, 0; tick 8: 280, 264, 16; tick 16: 600, 530, 70;
tick 24: 920, 784, 136); 2759 `field_spread` records; the group read from
tick 1 to tick 31 over 248 electron rays, `ray_layer_families`
`[["electron"], ["light"]]`.

## The ring meets its own field

`tests/test_ring_self_field.py` is the isolated test of the run E10
([the ring meets its own field](../examples/nature/README.md#the-ring-meets-its-own-field),
[E10](EXPERIMENTS.md#e10-the-ring-meets-its-own-field-the-loop-under-its-own-light-contents-32-to-128)),
pinned here on 2026-09-17 before its first run, as Highlights 5.5 requires.
It loads `examples/nature/e10_self_field/make_worlds.py` from its file and
checks that the nine world files are byte for byte what `cases()` writes;
then it takes the three content-32 worlds (`world(4, variant)`, the
smallest: the unit square P0 = (5,5,5), P1 = (6,5,5), P2 = (6,6,5), P3 =
(5,6,5) in the plane z = 5 on a 12 x 12 x 12 open board, eight `electron`
lamps of amount 4 at rest rate 1 on a 3-bit phase, `light` `field_of`
`electron` with `release` [1, 4] and `spread` [6, 1, 1, 1, 1, 1], 24 ray
slots, the rules `corner` alone, `corner` then `electron_field_turn`
(`momentum_table` `{"light": 1}`), and the two in the other order) with
`ticks` 16 and runs each through the runner, reading `run.json`,
`events.jsonl` and the extractor with the recording of `record_sidecar.py`.
One test. Corrected at the first look at the first 96-tick record of E10
(2026-09-17, before this test's first run; the 16 above is kept as
written): the run is 24 ticks, since the reader's window
(`periodic_window`) needs the states to repeat over at least two periods
with a recorded tick after them, 17 recorded ticks at period 8, and a
16-tick record holds the corners' states at ticks 1 to 15 only, so it reads
no group; 24 ticks, three periods, is the length E9's expectations named as
the fallback. Every statement below at "tick 15" reads "tick 23" and the
window "1 to 23".

Written before the first run (all of it computed from the rules, the
"Computed" item of E10): the control's record carries `ray_layer_families`
`[["electron"], ["light"]]` and no `ray_momentum_turn`; both coupled records
carry `[["electron", "light"]]` (the coupling names `light`, one layer);
`loop_binding` `"loop-binding-v1"`, `released_field`, `field_spreading` and
`field_remainder` as E9's. `corner_first`: no `ray_push` event, no
`ray_momentum_turn` in `run.json`, and its `events.jsonl` equal byte for
byte to the control's (the corner rule takes both electrons at every corner
in every cycle and the turn rule finds none). Corrected at the first look
at the first 96-tick record of E10 (2026-09-17, before this test's first
run; the statement above is kept as written): the two streams have the same
events line for line but for the host's `cost` of every `spatial_cycle`,
`cycle_started` and `cycle_committed` record, which counts the light rays
the one-layer meeting reads (`_meet` charges one read per view component
per resident ray of the layer); every physical line (`spatial_received`,
`spatial_sent`, `field_spread`, `spatial_escaped`, the cycles'
`source_delta`) is identical, so the test pins equality with `cost`
removed, the byte inequality, and that the differing keys are those three
`cost` lines and nothing else. The electron line 32 at every
tick with no escape; the group read as E9's: ring `[P0, P1, P2, P3]`,
content 32, `{"electron": 32}`, period 8, clock `{"electron": 1}`, from
tick 1 to tick 15, every tick row from 1 to 15 bound `{"electron": [32]}`.
`turn_first`: `ray_momentum_turn` `"ray-momentum-turn-v2"` in `run.json`;
exactly eight `ray_push` events at tick 2, two per corner, family
`electron`, amount 4, field `light`, field amount 1, in this order at each
corner (the light rays in heading-index order): P0, before `[-4, 0, 0]`,
field heading `[-1, 0, 0]`, after `[-5, 0, 0]`, then field heading
`[0, -1, 0]`, after `[-5, -1, 0]`; P1, before `[4, 0, 0]`, `[1, 0, 0]` to
`[5, 0, 0]`, then `[0, -1, 0]` to `[5, -1, 0]`; P2, before `[4, 0, 0]`,
`[1, 0, 0]` to `[5, 0, 0]`, then `[0, 1, 0]` to `[5, 1, 0]`; P3, before
`[0, 4, 0]`, `[-1, 0, 0]` to `[-1, 4, 0]`, then `[0, 1, 0]` to
`[-1, 5, 0]`; no `ray_push` at a corner after tick 2 (the ring is gone),
every later push at a Node off the ring; at tick 3 electron packets are
received at Nodes off the ring and none at a corner (every ring ray crossed
straight), and from tick 3 no electron packet arrives at a corner; the
extractor reads no group (the states at the corners exist at ticks 1 and
2 only, fewer than two periods); the momentum line (0, 0, 0) sourced and
current after tick 2 (the four corners' pushes cancel). Every world:
`conserved_at_every_completed_tick` true and every audit line balanced at
every completed tick; the light line sourced 40 (t - 1) after tick t in the
control and in `corner_first`.

Corrected at the first look at the first 96-tick record of E10
(2026-09-17, before this test's first run; the statement above is kept as
written): at P3 the receiver is the R ray, as written, but the R ray
arrives at P3 heading -X (from P2) and leaves on -Y, so its register is
`[-4, 0, 0]`, not `[0, 4, 0]` (that heading is the L ray's arrival there),
and the record's two pushes at P3 are field heading `[-1, 0, 0]`,
`[-4, 0, 0]` to `[-5, 0, 0]`, then `[0, 1, 0]` to `[-5, 1, 0]`; the other
three corners are as written, and the four pushes still sum to zero. The
test pins the record's values.

Read from the record of the first run of this board (2026-09-17, the first
24 ticks of the 96-tick records of E10, of which a 24-tick run of the same
world is a prefix) and pinned then, as the run's integers rather than
computed by hand: `turn_first` has 20 `ray_push` events in 24 ticks, 8 at
tick 2 (the corners), 8 at tick 3 (the eight rays one Link off the square,
each pushed by the light of amount 1 released beside it in the cycle of
tick 2 by the ray that left the same corner) and 4 at tick 6 (the four
pushed rays two Links further, at (2, 4, 5), (2, 7, 5), (9, 4, 5) and
(9, 7, 5)), every field ray of amount 1; the electron line escaped 16 after
tick 8 and 32 after tick 9, `escaped_totals` electron 32; the light line
after tick 24: `turn_first` sourced 300, current 300, escaped 0 (the eight
rays release 40 per interval while on the board, seven intervals of eight
rays and one of the four still on it, nothing after tick 9, and no light
has reached the boundary), the control sourced 920, current 900, escaped
20.

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
  therefore released again at (8,7,7): floor(5 x 6 / 11) = 2 are at (9,7,7)
  after two ticks as a fresh field ray with no event, steps 1, and 3 quanta
  wait in the registers of (8,7,7), 8/11 forward and 5/11 on each other
  heading, `field-remainder-v1`), `light` in the `field` of the three charged
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
  and transmission without a draw and their alternative `draw`
  (Highlights 5.4, 2026-09-17); both apparatus kinds landed. Since
  2026-09-17 (feature 14, `loop-binding-v1`) a coupling has `outputs` or
  `sink`, never `binds`: the four binding couplings are corner tables, an
  outputs rule whose loop closes with a `closes` note, `electron_proton_binding`
  the Port form and the three others `"undecided"`, and a bound group's
  `binding` names one of them;
- `undecided`: 28 entries (since 2026-09-17 the three undecided binding
  tables under `outputs` instead of `table`, the same count), every decider
  one of A1, A2, A3, A5, A6, A8, A9,
  A10, A12, hypothesis 12, hypothesis 13, hypothesis 16, hypothesis 17,
  feature 8b, read from the
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
  on the light world. `polarizer` (2026-09-17, feature 11,
  `ray-polarization-v1`): the same lamp with `polarization` 0 (along +Y) at
  a body of the apparatus family with coupling `polarizer`, angle 2 (45
  degrees on the eight-step circle of the reference width), pass +X and the
  catalog's table `[8, 7, 4, 1, 0, 1, 4, 7]`: the ray arrives at tick 1 and
  is split at the difference 2, share 4: floor(5 x 4 / 8) = 2 pass with
  polarization 2 and 2 sink, and the two shares of 4/8 wait in the body's
  registers as one quantum at the ray's phase 1; after tick 2 the pass ray is
  at (9,7,7), heading 0, amount 2, phase 1, steps 1, mask 1 and shares (2, 0,
  0, 0, 0, 0), polarization 2, nothing is left at (8,7,7), the totals are
  light 3 (2 on the ray and 1 held) and apparatus 0, `external_body_totals`
  light 2, and the body at rest reports sink light 2, `held` [0, 0, 4, 4, 0,
  0] and `held_phases` [0, 0, 1, 1, 0, 0]. The accounting balances at every
  tick of every world.

## A5 Coulomb

`test_a5_coulomb.py` pins the worlds and the record of experiment A5
([register](EXPERIMENTS.md#a5-electron-electron-repulsion-through-released-fields);
`examples/nature/a5_coulomb/`, the dictionary in its
[README](../examples/nature/README.md#a5-coulombs-law-through-the-spreading-field)).
Three tests, pinned before the first run:

- the thirteen world files are byte for byte what `make_worlds.py` writes
  (`json.dumps(indent=1)` and a newline), in the order `ee_b4`, `ee_b6`,
  `ee_b8`, `ee_b12`, `ee_b16`, `ep_b4`, ..., `ep_b16`, `nn_b4`,
  `ee_b4_nospread`, `ee_b16_nospread`, and each is the pinned geometry:
  shape [97, 49, 49], open, `ticks` min(48 + 3b + 8, 96); the lamp of ray a
  at (0, 24 − b/2, 24) emitting 64 along +X and of ray b at (96, 24 + b/2,
  24) emitting 64 along −X; the families `electron_a`, `electron_b`
  (`neutral_a`, `neutral_b` in the control) with charges (−3, −3), (−3, 3)
  and (0, 0) for `ee`, `ep` and `nn`, rate 1, `phase_bits` 12, 2 slots, and
  `light_a`, `light_b` with charge 0, rate 0, 30 slots, `field_of` ray a and
  ray b, `release` [1, 4] and `spread` [6, 1, 1, 1, 1, 1] (absent in the
  `nospread` worlds), all on the six Port headings; the couplings
  `electron_field_turn_a` over `[electron_a, light_b]` with
  `{"light_b": s}` and `electron_field_turn_b` over `[electron_b, light_a]`
  with `{"light_a": s}`, s = 1 for `ee` and −1 for `ep`, none in the
  control;
- `ee_b4.json` re-run for 8 ticks: status completed, `field_spreading`
  `field-spreading-v1`, `field_remainder` `field-remainder-v1`, no
  `ray_momentum_turn`, `conserved_at_every_completed_tick` true,
  `released_fields` `light_a` of `electron_a` and `light_b` of `electron_b`
  at [1, 4]; the ledger at tick 8: `light_a` and `light_b` each sourced 560,
  current 540, escaped 20; `electron_a` and `electron_b` sourced 0, current
  64, escaped 0; momentum sourced, current and escaped (0, 0, 0); no
  `ray_push`; ray a received at (8, 22, 24) and ray b at (88, 26, 24) at
  tick 8;
- `record.json`, written by `analyze.py --record` from the runs of
  2026-09-17 (source
  `4c6e313ce9f0b14be95ce85b3c4f256d4072f2e81715ddf1f1071b44c11d33bb`):
  thirteen runs, every one completed with the source above, its
  `initialization_sha256` equal to the SHA-256 of the committed world file,
  `conserved_at_every_completed_tick` true, `rays_sum_max_abs` 0 (the sum
  over every ray's momentum is (0, 0, 0) at every tick) and the momentum
  sourced (0, 0, 0) at the end; the spread series: at b = 4, `ee` dp
  (0, −3, 0) for `electron_a` and (0, 3, 0) for `electron_b`, `ep` (0, 3, 0)
  and (0, −3, 0), at the read-off (tick 60) and at the end (tick 68) alike,
  4 pushes each, two per ray, at tick 50 by a field ray of 2 and at tick 53
  by a field ray of 1 (ray a at (50, 22, 24) then (53, 22, 24) by `light_b`
  heading (0, −1, 0), ray b at (46, 26, 24) then (43, 26, 24) by `light_a`
  heading (0, 1, 0)), first return none for the recoil, the first
  co-arrival with own field at tick 65 for both rays, 6 self-meetings; at
  b = 6, 8, 12 and 16, dp (0, 0, 0) for both rays in both pairs, 0 pushes,
  0 self-meetings, no first return; the control: dp (0, 0, 0), 0 pushes, 0
  self-meetings, both rays straight; without spread: dp (0, −16, 0) and
  (0, 16, 0) at b = 4 and at b = 16, 2 pushes at tick 50 (b = 4) and 56
  (b = 16) by a field ray of 16, 8 and 16 self-meetings; the fit of
  |dp_y(b)| over b for each ray and pair: 4 zeros, no exponent; the clause
  table in order (momentum sum, equal and opposite, first recoil, exponent,
  sign of the deflection, neutral control, self-meeting): pass, pass, fail,
  fail, fail (no deflection either way at b ≥ 6), pass, fail.

## A5s Coulomb at rest

`test_a5_static.py` pins the worlds and the record of experiment A5s
([register](EXPERIMENTS.md#a5s-coulombs-force-law-between-two-charges-at-rest);
`examples/nature/a5_static/`, the dictionary in its
[README](../examples/nature/README.md#a5s-coulombs-force-law-between-two-charges-at-rest)).
Five tests, the first two pinned before the first run, the third from the
measured record, the fourth and fifth before Run 2:

- the fifteen world files are byte for byte what `make_worlds.py` writes
  (`json.dumps(indent=1)` and a newline), in the order `pp_r4`, `pp_r6`,
  `pp_r8`, `pp_r12`, `pp_r16`, `pe_r4`, ..., `pe_r16`, `pp_d3`, `pp_d4`,
  `pp_d6`, `pp_d8`, `p_alone`, and each is the pinned geometry: shape
  [r + 11, 11, 11] for the axis worlds, [d + 11, d + 11, 11] for the
  diagonal ones and [11, 11, 11] for the control, open, `phase_bits` 3,
  `ticks` 2r + 32 (2 × 2d + 32 on the diagonal, 64 for the control); no
  seeds and no `ray_interactions`; body A at (5, 5, 5) of family `proton_a`,
  charge 3, amount 2^28, `momentum_table` `{"light_b": s}`, and body B at
  (5 + r, 5, 5) or (5 + d, 5 + d, 5) of family `proton_b` (charge 3) in
  `pp` or `electron_b` (charge −3) in `pe`, `momentum_table` `{"light_a":
  s}`, s = 1 for `pp` and −1 for `pe`; the control's one body A with
  `{"light_a": 1}`; the body families with rate 0, 2 slots and their
  charge, and `light_a`, `light_b` with charge 0, rate 0, 8 slots,
  `field_of` their body's family, `release` [1, 65536] and `spread`
  [6, 1, 1, 1, 1, 1], all on the six Port headings; the momentum field
  and, per light family, one unseeded lamp `idle_light_a` (`idle_light_b`)
  with an emission of amount 1 along +X with `recoil_field` momentum;
- `pp_r4.json` re-run for 8 ticks: status completed, `field_spreading`
  `field-spreading-v1`, `field_remainder` `field-remainder-v1`,
  `external_body` `external-body-v1`, `conserved_at_every_completed_tick`
  true, `released_fields` `light_a` of `proton_a` and `light_b` of
  `proton_b` at [1, 65536]; B's register after ticks 1 to 8, read from the
  `external_body_absorbed` records, (0, 0, 0) three times then (664, 0, 0),
  (1329, 0, 0), (2028, 0, 0), (2727, 0, 0), (3444, 0, 0), the pushes 664,
  665, 699, 699, 717 (the unscattered 4096 × (6/11)³ = 665 on the axis and
  what the spread adds), and A's register the negative at every tick; both
  bodies at their Nodes at every tick and no `external_body_step`; the
  ledger at tick 8: `light_a` and `light_b` each sourced 196608 (6 × 4096 ×
  8), the momentum line sourced, current, escaped and absorbed (0, 0, 0),
  the bodies' momentum line (0, 0, 0), every line balanced. (The first
  effect of the open boundary on B is due at tick 16 at the earliest, so
  these eight ticks are those of an unbounded board, and of the 16-tick
  probe at margin 8 on which the register's planning paragraph rests.)
- `record.json`, written by `analyze.py --record` from the runs of
  2026-09-17 (the register's entry holds the fingerprints): fifteen runs,
  every one completed under one recorded source, its
  `initialization_sha256` equal to the SHA-256 of the committed world file,
  its ticks the world's, every ledger line balanced and
  `conserved_at_every_completed_tick` true, the positions fixed, the
  momentum line and the bodies' momentum line zero, the window 32 ticks;
  the control's register zero at every tick with 378 absorptions and no
  first push; in every two-body world the registers equal and opposite at
  every tick; the opposite-charge series the exact negation of the
  like-charge series (the register series and the window sums); the
  measured integers, written into the test from the record: the sums of
  B's pushes over the last 32 ticks (F(r) their 32nd part) 23770, 8090,
  2872, 422 and 77 at r = 4, 6, 8, 12, 16, B's register at the end 27214,
  9608, 3501, 522 and 91, the first push at tick 4, 6, 8, 12 and 18, the
  fit of `analyze.fit` over the five points −4.142 with standard error
  0.369 (three decimals), outside the band [−2.2, −1.8]; the pushes on B
  per tick of `pp_r4`, 0, 0, 0, 664, 665, 699, 699, 717, 717, 725, 727,
  732, 732, 736, 737, 739, 741, 742, 742, 743, 744, 746, 744, 746, 747,
  748, 747, 748, 747, 749, 749, 747, 750, 748, 750, 749, 750, 750, 748,
  750; the diagonal's window sums equal on x and y and zero on z, 3019,
  1509, 447 and 158 at d = 3, 4, 6, 8, the registers at the end 3461,
  1756, 524 and 182 on both axes, the first push at tick 6, 8, 12 and 19;
  the clause table's verdicts in order: ledger pass, control pass,
  registers pass, exponent fail, signs pass, diagonal reported; and the
  clause's series of (r, F) with the same exponent for `pp` and `pe`;
- Run 2 (the dense mode, to the steady state; the register's "Run 2, to the
  steady state (dense mode)"): the six world files `pp_r12d`, `pp_r16d`,
  `pp_r20d`, `pp_r24d`, `pe_r16d`, `p_alone_16d` are byte for byte what
  `make_worlds.dense_cases` writes, in that order, `make_worlds.DENSE_TICKS`
  is {12: 196, 16: 386, 20: 622, 24: 898} (t90 + 32 for t90 = 164, 354, 590,
  866), and each is the pinned geometry: `dense_field` true, no
  `conservation` and no `polarization` key, `model_id` `a5-static-<name with
  dashes>`, shape [5r + 1, 4r + 1, 4r + 1] (the control [65, 65, 65]), open,
  the ticks of its r (the opposite-charge world's and the control's those of
  r = 16), A at (2r, 2r, 2r) and B at (3r, 2r, 2r) (the control's one body at
  (32, 32, 32)), every body at least 2r from every face; stripped of the key
  and the name, each equals `make_worlds.world` at the same margin and ticks
  (the same families, tables, lamps and fields as Run 1); `pe_r16d`'s B with
  `{"light_a": -1}` and the control with `{"light_a": 1}`;
- `predictions.json`, written by `predict_dense.py` before Run 2 (the
  boundary factor 2, the window 32, the extra ticks 32): one row per r = 12,
  16, 20, 24 with the boundary 2r, the box {shape [5r + 1, 4r + 1, 4r + 1],
  a (2r, 2r, 2r), b (3r, 2r, 2r)}, the mean field's quarter board [5r + 1,
  2r + 1, 2r + 1], t50 = 34, 94, 164, 246, t90 = 164, 354, 590, 866, the
  ticks t90 + 32, the first push at tick r, the box's steady push 25.3245,
  10.6675, 6.1929, 4.1493 and the predicted push (the mean over the last 32
  ticks) 23.1370, 9.6752, 5.6039, 3.7474 (four decimals), the predicted
  between 90 and 92 % of the steady push and above the window before it,
  and the world's ticks equal to the row's; the fits over r = 12, 16, 20 and
  12, 16, 20, 24 with the rows' points, the predicted push's exponent −2.788
  and −2.629 and the steady push's −2.769 and −2.612 (three decimals); the
  asymptote's local exponent between r = 24 and 32 −2.093 and the free-space
  band r {0.2: 21, 0.1: 26}; and the r = 12 row recomputed by
  `predict_dense.predict(12, 24)`: the same t50, t90, ticks, first push, box
  and quarter board, and the three pushes within 1e-9.

## A6 light bending

`test_a6_bending.py` pins the worlds, the small worlds, the predictions and
the record of experiment A6
([register](EXPERIMENTS.md#a6-light-bending-by-a-bound-group-and-g_eff-n²-over-n--28-to-216);
`examples/nature/a6_bending/`, the dictionary in its
[README](../examples/nature/README.md#a6-light-bending-by-a-mass)). Four
tests, the first three pinned before the series, the fourth from the
measured record:

- the forty-six world files are byte for byte what `make_worlds.all_cases`
  writes (`json.dumps(indent=1)` and a newline), in the order `turn_b4`,
  `turn_b6`, `turn_b8`, `turn_b12`, `turn_b16`, `turn_control`, `turn_2m`,
  `turn_slow`, `turn_n8`, `turn_n10`, `turn_n14`, `turn_n16`, `turn_m4`, ...,
  `turn_m16`, `turn_c_b4`, `turn_c_b6`, `turn_c_b8`, `turn_c_d3`, `turn_c_d4`,
  `turn_c_d6`, then the same twenty-three cases of the `delay` form, and each
  is the pinned geometry: `model_id` `a6-bending-<name with dashes>`, shape
  [65, 65, 9] with the star at (32, 32, 4) (the cube cases [49, 33, 33] with
  the star at (24, 16, 16)), open, `dense_field` true, no `conservation` and
  no `polarization` key, 260 ticks; the star an external body of the family
  `neutron`, amount 2^28 (2^29 in `2m`), `momentum_table` `{"mass_field":
  -1}`, absent in `control`; the launcher body of the family `launcher`,
  amount 1, `coupling` `launch`, at (0, y, z) on the ray's line, the line
  through the star's Node offset by (0, b, 0) for `b{b}` and `m{b}` (b
  negative), (0, 8, 0) for `control`, `2m`, `slow` and `n{bits}`, (0, b, 0)
  and (0, d, d) on the cube; the lamp seeded one Node below the launcher;
  `mass_field` `field_of` `neutron` with `release` [1, 32768] and `spread`
  [6, 1, 1, 1, 1, 1] at `phase_bits` 3, `neutron` at 3, the ray's family
  (`light`, rate 0; `electron`, rate 1, charge −3, in `slow`) at the case's
  width, 12 but for `n{bits}`; the `launch` rule first, its ray output on
  Port 0 with `delay` 192 and `input` 0, then the form's rule over the ray
  and `mass_field`: `mass_field_delay` with the output's `delay` `{"of": 1,
  "table": [1, 1, 1, 1, 1, 1], "per": 1}`, heading and phase `same`, and the
  field reversed from input 1; or `mass_field_turn` with `momentum_table`
  `{"mass_field": -1}` and no outputs; the lamp's emission of 2^18 on +Y with
  `recoil_field` momentum and the unseeded `idle_mass_field` lamp;
- `small_world(form)` (25 × 25 × 9, the star at (12, 12, 4), b = 4, the
  launch after 10 intervals, 40 ticks) re-run through the Simulation for
  both forms: the light at the launcher (0, 16, 4) heading +Y with steps 1
  after tick 1, heading +X with steps 0 from tick 2 to 11 (waiting), at
  (t − 11, 16, 4) heading +X from tick 12 to 35, gone from tick 36, the
  ledger balanced at the end, the light escaped whole; the turn form: no
  lag, the register None until tick 14 and (262147, −2, 0), (262153, −9, 0),
  (262164, −22, 0), (262179, −48, 0), (262203, −93, 0), (262236, −166, 0),
  (262280, −289, 0), (262332, −485, 0), (262392, −791, 0), (262264, −2189,
  0), (262230, −2499, 0), (262204, −2700, 0), (262187, −2832, 0), (262174,
  −2917, 0), (262164, −2973, 0), (262158, −3009, 0), (262154, −3033, 0),
  (262150, −3049, 0), (262148, −3059, 0), (262147, −3065, 0), (262146,
  −3069, 0) after ticks 15 to 35, the steps counting up, 124 `ray_push`
  records, the first at tick 14 at (3, 16, 4) by a field ray of amount 3
  heading −X (the register (262144, 0, 0) to (262147, 0, 0)), the escape at
  tick 36 from (24, 16, 4) with momentum (262144, −3072, 0), the star's
  register [0, 219, 0] with accumulators [−24, 2831, 0] and sink 291901, the
  launcher's sink 211; the delay form: no push, the register None, a meeting
  at every Node from tick 15 (steps 1 at every tick from 15 to 35, a fresh
  event), the lag (3, 0, 0), (−3, 0, 0), (−2, 0, 0), (−4, 0, 0), (−7, 0, 0),
  (−13, 0, 0), (−21, 0, 0), (−35, 0, 0), (−52, 0, 0), (−75, 0, 0), (−188, 0,
  0), (−63, 0, 0), (−45, 0, 0), (−31, 0, 0), (−22, 0, 0), (−15, 0, 0), (−10,
  0, 0), (−7, 0, 0), (−5, 0, 0), (−3, 0, 0), (−2, 0, 0) after ticks 15 to 35
  (on the ray's own axis alone, one meeting's delay, never accumulated,
  never a transverse component, no heading change), the escape at tick 36
  from (24, 16, 4) with the packet's momentum (262145, 0, 0) (the light's
  262144 and one field quantum), the star's register [−1, 2, 0] with
  accumulators [−11, 9, 0] and sink 291649, the launcher's sink 216;
- `predictions.json`, written by `predict.py` before the series (the release
  8192 per heading, the light 2^18, the launch delay 192, 260 ticks): one row
  per case, the transverse push on the light over its pass −3417.70,
  −1660.36, −862.41, −269.84, −94.32 at b = 4, 6, 8, 12, 16 (two decimals,
  the x and z components zero), α = atan2(|p_⊥|, p_x) of the register
  0.0130367, 0.0063337, 0.0032898, 0.0010294, 0.0003598 (seven decimals),
  the box's steady-state α 0.0130369, 0.0063340, 0.0032902, 0.0010298,
  0.0003603, the beam 8192 (6/11)^(b−1) 1329.4, 395.5, 117.7, 10.4, 0.9,
  the other side `m{b}` the same push with the opposite sign, the cube's
  axis 0.0141011, 0.0076985, 0.0047585 and diagonal 0.0063323, 0.0048648,
  0.0031079 (the diagonal push equal on y and z, zero on x), `2m` 0.0065796,
  the N scan and the slow ray as `b8`, the control 0; the axis fit −2.586 ±
  0.207, the cube's −1.562 ± 0.050, the diagonal over the cube's fit 0.4883,
  0.5880, 0.7077; the steady exponent on boards 9, 17 and 33 deep −2.585,
  −1.951, −1.587; free space at half-width 96 α 0.0142978, 0.0052398,
  0.0021331, 0.0009809 at b = 4, 8, 16, 32 with the fits −1.384 over 4 to 16
  and −1.198 over 8 to 32; and the b = 4 row recomputed by
  `predict.transient_pass` to 1e-6, 64 per-tick pushes from tick 194 to the
  Node x = 64;

- `record.json`, the committed record of the measured series (2026-09-18,
  written by `analyze.py` from the forty-six records, the expectations
  pinned from its first reading): one row per form and case with the world's
  initialization digest (equal to the file's SHA-256 in the tree), one source
  fingerprint for all, status completed at 260 ticks in the dense mode, every
  ledger balanced and conserved at every completed tick, the escape on the
  line at tick 258 = 192 + 65 + 1 (`straight`), and the light's register at
  the end of its pass: the delay form (262144, 0, 0) with no push in every
  world; the turn form (262144, −3423, 0), (262144, −1661, 0), (262144,
  −862, 0), (262144, −269, 0), (262144, −93, 0) at b = 4, 6, 8, 12, 16 from
  295, 281, 274, 248, 214 pushes, the other side the exact mirror, 2M
  (262144, −1727, 0), the N scan and the slow ray (262144, −862, 0) as b = 8,
  the cube's axis (262144, −3697, 0), (262144, −2019, 0), (262144, −1246, 0)
  and the diagonal (262144, −1169, −1169), (262144, −900, −900), (262144,
  −578, −578), the control unchanged; the register the light plus the sum of
  the pushes; the star's final register the bodies' momentum line ((0, 222,
  0), (0, 26, 0), (0, 4, 0), 0, 0 on the axis, the mirror on the other side,
  (0, 4, 4), (0, 2, 2), (0, 1, 1) on the diagonal; at most (−2, 2, 0) in the
  delay form); α = atan2(|p_⊥|, p_x) of each register. The clause table: the
  turn form's exponent −2.595 ± 0.210 (recomputed by `analyze.fit` from the
  five α), the linearity 2.0035, one register at every N with `G_eff`
  constant and the N² clause failed, the diagonal 0.4862, 0.5869, 0.7107 of
  the cube's axis fit (exponent −1.564), the light/slow ratio exactly 1.0,
  the largest deviation from the mean field 0.014; the verdicts in the
  criterion's order [pass, pass, pass, fail, pass, fail, fail, reported,
  reported] for the turn form and [pass, pass, fail, fail, fail, fail, fail,
  reported, reported] for the delay form.

## The split table's mean field

`test_mean_field_gauss.py` pins the kernel of
`examples/nature/a5_static/mean_field_gauss.py`, the computation made after
experiment A5s ([register](EXPERIMENTS.md#a5s-coulombs-force-law-between-two-charges-at-rest),
"Computed after the run"): the catalog's table [6, 1, 1, 1, 1, 1] over 11 as
the linear map it is on average, per-heading amounts in floating point on a
box whose open faces absorb and whose mirrored faces are symmetry planes.
Three tests, written before the first run:

- the split of one heading's content at one Node: 11 arriving on +X at the
  centre of a 3^3 box leaves 6 on +X, 1 on -X and 1 on each of +Y, -Y, +Z, -Z,
  nothing elsewhere, the total 11 kept and the net momentum of the departures
  (6 - 1, 0, 0); 1 arriving on +Y leaves 6/11 on +Y, 1/11 on -Y and 1/11 on
  each of +X, -X, +Z, -Z (the Port order relative to the arriving heading);
  the split is linear, 11 on +X with 22 on -X leaving 8 on +X, 13 on -X and 3
  on each transverse Port, total 33; the simple walk [1, 1, 1, 1, 1, 1] sends
  6 on +X as 1 through every Port; the diffusion constants of the two walks
  are 4/9 and 1/6 Links^2 per interval;
- conservation: 11 on +X at the centre of a 9^3 box with no source and no
  sink keeps the total 11 exactly through ticks 1 to 4 (the front inside the
  box) and loses content to the open faces from tick 5, monotonically; the
  source releasing 4096 on six headings with its own sink has the totals
  6 x 4096 = 24576, 12 x 4096 - 6 x 4096 / 11 = 46917.82 and 18 x 4096 -
  12 x 4096 / 11 = 69259.64 after ticks 1, 2 and 3 (each tick from the second
  returns the six backward shares of the fresh releases, 6 x 4096 / 11, to the
  source's sink), its push (0, 0, 0) at every tick, and the octant of a 5^3
  box with three mirror planes holds the same field on the stored part as the
  full 9^3 box, to 1e-9;
- the beam: a sink at (r, 0, 0) with the boundary 6 Links from both bodies
  has no push before tick r; at ticks r and r + 1 the push on x is exactly
  4096 x (6/11)^(r-1): 4096, 2234.1818, 1218.6446 and 664.7153 at r = 1, 2,
  3, 4 (the engine's integers of A5s, 664 then 665 at r = 4, are this share
  under the remainder rule), zero on y and z; at tick r + 2 the first
  detoured content arrives and the push exceeds the beam for r = 2, 3, 4; at
  r = 1 (the source's neighbour) the first detoured content arrives on a
  transverse heading and the push on x stays 4096 through tick 4.

## The helium orbit

`test_helium_orbit.py` builds the E8 world
([the helium ion with the field spreading and the momentum turn](../examples/nature/README.md#the-helium-ion-with-the-field-spreading-and-the-momentum-turn))
inline on the smallest board that holds it: an open 7^3 lattice under the shared
Detector admission (schema 1, `link_ticks` 1, `metric: "links"`, pace 1/1, no
decay, the six unit-axial headings, `phase_bits` 8), the same families, rules
and bodies as `examples/nature/helium_orbit.json` with the radius 2 in place of
6, a hold of four intervals in place of forty and twelve ticks in place of 152.
The nucleus is a `proton` body of amount 2^20 and charge 6 at (3, 3, 3) under
`phase_plate`, with `momentum_table` `{"light_of_nucleus": -1}`; its light,
`field_of` `proton` with `release` [1, 749] (A = 1399 per heading per
interval) and `spread` [6, 1, 1, 1, 1, 1], has 24 ray slots, the three one-ray
families (electron 4, proton 2, launcher 2) the rest of the layer's 32; the
electron of amount 256 (rest rate 1, charge -3) is emitted along +Y from a lamp
at (5, 1, 3) with its recoil on the lamp's `momentum` vector; the `launcher`
body (an apparatus family, amount 1) at (5, 2, 3) with the coupling `launch`
(guard `eq(phase of the electron, 1)`, the electron returned on its heading with
`delay` 4, the token unchanged); `nucleus_turn` over `[electron,
light_of_nucleus]` with `momentum_table` `{"light_of_nucleus": -1}`; the
rules in the order `launch`, `nucleus_turn`, `phase_plate`. One test, run
through the runner, read from `run.json` and `events.jsonl`.

Written before the first run (the structure): the electron arrives at the
launcher at tick 1 with phase 1, the guard holds and it waits four intervals,
no arrival being recorded while it waits and no push reaching it (a delayed
ray is not met); it leaves on +Y and arrives at the tangent point (5, 3, 3) at
tick 6, where the spreading field is already present (the body's release
reaches the neighbours at tick 1 and every Node of the board within a few
ticks), so `ray_push` records appear from tick 6, one per field ray at the
Node in slot order, `family` electron, `amount` 256, `field` light_of_nucleus,
each `after` the `before` moved by -1 x field amount x field heading, the
register starting at (0, 256, 0), the +X beam of the axis the largest push and
the +Z and -Z content cancelling in pairs; the register's -X component sends
the electron down the axis to the nucleus, which it reaches at tick 8 and
passes (`phase_plate`, which assigns the heading and so clears the register to
(0, 256, 0)); at the nucleus's Node the sink takes every field ray before the
meeting, so no push is recorded there; on the +Y line the whole axis ray
(1399) pushes it back, the two-Link cage of E4, so the electron alternates
between (3, 4, 3) and (3, 3, 3) from tick 8 to tick 12; the runner records
`ray_momentum_turn`, `field_spreading`, `field_remainder` and `external_body`;
the electron total is 256 at every tick, none escaped; the light line reads
sourced = current + escaped + absorbed at every tick (the registers counted as
current); the momentum line's `current` equals its `sourced` (the lamp's recoil
against the ray's register, the pushes and reversals booked as the meeting's
source); every ledger line is balanced and `conserved_at_every_completed_tick`
is true.

Read from the record of the first run of this board (2026-09-17) and pinned
then, as the run's integers rather than computed by hand (the field's integer
state at tick 6 is the sum of many spreads); re-read under
`ray-momentum-turn-v2` on 2026-09-17 ([the walk kept through a
push](#the-walk-kept-through-a-push)) and unchanged, since the kept walk
takes the same Links here: the electron arrives at (5, 3, 3) with its
accumulators at zero and leaves -X (743 against 277 on the register
(-743, 277, 0)) with (-277, 277, 0), which every register of the pushes of
tick 7 holds and against which (4, 3, 3) is left -X again (1080 against 557
on (-1357, 280, 0), length 1637), and the cage's pushes start from the fresh
output of `phase_plate`: the pushes of tick 6 at (5, 3, 3),
(before, after, field amount, field heading): ((0, 256, 0), (-785, 256, 0),
785, +X), ((-785, 256, 0), (-743, 256, 0), 42, -X), ((-743, 256, 0), (-743,
277, 0), 21, -Y), ((-743, 277, 0), (-743, 277, -22), 22, +Z), ((-743, 277,
-22), (-743, 277, 0), 22, -Z); of tick 7 at (4, 3, 3): ((-743, 277, 0),
(-2142, 277, 0), 1399, +X), ((-2142, 277, 0), (-1357, 277, 0), 785, -X) (the
recoil of the +X push of tick 6, walking with the electron, pushes back),
((-1357, 277, 0), (-1357, 233, 0), 44, +Y), ((-1357, 233, 0), (-1357, 280, 0),
47, -Y), ((-1357, 280, 0), (-1357, 280, -47), 47, +Z), ((-1357, 280, -47),
(-1357, 280, 0), 47, -Z); at tick 9 seven pushes at (3, 4, 3) from (0, 256, 0)
to (-17, -1036, 0) and at tick 11 eleven from (0, 256, 0) to (-8, -1099, 0);
pushes at ticks 6, 7, 9 and 11 only. The light line (sourced, current,
escaped, absorbed) after tick 5: 41970, 34466, 3411, 4093; tick 6: 50364,
38801, 6116, 5447; tick 8: 67152, 44680, 13109, 9363; tick 12: 100728, 51215,
31967, 17546. The momentum line, sourced and current alike: (0, 0, 0) after
ticks 5 and 6, (-1357, 24, 0) after tick 8, (-8, -1355, 0) after tick 12. The
bodies' momentum: (0, 0, 0) after ticks 5 and 6, (1197, 3, 0) after tick 8,
(1169, 2398, 0) after tick 12, the nucleus's final momentum; its sink 17546
of light at tick 12; the nucleus at (3, 3, 3) at every tick.

## The dense mode

`tests/test_dense_field.py` is the isolated test of the dense mode for boards
that a field fills (`dense_field: true`, `dense-field-v1`;
[performance](PERFORMANCE.md#the-dense-mode-measured-before-adoption-2026-09-17),
[field spreading](SPATIAL_FIELDS.md#field-spreading-field-spreading-v1)),
pinned here on 2026-09-17 before its first run. It builds the boards of the
field spreading test (the same builders, loaded as data) with `dense_field`
on and without the local audit, which the mode rejects. Four cases:

- `split`: one cycle of the region at (6,7,7) against `spread_content` on the
  same rays and registers, the departures read from the arrays as (Port, sign,
  amount, phase, bit) rows and the eighteen registers with their phases. The
  single ray of 12 at phase 6 on +X leaves 6 forward and 1 on each other
  heading at phase 6 and fills the sign-0 block (6, 1, 1, 1, 1, 1) at phase 6;
  two rays of 3 of opposite sign on +X leave 1 forward each (sign -1 and sign
  1, phase 0) and fill both blocks (7, 3, 3, 3, 3, 3); one quantum on a forward
  register of 10 releases one forward at phase 0 and leaves (5, 1, 1, 1, 1, 1);
  and a mixed Node (7 at phase 1 with bit 1 on +X, 5 at phase 5 on -Y, 9 at
  phase 2 of sign 1 and 2 at phase 6 of sign -1 on +Z, the registers 1 to 18 at
  phases 3 x slot mod 8) gives the departures, the registers and the phases
  `spread_content` gives, every departure carrying bit 1 (the highest), the
  stored quanta the difference of the blocks over 11 and the (1, +Z) register
  changed. The region cycles one Node. A packet from an engine Node with three
  rays of 4 on +X at phases 1, 2 and 3 (one sign): the third ray is kept whole
  beside the two layers of the arrays, the Node reads back with the three rays
  resident, the mask of the -X face and one packet received, and the cycle
  spreads the twelve at the phase of the sum, 2, as `spread_content` does,
  the kept ray consumed.
- `boundary`: the `source` world of the field spreading test (a record of
  four electrons at (5,7,7) releasing light of sign -1, one per heading, every
  interval; a Detector at (8,7,7) with setting [0, 1]), twelve ticks. The
  Detector's Node, the record's Node and the Nodes a returned quantum walks
  back through are the engine's, every other Node the region's: (7,7,7) is
  the engine's after ticks 7 and 11 and (6,7,7) after 8 and 12, both the
  region's after ticks 1 to 6, 9 and 10 ((7,7,7) goes back to the region when
  it next receives content, one tick later than (6,7,7) does). The same
  integers as the engine alone: light 6 t per tick less 1 from tick 10, the
  source line equal, nothing escaped, the ledger balanced; the returns at ticks
  6 and 10, the `field_returned` at tick 9 at (5,7,7) by `electron`, not
  restored; after tick 12 (6,7,7) holds the twelfth release (heading 0, 1,
  phase 0, sign -1) and the second returned quantum (heading 1, 1, outbound 0,
  bit 0, sign -1), (7,7,7) one quantum of the release and the registers of sign
  -1 (8, 5, 5, 5, 5, 5), (8,7,7) nothing; the engine records `field_spread` at
  (7,7,7) at ticks 7 and 11 only, the region's cycles there recording nothing.
- `identity`: the `single` world for four ticks and the `source` world for
  twelve, run through the runner with the engine alone and with the mode:
  equal `state.json` digests, equal `audit` lists and final totals, the run
  record `dense_field: "dense-field-v1"` only when on, `events.jsonl` different
  (a dense Node writes no per-Node events); the runner's `--dense-field` flag
  gives the same `state.json` as the world's key.
- `rejected`: with `dense_field` on, a world with `conservation` (the local
  audit), a world without a spreading family, a spatial field without ray
  transport, a family with `polarization_bits` and a ray interaction whose two
  participants are the spreading family are rejected at initialization with
  the named reason; `node_workers` 2 is rejected at the simulation; a world
  without the key runs the engine alone (`dense_field` false, no region).
