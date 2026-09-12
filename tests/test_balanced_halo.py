"""Acceptance tests for the synchronous old/new six-neighbor scalar halo."""

import pytest

from event_universe.core.state import Config
from event_universe.diagnostics.measurements import total_momentum
from event_universe.dynamics.movement import advance_balanced_movement
from event_universe.particle_api import BalancedSimulation
from event_universe.particle_api import ScalarSimulation as Simulation
from event_universe.particle_scenarios import get_scenario


@pytest.mark.parametrize(
    "momentum",
    [(1, 1, 0), (6, 4, 0), (3, 2, 1), (1, 2, 3), (11, 1, 0), (-3, 2, -1)],
)
def test_isolated_moving_source_keeps_momentum_for_200_ticks(momentum):
    world = BalancedSimulation(
        Config(nx=160, ny=160, nz=64, c_units=12, source_strength=64, force_den=1)
    )
    world.add_particle(0, 80, 80, 32, *momentum)
    initial_total = total_momentum(world)
    for _ in range(200):
        world.step()
        assert world.particles[0].momentum == momentum
        assert total_momentum(world) == initial_total


def test_old_and_new_six_neighbor_halos_are_quiescent_after_a_move():
    world = BalancedSimulation(Config(nx=32, ny=32, nz=16, c_units=12, source_strength=64, force_den=1))
    origin = (10, 10, 8)
    world.add_particle(0, *origin, 12, 0, 0)
    world.step()
    current = world.particles[0].position
    assert current != origin
    targets = {*world._lattice.neighbors(origin), *world._lattice.neighbors(current)}
    assert len(targets) <= 12
    assert all(world.cell_at(address).phi == 0 for address in targets)
    assert all(world.cell_at(address).remainder == 0 for address in targets)


def test_external_seed_still_changes_particle_momentum():
    world = BalancedSimulation(
        Config(nx=32, ny=32, nz=16, c_units=12, source_strength=0, field_den=7, force_den=1)
    )
    world.seed_field((17, 16, 8), 1000)
    world.add_particle(0, 16, 16, 8)
    world.run(2)
    assert world.particles[0].momentum == (101, 0, 0)


def test_two_sources_retain_equal_opposite_transverse_response():
    scenario = get_scenario("contact")
    world = BalancedSimulation(scenario.config)
    for seed in scenario.particles:
        world.add_particle(*seed)
    initial_total = total_momentum(world)
    world.run(18)
    assert world.particles[0].momentum == (3, 1, 0)
    assert world.particles[1].momentum == (-3, -1, 0)
    assert total_momentum(world) == initial_total


def test_baseline_simulation_does_not_apply_the_candidate_halo():
    config = Config(nx=32, ny=32, nz=16, c_units=12, source_strength=64, force_den=1)
    baseline = Simulation(config, movement=advance_balanced_movement)
    candidate = BalancedSimulation(config)
    for world in (baseline, candidate):
        world.add_particle(0, 16, 16, 8, 1, 1, 0)
        world.run(8)
    assert baseline.particles[0].momentum == (1, -1, 0)
    assert candidate.particles[0].momentum == (1, 1, 0)
