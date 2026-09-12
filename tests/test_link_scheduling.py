"""Arrival indexing preserves ordered ownership, failures and dormant history."""

from dataclasses import replace

import pytest

from event_universe import Simulation
from event_universe.core.disturbance_engine import DisturbanceEngine
from event_universe.core.disturbance_state import Packet, pack
from event_universe.core.event_space import CausalEventSpace
from event_universe.core.link_schedule import LinkSchedule
from event_universe.initialization import parse_initial_state
from tests.test_disturbance_engine import document, kind, resident_values
from tests.test_finite_spatial_engine import finite_document


def test_reused_origins_arrive_in_persistent_mapping_order():
    initial = parse_initial_state(document([kind("parcel")], [((0, 0, 0), "parcel")], capacity=4))
    record = initial.seeds[0].record
    world = Simulation(replace(initial, seeds=()))
    west, east, target = (0, 0, 0), (2, 0, 0), (1, 0, 0)
    empty = (None,) * 24
    world._links[east] = empty
    world._links[west] = empty
    for tick in (1, 2):
        for origin, port, amount in ((west, 0, 11), (east, 1, 22)):
            packet = Packet(tick, origin, port, replace(record, values=(pack((amount,)),)))
            world._links[origin] = (packet,) + empty[1:]
        world.tick = tick
        world._deliver()
    assert [item["inventory"] for item in resident_values(world, target)] == [(22,), (11,), (22,), (11,)]
    assert list(world.links) == [east, west]
    assert list(reversed(world.links)) == [west, east]
    assert world.links.copy() == dict(world.links)
    assert all(packet is None for packets in world.links.values() for packet in packets)


def test_link_mapping_replacements_partial_clears_and_deletion_keep_due_ownership():
    initial = parse_initial_state(document([kind("parcel")], [((0, 0, 0), "parcel")]))
    record = initial.seeds[0].record
    first, second = (0, 0, 0), (2, 0, 0)
    links = LinkSchedule()
    early = Packet(3, first, 0, record)
    late = Packet(7, first, 1, record)
    links.update({first: (early, late), second: (replace(early, origin=second), None)})
    view = links.items()
    assert links.due(3) == [first, second]
    links[first] = (None, late)
    assert links.due(3) == [second]
    assert links.due(7) == [first]
    assert dict(view)[first] == (None, late)
    del links[first]
    assert links.due(7) == []
    links[first] = (early,)
    assert links.due(3) == [second, first]
    with pytest.raises(KeyError):
        del links[(99, 0, 0)]
    links.clear()
    assert not links
    assert links.due(3) == []


@pytest.mark.parametrize("boundary,travel,budget", [("periodic", 1, 100000), ("open", 3, 8)])
def test_indexed_scheduling_matches_forced_full_sweeps(boundary, travel, budget):
    raw = finite_document(moving=True, source=True, travel=travel, budget=budget)
    raw["boundary"] = boundary
    raw["shape"] = [5, 4, 5]
    raw["seeds"][0]["position"] = [2, 2, 2]
    raw["emissions"][0]["budget"] = 145
    initial = parse_initial_state(raw)
    events, reference_events = [], []
    world = Simulation(initial, observer=events.append)
    reference = Simulation(initial, observer=reference_events.append)
    reference._links.due = lambda _tick: list(reference._links)
    reference._spatial.links.due = lambda _tick: list(reference._spatial.links)

    def commit_full_sweep():
        for position in sorted(reference._cells):
            reference._commit(position, reference._cells[position])

    reference._commit_ready = commit_full_sweep
    for _ in range(50):
        reference._active_cells.update(reference._cells)
        reference.step()
        world.step()
        assert world.snapshot() == reference.snapshot()
        assert world.computation_report() == reference.computation_report()
        assert world.inventory_and_spatial_accounting() == (
            reference.totals(),
            reference.spatial_accounting(),
        )
    assert events == reference_events
    assert any(event["event"] == "sent" for event in events)
    assert any(event["event"] == "spatial_sent" for event in events)


def test_dormant_carrier_and_link_history_is_not_enumerated_by_stepping():
    raw = document([kind("parcel", values={"inventory": 0})], [((0, 0, 0), "parcel")])
    world = Simulation(parse_initial_state(raw))
    world.step()
    assert not world._active_cells
    for x in range(100):
        world._links[(x, 0, 0)] = (None,) * 6

    class NoHistoryScan(dict):
        def __iter__(self):
            pytest.fail("dormant history was enumerated")

        def values(self):
            pytest.fail("dormant history values were enumerated")

        def items(self):
            pytest.fail("dormant history items were enumerated")

    world._cells = NoHistoryScan(world._cells)
    world._links._packets = NoHistoryScan(world._links._packets)
    world.step()
    assert world.tick == 2


def test_spatial_off_clock_step_does_not_copy_resident_history():
    raw = finite_document(travel=3)
    world = Simulation(parse_initial_state(raw))
    world.step()

    class NoResidentCopy(dict):
        def items(self):
            pytest.fail("resident mapping was copied off the spatial clock")

    world._cells = NoResidentCopy(world._cells)
    world.step()
    assert world.tick == 2


def test_idle_records_continue_polling_a_time_dependent_resolver():
    raw = document([kind("parcel", values={"inventory": 0})], [((0, 0, 0), "parcel")])
    initial = parse_initial_state(raw)
    assembly = Simulation(initial)
    inspected, resolved = [], []

    class TimedResolver:
        def has_work(self, context):
            inspected.append(context.tick)
            return context.tick == 2

        def resolve(self, context, planner):
            resolved.append(context.tick)
            return planner(context.records, context.residuals, context.received)

        def advance(self, tick):
            pass

        def report(self):
            return {}

    world = DisturbanceEngine(
        initial,
        assembly._planner,
        record_policy=assembly._record_policy,
        event_space=CausalEventSpace(),
        resolver=TimedResolver(),
    )
    for _ in range(3):
        world.step()
    assert inspected == [0, 1, 2]
    assert resolved == [2]
    assert world.computation_report()["local_cycles_started"] == 1


def test_combined_diagnostics_reads_spatial_inventory_once_without_carrier_contamination(monkeypatch):
    world = Simulation(parse_initial_state(finite_document(moving=True, source=True)))
    world.step()
    expected = world.totals(), world.spatial_accounting()
    original = world._spatial.totals
    calls = []

    def inventory():
        calls.append(True)
        return original()

    monkeypatch.setattr(world._spatial, "totals", inventory)
    assert world.inventory_and_spatial_accounting() == expected
    assert len(calls) == 1
