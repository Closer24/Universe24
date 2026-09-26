"""THE CLICKS (ALGEBRA.md 9.25 (2), (3); 9.111 items 1, 2 and 6; 9.117 items 2 and 3): the ladder on the inward flux: the first k with 2 W (C + f_1 + ... + f_k) >= (2 u + 1) T; the deferred write a body's content M_k (+1 of the taken family) at t + 1; order 1 on the tally at (ii) and on M_k at (iv). 9.113 item 2: the click; the booking from the rule."""

from typing import Any

from event_universe.core.register import Declaration, Key

CLICKS = (Key("gives", "bool"), Key("takes", "bool"), Key("quantum", "int", low=1))
TERM = Key("clicks", "object", keys=CLICKS, role="a family of records", section="9.79 (1)")
SCHEMA = {"family": (TERM,)}
DECLARATION = Declaration(
    "the clicks",
    "(ii)",
    (
        "the inward flux at the detectors' Ports",
        "the record's residue u, wheel W and norm T",
        "the ladder",
    ),
    ("the record's tally", "a body's content M_k"),
    1,
    section="9.25 (2), (3); 9.111 items 1, 2 and 6; 9.117 items 2 and 3",
    word="after the step",
)


def bind(loop: Any) -> Any:
    """The loop's method `_ladder_click`, resolved at each call (cut 2)."""
    return loop._method("_ladder_click")
