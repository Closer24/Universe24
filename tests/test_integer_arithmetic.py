"""Independent numerical contracts for the shared bounded integer primitives.

The component arithmetic of the deleted engines (signed and ceiling division,
ordered sums, component addition and subtraction, dot and cross products,
reduced ratios) was deleted with its pins on 2026-09-19; see the migration
notes. `by_clock` and `apportion_whole` are pinned where the clock uses them.

The fraction-free primitive (2026-09-20, the mathematician's
docs/designs/fraction_free/FORM.md section 1; `by_drive` with the whole part
as its default and the step's cap `at_most`), the integers written first:
(a) the identity at a constant rate over 10^4 self-creations on seven rates
    from 1 / 3 to a star's 9 736 000 000 000 / 290 000 000 000 000: from an
    empty accumulator `by_drive` gains `by_clock(k - 1, n, d)` at the k-th
    self-creation and holds `(k n) mod d` after it; at 7 over 3 the counts
    2, 2, 3, 2, 2, 3, ... (70 over thirty, the accumulator 0 after), and
    with `at_most` 1 one per self-creation and 120 kept after thirty; the
    signed rate -7 the same with the sign;
(b) the bound: under 10^4 random rates below the denominator (3, 1000,
    2^20) an unsigned accumulator stays in [0, d) and a signed one in
    (-d, d), with the cap and without, the count in {-1, 0, 1} for a rate
    below the denominator; a denominator below 1 is refused.
"""

import random

import pytest

from event_universe.core.integer import (
    MAX_WORK_INT,
    bounded_gcd,
    by_clock,
    by_drive,
    checked_work,
    integer_root,
)

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
