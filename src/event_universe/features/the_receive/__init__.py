"""THE RECEIVE (ALGEBRA.md 9.112 item 1; 9.96 (2) (e)): the Port takes the value the other end put on the Link at the same start, rotated by the Port's accumulator through the one table of triples.

One folder, one primitive (record 2221 (3)); the register finds it by this folder and reads
DECLARATION; bind gives its function for the loop (cut 2: the loop's method that
implements it today; the next cut moves the body of code here).
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

DECLARATION = {
    "name": "the receive",
    "place": "(i)",
    "word": "the step",
    "reads": ("the Link's value", "the Port's accumulator", "the twist table"),
    "writes": ("the arrivals",),
    "order": 1,
    "section": "9.112 item 1; 9.96 (2) (e)",
}


def bind(loop: Any) -> Callable[..., object]:
    """The loop's method `_arrivals`, resolved at each call (cut 2)."""
    return loop._method("_arrivals")  # type: ignore[no-any-return]
