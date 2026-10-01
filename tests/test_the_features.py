"""The read, its own folder (ALGEBRA.md #the-paces): the content as it is, no floor, the reads summed at their weights; the axis content rounded at the read; the guard at load on squares (the checkerboard factor at -2) admits and refuses by name, and the read in the interval carries no guard. The write's folder and the hold's (ALGEBRA.md #the-primitives, a family's write is one act; the row "the hold"): (numerator + r) div wall at every Node by Rule3's carried division, the remainder kept at the Node, forward then back exact, over many intervals the written total the numerator's within one unit; a held part gains the same division each interval and loses it back; the refusals by name. The start, its own folder (ALGEBRA.md #the-generator (g), the start): a held family's rest is the division act iterated from nothing until the levels repeat, 6 den b = num S_6(b) + 3 den sigma at the fine unit from the width, the levels its nearest integers; the refusals by name."""

import json
import math
from fractions import Fraction
from itertools import pairwise

import numpy as np
from scipy.fft import dstn, idstn
from scipy.sparse import diags, kronsum
from scipy.sparse.linalg import spsolve

from event_universe.core import paces
from event_universe.core.integer import MAX_WORK_INT
from event_universe.core.ports import Wrap
from event_universe.features.hold import hold
from event_universe.features.read import content_of, edge_squared, guard, link_tension, stability_bound
from event_universe.features.start import arrivals, rest, scaled_source
from event_universe.features.write import carried
from tests.laws import UNIVERSE, refused

GAMMA, SHAPE = 10_000, (3, 3, 3)


