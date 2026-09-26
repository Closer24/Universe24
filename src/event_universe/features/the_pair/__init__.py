"""THE PAIR (ALGEBRA.md 9.57 (1); 9.111 item 7 row 1): the range and the rest rotation of the six-neighbour term: cos omega_0 = num / den at k = 0 and p = Gamma.

One folder, one primitive (record 2221 (3)); the register finds it by this folder and reads
DECLARATION; bind gives its function for the loop (cut 2: the loop's method that
implements it today; the next cut moves the body of code here).
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

DECLARATION = {
    "name": "the pair",
    "place": "(i)",
    "word": "the step",
    "reads": ("the family's pair", "a body's pair at its Nodes"),
    "writes": ("the rule's coefficients",),
    "section": "9.57 (1); 9.111 item 7 row 1",
}


def bind(loop: Any) -> Callable[..., object]:
    """The loop's method `pair_arrays`, resolved at each call (cut 2)."""
    return loop._method("pair_arrays")  # type: ignore[no-any-return]
