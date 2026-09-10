"""Alternative laws here are test fixtures, not new production physics."""

import pytest

from event_universe import Config, Simulation
from event_universe.core.state import Neighbors
from event_universe.diagnostics.measurements import audit, total_momentum
from event_universe.dynamics import FieldTurning
from event_universe.dynamics.turning import full_response
from event_universe.fields import ScalarField, ScalarSample


class SourceOnlyField:
    """A distinct local law to exercise the public field protocol."""

    def advance(
        self, sample: ScalarSample, neighbors: Neighbors, *, source: int, denominator: int
    ) -> ScalarSample:
        return ScalarSample(source, 0)


def test_another_scalar_law_runs_through_the_same_simulation_engine():
    config = Config(nx=8, ny=8, nz=8)
    current, alternative = Simulation(config), Simulation(config, field=SourceOnlyField())
    for world in (current, alternative):
        world.add_particle(0, 4, 4, 4)
        world.run(2)
        assert world.particles[0].momentum == (0, 0, 0)
        assert audit(world)["occupancy_consistent"]
    assert current.phi((4, 4, 4)) == 9
    assert current.phi((5, 4, 4)) == 1
    assert alternative.phi((4, 4, 4)) == 64
    assert alternative.phi((5, 4, 4)) == 0


def test_field_and_turning_are_independently_replaceable():
    config = Config(nx=8, ny=8, nz=8)
    transverse = Simulation(config, field=SourceOnlyField())
    full = Simulation(
        config, field=SourceOnlyField(), turning=FieldTurning(select_direction=full_response)
    )
    for world in (transverse, full):
        world.add_particle(0, 4, 4, 4, 3)
        world.add_particle(1, 5, 4, 4)
        world.step()
        assert world.phi((4, 4, 4)) == 64
        assert world.phi((5, 4, 4)) == 64
        assert total_momentum(world) == (3, 0, 0)
        assert audit(world)["occupancy_consistent"]
    assert transverse.particles[0].momentum == (3, 0, 0)
    assert full.particles[0].momentum == (4, 0, 0)
    assert transverse.cells[(4, 4, 4)].px == 0
    assert full.cells[(4, 4, 4)].px == -1


def test_invalid_custom_field_result_is_rejected_before_commit():
    class InvalidRemainderField(SourceOnlyField):
        def advance(self, sample, neighbors, *, source, denominator):
            return ScalarSample(1, denominator)

    world = Simulation(Config(nx=8, ny=8, nz=8), field=InvalidRemainderField())
    world.add_particle(0, 4, 4, 4)
    with pytest.raises(ValueError, match="invalid remainder"):
        world.step()
    assert not world.cells and world.tick == 0 and world.faulted


def test_custom_field_continues_remainder_only_evolution_until_value_changes():
    world = Simulation(
        Config(nx=8, ny=8, nz=8, field_den=7, source_strength=0),
        field=ScalarField(neighbor_weights=(0, 0, 0, 0, 0, 0), self_weight=8),
    )
    origin = (4, 4, 4)
    world.seed_field(origin, 1)
    samples = []
    for _ in range(7):
        world.step()
        cell = world.cells[origin]
        samples.append(ScalarSample(cell.phi, cell.remainder))
    assert samples == [
        ScalarSample(1, 1),
        ScalarSample(1, 2),
        ScalarSample(1, 3),
        ScalarSample(1, 4),
        ScalarSample(1, 5),
        ScalarSample(1, 6),
        ScalarSample(2, 0),
    ]


def test_activity_policy_is_replaceable_and_an_invalid_decision_cannot_commit():
    world = Simulation(Config(nx=8, ny=8, nz=8), field_activity=lambda previous, current, sources: 1)
    world.add_particle(0, 4, 4, 4)
    with pytest.raises(TypeError, match="must return bool"):
        world.step()
    assert not world.cells and world.tick == 0 and world.faulted
