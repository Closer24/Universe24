"""The write's folder (ALGEBRA.md #the-primitives, a family's write is one act): (numerator + r) div wall at every Node by Rule3's carried division, the remainder kept at the Node, forward then back exact, over many intervals the written total the numerator's within one unit, the refusals by name."""

from __future__ import annotations

import numpy as np
import pytest

from event_universe.features.write import carried


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
    with pytest.raises(ValueError, match="wall is from 1"):
        carried(5, 0, 0)
    with pytest.raises(ValueError, match="direction"):
        carried(5, 3, 0, 2)
