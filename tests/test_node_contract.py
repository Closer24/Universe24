"""Canonical node vocabulary, one capacity owner and validated migration."""

from copy import deepcopy
from dataclasses import fields

import pytest

from event_universe import Simulation
from event_universe.core.disturbance_state import InitialState
from event_universe.diagnostics.node_contract import node_state_violations
from event_universe.initialization import parse_initial_state

from .test_disturbance_engine import document, kind


def test_canonical_and_legacy_node_capacity_preserve_actual_run_behavior():
    legacy = document([kind("parcel", values={"inventory": 7})], [((4, 4, 4), "parcel")])
    canonical = deepcopy(legacy)
    canonical["slots_per_node"] = canonical.pop("slots_per_cell")
    before = deepcopy((legacy, canonical))
    initial = parse_initial_state(canonical)
    assert initial == parse_initial_state(legacy)
    assert initial.slots_per_node == initial.slots_per_cell == canonical["slots_per_node"]
    assert "slots_per_node" in {field.name for field in fields(InitialState)}
    assert "slots_per_cell" not in {field.name for field in fields(InitialState)}
    events, old_events = [], []
    world = Simulation(initial, observer=events.append)
    old = Simulation(parse_initial_state(legacy), observer=old_events.append)
    for _ in range(3):
        world.step()
        old.step()
        assert world.snapshot() == old.snapshot()
        assert events == old_events
    assert world.nodes == world.cells
    assert not node_state_violations(world.node_view((4, 4, 4)))
    assert (legacy, canonical) == before


@pytest.mark.parametrize("capacity", [2, 3])
def test_two_names_for_one_node_capacity_are_rejected_without_mutation(capacity):
    raw = document([kind("parcel")], [], capacity=2)
    raw["slots_per_node"] = capacity
    original = deepcopy(raw)
    with pytest.raises(ValueError, match="cannot be combined"):
        parse_initial_state(raw)
    assert raw == original


@pytest.mark.parametrize("capacity", [False, 0, 33])
def test_canonical_node_capacity_retains_integer_and_storage_bounds(capacity):
    raw = document([kind("parcel")], [])
    del raw["slots_per_cell"]
    raw["slots_per_node"] = capacity
    with pytest.raises(ValueError, match="slots_per_node"):
        parse_initial_state(raw)
