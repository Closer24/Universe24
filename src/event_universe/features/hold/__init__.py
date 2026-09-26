"""THE HOLD (ALGEBRA.md 9.45 (2); 9.91 (3); 9.111 item 3; 9.117 item 3): s = SUM_k (M_k P_0) div P_k written whole into the held family's level at the body's Nodes, the vector and tensor parts over the wall, the dipole on the six neighbours; order 1 on the level at (iv), the source 2. 9.113 item 2: the read from the rule, the write beyond (H)."""

from typing import Any

from event_universe.core.register import Declaration, Key

HELD = (
    Key("count", "one", values=("content", "sign")),
    Key("factors", "list", items=Key("factor", "int", low=1), low=1, high=3),
    Key("dipole", "one", values=("spin", "moment")),
    Key("dipole_div", "int", low=1),
)
SCHEMA = {"family": (Key("held", "object", keys=HELD, role="a field family", section="9.91 (3)"),)}
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
    1,
    section="9.45 (2); 9.91 (3); 9.111 item 3; 9.117 item 3",
    word="the right side",
)


def bind(loop: Any) -> Any:
    """The loop's method `_hold`, resolved at each call (cut 2)."""
    return loop._method("_hold")
