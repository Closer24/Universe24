"""The mode file of a one-Node body (tools/pixel_mode.py; ALGEBRA.md #the-primitives, THE BOUND BODY IS ONE NODE): the record at the pixel's Node is isqrt(c) at both levels, its clock the pair given per count, the world loads lawful with it; a body of more than one Node and a count without a pair are refused by name."""

from __future__ import annotations

import json
import shutil
from math import isqrt
from pathlib import Path

import pytest

from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import input_digest, load_world
from tests.worlds import load_file

ROOT = Path(__file__).resolve().parents[1]
WORLD = ROOT / "examples" / "events" / "experiments" / "rules_universe" / "fall_tent_0.json"
TOOL = load_file("pixel_mode", ROOT / "tools" / "pixel_mode.py")


def test_the_pixels_record_is_the_counts_root_at_its_node_at_both_levels_with_the_given_clock(tmp_path):
    world = shutil.copy(WORLD, tmp_path / "pixel.json")
    TOOL.main(["--input", str(world), "--clock", "3000", "700", "400"])
    mode = json.loads((tmp_path / "pixel.mode.json").read_text(encoding="utf-8"))
    body = json.loads(WORLD.read_text(encoding="utf-8"))["measured"][0]
    node, count = tuple(body["nodes"][0]["node"]), body["nodes"][0]["count"]
    entry = mode["bodies"][0]
    assert (entry["family"], entry["pair"], entry["clock"], entry["count"]) == (
        "matter",
        [2, 3],
        [700, 400],
        count,
    )
    assert entry["amplitude"] == isqrt(count) and sum(entry["profile"]) == isqrt(count)
    simulation = DetectorLawSimulation(load_world(Path(world)))
    own = simulation.blocks[0].own
    assert own is not None and (own.now[node], own.before[node], own.now.sum()) == (isqrt(count),) * 3
    assert mode["world_digest"] == input_digest(json.loads(WORLD.read_text(encoding="utf-8")))


def test_a_body_of_two_nodes_and_a_count_without_a_pair_are_refused_by_name():
    document = json.loads(WORLD.read_text(encoding="utf-8"))
    with pytest.raises(ValueError, match="measured\\[0\\] has the count 3000 and no --clock pair"):
        TOOL.pixel_mode(document, TOOL.clock_table([[4000, 7, 4]]))
    document["measured"][0]["nodes"].append({"node": [5, 1, 1], "count": 3000})
    with pytest.raises(ValueError, match="measured\\[0\\] is not a body of one declared Node"):
        TOOL.pixel_mode(document, TOOL.clock_table([[3000, 7, 4]]))
    with pytest.raises(ValueError, match="given twice"):
        TOOL.clock_table([[3000, 7, 4], [3000, 7, 4]])
