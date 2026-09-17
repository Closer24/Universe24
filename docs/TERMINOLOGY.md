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
carries them on every ray, `detector-mark-v1`
([Detector mark](DETECTOR_SAMPLING.md#the-detector-mark-detector-mark-v1)) sets
the Detector bit at a marked Node, `detector-return-v1`
([Detector return](DETECTOR_SAMPLING.md#the-return-detector-return-v1)) returns
the ray on a draw of 0, and `inverse-split-v1`
([Inverse split](DETECTOR_SAMPLING.md#the-inverse-split-inverse-split-v1))
performs the inverse split at the event Node.

- **Ray** — the trajectory of one event between two interactions: one heading, one straight line, one Node per Link interval, carrying its share of the event's information. In the spatial-field implementation a `Ray` record is one straight-moving share of a ray field.
- **Interaction** — a meeting of rays at a Node in one interval, decided by the coupling declared between their families; its result is at most six events, one per Port. In the current slice an emission by a resident record and a firing `ray_interactions` group are the interactions that create rays.
- **Event of a ray** — a change of trajectory: a new straight line leaving an interaction through one Port. The core term Event above names the engine's local transitions and completed transfers; a ray's event is the interaction that created its trajectory.
- **Steps** — the number of Links a ray has walked since its event, counted up while outbound and down on the walk back; zero at the event Node.
- **Outbound** — `1` while a ray travels on its event's heading, `0` once it is reversed on its own line (a return). A draw of 0 at a marked Node is the one thing that sets `0`.
- **Return** — what a marked Node does with a ray whose draw is 0 (`detector-return-v1`): the same wave ray reversed on its line, unchanged in amount, phase and event record, leaving in the same interval through the Port it came in through and walking its steps back one Link per tick. A returning ray enters no coupling and no absorption, is sampled by nothing, merges with nothing and is drawn for by no mark; a return is no measurement, and the `detector_return` record is a record of the reversal, not of an outcome.
- **Resident returned ray** — a returning ray at `steps` 0: it is at its event Node and stays there as a resident ray with `outbound` 0, its phase, amount and event record exactly what it left the event with, until the next cycle's inverse split consumes it: no Link is planned for it, its phase does not move, and it enters no coupling.
- **Inverse split** — what a returned ray does at its event Node (`inverse-split-v1`): it performs the inverse of its own share of the event by the world's return mode, transmitting its amount, phase and bit to the sibling lines of the event, continuing straight, or ending into the annulled sink; nothing stays at the Node. If the event's input is still at the Node, the share is first restored to it exactly and the transmission funded from it in the same interval.
- **Transmission** — the new event ray or rays the inverse split creates at the event Node: outbound, no steps walked, the returned ray's phase and bit, the mask of the lines transmitted to and the amount per line as their event record. A ray like any other; what happens when it meets the share it chases is a declared coupling.
- **Return mode** — the world key `return_mode` with the three values `siblings` (default: every line the event sent to except the ray's own), `straight` (the one line opposite its own) and `annul` (the share ends there).
- **Annulled** — content that left the world at an inverse split in `annul` mode, into an explicitly accounted sink per field (`annulled_totals()`): initial + sources = current + dissipated + escaped + annulled at every completed tick; its information survives only in the `inverse_split` record.
- **Event Ports** — the six-bit mask of the Ports the ray's event sent to, in Port order `[+X, -X, +Y, -Y, +Z, -Z]`.
- **Event shares** — the amount the ray's event sent through each Port, six entries in Port order and zero where the mask bit is zero: the information a returning ray needs for the inverse split.
- **Detector bit** — what a ray records of a Detector event: `0` none, `1` a Detector event that drew 0, `2` a Detector event that drew 1. The bit is all a Detector adds to a ray; a marked Node sets it on every arrival (`detector-mark-v1`).
- **Detector mark** — the Detector bit of a Node together with its setting `n / d` and its ticket seed (`detectors` in the initialization, `DetectorMark` in the code): bounded Node metadata, not a record and not stock. A marked Node draws one bit per arriving ray from its own ticket stream, reading nothing from the ray, and is otherwise an ordinary Node.
- **Click** — the `detector_click` record of a draw of 1 at a marked Node: position, tick, Port, family, amount and bit 1. The click is the record of the measurement and the only one; a draw of 0 records nothing, because a return is no measurement.
- **Hidden variable** — a value carried on a ray that no coupling, absorber or readout reads; the Detector bit is hidden in `ray-event-state-v1`. Steps and outbound are read by the return (`detector-return-v1`): the transport of a returning ray and its momentum readout; the event Ports and the event shares by the inverse split alone (`inverse-split-v1`), and the bit is copied onto the transmission unread. A marked Node writes the Detector bit and reads none of them.

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
