"""Turn a runner record into the viewer's ``runs.json``: rays, events, captions.

A Renderer reads records and never the engine (Highlights 3.29 and 3.30). This
module reads only the files the runner wrote next to ``run.json``: the event
stream ``events.jsonl``, the preserved ``initialization.json`` and, when a
recording tool wrote one, a per-tick ``ray-recording.json`` (``--sidecar`` names
it explicitly). Nothing here imports the simulator. One function handles each
record kind; a kind this module does not know becomes a generic marker, so a
record from a later feature still renders.

Run:  python tools/ray_viewer/extract.py RUN [RUN ...] --out runs.json
where RUN is a ``run.json`` file or the directory that holds it.
"""

from __future__ import annotations

import argparse
import json
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

SCHEMA = "ray-viewer-runs-v1"
PORT_HEADINGS = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
PORT_NAMES = ("+x", "-x", "+y", "-y", "+z", "-z")
RECORD_FILES = ("run.json", "events.jsonl", "initialization.json", "state.json", "ray-recording.json")
# Event kinds consumed structurally (they build rays) rather than drawn as markers,
# and host-timing diagnostics of a Node's cycle that mark nothing on the board.
STRUCTURAL_KINDS = ("spatial_sent", "spatial_received", "spatial_escaped", "spatial_cycle")
SILENT_KINDS = ("spatial_cycle_started", "cycle_started", "cycle_committed", "external_body_step")
# Event kinds the default caption lists (a style file can choose others).
CAPTION_KINDS = ("meeting", "deflection", "conversion", "click", "return", "arrival", "split")
CAPTION_MAX = 3

Position = tuple[int, int, int]
Amounts = dict[str, list[int]]


def position_of(value: object) -> Position:
    if not isinstance(value, list | tuple) or len(value) != 3:
        raise ValueError(f"a position needs three integers, not {value!r}")
    x, y, z = (int(v) for v in value)
    return (x, y, z)


def neighbor(position: Position, port: int, shape: Position, boundary: str) -> Position | None:
    """The Node behind a Port, or None when an open Link leaves the board."""
    axis, step = port // 2, 1 if port % 2 == 0 else -1
    moved = list(position)
    moved[axis] += step
    if 0 <= moved[axis] < shape[axis]:
        return (moved[0], moved[1], moved[2])
    if boundary == "periodic":
        moved[axis] %= shape[axis]
        return (moved[0], moved[1], moved[2])
    return None


def heading_of_port(port: int) -> list[int]:
    return list(PORT_HEADINGS[port])


def scale(heading: list[int], amount: int) -> list[int]:
    return [component * amount for component in heading]


def add_vectors(vectors: list[list[int]]) -> list[int]:
    total = [0, 0, 0]
    for vector in vectors:
        for axis in range(3):
            total[axis] += vector[axis]
    return total


def add_amounts(target: Amounts, family: str, values: list[int]) -> None:
    current = target.setdefault(family, [0] * len(values))
    for index, value in enumerate(values):
        current[index] += value


def sum_amounts(target: Amounts, other: Amounts) -> None:
    for family, values in other.items():
        add_amounts(target, family, values)


# ---------------------------------------------------------------------------
# The record on disk


@dataclass
class Record:
    """The files of one run, read once."""

    directory: Path
    metadata: dict[str, Any]
    events: list[dict[str, Any]]
    initialization: dict[str, Any] | None
    frames: list[dict[str, Any]] | None
    files: list[str]
    sidecar: Path | None = None


def load_record(path: Path, sidecar: Path | None = None) -> Record:
    """Read ``run.json`` and the files beside it; ``sidecar`` names a ray recording."""
    path = Path(path)
    directory = path if path.is_dir() else path.parent
    metadata_path = path if path.is_file() else directory / "run.json"
    if not metadata_path.is_file():
        raise ValueError(f"no run record at {path}")
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    if not isinstance(metadata, dict):
        raise ValueError(f"{metadata_path} is not a JSON object")
    files = [name for name in RECORD_FILES if (directory / name).is_file()]
    events: list[dict[str, Any]] = []
    stream = directory / "events.jsonl"
    if stream.is_file():
        for line in stream.read_text(encoding="utf-8").splitlines():
            if line.strip():
                events.append(json.loads(line))
    initialization = None
    source = directory / "initialization.json"
    if source.is_file():
        initialization = json.loads(source.read_text(encoding="utf-8"))
    frames = metadata.get("frames") if isinstance(metadata.get("frames"), list) else None
    recording = Path(sidecar) if sidecar is not None else directory / "ray-recording.json"
    sidecar_path: Path | None = None
    if sidecar is not None and not recording.is_file():
        raise ValueError(f"no ray recording at {recording}")
    if frames is None and recording.is_file():
        sidecar_path = recording
        recorded = json.loads(recording.read_text(encoding="utf-8"))
        if not isinstance(recorded, dict) or not isinstance(recorded.get("frames"), list):
            raise ValueError(f"{recording} holds no frames")
        for key in ("source_sha256", "initialization_sha256"):
            if key in recorded and key in metadata and recorded[key] != metadata[key]:
                raise ValueError(f"{recording} was made from another run ({key} differs)")
        frames = recorded["frames"]
        for key in ("model", "completed_ticks", "initial_totals", "escaped_totals"):
            metadata.setdefault(key, recorded.get(key))
    return Record(directory, metadata, events, initialization, frames, files, sidecar_path)


# ---------------------------------------------------------------------------
# Building rays and events from the stream


@dataclass
class Transit:
    """One packet on one Link: sent at ``tick`` through ``port``, arriving at ``arrival``."""

    tick: int
    origin: Position
    port: int
    target: Position | None
    arrival: int
    amounts: Amounts = field(default_factory=dict)
    escaped: bool = False


