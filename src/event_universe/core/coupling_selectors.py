"""Bounded compatibility sets shared by scheduling, execution and carried state."""

from collections.abc import Iterable

from .disturbance_state import (
    MAX_SLOTS,
    MAX_TYPES,
    CouplingDefinition,
    DisturbanceRecord,
    InteractionDefinition,
)
from .spatial_state import EmissionDefinition, SpatialCouplingDefinition, SpatialInteractionDefinition

SingleRule = EmissionDefinition | SpatialCouplingDefinition | SpatialInteractionDefinition
PairRule = CouplingDefinition | InteractionDefinition


def _participant_roles(
    rule: InteractionDefinition | SpatialInteractionDefinition,
) -> tuple[tuple[int, ...], ...]:
    roles = rule.participants
    minimum = 1 if isinstance(rule, InteractionDefinition) and rule.outputs else 2
    if type(roles) is not tuple or not minimum <= len(roles) <= MAX_SLOTS:
        raise ValueError("indexed interactions require bounded immutable participant roles")
    for kinds in roles:
        if type(kinds) is not tuple or not 1 <= len(kinds) <= MAX_TYPES:
            raise ValueError("participant compatibility set exceeds the bounded type capacity")
        if any(type(kind) is not int or not 0 <= kind < MAX_TYPES for kind in kinds):
            raise ValueError("participant compatibility requires bounded type indices")
    return roles


def selected_types(rule: SingleRule) -> tuple[int, ...]:
    """Resolve a compiled property selection or a legacy exact layout selector."""
    if isinstance(rule, SpatialInteractionDefinition) and rule.participants:
        return tuple(sorted({kind for role in _participant_roles(rule) for kind in role}))
    return rule.types or (rule.type_index,)


def selected_left_types(rule: PairRule) -> tuple[int, ...]:
    return rule.left_types or (rule.left_type,)


def selected_right_types(rule: PairRule) -> tuple[int, ...]:
    return rule.right_types or (rule.right_type,)


def matches_type(rule: SingleRule, type_index: int) -> bool:
    return type_index in selected_types(rule)


def matches_pair(rule: PairRule, left: int, right: int) -> bool:
    """Check oriented property roles; callers separately exclude the same slot."""
    return left in selected_left_types(rule) and right in selected_right_types(rule)


def participant_groups(
    rule: InteractionDefinition | SpatialInteractionDefinition,
    records: tuple[DisturbanceRecord | None, ...],
) -> tuple[tuple[int, ...], ...]:
    """Greedily select disjoint groups in role order and then local slot order.

    A partial group ends selection. There is no combinatorial search or retry
    with a different assignment, and conditions do not alter this selection.
    """
    roles = _participant_roles(rule)
    if type(records) is not tuple or len(records) > MAX_SLOTS:
        raise ValueError("indexed interactions require bounded participant and record counts")
    available = {slot for slot, record in enumerate(records) if record is not None}
    groups: list[tuple[int, ...]] = []
    for _ in range(len(records) // len(roles)):
        group = []
        for kinds in roles:
            selected = next(
                (
                    slot
                    for slot, record in enumerate(records)
                    if slot in available and record is not None and record.type_index in kinds
                ),
                None,
            )
            if selected is None:
                return tuple(groups)
            available.remove(selected)
            group.append(selected)
        groups.append(tuple(group))
    return tuple(groups)


def selected_type_set(*groups: Iterable[SingleRule]) -> frozenset[int]:
    """Combine rule groups without introducing a second eligibility implementation."""
    return frozenset(kind for group in groups for rule in group for kind in selected_types(rule))
