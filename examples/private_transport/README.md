# Private Register identity transport

This explicit engineering profile executes 24 independent private Registers in
each of 216 Nodes. A Node is only a spatial grouping and container. Every Register
has one input channel, one output channel and its own fixed private state. The
same pure identity law receives only that private state and an actual delivered
datum. It receives no Node, address, clock, peer state, callback or shared snapshot.

The ordinary whole-Node engine and the interim Port adapter in PR140 are separate
earlier references. Neither is used as the physical evaluator in this experiment.
The dense and sparse strategies here run the **same private graph and local law**.
Dense selection visits all 5,184 Registers each tick; sparse selection visits only
Registers with actual inputs. Selection never changes a physical value or delay.

## Explicit test graph and clock

[input.json](input.json) supplies every one of the 24 repeated directed channel
templates. The periodic world is 6 by 6 by 6. With signed cardinal directions
`p` and `q`, the supplied mapping is `T(n,p,q) = (n+q, -q, p)`, with coordinates
wrapped periodically and orthogonal `p,q`. It is bijective, and four transfers
return to the original Register. This configured square loop is an engineering
fixture. It does not establish a universal ray law or resolve straight/return
propagation for other experiments.

Every Link spans one lattice unit and takes one model tick; local waiting is
explicitly zero. Thus this fixture has `c_model = 1 lattice unit / tick`, without
an SI calibration. A seed processed at tick 0 owns an outgoing channel due at
tick 1. The recipient can process it at tick 1 and produce a channel due at tick
2. No unit can cascade through another physical Link within the same tick.
Snapshot tick 1 therefore contains the channel due at 1, before that receipt's
tick-1 processing. Dense and sparse share this convention.

The seed is one present datum containing encoded numerical zero (`codes: [1]`).
Only absence means idle. Components use the existing positive signed-integer
encoding and remain opaque here. They are not claims about physical momentum,
phase, charge, mass or energy. Identity transport moves the one datum owner from
an input to a channel, then to the recipient. Queue entries contain handles.
There is no per-source history in a Register and no copied physical inventory.
One input and one outgoing channel per Register are fixed capacities. Admission,
colliding receipt and unsupported configuration failures reject before consuming
existing owners; they never overwrite, silently drop or arbitrarily serialize.

## Reproduction and acceptance

```sh
PYTHONPATH=src python examples/private_transport/compare.py \
  --input examples/private_transport/input.json --source . \
  --output artifacts/private-comparison --repeats 3
```

This uses the active `src/event_universe/core/private_*` modules. The input is
an explicit private transport profile, not the ordinary initialization schema.
The loader rejects unsupported keys, rules, local waits and Link durations.
All physics remains the one private identity operation; wiring is input data.

The comparison records complete private state, input owners, channel owners,
destinations, payloads, due ticks and ordered events at every tick. Equal final
positions alone do not pass. Expected four-hop positions are independent frozen
test values; graph tests also check the inverse on all 5,184 units. Empty-world,
present-zero, invalid-wiring and capacity-rejection controls are included.

Every explicit run uses the existing HTML generator with a passive projection of
actual input/channel owners. Global observations never become Register inputs.
The generic playback displays the opaque datum's decoded components and actual
Link direction; it does not display an inferred particle or quantum state.

Initialization, stepping and HTML export have separate timers. Three fresh pairs
alternate execution order. A fourth pair separately measures peak traced Python
allocations, including initialization and passive audit/frame capture but excluding
HTML; those instrumented timings are excluded from the timing medians. Allocation
tracing does not measure all process or native-library memory. Fixed model slots,
active channel owners and due handles are reported separately. Unbounded event
history and complete snapshots belong only to the external diagnostic recorder.

## Recorded result

On Python 3.14.7, source fingerprint
`7645db6f860d891e562b42f72c8a72aec66cce99a8f7e6bc585f6ebb02c2e219`,
all four pairs matched all 13 recorded ticks and produced eight HTML files.

| Strategy | Median stepping, 12 ticks | Register checks | Nonempty transitions |
| --- | ---: | ---: | ---: |
| Dense Node batch | 6.44 ms | 62,208 | 12 |
| Sparse Register worklist | 0.323 ms | 12 | 12 |

The separate allocation run peaked at 4,237,896 traced Python bytes for dense
execution and 3,373,596 for sparse execution, within the measurement scope above.
Both retained exactly one channel owner and one future arrival handle. The
composed affected gate passed Ruff, strict mypy for four modules and 648 tests;
two existing opt-in movie tests were skipped. Embedded playback data was checked
for 13 frames and exactly one owner per frame. Browser layout and interaction
were not verified.

The sparse strategy was faster in this deliberately sparse identity fixture.
This result does not establish a speedup for populated fields or interactions.
The experiment implements private transport architecture; it does not yet implement
wave mixing, couplings, delay/mass laws, detectors, Bell tests or a physical species.
