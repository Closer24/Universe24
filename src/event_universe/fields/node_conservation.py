"""Read-only local transition checks using the shared bounded vector evaluator."""

from dataclasses import dataclass

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
    ConservedReadout,
    LocalInventory,
    NodeConservationDefinition,
)
from event_universe.core.spatial_state import SpatialBundle, SpatialFieldDefinition
from event_universe.core.validation import ValidationMeter

from .disturbances import evaluate

Readouts = tuple[tuple[int, ...], ...]


def _add(amount: list[int], values: tuple[int, ...]) -> None:
    for index, value in enumerate(values):
        amount[index] = checked_work(amount[index] + value)


@dataclass(frozen=True, slots=True)
class LocalBalanceGuard:
    """Check a configured closed transition without reading world state or repairing it.

    Definitions are shared immutable model data. Every invocation allocates only
    fixed-schema temporaries and returns no physical update or modeled work cost.
    The supplied readouts are model assumptions, not inferred physical quantities.
    """

    fields: tuple[FieldDefinition, ...]
    spatial_fields: tuple[SpatialFieldDefinition, ...]
    costs: OperationCosts
    definition: NodeConservationDefinition
    degree: int = 6

    def _evaluate(self, expression: Expression, values: Values, size: int) -> tuple[int, ...]:
        result = evaluate(expression, values, values, ValidationMeter(self.costs))
        if len(result) != size:
            raise ValueError("conservation readout has an incompatible component count")
        return tuple(checked_work(value) for value in result)

    def _record(self, record: DisturbanceRecord, quantity: ConservedReadout) -> tuple[int, ...]:
        matches = tuple(item for item in quantity.carriers if record.type_index in item.types)
        if len(matches) != 1:
            raise ValueError("conservation readout must cover each disturbance layout exactly once")
        if len(record.values) != len(self.fields):
            raise ValueError("conservation record has an incompatible field layout")
        for field, values in zip(self.fields, record.values, strict=True):
            field.validate(values)
        return self._evaluate(matches[0].expression, record.values, quantity.components)

    def _spatial(self, bundle: SpatialBundle, quantity: ConservedReadout) -> tuple[int, ...]:
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
        for quantity in self.definition.quantities:
            if any(self._spatial(zeros, quantity)):
                raise ValueError("empty spatial inventory must have zero conserved readouts")

    def measure(self, inventory: LocalInventory) -> Readouts:
        if len(inventory.records) > MAX_SLOTS:
            raise ValueError("local conservation record capacity exceeded")
        if len(inventory.carrier_packets) > self.degree * MAX_SLOTS:
            raise ValueError("local conservation transfer capacity exceeded")
        if len(inventory.spatial_packets) > self.degree * 2:
            raise ValueError("local conservation spatial transfer capacity exceeded")
        totals = []
        for quantity in self.definition.quantities:
            amount = [0] * quantity.components

            for record in inventory.records:
                if record is not None:
                    _add(amount, self._record(record, quantity))
            for record in inventory.carrier_packets:
                _add(amount, self._record(record, quantity))
            if inventory.spatial:
                _add(amount, self._spatial(inventory.spatial, quantity))
            for packet in inventory.spatial_packets:
                _add(amount, self._spatial(packet, quantity))
            totals.append(tuple(amount))
        return tuple(totals)

    def check(self, before: LocalInventory, after: LocalInventory, label: str) -> None:
        original, candidate = self.measure(before), self.measure(after)
        for quantity, first, second in zip(self.definition.quantities, original, candidate, strict=True):
            if first != second:
                raise ValueError(
                    f"{label} violates conserved readout {quantity.name}: {first} -> {second}"
                )
