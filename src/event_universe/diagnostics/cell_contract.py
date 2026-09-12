"""Read-only audit of formula-free evolving cells, records and transit state."""

from dataclasses import fields, is_dataclass
from typing import cast

from event_universe.core.disturbance_state import (
    CellView,
    Departure,
    DisturbanceCell,
    DisturbanceRecord,
    LocalPlan,
    Packet,
    PendingCycle,
)
from event_universe.core.spatial_state import (
    FieldInteractionGuard,
    SpatialCell,
    SpatialPacket,
    SpatialPlan,
    SpatialState,
    WaitingField,
)

# Shared immutable initialization definitions intentionally do not belong here.
STATE_RECORDS = (
    CellView,
    DisturbanceCell,
    DisturbanceRecord,
    LocalPlan,
    Packet,
    PendingCycle,
    FieldInteractionGuard,
    SpatialCell,
    SpatialPacket,
    SpatialPlan,
    SpatialState,
    WaitingField,
)


def cell_state_violations(value: object) -> tuple[str, ...]:
    """Inspect the complete reachable value graph without evaluating any law.

    Only exact numeric state, tuples, and registered state records are allowed.
    Expression trees, definition objects, strings, mappings and callbacks are
    forbidden even when nested inside a pending proposal or a packet payload.
    This is a structural guard, not a proof of locality or of physical accuracy.
    """
    errors: list[str] = []
    active: set[int] = set()

    def visit(item: object, path: str) -> None:
        if item is None or type(item) is int:
            return
        if id(item) in active:
            errors.append(f"{path}: cyclic evolving state")
            return
        active.add(id(item))
        try:
            if type(item) in STATE_RECORDS and is_dataclass(item):
                for member in fields(item):
                    visit(getattr(item, member.name), f"{path}.{member.name}")
            elif type(item) in (tuple, Departure):
                for index, child in enumerate(cast(tuple[object, ...], item)):
                    visit(child, f"{path}[{index}]")
            else:
                errors.append(f"{path}: forbidden cell-state object {type(item).__name__}")
        finally:
            active.remove(id(item))

    visit(value, "state")
    return tuple(errors)
