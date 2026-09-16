# Whole-property packet and local reservoir benchmark

This is a configuration of the active generic engine, based on main
`e5b5911ab13373e08345cf971a6ae8d7e9cb462e`. It exercises one whole record in
a periodic 6 by 6 by 6 world. The record carries inventory, signed charge,
an energy-like ledger, a vector called momentum, routing direction, phase
metadata and a participation property. The engine does not interpret these
names as particle species or physical equations.

The packet starts at Node `(0, 2, 2)` and routes through `+X`. A finite local
reservoir at `(2, 2, 2)` participates through the supported property-based
`requires` selector. One joint transaction reads the frozen carrier and local
field values and declares these exact changes:

| Quantity | Carrier before | Reservoir before | Carrier after | Reservoir after |
| --- | --- | --- | --- | --- |
| Energy-like ledger | 2 | 5 | 3 | 4 |
| Momentum vector | (1, 0, 0) | (0, 0, 0) | (1, 2, 0) | (0, -2, 0) |

Inventory stays 1, charge stays -1 and phase metadata stays 3 on the whole
packet. Its direction stays `+X`: this isolates property transport and is not
a force law relating the vector to velocity. The local rule's `k=1` waits one
tick before atomic commit; the next Link takes another tick. The carrier reaches
the reservoir at tick 2, commits at tick 3, and reaches the next Node at tick 4.
The activation condition stops further transfer after the carrier ledger reaches
3, including after periodic wrap. This condition and the exchange values are
explicit engineering test choices, not derived physics.

Run from the repository root using the project Python 3.14 environment:

```sh
PYTHONPATH=src python examples/property_packet/run_benchmark.py --case exchange --output artifacts/property-packet-exchange
```

Choose a fresh output directory. The existing runner and HTML generator write
the exact input, event trace, metadata, final state and playback. The wrapper adds
read-only per-frame ownership observations; it does not update the simulation.
An immutable source fingerprint identifies the actual imported tree.

The five controls are `exchange`, `zero_coupling`, `missing_property`, `renamed`
and `reordered`. Zero coupling and the missing participation property preserve
the initial reservoir and carrier ledgers. Renaming all physical field/type labels
and reversing independent declarations preserve the exchange. Missing-property
control keeps an unseeded compatible layout so the selector remains a valid
schema declaration; only the actually seeded unresponsive record is excluded.

`tests/test_property_packet_benchmark.py` checks every recorded frame: exactly
one actual carrier owner, unchanged metadata, componentwise ledger totals,
simultaneous two-owner exchange and periodic traversal. Every test run generates
HTML with the existing generator. On the recorded base, all five controls passed
for 18 ticks; every frame retained the declared inventory, charge and vector sums.

This does not establish an electron, phase evolution, an electromagnetic field,
physical energy, or empirical agreement. The separate experimental Port scheduler
currently rejects spatial-field inputs, so this reservoir case runs through the
ordinary Node scheduler. A passing configuration does not establish a new physical interaction law.
The Node is the active state and interaction unit; no private-register migration
is required.

Contracts: [whole-record transport](../../docs/DISTURBANCES.md),
[joint local transactions](../../docs/LOCAL_FIELD_RULES.md), and
[Node execution timing](../../docs/NODE_VECTOR_PROCESSOR.md).
