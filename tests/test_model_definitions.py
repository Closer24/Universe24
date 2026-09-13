"""Reusable definition ownership, whole-file validation and resolved run parity."""

import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.core.disturbance_state import InitialState
from event_universe.initialization import parse_initial_state
from event_universe.model_definitions import compose_initialization, validate_model_definitions

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples/named-definitions"


def _read(name):
    return json.loads((EXAMPLE / name).read_text(encoding="utf-8"))


def _documents():
    return _read("definitions.json"), _read("near.json")


def _unplaced_type():
    return {
        "name": "unplaced type",
        "fields": ["amber inventory"],
        "defaults": {"amber inventory": 1},
        "transport": {"mode": "hold"},
    }


def _records(world):
    return {
        world.initial.disturbances[record.type_index].name: world.record_values(record)
        for cell in world.cells.values()
        for record in cell.records
        if record is not None
    }


def _dynamic_fields(world):
    snapshot = world.snapshot()
    totals = dict.fromkeys((field.name for field in world.initial.fields), 0)
    for cell in snapshot["spatial_fields"]:
        for name, field in cell["fields"].items():
            totals[name] += sum(payload[0] for payload in field["populations"])
    for packet in snapshot["spatial_transfers"]:
        for name, populations in packet["fields"].items():
            totals[name] += sum(payload[0] for payload in populations)
    return totals


def _rename(value, names):
    if isinstance(value, dict):
        return {names.get(key, key): _rename(item, names) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_rename(item, names) for item in value]
    return names.get(value, value) if isinstance(value, str) else value


def _cli(definitions, experiment, output):
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "event_universe.model_definitions",
            "--definitions",
            str(definitions),
            "--experiment",
            str(experiment),
            "--output-init",
            str(output),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def test_one_and_multiple_owned_fields_are_resolved_without_running(monkeypatch):
    definitions, experiment = _documents()

    def unexpected_world(*args, **kwargs):
        raise AssertionError("configuration validation must not construct a world")

    monkeypatch.setattr(Simulation, "__init__", unexpected_world)
    initial = validate_model_definitions(definitions)
    assert isinstance(initial, InitialState)
    assert initial.seeds == ()
    assert [kind.fields for kind in initial.disturbances] == [(0,), (0, 1)]
    resolved = compose_initialization(definitions, experiment)
    assert parse_initial_state(resolved).seeds


@pytest.mark.parametrize("filename", ["near.json", "shifted.json"])
def test_both_experiments_use_one_definition_and_preserve_local_exchange(filename):
    definitions = _read("definitions.json")
    experiment = _read(filename)
    resolved = compose_initialization(definitions, experiment)
    inline = {**deepcopy(definitions["model"]), **deepcopy(experiment["world"])}
    assert parse_initial_state(resolved) == parse_initial_state(inline)
    events, inline_events = [], []
    world = Simulation(parse_initial_state(resolved), observer=events.append)
    reference = Simulation(parse_initial_state(inline), observer=inline_events.append)
    # Uniform baselines contribute once at each of the 343 physical cells.
    original_totals = {"amber inventory": (1059,), "blue inventory": (1745,)}
    assert world.totals() == original_totals
    for tick in range(experiment["world"]["ticks"]):
        world.step()
        reference.step()
        assert world.snapshot() == reference.snapshot()
        assert events == inline_events
        assert world.totals() == original_totals
        assert world.source_totals() == {"amber inventory": (0,), "blue inventory": (0,)}
        assert world.computation_report() == reference.computation_report()
        if tick == 0:
            assert _records(world) == {
                "single channel": {"amber inventory": (7,)},
                "dual channel": {"amber inventory": (17,), "blue inventory": (25,)},
            }
            assert _dynamic_fields(world) == {"amber inventory": 6, "blue inventory": 5}


