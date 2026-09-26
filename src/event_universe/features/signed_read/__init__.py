"""THE SIGNED READ (ALGEBRA.md 9.117 item 2, the first row; 9.78 (4); 9.108 items 8, 11, 12, 13; 9.116 items 4a and 4c): p_0 = Gamma - SUM over the reads of (weight x by x argument), the axes' paces with the tensor's parts; the guard 0 < p and p^2 (18 num + 6 den) <= Gamma^2 (18 den + 6 num). 9.113 item 2: from the rule.

One folder, one primitive (record 2221 (3)); the register finds it by this folder and reads
DECLARATION, the row of ALGEBRA.md 9.117 for this name (cut 2: bind gives the loop's method that
implements it today, resolved at each call; the next cut moves the body of code here).
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from event_universe.core.register import Declaration

DECLARATION = Declaration(
    "the signed read",
    "(i)",
    (
        "the read families' arguments at the interval's start (a level, or D_i for a pair)",
        "the signed weights",
        "by (plain, or q)",
        "the axis contents with their remainders",
    ),
    ("the paces",),
    None,
    None,
    "9.117 item 2, the first row; 9.78 (4); 9.108 items 8, 11, 12, 13; 9.116 items 4a and 4c",
    word="the right side",
)


def bind(loop: Any) -> Callable[..., object]:
    """The loop's method `_effective_content`, resolved at each call (cut 2)."""
    return loop._method("_effective_content")  # type: ignore[no-any-return]
