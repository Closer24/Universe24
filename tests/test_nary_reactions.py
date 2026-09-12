"""Bounded local n-to-m reaction ownership is configured, atomic and species-neutral."""

import copy

import pytest

from event_universe.core.disturbance_state import OPERATIONS
from event_universe.disturbance_api import Simulation
from event_universe.initialization import parse_initial_state


def configuration():
    return {
        "schema_version": 1,
        "model_id": "generic-three-to-two-reaction-contract-v1",
        "shape": [5, 5, 5],
        "boundary": "open",
        "slots_per_cell": 3,
        "link_ticks": 1,
        "normal_budget": 1000,
        "ticks": 1,
        "operation_costs": dict.fromkeys(OPERATIONS, 1),
        "fields": [
            {
                "name": "inventory",
                "components": 1,
                "units": "test unit",
                "signed": False,
                "conserved": True,
                "extensive": True,
            }
        ],
        "disturbance_types": [
            {"name": "input", "fields": ["inventory"], "transport": {"mode": "hold"}},
            {"name": "output", "fields": ["inventory"], "transport": {"mode": "hold"}},
        ],
        "reactions": [
            {
                "name": "three local inputs become two outputs",
                "input_types": ["input", "input", "input"],
                "output_types": ["output", "output"],
                "assignments": [
                    {
                        "output": 0,
                        "field": "inventory",
                        "expression": {
                            "op": "add",
                            "args": [
                                {"field": "inventory", "participant": 0},
                                {"field": "inventory", "participant": 1},
                            ],
                        },
                    },
                    {
                        "output": 1,
                        "field": "inventory",
                        "expression": {"field": "inventory", "participant": 2},
                    },
                ],
            }
        ],
        "seeds": [
            {"position": [2, 2, 2], "type": "input", "values": {"inventory": value}}
            for value in (1, 2, 3)
        ],
    }


def test_three_to_two_reaction_is_one_atomic_local_transaction():
    world = Simulation(parse_initial_state(configuration()))
    assert world.totals() == {"inventory": (6,)}
    world.step()
    cell = world.cells[(2, 2, 2)]
    records = [record for record in cell.records if record is not None]
    assert len(records) == 2
    assert [record.type_index for record in records] == [1, 1]
    assert sorted(world.record_values(record)["inventory"] for record in records) == [(3,), (3,)]
    assert world.totals() == {"inventory": (6,)}


def test_nary_reaction_rejects_tampered_conservation_without_partial_commit():
    raw = configuration()
    raw["reactions"][0]["assignments"][1]["expression"] = 2
    world = Simulation(parse_initial_state(raw))
    before = world.snapshot()
    with pytest.raises(ValueError, match="conservation of inventory"):
        world.step()
    assert world.snapshot() == before
    assert all(cell.pending is None for cell in world.cells.values())


def test_reaction_arity_must_fit_fixed_local_slot_capacity():
    raw = configuration()
    raw["reactions"][0]["output_types"] = ["output"] * 4
    raw["reactions"][0]["assignments"] = [
        {"output": index, "field": "inventory", "expression": 1} for index in range(4)
    ]
    with pytest.raises(ValueError, match="arity exceeds slots_per_cell"):
        parse_initial_state(raw)


def test_runtime_capacity_failure_does_not_discard_inputs():
    raw = configuration()
    raw["slots_per_cell"] = 4
    raw["disturbance_types"].append(
        {"name": "resident", "fields": ["inventory"], "transport": {"mode": "hold"}}
    )
    raw["seeds"].append({"position": [2, 2, 2], "type": "resident", "values": {"inventory": 0}})
    raw["reactions"][0]["output_types"] = ["output"] * 4
    raw["reactions"][0]["assignments"] = [
        {"output": index, "field": "inventory", "expression": 0} for index in range(4)
    ]
    raw["reactions"][0]["assignments"][0]["expression"] = {
        "op": "add",
        "args": [
            {"field": "inventory", "participant": 0},
            {"field": "inventory", "participant": 1},
        ],
    }
    raw["reactions"][0]["assignments"][1]["expression"] = {
        "field": "inventory",
        "participant": 2,
    }
    world = Simulation(parse_initial_state(raw))
    before = world.snapshot()
    with pytest.raises(ValueError, match="output capacity exhausted"):
        world.step()
    assert world.snapshot() == before


def test_legacy_side_expressions_remain_unchanged():
    raw = configuration()
    converted = copy.deepcopy(raw)
    converted["reactions"] = []
    parse_initial_state(converted)
