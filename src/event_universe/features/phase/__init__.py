"""THE PHASE (ALGEBRA.md 9.91 (2)): one level or the pair (now, before): the second-order line of the rule, a rotation. 9.113 item 2: from the rule."""

from typing import Any

from event_universe.core.register import Declaration, Key

SCHEMA = {"family": (Key("phase", "one", values=(1, 2), section="9.91 (1); 9.91 (2)"),)}
DECLARATION = Declaration(
    "the phase",
    "(i)",
    ("levels",),
    ("the second level",),
    None,
    section="9.91 (2)",
    word="the step",
)


def bind(loop: Any) -> Any:
    """The loop's method `_level_step`, resolved at each call (cut 2)."""
    return loop._method("_level_step")
