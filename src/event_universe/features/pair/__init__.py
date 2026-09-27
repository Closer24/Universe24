"""THE PAIR (ALGEBRA.md 9.57 (1); 9.111 item 7 row 1): the range and the rest rotation of the six-neighbour term: cos omega_0 = num / den at k = 0 and p = Gamma. 9.113 item 2: from the rule."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np

from event_universe.core.register import Declaration
from event_universe.core.schema import Either, Integer, ListOf, ObjectOf, OneOf, Schema


def pair_arrays(
    shape: tuple[int, ...], pair: tuple[int, int], wells: Sequence[tuple[np.ndarray, tuple[int, int]]]
) -> tuple[np.ndarray, np.ndarray]:
    """THE PAIR ARRAYS (ALGEBRA.md 9.85 (3), 9.91 (7)): num and den over the GameBoard, the pair everywhere but at the bodies' Nodes, whose declared pairs (the wells) are written at their masks in order."""
    num = np.full(shape, pair[0], dtype=np.int64)
    den = np.full(shape, pair[1], dtype=np.int64)
    for mask, (well_num, well_den) in wells:
        num[mask] = well_num
        den[mask] = well_den
    return num, den


DECLARATION = Declaration(
    "the pair",
    "(i)",
    ("the family's pair", "a body's pair at its Nodes"),
    ("the rule's coefficients",),
    pair_arrays,
    "9.57 (1); 9.111 item 7 row 1",
    word="the step",
    schema=Schema(
        {
            "a family's entry": ObjectOf(
                {"pair": Either((ListOf(Integer(least=1), length=2), OneOf(("body",))))}
            )
        }
    ),
)