def test_arbitrary_names_do_not_select_different_rules_or_state():
    definitions, experiment = _documents()
    names = {
        "amber inventory": "unrelated alpha",
        "blue inventory": "unrelated beta",
        "single channel": "unrelated gamma",
        "dual channel": "unrelated delta",
    }
    renamed_definitions, renamed_experiment = _rename(definitions, names), _rename(experiment, names)
    world = Simulation(parse_initial_state(compose_initialization(definitions, experiment)))
    renamed = Simulation(
        parse_initial_state(compose_initialization(renamed_definitions, renamed_experiment))
    )
    for _ in range(2):
        world.step()
        renamed.step()
        assert _rename(world.snapshot(), names) == _rename(renamed.snapshot(), {})
        assert _rename(world.totals(), names) == _rename(renamed.totals(), {})
        assert world.computation_report() == renamed.computation_report()


def test_composed_snapshots_do_not_alias_inputs_or_each_other():
    definitions, experiment = _documents()
    original_definitions, original_experiment = deepcopy(definitions), deepcopy(experiment)
    first = compose_initialization(definitions, experiment)
    second = compose_initialization(definitions, experiment)
    first["disturbance_types"][0]["defaults"]["amber inventory"] = 99
    first["spatial_couplings"][0]["amount"]["field"] = "changed"
    first["seeds"][0]["position"][0] = 0
    assert definitions == original_definitions
    assert experiment == original_experiment
    assert second == compose_initialization(original_definitions, original_experiment)
    definitions["model"]["fields"] = []
    experiment["world"]["seeds"][0]["position"][0] = 1
    assert second["seeds"][0]["position"] == [2, 3, 3]
    assert len(second["fields"]) == 2


@pytest.mark.parametrize("section", ["fields", "disturbance_types"])
def test_duplicate_and_empty_declarations_are_rejected(section):
    definitions, _ = _documents()
    definitions["model"][section].append(deepcopy(definitions["model"][section][0]))
    with pytest.raises(ValueError):
        validate_model_definitions(definitions)
    definitions["model"][section] = []
    with pytest.raises(ValueError):
        validate_model_definitions(definitions)


@pytest.mark.parametrize("owned", [[], ["missing"], ["amber inventory", "amber inventory"]])
def test_each_disturbance_requires_distinct_known_owned_fields(owned):
    definitions, _ = _documents()
    definitions["model"]["disturbance_types"][0]["fields"] = owned
    with pytest.raises(ValueError):
        validate_model_definitions(definitions)


@pytest.mark.parametrize("section", ["fields", "disturbance_types"])
def test_removing_a_referenced_definition_fails_without_deleting_its_rules(section):
    definitions, experiment = _documents()
    definitions["model"][section].pop(0)
    original_rules = deepcopy(definitions["model"]["spatial_couplings"])
    with pytest.raises(ValueError):
        compose_initialization(definitions, experiment)
    assert definitions["model"]["spatial_couplings"] == original_rules


def test_an_unplaced_unreferenced_disturbance_can_be_added_and_removed():
    definitions, experiment = _documents()
    original = compose_initialization(definitions, experiment)
    definitions["model"]["disturbance_types"].append(_unplaced_type())
    assert len(validate_model_definitions(definitions).disturbances) == 3
    assert len(parse_initial_state(compose_initialization(definitions, experiment)).seeds) == 2
    definitions["model"]["disturbance_types"].pop()
    assert compose_initialization(definitions, experiment) == original


def test_an_unused_named_field_can_be_added_and_removed():
    definitions, experiment = _documents()
    original = compose_initialization(definitions, experiment)
    field = deepcopy(definitions["model"]["fields"][0])
    field["name"] = "unused property"
    definitions["model"]["fields"].append(field)
    assert len(validate_model_definitions(definitions).fields) == 3
    assert len(parse_initial_state(compose_initialization(definitions, experiment)).fields) == 3
    definitions["model"]["fields"].pop()
    assert compose_initialization(definitions, experiment) == original


@pytest.mark.parametrize("invalid_default", [0.5, True, 1073741824])
def test_invalid_unplaced_definition_still_fails_whole_file_validation(invalid_default):
    definitions, experiment = _documents()
    unplaced = _unplaced_type()
    unplaced["defaults"]["amber inventory"] = invalid_default
    definitions["model"]["disturbance_types"].append(unplaced)
    with pytest.raises(ValueError):
        validate_model_definitions(definitions)
    with pytest.raises(ValueError):
        compose_initialization(definitions, experiment)


