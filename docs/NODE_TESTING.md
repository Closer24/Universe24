# Node inputs, outputs and clocks

## Node-owned execution

The executing classes in `core/disturbance_node.py` and `core/spatial_node.py`
own local sampling, planning, validation, reception and commits. They extend
the slotted state schemas without retaining a world, graph, law definition or
callback. Shared run services provide seed-free definitions, generic laws and
write-side accounting. The optional quantum resolver remains explicit; the
node-facing definition does not contain its serialized event program.

The scheduler sends `advance` clock notices and transports packets. Carrier
open notices may begin work and finish it; closing notices only finish earlier
work, including when no packet arrives. It does not call the node's private
begin/commit methods. Spatial and carrier components can cooperate only at the
same address. Reception checks the destination and exact arrival tick again,
so a misdispatched batch fails at the node boundary. The transport releases
sender slots before receipt acknowledgment invokes causal recording or observers.
A later recording failure stops the run without duplicating physical inventory.

Each node's output bank contains only its fixed local slots. The transport keeps
the address index and shares that same bank; it does not duplicate the packets.
Carrier output has D*K slots. Existing custom planners may direct all of those
slots to one port, so a receiving batch is bounded by D*D*K, not D*K. Spatial
batches have at most D packets. The ordinary law still receives only immutable
local payloads and samples. These are bug-prevention boundaries, not protection
against hostile Python reflection or private-attribute mutation.

`NodeView.h` exposes D bounded integers: the **last planned extra local carrier
wait** for each configured port. Initially all entries are zero. The existing
whole-cycle timing law gives every port the same extra wait; for cost 21,
budget 10 and link time 3 the vector is `(6, 6, 6, 6, 6, 6)`, the proposal
commits at tick 6, and sent packets arrive at tick 9. It is not a countdown or
the link transit time. It remains readable while later clock notices complete
that cycle. Independent per-port delays are not implemented by this refactor.

The existing `cost_field` reports operation cost C, and configured emissions
and responses can couple that property to a local field. Naming the wait `h`
does not redefine C or supply a field-to-computation response law. A reduction
of modeled work, delay or host CPU cost needs a separately specified mechanism;
no sign, gain or threshold is inferred here. Spatial forwarding retains its
existing fixed cadence.

## Local input and output protection

`core/node_boundary.py` validates local provider results before the scheduler
retains proposals or commits payloads. Laws receive immutable local records,
residuals and received samples, not a world mapping or an event graph. Departures
select a local port; the scheduler computes its neighbor. No per-node process,
world copy, persistent validation cache or new physical law is introduced.

The runtime rejects mutable containers, foreign objects, invalid field shapes,
invalid or repeated replacement slots, invalid departure ports and malformed
spatial proposals. Receipt checks packet origin against the actual link owner;
spatial receipt also checks its port. A record policy cannot overwrite a slot
locked by a pending proposal. Sampling, decay and reaction providers use the same
immutable shape checks. Sample changes are retained only after successful local
planning. Invalid local output does not become a pending result or transmission.

An exact immutable resident record already validated by the engine may be reused
by identity. New records still receive full validation. This avoids repeated
scanning without retaining a cache. Physical checks and declared conservation
laws remain with their existing owners; validation adds no model operations or
world ticks, but consumes host time.

`tests/test_node_boundary.py` exercises faulty providers and foreign provenance,
input mutation attempts, hidden world/graph access, pending-slot protection and
unchanged local results when remote state differs. Existing port and relay tests
retain the actual link-delay and configured-degree contracts.

This protects ordinary provider mistakes, not hostile Python with closures,
reflection or deliberate writes to private engine attributes. The static gate
rejects known world/graph accesses and imports in calculation layers; it is not
a proof for arbitrary dynamic code. The explicitly configured quantum resolver
still owns Past is Present Calc and receives a local request context, while
ordinary laws receive no graph reference. Completed independent events need not
roll back when a later event fails; implicit empty-node allocation is host state.

