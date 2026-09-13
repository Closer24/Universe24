"""Bounded compatibility sets shared by scheduling, execution and carried state."""

from collections.abc import Iterable

from .disturbance_state import MAX_SLOTS, CouplingDefinition, DisturbanceRecord, InteractionDefinition
from .spatial_state import EmissionDefinition, SpatialCouplingDefinition, SpatialInteractionDefinition

SingleRule = EmissionDefinition | SpatialCouplingDefinition | SpatialInteractionDefinition
PairRule = CouplingDefinition | InteractionDefinition


def selected_types(rule: SingleRule) -> tuple[int, ...]:
    """Resolve a compiled property selection or a legacy exact layout selector."""
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
    rule: InteractionDefinition, records: tuple[DisturbanceRecord | None, ...]
) -> tuple[tuple[int, ...], ...]:
    """Greedily select disjoint groups in role order and then local slot order.

    A partial group ends selection. There is no combinatorial search or retry
    with a different assignment, and conditions do not alter this selection.
    """
    if not 2 <= len(rule.participants) <= MAX_SLOTS or len(records) > MAX_SLOTS:
        raise ValueError("indexed interactions require bounded participant and record counts")
    available = {slot for slot, record in enumerate(records) if record is not None}
    groups: list[tuple[int, ...]] = []
    for _ in range(len(records) // len(rule.participants)):
        group = []
        for kinds in rule.participants:
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
