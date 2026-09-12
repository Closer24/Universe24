"""Executable coverage and honest boundaries for catalog representation probes."""

import copy
import json
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.entities import compile_entities
from event_universe.initialization import parse_initial_state

CATALOG = Path(__file__).resolve().parents[1] / "examples/known-entities/catalog.json"


def catalog():
    return json.loads(CATALOG.read_text())


def test_every_catalog_entry_has_a_valid_explicit_executable_profile():
    data = catalog()
    rows = data["field_entities"] + data["particle_entities"]
    assert len(rows) == 46
    for row in rows:
        compiled = compile_entities(data, [row["id"]])
        parsed = parse_initial_state(compiled)
        assert parsed.seeds or parsed.spatial_seeds
        assert row["emergence_status"] == "not_established"
        assert row["missing_capabilities"]
        if row["executable_profile"]["kind"] == "carrier":
            assert "mass" not in row["executable_profile"]["seed_values"]
        for rule in compiled["field_rules"]:
            for assignment in rule["assignments"]:
                assert assignment["expression"] in (0, [0, 0, 0]) or assignment["expression"] == {
                    "field": assignment["field"],
                    "side": "right",
                }


def test_composed_carriers_and_vector_field_keep_distinct_causal_owners():
    raw = compile_entities(catalog(), ["electron", "positron", "electromagnetic_field"], link_ticks=2)
    events = []
    world = Simulation(parse_initial_state(raw), observer=events.append)
    for _ in range(4):
        world.step()
        assert world.totals()["inventory"] == (2,)
        assert world.totals()["charge"] == (0,)
        assert world.totals()["momentum"] == (2, 0, 0)
        for balance in world.spatial_accounting().values():
            assert balance["balanced"]
            assert balance["current"] == (0, 1, 0)
    sent = [event for event in events if event["event"] in ("sent", "spatial_sent")]
    assert sent and all(event["arrival_tick"] - event["tick"] == 2 for event in sent)
    nodes = world.snapshot()["spatial_fields"]
    assert any(node["position"] == (4, 4, 4) for node in nodes)
    assert all(event["port"] == 0 for event in sent)


def test_multi_scalar_profile_moves_actual_nonzero_registers():
    raw = compile_entities(catalog(), ["higgs_field"])
    world = Simulation(parse_initial_state(raw))
    world.step()
    world.step()
    assert len(world.spatial_accounting()) == 4
    assert all(
        balance["current"] == (1,) and balance["balanced"]
        for balance in world.spatial_accounting().values()
    )
    assert any(node["position"] == (4, 4, 4) for node in world.snapshot()["spatial_fields"])


def test_renaming_and_reordering_catalog_does_not_select_a_law():
    data = catalog()
    raw = compile_entities(data, ["electron"])
    changed = copy.deepcopy(data)
    entry = next(row for row in changed["particle_entities"] if row["id"] == "electron")
    entry["id"] = "__proto__"
    entry["label"] = "arbitrary name"
    changed["particle_entities"].reverse()
    renamed = compile_entities(changed, ["__proto__"])
    assert raw == renamed
    changed["particle_entities"].append(copy.deepcopy(entry))
    with pytest.raises(ValueError, match="unique"):
        compile_entities(changed, ["__proto__"])


def test_invalid_profile_and_capacity_fail_before_execution():
    data = catalog()
    with pytest.raises(ValueError, match="disturbance_types"):
        compile_entities(data, [row["id"] for row in data["particle_entities"]])
    with pytest.raises(ValueError, match="fields"):
        compile_entities(data, [row["id"] for row in data["field_entities"]])
    with pytest.raises(ValueError, match="unknown entity"):
        compile_entities(data, ["missing"])
    with pytest.raises(ValueError, match="duplicates"):
        compile_entities(data, ["electron", "electron"])
    electron = next(row for row in data["particle_entities"] if row["id"] == "electron")
    electron["executable_profile"]["seed_values"]["inventory"] = 1.5
    with pytest.raises(ValueError, match="integer"):
        compile_entities(data, ["electron"])
    electron["executable_profile"]["seed_values"]["inventory"] = 1
    electron["executable_profile"]["unexpected_law"] = "annihilate"
    with pytest.raises(ValueError, match="unsupported"):
        compile_entities(data, ["electron"])
    del electron["executable_profile"]["unexpected_law"]
    electron["executable_profile"]["assumptions"] = [False]
    with pytest.raises(ValueError, match="assumptions"):
        compile_entities(data, ["electron"])


def test_shared_field_conflicts_and_duplicate_spatial_ownership_are_rejected():
    data = catalog()
    positron = next(row for row in data["particle_entities"] if row["id"] == "positron")
    positron["executable_profile"]["fields"][0]["units"] = "incompatible"
    with pytest.raises(ValueError, match="incompatible shared field"):
        compile_entities(data, ["electron", "positron"])
    duplicate = copy.deepcopy(data["field_entities"][0])
    duplicate["id"] = "duplicate spatial owner"
    data["field_entities"].append(duplicate)
    with pytest.raises(ValueError, match="distinct ownership"):
        compile_entities(data, [data["field_entities"][0]["id"], duplicate["id"]])
