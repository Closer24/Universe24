# Architecture and change boundaries

`entities.py` owns host-only compilation of selected explicit catalog profiles
into ordinary initialization; it delegates strict JSON and runtime schema
validation to `initialization.py`. Profiles contain their candidate operations.
It adds no runtime species lookup. See [entity catalog](ENTITY_CATALOG.md).
Optional two-record type conversion follows the existing frozen pair proposal
and delayed engine commit; its ownership restrictions are in
[local conversions](LOCAL_CONVERSIONS.md).

## Generated output ownership

`retention.py` owns host-only artifact registration, writer leases and expiry.
Runners own complete fresh output directories; the workspace owns exact input,
log and export files and declares the child-output dependency for companions.
Cleanup uses recorded filesystem generations and operating-system locks, with
recoverable quarantine before removal. The module never imports or changes
physical engine state. Its one-shot and singleton watcher interfaces share the
[same retention contract](RETENTION.md).

## Active generic ownership

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
cross-layer checks live in `tests/test_generic_identity.py`. Genericity is scoped
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
packets; `disturbance_api.py` composes its planner without formulas. The shared
engine combines diagnostics and costs while retaining separate field and
carrier clocks. See [SPATIAL_FIELDS.md](SPATIAL_FIELDS.md) for the contract and
the remaining self-attribution requirement. `fields/spatial_coupling.py` owns
local sampling, fractional exchange, exact quarter-turn rotation and reaction
allocation. The injected `SpatialCoupler` protocol keeps those calculations out
of engine scheduling. Carrier and field owners validate together before committing
the response; fixed sample registers and departure timestamps prevent future
reads or edits to old in-flight packets. See [SPATIAL_COUPLINGS.md](SPATIAL_COUPLINGS.md).

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

The remaining scalar, stream, linked, collision and balanced sections describe
explicitly named research APIs. Their record layouts, extension points, tick
orders and acceptance limits remain scoped to those candidates.

## Causal-stream candidate extension

`fields/streaming.py` owns bounded pure octant splitting and delivered-flux
selection. `core/streams.py` owns the fourteen-register stream records and
one-edge packet routing; its full-state validation is a read-only host audit.
`core/streaming_engine.py` schedules that phase before the existing local
particle update. `models/causal_stream.py` selects full-vector response and
ordinary movement through `CurrentFieldModel`; `api.CausalStreamSimulation`
assembles them. No field law receives an Engine or mutable source history.
The ordinary scalar seeding interface is rejected for this distinct state type.
The existing scalar and linked candidates retain their own implementations.

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
| Executable code and model selection | [src/event_universe](../src/event_universe/) | Keep shared formulas generic; models select them |
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
| `core/state` | Standard-library data types and `core/integer` |
| `core/disturbance_state` | Bounded arithmetic and immutable generic definitions |
| `core/disturbance_engine` | Generic records, local planner interface, scheduling and ownership |
| `fields/disturbances` | Generic records and bounded integer arithmetic; no world or diagnostics |
| `initialization` | JSON input and generic typed definitions; no arbitrary execution |
| `core/contracts` | State types |
| `core/lattice` | State types and integer bounds |
| `core/engine` | State, lattice and local contracts |
| `fields/scalar` | Integer primitives and fixed vector types from `core/state` |
| `fields/policies` | Integer primitives and scalar samples |
| `dynamics/turning`, `dynamics/movement` | Integer primitives and fixed vector types from `core/state` |
| `models/current_field` | State, local contracts, generic fields and dynamics |
| `models/local_field` | Compatibility re-exports only |
| `disturbance_api` | Generic engine and disturbance local law |
| `api` | Historical engine and explicitly chosen research model |
| `diagnostics` | Read-only engine views, immutable events, rendering libraries |
| `runner` | Generic public API, initialization and optional diagnostics |
| `ui` | Local HTTP, strict initialization validation and isolated CLI process ownership |
| `scenarios`, `legacy_runner` | Historical public APIs and optional diagnostics |

The historical scalar engine receives field and particle callables and an optional activity
predicate. `ScalarSimulation` assembles them from a scalar
field and a turning component through `CurrentFieldModel`. Callers can replace
either component independently with the keyword arguments `field=` and
`turning=`. `Engine` itself imports no field, dynamics, model, rendering or
file-writing module. No plugin registry or inheritance hierarchy is needed.
`PeriodicLattice` is the single implementation of periodic wrapping and the
six directional neighbors used for reads, activation and movement.

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

