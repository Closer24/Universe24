# Generic nodes and shared links

`universe24.core.network` provides a construction/readout layer over the
existing periodic cubic lattice, fixed tensor and complete `State`. It does
not add an evolution mode. Only `Engine.step` advances any node or link field.

Every node has six incident links in the order `+x,-x,+y,-y,+z,-z`. Each
undirected link is an independent entity with one shared state. Its positive-axis
base supplies a canonical array address, not ownership by that node. Each array
cell stores three links and a node views three more at its negative neighbors.
This convention also applies at periodic seams. With `N=L^3`
nodes there are exactly `3*N` links, not `6*N` independently evolving copies.

`node.faces` exposes six immutable `FacePort` views. For any view `face`,
`face.peer.peer == face` and `face.peer.link == face.link`. A face port is a
node's oriented interface, not an extra topology node, state allocation or
actor. A caller may allocate port registers to the node and shared processing
registers to the interface through the existing `NetworkLayout` fields.
See [the coupled face processor](FACE_PROCESSOR_MODEL.md) for a counted
25-channel example with one tensor, traffic feedback and real passage stages.
The axis names are graph addresses, not claims about physical angles.

## Objects and retained state

| Object | Responsibility | Retained physical state |
| --- | --- | --- |
| `CubicNetwork(L)` | Existing periodic topology, node/link enumeration | None |
| `Node(network, index)` | Six incident addresses and neighbors | None |
| `Link(network, storage_node, axis)` | Independent edge identity and two endpoints; storage address only | None |
| `NetworkLayout(node_fields, link_fields)` | Explicit channel names, allocation, factor templates and ownership manifest | None |
| `State` | Complete arrays of shape `(channels, L**3)` | All `a,b,r` values, including links |
| `NetworkSnapshot` | Reads complete triples from the supplied snapshot | None added; rebind after each Engine step |

Node/Link handles are immutable values. Equality identifies the same edge;
Python object identity is not a state-sharing mechanism. Equal-size networks
use the same topology address space, while the snapshot selects the actual run
state. Snapshot getters return immutable integer triples, never writable array
views. The caller must not mutate the underlying State while observing it.

Each node field costs one channel. Each generic link field costs three channels
per array cell, one for each stored axis:

```
channels = number_of_node_fields + 3 * number_of_link_fields <= 48
retained_integers_per_node = 3 * channels
```

For example, one node `signal` field and one link `length` field use four
channels and twelve retained integers per node. Both ends see the same
complete `(a,b,r)` for a shared link. There is no extra edge-state bank.

Both endpoints can contribute to the link's next state. A fixed polynomial
reads the old link and both old endpoint states, then Engine applies Rule3 once.
This is a synchronous shared interaction, not two sequential writers and not
permission for either endpoint to overwrite the other. The manifest's `owner`
field identifies the channel component (`network.links.x`, etc.), not a node
that physically owns an edge.

## Minimal use

```python
from universe24.core import Engine, NetworkLayout
from universe24.observe.network import link_length, static_crossing_time

layout = NetworkLayout(node_fields=("signal",), link_fields=("length",))

# Explicit demonstration law: inertial registers. Equal a,b remain constant.
# This example does not transport signals or supply a gravitational law.
tensor = layout.tensor([
    (gear.name, 6, ((gear.name, (0, 0, 0), "b"),))
    for gear in layout.gears
])
seed = layout.uniform_state(
    3,
    nodes={"signal": (0, 0, 4)},
    links={"length": ((2, 2, 1), (3, 3, 2), (4, 4, 5))},
)
snapshot = layout.bind(tensor, seed)
node = snapshot.network.node(0)
edge = node.link(0)  # +x
assert len(node.links) == 6
assert edge == node.neighbour(0).link(1)  # same link from the other end
assert snapshot.link_value(edge, "length") == (2, 2, 1)
assert link_length(snapshot, edge) == 2
assert static_crossing_time(snapshot, edge, c=1) == 2

after = Engine(tensor).step(seed)
next_snapshot = layout.bind(tensor, after)
assert after.same_as(seed)
```

`uniform_state` requires all declared fields and all three axis triples,
including nonzero carries. It is preparation only; arbitrary nonuniform data
can be set in the returned ordinary State before the bundle is sealed.

Use `create_bundle(tensor, seed, channels=layout.manifest(), ...)` with an
explicit model and protocol, then the existing prepare/run/verify pipeline.
The tensor retains standard Yee `GearType.link` metadata. No new bundle or
trace schema is required. A loaded tensor/state can be bound using the same
layout; binding rejects different names, labels, order or link axes.

## Coupling through the tensor

`node_read(field, direction=None, history='b')` and
`link_read(direction, field, history='b')` produce ordinary tensor factors,
relative to the target's storage node. For a negative direction, `link_read`
automatically uses the neighboring owner. `a` reads remain subject to the
existing acyclic-dependency requirement; `r` is retained by the Engine and is
not an allowed tensor factor.

A monomial may involve a node, its incident link and the other endpoint.
Multiplying two incident link values on different axes is not automatically
local: their physical support includes three nodes. `layout.tensor(...)`
always enforces strict physical support, polynomial degree and inverse-order
checks. Each signal-to-link or link-to-signal coupling must be explicitly
specified in the immutable law. No callbacks or per-link update methods exist.

## Lengths and time

The optional passive readout interprets a chosen link field's current `b` as
a positive length in declared units. `static_crossing_time` computes the exact
rational `length/c` for a frozen edge. Neither function feeds back into the
Engine, schedules an arrival or interprets Engine ticks as physical time.
Nonpositive lengths are reported as outside that readout chart; the state is
not clipped, repaired or discarded. The full histories and carries remain
available through `link_value`.

The intended lengths-first research direction takes graph lengths as primitive
and derives temporal observations from actual propagation and internal clock
processes. Angles and a continuum metric would be inferred, not extra generic
node/link state. The generic infrastructure does not yet establish that its
arbitrary caller-supplied law realizes propagation at `c`, Einstein geometry,
stable waves or physical clocks.

## Executable mechanical check

```bash
python -m unittest universe24.tests.test_network -v
python -m validation.network_smoke --out runs/new-network --side 3 --steps 4
python -m universe24 verify --run runs/new-network/run
```

The source-only fixture supplies a four-channel example with both directions
of coupling: link values affect endpoint fields, and endpoint differences
affect links. Its equations are

```
u_signal(x) = 6*b_signal(x)
              + 3*sum_incident[b_length(e)*(b_signal(neighbor)-b_signal(x))]
u_length(e) = 6*b_length(e) + 3*(b_signal(right)-b_signal(left))^2
```

The standard fixed-six update applies to every channel. This deliberately
simple fixture has fast integer growth and is not a validated wave equation.
Its evidence checks shared storage, actual coupling, scalar-oracle equality,
nonzero carries, arbitrary-precision execution, saved replay and full rewind.
The theoretical static `length/c` readout is explicitly not a measured signal
arrival time in this fixture.

## Prepared delay experiment

`validation.link_propagation` now implements a separate frozen-length experiment
through the same Engine. Each independent link retains two selectors and six
payload-stage fields (three per direction). Six node ports and one reference
oscillator bring the complete allocation to31 channels. On compatible complete
histories, lengths1,2,4 produce first neighbor arrivals at1,2,4 native updates
using one immutable tensor. The two directions are fields of the same link,
not two link entities. See [the experimental report](LINK_PROPAGATION_EXPERIMENT.md)
for the tests and the negative isotropy/clock results. This does not establish
general relativity, dynamical link lengths or calibrated physical proper time.
