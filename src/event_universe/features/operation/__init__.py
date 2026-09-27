"""THE OPERATION (ALGEBRA.md #the-line, #the-interval): a_next = (SUM of the six received x w + B now - W before + the loads + r) div W with the remainder kept at the Node.

One folder, one primitive; the register finds it by this folder and reads
DECLARATION, the row of ALGEBRA.md #the-primitives for this name (the operation's cut: bind gives rule3 of
core/rule3.py itself, one function for every record at every Node).
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from event_universe.core.register import Declaration
from event_universe.core.rule3 import rule3

DECLARATION = Declaration(
    "the operation",
    "(i)",
    ("the six arrivals", "now", "before", "the remainder", "the family's integers w, B, W", "the loads"),
    ("the level next, the remainder",),
    None,
    "ALGEBRA.md #the-line, #the-interval",
    word="the step",
)


def bind(loop: Any) -> Callable[..., object]:
    """Rule3 itself, core/rule3.py: the one function every record steps by, in either direction (ALGEBRA.md #the-line)."""
    return rule3