## Generic calculations and model choices

`core/integer.py` owns shared decoded component addition/subtraction, ordered
sums, dot/cross products and nonnegative ceiling division. Products and ordered
partial sums retain their working-register checks, including overflow before
cancellation. Ceiling division retains the existing adjusted-numerator bound;
`signed_divrem` instead rounds toward zero and returns a signed remainder.
Callers supply schema-bounded components and retain payload encoding, field
validation, operation pricing and atomic commit ownership. The expression
interpreter delegates arithmetic while retaining broadcasting and AST costs.
See [shared arithmetic tests](../tests/test_integer_arithmetic.py).

`ScalarFieldRule.advance(sample, neighbors, source=..., denominator=...)`
returns a `ScalarSample(value, remainder)`. The built-in `ScalarField` implements
one weighted six-neighbor stencil, with optional local retention. It supports
signed values and retains integer division residues. It knows neither source
occupancy nor particle or cell records. A different local scalar law can satisfy
the same protocol without inheriting from it.

`FieldTurning.apply(...)` takes particle momentum, field momentum, a supplied
local vector and carried residues. The selected direction function receives
only momentum and that vector. The component performs the bounded impulse
calculation and equal-and-opposite exchange once, regardless of the selected
direction policy. It does not compute or store a field, or interpret cell state.
`full_response` and `dominant_axis_transverse` are available policies; neither is
an implicit default. The transverse policy is a discrete dominant-axis filter,
not a geometric rotation or orthogonal projection.

`CurrentFieldModel` is the single adapter for the existing physical state. It
maps occupancy to source strength, enforces the current nonnegative scalar
policy, obtains a gradient, calls turning and movement, and builds validated
cell and particle proposals. `CURRENT_MODEL` explicitly selects six unit
neighbor weights, no local retention and dominant-axis transverse response.
Denominators come from `Config` so arithmetic and state audits share one value.
The reusable components never import `Config`, `CellState` or `ParticleState`.
Source multiplication, nonnegative clipping and scalar activity predicates live
in `fields/policies`; the adapter selects and calls them. Bounded scaling with a
carried remainder is implemented once in `core/state.scaled_divrem`, including
a bound on the product before adding a potentially cancelling remainder.

`CURRENT_MODEL` explicitly retains `value_changed_or_source` for exact v10
scheduling. Supplying `ScalarSimulation(field=...)` instead selects
`sample_changed_or_source`, which also tracks remainder-only evolution. Callers
can override either choice with `field_activity=`. The engine validates the
boolean result before committing any field proposal. Direct `Engine` callers
that omit an activity predicate conservatively retain every visited cell.
Custom scalar laws must preserve a zero sample with zero neighbors and zero
source; this is the quiescent state assumed by sparse scheduling. They must not
depend on an unstated time input or on private evolving state.

These extension points preserve the current five-register scalar cell schema.
A signed field can be calculated by the generic primitive, but the current
adapter clamps negative results. A vector field or several simultaneous fields
requires another schema rather than a replacement scalar callable. The active
disturbance engine supplies that separate fixed-size multi-field contract; this
historical adapter remains scalar-only.
The practical extension guide is `FIELDS.md`.

## Local contracts

`update_field(cell, six_neighbor_values, source_count, config)` returns one new
five-field cell record. `update_particle(particle, cell, six_neighbor_values,
config, tick)` returns new particle and field records, a hop direction, gradient
and impulse. Their inputs are immutable and their output size is fixed.

The engine owns position changes. A candidate must not change position in its
proposal, may request only one cardinal direction, and must mark the tick.
The current law computes both sides of the local momentum exchange and validates
them before returning. Contract tests must accompany another candidate law.
Custom field laws and direction functions are trusted deterministic local code;
they must use bounded integer arithmetic and retain no evolving private state.

Public mappings contain immutable named tuples and are read-only views. These
views reflect future engine updates, so they are not snapshots. `capture_frame`
creates independent diagnostic copies; changing a frame cannot change physics.

## Tick order

