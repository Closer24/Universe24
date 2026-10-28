"""The rewind check: the undo log read back, the one place a log is read."""

from collections.abc import Callable
from typing import Any


def rewind(untick: Callable[..., Any], layout: Any, s: Any, outs: list[Any]) -> Any:
    """The rounds run back from their outs, the last first."""
    for out in reversed(outs):
        s = untick(layout, s, out)
    return s
