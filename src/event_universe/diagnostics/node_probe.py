"""Bounded test observations of the real node scheduler and its causal ports.

This module owns no physical transition or input injection. Tests seed ordinary
neighbors, advance the ordinary Simulation, and inspect detached local views.
The probe retains at most one completed transition and one bounded active batch;
callers own any returned transition history they choose to retain.
"""

from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from itertools import islice
from typing import Literal

from event_universe.core.disturbance_state import Address3, InitialState, unpack
from event_universe.core.node_state import NodeSnapshot
from event_universe.core.topology import inverse_port, validate_position
from event_universe.disturbance_api import Simulation

MAX_PROBE_NODES = 64
MAX_PROBE_EVENTS = 65_536
DEFAULT_MAX_EVENTS = 4_096
MAX_ERROR_MESSAGE = 4_096
NamedValues = tuple[tuple[str, tuple[int, ...]], ...]
EventSink = Callable[[dict[str, object]], None]


@dataclass(frozen=True, slots=True)
class NodeSample:
    """A local physical view plus separate diagnostic completion counters."""

    snapshot: NodeSnapshot
    clock: int
    spatial_cycles: int


@dataclass(frozen=True, slots=True)
class NodePortEvent:
    """One real port observation, with both ends' port numbering explicit.

    ``port`` is the selected node's local side. ``travel_port`` is the sender's
    output index, and ``receiver_port`` is its configured reciprocal. Spatial
    receptions already carry receiver indices; they must not be inverted twice.
    ``values`` contains decoded integers, not additional physical inventory.
    """

    event: str
    kind: Literal["carrier", "spatial"]
    direction: Literal["input", "output"]
    position: Address3
    source: Address3 | None
    target: Address3 | None
    audit_tick: int
    clock: int
    port: int
    travel_port: int
    receiver_port: int
    event_port: int | None
    values: NamedValues
    disturbance: str | None
    arrival_tick: int


@dataclass(frozen=True, slots=True)
class NodeTransition:
    """One scheduler step, including the owned prefix of a failed step.

    Error text is retained instead of the exception or traceback. No exception
    graph can keep an old world or an unbounded execution history alive here.
    """

    start_tick: int
    end_tick: int
    before: tuple[NodeSample, ...]
    after: tuple[NodeSample, ...]
    events: tuple[NodePortEvent, ...]
    error_type: str | None = None
    error_message: str | None = None
    snapshot_error_type: str | None = None
    snapshot_error_message: str | None = None


def _named_values(value: object) -> NamedValues:
    if not isinstance(value, Mapping):
        raise ValueError("node port observations require named integer values")
    result = []
    for name, components in value.items():
        if (
            not isinstance(name, str)
            or not isinstance(components, (tuple, list))
            or len(components) not in (1, 3)
            or any(type(component) is not int for component in components)
        ):
            raise ValueError("node port values require scalar or three-component integers")
        result.append((name, tuple(components)))
    return tuple(result)


def _integer(value: object, label: str) -> int:
    if type(value) is not int:
        raise ValueError(f"{label} must be an integer")
    return value


def _error_message(error: BaseException) -> str:
    """Keep observer-owned formatting from replacing the original failure."""
    try:
        message = str(error)
    except BaseException:
        return "Exception message unavailable"
    if len(message) > MAX_ERROR_MESSAGE:
        return message[: MAX_ERROR_MESSAGE - 3] + "..."
    return message