1. Check that the world is healthy and the next tick fits its register.
2. Build the sparse field work set from the previous active frontier and neighbors.
3. Read all old scalar values before computing any new scalar values.
4. Compute and validate all field proposals, then commit them together.
5. Snapshot occupancy-address order; visit each address and its fixed slots.
6. For each particle not yet updated this tick, compute and validate a local
   particle-field proposal, commit it, then attempt the requested hop.
7. Emit immutable force/move/blocked records after their corresponding commits.
8. Increment the tick. New occupancy becomes the source for the next field phase.

Steps 5–6 preserve first-insertion and slot ordering from v10. Contended moves
are not claimed to be permutation-invariant. There is no hidden global repair
phase. `last_update_tick` prevents a moved particle from receiving another
update when its target address appears later in the occupancy snapshot.

An event is stamped with the tick being processed. A frame captured after the
step is stamped with the incremented tick. Thus an impulse recorded at event
tick 15 is first visible in completed frame 16; this convention is unchanged.

## Recording and resources

`ScalarSimulation` defaults to `NullObserver`, retaining no trace. `TraceRecorder` is
intended for small tests or old notebooks; its memory grows with history.
`JsonlRecorder` writes events immediately and does not retain them. Rendering
frames live only in the runner. `--frame-stride` controls their sampling cost.
The engine never reads an observer result. Observers are trusted application
code, not a security sandbox; an observer exception during a tick stops the world.

Run and test visualization is opt-in. When explicitly requested for a historical
scalar run, the renderer captures independent `VolumeFrame` records with full XYZ
coordinates and renders at 1500×1275; `volume=False` chooses a plane slice.
The authoritative headless/default output rule is in `SIMULATOR_DEFINITIONS.md`.
The volume renderer shows nonzero scalar cells, sampled particle trails and
momentum arrows with a rotating camera. Plane and volume renderers share one
GIF/HTML output function. Camera rotation, color and marker scaling are purely
diagnostic; they do not change the engine or particle motion.

With visualization enabled, the historical runner captures only the selected
view. A capture may receive momentum already measured from that same state;
otherwise it measures the state itself.
Every completed tick still gets its momentum acceptance check, including ticks
without a saved frame. A failed step is captured with a fresh measurement because
its partially committed state can change without advancing the tick counter.

The volume renderer retains static axes, grid and compass artists between frames
and extends diagnostic trail history incrementally. It resets that history when
playback seeks backward or the domain changes. Dynamic artists are replaced for
each frame, preserving the existing draw order and camera. The shared Pillow
writer copies the Agg canvas already drawn by FuncAnimation and encodes the
non-looping GIF once. Custom savefig backgrounds or transparency use savefig to
preserve their rendering semantics. See [PERFORMANCE.md](PERFORMANCE.md).

`diagnostics/live.py` owns disposable historical preview coordination.
`legacy_runner` enables it only with explicit `--live` or API `live=True`, which
also enables recorded visualization. Ordinary generic and historical runs are headless.
The parent alone steps the Engine, copies and retains every canonical frame,
and records events. Before nonblocking queue submission, the
preview serializes the copied frame, preventing later producer mutation from
reaching the consumer. A spawned process receives only serialized frames and
display configuration. Its queue holds one waiting snapshot and its trail window
holds at most eight; intermediate preview messages may be coalesced.

The worker uses the same volume/slice scene builders to publish the latest PNG
inside an atomically replaced `live.html`. Its scales are provisional because
future extrema are not yet known. An integer meta-refresh interval supports
ordinary local-file browsers without a server. After computation, the parent
signals a separate stop event, reaps the worker with bounded waits, and closes
queues without waiting for an abandoned feeder. Only then does the canonical
renderer publish selected already-drawn rasters through a read-only callback.
This preserves one live-page writer and avoids recomputing final frames.

Final GIF/HTML still uses the entire retained history and unchanged fixed scales.
Preview failures warn without changing physical stepping or canonical export;
physical failures keep their original exception and failed report. A final redirect
is registered only for the current run's successfully written artifact, preserving
failure status and avoiding a stale report left by an earlier run. Preview work,
IPC and page updates are host costs, not part of the physical model.

