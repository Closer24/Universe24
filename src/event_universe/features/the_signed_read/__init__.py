"""THE SIGNED READ (ALGEBRA.md 9.78 (4); 9.108 items 11 and 12; 9.116 item 4a): p_0 = Gamma - SUM of signed weight x argument at every Node and axis; a hollow positive, a hill negative; the guard 0 < p <= Gamma.

One folder, one primitive (record 2221 (3)); the register finds it by this folder and reads
DECLARATION; bind gives its function for the loop (cut 2: the loop's method that
implements it today; the next cut moves the body of code here).
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

DECLARATION = {
    "name": "the signed read",
    "place": "(i)",
    "word": "the right side",
    "reads": ("the read families' levels", "the signed weights", "q", "the Port angles"),
    "writes": ("the paces",),
    "section": "9.78 (4); 9.108 items 11 and 12; 9.116 item 4a",
}


def bind(loop: Any) -> Callable[..., object]:
    """The loop's method `_effective_content`, resolved at each call (cut 2)."""
    return loop._method("_effective_content")  # type: ignore[no-any-return]
