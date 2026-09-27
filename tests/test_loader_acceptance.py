"""THE LOADER'S ACCEPTANCE TESTS, written ahead of the schema loader (the Boss's word of
2026-09-26 21:17Z on the model owner's; record 2226: one generic reader of the three files,
every primitive's schema beside its code in its folder, read from the register; record 2089:
no default written in the code; records 2172 to 2174 and 2182: no family name, no flag, no
version in the engine; ALGEBRA.md 9.120 item 1: a body is its family, its Nodes, its count per
Node and its momentum n, nothing else; 9.117 row "the source" and record 2199 item 1: the words
`sourced` and `readings`). Tests only, no line of src/. A test the loader of today fails is
marked xfail strict, naming what fails today; it turns green the day the loader lands and then
must lose its mark. Each test says which record it checks."""

from __future__ import annotations

import ast
import copy
import json
import re
from pathlib import Path

import pytest

import event_universe.world_files as world_files
from event_universe.core.register import discover
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import input_stamp, parse_nature_beam_world
from tests.test_emitter import emitter_world

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "src" / "event_universe"
UNIVERSE = ROOT / "examples" / "events" / "universe.json"
START = ROOT / "examples" / "events" / "engine_start.json"
SOURCE_FOLDER = ROOT / "examples" / "events" / "source"
VERSION_STRING = re.compile(r"-v[0-9]+$")
VERSION_WORDS = {"version", "schema_version"}


def loader_modules() -> list[Path]:
    """The loader as it stands: loader/world.py since #1236 (events/world.py before it) (record 2226);
    every module of the engine whose name is the world's reader or names a loader."""
    found = [
        path
        for path in ENGINE.rglob("*.py")
        if "__pycache__" not in path.parts and (path.name == "world.py" or "loader" in path.name)
    ]
    assert found, "no loader module under src/event_universe"
    return sorted(found)


def string_constants(path: Path) -> list[tuple[int, str]]:
    """Every string constant of the module with its line, docstrings left out."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    docstrings: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Module | ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            body = node.body
            if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant):
                docstrings.add(id(body[0].value))
    return [
        (node.lineno, node.value)
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and id(node) not in docstrings
    ]


def written_defaults(path: Path) -> list[str]:
    """Every `<obj>.get("<key>", <default>)` of the module with a default that is not None: a
    key of the files with a default written in the code (record 2089)."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    found = []
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "get"
            and len(node.args) == 2
            and isinstance(node.args[0], ast.Constant)
            and isinstance(node.args[0].value, str)
            and not (isinstance(node.args[1], ast.Constant) and node.args[1].value is None)
        ):
            found.append(f"{path.relative_to(ROOT)}:{node.lineno} {node.args[0].value!r}")
    return found


def family_names() -> set[str]:
    universe = json.loads(UNIVERSE.read_text(encoding="utf-8"))
    return {family["name"] for family in universe["families"]}


# (a) THE CLOSED LOADER: no family name, no written default, no version (records 2172 to 2174,
# 2182, 2089, 2226; the e1, e3 and e4 acceptance tests extended to the loader alone, no
# exclusion: a family's name is not a column's name either)


@pytest.mark.xfail(
    strict=True,
    reason="record 2226: the loader of today translates the universe file to the loop's families list "
    "by the keys 'charge' and 'clicks', which are family names of the tests' worlds; the switch "
    "hands the loop the checked entries and names no key",
)
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


@pytest.mark.xfail(
    strict=True,
    reason="record 2089 with record 2226: the loader of today writes defaults for the tests' inline "
    "families' keys and for `fixed`, `span` and `margin` (ten shipped bodies write no `fixed`); "
    "the switch and the generator's worlds remove them",
)
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


# (b) WHAT LOADS: a body by its four attributes alone, the word `sourced`, the word `readings`


def place(tmp_path: Path, monkeypatch, universe: dict, document: dict) -> dict:
    """The universe and the start file placed where the loader reads them, the document
    stamped; the files' words unchanged."""
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
    """The world of ALGEBRA.md 9.120 item 1: the GameBoard, its boundary, the intervals, the
    files, and one body named by its family, its Nodes, its count per Node and its momentum n;
    no well, no seed, no stop, no profile, no closed Port, no residue key of the old loader."""
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
    reason="ALGEBRA.md 9.120 item 1 with record 2226: the loop still reads N, and the loader still "
    "requires K, release, width and the flags of the old form and a body's seed, pair and side; "
    "the body by its family, Nodes, count per Node and momentum n alone comes with the loop's "
    "reads of the momentum and the spin as families (the mathematician's word on #1210)",
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
    reason="ALGEBRA.md 9.117 row 'the source' with record 2226: the loader of today refuses the "
    "family key 'sourced' as unknown; the schema loader reads it from the source folder's schema",
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
    reason="record 2199 item 1 with record 2226: the source worlds carry none of the old form's keys "
    "K, N, release, width and the flags, which the loader still requires while the loop reads them",
)
def test_b3_the_word_readings_on_the_shipped_source_world_loads():
    """Record 2199 item 1 (the output declared in one format; Main Loop's interface: a name, a
    kind and the kind's keys per reading) with 9.117 row 'the source': the shipped rest world of
    the source, whose readings each carry a name, loads as it stands."""
    document = json.loads((SOURCE_FOLDER / "source_rest.json").read_text(encoding="utf-8"))
    assert all("name" in reading for reading in document["readings"])
    parse_nature_beam_world(document)


# (c) THE SCHEMA: an unknown key refused by name, every folder's schema its own


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
    reason="record 2226 (1) and (2): the folders' cards carry no schema yet, and the loader of today "
    "writes the keys itself; the schema loader reads every key of a family's entry from a folder's card",
)
def test_c2_every_key_of_a_familys_entry_is_a_folders_schema_and_not_a_line_of_the_loader():
    """Record 2226 (1) and (2): every key a shipped family entry carries beyond its name (the
    universe file and the source's fragment) is declared by one folder's card in the register
    (its `schema`, the keys and the kinds it accepts, beside its function); the loader names
    none of those keys as a string of its own."""
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