## Observing actual transitions

`NodeProbe` observes selected nodes while advancing the ordinary `Simulation`.
It does not contain another simulator, inject fabricated arrivals, or change
configured physical laws. Seed real neighboring nodes in initialization and
inspect the actual deliveries and commits. The implementation is
[diagnostics/node_probe.py](../src/event_universe/diagnostics/node_probe.py).

## Run the three-node relay

From a checkout with the project installed, validate and run the one shared
[initialization file](../examples/node-clock/three_nodes.json):

```bash
python -m event_universe.configuration_validation examples/node-clock/three_nodes.json
python -m event_universe --init examples/node-clock/three_nodes.json --output artifacts/node-clock
python -m pytest tests/test_node_example.py tests/test_node_probe.py -q
```

The output directory must be empty. The runner writes the copied initialization,
run metadata, final state and actual events; this command is headless.

The example has a periodic 5 by 1 by 1 domain, the default six ports, one slot
per node, and a parcel carrying integer inventory 7 through +X. Three successive
nodes send at audit ticks 0, 3 and 6; their links deliver at ticks 3, 6 and 9.
The parcel is at coordinates (1,0,0), (2,0,0) and (3,0,0) at those arrivals.
Resident and in-flight inventory together remain 7. The extra domain sites let
the test distinguish a real relay from a periodic self-link.

```python
from pathlib import Path

from event_universe.diagnostics.node_probe import NodeProbe
from event_universe.initialization import load_initial_state

initial = load_initial_state(Path("examples/node-clock/three_nodes.json"))
with NodeProbe(initial, [(0, 0, 0), (1, 0, 0), (2, 0, 0)]) as probe:
    for _ in range(initial.ticks):
        transition = probe.step()
        for event in transition.events:
            print(event.audit_tick, event.position, event.direction, event.port, event.values)
```

## Physical phases and three different counters

The phase owner is
[core/disturbance_engine.py](../src/event_universe/core/disturbance_engine.py).
Each `step()` begins eligible spatial field phases at the current audit tick,
then begins eligible carrier proposals and commits ready proposals. It advances
the audit tick by one, delivers due spatial packets and carrier packets, and
commits previously pending carrier proposals that are now ready. An explicitly
configured event resolver advances afterward. Spatial field phases begin only
on their configured link interval.

A carrier proposal reads frozen local inputs. Later arrivals do not enter that
already planned computation. Validation precedes the local ownership commit;
an invalid proposal does not partly overwrite its records or links. Earlier
independent commits remain completed. An arrival cannot traverse a second link
without that link's own positive transit interval.

| Observation | Meaning |
| --- | --- |
| `audit_tick`, transition `start_tick` and `end_tick` | Host-visible scheduler coordinate for physical event order |
| `NodeSample.clock` | Completed carrier cycles observed at this selected node |
| `NodeSample.spatial_cycles` | Completed spatial field phases observed at this selected node |

An empty, waiting or newly receiving node need not advance its carrier clock.
An arrival alone increments neither completion counter. These counters are
diagnostics, not a new physical register, proper time, or a law for spacetime.
For the relay, after tick 3 the three carrier clocks are (1,0,0), after tick 6
they are (1,1,0), and after tick 9 they are (1,1,1).

## Ports and local orientation

Omitting `topology` selects `[+X, -X, +Y, -Y, +Z, -Z]`. An explicit topology
selects one immutable ordered reciprocal list for the entire run, with an even
number of ports from 2 through 26. Nodes do not choose different port counts.
A count alone does not specify the neighbors: supply offsets and any site
pattern under the [configured topology contract](CONFIGURED_TOPOLOGY.md).
Configured topologies reject aliased or self-linked periodic destinations;
the unchanged default allows tiny periodic domains, including the one-node test.

`NodePortEvent` reports both ends explicitly:

