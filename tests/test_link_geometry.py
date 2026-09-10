"""Numerical expectations for generic geometry and travel arithmetic."""

import pytest

from event_universe.core.state import MAX_CORE_INT
from event_universe.dynamics.transit import transit_ticks
from event_universe.fields.geometry import MeanStretch


def test_mean_stretch_fixed_point_and_endpoint_symmetry():
    law = MeanStretch(100, 1, 1)
    assert law(0, 0) == 100
    assert law(10, 10) == 110
    assert law(0, 20) == law(20, 0) == 110
    assert law(1, 0) == 100  # quantization of a state function, not lost transport credit
    assert MeanStretch(100, 1, 2)(20, 20) == 110


def test_transit_respects_c_on_each_edge_without_borrowing():
    for length in (1, 5, 100, 110):
        for speed in (1, 3, 6, 12):
            ticks = transit_ticks(length, (speed, 0, 0), 12)
            assert ticks * speed >= length * 12
            assert (ticks - 1) * speed < length * 12
            assert ticks >= length
    assert transit_ticks(110, (12, 0, 0), 12) == 110
    assert transit_ticks(110, (6, 0, 0), 12) == 220
    assert transit_ticks(110, (120, 0, 0), 12) == 110


@pytest.mark.parametrize(
    "operation",
    [
        lambda: MeanStretch(100, 1, 1)(-1, 0),
        lambda: MeanStretch(100, 1, 1)(1.5, 0),
        lambda: MeanStretch(MAX_CORE_INT, 1, 1)(1, 1),
        lambda: transit_ticks(110, (0, 0, 0), 12),
        lambda: transit_ticks(MAX_CORE_INT, (1, 0, 0), 12),
    ],
)
def test_invalid_and_overflowing_geometry_or_transit_is_rejected(operation):
    with pytest.raises((ValueError, TypeError, OverflowError)):
        operation()
