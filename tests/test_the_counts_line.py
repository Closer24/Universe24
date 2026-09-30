"""The count's line (ALGEBRA.md #the-counts-line): T c_next + r' = T c_now + SUM F_ij + r is the exact continuity of Rule3's conserved form, SUM (W_c c + r) is conserved to the bit over a closed board, the inverse returns the start, a hole is conserved and filled; the click is a whole quantum's entry into a detector group through a boundary Port; The exact bands (ALGEBRA.md #rule3): 2 cos omega an integer gives the periods 6, 4 and 3 with no remainder."""

from __future__ import annotations

import random
from fractions import Fraction

import numpy as np
import pytest

from event_universe.core.ports import Wrap
from event_universe.core.rule3 import coefficients, rule3
from event_universe.features.counts_line import CountStart, CountTerm, Levels, apply
from event_universe.reports import Detector, clicks

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


def periodic_start(count: np.ndarray, remainder: np.ndarray, direction: int, levels):
    now, before = levels
    links = []
    for axis in range(3):
        for sign in (1, -1):
            links.append(Levels(np.roll(now, -sign, axis=axis), np.roll(before, -sign, axis=axis)))
    return CountStart(count, remainder, Levels(now, before), tuple(links), direction)


def test_the_count_is_conserved_to_the_bit_and_the_inverse_returns_the_start():
    """Theorem (the count is conserved): on a periodic GameBoard SUM (W_c c + r) is constant; the inverse is the same line with the current reversed, exact."""
    draw, shape = np.random.default_rng(7), (4, 4, 4)
    wall, weight = 3 * 24 * 128, 16
    now = draw.integers(-500, 500, shape).astype(np.int64)
    before = draw.integers(-500, 500, shape).astype(np.int64)
    count = draw.integers(100_000, 200_000, shape).astype(np.int64)
    remainder = draw.integers(0, wall, shape).astype(np.int64)
    term = CountTerm(wall, weight, 1 << 20, int(count.max()))
    forward = apply(term, periodic_start(count, remainder, 1, (now, before)))
    assert int((wall * forward.count + forward.remainder).sum()) == int((wall * count + remainder).sum())
    assert bool(np.all((0 <= forward.remainder) & (forward.remainder < wall)))
    back = apply(term, periodic_start(forward.count, forward.remainder, -1, (now, before)))
    assert np.array_equal(back.count, count) and np.array_equal(back.remainder, remainder)


def test_a_hole_is_conserved_by_the_line_and_the_inverse_fills_it():
    """The remainder's origin: a Node with no quantum reads the count -1 at its first outward swing, a hole the line conserves (SUM (W_c c + r) unchanged, the remainder in range) and the inverse fills exactly (issue #1495 finding 7: the plain division act, no block)."""
    shape, wall = (3, 3, 3), 3 * 24 * 128
    now, before = np.zeros(shape, dtype=np.int64), np.zeros(shape, dtype=np.int64)
    now[1, 1, 1], before[0, 1, 1] = 100_000, 100_000  # a current out of the centre through one Port
    count, remainder = np.zeros(shape, dtype=np.int64), np.zeros(shape, dtype=np.int64)
    term = CountTerm(wall, 16, 1 << 20, 0)
    forward = apply(term, periodic_start(count, remainder, 1, (now, before)))
    assert int(forward.count.min()) < 0
    assert bool(np.all((0 <= forward.remainder) & (forward.remainder < wall)))
    assert int((wall * forward.count + forward.remainder).sum()) == 0
    back = apply(term, periodic_start(forward.count, forward.remainder, -1, (now, before)))
    assert np.array_equal(back.count, count) and np.array_equal(back.remainder, remainder)


@pytest.mark.parametrize(("pair", "period"), [((1, 2), 6), ((0, 1), 4), ((-1, 2), 3)])
def test_the_exact_bands_turn_with_no_remainder(pair, period):
    """The exact bands: a Node at rest in the vacuum (its six reads its own level) turns by 2 cos omega = 2 num / den; the three integer rotations 1, 0 and -1 close in 6, 4 and 3 intervals with the remainder 0 at every step."""
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


def test_a_detectors_click_is_a_whole_quantums_entry_through_a_boundary_port_alone():
    """The click (ALGEBRA.md #the-counts-line; the advisor's ruling, #1515 comment 5909238819): a detector's Nodes are one group; the quanta the inward current carries over the wall at a Port leading in from outside the group click with the Port's axis and side, and none through a Port between two of its Nodes (a hop inside the group is no click)."""
    group = Detector("pair", np.array([True, True, False]).reshape(3, 1, 1), None)
    wrap, zero = Wrap(False, False, False), np.zeros((3, 1, 1), dtype=np.int64)
    inward = np.array([0, 40, 0]).reshape(3, 1, 1)  # a current into Node 1 through one Port
    remainder = np.array([70, 70, 70]).reshape(3, 1, 1)

    def entered(port: int) -> list[dict[str, object]]:
        through = tuple(inward if p == port else zero for p in range(6))
        return clicks(group, group.nodes, through, remainder, zero, 100, wrap, "charge", 5)

    assert [(line["node"], line["axis"]) for line in entered(0)] == [([1, 0, 0], [0, 1])]  # from outside
    assert entered(1) == []  # through -x, from Node 0 inside the group
