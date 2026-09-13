# Initialization-defined disturbances

The optional top-level `observer` member configures a passive reception probe in
the same input file. See [local observer](LOCAL_OBSERVER.md) for placement, limits
and runner behavior. It is validated for both schemas and excluded from physical state.

The optional [bounded rational and balanced-routing contract](RATIONAL_PARTICLES.md)
defines rational expression projections, exact dynamic movement divisors and
local consistency checks. Old integer arithmetic and cyclic routing remain
available with their original behavior; new particle candidates select their
new settings explicitly in initialization JSON.

This is the contract for the active generic simulator. `Simulation` takes a
validated `InitialState`; no built-in mass, charge, particle or force law is
selected when initialization is missing. Names and candidate laws come from a
JSON file. A field named `mass` receives exactly the same treatment as any other
field with the same declared structure and rules.

Optional [configured spatial fields](SPATIAL_FIELDS.md) separate emitted fields
from carried records. They add implicit baselines, bounded outward octant
transport through six faces, continuous declared sources and combined accounting.
They do not enable an unproved self-field subtraction law.

Optional [spatial couplings](SPATIAL_COUPLINGS.md) connect local spatial values
or scalar directional flux to a carried field through atomic exchange or exact
discrete rotation. Their response precedes ordinary updates and movement planning;
the field receives the opposite change when the frozen carrier proposal commits.

The fixed-physics `ScalarSimulation`, `LinkedSimulation`, `BalancedSimulation`
and `CausalStreamSimulation` APIs remain explicitly selected research models.
Their historical record schemas and physical assumptions do not constrain the
generic payload schema below.

## Run and initialize

```bash
python -m event_universe --init examples/basic.json --output artifacts/basic
python -m event_universe --init examples/basic.json --ticks 20 --output artifacts/basic-20
```

The file contains the run duration; `--ticks` explicitly overrides it. Missing
initialization is an error. Historical scenarios have a separate explicit
entry point, `python -m event_universe.legacy_runner --scenario ...`.
The active runner writes `initialization.json`, `run.json`, `state.json` and
`events.jsonl`: copied input, source identity, completion or failure, final state
and local events. Runs are headless by default. Visualization requires
`--visualize`; ordinary execution does not capture frames or import optional
rendering dependencies. The active runner rejects a nonempty output directory.

```python
from pathlib import Path

from event_universe import Simulation
from event_universe.initialization import load_initial_state

initial = load_initial_state(Path("examples/basic.json"))
world = Simulation(initial)
world.step()
```

The complete example is [examples/basic.json](../examples/basic.json). Its names
are illustrative data, not a list of recognized physical entities.

## Concepts and owners

| Concept | Meaning |
| --- | --- |
| Field definition | Named scalar or three-component vector, units, sign, scale, extensivity and conservation declaration |
| Disturbance type | Fields carried together, defaults, local updates and transport rule |
| Disturbance record | One local occurrence with field values and bounded routing/allocation state |
| Cell | Fixed resident slots, one pending local proposal and fixed coupling remainders |
| Transfer | A record owned by an outgoing link, with type, values, port and arrival time |
| Coupling | Configured local exchange between records, or between a record and a spatial field |

The six ordered ports are `[+X, -X, +Y, -Y, +Z, -Z]`. They identify the direction
of transport. A vector value still has three components; it is not automatically
the six port weights. A negative field component and travel through a negative
axis are independent facts. Oppositely directed transfers retain their separate
channels rather than being replaced by their net vector.

An absent carried field is zero. Spatial fields instead use their configured
baseline, which can be nonzero. Presence alone does not create a persistent
source: an update rule or an explicit `emissions` rule must declare injection.
Multiple co-resident records need not be merged: whole-record movement preserves
separate carriers and their different directions.

## JSON schema versions 1 and 2

