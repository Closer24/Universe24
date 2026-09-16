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
| Node | One logical unit at a physical location in Event Space. It groups the 24 private Registers defined below; it is a container, not an independent physical computation unit. |
| NodeState | The aggregate description of the bounded private states and metadata of one Node's Registers; grouping does not grant shared physical read access. It is not a second physical object or a copy per Register. |
| Register | A directed internal computational transition between orthogonal Ports, with exactly one input channel and exactly one output channel. Each Register reads only its own state and its actually received single-channel input. All execute the same generic local logic; state, input, direction and delay are data. |
| Scalar | A one-component value. |
| Vector | A three-component spatial value; wider bounded property arrays in the opt-in Node profile have their own explicit shape contract. |
| Port | One of the six external directional connection endpoints; a Port is not a Register. |
| Link | The causal connection between neighboring Nodes. It owns a transferred value during transit. |
| Event | A local state transition or a completed Link transfer. Computational substeps do not create new physical locations. |
| LocalRule | Configured generic logic operating only on one Register's private state and actually received input; no peer-state read, including within the same Node. |

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
| Node | Logical identity and grouping of private Registers; scheduling/reservation metadata is not an independent physical mixer |
| Register at (node, from_port, to_port) | Bounded state/ownership for one directed internal transition and its local delay within that NodeState |
| Link | Values dispatched by a Register and not yet delivered to the next Node |
| External scheduler | Host scheduling indexes and due-work entries; no additional physical state or hidden law |

Input and output are roles, not additional physical value types. Values remain
Scalars or Vectors while resident, received, waiting, outgoing or in transit.
A Register is a computational unit, not a synonym for a Scalar, Vector or Node.

Several inputs may arrive at a Node at the same simulated time, but each remains
an independently owned channel delivery. A Register cannot read another Register's
state or arrivals. Any physical information between Registers must arrive through
an actual causal channel transfer, even inside one Node. Bounded declared memory
of its own received inputs is allowed; hidden peer-state access is not.
The scheduling and dependency contract is owned by
[Register-level execution](ARCHITECTURE.md#register-level-execution-target).

In the design discussion, c denotes propagation speed, not a time unit. Local
Register delay and Link transit time are distinct; their physical calibration is
not selected merely by naming c. Use delta_t_min for the minimum model interval;
legacy local h notation is not Planck's constant. The exact mapping to current
`link_ticks`, k and cost-budget profiles remains explicit in their contracts.
A waiting value is still Node-owned; Link transit starts only after dispatch.
Computational decomposition alone adds no physical hop or elapsed model time.

Host transport addresses `(node_id, port_id)`; due computational work addresses
`(node_id, register_id)` or `(node_id, from_port, to_port)`. A delivered Port
input requires an explicit bounded delivery mapping into the internal graph.
The binding transition is
`F(own_state, actually_received_input, immutable_law) -> (new_own_state, one_output)`.
A channel can carry a bounded vector payload; packaging independent arrivals
together does not make them one input. No Register exposes a multi-input/multi-output
transition, reads peer state or copies inventory.

A Node coordinator may schedule work and reserve handles, timing or capacity.
It cannot read or supply another Register's physical state, synthesize aggregate
physical input, or independently mix values. Split/merge and other interactions
require a bounded causal message protocol preserving ownership and remainders;
that protocol and its atomic publication/timing remain OPEN. Earlier permission
for a shared Node-wide physical snapshot is superseded. NodeState is a grouping
and diagnostic view, not an input capability for a Register.

Straight passage exits the opposite face on the same axis; return exits the
entry face. Neither is a direct edge of the orthogonal internal graph. Their
realization through private Register channel transfers remains OPEN: do not ban either behavior,
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
