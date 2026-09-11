"""Whole-tick causal acceptance, including transport, response and movement."""

from event_universe import CausalStreamConfig
from event_universe.api import FaceStreamSimulation


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