@dataclass
class Unit:
    """One family's share of a transit: the drawable ray on that Link."""

    transit: Transit
    family: str
    amount: list[int]
    phase: int | None = None
    arrival_phase: int | None = None
    steps: int | None = None
    outbound: int | None = None
    event_ports: int | None = None
    event_shares: list[int] | None = None
    detector: int | None = None
    chain: Chain | None = None


@dataclass
class Chain:
    """A ray: the Links one share walked between two events."""

    identifier: int
    family: str
    origin_tick: int
    origin_node: Position
    origin_event: int | None
    returning: bool = False
    event_node: Position | None = None
    units: list[Unit] = field(default_factory=list)
    held: list[dict[str, int | list[int]]] = field(default_factory=list)
    end: dict[str, Any] | None = None
    steps_at_start: int = 0

    @property
    def amount(self) -> list[int]:
        return self.units[-1].amount if self.units else [0]

    @property
    def last_port(self) -> int | None:
        return self.units[-1].transit.port if self.units else None

    @property
    def steps(self) -> int:
        if self.units and self.units[-1].steps is not None:
            return self.units[-1].steps
        walked = len(self.units)
        return max(0, self.steps_at_start - walked) if self.returning else walked


@dataclass
class Event:
    """A marker on the board: where and when something happened, and to whom.

    ``field`` marks an event of field rays alone or a release, which the page
    keeps silent; ``escaped`` carries the family amounts of an escape.
    """

    identifier: int
    tick: int
    node: Position
    kind: str
    label: str
    ports: list[int] = field(default_factory=list)
    inputs: list[int] = field(default_factory=list)
    outputs: list[int] = field(default_factory=list)
    detail: dict[str, Any] = field(default_factory=dict)
    output_tick: int | None = None
    pending: Amounts = field(default_factory=dict)
    field: bool = False


@dataclass
class Builder:
    """Collects what each record kind says, then resolves rays and events."""

    shape: Position
    boundary: str
    transits: list[Transit] = field(default_factory=list)
    receptions: dict[tuple[Position, int], list[dict[str, Any]]] = field(default_factory=dict)
    escapes: dict[tuple[Position, int, int], Amounts] = field(default_factory=dict)
    clicks: list[dict[str, Any]] = field(default_factory=list)
    absorptions: dict[tuple[Position, int], list[dict[str, Any]]] = field(default_factory=dict)
    notes: dict[tuple[Position, int], dict[str, Any]] = field(default_factory=dict)
    sources: dict[int, Amounts] = field(default_factory=dict)
    generic: list[dict[str, Any]] = field(default_factory=list)
    unknown_kinds: dict[str, int] = field(default_factory=dict)

    def add_sent(self, event: dict[str, Any]) -> None:
        origin = position_of(event["position"])
        port = int(event["port"])
        self.transits.append(
            Transit(
                int(event["tick"]),
                origin,
                port,
                neighbor(origin, port, self.shape, self.boundary),
                int(event["arrival_tick"]),
            )
        )

    def add_received(self, event: dict[str, Any]) -> None:
        key = (position_of(event["position"]), int(event["tick"]))
        readings = event.get("received_fields")
        self.receptions[key] = list(readings) if isinstance(readings, list) else []

    def add_escaped(self, event: dict[str, Any]) -> None:
        key = (position_of(event["position"]), int(event["port"]), int(event["tick"]))
        amounts: Amounts = {}
        for family, values in dict(event.get("escaped") or {}).items():
            add_amounts(amounts, str(family), [int(v) for v in values])
        self.escapes[key] = amounts

    def add_cycle(self, event: dict[str, Any]) -> None:
        tick = int(event["tick"])
        for family, values in dict(event.get("source_delta") or {}).items():
            add_amounts(self.sources.setdefault(tick, {}), str(family), [int(v) for v in values])
        detail = {key: event[key] for key in ("source_delta", "rule_delta", "cost") if event.get(key)}
        if detail:
            self.notes[(position_of(event["position"]), tick)] = detail

    def add_click(self, event: dict[str, Any]) -> None:
        self.clicks.append(event)

    def add_absorbed(self, event: dict[str, Any]) -> None:
        """An external body absorbed an arriving ray into its sink (external-body-v1)."""
        key = (position_of(event["position"]), int(event["tick"]))
        self.absorptions.setdefault(key, []).append(event)

    def add_generic(self, event: dict[str, Any]) -> None:
        kind = str(event.get("event", "record"))
        self.unknown_kinds[kind] = self.unknown_kinds.get(kind, 0) + 1
        self.generic.append(event)


Handler = Callable[[Builder, dict[str, Any]], None]
EVENT_KINDS: dict[str, Handler] = {
    "spatial_sent": Builder.add_sent,
    "spatial_received": Builder.add_received,
    "spatial_escaped": Builder.add_escaped,
    "spatial_cycle": Builder.add_cycle,
    "detector_click": Builder.add_click,
    "external_body_absorbed": Builder.add_absorbed,
}


def ingest(builder: Builder, events: list[dict[str, Any]]) -> None:
    for event in events:
        kind = str(event.get("event", ""))
        if kind in SILENT_KINDS:
            continue
        handler = EVENT_KINDS.get(kind)
        if handler is None:
            builder.add_generic(event)
        else:
            handler(builder, event)


