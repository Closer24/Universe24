"""The matter world of Universe24 on the small structured board (examples/events/universe24/universe24_matter.json; the owner's word of 2026-10-23, matter and a bound body must be created; the owner's rule, every test of the law's course on a structured board): the universe with matter at the Pythagorean pair [600, 1000] (1000^2 - 600^2 = 800^2), the holder of the sign (a held row sourced by the Wronskian) and the atom's two plane families reading it, the proton [0, 1000] at the read 1 and the electron [800, 1000] at the read 3, laid on the 3-cube torus with gravity's gap [990, 1000] (the universe test's short course), one clump of matter, light uniform and the atom's two bodies at two adjacent void Nodes. The clauses, the law's own readings: (1) the conversion is derived from the pairs with no key (ALGEBRA.md, The conversion): the proton's list is matter and the electron, and matter, light and the electron convert into nothing (light massless, no gap; matter and the electron with no list of other gapped families keeping the conservations); (2) a conversion click needs a region's draw, and on this torus the draw is refused by name, since no lay with an end passes a declared region (a wave filling a periodic ring), so matter's creation by the conversion click is not drawable on Universe24's torus and the sentence is the loader's; (3) the world with the atom's bodies loads and runs through the board's top and its turn with no refusal, the proton's record standing on the board through the turn (its quanta over the board at least one before and after the top) and the fifth act firing; what stands at the proton's own Node is read on the 5-torus in the README; (4) the lay with an end that the draw asks for, on the birth world (the clump laid in the dust family, the converting parent whose derived list is matter and partner, no matter record laid, light uniform): a light packet laid along z with the wave [1, 2] toward a 2 x 2 x 2 region about the clump (a thinner region is refused by name, under half the wavelength across an axis read through the wrap) with the world's draw declared empty loads with the region's window derived as the packet's passage, 5 intervals on the 3-cube; at every close the region's draw credits the LIGHT standing in it and never the dust's record, the light's quanta taken and written nowhere (the books' light deficit 7 at the refusal, the clicks hand's finding), and at the seventh close, the interval 35, the digits read are spent before any other draw, the run refused by name ("the digits read are spent at this interval by its earlier draws"): no conversion click fires and matter is born nowhere on this board, read and not declared around (on the 5-torus the refusal at the close 18 with the deficits 0)."""

import json
from pathlib import Path

import pytest

from event_universe import world_files
from event_universe.lattice import Lattice
from event_universe.loader.universe import universe_of
from event_universe.world_files import input_digest, load_world
from tests.laws_universe import CLUMP, CUBE, GAMMA, GAP, NOW, flat

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


BIRTH_UNIVERSE = {
    "integers": {"node_clock": GAMMA, "quantum_action": 36000, "width": 92, "link_unit": 16},
    "families": [
        {
            "name": "gravity",
            "pair": [GAP, GAMMA],
            "reads": {"gravity": 1},
            "held": {"sources": ["form", "tensions"], "level_weight": 1, "write_weight": 1},
        },
        {"name": "dust", "pair": [0, GAMMA], "reads": {"gravity": 1}, "dimension": 1},
        {"name": "matter", "pair": [600, GAMMA], "reads": {"gravity": 1}, "dimension": 1},
        {"name": "partner", "pair": [800, GAMMA], "reads": {"gravity": 1}, "dimension": 1},
        {"name": "light", "pair": [GAMMA, GAMMA], "reads": {"gravity": 1}, "dimension": 1},
    ],
}  # the birth world's universe: the dust at the frozen pair the converting parent, its derived list matter and partner, no sign holder
DUST_COUNT = 253  # the gate's count of the dust clump's share on the 3-cube at T 36,000


