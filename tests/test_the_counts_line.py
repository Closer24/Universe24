"""THE COUNT'S LINE (ALGEBRA.md #the-counts-line): T c_next + r' = T c_now + SUM F_ij + r is the exact continuity of Rule3's conserved form, SUM (W_c c + r) is conserved to the bit over a closed board, the inverse returns the start, a count below zero at the interval's end is refused by name; THE EXACT BANDS (ALGEBRA.md #rule3): 2 cos omega an integer gives the periods 6, 4 and 3 with no remainder."""

from __future__ import annotations

import random
import re
from fractions import Fraction

import numpy as np
import pytest

from event_universe.core.rule3 import coefficients, rule3
from event_universe.features.counts_line import CountStart, CountTerm, Levels, apply

GAMMA, NODES = 10_000, 12


def ring_sum(values: list[Fraction]) -> list[Fraction]:
    """S_6 on a ring with four self reads: the six Ports' arrivals of a Node."""
    return [4 * values[i] + values[i - 1] + values[(i + 1) % NODES] for i in range(NODES)]


@pytest.mark.parametrize("pair", [(24, 24), (16, 24), (5000, 10000)])
def test_the_forms_share_changes_by_the_currents_exactly(pair):
    """E_i / 2 = 3 den (now^2 + before^2) - num now S_6(before): its change over one interval of Rule3 (exact in rationals) is SUM_j F_ij with F_ij = num (now_i before_j - before_i now_j), at every Node (issue #1495 finding 6)."""
    num, den = pair
    (read, _, _), self_coefficient, wall = coefficients(num, den, GAMMA, 0)
    draw = random.Random(3)
    now = [Fraction(draw.randint(-1000, 1000)) for _ in range(NODES)]
    before = [Fraction(draw.randint(-1000, 1000)) for _ in range(NODES)]
    nxt = [
        (read * ring_sum(now)[i] + self_coefficient * now[i] - wall * before[i]) / wall
        for i in range(NODES)
    ]

    def share(a: list[Fraction], b: list[Fraction]) -> list[Fraction]:
        return [3 * den * (a[i] ** 2 + b[i] ** 2) - num * a[i] * ring_sum(b)[i] for i in range(NODES)]

    flux = [num * (now[i] * ring_sum(before)[i] - before[i] * ring_sum(now)[i]) for i in range(NODES)]
    assert [share(nxt, now)[i] - share(now, before)[i] for i in range(NODES)] == flux


def periodic_start(
    draw: random.Random, count: np.ndarray, remainder: np.ndarray, direction: int, levels
):
    now, before = levels
    links = []
    for axis in range(3):
        for sign in (1, -1):
            links.append(
                Levels(np.roll(now, sign, axis=axis), np.roll(before, sign, axis=axis), None, None)
            )
    return CountStart(count, remainder, Levels(now, before, None, None), tuple(links), direction)


def test_the_count_is_conserved_to_the_bit_and_the_inverse_returns_the_start():
    """THEOREM (the count is conserved): on a periodic GameBoard SUM (W_c c + r) is constant; THE INVERSE is the same line with the current reversed, exact."""
    draw, shape = np.random.default_rng(7), (4, 4, 4)
    wall, weight = 3 * 24 * 128, 16
    now = draw.integers(-500, 500, shape).astype(np.int64)
    before = draw.integers(-500, 500, shape).astype(np.int64)
    count = draw.integers(100_000, 200_000, shape).astype(np.int64)
    remainder = draw.integers(0, wall, shape).astype(np.int64)
    term = CountTerm(wall, weight, 1 << 20, int(count.max()))
    forward = apply(term, periodic_start(draw, count, remainder, 1, (now, before)))
    assert int((wall * forward.count + forward.remainder).sum()) == int((wall * count + remainder).sum())
    assert bool(np.all((0 <= forward.remainder) & (forward.remainder < wall)))
    back = apply(term, periodic_start(draw, forward.count, forward.remainder, -1, (now, before)))
    assert np.array_equal(back.count, count) and np.array_equal(back.remainder, remainder)


def test_a_count_below_zero_at_the_intervals_end_is_refused_by_name():
    """THE COUNT IS NEVER NEGATIVE: a Node with no quantum reads the count -1 at its first outward swing (T c + r below 0), the arithmetic's hole, and the line refuses it by name at the interval's end with the quanta it would move and the count held there (ALGEBRA.md #the-counts-line THE INVERSE: a defect of the lay, never a clamp and never a block; issue #1495 finding 7); the same current from a Node holding the quanta moves them, conserved to the bit."""
    shape, wall = (3, 3, 3), 3 * 24 * 128
    now, before = np.zeros(shape, dtype=np.int64), np.zeros(shape, dtype=np.int64)
    now[1, 1, 1], before[0, 1, 1] = 100_000, 100_000  # a current out of the centre through one Port
    count, remainder = np.zeros(shape, dtype=np.int64), np.zeros(shape, dtype=np.int64)
    term = CountTerm(wall, 16, 1 << 20, 0)
    draw = np.random.default_rng(1)
    with pytest.raises(ValueError, match=r"holding 0 < .*never negative") as refusal:
        apply(term, periodic_start(draw, count, remainder, 1, (now, before)))
    named = re.search(r"move (\d+) quanta .* Node (\d+) in", str(refusal.value))
    moved, node = (int(named[1]), int(named[2])) if named else (0, 0)
    count.ravel()[node] = moved  # the Node named, holding what the current moves
    forward = apply(term, periodic_start(draw, count, remainder, 1, (now, before)))
    assert int(forward.count.min()) >= 0 and int(forward.count.ravel()[node]) == 0
    assert int((wall * forward.count + forward.remainder).sum()) == moved * wall


@pytest.mark.parametrize(("pair", "period"), [((1, 2), 6), ((0, 1), 4), ((-1, 2), 3)])
def test_the_exact_bands_turn_with_no_remainder(pair, period):
    """THE EXACT BANDS: a Node at rest in the vacuum (its six reads its own level) turns by 2 cos omega = 2 num / den; the three integer rotations 1, 0 and -1 close in 6, 4 and 3 intervals with the remainder 0 at every step."""
    num, den = pair
    (read, _, _), self_coefficient, wall = coefficients(num, den, GAMMA, 0)
    before, now = 0, 1_000
    for _ in range(1, period + 1):
        nxt, carry = rule3(
            (read, read, read), (2 * now, 2 * now, 2 * now), self_coefficient, wall, now, before, 0
        )
        assert carry == 0
        before, now = now, nxt
    assert (before, now) == (0, 1_000)
