"""THE WAIT (ALGEBRA.md 9.112 item 1): one interval, for every Port, always: a value sent at the start of t is combined in t.

One folder, one primitive (record 2221 (3)); the register finds it by this folder and reads
DECLARATION, the row of ALGEBRA.md 9.117 for this name (cut 2: bind gives the loop's method that
implements it today, resolved at each call; the next cut moves the body of code here).
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from event_universe.core.register import Declaration

DECLARATION = Declaration("the wait", "(i)", (), (), None, "9.112 item 1", word="the step")


def bind(loop: Any) -> Callable[..., object]:
    """The loop's method `_wait`, resolved at each call (cut 2)."""
    return loop._method("_wait")  # type: ignore[no-any-return]
