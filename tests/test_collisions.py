"""Independent conservation checks and numerical outcomes for massive local contacts."""

from fractions import Fraction
from itertools import product

import pytest

from event_universe import Config, LinkedSimulation
from event_universe import ScalarSimulation as Simulation
from event_universe.core.links import LinkConfig
from event_universe.core.state import MAX_CORE_INT, NodeState, ParticleState, validate_particle
from event_universe.diagnostics.frames import capture_volume
from event_universe.diagnostics.measurements import audit, total_momentum
from event_universe.diagnostics.recorder import TraceRecorder
from event_universe.diagnostics.render import _speed_arrow
from event_universe.dynamics.collision import CollisionBody, elastic_backscatter
from event_universe.dynamics.movement import advance_movement
from event_universe.dynamics.transit import transit_ticks
from event_universe.models.scalar_field import update_particle


def values(body):
    return tuple(Fraction(p, body.denominator) for p in body.momentum)


def invariants(bodies):
    momentum = tuple(sum(values(b)[axis] for b in bodies) for axis in range(3))
    energy = sum(sum(p * p for p in values(b)) / (2 * b.mass) for b in bodies)
    return momentum, energy


def bodies(world):
    return tuple(CollisionBody(p.momentum, p.mass, p.momentum_den) for p in world.particles.values())


@pytest.mark.parametrize(
    "first,second,expected",
    [
        (CollisionBody((3, 0, 0), 1), CollisionBody((-3, 0, 0), 1), ((-3, 0, 0), (3, 0, 0))),
        (CollisionBody((3, 0, 0), 1), CollisionBody((0, 0, 0), 2), ((-1, 0, 0), (4, 0, 0))),
        (
            CollisionBody((1, 0, 0), 1),
            CollisionBody((0, 0, 0), 2),
            ((Fraction(-1, 3), 0, 0), (Fraction(4, 3), 0, 0)),
        ),
        (CollisionBody((3, 2, -1), 1), CollisionBody((-3, -2, 1), 1), ((-3, -2, 1), (3, 2, -1))),
        (CollisionBody((3, 0, 0), 1), CollisionBody((0, 3, 0), 1), ((0, 3, 0), (3, 0, 0))),
    ],
)
def test_known_elastic_outcomes(first, second, expected):
    after = elastic_backscatter(first, second)
    assert tuple(values(b) for b in after) == expected
    assert invariants(after) == invariants((first, second))


def test_exact_conservation_reversibility_and_exchange_symmetry_over_unequal_masses():
    for m1, m2, a, b in product((1, 2, 7), (1, 3, 5), (-3, 0, 2), (-1, 1)):
        first = CollisionBody((a, 2, -1), m1, 3)
        second = CollisionBody((b, -3, 2), m2, 5)
        after = elastic_backscatter(first, second)
        assert invariants(after) == invariants((first, second))
        again = elastic_backscatter(*after)
        assert tuple(values(x) for x in again) == (values(first), values(second))
        reversed_order = elastic_backscatter(second, first)
        assert after.first == reversed_order.second and after.second == reversed_order.first


@pytest.mark.parametrize("mass", [0, -1, True, 1.5, MAX_CORE_INT + 1])
def test_invalid_mass_rejected_at_state_and_law_boundaries(mass):
    with pytest.raises((TypeError, ValueError, OverflowError)):
        validate_particle(ParticleState(0, 0, 0, mass=mass))
    with pytest.raises((TypeError, ValueError, OverflowError)):
        elastic_backscatter(CollisionBody((1, 0, 0), mass), CollisionBody((0, 0, 0), 2))


def test_fractional_mass_speed_keeps_credit_instead_of_rounding_to_rest():
    result = advance_movement((1, 0, 0), 0, 0, speed_cap=12, mass=2)
    assert (result.budget, result.budget_den) == (1, 2)
    for _ in range(23):
        result = advance_movement(
            (1, 0, 0), result.budget, result.phase, speed_cap=12, mass=2, budget_den=result.budget_den
        )
    assert result.direction == 0 and result.budget == 0
    assert transit_ticks(5, (1, 0, 0), 12, 2, 3) == 360
    assert transit_ticks(5, (MAX_CORE_INT, 0, 0), 12, 2, 1) == 5


