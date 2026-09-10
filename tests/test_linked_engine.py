"""Candidate behavior and causal boundary; original v10 expectations are untouched."""

from event_universe.api import LinkedSimulation
from event_universe.core.links import LinkConfig
from event_universe.core.state import Config
from event_universe.diagnostics.measurements import audit, total_momentum


def small(**changes):
    return Config(nx=11, ny=11, nz=11, c_units=12, **changes)


def test_actual_c_transit_and_rest_with_fixed_local_state():
    w = LinkedSimulation(small(source_strength=0, force_num=0), links=LinkConfig(5))
    w.add_particle(0, 3, 3, 3, 12, 0, 0)
    w.add_particle(1, 5, 5, 5)
    w.run(5)
    assert w.particles[0].position == (3, 3, 3)
    assert w.transits[0].due == 5 and w.transits[0].length == 5
    w.step()
    assert w.particles[0].position == (4, 3, 3)
    assert w.transits[0].due == 10
    assert w.particles[1].position == (5, 5, 5) and 1 not in w.transits
    w.links.validate()
    audit(w)


def test_far_change_cannot_affect_local_cell_before_two_edge_deliveries():
    a = LinkedSimulation(small(force_num=0), links=LinkConfig(3, 0))
    b = LinkedSimulation(small(force_num=0), links=LinkConfig(3, 0))
    b.seed_field((6, 4, 4), 100)
    target = (4, 4, 4)
    for _ in range(6):
        a.step()
        b.step()
        assert a.cell_at(target) == b.cell_at(target)
        assert a.links.at(target) == b.links.at(target)
    a.step()
    b.step()
    assert a.cell_at(target).phi == 0 < b.cell_at(target).phi


def test_no_direct_remote_scalar_reads_and_all_versions_agree():
    w = LinkedSimulation(small(), links=LinkConfig(3))
    w.add_particle(0, 5, 5, 5, 3, 0, 0)

    def forbidden_remote_read(*args):
        raise AssertionError("direct remote scalar read instead of delivered mailbox")

    w.phi = forbidden_remote_read
    for _ in range(25):
        w.step()
        w.links.validate()
        assert all(t.due - t.departure >= t.length for t in w.transits.values())
    audit(w)


def test_transit_length_is_frozen_while_geometry_changes():
    w = LinkedSimulation(small(force_num=0), links=LinkConfig(3))
    w.add_particle(0, 4, 4, 4, 1, 0, 0)
    w.step()
    locked = w.transits[0]
    assert locked.length == 3 and locked.due == 36
    w.run(12)
    assert w.links.at((4, 4, 4)).lengths[0] > 3
    assert w.transits[0] == locked


def test_three_particle_local_exchange_total_momentum_and_capacity():
    w = LinkedSimulation(small(force_den=1), links=LinkConfig(3))
    w.add_particle(0, 3, 4, 5, 6, 0, 0)
    w.add_particle(1, 7, 6, 5, -6, 0, 0)
    w.add_particle(2, 5, 8, 5, 0, -3, 0)
    initial = total_momentum(w)
    for _ in range(50):
        w.step()
        assert total_momentum(w) == initial
        w.links.validate()
        audit(w)


def test_stationary_source_symmetric_and_zero_self_force():
    w = LinkedSimulation(small(force_den=1), links=LinkConfig(3))
    w.add_particle(0, 5, 5, 5)
    for _ in range(80):
        w.step()
        assert w.particles[0].momentum == (0, 0, 0)
        sides = w._lattice.sample((5, 5, 5), w.phi)
        assert sides[0] == sides[1] == sides[2] == sides[3] == sides[4] == sides[5]