| Top-level member | Contract |
| --- | --- |
| `schema_version` | `1` for conservative spatial laws, or `2` for finite dissipative spatial laws |
| `model_id` | Explicit identifier for this configured candidate |
| `shape` | Three positive bounded integer domain extents |
| `boundary` | Optional `"periodic"` or `"open"`, default `"periodic"`, in either schema version |
| `slots_per_cell` | Fixed positive resident capacity, at most 32 |
| `link_ticks` | Fixed positive transit time shared by all neighbor links |
| `normal_budget` | Positive ordinary local computation cost `B` |
| `ticks` | Nonnegative requested simulation duration |
| `operation_costs` | All nine primitive prices, each a positive integer |
| `fields` | Between 1 and 16 unique field definitions |
| `disturbance_types` | Between 1 and 16 unique disturbance definitions |
| `couplings` | Optional list, at most 32 local exchange rules |
| `interactions` | Optional list, at most 32 atomic pair transactions |
| `seeds` | Positions, disturbance type names and optional value overrides |
| `spatial_fields` | Optional outward fields with baseline and branch weights, or schema 1 local fields; version 2 requires decay per field |
| `emissions` | Optional hold/move source expressions with injection accounting; version 2 requires a budget per rule |
| `spatial_seeds` | Optional initial octant populations at named lattice cells |
| `spatial_couplings` | Optional list, at most 32 local field-response rules; version 2 requires a budget per rule |
| `field_groups` | Optional metadata groups referencing existing scalar/vector fields, at most 16 |
| `field_rules` | Schema 1 only: at most 32 atomic multi-field retained/six-output rules |
| `spatial_interactions` | Schema 1 only: at most 32 joint field/carrier transactions with delayed-commit guards |
| `event_program` | Optional bounded causal graph; `causal-events-v1` records carrier and spatial events without quantum rules; see [graph configuration](EVENT_GRAPH_CONFIGURATION.md) |

The authoritative contract for local field selection, group semantics, rule
expressions and joint transactions is [LOCAL_FIELD_RULES.md](LOCAL_FIELD_RULES.md).
Those rules can read existing outward fields while writing only fields explicitly
configured with local transport. Their absence preserves existing behavior.

Names and unit labels are nonempty strings of at most 128 characters. All names
must resolve within this file. Unknown keys, duplicate JSON keys,
duplicate names and incompatible values fail validation. Seeds must lie inside
the configured shape and fit the local slot capacity. The file is data, not
Python source; it cannot import a law, evaluate source text or invoke callbacks.

### Schema version and candidate identity

Version 1 records `conservative-outward-v1` for outward-only spatial runs and
`configured-local-fields-v1` when local transport is selected. Existing outward
runs preserve conservative spatial transport, unlimited declared emission
and unlimited spatial response. It rejects `decay` and spatial-rule `budget`
keys. Version 2 selects the explicit `finite-dissipative-v1` policy: every spatial
field requires `decay` with bounded integers `0 <= retain_numerator <
retain_denominator`, and every emission and spatial coupling requires a
nonnegative scalar/vector `budget` in its target field's units. Omitting these
keys is an error in version 2. A version 2 configuration without spatial features
is valid and retains the ordinary disturbance laws.

The runner records this policy from `schema_version`; the user's `model_id`
remains a free configured identity and cannot select behavior through its name.
See [spatial fields](SPATIAL_FIELDS.md) for per-completed-link decay and clipped
emission allowances, and [spatial response](SPATIAL_COUPLINGS.md) for atomic
whole-action allowances. Neither allowance is a conserved physical reservoir.
Ordinary local update and paired-exchange rules retain their existing contracts.

### Domain boundary

The top-level `boundary` setting applies equally to carried disturbances and
spatial-field packets. It is independent of the schema's conservative or
dissipative policy. Omitting it preserves the existing periodic behavior.

| Setting | Transfer across an outer face |
| --- | --- |
| `"periodic"` | Arrives at the opposite side of the same axis, with the same travel direction and payload signs |
| `"open"` | Leaves the simulated domain and is recorded as escaped quantity |

For shape `[3,4,5]`, a +X step from `[2,1,1]` wraps to `[0,1,1]` under periodic
boundaries. Under open boundaries it has no destination inside the world. Interior
steps are identical under both settings. Open does not mean reflection, a growing
domain, or an unrecorded deletion. No off-grid cell is created, and no escaped
influence re-enters from an opposite face. An immutable baseline exists only
inside the declared shape and is not an outgoing source.

An outward transfer remains owned by its terminal link for the normal
`link_ticks`, then its unchanged signed quantities are recorded as escaped.
There is no outside receiving cell, so this terminal link performs no destination
receipt, merge or decay. Schema 2 decay applies only to links with a destination
inside the domain. For example, a component of 1 with zero retention escapes as
1 across an open face; the same component delivered to an interior cell instead
loses 1 to decay. Interior and escaping quantities remain separate in accounting.