def resolve_amounts(builder: Builder, ray_families: set[str] | None = None) -> list[Unit]:
    """Give every transit the family amounts its receiver, or the escape, recorded.

    Only ray families travel on Links; an audit family such as a lamp's recoil
    momentum appears in escape totals but is not a ray, so it is left out when
    the record says which families are ray fields.
    """
    units: list[Unit] = []
    for transit in builder.transits:
        if transit.target is None:
            transit.escaped = True
            transit.amounts = builder.escapes.get((transit.origin, transit.port, transit.arrival), {})
        else:
            readings = builder.receptions.get((transit.target, transit.arrival), [])
            entry = transit.port ^ 1
            reading = readings[entry] if entry < len(readings) and readings[entry] else {}
            for family, values in dict(reading).items():
                transit.amounts[str(family)] = [int(v) for v in values]
            # What an external body's sink took on arrival is not in the receiver's
            # reading (external-body-v1): the absorbed record names the Port the ray
            # came in through, the family and the amount, so the transit keeps them.
            for taken in builder.absorptions.get((transit.target, transit.arrival), []):
                if int(taken.get("port", -1)) == entry:
                    add_amounts(transit.amounts, str(taken["family"]), [int(taken["amount"])])
        for family, values in transit.amounts.items():
            if any(values) and (ray_families is None or family in ray_families):
                units.append(Unit(transit, family, values))
    return units


def recorded_ray(
    frame: dict[str, Any] | None, node: Position, family: str, port: int
) -> dict[str, Any] | None:
    """The recorded ray of ``family`` at ``node`` in one frame, on the Port's heading if any."""
    if frame is None:
        return None
    heading = heading_of_port(port)
    candidates = [
        item
        for item in frame.get("rays", [])
        if item.get("field") == family
        and (
            (item.get("owner") == "node" and position_of(item["position"]) == node)
            or (
                item.get("owner") == "link"
                and position_of(item["position" if "position" in item else "origin"]) == node
                and int(item.get("port", -1)) == port
            )
        )
    ]
    exact = [item for item in candidates if list(item.get("heading_vector", [])) == heading]
    chosen = (exact or candidates or [None])[0]
    return None if chosen is None else dict(chosen.get("ray") or {})


def enrich_from_frames(units: list[Unit], frames: list[dict[str, Any]] | None) -> None:
    """Phase and ray-event fields from a per-tick ray recording, when one exists.

    The departure frame gives the ray as it leaves its Node; the arrival frame
    gives the phase it reaches the next Node with, which is the phase a meeting
    there sees.
    """
    if not frames:
        return
    by_tick = {int(frame["tick"]): frame for frame in frames if "tick" in frame}
    for unit in units:
        transit = unit.transit
        ray = recorded_ray(by_tick.get(transit.tick), transit.origin, unit.family, transit.port)
        if ray is not None:
            unit.phase = int(ray["phase"]) if "phase" in ray else None
            for name in ("steps", "outbound", "event_ports", "detector"):
                if name in ray:
                    setattr(unit, name, int(ray[name]))
            if "event_shares" in ray:
                unit.event_shares = [int(v) for v in ray["event_shares"]]
        if transit.target is not None:
            arrived = recorded_ray(
                by_tick.get(transit.arrival), transit.target, unit.family, transit.port
            )
            if arrived is not None and "phase" in arrived:
                unit.arrival_phase = int(arrived["phase"])


def momentum(units: list[Unit]) -> list[int]:
    return add_vectors([scale(heading_of_port(u.transit.port), u.amount[0]) for u in units])


def amounts_of(units: list[Unit]) -> Amounts:
    total: Amounts = {}
    for unit in units:
        add_amounts(total, unit.family, unit.amount)
    return total


def phases_of(units: list[Unit]) -> list[int | None]:
    return [unit.phase for unit in units]


def arrival_phases_of(units: list[Unit]) -> list[int | None]:
    return [unit.arrival_phase for unit in units]


def straight_continuation(ins: list[Unit], outs: list[Unit]) -> bool:
    """Every arriving share leaves on its own line, same family and amount."""
    if len(ins) != len(outs):
        return False
    remaining = list(outs)
    for unit in ins:
        match = next(
            (
                o
                for o in remaining
                if o.transit.port == unit.transit.port
                and o.family == unit.family
                and o.amount == unit.amount
            ),
            None,
        )
        if match is None:
            return False
        remaining.remove(match)
    return True


@dataclass
class Resolution:
    chains: list[Chain]
    events: list[Event]
    units: list[Unit]


