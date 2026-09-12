"""Generic local record operations selected from immutable initialization data."""

from dataclasses import dataclass, replace

from event_universe.core.disturbance_state import (
    CouplingDefinition,
    DisturbanceDefinition,
    DisturbanceRecord,
    FieldDefinition,
    InteractionDefinition,
    LocalPlan,
    pack,
    unpack,
)
from event_universe.core.integer import add_components


@dataclass(frozen=True)
class RecordOperations:
    """Activity, delivered-record combination and configured cost reporting.

    The scheduler supplies fixed local slots, pending locks and delivered values.
    No method receives positions, time, packets, a cell owner or the whole world.
    Existing arithmetic, slot order and cost accounting are preserved.
    """

    fields: tuple[FieldDefinition, ...]
    disturbances: tuple[DisturbanceDefinition, ...]
    couplings: tuple[CouplingDefinition, ...] = ()
    interactions: tuple[InteractionDefinition, ...] = ()
    spatial_types: frozenset[int] = frozenset()

    def has_work(self, records: tuple[DisturbanceRecord | None, ...]) -> bool:
        present = [record.type_index for record in records if record is not None]
        if self.spatial_types.intersection(present):
            return True
        rules: tuple[CouplingDefinition | InteractionDefinition, ...] = (
            *self.couplings,
            *self.interactions,
        )
        for coupling in rules:
            if coupling.left_type in present and coupling.right_type in present:
                if coupling.left_type != coupling.right_type or present.count(coupling.left_type) > 1:
                    return True
        for record in records:
            if record is not None:
                definition = self.disturbances[record.type_index]
                if definition.transport.mode == "move" and definition.transport.direction_field is None:
                    return True
                if definition.updates or definition.cost_field is not None:
                    return True
                if any(any(unpack(v)) for v in record.values):
                    return True
        return False

    def report_cost(self, plan: LocalPlan) -> LocalPlan:
        """Write already-metered cost reporters after local costs are combined."""
        replacements = []
        for slot, record in plan.replacements:
            if record is not None:
                cost_field = self.disturbances[record.type_index].cost_field
                if cost_field is not None:
                    values = list(record.values)
                    # This reporter assignment was already metered by the local planner.
                    values[cost_field] = pack((plan.cost,))
                    record = replace(record, values=tuple(values))
            replacements.append((slot, record))
        return replace(plan, replacements=tuple(replacements))

    def receive(
        self,
        resident: tuple[DisturbanceRecord | None, ...],
        arrivals: tuple[DisturbanceRecord, ...],
        locked: frozenset[int],
    ) -> tuple[DisturbanceRecord | None, ...]:
        """Prepare all delivered records without mutating residents or packets."""
        records = list(resident)
        for incoming in arrivals:
            definition = self.disturbances[incoming.type_index]
            match = None
            if definition.transport.mode == "split":
                match = next(
                    (
                        slot
                        for slot, old in enumerate(records)
                        if slot not in locked
                        and old is not None
                        and old.type_index == incoming.type_index
                        and old.channel_code == incoming.channel_code
                    ),
                    None,
                )
            if match is not None:
                old = records[match]
                assert old is not None
                combined: list[tuple[int, ...]] = []
                for index, (a, b) in enumerate(zip(old.values, incoming.values, strict=True)):
                    value = pack(add_components(unpack(a), unpack(b)))
                    self.fields[index].validate(value)
                    combined.append(value)
                records[match] = replace(old, values=tuple(combined))
            else:
                try:
                    slot = records.index(None)
                except ValueError as error:
                    raise ValueError(
                        "local receiving capacity exhausted; no disturbance was discarded"
                    ) from error
                records[slot] = incoming
        return tuple(records)