Use `"boundary": "open"` alongside the other top-level initialization members.
Unknown names, null values and non-string values fail validation. Initial
positions must still lie inside the shape; periodic mode does not wrap invalid
seed coordinates. Historical research APIs retain their own topology contract.

### Field definitions

```json
{"name": "inventory", "components": 1, "units": "unit",
 "signed": false, "conserved": true, "scale": 1, "extensive": true}
```

`components` is 1 or 3. JSON scalar values are integers; vector values are
three-element integer arrays. `signed` controls permitted mathematical signs.
`scale` is a positive declared denominator, default 1. Units and scale describe
the quantity; the evaluator does not infer dimensional consistency or convert
between units automatically. Rules must use compatible scales explicitly.

`extensive`, default true, means additive amounts may be divided among outgoing
records. A conserved field must be extensive. A direction or other intensive
attribute can declare `extensive: false` and move with a whole record; splitting
such a record is rejected. This avoids treating an attribute as divisible stock.

Mathematical component magnitudes are bounded by `1_073_741_823`. Stored payload
components use positive integer codes: nonnegative `v` maps to `2*v+1`, and
negative `v` maps to `-2*v`. Thus zero maps to 1. Signed temporary arithmetic is
bounded separately; addresses, counters and schema indices are control state,
not additional physical payload components. Bounds apply before commit.

### Disturbance types and seeds

```json
{"name": "carrier", "fields": ["inventory", "heading"],
 "defaults": {"inventory": 12, "heading": [2, 1, 0]},
 "transport": {"mode": "move", "direction_field": "heading"}}
```

The referenced `heading` must be declared as a three-component field. Seed values
override defaults only for fields owned by the selected type. Unspecified owned
values start at zero. Defaults and seed overrides share the same validation.

```json
{"position": [2, 2, 2], "type": "carrier", "values": {"inventory": 6}}
```

### Transport

| Mode | Result |
| --- | --- |
| `hold` | Retain the record in its cell |
| `move` | Transfer the whole record to one selected neighbor |
| `split` | Divide extensive field components among up to six outgoing records |

`move` accepts six nonnegative integer `weights` or a `direction_field`, not
both. Direction `(2,-1,0)` yields port weights `[2,0,0,1,0,0]`. Weighted cyclic
selection retains phase; it does not require floating-point normalization.
A zero direction holds the record. Optional scalar `rate` and positive
`rate_denominator` define zero to one hop per base interval. Integer remainders
retain fractional movement opportunity. A rate outside that range fails. The complete basic example derives its rate
numerator from `sum(abs(velocity))` and divides by 12, matching that configured
field's scale. The engine does not supply this relation from the name.

`split` accepts six nonnegative weights with a positive bounded sum. Each
component's magnitude is partitioned exactly, then its sign is applied to the
shares. Equal positive and negative amounts at the same phase therefore use the
same ports with opposite signs and advance allocation phase identically. Phase
remains in the originating local channel. For example, 12 units with
weights `[2,0,1,0,0,0]` send 8 through +X and 4 through +Y. Nondivisible inputs
use retained integer phase, not dropped fractions. The split rule does not
establish a diffusion equation or wave equation by itself.

Split arrivals may combine only with an unlocked record of the same type and
directional channel. Whole-record arrivals occupy distinct free slots. There is
no automatic averaging of velocities or other attributes.

### Local updates and expressions

An update assigns a new value, rather than implicitly adding its expression:

```json
{"field": "inventory", "source": true,
 "expression": {"op": "add", "args": [{"field": "inventory"}, 1]}}
```

Updating a conserved field requires explicit `source: true`. The change is
recorded as source or sink contribution; it does not disappear from the balance.
There are at most 32 update rules across all types. A type cannot update the
same target twice in one cycle. Updates run in declared
order, so later updates in a record see earlier updates to that record.

Expressions are bounded JSON trees, at most 64 nodes and depth 16. Available
operations are `add`, `sub`, `mul`, `exact_div`, `min`, `max`, `neg`, `abs`,
`sum`, `component`, `dot`, `transform`, `gt`, `cross` and `vector`. Literals and field references are also nodes. Binary
component operations may broadcast a scalar to a vector. `sum` reduces to a
scalar; `component` takes a zero-based `index`. `exact_div` requires a nonzero
scalar divisor and an exact integer result. There is no truncating division,
floating-point value, string expression, function call or arbitrary code.

