# Generic local field rules

This optional schema 1 extension lets a node retain dynamic field stock, combine
several scalar/vector components, and choose payloads for its six outgoing
links. It also supports joint field/carrier transactions. The node reads its
own state and information already delivered through those links. It never reads
another node's current state, a global measurement or a source history.

These are configurable operations, not a supplied electromagnetic model.

The optional [directional-wave example](DIRECTIONAL_WAVE.md) composes the existing
operations into a transverse-mode candidate with explicit conserved energy and
momentum, including unequal polarization encounters. Its limitations are explicit.

Grouping two vectors does not establish Maxwell's equations, the Lorentz force,
a quantum photon, or a general energy-conservation law. Candidate laws and
independent acceptance criteria still belong in each experiment's initialization
and validation evidence.

## Selection and existing fields

Declare ordinary scalar/vector fields through `fields`, then select
`"transport": "local"` for the corresponding `spatial_fields` entries. These
fields retain their stock unless a rule assigns another value or sends it out.
They may coexist with existing `"transport": "outward"` fields. Rules can read
both kinds but can assign only local fields. Existing outward transport,
emissions, pair interactions and spatial exchange/rotation retain their own
contracts when the new features are absent.

Local transport, `field_rules` and `spatial_interactions` require schema 1.
Schema 2 rejects the two rule keys even when their lists are empty and continues
to use its finite attenuation candidate. The new rules do not bypass schema 2
allowances or remove its required decay.

Run metadata identifies local transport as `configured-local-fields-v1`.
Outward-only schema 1 runs keep `conservative-outward-v1`; schema 2 records
`finite-localizing-v1`, or `finite-dissipative-v1` when a field selects
`"residue": "dissipate"`. Physical field names do not select any of these policies.

Optional `field_groups` describe logical grouping without allocating new physical
stock or selecting a law:

```json
"field_groups": [{"name": "paired_vectors", "fields": ["a", "b"]}],
"spatial_fields": [
  {"field": "a", "baseline": [0, 0, 0], "transport": "local"},
  {"field": "b", "baseline": [0, 0, 0], "transport": "local"}
]
```

Each member still has its original scalar or three-component schema, units,
scale, sign and conservation declaration. Expressions reference member field
names. Group names are metadata; different groups may overlap without counting
their members twice. There are at most 16 groups with 1 to 16 distinct existing
members each. The existing total field limit remains 16.

The node has six ordered ports `[+X, -X, +Y, -Y, +Z, -Z]`. The index identifies
travel direction, independently of the scalar/vector payload. For example,
travel through +X arrives at the next node with port index 0 even though that
node is approached from its negative-X side. No geometric face or edge record
is introduced.

## Read views and ownership

| Expression or target | Meaning |
| --- | --- |
| `{"field": "a", "side": "right"}` | Observable local value: immutable baseline plus current retained dynamic stock |
| `{"received": "a", "port": 0}` | Scalar/vector amount delivered in the preceding input interval through the +X travel channel |
| `{"outgoing": "a", "port": 0}` | Proposed +X outgoing payload accumulated by preceding field rules in this phase |
| Assignment without `port` in a field rule | Replace retained dynamic stock only |
| Assignment with `port` in a field rule | Replace that outgoing payload only |

The received channels are read-only projections of stock already owned by the
node. Reading them does not add that stock again. Opposite channels remain
individually readable even when their sum is zero. Payload direction and port
direction remain independent, including for vectors.

The baseline is immutable background. It can influence expressions, but cannot
be assigned, spent as a reservoir, or sent by moving dynamic stock. For example,
baseline 10 and stock 3 read as 13; retaining dynamic stock 3 preserves that
state. Assigning the read value 13 to retained stock would instead propose
dynamic stock 13, which must pass the declared balances.

Local stock and each explicit outgoing payload use the existing bounded packet
representation. For local transport, the aggregate occupies internal population
slot 0; the other seven population slots are zero after preparation. That storage
choice does not impose the outward candidate's octant signs on local routing.
Initial `spatial_seeds` retain the eight-population input format. Their amounts
are summed into the local aggregate. The delivered channels are cleared after
the phase so old arrivals do not become a permanent input trail.

## Field rules

`field_rules` is an optional list of at most 32 named rules. Each rule has 1 to
32 `assignments`, 1 to 16 named `invariants`, and optional scalar `when` and
`commit_when` conditions.
Absent `when` means active whenever the node has relevant work; otherwise a
strictly positive result activates the rule. Assignment targets must be unique
within one rule. Unsupported names, directions, shapes and duplicate targets
fail initialization.

