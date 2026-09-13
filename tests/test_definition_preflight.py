"""Shared definition file reports remain pure and identify the failing input."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

from event_universe.configuration_validation import validate_configuration
from event_universe.disturbance_api import Simulation

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples/named-definitions"


def sources():
    return (
        (EXAMPLE / "definitions.json").read_bytes(),
        (EXAMPLE / "near.json").read_bytes(),
    )


def test_definitions_and_experiment_report_without_filesystem_or_world_access(monkeypatch):
    definitions, experiment = sources()

    def forbidden(*args, **kwargs):
        pytest.fail("Preflight must not access files or construct a simulation")

    monkeypatch.setattr(Simulation, "__init__", forbidden)
    for method in ("read_text", "read_bytes", "write_text", "write_bytes", "mkdir"):
        monkeypatch.setattr(Path, method, forbidden)
    model = validate_configuration(definitions)
    run = validate_configuration(experiment, definitions_source=definitions)
    assert model.valid and run.valid, (model.to_dict(), run.to_dict())
    assert model.kind == "definitions" and run.kind == "experiment"
    assert model.summary["fields"] == 2
    assert model.summary["types"] == 2
    assert run.summary["model"] == model.summary["model"]


@pytest.mark.parametrize("kind", ["auto", "experiment"])
def test_experiment_needs_explicit_definitions(kind):
    _, experiment = sources()
    report = validate_configuration(experiment, kind=kind)
    assert not report.valid
    assert (report.issues[0].code, report.issues[0].document) == ("missing_dependency", "definitions")


@pytest.mark.parametrize("bad", ["{", '{"definitions_version":1,"definitions_version":1}', "{}"])
def test_invalid_definition_dependency_is_identified(bad):
    _, experiment = sources()
    report = validate_configuration(experiment, definitions_source=bad)
    assert not report.valid
    assert report.issues[0].document == "definitions"


def test_deleting_used_definition_fails_even_when_type_is_not_placed():
    definitions, experiment = sources()
    library = json.loads(definitions)
    library["model"]["fields"].pop()
    world = json.loads(experiment)
    world["world"]["seeds"] = []
    report = validate_configuration(json.dumps(world), definitions_source=json.dumps(library))
    assert not report.valid
    assert report.issues[0].document == "definitions"


@pytest.mark.parametrize("unplaced", [False, True])
def test_every_declared_disturbance_needs_an_explicit_field_coupling(unplaced):
    definitions, experiment = sources()
    library = json.loads(definitions)
    if unplaced:
        library["model"]["disturbance_types"].append(
            {"name": "unplaced", "fields": ["amber inventory"], "transport": {"mode": "hold"}}
        )
    else:
        library["model"]["spatial_couplings"].pop(0)
    source = json.dumps(library)
    standalone = validate_configuration(source)
    composed = validate_configuration(experiment, definitions_source=source)
    assert not standalone.valid and not composed.valid
    assert standalone.issues[0].document == "input"
    assert composed.issues[0].document == "definitions"
    assert "explicit field coupling" in standalone.issues[0].message
    assert "explicit field coupling" in composed.issues[0].message


def test_valid_model_does_not_hide_bad_experiment_or_allow_definition_override():
    definitions, experiment = sources()
    world = json.loads(experiment)
    world["world"]["seeds"][0]["type"] = "deleted disturbance"
    report = validate_configuration(json.dumps(world), definitions_source=definitions)
    assert not report.valid and report.issues[0].document == "input"
    world["world"]["fields"] = []
    report = validate_configuration(json.dumps(world), definitions_source=definitions)
    assert not report.valid and report.issues[0].document == "input"


def test_unused_definitions_dependency_and_ambiguous_discriminators_are_rejected():
    definitions, experiment = sources()
    report = validate_configuration(definitions, definitions_source=definitions)
    assert not report.valid and report.issues[0].code == "unexpected_dependency"
    world = json.loads(experiment)
    world["schema_version"] = 1
    report = validate_configuration(json.dumps(world), definitions_source=definitions)
    assert not report.valid and report.issues[0].code == "unsupported_kind"


def test_preflight_cli_checks_both_files_and_reports_dependency_io_without_writes(tmp_path):
    definitions, experiment = sources()
    model_path, run_path = tmp_path / "model.json", tmp_path / "run.json"
    model_path.write_bytes(definitions)
    run_path.write_bytes(experiment)
    before = {path.name: path.read_bytes() for path in tmp_path.iterdir()}
    command = [sys.executable, "-m", "event_universe.configuration_validation"]
    for args, kind in (
        ([str(model_path), "--json"], "definitions"),
        ([str(run_path), "--definitions", str(model_path), "--json"], "experiment"),
    ):
        completed = subprocess.run(command + args, cwd=ROOT, capture_output=True, text=True)
        assert completed.returncode == 0, completed.stderr
        report = json.loads(completed.stdout)
        assert report["valid"] and report["results"][0]["kind"] == kind
    completed = subprocess.run(
        command + [str(run_path), "--definitions", str(tmp_path / "missing.json"), "--json"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 1
    issue = json.loads(completed.stdout)["results"][0]["issues"][0]
    assert (issue["code"], issue["document"]) == ("io", "definitions")
    assert {path.name: path.read_bytes() for path in tmp_path.iterdir()} == before
