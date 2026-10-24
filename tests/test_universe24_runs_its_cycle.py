"""The test of the law's course for Universe24, the one world (examples/events/universe24/; the fold of 2026-10-24, the owner's word: the file is the universe at nature's den, the board's shape and the run's length alone, no body, no detector, no option key; and the same day's later word: declaring a family is forbidden, the universe file one object of integers and no family row, ALGEBRA.md, The circle of den): (1) the bare world parses with the family-less universe, its seed the massless point and every point of den's circle a plane; (11) the small bare torus of the tests' small universe is seeded with light at one quantum on every Node, bangs and births a pair of a point of den's circle at the first meeting, every Node alike. The replay of the shipped eras log's first eight lines (the former (6)) left 2026-10-24 with the family-less file: the record stands as the law's to the former file, to be re-recorded once after everything (the Boss's word), and until then its header names the former rows."""

import copy
import json
from pathlib import Path
from typing import Any

import pytest

from event_universe import world_files
from event_universe.lattice import Lattice
from event_universe.loader.circle import vector_of
from event_universe.loader.universe import MASSLESS, SIGN, VOLUME
from event_universe.world_files import input_digest, load_world
from tests.laws_universe import CUBE, GAMMA, UNIVERSE, WORLD, flat, small_universe


def test_the_fold_accepts_the_bare_world_and_refuses_a_former_key() -> None:
    """(1) The one world's file is the universe, the shape and the run's length alone and parses with no mode file, its seed the massless point on one real line (the row named by what it is, the page's caption light), the rows the volume holder, the sign holder, the massless point and the 242 points of nature's den, every point a plane named by its vector; the former keys `bodies` and `interval` of the world and `families` of the universe refused by name."""
    world = json.loads(WORLD.read_text(encoding="utf-8"))
    universe = json.loads(UNIVERSE.read_text(encoding="utf-8"))
    files = {world["universe"]: universe}
    from event_universe.loader.world import parse_world

    assert (
        set(world) == {"universe", "shape", "intervals"} and not WORLD.with_suffix(".mode.json").exists()
    )
    assert set(universe) == {"integers"}  # no family row (2026-10-24)
    parsed = parse_world(world, files, input_digest(world))  # (1) the bare world, accepted
    names = [family.name for family in parsed.families]
    assert names[:3] == [VOLUME, SIGN, MASSLESS] and names[parsed.seed] == MASSLESS
    assert len(names) == 3 + 3**5 - 1 and all(vector_of(name) is not None for name in names[3:])
    assert all(family.plane for family in parsed.families[3:])  # every point a plane until the kind sentence
    emptied = {**world, "bodies": []}  # the declared bodies, a key refused since 2026-10-24
    with pytest.raises(ValueError, match="unknown key 'bodies'"):
        parse_world(emptied, files, input_digest(emptied))
    former = copy.deepcopy(world)
    former["interval"] = "unobservable"
    with pytest.raises(ValueError, match="unknown key 'interval'"):
        parse_world(former, files, input_digest(former))
    declared = {**universe, "families": [{"name": "light", "pair": [2, 2], "dimension": 1}]}
    with pytest.raises(ValueError, match="holds the key 'families', a declaration no file carries"):
        parse_world(world, {**files, world["universe"]: declared}, input_digest(world))


def test_the_bare_torus_is_seeded_with_light_bangs_and_births_the_pairs_at_the_first_meeting(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """(11) The folded sentences on the small bare torus, the 3-cube with the tests' small universe and nothing declared (ALGEBRA.md, The uniform seed is a lay; The board reads itself; 2026-10-24): the seed is the massless point at one quantum on every Node, the level 189 now and 0 before; the volume holder at rest at Gamma; the bang uniform to the first meeting; there every Node alike births the pair of one point of den's circle at the senses -1 and 1 (the point the fit of act.born_table picks until the selection sentence), paying by the hole at its Node; the credit and birth lines name the point by its vector."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    small_universe(tmp_path)
    bare = {"universe": "u.json", "shape": [CUBE] * 3, "intervals": 60}
    (path := tmp_path / "bare.json").write_text(json.dumps(bare), encoding="utf-8")
    lines: list[dict[str, Any]] = []
    board = Lattice(load_world(path), output=lines.append)
    names, light = [family.name for family in board.families], board.world.seed
    assert light is not None and names[light] == MASSLESS
    seed = board.states[light].lines[0]
    assert flat(seed.now) == [189] * CUBE**3 and flat(seed.before) == [0] * CUBE**3
    assert flat(board.quanta(light)[0]) == [1] * CUBE**3 and board.credit.counts[light] == CUBE**3
    g = board.held[0]
    xs = lambda: flat(board.states[g].lines[0].now)  # noqa: E731
    assert xs() == [GAMMA] * CUBE**3  # the seed at rest
    births: list[dict[str, Any]] = []
    while not births and board.interval < 60:
        alike = xs()
        board.step()
        births = [line for line in lines if line.get("event") == "birth"]
    assert births and len(set(alike)) == 1 and alike[0] > GAMMA  # the bang, uniform to the birth
    first = births[0]["interval"]
    assert len(births) == CUBE**3 and all(b["interval"] == first for b in births)  # every Node alike
    child = births[0]["children"][0]
    assert vector_of(child) is not None and board.families[names.index(child)].plane
    assert all(b["children"] == [child] * 2 and b["senses"] == [-1, 1] for b in births)
    credits = [line for line in lines if line.get("event") == "credit"]
    assert sorted(c["node_detector"] for c in credits) == list(range(CUBE**3))  # the Nodes by index
    assert all(c["absorbed"] == MASSLESS and c["realised"] == child for c in credits)
    spent = board.states[light].lines[0]  # the record's line after the holes
    assert flat(spent.now) == [0] * CUBE**3 and flat(spent.before) == [0] * CUBE**3  # the holes
    assert board.credit.counts[light] == 0 and board.credit.counts[names.index(child)] == 2 * CUBE**3
