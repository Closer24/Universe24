"""The worlds of the entity catalog (docs/ENTITY_CATALOG.md; the model
owner's decision of 2026-09-20, Highlights 5.4: every entity physics knows
as one row of the law's keys, and the external things placed on the
GameBoard "so that they can be placed and things tested"). The catalog's
worlds under `examples/events/catalog/` are placements, not experiments,
so this module pins no number of any world (the model owner's rule of
2026-09-17); it checks that each world is what the catalog says it is
(docs/TEST_EXPECTATIONS.md, "The entity catalog"):

(a) every catalog world is the one its generator writes (the shipped file
    equals `make_worlds.worlds()` document for document), parses through
    the canonical loader as a world of the law (its `law` the value
    `world.py` names, its `model_id` naming the catalog), declares
    `quantum` on every family and `reading` on every declared detector,
    and runs 20 to 50 intervals;
(b) each runs its declared intervals headless with the books balanced at
    every interval;
(c) the readings the catalog names exist: every declared detector appears
    in the run's detector report with an integer `record` per family, at
    least one declared detector of a world that declares detectors wrote a
    `record` line, and every probe (a measured event whose table passes a
    family, the clock the catalog reads) ends with its clock's identity,
    age + waited = the intervals run, its owed count an integer.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

from event_universe.events import NatureBeamSimulation
from event_universe.events.world import LAW_VALUE
from event_universe.world_loading import load_world

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "examples" / "events" / "catalog"
WORLDS = ("sun_planet", "neutron_star", "lamp_mirror_screen", "clock_near_mass")


def load_generator():
    path = CATALOG / "make_worlds.py"
    spec = importlib.util.spec_from_file_location("catalog_make_worlds", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["catalog_make_worlds"] = module
    spec.loader.exec_module(module)
    return module


def shipped(name: str) -> dict[str, object]:
    return json.loads((CATALOG / f"{name}.json").read_text(encoding="utf-8"))


def test_the_shipped_worlds_are_the_generators():
    """(a): the files and the generator agree, world by world."""
    generated = load_generator().worlds()
    assert set(generated) == set(WORLDS)
    for name in WORLDS:
        assert shipped(name) == generated[name], name


@pytest.mark.parametrize("name", WORLDS)
def test_every_catalog_world_declares_its_keys_and_parses(name):
    """(a)."""
    document = shipped(name)
    # The law's value as `world.py` names it (`beam` since the Beam Law
    # rename of 2026-09-20), never a literal.
    assert document["law"] == LAW_VALUE and "catalog" in document["model_id"]
    assert 20 <= document["ticks"] <= 50
    assert all("quantum" in family for family in document["families"])
    assert all("reading" in detector for detector in document.get("detectors", []))
    loaded = load_world((CATALOG / f"{name}.json").read_bytes(), base_dir=CATALOG)
    assert loaded.world.model_id == document["model_id"]
    assert len(loaded.world.measured) == len(document["measured"])


@pytest.mark.parametrize("name", WORLDS)
def test_every_catalog_world_runs_with_the_books_balanced_and_its_readings_exist(name):
    """(b) and (c)."""
    document = shipped(name)
    world = load_world(json.dumps(document).encode("utf-8")).world
    lines: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(world, lines.append)
    ticks = int(document["ticks"])
    for tick in range(1, ticks + 1):
        simulation.step()
        assert simulation.books()["balanced"], (name, tick)
    assert simulation.tick == ticks
    # The declared detectors: one record per family each, exact integers.
    reports = {str(entry["name"]): entry for entry in simulation.detectors()}
    declared = [str(detector["name"]) for detector in document.get("detectors", [])]
    for detector_name in declared:
        report = reports[detector_name]
        assert report["reading"] == "wave"
        for family in world.families:
            assert isinstance(report["families"][family.name]["record"], int)
    recorded = {str(line.get("detector")) for line in lines if line["event"] == "record"}
    if declared:
        assert recorded & set(declared), (name, recorded)
    # The probes: a measured event whose table passes a family reads its
    # clock; every interval is a self-creation or a wait.
    probes = [
        entry
        for entry in simulation.measured.values()
        if "pass" in world.measured[entry.number - 1].table
    ]
    if name in ("neutron_star", "clock_near_mass"):
        assert probes, name
    for probe in probes:
        state = probe.state()
        assert state["age"] + state["waited"] == ticks, (name, probe.number)
        assert isinstance(state["owed"], int) and state["owed"] >= 0
