"""THE DEGREE (ALGEBRA.md 9.86 (2); 9.91 (2)): the representation as parts (1, 3 or 6 components), the same rule on each component.

One folder, one primitive (record 2221 (3)); the register finds it by this folder and reads
DECLARATION; bind gives its function for the loop (cut 2: the loop's method that
implements it today; the next cut moves the body of code here).
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

DECLARATION = {
    "name": "the degree",
    "place": "(i)",
    "word": "the step",
    "reads": ("parts",),
    "writes": ("the components' axes",),
    "section": "9.86 (2); 9.91 (2)",
}


def bind(loop: Any) -> Callable[..., object]:
    """The loop's method `_part_axes`, resolved at each call (cut 2)."""
    return loop._method("_part_axes")  # type: ignore[no-any-return]
