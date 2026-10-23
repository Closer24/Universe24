"""The shared builders of the Universe24 tests (tests/test_universe24_runs_its_cycle.py, tests/test_the_matter_world_on_the_torus.py, tests/test_the_torus_page_draws_the_log.py): the shipped folder's paths, the small structured 3-cube torus's numbers (the gap, the lightest clump's levels, the detector's region, the instrument bodies' Nodes and resonances) and `small_world`, which writes the small universe, world and mode file beside each other, with `flat` for the arrays' integers; moved here on 2026-10-23 so that no test module imports another (tools/tests_shape.py, rule (b))."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np

from event_universe.world_files import input_digest
from tests.laws import ROOT, load_file

FOLDER = ROOT / "examples" / "events" / "universe24"
WORLD, UNIVERSE = FOLDER / "universe24.json", FOLDER / "universe_universe24.json"
LOG = FOLDER / "universe24.eras.jsonl"
ERAS = load_file("eras", ROOT / "tools" / "eras.py")
GAMMA, CUBE, LEVEL, SPEED, GAP = 1000, 3, 636, 190, 990
CLUMP, COUNT, NOW, BEFORE = (
    [1, 1, 1],
    489,
    3015,
    2008,
)  # the shipped lightest clump's levels, the gate's count of its share on the 3-cube at T 36,000
DETECTOR = [
    [0, 0, 0],
    [0, 0, 1],
]  # the smallest region the law admits: through one Node what enters leaves


ABSORBER = [
    2,
    2,
    2,
]  # the click variant's instrument body, the clicks world's absorber reading the light
SECOND = [0, 2, 0]  # the second instrument of the many-clicks clause, two Links from the first
RESONANCES = (
    810,
    868,
)  # the two instruments' resonance pairs over Gamma, their derived beats 11 and 13 (period_of)
BEFORE_TOP, AFTER_TOP = (
    2,
    1,
)  # the two instruments' clicks on the small structured board, before and after its top, as read


def small_world(
    folder: Path, detector: bool = True, absorber: bool = False, resonances: tuple[int, ...] = (902,)
) -> Path:
    """The shipped universe's three families with gravity's gap widened to [GAP, Gamma], one clump at the centre of the 3-cube torus at the shipped lightest clump's two levels, light uniform at LEVEL now and LEVEL - SPEED before on every Node (declared on the void Nodes, one quantum each at v^2 near T), and the detector on two Nodes."""
    universe = json.loads(UNIVERSE.read_text(encoding="utf-8"))
    universe["families"][0]["pair"] = [GAP, GAMMA]
    if absorber:
        universe["families"].append(
            {"name": "absorber", "pair": [666, GAMMA], "reads": {"gravity": 1}, "dimension": [2, 2]}
        )
    (folder / "u.json").write_text(json.dumps(universe), encoding="utf-8")
    nodes = [[x, y, z] for x in range(CUBE) for y in range(CUBE) for z in range(CUBE)]
    world: dict[str, Any] = {
        "shape": [CUBE] * 3,
        "boundary": {"x": "periodic", "y": "periodic", "z": "periodic"},
        "intervals": 200,
        "universe": "u.json",
        "bodies": [
            {"family": "matter", "nodes": [{"node": CLUMP, "count": COUNT}]},
            {
                "family": "light",
                "nodes": [
                    {"node": at, "count": 1}
                    for at in nodes
                    if at != CLUMP and not (absorber and at in (ABSORBER, SECOND)[: len(resonances)])
                ],
            },
        ],
        "node_detectors": [{"name": "detector", "positions": DETECTOR}] if detector else [],
    }
    for at, resonance in zip((ABSORBER, SECOND), resonances, strict=False) if absorber else ():
        world[
            "bodies"
        ].append(  # declared as examples/events/universe24/universe24_click.json declares it
            {
                "family": "absorber",
                "nodes": [{"node": at, "weight": 1}],
                "parts": [{"part": 0, "name": "g", "count": 1}, {"part": 1, "name": "e", "count": 0}],
                "transitions": [
                    {
                        "from": "g",
                        "to": "e",
                        "drive": "light",
                        "weight": [23, 2],
                        "resonance": [resonance, GAMMA],
                    }
                ],
                "rates": [{"from": "e", "to": "g", "lifetime": 24, "gives_to": "light"}],
                "node_detector": {},
            }
        )
    at = nodes.index(CLUMP)
    now, before = [0] * len(nodes), [0] * len(nodes)
    now[at], before[at] = NOW, BEFORE
    mode = {
        "world_digest": input_digest(world),
        "bodies": [
            {"family": "matter", "pair": [666, GAMMA], "moving": {"now": now, "before": before}},
            {
                "family": "light",
                "pair": [GAMMA, GAMMA],
                "moving": {"now": [LEVEL] * len(nodes), "before": [LEVEL - SPEED] * len(nodes)},
            },
        ],
        "packets": [],
    }
    path = folder / "small.json"
    path.write_text(json.dumps(world), encoding="utf-8")
    path.with_suffix(".mode.json").write_text(json.dumps(mode), encoding="utf-8")
    return path


def flat(array: Any) -> list[int]:
    return [int(x) for x in np.asarray(array, dtype=object).reshape(-1)]
