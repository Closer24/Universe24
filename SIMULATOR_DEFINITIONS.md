# Event Universe — active modular 3D integer simulator

## Active generic disturbance model

The primary API is `Simulation(initial: InitialState)`. An initialization JSON
file supplies every field/type name, seed, allowed local expression, coupling,
transport rule and cost setting. The engine has no hardcoded interpretation of
mass, charge, velocity or other user-defined physical names. Missing initialization
does not select a scalar model.

[docs/DISTURBANCES.md](docs/DISTURBANCES.md) is the authoritative active schema
and transition contract: bounded scalar/vector payloads, whole-record or extensive
transport, atomic local exchange, explicit sources, fixed link transit, local
computation delay without debt, capacity failures and headless output.

Optional [spatial fields](docs/SPATIAL_FIELDS.md) add initialization-defined
baselines, continuous external emission and fixed-clock outward octant transport.
Their six delivered channels preserve travel direction; eight internal sign
classes prevent reversal of an emitted branch. The document specifies source
cadence, bounded residual ownership, cost coupling and periodic/self-field limits.

Optional [spatial couplings](docs/SPATIAL_COUPLINGS.md) add same-field atomic
exchange and discrete norm-preserving rotation, driven by local values or scalar
directional flux. Samples precede fresh emission; a delayed carrier proposal
commits its equal-and-opposite spatial reaction with the carrier. The response
contract defines same-timestamp packet preparation, fixed local cost and the
restricted straight-line isolation result without general source attribution.

Schema version 1 retains those conservative spatial laws. Schema version 2
selects the explicit `finite-dissipative-v1` policy, derived from the schema
version independently of user-defined names. Every spatial field requires a
bounded integer ratio `0 <= p < q`; each original packet/octant/component is
attenuated to `sign(v) * floor(abs(v) * p / q)` on completing an interior link,
before arrival packets merge. Removed fractions are intentionally not retained.
Immutable baselines are exempt. Per-record finite allowances bound absolute
emission and opposite coupling reactions; they are not physical reservoirs.
The complete laws belong to [spatial fields](docs/SPATIAL_FIELDS.md) and
[spatial response](docs/SPATIAL_COUPLINGS.md).

The version 2 combined balance is initial inventory plus committed sources minus
committed signed dissipation and escaped quantity. Integer attenuation can change vector direction and does not
preserve momentum or energy. Coupling remains equal-and-opposite at its atomic
commit, before subsequent propagation loss. Fixed finite initial records and
allowances bound dynamic input; after the last nonzero input, dynamic spatial
stock vanishes after finitely many links. This does not require carriers to stop
or immutable backgrounds to disappear. Schema 1 rejects the new decay and budget
keys, and named historical research models retain their own integer rules.

The optional initialization `boundary` is `periodic` by default or `open`.
Periodic topology wraps independently across all six faces, preserving port,
vector, full link time and ownership. Open terminal packets remain counted while
in flight, then their unchanged payloads leave the simulation at link completion.
There is no simulated outside receiver, decay or receive cost. The boundary law
is independent of schema version and named in metadata. Combined accounting is
`current + dissipated + escaped = initial + sources`; spatial-only accounting
also includes committed opposite reactions. The escaped ledger is diagnostic,
never a global repair or a physical input. See [the schema](docs/DISTURBANCES.md).

Optional atomic pair `interactions` assign multiple fields from one frozen input
pair, enforce each declared invariant and conserved-field pair balance, then
enter the existing delayed local commit together. Generic integer dot products,
matrix transforms and scalar comparisons are initialization operations. Exact
division cannot round away a failed invariant. The configured unequal-mass
elastic example and its limits are specified in the disturbance contract; they
do not change the historical collision laws below or introduce a built-in force.

The source/self-force, scalar cell, particle, turning, variable-link and collision
laws below remain requirements of explicitly named research APIs. They do not
define the active generic schema. Shared locality, integer bounds, read-only
diagnostics and honest failure reporting still apply across applicable models.

## Opt-in causal outward streams

