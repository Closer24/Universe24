"""Bounded compatibility sets shared by scheduling, execution and carried state."""

from collections.abc import Iterable

from .disturbance_state import CouplingDefinition, InteractionDefinition
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


def selected_type_set(*groups: Iterable[SingleRule]) -> frozenset[int]:
    """Combine rule groups without introducing a second eligibility implementation."""
    return frozenset(kind for group in groups for rule in group for kind in selected_types(rule))
