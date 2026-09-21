"""Independent numerical contracts for the shared bounded integer primitives.

The component arithmetic of the deleted engines (signed and ceiling division,
ordered sums, component addition and subtraction, dot and cross products,
reduced ratios) was deleted with its pins on 2026-09-19; see the migration
notes. `by_clock` and `apportion_whole` are pinned where the clock uses them.
"""

import pytest

from event_universe.core.integer import (
    MAX_WORK_INT,
    bounded_gcd,
    checked_work,
    integer_root,
    signed_inner,
)

# The coupling's register, `world.MOMENTUM_BOUND`, as its caller passes it.
REGISTER = (1 << 62) - 1


def test_working_register_is_bounded():
    assert checked_work(MAX_WORK_INT) == MAX_WORK_INT
    assert checked_work(-MAX_WORK_INT) == -MAX_WORK_INT
    with pytest.raises(OverflowError):
        checked_work(MAX_WORK_INT + 1)
    with pytest.raises(OverflowError):
        checked_work(-MAX_WORK_INT - 1)
    with pytest.raises(TypeError):
        checked_work(True)


@pytest.mark.parametrize(
    "value,expected",
    [
        (0, 0),
        (1, 1),
        (2, 1),
        (3, 1),
        (4, 2),
        (15, 3),
        (16, 4),
        (17, 4),
        (1 << 62, 1 << 31),
        (MAX_WORK_INT, 3037000499),
    ],
)
def test_integer_root_is_the_exact_floor(value, expected):
    assert integer_root(value) == expected
    assert expected * expected <= value < (expected + 1) * (expected + 1)


def test_integer_root_refuses_a_negative_a_float_and_an_overflow():
    with pytest.raises(ValueError):
        integer_root(-1)
    with pytest.raises(TypeError):
        integer_root(4.0)
    with pytest.raises(OverflowError):
        integer_root(MAX_WORK_INT + 1)


@pytest.mark.parametrize(
    "first,second,expected",
    [(12, 18, 6), (0, 5, 5), (5, 0, 5), (-4, 6, 2), (0, 0, 0), (MAX_WORK_INT, 1, 1)],
)
def test_bounded_gcd_on_magnitudes(first, second, expected):
    assert bounded_gcd(first, second) == expected


def test_bounded_gcd_checks_its_inputs():
    with pytest.raises(OverflowError):
        bounded_gcd(MAX_WORK_INT + 1, 1)
    with pytest.raises(TypeError):
        bounded_gcd(True, 1)


@pytest.mark.parametrize(
    "left,right,signs,expected",
    [
        # The pointer with itself: 3^2 + 4^2, nothing squared as a step of its own.
        ((3, 4), (3, 4), (1, 1), 25),
        ((-3, 4), (-3, 4), (1, 1), 25),
        # A declared minus on the second component: 25 - 9.
        ((5, 3), (5, 3), (1, -1), 16),
        ((2, 3, 5), (7, 11, 13), (1, -1, 1), 14 - 33 + 65),
        ((0, 9), (9, 0), (1, 1), 0),
        ((), (), (), 0),
        # Exact without a bound: the layer's weights pass 2^64.
        ((1 << 100, 1), (1 << 100, 1), (1, 1), (1 << 200) + 1),
    ],
)
def test_signed_inner_is_the_sum_of_the_signed_products(left, right, signs, expected):
    assert signed_inner(left, right, signs) == expected
    assert signed_inner(list(left), list(right), list(signs)) == expected


def test_signed_inner_at_the_bound():
    assert signed_inner((REGISTER,), (1,), (1,), REGISTER) == REGISTER
    assert signed_inner((REGISTER,), (1,), (-1,), REGISTER) == -REGISTER
    # Two components at the bound with opposite signs: the partial sum
    # reaches the bound and comes back to 0.
    assert signed_inner((REGISTER, REGISTER), (1, 1), (1, -1), REGISTER) == 0
    root = 1 << 31
    within = (root - 1) * root + 1
    assert within <= REGISTER
    assert signed_inner((root - 1, 1), (root, 1), (1, 1), REGISTER) == within
    # 2^31 x 2^31 = 2^62, one beyond: refused before the product is formed.
    with pytest.raises(OverflowError, match="the product at component 0"):
        signed_inner((root,), (root,), (1,), REGISTER)
    # Every product within the bound, the partial sum beyond it.
    with pytest.raises(OverflowError, match="the sum through component 1"):
        signed_inner((REGISTER, 1), (1, 1), (1, 1), REGISTER)
    # A component beyond the bound is refused even against 0.
    with pytest.raises(OverflowError, match="component 0 exceeds"):
        signed_inner((REGISTER + 1,), (0,), (1,), REGISTER)
    # A bound at the working register accepts what the register holds.
    assert signed_inner((MAX_WORK_INT,), (1,), (1,), MAX_WORK_INT) == MAX_WORK_INT


def test_signed_inner_checks_its_inputs():
    with pytest.raises(ValueError, match="different lengths"):
        signed_inner((1, 2), (1,), (1, 1))
    with pytest.raises(ValueError, match="different lengths"):
        signed_inner((1,), (1,), (1, 1))
    with pytest.raises(ValueError, match="a declared sign"):
        signed_inner((1,), (1,), (0,))
    with pytest.raises(ValueError, match="a declared sign"):
        signed_inner((1,), (1,), (2,))
    with pytest.raises(TypeError):
        signed_inner((True,), (1,), (1,))
    with pytest.raises(TypeError):
        signed_inner((1,), (1.0,), (1,))
    with pytest.raises(TypeError):
        signed_inner((1,), (1,), (True,))
    with pytest.raises(ValueError, match="positive integer bound"):
        signed_inner((1,), (1,), (1,), 0)
    with pytest.raises(ValueError, match="positive integer bound"):
        signed_inner((1,), (1,), (1,), True)
