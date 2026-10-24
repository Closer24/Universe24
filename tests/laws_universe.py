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
CHARGE_LEVEL = 173  # isqrt(T / (2 sin omega_0)) at T 36,000 and the electron's sine 0.6: one quantum of charge, its Wronskian T / 2 within the rounding


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


def atom_world(
    folder: Path,
    electron: list[int] = ELECTRON,
    proton: list[int] = PROTON,
    region: bool = False,
    draw: bool = False,
    reads: dict[str, int] | None = None,
) -> Path:
    """The small structured board with the atom's two bodies, the universe file's families with gravity's gap widened to [GAP, Gamma]: the clump in matter [600, 1000] at the shipped lightest clump's levels (the before level 0.6 of the now), light uniform, the proton's pixel [0, 1000] and the electron's plane [800, 1000] (the sign holder's two readers) at two void Nodes, the proton at the level the gate reads as one quantum and the electron rotating in the sense +1 at one quantum of charge (its Wronskian T / 2 within the rounding, the count-1 gate), and, where asked, a two-Node region and the world's draw; `reads` replaces the two readers' reads where given (the sign alone: the content 0, the exact vacuum paces)."""
    universe = json.loads(UNIVERSE.read_text(encoding="utf-8"))
    universe["families"][0]["pair"] = [GAP, GAMMA]
    for row in universe["families"]:
        if reads is not None and row["name"] in ("proton", "electron"):
            row["reads"] = dict(reads)
    (folder / "u.json").write_text(json.dumps(universe), encoding="utf-8")
    nodes = [[x, y, z] for x in range(CUBE) for y in range(CUBE) for z in range(CUBE)]
    world: dict[str, object] = {
        "shape": [CUBE] * 3,
        "intervals": 100,
        "universe": "u.json",
        "bodies": [
            {"family": "matter", "nodes": [{"node": CLUMP, "count": COUNT}]},
            {
                "family": "light",
                "nodes": [
                    {"node": at, "count": 1} for at in nodes if at not in (CLUMP, proton, electron)
                ],
            },
            {"family": "proton", "nodes": [{"node": proton, "count": 1}]},
            {"family": "electron", "nodes": [{"node": electron, "count": 1}]},
        ],
        "node_detectors": [{"name": "detector", "positions": [[2, 0, 0], [2, 0, 1]]}] if region else [],
    }
    if draw:
        world["draw"] = {}
    at = lambda node: (node[0] * CUBE + node[1]) * CUBE + node[2]  # noqa: E731
    levels = lambda node, now: ([now if i == at(node) else 0 for i in range(CUBE**3)])  # noqa: E731
    mode = {
        "world_digest": input_digest(world),
        "bodies": [
            {
                "family": "matter",
                "pair": [600, GAMMA],
                "moving": {"now": levels(CLUMP, NOW), "before": levels(CLUMP, BEFORE)},
            },
            {
                "family": "light",
                "pair": [GAMMA, GAMMA],
                "moving": {"now": [LEVEL] * CUBE**3, "before": [LEVEL - SPEED] * CUBE**3},
            },
            {
                "family": "proton",
                "pair": [0, GAMMA],
                "moving": {"now": levels(proton, 189), "before": [0] * CUBE**3},
            },
            {
                "family": "electron",
                "pair": [800, GAMMA],
                "moving": {  # one quantum of charge by hand, 2 L^2 sin omega_0 = T: the level now (L, 0), the level before the band's rest rotation in the sense +1, (L cos omega_0, L sin omega_0)
                    "now": levels(electron, CHARGE_LEVEL),
                    "before": levels(electron, CHARGE_LEVEL * 800 // GAMMA),
                    "im_now": [0] * CUBE**3,
                    "im_before": levels(electron, CHARGE_LEVEL * 600 // GAMMA),
                },
            },
        ],
        "packets": [],
    }
    path = folder / "atom.json"
    path.write_text(json.dumps(world), encoding="utf-8")
    path.with_suffix(".mode.json").write_text(json.dumps(mode), encoding="utf-8")
    return path


def flat(array: Any) -> list[int]:
    return [int(x) for x in np.asarray(array, dtype=object).reshape(-1)]
