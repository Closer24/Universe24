"""The start (ALGEBRA.md #the-generator (g), the start): a held family's rest under its own line at the pace 1 with the sum's sources, 6 den a = num S_6(a) + 3 den sigma at a fine unit derived from the width, the division act iterated from nothing until the levels repeat (the map monotone from nothing, its first repeat its fixed point), the levels the nearest integers by the division act; the remainder at the half wall, the division's origin, and the hold's carry E_s div 2 at the sources' Nodes; on a chain and a box alike, in the engine and in the generator."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from event_universe.core.ports import Wrap, arrival
from event_universe.core.rule3 import NO_READ, rule3

Pair = tuple[int, int]


@dataclass(frozen=True)
class FieldAtRest:
    """The held field at rest: the levels (the nearest integers), the fine levels at the unit, the unit, the iterations to the repeat, the level's remainder at the half wall and the hold's carries E_s div 2 at the sources' Nodes."""

    levels: np.ndarray
    fine: np.ndarray
    unit: int
    iterations: int
    remainder: int
    carries: np.ndarray


def division(numerator: object, wall: object, value: object) -> np.ndarray:
    """Rule3's division act on a value: (numerator x value) div wall, the remainder not kept (ALGEBRA.md #the-four-acts)."""
    return np.asarray(rule3(NO_READ, NO_READ, numerator, wall, value, 0, 0)[0])


def arrivals(a: np.ndarray, wrap: Wrap) -> tuple[np.ndarray, ...]:
    """The six arrivals as Rule3 reads them, the two of each axis summed: the wrap on a periodic axis, 0 beyond a face, the Node itself on a folded axis (core/ports.py)."""
    return tuple(arrival(a, axis, 1, wrap[axis]) + arrival(a, axis, -1, wrap[axis]) for axis in range(3))


def unit_of(counts: np.ndarray, pair: Pair, divisor: int, width: int) -> int:
    """The fine unit, derived from the width and never written: the largest unit at which num S_6 of the rest stays inside the width, the rest's bound the larger of the counts and the tent of the whole source over the longest extent (half of 3 x the source total over the divisor times the extent)."""
    tent = int(division(3 * int(np.abs(counts).sum()) * (max(counts.shape) + 1), 2 * divisor, 1))
    largest = max(int(np.abs(counts).max()), tent + 1)
    return int(division(1, 2 * abs(pair[0]) * 6 * largest, width))


def rest(counts: np.ndarray, pair: Pair, wrap: Wrap, divisor: int, width: int) -> FieldAtRest:
    """The rest by the line itself: the fine levels b <- (num S_6(b) + 3 den x (count x unit div E_s)) div (6 den) by Rule3's division act from nothing, until the levels repeat; refused by name where the sources are not of one sign (the map is monotone only then), where a board periodic on its every axis at [1, 1] gives the sources no sink, and where the divisor is below 1."""
    num, den = pair
    if divisor < 1:
        raise ValueError(f"the start's divisor is from 1, got {divisor}")
    if bool((counts > 0).any()) and bool((counts < 0).any()):
        raise ValueError(
            "the start's sources are of one sign: the map from nothing is monotone only then"
        )
    long = [axis for axis in range(len(wrap)) if counts.shape[axis] > 1]
    if num == den and all(wrap[axis] for axis in long) and bool(counts.any()):
        raise ValueError(
            f"the sum's rest needs a sink: a board periodic on every axis at [1, 1] has no rest under the "
            f"source total {int(counts.sum())}"
        )
    unit = unit_of(counts, pair, divisor, width)
    source = division(3 * den * unit, divisor, counts)
    fine, iterations = np.zeros(counts.shape, dtype=np.int64), 0
    while True:
        iterations += 1
        after = np.asarray(rule3((num, num, num), arrivals(fine, wrap), 0, 6 * den, fine, 0, source)[0])
        if np.array_equal(after, fine):
            break
        fine = after
    half = int(division(1, 2, unit))
    levels = np.asarray(rule3(NO_READ, NO_READ, 1, unit, fine, 0, half)[0], dtype=np.int64)
    carries = np.where(counts != 0, division(1, 2, divisor), 0).astype(np.int64)
    return FieldAtRest(levels, fine, unit, iterations, int(division(1, 2, 3 * den - 1)), carries)
