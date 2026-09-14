# Configured outward spatial fields

These optional candidates separate a carried disturbance from the spatial fields
it emits. Select fields through `spatial_fields` in initialization. Schema version
1 selects `conservative-outward-v1`, with conservative transport and unlimited
declared emission; its example is
[moving_source.json](../examples/moving_source.json). Schema version 2 requires
finite decay and source allowances and selects `finite-localizing-v1` by default:
attenuated fractions become stationary stock at the receiving Node, so total
signed inventory is preserved. Its example is
[finite_fields.json](../examples/finite_fields.json). The explicit
`"residue": "dissipate"` option selects the historical `finite-dissipative-v1`
loss law instead. Names such as `radiation`,
`strength` and `heading` remain configuration data. The runner derives the policy
from `schema_version`, never from words in the user's `model_id`.

Schema 1 also offers opt-in `"transport": "local"` fields through
[LOCAL_FIELD_RULES.md](LOCAL_FIELD_RULES.md). They retain dynamic stock and use
configured six-port output assignments instead of outward octant splitting.
Local and outward fields can coexist. The sections below describe the outward
candidate; the linked contract owns the local mode, field groups, multi-field
rules and transformation accounting. Schema 2 remains unchanged.

## Local state and propagation

Each spatial field references an existing scalar/vector field definition, with
its units, scale, sign, extensivity and `conserved` flag. Each materialized node
has eight octant populations, bounded allocation phases and six delivered
directional samples. All payloads use positive integer encoding. These are
independent of the disturbance slots; there are no source IDs or histories.

Octants are `+++`, `++-`, `+-+`, `+--`, `-++`, `-+-`, `--+`, `---`. An octant
splits only among its three sign-compatible cardinal directions. Each hop
therefore increases unwrapped Manhattan distance from its emission point by
one. Sideways branches cannot reverse an octant's signs. Travel through +X
enters the next node through -X while remaining +X travel; the face does not
negate the payload. Periodic boundary return is a separate effect.

The six delivered samples are a projection of inventory, never extra stock.
Counterflows remain separate even if their resultant is zero. A vector payload
travels component by component, independently of the carrying port. Preserving
scalar stock does not automatically preserve vector momentum or energy.

Every populated channel crosses one link per `link_ticks` interval. All integer
units leave immediately; bounded rotating phases allocate indivisible units
without losing quantity or waiting to accumulate a larger packet. The phase is
allocation bookkeeping, not missing physical stock. Splitting itself preserves
every component. Schema 1 dilutes only through redistribution; schema 2 also
applies the explicit completed-link decay below. Neither law uses a global radius
or imposed inverse-square factor. The lattice rule does not promise uniform shell
intensity or Euclidean isotropy.

## Initialization

This fragment uses schema version 1:

```json
"spatial_fields": [{
  "field": "radiation", "baseline": 0, "transport": "outward",
  "axis_weights": [1, 1, 1],
  "octant_weights": [1, 1, 1, 1, 1, 1, 1, 1]
}],
"emissions": [{
  "type": "carrier", "field": "radiation",
  "amount": {"field": "strength"}, "denominator": 1, "source": true
}]
```

`baseline` is immutable local background, zero when omitted. Untouched nodes
return it without creating active records. Only deviations propagate. The local
value is baseline plus resident populations. Diagnostics count baseline once
per lattice node, not once per materialized sparse record.

`axis_weights` contains three nonnegative integers with a positive bounded sum;
`octant_weights` contains eight. Both default to equal weights. They select
branches within each octant and distribute total emission among octants.

Emission expressions read only their resident record's owned fields. The
numerator divided by `denominator` is an amount per propagation interval,
not per carrier movement or per elementary tick when `link_ticks > 1`.
Sources waiting for a frozen movement proposal continue to emit. A record
wholly in a link is not a second resident source. Emission preserves carried
source strength: required `source: true` declares external injection. A
reservoir-funded source needs a separately defined atomic debit law.

For schema version 2, every spatial-field entry additionally requires
`"decay": {"retain_numerator": 2, "retain_denominator": 3}`, optionally with
`"residue": "dissipate"` for the historical loss law, and every emission
requires `"budget": 216`, or a three-element array for a vector target. Budgets
are nonnegative component amounts in the target field's configured units,
bounded by `1_073_741_823`. A zero component budget is valid. Schema 1 rejects
both new keys, and schema 2 rejects their omission. Schema 2 without any spatial
fields is valid.

