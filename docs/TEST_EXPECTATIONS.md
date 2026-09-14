# Test inputs and expected results

## Spatial momentum and position output

`test_spatial_momentum.py` verifies the
[finite observable](../examples/quantum/position_moment_response.md) against
independent phase and mixed-state expectations. Equal spatial probabilities
can have mean +2, -2 or zero; real coherent and incoherent uniform states have
variance 0 and 2. Endpoint superpositions distinguish second-neighbor coherence.
Vacuum has unavailable particle moments, partial occupation is explicit, and
multiple excitations or nonlocal/duplicate edges are rejected.

`test_position_moment_response.py` runs the primary native middle-capture input,
six endpoint orientations, absent reservoir, delayed computation and longer
Links. Local re-encoding gives variance 1 or 2 from the operator row. Wave
diagnostics leave native events and model cost exactly unchanged. The actual
combined second moment changes 10 -> 11 -> 10 during endpoint propagation,
and remains 11 after middle capture. This is an exposed closure gap, not a
conserved quantum energy claim. Subsequent ordinary exchange and escape balance;
invalid first/second moment proposals reject before conversion.
Projective controls separate the ensemble drift from selected conditional change.
The target's later direction still comes from the supplied reservoir.

## Local moment response after capture

`test_local_moment_exchange.py` runs the
[candidate](../examples/quantum/local_moment_exchange.md) in all six directions,
with no reservoir, longer Links and computation delay. A unit-mass target with
mean 0 and variance 1 exchanges moments with a unit-mass reservoir with mean 3
and variance 0. Total mean momentum 3 and doubled expected kinetic energy 10
include ordinary, quantum-inventory and escaped owners. The target follows the
selected axis at nominal c/100; the zero-mean recoil remains uncertain. Test
mass/validity rejection, renamed fields/types and nonlinear energy rejection
despite an unchanged mean sum. Separate exact quantum-owner controls preserve
all sixteen basis momentum/energy cases and coherent reversal.

`test_record_operations.py` verifies that reserved empty slots cannot receive
new records: select the first unlocked spare, or reject the entire proposal
without mutation when capacity is insufficient. The delayed quantum capture
regression in `test_localized_quantum_contact.py` receives a messenger into
spare slot 2 at tick 4 and commits capture at tick 11 with both owners intact.

## Quantum-to-classical investigation

`test_quantum_classical_experiment.py` runs the bounded
[investigation](../examples/quantum/quantum_classical_check.md). Ten native controls
must give exact visibility `(9/25)^n` at fixed contact tick 8; zero coupling and
phase reversal cover both certain outputs. Explicit coherent environment controls
must restore interference after retained interactions are inverted. The existing
five-cycle Markov comparison remains exact. Three spatial outcome controls
preserve inventory and field accounting while recording configured hold and
unknown momentum; direct moving capture remains a rejected composition. A pass
must retain the report's `not_established` trajectory conclusion. No statistical
or Newtonian emergence claim follows from this acceptance test.

## Recurrent quantum contacts

`test_recurrent_quantum_contact.py` owns the
[recurrent contract](RECURRENT_QUANTUM_CONTACT.md). Exhaustive source tickets for
matrices 3I and 4X yield 9 localized retentions and 16 new waves out of 25.
Capture matrices 13P0, 3|0><1|, 4P1 and 12P1 yield 9 localizations, 16 new waves
and 144 continuations out of 169 occupied-mode tickets; vacuum is a certain null.
Check no extra draw for a certain outcome, one scalar/vector inventory owner,
renamed entities/fields, equal-inventory alternate outputs, finite original
source allowances and capacity rejection before RNG. The checked-in 48-tick
example has fresh-wave events at ticks 3, 9 and 21, localization at 24, injection
-36 and eventual zero field stock under explicit dissipation.

`test_recurrent_contact_locality.py` compares reversed-address source prefixes:
a remote event at tick 3 cannot select which ordinary local bank clears before
the notice can arrive at tick 6. Source amplitude, field and local cost 45 agree.
It also rejects preparation into local vacuum when another mode is occupied and
checks same-tick result replay after absorption without origin resurrection.
Retain all affected localized/causal contact, origin, state and field regressions.

The Kerengonen integration regressions in `test_ray_integration_guards.py` cover
ordinary runner momentum accounting through absorption and escape, frozen phase
tables after host-cache eviction, independent trigonometric reference entries,
distinguishable external phases and advances under self-exclusion, frozen
departure metadata after emitter changes, largest-share carried advance with
explicit-zero and field-fallback cases, per-field ticket seeds,
whole negative lottery rays with insufficient/exact stock, delayed-owner
rejection before stale commits, immutable carrier routing/unrelated fields,
expired emission metadata and conflicting momentum or unsupported response
bindings. `test_kerengonen.py` retains the actual recoil configuration through
the ordinary runner identity test. Coherence work is quadratic in the configured
local phase/ray count; it is bounded relative to world size for fixed capacities,
not a claim of linear host work.

## Active contract coverage and shared execution

`test_active_node_contracts.py` exercises receipt and completion at all six Ports
for the active carrier Node, spatial Node and source-envelope Node. For the same
local payload and fixed capacity it varies world extent, unrelated resident/event
counts (0, 8, 128) and elapsed model ticks. The measured production-path line counts,
modeled carrier cost, local event count and recursively retained payload size must
stay equal. Host world indexes are made unreadable during each local transition.
Expected outputs remain explicit: one carrier crosses one Link, spatial stock 64
is owned locally or in outgoing packets, and the source mixer yields amplitude 3/5.
These are bounded-work regressions plus state/locality guards, not a timing-based
proof for arbitrary callbacks, whole-world scheduling or quantum evaluation.

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
| 34 full catalog-contact worlds | All 34 preparation bindings checked through parsed source records and capture templates; 11 dynamic representatives cover every charge value, passive spin value, zero/unknown/positive mass and maximum mass, plus the original simultaneous-domain and rejection tests |
| Contact renaming checked only charge/source totals | Semantic rename, declaration reorder and combined variants compare complete public snapshots, events, balances and quantum outcomes at each tick; real capture and nonzero emission are required |

