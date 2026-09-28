"""A moving body loads moving (ALGEBRA.md #the-generator (e), #the-velocity): the mode file's two levels and proper pair, read by the loader and written by the assembly, move the body by the count's line one Link per 1 / v intervals, v = n / (3 Q M) from the file's numbers alone."""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import input_digest, parse_world_document, world_files

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from body_generator import clock_pair, generate, mode_document, split_levels, to_amplitude  # noqa: E402

CHAIN, NODES, COUNT = 120, 3, 1000


def test_a_moving_body_loads_moving_and_moves_one_link_per_1_over_v_intervals(tmp_path: Path) -> None:
    """One open chain, one body of matter by its Nodes with their counts and its momentum n along x; the mode by the generator's functions, its amplitude brought under the file's bound by the generator's own division act ((f): the fixed point does not depend on A beyond its resolution); after t intervals the body's corner has moved n t div W Links, W = 3 Q M, within one Link of the rounding."""
    sys.set_int_max_str_digits(0)
    universe = json.loads((ROOT / "examples/events/generated/universe.json").read_text(encoding="utf-8"))
    for row in universe["families"]:
        for read in row.get("reads", []):
            read["twist"] = (
                0  # the transport's twist is another primitive's; this test is the count's line's
            )
    path = tmp_path / "universe.json"
    path.write_text(json.dumps(universe))
    bound, unit = universe["integers"]["amplitude_bound"], universe["integers"]["momentum_unit"]
    wall = 3 * unit * NODES * COUNT
    momentum = wall // 20
    corner = CHAIN // 2 - NODES // 2
    nodes = [{"node": [corner + i, 0, 0], "count": COUNT} for i in range(NODES)]
    body = {
        "family": "matter",
        "nodes": nodes,
        "momentum": [momentum, 0, 0],
        "momentum_before": [momentum, 0, 0],
    }
    world = {
        "shape": [CHAIN, 1, 1],
        "boundary": {"x": "open", "y": "periodic", "z": "periodic"},
        "ticks": 1,
    }
    world.update(
        {"N": 64, "engine": "examples/events/engine_start.json", "universe": str(path), "face_depth": 16}
    )
    world.update({"measured": [{**body, "phase_denominator": 256}], "detectors": []})
    reading = generate(world)
    entry = reading["bodies"][0]
    assert "refused" not in entry, entry.get("refused")
    profiles, levels = split_levels(reading)
    (profiles[0],) = to_amplitude((profiles[0],), bound // 2)
    levels[0] = to_amplitude(levels[0], bound // 2)
    entry["clock"] = list(clock_pair(Fraction(*entry["clock"]), bound // 2))
    mode = mode_document(reading, profiles, levels)
    mode["world_digest"] = input_digest(world)
    files = {**world_files(world), str(path): universe, "world.mode.json": mode}
    simulation = DetectorLawSimulation(parse_world_document(world, files, input_digest(world)))
    block = simulation.blocks[0]
    assert list(block.own.now.ravel()) == mode["bodies"][0]["moving"]["now"] and block.own.now.any()
    start, intervals = block.corner[0], 3 * wall // momentum
    for _ in range(intervals):
        simulation.step()
    expected = momentum * intervals // wall
    assert expected >= 3 and abs((block.corner[0] - start) - expected) <= 1
