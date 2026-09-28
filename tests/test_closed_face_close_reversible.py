"""The reversible row through a window's close at a closed face (ALGEBRA.md #the-direction): a giving body of two Nodes one Node off the closed -x face on the universe of record, stepped to its window's close and back through it by the host's tool, returns every row bit for bit (de Broglie's fixture of #1392, the finding of 2026-09-28 11:50 Israel: MISS since #1375 at the polarisation's held record on the face Node)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import event_universe.world_files as world_files
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import input_stamp, load_world

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from reversible import reversible_row  # noqa: E402

UNIVERSE = ROOT / "examples" / "events" / "experiments" / "universe.json"
START = ROOT / "examples" / "events" / "engine_start.json"
GIVER = {"family": "charge", "weight": 1, "norm": 100, "norm_denominator": 1, "receiver": ["strip"]}
NODES = [{"node": [1, 0, 0], "count": 1}, {"node": [2, 0, 0], "count": 1}]
FACES = {"x": "closed", "y": "periodic", "z": "periodic"}
STRIP = {"name": "strip", "positions": [[2, 0, 0]]}
MODE = {"family": "matter", "pair": [800, 1200], "profile": [0, 1000, 1000] + [0] * 13}


def giver_world(tmp_path: Path, monkeypatch) -> Path:
    """The giver of two Nodes at x = 1, 2 by the closed -x face, its mode file beside it (the record's profile, its clock at a fine unit, its twist and wavelength), the strip on its own Node."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    (tmp_path / "universe.json").write_text(UNIVERSE.read_text(encoding="utf-8"), encoding="utf-8")
    (tmp_path / "start.json").write_text(START.read_text(encoding="utf-8"), encoding="utf-8")
    body = {"family": "matter", "moment": [0, 0, 1], "stocks": {"charge": 4}, "emitter": GIVER, "q": 1}
    body.update(nodes=NODES, momentum=[0, 0, 0], momentum_before=[0, 0, 0])
    world = {"shape": [16, 1, 1], "boundary": FACES, "ticks": 400, "N": 1024, "measured": [body]}
    world.update(universe="universe.json", engine="start.json", detectors=[STRIP])
    world["stamp"] = input_stamp(world)
    (tmp_path / "giver.json").write_text(json.dumps(world), encoding="utf-8")
    entry = {**MODE, "clock": [153 * 10**6, 10**8], "twist": 45875, "wavelength": 7}
    mode = {"world_digest": world["stamp"]["hash"], "bodies": [entry]}
    (tmp_path / "giver.mode.json").write_text(json.dumps(mode), encoding="utf-8")
    return tmp_path / "giver.json"


def test_the_close_at_a_closed_face_steps_back_bit_for_bit(tmp_path, monkeypatch):
    """The window opens and closes within the first intervals; the reversible row from the close's interval reads MATCH over every interval back but the last, where the known defect of the hold's rewrite across the click is named (a MISS by name, not a MATCH)."""
    path = giver_world(tmp_path, monkeypatch)

    def build() -> tuple[DetectorLawSimulation, list[dict]]:
        found: list[dict] = []
        return DetectorLawSimulation(load_world(path), observer=found.append), found

    simulation, lines = build()
    while not [line for line in lines if line["event"] == "giving"] and simulation.tick < 400:
        simulation.step()
    (giving,) = [line for line in lines if line["event"] == "giving"]
    row = reversible_row(build, giving["tick"])
    # THE KNOWN MISS, BY NAME (the Closer's rule of 14:49 Israel, 2026-09-28): the hold's rewrite across the click
    # returns the polarisation's `before` at the giver's Node off by the count M (the second inverse layer, #1325
    # 13:44 and 14:04); the row reads MISS there and nowhere earlier; MATCH is the line once the loop's inverse holds
    assert row["verdict"] == "MISS" and row["read"]["intervals_back"] >= 1, row["read"]
    miss = row["read"]["first_miss"]
    assert miss["row"] == "record held:3 before" and miss["node"] == [1, 0, 0], miss