`CausalStreamSimulation` selects `causal-octant-stream-v1`. It replaces scalar
transport with exactly fourteen nonnegative bounded integers per stream cell:
eight octant populations and six delivered directional amounts. Ordinary cell
momentum registers remain the local exchange ledger. Stream records contain no
source identities or histories. Each update reads one old population record and
at most K local resident slots, produces six fixed eight-integer packets, and
each destination combines at most six packets. This is bounded local work;
the host sparse sweep and aggregate storage are not constant in world size.

Every old population is validated before adding the local source. Emission and
one-edge delivery complete before the particle response and movement. Octant
signs never change, so the stream travels monotonically away from its emission
point in the unwrapped Manhattan metric. Before periodic return it is ahead of
its emitting particle at each response. No isolation-count branch or cancellation
of a calculated force is used. A scalar `seed_field` call is rejected: no law
converting one scalar into directional streams has been specified.

The model uses full-vector response to the reversed locally delivered flux,
with the existing bounded impulse exchange and movement. `source_per_octant`
is an explicit independent strength. The three-tick integer branching phase
is anisotropic. Periodic return, radial falloff, energy conservation and physical
field-momentum transport are not established by the free-space self-force proof.
See [the candidate contract](docs/CAUSAL_STREAM_FIELD.md).

The canonical implementation is the `event_universe` Python package under `src/`.
`persistent_source_field.py` is a compatibility facade, with no copied physical law.
The historical scalar model identifier is `scalar-field-v10-contact`.
The active generic user identity is supplied by initialization; its schema version
separately identifies conservative or finite dissipative spatial policy.
The plain-language conceptual source is `POSTULATES.md`. If its wording is
ambiguous, this file defines the executable technical requirement. A deliberate
change to a postulate must update both files and the relevant regression tests.

## Spatial-causal consistency postulate

Every location must be consistent with all information that could already have
reached it through causal neighbor links. A location is not required to reflect
a remote event before that event's influence arrives. Global consistency must
emerge from consistent local transitions; the engine may not broadcast a remote
change, rewrite a completed event, or repair the world globally after a step.

The present implementation enforces the local information boundary and one-edge
field propagation. It does not yet establish quantum consistency or entanglement.

## Hard physical constraints

The numbered record/source/response constraints here describe the historical
scalar models selected through ScalarSimulation and related named APIs. Their
five-register cell and sixteen-register particle schema is not universal. The
active generic state and its smaller payload bound are defined in
[the disturbance contract](docs/DISTURBANCES.md).

1. All dynamic physical registers and arithmetic are integers. No floats, true
   division, trigonometry, square roots, logarithms or vector normalization occur
   in `core/`, `fields/`, `dynamics/` or `models/`. Rational factors use integer numerators, denominators
   and retained integer remainders.
2. Physical registers are bounded to `[-2147483647, 2147483647]`. Intermediate
   working registers are bounded to `[-9223372036854775807, 9223372036854775807]`.
   Exceeding a bound raises `OverflowError`; neither wraparound nor saturation is
   used. Python is the host representation, with explicit bounds at the model
   and commit boundaries; arbitrary precision is not an escape for physical state.
3. A cell contains exactly five integer fields:
   `phi, px, py, pz, remainder`.
4. A particle contains exactly sixteen integer fields:
   `x, y, z, px, py, pz, move_budget, axis_phase, force_rx, force_ry, force_rz,
   last_update_tick, mass, momentum_den, move_budget_den, last_collision_tick`.
   The v13 section below defines the four appended registers and their defaults.
5. The physical neighborhood is exactly `+x, -x, +y, -y, +z, -z`.
   Each local rule receives only fixed records and six neighbor values.
6. Every occupied cell has exactly `K = max_particles_per_cell` slots, with
   `-1` denoting an empty slot. K is fixed for a world. No source maps, growing
   histories or dynamically expanding particle lists are stored per cell.
7. A source persists by occupancy. The model never repeatedly adds its own
   emission to an accumulated source history.
8. A scalar-field change traverses at most one neighbor edge per synchronous
   field update. Movement is also limited to at most one neighbor per tick.
   No special slow-speed law is introduced.
9. An isolated stationary source must have equal values on opposite sides of
   every coordinate axis and zero net self-force.
