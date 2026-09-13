"""Atomic carrier/node updates with exact balances and delayed commit guards."""

from copy import deepcopy

import pytest

from event_universe import Simulation
from event_universe.core.disturbance_state import MAX_VALUE
from event_universe.initialization import parse_initial_state

from .test_local_field_rules import ORIGIN, document, field, invariant, local, operation, seed, value


def carrier(world):
    return next(
        world.record_values(record)["quantity"]
        for record in world.nodes[ORIGIN].records
        if record is not None
    )


def exchange(*, delayed=False, incoming=False):
    raw = document([field("quantity", conserved=True)], [seed("quantity", 2)])
    raw["disturbance_types"][0]["defaults"] = {"quantity": 5}
    raw["seeds"] = [{"position": list(ORIGIN), "type": "held"}]
    raw["normal_budget"] = 10 if delayed else 100000
    particle = {"field": "quantity", "side": "left"}
    spatial = local("quantity")
    raw["spatial_interactions"] = [
        {
            "name": "swap_inventory",
            "type": "held",
            "assignments": [
                {"side": "left", "field": "quantity", "expression": spatial},
                {"side": "right", "field": "quantity", "expression": particle},
            ],
            "invariants": [
                invariant("joint_inventory", operation("add", particle, spatial)),
                invariant(
                    "joint_squared_values",
                    operation(
                        "add", operation("mul", particle, particle), operation("mul", spatial, spatial)
                    ),
                ),
            ],
        }
    ]
    if incoming:
        raw["spatial_seeds"].append(seed("quantity", 1, (1, 2, 2)))
        raw["field_rules"] = [
            {
                "name": "route_one_unit",
                "when": operation("gt", 2, spatial),
                "assignments": [
                    {"field": "quantity", "expression": 0},
                    {"field": "quantity", "port": 0, "expression": spatial},
                ],
                "invariants": [
                    invariant("stock", operation("add", spatial, {"outgoing": "quantity", "port": 0}))
                ],
            }
        ]
    return raw


@pytest.mark.parametrize("delayed", [False, True])
def test_carrier_and_local_field_swap_atomically_with_exact_joint_invariants(delayed):
    world = Simulation(parse_initial_state(exchange(delayed=delayed)))
    world.step()
    if delayed:
        pending = world.nodes[ORIGIN].pending
        assert pending is not None and pending.ready_tick > 1
        ready = pending.ready_tick
        while world.tick < ready:
            assert carrier(world) == (5,)
            assert value(world, "quantity") == (2,)
            assert world.totals()["quantity"] == (7,)
            world.step()
    assert carrier(world) == (2,)
    assert value(world, "quantity") == (5,)
    assert carrier(world)[0] ** 2 + value(world, "quantity")[0] ** 2 == 29
    assert world.totals()["quantity"] == (7,)
    assert world.source_totals()["quantity"] == (0,)
    assert world.spatial_accounting()["quantity"]["reactions"] == (3,)
    assert world.spatial_accounting()["quantity"]["balanced"]


def test_arrival_during_delay_cannot_commit_a_stale_nonlinear_invariant():
    world = Simulation(parse_initial_state(exchange(delayed=True, incoming=True)))
    world.step()
    pending = world.nodes[ORIGIN].pending
    assert pending is not None and pending.ready_tick > 1
    ready = pending.ready_tick
    assert value(world, "quantity") == (3,)
    while world.tick < ready - 1:
        assert carrier(world) == (5,)
        assert value(world, "quantity") == (3,)
        assert world.totals()["quantity"] == (8,)
        world.step()
    # Frozen delta +3 would preserve 5+3 = 2+6, but would change 34 to 40.
    with pytest.raises(ValueError, match="invariant"):
        world.step()
    assert world.faulted
    assert carrier(world) == (5,)
    assert value(world, "quantity") == (3,)
    assert world.totals()["quantity"] == (8,)
    assert world.spatial_accounting()["quantity"]["reactions"] == (0,)
    assert world.spatial_accounting()["quantity"]["balanced"]