def test_fractional_particle_field_impulse_changes_physical_momentum_by_one():
    p = ParticleState(1, 1, 1, px=1, momentum_den=3, mass=2)
    result = update_particle(
        p, NodeState(), (0, 0, 1, 0, 0, 0), Config(force_den=1, source_strength=0), 0
    )
    assert result.particle.momentum == (1, 3, 0)
    assert result.particle.momentum_den == 3
    assert result.node.py == -1
    assert result.particle.mass == 2


def test_same_node_reflects_once_and_separates_without_extra_hop():
    trace = TraceRecorder()
    world = Simulation(
        Config(nx=20, ny=8, nz=8, c_units=12, source_strength=0), observer=trace, collisions=True
    )
    world.add_particle(0, 4, 4, 4, 3)
    world.add_particle(1, 6, 4, 4, -3)
    initial = invariants(bodies(world))
    for tick in range(1, 13):
        before = {pid: p.position for pid, p in world.particles.items()}
        world.step()
        assert invariants(bodies(world)) == initial
        assert total_momentum(world) == (0, 0, 0)
        assert audit(world)["occupancy_consistent"]
        for pid, p in world.particles.items():
            assert sum(abs(a - b) for a, b in zip(p.position, before[pid], strict=True)) <= 1
        if tick == 4:
            assert world.particles[0].position == world.particles[1].position == (5, 4, 4)
            assert world.particles[0].px == -3 and world.particles[1].px == 3
        if tick == 8:
            assert (world.particles[0].x, world.particles[1].x) == (4, 6)
    assert len(trace.collision_records) == 1
    assert trace.collision_records[0].tick == 3
    assert not trace.collisions  # Legacy blocked-move events are separate.


def test_stationary_heavy_target_gets_exact_fractional_impulse():
    trace = TraceRecorder()
    world = Simulation(
        Config(nx=20, ny=8, nz=8, c_units=12, source_strength=0), observer=trace, collisions=True
    )
    world.add_particle(0, 4, 4, 4, 1, mass=1)
    world.add_particle(1, 5, 4, 4, mass=2)
    initial = invariants(bodies(world))
    for _ in range(31):
        world.step()
        assert invariants(bodies(world)) == initial
        assert total_momentum(world) == (1, 0, 0)
    assert len(trace.collision_records) == 1
    assert values(bodies(world)[0]) == (Fraction(-1, 3), 0, 0)
    assert values(bodies(world)[1]) == (Fraction(4, 3), 0, 0)
    assert world.particles[1].x > 5


def test_mass_changes_motion_and_visual_speed_at_fixed_momentum():
    world = Simulation(Config(nx=20, ny=8, nz=8, c_units=12, source_strength=0))
    world.add_particle(0, 4, 3, 4, 3)
    world.add_particle(1, 4, 5, 4, 3, mass=2)
    world.run(8)
    assert (world.particles[0].x, world.particles[1].x) == (6, 5)
    frame = capture_volume(world)
    assert frame.particle_scales == {0: (1, 1), 1: (2, 1)}
    assert _speed_arrow((3, 0, 0), 12, 2)[0] == _speed_arrow((3, 0, 0), 12)[0] / 2


def test_link_contacts_wait_for_arrival_and_never_reflect_in_flight():
    trace = TraceRecorder()
    world = LinkedSimulation(
        Config(nx=20, ny=8, nz=8, c_units=12, source_strength=0),
        links=LinkConfig(base_length=2, stretch_num=0),
        observer=trace,
        collisions=True,
    )
    world.add_particle(0, 4, 4, 4, 6)
    world.add_particle(1, 6, 4, 4, -6)
    for _ in range(4):
        world.step()
        assert not trace.collision_records
    world.step()
    assert len(trace.collision_records) == 1
    assert world.particles[0].position == world.particles[1].position == (5, 4, 4)
    assert world.particles[0].px == -6
    world.run(4)
    assert (world.particles[0].x, world.particles[1].x) == (4, 6)
    assert len(trace.collision_records) == 1


