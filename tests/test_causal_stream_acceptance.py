"""Independent active-source/free-control acceptance for the delivered-face candidate."""

from dataclasses import replace

import pytest

from event_universe import CausalStreamConfig, Config
from event_universe.api import FaceStreamSimulation, GenericFaceSimulation
from event_universe.fields.definitions import octant_definition


@pytest.mark.parametrize(
    "momentum,generic",
    [
        ((1, 0, 0), False),
        ((3, 0, 0), False),
        ((12, 0, 0), False),
        ((0, -3, 0), False),
        ((0, 0, 12), False),
        ((1, 1, 0), False),
        ((3, -2, 1), False),
        ((6, 4, -2), False),
        ((12, 0, 0), True),
    ],
)
def test_active_stream_matches_free_trajectory_at_every_tick(momentum, generic, monkeypatch):
    settings = CausalStreamConfig(nx=257, ny=257, nz=257, c_units=12, source_per_octant=1, force_den=12)
    if generic:
        config = Config(nx=257, ny=257, nz=257, c_units=12, force_den=12)
        active = GenericFaceSimulation(config, definitions=(octant_definition(source_per_octant=1),))
        control = GenericFaceSimulation(config, definitions=(octant_definition(source_per_octant=0),))
    else:
        active = FaceStreamSimulation(settings)
        control = FaceStreamSimulation(replace(settings, source_per_octant=0))

    def has_field(world):
        if generic:
            zero = world.bank.definitions[0].zero_state
            return any(records[0].state != zero for records in world.bank.cells.values())
        return any(any(cell.populations) for cell in world.streams.cells.values())

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
        assert has_field(active)
        assert not has_field(control)
        if tick % 12 == 0:
            expected = tuple(origin[axis] + tick // 12 * momentum[axis] for axis in range(3))
            assert free.position == expected
