"""THE FRAME OF THE FILES READ THROUGH THE SCHEMAS, the loader's second cut (the Boss's word of
2026-09-26 22:12Z on the model owner's; record 2226; ALGEBRA.md 9.117 item 2: a term is one line
of the files). loader/frame.py reads the universe file, its integers by the frame's schema and
every family's entry by the folders' cards with the frame's one key, the name, and the start
file, its mode; every refusal by name, no default written (record 2089: the dipole's divisor is
the universe file's). Checked here: the shipped file and the source's fragment pass with the
weight word resolved, every genericity draw passes, each defect is refused by name, the start
file is its mode and nothing else, the world's own keys by the frame's schema with the bodies and the
universe handed on, and the frame holds no default, no family name and no
version (the acceptance tests' readers on the new module)."""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from event_universe.core.register import discover
from event_universe.loader import frame
from tests.test_genericity import SEEDS, draw
from tests.test_loader_acceptance import family_names, string_constants, written_defaults

ROOT = Path(__file__).resolve().parents[1]
UNIVERSE = ROOT / "examples" / "events" / "universe.json"
FRAGMENT = ROOT / "examples" / "events" / "source" / "universe_entries.json"
FRAME = ROOT / "src" / "event_universe" / "loader" / "frame.py"
FILE = "universe.json"


def shipped() -> dict:
    return json.loads(UNIVERSE.read_text(encoding="utf-8"))


def read(universe: dict):
    return frame.universe(FILE, {FILE: universe}, discover())


def test_the_shipped_file_and_the_sources_fragment_pass_with_the_weight_word_resolved():
    """The three shipped families and the source's entries (the word `sourced`, a card's key)
    pass the frame; matter's read of the charge at the word Lambda is the integer; the table's
    lists are read as tuples of three."""
    universe = shipped()
    universe["families"] += json.loads(FRAGMENT.read_text(encoding="utf-8"))["families"]
    entries, integers = read(universe)
    assert [entry["name"] for entry in entries] == [f["name"] for f in universe["families"]]
    assert any("sourced" in entry for entry in entries)
    assert entries[2]["reads"][1]["weight"] == integers["Lambda"] == 1
    assert entries[0]["held"]["dipole_div"] == 1 and entries[0]["parts"] == (1, 3, 6)
    for key in ("node_clock", "amplitude_bound", "momentum_unit"):
        assert integers[key] == universe["integers"][key]
    table = integers["twist_table"]
    assert table["unit"] == universe["integers"]["twist_table"]["unit"]
    assert len(table["fine"]) == 1024 and table["fine"][0] == (1, 0, 1)


@pytest.mark.parametrize("seed", SEEDS)
def test_every_genericity_draw_passes_the_frame(seed: int):
    """A draw's families on the shipped integers, as the genericity test places them."""
    universe = {"integers": shipped()["integers"], "families": draw(seed)["families"]}
    entries, _ = read(universe)
    assert len(entries) == len(universe["families"])


def test_every_defect_of_the_universe_file_is_refused_by_name():
    """An unknown or missing key at the file, the integers, an entry or a nested object; a
    wrong kind; a name the universe lacks; the divisor with no default; the table's triples;
    the files the host did not read."""
    good = shipped()

    def refuses(change, match: str) -> None:
        broken = copy.deepcopy(good)
        change(broken)
        with pytest.raises(ValueError, match=match):
            read(broken)

    refuses(lambda d: d.__setitem__("law", 1), "the universe file 'universe.json' has unknown keys: law")
    refuses(lambda d: d.pop("integers"), "lacks keys: integers")
    refuses(lambda d: d["integers"].pop("node_clock"), r"\.integers lacks keys: node_clock")
    refuses(lambda d: d["integers"].__setitem__("Mu", 1), r"\.integers has unknown keys: Mu")
    refuses(
        lambda d: d["integers"].__setitem__("Lambda", 0), r"\.integers\.Lambda is 0, below its least 1"
    )
    refuses(
        lambda d: d["integers"]["twist_table"]["fine"].__setitem__(3, [1, 0]),
        r"fine\[3\] must be a list of 3, not of 2",
    )
    refuses(lambda d: d.__setitem__("families", []), r"\.families must be a nonempty list")
    refuses(
        lambda d: d["families"][0].__setitem__("name", 3), r"families\[0\]\.name must be a word, not 3"
    )
    refuses(lambda d: d["families"][0].pop("parts"), r"families\[0\] lacks keys: parts")
    refuses(lambda d: d["families"][0].__setitem__("mass", 1), r"families\[0\] has unknown keys: mass")
    refuses(
        lambda d: d["families"][0]["held"].pop("dipole_div"),
        r"families\[0\]\.held lacks keys: dipole_div",
    )
    refuses(
        lambda d: d["families"][1].__setitem__("phase", True),
        r"families\[1\]\.phase must be one of \[1, 2\], not True",
    )
    refuses(
        lambda d: d["families"][2]["reads"][1].__setitem__("weight", "Mu"),
        r"reads\[1\]\.weight names 'Mu', no integer of the universe",
    )
    refuses(
        lambda d: d["families"][2]["reads"][1].__setitem__("family", "ions"),
        r"reads\[1\]\.family names 'ions', no family of the universe",
    )
    with pytest.raises(
        ValueError, match="universe names 'nowhere.json', no file at the repository's root"
    ):
        frame.universe("nowhere.json", {}, discover())
    with pytest.raises(ValueError, match="the universe file 'universe.json' must be a JSON object"):
        frame.universe(FILE, {FILE: []}, discover())


