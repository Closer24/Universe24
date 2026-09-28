"""THE LOADER'S ACCEPTANCE TESTS (the Boss's word of 2026-09-26 21:17Z; records 2226, 2089, 2172 to 2174, 2182)."""

from __future__ import annotations

import copy
import json
import re
from pathlib import Path

import pytest

import event_universe.world_files as world_files
from event_universe.core.register import discover
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.loader.mode import period_by_the_rule
from event_universe.world_files import input_stamp, load_world, parse_nature_beam_world
from tests.running import family_names, string_constants, written_defaults
from tests.worlds import SOURCED, emitter_world

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "src" / "event_universe"
UNIVERSE = ROOT / "examples" / "events" / "universe.json"
GENERATED = ROOT / "examples" / "events" / "experiments" / "universe.json"  # matter's pair declared
START = ROOT / "examples" / "events" / "engine_start.json"
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


# (a) THE CLOSED LOADER: no family name, no written default, no version (records 2172 to 2174, 2182, 2089, 2226)


def test_a1_the_loader_holds_no_family_name_of_the_universe():
    """Record 2226 with records 2172 to 2174: no string constant of the loader is a family name of the universe file."""
    names = family_names()
    offending = [
        f"{path.relative_to(ROOT)}:{line} {value!r}"
        for path in loader_modules()
        for line, value in string_constants(path)
        if value in names
    ]
    assert offending == [], offending


def test_a2_the_loader_writes_no_default_for_a_key_of_the_files():
    """Records 2089 and 2226 (every default out of the code, a missing key refused by name): no `.get(key, default)` with a default that is not None."""
    defaults = [line for path in loader_modules() for line in written_defaults(path)]
    assert defaults == [], defaults


def test_a3_the_loader_holds_no_version_and_no_schema_version():
    """Records 2182 and 2226: no string constant of the loader is a version string (`<name>-v<digits>`), 'version' or 'schema_version'."""
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
    placed["stamp"] = input_stamp(placed)
    return placed


def body_world() -> dict:
    """#the-stable-body: one body by its family, Nodes with counts and momentum, a card's key, a set on its own Nodes."""
    return {
        "shape": [16, 1, 1],
        "boundary": {"x": "closed", "y": "periodic", "z": "periodic"},
        "ticks": 4,
        "N": 64,
        "measured": [
            {
                "family": "matter",
                "nodes": [{"node": [5, 0, 0], "count": 1}, {"node": [6, 0, 0], "count": 1}],
                "momentum": [0, 0, 0],
                "momentum_before": [0, 0, 0],
                "polariser": {"angle": [2, 1], "sets": ["rest", "strip"]},
            }
        ],
        "detectors": [{"name": "strip", "positions": [[6, 0, 0]]}],
    }


def test_b1_a_body_declared_by_its_family_nodes_count_and_momentum_alone_loads_and_runs(
    tmp_path, monkeypatch
):
    """#the-stable-body: the body by family, Nodes with counts and momentum loads and steps; Q the signed sum of its
    counts by the row's `sign`; the set on its own Node its own; the card's key on `declared`; the pace bound per Node."""
    universe = json.loads(GENERATED.read_text(encoding="utf-8"))
    next(row for row in universe["families"] if row["name"] == "matter")["sign"] = -1
    world = parse_nature_beam_world(place(tmp_path, monkeypatch, universe, body_world()))
    entry, (strip,) = world.measured[0], world.detectors
    assert entry.block.declared == {"polariser": {"angle": (2, 1), "sets": ("rest", "strip")}}
    assert entry.block.q == 0
    assert sum(f.charge[0] * h for f, h in zip(world.families, entry.held, strict=True)) == -2
    assert (strip.positions, strip.block) == (((6, 0, 0),), 0)
    simulation = DetectorLawSimulation(world)
    assert simulation.step() is None and simulation.leaks() == []
    wide = (
        body_world()
    )  # the pace bound per Node (#the-paces): six Nodes at 2,000 load, one at Gamma is refused
    wide["measured"][0]["nodes"] = [{"node": [x, 0, 0], "count": 2000} for x in range(4, 10)]
    loaded = parse_nature_beam_world(place(tmp_path, monkeypatch, universe, wide))
    assert sum(loaded.measured[0].held) == 12_000
    wide["measured"][0]["nodes"][0]["count"] = 10000  # read over the row's divisor: 10000 div 40000 = 0
    parse_nature_beam_world(place(tmp_path, monkeypatch, universe, wide))
    for row in [row for row in universe["families"] if "held" in row]:
        row["held"] = {**row["held"], "divisor": 1}
    with pytest.raises(ValueError, match="the pace of 'charge' could reach 0 .* to 10000"):
        parse_nature_beam_world(place(tmp_path, monkeypatch, universe, wide))


