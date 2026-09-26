"""THE SPIN'S STEP (ALGEBRA.md 9.117 item 2; 9.78 (5); 9.104): S_next = S_now + [(Omega x S_now) + mu x B_q] div (W Gamma), the remainder on the record.

One folder, one primitive (record 2221 (3)); the register finds it by this folder and reads
DECLARATION, the row of ALGEBRA.md 9.117 for this name (cut 2: bind gives the loop's method that
implements it today, resolved at each call; the next cut moves the body of code here).
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from event_universe.core.register import Declaration

DECLARATION = Declaration(
    "the spin's step",
    "(v)",
    (
        "S_now",
        "the curls at the body's Node (V gravity's vector part, c its t part, B_q the charge's curl)",
        "mu",
        "n",
        "W",
        "Gamma",
    ),
    ("a body's spin S", "a body's remainders"),
    None,
    None,
    "9.117 item 2; 9.78 (5); 9.104",
    word="after the step",
)


def bind(loop: Any) -> Callable[..., object]:
    """The loop's method `_body_step`, resolved at each call (cut 2)."""
    return loop._method("_body_step")  # type: ignore[no-any-return]
