"""The hold's folder (ALGEBRA.md #the-primitives, the row "the hold"): a part gains (numerator + r) div wall each interval by the write's carried division, the one remainder kept at the Node, exact back; the parts of a rank, the time part and the three tensions Rule3 reads; the refusal by name."""

import numpy as np
import pytest

from event_universe.features.hold import components, diagonal, hold


def test_the_parts_of_a_rank_the_one_write_and_the_refusal():
    """The ranks 1 and 1 + 3: one and four components, the tensions xx, yy, zz right after the time part, none at the rank 1 (the vector and the off-diagonal parts, which Rule3 never reads, left); a numerator of 10 over the wall 7 from the remainder 0 adds [1, 1, 2, 1, 2, 1, 2] over seven intervals, 10 in all with the remainder back at 0, and the inverse takes each increment off; a wall below 1 is refused by name."""
    assert [components(parts) for parts in ((1,), (1, 3))] == [1, 4]
    assert diagonal((1, 3)) == (1, 2, 3) and diagonal((1,)) is None
    zero = np.zeros((2, 1, 1), dtype=np.int64)
    level, carry, states = zero, zero.copy(), []
    numerator = np.array([[[10]], [[0]]], dtype=np.int64)
    for _ in range(7):
        states.append((level, carry))
        level, carry = hold(level, numerator, 7, carry)
    assert [
        int(a[0, 0, 0] - b[0, 0, 0])
        for (b, _), (a, _) in zip(states, states[1:] + [(level, carry)], strict=True)
    ] == [1, 1, 2, 1, 2, 1, 2]
    assert int(level[0, 0, 0]) == 10 and not carry.any() and not level[1].any()
    for back_level, back_carry in reversed(states):
        level, carry = hold(level, numerator, 7, carry, -1)
        assert np.array_equal(level, back_level) and np.array_equal(carry, back_carry)
    with pytest.raises(ValueError, match="wall E_s T is from 1"):
        hold(0, 1, 0, 0)
