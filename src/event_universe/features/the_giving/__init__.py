"""THE GIVING (ALGEBRA.md 9.107; 9.71 (1); 9.116 item 5): the window: the body's rotation written into the given row at its shell until the outward norm reaches the quantum; the giving's writes (M_k, the stock, the bulk share of n) enter at t + 1.

One folder, one primitive (record 2221 (3)); the register finds it by this folder and reads
DECLARATION; bind gives its function for the loop (cut 2: the loop's method that
implements it today; the next cut moves the body of code here).
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

DECLARATION = {
    "name": "the giving",
    "place": "(ii)",
    "word": "after the step",
    "reads": (
        "the body's rotation at its shell",
        "the emitter's weight",
        "the outward flux through the body's Ports",
        "the excitation's norm",
    ),
    "writes": (
        "the given record's level",
        "the record's tally",
        "the body's count M_k",
        "the body's momentum n",
        "the stock",
    ),
    "order": 2,
    "section": "9.107; 9.71 (1); 9.116 item 5",
}


def bind(loop: Any) -> Callable[..., object]:
    """The loop's method `_emit`, resolved at each call (cut 2)."""
    return loop._method("_emit")  # type: ignore[no-any-return]