10. A particle impulse is paired with the exact opposite field impulse in the
    same local proposal. Both records must be valid before either is committed.
    Global momentum measurements are diagnostic only; no later global correction
    is permitted.

## Engine, candidate model and measurements

The engine owns addresses, fixed occupancy, scheduling and commits. Generic
`fields/` code owns scalar arithmetic and gradients; generic `dynamics/` code
owns the shared response, local momentum exchange and movement calculations.
`models/current_field.py` selects their policies and maps them to physical
records: six equal neighbor weights, no local retention, occupancy-based source,
nonnegative scalar values and dominant-axis transverse response. No copied
formulas are maintained in the adapter or compatibility imports.
Source scaling and range/activity policies are reusable functions in
`fields/policies.py`. `core/lattice.py` owns all periodic neighbor geometry.
Model, API and compatibility assembly are checked for accidental runtime
arithmetic, alongside absolute and relative import boundaries.

The field and turning components can be supplied independently to `ScalarSimulation`.
Their denominators come from the same `Config` used by state audits. A scalar
replacement must fit the existing fixed cell schema; vector or multiple-field
state needs a separate explicit contract. Custom implementations must be local,
deterministic, bounded and without evolving private state. Measurement code
reads output and records evidence. No local law receives a world object or
knows source identities at remote cells.

The engine receives field activity as a predicate instead of interpreting the
candidate law's changes itself. The historical scalar model explicitly retains its legacy
value-based predicate. An injected scalar law tracks changes to both value and
remainder unless `field_activity=` is supplied. A law must preserve the all-zero
sample when neighbors and source are zero, as required by sparse scheduling.
With no predicate, direct `Engine` callers retain all visited cells.

No gravitational attraction law, Newton/Einstein equation, future path search or
unproven physical identification is added as part of architecture maintenance.
When testing a new physical hypothesis, use a separately identified candidate
law and a separate change; preserve the old result, including failures.

## Parameters and known model assumptions

Defaults: dimensions `240 × 240 × 240`, `c_units=1000`, `source_strength=64`,
`field_den=7`, `force_num=1`, `force_den=64`, `K=4`.

These are explicit model choices. The contact demonstration uses `force_den=1`;
the turning regression uses `force_den=12`. Those scenarios do not replace the
default coupling. An impulse smaller than one integer unit accumulates as a
remainder, so nonzero field contact need not produce an immediate integer turn
at every denominator.

The current turning law removes the gradient along the dominant momentum axis.
Ties prefer x, then y, then z. The digital hop sequence also orders axes. Full
rotational invariance, arbitrary diagonal self-force cancellation and energy
conservation are not established. Coordinate-plane regressions do not prove all
lattice symmetries. Field-momentum storage is the existing local exchange model;
there is no new field-momentum transport or quantum dynamics in this refactor.

The scalar field is synchronous; particle movement is sequential. Occupancy
addresses are visited in their first-insertion order, then slot order. The first
available target slot is used. A full target blocks the move and consumes that
tick's movement budget. This is a blocked movement record, not a physical
scattering law. Changing conflict resolution or moving all particles
simultaneously would change the model and requires separate evaluation.

## Complexity accounting

### LOCALITY-1: end-to-end local physics

Every physical update, including a self-field estimator or subtraction, may use
only its fixed local records and six causally available neighbor records. For
fixed K and fixed-width integers, its work and stored state must be O(1) with
respect to world size, source count, elapsed ticks and traveled distance.
Each dependency must satisfy this rule end-to-end, not only the final arithmetic.

Forbidden physical dependencies include shadow worlds, per-source field maps,
trajectory replay, expanding neighborhoods, remote source searches and global
field solves. A fixed-size local answer computed by any such method is still
nonlocal. A self-force correction may not infer isolation by counting all world
particles or erase a response using global knowledge.

Independent shadow simulations are allowed only as clearly labeled test/reference
oracles. Their values must not feed a production trajectory, force or field, and
their success does not establish a compliant cure. Read-only diagnostics may
scan the world and reject a run; they must never repair its physical state.

Q-ORACLE-1 is the sole explicit model-computation exception and is confined to
the opt-in quantum owner. It does not relax ordinary field, self-field, movement,
force or geometry locality. The current bridge does not write physical state.

