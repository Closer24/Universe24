"""THE SPIN'S STEP (ALGEBRA.md 9.78 (5); 9.91 (8) (v)): S_next = S_now + ((Omega x S_now) + mu x B_q) div (W Gamma), the remainder on the body's record.

One folder, one primitive (record 2221 (3)); the register finds it by this folder and reads
DECLARATION; bind gives its function for the loop (cut 2: the loop's method that
implements it today; the next cut moves the body of code here).
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

DECLARATION = {
    "name": "the spin's step",
    "place": "(v)",
    "word": "after the step",
    "reads": (
        "the fields' curl at the body's Node",
        "the spin S",
        "the body's momentum n",
        "the wall W",
    ),
    "writes": ("the body's spin S",),
    "section": "9.78 (5); 9.91 (8) (v)",
}


def bind(loop: Any) -> Callable[..., object]:
    """The loop's method `_body_step`, resolved at each call (cut 2)."""
    return loop._method("_body_step")  # type: ignore[no-any-return]
