"""THE CLICKS (ALGEBRA.md #the-ladder, #the-primitives): the ladder on the inward flux: the first k with 2 W (C + f_1 + ... + f_k) >= (2 u + 1) T; the deferred write a body's content M_k (+1 of the taken family) at t + 1; order 1 on the tally at (ii) and on M_k at (iv). ALGEBRA.md #the-primitives: the click; the booking from the rule."""

from __future__ import annotations

from collections.abc import Sequence

from event_universe.core.register import Declaration
from event_universe.core.schema import Flag, Integer, ObjectOf, Schema


def ladder_click(
    residue: int,
    norm: int,
    wheel: int,
    pace: int,
    total: int,
    ladder: Sequence[int],
    increments: Sequence[int],
) -> tuple[int | None, int]:
    """The increment ladder on one interval's bookings: the running total gains the one-way flux into the ladder's detectors in the declared order, and the click fires at the first detector at which 2 W pace (C + f_1 + ... + f_k) >= (2 u + 1) T, the threshold fixed at the giving (Born's rule its theorem); a record without its norm yet books and waits; the pair (the detector or None, the total after the bookings)."""
    if norm <= 0:
        return None, total + sum(increments)
    threshold = (2 * residue + 1) * norm
    running = 2 * wheel * pace * total
    for detector in ladder:
        running += 2 * wheel * pace * increments[detector]
        total += increments[detector]
        if running >= threshold:
            return detector, total
    return None, total


DECLARATION = Declaration(
    "the clicks",
    "(ii)",
    (
        "the inward flux at the detectors' Ports",
        "the record's residue u, wheel W and norm T",
        "the ladder",
    ),
    ("the record's tally", "a body's content M_k"),
    ladder_click,
    "ALGEBRA.md #the-ladder, #the-primitives",
    word="after the step",
    schema=Schema(
        {
            "a family's entry": ObjectOf(
                {"clicks": ObjectOf({"gives": Flag(), "takes": Flag(), "quantum": Integer(least=1)})},
                frozenset({"clicks"}),
            )
        }
    ),
)
