"""THE DEGREE (ALGEBRA.md #the-primitives, #the-interval): the representation as parts (1, 3 or 6 components), the same rule on each component. ALGEBRA.md #the-primitives: from the rule."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from event_universe.core.register import Declaration
from event_universe.core.schema import Integer, ListOf, ObjectOf, Schema

DECLARATION = Declaration(
    "the degree",
    "(i)",
    ("parts",),
    ("the components' axes",),
    None,
    "ALGEBRA.md #the-primitives, #the-interval",
    word="the step",
    schema=Schema({"a family's entry": ObjectOf({"parts": ListOf(Integer(least=1))})}),
)


def bind(loop: Any) -> Callable[..., object]:
    """The loop's method `_part_axes`, resolved at each call (cut 2)."""
    return loop._method("_part_axes")  # type: ignore[no-any-return]
