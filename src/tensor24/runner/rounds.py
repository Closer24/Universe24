"""The rounds: the engine's tick, passed in, run round by round, every Node-clock stepping in every round."""

from collections.abc import Callable, Iterator
from typing import Any


def rounds(tick: Callable[..., Any], layout: Any, s: Any, n: int) -> Iterator[Any]:
    """The state after each of n rounds of the tick, in order."""
    for _ in range(n):
        s = tick(layout, s)
        yield s
