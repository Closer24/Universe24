"""Clock: the rounds, counted from outside, since no Node-clock holds a count.
Algebra: the engine's tick iterated.
Board: every Node-clock steps in every round, and each round's state is given in turn.
Clicks: n/a.
"""

from collections.abc import Callable, Iterator
from typing import Any


def rounds(tick: Callable[..., Any], layout: Any, s: Any, n: int) -> Iterator[Any]:
    """The state after each of n rounds of the tick, in order."""
    for _ in range(n):
        s = tick(layout, s)
        yield s
