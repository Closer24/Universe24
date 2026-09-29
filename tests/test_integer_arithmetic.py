"""The shared bounded integer primitives against independent integers: the working register's bound, the bounded gcd and the GameBoard's extents."""

import sys

import pytest

from event_universe.core.game_board import MAX_VALUE, adjacent_node
from event_universe.core.integer import MAX_WORK_INT, bounded_gcd, checked_work

# The coupling's register, `world.MOMENTUM_BOUND`, as its caller passes it.
REGISTER = (1 << 62) - 1


def test_working_register_is_bounded():
    assert checked_work(MAX_WORK_INT) == MAX_WORK_INT and checked_work(-MAX_WORK_INT) == -MAX_WORK_INT
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


def test_the_bounds_are_the_hosts_width_and_a_gameboard_extent_has_no_cap():
    """The working bound is the host's signed integer width (`sys.maxsize`, no literal), MAX_VALUE half the width less the six Ports' three bits so that a product of two summed over the six Ports fits the width, the gcd's divisions twice the width's bits; a GameBoard extent has no cap beyond 1 (the shape is the file's): an extent above the old cap of 4096 is adjacent and 0 is refused naming "from 1"."""
    assert MAX_WORK_INT == sys.maxsize and MAX_VALUE == (1 << ((MAX_WORK_INT.bit_length() - 3) // 2)) - 1
    assert 6 * MAX_VALUE * MAX_VALUE <= MAX_WORK_INT and bounded_gcd(MAX_WORK_INT, MAX_WORK_INT - 1) == 1
    assert adjacent_node((4998, 0, 0), 0, (5000, 1, 1)) == (4999, 0, 0)
    assert adjacent_node((4999, 0, 0), 0, (5000, 1, 1)) is None
    with pytest.raises(ValueError, match="extents from 1"):
        adjacent_node((0, 0, 0), 0, (0, 1, 1))
