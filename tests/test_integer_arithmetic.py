"""The shared bounded integer primitives against independent integers: `by_drive` at constant
rates and its bound, and the age wall `age_wall` with its refusals."""

import random

import pytest

from event_universe.core.integer import (
    MAX_WORK_INT,
    age_wall,
    bounded_gcd,
    by_clock,
    by_drive,
    checked_work,
    signed_inner,
)

# The coupling's register, `world.MOMENTUM_BOUND`, as its caller passes it.
REGISTER = (1 << 62) - 1
RATES = [
    (1, 3),
    (3, 10),
    (7, 3),
    (32, 55),
    (100, 82),
    (1024, 8193),
    (9_736_000_000_000, 290_000_000_000_000),
]


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
    # A bound at the working bound accepts what it holds.
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


# -- the fraction-free primitive ------------------------------------------------------


@pytest.mark.parametrize(("numerator", "denominator"), RATES)
def test_by_drive_at_a_constant_rate_is_by_clock_with_the_remainder_kept(numerator, denominator):
    """(a)."""
    accumulator = 0
    for k in range(1, 10_001):
        count, accumulator = by_drive(accumulator, numerator, denominator)
        assert count == by_clock(k - 1, numerator, denominator), k
        assert accumulator == (k * numerator) % denominator, k


def test_by_drive_takes_the_whole_part_unless_capped():
    """(a), 7 over 3."""
    drive, gained = 0, []
    for _ in range(30):
        count, drive = by_drive(drive, 7, 3)
        gained.append(count)
    assert gained[:6] == [2, 2, 3, 2, 2, 3] and sum(gained) == 70 and drive == 0
    drive, gained = 0, []
    for _ in range(30):
        count, drive = by_drive(drive, 7, 3, at_most=1)
        gained.append(count)
    assert set(gained) == {1} and drive == 120
    drive, gained = 0, []
    for _ in range(30):
        count, drive = by_drive(drive, -7, 3)
        gained.append(count)
    assert gained[:6] == [-2, -2, -3, -2, -2, -3] and sum(gained) == -70 and drive == 0
    drive, gained = 0, []
    for _ in range(30):
        count, drive = by_drive(drive, -7, 3, at_most=1)
        gained.append(count)
    assert set(gained) == {-1} and drive == -120
    with pytest.raises(ValueError, match="positive denominator"):
        by_drive(0, 1, 0)


@pytest.mark.parametrize("denominator", [3, 1000, 1 << 20])
def test_by_drive_keeps_the_accumulator_below_the_denominator(denominator):
    """(b)."""
    draw = random.Random(41)
    unsigned = signed = capped = 0
    for _ in range(10_000):
        rate = draw.randrange(denominator)
        count, unsigned = by_drive(unsigned, rate, denominator)
        assert 0 <= unsigned < denominator and count in (0, 1)
        signed_rate = rate if draw.random() < 0.5 else -rate
        count, signed = by_drive(signed, signed_rate, denominator)
        assert -denominator < signed < denominator and count in (-1, 0, 1)
        count, capped = by_drive(capped, signed_rate, denominator, at_most=1)
        assert -denominator < capped < denominator and count in (-1, 0, 1)


# -- the age wall --------------------------------------------------------------------


def test_the_age_wall_stretches_the_wall_by_the_crowd():
    """(c)."""
    assert age_wall(1, 1, 1, 11, (1, 4)) == (4, 15)
    rate, wall = age_wall(1, 1, 1, 11, (1, 4))
    assert wall - rate == 11 * 1
    assert age_wall(128, 192, 2, 11, (1, 4)) == (512, 192 * (4 + 2 * 11 * 1))
    assert age_wall(128, 192, 2, 11, (1, 4)) == (512, 4992)
    assert age_wall(128, 192, 2, 0, (1, 4)) == (512, 768)
    assert age_wall(3, 5, 1, 0, (0, 7)) == (21, 35)
    fired, accumulator = 0, 0
    for _ in range(15):
        count, accumulator = by_drive(accumulator, 4, 15)
        fired += count
    assert fired == 4 and accumulator == 0
    with pytest.raises(ValueError, match="positive denominator"):
        age_wall(1, 1, 1, 11, (1, 0))
    with pytest.raises(ValueError, match="coefficient is a positive integer"):
        age_wall(1, 1, 0, 11, (1, 4))
    with pytest.raises(ValueError, match="not negative"):
        age_wall(1, 1, 1, -1, (1, 4))
    with pytest.raises(ValueError, match="not negative"):
        age_wall(1, 1, 1, 11, (-1, 4))
