# Local Focus scheduling and transition reuse

Local Focus is enabled by default in both ordinary initialization JSON and the
Python InitialState interface. Set `"focus": false` to opt out. Only actual
booleans are accepted. Focus skips certified empty carrier Nodes and reuses
pure local transition calculations when every input is exactly equal.
This host optimization is separate from `quantum/focus.py`, the existing
Q-ORACLE option, physical LocalRules and configured interaction durations.

Spatial transport already maintains an active-Node index without this option.
Local Focus adds a carrier index; it does not replace the ordinary baseline
with an artificial full-world scan. It never jumps a ray across several Links.
Pace, computation delay, phase, decay, absorption and claim propagation still
execute at their existing local boundaries.

## Eligibility and wake contract

`DisturbanceNode.can_sleep` inspects only its own fixed payload and immutable
services. Every occupied record and every pending cycle stays awake. A Node
may sleep only when no record exists, no pending cycle exists, no delay counter
still needs clearing, and the configured pure record policy reports no work.
Actual creation and completed Link delivery wake its address before the closing
commit phase. Retained NodeState and in-transit ownership are never deleted.

An event resolver or shared field computation clock retains the ordinary
scheduler because it can own autonomous work. `execution_report()` reports the
requested flag, effective flag and fallback reason. It also reports
`carrier_phase_visits` and `awake_carrier_nodes` as host measurements, separate
from modeled operation cost. Nonempty inactive records are deliberately retained
in the first implementation's active set.

## Repeated local behavior

`core/plan_reuse.py` holds a bounded host cache for each certified pure planner.
The canonical Simulation enables carrier reuse and, when no mutable bond registry
is present, spatial reuse. Event resolvers bypass both caches. Low-level custom
DisturbanceEngine planners are not assumed pure; their reuse flags default off.
The empty-carrier scheduler fallback and planner reuse are separate decisions:
shared field clocks keep the ordinary carrier schedule but can reuse pure plans.

Equality means the complete immutable planning input, not equal output on the
previous tick. Carrier keys include every record field (including residuals and
phase), coupling remainders, arrival count and directional loads. Spatial keys
also include field state, rays, claims, local computation cost, the tick and
ray-hold mode. Each cache belongs to one law/configuration in one simulation;
results cannot leak across configurations. Hash matches still require full key
equality. Exceptions are never cached. Pending proposals are immutable.

Equivalent Nodes compute one plan and independently commit it at their existing
local boundaries. Repeated parallel requests are evaluated once per distinct
input and restored to their original request order. Every Node still charges
its original model cost, executes validation, retains ownership and emits its
own events. A cache hit saves host work, never a modeled operation or world tick.

Each planner cache retains at most 4096 entries with least-recently-used eviction.
This is a host memory limit, not a physical parameter. `execution_report()` gives
requests, actual evaluations, hits, capacity and retained entries independently
for carrier and spatial plans. Closing the simulation releases cached entries.

A repeated multi-Node pattern can reuse its component local plans. Collapsing an
interacting region into a supercell with a multi-tick transition is not implemented:
it additionally requires the entire interior state, boundary input sequence,
phase alignment and exact intermediate event/ownership semantics. Merely having
the same recent output does not certify such a region. No tick or Link is skipped.

## Active transport banks

Both transport engines index banks that actually contain packets. After each
local transition the host refreshes only the touched output banks; Nodes retain
only their original fixed PortBank payload and receive no host index or callback.
Direct writes through PortTable update its index immediately. Delivery snapshots
active addresses in original bank-creation order, preserving reactivation order
and simultaneous delivery/error behavior. Future packets remain indexed and are
still delivered only at their declared arrival tick.

Public mapping iteration keeps visible empty banks, so inventories and snapshots
retain their previous format and order. Transport alone uses `active_items()`.
The index costs O(A) active membership plus O(H) stable ordering metadata for H
retained banks. A delivery pass sorts A active banks, not historical empty banks.
Carrier and spatial transport visit counts appear separately in execution reports.

## Equivalence argument and limits

Assume the documented pure LocalRules and record policies, immutable proposals,
and Node-owned mutations. At an equal tick boundary, each omitted carrier visit
has no pending commit and no eligible begin, so its physical transition is the
identity. Real deliveries retain the same sorted order and wake every receiving
owner. The remaining visits use the same snapshots, clocks and plans. Induction
therefore preserves NodeState, packets, event order and model cost across completed
ticks. Capacity and arithmetic errors retain their ordinary handling; custom
Python code that mutates another Node violates the premise and is not sandboxed.

[The focused tests](../tests/test_local_focus.py) compare complete inventories,
snapshots, costs and ordered events at every tick. They cover all six Ports,
periodic revisits, pending delays, parallel workers, ray transport, loaded phased
rays, field reactions, finite decay, fallback paths and capacity failure.
Finite examples support the stated scheduler argument; they do not prove a
real-world physical law or every unreviewed plugin composition.

## Memory and host cost

The host set retains at most one address per active carrier Node. Its storage is
O(A), while each sleep decision remains bounded for fixed local capacity K.
The tick driver still sorts active addresses, routes actual packets and performs
existing field work. It is not O(1) for the whole world. Retained history is not
replicated. Transition caches have the fixed entry bounds above, not one cache
per ray or source. Sparse moving-carrier
worlds benefit as their empty trail grows; a dense world or a pure-ray world may
show little improvement. Wall time and peak host memory must be measured separately
from model cost on the actual machine and input.
