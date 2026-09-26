"""THE PHASE (ALGEBRA.md 9.91 (2)): one level or the pair (now, before): the second-order line of the rule, a rotation. 9.113 item 2: from the rule.

One folder, one primitive (record 2221 (3)); the register finds it by this folder and reads
DECLARATION, the row of ALGEBRA.md 9.117 for this name (cut 2: bind gives the loop's method that
implements it today, resolved at each call; the next cut moves the body of code here).
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from event_universe.core.register import Declaration

DECLARATION = Declaration(
    "the phase", "(i)", ("levels",), ("the second level",), None, "9.91 (2)", word="the step"
)


def bind(loop: Any) -> Callable[..., object]:
    """The loop's method `_level_step`, resolved at each call (cut 2)."""
    return loop._method("_level_step")  # type: ignore[no-any-return]
