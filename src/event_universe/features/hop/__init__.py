"""THE HOP (ALGEBRA.md #the-primitives): the position's accumulator += n each interval; at W the body's Nodes move one Link along the axis and the accumulator keeps the rest; a body with fixed does not hop.

One folder, one primitive (record 2221 (3)); the register finds it by this folder and reads
DECLARATION, the row of ALGEBRA.md #the-primitives for this name (cut 2: bind gives the loop's method that
implements it today, resolved at each call; the next cut moves the body of code here).
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from event_universe.core.register import Declaration

DECLARATION = Declaration(
    "the hop",
    "(v)",
    ("n", "W", "the hop's remainder", "fixed"),
    ("a body's position", "a body's remainders"),
    None,
    "ALGEBRA.md #the-primitives",
    word="after the step",
)


def bind(loop: Any) -> Callable[..., object]:
    """The loop's method `_move_block`, resolved at each call (cut 2)."""
    return loop._method("_move_block")  # type: ignore[no-any-return]
