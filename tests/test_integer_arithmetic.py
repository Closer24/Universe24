"""Independent numerical contracts for the shared bounded integer primitives.

The component arithmetic of the deleted engines (signed and ceiling division,
ordered sums, component addition and subtraction, dot and cross products,
reduced ratios) was deleted with its pins on 2026-09-19; see the migration
notes. `by_clock` and `apportion_whole` are pinned where the clock uses them.
"""

import pytest

from event_universe.core.integer import MAX_WORK_INT, bounded_gcd, checked_work, integer_root


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
