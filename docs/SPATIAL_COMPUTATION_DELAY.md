# Shared field and carrier computation cycles

> **History (2026-09-19).** The engine this document describes was deleted on
> 2026-09-19 with the old engine ([migration](MIGRATION.md#one-engine-on-2026-09-19-the-old-engine-deleted));
> the one engine is the field-only engine of the law of the shadow
> ([SPATIAL_FIELDS.md](SPATIAL_FIELDS.md#the-law-of-the-shadow-field-only-v1)).
> The text below is kept as the record of what was built and measured; its
> links to code, worlds and tests name files that no longer exist.

Set the top-level boolean `"spatial_computation_delay": true` in an initialization
with spatial fields to select the `shared-field-carrier-cycle-v1` timing candidate.
It works with schema 1 local/outward fields and schema 2 finite attenuating fields.
This cost-derived clock cannot be combined with `node_execution: true`, whose
interaction durations are configured independently of operation cost.
The default is false: existing fixed-clock field transport keeps its timing.
The option applies to every configured field at a node, including vector fields.
It does not select individual physical field names or add a force.

## Configure and run

```json
{
  "spatial_computation_delay": true,
  "link_ticks": 1,
  "normal_budget": 40
}
```

This is a fragment to add to a complete initialization. The timing section of
the configuration UI exposes the same boolean when spatial fields exist.
Use the complete example:

```powershell
python -m event_universe --init examples/spatial_computation_delay.json --output artifacts/field-delay --visualize
```

For a control, copy that input and change only the boolean to false. Compare
actual receipt ticks and inventory, not GIF playback time. The signed streams
are a model probe, not an electromagnetic or gravitational identification.

## One shared clock

Let `h = link_ticks`, `B = normal_budget` and `C` be the combined local work:
field updates, emission, previously completed receipt/decay work, carrier
updates, coupling and the fixed input-merge reservation. Operation prices come
from `operation_costs`; passive diagnostics do not determine C.

```text
k = max(1, ceil(C / B))
commit and directional departure = start + (k - 1) * h
neighbor reception              = start + k * h
next local cycle                = start + k * h
```

The two owners use one ceiling, not two consecutive waits. For example,
C=401, B=100 and h=1 gives departure at tick 4 and reception at tick 5
from a cycle starting at 0. At C<=B departure is at the starting tick,
followed by one full link transit. All scheduling uses bounded integers.

Each port has a logical input at every elementary tick: absent packets mean
zero input. With h=1, an emitted nonzero packet arrives one tick after departure.
Empty ports need no packet object, event or repeated empty calculation. A
nonzero input can arrive while the node is waiting; it cannot restart or retime
the frozen cycle. With h>1, configured link transit takes h ticks.

## Owners and bounded storage

The engine prepares one immutable field/carrier proposal from the local
pre-cycle input. It keeps the original stock and carrier records until ready.
Fresh emission does not enter that cycle's carrier sample. Finite source
allowances are debited only when the entire proposal commits, including when
the emitter moves in that commit. Emission occurs once per completed local
cycle, so its interval increases under load.

Later field arrivals finish their existing transit and optional decay before
entering fixed destination-owned input registers. They are excluded from the
frozen proposal. Registers combine arrivals componentwise into eight octants
per field and retain six port readings. There is no list of waiting packets,
per-source history or unbounded computation-debt queue. Bounded receipt counts
and completed decay costs are charged in the next cycle.
Carrier inputs use free record slots; captured slots stay reserved.

NodeState retains octant totals; configured LocalRules read aggregate retained
field values and six port totals, including opposite-port contributions whose
scalar sum is zero.
These projections do not preserve a packet's octant-to-port identity or the
arrival-tick groups accumulated during a wait. Rules requiring exact simultaneous
packet identity need a separately specified bounded interface.

At ready time, validate the complete proposal and reserve its event capacity
before changing either owner. Commit the retained fields, carrier updates,
source allowances and directional departures together. Merge later input into
the retained field for the next cycle. Outgoing packets start their full h-tick
transit at this actual commit. Integer overflow and capacity exhaustion stop
the run; input is never silently dropped.

Merging is physical computation. For each of the eight population components
per field, reserve two reads, one evaluation and one update at cycle start.
The merge executes with zero operands when no later input exists. With unit
prices this adds 32 for a scalar field, or 96 for a three-component field.
Later arrivals cannot change that fixed reservation or ready time.

## Accounting, events and limits

Inventory includes original waiting stock, actual transit and buffered input
once each. Prepared proposals are not additional owners. Declared joint
invariants are checked before scheduling and, when later input exists, against
the cached pre-joint state plus that input before commit.

Additive merging does not generally conserve squared amplitude or a declared
nonlinear energy. The passive conservation audit can detect a failure after an
actual owner change; it cannot repair it. Linear inventory tests do not prove
universal energy/momentum conservation or a gravitational effect.

The optional classical causal graph records the shared `cycle_started` with C
once, followed by the actual field cycle and sends at commit. Buffered arrivals
are causes of the later commit, not of its earlier frozen sample. Receipt port
diagnostics report only that arrival's contribution. Graph capacity remains
explicit and bounded; turning it off does not change the physics.

An optional [local observer](LOCAL_OBSERVER.md) counts completed shared cycles
at its node, including field-only cycles. It records arrivals during a wait
at the current completed-cycle count; empty input does not advance that clock.

Snapshots expose `pending` and separate `incoming` spatial registers in this
mode. Run metadata identifies the shared clock and variable emission schedule.
The state remains formula-free; laws stay in immutable initialization.

## Contract ownership and evidence

Local shared-cycle preparation and commit belong to `core/disturbance_node.py`;
field proposals, receipt owners and commit preparation belong to
`core/spatial_node.py`. The engines route clock notices and adjacent delivery. Generic
field and carrier laws retain their existing owners. The new state has fixed
size for fixed fields, components and record capacity.

Focused tests (`tests/test_spatial_computation_delay.py` (deleted on 2026-09-17), deleted on 2026-09-17) cover budget
boundaries, real scalar/vector operation costs, one/two-tick transit, continuous
input with empty intervals, delayed moving emitters, finite budgets, nonlinear
guards, atomic event-capacity failures, formula-free state, passive conservation,
and graph/default-off controls. This candidate changes timing, not the
configured field transformation or a particle's physical identity.
