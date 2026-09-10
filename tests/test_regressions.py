from dataclasses import asdict

import pytest

from event_universe import Config, Simulation
from event_universe.diagnostics.frames import Slice
from event_universe.diagnostics.measurements import audit, total_momentum
from event_universe.diagnostics.recorder import TraceRecorder
from event_universe.scenarios import get_scenario


@pytest.mark.parametrize("name", ["stationary", "contact", "turning"])
def test_full_state_matches_frozen_legacy_after_every_tick(name, legacy, reference_sha256):
    assert reference_sha256 == "822f62ac790c0b8477ed634d24454774152bcba8fb3322a53d039c251376163f"
    scenario = get_scenario(name)
    trace = TraceRecorder()
    current = scenario.create(trace)
    reference = legacy.IntegerO1Field3D(legacy.Config(**asdict(scenario.config)))
    for seed in scenario.particles:
        reference.add_particle(*seed)
    for _ in range(scenario.ticks):
        current.step()
        reference.step()
        assert current.tick == reference.tick
        assert dict(current.cells) == {key: tuple(value) for key, value in reference.cells.items()}
        assert dict(current.particles) == {
            key: tuple(value) for key, value in reference.particles.items()
        }
        assert dict(current.occupancy) == {
            key: tuple(value) for key, value in reference.occupancy.items()
        }
        assert current.active == reference.active
        assert trace.force_records == reference.force_records
        assert trace.paths == reference.paths
        assert trace.collisions == reference.collisions
        assert total_momentum(current) == reference.total_momentum()
    assert audit(current)["valid_remainders"]


@pytest.mark.parametrize("plane", ["XY", "XZ", "YZ"])
def test_offset_pair_turns_in_all_three_coordinate_planes(plane):
    # Keep the original order of the two nonzero digital axes in each embedding.
    permutations = {"XY": (0, 1, 2), "XZ": (0, 2, 1), "YZ": (2, 0, 1)}
    order = permutations[plane]
    shape = tuple((128, 96, 32)[axis] for axis in order)
    world = Simulation(Config(nx=shape[0], ny=shape[1], nz=shape[2], c_units=12, force_den=12))
    world.diagnostic_view = Slice(plane, 16)
    for pid, position, momentum in [(0, (44, 47, 16), (3, 0, 0)), (1, (84, 49, 16), (-3, 0, 0))]:
        world.add_particle(pid, *(position[i] for i in order), *(momentum[i] for i in order))
    for _ in range(110):
        world.step()
        assert total_momentum(world) == (0, 0, 0)
    first, second = world.particles[0], world.particles[1]
    transverse = order.index(1)
    fixed = order.index(2)
    assert first.momentum[transverse] > 0 and second.momentum[transverse] < 0
    assert first.momentum == tuple(-value for value in second.momentum)
    assert first.position[fixed] == second.position[fixed] == 16


def test_first_transverse_contact_changes_momentum_on_same_tick_at_unit_coupling():
    trace = TraceRecorder()
    world = get_scenario("contact").create(trace)
    contact_tick, turn_tick = None, None
    for _ in range(24):
        previous = len(trace.force_records)
        before = world.particles[0].py, world.particles[1].py
        world.step()
        if contact_tick is None and any(event.gy for event in trace.force_records[previous:]):
            contact_tick = world.tick
        if turn_tick is None and before != (world.particles[0].py, world.particles[1].py):
            turn_tick = world.tick
        assert total_momentum(world) == (0, 0, 0)
    assert contact_tick is not None and turn_tick == contact_tick


def test_isolated_cardinal_mover_has_no_self_drag():
    trace = TraceRecorder()
    world = Simulation(Config(nx=64, ny=64, nz=32, c_units=12, force_den=12), observer=trace)
    world.add_particle(9, 20, 20, 16, 3)
    world.run(100)
    assert world.particles[9].momentum == (3, 0, 0)
    assert all((event.ix, event.iy, event.iz) == (0, 0, 0) for event in trace.force_records)


def test_original_180_tick_two_particle_regression():
    trace = TraceRecorder()
    world = Simulation(Config(nx=64, ny=64, nz=32, c_units=12, force_den=12), observer=trace)
    world.add_particle(0, 22, 31, 16, 3)
    world.add_particle(1, 42, 33, 16, -3)
    world.run(180)
    assert any(event.ix or event.iy or event.iz for event in trace.force_records)
    assert world.particles[0].momentum == tuple(-value for value in world.particles[1].momentum)
    assert world.particles[0].z == world.particles[1].z == 16
    assert total_momentum(world) == (0, 0, 0)


def test_reflection_of_contact_experiment_reflects_result():
    scenario = get_scenario("contact")
    original, reflected = scenario.create(), Simulation(scenario.config)
    for pid, x, y, z, px, py, pz in scenario.particles:
        reflected.add_particle(pid, 63 - x, 47 - y, z, -px, -py, pz)
    for _ in range(24):
        original.step()
        reflected.step()
        for pid, old in original.particles.items():
            new = reflected.particles[pid]
            assert new.position == (63 - old.x, 47 - old.y, old.z)
            assert new.momentum == (-old.px, -old.py, old.pz)
