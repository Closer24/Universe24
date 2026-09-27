"""THE LOADER'S ACCEPTANCE TESTS, written ahead of the schema loader (the Boss's word of 2026-09-26
21:17Z; records 2226, 2089, 2172 to 2174, 2182; ALGEBRA.md 9.120 item 1 and 9.117 row "the source"):
tests only; a test the loader fails is xfail strict naming what holds it and loses its mark when green."""

from __future__ import annotations

import copy
import json
import re
from pathlib import Path

import pytest

import event_universe.world_files as world_files
from event_universe.core.register import discover
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import input_stamp, parse_nature_beam_world
from tests.running import family_names, string_constants, written_defaults
from tests.worlds import emitter_world

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "src" / "event_universe"
UNIVERSE = ROOT / "examples" / "events" / "universe.json"
START = ROOT / "examples" / "events" / "engine_start.json"
SOURCE_FOLDER = ROOT / "examples" / "events" / "source"
VERSION_STRING = re.compile(r"-v[0-9]+$")
VERSION_WORDS = {"version", "schema_version"}


def loader_modules() -> list[Path]:
    """The loader as it stands: loader/world.py and every module whose name names a loader (record 2226)."""
    found = [
        path
        for path in ENGINE.rglob("*.py")
        if "__pycache__" not in path.parts and (path.name == "world.py" or "loader" in path.name)
    ]
    assert found, "no loader module under src/event_universe"
    return sorted(found)


# (a) THE CLOSED LOADER: no family name, no written default, no version (records 2172 to 2174,
# 2182, 2089, 2226)


def test_a1_the_loader_holds_no_family_name_of_the_universe():
    """Record 2226 with records 2172 to 2174: no string constant of the loader is a family name
    of the universe file, with no exclusion."""
    names = family_names()
    offending = [
        f"{path.relative_to(ROOT)}:{line} {value!r}"
        for path in loader_modules()
        for line, value in string_constants(path)
        if value in names
    ]
    assert offending == [], offending


def test_a2_the_loader_writes_no_default_for_a_key_of_the_files():
    """Record 2089 (every default and flag out of the engine's code into the files) with record
    2226 (a missing key is refused by name from the schema): the loader has no `.get(key,
    default)` with a default that is not None."""
    defaults = [line for path in loader_modules() for line in written_defaults(path)]
    assert defaults == [], defaults


# green since the frame's cut of the world's keys (the earlier engines' key sets left world.py)
def test_a3_the_loader_holds_no_version_and_no_schema_version():
    """Record 2182 (no flag and no version in the engine) with record 2226: no string constant
    of the loader is a version string (`<name>-v<digits>`), the word 'version' or the word
    'schema_version'."""
    offending = [
        f"{path.relative_to(ROOT)}:{line} {value!r}"
        for path in loader_modules()
        for line, value in string_constants(path)
        if VERSION_STRING.search(value) or value in VERSION_WORDS
    ]
    assert offending == [], offending


def place(tmp_path: Path, monkeypatch, universe: dict, document: dict) -> dict:
    """The universe and the start file placed where the loader reads them, the document stamped."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    (tmp_path / "universe.json").write_text(json.dumps(universe), encoding="utf-8")
    (tmp_path / "start.json").write_text(START.read_text(encoding="utf-8"), encoding="utf-8")
    placed = copy.deepcopy(document)
    for key in ("node_clock", "amplitude_bound", "momentum_unit"):
        placed.pop(key, None)  # the universe's integers, never a world's (record 2089)
    placed["universe"] = "universe.json"
    placed["engine"] = "start.json"
    placed.pop("stamp", None)
    placed["stamp"] = input_stamp(placed)
    return placed


def body_world() -> dict:
    """The world of ALGEBRA.md 9.120 item 1: one body by its family, Nodes, count per Node and momentum."""
    return {
        "shape": [16, 1, 1],
        "boundary": {"x": "closed", "y": "periodic", "z": "periodic"},
        "ticks": 4,
        "measured": [
            {
                "family": "matter",
                "nodes": [[5, 0, 0], [6, 0, 0]],
                "count": 1,
                "momentum": [0, 0, 0],
            }
        ],
        "detectors": [],
    }


@pytest.mark.xfail(
    strict=True,
    reason="ALGEBRA.md 9.120 item 1 with record 2226: the frame reads the body's form (#1221) and "
    "the loop still reads N, age_bound, clock_stamp and the flags massive_record and body_record, "
    "which the world of 9.120 does not name; the count's line is not bound in the loop (path B, "
    "the mathematician's word on #1210), so `world.py` refuses the form by name",
)
def test_b1_a_body_declared_by_its_family_nodes_count_and_momentum_alone_loads_and_runs(
    tmp_path, monkeypatch
):
    """ALGEBRA.md 9.120 item 1 (records 2243, 2244): the world file names the body's family, its
    Nodes, its count per Node and its momentum n, and nothing else; it loads on the shipped
    universe and steps."""
    universe = json.loads(UNIVERSE.read_text(encoding="utf-8"))
    placed = place(tmp_path, monkeypatch, universe, body_world())
    simulation = DetectorLawSimulation(parse_nature_beam_world(placed))
    simulation.step()
    assert simulation.leaks() == []


@pytest.mark.xfail(
    strict=True,
    reason="ALGEBRA.md 9.117 row 'the source' with record 2226: the frame reads `sourced` from the "
    "source folder's card (#1206) and `world.py` carries it as the family's source term (#1236); "
    "the fragment's `control` family declares neither held, clicks nor sourced, and the law "
    "(9.86 (2)) refuses a family that does none: the unsourced control waits on the owner's word",
)
def test_b2_the_word_sourced_on_a_family_of_the_universe_loads(tmp_path, monkeypatch):
    """ALGEBRA.md 9.117 row 'the source', 9.108 items 3 and 11 (record 2217): the universe with
    the source's fragment (`sourced` {of, weight, scale} and the table form with `cap`) loads,
    and the emitter's unit world runs on it with every family on."""
    universe = json.loads(UNIVERSE.read_text(encoding="utf-8"))
    fragment = json.loads((SOURCE_FOLDER / "universe_entries.json").read_text(encoding="utf-8"))
    universe["families"] = universe["families"] + fragment["families"]
    assert any("sourced" in entry for entry in fragment["families"])
    placed = place(tmp_path, monkeypatch, universe, emitter_world(stock=1, ticks=4))
    simulation = DetectorLawSimulation(parse_nature_beam_world(placed))
    assert [f.name for f in simulation.families] == [f["name"] for f in universe["families"]]
    simulation.step()
    assert simulation.leaks() == []


