"""The start (ALGEBRA.md #the-generator, the (g) row, THE START; #the-stable-body): a held family's levels around the bodies under its own line at the pace 1, the clamp iterated by Rule3's division act with the counts rewritten at the bodies' Nodes each time, monotone from nothing to its fixed point, the stop its first repeat; the levels the nearest integers by the division act; the loop starts every held family from it, never from zeros (the transient rings); the generator reads it from here."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Any

import numpy as np

from event_universe.core.integer import MAX_WORK_INT
from event_universe.core.ports import arrival
from event_universe.core.register import Declaration
from event_universe.core.rule3 import rule3

NO_READ = (0, 0, 0)  # the line with no read
Wrap = tuple[bool, bool, bool]
Pair = tuple[int, int]
PERIODIC: Wrap = (True, True, True)


@dataclass(frozen=True)
class FieldAtRest:
    """The held field at rest around the body under its family's pair: the levels (the nearest integers), the fine levels at the derived unit, the unit, the iterations to the repeat and the cycle's length, 1 at a fixed point (ALGEBRA.md #the-generator (g))."""

    levels: np.ndarray
    fine: np.ndarray
    unit: int
    iterations: int
    cycle: int


def check_counts(counts: np.ndarray, gamma: int) -> None:
    """The refusals by name: the counts an int64 array of nonnegative integers below Gamma, at least one nonzero (ALGEBRA.md #the-paces, the guard's lower side)."""
    if counts.dtype != np.int64 or counts.size == 0 or not counts.any():
        raise ValueError("the counts are an int64 array (integers only), not zero everywhere: no body")
    low, high = int(counts.min()), int(counts.max())
    if low < 0 or high >= gamma:
        raise ValueError(
            f"a count {low if low < 0 else high}: the counts stay in [0, Gamma) with Gamma = {gamma}"
        )


def division(numerator_coefficient: Any, wall: Any, level: np.ndarray) -> np.ndarray:
    """Rule3's division act on a level: (coefficient x level) div wall, the line with no read, the coefficient as the self coefficient and the remainder not kept (ALGEBRA.md #the-four-acts)."""
    return np.asarray(rule3(NO_READ, NO_READ, numerator_coefficient, wall, level, 0, 0)[0])


def axis_arrivals(a: np.ndarray, axis: int, wrap: Wrap) -> np.ndarray:
    """The two neighbours' levels summed along one axis at every Node, each read through its Port (core/ports.py `arrival`): the row itself twice on an axis of one layer, 0 beyond a closed face (the receive of ALGEBRA.md #the-line)."""
    return np.asarray(arrival(a, axis, 1, wrap[axis]) + arrival(a, axis, -1, wrap[axis]))


def arrivals(a: np.ndarray, wrap: Wrap) -> tuple[np.ndarray, ...]:
    """The six arrivals as Rule3 reads them, one sum per axis."""
    return tuple(axis_arrivals(a, axis, wrap) for axis in range(3))


def field_unit(counts: np.ndarray, num: int) -> int:
    """The field's fine unit, derived and never written: the largest scale of the levels at which num S_6 stays inside the integer width with room, the width div (2 x 6 num x the largest count)."""
    return int(division(1, 2 * 6 * num * int(counts.max()), np.array(MAX_WORK_INT, dtype=object)))


def field_at_rest(counts: np.ndarray, pair: Pair, wrap: Wrap = PERIODIC) -> FieldAtRest:
    """The held family's field at rest under its own line at the pace 1 (ALGEBRA.md #the-line; #the-generator (g)): a stands where 6 den a = num S_6(a), so from nothing b <- num S_6(b) div (6 den) by Rule3's division act on the levels at the fine unit (the counts times the unit at the body's Nodes, rewritten each time: the hold); the map is monotone from nothing, so the levels rise to a fixed point, the stop at its first repeat (exact, no tolerance); the fixed point is below the line's own by less than one fine unit per Node, so the levels, the nearest integers by the division act, are the rest within one unit."""
    check_counts(counts, 1 + int(counts.max()))
    num, den = pair
    if num < 1 or den < num:
        raise ValueError(f"the field's pair [{num}, {den}] has num from 1 and den from num")
    unit = field_unit(counts, num)
    hold = counts > 0
    fine = np.zeros(counts.shape, dtype=np.int64)
    seen: dict[bytes, int] = {}
    step = 0
    key = hashlib.sha256(fine.tobytes()).digest()
    while key not in seen:
        seen[key] = step
        fine = np.asarray(rule3((num, num, num), arrivals(fine, wrap), 0, 6 * den, fine, 0, 0, 1)[0])
        fine[hold] = counts[hold] * unit
        step += 1
        key = hashlib.sha256(fine.tobytes()).digest()
    half = int(division(1, 2, np.array(unit, dtype=object)))
    levels = np.asarray(rule3(NO_READ, NO_READ, 1, unit, fine, 0, half, 1)[0])
    return FieldAtRest(levels, fine, unit, step, step - seen[key])


def chain_axis(counts: np.ndarray) -> int | None:
    """The one axis of extent above one where the other two are folded (a chain), else None."""
    long = [axis for axis in range(3) if counts.shape[axis] > 1]
    return long[0] if len(long) == 1 else None


def chain_rest(counts: np.ndarray, pair: Pair, wrap: Wrap) -> FieldAtRest:
    """The rest on a chain in one pass (ALGEBRA.md #the-generator, THE START): the fixed point of the clamp's map, 6 den b_i = num (b_(i-1) + b_(i+1) + 4 b_i) between the bodies' Nodes with the counts times the unit at them and 0 beyond an open face, solved exactly in integers segment by segment (the tridiagonal line of the same map: the segment's determinants p_k = d p_(k-1) - num^2 p_(k-2) with d = 6 den - 4 num, the Node's value the division act N_i div p_s with N_i = L num^i p_(s-i) + R num^(s+1-i) p_(i-1) from the two ends L and R), the levels then the nearest integers by the division act; the clamp's fixed point, bit for bit."""
    check_counts(counts, 1 + int(counts.max()))
    num, den = pair
    if num < 1 or den < num:
        raise ValueError(f"the field's pair [{num}, {den}] has num from 1 and den from num")
    axis = chain_axis(counts)
    if axis is None:
        raise ValueError("the one-pass rest is the chain's: two axes of extent one")
    unit = field_unit(counts, num)
    line = np.moveaxis(counts, axis, 0).reshape(-1)
    extent = int(line.shape[0])
    clamped = [int(c) * unit for c in line]
    bodies = [i for i, c in enumerate(line) if c > 0]
    diagonal = 6 * den - 4 * num
    fine_values = [0] * extent
    for i in bodies:
        fine_values[i] = clamped[i]

    def solve(nodes: list[int], left: int, right: int) -> None:
        """One free segment between two known values: the determinants' recurrence, then one exact division per Node by the division act."""
        size = len(nodes)
        if size == 0:
            return
        determinants = [1, diagonal]
        powers = [1]
        for _ in range(size + 1):
            determinants.append(diagonal * determinants[-1] - num * num * determinants[-2])
            powers.append(powers[-1] * num)
        for k, node in enumerate(nodes):
            i = k + 1
            numerator = (
                left * powers[i] * determinants[size - i]
                + right * powers[size + 1 - i] * determinants[i - 1]
            )
            fine_values[node] = int(division(numerator, determinants[size], np.array(1, dtype=object)))

    if wrap[axis]:
        for index, start in enumerate(bodies):
            end = bodies[index + 1] if index + 1 < len(bodies) else bodies[0]
            gap = end - start if end > start else end - start + extent
            nodes = []
            for step in range(1, gap):
                node = start + step
                nodes.append(node - extent if node >= extent else node)
            solve(nodes, fine_values[start], fine_values[end])
    else:
        solve(list(range(0, bodies[0])), 0, fine_values[bodies[0]])
        for start, end in zip(bodies, bodies[1:], strict=False):
            solve(list(range(start + 1, end)), fine_values[start], fine_values[end])
        solve(list(range(bodies[-1] + 1, extent)), fine_values[bodies[-1]], 0)
    fine = np.array(fine_values, dtype=np.int64).reshape(np.moveaxis(counts, axis, 0).shape)
    fine = np.moveaxis(fine, 0, axis)
    half = int(division(1, 2, np.array(unit, dtype=object)))
    levels = np.asarray(rule3(NO_READ, NO_READ, 1, unit, fine, 0, half, 1)[0])
    return FieldAtRest(levels, fine, unit, 1, 1)


def rest(counts: np.ndarray, pair: Pair, wrap: Wrap = PERIODIC) -> FieldAtRest:
    """The start's rest of a held family on the counts: the chain's one pass where the region is a chain, the clamp iterated elsewhere (ALGEBRA.md #the-generator, THE START)."""
    return (
        chain_rest(counts, pair, wrap)
        if chain_axis(counts) is not None
        else field_at_rest(counts, pair, wrap)
    )


DECLARATION = Declaration(
    name="the start",
    place="any",
    reads=("a body's counts at its Nodes", "a family's pair", "the faces"),
    writes=("a family's level at a Node",),
    function=rest,
    section="ALGEBRA.md #the-generator, #the-stable-body",
    word="any",
)
