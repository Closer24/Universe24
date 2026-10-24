"""The one world's helpers shared by the Universe24 tests (tests/test_universe24_runs_its_cycle.py, tests/test_matter_is_born_from_light.py, tests/test_the_sign_holder_and_the_pairs_on_the_small_torus.py, tests/test_the_torus_page_draws_the_log.py, tests/test_the_node.py, tests/test_the_bound_body.py): the shipped files' paths, the small structured board's constants as read on the one world, `small_world` (the shipped world cut to a small torus, with or without its detector and its one instrument body), `atom_world` (the small torus with the atom's two bodies, the proton's pixel and the electron's plane reading the sign holder) and `flat`."""

import json
from pathlib import Path
from typing import Any

import numpy as np

from event_universe.world_files import input_digest
from tests.laws import ROOT

FOLDER = ROOT / "examples" / "events" / "universe24"
WORLD, UNIVERSE = FOLDER / "universe24.json", FOLDER / "universe_universe24.json"
GAMMA, CUBE, LEVEL, SPEED, GAP = 1000, 3, 636, 190, 990
CLUMP, COUNT, NOW, BEFORE = (
    [1, 1, 1],
    429,
    3015,
    1809,
)  # the shipped lightest clump's levels at the pair [600, 1000] (the before level 0.6 of the now), the gate's count of its share on the 3-cube at T 36,000
DETECTOR = [
    [0, 0, 0],
    [0, 0, 1],
]  # the smallest region the law admits: through one Node what enters leaves


ABSORBER = [
    2,
    2,
    2,
]  # the click variant's instrument body, the clicks world's absorber reading the light
RESONANCE = 902  # the one instrument's resonance pair over Gamma, its derived beat 15 (period_of)
PROTON, ELECTRON = (
    [0, 2, 0],
    [0, 2, 1],
)  # the atom's two bodies at two adjacent void Nodes of the 3-cube torus


def small_world(
    folder: Path,
    detector: bool = True,
    absorber: bool = False,
    cube: int = CUBE,
) -> Path:
    """The shipped universe's three families with gravity's gap widened to [GAP, Gamma], one clump at the centre of the 3-cube torus at the shipped lightest clump's two levels, light uniform at LEVEL now and LEVEL - SPEED before on every Node (declared on the void Nodes, one quantum each at v^2 near T), the detector on two Nodes, and with `absorber` the one instrument body at ABSORBER reading the light (the two instruments' small world of the many-clicks clause left on 2026-10-24, every world but Universe24 cancelled)."""
    universe = json.loads(UNIVERSE.read_text(encoding="utf-8"))
    universe["families"][0]["pair"] = [GAP, GAMMA]
    if absorber and not any(family["name"] == "absorber" for family in universe["families"]):
        universe["families"].append(
            {"name": "absorber", "pair": [666, GAMMA], "reads": {"gravity": 1}, "dimension": [2, 2]}
        )
    (folder / "u.json").write_text(json.dumps(universe), encoding="utf-8")
    nodes = [[x, y, z] for x in range(cube) for y in range(cube) for z in range(cube)]
    world: dict[str, Any] = {
        "shape": [cube] * 3,
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
                    if at != CLUMP and not (absorber and at == ABSORBER)
                ],
            },
        ],
        "node_detectors": [{"name": "detector", "positions": DETECTOR}] if detector else [],
    }
    if absorber:
        world[
            "bodies"
        ].append(  # declared as examples/events/universe24/universe24.json declares its instruments
            {
                "family": "absorber",
                "nodes": [{"node": ABSORBER, "weight": 1}],
                "parts": [{"part": 0, "name": "g", "count": 1}, {"part": 1, "name": "e", "count": 0}],
                "transitions": [
                    {
                        "from": "g",
                        "to": "e",
                        "drive": "light",
                        "weight": [23, 2],
                        "resonance": [RESONANCE, GAMMA],
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
            {"family": "matter", "pair": [600, GAMMA], "moving": {"now": now, "before": before}},
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