def test_delayed_linear_exchange_preserves_stock_received_after_its_original_sample():
    raw = exchange(delayed=True, incoming=True)
    raw["spatial_interactions"][0]["invariants"] = raw["spatial_interactions"][0]["invariants"][:1]
    world = Simulation(parse_initial_state(raw))
    world.step()
    pending = world.nodes[ORIGIN].pending
    assert pending is not None and pending.ready_tick > 1
    ready = pending.ready_tick
    while world.tick < ready:
        assert carrier(world) == (5,)
        assert value(world, "quantity") == (3,)
        assert world.totals()["quantity"] == (8,)
        world.step()
    # Original stock two receives one independently, then the frozen reaction adds three.
    assert carrier(world) == (2,)
    assert value(world, "quantity") == (6,)
    assert world.totals()["quantity"] == (8,)
    assert world.spatial_accounting()["quantity"]["reactions"] == (3,)
    assert world.spatial_accounting()["quantity"]["balanced"]


def test_active_field_and_joint_rules_keep_results_after_rename_and_declaration_permutation():
    raw = exchange()
    raw["fields"].append(field("signal", 3))
    raw["disturbance_types"][0]["fields"].append("signal")
    raw["spatial_fields"].append({"field": "signal", "baseline": [0, 0, 0], "transport": "local"})
    raw["spatial_seeds"].append(seed("signal", [3, 4, 0]))
    raw["field_groups"] = [{"name": "configured_components", "fields": ["quantity", "signal"]}]
    signal = local("signal")
    raw["field_rules"] = [
        {
            "name": "rotate_signal",
            "assignments": [{"field": "signal", "expression": operation("cross", [0, 0, 1], signal)}],
            "invariants": [invariant("squared_amplitude", operation("dot", signal, signal))],
        }
    ]
    names = {"quantity": "renamed_inventory", "signal": "renamed_vector"}

    def rename(item):
        if isinstance(item, dict):
            return {names.get(key, key): rename(value) for key, value in item.items()}
        if isinstance(item, list):
            return [rename(value) for value in item]
        return names.get(item, item) if isinstance(item, str) else item

    changed = rename(raw)
    for collection in ("fields", "spatial_fields", "spatial_seeds"):
        changed[collection].reverse()
    changed["disturbance_types"][0]["fields"].reverse()
    changed["field_groups"][0]["fields"].reverse()
    original = Simulation(parse_initial_state(raw))
    renamed = Simulation(parse_initial_state(changed))
    for particle, stock, vector in ((2, 5, (-4, 3, 0)), (5, 2, (-3, -4, 0))):
        original.step()
        renamed.step()
        assert carrier(original) == (particle,)
        renamed_record = next(record for record in renamed.nodes[ORIGIN].records if record is not None)
        assert renamed.record_values(renamed_record)[names["quantity"]] == (particle,)
        for name, expected in (("quantity", (stock,)), ("signal", vector)):
            assert value(original, name) == value(renamed, names[name]) == expected
            assert original.spatial_accounting()[name] == renamed.spatial_accounting()[names[name]]
        assert original.totals() == {"quantity": (7,)}
        assert renamed.totals() == {names["quantity"]: (7,)}


def test_nonempty_joint_rules_require_declared_spatial_owners():
    raw = exchange()
    del raw["spatial_fields"]
    del raw["spatial_seeds"]
    particle = {"field": "quantity", "side": "left"}
    raw["spatial_interactions"][0]["assignments"] = [
        {"side": "left", "field": "quantity", "expression": particle}
    ]
    raw["spatial_interactions"][0]["invariants"] = [invariant("carrier_inventory", particle)]
    with pytest.raises(ValueError):
        parse_initial_state(raw)


def test_zero_net_joint_chain_keeps_both_guards_and_prices_its_frozen_delay():
    ready_ticks = []
    costs = []
    for read_price in (1, 10):
        raw = exchange(delayed=True)
        second = deepcopy(raw["spatial_interactions"][0])
        second["name"] = "swap_back"
        raw["spatial_interactions"].append(second)
        raw["operation_costs"]["read"] = read_price
        world = Simulation(parse_initial_state(raw))
        world.step()
        pending = world.nodes[ORIGIN].pending
        assert pending is not None and pending.ready_tick > 1
        assert pending.plan.spatial_reaction == ((0,),)
        assert len(pending.plan.spatial_guards) == 2
        ready_ticks.append(pending.ready_tick)
        costs.append(pending.plan.cost)
        while world.tick < pending.ready_tick:
            assert carrier(world) == (5,)
            assert value(world, "quantity") == (2,)
            world.step()
        assert carrier(world) == (5,)
        assert value(world, "quantity") == (2,)
        assert world.totals()["quantity"] == (7,)
        assert world.spatial_accounting()["quantity"]["reactions"] == (0,)
    assert costs[1] > costs[0]
    assert ready_ticks[1] > ready_ticks[0]


