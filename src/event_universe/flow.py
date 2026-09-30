"""The flows into a held row's vector and tensor parts (ALGEBRA.md #the-primitives, the row "the hold"): a family of quanta's current as it sources a held row this interval, the carries of its writes at their origin, and the carried divisions that add its current to the vector parts and the current's square over its count to the tensor parts, forward and back."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from event_universe.core.rule3 import NO_READ, rule3
from event_universe.features.hold import TENSOR_AXES, hold
from event_universe.loader.derived import FamilyRule


@dataclass(frozen=True)
class Flow:
    """A family of quanta's current as it sources a held family's vector and tensor parts this interval: the weight it sources with, its line's travel per axis, its count at every Node after the line and its count's wall W_c."""

    weight: int
    travel: tuple[np.ndarray, np.ndarray, np.ndarray]
    count: np.ndarray
    wall: int


def flow_origins(family: FamilyRule, wall: int, count: np.ndarray) -> list[np.ndarray]:
    """The carries of a sourcing family's vector and tensor writes into a held family at the first act, each at half its divisor, the division's origin: (E_s W_c) div 2 for the vector's three, (E_s W_c^2) div 2 for the tensor's six."""
    assert family.divisor is not None
    vector = family.divisor * wall
    carries = [
        np.full(count.shape, rule3(NO_READ, NO_READ, 1, 2, vector, 0, 0)[0], dtype=np.int64)
        for _ in range(3)
    ]
    if len(family.parts) > 2:
        half = rule3(NO_READ, NO_READ, 1, 2, vector * wall, 0, 0)[0]
        carries += [np.full(count.shape, half, dtype=object) for _ in TENSOR_AXES]
    return carries


def flow_hold(
    family: FamilyRule, levels: list[np.ndarray], flow: Flow, carries: list[np.ndarray], direction: int
) -> tuple[list[np.ndarray], list[np.ndarray]]:
    """The hold's vector and tensor parts from one sourcing family (ALGEBRA.md #the-primitives, the row "the hold"): given the parts' levels now (the time part first), the vector part a gains (w x j_a + r_a) div (E_s W_c), the tensor part ab gains ((w x j_a j_b) div c_i + r_ab) div (E_s W_c^2) where c_i is above 0 (the current's square over the count, in the count's units), each by the carried division with its carry at the Node, back the same increments taken off; returns the levels and the carries after."""
    assert family.divisor is not None
    vector = family.divisor * flow.wall
    found, written = list(carries), list(levels)
    for a in range(3):
        level, found[a] = hold(written[1 + a], flow.weight * flow.travel[a], vector, found[a], direction)
        written[1 + a] = np.asarray(level)
    if len(family.parts) > 2:
        standing = flow.count > 0
        count = np.where(standing, flow.count, 1).astype(object)
        travel = [value.astype(object) for value in flow.travel]
        for pair, (a, b) in enumerate(TENSOR_AXES):
            square = rule3(NO_READ, NO_READ, flow.weight, count, travel[a] * travel[b], 0, 0)[0]
            at = 1 + 3 + pair
            level, found[3 + pair] = hold(
                written[at],
                np.where(standing, square, 0),
                vector * flow.wall,
                found[3 + pair],
                direction,
            )
            written[at] = np.asarray(level, dtype=np.int64)
    return written, found
