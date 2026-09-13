# Canonical simulation terminology

Universe24 uses one canonical vocabulary for the active simulator. These names describe the model, documentation, new identifiers, diagnostics and configuration concepts.

## Core terms

- **Node** — one local location in Event Space. A Node is the basic physical location of the simulator.
- **NodeState** — all local information currently owned by one Node. NodeState is not a second physical object; it is the state of the Node.
- **Scalar** — a one-component local value.
- **Vector** — a three-component local value.
- **Port** — one local directional connection endpoint of a Node.
- **Link** — the causal connection between neighboring Nodes. A Link owns a transferred value while it is in transit.
- **Event** — a local state transition at a Node or a completed transfer on a Link.
- **LocalRule** — configured local logic that reads only the NodeState and values that have already arrived through Links, then proposes the next local state and outgoing transfers.

## Values do not become new physical kinds when they move

Input and output are roles, not value types. Values remain Scalars or Vectors throughout their lifetime.

A Scalar or Vector can have local transport metadata such as:

- `resident` — owned by the Node;
- `incoming` — completed a Link transfer and is available to the Node's local rules;
- `waiting` — reserved at the Node until its configured directional delay expires;
- `outgoing` — reserved for a Port and ready for Link dispatch;
- `in_transit` — owned by a Link until arrival.

Direction, Port, ownership and timing metadata do not change a Scalar into a different kind of physical quantity.

## Node model

Conceptually:

```text
Node
  NodeState
    Scalars
    Vectors
    ownership / port / timing metadata
  LocalRules
  Ports -> Links -> neighboring Nodes
```

A Node may receive values from several neighboring Nodes on the same tick. Those arrivals are one local Event set. The configured LocalRules determine whether and how they interact. The engine must not silently compress distinct simultaneous arrivals before the selected local interaction has access to them.

Directional delay belongs to a Node's outgoing scheduling. It is an integer multiple of `link_ticks`. A waiting value remains owned by its Node until dispatch. Link transit begins only after dispatch and always takes the configured fixed Link time.

## Terms that are not canonical physical concepts

`Node` and `Site` are not separate physical entities in the active model.

- New active code, documentation, tests and diagnostics must use `Node` or `NodeState` when referring to a simulation location or its local state.
- `Site` may appear only when describing a mathematical topology set or a quoted external/historical API where changing the word would change that API's identity.
- `Node` may appear only inside explicitly historical compatibility APIs or migration notes that name an old identifier. Such text must say that the identifier is legacy; it must not define a second physical concept.
- Historical identifiers are migrated toward `Node` / `NodeState` when their public compatibility contract allows it.

## Naming rule

When adding or renaming active implementation symbols:

- use `node` / `nodes` for positions and position-indexed state;
- use `NodeState` for the local state record;
- use `port` for a directional endpoint;
- use `link` for in-transit ownership;
- use `event` for a local transition;
- use `scalar` / `vector` for physical value shape;
- do not introduce `node`, `site`, `input state`, or `output state` as alternative physical nouns.

Configuration keys that predate this contract may remain temporarily for backward compatibility. Their documentation must describe them using the canonical Node vocabulary and migration must not silently change physical behavior.