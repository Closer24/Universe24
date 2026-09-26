"""THE HOLD (ALGEBRA.md 9.45 (2); 9.91 (3); 9.111 item 3): s = SUM_k (M_k P_0) div P_k written whole into the held family's level at the body's Nodes, the vector and tensor parts over the wall, the dipole on the six neighbours.

One folder, one primitive (record 2221 (3)); the register finds it by this folder and reads
DECLARATION; bind gives its function for the loop (cut 2: the loop's method that
implements it today; the next cut moves the body of code here).
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

DECLARATION = {
    "name": "the hold",
    "place": "(iv)",
    "word": "the right side",
    "reads": (
        "the body's count M_k",
        "the wall W",
        "the body's momentum n",
        "the held factors",
        "the dipole",
    ),
    "writes": ("the held level",),
    "section": "9.45 (2); 9.91 (3); 9.111 item 3",
}


def bind(loop: Any) -> Callable[..., object]:
    """The loop's method `_hold`, resolved at each call (cut 2)."""
    return loop._method("_hold")  # type: ignore[no-any-return]
