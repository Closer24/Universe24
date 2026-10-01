"""The start, its own folder (ALGEBRA.md #the-generator (g), the start): a held family's rest is the division act iterated from nothing until the levels repeat, 6 den b = num S_6(b) + 3 den sigma at the fine unit from the width, the levels its nearest integers; the refusals by name."""

from __future__ import annotations

import json
import math
from fractions import Fraction

import numpy as np
from scipy.fft import dstn, idstn

from event_universe.core.integer import MAX_WORK_INT
from event_universe.core.ports import Wrap
from event_universe.features.start import arrivals, rest
from tests.laws import UNIVERSE, refused

OPEN_CHAIN = Wrap(False, True, True)


def test_the_rest_is_the_lines_own_fixed_point_on_a_chain_and_a_box():
    """On a chain and a box, at [1, 1], at the binding holder's pair [2400, 2401] (a periodic box too, the screening its sink) and at short-range pairs, with sources of one sign and of both (a box with one open face, its sink): one more act of the line returns the fine levels (the first repeat is a fixed point), the line's residual 6 den b - num S_6(b) - 3 den sigma is within one act's floor (0 to 6 den), and the levels are the fine levels over the unit to the nearest integer, of the sources' sign at the sources (a negative source beside a positive one at 0 at most) and, with one sign, never below 0."""
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


def test_the_tent_on_an_open_chain_is_the_exact_rest_to_the_nearest_integer():
    """The massless line on an open chain of 30 with two sources of 3,600 over the level weight 400: 2 a_i - a_(i-1) - a_(i+1) = 3 sigma_i with 0 beyond the faces, solved in exact rationals; the levels are its nearest integers."""
    counts = np.zeros((30, 1, 1), dtype=np.int64)
    counts[14:16, 0, 0] = 3600
    found = rest(counts, (1, 1), OPEN_CHAIN, 400, MAX_WORK_INT, 3)
    sigma = [Fraction(int(c), 400) * 3 for c in counts[:, 0, 0]]
    diagonal, right = [Fraction(2)] * 30, list(sigma)
    for i in range(1, 30):  # the tridiagonal line eliminated forward, exact
        factor = Fraction(-1) / diagonal[i - 1]
        diagonal[i] -= factor * -1
        right[i] -= factor * right[i - 1]
    exact = [Fraction(0)] * 30
    for i in reversed(range(30)):
        exact[i] = (right[i] + (exact[i + 1] if i + 1 < 30 else 0)) / diagonal[i]
    assert [int(level) for level in found.levels[:, 0, 0]] == [round(value) for value in exact]


def test_the_rest_of_a_gapped_pair_about_one_source_is_isotropic_and_the_lines_exact_solution():
    """The binding holder's pair of the tests' universe at its level weight on a closed box of 21^3 with one source of 1,000 quanta per interval at the centre: the level at the six neighbours is one number (an isotropic rest, the vector test of the two rows), the level falls along each axis all the way to the face, and at every Node the level is the nearest integer of the line's exact solution, 6 den a - num S_6(a) = 3 den sigma with 0 beyond every face solved by the sine transform (the screened well of the six Ports, whose reach is the pair's, ALGEBRA.md #the-well)."""
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


def test_the_refusals_by_name():
    """A board periodic on its every axis at [1, 1] gives the sources no sink; a level weight below 1 is refused."""
    ring = np.zeros((16, 1, 1), dtype=np.int64)
    ring[3, 0, 0] = 2
    refused("needs a sink", lambda: rest(ring, (1, 1), Wrap(True, True, True), 1, MAX_WORK_INT, 3))
    refused("level weight is from 1", lambda: rest(ring, (1, 2), OPEN_CHAIN, 0, MAX_WORK_INT, 6))
