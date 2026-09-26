"""THE SELF-SOURCE (ALGEBRA.md 9.78 (3); 9.88 (2); 9.91 (5)): the six squared differences at the Node summed over the components div P_2, with the structure table the cubic term, a load into the step's sum. 9.113 item 2: beyond (L)."""

from typing import Any

from event_universe.core.register import Declaration, Key

UNIT = Key("unit", "int", low=(24, "amplitude_bound"), also=(0,))
SCHEMA = {"family": (Key("self_source", "object", keys=(UNIT,), section="9.78 (3); 9.91 (5)"),)}
DECLARATION = Declaration(
    "the self-source",
    "(i)",
    ("the family's own levels", "P_2", "the structure table"),
    ("a family's level at a Node",),
    None,
    section="9.78 (3); 9.88 (2); 9.91 (5)",
    word="the right side",
)


def bind(loop: Any) -> Any:
    """The loop's method `_self_source`, resolved at each call (cut 2)."""
    return loop._method("_self_source")
