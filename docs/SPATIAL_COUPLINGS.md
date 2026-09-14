# Generic local field response

The optional `spatial_couplings` list connects a carried field to local spatial
input. It selects integer operations, not physical identities. The complete
turning example is [spatial_turning.json](../examples/spatial_turning.json).
Transport and source ownership remain defined in [SPATIAL_FIELDS.md](SPATIAL_FIELDS.md).
That example uses schema 1. Schema 2 keeps the same local operations but requires
a finite `budget` on every spatial coupling and decay on every spatial field.

Schema 1 separately offers [joint field/carrier transactions](LOCAL_FIELD_RULES.md#joint-fieldcarrier-transactions)
through `spatial_interactions`. They can assign multiple carrier and local field
components, with named invariants rechecked against actual field stock at delayed
commit. They run after the response rules described here. Their six-port inputs
retain scalar/vector channels independently; they do not expand the scalar
`flux` projection below into an implicit vector-flux tensor.

## Inputs and ownership

Each rule names its receiving disturbance type and the carried target `field`.
That same field must also have a spatial definition. It is the signed, extensive
owner of the equal-and-opposite reaction. Reading another field as a driver does
not imply that differently named fields have interchangeable conserved units.
The target cannot be a computation-cost reporter or belong to a split type.

Ordinary expression leaves read the carrier on `side: "left"` and local spatial
values on `side: "right"`. A right-side field must have a spatial definition.
Its value is the configured baseline plus resident stock. A `{"flux": "name"}`
leaf is available only for a scalar spatial field and produces a vector from
its six delivered channels: `(F+X-F-X, F+Y-F-Y, F+Z-F-Z)`. It is a signed travel
projection, not new inventory. Vector field flux would require a separate tensor
contract and is rejected. Baselines have no incoming directional flux.

Samples are captured before this interval's fresh emission and forwarding.
The carrier therefore does not read its own newly created local source as an
additional field value. Previously delivered self contributions are not removed
by this sampling rule. Each local sample and carried remainder has fixed size;
no source identifiers, histories, other-world simulations or global measurements
enter the response.

## Absorb

`"mode": "absorb"` applies to a straight-ray field that the absorbing type also
carries. It takes no `amount`: of every ray resident at the record's Node on the
cycle after it arrived, the share `amount x fraction / fraction_denominator`
(truncated toward zero; the whole ray without a `fraction`) is removed, added to
the record's field of the same name, and with `"momentum_field"` its
`share x heading` is added to that owned vector; the rest of the ray is
forwarded. `fraction` is a nonnegative expression over the record's own fields,
so a share proportional to `mass` gives every body the same acceleration. A
negative share is paid from the record's stock and never beyond it: the clipped
remainder continues as a ray. One ray field is either absorbed or exchanged and
rotated, never both. Absorb runs inside the spatial plan before forwarding,
needs no response law, and is described with funded emission in
[SPATIAL_FIELDS.md](SPATIAL_FIELDS.md#funded-emission-and-absorption).

## Exchange and rotation

An `exchange` rule evaluates `amount`, divides it by `denominator` with a signed
carried remainder, removes the whole amount from the carrier and adds it to the
same spatial field. The expression may read any declared local driver. A negative
amount reverses the exchange. This mode preserves combined component totals; it
does not promise to preserve the carrier vector's length.

```json
"spatial_couplings": [{
  "name": "turn", "type": "carrier", "field": "inventory",
  "mode": "rotation",
  "rotation": {"field": "control", "side": "right"},
  "denominator": 1, "axis_order": [0, 1, 2]
}]
```

This fragment is schema 1; schema 2 additionally requires a nonnegative scalar
or three-component `budget` matching the target field. Its exact allowance law
is described below.

A `rotation` rule requires a three-component target and a three-component
expression. Each expression component requests signed quarter turns about its
axis per local carrier cycle. `denominator` controls how much accumulated request
completes a quarter turn. All fractional remainders travel with the record.
The configured axis order is a permutation of X, Y and Z, represented by 0, 1 and
2. Rotations about different axes do not commute, so order is part of the law.

The positive transforms are `Rx(x,y,z)=(x,-z,y)`, `Ry(x,y,z)=(z,y,-x)` and
`Rz(x,y,z)=(-y,x,z)`. Counts are reduced modulo four, so arbitrarily large valid
requests do not create arbitrarily long loops. A turn about an invariant axis
(both perpendicular components zero) leaves that axis's remainder unchanged.
It cannot accumulate an otherwise invisible request against a parallel vector.

For `(5,0,0)` and one positive Z turn, the carrier becomes `(0,5,0)` and its
spatial field receives `(5,-5,0)`. Their sum remains `(5,0,0)` and the carrier's
squared length remains 25. Signed permutations preserve its squared Euclidean
length, absolute component sum and maximum absolute component exactly. This
deliberately discrete law introduces no rounded trigonometry or normalization.
It does not implement arbitrary continuous angles.

Each rule acts in configured order, then fixed local slot order. The sampled
driver remains frozen for that cycle; later rules see the carrier changes from
earlier rules. The field reaction is accumulated and validated before commitment.
Neither carrier length preservation nor combined component conservation proves
conservation of general energy or angular momentum under spatial transport.

## Finite response allowance in schema 2

Each matching record owns the configured component budget for each rule. This is
an allowance on cumulative absolute field reaction, not physical stock and not a
reservoir of energy or momentum. Remaining allowances are fixed registers carried
with whole-record movement; a new node does not reset them. An exchange of either
sign spends `abs(old_component - proposed_component)` on each component. A rotation
spends the same component-wise magnitude of its complete vector change.

After evaluating a rule with the old carried fractions, every component must fit
its remaining allowance. The complete action is then accepted and the allowances
are debited, or the complete action is rejected. Rejection preserves the old
carrier values, fractional requests and allowances and creates no reaction.
Individual components are never clipped, because partial rotation would destroy
the exact norm invariant. A zero whole action may advance its affordable fraction;
an entirely exhausted rule skips expression evaluation and cannot accumulate new
demand. Reversing a later request never refunds earlier expenditure.

For example, turning `(5,0,0)` to `(0,5,0)` requires at least `[5,5,0]` of
allowance. `[5,4,0]` rejects the whole turn and leaves the carrier unchanged.
Accepted changes and allowance debits commit with the same frozen carrier
proposal and opposite field reaction. A delayed proposal cannot spend its budget
twice, and an unrelated emission updates only its own separate source allowance.

At that commit, equal-and-opposite exchange remains exact. Once the reaction
completes a link, schema 2 attenuation applies. By default the removed fraction
comes to rest at the receiving node, so the combined physical vector total stays
constant while its moving part shrinks; under `"residue": "dissipate"` the total
need not remain constant and its change is recorded as dissipation. The configured rotation itself still preserves the
carrier norm exactly. Schema 1 rejects `budget` and retains unlimited response.

## Timing, prices and atomicity

The spatial response precedes ordinary local updates, paired exchange and
movement planning. Their physical state-generating work uses one frozen carrier
proposal and contributes to its computation cost. The existing normal-budget
rule determines the local wait; this extension does not add a fixed movement
pause. Bounded acceptance checks are passive validation, so their expressions
and replay do not add model cost or waiting time.

During a wait, the original carrier still owns its old values and continues
emitting according to its source rule. Spatial fields keep propagating. The
proposed response, sample and remainders do not change when later fields arrive.
At commit, the carrier change and its opposite field change become real together.
The pending reaction is a proposal, not extra inventory or an external source.

The reaction is validated against the field's current state and packet buffers
before either owner changes. An overflow stops the event without committing
either side. Reactions are partitioned across the target's configured octants.
If this timestamp's field phase has already run, they are split and appended only
to packets departing at that same timestamp. An older packet already in transit
cannot be edited. Otherwise they remain local until that timestamp's field phase.
In both cases a newly available reaction can arrive one `link_ticks` later.
Separate ordinary-field and reaction splits are the declared local event order;
integer rounding need not equal a hypothetical single merged split.

Physical sample reads, activation and assignment evaluation, fractional updates,
rotations, reaction allocation and six-buffer preparation have explicit operation
prices. Invariants and conservation comparisons remain checked without model
charges; they do not replace any part of the physical transfer. Reaction
preparation reserves its six possible buffers in the frozen carrier cost. For
each nonzero target reaction with `C` components, the fixed preparation tariff is
121 reads, `9*C` splits, `56*C` updates, eight route operations and six send-buffer
operations at their configured prices. This is a model reservation tariff, not
an exact count of host instructions or of the branch eventually executed. A
delayed local deposit still participates in the next ordinary priced field phase;
that stage's forwarding work is separate from the response reservation. The
engine does not acquire computation debt when the proposal eventually commits.
Allowance reads and accepted allowance updates are also priced. Snapshots expose
`spatial_remainders` and finite `spatial_remaining` separately from stock;
`spatial_coupled` events report the signed field reaction.

## Straight motion and self interaction

The first-arrival intuition has a precise restricted form. Before periodic
return, a field emitted `n` intervals ago lies at unwrapped Manhattan distance
`n` from its emission point. A straight cardinal carrier has advanced `j <= n`
steps. Coincidence requires `j = n`: only its latest uninterrupted sequence of
maximum-speed steps can meet its own field, along that same cardinal path.
A complete waiting interval lets every older front move ahead.

For a rotation driven by scalar directional flux, this own straight-line flux is
parallel to a cardinal carrier vector. Turning about that axis leaves both the
vector and its fractional turn state unchanged. External transverse flux still
acts. This is a geometric property of the selected rotation law, not a test of
how many sources exist in the world and not automatic source subtraction.

A turn admits alternate shortest paths. A periodic boundary can return earlier
field. A generic value-driven exchange can also respond to coarriving self stock.
Those cases do not inherit the restricted straight-line guarantee. Explicit
source attribution remains a separate feature: a carried own-front register could
support unsigned straight paths with a defined partition order, but is not
implemented by this response extension. Current rules always operate on the
declared local samples and do not claim to identify their sources.