def test_periodic_colocation_and_new_encounter_after_separation():
    trace = TraceRecorder()
    world = Simulation(
        Config(nx=4, ny=4, nz=4, c_units=12, source_strength=0), observer=trace, collisions=True
    )
    world.add_particle(0, 3, 2, 2, 6)
    world.add_particle(1, 1, 2, 2, -6)
    world.run(6)
    assert len(trace.collision_records) == 2
    assert trace.collision_records[0].after_first.position == (0, 2, 2)
    assert trace.collision_records[1].after_first.position == (2, 2, 2)


def test_different_nodes_and_different_arrival_times_are_not_contacts():
    trace = TraceRecorder()
    world = Simulation(
        Config(nx=20, ny=8, nz=8, c_units=12, source_strength=0), observer=trace, collisions=True
    )
    world.add_particle(0, 4, 4, 4, 12)
    world.add_particle(1, 6, 4, 4, 12)
    world.run(4)
    assert not trace.collision_records


def test_overflow_rejects_both_collision_records_and_stops_world():
    world = Simulation(Config(nx=8, ny=8, nz=8, source_strength=0), collisions=True)
    world.add_particle(0, 4, 4, 4, MAX_CORE_INT, mass=1)
    world.add_particle(1, 4, 4, 4, mass=2)
    before = dict(world.particles)
    with pytest.raises(OverflowError):
        world.step()
    assert world.faulted and dict(world.particles) == before
    with pytest.raises(RuntimeError):
        world.step()


def test_fixed_capacity_multi_contact_is_deterministic_and_conservative():
    trace = TraceRecorder()
    world = Simulation(
        Config(nx=12, ny=8, nz=8, c_units=1000, source_strength=0), collisions=True, observer=trace
    )
    for pid, momentum in enumerate((3, -3, 2, -2)):
        world.add_particle(pid, 4, 4, 4, momentum)
    initial = invariants(bodies(world))
    for _ in range(3):
        world.step()
        assert invariants(bodies(world)) == initial
        assert len(world._contacts[(4, 4, 4)]) == 16
        events = [e for e in trace.collision_records if e.tick == world.tick - 1]
        involved = [pid for e in events for pid in (e.first_pid, e.second_pid)]
        assert len(involved) == len(set(involved))


def test_periodic_self_loop_preserves_contact_identity():
    trace = TraceRecorder()
    world = Simulation(
        Config(nx=1, ny=1, nz=1, c_units=1, source_strength=0), collisions=True, observer=trace
    )
    world.add_particle(0, 0, 0, 0, 3)
    world.add_particle(1, 0, 0, 0, -3)
    world.run(4)
    assert len(trace.collision_records) == 1
    assert world.occupancy[(0, 0, 0)] == (0, 1, -1, -1)
    assert world.particles[0].px == -3


def test_collision_callable_can_be_replaced_without_world_access():
    from event_universe.core.scalar_engine import ScalarEngine
    from event_universe.models.scalar_field import SCALAR_MODEL

    def transparent_contact(first, second):
        return first, second

    world = ScalarEngine(
        Config(nx=8, ny=8, nz=8, source_strength=0),
        SCALAR_MODEL.update_field,
        SCALAR_MODEL.update_particle,
        collision_rule=transparent_contact,
        field_activity=SCALAR_MODEL.field_is_active,
    )
    world.add_particle(0, 4, 4, 4, 3)
    world.add_particle(1, 4, 4, 4, -3)
    world.step()
    assert world.particles[0].px == 3 and world.particles[1].px == -3
    assert all(p.last_collision_tick == 0 for p in world.particles.values())


def test_mass_and_collisions_compose_with_balanced_motion_and_halo():
    from event_universe.particle_api import BalancedSimulation

    trace = TraceRecorder()
    world = BalancedSimulation(
        Config(nx=24, ny=24, nz=24, c_units=12, source_strength=0),
        collisions=True,
        observer=trace,
    )
    world.add_particle(0, 12, 12, 12, 3, 2, 1, mass=1)
    world.add_particle(1, 12, 12, 12, -3, -2, -1, mass=2)
    initial = invariants(bodies(world))
    for _ in range(12):
        world.step()
        assert invariants(bodies(world)) == initial
        assert audit(world)["occupancy_consistent"]
    assert len(trace.collision_records) == 1
    assert world.particles[0].position != world.particles[1].position
    assert world.particles[0].momentum == (-3, -2, -1)
    assert world.particles[1].mass == 2