Review must identify each input's owner, causal delivery, fixed record count and
maximum local loop bound. The architecture gate rejects known world/replay member
access in calculations; six-read tests check the baseline neighbor boundary.
These are partial checks, not a proof for arbitrary callbacks or dynamic Python.

The physical rule and fixed-slot local work have constant bounds for fixed K
and fixed-width numbers. Sparse dictionaries, sets, global sweeps and
measurements do not have strict constant total runtime. The Python storage
adapter does not provide worst-case constant-time hash lookups. Empty historical
occupancy keys and materialized cells are retained to preserve legacy scheduling;
world memory can grow as new cells are visited. History collection is optional
and external; JSONL recording streams it to disk.

## Required regression gates

- Exact signed division and remainder accumulation at denominators 1, 12 and 64.
- Invalid input, physical-register and working-register overflow rejection.
- Persistent stationary source and zero stationary self-force.
- One-edge scalar-field propagation and one-hop movement bound.
- At most one update per particle per tick and fixed-capacity occupancy.
- Exact local matter-field exchange and total momentum through tested runs.
- Offset-pair turning on XY, XZ and YZ slices, and original 180-tick regression.
- Immediate transverse contact response with unit force denominator.
- Identical physical evolution with and without recording and measurement.
- Static numeric audit over every physical module and import-boundary checks.
- Generic field/turning unit tests, current-model-specific tests and independent
  replacement of both components through the public simulation API.
- Dedicated lattice, movement, source/activity-policy and diagnostic-projection
  tests; explicit numerical expectations in `docs/TEST_EXPECTATIONS.md`.

## Opt-in quantum contracts — Q-ORACLE-1

The model assumption `deferred-unit-cost-oracle-v1` is defined in POSTULATES.md.
A successful query returns fixed-size integer records with model_cost=1 and
world_ticks=0, regardless of host evaluation work. It never calls Engine.step
or writes physical state. Host counters and budgets remain distinct from cost.
No automatic per-cell polling is added; any future scheduler must bound calls
per cell update, with one call per tick as the intended policy.

The optional sidecar has a single owner for its bounded deferred graph, cache,
query accounting and terminal state. Node records have ten integers and at most
two parents. Amplitudes have two integers; weight is their squared norm. Public
registers and intermediate work obey the same 32-bit and 64-bit bounds above.
max_nodes, max_eval_nodes and max_cached_results are explicit positive budgets.
Failure raises an exception without manufacturing an outcome. Python allocation
and graph traversal are host work, not strict constant-time cell calculations.

Recorded physical graph edges use an unwrapped 3D chart: same-cell or one cardinal
neighbor with a sufficient tick difference. Periodic seam mapping and variable-
length physical links are not inferred by the sidecar. Pure queries must match
their root address and cannot read a future root. They do not measure or resample.

`terminal-two-output-trial-v1` binds one complete absorbing output pair per owner.
The amplitudes must share a scale. The first readout must occur at the scheduled
tick with a supplied uniform integer ticket in [0, weight_a + weight_b). Weights
and their sum must fit the physical bound. Zero total weight is an error. Both
output evaluations share the combined work budget; repeated ancestors across
the two resolves are counted as host work twice. Readout commits one immutable
record after all validation; subsequent calls reuse it. The test enumerates
tickets, rather than validating an RNG or general measurement statistics.

Only the test controller stores detector bits and an event slot. No Engine-native
physical event is added, no source or field is changed, and no post-detection
excitation continues. No general entanglement, Bell, no-signalling, energy or
momentum claim follows. See docs/QUANTUM_DETECTOR_TRIAL.md for the trial contract.

## Output and failures

### Generated output lifetime

Registered generated outputs are temporary: the default retention period is
24 hours after their writers finish, including failure reports and cancelled
workspace jobs. Active operating-system writer leases prevent cleanup. An
unfinalized process exit uses the last recorded start or content modification
time. Source files, original initialization and unregistered content are not
cleanup targets. Both runners require a new or empty output directory.

