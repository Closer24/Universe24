"""THE FRAME OF THE FILES READ THROUGH THE SCHEMAS (the Boss's word of 2026-09-26 22:12Z; record 2226;
ALGEBRA.md #the-primitives): loader/frame.py reads the universe file, the world's own keys, the bodies, the
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
from tests.worlds import SOURCED

ROOT = Path(__file__).resolve().parents[1]
REGISTER = discover()  # the folders' cards, the keys they declare at "a body" among them
UNIVERSE = ROOT / "examples" / "events" / "universe.json"
# one sourced entry (the word `sourced`, a card's key), as the retired source folder wrote it
FRAME = ROOT / "src" / "event_universe" / "loader" / "frame.py"
FILE = "universe.json"


def shipped() -> dict:
    return json.loads(UNIVERSE.read_text(encoding="utf-8"))


def read(universe: dict):
    return frame.universe(FILE, {FILE: universe}, discover())


def test_the_shipped_file_and_a_sourced_entry_pass_with_the_weight_word_resolved():
    """The three shipped families and a sourced entry pass the frame; matter's read of the charge at the word Lambda is the integer; the table's lists are read as tuples of three."""
    universe = shipped()
    universe["families"] += [dict(SOURCED)]
    entries, integers = read(universe)
    assert [entry["name"] for entry in entries] == [f["name"] for f in universe["families"]]
    assert any("sourced" in entry for entry in entries)
    assert entries[2]["reads"][1]["weight"] == integers["Lambda"] == 1
    assert entries[0]["held"]["dipole_div"] == 1 and entries[0]["parts"] == (1, 3, 6)
    for key in ("node_clock", "momentum_unit"):
        assert integers[key] == universe["integers"][key]
    table = integers["twist_table"]
    assert table["unit"] == universe["integers"]["twist_table"]["unit"]
    assert len(table["fine"]) == 1024 and table["fine"][0] == (1, 0, 1)


def test_every_defect_of_the_universe_file_is_refused_by_name():
    """An unknown or missing key at the file, the integers, an entry or a nested object; a wrong kind; a name the universe lacks; the divisor with no default; the table's triples; the files the host did not read."""
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


def test_every_world_file_passes_the_frames_world_schema():
    """Every world file of the repository (the rule tests' own `tests/light_clock.json` and every world under `examples/events/`, the worlds of record as they land) passes the frame's reading of the world's keys; the handed keys come back as written and the frame's as checked (lists as tuples)."""
    count = 0
    paths = [
        ROOT / "tests" / "light_clock.json",
        *sorted((ROOT / "examples" / "events").glob("**/*.json")),
    ]
    for path in paths:
        document = json.loads(path.read_text(encoding="utf-8"))
        if not (isinstance(document, dict) and "universe" in document):
            continue
        count += 1
        checked = frame.world(document)
        assert (
            checked["measured"] is document["measured"] and checked["universe"] == document["universe"]
        )
        assert checked["shape"] == tuple(document["shape"]) and checked["engine"] == document["engine"]
        assert set(checked) == set(document)
    assert count >= 1


def test_every_defect_of_the_worlds_own_keys_is_refused_by_name():
    """An unknown key (the ray law's, a retired one, a law's name), a missing key, a wrong kind, a face word the GameBoard lacks, a stamp without its hash; the handed keys unchecked."""
    good = json.loads((ROOT / "tests/light_clock.json").read_text(encoding="utf-8"))

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
    for key in ("engine", "measured", "shape", "boundary"):
        refuses(lambda d, key=key: d.pop(key), f"the world lacks keys: {key}")
    refuses(lambda d: d.__setitem__("shape", [4, 4]), r"the world\.shape must be a list of 3, not of 2")
    refuses(lambda d: d.__setitem__("ticks", -1), r"the world\.ticks is -1, below its least 0")
    refuses(lambda d: d.__setitem__("N", 1), r"the world\.N is 1, below its least 2")
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


def test_every_body_and_detector_of_a_world_in_todays_form_passes_the_frames_schemas():
    """Every body and every detector of the repository's world files in today's form (a body by its position: the rule tests' own `tests/light_clock.json`; a world of record in the law's form declares its bodies by their Nodes and is read by the law's-form schema) passes the frame with the families known; a stock names a family, the checked lists are tuples."""
    families = tuple(entry["name"] for entry in shipped()["families"])
    context = Context(families)
    count = 0
    paths = [
        ROOT / "tests" / "light_clock.json",
        *sorted((ROOT / "examples" / "events").glob("**/*.json")),
    ]
    for path in paths:
        document = json.loads(path.read_text(encoding="utf-8"))
        if not (isinstance(document, dict) and "universe" in document):
            continue
        if any("position" not in body for body in document["measured"]):
            continue
        count += 1
        bodies = frame.bodies(document["measured"], context, REGISTER)
        assert len(bodies) == len(document["measured"])
        for body, written in zip(bodies, document["measured"], strict=True):
            assert body["position"] == tuple(written["position"]) and body["family"] in families
            assert set(body["stocks"]) <= set(families)
        detectors = frame.detectors(document["detectors"])
        assert [d["name"] for d in detectors] == [d["name"] for d in document["detectors"]]
    assert count >= 1