def test_a_hill_enters_as_it_is_and_the_guard_refuses_a_pace_beyond_the_edge_by_name():
    """No floor and no clamp: a hill of 150 on [800, 850] (the edge's square 2 den Gamma^2 div (den + num) between 10,150^2 and 10,151^2) takes the clock's square to 10,151^2 and the load refuses it naming the Node; 75 passes as it is, the content -75, and the read alone never refuses; the same hill on one Link's content alone is caught on that Port as an integer pace; for den = num the edge is p <= Gamma exactly: a content of -1 refuses by name, a content at Gamma div 2 at both ends of every Link (the Link's pace at 0) refuses on the lower side and Gamma div 2 - 1 passes; for a negative numerator the band's lowest mode is at wave number 0 and the edge's square is 2 den Gamma^2 div (den + |num|), 21 for the pair [-1, 2] at Gamma = 4, so the audit's witness (#1583 B2), the content -1 with the clock's square 26 and 2 cos omega = -23 / 8 at k = 0, is refused by name where the edge of den + num (64) admitted it, and the vacuum of that pair passes. Three reads (2 a - 3 b + 4 c) sum per Node exactly; no reads give the integer 0 (the plain rule at Gamma); the Link's tension is SUM over the reads of (weight x (aa_i + aa_j) + 1) div 2, the mean of its two ends' parts, one division per read per Link: the ends 7 and 7 at the weight 1 give 7 and -7 and -7 give -7 (the Node's own part in a uniform level), the ends 7 and -7 give 0 and a second read of the ends 3 and 4 beside it 0 + 4. Forward the quotient and the remainder of numerator + r; back from the remainder after, the same quotient and the remainder before; forty intervals forward and back exact at three walls; a wall below 1 and a direction other than +1 or -1 are refused by name. A numerator of 10 over the wall 7 from the remainder 0 adds [1, 1, 2, 1, 2, 1, 2] over seven intervals, 10 in all with the remainder back at 0, and the inverse takes each increment off; a wall below 1 is refused by name."""
    (left, right), edge = stability_bound((800, 850), GAMMA), edge_squared((800, 850), GAMMA)
    assert (left, right) == (1_650, GAMMA * GAMMA * 1_700) and edge == right // left
    assert 10_150**2 <= edge < 10_151**2 and GAMMA % 2 == 0
    flat = np.zeros(SHAPE, dtype=np.int64)

    def hill(depth: int) -> np.ndarray:
        return content_of([(-1, np.pad(np.array([[[depth]]]), 1))])

    plain = (np.full(SHAPE, 256),) * 6  # the six Links' factors with no tension, G^2 at G = 16
    assert int(hill(74)[1, 1, 1]) == -74 and int(hill(150)[1, 1, 1]) == -150  # the read carries no guard
    guard((800, 850), GAMMA, 16, hill(74), plain, "matter")
    axis, hollow, deep = plain[0].copy(), flat.copy(), flat.copy()
    axis[2, 0, 1], hollow[0, 1, 0] = 264, -1  # 264: the tension -153, a hill
    deep[1, 1, 1] = paces.frozen_content(GAMMA)  # the Link's zero, 49,545 at Gamma 10,000
    edge, light, hill_pair = r"squared is 103042801 at the Node \(1, 1, 1\) at load", "light", (800, 850)
    port, closed = (*plain[:4], axis, plain[5]), (plain[0], 0 * plain[0], *plain[2:])
    for match, pair, content, factors, name in (
        (rf"the clock\) {edge}", hill_pair, hill(150), plain, "matter"),
        (rf"the Node\) {edge}", hill_pair, hill(75), plain, "matter"),
        (r"the Port 4\) squared is 26400000000 in the unit G\^2 = 256", hill_pair, flat, port, "matter"),
        (r"squared is 100020001 at the Node \(0, 1, 0\) at load, above", (1, 1), hollow, plain, light),
        (r"is 49545 at the Node \(1, 1, 1\) at load, at or beyond 49545", (1, 1), deep, plain, light),
        (r"factor of 'light' \(the Port 1\) is 0 at the Node \(0, 0, 0\)", (1, 1), flat, closed, light),
    ):
        refused(match, guard, pair, GAMMA, 16, content, factors, name)
    deep[1, 1, 1] -= 1
    guard((1, 1), GAMMA, 16, deep, plain, "light")
    assert (stability_bound((-1, 2), 4), edge_squared((-1, 2), 4)) == ((3, 64), 21)  # [-1, 2] at Gamma 4
    witness = r"the clock\) squared is 25 at the Node \(0, 0, 0\) at load, above the stability edge's square 21"
    refused(witness, guard, (-1, 2), 4, 1, flat - 1, (1,) * 6, "quarks")  # the content -1, a hill
    guard((-1, 2), 4, 1, flat, (1,) * 6, "quarks")  # the pair's vacuum, 2 cos omega = -1 at k = 0
    shape, a = (2, 1, 1), np.array([[[5]], [[7]]], dtype=np.int64)
    b, c = np.array([[[1]], [[-2]]], dtype=np.int64), np.array([[[3]], [[0]]], dtype=np.int64)
    assert content_of([(2, a), (-3, b), (4, c)]).tolist() == [[[10 - 3 + 12]], [[14 + 6]]]
    level, full = np.array([[[7]], [[-7]]], dtype=np.int64), np.full(shape, 3)
    assert content_of([]) == 0 and link_tension([]) == 0
    assert link_tension([(1, level, level)]).ravel().tolist() == [7, -7]
    assert link_tension([(1, level, -level), (1, full, full + 1)]).ravel().tolist() == [4, 4]
    draw = np.random.default_rng(11)
    for wall in (1, 7, 12_345):
        numerator, carry = draw.integers(-(10**6), 10**6, (3, 2, 1)), draw.integers(0, wall, (3, 2, 1))
        for _ in range(40):
            quotient, after = carried(numerator, wall, carry)
            assert np.array_equal(quotient * wall + after, numerator + carry) and (0 <= after).all()
            back, before = carried(numerator, wall, after, -1)
            assert (after < wall).all() and np.array_equal(back, quotient)
            assert np.array_equal(before, carry)
            carry = after
    refused("wall is from 1", carried, 5, 0, 0)
    refused("direction", carried, 5, 3, 0, 2)
    zero = np.zeros((2, 1, 1), dtype=np.int64)
    level, carry, states, numerator = zero, zero.copy(), [], np.array([[[10]], [[0]]], dtype=np.int64)
    for _ in range(7):
        states.append((level, carry))
        level, carry = hold(level, numerator, 7, carry)
    steps = [int(a[0, 0, 0] - b[0, 0, 0]) for (b, _), (a, _) in pairwise([*states, (level, carry)])]
    assert (steps, int(level[0, 0, 0]), carry.any(), level[1].any()) == ([1, 1, 2, 1, 2, 1, 2], 10, 0, 0)
    for back_level, back_carry in reversed(states):
        level, carry = hold(level, numerator, 7, carry, -1)
        assert np.array_equal(level, back_level) and np.array_equal(carry, back_carry)
    refused("wall E_s T is from 1", hold, 0, 1, 0, 0)