The [retention contract](docs/RETENTION.md) defines registration, expiry checks,
workspace links, interrupted writes and the cleanup CLI. Startup and active UI
checks do not provide an idle background service; a watcher or scheduler is
needed for that. Visual test sessions use unique output directories, and CI
diagnostic uploads have one-day retention. This is a host storage policy and
does not alter simulation ticks, physical updates or failure detection.

### Default run display

Runs are headless by default, including ordinary tests. The active CLI requires
an initialization file. Historical scenarios use the explicitly selected
`event_universe.legacy_runner` module. Metadata and JSONL events do not depend
on Matplotlib, Pillow or animation capture.

Only an explicit visualization request enables output frames and rendering.
`--visualize` requests the active runner's optional view. For historical
`legacy_runner.run_scenario`, pass `visualize=True`; its `volume` option chooses
volume or slice. Explicit historical CLI view options also request visualization.
The historical 3D view uses the existing 1500×1275 renderer; a generic view must
label configured fields rather than interpreting their names as scalar phi or
particle momentum.

Pytest enables captured run reports and presentation-only tests only through
`--visualize-runs`. Without that flag, physical assertions still execute and no
HTML/GIF run reports are generated. Requested frame stride changes recording
only, never the physical update interval.

The historical runner supports a live display during calculation and replay
export only when explicitly requested with `--live` or API `live=True`. A live
request also enables recorded visualization. Both options default off.
Live preview snapshots may be coalesced and use explicitly provisional framing
and color scales. They never replace the canonical sampled frames, final enhanced
GIF/HTML, event trace or acceptance checks. Preview faults must not alter physical
evolution or prevent the recorded failure report. A completed live page opens the
current run's final replay, retaining its completion or failure status.

The active generic local commit and failure behavior is defined in
[docs/DISTURBANCES.md](docs/DISTURBANCES.md). The following field-phase description
applies to historical scalar models.

Field proposals are validated before the field phase commits. Particle-field
proposals are validated before that local exchange commits. A whole tick is not
transactional: if a later operation fails, previously committed local operations
remain available for diagnosis. The world then rejects further steps. On such
failure the runner saves diagnostic output and re-raises the error.

Runtime validation uses exceptions and remains active under `python -O`.
Reports distinguish checks actually performed from architecture descriptions
and physical claims not established by the tests.

### Display readability and playback

The following visual conventions apply when the historical scalar/particle
renderer is explicitly requested. They do not assign meanings to generic field
names or require visualization for a run.

The 3D axes have readable coordinate ticks and distinct colors: X is coral,
Y is green and Z is blue. A camera-synchronized corner compass shows positive
axis directions, not position or distance. Narrow views gain display padding
while preserving equal coordinate-unit scales on all axes.

Total particle-plus-field momentum appears at the top as (Px, Py, Pz).
Particle markers are opaque colored discs with a white outline and glow;
outlined arrows remain readable above the translucent field. Arrow length
represents the model's capped movement-budget rate relative to c: full rate
has length 10.8 display-coordinate units. The captured c_units sets this scale.
Missing scale means no velocity arrow, not a guessed speed. In linked worlds
this is the departure budget rate, not a measurement of displacement per tick.

A cyan ↻ marks a shorter displacement through the periodic boundary, using the
captured world dimensions. A red X marks a shortest displacement of at least
two cardinal grid steps between displayed frames. A multi-cell jump across a
boundary shows both markers; a periodic symbol must not hide that jump.
Trails break at coordinate discontinuities. Sparse sampling is ambiguous, so
a marker alone is not proof of faster-than-c motion; inspect consecutive ticks.

The combined scalar field uses a fixed amber scale throughout an animation.
A square-root display mapping lifts weak values; color is not a linear field
measurement. Wide soft halos improve visibility without changing physical
field range. There is no invented per-particle attribution of a shared field.
The floor and two walls have twice as many visual grid subdivisions; this does
not change the physical lattice or simulation resolution.

The exported GIF stops at the final frame instead of resetting time through
automatic replay. Reloading its HTML replays it from the start. This playback
contract applies to both slices and 3D views. None of these display operations
smooths physical positions, cancels self-force or changes a simulation record.


## Optional local-link geometry candidate — v11

