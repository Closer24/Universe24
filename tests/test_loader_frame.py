"""THE FRAME OF THE FILES READ THROUGH THE SCHEMAS (the Boss's word of 2026-09-26 22:12Z; record 2226;
ALGEBRA.md 9.117 item 2): loader/frame.py reads the universe file, the world's own keys, the bodies, the
detectors and the start file by schemas and the folders' cards; every defect refused by name, no default."""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from event_universe.core.register import discover
from event_universe.core.schema import Context
from event_universe.loader import frame
from event_universe.loader.world import parse_world_document
from event_universe.world_files import input_digest, world_files
from tests.running import family_names, string_constants, written_defaults

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
        lambda d: d["families"][0]["held"].pop("factors"),
        r"families\[0\]\.held lacks keys: factors",
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


def test_every_shipped_body_and_detector_passes_the_frames_schemas():
    """Every body and every detector of the shipped worlds passes the frame with the families
    known; a stock names a family, the checked lists are tuples."""
    families = tuple(entry["name"] for entry in shipped()["families"])
    context = Context(families)
    ahead = {"check_mode", "source"}
    count = 0
    for path in sorted((ROOT / "examples" / "events").glob("*/*.json")):
        document = json.loads(path.read_text(encoding="utf-8"))
        if not (isinstance(document, dict) and "universe" in document) or ahead & set(path.parts):
            continue
        count += 1
        bodies = frame.bodies(document["measured"], context)
        assert len(bodies) == len(document["measured"])
        for body, written in zip(bodies, document["measured"], strict=True):
            assert body["position"] == tuple(written["position"]) and body["family"] in families
            assert set(body["stocks"]) <= set(families)
        detectors = frame.detectors(document["detectors"])
        assert [d["name"] for d in detectors] == [d["name"] for d in document["detectors"]]
    assert count >= 22


def test_every_defect_of_a_body_or_a_detector_is_refused_by_name():
    """The ray law's and the retired keys as unknown keys, a missing key, a wrong kind, a
    family the universe lacks (on the body, in its stocks, in its emitter), a bad mapping."""
    good = json.loads(
        (ROOT / "examples" / "events" / "dark_body" / "bright.json").read_text(encoding="utf-8")
    )
    context = Context(tuple(entry["name"] for entry in shipped()["families"]))

    def refuses(change, match: str) -> None:
        broken = copy.deepcopy(good)
        change(broken)
        with pytest.raises(ValueError, match=match):
            frame.bodies(broken["measured"], context)
            frame.detectors(broken["detectors"])

    for key in (
        "lamp",
        "phase",
        "directions",
        "table",
        "become",
        "span",
        "wheel",
        "take",
        "coupling",
        "cavity",
    ):
        refuses(
            lambda d, key=key: d["measured"][0].__setitem__(key, 1),
            rf"measured\[0\] has unknown keys: {key} \(the keys: ",
        )
    for key in ("family", "amount", "momentum", "stocks"):
        refuses(lambda d, key=key: d["measured"][0].pop(key), rf"measured\[0\] lacks keys: {key}")
    refuses(
        lambda d: d["measured"][0].pop("position"),
        r"measured\[0\] is written by its position \(today's form\) or by its nodes .* not neither",
    )
    refuses(
        lambda d: d["measured"][0].__setitem__("family", "nobody"),
        r"measured\[0\]\.family names 'nobody', no family of the universe",
    )
    refuses(
        lambda d: d["measured"][0].__setitem__("stocks", {"nobody": 1}),
        r"measured\[0\]\.stocks key 'nobody' names 'nobody', no family",
    )
    refuses(
        lambda d: d["measured"][0].__setitem__("stocks", {"charge": 0}),
        r"measured\[0\]\.stocks\['charge'\] is 0, below its least 1",
    )
    refuses(
        lambda d: d["measured"][0].__setitem__("stocks", [1]),
        r"measured\[0\]\.stocks must be an object mapping names to values",
    )
    refuses(
        lambda d: d["measured"][0].__setitem__("momentum", [0, 0]),
        r"measured\[0\]\.momentum must be a list of 3, not of 2",
    )
    refuses(
        lambda d: d["measured"][0].__setitem__("emitter", {"family": "nobody", "twist": 0}),
        r"emitter\.family names 'nobody', no family of the universe",
    )
    refuses(
        lambda d: d["measured"][0].__setitem__("emitter", {"family": "charge", "wheel": 1, "twist": 0}),
        r"emitter has unknown keys: wheel",
    )
    refuses(
        lambda d: d["measured"][0].__setitem__("emitter", {"family": "charge"}),
        r"emitter lacks keys: twist",
    )
    refuses(
        lambda d: d["detectors"][0].__setitem__("threshold", 1),
        r"detectors\[0\] has unknown keys: threshold",
    )
    refuses(lambda d: d["detectors"][0].pop("name"), r"detectors\[0\] lacks keys: name")
    refuses(
        lambda d: d["detectors"][0].__setitem__("positions", [[0, 0]]),
        r"positions\[0\] must be a list of 3, not of 2",
    )
    with pytest.raises(ValueError, match="measured must be a list"):
        frame.bodies({}, context)
    with pytest.raises(ValueError, match="detectors must be a list"):
        frame.detectors({})


