# Architecture and change boundaries

[Integer Node execution](NODE_VECTOR_PROCESSOR.md) owns receive, preparation,
pending completion and publication in `core/disturbance_node.py` and
`core/spatial_node.py`. Shared services contain seed-free immutable definitions,
local law providers and write-side accounting; Nodes receive no world lookup.
Transport indexes local fixed output banks and validates adjacent delivery.
`core/node_conservation.py` is a DTO/protocol boundary; generic readout arithmetic
lives in `fields/node_conservation.py`, and its parser reuses initialization's
expression grammar. A configured exact balance check precedes physical mutation.
The profile's declared k and counted operation cost are separate quantities.
Indexed spatial rules reuse carrier role selection and the existing expression
evaluator with an additional local field owner. Pending proposals contain bounded
slot snapshots and deltas, never executable expressions. Field-only pending
proposals similarly retain per-rule deltas and outgoing views. Shared immutable
law services revalidate them before Node-owned commits; they receive local state
only. The [rule contract](NODE_VECTOR_PROCESSOR.md#local-rules) separates consumed
start triggers from persistent conditions and defines their failure behavior.

The opt-in [shared field computation cycle](SPATIAL_COMPUTATION_DELAY.md)
extends `PendingCycle` with one immutable spatial proposal, reaction phases
and cached joint-guard input. `SpatialNodeState` retains fixed incoming populations,
port readings, counts and decay cost while pending. Inventory includes these
actual input owners once and excludes proposals. No expressions or histories
enter evolving state. The carrier Node coordinates both local owners atomically.

[Property selectors](PROPERTY_COUPLINGS.md) compile into fixed layout compatibility
sets in `core/coupling_selectors.py`, shared by parsing, scheduling and local laws.
`core/validation.py` retains bounded checks without charging the physical clock.
The optional [local conservation audit](LOCAL_CONSERVATION.md) lives in
`diagnostics/local_conservation.py`; public assembly attaches it to committed
events and exposes immutable `core/conservation_state.py` inventory views.
Its host work is separate from model operation costs; it never provides an update or repair.

The quantum-register extension (`quantum/mixed.py`, `quantum/operations.py`,
`integration/quantum_entities.py`) was deleted on 2026-09-17; `entities.py`
compiles classical profiles only.

`entity_catalog.py` validates descriptive reference metadata and its links.
Its decimal measurement parsing is host-side only and never updates physical
state. `entities.py` requires separate explicit experiment profiles for version 2
catalogs, compiles them into ordinary initialization, and delegates runtime schema
validation to `initialization.py`. Reference properties and interaction lists do
not enter runtime laws or select species-specific behavior. See
[entity catalog](ENTITY_CATALOG.md).
The [reference units](REFERENCE_UNITS.md) authoring tool owns the shared external
constant/unit registry and one-time exact rational conversion into bounded
Scalar/Vector initialization components. Rational calibration and error reports
remain host metadata; they are never a physical arithmetic fallback or a runtime
unit conversion. Integer scales and future physical intermediates still obey
the ordinary bounds. Unit names do not select interactions or propagation laws.
Optional two-record type conversion follows the existing frozen pair proposal
and delayed engine commit; its ownership restrictions are in
[local conversions](LOCAL_CONVERSIONS.md).

## Configuration validation ownership

The [configuration preflight contract](CONFIGURATION_VALIDATION.md) defines the
shared JSON decoder, supported format dispatch and explicit context dependencies.
`configuration_validation.py` coordinates existing format owners and returns
reports without constructing a simulation. It shares initialization/observer
preparation with the runner; the UI consumes its read-only validation result.
Semantic rules remain in initialization, native programs, catalog, profiles and
observer owners. Runtime execution and physical acceptance remain separate checks.

## Local integer operation contract

This contract applies to all new and changed physical code, entity definitions,
configuration adapters and prototypes intended for the active Simulation.
Use [DISTURBANCES.md](DISTURBANCES.md) for the supported operation vocabulary
and [LOCAL_FIELD_RULES.md](LOCAL_FIELD_RULES.md) for delivered field inputs.
LOCALITY-1 and the numeric bounds in SIMULATOR_DEFINITIONS.md remain authoritative.

### Generic operations and law ownership

Express active laws as initialization-defined compositions of supported scalar
and vector operations. Particle names, charges, masses, couplings, thresholds,
interaction eligibility and participant limits are data; names must not select
hidden physical equations. Reuse generic operators instead of adding a special
electron, proton, electromagnetic or computation-load branch to the engine.

The engine owns scheduling, addresses, capacities, transport timing, validation
and atomic commits. It must not own a model-specific force, energy, momentum or
field equation. Generic arithmetic belongs to its documented reusable owner;
model/API assembly only composes it. Scheduler indexing and timing arithmetic
are necessary bookkeeping, not permission to hide physical laws in the scheduler.
An externally configured equation is still a chosen law, not evidence that it
emerged from the lattice.

Keep immutable parsed law definitions outside dynamic node, disturbance,
pending-proposal and packet payloads. Payloads carry bounded state values and
declared identifiers, never copied expression trees, formula strings, Python
callbacks or executable code. Read-only diagnostics may calculate global
measurements but cannot supply a physical update or repair conservation.

### Integers, vectors and tensors

All physical numeric inputs, registers, intermediate results and transmitted
components use the declared bounded integer domains. Reject booleans and
floating-point inputs rather than coercing them. Python's arbitrary-precision
integers do not remove the model's working-register bounds: check intermediates
before cancellation, scaling or assignment. Never add float, complex, NumPy,
Decimal or Fraction arithmetic as a physical fallback.

Represent scales and ratios with explicit bounded integer numerators and
denominators. Exact-division operators must reject a zero divisor or a nonexact
result. A rule that permits division with remainder must declare the existing
bounded remainder owner, update and lifetime; do not silently discard a remainder,
round through floating point, wrap overflow or clamp a failed calculation.
Keep documented integer split/quantization policies explicit and test their
accounting. Arithmetic failure must not leave a partially committed transaction.

The active field schema currently supports scalars and three-component vectors.
Its constant 3-by-3 integer matrix transform is not general tensor-valued state.
Do not claim arbitrary tensor support or silently flatten an unsupported shape.
A future tensor extension must declare fixed rank and dimensions, component
bounds, generic operators, transport coding and all state/diagnostic consumers,
with shape, overflow and locality tests before use. Tensor notation alone does
not make a calculation generic, integer or local.

### Local inputs and bounded work

A physical rule may read its own fixed local records and information already
delivered through the six neighbor ports under the transport contract. Neighbor
coordinates do not authorize instantaneous reads of remote physical state.
Trace every input to its causal owner, including self-field subtraction,
computation-load fields, energy bookkeeping and collision eligibility.

Fix local record, field, rule and participant capacities in validated definitions.
Only supported configured participant limits may be used; a larger value does
not create an unsupported many-body operator. Bound local loops and storage by
those capacities, independently of world size. Never compute responses from an
all-particle scan, global field reconstruction, growing per-source history or a
host-side correction. Charge, momentum and declared energy balances need explicit
local owners and transaction checks; a diagnostic total alone is not a law.

### Review evidence and scope

For each affected operator or rule, identify its owner, scalar/vector shape,
integer input/intermediate/output bounds, causal input path and failure behavior.
Run the affected checks selected by tools/check.py, including related integer,
initialization, architecture and locality gates when those contracts change.
The existing entry points include tests/test_integer_contract.py,
tests/test_initialization.py, tests/test_architecture.py and tests/test_locality.py.
Review gaps in scanner coverage explicitly; passing static checks is not a proof
about arbitrary Python or every possible configuration.

Read-only rendering and host timing may use noninteger arithmetic outside the
physical path; their results must never feed physical state. Historical named
models retain their explicit contracts and must not be copied into the active
generic engine. External floating-point or globally coupled reference prototypes
are not compliant active-engine implementations, even if their GIFs look useful.

Q-ORACLE-1, the explicitly scoped opt-in quantum exception, was deleted on
2026-09-17 with Highlights section 3.18 (issue #164, buckets B.1 and B.2), the
source envelopes on the same day under Highlights section 3.5 (bucket B.3),
the causal event ledger under Highlights section 3.20 (bucket B.4) and the
bond registry, claim-gather and the lottery capture the same day under
Highlights sections 3.19, 3.20, 5.1 and 5.4 (bucket B.5), and the record
operations (records as owners and the N-to-M conversion of records) the same
day under Highlights sections 3.20 and 5.1 (bucket B.6, the last). No path in
the package answers at a distance, and no Node folds an arrival into a
resident. That every bucket of issue #164 is deleted is not evidence that every
repository path already satisfies the active local integer contract.

## Generated output ownership

The optional [local observer](LOCAL_OBSERVER.md) belongs to diagnostics.
`observer_configuration.py` owns placement validation shared by initialization and
the runner. Initialization validates the optional `observer` member without adding
it to physical state; the runner selects recording without eager diagnostic imports.
`diagnostics/local_observer.py` whitelists completed events at one node and
archives copied reception values plus a cycle counter. The runner captures exact
receipt prefixes beside playback frames. Enriched spatial reception events are
emitted after ownership commits. Neither archive, display nor clock count is a
physical planner input.

`retention.py` owns host-only artifact registration, writer leases and expiry.
Runners own complete fresh output directories; the workspace owns exact input,
log and export files and declares the child-output dependency for companions.
Cleanup uses recorded filesystem generations and operating-system locks, with
recoverable quarantine before removal. The module never imports or changes
physical engine state. Its one-shot and singleton watcher interfaces share the
[same retention contract](RETENTION.md).

## Active generic ownership

The record policy (`core/record_policy.RecordPolicy`,
`fields/record_operations.RecordOperations`) was deleted on 2026-09-17 (issue
#164, bucket B.6; see the
[migration note](MIGRATION.md#records-as-owners-deleted-on-2026-09-17)).
`core/disturbance_node.py` owns what stays of it as pure functions over the
immutable run definition: `carrier_work`, the activity predicate that decides
whether resident records give a Node a cycle to plan, and `report_cost`, the
write of an already-metered `cost_field`. A delivered record takes the first
spare slot outside the pending lock; nothing is folded into a resident record.
The engine alone determines arrival eligibility, supplies locks, validates slot
capacity and commits proposals before clearing packets; `NodeServices` carries
the carrier types a spatial coupling or interaction selects (`spatial_types`).
Direct `DisturbanceEngine` callers pass no `record_policy=`. Configuration files
are unchanged.


`disturbance_api.Simulation(initial: InitialState)` composes the generic engine
and local law; it is exported as the primary package Simulation.
`initialization.py` reads strict JSON data and resolves names to bounded typed
definitions. `core/disturbance_state.py` owns fixed schemas and payload coding;
`fields/disturbances.py` owns expression arithmetic, updates, paired coupling
and transport proposals; `core/disturbance_engine.py` owns addresses, capacity,
fixed transit and delayed atomic commits. No layer branches on a physical field
name or imports Python code named by initialization.

The opt-in rational extension stays within these owners: `fields/ratios.py`
owns finite exact arithmetic and projections; `fields/routing.py` owns balanced
six-port selection and fractional credit. Neither receives world state. Fixed
carrier bookkeeping travels through the existing scheduler. The numerical and
cost amendment is explicit in [RATIONAL_PARTICLES.md](RATIONAL_PARTICLES.md).
Physical formulas in its examples are reference benchmarks, separate from the
elementary emergence probes in [PHYSICAL_ENTITIES.md](PHYSICAL_ENTITIES.md).

Field, type, model and unit labels are data. Reordering field/type declarations
must preserve the same resolved behavior; declared update/coupling order and
spatial axes can be meaningful and are not interchangeable. The executable
cross-layer checks live in `tests/test_generic_identity.py` (deleted on 2026-09-17). Genericity is scoped
to the supported integer scalar/vector schema, three-dimensional six-port
geometry, fixed capacities and declared operation set; it does not imply an
arbitrary equation interpreter.

Atomic interaction definitions share that path: initialization resolves bounded
assignments, invariants and activation expressions; `fields/disturbances.py`
evaluates frozen-pair proposals and exact per-transaction balances before routing.
They add no per-source memory or alternate commit path. Example physics remains
JSON data, including vector transforms and the unequal-mass elastic contact law.
The shared evaluator propagates explicitly supplied spatial flux through nested
operators. Atomic interactions operate after proposed spatial responses and
ordinary exchanges, retaining carried emission/reaction allowances and the
prepared opposite field reaction until the common delayed commit.

The complete source contract is [DISTURBANCES.md](DISTURBANCES.md). Its six-port,
bounded-record schema replaces the implicit scalar/particle schema for the
primary API. Global diagnostics never drive physical rules, and rendering is
absent unless explicitly requested.

The optional spatial extension uses `core/spatial_state.py` for fixed schemas,
`fields/spatial.py` for bounded emission/splitting and `fields/spatial_plan.py`
for pure local proposals. `core/spatial_engine.py` schedules and owns field
packets; `disturbance_api.py` composes its planner without formulas, and, when
a world declares `dense_field`, the dense region of `dense_field.py` (numpy
integer arrays, outside the core, behind the engine's `DenseRegion` protocol)
that cycles the board's pure-field Nodes as one step with the same integers
([the dense mode](SPATIAL_FIELDS.md#the-dense-mode-dense-field-v1)). The shared
engine combines diagnostics and costs while retaining separate field and
carrier clocks. See [SPATIAL_FIELDS.md](SPATIAL_FIELDS.md) for the contract and
the remaining self-attribution requirement. `fields/spatial_coupling.py` owns
local sampling, fractional exchange, exact quarter-turn rotation and reaction
allocation. The injected `SpatialCoupler` protocol keeps those calculations out
of engine scheduling. Carrier and field owners validate together before committing
the response; fixed sample registers and departure timestamps prevent future
reads or edits to old in-flight packets. See [SPATIAL_COUPLINGS.md](SPATIAL_COUPLINGS.md).

The optional phased-ray law retains its bounded prepared cosine/sine tuples in
immutable `SpatialFieldDefinition`, outside NodeState. Per-record departure,
capture-ticket and absorbed-phase rows have fixed configuration-derived sizes.
Each departure row carries four integers (amount, cursor, phase, advance); an
absorbed-phase row carries phase and advance. These bounded owner registers
preserve a ray's emitted advance without looking up a later emitter state;
Nodes validate that a field proposal changes only selected stock/vector fields
and permitted bookkeeping, preserving transport metadata. Funded/absorbed owners
currently reject delayed carrier plans on the independent spatial clock. The
read-only runner inventory binds ray momentum through explicit recoil/absorption
field references and counts actual resident, in-flight and escaped owners.

The opt-in [local field-rule contract](LOCAL_FIELD_RULES.md) reuses these owners.
`fields/local_field_rules.py` evaluates bounded multi-field retained/outgoing
proposals using delivered six-port data; `fields/spatial_plan.py` composes them
with existing emission and outward routing. Logical groups reference existing
scalar/vector fields and allocate no second physical owner.
`fields/spatial_interactions.py` extends the injected coupler with generic
field/carrier assignments and actual-commit invariant guards. The engine freezes
carrier transaction views and additive field deltas, then validates the complete
commit against current local field stock before either owner mutates. It never
replaces live fields with sampled state. Old emission metadata keeps its owner
through delayed carrier commits. Transformation ledgers are diagnostics, not
sources or inputs to physical laws. The schema, bounded expression evaluator,
fixed field clock and existing outward path remain shared.

The historical scalar, stream, linked, collision and balanced candidates and
their named research APIs were deleted on 2026-09-17 under Highlights sections
3.3, 3.4, 3.5, 3.19, 3.20, 5.1 and 5.4 (issue #164, bucket A). Their contracts
are no longer described here; the dated evidence in [VALIDATION.md](VALIDATION.md)
keeps their original scope.

[AGENTS.md](../AGENTS.md) is the shared contributor entry point.
`POSTULATES.md` is the plain-language conceptual entry point.
`SIMULATOR_DEFINITIONS.md` translates those principles into exact technical
requirements, and this document describes the code boundaries that enforce them.

## Monorepo ownership

Universe24 is one versioned repository, not a requirement that every component
run in one process. Keep the current package layout until an actual independently
built component justifies another package; do not create empty apps/packages trees.
The [README project map](../README.md#project-map) is the path index; the dependency
table below defines code boundaries. Architecture owns this repository policy.

| Information | Single owner | Update rule |
| --- | --- | --- |
| Executable code and law selection | [src/event_universe](../src/event_universe/) | Keep shared formulas generic; initialization data selects them |
| Generic initialization schema and transition law | [DISTURBANCES.md](DISTURBANCES.md) | Keep the active source contract separate from historical candidates |
| Physical contracts | [POSTULATES.md](../POSTULATES.md), [SIMULATOR_DEFINITIONS.md](../SIMULATOR_DEFINITIONS.md) | Plain-language principles and exact contracts have distinct roles |
| Test expectations | [TEST_EXPECTATIONS.md](TEST_EXPECTATIONS.md) | Link the responsible tests, inputs and outcomes without copying laws |
| Installation and execution | [README.md](../README.md) | Reuse the package CLI and [tools/check.py](../tools/check.py) |
| Contribution and integration | [CONTRIBUTING.md](../CONTRIBUTING.md) | One coordinated change includes affected providers and consumers |
| Durable agent procedures | [skills/workflow.md](../skills/workflow.md) and specialist Skills | Shared rules live once; specialist Skills reference them |
| Current task, owner and evidence | Repository Issues and PRs | Record head/base, acceptance target, blockers and next action |
| Checkout orientation | [PROJECT_STATUS.md](PROJECT_STATUS.md) | A dated, commit-pinned snapshot links to live work; no duplicate task ledger |

Use existing definition headings or stable rule IDs when mapping a change to code
and tests. Record the exact contract, implementation path and test path in the PR;
extend the responsible test-expectation entry if coverage changes. Never treat a
test's existence as proof it passed. Architectural decisions belong here or in a
linked focused decision document; physics decisions belong in their contracts.

Store reproducible scenario inputs, configuration and test fixtures with the code.
Keep generated videos, HTML, traces and large outputs outside source commits.
Link them from the PR with the code identity, command and relevant parameters;
artifact retention is finite, so preserve required evidence before it expires.
There is no automatic chat-to-repository or Google-Doc-to-code synchronization.

## Dependency direction

| Module | Allowed dependencies |
| --- | --- |
| `core/integer` | Standard-library types; owns working bounds, integer division and decoded component arithmetic |
| `core/disturbance_state` | Bounded arithmetic and immutable generic definitions |
| `core/disturbance_engine` | Generic records, local planner interface, scheduling and ownership |
| `core/node_execution` | Host-only isolated-interpreter Node tasks and execution measurements; no physical state ownership |
| `fields/disturbances` | Generic records and bounded integer arithmetic; no world or diagnostics |
| `initialization` | JSON input and generic typed definitions; no arbitrary execution |
| `disturbance_api` | Generic engine and disturbance local law |
| `diagnostics` | Read-only engine views, immutable events, rendering libraries |
| `runner` | Generic public API, initialization and optional diagnostics |
| `ui` | Local HTTP, strict initialization validation and isolated CLI process ownership |

## Configuration workspace

`ui.py` serves packaged `ui_assets/` HTML, CSS and JavaScript without a frontend
build. Templates remain the canonical JSON files in `examples/`, included as
package data files for installed use; `--configs` selects another directory.
Full inputs and JSON fragments share `initialization.parse_json_document`
duplicate-key enforcement. The existing validator checks configurations before
runs. The browser previews initial seed positions, not computed motion.

Each accepted request becomes immutable JSON passed to the existing runner in
a separate Python process using the server's package source. The UI never steps
an Engine or supplies physical arithmetic. It owns one active job, session
history, cancellation and links restricted to known artifacts. Configuration
edits require no compilation or restart. Output directories are unique;
Run & watch explicitly requests a movie; recording can be disabled and the CLI
remains headless by default. `diagnostics/disturbance_render.py` embeds copied
frames and metadata in the packaged self-contained player. Neither the player
nor its speed/projection controls supply simulation inputs. Name controls update
declarative references only. Cancelled runs are labeled incomplete. Loopback
binding, Host/Origin checks and a session token constrain HTTP access.
See [WORKSPACE.md](WORKSPACE.md) for lifecycle and persistence behavior.

## Generic calculations

`core/integer.py` owns shared decoded component addition/subtraction, ordered
sums, dot/cross products and nonnegative ceiling division. Products and ordered
partial sums retain their working-register checks, including overflow before
cancellation. Ceiling division retains the existing adjusted-numerator bound;
`signed_divrem` instead rounds toward zero and returns a signed remainder.
Callers supply schema-bounded components and retain payload encoding, field
validation, operation pricing and atomic commit ownership. The expression
interpreter delegates arithmetic while retaining broadcasting and AST costs.
See [shared arithmetic tests](../tests/test_integer_arithmetic.py).

## Deleted on 2026-09-17: the source envelopes

The modules `core/source_envelope_node.py`, `core/source_envelope_state.py`,
`core/source_emission.py`, `core/source_emission_node.py`,
`fields/source_envelope.py` and `fields/source_emission.py` (formula-free
amplitudes, finite source state, pending proposals, twenty-four Port slots,
the rational weight scale, the null record and their local transitions), the
`CausalSourceResolver` protocol of `core/event_resolution.py`,
`SpatialEngine.commit_source` with its `spatial_envelope_source` event, the
`source_envelope` member of the disturbance NodeState and the envelope
records of the formula-free state audit were deleted under Highlights section
3.5 and the [ray-event model](RAY_EVENT_MODEL.md) section 5 (row R5) and
section 6, step 7 (issue #164, bucket B.3): a field is the ray's own
information spreading in ray form, not a complex envelope retained at a Node.
Their runtime owners had gone with the integration layer on the same day.
There is no replacement module; the dated evidence stays in
[validation](VALIDATION.md).

## Deleted on 2026-09-17: the shared quantum resource, Q-ORACLE-1

The `quantum/` package (`deferred-unit-cost-oracle-v1`, the deferred event
network, wave origins, focus, mixed states and the terminal trial) and the
`integration/` package that bound it to the primary Simulation
(`event_program`, `event_runtime`, the contact runtimes, `quantum_entities`,
`quantum_bridge` and the two trials) were deleted under Highlights sections
3.18 (deleted), 3.19, 3.20 and 5.4 (issue #164, buckets B.1 and B.2). No
owner answers at a distance; the Detector is a marked Node, and every
alternative is an event on the board ([ray-event model](RAY_EVENT_MODEL.md)
section 5). The `event_program` initialization member went with them. Dated
evidence in [VALIDATION.md](VALIDATION.md) keeps its original scope.

## Verification scope

LOCALITY-1 in SIMULATOR_DEFINITIONS.md governs the complete dependency path of
every physical update, including self-field inputs. Shadow/reference
computations cannot be hidden behind a local adapter. `test_locality.py` rejects
known world access and replay in generic field modules. Code review
must still check causal input provenance and bounded loops; static checks do
not prove arbitrary Python is O(1). Global scheduling and diagnostics retain
their explicitly separate host costs.

| Reviewed path | Local bound | Separate host cost |
| --- | --- | --- |
| Generic disturbance local cycle | Fixed fields/types/rules and resident slots; up to six outgoing channels per record | Sparse scheduler and diagnostic totals grow with materialized nodes and packets |
| Diagnostics and rendering | Not a physical update; cannot feed state repairs | Full-state audits, histories and rendering are not O(1) |

The implementation therefore supports bounded local model work, not a claim that
the entire Python program or a full simulation tick is O(1).

The import-boundary audit resolves absolute and relative imports and rejects
runtime arithmetic in API assembly while allowing type annotations and literal
configuration; it is tested with both allowed and forbidden examples. Inputs and
expected outcomes are listed in `TEST_EXPECTATIONS.md`.

## Adding physical features

Follow [the physical-feature procedure](PHYSICAL_FEATURES.md) before adding a
law or state contract. It separates explicit local inputs, evolving state,
immutable parameters, derived values and model assembly. Dependencies between
physical inputs remain explicit; code separation does not imply statistical
independence. Formula-free assembly is checked for the public API assembly.

## Repository language

English is required for all repository comments, docstrings, documentation,
instructions, diagnostic messages and new identifiers. The authoritative rule
is [Repository language: English](../AGENTS.md#repository-language-english).
`tests/test_repository_language.py` guards against legacy non-English scripts;
review checks the actual language. Older branches must follow this rule when
merged. Mathematical notation remains valid. This affects documentation and
review, not physical laws.

## Standalone vector-lab experiment

The user-requested [tools/generic_vector_lab](../tools/generic_vector_lab/README.md)
is an opt-in mechanism experiment with its own explicit JSON laws. It does not
import, replace or extend the active engine or its schema. The lab runtime owns
its local transactions; its separate movie tool reads saved states. Generated
outputs go under artifacts and remain outside source commits. Its local quantum
coupling is a toy experiment of the lab alone; the repository's shared quantum
resource was deleted on 2026-09-17. The active source-of-truth boundaries above
remain unchanged.

## Causal event ledger, deleted on 2026-09-17

`core/event_space.py`, `core/event_links.py` and `tests/test_event_links.py`
were deleted on 2026-09-17 under issue #164 bucket B.4: all the information is
on the rays, the origin Node keeps nothing and there is no register
([Highlights 3.20](HIGHLIGHTS.md), the "Where is state stored" row of the
[ray/event model](RAY_EVENT_MODEL.md)). No engine, Node, packet, plan, pending
cycle or view carries an event identity, cursor, reference bank or cause;
`NodeEvents` only builds and publishes observer messages; the snapshot has no
`event_support`. `core/event_resolution.py` keeps the `Planner` protocol used
by the local planners and the resolver protocols, which no code implements.


### Local carrier scheduling and prepared ray laws

[Local Focus](LOCAL_FOCUS.md) defaults on. `core/plan_reuse.py` shares immutable
pure transition results through the host `NodeExecution` service with bounded
per-simulation caches. Full input equality is required; laws cannot read cache
state. Local commits, guards, model charges and timing remain Node-owned.
Event resolvers bypass reuse. `PortTable` indexes only
active transport banks and retains stable creation order; schedulers refresh
changed banks without adding callbacks or world references to PortBank.
The detailed limits, metrics and supercell boundary are in the Focus contract.

Local Focus owns a host address set and visit counters, never
physical history or a new per-Node state type. Nodes certify dormancy from fixed
local state; actual delivery wakes them. The spatial active index remains shared
by both scheduling modes. Frozen field definitions own bounded immutable phase
and pace tables prepared before any tick; no lazy pace cache grows across runs.
Retained-ray owners pass the same trusted pre-commit/receipt validation
boundary as outgoing payloads. No global reference enters initialization or
planner composition; the bond registry was deleted on 2026-09-17.

## Sampling admission ownership

`core/sampling_contract.py` owns immutable profile validation under the
[Detector-owned sampling contract](DETECTOR_SAMPLING.md). Generic field laws may
read these bounded configuration guards, which do not read world state, schedule
events or implement probability laws. Initialization and native adapters enforce
the same admission boundary. Historical mathematical samplers remain separately
scoped and are not Detector implementations.
