# Local Focus scheduling

Local Focus skips certified empty carrier Nodes by default. Omitted `focus`
means `true` in JSON and in the typed initialization interface. Set
`"focus": false` explicitly for the reference scheduler; only actual booleans
are accepted. Unsupported compositions still fall back automatically.
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
replicated, and no per-ray or per-source cache is introduced. Sparse moving-carrier
worlds benefit as their empty trail grows; a dense world or a pure-ray world may
show little improvement. Wall time and peak host memory must be measured separately
from model cost on the actual machine and input.
