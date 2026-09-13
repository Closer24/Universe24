"""A passive reception probe: local completed events, never remote world state."""

from collections.abc import Mapping
from typing import TypedDict

from event_universe.core.disturbance_state import MAX_PORTS
from event_universe.observer_configuration import ObserverDefinition as ObserverDefinition

MODEL = "local-reception-observer-v1"


class Receipt(TypedDict):
    sequence: int
    clock: int
    kind: str
    port: int
    label: str
    values: dict[str, tuple[int, ...]]


class ObserverSample(TypedDict):
    audit_tick: int
    clock: int
    received_count: int


def _values(value: object) -> dict[str, tuple[int, ...]]:
    if not isinstance(value, Mapping):
        raise ValueError("a completed reception must carry named integer values")
    result = {}
    for name, components in value.items():
        if (
            not isinstance(name, str)
            or not isinstance(components, (tuple, list))
            or len(components) not in (1, 3)
            or any(type(item) is not int for item in components)
        ):
            raise ValueError("reception values must have one or three integer components")
        result[name] = tuple(components)
    return result


class LocalObserver:
    """Whitelist the selected node's completed inputs and cycle completions.

    Clock counts completed whole-node carrier cycles, not ticks or proper time.
    Receipt sequence is archive order, not a measured time interval. Histories
    belong to the host and never become cell state or a planner input.
    """

    def __init__(self, definition: ObserverDefinition, *, port_count: int = 6) -> None:
        if type(port_count) is not int or not 2 <= port_count <= MAX_PORTS:
            raise ValueError(f"observer port_count must be an integer from 2 through {MAX_PORTS}")
        self.definition = definition
        self.port_count = port_count
        self.clock = 0
        self.receipts: list[Receipt] = []
        self.samples: list[ObserverSample] = []

    def receive(self, event: dict[str, object]) -> None:
        position = event.get("position")
        if not isinstance(position, (tuple, list)) or tuple(position) != self.definition.position:
            return
        kind = event.get("event")
        if kind == "cycle_committed":
            self.clock += 1
            return
        if kind == "received":
            label = event.get("disturbance")
            if not isinstance(label, str):
                raise ValueError("a received disturbance needs its configured type label")
            batch = [self._receipt("disturbance", event.get("port"), label, event.get("values"))]
        elif kind == "spatial_received":
            ports = event.get("received_fields")
            if not isinstance(ports, (list, tuple)) or len(ports) != self.port_count:
                raise ValueError("spatial reception requires every configured receiver-port reading")
            batch = [
                self._receipt("field", port, "Field reception", values)
                for port, values in enumerate(ports)
                if values
            ]
        else:
            return
        if len(self.receipts) + len(batch) > self.definition.max_receipts:
            raise ValueError(
                "observer receipt archive capacity exceeded; recording stopped before appending "
                "this reception batch"
            )
        for receipt in batch:
            receipt["sequence"] = len(self.receipts) + 1
            self.receipts.append(receipt)

    def _receipt(self, kind: str, port: object, label: str, values: object) -> Receipt:
        if type(port) is not int or not 0 <= port < self.port_count:
            raise ValueError("reception port must be one of the configured receiver sides")
        return Receipt(
            sequence=0, clock=self.clock, kind=kind, port=port, label=label, values=_values(values)
        )

    def capture(self, audit_tick: int) -> None:
        """Save an exact prefix at capture time, even for two frames at one tick."""
        self.samples.append(
            ObserverSample(audit_tick=audit_tick, clock=self.clock, received_count=len(self.receipts))
        )

    def recording(self) -> dict[str, object]:
        return {
            "model": MODEL,
            "position": self.definition.position,
            "clock_kind": "completed-local-cycles",
            "max_receipts": self.definition.max_receipts,
            "samples": self.samples,
            "receipts": self.receipts,
        }