def test_every_defect_of_a_body_or_a_detector_is_refused_by_name():
    """The ray law's and the retired keys as unknown keys, a missing key, a wrong kind, a family the universe lacks (on the body, in its stocks, in its emitter), a bad mapping."""
    good = json.loads((ROOT / "tests" / "light_clock.json").read_text(encoding="utf-8"))
    context = Context(tuple(entry["name"] for entry in shipped()["families"]))
    retired = (
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
    )
    S = lambda key, value: lambda d: d["measured"][0].__setitem__(key, value)  # noqa: E731
    D = lambda key, value: lambda d: d["detectors"][0].__setitem__(key, value)  # noqa: E731
    defects = [(S(k, 1), rf"measured\[0\] has unknown keys: {k} \(the keys: ") for k in retired]
    for k in ("family", "amount", "momentum", "momentum_before", "stocks"):
        defects.append((lambda d, k=k: d["measured"][0].pop(k), rf"measured\[0\] lacks keys: {k}"))
    defects += [
        (lambda d: d["measured"][0].pop("spin_before"), r"declares spin without spin_before"),
        (
            lambda d: d["measured"][0].pop("position"),
            r"by its position \(today's form\) or by its nodes .* neither",
        ),
        (S("family", "nobody"), r"\.family names 'nobody', no family of the universe"),
        (S("stocks", {"nobody": 1}), r"\.stocks key 'nobody' names 'nobody', no family"),
        (S("stocks", {"charge": 0}), r"\.stocks\['charge'\] is 0, below its least 1"),
        (S("stocks", [1]), r"\.stocks must be an object mapping names to values"),
        (S("momentum", [0, 0]), r"\.momentum must be a list of 3, not of 2"),
        (S("emitter", {"family": "nobody"}), r"emitter\.family names 'nobody', no family"),
        (S("emitter", {"family": "charge", "wheel": 1}), r"emitter has unknown keys: wheel"),
        (S("emitter", {"family": "charge", "twist": 0}), r"emitter has unknown keys: twist"),
        (D("threshold", 1), r"detectors\[0\] has unknown keys: threshold"),
        (lambda d: d["detectors"][0].pop("name"), r"detectors\[0\] lacks keys: name"),
        (D("positions", [[0, 0]]), r"positions\[0\] must be a list of 3, not of 2"),
    ]
    for change, match in defects:
        broken = copy.deepcopy(good)
        change(broken)
        with pytest.raises(ValueError, match=match):
            frame.bodies(broken["measured"], context, REGISTER)
            frame.detectors(broken["detectors"])
    with pytest.raises(ValueError, match="measured must be a list"):
        frame.bodies({}, context, REGISTER)
    with pytest.raises(ValueError, match="detectors must be a list"):
        frame.detectors({})


