# Test inputs and expected results

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
| `test_boundary_configuration.py` | Periodic default under both schemas; exact open/periodic setting; every positive and negative face of a 3x4x5 world; single-cell extents; invalid names, coordinates, faces and bounds rejected |
| `test_open_boundaries.py` | Carrier exits and wrapping on all six faces after full transit; unchanged signed vectors; terminal quantity 1 escapes even with zero retention while an interior copy decays; mixed corner fields/baselines; invalid terminal payloads commit neither loss nor removal; unused emitter allowance does not become physical escape |
| `test_spatial_scheduling.py` | Optimized and forced full-sweep runs have identical per-tick snapshots, costs, events and balances; dormant history is not enumerated; reactions reactivate known idle cells without delaying their departure; newly created cells are not backdated |
| `test_disturbance_application.py` | Open example records carried escape 72, spatial escape 20 and dissipation 52; no carrier reentry; zero-tick edge case has empty events and zero escape; runner and snapshot agree |
| `test_workspace.py`, `test_workspace_integration.py` | Workspace accepts field examples and records open escape; direct/HTTP runs retain equal physical output; open terminal playback does not wrap or dereference a missing target; balanced loss/escape is not a failed check; field renaming updates flux expressions |

Measured performance comparisons use the same 5,000 ticks, configuration,
per-tick accounting and three-record checks. Record source import paths and
fingerprints, stepping and diagnostic time separately. Timing is evidence for
that machine, not a fixed wall-time test threshold or a change to model cost.

## Finite spatial candidate, schema 2

The law is specified in [SPATIAL_FIELDS.md](SPATIAL_FIELDS.md) and
[SPATIAL_COUPLINGS.md](SPATIAL_COUPLINGS.md). These tests retain the schema 1
conservative expectations and add separate dissipative expectations.

| Suite | Independent inputs and required outcomes |
| --- | --- |
| `test_dissipative_initialization.py` | Version 2 requires strict integer retention and nonnegative component budgets; version 1 rejects new keys; invalid signs, shapes, bounds, missing fields and splitting sources fail |
| `test_spatial_decay.py` | Half retention maps 20 through 10, 5, 2, 1 to 0; both signed one-unit tails vanish even at retention `(MAX_VALUE-1)/MAX_VALUE`; unsigned invalid input cannot be erased by decay |
| `test_finite_spatial_engine.py` | Link times 1, 2 and 3 preserve in-flight stock until arrival; budget 5/request 2 emits 2, 2, 1 then 0; moving and delayed sources cannot restore allowances; baseline remains; delivery failure commits neither loss nor packet removal |
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

Cell activity is an injected decision. The original model explicitly keeps its
old value-based activity. Supplying `ScalarSimulation(field=...)` tracks remainder
changes by default; `field_activity=` selects another policy.

Model, API and compatibility assembly contain no independent arithmetic.
Architecture checks reject runtime formulas in these modules. Configuration and
initial conditions are intentionally specific and tested through the behavior
they produce. The framework remains constrained to 3D, six neighbors and the
declared fixed cell schema.

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
Negative source examples in fields, dynamics and models must reject global cell
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
  x=63 to x=0 in a 64-cell axis is a boundary crossing, not a multi-cell jump.
  The move x=63 to x=1 is both a boundary crossing and a two-cell jump;
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

## Mass and elastic same-cell contact

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
| Same-cell head-on arrival at completed tick 4 | One collision, no extra hop; separation at tick 8 |
| Heavy stationary target | Fractional outgoing momenta persist and the target eventually moves |
| Local links of length 2 at half c | No collision in flight; one on arrival at event tick 4 |
| One-cell periodic self-loop | One contact, stable slot identity across four ticks |
| Independent transparent contact callable | Replacement preserves momentum instead of backscattering |
| Periodic four-cell axis | Contact at x=0, then another at x=2 after separation |
| Different simultaneous addresses | No collision despite visiting the same address at different times |
| Four co-residents | Fixed 16 flags, conserved totals and at most one collision per particle per tick |
| Invalid mass or bound overflow | Failure before insertion or atomic pair commit; faulted world rejects continuation |

Integration worlds are headless unless visualization is requested. Historical
fixed-schema, numeric and collision checks cover those research records and defaults.

## Balanced movement and twelve-cell halo candidate

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
cell and passes without an invented collision, that parallel speeds differ and
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

The contract is [QUANTUM_EVENTS.md](QUANTUM_EVENTS.md), Q-EVENTS-1 in the main
definitions, and the existing Q-ORACLE-1 exception. This table defines required
expectations; a passing source identity and command belong in the integration PR.

| Suite | Independent expectations |
| --- | --- |
| `test_quantum_event_network.py` | Existing-owner selection; 3:4 split gives 9:16 weights; deferred/eager agreement using independently lifted dense matrices; prior correlated records are included; a postponed phase becomes necessary at recombination; partial records and exact checkpoints preserve remaining entanglement |
| `test_quantum_event_network.py` | No-transfer changes excitation from 1/2 to 9/34; early projection changes coherent return from 1 to 337/625; fresh-environment contacts use no detector call; immutable and stale decision guards; certain outcomes require no random ticket |
| `test_quantum_event_network.py` | A 2,000-operation queried chain leaves a disconnected 2,000-operation chain unevaluated; zero extra world ticks; nearest-neighbor/disjoint supports; matrix completeness; node/term/traversal/record/register failures do not commit an outcome |
| `test_quantum_event_network.py` | A single occupied site has 16 equal Fourier weights; Parseval and the finite position/Fourier uncertainty bound; these are state-representation checks, not a derived free-motion law |
| `test_quantum_event_trial.py` | Reproducible 4x4 headless controller through the existing owner, explicit ticket choice, fixed event time, and preserved legacy scalar query API |

The legacy quantum, architecture, integer, locality, navigation and language
suites remain regression requirements. Do not weaken them to accept the new
candidate. No physical engine behavior or default rendering mode is changed.

## Local field impulse and cell ownership

`tests/test_local_lorentz_field.py` covers a four-link causal pulse, independent
electric/magnetic impulse directions, neutral response, equal/opposite local
momentum, delayed commit, field autonomy, renaming and invalid arithmetic.
`tests/test_cell_state_contract.py` verifies formula-free evolving state and
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

Inline observer input is covered by `tests/test_local_observer.py`: normal schema
validation, rejection before output creation, ambiguous placement rejection, exact
saved initialization and unchanged physical results with recording enabled.
