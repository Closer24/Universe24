"""THE CLICKS (ALGEBRA.md 9.25 (2), (3); 9.111 items 1, 2 and 6): the ladder on the inward flux: the first k with 2 W (C + f_1 + ... + f_k) >= (2 u + 1) T; the taking's writes (M_k, Q, n, the stock) enter at t + 1.

One folder, one primitive (record 2221 (3)); the register finds it by this folder and reads
DECLARATION; bind gives its function for the loop (cut 2: the loop's method that
implements it today; the next cut moves the body of code here).
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

DECLARATION = {
    "name": "the clicks",
    "place": "(ii)",
    "word": "after the step",
    "reads": (
        "the inward flux at the detectors' Ports",
        "the record's residue u, wheel W and norm T",
        "the ladder",
    ),
    "writes": (
        "the record's tally",
        "the body's count M_k",
        "the body's charge Q",
        "the body's momentum n",
        "the stock",
    ),
    "order": 1,
    "section": "9.25 (2), (3); 9.111 items 1, 2 and 6",
}


def bind(loop: Any) -> Callable[..., object]:
    """The loop's method `_ladder_click`, resolved at each call (cut 2)."""
    return loop._method("_ladder_click")  # type: ignore[no-any-return]