def birth_world(folder: Path) -> Path:
    """The birth world small: the clump laid in the dust family, the converting parent (no matter record laid, matter stands nowhere until born), light uniform, a light packet with an end laid along z at [1, 1, 0] toward the clump at [1, 1, 1] with the wave [1, 2], a 2 x 2 x 2 region about the clump (x 1..2, y 1..2, z 1..2) and the world's draw declared empty, so the region's window derives as the packet's passage; the packet's two levels written with zero sums as a massless lay asks."""
    (folder / "u.json").write_text(json.dumps(BIRTH_UNIVERSE), encoding="utf-8")
    nodes = [[x, y, z] for x in range(CUBE) for y in range(CUBE) for z in range(CUBE)]
    at = lambda node: (node[0] * CUBE + node[1]) * CUBE + node[2]  # noqa: E731
    region = [[x, y, z] for x in (1, 2) for y in (1, 2) for z in (1, 2)]
    world: dict[str, object] = {
        "shape": [CUBE] * 3,
        "boundary": {"x": "periodic", "y": "periodic", "z": "periodic"},
        "intervals": 100,
        "universe": "u.json",
        "bodies": [
            {"family": "dust", "nodes": [{"node": CLUMP, "count": DUST_COUNT}]},
            {
                "family": "light",
                "nodes": [
                    {"node": n, "count": LIGHT_COUNTS.get(tuple(n), 1)} for n in nodes if n != CLUMP
                ],
            },
        ],
        "node_detectors": [{"name": "clump", "positions": region}],
        "draw": {},
        "packets": [
            {
                "family": "light",
                "along": "z",
                "wave": [1, 2],
                "phase": [0, 1],
                "amplitude": 300,
                "top": {"x": [1, 1], "y": [1, 1], "z": [0, 0]},
                "edge": {"x": 0, "y": 0, "z": 0},
            }
        ],
    }
    levels = lambda node, now: [now if i == at(node) else 0 for i in range(CUBE**3)]  # noqa: E731
    now, before = [0] * CUBE**3, [0] * CUBE**3
    now[at([1, 1, 0])], now[at([1, 1, 2])], now[at([0, 1, 0])] = 300, -150, -150
    before[at([1, 1, 2])], before[at([1, 1, 0])], before[at([0, 1, 2])] = 300, -150, -150
    mode = {
        "world_digest": input_digest(world),
        "bodies": [
            {
                "family": "dust",
                "pair": [0, GAMMA],
                "moving": {"now": levels(CLUMP, NOW), "before": [0] * CUBE**3},
            },
            {
                "family": "light",
                "pair": [GAMMA, GAMMA],
                "moving": {"now": [636] * CUBE**3, "before": [446] * CUBE**3},
            },
        ],
        "packets": [
            {"family": "light", "pair": [GAMMA, GAMMA], "moving": {"now": now, "before": before}}
        ],
    }
    path = folder / "birth.json"
    path.write_text(json.dumps(world), encoding="utf-8")
    path.with_suffix(".mode.json").write_text(json.dumps(mode), encoding="utf-8")
    return path


LIGHT_COUNTS: dict[tuple[int, int, int], int] = {
    (1, 1, 0): 7,
    (1, 1, 2): 6,
    (0, 1, 0): 6,
}  # the light body's counts where the packet adds its share, the gate's reading


def test_the_packet_with_an_end_derives_the_window_and_the_draw_is_spent_before_the_conversion(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    lines: list[dict[str, object]] = []
    board = Lattice(load_world(birth_world(tmp_path)), output=lines.append)
    assert (
        board.world.draw is not None and board.world.draw.window == 5
    )  # (4) the window the packet's passage, derived
    names = [family.name for family in board.families]
    dust = board.families[names.index("dust")]
    assert {names[index] for index, _sense in dust.converts} == {
        "matter",
        "partner",
    }  # the parent's derived list
    with pytest.raises(
        RuntimeError, match="the digits read are spent at this interval by its earlier draws"
    ) as refusal:
        for _ in range(60):
            board.step()
    assert board.interval == 35 and "at the interval 35" in str(refusal.value), (
        board.interval
    )  # refused at the seventh close
    credits = [line for line in lines if line.get("event") == "credit"]
    assert credits and {str(c["family"]) for c in credits} == {
        "light"
    }  # the light standing in the region drawn at every close, never the dust's record
    books = board.books()
    assert books["light"]["deficit"] == 7 and all(
        books[name]["deficit"] == 0 for name in ("dust", "matter", "partner")
    ), books  # the light's quanta taken by the region and written nowhere, the clicks hand's finding
    assert not [
        line for line in lines if line.get("event") == "conversion"
    ]  # no conversion click, matter born nowhere
