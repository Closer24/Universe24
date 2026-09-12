import copy
import json
from pathlib import Path

import pytest

from .algebra import literal
from .runtime import Lab
from .test_lab import state, values


@pytest.fixture
def lab():
    return Lab(json.loads(Path(__file__).with_name("definitions.json").read_text(encoding="utf-8")))


def populate(engine):
    return [
        engine.insert(0, engine.record(p["type"], p["fields"]))
        for p in engine.definitions["node_demo"]["participants"]
    ]


def test_six_way_node_transaction(lab):
    ids = populate(lab)
    before = lab.totals()
    products = lab.react(0, "six_node_exchange", list(reversed(ids)))
    assert len(products) == 6 and lab.totals() == before
    assert before["E"] == literal(3, [2, 0])
    assert before["p"] == literal([0, 0, 0], [2, 0])
    assert values(lab, products[0], "p") == literal([0, 1, 0], [2, 0])
    assert values(lab, products[2], "p") == literal([0, 0, 1], [2, 0])
    assert values(lab, products[4], "p") == literal([1, 0, 0], [2, 0])
    assert not set(ids).intersection(products)


def test_wrong_six_type_composition_rolls_back(lab):
    lab.definitions["node_demo"]["participants"][-1]["type"] = "disturbance_A"
    ids = populate(lab)
    before = state(lab)
    with pytest.raises(ValueError, match="No allowed participant combination"):
        lab.react(0, "six_node_exchange", ids)
    assert state(lab) == before


@pytest.mark.parametrize("setting", ["max_participants", "max_products"])
def test_configured_limit_rejects_oversized_rule(lab, setting):
    lab.definitions["limits"][setting] = 5
    with pytest.raises(ValueError, match="configured"):
        Lab(lab.definitions)


@pytest.mark.parametrize("value", [0, -1, True, 1.5])
def test_invalid_limits(lab, value):
    lab.definitions["limits"]["cell_capacity"] = value
    with pytest.raises(ValueError):
        Lab(lab.definitions)


def test_more_than_sixteen_is_configuration_only(lab):
    definitions = copy.deepcopy(lab.definitions)
    definitions["limits"].update(cell_capacity=17, max_participants=17, max_products=17)
    rule = {"inputs": [], "outputs": []}
    for i in range(17):
        alias = f"r{i}"
        rule["inputs"].append({"alias": alias, "types": ["classical"]})
        rule["outputs"].append(
            {
                "type": "classical",
                "fields": {name: {"ref": alias + "." + name} for name in ["mass", "p", "q"]},
            }
        )
    definitions["reactions"]["seventeen_identity"] = rule
    engine = Lab(definitions)
    ids = [
        engine.insert(0, engine.record("classical", {"mass": 1, "p": [1, 0, 0], "q": 0}))
        for _ in range(17)
    ]
    before = engine.totals()
    assert len(engine.react(0, "seventeen_identity", ids)) == 17
    assert engine.totals() == before


def test_matching_budget_failure_is_atomic(lab):
    ids = populate(lab)
    lab.definitions["limits"]["match_attempts"] = 1
    before = state(lab)
    with pytest.raises(ValueError, match="matching work budget"):
        lab.react(0, "six_node_exchange", ids)
    assert state(lab) == before


def test_rule_predicate_can_filter_properties(lab):
    ids = populate(lab)
    lab.definitions["reactions"]["six_node_exchange"]["when"] = {
        "op": "gt",
        "args": [{"ref": "a.q"}, {"value": 0, "unit": "charge"}],
    }
    before = state(lab)
    with pytest.raises(ValueError, match="condition"):
        lab.react(0, "six_node_exchange", ids)
    assert state(lab) == before


def test_backtracking_binds_overlapping_type_sets(lab):
    rule = {
        "inputs": [
            {"alias": "a", "types": ["electron", "positron"]},
            {"alias": "b", "types": ["electron"]},
        ],
        "outputs": copy.deepcopy(lab.definitions["reactions"]["annihilate"]["outputs"]),
    }
    lab.definitions["reactions"]["overlap"] = rule
    ids = [
        lab.insert(0, lab.record(kind, {"mass": 1, "E": 1, "p": [0, 0, 0], "q": q}))
        for kind, q in [("electron", -1), ("positron", 1)]
    ]
    before = lab.totals()
    lab.react(0, "overlap", ids)
    assert lab.totals() == before


def test_missing_rule_and_missing_explicit_type_list(lab):
    ids = populate(lab)
    before = state(lab)
    with pytest.raises(KeyError):
        lab.react(0, "not_configured", ids)
    assert state(lab) == before
    lab.definitions["reactions"]["six_node_exchange"]["inputs"][0]["types"] = []
    with pytest.raises(ValueError, match="explicitly"):
        Lab(lab.definitions)
