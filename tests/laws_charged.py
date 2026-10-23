"""The charged structured world of the swap tests (tests/test_the_swap_with_a_charge.py, tests/test_a_reading_across_a_mixed_link_is_framed.py): the 3-cube torus's numbers (Gamma 1,000, the gap, the charged pair [600, 1000] with its sine 800, the two centres) and `charged_world`, which writes the universe, the world and its mode file with the dust laid by layers so that a top may be split; moved here on 2026-10-23 so that no test module imports another (tools/tests_shape.py, rule (b))."""

from __future__ import annotations

import json
import math

import numpy as np

from event_universe.core import paces
from event_universe.world_files import input_digest

GAMMA, ACTION, CUBE, NUM = 1000, 36000, 3, 600
GAP, LAY = (
    GAMMA - 10,
    3,
)  # gravity's pair [990, 1000], the top within 50 intervals; the charged lay over 3, the counts in the tens
SINE = math.isqrt(GAMMA * GAMMA - NUM * NUM)  # 800: the charged pair's sine times den
CENTRES = [(0, 0, 0), (1, 1, 1)]


def charged_world(folder, gap, count, amplitude, intervals=400, weight=100, divisor=1, layers=None):  # type: ignore[no-untyped-def]
    """The gapped 3-cube torus with two one-quantum charged records (the count-1 gate's lay, tests/laws.sign_world), the dust everywhere else; `layers`, the dust's amplitude per layer x in place of `amplitude` (the deliberately split board of clause (5))."""
    universe = {
        "integers": {"node_clock": GAMMA, "quantum_action": ACTION, "width": 92, "link_unit": 16},
        "families": [
            {
                "name": "gravity",
                "pair": [gap, GAMMA],
                "reads": {"gravity": 1},
                "held": {"sources": ["form", "tensions"], "level_weight": 1, "write_weight": 1},
            },
            {"name": "dust", "pair": [0, GAMMA], "reads": {"gravity": 1}, "dimension": 1},
            {
                "name": "charge",
                "pair": [GAMMA, GAMMA],
                "reads": {"gravity": 1},
                "held": {"sources": ["wronskian"], "level_weight": weight},
            },
            {
                "name": "charged",
                "pair": [NUM, GAMMA],
                "reads": {"gravity": 1, "charge": 1},
                "dimension": 2,
            },
        ],
    }
    (folder / "u.json").write_text(json.dumps(universe), encoding="utf-8")
    shape = (CUBE,) * 3
    nodes = [
        [x, y, z]
        for x in range(CUBE)
        for y in range(CUBE)
        for z in range(CUBE)
        if (x, y, z) not in CENTRES
    ]
    world = {"shape": [CUBE] * 3, "boundary": {"x": "periodic", "y": "periodic", "z": "periodic"}}
    world.update(intervals=intervals, universe="u.json", node_detectors=[])
    bodies = [{"family": "dust", "nodes": [{"node": at, "count": count} for at in nodes]}]
    clock = paces.clock(GAMMA, 0)
    amplitudes = [
        (amplitude if layers is None else layers[x]) if (x, y, z) not in CENTRES else 0
        for x in range(CUBE)
        for y in range(CUBE)
        for z in range(CUBE)
    ]
    modes = [
        {
            "family": "dust",
            "pair": [0, GAMMA],
            "moving": {
                "now": amplitudes,
                "before": [
                    (2 * (GAMMA**3 - GAMMA * clock * clock) * a + GAMMA**3) // (2 * GAMMA**3) if a else 0
                    for a in amplitudes
                ],
            },
        }
    ]
    for centre in CENTRES:
        d = np.abs(np.indices(shape) - np.asarray(centre).reshape(3, 1, 1, 1)).sum(axis=0)
        profile = np.select([d == 0, d == 1], [1200, 600], 0)
        values = [int(v) for v in profile.ravel()]
        scale = math.isqrt(ACTION * GAMMA * 1000 * 1000 // (2 * SINE * sum(v * v for v in values)))
        levels = [v * scale // (1000 * divisor) for v in values]  # the one quantum's lay over `divisor`
        moving = dict(now=levels, before=[v * NUM // GAMMA for v in levels])
        moving.update(im_now=[0] * len(levels), im_before=[v * SINE // GAMMA for v in levels])
        bodies.append({"family": "charged", "nodes": [{"node": list(centre), "count": 1}]})
        modes.append({"family": "charged", "pair": [NUM, GAMMA], "moving": moving})
    world["bodies"] = bodies
    path = folder / "charged_swap.json"
    path.write_text(json.dumps(world), encoding="utf-8")
    path.with_suffix(".mode.json").write_text(
        json.dumps({"world_digest": input_digest(world), "bodies": modes, "packets": []}),
        encoding="utf-8",
    )
    return path
