"""Explicit whole-record motion does not depend on a nonzero payload."""

import pytest

from event_universe.core.disturbance_state import OPERATIONS, unpack
from event_universe.reference_api import ReferenceSimulation as Simulation
from event_universe.reference_api import parse_reference_state as parse_initial_state


def initialization(*, travel=1):
    return {
        "schema_version": 1,
        "model_id": "zero-carrier-fixed-route-v1",
        "shape": [23, 7, 7],
        "slots_per_cell": 2,
        "link_ticks": travel,
        "normal_budget": 10000,
        "ticks": 8,
        "operation_costs": {name: 1 for name in OPERATIONS},
        "fields": [
            {"name": "stock", "components": 1, "units": "unit", "signed": True, "conserved": True}
        ],
        "disturbance_types": [
            {
                "name": "carrier",
                "fields": ["stock"],
                "transport": {"mode": "move", "weights": [1, 0, 0, 0, 0, 0]},
            },
            {"name": "receiver", "fields": ["stock"], "transport": {"mode": "hold"}},
        ],
        "seeds": [{"position": [3, 3, 3], "type": "carrier"}],
    }


def carriers(world):
    return [
        (position, record)
        for position, cell in world.cells.items()
        for record in cell.records
        if record is not None and record.type_index == 0
    ]


@pytest.mark.parametrize("travel", [1, 2])
def test_zero_payload_carrier_moves_at_the_configured_link_time(travel):
    world = Simulation(parse_initial_state(initialization(travel=travel)))
    for interval in range(1, 5):
        for elapsed in range(1, travel + 1):
            world.step()
            assert world.totals() == {"stock": (0,)}
            if elapsed < travel:
                assert carriers(world) == []
                assert (
                    sum(packet is not None for packets in world.links.values() for packet in packets)
                    == 1
                )
        [(position, record)] = carriers(world)
        assert position == (3 + interval, 3, 3)
        assert world.record_values(record) == {"stock": (0,)}


def test_carried_exchange_fraction_crosses_empty_cells_before_later_receivers():
    raw = initialization()
    raw["couplings"] = [
        {
            "name": "fractional_request",
            "left_type": "carrier",
            "right_type": "receiver",
            "field": "stock",
            "amount": 1,
            "denominator": 3,
            "remainder_owner": "left",
        }
    ]
    raw["seeds"].extend({"position": [x, 3, 3], "type": "receiver"} for x in (3, 6, 9))
    world = Simulation(parse_initial_state(raw))
    for tick in range(1, 8):
        world.step()
        [(position, record)] = carriers(world)
        assert position == (3 + tick, 3, 3)
        contacts = (tick - 1) // 3 + 1
        assert unpack(record.exchange_remainders[0]) == (contacts % 3,)
        assert world.record_values(record)["stock"] == (-(contacts // 3),)
        assert world.totals() == {"stock": (0,)}
    receipts = [
        world.record_values(record)["stock"]
        for x in (3, 6, 9)
        for record in world.cells[(x, 3, 3)].records
        if record is not None and record.type_index == 1
    ]
    assert receipts == [(0,), (0,), (1,)]


def test_zero_split_channel_remains_idle():
    raw = initialization()
    raw["disturbance_types"][0]["transport"]["mode"] = "split"
    world = Simulation(parse_initial_state(raw))
    for _ in range(3):
        world.step()
    [(position, record)] = carriers(world)
    assert position == (3, 3, 3)
    assert world.record_values(record) == {"stock": (0,)}
    assert world.cells[position].last_cost == 0
    assert not world.links
