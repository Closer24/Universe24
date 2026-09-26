"""THE HOP (ALGEBRA.md 9.96 (1); 9.89 (2)): the body's drive gains n against the wall W = 3 Q M, at most one Link per interval, the remainder kept; the body's Nodes translate.

One folder, one primitive (record 2221 (3)); the register finds it by this folder and reads
DECLARATION; bind gives its function for the loop (cut 2: the loop's method that
implements it today; the next cut moves the body of code here).
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

DECLARATION = {
    "name": "the hop",
    "place": "(v)",
    "word": "after the step",
    "reads": ("the body's momentum n", "the wall W", "the drive's remainder"),
    "writes": ("the body's Nodes", "the drive's remainder"),
    "section": "9.96 (1); 9.89 (2)",
}


def bind(loop: Any) -> Callable[..., object]:
    """The loop's method `_move_block`, resolved at each call (cut 2)."""
    return loop._method("_move_block")  # type: ignore[no-any-return]
