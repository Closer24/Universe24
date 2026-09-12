"""Reusable data composition preserves canonical physics, order and provenance."""

import copy
import hashlib
import json
import shutil
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe import experiment as owner
from event_universe.experiment import load_experiment
from event_universe.initialization import parse_initial_json

EXAMPLE = Path(__file__).resolve().parents[1] / "examples/experiment-package"


@pytest.fixture
def package(tmp_path):
    target = tmp_path / "package"
    shutil.copytree(EXAMPLE, target)
    return target


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def test_repeated_type_instances_match_direct_runtime_and_pass_through_each_other():
    package = load_experiment(EXAMPLE / "experiment.json")
    events, direct_events = [], []
    world = Simulation(package.initial, observer=events.append)
    direct = Simulation(parse_initial_json(package.runtime_json), observer=direct_events.append)
    assert len(package.initial.disturbances) == 1
    assert len(package.initial.seeds) == 2
    for _ in range(4):
        world.step()
        direct.step()
        assert world.snapshot() == direct.snapshot()
        assert world.totals() == {"quantity": (2,)}
    assert events == direct_events
    receptions = [event for event in events if event["event"] == "received"]
    assert len(receptions) == 8
    assert {tuple(event["position"]) for event in receptions if event["tick"] == 2} == {(4, 4, 4)}
    assert {tuple(event["position"]) for event in receptions if event["tick"] == 4} == {
        (2, 4, 4),
        (6, 4, 4),
    }


def test_exact_source_bytes_and_frozen_run_input_survive_later_edits(package):
    manifest = package / "experiment.json"
    manifest.write_bytes(
        manifest.read_bytes().replace(b'  "experiment_version"', b'    "experiment_version"')
    )
    compiled = load_experiment(manifest)
    before = compiled.runtime_json
    assert len(compiled.sources) == 6
    for source in compiled.sources:
        assert source.content == (package / source.path).read_bytes()
        assert source.sha256 == hashlib.sha256(source.content).hexdigest()
        assert not Path(source.path).is_absolute()
    assert compiled.provenance["runtime_sha256"] == hashlib.sha256(before).hexdigest()
    compiled.run_controls["ticks"] = 999
    compiled.provenance["manifest"] = "changed"
    run = read(package / "run.json")
    run["data"]["ticks"] = 5
    write(package / "run.json", run)
    changed = load_experiment(manifest)
    assert compiled.runtime_json == before
    assert compiled.run_controls["ticks"] == 4
    assert compiled.provenance["manifest"] == "experiment.json"
    assert changed.runtime_json != before
    assert changed.provenance["runtime_sha256"] != compiled.provenance["runtime_sha256"]


def test_shared_diamond_definitions_are_loaded_once_and_identical_types_are_reusable(package):
    source = read(package / "definitions/entities.json")
    write(package / "definitions/alias.json", source)
    manifest = read(package / "experiment.json")
    manifest["definitions"].append("definitions/alias.json")
    write(package / "experiment.json", manifest)
    result = load_experiment(package / "experiment.json")
    assert len(result.initial.fields) == 2
    assert len(result.initial.disturbances) == 1
    assert len(result.initial.seeds) == 2
    assert len([source for source in result.sources if source.path.endswith("fields.json")]) == 1


@pytest.mark.parametrize("change", ["conflict", "duplicate", "numeric_type"])
def test_ambiguous_reusable_definitions_are_rejected(package, change):
    fields = read(package / "definitions/fields.json")
    if change == "duplicate":
        fields["data"]["fields"].append(copy.deepcopy(fields["data"]["fields"][0]))
        write(package / "definitions/fields.json", fields)
    else:
        fields["data"]["fields"][0]["components"] = 3 if change == "conflict" else 1.0
        write(package / "definitions/conflict.json", fields)
        manifest = read(package / "experiment.json")
        manifest["definitions"].append("definitions/conflict.json")
        write(package / "experiment.json", manifest)
    with pytest.raises(ValueError, match="conflicting|duplicate"):
        load_experiment(package / "experiment.json")


