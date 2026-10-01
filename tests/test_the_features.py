"""The read, its own folder (ALGEBRA.md #the-paces): the content as it is, no floor, the reads summed at their weights; the axis content rounded at the read; the guard at load on squares (the checkerboard factor at -2) admits and refuses by name, and the read in the interval carries no guard. The write's folder and the hold's (ALGEBRA.md #the-primitives, a family's write is one act; the row "the hold"): (numerator + r) div wall at every Node by Rule3's carried division, the remainder kept at the Node, forward then back exact, over many intervals the written total the numerator's within one unit; a held part gains the same division each interval and loses it back; the refusals by name. The start, its own folder (ALGEBRA.md #the-generator (g), the start): a held family's rest is the division act iterated from nothing until the levels repeat, 6 den b = num S_6(b) + 3 den sigma at the fine unit from the width, the levels its nearest integers; the refusals by name."""

import json
import math
from fractions import Fraction
from itertools import pairwise

import numpy as np
import pytest
from scipy.fft import dstn, idstn

from event_universe.core.integer import MAX_WORK_INT
from event_universe.core.ports import Wrap
from event_universe.features.hold import hold
from event_universe.features.read import axis_content, content_of, edge_squared, guard, stability_bound
from event_universe.features.start import arrivals, rest
from event_universe.features.write import carried
from tests.laws import UNIVERSE

GAMMA, SHAPE = 10_000, (3, 3, 3)


def test_a_hill_enters_as_it_is_and_the_guard_refuses_a_pace_beyond_the_edge_by_name():
    """No floor and no clamp: a hill of 150 on [800, 850] (the edge's square 2 den Gamma^2 div (den + num) between 10,150^2 and 10,151^2) takes the clock's square to 10,151^2 and the load refuses it naming the Node; 75 passes as it is, the content -75, and the read alone never refuses; the same hill on the axis contents alone is caught on that axis as an integer pace; for den = num the edge is p <= Gamma exactly: a content of -1 refuses by name, a content at Gamma div 2 (the Link's pace at 0) refuses on the lower side and Gamma div 2 - 1 passes. Three reads (2 a - 3 b + 4 c) sum per Node exactly; no reads give the integer 0 (the plain rule at Gamma); the axis content is SUM over the reads of (weight x level + 1) div 2, one division per read: 7 and -7 at the weight 1 give 4 and -3, two reads of 3 and 4 give 2 + 2. Forward the quotient and the remainder of numerator + r; back from the remainder after, the same quotient and the remainder before; forty intervals write forty times the numerator over the wall within one unit; a wall below 1 and a direction other than +1 or -1 are refused by name. A numerator of 10 over the wall 7 from the remainder 0 adds [1, 1, 2, 1, 2, 1, 2] over seven intervals, 10 in all with the remainder back at 0, and the inverse takes each increment off; a wall below 1 is refused by name."""
    (left, right), edge = stability_bound((800, 850), GAMMA), edge_squared((800, 850), GAMMA)
    assert (left, right) == (1_650, GAMMA * GAMMA * 1_700) and edge == right // left
    assert 10_150**2 <= edge < 10_151**2 and GAMMA % 2 == 0
    flat = np.zeros(SHAPE, dtype=np.int64)

    def hill(depth: int) -> np.ndarray:
        return content_of([(-1, np.pad(np.array([[[depth]]]), 1))])

    assert int(hill(75)[1, 1, 1]) == -75 and int(hill(150)[1, 1, 1]) == -150  # the read carries no guard
    guard((800, 850), GAMMA, hill(75), (flat, flat, flat), "matter")
    with pytest.raises(ValueError, match=r"squared is 103045000 at the Node \(1, 1, 1\) at load"):
        guard((800, 850), GAMMA, hill(150), (flat, flat, flat), "matter")
    axis, hollow, deep = flat.copy(), flat.copy(), flat.copy()
    axis[2, 0, 1], hollow[0, 1, 0], deep[1, 1, 1] = -153, -1, GAMMA // 2
    with pytest.raises(ValueError, match=r"axis 2\) squared is 103083409 at the Node \(2, 0, 1\)"):
        guard((800, 850), GAMMA, flat, (flat, flat, axis), "matter")
    with pytest.raises(ValueError, match=r"squared is 100020002 at the Node \(0, 1, 0\) at load, above"):
        guard((1, 1), GAMMA, hollow, (flat, flat, flat), "light")
    with pytest.raises(ValueError, match=r"is 0 at the Node \(1, 1, 1\) at load: the pace"):
        guard((1, 1), GAMMA, deep, (flat, flat, flat), "light")
    deep[1, 1, 1] = GAMMA // 2 - 1
    guard((1, 1), GAMMA, deep, (flat, flat, flat), "light")
    shape, a = (2, 1, 1), np.array([[[5]], [[7]]], dtype=np.int64)
    b, c = np.array([[[1]], [[-2]]], dtype=np.int64), np.array([[[3]], [[0]]], dtype=np.int64)
    assert content_of([(2, a), (-3, b), (4, c)]).tolist() == [[[10 - 3 + 12]], [[14 + 6]]]
    assert content_of([]) == 0 and axis_content([]) == 0
    level = np.array([[[7]], [[-7]]], dtype=np.int64)
    assert axis_content([(1, level)]).ravel().tolist() == [4, -3]
    assert axis_content([(1, np.full(shape, 3)), (1, np.full(shape, 4))]).ravel().tolist() == [4, 4]
    draw = np.random.default_rng(11)
    for wall in (1, 7, 12_345):
        numerator = draw.integers(-(10**6), 10**6, (3, 2, 1))
        carry, written = draw.integers(0, wall, (3, 2, 1)), np.zeros((3, 2, 1), dtype=np.int64)
        start = carry.copy()
        for _ in range(40):
            quotient, after = carried(numerator, wall, carry)
            assert np.array_equal(quotient * wall + after, numerator + carry) and (0 <= after).all()
            assert (after < wall).all()
            back, before = carried(numerator, wall, after, -1)
            assert np.array_equal(back, quotient) and np.array_equal(before, carry)
            written, carry = written + quotient, after
        assert np.array_equal(written * wall + carry, 40 * numerator + start)
    with pytest.raises(ValueError, match="wall is from 1"):
        carried(5, 0, 0)
    with pytest.raises(ValueError, match="direction"):
        carried(5, 3, 0, 2)
    zero = np.zeros((2, 1, 1), dtype=np.int64)
    level, carry, states = zero, zero.copy(), []
    numerator = np.array([[[10]], [[0]]], dtype=np.int64)
    for _ in range(7):
        states.append((level, carry))
        level, carry = hold(level, numerator, 7, carry)
    steps = [int(a[0, 0, 0] - b[0, 0, 0]) for (b, _), (a, _) in pairwise([*states, (level, carry)])]
    assert (steps, int(level[0, 0, 0]), carry.any(), level[1].any()) == ([1, 1, 2, 1, 2, 1, 2], 10, 0, 0)
    for back_level, back_carry in reversed(states):
        level, carry = hold(level, numerator, 7, carry, -1)
        assert np.array_equal(level, back_level) and np.array_equal(carry, back_carry)
    with pytest.raises(ValueError, match="wall E_s T is from 1"):
        hold(0, 1, 0, 0)