Sparse world storage is distinct from constant-size physical state. Existing
materialized cells and occupancy-address order are retained for exact legacy
equivalence. Reclaiming them is a separate scheduler change requiring physical
contract checks. This refactor does not claim constant total memory or
worst-case constant-time Python dictionary operations.

## Opt-in quantum ownership — Q-ORACLE-1

The `deferred-unit-cost-oracle-v1` assumption is defined in POSTULATES.md and its
numeric, timing and resource contracts in SIMULATOR_DEFINITIONS.md. The feature
contract and limits are in [QUANTUM_DETECTOR_TRIAL.md](QUANTUM_DETECTOR_TRIAL.md).
The existing physical engines and schemas above are unchanged.

| Module | Responsibility and allowed dependencies |
| --- | --- |
| `quantum/state`, `quantum/query`, `quantum/terminal` | Fixed records and bounded integer helpers; may use core.state, never an engine |
| `quantum/deferred` | Sole owner of deferred history, cache, accounting and one terminal result |
| `integration/quantum_bridge` | Sole production adapter between spacetime references and quantum APIs; no Engine or write callback |
| `tests/quantum_detector_fixture` | Test-only controller with one detector-event slot and two detector bits |

Physical modules, models, application assembly and diagnostics must not import
quantum. Quantum must not import physical engines, models, dynamics, fields,
diagnostics or integration. Shared bounded arithmetic from core.state is allowed.
The architecture tests reuse the existing import resolver and cover relative,
member and aliased imports. They are static guards, not a sandbox against dynamic
Python. The bridge does not duplicate evaluation or maintain another quantum cache.

Queries are explicit, not automatically polled. Only DeferredQuantum evaluates
histories or chooses the terminal output. Replies are immutable. The test
controller records that result without writing CellState, ParticleState, time or
Engine events. A future native physical commit needs an explicit engine contract;
it cannot be added by turning a diagnostic observer into a second state owner.

### Selected joint-state event backend

`DeferredQuantum.bind_event_network` composes the selected finite backend from
`quantum/event_network.py`. That module owns the per-cell heads, immutable event
DAG, conditional-record closure and exact host checkpoints. `quantum/event_rules.py`
owns generic bounded local matrix validation/evaluation. It does not infer a
physical law from a name. The existing scalar-expression backend is preserved;
an owner cannot mix the two representations or silently switch a live history.

`integration/quantum_event_trial.py` is an explicit headless test controller, not
an Engine adapter. It supplies example matrices and one externally supplied
integer ticket. Native disturbance schemas, scheduling, fields and momentum
updates are unchanged. The existing quantum import boundary applies to the new
modules. Host full-state inspection and controller-conditioned weights are not
local physical observables. See [QUANTUM_EVENTS.md](QUANTUM_EVENTS.md) for the
selected contract and [TEST_EXPECTATIONS.md](TEST_EXPECTATIONS.md) for its tests.

## Verification scope

LOCALITY-1 in SIMULATOR_DEFINITIONS.md governs the complete dependency path of
every non-quantum physical update, including self-field inputs. Shadow/reference
computations cannot be hidden behind a local adapter. `test_locality.py` checks
exactly six baseline neighbor reads independent of world extent and rejects
known world access and replay in field, dynamics and model modules. Code review
must still check causal input provenance and bounded loops; static checks do
not prove arbitrary Python is O(1). Global scheduling and diagnostics retain
their explicitly separate host costs.

| Reviewed path | Local bound | Separate host cost |
| --- | --- | --- |
| Generic disturbance local cycle | Fixed fields/types/rules and resident slots; up to six outgoing channels per record | Sparse scheduler and diagnostic totals grow with materialized cells and packets |
| Baseline scalar update | Six neighbor samples, five cell registers and at most K source slots | Work/frontier sweeps grow with visited cells |
| Field response and movement | Three vector components; one hop request; at most K destination slots | Occupancy-address scheduling grows with retained addresses |
| One cell's particle phase | At most K particles, each with at most K slot work | K is fixed; no all-source search supplies force inputs |
| Link transport and geometry | Six ports per cell, one packet per port, at most two delivered proposals per edge | `advance` visits materialized link cells |
| Matter transit | Four integers per in-flight particle; one neighbor destination | Tick scheduling visits in-flight particles |
| Diagnostics and rendering | Not a physical update; cannot feed state repairs | Full-state audits, histories and rendering are not O(1) |

