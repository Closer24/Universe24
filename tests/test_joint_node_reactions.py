"""Real local transactions across distinct carrier roles and one field owner."""

from copy import deepcopy
from dataclasses import replace

import pytest

from event_universe import Simulation
from event_universe.core.coupling_selectors import participant_groups, selected_types
from event_universe.core.node_boundary import validate_local_plan
from event_universe.initialization import parse_initial_state

from .test_joint_reaction_configuration import joint_document
from .test_local_field_rules import ORIGIN, field, invariant, local, operation, value
from .test_spatial_interactions import carrier, exchange


def quantities(world):
    return tuple(
        world.record_values(record)["quantity"][0]
        for record in world.nodes[ORIGIN].records
        if record is not None
    )


def cross_layout_document():
    raw = joint_document()
    raw["fields"].extend(
        [
            {**field("first_role"), "aggregation": "keep_equal"},
            {**field("second_role"), "aggregation": "keep_equal"},
        ]
    )
    first = raw["disturbance_types"][0]
    first["fields"].append("first_role")
    first["defaults"]["first_role"] = 11
    raw["disturbance_types"].append(
        {
            "name": "other_layout",
            "fields": ["quantity", "second_role"],
            "defaults": {"quantity": 3, "second_role": 22},
            "transport": {"mode": "hold"},
        }
    )
    raw["seeds"][1]["type"] = "other_layout"
    rule = raw["spatial_interactions"][0]
    rule["participants"] = [
        {"requires": ["quantity", "first_role"]},
        {"requires": ["quantity", "second_role"]},
    ]
    owners = [{"field": "quantity", "participant": i} for i in range(2)] + [local("quantity")]
    squares = [operation("mul", owner, owner) for owner in owners]
    rule["invariants"].append(
        invariant(
            "sum_of_individual_squares", operation("add", operation("add", *squares[:2]), squares[2])
        )
    )
    readout = raw["conservation_contract"]["quantities"][0]
    nonlinear = deepcopy(readout)
    nonlinear["name"] = "sum of individual squares"
    nonlinear["carriers"][0]["value"] = operation("mul", {"field": "quantity"}, {"field": "quantity"})
    nonlinear["spatial"] = operation("mul", local("quantity"), local("quantity"))
    raw["conservation_contract"]["quantities"].append(nonlinear)
    return raw


def test_distinct_layouts_and_field_rotate_from_one_snapshot_after_declared_k():
    initial = parse_initial_state(cross_layout_document())
    assert selected_types(initial.spatial_interactions[0]) == (0, 1)
    world = Simulation(initial)
    original = world.nodes[ORIGIN].records
    for tick in (1, 2):
        world.step()
        assert world.tick == tick
        assert world.nodes[ORIGIN].records == original
        assert quantities(world) == (5, 3) and value(world, "quantity") == (2,)
        guard = world.nodes[ORIGIN].pending.plan.spatial_guards[0]
        assert guard.slots == (0, 1)
        assert len(guard.participant_before) == len(guard.participant_after) == 2
        assert world.nodes[ORIGIN].pending.ready_tick == 3
    world.step()
    assert quantities(world) == (2, 5) and value(world, "quantity") == (3,)
    assert world.totals()["quantity"] == (10,)
    report = world.conservation_report()["node_contract"]["quantities"]
    assert tuple(row["value"] for row in report) == ((10,), (38,))
    records = world.nodes[ORIGIN].records
    assert world.record_values(records[0])["first_role"] == (11,)
    assert world.record_values(records[1])["second_role"] == (22,)


def test_false_first_group_is_not_reassigned_and_later_group_uses_disjoint_slots():
    raw = joint_document()
    raw["slots_per_node"] = 4
    raw["seeds"] = [{**raw["seeds"][0], "values": {"quantity": quantity}} for quantity in (1, 3, 5, 7)]
    raw["spatial_interactions"][0]["when"] = operation("gt", {"field": "quantity", "participant": 0}, 4)
    world = Simulation(parse_initial_state(raw))
    world.step()
    plan = world.nodes[ORIGIN].pending.plan
    assert plan.interaction_ticks == 3
    assert tuple(guard.slots for guard in plan.spatial_guards) == ((2, 3),)
    world.step()
    world.step()
    assert quantities(world) == (1, 3, 2, 5)
    assert value(world, "quantity") == (7,)


