"""THE PHASE (ALGEBRA.md 9.91 (2)): one level or the pair (now, before): the second-order line of the rule, a rotation.

One folder, one primitive (record 2221 (3)); the register finds it by this folder and reads
DECLARATION; bind gives its function for the loop (cut 2: the loop's method that
implements it today; the next cut moves the body of code here).
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

DECLARATION = {
    "name": "the phase",
    "place": "(i)",
    "word": "the step",
    "reads": ("levels",),
    "writes": ("the second level",),
    "section": "9.91 (2)",
}


def bind(loop: Any) -> Callable[..., object]:
    """The loop's method `_level_step`, resolved at each call (cut 2)."""
    return loop._method("_level_step")  # type: ignore[no-any-return]