@pytest.mark.xfail(
    strict=True,
    reason="record 2199 item 1 with record 2226: K, release and width are gone (#1236); the source "
    "worlds still carry none of N, age_bound, clock_stamp, massive_record and body_record, "
    "which the loader requires while the loop reads them",
)
def test_b3_the_word_readings_on_the_shipped_source_world_loads():
    """Record 2199 item 1 (the output declared in one format; Main Loop's interface: a name, a
    kind and the kind's keys per reading) with 9.117 row 'the source': the shipped rest world of
    the source, whose readings each carry a name, loads as it stands."""
    document = json.loads((SOURCE_FOLDER / "source_rest.json").read_text(encoding="utf-8"))
    assert all("name" in reading for reading in document["readings"])
    parse_nature_beam_world(document)


def test_c1_an_unknown_key_is_refused_by_name_on_the_world_the_universe_and_a_body(
    tmp_path, monkeypatch
):
    """Record 2226 (2): an unknown key of the world, of a family's entry or of a body is refused
    by name, never read silently."""
    universe = json.loads(UNIVERSE.read_text(encoding="utf-8"))
    world = emitter_world(stock=1, ticks=4)
    with pytest.raises(ValueError, match="nonsense_world_key"):
        parse_nature_beam_world(
            place(tmp_path, monkeypatch, universe, {**world, "nonsense_world_key": 1})
        )
    odd = copy.deepcopy(universe)
    odd["families"][0]["nonsense_attribute"] = 1
    with pytest.raises(ValueError, match="nonsense_attribute"):
        parse_nature_beam_world(place(tmp_path, monkeypatch, odd, world))
    body = copy.deepcopy(world)
    body["measured"][0]["nonsense_body_key"] = 1
    with pytest.raises(ValueError, match="nonsense_body_key"):
        parse_nature_beam_world(place(tmp_path, monkeypatch, universe, body))


@pytest.mark.xfail(
    strict=True,
    reason="record 2226 (1) and (2): every key of a shipped family's entry is one folder's card "
    "(#1206, #1236) but `spins_step`, the frame's until #1203's card lands; `world.py` still builds the loop's families "
    "from the checked entries by the cards' keys (held, clicks, reads, parts, phase, sign, "
    "self_source, pair) and reads a body's and an emitter's `pair`, the same word",
)
def test_c2_every_key_of_a_familys_entry_is_a_folders_schema_and_not_a_line_of_the_loader():
    """Record 2226 (1) and (2): every key of a shipped family's entry is one folder's card; the loader
    names none of those keys as a string of its own."""
    register = discover()
    words = {
        key
        for declaration in register.declarations.values()
        for key in (getattr(declaration, "schema", None) or ())
    }
    universe = json.loads(UNIVERSE.read_text(encoding="utf-8"))
    fragment = json.loads((SOURCE_FOLDER / "universe_entries.json").read_text(encoding="utf-8"))
    keys = {key for entry in universe["families"] + fragment["families"] for key in entry} - {"name"}
    assert keys <= words, f"keys of a family's entry no folder declares: {sorted(keys - words)}"
    offending = [
        f"{path.relative_to(ROOT)}:{line} {value!r}"
        for path in loader_modules()
        for line, value in string_constants(path)
        if value in words
    ]
    assert offending == [], offending
