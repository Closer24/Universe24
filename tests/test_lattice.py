import pytest

from event_universe.core.lattice import PeriodicLattice
from event_universe.core.state import DIRECTIONS


def test_periodic_wrapping_handles_negative_and_multiple_domain_lengths():
    assert PeriodicLattice((4, 5, 6)).wrap((-1, 12, 13)) == (3, 2, 1)


def test_neighbor_order_and_sampling_wrap_each_face_consistently():
    lattice = PeriodicLattice((4, 5, 6))
    expected = ((1, 0, 0), (3, 0, 0), (0, 1, 0), (0, 4, 0), (0, 0, 1), (0, 0, 5))
    assert lattice.neighbors((0, 0, 0)) == expected
    assert tuple(lattice.neighbor((0, 0, 0), direction) for direction in range(6)) == expected
    values = dict(zip(expected, (10, 20, 30, 40, 50, 60), strict=True))
    assert lattice.sample((0, 0, 0), values.__getitem__) == (10, 20, 30, 40, 50, 60)


def test_one_node_dimensions_retain_six_directional_neighbor_slots():
    lattice = PeriodicLattice((1, 1, 1))
    assert lattice.neighbors((0, 0, 0)) == ((0, 0, 0),) * 6
    assert lattice.sample((0, 0, 0), lambda address: 7) == (7, 7, 7, 7, 7, 7)


def test_interior_neighbors_are_one_cardinal_edge_away():
    lattice = PeriodicLattice((8, 8, 8))
    origin = (4, 4, 4)
    offsets = tuple(
        tuple(a - b for a, b in zip(point, origin, strict=True)) for point in lattice.neighbors(origin)
    )
    assert offsets == DIRECTIONS


@pytest.mark.parametrize("shape", [(0, 8, 8), (-1, 8, 8), (8, 8), [8, 8, 8]])
def test_invalid_lattice_dimensions_are_rejected(shape):
    with pytest.raises(ValueError):
        PeriodicLattice(shape)


@pytest.mark.parametrize("direction", [-1, 6])
def test_neighbor_rejects_noncardinal_directions(direction):
    with pytest.raises(ValueError):
        PeriodicLattice((8, 8, 8)).neighbor((4, 4, 4), direction)