`when` is a start trigger. `commit_when` must be positive at selection and at
commit, reading owned field values only. It cannot read received, presence, flux
or outgoing views. A false initial condition skips that rule; invalidation during
a wait faults before committing the proposal. These guard checks add no physical
operation cost. The [Node profile](NODE_VECTOR_PROCESSOR.md#local-rules) defines
the explicit k*h wait, ordered frozen-delta revalidation and ownership behavior.

```json
"field_rules": [{
  "name": "exchange_components",
  "assignments": [
    {"field": "a", "expression": {"field": "b", "side": "right"}},
    {"field": "b", "expression": {"field": "a", "side": "right"}}
  ],
  "invariants": [{
    "name": "component_sum",
    "expression": {"op": "add", "args": [
      {"field": "a", "side": "right"},
      {"field": "b", "side": "right"}
    ]}
  }]
}]
```

This fragment assumes matching component shapes and zero baselines. Component
exchange requires that the two fields are not individually declared conserved,
unless the particular inputs also preserve each field separately. The named
invariant preserves their configured combined value; it does not infer units
or assert that this value is energy.

At each field interval, existing source emission first adds its explicitly
accounted injection. Outgoing local buffers initially contain zero. Every rule
reads a frozen view of retained values, six received samples and currently
proposed outgoing buffers. All its right-hand sides use that same view. After
validation, the next rule sees the accepted retained values and outgoing
buffers. Received samples remain fixed for the whole phase. An omitted target
retains its previous proposal value.

A rule can move stock into a selected outgoing buffer by assigning both owners:
set retained stock to zero and the outgoing payload to the old stock. Assigning
only the outgoing payload while retaining the same stock would duplicate it
and fails a conserved-field balance. Outgoing ownership crosses exactly one
nearest-neighbor link after the existing `link_ticks` transit time. It cannot
be read as an arrival at its destination during the same event.

After every rule, each `conserved` field must preserve the component-wise total
of retained dynamic stock plus all six outgoing payloads. Named invariant
expressions are also compared exactly before and after that rule. If an
invariant is intended to include outgoing content, its expression must include
the relevant `outgoing` leaves. A local-value expression alone observes retained
value, not inventory already assigned to a link. Received leaves are available
to assignments and activation expressions, but are rejected in invariants;
they are never a second stock owner.

All local proposals must validate before any field state, emitted-record
bookkeeping or outgoing packet from that node's phase commits. Failure stops
the run without partially applying that proposal. Earlier independently
committed events remain real.

## Joint field/carrier transactions

`spatial_interactions` extends local response to assignments across resident
carriers and one or more local fields. A rule selects one `type`/`requires` role
or an indexed `participants` array of 2 through `slots_per_node` roles (at most
32). Each role selects a whole-record `hold` or `move` layout; splitting
participants are rejected. There are at most 32 rules and 16 invariants per
rule. Assignments are bounded by the field count limit times the number of
participant owners plus one field owner. Duplicate targets are rejected.
Nonempty joint rules require at least one declared spatial field, even when a
particular rule reads that field and assigns only carrier values.

Assignments explicitly select `side: "left"` for an owned carrier field or
`side: "right"` for a local spatial field. The computation-cost reporter cannot
be assigned. Ordinary expression leaves default to the carrier on the left;
right-side leaves read observable field values. Unlike a retained field-rule
assignment, a right-side interaction assignment proposes an observable value.
The engine derives its dynamic-stock change by subtracting the previous
observable value, leaving the baseline unchanged.

For an indexed rule, carrier references and targets use `participant: i`, and
`side: "right"` still selects spatial fields. Left-side or default references
are ambiguous and rejected. Roles use the same bounded deterministic disjoint
selection as [indexed carrier interactions](NODE_VECTOR_PROCESSOR.md#local-rules).
One group reads one frozen snapshot of all its carriers and local fields.
Selection by properties cannot mix with a top-level type selector.

```json
"spatial_interactions": [{
  "name": "local_exchange",
  "type": "carrier",
  "assignments": [
    {"side": "left", "field": "inventory", "expression": {
      "op": "sub", "args": [{"field": "inventory"}, 1]
    }},
    {"side": "right", "field": "inventory", "expression": {
      "op": "add", "args": [{"field": "inventory", "side": "right"}, 1]
    }}
  ],
  "invariants": [{
    "name": "combined_inventory",
    "expression": {"op": "add", "args": [
      {"field": "inventory"}, {"field": "inventory", "side": "right"}
    ]}
  }]
}]
```

These rules run after existing spatial exchange/rotation and before ordinary
carrier updates, pair couplings/interactions and transport planning. Rule order,
then local slot order, determines evaluation order. Each transaction evaluates
its assignments from one frozen participant/field view; later transactions see its
proposed changes. Named invariants and automatic conserved-field combined sums
must hold. The initial spatial samples precede fresh emission and field-rule
updates in that interval, matching the existing carrier response contract.

Assignments and `when` may read six received channels. Optional `commit_when`
uses owned participant and field values, with the same persistent-condition
semantics as field rules. Joint invariants use
carrier and field values only; received and outgoing leaves are rejected there.
The frozen transaction stores each carrier before/after view and its additive
field delta. A pending proposal is not new inventory.

During a carrier's computation wait, its original values remain owned and its
source bookkeeping continues updating. Spatial fields continue on their fixed
clock. At commit, the engine applies the frozen deltas to the field's current
state, never overwriting it with the old sampled state. Each transaction's
invariants are rechecked sequentially against that actual before/after field
view and its stored carrier transaction views. A nonlinear invariant that held
at planning can fail after the field changed. In that case the run faults
before committing either owner; the engine does not recompute the old decision,
silently drop it, or force the invariant by changing physical values.

The guard covers its own transaction. Later ordinary carrier rules and pair
interactions retain their separate contracts; one invariant is not automatically
a promise about the entire later cycle. Local field deltas remain at the node
until its next field phase. Existing reactions into outward fields retain their
same-timestamp forwarding contract. New joint assignments can write only local
fields, though their expressions may read any spatial field.

## Accounting, cost and limits

Nonconserved component changes made by field rules are recorded in the spatial
`transformations` ledger. They are not external `sources`. Spatial accounting
includes initial stock, committed sources, reactions and transformations, minus
dissipation and escaped quantities. Conserved fields require zero transformation
change in their own totals. Named cross-field invariants can describe additional
configured relations, but the diagnostics do not infer energy or compatible
units from names. Immutable baselines remain counted once per world node.

When visualization is requested, the shared recording player shows node field
values and field transfers alongside disturbances. Node values already include
baseline; received samples are not added to them. Packet populations are summed
once for display, with separate link ownership. Vector arrows use the selected
projection and a per-field scale across the recording; the table retains exact
component values. These display calculations never update the physical state.

Every new rule uses the bounded integer expression evaluator, including generic
`cross` of two vectors and `vector` construction from three scalar expressions.
Existing limits of 64 nodes and depth 16 per expression apply. Intermediate
products and sums must fit the working register before any later cancellation;
physical payload bounds are checked before commit. `exact_div` remains exact,
with no implicit truncation or floating-point normalization.

Field state generation contributes priced work to new carrier cycles without
delaying the fixed field clock. Joint activation and assignment evaluation,
six-channel physical sampling, proposal delta construction and reaction
accumulation contribute to the frozen carrier cost. Local deposit and
post-deposit sampling retain their separate fixed reservation when stock changes.
No later computation debt is added to an already frozen carrier proposal.

Named invariants, automatic conserved-field comparisons and delayed guard replay
are passive validation. Their bounded arithmetic and rejection behavior remain,
but they add no model work or waiting time. Replay-only field sampling and delta
reconstruction have no physical-cost reservation. This differs from the sampling
and delta construction used to generate a physical proposal. The optional
[energy/momentum audit](LOCAL_CONSERVATION.md) separately observes complete
committed ownership transitions without replacing those precommit checks.

A node runs field rules when it owns nonzero local dynamic stock or has nonzero
received directional samples. A nonzero baseline alone does not activate empty
space; outward resident stock alone does not activate local rules. Source
emission can provide local stock and activate the phase. Zero-input creation
must use an explicit source law, not an unscheduled rule on untouched nodes.
Node work and registers are bounded by the configured field/rule/slot limits;
host frontier indices and diagnostic history are not physical inputs.

The focused acceptance requirements are in
[TEST_EXPECTATIONS.md](TEST_EXPECTATIONS.md#generic-local-field-rules).
The complete runnable example is [local_field_rules.json](../examples/local_field_rules.json).
It tests generic two-component transformations, not an electromagnetic field.
