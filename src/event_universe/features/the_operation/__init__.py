"""THE OPERATION (ALGEBRA.md 9.57 (1); 9.112 items 1 and 2): a_next = (SUM of the six received x w + B now - W before + the loads + r) div W with the remainder kept at the Node.

One folder, one primitive (record 2221 (3)); the register finds it by this folder and reads
DECLARATION; bind gives its function for the loop (cut 2: the loop's method that
implements it today; the next cut moves the body of code here).
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

DECLARATION = {
    "name": "the operation",
    "place": "(i)",
    "word": "the step",
    "reads": (
        "the six arrivals",
        "now",
        "before",
        "the remainder",
        "the family's integers w, B, W",
        "the loads",
    ),
    "writes": ("the level next", "the remainder"),
    "section": "9.57 (1); 9.112 items 1 and 2",
}


def bind(loop: Any) -> Callable[..., object]:
    """The loop's method `one_rule`, resolved at each call (cut 2)."""
    return loop._method("one_rule")  # type: ignore[no-any-return]
