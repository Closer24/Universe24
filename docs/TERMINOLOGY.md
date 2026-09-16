# Canonical simulation terminology

Universe24 uses the following vocabulary for its intended architecture.
The Node/Register distinction is a design definition, not a claim that the
Register-level scheduler is already implemented. Existing execution contracts
remain in force until an explicit implementation change is validated.

## Core terms

| Term | Definition |
| --- | --- |
| Node | One logical unit at a physical location in Event Space. It owns one bounded NodeState and contains one Register per Port. |
| NodeState | All local information owned by one Node, including the bounded values and metadata of its Registers. It is not a second physical object or a copy per Register. |
| Register | A generic computational input/output unit inside a Node, associated with exactly one Port. All Registers execute the same generic local logic; input, state, direction, configured rules and delay are data. |
| Scalar | A one-component value. |
| Vector | A three-component spatial value; wider bounded property arrays in the opt-in Node profile have their own explicit shape contract. |
| Port | A directional connection endpoint, served by its associated Register. |
| Link | The causal connection between neighboring Nodes. It owns a transferred value during transit. |
| Event | A local state transition or a completed Link transfer. Computational substeps do not create new physical locations. |
| LocalRule | Configured generic logic operating on owned local state and already-delivered inputs; joint dependencies retain Node-level coordination and atomicity. |

The initial six-port cube therefore contains **six Registers in one Node**,
not six new physical Nodes. Port count is intended to be a bounded topology
configuration, not part of the universal definition of Node or Register.
The current code still fixes the degree to six; configurable topology and
Register-level scheduling are not implemented by this terminology update.

## Node, Register and value ownership

| Owner | Contents or role |
| --- | --- |
| Node | One logical identity, one NodeState, its Registers and joint-operation coordination |
| Register at (node, port) | Bounded input/output state, direction and local delay metadata within that NodeState |
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

## No second physical-location noun

Node is the only active physical-location noun. Register is an internal
computational unit, not another physical location; `Site` is not a synonym.

- Use `node` / `nodes` for locations and `NodeState` for their state.
- Use Register or `port_register` for the intended per-Port computational unit;
  use `port`, `link` and `event` for their distinct responsibilities.
- Existing quantum algebra registers are separate mathematical subsystems.
  Retain their technical identifiers and qualify them as quantum registers when
  ambiguity exists. They are not automatically per-Port Registers.
- Registry and `BondRegistry` mean a registry, not a Register or Node. Do not
  rename them by text substitution.
- External API identifiers and historical evidence retain their exact meaning.
  Existing references to storage registers or counted integer slots are not a
  count of the new computational Registers.
- Do not introduce `site`, `input state` or `output state` as physical-location
  synonyms.

## Implementation boundary

This definition supersedes the earlier use of Register as another name for Node.
It does not rename runtime classes, JSON keys, quantum registers or existing
state-layout counts. The current Node-owned execution path remains documented in
[NODE_VECTOR_PROCESSOR.md](NODE_VECTOR_PROCESSOR.md); current active-set behavior
remains in [LOCAL_FOCUS.md](LOCAL_FOCUS.md). Any runtime migration must update its
consumers and test ownership, timing, errors and event equivalence explicitly.
