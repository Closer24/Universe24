"""A BOUND BODY (ALGEBRA.md #the-generator, #what-a-body-is, #the-counts-line): the pixel tool lays a body on the rule's own universe, the loop admits its declared count within 2 isqrt(c) + 1 of the record's form and refuses one beyond it by name, and the body stands in the engine with its quanta in its set."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

import event_universe.world_files as world_files
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import input_stamp, load_world
from tests.laws import BODY_24 as QUANTA
from tests.laws import body_at_24, load_file

TOOL = load_file("pixel_mode", Path(__file__).resolve().parents[1] / "tools" / "pixel_mode.py")


def test_the_laid_body_stands_in_the_engine_with_its_quanta_in_its_set(tmp_path, monkeypatch):
    """The count is laid from the record's form at the wall 3 den T within the law's tolerance of the declared count; over forty intervals no quantum leaves the body's Nodes and their Links, no count goes below zero and the total is conserved."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    world = body_at_24(tmp_path, TOOL)
    document = json.loads(world.read_text(encoding="utf-8"))
    simulation = DetectorLawSimulation(load_world(world))
    block = simulation.blocks[0]
    inset = np.zeros(simulation.shape, dtype=bool)
    for node in document["measured"][0]["nodes"]:
        inset[tuple(node["node"])] = True
    near = inset.copy()
    for axis in range(3):
        near |= np.roll(inset, 1, axis=axis) | np.roll(inset, -1, axis=axis)
    simulation.step()
    assert block.counts is not None and block.count_remainder is not None
    wall = simulation.count_wall(block)
    total = int((wall * block.counts + block.count_remainder).sum())
    laid = int(block.counts.sum())
    assert abs(laid - QUANTA) <= 2 * int(QUANTA**0.5) + 1
    for _ in range(40):
        simulation.step()
        assert int(block.counts.min()) >= 0 and int(block.counts[~near].sum()) == 0
        assert int((wall * block.counts + block.count_remainder).sum()) == total


def test_a_declared_count_far_from_the_records_form_is_refused_by_name(tmp_path, monkeypatch):
    """The gate at the lay: the declared count off the record's form by more than 2 isqrt(c) + 1 ends the run by name."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    world = body_at_24(tmp_path, TOOL)
    document = json.loads(world.read_text(encoding="utf-8"))
    for node in document["measured"][0]["nodes"]:
        node["count"] *= 3
    document["stamp"] = input_stamp(document)
    world.write_text(json.dumps(document), encoding="utf-8")
    mode_path = world.with_suffix(".mode.json")
    mode = json.loads(mode_path.read_text(encoding="utf-8"))
    mode["world_digest"] = document["stamp"]["hash"]
    mode_path.write_text(json.dumps(mode), encoding="utf-8")
    simulation = DetectorLawSimulation(load_world(world))
    with pytest.raises(ValueError, match="a declared count is within 2 isqrt"):
        simulation.step()
