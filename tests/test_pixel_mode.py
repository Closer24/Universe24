"""The mode file of a one-Node body (tools/pixel_mode.py; ALGEBRA.md #the-primitives, THE BOUND BODY IS ONE NODE): the amplitude at the pixel from the form at rest, b = isqrt(c T den div (2 den - a)) with the clock pair given per count, the tail round(b t^d) per Link with t given over 2^16 until it falls below 1, both levels the profile, the world loading lawful with it; a body of more than one Node, a count without its rows and a row given twice are refused by name."""

from __future__ import annotations

import json
from math import isqrt
from pathlib import Path

import pytest

from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import input_digest, load_world
from tests.worlds import load_file

ROOT = Path(__file__).resolve().parents[1]
WORLD = ROOT / "examples" / "events" / "experiments" / "rules_universe" / "fall_control.json"
UNIVERSE = (
    "examples/events/experiments/rules_universe/rules_universe.json"  # Gamma 12,000, the form of #1403
)
TOOL = load_file("pixel_mode", ROOT / "tools" / "pixel_mode.py")
COUNT, A, DEN, TAIL = 5000, 93270, 65536, 34734  # the pixel of 5,000, its pair and tail: Cheshbon's line


def test_the_pixels_record_is_the_forms_amplitude_at_its_node_with_the_tail_at_both_levels(tmp_path):
    document = json.loads(WORLD.read_text(encoding="utf-8"))
    document["universe"] = UNIVERSE  # the pixel of 5,000 and its pair are the 12,000 file's
    document["measured"][0]["nodes"][0]["count"] = COUNT
    world = tmp_path / "pixel.json"
    world.write_text(json.dumps(document), encoding="utf-8")
    TOOL.main(["--input", str(world), "--clock", "5000", str(A), str(DEN), "--tail", "5000", str(TAIL)])
    mode = json.loads((tmp_path / "pixel.mode.json").read_text(encoding="utf-8"))
    body, entry = document["measured"][0], mode["bodies"][0]
    node = tuple(body["nodes"][0]["node"])
    families = json.loads((ROOT / document["universe"]).read_text(encoding="utf-8"))["families"]
    pair = next(family["pair"] for family in families if family["name"] == "matter")
    amplitude = isqrt(COUNT * DEN // (2 * DEN - A))  # T = 1 in the rule's own universe file
    assert entry["family"] == "matter" and entry["pair"] == pair
    assert entry["clock"] == [A, DEN] and entry["count"] == COUNT
    assert (entry["amplitude"], entry["tail"]) == (amplitude, [TAIL, 1 << 16])
    simulation = DetectorLawSimulation(load_world(world))
    own = simulation.blocks[0].own
    assert own is not None and (own.now == own.before).all() and own.now[node] == amplitude
    beside = (node[0] + 1, node[1], node[2])
    one, two = (amplitude * TAIL + (1 << 15)) >> 16, (amplitude * TAIL**2 + (1 << 31)) >> 32
    assert own.now[beside] == one and own.now[node[0] + 2, node[1], node[2]] == two and one > two > 0
    assert own.now[0, node[1], node[2]] == (amplitude * TAIL**4 + (1 << 63)) >> 64
    assert own.now[node[0], (node[1] + 1) % 3, node[2]] == one  # the periodic axis, one Link
    assert mode["world_digest"] == input_digest(document)


def test_a_body_of_two_nodes_a_count_without_its_rows_and_a_row_given_twice_are_refused_by_name():
    document = json.loads(WORLD.read_text(encoding="utf-8"))
    document["universe"] = UNIVERSE  # the pixel of 5,000 and its pair are the 12,000 file's
    document["measured"][0]["nodes"][0]["count"] = 3000  # the world's count is the day's
    with pytest.raises(
        ValueError, match="measured\\[0\\] has the count 3000 and no --clock and --tail rows"
    ):
        TOOL.pixel_mode(document, TOOL.clock_table([[4000, A, DEN]], [[4000, TAIL]]))
    document["measured"][0]["nodes"].append({"node": [5, 1, 1], "count": 3000})
    with pytest.raises(ValueError, match="measured\\[0\\] is not a body of one declared Node"):
        TOOL.pixel_mode(document, TOOL.clock_table([[3000, A, DEN]], [[3000, TAIL]]))
    with pytest.raises(ValueError, match="given twice"):
        TOOL.clock_table([[3000, A, DEN], [3000, A, DEN]], [[3000, TAIL]])
    with pytest.raises(ValueError, match="a below 2 den"):
        TOOL.clock_table([[3000, 2 * DEN, DEN]], [[3000, TAIL]])
    with pytest.raises(ValueError, match="--clock 3000 has no --tail 3000"):
        TOOL.clock_table([[3000, A, DEN]], [])
    with pytest.raises(ValueError, match="--tail 4000 has no --clock 4000"):
        TOOL.clock_table([[3000, A, DEN]], [[3000, TAIL], [4000, TAIL]])