def resolve(
    builder: Builder,
    units: list[Unit],
    *,
    ticks: int,
    detectors: set[Position],
    couplings: list[str],
    field_families: set[str],
) -> Resolution:
    """Chain the Link transits into rays and mark every event on the board.

    Matter rays (families that are not a field of another) make the events: a
    Node that receives one share and sends it on continues the ray; a Node where
    two or more shares are present, or where one leaves changed, is an event and
    its outputs are new rays. A field ray passes a Node in silence unless it
    leaves changed there, which is a meeting with the matter at that Node; field
    rays leaving a Node with a departing matter ray are that ray's release.
    """
    chains: list[Chain] = []
    events: list[Event] = []
    resident: dict[Position, list[Chain]] = {}
    pending: dict[Position, Event] = {}
    by_arrival: dict[tuple[Position, int], list[Unit]] = {}
    by_departure: dict[tuple[Position, int], list[Unit]] = {}
    for unit in units:
        by_departure.setdefault((unit.transit.origin, unit.transit.tick), []).append(unit)
        if unit.transit.target is not None:
            by_arrival.setdefault((unit.transit.target, unit.transit.arrival), []).append(unit)
    clicks_at: dict[tuple[Position, int], list[dict[str, Any]]] = {}
    for click in builder.clicks:
        clicks_at.setdefault((position_of(click["position"]), int(click["tick"])), []).append(click)

    def new_chain(unit: Unit, tick: int, node: Position, event: Event | None) -> Chain:
        chain = Chain(len(chains), unit.family, tick, node, None if event is None else event.identifier)
        chains.append(chain)
        attach(chain, unit)
        return chain

    def attach(chain: Chain, unit: Unit) -> None:
        unit.chain = chain
        chain.units.append(unit)

    def new_event(tick: int, node: Position, kind: str, label: str, **detail: Any) -> Event:
        event = Event(len(events), tick, node, kind, label, detail=detail)
        events.append(event)
        return event

    def end_chain(chain: Chain, tick: int, node: Position, kind: str, event: Event | None) -> None:
        chain.end = {"tick": tick, "node": list(node), "kind": kind}
        if event is not None:
            chain.end["event"] = event.identifier
            event.inputs.append(chain.identifier)

    def start_outputs(event: Event, outs: list[Unit], tick: int, node: Position) -> list[Chain]:
        if event.output_tick is None:
            event.output_tick = tick
            if tick > event.tick:
                event.detail["held_ticks"] = tick - event.tick
        started = []
        for unit in outs:
            chain = new_chain(unit, tick, node, event)
            started.append(chain)
            event.outputs.append(chain.identifier)
            if unit.transit.port not in event.ports:
                event.ports.append(unit.transit.port)
        event.detail.setdefault("amount_out", {})
        sum_amounts(event.detail["amount_out"], amounts_of(outs))
        event.detail["momentum_out"] = add_vectors(
            [event.detail.get("momentum_out", [0, 0, 0]), momentum(outs)]
        )
        event.detail.setdefault("phase_out", []).extend(phases_of(outs))
        for family, values in amounts_of(outs).items():
            left = event.pending.get(family)
            if left is not None:
                for index, value in enumerate(values):
                    left[index] -= value
        if not any(any(v > 0 for v in values) for values in event.pending.values()):
            pending.pop(node, None)
        return started

    def open_meeting(node: Position, tick: int, present: list[Chain]) -> Event:
        arrived = [chain.units[-1] for chain in present]
        event = new_event(
            tick,
            node,
            "meeting",
            "meeting",
            amount_in=amounts_of(arrived),
            momentum_in=momentum(arrived),
            phase_in=arrival_phases_of(arrived),
            coupling=couplings,
        )
        for chain in present:
            end_chain(chain, tick, node, "event", event)
        event.pending = amounts_of(arrived)
        return event

    def release(node: Position, tick: int, field_outs: list[Unit], sources: list[Chain]) -> None:
        event = new_event(tick, node, "release", "field released")
        event.field = True
        event.output_tick = tick
        for chain in sources:
            if chain.identifier not in event.inputs:
                event.inputs.append(chain.identifier)
        for unit in field_outs:
            chain = new_chain(unit, tick, node, event)
            event.outputs.append(chain.identifier)
            if unit.transit.port not in event.ports:
                event.ports.append(unit.transit.port)
        event.detail["amount_out"] = amounts_of(field_outs)

    nodes_by_tick: dict[int, set[Position]] = {}
    for (node, tick), _ in list(by_arrival.items()) + list(by_departure.items()):
        nodes_by_tick.setdefault(tick, set()).add(node)
    for (node, tick), _ in clicks_at.items():
        nodes_by_tick.setdefault(tick, set()).add(node)

    for tick in range(ticks + 1):
        for node in sorted(nodes_by_tick.get(tick, set())):
            ins = by_arrival.get((node, tick), [])
            outs = by_departure.get((node, tick), [])
            matter_ins = [u for u in ins if u.family not in field_families]
            field_ins = [u for u in ins if u.family in field_families]
            matter_outs = [u for u in outs if u.family not in field_families]
            field_outs = [u for u in outs if u.family in field_families]
            arrived: list[Chain] = [u.chain for u in matter_ins if u.chain is not None]
            arrived_field: list[Chain] = [u.chain for u in field_ins if u.chain is not None]
            for click in clicks_at.get((node, tick), []):
                port = int(click.get("port", -1))
                clicked = next((c for c in arrived + arrived_field if c.last_port == port ^ 1), None)
                marker = new_event(
                    tick,
                    node,
                    "click",
                    "Detector PASS",
                    port=port,
                    family=click.get("family"),
                    amount=click.get("amount"),
                    bit=click.get("bit", 1),
                )
                if clicked is not None:
                    marker.inputs.append(clicked.identifier)
            for chain in arrived + arrived_field:
                if chain.returning and chain.event_node == node:
                    marker = new_event(tick, node, "arrival", "returning ray at its event Node")
                    marker.field = chain.family in field_families
                    marker.inputs.append(chain.identifier)
            taken_here = builder.absorptions.get((node, tick), [])
            if taken_here:
                # A body's sink (external-body-v1): the arriving rays of the families
                # the body took end here, drawn as an absorption; a family its declared
                # coupling meets goes on to the ordinary law below, as does what leaves.
                families_taken = {str(taken.get("family")) for taken in taken_here}
                taken = [c for c in arrived + arrived_field if c.family in families_taken]
                absorbed = new_event(tick, node, "absorption", "absorbed by the body")
                absorbed.detail["absorbed"] = amounts_of([c.units[-1] for c in taken])
                for chain in taken:
                    end_chain(chain, tick, node, "absorbed", absorbed)
                arrived = [c for c in arrived if c.family not in families_taken]
                arrived_field = [c for c in arrived_field if c.family not in families_taken]
            # Field rays that pass straight through are not an event here.
            changed_field: list[Chain] = []
            for chain in arrived_field:
                onward = next(
                    (
                        o
                        for o in field_outs
                        if o.chain is None
                        and o.transit.port == chain.last_port
                        and o.family == chain.family
                    ),
                    None,
                )
                if onward is None:
                    changed_field.append(chain)
                else:
                    attach(chain, onward)
            held = resident.pop(node, [])
            present = held + arrived
            note = builder.notes.get((node, tick), {})
            departing: list[Chain] = []
            if changed_field and present:
                # A field ray meets the matter at this Node and leaves changed.
                event = open_meeting(node, tick, present + changed_field)
                pending[node] = event
                outs_now = list(matter_outs)
                for chain in changed_field:
                    back = next(
                        (
                            o
                            for o in field_outs
                            if o.chain is None
                            and o.family == chain.family
                            and o.transit.port == (chain.last_port or 0) ^ 1
                        ),
                        None,
                    )
                    if back is not None:
                        outs_now.append(back)
                if outs_now:
                    started = start_outputs(event, outs_now, tick, node)
                    for chain, unit in zip(started, outs_now, strict=True):
                        if unit.family in field_families:
                            source = next(c for c in changed_field if c.family == unit.family)
                            chain.returning = True
                            chain.event_node = source.origin_node
                            chain.steps_at_start = source.steps
                        else:
                            departing.append(chain)
            elif changed_field:
                for chain in changed_field:
                    onward = next((o for o in field_outs if o.chain is None), None)
                    if onward is None:
                        if tick < ticks:
                            chain.end = {"tick": tick, "node": list(node), "kind": "absorbed"}
                    else:
                        event = new_event(tick, node, "deflection", "trajectory changed")
                        event.field = True
                        end_chain(chain, tick, node, "event", event)
                        started = start_outputs(event, [onward], tick, node)
                        started[0].returning = chain.returning
                        started[0].event_node = chain.event_node
            elif node in pending and pending[node].tick < tick:
                # Outputs of a meeting whose rays were held at the Node.
                event = pending[node]
                for chain in arrived:
                    end_chain(chain, tick, node, "event", event)
                    add_amounts(event.pending, chain.family, chain.amount)
                if matter_outs:
                    departing = start_outputs(event, matter_outs, tick, node)
            elif not present and matter_outs:
                event = new_event(tick, node, "emission", "emission", **note)
                departing = start_outputs(event, matter_outs, tick, node)
            elif present and not matter_outs:
                if len(present) >= 2:
                    pending[node] = open_meeting(node, tick, present)
                else:
                    for chain in present:
                        chain.held.append({"tick": tick, "node": list(node)})
                    resident[node] = present
            elif present:
                arrived_units = [chain.units[-1] for chain in present]
                if len(present) >= 2 or len(matter_outs) >= 2:
                    if (
                        len(present) >= 2
                        and straight_continuation(arrived_units, matter_outs)
                        and not held
                    ):
                        marker = new_event(tick, node, "crossing", "crossing, no interaction")
                        for chain in present:
                            marker.inputs.append(chain.identifier)
                            onward = next(
                                o
                                for o in matter_outs
                                if o.chain is None and o.transit.port == chain.last_port
                            )
                            attach(chain, onward)
                            departing.append(chain)
                    else:
                        if len(present) == 1:
                            chain = present[0]
                            kind = "inverse split" if chain.returning else "split"
                            event = new_event(
                                tick,
                                node,
                                "split",
                                kind,
                                amount_in=amounts_of(arrived_units),
                                momentum_in=momentum(arrived_units),
                                phase_in=arrival_phases_of(arrived_units),
                            )
                            end_chain(chain, tick, node, "event", event)
                        else:
                            event = open_meeting(node, tick, present)
                        departing = start_outputs(event, matter_outs, tick, node)
                else:
                    chain, out = present[0], matter_outs[0]
                    came_in, goes_out = chain.last_port, out.transit.port
                    if goes_out == came_in and out.family == chain.family:
                        if held:
                            chain.held.append({"tick": tick, "node": list(node)})
                        attach(chain, out)
                        departing = [chain]
                    elif came_in is not None and goes_out == came_in ^ 1 and out.family == chain.family:
                        if node in detectors:
                            kind, label = "return", "Detector RETURN"
                        else:
                            kind, label = "reversal", "reversed on its line"
                        event = new_event(
                            tick,
                            node,
                            kind,
                            label,
                            amount_in=amounts_of(arrived_units),
                            momentum_in=momentum(arrived_units),
                            phase_in=arrival_phases_of(arrived_units),
                        )
                        end_chain(chain, tick, node, "event", event)
                        reversed_chain = start_outputs(event, [out], tick, node)[0]
                        reversed_chain.returning = True
                        reversed_chain.event_node = chain.origin_node
                        reversed_chain.steps_at_start = chain.steps
                        departing = [reversed_chain]
                    else:
                        kind = "conversion" if out.family != chain.family else "deflection"
                        label = "family changed" if kind == "conversion" else "trajectory changed"
                        event = new_event(
                            tick,
                            node,
                            kind,
                            label,
                            amount_in=amounts_of(arrived_units),
                            momentum_in=momentum(arrived_units),
                            phase_in=arrival_phases_of(arrived_units),
                            coupling=couplings,
                        )
                        end_chain(chain, tick, node, "event", event)
                        departing = start_outputs(event, matter_outs, tick, node)
            left = [u for u in field_outs if u.chain is None]
            if left:
                release(node, tick, left, departing)
    for unit in units:
        if unit.chain is None:
            new_chain(unit, unit.transit.tick, unit.transit.origin, None)
        if unit.transit.escaped and unit.chain is not None and unit.chain.end is None:
            marker = new_event(unit.transit.arrival, unit.transit.origin, "escape", "escaped the board")
            marker.field = unit.family in field_families
            marker.ports.append(unit.transit.port)
            marker.inputs.append(unit.chain.identifier)
            marker.detail["escaped"] = {unit.family: list(unit.amount)}
            unit.chain.end = {
                "tick": unit.transit.arrival,
                "node": list(unit.transit.origin),
                "kind": "escaped",
                "event": marker.identifier,
            }
    for node, held_chains in resident.items():
        for chain in held_chains:
            chain.end = {"tick": ticks, "node": list(node), "kind": "held"}
    for event in events:
        if event.kind == "meeting" and event.output_tick is None:
            event.label = "meeting, rays held"
        if event.kind == "crossing" and all(chains[i].family in field_families for i in event.inputs):
            event.field = True
    for record in builder.generic:
        try:
            node = position_of(record.get("position"))
        except ValueError:
            continue
        kind = str(record.get("event", "record"))
        detail = {k: v for k, v in record.items() if k not in ("event", "tick", "position")}
        new_event(int(record.get("tick", 0)), node, kind, kind.replace("_", " "), **detail)
    events.sort(key=lambda e: (e.tick, e.node, e.identifier))
    renumbered = {event.identifier: index for index, event in enumerate(events)}
    for event in events:
        event.identifier = renumbered[event.identifier]
    for chain in chains:
        if chain.origin_event is not None:
            chain.origin_event = renumbered[chain.origin_event]
        if chain.end is not None and "event" in chain.end:
            chain.end["event"] = renumbered[chain.end["event"]]
    return Resolution(chains, events, units)


