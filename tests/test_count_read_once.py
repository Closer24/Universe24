"""THE COUNT IS READ ONCE and THE COUNT IS THE RECORD'S FORM OVER ITS PERIOD (ALGEBRA.md THE ALGEBRA OF CLUSTERS (1) and (2)): on the rule's universe a pixel's count enters every family's pace once, the held level at its Node the well D div T written once and never added, so the charge's and the matter's content there equal gravity's level and the pace is Gamma - c, not 2c; the count's line lays its counts from the loaded record's well and then once per period of the record, every count at or above 0, twenty intervals without a refusal."""

from __future__ import annotations

import json
from math import isqrt
from pathlib import Path
from types import SimpleNamespace

import pytest

import event_universe.world_files as world_files
from event_universe.events import count_once
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import load_world
from tests.worlds import load_file

EVENTS = Path(__file__).resolve().parents[1] / "examples" / "events"
TOOL = load_file("pixel_mode", EVENTS.parents[1] / "tools" / "pixel_mode.py")
COUNT, CLOCK, TAIL = "4400", ["88553", "65536"], "49395"  # a pixel at 12,000 today, Cheshbon's line
GAMMA, ROWS = 12000, ([12000, 12000, 1], [12000, 12000, 400000], [8000, 12000, None])  # #1419's rows


def pixel_world(tmp_path: Path) -> Path:
    """The tree's planck.json in its form at Gamma 12,000 (#1419; the tree's file is at 24): the three rows over Gamma, the identity twist table (a pixel's twist is 0), the spin's row the loop still asks; the fall world's pixel at COUNT with q = 1, its mode by the tool."""
    universe = json.loads((EVENTS / "planck.json").read_text(encoding="utf-8"))
    identity = dict(unit=4 * GAMMA << 16, fine=[[1, 0, 1]], coarse=[[1, 0, 1]])
    universe["integers"].update(node_clock=GAMMA, twist_table=identity)
    for family, (num, den, divisor) in zip(universe["families"], ROWS, strict=True):
        family["pair"] = [num, den]
        if divisor:
            family["held"]["divisor"] = divisor
    universe["families"][0]["spins_step"] = {"curl": [1, 4], "tidal": [3, 4]}
    (tmp_path / "u.json").write_text(json.dumps(universe), encoding="utf-8")
    (tmp_path / "e.json").write_bytes((EVENTS / "engine_start.json").read_bytes())
    body = dict(family="matter", q=1, nodes=[dict(node=[4, 1, 1], count=int(COUNT))], momentum=[0, 0, 0])
    body.update(momentum_before=[0, 0, 0], phase_denominator=1024)  # the fall world's pixel (#1403)
    document = dict(shape=[9, 3, 3], boundary=dict(x="open", y="periodic", z="periodic"), detectors=[])
    document.update(ticks=64, N=1024, face_depth=1, universe="u.json", engine="e.json", measured=[body])
    (world := tmp_path / "pixel.json").write_text(json.dumps(document), encoding="utf-8")
    TOOL.main(["--input", str(world), "--clock", COUNT, *CLOCK, "--tail", COUNT, TAIL])
    return world


def test_the_pixels_count_enters_every_pace_once_and_every_node_holds_its_count(tmp_path, monkeypatch):
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    simulation = DetectorLawSimulation(load_world(pixel_world(tmp_path)))
    node = tuple(simulation.world.measured[0].block.nodes[0])
    by = {family.name: number for number, family in enumerate(simulation.families)}
    block, lays = simulation.blocks[0], []
    for _ in range(20):
        carried = None if block.count_remainder is None else int(block.count_remainder.sum())
        simulation.step()  # no refusal: the pace stays above 0 and no count falls below 0
        well, level = block.well, simulation.held_records[by["gravity"]].now
        assert well is not None and block.counts is not None and level[node] == well[node] > 0
        contents = [simulation._effective_content(by[name])[node] for name in ("charge", "matter")]
        assert contents[0] == contents[1] == level[node]  # the count read once, down the ranks at 1
        assert simulation.node_clock_pair(node, by["charge"]) == (GAMMA - level[node], GAMMA)
        assert block.counts.min() >= 0 and block.counts[node] > 0 and block.period_counts is not None
        moved = int((block.count_norm * block.counts + block.count_remainder).sum())  # T c + r after
        assert carried is None or moved == block.count_norm * block.period_counts.sum() + carried
        lays.append(int(block.period_counts[node]))
    assert 1 < len(set(lays)) < 6 and min(lays) > isqrt(int(COUNT))  # read once per period
    half = SimpleNamespace(**{**vars(block.definition), "counts": (int(COUNT) // 2,)})  # off its mode
    off = SimpleNamespace(number=0, own=block.own, definition=half)
    with pytest.raises(ValueError, match="a declared count is D div T of its mode within 2 isqrt"):
        count_once.declared_within_gate(off)


def test_the_first_lay_is_the_declared_count_and_the_average_after_a_whole_period(tmp_path, monkeypatch):
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    simulation = DetectorLawSimulation(load_world(pixel_world(tmp_path)))
    node, block = tuple(simulation.world.measured[0].block.nodes[0]), simulation.blocks[0]
    signs, lays = [], []  # the sign of the level at the Node and the sum of the lay, per interval
    for _ in range(20):
        simulation.step()
        signs.append(int(block.own.now[node]) > 0)
        lays.append(int(block.period_counts.sum()))
    changes = [index for index in range(1, 20) if signs[index] != signs[index - 1]]  # the sign changes
    assert lays[0] == int(COUNT) and len(changes) >= 3  # the declared count at its Node alone
    assert all(lay == int(COUNT) for lay in lays[: changes[2]]) and lays[changes[2]] != int(COUNT)