def test_a_body_in_the_laws_form_passes_the_frame_and_its_defects_are_refused_by_name():
    """A body in the law's form (its family, its Nodes with counts, its momentum, spin and moment) passes the
    frame; every defect is refused by name; world.py refuses the form until the loop reads it."""
    families = tuple(entry["name"] for entry in shipped()["families"])
    context = Context(families)
    body = {
        "family": families[-1],
        "nodes": [{"node": [1, 2, 3], "count": 5}, {"node": [1, 2, 4], "count": 7}],
        "momentum": [0, 0, -3],
    }
    (found,) = frame.bodies([body], context)
    assert found["nodes"] == ({"node": (1, 2, 3), "count": 5}, {"node": (1, 2, 4), "count": 7})
    assert found["momentum"] == (0, 0, -3) and "spin" not in found
    (found,) = frame.bodies([{**body, "spin": [0, 1, 0], "moment": [2, 0, 0]}], context)
    assert found["spin"] == (0, 1, 0) and found["moment"] == (2, 0, 0)

    def refuses(change, match: str) -> None:
        broken = copy.deepcopy(body)
        change(broken)
        with pytest.raises(ValueError, match=match):
            frame.bodies([broken], context)

    refuses(
        lambda b: b.__setitem__("position", [1, 2, 3]),
        r"measured\[0\] is written by its position \(today's form\) or by its nodes with their "
        r"counts \(the law's form\), not both",
    )
    refuses(lambda b: b.pop("nodes"), r"measured\[0\] is written by its position .* not neither")
    refuses(lambda b: b.pop("momentum"), r"measured\[0\] lacks keys: momentum")
    for key in ("amount", "stocks", "fixed", "kind", "seed", "emitter", "count"):
        refuses(
            lambda b, key=key: b.__setitem__(key, 1),
            rf"measured\[0\] has unknown keys: {key} \(the keys: family, moment, momentum, momentum_before, nodes, spin\)",
        )
    refuses(lambda b: b.__setitem__("nodes", []), r"measured\[0\]\.nodes is empty")
    refuses(
        lambda b: b["nodes"].append({"node": [1, 2, 3], "count": 1}),
        r"measured\[0\]\.nodes names the Node \[1, 2, 3\] twice",
    )
    refuses(
        lambda b: b["nodes"][0].__setitem__("count", 0),
        r"measured\[0\]\.nodes\[0\]\.count is 0, below its least 1",
    )
    refuses(
        lambda b: b["nodes"][0].__setitem__("node", [1, 2]),
        r"measured\[0\]\.nodes\[0\]\.node must be a list of 3, not of 2",
    )
    refuses(lambda b: b["nodes"][0].pop("count"), r"measured\[0\]\.nodes\[0\] lacks keys: count")
    refuses(
        lambda b: b.__setitem__("momentum", [1, 2]),
        r"measured\[0\]\.momentum must be a list of 3, not of 2",
    )
    refuses(
        lambda b: b.__setitem__("family", "nobody"),
        r"measured\[0\]\.family names 'nobody', no family of the universe",
    )
    with pytest.raises(ValueError, match=r"measured\[0\] must be an object: a body by its position"):
        frame.bodies([3], context)
    world = json.loads(
        (ROOT / "examples" / "events" / "dark_body" / "bright.json").read_text(encoding="utf-8")
    )
    world["measured"][0] = body
    with pytest.raises(
        ValueError,
        match=r"measured\[0\] is a body in the law's form \(its Nodes with their counts\): the loop "
        r"reads a body by its position until the count's line is bound to it",
    ):
        parse_world_document(world, world_files(world), input_digest(world))


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
