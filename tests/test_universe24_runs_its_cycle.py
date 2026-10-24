"""The test of the law's course for Universe24, the one world (examples/events/universe24/; the fold of 2026-10-24, the owner's word: the file is the universe at nature's den, the board's shape and the run's length alone, no body, no detector, no option key; and the same day's later word: declaring a family is forbidden, the universe file one object of integers and no family row, ALGEBRA.md, The circle of den): (1) the bare world parses with the family-less universe, its seed the massless point and every point of den's circle a row of two lines; (11) the small bare torus of the tests' small universe is seeded with the massless point at one quantum on every Node but the origin (the owner's closure of 2026-10-24: the uniform sea births nothing, the hole opens the draw), bangs and births pairs of den's points at the senses -1 and 1 (the rolled run, the former (12), stands in tests/test_the_draw_reads_the_nodes_own_frame.py on every array since the tests' audit of 2026-10-24). The replay of the shipped eras log's first eight lines (the former (6)) left 2026-10-24 with the family-less file: the record stands as the law's to the former file, to be re-recorded once after everything (the Boss's word)."""

import copy
import json
from pathlib import Path
from typing import Any

import pytest

from event_universe import world_files
from event_universe.lattice import Lattice
from event_universe.loader.circle import vector_of
from event_universe.loader.universe import MASSLESS, SIGN, VOLUME
from event_universe.world_files import load_world
from tests.laws_universe import CUBE, GAMMA, UNIVERSE, WORLD, flat, small_universe


def test_the_fold_accepts_the_bare_world_and_refuses_a_former_key() -> None:
    """(1) The one world's file is the universe, the shape and the run's length alone and parses with no mode file, its seed the massless point on one real line (the row named by what it is, the page's caption light), the rows the volume holder, the sign holder, the massless point and the 26 points of the file's den (the PeV tier since 2026-10-24, 26 at the top tier too), every point a row of two lines named by its vector; the former keys `bodies` and `interval` of the world and `families` of the universe refused by name."""
    world = json.loads(WORLD.read_text(encoding="utf-8"))
    universe = json.loads(UNIVERSE.read_text(encoding="utf-8"))
    files = {
        world["universe"]: json.loads(
            '{"integers": {"den": 1166991900949580266237, "node_clock": 1000, "quantum_action": 36000}}'
        )
    }  # the shipped world's keys with the top tier's den: the fold accepts the bare world at every den, and the loader's circle test alone factors the PeV den (2026-10-24)
    from event_universe.loader.world import parse_world

    assert (
        set(world) == {"universe", "shape", "intervals"} and not WORLD.with_suffix(".mode.json").exists()
    )
    assert set(universe) == {"integers"}  # no family row (2026-10-24)
    parsed = parse_world(world, files)  # (1) the bare world, accepted
    names = [family.name for family in parsed.families]
    assert names[:3] == [VOLUME, SIGN, MASSLESS] and names[parsed.seed] == MASSLESS
    assert len(names) == 3 + 3**3 - 1 and all(vector_of(name) is not None for name in names[3:])
    assert all(
        family.plane and family.width == 2 for family in parsed.families[3:]
    )  # two lines for a gap, per record
    emptied = {**world, "bodies": []}  # the declared bodies, a key refused since 2026-10-24
    with pytest.raises(ValueError, match="unknown key 'bodies'"):
        parse_world(emptied, files)
    former = copy.deepcopy(world)
    former["interval"] = "unobservable"
    with pytest.raises(ValueError, match="unknown key 'interval'"):
        parse_world(former, files)
    declared = {**universe, "families": [{"name": "light", "pair": [2, 2], "dimension": 1}]}
    with pytest.raises(ValueError, match="holds the key 'families', a declaration no file carries"):
        parse_world(world, {**files, world["universe"]: declared})


def bare_board(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, lines: list[dict[str, Any]], intervals: int = 60
) -> Lattice:
    """The tests' small universe on the bare 3-cube torus with its output kept."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    small_universe(tmp_path)
    bare = {"universe": "u.json", "shape": [CUBE] * 3, "intervals": intervals}
    (path := tmp_path / "bare.json").write_text(json.dumps(bare), encoding="utf-8")
    return Lattice(load_world(path), output=lines.append)


def test_the_bare_torus_is_seeded_with_the_hole_bangs_and_births_the_pairs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """(11) The folded sentences on the small bare torus (ALGEBRA.md, The uniform seed is a lay, the closure of 2026-10-24; The board reads itself): the seed is the massless point at the drift 189 now and 0 before on every Node but the origin, where no quantum is laid; the volume holder at rest at Gamma; the hole parts the Nodes and the draw births a pair of one point of den's circle at the senses -1 and 1, paying by the hole at its Node; the credit and birth lines name the point by its vector; the births go on as the sea rises."""
    lines: list[dict[str, Any]] = []
    board = bare_board(tmp_path, monkeypatch, lines)
    names, light = [family.name for family in board.families], board.world.seed
    assert light is not None and names[light] == MASSLESS
    laid = board.states[light].lines[0]
    assert (
        flat(laid.now) == [0] + [189] * (CUBE**3 - 1) and flat(laid.before) == [0] * CUBE**3
    )  # the hole at the origin
    assert flat(board.quanta(light)[0]) == [0] + [1] * (CUBE**3 - 1)
    g = names.index(VOLUME)
    assert flat(board.states[g].lines[0].now) == [GAMMA] * CUBE**3  # the seed at rest, no rest solve
    births: list[dict[str, Any]] = []
    while not births and board.interval < 60:
        board.step()
        births = [line for line in lines if line.get("event") == "birth"]
    assert births and births[0]["interval"] < 60
    for birth in births:
        for child in birth["children"]:
            assert vector_of(child) is not None and board.families[names.index(child)].plane
        assert (
            len(birth["children"]) == len(birth["senses"]) >= 2 and sum(birth["senses"]) == 0
        )  # one record per child, the senses summing to 0 (2026-10-24)
    credits = [line for line in lines if line.get("event") == "credit"]
    assert credits and all(
        c["absorbed"] == MASSLESS and vector_of(c["realised"]) is not None for c in credits
    )
    assert all(0 <= c["node_detector"] < CUBE**3 for c in credits)  # the Nodes by index
    for _ in range(20):
        board.step()
    later = [line for line in lines if line.get("event") == "birth"]
    assert len(later) > len(births) and board.credit.counts[names.index(later[-1]["children"][0])] > 0
