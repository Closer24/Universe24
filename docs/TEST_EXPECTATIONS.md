# Test inputs and expected results

## Complete-ray direction projection

`test_ray_heading_flux.py` distinguishes the optional carried-heading readout
from the default last-hop projection: amount three with heading `(2,1,0)` arriving
through +X reads `(6,3,0)` versus `(3,0,0)`. The actual receiver cannot respond
before causal delivery, and its configured response has an equal opposite field
reaction. Opposite headings cancel; signed amounts reverse the projection; empty
resident rays and an immutable baseline contribute no heading. Supported local
self-exclusion removes the full own-ray vector while retaining external input.
Missing owners, excessive capacity, invalid selection and overflow reject; a
receiving ray and carrier remain unchanged on overflow. The explicit projection
adds ten unit-cost operations per declared ray slot. These checks establish
direction access, not an electron orbit or a physical force law.

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
tables after host-cache eviction, independent trigonometric reference entries,
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

`test_active_node_contracts.py` exercises receipt and completion at all six Ports
for the active carrier Node and spatial Node. For the same
local payload and fixed capacity it varies world extent, unrelated resident/event
counts (0, 8, 128) and elapsed model ticks. The measured production-path line counts,
modeled carrier cost, local event count and recursively retained payload size must
stay equal. Host world indexes are made unreadable during each local transition.
Expected outputs remain explicit: one carrier crosses one Link and spatial stock
64 is owned locally or in outgoing packets.
These are bounded-work regressions plus state/locality guards, not a timing-based
proof for arbitrary callbacks, whole-world scheduling or remote evaluation.
The source-envelope Node's cases of this suite (its six-Port transition and its
gate and terminal transitions) were deleted on 2026-09-17 with the envelope
modules (issue #164, bucket B.3).

Shared builders live in narrowly scoped `tests/support/` modules. Their imports
remain dependencies of every consuming test. They do not contain alternate
simulation engines. `test_generic_identity.py` records one immutable seven-tick
baseline per configuration; rename, reorder and combined variants each retain
their own world and all state/event/accounting comparisons. Baseline conservation,
activity and input immutability assertions are retained.

| Removed or consolidated execution | Retained or stronger acceptance |
| --- | --- |
| Three self-identity assertions in the obsolete Node alias test | Recursive NodeState/schema rejection tests remain; no supported alias requirement was being checked by the self-comparisons |
| 21 repeated classic baseline worlds | Seven immutable baselines and all 21 independent transformed worlds; all original trace and accounting assertions |

The representative regime-coverage test must fail if a new catalog property value
is not represented. Data preparation remains checked for every entry. Catalog
mass and spin are passive inventory/properties in this candidate; these tests do
not establish species dynamics. Distinct signed, overflow, denominator, boundary,
null/capture and correlated-state cases are not removed. The exact 25-ticket
fixtures remain exhaustive.

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


## Computational response

`test_node_work_emission.py` checks committed local work, zero startup, pending
cycles, moving-carrier arrival without transported cost, bounded readout inputs
and emission-only expression scope. Shared-clock integration checks the same
Node-owned cost across a moving emission and rejects conflicting clock selections. `test_computational_response.py` checks real
one-link delivery on all six ports: a unit reaction opposite travel, its exact
local field counter-reaction, no early/repeated response, cancellation and a zero
or reversed property coupling. These tests establish the configured mechanism,
not a Newtonian or energy-conserving physical model.

## Integer Node execution

`test_node_rule_contract.py` checks six-record frozen permutations, generic vector
widths, explicit fired-rule duration, nonadditive policy rejection and independent
arrival presence. `test_node_conservation.py` checks complete-owner readouts and
rejects nonlinear merge drift (13 becomes 25), unequal momentum, overflow and
capacity errors without modifying inputs. `test_node_conservation_configuration.py`
checks exact layout coverage and rejection through the read-only preflight.
`test_node_runtime.py` checks isolated Node boundaries; `test_node_vector_integration.py`
checks public execution, timing and failed-transition atomicity.
`test_joint_reaction_configuration.py` checks role ownership, capacity, ambiguous
references and rejection of transient commit guards. `test_joint_node_reactions.py`
checks distinct property layouts, deterministic disjoint selection, all 32 local
slots, frozen group/field updates, guard invalidation and participant locks.
`test_field_commit_guards.py` reproduces a delayed norm violation (32 to 34),
including a zero-net-delta phase, and requires rejection before any owner changes.
It also covers valid arrivals, ordered guards, consumed triggers and direct
assembly boundaries. `test_node_vector_examples.py` owns the three example configurations and their
independently known declared readouts. These are correctness contracts for the
[selected model](NODE_VECTOR_PROCESSOR.md), not proofs of quantum dynamics.

## Shared field computation delay

`test_spatial_computation_delay.py` checks the opt-in
[shared-cycle contract](SPATIAL_COMPUTATION_DELAY.md). With unit scalar merge
cost 32, field costs 68/69/169 and B=100,h=2, departures occur at 0/2/4 and
receipts at 2/4/6. Field/carrier costs 20+20 plus merge32 share C=72, giving
one wait at B=40. Later arrivals cannot alter the frozen result or deadline;
their original owners, source allowances and declared linear inventory remain
exact through commit. Nonlinear guards stop before the affected transaction
mutates stock. Real scalar/vector costs, empty input intervals, moving sources,
finite decay, formula-free state and passive conservation are covered. These
are timing and inventory claims.

## Property coupling and passive local conservation

`test_property_couplings.py` requires property compatibility across differently
named layouts, all supported selector families, missing-property rejection,
fraction/budget ownership and identical timing for equivalent check expressions.
`test_property_entity_profiles.py` validates the shared catalog profiles and
two independent reservoirs: total energy 14 and momentum zero persist through
four ticks while the neutral control stays unchanged. Late energy or momentum
corruption must fault without correction.
`test_local_conservation.py` covers local changes and actual packet flux,
pending originals, periodic/open transit, all momentum components, nonlinear
arrival cancellation, passive observation and saved failure reports. These
measurements use explicit candidate quantities, not inferred physical energies.

## Coupled unit excitations

`tests/test_coupled_excitations.py` owns the independent expectations for the
[local coupling candidate](COUPLED_EXCITATIONS.md). Positive absorption of Y into
an empty receiver gives internal Y and recoil +X; negative coupling gives -Y
with the same recoil. Zero coupling forwards unchanged. Positive emission of
internal Y gives spatial -Y and recoil -X; occupied Y/Z exchange gives internal Z
and spatial -Y without recoil. All admissible cases retain the declared U/P at
every tick, counting actual in-flight owners once. Delays preserve original state
until atomic commit; send/arrival and release follow causal event order. Invalid
state and a deliberately out-of-envelope concurrent arrival test rejection,
without claiming energy conservation through an invalid same-mode merge.

## Configuration preflight

The [validation contract](CONFIGURATION_VALIDATION.md) is covered by
`test_json_documents.py`, `test_profile_validation.py` and
`test_configuration_validation.py`. Shipped runnable configurations must pass;
unknown/ambiguous formats, duplicate keys, nonfinite numbers, invalid references,
bad placements and missing/mismatched dependencies must fail. All 46 classical
profiles are checked independently, including unselected rows; subsets remain
valid. Tests forbid world construction
and implicit filesystem access, preserve supplied objects and verify CLI batch
exit/report behavior and rejection before runner artifacts are created. Existing
UI and runner tests retain accepted output and physical execution contracts.
The native event-program validation and the spatial causal-event suites were
deleted on 2026-09-17 with the `event_program` member.


## Local observer

The [observer contract](LOCAL_OBSERVER.md) specifies causal receipt withholding,
two-tick periodic transit, signed post-decay readings, zero versus absence,
unchanged physical states/costs, exact prefixes, clock independence from global
timestamps and archive exhaustion. `tests/test_local_observer.py` checks these
paths. `tests/test_observer_playback.py` checks safe labels, backward seeking,
paused-clock samples and the explicit world-audit switch. These are observation
contracts, not human vision or Maxwell acceptance tests.


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



## Transverse directional-wave candidate

`tests/test_directional_wave.py` validates the configuration-defined
[candidate](DIRECTIONAL_WAVE.md). The unequal 3Y/2Y encounter produces 3Z/-2Z
while preserving U=13 and P=5X. It also checks coincident/dark readouts, solitary
motion, all six modes, same-law cubic covariance, periodic state return and
atomic rejection of longitudinal, oversized, amplified or misrouted proposals.
These are candidate acceptance tests, not evidence of Maxwell dynamics.


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


## Local reflection and Maxwell-limit experiment

`tests/test_maxwell_configuration.py` checks the selected six-population
configuration with an independent nontrivial reflection example and involution,
an atomic rejection of an inexact half, exact one-link population ownership,
frequency recovery from a signal containing static and fast components, and
divergence on initially empty neighboring nodes. The tests validate these
mechanisms; the [experiment](../examples/maxwell/README.md) records physical
agreement and failures separately. Frequency forecasts and the Gauss
counterexample are specified in its independent derivation before engine runs.

## Small-space physical comparisons

See [the experiment evidence](../examples/small-space/README.md).
`tests/test_small_space_experiments.py` checks finite reservoir depletion with
zero injection, delayed-by-one-link source response and opposite vector stock,
and a restricted unequal-mass momentum permutation. It also rejects a nonzero
total-momentum pair and checks classical units using actual displacement.
The experiment report separately exposes missing physical laws; an accounting
pass must not be relabeled as physical acceptance.

## Physical entity catalog and elementary probes

`tests/test_entity_catalog.py` checks coverage of the Standard Model inventory,
disturbance families and representative interactions, alongside sourced values,
unknowns, units and reciprocal identity links. Negative inputs cover executable
content, invalid references, measurement descriptors, alias cycles and reaction
charge imbalance. These tests validate a reference, not a physical derivation.

`tests/test_physical_entities.py` covers the sourced catalog and only its new
runtime probes. Antiparticle references must be reciprocal where applicable,
charges conjugate and neutrino ambiguity explicit. Example references and
particle properties must agree with their catalog mappings.

The equal-mass contact swaps momenta without a continuum update formula;
individual positive masses/opposite charges and joint momentum/norm persist.
Equivalent local trials on 9-cubed and 15-cubed domains and different lattice
axes must agree before any boundary can matter. Rest and separated states must
not trigger the contact. Two transverse field payloads travel one neighbor per
two ticks with retained and in-flight ownership counted once. These checks do
not establish Maxwell dynamics, annihilation or general classical emergence.
See [the acceptance limits](PHYSICAL_ENTITIES.md).

## Generic local field rules

These are focused acceptance requirements for
[LOCAL_FIELD_RULES.md](LOCAL_FIELD_RULES.md), not claims that a particular tree
passed. Reuse the affected run and tests when collecting integration evidence.

| Suite | Independent inputs and required outcomes |
| --- | --- |
| `test_local_field_rules.py` | Two-vector exchange/rotation reads one frozen rule snapshot and preserves its named invariant; existing outward 216-unit pulse still sends 36 to each axial neighbor; retained and six outgoing owners count stock once and wait a full link; signed counterflows remain separately observable; cross-field changes appear as transformations rather than sources; invalid shapes, bounds, schema 2 rules and broken invariants fail before local commit |
| `test_spatial_interactions.py` | Multiple field/carrier assignments commit together; conserved combined components hold; delayed field evolution is preserved when a frozen delta commits; an invariant invalidated by live field changes rejects the whole transaction; pending source bookkeeping is not restored from old carrier state |
| `test_workspace_integration.py` | Field/type renaming preserves groups and directional/joint references; field-only playback reads node values once, keeps field packets separate, and does not mutate the recording or add received samples as inventory |

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
| `test_workspace_retention.py` | Finished/failed/cancelled jobs and exports expire, active and orphaned children protect companion files, log-close failures keep their lease, stale links return 404, linked output paths cause no writes or process launch |
| `test_check_scope.py` | Explicit non-import edges retain identity-example and reference-script consumers; the exact scope report expires while unrelated files survive; dry-run creates no output |

Ordinary test execution leases its JUnit report. Neither test collection nor
cleanup enables rendering.

## Configured boundaries and dormant spatial work

| Suite | Independent expectations |
| --- | --- |
| `test_boundary_configuration.py` | Periodic default under both schemas; exact open/periodic setting; every positive and negative face of a 3x4x5 world; single-node extents; invalid names, coordinates, faces and bounds rejected |
| `test_open_boundaries.py` | Carrier exits and wrapping on all six faces after full transit; unchanged signed vectors; terminal quantity 1 escapes even with zero retention while an interior copy decays; mixed corner fields/baselines; invalid terminal payloads commit neither loss nor removal; unused emitter allowance does not become physical escape |
| `test_spatial_scheduling.py` | Optimized and forced full-sweep runs have identical per-tick snapshots, costs, events and balances; dormant history is not enumerated; reactions reactivate known idle nodes without delaying their departure; newly created nodes are not backdated |
| `test_disturbance_application.py` | Open example records carried escape 72, spatial escape 20 and 52 localized deposits with zero dissipation; no carrier reentry; zero-tick edge case has empty events and zero escape; runner and snapshot agree |
| `test_workspace.py`, `test_workspace_integration.py` | Workspace accepts field examples and records open escape; direct/HTTP runs retain equal physical output; open terminal playback does not wrap or dereference a missing target; balanced loss/escape is not a failed check; field renaming updates flux expressions |

Measured performance comparisons use the same 5,000 ticks, configuration,
per-tick accounting and three-record checks. Record source import paths and
fingerprints, stepping and diagnostic time separately. Timing is evidence for
that machine, not a fixed wall-time test threshold or a change to model cost.

## Finite spatial candidate, schema 2

The law is specified in [SPATIAL_FIELDS.md](SPATIAL_FIELDS.md) and
[SPATIAL_COUPLINGS.md](SPATIAL_COUPLINGS.md). These tests retain the schema 1
conservative expectations and add separate finite attenuation expectations. The
historical dissipative cases select `"residue": "dissipate"` explicitly; omitting
the key selects the default localizing residue.

| Suite | Independent inputs and required outcomes |
| --- | --- |
| `test_dissipative_initialization.py` | Version 2 requires strict integer retention and nonnegative component budgets; version 1 rejects new keys; invalid signs, shapes, bounds, missing fields and splitting sources fail |
| `test_spatial_decay.py` | Half retention maps 20 through 10, 5, 2, 1 to 0; both signed one-unit tails vanish even at retention `(MAX_VALUE-1)/MAX_VALUE`; unsigned invalid input cannot be erased by decay |
| `test_finite_spatial_engine.py` | Link times 1, 2 and 3 preserve in-flight stock until arrival; budget 5/request 2 emits 2, 2, 1 then 0; moving and delayed sources cannot restore allowances; baseline remains; delivery failure commits neither loss nor packet removal; the default localizing residue keeps a 20-unit pulse at total 20 with deposits 10, 5, 3, 1, 1 along its path and zero dissipation under both field clocks, deposits two separate 1-unit arrivals before merging, leaves deposits in place under later arrivals, and rejects unknown residues while the runner records `finite-localizing-v1` |
| `test_ray_field.py` | DDA rays return to their heading after one period with bounded accumulators; emission shares 5 over 2 rays as 3 and 2 and cycles the cursor, and a stock below the sweep count fills the next headings in turn (2 over 4 headings gives 0 and 1, then 2 and 3, then 0 and 1) while a stock that covers the sweep still advances by the whole count; a 64-unit ray source keeps totals at 64 per tick and 64 on every Manhattan shell; a receiver gains 15 momentum from three ticks of 5-unit ray flux; retention 1/2 deposits 4, 2, 1, 1 along a ray or dissipates 8; a third ray phase at a two-slot Node fails explicitly; open boundaries count escaped rays; invalid keys, zero headings, vector fields, octant seeds and the shared clock are rejected; the runner records `isotropic-ray-field-v1`; a ray passes a Node whose receiver reacts to it and reaches the Nodes beyond |
| `test_gravity_probe.py` | Held bodies beside an axis-ray source gain momentum toward it, proportional to mass within the carried integer remainder, with combined carrier plus local-field momentum conserved; a moving body starting five links out only moves inward with growing inward momentum, turns between five and seven links past the source with zero momentum, and comes back through it: a bound oscillation with combined momentum still zero; signed quanta pull held bodies toward the source and each pays exactly the momentum it gains from its stock, the far body takes its share of what the near one left, the source is credited 65,536 per tick with zero recoil and the quanta close; a body with stock 50 stops at momentum -50 with the event audit passed |
| `test_energy_audit.py` | Funded emission along (1,0,0) and (0,2,0) debits the emitter by 2 per tick and recoils by (-1,-2,0) per tick with the audit closed; a stock of 5 emits 2, 2, 1, 0; `source: true` is still rejected and `recoil_field` needs funding; escaped quanta are measured escape; an absorber banks five quanta with momentum (5,0,0) while quanta beyond it vanish and the audit stays closed; a moving absorber-emitter never eats its own wake (40, 38, 36, 34, 32, 30); absorb validation rejects a scalar momentum field and an amount key; a fraction 1/4 absorbs one quantum of each 4-quantum ray and forwards 3; negative quanta pull an absorber with stock 3 by (-2, -1, 0, 0) and credit the emitter 16 with recoil (16, 0, 0); a ray field cannot be both absorbed and exchanged |
| `test_kerengonen.py` | A phase advances by the field's step on every link and wraps, a plain field leaves it alone, and rays merge only with equal phase; the cosine table for four steps is (256, 0, -256, 0), equal phases give coherence exactly one, opposite equal amounts exactly zero and a quarter turn one half; two lamps three links from a Node fire 2-quantum rays at each other and the sampled values along the line are 4, 0, 4, 0, 4 with four steps and 4, 2, 0 with eight, while the plain field reads 4 everywhere and the audit closes on 800 quanta; an absorber between the lamps takes 4 quanta before the opposite pair arrives and nothing after, takes 20 at the in-phase Node, and 20 at the dark Node when the second lamp is offset two steps; the runner records `kerengonen-ray-field-v1` and rejects one phase step, an advance equal to the steps, a missing advance, an emission phase beyond the steps, a phase without the key and the key without ray transport; the double-slit probe composes and closes; the bounded ticket rule advances and squares as specified and no absorber draws from it, the share rule takes 2 whole single quanta at a quarter turn where a half share truncates to nothing (closed on 800 quanta), and an unknown capture, the deleted lottery capture and a capture seed are rejected; a slit that re-emits the phase it absorbed makes a lamp's wave arrive at a Node three links on opposite to a second lamp's (reading 0), equal with that lamp offset four steps (4), and partial at a fixed re-emission phase (3), and a carried phase without an absorb rule is rejected; a ray with its own advance ignores the field's, rays of different advance do not merge, beams of momentum 16 and 32 at advance |p|/4 carry advances 4 and 8 with phases in ratio two after the same links, a negative advance and one without the key are rejected, and a slit re-emits the absorbed advance so readings are 2, 4, 0 for lamp offsets 0, 16, 48 on a 64-step field; a mirror sends a lamp's wave back along -x with the carried phase, holds 4 quanta and the reversed momentum, closes on 400 quanta, and the line reads 0, 2, 5, 7, 7, 5, 2, 0, 0, 2, 5 at advance 4 (period 8) and 6, 1, 1, 6 repeating at advance 8 (period 4); a mirror without every image heading, without a recoil field, on an unknown axis or without an absorb rule is rejected; a three-layer screen's first layer absorbs exactly what a one-layer screen does and the layers behind add to it, both worlds closed; a dissolving record of 10 quanta with after 3 and over 4 holds 10, 10, 10, 7, 4, 1, 0 and a moving one flies while it holds quanta and stops at x = 2 when empty, both closed; dissolution on a sourced emission, an emission without amount or dissolve, and over_ticks 0 are rejected; on the Euclidean metric the integer square root is exact at 0, 1, 2, 3, 4, 15, 16, 17 and a million, the paces of an axis, face and body diagonal are 2364/4096, 2364/2896 and equal, twelve ticks carry the first axis ray 6 links, the face diagonal 9 and the body diagonal 12, the world closes on 400 quanta and an unknown metric is rejected; a diagonal `xy` mirror returns the +x ray along +y with nothing back along -x, and a quarter-fraction mirror passes 3 of every 4 quanta and returns 1, closed; a directed emitter with `heading` fires every ray along -x and closes, and a heading outside the field's list or combined with a mirror is rejected |
| `test_redshift_sweep.py` | On a 16-row at emission 32 the twelve rays are absorbed, the quanta conserved, the field linear in age, the eye's clock equal to the tick count, the gaps 8, 9, 9, 9, 9, 10, 10, 10, 11, 11, 11, z = 0.2159, the duration ratio 1.2159, the hop-schedule slope between 0.025 and 0.035 and the last hops within a tick of the gaps; without emission the gaps are all 7 and z = 0; a row no longer than the train is rejected; the shapes' deceleration parameters are 1, 0, -1/2, -1/2 and 1/2; the fit recovers LambdaCDM exactly and the coasting shape's residual falls with redshift; the Pantheon table reader drops calibrators and z below 0.01; the wave's frequency is read from link 12 to the eye and compared with the gap ratio over that span, 1.0918: ratio 0.9178 against 0.9159 with phase per link (conserved phase differences, so by construction), 0.8164 against 0.8121 per interval, 1.0 without emission; the single source's frequency is read from link 1, ratio 0.645 against 0.6439; one source emitting twelve rays 24 ticks apart on its own clock across 15 links gives gaps 36, 38, 36, 39, 37, 38, 37, 39, 34, 39, 37, z = 0.553, duration ratio 1.553 and a ray-by-ray k_o / k_e of 1.5051, within 1.2 ticks per gap of 1 + z |
| `test_euclidean_pace.py` | One lamp on the 26 neighbor headings after twelve ticks reaches 12 links in every heading on the links metric (Euclidean radii 12, 8.49, 6.93, spread 1.732) and 6, 9 and 12 links on the Euclidean metric (radii 6, 6.4, 6.93, spread below 1.2); two lamps four links apart behind a screen twelve links away read their darkest Nodes at x = -1 and 1 on the links metric with a flat line beyond, and at x = -5 and 5 on the Euclidean metric where the Euclidean path difference is a half turn, with the center more than four times the dark reading; every world closed; the runner records `euclidean-ray-pace-v1` beside `isotropic-ray-field-v1` |
| `test_particle_interactions.py` | With six axis rays per body through one shared field with `self_exclusion` (a lone mover keeps momentum 16 while moving, and without exclusion it pushes itself): like charges approaching head-on never share a Node and leave with reversed, equal-and-opposite momenta; opposite charges at rest move toward each other; neutral bodies emit nothing and cross unchanged; a light body beside a heavy one takes the same kick per hit, moves farther, and the heavy one's kicks lag by retardation; a bound pair converts after its timer into a proton leaving at one hop per tick and a triple-mass core recoiling at a third, with mass 4 and zero momentum conserved |
| `test_spatial_coupling_budget.py` | Signed reversal never refunds budget; unaffordable turns/exchanges leave both owners and old fractions unchanged; large work-register requests are rejected before payload packing; concurrent delayed emission refresh does not overwrite frozen coupling allowance |

The runner must distinguish actual physical conservation from balanced loss
accounting. It checks tracked combined quantities and every spatial owner,
including a nonconserved computation field. The public examples
`finite_fields.json` and `three_mass_finite.json` require no visualization.

An independent periodic 3x3x3 rotation check starts a carrier at `(2,1,0)`.
With two affordable positive Z turns it becomes `(-1,2,0)`, then `(-2,-1,0)`;
its squared norm remains 5. Sources total `(5,-3,0)`, signed reaction totals
`(4,2,0)`, and all dynamic field stock is gone at tick 3 with signed loss
`(9,-1,0)`. Further prescribed turns cannot spend an exhausted allowance.

## Active generic disturbance contracts

`test_interaction_spatial_integration.py` checks atomic pair assignments after
a nonzero spatial response, their frozen delayed commit while finite emission
continues, and nested matrix/dot operations using delivered spatial flux.
Pair invariants preserve the post-response sum; opposite field reactions and
independently committed field emissions retain their existing owners.
An invalid atomic proposal commits neither the rotated carriers nor their recoil,
while an earlier independently committed emission and allowance debit remain.

The primary Simulation follows [DISTURBANCES.md](DISTURBANCES.md). Schema and
engine tests must use independent examples for the contracts below. These are
acceptance requirements, not a statement that a particular source tree passed.

| Input or boundary | Required outcome |
| --- | --- |
| Complete JSON initialization; renamed field/type labels | Equivalent declared behavior with no physical-name branches |
| `test_generic_identity.py`: rename labels/units, reorder declarations, or both | Exact snapshots, ordered events, costs, timing and accounting over six ticks in six active scenarios; real commits, delays, reactions, decay and exits prevent vacuous equality |
| Workspace drafts and generated names | `__proto__`, `constructor` and `toString` survive browser draft storage; adding fields/types skips existing names and leaves existing definitions intact |
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
`test_spatial_engine.py` checks a 216-unit pulse at successive Manhattan radii,
continuous stationary/moving injection, fixed transit with carrier delay,
baseline behavior, signed fractional emission and headless combined accounting.
Coarrival with a source's own field does not by itself identify its contribution.
Straight-path and turning behavior are treated separately by the response tests.

`test_emission_residuals.py` checks that independent emitting records retain
their fractions and that later emission metadata survives a pending carrier
proposal without changing its physical payload. `test_exchange_residuals.py`
checks opt-in left-owned fractional exchange across new recipients, signs and
ordered concurrent matches; pair-owned defaults retain their previous contract.

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
deleted with their engines on 2026-09-17 (issue #164, bucket A); the dated
records in `VALIDATION.md` keep their original scope.

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

## Local configuration workspace

`test_workspace.py` drives a real loopback HTTP server and isolated runner children.
Edited tick counts, model labels and initial amounts must reach saved metadata;
two configurations must use distinct outputs and match direct CLI input, events,
state and metadata byte for byte without changing source files. Invalid inputs
and duplicate keys, including nested editor fragments, fail before execution.
Tests cover cross-origin/token/Host rejection, restricted artifact paths, active
job conflicts, explicit cancellation, shutdown cleanup and physical failure data.
The browser workflow additionally checks forms, JSON editing, draft persistence,
selection, validation after editing, imports/exports and optional recorded results.
Inspect the actual UI; a passing HTTP test is not proof of correct controls.
For phone layout changes, inspect narrow portrait and landscape viewports, all
configuration tabs, numeric and JSON editing, shortcuts and completed results.
Check document overflow, readable input text and touch target size. Record the
actual browser and dimensions; viewport emulation does not verify native iOS
keyboard, Safari or safe-area behavior on a physical device.

`test_recorded_movie.py` checks that the approaching pair meets at the declared
node and passes without an invented collision, that parallel speeds differ and
the pulse spreads while declared inventory remains conserved. Its explicitly
marked visualization tests check exact sampled/final payloads, headless event
parity, escaped names and partial failures. Browser checks must cover movie
play/pause/restart/final hold, scrubbing, projection/speed, folded settings and
renaming references without resetting an already loaded movie during polling.

## Atomic generic interaction acceptance

`tests/test_atomic_interactions.py` checks the configured 15-cube unequal-mass
collision: m=(2,3), p=(8,-3)->(-4,9), independent rational kinetic energy 35/2,
constant total momentum 5, causal arrivals, no repeated bounce while co-resident,
and final opposite departures. Further small cases cover simultaneous multi-field
conversion/rotation, weighted inventory, rejection before commit, invalid schema,
pair totals larger than individual registers, and renamed fields in a larger
world. These are classical-candidate and generic-contract checks, not proof of
an emergent gravitational or universal energy law.

## Standalone generic vector lab

[The lab contract suite](../tools/generic_vector_lab/test_lab.py) checks exact
rational vectors, energy/momentum/charge accounting, reaction rollback, binding,
recoil and local quantum examples. [Node-rule tests](../tools/generic_vector_lab/test_node_rules.py)
check six-way A/A/B/B/C/C composition, forbidden mixtures, configurable limits
including a 17-input case, deterministic matching and property predicates.
The six-node example has E=3, p=(0,0,0), q=0 before and after its configured
cyclic vector map. These are mechanism checks, not real-particle validation.
[The repository adapter](../tests/test_generic_vector_lab.py) runs all 52 lab
cases; the check selector maps every lab source/configuration change to it.


## Causal event ledger

`test_event_links.py` checks immutable event spacetime through a split/join,
direct event lookup without separate predecessor lists, current-head updates,
foreign and forged handle rejection, failed-append atomicity, fixed capacity,
and that a dependency edge is not a physical link while a capacity failure
leaves the identity counter unchanged. The quantum event network, the origin
cells and their suites were deleted on 2026-09-17; the ledger stays until
issue #164 bucket B.4.


## Local field impulse and node ownership

`tests/test_local_lorentz_field.py` covers a four-link causal pulse, independent
electric/magnetic impulse directions, neutral response, equal/opposite local
momentum, delayed commit, field autonomy, renaming and invalid arithmetic.
`tests/test_node_state_contract.py` verifies formula-free evolving state and
rejects injected ASTs, laws, callbacks and formula strings. See
[the scoped candidate contract](LOCAL_LORENTZ_FIELD.md).

## Executable entity and conversion expectations

`tests/test_entity_compiler.py` validates all 46 profiles, active representative
carrier/vector and scalar transport, generic name selection, capacity rejection,
conflicting declarations and malformed profiles. Version 2 requires explicit
separate profiles; version 1 retains embedded-profile compatibility. Metadata
changes must not change compiled laws. Profile compilation is distinct
from physical-law acceptance; do not multiply identical runs across labels.
`tests/test_local_conversions.py` checks two-to-two ownership, ignored output
defaults, causal/delayed commits and rejected invalid balances or carried progress.
Existing shared engine tests remain necessary consumers of the changed schema.

`tests/test_family_conversion.py` covers the
[energy-dependent family-conversion candidates](../examples/family-conversion/README.md)
with expectations written before the first run. Annihilation of an on-shell
electron (1825, +1752) and positron (1825, -1752) meeting at tick 6 gives two
1825 keV photons along +/-X that escape at tick 15; asymmetric inputs
(1825, +1752) + (511, 0) give photons (2044, +2044) and (292, -292), and the odd
case (1825, +1752) + (512, 0) gives (2044, +2044) and (293, -292) with the
indivisible keV owned by photon b; transverse momenta block the rule. Pair
production converts 511 + 511 into a resting pair and rejects 511 + 510; 49 + 5329
(product exactly 511^2) gives an on-shell pair (2689, -2640) each, 48 + 5329 does
not convert although its total exceeds 1022; the 500 + 500 control crosses and
escapes at tick 15 with only photon records ever present. Compton with a 511 keV
photon on a resting electron gives 255 keV along +Y and a 767 keV electron with
momentum (511, -255, 0); the fraction follows the integer formula at 100, 511,
1022, 10,000,000 and `MAX_VALUE - 1` keV, the electron owns the remainder, a
moving electron crossing a photon strands nothing at any Node, and a stream of
three photons past a resting electron scatters once and forwards the rest.
Bound cases: annihilation and pair production at exactly `MAX_VALUE` per record,
`MAX_VALUE + 1` rejected at initialization, and the Compton proposal at a
`MAX_VALUE` photon rejected with an unchanged snapshot. Sixteen pairs on a
48-cubed board convert at tick 21 with energies up to 10 GeV and exact totals.
The 2 -> 3 three-photon rule turns (1825, +1752) + (511, 0) into photons
(1752, +X), (292, +Y) and (292, -Y) on three distinct Ports at tick 6, gives the
transverse photon the odd keV for a 512 keV positron, and does not fire at zero
net momentum; its capacity control (two slots) and Port control (the collinear variant
sending two products on +X) fail before commit with unchanged snapshots,
while a spectator photon leaving on a product's Port completes the cycle. The 4 -> 4 joint rule pools four rays arriving through four Ports at tick 6,
(1825, +1752), (1825, -1752), (300, +Y), (300, -Y), into photons 1062 along
+/-X and 1063 along +/-Y; an odd pooled energy gives the +X photon the unit;
unequal or collinear photons leave the rule silent; three of four rays let the
declared 2 -> 2 annihilation act instead; the collinear variant with two products
per Port fails the cycle before commit with four unchanged residents while a
catalog muon spectator leaving on -X beside a product keeps ordinary transport; sixteen
quadruples on a 48-cubed board convert at tick 21 into 64 photons.
Generic arity cases on the stock probe world: 1 -> 6 sends one record
per Port, 6 -> 1 consumes five slots, seven or zero roles or outputs are
rejected, two products on one Port, missing free slots, a broken readout
invariant and a conserved-field mismatch each leave every owner unchanged with
no pending plan, property-selected inputs convert, and a slow conversion locks
the free slots its extra outputs need against arrivals, and the same conversion
under `node_execution` with `k` 2 fires at `ready_tick` 2 while a missing `k`
is rejected. `bindings.json` must
equal the builder's catalog derivation: rest energy 511 keV encoded to the
nearest keV/c2, charges -3/+3/0 in thirds, and each rule's interaction family
and representative channel matching its participants and outputs.
Totals plus escaped quantity equal the initial totals at every tick and the local
audit passes in every run; these are accounting results for supplied laws.


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

`test_reference_examples.py` verifies that collision checks load the canonical
workspace JSON and that all five existing reference worlds keep their independent numeric
assertions without producing HTML/GIF. The wrapper and its dynamically selected
inputs explicitly select this regression through `tools/check.py`; every changed
path selects the inexpensive repository language and canonical-copy guards.

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

## Parallel Node execution

`test_parallel_node_execution.py` compares serial and two-worker execution after
every tick for carried disturbances, finite spatial fields and the shared delayed
field/carrier Node cycle. Snapshots, events, model costs, conserved totals, sources,
dissipation and escape must remain exactly equal. Separate checks require bounded
worker counts, saved host-execution
metadata and actual disturbance/spatial task submission. The tests do not claim a
speedup for small worlds; performance depends
on local rule cost, active Node count and interpreter serialization overhead.

Inline observer input is covered by `tests/test_local_observer.py`: normal schema
validation, rejection before output creation, ambiguous placement rejection, exact
saved initialization and unchanged physical results with recording enabled.


Parallel integration also compares indexed field-only and joint Node profiles,
and work-driven emissions, against serial snapshots, committed-cost readouts,
modeled work and complete event order. Worker planning keeps the same local
proposal validation and field/carrier commit boundaries.

## Localizing-residue integration boundaries

Localizing-residue integration also covers a signed (5, -3, 0) pulse under both
field clocks, independent localize/dissipate fields, and deposit overflow that
preserves all receiver state and leaves the original packet on its Link. These
are component-inventory and atomicity checks, not physical energy proofs.

## Reference unit authoring

`tests/test_reference_units.py` independently checks SI dimensions and exact defining
constants, Scalar/Vector shape and sign, known catalog mass/charge/magnetic inputs,
explicit rounding budgets, runtime payload bounds and malformed dependency graphs.
Its periodic 40-tick probe preserves encoded reference mass inventory and all three
momentum registers under unchanged two-tick Link transport. It is not a proof of
mass-dependent dynamics. `tests/test_entity_catalog.py` pins PDG 2026 masses and
widths, CODATA 2022 electron magnetic moment, signed antiparticle references and
the distinction between omitted and inapplicable lifetimes. See
[reference units](REFERENCE_UNITS.md) for calibration and evidence boundaries.

### Ray integration and local Focus

`test_ray_merge_contracts.py` independently covers funded inventory during a
load wait, waiting-time absorption, retained-owner capacity and shape, full ray
packet validation before residents merge, exact 100005/3 share capture, unfundable
negative threshold capture, directed self-exclusion and maximum pace inputs.
`test_local_focus.py` checks per-tick inventory, snapshots, ordered events and
modeled cost against the unchanged ordinary scheduler, including six-Port
revisits, pending delays, failure timing, parallel execution and explicit fallback.
Host visit reduction is distinct from physical O(1) local work.


### Exact transition reuse and active transport

`test_plan_reuse.py` checks all carrier and spatial planning arguments, including
local phases, resident rays, computation cost and time; hash collisions; bounded
LRU eviction; retry after failure; independent configurations; and default reuse
of repeated moving patterns in serial and parallel execution. Each tick retains
identical inventory, snapshots, ordered events, operation cost and local clocks.
`test_active_ports.py` checks stable
bank-creation order after reactivation, release during iteration, preserved empty
mapping entries and continued stepping without scans of inactive bank history.
The existing Focus, field, delay, boundary, parallel and formula-free state tests
remain consumers of this host-only optimization. Timing is measured outside CI
assertions with identical inputs; no speed threshold replaces physical equality.


### Boundary validation once per crossing and readout reuse

`test_node_runtime.py` rejects a malformed delivered record (unknown type,
zero code, mutable payload) and a record policy's unvalidated output at the
Node boundary without changing owners, and counts boundary validations by
object identity: one per delivered record at the Node and through transport,
plus one for a merged record, while a malformed link packet leaves its link
and target untouched. `test_payload_validation.py` tables signed, unsigned,
negative-in-unsigned, largest, zero, above-bound, negative, float and bool
codes and wrong component counts for field and spatial-state validation
against the original decoding reference, with identical messages in the same
order, and confirms that validation decodes no component.
`test_node_conservation.py` also checks that repeated readouts of equal
payloads reuse host evaluations with identical results, that changed values,
bundles or quantities miss the bounded cache while bookkeeping outside the
values hits it, and that failed readouts are requested again and never retained.

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
instrument/contact fixtures with the integration layer. Full PASS/RETURN and
output-clock composition remain blocked by the contract's owner/acceptance table.