# ---------------------------------------------------------------------------
# Families, sources and the per-tick caption


def is_field_family(name: str, definition: dict[str, Any] | None) -> bool:
    """A field family: declared with ``field_of`` (feature 7) or named as a field."""
    if definition is not None and (definition.get("field_of") or definition.get("release")):
        return True
    return "field" in name.lower()


def families(record: Record) -> list[dict[str, Any]]:
    initialization = record.initialization or {}
    fields = {str(item["name"]): item for item in initialization.get("fields", [])}
    spatial = {}
    for definition in initialization.get("spatial_fields", []):
        index = definition.get("field")
        name = str(index) if isinstance(index, str) else list(fields)[int(index)] if fields else ""
        spatial[name] = definition
    names = [str(n) for n in record.metadata.get("fields", [])] or list(fields)
    result = []
    for name in names:
        definition = spatial.get(name)
        kerengonen = dict(definition.get("kerengonen") or {}) if definition else {}
        result.append(
            {
                "name": name,
                "components": int(fields.get(name, {}).get("components", 1)),
                "conserved": bool(fields.get(name, {}).get("conserved", False)),
                "ray": definition is not None,
                "field": is_field_family(name, definition),
                "field_of": None if definition is None else definition.get("field_of"),
                "release": None if definition is None else definition.get("release"),
                "phase_steps": kerengonen.get("phase_steps"),
            }
        )
    return result


