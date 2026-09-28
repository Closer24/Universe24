"""THE BOUND BODY IS ONE NODE (ALGEBRA.md #the-primitives, THE RULE'S OWN UNIVERSE) as a GameBoard reading: in a universe whose every held divisor is 1 a body of one declared Node on a massive pair reads as bound per the files, beside its lattice record and not instead of it; the reading gives the record's levels at its Node and the one-Node line's rotation there, the pixel keeps its lattice record and Rule3 steps at every Node, the hold sources its count, and no count falls below 0."""

from __future__ import annotations

import json
from pathlib import Path

import event_universe.world_files as world_files
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.events.one_node import one_node_body
from event_universe.world_files import input_stamp, load_world

ROOT = Path(__file__).resolve().parents[1]
UNIVERSE = ROOT / "examples" / "events" / "experiments" / "universe.json"
START = ROOT / "examples" / "events" / "engine_start.json"
NODE, COUNT, SIDE, CLOCK, AMPLITUDE = (4, 4, 4), 300, 9, 12000, 17  # the pixel, c, side, Gamma, isqrt(c)


def pixel_world(tmp_path: Path, monkeypatch, divisor: int) -> Path:
    """A closed cube of SIDE Nodes a side (the well the six Ports' Green's function, three-dimensional) with one body of matter of one Node at NODE with COUNT quanta at rest, its mode file the record at its Node (the profile AMPLITUDE there, a clock above the band) and nothing elsewhere; the families are the universe of record's with every held divisor set to `divisor` and Gamma the rule's (the rule's own universe file is the loader's), the count keeping the pace above 0 under their reads."""
    tmp_path.mkdir(exist_ok=True)
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    universe = json.loads(UNIVERSE.read_text(encoding="utf-8"))
    universe["integers"]["node_clock"] = CLOCK
    for family in universe["families"]:
        family.get("held", {}).update(divisor=divisor) if "held" in family else None
    (tmp_path / "universe.json").write_text(json.dumps(universe), encoding="utf-8")
    (tmp_path / "start.json").write_text(START.read_text(encoding="utf-8"), encoding="utf-8")
    body = dict(family="matter", nodes=[{"node": list(NODE), "count": COUNT}], phase_denominator=1024)
    body.update(momentum=[0, 0, 0], momentum_before=[0, 0, 0])
    world = {"shape": [SIDE, SIDE, SIDE], "boundary": {"x": "closed", "y": "closed", "z": "closed"}}
    world.update(ticks=64, N=1024, measured=[body], universe="universe.json", engine="start.json")
    world["detectors"] = [{"name": "own", "positions": [list(NODE)]}]
    world["stamp"] = input_stamp(world)
    (tmp_path / "pixel.json").write_text(json.dumps(world), encoding="utf-8")
    profile = [0] * SIDE**3
    profile[(NODE[0] * SIDE + NODE[1]) * SIDE + NODE[2]] = AMPLITUDE
    entry = dict(family="matter", pair=[800, 1200], profile=profile, twist=0, clock=[432, 300])
    mode = {"world_digest": world["stamp"]["hash"], "bodies": [entry]}
    (tmp_path / "pixel.mode.json").write_text(json.dumps(mode), encoding="utf-8")
    return tmp_path / "pixel.json"


def test_under_the_divisor_1_the_one_node_body_reads_as_bound_beside_its_lattice_record(
    tmp_path, monkeypatch
):
    """Under the divisors 1 the body reads as bound, keeps its lattice record and has no Node record; under the universe of record's divisors it reads as not bound with no rotation reading. The rotation reading gives the record's levels at the Node, (17, 17, 0) at the load, and the one-Node line's (coefficient, wall) there as the loop reads them; the hold sources the declared count at the Node; the record rotates at its Node over twelve intervals and no count falls below 0 (the clamp; the step back of a cloud is not bit for bit and is not claimed)."""
    lattice = DetectorLawSimulation(load_world(pixel_world(tmp_path / "record", monkeypatch, 40000)))
    block = lattice.blocks[0]
    assert not one_node_body(lattice.world, block.definition) and block.own is not None
    reading = dict(lattice.snapshot_stream())["blocks"][0]
    assert (reading["bound"], reading["rotation"]) == (False, None)
    simulation = DetectorLawSimulation(load_world(pixel_world(tmp_path / "rule", monkeypatch, 1)))
    block = simulation.blocks[0]
    own = block.own
    assert own is not None and block.node_record is None
    reading = dict(simulation.snapshot_stream())["blocks"][0]
    assert reading["bound"] and reading["rotation"]["node"] == list(NODE)
    assert reading["rotation"]["levels"] == [AMPLITUDE, AMPLITUDE, 0]
    assert tuple(reading["rotation"]["line"]) == simulation.node_record_coefficients(block)
    assert simulation.node_sources(0, "content") == [(NODE, COUNT)]
    for _ in range(12):
        simulation.step()  # a cloud of 300 under the edge: the count's line clamps what a Node at 0 would give
    levels = dict(simulation.snapshot_stream())["blocks"][0]["rotation"]["levels"]
    assert levels[0] != levels[1] and block.counts is not None and block.counts.min() >= 0
