"""THE PAIR (ALGEBRA.md 9.57 (1); 9.111 item 7 row 1): the range and the rest rotation of the six-neighbour term: cos omega_0 = num / den at k = 0 and p = Gamma. 9.113 item 2: from the rule.

One folder, one primitive (record 2221 (3)); the register finds it by this folder and reads
DECLARATION, the row of ALGEBRA.md 9.117 for this name (cut 2: bind gives the loop's method that
implements it today, resolved at each call; the next cut moves the body of code here).
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from event_universe.core.register import Declaration

DECLARATION = Declaration(
    "the pair",
    "(i)",
    ("the family's pair", "a body's pair at its Nodes"),
    ("the rule's coefficients",),
    None,
    "9.57 (1); 9.111 item 7 row 1",
    word="the step",
)


def bind(loop: Any) -> Callable[..., object]:
    """The loop's method `pair_arrays`, resolved at each call (cut 2)."""
    return loop._method("pair_arrays")  # type: ignore[no-any-return]