Each matching initial record receives its own budget for each emission rule.
At an interval, signed division first produces the requested whole amount and
fraction. The emitted component is that whole amount, limited in magnitude by
its remaining allowance; the allowance decreases by the absolute amount actually
emitted. Reversing the source sign cannot refund earlier use. Unfulfilled demand
is discarded rather than carried as debt, and an exhausted component clears its
fraction. An entirely exhausted rule does not evaluate its expression again.
This allowance limits external injection; it is not a mass, energy or other
physical reservoir, and is not included in field inventory.

Fractional emission remainders and source allocation phases belong to each
emitting record, together with finite remaining allowances in schema 2. They
travel with it and survive waiting. An older frozen movement proposal cannot
overwrite newer emission metadata. These are fixed registers per configured
rule, not a growing source history. Emission requires whole-record hold or move
transport, so splitting cannot duplicate an allowance.

An optional initial pulse supplies eight populations:

```json
"spatial_seeds": [{
  "position": [15, 15, 15], "field": "radiation",
  "populations": [27, 27, 27, 27, 27, 27, 27, 27]
}]
```

This contains 216 units. Under schema 1 with equal weights, each axial neighbor
receives 36 after one interval. After two intervals the origin is empty and all
stock lies at Manhattan distance two. Schema 2 additionally attenuates the
delivered populations as specified below. For vector fields each entry is an integer triple.
Spatial fields must be extensive. Unsupported laws, wrong shapes, nonintegral
values, duplicate seeds and unknown keys are rejected.

## Straight-ray transport (`isotropic-ray-field-v1`)

`"transport": "ray"` replaces octant splitting by straight-moving rays for a
scalar field. Each ray carries its heading index, three integer accumulators and
an amount. On every completed link it steps along the axis that is furthest
behind its heading (an integer digital differential analyzer), so all units of
one ray follow the same lattice line and never spread. A Node keeps a ray only
between arrival and the next cycle; there is no octant stock.

```json
{"field": "radiation", "baseline": 0, "transport": "ray",
 "headings": [[24, 0, 0], [-7, 22, 5], ...], "rays_per_tick": 64, "ray_slots": 512}
```

| Key | Contract |
| --- | --- |
| `headings` | One to 65536 nonzero integer vectors, components at most 4096 in magnitude; the emission sequence |
| `rays_per_tick` | Rays each emitting source creates per tick; the amount is shared as evenly as integers allow |
| `ray_slots` | Fixed resident ray capacity of one Node; exceeding it is an explicit failure, never a silent merge or loss |
| `self_exclusion` | Optional, default false: a record that emits into this field and departs subtracts its own rays from the flux and value it samples at the next Node |

An emitting record keeps a cursor into the heading sequence in its emission
phase register and advances it by `rays_per_tick` each tick, so a long sequence
spread evenly over the observer's sphere is swept over time. Rays with the same
heading and phase merge exactly at a Node because they share one line. Delivered
samples and the `flux` leaf see ray arrivals per port, resident ray stock is the
local `value`, and node values report `ray_count`. A coupling reaction that
amends a departing packet leaves the rays on that port untouched, so rays pass
through Nodes whose carriers respond to them.

A record that emits rays and moves one link meets, at the next Node, exactly the
rays it emitted on the cycle it departed whose first DDA step took the same
port. With `"self_exclusion": true` the record carries two rows per emission
rule, this cycle's `(amount, cursor)` and the pair from its last departure
(zero while it stays), and every coupling it evaluates after arriving reads the
sampled flux and value with those rays subtracted. The work is bounded by
`rays_per_tick`, uses only the record's own registers and the port it left
through, and reads no ray identity or remote state. Rays of another record
that merged with them at that Node are subtracted too; that coincidence needs
the same heading and phase from an adjacent Node. Rays that return later, from
any distance, are not excluded: this is one-link exclusion of the emitter's own
wake, not a general self-field law. Schema 2 decay attenuates each
ray on arrival with the same ratio and residue rules as octant stock. Open
boundaries record escaping rays. Ray fields reject octant seeds, axis/octant
weights, vector fields, field rules, spatial interactions, `node_execution` and
the shared field clock. Host work per Node is bounded by `ray_slots`. An emitted amount below `rays_per_tick` fills only as many headings as it has quanta and moves the cursor on by that many, so a small stock still sweeps the whole sequence in turn.

