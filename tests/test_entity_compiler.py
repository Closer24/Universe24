"""Executable coverage and honest boundaries for catalog representation probes."""

import copy
import json
import sys
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.entities import compile_entities, main
from event_universe.initialization import parse_initial_state

CATALOG = Path(__file__).resolve().parents[1] / "examples/known-entities/catalog.json"


def physical_catalog():
    return json.loads(CATALOG.read_text())


def profiles():
    return json.loads(CATALOG.with_name("representation-probes.json").read_text())


def catalog():
    """Legacy embedded authoring fixture assembled from the canonical experiments."""
    data = physical_catalog()
    data["catalog_version"] = 1
    experiments = {row["entity_id"]: row for row in profiles()["profiles"]}
    for entry in data["field_entities"] + data["particle_entities"]:
        entry.update(
            {key: value for key, value in experiments[entry["id"]].items() if key != "entity_id"}
        )
    return data


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


@pytest.mark.parametrize("representation", ["classical", "quantum"])
def test_v2_metadata_and_profile_order_cannot_select_or_modify_a_law(representation):
    data = physical_catalog()
    experiments = profiles()
    selected = ["electron", "electromagnetic_field"]
    original = compile_entities(data, selected, profiles=experiments, representation=representation)
    changed = copy.deepcopy(data)
    for section in ("field_entities", "particle_entities", "disturbance_families"):
        changed[section].reverse()
        for row in changed[section]:
            row["label"] = "Arbitrary descriptive label"
            # Synthetic, internally consistent metadata must not configure dynamics.
            if "electric_charge_thirds" in row:
                row["electric_charge_thirds"] *= 2
            if "twice_spin" in row:
                row["twice_spin"] += 2
            for prop in row["physical_properties"].values():
                if "value_decimal" in prop:
                    prop["value_decimal"] = "123456789"
            row["physical_properties"]["description_probe"] = {
                "status": "hypothetical",
                "description": "Descriptive reference text cannot configure an update.",
                "sources": row["sources"],
            }
    for row in changed["representative_channels"]:
        row["conditions"] = ["A different descriptive condition for this reference channel."]
    changed["representative_channels"].reverse()
    experiments["profiles"].reverse()
    assert (
        compile_entities(changed, selected, profiles=experiments, representation=representation)
        == original
    )


def replace_identity(value, previous, identity):
    """Rename exact identity references while retaining metadata consistency."""
    if isinstance(value, dict):
        return {key: replace_identity(item, previous, identity) for key, item in value.items()}
    if isinstance(value, list):
        return [replace_identity(item, previous, identity) for item in value]
    return identity if value == previous else value


@pytest.mark.parametrize("representation", ["classical", "quantum"])
def test_v2_arbitrary_ids_only_bind_profiles(representation):
    data = physical_catalog()
    experiments = profiles()
    original = compile_entities(data, ["electron"], profiles=experiments, representation=representation)
    changed = replace_identity(data, "electron", "__proto__")
    binding = next(row for row in experiments["profiles"] if row["entity_id"] == "electron")
    binding["entity_id"] = "__proto__"
    renamed = compile_entities(
        changed, ["__proto__"], profiles=experiments, representation=representation
    )
    if representation == "quantum":
        original["event_program"]["register_names"] = renamed["event_program"]["register_names"]
    assert renamed == original


@pytest.mark.parametrize("representation", ["classical", "quantum"])
def test_v2_compilation_neither_mutates_nor_aliases_inputs(representation):
    data, experiments = physical_catalog(), profiles()
    before = copy.deepcopy((data, experiments))
    result = compile_entities(data, ["electron"], profiles=experiments, representation=representation)
    assert (data, experiments) == before
    result["fields"][0]["units"] = "Changed compiled output"
    if representation == "quantum":
        result["event_program"]["initial_levels"][0] = 0
    else:
        result["seeds"][0]["values"]["momentum"][0] = 99
        result["disturbance_types"][0]["transport"]["rate_denominator"] = 3
    assert (data, experiments) == before


def test_v2_requires_explicit_profiles_without_filesystem_fallback(monkeypatch):
    data, experiments = physical_catalog(), profiles()

    def forbidden_read(*args, **kwargs):
        raise AssertionError("Compiler must not read a profile file implicitly")

    monkeypatch.setattr(Path, "read_text", forbidden_read)
    monkeypatch.setattr(Path, "read_bytes", forbidden_read)
    with pytest.raises(ValueError, match="requires explicit profiles"):
        compile_entities(data, ["electron"])
    assert compile_entities(data, ["electron"], profiles=experiments)["seeds"]


@pytest.mark.parametrize("version", [None, True, 0, 2, "1", 1.0])
def test_external_profile_version_is_strict(version):
    experiments = profiles()
    experiments["profile_version"] = version
    with pytest.raises(ValueError, match="profile_version"):
        compile_entities(physical_catalog(), ["electron"], profiles=experiments)


@pytest.mark.parametrize("version", [None, True, 0, 3, "2", 2.0])
def test_catalog_version_is_strict(version):
    data = physical_catalog()
    data["catalog_version"] = version
    with pytest.raises(ValueError, match="catalog_version"):
        compile_entities(data, ["electron"], profiles=profiles())


