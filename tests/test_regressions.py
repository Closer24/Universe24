import pytest

from event_universe import Config
from event_universe import ScalarSimulation as Simulation
from event_universe.diagnostics.frames import Slice
from event_universe.diagnostics.measurements import audit, total_momentum
from event_universe.diagnostics.recorder import TraceRecorder
from event_universe.particle_scenarios import get_scenario


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
    assert audit(world)["valid_remainders"]


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


def test_contact_response_is_prompt_and_reflection_symmetric():
    scenario = get_scenario("contact")
    trace = TraceRecorder()
    original, reflected = scenario.create(trace), Simulation(scenario.config)
    for pid, x, y, z, px, py, pz in scenario.particles:
        reflected.add_particle(pid, 63 - x, 47 - y, z, -px, -py, pz)
    contact_tick, turn_tick = None, None
    for _ in range(24):
        previous = len(trace.force_records)
        before = tuple(p.py for p in original.particles.values())
        original.step()
        reflected.step()
        if contact_tick is None and any(event.gy for event in trace.force_records[previous:]):
            contact_tick = original.tick
        if turn_tick is None and before != tuple(p.py for p in original.particles.values()):
            turn_tick = original.tick
        assert total_momentum(original) == total_momentum(reflected) == (0, 0, 0)
        for pid, old in original.particles.items():
            new = reflected.particles[pid]
            assert new.position == (63 - old.x, 47 - old.y, old.z)
            assert new.momentum == (-old.px, -old.py, old.pz)
    assert contact_tick is not None and turn_tick == contact_tick
    assert audit(original)["valid_remainders"] and audit(reflected)["valid_remainders"]