The user-authorized link extension is `scalar-field-v11-local-links`, selected
by `LinkedSimulation` or the historical CLI's `--scenario links`. Baseline v10 remains available for
comparison. The five/sixteen-register schemas above describe historical scalar field and
particle records; the frozen v10 reference retains twelve particle registers.
The v11 candidate additionally has fixed `LinkCell` and `Transit` records:

- Six received scalar integers; six active length integers; six packets of
  `(value, proposed_length, remaining)` = 30 link integers per materialized cell.
- `(direction, departure, length, due)` = four integers per in-flight particle.
  The particle remains in its origin's fixed occupancy slot throughout transit.
- Three canonical owned edges: +x,+y,+z. Negative edges are local copies. Both
  endpoints may propose changes; ownership must not bias the law by direction.
- Length proposal: `base + (stretch_num*(local_phi+received_phi))//(2*stretch_den)`.
  Defaults: base=100, stretch_num=1, stretch_den=1. A pair of field values 10,10
  gives length 110, representing 1.10 original cell spacings. The base is a
  scale separating address spacing from the minimum represented length.
- A proposal travels for the OLD active length, then both endpoints activate
  it. Same-tick opposing proposals use the larger value (explicit candidate
  choice). Intermediate snapshots are coalesced, not queued.
- Field packets travel at c=1 elementary length unit per elementary time tick.
  Matter uses the existing speed proxy `min(L1(momentum),c_units)/c_units`.
  Transit duration is `ceil(length*c_units/speed_proxy_numerator)`, calculated
  with bounded integer operations. There is no cross-edge time credit: every
  individual edge respects c. For speeds whose arrival does not align with a
  tick, the delay is less than one elementary tick per edge. It can accumulate;
  this is a documented discretization, not exact rational mean speed.
- Rest does not schedule movement. Travel length and direction are locked at
  departure; evolving geometry affects subsequent transits. This is a model
  approximation. The turning response still uses the scalar gradient; it has
  not been derived from link lengths as an Einstein geodesic.
- A full target blocks arrival; it neither deletes a particle nor grows cell
  capacity. Any retry uses a newly scheduled full transit, with no banked credit.
- Initial field seeds are published before the first local scalar replacement.
  No dynamic field rewrite API was added.

New regression gates: generic length/travel inputs and overflows, shared owner
at periodic seams, delayed geometry activation and zero messages, busy-channel
fixed storage, order-independent simultaneous proposal merging, remote
intervention outside the causal reach, no direct remote scalar reads, locked
travel length, source symmetry with zero self-force, and three-particle local
momentum exchange. The first owner-only proposal failed the stationary-source
check; allowing symmetric proposals from both endpoints removed that artifact.
No force cancellation or momentum repair was introduced to do so.

### Reject isolated self-force in application runs

The application runner validates particle momentum after every completed tick
when the initial world contains exactly one particle and entirely zero field
records. Its own source stays active. Any change in its initial momentum raises
`InertialMotionViolation`, terminates the application run and saves the failing
tick, event trace and failed metadata. If visualization was requested, preserve
the failure frame and an HTML heading explicitly marked FAILED RUN.
The check is independent of display sampling and never clears remainders, changes
momentum or disables sources. Multi-particle and initially seeded-field worlds
are not classified as isolated by this check.

This is read-only diagnostic rejection, not a corrected physical law or a proof
of straight trajectories. Direct Engine/ScalarSimulation callers still receive the
underlying model behavior. Model acceptance requires the separate isolated-motion
gate; a test that confirms rejection does not turn that failing physical gate
into a pass. Existing baseline physical requirements remain unchanged.
No threshold exempts a one-unit impulse.

## User-authorized mass and elastic point contacts — v13

The user requested same-point particle collisions and then an individual mass
parameter. `ScalarSimulation(collisions=True)` selects
`scalar-field-v13-mass-elastic-contact`; `LinkedSimulation(collisions=True)` selects
`scalar-field-v13-mass-elastic-local-links`. Both public APIs accept
`add_particle(..., mass=...)`. Mass is a fixed positive integer in simulation
mass units, default 1. Zero, negative, non-integer and overflowing masses fail
before insertion. It is supplied inertial mass, not emergent mass or a claim
about gravitational charge. The existing occupancy-based scalar source and field
coupling are unchanged. Collision-free mass-1 v10/v11 behavior remains available.

