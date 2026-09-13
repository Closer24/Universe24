"""Explicit left-owned exchange fractions survive changes of local partner."""

import pytest

from event_universe import Simulation
from event_universe.core.disturbance_state import OPERATIONS, unpack
from event_universe.initialization import parse_initial_state


def initialization(amount=1, *, owner="left", components=1, signed=True):
    zero = 0 if components == 1 else [0, 0, 0]
    coupling = {
        "name": "exchange",
        "left_type": "mover",
        "right_type": "receiver",
        "field": "inventory",
        "amount": amount,
        "denominator": 3,
    }
    if owner is not None:
        coupling["remainder_owner"] = owner
    return {
        "schema_version": 1,
        "model_id": "carried-exchange-residual-v1",
        "shape": [23, 7, 7],
        "slots_per_node": 5,
        "link_ticks": 1,
        "normal_budget": 10000,
        "ticks": 8,
        "operation_costs": {name: 1 for name in OPERATIONS},
        "fields": [
            {
                "name": "inventory",
                "components": components,
                "units": "unit",
                "signed": signed,
                "conserved": True,
            },
            {"name": "signal", "components": 1, "units": "ratio", "signed": True, "conserved": False},
        ],
        "disturbance_types": [
            {
                "name": "mover",
                "fields": ["inventory"],
                "defaults": {"inventory": zero},
                "transport": {"mode": "move", "weights": [1, 0, 0, 0, 0, 0]},
            },
            {
                "name": "receiver",
                "fields": ["inventory", "signal"],
                "defaults": {"inventory": zero, "signal": 1},
                "transport": {"mode": "hold"},
            },
        ],
        "couplings": [coupling],
        "seeds": [{"position": [3, 3, 3], "type": "mover"}]
        + [{"position": [x, 3, 3], "type": "receiver"} for x in range(3, 10)],
    }


def mover(world, x):
    return next(
        record
        for record in world.nodes[(x, 3, 3)].records
        if record is not None and record.type_index == 0
    )


def receiver(world, x):
    return next(
        record
        for record in world.nodes[(x, 3, 3)].records
        if record is not None and record.type_index == 1
    )


