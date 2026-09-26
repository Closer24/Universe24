"""THE COUNT'S LINE, its own folder (ALGEBRA.md 9.121 item 3, the law by the owner's word; 9.119
item 1; 9.57 (1)): Rule3 for the family of clicks with the record's current as its read; a
body at rest keeps its count in place; the count is conserved exactly; the inverse undoes the
line; the int64 bound on the current; the refusals; the declaration."""

from __future__ import annotations

import math

import numpy as np
import pytest

from event_universe.core.integer import MAX_WORK_INT
from event_universe.core.register import folder_of
from event_universe.core.rule3 import coefficients, rule3
from event_universe.features.counts_line import (
    DECLARATION,
    CountStart,
    CountTerm,
    Levels,
    apply,
    bound,
    current,
)


def links_of(levels: Levels, periodic: bool = True) -> tuple[Levels, ...]:
    """The neighbour's levels across each Port as the send puts them on the Link: the wrap on a periodic axis, 0 beyond an open face, the Node itself on an axis of one layer."""
    found = []
    for axis in range(3):
        for sigma in (1, -1):
            found.append(
                Levels(
                    *(
                        None if a is None else across(a, axis, sigma, periodic)
                        for a in (levels.now, levels.before, levels.im_now, levels.im_before)
                    )
                )
            )
    return tuple(found)


def across(a: np.ndarray, axis: int, sigma: int, periodic: bool) -> np.ndarray:
    if a.shape[axis] == 1:
        return a
    rolled = np.roll(a, -sigma, axis=axis)
    if not periodic:
        index = [slice(None)] * 3
        index[axis] = -1 if sigma > 0 else 0
        rolled[tuple(index)] = 0
    return rolled


def standing_record(nodes: int, amplitude: int, num: int, den: int, gamma: int, intervals: int):
    """A record of one standing mode on a ring of Nodes stepped by Rule3 at the vacuum's pace: the levels now and before at every interval."""
    x = np.arange(nodes)
    now = np.rint(amplitude * np.cos(2 * math.pi * x / nodes)).astype(np.int64).reshape(nodes, 1, 1)
    # the mode's own clock from the pair: cos omega = (num / den) cos k at the pace Gamma (9.57 (1))
    omega = math.acos(num / den * math.cos(2 * math.pi / nodes))
    before = np.rint(amplitude * np.cos(2 * math.pi * x / nodes) * math.cos(omega)).astype(np.int64)
    before = before.reshape(nodes, 1, 1)
    reads, self_coefficient, wall = coefficients(num, den, gamma, 0)
    remainder = np.zeros_like(now)
    history = [(now, before)]
    for _ in range(intervals):
        arrivals = (across(now, 0, 1, True) + across(now, 0, -1, True), 2 * now, 2 * now)
        nxt, remainder = rule3(reads, arrivals, self_coefficient, wall, now, before, remainder)
        now, before = nxt, now
        history.append((now, before))
    return history


def test_a_body_at_rest_keeps_its_count_in_place():
    nodes, amplitude = 16, 1 << 10
    num, den, gamma = 1, 2, 10
    history = standing_record(nodes, amplitude, num, den, gamma, 400)
    # T the quantum's norm in the current's units: the mode's form, weight x 2 A^2 x the Nodes
    weight = num
    norm = weight * 2 * amplitude * amplitude * nodes
    term = CountTerm(norm, weight, amplitude, 1)
    count = np.zeros((nodes, 1, 1), dtype=np.int64)
    count[3, 0, 0] = 1  # one quantum at the Node 3
    # the remainder starts at the ladder's origin, (2 u + 1) T div 2 at the residue u = 0 (9.25 (2))
    remainder = np.full_like(count, norm // 2)
    origin = norm * count + remainder
    excursion = 0
    for now, before in history:
        here = Levels(now, before, None, None)
        writes = apply(term, CountStart(count, remainder, here, links_of(here), 1))
        count, remainder = writes.count, writes.remainder
        excursion = max(excursion, int(np.max(np.abs(norm * count + remainder - origin))))
        assert int(count[3, 0, 0]) == 1 and int(count.sum()) == 1 and not np.any(count < 0)
    # the current is not zero to the bit; its accumulated swing stays below half the quantum's norm
    assert 0 < excursion < norm // 2


def test_the_count_is_conserved_exactly_and_the_inverse_undoes_the_line():
    generator = np.random.default_rng(3)
    shape = (4, 3, 2)
    amplitude = 1 << 8
    norm, weight = 5000, 7
    term = CountTerm(norm, weight, amplitude, 1 << 20)
    count = generator.integers(0, 5, size=shape).astype(np.int64)
    remainder = generator.integers(0, norm, size=shape).astype(np.int64)
    for periodic in (True, False):
        for _ in range(50):
            levels = [
                generator.integers(-amplitude, amplitude + 1, size=shape).astype(np.int64)
                for _ in range(4)
            ]
            here = Levels(*levels)
            links = links_of(here, periodic)
            forward = apply(term, CountStart(count, remainder, here, links, 1))
            total = norm * count + remainder
            assert int((norm * forward.count + forward.remainder).sum()) == int(total.sum())
            assert np.all(forward.remainder >= 0) and np.all(forward.remainder < norm)
            assert np.array_equal(sum(forward.net), (norm * forward.count + forward.remainder) - total)
            back = apply(term, CountStart(forward.count, forward.remainder, here, links, -1))
            assert np.array_equal(back.count, count) and np.array_equal(back.remainder, remainder)
            count, remainder = forward.count, forward.remainder


def test_the_current_is_the_booking_and_its_bound_holds_within_int64():
    here = Levels(np.array([3]), np.array([-2]), np.array([5]), np.array([1]))
    there = Levels(np.array([7]), np.array([4]), np.array([-1]), np.array([6]))
    assert int(current(3, here, there)[0]) == 3 * ((3 * 4 - (-2) * 7) + (5 * 6 - 1 * (-1)))
    assert int(current(3, there, here)[0]) == -int(current(3, here, there)[0])
    within = CountTerm(1 << 40, 1000, 1 << 20, 1 << 10)
    assert bound(within) <= MAX_WORK_INT
    beyond = CountTerm(1 << 40, 1000, 1 << 28, 1 << 10)
    assert bound(beyond) > MAX_WORK_INT
    level = np.zeros((1, 1, 1), dtype=np.int64)
    here = Levels(level, level, None, None)
    with pytest.raises(ValueError, match="beyond int64"):
        apply(beyond, CountStart(level, level, here, links_of(here), 1))
    with pytest.raises(ValueError, match="six Links"):
        apply(within, CountStart(level, level, here, links_of(here)[:5], 1))
    with pytest.raises(ValueError, match="direction"):
        apply(within, CountStart(level, level, here, links_of(here), 2))
    with pytest.raises(ValueError, match="from 1"):
        apply(CountTerm(0, 1, 1, 1), CountStart(level, level, here, links_of(here), 1))


def test_the_declaration_is_the_registers_row():
    assert DECLARATION.name == "the count's line" and folder_of(DECLARATION.name) == "counts_line"
    assert DECLARATION.place == "(ii)" and DECLARATION.word == "after the step"
    assert DECLARATION.function is apply and DECLARATION.writes == (
        "the count at a Node",
        "the count's remainder",
    )
