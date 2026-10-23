"""The gapped structured world of the swap-at-the-top tests (tests/test_the_swap_at_the_top.py, tests/test_a_write_that_writes_nothing_is_crossed_by_nothing.py): the 3-cube torus's numbers (Gamma 1,000, T 36,000, the cube 3), the held row of the content and `gapped_world`, which writes the universe, the world and its mode file with gravity gapped and the dust laid at one Node; moved here on 2026-10-23 so that no test module imports another (tools/tests_shape.py, rule (b))."""

from __future__ import annotations

import json

from event_universe.core import paces
from event_universe.world_files import input_digest

GAMMA, ACTION, CUBE = 1000, 36000, 3
HELD = {"sources": ["form", "tensions"], "level_weight": 1, "write_weight": 1}


def gapped_world(folder, gap, count, amplitude):  # type: ignore[no-untyped-def]
    """The 3-cube torus with gravity's pair [gap, Gamma] and dust [0, Gamma] laid uniform at the band's rest rotation (test_the_gapped_volume's world, the count the gate's own reading)."""
    universe = {
        "integers": {"node_clock": GAMMA, "quantum_action": ACTION, "width": 92, "link_unit": 16},
        "families": [
            {"name": "gravity", "pair": [gap, GAMMA], "reads": {"gravity": 1}, "held": HELD},
            {"name": "dust", "pair": [0, GAMMA], "reads": {"gravity": 1}, "dimension": 1},
        ],
    }
    (folder / "u.json").write_text(json.dumps(universe), encoding="utf-8")
    nodes = [[x, y, z] for x in range(CUBE) for y in range(CUBE) for z in range(CUBE)]
    world = {"shape": [CUBE] * 3, "boundary": {"x": "periodic", "y": "periodic", "z": "periodic"}}
    world.update(intervals=400, universe="u.json", node_detectors=[])
    world["bodies"] = [{"family": "dust", "nodes": [{"node": at, "count": count} for at in nodes]}]
    clock = paces.clock(GAMMA, 0)
    before = (2 * (GAMMA**3 - GAMMA * clock * clock) * amplitude + GAMMA**3) // (2 * GAMMA**3)
    entry = {
        "family": "dust",
        "pair": [0, GAMMA],
        "moving": {"now": [amplitude] * len(nodes), "before": [before] * len(nodes)},
    }
    path = folder / "swap.json"
    path.write_text(json.dumps(world), encoding="utf-8")
    path.with_suffix(".mode.json").write_text(
        json.dumps({"world_digest": input_digest(world), "bodies": [entry], "packets": []}),
        encoding="utf-8",
    )
    return path
