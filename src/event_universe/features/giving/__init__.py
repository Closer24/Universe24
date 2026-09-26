"""THE GIVING (ALGEBRA.md 9.117 item 2; 9.107; 9.116 item 5): the window: a_given at the outer Ports += g x a_body each interval until the outward norm reaches T; at the close M_k -= 1 and the bulk share n_a -= n_a div M with the remainder on the record.

One folder, one primitive (record 2221 (3)); the register finds it by this folder and reads
DECLARATION, the row of ALGEBRA.md 9.117 for this name (cut 2: bind gives the loop's method that
implements it today, resolved at each call; the next cut moves the body of code here).
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from event_universe.core.register import Declaration

DECLARATION = Declaration(
    "the giving",
    "(ii)",
    (
        "the body's own levels (its rotation)",
        "the weight g",
        "the outward flux through the body's outer Ports over the window",
        "the quantum's norm T",
        "M",
        "n",
    ),
    ("a family's level at a Node", "a body's content M_k", "a body's momentum n"),
    {"a body's content M_k": 2, "a body's momentum n": 1},
    None,
    "9.117 item 2; 9.107; 9.116 item 5",
    word="after the step",
)


def bind(loop: Any) -> Callable[..., object]:
    """The loop's method `_emit`, resolved at each call (cut 2)."""
    return loop._method("_emit")  # type: ignore[no-any-return]
