"""THE HOLD (ALGEBRA.md 9.45 (2); 9.91 (3); 9.111 item 3; 9.117 item 3): s = SUM_k (M_k P_0) div P_k written whole into the held family's level at the body's Nodes, the vector and tensor parts over the wall, the dipole on the six neighbours; order 1 on the level at (iv), the source 2. 9.113 item 2: the read from the rule, the write beyond (H)."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from event_universe.core.register import Declaration
from event_universe.core.schema import Integer, ListOf, ObjectOf, OneOf, Schema

DECLARATION = Declaration(
    "the hold",
    "(iv)",
    (
        "a body's content M_k",
        "P_0 and P_k",
        "the wall W",
        "a body's momentum n",
        "the held factors",
        "the dipole",
    ),
    ("a family's level at a Node", "a body's remainders"),
    None,
    "9.45 (2); 9.91 (3); 9.111 item 3; 9.117 item 3",
    word="the right side",
    schema=Schema(
        {
            "a family's entry": ObjectOf(
                {
                    "held": ObjectOf(
                        {
                            "count": OneOf(("content", "sign")),
                            "factors": ListOf(Integer(least=1)),
                            "dipole": OneOf(("spin", "moment")),
                            "dipole_div": Integer(least=1),
                        },
                        frozenset({"dipole_div"}),
                    )
                },
                frozenset({"held"}),
            )
        }
    ),
)


def bind(loop: Any) -> Callable[..., object]:
    """The loop's method `_hold`, resolved at each call (cut 2)."""
    return loop._method("_hold")  # type: ignore[no-any-return]