def test_every_shipped_world_passes_the_frames_world_schema():
    """Every shipped world of the engine passes the frame's reading of the world's keys; the
    handed keys come back as written and the frame's as checked (lists as tuples)."""
    count = 0
    ahead = {
        "check_mode",
        "source",
    }  # the worlds the loader of today does not load (AHEAD in the regression record)
    for path in sorted((ROOT / "examples" / "events").glob("*/*.json")):
        document = json.loads(path.read_text(encoding="utf-8"))
        if not (isinstance(document, dict) and "universe" in document) or ahead & set(path.parts):
            continue
        count += 1
        checked = frame.world(document)
        assert (
            checked["measured"] is document["measured"] and checked["universe"] == document["universe"]
        )
        assert checked["shape"] == tuple(document["shape"]) and checked["engine"] == document["engine"]
        assert set(checked) == set(document)
    assert count >= 22


def test_every_defect_of_the_worlds_own_keys_is_refused_by_name():
    """An unknown key (the ray law's, a retired one, a law's name), a missing key, a wrong
    kind, a face word the GameBoard lacks, a stamp without its hash; the handed keys unchecked."""
    good = json.loads((ROOT / "examples/events/dark_body/bright.json").read_text(encoding="utf-8"))

    def refuses(change, match: str) -> None:
        broken = copy.deepcopy(good)
        change(broken)
        with pytest.raises(ValueError, match=match):
            frame.world(broken)

    for key in ("suspension", "action", "meeting", "massive_rows", "directions", "detector_law", "law"):
        refuses(
            lambda d, key=key: d.__setitem__(key, 1), f"the world has unknown keys: {key} \\(the keys: "
        )
    refuses(lambda d: d.__setitem__("families", []), "the world has unknown keys: families")
    for key in ("engine", "measured", "shape", "boundary", "clock_stamp"):
        refuses(lambda d, key=key: d.pop(key), f"the world lacks keys: {key}")
    refuses(lambda d: d.__setitem__("shape", [4, 4]), r"the world\.shape must be a list of 3, not of 2")
    refuses(lambda d: d.__setitem__("ticks", -1), r"the world\.ticks is -1, below its least 0")
    refuses(lambda d: d.__setitem__("N", 1), r"the world\.N is 1, below its least 2")
    refuses(
        lambda d: d.__setitem__("massive_record", 1),
        r"the world\.massive_record must be true or false, not 1",
    )
    refuses(
        lambda d: d["boundary"].__setitem__("x", "mirror"),
        r"boundary\.x must be one of \['open', 'periodic', 'closed'\], not 'mirror'",
    )
    refuses(
        lambda d: d.__setitem__("boundary", "closed"), r"the world\.boundary must be one of \['open'\]"
    )
    refuses(lambda d: d.__setitem__("stamp", {}), r"the world\.stamp lacks keys: hash")
    refuses(lambda d: d.__setitem__("probes", [[0, 0]]), r"probes\[0\] must be a list of 3")
    with pytest.raises(ValueError, match="a world is a JSON object"):
        frame.world([])
    handed = copy.deepcopy(good)
    handed["measured"] = "not checked here"
    assert frame.world(handed)["measured"] == "not checked here"


def test_the_start_file_is_its_mode_and_nothing_else():
    assert frame.start("start.json", {"start.json": {"mode": "pin"}}) == frame.EngineStart(
        "start.json", "pin"
    )
    for document, match in (
        ({}, "the engine start file 'start.json' lacks keys: mode"),
        ({"mode": "check", "jobs": 2}, r"has unknown keys: jobs \(the keys: mode\)"),
        ({"law": "beam-v1", "mode": "check"}, "has unknown keys: law"),
        ({"mode": "maybe"}, r"mode must be one of \['check', 'pin'\], not 'maybe'"),
        ([], "the engine start file 'start.json' must be a JSON object"),
    ):
        with pytest.raises(ValueError, match=match):
            frame.start("start.json", {"start.json": document})
    with pytest.raises(
        ValueError, match="engine names 'nowhere.json', no file at the repository's root"
    ):
        frame.start("nowhere.json", {})


def test_the_frame_holds_no_default_no_family_name_and_no_version():
    """The acceptance tests' readers (tests/test_loader_acceptance.py) on the new module alone:
    no `.get(key, default)`, no string that is a family's name, no version word."""
    assert written_defaults(FRAME) == []
    names = family_names() | {"version", "schema_version"}
    assert [value for _, value in string_constants(FRAME) if value in names] == []
