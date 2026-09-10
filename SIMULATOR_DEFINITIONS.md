# Event Universe — active modular 3D integer simulator

The canonical implementation is the `event_universe` Python package under `src/`.
`persistent_source_field.py` is a compatibility facade, with no copied physical law.
The model identifier is `scalar-field-v10-contact`; package version is `0.1.0`.
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
4. A particle contains exactly twelve integer fields:
   `x, y, z, px, py, pz, move_budget, axis_phase, force_rx, force_ry, force_rz,
   last_update_tick`. The last field prevents multiple updates in one tick.
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

The field and turning components can be supplied independently to `Simulation`.
Their denominators come from the same `Config` used by state audits. A scalar
replacement must fit the existing fixed cell schema; vector or multiple-field
state needs a separate explicit contract. Custom implementations must be local,
deterministic, bounded and without evolving private state. Measurement code
reads output and records evidence. No local law receives a world object or
knows source identities at remote cells.

The engine receives field activity as a predicate instead of interpreting the
candidate law's changes itself. The default model explicitly retains its legacy
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
- Tick-by-tick equivalence to frozen v10 for stationary, contact and turning
  scenarios, including fields, particles, slots, active cells and event traces.
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

### Default run display

Every run defaults to enhanced 1500×1275 3D: outlined particle markers with glow,
a soft translucent field, emphasized paths and a rotating camera. Provide a
standalone HTML file and its GIF animation. This also applies to new scenarios
and every test world, including frozen-reference runs. Test reports may sample
frames while retaining the same design and resolution. Pure-function tests need
no animation.

This changes display defaults only, not lattice resolution or physics. Marker
and glow sizes are visual symbols, not physical particle sizes. A slice requires
explicit `--view-2d` or `volume=False` in `run_scenario`. `--plane` and `--slice`
choose the slice in 2D mode; `--view-3d` remains supported.

Every application run also records metadata and JSONL events through the existing
Matplotlib/FuncAnimation/Pillow pipeline. Pytest produces a combined standalone
HTML report of every captured engine run.

Field proposals are validated before the field phase commits. Particle-field
proposals are validated before that local exchange commits. A whole tick is not
transactional: if a later operation fails, previously committed local operations
remain available for diagnosis. The world then rejects further steps. On such
failure the runner saves diagnostic output and re-raises the error.

Runtime validation uses exceptions and remains active under `python -O`.
Reports distinguish checks actually performed from architecture descriptions
and physical claims not established by the tests.

### Display readability and playback

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
by `LinkedSimulation` or `--scenario links`. Baseline v10 remains available for
comparison. The five/twelve-register schemas above describe baseline field and
particle records; v11 additionally has fixed `LinkCell` and `Transit` records:

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
tick, event trace, failed metadata and an HTML heading explicitly marked FAILED RUN.
The check is independent of display sampling and never clears remainders, changes
momentum or disables sources. Multi-particle and initially seeded-field worlds
are not classified as isolated by this check.

This is read-only diagnostic rejection, not a corrected physical law or a proof
of straight trajectories. Direct Engine/Simulation callers still receive the
underlying model behavior. Model acceptance requires the separate isolated-motion
gate; a test that confirms rejection does not turn that failing physical gate
into a pass. Existing baseline physics and frozen regression expectations remain
unchanged. No threshold exempts a one-unit impulse.
