"""Passive event-level energy/momentum accounting over actual physical owners.

This host observer can reject a run after a committed event. It never repairs
state or contributes computation cost to the model. Measurements are explicitly
configured candidate quantities, not physical laws inferred from field names.
"""

from collections.abc import Callable
from typing import cast

from event_universe.core.conservation_state import (
    InventoryPacket,
    InventoryView,
    QuantityExpressions,
)
from event_universe.core.disturbance_state import (
    Address3,
    DisturbanceRecord,
    InitialState,
    Values,
    pack,
    unpack,
)
from event_universe.core.integer import checked_work
from event_universe.core.topology import neighbor_address
from event_universe.core.validation import ValidationMeter
from event_universe.fields.disturbances import evaluate

Quantity = tuple[int, int, int, int]
PacketKey = tuple[str, Address3, int, int]
ZERO: Quantity = (0, 0, 0, 0)
EVENTS = frozenset(
    {"spatial_cycle", "spatial_received", "cycle_committed", "received", "escaped", "spatial_escaped"}
)


def _add(left: Quantity, right: Quantity) -> Quantity:
    return cast(Quantity, tuple(checked_work(a + b) for a, b in zip(left, right, strict=True)))


def _subtract(left: Quantity, right: Quantity) -> Quantity:
    return cast(Quantity, tuple(checked_work(a - b) for a, b in zip(left, right, strict=True)))


def _plain(quantity: Quantity) -> dict[str, object]:
    return {"energy": quantity[0], "momentum": quantity[1:]}


def validate_empty_measurement(initial: InitialState) -> None:
    """Check diagnostic zero consistency without constructing or updating a world."""
    if initial.conservation is None or initial.conservation.spatial is None:
        return
    values = tuple(pack((0,) * field.components) for field in initial.fields)
    meter = ValidationMeter(initial.operation_costs)
    quantities = initial.conservation.spatial
    if any(evaluate(quantities.energy, values, values, meter)) or any(
        evaluate(quantities.momentum, values, values, meter)
    ):
        raise ValueError("empty spatial inventory must have zero energy and momentum")


