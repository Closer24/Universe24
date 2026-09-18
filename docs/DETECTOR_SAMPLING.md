# Detector-owned sampling

The canonical contract is `detector-only-v1`, the only sampling profile. Only a
Node whose Detector bit is set may draw ([Highlights](HIGHLIGHTS.md) 3.19):
creation, propagation, ordinary contacts, phase changes, field emission,
strong/weak coupling and absorption do not authorize a draw. An entity name,
diagnostic observer, seed or supplied ticket does not establish a Detector.

Since 2026-09-18 (Highlights 5.4, the law of the bit, points 6 and 14;
`bit-law-v1`, `node-is-ports-v1`) nothing draws: a mark meets a thing or its
shadow, decided at the ray's birth; it absorbs a thing into its resident
thing by its declared table (`setting` `[n, d]` read as a counter, the k-th
thing caught when k mod d < n, else returned; `on_click` absorb or pass per
family) and returns a shadow without counting it; the mark declares no seed.
The mark's draw of `detector-mark-v1`, the bit read of
`detector-bit-property-v1` and the decay draw of `decay-draw-v1` below
describe the form before that date, and the last two are retired from the
engine (a decay is a table, point 20); the return and the inverse split
below are what a mark does with a seeded thing it misses (the settled rule
(iii)); a shadow's return is a field with no step count and no inverse
split (point 3 as amended; `bit-law-v1` walks it home on the owner's trace
as the interim form until that lands). The tests of the current rule are
`tests/test_bit_law.py` and `tests/test_node_is_ports.py`
([the law of the bit](TEST_EXPECTATIONS.md#the-law-of-the-bit),
[a Node is its six Ports](TEST_EXPECTATIONS.md#a-node-is-its-six-ports)).

This supersedes autonomous sampling as a universal interpretation of
[postulate 22](../POSTULATES.md#22-historical-autonomous-sampling-candidates).
The earlier local-lottery and bond laws and the `historical-autonomous-v1`
research profile that selected them were deleted on 2026-09-17 (issue #164,
bucket B.5), after the native-contact laws and the shared quantum resource
(buckets B.1 and B.2). Their dated measurements stay in
[validation](VALIDATION.md) and do not establish compliance with this contract.

## Configuration and admission

`sampling_profile` is immutable initialization metadata with one accepted
value, `detector-only-v1` (the default). Any other value, including
`historical-autonomous-v1`, fails admission before a world is constructed or a
ticket is consumed. The keys of the deleted samplers (`"capture": "lottery"`,
`capture_seed`, `capture_salt`, `bond`, `bond_field`, `bond_setting`) are
unknown to the parser, and a typed `SpatialFieldDefinition` whose `capture` is
`"lottery"` is rejected by `validate_spatial_sampling` at `InitialState` and
`SpatialLaw` construction. The deterministic `share` and `threshold` captures
remain and draw nothing. Preflight and run metadata record the profile. No
model ID, entity label or observation callback changes admission.

Validate both the parsed immutable initial state and the responsible local law;
direct typed construction must not bypass the same boundary. The bounded ticket
sequence (`TICKET_MODULUS`, `next_ticket`, `ticket_draw` and the phase tables
in `core/spatial_state.py`) is the local draw the Detector mark owns
([the mark](#the-detector-mark-detector-mark-v1), `detector-mark-v1`); its
one other caller is the draw of a decaying rule at its meeting, the same
draw at a Node the rule's declaration marks
([the decay draw](#the-decay-draw-decay-draw-v1), `decay-draw-v1`,
2026-09-17); no ordinary owner calls it. The native program admission, resolver construction
and resolver ticket gates were deleted on 2026-09-17 with the integration
layer, and the bond-registry gate with the registry itself.

No physical probability, transport, conserved quantity, ownership layout, phase
rule or timing law is changed by this admission boundary. The mark below
implements the draw and PASS, [the return](#the-return-detector-return-v1)
implements RETURN on 0, and [the inverse split](#the-inverse-split-inverse-split-v1)
what the returned ray does at its event Node.

## The Detector mark (`detector-mark-v1`)

The rule ([Highlights](HIGHLIGHTS.md) 3.19, 3.20 and 5.4; [ray-event
model](RAY_EVENT_MODEL.md#1-definitions) "Detector", migration step 3; issue
#169, feature 2): every Node carries one bit, Detector or not, and a marked
Node draws once for each arriving ray, independently, from its own ticket
stream, reading nothing from the ray. This section states the rule the code
implements; the schema key is in [spatial fields](SPATIAL_FIELDS.md#detector-mark-detector-mark-v1).

Decision of 2026-09-17 (Highlights 5.4; feature 2b of the ray-event model,
landed the same day as `detector-bit-property-v1`): a Detector reads the
bit a ray already carries. A ray carrying 1 is already realized and passes
a later Detector without a draw, as a measurement repeated in the same
basis repeats its result, a ray carrying 0 is a transmission and is never
drawn, and only a ray carrying no bit is drawn, how a marked Node meets each
bit being its declared coupling in the catalog with this as the default
([the bit read](#the-bit-read-detector-bit-property-v1)). This section
states the draw of a ray carrying no bit.

**The mark.** The initialization key `"detectors": [{"position": [x, y, z],
"setting": [n, d], "seed": s}]` sets the Detector bit of the Node at
`position`. `DetectorMark(position, pass_numerator, pass_denominator, seed)`
in `core/spatial_state.py` is bounded Node metadata, not a record, not stock
and not an external device: the position must lie within the shape, the
setting is the rational `n / d` with `1 <= d <= MAX_VALUE` and `0 <= n <= d`,
and the seed satisfies `0 <= s < TICKET_MODULUS`. All three are required:
there is no default rate and no default seed, a mark without a setting is a
validation error, and two marks at one position are rejected. A marked Node is
an ordinary Node with its bit set: `SpatialNodeState.detector` holds the mark
and `SpatialNodeState.detector_ticket` its ticket state, seeded from `seed`
when the Node is created and advanced only by draws. In the model a source is
a Detector; in this slice marks are declared explicitly and act on arriving
rays only (an emitting record at a marked Node draws nothing for what it
emits). Nothing else about the Node changes: rays crossing it, couplings,
absorption, fields and audits are what they are at an unmarked Node.

**The draw.** In `SpatialNode.receive`, for each ray that arrives at a marked
Node in one interval carrying no bit (and each ray carrying a bit that the
mark's coupling says to draw), the Node draws one bit from the mark's own stream,
unsalted: `state = next_ticket(state, 0)`, `number = ticket_draw(state)`, and
the bit is `1` (PASS) when `number x d < n x TICKET_MODULUS` and `0`
otherwise, so the setting `n / d` is the pass share of the draw range and
`1 / 1` always passes, `0 / 1` never does. One draw per arriving ray, not per
Port: the draws of one interval, up to six arrivals, one per Port, are taken
one after another from the same stream in the order of the Node's Ports the
rays came in through (`[+X, -X, +Y, -Y, +Z, -Z]`; a ray travelling `-X`
arrives through the `+X` Port) and, within one Port, in the merge-key order of
the rays (heading, accumulators, phase, advance, wait, delay, steps, outbound,
event Ports, event shares, Detector bit). The draw reads nothing from the ray:
not its family, not its amount, not its phase and not its hidden fields; the
Node sees only its own value. Each draw is one `next_ticket` step of the
mark's own state, so a second mark with its own seed draws independently, and
a Node without a mark never calls the ticket rule for an arrival; since
2026-09-17 a Node at which a decaying rule fires draws once per meeting of
that rule from the same one stream ([the decay draw](#the-decay-draw-decay-draw-v1)).

**1, PASS.** The ray continues exactly as at an unmarked Node: it joins the
resident rays and leaves on its line at the next cycle, or enters the coupling
or absorption declared for it. The ray's `detector` field becomes `2`
(a Detector event, bit 1); its steps, outbound flag, event Ports and event
shares are untouched. A `detector_click` event is recorded with the Node's
position, the tick of the arrival, the Port the ray came in through, the
family (the ray field's name), the ray's amount and `bit` 1. The click is the
record of that 1 and the only measurement. Since 2026-09-18 the ray continues
so only when the mark's coupling for its family is `pass`, the default for
matter; a field quantum is absorbed into the mark's counter on its click, by
default ([the click absorbs](#the-click-absorbs-detector-absorb-v1)).

**0, RETURN.** The ray's `detector` field becomes `1` (a Detector event, bit
0) and the ray is returned on its own line, reversed and otherwise unchanged
([the return](#the-return-detector-return-v1), `detector-return-v1`). No
click and no outcome are recorded, because a return is no measurement; a
`detector_return` event records the reversal for the Renderer. At its event
Node the returned ray performs [the inverse split](#the-inverse-split-inverse-split-v1).

**Replay.** The stream is a function of the seed and the arrival order alone:
a recorded run replayed with the same initialization draws the same bits,
records the same clicks and writes the same events. Nothing redraws.

**Admission.** Marks are admitted under the shared Detector admission of
issue #169: `schema_version` 1, `link_ticks` 1, at least one ray field, and
every ray field on `"metric": "links"` with pace `1 / 1`, no decay and
unit-axial headings closed under negation; `node_execution` and
`spatial_computation_delay` are rejected with marks. A document outside this
admission fails before a world is constructed or a ticket is consumed.

**Storage.** Stored values are 32-bit bounded integers (`MAX_VALUE`): the
setting, the seed and the ticket state (below `TICKET_MODULUS`, itself below
the bound). The comparison `number x d` and the ticket square are 64-bit
intermediates (`checked_work`). The Node holds one mark and one ticket state
and nothing about the rays it drew for; the bit travels on the ray.

**Identity.** The runner records `detector_mark: "detector-mark-v1"` in
`run.json` beside `sampling_profile` and `ray_state`.

## The bit read (`detector-bit-property-v1`)

The rule ([Highlights](HIGHLIGHTS.md) 3.20 "Everything is information on
rays" and 5.4 "The Detector's bit is a property of the ray", model owner,
2026-09-17; [ray-event model](RAY_EVENT_MODEL.md#6-migration-in-order)
feature 2b under step 3; issue #169): the bit is a property of the ray like
charge, and a marked Node reads it before it draws. A ray carrying 1 is
already realized: it passes a later Detector without a draw, as a
measurement repeated in the same basis repeats its result. A ray carrying 0
is a transmission: it is never drawn, it passes the marked Node and does
what a transmission does. Only a ray carrying no bit is drawn, as [the
mark](#the-detector-mark-detector-mark-v1) states. How a marked Node meets
each bit is its declared coupling in the catalog
(`apparatus.detector.couplings` of `catalog/nature.json`, `on_bit_1` and
`on_bit_0`), a table entry and not an engine mechanism (Highlights 3.26):
the mark's `detectors[]` entry writes `on_bit_1` and `on_bit_0` as
`"pass"`, the default, or `"draw"`, the draw of `detector-mark-v1` on that
arrival as for a ray carrying no bit, and a mark that writes both `"draw"`
behaves as every mark did before 2026-09-17. Any other value is rejected
before a world exists.

**The pass.** A ray read and passed is unchanged: its bit, steps, phase and
event record are what arrived, it continues on its line or enters the
declared coupling as a pass does, and the mark's ticket stream does not
move. A `detector_pass` event records it: position, tick, the Port the ray
came in through, family, amount and `bit`, the bit it carries (1 or 0). The
passes of one interval follow its clicks and precede its returns in the
event stream. A pass is no measurement: the ray was measured where its bit
was set. A ray on its walk back is not an arrival and is neither drawn nor
recorded ([the return](#the-return-detector-return-v1)); a returning ray at
its event Node performs the inverse split undrawn; what a marked Node emits
or transmits is not an arrival.

**The property.** Two more things make the bit a property and not a hidden
variable, stated with the schema in [spatial
fields](SPATIAL_FIELDS.md#the-detectors-bit-as-a-property-detector-bit-property-v1):
the outputs of every meeting a marked ray takes part in inherit it, the
highest bit among the inputs by the order 1 over 0 over none unless the
rule declares `bit` (`"highest"`, `"none"`, `{"of": i}`), so the
descendants of a realized ray are known to be realized and the descendants
of a transmission are known to carry a return; and a coupling reads it at a
meeting as it reads charge, the read-only ray property `detector` (`0`
none, `1` a draw of 0, `2` a draw of 1) in a `when` guard or an invariant,
so an apparatus that behaves differently for realized content is a catalog
entry. The event Ports and shares stay hidden.

**The price.** The price of Highlights 5.4 (CHSH at most 2 for spacelike
settings) was derived under the rule that the second Detector draws on
every arrival; it is to be re-derived under this rule by hypothesis 11 and
experiment A13 before it is quoted again.

**Identity.** The runner records `detector_bit_property:
"detector-bit-property-v1"` in `run.json` when the world declares the rule
anywhere (a mark's `on_bit_1` or `on_bit_0`, a rule's `bit`); a world that
declares neither runs the defaults and its record is what it was, byte for
byte, unless a marked ray reaches a second mark or meets another ray. The
viewer reads `detector_pass` as the kind `pass` and carries each ray's
`bit`. The test is `test_detector_bit_property.py` ([Detector bit as a
property](TEST_EXPECTATIONS.md#detector-bit-as-a-property)).

## The click absorbs (`detector-absorb-v1`)

The rule ([Highlights](HIGHLIGHTS.md) 5.4 "A click is an absorption", model
owner, 2026-09-18; [ray-event model](RAY_EVENT_MODEL.md#6-migration-in-order)
feature 2c under step 3; issue #169): the field quantum a marked Node
realizes ends there. On a draw of 1 the arriving field content is absorbed
into the mark's exact counter, per family, booked on the audit as absorbed by
marks with its momentum on the marks' line, and nothing of it spreads on: a
photon is detected by being absorbed, and every measurement is paid (3.14). A
draw of 0 stays [the return](#the-return-detector-return-v1), the ray sent
back on its line unchanged, a perfect mirror; a ray carrying 1 still passes
without a draw ([the bit read](#the-bit-read-detector-bit-property-v1)).
Matter that draws 1 passes with the bit 1 as before, so the electron seen
carries its mark.

**The coupling.** How a mark meets each family on a click, absorb or pass, is
its declared coupling in the catalog (`apparatus.detector.couplings.on_click`
of `catalog/nature.json`), with absorb the default for a field family, one
declared `field_of` another, and pass the default for matter (3.26): the
mark's `detectors[]` entry writes `on_click` as `"absorb"` or `"pass"` for
every ray family or as a mapping of ray family name to one of them, so a
screen that stops electrons and a counter that lets light through are catalog
entries. Any other value or an unknown family is rejected before a world
exists; the engine's notion of a field family and the schema are in [spatial
fields](SPATIAL_FIELDS.md#a-click-is-an-absorption-detector-absorb-v1).

**The click.** The draw is the draw of [the mark](#the-detector-mark-detector-mark-v1),
reading nothing from the ray; the coupling is read after the 1, by the ray's
family alone. Under `absorb` the `detector_click` event records position,
tick, Port, family, amount, `bit` 1 and `absorbed`, the amount, and the Node
never holds the ray: it enters no reading, no meeting and no spread, and the
mark's counter for the family and its momentum (amount x heading) grow by
exactly what arrived. Under `pass` the ray continues with its bit 1 and the
click is recorded as before, without `absorbed`. The bit is therefore the
mark of content that passed a Detector without being absorbed, and the field
a Node re-releases never carries the bit of what was realized, because what
was realized is no longer there to spread. The mark's ticket stream moves
once per draw either way; a replay redraws nothing.

**The account.** The counter and the momentum are bounded Node metadata on
the mark, like a body's sink: no rays, no history. Every line of the world
ledger reads `absorbed_by_marks` beside `absorbed` (the bodies' sinks),
initial + sourced = current + escaped + annulled + absorbed + absorbed_by_marks
at every completed tick for amount, momentum and charge, and the marks' own
lines (count, momentum, counters) stand beside the identity as the bodies'
do; the local audit reads what a mark absorbed from the reception record and
reports it as its `absorbed_by_marks` line ([the world
ledger](LOCAL_CONSERVATION.md#the-world-ledger-ray-event-audit-v1)).

**Why.** Decided on the finding of the loop screen (E9, 2026-09-17): with the
clicked quantum spreading on, its bit left the marks along the screen and
back toward the source and the screen stopped clicking at tick 72, a screen
that remembers; a screen that absorbs counts, and its count grows as an
intensity, which the two-slit run A1 needs. E9 was repeated under the rule on
2026-09-18: 265 clicks in 240 ticks, every one absorbed, no pass, the count
growing to the last tick
([E9](EXPERIMENTS.md#e9-the-screen-with-a-loop-source-the-ring-radiating-on-seven-marks)).

**Identity.** The runner records `detector_absorb: "detector-absorb-v1"` in
`run.json` with `detector_marks`, `detector_mark_totals` and
`detector_mark_momentum`, and the marks' lines in every ledger under `audit`.
The test is `test_detector_absorb.py` ([A click is an
absorption](TEST_EXPECTATIONS.md#a-click-is-an-absorption)).

## The decay draw (`decay-draw-v1`)

The rule ([Highlights](HIGHLIGHTS.md) 3.26 with 3.19; feature 13 of the
[ray-event model](RAY_EVENT_MODEL.md#6-migration-in-order), landed
2026-09-17): a bound group that can decay is a source, and a source is a
Detector, so at each of its ticks, its corner meetings in the loop form, it
draws with its declared ratio as the setting, 1 = the conversion fires, 0 =
the group ticks on unchanged, and nothing else in the world draws. The
conversion's `ray_interactions` rule declares `draw: [n, d]` and its
`seed`; when its participants meet, the meeting draws once (per meeting,
not per ray) from the Node's ticket stream with `ticket_bit`, the unsalted
draw of the mark, and fires on 1 only. The Node the rule fires at counts as
marked by that declaration, for the meeting alone: its arrivals are not
drawn unless a `detectors` mark is declared there too, and then the one
stream serves both, the arrivals at the receipt and the meetings in the
cycle. A Node without a mark is seeded from the declaration salted by its
position, so the corners of a ring draw independently. Each draw is a
`decay_draw` record (position, tick, rule, setting, ticket, bit), one per
ticket consumed. The schema, the reading of "at each tick" in the loop form
with the survival law per meeting, the family change of the conversion and
its booking are stated in [spatial
fields](SPATIAL_FIELDS.md#a-decaying-group-draws-decay-draw-v1); the test
is `test_decay_draw.py` ([decay draw](TEST_EXPECTATIONS.md#decay-draw)).

## The return (`detector-return-v1`)

The rule ([Highlights](HIGHLIGHTS.md) 3.19 "0, no measurement", 3.20 "A
return is the inverse split" and 5.4 "PASS and RETURN"; [ray-event
model](RAY_EVENT_MODEL.md#6-migration-in-order) step 4, first half; issue
#169, feature 3): 0 = RETURN is the same wave ray reversed on its line,
unchanged, walking back the number of steps it has made since its event. This
section states what the code does on a draw of 0; the transport of the
returning ray is in [spatial fields](SPATIAL_FIELDS.md#detector-return-detector-return-v1).

**The reversal.** In `SpatialNode.receive`, a ray whose draw is 0 is returned
in the same interval it arrived (`return_ray` in `core/spatial_state.py`):
its heading is negated on its line (the index of the negated heading in the
field's sequence, which the Detector admission guarantees exists), `outbound`
becomes `0`, its per-ray transport accumulators are reset (the three DDA
accumulators, the pace wait and the interaction delay), and its amount,
phase, `steps`, `event_ports`, `event_shares` and family are exactly what
arrived; `detector` is `1`. The returned ray joins the Node's rays and leaves
at the next cycle through the Port it came in through, one Link per tick, as
an ordinary departure: the Node adds nothing, holds nothing and reads
nothing. It merges with nothing, because `outbound` is part of the merge
identity and the returned ray is the only ray of its event on its line.

**No measurement.** Nothing is recorded as an outcome: the `detector_click`
list is what it was, a click per draw of 1 only. The reversal is recorded as
a `detector_return` event (position, tick, the Port the ray came in through
and leaves by, family, amount) so that the Renderer can draw it; it is a
record of the return, not of a measurement. The returned ray is not delivered
flux either: it is left out of the Node's per-Port readings of that interval,
as if the ray had not arrived (Highlights 3.19).

**The walk back.** A returning ray (`outbound` 0) crosses every Node as if
alone: it enters no coupling and no absorption, it is not part of the value,
flux or per-Port samples that couplings read, it takes part in no ray
interaction group, and a marked Node on its way does not draw for it (RETURN
is no measurement, and a return is not an arrival to be measured). Per Link
its `steps` count down and its phase steps back by the field's advance
(`ray-event-state-v1`), so at `steps` 0 it is at its event Node with exactly
the phase and the amount it left the event with.

**Resident at the event Node.** At `steps` 0 the returning ray stops: no
further Link is planned for it (`forward_rays` keeps it) and a Link beyond
its event Node is refused (`advance_ray`). It stays a resident ray of that
Node with `outbound` 0, inert: its phase no longer moves, it enters no
coupling and no absorption, it merges with nothing, and it counts in the
Node's `ray_count` and in the totals. In the next cycle it performs the
inverse split of its share ([below](#the-inverse-split-inverse-split-v1),
`inverse-split-v1`).

**Momentum.** A returning ray's momentum reads as its share of the event on
the event's heading: `ray_momentum` reads amount times the ray's heading
negated when `outbound` is 0 (issue #169, "Momentum of a returning ray reads
as its event share, so the Detector takes no recoil and the audit stays
exact"). The Detector takes no recoil, the return books nothing, and the
momentum total of the world is unchanged by a return, so
`conserved_at_every_completed_tick` and the local audits stay exact through
the return; the inverse split restores the share where it meets it.

**Boundary.** A returning ray never reaches an open boundary before its event
Node, because its `steps` bound its walk. A returning ray in a packet that
would escape means its event Node is not in the world, never the case on a
static board, and the engine fails closed with a validation error instead of
recording an escape.

**Identity.** The runner records `detector_return: "detector-return-v1"` in
`run.json` beside `detector_mark`. No new draw and no new physics: a world
without a mark has no returning ray and runs byte for byte as before.

## The inverse split (`inverse-split-v1`)

The rule ([Highlights](HIGHLIGHTS.md) 3.20 "A return is the inverse split",
"The transmission is a ray" and "Return modes", 5.4 "A pair"; [ray-event
model](RAY_EVENT_MODEL.md#6-migration-in-order) step 4, second half; issue
#169, feature 4, and the model owner's decisions of 2026-09-17): a return
turns time back for that ray's share only. At its event Node the returning
ray performs the inverse split with its information, transmitting it to the
same places the event sent to, so that it cancels what was already there
where it meets it. This section states what the code does with a returned
ray resident at its event Node; the transmission's transport and the
bookkeeping are in [spatial fields](SPATIAL_FIELDS.md#inverse-split-inverse-split-v1).

**When.** A returned ray with `steps` 0 and `outbound` 0 is at its event
Node. In the Node's next cycle (the cycle after the interval it arrived in,
as an emission leaves on the cycle after its record's arrival) it performs
the inverse split of its own share, after the meeting by the declared
couplings and before forwarding, so the transmission leaves the Node on that
cycle like an emission. Nothing stays at the Node: the returned ray is
consumed by the split in every mode.

**The mode.** The world key `return_mode` ([disturbances](DISTURBANCES.md#json-schema-versions-1-and-2),
default `siblings`) selects what the returned ray does. Its own Port is the
Port its event sent it through, the first step of its event heading (its own
heading negated).

- `siblings`: it transmits its amount, phase and bit to every line the event
  sent to except its own: the Ports of its `event_ports` mask other than its
  own Port, at most five. Each transmission is a new event ray at this Node
  (`transmit` in `core/spatial_state.py`): `outbound` 1, `steps` 0, the
  returned ray's phase, advance and Detector bit, `event_ports` the mask of
  the lines transmitted to and `event_shares` the amount per Port. The
  amount is shared over those lines exactly, the remainder to the first
  lines in Port order (Highlights 3.17); a line that would get nothing gets
  no ray. A one-line event (a directed lamp) has no sibling line: with the
  event's input at the Node the share is restored to it (below) and nothing
  is transmitted, the inverse of the emission; without an input the engine
  fails closed, because the share would have no owner.
- `straight`: it continues straight through the Node on the one line
  opposite its own Port, as one new event ray with its whole amount, phase
  and bit, mask of that one Port; enough for a pair, with no per-Port
  records needed on the ray.
- `annul`: it ends there. Its content leaves the world into an explicitly
  accounted sink: its amount into the ray field's annulled total and its
  momentum reading (`ray_momentum`, its share on the event's heading) into
  the momentum field's, `annulled_totals()` per field in the engine and the
  runner, so that initial + sources = current + dissipated + escaped +
  annulled at every completed tick (the runner's
  `accounting_balanced_at_every_completed_tick`, the spatial accounting's
  `balanced` and the local conservation audit's per-Node residual all read
  the sink; since `ray-event-audit-v1` (2026-09-17) the runner's
  `conserved_at_every_completed_tick` reads the sink as a ledger line and
  stays true, as at an open boundary). Its information survives only in the
  record.

**The emission-event case.** If the event's input is still at the Node, the
resident emitting record (a lamp, a bound group: the first record in slot
order with a funded emission rule into the ray's field), the returned share
is first restored to it exactly, the inverse of the funded-emission
bookkeeping: its stock of the field grows by the share and, with a
`recoil_field`, its recoil by share x event heading. The transmission of
the chosen mode is then funded from it in the same interval: stock out by
the amounts transmitted (or annulled) and recoil out by amount x heading
per transmission (or by the annulled momentum), so the net movement of
content equals the mode's rule and the input keeps nothing of the returned
share after the interval; in `siblings` and `straight` it keeps the recoil
of what it transmitted, as of any emission. Both movements are booked as
reactions (restore: field to record; funding: record to field) and the
`inverse_split` record says `restored`. A restored stock or recoil the
field cannot hold fails closed with a clear error before anything moves.
A record that emits by its own rule what it holds will emit a restored
share that stays with it (a one-line event) again as a new event on a later
cycle; that is its rule, not the split.

**No input.** With nothing of the event's input at the Node (an interaction
event whose inputs were consumed), the transmission is booked as a sourced
emission books its rays: the returned share's momentum reading leaves the
source ledger and the transmission's momentum enters it (`source_totals`),
and the ray field's amount moves from the returned ray to the transmission
unchanged. A world under the local conservation audit reports such a Node
as a residual, as it does a sourced emission; the owner of that recoil is
an open point of feature 5 (Highlights 3.20, an ordinary meeting is an
event whose outputs are new siblings).

**The meeting first.** In every mode, if something else is at the Node
(other rays, a bound group that is not the event's input), the returned ray
meets it by the declared couplings before the split (feature 5's layers
apply); a meeting that consumes it makes no transmission. In this slice a
returning ray enters no coupling and no absorption
([the return](#the-return-detector-return-v1)), so nothing consumes it and
the split follows; rays that share the Node with it cross it as before.
The transmission is a ray like any other: what happens when it meets the
share it chases is a declared coupling, not part of this rule.

**The record.** An `inverse_split` event is recorded per returned ray:
position, tick (the cycle's label), `family`, `mode`, `ports` (the Ports
transmitted to, in Port order), `amounts` (the amount per Port), `amount`
(the returned share), `bit` (the ray's Detector bit, 0 or 1), `restored`
and, in `annul`, `annulled` per field. It precedes the cycle's
`spatial_cycle` record.

**Identity.** The runner records `inverse_split: "inverse-split-v1"` and
`return_mode` in `run.json` beside `detector_return`, and `annulled_totals`
beside `escaped_totals`. No new draw: a world without a mark has no returned
ray and runs byte for byte as before.

## External exchange implementation boundary

The adopted exchange is the Detector of [Highlights](HIGHLIGHTS.md) sections
3.19, 3.20 and 5.4: a marked Node draws 1 or 0 for each arriving transfer,
`1 = PASS` (ordinary behavior for that arrival) and `0 = RETURN` (the same
wave ray reversed on its line, unchanged, walking back the number of steps it
has made since its event and performing the inverse split at its birth event,
`inverse-split-v1`); the form before 2026-09-18, since when no mark draws
(Highlights 5.4, point 14).
A repeated committed decision reuses its immutable result without another
draw, output or inventory charge. The historical quantum instrument that
earlier revisions of this section compared against was deleted on 2026-09-17
with the shared quantum resource.

Closed by `detector-mark-v1` ([the mark](#the-detector-mark-detector-mark-v1)):
the action-bit distribution is the mark's explicit setting `n / d`, with no
default and no assumed 50/50, drawn from the mark's own ticket stream and
reading nothing from the ray; repeat and simultaneous encounters draw
independently, one draw per arriving ray, up to six in one interval, from
that stream seeded by the mark's `seed`. Closed by `detector-return-v1`
([the return](#the-return-detector-return-v1)): the one-Link-at-a-time
return of the same wave ray reversed on its line, unchanged, entering no
coupling on the way back and resident at its event Node at `steps` 0.
Closed by `inverse-split-v1` ([the inverse split](#the-inverse-split-inverse-split-v1)):
the transmission of the returned share to the sibling lines of its event by
the world's `return_mode`, the restore and funding through the event's
input, and the annulled sink. The following definitions are still open:

| Owner | Missing definition | Acceptance after closure |
| --- | --- | --- |
| Physics, then field developer | The cancellation arithmetic where the transmission meets the delayed share it chases: a declared coupling of feature 5, not part of the split; and the owner of the transmission's recoil at an event Node with no input | Conserved at the Node where they meet; no remote/global erase; complete retained/transferred amounts and remainders |
| Architecture, then engine developer | Detector/model clock mapping, bounded transaction capacity and output-clock composition | Fixed neighbor transit H plus defined output delay, atomic once-only publication and rejected overflow |

An opposite-going ray alone does not define cancellation. An ordinary absorber
cannot be renamed a Detector to fill these gaps. The split without the
meeting is not published as physical support: in this slice a draw of 0
reverses the ray, walks it back to its event Node and transmits its share
onward, and no world claims the cancellation until feature 5 declares the
coupling.


## Required evidence

Items 5 to 9 state the evidence of the form before 2026-09-18; under the law
of the bit the mark's evidence is `tests/test_bit_law.py` and
`tests/test_node_is_ports.py`.

1. The lottery capture, the bond-registry and claim-gather keys and any
   sampling profile other than `detector-only-v1` are rejected before any
   draw; adding an observer or naming an absorber Detector cannot authorize
   them.
2. Direct immutable-state/local-law construction rejects the same samplers.
3. Deterministic ordinary controls consume zero tickets and preserve their
   exact traces. Every actual simulation run retains its canonical HTML.
4. The dated results of the deleted samplers stay in the validation log under
   their historical profile; they are not canonical acceptance results.
5. A marked Node draws one bit per arriving ray from its own stream, in Port
   then merge-key order, reads nothing from the ray, sets the ray's bit,
   clicks on 1 only and replays identically; an unmarked Node and a control
   world consume no ticket ([Node Detector bit](TEST_EXPECTATIONS.md#node-detector-bit)).
6. A draw of 0 returns the ray reversed on its line, unchanged, one Link per
   tick, through no coupling and no absorption, to rest at its event Node
   with the phase it left with; the momentum total is unchanged and the
   audits exact every tick ([Detector return](TEST_EXPECTATIONS.md#detector-return)).
7. A returned ray at its event Node transmits its share by the world's
   `return_mode`: to the sibling lines with its phase and bit, straight
   through, or into the annulled sink with the conservation line exact; the
   event's input takes the share back and funds the transmission in one
   interval ([Inverse split](TEST_EXPECTATIONS.md#inverse-split)).
8. The cancellation where the transmission meets the share it chases and
   output-clock composition remain separately blocked until their contracts
   and implementation meet the table above.
9. A marked Node reads the bit a ray carries: a realized ray passes a later
   mark without a draw with a `detector_pass` record and a transmission is
   never drawn, unless the mark declares `draw`; the outputs of a meeting
   inherit the highest bit of its inputs unless the rule declares `bit`; a
   `when` guard on `detector` fires for a realized ray only
   ([Detector bit as a property](TEST_EXPECTATIONS.md#detector-bit-as-a-property)).