def test_b2_a_giving_body_in_the_laws_form_takes_its_own_record_from_the_mode_file(
    tmp_path, monkeypatch
):
    """#what-a-body-is, #the-primitives (the recoil's row): a giving body by its Nodes takes its profile, clock and
    twist from the mode file beside the world (this world's by `world_digest`), its receiver a list; defects refused by name."""
    world, universe = body_world(), json.loads(GENERATED.read_text(encoding="utf-8"))
    world["N"] = 1024  # the given clock [512, 1] whole in the wavelength (the loop's L)
    giver = {"family": "charge", "weight": 1, "receiver": ["strip"]}
    world["measured"][0].update(emitter=giver, stocks={"charge": 4}, moment=[0, 0, 1])
    placed = place(tmp_path, monkeypatch, universe, world)
    (tmp_path / "giver.json").write_text(json.dumps(placed), encoding="utf-8")
    profile = [0] * 5 + [1000, 1000] + [0] * 9
    entry = {"family": "matter", "pair": [800, 1200], "profile": profile, "clock": [1530, 1000]}
    mode = {"world_digest": placed["stamp"]["hash"], "bodies": [{**entry, "twist": 45875}]}
    big = {"profile": [v << 40 for v in profile], "clock": [3 << 49, 1 << 50]}  # above the derived A

    def loaded(change=None):
        broken = copy.deepcopy(mode)
        if change is not None:
            change(broken)
        (tmp_path / "giver.mode.json").write_text(json.dumps(broken), encoding="utf-8")
        return load_world(tmp_path / "giver.json")

    with pytest.raises(ValueError, match="from the mode file .* no entry"):
        load_world(tmp_path / "giver.json")
    block = loaded().measured[0].block
    assert (block.clock, block.twist, block.seed) == ((1530, 1000), 45875, 1000)
    assert block.profile[5:7] == (1000, 1000) and block.emitter.receiver == ("strip",)
    assert block.emitter.period == period_by_the_rule(1530, 1000)
    B = lambda key, value: lambda m: m["bodies"][0].__setitem__(key, value)  # noqa: E731
    defects = (
        (lambda m: m.__setitem__("world_digest", "0" * 64), "is not this world's digest"),
        (lambda m: m["bodies"][0].pop("twist"), "from the mode file .* no twist"),
        (B("family", "charge"), "the body of 'matter'"),
        (B("clock", [1530, 999]), "at least the profile's amplitude 1000"),
        (lambda m: m["bodies"][0].update(big), "above the world's amplitude bound"),
        (lambda m: m.__setitem__("bodies", []), "bodies must be 1 objects"),
    )
    for change, match in defects:
        with pytest.raises(ValueError, match=match):
            loaded(change)


def test_c1_an_unknown_key_is_refused_by_name_on_the_world_the_universe_and_a_body(
    tmp_path, monkeypatch
):
    """Record 2226 (2): an unknown key of the world, of a family's entry or of a body is refused by name, never read silently."""
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
    reason="record 2226 (1) and (2): `spins_step` is the frame's until #1203's card lands; `world.py` still builds "
    "the loop's families from the checked entries by the cards' keys and reads a body's and an emitter's `pair`",
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
    keys = {key for entry in universe["families"] + [SOURCED] for key in entry} - {"name"}
    assert keys <= words, f"keys of a family's entry no folder declares: {sorted(keys - words)}"
    offending = [
        f"{path.relative_to(ROOT)}:{line} {value!r}"
        for path in loader_modules()
        for line, value in string_constants(path)
        if value in words
    ]
    assert offending == [], offending
