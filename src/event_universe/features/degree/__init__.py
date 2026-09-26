"""THE DEGREE (ALGEBRA.md 9.86 (2); 9.91 (2)): the representation as parts (1, 3 or 6 components), the same rule on each component. 9.113 item 2: from the rule."""

from typing import Any

from event_universe.core.register import Declaration, Key

PARTS = ([1], [1, 3], [1, 3, 6])
SCHEMA = {"family": (Key("parts", "one", values=PARTS, section="9.86 (2); 9.91 (1)"),)}
DECLARATION = Declaration(
    "the degree",
    "(i)",
    ("parts",),
    ("the components' axes",),
    None,
    section="9.86 (2); 9.91 (2)",
    word="the step",
)


def bind(loop: Any) -> Any:
    """The loop's method `_part_axes`, resolved at each call (cut 2)."""
    return loop._method("_part_axes")
