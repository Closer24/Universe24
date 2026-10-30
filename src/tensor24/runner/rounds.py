"""Clock: the rounds, counted from outside, since no Node-clock holds a count.
Algebra: the engine's act iterated.
Board: every Node-clock steps in every round, and each round's state is given in turn with its clicks.
Clicks: each round's clicks, the click teeth's quotients, are given beside its state for the record.
"""

from collections.abc import Callable, Iterator
from typing import Any


def rounds(act: Callable[..., Any], layout: Any, s: Any, n: int) -> Iterator[tuple[Any, Any]]:
    """The state after each of n rounds of the act with that round's clicks, in order."""
    for _ in range(n):
        s, clicks = act(layout, s)
        yield s, clicks
