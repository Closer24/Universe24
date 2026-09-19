"""Host consumers preserve entity dependencies without changing physical rules."""

import copy
import hashlib
import json
from pathlib import Path

import pytest

from event_universe import ui
from event_universe.runner import run_initialization
from event_universe.world_loading import load_world


def _authored_world(*, ticks=0, flight=False):
    document = {
        "law": "events",
        "dynamics": "reversible-detector-v1",
        "max_active_owners": 1,
        "model_id": "entity-consumer-fixture",
        "shape": [2, 1, 1],
        "ticks": ticks,
        "K": 1024,
        "N": 8,
        "release": [0, 1],
        "suspension": 0,
        "families": [{"name": "packet", "kind": "paid"}],
        "entity_definitions": "entities/device.json",
        "entities": [{"name": "a", "definition": "probe", "position": [1, 0, 0]}],
    }
    if flight:
        document["in_transit"] = [
            {
                "position": [1, 0, 0],
                "family": "packet",
                "number": 1,
                "heading": [1, 0, 0],
                "amount": 1,
                "phase": 0,
            }
        ]
    return document


def _definitions(amount=1):
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
                        "table": {"packet": "pass"},
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
    with pytest.raises(ValueError):
        ui.Workspace(path.parent, tmp_path / "workspace").start(path.read_text())
    assert not (tmp_path / "workspace").exists()


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
    path, _ = _write_authoring(tmp_path / "input", ticks=2, flight=True)
    output = tmp_path / "failed-run"
    with pytest.raises(ValueError, match="open-edge escape"):
        run_initialization(path, output)
    record = json.loads((output / "run.json").read_bytes())
    assert record["status"] == "failed" and record["completed_ticks"] == 1
    assert record["initialization_resolution"]["bundle_sha256"] == _digest(
        (output / "initialization_bundle.json").read_bytes()
    )
    assert (output / "resolved_initialization.json").is_file()


class _Process:
    """A host process stub: exercise saved input ownership without a world run."""

    def __init__(self):
        self.code = None

    def poll(self):
        return self.code

    def terminate(self):
        self.code = 0

    def wait(self, timeout=None):
        return self.code

    def kill(self):
        self.code = -1


def test_workspace_prepares_frozen_portable_templates_export_and_start(tmp_path, monkeypatch):
    configs = tmp_path / "configs"
    path, definition_path = _write_authoring(configs / "nested")
    _write_authoring(configs / "another")
    workspace = ui.Workspace(configs, tmp_path / "workspace")
    templates = workspace.templates()
    assert [item["id"] for item in templates] == ["another/world", "nested/world"]
    original = next(item["source"] for item in templates if item["id"] == "nested/world")
    assert json.loads(original)["format"] == "event-world-bundle-v1"
    assert ui.validate_source(original)["measured"] == 1
    definition_path.write_text(json.dumps(_definitions(2)), encoding="utf-8")
    refreshed = next(item["source"] for item in workspace.templates() if item["id"] == "nested/world")
    assert load_world(original).world.measured[0].amount == 1
    assert load_world(refreshed).world.measured[0].amount == 2
    definition_path.unlink()
    exported = workspace.export(original)
    export_id = Path(exported["url"]).stem
    exported_bytes = workspace.exports[export_id][0].read_bytes()
    assert exported_bytes == original.encode()
    assert load_world(exported_bytes).world.measured[0].amount == 1
    commands = []
    process = _Process()

    def start_process(command, **kwargs):
        commands.append(command)
        return process

    monkeypatch.setattr(ui.subprocess, "Popen", start_process)
    try:
        result = workspace.start(original)
        job = workspace.jobs[result["id"]]
        assert job.initialization.read_bytes() == exported_bytes
        assert commands[0][commands[0].index("--init") + 1] == str(job.initialization)
        assert load_world(job.initialization.read_bytes()).world.measured[0].amount == 1
        job.output.mkdir(parents=True)
        for name in ("initialization_bundle.json", "resolved_initialization.json"):
            (job.output / name).write_bytes(b"{}")
        process.code = 0
        artifacts = job.describe()["artifacts"]
        for name in ("initialization_bundle.json", "resolved_initialization.json"):
            assert name in artifacts
            match = ui.FILE_ROUTE.fullmatch(artifacts[name])
            assert match is not None and match[2] == name and name in ui.ARTIFACTS
    finally:
        workspace.close()
    assert path.is_file()


def test_metadata_copy_cannot_be_changed_during_execution(tmp_path, monkeypatch):
    from event_universe.events import run

    path, _ = _write_authoring(tmp_path / "input")
    loaded = load_world(path.read_bytes(), base_dir=path.parent)
    initialization_record = {"sources": [{"path": "fixed.json", "sha256": "original"}]}
    expected = copy.deepcopy(initialization_record)
    original_simulation = run.EventSimulation

    def construct(world, observer=None):
        initialization_record["sources"][0]["sha256"] = "changed"
        return original_simulation(world, observer)

    monkeypatch.setattr(run, "EventSimulation", construct)
    output = tmp_path / "run"
    output.mkdir()
    record = json.loads(
        run.execute_event_run(
            loaded.world,
            path.read_bytes(),
            output,
            "source-fingerprint",
            0,
            initialization_record=initialization_record,
        ).read_bytes()
    )
    assert record["initialization_resolution"] == expected
