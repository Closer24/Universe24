"""THE START, its own folder (ALGEBRA.md #the-generator (g), the start): a held family's rest is the division act iterated from nothing until the levels repeat, 6 den b = num S_6(b) + 3 den sigma at the fine unit from the width, the levels its nearest integers; the refusals by name."""

from __future__ import annotations

from fractions import Fraction

import numpy as np
import pytest

from event_universe.core.integer import MAX_WORK_INT
from event_universe.features.start import arrivals, rest

OPEN_CHAIN = (False, True, True)


def test_the_rest_is_the_lines_own_fixed_point_on_a_chain_and_a_box():
    """On a chain and a box, at [1, 1] and at short-range pairs: one more act of the line returns the fine levels (the first repeat is a fixed point), the line's residual 6 den b - num S_6(b) - 3 den sigma is within one act's floor (0 to 6 den), and the levels are the fine levels over the unit to the nearest integer, positive at the sources and never below 0."""
    chain = np.zeros((40, 1, 1), dtype=np.int64)
    chain[10:13, 0, 0], chain[25, 0, 0] = 30, 12
    box = np.zeros((6, 5, 4), dtype=np.int64)
    box[1:3, 1:3, 1] = 9
    for counts, faces, pair, divisor in (
        (chain, OPEN_CHAIN, (1, 1), 7),
        (chain, OPEN_CHAIN, (1, 4), 7),
        (box, (False, True, True), (1, 1), 7),
        (box, (True, True, True), (3, 4), 7),
    ):
        num, den = pair
        found = rest(counts, pair, faces, divisor, MAX_WORK_INT)
        fine = found.fine.astype(object)
        side = counts.astype(object) * (3 * den * found.unit) // divisor
        left = 6 * den * fine - num * sum(arrivals(fine, faces)) - side
        assert ((0 >= left) & (left > -6 * den)).all(), (pair, faces)
        assert (found.levels == (fine + found.unit // 2) // found.unit).all() and found.iterations > 1
        assert (found.levels[counts > 0] > 0).all() and (found.levels >= 0).all()
        assert (
            found.remainder == (3 * den - 1) // 2 and (found.carries[counts > 0] == divisor // 2).all()
        )


def test_the_tent_on_an_open_chain_is_the_exact_rest_to_the_nearest_integer():
    """The massless line on an open chain of 30 with two sources of 3,600 over the divisor 400: 2 a_i - a_(i-1) - a_(i+1) = 3 sigma_i with 0 beyond the faces, solved in exact rationals; the levels are its nearest integers."""
    counts = np.zeros((30, 1, 1), dtype=np.int64)
    counts[14:16, 0, 0] = 3600
    found = rest(counts, (1, 1), OPEN_CHAIN, 400, MAX_WORK_INT)
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


def test_the_refusals_by_name():
    """A board periodic on its every axis at [1, 1] gives the sources no sink; sources of two signs make the map no longer monotone; a divisor below 1 is refused."""
    ring = np.zeros((16, 1, 1), dtype=np.int64)
    ring[3, 0, 0] = 2
    with pytest.raises(ValueError, match="needs a sink"):
        rest(ring, (1, 1), (True, True, True), 1, MAX_WORK_INT)
    ring[11, 0, 0] = -2
    with pytest.raises(ValueError, match="of one sign"):
        rest(ring, (1, 2), (True, True, True), 1, MAX_WORK_INT)
    with pytest.raises(ValueError, match="divisor is from 1"):
        rest(ring, (1, 2), OPEN_CHAIN, 0, MAX_WORK_INT)
