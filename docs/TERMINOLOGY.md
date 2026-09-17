# Canonical simulation terminology

Universe24 uses one canonical vocabulary for the active simulator. These names describe the model, documentation, identifiers, diagnostics and configuration concepts.

## Core terms

- **Node** — one local location in Event Space. A Node is the basic physical location of the simulator.
- **NodeState** — all local information currently owned by one Node. NodeState is not a second physical object; it is the state of the Node.
- **Scalar** — a one-component local value.
- **Vector** — a three-component local value.
- **Port** — one local directional connection endpoint of a Node.
- **Link** — the causal connection between neighboring Nodes. A Link owns a transferred value while it is in transit.
- **Event** — a local state transition at a Node or a completed transfer on a Link.
- **LocalRule** — configured local logic that reads only the NodeState and values that have already arrived through Links, then proposes the next local state and outgoing transfers.

## Ray-event terms

The ray-event model ([Highlights](HIGHLIGHTS.md) 3.3, 3.19, 3.20 and 5.1;
[ray-event model](RAY_EVENT_MODEL.md#1-definitions)) uses these terms;
`ray-event-state-v1` ([ray state](SPATIAL_FIELDS.md#ray-state-ray-event-state-v1))
carries them on every ray.

- **Ray** — the trajectory of one event between two interactions: one heading, one straight line, one Node per Link interval, carrying its share of the event's information. In the spatial-field implementation a `Ray` record is one straight-moving share of a ray field.
- **Interaction** — a meeting of rays at a Node in one interval, decided by the coupling declared between their families; its result is at most six events, one per Port. In the current slice an emission by a resident record and a firing `ray_interactions` group are the interactions that create rays.
- **Layer** — a set of families that couple: a connected component of the ray fields over the participants of the declared `ray_interactions`, derived, never declared (`ray-layers-v1`, [layers](SPATIAL_FIELDS.md#layers-ray-layers-v1)). A meeting exists only inside a layer; rays of different layers cross as if the other were not there, so two events can happen at one Node in one interval. A family that no rule selects is its own layer.
- **Output** — one of the new event rays that a meeting with declared `outputs` creates at its Node in place of its participants (`ray-meeting-conversion-v1`, [meetings with outputs](SPATIAL_FIELDS.md#meetings-with-outputs-ray-meeting-conversion-v1)): a family, an amount, a heading (a Port, the source input's or its reverse), a phase and a delay, stamped with the meeting's Ports and shares; an output of amount zero is no ray.
- **Table split** — the split of the content two inputs share between two outputs in the ratio a declared integer table gives at their phase difference, the table output taking the whole quanta of its share and the rest output the rest, including the remainder (Highlights 3.17); the engine only splits by the table, the physics is the declared table (Highlights 3.26).
- **Event of a ray** — a change of trajectory: a new straight line leaving an interaction through one Port. The core term Event above names the engine's local transitions and completed transfers; a ray's event is the interaction that created its trajectory.
- **Steps** — the number of Links a ray has walked since its event, counted up while outbound and down on the walk back; zero at the event Node.
- **Outbound** — `1` while a ray travels on its event's heading, `0` once it is reversed on its own line (a return).
- **Event Ports** — the six-bit mask of the Ports the ray's event sent to, in Port order `[+X, -X, +Y, -Y, +Z, -Z]`.
- **Event shares** — the amount the ray's event sent through each Port, six entries in Port order and zero where the mask bit is zero: the information a returning ray needs for the inverse split.
- **Detector bit** — what a ray records of a Detector event: `0` none, `1` a Detector event that drew 0, `2` a Detector event that drew 1. The bit is all a Detector adds to a ray.
- **Hidden variable** — a value carried on a ray that no rule, coupling, absorber or readout reads; steps, outbound, event Ports, event shares and the Detector bit are hidden in `ray-event-state-v1`.

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

## No second physical-location noun

Node is the only active physical-location noun. `Site` is not a synonym for Node.

- Active code, documentation, tests and diagnostics use `Node` or `NodeState` for a simulation location or its local state.
- `Site` may appear only when it is part of an external standard name or when it denotes a distinct non-physical mathematical/register concept. In quantum code, prefer `register` or `register_index` when that is the actual meaning.
- External protocol, package and API identifiers are preserved verbatim when renaming them would change their defined identity.
- Retired pre-migration location identifiers are not retained as active API aliases.
- Historical evidence may preserve old literal names when changing them would falsify the recorded source; such evidence does not define the active vocabulary.

## Naming rule

When adding or renaming active implementation symbols:

- use `node` / `nodes` for positions and position-indexed state;
- use `NodeState` for the local state record;
- use `port` for a directional endpoint;
- use `link` for in-transit ownership;
- use `event` for a local transition;
- use `scalar` / `vector` for physical value shape;
- use `register` / `register_index` for a quantum algebra register when it is not a physical-location name;
- do not introduce `site`, `input state`, or `output state` as alternative physical nouns.

The active API and configuration use the canonical Node vocabulary directly. Breaking migrations are explicit and must update all active consumers rather than preserving a parallel physical vocabulary.
