"""THE ONE FAMILIES FILE (ALGEBRA.md 9.83 (2), 9.85 (3), 9.79 (1); the model owner's record 2075
through the Boss, "in every experiment we put all the families into action"; BUILD.md section
26 item 59): (1) examples/events/families.json holds the universe's integers and every family as
a law with the eight attributes; every shipped world of the detector law names it as `families`
and declares no node_clock and no amplitude_bound of its own; (2) the loader translates the
file's entries and refuses by name a missing key, a wrong representation, a phase other than 2,
a self-unit other than 0, an entry with both or neither of held and clicks, a booked flag
against the derivation, a held factor other than 1, and a world that names the file under the
ray law or beside its own integers; (3) the light record's clock is its emitter's: `clock` on
the emitter, required when the given family declares none and refused when it does; (4) a small
world built with the file's entries and the same world with an inline list step bit for bit.
HOST; no physics, no pin."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from event_universe.events import world as loader
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.events.world import families_file_entries, input_stamp, parse_nature_beam_world
from tests.test_emitter import emitter_world

ROOT = Path(__file__).resolve().parents[1]
FILE = "examples/events/families.json"
ATTRIBUTES = {
    "name",
    "quantum",
    "charge",
    "pair",
    "reads",
    "representation",
    "phase",
    "self_unit",
    "booked",
}


def refused(document: dict, match: str) -> None:
    document["input"] = input_stamp(document)
    with pytest.raises(ValueError, match=match):
        parse_nature_beam_world(document)


def test_the_file_holds_the_integers_and_every_family_as_a_law_and_every_world_names_it():
    document = json.loads((ROOT / FILE).read_text(encoding="utf-8"))
    assert document["law"] == "detector-law-v1"
    assert document["integers"] == {"node_clock": 10000, "amplitude_bound": 1 << 20}
    names = [entry["name"] for entry in document["families"]]
    assert names == ["light", "matter", "well", "dark", "heavy", "muon", "point", "clicks", "charge"]
    for entry in document["families"]:
        assert ATTRIBUTES <= set(entry) and entry["representation"] == "scalar"
        assert entry["phase"] == 2 and entry["self_unit"] == 0
        assert ("held" in entry) != ("clicks" in entry)
        assert entry["booked"] is ("clicks" in entry)
        assert "phase_per_link" not in entry  # a light record's clock is its emitter's (9.85 (3))
    entries, integers = families_file_entries(FILE)
    assert integers == document["integers"] and len(entries) == 9
    assert entries[-2]["held"] == "content" and entries[-1]["held"] == "sign"
    for path in (ROOT / "examples/events").glob("*/*.json"):
        text = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(text, dict) and text.get("detector_law") is True:
            assert text["families"] == FILE, path
            assert "node_clock" not in text and "amplitude_bound" not in text, path
            world = parse_nature_beam_world(text)
            assert world.families_file == FILE and world.node_clock == 10000
            assert [family.name for family in world.families] == names


def on_the_file(document: dict, clock: list[int]) -> dict:
    """The emitter world moved onto the families file: the path, no integers of its own, the
    given clock on the emitter."""
    moved = json.loads(json.dumps(document))
    moved["families"] = FILE
    del moved["node_clock"]
    del moved["amplitude_bound"]
    for entry in moved["measured"]:
        if "emitter" in entry:
            entry["emitter"]["clock"] = clock
    moved["input"] = input_stamp(moved)
    return moved


def test_the_file_and_the_inline_list_step_bit_for_bit(tmp_path, monkeypatch):
    inline = emitter_world(stock=2, ticks=300)
    # the same entries and the test world's own integers (its A is 2^22, the shipped file's
    # 2^20), written as a families file of the test's root
    document = json.loads((ROOT / FILE).read_text(encoding="utf-8"))
    document["integers"] = {
        "node_clock": inline["node_clock"],
        "amplitude_bound": inline["amplitude_bound"],
    }
    # the test world's four families alone: the heavier kinds' rule total exceeds 2^63 at 2^22
    kept = ("light", "matter", "clicks", "charge")
    document["families"] = [entry for entry in document["families"] if entry["name"] in kept]
    (tmp_path / "families.json").write_text(json.dumps(document), encoding="utf-8")
    (tmp_path / "start.json").write_text(
        json.dumps({"law": "detector-law-v1", "mode": "check"}), encoding="utf-8"
    )
    a = DetectorLawSimulation(parse_nature_beam_world(inline))
    monkeypatch.setattr(loader, "REPOSITORY_ROOT", tmp_path)
    moved = on_the_file(inline, [512, 1])
    moved["families"] = "families.json"
    moved["engine"] = "start.json"
    moved["input"] = input_stamp(moved)
    b = DetectorLawSimulation(parse_nature_beam_world(moved))
    assert b.world.families_file == "families.json" and a.world.families_file is None
    lines_a: list[dict] = []
    lines_b: list[dict] = []
    a.record, b.record = lines_a.append, lines_b.append
    for _ in range(300):
        a.step()
        b.step()
    assert set(a.records) == set(b.records) and lines_a == lines_b and len(lines_a) > 0
    for identity, live in a.records.items():
        other = b.records[identity]
        assert np.array_equal(live.now, other.now) and np.array_equal(live.remainder, other.remainder)
    for source in ("content", "sign"):
        assert np.array_equal(a.level_of(source), b.level_of(source))


def test_the_loader_refuses_the_files_defects_and_the_worlds_second_copy(tmp_path, monkeypatch):
    document = on_the_file(emitter_world(stock=1, ticks=10), [512, 1])
    second = json.loads(json.dumps(document))
    second["node_clock"] = 10000
    refused(second, "the world declares node_clock, which the detector law never reads")
    ray = json.loads(json.dumps(document))
    ray["detector_law"] = False
    del ray["engine"]
    refused(ray, "families as a file path is admitted under `detector_law` alone")
    missing = json.loads(json.dumps(document))
    missing["families"] = "examples/events/nowhere.json"
    refused(missing, "no file at the repository's root")
    # the file's own defects, one at a time
    good = json.loads((ROOT / FILE).read_text(encoding="utf-8"))
    monkeypatch.setattr(loader, "REPOSITORY_ROOT", tmp_path)
    (tmp_path / "start.json").write_text(
        json.dumps({"law": "detector-law-v1", "mode": "check"}), encoding="utf-8"
    )
    document["engine"] = "start.json"
    document["families"] = "families.json"

    def refuses(change, match):
        broken = json.loads(json.dumps(good))
        change(broken)
        (tmp_path / "families.json").write_text(json.dumps(broken), encoding="utf-8")
        refused(json.loads(json.dumps(document)), match)

    refuses(lambda d: d["integers"].pop("node_clock"), "integers must hold exactly")
    refuses(
        lambda d: d["families"][0].pop("representation"), r"families\[0\] lacks keys: representation"
    )
    refuses(
        lambda d: d["families"][0].__setitem__("representation", "vector"),
        "representation must be one of",
    )
    refuses(lambda d: d["families"][0].__setitem__("phase", 1), "phase must be 2")
    refuses(lambda d: d["families"][0].__setitem__("self_unit", 24), "self_unit must be 0")
    refuses(
        lambda d: d["families"][0].__setitem__("held", {"count": "content", "factor": 1}),
        "exactly one of held",
    )
    refuses(
        lambda d: d["families"][0].__setitem__("booked", False),
        "booked must be true on a family of records",
    )
    refuses(
        lambda d: d["families"][-1].__setitem__("booked", True), "booked must be false on a held family"
    )
    refuses(lambda d: d["families"][-1]["held"].__setitem__("factor", 4), "held.factor must be 1")
    refuses(lambda d: d.__setitem__("law", "beam-v1"), "declares law 'beam-v1'")
    (tmp_path / "families.json").write_text(json.dumps(good), encoding="utf-8")
    document["input"] = input_stamp(document)
    assert parse_nature_beam_world(document).families_file == "families.json"


def test_the_given_clock_is_the_emitters_when_the_family_declares_none():
    document = on_the_file(emitter_world(stock=1, ticks=10), [512, 1])
    world = parse_nature_beam_world(document)
    emitter = world.measured[0].block.emitter  # type: ignore[union-attr]
    assert emitter is not None and emitter.clock == (512, 1) and emitter.train is not None
    assert emitter.train.clock == (512, 1) and emitter.train.wavelength == 4
    without = json.loads(json.dumps(document))
    del without["measured"][0]["emitter"]["clock"]
    refused(
        without, r"measured\[0\]\.emitter\.clock is required: the given family 'light' declares no clock"
    )
    inline = emitter_world(stock=1, ticks=10)
    inline["measured"][0]["emitter"]["clock"] = [512, 1]
    refused(
        inline, r"measured\[0\]\.emitter\.clock is refused: the given family 'light' declares its own"
    )