The implementation therefore supports bounded local model work, not a claim that
the entire non-quantum Python program or a full simulation tick is O(1).

The archived frozen reference has SHA-256
`822f62ac790c0b8477ed634d24454774152bcba8fb3322a53d039c251376163f`.
It was used for historical tick-by-tick comparisons, totaling 278 ticks
(120 stationary, 48 contact, 110 turning). It is no longer imported or executed
by the suite. Current physical regression coverage is described in
[TEST_EXPECTATIONS.md](TEST_EXPECTATIONS.md).

Generic unit tests cover weighted and signed scalar values, exact fractional
response, selectable directions and overflow on both sides of an exchange.
`test_current_field.py` pins the current model's source, clipping and transverse
response choices. `test_field_composition.py` injects a distinct source-only law
and full-vector response through the public API, verifies their observed
behavior and local conservation, and rejects an invalid law before commit.
These alternative laws are test fixtures, not a newly adopted physical model.
The numeric audit and import-boundary tests include both new generic packages.
The boundary audit resolves absolute and relative imports and rejects runtime
arithmetic in model assembly, API assembly and compatibility facades, while
allowing type annotations and literal configuration. It is tested with both
allowed and forbidden examples. Dedicated tests also cover periodic lattice
geometry, scalar policies, digital movement and each diagnostic projection.
Inputs and expected outcomes are listed in `TEST_EXPECTATIONS.md`.

Stricter input checks and exception atomicity are intentional boundary fixes.
They can reject invalid inputs that old code accepted. They do not alter the
successful regression trajectories. Preserved model limitations are listed in
`SIMULATOR_DEFINITIONS.md`; an architecture cleanup does not establish new physics.


## Local-link candidate (v11)

`LinkedSimulation` / historical CLI `--scenario links` explicitly selects
`scalar-field-v11-local-links`. `ScalarSimulation` retains the previous model and its
physical behavior checks. This is a new geometry/transport hypothesis,
not an architecture-only change to the baseline.

| Module | Responsibility |
| --- | --- |
| `fields/geometry.py` | Reusable bounded integer mean-to-length mapping |
| `dynamics/transit.py` | Reusable departure selection and per-edge travel time |
| `core/links.py` | Fixed six-port records, ownership, old-message delivery and commits |
| `core/linked_engine.py` | Scheduling transport around the existing field/particle engine |
| `models/linked_field.py` | Select the candidate components and identify the model |
| `api.LinkedSimulation` | Assemble the engine; inject the symmetric merge policy |

The existing model adapter accepts a `MovementRule`; it still contains no
independent arithmetic. Linked movement selects direction at departure and
schedules an integer arrival. Its motion and scalar inputs use delivered local
mailboxes. `Engine` adds extension hooks without copying its occupancy, local
impulse exchange, record validation or observer logic.

Each cell owns its three positive edges. The opposite endpoint keeps a copy of
the active length. Ownership is storage identity, not a privileged physical
source. Either endpoint sends a proposed length on the current edge. At expiry,
both ends know that delivered proposal: the sender from its own old timer,
the receiver from its incoming packet. If two proposals arrive on the same edge
in the same tick, the candidate selects their maximum. This commutative merge is
injected; it is a candidate choice, not a derived gravity equation.

The host collects at most two proposals per edge and commits the two endpoint
records together. This is equivalent to each endpoint merging its own expired
proposal and the opposite incoming proposal. No global measurement, remote
source lookup or global repair supplies a value. Subsequent communication uses
the committed length; packets and particles already in flight retain theirs.

Tick order: complete due matter transits, deliver old port packets, compute and
commit fields from delivered inboxes, publish changed values/proposals, then
run the existing local particle-field exchange for particles ready to depart.
No field/particle rule reads current remote scalar registers. Sequential
capacity conflict resolution is inherited from the baseline and is not a claim
of full parallel particle scheduling. In-flight particles remain resident
sources and do not receive new impulses until arrival. This is explicit model
behavior, not continuous geodesic integration.

A materialized cell adds exactly 30 integer link registers to its five scalar
registers. Each in-flight particle adds four integer registers, bounded by K
resident slots per cell. Dictionary storage and full work-set iteration remain
host costs, not strict worst-case O(1). There is no per-source field map or
unbounded local message queue. Busy channels retain one snapshot; intermediate
versions are coalesced to the current cell value after delivery.