@pytest.mark.parametrize("placement", ["outside", "unknown type", "unknown value", "capacity"])
def test_valid_definitions_do_not_bypass_experiment_validation(placement):
    definitions, experiment = _documents()
    validate_model_definitions(definitions)
    seed = experiment["world"]["seeds"][0]
    if placement == "outside":
        seed["position"] = [7, 3, 3]
    elif placement == "unknown type":
        seed["type"] = "not declared"
    elif placement == "unknown value":
        seed["values"] = {"blue inventory": 3}
    else:
        experiment["world"]["slots_per_cell"] = 1
        experiment["world"]["seeds"][1]["position"] = seed["position"].copy()
    with pytest.raises(ValueError):
        compose_initialization(definitions, experiment)


@pytest.mark.parametrize("key", ["shape", "seeds", "ticks", "normal_budget", "observer"])
def test_world_settings_cannot_be_hidden_in_the_model(key):
    definitions, experiment = _documents()
    definitions["model"][key] = deepcopy(experiment["world"].get(key, {}))
    with pytest.raises(ValueError):
        compose_initialization(definitions, experiment)


@pytest.mark.parametrize("key", ["fields", "disturbance_types", "spatial_couplings", "model_id"])
def test_experiments_cannot_override_model_definitions_or_rules(key):
    definitions, experiment = _documents()
    experiment["world"][key] = deepcopy(definitions["model"][key])
    with pytest.raises(ValueError):
        compose_initialization(definitions, experiment)


@pytest.mark.parametrize("version", [True, 2, "1"])
@pytest.mark.parametrize("document", ["definitions", "experiment"])
def test_versions_are_explicit_supported_integers(document, version):
    definitions, experiment = _documents()
    target = definitions if document == "definitions" else experiment
    target[f"{document}_version"] = version
    with pytest.raises(ValueError):
        compose_initialization(definitions, experiment)


def test_cli_writes_valid_initialization_and_preserves_source_files(tmp_path):
    output = tmp_path / "resolved.json"
    definitions, experiment = EXAMPLE / "definitions.json", EXAMPLE / "near.json"
    source_bytes = definitions.read_bytes(), experiment.read_bytes()
    completed = _cli(definitions, experiment, output)
    assert completed.returncode == 0, completed.stderr
    assert parse_initial_state(json.loads(output.read_text(encoding="utf-8"))).shape == (7, 7, 7)
    assert (definitions.read_bytes(), experiment.read_bytes()) == source_bytes
    assert sorted(path.name for path in tmp_path.iterdir()) == ["resolved.json"]


def test_cli_refuses_to_overwrite_an_existing_output(tmp_path):
    output = tmp_path / "resolved.json"
    output.write_bytes(b"existing user content\n")
    completed = _cli(EXAMPLE / "definitions.json", EXAMPLE / "near.json", output)
    assert completed.returncode != 0
    assert output.read_bytes() == b"existing user content\n"


def test_cli_rejects_invalid_experiment_before_creating_output(tmp_path):
    _, experiment = _documents()
    experiment["world"]["seeds"][0]["type"] = "missing"
    source = tmp_path / "bad-experiment.json"
    source.write_text(json.dumps(experiment), encoding="utf-8")
    output = tmp_path / "output" / "resolved.json"
    completed = _cli(EXAMPLE / "definitions.json", source, output)
    assert completed.returncode != 0
    assert not output.parent.exists()


def test_cli_uses_strict_json_decoding_for_duplicate_keys(tmp_path):
    source = tmp_path / "duplicate-definition.json"
    source.write_text(
        '{"definitions_version": 1, "definitions_version": 1, "model": {}}', encoding="utf-8"
    )
    output = tmp_path / "resolved.json"
    completed = _cli(source, EXAMPLE / "near.json", output)
    assert completed.returncode != 0
    assert not output.exists()
