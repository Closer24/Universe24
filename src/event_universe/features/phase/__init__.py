"""THE PHASE (ALGEBRA.md #the-interval): one level or the pair (now, before): the second-order line of the rule, a rotation. ALGEBRA.md #the-primitives: from the rule."""

from __future__ import annotations

import numpy as np

from event_universe.core.register import Declaration
from event_universe.core.rule3 import ISOTROPIC, coefficients, rule3
from event_universe.core.schema import ObjectOf, OneOf, Schema


def level_step(
    num: np.ndarray,
    den: np.ndarray,
    gamma: int,
    content: np.ndarray | int,
    axis_contents: tuple[np.ndarray, ...] | None,
    reads: list[np.ndarray],
    now: np.ndarray,
    other: np.ndarray,
    remainder: np.ndarray,
    weak_field: bool,
    direction: int = 1,
) -> tuple[np.ndarray, np.ndarray]:
    """One level's step by Rule3 in `direction` from its three per-axis arrival sums, `now` the level read and `other` the far level (ALGEBRA.md #the-interval, #the-direction)."""
    integers, self_coefficient, wall = coefficients(
        num, den, gamma, content, ISOTROPIC if axis_contents is None else axis_contents, weak_field
    )
    return rule3(
        integers,
        (reads[0], reads[1], reads[2]),
        self_coefficient,
        wall,
        now,
        other,
        remainder,
        direction,
    )


DECLARATION = Declaration(
    "the phase",
    "(i)",
    ("levels",),
    ("the second level",),
    level_step,
    "ALGEBRA.md #the-interval",
    word="the step",
    schema=Schema({"a family's entry": ObjectOf({"phase": OneOf((1, 2))})}),
)
