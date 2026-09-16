# Canonical simulation terminology

Universe24 uses the following vocabulary for its binding architecture.
The Node/Register distinction is a design definition, not a claim that the
Register-level scheduler is already implemented. See the project-wide
[binding architecture](ARCHITECTURE.md#binding-system-architecture) for required
periodic topology, scheduling and lossless arithmetic. Existing execution
contracts describe implementation; gaps do not relax the binding design.

## Core terms

| Term | Definition |
| --- | --- |
| Node | One logical unit at a physical location in Event Space. It owns one bounded NodeState and contains the directed internal Registers defined below. |
| NodeState | All local information owned by one Node, including the bounded values and metadata of its Registers. It is not a second physical object or a copy per Register. |
| Register | A directed internal computational transition between orthogonal Ports, with exactly one input channel and exactly one output channel. All Registers execute the same generic local logic; input, state, direction, configured rules and delay are data. |
| Scalar | A one-component value. |
| Vector | A three-component spatial value; wider bounded property arrays in the opt-in Node profile have their own explicit shape contract. |
| Port | One of the six external directional connection endpoints; a Port is not a Register. |
| Link | The causal connection between neighboring Nodes. It owns a transferred value during transit. |
| Event | A local state transition or a completed Link transfer. Computational substeps do not create new physical locations. |
| LocalRule | Configured generic logic operating on owned local state and already-delivered inputs; joint dependencies retain Node-level coordination and atomicity. |

The revised six-Port model contains **24 directed Registers in one Node**:

`P = {+X, -X, +Y, -Y, +Z, -Z}`
`R = {(p,q) in P x P : axis(p) != axis(q)}`

Each Port connects internally to the four orthogonal Ports: 12 unoriented pairs
or 24 directed one-input/one-output units. Four Nodes contain 96 Registers.
This internal graph is symmetric under proper signed-axis rotations; it does
not establish continuous isotropy or relativity. External spatial degree remains
six. Any future topology change needs explicit user approval.

This supersedes the earlier one-Register-per-Port definition. Existing six-Port
banks/readiness adapters retain their implementation meaning and are not evidence
of the revised 24-Register runtime. No runtime is changed by this definition.

## Node, Register and value ownership

| Owner | Contents or role |
| --- | --- |
| Node | One logical identity, one NodeState, its Registers and joint-operation coordination |
| Register at (node, from_port, to_port) | Bounded state/ownership for one directed internal transition and its local delay within that NodeState |
| Link | Values dispatched by a Register and not yet delivered to the next Node |
| External scheduler | Host scheduling indexes and due-work entries; no additional physical state or hidden law |

Input and output are roles, not additional physical value types. Values remain
Scalars or Vectors while resident, received, waiting, outgoing or in transit.
A Register is a computational unit, not a synonym for a Scalar, Vector or Node.

A Node may receive several inputs at the same simulated time. Keep the distinct
arrivals available to joint rules. Splitting work across Registers must not
duplicate owned stock, discard another Port's input or expose half a joint commit.
The scheduling and dependency contract is owned by
[Register-level execution](ARCHITECTURE.md#register-level-execution-target).

In the design discussion, C denotes the Link propagation clock and h the local
Register/Node delay. They are distinct model quantities, not an automatic SI
calibration; h is not Planck's constant. The exact mapping to current
`link_ticks`, k and cost-budget profiles remains explicit in their contracts.
A waiting value is still Node-owned; Link transit starts only after dispatch.
Computational decomposition alone adds no physical hop or elapsed model time.

Host transport addresses `(node_id, port_id)`; due computational work addresses
`(node_id, register_id)` or `(node_id, from_port, to_port)`. A delivered Port
input does not select a unique Register until the local operation resolves its
bounded dependencies. Splitting/merging uses one Node-owned atomic transaction
over participating Registers, with a common snapshot, reservations and explicit
allocation/transfer of owned values. A channel can carry a bounded vector payload;
packaging independent arrivals together does not make them one input. No individual
Register exposes a multi-input/multi-output transition or copies inventory.

Straight passage exits the opposite face on the same axis; return exits the
entry face. Neither is a direct edge of the orthogonal internal graph. Their
realization through a Node operation remains OPEN: do not ban either behavior,
choose an intermediate axis, or invent microstep ticks or extra physical Links.

## No second physical-location noun

Node is the only active physical-location noun. Register is an internal
computational unit, not another physical location; `Site` is not a synonym.

- Use `node` / `nodes` for locations and `NodeState` for their state.
- Use Register or `directed_register` for the intended internal directed unit;
  use `port`, `link` and `event` for their distinct responsibilities.
- Existing quantum algebra registers are separate mathematical subsystems.
  Retain their technical identifiers and qualify them as quantum registers when
  ambiguity exists. They are not automatically internal computational Registers.
- Registry and `BondRegistry` mean a registry, not a Register or Node. Do not
  rename them by text substitution.
- External API identifiers and historical evidence retain their exact meaning.
  Existing references to storage registers or counted integer slots are not a
  count of the new computational Registers.
- Do not introduce `site`, `input state` or `output state` as physical-location
  synonyms.

## Implementation boundary

This definition supersedes Register-as-Node and the earlier one-Register-per-Port design.
It does not rename runtime classes, JSON keys, quantum registers or existing
state-layout counts. The current Node-owned execution path remains documented in
[NODE_VECTOR_PROCESSOR.md](NODE_VECTOR_PROCESSOR.md); current active-set behavior
remains in [LOCAL_FOCUS.md](LOCAL_FOCUS.md). Any runtime migration must update its
consumers and test ownership, timing, errors and event equivalence explicitly.
