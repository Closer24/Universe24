"""The rounds: the engine's tick, passed in, run under the runner's masks, every due beat or some."""

from collections.abc import Callable
from typing import Any


def rounds(tick: Callable[..., Any], layout: Any, s: Any, masks: list[Any]) -> tuple[Any, list[Any]]:
    """Each mask one round of the tick where it allows; the outs kept in order for the rewind check."""
    outs = []
    for allowed in masks:
        s, out = tick(layout, s, allowed)
        outs.append(out)
    return s, outs
