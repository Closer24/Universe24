# Local energy and momentum conservation audit

A local law that claims conservation must account for the energy and all three
momentum components of its fields and disturbances together. At each event, the
change in combined node inventory must match actual incoming and outgoing
transport, plus explicitly declared external supply or loss. Field-to-carrier
exchange inside the node cancels between its participants.

The optional audit measures these configured quantities. It does not generate a
physical update, choose an interaction, repair a residual or charge model time.
A failed comparison is evidence that the measured transition does not satisfy
the declared contract. It is not a replacement transition.

## Configuration and supported scope

The optional initialization member `conservation` declares:

| Member | Meaning |
| --- | --- |
| `name` | Identity of this measurement contract |
| `energy_units` | Declared units of the scalar measurement |
| `momentum_units` | Declared units of the three-component measurement |
| `carriers` | Measurement rows with `requires`, scalar `energy` and vector `momentum` expressions |
| `spatial` | One joint scalar `energy` and vector `momentum` expression, required exactly when spatial fields exist |

Each carrier row selects types by the fields listed in `requires`. Every declared
carrier type must match exactly one row, and a measurement may read only the
properties explicitly listed in that row. Field and type names remain references;
no physical species or catalog identity supplies a measurement. The expressions
use the existing bounded integer expression format. Initialization checks their
result shapes and the fields available to the selected owners. Carrier expressions
use the `left` side; spatial expressions use the `right` side. Received/outgoing views
and computation-cost reporters cannot supply measured inventory.

The spatial expressions evaluate the node's joint spatial values and, separately,
the dynamic values in each actual spatial packet. An empty packet must measure
zero energy and zero momentum. Canonical preflight and audit construction use
the same bounded zero-input diagnostic check. That check evaluates only the
measurement expressions; it neither constructs a world nor executes an update,
and it contributes no model operation cost.

This scope requires zero spatial baselines and rejects declared external sources,
unfunded emissions, nonzero decay and native event programs. Open boundaries are supported as explicitly measured escape.

