"""Public execution checks for the declared Node model, distinct from physical claims."""

import json
from pathlib import Path

import pytest

from event_universe.core.node_conservation import LocalInventory
from event_universe.disturbance_api import Simulation
from event_universe.fields.node_conservation import LocalBalanceGuard
from event_universe.initialization import parse_initial_state

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = (2, 2, 2)


def example(name):
    return json.loads((ROOT / "examples/node-vector" / f"{name}.json").read_text(encoding="utf-8"))


def measured(world):
    initial = world.initial
    policy = LocalBalanceGuard(
        initial.fields, initial.spatial_fields, initial.operation_costs, initial.conservation_contract
    )
    values = []
    view = world.inventory_view()
    for node in view.nodes:
        values.append(
            policy.measure(
                LocalInventory(
                    records=node.records, spatial=tuple(state.populations for state in node.spatial)
                )
            )
        )
    for packet in view.packets:
        values.append(
            policy.measure(
                LocalInventory(
                    carrier_packets=() if packet.record is None else (packet.record,),
                    spatial_packets=() if not packet.spatial else (packet.spatial,),
                )
            )
        )
    return tuple(
        tuple(sum(value[q][c] for value in values) for c in range(quantity.components))
        for q, quantity in enumerate(initial.conservation_contract.quantities)
    )


def energy_registers(world):
    return [
        world.record_values(record)["registers"][0]
        for record in world.nodes[ORIGIN].records
        if record is not None
    ]


def test_six_record_rule_waits_three_h_with_actual_owners_preserved():
    world = Simulation(parse_initial_state(example("six-records")))
    expected = ((21,), (3, 0, 0), (0,), (0, 15, 0))
    assert measured(world) == expected
    for tick in (1, 2):
        world.step()
        assert world.tick == tick
        assert energy_registers(world) == [1, 2, 3, 4, 5, 6]
        assert world.nodes[ORIGIN].pending.ready_tick == 3
        assert world.nodes[ORIGIN].delay_counts == (3 - tick,) * 6
        assert measured(world) == expected
    world.step()
    assert energy_registers(world) == [2, 3, 4, 5, 6, 1]
    assert measured(world) == expected
    assert world.nodes[ORIGIN].pending is None
    assert world.nodes[ORIGIN].delay_counts == (0,) * 6
    assert world.conservation_report()["node_contract"]["mode"] == "exact_pre_commit"
    assert (
        tuple(row["value"] for row in world.conservation_report()["node_contract"]["quantities"])
        == expected
    )
    before = world.inventory_view()
    world.conservation_report()
    assert world.inventory_view() == before


def test_two_local_fields_and_carrier_commit_together_after_two_h():
    world = Simulation(parse_initial_state(example("two-fields")))
    expected = ((7,), (0, 0, 0), (0,), (0, 0, 0))
    before = world.nodes[ORIGIN].records
    world.step()
    assert world.nodes[ORIGIN].records == before
    assert world.spatial_values(ORIGIN)["second"]["value"][0] == 2
    assert measured(world) == expected
    world.step()
    carrier = next(record for record in world.nodes[ORIGIN].records if record is not None)
    assert world.record_values(carrier)["first"] == (2, -2, 1, 0, -1, 0, 0, -1)
    assert world.spatial_values(ORIGIN)["second"]["value"] == (5, 2, -1, 0, 1, 0, 0, 1)
    assert measured(world) == expected
    for _ in range(5):
        world.step()
        assert measured(world) == expected


def test_declared_guard_rejects_bad_carrier_output_before_owner_mutation():
    raw = example("six-records")
    raw["interactions"][0]["invariants"] = [{"name": "irrelevant_constant", "expression": 0}]
    raw["interactions"][0]["assignments"][0]["expression"] = [999, 0, 0, 0, 0, 0, 0, 0]
    world = Simulation(parse_initial_state(raw))
    world.step()
    world.step()
    before = world.inventory_view()
    with pytest.raises(ValueError, match="conserved readout"):
        world.step()
    assert world.faulted
    assert world.inventory_view() == before
    assert energy_registers(world) == [1, 2, 3, 4, 5, 6]


def test_declared_guard_rejects_bad_spatial_output_before_owner_mutation():
    raw = example("two-fields")
    raw["seeds"] = []
    raw["spatial_interactions"] = []
    raw["field_rules"] = [
        {
            "name": "invalid_source",
            "k": 1,
            "assignments": [
                {
                    "field": "second",
                    "expression": {
                        "op": "add",
                        "args": [{"field": "second", "side": "right"}, [1, 0, 0, 0, 0, 0, 0, 0]],
                    },
                }
            ],
            "invariants": [{"name": "irrelevant_constant", "expression": 0}],
        }
    ]
    world = Simulation(parse_initial_state(raw))
    original = measured(world)
    with pytest.raises(ValueError, match="conserved readout"):
        world.step()
    assert world.faulted
    assert measured(world) == original
    assert world.spatial_values(ORIGIN)["second"]["value"][0] == 2
