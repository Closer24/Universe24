"""THE SEND (ALGEBRA.md 9.112 item 1): the Port puts on its Link weight x the component's level at the interval's start.

One folder, one primitive (record 2221 (3)); the register finds it by this folder and reads
DECLARATION, the row of ALGEBRA.md 9.117 for this name (cut 2: bind gives the loop's method that
implements it today, resolved at each call; the next cut moves the body of code here).
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from event_universe.core.register import Declaration

DECLARATION = Declaration(
    "the send",
    "(i)",
    ("the level now", "the weight"),
    ("the Link's value",),
    None,
    None,
    "9.112 item 1",
    word="the step",
)


def bind(loop: Any) -> Callable[..., object]:
    """The loop's method `_neighbours`, resolved at each call (cut 2)."""
    return loop._method("_neighbours")  # type: ignore[no-any-return]
