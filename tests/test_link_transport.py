"""Pure transport tests: no world, no rendering, only fixed local records."""

from event_universe.core.lattice import PeriodicLattice
from event_universe.core.links import LINK_REGISTERS, LinkConfig, LinkTransport
from event_universe.fields.geometry import MeanStretch


def network(base=3):
    return LinkTransport(PeriodicLattice((7, 7, 7)), LinkConfig(base), MeanStretch(base, 1, 1))


def test_single_owner_including_periodic_seams_and_all_axes():
    net = network()
    for p in ((0, 0, 0), (6, 6, 6), (3, 2, 1)):
        for d in range(6):
            other = net.lattice.neighbor(p, d)
            assert net.owner(p, d) == net.owner(other, d ^ 1)
            assert net.owner(p, d)[1] in (0, 2, 4)


def test_announcement_uses_old_length_and_activates_both_ends_only_on_arrival():
    net = network(100)
    p, q = (3, 3, 3), (4, 3, 3)
    net.publish(p, 20)  # proposed length 110, transit on existing length 100
    assert net.at(p).outgoing[0].remaining == 100
    for _ in range(99):
        net.advance()
        assert net.at(p).lengths[0] == net.at(q).lengths[1] == 100
        assert net.at(q).received[1] == 0
    net.advance()
    assert net.at(q).received[1] == 20
    assert net.at(p).lengths[0] == net.at(q).lengths[1] == 110
    net.publish(p, 22)
    assert net.at(p).outgoing[0].remaining == 110
    net.validate()


def test_busy_channel_has_one_snapshot_not_a_growing_queue_and_zero_is_delivered():
    net = network()
    p, q = (3, 3, 3), (4, 3, 3)
    net.publish(p, 20)
    for value in range(21, 200):
        net.publish(p, value)
        assert net.at(p).outgoing[0].value == 20
    for _ in range(3):
        net.advance()
    net.publish(p, 0)
    for _ in range(13):  # active length = 3 + (20 + 0)//2
        net.advance()
    assert net.at(q).received[1] == 0
    net.validate()
    cell = net.at(p)
    assert len(cell.received) + len(cell.lengths) + sum(len(p) for p in cell.outgoing) == LINK_REGISTERS


def test_multiple_deliveries_and_owner_updates_are_iteration_order_independent():
    a, b = network(), network()
    seeds = [((3, 3, 3), 20), ((4, 3, 3), 12), ((3, 4, 3), 8), ((3, 3, 4), 6)]
    for p, value in seeds:
        a.publish(p, value)
    for p, value in reversed(seeds):
        b.publish(p, value)
    for _ in range(3):
        a.advance()
        b.advance()
        assert a.cells == b.cells
        a.validate()
        b.validate()


def test_two_simultaneous_proposals_merge_symmetrically_and_can_be_replaced():
    for policy, expected in ((max, 13), (min, 7)):
        net = LinkTransport(PeriodicLattice((7, 7, 7)), LinkConfig(3), MeanStretch(3, 1, 1), policy)
        net.publish((3, 3, 3), 20)
        net.publish((4, 3, 3), 8)
        for _ in range(3):
            net.advance()
        assert net.at((3, 3, 3)).lengths[0] == expected
        assert net.at((4, 3, 3)).lengths[1] == expected
        net.validate()
