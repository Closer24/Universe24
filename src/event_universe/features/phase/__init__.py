"""THE PHASE (ALGEBRA.md #the-interval): one level or the pair (now, before): the second-order line of the rule, a rotation. ALGEBRA.md #the-primitives: from the rule."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from event_universe.core.register import Declaration
from event_universe.core.schema import ObjectOf, OneOf, Schema

DECLARATION = Declaration(
    "the phase",
    "(i)",
    ("levels",),
    ("the second level",),
    None,
    "ALGEBRA.md #the-interval",
    word="the step",
    schema=Schema({"a family's entry": ObjectOf({"phase": OneOf((1, 2))})}),
)


def bind(loop: Any) -> Callable[..., object]:
    """The loop's method `_level_step`, resolved at each call (cut 2)."""
    return loop._method("_level_step")  # type: ignore[no-any-return]