Straight-ray fields are measured as quanta. A ray of amount `a` adds `a` to its
field's value, so the declared spatial energy expression sees it, and carries
momentum `a x heading` intrinsically, in amount times heading units, which no
field expression can express; the spatial momentum expression must therefore
not count ray fields. A [funded emission](SPATIAL_FIELDS.md#funded-emission-and-absorption)
is admitted: the emitter pays each quantum from its own field of the same name
and, with `recoil_field`, loses the emitted `a x heading`, so the transfer is
internal and the audit stays closed. An `absorb` coupling is the reverse
transfer, of a whole ray or of a share of it. Quanta may be negative on a signed
field: the emitter is then credited, the ray's momentum points back at it, and
the absorber pays the share it takes from its own stock, so attraction closes
the same way. Unfunded `source: true` emissions remain rejected.
These restrictions describe supported measurement composition, not a claim that
the excluded physics is impossible.

An omitted `conservation` member selects no additional energy/momentum audit.
Ordinary component accounting and the configured physical laws remain in force.
A passing preflight establishes that the measurement can be prepared, not that
the resulting evolution conserves it or that its units describe real particles.

## Quantities and owners

The model must declare scalar energy, three-component momentum, units and the
admitted input domain. An expression's name does not establish its physical
meaning. A field marked `conserved` preserves additive component stock; it does
not automatically represent kinetic energy, field energy or momentum.

Measurements are additive across actual owners:

- Each resident or traveling disturbance record contributes its configured
  carrier energy and momentum once.
- A node's spatial fields contribute one joint measurement. Expressions may
  include cross terms between those spatial components.
- Each actual spatial packet contributes one joint measurement of the payload
  it owns. Its outgoing port and completed link transit identify its flux.

Received samples are views of node stock. Frozen proposals and pending deltas
are plans, not additional inventory. An unchanged original record remains the
owner during a delayed computation; ownership changes at actual commit.
Immutable baselines are node background, never extra packet payload or a
spendable source. Nonzero baselines are outside this first audit contract; future
background energy exchange needs an explicit model interpretation and a balance
that includes its physical source.

An additive owner model does not implicitly include interaction energy between
separate carriers, or between a carrier and node fields. Such energy needs an
explicit owner or a separately supported joint measurement. Missing terms cannot
be assigned to an unexplained diagnostic remainder.

Joint measurements matter at ownership boundaries. Two cancelling vector fields
can have zero combined squared amplitude at one node, while separating them into
two outgoing packets gives nonzero total squared amplitude. Likewise, adding two
unit packets into one amplitude can change its squared norm while preserving its
linear component sum. Transport, splitting and arrival merging therefore require
the same energy and momentum audit as local scattering.

## Event boundaries and flux

Evidence belongs to world events and their audit ticks. A source event, a later
neighbor receipt and an observer's eventual record are distinct. Local cycle
counters and playback time do not change their order.

The audit compares read-only inventory snapshots after actual commit events.
Check the complete ownership transition at each supported stage:

| Stage | Inventory to compare |
| --- | --- |
| Field phase | Node before and after, together with the actual outgoing packets created by that phase |
| Spatial receipt | Recipient before and after, together with each incoming packet consumed at delivery |
| Carrier cycle | All original and final resident records, actual departing records and simultaneous field reaction, after every update and interaction in the cycle |
| Carrier receipt | Recipient and incoming record ownership across completed delivery |
| Open boundary | The actual escaping packet after its full terminal-link transit |

A packet must have the same measured quantity at departure and receipt in this
closed, nondissipative audit. Link identity includes its carrier/spatial kind,
origin, slot or port, and arrival tick. A newly owned packet contributes outgoing
flux; a consumed incoming packet contributes received flux. When the existing
engine legally changes a packet at the same timestamp, measure the difference
between its new and old measured quantities. Evaluating the payload difference
is not equivalent for a nonlinear measurement. Measure each actual packet
before merging; a function of the aggregate signed flux is generally not
the sum of the packet measurements. A port identifies where flux travels; it
does not derive a dispersion relation or force the configured momentum vector
to be parallel to that port. Such a relation belongs to the candidate law.

A passing early coupling check does not cover a later carrier update. A passing
field-rule check does not cover later arrival merging. A later fault does not
undo an earlier independent event. Reports must identify the stage that failed
and distinguish proposed, committed and in-flight ownership. Because this audit
observes committed events, a reported violation does not undo the event that
violated the contract. A model's separate precommit guards retain their own
atomicity rules.

## Closed transfer, external supply and loss

A closed transfer debits one physical owner and credits another in the same
transaction. Calling a register a budget, or recording an emitted amount as a
source, does not establish such a reservoir. Source and response allowances
bound activity but are not automatically stored energy.

External supply and loss are rejected by this first closed-system audit. A future
implementation admitting them would require separate declared meanings and
independently computed quantities. An open boundary contributes escaped flux.
A dissipative law must identify removed energy and momentum, or reject a
closed-system claim.
The component `transformations` ledger describes changes in coordinates or
components; it is not an energy source. Never define external supply as whatever
residual is needed to make the comparison pass.

## Independence, bounds and acceptance

Measurement definitions are immutable configuration. Each owner expression uses
the fixed configured field and slot bounds. The audit obtains host-wide
read-only inventory snapshots and computes a residual for each affected node.
This is an analyst's world/event audit, not information available to a physical
node or local reception observer. Snapshot traversal, storage and report
aggregation scale with the inspected world and are host work: every checked
event re-measures every active Node and in-flight packet, so a run with many
active Nodes and many events per tick costs their product in host time.

The expressions and comparisons cannot become inputs to physical selection,
routing, updates, timing or local cost. Enabling measurement adds no model
operations or model-time delay; host execution can take longer.

Check expression shapes and integer bounds. An undefined or overflowing
measurement is a failed audit, never zero, a clipped result or permission to
continue claiming conservation. Enabling the audit must leave valid physical
states, physical event order and model operation costs unchanged.

Acceptance needs an argument covering every admitted branch and ownership
transition, plus independent checks with nonzero energy and momentum. Include
signs, axes, noncollinear exchanges, bounds, delayed commits, sources, boundaries
and supported overlap. A globally constant total alone can hide compensating
local errors. Local comparisons plus correct link ownership should explain the
global balance without a repair step.

The [unit-excitation probe](COUPLED_EXCITATIONS.md) conserves its declared
occupation and recoil/flux quantities in a restricted envelope. The
[directional-wave candidate](DIRECTIONAL_WAVE.md) has a different normalized
energy and momentum definition. Neither result establishes all field/matter
physics. Conservation alone does not derive electromagnetic constraints,
particle dispersion, spin dynamics or gravity. Catalog properties and possible
interactions remain descriptive until an explicit law and its independent
acceptance evidence implement the claimed behavior.

The [property-selected reservoir probe](../examples/known-entities/property-coupling-probes.json)
provides explicit carrier and joint spatial measurement data. Its configured
energy and impulse registers are a finite demonstration, not measured particle
energies. [Audit tests](../tests/test_local_conservation.py) cover independent
residual and ownership expectations; passing data still needs the model-specific
acceptance limits described above.
