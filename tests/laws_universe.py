"""The one world's helpers shared by the Universe24 tests (tests/test_universe24_runs_its_cycle.py, tests/test_matter_is_born_from_light.py, tests/test_the_sign_holder_and_the_pairs_on_the_small_torus.py, tests/test_the_torus_page_draws_the_log.py): the shipped files' paths (the folded world of 2026-10-24, the universe at nature's den, the board and the run's length alone), the declared seed's universe of 2026-10-23 kept by name (`DECLARED`, `declared_universe`: gravity [999, 1000], the sign holder, matter [600, 1000], light, the proton [0, 1000] and the electron [800, 1000] as planes, the absorber), the small structured board's constants as read on it, `small_world` (the declared seed's world cut to a small torus, with or without its detector and instrument bodies) and `flat`."""

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
# the declared seed's lightest clump's levels at the pair [600, 1000] (the before level 0.6 of the now), the gate's count of its share on the 3-cube at T 36,000
CLUMP, COUNT, NOW, BEFORE = [1, 1, 1], 429, 3015, 1809
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
RESONANCES = (810, 868)  # the two instruments' resonance pairs over Gamma, their derived beats 11 and 13
# the two instruments' clicks on the small structured board, before and after its top, read from the run under the content register (2026-10-24; 3 and 1 at the merge base c942951f2, where the register was the W = 0 sign holder's write room, an artefact removed by the Boss's word)
BEFORE_TOP, AFTER_TOP = 2, 2
# the declared seed's universe (examples/events/universe24/universe_universe24.json to 2026-10-23, kept by name on the fold of 2026-10-24: the one world's file is nature's den since, and the small structured board's tests read this seed)
DECLARED: dict[str, Any] = {
    "integers": {"node_clock": GAMMA, "quantum_action": 36000, "width": 92, "link_unit": 16},
    "families": [
        {
            "name": "gravity",
            "pair": [999, GAMMA],
            "reads": {"gravity": 1},
            "held": {"sources": ["form", "tensions"], "level_weight": 1, "write_weight": 1},
        },
        {
            "name": "charge",
            "pair": [GAMMA, GAMMA],
            "reads": {},
            "held": {"sources": ["wronskian"], "level_weight": 1},
        },
        {"name": "matter", "pair": [600, GAMMA], "reads": {"gravity": 1}, "dimension": 1},
        {"name": "light", "pair": [GAMMA, GAMMA], "reads": {"gravity": 1}, "dimension": 1},
        {"name": "proton", "pair": [0, GAMMA], "reads": {"gravity": 1, "charge": 1}, "dimension": 2},
        {"name": "electron", "pair": [800, GAMMA], "reads": {"gravity": 1, "charge": 1}, "dimension": 2},
        {"name": "absorber", "pair": [666, GAMMA], "reads": {"gravity": 1}, "dimension": [2, 2]},
    ],
}


def declared_universe() -> dict[str, Any]:
    """The declared seed's universe, a copy of its own (the heaviest-pair test's builder, tests/test_the_heaviest_pair_within_the_two_quanta.py)."""
    return json.loads(json.dumps(DECLARED))


def small_world(
    folder: Path,
    detector: bool = True,
    absorber: bool = False,
    resonances: tuple[int, ...] = (902,),
    cube: int = CUBE,
) -> Path:
    """The declared seed's universe with gravity's gap widened to [GAP, Gamma], one clump at the centre of the 3-cube torus at the shipped lightest clump's two levels, light uniform at LEVEL now and LEVEL - SPEED before on every Node (declared on the void Nodes, one quantum each at v^2 near T), and the detector on two Nodes."""
    universe = declared_universe()
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
                    if at != CLUMP and not (absorber and at in (ABSORBER, SECOND)[: len(resonances)])
                ],
            },
        ],
        "node_detectors": [{"name": "detector", "positions": DETECTOR}] if detector else [],
    }
    for at, resonance in zip((ABSORBER, SECOND), resonances, strict=False) if absorber else ():
        world[
            "bodies"
        ].append(  # declared as examples/events/universe24/universe24.json declares its instruments
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
