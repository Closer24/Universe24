# Elementary fields and local exchanges

Schema 3 is the active candidate. Ordinary `Simulation`, initialization loading,
the CLI and the workspace accept this closed vocabulary. A JSON expression tree
can encode a continuum force just as Python can; being JSON is not a sufficient
restriction. The active parser therefore rejects every unrecognized key, every
supplied update/condition/invariant program and every nonliteral movement rate.
Renaming a formula or putting it inside an emission does not permit it.

The explicit schema 1/2 research interface remains available through
`event_universe.reference_api.ReferenceSimulation`, `load_reference_state`,
`parse_reference_state` and `parse_reference_json`. Run it with
`python -m event_universe.reference_runner --init ... --output ...`.
These names select supplied-law reference experiments. No JSON flag, filename,
model label or workspace template can select that execution path.

## Input and ownership

The required top-level members are `schema_version: 3`, `model_id`, `shape`,
`slots_per_cell`, `link_ticks`, `normal_budget`, `ticks`, `operation_costs`,
`fields`, `disturbance_types` and `seeds`. Optional members are `boundary`,
`field_groups`, `spatial_fields`, `spatial_seeds`, `emissions`, `exchanges` and
`observer`. The optional [passive observer](LOCAL_OBSERVER.md) uses the shared
placement validator, changes no physical state, and cannot supply a law or value.
Duplicate JSON keys, unknown keys and booleans used as integers are errors.
Typed initialization must also satisfy the same declaration capacities, transport
vocabulary, field/seed ownership and fresh fixed-size bookkeeping. It cannot
enable reference propagation settings or bypass finite emission bounds.
Existing [bounded field declarations](DISTURBANCES.md#field-definitions) apply:
one or three components, integer scale, units, signedness, extensivity and a
declared conserved amount. Names are labels and never select physical laws.

A type declares `name`, `fields`, `transport`, optional `defaults` and an optional
`cost_field` reporter. Transport selects `hold`, `move` or `split`, six constant
`weights` or a carried `direction_field`, a constant integer `rate`, positive
`rate_denominator`, and existing `cyclic`/`balanced` routing. Rate remainders are
bounded motion bookkeeping. A cost reporter cannot control routing, emission or
exchange. Seeds contain only `position`, `type` and optional `values`.

Spatial stock is separate from every carrier's payload. A spatial field requires
an extensive declaration and the following parameters:

```json
{
  "field": "flow",
  "baseline": [0, 0, 0],
  "routing_weights": [1, 1, 1, 1, 1, 1],
  "computation_delay": true,
  "decay": {"retain_numerator": 1, "retain_denominator": 2}
}
```

`baseline` is optional, immutable and defaults to zero. Each of six weights is
nonnegative; their sum must be positive and bounded. A phase partitions resident
stock among those links with bounded integer allocation remainders. This is a
local weighted transport candidate, not an isotropic wave or a Maxwell solver.
Existing spatial seeds supply eight bounded internal populations; their sum is
the local dynamic value. The eight slots are storage channels, not extra neighbors.

## Per-field computation delay

Every spatial declaration must explicitly choose boolean `computation_delay`.
The local field phase prices the existing declared operations, including receipt
and completed-link decay. Let `C` be that cell's field-phase tariff, `B` the normal
budget and `tau` the fixed link transit. The prepared outgoing stock waits
`(max(1, ceil(C/B)) - 1) * tau` before departure when the field's flag is true.
Its next field activation is at least `max(1, ceil(C/B)) * tau` after preparation.
A false flag gives no computation wait. Two fields in one cell can choose differently.

Preparation commits the retained field values and source allowance locally.
Only the prepared outbound stock is held until its frozen departure tick; this
is not a delayed reread of the entire field or a unified proper-time law. Receipt
can add new resident stock while a previous outbound amount waits. Every departure
then takes the same full `link_ticks`, independently of its earlier waiting time.
Carrier planning keeps its existing separately priced local commit clock and
includes the field work at its sampled phase. A tariff counts model operations,
not measured Python instructions or host time. There is no accumulated debt.

There is at most one waiting register per field per cell, containing six fixed
outbound population arrays and a departure tick. It owns physical stock until
dispatch. Resident, waiting and in-flight quantities are disjoint in totals.
Snapshots and the player display waiting stock at its owning node, not partway
along a link. Diagnostics never feed these global views back into dynamics.

## Finite emission and decay

An emission declares `type`, spatial `field`, `amount`, `source: true`, a finite
nonnegative per-component `budget` and an optional positive integer `denominator`.
An amount is a scalar/vector literal or exactly `{"field":"carried_name"}`.
It cannot contain arithmetic or a condition. The amount is an explicitly counted
source, not an unreported transfer from the carrier. Its allowance is carried
fixed state; fractional emission keeps the existing bounded remainder. An
exhausted allowance emits nothing, including after periodic return.

Every field requires a ratio `0 <= p < q`. At each completed interior link,
each original population component becomes `sign(v) * floor(abs(v) * p/q)`
before arrival merging. Lost magnitude goes to signed dissipation accounting;
the discarded fraction is not retained. Positive stock cannot cross below zero,
and even a single unit disappears. Baseline does not decay. With finite sources,
finite exchange allowances and finite completed cycles, dynamic spatial stock
eventually vanishes. A trapped nonzero field is not allowed to emit forever.

Periodic space wraps all three axes. An open terminal link retains its payload
until full transit, then records it as escaped without simulating exterior decay.
For each conserved component, the independent balance is
`current + dissipated + escaped = initial + committed_sources`.
Spatial-only accounting additionally includes opposite carrier reactions.
This is an accounting identity; surviving momentum or energy is not conserved
through the intentionally dissipative propagation law.

## Elementary local exchange

```json
{
  "name": "encounter",
  "type": "carrier",
  "field": "flow",
  "components": [0, 1, 2],
  "budget": [3, 3, 0]
}
```

An exchange requires a signed extensive field with zero baseline, owned both by
that whole carrier and the local spatial field. Split types are rejected. The
optional component list defaults to every component. One descriptor is allowed
per type/field pair; duplicate names or components are errors. Each carrier owns
one finite allowance vector for each configured descriptor.

For selected components only, the built-in operation swaps carried value `a`
and local value `b`. Its absolute spending is `abs(a-b)`. All selected spending
must fit the remaining allowance; otherwise no exchange occurs. Zero local stock
and an unchanged swap also produce no response. There is no partial swap, force
coefficient, field-name branch, supplied expression or per-instance source lookup.

An eligible local encounter retains that field during routing and samples it
after the local emission phase. The carrier and opposite field reaction commit
together. A swap preserves each combined component `a+b` and the joint squared
norm `a.a+b.b`, including signed turns and partial component selection. These are
normalized integer invariants, not a universal mass-dependent kinetic energy.
Carrier norm alone need not remain fixed. Finite allowances prevent indefinite
repeated response from trapping or replenishing the field.

Several resident carriers use deterministic slot order and each sees the local
proposal from the preceding exchange. All guards and bounds must pass before
their local transaction commits. A delayed proposal rechecks the live field;
intervening arrival can invalidate its squared-norm guard. In that case the run
fails before either side or its exchange allowance commits. No stale overwrite,
global repair or silently weakened invariant is used. This rejection is an
explicit current composition limit, not a claim of unrestricted many-body physics.

## Reproduction and limits

- [Straight motion](../examples/elementary_motion.json): a whole carrier crosses
  one link per tick at normal cost and wraps in the periodic domain.
- [Local encounter](../examples/elementary_contact.json): carried `(3,0,0)` meets
  post-decay field `(0,3,0)`, leaves in +Y and returns `(3,0,0)` to the field.
  The local combined vector is `(3,3,0)` and joint squared norm is 18.
- [Open finite source](../examples/elementary_open.json): source total 8 divides
  into 6 escaped and 2 dissipated units; all 9 carried strength units escape.

Run with `python -m event_universe --init examples/elementary_contact.json
--output artifacts/elementary-contact`. No compilation or visualization is needed.
`tests/test_elementary_fields.py` covers numerical outcomes, all six boundaries,
field clocks, extinction, typed and JSON rejection, signed turns and guarded
failure. The workspace and headless JavaScript suites cover consumers.

Schema 3 deliberately does not accept schema 1/2 field programs, arbitrary pair
collisions, supplied Lorentz rules, native quantum events or catalog law programs.
Their existing assertions remain in the explicit reference suites. This change
does not derive Lorentz/Maxwell dynamics, gravity, a quantum-to-classical transition
or general self-field exclusion. Arrival order is not attribution after a turn
or periodic return. It also does not implement the separately proposed variable
port topology; this contract uses main's six axial links.
