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
from tests.laws import body_at_24, chain_body_world, load_file

TOOL = load_file("pixel_mode", Path(__file__).resolve().parents[1] / "tools" / "pixel_mode.py")


def test_the_laid_body_is_admitted_with_its_count_at_its_nodes(tmp_path, monkeypatch):
    """The count is laid from the record's form at the wall 3 den T within the law's tolerance of the declared count, every Node of the body carrying a quantum (the rule's own universe at Gamma = 24 is coarse: its body of sixteen quanta loses a third of them to its surround within forty intervals; the standing is read on the chain at Gamma = 6000 below)."""
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
    laid = int(block.counts[inset].sum())
    assert abs(laid - QUANTA) <= 2 * int(QUANTA**0.5) + 1 and int(block.counts[inset].min()) >= 1


def test_a_declared_count_far_from_the_records_form_is_refused_by_name(tmp_path, monkeypatch):
    """The gate at the lay: the declared count off the record's form by more than 2 isqrt(c) + 1 ends the run by name."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    world = body_at_24(tmp_path, TOOL)
    document = json.loads(world.read_text(encoding="utf-8"))
    for node in document["measured"][0]["nodes"]:
        node["count"] = (
            1  # far below the record's form (a larger count would first trip the pace guard at Gamma = 24)
        )
    document["stamp"] = input_stamp(document)
    world.write_text(json.dumps(document), encoding="utf-8")
    mode_path = world.with_suffix(".mode.json")
    mode = json.loads(mode_path.read_text(encoding="utf-8"))
    mode["world_digest"] = document["stamp"]["hash"]
    mode_path.write_text(json.dumps(mode), encoding="utf-8")
    simulation = DetectorLawSimulation(load_world(world))
    with pytest.raises(ValueError, match="a declared count is within 2 isqrt"):
        simulation.step()


def test_a_chain_body_at_gamma_6000_keeps_its_quanta_over_a_hundred_intervals(tmp_path, monkeypatch):
    """A BOUND BODY STANDS: on the universe of Gamma 6000 a body of six hundred quanta laid by the pixel tool keeps at least nineteen of every twenty laid quanta on its Nodes and their Links over a hundred intervals, its total conserved to the bit, no hole in its set (the Paper Writer's reading of 2026-09-29: 97 percent over 400 intervals)."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    world = chain_body_world(tmp_path, TOOL)
    document = json.loads(world.read_text(encoding="utf-8"))
    simulation = DetectorLawSimulation(load_world(world))
    block = simulation.blocks[0]
    inset = np.zeros(simulation.shape, dtype=bool)
    for node in document["measured"][0]["nodes"]:
        inset[tuple(node["node"])] = True
    near = inset | np.roll(inset, 1, axis=0) | np.roll(inset, -1, axis=0)
    simulation.step()
    assert block.counts is not None and block.count_remainder is not None
    wall, laid = simulation.count_wall(block), int(block.counts.sum())
    total = int((wall * block.counts + block.count_remainder).sum())
    assert abs(laid - 600) <= 2 * 24 + 1
    momentum_wall = simulation.wall_of(block)  # W = 3 Q M
    for _ in range(99):
        simulation.step()
        assert int(block.counts[inset].min()) >= 0 and 20 * int(block.counts[near].sum()) >= 19 * laid
        assert int((wall * block.counts + block.count_remainder).sum()) == total
        # THE MOMENTUM AS A READING (the recoil's row): n = W x the current over the form c W_c, the current
        # num x SUM (now_j before_i - before_j now_i) through the +x Ports, so n = W v within W; at rest within 3 Q
        live = block.own
        assert live is not None
        wrap = simulation.kind_wrap[block.family]
        now_in, before_in = (
            simulation.ports.arrivals(live.now, wrap)[0],
            simulation.ports.arrivals(live.before, wrap)[0],
        )
        current = 4000 * int((now_in * live.before - before_in * live.now).sum(dtype=object))
        form = wall * int(simulation._body_count(block))
        assert abs(block.momentum[0] * form - momentum_wall * current) <= form
        assert abs(block.momentum[0]) <= 3 * simulation.momentum_unit and block.momentum[1:] == [0, 0]