def sources(record: Record) -> list[dict[str, Any]]:
    initialization = record.initialization or {}
    return [
        {"pos": list(position_of(seed["position"])), "type": str(seed.get("type", "seed"))}
        for seed in initialization.get("seeds", [])
    ]


def detectors(record: Record) -> list[dict[str, Any]]:
    initialization = record.initialization or {}
    return [
        {
            "pos": list(position_of(mark["position"])),
            "setting": [int(v) for v in mark.get("setting", [])],
            "seed": mark.get("seed"),
        }
        for mark in initialization.get("detectors", [])
    ]


def external_bodies(record: Record) -> list[dict[str, Any]]:
    """External bodies (Highlights 3.19, ``external-body-v1``): declaration and positions.

    ``run.json`` lists each body with its declaration, its ``positions`` as
    ``[tick, x, y, z]`` rows (tick 0 first) and its final state; the page draws
    the body at the recorded position of the tick shown.
    """
    initialization = record.initialization or {}
    bodies = record.metadata.get("external_bodies") or initialization.get("external_bodies") or []
    result = []
    for body in bodies:
        if not isinstance(body, dict):
            continue
        rows = [[int(v) for v in row] for row in body.get("positions", []) if isinstance(row, list)]
        start = rows[0][1:] if rows else body.get("position")
        if start is None:
            continue
        result.append(
            {
                "pos": list(position_of(start)),
                "family": body.get("family"),
                "amount": body.get("amount"),
                "coupling": body.get("coupling", "sink"),
                "field": body.get("field"),
                "positions": rows,
            }
        )
    return result


def couplings(record: Record) -> list[str]:
    initialization = record.initialization or {}
    names = [str(rule.get("name", "rule")) for rule in initialization.get("ray_interactions", [])]
    names += [str(rule.get("name", "rule")) for rule in initialization.get("spatial_couplings", [])]
    return names


def vector_text(values: list[int] | None) -> str:
    if values is None:
        return "?"
    return str(values[0]) if len(values) == 1 else "(" + ", ".join(str(v) for v in values) + ")"


def amounts_text(amounts: Amounts | None) -> str:
    if not amounts:
        return "?"
    return ", ".join(f"{family} {vector_text(values)}" for family, values in sorted(amounts.items()))


def phase_text(phases: list[int | None] | None) -> str:
    if not phases:
        return "?"
    return "/".join("?" if p is None else str(p) for p in phases)


def node_text(node: Position) -> str:
    return f"({node[0]},{node[1]},{node[2]})"


def event_caption(event: Event, chains: list[Chain]) -> str:
    """One short line per event, every number from the record."""
    text = f"t{event.tick} {event.label} {node_text(event.node)}"
    detail = event.detail
    if event.kind == "emission":
        out = ", ".join(f"{chains[i].family} {vector_text(chains[i].amount)}" for i in event.outputs)
        ports = ", ".join(PORT_NAMES[p] for p in event.ports)
        return f"{text}: {out} through {ports}"
    if event.kind == "release":
        return f"{text}: {amounts_text(detail.get('amount_out'))}"
    if event.kind == "click":
        return (
            f"{text}: {detail.get('family')} {detail.get('amount')} through"
            f" {PORT_NAMES[int(detail.get('port', 0))]}, bit {detail.get('bit')}"
        )
    if event.kind == "escape":
        return f"{text}: {amounts_text(detail.get('escaped'))} through {', '.join(PORT_NAMES[p] for p in event.ports)}"
    if event.kind in ("meeting", "split", "deflection", "conversion", "return", "reversal"):
        names = detail.get("coupling") or []
        head = text + (" " + ", ".join(names) if names else "")
        parts = [
            f"in {amounts_text(detail.get('amount_in'))}, p {vector_text(detail.get('momentum_in'))},"
            f" φ {phase_text(detail.get('phase_in'))}"
        ]
        if event.output_tick is not None:
            parts.append(
                f"out t{event.output_tick} {amounts_text(detail.get('amount_out'))},"
                f" p {vector_text(detail.get('momentum_out'))}, φ {phase_text(detail.get('phase_out'))}"
            )
        else:
            parts.append("outputs pending")
        return head + ": " + " · ".join(parts)
    return text


