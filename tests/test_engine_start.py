"""The start file and no default: every world names the start file, a key the law reads and the world leaves out is refused by name, a key the law never reads is refused by name, and the runner's own options. HOST; no pin."""

import json
import sys
from pathlib import Path

import pytest

from event_universe import world_files
from event_universe.world_files import input_stamp, parse_nature_beam_world
from tests.worlds import emitter_world

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from run_inputs import main  # noqa: E402

START = "examples/events/engine_start.json"


def refused(document: dict, match: str) -> None:
    document["stamp"] = input_stamp(document)  # the stamp over the document as edited (item 28)
    with pytest.raises(ValueError, match=match):
        parse_nature_beam_world(document)


def test_the_shipped_start_file_says_check_and_every_world_of_the_law_names_it():
    start = json.loads((ROOT / START).read_text(encoding="utf-8"))
    assert start == {"mode": "check"}  # no law's name (ALGEBRA.md #the-primitives)
    document = emitter_world(stock=1, ticks=10)
    assert document["engine"] == START
    world = parse_nature_beam_world(document)
    assert world.start is not None and world.start.mode == "check" and world.start.path == START
    for path in (ROOT / "examples/events").glob("*/*.json"):
        text = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(text, dict) and "universe" in text:  # a world of the engine
            assert text["engine"] == START, path


def test_a_missing_key_of_the_world_or_the_start_file_is_refused_by_name(tmp_path, monkeypatch):
    document = emitter_world(stock=1, ticks=10)
    del document["engine"]
    refused(document, "the world lacks keys: engine")
    for key in ("boundary",):
        broken = json.loads(json.dumps(document))
        broken["engine"] = START
        del broken[key]
        refused(broken, f"the world lacks keys: .*{key}")
    # the start file: a missing key, an unknown key, a law's name (refused as an unknown key: no law's name and no version, ALGEBRA.md #the-primitives), a wrong mode
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    start = tmp_path / "start.json"
    document["engine"] = "start.json"
    start.write_text(json.dumps({}), encoding="utf-8")
    refused(document, "lacks keys: mode")
    start.write_text(json.dumps({"mode": "check", "jobs": 2}), encoding="utf-8")
    refused(document, "unknown keys: jobs")
    start.write_text(json.dumps({"law": "beam-v1", "mode": "check"}), encoding="utf-8")
    refused(document, "unknown keys: law")
    start.write_text(json.dumps({"mode": "maybe"}), encoding="utf-8")
    refused(document, r"mode must be one of \['check', 'pin'\], not 'maybe'")
    document["engine"] = "missing.json"
    refused(document, "no file at the repository's root")
    start.write_text(json.dumps({"mode": "pin"}), encoding="utf-8")
    document["engine"] = "start.json"
    document["stamp"] = input_stamp(document)
    assert parse_nature_beam_world(document).start.mode == "pin"  # type: ignore[union-attr]


def test_a_key_the_law_reads_is_required_and_a_key_it_never_reads_is_refused():
    document = emitter_world(stock=1, ticks=10)
    # the family's pair, the block's held quanta and drive, the well's margin
    light = document["universe"][0]
    assert light["pair"] == [1, 1]
    broken = json.loads(json.dumps(document))
    del broken["universe"][0]["pair"]
    refused(broken, r"the family 'light' lacks keys: m")  # THE MASS IS ONE INTEGER: m, or the older pair
    for key in ("momentum", "stocks"):  # the body's schema (loader/frame.py, BODY)
        broken = json.loads(json.dumps(document))
        del broken["measured"][0][key]
        refused(broken, rf"measured\[0\] lacks keys: {key}")
    for key in ("ramp", "start"):  # required with a block, the loader's own rule
        broken = json.loads(json.dumps(document))
        del broken["measured"][0][key]
        refused(broken, rf"measured\[0\] lacks keys the engine reads: {key}")
    broken = json.loads(json.dumps(document))
    del broken["measured"][0]["margin"]
    refused(
        broken,
        r"measured\[0\]\.(margin is required on a well|seed as a profile is admitted only with margin)",
    )
    # the keys the law never reads
    for key, value in (("phase", 0), ("directions", [[1, 0, 0]])):
        broken = json.loads(json.dumps(document))
        broken["measured"][0][key] = value
        refused(broken, rf"measured\[0\] has unknown keys: {key}")
    held_in_place = json.loads(json.dumps(document))
    held_in_place["measured"][0]["fixed"] = True  # no body is held in place: the key is refused
    held_in_place["stamp"] = input_stamp(held_in_place)
    refused(held_in_place, r"measured\[0\] has unknown keys: fixed")
    broken = json.loads(json.dumps(document))
    broken["detectors"][0]["threshold"] = 1
    refused(broken, r"detectors\[0\] has unknown keys: threshold")
    for key, value in (("suspension", 0), ("directions", []), ("action", 1)):
        broken = json.loads(json.dumps(document))
        broken[key] = value
        refused(broken, f"the world has unknown keys: {key}")
    broken = json.loads(json.dumps(document))
    broken["universe"][0]["lifetime"] = 0
    refused(broken, r"universe\[0\]\.lifetime is 0, below its least 1")
    broken = json.loads(json.dumps(document))
    broken["universe"][0]["hand"] = 0
    refused(broken, r"universe\[0\]\.hand must be one of \[-1, 1\], not 0")


def test_the_runner_requires_jobs_and_refuses_pins_under_the_mode_check(tmp_path):
    document, source = emitter_world(stock=1, ticks=10), tmp_path / "small.json"
    source.write_text(json.dumps(document) + "\n", encoding="utf-8")
    with pytest.raises(SystemExit):
        main(["--out", str(tmp_path / "out"), str(source)])  # no --jobs
    pins = tmp_path / "pins.json"
    pins.write_text(json.dumps({"small": [{"detector": "screen", "count": 1, "band": 1}]}))
    with pytest.raises(SystemExit):
        main(["--out", str(tmp_path / "out"), "--jobs", "1", "--pins", str(pins), str(source)])
    assert main(["--out", str(tmp_path / "out"), "--jobs", "1", str(source)]) == 0
    output = json.loads((tmp_path / "out" / "small.output.json").read_text(encoding="utf-8"))
    assert output["verdict"] == "LAWFUL" and output["mode"] == "check" and output["pins"] == []
