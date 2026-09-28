"""THE COUNT IS READ ONCE and THE COUNT IS THE RECORD'S FORM OVER ITS PERIOD (ALGEBRA.md THE ALGEBRA OF CLUSTERS (1) and (2)): on the rule's universe file a pixel's count enters every family's pace once, the held level at its Node the well D div T written once and never added interval after interval, so the charge's and the matter's content there equal gravity's level and the pace is Gamma - c, not 2c; the count's line lays its counts from the well of the loaded record and then once per period of the record, every Node holding its count and giving at most that, and twenty intervals run without a refusal."""

from __future__ import annotations

import json
from math import isqrt
from pathlib import Path

import event_universe.world_files as world_files
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import load_world
from tests.worlds import load_file

ROOT = Path(__file__).resolve().parents[1]
WORLD = ROOT / "examples" / "events" / "experiments" / "rules_universe" / "fall_tent_0.json"
TOOL = load_file("pixel_mode", ROOT / "tools" / "pixel_mode.py")
COUNT, CLOCK, TAIL = 4400, (88553, 65536), 49395  # the pixel of 4,400 on today's engine, Cheshbon's line
GAMMA, CHARGE_DIVISOR = (
    12000,
    400000,
)  # the rule's universe at 12,000 (#1419); the tree's file is at 24 now
ROWS = ([GAMMA, GAMMA], [GAMMA, GAMMA], [8000, GAMMA])  # gravity, the charge, matter over Gamma
SPINS_STEP = {"curl": [1, 4], "tidal": [3, 4]}  # the row the loop's spin read still asks (main 64f3493d)


def universe_at_12000(tmp_path: Path) -> None:
    """The tree's planck.json in its form at Gamma 12,000: the three rows over Gamma, the identity twist table (a pixel's twist is 0), the spin's row the loop asks."""
    universe = json.loads((ROOT / "examples" / "events" / "planck.json").read_text(encoding="utf-8"))
    table = dict(unit=4 * GAMMA << 16, fine=[[1, 0, 1]], coarse=[[1, 0, 1]])
    universe["integers"].update(node_clock=GAMMA, twist_table=table)
    for family, pair, divisor in zip(universe["families"], ROWS, (1, CHARGE_DIVISOR, None), strict=True):
        family["pair"] = pair
        if divisor is not None:
            family["held"]["divisor"] = divisor
    universe["families"][0]["spins_step"] = SPINS_STEP
    (tmp_path / "planck.json").write_text(json.dumps(universe), encoding="utf-8")
    start = (ROOT / "examples" / "events" / "engine_start.json").read_text(encoding="utf-8")
    (tmp_path / "start.json").write_text(start, encoding="utf-8")


def test_the_pixels_count_enters_every_pace_once_and_every_node_holds_its_count(tmp_path, monkeypatch):
    document = json.loads(WORLD.read_text(encoding="utf-8"))
    universe_at_12000(tmp_path)
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    document.update(universe="planck.json", engine="start.json", readings=[])
    node = tuple(document["measured"][0]["nodes"][0]["node"])
    document["measured"][0].update(q=1, nodes=[{"node": list(node), "count": COUNT}])
    world = tmp_path / "pixel.json"
    world.write_text(json.dumps(document), encoding="utf-8")
    TOOL.main(
        ["--input", str(world), "--clock", str(COUNT), *map(str, CLOCK), "--tail", str(COUNT), str(TAIL)]
    )
    mode = json.loads((tmp_path / "pixel.mode.json").read_text(encoding="utf-8"))
    mode["bodies"][0]["twist"] = 0  # a pixel's twist is 0 (Cheshbon 15:27): the identity table, no acos
    (tmp_path / "pixel.mode.json").write_text(json.dumps(mode), encoding="utf-8")
    simulation = DetectorLawSimulation(load_world(world))
    names = [family.name for family in simulation.families]
    gravity, charge, matter = (names.index(name) for name in ("gravity", "charge", "matter"))
    block, lays = simulation.blocks[0], []
    for _ in range(20):
        simulation.step()  # no refusal: the pace stays above 0 and no count falls below 0
        well, level = block.well, simulation.held_records[gravity].now
        assert well is not None and block.counts is not None and level[node] == well[node] > 0
        assert (
            simulation._effective_content(charge)[node]
            == simulation._effective_content(matter)[node]
            == level[node]
        )
        assert simulation.node_clock_pair(node, charge) == (
            simulation.node_clock - level[node],
            simulation.node_clock,
        )
        assert block.counts.min() >= 0 and block.counts[node] > 0 and block.period_counts is not None
        lays.append(int(block.period_counts[node]))
    assert 1 < len(set(lays)) < 6 and all(
        lay > isqrt(COUNT) for lay in lays
    )  # read once per period, not per interval
