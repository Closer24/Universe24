"""The orbit world `s32_r12` of series D (examples/events/orbit/README.md;
the register entry "D, the orbit under the law of the ray, on the plane
(2026-09-19)" in docs/EXPERIMENTS.md): one world, one interval count, one
pinned position, read from the registered run of 2026-09-19 (source
fingerprint 587cbf48..., the expected integers of docs/TEST_EXPECTATIONS.md
"The worlds of the ray law" (e), written down before this test's first
run). Under the width S = 32 the probe of content 1 with momentum [0, 9, 0]
at r = 12 turns once about the source in 346 intervals (the derivation's
343) and is then at (71, 60, 0), one Link from its start on x and none on
y, with its momentum's y component still positive: the one closing of the
series. The test replays the world through the API for 346 intervals; it
pins the reading of a registered run so that a change of the step rule, the
flight or the push is seen, and is the register's milestone, not a law
(the rule of 2026-09-17 in CONTRIBUTING.md keeps research runs out of the
suite: if the model owner reads this pin as one, the register keeps the
numbers and this module goes). About 0.4 s of host time.
"""

from __future__ import annotations

import json
from pathlib import Path

from event_universe.events import RaySimulation, parse_ray_world

ROOT = Path(__file__).resolve().parents[1]
WORLD = ROOT / "examples" / "events" / "orbit" / "s32_r12.json"
CLOSING_TICK = 346
START = (72, 60, 0)
CLOSING_NODE = (71, 60, 0)


def test_the_probe_of_s32_r12_turns_once_in_346_intervals_and_returns_one_link_off():
    """(e)."""
    world = parse_ray_world(json.loads(WORLD.read_text(encoding="utf-8")))
    assert world.width == 32 and len(world.directions) == 124
    simulation = RaySimulation(world)
    probe = simulation.measured[2]
    assert probe.position == START and probe.momentum == [0, 9, 0]
    for tick in range(1, CLOSING_TICK + 1):
        simulation.step()
        assert simulation.books()["balanced"], tick
    assert probe.position == CLOSING_NODE
    assert probe.momentum[1] > 0
    assert probe.age == CLOSING_TICK and probe.waited == 0
