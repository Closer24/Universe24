"""THE DEGREE (ALGEBRA.md 9.86 (2); 9.91 (2)): the representation as parts (1, 3 or 6 components), the same rule on each component. 9.113 item 2: from the rule."""

from __future__ import annotations

from collections.abc import Sequence

from event_universe.core.register import Declaration
from event_universe.core.schema import Integer, ListOf, ObjectOf, Schema

TENSOR_AXES = ((0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2))


def axes_of(parts: Sequence[int], part: int) -> tuple[int, tuple[int, ...]]:
    """A component's part group (0 the time part, 1 the vector, 2 the tensor) and the axes it multiplies (ALGEBRA.md 9.91 (1), (3): n_a for the vector, n_a n_b for the tensor), by the family's parts list; a part beyond the components is refused."""
    offset = 0
    for group, count in enumerate(parts):
        if part < offset + count:
            index = part - offset
            if group == 0:
                return 0, ()
            if group == 1:
                return 1, (index,)
            return 2, TENSOR_AXES[index]
        offset += count
    raise ValueError(f"the part {part} is beyond the family's components {list(parts)}")


DECLARATION = Declaration(
    "the degree",
    "(i)",
    ("parts",),
    ("the components' axes",),
    axes_of,
    "9.86 (2); 9.91 (2)",
    word="the step",
    schema=Schema({"a family's entry": ObjectOf({"parts": ListOf(Integer(least=1))})}),
)
