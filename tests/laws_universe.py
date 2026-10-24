"""The one world's helpers shared by the Universe24 tests (tests/test_universe24_runs_its_cycle.py, tests/test_matter_is_born_from_light.py, tests/test_the_sign_holder_and_the_pairs_on_the_small_torus.py, tests/test_the_torus_page_draws_the_log.py, tests/test_the_node.py, tests/test_the_bound_body.py): the shipped files' paths (the folded world of 2026-10-24, the universe at nature's den, the board and the run's length alone), the declared seed's universe of 2026-10-23 kept by name (`DECLARED`, `declared_universe`: gravity [999, 1000], the sign holder, matter [600, 1000], light, the proton [0, 1000] and the electron [800, 1000] as planes, the absorber), the small structured board's constants as read on it, `small_world` (the declared seed's world cut to a small torus, with or without its detector and its one instrument body), `atom_world` (the small torus with the atom's two bodies, the proton's pixel and the electron's plane reading the sign holder) and `flat`."""

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
    """The declared seed's universe with gravity's gap widened to [GAP, Gamma], one clump at the centre of the 3-cube torus at the shipped lightest clump's two levels, light uniform at LEVEL now and LEVEL - SPEED before on every Node (declared on the void Nodes, one quantum each at v^2 near T), the detector on two Nodes, and with `absorber` the one instrument body at ABSORBER reading the light (the two instruments' small world of the many-clicks clause left on 2026-10-24, every world but Universe24 cancelled)."""
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


def bare_torus(folder: Path, cube: int = CUBE, intervals: int = 60) -> Path:
    """The folded world's three keys on a bare torus of `cube` Nodes a side with the one universe file copied beside it (the folded loader, 2026-10-24: nothing declared, the light seeded on every Node); `world_files.REPOSITORY_ROOT` is `folder`."""
    (folder / "u.json").write_text(UNIVERSE.read_text(encoding="utf-8"), encoding="utf-8")
    world = {"universe": "u.json", "shape": [cube] * 3, "intervals": intervals}
    (path := folder / "bare.json").write_text(json.dumps(world), encoding="utf-8")
    return path


def flat(array: Any) -> list[int]:
    return [int(x) for x in np.asarray(array, dtype=object).reshape(-1)]
