"""Read-only local transition checks using the shared bounded vector evaluator."""

from collections import OrderedDict
from collections.abc import Callable, Hashable
from dataclasses import dataclass
from dataclasses import field as dataclass_field

from event_universe.core.disturbance_state import (
    MAX_SLOTS,
    DisturbanceRecord,
    Expression,
    FieldDefinition,
    OperationCosts,
    Values,
    pack,
    unpack,
)
from event_universe.core.integer import checked_work
from event_universe.core.node_conservation import (
    LocalInventory,
    NodeConservationDefinition,
)
from event_universe.core.spatial_state import SpatialBundle, SpatialFieldDefinition
from event_universe.core.validation import ValidationMeter

from .disturbances import evaluate

Readout = tuple[int, ...]
Readouts = tuple[Readout, ...]
RecordKey = tuple[int, int, Values]
SpatialKey = tuple[int, SpatialBundle]


def _add(amount: list[int], values: tuple[int, ...]) -> None:
    for index, value in enumerate(values):
        amount[index] = checked_work(amount[index] + value)


class ReadoutReuse[Key: Hashable]:
    """Bounded least-recently-used host cache of successful readouts.

    This keeps the serial policy of ``core.plan_reuse``, which the generic
    calculation layer may not import: exact key equality, a fixed capacity as a
    host memory bound, and no retained failure. It shares host work only.
    """

    __slots__ = ("capacity", "_entries", "requests", "evaluations", "hits")

    def __init__(self, capacity: int = 4096) -> None:
        if type(capacity) is not int or capacity < 0:
            raise ValueError("readout reuse capacity must be a nonnegative integer")
        self.capacity = capacity
        self._entries: OrderedDict[Key, Readout] = OrderedDict()
        self.requests = 0
        self.evaluations = 0
        self.hits = 0

    def one(self, key: Key, evaluate: Callable[[], Readout]) -> Readout:
        self.requests += 1
        if not self.capacity:
            self.evaluations += 1
            return evaluate()
        try:
            result = self._entries[key]
        except KeyError:
            self.evaluations += 1
            result = evaluate()
            self._entries[key] = result
            if len(self._entries) > self.capacity:
                self._entries.popitem(last=False)
        else:
            self.hits += 1
            self._entries.move_to_end(key)
        return result

    def report(self) -> dict[str, int]:
        return {
            "capacity": self.capacity,
            "entries": len(self._entries),
            "requests": self.requests,
            "evaluations": self.evaluations,
            "hits": self.hits,
        }


@dataclass(frozen=True, slots=True)
class LocalBalanceGuard:
    """Check a configured closed transition without reading world state or repairing it.

    Definitions are shared immutable model data. Every invocation allocates only
    fixed-schema temporaries and returns no physical update or modeled work cost.
    The supplied readouts are model assumptions, not inferred physical quantities.

    A readout is a pure function of one quantity and one immutable payload, so
    equal payloads reuse a bounded host cache of earlier successful readouts.
    Validation belongs to the first evaluation; failures are never retained.
    The cache shares host work only, never a physical update or modeled cost.
    """

    fields: tuple[FieldDefinition, ...]
    spatial_fields: tuple[SpatialFieldDefinition, ...]
    costs: OperationCosts
    definition: NodeConservationDefinition
    degree: int = 6
    _record_readouts: ReadoutReuse[RecordKey] = dataclass_field(
        default_factory=ReadoutReuse, compare=False, repr=False
    )
    _spatial_readouts: ReadoutReuse[SpatialKey] = dataclass_field(
        default_factory=ReadoutReuse, compare=False, repr=False
    )

    def _evaluate(self, expression: Expression, values: Values, size: int) -> Readout:
        result = evaluate(expression, values, values, ValidationMeter(self.costs))
        if len(result) != size:
            raise ValueError("conservation readout has an incompatible component count")
        return tuple(checked_work(value) for value in result)

    def _record(self, record: DisturbanceRecord, index: int) -> Readout:
        return self._record_readouts.one(
            (index, record.type_index, record.values), lambda: self._record_readout(record, index)
        )

    def _spatial(self, bundle: SpatialBundle, index: int) -> Readout:
        return self._spatial_readouts.one((index, bundle), lambda: self._spatial_readout(bundle, index))

    def _record_readout(self, record: DisturbanceRecord, index: int) -> Readout:
        quantity = self.definition.quantities[index]
        matches = tuple(item for item in quantity.carriers if record.type_index in item.types)
        if len(matches) != 1:
            raise ValueError("conservation readout must cover each disturbance layout exactly once")
        if len(record.values) != len(self.fields):
            raise ValueError("conservation record has an incompatible field layout")
        for field, values in zip(self.fields, record.values, strict=True):
            field.validate(values)
        return self._evaluate(matches[0].expression, record.values, quantity.components)

    def _spatial_readout(self, bundle: SpatialBundle, index: int) -> Readout:
        quantity = self.definition.quantities[index]
        if not self.spatial_fields:
            if bundle or quantity.spatial is not None:
                raise ValueError("unexpected spatial conservation owner")
            return (0,) * quantity.components
        if quantity.spatial is None:
            raise ValueError("spatial conservation readout is required")
        if len(bundle) != len(self.spatial_fields):
            raise ValueError("conservation spatial bundle has an incompatible layout")
        values = [pack((0,) * field.components) for field in self.fields]
        for definition, populations in zip(self.spatial_fields, bundle, strict=True):
            field = self.fields[definition.field]
            if len(populations) != 8:
                raise ValueError("conservation spatial owner requires eight populations")
            amount = [0] * field.components
            for payload in populations:
                field.validate(payload)
                for index, component in enumerate(unpack(payload)):
                    amount[index] = checked_work(amount[index] + component)
            values[definition.field] = pack(tuple(amount))
        return self._evaluate(quantity.spatial, tuple(values), quantity.components)

    def validate_empty(self) -> None:
        """Absence of spatial stock cannot contribute a constant readout offset."""
        if not self.definition.quantities:
            raise ValueError("a conservation contract requires at least one quantity")
        zeros = tuple(
            (pack((0,) * self.fields[item.field].components),) * 8 for item in self.spatial_fields
        )
        for index in range(len(self.definition.quantities)):
            if any(self._spatial(zeros, index)):
                raise ValueError("empty spatial inventory must have zero conserved readouts")

    def measure(self, inventory: LocalInventory) -> Readouts:
        if len(inventory.records) > MAX_SLOTS:
            raise ValueError("local conservation record capacity exceeded")
        if len(inventory.carrier_packets) > self.degree * MAX_SLOTS:
            raise ValueError("local conservation transfer capacity exceeded")
        if len(inventory.spatial_packets) > self.degree * 2:
            raise ValueError("local conservation spatial transfer capacity exceeded")
        totals = []
        for index, quantity in enumerate(self.definition.quantities):
            amount = [0] * quantity.components
            for record in inventory.records:
                if record is not None:
                    _add(amount, self._record(record, index))
            for record in inventory.carrier_packets:
                _add(amount, self._record(record, index))
            if inventory.spatial:
                _add(amount, self._spatial(inventory.spatial, index))
            for packet in inventory.spatial_packets:
                _add(amount, self._spatial(packet, index))
            totals.append(tuple(amount))
        return tuple(totals)

    def check(self, before: LocalInventory, after: LocalInventory, label: str) -> None:
        original, candidate = self.measure(before), self.measure(after)
        for quantity, first, second in zip(self.definition.quantities, original, candidate, strict=True):
            if first != second:
                raise ValueError(
                    f"{label} violates conserved readout {quantity.name}: {first} -> {second}"
                )
