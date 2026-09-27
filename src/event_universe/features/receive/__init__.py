"""THE RECEIVE (ALGEBRA.md 9.112 item 1; 9.96 (2) (e); 9.117 item 3): the Port takes the value the other end put on the Link at the same start, rotated by the Port's accumulator through the one table of triples.

One folder, one primitive (record 2221 (3)); the register finds it by this folder and reads
DECLARATION, the row of ALGEBRA.md 9.117 for this name (cut 2: bind gives the loop's method that
implements it today, resolved at each call; the next cut moves the body of code here).
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from event_universe.core.register import Declaration

DECLARATION = Declaration(
    "the receive",
    "(i)",
    ("the Link's value", "a Port's accumulator", "the twist table"),
    ("the arrivals",),
    None,
    "9.112 item 1; 9.96 (2) (e); 9.117 item 3",
    word="the step",
)


def bind(loop: Any) -> Callable[..., object]:
    """The loop's method `_arrivals`, resolved at each call (cut 2)."""
    return loop._method("_arrivals")  # type: ignore[no-any-return]