def test_greedy_selection_does_not_search_alternative_role_permutations():
    raw = cross_layout_document()
    raw["spatial_interactions"][0]["participants"] = [
        {"requires": ["quantity"]},
        {"requires": ["quantity", "first_role"]},
    ]
    initial = parse_initial_state(raw)
    records = tuple(seed.record for seed in initial.seeds)
    assert participant_groups(initial.spatial_interactions[0], records) == ()
    world = Simulation(initial)
    world.step()
    assert quantities(world) == (5, 3) and value(world, "quantity") == (2,)
    assert world.nodes[ORIGIN].pending is None


def test_false_commit_predicate_does_not_select_rule_or_reserve_duration():
    raw = joint_document()
    raw["spatial_interactions"][0]["commit_when"] = operation("gt", local("quantity"), 2)
    world = Simulation(parse_initial_state(raw))
    world.step()
    assert world.nodes[ORIGIN].pending is None
    assert quantities(world) == (5, 3) and value(world, "quantity") == (2,)


@pytest.mark.parametrize("persistent", [False, True])
@pytest.mark.parametrize("indexed", [False, True])
def test_arrival_can_invalidate_persistent_guard_but_not_a_start_only_trigger(persistent, indexed):
    raw = exchange(delayed=True, incoming=True)
    rule = raw["spatial_interactions"][0]
    rule["invariants"] = rule["invariants"][:1]
    rule["when"] = operation("eq", local("quantity"), 2)
    if persistent:
        rule["commit_when"] = deepcopy(rule["when"])
    if indexed:
        del rule["type"]
        rule["participants"] = [{"requires": ["quantity"]}] * 2
        raw["seeds"].append({**raw["seeds"][0], "values": {"quantity": 3}})
        rule["assignments"][0] = {"participant": 0, "field": "quantity", "expression": local("quantity")}
        rule["assignments"][1]["expression"] = {"field": "quantity", "participant": 0}
        total = operation(
            "add", {"field": "quantity", "participant": 0}, {"field": "quantity", "participant": 1}
        )
        rule["invariants"] = [invariant("all_owners", operation("add", total, local("quantity")))]
    world = Simulation(parse_initial_state(raw))
    world.step()
    pending = world.nodes[ORIGIN].pending
    assert pending is not None
    assert value(world, "quantity") == (3,)
    original = world.nodes[ORIGIN].records
    while world.tick < pending.ready_tick - 1:
        world.step()
    if persistent:
        with pytest.raises(ValueError, match="commit_when"):
            world.step()
        assert world.faulted and world.nodes[ORIGIN].records == original
        assert value(world, "quantity") == (3,)
        assert world.spatial_accounting()["quantity"]["reactions"] == (0,)
    else:
        world.step()
        assert carrier(world) == (2,)
        assert value(world, "quantity") == (6,)


def test_persistent_guard_validation_does_not_add_model_cost_or_duration():
    raw = joint_document()
    guarded = Simulation(parse_initial_state(raw))
    del raw["spatial_interactions"][0]["commit_when"]
    ordinary = Simulation(parse_initial_state(raw))
    for _ in range(3):
        ordinary.step()
        guarded.step()
        assert guarded.inventory_view() == ordinary.inventory_view()
        assert guarded.computation_report() == ordinary.computation_report()


