"""Read-only display contracts: arrow speed scale and visible coordinate discontinuities."""

from math import hypot

import pytest

from event_universe.diagnostics.render import _display_jump, _periodic_crossing, _speed_arrow


def test_arrow_length_tracks_speed_and_preserves_direction():
    quarter = _speed_arrow((3, 0, 0), 12)
    full = _speed_arrow((12, 0, 0), 12)
    assert quarter == pytest.approx((2.7, 0, 0))
    assert full == pytest.approx((10.8, 0, 0))
    assert _speed_arrow((-3, 0, 0), 12) == pytest.approx((-2.7, 0, 0))
    diagonal = _speed_arrow((3, 4, 0), 14)
    assert diagonal == pytest.approx((3.24, 4.32, 0))
    assert hypot(*diagonal) == pytest.approx(5.4)


def test_arrow_caps_at_c_and_does_not_invent_a_missing_speed_scale():
    assert _speed_arrow((120, 0, 0), 12) == pytest.approx((10.8, 0, 0))
    assert _speed_arrow((0, 0, 0), 12) == (0, 0, 0)
    assert _speed_arrow((3, 0, 0), None) == (0, 0, 0)
    with pytest.raises(ValueError, match="positive integer"):
        _speed_arrow((3, 0, 0), 0)


@pytest.mark.parametrize(
    "before,after,expected",
    [
        ((4, 5, 6), (4, 5, 6), False),
        ((4, 5, 6), (5, 5, 6), False),
        ((4, 5, 6), (4, 5, 5), False),
        ((4, 5, 6), (6, 5, 6), True),
        ((4, 5, 6), (5, 6, 6), True),
        ((63, 5, 6), (0, 5, 6), True),
    ],
)
def test_jump_means_two_displayed_grid_steps_including_wraps(before, after, expected):
    assert _display_jump(before, after) is expected


@pytest.mark.parametrize(
    "before,after,shape,expected",
    [
        ((63, 5, 6), (0, 5, 6), (64, 48, 32), True),
        ((0, 5, 6), (63, 5, 6), (64, 48, 32), True),
        ((4, 47, 6), (4, 0, 6), (64, 48, 32), True),
        ((4, 5, 0), (4, 5, 31), (64, 48, 32), True),
        ((4, 5, 6), (6, 5, 6), (64, 48, 32), False),
        ((4, 5, 6), (4, 5, 6), (64, 48, 32), False),
        ((63, 5, 6), (0, 5, 6), None, False),
    ],
)
def test_periodic_crossing_uses_domain_size(before, after, shape, expected):
    assert _periodic_crossing(before, after, shape) is expected
