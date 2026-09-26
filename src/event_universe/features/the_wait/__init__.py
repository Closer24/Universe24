"""THE WAIT (ALGEBRA.md 9.112 item 1): one interval, for every Port, always: a value sent at the start of t is combined in t.

One folder, one primitive (record 2221 (3)); the register finds it by this folder and reads
DECLARATION; bind gives its function for the loop (cut 2: the loop's method that
implements it today; the next cut moves the body of code here).
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

DECLARATION = {
    "name": "the wait",
    "place": "(i)",
    "word": "the step",
    "reads": (),
    "writes": (),
    "section": "9.112 item 1",
}


def bind(loop: Any) -> Callable[..., object]:
    """The loop's method `_wait`, resolved at each call (cut 2)."""
    return loop._method("_wait")  # type: ignore[no-any-return]