### Contract and independent quantities

| Part | Contract |
| --- | --- |
| Law | Classical elastic backscattering: reverse relative velocity in the pair center-of-mass frame |
| Inputs | The two co-resident particles' three momentum numerators, denominator and positive mass; no remote particles or field solve |
| Evolving state | Four added particle integers: mass, momentum_den, move_budget_den, last_collision_tick; fixed K-by-K contact flags owned by each contacted cell |
| Parameters | Mass is constant per particle; c_units, K and field parameters retain their existing roles |
| Derived values | Physical momentum is (px,py,pz)/momentum_den; movement-budget rate is min(L1(p)/mass,c_units), never an independent velocity parameter |
| Output | Two validated particle records committed together; immutable collision event with before/after state |
| Bounds | Every stored integer fits 32-bit magnitude; every intermediate fits 64-bit magnitude; exact reduction, never truncation or saturation |
| Errors | Overflow stops the world before either member of the failing pair commits; prior local events need not roll back |

For physical momenta p1 and p2 and M=m1+m2, componentwise:

- p1' = ((m1-m2) p1 + 2 m1 p2) / M
- p2' = (2 m2 p1 + (m2-m1) p2) / M

The calculation preserves p1+p2 and p1^2/(2m1)+p2^2/(2m2) exactly. Squared
momentum here is the sum of the three component squares. These energy checks
belong to tests/diagnostics and do not repair physics. For equal and opposite
momenta both particles reverse; equal masses exchange momentum vectors. General
unequal masses or oblique inputs need not reverse both lab-frame directions.
Literal lab-frame reversal would change total momentum whenever it is nonzero.
The selected 180-degree center-of-mass scattering angle is a model choice.

All fractional results use integer numerators and a positive common denominator
per vector. Movement credit also has a positive denominator and is retained
exactly across a collision. Direction phase restarts at zero for a newly scattered
trajectory; carried field-force remainders remain attached to their particles.
Field impulses remain integer physical impulses: a numerator changes by impulse
multiplied by momentum_den, and the cell receives the opposite physical impulse.
Linked transit time is ceil(length*c_units*mass*momentum_den/L1(numerators)),
with the existing speed cap and no cross-edge credit. The same rule applies at
all speeds. Bounded Euclid uses at most 128 divisions for 63-bit inputs. Vector
reduction concerns rational representation, not Euclidean vector normalization.
Denominator growth can exhaust fixed registers; that is an explicit error.

### Contact timing, locality and scope

A contact means the same canonical integer XYZ address at a tick boundary.
After due link arrivals and before the field phase, resolve initial/current
co-residence. After the complete sequential movement phase, resolve new baseline
arrivals. Intermediate occupancy during sequential movement is not simultaneous
co-residence. In-flight link residents are excluded until arrival. No collision
adds a hop, rewrites a past event or changes locked in-flight travel.

Each cell inspects only its K resident slots, at most K(K-1)/2 pairs. A pair's
contact flag prevents repeated bouncing while it remains together. An actual
move clears flags incident on the departing and arriving slots. Each particle
scatters at most once in a tick. More than two co-residents are resolved in slot
order as disjoint pairs per tick; remaining fresh pairs can scatter on later
ticks. This is a deterministic local multiparticle policy, not a unique
simultaneous many-body solution or a permutation-invariance claim. Capacity
blocking remains distinct; K=1 cannot host a two-particle contact.

The contact flags are K*K integer registers per contacted cell, independent of
world size and elapsed time. Global address sweeps and Python dictionaries remain
host costs. There are no per-source maps, growing local histories, external
queries or quantum exceptions in this law.

Point contacts do not detect crossing between sampled addresses, overlapping
finite-radius surfaces or meeting midway along a link. The lattice's capped L1
speed and field law are not relativistic mechanics. Exact classical pair energy
conservation therefore does not establish relativistic energy conservation or
energy conservation for the entire field-coupled simulator.

### Output and compatibility

