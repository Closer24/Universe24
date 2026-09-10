# Architecture and change boundaries

[AGENTS.md](../AGENTS.md) is the shared contributor entry point.
`POSTULATES_HE.md` is the plain-language conceptual entry point.
`SIMULATOR_DEFINITIONS.md` translates those principles into exact technical
requirements, and this document describes the code boundaries that enforce them.

## Dependency direction

| Module | Allowed dependencies |
| --- | --- |
| `core/state` | Standard-library data types |
| `core/contracts` | State types |
| `core/lattice` | State types and integer bounds |
| `core/engine` | State, lattice and local contracts |
| `fields/scalar` | Integer primitives and fixed vector types from `core/state` |
| `fields/policies` | Integer primitives and scalar samples |
| `dynamics/turning`, `dynamics/movement` | Integer primitives and fixed vector types from `core/state` |
| `models/current_field` | State, local contracts, generic fields and dynamics |
| `models/local_field` | Compatibility re-exports only |
| `api` | Engine and chosen candidate model |
| `diagnostics` | Read-only engine views, immutable events, rendering libraries |
| `scenarios`, `runner` | Public API and diagnostics |

The engine receives field and particle callables and an optional activity
predicate. `Simulation` assembles them from a scalar
field and a turning component through `CurrentFieldModel`. Callers can replace
either component independently with the keyword arguments `field=` and
`turning=`. `Engine` itself imports no field, dynamics, model, rendering or
file-writing module. No plugin registry or inheritance hierarchy is needed.
`PeriodicLattice` is the single implementation of periodic wrapping and the
six directional neighbors used for reads, activation and movement.

## Generic calculations and model choices

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
`CurrentFieldModel` constructs a `UnifiedFieldAction` from its selected response
and movement components once, then delegates the particle transition to it.
`dynamics/field_action.py` returns fixed response/motion records for the adapter
to map into particle/cell state. `dynamics/rate.py` owns the shared hop-rate
calculation for movement and linked travel; hop rate is not Euclidean speed.
`models/unified_field.py` identifies the full-vector candidate and selects its
response; `UnifiedSimulation` and `UnifiedLinkedSimulation` reuse the existing
API assembly, scheduling and record schemas with that response.
The reusable components never import `Config`, `CellState` or `ParticleState`.
Source multiplication, nonnegative clipping and scalar activity predicates live
in `fields/policies`; the adapter selects and calls them. Bounded scaling with a
carried remainder is implemented once in `core/state.scaled_divrem`, including
a bound on the product before adding a potentially cancelling remainder.

`CURRENT_MODEL` explicitly retains `value_changed_or_source` for exact v10
scheduling. Supplying `Simulation(field=...)` instead selects
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
requires a separately designed fixed-size state contract and corresponding
engine and diagnostic support. It is not enabled merely by passing a new law.
The practical extension guide is `FIELDS_HE.md`.

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

`Simulation` defaults to `NullObserver`, retaining no trace. `TraceRecorder` is
intended for small tests or old notebooks; its memory grows with history.
`JsonlRecorder` writes events immediately and does not retain them. Rendering
frames live only in the runner. `--frame-stride` controls their sampling cost.
The engine never reads an observer result. Observers are trusted application
code, not a security sandbox; an observer exception during a tick stops the world.

The default runner and test-report view captures independent `VolumeFrame` records
with full XYZ coordinates and renders at 1500×1275. `--view-2d` or `volume=False`
explicitly selects a plane slice. The authoritative output rule is in
`SIMULATOR_DEFINITIONS.md`.
The volume renderer shows nonzero scalar cells, sampled particle trails and
momentum arrows with a rotating camera. Plane and volume renderers share one
GIF/HTML output function. Camera rotation, color and marker scaling are purely
diagnostic; they do not change the engine or particle motion.

Sparse world storage is distinct from constant-size physical state. Existing
materialized cells and occupancy-address order are retained for exact legacy
equivalence. Reclaiming them is a separate scheduler change requiring the same
differential checks. This refactor does not claim constant total memory or
worst-case constant-time Python dictionary operations.

## Verification scope

The frozen reference has SHA-256
`822f62ac790c0b8477ed634d24454774152bcba8fb3322a53d039c251376163f`.
It is loaded only by tests. The three primary experiments compare every physical
record, active frontier, occupancy and history after every tick, for 278 ticks
in total (120 stationary, 48 contact, 110 turning).

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
Inputs and expected outcomes are listed in `TEST_EXPECTATIONS_HE.md`.

Stricter input checks and exception atomicity are intentional boundary fixes.
They can reject invalid inputs that old code accepted. They do not alter the
successful regression trajectories. Preserved model limitations are listed in
`SIMULATOR_DEFINITIONS.md`; an architecture cleanup does not establish new physics.


## Local-link candidate (v11)

`LinkedSimulation` / CLI `--scenario links` explicitly selects
`scalar-field-v11-local-links`. `Simulation` and its frozen-v10 differential
checks retain the previous model. This is a new geometry/transport hypothesis,
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
