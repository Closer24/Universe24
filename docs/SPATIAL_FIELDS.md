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

## Carried allocation phases

`split_outward` partitions each octant population over the three allowed
cardinal directions by walking a cycle of axis weights from an allocation
phase. Highlights 3.3.1 requires the remainder of that integer division to be
carried into later updates. `"allocation_phase"` selects who owns it:

- `"straight"` (default): every nonzero portion leaves with the first slot of
  its own axis. A lone unit therefore keeps its axis and travels a straight
  ray at link speed; only when portions of the same octant meet at a node do
  their phases merge (by addition modulo the axis weight total) and the group
  spreads again. Directions are decided where the field is still divisible,
  near its source, and kept afterwards.
- `"rotate"`: every portion leaves with the slot after its last allocated slot,
  so a lone unit visits the axes in turn along its octant. The far field is
  isotropic in the Manhattan sense but no lone unit advances along an axis
  faster than one third of link speed.
- `"node"`: the legacy node-owned phase for identified old configurations. A
  fresh node starts at the first axis weight, so far-field units all follow
  that axis.

The transported quantity is unchanged by this choice: every portion is still
allocated exactly and every component is conserved. Only the destination of
indivisible units differs. With node-owned phases a decay-free 216-unit pulse
froze into 178 far-field cells whose units all travelled along the first axis
weight; with rotating phases the unit-weighted mean distances along x, y and z
agreed within a few percent but a lamp sixteen links away was never seen on
its axis within forty ticks; with straight phases the axial front moves at
link speed again while the axes share the units. Reaction packets committed
from carrier responses keep the node-owned phase in every mode. Run metadata
records `spatial_allocation` as `carried-straight-phase-v1`,
`carried-rotate-phase-v1` or `node-phase-legacy`.

## Computation field and local delay

Highlights 4.4 defines the computational field as a configured field whose
local scalar describes the cycle's modeled work and couples to delay through
`k = max(1, ceil(C / B))`. The top-level member `"computation_field"` names an
unsigned conserved scalar outward field for that role. Its local value at a
node, the immutable baseline plus the stock present before that interval's
forwarding, is added to the cost `C` of every carrier cycle at the node, in
addition to the priced field operations already contributed. Nothing else
changes: the field is emitted, transported, diluted and accounted like any
other conserved outward field, and no mass, distance or force enters the law.

Because the field is conserved, its total stays constant while it dilutes
with distance, so the extra cost decays with the field itself. With a mass
emitting 24000 units per interval and `normal_budget` 100, held clocks at
distances 1, 2, 3, 4 and 8 completed 2, 6, 12, 23 and 40 of 40 cycles; a large
budget restores 40 everywhere without changing the field. A moving carrier
crossing such a region is delayed the same way. Under the
[shared computation cycle](SPATIAL_COMPUTATION_DELAY.md) the same load also
prices field forwarding, so other fields crossing the region are delayed: with
budget 200 a light pulse reached a node 16 links behind an emitting mass at
tick 16 without the mass and not within 40 ticks with it, while a node six
links off that line saw its first light at the same tick in both cases. This
is the local delay law applied to a configured field, not a derived
gravitational potential; whether the resulting profile matches any physical
law is a separate measurement.

### Directional delay

The six delivered channels of the computation field carry more than its local
sum. With `"delay_direction": "along"` or `"against"`, the load no longer
delays the whole cycle. Local updates commit after the bare cycle time, and
each departure through a port waits for its own `k`, computed from the cycle
cost plus the baseline plus the load delivered through one channel: the field
travelling in the same direction as the departure (`along`), or the field
arriving from the side the departure heads to (`against`). The extra wait is
spent before the transfer's arrival, the `sent` event reports that arrival,
and the node starts no new cycle until its slowest departure has arrived.

The two conventions have opposite consequences. Under `along` a probe moving
towards the emitting mass is never delayed while a probe moving away stalls
where the outward field is dense: falling in is free and climbing out is
slow. Under `against` the approach slows and the climb out is free. With a
mass emitting 24000 units per interval, budget 100 and probes at half link
speed, `along` left the inward probe on its two-tick cadence through the mass
and stalled the outward probe for seven ticks, and `against` did the reverse.
A resting body is never moved. Both are configured hypotheses; neither is a
derived force, and the option requires the default clock.

### Ray delay and phase per interval

By default the field clock is fixed: a ray crosses one link per interval
whatever the computation load of the Node it rests at, so a mass delays the
carriers that pass it and not the rays. `"ray_delay": true` (default clock,
`computation_field` set) makes rays wait too: on a field cycle at a Node whose
resident rays have no wait pending, the Node prices its load alone with the
carrier timing rule, `k = ceil(load / normal_budget) - 1`, and holds its
resident rays for the next `k` field cycles; fresh emissions still leave, and
held rays stay owned by the Node, counted by every audit and exposed to its
absorbers on each waiting cycle. The waiting register is one bounded integer
per Node (`ray_wait`).

A Kerengonen ray's phase advances per link, so a delayed ray arrives later with
the phase of an undelayed one and an interferometer cannot see the delay.
`"ray_phase_per_tick": true` (requires `ray_delay` and a Kerengonen field)
advances the phase of every held ray by its advance on each waiting interval as
well, so two arms that waited differently meet with a phase difference of
`advance x (waits)` steps. Both keys are declared timing rules, not a
gravitational law: which of the two the world uses is a configuration choice
that the relativity probes compare.

### Least-delay routing

Directional delay alone changes when a hop happens, not where: the balanced
router picks lanes by their counters and the carried split walks its axis
cycle in a fixed order. `"least_delay_routing": true` closes the loop. A
carrier's balanced router and an outward field's carried split both read the
load pricing each port (the same `along` or `against` channel as the delay)
and take the cheapest eligible option first. Every lane still receives
exactly its reduced weight per cycle, so directional ratios remain exact
(Highlights 3.3.1) and only the order inside a cycle changes. Everything
therefore flows first towards the neighbor where computation is free.

