"""Delayed field transactions keep their declared conditions on actual local stock."""

from copy import deepcopy
from dataclasses import replace

import pytest

from event_universe import Simulation
from event_universe.core.disturbance_state import (
    MAX_EXPRESSION_NODES,
    MAX_RULES,
    MAX_VALUE,
    Expression,
    Invariant,
    pack,
)
from event_universe.core.spatial_engine import SpatialEngine
from event_universe.core.spatial_state import SpatialPacket
from event_universe.initialization import parse_initial_state

from .test_local_field_rules import ORIGIN, document, field, invariant, local, operation, seed, value
from .test_node_rule_contract import node_profile
from .test_node_runtime import delayed_field_document


def rotating_document(incoming=(1, 0, 0), *, double=False):
    raw = node_profile(
        document(
            [field("quantity", 3)],
            [seed("quantity", [3, 4, 0]), seed("quantity", list(incoming), (1, 2, 2))],
        )
    )
    spatial = local("quantity")
    quantity = raw["conservation_contract"]["quantities"][0]
    quantity["components"] = 1
    quantity["carriers"][0]["value"] = operation("sum", {"field": "quantity"})
    quantity["spatial"] = operation("sum", spatial)
    rotate = {
        "name": "swap axes",
        "k": 2 if double else 3,
        "when": operation("gt", operation("sum", spatial), 2),
        "assignments": [
            {
                "field": "quantity",
                "expression": {
                    "op": "transform",
                    "args": [spatial],
                    "matrix": [[0, 1, 0], [1, 0, 0], [0, 0, 1]],
                },
            }
        ],
        "invariants": [invariant("squared length", operation("dot", spatial, spatial))],
    }
    raw["field_rules"] = [rotate]
    if double:
        raw["field_rules"].append({**deepcopy(rotate), "name": "swap back", "k": 1})
    raw["field_rules"].append(
        {
            "name": "deliver small vector",
            "k": 1,
            "when": operation("gt", 3, operation("sum", spatial)),
            "assignments": [
                {"field": "quantity", "expression": [0, 0, 0]},
                {"field": "quantity", "port": 0, "expression": spatial},
            ],
            "invariants": [
                invariant("stock", operation("add", spatial, {"outgoing": "quantity", "port": 0}))
            ],
        }
    )
    return raw


@pytest.mark.parametrize("double", [False, True])
def test_arrival_cannot_invalidate_any_frozen_field_rule_invariant(double):
    events = []
    world = Simulation(parse_initial_state(rotating_document(double=double)), observer=events.append)
    world.step()
    world.step()
    node = world._spatial.nodes[ORIGIN]
    pending, states, links = node.pending, node.states, node.output.packets
    accounting = world.spatial_accounting()
    assert pending.ready_tick == 3
    assert value(world, "quantity") == (4, 4, 0)
    events.clear()
    # A swap's frozen delta would change squared length 32 to 34. With two
    # swaps the final delta is zero, but the first substep must still be valid.
    with pytest.raises(ValueError, match="field rule swap axes.*squared length"):
        world.step()
    assert world.faulted
    assert node.pending is pending
    assert node.states == states
    assert node.output.packets == links
    assert world.spatial_accounting() == accounting
    assert events == []


def test_valid_arrival_preserves_frozen_field_delta_and_declared_duration():
    world = Simulation(parse_initial_state(rotating_document((1, 1, 0))))
    world.step()
    world.step()
    node = world._spatial.nodes[ORIGIN]
    assert node.pending.ready_tick == 3
    assert value(world, "quantity") == (4, 5, 0)
    assert sum(v * v for v in value(world, "quantity")) == 41
    world.step()
    assert not world.faulted
    assert value(world, "quantity") == (5, 4, 0)
    assert sum(v * v for v in value(world, "quantity")) == 41
    assert node.pending is None
    assert node.states[0].received_mask == 1


def test_persistent_condition_invalidated_during_wait_rejects_before_owner_changes():
    raw = rotating_document((1, 1, 0))
    raw["field_rules"][0]["commit_when"] = operation("eq", operation("sum", local("quantity")), 7)
    world = Simulation(parse_initial_state(raw))
    world.step()
    world.step()
    node = world._spatial.nodes[ORIGIN]
    pending, states, links = node.pending, node.states, node.output.packets
    # The norm invariant still holds for this arrival; only the explicit
    # persistent condition invalidates the transaction.
    with pytest.raises(ValueError, match="field rule swap axes.*commit_when"):
        world.step()
    assert node.pending is pending
    assert node.states == states
    assert node.output.packets == links
    assert node.states[0].received_mask == 1


@pytest.mark.parametrize("condition", [0, -1])
def test_persistent_condition_must_be_positive_before_selecting_a_rule(condition):
    raw = rotating_document()
    raw["spatial_seeds"] = raw["spatial_seeds"][:1]
    raw["field_rules"][0]["commit_when"] = condition
    world = Simulation(parse_initial_state(raw))
    world.step()
    node = world._spatial.nodes[ORIGIN]
    assert node.pending is None
    assert value(world, "quantity") == (3, 4, 0)
    assert node.delay_counts == (0,) * 6


def test_each_persistent_condition_reads_its_own_rebased_substep():
    raw = rotating_document((1, 1, 0), double=True)
    # First swap changes the first component from 3 to 4 while planning.
    raw["field_rules"][1]["commit_when"] = operation(
        "eq", {"op": "component", "args": [local("quantity")], "index": 0}, 4
    )
    world = Simulation(parse_initial_state(raw))
    world.step()
    world.step()
    node = world._spatial.nodes[ORIGIN]
    before = node.states
    # Live input (4,5,0) passes through the first frozen delta to (5,4,0).
    # Checking every guard against the initial live view would incorrectly pass.
    with pytest.raises(ValueError, match="field rule swap back.*commit_when"):
        world.step()
    assert node.states == before


