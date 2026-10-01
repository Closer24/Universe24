"""The write's folder and the hold's (ALGEBRA.md #the-primitives, a family's write is one act; the row "the hold"): (numerator + r) div wall at every Node by Rule3's carried division, the remainder kept at the Node, forward then back exact, over many intervals the written total the numerator's within one unit; a held part gains the same division each interval and loses it back; the refusals by name."""

from __future__ import annotations

from itertools import pairwise

import numpy as np

from event_universe.features.hold import hold
from event_universe.features.write import carried
from tests.laws import refused


def test_the_write_is_the_carried_division_exact_back_and_refusing_by_name():
    """Forward the quotient and the remainder of numerator + r; back from the remainder after, the same quotient and the remainder before; forty intervals write forty times the numerator over the wall within one unit; a wall below 1 and a direction other than +1 or -1 are refused by name."""
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
    refused("wall is from 1", lambda: carried(5, 0, 0))
    refused("direction", lambda: carried(5, 3, 0, 2))


def test_the_one_write_and_the_refusal():
    """A numerator of 10 over the wall 7 from the remainder 0 adds [1, 1, 2, 1, 2, 1, 2] over seven intervals, 10 in all with the remainder back at 0, and the inverse takes each increment off; a wall below 1 is refused by name."""
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
    refused("wall E_s T is from 1", lambda: hold(0, 1, 0, 0))
