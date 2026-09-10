"""Mandatory inertial-motion gate: an isolated particle cannot deflect itself.

The source-free control uses the same scheduler and digital movement law. The
self-field world must match its trajectory at every tick, not just at the end.
This is an acceptance requirement, not an expected failure or an optional test.
"""

from dataclasses import replace

import pytest

from event_universe import Config, Simulation
from event_universe.api import LinkedSimulation
from event_universe.core.links import LinkConfig


@pytest.mark.parametrize("model", ["baseline", "linked"])
@pytest.mark.parametrize(
    "momentum",
    [
        (1, 0, 0),
        (3, 0, 0),
        (12, 0, 0),
        (0, -3, 0),
        (0, 0, 12),
        (1, 1, 0),
        (3, -2, 1),
        (6, 4, -2),
    ],
    ids=["slow-x", "medium-x", "max-x", "negative-y", "max-z", "slow-xy", "diagonal-xyz", "max-xyz"],
)
def test_isolated_particle_keeps_momentum_and_free_trajectory(model, momentum):
    config = Config(nx=257, ny=257, nz=257, c_units=12, source_strength=64, force_den=12)
    control_config = replace(config, source_strength=0)
    if model == "baseline":
        own_field = Simulation(config)
        control = Simulation(control_config)
    else:
        # Fix geometry to isolate self-response from changing transit lengths.
        links = LinkConfig(base_length=1, stretch_num=0)
        own_field = LinkedSimulation(config, links=links)
        control = LinkedSimulation(control_config, links=links)
    origin = (128, 128, 128)
    for world in (own_field, control):
        world.add_particle(0, *origin, *momentum)
    field_was_nonzero = False
    for tick in range(1, 73):
        own_field.step()
        control.step()
        actual = own_field.particles[0]
        free = control.particles[0]
        field_was_nonzero |= any(cell.phi for cell in own_field.cells.values())
        assert free.momentum == momentum, (model, tick, "source-free momentum changed")
        assert actual.momentum == momentum, (
            model,
            tick,
            "self-field changed isolated momentum",
            momentum,
            actual.momentum,
        )
        assert actual.position == free.position, (
            model,
            tick,
            "self-field changed the free trajectory",
            free.position,
            actual.position,
        )
        assert not any(cell.phi for cell in control.cells.values())
        if model == "baseline" and tick % 12 == 0:
            # Independent full-cycle displacement for these unsaturated inputs.
            expected = tuple(origin[axis] + (tick // 12) * momentum[axis] for axis in range(3))
            assert free.position == expected, (tick, expected, free.position)
    assert field_was_nonzero, "The test must exercise an actual self-field"
