"""The mode file of a one-Node body (tools/pixel_mode.py; ALGEBRA.md #the-primitives, THE BOUND BODY IS ONE NODE): the amplitude at the pixel from the form at rest, b = isqrt(c T den div (2 den - a)) with the clock pair given per count, the tail round(b t^d) per Link with t given over 2^16 until it falls below 1, both levels the profile, the world loading lawful with it; a body of more than one Node, a count without a row and a row given twice are refused by name."""

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
A, DEN, TAIL = (
    90000,
    65536,
    41943,
)  # a clock pair in the matter band and a tail factor, the test's own


def test_the_pixels_record_is_the_forms_amplitude_at_its_node_with_the_tail_at_both_levels(tmp_path):
    world = shutil.copy(WORLD, tmp_path / "pixel.json")
    TOOL.main(["--input", str(world), "--clock", "3000", str(A), str(DEN), str(TAIL)])
    mode = json.loads((tmp_path / "pixel.mode.json").read_text(encoding="utf-8"))
    document = json.loads(WORLD.read_text(encoding="utf-8"))
    body, entry = document["measured"][0], mode["bodies"][0]
    node, count = tuple(body["nodes"][0]["node"]), body["nodes"][0]["count"]
    families = json.loads((ROOT / document["universe"]).read_text(encoding="utf-8"))["families"]
    pair = next(family["pair"] for family in families if family["name"] == "matter")
    amplitude = isqrt(count * DEN // (2 * DEN - A))  # T = 1 in the rule's own universe file
    assert (entry["family"], entry["pair"], entry["clock"], entry["count"]) == (
        "matter",
        pair,
        [A, DEN],
        count,
    )
    assert (entry["amplitude"], entry["tail"]) == (amplitude, [TAIL, 1 << 16])
    simulation = DetectorLawSimulation(load_world(Path(world)))
    own = simulation.blocks[0].own
    assert own is not None and (own.now == own.before).all() and own.now[node] == amplitude
    beside = (node[0] + 1, node[1], node[2])
    assert (
        own.now[beside] == (amplitude * TAIL + (1 << 15)) // (1 << 16)
        and own.now[beside] < own.now[node]
    )
    assert own.now[0, node[1], node[2]] == (amplitude * TAIL**4 + (1 << 63)) // (1 << 64)
    assert own.now[node[0], (node[1] + 1) % 3, node[2]] == own.now[beside]  # the periodic axis, one Link
    assert mode["world_digest"] == input_digest(document)


def test_a_body_of_two_nodes_a_count_without_a_row_and_a_row_given_twice_are_refused_by_name():
    document = json.loads(WORLD.read_text(encoding="utf-8"))
    with pytest.raises(ValueError, match="measured\\[0\\] has the count 3000 and no --clock row"):
        TOOL.pixel_mode(document, TOOL.clock_table([[4000, A, DEN, TAIL]]))
    document["measured"][0]["nodes"].append({"node": [5, 1, 1], "count": 3000})
    with pytest.raises(ValueError, match="measured\\[0\\] is not a body of one declared Node"):
        TOOL.pixel_mode(document, TOOL.clock_table([[3000, A, DEN, TAIL]]))
    with pytest.raises(ValueError, match="given twice"):
        TOOL.clock_table([[3000, A, DEN, TAIL], [3000, A, DEN, TAIL]])
    with pytest.raises(ValueError, match="a below 2 den"):
        TOOL.clock_table([[3000, 2 * DEN, DEN, TAIL]])