def test_immutable_baseline_cannot_supply_an_unsigned_carrier_exchange():
    raw = exchange()
    raw["fields"][0]["signed"] = False
    raw["spatial_fields"][0]["baseline"] = 10
    world = Simulation(parse_initial_state(raw))
    assert value(world, "quantity") == (12,)
    initial_total = world.totals()["quantity"]
    assert initial_total == (1257,)  # 125 immutable node baselines, plus carrier and seed.
    # Swapping observable values 5 and 12 would require dynamic stock -5.
    with pytest.raises((ValueError, OverflowError)):
        world.step()
    assert world.faulted
    assert carrier(world) == (5,)
    assert value(world, "quantity") == (12,)
    assert world.totals()["quantity"] == initial_total
    assert world.spatial_accounting()["quantity"]["reactions"] == (0,)


def test_existing_exchange_into_local_field_retains_its_reaction_at_the_same_node():
    raw = exchange()
    del raw["spatial_interactions"]
    raw["spatial_couplings"] = [
        {
            "name": "transfer_to_local_stock",
            "type": "held",
            "field": "quantity",
            "mode": "exchange",
            "amount": 1,
        }
    ]
    world = Simulation(parse_initial_state(raw))
    world.step()
    assert carrier(world) == (4,)
    assert value(world, "quantity") == (3,)
    assert world.snapshot()["spatial_transfers"] == []
    assert world.totals()["quantity"] == (7,)
    assert world.source_totals()["quantity"] == (0,)
    assert world.spatial_accounting()["quantity"]["reactions"] == (1,)
    assert world.spatial_accounting()["quantity"]["balanced"]


@pytest.mark.parametrize("failure", ["invariant", "conserved", "overflow"])
def test_invalid_joint_proposal_commits_neither_carrier_nor_field(failure):
    raw = exchange()
    rule = raw["spatial_interactions"][0]
    if failure == "invariant":
        # Sum seven survives, while squared values fall from 29 to 25.
        rule["assignments"][0]["expression"] = 3
        rule["assignments"][1]["expression"] = 4
    elif failure == "conserved":
        rule["assignments"][1]["expression"] = 6
        rule["invariants"] = [invariant("squared_carrier_field_difference", 0)]
    else:
        rule["assignments"][1]["expression"] = operation("add", MAX_VALUE, 1)
    world = Simulation(parse_initial_state(raw))
    with pytest.raises((ValueError, OverflowError)):
        world.step()
    assert world.faulted
    assert carrier(world) == (5,)
    assert value(world, "quantity") == (2,)
    assert world.totals()["quantity"] == (7,)
    assert world.nodes[ORIGIN].pending is None
    assert world.spatial_accounting()["quantity"]["reactions"] == (0,)


@pytest.mark.parametrize("malformation", ["split", "outward_write", "duplicate", "cost_write"])
def test_joint_schema_rejects_unsupported_owners_and_ambiguous_writes(malformation):
    raw = exchange()
    rule = raw["spatial_interactions"][0]
    if malformation == "split":
        raw["disturbance_types"][0]["transport"] = {"mode": "split", "weights": [1, 0, 0, 0, 0, 0]}
    elif malformation == "outward_write":
        raw["spatial_fields"][0]["transport"] = "outward"
    elif malformation == "duplicate":
        rule["assignments"].append(deepcopy(rule["assignments"][0]))
    else:
        raw["fields"].append(field("work"))
        raw["fields"][-1]["extensive"] = False
        raw["disturbance_types"][0]["fields"].append("work")
        raw["disturbance_types"][0]["cost_field"] = "work"
        rule["assignments"].append({"side": "left", "field": "work", "expression": 0})
    with pytest.raises(ValueError):
        parse_initial_state(raw)