`cross` takes two three-component vectors and checks the working bounds of each
product before subtraction. `vector` constructs a vector from exactly three
scalar expressions. The `received` and `outgoing` leaves have deliberately
restricted local field-rule contexts; see [their contract](LOCAL_FIELD_RULES.md#read-views-and-ownership).

Ordinary update and movement expressions read fields owned by that record.
Coupling expressions can reference the declared participant with `side: "left"`
or `side: "right"`; left is the default. Remote cells, global totals, clocks
outside the modeled scheduler and diagnostic histories are not expression inputs.

### Paired exchange couplings

```json
{"name": "local_exchange", "left_type": "donor", "right_type": "receiver",
 "field": "inventory", "amount": 1, "denominator": 1}
```

Both participant types must own the named field. For each matching local pair,
the amount expression proposes component-wise exchange from left to right.
A positive quotient subtracts from the left and adds to the right; a negative
quotient reverses the exchange. The denominator is positive, default 1. Division
truncates toward zero, with a bounded signed remainder retained in positive-code
storage, so sign reversal does not introduce a rounding bias. Both resulting
records are validated before committing either side. An unsigned field cannot be
driven negative. Each remainder belongs to one rule and current local slot pair;
when either participant departs, that pair's remainder resets to zero. A later
occupant does not inherit it. Retained local split channels keep their remainders.
These are subquantum rounding registers, not additional conserved quantities.

An optional `"remainder_owner": "left"` instead stores one signed remainder per
rule/component on the left record. Whole-record movement carries that fraction
to the next cell. A later matching right record can receive the integer unit
completed by earlier fractional requests; this is deliberately a sender-owned
request accumulator, not a persistent ledger for the old pair. Multiple right
records advance it in the declared local order. This mode requires distinct
left/right types and a hold/move left type; split emitters are rejected. The
default `"pair"` preserves the existing pair-local behavior. Both modes exchange
exactly equal-and-opposite integer components and keep fractional bookkeeping
separate from conserved inventory.

Configured coupling order followed by fixed slot order is part of the declared
law. Identical participant types use each distinct unordered pair once. Different
types use matching ordered pairs. All updates precede couplings; transport uses
the resulting values. Conditional activation is expressed through an amount that
becomes zero; there is no independent arbitrary predicate or Python hook.

This version exchanges one shared field per rule. It does not automatically
derive mass-times-velocity or coordinate multiple different physical quantities.
Any additional relation or conservation promise needs an explicit supported law
and independent tests.

### Atomic multi-field interactions

`interactions` extends the generic framework without interpreting physical names.
Each rule declares `name`, `left_type`, `right_type`, `assignments`, `invariants`
and an optional scalar `when`. A strictly positive `when` activates the rule;
zero or negative skips it. Omission activates every matching pair cycle.
Activation reads only the pair's locally available fields. It is not an implicit
geometric contact detector and adds no encounter history.

Each assignment contains `side` (`left` or `right`), an owned `field`, and an
`expression` producing its complete new value. There are 1–32 assignments with
unique `(side, field)` targets; cost outputs cannot be targets. All right-hand
sides read the same pre-interaction pair. The transaction builds both candidate
records before validating either outcome. No partial update becomes physical.

Each of 1–16 named invariants contains `name` and `expression`. The expression
must have exactly equal scalar/vector values before and after the transaction.
Every field marked `conserved` also retains its pair sum component by component,
even if the configuration omits an invariant for it. Checks occur per transaction,
so a later transaction cannot cancel an earlier violation. Units and scales of
custom expressions must be declared consistently by the model; the evaluator
does not infer dimensional correctness or prove physical meaning from a label.

The generic expression additions are:

- `dot`: two three-component vectors produce their integer dot product.
- `transform`: one vector and a constant `matrix` (3 by 3 bounded integers)
  produce matrix-vector multiplication. A matrix is not automatically a rotation;
  the model declares any norm or momentum constraints it needs.
- `gt`: two scalars produce 1 when the first exceeds the second, otherwise 0.

Every product and partial sum uses the bounded working register. Every output
uses the existing positive-coded payload schema. Existing `exact_div` rejects
nonintegral results; transactions never round a violated invariant away. Choose
appropriate integer units or explicitly modeled fraction fields when needed.
The existing fractional single-field exchange remains available separately.

Order is spatial response when configured, ordinary updates, exchange couplings,
atomic interactions, then routing. Interaction invariants compare the pair after
those earlier proposed responses; they preserve its conserved sum while retaining
the spatial response's prepared opposite reaction.
Interactions use declared rule order, then fixed slot order, with each unordered
pair once for equal types and ordered matching pairs for distinct types. Each
assignment charges `update`, each accepted activation charges `couple`, and
activation/assignment AST evaluation charges `evaluate`. Invariant evaluation is
passive validation and contributes no model cost. Every AST retains the
64-node/depth-16 bound. State and work remain bounded for fixed schema
and slot capacity. All proposals obey the existing frozen computation wait and
simultaneous local commit contract. An invalid interaction faults the run before
committing its carrier proposal or installing its pending plan. Previously
completed independent events, including field transport and fresh emission with
its carried allowance metadata, are not rolled back.

### Configured unequal-mass elastic example

`examples/04-unequal-mass-collision.json` selects
`configured-unequal-mass-elastic-head-on-v1`. This is a configured classical
one-dimensional elastic contact example, not a force derived from a field.
Mass and momentum are ordinary named fields; no collision formula or name is
built into the engine. Movement uses `sum(abs(momentum)) / mass` exactly as an
integer rate numerator with denominator 120; its x-axis velocities are in c/120.
Both records move through the existing neighbor transport.

For M=mL+mR, P=pL+pR, D=mR*pL-mL*pR, the configuration supplies
`pL'=(mL*P+R*D)/M`, `pR'=(mR*P-R*D)/M`, with
R=diag(-1,1,1). This reflects the relative x component. The rule activates when
D.x>0 for the named incoming roles. It keeps each mass unchanged and preserves
P and `mR*dot(pL,pL)+mL*dot(pR,pR)`, which is proportional to classical kinetic
energy for the fixed pair masses. It therefore does not fire again while this
outgoing pair remains co-resident. Arbitrary 3D contact normals, crossing between
cells, species creation and relativistic scattering are not supplied by this example.

Independent expected values: masses (2,3), momenta (8,-3) become (-4,9), hence
velocity numerators (4,-1) become (-2,3). Total momentum is 5 and kinetic energy
is 35/2 in the declared scaled units throughout. In a 15 by 15 by 15 lattice,
seeds (3,7,7) and (8,7,7) arrive at (7,7,7) at tick 120, change momentum in the
next local cycle, and are at x=3 and x=13 at tick 360 without boundary wrapping.
This reproduces a classical elastic-collision benchmark; it does not establish
universal energy conservation or emergence of real-world physics.

Physical reference: [OpenStax, Types of collisions](https://openstax.org/books/university-physics-volume-1/pages/9-4-types-of-collisions).

## Computation cost and uniform cell delay

Every modeled local cycle meters these primitives using `operation_costs`:

| Primitive | Charged work |
| --- | --- |
| `receive` | Packets received since the previous local plan |
| `read` | Fields owned by each processed resident record |
| `evaluate` | Each expression-tree node visited for physical activation or state generation |
| `update` | Each update assignment, including a configured cost-field write |
| `couple` | Each applicable record-pair exchange |
| `route` | Each processed record's transport decision |
| `split` | Each component partition in the fixed payload schema |
| `send` | Each outgoing record |
| `commit` | The local cycle commit |

Carrier local checks, invariant expressions, automatic conservation comparisons
and replay used only for validation do not contribute to these model prices.
They still use bounded arithmetic and reject failures. Physical `when` predicates,
assignments, coupling reads, reaction deltas and actual deposit preparation remain
priced: they choose or generate the transition. Adding a passive acceptance check
does not itself delay a valid physical cycle. Host validation work can still grow.
The separate [local energy/momentum audit](LOCAL_CONSERVATION.md) measures complete
committed transitions and has no model-time or operation-cost contribution.

These are model operations. Python instruction count, diagnostics, rendering,
global scheduler scans and metering its own bookkeeping are separate host work.
Charging the cost-field assignment once avoids recursive measurement overhead.

Let `C` be the summed cost of this local cycle, `B = normal_budget` and
`tau = link_ticks`. The timing law is:

```text
k = max(1, ceil(C / B))
extra cell delay = (k - 1) * tau
link transit = tau
earliest arrival after cycle start = k * tau
```

`ceil` is implemented with bounded integer arithmetic. Up to the ordinary cost
`B`, no extra waiting is introduced. For `B=10`, costs 10, 11 and 21 imply total
neighbor-arrival intervals `tau`, `2*tau` and `3*tau`. The link's transit never
changes; if physical spacing is `L`, its fixed speed corresponds to `c=L/tau`.
There is no accumulated computation debt between cycles and no global mean-load
normalization. A fresh cycle has its own measured cost.

One frozen local proposal includes updates, coupling results and departures.
The original records remain owned by the cell while it waits. All proposal
changes become effective together after the extra delay; the source cannot start
another cycle before the full interval ends. Arrivals into available unlocked
slots wait for a later cycle and cannot alter the frozen proposal.

A type may name an owned scalar `cost_field` to store the measured `C`:

```json
{"name": "local_work", "fields": ["computation"],
 "transport": {"mode": "hold"}, "cost_field": "computation"}
```

That field must be nonconserved, held locally, and cannot also be an update or
coupling target. Its label is arbitrary. It reports the cost that drives the
cell's general delay; storing a number in an unrelated field does not itself
slow the cell. Propagating computation disturbance as a physical influence is a
separate configured-law question, not an implicit feature of this cost output.

## Conservation, capacity and failure

For each conserved component, a local plan must satisfy:

```text
original resident amount + explicit source change
    = remaining resident amount + outgoing amount
```

Delivery transfers ownership from a packet to the destination. At any tick,
diagnostic totals count resident amounts, including originals waiting for a
pending cycle, and in-flight packets exactly once. Pending proposals are not
additional owned stock. Under schema 1 with periodic boundaries, total change
equals committed source/sink change;
source creation is not reported before its proposal commits. Direction/rate
phases and fractional exchange remainders remain bounded bookkeeping.

Schema 2 additionally subtracts committed signed dissipation from that balance.
Its declared decay intentionally removes integer magnitude without retaining a
fraction; it is not a transport conservation claim or a numerical approximation
to the version 1 law. Baseline values are exempt. Finite remaining allowances are
bookkeeping owned by records, never extra field stock. These distinctions remain
visible in run metadata, events and snapshots.

An open boundary additionally records the signed components that leave the world
as escaped quantity. They are no longer resident or in flight after escape, and
are not counted a second time as an implicit source or decay loss. For declared
conserved components the combined diagnostic balance is:

```text
resident + in flight = initial + committed sources - dissipation - escaped
```

Periodic boundaries have no escape term; schema 1 has no decay term. This is
an accounting statement, not a claim that an open world's physical inventory
stays constant. Global ledgers only verify locally committed events.

Conservation refers to an amount, not a constant throughput. Delaying transfers
can reduce local flux while preserving every conserved unit. Global totals are
read-only verification and cannot correct the local law.

Local records, outgoing packet capacity and rule/remainder storage have fixed
bounds from the schema. More world cells increase total host storage and runtime;
the complete world step is not constant-time. Receiving capacity exhaustion,
occupied outgoing capacity, overflow, invalid division, wrong component counts,
forbidden signs or failed conservation stop the run explicitly. No disturbance
is silently dropped and no queue grows without bound. A failed engine rejects
continuation. Already completed independent local events need not roll back when
a later local event fails; failure metadata must preserve the actual stopped state.

## Implementation and evidence

The authoritative implementation owners are `initialization.py` for parsing,
`core/disturbance_state.py` for fixed schemas, `fields/disturbances.py` for local
arithmetic/proposals and `core/disturbance_engine.py` for time and ownership.
`disturbance_api.py` composes the primary public Simulation. The runner handles
output without supplying physical inputs.

Validation must include independent signed scalar/vector split examples,
whole-record transport, coupled exchange, source accounting, exact arrival
timing, overflow/capacity failures, renamed user-defined fields and headless
execution. See [the test expectations](TEST_EXPECTATIONS.md). Test results and
the tested source identity belong in the current validation evidence, not in
this contract. This framework does not establish gravity, wave behavior,
relativity, energy conservation or all historical candidates' acceptance laws.

## Optional event program

The top-level `event_program` selects [native causal events and local instruments](NATIVE_QUANTUM_EVENTS.md).
It leaves existing configurations unchanged. It can supply a locally recorded
control code to an existing generic law; all resulting moves retain ordinary
operation costs, frozen proposals, conservation checks and causal transit.