class NodeProbe:
    """Advance one real world and observe an explicit bounded selection of nodes.

    ``clock`` counts completed carrier cycles; ``spatial_cycles`` counts completed
    field phases. Neither is audit time, proper time, or a new physical register.
    Only ``step`` collects a transition. Direct ``world.step`` calls update the
    counters and forward the observer, but do not accumulate event history.
    The optional observer follows the engine's existing read-only callback
    contract. Its exceptions preserve their original type and stopping point.
    """

    def __init__(
        self,
        initial: InitialState,
        positions: Iterable[Address3],
        *,
        max_events: int = DEFAULT_MAX_EVENTS,
        observer: EventSink | None = None,
    ) -> None:
        if type(max_events) is not int or not 1 <= max_events <= MAX_PROBE_EVENTS:
            raise ValueError(f"max_events must be from 1 through {MAX_PROBE_EVENTS}")
        selected = tuple(islice(iter(positions), MAX_PROBE_NODES + 1))
        if not 1 <= len(selected) <= MAX_PROBE_NODES:
            raise ValueError(f"select from 1 through {MAX_PROBE_NODES} probe nodes")
        for position in selected:
            validate_position(position, initial.shape, initial.topology)
        if len(set(selected)) != len(selected):
            raise ValueError("probe node positions must be unique")
        self.positions = selected
        self.max_events = max_events
        self._initial = initial
        self._observer = observer
        self._clocks = dict.fromkeys(selected, 0)
        self._spatial_cycles = dict.fromkeys(selected, 0)
        self._events: list[NodePortEvent] = []
        self._collecting = False
        self._closed = False
        self.last_transition: NodeTransition | None = None
        self.world = Simulation(initial, observer=self._observe)

    def sample(self) -> tuple[NodeSample, ...]:
        """Read only selected local owners, without creating nodes or a world scan."""
        return tuple(
            NodeSample(
                self.world.node_view(position), self._clocks[position], self._spatial_cycles[position]
            )
            for position in self.positions
        )

    def step(self) -> NodeTransition:
        """Run the ordinary phase order; publish a failure prefix before reraising."""
        if self._closed:
            raise RuntimeError("node probe is closed")
        if self._collecting:
            raise RuntimeError("node probe step cannot be called from an observer")
        before = self.sample()
        start_tick = self.world.tick
        self._events.clear()
        self._collecting = True
        error_type = error_message = None
        try:
            self.world.step()
        except BaseException as error:
            error_type = type(error).__name__
            error_message = _error_message(error)
            raise
        finally:
            self._collecting = False
            capture_error: BaseException | None = None
            snapshot_error_type = snapshot_error_message = None
            try:
                after = self.sample()
            except BaseException as error:
                after = ()
                capture_error = error
                snapshot_error_type = type(error).__name__
                snapshot_error_message = _error_message(error)
            self.last_transition = NodeTransition(
                start_tick,
                self.world.tick,
                before,
                after,
                tuple(self._events),
                error_type,
                error_message,
                snapshot_error_type,
                snapshot_error_message,
            )
            self._events.clear()
            if capture_error is not None and error_type is None:
                raise capture_error
        return self.last_transition

    def _observe(self, event: dict[str, object]) -> None:
        raw_position = event.get("position")
        if isinstance(raw_position, (tuple, list)) and len(raw_position) == 3:
            position = (raw_position[0], raw_position[1], raw_position[2])
            if position in self._clocks:
                kind = event.get("event")
                if kind == "cycle_committed":
                    self._clocks[position] += 1
                elif kind == "spatial_cycle":
                    self._spatial_cycles[position] += 1
                elif self._collecting:
                    batch = self._port_events(position, event)
                    if len(self._events) + len(batch) > self.max_events:
                        raise ValueError(
                            "node probe event capacity exceeded before retaining this batch"
                        )
                    self._events.extend(batch)
        if self._observer is not None:
            self._observer(event)

    def _port_events(self, position: Address3, event: dict[str, object]) -> tuple[NodePortEvent, ...]:
        name = event.get("event")
        if name == "spatial_received":
            ports = event.get("received_fields")
            if not isinstance(ports, (list, tuple)) or len(ports) != self._initial.topology.degree:
                raise ValueError("node field reception must match the configured port count")
            return tuple(
                self._port_event(position, event, "spatial", "input", port, _named_values(values))
                for port, values in enumerate(ports)
                if values
            )
        if name not in ("received", "sent", "spatial_sent"):
            return ()
        port = _integer(event.get("port"), "event port")
        if name == "spatial_sent":
            packet = self.world.node_view(position).spatial_outgoing[port]
            if packet is None:
                raise ValueError("completed spatial send requires its locally owned packet")
            values = tuple(
                (
                    self._initial.fields[definition.field].name,
                    tuple(
                        sum(unpack(population)[component] for population in populations)
                        for component in range(self._initial.fields[definition.field].components)
                    ),
                )
                for definition, populations in zip(
                    self._initial.spatial_fields, packet.fields, strict=True
                )
            )
            return (self._port_event(position, event, "spatial", "output", port, values),)
        return (
            self._port_event(
                position,
                event,
                "carrier",
                "input" if name == "received" else "output",
                port,
                _named_values(event.get("values")),
            ),
        )

    def _port_event(
        self,
        position: Address3,
        event: dict[str, object],
        kind: Literal["carrier", "spatial"],
        direction: Literal["input", "output"],
        port: int,
        values: NamedValues,
    ) -> NodePortEvent:
        opposite = inverse_port(port, self._initial.topology)
        tick = _integer(event.get("tick"), "event tick")
        receiving = direction == "input"
        label = event.get("disturbance")
        if kind == "carrier" and not isinstance(label, str):
            raise ValueError("carrier port observation requires a disturbance label")
        return NodePortEvent(
            event=str(event["event"]),
            kind=kind,
            direction=direction,
            position=position,
            source=self.world.neighbor(position, port) if receiving else position,
            target=position if receiving else self.world.neighbor(position, port),
            audit_tick=tick,
            clock=self._clocks[position],
            port=port,
            travel_port=opposite if receiving else port,
            receiver_port=port if receiving else opposite,
            event_port=None if event["event"] == "spatial_received" else port,
            values=values,
            disturbance=label if isinstance(label, str) else None,
            arrival_tick=tick if receiving else _integer(event.get("arrival_tick"), "arrival tick"),
        )

    def close(self) -> None:
        """Close any world-owned host resources once; retain the last detached result."""
        if not self._closed:
            self._closed = True
            close = getattr(self.world, "close", None)
            if callable(close):
                close()

    def __enter__(self) -> NodeProbe:
        if self._closed:
            raise RuntimeError("node probe is closed")
        return self

    def __exit__(self, *exception: object) -> None:
        self.close()