@pytest.mark.parametrize("sign", [-1, 1])
def test_moving_left_owner_accumulates_fraction_across_three_fresh_receivers(sign):
    world = Simulation(parse_initial_state(initialization(sign)))
    for tick in (1, 2, 3):
        world.step()
        carried = mover(world, 3 + tick)
        assert world.record_values(carried)["inventory"] == (-sign * (tick // 3),)
        assert unpack(carried.exchange_remainders[0]) == (sign * (tick % 3),)
        assert world.totals() == {"inventory": (0,)}
    assert [world.record_values(receiver(world, x))["inventory"] for x in (3, 4, 5)] == [
        (0,),
        (0,),
        (sign,),
    ]


def test_vector_components_accumulate_independently_while_moving():
    world = Simulation(parse_initial_state(initialization([1, -1, 2], components=3)))
    expected = [((0, 0, 0), (1, -1, 2)), ((0, 0, -1), (2, -2, 1)), ((-1, 1, -2), (0, 0, 0))]
    for tick, (value, residue) in enumerate(expected, 1):
        world.step()
        record = mover(world, 3 + tick)
        assert world.record_values(record)["inventory"] == value
        assert unpack(record.exchange_remainders[0]) == residue
        assert world.totals() == {"inventory": (0, 0, 0)}


def test_signed_reversal_cancels_carried_fraction_before_reversing_exchange():
    raw = initialization({"field": "signal", "side": "right"})
    signs = (1, 1, -1, -1, -1, -1, -1)
    for seed, sign in zip(raw["seeds"][1:], signs, strict=True):
        seed["values"] = {"signal": sign}
    world = Simulation(parse_initial_state(raw))
    expected_residues = (1, 2, 1, 0, -1, -2, 0)
    for tick, residue in enumerate(expected_residues, 1):
        world.step()
        record = mover(world, 3 + tick)
        assert unpack(record.exchange_remainders[0]) == (residue,)
        assert world.record_values(record)["inventory"] == (int(tick == 7),)
        assert world.totals() == {"inventory": (0,)}


def test_multiple_right_participants_consume_one_left_remainder_in_slot_order():
    raw = initialization()
    raw["disturbance_types"][0]["transport"] = {"mode": "hold"}
    raw["seeds"] = [{"position": [3, 3, 3], "type": "mover"}] + [
        {"position": [3, 3, 3], "type": "receiver"} for _ in range(3)
    ]
    world = Simulation(parse_initial_state(raw))
    world.step()
    values = [
        world.record_values(record)["inventory"]
        for record in world.nodes[(3, 3, 3)].records
        if record is not None
    ]
    assert values == [(-1,), (0,), (0,), (1,)]
    assert unpack(mover(world, 3).exchange_remainders[0]) == (0,)
    assert world.totals() == {"inventory": (0,)}


def test_signed_vector_exchange_with_two_receivers_matches_independent_three_cycle_values():
    raw = initialization([2, -2, 1], components=3)
    raw["disturbance_types"][0]["transport"] = {"mode": "hold"}
    raw["seeds"] = [{"position": [3, 3, 3], "type": "mover", "values": {"inventory": [10, -10, 5]}}] + [
        {"position": [3, 3, 3], "type": "receiver"} for _ in range(2)
    ]
    world = Simulation(parse_initial_state(raw))
    expected = [
        ([(9, -9, 5), (0, 0, 0), (1, -1, 0)], (1, -1, 2)),
        ([(8, -8, 4), (1, -1, 1), (1, -1, 0)], (2, -2, 1)),
        ([(6, -6, 3), (2, -2, 1), (2, -2, 1)], (0, 0, 0)),
    ]
    for values, residue in expected:
        world.step()
        records = [record for record in world.nodes[(3, 3, 3)].records if record is not None]
        assert [world.record_values(record)["inventory"] for record in records] == values
        assert unpack(records[0].exchange_remainders[0]) == residue
        assert world.totals() == {"inventory": (10, -10, 5)}


@pytest.mark.parametrize("owner", [None, "pair"])
def test_default_pair_owner_still_resets_at_departure(owner):
    initial = parse_initial_state(initialization(owner=owner))
    assert initial.couplings[0].remainder_owner == "pair"
    world = Simulation(initial)
    for tick in (1, 2, 3):
        world.step()
        record = mover(world, 3 + tick)
        assert world.record_values(record)["inventory"] == (0,)
        assert record.exchange_remainders == ()
        assert world.totals() == {"inventory": (0,)}


@pytest.mark.parametrize("owner", ["right", "global", "LEFT", 1, None])
def test_unsupported_explicit_owner_is_rejected(owner):
    raw = initialization()
    raw["couplings"][0]["remainder_owner"] = owner
    with pytest.raises(ValueError, match="remainder_owner"):
        parse_initial_state(raw)


def test_same_type_and_split_left_owner_are_rejected():
    raw = initialization()
    raw["couplings"][0]["right_type"] = "mover"
    with pytest.raises(ValueError, match="distinct participant types"):
        parse_initial_state(raw)
    raw = initialization()
    raw["disturbance_types"][0]["transport"]["mode"] = "split"
    with pytest.raises(ValueError, match="whole-record hold or move"):
        parse_initial_state(raw)


def test_invalid_exchange_preserves_both_current_records_and_the_carried_fraction():
    world = Simulation(parse_initial_state(initialization(-1, signed=False)))
    world.step()
    world.step()
    before = world.nodes[(5, 3, 3)].records
    assert unpack(mover(world, 5).exchange_remainders[0]) == (-2,)
    with pytest.raises(ValueError, match="negative"):
        world.step()
    assert world.nodes[(5, 3, 3)].records == before
    assert world.totals() == {"inventory": (0,)}


def test_delayed_emitter_refresh_keeps_the_proposed_exchange_remainder():
    raw = initialization()
    raw["normal_budget"] = 10
    raw["fields"].append(
        {"name": "radiation", "components": 1, "units": "unit", "signed": True, "conserved": True}
    )
    raw["spatial_fields"] = [{"field": "radiation", "baseline": 0, "transport": "outward"}]
    raw["emissions"] = [
        {"type": "mover", "field": "radiation", "amount": 1, "denominator": 101, "source": True}
    ]
    world = Simulation(parse_initial_state(raw))
    world.step()
    pending = world.nodes[(3, 3, 3)].pending
    assert pending is not None and 2 <= pending.ready_tick < 101
    while world.tick < pending.ready_tick:
        assert mover(world, 3).exchange_remainders == ()
        world.step()
    packet = next(packet for packet in world.links[(3, 3, 3)] if packet is not None)
    assert unpack(packet.record.exchange_remainders[0]) == (1,)
    assert unpack(packet.record.emission_remainders[0]) == (pending.ready_tick,)
    assert world.totals() == {"inventory": (0,), "radiation": (0,)}
