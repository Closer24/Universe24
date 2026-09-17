# Detector-owned sampling

The canonical contract is `detector-only-v1`, the only sampling profile. Only a
Node whose Detector bit is set may draw ([Highlights](HIGHLIGHTS.md) 3.19):
creation, propagation, ordinary contacts, phase changes, field emission,
strong/weak coupling and absorption do not authorize a draw. An entity name,
diagnostic observer, seed or supplied ticket does not establish a Detector.

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
([the mark](#the-detector-mark-detector-mark-v1), `detector-mark-v1`); no
ordinary owner calls it. The native program admission, resolver construction
and resolver ticket gates were deleted on 2026-09-17 with the integration
layer, and the bond-registry gate with the registry itself.

No physical probability, transport, conserved quantity, ownership layout, phase
rule or timing law is changed by this admission boundary. The mark below
implements the draw and PASS; the return on 0 is the next step.

## The Detector mark (`detector-mark-v1`)

The rule ([Highlights](HIGHLIGHTS.md) 3.19, 3.20 and 5.4; [ray-event
model](RAY_EVENT_MODEL.md#1-definitions) "Detector", migration step 3; issue
#169, feature 2): every Node carries one bit, Detector or not, and a marked
Node draws once for each arriving ray, independently, from its own ticket
stream, reading nothing from the ray. This section states the rule the code
implements; the schema key is in [spatial fields](SPATIAL_FIELDS.md#detector-mark-detector-mark-v1).

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
Node in one interval, the Node draws one bit from the mark's own stream,
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
a Node without a mark never calls the ticket rule.

**1, PASS.** The ray continues exactly as at an unmarked Node: it joins the
resident rays and leaves on its line at the next cycle, or enters the coupling
or absorption declared for it. The ray's `detector` field becomes `2`
(a Detector event, bit 1); its steps, outbound flag, event Ports and event
shares are untouched. A `detector_click` event is recorded with the Node's
position, the tick of the arrival, the Port the ray came in through, the
family (the ray field's name), the ray's amount and `bit` 1. The click is the
record of that 1 and the only measurement.

**0, in this slice.** The ray also continues unchanged, its `detector` field
becomes `1` (a Detector event, bit 0), and nothing is recorded: no click and
no outcome, because a return is no measurement. The reversal on the ray's own
line, the walk back by its step count and the inverse split at the event are
feature 3 (`detector-return-v1`) and feature 4 of issue #169, which define
what changes on a return; the mark of this slice changes nothing on the ray
but the bit.

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

## External exchange implementation boundary

The adopted exchange is the Detector of [Highlights](HIGHLIGHTS.md) sections
3.19, 3.20 and 5.4: a marked Node draws 1 or 0 for each arriving transfer,
`1 = PASS` (ordinary behavior for that arrival) and `0 = RETURN` (the same
wave ray reversed on its line, unchanged, walking back the number of steps it
has made since its event and performing the inverse split at its birth event).
A repeated committed decision reuses its immutable result without another
draw, output or inventory charge. The historical quantum instrument that
earlier revisions of this section compared against was deleted on 2026-09-17
with the shared quantum resource.

Closed by `detector-mark-v1` ([the mark](#the-detector-mark-detector-mark-v1)):
the action-bit distribution is the mark's explicit setting `n / d`, with no
default and no assumed 50/50, drawn from the mark's own ticket stream and
reading nothing from the ray; repeat and simultaneous encounters draw
independently, one draw per arriving ray, up to six in one interval, from
that stream seeded by the mark's `seed`. The following definitions are
still open before the return:

| Owner | Missing definition | Acceptance after closure |
| --- | --- | --- |
| Architecture, then field developer | The inverse split at the birth event and the cancellation arithmetic where the returning ray meets the delayed share; the carried step count, the event's Ports and shares and the Detector bit are on every ray since `ray-event-state-v1` ([ray state](SPATIAL_FIELDS.md#ray-state-ray-event-state-v1)), unread | One-Link-at-a-time return; no remote/global erase; complete retained/transferred amounts and remainders |
| Architecture, then engine developer | Detector/model clock mapping, bounded transaction capacity and output-clock composition | Fixed neighbor transit H plus defined output delay, atomic once-only publication and rejected overflow |

An opposite-going ray alone does not define cancellation. An ordinary absorber
cannot be renamed a Detector to fill these gaps. A return that is not the
full reversal and inverse split is not published as physical support: in
this slice a draw of 0 leaves the ray unchanged and recorded as bit 0, and
no world claims a return until feature 3 defines it.


## Required evidence

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
6. The return on 0, causal branch cancellation by the inverse split and
   output-clock composition remain separately blocked until their contracts
   and implementation meet the table above.
