"""The hold's folder (ALGEBRA.md #the-primitives, the row "the hold"): the time part gains (source + r) div E_s each interval by the write's carried division, the carry kept at the Node, exact back; the parts of a rank, the time part and the three tensions Rule3 reads; the refusal by name."""

import numpy as np
import pytest

from event_universe.features.hold import components, diagonal, hold


def test_the_source_adds_the_count_over_the_divisor_each_interval_and_steps_back():
    """A source of 10 over E_s = 7 from the carry 0 adds [1, 1, 2, 1, 2, 1, 2] over seven intervals, 10 in all with the carry back at 0; the inverse takes each increment off and returns the carry, exact on arrays."""
    level, carry, increments = (
        np.zeros((2, 1, 1), dtype=np.int64),
        np.zeros((2, 1, 1), dtype=np.int64),
        [],
    )
    source = np.array([[[10]], [[0]]], dtype=np.int64)
    states = [(level, carry)]
    for _ in range(7):
        after, carry = hold(level, source, 7, carry)
        increments.append(int(after[0, 0, 0] - level[0, 0, 0]))
        level = after
        states.append((level, carry))
    assert increments == [1, 1, 2, 1, 2, 1, 2] and int(level[0, 0, 0]) == 10 and not carry.any()
    assert not level[1].any()
    for back_level, back_carry in reversed(states[:-1]):
        level, carry = hold(level, source, 7, carry, -1)
        assert np.array_equal(level, back_level) and np.array_equal(carry, back_carry)


def test_the_parts_of_a_rank_and_the_refusal():
    """The ranks 1 and 1 + 3: one and four components, the tensions xx, yy, zz right after the time part, none at the rank 1 (the vector and the off-diagonal parts, which Rule3 never reads, left); a divisor below 1 is refused by name."""
    assert [components(parts) for parts in ((1,), (1, 3))] == [1, 4]
    assert diagonal((1, 3)) == (1, 2, 3) and diagonal((1,)) is None
    with pytest.raises(ValueError, match="divisor E_s is from 1"):
        hold(0, 1, 0, 0)