def test_a_body_in_the_laws_form_passes_the_frame_and_its_defects_are_refused_by_name():
    """A body in the law's form (its family, its Nodes with counts, its momentum and spin at two levels, its moment, its stocks and its emitter) passes the frame; every defect is refused by name; world.py builds its block: the corner the Nodes' lowest per axis, the extents their box, the Nodes and counts kept, the count their sum; a giving body in the form is refused until the generator writes its record."""
    families = tuple(entry["name"] for entry in shipped()["families"])
    context = Context(families)
    body = {
        "family": families[-1],
        "nodes": [{"node": [1, 2, 3], "count": 5}, {"node": [1, 2, 4], "count": 7}],
        "momentum": [0, 0, -3],
        "momentum_before": [0, 0, -2],
    }
    (found,) = frame.bodies([body], context, REGISTER)
    assert found["nodes"] == ({"node": (1, 2, 3), "count": 5}, {"node": (1, 2, 4), "count": 7})
    assert found["momentum"] == (0, 0, -3) and found["momentum_before"] == (0, 0, -2)
    assert "spin" not in found and "stocks" not in found and "emitter" not in found
    spinning = {**body, "spin": [0, 1, 0], "spin_before": [0, 1, 1], "moment": [2, 0, 0]}
    (found,) = frame.bodies([spinning], context, REGISTER)
    assert found["spin"] == (0, 1, 0) and found["spin_before"] == (0, 1, 1)
    giver = {"family": families[0], "weight": 3}
    stocks = {families[0]: 4}
    (found,) = frame.bodies([{**body, "stocks": stocks, "emitter": giver}], context, REGISTER)
    assert found["stocks"] == stocks and found["emitter"] == giver
    (found,) = frame.bodies([{**body, "emitter": {**giver, "family": families[-1]}}], context, REGISTER)
    assert found["emitter"]["family"] == families[-1]
    turned = {"polariser": {"angle": [2, 1], "sets": ["along", "across"]}}  # a card's key at "a body"
    (found,) = frame.bodies([{**body, **turned}], context, REGISTER)
    assert found["polariser"] == {"angle": (2, 1), "sets": ("along", "across")}

    def refuses(change, match: str) -> None:
        broken = copy.deepcopy(body)
        change(broken)
        with pytest.raises(ValueError, match=match):
            frame.bodies([broken], context, REGISTER)

    known = ", ".join(sorted(frame.counted_kind(REGISTER).keys))  # the frame's and the cards'
    S = lambda key, value: lambda b: b.__setitem__(key, value)  # noqa: E731
    E = lambda **keys: S("emitter", {**giver, **keys})  # noqa: E731
    for change, match in (
        (S("position", [1, 2, 3]), r"by its position \(today's form\) or by its nodes .* not both"),
        (lambda b: b.pop("nodes"), r"is written by its position .* not neither"),
        (lambda b: b.pop("momentum"), r"measured\[0\] lacks keys: momentum"),
        (lambda b: b.pop("momentum_before"), r"lacks keys: momentum_before"),
        (S("spin_before", [0, 0, 0]), r"declares spin_before without spin: the spin's two levels"),
        (S("seed", 1), rf"has unknown keys: seed \(the keys: {known}\)"),
        (S("period", 1), rf"has unknown keys: period \(the keys: {known}\)"),
        (S("polariser", {"angle": [2, 1]}), r"\.polariser lacks keys: sets"),
        (E(twist=1), r"\.emitter has unknown keys: twist "),
        (E(period=1), r"\.emitter has unknown keys: period "),
        (S("emitter", {**giver, "norm": 5}), r"\.emitter has unknown keys: norm"),
        (E(weight=0), r"\.emitter\.weight is 0, below its least 1"),
        (E(family="nobody"), r"\.emitter\.family names 'nobody', no family"),
        (S("emitter", giver), rf"gives '{families[0]}', a family the body neither is nor stocks"),
        (S("stocks", {families[0]: 0}), rf"\.stocks\['{families[0]}'\] is 0, below its least 1"),
        (S("stocks", {"nobody": 1}), r"\.stocks key 'nobody' names 'nobody', no family"),
        (S("nodes", []), r"\.nodes is empty"),
        (
            lambda b: b["nodes"].append({"node": [1, 2, 3], "count": 1}),
            r"names the Node \[1, 2, 3\] twice",
        ),
        (
            lambda b: b["nodes"][0].__setitem__("count", 0),
            r"\.nodes\[0\]\.count is 0, below its least 1",
        ),
        (lambda b: b["nodes"][0].__setitem__("node", [1, 2]), r"\.nodes\[0\]\.node must be a list of 3"),
        (lambda b: b["nodes"][0].pop("count"), r"\.nodes\[0\] lacks keys: count"),
        (S("momentum", [1, 2]), r"\.momentum must be a list of 3, not of 2"),
        (S("family", "nobody"), r"\.family names 'nobody', no family of the universe"),
    ):
        refuses(change, match)
    with pytest.raises(ValueError, match=r"measured\[0\] must be an object: a body by its position"):
        frame.bodies([3], context, REGISTER)
    world = json.loads((ROOT / "tests" / "light_clock.json").read_text(encoding="utf-8"))
    nodes = [
        {"node": [1, 0, 0], "count": 5},
        {"node": [1, 2, 0], "count": 7},
        {"node": [3, 1, 0], "count": 1},
    ]  # free Nodes of the light clock's chain [760, 3, 3], its bodies from x = 629
    counted = {**spinning, "family": families[1], "nodes": nodes}

    def load(**change):
        world["measured"][0] = {**counted, **change}
        world["stamp"] = {"hash": input_digest(world)}
        return parse_world_document(world, world_files(world), input_digest(world)).measured[0]

    entry = load()
    assert (entry.position, entry.block.extents, entry.amount) == ((1, 0, 0), (3, 3, 1), 13)
    assert entry.block.nodes == ((1, 0, 0), (1, 2, 0), (3, 1, 0)) and entry.block.counts == (5, 7, 1)
    assert (
        entry.block.spin == (0, 1, 0) and entry.block.moment == (2, 0, 0) and entry.block.declared == {}
    )
    assert load(**turned).block.declared == {"polariser": {"angle": (2, 1), "sets": ("along", "across")}}
    with pytest.raises(ValueError, match=r"measured\[0\]\.emitter on a body in the law's form"):
        load(emitter={**giver, "family": families[1]})
    with pytest.raises(
        ValueError, match=r"measured\[0\]: the family 'matter' declares no pair, and a body"
    ):
        load(family=families[-1])
    with pytest.raises(ValueError, match=r"measured\[0\]\.nodes names the Node \[1, 0, 0\] twice"):
        load(nodes=[*nodes, {"node": [1, 0, 0], "count": 2}])


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
    """The acceptance tests' readers (tests/test_loader_acceptance.py) on the new module alone: no `.get(key, default)`, no string that is a family's name, no version word."""
    assert written_defaults(FRAME) == []
    names = family_names() | {"version", "schema_version"}
    assert [value for _, value in string_constants(FRAME) if value in names] == []