The representative regime-coverage test must fail if a new catalog property value
is not represented. Data preparation remains checked for every entry. Catalog
mass and spin are passive inventory/properties in this candidate; these tests do
not establish species dynamics. Distinct signed, overflow, denominator, boundary,
null/capture and correlated-state cases are not removed. The exact 25-ticket
fixtures remain exhaustive.

The remote-detector causal comparison also requires equal local source-cost and
delay prefixes before delivery, with observed source work and an actual later
capture/terminal effect. Globally conditioned quantum state remains distinct from
the retarded ordinary source envelope after a measurement.

`test_check_scope.py` requires empty selections to avoid source/dependency scans
while honoring explicit `--tests`. Prior source reads use two Git processes and
preserve exact blobs, including empty files and deleted providers. Old and current
dependency selections, dynamic resource consumers and failure evidence remain
part of the gate; batching does not authorize dropping related tests.

## Recurrent quantum contacts

`test_recurrent_quantum_contact.py` owns the
[recurrent contract](RECURRENT_QUANTUM_CONTACT.md). Exhaustive source tickets for
matrices 3I and 4X yield 9 localized retentions and 16 new waves out of 25.
Capture matrices 13P0, 3|0><1|, 4P1 and 12P1 yield 9 localizations, 16 new waves
and 144 continuations out of 169 occupied-mode tickets; vacuum is a certain null.
Check no extra draw for a certain outcome, one scalar/vector inventory owner,
renamed entities/fields, equal-inventory alternate outputs, finite original
source allowances and capacity rejection before RNG. The checked-in 48-tick
example has fresh-wave events at ticks 3, 9 and 21, localization at 24, injection
-36 and eventual zero field stock under explicit dissipation.

`test_recurrent_contact_locality.py` compares reversed-address source prefixes:
a remote event at tick 3 cannot select which ordinary local bank clears before
the notice can arrive at tick 6. Source amplitude, field and local cost 45 agree.
It also rejects preparation into local vacuum when another mode is occupied and
checks same-tick result replay after absorption without origin resurrection.
Retain all affected localized/causal contact, origin, state and field regressions.


## Causal quantum sources

The [causal source contract](CAUSAL_QUANTUM_SOURCES.md) requires exact 3:4 mixing
and inverse interference, signed full emission `-25` producing requests `-9`
and `-16`, rational complex vacuum normalization, changing-denominator residue,
finite allowance exhaustion and explicit overflow rejection. These arithmetic
cases belong to `test_source_envelope.py`.

`test_causal_contact_fields.py` owns integration acceptance: frozen neighbor
inputs, tariff-derived local delays, every periodic direction, one committed
localized output, a local null
without remote renormalization, and terminal packets that end remote emission
only after causal arrival and local delay. Compare ordinary source, field and
cost prefixes with and without a distant detector. Include a coupled third
resident, pending emissions at capture, charged duplicate notices, termination
before amplitude arrival, no resurrection, finite per-mode allowances and
formula-free transitive NodeState. Preserve the older contact profile's tests.
These expectations distinguish conserved carrier inventory from retarded source
weights and field injection; they are not a claim of full field/matter energy
conservation. Completed results belong in [validation evidence](VALIDATION.md).

`test_causal_source_commit.py` checks that generation, identity, arrival-time
and accounting failures occur before sampling or publishing a quantum result.
Source observers must see both deposited stock and the consumed finite allowance.
A null during an already started gate retains both frozen operands: mixing
`(3/5, 4/5)` yields `(-7/25, 24/25)`, and the inverse restores the original pair.
Changing only one frozen operand is forbidden because it can increase the norm.

## Localized quantum contacts

`test_causal_interference.py` runs the
[two-arm interference harness](../examples/quantum/causal_interference.md) in
the fast gate: exact output decision weights `[337, 288]`, `[49, 576]` and
`[337, 288]` for `phi = pi/2, pi, 3pi/2` and no uncertain decision at `phi = 0`;
balanced Hadamard capture probabilities 0, 1/2, 1 and 1/2 with arm emission
(12, 12); mean source emission after recombination within 1/6 unit of `25 |a_S|^2`;
one localized capture at D at tick 7 when the ticket selects it; an arm
detector giving `[9, 16]` for every phase with no later uncertain output
decision; and a retarded source emission of 9 of 25 after an arm null. With
`null_notices` the same arm null gives 25 of 25 from tick 2, 9 and 16 at the
next gate and final scales 625/81; the output null gives 25 from tick 9 and
scales 625/337. With a `field_phase` on the M arm, coil fields 0, 200, 400 and
800 give capture probabilities 0, 0, `576/3125` and `9216/15625`, and a coil on
the far side of the source gives 0.