def tick_note(
    listed: list[Event],
    more: int,
    escaped: Amounts,
    field_escaped: Amounts,
    emissions: int,
    chains: list[Chain],
) -> str:
    lines = [event_caption(e, chains) for e in listed]
    if more:
        lines.append(f"and {more} more")
    if emissions:
        lines.append(f"{emissions} emission{'s' if emissions != 1 else ''}")
    if escaped:
        lines.append("escaped: " + amounts_text(escaped))
    if field_escaped:
        lines.append("field escaped: " + amounts_text(field_escaped))
    return " | ".join(lines)


def tick_captions(
    record: Record, resolution: Resolution, builder: Builder, ticks: int
) -> list[dict[str, Any]]:
    metadata = record.metadata
    initial: Amounts = {
        str(k): [int(x) for x in v] for k, v in dict(metadata.get("initial_totals") or {}).items()
    }
    frames_by_tick = {int(f["tick"]): f for f in (record.frames or []) if "tick" in f}
    escaped: Amounts = {name: [0] * len(values) for name, values in initial.items()}
    sourced: Amounts = {name: [0] * len(values) for name, values in initial.items()}
    events_by_tick: dict[int, list[Event]] = {}
    outputs_by_tick: dict[int, list[Event]] = {}
    for event in resolution.events:
        events_by_tick.setdefault(event.tick, []).append(event)
        if event.output_tick is not None and event.output_tick != event.tick:
            outputs_by_tick.setdefault(event.output_tick, []).append(event)
    rows = []
    for tick in range(ticks + 1):
        on_links: Amounts = {}
        held: Amounts = {}
        escaped_now: Amounts = {}
        field_escaped_now: Amounts = {}
        for unit in resolution.units:
            if unit.transit.tick == tick:
                add_amounts(on_links, unit.family, unit.amount)
            if unit.transit.escaped and unit.transit.arrival == tick:
                add_amounts(escaped, unit.family, unit.amount)
        for chain in resolution.chains:
            if any(h["tick"] == tick for h in chain.held):
                add_amounts(held, chain.family, chain.amount)
        # What a tick released is on the Links from the next tick, so the in-world
        # figure of tick t counts the sources through t - 1, as a recording does.
        sourced_before = {k: list(v) for k, v in sourced.items()}
        sum_amounts(sourced, builder.sources.get(tick, {}))
        here = events_by_tick.get(tick, [])
        for event in here:
            if event.kind == "escape":
                target = field_escaped_now if event.field else escaped_now
                sum_amounts(target, event.detail.get("escaped", {}))
        frame = frames_by_tick.get(tick)
        totals = frame.get("totals") if frame else None
        recorded_escaped = frame.get("escaped_totals") if frame else None
        in_world: Amounts = {}
        for name in set(initial) | set(sourced) | set(escaped):
            width = len(initial.get(name) or sourced.get(name) or escaped.get(name) or [0])
            in_world[name] = [
                initial.get(name, [0] * width)[i]
                + sourced_before.get(name, [0] * width)[i]
                - escaped.get(name, [0] * width)[i]
                for i in range(width)
            ]
        listed_all = [
            e for e in here + outputs_by_tick.get(tick, []) if e.kind in CAPTION_KINDS and not e.field
        ]
        listed, more = listed_all[:CAPTION_MAX], max(0, len(listed_all) - CAPTION_MAX)
        emissions = sum(1 for e in here if e.kind == "emission")
        rows.append(
            {
                "tick": tick,
                "on_links": on_links,
                "held": held,
                "sourced": {k: list(v) for k, v in sourced.items()},
                "escaped": {k: list(v) for k, v in escaped.items()},
                "in_world": in_world,
                "totals": totals,
                "recorded_escaped": recorded_escaped,
                "events": [e.identifier for e in here],
                "outputs_of": [e.identifier for e in outputs_by_tick.get(tick, [])],
                "escaped_now": escaped_now,
                "field_escaped_now": field_escaped_now,
                "emissions": emissions,
                "releases": sum(1 for e in here if e.kind == "release"),
                "note": tick_note(
                    listed, more, escaped_now, field_escaped_now, emissions, resolution.chains
                ),
            }
        )
    return rows


def conservation(record: Record) -> dict[str, Any]:
    metadata = record.metadata
    local = metadata.get("local_conservation")
    status = local.get("status") if isinstance(local, dict) else local
    return {
        "status": status,
        "every_tick": metadata.get("conserved_at_every_completed_tick"),
        "balanced": metadata.get("accounting_balanced_at_every_completed_tick"),
        "initial_totals": metadata.get("initial_totals"),
        "final_totals": metadata.get("final_totals"),
        "escaped_totals": metadata.get("escaped_totals"),
        "source_totals": metadata.get("source_totals"),
        # The world ledger per completed tick (ray-event-audit-v1), when recorded.
        "audit": metadata.get("audit"),
    }