The [inverse-square probe](../examples/inverse-square/README.md) measures the
result: every Manhattan shell still carries exactly one tick of emission, and
with an evenly spread heading sequence the time-averaged flux per node follows the
solid angle the node subtends from the source, in every direction. The
[gravity probe](../examples/gravity-probe/README.md) then couples held and moving
bodies to that flux with `mass x flux / D` and reports attraction, an inverse
square in every direction, and mass-independent acceleration.

### Funded emission and absorption

A ray field whose emitting type also carries a scalar field of the same name may
emit with `"source": false`: the emitted amount is paid from the record's own
stock, clipped to what it holds, and no external source is recorded. An optional
`"recoil_field"` names an owned signed vector that loses `amount x heading` for
every emitted ray. The reverse is the `absorb` coupling mode: a record of the
absorbing type takes a share of every ray resident at its Node on the cycle
after arrival (`amount x fraction / fraction_denominator`, or the whole ray),
adds it to its own field of the same name and, with `momentum_field`,
`share x heading` to that vector; the rest of the ray is forwarded. Absorption
happens before forwarding and before this cycle's emission joins the residents,
so a record never swallows its fresh rays; with `self_exclusion` the rays of its
own last departure are left alone by exact heading and phase. Absorbers act in
slot order.

Quanta are signed when the field is. A funded emission of a negative amount
credits the emitter with what it emits, and the ray's momentum `amount x heading`
points back at the emitter; a record that absorbs a share of such a ray pays it
from its own stock, never beyond what it holds, and gains momentum toward the
source. That is attraction with the ledger closed: the pulled body pays for its
pull, and a body with nothing left is not pulled.

```json
"emissions": [{"type": "lamp", "field": "quanta", "amount": 2048, "source": false,
               "recoil_field": "momentum"}],
"spatial_couplings": [{"name": "sail_absorbs", "type": "sail", "field": "quanta",
                       "mode": "absorb", "momentum_field": "momentum"}]
```

Together with the [conservation audit](LOCAL_CONSERVATION.md), which measures
rays as quanta, this closes the ledger: energy is the amount, momentum is amount
times heading, and both move only between records and rays. Positive quanta
give radiation pressure; negative quanta give attraction paid by the absorber.
Schema 2 attenuation of such fields is not supported.

### Kerengonen: phased rays (`kerengonen-ray-field-v1`)

A ray field may add `"kerengonen": {"phase_steps": P, "phase_advance": k}`,
with `2 <= P <= 4096` and `0 <= k < P`. Every ray then carries a phase step,
starting at the emission rule's `kerengonen_phase` (default 0) and advancing by
`k` on every link. Rays merge only when heading, lattice phase and wave phase
all agree. Nothing else about transport changes: a ray still follows one
integer line, keeps its amount, and is counted whole by the ledger and the
audit.

Phase acts where rays meet. The coherence of the rays resident at one Node is
`|sum a e^(i phi)|^2 / (sum |a|)^2`, computed in bounded integers from a fixed
cosine table over phase differences (scale 256), so equal phases give exactly
one and opposite phases of equal amounts exactly zero. It gates two things:
the value a reader samples at the Node (couplings and `spatial_values` see the
ray total times the coherence, toward zero), and the share an `absorb` coupling
takes of each ray. Quanta that cancel are not absorbed and not seen; they
continue along their lines and are absorbed or escape elsewhere. The total is
never changed by phase: the audit measures amounts, not coherence.

How an absorber takes a ray is a run-time choice, `"capture"`. The default
`"share"` takes the coherent share of each ray's amount, truncated toward
zero, and forwards the rest: a single quantum at a half-coherent Node is never
taken. `"lottery"` takes the whole ray or nothing: the record advances a local
ticket, seeded by `"capture_seed"` and salted by the ray it meets, and takes
the ray when the ticket falls below the coherent share. At full coherence the
two are identical; at partial coherence the lottery builds the fringe click
by click, one whole quantum at a time, with the coherent share as its rate.
The ticket state is a record row (`absorb_tickets`), never a global number,
and the same seed with the same rays repeats the same clicks.

Two sources in phase therefore give a fringe in Manhattan path difference:
`k x (d_a - d_b)` steps. One source alone never interferes with itself, because
rays that meet at one Node on one tick have traveled the same number of links;
it does through a Huygens source. A record that absorbs on the field keeps, per
absorb rule, the phase step nearest the direction of the coherent sum of what
it took (`absorbed_phases`, a record row), and an emission with
`"kerengonen_phase": "carried"` starts its rays at that phase plus one advance,
the emitter's own tick. A slit that absorbs and re-emits its stock every cycle
therefore continues the wave that reached it, and two slits lit by one lamp are
two sources in the lamp's phase. A carried phase requires an absorb rule on the
same field for the emitting type.