OPEN_CHAIN = Wrap(False, True, True)


def test_the_rest_is_the_lines_own_fixed_point_on_a_chain_and_a_box():
    """On a chain and a box, at [1, 1], at the binding holder's pair [2400, 2401] (a periodic box too, the screening its sink) and at short-range pairs, with sources of one sign and of both (a box with one open face, its sink): one more act of the line returns the fine levels (the first repeat is a fixed point), the line's residual at the row's own composed paces, (6 (den - num) p_0^2 + 6 num p_i^2) b - num p_i^2 S_6(b) - 3 den Gamma^2 sigma with sigma scaled per proper volume and per proper interval, is within one act's floor (0 to the divisor), and the levels are the fine levels over the unit to the nearest integer, of the sources' sign at the sources (a negative source beside a positive one at 0 at most) and, with one sign, never below 0. The massless line on an open chain of 30 with two sources of 3,600 over the level weight 400: 2 a_i - a_(i-1) - a_(i+1) = 3 sigma_i / p_i^2 with the scaled source and 0 beyond the faces, solved in exact rationals; the levels are its nearest integers. The binding holder's pair of the tests' universe at its level weight on a closed box of 21^3 with one source of 100 quanta per interval at the centre (the fine unit 485; at 1,000 the unit 48 leaves the floored iteration two levels off the exact line): the level at the six neighbours is one number (an isotropic rest, the vector test of the two rows), the level falls along each axis all the way to the face, outside the body the level is the plain line's shape, 6 den a - num S_6(a) = 3 den sigma with 0 beyond every face solved by the sine transform (the screened well of the six Ports, whose reach is the pair's, ALGEBRA.md #the-well), times one factor (the source per proper volume read through the pace at the body, the well shallower by about N at the body, U = U_0 / h, within the levels' rounding), and at every Node the level is within one unit of the self-consistent line at the row's own composed paces with the source scaled as the write scales it, solved sparse. A board periodic on its every axis at [1, 1] gives the sources no sink; a level weight below 1 is refused. The self-consistent line at the row's own paces, solved sparse at those paces, returns the levels."""
    chain = np.zeros((40, 1, 1), dtype=np.int64)
    chain[10:13, 0, 0], chain[25, 0, 0], box = 30, 12, np.zeros((6, 5, 4), dtype=np.int64)
    box[1:3, 1:3, 1] = 9
    mixed = box.copy()
    mixed[4, 2:4, 2], mixed[1, 1, 1] = -13, -9  # sources of both signs, the tension and the senses
    cases = [(chain, OPEN_CHAIN, pair, 7) for pair in ((1, 1), (2400, 2401), (1, 4))]
    cases += [(box, OPEN_CHAIN, (1, 1), 7)] + [(mixed, OPEN_CHAIN, pair, 7) for pair in ((1, 1), (1, 2))]
    cases += [(box, Wrap(True, True, True), (2400, 2401), 1), (box, Wrap(True, True, True), (3, 4), 7)]
    for counts, faces, (num, den), level_weight in cases:
        found = rest(counts, (num, den), faces, level_weight, MAX_WORK_INT, 3 * den, GAMMA)
        fine, own = found.fine.astype(object), found.content.astype(object)
        side = counts.astype(object) * (3 * den * found.unit) // level_weight * GAMMA**2
        clock, pace = paces.node_paces(GAMMA, own)  # the row's own level in its composed paces
        side = paces.write_factor(side, pace, pace, pace, clock, GAMMA, 2)  # per proper volume
        divisor = 6 * (den - num) * clock**2 + 6 * num * pace**2
        left = divisor * fine - num * pace**2 * sum(arrivals(fine, faces)) - side
        assert ((0 >= left) & (left > -divisor)).all(), (num, den, faces)
        assert (found.levels == (fine + found.unit // 2) // found.unit).all() and found.iterations > 1
        assert (found.levels[counts > 0] > 0).all() and (found.levels[counts < 0] <= 0).all()
        assert (found.levels < 0).any() != (counts >= 0).all()  # only negative sources sink below 0
        assert found.remainder == (3 * den - 1) // 2
    counts = np.zeros((30, 1, 1), dtype=np.int64)
    counts[14:16, 0, 0] = 3600
    found = rest(counts, (1, 1), OPEN_CHAIN, 400, MAX_WORK_INT, 3, GAMMA)
    clock, pace = paces.node_paces(GAMMA, found.content)  # the row's own paces, the source at them
    scaled = scaled_source(counts * (3 * found.unit) // 400 * GAMMA**2, clock, pace, GAMMA, 2)
    pairs = zip(scaled[:, 0, 0], pace[:, 0, 0], strict=True)
    right = [Fraction(int(s), found.unit * int(p) ** 2) for s, p in pairs]
    diagonal = [Fraction(2)] * 30  # the scaled source over the pace squared, the line else the plain
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
    counts[10, 10, 10] = 100
    found = rest(counts, (num, den), Wrap(False, False, False), weight, MAX_WORK_INT, 3 * den, GAMMA)
    levels = found.levels
    near = {int(np.moveaxis(levels, a, 0)[10 + s, 10, 10]) for a in range(3) for s in (1, -1)}
    assert len(near) == 1 and 0 < near.pop() < int(levels[10, 10, 10])
    for axis in range(3):
        along = [int(np.moveaxis(levels, axis, 0)[10 + r, 10, 10]) for r in range(11)]
        assert along == sorted(along, reverse=True) and along[10] >= 0
    cosines = np.cos(math.pi * np.arange(1, 22) / 22)
    summed = cosines[:, None, None] + cosines[None, :, None] + cosines[None, None, :]
    denominator = 6 * den - 2 * num * summed
    source = dstn(3 * den * counts.astype(float) / weight, type=1, norm="ortho")
    plain = idstn(source / denominator, type=1, norm="ortho")  # the line at the pace 1, the far limit
    own_paces = paces.node_paces(GAMMA, found.content)  # the row's own composed paces
    clock, pace = (np.asarray(p).astype(float) for p in own_paces)
    own = found.content.astype(float)
    far = (np.abs(own) < GAMMA / 100) & (np.abs(plain) >= 8)  # outside the body: the plain line's shape
    scale = (own / plain)[far]  # one factor, the source per proper volume at the body
    centre = clock[10, 10, 10] / GAMMA  # N at the source: the well shallower by its order, U = U_0 / h
    assert far.any() and 0 < scale.min() and scale.max() < 1.25 * scale.min() < 1.25
    path = diags([1.0, 1.0], [-1, 1], shape=(21, 21))  # the open cube's Links, one axis then the three
    links = kronsum(kronsum(path, path), path)
    divisor = 6 * (den - num) * clock**2 + 6 * num * pace**2  # the Node's term, the Links' -num p^2
    operator = (diags(divisor.ravel()) - diags((num * pace**2).ravel()) @ links).tocsr()
    scaled = scaled_source(counts * (3 * den * found.unit) // weight * GAMMA**2, *own_paces, GAMMA, 2)
    exact = spsolve(operator, (scaled / found.unit).ravel().astype(float))
    assert (np.abs(levels - np.rint(exact).reshape(21, 21, 21)) <= 1).all()
    span = f"plain {plain[10, 10, 10]:.0f}, scale {scale.min():.3f} to {scale.max():.3f}, N {centre:.3f}"
    print(f"GAMEBOARD the well at its paces: centre {int(levels[10, 10, 10])}, {span}")
    ring = np.zeros((16, 1, 1), dtype=np.int64)
    ring[3, 0, 0] = 2
    refused("needs a sink", rest, ring, (1, 1), Wrap(True, True, True), 1, MAX_WORK_INT, 3, GAMMA)
    refused("level weight is from 1", rest, ring, (1, 2), OPEN_CHAIN, 0, MAX_WORK_INT, 6, GAMMA)
