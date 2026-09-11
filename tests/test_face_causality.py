"""Whole-tick causal acceptance, including transport, response and movement."""

from event_universe import CausalStreamConfig
from event_universe.api import FaceStreamSimulation
from event_universe.core.state import EMPTY_SLOT


def test_source_intervention_cannot_ride_particle_two_edges_in_one_tick():
    settings = CausalStreamConfig(nx=16, ny=16, nz=16, c_units=1, source_per_octant=1, force_den=1)
    active, control = FaceStreamSimulation(settings), FaceStreamSimulation(settings)
    for world in (active, control):
        world.add_particle(0, 6, 5, 5, 100, 0, 0)
    active.add_particle(1, 5, 5, 5)
    for world in (active, control):
        world.step()
    target = (7, 5, 5)
    # The initial intervention is two edges from target, so every local target
    # record must still agree after one elementary tick, including arriving matter.
    active_target = tuple(p for p in active.particles.values() if p.position == target)
    control_target = tuple(p for p in control.particles.values() if p.position == target)
    assert active_target == control_target
    assert active.cell_at(target) == control.cell_at(target)


def test_competing_request_cannot_change_remote_sender_in_same_tick():
    settings = CausalStreamConfig(
        nx=16, ny=16, nz=16, c_units=1, source_per_octant=0, force_num=0, max_particles_per_cell=1
    )
    active, control = FaceStreamSimulation(settings), FaceStreamSimulation(settings)
    active.add_particle(1, 6, 5, 5, -1, 0, 0)
    for world in (active, control):
        world.add_particle(0, 4, 5, 5, 1, 0, 0)
        world.step()
    # A competitor at (6,5,5) is outside the one-tick cone of sender (4,5,5).
    # Its same-tick request must not decide whether that sender has departed.
    origin = (4, 5, 5)
    assert active.occupancy.get(origin) == control.occupancy.get(origin)

    # The source-owned reservation is local state too. Receiver arbitration may
    # not release it before the return acknowledgement crosses its link.
    assert active.matter_transport is not None
    assert control.matter_transport is not None
    assert active.matter_transport.busy[origin] == control.matter_transport.busy[origin]
    assert active.particles[0].momentum == control.particles[0].momentum == (1, 0, 0)

    def assert_owned_once(world, expected_ids):
        transport = world.matter_transport
        assert transport is not None
        residents = [pid for slots in world.occupancy.values() for pid in slots if pid != EMPTY_SLOT]
        owners = residents + list(transport.packets)
        assert sorted(owners) == sorted(expected_ids)
        assert set(world.particles) == set(expected_ids)
        assert sum(world.particles[pid].mass for pid in owners) == len(expected_ids)
        assert all(sum(pid != EMPTY_SLOT for pid in slots) <= 1 for slots in world.occupancy.values())
        assert all(len(slots) == 6 for slots in transport.busy.values())

    for tick in range(1, 7):
        assert_owned_once(active, (0, 1))
        assert_owned_once(control, (0,))
        # Uncontended motion retains one hop per tick, including successive
        # departures while previous link acknowledgements are still in flight.
        assert control.particles[0].position == (4 + tick, 5, 5)
        if tick < 6:
            active.step()
            control.step()
