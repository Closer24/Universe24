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
| `test_dense_field.py` | 3 | 1.0 | The dense mode for boards that a field fills (`dense-field-v1`, [performance](PERFORMANCE.md#the-dense-mode-measured-before-adoption-2026-09-17)): the pure-field Nodes cycled as one vectorized step, one split step equal to `spread_content` (the registers, the releases, the phases, the bit), the hand-over of rays between the region and the engine's Nodes both ways, the same `state.json` and ledger as the engine alone, the unsupported worlds rejected, pinned below |
| `test_perf_arrays.py` | 8 | 9.2 | The performance lane of 2026-09-18 (`perf-arrays-v1`, [performance](PERFORMANCE.md#snapshots-from-the-arrays-parallel-series-runs-and-the-standing-set-2026-09-18)): `state.json` written Node by Node from the engine and the dense arrays, byte for byte `json.dumps(snapshot)`; a series run one process per world byte-identical to a single run; the standing set (`standing-field-v1`): the layer kept fixed from its exact repeat, the things reading it as the stepping engine gives, the run's files identical, the fallback when a thing steps, the residual without a repeat, the refusals, pinned below |
| `test_bit_law.py` | 19 | 2.2 | Feature 15, the law of the bit (`bit-law-v1`, the model owner's decision of 2026-09-18, Highlights 5.4): every ray carries one bit, 1 a thing and 0 its shadow, a ray of the same family; a shadow pushes a thing and walks home with -dp, home to a body and to a thing ray; a shadow meets its own thing without a push; a mark returns a shadow and counts nothing, catches things by its counter; the ledger's `returned` line and the things' own identity; the trace; the bit never changes; the things' content is constant between absorptions; a shadow-only board makes no event and the dense layer equals the engine; no lottery, two runs byte-identical; the retired keys rejected, pinned below |
| `test_clock_readings.py` | 8 | 0.5 | Feature 16b, the clock is the content, the two readings and the decay table (`clock-readings-v1`, Highlights 5.4 points 11, 16, 18, 19, 20): the computation per tick is the things' phase steps and is constant between absorptions; a shadow has no clock and two contents are two clocks; K and N bound the content at parsing and at a meeting; a neutral thing has gravity and no electric push, a charged thing's push below one quantum accumulates exactly on its remainder; a bound group breaks by its declared table, byte-identically, and `draw` is refused, pinned below |
| `test_wait_rule.py` | 6 | 0.4 | Feature 16b, a thing pays a tick for every whole quantum it reads (`clock-readings-v1`, Highlights 5.4 point 23): one quantum read, one interval without a Link, a step or a phase step; a shadow pays nothing; w = 2 doubles the wait; no reading, no wait; a rational w kept exactly, pinned below |
| `test_node_is_ports.py` | 7 | 1.5 | Feature 17, a Node is its six Ports (`node-is-ports-v1`, Highlights 5.4 point 22 and the settled rules): the parked shadow below one quantum in units of the split's denominator, the engine and the dense layer agreeing; the trace as a zero-amount shadow and the return that follows it to the mark, home to the resident thing on its shadow line with no click (M8); a prefilled shadow of a loop at its Link distance from its owner, absorbed and re-released with the `returned` momentum exact (M9); the record's fixed terms, no register, counter, seed or trace key (M13); a seeded thing missed at a mark restored to its lamp and re-emitted (M14); a source that spends its content, nothing sourced; a mirror thing returning a thing and a shadow |
| `test_return_field.py` | 4 | 0.9 | Feature 16d, the return is a field (`return-field-v1`, Highlights 5.4 point 3 as amended): the inverted share leaving the pushed body reversed and mixing, the owner's momentum line receiving what reaches it with the books exact per interval and the momentum in flight on the shadows (a); a returning share pushing a third thing with the opposite sign (b); a returning share absorbed at its owner with no push (c); no trace, no wait, every share moving, the identity recorded (d) |
| `test_lanes.py` | 9 | 2.0 | Feature 18, a Port is two lanes (`lanes-v1`, Highlights 5.4 point 25, the model owner's decision of 2026-09-18): a Node's state is twelve lanes with one real slot and one shadow slot per owner on each, addressable as [Port][lane][real \| shadow(owner)] beside the parked shadows and the rays at rest; two reals declared on one lane refused, a table with two outputs on one heading refused, a sweep that repeats a heading refused, each naming point 25; the lane a condition on the step, the thing already on the heading keeping it and the other continuing on its own heading with its momentum kept and stepping at the next Node, one Link per interval, the books exact; two owners' shadows sharing a lane in one slot each with the sums exact; two reals of one family given one lane one real ray (amounts, momentum and charge exact, the phase the coherent sum's, the owners a set) that is home to a shadow of each owner, things of two families on one lane refused; the record of a world with no contested lane byte-identical, pinned below |
| `test_detector_absorb.py` | 3 | 1.1 | Issue #169 feature 2c: a click on a field family absorbs the quantum into the mark's counter with its momentum on the marks' line, booked as `absorbed_by_marks` in the world ledger and the local audit, nothing of it delivered or spread on; matter passes with the bit 1; `on_click` per family, its defaults and its validation (`detector-absorb-v1`), pinned below |
| `test_detector_mark.py` | 1 | 0.18 | Issue #169 feature 2: a marked Node draws one bit per arriving ray (`detector-mark-v1`; feature test, untouched) |
| `test_detector_return.py` | 6 | 0.40 | Issue #169 feature 3: a draw of 0 returns the ray reversed on its line, through no coupling, to rest at its event Node (`detector-return-v1`) |
| `test_disturbance_application.py` | 14 | 0.29 | Runner record: headless run files, the saved initialization and source fingerprint that replay a run, explicit CLI opt-ins |
| `test_disturbance_engine.py` | 23 | 0.02 | Carrier Node cycle: budget wait, fixed Link time, split and whole-record transport, exchange remainders, capacity-failure atomicity |
| `test_energy_audit.py` | 9 | 0.31 | Funded ray emission with recoil and absorption under the audit (running branch, untouched) |
| `test_field_spreading.py` | 6 | 0.90 | Issue #169 feature 12: every Node that field content reaches releases it again by the family's split table, amounts adding per heading, the phase of the coherent sum, whole quanta leaving and the shares below one quantum owned by the Node's remainder registers until they reach one (`field-spreading-v1`, `field-remainder-v1`); the source sign on the field ray; a returned field quantum walking back until something takes it |
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
| `test_momentum_turn_walk.py` | 4 | 7.8 | Deleted on 2026-09-18 under `clock-readings-v1` (the DDA walk and the output-clock delay of a departure are retired: every ray moves one Link per interval); The fix of `ray-momentum-turn-v2`: a push keeps the DDA's accumulators, so a ray pushed at every interval walks the DDA line of its running register; the staircases of a push of 1 and of 8 per interval on a ray of 64, the flip, the cancel, the shrink and the lift by hand, and two boards where a field ray meets the ray at every Node |
| `test_native_ray_coupling.py` | 33 | 0.04 | Ray interactions, the generic coupling (running branch, untouched) |
| `test_nature_catalog.py` | 4 | 0.12 | Data gate: `catalog/nature.json` parses, every record and reference resolves, every undecided entry names its decider and is tabled in `CATALOG.md`, the register's entries agree, and every runnable ray and decided coupling is built from the file and run for two ticks (pinned below) |
| `test_node_conservation.py` | 13 | 0.00 | Pre-commit conservation readout guard and its bounded readout cache |
| `test_node_rule_contract.py` | 37 | 0.00 | Node profile contract: explicit k*h duration, indexed vector rules, aggregation policies |
| `test_node_state_contract.py` | 9 | 0.31 | Node-state contract: evolving state is formula-free |
| `test_payload_validation.py` | 26 | 0.00 | Signed and unsigned integer codes (zigzag) validate exactly as the decoding reference, without decoding |
| `test_phase_spread.py` | 11 | (first run) | Feature 16a, the phase-steered spread (`phase-spread-v1`, Highlights 5.4 point 17, the model owner's decision of 2026-09-18): the shares of one owner that meet at a Node steer each other by the Born table, each continuing on its heading by its phase difference to the others and sending the rest apart; a lone share keeps the split table; different owners and differing polarizations are lone to each other; the table written from the phase width, never declared; the dense layer agrees, pinned below |
| `test_plan_reuse.py` | 10 | 0.37 | Exact transition plan reuse: every argument of a law is its key, the world tick is not (a Node in a steady field reuses its plan across ticks, a lamp whose stock counts down does not), and a plan is validated once, when it is made, a hit being served without a second check, pinned below |
| `test_rational_particles.py` | 16 | 0.47 | Opt-in bounded rational ratios: balanced routes, fractional credit, local checks |
| `test_ray_coupling_evidence.py` | 3 | 0.00 | Evidence helper of the ray coupling (running branch, untouched) |
| `test_ray_delay.py` | 6 | 12.78 | Deleted on 2026-09-18 under `clock-readings-v1` (the DDA walk and the output-clock delay of a departure are retired: every ray moves one Link per interval); Output clocks: rays wait at a loaded Node and the phase per interval shows the wait |
| `test_ray_event_audit.py` | 3 | 0.90 | Issue #169 feature 10: the world ledger per completed tick, exact for amount, momentum and charge through a return, an inverse split, a release, an escape and an external body's sink (`ray-event-audit-v1`) |
| `test_ray_field.py` | 22 | 0.31 | Straight ray transport: DDA heading, emission sweep and shares, shell stock, slots, escape |
| `test_ray_hidden_state.py` | 1 | 0.19 | Issue #169 feature 1: every ray carries its event and its steps (`ray-event-state-v1`) |
| `test_ray_layers.py` | 1 | 0.14 | Issue #169 feature 5: rules of different layers fire in one interval and an unruled family crosses (`ray-layers-v1`) |
| `test_ray_integration_guards.py` | 22 | 0.36 | Ray integration boundaries (running branch, untouched) |
| `test_ray_meeting_conversion.py` | 6 | 0.25 | Issue #169 feature 6: a meeting replaces its rays by declared outputs, an amount split by a declared table, every family's stock exact (`ray-meeting-conversion-v1`) |
| `test_ray_merge_contracts.py` | 16 | 0.04 | Ray merge and ownership boundaries (running branch, untouched) |
| `test_ray_polarization.py` | 7 | 0.30 | Issue #169 feature 11: polarization as a ray property, a transverse direction modulo a half turn in steps of the family's polarization circle or none, declared by a lamp, part of the merge identity, carried by a meeting's outputs from their source input unless declared, by a spread as the axial mean and by the return; the polarizer, an external body's coupling splitting an arriving ray by its declared table at the difference between the body's angle and the ray's polarization, the pass share on the pass Port with the body's angle, the rest in the sink, the shares below one quantum in the body's registers (`ray-polarization-v1`) |
| `test_ray_momentum_turn.py` | 5 | 0.90 | Issue #169 feature 8b: a free ray's direction is its momentum register, walked by the DDA one Link per interval, pushed by the field rays a coupling's `momentum_table` names, the field ray returned reversed (`ray-momentum-turn-v1`; the walk kept through a push since `ray-momentum-turn-v2`, [the walk kept through a push](#the-walk-kept-through-a-push)) |
| `test_ray_viewer.py` | 6 | 0.2 | Tooling: `tools/ray_viewer/extract.py` reads a runner record into rays, events and captions, the style file, its GIF presets, the compressed inline page, the events camera fit and the GIF palette that keeps the families' colours, pinned below (no browser) |
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

Re-pinned on 2026-09-18 under `clock-readings-v1`: the families of these worlds declare no rate (their phases stay), `two_lamps(steps, advance)` declares `clock` and K 2 / advance (rays of 2), the tests of a ray's own advance (`kerengonen_advance`) and of the carried advance are deleted with the key, and the attenuated self-exclusion world is the plain one.

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
| `test_energy_audit.py` | Funded emission along (1,0,0) and (0,2,0) debits the emitter by 2 per tick and recoils by (-1,-2,0) per tick with the audit closed; a stock of 5 emits 2, 2, 1, 0; `source: true` is still rejected and `recoil_field` needs funding; escaped quanta are measured escape; an absorber banks five quanta with momentum (5,0,0) while quanta beyond it vanish and the audit stays closed; a moving absorber-emitter never eats the wake of the cycle it departed on, and since `ray-event-state-v1` the quantum of the cycle before, a distinct event travelling with it, is absorbed back from the third tick on (38, 36, 36, 34, 34 since feature 18 on 2026-09-18, the quantum of the cycle before and the new one leaving on one lane as one real ray of two quanta with the older event's record; 38, 36, 35, 34, 33 under ray-event-state-v1 alone; 38, 36, 34, 32, 30 when the two cycles merged); absorb validation rejects a scalar momentum field and an amount key; a fraction 1/4 absorbs one quantum of each 4-quantum ray and forwards 3; negative quanta pull an absorber with stock 3 by (-2, -1, 0, 0) and credit the emitter 16 with recoil (16, 0, 0); a ray field cannot be both absorbed and exchanged |
| `test_kerengonen.py` | A phase advances by the field's step on every link and wraps, a plain field leaves it alone, and rays merge only with equal phase; the cosine table for four steps is (256, 0, -256, 0), equal phases give coherence exactly one, opposite equal amounts exactly zero and a quarter turn one half; two lamps three links from a Node fire 2-quantum rays at each other and the sampled values along the line are 4, 0, 4, 0, 4 with four steps and 4, 2, 0 with eight, while the plain field reads 4 everywhere and the audit closes on 800 quanta; an absorber between the lamps takes 4 quanta before the opposite pair arrives and nothing after, takes 20 at the in-phase Node, and 20 at the dark Node when the second lamp is offset two steps; the runner records `kerengonen-ray-field-v1` and rejects one phase step, an advance equal to the steps, a missing advance, an emission phase beyond the steps, a phase without the key and the key without ray transport; the double-slit probe composes and closes; the bounded ticket rule advances and squares as specified and no absorber draws from it, the share rule takes 2 whole single quanta at a quarter turn where a half share truncates to nothing (closed on 800 quanta), and an unknown capture, the deleted lottery capture and a capture seed are rejected; a slit that re-emits the phase it absorbed makes a lamp's wave arrive at a Node three links on opposite to a second lamp's (reading 0), equal with that lamp offset four steps (4), and partial at a fixed re-emission phase (3), and a carried phase without an absorb rule is rejected; a ray with its own advance ignores the field's, rays of different advance do not merge, beams of momentum 16 and 32 at advance |p|/4 carry advances 4 and 8 with phases in ratio two after the same links, a negative advance and one without the key are rejected, and a slit re-emits the absorbed advance so readings are 2, 4, 0 for lamp offsets 0, 16, 48 on a 64-step field; a mirror sends a lamp's wave back along -x with the carried phase, holds 4 quanta and the reversed momentum, closes on 400 quanta, and the line reads 0, 2, 5, 7, 7, 5, 2, 0, 0, 2, 5 at advance 4 (period 8) and 6, 1, 1, 6 repeating at advance 8 (period 4); a mirror without every image heading, without a recoil field, on an unknown axis or without an absorb rule is rejected; a three-layer screen's first layer absorbs exactly what a one-layer screen does and the layers behind add to it, both worlds closed; a dissolving record of 10 quanta with after 3 and over 4 holds 10, 10, 10, 7, 4, 1, 0 and a moving one flies while it holds quanta and stops at x = 2 when empty, both closed; dissolution on a sourced emission, an emission without amount or dissolve, and over_ticks 0 are rejected; on the Euclidean metric the integer square root is exact at 0, 1, 2, 3, 4, 15, 16, 17 and a million, the paces of an axis, face and body diagonal are 2364/4096, 2364/2896 and equal, twelve ticks carry the first axis ray 6 links, the face diagonal 9 and the body diagonal 12, the world closes on 400 quanta and an unknown metric is rejected; a diagonal `xy` mirror returns the +x ray along +y with nothing back along -x, and a quarter-fraction mirror passes 3 of every 4 quanta and returns 1, closed; a directed emitter with `heading` fires every ray along -x and closes, and a heading outside the field's list or combined with a mirror is rejected |
| `test_ray_hidden_state.py` | Every ray carries its event and its steps ([ray hidden state](#ray-hidden-state)): a sweeping lamp's six rays carry mask 63 and shares (3, 3, 3, 2, 2, 2) with steps and phase equal to the tick; rays of two events with one heading and phase stay two rays in the pure function, and in the world A's +X ray and B's emission given one lane at B's Node are one real ray of 7 at the coherent sum's phase 1 with owners (2,) from tick 3 (feature 18, lanes-v1, 2026-09-18: 7t - (t - 2) rays after t ticks); a returning ray walks steps 5 to 0 and phase 1 to 4 backward, is kept resident at steps 0 and is refused a Link beyond its event Node; 1200 quanta and zero momentum every tick, the audit passed, the runner recording `ray-event-state-v1` |
| `test_ray_layers.py` | Rules of different layers fire in one interval and an unruled family crosses ([ray layers](#ray-layers)): five rays of families a, a, b, b, c meet at one Node after tick 2; after tick 3 the a rays have swapped headings (mask 3, shares (5, 5, 0, 0, 0, 0), steps 1), the b rays have turned to +Z and -Z at phase 7 (mask 48, shares (0, 0, 0, 0, 5, 5), steps 1) and the c ray is one Link past the Node unchanged (mask 16, steps 3, phase 3); the derived layers are (a), (b), (c) whether or not the b rule is declared, and without it the b rays cross like c; totals 10, 10, 5 and zero momentum every tick with the audit passed, the runner recording `ray-layers-v1` and the layer families |
| `test_detector_mark.py` | A marked Node draws one bit per arriving ray ([Node Detector bit](#node-detector-bit)): six lamps around one marked Node with setting 1/2 and seed 3 arrive in one interval and draw (0, 0, 0, 1, 1, 0) in Port order, exactly two clicks (Ports 3 and 4, amounts 4 and 5), the two rays that drew 1 leave with `detector` 2 and continue unchanged while the four that drew 0 leave with `detector` 1 reversed and rest at their lamps from tick 2 on, the marked and the unmarked control world agree on totals, momentum and lamps at every tick, the control consumes no ticket, a replay writes the same events and run record, the runner records `detector-mark-v1`, and a mark without a setting, a setting above 1, a zero denominator, a seed at the modulus, a duplicate or outside position and a world without an admitted ray field are rejected |
| `test_detector_return.py` | A draw of 0 returns the ray ([Detector return](#detector-return)): for each of the six unit-axial headings a lamp's ray of 8 is halved by an absorber one Link before the marked Node, drawn 0 there at tick 3 (seed 3, setting 1/2), reversed with `outbound` 0 and no click, walks back one Link per tick with steps 3, 2, 1, 0 and phase 3, 2, 1, 0, crosses the absorber untouched, reaches the lamp at tick 6 with the phase it left with and, since `inverse-split-v1`, is restored to the lamp (a one-line event has no sibling line; the lamp holds 4 and momentum -4u after tick 7) and emitted again by it as a new event of 4 after tick 8, 8 quanta and zero momentum every tick, one `detector_return` and one `inverse_split` event, the runner recording `detector-return-v1` and `inverse-split-v1`, and a returning ray at an open boundary refused |
| `test_inverse_split.py` | A returned ray at its event Node performs the inverse split by the world's `return_mode` ([Inverse split](#inverse-split)): a pair lamp at X sends 4 quanta each way on one line, arm A's ray is returned at a marked Node three Links out and reaches X at tick 6; at tick 7 in `siblings` and `straight` a transmission of 4 with A's phase 0 and bit 0 leaves X on arm B's line and never shares a Node with B (B is 6 Links ahead, the round trip), the lamp holding 0 quanta and momentum 8u; in `annul` the share ends at X, the lamp unchanged and `annulled_totals()` 4 quanta and momentum 4u; totals, momentum, the spatial accounting and the conservation report exact at every tick, one `inverse_split` event, the runner recording `inverse-split-v1` and the mode, and an unknown mode rejected |
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

Re-pinned on 2026-09-18 under `clock-readings-v1`: no rate, no clock; A's rays keep phase 0 and the returning ray of (c) keeps phase 1 on its walk back; `forward_rays` returns three values.

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

Re-pinned on 2026-09-18 under `clock-readings-v1`: the family declares no rate, so the continuing and returned rays keep phase 0.

Re-pinned on 2026-09-18 under `bit-law-v1` (point 14, no lottery): the mark's setting is its counter table, the k-th arrival catching the bit 1 when k mod 2 < 1, so the bits are (1, 0, 1, 0, 1, 0) in Port order and the counter stands at 6; the seed is retired; the mark declares `on_click: "pass"` so that a thing that draws 1 walks on as before; a click and a return name the thing's owner (`tests/test_detector_mark.py`).

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

Re-pinned on 2026-09-18 under `clock-readings-v1`: the family declares no rate and no clock, so the phase column of the tick table is 0 throughout (the shares of one emission are of several amounts, which no one K makes one step per Link).

Re-pinned on 2026-09-18 under `bit-law-v1` (point 14): the mark's setting [0, 1] is a counter table that catches nothing and returns every thing (the draw of 0 of the old world); the seed is retired, the counter stands at 1 after the one arrival, a return names the owner (`tests/test_detector_return.py`).

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

Re-pinned on 2026-09-18 under `clock-readings-v1`: no rate, no clock; every phase pinned as the Links walked is 0.

Re-pinned on 2026-09-18 under `bit-law-v1` (point 14): the mark's setting [0, 1] returns every thing; no `bit` on an `inverse_split` record; a return names the owner (`tests/test_inverse_split.py`).

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

Retired on 2026-09-18 under the law of the bit (`bit-law-v1`): `tests/test_detector_bit_property.py` pinned behaviour the law removed and is deleted; the run is repeated under the law in a follow-up (the worlds stay in `examples/`).

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

Re-pinned with feature 18 (`lanes-v1`, 2026-09-18): the case `a_and_b` was deleted; with the b rule declared a turned b ray and the c ray are given one lane at the meeting Node, two real rays of different families, a meeting the table of the pair decides and no departure holds (the model owner's decision of 2026-09-18 on the case feature 18 left open), and the world declares no such table. The case `a_only` stands as pinned.

## The law of the bit

Re-pinned on 2026-09-18 under `return-field-v1` (feature 16d, Highlights 5.4 point 3 as amended; `tests/test_bit_law.py`): a shadow that pushes turns back with the opposite sign and is a field from then on, a mark returns a shadow as it is, and no trace is left anywhere. (a) no trace beside the body's ninths at (2,2,2) or at (1,2,2); (d) the returned shadow, an outgoing share, mixes at (5,2,2) in the cycle of tick 3 and parks 4 on -X and 1 on each other heading; (h) the re-released shadow reaches the mark in the thing's delivery, is returned before the thing is resident and parks at (3,2,2) (4 on +X, 1 each other way), nothing absorbed at home in five ticks, the resident's shadow line 0; (j) the inverted shadow rides the Link to (3,y,2) with the thing it pushed and pushes it again there (the same push), so the things carry twice the push after tick 3 and the shares, outgoing again at (2,y,2), carry twice -dp.

Re-pinned on 2026-09-18 under `clock-readings-v1` (feature 16b): `m` declares `clock` where a rate was declared and the world K (world (a): K 2, a thing of 2 one step per interval); a body of 100 quanta declares its whole charge -100, so the electricity reading (the owner's charge over its content times the thing's charge per quantum) gives the pushes of the first pin; a thing's `momentum` on the ray is the pushes it carries ((-1, 0, 0) after the push of (a), (push, 0, 0) in (j)) while the register line stays amount x heading plus that; the momentum line carries `spent` (0 here); `wait_per_quantum` is 0 in these worlds.

Re-pinned on 2026-09-18 under `node-mixing-v1` (Highlights 5.4 point 24, feature 16c; `tests/test_bit_law.py`): these worlds declared no split table, so their shadows walked straight to what they were to meet; under point 24 every shadow of a family with a shadow set mixes at every Node with nothing else there, and a lone quantum parks its ninths and goes nowhere. Every shadow that is to meet a thing, a body or a mark now leaves fresh (`steps` 0) from the Node beside it and arrives there in the first delivery, and a return whose one step is spent waits where it is (node-is-ports-v1, rule (ii)), so the meetings are at tick 1 or 2 and the geometry adjacent: (a) the body at (3,2,2), the push at (2,2,2) in the cycle of tick 2, the thing absorbed and the shadow home at tick 2 (`returned_to_body` (2, (3,2,2), amount 1, momentum (1,0,0))), the re-released quantum parked at (2,2,2) from tick 4 in ninths (4 on its back heading, 1 on each other) beside the thing's trace, contents [2, 0, 0, 0, 0], shadows [1] x 5; (b) the bodies at (2,2,2) and (3,2,2), a push at the delivery of every odd tick and a receipt at every even one, so the momenta are (-t, 0, 0) and (t, 0, 0) after tick t, six ticks; (c) the homecoming at (2,2,2) at tick 1, the shadow riding with the thing at (3,2,2) after tick 2 (steps 1 beside steps 2) and mixing there; (d) the returned shadow waiting at (5,2,2) from tick 2 with steps 0, everything else as pinned; (e) with the 11s: after tick 1 (5,2,2) holds 1 on +X, (6,2,2) 4 on +X and (3,2,2) 4 on -X, twelve Nodes, after tick 2 (6,2,2) 1 on +X and (3,2,2) 1 on -X, after tick 4 no ray, the registers (8, 8, 5, 5, 5, 5) at (4,2,2) and (5, 2, 5, 5, 5, 5) at (6,2,2), 22 at every tick in both modes; (f) the fill's 132 with 120 in rays and 12 quanta parked in ninths, (6,2,2) 1, (4,2,2) [4] x 6, (5,3,2) [1, 1]; (h) the shadow fresh from (3,2,2) into the mark at (4,2,2), returned at tick 1, waiting at (3,2,2) for its thing, home with it in the cycle of tick 2 and released again with it into the mark, which absorbs the thing at tick 3 and the shadow a round later, shadows [1, 1, 1, 1, 0] and the mark's resident shadow line 1; (i) the shadows fresh from (9,1,2) (off the edge at tick 1), (5,2,2) (into the body) and (3,3,2) (into the mark, which returns it to its thing at (3,3,2), where it is home and released again every other tick), the real lines the same, the shadow line initial 3, current 2, escaped 1, absorbed at home 0, shadows [2] x 6; (j) the shadows fresh from (3,y,2), the push at (2,y,2) in the cycle of tick 2, the momenta pushed from tick 2, each return waiting at (3,y,2) with steps 0; (k) the 11 sends 1 on to (5,2,2) and 4 back to (3,2,2), then (4,2,2) holds 1 on +X after tick 2 and (6,2,2) nothing.

`tests/test_bit_law.py` is the isolated test of `bit-law-v1`
([the law of the bit](SPATIAL_FIELDS.md#the-law-of-the-bit-bit-law-v1);
Highlights 5.4, the model owner's decision of 2026-09-18, with the amendments
of that day: a shadow is a ray of the same family as its thing with the bit 0,
shadows are given with the board, escapes are the only loss, a shadow has no
mass, no clock and no delay, a thing has a stable id stamped on its shadows,
the bit never changes at a meeting, the things' content is constant between
absorptions, events happen at Nodes that hold a thing, there is no lottery),
pinned here on 2026-09-18 before its first run, as Highlights 5.5 requires.

The board of every world: open 10 x 5 x 5, `link_ticks` 1, costs 1, one ray
family `m` (the six unit-axial headings, `metric: "links"`, pace 1/1, 8 ray
slots, charge -1, `release` [1, 1], no `spread` unless said) and the
three-component `momentum` field; a `lamp` type (thing 1) holds `m` 2 and
emits it once along +X in the cycle of tick 0, funded, recoiling into
`momentum`; a `ring` type (thing 2) holds `m` 4 and emits nothing; an
external body of `m` is thing 3 (one past the two types), or 4 for a second
body; the coupling `turn` is `{"participants": [m, m], "momentum_table":
{"m": 1}, "reads": "charge"}`, a thing of `m` pushed by the shadows of `m`
(repulsion), the push read times the shadow's sign and the thing's charge (a
shadow given with the board carries its owner's sign, -1 here, so the product
is 1 and the push is sign x amount x heading); a body's table declares the
same reading; a mark's `setting` is its counter table. Written before the first run, all of it
computed from the rules:

- (a) push and home to a body: the lamp at (1,2,2); a body at (7,2,2), amount
  100, sink, thing 3; the board gives one shadow of thing 3 at (5,2,2) on -X,
  amount 1 (`initial_field.m.rays`); `m` has `phase_bits` 2 and rest rate 1.
  The thing (amount 2, phase 0 at emission) is at (2,2,2) after tick 1 and at
  (3,2,2) after tick 2 with phase 2, two Links walked; the shadow is at
  (4,2,2) after tick 1 and at (3,2,2) after tick 2 with phase 0 (no clock) and
  steps 3. In the cycle of tick 2 (a cycle follows the delivery of its tick,
  so its records carry that tick) the table pushes the thing by 1 x 1 x
  (-1, 0, 0): no event (a push is not an event, point 15), the register line
  of the record reading thing 1 at (2, 0, 0) after tick 2 and (1, 0, 0) after
  tick 3; the shadow turns back on its steps, heading +X, carrying
  (1, 0, 0), no event of its own, and the thing's bit is 1 after the push
  (read from the inventory at (5,2,2) after tick 4: detector 1, owner 1,
  momentum (1, 0, 0)). The thing reaches the body after tick 6 and ends in
  its sink (`external_body_absorbed` amount 2, absorbed `m` 2, momentum
  (1, 0, 0)); the shadow walks (4,2,2), (5,2,2), (6,2,2) with steps 2, 1, 0,
  follows no trace (none of thing 3 is written) and walks on straight into the
  body after tick 6: home, no event of its own (a homecoming crosses no
  border, point 7: nothing sourced, nothing returned on the amount lines), the
  reception record at
  (7,2,2) reading `returned_to_body` m amount 1, momentum (1, 0, 0), and the
  body's momentum is (1, 0, 0), the thing's dp reversed (the register line:
  thing 1 (1, 0, 0) and thing 3 (0, 0, 0) after tick 5, thing 3 (1, 0, 0)
  alone after tick 6, thing 1 being absorbed); it leaves again on -X, a fresh shadow at (7,2,2)
  after tick 6 and at (6,2,2) after tick 7. The ledger after tick 6: `m`
  initial 3, sourced 0, current 1, absorbed 2, returned 0; `things.m` initial
  2, sourced 0, current 0, absorbed 2; `shadows.m` initial 1, sourced 0,
  current 1, returned 0; `momentum` initial 0, sourced 0, current (-2, 0, 0)
  (the lamp's recoil), absorbed (1, 0, 0), returned (1, 0, 0); the charge
  line of `m` initial -2, sourced 0, current 0, absorbed -2; every line
  balances at every tick and `things_conserved` holds. The trace at (3,2,2)
  after the run is [[1, 0]] (thing 1 left through Port 0); `things_content`
  per completed tick reads 2, 2, 2, 2, 2, 0.
- (b) two bodies, each other's shadows: A at (2,2,2) (`thing` 3, declared)
  and B at (7,2,2) (`thing` 4), amount 100, `momentum_table` {"m": 1}; the
  board gives A's shadow at (3,2,2) on +X and B's at (6,2,2) on -X, amount 1
  each. After tick 4 A's shadow reaches B and B's reaches A: each pushes, no
  event (the reception records at A and B read `returned_to_body` momentum
  (-1, 0, 0) and (1, 0, 0)), A's momentum (-1, 0, 0), B's (1, 0, 0), each
  shadow turned back with the opposite. After tick 9 each is home (steps 5
  walked back), again no event, the reception records reading the same
  momenta once more, A's momentum (-2, 0, 0), B's (2, 0, 0) (the register
  line: thing 3 (-1, 0, 0) and thing 4 (1, 0, 0) after ticks 4 to 8, (-2, 0,
  0) and (2, 0, 0) after tick 9); the bodies' momentum sums to zero and the
  `momentum` line balances at every tick with `returned` reading zero in
  total; `shadow_counts` reads {3: [1, 1], 4: [1, 1]} after every tick (a
  thing keeps its shadow set), `things_content` 0 and `shadows_content` 2
  after every tick; no `spatial_received`, `spatial_cycle` or `spatial_sent`
  is recorded at any Node but A and B in ten ticks (a Node holding shadows
  alone makes no event); `shadows.m` after tick 9: initial 2, sourced 0,
  current 2, returned 0 (a homecoming crosses no border, point 7).
- (c) a thing meets its own shadow: the lamp at (1,2,2) and one shadow of
  thing 1 at (5,2,2) on -X. They meet at (3,2,2) after tick 2; in the cycle
  of tick 2 the table gives no push (the shadow is its own) and the shadow is
  home to the thing ray: no event, the cycle record at (3,2,2), tick 2,
  reading `returned` m amount 1, momentum (0, 0, 0), and the register line
  thing 1 (2, 0, 0) after every tick; the fresh shadow leaves
  with the thing on its line and is home again only when it meets the thing
  from another heading (walking with it is not a meeting), both at (6,2,2)
  after tick 5, the thing with detector 1 and no register; `m` returned 0 and
  sourced 0 after tick 3 (point 7); `things_content` 2 and `shadows_content` 1 after
  every tick. The same world on a periodic board (closed, no mark) for twelve
  ticks: the thing loops and both contents are constant, 2 and 1, every line
  balancing.
- (d) the mark: the lamp at (1,2,2), a second lamp `lamp2` (thing 2, `m` 1)
  at (0,2,2), a mark at (4,2,2) with setting [1, 2], and a shadow of thing 5
  at (5,2,2) on -X. After tick 1 the shadow reaches the mark and is returned:
  no event (a mark returning a shadow is none, point 13), no click, the
  mark's counter empty, the shadow at (5,2,2) after tick 2 on +X, outbound 0,
  steps 1; it walks back through (6,2,2) and on. After tick 3 the first thing
  (amount 2) reaches the mark, the 0-th arrival: 0 mod 2 < 1, caught, a
  `detector_click` with `absorbed` 2, owner 1, the counter `m` 2, the marks'
  momentum (2, 0, 0), the mark's `things` [1]. After tick 4 the second thing
  (amount 1) reaches it, the 1st arrival: 1 mod 2 = 1, returned, a
  `detector_return` with owner 2, no click, the thing walking back and at
  (2,2,2) after tick 6 with steps 2. After tick 6 `things.m` reads initial 3,
  current 1, absorbed_by_marks 2; the `momentum` line current (-2, 0, 0),
  absorbed_by_marks (2, 0, 0); `things_content` per tick 3, 3, 1, 1, 1, 1 and
  `shadows_content` 1 at every tick. The same world with the marks' `seed` 7
  runs byte-identically (the seed is read by nothing), and the runner records
  both contents per tick.
- (e) a shadow-only board: no seed, no mark, no body; `m` spreads by
  [6, 1, 1, 1, 1, 1]; the board gives two shadows of thing 2 (the ring's id;
  nothing of it is seeded), 11 at (4,2,2) on +X and 11 at (5,2,2) on -X.
  Four ticks, once with `dense_field` false and once on the default (dense,
  admitted): no event kind but `cycle_started` and `cycle_committed` is
  recorded (none at all here, no carrier holding a record); `things_content`
  0 and `shadows_content` 22 after every tick; the ledger's `m` current is 22
  after every tick with nothing escaped. Each shadow is content that arrived
  and spreads at its own Node in the cycle of tick 0: after tick 1 (5,2,2)
  holds 6 on +X (the forward share of 11 x 6 / 11) and (6,2,2) holds 1 on +X
  (the backward share of the shadow on -X); after tick 2 (6,2,2) holds one
  shadow of amount 3 on +X (6 x 6 / 11, the rest in the registers) and
  (3,2,2) one of 3 on -X; the two modes agree on every ledger line and on
  every Node's rays and registers.
- (f) the fill: a body of `m` at (4,2,2), amount 11 (11 per heading, the
  release 1 / 1), thing 2, `m` spreading by [6, 1, 1, 1, 1, 1],
  `initial_field.m.fill` 2. The board starts with 132 quanta of shadows
  (thing 2), nothing of a thing: each of the six neighbours holds 11 arriving
  from the body, each axial Node two Links out holds 6, each of the twelve
  Nodes one Link out on two axes holds two quanta on two headings, and the
  body's Node holds six fresh shadows of 1, one per heading, what arrived
  there in the last interval and leaves again; `initial.m` reads 132 and
  `shadows.m` initial 132; three ticks in both modes agree on every ledger
  line and every Node. Nothing of the fill is dropped (the model owner,
  2026-09-18): what reaches a source or a mark during the fill leaves again
  the way it came, and the field is whole quanta per Node and heading with
  the fractional parts in the remainder registers.
- (h) the mark as the home of what it absorbed (the model owner, 2026-09-18):
  the lamp at (1,2,2), a mark M at (4,2,2) with setting [1, 1], a second mark
  N at (8,2,2) with setting [1, 1], and a shadow of thing 1 at (7,2,2) on +X.
  After tick 1 the shadow reaches N and is returned without an event, at
  (7,2,2) after tick 2 on -X with steps 1; after tick 3 the thing reaches M
  and is caught (counter `m` 2, momentum (2, 0, 0), M's `things` [1], the
  trace at M [[1, 6]]: the thing ended there). The returned shadow is at
  (6,2,2) after tick 3 with its steps spent, follows no trace there and walks
  on straight, (5,2,2) after tick 4, and reaches M after tick 5: a returning
  shadow of a thing M absorbed, home to M: a `shadow_absorbed` at M, tick 5,
  amount 1, owner 1, momentum (0, 0, 0) (an absorption at a mark is recorded,
  the mark being the thing's border); M's counter `m` 3, momentum (2, 0, 0).
  After tick 5 `fields.m` absorbed_by_marks 3, `things.m` absorbed_by_marks 2
  with current 0, `shadows.m` absorbed_by_marks 1 with current 0, and every
  line balances (the charge line reads the things' share of the marks' line: a
  shadow carries no charge); `things_content` per tick 2, 2, 0, 0, 0 and
  `shadows_content` 1, 1, 1, 1, 0: each constant but for what the marks
  absorbed.
- (i) the ledger per bit with the border lines (the model owner, 2026-09-18):
  the marked and external elements and the board's edge are the border
  between the board and the outside, and per family and per bit initial +
  sourced = current + absorbed_by_bodies + absorbed_by_marks + escaped +
  returned holds exactly at every tick. Two lamps, `lamp_a` (thing 1) at
  (1,2,2) and `lamp_b` (thing 2) at (1,3,2), each a source of one quantum per
  interval along +X (unfunded, booked as sourced, no recoil); a body at
  (4,2,2), thing 3, the sink, on lamp_a's line (a body absorbs things and
  returns shadows); a mark M at (4,3,2) with setting [1, 1] on lamp_b's line
  and a mark N at (8,3,2); the board gives a shadow of thing 3 at (6,1,2) on
  +X (it walks off the +X edge after tick 4), one of thing 3 at (6,2,2) on -X
  (home at the body after tick 2, released again on +X) and one of thing 2 at
  (7,3,2) on +X (returned by N after tick 1, back through (7,3,2), (6,3,2),
  (5,3,2), and absorbed by M after tick 5 as the home of thing 2, which M
  caught after tick 3). Six ticks. Things: twelve quanta sourced, the k-th of
  each lamp at its border after tick k + 3, so four in the body's sink and
  four in M's counter, four still on the board; shadows: three given, one
  home and released again (no line, point 7), one escaped, one absorbed by
  M, one on the board.
  After tick 6 `things.m` reads initial 0, sourced 12, current 4, absorbed 4,
  absorbed_by_marks 4, escaped 0, returned 0; `shadows.m` initial 3, sourced
  0, current 1, escaped 1, absorbed_by_marks 1, returned 0; `fields.m`
  initial 3, sourced 12, current 5, absorbed 4, absorbed_by_marks 5, escaped
  1, returned 0; `things_content` per tick 2, 4, 4, 4, 4, 4 and
  `shadows_content` 3, 3, 3, 2, 1, 1; M's counter `m` 5 with `things` [2],
  the body's sink `m` 4.
- (j) what the thing multiplies the shadow's message by (point 16): two lamps,
  `lamp` (thing 1, `m` 2) at (1,1,2) and `lamp2` (thing 2, `m` 4) at (1,3,2),
  a body at (9,2,2) (thing 3) and two shadows of thing 3, sign -1, at (5,1,2)
  and (5,3,2) on -X; the coupling `turn` with `momentum_table` {"m": -1}
  (attraction) and `reads` "content" or "charge". Each thing meets its shadow
  at (3,y,2) after tick 2; the register line after tick 3 reads, under
  "content", thing 1 (4, 0, 0) and thing 2 (8, 0, 0) (the push -1 x 1 x
  content x (-1, 0, 0): (2, 0, 0) and (4, 0, 0), the same acceleration), under
  "charge" thing 1 (3, 0, 0) and thing 2 (5, 0, 0) (the push -1 x 1 x (-1 x
  -1) x (-1, 0, 0) = (1, 0, 0) each, the same push); after tick 3 each
  returning shadow at (4,y,2) carries -push with steps 2 and each thing its
  register with steps 3; `things_content` 6 and `shadows_content` 2 after
  every tick, every line balanced. A table without `reads`, a `reads` that is
  neither word, and a body's table without `reads` are rejected naming point
  16.
- (k) a thing moves whole while its shadows spread: the lamp (thing 1, `m` 2)
  at (1,1,2), `m` spreading by [6, 1, 1, 1, 1, 1], and one shadow of thing 1,
  amount 11, at (4,2,2) on +X, no coupling. The thing is one ray of 2 at
  (1 + t, 1, 2) after tick t, never split, bit 1, owner 1; the shadow, content
  that arrived at (4,2,2), spreads there in the cycle of tick 0: after tick 1
  (5,2,2) holds 6 on +X and (3,2,2) 1 on -X, bit 0, owner 1, and after tick 2
  (6,2,2) holds 3 on +X; `things_content` 2 and `shadows_content`
  11 after every tick, `shadows.m` sourced 0 (nothing is created from a
  shadow), every line balanced; every event but the cycle's own is at a Node
  on the thing's line y = 1, z = 2 (a Node holding shadows alone publishes
  nothing).
- (g) the retired declarations: `field_of` on a spatial field, `on_bit_1` on
  a mark, `bit` on a ray interaction and `field` on a body are rejected with
  the words "bit-law-v1"; two types with one `thing` id are rejected; a
  spatial field lists its owners after parsing, [1, 2, 3] in world (a).

## The Node mixes the six

Re-pinned on 2026-09-18 under `return-field-v1` (feature 16d; `tests/test_node_mixing.py` (g), `tests/test_dense_field.py` (a)): `spread_content` takes and returns the parked block of thirty-six slots per owner (the outgoing eighteen, then the returning eighteen) with its momenta, five results; the region's block stays the outgoing eighteen (`engine_block`, `region_block`).

`tests/test_node_mixing.py` is the isolated test of `node-mixing-v1`
([the Node mixes the six](SPATIAL_FIELDS.md#the-node-mixes-the-six-node-mixing-v1);
Highlights 5.4 point 24, the model owner's decision of 2026-09-18; feature
16c), pinned here on 2026-09-18 before its first run, as Highlights 5.5
requires.

The board of every world: open 11 x 5 x 5, `link_ticks` 1, costs 1, one ray
family `m` (the six unit-axial headings, `metric: "links"`, pace 1/1, 8 ray
slots, charge -1, `release` [1, 1], `phase_bits` 3, so N = 8 and a half turn
is four steps; nothing else declared of the spread) and one never-seeded
holder type (thing 1; a second, thing 2, in world (d)); the shadows are given
with the board (`initial_field.m.rays`) at (5,2,2), content that arrived and
mixes there in the cycle of tick 0. The rule: at a Node the shadows of one
group (owner, sign, polarization) that arrived on each heading are one
amplitude, sqrt(amount) at the step nearest their coherent sum; the leaving
amplitude of a heading is a third of the sum of the six less the arrival
that came in through that Port (the one walking the opposite heading), sent
back; the total in ninths is shared among the six headings in proportion to
the squared leaving amplitudes by the largest-remainder rule (ties to the
lower Port), the whole quanta leave at the phase of their leaving amplitude
and the ninths below one quantum are parked in the Node's register of that
heading (released whole when a register reaches nine, as
`field-remainder-v1` does). Registers are read per Node in Port order
[+X, -X, +Y, -Y, +Z, -Z] with their phases. Written before the first run,
all of it computed from the rule:

- (a) a lone arrival: 9 on +X at phase 0. Its leaving amplitude back through
  the Port it came in by (-X) is -2/3 of its own, the five others +1/3: the
  weights 4 : 1 : 1 : 1 : 1 : 1 of 81 ninths give 4 back and 1 on each other
  heading, exactly, the back share at phase 4 (the minus), the rest at 0.
  After tick 1 (4,2,2) holds 4 on -X at phase 4, (6,2,2) 1 on +X, (5,3,2) 1
  on +Y, (5,1,2) 1 on -Y, (5,2,3) 1 on +Z and (5,2,1) 1 on -Z, at phase 0,
  six Nodes, no register, `shadows_content` 9. In the cycle of tick 1 the 4
  (36 ninths, 16 back and 4 on each other heading) sends 1 back on +X at
  phase 0 (4 + 4) and parks (7, 4, 4, 4, 4, 4) at phases (0, 4, 4, 4, 4, 4);
  each lone 1 parks whole, 4 ninths on its back heading and 1 on each other:
  after tick 2 the one ray on the board is 1 on +X at phase 0 at (5,2,2);
  the registers read (7, 4, 4, 4, 4, 4) at (4,2,2), (1, 4, 1, 1, 1, 1) at
  phases (0, 4, 0, 0, 0, 0) at (6,2,2), (1, 1, 1, 4, 1, 1) at (5,3,2) with
  the 4 at phase 4, (1, 1, 4, 1, 1, 1) at (5,1,2), (1, 1, 1, 1, 1, 4) at
  (5,2,3) and (1, 1, 1, 1, 4, 1) at (5,2,1); content 9 (1 in the ray, 8 in
  the registers). After tick 3 no ray is on the board and (5,2,2) parks
  (1, 4, 1, 1, 1, 1) at phases (0, 4, 0, 0, 0, 0), seven blocks in all,
  content 9, every ledger line balanced, no event beyond the cycle's own.
- (b) two equal arrivals head on in phase: 9 on +X and 9 on -X, phase 0.
  The sum is 2 amplitudes; each axis heading gets 2/3 - 1 = -1/3 of one,
  each transverse heading 2/3: weights 1 : 1 : 4 : 4 : 4 : 4 of 162 ninths,
  a/9 = 1 on each axis heading at phase 4 and 4a/9 = 4 on each transverse
  heading at phase 0. After tick 1 (6,2,2) holds 1 on +X and (4,2,2) 1 on
  -X, phase 4, and (5,3,2), (5,1,2), (5,2,3), (5,2,1) hold 4 on +Y, -Y, +Z,
  -Z at phase 0; content 18, no register. In the cycle of tick 1 each 4
  sends 1 back at phase 4 and parks 7 on its back heading and 4 on the
  others, each 1 parks whole: after tick 2 (5,2,2) holds four rays of 1 on
  +Y, -Y, +Z and -Z at phase 4 and nothing else is on the board; the
  registers read (1, 4, 1, 1, 1, 1) at phases (4, 0, 4, 4, 4, 4) at (6,2,2),
  (4, 1, 1, 1, 1, 1) at phases (0, 4, 4, 4, 4, 4) at (4,2,2), (4, 4, 4, 7,
  4, 4) at (5,3,2) with the 7 at phase 4, (4, 4, 7, 4, 4, 4) at (5,1,2),
  (4, 4, 4, 4, 4, 7) at (5,2,3), (4, 4, 4, 4, 7, 4) at (5,2,1); content 18.
  In the cycle of tick 2 the four 1s in phase mix at (5,2,2): the sum is 4
  amplitudes, the four headings they came in by get 4/3 - 1 = 1/3, the two
  axis headings 4/3: weights 16 : 16 : 1 : 1 : 1 : 1 of 36 ninths, 1 on +X
  and 1 on -X at phase 4 and (7, 7, 1, 1, 1, 1) parked at phase 4. After
  tick 3 (6,2,2) holds 1 on +X and (4,2,2) 1 on -X at phase 4, the seven
  blocks hold 16 quanta, content 18.
- (c) two equal arrivals head on in antiphase: 9 on +X at phase 0 and 9 on
  -X at phase 4. The sum cancels; each is sent back whole through the Port
  it came in by, its phase turned by a half turn, nothing transverse: after
  tick 1 (6,2,2) holds 9 on +X at phase 0 and (4,2,2) 9 on -X at phase 4,
  nothing else, content 18. Each is lone in the cycle of tick 1 and mixes as
  (a): after tick 2 (5,2,2) holds 4 on -X at phase 4 and 4 on +X at phase 0,
  (7,2,2) 1 on +X at phase 0, (3,2,2) 1 on -X at phase 4, the four
  transverse Nodes of (6,2,2) 1 each at phase 0 and those of (4,2,2) 1 each
  at phase 4, eleven Nodes, no register. The pair at (5,2,2) is in
  antiphase again and is sent back whole in the cycle of tick 2, the ten 1s
  park: after tick 3 (6,2,2) holds 4 on +X at phase 0 and (4,2,2) 4 on -X
  at phase 4, the only rays, ten blocks of one quantum, content 18.
- (d) two owners at one Node do not mix: 9 on +X of thing 1 and 9 on -X of
  thing 2, both phase 0. Each is lone and mixes as (a): after tick 1 (6,2,2)
  holds 1 on +X of thing 1 at phase 0 and 4 on +X of thing 2 at phase 4,
  (4,2,2) 4 on -X of thing 1 at phase 4 and 1 on -X of thing 2 at phase 0,
  and each transverse Node 1 of thing 1 and 1 of thing 2 at phase 0, two
  rays; content 18, no register; the same amounts of one owner give (b).
- (e) two shadows of one owner on one heading are one amplitude: 9 on +X at
  phase 0 and 9 on +X at phase 2 (two rays, their phases differ). Their
  amount 18 at the phase of their sum, 1, mixes as a lone arrival: 8 back
  on -X at phase 5 and 2 on each other heading at phase 1 (162 ninths, 72
  back and 18 each), content 18, no register.
- (f) unequal amounts and phases, the integers of the rule: 24 on +X at
  phase 0 and 8 on -X at phase 2. The amplitudes are the integer square
  roots of 24 x 1024 and 8 x 1024, 156 and 90, times the cosine and sine at
  256: (39936, 0) and (0, 23040), sum (39936, 23040). Three times the
  leaving amplitude of +X (the -X walker came in through it) is (39936,
  -46080), of -X (-79872, 23040), of each transverse heading the sum; their
  squared lengths 3718250496, 6910377984 and 2125725696 total 19131531264
  (35 bits), reduced by 7 bits to 29048832, 53987328 and 16607232 (total
  149465088); the 288 ninths give 55, 104 and 32 x 4 with a remainder of 1
  to the largest fraction, +X: 56, 104, 32, 32, 32, 32, so 6 on +X at phase
  7, 11 on -X at phase 4, 3 on each transverse heading at phase 1, and
  (2, 5, 5, 5, 5, 5) parked at phases (7, 4, 1, 1, 1, 1): 29 in rays, 3 in
  the registers, content 32.
- (g) the registers (`field-remainder-v1` under the mixing, through
  `spread_content`): lone quanta of 1 on +X at phase 0 arriving one per
  cycle at one Node park 4 ninths on -X and 1 on each other heading per
  arrival; the -X register releases one quantum at the third, fifth,
  seventh and ninth arrival (12, 11, 10 and 9 ninths, left at 3, 2, 1 and
  0) and the five others one each at the ninth, so after nine arrivals nine
  quanta have left, 4 back at phase 4 and 1 on each other heading at phase
  0, and the block is empty; after two arrivals the block reads (2, 8, 2,
  2, 2, 2). Two lone shadows of 3 of opposite sign on +X are two groups: 1
  back each on -X at phase 4, a ray per sign, and (3, 3, 3, 3, 3, 3) in each
  sign's block, `signs` (-1, 1), `stored` 4.
- (h) nothing declared: a `spread` key and a `steering` key on a family are
  refused naming point 24 ("the Node mixes the six"); a `table` on a split by
  the phase difference is refused as before (point 17, the split of two
  things of section 5.2 stands) and such a split carries the family's table
  [8, 7, 4, 1, 0, 1, 4, 7], which `steering_table(8)` still writes. The
  runner records `node_mixing` "node-mixing-v1" and `mixing_fields`
  `[{"field": "m", "phase_width": 8}]`, `shadow_families` carries
  `phase_width` 8 and no table, no `phase_spread` and no `field_spreading`
  key is written, and world (a) for two ticks writes no event beyond the
  cycle's own.
- (i) the dense layer: worlds (a) to (f) for four ticks under the engine
  alone and under the dense mode (the default, admitted) give the same board,
  ledger, content and registers at every tick.

## The phase-steered spread (deleted on 2026-09-18)

`tests/test_phase_spread.py` was deleted on 2026-09-18 with `phase-spread-v1`
by feature 16c, `node-mixing-v1` (Highlights 5.4, point 24): a shadow does
not choose its next heading alone and not in a pair, the six Ports mix, so
the pairwise steering of point 17 and the split table of a lone share are
retired for shadows and no case of that module states the rule. The steering
table stays the Born split of two things that meet (section 5.2), pinned in
`tests/test_ray_meeting_conversion.py` and `tests/test_loop_binding.py`.

## A Node is its six Ports

Re-pinned on 2026-09-18 under `return-field-v1` (feature 16d; `tests/test_node_is_ports.py`): the trace is retired, so (b) M8 is deleted, (d) M13 lists no parked shadow after one tick, (c) M9's shadow is returned by the mark as it is (outbound 1, fresh) and home at P0 every second tick as before, and (g)'s shadow, returned by the mirror without a push, mixes at (5,2,2) in the cycle of tick 3 and parks 4 on +X and 1 on each other heading.

Re-pinned on 2026-09-18 under `node-mixing-v1` (Highlights 5.4 point 24, feature 16c; `tests/test_node_is_ports.py`): no split table is declared, the parked unit is ninths, and a lone shadow mixes at every Node it reaches with nothing else there, so (a) reads the mixing (5 on +X at (4,2,2): 2 leave back on -X, 5 ninths park on +X and on each transverse heading and 2 on -X, 27 in all; the 2 park whole at (3,2,2), 8 on +X and 2 on each other heading), the shadows of (b), (c), (d) and (g) leave fresh from the Node beside the mark or the body they are to reach (M2 at (1,1,1) and the shadow from the seed Node (2,1,1), its step spent there where the trace is, home at M after tick 5; the ring's mark at (4,5,5) and the shadow from P0, home every second tick; the mirror's shadow from (5,2,2), waiting there from tick 2), and the M8 record's trace carries `unit` 9.

`tests/test_node_is_ports.py` is the isolated test of `node-is-ports-v1`
([a Node is its six Ports](SPATIAL_FIELDS.md#a-node-is-its-six-ports-node-is-ports-v1);
Highlights 5.4 point 22 and the five settled rules, the model owner's
decision of 2026-09-18), pinned here on 2026-09-18 before its first run, as
Highlights 5.5 requires. The boards follow those of the law of the bit (open,
`link_ticks` 1, costs 1, the six Port headings, `metric: "links"`, pace 1/1,
8 ray slots, family `m` with charge -1 and `release` [1, 1]); a lamp is a
thing that spends its content, a type holding its content and the momentum
field with an emission rule (no `source`, no `recoil_field`); a profile shadow
without `steps` starts its Link distance from its owner's Node away. Written
before the first run, all of it computed from the rules:

- (a) the parked shadow: a shadow of owner 2 (no Node), amount 5, at (4,2,2)
  on +X with `steps` 1, the table [6, 1, 1, 1, 1, 1]; in the cycle of tick 0
  the 5 on +X splits 30/11 forward and 5/11 on each other heading: 2 leave
  forward and 8 (+X), 5, 5, 5, 5, 5 park, 33 elevenths, three quanta; after
  tick 1 (5,2,2) holds 2 on +X (steps 1) and after tick 2 (6,2,2) holds 1,
  (5,2,2) parking 1, 2, 2, 2, 2, 2; the parked rays are bit 0, `parked` 1,
  steps 0, outbound 1, of owner 2, each below 11; `shadow_content` 5 at
  every tick, `fields.m` current 5 and sourced 0, the shadow line initial 5,
  current 5, escaped 0, absorbed_at_home 0; no event; the snapshot's `parked`
  entries at (4,2,2) carry unit 11, bit 0, owner 2, sign -1, family m; the
  engine and the dense layer agree on the ledgers, the rays, the parked
  shadows and the snapshot.
- (b) M8, the trace and the mark as home: 7x3x3, a lamp `e` of content 4 at
  (2,1,1) heading +X (no momentum field), marks M (5,1,1) and M2 (0,1,1) with
  the table [1, 1], a shadow of e, amount 1, at (1,1,1) on -X (steps 1, its
  distance from (2,1,1)). The thing leaves a zero-amount parked shadow on +X
  at (2,1,1) after tick 0, (3,1,1) after tick 1, (4,1,1) after tick 2, none at
  M; it is caught at M after tick 3 (one `detector_click`, absorbed 4, owner
  1). The shadow reaches M2 after tick 1 and is returned (steps 2, +X), is at
  (1,1,1) after tick 2 (steps 1) and at (2,1,1) after tick 3 with its steps
  spent, the lamp there holding nothing; it follows the traces, (3,1,1) after
  tick 4 and (4,1,1) after tick 5 with steps 0, and reaches M after tick 6:
  absorbed into the resident on its shadow line, no event, no click. The
  resident of M: real {m: 4}, shadow {m: 1}, momentum (4,0,0), owners [1]; M2
  empty. `real_content` 4, 4, 0, 0, 0, 0; `shadow_content` 1, 1, 1, 1, 1, 0;
  the real line initial 4, current 0 from tick 3, absorbed 4 from tick 3; the
  shadow line initial 1, current 0 from tick 6, absorbed_at_home 1 from tick
  6; `fields.m` absorbed_by_marks 4 from tick 3 and 5 from tick 6; the marks'
  lines after tick 6: count 2, momentum (4,0,0), real {m: 4}, shadow {m: 1}.
- (c) M9, a prefilled shadow of a loop: the E5 unit square ring of
  `test_loop_binding` (Port corner table, rate 2), a mark at (2,5,5) [1, 1]
  and a shadow of thing 1 (corner_0_r, at P0 = (5,5,5)), amount 1, at (3,5,5)
  on -X: its steps are 2, its Link distance from P0 on its line. Returned by
  the mark after tick 1 (steps 3, +X), at (3,5,5) after tick 2 (steps 2),
  (4,5,5) after tick 3 (steps 1), P0 after tick 4 with steps 0 as thing 1's
  ray is there: home, the cycle record at P0, tick 4, reading `returned`
  electron amount 1, momentum (0,0,0), and re-released reversed: at (4,5,5)
  after tick 5 (steps 1, -X) and (3,5,5) after tick 6. `electron` 9 in total,
  `real_content` 8 and `shadow_content` 1 at every tick, every corner holding
  two quanta of things from tick 2, the momentum line's `returned` (0,0,0)
  and `electron` sourced 0 at every tick; no `shadow_return`, `shadow_absorbed`
  or `ray_push`.
- (d) M13, the record: the M8 world through the runner for one tick.
  `state.json` lists one parked entry, the trace: position [2,1,1], family m,
  owner 1, sign 0, heading [1,0,0], amount 0, unit 1, phase 0, bit 0.
  `run.json` reads `node_is_ports` "node-is-ports-v1", `bit_law`, `momentum`
  [{"1": [4,0,0]}], each mark's `resident` (real {}, shadow {}, momentum
  [0,0,0], owners []), the shadow family m with release [1, 1] and owners [1],
  `real_content` [4] and `shadow_content` [1]; no key `registers`,
  `register_phases`, `counter`, `seed`, `traces` or `field_remainders`
  anywhere in either file.
- (e) M14, a seeded thing missed at a mark: 9x3x3, a lamp `e` of content 4 at
  (1,1,1) heading +X, a mark at (4,1,1) with the table [0, 1]. The thing is
  at (2,1,1) after tick 1 and (3,1,1) after tick 2 (steps 1, 2), returned at
  the mark after tick 3 (a `detector_return`, amount 4, owner 1; steps 3,
  -X), back at (3,1,1), (2,1,1), (1,1,1) after ticks 4, 5, 6 with steps 2, 1,
  0; at its seed Node the inverse split of a lone ray restores it to the lamp
  (an `inverse_split` at (1,1,1), tick 6, ports (), amount 4, restored true),
  no ray resident after tick 7, and the lamp emits it again on +X in the cycle
  of tick 7: at (2,1,1) after tick 8 and (3,1,1) after tick 9 (steps 1, 2,
  outbound, bit 1). No click; `real_content` 4 and `shadow_content` 0 at
  every tick; the real line initial 4, current 4 at every tick; the
  `momentum` line per tick {1: (4,0,0)} twice, {1: (-4,0,0)} four times, {}
  once, {1: (4,0,0)} twice; the momentum field's current (0,0,0) at every
  tick (the lamp's recoil and its ray's momentum together).
- (f) the source: a lamp of content 6 at (1,2,2) emitting 2 per interval on
  +X: rays of 2 (bit 1, owner 1) at (1 + k, 2, 2) for the k-th interval, the
  lamp's stock 4, 2, 0, 0 after ticks 1 to 4, `source_totals` zero,
  `fields.m` sourced 0, the real line initial 6, current 6 at every tick, the
  momentum field's current (0,0,0), the `momentum` line {1: (2k,0,0)} for k =
  1, 2, 3, 3; no `sourced` key on the per-bit lines; a lamp of content 0
  emits nothing.
- (g) the mirror: a second ray family `wall` (charge 0), a body of `wall`,
  amount 1, thing 3, at (6,2,2) under the table `mirror` (the arriving m
  leaves reversed, the token returned), the lamp of content 2 at (1,2,2), a
  shadow of owner 2 at (5,2,2) on +X with `steps` 1. The shadow reaches the
  body after tick 1 and is returned without a push (no momentum table):
  outbound 0, steps 2, -X, at (6,2,2) after tick 1, (5,2,2) after tick 2
  (steps 1), (4,2,2) after tick 3 with its steps spent and no trace of owner
  2: it waits there through tick 8. The thing reaches the body after tick 5,
  leaves reversed as a fresh event in that cycle, and is at (5,2,2) after tick
  6 and (4,2,2) after tick 7 (steps 1, 2; bit 1, owner 1, -X). No
  `external_body_absorbed`, `ray_push`, `shadow_absorbed` or `detector_click`;
  the body's sink empty; `real_content` 2 and `shadow_content` 1 at every
  tick, `fields.m` absorbed 0, the shadow line initial 1, current 1.

Re-pinned with feature 17 (`node-is-ports-v1`): in `tests/test_bit_law.py`
the lamp's emission declares no `source` or `recoil_field`, a profile shadow
starts its Link distance from its owner away (world (a): steps 4 at the push,
walking back 3, 2, 1 and home at the body with 0; (h): steps 6; (j): steps 6
after tick 3), the mark records read `resident` (real, shadow, momentum,
owners) and a shadow home to a mark makes no event ((h): the resident's real
{m: 2}, shadow {m: 1}), the per-tick `registers` line is `momentum`, the
ledgers per bit are `real` (initial, converted, current, escaped, absorbed)
and `shadow` (initial, current, escaped, absorbed_at_home) with the flag
`real_conserved` and the per-tick lines `real_content` and `shadow_content`,
world (i)'s lamps hold six quanta each (real initial 12, current 4, absorbed
8; `real_content` 12, 12, 10, 8, 6, 4), the trace is read from the snapshot's
`parked` list ((a): (3,2,2) holds a zero-amount shadow of thing 1 on +X) and
`seed` on a mark is rejected. In `tests/test_ray_momentum_turn.py` the recoil
shadow waits at (10,4,10) once its steps are spent and nothing of f escapes;
in `tests/test_plan_reuse.py` a Node holding a trace reuses its plan (13
evaluations, 20 hits); in `tests/test_kerengonen.py` the dissolving moving
particle recoils from its own emissions and walks back to -2.

## The return is a field

`tests/test_return_field.py` is the isolated test of `return-field-v1`
([the return is a field](SPATIAL_FIELDS.md#the-return-is-a-field-return-field-v1);
Highlights 5.4 point 3 as amended by the model owner on 2026-09-18, feature
16d), pinned here on 2026-09-18 before its first run, as Highlights 5.5
requires. The boards are those of the law of the bit (open, 10 x 5 x 5, costs
1, the six Port headings, family `m` with charge -1 and `release` [1, 1], no
`K`, `wait_per_quantum` 0); a body of `amount` quanta declares the whole charge
-amount, so a body with the table {"m": 1} reading charge is pushed by one
quantum of another body's shadow by one unit along the shadow's heading; the
mixing is node-mixing-v1 (a lone quantum leaves 4 back and 1 each other way
from 9; a lone 1 parks its ninths). Computed from the rules before the run:

- (a) A of 81 at (0,2,2) with its standing shell, 81 of its shadows at
  (1,2,2) heading +X with a Link walked; B of 1000 with the table at (2,2,2);
  `ray_slots` 32. Tick 1: the shell mixes, 36 back home to A (returned amount
  36, momentum (0, 0, 0)), 9 on to B, 9 each transverse way; B is pushed
  (9, 0, 0) and the 9 turns back with the opposite sign: fresh at B on -X,
  outbound 0, sign 1, carrying (-9, 0, 0). Tick 2: A re-releases the 36 on +X;
  the four transverse 9s mix and send 4 back each. Tick 3, at (1,2,2): the
  returning 9 is its own group, 4 back to B with (-4, 0, 0), 1 to A with
  (-1, 0, 0), 1 each transverse way with (-1, 0, 0); the outgoing group, 36
  from -X and 4 from each transverse Port (amplitudes 6, 2, 2, 2, 2, the mean
  4 2/3), sends 1 back to A and 21 on to B, the rest transverse. A receives 2
  with (-1, 0, 0); B is pushed (21, 0, 0) by the outgoing 21 and (-4, 0, 0) by
  the returning 4 (its heading and its sign both inverted: the opposite sign
  on the same heading), the 21 turning back with (-21, 0, 0), the 4 turning
  back once more as an outgoing share carrying nothing. The bodies' momenta
  per tick: B (9, 9, 26, 26, 19), A (0, 0, -1, -1, -3); A's third receipt at
  tick 5 is 6 with (-2, 0, 0). At every tick the bodies' momenta plus the
  momentum on the shadows, on their way and parked, sum to zero, the ledger is
  balanced and the things conserved; after tick 5 the returning ninths park
  with their momentum: (-1, 0, 0) at (1,1,2), (1,3,2), (1,2,1) and (1,2,3) on
  the share back toward (1,2,2) (the largest remainder), and (-1, 0, 0) on
  each of the returning +X and -X ninths at (1,2,2); the shadows total 81
  throughout.
- (b) A of 81 at (0,2,2); C of 1000 with the table at (1,2,2), B of 1000 with
  the table at (2,2,2); A's shadow of 81 fresh at (1,2,2) on +X. Tick 1: B is
  pushed (81, 0, 0), the share turns back (-X, outbound 0, sign 1,
  (-81, 0, 0)). Tick 2: at C the returning share pushes with the opposite
  sign, (81, 0, 0) where an outgoing share on -X would push (-81, 0, 0), and
  turns back once more: +X, outbound 1, sign -1, carrying (-162, 0, 0). Tick
  3: B pushed (81, 0, 0) again, the share back to -X with (-243, 0, 0). Tick
  4: C again. The momenta per tick: C (0, 81, 81, 162), B (81, 81, 162, 162);
  balanced every tick; the shadows total 81.
- (c) A of 729 at (1,2,2) with the table {"m": 1} itself, B of 1000 with the
  table at (2,2,2), A's shadow of 9 fresh at (1,2,2) on +X. Tick 1: B pushed
  (9, 0, 0), the share back with (-9, 0, 0). Tick 2: home at A, absorbed with
  no push (a push would read (9, 0, 0) here), A's momentum (-9, 0, 0), the
  receipt amount 9 momentum (-9, 0, 0); re-released on +X as an outgoing
  share of sign -1 carrying nothing. Ticks 3 and 4 repeat: A (0, -9, -9, -18),
  B (9, 9, 18, 18); balanced.
- (d) The world of (a): no parked shadow of amount zero, every share on its
  way has steps 0 or 1, `leave_trace`, `trace_of` and `MAX_TRACES` are gone
  from the state module, `run.json` records `return_field`
  "return-field-v1" and every `parked` entry of `state.json` carries a
  positive amount and its `momentum`.

## A click is an absorption

Re-pinned on 2026-09-18 under `clock-readings-v1`: the family declares `clock` at K 4 (one step per interval for the thing of 4); `detector_absorb` reads a thing's momentum as amount x heading plus the pushes it carries, (1, 2, -1) and (5, 2, -1) in the helper case.

Re-pinned on 2026-09-18 under `bit-law-v1`: the field family `G` and its release per tick went with the law; absorb is the default for every family, the thing of the lamp is caught by C at tick 4 with its momentum (or passed under `on_click: "pass"`), a click names the owner (`tests/test_detector_absorb.py`, three tests).

`tests/test_detector_absorb.py` is the isolated test of `detector-absorb-v1`
([a click is an absorption](SPATIAL_FIELDS.md#a-click-is-an-absorption-detector-absorb-v1),
[the click absorbs](DETECTOR_SAMPLING.md#the-click-absorbs-detector-absorb-v1);
Highlights 5.4, model owner, 2026-09-18; issue #169, feature 2c), pinned here
on 2026-09-18 before its first run, as Highlights 5.5 requires. The board,
under the shared Detector admission: periodic 15 x 15 x 15, `link_ticks` 1,
`metric: "links"`, pace 1/1, the six unit-axial headings; a lamp at (5,7,7)
holding 4 `quanta` (charge -2, rest rate 1 on an 8-step phase, 8 ray slots)
emits them once along +X in the cycle of tick 0, funded, recoiling into
`momentum`; `G` (rest rate 0, no charge, 16 slots) is the field of `quanta`
with `release` [1, 4] and no `spread`; four marks with setting 1/1 and seed 0:
A (6,8,7) with no coupling key, B (6,6,7) with `on_click: {"G": "pass"}`, C
(9,7,7) with `on_click: {"quanta": "absorb"}` (or no key in the second test),
E (6,7,6) with `on_click: "absorb"`; a `conservation` block reading energy as
quanta + G on the right side and momentum from the `momentum` field. Six ticks
through the Simulation API and through the runner. Written before the first
run, all of it computed from the rules:

- (a) the field: the quanta ray is at (6,7,7) after tick 1 and releases G
  floor(4 / 4) = 1 on the five headings other than its own (+X) in the cycle
  of tick 1, so G 1 arrives at (5,7,7), A, B, (6,7,8) and E at tick 2; the ray
  releases again from (7,7,7) in the cycle of tick 2 and from (8,7,7) in the
  cycle of tick 3, and at C, where it is absorbed at tick 4, it releases
  nothing, so G sourced reads 0, 5, 10, 15, 15, 15 after ticks 1 to 6;
- (b) the clicks of tick 2, in Node order: B draws 1 (seed 0 at 1/1) and passes
  the G quantum with the bit 1 (a `detector_click` through Port 2, the +Y face,
  family G, amount 1, bit 1, no `absorbed` entry; the ray at B after tick 2
  with heading 3, amount 1, outbound, bit 2); E draws 1 and absorbs it (the
  click through Port 4, the +Z face, with `absorbed` 1; E's counter (0, 1) by
  spatial-field index, quanta then G, its momentum (0, 0, -1), its Node holding
  no G ray); A draws 1 and absorbs it by the default of a field family (the
  click through Port 3, the -Y face, `absorbed` 1; counter (0, 1), momentum
  (0, 1, 0), no G ray at A, A's ticket 1 after the draw); the quantum at
  (5,7,7) and at (6,7,8) walks on unmarked;
- (c) the click of tick 4: C absorbs the matter ray under its declared
  coupling (the click through Port 1, the -X face, family quanta, amount 4,
  bit 1, `absorbed` 4; counter (4, 0), momentum (4, 0, 0)), and from tick 4 no
  quanta ray exists in the world; B's counter stays empty; five Detector
  events in all, no pass, no return, no inverse split;
- (d) the world ledger at every tick, every line balanced: G initial 0,
  sourced as in (a), current sourced minus 2 from tick 2, escaped, annulled
  and absorbed 0, `absorbed_by_marks` 2 from tick 2; quanta initial 4, current
  4 through tick 3 and 0 from tick 4, `absorbed_by_marks` 4 from tick 4;
  momentum initial (0, 0, 0), sourced (0, 0, 0), current (0, 0, 0) through
  tick 3 and (-4, 0, 0) from tick 4 (the lamp's recoil, its ray gone),
  `absorbed_by_marks` (4, 0, 0) from tick 4; the charge line quanta initial -8,
  current -8 then 0, `absorbed_by_marks` -8 from tick 4; the marks' lines:
  count 4, momentum (0, 1, -1) from tick 2 and (4, 1, -1) from tick 4, the
  counter per field equal to the `absorbed_by_marks` line; `detector_mark_totals`
  and `detector_mark_momentum` the same; the spatial accounting's
  `absorbed_by_marks` G 2 and quanta 4; `detector_marks` after the run: A
  momentum [0, 1, 0] counter {G: 1}, B [0, 0, 0] {}, C [4, 0, 0] {quanta: 4},
  E [0, 0, -1] {G: 1};
- (e) the local audit passes at every tick and reports `absorbed_by_marks`
  energy 6 (4 quanta and 2 G through the declared expression), momentum
  (4, 1, -1), charge -8, with initial + sourced = current + escaped + annulled
  + absorbed_by_marks for energy and charge;
- (f) the runner: `detector_absorb: "detector-absorb-v1"`, `detector_marks`
  as in (d), `detector_mark_totals` {quanta: [4], G: [2], momentum:
  [4, 0, 0]}, `detector_mark_momentum` [4, 1, -1],
  `conserved_at_every_completed_tick` and
  `accounting_balanced_at_every_completed_tick` true, the local audit passed
  with its line, `final_totals` quanta 0, G 13, momentum (-4, 0, 0); the
  `spatial_received` records of A and E at tick 2 and of C at tick 4 carry
  `absorbed_by_mark` (per family the amount and its momentum: G 1 with
  (0, 1, 0) at A, G 1 with (0, 0, -1) at E, quanta 4 with (4, 0, 0) at C) and
  no other reception record carries the key; the Detector events of
  `events.jsonl` are those of (b) and (c); a second run replays byte for byte;
- (g) with C on the defaults (no `on_click`), the matter ray passes C at tick
  4 with the bit 1 and the click without `absorbed`, C's counter empty and its
  momentum zero after tick 4, the one quanta ray in the world realized
  (amount 4, bit 2, outbound), the momentum line's current (0, 0, 0) and the
  marks' momentum (0, 1, -1); the reading stops at tick 4, since the field
  the ray releases beyond C reaches C at tick 6 and is absorbed there;
- (h) a world whose three marks A, B and E all declare `on_click: "pass"`, run
  through the runner: three clicks, none carrying `absorbed`, no reception
  record carrying `absorbed_by_mark`, `detector_mark_totals` zero,
  `detector_mark_momentum` (0, 0, 0), every counter empty, the G line's
  `absorbed_by_marks` 0 at every tick, the ledger's identity and the local
  audit exact;
- (i) rejected before a world exists, and by the configuration preflight:
  `on_click` "maybe" or 5 (must be absorb, pass or a mapping), {"G": "draw"}
  (on_click.G must be absorb or pass), {"photon": "absorb"} and {"momentum":
  "absorb"} (an unknown ray family); `DetectorMark` with an `on_click` entry
  outside pass, absorb and default, or a negative counter; `DetectorMark(A, 1,
  1, 0)` equals the record with every field at its default; `click_coupling`
  reads pass for quanta and absorb for G on a plain mark (`field_family` false
  and true) and the declared value on a declared one; `detector_absorb` sizes
  the counter on the first take (one entry per spatial field) and adds amount
  x heading, or the register where a push set one, exactly: rays of 3 on +Y
  and of 1 with the register (1, -1, 0) give counter (0, 4) and momentum
  (1, 2, 0), then quanta 4 on +X gives (4, 4) and (5, 2, 0), the mark's
  position, seed and `on_click` untouched.

The first run of the test on 2026-09-18 agreed with every integer above; the
board first held a fifth mark D (6,7,8) with setting 0/1 to show the return
untouched, removed before the first passing run because a returned field
quantum in a world without `spread` reaches the inverse split of feature 4
with no event (the return of a field quantum is the spreading test's case
`returned`); the return of a matter ray is the return test's.

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
- (l) the GIF palette (model owner, 2026-09-18, "the GIF has no colours":
  the phone GIFs came out white and grey): `quantize` builds one palette
  for the frames by maximum coverage, not by population. Pinned before the
  change on a synthetic frame, 200 by 120 pixels of a dark blue gradient
  (the scene with its vignette and grey lattice lines, 93 shades) with
  twelve dots of four by five pixels in yellow (255, 196, 0), cyan
  (34, 211, 255) and red (255, 59, 59), 240 saturated pixels, 1 percent of
  the frame (a saturated pixel is one whose channels differ by more than
  60): with 64 colours the median cut of the old palette left 160 of the
  240, one colour's dots quantized to the greys of the gradient (on the
  real frames, 1.5 percent saturated over 160000 pixels, it left none); the
  new palette keeps every dot's colour within 24 per channel and the count
  of saturated pixels within 5 percent of the frame's own, and holds the
  background too (no background pixel moves by more than 24 per channel);
  three frames with the dots at different places share the one palette;
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

Re-pinned on 2026-09-18 under `clock-readings-v1`: no rate, no clock; the inputs meet at phase 0 and delta, so the four outputs read 0, 0, 3 and 7 and the table cases 0, 4, (0, 2) and (0, 1); a product's phase stays as it walks.

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

Retired on 2026-09-18 under the law of the bit (`bit-law-v1`): `tests/test_released_field.py` pinned behaviour the law removed and is deleted; the run is repeated under the law in a follow-up (the worlds stay in `examples/`).

## External body

Re-pinned on 2026-09-18 under `bit-law-v1`: a body radiates nothing (its shadows are given with the board), so the `sink` world has no field, the electron ends in the sink and the body stays at rest, the light passes untouched; the `stars` case went with the law (`tests/test_bit_law.py` (b) holds its physics); a body's record names no `field`; a momentum table needs `reads` (`tests/test_external_body.py`).

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

## Field spreading (deleted on 2026-09-18)

`tests/test_field_spreading.py` was deleted on 2026-09-18 with
`field-spreading-v1` by feature 16c, `node-mixing-v1` (Highlights 5.4, point
24): the declared split table is retired, a shadow spreads by the Node's
mixing and nothing of the spread is declared, so every case of the module
(`single`, `superposition`, `cancelled`, `stream`, `sign`, `rejected`) stated
a retired rule. Its surviving subjects, the Node-owned remainder
(`field-remainder-v1`, now in ninths), the sign kept through the spread and
the refusal of a declared table, are pinned in
[The Node mixes the six](#the-node-mixes-the-six), (g) and (h). The pins
below stay for the record of what the table was.

Re-pinned on 2026-09-18 under `phase-spread-v1` (Highlights 5.4 point 17): two shares of one owner meeting at a Node steer each other by the Born table instead of spreading by the split table, so `superposition` (a difference of two steps) reads 11 forward each way and 6 on each transverse heading at phase 7, and `cancelled` reads 12, 12, 12, 10 apart at phase 0, nothing in the registers (`tests/test_field_spreading.py`).

Re-pinned on 2026-09-18 under `bit-law-v1`: what spreads is a shadow given with the board (`initial_field.light.rays`, steps 1), so every board reads one tick sooner than the lamp world's; no momentum field, no `field_spread` records (a Node holding shadows alone publishes nothing); the `stream` is the same arithmetic through `spread_content`; `returned`, `source`, `resident` and `unchanged` went with the law (`tests/test_field_spreading.py`, six cases).

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

Re-pinned on 2026-09-18 under `clock-readings-v1`: the momentum field's line carries `spent`, zero in these worlds; the families declare no rate.

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

Retired on 2026-09-18 under the law of the bit (`bit-law-v1`): `tests/test_detector_sampling_contract.py` pinned behaviour the law removed and is deleted; the run is repeated under the law in a follow-up (the worlds stay in `examples/`).

## Wave-ray families

Re-pinned on 2026-09-18 under `clock-readings-v1`: no family declares a rate; every world declares K 1; the massive family of case (b) declares `clock` and its rays of 4 advance 4 steps per interval (phases (77 + 4 t) mod 256); the wide case's ray of 2 advances 2 per interval on the 128-bit circle (`WIDE_RATE` 2, `WIDE_PHASE` the turn less 6; outbound[1] = 2^128 - 4, outbound[100] = 194; a rest rate of 2^70 is no family's to declare); the rejections name `clock-readings-v1` for `phase_advance` and `coherence table` for a carried phase on a family with a clock and no table; `forward_rays` returns the departures' account as a third value.

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

Retired on 2026-09-18 under the law of the bit (`bit-law-v1`): `tests/test_ray_binding.py` pinned behaviour the law removed and is deleted; the run is repeated under the law in a follow-up (the worlds stay in `examples/`).

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

Re-pinned on 2026-09-18 under `return-field-v1` (feature 16d; `tests/test_ray_momentum_turn.py`, `tests/test_wait_rule.py`, `tests/test_clock_readings.py` (d), `tests/test_lanes.py` (d), (f) and (h)): a shadow that pushes turns back with the opposite sign (outbound 0, sign -1) carrying -push, mixes at the next Node it reaches with nothing to meet and parks its ninths there with the momentum on the largest share; a thing turned onto the shadow's line, or pushed head on, rides the Link with it and is pushed once more at the next Node, the same push, after which the share is an outgoing share (sign 1) carrying twice -push, parked at C from the tick after. `turn`: the thing carries (0, -8, 0) from tick 3, the share (0, 16, 0) at C after tick 3, the momentum line current (-8, 16, 0) and escaped (0, -16, 0) from tick 12, the final momentum (-8, 16, 0); `cancel`: each share beside C after tick 2, parked from tick 3; `reverse`: the share parks at (11, 10, 10) with (8, 0, 0); `along`: the thing carries (16, 0, 0) from tick 3 and the share (-16, 0, 0) at C; the wait rule's `shadow` parks at (10, 9, 10) with (0, 1, 0) and `half` owes a whole interval at the second read, paid at tick 3; the neutral and the charged thing carry (0, -4, 0) after tick 3 and the charged one's remainder is (0, -2, 0); the lanes' B carries (0, -8, 0) on its lane and leaves with (0, -16, 0), the ring record's `state.json` digest reads the parked entries' `outbound` and `momentum`, and the merged thing passes the parked ninths of both owners, nothing home.

Re-pinned on 2026-09-18 under `clock-readings-v1` (`ray-momentum-turn-v3`): the module is rewritten to the step of the settled rule (i), the cases `turn`, `cancel`, `reverse`, `along`, `identical` and `rejected` of `tests/test_ray_momentum_turn.py`, the world of 21^3, K 8, `wait_per_quantum` 0, the coupling reading the thing's content (the shadows of `f` have no charge): a thing of 8 heading +X at (4,10,10) meets a shadow of 1 from -Y at C after tick 6; the push (0, -8, 0) is its momentum, the shadow turns back carrying (0, 8, 0), at its departure of tick 7 the thing turns to -Y with nothing carried and (8, 0, 0) spent, both walk -Y together, the momentum line reading current (-8, 0, 0) and spent (8, 0, 0) from tick 7 and the momentum line of the record (0, -8, 0); re-pinned the same day under `node-is-ports-v1` (settled rule (ii)): the shadow's steps are spent at (10,4,10) after tick 12 and it waits there at rest, nothing of `f` leaving the board, while the thing leaves after tick 16 with (0, -8, 0) escaped, the momentum line reading current (-8, 8, 0) from tick 17 and the record's final totals `f` 1 and momentum (-8, 8, 0); in `cancel` each shadow waits at its Node of the board from tick 13; a second shadow from +Y in the same cycle cancels the push, nothing spent, the thing walks on +X; a shadow head on with sign 1 reverses the thing to -X (spent (8, 0, 0)), with sign -1 pushes along its own direction, which turns it nowhere and leaves (8, 0, 0) carried (the momentum line (16, 0, 0)); a world without a table records no identity and runs byte-identically twice; the malformed tables of the first pin are rejected and a table without `reads` names point 16. The tables of the DDA walk below stand as history.

Re-pinned on 2026-09-18 under `node-mixing-v1` (Highlights 5.4 point 24, feature 16c; `tests/test_ray_momentum_turn.py`, on the `ray-momentum-turn-v3` module): a lone shadow no longer walks straight to the thing it pushes, so the thing's lamp is one Link before C, at (9,10,10), and every shadow leaves fresh from the Node beside C ((10,9,10), (10,11,10), (11,10,10)); both reach C after tick 1, the push is in the cycle of tick 2 and every tick is five earlier than the pins above (`turn` 14 ticks, the thing off the board after tick 11; `cancel`, `reverse` and `along` 8 ticks); the return walks its one step back, waits beside C with steps 0 (a waiting shadow reads heading 0 from the tick after it arrives) and nothing of `f` leaves the board.

Re-pinned on 2026-09-18 under `bit-law-v1`: only a shadow pushes, so the `f` rays are shadows given with the board (sign 1) and the coupling reads the thing's charge (`m` charge 1); no `ray_push` record; a returned shadow carries -push, its steps counting down to 0 and staying there; the momentum line is exact at zero until a shadow escapes; the `identical` digests carry the law's identities (`tests/test_ray_momentum_turn.py`).

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

Retired on 2026-09-18 under `clock-readings-v1`: `tests/test_momentum_turn_walk.py` pinned the DDA staircase, which the settled rule (i) retires, and is deleted; the text below stands as its history.

Re-pinned on 2026-09-18 under `bit-law-v1`: the `f` and `g` rays are shadows given with the board, the couplings read the thing's charge (`m` charge 1), no `ray_push` record, the momentum line exact at zero (`tests/test_momentum_turn_walk.py`).

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

Re-pinned on 2026-09-18 under `clock-readings-v1`: the ring's rays of 1 declare `clock` at the world's K; at K 1 they advance one step per interval (the rate 2 of the first pin is out of the bound content / K < N / 2 for a corner's merged output of 2 at N = 8), so (a) reads phases t mod 8 with the lines closing in one circuit and the phases in two (`seen[t] == seen[t - 8]`), (b) the merged outputs of 2 at phase 3 after tick 2 and (2 t - 1) mod 8 after, (d) and (e) likewise with the two-circuit closure, and the record case runs 24 ticks for the extractor's window of two periods of 8 (clock 1, `to_tick` 23, 184 rays, the plain reading period 1 with an unknown clock); (c) runs at K 2, one step every second interval with the remainder t mod 2 on the rays, the phases (t // 2) mod 8, four ticks apart two steps, closing after sixteen (20 ticks).

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

Retired on 2026-09-18 under the law of the bit (`bit-law-v1`): `tests/test_decay_draw.py` pinned behaviour the law removed and is deleted; the run is repeated under the law in a follow-up (the worlds stay in `examples/`).

## The screen with a loop

Retired on 2026-09-18 under the law of the bit (`bit-law-v1`): `tests/test_screen_loop.py` pinned behaviour the law removed and is deleted; the run is repeated under the law in a follow-up (the worlds stay in `examples/`).

## The ring meets its own field

Retired on 2026-09-18 under the law of the bit (`bit-law-v1`): `tests/test_ring_self_field.py` pinned behaviour the law removed and is deleted; the run is repeated under the law in a follow-up (the worlds stay in `examples/`).

## The screen without a draw

Retired on 2026-09-18 under the law of the bit (`bit-law-v1`): `tests/test_screen_no_draw.py` pinned behaviour the law removed (a mark's ticket seed, a body radiating per tick, `field_of`) and is deleted; the run is repeated under the law in a follow-up (the worlds stay in `examples/`).

## Catalog of nature

Re-pinned on 2026-09-18 under `clock-readings-v1`: a ray declares `content` (its rung, the former rest rate in m_0) and `clock`, the units name `content` and the world's `K`, `mass_field` and `mass_field_delay` are retired (11 rays, 15 couplings, 25 undecided entries, A6 no longer a decider), `weak_conversion` declares `decay.after_periods` (undecided, A9) and no `draw`, the neutron's decay names its coupling alone, and the apparatus family declares content 0 and no clock; the worlds case stays skipped (the field families' textual migration is in the feature's remaining list).

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

Retired on 2026-09-18 under the law of the bit (`bit-law-v1`): `tests/test_a5_coulomb.py` pinned behaviour the law removed and is deleted; the run is repeated under the law in a follow-up (the worlds stay in `examples/`).

## A5s Coulomb at rest

Retired on 2026-09-18 under the law of the bit (`bit-law-v1`): `tests/test_a5_static.py` pinned behaviour the law removed and is deleted; the run is repeated under the law in a follow-up (the worlds stay in `examples/`).

## A6 light bending

Retired on 2026-09-18 under the law of the bit (`bit-law-v1`): `tests/test_a6_bending.py` pinned behaviour the law removed and is deleted; the run is repeated under the law in a follow-up (the worlds stay in `examples/`).

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

Retired on 2026-09-18 under the law of the bit (`bit-law-v1`): `tests/test_helium_orbit.py` pinned behaviour the law removed and is deleted; the run is repeated under the law in a follow-up (the worlds stay in `examples/`).

## The dense mode

Re-pinned on 2026-09-18 under `node-mixing-v1` (Highlights 5.4 point 24, feature 16c; `tests/test_dense_field.py`): the boards are built in the module (the field spreading test went with the split table) with nothing declared of the spread; part 2 of the feature (the vectorized mixing, `DenseField._mix`) gives at every Node the integers of `spread_content`, so `split` reads the mixing's integers: the single 12 at phase 6 on +X sends 5 back on -X at phase 2 and 1 on each other heading at phase 6, the sign-0 block (3, 3, 3, 3, 3, 3); the two 3s of opposite sign send 1 back each on -X at phase 4; the quantum on +X with its +X register at 10 parks (1, 4, 1, 1, 1, 1) and the register at 11 releases one forward, left at 2, the block (2, 4, 1, 1, 1, 1); the mixed and three-shadow cases against the oracle as before (the phase of the three is 2); `identity` unchanged in form; `rejected` names a world without a shadow set, an outward field beside the rays and polarization.

Re-pinned on 2026-09-18 under `bit-law-v1` (point 13): the region is the shadow layer, on by default wherever admitted, holding shadows alone (no bit, one block per owner); the boards are shadows given with the board; a mark returns every shadow and counts none; the `boundary` case's world went with the law (`tests/test_dense_field.py`, three cases).

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

The `identity` case gained `counter` on 2026-09-18 (`detector-absorb-v1`, the
click as an absorption), written before its first run: the `source` board
with the mark at (8,7,7) set to 1/1, so the quanta the region hands it click
and are absorbed into its counter at the engine's Node under both modes; the
engine alone and the dense mode give the same `state.json`, the same ledger
(its light line's `absorbed_by_marks` equal to `detector_mark_totals`), the
same `final_totals`, the same `detector_marks` (the one mark's counter light
equal to the totals, positive) and `detector_mark_totals`; the first run
agreed.

## Snapshots from the arrays, parallel series runs and the standing set

`tests/test_perf_arrays.py` is the isolated test of the performance lane of
2026-09-18 (`perf-arrays-v1`; [performance](PERFORMANCE.md#snapshots-from-the-arrays-parallel-series-runs-and-the-standing-set-2026-09-18)),
pinned here before its first run and re-pinned the same day when the Node's
mixing (`node-mixing-v1`, feature 16c) and the clock readings
(`clock-readings-v1`, feature 16b) became the layer's step and the schema
(no split table, no `kerengonen`, a body's whole charge a multiple of its
amount, `wait_per_quantum` 0 as the bit-law test pins its pushes). Two
minimal worlds built as data: the *line*, 9 x 3 x 3 open, two bodies of the
family `m` (amount 2^24, whole charge -2^24, release 1/4096 of the amount:
4096 quanta per heading per fill interval) at (2, 1, 1) and (5, 1, 1), each
reading the other's shadows by the momentum table `{m: 1}` on its charge, a
fill of 8 intervals, the dense mode, the mixing the only spread; the *box*,
9 x 5 x 5 open, the same bodies at (3, 2, 2) and (6, 2, 2). The standing
set's integers are the current rule's (the mixing with the Node-owned
remainder) and are re-pinned when the rule changes; the identities are not
the rule's. Six cases:

- `snapshot`: after 24 ticks of the box, in the dense mode and with the
  engine alone, the text `snapshot_writer.write_snapshot` streams equals
  `json.dumps(world.snapshot(), indent=2)` byte for byte (the dense case
  lists the region's Nodes with their parked shares among the `parked`
  entries, more than one); through the runner, `state.json` of the box for
  24 ticks equals that text of a second world stepped the same 24 ticks plus
  a line break, and its SHA-256 equals the digest the runner of `main` at
  `9c689f1` wrote on the same world before the writer existed (the pin of
  the migration).
- `series`: `tools/run_series.py`'s `run_series` on the line and the box for
  12 ticks each with two jobs: two `run` directories with `run.json`,
  `state.json` and `log.txt`, both rows `completed` with `ticks` 12 and a
  peak RSS above zero, `summary.json` and `summary.md` written, and every
  `state.json` and ledger (`audit` of `run.json`) byte-identical to
  `run_initialization` of the same world for the same ticks in the test's own
  process; two worlds of one name refused.
- `standing`: the line for 200 ticks with `standing_field: true`: the layer
  repeats exactly after tick 30 with period 1 (`standing_field_iterations`
  30, `standing_field_period` 1, the residual `{cells: 0, amount: 0}`), is
  kept fixed for the remaining 170 ticks (`standing_field_ticks` 170,
  `standing_field` true, no fallback), and the things read it as the stepping
  engine gives: the momentum of both bodies after every tick identical to the
  stepping run's, pushes taken before the fixed point (a nonzero momentum
  within the first 30 ticks) and (-186, 0, -1) and (191, 2, 0) at the end,
  the ledger balanced at every tick, `state.json` and the ledger of the run
  byte-identical to the stepping run's.
- `residual`: the same line with `standing_field: 10`: no repeat within 10
  intervals, `standing_field` false, `standing_field_iterations` and
  `standing_field_period` null, the residual of the last comparison
  `{cells: 1316, amount: 3573}`, zero ticks fixed, and the files identical
  to the stepping run's (the layer stepped throughout).
- `fallback`: the line with a lamp at (4, 0, 0) that pays out one thing ray
  of amount 2 on +Y after 130 cycles (`dissolve`): the layer is fixed after
  tick 27 (period 1), the thing's packet changes the engine's part of the
  state at tick 131 and the region falls back to stepping there
  (`standing_field_fallback` `{tick: 131, reason: ...}`, `standing_field`
  false, `standing_field_ticks` 103), and the run's `state.json` and ledger
  are byte-identical to the stepping run's of the same world: the fallback
  is exact.
- `rejected`: `standing_field` on a world without the dense mode
  (`dense_field: false`), a negative `standing_field`, and a non-integer one
  are refused by the parser with the reason.

## The field's books

Retired on 2026-09-18 under the law of the bit (`bit-law-v1`): `tests/test_field_books.py` pinned behaviour the law removed and is deleted; the run is repeated under the law in a follow-up (the worlds stay in `examples/`).

## The clock and the readings

Re-pinned on 2026-09-18 under `node-mixing-v1` (feature 16c; `tests/test_clock_readings.py`): in (b) the shadows s and u leave fresh from (2,1,2) and (4,1,2), share (3,1,2) after tick 1 with their phases 5 and 2 unchanged and no event, and mix there in the cycle of tick 2, each alone, a lone quantum parking whole; in (d) the lamps are at (2,2,1) and (2,3,1) and the star's shadows leave fresh from (3,1,1) and (3,2,1), so the meeting is after tick 1, the push in the cycle of tick 2 and the turn at the departure of tick 2, the things at (3,0,1) and (3,1,1) after tick 3, each return waiting one Link back with steps 0.

`tests/test_clock_readings.py` is the isolated test of `clock-readings-v1`
([the clock and the readings](SPATIAL_FIELDS.md#the-clock-and-the-readings-clock-readings-v1);
Highlights 5.4 points 11, 16, 18, 19 and 20, the model owner's decisions of
2026-09-18), pinned here on 2026-09-18 before its first run. Boards are open,
`link_ticks` 1, costs 1, the six unit-axial headings, 8 ray slots, `release`
[1, 1], N = 8 (`phase_bits` 3) unless said, `wait_per_quantum` 0 (the wait is
pinned in its own module), a three-component `momentum` field; a lamp of a
family emits its whole stock once along its heading in the cycle of tick 0,
recoiling into `momentum`; a shadow of a profile is given with `steps` 0. A
tick t is one `step()`: the cycle of interval t - 1 and the delivery of tick t;
a push of the cycle of tick t is on the thing after tick t + 1, and its step at
the departure of tick t + 1.

- (a) the computation: 9 x 3 x 3, K 2, `m` (charge -1, `clock`): a thing e of
  6 at (1,1,1) +X (three steps per interval) and a thing f of 2 at (1,2,1) +X
  (one), a mark at (5,2,1) [1, 1] on f's line, three shadows of e (amount 1,
  z = 2, +X) that add nothing. The phase steps per completed tick read 4 at
  ticks 1 to 4 (f's step of tick 4 counted, then absorbed on its arrival at the
  mark), 3 at ticks 5 to 8 (e's step of tick 8 counted, then it leaves the
  board on that departure) and 0 from tick 9; `real_content` 8, 8, 8, 6, 6,
  6, 6, 0, 0, 0; the same world without the shadows gives the same running
  totals; the runner records `computation_per_tick` equal to the differences,
  `clock_readings`, `K` 2 and `wait_per_quantum` [0, 1].
- (b) two clocks, no clock on a shadow: 9 x 3 x 3, K 2: e of 6 at (1,1,1) +X
  is at (1 + t, 1, 1) after tick t with phase 3 t mod 8 and remainder 0; f of
  2 at (8,2,1) -X at (8 - t, 2, 1) with phase t mod 8; a shadow s of e (phase
  5) at (1,1,2) +X and a shadow u of f (phase 2) at (5,1,2) -X are at (1 + t,
  1, 2) and (5 - t, 1, 2) with phases 5 and 2 and remainder 0 at every tick,
  share (3,1,2) after tick 2 with no event there, and the running total of
  phase steps reads 4, 8, 12, 16.
- (c) the bound: at N 8 and K 1 an emission of 3 parses and one of 4 is refused
  naming half the phase circle; at K 2, 7 parses and 8 is refused. Two things
  of half that content head on, at (1,1,1) +X and (5,1,1) -X, under an outputs
  rule joining them into one output of the sum on +X: the totals read the sum
  after tick 2, and the third step fails closed with the same words (K 1: 4;
  K 2: 8).
- (d) the readings: 9 x 5 x 3, K 4: a neutral thing n of 4 (`n`, charge 0,
  `clock`) at (1,2,1) +X and a charged thing c of 4 (`c`, charge 1 per
  quantum, `clock`) at (1,3,1) +X; a body of `e` (charge -1 per quantum on
  the family, the body's whole charge -1, amount 32, thing 3) at (7,4,1), its
  shadows of 1 at (3,0,1) and (3,1,1) on +Y; per pushed family a gravity rule
  (table {"e": -1}, `reads` "content") and an electric rule ({"e": 1},
  `reads` "charge"). The owner table reads content 32 and charge -1 for thing
  3 and the push denominator is 32. Each thing meets its shadow after tick 2;
  in the cycle of that tick the gravity reading gives (0, -4, 0) to each and
  the electric reading 0 to n (its charge 0) and -1 / 32 to c: nothing into
  its momentum, the remainder (0, -1, 0). The momentum line reads (4, 0, 0),
  (4, 0, 0), (0, 0, 0) after tick 2 and (0, -4, 0), (0, -4, 0), (0, 0, 0)
  after tick 3, both things turned to -Y at their departure of tick 3 with
  nothing carried, n at (3,1,1) with remainder (0, 0, 0) and c at (3,2,1)
  with `push_remainder` (0, -1, 0); each shadow, read twice, walks back -Y
  carrying (0, 4, 0) with steps 1; the momentum line's `spent` reads (8, 0,
  0); no push and no draw is an event.
- (e) the decay table: the unit-square ring of `tests/test_loop_binding.py`
  (K 1) under a rule `weak` declared before its corner table, participants
  two electrons, outputs the two inputs on +Z and -Z. With `decay`
  {"after_periods": 3} the corners hold two rays each after ticks 1 to 3 with
  passages 0, 1 and 2, the third meeting (the cycle of tick 3) breaks every
  corner's pair, and after ticks 4 to 6 the corners are empty and eight rays of
  1 with passages 0 stand tick - 3 Links above and below them on +Z and -Z,
  content 8 exact; with {"content_at_most": 1} the ring holds for eight ticks
  with the passages counting up, with {"content_at_most": 2} it breaks at the
  first meeting; two runs write the same `events.jsonl` and no `decay_draw`
  identity; `draw` with `seed` is refused naming `clock-readings-v1`, an empty
  or a double condition names one condition, `after_periods` 0 is refused, and
  `decay` on a rule without outputs names the outputs.

## The wait per quantum read

Re-pinned on 2026-09-18 under `node-mixing-v1` (feature 16c; `tests/test_wait_rule.py`): the thing's lamp is at (9,10,10) and the shadow leaves fresh from (10,9,10), both at C after tick 1, the push in the cycle of tick 2 and every tick five earlier than pinned below (eight ticks per case): with w = 1 the thing waits the interval of tick 2 and steps to -Y at tick 3, with w = 2 it waits ticks 2 and 3 (`owed` 1 then 0), with w = 1/2 it steps at tick 2 owing 1; the returned shadow waits at (10,9,10) with steps 0.

`tests/test_wait_rule.py` is the isolated test of Highlights 5.4 point 23
under `clock-readings-v1` (a thing pays a tick for every whole quantum it
reads, the model owner's decision of 2026-09-18), pinned here on 2026-09-18
before its first run, on the world of `tests/test_ray_momentum_turn.py` with a
thing of 1 (K 1: one phase step per interval) at (4,10,10) +X and a shadow of
1 from -Y at (10,4,10), the coupling reading the content with sign -1: a push
of one whole quantum, (0, -1, 0), in the cycle of tick 6.

- (a) w 1: after ticks 1 to 6 the thing is at (4 + t, 10, 10) with phase t and
  the running phase steps t; after tick 7 it is still at C with steps 6, phase
  6, momentum (0, -1, 0) and nothing owed (its one interval spent), the
  running total 6; from tick 8 it is at (10, 17 - t, 10) heading -Y (the
  component reached its content at the departure of tick 8) with phase and
  steps t - 1 and the running total t - 1; the ledger balances at every tick.
- (b) a shadow pays nothing: the shadow is at (10, 4 + t, 10) after ticks 1
  to 6 and, turned back with (0, 1, 0), at (10, 16 - t, 10) with steps 12 - t
  from tick 7, one Link every interval while the thing waits; no shadow ever
  owes.
- (c) w 2: the thing stays at C after ticks 7 and 8 (owed 1 then 0, phase 6,
  steps 6, the running total 6) and is at (10, 18 - t, 10) from tick 9 with
  phase and steps t - 2.
- (d) no reading, no wait: alone, at w 2, the thing is at (4 + t, 10, 10)
  after every tick with phase t and the running total t.
- (e) w 1 / 2: one quantum read owes half an interval, kept exactly (`owed` 1
  in units of 1 / 2) and never spent: the thing steps at tick 7 as if it owed
  nothing and carries the debt; `wait_per_quantum` [11, 9] parses as (11, 9),
  the default is (1, 1), and [1, 0], -1 and [1] are refused.

## A Port is two lanes

`tests/test_lanes.py` is the isolated test of `lanes-v1`
([a Port is two lanes](SPATIAL_FIELDS.md#a-port-is-two-lanes-lanes-v1);
Highlights 5.4 point 25, the model owner's decision of 2026-09-18, feature 18),
pinned here on 2026-09-18 before its first run, as Highlights 5.5 requires.
The boards are those of `tests/test_node_is_ports.py` (open, `link_ticks` 1,
costs 1, the six Port headings, family `m` with charge -1 and `release`
[1, 1], a lamp a thing that spends its content) and, for the contested lane,
that of `tests/test_ray_momentum_turn.py` (21^3, K 8, `wait_per_quantum` 0,
the family `m` of charge 1 with a clock and the shadow family `f`, the
coupling `turn` reading the content with sign -1). Written before the first
run, all of it computed from the rules:

- (a) the slots: the family `m` of a world with a lamp `e` (thing 1) and a
  profile shadow of owner 2 has owners (1, 2). The rays of one Node, a thing
  of 4 on +X with steps 1, a shadow of owner 1, amount 3, on +X (steps 1), a
  shadow of owner 2, amount 5, on -Y (steps 1), a trace of owner 1 on +X and a
  returned thing of 4 at its event Node (-X, outbound 0, steps 0), read as:
  twelve real slots and twelve shadow slots of two owners each; the thing in
  the real slot of lane 2 (Port 1, in: it entered through -X), every other
  real slot empty; the owner-1 shadow in slot (2, 0) and the owner-2 shadow in
  slot (4, 1) (Port 2, in: it entered through +Y), every other shadow slot
  empty; the trace among `parked`, the returned thing among `resident`;
  `lane_index` reads (0, in) 0, (0, out) 1, (5, out) 11; a second thing of
  another key on +X is refused with a message naming point 25.
- (b) two reals declared on one lane: two lamps `e` and `e2` of content 4
  seeded at (1,1,1), both emitting `m` on +X, are refused at parsing with a
  message naming point 25 and both lamps; seeded at (1,1,1) and (1,2,2) they
  parse; a family whose sequence is [+X, +X, -X, +Y, -Y, +Z, -Z] with
  `rays_per_tick` 2 is refused (its sweep repeats a heading); with
  `rays_per_tick` 1 it parses.
- (c) a table with two outputs on one heading: a rule of `m` meeting `m` whose
  two outputs both leave `"reversed"` of input 1 is refused at parsing with a
  message naming point 25 and outputs 0 and 1; two outputs on Port 0 likewise;
  outputs `"same"` of input 0 and `"reversed"` of input 1 parse (their
  coincidence is a meeting's, decided there).
- (d) the contested lane: the world of test_ray_momentum_turn (a) under
  node-mixing-v1 with a second thing: lamp A of 8 at (9,10,10) heading +X
  (thing 1), lamp B of 8 at (10,11,10) heading -Y (thing 2), the shadow of 1
  from -Y at (10,9,10) with sign 1 and steps 0 under `turn({"f": -1})`
  (re-derived on 2026-09-18 when node-mixing-v1 merged: a shadow that has
  walked a Link mixes at every Node, so the three start one Link from C =
  (10,10,10) as test_ray_momentum_turn does). After tick 1 all three are at
  C: A (heading +X, phase 1, steps 1), B (heading -Y, phase 1, steps 1), the
  shadow (+Y, steps 1); `thing_momentum` {1: (8,0,0), 2: (0,-8,0)}, the
  momentum line current (0,0,0). In the cycle of tick 2 at C the shadow
  pushes A, the first thing in slot order, by (0,-8,0) and turns back on -Y
  carrying (0,8,0); B, already on -Y, keeps its lane, and A, whose momentum
  has reached its content on Y, finds the -Y lane taken: it keeps +X with its
  momentum (0,-8,0) accumulated. After tick 2: A at (11,10,10) (heading +X,
  phase 2, steps 2, momentum (0,-8,0)), B at (10,9,10) (heading -Y, phase 2,
  steps 2), the shadow at (10,9,10) with its steps spent (0, -Y, momentum
  (0,8,0)), waiting there from then on; `thing_momentum` {1: (8,-8,0), 2:
  (0,-8,0)}; the momentum line current (0,0,0), spent (0,0,0), escaped
  (0,0,0). At its departure of tick 3 A steps to -Y, the lane free: after
  tick t >= 3, A at (11, 12 - t, 10) (heading -Y, phase t & 7, steps t, no
  momentum), B at (10, 11 - t, 10), one Link each per interval;
  `thing_momentum` {1: (0,-8,0), 2: (0,-8,0)} through tick 11; the momentum
  line current (-8,0,0) and spent (8,0,0) from tick 3. B leaves the board
  after tick 12 (escaped (0,-8,0), current (-8,8,0), `m` 8) and A after tick
  13 (escaped (0,-16,0), current (-8,16,0), `m` 0); `f` 1 and nothing of it
  escaped at every tick; the books balanced at every tick; no `ray_push`.
  The control without B: A at (10,9,10) after tick 2 with spent (8,0,0), as
  test_ray_momentum_turn pins.
- (e) two owners' shadows on one lane (re-derived on 2026-09-18 under
  node-mixing-v1): two lamps of content 0 (things 1 and 2, nothing emitted)
  at (1,2,2) and (1,3,3) on 8x5x5, and at (3,2,2) on +X three shadows: owner
  1 amount 3 with steps 1, owner 1 amount 2 with steps 0, owner 2 amount 6
  with steps 1. In the cycle of tick 1 the two shadows that have walked a
  Link mix at (3,2,2), each alone: four ninths back through -X, the whole
  quanta 1 (of 3) and 2 (of 6), and the rest parked in ninths, 3 and 6 on
  each of the six headings; the fresh shadow of 2 walks on to (4,2,2). After
  tick 1 the lanes read: at (2,2,2) lane 0 (Port 0, in) shadow slot 0 amount
  1 and slot 1 amount 2 (steps 1 each), one slot per owner, every other
  shadow slot and every real slot empty, nothing parked or at rest; at
  (3,2,2) twelve parked shadows, (owner 1, 3 ninths) and (owner 2, 6 ninths)
  on every heading, outside the lanes, every slot empty; at (4,2,2) lane 2
  (Port 1, in) shadow slot 0 amount 2 (steps 1) and slot 1 empty;
  `shadow_content` 11, `real_content` 0, the shadow line initial 11 and
  current 11.
- (f) the record unchanged: `examples/nature/ring.json` for 8 ticks:
  `events.jsonl` sha256
  091f6666d75ec307bf5d13f3f82123fab34c1d68524bade9b59d9fdbdcf20420 and
  `state.json` sha256
  3de44da77e91431f4208f648d747b6a84665e7aad74e03a18f9cf406bf201afa, computed
  on origin/main at 3cfb5e4 before the change; `run.json` reads `lanes`
  "lanes-v1" beside `node_is_ports`.
- (g) two real rays of one family on one lane are one real ray (the model
  owner, 2026-09-18, on the case this feature left open): in the pure function
  `merge_lane` on the light family of test_ray_polarization (a coherence table
  of eight steps), a ray of 3 at phase 0 (steps 2, owner 1) and one of 4 at
  phase 2 (steps 1, owner 2) given lane 0 are one ray of 7 at phase 1, the
  step nearest their coherent sum 3 + 4i, with owner 1, owners (2,) and the
  first ray's record; a passing thing of 4 on -X (steps 3, owner 1) and a
  returned thing of 1 on -X (outbound 0, steps 3, owner 2, its event on Port
  0) are one thing of 5 on -X with the passing thing's record, owner 1,
  owners (2,) and the momentum (2, 0, 0), the ledger's sum -4 + 1 = -3 less
  its own motion -5; a claim of another family on a taken lane is refused
  naming point 25; a ray whose owners name its own owner is refused by
  `validate_rays` naming lanes-v1. In the world (8x5x5): P of 4 at (7,2,2)
  heading -X (thing 1) and R of 1 at (1,2,2) heading +X (thing 2) meet at the
  mark M (4,2,2), setting [1, 2] with `on_click` pass, after tick 3: P, the
  first arrival in Port order, passes (a `detector_click` of bit 1, nothing
  absorbed, the mark's resident empty) and R is returned onto P's lane (one
  `detector_return`); after tick 4 one thing at (3,2,2): -X, amount 5, steps
  4, owner 1, owners (2,), momentum (2,0,0), P's event record (mask 2, shares
  (0,4,0,0,0,0)), its charge -5; it leaves the traces of both owners at M (two
  zero-amount parked shadows on -X); it is at (7 - t, 2, 2) after ticks 5, 6
  and 7 with steps t and leaves the board after tick 8. `real_content` 5
  through tick 7 and 0 after tick 8 (the real line current 5 then 0, escaped
  0 then 5); `thing_momentum` {1: (-4,0,0), 2: (1,0,0)} through tick 2,
  {1: (-4,0,0), 2: (-1,0,0)} after tick 3 (a returned thing's momentum read
  on its heading; corrected before the first passing run, the first draft
  read the ledger's negation and no click), {1: (-3,0,0)} from tick 4 through
  7, {} after tick 8; the momentum line current (0,0,0) through tick 7 and
  (3,0,0) after tick 8 with escaped (-3,0,0), the books balanced at every
  tick; no `ray_push`.
- (h) a merged owner set: the world of (g) with a shadow of owner 1 at
  (1,2,2) and one of owner 2 at (0,2,2), each of amount 1 on +Y with steps 0
  and a mark one Link up +Y ((1,3,2) and (0,3,2), [1, 1]) that returns it,
  the engine alone (`dense_field` false, the region's read-back of a waiting
  shadow not keeping its heading): after tick 1 each is at its mark walking
  back (-Y, outbound 0, steps 1), after tick 2 at rest at its Node (steps 0),
  where it waits, no trace of its owner being there (R's trace at (1,2,2) is
  owner 2's). The merged thing reaches (1,2,2) after tick 6 and (0,2,2) after
  tick 7: in the cycle of tick 7 owner 1's shadow is home to it and
  re-released +Y (at (1,3,2) after tick 7, returned again, at rest at (1,2,2)
  after tick 8), and in the cycle of tick 8 owner 2's shadow is home to it by
  the owner set and re-released +Y (at (0,3,2) after tick 8); `shadow_content`
  2 at every tick, the shadow line initial 2, current 2, escaped 0,
  absorbed_at_home 0.
- (i) two real families on one lane: a lamp of `m` and a lamp of `g` (charge
  0) both at (1,1,1) emitting on +X, a declared board with things of two
  families on one lane, are refused at parsing with a message naming point 25,
  both lamps and both families; with the lamp of `g` at (1,2,2) the world
  parses; at a departure a real of another family on a taken lane is refused
  as a meeting the table of the pair decides, not a departure's to hold.

Re-pinned with feature 18 (`lanes-v1`, 2026-09-18): in
`tests/test_configuration_validation.py` the shipped worlds
`examples/nature/absorption.json`, `absorption_emission.json` and
`helium_ion.json`, whose tables `absorb` and `nucleus_turn` send two outputs
on one heading, are refused at parsing with a message naming point 25 until
the model owner declares their tables anew; in
`tests/test_ray_meeting_conversion.py` the table with two outputs on Port 2
is refused at parsing naming point 25 (its momentum invariant is no longer
reached); in `tests/test_ray_polarization.py` two lamps at one Node emitting
on one heading are refused at parsing naming point 25 (the merge identity
stays pinned on the pure function). The lane is one direction of a Port, so
the departure claims and the plan check take the rays on the six Port lines:
the worlds of `test_ray_field`, `test_energy_audit`,
`test_ray_merge_contracts` and `test_local_focus`, whose headings are not
Port headings, run as before.

The case this feature left open, a ray born onto a lane another thing
continues on in the same interval, was decided by the model owner on
2026-09-18 (Highlights 5.4 point 25, PR #294): two real rays of one family
given one lane are one real ray (the merge of (g)), two of different families
a meeting the table of the pair decides: a declared board with things of two
families on one lane is refused at parsing and a departure that would put two
on one lane is refused (the reading that every pair of thing families must
declare a table would refuse 86 shipped worlds, a5, a6, a12, e10 to e12 among
them, whose things never share a lane, and is not taken here; the coordinator
holds the question). Re-pinned on 2026-09-18 by what the merge gives:
`tests/test_ray_hidden_state.py` (A's +X ray and B's emission one real ray
of 7 at the coherent sum's phase 1 with owners (2,) from tick 3, 7t - (t - 2)
rays after t ticks, (9,7,7) [(7, 4)] and (8,7,7) [(7, 3)], one ray counted);
`tests/test_energy_audit.py` (the self-exclusion world: 38, 36, 36, 34, 34,
the quantum of the cycle before and the new one leaving on one lane as one
real ray of two quanta with the older event's record, which the one-Link
exclusion does not name); `tests/test_detector_mark.py` (after tick 2 each
returned ray and the passing ray of the opposite lamp are one thing with the
passing ray's record and both owners: 3 on -X at (6,7,7) carrying (4,0,0), 7
on -Y at (7,6,7) carrying (0,8,0), 11 on -Z at (7,7,6) carrying (0,0,12), the
ledger's sums less their own motion; each momentum reaches the content, so at
its departure of tick 3 every pair turns back to C, spending 3, 7 and 11 on
the momentum field's line, which the cycle record publishes as `spent` and
the local audit reads: after tick 3 the pair of 3 passed C on +X carrying
(1,0,0), the seventh arrival, the pair of 7 was returned on -Y carrying
(0,-1,0), the eighth, and the pair of 11 passed on +Z carrying (0,0,1), the
ninth; the world's momentum (3, 7, 11), the lamps never restored, no inverse
split, the counter at nine, the marked world equal to the control through
tick 2); the four cases of `tests/test_kerengonen.py` pass as pinned. A
merged thing above its family's K and N bound is the decay table's business
(point 20), so `validate_rays` leaves it to that. The case `a_and_b` of
`tests/test_ray_layers.py` was deleted on 2026-09-18: a turned b ray and the
c ray are given one lane at the meeting Node, two real rays of different
families with no table naming both, which no departure holds; `a_only` stands.