| Member | Meaning |
| --- | --- |
| `position`, `port` | Selected node and its local output or input side |
| `source`, `target` | Actual endpoint addresses; an open boundary can have no target |
| `travel_port` | Sender's chosen output direction |
| `receiver_port` | Configured reciprocal of that direction |
| `event`, `event_port` | Original engine event and its raw port, when present |
| `audit_tick`, `arrival_tick` | Observed event tick and completed or scheduled delivery tick |
| `values` | Named decoded integer scalar/vector components, copied for observation |

For a default +X transfer, output port is 0 and input port is 1. A reordered
topology uses its declared reciprocal, so do not compute the inverse with an
assumed adjacent pair. Raw carrier `received.port` and spatial
`spatial_received.received_fields` already use receiver sides. Spatial
`spatial_values(...)[field]["directions"]` retains the existing travel-index
convention; the probe does not rewrite stored physical state. A batched spatial
reception has no single raw `event_port`, so that member is `None`.
Vector components remain three-dimensional; the eight spatial population bins
are also independent of the number of neighbor ports.

## State names and bounded observation

The canonical physical owners are `DisturbanceNode` and `SpatialNode`.
`NodeView` is the immutable carrier view; `NodeSnapshot` combines the local
carrier and spatial views with outgoing packets. `world.node_view(position)`
looks up only that address, without creating state or copying the world.
`None` means that lane has no materialized owner; implicit spatial baselines
remain in initialization. `world.nodes` exposes the carrier mapping.

Use `slots_per_node` in new JSON, with an integer capacity from 1 through 32.
Old `slots_per_cell` JSON remains accepted by the same parser, and
`InitialState.slots_per_cell` remains a read property. Supplying both names is
rejected even if they agree. `DisturbanceCell`, `SpatialCell` and `CellView`
remain class aliases; `.cells` remains a compatibility accessor. These names
do not create parallel owners. Existing serialized snapshots keep the `cells`
wire key for consumers. See [memory ownership](MEMORY.md) for lookup costs.
Direct Python `InitialState` construction uses `slots_per_node`; the old name is
a JSON/read compatibility alias, not an alternative constructor keyword.

A probe selects 1 through 64 distinct valid nodes. `max_events` defaults to
4096 and accepts 1 through 65536. It retains one latest immutable transition
and one bounded active event batch, not the whole run. Returned snapshots share
immutable payload references and remain stable after later commits. Callers
that save every transition own that additional history.

An event batch exceeding the remaining diagnostic capacity fails before any
part of that batch is archived. Physical receipt may already have committed;
diagnostic failure is not a physical rollback. `last_transition` records the
completed prefix and bounded error text before the error propagates. A failed
post-step snapshot uses separate `snapshot_error_*` fields and does not replace
an earlier engine or observer exception. Direct `probe.world.step()` calls
update completion counters but do not extend retained transition history.
Close the probe or use its context manager.

## Acceptance coverage

- [Node behavior tests](../tests/test_node_probe.py): distinct signed scalar and
  vector payloads on all 2/6/8 ports, reordered reciprocal indices, real 1/3-tick
  links, one periodic node, multiple nodes, frozen waiting, invalid-output
  atomicity, diagnostic errors and bounded history.
- [Runnable relay test](../tests/test_node_example.py): independent 3/6/9 arrival
  expectations and inventory 7 from the same example file used by the runner.
- [Node integration](../tests/test_node_integration.py) and
  [node contract](../tests/test_node_contract.py): current naming/capacity
  compatibility, actual owners and high-port composition.
- [Memory tests](../tests/test_node_memory.py): point-only reads, immutable
  sharing, maximum widths, released history and callback lifetime.

These are real single-process engine tests. Different world embeddings check
local behavior; they do not establish a distributed runtime or partitioned
execution equivalence. Generic transport and declared inventory accounting do
not establish a physical force, energy definition or particle model.
