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
from event_universe.core.spatial_state import Rays
from event_universe.core.topology import neighbor_address
from event_universe.core.validation import ValidationMeter
from event_universe.fields.disturbances import evaluate

# Energy, the three momentum components and, since ray-event-audit-v1, charge.
Quantity = tuple[int, int, int, int, int]
PacketKey = tuple[str, Address3, int, int]
ZERO: Quantity = (0, 0, 0, 0, 0)
EVENTS = frozenset(
    {"spatial_cycle", "spatial_received", "cycle_committed", "received", "escaped", "spatial_escaped"}
)


def _add(left: Quantity, right: Quantity) -> Quantity:
    return cast(Quantity, tuple(checked_work(a + b) for a, b in zip(left, right, strict=True)))


def _subtract(left: Quantity, right: Quantity) -> Quantity:
    return cast(Quantity, tuple(checked_work(a - b) for a, b in zip(left, right, strict=True)))


def _plain(quantity: Quantity, charged: bool = False) -> dict[str, object]:
    plain: dict[str, object] = {"energy": quantity[0], "momentum": quantity[1:4]}
    if charged:
        plain["charge"] = quantity[4]
    return plain


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
        # Content annulled at inverse splits (inverse-split-v1): the world total and
        # what each Node annulled since its last check.
        self.annulled: Quantity = ZERO
        # Content released as a field (released-field-v1): an explicitly accounted
        # source at the Node that released it, the world total (ray-event-audit-v1).
        self.sourced: Quantity = ZERO
        self._pending_annulled: dict[Address3, Quantity] = {}
        validate_empty_measurement(initial)
        # The charged ray families (ray-event-audit-v1): the audit measures their
        # charge, charge x amount over rays and over held stock, beside energy and
        # momentum, and reports it when any family declares a charge.
        self._charges = {
            definition.field: definition.charge
            for definition in initial.spatial_fields
            if definition.rays and definition.charge
        }
        self.charged = bool(self._charges)
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
        return (energy[0], momentum[0], momentum[1], momentum[2], 0)

    def _carrier(self, record: DisturbanceRecord) -> Quantity:
        for measurement in self.definition.carriers:
            if record.type_index in measurement.types:
                energy, px, py, pz, _ = self._evaluate(measurement.quantities, record.values)
                # The stock a record holds of a charged family reads charge x stock.
                charge = 0
                for field, per_quantum in self._charges.items():
                    stock = unpack(record.values[field])[0]
                    charge = checked_work(charge + checked_work(stock * per_quantum))
                return (energy, px, py, pz, charge)
        raise ValueError("conservation measurement missing for a disturbance layout")

    def _spatial(
        self,
        populations: tuple[tuple[tuple[int, ...], ...], ...],
        rays: tuple[Rays, ...] = (),
    ) -> Quantity:
        """Octant stock feeds the declared expressions; rays add their own quanta.

        A ray of amount a carries energy a through the declared spatial energy
        expression (its amount joins the field value) and momentum a x heading
        intrinsically, in amount times heading units, which no field expression
        can see. The spatial momentum expression must not count ray fields.
        """
        if self.definition.spatial is None:
            return ZERO
        values = [pack((0,) * field.components) for field in self.initial.fields]
        intrinsic = [0, 0, 0]
        charge = 0
        for index, (definition, owned) in enumerate(
            zip(self.initial.spatial_fields, populations, strict=True)
        ):
            components = [0] * self.initial.fields[definition.field].components
            for payload in owned:
                for component, value in enumerate(unpack(payload)):
                    components[component] = checked_work(components[component] + value)
            if definition.rays and rays and index < len(rays):
                for ray in rays[index]:
                    components[0] = checked_work(components[0] + ray.amount)
                    # A returning ray reads as its share on the event's heading, its
                    # own heading negated (detector-return-v1), and its charge as
                    # charge x amount like any ray (ray-event-audit-v1).
                    heading = definition.headings[ray.heading]
                    sign = 1 if ray.outbound else -1
                    for axis in range(3):
                        intrinsic[axis] = checked_work(
                            intrinsic[axis] + sign * ray.amount * heading[axis]
                        )
                    charge = checked_work(charge + checked_work(ray.amount * definition.charge))
            values[definition.field] = pack(tuple(components))
        energy, px, py, pz, _ = self._evaluate(self.definition.spatial, tuple(values))
        return (
            energy,
            checked_work(px + intrinsic[0]),
            checked_work(py + intrinsic[1]),
            checked_work(pz + intrinsic[2]),
            charge,
        )

    def _annulled(self, event: dict[str, object]) -> Quantity:
        """The quantity an inverse split in annul mode removed from its Node: the ray
        field's amount through the declared energy expression, the momentum field's
        vector as the intrinsic momentum, as `_spatial` reads a resident ray."""
        if self.definition.spatial is None:
            return ZERO
        annulled = cast(dict[str, tuple[int, ...]], event.get("annulled", {}))
        values = [pack((0,) * field.components) for field in self.initial.fields]
        intrinsic = [0, 0, 0]
        charge = 0
        for definition in self.initial.spatial_fields:
            name = self.initial.fields[definition.field].name
            if definition.rays and name in annulled:
                values[definition.field] = pack(tuple(annulled[name]))
                charge = checked_work(charge + checked_work(annulled[name][0] * definition.charge))
                if definition.momentum_field is not None:
                    momentum = annulled.get(self.initial.fields[definition.momentum_field].name)
                    if momentum is not None:
                        for axis in range(3):
                            intrinsic[axis] = checked_work(intrinsic[axis] + momentum[axis])
        energy, px, py, pz, _ = self._evaluate(self.definition.spatial, tuple(values))
        return (
            energy,
            checked_work(px + intrinsic[0]),
            checked_work(py + intrinsic[1]),
            checked_work(pz + intrinsic[2]),
            charge,
        )

    def _packet(self, packet: InventoryPacket) -> Quantity:
        if packet.record is not None:
            return self._carrier(packet.record)
        return self._spatial(packet.spatial, packet.rays)

    def _released(self, packet: InventoryPacket) -> Quantity:
        """What a new packet carries that its origin released in the cycle that sent
        it (released-field-v1): the rays of a field family with no event and one
        Link walked, measured like any rays. A release is booked as a source and
        no owner pays for it, so it is a source term at the Node, not a residual
        (ray-event-audit-v1); an emitted or transmitted ray carries its event's
        mask, and a field ray that crosses the Node has walked more than one Link."""
        if packet.record is not None or not packet.rays:
            return ZERO
        rays = tuple(
            tuple(ray for ray in bundle if ray.outbound and ray.steps == 1 and not ray.event_ports)
            if definition.field_of is not None
            else ()
            for definition, bundle in zip(self.initial.spatial_fields, packet.rays, strict=True)
        )
        if not any(rays):
            return ZERO
        return self._spatial(tuple(() for _ in self.initial.spatial_fields), rays)

    def _measure(
        self, view: InventoryView
    ) -> tuple[dict[Address3, Quantity], dict[PacketKey, tuple[InventoryPacket, Quantity]]]:
        nodes: dict[Address3, Quantity] = {}
        for node in view.nodes:
            amount = self._spatial(tuple(state.populations for state in node.spatial), node.rays)
            if node.incoming_spatial:
                amount = _add(amount, self._spatial(tuple(s.populations for s in node.incoming_spatial)))
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
        return cast(Quantity, tuple(sum(value[c] for value in quantities) for c in range(5)))

    def observe(self, event: dict[str, object]) -> None:
        if event.get("event") == "inverse_split" and event.get("mode") == "annul":
            position = cast(Address3, tuple(cast(tuple[int, int, int], event["position"])))
            amount = self._annulled(event)
            self._pending_annulled[position] = _add(self._pending_annulled.get(position, ZERO), amount)
            self.annulled = _add(self.annulled, amount)
            return
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
        sourced: dict[Address3, Quantity] = {}
        for key, (packet, amount) in packets.items():
            if key not in self._packets:
                outgoing[packet.origin] = _add(outgoing.get(packet.origin, ZERO), amount)
                released = self._released(packet)
                if released != ZERO:
                    sourced[packet.origin] = _add(sourced.get(packet.origin, ZERO), released)
        self.current_total = self._total(nodes, packets)
        for position in sorted(self._nodes.keys() | nodes.keys() | incoming.keys() | outgoing.keys()):
            before, after = self._nodes.get(position, ZERO), nodes.get(position, ZERO)
            arrived, sent = incoming.get(position, ZERO), outgoing.get(position, ZERO)
            residual = _add(_subtract(after, before), _subtract(sent, arrived))
            # What the Node annulled left it for the explicit sink, not for a Link.
            residual = _add(residual, self._pending_annulled.pop(position, ZERO))
            # What the Node released as a field came from no owner: a source.
            residual = _subtract(residual, sourced.get(position, ZERO))
            self.checks += 1
            if residual != ZERO:
                self.failure = {
                    "tick": tick,
                    "event": event,
                    "position": position,
                    "before": _plain(before, self.charged),
                    "after": _plain(after, self.charged),
                    "incoming": _plain(arrived, self.charged),
                    "outgoing": _plain(sent, self.charged),
                    "residual": _plain(residual, self.charged),
                }
                raise ValueError(f"local energy/momentum conservation failed at {position}: {residual}")
        self.escaped = cast(Quantity, tuple(a + b for a, b in zip(self.escaped, escaped, strict=True)))
        for released in sourced.values():
            self.sourced = _add(self.sourced, released)
        self._nodes, self._packets = nodes, packets

    def report(self) -> dict[str, object]:
        return {
            "status": "passed" if self.failure is None else "failed",
            "name": self.definition.name,
            "energy_units": self.definition.energy_units,
            "momentum_units": self.definition.momentum_units,
            "checked_node_events": self.checks,
            "initial": _plain(self.initial_total, self.charged),
            "sourced": _plain(self.sourced, self.charged),
            "current": _plain(self.current_total, self.charged),
            "escaped": _plain(self.escaped, self.charged),
            "annulled": _plain(self.annulled, self.charged),
            "failure": self.failure,
        }
