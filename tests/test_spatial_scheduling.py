"""Skipping dormant host records must retain local clocks, costs and physical output."""

import pytest

from event_universe import Simulation
from event_universe.initialization import parse_initial_state
from tests.test_finite_spatial_engine import finite_document
from tests.test_spatial_coupling import document as coupling_document
from tests.test_spatial_engine import ORIGIN


@pytest.mark.parametrize("boundary,travel,budget", [("periodic", 1, 100000), ("open", 2, 8)])
def test_active_scheduling_matches_a_full_cell_sweep(boundary, travel, budget):
    raw = finite_document(moving=True, source=True, travel=travel, budget=budget)
    raw["boundary"] = boundary
    raw["shape"] = [3, 4, 5]
    raw["seeds"][0]["position"] = [2, 2, 2]
    raw["emissions"][0]["budget"] = 145
    raw["spatial_fields"][0]["axis_weights"] = [2, 1, 0]
    initial = parse_initial_state(raw)
    events, reference_events = [], []
    world = Simulation(initial, observer=events.append)
    reference = Simulation(initial, observer=reference_events.append)
    for _ in range(40):
        reference._spatial._active.update(reference._spatial.cells)
        reference.step()
        world.step()
        assert world.snapshot() == reference.snapshot()
        assert world.totals() == reference.totals()
        assert world.spatial_accounting() == reference.spatial_accounting()
    assert events == reference_events


def test_empty_history_is_not_scanned_by_steps_or_inventory_checks():
    raw = finite_document()
    raw["spatial_seeds"] = [
        {"position": list(ORIGIN), "field": "radiation", "populations": [1, 0, 0, 0, 0, 0, 0, 0]}
    ]
    world = Simulation(parse_initial_state(raw))
    for _ in range(4):
        world.step()
    assert not world._spatial._active

    class NoHistoryScan(dict):
        def __iter__(self):
            pytest.fail("idle spatial history was enumerated")

        def values(self):
            pytest.fail("idle spatial history values were enumerated")

        def items(self):
            pytest.fail("idle spatial history items were enumerated")

    world._spatial.cells = NoHistoryScan(world._spatial.cells)
    for _ in range(3):
        world.step()
        assert world.totals()["radiation"] == (0,)
        assert world.spatial_accounting()["radiation"]["balanced"]


def test_reaction_wakes_a_known_idle_cell_without_missing_its_completed_phase():
    raw = coupling_document()
    raw["seeds"] = []
    world = Simulation(parse_initial_state(raw))
    engine = world._spatial
    engine._at(ORIGIN)
    engine.begin(0, {}, lambda _position, _records: None)
    assert ORIGIN not in engine._active
    engine.begin(1, {}, lambda _position, _records: None)
    reaction = ((8, -8, 0), (0, 0, 0), (0,))
    proposal = engine.prepare_reaction(ORIGIN, 1, reaction)
    assert proposal.links is not None
    assert all(packet is None or packet.arrival_tick == 2 for packet in proposal.links)
    engine.commit_reaction(ORIGIN, proposal, reaction)
    assert ORIGIN in engine._active
    engine.deliver(2)
    assert engine.accounting()["inventory"]["current"] == (8, -8, 0)
    assert engine.accounting()["inventory"]["balanced"]


def test_a_new_cell_is_not_backdated_to_an_earlier_empty_phase():
    raw = coupling_document()
    raw["seeds"] = []
    world = Simulation(parse_initial_state(raw))
    engine = world._spatial
    engine.begin(1, {}, lambda _position, _records: None)
    reaction = ((8, -8, 0), (0, 0, 0), (0,))
    proposal = engine.prepare_reaction(ORIGIN, 1, reaction)
    assert proposal.links is None
    engine.commit_reaction(ORIGIN, proposal, reaction)
    assert engine.accounting()["inventory"]["current"] == (8, -8, 0)
    assert ORIGIN in engine._active