OPEN_CHAIN = Wrap(False, True, True)


def test_the_rest_is_the_lines_own_fixed_point_on_a_chain_and_a_box():
    """On a chain and a box, at [1, 1], at the binding holder's pair [2400, 2401] (a periodic box too, the screening its sink) and at short-range pairs, with sources of one sign and of both (a box with one open face, its sink): one more act of the line returns the fine levels (the first repeat is a fixed point), the line's residual 6 den b - num S_6(b) - 3 den sigma is within one act's floor (0 to 6 den), and the levels are the fine levels over the unit to the nearest integer, of the sources' sign at the sources (a negative source beside a positive one at 0 at most) and, with one sign, never below 0. The massless line on an open chain of 30 with two sources of 3,600 over the level weight 400: 2 a_i - a_(i-1) - a_(i+1) = 3 sigma_i with 0 beyond the faces, solved in exact rationals; the levels are its nearest integers. The binding holder's pair of the tests' universe at its level weight on a closed box of 21^3 with one source of 1,000 quanta per interval at the centre: the level at the six neighbours is one number (an isotropic rest, the vector test of the two rows), the level falls along each axis all the way to the face, and at every Node the level is the nearest integer of the line's exact solution, 6 den a - num S_6(a) = 3 den sigma with 0 beyond every face solved by the sine transform (the screened well of the six Ports, whose reach is the pair's, ALGEBRA.md #the-well). A board periodic on its every axis at [1, 1] gives the sources no sink; a level weight below 1 is refused."""
    chain = np.zeros((40, 1, 1), dtype=np.int64)
    chain[10:13, 0, 0], chain[25, 0, 0] = 30, 12
    box = np.zeros((6, 5, 4), dtype=np.int64)
    box[1:3, 1:3, 1] = 9
    mixed = box.copy()
    mixed[4, 2:4, 2], mixed[1, 1, 1] = -13, -9  # sources of both signs, the tension and the senses
    cases = [(chain, OPEN_CHAIN, (1, 1), 7), (chain, OPEN_CHAIN, (2400, 2401), 1)]
    cases += [(chain, OPEN_CHAIN, (1, 4), 7), (box, OPEN_CHAIN, (1, 1), 7)]
    cases += [(box, Wrap(True, True, True), (2400, 2401), 1), (box, Wrap(True, True, True), (3, 4), 7)]
    cases += [(mixed, OPEN_CHAIN, (1, 1), 7), (mixed, OPEN_CHAIN, (1, 2), 7)]
    for counts, faces, pair, level_weight in cases:
        num, den = pair
        found = rest(counts, pair, faces, level_weight, MAX_WORK_INT, 3 * den)
        fine = found.fine.astype(object)
        side = counts.astype(object) * (3 * den * found.unit) // level_weight
        left = 6 * den * fine - num * sum(arrivals(fine, faces)) - side
        assert ((0 >= left) & (left > -6 * den)).all(), (pair, faces)
        assert (found.levels == (fine + found.unit // 2) // found.unit).all() and found.iterations > 1
        if (counts >= 0).all():
            assert (found.levels[counts > 0] > 0).all() and (found.levels >= 0).all()
        else:
            assert (found.levels[counts > 0] > 0).all() and (found.levels[counts < 0] <= 0).all()
            assert (found.levels < 0).any()  # the far negative sources sink below 0
        assert found.remainder == (3 * den - 1) // 2
    counts = np.zeros((30, 1, 1), dtype=np.int64)
    counts[14:16, 0, 0] = 3600
    found = rest(counts, (1, 1), OPEN_CHAIN, 400, MAX_WORK_INT, 3)
    diagonal, right = [Fraction(2)] * 30, [Fraction(int(c), 400) * 3 for c in counts[:, 0, 0]]
    for i in range(1, 30):  # the tridiagonal line eliminated forward, exact
        diagonal[i] -= 1 / diagonal[i - 1]
        right[i] += right[i - 1] / diagonal[i - 1]
    exact = [Fraction(0)] * 30
    for i in reversed(range(30)):
        exact[i] = (right[i] + (exact[i + 1] if i + 1 < 30 else 0)) / diagonal[i]
    assert [int(level) for level in found.levels[:, 0, 0]] == [round(value) for value in exact]
    rows = json.loads(UNIVERSE.read_text(encoding="utf-8"))["families"]
    row = next(entry for entry in rows if entry["name"] == "binding")
    (num, den), weight = row["pair"], row["held"]["level_weight"]
    counts = np.zeros((21, 21, 21), dtype=np.int64)
    counts[10, 10, 10] = 1000
    levels = rest(counts, (num, den), Wrap(False, False, False), weight, MAX_WORK_INT, 3 * den).levels
    near = {int(np.moveaxis(levels, a, 0)[10 + s, 10, 10]) for a in range(3) for s in (1, -1)}
    assert len(near) == 1 and 0 < near.pop() < int(levels[10, 10, 10])
    for axis in range(3):
        along = [int(np.moveaxis(levels, axis, 0)[10 + r, 10, 10]) for r in range(11)]
        assert along == sorted(along, reverse=True) and along[10] >= 0
    cosines = np.cos(math.pi * np.arange(1, 22) / 22)
    summed = cosines[:, None, None] + cosines[None, :, None] + cosines[None, None, :]
    denominator = 6 * den - 2 * num * summed
    source = dstn(3 * den * counts.astype(float) / weight, type=1, norm="ortho")
    exact = idstn(source / denominator, type=1, norm="ortho")
    assert np.array_equal(levels, np.rint(exact).astype(np.int64))
    ring = np.zeros((16, 1, 1), dtype=np.int64)
    ring[3, 0, 0] = 2
    with pytest.raises(ValueError, match="needs a sink"):
        rest(ring, (1, 1), Wrap(True, True, True), 1, MAX_WORK_INT, 3)
    with pytest.raises(ValueError, match="level weight is from 1"):
        rest(ring, (1, 2), OPEN_CHAIN, 0, MAX_WORK_INT, 6)
