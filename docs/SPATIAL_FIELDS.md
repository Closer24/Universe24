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
the transport of a returning ray and the momentum readout. The event Ports
and the event shares are hidden variables (Highlights 5.4), read by no rule,
coupling, absorber or readout; the Detector bit is a visible property of the
ray since 2026-09-17 ([the bit as a property](#the-detectors-bit-as-a-property-detector-bit-property-v1)).
An existing world runs exactly as before except where rays of different
events used to merge; they no longer do.

The `Ray` record (`core/spatial_state.py`) holds, beside its heading index,
DDA accumulators, amount, wave phase, advance, pace wait and interaction
delay:

| Field | Values | Rule |
| --- | --- | --- |
| `steps` | `0` to `MAX_VALUE` | Links walked since the ray's event: `+1` per Link while outbound, `-1` per Link on the walk back; `0` at the event Node. The count starts at the trajectory's origin event and resets only when the trajectory changes (a new event). A returning ray with no steps left is at its event Node: it stays resident there until the next cycle's inverse split ([below](#inverse-split-inverse-split-v1)); no Link is planned for it and a Link beyond its event Node is refused |
| `outbound` | `1` or `0` | `1` while the ray travels on its event's heading, `0` once it is reversed on its line. Every created ray is outbound; a draw of 0 at a marked Node sets `0` ([Detector return](#detector-return-detector-return-v1)) |
| `event_ports` | six-bit mask | The Ports the event sent to, bit `p` for Port `p` in the order `[+X, -X, +Y, -Y, +Z, -Z]` |
| `event_shares` | six bounded integers | The amount the event sent through each Port, in Port order, `0` where the mask bit is `0`. The record is fixed at six entries rather than a variable list: at most six records, one per Port (Highlights 3.20), and exactly the information of a mask-indexed list. A share is signed where the field is signed, like `amount`; the record stores the integer, not a zigzag code |
| `detector` | `0`, `1` or `2` | No Detector event, a Detector event that drew 0, a Detector event that drew 1. Every emitted ray carries `0`; a marked Node sets `1` or `2` on arrival ([Detector mark](#detector-mark-detector-mark-v1)). A property of the ray like charge (`detector-bit-property-v1`): the outputs of a meeting inherit it, a coupling reads it as the ray property `detector`, and a marked Node reads it ([the bit as a property](#the-detectors-bit-as-a-property-detector-bit-property-v1)) |
| `lag` | three bounded signed integers | The lag of the ray's output-face clocks in phase steps, one per axis, positive toward the +axis Port ([binding](#binding-and-gravity-by-delay-ray-binding-v1)); `(0, 0, 0)` on every created ray, reset by a return |
| `momentum` | `None` or three bounded signed integers | The momentum register ([a free ray turns by momentum](#a-free-ray-turns-by-momentum-ray-momentum-turn-v2)): the ray's momentum, `None` for the default amount x heading of its line, which every created ray carries; set by a push, walked by the DDA in place of the heading, cleared when a push brings it back to the default, negated by a return with the heading, part of the merge identity and, being extensive, summed when rays merge |
| `polarization` | `-1` or `0` to 2^`polarization_bits` - 1 | The polarization ([polarization](#polarization-ray-polarization-v1)): a transverse direction modulo a half turn in steps of the family's polarization circle, or `-1` for none, which every created ray carries unless its emission declares one; part of the merge identity, kept by the return, the inverse split, a push and a spread (as the axial mean), read by the polarizer and by a coupling's guard |

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
event Ports, event shares, Detector bit, momentum register and polarization. Rays of different events never
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
| `on_bit_1` | `"pass"` (default) or `"draw"` | What the mark does with a ray carrying bit 1 ([the bit as a property](#the-detectors-bit-as-a-property-detector-bit-property-v1)): passes it without a draw, or draws as for a ray carrying no bit. Optional |
| `on_bit_0` | `"pass"` (default) or `"draw"` | The same for a ray carrying bit 0, a transmission. Optional |
| `on_click` | `"absorb"` or `"pass"` for every ray family, or a mapping of ray family name to one of them | What the mark does with a ray that draws 1 ([a click is an absorption](#a-click-is-an-absorption-detector-absorb-v1)): absorbs it into the mark's counter, or passes it with the bit 1. A family not named keeps the default, absorb for a field family (one declared `field_of`) and pass for matter. Optional |

The first three keys are required, the three couplings are optional, and no
other key is accepted. The parsed
`DetectorMark(position, pass_numerator, pass_denominator, seed, on_bit_1,
on_bit_0, bit_keys, on_click, click_keys, counter, momentum)` records are
`InitialState.detectors` (the bit couplings as `BIT_PASS` 0 or `BIT_DRAW` 1,
`bit_keys` 1 when the file wrote either; `on_click` as `CLICK_PASS` 0,
`CLICK_ABSORB` 1 or `CLICK_DEFAULT` -1 per spatial field, empty for all
defaults, `click_keys` 1 when the file wrote it; `counter` and `momentum`, the
mark's exact count per spatial field and the momentum of what it absorbed,
empty and zero at the start); the engine installs each on its Node as
`SpatialNodeState.detector` with `detector_ticket` seeded from `seed`. A
document with marks is admitted only under the shared Detector admission:
`schema_version` 1, `link_ticks` 1, at least one ray field, every ray field on
`"metric": "links"` with pace `1 / 1`, no decay and unit-axial headings closed
under negation, without `node_execution` or `spatial_computation_delay`.

On arrival each ray carrying no bit (and each ray carrying a bit whose
coupling is `draw`) draws one bit from the mark's stream, in Port then
merge-key order, and leaves with its `detector` field set: `2` on 1, with a
`detector_click` event (position, tick, Port, family, amount, bit 1), the ray
continuing unchanged when the mark's `on_click` for its family is `pass`, the
default for matter, or absorbed into the mark's counter when it is `absorb`,
the default for a field family, the click then carrying `absorbed`
([a click is an absorption](#a-click-is-an-absorption-detector-absorb-v1));
`1` on 0, the ray returned on its line
([Detector return](#detector-return-detector-return-v1)) with a
`detector_return` event and no click. A ray carrying a bit whose coupling is
`pass`, the default, is read and not drawn: it continues unchanged with a
`detector_pass` event ([the bit as a property](#the-detectors-bit-as-a-property-detector-bit-property-v1)).
A document without `detectors` has no marked Node and runs exactly as
before, and the runner records `detector_mark: "detector-mark-v1"`.

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
  nothing (a returning ray is not an arrival; `detector-bit-property-v1`
  reads the bit of arrivals only);
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

### The Detector's bit as a property (`detector-bit-property-v1`)

The rule ([Highlights](HIGHLIGHTS.md) 3.20 and 5.4 "The Detector's bit is a
property of the ray", model owner, 2026-09-17; [ray-event
model](RAY_EVENT_MODEL.md#6-migration-in-order), feature 2b under step 3;
issue #169): the bit a marked Node set on a ray, 1 for PASS and 0 for
RETURN, travels with the ray as a property like charge, visible to every
meeting, to the record and to the rendering; it propagates, so the
descendants of a realized ray are known to be realized and the descendants
of a transmission are known to carry a return; and a Detector reads it. The
statement of the rule at the mark is in [Detector-owned
sampling](DETECTOR_SAMPLING.md#the-bit-read-detector-bit-property-v1); this
section is the schema and what the code does. Three things, and nothing
else, changed on 2026-09-17:

**Inheritance.** `stamp_event(rays, headings, detector)` stamps the bit the
event's outputs carry: `DETECTOR_NONE` for an emission (a lamp, a release, a
restored share emitted again), the returned ray's bit for an inverse split
(as before), and for a meeting the bit `inherited_bit(bits, rule)` hands
down from the inputs. Every group that fires in `apply_ray_interactions`,
a rule with `outputs` and a rule with assignments alike, stamps its outputs
with it: by default the highest bit among the inputs in the order 1 over 0
over none (`DETECTOR_BIT_1` 2 over `DETECTOR_BIT_0` 1 over `DETECTOR_NONE`
0, the stored order), unless the rule declares `bit`:

```json
{"name": "meeting", "participants": [{"type": "a"}, {"type": "a"}],
 "bit": "none",
 "outputs": [...], "invariants": [...]}
```

| `bit` | The outputs carry |
| --- | --- |
| `"highest"` (default) | The highest bit among the inputs, 1 over 0 over none |
| `"none"` | No bit |
| `{"of": i}` | The bit of input i, one of the rule's roles |

Any other value, or an index beyond the roles, is rejected before a world
exists. A meeting of a marked ray with an unmarked ray therefore sends both
outputs on with the bit (a realized ray's meeting products are realized; a
transmission's are transmissions); an external body's coupled token
(`external-body-v1`) inherits it too and is stripped as before. A field ray
released by a marked ray carries no bit, since a release is an emission and
a field ray carries no event.

**Visibility.** `RAY_PROPERTIES`, the view of a ray in a [ray
interaction](SHARED_RAY_COUPLING.md), gains the read-only property
`detector`, the bit as the engine stores it: `0` none, `1` a draw of 0, `2`
a draw of 1. A `when` guard or an invariant reads it as it reads `charge`
(`{"field": "detector", "participant": 0}`); an assignment to it is refused
as read-only, and a meeting's outputs carry the inherited bit whatever the
view of the outputs says of it. A world with ray interactions reads one
more view component per participant (`read` cost 10 instead of 9), as
`wave-ray-family-v1` added two; a world without is unchanged.

**The marked Node reads the bit.** In `SpatialNode.receive`, before the
draw, each arriving ray is read: a ray carrying 1 under `on_bit_1: "pass"`
(the default) passes without a draw, unchanged, and a ray carrying 0 under
`on_bit_0: "pass"` (the default) is a transmission and passes without a
draw, unchanged; a `detector_pass` event (position, tick, the Port the ray
came in through, family, amount, `bit` 1 or 0, the bit it carries) records
each such pass, after the interval's clicks and before its returns, and the
mark's ticket stream does not move. Under `"draw"` the ray is drawn exactly
as a ray carrying no bit (`detector-mark-v1`), its bit set by that draw: a
mark that declares both keys `"draw"` behaves as every mark did before
2026-09-17. Only a ray carrying no bit is always drawn. A ray on its walk
back is not an arrival and is never drawn nor recorded, as before
([Detector return](#detector-return-detector-return-v1)); a ray arriving at
its event Node performs the inverse split undrawn; what a marked Node emits
or transmits is not an arrival and is not drawn.

**Identity and the record.** The runner records `detector_bit_property:
"detector-bit-property-v1"` in `run.json` when the world declares the rule
anywhere (a mark that writes `on_bit_1` or `on_bit_0`, a ray interaction
that writes `bit`); a world that declares neither runs the same rule with
its defaults and its record is what it was, byte for byte, unless a marked
ray reaches a second mark (a `detector_pass` line, no draw) or meets another
ray (the outputs carry the bit). The viewer
([`tools/ray_viewer/extract.py`](../tools/ray_viewer/README.md)) reads
`detector_pass` as the event kind `pass`, a marker listed in the captions
like a click, and carries each ray's `bit` (`null`, 0 or 1) in `runs.json`.
`test_detector_bit_property.py`
([expectations](TEST_EXPECTATIONS.md#detector-bit-as-a-property)) is the
test.

### A click is an absorption (`detector-absorb-v1`)

The rule ([Highlights](HIGHLIGHTS.md) 5.4 "A click is an absorption", model
owner, 2026-09-18; [ray-event model](RAY_EVENT_MODEL.md#6-migration-in-order),
feature 2c under step 3; issue #169): the field quantum a marked Node
realizes ends there. On a draw of 1 the arriving content of a field family is
absorbed into the mark's exact counter, per family, booked on the audit as
absorbed by marks with its momentum on the marks' line, and nothing of it
spreads on: a photon is detected by being absorbed, and every measurement is
paid (3.14). A draw of 0 stays the return (`detector-return-v1`), a ray
carrying 1 still passes without a draw (`detector-bit-property-v1`), and
matter that draws 1 passes with the bit 1 as before, so the electron seen
carries its mark. The statement of the rule at the mark is in [Detector-owned
sampling](DETECTOR_SAMPLING.md#the-click-absorbs-detector-absorb-v1); this
section is the engine's notion of a field family, the schema and what the
code does.

**A field family, in the engine's terms.** A field family is a family declared
`field_of` another ([released field](#field-as-the-rays-information-released-field-v1),
`SpatialFieldDefinition.field_of`; `field_family`): its rays are the eventless
field rays a release and a spread make, and light and the field of a charge
are one such family (3.5). Every other family is matter to a click. That is
the whole of the default, and it is a declaration of the family, not a reading
of the ray: `light` declared `field_of` `electron` absorbs on a click and
`electron` passes; a lone family with rest rate 0 and no charge that no family
declares as its field is matter to a click until its world writes `on_click`.

**The coupling.** How a mark meets each family on a click is its declared
coupling in the catalog (`apparatus.detector.couplings.on_click` of
`catalog/nature.json`), a table entry and not an engine mechanism (3.26): the
mark's `detectors[]` entry writes `on_click` as `"absorb"` or `"pass"` for
every ray family, or as a mapping of ray family name to one of them, and a
family not named keeps the default, absorb for a field family and pass for
matter (`click_coupling`, reading the mark's `on_click` per spatial field
index, `CLICK_ABSORB`, `CLICK_PASS` or `CLICK_DEFAULT`). So a screen that
stops electrons (`{"electron": "absorb"}`) and a counter that lets light
through (`{"light": "pass"}`) are catalog entries. Any other value, an unknown
family or a family that is no ray field is rejected before a world exists.

**The absorption.** In `SpatialNode._draw_arrivals`, a ray that draws 1 under
`absorb` is not among the arrivals the Node keeps: `detector_absorb` adds its
amount to the mark's counter for its spatial field (`DetectorMark.counter`,
one exact entry per spatial field, sized on the first absorption) and its
momentum, amount x heading or the register where a push set one
(`ray_momentum_vector`, taken whole), to the mark's momentum
(`DetectorMark.momentum`), bounded Node metadata like a body's sink, no rays
and no history; the `detector_click` event (position, tick, Port, family,
amount, bit 1) carries `absorbed`, the amount, and only then. Nothing of the
quantum is delivered: it enters no Port reading, no resident ray, no meeting
and no spread register, so the field a marked Node re-releases never carries
the bit of what was realized, since what was realized is no longer there to
spread. Under `pass` the ray leaves with its bit 1 exactly as before
(`detector-mark-v1`) and the click is what it was. The reception record
(`spatial_received`) carries `absorbed_by_mark`, per family the amount and
the momentum absorbed in that interval, only when something was, and the
local audit reads it before it checks the Node, since the clicks follow the
record.

**The ledger.** The Node books what its mark absorbed through
`SpatialAccounting.record_absorbed_by_marks` into
`SpatialEngine.absorbed_by_marks`, per field with the momentum field's
components when one is bound, read by `detector_mark_totals()`, by the
spatial accounting (`absorbed_by_marks`, subtracted like `absorbed_by_bodies`)
and by the world ledger, whose every line gains `absorbed_by_marks`: initial +
sourced = current + escaped + annulled + absorbed + absorbed_by_marks at every
completed tick for amount, momentum and charge (charge x the absorbed amount),
and the runner's conservation line reads initial + sources = current +
dissipated + escaped + annulled + absorbed_by_bodies + absorbed_by_marks
([the world ledger](LOCAL_CONSERVATION.md#the-world-ledger-ray-event-audit-v1)).
`detector_marks()` lists every mark in declaration order with its Node, its
counter per family and its momentum, `detector_mark_momentum()` is the marks'
momentum line, the exact sum, and every ledger carries the marks' own lines
(`marks`: count, momentum, counters) beside the bodies'. Since the momentum a
mark takes is on its own line, the momentum ledger stays exact whether or not
the family binds a momentum field: `light` of E9 binds none, and its 265
absorbed quanta read (218, 0, -27) on the marks' line.

**Identity and the record.** The runner records `detector_absorb:
"detector-absorb-v1"`, `detector_marks`, `detector_mark_totals` and
`detector_mark_momentum` in `run.json`, and the marks' lines in every ledger
under `audit`. A world without marks, or with marks that only ever draw 0 or
meet rays carrying a bit, runs byte-identically in its events and states (its
`run.json` gains the identity and the zero lines); where a field ray clicks
the record changes, and the pins of `test_ray_viewer.py` and
`test_screen_loop.py` were rewritten on 2026-09-18
([expectations](TEST_EXPECTATIONS.md#ray-viewer-extraction), [the screen with
a loop](TEST_EXPECTATIONS.md#the-screen-with-a-loop)). In [the dense
mode](#the-dense-mode-dense-field-v1) a mark is the engine's Node, so the
absorption happens in the engine's delivery, and a dense world with a counting
mark gives the same `state.json`, ledger and marks as the engine alone
(`test_dense_field.py`, the `counter` case). The viewer
([`tools/ray_viewer/extract.py`](../tools/ray_viewer/README.md)) ends the ray
at the mark on a click that absorbed ("Detector PASS, absorbed", the
`absorbed` amount on the marker and on each `eye.clicks` entry), gives the
transit into the mark the amount the receiver's reading leaves out, takes what
the sinks took off `in_world`, and counts `eye.counts`, the absorbed amount
per marked Node, a screen's intensity. `test_detector_absorb.py`
([expectations](TEST_EXPECTATIONS.md#a-click-is-an-absorption)) is the test;
E9 was repeated under the rule on 2026-09-18
([E9](EXPERIMENTS.md#e9-the-screen-with-a-loop-source-the-ring-radiating-on-seven-marks)):
a screen that absorbs counts, 265 clicks in 240 ticks and no pass, its count
growing to the last tick.

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
leave through, `event_shares` the amount per Port, `detector` the bit the
inputs hand down ([the bit as a property](#the-detectors-bit-as-a-property-detector-bit-property-v1)),
so outputs on distinct Ports are distinct events in the record and two
outputs on one Port are one share; nothing is left at the Node. A rule with
outputs declares no `assignments`: it assigns through its outputs.

| Key | Contract |
| --- | --- |
| `field` | The output's family, a ray field; the layers derivation puts a rule's output fields in its layer |
| `amount` | An integer of at least 1; `{"of": i}`, input i's amount; `{"of": "sum"}`, the sum over the inputs; a split by a table (below); `{"rest_of": j}`, the rest of the content that output j's table splits |
| `heading` | A Port index 0 to 5 (the unit-axial heading in Port order, which the field's heading table must contain), `"same"` (the source input's heading) or `"reversed"` (its negation) |
| `phase` | Optional, default `"same"`, the source input's phase; an integer offset k below the phase modulus, the source input's phase plus k; `{"of": i, "offset": k}`, input i's phase plus k; read modulo the field's phase steps |
| `delay` | Optional nonnegative interaction delay, default 0: an output-clock wait, the output stays at the Node that many intervals, met by nothing there, and leaves ([binding as a loop](#binding-as-a-loop-loop-binding-v1)); or `{"of": i, "table": [six], "per": u}`, a delay by a declared table per the Port input i came through ([gravity by delay](#binding-and-gravity-by-delay-ray-binding-v1)) |
| `input` | Optional source input index, default 0: the input whose heading and phase the output reads by default; every output carries its source input's advance |

The rule's optional `bit` (`"highest"`, the default, `"none"` or `{"of": i}`)
says which Detector bit every output carries
([the bit as a property](#the-detectors-bit-as-a-property-detector-bit-property-v1)).

The rule's `invariants` are per-ray readouts (`{"field": "amount"}`,
`{"op": "mul", "args": [{"field": "amount"}, {"field": "heading"}]}`) summed
over the inputs and over the outputs and compared exactly, as the
[N-to-M conversion](LOCAL_CONVERSIONS.md#n-to-m-family-conversion) of records
did until bucket B.6 deleted it on 2026-09-17; the total amount and the stock of every family (the sum of the amounts
of one field over the inputs equals the sum over its outputs) are checked
without a declaration, so no family total changes and the spatial
accounting's `rule_delta` is zero (a rule that declares `draw` is the one
exception: its outputs may change family, the total amount still exact,
[a decaying group draws](#a-decaying-group-draws-decay-draw-v1)). Every
output is a ray of its `field` with
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
`{"of": "sum", "index": "phase_difference"}` (the table is the family's, written
from its phase width, never declared: phase-spread-v1, 2026-09-18; `of`
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
accumulators (0, 0, 0) and pace wait 0. No draw anywhere unless the rule
declares `draw`, the decay setting of a conversion, and then the meeting
draws once from the Node's ticket stream and fires on 1 only, and its
outputs may be of other families with the change booked as each family's
source ([a decaying group draws](#a-decaying-group-draws-decay-draw-v1),
2026-09-17); the Detector (feature 2) is not touched, and its bit is
inherited (feature 2b); a family with no rule crosses
([layers](#layers-ray-layers-v1)); existing worlds with single-output rules
run byte-identically, and the runner records
`ray_meeting: "ray-meeting-conversion-v1"` beside `ray_layers`.

```json
{"name": "split", "participants": [{"type": "a"}, {"type": "a"}],
 "outputs": [
   {"field": "a", "amount": {"of": "sum", "index": "phase_difference"}, "heading": 2},
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
field, and `charge`, the family's charge per quantum (and, since
`detector-bit-property-v1`, a third, `detector`; since
`ray-polarization-v1`, a fourth, `polarization`). Charge is per quantum
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
participant (`read` cost 9 instead of 7; 10 since `detector-bit-property-v1`)
and is otherwise identical. The runner
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
(0 delivers the phase unchanged, as light does); the sign of the source's
charge is a planned property of the released ray (feature 12, Highlights
3.5, 2026-09-17), never encoded in its phase. The fraction the floor leaves
is not released: the field is a description booked as a source, so
nothing owned is destroyed and no remainder needs an owner (Highlights
3.17); a release whose floor is 0 releases nothing. The released rays leave
in the same interval as the F ray, with the residents; the release is a
departure, not an arrival, so it is no meeting. A ray of a family that has a
meeting rule releases after the interval's meetings, from the trajectory
that departs. The release does not wait for the clock (Highlights 3.5,
model owner, 2026-09-17): a field release is information, not a departure
of matter, so a ray waiting at a Node under a declared `delay` is content
resident there and releases every interval it is there, on the five
headings other than its own like any ray, while the clock delays only its
departure as matter; this slice releases from the departure, which at pace
1/1 with no delay is every interval. The six-heading release of a held ray,
which existed only because a held ray occupied no line ahead of it, went
with the held form on 2026-09-17
([binding as a loop](#binding-as-a-loop-loop-binding-v1)). A G ray crosses
Nodes like any ray and releases nothing: a
field has no field, and the density of the field falls by the geometry of the
lattice alone. Without `spread` a G ray therefore stays on its line and the
field of a source lives on the six axis lines of the Nodes it crosses; with
it, feature 12, field spreading (Highlights 3.5, model owner, 2026-09-17;
[field spreading](#field-spreading-field-spreading-v1)), every Node that
field content reaches releases it again by the family's declared split
table, and light, the field of a charge, is one such family. A G ray that
reaches an open boundary escapes like any ray.
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
the default, `"polarizer"` with its `polarizer` declaration
([polarization](#polarization-ray-polarization-v1)), or the name of a
declared ray interaction) and
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
absorbed_by_bodies at every completed tick (plus absorbed_by_marks since
`detector-absorb-v1`, 2026-09-18), the sources holding what the bodies released; since `ray-event-audit-v1` (2026-09-17)
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
polarization read is a polarizer, the body's third coupling value,
`"polarizer"`, declared on the body and not as a rule (feature 11,
[polarization](#polarization-ray-polarization-v1)).

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

### Field spreading (`field-spreading-v1`)

Retired for shadows on 2026-09-18 by `node-mixing-v1` (Highlights 5.4, point
24; [the Node mixes the six](#the-node-mixes-the-six-node-mixing-v1)): the
split table is no longer declared and a shadow spreads by the Node's mixing;
the Node-owned remainder of `field-remainder-v1` stays, in ninths. The
description below is kept for the record of what the table was.


The rule ([Highlights](HIGHLIGHTS.md) 3.5, "Light is the field, and the
field spreads", 3.17, 3.20 and 3.23; [ray-event
model](RAY_EVENT_MODEL.md#6-migration-in-order), feature 12; model owner,
2026-09-17): light and the field of a charge are one family, and because
light spreads, the field spreads by the same rule: every Node that field
content reaches releases it again in all six headings by a declared split
table, Huygens' principle in the lattice's language, one catalog entry of the
family and not an engine mechanism. A ray family declares it with `spread`:

```json
{"field": "light", "baseline": 0, "transport": "ray", "headings": [[1, 0, 0], ...],
 "rays_per_tick": 1, "ray_slots": 16, "spread": [6, 1, 1, 1, 1, 1],
 "kerengonen": {"phase_steps": 8, "phase_advance": 0}}
```

**The table.** `spread` is six nonnegative integer weights in Port order
relative to the arriving heading: forward (the heading the content arrived
on), backward (its reverse) and the four transverse Port headings in Port
order (for content arriving on +X or -X: +Y, -Y, +Z, -Z; on +Y or -Y: +X,
-X, +Z, -Z; on +Z or -Z: +X, -X, +Y, -Y); the denominator is their sum, as
for `octant_weights`. The backward weight must be positive: a forward-only
split piles the field on the diagonals and empties the axes (Highlights
3.5). The four transverse weights must be equal: the lattice has no
preferred transverse direction (Highlights 3.23), so the momentum a spread
moves lies on the arriving axis up to the remainder. The total is a bounded
integer.

**The step.** In every interval, after the marks of step 2 (a Detector's
draw, a body's sink or coupling) and the meetings of step 3 (Highlights 5.2)
and before the departures, the spatial law takes off the Node the content of
the family that arrived this interval and is due to leave: the outbound rays
with at least one Link walked and no delay or wait pending. A fresh ray at
its event Node (an emission, a meeting's output, the recoil, a transmission)
and a fresh release depart on their line and spread from the next Node; a
returning ray walks back and is not spread; a held ray is not due. What a
Detector returned, a mark absorbed on a click (`detector-absorb-v1`) or a body
took follows those rules first, and only the rest spreads. Nothing of the taken content is forwarded as it came, and
nothing stays at the Node.

**The combination.** Field rays carry no event, so the content combines
before it spreads (Highlights 3.20): amounts add per arriving heading,
content on one line being one content; the phase of the whole is one phase,
the phase step nearest the direction of the coherent sum of amount x
e^(i phase) over every taken ray (`phase_of_sum`, the coherence rule and its
cosine table; a cancelled sum gives step 0); the Detector bit of the whole is
the catalog default of Highlights 5.4, 1 outranks 0 outranks none. The
amount is exact: the coherence of the arrivals (`coherence`, the ratio a
reader or an absorber sees) is recorded and never applied to the amount,
since nothing but a sink ends a quantum.

**The split and the remainder (`field-remainder-v1`; Highlights 3.5 and
3.17, model owner, 2026-09-17; feature 12b).** Each arriving heading's
content A is shared over the six relative headings: the whole quanta
floor(A x w_i / S), S the table's total, leave through heading i, and the
share below one quantum, A x w_i mod S in units of 1/S, is the Node's. It
goes to the Node's remainder register of that family, source sign and
Port (eighteen registers per spreading family, sign-major -1, 0, 1 then
Port, `SpatialNodeState.remainders`, with a phase each,
`remainder_phases`), and the register's phase becomes the phase of the
coherent sum of what it held at its phase and the share at the spread's
phase (`phase_of_sum` over the two, weighted by their amounts in 1/S; an
empty register takes the share's phase; a family without a phase width
keeps 0). Then every register that has reached S releases the whole quanta
it holds, k for kS, through its Port in the same interval, with the
register's phase and its sign, as a departure like the others, and keeps
the rest, its phase reset to 0 when it empties. So a quantum of amount 1
does not turn: it fills the forward register by 6/11 and each other one by
1/11 per arrival; the second arrival releases a quantum forward, the
eleventh releases one through every heading, and a weak field reaches
every Node in the end, a quantum waiting at a Node for that while the front
of a strong field moves at the causal speed; the average intensities follow
the table exactly and the wave shows in them. Since the weights sum to S,
one spread adds a multiple of S to a Node's registers of a family and a
release takes a multiple of S, so a Node's registers of a family always
hold whole quanta in total (`remainder_stock`), and the record's `stored`
is that gain net of the releases. A Node with a nonzero register is active
until it is empty: it cycles every interval as a Node holding a ray does,
and the registers are read and written by the planner as plain bounded
integers of the Node state contract, part of the plan-reuse key. The model
owner chose this on 2026-09-17 over the phase-selected heading
`field-spreading-v1` first implemented (the remainder leaving whole through
the entry the phase selects, so that a quantum never waited), which the
screen run (E6) showed sends a single quantum along one fixed line and
leaves every Node off the axis dark. Departures on one Port merge. Each
departure is a fresh field ray: the Port's heading, accumulators (0, 0, 0),
the combined phase (a register's release, the register's), the family's
rate, no wait, no delay, no lag, `steps` 0, `outbound` 1, no event (mask 0,
shares all zero), the combined bit of this interval's arrivals and its
source sign; it walks one Link with this interval's residents and is spread
again at the next Node.

**The booking.** The total is exact, so the amount has no source and the
world ledger of feature 10 is unchanged by a spread. The registers are
current content (`field-remainder-v1`): the ledger's `current` line
(`totals`, `charge_totals`) counts a Node's registers of a family as their
sum over S, whole quanta exactly by the paragraph above, with the family's
charge and no momentum, a share in a register having none until it leaves;
`sourced`, `escaped`, `annulled` and `absorbed` are untouched by them, so
initial + sourced = current + escaped + annulled + absorbed holds at every
completed tick with a register's content on the `current` line until a
release moves it onto a ray. A register never escapes: content leaves a
register only by a release, and only the released quantum walks a Link, so
the open boundary sees rays alone. A spread changes the momentum of field
content, amount x heading: a ray heading +X becomes six rays, and the
difference, amount x heading summed over the departures (the registers'
releases included) less the same sum over what arrived, is booked as an
explicitly accounted source of the family's momentum field when one is
bound (Highlights 3.15), exactly as the release of feature 7 and the table
split of feature 6 are booked; `source_totals` and the per-tick
`source_delta` name it, and `conserved_at_every_completed_tick` stays the
ledger's identity. The local audit (`diagnostics/local_conservation.py`)
measures the departures as it measures a release, a source at the Node,
measures the registers as content of the family at the Node before and
after the step, and reads the `field_spread` record to give back what the
Node itself held and the whole quanta its registers gained (`stored`), so
its `sourced` line gains the momentum difference and nothing else
([local conservation](LOCAL_CONSERVATION.md#the-world-ledger-ray-event-audit-v1)).

**The record.** One `field_spread` record per Node, interval and family:
`family`, `amount` (what was taken), `arrived` (the amount per arriving
heading, six entries by the heading's Port index), `amounts` (the departure
per Port, the registers' releases included), `released` (the quanta the
registers released per Port), `stored` (the whole quanta the registers
gained net of the releases, negative when the releases exceed the gain),
`registers` and `register_phases` (the Node's eighteen registers of the
family and their phases after the step, sign-major -1, 0, 1 then Port, in
units of 1/S), `phase` (the combined phase), `coherence` (the reduced ratio
of the arrivals' coherence) and `signs` (the source signs taken). It is
published before the interval's `spatial_cycle` record, like
`inverse_split`. `FieldSpread` (`core/spatial_state.py`) is the plan's
record, registered in the Node state contract; `spread_content` is the pure
function (the departures, the record, the registers and their phases after
the step), `relative_ports` the relative Port order, `remainder_slot`,
`blank_remainders`, `validate_remainders` and `remainder_stock` the
registers' helpers. The snapshot (`state.json`, the viewer's frames) lists
every nonzero block as `field_remainders` (`position`, `family`, `sign`,
six `registers`, six `phases`, `total`) when a family spreads, and the
inventory view carries `InventoryNode.remainders`.

**The sign of the source (Highlights 3.5, the field is matter's message
about itself; model owner, 2026-09-17).** The sign of the source's charge
travels on the field ray as a visible property, like the Detector bit and
never encoded in the phase, which is reserved for interference: `Ray` carries
`source_sign`, -1, 0 or 1, set at the release from the releasing family's
charge (`release_field`, `release_stock`; a body's release from its declared
`charge`, `body_release`), 0 on an emission and on every existing world's
ray, part of the merge identity, so content of opposite signs at one Node
stays two rays of the same family, kept by the return and copied by the
inverse split (`transmit`), carried by a meeting's output from the first
input of its own family (the recoil keeps its field's sign) and through the
spread: the content of one Node combines by phase as content does, and each
sign's content is split and placed on its own, the departures carrying
their sign and the record its `signs`. The engine reads it nowhere; a
coupling reads it as it reads the Detector bit, with the catalog read of
feature 2b, and the attraction of opposite charges (the catalog's
`opposite_charge` entry of `electron_field_turn`, experiment A5) closes with
it.

**A returned field quantum (the orchestrator's proposal of Highlights 5.5,
pending the model owner's decision).** A returning ray retraces its line by
its step count; once the field spreads, a field quantum's path is no longer
one line and a field ray has no event at which to perform an inverse split.
The proposal, implemented exactly and stated as such until the model owner
decides it: a field quantum of a spreading family that a Detector returns
with 0 (`outbound` 0, no event) reverses on the line it arrived by and walks
back one Link per interval, its steps counting down to 0 and staying 0, past
the Node that spread it, with no inverse split, until it is absorbed by the
first content its coupling responds to or reaches its source. At every Node
it reaches, before the spread of that interval: if the record that emitted
the family is there (the funded emission's input), it is restored to that
record's stock with its recoil, exactly as the inverse split restores a
share; else if content of the family this field is the field of is there (a
record holding its stock, a resident ray of it) or a resident ray of a family
a declared `ray_interactions` rule couples with this one, it ends there and
its release is unbooked, a negative source of the family and of its momentum
field; an external body takes it into its sink as it takes every returning
ray; otherwise it walks on, and through an open boundary it escapes like any
ray. Nothing is created and every audit stays exact. One `field_returned`
record per quantum that ends (`family`, `amount`, `port`, the Port index of
the heading it walked on, `by`, the family that took it or none for the
emitter, `restored`), published before the cycle's record; the local audit
gives back what an unbooked quantum took off its Node, as it does for a
spread. A world without `spread` keeps the return of feature 3 and the
inverse split of feature 4 unchanged.

**Consequences, none inserted.** With the released field of feature 7
declared with `spread`, a charge's field fills the board: five rays per Node
crossed, each spread again at the next Node, whole quanta released where
the registers fill and the shares below one quantum waiting in them, a Node
with a register cycling until it empties (feature 12b). A recoil, the reversed output of a meeting, departs on its line and
spreads from the next Node like every field content: what walks back toward
the source is the net momentum of the spread, forward less backward on the
line, not one whole ray; a world that wants the recoil whole declares no
`spread`. Field content that meets a ray whose coupling responds is met
before it spreads, so the rule of feature 7 and the sink of feature 7b act on
what arrived. The cost is measured before adoption
([performance](PERFORMANCE.md#plan-compiling-the-catalog-into-transition-tables)).

Admission: `spread` requires ray transport, a positive, conserved, unpaced
unit-axial ray field on the links metric with the six Port headings, zero
baseline, no decay and no self-exclusion (the geometry of a released field),
a phase width of at most twelve bits (the coherent sum uses the family's
coherence table, or the table of its modulus when none is declared), and
the shared Detector admission
(schema 1, `link_ticks` 1, the default fixed clock, no field rules, spatial
interactions or couplings on the family); a table of another length, a
negative weight, a zero backward weight or unequal transverse weights is
rejected at initialization. The runner records `field_spreading:
"field-spreading-v1"`, `field_remainder: "field-remainder-v1"` and
`spreading_fields` (each family with its table) only when a family declares
`spread`; a world that declares none runs byte-identically, records
included. `test_field_spreading.py`
([expectations](TEST_EXPECTATIONS.md#field-spreading-deleted-on-2026-09-18)) was the test.

### The dense mode (`dense-field-v1`)

A host scheduling choice (performance, 2026-09-17), not a rule: with
`dense_field: true` in the world, the
pure-field Nodes of the board, those holding nothing but outbound content of
spreading families and their remainder registers, are cycled by the host as
one vectorized step over integer arrays (`event_universe/dense_field.py`,
numpy int64, outside the core; the engine schedules around it through the
`DenseRegion` protocol of `core/spatial_engine.py`) that applies this rule to
every such Node at once with the same integers: the split of each arriving
heading's content in whole quanta and shares, the registers per sign and Port
with their phases combined by the coherence rule in the engine's order, the
releases at one quantum, the departures walking one Link with the family's
rate, the open boundary's escapes per family and sign, the Detector bit of the
whole on every departure. A Node holding anything else (a Detector mark, an
external body, a record, a ray of another family, a returning ray, an
event-carrying ray) is the engine's, and ownership is decided at every
delivery for the Nodes that receive something: a ray leaving a dense Node
toward an engine Node is handed over as an ordinary packet of merged rays, a
packet leaving an engine Node into the region is absorbed into its arrays,
and the registers move with the Node. The region's Nodes read back as Node
state for the totals, the snapshot and the inventory view, so the world ledger
and `state.json` are byte for byte the engine's ([measured before
adoption](PERFORMANCE.md#the-dense-mode-measured-before-adoption-2026-09-17));
a dense Node publishes no per-Node event (no `field_spread`, no
`spatial_cycle`, no `spatial_escaped` of its own), the record of a dense
region being its totals per tick, so the mode is not for records that need
per-Node field events. The prototype admits a world with a spreading family
whose spatial fields are all ray fields, without the local conservation audit
(`conservation`, which reads per-Node events), without polarization and
without a ray interaction two of whose participants can be spreading families
(a coupling on field rays inside the region), one Node worker; the runner's
`--dense-field` flag is the same switch, and the run record carries
`dense_field: "dense-field-v1"` only when the mode is on.
`test_dense_field.py` ([expectations](TEST_EXPECTATIONS.md#the-dense-mode))
is the test.

### Polarization (`ray-polarization-v1`)

The rule ([Highlights](HIGHLIGHTS.md) 3.26, "Forces and polarization are
catalog entries, not engine mechanisms", and 3.19, the external body's
couplings; [ray-event model](RAY_EVENT_MODEL.md#6-migration-in-order),
feature 11; issue #169; 2026-09-17): polarization is a family property read
only at a meeting, exactly as charge is. A ray carries a transverse direction
modulo a half turn, an integer from 0 below 2^`polarization_bits`, or none.
The engine adds no mechanism for it: nothing moves differently because of
it. Three things read it: a coupling's `when` guard or invariant, a meeting's
output that declares which polarization it carries, and the polarizer, an
external body's coupling that splits by a declared table.

**The property.** `Ray.polarization` is `-1` (`POLARIZATION_NONE`, an
unpolarized ray, which every ray of every existing world is and every field
ray a charge releases is) or an integer step of the family's polarization
circle. A polarization is a line, not an arrow, so the circle covers a half
turn: a family declares `polarization_bits` on its `spatial_fields` entry
(ray transport only, an integer from 0 through 30), 2^`polarization_bits`
steps per half turn, and without the key its circle is its phase width
(`polarization_modulus` is 2^`phase_bits` then), so a world with the
catalog's default width of 8 has 256 steps of 180/256 degrees and 22.5, 45,
67.5 and 90 degrees are the steps 32, 64, 96 and 128 exactly. Step 0 is the
first transverse lattice axis of the ray's heading in Port order (+Y for a
ray on +X or -X, +X for a ray on +Y, -Y, +Z or -Z) and half the circle the
second (+Z, +Z, +Y): these two values are the two states of Highlights 3.26,
the two lattice axes perpendicular to an axial heading; the steps between
them are the transverse direction 3.26 allows for the circular case, without
the handedness bit, which no ray carries. The engine reads the value only as
a difference on the circle, so which axis is "first" is a convention of the
tables, not a rule. The electron family's spin is the same property at one
bit: `polarization_bits` 1, the steps 0 and 1 or none, with no other engine
meaning (the catalog's `pauli_exclusion` may read it; nothing reads it today).

**Where it comes from and what keeps it.** A lamp declares the polarization
of what it emits: `polarization` on the emission, `"none"` (the default) or
a step below the field's circle; a directed or swept emission, a Kerengonen
mirror's re-emission and a carried re-emission stamp it on every ray they
create (`emit_rays`). A field ray released by a charge or a body carries
none. It is part of the merge identity (`ray_merge_key`, last): rays merge
only at equal polarization, as they merge only at equal bit and sign, the
unpolarized ray ordered first. The return keeps it (`return_ray`), the
inverse split copies it to every transmission (`transmit`), a push keeps it
(`pushed_ray`), and a recoil, the field ray a momentum table returns
reversed, keeps its field ray's. A spread carries it as it carries the phase
(`spread_polarization`): the polarization of the whole is one polarization,
the step nearest the direction of the sum of amount x e^(i 2 pi p / 2^bits)
over the taken polarized rays (the axial mean, each line's doubled angle on
the polarization circle, which is exactly that circle; `combined_polarization`
over the family's `polarization_tables`, the cosine and sine tables of the
polarization modulus, at most twelve bits for a spreading family); an
unpolarized ray adds no direction, and a cancelled sum, two equal crossed
lines, or no polarized ray gives none. Every departure of the spread carries
it, a register's release included: a remainder register stores no
polarization, as it stores no bit, so keying the registers by polarization,
which would multiply their eighteen by the circle, is not done and the
combination is the phase's. A meeting's outputs carry the polarization of
their source `input` unless the output declares `polarization`:

| `polarization` on an output | The output carries |
| --- | --- |
| `"same"` (default) | Its source input's polarization |
| `{"of": i}` | Input i's |
| `"none"` | None |
| an integer | That step of the output field's circle |

An output's polarization is not an assignment of the view (no `read` or
`update` is charged for the default), so a rule that declares none is
charged what it was charged before this feature; a rule that declares one,
or whose guard or invariant names the property, reads one more view
component per participant and is charged one `update` per output. Any
other value, an index beyond the roles or a step outside the circle is
rejected before a world exists.

**Visibility.** `RAY_PROPERTIES` gains the read-only property
`polarization`, the step as stored (`-1` none): a `when` guard or an
invariant reads it as it reads `charge` (`{"field": "polarization",
"participant": 0}`); an assignment to it in a rule without outputs is
refused as read-only. `validate_rays` refuses a step outside the family's
circle. The `ray-recording.json` sidecar carries it on every ray and the
viewer's `runs.json` on every segment (`polarization`, `null` for none).

**The polarizer.** The fourth coupling of an external body beside the sink,
a rule over a token and the momentum table: a polarization read
([Highlights](HIGHLIGHTS.md) 3.19), declared on the body, `"coupling":
"polarizer"` with its declaration:

```json
{"external_bodies": [
  {"position": [12, 4, 4], "family": "apparatus", "amount": 1,
   "coupling": "polarizer",
   "polarizer": {"family": "light", "angle": 32, "pass": [1, 0, 0],
                 "table": [256, 256, 256, 255, ...], "unpolarized": 128}}
]}
```

`family` is the ray family it polarizes (any ray family of the world other
than its own), `angle` the body's own polarization, an integer step of that
family's circle, `pass` a unit-axial heading of the family (+X by default),
`table` one entry per step of the circle (D = 2^`polarization_bits`
entries, each from 0 through D), the pass share in D-ths at the difference
d, and `unpolarized` the pass share of an unpolarized ray in D-ths, the
table's mean, floor(sum(T) / D), by default. The catalog's reference table
is cos^2(d x 180 / D degrees) in D-ths, rounded: `[8, 7, 4, 1, 0, 1, 4, 7]`
at three bits, the Born table read over the half turn; a world writes its
own D entries, and the engine only splits by the table. A polarizer without
`angle`, a table of another length, an entry above D, a heading that is not
unit-axial, a declaration under another coupling and a coupling `polarizer`
without the declaration are rejected with a message that names the circle.

What it does, in `SpatialNode.receive` at step 2 of the Node's law, where
the sink acts: each outbound ray of the polarized family that arrives, in
merge-key order (`polarize_content`), is split by the table at d = (angle -
polarization) mod D: the whole quanta of amount x T[d] / D leave on the pass
Port as a fresh event ray of the body's Node (`steps` 0, the mask of the
pass Port and its amount as the share) with the ray's phase, advance, bit
and source sign and the body's angle as its polarization, resident this
interval and one Link on with the residents; the whole quanta of amount x
(D - T[d]) / D end in the body's sink counter for the family, on the audit's
`absorbed_by_bodies` line, moving the body by its `momentum_table` as the
sink does; and the two shares below one quantum, amount x T[d] mod D and
amount x (D - T[d]) mod D in D-ths, which sum to D or to 0, go to the body's
pass and sink registers of the ray's sign (`ExternalBody.held`, six per
body, sign-major -1, 0, 1 then pass and sink, with a phase each,
`held_phases`, combined with the share's phase by the coherence rule as a
spread's register's is, `field-remainder-v1`). A register that reaches D
releases the whole quanta it holds, to the pass Port as a fresh event ray
with the register's phase, sign and the body's angle and the highest bit of
this meeting's arrivals, merged with a pass ray of the same phase, or into
the sink, and keeps the rest; the registers of one sign therefore always
hold whole quanta in total (`held_stock`), which the ledger's `current` line
counts (`totals`, `charge_totals`), content without momentum. An unpolarized
ray takes the `unpolarized` share. A returning ray ends in the sink as at
every body; a family the polarizer does not name ends in the sink. The
momentum the body takes is booked on the absorbed momentum line when a
momentum field is bound: what arrived less what left on the pass Port, the
held quanta having none. Energy is exact: what arrived equals what passed
plus what sank plus the whole quanta the registers gained, at every arrival
and in the world ledger at every tick. When every amount is a multiple of D
the split is exact and the remainder rule is not exercised; A12's chain of
four exercises it. The polarizer is declared on the body and not as a rule
over a token because its rest ends in a counter and its remainder in
registers, which the rule form (rays in, rays out, exact over rays) cannot
express; the token form is that form's device and is not needed here. The
two-channel form A13 names, the rejected share leaving on a second Port
instead of sinking, is not declared.

**The record.** One `polarizer` event per arriving ray (`body`, `port` the
Port it came in through, `family`, `amount`, `polarization` (`null` for
none), `sign`, `angle`, `difference` (`null` for none), `share`, `steps`,
`passed`, `sunk`, `held` (the two shares added), `released` (the whole
quanta the registers released to the pass Port and to the sink after this
ray) and `registers` (the six after it)), published with the interval's
returns, and one `external_body_absorbed` per arrival Port for what sank in
whole quanta, so a reader of the sink line and the viewer see it as any
absorption. `Polarized` (`core/spatial_state.py`) is the record, registered
in the Node state contract with `Polarizer`. `external_bodies()` lists a
polarizer body's `held` and `held_phases`; the runner's `external_bodies`
entry carries its `polarizer` declaration (`family`, `angle`, `pass`,
`steps`, `unpolarized`) and its `coupling` `"polarizer"`, and the runner
records `ray_polarization: "ray-polarization-v1"` when the world declares
the property anywhere (a family's `polarization_bits`, an emission's
`polarization`, a rule naming it, a polarizer body). A world that declares
none runs byte-identically, records included: every ray carries none, no
view is read wider, no output is assigned, and the pinned digests of
`test_ray_momentum_turn.py` and `test_field_spreading.py` hold.
`test_ray_polarization.py` ([expectations](TEST_EXPECTATIONS.md#ray-polarization))
is the test; A12 ([experiments](EXPERIMENTS.md#a12-maluss-law-and-the-three-polarizer-chain-after-feature-11))
is the confrontation, `examples/nature/a12_malus/`.

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
  `escaped` and `annulled` lines, `external_body_totals()` the
  `absorbed` line, what the external bodies' sinks took (`absorbed_by_bodies`,
  [external body](#the-external-body-external-body-v1)), and, since
  `detector-absorb-v1` (2026-09-18), `detector_mark_totals()` the
  `absorbed_by_marks` line, what the Detector marks absorbed on their clicks
  ([a click is an absorption](#a-click-is-an-absorption-detector-absorb-v1)),
  each with the momentum field's components when one is bound; every ledger
  also carries the bodies' own lines (`bodies`: their count, the exact sum of
  their momentum from `external_body_momentum()`, the sum of their declared
  charge and their sinks per field) and the marks' (`marks`: their count, the
  exact sum of their momentum from `detector_mark_momentum()`, their counters
  per field), beside the identity, since a body's content never enters a sum
  and its momentum is its declared response to the fields it absorbs, not a
  ray's, and a mark's counter is what its clicks took;
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
identity, initial + sourced = current + escaped + annulled + absorbed +
absorbed_by_marks for amount, momentum and charge at every completed tick,
re-checked from the recorded integers (`audit_failure`; a line recorded before
`detector-absorb-v1` has no `absorbed_by_marks` and reads it as zero). A `ray_interactions` rule with outputs
whose family's charge differs from the charge of the inputs its amount comes
from would change the total charge, and is rejected at validation. Nothing
else changes: events, states and totals are byte for byte what they were,
the audit adds readouts. `test_ray_event_audit.py`
([expectations](TEST_EXPECTATIONS.md#ray-event-audit)) is the test.

### Binding as a loop (`loop-binding-v1`)

The rule ([Highlights](HIGHLIGHTS.md) 3.4, "Binding is a periodic orbit of
the meeting rule", model owner, 2026-09-17, with 3.3, 3.5, 3.17, 3.19, 3.20,
3.28 and 5.2; [ray-event model](RAY_EVENT_MODEL.md#6-migration-in-order),
feature 14; the design in [loop binding](LOOP_BINDING.md)): a ray never
stops, and "bound" does not mean "resident" but "back at the same place in
the same state". A **bound group** is a set of rays that is a periodic orbit
of the Node's law of Highlights 5.2: rays in motion on a **ring** of Nodes,
the closed path they walk, whose corner meetings, under an ordinary
`ray_interactions` rule with outputs ([meetings with
outputs](#meetings-with-outputs-ray-meeting-conversion-v1)), reproduce the
rays that entered them, every ray again at the same Node with the same
heading, amount and phase modulo the circle after the period, so that the
same meetings happen again. There is no binding rule and no register: the
only declared thing is the table, and whether a content closes under it is a
computation, not a declaration. A set whose meetings do not reproduce it
disperses: a corner with one ray fires no rule and the ray crosses off the
ring. `test_loop_binding.py`
([expectations](TEST_EXPECTATIONS.md#loop-binding)) is the test; the
demonstration is the unit-square electron, `examples/nature/ring.json` with
its dispersing control `ring_open.json`
([E5](EXPERIMENTS.md#e5-the-ring-an-electron-at-rest-as-a-loop)).

**What it does.** The smallest loop on the cubic lattice is the unit square,
four Nodes and four Links, with rays circulating both ways; the Port form of
the **corner table** is an outputs rule in today's schema, each input's
amount and phase leaving through the Port the other input came in by:

```json
{"name": "corner", "participants": [{"type": "electron"}, {"type": "electron"}],
 "outputs": [
   {"field": "electron", "amount": {"of": 0}, "heading": "reversed", "input": 1, "phase": {"of": 0}},
   {"field": "electron", "amount": {"of": 1}, "heading": "reversed", "input": 0, "phase": {"of": 1}}],
 "invariants": [{"name": "energy", "expression": {"field": "amount"}}]}
```

Eight rays, one of each sense at every corner, make every corner meet every
interval (two interleaved four-ray orbits whose meetings never mix); four
rays, two per sense at opposite corners, are the smallest closed set.
Closure is integer equalities ([loop binding](LOOP_BINDING.md#3-closure-as-integer-equalities)):
a partner at every corner, the headings by the ring's geometry, the amounts
by the table (every amount under the Port form; equal senses a quarter turn
apart under the catalog's Born table, which disperses in phase), and the
phase closing on the circle, `L r = 0 (mod N)` for one circuit (`4 r = 0
(mod 8)` at N = 8: r = 2 closes in one circuit, the catalog's r = 1 in two,
nothing lost). The group's content is the sum of its rays' amounts, exact at
every tick, and its mass (Highlights 3.4, 3.28); its clock is the phase of
its rays, advancing by the rest rate at every Link; the content passing a
corner per interval is what a crossing ray meets, and the delay such a ray
suffers is the `delay` output of its meeting with the ring's rays, per corner
crossed, not a Node-wide number. The momentum the two quarter turns of a
corner move, `(2a, 2a, 0)` at P0 of the unit square and the like at the
other corners, is booked as that corner's source of the momentum field, as
the momentum a table split moves, the four corners summing to zero; the
recoil it stands for belongs to the group's own field, and the closure of a
ring with its own field, from which alone a content ladder can come, is open
([loop binding](LOOP_BINDING.md#6-the-field-of-a-loop)). Every ring ray
releases its field on the five headings other than its own at every Node it
departs, as any ray in motion ([released
field](#field-as-the-rays-information-released-field-v1)). An arriving ray
meets a ring ray at a corner by the table declared for the families present,
and its outputs leave the ring or join it (`examples/nature/absorption.json`:
a light ray taken into the ring by a corner rule over
`[electron, electron, light]`; `photofission.json`: a light ray above the
threshold letting a pair through unturned, momentum exact by heading);
nothing else creates or destroys a group. The motion of a group as a whole
is its corners shifting, a different periodic orbit, open
([loop binding](LOOP_BINDING.md#8-motion-of-a-loop-as-a-whole)).

**The schema.** Nothing new: a binding coupling is an ordinary
`ray_interactions` rule with outputs, and the catalog's `binds` entries are
corner tables ([catalog](CATALOG.md)). The engine's one rule of this
feature is in the meeting: a rule meets only rays that arrived at the Node,
so an event ray still at its event Node (`steps` 0 with an event stamp), the
output of a rule waiting its declared `delay` there, is met by nothing and
leaves when its wait is over; a `delay` assignment or output is an
output-clock wait, never a hold, and no rule can hold its participants by
meeting them again. A world that declares `ray_delay` on a rule, or
`momentum_table` beside `assignments`, is rejected at initialization with a
message naming the [migration
note](MIGRATION.md#binding-as-a-loop-landed-on-2026-09-17-loop-binding-v1).
The runner records `loop_binding: "loop-binding-v1"` beside `ray_binding`.

**What was removed (2026-09-17).** The held form of
[`ray-binding-v1`](#binding-and-gravity-by-delay-ray-binding-v1): a rule
without outputs whose assignments set `delay` 1 as a hold, the rule's
`ray_delay` and the Node's `bound_delay`, `bound_group`, the snapshot's
`bound_groups`, the `bound_tick` record and the six-heading release of a
held ray; and all of
[`bound-group-motion-v1`](#bound-group-motion-bound-group-motion-v1): the
register and its accumulators, `group_step`, `carry_rays`,
`bound_group_step`, `momentum_table` on a binding rule, the ledgers'
reading of a group by its register and `SpatialPacket.group`. What stays:
the outputs rule and its `delay` output, the delay table and the lag
register (gravity by delay, the identity `ray-binding-v1` keeps), the
momentum register of a free ray and `momentum_table` on couplings of free
rays and on the external body, the released field with its spreading and
remainder, the external body, and the Node's five-step law, which the loop
uses unchanged. The nature examples that used the held form are loops
(E1 to E3) or retired with their records kept (E6).

**The reading of a group.** Nothing at a Node names a group; a group is a
set of rays that repeat, read from the record by a Renderer. The ray
viewer's extractor (`tools/ray_viewer/extract.py`, `periodic_groups`) reads
the matter rays that keep meeting each other at the Nodes where they meet:
their states there (Node, heading, amount, phase) must recur with a period
T over a window of at least two periods, the rays that meet there within the
window are the group, the Nodes they walk its ring, at least four distinct
Nodes; the components that walk one ring are one group. Each group reports
its ring (the closed walk of its Nodes), its content (per family and in
all), its period, its clock (the phase advance per interval of each family,
read from the recorded phases) and the ticks it was read over; the run
document lists `groups`, each ray carries its `group`, each tick row its
`bound` content, which the viewer draws as matter
([ray viewer](../tools/ray_viewer/README.md)). On `ring.json` the reading
is one group on the unit square, content 8, period 4, clock 2 on the 8-step
circle, from tick 1; on `ring_open.json` none.

Admission: that of every ray interaction with outputs; no draw, no new
arithmetic. A world without a `delay` assignment on a rule without outputs
runs byte-identically in its events; its `state.json` lost the empty
`bound_groups` key.

### A decaying group draws (`decay-draw-v1`)

The rule ([Highlights](HIGHLIGHTS.md) 3.26 with 3.19 and 5.4; [ray-event
model](RAY_EVENT_MODEL.md#6-migration-in-order), "the weak interaction and
decay", feature 13 of issue #169, landed 2026-09-17 in the loop form of
feature 14): "A free particle never decays, because there is no event
without a meeting and a straight ray does not change; a neutron is a bound
group whose ticks are events, and a bound group that can decay is a source,
and a source is a Detector (section 3.19): at each tick it draws with its
declared ratio as the setting, 1 = the conversion fires, 0 = the group ticks
on unchanged, so half-life follows and nothing else in the world draws."
Under [binding as a loop](#binding-as-a-loop-loop-binding-v1) there is no
held group and no group tick at one Node: a bound group is rays circulating
on a ring whose corner meetings are its events. The draw is therefore a
property of the meeting, declared on the conversion's rule, and the Detector
mark on a Node is a different thing and is not required.

**The reading of "at each tick" (the implementation's, 2026-09-17, for the
model owner to confirm).** A group's ticks are its corner meetings, so a
decaying group draws once at every corner meeting of the rule that can
convert it, and a ring whose rays meet at every corner every interval draws
at every corner meeting. The survival law that follows is per meeting: a
ring survives k meetings with probability `(1 - n/d)^k`, so its half-life is
`k_half = -ln 2 / ln(1 - n/d)` meetings (about `d ln 2 / n` for a small
setting), and in intervals it is `k_half / m` for a ring with m meetings per
interval: on the unit square four per interval on the eight-ray ring
(`ring.json`, every corner every interval) and two per interval on the
four-ray ring, so `T_half = k_half / 4` and `k_half / 2` intervals there. The
formula of the register and the catalog, `T_half = -ln 2 / ln(1 - n/d)`
intervals, is the case of one meeting per interval; experiment A9 reads its
neutron's half-life from its ring's meetings per interval
([A9](EXPERIMENTS.md#a9-neutron-decay-from-the-bound-group-draw)).

**The schema.** A `ray_interactions` rule with outputs may declare its decay
setting and the seed of its draws:

```json
{"name": "decay", "participants": [{"type": "electron"}, {"type": "electron"}],
 "draw": [1, 64], "seed": 6,
 "outputs": [
   {"field": "p", "amount": {"of": 0}, "heading": "same", "input": 0, "phase": {"of": 0}},
   {"field": "p", "amount": {"of": 1}, "heading": "same", "input": 1, "phase": {"of": 1}}],
 "invariants": [{"name": "energy", "expression": {"field": "amount"}}]}
```

| Key | Values | Rule |
| --- | --- | --- |
| `draw` | `[n, d]`, `1 <= d <= MAX_VALUE`, `0 <= n <= d` | The decay setting: the share of the draw range on which the conversion fires, read exactly as a mark's `setting` (the bit is 1 when the drawn number times `d` is below `n` times `TICKET_MODULUS`); `[0, 1]` never fires, `[1, 1]` always |
| `seed` | `0 <= seed < TICKET_MODULUS` | The start of the stream a Node the declaration marks draws from; required with `draw`, refused without it |

`draw` on a rule without outputs, a numerator above the denominator or below
0, a denominator below 1 or not an integer, a setting that is not a pair, a
`draw` without `seed`, a `seed` without `draw`, or a seed at or above the
ticket modulus are rejected at initialization with a message naming the
reason. The parsed rule carries `draw` (the pair) and `seed`
(`InteractionDefinition`); a rule without `draw` carries None and is what it
was.

**What it does.** When the participants of a decaying rule meet (a group
`participant_groups` forms in declared order, its `when` guard true; a false
guard is no meeting under the rule and draws nothing), the meeting draws
once, one draw per meeting and not per ray, from the Node's ticket stream
with the rule's setting: `ticket_bit(state, n, d)` in `core/spatial_state.py`
is the unsalted draw of [the mark](#detector-mark-detector-mark-v1)
(`state = next_ticket(state, 0)`, `number = ticket_draw(state)`, bit 1 when
`number x d < n x TICKET_MODULUS`), the one `detector_draw` calls, and it
reads nothing from the rays. On 1 the rule fires: its outputs replace the
participants as at any [meeting with
outputs](#meetings-with-outputs-ray-meeting-conversion-v1), the conversion.
On 0 the rule does not fire, the participants stay available, and the
meeting continues to the next rule in declared order; on a ring that is the
corner table, which reproduces the ring, so the group ticks on unchanged.
The draws of one cycle are taken from the stream in the order the rules and
groups are met, and a Node with several decaying rules draws for each
meeting of each from the same stream. Nothing is charged to the cost meter
for a draw, as at a mark.

**The marked Node.** Only a Node whose Detector bit is set may draw
(Highlights 3.19, 5.4). A Node at which a decaying rule fires counts as
marked by the declaration: what marks it is the rule, its setting the
rule's `draw` and its seed the rule's `seed`, and the mark acts on the
meeting alone, since nothing declared a setting for the Node's arrivals, so
they are not drawn and its bit is not set for them. The Node's one ticket
state, `SpatialNodeState.detector_ticket`, is the stream: at a Node that
carries a `detectors` mark it is the mark's, seeded from the mark, its
arrivals drawn at the receipt (`detector-mark-v1`) and its meetings drawn in
the cycle from the same stream, in that order; at a Node without a mark it
is seeded when the Node is created from the declaration salted by the
Node's position, `decay_ticket_seed(decay_seed(rules), position)`: the seeds
of the rules that declare `draw` folded in declared order by the ticket rule
(the first seed as the state, each further seed one salted step) and then
one salted step per coordinate, so that two corners of one ring draw
independently, as two marks with their own seeds do (the square in
`ticket_draw` breaks the affine relation between the streams). A world
without a decaying rule seeds nothing: every unmarked Node's ticket stays 0
and the ticket rule is never called, as before. The ticket state enters the
Node's law as an input (`SpatialLaw.__call__(..., detector_ticket)`, the
last argument of `SpatialPlanningInput`, so a reused plan never replays a
draw at another state) and leaves with the plan's `decay_draws`, the last of
which is the stream's state after the cycle, which the Node commits.

**The conversion may change family.** The weak interaction is a change of
family (Highlights 3.26), so a decaying rule's outputs may be of families
its inputs are not: the total amount (the energy invariant), the declared
invariants and the appended charge invariant are exact as before, the
per-family stock equality of `ray-meeting-conversion-v1` is not required of
a rule with `draw`, and what each family lost or gained at the meeting is
booked as that family's source in that cycle (`source_delta` of the
`spatial_cycle` record, `electron -2, p 2` for the rule above), the families
summing to zero, so every line of the [world
ledger](LOCAL_CONSERVATION.md#the-world-ledger-ray-event-audit-v1) stays
exact, the charge lines with them (a family's sourced charge is its charge
times that amount). A rule without `draw` keeps every family's stock as
before; the generic key the [dictionary](../examples/nature/README.md)
states for such a rule (`"stock": "converted"` with a `converted` line of
the audit) stays open.

**The record and the audit.** Each draw is a `decay_draw` event of the Node
in the cycle: position, tick, `rule` (the rule's name), `setting` `[n, d]`,
`ticket` (the stream's state the draw left) and `bit`, written before the
cycle's `ray_push` and `spatial_cycle` records, in the record's order of
Nodes; a draw of 0 is recorded as much as a draw of 1, since a ticket was
consumed either way. The tickets a Node consumed in one tick are therefore
counted from the record as its `detector_click`, `detector_return` and
`decay_draw` lines, the line experiment B2 audits against the arrivals at
marked Nodes and, now, the meetings of decaying rules
([B2](EXPERIMENTS.md#b2-one-draw-only-at-a-marked-node-and-replay-determinism)).
The stream is a function of the seed, the Node's position and the order of
its draws alone, so a replay writes the same draws, conversions and events.
The ray viewer reads the event as a generic marker (`decay draw`).

**Identity and admission.** The runner records `decay_draw:
"decay-draw-v1"` in `run.json` when a rule of the world declares `draw`; a
world without one runs and records byte for byte what it did (its plan key
carries a constant 0). The admission is that of every ray interaction with
outputs. `test_decay_draw.py` ([expectations](TEST_EXPECTATIONS.md#decay-draw))
is the test: the E5 ring with a decaying conversion of two electrons into
two rays of a second family declared before the corner table, its draws by
hand from the published ticket rule, the first 1 at P1 in the cycle of tick
11, the ring surviving until then and dispersing after, the ledger exact,
the tickets consumed equal to the meetings, the replay identical, the
control without `draw` never calling the ticket rule, the rejections. The
catalog's `weak_conversion` is written in this form
([catalog](CATALOG.md)); the neutron's ring under `quark_binding` is not
yet declared, so A9 stays planned.

### Binding and gravity by delay (`ray-binding-v1`)

The rule ([Highlights](HIGHLIGHTS.md) 3.4, 3.17 and 3.28; [ray-event
model](RAY_EVENT_MODEL.md#6-migration-in-order), step 8; issue #169,
feature 8): matter is a bound group, binding is the interaction whose result
is zero events, a bound group is unbound by an arriving ray, and gravity is
bending by delay. `test_ray_binding.py`
([expectations](TEST_EXPECTATIONS.md#ray-binding)) is the test.

**Superseded on 2026-09-17.** The held form of this section (binding,
unbinding, mass as output-clock delay: rays resident under a rule with
`delay` 1 and no outputs, the `ray_delay` wait, `bound_group`,
`bound_groups`, `bound_tick`, the six-heading release of a held ray) was
removed by feature 14, [binding as a loop](#binding-as-a-loop-loop-binding-v1)
(`loop-binding-v1`; Highlights 3.4, model owner, 2026-09-17): a bound group is
a periodic orbit of the ordinary meeting rule on a ring of Nodes. The text
below describes the interim form as it was, for the record; what stays of this
identity is gravity as bending by delay, the delay table and the lag, which
the paragraphs "Gravity as bending by delay" and "G_eff across the phase
width" state and `test_ray_binding.py` keeps (with resident content, a
record holding stock, as the mass).

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
rays and, since `bound-group-motion-v1`, the group's momentum register:
`bound_group` reads the group from the rays (the outbound rays at their
event Node with no delay or wait pending, which under this admission are
exactly the rays a rule holds there), the snapshot lists `bound_groups`
(position, families, amounts, phases, `ray_delay`, `momentum`,
`accumulators`) for a Renderer to draw matter, and the runner records
`ray_binding: "ray-binding-v1"` beside `released_field`. A group whose
register is nonzero moves by it ([bound group
motion](#bound-group-motion-bound-group-motion-v1)); the head-on pair of
this section, with register (0, 0, 0), stays. A rule assigning a delay above 1 holds its group and ticks
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

### Bound group motion (`bound-group-motion-v1`)

**Removed on 2026-09-17.** All of this identity (the register and its
accumulators, `group_step`, `carry_rays`, `bound_group_step`,
`momentum_table` on a binding rule, the ledgers' reading of a group by its
register, `SpatialPacket.group`, `test_bound_group_motion.py`) went with the
held form under feature 14, [binding as a loop](#binding-as-a-loop-loop-binding-v1)
(`loop-binding-v1`): the motion of a group as a whole must be its corners
shifting, a different periodic orbit
([loop binding](LOOP_BINDING.md#8-motion-of-a-loop-as-a-whole)), which is
open. The text below describes the interim form as it was, for the record;
`motion_step` stays for the external body.

The rule ([Highlights](HIGHLIGHTS.md) 3.4, 3.14, 3.16, 3.19 and 3.28;
[ray-event model](RAY_EVENT_MODEL.md#6-migration-in-order), step 8, feature
8c; issue #169): matter is a bound group, and a group that moves one Link
every k intervals has speed 1/k with no kinematic rule in the engine. The
motion is the external body's rule of section 3.19 applied to matter, the
same integers and nothing new: a momentum register over the group's content,
exact accumulators that step one Link when a whole content has accumulated
on an axis. The gap it closes was found by the helium-ion run
([E4](EXPERIMENTS.md#e4-the-helium-ion-one-electron-at-a-nucleus-of-charge-2)):
under `ray-binding-v1` alone a group was held at its Node and could not
move. `test_bound_group_motion.py` was the test.

**The register.** A bound group carries a momentum register, three integers,
and three per-axis accumulators (`BoundMotion`, held by the Node beside the
rays as `bound_motion`, bounded metadata of the group like the external
body's mark; None at a Node without a group). The register is set when the
group forms, in the cycle whose binding meeting first holds the rays, as the
sum of amount x heading of the group's rays as that meeting stamps them (a
binding rule assigns no heading, so this is the momentum that arrived): a
head-on pair of equal amounts has (0, 0, 0) and stays at rest. The
accumulators start at (0, 0, 0). A meeting that re-holds the group with its
rays turned (an outputs rule whose outputs carry `delay` 1, the excited
electron of the nature examples) moves the register by exactly the momentum
by headings it moved, so the register is the rays' headings plus every push
the group has received.

**The push.** A binding rule may declare `"momentum_table": {family: sign}`
(family name to -1, attraction toward the source of an arriving field ray,
or 1, repulsion; [disturbances](DISTURBANCES.md#json-schema-versions-1-and-2)),
exactly the external body's table. The named families join the rule's
layer. In every interval the binding rule fires, every resident outbound ray
of a named family that no earlier declared rule met (a field ray that
arrived that interval) is met by the group: the register changes by sign x
amount x heading of the arriving ray, as `body_absorb` changes the body's
momentum, and the field ray is returned reversed as the recoil, a new event
ray on the negated heading with its amount and phase (the recoil of
[released-field-v1](#field-as-the-rays-information-released-field-v1),
Highlights 3.5). A family that also has a declared rule with the group's
families is met by that rule first, in declared order; absorption of the
field ray into the group is not declared in this slice (the group's content
is its rays, and a field ray is information).

**The step.** Each interval the group is bound, from the first tick after the
meeting that formed it and before the cycle, every accumulator adds its
momentum component, and the whole group departs one Link through the Port
of the first axis (x before y before z) whose accumulator has reached the
group's content, the sum of the amounts of the rays held at the start of the
interval, the accumulator reduced by the content: `body_step` applied to the
group, at most one Link per interval, never faster than a ray, a momentum
above the content failing the cycle. In that cycle the binding rule fires as
every interval (the group's tick: the event stamp, each phase advanced by
its rest rate, `bound_tick` published), the group releases its field on the
five headings other than the one it steps through (that heading is its own
line ahead of it, which the group occupies: no self-field, Highlights 3.5,
as the body releases), and the held rays leave on the packet of that Port as
the group reads them, steps 0 and delay 0, with their event stamp and phases,
the register and its accumulators (`SpatialPacket.group`) and the group's
clock; the Node publishes `bound_group_step` (position left, Port, arrival
tick, momentum, accumulators, content) after the `bound_tick`, and its
output-clock delay `bound_delay` returns to 0, since the clock went with the
group. The group is on the Link for the interval, and at the arrival tick
the neighbour Node holds its rays resident with the register installed; in
that Node's cycle the binding rule fires again on arrival, as at any
meeting, so the group re-forms there and `bound_tick` continues at the new
Node; whatever else arrives or is resident there is met by the declared
rules in declared order (a collision decided by the tables, an unbinding
rule with outputs first). The `ray_delay` of the rule is set on the new Node
by the plan of that cycle, so rays arriving there with the group are not
delayed in the arrival interval. Speed is therefore momentum over content,
one Link every k = content / |p| intervals on an axis, Highlights 3.28 with
no kinematic rule: a group of content 8 and momentum (4, 0, 0) moves one
Link every two intervals, and one pushed to (-2, 0, 0) one every four.

**Dissolution and collision.** When a group dissolves (an earlier outputs
rule unbinds it, or the rule does not fire and the rays leave along their
lines), the Node books the difference between the held rays' momentum by
headings and the register as the meeting's source of the momentum field
(zero unless the group was pushed), so that the outputs' momentum by
headings is exact against the register that left the ledger, as the
momentum a table split moves is booked
([meetings](#meetings-with-outputs-ray-meeting-conversion-v1)); the register
is dropped. A Node holds one register: a group arriving at a Node that
already holds a group, or two groups arriving in one interval, fails closed
(two bound groups at one Node are not admitted in this slice, and a Renderer
draws a moving group as one sphere that moves).

**The audit.** The world ledger reads a bound group's momentum by its
register, not by its held rays' headings: at a Node, or on a Link while it
steps, the group's rays add nothing by heading and the register is added
once under the momentum field the group's families bind (a group whose
families bind two momentum fields fails closed at formation; one whose
families bind none reads nothing, as before). The push is booked as an
explicitly accounted source of that momentum field, and the recoil's
reversal by headings as any meeting's momentum change, so
`conserved_at_every_completed_tick` stays true at every tick; a group that
leaves an open boundary is booked as escaped with its content per family and
its register (`spatial_escaped` carries `bound_group`: families, amounts,
content, momentum). The local conservation audit reads the register the same
way (`InventoryNode.group`, `InventoryPacket.group`,
[local conservation](LOCAL_CONSERVATION.md#the-world-ledger-ray-event-audit-v1));
the push, like the momentum a split moves, is booked to the world ledger
only. The snapshot's `bound_groups` entries carry `momentum` and
`accumulators`; the runner records `bound_group_motion:
"bound-group-motion-v1"` when any group stepped or any rule declares a
momentum table. A world where no group ever has a nonzero register runs
byte-identically in its events and run record (the head-on pair of
`ray-binding-v1`); its `state.json` gains the two zero entries per group.

```json
{"name": "bind", "participants": [{"type": "n"}, {"type": "n"}],
 "assignments": [
   {"participant": 0, "field": "delay", "expression": 1},
   {"participant": 1, "field": "delay", "expression": 1}],
 "momentum_table": {"G": -1},
 "invariants": [{"name": "energy", "expression": {"op": "add", "args": [
   {"field": "amount", "participant": 0}, {"field": "amount", "participant": 1}]}}]}
```

Admission: `momentum_table` on a rule without outputs that assigns `delay`
only, naming ray families that are not among its participants, signs -1 or
1; the named families are admitted as every selected ray field is
(unit-axial, unpaced, no decay). No draw, no new arithmetic beyond the
body's; nothing else changes.

### The law of the bit (`bit-law-v1`)

The rule ([Highlights](HIGHLIGHTS.md) 5.4, the model owner's decision of
2026-09-18 with the amendments of that day; issue #169, feature 15): every ray
carries one bit, `detector` 1 a thing and 0 its shadow, a ray of the same
family as its thing (there is no field family: `field_of` is retired, a family
declares its own `release`, the size of its things' shadow sets; since
node-mixing-v1 nothing of the spread is declared). A thing has a stable id,
`thing` on its disturbance type or external body (the type's index from 1,
then the bodies), stamped on every ray as `owner`. Things move whole and turn
by pushes; shadows spread by the Node's mixing ([below](#the-node-mixes-the-six-node-mixing-v1)),
have no mass, no clock (their phase never
advances) and no delay, and cost no computation of their own. A shadow meeting
a thing of another owner under a coupling with a `momentum_table` pushes it by
sign x amount x heading read times the thing's content (`reads: "content"`) or
times the shadow's source sign and the thing's charge (`reads: "charge"`; the
key is required beside every momentum table, point 16), turns back on its own
steps carrying -dp and walks home, following the Node trace its owner left
(`traces`, the Port the largest thing of each owner left a Node by, at most
sixteen owners per Node), is absorbed back and released again reversed; a
shadow meeting its own thing is home, never a push; a push is not an event
(point 15: no `ray_push`, the runner records the per-thing `momentum` line per
tick, `registers` until node-is-ports-v1). Shadows are given with the board: `initial_field` per family, `{"fill":
T}` (T intervals of the fill, each thing releasing its shadow set of
`release` x stock per heading, rounded to whole quanta per Node and heading
with the fractions in the Node's remainder registers, reflected at sources and
marks, nothing dropped, booked as initial content) or `{"rays": [...]}` (a
profile of shadows with `position`, `heading`, `amount`, `phase`, `sign`,
`owner`, `steps` 0 or 1); nothing is released during a run. A mark returns a
shadow without counting it, and catches things by its setting `[n, d]` read as
a counter: the k-th arrival is absorbed when k mod d < n, else returned (point
14, no lottery: `seed` is accepted and never read; two runs are byte-identical;
`on_click` "absorb" is the default for every family); a mark that absorbs a
thing becomes the home of that thing's shadows, absorbing each that returns
into the same counter. An external body absorbs things into its sink and
returns shadows (pushing itself by its table when it names the family), and
radiates nothing; bodies, marks and the board's edge are the border. The
ledger: `initial + sourced = current + escaped + annulled + absorbed +
absorbed_by_marks + returned` per family, and per bit (`things`, `shadows`,
`things_conserved`): a shadow is initial content, never sourced, and its
homecoming crosses no border (point 7), so `returned` carries only the
momentum shadows bring home; every ray family of a world with one momentum
field is bound to it. Events happen only at Nodes that hold a thing (point
13): a Node holding shadows alone publishes no record, and the dense mode is
the shadow layer, the default wherever a world admits it. The runner records
`bit_law`, `shadow_families`, `initial_field`, `real_content` and
`shadow_content` per tick, `momentum`, `shadows` and `real_conserved` (the
names of node-is-ports-v1; the bit's values are `real` and `shadow`).
Identity `bit-law-v1`; isolated test `tests/test_bit_law.py`
([expectations](TEST_EXPECTATIONS.md#the-law-of-the-bit)); old worlds are
migrated textually by `examples/nature/bit_law_migration.py`. The catalog's
textual migration, the decay table (point 20), the speed rule (point 21), the
restated readings of point 18 and the rest rate of point 19 follow in feature
16.

### The Node mixes the six (`node-mixing-v1`)

The rule ([Highlights](HIGHLIGHTS.md) 5.4, point 24, the model owner's
decision of 2026-09-18; feature 16c): a shadow does not choose its next
heading alone, and not in a pair. At every Node, in every interval, for each
group (one owner, source sign and polarization, as before; shadows of
different owners or of differing polarization do not mix), the shadows that
arrived through the six Ports are six complex amplitudes, A_j = sqrt(amount_j)
at the phase phi_j on the family's phase circle of N steps (a Port with no
arrival is 0; two shadows of the group on one heading are one amplitude, their
amount at the step nearest their coherent sum), and the six leaving amplitudes
are B_h = (1/3) sum_j A_j - A_h: a third of the coherent sum to every Port,
less the arrival that came in through that Port, sent back (the
transmission-line matrix node of Johns and Beurle, S = J/3 - I). The amounts
leaving are the total amount arriving, shared among the six headings in
proportion to |B_h|^2 in whole quanta, the parts below one quantum parked in
the Node's remainder registers per owner, sign and heading in ninths
(`field-remainder-v1`, its unit now `MIXING_DENOMINATOR` = 9, the third
squared; a register at nine releases a whole quantum through its heading with
its phase, as before), and each leaving share carries the phase of its B_h,
the nearest step of N; a zero B_h sends nothing. Nothing is declared: a
`spread` table or a `steering` key on a family is refused naming point 24, and
the family's phase width N is the mixing's one input; every ray family with a
shadow set (a `release`, or a field given with the board) spreads its shadows
this way, and a shadow that walks straight no longer exists. The integers
(`node_mixing` in `core/spatial_state.py`): the amplitude is the integer
square root of amount x 32^2, the phase factors are the cosine and sine tables
of the phase circle at 256, the weights are the squared lengths of 3 B_h (the
same ratios and phases), reduced by a common shift to 28 bits so that every
product stays in 64-bit work, and the total in ninths is apportioned by the
largest-remainder rule, ties to the lower Port: exact conservation,
deterministic, integers only.

By hand: a lone arrival of 9 sends 4 back through the Port it came in by, its
phase turned by a half turn (the minus), and 1 through each of the other five
(four ninths back, a ninth on each other heading); two equal arrivals head on
in phase, a each, send a/9 back each way and 4a/9 through each of the four
transverse Ports; two equal arrivals in antiphase are each sent back whole
through the Port they came in by, nothing transverse. A 1-D chain does not
transmit: the six-Port rule sends a lone shadow on a line mostly back (a
two-Port restriction of S would be pure transmission, but the Node has six
Ports and that is the rule), so a set in one phase moves as a wave because the
turned-back parts of neighbours cancel, and the field is a collective, not a
stream. What stays: the Born split of two things that meet (section 5.2,
`steering_table`, a split indexed by the phase difference); the return of a
shadow after a push, a walk back on the trace, never mixed; a shadow arriving
at its own thing is home; marks and bodies return shadows as before; the
remainders parked at a Node join the next interval's departures on their
heading as before. Retired for shadows: the split table of section 3.5
(`field-spreading-v1`, the `spread` key) and the pairwise steering of point 17
(`phase-spread-v1`, `SpatialFieldDefinition.steering`); the example worlds
lost their `spread` keys (`examples/nature/bit_law_migration.py` drops them).
The dense mode (part 1 of the feature) cycles every Node that holds arrivals
through `spread_content` itself, ray by ray, so the two modes are one
arithmetic by construction; the vectorized twin is part 2. The runner records
`node_mixing` "node-mixing-v1", `field_remainder` and `mixing_fields` (each
family with its `phase_width`), and `shadow_families` carries `phase_width`
in place of a table. Identity `node-mixing-v1`; isolated test
`tests/test_node_mixing.py`
([expectations](TEST_EXPECTATIONS.md#the-node-mixes-the-six)).

### The clock and the readings (`clock-readings-v1`)

The rule ([Highlights](HIGHLIGHTS.md) 5.4 points 11, 16, 18, 19, 20, 21 and
23 and the settled rule (i), the model owner's decisions of 2026-09-18; issue
#169, feature 16b), the engine's only behaviour:

- **The clock is the content (point 19).** No family declares a rest rate:
  `kerengonen.phase_advance`, `rest_rate` on a family and `kerengonen_advance`
  on an emission are refused. A family whose things have a clock declares
  `clock: true` beside its charge (light and the plain family do not), and the
  world declares `K` once, the content per phase step per interval, required
  when any family declares a clock. A thing of a clock family advances its
  phase by `(remainder + content) // K` steps per interval and keeps the rest
  on itself (`Ray.remainder`, below K, a property of the thing and no ledger
  quantity); on its walk back it undoes exactly that interval. A shadow has no
  clock and neither has a family without one: their phase stays what it was
  given. K and N = 2^`phase_bits` bound the content one Node may hold: a
  thing's content / K stays below N / 2 (2 x content < K x N), refused at
  parsing for every emitted content (the largest share of an undirected
  emission) and at a meeting whose output would hold more, which fails closed
  before any owner changes.
- **The computation (point 11).** The world's computation per interval is the
  sum over its things of the phase steps they made that interval, content / K
  each with the remainders carried, constant between absorptions and escapes;
  the engine keeps the running total (`Simulation.phase_steps()`) and the
  runner records `computation_per_tick`, `clock_readings`, `K` and
  `wait_per_quantum` in `run.json`.
- **One shadow set, read twice (points 16 and 18).** A shadow carries its
  owner's id; its owner's charge and content are read by that id from the
  family's owner table (`SpatialFieldDefinition.owner_contents`,
  `owner_charges`: a type's default stock of the family's field with the
  family's charge per quantum times that stock, a body's amount with its
  declared whole charge, 1 and 0 for an owner known from a profile alone). The
  gravity reading, `reads: "content"`: dp = sign x amount x heading x the
  content of what is pushed, exact. The electricity reading, `reads:
  "charge"`: dp = sign x amount x heading x (the owner's charge / the owner's
  content) x the charge per quantum of what is pushed (the family's for a
  thing, the declared charge over the amount for a body, which must divide
  it), accumulated per axis in units of 1 / D on the pushed thing's
  `push_remainder` (D the least common multiple of every owner's content over
  the world, `push_denominator` on every family), the whole units into the
  momentum, rounded toward zero so that a push below one quantum of either
  sign accumulates exactly and the remainder keeps its sign. The same shadows
  are read once per momentum rule of the thing they meet: a shadow an earlier
  rule turned back for that thing pushes it again under the next rule's
  reading and carries the sum of the pushes home; a shadow another thing took
  is left to it. The catalog's `mass_field` and `mass_field_delay` are retired;
  `reads` admits nothing beyond the two words.
- **The decay table (point 20).** `draw` and `seed` on a rule are refused. A
  rule with outputs may declare `decay: {"after_periods": n}` (the group
  breaks at its n-th meeting under the rule; its passages are counted on its
  rays, `Ray.periods`, carried by the outputs of the corner table declared
  after it, and reset to 0 on the outputs of the decay, which are fresh
  things) or `{"content_at_most": c}` (it breaks when the content of the rays
  met is at most c); the condition is read at every meeting the rule's guard
  admits, nothing is drawn, no counter and no ticket, and two runs are
  byte-identical.
- **One Link per interval and the step (point 21, the settled rule (i)).**
  Every ray moves one Link per interval on its heading; `ray_delay`,
  `ray_phase_per_tick` and, on a board of ray fields, `computation_field` are
  refused, and the DDA staircase of `ray-momentum-turn-v2` is retired
  (`ray-momentum-turn-v3`). The momentum a thing carries (`Ray.momentum`) is
  the pushes it has taken and not yet spent; the ledger reads a thing's
  momentum as amount x heading plus that (`thing_momentum`, the `momentum`
  line of the record). At a departure the first axis (x before y before z)
  whose component has reached the thing's content turns the thing to that
  axis, the sign choosing the sense, and the component drops by the content;
  at most one step per departure; a component on the thing's own direction
  turns it nowhere and drops nothing. What a step takes off the thing's
  momentum as the ledger reads it, content x the heading before the step, is
  booked on the momentum field's line as `spent`: `initial + sourced = current
  + escaped + annulled + absorbed + absorbed_by_marks + returned + spent`
  there, the other lines carrying no `spent` key (an optional line of
  `ray-event-audit-v1`).
- **A thing pays a tick for every whole quantum it reads (point 23).** A push
  of whole quanta on a thing's momentum owes it w intervals per quantum,
  w = n / d the world's `wait_per_quantum` (1 by default; an integer or
  `[n, d]`), kept exactly on the thing (`Ray.owed`, in units of 1 / d) and
  spent one interval at a time: an interval in which the thing neither moves,
  nor steps, nor advances its phase, the only exception to one Link per
  interval; a shadow pays nothing. The queued reading of DERIVATIONS.md
  section 24 (w per quantum, always).

Choices where the text was open, flagged for the owner: the clock is declared
per family as `clock: true` (the text says a family declares only its charge
and its tables; something must tell light from an electron); a body's declared
`charge` is its whole charge; a type owner's charge is the family's charge per
quantum times its stock; the electricity remainder rounds toward zero; a
component reaching the content on the thing's own direction drops nothing;
`after_periods` counts the group's meetings under the rule, so a world that
means full circuits of a ring of L corners declares n x L or guards the rule
to one corner. Identity `clock-readings-v1`; isolated tests
`tests/test_clock_readings.py` ([expectations](TEST_EXPECTATIONS.md#the-clock-and-the-readings)),
`tests/test_wait_rule.py` ([expectations](TEST_EXPECTATIONS.md#the-wait-per-quantum-read))
and the step in `tests/test_ray_momentum_turn.py`; old worlds are migrated
textually by `migrate_clock` in `examples/nature/bit_law_migration.py`.

### A Node is its six Ports (`node-is-ports-v1`)

The rule ([Highlights](HIGHLIGHTS.md) 5.4, point 22 and the five settled
rules, the model owner's decision of 2026-09-18; issue #169, feature 17):
every store the model kept on a Node or beside the rays is a ray with a
property, and what remains of a Node is its Ports. The engine's only
behaviour, with no declarable alternative:

- **The parked shadow.** What a Node holds below one quantum is a shadow at
  rest among its rays, `Ray.parked` 1, a bit-0 ray of its owner on the Port
  heading it will leave through, its amount in ninths of a quantum (the
  mixing's unit S = 9 since node-mixing-v1, `parked_unit`; a family without a
  shadow set parks nothing but traces). The spread step reads
  the parked shares as the block it always read (`parked_shares`), combines
  each with the shares it adds by the coherence rule, releases a share that
  reaches S whole through its heading, and parks the rest again
  (`park_shares`); the books count the parked shadows as shadow content, whole
  quanta per Node in total (`parked_stock`); a parked shadow is outside the
  slot budget and never forwarded. The separate remainder registers of
  `field-remainder-v1` and their `field_remainders` snapshot are gone: the
  snapshot lists `parked` (position, family, owner, sign, heading, amount,
  unit, phase, bit), the `field_spread` record carries `parked` and
  `parked_phases`, and the dense region keeps the same shares in its `reg`
  arrays, read back as parked rays.
- **The trace.** What a Node remembers of a departure is a parked shadow of
  amount zero, left at the Node a thing departs on the heading the largest
  thing of each owner left by (`leave_trace`, at most sixteen owners per
  family and Node, the lowest ids dropped beyond it), read by the shadows
  coming home (`trace_of`); a family whose lines are not the six Port headings
  leaves none. Settled rule (ii): a prefilled shadow's steps are its Link
  distance from its owner's Node (for several Nodes, the one its line crosses,
  else the nearest; 1 for an owner with no Node on the board; `steps` 0 or 1
  may still be declared), so its return arrives where the owner was; home with
  the owner present it is absorbed and re-released; with a trace it follows;
  with none it waits at the Node, a zero-step shadow at rest (outbound 0,
  steps 0), until a thing of its owner passes and takes it home. The record
  of a trace at a mark where a thing ended is no longer needed: the resident
  thing is the home.
- **The resident thing.** A mark's counter is a thing resident at the mark
  (`DetectorMark.resident`, a `Resident`): a click is an absorption into it,
  its content per family growing by the absorbed amount (`real`) and its
  momentum by the absorbed momentum, its `owners` the identities absorbed; the
  mark's `on_click` table is the resident's declared table. Settled rule
  (iv): a shadow of an absorbed thing that returns to the mark is absorbed into
  the resident on its `shadow` line with the momentum it carries, makes no
  event and is never a click (the `shadow_absorbed` record is gone; the
  reception record still carries `absorbed_by_mark` for the local audit).
  `detector_marks()` and `run.json` list each mark's `resident` (`real`,
  `shadow`, `momentum`, `owners`); the ledger's `marks` lines read `real` and
  `shadow`. Settled rule (iii): a seeded thing missed at a mark walks back to
  its seed Node and, the inverse split of a lone ray being the ray itself, is
  restored to its lamp and leaves again on its original heading in the next
  cycle. A mark declares no `seed` (rejected).
- **The source.** A source is a thing that spends its content: an emission on
  a ray family is paid from the emitting type's content of that family and
  recoils into the type's momentum, the world's one signed three-component
  conserved field that is not a spatial field, which the type must hold; the
  `source`, `recoil_field` and `funded` keys of the lamp are rejected on a ray
  family, nothing is sourced, and a lamp burns content. The ledgers per bit
  read `initial + converted = current + escaped + absorbed` (the real line,
  `converted` what a meeting turned into or out of the family, `absorbed` what
  ended in a body, in a resident thing or at an annulling inverse split) and
  `initial = current + escaped + absorbed_at_home` (the shadow line).
- **The apparatus** (a mirror, a splitter, a phase plate, a polarizer, a
  wall, a screen, a beam stop) are things with declared tables: an external
  body with its identity, its content and its coupling rule; the catalog's
  apparatus entries and the example worlds are migrated textually
  (`examples/nature/bit_law_migration.py`).
- **The names of the bit.** The two values of the bit are `real` (1) and
  `shadow` (0) (the model owner, 2026-09-18), and the records and the books use
  them: the ledgers per bit are `real` and `shadow`, the flag
  `real_conserved`, the runner's per-tick lines `real_content` and
  `shadow_content`, the resident's lines `real` and `shadow`; the ray's bit
  stays the field `detector` with the values 1 real and 0 shadow. "Thing"
  stays the noun for a real ray.
- **The momentum.** A thing's momentum is a property of the thing; the word
  register leaves the engine with the stores it named. The runner's per-tick
  `registers` line is `momentum` (the momentum of every thing per tick, keyed
  by thing id, from its rays and its body).
- **Performance.** The dense region carries the returns per Node, owner, sign
  and heading (`ret_*`: the amount, the phase of the sum, the momentum carried
  and the least steps), walked one Link back per interval, following the
  owner's trace (`trace`) or waiting (`wait_*`) as the planner does, handed to
  the engine only at its Nodes; the arrays hold amounts as int32, phases as
  int16 and flags as int8; the engine's totals are computed once per tick per
  bit and memoized until content moves. The loss is the per-ray identity of a
  return inside the region (its own phase and steps); the record of a dense
  Node is its totals. The per-Node snapshot still reads the region's Nodes as
  Node state.

Identity `node-is-ports-v1`, recorded in `run.json` as `node_is_ports`;
isolated test `tests/test_node_is_ports.py`
([expectations](TEST_EXPECTATIONS.md#a-node-is-its-six-ports)).

### A Port is two lanes (`lanes-v1`)

The rule ([Highlights](HIGHLIGHTS.md) 5.4, point 25, the model owner's
decision of 2026-09-18; issue #169, feature 18), the engine's only behaviour:
a Link carries rays both ways, so every Port has two lanes, in and out, and a
Node has twelve; in one interval a lane carries at most one real ray and at
most one shadow of each owner.

- **The slots.** The state of one family at a Node is addressable as
  [Port][lane][real | shadow(owner)] (`node_lanes`, a `LaneSlots`): twelve
  lanes (`lane_index`, the Port's in-lane 0 or out-lane 1), on each one real
  slot and one shadow slot per owner in the family's owner order
  (`owner_index`; the owners are assigned at parsing to every thing and to
  every owner of a declared profile, `family_owners`, so the shadow axis is
  fixed before the run), and beside them the parked shadows and the traces of
  point 22 (`parked`) and the rays at rest at the Node this interval
  (`resident`: a returned thing at its event Node, a shadow whose steps are
  spent, a held ray). A ray on its way occupies the in-lane of the Port it
  entered through, opposite to its heading; the shadow slot of an owner holds
  the owner's shadows on that lane as one sum (their amount and the momentum
  they carry added, the least steps, the phase of their coherent sum), one
  ray each once the Node's mixing of point 24 (feature 16c) lands. The engine
  stores the slots as the Node's ray tuple in merge order, so the reading
  functions, the inventory, the records and the snapshot are unchanged in
  content and in order, and holds the slots' bounds as its invariant: one
  real per out-lane at every departure, whatever the families (`LaneClaims`
  in `forward_rays`, checked again by `validate_plan_rays`), and one real per
  lane on a declared board.
- **The step condition.** The lane is a condition on the step, not a queue:
  at a Node's departure every ray that leaves on its own heading takes its
  lane first (an emission, a returned ray, a re-release, a thing continuing);
  a thing whose momentum has reached its content on another axis
  (`step_thing`) steps into that out-lane only if the lane is free, otherwise
  it keeps its heading, its momentum stays accumulated, and it steps at the
  next Node; every thing moves one Link every interval, the wait of point 23
  the only exception. The things that would step are resolved after the
  others, in the Node's ray order, each holding its own heading's lane until
  it is resolved. Two reals of different merge keys leaving on one lane are
  refused (a `ValueError` naming point 25): no Port sends two, so none
  receives two; rays of one merge key are one ray. The lane is one direction
  of a Port, so the claims and the check take the rays on the six Port lines;
  a ray of the old ray worlds on a line that is not a Port heading holds no
  lane. A ray born onto a lane another thing continues on in the same
  interval (a return at a mark, an emission, a meeting's output) is the case
  the law declares impossible without naming another rule; the engine
  refuses that departure rather than queue, wait or carry two.
- **The validations at parsing.** A declared board with two real rays on one
  lane is refused: two seeds at one Node whose types emit one ray family on
  the same declared heading (or both sweeping the sequence). A table of
  section 5.2 gives its outputs distinct lanes: two outputs of one rule on
  one heading (the same Port, or the same or the reversed heading of one
  input) are refused. An emission table's outputs occupy distinct lanes: a
  sweep of `rays_per_tick` consecutive headings that repeats a heading is
  refused. Every refusal names point 25. A source emits and its thing leaves,
  always: no condition of a free lane stands on an emission.
- **The dense layer.** Its per-owner arrays are the shadow slots of this rule
  already (one entry per Node, owner, sign and Port, the returns beside
  them); a Node holding a thing is the engine's (`_engine_bound`), so the
  real slot lives in the ray path and not in the arrays.

Identity `lanes-v1`, recorded in `run.json` as `lanes`; isolated test
`tests/test_lanes.py` ([expectations](TEST_EXPECTATIONS.md#a-port-is-two-lanes)).
The shipped worlds `examples/nature/absorption.json`, `absorption_emission.json`
and `helium_ion.json` declare tables (`absorb`, `nucleus_turn`) whose outputs
share a heading; they are refused by this rule until the model owner declares
their tables anew.

### A free ray turns by momentum (`ray-momentum-turn-v2`)

Restated on 2026-09-18 under `clock-readings-v1` (above): the momentum a
thing carries is the pushes it has taken, the step of the settled rule (i)
replaces the DDA walk of v2, and the momentum spent on a step is booked. The
text below describes v2 and stands as its history.


The rule ([Highlights](HIGHLIGHTS.md) 3.5, 3.14, 3.16 and 3.28;
[ray-event model](RAY_EVENT_MODEL.md#6-migration-in-order), step 8, feature
8b; issue #169): a ray's direction is its momentum vector, and a field ray
that meets it changes that vector by the momentum it carries, so a free ray
bends gradually, by the field, and not by whole Ports alone. The gap it
closes was found by the helium-ion run
([E4](EXPERIMENTS.md#e4-the-helium-ion-one-electron-at-a-nucleus-of-charge-2),
"the missing rules", ii): a free ray's heading changed only by an outputs
rule's Port table or by the lag of `ray-binding-v1`, one Link sideways per
phase modulus with the heading unchanged, so a curved path, light bending
(A6) or an electron deflected by a charge (A5), was not expressible. It is
the momentum register of `bound-group-motion-v1` given to a free ray.
`test_ray_momentum_turn.py`
([expectations](TEST_EXPECTATIONS.md#a-free-ray-turns-by-momentum)) is the
test. `ray-momentum-turn-v2` (2026-09-17) keeps the DDA's accumulators
through a push ("a push keeps the walk", below), the fix the helium-orbit
run ([E8](EXPERIMENTS.md#e8-the-helium-ion-with-the-field-spreading-and-the-momentum-turn)) asked for.

**The register.** Every ray carries a momentum register, `Ray.momentum`,
three integers: by default `None`, which reads as amount x heading of its
line, the momentum every ray has carried since `isotropic-ray-field-v1`, so
every existing ray is unchanged and every existing record byte-identical
where no push happens (the test's case (d) pins the digests of two worlds).
A push sets the register to an explicit vector; a push that brings it back
to the default clears it, so a ray that resumes its line is the ray it was
and merges with its kind. `ray_momentum_vector` reads a ray's momentum
either way; a return negates the register with the heading
(`return_ray`), and a returning ray reads as its share on the event's
heading as before; the register is part of the merge identity, and rays of
one register that merge carry the sum of their registers, as they carry the
sum of their amounts (a register is extensive). Storage: three stored
values bounded by `MAX_VALUE`, not all zero.

**The DDA walks the register.** At every departure the Port is chosen by
`dda_step` on the ray's vector (`ray_vector`): the register when one is
set, the heading of its line otherwise, with the ray's three accumulators
exactly as today (they add the vector's components, the axis furthest
ahead steps and loses the vector's Manhattan length, ties to the lowest
axis). So a ray with momentum (7, -1, 0) takes seven +X Links per -Y Link,
and one with (2, 3, 0), past 45 degrees, three +Y per two +X, one Link per
interval always: the momentum sets the direction and never the speed, which
is the one speed of the board (Highlights 3.28). The DDA on a register and
on the same vector scaled give the same Ports (the accumulators scale with
it), so the register needs no reduction. The heading index stays the ray's
line for the rules that read it: a coupling's view of `heading`, the event
Port of a return and the inverse split read the index; the release
geometry of [released-field-v1](#field-as-the-rays-information-released-field-v1)
skips `ray_line`, the unit-axial heading of the register's dominant axis
(the largest component, ties to the lowest axis), the line the ray occupies
ahead of it, and releases on the five others. A rule that assigns the ray a
new heading clears the register: the new line is what the rule said.

**The push.** A `ray_interactions` entry without outputs and without
assignments may declare `"momentum_table": {family: sign}` (family name to
-1, attraction toward the source of an arriving field ray, or 1, repulsion;
[disturbances](DISTURBANCES.md#json-schema-versions-1-and-2)), the table of
`bound-group-motion-v1` with one difference: it names a participant
family. Such a rule is a coupling of free rays: its one role the table does
not name is the ray that is pushed (`turn_receiver`); every other role's
families are named, the field rays; a table that names no participant is a
binding rule's (a group's push), and a mixed role or two unnamed roles is
refused at admission. In the interval the rule's guard holds over a group of
its participants, the ray is pushed by every resident outbound ray of a
named family that no earlier declared rule met, the group's field
participant among them, in slot order: each push is sign x amount x heading
of the field ray, exactly `body_absorb`'s and the group's arithmetic, the
register moves by it (`pushed_ray`) with the walk kept (the next
paragraph), and the field ray is returned reversed as the recoil, a new event
ray on the negated heading with its amount and phase (the recoil of
[released-field-v1](#field-as-the-rays-information-released-field-v1),
Highlights 3.5, 3.14). A push never changes the ray's amount, phase, bit,
heading index, steps or event record: it is not a new event of trajectory
in the sense of Highlights 5.2 step 4, no event is stamped and the ray's
record stays, so the return of a pushed ray still undoes its event. A push
that would leave the register at the zero vector fails the cycle: a ray
never stops. A later group of the same rule whose field ray an earlier push
took does not fire (one receiver per rule per Node per interval takes every
field ray the table names); a family that also has an earlier declared
rule with the ray's family is met by that rule first. A coupling with
outputs is an ordinary meeting and declares no table, as before. The Node
publishes one `ray_push` record per field ray met (family, amount, the
register before and after, the field family, its amount and its heading),
before the cycle's record; the runner records `ray_momentum_turn:
"ray-momentum-turn-v2"` when any push happened, and nothing for a world
where none did (a free-ray table alone does not mark `bound_group_motion`).

**A push keeps the walk (`ray-momentum-turn-v2`, 2026-09-17).** The three
accumulators are the walk's progress along the register: per axis, the
momentum-intervals banked toward the next Link on that axis, every interval
depositing the register's component and a Link on the axis withdrawing the
register's Manhattan length (`dda_step`). A push changes the deposit and the
price, not the balance: the accumulators carry over unchanged and continue
against the new register (`continued_walk`), so under a push at every
interval the ray walks the DDA line of its running register, one Link per
interval along the axis furthest behind, the staircase of a circle under a
central push that turns the register, and a small transverse push that
arrives every interval banks toward a transverse Link as the register turns
(a ray of 64 along +X pushed by (0, 1, 0) at every Node steps +Y at Links 9,
15, 20 and 24, the parabola of a constant push; pushed by (0, 8, 0) it is
past 45 degrees at Link 8). Two cases start the walk over at (0, 0, 0): a
push that returns the register to the default amount x heading, the ray
resuming its line as the ray it was, and a push that shrinks the register
below the banked progress, an accumulator outside the admissible (-length,
length] of the new length, which the new register cannot hold. A ray
without a register walks the heading of its line at the table's scale, and
the default register is amount x that heading, so the first push lifts its
accumulators by the amount, exactly (the DDA on a scaled vector takes the
same Ports from accumulators scaled with it), zero on a unit-axial heading.
v1 reset the accumulators at every push, as at a change of line, which the
helium-orbit run ([E8](EXPERIMENTS.md#e8-the-helium-ion-with-the-field-spreading-and-the-momentum-turn)) showed
steps a ray pushed at every interval, every ray in a spreading field, along
its register's dominant axis alone, the whole-Port turn by another road; a
record made under v1 in which a pushed ray had progress banked is not
reproduced by v2 ([migration](MIGRATION.md#a-push-keeps-the-walk-on-2026-09-17-ray-momentum-turn-v2)).
A world without a push runs byte-identically, as before.
`test_momentum_turn_walk.py`
([expectations](TEST_EXPECTATIONS.md#the-walk-kept-through-a-push)) pins the
staircases, the flip, the cancel, the shrink and the lift.

```json
{"name": "turn", "participants": [{"type": "electron"}, {"type": "light"}],
 "momentum_table": {"light": -1},
 "invariants": [{"name": "energy", "expression": {"op": "add", "args": [
   {"field": "amount", "participant": 0}, {"field": "amount", "participant": 1}]}}]}
```

**The identity.** The world ledger reads a free ray's momentum by its
register (`ray_momentum`, wherever it is: at a Node, on a Link, escaped,
absorbed by a body's sink), and the push is booked as a meeting's momentum
change exactly as `bound-group-motion-v1` books a group's push: at the push
Node the ray's family changes by sign x amount x heading of the field ray
(the push) and the field family by -2 x amount x heading (the reversal),
both as the meeting's source of the momentum field the families bind, so
`initial + sourced = current + escaped + annulled + absorbed` holds at every
tick and `conserved_at_every_completed_tick` stays true. The recoil carries
the opposite of what the field ray brought back along its line to its
source, and what the source does with it is the source's own table (a
body's `momentum_table`, a group's, or the open `recoil_return`); the
identity does not depend on it, since every change is an explicitly
accounted source (Highlights 3.15). The local audit reads the register the
same way (`InventoryNode` rays, [local
conservation](LOCAL_CONSERVATION.md#the-world-ledger-ray-event-audit-v1));
the push, like the momentum a split moves and a group's push, is booked to
the world ledger only. A ray with a register that a legacy absorption rule
takes is taken whole (`ray_momentum_share`). The ray viewer's momentum
arrow reads the register from the recording (`tools/ray_viewer`).

Admission: `momentum_table` on a rule without outputs and without
assignments, naming at least one participant family and leaving exactly
one role unnamed, signs -1 or 1; the named families are admitted as every
selected ray field is (unit-axial, unpaced, no decay). Not in this slice:
absorption of the field ray into the ray (the table returns it reversed),
a push combined with an assignment or a delay table on one rule (gravity's
delay and turn stay two rules), and the lag's own modulus for the delay on
the ray's own axis (`lag_bits`, [catalog](CATALOG.md)); the transverse
part of the lag, the turn, is what this register carries with no modulus
but the ray's amount, of any width because it enters no phase sum
(Highlights 3.28).

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
