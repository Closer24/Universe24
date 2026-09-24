# Event Universe — active modular 3D integer simulator

## The Beam Law: RAYS-1 (2026-09-19)

A world selecting `"law": "beam"` runs the Beam Law
([docs/BEAM_LAW.md](docs/BEAM_LAW.md)): a row with a record on the digital line
of its momentum at one speed, the collision table a bijection inside its
invariant classes, the detector's record the squared coherent sum of what it
clicked, the click the one one-way border and the one measurement: an
action of the law on the state, the record ended at the detector and the
detector's own record changed (the model owner, 2026-09-23, record 1139;
[POSTULATES.md](POSTULATES.md) section 10). Coverage (a detector's Nodes), the
threshold and the `reads` component are independent data. No audit record or
whole-GameBoard sum supplies memory, routing or a physical result; the readings
of the engine (`cube_flux`) and of the host (`diagnostics/shell_readings`, the
shell means, outside the engine since 2026-09-21) are read-only. The
`reversible-detector-v1` candidate of the same day is absorbed and deleted
([migration](docs/MIGRATION.md#the-law-of-the-ray-on-2026-09-19-rays-v1));
quantum uncertainty and Born behavior remain separate unproved goals.

### The couplings on the GameBoard are the six verbs (2026-09-22)

Every rule a LocalRule runs on a NodeState, for a row on its Link or for a
body at its Node, is one of the six verbs on bounded integers (the model
owner, records 181, 202 and 929): the translation of an accumulator by its
rate with the whole part taken and the remainder kept
(`core.integer.by_drive`, `nature_beam.by_drive_rows`), the bilinear form
with a declared matrix (`core.integer.signed_inner`, the columns' signs,
the labels' weights, the Gram matrix), the group-ring addition, the
permutation, the evaluation and the Euclidean division; a rule that needs
more is stated under its own identity and never enters the law by a key.
The couplings the atom worlds and the light worlds exercise are read
against the six, one row each with its code lines and its three tests, in
[docs/designs/couplings_algebra/COUPLINGS.md](docs/designs/couplings_algebra/COUPLINGS.md);
the definitions they add to the vocabulary, each pointing at its code and
its design, are in [docs/TERMINOLOGY.md](docs/TERMINOLOGY.md) ("The rule"):

- **The age wall** and **the age wall's set**: the one wall function of
  the crowd, `core.integer.age_wall` (`core/integer.py:153-187`), and its
  declared members with their coefficients, `measured.AGE_WALL_SET`
  (`measured.py:345`, `age_wall_set` `:364-379`): the body's clock at 1
  (the owed count, `engine.count_owed`, `engine.py:157-182`), the row's
  flight at 1 + gamma under the world key `optical`; never the phase per
  age (BEAM_LAW note 25; records 394, 421, 422, 428).
- **The crowd at a row's Node**: a row's two reads of the one reading set
  at its own Node, less its own number, the age moment before step 1 and
  the arrival flow after the walk (`nature_beam.CrowdMoments`,
  `nature_beam.py:3069-3153`; under `optical`).
- **The wall on the flight, the push on a row, the label by Bresenham**:
  the three verbs of `optical-v1` on a row in transit
  (`nature_beam.optical_walk_step` `:3634-3710`, `optical_turn`
  `:3730-3963`; docs/designs/one_wall/NOTE.md, EVERY_FAMILY.md).
- **The phase per age**: the pair form of `phase_per_link`, the first
  difference of a floor at every walk (`nature_beam.by_clock_rows`
  `:569-583`), the remainder read at the click (BEAM_LAW notes 37 and 45).
- **The placed fraction and the completion's quantum** (f_F, q_F) of a
  family: (1, 0) without the flag `massive`, (0, M) with it
  (`nature_beam.FamilyFlight` `:979-980`, `_place_completion`
  `:6363-6455`; docs/designs/massive_rows/DESIGN.md section 3).
- **The flow label f_D** of `flow-link-v1`, the integer vector nearest
  Q D / S_1 in the flow sums alone, when it merges (docs/designs/flow_weight/DESIGN.md
  section 1.2; absent from `main` at 8fa9e00b).

The gate is `tests/test_integer_algebra.py` (the Register Architect's,
record 920 (A)): no float literal, no true division, no float dtype, no
random draw and no integer root outside the named table-formation
functions in the five modules of the physical path. Two integer roots
taken at run time on these worlds' path are named by their design and by
COUPLINGS.md (section 3) for that gate: the meeting's norm
(`meeting.py:359-361`) and the pair of a pushed row
(`nature_beam.py:3549`).

### The four building blocks (2026-09-24)

The model owner's rule (2026-09-24, 13:36Z and 13:43Z, through the Boss;
Highlights 5.4): the engine knows the four building blocks and the six
verbs only. A lamp, a polariser, a light clock, a mirror line or a
receiver by name is a COMPOSITION declared in the world file and defined
in this section, never a name the engine branches on; every feature of the
local detector law (the receiver by name, the joint gather and the lamp's
ladder below) is such a composition, and its line
names the blocks it composes and nothing else. The engine as it stands on
`main` (`src/event_universe/events/detector_law.py`, `world.py`) has these
four and no fifth thing; the three tests of every rule (generic, vector,
local; [skills/workflow.md](skills/workflow.md)) are read against them.

- **The emitter.** A measured event that births records from its cells
  from a declared interval: a lamp (a body at a Node that inserts its
  family's train by the family's clock, one record per birth, the birth
  wheel's u on the record; `_births`) or an emitting block (a block whose
  own record's cycles source one light record per cycle at its cells,
  `emits`; `_block_births`). Its declarations are the train, the rate, the
  wheel, `own_grace` (the intervals after the train during which its own
  cells take nothing of its own record) and, from the receiver by name and the lamp's ladder,
  `receiver`.
  From the first interval after the train its own cells take the record's
  remnant and book it on no pointer (item 10 of DECLARATIONS.md section
  10; `_own_take`).
- **The body.** A block of cells with a pair on the six-neighbour term
  (a well of a massive kind, a gap of light's kind) and a momentum: it
  moves one Link at a time by the drive's accumulators (`_move_block`),
  carries its own massive record on its cells (`seed`), takes what
  reaches its cells where it is `absorbing` or bound to a receiver, and
  is hit (its response records and its coupling `receive` and `source`).
  A wall is a body: a MIRROR LINE is a line of blocks of light's kind with
  the gap pair [1, 2] (DECLARATIONS.md section 15 L-1); a matter kind's
  zero face is the kind's own `faces` declaration, not a body. A
  polariser is a body WITH A TABLE (a measured event whose table entry
  carries an integer `phase_window`, the setting): under the joint gather it is a table
  body of two cells, its own Node and the next Node on the arm's line.
- **The receiver.** A set of cells with a wheel (`detectors`: named
  positions, or `block` for the cells of a body): the record's offer at
  its Ports is booked to the set's pointer, and when the pointer crosses
  the rung (pointer x wheel at or above the record's norm, the counting
  form) the set has clicked; the record's line names the cell the birth
  wheel's u chooses on the record's ladder and the record ends there for
  the ladder. A face of the GameBoard is a receiver that books to the
  escaped row (light's sponge), and so is every set the record's ladder
  does not name: a SINK takes and books, and is never chosen.
- **The clock.** A body's own count (its record's cycles across its
  cells, `_block_clock`; the stamp `clock` on its lines) or a detector
  set's count (the interval of the first rung at the set): the click is
  stamped with it (`click`, `clock_source`), and the clock's readings are
  the only thing compared with nature (a DETECTOR reading; every reading
  of the board is a GAMEBOARD diagnostic, ENGINE.md).

The features, each a composition of the four and nothing else:

- **The receiver by name** (DECLARATIONS.md section 13 item 7; BUILD.md
  section 21): an emitting body + one named receiver (its record's ladder
  that one set, the line at the set's first rung; every other receiver a
  sink) + the clock of the receiver (the stamp).
- **The joint gather** (section 1 item 3, section 14 item 6; BUILD.md
  section 19): an emitter of two arms + two bodies with a table (each a
  receiver of two cells) + one receiver of the pair on the four joint
  cells (the rung on the joint weights R = J^2) + the bodies' clocks.
- **The lamp's ladder** (SIZING.md; BUILD.md section 20): a
  lamp + the named receivers (the screen's sets, the record's ladder) +
  the sinks outside the ladder (the faces, the mirror line's take) + the
  sets' clocks.

WHERE THE CODE BRANCHED PER BODY BEFORE, AND WHERE IT IS ONE NOW (the
owner's framing, 14:00Z: the three features are one job, the four blocks
the same code for every body on the board): before, a block's record and
a lamp's record clicked by the same rule, every cell on the ladder and the
line at the close, so an emitting block's receiver was whichever cell held
the most; the emitter's own take of its record was limited to a grace (an
age branch per record); a polariser acted on a label (the amplitude law's
per-label table) and the pair's arms clicked one by one. Now, one rule
each for every body: a record's ladder is what the world names (a named
set for a block's record, the named sets for a lamp's, every cell where
none is named) and every other cell a sink; the line at the rung where the
ladder holds one cell, at the close where several; the emitter's own cells
take its record on no pointer at every age after the train; a table entry
with an integer setting on an arm forms a table body of two cells for any
family; a record of several arms gathers once on the joint cells. No
branch on a family's or an experiment's name remains in `src/`.

A fifth thing: none. The probes (`probes`, a list of Nodes whose light
amplitude is written per interval) are a HOST reading of the board, not a
block; they act on nothing and are compared with nothing but the
declaration's own script (a GAMEBOARD diagnostic). The splitter of the
TABLE form (a table entry with `inputs`) is a body with a table, as the
polariser is.

## GameBoard topology (2026-09-19)

The owner-approved run parameter selects open or periodic topology independently
per axis; open is the default. The exact schema, one-interval Link transfer,
extent-one return, unchanged carried momentum and mixed-axis refusal rules are
in [the engine contract](docs/ENGINE.md#per-axis-gameboard-topology-2026-09-19-implementation-amendment).
This choice does not change a local contact law or establish equivalence between
a thin periodic GameBoard and full 3D matter. Earlier topology descriptions below
belong to their dated models, not an implicit events-world default.


## Historical generic disturbance model (deleted on 2026-09-19)

History marker (2026-09-19): the generic disturbance simulator this section
describes was deleted on 2026-09-19 with the engines before the Beam Law
([migration](docs/MIGRATION.md#one-engine-on-2026-09-19-the-old-engine-deleted));
its schema document, docs/DISTURBANCES.md, is in git at any commit before that
deletion. The active contract is [the Beam Law](docs/BEAM_LAW.md) with
[the engine's bookkeeping](docs/ENGINE.md). The text below is kept as written,
the record of that model; it defines nothing in the engine.

Initialization accepts only `sampling_profile: "detector-only-v1"` under the
Detector-owned sampling contract: an ordinary
absorber never draws. The ray lottery, the bond registry and the
`historical-autonomous-v1` research profile were deleted on 2026-09-17 (issue
#164, bucket B.5), after the native instrument/contact bindings (buckets B.1
and B.2). Deterministic ordinary and coherent evolution remain available. This
admission boundary does not implement PASS/RETURN or remove the output-clock
composition restrictions. Since 2026-09-18 nothing draws (Highlights 5.4,
point 14): a mark absorbs a thing and returns a shadow, and it declares no
seed (`bit-law-v1`).

The opt-in integer Node contract extends the
active engine with indexed bounded interactions, 1..32-component properties,
explicit aggregation and pre-commit conserved readouts. In this profile one hop
takes one h and local rules take their declared k*h before dispatch. Existing
cost-budget timing below applies to configurations without that opt-in.
Indexed spatial reactions read n resident records and local fields from one
frozen view; n is separate from duration k. Optional `commit_when` is checked at
selection and against the rebased pre-substep state before committing, while
`when` remains a start trigger. Each delayed field-only or joint substep must
preserve its declared invariants on its actual before/after values. A failed
condition, invariant or bound faults before any owner in the proposal changes.
The local rule contract defines
bounded selection, stored guard metadata and the complete-owner balance check.

The primary API is `Simulation(initial: InitialState)`. An initialization JSON
file supplies every field/type name, seed, allowed local expression, coupling,
transport rule and cost setting. The engine has no hardcoded interpretation of
mass, charge, velocity or other user-defined physical names. Missing initialization
does not select a scalar model.

New emergence experiments produce states using elementary local vector
operations rather than supplied continuum physical formulas. Comparisons,
invariants and independent external benchmarks remain validation tools. Existing
formula-based reference configurations are labeled separately; they do not
establish emergence. The entity audit records the
physical inventory, executable probes and remaining classical/quantum gaps.

docs/DISTURBANCES.md is the authoritative active schema
and transition contract: bounded scalar/vector payloads, whole-record or extensive
transport, atomic local exchange, explicit sources, fixed link transit, local
computation delay without debt, capacity failures and headless output.

Optional spatial fields add initialization-defined
baselines, continuous external emission and fixed-clock outward octant transport
by default. The opt-in shared computation cycle
freezes field and carrier updates under one combined budget, retaining later
input separately until commit; all waits and transits are integer tick counts.
Their six delivered channels preserve travel direction; eight internal sign
classes prevent reversal of an emitted branch. The document specifies source
cadence, bounded residual ownership, cost coupling and periodic/self-field limits.

Optional spatial couplings add same-field atomic
exchange and discrete norm-preserving rotation, driven by local values or scalar
directional flux. Samples precede fresh emission; a delayed carrier proposal
commits its equal-and-opposite spatial reaction with the carrier. The response
contract defines same-timestamp packet preparation, fixed local cost and the
restricted straight-line isolation result without general source attribution.

Optional generic local field rules add schema 1
local transport alongside existing outward fields. A node can retain dynamic
stock, read six delivered scalar/vector channels independently, and assign
several retained/outgoing values from one frozen rule view. Groups are metadata
over existing field definitions. Joint carrier/field assignments store additive
field deltas and revalidate declared invariants against live stock before delayed
commit, while immutable baseline and ongoing source bookkeeping keep their own
owners. Fixed capacities, integer bounds and priced local work still apply.
The linked contract defines quiescent scheduling and records nonconserved field
conversions as transformations rather than external sources. It supplies no
Maxwell, Lorentz or quantum law, and does not alter schema 2 finite decay.

A scalar spatial field may instead select `"transport": "ray"`
(`isotropic-ray-field-v1`): rays carry an integer heading and accumulators and
move one link per tick along their own GameBoard line, with a per-Node slot
capacity. Such a field may add `kerengonen` (`kerengonen-ray-field-v1`): rays
carry a phase that advances per link, and the coherence of the rays meeting at
a Node gates what is absorbed and sampled there while every amount stays whole.
Its fixed law tables are prepared before stepping. Funded/absorbed ray owners
currently reject delayed carrier plans; phased/attenuating self-exclusion composes with
absorption only. See the exact candidate bounds.
A ray field may set `"metric": "euclidean"` (`euclidean-ray-pace-v1`): rays
wait at Nodes by their heading's pace, never faster than one link per tick, so
every heading covers equal Euclidean distance per tick. Historical (deleted on
2026-09-17, issue #164 bucket B.5): a ray field with `claim`
(`claim-gather-ray-field-v1`) gathered a captured train to the Node that
captured it by a claim flooding Node to Node at link speed, and the global
`bonded-ray-field-v1` reference supplied nonlocal outcomes through a bond
registry. Both went with the shared quantum resource (Q-ORACLE-1): there is no
register at any Node, no owner answers at a distance, and no occupied channel
or capacity rule holds a ray back (Highlights 5.1 and 5.4; superseded for
real rays on a lane on 2026-09-18 by Highlights 5.4, point 25: a Port is two
lanes, one real ray and one shadow per owner per lane, a thing stepping into
a lane only if it is free, with no queue and no wait).
Schema version 1 retains those conservative spatial laws. Schema version 2
selects finite attenuation, derived from the schema version independently of
user-defined names. Every spatial field requires a bounded integer ratio
`0 <= p < q`; each original packet/octant/component is attenuated to
`sign(v) * floor(abs(v) * p / q)` on completing an interior link, before arrival
packets merge. By default (`finite-localizing-v1`) each removed fraction is
deposited as stationary stock at the receiving Node, preserving signed inventory:
it comes to rest as whole units at known Nodes. The explicit
`"residue": "dissipate"` option (`finite-dissipative-v1`) records removed
fractions as loss instead. Immutable baselines are exempt. Per-record finite allowances bound absolute
emission and opposite coupling reactions; they are not physical reservoirs.
The complete laws belong to spatial fields and
spatial response.

The version 2 combined balance is initial inventory plus committed sources minus
committed signed dissipation and escaped quantity, where deposits count as
inventory and dissipation is zero under the default residue. Integer attenuation
can change vector direction and does not preserve momentum or energy. Coupling
remains equal-and-opposite at its atomic commit, before subsequent attenuation.
Fixed finite initial records and allowances bound dynamic input; after the last
nonzero input, moving spatial stock comes to rest after finitely many links. This does not require carriers to stop
or immutable backgrounds to disappear. Schema 1 rejects the new decay and budget
keys, and named historical research models retain their own integer rules.

The optional initialization `boundary` is `periodic` by default or `open`.
Periodic topology wraps independently across all six faces, preserving port,
vector, full link time and ownership. Open terminal packets remain counted while
in flight, then their unchanged payloads leave the simulation at link completion.
There is no simulated outside receiver, decay or receive cost. The boundary law
is independent of schema version and named in metadata. Combined accounting is
`current + dissipated + escaped = initial + sources` for declared conserved
quantities; spatial-only accounting also includes committed reactions and, for
nonconserved local fields, configured transformations. The escaped ledger is diagnostic,
never a global repair or a physical input. See the schema.

Optional atomic pair `interactions` assign multiple fields from one frozen input
pair, enforce each declared invariant and conserved-field pair balance, then
enter the existing delayed local commit together. Generic integer dot products,
matrix transforms and scalar comparisons are initialization operations. Exact
division cannot round away a failed invariant. The configured unequal-mass
elastic example and its limits are specified in the disturbance contract; they
do not change the historical collision laws below or introduce a built-in force.

The source/self-force, scalar node, particle, turning, variable-link and collision
laws below were requirements of explicitly named historical research APIs whose
implementations were deleted on 2026-09-17 (Highlights sections 3.3, 3.4, 3.5,
3.19, 3.20, 5.1 and 5.4; issue #164, bucket A). They are retained as the record of
those candidates and do not define the active generic schema. Shared locality,
integer bounds, read-only diagnostics and honest failure reporting still apply.

## Local energy and momentum audit

The optional initialization `conservation` member defines scalar energy and
three-component momentum measurements for property-selected carrier records and
joint spatial values. The local conservation contract
owns its schema, additive-owner interpretation and restrictions. The first
contract permits zero-baseline closed systems and measured open-boundary escape;
it rejects external sources, decay and native-event composition.

Read-only inventory snapshots bracket committed field phases, arrivals, complete
carrier cycles and escapes. Local residuals compare node changes with measured
actual link flux, including nonlinear packet merging and later carrier updates.
This host audit does not repair a transition, supply physical inputs or charge
model computation. Detection after an event does not roll back its committed
owners. Per-rule precommit guards remain a separate mechanism.

Passing the audit establishes the configured balance on the inspected transitions.
The law still needs independent admitted-domain and physical-interpretation
evidence. Additive component conservation, local coupling and labels such as
energy, spin or gravity do not provide that evidence by themselves.

## Historical causal outward streams

The historical `causal-octant-stream-v1` candidate, deleted on 2026-09-17, replaced
scalar transport with exactly fourteen nonnegative bounded integers per stream node:
eight octant populations and six delivered directional amounts. Ordinary node
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
Its separate candidate contract document was deleted with it.

The canonical implementation is the `event_universe` Python package under `src/`.
The historical scalar model identifier was `scalar-field-v10-contact`; its
implementation was deleted on 2026-09-17.
The active generic user identity is supplied by initialization; its schema version
separately identifies conservative or finite attenuating spatial policy, and the
decay residue distinguishes localizing from dissipative attenuation.
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

The active generic simulator also supports an explicitly selected
bounded rational expression candidate. Only inside
those opt-in regions, canonical numerators/denominators allow 127 magnitude bits
and temporaries allow 255 magnitude bits, with bounded integer arithmetic and
fixed model work charges. Persistent payload bounds, legacy integer expressions,
and the historical constraints below remain unchanged. This is a numeric
contract extension, not unbounded host arithmetic or a relaxation of locality.

The numbered record/source/response constraints here describe the historical
scalar models whose named APIs were deleted on 2026-09-17. Their
five-register node and sixteen-register particle schema is not universal. The
active generic state and its smaller payload bound are defined in
the disturbance contract.

1. All dynamic physical registers and arithmetic are integers. No floats, true
   division, trigonometry, square roots, logarithms or vector normalization occur
   in `core/` or `fields/`. Rational factors use integer numerators, denominators
   and retained integer remainders.
2. Physical registers are bounded to `[-2147483647, 2147483647]`. Intermediate
   arithmetic is bounded by the working bound, `[-9223372036854775807, 9223372036854775807]`.
   Exceeding a bound raises `OverflowError`; neither wraparound nor saturation is
   used. Python is the host representation, with explicit bounds at the model
   and commit boundaries; arbitrary precision is not an escape for physical state.
3. A node contains exactly five integer fields:
   `phi, px, py, pz, remainder`.
4. A particle contains exactly sixteen integer fields:
   `x, y, z, px, py, pz, move_budget, axis_phase, force_rx, force_ry, force_rz,
   last_update_tick, mass, momentum_den, move_budget_den, last_collision_tick`.
   The v13 section below defines the four appended registers and their defaults.
5. The physical neighborhood is exactly `+x, -x, +y, -y, +z, -z`.
   Each local rule receives only fixed records and six neighbor values.
6. Every occupied node has exactly `K = max_particles_per_node` slots, with
   `-1` denoting an empty slot. K is fixed for a world. No source maps, growing
   histories or dynamically expanding particle lists are stored per node.
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

In the historical scalar candidate, deleted on 2026-09-17, the engine owned
addresses, fixed occupancy, scheduling and commits; generic field code owned
scalar arithmetic and gradients; generic dynamics code owned the shared
response, local momentum exchange and movement calculations; and one model
adapter selected their policies and mapped them to physical records: six equal
neighbor weights, no local retention, occupancy-based source, nonnegative scalar
values and dominant-axis transverse response. No copied formulas were maintained
in the adapter or compatibility imports. The active package keeps the same
division of responsibility: API assembly is checked for accidental runtime
arithmetic, alongside absolute and relative import boundaries.

The field and turning components could be supplied independently to that
candidate's API, with denominators from the same configuration used by state
audits. Custom implementations had to be local, deterministic, bounded and
without evolving private state. Measurement code reads output and records
evidence (the host's tools; a measurement of the law is the detector's click,
an action, [POSTULATES.md](POSTULATES.md) section 10, the model owner, 2026-09-23, record 1139). No local law receives a world object or knows source identities at
remote nodes.

That engine received field activity as a predicate instead of interpreting the
candidate law's changes itself, and a law had to preserve the all-zero sample
when neighbors and source are zero, as required by sparse scheduling.

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
GameBoard symmetries. Field-momentum storage is the existing local exchange model;
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

There is no model-computation exception: the shared quantum resource
(Q-ORACLE-1) was deleted on 2026-09-17 under Highlights section 3.18, and
ordinary field, self-field, movement, force and geometry locality hold without
exception.

Review must identify each input's owner, causal delivery, fixed record count and
maximum local loop bound. The architecture gate rejects known world/replay member
access in calculations; six-read tests check the baseline neighbor boundary.
These are partial checks, not a proof for arbitrary callbacks or dynamic Python.

The physical rule and fixed-slot local work have constant bounds for fixed K
and fixed-width numbers. Sparse dictionaries, sets, global sweeps and
measurements do not have strict constant total runtime. The Python storage
adapter does not provide worst-case constant-time hash lookups. Empty historical
occupancy keys and materialized nodes are retained to preserve legacy scheduling;
world memory can grow as new nodes are visited. History collection is optional
and external; JSONL recording streams it to disk.

## Required regression gates

- Exact signed division and remainder accumulation at denominators 1, 12 and 64.
- Invalid input, physical-register and working-bound overflow rejection.
- Static numeric audit over every physical module (`diagnostics/numeric_audit`,
  `tests/test_architecture.py`): `core/` integers only, no numeric library;
  `events/` integer numpy permitted and nothing that leaves the integers (a
  float literal or dtype, true division, the square root, the means, the
  transcendental functions and constants), beside its runtime bounds; the
  artifacts' writer `events/run.py` (path joins, no physics) outside it as
  the import gate exempts it; and import-boundary checks.
- Explicit numerical expectations in `docs/TEST_EXPECTATIONS.md` for every
  active contract.

The gates of the historical scalar candidate (stationary self-force, one-edge
propagation, per-particle update order, matter-field exchange, offset-pair
turning, contact response, recording invariance and component replacement
through its API) were deleted with that candidate on 2026-09-17.

## Historical opt-in quantum contracts — Q-ORACLE-1 (deleted on 2026-09-17)

The shared quantum resource, its terminal trial and its bridge were deleted on
2026-09-17 with Highlights section 3.18 (issue #164, buckets B.1 and B.2). The
contract below is history.

The model assumption `deferred-unit-cost-oracle-v1` was defined in POSTULATES.md.
A successful query returns fixed-size integer records with model_cost=1 and
world_ticks=0, regardless of host evaluation work. It never calls Engine.step
or writes physical state. Host counters and budgets remain distinct from cost.
This original sidecar adds no automatic polling. The later Q-ORIGINS-3 extension
bounds origin-status inspection to six entries per participating Node per native
tick; its explicit encounter instruments remain distinct from pure queries.

The optional sidecar has a single owner for its bounded deferred graph, cache,
query accounting and terminal state. Node records have ten integers and at most
two parents. Amplitudes have two integers; weight is their squared norm. Public
registers and intermediate work obey the same 32-bit and 64-bit bounds above.
max_nodes, max_eval_nodes and max_cached_results are explicit positive budgets.
Failure raises an exception without manufacturing an outcome. Python allocation
and graph traversal are host work, not strict constant-time node calculations.

Recorded physical graph edges use an unwrapped 3D chart: same-node or one cardinal
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

Only the quantum owner's single terminal record stores the readout. No Engine-native
physical event is added, no source or field is changed, and no post-detection
excitation continues. No general entanglement, Bell, no-signalling, energy or
momentum claim follows. The trial contract document was deleted with it.

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

The optional local reception probe records completed
inputs at one node with a completed-node-cycle counter. Six receiver ports
identify the last hop, not distant source positions. Archive prefixes are
captured alongside frames; global tick and state remain audit information.
This is a passive diagnostic, not human optics or a derived proper-time law.

Runs are headless by default, including ordinary tests. The active CLI requires
an initialization file. Metadata and JSONL events do not depend on Matplotlib,
Pillow or animation capture.

Only an explicit visualization request enables output frames and rendering.
`--visualize` requests the active runner's optional view. A generic view must
label configured fields rather than interpreting their names as scalar phi or
particle momentum.

Pytest enables presentation-only tests only through `--visualize-runs`. Without
that flag, physical assertions still execute and no HTML/GIF run reports are
generated. Requested frame stride changes recording
only, never the physical update interval.

The generic local commit and failure behavior was defined in
docs/DISTURBANCES.md until the generic disturbance simulator's deletion on
2026-09-19; the active engine's refusals and failures are in
[the engine's bookkeeping](docs/ENGINE.md). The following field-phase description
applied to the historical scalar models deleted on 2026-09-17.

Field proposals are validated before the field phase commits. Particle-field
proposals are validated before that local exchange commits. A whole tick is not
transactional: if a later operation fails, previously committed local operations
remain available for diagnosis. The world then rejects further steps. On such
failure the runner saves diagnostic output and re-raises the error.

Runtime validation uses exceptions and remains active under `python -O`.
Reports distinguish checks actually performed from architecture descriptions
and physical claims not established by the tests.

### Display readability and playback

The following visual conventions applied to the historical scalar/particle
renderer, deleted on 2026-09-17; they are kept as the record of that display
contract. They do not assign meanings to generic field names or require
visualization for a run.

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
two cardinal GameBoard steps between displayed frames. A multi-node jump across a
boundary shows both markers; a periodic symbol must not hide that jump.
Trails break at coordinate discontinuities. Sparse sampling is ambiguous, so
a marker alone is not proof of faster-than-c motion; inspect consecutive ticks.

The combined scalar field uses a fixed amber scale throughout an animation.
A square-root display mapping lifts weak values; color is not a linear field
measurement. Wide soft halos improve visibility without changing physical
field range. There is no invented per-particle attribution of a shared field.
The floor and two walls have twice as many visual grid subdivisions; this does
not change the GameBoard or the simulation resolution.

The exported GIF stops at the final frame instead of resetting time through
automatic replay. Reloading its HTML replays it from the start. This playback
contract applies to both slices and 3D views. None of these display operations
smooths physical positions, cancels self-force or changes a simulation record.


## Historical local-link geometry candidate — v11

The user-authorized link extension was `scalar-field-v11-local-links`; its named
API, CLI scenario and the frozen v10 reference were deleted on 2026-09-17. The
five/sixteen-register schemas above describe the historical scalar field and
particle records.
The v11 candidate additionally has fixed `LinkNodeState` and `Transit` records:

- Six received scalar integers; six active length integers; six packets of
  `(value, proposed_length, remaining)` = 30 link integers per materialized node.
- `(direction, departure, length, due)` = four integers per in-flight particle.
  The particle remains in its origin's fixed occupancy slot throughout transit.
- Three canonical owned edges: +x,+y,+z. Negative edges are local copies. Both
  endpoints may propose changes; ownership must not bias the law by direction.
- Length proposal: `base + (stretch_num*(local_phi+received_phi))//(2*stretch_den)`.
  Defaults: base=100, stretch_num=1, stretch_den=1. A pair of field values 10,10
  gives length 110, representing 1.10 original node spacings. The base is a
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
- A full target blocks arrival; it neither deletes a particle nor grows node
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

The historical application runner validated particle momentum after every completed tick
when the initial world contains exactly one particle and entirely zero field
records. Its own source stays active. Any change in its initial momentum raises
`InertialMotionViolation`, terminates the application run and saves the failing
tick, event trace and failed metadata. If visualization was requested, preserve
the failure frame and an HTML heading explicitly marked FAILED RUN.
The check is independent of display sampling and never clears remainders, changes
momentum or disables sources. Multi-particle and initially seeded-field worlds
are not classified as isolated by this check.

This is read-only diagnostic rejection, not a corrected physical law or a proof
of straight trajectories. Direct engine callers still received the
underlying model behavior. Model acceptance requires the separate isolated-motion
gate; a test that confirms rejection does not turn that failing physical gate
into a pass. Existing baseline physical requirements remain unchanged.
No threshold exempts a one-unit impulse.

## Historical mass and elastic point contacts — v13

The user requested same-point particle collisions and then an individual mass
parameter. The scalar candidate selected `scalar-field-v13-mass-elastic-contact`
and the linked candidate `scalar-field-v13-mass-elastic-local-links`; both named
APIs were deleted on 2026-09-17. Both accepted `add_particle(..., mass=...)`. Mass is a fixed positive integer in simulation
mass units, default 1. Zero, negative, non-integer and overflowing masses fail
before insertion. It is supplied inertial mass, not emergent mass or a claim
about gravitational charge. The existing occupancy-based scalar source and field
coupling are unchanged. Collision-free mass-1 v10/v11 behavior remains available.

### Contract and independent quantities

| Part | Contract |
| --- | --- |
| Law | Classical elastic backscattering: reverse relative velocity in the pair center-of-mass frame |
| Inputs | The two co-resident particles' three momentum numerators, denominator and positive mass; no remote particles or field solve |
| Evolving state | Four added particle integers: mass, momentum_den, move_budget_den, last_collision_tick; fixed K-by-K contact flags owned by each contacted node |
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
multiplied by momentum_den, and the node receives the opposite physical impulse.
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

Each node inspects only its K resident slots, at most K(K-1)/2 pairs. A pair's
contact flag prevents repeated bouncing while it remains together. An actual
move clears flags incident on the departing and arriving slots. Each particle
scatters at most once in a tick. More than two co-residents are resolved in slot
order as disjoint pairs per tick; remaining fresh pairs can scatter on later
ticks. This is a deterministic local multiparticle policy, not a unique
simultaneous many-body solution or a permutation-invariance claim. Capacity
blocking remains distinct; K=1 cannot host a two-particle contact.

The contact flags are K*K integer registers per contacted node, independent of
world size and elapsed time. Global address sweeps and Python dictionaries remain
host costs. There are no per-source maps, growing local histories, external
queries or quantum exceptions in this law.

Point contacts do not detect crossing between sampled addresses, overlapping
finite-radius surfaces or meeting midway along a link. The GameBoard's capped L1
speed and field law are not relativistic mechanics. Exact classical pair energy
conservation therefore does not establish relativistic energy conservation or
energy conservation for the entire field-coupled simulator.

### Output and compatibility

The historical runner's `collision`, `collision-masses` and `collision-links`
scenarios exercised this feature. The 3D HTML/GIF renderer is used only
when visualization is explicitly requested. Scenario `masses`
contains one mass for each seed (or is empty for unit defaults). Metadata records
these masses, collision selection and the explicit model identifier. In 3D,
particle labels show mass and velocity arrows use the mass and momentum scale.
`particle_collision` JSONL events include named before/after records and their
denominators. Legacy force events keep their tuple layout; their momentum fields
are numerators at the denominator from that particle's latest collision record
(or 1 before any collision). The legacy trace recorder's `collisions` meant blocked
moves; actual scattering events were in `collision_records`.

The original twelve particle fields keep their order. Four new fields append
with defaults (1,1,1,-1). Fixed-schema and physical behavior checks cover current
records. Frozen-v10 equality is no longer an acceptance gate; its archived source was
deleted on 2026-09-17.

## Historical balanced-motion and local-halo candidate

`scalar-field-v12-balanced-halo`, whose named API was deleted on 2026-09-17, combined
interleaved integer movement with a synchronous local scalar cancellation phase.
After every particle has completed its response and optional hop, the phase sets
`phi` and `remainder` to zero in the union of the six neighbors of its previous
and current positions. It retains field momentum. Every proposal validates before
commit; baseline v10 is unchanged.

The scheduler may visit at most twelve targets per particle and coalesces overlaps.
The local rule receives one fixed node record. It adds no physical registers,
source map or history and satisfies LOCALITY-1 for fixed K. The candidate must keep
isolated particle momentum exactly at all tested ticks and retain nonzero external
response. Its exact inputs, results and limitations were recorded in a candidate document
deleted with it.


## Historical quantum event network — Q-EVENTS-1 (deleted on 2026-09-17)

The event network and its document were deleted on 2026-09-17 with the shared
quantum resource (Highlights 3.18 deleted, 3.20: no register). The contract
below is history.

The selected finite candidate was `deferred-event-network-v1`. A fresh `DeferredQuantum` owner bound
one `EventNetworkConfig` before creating legacy scalar nodes. The two state
representations cannot be mixed in one owner. Existing terminal/Focus consumers
retain their old API and behavior unless the new representation is selected.

The event backend owns immutable local matrices, current register head IDs, joint source
or checkpoint amplitudes, earlier outcome constraints and bounded decision records.
Ordinary nodes do not acquire this growing host state. Coherent steps append only
disjoint one-node or nearest-neighbor operations. Queries return fixed-size local
weights at the current tick; full-state inspection is host-only diagnostic work.
Prior correlated records are included in a conservative dependency closure.
This is sufficient pruning, not a proof of the smallest possible contraction.

An explicit one-node instrument supplies one to four outcome matrices whose
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
are not a remotely readable physical register or a classical communication channel.
The later native contracts define their limited Engine interface and origin
polling. Quantum-field feedback, a universal measurement trigger, a physical
free-momentum law and a derived classical limit remain outside this backend.
The 3:4 matrix is a
test fixture and explicit demonstration parameter, never a hidden default law.
## Executable entity profiles and bounded conversion

The host-side entity catalog adapter selects explicit
profiles and emits ordinary validated initialization. It adds no physical-name
dispatch, enlarged local registers or alternate engine. Representation probes
do not certify physical field dynamics.

The optional `interactions.output_types` contract is defined in
local conversions: exactly two outputs replace the
same two local slots, with complete explicit payload assignments, exact declared
balances, zero carried routing progress and the documented schema/ownership
restrictions. Invalid proposals cannot install partial converted records.

## Historical native causal event programs — NATIVE-EVENTS-1 (deleted on 2026-09-17)

The `event_program` member, its parser and runtime and their document were
deleted on 2026-09-17 with the integration layer. The contract below is history.

The optional native program bound the selected
Q-EVENTS-1 owner into the primary Simulation through a generic local protocol.
Physical causes and computational dependencies retain distinct permissions in
one bounded immutable identity store. Local nodes and packets keep fixed-size
references only. Path cost includes the selected mechanical law, a local trigger
inspection and code writes, and one model unit per successful oracle request.
The existing budget delay applies once to the entire local cycle; neither
waiting nor commit charges it again. Host work remains separate. Independent
spatial-field composition is currently rejected for this candidate, not silently
run without provenance. Existing configurations without event_program are unchanged.

## Historical finite quantum registers and channels - Q-REGISTERS-2 (deleted on 2026-09-17)

The register extension, the quantum entity profiles and their document were
deleted on 2026-09-17 with the shared quantum resource. The contract below is
history.

The explicit `local-quantum-events-v2` contract permitted dimensions two to four,
colocated named degrees of freedom, unobserved complete channels and grouped
observable outcomes under existing bounded arithmetic and local support rules.
Only an observable result is sampled. Inaccessible alternatives are summed as
mixed-state contributions, not independently chosen paths. Classical trajectories
still incur native cycle cost; zero oracle ticks do not imply zero host work.
The entity compiler's explicit quantum selection adds no species-name dispatch.
Independent spatial-field clocks and general field/particle dynamics remain
outside this candidate. Legacy binary inputs retain their original behavior.

## Historical localized contact quantum/classical transfer - Q-CONTACT-1 (deleted on 2026-09-17)

The contact program, its runtime and their document were deleted on 2026-09-17
with the integration layer. The contract below is history.

`localized-contact-quantum-v1` composed the ordinary runner, fixed spatial clock
and finite deferred quantum owner under the localized contact contract. An actual local
unknown-momentum contact creates its origin at commit; absorption returns one
held localized record. Conserved template quantities have exactly one ordinary
or coherent owner. Delayed alternatives preserve local field reactions and every
coupled resident. Classical emission occurs only while the source is localized;
its previously emitted packets keep their causal evolution.

The profile validates finite emission budgets, number-preserving local gates,
complete absorption instruments and domain identity in the semantic owner as
well as JSON. It does not support the shared field-delay clock, Node execution,
the passive classical-only conservation audit, automatic exterior quantum modes
or reciprocal classical-field action on delocalized matter. Read-only playback
separates possible origin support from particles, field inventory and probability.

## Historical causal ordinary sources from quantum contacts - Q-CAUSAL-SOURCE-1 (deleted on 2026-09-17)

The causal contact runtime and its document were deleted on 2026-09-17 with
the integration layer, and the source-envelope modules on the same day under
Highlights section 3.5 (issue #164, bucket B.3). The contract below is history.

`causal-contact-fields-v1` selected the causal source contract, retaining Q-CONTACT-1's
local preparation, absorption and single inventory ownership. Each participating
Node additionally owns one bounded complex source envelope and finite emission
allowances. Its source is full configured emission times local squared magnitude.
Rational complex evolution preserves phase using number-preserving matrices and
their nonzero vacuum coefficient; no remote normalization is performed.

Amplitude and terminal packets cross actual Links and commit after tariff-derived
Node delays. Localized capture creates one full-strength ordinary source, ends
the colocated envelope and initiates causal termination. A local null zeros only
the local envelope. Quantum origin status and conditional oracle results never
select remote ordinary source values, timing or cancellation. Pending outputs
retain bounded data and local invalidation guards; no formulas enter NodeState.

After measurement the envelopes are a retarded, potentially unnormalized source
approximation. Their sum is not conserved charge. Existing emitted field stock
continues under its configured laws and separate injection accounting. The linked
contract defines the finite domain, clock, transport and conservation limitations;
the older localized-only profile is unchanged.

The explicit `null_notices` option adds one rational weight scale per Node, six
pending-notice slots, a fixed six-entry bank of applied notice identities and
six notice output slots, so the envelope output bank has eighteen fixed slots.
A null with local scaled weight `p < 1` multiplies the local scale by `1/(1-p)`
and sends that factor as a notice through the domain Ports; receivers apply it
after their control delay and forward it away from the arrival Port. Emission
uses the scaled weight, clipped at one. Without the option the scale stays one
and no notice is sent. The candidate does not read the quantum owner and does
not remove the departure for several excitations.

The explicit `field_phase` propagation operation replaces one one-mode matrix
by a fixed table `diag(vacuum^|n|, unit^|n|)`, conjugating both coefficients
for negative `n` so the relative phase is `(unit / vacuum)^n`,
with `|n| <= max_exponent <= 12`. At the gate's schedule tick the Node reads its
own start-of-cycle value of one spatial field component and sets `n` to that
value divided by `divisor` toward zero; an exponent beyond the table stops the
run. The ordinary envelope gate and the quantum owner's recipe for that epoch
use the same matrix. The read costs one `read` tariff; no evolving state is
added to NodeState and the field is not changed by the gate.

An envelope emission rule with `source: false` is funded: its amount is booked
as an internal transfer from the wave's conserved stock of the same field, the
quantum inventory decreases by what the modes have paid, the localized output
receives the remainder, and an emission committed after the domain localized
elsewhere is recorded as an explicit external residual. Parsing requires the
causal model, ownership of the field by the source and output types, and
`modes x budget <= stock`. Funded octant emission by ordinary records is
admitted under both schemas; funded ray emission keeps schema 1.

## Historical recurrent contact outcomes - Q-RECURRENT-1 (deleted on 2026-09-17)

The recurrent contact runtime and its document were deleted on 2026-09-17 with
the integration layer. The contract below is history.

The separate recurrent contact profile,
`recurrent-contact-fields-v1`, composed Q-CONTACT-1 and Q-CAUSAL-SOURCE-1 with
configured outcome effects. Its source supports localized retention and new-wave
transfer; its capture supports null, localization, continuation and a fresh local
origin. Matrix support, completeness, full-domain vacuum and conserved output
inventory are validated before sampling. Conditional commit atomically resolves
the prior origin and creates a new one when selected. Replaying a result cannot
resurrect it. Explicit `max_generations` in 1..6 bounds separately preallocated
ordinary envelope banks. Fixed round-robin emission, causal cancellation,
finite allowances and locally applied nulls cannot use remote generation status
to choose ordinary field values or clocks. See the linked contract for exact
schema, cost, capacity and representation limits.

## Historical quantum origin cells in event spacetime - Q-ORIGINS-3 (deleted on 2026-09-17)

The origin cells and their document were deleted on 2026-09-17 with the shared
quantum resource. The contract below is history.

The explicit native v3 candidate gave every participating physical Node
at most six integer origin references. Origins propagate only through configured
local quantum operations, subject to native Link timing and capacity checks.
The references describe possible causal support; exact amplitudes and correlations
remain in the existing finite quantum owner. Up to thirty configured virtual
registers and their current heads are a separate representation limit.

All past events stay in the shared immutable event spacetime. No separate local
predecessor list or linked-history traversal is maintained. A source-associated
resolution slot is written once by a successful configured terminal outcome,
under the same transaction as conditional probability preparation and record
commit. Relevance is checked before another contender samples. Each Node prunes
its own resolved origins on its next native tick, without an eager global sweep.
Every v3 operation names its participating origins; unarrived support cannot
execute it. A retired gate is suppressed without a quantum operation payload or
register-time change only after certifying invariance of the full retained joint
density. A retired instrument also requires exactly one possible outcome equal
to its explicit `null_outcome`, with unchanged full density. An unsafe cancellation
fails explicitly. Native null certificates are checked again after the target
head changes, even without a fresh arrival. Untagged gates and legacy carrier bindings are
rejected in this profile. Origin IDs also remain explicit ledger provenance,
separate from the quantum recipe dependencies.

Nonterminal outcomes preserve conditional continuation, including unresolved
momentum after a position record. Only explicit instruments sample. Coherent
interactions and a lack of classical knowledge do not supply a universal collapse
law. Checkpoints retain complete correlated state, origin identity, immutable
past records and each register's Link readiness. Direct status checks use bounded
local work; tensor evaluation, serialization and total event storage remain host
costs under Q-ORACLE-1. Cancellation certification is additional bounded quantum
evaluation, not an O(1) status lookup. Its audit checks cost one model operation
each and are included once in the ledger total, separate from the carrier subtotal;
they do not create a physical observer or delay channel. Interaction lists name
one to six origins, and one origin may represent several disturbances. No new
conservation law or infinite-memory claim follows.
