"""THE SEND (ALGEBRA.md 9.112 item 1): the Port puts on its Link weight x the component's level at the interval's start.

One folder, one primitive (record 2221 (3)); the register finds it by this folder and reads
DECLARATION; bind gives its function for the loop (cut 2: the loop's method that
implements it today; the next cut moves the body of code here).
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

DECLARATION = {
    "name": "the send",
    "place": "(i)",
    "word": "the step",
    "reads": ("the level now", "the weight"),
    "writes": ("the Link's value",),
    "section": "9.112 item 1",
}


def bind(loop: Any) -> Callable[..., object]:
    """The loop's method `_neighbours`, resolved at each call (cut 2)."""
    return loop._method("_neighbours")  # type: ignore[no-any-return]
