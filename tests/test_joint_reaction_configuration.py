"""Reject ambiguous roles and transient commit guards before creating a world."""

from copy import deepcopy

import pytest

from event_universe.initialization import parse_initial_state

from .test_local_field_rules import invariant, local, operation
from .test_node_rule_contract import node_profile
from .test_spatial_interactions import exchange


def joint_document():
    raw = node_profile(exchange())
    raw["slots_per_node"] = 2
    raw["seeds"].append({**raw["seeds"][0], "values": {"quantity": 3}})
    references = [{"field": "quantity", "participant": i} for i in range(2)]
    raw["spatial_interactions"] = [
        {
            "name": "three owner rotation",
            "participants": [{"requires": ["quantity"]}] * 2,
            "k": 3,
            "commit_when": operation("gt", local("quantity"), 0),
            "assignments": [
                {"participant": 0, "field": "quantity", "expression": local("quantity")},
                {"participant": 1, "field": "quantity", "expression": references[0]},
                {"side": "right", "field": "quantity", "expression": references[1]},
            ],
            "invariants": [
                invariant("stock", operation("add", operation("add", *references), local("quantity")))
            ],
        }
    ]
    return raw


def test_indexed_spatial_references_have_distinct_carrier_and_field_owners():
    initial = parse_initial_state(joint_document())
    rule = initial.spatial_interactions[0]
    assert rule.participants == ((0,), (0,))
    assert [item.side for item in rule.assignments] == [0, 1, 2]
    assert [item.expression.side for item in rule.assignments] == [2, 0, 1]
    assert rule.commit_when.arguments[0].side == 2
    assert rule.k == 3


@pytest.mark.parametrize("target", ["when", "assignment", "invariant", "commit_when"])
def test_indexed_rule_rejects_ambiguous_legacy_left_references(target):
    raw = joint_document()
    rule = raw["spatial_interactions"][0]
    reference = {"field": "quantity", "side": "left"}
    if target == "assignment":
        rule["assignments"][0]["expression"] = reference
    elif target == "invariant":
        rule["invariants"][0]["expression"] = reference
    else:
        rule[target] = reference
    with pytest.raises(ValueError, match="explicit participant"):
        parse_initial_state(raw)


@pytest.mark.parametrize("key", ["type", "requires"])
def test_indexed_rule_rejects_mixed_selection_syntax(key):
    raw = joint_document()
    raw["spatial_interactions"][0][key] = "held" if key == "type" else ["quantity"]
    with pytest.raises(ValueError, match="mix"):
        parse_initial_state(raw)


@pytest.mark.parametrize("count", [0, 1, 3, 33])
def test_participant_count_must_fit_declared_local_capacity(count):
    raw = joint_document()
    raw["spatial_interactions"][0]["participants"] = [{"requires": ["quantity"]}] * count
    with pytest.raises(ValueError, match="participants|participant count"):
        parse_initial_state(raw)


@pytest.mark.parametrize("key", ["received", "received_present", "flux", "outgoing"])
@pytest.mark.parametrize("indexed", [False, True])
def test_commit_guard_cannot_read_transient_input_or_proposed_output(key, indexed):
    raw = joint_document() if indexed else node_profile(exchange())
    rule = raw["spatial_interactions"][0]
    rule["k"] = 2
    rule["commit_when"] = {key: "quantity", **({"port": 0} if key != "flux" else {})}
    with pytest.raises(ValueError):
        parse_initial_state(raw)


@pytest.mark.parametrize("reference", [{"participant": 2}, {"participant": True}, {"side": "left"}])
def test_assignment_rejects_invalid_or_ambiguous_owner(reference):
    raw = joint_document()
    raw["spatial_interactions"][0]["assignments"][0] = {
        **reference,
        "field": "quantity",
        "expression": 0,
    }
    with pytest.raises(ValueError):
        parse_initial_state(raw)


def test_repeated_target_rejected_even_when_other_owners_are_valid():
    raw = joint_document()
    rule = raw["spatial_interactions"][0]
    rule["assignments"].append(deepcopy(rule["assignments"][0]))
    with pytest.raises(ValueError, match="duplicate"):
        parse_initial_state(raw)