A ray may also carry its own advance per link. An emission with
`"kerengonen_advance": {"amount": <expression>, "denominator": D}` evaluates the
expression over the emitter's own fields, divides by `D`, takes the result
modulo the phase steps, and stamps it on every ray it emits; rays merge only
with equal advance, and a Huygens re-emission carries the advance of the
largest share it absorbed with the phase. An advance from the emitter's
momentum, `|p| / D`, is the de Broglie rule: a faster beam has a shorter
wavelength, and the [de Broglie probe](../examples/de-broglie/README.md)
measures the fringe spacing it gives. A ray without its own advance uses the
field's. Without the key the field is the plain `isotropic-ray-field-v1`; a
`kerengonen_phase` or `kerengonen_advance` on an emission requires the key. The
runner records the identity `kerengonen-ray-field-v1`. The [double-slit probe](../examples/kerengonen-double-slit/README.md)
measures the fringe on a line of absorbers.

## Finite completed-link decay

Schema 2 requires integer parameters `0 <= p < q <= 1_073_741_823`, with
`p = retain_numerator` and `q = retain_denominator`. On completing a link with an
interior receiving node, each original packet's octant component `v` becomes:

```text
retained = sign(v) * floor(abs(v) * p / q)
removed = v - retained
```

The optional `residue` key decides the fate of `removed`. The default
`"localize"` deposits it as stationary stock at the receiving Node (see
[Localizing residue](#localizing-residue) below). The explicit `"dissipate"`
option records it as loss, as the rest of this section describes.

This operates before packets are merged at the destination. For example, two
separate incoming components of 1 with `p/q = 1/2` both disappear; merging them
first and retaining 1 would implement a different law. The six delivered samples
are built from the attenuated arrivals. Resident seeds and newly committed
reactions first traverse a full link before this loss is applied. There is no
loss merely because a carrier waits or a diagnostic reads a node.

Under `"residue": "dissipate"` no decay remainder is retained. That is an explicit
dissipative integer law, not conservation-preserving division. The immutable baseline is exempt and
persists even after all dynamic populations vanish. Each component retains its
own sign until it becomes zero, but component-wise rounding can change a vector's
direction and norm. It does not conserve physical momentum or energy. Exact
opposite reactions at coupling commit remain a separate local property.

Every nonzero integer component loses moving magnitude on each completed interior
link or leaves the domain through an open boundary. For a
fixed finite set of initial records, initial populations and finite source and
coupling budgets, total absolute dynamic injection is bounded. Once the last
nonzero input has occurred, all moving spatial populations therefore come to
rest after finitely many links, including on the periodic lattice: as deposits
under the default residue, or as recorded loss under `"dissipate"`. This does not
promise that carriers stop moving or that unused allowances reach zero, nor a
universal extinction tick independent of the source schedule. Allocation phases
may remain in sparse nodes after their physical stock vanishes.

### Localizing residue

The default residue, `"localize"`, preserves signed component inventory:
it keeps the same retained quantity moving, but the removed fraction
`v - retained` is deposited as stationary stock owned by the receiving Node
instead of being recorded as loss. Omitting `residue` selects it; the historical
loss law needs the explicit key:

```json
"decay": {"retain_numerator": 1, "retain_denominator": 2}
"decay": {"retain_numerator": 1, "retain_denominator": 2, "residue": "dissipate"}
```

The deposit is computed per original packet/octant/component before merging,
exactly like dissipation, so two separate arrivals of 1 with `p/q = 1/2` deposit
two stationary units at that Node. A deposit stays at its Node: it is never
transported, split, decayed, sampled into the six delivered readings or read by
field rules and couplings, and it does not enter `value`. Localizing fields
report it separately as `localized` in node values, snapshots and accounting.
Under this residue the dissipation ledger stays zero and total field inventory,
moving stock plus deposits, is preserved: a wave that thins below one unit ends
as whole units at known Nodes rather than as recorded loss. Idle Nodes keep their
deposits; a committed-deposit ledger totals them without scanning idle history. The runner
records `finite-localizing-v1` when every spatial field localizes, otherwise
`finite-dissipative-v1`, and lists each field's residue in `spatial_decay_residue`.
The schema 1 conservation audits do not cover schema 2; the engine accounting
`balanced` flag and the runner's conservation flag check the preserved total.
This is a configured integer law, not a derived particle or absorption model.
In [finite_fields.json](../examples/finite_fields.json) every emitted unit ends
at rest at a known Node with zero dissipation.

## Event order and cost

At interval start `t`, each active node evaluates resident sources and combines
them with its owned octants. It validates the complete local proposal, moves
ownership into six fixed link packets and records injection. Delivery occurs
at `t + link_ticks`. In schema 2, decay is evaluated separately on each packet
reaching an interior receiver before validating the combined destination and
clearing packet ownership.
No received influence crosses another link in the same event.

The configured `boundary` applies to fields and carriers alike. `periodic` wraps
across every positive and negative axis face without changing the packet port or
octant label. `open` sends a terminal packet out of the simulation after the same
full link time. Its original signed populations become escaped quantity; they
are not decayed, merged or sampled outside because no exterior receiver exists.
A baseline never enters a packet or the escaped ledger. See
[the boundary contract](DISTURBANCES.md#domain-boundary).

By default the candidate has a separate fixed field clock. Priced spatial work contributes
to a new carrier cycle at the same node and interval; spatial forwarding itself
does not wait for the carrier. Thus `normal_budget` controls carrier delay and
does not bound the field stage's throughput. This is an explicit change from
the old single uniform-delay stage, supported by the requested fixed-c field.
Configurations without spatial fields retain the old timing contract.

Set `spatial_computation_delay: true` for the alternative
[shared field/carrier clock](SPATIAL_COMPUTATION_DELAY.md). In that mode all
local work determines one wait, emission happens at commit, and later input is
retained separately. The following fixed-clock scheduling details describe the
default mode; receipt decay and integer inventory rules apply to both modes.

Every field operation, including receipt and configured decay, has a price.
Completed-link decay cost is accumulated at the receiving node and charged once
in its next spatial cycle, alongside receipt and merge work. This does not change
link speed. Inactive empty nodes retain their allocation phases without repeatedly
charging old field work.

The host scheduler indexes nodes with field work or one pending cleanup phase,
plus resident emitters and spatially coupled carriers. A known idle node retains
its octant allocation phases and zero cost without a full history scan. New
arrivals and committed reactions reactivate their local node. An idle node's
empty-phase timestamp is resolved from the field clock when accessed; a newly
created node is never backdated. This is host bookkeeping, not a skipped physical
tick or a changed delay. Inventory diagnostics may use this index because idle
nodes own no dynamic populations. Neither the index nor measured totals supplies
values to a field law.
A previously frozen carrier proposal retains its original physical values and
cost; later field activity does not create computation debt. Carriers within
the normal budget move every interval, without an arbitrary extra wait.

## Accounting and output

Each conservative local split satisfies old inventory plus injection equals
outgoing inventory. Read-only totals include baseline, spatial stock, waiting
carrier originals and all in-flight packets once. The component-wise balances are:

```text
schema 1: final = initial + committed sources - escaped
schema 2: final = initial + committed sources - committed dissipation - escaped
```

Dissipation is a signed loss
ledger: removing a negative component records a negative loss. A `conserved`
declaration still requires exact accounting; schema 2 explicitly includes this
loss and does not promise constant physical totals.

Runs remain headless by default. `state.json` separates disturbances, spatial
baselines, octants, directional samples and packets. Events record field costs,
injection, sends, receipts and committed decay. Source/configuration fingerprints,
the selected schema policy and per-tick balance checks cover the combined world.

Records with carried source or exchange state also expose a decoded
`bookkeeping` section in snapshots, in configured rule order. These fractions
and allocation phases are not additional conserved field stock. Remaining
emission and coupling allowances are also exposed separately from inventory.

## Response and self interaction

Outward propagation does not establish that a source always arrives before its
own field. Both can traverse the same link together. A turn can collect earlier
contributions along multiple paths; a periodic boundary can return old field.
Merged integer allocation is not generally source-linear. Automatic self
subtraction is not enabled by this extension. Unknown self-filter settings fail
instead of being silently ignored. Optional [spatial couplings](SPATIAL_COUPLINGS.md)
now provide generic exchange and exact discrete rotation with a local opposite
field reaction. Their straight-line flux response has a restricted geometric
self-interaction guarantee; it does not claim general source attribution.
Existing explicit paired-record couplings remain available independently.

A future self filter must provide a bounded local attribution law and pass both
isolated-source and external-source controls. Shadow worlds, source histories
and global isolation checks may be diagnostic references only, never physical
inputs. The transport candidate does not establish a general force law.
