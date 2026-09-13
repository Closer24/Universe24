# Memory ownership in the active engine

The active `Simulation` composes the carrier scheduler and optional spatial
field scheduler. Both use ordinary Python dictionaries and immutable tuple
payloads. This document describes the implemented owners, not a packed-array,
worker-process or distributed backend. General boundaries remain in
[ARCHITECTURE.md](ARCHITECTURE.md); the local observation API is in
[NODE_TESTING.md](NODE_TESTING.md).

## Immutable definitions and evolving owners

`InitialState` owns the parsed field/type definitions, configured expression
trees, operation prices and topology. The world and composed law providers
reference these immutable definitions. Nodes, records, pending plans and
packets contain bounded values and identifiers, without copied expressions,
formula strings or executable callbacks. The structural
[node state audit](../src/event_universe/diagnostics/node_contract.py) checks
the reachable state graph; it does not prove the physical meaning of a law.

| Owner | Retained state |
| --- | --- |
| Carrier `_nodes[position]` | One `DisturbanceNode`: fixed record tuple, coupling remainders, at most one pending cycle, availability and bounded bookkeeping |
| Carrier `_links[origin]` | Fixed tuple of outgoing packet slots, each holding at most one immutable `Packet` |
| Spatial `nodes[position]` | One `SpatialNode`: immutable field states, bounded sampled inputs, reaction phases and bookkeeping |
| Spatial `links[origin]` | One outgoing `SpatialPacket` slot per configured port |
| Spatial `_active` | Host scheduling index of addresses; physical registers remain in spatial nodes |
| Accounting ledgers | Separate source, reaction, transformation, dissipation and escape totals where applicable |

For fixed resident capacity K, port degree D, field count and rule count, each
local owner's size is bounded independently of the world shape. Currently K
is at most 32, D at most 26, and fields/types at most 16 each. Carrier outgoing
storage has D*K slots. Each spatial field retains eight populations, eight
allocation-phase payloads and D delivered channels. Scalar payloads have one
component; vector payloads have three. Pair-coupling remainder storage depends
on the configured rule count and K squared, so bounded does not mean small.

A pending cycle retains a frozen proposed result while the original records
still own the physical inventory. The proposal is not another inventory owner.
At a validated commit, ownership moves into replacements and outgoing packets.
Packets remain link-owned until complete delivery or escape. Delivered spatial
samples are projections of received inventory, not additional stock. Read-only
inventory diagnostics count actual owners, not pending proposals or samples.

The physical schemas use slotted records, but values are still Python objects
and tuples, not contiguous native numeric arrays. Model integer bounds are
enforced separately from Python's integer representation. A payload reference
and a fresh tuple each have host memory costs even when local capacities are
fixed. No constant whole-run byte bound follows from the local schema.

## Passive point views

The [local I/O boundary](NODE_TESTING.md#local-input-and-output-protection)
validates bounded records and proposals without retaining another owner. Its
temporary replacement-slot set is limited to K. It shares already validated
immutable resident records by identity and retains no validation history or
global cache. Bounds depend on configured slots, fields, rules and ports, not
world size. Validation consumes host time without changing model costs.

`world.node_view(position)` validates an address and performs point lookups in
the carrier/spatial node and outgoing-link dictionaries. It constructs small
immutable view wrappers and shares immutable records, pending plans, field
states and packet tuples. It neither invokes materialization nor iterates
unrelated nodes. Missing lanes return `None`; implicit spatial baselines and
type definitions stay in initialization. Empty outgoing tuples are shared by
the corresponding engine instead of rebuilt for each missing-node lookup.

Old snapshots stay readable after commits replace the current tuples. Holding
such snapshots also retains their referenced old payloads until the caller
releases them. This is deliberate immutable sharing, not zero memory cost.

`world.nodes` has a different cost: it constructs an immutable mapping of
carrier views across the materialized carrier nodes. The `.cells` compatibility
accessor delegates to it; it is not a second store. Full `snapshot()`, totals
and `inventory_view()` are world-scale diagnostic operations. Prefer
`node_view()` when only a few positions are needed.

The canonical classes are `DisturbanceNode`, `SpatialNode` and `NodeView`;
legacy class names are aliases. `slots_per_node` is the sole stored capacity.
The old JSON name and read property `slots_per_cell` share that owner, with
dual-name inputs rejected. Serialized snapshots retain their `cells` key.

## Probe, host and history limits

`NodeProbe` keeps counters for at most 64 selected positions, the latest
`NodeTransition`, and a bounded active list of events. The default event limit
is 4096 and the maximum is 65536. Each event holds bounded named integer data.
Completed transitions keep exception class names and messages rather than
exception objects or traceback graphs; messages are capped at 4096 characters. The active list
is cleared after success or failure. Observers and callers remain responsible
for any additional retained data; saving all transitions grows history.

The ordinary engine's host containers scale with the materialized world.
Visited carrier/spatial node dictionaries are not a constant-size arena, and
link rows can remain after their packets depart. Carrier stepping scans and
sorts materialized nodes; packet delivery groups due transfers, and the spatial
scheduler maintains an active-address set. These host costs must be measured
separately from the configured local operation cost and link timing. A point
view does not remove these world-scale scheduler costs.

Global audits, selected native causal/quantum state, archived observations,
runner event files and optional playback frames have their own lifetimes and
limits. They are not certified as constant-space by the node-local contract.
The headless runner streams events to disk; optional visualization retains
frames. Whole-run disk output can grow with duration. See the separate
[retention contract](RETENTION.md), [native event contract](NATIVE_QUANTUM_EVENTS.md)
and [local observer contract](LOCAL_OBSERVER.md).

## Permanent checks and remaining scope

For every change, review system dependencies and the owner, capacity and lifetime
of affected state. The submission selector always includes architecture and
node-memory tests. If allocations or ownership change, measure representative
empty, active and maximum-capacity cases with the same parsed input and tick
count. Identify the source fingerprint and separate creation, steady stepping,
retained history and failure cleanup. Verify physical states/events separately;
tracing overhead and host timing are not model operation costs. Documentation
changes can reuse unchanged implementation evidence, with that scope stated.

[test_node_memory.py](../tests/test_node_memory.py) forbids whole-world
iteration and materialization during point inspection, exercises K=32/D=26,
checks reference sharing for live packets and default buffers, releases 80
successive probe transitions, and verifies that an observer exception does not
retain callback frames. These are deterministic ownership and lifetime checks,
not a process RSS benchmark.

[test_node_probe.py](../tests/test_node_probe.py) checks bounded event/selection
capacity, immutable snapshots, latest-transition retention and failure prefixes.
[test_node_contract.py](../tests/test_node_contract.py) checks canonical capacity
and legacy access. [test_node_integration.py](../tests/test_node_integration.py)
checks the evolving state contract through real high-port runs. Existing
[spatial scheduling tests](../tests/test_spatial_scheduling.py) compare the
active-address optimization with ordinary full-sweep behavior.

The measurements apply to these owners and test scenarios. Arbitrary world
growth, external observers, retained run histories and optional global quantum
representations require separate memory budgets. Passing local tests does not
establish distributed partition behavior or a fixed total process footprint.
