"""THE SELF-SOURCE (ALGEBRA.md 9.78 (3); 9.88 (2); 9.91 (5)): the six squared differences at the Node summed over the components div P_2, with the structure table the cubic term.

One folder, one primitive (record 2221 (3)); the register finds it by this folder and reads
DECLARATION; bind gives its function for the loop (cut 2: the loop's method that
implements it today; the next cut moves the body of code here).
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

DECLARATION = {
    "name": "the self-source",
    "place": "(i)",
    "word": "the right side",
    "reads": ("the family's own levels", "P_2", "the structure table"),
    "writes": ("the step's load",),
    "section": "9.78 (3); 9.88 (2); 9.91 (5)",
}


def bind(loop: Any) -> Callable[..., object]:
    """The loop's method `_self_source`, resolved at each call (cut 2)."""
    return loop._method("_self_source")  # type: ignore[no-any-return]
