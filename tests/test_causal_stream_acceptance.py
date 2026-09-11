"""Independent active-source/free-control acceptance for the delivered-face candidate."""

from dataclasses import replace

import pytest

from event_universe import CausalStreamConfig
from event_universe.api import FaceStreamSimulation


@pytest.mark.parametrize(
    "momentum",
    [(1, 0, 0), (3, 0, 0), (12, 0, 0), (0, -3, 0), (0, 0, 12), (1, 1, 0), (3, -2, 1), (6, 4, -2)],
)
def test_active_stream_matches_free_trajectory_at_every_tick(momentum, monkeypatch):
    settings = CausalStreamConfig(nx=257, ny=257, nz=257, c_units=12, source_per_octant=1, force_den=12)
    active = FaceStreamSimulation(settings)
    control = FaceStreamSimulation(replace(settings, source_per_octant=0))

    def forbid_scalar_lookup(*args):
        raise AssertionError("response must use delivered faces, not remote scalar lookups")

    monkeypatch.setattr(active, "phi", forbid_scalar_lookup)
    monkeypatch.setattr(type(active._lattice), "sample", forbid_scalar_lookup)
    origin = (128, 128, 128)
    for world in (active, control):
        world.add_particle(0, *origin, *momentum)
    for tick in range(1, 73):
        active.step()
        control.step()
        actual, free = active.particles[0], control.particles[0]
        assert actual.momentum == free.momentum == momentum
        assert actual.position == free.position
        assert (actual.force_rx, actual.force_ry, actual.force_rz) == (0, 0, 0)
        assert any(any(cell.populations) for cell in active.streams.cells.values())
        assert not any(any(cell.populations) for cell in control.streams.cells.values())
        if tick % 12 == 0:
            expected = tuple(origin[axis] + tick // 12 * momentum[axis] for axis in range(3))
            assert free.position == expected
