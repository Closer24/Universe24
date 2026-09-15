"""Transport visits occupied banks without changing public inventory or order."""

from event_universe import Simulation
from event_universe.core.disturbance_state import Packet
from event_universe.core.node_ports import PortTable
from event_universe.initialization import parse_initial_state

from .test_local_focus import moving_document


def test_reactivation_preserves_bank_creation_order_and_empty_mapping_entries():
    initial = parse_initial_state(moving_document())
    record = initial.seeds[0].record
    table = PortTable((None,))
    first, second = (2, 2, 2), (1, 1, 1)
    table[first] = (Packet(3, first, 0, record),)
    table[second] = (Packet(3, second, 0, record),)
    table[first] = (None,)
    assert list(table) == [first, second]
    assert [position for position, _ in table.active_items()] == [second]
    table[first] = (Packet(4, first, 0, record),)
    assert [position for position, _ in table.active_items()] == [first, second]
    # Releasing banks during delivery must not invalidate the selected batch.
    for position, _ in table.active_items():
        table[position] = (None,)
    assert list(table.active_items()) == []
    assert len(table) == 2 and table[first] == (None,)
    del table[first]
    assert list(table) == [second]


def test_empty_history_and_future_packets_do_not_change_transport_timing():
    raw = moving_document(travel=3)
    raw.update(boundary="open", focus=True)
    world = Simulation(parse_initial_state(raw))
    for _ in range(30):
        world.step()
    assert world._links.execution_report()["active_banks"] == 0
    assert len(world._links) > 0

    class NoHistoryScan(dict):
        def items(self):
            raise AssertionError("transport scanned inactive bank history")

        def values(self):
            raise AssertionError("transport scanned inactive bank history")

        def __iter__(self):
            raise AssertionError("transport scanned inactive bank history")

    world._links._banks = NoHistoryScan(world._links._banks)
    for _ in range(3):
        world.step()
    assert world._links.execution_report()["active_banks"] == 0
