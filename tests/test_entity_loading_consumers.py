"""Host consumers preserve entity dependencies without changing physical rules."""

import copy
import hashlib
import json

import pytest

from event_universe.runner import run_initialization
from event_universe.world_loading import load_world


def _authored_world(*, ticks=0, flight=False):
    document = {
        "law": "beam",
        "model_id": "entity-consumer-fixture",
        "shape": [2, 1, 1],
        "ticks": ticks,
        "K": 1,
        "N": 8,
        "release": [0, 1],
        "suspension": 0,
        "families": [{"name": "packet", "quantum": 1}],
        "entity_definitions": "entities/device.json",
        "entities": [{"name": "a", "definition": "probe", "position": [1, 0, 0]}],
    }
    if flight:
        document["in_transit"] = [
            {
                "position": [0, 0, 0],
                "family": "packet",
                "number": 1,
                "direction": [1, 0, 0],
                "amount": 1,
                "phase": 0,
            }
        ]
    return document


def _definitions(amount=3):
    return {
        "format": "event-entities-v1",
        "entities": [
            {
                "name": "probe",
                "measured": [
                    {
                        "position": [0, 0, 0],
                        "family": "packet",
                        "amount": amount,
                        "fixed": True,
                        "table": {"packet": "measure"},
                    }
                ],
                "detectors": [],
            }
        ],
    }


def _write_authoring(directory, *, ticks=0, flight=False):
    directory.mkdir(parents=True, exist_ok=True)
    definition_path = directory / "entities" / "device.json"
    definition_path.parent.mkdir()
    definition_path.write_text(json.dumps(_definitions(), indent=2) + "\n", encoding="utf-8")
    path = directory / "world.json"
    path.write_text(
        json.dumps(_authored_world(ticks=ticks, flight=flight), indent=2) + "\n", encoding="utf-8"
    )
    return path, definition_path


def _digest(source):
    return hashlib.sha256(source).hexdigest()


def test_runner_preserves_original_dependencies_and_expanded_provenance(tmp_path):
    path, definition_path = _write_authoring(tmp_path / "input")
    original = path.read_bytes()
    definition_source = definition_path.read_bytes()
    output = tmp_path / "run"
    record = json.loads(run_initialization(path, output).read_bytes())
    bundle = (output / "initialization_bundle.json").read_bytes()
    expanded = (output / "resolved_initialization.json").read_bytes()
    assert (output / "initialization.json").read_bytes() == original
    assert record["initialization_sha256"] == _digest(original)
    assert record["initialization_resolution"] == {
        "format": "event-world-bundle-v1",
        "bundle_sha256": _digest(bundle),
        "expanded_sha256": _digest(expanded),
        "sources": [{"path": "entities/device.json", "sha256": _digest(definition_source)}],
    }
    assert json.loads(expanded)["measured"][0]["position"] == [1, 0, 0]
    assert "entity_definitions" not in json.loads(expanded)
    assert record["completed_ticks"] == 0
    # Relocation cannot reopen the original file: remove it before replay.
    definition_path.unlink()
    relocated = tmp_path / "relocated.json"
    relocated.write_bytes(bundle)
    relocated_output = tmp_path / "relocated-run"
    other = json.loads(run_initialization(relocated, relocated_output).read_bytes())
    assert other["initialization_resolution"] == record["initialization_resolution"]
    assert (relocated_output / "resolved_initialization.json").read_bytes() == expanded
    assert load_world(bundle).world == load_world(expanded).world


def test_invalid_external_input_fails_before_output_directory(tmp_path):
    path, definition_path = _write_authoring(tmp_path / "input")
    definition_path.unlink()
    output = tmp_path / "run"
    with pytest.raises(OSError):
        run_initialization(path, output)
    assert not output.exists()


def test_plain_runner_retains_original_artifact_schema(tmp_path):
    document = _authored_world()
    del document["entity_definitions"], document["entities"]
    material = _definitions()["entities"][0]["measured"][0]
    material["position"] = [1, 0, 0]
    document["measured"] = [material]
    path = tmp_path / "plain.json"
    source = json.dumps(document, indent=3).encode()
    path.write_bytes(source)
    output = tmp_path / "plain-run"
    record = json.loads(run_initialization(path, output).read_bytes())
    assert (output / "initialization.json").read_bytes() == source
    assert "initialization_resolution" not in record
    assert not (output / "initialization_bundle.json").exists()
    assert not (output / "resolved_initialization.json").exists()
    assert load_world(source).portable_source == source


def test_resolution_artifacts_survive_a_recorded_runtime_refusal(tmp_path):
    # A second probe `b` at x = 0 owns the ray; the probe `a` at x = 1
    # (content 3 at K 1, N 8) measures it in interval 1 and turns 4 steps,
    # half the circle, at its next self-creation: refused at interval 2
    # with one completed tick.
    path, _ = _write_authoring(tmp_path / "input", ticks=2, flight=True)
    document = json.loads(path.read_text(encoding="utf-8"))
    document["entities"].append({"name": "b", "definition": "probe", "position": [0, 0, 0]})
    document["in_transit"][0]["number"] = 2
    path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    output = tmp_path / "failed-run"
    with pytest.raises(ValueError, match="half the circle"):
        run_initialization(path, output)
    record = json.loads((output / "run.json").read_bytes())
    assert record["status"] == "failed" and record["completed_ticks"] == 1
    assert record["initialization_resolution"]["bundle_sha256"] == _digest(
        (output / "initialization_bundle.json").read_bytes()
    )
    assert (output / "resolved_initialization.json").is_file()


def test_metadata_copy_cannot_be_changed_during_execution(tmp_path, monkeypatch):
    from event_universe.events import run

    path, _ = _write_authoring(tmp_path / "input")
    loaded = load_world(path.read_bytes(), base_dir=path.parent)
    initialization_record = {"sources": [{"path": "fixed.json", "sha256": "original"}]}
    expected = copy.deepcopy(initialization_record)
    original_simulation = run.NatureBeamSimulation

    def construct(world, observer=None, *, keep_row_clicks=False):
        # The runner's record switch (2026-09-23), taken as the engine takes it.
        initialization_record["sources"][0]["sha256"] = "changed"
        return original_simulation(world, observer)

    monkeypatch.setattr(run, "NatureBeamSimulation", construct)
    output = tmp_path / "run"
    output.mkdir()
    record = json.loads(
        run.execute_nature_beam_run(
            loaded.world,
            path.read_bytes(),
            output,
            "source-fingerprint",
            0,
            initialization_record=initialization_record,
        ).read_bytes()
    )
    assert record["initialization_resolution"] == expected
