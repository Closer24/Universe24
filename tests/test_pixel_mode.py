from __future__ import annotations

import json
from pathlib import Path

import pytest

import event_universe.world_files as world_files
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import input_digest, load_world
from tests.worlds import PIXEL_12000 as COUNT
from tests.worlds import ROWS_12000 as ROWS
from tests.worlds import load_file, pixel_at_12000

TOOL = load_file("pixel_mode", Path(__file__).resolve().parents[1] / "tools" / "pixel_mode.py")


def test_the_pixels_record_is_what_rule3_makes_of_its_count_and_loads_lawful(tmp_path, monkeypatch):
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    world = pixel_at_12000(tmp_path, TOOL)
    document = json.loads(world.read_text(encoding="utf-8"))
    mode = json.loads((tmp_path / "pixel.mode.json").read_text(encoding="utf-8"))
    entry, (a, den) = mode["bodies"][0], mode["bodies"][0]["clock"]
    off = abs(entry["carried"] - COUNT)  # the record carries the count within 2 isqrt(c) + 1
    assert (off - (off & 1)) ** 2 <= 4 * COUNT and entry["count"] == COUNT and entry["seed"] >= 1
    assert 2 * ROWS[2][0] * den < a * ROWS[2][1] and a < 2 * den  # a bound rotation of the matter kind
    profile, peak = entry["profile"], entry["amplitude"]
    assert max(map(abs, profile)) == abs(profile[20 * 41 + 20]) == peak > 0  # the peak at its Node
    assert entry["period"][1] == 2 and entry["period"][0] >= 4 and entry["twist"] == 0
    assert (
        entry["moving"]["now"] == profile and len(entry["moving"]["before"]) == len(profile) == 41 * 41
    )
    assert entry["wavelength"] >= 1 and entry["pair"] == ROWS[2][:2] and entry["family"] == "matter"
    assert mode["world_digest"] == input_digest(document)
    own = DetectorLawSimulation(load_world(world)).blocks[0].own  # LAWFUL, the record's two levels
    assert own is not None and own.now[20, 20, 0] == peak
    assert own.before.ravel().tolist() == entry["moving"]["before"]
    assert TOOL.wavelength((100, 100), 300) == 3 and TOOL.wavelength((200, 100), 300) == 300


def test_a_mode_of_the_walls_and_a_body_of_two_nodes_are_refused_by_name(tmp_path, monkeypatch):
    body = dict(family="matter", q=1, nodes=[dict(node=[12, 4, 4], count=8)], momentum=[0, 0, 0])
    body.update(momentum_before=[0, 0, 0], phase_denominator=1024)  # the pixel of 8 at Gamma 24
    world = dict(shape=[25, 9, 9], boundary=dict(x="open", y="open", z="open"), measured=[body], N=1024)
    world.update(universe="examples/events/planck.json", engine="examples/events/engine_start.json")
    with pytest.raises(ValueError, match="a mode of the board's walls, no bound pixel"):
        TOOL.pixel_mode(world)  # at 24 the integers hold no bound pixel of 8 on this board: the reading
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    document = json.loads(pixel_at_12000(tmp_path, TOOL, mode=False).read_text(encoding="utf-8"))
    document["measured"][0]["nodes"].append({"node": [8, 4, 0], "count": COUNT})
    with pytest.raises(ValueError, match="measured\\[0\\] is not a body of one declared Node"):
        TOOL.pixel_mode(document)
