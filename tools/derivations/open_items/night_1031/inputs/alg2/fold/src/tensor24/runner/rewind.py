"""Clock: all the rounds run back, to see the start return.
Algebra: the engine's untick iterated, with no log read.
Board: the state after the rounds, rewound round by round by the act's run back alone.
Clicks: n/a.
"""

from collections.abc import Callable
from typing import Any


def rewind(untick: Callable[..., Any], layout: Any, s: Any, n: int) -> Any:
    """The last n rounds run back from the state they reached."""
    for _ in range(n):
        s = untick(layout, s)
    return s
