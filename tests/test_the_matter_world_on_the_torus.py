"""The matter world of Universe24 on the small structured board (examples/events/universe24/universe24_matter.json; the owner's word of 2026-10-23, matter and a bound body must be created; the owner's rule, every test of the law's course on a structured board): the universe with matter at the Pythagorean pair [600, 1000] (1000^2 - 600^2 = 800^2), the holder of the sign (a held row sourced by the Wronskian) and the atom's two plane families reading it, the proton [0, 1000] at the read 1 and the electron [800, 1000] at the read 3, laid on the 3-cube torus with gravity's gap [990, 1000] (the universe test's short course), one clump of matter, light uniform and the atom's two bodies at two adjacent void Nodes. The clauses, the law's own readings: (1) the conversion is derived from the pairs with no key (ALGEBRA.md, The conversion): the proton's list is matter and the electron, and matter, light and the electron convert into nothing (light massless, no gap; matter and the electron with no list of other gapped families keeping the conservations); (2) a conversion click needs a region's draw, and on this torus the draw is refused by name, since no lay with an end passes a declared region (a wave filling a periodic ring), so matter's creation by the conversion click is not drawable on Universe24's torus and the sentence is the loader's; (3) the world with the atom's bodies loads and runs through the board's top and its turn with no refusal, the proton's record standing on the board through the turn (its quanta over the board at least one before and after the top) and the fifth act firing; what stands at the proton's own Node is read on the 5-torus in the README."""

import json
from pathlib import Path

import pytest

from event_universe import world_files
from event_universe.lattice import Lattice
from event_universe.loader.universe import universe_of
from event_universe.world_files import input_digest, load_world
from tests.test_universe24_runs_its_cycle import CLUMP, CUBE, GAMMA, GAP, NOW, flat

PROTON, ELECTRON = [0, 2, 0], [0, 2, 1]
MATTER_COUNT = (
    429  # the gate's count of the clump's share at the pair [600, 1000] on the 3-cube at T 36,000
)
UNIVERSE = {
    "integers": {"node_clock": GAMMA, "quantum_action": 36000, "width": 92, "link_unit": 16},
    "families": [
        {
            "name": "gravity",
            "pair": [GAP, GAMMA],
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
        {"name": "electron", "pair": [800, GAMMA], "reads": {"gravity": 1, "charge": 3}, "dimension": 2},
    ],
}


def matter_world(folder: Path, region: bool = False, draw: bool = False) -> Path:
    """The small structured board of the universe test with the matter universe: the clump in matter [600, 1000] at the shipped lightest clump's levels (the before level 0.6 of the now), light uniform, the proton and the electron at two adjacent void Nodes at the levels the gate reads as one quantum each, and, where asked, a two-Node region and the world's draw."""
    (folder / "u.json").write_text(json.dumps(UNIVERSE), encoding="utf-8")
    nodes = [[x, y, z] for x in range(CUBE) for y in range(CUBE) for z in range(CUBE)]
    world: dict[str, object] = {
        "shape": [CUBE] * 3,
        "boundary": {"x": "periodic", "y": "periodic", "z": "periodic"},
        "intervals": 100,
        "universe": "u.json",
        "bodies": [
            {"family": "matter", "nodes": [{"node": CLUMP, "count": MATTER_COUNT}]},
            {
                "family": "light",
                "nodes": [
                    {"node": at, "count": 1} for at in nodes if at not in (CLUMP, PROTON, ELECTRON)
                ],
            },
            {"family": "proton", "nodes": [{"node": PROTON, "count": 1}]},
            {"family": "electron", "nodes": [{"node": ELECTRON, "count": 1}]},
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
                "moving": {"now": levels(CLUMP, NOW), "before": levels(CLUMP, round(NOW * 0.6))},
            },
            {
                "family": "light",
                "pair": [GAMMA, GAMMA],
                "moving": {"now": [636] * CUBE**3, "before": [446] * CUBE**3},
            },
            {
                "family": "proton",
                "pair": [0, GAMMA],
                "moving": {"now": levels(PROTON, 189), "before": [0] * CUBE**3},
            },
            {
                "family": "electron",
                "pair": [800, GAMMA],
                "moving": {"now": levels(ELECTRON, 189), "before": levels(ELECTRON, 151)},
            },
        ],
        "packets": [],
    }
    path = folder / "matter.json"
    path.write_text(json.dumps(world), encoding="utf-8")
    path.with_suffix(".mode.json").write_text(json.dumps(mode), encoding="utf-8")
    return path


def test_the_conversion_is_derived_for_the_proton_and_light_converts_into_nothing() -> None:
    _integers, families = universe_of(UNIVERSE)
    lists = {family.name: family.converts for family in families}
    by_name = [family.name for family in families]
    assert lists["proton"] and {by_name[index] for index, _sense in lists["proton"]} == {
        "matter",
        "electron",
    }  # (1)
    assert lists["light"] == () and lists["matter"] == () and lists["electron"] == ()


def test_the_matter_world_runs_through_its_turn_and_the_draw_is_refused_on_the_torus(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    with pytest.raises(
        ValueError, match="no lay with an end passes a declared region"
    ):  # (2) the conversion click's draw
        load_world(matter_world(tmp_path, region=True, draw=True))
    board = Lattice(load_world(matter_world(tmp_path)))
    board.output = lambda line: None
    g, names = board.held[0], [family.name for family in board.families]
    proton = names.index("proton")
    volumes, quanta = [], []
    for _ in range(60):
        board.step()  # (3) no refusal through the top and the turn
        volumes.append(sum(flat(board.states[g].lines[0].now)))
        quanta.append(int(sum(flat(board.quanta(proton)[0]))))
    top = volumes.index(max(volumes)) + 1
    assert 20 < top < 50 and any(s[1] == 1 for s in board.swaps), (top, board.swaps[:3])
    assert quanta[top - 1] >= 1 and quanta[-1] >= 1, (
        quanta[top - 1],
        quanta[-1],
    )  # the proton's record stands on the board through the turn
