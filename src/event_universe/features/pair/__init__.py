"""THE PAIR (ALGEBRA.md 9.57 (1); 9.111 item 7 row 1): the range and the rest rotation of the six-neighbour term: cos omega_0 = num / den at k = 0 and p = Gamma. 9.113 item 2: from the rule."""

from typing import Any

from event_universe.core.register import Declaration, Key

SCHEMA = {"family": (Key("pair", "pair", low=1, also=("body",), section="9.85 (3); 9.91 (7)"),)}
DECLARATION = Declaration(
    "the pair",
    "(i)",
    ("the family's pair", "a body's pair at its Nodes"),
    ("the rule's coefficients",),
    None,
    section="9.57 (1); 9.111 item 7 row 1",
    word="the step",
)


def bind(loop: Any) -> Any:
    """The loop's method `pair_arrays`, resolved at each call (cut 2)."""
    return loop._method("pair_arrays")
