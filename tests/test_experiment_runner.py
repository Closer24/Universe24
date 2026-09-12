"""Package runner controls, exact captured artifacts and output-free CLI inspection."""

import hashlib
import json
import shutil
import sys
from pathlib import Path
from types import ModuleType

import pytest

from event_universe import Simulation, load_experiment
from event_universe.runner import main, run_experiment

EXAMPLE = Path(__file__).resolve().parents[1] / "examples/experiment-package"


@pytest.fixture
def manifest(tmp_path):
    package = tmp_path / "inputs"
    shutil.copytree(EXAMPLE, package)
    return package / "experiment.json"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def controls(manifest, **values):
    path = manifest.parent / "run.json"
    raw = read(path)
    raw["data"].update(values)
    path.write_text(json.dumps(raw), encoding="utf-8")


def test_runner_preserves_reloadable_starting_package_despite_later_source_edits(
    manifest, tmp_path, monkeypatch
):
    package = load_experiment(manifest)
    original = Simulation.step

    def edit_after_start(self):
        controls(manifest, ticks=99)
        original(self)

    monkeypatch.setattr(Simulation, "step", edit_after_start)
    output = tmp_path / "result"
    artifact = run_experiment(manifest, output)
    metadata = read(artifact)
    assert artifact.name == "run.json"
    assert metadata["status"] == "completed"
    assert metadata["requested_ticks"] == metadata["completed_ticks"] == metadata["tick"] == 4
    assert metadata["final_totals"] == {"quantity": [2]}
    assert metadata["accounting_balanced_at_every_completed_tick"]
    assert metadata["display"] == "none"
    assert metadata["experiment"] == package.provenance
    assert read(output / "experiment-provenance.json") == package.provenance
    assert (output / "initialization.json").read_bytes() == package.runtime_json
    assert metadata["initialization_sha256"] == hashlib.sha256(package.runtime_json).hexdigest()
    for source in package.sources:
        assert (output / "experiment" / source.path).read_bytes() == source.content
    restored = load_experiment(output / "experiment" / "experiment.json")
    assert restored.runtime_json == package.runtime_json
    assert restored.provenance == package.provenance
    assert not (output / "run.html").exists()
    assert (output / "events.jsonl").read_text(encoding="utf-8")


def test_explicit_tick_and_sampling_overrides_are_recorded_without_rewriting_input(manifest, tmp_path):
    controls(manifest, ticks=6, frame_stride=2)
    output = tmp_path / "override"
    metadata = read(run_experiment(manifest, output, ticks=3, frame_stride=5))
    assert metadata["requested_ticks"] == metadata["completed_ticks"] == 3
    assert read(output / "initialization.json")["ticks"] == 6
    assert read(output / "experiment/run.json")["data"]["frame_stride"] == 2
    assert metadata["effective_run_controls"] == {"ticks": 3, "visualize": False, "frame_stride": 5}


@pytest.mark.parametrize(
    "overrides,expected", [({}, [0, 2, 4]), ({"frame_stride": 3}, [0, 3, 4]), ({"visualize": False}, [])]
)
def test_visual_package_defaults_and_overrides_control_saved_sampling_only(
    manifest, tmp_path, monkeypatch, overrides, expected
):
    controls(manifest, visualize=True, frame_stride=2)
    captured = []
    renderer = ModuleType("event_universe.diagnostics.disturbance_render")

    def render(frames, path, metadata, *, observation=None):
        captured.extend(frame["tick"] for frame in frames)
        return path

    renderer.render_disturbances = render
    monkeypatch.setitem(sys.modules, renderer.__name__, renderer)
    run_experiment(manifest, tmp_path / "view", **overrides)
    assert captured == expected
    metadata = read(tmp_path / "view/run.json")
    assert metadata["completed_ticks"] == 4
    assert metadata["final_totals"] == {"quantity": [2]}


def test_validate_cli_uses_canonical_input_without_steps_or_artifacts(
    manifest, tmp_path, monkeypatch, capsys
):
    def forbidden_step(self):
        raise AssertionError("validation must not advance time")

    monkeypatch.setattr(Simulation, "step", forbidden_step)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["event-universe", "--experiment", str(manifest), "--validate"])
    before = sorted(path.relative_to(tmp_path).as_posix() for path in tmp_path.rglob("*"))
    main()
    assert capsys.readouterr().out.strip() == "Valid"
    assert sorted(path.relative_to(tmp_path).as_posix() for path in tmp_path.rglob("*")) == before


@pytest.mark.parametrize(
    "arguments,name", [(["--schema"], "runtime"), (["--schema", "experiment"], "experiment")]
)
def test_schema_cli_prints_packaged_contract_without_outputs(
    arguments, name, tmp_path, monkeypatch, capsys
):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["event-universe", *arguments])
    main()
    document = json.loads(capsys.readouterr().out)
    assert document["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert document["$id"].endswith(f"/{name}.schema.json")
    assert list(tmp_path.iterdir()) == []


@pytest.mark.parametrize(
    "options", [["--ticks", "-1"], ["--frame-stride", "0"], ["--observer", "missing-observer.json"]]
)
def test_validate_rejects_invalid_explicit_run_inputs(manifest, tmp_path, monkeypatch, capsys, options):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        sys, "argv", ["event-universe", "--experiment", str(manifest), "--validate", *options]
    )
    with pytest.raises(SystemExit) as error:
        main()
    assert error.value.code == 1
    assert "Run failed:" in capsys.readouterr().err
    assert not (tmp_path / "artifacts").exists()


def test_cli_no_visualize_overrides_package_and_invalid_package_creates_no_output(
    manifest, tmp_path, monkeypatch, capsys
):
    controls(manifest, visualize=True)
    output = tmp_path / "headless"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "event-universe",
            "--experiment",
            str(manifest),
            "--no-visualize",
            "--ticks",
            "1",
            "--output",
            str(output),
        ],
    )
    main()
    assert Path(capsys.readouterr().out.strip()) == (output / "run.json").resolve()
    assert read(output / "run.json")["display"] == "none"
    assert not (output / "run.html").exists()
    raw = read(manifest)
    raw["environment"] = "../outside.json"
    manifest.write_text(json.dumps(raw), encoding="utf-8")
    bad_output = tmp_path / "invalid"
    monkeypatch.setattr(
        sys, "argv", ["event-universe", "--experiment", str(manifest), "--output", str(bad_output)]
    )
    with pytest.raises(SystemExit) as error:
        main()
    assert error.value.code == 1
    assert "traversal" in capsys.readouterr().err
    assert not bad_output.exists()


def test_runner_rejects_output_containing_original_package(manifest):
    with pytest.raises(ValueError, match="original input files"):
        run_experiment(manifest, manifest.parent)
    assert load_experiment(manifest).initial.ticks == 4