@pytest.mark.parametrize(
    "mutation, message",
    [
        ("duplicate", "unique"),
        ("orphan", "orphan"),
        ("blank", "unique"),
        ("extra", "binding"),
        ("empty", "binding"),
        ("null_profile", "object"),
        ("unknown_top_level", "document"),
        ("missing_purpose", "document"),
        ("blank_purpose", "purpose"),
        ("invalid_rows", "array"),
        ("invalid_row", "object"),
    ],
)
def test_external_profile_document_boundaries(mutation, message):
    experiments = profiles()
    row = experiments["profiles"][0]
    if mutation == "duplicate":
        experiments["profiles"].append(copy.deepcopy(row))
    elif mutation == "orphan":
        row["entity_id"] = "unknown catalog entity"
    elif mutation == "blank":
        row["entity_id"] = ""
    elif mutation == "extra":
        row["unexpected"] = "unrecognized binding data"
    elif mutation == "empty":
        experiments["profiles"][0] = {"entity_id": row["entity_id"]}
    elif mutation == "null_profile":
        row["quantum_profile"] = None
    elif mutation == "unknown_top_level":
        experiments["unexpected"] = "unrecognized document data"
    elif mutation == "missing_purpose":
        del experiments["purpose"]
    elif mutation == "blank_purpose":
        experiments["purpose"] = " "
    elif mutation == "invalid_rows":
        experiments["profiles"] = {}
    else:
        experiments["profiles"][0] = []
    with pytest.raises(ValueError, match=message):
        compile_entities(physical_catalog(), ["electron"], profiles=experiments)


@pytest.mark.parametrize("representation", ["classical", "quantum"])
def test_missing_profiles_and_known_unsupported_families_fail_clearly(representation):
    data, experiments = physical_catalog(), profiles()
    experiments["profiles"] = [row for row in experiments["profiles"] if row["entity_id"] == "electron"]
    compile_entities(data, ["electron"], profiles=experiments, representation=representation)
    for identity in ("positron", data["disturbance_families"][0]["id"]):
        with pytest.raises(ValueError, match=f"unsupported {representation} representation"):
            compile_entities(data, [identity], profiles=experiments, representation=representation)
    with pytest.raises(ValueError, match="unknown entity"):
        compile_entities(data, ["no such entity"], profiles=experiments, representation=representation)
    key = "executable_profile" if representation == "classical" else "quantum_profile"
    del experiments["profiles"][0][key]
    with pytest.raises(ValueError, match=f"unsupported {representation} representation"):
        compile_entities(data, ["electron"], profiles=experiments, representation=representation)


@pytest.mark.parametrize("version", [1, 2])
def test_embedded_and_external_profiles_cannot_be_combined(version):
    data = physical_catalog()
    data["catalog_version"] = version
    data["particle_entities"][0]["quantum_profile"] = {}
    with pytest.raises(ValueError, match="embedded profiles"):
        compile_entities(data, ["electron"], profiles=profiles())
    if version == 2:
        with pytest.raises(ValueError, match="embedded profiles"):
            compile_entities(data, ["electron"])


def test_v2_rejects_metadata_formula_injection_before_compilation():
    data = physical_catalog()
    data["particle_entities"][0]["physical_properties"]["hidden_law"] = {
        "expression": {"op": "add", "args": [1, 2]}
    }
    with pytest.raises(ValueError, match="executable rules or formulas"):
        compile_entities(data, ["electron"], profiles=profiles())


@pytest.mark.parametrize("representation", ["classical", "quantum"])
def test_cli_requires_and_reads_explicit_profiles(tmp_path, monkeypatch, representation):
    output = tmp_path / "compiled.json"
    args = [
        "entities",
        "--catalog",
        str(CATALOG),
        "--entity",
        "electron",
        "--output-init",
        str(output),
        "--representation",
        representation,
    ]
    monkeypatch.setattr(sys, "argv", args)
    with pytest.raises(ValueError, match="requires explicit profiles"):
        main()
    assert not output.exists()
    monkeypatch.setattr(
        sys, "argv", args + ["--profiles", str(CATALOG.with_name("representation-probes.json"))]
    )
    main()
    assert json.loads(output.read_text()) == compile_entities(
        physical_catalog(), ["electron"], profiles=profiles(), representation=representation
    )


def test_cli_profile_json_rejects_duplicate_keys(tmp_path, monkeypatch):
    invalid = tmp_path / "invalid.json"
    invalid.write_text('{"profile_version": 1, "profile_version": 1}')
    output = tmp_path / "compiled.json"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "entities",
            "--catalog",
            str(CATALOG),
            "--entity",
            "electron",
            "--profiles",
            str(invalid),
            "--output-init",
            str(output),
        ],
    )
    with pytest.raises(ValueError, match="duplicate"):
        main()
    assert not output.exists()


@pytest.mark.parametrize(
    "mutation, message",
    [
        ("noninteger_seed", "integer"),
        ("unexpected_law", "unsupported"),
        ("invalid_assumption", "assumptions"),
    ],
)
def test_external_classical_profiles_use_the_existing_strict_validator(mutation, message):
    experiments = profiles()
    probe = next(row for row in experiments["profiles"] if row["entity_id"] == "electron")
    profile = probe["executable_profile"]
    if mutation == "noninteger_seed":
        profile["seed_values"]["inventory"] = 1.5
    elif mutation == "unexpected_law":
        profile["unexpected_law"] = "annihilate"
    else:
        profile["assumptions"] = [False]
    with pytest.raises(ValueError, match=message):
        compile_entities(physical_catalog(), ["electron"], profiles=experiments)
