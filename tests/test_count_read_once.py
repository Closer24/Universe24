"""THE COUNT IS READ ONCE and THE COUNT IS THE RECORD'S FORM OVER ITS PERIOD (ALGEBRA.md THE ALGEBRA OF CLUSTERS (1) and (2)): on the rule's universe a pixel's count enters every family's pace once, the held level at its Node the well D div T written once and never added, so the charge's and the matter's content there equal gravity's level and the pace is Gamma - c, not 2c; the count's line lays its counts from the loaded record's well and then once per period of the record, every count at or above 0, twenty intervals without a refusal."""

from __future__ import annotations

from math import isqrt
from pathlib import Path
from types import SimpleNamespace

import pytest

import event_universe.world_files as world_files
from event_universe.events import count_once
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import load_world
from tests.worlds import GAMMA_12000, PIXEL_12000, load_file, pixel_at_12000

ROOT = Path(__file__).resolve().parents[1]
TOOL = load_file("pixel_mode", ROOT / "tools" / "pixel_mode.py")
COUNT, GAMMA = PIXEL_12000, GAMMA_12000


def pixel_world(tmp_path: Path, shape=(41, 41, 1), node=(20, 20, 0), mode: bool = True) -> Path:
    """The pixel of 12,000 on its board with its mode by the tool (tests/worlds.py)."""
    return pixel_at_12000(tmp_path, TOOL, shape, node, mode)


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
    assert 1 < len(set(lays)) < 6 and min(lays) > isqrt(COUNT)  # read once per period
    half = SimpleNamespace(**{**vars(block.definition), "counts": (COUNT // 2,)})  # off its mode
    off = SimpleNamespace(number=0, own=block.own, definition=half)
    with pytest.raises(ValueError, match="a declared count is D div T of its record within 2 isqrt"):
        count_once.declared_within_gate(off, block.period_counts)
