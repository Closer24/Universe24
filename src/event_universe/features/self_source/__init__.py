"""THE SELF-SOURCE (ALGEBRA.md 9.78 (3); 9.88 (2); 9.91 (5)): the six squared differences at the Node summed over the components div P_2, with the structure table the cubic term, a load into the step's sum. 9.113 item 2: beyond (L)."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from event_universe.core.register import Declaration
from event_universe.core.schema import Integer, ObjectOf, Schema

DECLARATION = Declaration(
    "the self-source",
    "(i)",
    ("the family's own levels", "P_2", "the structure table"),
    ("a family's level at a Node",),
    None,
    None,
    "9.78 (3); 9.88 (2); 9.91 (5)",
    word="the right side",
    schema=Schema({"a family's entry": ObjectOf({"self_source": ObjectOf({"unit": Integer(least=0)})})}),
)


def bind(loop: Any) -> Callable[..., object]:
    """The loop's method `_self_source`, resolved at each call (cut 2)."""
    return loop._method("_self_source")  # type: ignore[no-any-return]