@pytest.mark.parametrize(
    "path",
    [
        "../outside.json",
        "/absolute.json",
        "C:/outside.json",
        "x\\part.json",
        "https://x/a.json",
        "./environment.json",
        "a//b.json",
        "a/../b.json",
        "env.txt",
    ],
)
def test_references_cannot_escape_or_select_network_sources(package, path):
    manifest = read(package / "experiment.json")
    manifest["environment"] = path
    write(package / "experiment.json", manifest)
    with pytest.raises(ValueError, match="relative .json paths without traversal"):
        load_experiment(package / "experiment.json")


def test_include_cycle_and_conflicting_environment_are_explicit(package):
    env = read(package / "environment.json")
    env["includes"] = ["environment.json"]
    write(package / "environment.json", env)
    with pytest.raises(ValueError, match="include cycle"):
        load_experiment(package / "experiment.json")
    env["includes"] = ["other-environment.json"]
    write(
        package / "other-environment.json",
        {"part_version": 1, "part_kind": "environment", "data": {"link_ticks": 2}},
    )
    write(package / "environment.json", env)
    with pytest.raises(ValueError, match="conflicting experiment member: link_ticks"):
        load_experiment(package / "experiment.json")


@pytest.mark.parametrize(
    "filename,mutation,expected",
    [
        ("experiment.json", lambda value: value.update(unknown=True), "unknown keys"),
        (
            "experiment.json",
            lambda value: value.update(experiment_version=True),
            "unsupported experiment_version",
        ),
        ("environment.json", lambda value: value.update(part_kind="run"), "requires a environment part"),
        ("run.json", lambda value: value["data"].update(visualize=1), "visualize must be a boolean"),
        ("run.json", lambda value: value["data"].update(frame_stride=0), "frame_stride must"),
        ("initial.json", lambda value: value["data"]["seeds"][0].update(type="missing"), "unknown name"),
        (
            "initial.json",
            lambda value: value["data"]["seeds"][0].update(position=[9, 4, 4]),
            "within shape",
        ),
    ],
)
def test_parts_and_merged_runtime_use_strict_validation(package, filename, mutation, expected):
    value = read(package / filename)
    mutation(value)
    write(package / filename, value)
    with pytest.raises(ValueError, match=expected):
        load_experiment(package / "experiment.json")


def test_duplicate_json_keys_are_rejected_before_merge(package):
    (package / "run.json").write_text(
        '{"part_version":1,"part_kind":"run","data":{"ticks":4,"ticks":8}}', encoding="utf-8"
    )
    with pytest.raises(ValueError, match="duplicate JSON key 'ticks'"):
        load_experiment(package / "experiment.json")


@pytest.mark.parametrize(
    "limit,value,message",
    [
        ("MAX_EXPERIMENT_FILES", 2, "file limit"),
        ("MAX_EXPERIMENT_DEPTH", 1, "depth limit"),
        ("MAX_EXPERIMENT_BYTES", 32, "source byte limit"),
    ],
)
def test_host_package_work_has_explicit_bounds(monkeypatch, limit, value, message):
    monkeypatch.setattr(owner, limit, value)
    with pytest.raises(ValueError, match=message):
        load_experiment(EXAMPLE / "experiment.json")


def test_repeated_identical_seed_entries_are_instances_and_preserve_order(package):
    initial = read(package / "initial.json")
    initial["data"]["seeds"].insert(1, copy.deepcopy(initial["data"]["seeds"][0]))
    write(package / "initial.json", initial)
    parsed = load_experiment(package / "experiment.json").initial
    assert len(parsed.seeds) == 3
    assert [seed.position for seed in parsed.seeds] == [(2, 4, 4), (2, 4, 4), (6, 4, 4)]
    assert Simulation(parsed).totals() == {"quantity": (3,)}


@pytest.mark.parametrize(
    "method,part", [("is_symlink", "definitions/entities.json"), ("is_junction", "definitions")]
)
def test_link_components_are_rejected_before_capture(package, monkeypatch, method, part):
    # Inject the host link classification to exercise the portable boundary on
    # Windows installations that do not grant tests permission to create links.
    original = getattr(Path, method)
    link = package / part
    monkeypatch.setattr(Path, method, lambda self: self == link or original(self))
    with pytest.raises(ValueError, match="symbolic links or junctions"):
        load_experiment(package / "experiment.json")
