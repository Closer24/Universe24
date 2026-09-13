"""Fixed read-only records isolate diagnostic calculations from physical evolution."""

from types import MappingProxyType, SimpleNamespace

import pytest

from event_universe import Config, NodeState, ParticleState
from event_universe.diagnostics.frames import Slice, capture_frame, capture_volume
from event_universe.diagnostics.measurements import field_momentum, particle_momentum, total_momentum


@pytest.fixture
def records():
    return SimpleNamespace(
        config=Config(nx=16, ny=16, nz=16),
        tick=0,
        nodes=MappingProxyType(
            {(2, 3, 4): NodeState(9, 10, -20, 30), (6, 7, 8): NodeState(11, -3, 5, -7)}
        ),
        particles=MappingProxyType(
            {5: ParticleState(2, 3, 4, 5, -6, 7), 6: ParticleState(6, 7, 8, -2, 3, -4)}
        ),
    )


def test_momentum_measurements_sum_each_axis_without_modifying_records(records):
    assert particle_momentum(records) == (3, -3, 3)
    assert field_momentum(records) == (7, -15, 23)
    assert total_momentum(records) == (10, -18, 26)
    assert records.nodes[(2, 3, 4)] == NodeState(9, 10, -20, 30)
    assert records.particles[5] == ParticleState(2, 3, 4, 5, -6, 7)


@pytest.mark.parametrize(
    "view,field,particle",
    [
        (Slice("XY", 4), {(2, 3): 9}, (5, 2, 3, 5, -6, 7)),
        (Slice("XZ", 3), {(2, 4): 9}, (5, 2, 4, 5, 7, -6)),
        (Slice("YZ", 2), {(3, 4): 9}, (5, 3, 4, -6, 7, 5)),
    ],
)
def test_each_slice_has_exact_positions_momentum_axes_and_off_plane_exclusion(
    records, view, field, particle
):
    frame = capture_frame(records, view)
    assert frame.field == field
    assert frame.particles == [particle]
    assert frame.total_momentum == (10, -18, 26)
    frame.field.clear()
    frame.particles.clear()
    assert len(records.nodes) == len(records.particles) == 2


def test_empty_momentum_measurement_returns_three_integer_zeros():
    records = SimpleNamespace(nodes={}, particles={})
    assert total_momentum(records) == (0, 0, 0)


def test_volume_preserves_all_three_coordinates_and_copies_off_plane_records(records):
    frame = capture_volume(records)
    assert frame.c_units == records.config.c_units
    assert frame.shape == (16, 16, 16)
    assert frame.field == {(2, 3, 4): 9, (6, 7, 8): 11}
    assert frame.particles == [(5, 2, 3, 4, 5, -6, 7), (6, 6, 7, 8, -2, 3, -4)]
    assert frame.total_momentum == (10, -18, 26)
    frame.field.clear()
    frame.particles.clear()
    assert len(records.nodes) == len(records.particles) == 2


@pytest.mark.parametrize("view", [Slice("XY", -1), Slice("XZ", 16), Slice("YZ", 16)])
def test_out_of_domain_slices_are_rejected(records, view):
    with pytest.raises(ValueError, match="outside"):
        capture_frame(records, view)
