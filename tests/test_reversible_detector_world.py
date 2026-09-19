"""Strict candidate configuration, independent of runtime detector behavior.

The published contract separates coverage, output grouping and trigger count.
One active owner fits 100 material Nodes; two active owners exceed a declared
bound of one. A group partitions its detector, has a unique measured output,
and fits its calibrated initial displacement within an explicit finite capacity.
Legacy worlds retain their defaults and preflight output.
"""

import json
from copy import deepcopy
from dataclasses import FrozenInstanceError

import pytest

from event_universe.configuration_validation import validate_configuration
from event_universe.events.world import (
    AMOUNT_BOUND,
    EVENTS_LAW,
    REVERSIBLE_DETECTOR_DYNAMICS,
    DetectorDefinition,
    parse_event_world,
)


def candidate(coverage=3, threshold=1):
    positions = [[x, 0, 0] for x in range(1, coverage + 1)]
    return {
        "law": "events",
        "dynamics": REVERSIBLE_DETECTOR_DYNAMICS,
        "max_active_owners": 1,
        "model_id": "detector-schema-test",
        "shape": [coverage + 2, 1, 1],
        "ticks": 1,
        "K": 32,
        "N": 32,
        "release": 0,
        "suspension": 0,
        "families": [{"name": "carrier", "kind": "paid"}],
        "measured": [
            {
                "position": position,
                "family": "carrier",
                "amount": 1,
                "fixed": True,
                "table": {"carrier": "transduce"},
                "port_map": [0, 1, 2, 3, 4, 5],
            }
            for position in positions
        ],
        "in_transit": [
            {
                "position": [0, 0, 0],
                "family": "carrier",
                "number": 1,
                "heading": [1, 0, 0],
                "amount": 1,
                "phase": 16,
            }
        ],
        "detectors": [
            {
                "name": "apparatus",
                "positions": positions,
                "groups": [
                    {
                        "name": "shared",
                        "positions": positions,
                        "output": positions[-1],
                        "threshold": threshold,
                        "capacity": 31,
                        "reference_phase": 0,
                    }
                ],
            }
        ],
    }


def legacy():
    document = candidate(1)
    del document["dynamics"], document["max_active_owners"]
    document["measured"][0].pop("port_map")
    document["measured"][0].pop("table")
    document["detectors"][0].pop("groups")
    return document


@pytest.mark.parametrize("coverage,threshold", [(1, 1), (1, 2), (3, 1), (100, 2)])
def test_coverage_does_not_set_trigger_or_active_owner_count(coverage, threshold):
    world = parse_event_world(candidate(coverage, threshold))
    assert world.dynamics == REVERSIBLE_DETECTOR_DYNAMICS
    assert world.max_active_owners == 1 and world.owners(0) == (1,)
    detector = world.detectors[0]
    assert len(detector.positions) == coverage and len(detector.groups) == 1
    group = detector.groups[0]
    assert group.positions == detector.positions
    assert group.output == (coverage, 0, 0)
    assert (group.threshold, group.capacity, group.reference_phase) == (threshold, 31, 0)
    with pytest.raises(FrozenInstanceError):
        group.capacity = 2


def test_separate_groups_define_distinguishable_outputs_without_extra_owners():
    document = candidate(3)
    detector = document["detectors"][0]
    shared = detector["groups"][0]
    detector["groups"] = [
        {**shared, "name": str(index), "positions": [position], "output": position}
        for index, position in enumerate(detector["positions"])
    ]
    world = parse_event_world(document)
    assert [group.output for group in world.detectors[0].groups] == [(1, 0, 0), (2, 0, 0), (3, 0, 0)]
    assert world.owners(0) == (1,)


def test_output_can_be_another_material_node_and_keeps_fixed_calibration():
    document = candidate(3)
    detector = document["detectors"][0]
    detector["positions"] = [[1, 0, 0]]
    group = detector["groups"][0]
    group.update(positions=[[1, 0, 0]], capacity=3, reference_phase=4)
    document["measured"][-1]["phase"] = 6
    world = parse_event_world(document)
    assert world.detectors[0].groups[0].reference_phase == 4
    assert world.measured[-1].phase == 6
    document["measured"][-1]["phase"] = 8
    with pytest.raises(ValueError, match="initial displacement"):
        parse_event_world(document)


@pytest.mark.parametrize(
    "path,value,match",
    [
        (("dynamics",), "unrecognized", "dynamics"),
        (("max_active_owners",), True, "max_active_owners"),
        (("max_active_owners",), 17, "max_active_owners"),
        (("release",), 1, "release"),
        (("suspension",), 1, "suspension"),
        (("families", 0, "kind"), "free", "paid families"),
        (("measured", 0, "fixed"), False, "fixed"),
        (("measured", 0, "lamp"), {"rate": 0}, "lamp"),
        (("measured", 0, "table"), {}, "every family"),
        (("measured", 0, "table", "carrier"), "measure", "transduce"),
        (("measured", 0, "table", "carrier"), {"rule": "transduce", "phase_window": 0}, "phase_window"),
        (("measured", 0, "port_map"), [0, 0, 2, 3, 4, 5], "permutation"),
        (("measured", 0, "port_map"), [0, True, 2, 3, 4, 5], "port_map"),
        (("measured", 0, "port_map"), [0, 1], "six Port"),
        (("in_transit", 0, "heading"), [True, 0, 0], "heading"),
        (("detectors", 0, "threshold"), 1, "threshold"),
        (("detectors", 0, "groups"), [], "nonempty"),
        (("detectors", 0, "groups", 0, "capacity"), 32, "capacity"),
        (("detectors", 0, "groups", 0, "threshold"), 32, "threshold"),
        (("detectors", 0, "groups", 0, "threshold"), True, "threshold"),
        (("detectors", 0, "groups", 0, "reference_phase"), 32, "reference_phase"),
        (("detectors", 0, "groups", 0, "output"), [0, 0, 0], "output"),
        (("detectors", 0, "groups", 0, "positions"), [[1, 0, 0]], "partition"),
        (("detectors", 0, "positions"), [[1, 0, 0], [1, 0, 0]], "repeats a Node"),
    ],
)
def test_unsupported_inputs_are_rejected_by_the_named_schema_field(path, value, match):
    document = candidate()
    target = document
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    with pytest.raises(ValueError, match=match):
        parse_event_world(document)


