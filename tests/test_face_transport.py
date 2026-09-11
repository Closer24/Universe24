"""Independent delivery and atomicity checks without running duplicate worlds."""

import pytest

from event_universe.core.faces import ScalarFaceTransport
from event_universe.core.lattice import PeriodicLattice
from event_universe.core.state import MAX_CORE_INT
from event_universe.core.streams import StreamTransport


def test_scalar_publisher_cannot_create_field_from_zero():
    with pytest.raises(ValueError):
        ScalarFaceTransport(PeriodicLattice((16, 16, 16)), lambda value: (1, 0, 0, 0, 0, 0))


def test_scalar_publisher_delivery_is_directional_one_edge_and_atomic():
    def publish(value):
        return (value, 2 * value, 3 * value, 4 * value, 5 * value, 6 * value)

    transport = ScalarFaceTransport(PeriodicLattice((16, 16, 16)), publish)
    transport.advance({(5, 5, 5): 7})
    assert transport.at((6, 5, 5)) == (0, 7, 0, 0, 0, 0)
    assert transport.at((4, 5, 5)) == (14, 0, 0, 0, 0, 0)
    assert transport.at((5, 6, 5)) == (0, 0, 0, 21, 0, 0)
    assert transport.at((7, 5, 5)) == (0,) * 6
    before = dict(transport.cells)
    with pytest.raises(OverflowError):
        transport.advance({(5, 5, 5): MAX_CORE_INT})
    assert dict(transport.cells) == before
    transport.advance({})
    assert not transport.cells


def forward_only(populations, count, strength, phase):
    """Test law: forward octant zero to +x, preserving one known integer."""
    zero = (0,) * 8
    return ((populations[0] + count * strength, *zero[1:]), zero, zero, zero, zero, zero)


def test_stream_delivery_uses_old_snapshot_and_arrival_face():
    transport = StreamTransport(PeriodicLattice((16, 16, 16)), forward_only, 7)
    origin, first, second = (5, 5, 5), (6, 5, 5), (7, 5, 5)
    transport.advance({origin: 1}, 0)
    assert transport.at(first).populations == (7, 0, 0, 0, 0, 0, 0, 0)
    assert transport.at(first).flux == (0, 7, 0, 0, 0, 0)
    assert transport.at(second).populations == (0,) * 8
    transport.advance({}, 1)
    assert transport.at(first).populations == (0,) * 8
    assert transport.at(second).flux == (0, 7, 0, 0, 0, 0)


def test_stream_overflow_rejects_complete_transport_commit():
    transport = StreamTransport(PeriodicLattice((16, 16, 16)), forward_only, MAX_CORE_INT)
    origin, first = (5, 5, 5), (6, 5, 5)
    transport.advance({origin: 1}, 0)
    before = dict(transport.cells)
    with pytest.raises(OverflowError):
        transport.advance({first: 1}, 1)
    assert dict(transport.cells) == before