def test_consumed_start_trigger_is_not_rechecked_or_used_to_replay_assignments():
    raw = delayed_field_document()
    rule = raw["field_rules"][0]
    rule["when"] = operation("eq", local("quantity"), 8)
    rule["commit_when"] = operation("gt", local("quantity"), 0)
    world = Simulation(parse_initial_state(raw))
    world.step()
    engine = world._spatial
    node = engine.nodes[ORIGIN]
    population = (pack((5,)),) + (pack((0,)),) * 7
    node.receive((SpatialPacket(1, (1, 2, 2), 0, (population,)),), 1, engine._services)
    cost, ready = node.pending.cost, node.pending.ready_tick
    node.commit_ready(2, None, engine._services)
    assert ready == 2
    assert value(world, "quantity") == (5,)
    assert node.output.packets[0].fields[0][0] == pack((8,))
    assert node.last_cost == cost
    assert node.states[0].delivered[0] == pack((5,))


@pytest.mark.parametrize("boundary", ["engine", "services"])
def test_custom_field_assembly_cannot_omit_required_commit_validation(boundary):
    initial = parse_initial_state(delayed_field_document())
    world = Simulation(initial)
    services = world._spatial._services
    with pytest.raises(ValueError, match="field rules require a field commit guard"):
        if boundary == "services":
            replace(services, field_guard=None)
        else:
            SpatialEngine(initial, services.planner, None, balance_guard=services.balance_guard)


@pytest.mark.parametrize(
    "failure", ["capacity", "duplicate", "channels", "delta", "proposal", "outgoing", "populations"]
)
def test_field_guard_metadata_is_bounded_and_matches_the_frozen_proposal(failure):
    world = Simulation(parse_initial_state(delayed_field_document()))
    world.step()
    node = world._spatial.nodes[ORIGIN]
    pending = node.pending
    plan = pending.plan
    guard = plan.field_guards[0]
    if failure == "capacity":
        plan = replace(plan, field_guards=(guard,) * (MAX_RULES + 1))
    elif failure == "duplicate":
        plan = replace(plan, field_guards=(guard, guard))
    elif failure == "channels":
        plan = replace(plan, field_guards=(replace(guard, outgoing=guard.outgoing[:5]),))
    elif failure == "delta":
        plan = replace(plan, field_guards=(replace(guard, delta=()),))
    elif failure == "outgoing":
        plan = replace(plan, outgoing=plan.outgoing * 2)
    elif failure == "populations":
        plan = replace(plan, outgoing=((plan.outgoing[0][0] * 2,),) + plan.outgoing[1:])
    else:
        plan = replace(plan, states=pending.before)
    before = node.states
    with pytest.raises(ValueError, match="field guard"):
        world._spatial._services.field_guard(pending.before, plan)
    assert node.states == before
    assert node.pending is pending


@pytest.mark.parametrize("persistent", [False, True])
def test_direct_guard_assembly_rejects_transient_inputs(persistent):
    world = Simulation(parse_initial_state(delayed_field_document()))
    law = world._spatial.planner
    rule = law.field_rules[0]
    expression = Expression("received", field=0, port=0)
    altered = replace(
        rule,
        commit_when=expression if persistent else None,
        invariants=rule.invariants if persistent else (Invariant("transient", expression),),
    )
    law = replace(law, field_rules=(altered,))
    with pytest.raises(ValueError, match="field guard cannot read transient"):
        law(world._spatial.nodes[ORIGIN].states, (), 0)


def test_frozen_difference_uses_a_work_integer_without_narrowing_valid_payloads():
    raw = node_profile(document([field("quantity")], [seed("quantity", MAX_VALUE)]))
    spatial = local("quantity")
    quantity = raw["conservation_contract"]["quantities"][0]
    quantity["carriers"][0]["value"] = operation("mul", {"field": "quantity"}, {"field": "quantity"})
    quantity["spatial"] = operation("mul", spatial, spatial)
    raw["field_rules"] = [
        {
            "name": "reverse sign",
            "k": 2,
            "assignments": [{"field": "quantity", "expression": operation("neg", spatial)}],
            "invariants": [invariant("squared amount", operation("mul", spatial, spatial))],
        }
    ]
    raw["field_rules"].append({**deepcopy(raw["field_rules"][0]), "name": "restore sign", "k": 1})
    world = Simulation(parse_initial_state(raw))
    world.step()
    node = world._spatial.nodes[ORIGIN]
    assert node.pending.plan.field_guards[0].delta == ((-2 * MAX_VALUE,),)
    assert node.pending.plan.field_guards[1].delta == ((2 * MAX_VALUE,),)
    world.step()
    world.step()
    assert value(world, "quantity") == (MAX_VALUE,)
    assert not world.faulted


def test_direct_persistent_expression_rejects_excess_arguments_before_traversal():
    world = Simulation(parse_initial_state(delayed_field_document()))
    law = world._spatial.planner
    expression = Expression(
        "add", arguments=(Expression("literal", literal=(1,)),) * (MAX_EXPRESSION_NODES + 1)
    )
    law = replace(law, field_rules=(replace(law.field_rules[0], commit_when=expression),))
    with pytest.raises(ValueError, match="field guard expression exceeds"):
        law(world._spatial.nodes[ORIGIN].states, (), 0)
