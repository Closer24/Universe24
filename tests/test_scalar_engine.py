import pytest

from event_universe import Config
from event_universe import ScalarSimulation as Simulation
from event_universe.core.state import DIRECTIONS, MAX_CORE_INT, ZERO_CELL
from event_universe.diagnostics.frames import Slice, capture_frame
from event_universe.diagnostics.measurements import audit, total_momentum
from event_universe.diagnostics.recorder import TraceRecorder


def test_stationary_source_persists_with_no_self_force():
    world = Simulation(Config(nx=48, ny=48, nz=48))
    world.add_particle(0, 24, 24, 24)
    world.run(60)
    center = world.phi((24, 24, 24))
    world.run(60)
    assert abs(world.phi((24, 24, 24)) - center) <= 1
    assert center > 0
    assert len({world.phi((24 + x, 24 + y, 24 + z)) for x, y, z in DIRECTIONS}) == 1
    assert world.particles[0].momentum == (0, 0, 0)
    assert audit(world)["occupancy_consistent"]


def test_field_change_cannot_cross_more_than_one_edge_per_tick():
    world = Simulation(Config(nx=21, ny=21, nz=21))
    origin = (10, 10, 10)
    world.seed_field(origin, 117649)
    for tick in range(1, 6):
        world.step()
        assert all(
            sum(abs(p[i] - origin[i]) for i in range(3)) <= tick
            for p, cell in world.cells.items()
            if cell.phi
        )
        assert world.phi((10 + tick, 10, 10)) > 0


@pytest.mark.parametrize("speed", [0, 1, 3, 12, 120])
def test_one_speed_law_and_at_most_one_hop_per_tick(speed):
    world = Simulation(Config(nx=64, ny=8, nz=8, c_units=12, source_strength=0))
    world.add_particle(0, 4, 4, 4, speed)
    for tick in range(1, 25):
        previous = world.particles[0].x
        world.step()
        assert world.particles[0].x - previous in (0, 1)
        assert world.particles[0].x == 4 + tick * min(speed, 12) // 12


def test_particle_entering_later_occupied_cell_updates_only_once():
    trace = TraceRecorder()
    world = Simulation(Config(nx=16, ny=8, nz=8, c_units=1, source_strength=0), observer=trace)
    world.add_particle(0, 2, 4, 4, 1)
    world.add_particle(1, 3, 4, 4, 0)
    world.step()
    assert world.particles[0].x == 3
    assert [(r.tick, r.pid) for r in trace.force_records] == [(0, 0), (0, 1)]


def test_full_cell_blocks_without_growing_slots_or_dropping_particle():
    trace = TraceRecorder()
    world = Simulation(
        Config(nx=16, ny=8, nz=8, c_units=1, source_strength=0, max_particles_per_cell=1), observer=trace
    )
    world.add_particle(0, 2, 4, 4, 1)
    world.add_particle(1, 3, 4, 4)
    world.step()
    assert world.particles[0].position == (2, 4, 4)
    assert len(trace.collisions) == 1
    assert all(len(slots) == 1 for slots in world.occupancy.values())
    assert world.particles[0].move_budget == 0
    assert audit(world)["occupancy_consistent"]


def test_periodic_boundary():
    world = Simulation(Config(nx=8, ny=8, nz=8, c_units=1, source_strength=0))
    world.add_particle(0, 7, 4, 4, 1)
    world.step()
    assert world.particles[0].position == (0, 4, 4)
    assert audit(world)["occupancy_consistent"]


def test_single_cell_dimension_keeps_exactly_one_occupancy_entry():
    world = Simulation(Config(nx=1, ny=8, nz=8, c_units=1, source_strength=0))
    world.add_particle(0, 0, 4, 4, 1)
    world.run(4)
    assert sum(slot == 0 for slots in world.occupancy.values() for slot in slots) == 1
    assert audit(world)["occupancy_consistent"]


def test_state_views_and_diagnostic_copies_cannot_modify_physics():
    world = Simulation(Config(nx=8, ny=8, nz=8))
    world.add_particle(0, 4, 4, 4)
    world.step()
    before = dict(world.cells)
    with pytest.raises(TypeError):
        world.cells[(4, 4, 4)] = ZERO_CELL
    with pytest.raises(AttributeError):
        world.particles[0].px = 10
    frame = capture_frame(world, Slice("XY", 4))
    frame.field.clear()
    frame.particles.clear()
    assert dict(world.cells) == before


def test_seed_api_cannot_rewrite_evolving_field():
    world = Simulation(Config(nx=8, ny=8, nz=8))
    world.step()
    with pytest.raises(RuntimeError):
        world.seed_field((4, 4, 4), 99)


def test_field_overflow_is_terminal_and_field_commit_is_atomic():
    world = Simulation(
        Config(nx=8, ny=8, nz=8, source_strength=MAX_CORE_INT, field_den=1, max_particles_per_cell=2)
    )
    world.add_particle(0, 4, 4, 4)
    world.add_particle(1, 4, 4, 4)
    with pytest.raises(OverflowError):
        world.step()
    assert not world.cells and world.tick == 0 and world.faulted
    with pytest.raises(RuntimeError):
        world.step()


def test_recording_and_measurements_do_not_change_any_physical_state():
    config = Config(nx=32, ny=24, nz=16, c_units=12, force_den=1)
    plain, observed = Simulation(config), Simulation(config, observer=TraceRecorder())
    for world in (plain, observed):
        world.add_particle(0, 12, 11, 8, 3)
        world.add_particle(1, 20, 13, 8, -3)
    for _ in range(24):
        plain.step()
        observed.step()
        capture_frame(observed, Slice("XY", 8))
        audit(observed)
        assert plain.cells == observed.cells
        assert plain.particles == observed.particles
        assert plain.occupancy == observed.occupancy
        assert plain.active == observed.active
        assert total_momentum(plain) == (0, 0, 0)