def test_indexed_nonlinear_invariant_rechecks_each_owner_after_live_field_change():
    raw = exchange(delayed=True, incoming=True)
    raw["seeds"].append({**raw["seeds"][0], "values": {"quantity": 3}})
    rule = raw["spatial_interactions"][0]
    del rule["type"]
    rule["participants"] = [{"requires": ["quantity"]}] * 2
    owners = [{"field": "quantity", "participant": i} for i in range(2)] + [local("quantity")]
    rule["assignments"][0] = {"participant": 0, "field": "quantity", "expression": owners[2]}
    rule["assignments"][1]["expression"] = owners[0]
    squares = [operation("mul", owner, owner) for owner in owners]
    rule["invariants"] = [
        invariant("individual_squares", operation("add", operation("add", *squares[:2]), squares[2]))
    ]
    world = Simulation(parse_initial_state(raw))
    world.step()
    pending = world.nodes[ORIGIN].pending
    while world.tick < pending.ready_tick - 1:
        world.step()
    original = world.inventory_view()
    # Frozen swap 5,3,2 -> 2,3,5 was valid; live 5,3,3 -> 2,3,6 changes 43 to 49.
    with pytest.raises(ValueError, match="individual_squares"):
        world.step()
    assert world.faulted
    assert world.inventory_view() == original
    assert quantities(world) == (5, 3) and value(world, "quantity") == (3,)


@pytest.mark.parametrize("width", [3, 32])
def test_joint_vector_reaction_preserves_all_components_and_declared_width(width):
    raw = joint_document()
    raw["fields"][0]["components"] = width
    raw["fields"][0]["aggregation"] = "vector_sum"
    raw["disturbance_types"][0]["defaults"]["quantity"] = list(range(1, width + 1))
    raw["seeds"][1]["values"]["quantity"] = [7] * width
    raw["spatial_fields"][0]["baseline"] = [0] * width
    raw["spatial_seeds"][0]["populations"] = [[-3] * width] + [[0] * width] * 7
    raw["spatial_interactions"][0]["commit_when"] = 1
    raw["conservation_contract"]["quantities"][0]["components"] = width
    world = Simulation(parse_initial_state(raw))
    for _ in range(3):
        world.step()
    records = world.nodes[ORIGIN].records
    assert world.record_values(records[0])["quantity"] == (-3,) * width
    assert world.record_values(records[1])["quantity"] == tuple(range(1, width + 1))
    assert value(world, "quantity") == (7,) * width
    assert world.totals()["quantity"] == tuple(range(5, width + 5))


def test_all_configured_slots_can_participate_without_more_than_one_field_owner():
    raw = joint_document()
    count = 32
    raw["slots_per_node"] = count
    raw["seeds"] = [{**raw["seeds"][0], "values": {"quantity": index + 1}} for index in range(count)]
    rule = raw["spatial_interactions"][0]
    rule["participants"] = [{"requires": ["quantity"]}] * count
    references = [{"field": "quantity", "participant": i} for i in range(count)]
    rule["assignments"] = [
        {
            "participant": index,
            "field": "quantity",
            "expression": references[index + 1] if index + 1 < count else local("quantity"),
        }
        for index in range(count)
    ] + [{"side": "right", "field": "quantity", "expression": references[0]}]
    # Automatic conserved stock and the Node readout count all owners; no oversized expression tree.
    rule["invariants"] = [invariant("constant", 0)]
    world = Simulation(parse_initial_state(raw))
    for _ in range(3):
        world.step()
    assert quantities(world) == (*range(2, 33), 2)
    assert value(world, "quantity") == (1,)
    assert world.totals()["quantity"] == (530,)


@pytest.mark.parametrize("malformation", ["missing_lock", "repeated_slot", "missing_snapshot"])
def test_custom_pending_plan_cannot_omit_or_alias_a_guarded_participant(malformation):
    initial = parse_initial_state(joint_document())
    world = Simulation(initial)
    world.step()
    node = world.nodes[ORIGIN]
    plan = node.pending.plan
    guard = plan.spatial_guards[0]
    if malformation == "missing_lock":
        plan = replace(plan, replacements=plan.replacements[:1])
    elif malformation == "repeated_slot":
        plan = replace(plan, spatial_guards=(replace(guard, slots=(0, 0)),))
    else:
        plan = replace(plan, spatial_guards=(replace(guard, participant_after=()),))
    with pytest.raises(ValueError):
        validate_local_plan(initial, plan, len(node.coupling_remainders), node.records)
