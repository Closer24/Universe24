# Event Universe — active modular 3D integer simulator

The canonical implementation is the `event_universe` Python package under `src/`.
`persistent_source_field.py` is a compatibility facade, with no copied physical law.
The model identifier is `scalar-field-v10-contact`; package version is `0.1.0`.
The plain-language conceptual source is `POSTULATES_HE.md`. If its wording is
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
  tests; explicit numerical expectations in `docs/TEST_EXPECTATIONS_HE.md`.

## Output and failures

### ברירת המחדל להצגת הרצות

כל הרצה מוצגת כברירת מחדל בתלת־ממד באיכות 1500×1275: חלקיקים ככדורים
מוארים עם הילה, שדה רך ושקוף, מסלולים מודגשים ומצלמה מסתובבת.
מצרפים HTML עצמאי ואנימציית GIF שאפשר לצפות בה. הכלל חל גם על תרחישים
חדשים ועל כל הרצת עולם בבדיקות, לרבות הרצות ההשוואה לגרסה המקורית.
דוח הבדיקות רשאי לדגום פריימים, אך משתמש באותו עיצוב ובאותה רזולוציה.
בדיקות של פונקציה בודדת שאינן מריצות עולם אינן צריכות אנימציה.

זו ברירת מחדל של תצוגה בלבד: אין שינוי ברזולוציית הסריג או בפיזיקה.
גודל הכדור וההילה הם סמלים חזותיים ולא גודל פיזיקלי של החלקיק.
תצוגת חתך דורשת בחירה מפורשת: `--view-2d` בשורת הפקודה או
`volume=False` ב־`run_scenario`. האפשרויות `--plane` ו־`--slice`
קובעות את החתך כשנבחר מצב דו־ממדי; `--view-3d` נשאר נתמך.

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


## Shared local interaction candidate (v12)

`SharedActionSimulation` explicitly selects `scalar-field-v12-shared-interaction`.
The existing `Simulation` (v10), `LinkedSimulation` (v11), and frozen-reference
expectations are unchanged. This candidate implements the **shared interaction
term**, NOT a complete variational time integrator and NOT a self-force cure.

The single immutable term is `S_int(n, phi) = g*n*phi`. Its unit field variation
is `g*n`, used for the local source. Its central spatial variation for one
particle is `g*(phi_plus - phi_minus)` on each axis, divided by
`2*impulse_units` with retained signed integer remainders. Both callbacks are
bound to the same `ScalarInteraction` instance. There is no independent source
coefficient or response coupling in the public candidate configuration.

A local spatial functional with neighboring values held fixed is
`2V_i = (D-6)*phi_i^2 + sum6((phi_i-phi_j)^2) - 2*g*n_i*phi_i`.
Its centered unit variation divided by four gives
`D*phi_i - sum6(phi_j) - g*n_i`, identifying the **stationary** screened stencil.
This local expression is not a globally additive energy: summing it would
count spatial edges twice. The current relaxation, integer projection, delayed
sampling, digital movement, and accumulated field-momentum bookkeeping have
NOT been derived from a common temporal action. No energy/Noether claim follows.

The field recurrence is retained. Full-vector response replaces dominant-axis
suppression only in this candidate. It uses the existing fixed six-port linked
transport with base length 1 and stretch 0, not new instantaneous neighbor reads.
Signals traverse one port per tick; a particle occupies its departure cell until
its frozen transit completes and is pushed only when ready to depart. Transit
uses `ceil(length*c_units/min(L1(p),c_units))`, so nominal momentum ratios are
NOT exact continuously varying velocities, nor isotropic Euclidean light speeds.
These inherited v11 semantics differ explicitly from the v10 one-push-per-tick
scheme. This is not a claim that delayed samples share one equal-time action.

### Candidate parameters and exact register contract

| Parameter | Default | Why / status |
|---|---:|---|
| `coupling` | 64 | Same experimental `g` in both variations; not calibrated physics |
| `impulse_units` | 2048 | Declared impulse scale; default effective coefficient is 1/64 |
| `field_den` | 7 | Retains screened six-neighbor recurrence, constrained to D >= 7 |
| `c_units` | 12 | Inherited integer transit scale, not a relativistic dispersion law |
| `nx, ny, nz` | 64, 48, 32 | Periodic experiment domain; all dimensions >= 3 |
| `max_particles_per_cell` | 4 | Fixed local slot capacity K |
| port length / stretch | 1 / 0 | Fixed transport policy for this candidate, not fitted geometry |

Core state remains 5 cell + 12 particle registers; existing transport adds 30
registers per materialized cell and 4 per in-flight particle, with at most K
resident/in-flight particles per cell. Coefficients/physical state are bounded
32-bit integers; every product/difference is bounded before use as 64-bit work.
No source-ID maps, unbounded local queues, speed-dependent special physics, or
global correction is introduced. Host dictionaries, iteration and rendering
remain separately charged, not strict worst-case O(1) host computation.

### Acceptance and scope

CLI scenarios `action-contact`, `action-isolated`, `action-rest`, `action-free`
are demonstration runs with `impulse_units=64` (effective coefficient 1/2 for
`g=64`), NOT default physical parameters. The free control sets `g=0`, disabling
both source and force. Every run uses the existing standalone 3D GIF/HTML output.
Run `python tools/shared_action_evidence.py` for stationary/free controls,
slow/fast isolated particles, the offset pair, and a near-pair response. It
writes HTML/JSON/JSONL and exits nonzero for failed acceptance. Initial fields
are empty; no velocity-matched dressed initial state is claimed. Residual force
counts as response even when no integer momentum unit has changed yet.

The offset-pair and slow/fast isolated-motion acceptances in
`tests/test_shared_action_simulation.py` remain ordinary assertions. Missing
transverse deflection or an isolated response in momentum OR remainder is a
failure; these gates are not skipped, marked xfail, or weakened. Exact algebra, integer bounds, port
locality and bookkeeping can pass while physical acceptance fails. Do not
replace the default model or merge as a physical fix while these gates fail.
