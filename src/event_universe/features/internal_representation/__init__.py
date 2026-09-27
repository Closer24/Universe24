"""THE INTERNAL REPRESENTATION (ALGEBRA.md #the-primitives item 3, #the-line): n pairs at a Node, the generators exact triples, the transport across a Link the product of the Port's rotation with the generator's table (the receive's twist reads); order 2 on the arrivals, the receive 1; today the record's one pair, its second level stepped by the phase's function on its own arrivals."""

from __future__ import annotations

from collections.abc import Callable

import numpy as np

from event_universe.core.register import Declaration

Rule = tuple[np.ndarray, np.ndarray, int, np.ndarray | int, tuple[np.ndarray, ...] | None]
Stepped = tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]


def second_level(
    step: Callable[..., tuple[np.ndarray, np.ndarray]],
    rule: Rule,
    reads: list[np.ndarray] | None,
    now: np.ndarray | None,
    other: np.ndarray | None,
    remainder: np.ndarray | None,
    weak_field: bool,
    direction: int = 1,
    like: np.ndarray | None = None,
) -> Stepped:
    """The pair's second level stepped by the phase's function `step` in `direction` under the rule's five (the pair's two arrays, the Node clock, the content, the axis contents) on its own three arrival sums (`reads`, zeros where the transport brought none), `now` the level read, `other` the far level and `remainder` its remainder, allocated at zero like the first level's array `like` where the pair had one member; returns the stepped level, its remainder, the level read and the far level."""
    if now is None or other is None or remainder is None:
        now, other, remainder = np.zeros_like(like), np.zeros_like(like), np.zeros_like(like)
    arrivals = [np.zeros_like(now) for _ in range(3)] if reads is None else reads
    nxt, remainder = step(*rule, arrivals, now, other, remainder, weak_field, direction)
    return nxt, remainder, now, other


DECLARATION = Declaration(
    "the internal representation",
    "(i)",
    ("n pairs", "the generators' tables", "the Ports' accumulators"),
    ("the arrivals",),
    second_level,
    "ALGEBRA.md #the-primitives item 3, #the-line",
    word="the right side",
)
