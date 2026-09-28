"""THE BOUND BODY IS ONE NODE (ALGEBRA.md #the-primitives, THE RULE'S OWN UNIVERSE): in a universe whose every held divisor is 1 a body of one declared Node on a massive pair is a bound body: its record is the one-Node line at its Node, stepped by the rule with the content there, no record of it lies on the GameBoard, the hold sources its count, and the step back is exact."""

from __future__ import annotations

import json
from pathlib import Path

import event_universe.world_files as world_files
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import input_stamp, load_world

ROOT = Path(__file__).resolve().parents[1]
UNIVERSE = ROOT / "examples" / "events" / "experiments" / "universe.json"
START = ROOT / "examples" / "events" / "engine_start.json"
NODE, COUNT, SIDE, CLOCK, AMPLITUDE = (
    (4, 4, 4),
    300,
    9,
    12000,
    17,
)  # the pixel, c, the side, Gamma, isqrt(c)


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
    body = {"family": "matter", "nodes": [{"node": list(NODE), "count": COUNT}]}
    body.update(momentum=[0, 0, 0], momentum_before=[0, 0, 0], phase_denominator=1024)
    world = {"shape": [SIDE, SIDE, SIDE], "boundary": {"x": "closed", "y": "closed", "z": "closed"}}
    world.update(ticks=64, N=1024, measured=[body], universe="universe.json", engine="start.json")
    world["detectors"] = [{"name": "own", "positions": [list(NODE)]}]
    world["stamp"] = input_stamp(world)
    (tmp_path / "pixel.json").write_text(json.dumps(world), encoding="utf-8")
    profile = [0] * SIDE**3
    profile[(NODE[0] * SIDE + NODE[1]) * SIDE + NODE[2]] = AMPLITUDE
    entry = {
        "family": "matter",
        "pair": [800, 1200],
        "profile": profile,
        "twist": 0,
        "clock": [432, 300],
    }
    mode = {"world_digest": world["stamp"]["hash"], "bodies": [entry]}
    (tmp_path / "pixel.mode.json").write_text(json.dumps(mode), encoding="utf-8")
    return tmp_path / "pixel.json"


def test_under_the_divisor_1_the_one_node_body_is_its_node_record_and_steps_back_exactly(
    tmp_path, monkeypatch
):
    """Under the divisors 1 the body has a Node record and no record on the GameBoard; under the universe of record's divisors it has its lattice record as before. The Node record steps by the one-Node line with the content at its Node, wall x next + r' = coefficient x now - wall x before + r with the coefficients read at its Node before the step (the content there moves with the fields, so the line's integers move with it), the hold sources the declared count at the Node, and twelve intervals forward then back return the record's levels and remainder bit for bit."""
    lattice = DetectorLawSimulation(load_world(pixel_world(tmp_path / "record", monkeypatch, 40000)))
    assert lattice.blocks[0].node_record is None and lattice.blocks[0].own is not None
    simulation = DetectorLawSimulation(load_world(pixel_world(tmp_path / "rule", monkeypatch, 1)))
    block = simulation.blocks[0]
    record = block.node_record
    assert record is not None and block.own is None and not simulation.records
    assert (record.now, record.before, record.remainder) == (AMPLITUDE, AMPLITUDE, 0)
    assert simulation.node_sources(0, "content") == [(NODE, COUNT)]
    levels = []
    for _ in range(12):
        levels.append((record.now, record.before, record.remainder))
        coefficient, wall = simulation.node_record_coefficients(block)
        simulation.step()
        now, before, remainder = levels[-1]
        assert wall * record.now + record.remainder == coefficient * now - wall * before + remainder
    assert record.now != record.before  # the record rotates at its Node
    for tick in range(12, 0, -1):
        simulation.step_inverse()
        assert (record.now, record.before, record.remainder) == levels[tick - 1]
