"""The rewind check: the rounds run back by the engine's run back alone, with no log read."""

from collections.abc import Callable
from typing import Any


def rewind(untick: Callable[..., Any], layout: Any, s: Any, n: int) -> Any:
    """The last n rounds run back from the state they reached."""
    for _ in range(n):
        s = untick(layout, s)
    return s