## Adding physical features

Follow [the physical-feature procedure](PHYSICAL_FEATURES.md) before adding a
law or state contract. It separates explicit local inputs, evolving state,
immutable parameters, derived values and model assembly. Dependencies between
physical inputs remain explicit; code separation does not imply statistical
independence. Formula-free assembly is checked for every module beneath
`models/`, including future and nested models, rather than a fixed name list.

### Audit against main e74f2fd

- `ScalarField.advance` receives samples, six neighbors, source and denominator;
  it does not import model state or the world.
- `FieldTurning.apply` receives momenta, a vector, residues and rational coupling;
  direction selection is injected. Local exchange is implemented once.
- `MeanStretch` stores immutable coefficients and receives two local samples.
  Its caller supplies already delivered neighbor information.
- `CurrentFieldModel` extracts values from physical records, invokes the generic
  laws and constructs proposals. The engine owns the subsequent commits.
- API assembly independently accepts field, turning and (for linked worlds)
  length policies. Tests exercise alternate laws and numerical parameter changes.
- The baseline fixed state does not accept arbitrary vector/multiple-field
  records. Such an extension needs a new explicit contract and diagnostic support.

These are code and tested-contract findings, not a proof of every possible
plugin's locality or physical correctness. Dynamic imports, arbitrary callbacks
and hidden external state still require review; the static gate is not a sandbox.

## Repository language

English is required for all repository comments, docstrings, documentation,
instructions, diagnostic messages and new identifiers. The authoritative rule
is [Repository language: English](../AGENTS.md#repository-language-english).
`tests/test_repository_language.py` guards against legacy non-English scripts;
review checks the actual language. Older branches must follow this rule when
merged. Mathematical notation remains valid. This affects documentation and
review, not physical laws.

### Run acceptance diagnostics

`diagnostics/invariants.py` compares immutable momentum values and raises on an
isolated-motion violation. The runner establishes the initial applicability
(single particle and zero field records), calls the check each tick before frame
sampling, and uses the existing failure-output pipeline. No check result is fed
back into a physical law to repair state. The engine remains separate from this
application-level acceptance policy.

## Massive point-contact extension

The user-authorized v13 contract is in SIMULATOR_DEFINITIONS.md. Shared integer
ratio reduction stays in core/state (a fixed 128-step bound, no numeric imports).
`dynamics/collision.py` accepts only two fixed CollisionBody records and implements
the elastic law once. `models/collisions.py` selects it and maps records without
arithmetic. Engine receives the callable, resolves co-resident fixed slots,
validates both output records and commits the pair before notifying observers.

The original particle schema appends four integers; defaults preserve every
legacy trajectory. Mass remains constant. Momentum and movement-credit
numerators have explicit denominator owners. Generic movement, turning and
transit accept these independent inputs without a Config or world reference.
Neither diagnostics nor the optional quantum bridge feeds the collision law.
Contact state is at most K*K flags per contacted address. Each local sweep has
at most K(K-1)/2 pair candidates; sparse world iteration is a separate host cost.

Historical frozen comparisons projected the original twelve fields and checked
the four appended defaults. Current fixed-schema, numeric and behavior tests
cover the active records without requiring equality to the archived engine.

## Opt-in balanced motion and local halo

`ScalarSimulation(movement=..., post_motion_halo=...)` passes generic local components
to the existing adapter and engine. `BalancedSimulation` selects
`advance_balanced_movement` and the current model's scalar-halo adapter. Movement
remains in `dynamics/`; the scalar transformation remains in `fields/`; the model
maps fixed records; the engine alone schedules the old/current six-neighbor union
after all particle responses. No core schema changes. The law and evidence are
documented in [BALANCED_MOTION.md](BALANCED_MOTION.md).

## Shared native event extension

The [native event contract](NATIVE_QUANTUM_EVENTS.md) adds a domain-neutral causal
ledger and local resolver protocol under core. The integration owner composes
quantum payloads, initialization-selected instruments and classical control codes.
Only primary API assembly and initialization reference that integration owner;
core and ordinary field arithmetic never import quantum.
