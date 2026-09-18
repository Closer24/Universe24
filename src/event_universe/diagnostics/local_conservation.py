"""Passive event-level energy/momentum accounting over actual physical owners.

This host observer can reject a run after a committed event. It never repairs
state or contributes computation cost to the model. Measurements are explicitly
configured candidate quantities, not physical laws inferred from field names.
"""

from collections.abc import Callable, Sequence
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
from event_universe.core.spatial_state import (
    BIT_THING,
    Rays,
    ledger_momentum,
    parked_momentum,
    parked_stock,
)
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
        # Content sourced at a Node (ray-event-audit-v1): since bit-law-v1 nothing
        # is released during a run, a spread moves content and a shadow that comes
        # home leaves again with what it brought; the line is kept, at zero.
        self.sourced: Quantity = ZERO
        # Content a Detector mark absorbed on a click (detector-absorb-v1): the world
        # total and what each Node's mark absorbed since its last check, read from
        # the reception record before the Node is checked.
        self.absorbed_by_marks: Quantity = ZERO
        self._pending_absorbed: dict[Address3, Quantity] = {}
        # The momentum delivered outside the measurement (bit-law-v1): to an
        # external body by a push or a homecoming, or to a record without a
        # recoil field, read from the Node's records before it is checked.
        self.returned: Quantity = ZERO
        self._pending_returned: dict[Address3, Quantity] = {}
        # The momentum the things spent on their steps (clock-readings-v1): it
        # left the rays at the Node for the momentum field's line.
        self._pending_spent: dict[Address3, Quantity] = {}
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
        parked: tuple[Rays, ...] = (),
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
                    if ray.parked:
                        continue
                    components[0] = checked_work(components[0] + ray.amount)
                    # The momentum as the ledger reads it (bit-law-v1): a thing its
                    # momentum or amount x heading, negated on its walk back
                    # (detector-return-v1); a shadow zero outbound and -dp on its
                    # walk home. A thing's charge is charge x amount; a shadow
                    # carries none (ray-event-audit-v1).
                    for axis, value in enumerate(ledger_momentum(ray, definition)):
                        intrinsic[axis] = checked_work(intrinsic[axis] + value)
                    if ray.detector == BIT_THING:
                        charge = checked_work(charge + checked_work(ray.amount * definition.charge))
            if definition.spread and parked and index < len(parked) and parked[index]:
                # The Node's parked shadows hold whole quanta in total, shadow
                # content without charge (node-is-ports-v1), with the momentum
                # they hold in flight (return-field-v1).
                components[0] = checked_work(components[0] + parked_stock(parked[index], definition))
                for axis, value in enumerate(parked_momentum(parked[index])):
                    intrinsic[axis] = checked_work(intrinsic[axis] + value)
            values[definition.field] = pack(tuple(components))
        energy, px, py, pz, _ = self._evaluate(self.definition.spatial, tuple(values))
        return (
            energy,
            checked_work(px + intrinsic[0]),
            checked_work(py + intrinsic[1]),
            checked_work(pz + intrinsic[2]),
            charge,
        )

    def _absorbed(self, event: dict[str, object]) -> Quantity:
        """The quantity a Detector mark absorbed on its clicks in one reception
        (detector-absorb-v1): per family the amount through the declared energy
        expression, the momentum the record carries (amount x heading, a register
        where a push set one) as the intrinsic momentum, charge x amount."""
        if self.definition.spatial is None:
            return ZERO
        taken = cast(dict[str, dict[str, object]], event.get("absorbed_by_mark", {}))
        values = [pack((0,) * field.components) for field in self.initial.fields]
        intrinsic = [0, 0, 0]
        charge = 0
        for definition in self.initial.spatial_fields:
            name = self.initial.fields[definition.field].name
            if definition.rays and name in taken:
                amount = cast(int, taken[name]["amount"])
                values[definition.field] = pack((amount,))
                charge = checked_work(charge + checked_work(amount * definition.charge))
                for axis, value in enumerate(cast(Sequence[int], taken[name]["momentum"])):
                    intrinsic[axis] = checked_work(intrinsic[axis] + value)
        energy, px, py, pz, _ = self._evaluate(self.definition.spatial, tuple(values))
        return (
            energy,
            checked_work(px + intrinsic[0]),
            checked_work(py + intrinsic[1]),
            checked_work(pz + intrinsic[2]),
            charge,
        )

    @staticmethod
    def _outside(momentum: Sequence[int]) -> Quantity:
        """Momentum delivered outside the measurement, as a quantity."""
        return (0, int(momentum[0]), int(momentum[1]), int(momentum[2]), 0)

    def _packet(self, packet: InventoryPacket) -> Quantity:
        if packet.record is not None:
            return self._carrier(packet.record)
        return self._spatial(packet.spatial, packet.rays)

    def _measure(
        self, view: InventoryView
    ) -> tuple[dict[Address3, Quantity], dict[PacketKey, tuple[InventoryPacket, Quantity]]]:
        nodes: dict[Address3, Quantity] = {}
        for node in view.nodes:
            amount = self._spatial(
                tuple(state.populations for state in node.spatial), node.rays, node.parked
            )
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
        if event.get("event") not in EVENTS:
            return
        if event.get("event") == "spatial_cycle" and event.get("returned"):
            # Shadows came home this cycle (bit-law-v1): the momentum delivered to a
            # record without a recoil field left the measurement on the returned line.
            position = cast(Address3, tuple(cast(tuple[int, int, int], event["position"])))
            for entry in cast(dict[str, dict[str, object]], event["returned"]).values():
                amount = self._outside(cast(Sequence[int], entry["momentum"]))
                if amount != ZERO:
                    self._pending_returned[position] = _add(
                        self._pending_returned.get(position, ZERO), amount
                    )
                    self.returned = _add(self.returned, amount)
        if event.get("event") == "spatial_cycle" and event.get("spent"):
            # The momentum the things spent on their steps this cycle
            # (clock-readings-v1, the settled rule (i)) left the rays for the
            # momentum field's line, outside the measurement.
            position = cast(Address3, tuple(cast(tuple[int, int, int], event["position"])))
            for vector in cast(dict[str, Sequence[int]], event["spent"]).values():
                if len(vector) == 3:
                    self._pending_spent[position] = _add(
                        self._pending_spent.get(position, ZERO), self._outside(vector)
                    )
        if event.get("event") == "spatial_received" and event.get("absorbed_by_mark"):
            # What the Node's mark absorbed on its clicks left it for the marks'
            # sink, not for a Link (detector-absorb-v1), read before the check.
            position = cast(Address3, tuple(cast(tuple[int, int, int], event["position"])))
            amount = self._absorbed(event)
            self._pending_absorbed[position] = _add(self._pending_absorbed.get(position, ZERO), amount)
            self.absorbed_by_marks = _add(self.absorbed_by_marks, amount)
        if event.get("event") == "spatial_received" and event.get("returned_to_body"):
            # What the shadows delivered to the Node's body (bit-law-v1): the push
            # of every shadow of a named family and the -dp of every shadow of
            # the body's own that came home, outside the measurement.
            position = cast(Address3, tuple(cast(tuple[int, int, int], event["position"])))
            taken = cast(dict[str, dict[str, object]], event["returned_to_body"])
            for entry in taken.values():
                amount = self._outside(cast(Sequence[int], entry["momentum"]))
                self._pending_returned[position] = _add(
                    self._pending_returned.get(position, ZERO), amount
                )
                self.returned = _add(self.returned, amount)
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
        positions = (
            self._nodes.keys()
            | nodes.keys()
            | incoming.keys()
            | outgoing.keys()
            | self._pending_returned.keys()
            | self._pending_spent.keys()
            | self._pending_absorbed.keys()
        )
        for position in sorted(positions):
            before, after = self._nodes.get(position, ZERO), nodes.get(position, ZERO)
            arrived, sent = incoming.get(position, ZERO), outgoing.get(position, ZERO)
            residual = _add(_subtract(after, before), _subtract(sent, arrived))
            # What the Node's mark absorbed on a click left it for the marks' sink.
            residual = _add(residual, self._pending_absorbed.pop(position, ZERO))
            # The momentum the Node's shadows delivered outside the measurement
            # (bit-law-v1): to its body or to a record without a recoil field.
            residual = _add(residual, self._pending_returned.pop(position, ZERO))
            residual = _add(residual, self._pending_spent.pop(position, ZERO))
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
            "absorbed_by_marks": _plain(self.absorbed_by_marks, self.charged),
            "returned": _plain(self.returned, self.charged),
            "failure": self.failure,
        }
