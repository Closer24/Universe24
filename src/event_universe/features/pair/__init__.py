"""THE PAIR (ALGEBRA.md 9.57 (1); 9.111 item 7 row 1): the range and the rest rotation of the six-neighbour term: cos omega_0 = num / den at k = 0 and p = Gamma. 9.113 item 2: from the rule."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from event_universe.core.register import Declaration
from event_universe.core.schema import Either, Integer, ListOf, ObjectOf, OneOf, Schema

DECLARATION = Declaration(
    "the pair",
    "(i)",
    ("the family's pair", "a body's pair at its Nodes"),
    ("the rule's coefficients",),
    None,
    "9.57 (1); 9.111 item 7 row 1",
    word="the step",
    schema=Schema(
        {
            "a family's entry": ObjectOf(
                {"pair": Either((ListOf(Integer(least=1), length=2), OneOf(("body",))))}
            )
        }
    ),
)


def bind(loop: Any) -> Callable[..., object]:
    """The loop's method `pair_arrays`, resolved at each call (cut 2)."""
    return loop._method("pair_arrays")  # type: ignore[no-any-return]