def chain_document(chain: Chain, family_flags: dict[str, bool]) -> dict[str, Any]:
    segments = []
    for index, unit in enumerate(chain.units):
        if unit.steps is not None:
            steps = unit.steps
        elif chain.returning:
            steps = max(0, chain.steps_at_start - index - 1)
        else:
            steps = index + 1
        segments.append(
            {
                "tick": unit.transit.tick,
                "arrival": unit.transit.arrival,
                "from": list(unit.transit.origin),
                "to": None if unit.transit.target is None else list(unit.transit.target),
                "port": unit.transit.port,
                "heading": heading_of_port(unit.transit.port),
                "amount": unit.amount,
                "phase": unit.phase,
                "arrival_phase": unit.arrival_phase,
                "steps": steps,
                "outbound": (0 if chain.returning else 1) if unit.outbound is None else unit.outbound,
                "event_ports": unit.event_ports,
                "event_shares": unit.event_shares,
                "detector": unit.detector,
                "escaped": unit.transit.escaped,
            }
        )
    return {
        "id": chain.identifier,
        "family": chain.family,
        "field": family_flags.get(chain.family, False),
        "amount": chain.amount,
        "origin": {
            "tick": chain.origin_tick,
            "node": list(chain.origin_node),
            "event": chain.origin_event,
        },
        "returning": chain.returning,
        "event_node": None if chain.event_node is None else list(chain.event_node),
        "segments": segments,
        "held": chain.held,
        "end": chain.end,
    }


def event_document(event: Event, chains: list[Chain]) -> dict[str, Any]:
    return {
        "id": event.identifier,
        "tick": event.tick,
        "node": list(event.node),
        "kind": event.kind,
        "label": event.label,
        "field": event.field,
        "ports": event.ports,
        "in": event.inputs,
        "out": event.outputs,
        "output_tick": event.output_tick,
        "detail": event.detail,
        "caption": event_caption(event, chains),
    }


def extract_record(
    path: Path, *, key: str | None = None, label: str | None = None, sidecar: Path | None = None
) -> dict[str, Any]:
    """The viewer document of one recorded run."""
    record = load_record(Path(path), sidecar)
    metadata = record.metadata
    shape = position_of(metadata.get("shape") or (record.initialization or {}).get("shape"))
    boundary = str(metadata.get("boundary") or (record.initialization or {}).get("boundary", "open"))
    ticks = int(metadata.get("completed_ticks", metadata.get("tick", 0)))
    builder = Builder(shape, boundary)
    ingest(builder, record.events)
    family_list = families(record)
    ray_families = {str(f["name"]) for f in family_list if f["ray"]} or None
    field_set = {str(f["name"]) for f in family_list if f["field"]}
    units = resolve_amounts(builder, ray_families)
    enrich_from_frames(units, record.frames)
    marks = detectors(record)
    resolution = resolve(
        builder,
        units,
        ticks=ticks,
        detectors={position_of(m["pos"]) for m in marks},
        couplings=couplings(record),
        field_families=field_set,
    )
    flags = {str(f["name"]): bool(f["field"]) for f in family_list}
    name = key or record.directory.name or str(metadata.get("model", "run"))
    kinds: dict[str, int] = {}
    for event in resolution.events:
        kinds[event.kind] = kinds.get(event.kind, 0) + 1
    return {
        "key": name,
        "label": label or str(metadata.get("model", name)),
        "model": metadata.get("model"),
        "status": metadata.get("status"),
        "ticks": ticks,
        "shape": list(shape),
        "boundary": boundary,
        "link_ticks": metadata.get("link_ticks"),
        "record": {
            "directory": str(record.directory),
            "files": record.files,
            "sidecar": None if record.sidecar is None else str(record.sidecar),
            "source_sha256": metadata.get("source_sha256"),
            "initialization_sha256": metadata.get("initialization_sha256"),
            "package_version": metadata.get("package_version"),
            "ray_state": metadata.get("ray_state"),
            "detector_mark": metadata.get("detector_mark"),
            "released_field": metadata.get("released_field"),
            "sampling_profile": metadata.get("sampling_profile"),
            "event_count": len(record.events),
            "unknown_event_kinds": builder.unknown_kinds,
            "frames": record.frames is not None,
        },
        "families": family_list,
        "sources": sources(record),
        "detectors": marks,
        "external_bodies": external_bodies(record),
        "couplings": couplings(record),
        "conservation": conservation(record),
        "event_kinds": kinds,
        "rays": [chain_document(c, flags) for c in resolution.chains],
        "events": [event_document(e, resolution.chains) for e in resolution.events],
        "ticks_data": tick_captions(record, resolution, builder, ticks),
    }


def extract_runs(
    paths: list[Path], labels: list[str] | None = None, sidecars: list[Path] | None = None
) -> dict[str, Any]:
    labels = labels or []
    sidecars = sidecars or []
    runs = [
        extract_record(
            path,
            label=labels[i] if i < len(labels) else None,
            sidecar=sidecars[i] if i < len(sidecars) else None,
        )
        for i, path in enumerate(paths)
    ]
    keys = [run["key"] for run in runs]
    if len(set(keys)) != len(keys):
        for index, run in enumerate(runs):
            run["key"] = f"{run['key']}-{index}"
    return {"schema": SCHEMA, "generator": "tools/ray_viewer/extract.py", "runs": runs}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("records", nargs="+", type=Path, help="run.json files or their directories")
    parser.add_argument("--out", type=Path, required=True, help="the runs.json to write")
    parser.add_argument("--label", action="append", default=[], help="one label per record, in order")
    parser.add_argument(
        "--sidecar",
        action="append",
        default=[],
        type=Path,
        help="a ray-recording.json per record, in order (default: the one beside run.json)",
    )
    args = parser.parse_args()
    document = extract_runs(args.records, args.label, args.sidecar)
    args.out.write_text(json.dumps(document, separators=(",", ":")) + "\n", encoding="utf-8")
    summary = {
        "output": str(args.out),
        "bytes": args.out.stat().st_size,
        "runs": [
            {
                "key": run["key"],
                "ticks": run["ticks"],
                "rays": len(run["rays"]),
                "events": run["event_kinds"],
                "sidecar": run["record"]["sidecar"],
                "unknown_event_kinds": run["record"]["unknown_event_kinds"],
            }
            for run in document["runs"]
        ],
    }
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
