"""THE ENGINE START FILE AND NO DEFAULT UNDER THE DETECTOR LAW (the model owner's record 2089 of
2026-09-25 through the Boss, "every flag the engine needs for a run should leave the code";
the Boss's records 2092 and 2094; ALGEBRA.md 9.83 (2) (a); BUILD.md section 26 item 57): (1)
every world of the law names the one start file by its repository path (`engine`), the file
holds the run's mode, and a missing key of either is refused by name; (2) a key the law's path
reads and the world leaves out is refused by name (the world's flags and width, a family's
pair, a block's held quanta and drive, a well's margin); (3) a key the law never reads is
refused by name (a block's fixed, phase and directions, a detector's threshold, the ray law's
suspension and direction table); (4) the runner: --jobs required, --pins refused under the mode
check; (5) the shipped start file says check. HOST; no physics, no pin."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from event_universe.events import world as loader
from event_universe.events.world import input_stamp, parse_nature_beam_world
from tests.test_emitter import emitter_world

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from run_inputs import main  # noqa: E402

START = "examples/events/engine_start.json"


def refused(document: dict, match: str) -> None:
    document["input"] = input_stamp(document)  # the stamp over the document as edited (item 28)
    with pytest.raises(ValueError, match=match):
        parse_nature_beam_world(document)


def test_the_shipped_start_file_says_check_and_every_world_of_the_law_names_it():
    start = json.loads((ROOT / START).read_text(encoding="utf-8"))
    assert start == {"law": "detector-law-v1", "mode": "check"}
    document = emitter_world(stock=1, ticks=10)
    assert document["engine"] == START
    world = parse_nature_beam_world(document)
    assert world.start is not None and world.start.mode == "check" and world.start.path == START
    for path in (ROOT / "examples/events").glob("*/*.json"):
        text = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(text, dict) and text.get("detector_law") is True:
            assert text["engine"] == START, path


def test_a_missing_key_of_the_world_or_the_start_file_is_refused_by_name(tmp_path, monkeypatch):
    document = emitter_world(stock=1, ticks=10)
    del document["engine"]
    refused(document, "the world lacks keys required under `detector_law`: engine")
    for key in ("boundary", "width", "clock_stamp", "massive_record", "body_record"):
        broken = json.loads(json.dumps(document))
        broken["engine"] = START
        del broken[key]
        refused(broken, f"the world lacks keys required under `detector_law`: .*{key}")
    # the start file: a missing key, an unknown key, another law, a wrong mode
    monkeypatch.setattr(loader, "REPOSITORY_ROOT", tmp_path)
    start = tmp_path / "start.json"
    document["engine"] = "start.json"
    start.write_text(json.dumps({"law": "detector-law-v1"}), encoding="utf-8")
    refused(document, "lacks keys: mode")
    start.write_text(
        json.dumps({"law": "detector-law-v1", "mode": "check", "jobs": 2}), encoding="utf-8"
    )
    refused(document, "unknown keys: jobs")
    start.write_text(json.dumps({"law": "beam-v1", "mode": "check"}), encoding="utf-8")
    refused(document, "declares law 'beam-v1'")
    start.write_text(json.dumps({"law": "detector-law-v1", "mode": "maybe"}), encoding="utf-8")
    refused(document, "declares mode 'maybe'")
    document["engine"] = "missing.json"
    refused(document, "no file at the repository's root")
    start.write_text(json.dumps({"law": "detector-law-v1", "mode": "pin"}), encoding="utf-8")
    document["engine"] = "start.json"
    document["input"] = input_stamp(document)
    assert parse_nature_beam_world(document).start.mode == "pin"  # type: ignore[union-attr]


def test_a_key_the_law_reads_is_required_and_a_key_it_never_reads_is_refused():
    document = emitter_world(stock=1, ticks=10)
    # the family's pair, the block's held quanta and drive, the well's margin
    light = document["families"][0]
    assert light["pair"] == [1, 1]
    broken = json.loads(json.dumps(document))
    del broken["families"][0]["pair"]
    refused(broken, r"families\[0\] lacks keys required under `detector_law`: pair")
    for key in ("momentum", "held", "ramp", "start"):
        broken = json.loads(json.dumps(document))
        del broken["measured"][0][key]
        refused(broken, rf"measured\[0\] lacks keys required under `detector_law`: {key}")
    broken = json.loads(json.dumps(document))
    del broken["measured"][0]["margin"]
    refused(
        broken,
        r"measured\[0\]\.(margin is required on a well|seed as a profile is admitted only with margin)",
    )
    # the keys the law never reads
    for key, value in (("fixed", True), ("phase", 0), ("directions", [[1, 0, 0]])):
        broken = json.loads(json.dumps(document))
        broken["measured"][0][key] = value
        refused(broken, rf"measured\[0\] declares {key}, which the detector law never reads")
    broken = json.loads(json.dumps(document))
    broken["detectors"][0]["threshold"] = 1
    refused(broken, r"detectors\[0\] declares threshold, which the detector law never reads")
    for key, value in (("suspension", 0), ("directions", []), ("action", 1)):
        broken = json.loads(json.dumps(document))
        broken[key] = value
        refused(broken, f"the world declares {key}, which the detector law never reads")
    broken = json.loads(json.dumps(document))
    broken["families"][0]["lifetime"] = 5
    refused(broken, r"families\[0\] declares lifetime, which the detector law never reads")


def test_the_runner_requires_jobs_and_refuses_pins_under_the_mode_check(tmp_path):
    document = emitter_world(stock=1, ticks=10)
    source = tmp_path / "small.json"
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