class LocalConservationAudit:
    """Compare each committed node change with measured actual link transfers."""

    def __init__(self, initial: InitialState, inventory: Callable[[], InventoryView]) -> None:
        assert initial.conservation is not None
        self.initial = initial
        self.definition = initial.conservation
        self.inventory = inventory
        self.checks = 0
        self.failure: dict[str, object] | None = None
        self.escaped: Quantity = ZERO
        validate_empty_measurement(initial)
        self._nodes, self._packets = self._measure(inventory())
        self.initial_total = self._total(self._nodes, self._packets)
        self.current_total = self.initial_total

    def _evaluate(self, expressions: QuantityExpressions, values: Values) -> Quantity:
        # The evaluator's bounded arithmetic remains active; its meter is private
        # host bookkeeping and is never returned to a planner or scheduler.
        meter = ValidationMeter(self.initial.operation_costs)
        energy = evaluate(expressions.energy, values, values, meter)
        momentum = evaluate(expressions.momentum, values, values, meter)
        if len(energy) != 1 or len(momentum) != 3:
            raise ValueError("conservation measurements require scalar energy and vector momentum")
        return (energy[0], momentum[0], momentum[1], momentum[2])

    def _carrier(self, record: DisturbanceRecord) -> Quantity:
        for measurement in self.definition.carriers:
            if record.type_index in measurement.types:
                return self._evaluate(measurement.quantities, record.values)
        raise ValueError("conservation measurement missing for a disturbance layout")

    def _spatial(self, populations: tuple[tuple[tuple[int, ...], ...], ...]) -> Quantity:
        if self.definition.spatial is None:
            return ZERO
        values = [pack((0,) * field.components) for field in self.initial.fields]
        for definition, owned in zip(self.initial.spatial_fields, populations, strict=True):
            components = [0] * self.initial.fields[definition.field].components
            for payload in owned:
                for index, value in enumerate(unpack(payload)):
                    components[index] = checked_work(components[index] + value)
            values[definition.field] = pack(tuple(components))
        return self._evaluate(self.definition.spatial, tuple(values))

    def _packet(self, packet: InventoryPacket) -> Quantity:
        if packet.record is not None:
            return self._carrier(packet.record)
        return self._spatial(packet.spatial)

    def _measure(
        self, view: InventoryView
    ) -> tuple[dict[Address3, Quantity], dict[PacketKey, tuple[InventoryPacket, Quantity]]]:
        nodes: dict[Address3, Quantity] = {}
        for node in view.nodes:
            amount = self._spatial(tuple(state.populations for state in node.spatial))
            for record in node.records:
                if record is not None:
                    amount = _add(amount, self._carrier(record))
            nodes[node.position] = amount
        packets = {
            (packet.kind, packet.origin, packet.slot, packet.arrival_tick): (
                packet,
                self._packet(packet),
            )
            for packet in view.packets
        }
        return nodes, packets

    @staticmethod
    def _total(
        nodes: dict[Address3, Quantity], packets: dict[PacketKey, tuple[InventoryPacket, Quantity]]
    ) -> Quantity:
        # Global accumulation is an unbounded host diagnostic, not local work.
        quantities = [*nodes.values(), *(amount for _, amount in packets.values())]
        return cast(Quantity, tuple(sum(value[c] for value in quantities) for c in range(4)))

    def observe(self, event: dict[str, object]) -> None:
        if event.get("event") not in EVENTS:
            return
        tick = cast(int, event["tick"])
        try:
            self._check(tick, str(event["event"]))
        except (ValueError, OverflowError) as error:
            if self.failure is None:
                self.failure = {"tick": tick, "event": event["event"], "message": str(error)}
            raise

    def _check(self, tick: int, event: str) -> None:
        nodes, packets = self._measure(self.inventory())
        incoming: dict[Address3, Quantity] = {}
        outgoing: dict[Address3, Quantity] = {}
        escaped: Quantity = ZERO
        for key, (old, amount) in self._packets.items():
            if key in packets:
                new, current = packets[key]
                if old.port != new.port:
                    raise ValueError("conservation audit found an altered in-flight packet port")
                delta = _subtract(current, amount)
                if delta != ZERO:
                    if old.arrival_tick != tick + self.initial.link_ticks:
                        raise ValueError("conservation audit found an altered in-flight packet")
                    outgoing[old.origin] = _add(outgoing.get(old.origin, ZERO), delta)
                continue
            if old.arrival_tick != tick:
                raise ValueError("conservation audit found a packet removed before arrival")
            target = neighbor_address(old.origin, old.port, self.initial.shape, self.initial.boundary)
            if target is None:
                escaped = _add(escaped, amount)
            else:
                incoming[target] = _add(incoming.get(target, ZERO), amount)
        for key, (packet, amount) in packets.items():
            if key not in self._packets:
                outgoing[packet.origin] = _add(outgoing.get(packet.origin, ZERO), amount)
        self.current_total = self._total(nodes, packets)
        for position in sorted(self._nodes.keys() | nodes.keys() | incoming.keys() | outgoing.keys()):
            before, after = self._nodes.get(position, ZERO), nodes.get(position, ZERO)
            arrived, sent = incoming.get(position, ZERO), outgoing.get(position, ZERO)
            residual = _add(_subtract(after, before), _subtract(sent, arrived))
            self.checks += 1
            if residual != ZERO:
                self.failure = {
                    "tick": tick,
                    "event": event,
                    "position": position,
                    "before": _plain(before),
                    "after": _plain(after),
                    "incoming": _plain(arrived),
                    "outgoing": _plain(sent),
                    "residual": _plain(residual),
                }
                raise ValueError(f"local energy/momentum conservation failed at {position}: {residual}")
        self.escaped = cast(Quantity, tuple(a + b for a, b in zip(self.escaped, escaped, strict=True)))
        self._nodes, self._packets = nodes, packets

    def report(self) -> dict[str, object]:
        return {
            "status": "passed" if self.failure is None else "failed",
            "name": self.definition.name,
            "energy_units": self.definition.energy_units,
            "momentum_units": self.definition.momentum_units,
            "checked_node_events": self.checks,
            "initial": _plain(self.initial_total),
            "current": _plain(self.current_total),
            "escaped": _plain(self.escaped),
            "failure": self.failure,
        }