@pytest.mark.parametrize("key", ["max_active_owners", "port_map", "reference_phase"])
def test_required_candidate_fields_have_no_implicit_defaults(key):
    document = candidate()
    target = document
    if key == "port_map":
        target = document["measured"][0]
    elif key == "reference_phase":
        target = document["detectors"][0]["groups"][0]
    del target[key]
    with pytest.raises(ValueError, match=key):
        parse_event_world(document)


def test_group_membership_and_output_ownership_cannot_overlap():
    document = candidate(3)
    detector = document["detectors"][0]
    first = detector["groups"][0]
    first["positions"] = [[1, 0, 0]]
    second = {**first, "name": "second", "positions": [[2, 0, 0], [3, 0, 0]]}
    detector["groups"].append(second)
    with pytest.raises(ValueError, match="output"):
        parse_event_world(document)
    second["output"] = [2, 0, 0]
    second["positions"].append([1, 0, 0])
    with pytest.raises(ValueError, match="partition"):
        parse_event_world(document)


def test_active_owner_bound_counts_carriers_and_initial_slots_cannot_merge():
    document = candidate(3)
    duplicate = deepcopy(document["in_transit"][0])
    document["in_transit"].append(duplicate)
    with pytest.raises(ValueError, match="occupied initial slot"):
        parse_event_world(document)
    duplicate["number"] = 2
    with pytest.raises(ValueError, match="max_active_owners"):
        parse_event_world(document)
    document["max_active_owners"] = 2
    assert parse_event_world(document).owners(0) == (1, 2)


def test_candidate_family_limit_is_independent_of_material_coverage():
    document = candidate(1)
    document["families"] = [{"name": str(index), "kind": "paid"} for index in range(9)]
    with pytest.raises(ValueError, match="at most 8"):
        parse_event_world(document)


def test_initial_amount_and_momentum_products_have_checked_bounds():
    document = candidate(1)
    document["in_transit"][0]["amount"] = AMOUNT_BOUND
    document["families"][0]["quantum"] = 2
    with pytest.raises(ValueError, match="momentum bound"):
        parse_event_world(document)
    document["families"][0]["quantum"] = 3
    with pytest.raises(OverflowError, match="64-bit"):
        parse_event_world(document)
    document["families"][0]["quantum"] = 1
    extra = {**document["in_transit"][0], "amount": 1, "heading": [-1, 0, 0]}
    document["in_transit"].append(extra)
    with pytest.raises(ValueError, match="per-Node amount"):
        parse_event_world(document)
    document = candidate(1)
    document["K"] = AMOUNT_BOUND
    with pytest.raises(OverflowError, match="64-bit"):
        parse_event_world(document)


def test_pass_is_explicit_and_does_not_need_a_scattering_map():
    document = candidate(1)
    document["measured"][0]["table"] = {"carrier": "pass"}
    document["measured"][0].pop("port_map")
    definition = parse_event_world(document).measured[0]
    assert definition.table == ("pass",) and definition.port_map == ()


def test_legacy_defaults_and_summary_are_unchanged_and_candidate_preflight_is_identified():
    document = legacy()
    world = parse_event_world(document)
    assert world.dynamics == EVENTS_LAW and world.max_active_owners == 0
    assert world.measured[0].table == ("measure",) and world.measured[0].port_map == ()
    assert world.detectors[0] == DetectorDefinition("apparatus", ((1, 0, 0),), 1)
    report = validate_configuration(json.dumps(document))
    assert report.valid and report.summary == {
        "model": "detector-schema-test",
        "law": EVENTS_LAW,
        "shape": (3, 1, 1),
        "ticks": 1,
        "families": 1,
        "measured": 1,
        "detectors": 1,
    }
    report = validate_configuration(json.dumps(candidate(100)))
    assert report.valid and report.summary["dynamics"] == REVERSIBLE_DETECTOR_DYNAMICS


@pytest.mark.parametrize("field", ["max_active_owners", "groups", "port_map", "transduce"])
def test_candidate_only_fields_and_rules_are_refused_by_legacy_worlds(field):
    document = legacy()
    if field == "max_active_owners":
        document[field] = 1
    elif field == "groups":
        document["detectors"][0][field] = []
    elif field == "port_map":
        document["measured"][0][field] = [0, 1, 2, 3, 4, 5]
    else:
        document["measured"][0]["table"] = {"carrier": "transduce"}
    with pytest.raises(ValueError, match="one of" if field == "transduce" else field):
        parse_event_world(document)
