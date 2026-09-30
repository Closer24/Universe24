"""The flows into a held row's tensions (ALGEBRA.md #the-primitives, the row "the hold"): a family of quanta's stress on each axis as it sources a held row this interval, the carries of its writes at their origin, and the carried divisions, one act per axis at the one wall E_s W_c, that add its stress to the row's tensions, forward and back, exact."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from event_universe.core.rule3 import NO_READ, rule3
from event_universe.features.hold import diagonal, hold
from event_universe.loader.derived import FamilyRule

Vector = tuple[np.ndarray, np.ndarray, np.ndarray]


@dataclass(frozen=True)
class Flow:
    """A family of quanta's booking as it sources a held family's tensions this interval: the weight it sources with, its stress per axis (T_xx, T_yy, T_zz) and its count's wall W_c."""

    weight: int
    stress: Vector
    wall: int


def flow_origins(family: FamilyRule, wall: int, shape: tuple[int, int, int]) -> list[np.ndarray]:
    """The carries of a sourcing family's writes into a held family's tensions at the first act, one per axis, each at half its divisor (E_s W_c) div 2, the division's origin."""
    assert family.divisor is not None
    origin = rule3(NO_READ, NO_READ, 1, 2, family.divisor * wall, 0, 0)[0]
    return [np.full(shape, origin, dtype=np.int64) for _ in range(3)]


def flow_hold(
    family: FamilyRule, levels: list[np.ndarray], flow: Flow, carries: list[np.ndarray], direction: int
) -> tuple[list[np.ndarray], list[np.ndarray]]:
    """The hold's tensions from one sourcing family (ALGEBRA.md #the-primitives, the row "the hold"): given the parts' levels now (the time part first), the tension on the axis a gains (w x T_aa + r_aa) div (E_s W_c), T_aa the wave's own stress along the axis, by the carried division with its carry at the Node, no count in the divisor and no branch; back the same increments taken off; returns the levels and the carries after."""
    assert family.divisor is not None
    first = diagonal(family.parts)
    assert first is not None
    divisor = family.divisor * flow.wall
    found, written = list(carries), list(levels)
    for axis, part in enumerate(first):
        level, found[axis] = hold(
            written[part], flow.weight * flow.stress[axis], divisor, found[axis], direction
        )
        written[part] = np.asarray(level, dtype=np.int64)
    return written, found