`--scenario collision`, `collision-masses` and `collision-links` exercise this
feature through the historical runner. The 3D HTML/GIF renderer is used only
when visualization is explicitly requested. Scenario `masses`
contains one mass for each seed (or is empty for unit defaults). Metadata records
these masses, collision selection and the explicit model identifier. In 3D,
particle labels show mass and velocity arrows use the mass and momentum scale.
`particle_collision` JSONL events include named before/after records and their
denominators. Legacy force events keep their tuple layout; their momentum fields
are numerators at the denominator from that particle's latest collision record
(or 1 before any collision). Legacy `TraceRecorder.collisions` still means blocked
moves; actual scattering events are in `collision_records`.

The original twelve particle fields keep their order. Four new fields append
with defaults (1,1,1,-1). Fixed-schema and physical behavior checks cover current
records. Frozen-v10 equality is no longer an acceptance gate; its source remains
an unchanged historical archive.

## Opt-in balanced-motion and local-halo candidate

`scalar-field-v12-balanced-halo`, exposed as `BalancedSimulation`, combines
interleaved integer movement with a synchronous local scalar cancellation phase.
After every particle has completed its response and optional hop, the phase sets
`phi` and `remainder` to zero in the union of the six neighbors of its previous
and current positions. It retains field momentum. Every proposal validates before
commit; baseline v10 is unchanged.

The scheduler may visit at most twelve targets per particle and coalesces overlaps.
The local rule receives one fixed cell record. It adds no physical registers,
source map or history and satisfies LOCALITY-1 for fixed K. The candidate must keep
isolated particle momentum exactly at all tested ticks and retain nonzero external
response. Exact inputs, results and limitations are in
[docs/BALANCED_MOTION.md](docs/BALANCED_MOTION.md).


## Selected quantum event network — Q-EVENTS-1

The selected finite candidate is `deferred-event-network-v1`, specified in
[QUANTUM_EVENTS.md](docs/QUANTUM_EVENTS.md). A fresh `DeferredQuantum` owner binds
one `EventNetworkConfig` before creating legacy scalar nodes. The two state
representations cannot be mixed in one owner. Existing terminal/Focus consumers
retain their old API and behavior unless the new representation is selected.

The event backend owns immutable local matrices, per-cell head IDs, joint source
or checkpoint amplitudes, earlier outcome constraints and bounded decision records.
Ordinary cells do not acquire this growing host state. Coherent steps append only
disjoint one-cell or nearest-neighbor operations. Queries return fixed-size local
weights at the current tick; full-state inspection is host-only diagnostic work.
Prior correlated records are included in a conservative dependency closure.
This is sufficient pruning, not a proof of the smallest possible contraction.

An explicit one-cell instrument supplies one to four outcome matrices whose
completeness relation has a positive common integer scale. `prepare` computes
all branch weights without sampling. `commit` accepts a uniform integer ticket
when multiple outcomes have positive weight, or no ticket for a certain result.
Repeated record identities cannot resample. A graph change invalidates an
uncommitted decision. The no-event branch is applied like every other branch.
A coherent interaction alone never requests a ticket.

The executable representation retains the existing signed 32-bit real/imaginary
registers and checked 64-bit intermediates. The positive-code representation in
the high-level Highlights is not newly claimed implemented. Node, traversal,
term and decision budgets are explicit. Exhaustion/overflow rejects an operation
without inventing a physical result. Removing an exact common integer factor
is representation reduction, not a floating-point normalization or rounding.

Query evaluation and record commit add zero world ticks under Q-ORACLE-1. Host
node evaluations are counted separately; state size, condition scans, checkpoint
work and bit/storage limits remain host costs. A checkpoint replaces the full
live correlated component, never merely a target marginal. It preserves all
unresolved phases and the immutable audit ledger. This is not bounded total
memory for an unlimited simulated lifetime.

The controller may condition on its known records. Such conditional probabilities
are not a remotely readable physical register, a classical communication channel,
or an implemented generic Engine commit interface. There is no automatic native
per-cell polling, quantum-field feedback, universal measurement trigger, physical
free-momentum law or derived classical limit in this change. The 3:4 matrix is a
test fixture and explicit demonstration parameter, never a hidden default law.