That exactness also bounds the effect: a mover with one lane, such as
momentum `(0, 60, 0)`, has nothing to choose and is never turned, and a 1:1
diagonal can be reordered by at most one hop per two. Bending a straight
trajectory requires changing the momentum itself, which is a coupling, not a
routing choice. Light and other outward fields, whose octants always own
three lanes, are the natural users of this option. It requires
`delay_direction` and is recorded in run metadata as `least_delay_routing`.

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
| `phase_bits`, `charge`, `kerengonen` | The family's phase width, charge per quantum and phase rule: every ray is a wave ray ([wave-ray families](#wave-ray-families-wave-ray-family-v1), [Kerengonen](#kerengonen-phased-rays-kerengonen-ray-field-v1)) |
| `field_of` | Optional, with `release`: the name of the ray family this field is the field of ([released field](#field-as-the-rays-information-released-field-v1)) |
| `release` | With `field_of`: `[n, d]`, `1 <= n <= d`, the share of the source's amount each released ray carries per Node crossed |

An emitting record keeps a cursor into the heading sequence in its emission
phase register and advances it by `rays_per_tick` each tick, so a long sequence
spread evenly over the observer's sphere is swept over time. Rays of one event
with the same heading and phase merge exactly at a Node because they share one
line; rays of different events never merge
([ray state](#ray-state-ray-event-state-v1)). Delivered
samples and the `flux` leaf see ray arrivals per port, resident ray stock is the
local `value`, and node values report `ray_count`. A coupling reaction that
amends a departing packet leaves the rays on that port untouched, so rays pass
through Nodes whose carriers respond to them.

A record that emits rays and moves one link meets, at the next Node, exactly the
rays it emitted on the cycle it departed whose first DDA step took the same
port. With `"self_exclusion": true` the record carries two rows per emission
rule, this cycle's `(amount, cursor, wave phase, advance)` and the row from its last departure
(zero while it stays), and every coupling it evaluates after arriving reads the
sampled flux and value with those rays subtracted. The work is bounded by
`rays_per_tick`, uses only the record's own registers and the port it left
through, and reads no ray identity or remote state. The reconstructed rays
carry the departure's event state, so they match exactly the rays of that
emission event: a ray of another event, another record's or the same record's
earlier cycle, never merges with them
([ray state](#ray-state-ray-event-state-v1)) and is not subtracted. An
emitter that moves at link speed therefore meets the rays of its earlier
cycles as distinct events and treats them as foreign. Rays that return later,
from any distance, are not excluded: this is one-link exclusion of the
emitter's own wake, not a general self-field law. Schema 2 decay attenuates each
ray on arrival with the same ratio and residue rules as octant stock. Open
boundaries record escaping rays. Ray fields reject octant seeds, axis/octant
weights, vector fields, field rules, spatial interactions, `node_execution` and
the shared field clock. Host work per Node is bounded by `ray_slots`. An emitted amount below `rays_per_tick` fills only as many headings as it has quanta and moves the cursor on by that many, so a small stock still sweeps the whole sequence in turn.

The inverse-square probe (`examples/inverse-square/`, deleted on 2026-09-17) measures the
result: every Manhattan shell still carries exactly one tick of emission, and
with an evenly spread heading sequence the time-averaged flux per node follows the
solid angle the node subtends from the source, in every direction. The
gravity probe (`examples/gravity-probe/`, deleted on 2026-09-17) then couples held and moving
bodies to that flux with `mass x flux / D` and reports attraction, an inverse
square in every direction, and mass-independent acceleration.

### Ray state (`ray-event-state-v1`)

The rule ([Highlights](HIGHLIGHTS.md) 3.3, 3.19, 3.20 and 5.1; [ray-event
model](RAY_EVENT_MODEL.md#1-definitions), migration step 2): every ray
carries the number of steps it has made since its event and the information
of that event, and if that event was at a Detector, the bit drawn. They are
carried, part of the merge identity and validated. `steps` and `outbound`
are read by the return alone ([Detector return](#detector-return-detector-return-v1)):
the transport of a returning ray and the momentum readout. The event Ports,
the event shares and the Detector bit are hidden variables (Highlights 5.4),
read by no rule, coupling, absorber or readout. An existing world runs
exactly as before except where rays of different events used to merge; they
no longer do.

The `Ray` record (`core/spatial_state.py`) holds, beside its heading index,
DDA accumulators, amount, wave phase, advance, pace wait and interaction
delay:

| Field | Values | Rule |
| --- | --- | --- |
| `steps` | `0` to `MAX_VALUE` | Links walked since the ray's event: `+1` per Link while outbound, `-1` per Link on the walk back; `0` at the event Node. The count starts at the trajectory's origin event and resets only when the trajectory changes (a new event). A returning ray with no steps left is at its event Node: it stays resident there until the next cycle's inverse split ([below](#inverse-split-inverse-split-v1)); no Link is planned for it and a Link beyond its event Node is refused |
| `outbound` | `1` or `0` | `1` while the ray travels on its event's heading, `0` once it is reversed on its line. Every created ray is outbound; a draw of 0 at a marked Node sets `0` ([Detector return](#detector-return-detector-return-v1)) |
| `event_ports` | six-bit mask | The Ports the event sent to, bit `p` for Port `p` in the order `[+X, -X, +Y, -Y, +Z, -Z]` |
| `event_shares` | six bounded integers | The amount the event sent through each Port, in Port order, `0` where the mask bit is `0`. The record is fixed at six entries rather than a variable list: at most six records, one per Port (Highlights 3.20), and exactly the information of a mask-indexed list. A share is signed where the field is signed, like `amount`; the record stores the integer, not a zigzag code |
| `detector` | `0`, `1` or `2` | No Detector event, a Detector event that drew 0, a Detector event that drew 1. Every created ray carries `0`; a marked Node sets `1` or `2` on arrival ([Detector mark](#detector-mark-detector-mark-v1)), and no rule reads it |
| `lag` | three bounded signed integers | The lag of the ray's output-face clocks in phase steps, one per axis, positive toward the +axis Port ([binding](#binding-and-gravity-by-delay-ray-binding-v1)); `(0, 0, 0)` on every created ray, reset by a return |

Storage width: every stored value is bounded by `MAX_VALUE` (2^30 - 1); the
sums that form the shares and the step count are 64-bit intermediates
(`checked_work`) bounded before they are stored. The phase has the width its
family declares (`phase_bits`, [wave-ray families](#wave-ray-families-wave-ray-family-v1)),
a mask over 2^`phase_bits`: outbound, the phase advances by the ray's rate per
Link as before; on the walk back it decrements by the same rate, so the
phase, like the count, returns to what it was at the event. A ray that spends
a tick at its Node (pace wait, interaction delay, load hold) moves its phase
by the same signed step.

An event is where rays are created, and every ray it creates is stamped with
the event's mask and shares as a fresh outbound trajectory with `steps 0`:

- an emission (`emit_rays`: one record, one emission rule, one cycle, funded or
  sourced, swept or directed, and a mirror's reflection alike) is one event;
  its mask is the set of Ports its rays first step through, and its share per
  Port is the sum of their amounts, so a sweep of several headings that leave
  through one Port is one event on that Port;
- a ray interaction (`ray_interactions`) is one event per group that fires: its
  outputs, whether their heading changed or not, carry the mask and shares of
  all the group's outputs; a rule with declared `outputs` stamps the new rays
  that replace its participants the same way
  ([meetings with outputs](#meetings-with-outputs-ray-meeting-conversion-v1)).
  A group that does not fire leaves its rays, and their event state, untouched;
- the inverse split of a returned ray at its event Node is one event: its
  transmissions carry the mask of the lines transmitted to and the amount per
  line, and the returned ray's Detector bit
  ([inverse split](#inverse-split-inverse-split-v1)).

Merge identity: `merge_rays` combines rays that agree in heading, lattice
accumulators, wave phase, advance, wait, interaction delay, steps, outbound,
event Ports, event shares and Detector bit. Rays of different events never
merge, even with the same heading, family and phase: each keeps the
information of its own event, and two rays of one emitter's successive cycles
are two events. `ray_count` and slot use therefore count events on a line,
not lines, and one-Link self-exclusion excludes exactly the departure cycle's
rays (above). Nothing else changes: amounts, headings, phases, coherence,
absorption shares, totals and the audits are what they were, and the runner
records `ray_state: "ray-event-state-v1"` beside `sampling_profile`.

### Detector mark (`detector-mark-v1`)

The rule is stated in [Detector-owned sampling](DETECTOR_SAMPLING.md#the-detector-mark-detector-mark-v1)
([Highlights](HIGHLIGHTS.md) 3.19, 3.20 and 5.4; migration step 3 of the
[ray-event model](RAY_EVENT_MODEL.md#6-migration-in-order); issue #169,
feature 2). The schema key:

```json
"detectors": [{"position": [7, 7, 7], "setting": [1, 2], "seed": 3}]
```

| Key | Values | Rule |
| --- | --- | --- |
| `position` | three integers within `shape` | The marked Node; one mark per position |
| `setting` | `[n, d]`, `1 <= d <= MAX_VALUE`, `0 <= n <= d` | The pass share of the draw range: the bit is 1 when the drawn number times `d` is below `n` times `TICKET_MODULUS`. Required; there is no default rate |
| `seed` | `0 <= seed < TICKET_MODULUS` | The start of the mark's own ticket stream. Required |

All three keys are required and no other key is accepted. The parsed
`DetectorMark(position, pass_numerator, pass_denominator, seed)` records are
`InitialState.detectors`; the engine installs each on its Node as
`SpatialNodeState.detector` with `detector_ticket` seeded from `seed`. A
document with marks is admitted only under the shared Detector admission:
`schema_version` 1, `link_ticks` 1, at least one ray field, every ray field on
`"metric": "links"` with pace `1 / 1`, no decay and unit-axial headings closed
under negation, without `node_execution` or `spatial_computation_delay`.

On arrival each ray draws one bit from the mark's stream, in Port then
merge-key order, and leaves with its `detector` field set: `2` on 1, with a
`detector_click` event (position, tick, Port, family, amount, bit 1), the ray
continuing unchanged; `1` on 0, the ray returned on its line
([Detector return](#detector-return-detector-return-v1)) with a
`detector_return` event and no click. A document without `detectors` has no
marked Node and runs exactly as before, and the runner records
`detector_mark: "detector-mark-v1"`.

### Detector return (`detector-return-v1`)

The rule is stated in [Detector-owned sampling](DETECTOR_SAMPLING.md#the-return-detector-return-v1)
([Highlights](HIGHLIGHTS.md) 3.19, 3.20 and 5.4; migration step 4 of the
[ray-event model](RAY_EVENT_MODEL.md#6-migration-in-order), first half;
issue #169, feature 3). This section is the transport of a returning ray.

On a draw of 0 the arriving ray is returned in the same interval
(`return_ray`): heading index replaced by the index of the negated heading,
`outbound` 0, accumulators `(0, 0, 0)`, `wait` 0, `interaction_delay` 0,
everything else as it arrived. It is not counted in the Node's per-Port
delivered readings of that interval (as if it had not arrived), so the `flux`
sample and the `received_fields` of the `spatial_received` event do not see
it. At the next cycle it leaves through the Port it came in through, an
ordinary departure of `forward_rays`: one Link per tick, `steps` down by one
and the phase back by the field's advance per Link (`advance_ray`).

On the walk back a ray with `outbound` 0:

- enters no absorption: `_absorb` leaves it in the residents untouched and
  computes the coherence of the arrivals over the outbound rays only;
- takes part in no ray interaction: `apply_ray_interactions` gives it no
  participant view, so no group contains it;
- is not sampled: the value sample (`coherent_stock`) and the flux sample
  (`sample_fluxes`, both projections) that couplings read are taken over the
  outbound rays, and its arrival adds nothing to the per-Port readings;
- is not drawn for: a marked Node on its way sets nothing and records
  nothing;
- merges with nothing: `outbound` is in the merge key, and the returned ray
  is the only ray of its event on its line;
- counts: it is in the Node's rays, in `ray_count`, in the totals and in the
  escape check.

At `steps` 0 it is at its event Node and stops: `forward_rays` keeps it as a
resident ray with `outbound` 0 and does not move its phase, and `advance_ray`
refuses a Link for it. It carries exactly the phase, amount and event record
it left the event with, the Node keeps nothing else, and in the next cycle it
performs the inverse split ([below](#inverse-split-inverse-split-v1)).

`ray_momentum` reads a ray with `outbound` 0 as amount times its heading
negated, its share of the event on the event's heading, in the totals, the
carried-heading flux projection and the escape ledger alike: a return leaves
the momentum total unchanged and the audits exact. A returning ray in a
packet that would leave an open boundary is a validation error (its event
Node is not in the world), never an escape. The runner records
`detector_return: "detector-return-v1"`, and a world without a mark has no
returning ray and runs byte for byte as before.

### Inverse split (`inverse-split-v1`)

The rule is stated in [Detector-owned sampling](DETECTOR_SAMPLING.md#the-inverse-split-inverse-split-v1)
([Highlights](HIGHLIGHTS.md) 3.20 and 5.4; migration step 4 of the
[ray-event model](RAY_EVENT_MODEL.md#6-migration-in-order), second half;
issue #169, feature 4). This section is the transmission as an event ray and
the restore-and-refund bookkeeping. The world key:

```json
"return_mode": "siblings"
```

| Value | What a returned ray does at its event Node |
| --- | --- |
| `siblings` (default) | Transmits its amount, phase and bit to every Port of its event's mask except its own, the amount shared exactly with the remainder to the first Ports in Port order |
| `straight` | Continues on the one Port opposite its own with its whole amount, phase and bit |
| `annul` | Ends there; amount and momentum reading into the annulled sink |

Any other value is rejected before a world is constructed. The key is read
only for a returned ray, so a world without a mark runs byte for byte as
before.

**The transmission.** In `SpatialLaw.__call__`, for each ray field after
`_absorb` and before `forward_rays`, `_inverse_split` takes every resident
ray with `outbound` 0 and `steps` 0 out of the residents and calls
`transmit` (`core/spatial_state.py`): the Ports (`split_ports`: the mask
minus the own Port, the opposite Port, or none), the amounts
(`split_amounts`, Highlights 3.17), one `Ray` per Port on the unit-axial
heading that leaves through it (`port_heading`; a field without that line
fails closed), accumulators `(0, 0, 0)`, the returned ray's phase and
advance, stamped as one event (`stamp_event`: `steps` 0, `outbound` 1,
`event_ports` the mask of those Ports, `event_shares` the amount per Port)
with the returned ray's `detector` copied on. The transmissions join this
cycle's emitted rays, so they leave on this cycle with the residents, one
Link per tick, and merge with nothing of another event. A one-line event
in `siblings` transmits nothing; with no input at the Node that is a
validation error.

**Restore and refund.** When a record with a funded emission rule into the
field is at the Node (the event's input, the first such record in slot
order), `_refund` first adds the returned share to the record's stock of
the field and, if the rule has a `recoil_field`, share x event heading to
its recoil (the returned ray's `ray_momentum`), the exact inverse of the
funded-emission bookkeeping; then it takes the transmitted amounts (or the
annulled amount) out of the stock and amount x heading per transmission (or
the annulled momentum) out of the recoil. Both are booked in the cycle's
`transfer_delta` (restore as absorbed, funding as funded), so the spatial
accounting's reactions move by zero net and the record's values validate at
each step; a stock or recoil the field cannot hold fails closed with a
clear error. The plan's ray conservation check counts a restored or
annulled share as taken out of the residents. Without such a record the
share's momentum reading and the transmission's momentum are booked in the
source ledger, as a sourced emission's rays are.

**The sink.** `SpatialPlan.annulled` carries the per-field content annulled
by the cycle; the Node books it through `SpatialAccounting.record_annulled`
into `SpatialEngine.annulled`, read by `annulled_totals()`, by the spatial
accounting (`balanced` subtracts it) and by the runner's conservation line.
The `inverse_split` record (position, tick, family, mode, ports, amounts,
amount, bit, restored, annulled) carries the same per-field values, and the
local conservation audit adds them to the Node's residual, so a world under
the audit passes with content annulled.

**Momentum.** The transmission reads as amount times its heading, a ray like
any other. In `siblings` and `straight` through a lamp, the lamp's recoil
takes the returned share's momentum back and gives the transmission's, so
the momentum total is unchanged; in `annul` the sink takes the share's
reading and the lamp is unchanged.

### Layers (`ray-layers-v1`)

The rule ([Highlights](HIGHLIGHTS.md) 5.1; [ray-event
model](RAY_EVENT_MODEL.md#1-definitions)): event spacetime has layers. A
layer is a set of families that couple, and a meeting exists only inside a
layer. Rays whose families have no declared coupling never meet: they cross
as if the other were not there, so two events can happen at the same Node
in the same interval in layers that do not communicate.

Layers are derived, never declared. A family is a ray field and the
catalog's couplings are the declared `ray_interactions`: the layers are the
connected components of the ray fields over the participants of those
rules, where every field a rule's roles can select is one participant set
(a rule whose roles select `a` and `b` puts `a` and `b` in one layer, and
two rules that share a field chain their fields into one layer). A ray
field that no rule selects is its own layer and always crosses.
`ray_layers` (`core/spatial_state.py`) derives them from the catalog once,
when the `SpatialLaw` is built, as a tuple of tuples of spatial-field
indices in field order, bounded by the number of spatial fields; the runner
records `ray_layers: "ray-layers-v1"` and `ray_layer_families`, the derived
layers as lists of field names sorted within each layer and between layers,
in `run.json` beside `ray_state`.

At a Node in one interval the interaction step (`apply_ray_interactions`)
meets the resident rays layer by layer. For each layer that has a rule, its
rays and only its rays are the candidate participants; its rules fire in
declared order, each with its own participants, guard, invariants and
events, exactly as the [shared coupling contract](SHARED_RAY_COUPLING.md)
states for one layer; a ray of a layer that has no rule, or whose rules do
not fire, crosses unchanged with its event record intact. Rules of
different layers therefore fire independently in the same cycle, and a ray
of one layer is never a participant, a blocker or a merge partner of a ray
of another: the indexed selector's 32-slot participant capacity is a bound
per layer (the declared `ray_slots` of the fields of one layer with a rule
sum to at most 32), rays of different fields never merge, and there is no
occupied channel and no capacity rule between layers. The Node's proposal
stays one atomic commit: a failed guard or invariant in any layer rejects
the interval's proposal before any owner changes, as before. A world with a
single layer runs byte-identically to the previous rule, and the existing
suite is its regression. No new draw, no new arithmetic and no new
initialization key; the Detector (issue #169, feature 2) is untouched.

### Meetings with outputs (`ray-meeting-conversion-v1`)

The rule ([Highlights](HIGHLIGHTS.md) 3.15, 3.17, 3.26 and 5.1; [ray-event
model](RAY_EVENT_MODEL.md#6-migration-in-order), step 6): at a meeting the
declared coupling decides a deterministic interaction with exact invariants
and at most six events out. A `ray_interactions` rule with `outputs`
replaces its participants, two to six rays of one layer, by one to six new
rays at the meeting Node, one per output. Each output is a new event ray:
`steps 0`, `outbound 1`, `event_ports` the mask of the Ports the outputs
leave through, `event_shares` the amount per Port, `detector 0`, so outputs
on distinct Ports are distinct events in the record and two outputs on one
Port are one share; nothing is left at the Node. A rule with outputs declares
no `assignments`: it assigns through its outputs.

| Key | Contract |
| --- | --- |
| `field` | The output's family, a ray field; the layers derivation puts a rule's output fields in its layer |
| `amount` | An integer of at least 1; `{"of": i}`, input i's amount; `{"of": "sum"}`, the sum over the inputs; a split by a table (below); `{"rest_of": j}`, the rest of the content that output j's table splits |
| `heading` | A Port index 0 to 5 (the unit-axial heading in Port order, which the field's heading table must contain), `"same"` (the source input's heading) or `"reversed"` (its negation) |
| `phase` | Optional, default `"same"`, the source input's phase; an integer offset k below the phase modulus, the source input's phase plus k; `{"of": i, "offset": k}`, input i's phase plus k; read modulo the field's phase steps |
| `delay` | Optional nonnegative interaction delay, default 0; or `{"of": i, "table": [six], "per": u}`, a delay by a declared table per the Port input i came through ([binding](#binding-and-gravity-by-delay-ray-binding-v1)) |
| `input` | Optional source input index, default 0: the input whose heading and phase the output reads by default; every output carries its source input's advance |

The rule's `invariants` are per-ray readouts (`{"field": "amount"}`,
`{"op": "mul", "args": [{"field": "amount"}, {"field": "heading"}]}`) summed
over the inputs and over the outputs and compared exactly, as the
[N-to-M conversion](LOCAL_CONVERSIONS.md#n-to-m-family-conversion) of records
did until bucket B.6 deleted it on 2026-09-17; the total amount and the stock of every family (the sum of the amounts
of one field over the inputs equals the sum over its outputs) are checked
without a declaration, so no family total changes and the spatial
accounting's `rule_delta` is zero. Every output is a ray of its `field` with
that family's charge per quantum, and the charge readout of feature 9
(`charge x amount` of one ray, summed over the inputs and over the outputs) is
appended to every meeting's invariants as the `charge` invariant, checked like
the declared ones. Momentum is a declared invariant, as in the
[shared coupling contract](SHARED_RAY_COUPLING.md): the adapter hardcodes no
physical formula. A false guard leaves the group untouched; a failed check
rejects the interval's proposal before any owner changes. The arithmetic is
`convert_values` (`fields/disturbances.py`), one pure function over bounded
integers (the record conversion that shared it was deleted on 2026-09-17,
issue #164 bucket B.6): the
guard, the outputs built from the frozen inputs, the table splits, the
conserved sums and the invariant sums, returning the outputs and the
remainder.

**Split by a table (the Born decision).** An output amount may be
`{"table": [n0, n1, ...], "of": "sum", "index": "phase_difference"}` (`of`
may also name one input, and `"between": [i, j]` the two inputs, default 0
and 1): the content is shared between this output and the one that declares
`{"rest_of": <this output>}` in the ratio `table[d] : (m - table[d])`, `m`
the table length, which must equal the phase modulus of the rule's fields,
and `d = (phase_j - phase_i) mod m` the phase difference of the two inputs;
every entry is an integer from 0 to m. The reference table for 8 phase steps
is `[8, 7, 4, 1, 0, 1, 4, 7]`, cos^2(d/2) in eighths, rounded. The engine
only splits by the table; the physics is the declared table. The table
output takes the whole quanta of its share, `floor(content x table[d] / m)`;
the rest output takes the rest, so the quantum that the two floors leave,
the remainder, has an explicit bounded owner, the rest output, and never a
Node register (Highlights 3.17 and 3.20); `convert_values` reports it and
charges one `split` per table. An output of amount zero is no ray and no
Port in the mask: at d = 0 the whole content leaves through the table
output's Port, at half a turn through the rest output's, at a quarter turn
half through each.

**Momentum of a split.** A split between two Ports moves the rays' momentum
(amount x heading) and no ray owns the difference: the recoil belongs to the
[field ray](#field-as-the-rays-information-released-field-v1), and what the
returning field ray does when it reaches its source is the declared coupling
of feature 8. Until that coupling exists the spatial law books the momentum
change of a meeting as an explicitly accounted source of the ray field's
momentum field (Highlights 3.15), so `source_totals` names it and
`conserved_at_every_completed_tick` stays exact. The local energy/momentum
audit (`diagnostics/local_conservation.py`) has no source term for it (it
reads releases as sources since `ray-event-audit-v1`), so a world
that declares it must keep momentum at every meeting, as a declared momentum
invariant does.

Bounds and admission: two to six participants, one to six outputs, one table
split per pair of outputs, the admission of every ray interaction (schema 1,
`link_ticks` 1, positive unit-axial unpaced fields, no decay, no absorption
on the selected fields), and at most `ray_slots` rays per field after the
meeting; more is an explicit failure. The outputs are new rays with
accumulators (0, 0, 0) and pace wait 0. No draw anywhere; the Detector
(feature 2) is not touched; a family with no rule crosses
([layers](#layers-ray-layers-v1)); existing worlds with single-output rules
run byte-identically, and the runner records
`ray_meeting: "ray-meeting-conversion-v1"` beside `ray_layers`.

```json
{"name": "split", "participants": [{"type": "a"}, {"type": "a"}],
 "outputs": [
   {"field": "a", "amount": {"table": [8, 7, 4, 1, 0, 1, 4, 7], "of": "sum", "index": "phase_difference"}, "heading": 2},
   {"field": "a", "amount": {"rest_of": 0}, "heading": 3, "phase": {"of": 1}}],
 "invariants": [{"name": "energy", "expression": {"field": "amount"}}]}
```
### Wave-ray families (`wave-ray-family-v1`)

The rule ([Highlights](HIGHLIGHTS.md) 3.3 and 5.1; [ray-event
model](RAY_EVENT_MODEL.md#6-migration-in-order), the wave-ray part of
migration step 6): every ray is a wave ray and carries a phase; a plain ray is
the special case of the wave ray whose family's rest rate is 0, not a second
kind. Three things change a phase and nothing else: each interval advances it
at the rest rate its family declares (the ray's mass as a clock, zero for
light), an interaction changes it as the declared coupling says, and a bound
group advances it once per interval it is held (feature 8 of issue #169). A
light ray carries the phase of the clock that emitted it and delivers it
unchanged. Every ray field is one family, and its `spatial_fields` entry is the
catalog entry that declares the family's phase rule and charge; the engine
applies what the catalog says and holds no phase rule of its own.

| Key | Contract |
| --- | --- |
| `phase_bits` | Optional, ray transport only: the width of the phase every ray of the family carries, an integer at least 0. The phase is an integer from 0 below 2^`phase_bits`, and every phase advance and difference is a mask with 2^`phase_bits` - 1, never a division. Default 0 (one phase value: the plain field of every existing world), or log2 of `kerengonen.phase_steps` when a coherence table is declared, so an existing Kerengonen world keeps its modulus (8 phase steps is `phase_bits` 3); both given, they must agree. The model sets no upper bound: Python integers are unbounded, and a Rust or GPU port uses a two-word type above 64 bits |
| `kerengonen.phase_advance` | The family's rest rate: the steps its phase advances every interval, an integer from 0 below 2^`phase_bits`, bounded by the width and not by `MAX_VALUE`; required with the `kerengonen` key, 0 without it. Light is a family with rest rate 0: a plain field with a declared width, or the key with `phase_advance` 0 |
| `kerengonen.phase_steps` | Optional with the key: the coherence table of the Kerengonen coupling (below), one entry per phase step of one turn, 2^`phase_bits` entries, a power of two from 2 to 4096 (at most twelve bits). A family with a rest rate and no table meets readers and absorbers without coherence gating; `capture`, a carried phase and a mirror require the table |
| `charge` | Optional, ray transport only: the family's charge per quantum, a bounded signed integer, default 0 |

An emission stamps its `kerengonen_phase` on any ray field of the declared
width, a plain field included: the ray carries the emitter's phase along its
line, advancing by the family's rest rate per Link (and per waiting interval,
[ray delay](#ray-delay-and-phase-per-interval)), so a light ray delivers the
emitter's phase unchanged and a massive ray arrives with `phase + rate x Links`,
masked. Without a declared width only phase 0 is admissible, which is what
every existing plain world carries. A ray's own advance (`kerengonen_advance`)
overrides the family's rate and requires the key. The phase is the one value
with its own declared width (issue #169, 2026-09-17); two host limits follow
from what else stores it. The coherence table has at most 4096 entries, so a
phase wider than twelve bits has no table. A ray interaction views the phase
as a stored value (`MAX_VALUE`, thirty bits) and a self-exclusion row stores
it likewise, so `ray_interactions` on the family and `self_exclusion` require
`phase_bits` at most 30. Everything else (content, steps, shares, headings)
keeps 32-bit storage and 64-bit intermediates.

`RAY_PROPERTIES`, the view of a ray in a [ray interaction](SHARED_RAY_COUPLING.md),
gains two read-only properties: `family`, the index of the ray's spatial
field, and `charge`, the family's charge per quantum. Charge is per quantum
because amounts merge and split; the charge readout of a bundle is `charge x
amount` summed over its rays (`ray_charge`), and `charge_totals()` reads it
per ray field over the rays resident at active Nodes and in flight on Links,
the owners `totals()` reads (escaped charge and the runner's conservation flag
are feature 10). The readout is an invariant of every declared ray
interaction: the parser appends `charge`, `charge x amount` summed over the
participants, to the rule's invariants, checked like the declared ones, exact
before and after; a declared invariant named `charge` is refused, an
assignment to `family` or `charge` is refused as read-only, and a rule may
declare at most fifteen invariants of its own.

Nothing else changes: an existing world without ray interactions runs
byte-identically (a plain field has width 0 and rate 0; a Kerengonen field has
the width of its `phase_steps`, and the mask equals its former modulus), and a
world with ray interactions reads the two added view components per
participant (`read` cost 9 instead of 7) and is otherwise identical. The runner
records `wave_ray: "wave-ray-family-v1"` beside `ray_state`.
`test_wave_ray_families.py` ([expectations](TEST_EXPECTATIONS.md#wave-ray-families))
is the test.

### Field as the ray's information (`released-field-v1`)

The one field rule ([Highlights](HIGHLIGHTS.md) 3.3, 3.5, 3.14, 3.15, 3.17
and 3.28; [ray-event model](RAY_EVENT_MODEL.md#6-migration-in-order), step
7; issue #169, feature 7): a ray has a field, and the field is the ray's own
information spreading in ray form to the Nodes around it, without an event.
A ray field G declared with `field_of: F` and `release: [n, d]` is the field
of the ray family F:

```json
{"field": "G", "baseline": 0, "transport": "ray", "headings": [[1, 0, 0], ...],
 "rays_per_tick": 1, "ray_slots": 16, "field_of": "electron", "release": [1, 4],
 "kerengonen": {"phase_steps": 8, "phase_advance": 0}}
```

**The release.** At every Node an F ray is at, in every interval it is
there, held by a coupling or a clock as well as the interval it departs in
(the release does not wait for the clock, [Highlights](HIGHLIGHTS.md) 3.5),
G rays are released at that Node, one per
Port heading except the F ray's own, each of amount `floor(amount_F x n /
d)`, with `event_ports` 0, `event_shares` all zero, `steps` 0, `outbound` 1,
`detector` 0, accumulators (0, 0, 0) and the F ray's phase at the release:
the field carries its emitter's phase, and G declares its own `phase_advance`
(0 delivers the phase unchanged, as light does). The fraction the floor
leaves is not released: the field is a description booked as a source, so
nothing owned is destroyed and no remainder needs an owner (Highlights
3.17); a release whose floor is 0 releases nothing. The released rays leave
in the same interval as the F ray, with the residents; the release is a
departure, not an arrival, so it is no meeting. A ray of a family that has a
meeting rule releases after the interval's meetings, from the trajectory
that departs. The release does not wait for the clock (Highlights 3.5,
model owner, 2026-09-17): a field release is information, not a departure
of matter, so a ray held at a Node by an output-clock delay (`ray_delay`,
feature 8) is content resident there and releases every interval it is
held, on all six headings as resident content does, while the clock delays
only its departure as matter; this slice releases from the departure, which
at pace 1/1 with no delay is every interval, and a held ray releases on all
six headings every interval it is held
([binding](#binding-and-gravity-by-delay-ray-binding-v1)). A G ray crosses
Nodes like any ray and releases nothing: a
field has no field, and the density of the field falls by the geometry of the
lattice alone. Until feature 12, field spreading (Highlights 3.5, model
owner, 2026-09-17), a G ray therefore stays on its line and the field of a
source lives on the six axis lines of the Nodes it crosses; with it every
Node that field content reaches releases it again by the family's declared
split table, and light, the field of a charge, is one such family. A G ray
that reaches an open boundary escapes like any ray.
`release_field` (`core/spatial_state.py`) is the pure function, called by the
spatial law after its emissions and before forwarding.

**The heading the ray travels on.** The ray's own line ahead of it is, at
link speed, the ray itself: the field is born where the ray is and leaves at
the causal speed, and the ray is never faster than its field (Highlights 3.5),
so under this admission (pace 1/1 for F and G) the forward heading is not
released and the five other headings are. That is the geometry of the
no-self-field rule: the release on the ray's own heading is the ray, the
release behind it walks away from it, and the four transverse releases leave
its line, so a straight ray never shares a Node with a ray of its own field
and no exclusion rule is needed. Only after a change of trajectory can a ray
cross field it released earlier, and that is a meeting like any other. A
slower family (feature 9) will release its forward field ahead of it.

**Resident content.** A record holding stock of F (a bound group in the
sense of Highlights 3.4, in this slice any resident record whose type owns
F) releases once per interval on all six headings, from the stock it still
holds after the interval's emission, with phase 0 (a record carries no phase
of its own in this slice); a record that has paid out its stock releases
nothing. A Node that holds such a record runs its spatial cycle every
interval.

**The booking.** G is not conserved by the F ray: the F ray pays nothing for
its field until the field meets something (Highlights 3.5), so its amount,
phase and heading are unchanged by the release, and the released amount, and
`amount x heading` into G's momentum field when one is bound, are booked as
an explicitly accounted source of G (Highlights 3.15). `source_totals` and
the per-tick `source_delta` name it, the spatial accounting balances at every
tick, and a G field declared conserved has total equal to its released sum
less what escaped.

**The recoil.** A meeting of a G ray with a family whose declared coupling
responds is an ordinary rule of `ray_interactions` with outputs
([meetings with outputs](#meetings-with-outputs-ray-meeting-conversion-v1)):
its outputs change the ray that was met as the rule says (heading, delay or
phase) and return the G ray reversed, an output of field G with heading
`"reversed"` of the G input and its amount, a new event ray at the meeting
Node stamped with the meeting's Ports and shares, so the recoil walks back
along the field ray's line toward the line of the ray that released it, at
finite speed (Highlights 3.14). The momentum the turn moves belongs to the
recoil's line; what the recoil does when it reaches its source or a bound
group is the declared coupling of feature 8, which uses it for gravity as
bending by delay (Highlights 3.28). No rule reads G unless declared: a family
with no coupling to G crosses it ([layers](#layers-ray-layers-v1)).

```json
{"name": "turn", "participants": [{"type": "electron"}, {"type": "G"}],
 "outputs": [
   {"field": "electron", "amount": {"of": 0}, "heading": "same", "input": 1, "phase": {"of": 0}},
   {"field": "G", "amount": {"of": 1}, "heading": "reversed", "input": 1}],
 "invariants": [{"name": "energy", "expression": {"field": "amount"}}]}
```

Admission: `field_of` and `release` are declared together, `field_of` names
another ray spatial field that is not itself a field of anything (a field has
no field), G carries the six Port headings, G and F are positive, conserved,
unpaced unit-axial ray fields on the links metric with zero baseline, no
decay and no self-exclusion, with the same phase width (`phase_bits`, and
so the same phase steps), under the shared
Detector admission (schema 1, `link_ticks` 1, the default fixed clock, no
field rules, spatial interactions, couplings or absorption on G or F). The
runner records `released_field: "released-field-v1"` and `released_fields`,
each field ray family with the family it is the field of and its ratio
(`[{"field": "G", "field_of": "electron", "release": [1, 4]}]`, empty when
none), beside `ray_meeting`, so a Renderer can draw the G rays faint from the
per-Node `ray_count` and `value` of that family. A world that declares no
`field_of` runs byte-identically.

### The external body (`external-body-v1`)

The second declared element of a world beside the Detector mark
([Highlights](HIGHLIGHTS.md) 3.19, model owner 2026-09-17; [ray-event
model](RAY_EVENT_MODEL.md#6-migration-in-order), feature 7b; issue #169): a
Node declared to hold a family with an amount of any width, standing for a
star, a fixed proton, a large charge or a piece of apparatus. Like the
Detector it is a declaration, not physics, and bounded Node metadata: the
kind of mark, the declaration, the momentum with its three accumulators and
one exact sink counter per family; no rays, no history.

```json
{"external_bodies": [
  {"position": [7, 7, 7], "family": "star", "amount": 4096, "charge": 0,
   "initial_momentum": {"heading": [1, 0, 0], "pace": [1, 4]},
   "coupling": "sink", "momentum_table": {"G": -1}, "phase": 0}
]}
```

**The declaration.** `position`, `family` (a ray spatial field that is not
itself a field of anything, unit-axial, on the links metric at pace 1, no
decay) and `amount` (a positive integer of any width: it enters no sum, it
only sets how much field leaves per interval) are required; `charge` (a
bounded integer, read by couplings as the family's charge is), `phase` (the
phase its field rays carry, below the family's width), `initial_momentum`
(a unit-axial `heading` and a rational `pace` `[n, d]` of Links per interval,
n at most d; the momentum is the whole quanta of amount x n / d on that
axis, signed; zero, the default, for a body at rest), `coupling` (`"sink"`,
the default, or the name of a declared ray interaction) and
`momentum_table` (family name to sign, -1 attraction toward the source of an
arriving field ray, 1 repulsion) are optional. One body per Node, never on a
Detector; a body is never a field family. A world with a body runs under the
shared Detector admission (schema 1, `link_ticks` 1, the default fixed
clock, no field rules, spatial interactions or couplings).

**The release.** Every interval the body releases the field of its family,
the ray field declared `field_of` its family, on all six Port headings: one
ray per heading of amount `floor(amount x n / d)` by that field's `release`,
with the body's declared phase, no event, one Link on with the residents.
The released stock is booked as an explicitly accounted source of the field
(and of its momentum field when one is bound), exactly as a bound group's
release of resident content (`release_stock`); the body's amount never
changes. In an interval the body steps through a Port, that heading is its
own line ahead of it, which its ray occupies, and it releases nothing there
(no self-field, Highlights 3.5). A body whose family has no `field_of`
radiates nothing. A body's Node exists and is active from the start.

**It does not spread.** The body never splits, binds, unbinds, converts or
decays: it is one flag in the Node's law, and every other step (the
arrivals, the meetings by table, the stamping, the departures of what
leaves) is unchanged. No ray of its family exists at its Node.

**The sink.** Whatever arrives at the body's Node is met by its declared
coupling. Under `"sink"`, every arriving ray, outbound or returning, ends in
the body's exact sink counter for its family in the arrival interval and is
booked on the audit's `absorbed_by_bodies` line per field
(`external_body_totals()`, with the momentum field's components when one is
bound), an `external_body_absorbed` record naming the body, the Port, the
family, the amount and the body's momentum after it. The conservation line
becomes initial + sources = current + dissipated + escaped + annulled +
absorbed_by_bodies at every completed tick, the sources holding what the
bodies released; since `ray-event-audit-v1` (2026-09-17)
`conserved_at_every_completed_tick` is the world ledger's identity, in which
the sink is the `absorbed` line, so it stays true, as under `annul`
([audits](#audits-ray-event-audit-v1)). A wall, a screen and a beam stop are
this default.

**A declared coupling.** Under the name of a declared meeting with outputs
([meetings](#meetings-with-outputs-ray-meeting-conversion-v1)), the body is
the participant that never changes: the rule has one role that selects the
body's family alone and returns it once among its outputs, and the other
roles name the families it meets. Each interval the Node adds one token of
the body's family (amount 1, heading +X, the body's phase, no event) to the
residents, the rule fires over the token and the arriving rays of the
families it names as an ordinary meeting, and the Node strips the token's
output before anything leaves, requiring it back unchanged (amount 1, the
body's phase) or the cycle fails. The event record of the rule's other
outputs therefore counts the token as one quantum on its Port, +X. A family
the rule does not name, and every returning ray, ends in the sink as under
the default. A reversed heading of the arriving ray is a mirror, a split by
a declared table a beam splitter, a phase offset a phase plate; a
polarization read is a polarizer once feature 11 exists.

**Motion by fields only.** The body starts with its declared momentum. A
field ray of a family its `momentum_table` names that ends in its sink
changes its momentum by sign x amount x heading of the arriving ray, an
integer vector (-1: toward the source, which lies opposite the arriving
heading); nothing else moves it, since matter that arrives is absorbed
without a push, and a coupled family is met by the rule, not the table. Its
velocity is its momentum over its amount, kept exactly: every interval each
axis accumulator adds the momentum component, and the body steps one Link
through the Port of the first axis (x before y before z) whose accumulator
has reached a whole amount, subtracting the amount; at most one Link per
interval, never faster than a ray, and a momentum that would exceed the
amount fails the cycle. The step is a departure like a ray's: the body
leaves on the packet of that Port (`external_body_step`, with the arrival
tick), is on the Link for the interval, and the next Node holds all of it
from the arrival tick, meeting every ray that arrives there in the same
interval; a body cannot leave an open world. So a small momentum over a huge
amount moves it rarely and exactly, against an electron it stands still,
and two stars turn each other over long times.

**The audit.** `external_bodies()` lists every body in declaration order
with its Node (the Node it steps to while on a Link, `stepping` true), its
momentum, its accumulators and its sink per family; `external_body_momentum()`
is the bodies' momentum line, the exact sum. The runner records
`external_body: "external-body-v1"`, `external_bodies` (each declaration
with its `positions` per completed tick, `[tick, x, y, z]`, and its final
state), `external_body_totals` and `external_body_momentum`. A world that
declares no `external_bodies` runs byte-identically.

### Audits (`ray-event-audit-v1`)

The rule ([Highlights](HIGHLIGHTS.md) 3.15; [ray-event
model](RAY_EVENT_MODEL.md#6-migration-in-order); issue #169, feature 10):
every declared invariant is exact across every interaction and transfer, and
the world audit is one exact ledger per completed tick for each conserved
readout, amount per family, momentum (three integers) and charge, stated in
[the world ledger](LOCAL_CONSERVATION.md#the-world-ledger-ray-event-audit-v1).
`Simulation.audit()` (`DisturbanceEngine.audit`, built by
`core/ray_event_audit.py`) reads the ledger at the current tick from the
readouts of this document:

- `totals()` and `source_totals()` are the `current` and `sourced` lines of
  every conserved field, `escaped_totals()` and `annulled_totals()` the
  `escaped` and `annulled` lines, and `external_body_totals()` the
  `absorbed` line, what the external bodies' sinks took (`absorbed_by_bodies`,
  [external body](#the-external-body-external-body-v1)), with the momentum
  field's components when one is bound; every ledger also carries the
  bodies' own lines (`bodies`: their count, the exact sum of their momentum
  from `external_body_momentum()`, the sum of their declared charge and
  their sinks per field), beside the identity, since a body's content never
  enters a sum and its momentum is its declared response to the fields it
  absorbs, not a ray's;
- `charge_totals()` reads charge x amount per ray family over the owners
  `totals()` reads: the rays resident at active Nodes and in flight on Links
  and, since this feature, the stock a record holds of the family, resident
  or in transit (a lamp holding a charged quantum holds its charge);
  `escaped_charge_totals()` is the charge x amount of every escaped ray, and
  of stock a record carried out; the charge a family sourced, annulled or
  absorbed is its charge per quantum times that amount;
- a returning ray reads its momentum as its share on the event's heading
  (`ray_momentum`, `detector-return-v1`) and its charge as charge x amount
  like any ray, in every line.

The runner records `ray_event_audit: "ray-event-audit-v1"`, the ledger of
every completed tick under `audit` (so a Renderer's caption can show the
lines tick by tick), and `conserved_at_every_completed_tick` as the ledger's
identity, initial + sourced = current + escaped + annulled + absorbed for
amount, momentum and charge at every completed tick, re-checked from the
recorded integers (`audit_failure`). A `ray_interactions` rule with outputs
whose family's charge differs from the charge of the inputs its amount comes
from would change the total charge, and is rejected at validation. Nothing
else changes: events, states and totals are byte for byte what they were,
the audit adds readouts. `test_ray_event_audit.py`
([expectations](TEST_EXPECTATIONS.md#ray-event-audit)) is the test.

### Binding and gravity by delay (`ray-binding-v1`)

The rule ([Highlights](HIGHLIGHTS.md) 3.4, 3.17 and 3.28; [ray-event
model](RAY_EVENT_MODEL.md#6-migration-in-order), step 8; issue #169,
feature 8): matter is a bound group, binding is the interaction whose result
is zero events, a bound group is unbound by an arriving ray, and gravity is
bending by delay. `test_ray_binding.py`
([expectations](TEST_EXPECTATIONS.md#ray-binding)) is the test.

**Binding.** A `ray_interactions` rule without outputs whose assignments set
`delay` 1 on its participants binds them: the rays stay resident at the Node
as a bound group and the rule fires again every interval. The first firing is
the meeting that forms the group, recorded as every meeting is; each later
firing, on rays the rule already holds, is the group's tick, an event: the
participants are stamped as one event on the Ports of their headings
(`steps` 0, the mask and shares of the group), the Node publishes a
`bound_tick` record (position, families, amounts, phases, `ray_delay`), and
each participant's phase advances once per interval by its family's rest
rate ([wave-ray families](#wave-ray-families-wave-ray-family-v1)), the
group's clock. A rule that holds its participants once and does not fire
again (a guarded bounce) forms no lasting group and publishes no tick. The group is matter: a held ray occupies no line ahead of
it, so it releases its field on all six headings once per interval
(`release_field`, [released field](#field-as-the-rays-information-released-field-v1)),
booked as a source like every release. The Node keeps nothing beyond its
rays: `bound_group` reads the group from them (the outbound rays at their
event Node with no delay or wait pending, which under this admission are
exactly the rays a rule holds there), the snapshot lists `bound_groups`
(position, families, amounts, phases, `ray_delay`) for a Renderer to draw
matter, and the runner records `ray_binding: "ray-binding-v1"` beside
`released_field`. A rule assigning a delay above 1 holds its group and ticks
once per that many intervals; a returned ray resident at its event Node joins
no binding rule before its inverse split.

**Unbinding.** An earlier declared rule with outputs
([meetings with outputs](#meetings-with-outputs-ray-meeting-conversion-v1))
that names a bound participant and an arriving ray fires when such a ray
arrives, in declared order before the binding rule: its outputs replace the
participants and leave the Node as new event rays, and the binding rule, with
its participants gone, no longer fires. Nothing else creates or destroys a
group; a family with no coupling to the group's families crosses it
([layers](#layers-ray-layers-v1)).

**Mass as output-clock delay.** A binding rule may declare `"ray_delay": k`,
the output-clock delay of the Node that holds its group: while the rule
fires there, every ray of a matter family arriving at that Node waits `k`
intervals (`interaction_delay` plus `k` on arrival, its phase moving by its
rate per waiting interval) before it meets anything or departs, so every
departure of matter from the Node is `k` intervals later than it would be.
A field ray (a family with `field_of`) is information, not matter: it is
never delayed by a clock (Highlights 3.5), neither the group's own release,
which leaves every interval, nor a field ray crossing the Node. This one
Node-wide wait approximates the six per-face output clocks of Highlights
3.28 in this slice: one `k` for every face, the register `bound_delay` on
the Node set by the plan of the cycle in which the rule fired and 0 once
the group is unbound. The outputs of the unbinding leave in their own
interval. The world key `ray_delay` of the computation-field hold is a
different rule and is not admitted with ray interactions.

**Gravity as bending by delay.** A coupling of a light ray with the field of a
bound family (`light x G`) is an outputs rule whose light output keeps the
light ray's amount and phase (`heading` `"same"`, `phase` `"same"`) and
declares `"delay": {"of": 1, "table": [t0, t1, t2, t3, t4, t5], "per": u}`:
the delay is the whole quanta of `amount_G x t[p] / u` phase steps, `p` the
Port the field ray came in through (the Port opposite its heading), and the
rule returns the field ray reversed (the recoil). The engine applies the
table; the physics is the table. A delay in phase steps is a delay of the
output-face clock on the side of Port `p` in units of the phase step, the
smallest time (`k_out x delta_t_min` of Highlights 3.28, `delta_t_min` the
interval over the phase modulus N), and the ray carries it as `lag`, one
signed integer per axis toward the lagging side. The fraction the floor
leaves is a fraction of a clock count, not of content; nothing owned is
divided. At every departure after the ray has left its event Node through its
event's Port, a transverse lag that has reached N, one full interval of
delay on that side, is spent as one Link toward the lagging side, the ray's
steps up by one, its phase moved by its rate and its heading and event record
unchanged; a lag on the ray's own axis is spent as one interval of wait. The
side nearer the heavy Node is where its field comes from, so the light ray's
line is delayed more on that side and turns toward the mass over the Nodes
that follow: bending by delay, no formula in the engine. The recoil walks
back along the field ray's line to the group's Node; what it does there is
not declared in this slice (a family with no coupling to G crosses it), so
the momentum the turn moves is booked at the meeting as the meeting's source
of the momentum field, as for any meeting, and `ray_momentum` reads `amount x
heading` alone: the transverse momentum of a lag below N is not read out.
The declared coupling of the recoil to the group (the heavy Node drawn
toward the ray) is open.

```json
{"name": "gravity", "participants": [{"type": "light"}, {"type": "G"}],
 "outputs": [
   {"field": "light", "amount": {"of": 0}, "heading": "same", "phase": "same",
    "delay": {"of": 1, "table": [4, 4, 4, 4, 4, 4], "per": 1}},
   {"field": "G", "amount": {"of": 1}, "heading": "reversed", "input": 1}],
 "invariants": [{"name": "energy", "expression": {"field": "amount"}}]}
```

**G_eff across the phase width.** With the mass of a group in phase units
(the sum of its participants' rest rates, m_0 = 1 phase step per interval)
a fixed fraction of N, the field amount fixed by the content and the table
fixed, the delay in phase steps is the same integer at every N, the shift of
the light's line is that integer over N Links, and G_eff = alpha x b / (4 M)
falls as 1/N^2: the test pins G_eff x N^2 = 64 over N = 2^8, 2^10, 2^12 and
2^16 at b = 4 (hypothesis 14 of [HYPOTHESES.md](HYPOTHESES.md)). The
constancy follows from the delay table acting on the field amount and being
counted in phase steps; a table acting on the rate would give G_eff x N^2
growing with N.

Admission: `ray_delay` on a rule without outputs only, a nonnegative bounded
integer; a delay table on an output of a meeting only, naming one input and
one output, six entries from 0 through `MAX_VALUE` and a unit from 1, the
input's field unit-axial as every selected field is. No draw, no new
arithmetic beyond the table's product and floor; a world without a binding
rule, a `ray_delay` or a delay table runs byte-identically.

### Funded emission and absorption

A field whose emitting type also carries a scalar field of the same name may
emit with `"source": false`: the emitted amount is paid from the record's own
stock, clipped to what it holds, and no external source is recorded. Ray fields
require schema 1 for this; octant fields accept it under both schemas. The
causal source envelope's extension to a delocalized wave was deleted on
2026-09-17 with the shared quantum resource. An optional
`"recoil_field"` names an owned signed vector that loses `amount x heading` for
every emitted ray. The reverse is the `absorb` coupling mode: a record of the
absorbing type takes a share of every ray resident at its Node on the cycle
after arrival (`amount x fraction / fraction_denominator`, or the whole ray),
adds it to its own field of the same name and, with `momentum_field`,
`share x heading` to that vector; the rest of the ray is forwarded. Absorption
happens before forwarding and before this cycle's emission joins the residents,
so a record never swallows its fresh rays; with `self_exclusion` the rays of its
own last departure are left alone by their complete ray key. Absorbers act in
slot order.

A funded emission may carry a `"dissolve": {"after_ticks": N, "over_ticks": K}`
schedule instead of an amount: the record emits nothing for its first `N`
cycles, then the stock it held when the rule first saw it, divided over `K`
cycles and never more than is left. The count and the initial stock are a
record row (`dissolve_clocks`), so the schedule follows the record wherever it
moves. A particle that pays itself out as rays this way is a matter wave in
flight; the matter-wave probe (`examples/matter-wave/`, deleted on 2026-09-17) lands one
on a screen as the fringe of its momentum.

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

The candidate uses immutable cosine/sine tables prepared with the field definition,
before physical stepping. Each table has at most 4096 bounded entries; the two
host preparation caches retain at most 16 tables each. A bounded integer series
uses fixed-point scale 1,000,000,000, checked 64-bit intermediates and at most 32
terms. Physical events read the prepared tuples and never construct trigonometric
tables. Preparation and cache storage are host costs outside NodeState.

A ray field may add `"kerengonen": {"phase_steps": P, "phase_advance": k}`,
with `P` a power of two from 2 to 4096 (the phase width `phase_bits` is log2 `P`;
[wave-ray families](#wave-ray-families-wave-ray-family-v1)) and `0 <= k < P`,
the family's rest rate. Every ray carries a phase step in any case, since every
ray is a wave ray, starting at the emission rule's `kerengonen_phase` (default
0) and advancing by `k` on every link, masked to the width; the key adds the
rate and the coherence table below. Rays merge only when heading, lattice phase
and wave phase all agree. Nothing else about transport changes: a ray still follows one
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
taken. The other choice, `"threshold"`, is the deterministic hidden-variable
rule: the whole ray is taken when its coherent share reaches one half and left
otherwise, so the outcome is fixed by the phases alone. A threshold capture of
a negative ray is left whole when the absorber cannot pay its complete amount;
only the share mode may take a smaller stock-limited amount. Neither capture
draws: an ordinary absorber has no ticket and no seed. The whole-or-nothing
`"lottery"` capture, its `capture_seed`, the absorb rule's `capture_salt` and
the record row `absorb_tickets` were deleted on 2026-09-17 (issue #164, bucket
B.5) under [Highlights](HIGHLIGHTS.md) 3.19: the only draw in the model is at
a Node whose Detector bit is set. The bounded ticket sequence
(`TICKET_MODULUS`, `next_ticket`, `ticket_draw`) stays in
`core/spatial_state.py` as the local draw the
[Detector mark](#detector-mark-detector-mark-v1) owns.

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
momentum, `|p| / D`, supplies a candidate de Broglie relation: a faster beam has a
shorter wavelength within the probe's configured range. The
de Broglie probe (`examples/de-broglie/`, deleted on 2026-09-17) measures the fringe spacing
it gives; this relation is configured, not derived. A ray without its own advance uses the
field's rate. Without the key the field is the plain `isotropic-ray-field-v1`,
a wave-ray family with rest rate 0 and no coherence table, which still admits
a `kerengonen_phase` below its declared width; a `kerengonen_advance` on an
emission requires the key. The runner records the identity
`kerengonen-ray-field-v1`. The [double-slit probe](../examples/kerengonen-double-slit/README.md)
measures the fringe on a line of absorbers.

Self-exclusion carries `(amount, cursor, wave phase, advance)` for the actual
departure cycle and compares heading, lattice accumulators, wave phase and advance.
A distinguishable external phase or advance is not excluded, even if the emitter's
properties have changed since departure. A cycle without emission clears the
previous emission row to four zeros, so the fallback advance sentinel cannot keep
an exhausted source active. A foreign ray never merges with the own key, since
its event differs ([ray state](#ray-state-ray-event-state-v1)); the own ray
of the departure cycle is the only one excluded. Phased or attenuating
self-exclusion alongside response couplings is rejected: subtracting a raw own
amount from a coherent or decayed sample is not the corresponding local
subtraction; the supported combination is absorption. Coherence evaluation is
quadratic in the configured local phase count, bounded relative to world size.

Funded emission and absorption currently require an immediate carrier commit on
the independent fixed field clock. If the local carrier cost requires a delayed
plan, the Node rejects it before publishing that plan. This prevents a later
carrier commit from restoring stock changed by intervening field cycles. The
candidate does not yet arbitrate these two clocks for delayed shared ownership.

Declared component accounting associates ray momentum with the vector explicitly
named by `recoil_field` or absorption's `momentum_field`. All declarations for one
ray field must agree; that vector cannot also own spatial populations. Actual
resident rays, in-flight rays, external injection and completed escape contribute
`amount x heading` to that vector's read-only totals. No field name supplies a
binding, and this accounting never repairs state or replaces the separate local
energy/momentum audit.
momentum, `|p| / D`, is the de Broglie rule: a faster beam has a shorter
wavelength, and the de Broglie probe (`examples/de-broglie/`, deleted on 2026-09-17)
measures the fringe spacing it gives. A ray without its own advance uses the
field's.

A mirror is the same rule turned around. The absorbed row also keeps the
heading of the largest share, and an emission with
`"kerengonen_mirror": "x"` (or `"y"`, `"z"`) sends its whole amount back as
one ray along the mirror image of that heading across the named axis, at the
carried phase and advance when `"kerengonen_phase": "carried"` is set. A
diagonal mirror, `"xy"`, `"xz"` or `"yz"`, swaps the two named components
instead, so a ray along `+x` returns along `+y`. The heading sequence must
contain every mirror image, the emission must name a `recoil_field` (the
mirror takes the momentum it reverses), and the emitting type must absorb on
the field. A mirror whose absorb rule carries a `fraction` is partial: it
returns the fraction it takes and lets the rest pass. A lamp facing a mirror
then holds a standing wave: the reading along the line repeats every
`phase_steps / (2 x advance)` links, as the
mirror probe (`examples/kerengonen-mirror/`, deleted on 2026-09-17) measures.
Without the key the field is the plain `isotropic-ray-field-v1`; a
`kerengonen_advance` on an emission requires the key, and a carried phase or a
`kerengonen_mirror` requires its coherence table. The runner records the
identity `kerengonen-ray-field-v1`. The [double-slit probe](../examples/kerengonen-double-slit/README.md)
measures the fringe on a line of absorbers.

### Euclidean pace (`"metric": "euclidean"`)

A ray field moves every ray one link per tick, so a wave front reaches the
same Manhattan distance in every heading and the fringe of two sources follows
Manhattan path difference. A ray field may instead set `"metric": "euclidean"`
(identity `euclidean-ray-pace-v1` in the run metadata, beside the field's
policy). Every heading then has a pace, the ratio of its Euclidean length to
its Manhattan length scaled by 4096 and computed by integer square root; the
slowest heading (the one nearest a body diagonal) hops every tick, and every
other ray adds that slowest pace to a per-ray `wait` on every tick and hops
only when the wait passes its own pace, carrying the remainder. A ray that
waits stays resident at its Node, counted by the ledger, sampled by readers
and open to absorption like any other, and its phase still advances by one
step for the tick. No ray ever moves faster than one link per tick; the
Euclidean metric only makes rays slower, so that every heading covers the same
Euclidean distance per tick and the front is round to within one link. Rays
merge only with equal wait. Two sources in phase then give a fringe in
Euclidean path difference, and the
Euclidean pace probe (`examples/euclidean-pace/`, deleted on 2026-09-17) measures both.

A ray field may also set `"pace": [n, d]` with `n <= d`: the fastest heading
then hops `n` links every `d` ticks, on either metric, by the same wait. A
pace is never faster than one link per tick; it exists so that a matter wave
can be slower than the signals that chase it.

A funded ray emission may also name `"heading": [x, y, z]`, one of the
field's headings: every ray it emits leaves on that heading instead of
sweeping the sequence, a directed emitter. It cannot be combined with a
mirror, which chooses its heading from what it absorbed.

### Claim and gather (`claim-gather-ray-field-v1`)

Deleted on 2026-09-17 (issue #164, bucket B.5). The ray-field key `claim`, the
emission keys `train_field` and `"train_field": "carried"`, the absorb rule's
`claim`, the ray fields `train` and `homing`, the `Claim` record with its
flood, adoption and expiry, the record row `absorbed_trains` and the runner
identity `claim-gather-ray-field-v1` are gone. Under
[Highlights](HIGHLIGHTS.md) 3.20 and 5.4 a wave is not gathered by a claim
that floods the board: what a Detector returns walks back on the ray itself,
one Link per interval, to the event it came from, and no Node keeps a register
of any kind. The recorded measurements of the deleted rule (the isotropic
gather, the contested gather, the double-slit landing and the gathered-gravity
probe) stay in [validation](VALIDATION.md) as evidence about that rule, not
about the current model.

### Bonded rays (`bonded-ray-field-v1`)

Deleted on 2026-09-17 (issue #164, bucket B.5), with the shared quantum
resource of Highlights 3.18 that it followed. The ray-field key `bond`
(`seed`, `stream`), the emission key `bond_field` (`"origin"` or an owned
scalar), the absorb rule's `bond_setting`, the ray field `bond`, the birth code
`origin_bond`, the world's `BondRegistry` (`fields/bonds.py`), the sampling
profile `historical-autonomous-v1` and the runner identity
`bonded-ray-field-v1` are gone. Under [Highlights](HIGHLIGHTS.md) 5.4 no
registry answers at a distance and pair identity is the trajectory: the first
Detector's bit travels on the returning ray through the birth event to the
partner's line, and the second Detector draws its own bit on that arrival. The
accepted price is that two Detectors at equal distance from the birth draw
independently (CHSH at most 2 for spacelike settings). The recorded CHSH
measurements of the deleted registry stay in [validation](VALIDATION.md) as
evidence about that profile, not about the current model.

## Integrated ray ownership boundaries

Load-delayed rays remain visible to absorption. Surviving residents, fresh
emissions, owned carrier stock and retained pace state commit together, before
observers see the result. Every retained ray and every incoming ray bundle is
validated before it is merged, and the field's `ray_slots` is the only bound on
residency. There is no occupied channel and no capacity rule
([Highlights](HIGHLIGHTS.md) 5.1): rays leaving a Node on one Link in one
interval travel together in one packet, and nothing is pushed back or made to
wait for room. The former refusal to begin a field cycle while a Node's
outgoing Links still held packets was deleted on 2026-09-17; what remains is a
host integrity check at commit, `SpatialNode.require_free_links`, which rejects
a departure that would overwrite a packet still in transit. Delivery clears
every Link before the next field cycle, so that check names a scheduling
error, never a physical rule.

Euclidean pace tables are immutable configuration data prepared before stepping.
Ratios are reduced before physical-register bounds are checked; irreducible terms
outside those bounds fail preflight. There is no growing global pace cache.
Share and threshold capture retain exact rational decisions, and an unfundable
negative whole-ray capture is rejected rather than partially paid.

One-Link self-exclusion reconstructs swept or fixed directed emissions and matches
all ray metadata except amount. Its current departure record does not prove
coarrival for paced, load-delayed or mirrored rays; these
combinations fail preflight. This is still a scoped candidate and cannot identify
otherwise identical waves by an absent source label.

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
instead of being silently ignored. Two explicit opt-in policies change when a
carrier samples relative to its own emission without identifying sources:
[`field_phase_first`](SPATIAL_COUPLINGS.md#field-phase-first-ordering) and
[`arrival_port_blind`](SPATIAL_COUPLINGS.md#arrival-port-blind-sampling).
Optional [spatial couplings](SPATIAL_COUPLINGS.md)
now provide generic exchange and exact discrete rotation with a local opposite
field reaction. Their straight-line flux response has a restricted geometric
self-interaction guarantee; it does not claim general source attribution.
Existing explicit paired-record couplings remain available independently.

A future self filter must provide a bounded local attribution law and pass both
isolated-source and external-source controls. Shadow worlds, source histories
and global isolation checks may be diagnostic references only, never physical
inputs. The transport candidate does not establish a general force law.