`test_null_notices.py` owns the opt-in
[null notice extension](CAUSAL_QUANTUM_SOURCES.md#opt-in-causal-null-notices):
factor 25/9 from a 16/25 null and `None` for vacuum or certain occupation;
scaled weight clipped at one; notice packets require a factor of at least one
and an event identity; a null without the option sends nothing and keeps scale
one; a null with it scales itself and fills one notice slot per Port; a received
notice waits the control delay, applies, forwards away from its arrival Port
and is ignored when repeated or at a retired Node; the applied bank keeps six
identities; the option is rejected without the causal model; in the two-arm
world the source emits 25 from tick 2 after an arm null at tick 1, the next
gate emits 9 and 16, all scales reach 625/81 after the second null, and an
output null at tick 7 reaches the source at tick 9 with scale 625/337.
The default profile without the option is unchanged.

`test_field_phase.py` owns the opt-in
[field-dependent phase](CAUSAL_QUANTUM_SOURCES.md#opt-in-field-dependent-phase):
a nine-entry table for `max_exponent` 4 with identity at zero, `(3, 4)` at one,
`(3, -4)` at minus one and `(-7, 24)` over `25` at two; exponent 0/1/4 for
values 24/25/100 and rejection at 125; parser rejections for unequal norms,
zero divisor, a limit above twelve, a non-spatial field, a bad component, the
localized model, two registers and a matrix given together; coil fields 0, 200,
400 and 800 selecting exponents 0, 0, 1 and 2 with output weights
`[12745, 2880]` and `[160225, 230400]` at tick 7; a coil beside the far side of
the source selecting exponent 0; source port weight `2549/3125` after the
shifted recombination; rejection of `start_sources` without field values; the
headless report listing the retained choice; and zero field phases in the
unchanged default example.

Complex-coefficient regressions require unchanged interference under a common
phase for exponents -3 through 3 and exact reversal for positive/negative powers
in either order. A native coil of -400 compares `(5, 3+4i)` with `(5i, -4+3i)`:
both must select -1, capture with probability `576/3125` at tick 7, retain source
envelope weight `2549/3125` after twelve ticks and balance ordinary field stock.

`test_many_contacts.py` validates the thirty-mode periodic experiment, two-Link
target separation and its fixed-seed one-shot result: three A captures at event
tick 3, two B captures at 5 and one C capture at 7. It checks charge/mass ownership,
finite dissipative field accounting and unchanged headless output. The actual
200-trial evidence belongs to the
[experiment report](../examples/quantum/many_contacts.md).

`test_localized_quantum_contact.py` owns the
[contact hybrid expectations](LOCALIZED_QUANTUM_CONTACT.md#numerical-acceptance):
actual source birth, delayed single ownership, finite classical emission and Link
fronts, 9/25 versus 16/25 mixing and inverse interference, exhaustive capture
tickets, unchanged unconditional receiver statistics, constant detector cost,
six periodic directions, positive transit times and unused local capacity.
It also reproduces a third-resident field-reaction conservation defect, checks
rejection before sampling, semantic-owner guards, concurrent snapshot publication,
active generic renaming and headless primary-runner output. The scope is finite
configured absorption and component accounting, not complete electromagnetic
energy/momentum conservation or quantum emergence.

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
exact through commit. Nonlinear guards and event-capacity failures stop before
the affected transaction mutates stock. Real scalar/vector costs, empty input
intervals, moving sources, finite decay, formula-free state, graph controls
and passive conservation are covered. These are timing and inventory claims.

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
and quantum profiles are checked independently, including unselected rows;
subsets and single representations remain valid. Tests forbid world construction
and implicit filesystem access, preserve supplied objects and verify CLI batch
exit/report behavior and rejection before runner artifacts are created. Existing
UI and runner tests retain accepted output and physical execution contracts.
`test_event_program_validation.py` checks exact and insufficient startup event
capacity for distinct/colocated classical seeds and quantum registers, including
mixed worlds. Future exhaustion remains a separate runtime test.

`test_spatial_causal_events.py` covers two-tick field transport and periodic return,
two-parent cancellation and complete decay, frozen samples versus later field
arrivals, emission allowances, joint packet creation/amendment/cancellation,
exact and one-short transaction capacities, runner failure evidence, and on/off
equality of physical state, bookkeeping, costs and timing. The shipped signed
encounter reaches zero at tick 6 while retaining both histories and 20 events.
Stepping must not traverse ancestry or instantiate a quantum resolver. Existing
native quantum/runtime tests retain their own inverse, checkpoint and cost checks.
Typed initialization with the separate conservation audit and a native event
program must fail before event-space or resolver allocation, through parsing,
runtime construction and the public simulation entry point.


## Local observer

The [observer contract](LOCAL_OBSERVER.md) specifies causal receipt withholding,
two-tick periodic transit, signed post-decay readings, zero versus absence,
unchanged physical states/costs, exact prefixes, clock independence from global
timestamps and archive exhaustion. `tests/test_local_observer.py` checks these
paths. `tests/test_observer_playback.py` checks safe labels, backward seeking,
paused-clock samples and the explicit world-audit switch. These are observation
contracts, not human vision or Maxwell acceptance tests.


## Local record operations

`test_record_operations.py` checks generic vector merging with independent
expected components, separation by type/channel/pending lock and whole-record
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


## Quantum registers, channels and catalog profiles

See [the explicit v2 contract](QUANTUM_ENTITIES.md). New tests cover channel
completeness, grouped outcomes without hidden sampling, 72 dense rational state
comparisons, phase interference, CHSH 14/5 and local marginals, classical Markov
probabilities, multilevel/colocated registers, rejection boundaries, all 46
profiles, and native priced control paths. Preserve earlier uncertainty, quantum,
classical, import and locality regressions. Quantum-mode definitions alone are
not evidence of full species dynamics.


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
| `test_runner_retention.py` | Both runners lease fresh or empty output through writing, reject nonempty output, preserve original initialization, and expire finished or failed artifacts; cleanup during a simulation step cannot remove its output |
| `test_workspace_retention.py` | Finished/failed/cancelled jobs and exports expire, active and orphaned children protect companion files, log-close failures keep their lease, stale links return 404, linked output paths cause no writes or process launch |
| `test_check_scope.py` | Explicit non-import edges retain identity-example and runpy consumers; the exact scope report expires while unrelated files survive; dry-run creates no output |

Ordinary test execution leases its JUnit report and generated detector result.
Explicit visual sessions lease a unique output directory and summary through
render completion. Neither test collection nor cleanup enables rendering.

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
| `test_ray_field.py` | DDA rays return to their heading after one period with bounded accumulators; emission shares 5 over 2 rays as 3 and 2 and cycles the cursor; a 64-unit ray source keeps totals at 64 per tick and 64 on every Manhattan shell; a receiver gains 15 momentum from three ticks of 5-unit ray flux; retention 1/2 deposits 4, 2, 1, 1 along a ray or dissipates 8; a third ray phase at a two-slot Node fails explicitly; open boundaries count escaped rays; invalid keys, zero headings, vector fields, octant seeds and the shared clock are rejected; the runner records `isotropic-ray-field-v1`; a ray passes a Node whose receiver reacts to it and reaches the Nodes beyond |
| `test_gravity_probe.py` | Held bodies beside an axis-ray source gain momentum toward it, proportional to mass within the carried integer remainder, with combined carrier plus local-field momentum conserved; a moving body starting five links out only moves inward with growing inward momentum, turns between five and seven links past the source with zero momentum, and comes back through it: a bound oscillation with combined momentum still zero; signed quanta pull held bodies toward the source and each pays exactly the momentum it gains from its stock, the far body takes its share of what the near one left, the source is credited 65,536 per tick with zero recoil and the quanta close; a body with stock 50 stops at momentum -50 with the event audit passed |
| `test_energy_audit.py` | Funded emission along (1,0,0) and (0,2,0) debits the emitter by 2 per tick and recoils by (-1,-2,0) per tick with the audit closed; a stock of 5 emits 2, 2, 1, 0; `source: true` is still rejected and `recoil_field` needs funding; escaped quanta are measured escape; an absorber banks five quanta with momentum (5,0,0) while quanta beyond it vanish and the audit stays closed; a moving absorber-emitter never eats its own wake (40, 38, 36, 34, 32, 30); absorb validation rejects a scalar momentum field and an amount key; a fraction 1/4 absorbs one quantum of each 4-quantum ray and forwards 3; negative quanta pull an absorber with stock 3 by (-2, -1, 0, 0) and credit the emitter 16 with recoil (16, 0, 0); a ray field cannot be both absorbed and exchanged |
| `test_kerengonen.py` | A phase advances by the field's step on every link and wraps, a plain field leaves it alone, and rays merge only with equal phase; the cosine table for four steps is (256, 0, -256, 0), equal phases give coherence exactly one, opposite equal amounts exactly zero and a quarter turn one half; two lamps three links from a Node fire 2-quantum rays at each other and the sampled values along the line are 4, 0, 4, 0, 4 with four steps and 4, 2, 0 with eight, while the plain field reads 4 everywhere and the audit closes on 800 quanta; an absorber between the lamps takes 4 quanta before the opposite pair arrives and nothing after, takes 20 at the in-phase Node, and 20 at the dark Node when the second lamp is offset two steps; the runner records `kerengonen-ray-field-v1` and rejects one phase step, an advance equal to the steps, a missing advance, an emission phase beyond the steps, a phase without the key and the key without ray transport; the double-slit probe composes and closes; the lottery capture takes 18 in-phase quanta and 2 before the dark pair meets like the share rule, takes between 2 and 16 whole single quanta at a quarter turn where the share rule truncates to 2, and rejects an unknown capture, a seed without the lottery and a seed at the ticket modulus; a slit that re-emits the phase it absorbed makes a lamp's wave arrive at a Node three links on opposite to a second lamp's (reading 0), equal with that lamp offset four steps (4), and partial at a fixed re-emission phase (3), and a carried phase without an absorb rule is rejected; a ray with its own advance ignores the field's, rays of different advance do not merge, beams of momentum 16 and 32 at advance |p|/4 carry advances 4 and 8 with phases in ratio two after the same links, a negative advance and one without the key are rejected, and a slit re-emits the absorbed advance so readings are 2, 4, 0 for lamp offsets 0, 16, 48 on a 64-step field |
| `test_quantum_classical.py` | A one-excitation walk with the position record discarded after every step equals the classical Markov chain exactly, with variance `t - 3/4`, while the coherent walk is wider and not the classical bell at step 6; single quanta on the ray field click as 0 or 1 at a detector and every emitted quantum is a record, in flight or escaped; repeated capture attempts land only on pass ticks 3 and 7 with charge and mass exact |
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

## Causal-stream candidate

`test_causal_stream.py` checks exact conservative six-port branching; rejection
of a negative old population even when a positive source would mask it; explicit
rejection of scalar seeding without mutation; isolated axis and diagonal momenta
with zero impulse residues at every tick; a Manhattan-distance-nine source pair
with zero response through tick eight and opposite (2,0,1) impulses at tick nine;
and an offset moving pair with opposite transverse responses at tick twenty-six.
The free-space cases do not reach periodic return. These are candidate acceptance
checks, not a claim of isotropic propagation or an established force law.

Shared calculations live in generic components. The model selects weights,
sources, response and activity policies and maps results to fixed records.
Scenarios provide initial conditions; the engine manages time, neighbors and
occupancy; measurements read the result.

## Tests by responsibility

| Test file | Responsibility | Expected outcome |
| --- | --- | --- |
| `test_integer_contract.py` | Integer arithmetic and bounds | Exact quotient and remainder for either sign; reject overflow before use |
| `test_lattice.py` | Periodic geometry | Same six-neighbor ordering for reads and moves, including boundaries |
| `test_scalar_field.py` | Generic field | Known numerical results for weights, signed values and remainders |
| `test_field_policies.py` | Source, range and activity | Derive source from count; test clipping and activity separately |
| `test_turning.py` | Generic vector response | Shared impulse arithmetic for each direction policy; opposite field impulse |
| `test_movement.py` | Movement budget and axis selection | Preserve momentum without field influence; budget schedules one step |
| `test_scalar_field_model.py` | Current-model assembly | Occupancy source, nonnegative field, transverse response and legacy activity |
| `test_field_composition.py` | Replacement in the engine | Alternative laws change the expected outcome; remainder-only activity persists |
| `test_scalar_engine.py` | Causality, occupancy and scheduling | One-edge propagation and movement; one particle update per tick |
| `test_diagnostics.py` | Measurement and display | Exact XY/XZ/YZ slices; full XYZ and off-plane records; source state untouched |
| `test_legacy_application.py` | Historical runner output | Headless metadata/events and lazy imports; diagonal acceptance tool selects explicit ScalarSimulation; explicit visualization preserves slice/volume event identity |
| `test_regressions.py` | Physical behavior | Prompt contact, reflection symmetry, three-plane turning, momentum, isolated motion and the original 180-tick result |
| `test_architecture.py` | Layer separation | Reject forbidden imports and adapter formulas; audit integer physics |
| `test_repository_language.py` | English repository text | Reject legacy non-English scripts in project prose; preserve mathematical notation |

Paths are relative to `tests/`. The dependency rules live in
`tests/architecture_rules.py`. Allowed and rejected examples test the rules
including relative imports and aliases.

## Exact numerical examples

| Calculation | Input | Expected result |
| --- | --- | --- |
| Uniform source | 3 sources, strength 64 | 192; no accumulated emission history |
| Current field | Neighbors `(1,2,3,4,5,6)`, two strength-64 sources, remainder 3, denominator 7 | Value 21, remainder 5 |
| Signed generic field | First-neighbor weight -1, neighbor value 10, denominator 3 | Value -3, remainder -1 |
| Range policy | Sample value -3, remainder -1 | Current policy returns value 0, remainder 0 |
| Gradient | Neighbors `(9,4,2,10,6,6)` | `(5,-8,0)` |
| Current turning | Momentum `(3,0,0)`, gradient `(128,64,0)`, denominator 64 | Impulse `(0,1,0)`, new momentum `(3,1,0)`, field momentum `(0,-1,0)` |
| Small impulse | Vector `(0,1,0)` each tick, numerator 1, denominator 64 | After 64 ticks: one y momentum unit, zero remainder |
| Quarter-rate movement | Momentum `(3,0,0)`, cap 12, initial budget 0 | Budgets 3, 6, 9; fourth tick moves +x with budget 0 |
| Diagonal direction | Momentum `(3,-2,1)`, initial phase 0 | Cycle: +x, +x, +x, -y, -y, +z |
| Periodic boundary | Shape `(4,5,6)`, address `(-1,12,13)` | `(3,2,1)` |
| Alternative field remainder | Initial value 1, local weight 8, neighbor weights 0, denominator 7 | Value 1 with remainders 1 through 6; seventh tick value 2, remainder 0 |
| Intermediate overflow | Product exceeds 64-bit work bound, even with a cancelling remainder | OverflowError at multiplication |

These are independently fixed expectations. Conservation tests also use identities
such as the sum of particle and field momentum before and after exchange.
Regression assertions use independently specified physical outcomes rather than
copying the tested formula. Historical engine/API and old-Python compatibility
are not acceptance targets.

## Calculation ownership

Source multiplication and nonnegative clipping live in `fields/policies.py`.
Field arithmetic lives in `fields/scalar.py`; turning and movement in `dynamics/`.
`core/lattice.py` centralizes addresses and neighbors. Bounded multiplication,
remainder accumulation and division live in `core/state.py` and serve all three
turning components.

Node activity is an injected decision. The original model explicitly keeps its
old value-based activity. Supplying `ScalarSimulation(field=...)` tracks remainder
changes by default; `field_activity=` selects another policy.

Model, API and compatibility assembly contain no independent arithmetic.
Architecture checks reject runtime formulas in these modules. Configuration and
initial conditions are intentionally specific and tested through the behavior
they produce. The framework remains constrained to 3D, six neighbors and the
declared fixed node schema.

## Running and validating changes

The suite reuses world runs when their inputs and required observations coincide.
The existing 24-tick contact/reflection experiment also checks the first transverse
response, per-tick momentum and final remainders. The 110-tick turning experiment
covers XY, XZ and YZ with momentum and remainder checks. Stationary-source symmetry
and persistence remain in `test_scalar_engine.py`. The shared
plane/volume application test checks metadata, traces and standalone HTML together.
The independent eight-case stream/free-control comparison covers the ordinary
isolated-rate cases; the original sampler retains only the additional 1/100 and
18/20 rate regimes. Bounds and known physical failure evidence remain covered.
The frozen engine is no longer imported or simulated, and the old facade API
comparison is removed. This reduction removes four collected cases, six worlds
and 447 simulation ticks without removing the physical regimes above.

Run `python tools/check.py` from the installed project. It checks style, types and
behavior and creates `artifacts/test-runs.html` for all captured world runs.
Pure-function unit tests do not run a world. See `VALIDATION.md` for recorded
validation and tool versions.

A new law requires inputs, expected outputs and edge cases before implementation.
Test its generic calculation and engine integration independently. Static checks
enforce known boundaries; they do not replace behavioral tests.

## Local links: candidate v11

| Test | Input | Expected outcome or boundary |
| --- | --- | --- |
| Generic stretch | Base 100, endpoint values 10 and 10 | Length 110; swapping endpoints changes nothing |
| Transit time | Length 110, rate c or c/2 | 110 or 220 ticks; no credit from a previous link |
| Numerical limits | Negative, floating-point or overflowing input | Explicit error before commit |
| Ownership | All six directions, including periodic seams | Both endpoints identify the same owner |
| Geometry message | Old length 100, proposed 110 | Both endpoints stay at 100 until delivery at tick 100 |
| Busy channel | Hundreds of updates during transit | One packet, three integers; zero is delivered and clears state |
| Simultaneous proposals | Lengths 13 and 7 arrive together | Both sides select 13 regardless of processing order |
| Replace merge policy | Same inputs with min | Both sides select 7; policy is injectable |
| Causality | Source two length-3 links away | No target influence before t=6 |
| Read boundary | Direct remote scalar read raises | Run succeeds through delivered mailboxes only |
| Rest and c | Stationary particle and fast particle on length-5 link | Rest stays fixed; fast particle arrives at t=5 |
| Locked transit | Departure length 3, field grows en route | Arrival time remains fixed at departure |
| Symmetry | Stationary source, coupling 1, 80 ticks | Six directions equal; zero momentum |
| Three particles | Moving sources, coupling 1, 50 ticks | Total momentum conserved each tick; valid occupancy |

Historical baseline expectations remain unchanged. World tests use the existing
HTML pipeline only when `--visualize-runs` is explicitly requested.
The stretch law and proposal merge are tested as separate hypotheses.

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
- A model importing an engine through `from ..core import engine` or
  `linked_engine` must be rejected, including that indirect form.
- A new or nested model containing `x + 1` or `source * count` must fail the
  assembly gate. Every file under `models/` is covered rather than a fixed list
  of existing model names.
- A model selecting `MeanStretch(100, 1, 2)` must pass: selecting parameters is
  composition, while the reusable component owns the formula.
- These tests do not run worlds and do not prove that an agent in another
  conversation has read the instructions.

## Quantum detector trial — opt-in only

The feature contract is in [QUANTUM_DETECTOR_TRIAL.md](QUANTUM_DETECTOR_TRIAL.md).
For a prescribed two-output interferometer, phase counts 0, 1, 2, 3 must yield
weights (4,0), (2,2), (0,4), (2,2). Enumerating tickets 0 through 3 verifies the
exact categorical selection; it does not test empirical randomness.

At world tick 8, the test controller commits exactly one detector record while
Engine state and time remain unchanged. Four repeated readouts, including a
changed ticket, return the same record without extra evaluation. Two bridges
share the result. Continued physical evolution must match the unqueried baseline
through tick 12. The detector record is not an Engine-native physical event.

Bad tickets, early or late first-readout timestamps, overflowing amplitudes or
weights, a zero total weight and exhausted combined work budgets must fail
without creating a terminal record. Pure queries never sample; repeated queries
preserve history and report cache hits. Different query depths retain model cost
1 and world time cost 0 while reporting distinct host work under Q-ORACLE-1.

Quantum boundary tests reuse the project's import resolver. Relative Engine
imports, importing engine from core and importing quantum from diagnostics must
be rejected even with aliases. Bounded arithmetic from core.state, imports within
quantum and the integration adapter are allowed. These are static checks, not a
proof against arbitrary dynamic Python or a proof of physical locality.

## Locality and bounded local work

`test_locality.py` supplies a read spy at (3,3,3) in extents 8 and 1,000,000.
Both calls must read the same six cardinal neighbors once each and return the
six supplied values in order. This test creates no world and advances no time.
Negative source examples in fields, dynamics and models must reject global node
or particle access, occupancy/history reads and shadow step/run calls. The
normal architecture test scans all production modules with the same guard.
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

## Motion display and playback

- `test_render_motion.py`: momentum (3,0,0) at c_units=12 produces an arrow
  of length 2.7; (12,0,0) produces 10.8. Momentum (3,4,0) at c_units=14
  produces (3.24,4.32,0), length 5.4. Rest or a missing scale shows no arrow;
  invalid scales are rejected. These are display-only numerical calculations.
- Periodic display fixtures cover both directions and every axis. The move
  x=63 to x=0 in a 64-node axis is a boundary crossing, not a multi-node jump.
  The move x=63 to x=1 is both a boundary crossing and a two-node jump;
  the renderer must preserve both indicators. Two simultaneous seam crossings
  likewise cannot hide a two-cardinal-step displacement.
- `test_playback.py`: two distinct synthetic snapshots are rendered in both
  slice and 3D modes. Expect two distinct GIF frames with positive duration,
  no repeat extension, and an HTML note that playback stops at the end.
- `test_three_particle_continuity.py`: replay the reported 64-tick experiment
  in a 64x48x32 world with its original three seeds. Every particle ID persists;
  each particle stays put or moves to one periodic neighbor at each tick.
  Expect no boundary crossings in this exact experiment. When visualization is
  requested, save every tick in HTML without interpolating or smoothing positions.
- Continuity is not an isolated-motion or self-force test. A trajectory may
  obey the one-hop bound and still contain an incorrect self-induced turn.


## Run rejection for isolated momentum changes

`test_run_invariants.py` requires rejection of even a one-unit isolated momentum
change and acceptance of unchanged momentum. A real diagonal self-field run with
initial momentum (1,1,0), force denominator 12 and 72 requested ticks must stop at
tick 45 with actual momentum (1,0,0), even with frame_stride=64. Metadata must say
failed and the trace must survive. When visualization is requested, HTML must
say FAILED RUN and include the failure frame.
Total momentum conservation does not excuse the particle's self-impulse. A stationary
isolated run passes; a two-particle contact run is not subject to isolated classification.
These tests verify the detector, not success of the physical inertial-motion gate.

## Mass and elastic same-node contact

`test_collisions.py` independently evaluates total momentum and classical kinetic
energy with diagnostic Fraction arithmetic, never using those values in physics.

| Input | Required outcome |
| --- | --- |
| Masses 1,1; momenta +3,-3 | Momenta -3,+3 |
| Masses 1,2; momenta +3,0 | Momenta -1,+4 |
| Masses 1,2; momenta +1,0 | Exact momenta -1/3,+4/3; no integer truncation |
| Opposite 3D momenta (3,2,-1),(-3,-2,1) | Every component reverses |
| Oblique equal-mass momenta (3,0,0),(0,3,0) | Momentum vectors exchange |
| 54 rational input pairs across unequal masses | Exact energy/momentum, reversibility and input-exchange symmetry |
| Momentum 1, mass 2, cap 12 | Half-unit budget credit, first hop after 24 ticks |
| Length 5, momentum numerator 1, denominator 3, mass 2, cap 12 | Transit 360 ticks |
| Same-node head-on arrival at completed tick 4 | One collision, no extra hop; separation at tick 8 |
| Heavy stationary target | Fractional outgoing momenta persist and the target eventually moves |
| Local links of length 2 at half c | No collision in flight; one on arrival at event tick 4 |
| One-node periodic self-loop | One contact, stable slot identity across four ticks |
| Independent transparent contact callable | Replacement preserves momentum instead of backscattering |
| Periodic four-node axis | Contact at x=0, then another at x=2 after separation |
| Different simultaneous addresses | No collision despite visiting the same address at different times |
| Four co-residents | Fixed 16 flags, conserved totals and at most one collision per particle per tick |
| Invalid mass or bound overflow | Failure before insertion or atomic pair commit; faulted world rejects continuation |

Integration worlds are headless unless visualization is requested. Historical
fixed-schema, numeric and collision checks cover those research records and defaults.

## Balanced movement and twelve-node halo candidate

`test_balanced_movement.py` checks all 342 signed nonzero directions in [-3,3]^3
for exact cycle counts, bounded prefix error, scaling, rate, invalid inputs and
register limits. `test_balanced_halo.py` runs six isolated signed 3D momenta for
200 ticks, checks the exact old/new six-neighbor target set, verifies an external
seed still creates momentum, verifies equal-and-opposite contact response, and
shows the same balanced movement without the halo fails the p=(1,1,0) input.
`tools/check_diagonal_motion.py` renders five engine runs and accepts only the new
candidate cases. See [BALANCED_MOTION.md](BALANCED_MOTION.md).

- Historical candidate composition: `BalancedSimulation(collisions=True)` handles
  two diagonal particles of masses 1 and 2, conserves pair invariants in a
  source-free run and separates them after one contact. All existing balanced
  movement and self-halo expectations remain unchanged.

## Run capture and export performance

These contracts belong to the historical runner and optional renderer. Tests that
generate visual artifacts require `pytest --visualize-runs`; ordinary tests stay
headless and retain physical assertions.

- `test_run_capture.py` checks selected-view snapshots against independent state
  expectations, including zero ticks, an unsampled final tick, invalid slices,
  complete event records and a partially committed failed tick. Failure metadata
  and its final frame must reflect the changed state, including exact fractions.
- `test_render_export.py` checks saved pixels and frame durations against the
  previous export path for synthetic figures, full 3D dimensions, non-repeating
  playback and figure cleanup on failure.
- Performance measurements use identical scenario inputs, tick counts, display
  sampling, image dimensions and dependencies. Timing comparisons are recorded
  separately from functional tests; CI does not assert machine-dependent seconds.

## Live display during execution

- `test_live_display.py` exercises a real spawned consumer: a copied snapshot
  appears before completion, later producer mutation stays isolated, and queued
  large snapshots can be cancelled without a feeder shutdown deadlock. Startup,
  publication and unexpected worker-exit errors remain diagnostic. Failed runs
  preserve their reason and link only a newly registered artifact.
- `test_render_live.py` compares preview PNGs with the actual canonical last
  raster for volume and slice views, including transparent and tight-crop export
  settings. Callbacks arrive before final GIF/HTML completion and cannot mutate
  the canonical images. Empty histories and failed writes close figures.
- `test_run_live.py` checks live/nonlive event and metadata parity, early page
  availability, headless defaults and explicit opt-in, cleanup, and preservation
  of physical errors even when final rendering also fails.
- Manual run evidence records page/image availability before final output,
  observed phases and saved image changes. First-image latency and whole-run
  duration are distinct measurements; browser refresh and recorded-frame
  equivalence are separate checks. Never infer concurrency from a callback name.

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


## Selected deferred quantum event network

`test_event_links.py` checks immutable event spacetime through a split/join,
direct event lookup without separate predecessor lists, current-head updates,
foreign and forged handle rejection, failed-append atomicity and fixed capacity.
`test_quantum_node_events.py` runs the native four-Node initialization: final
C/D weights are 0/1, reversed by a phase, and 1/2 each after either intermediate
position outcome. Exact correlated checkpoints preserve those cases, audit
records, handle identity and individual modeled times. A two-tick link must
remain admissible after compaction, while a prematurely reused register remains
inadmissible. Colocated registers retain disjoint dependency components until
their configured joint operation. A 2,000-event DAG leaves cursor storage fixed
and stores its past solely in immutable spacetime events. Empty quantum
Nodes introduce no carrier source, cycle, inventory, transport or model cost;
public head snapshots stay immutable and queries never change physical state.

The [origin-cell contract](WAVE_ORIGINS.md) additionally requires a six-origin
local capacity, causal support propagation without multi-Link same-tick relay,
one terminal commit under competing requests, conditional retry after no-click,
and local invalidation at the next tick without a commit-time bank sweep. A
continuing outcome must preserve conditional state and remaining coherence; a
position result must not fabricate a sharp momentum, and this extension does not
claim a physical momentum observable. A seventh origin fails before
partial publication. Origins and immutable source events survive checkpoints.
Unarrived support cannot execute a gate. Retired gates may be skipped only when
the complete retained correlated density is invariant; otherwise reject before
layer publication. A certified skip adds no operation payload, phase change or
physical-ready-time write. A retired instrument requires one possible outcome,
equal to its declared `null_outcome`, and unchanged complete density. An arbitrary
remote X, deterministic click or state-changing null must fail cancellation.
Recheck native null certificates when the target head changes even without a
fresh arrival marker. One-origin joint states are valid interaction definitions;
origin count never supplies evidence of a two-disturbance collision.
Untagged v3 gates, instrument requests without participant IDs and origin-unaware carrier
bindings are rejected. Active tagged continuations preserve the configured
interference. Event provenance names origins without treating them as extra
quantum amplitude sources. Cancellation guards and their one-unit audit events
must be included once in total model cost and reported in `host_cancellation_checks`.
The carrier subtotal remains separate. Direct status checks are bounded local
work; certification, tensor evaluation, locking and total audit size have separate
host costs. Finite passing cases do not prove
universal physical locality, conservation or a classical limit.

The contract is [QUANTUM_EVENTS.md](QUANTUM_EVENTS.md), Q-EVENTS-1 in the main
definitions, and the existing Q-ORACLE-1 exception. This table defines required
expectations; a passing source identity and command belong in the integration PR.

| Suite | Independent expectations |
| --- | --- |
| `test_quantum_event_network.py` | Existing-owner selection; 3:4 split gives 9:16 weights; deferred/eager agreement using independently lifted dense matrices; prior correlated records are included; a postponed phase becomes necessary at recombination; partial records and exact checkpoints preserve remaining entanglement |
| `test_quantum_event_network.py` | No-transfer changes excitation from 1/2 to 9/34; early projection changes coherent return from 1 to 337/625; fresh-environment contacts use no detector call; immutable and stale decision guards; certain outcomes require no random ticket |
| `test_quantum_event_network.py` | A 2,000-operation queried chain leaves a disconnected 2,000-operation chain unevaluated; zero extra world ticks; nearest-neighbor/disjoint supports; matrix completeness; node/term/traversal/record/register failures do not commit an outcome |
| `test_quantum_event_network.py` | A single occupied Node has 16 equal Fourier weights; Parseval and the finite position/Fourier uncertainty bound; these are state-representation checks, not a derived free-motion law |
| `test_quantum_event_trial.py` | Reproducible 4x4 headless controller through the existing owner, explicit ticket choice, fixed event time, and preserved legacy scalar query API |

The legacy quantum, architecture, integer, locality, navigation and language
suites remain regression requirements. Do not weaken them to accept the new
candidate. No physical engine behavior or default rendering mode is changed.

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

`test_reference_examples.py` verifies that public APIs resolve to the correct
active or historical owner, that collision checks load the canonical workspace
JSON, and that all five existing reference worlds keep their independent numeric
assertions without producing HTML/GIF. The wrapper and its dynamically selected
inputs explicitly select this regression through `tools/check.py`; every changed
path selects the inexpensive repository language and canonical-copy guards.

## Native event programs and path costs

`tests/test_native_event_runtime.py` covers the [native event contract](NATIVE_QUANTUM_EVENTS.md):
365 exact ticket cases, deterministic classical trajectories, shared identity
and packet ancestry, repeated encounters, bounded failures, code/type renaming,
normal runner output and per-cycle cost-dependent delay without repeated charges.
Existing quantum, locality, generic initialization and physical regression suites
remain affected consumers. These checks do not derive a classical limit.

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
worker counts, explicit rejection of native event programs, saved host-execution
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

## Catalog contact bindings

`tests/test_catalog_contact.py` exercises all 34 established particle/multiplet
bindings through the existing causal contact rule for 16 ticks each. Charge and
encoded mass inventory keep one owner through preparation and capture; spatial
source/loss/escape accounting remains balanced. The default three-domain world
retains charge -2 in charge-thirds and mass reference inventory 7371 keV/c2.
Positive, negative and neutral source signs, antiparticle references, duplicate
placements, metadata preservation and the ten-domain schema bound are checked.
Unassigned flavor-neutrino mass is distinguished from theoretical zero mass.
This is configuration integration, not QCD, spin dynamics, physical total mass
or field/matter energy closure. The [example guide](../examples/catalog-contact/README.md)
owns the setup and limitations.
