"""THE SEND (ALGEBRA.md 9.112 item 1): the Port puts on its Link weight x the component's level at the interval's start; one folder, one primitive, the register reads DECLARATION and its function `send`."""

from __future__ import annotations

from typing import Any

import numpy as np

from event_universe.core.register import Declaration


def send(ports: Any, a: np.ndarray, wrap: tuple[bool, bool, bool] | None = None) -> np.ndarray:
    """The sum of the six arrivals at every Node through the GameBoard's Ports (a folded axis gives the Node itself twice), on the world's faces or the family's (`wrap`)."""
    total = np.zeros_like(a)
    for port in ports.arrivals(a, wrap):
        total += port
    return total


DECLARATION = Declaration(
    "the send",
    "(i)",
    ("the level now", "the weight"),
    ("the Link's value",),
    send,
    "9.112 item 1",
    word="the step",
)
