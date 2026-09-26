"""THE SIGNED READ (ALGEBRA.md 9.117 item 2, the first row; 9.78 (4); 9.108 items 8, 11, 12, 13; 9.116 items 4a and 4c): p_0 = Gamma - SUM over the reads of (weight x by x argument), the axes' paces with the tensor's parts; the guard 0 < p and p^2 (18 num + 6 den) <= Gamma^2 (18 den + 6 num). 9.113 item 2: from the rule."""

from typing import Any

from event_universe.core.register import Declaration, Key

READ = (
    Key("family", "name"),
    Key("weight", "int", low=1, named=True),
    Key("twist", "int", low=0, also=("own",)),
    Key("by", "one", values=(1, "q")),
)
SCHEMA = {"family": (Key("reads", "list", items=Key("read", "object", keys=READ), section="9.91 (7)"),)}
DECLARATION = Declaration(
    "the signed read",
    "(i)",
    (
        "the read families' arguments at the interval's start (a level, or D_i for a pair)",
        "the signed weights",
        "by (plain, or q)",
        "the axis contents with their remainders",
    ),
    ("the paces",),
    None,
    section="9.117 item 2, the first row; 9.78 (4); 9.108 items 8, 11, 12, 13; 9.116 items 4a and 4c",
    word="the right side",
)


def bind(loop: Any) -> Any:
    """The loop's method `_effective_content`, resolved at each call (cut 2)."""
    return loop._method("_effective_content")
