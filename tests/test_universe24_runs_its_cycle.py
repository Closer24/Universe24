"""The test of the law's course for Universe24, the one world (examples/events/universe24/; the fold of 2026-10-24, the owner's word: the file is the universe at nature's den, the board's shape and the run's length alone, no body, no detector, no option key; ALGEBRA.md, The one Node, The uniform seed is a lay, The board reads itself, The swap at the top, The carried momentum): (1) the bare file loads with no mode file, its seed the light family; (11) on the small bare torus the seed is one quantum of light on every Node, the board bangs from it and births the electron pairs at the first meeting with the Node's index on the click's line, the books' count the cap; and the declared seed's small structured board of 2026-10-23 (tests/laws_universe.small_world: the 3-cube torus with one clump of matter at the pair [600, 1000], the light family at the uniform level 636 with the velocity 190 and the detector on two Nodes, gravity's gap widened to [990, 1000] so that the course is ten times shorter) kept by name with its readings, (2) to (10): the rise from the seed, the deceleration, the fifth act's fires at the top, the fall, the light's velocity reversed bit for bit at every turned Node, the clicks kept one way through the run back, the detector writing nothing the board reads, the instrument's clicks at the derived cadence 15 and the two instruments' clicks by stage. The former file's own numbers (2026-10-23, six bodies, two instruments, 1,500 intervals) stand in examples/events/universe24/notes.md as the declared seed's reading."""

import copy
import json
from pathlib import Path
from typing import Any

import pytest

from event_universe import world_files
from event_universe.lattice import Lattice
from event_universe.world_files import input_digest, load_world
from tests.laws_universe import (
    CUBE,
    ERAS,
    GAMMA,
    LOG,
    UNIVERSE,
    WORLD,
    flat,
)


def test_the_fold_accepts_the_bare_world_and_refuses_a_former_key() -> None:
    """(1) The one world's file is the universe, the shape and the run's length alone and parses with no mode file, its seed the light family and no body and no reader (the two keys optional since 2026-10-24, required to then; the declared seed's file of 2026-10-23 named six bodies and an empty node_detectors list); the former key `interval` and the held row's former key `booking` refused by name; the same world naming the two keys as empty lists declares an empty board and is not seeded (the former path, every former test world bit for bit)."""
    world = json.loads(WORLD.read_text(encoding="utf-8"))
    universe = json.loads(UNIVERSE.read_text(encoding="utf-8"))
    files = {world["universe"]: universe}
    from event_universe.loader.world import parse_world

    assert (
        set(world) == {"universe", "shape", "intervals"} and not WORLD.with_suffix(".mode.json").exists()
    )
    parsed = parse_world(world, files, input_digest(world))  # (1) the bare world, accepted
    assert parsed.families[parsed.seed].name == "light"
    emptied = {**world, "bodies": []}  # the declared bodies, a key refused since 2026-10-24
    with pytest.raises(ValueError, match="unknown key 'bodies'"):
        parse_world(emptied, files, input_digest(emptied))
    former = copy.deepcopy(world)
    former["interval"] = "unobservable"
    with pytest.raises(ValueError, match="unknown key 'interval'"):
        parse_world(former, files, input_digest(former))
    held = copy.deepcopy(universe)
    held["families"][0]["held"] = {
        "booking": "form"
    }  # the gone declaration, refused by name before any key of it
    with pytest.raises(ValueError, match="holds the key 'held', a declaration no file carries"):
        parse_world(world, {**files, world["universe"]: held}, input_digest(world))


def test_the_shipped_eras_log_opens_with_the_shipped_worlds_own_readings() -> None:
    shipped = [json.loads(line) for line in LOG.read_text(encoding="utf-8").splitlines()[1:9]]
    board = Lattice(load_world(WORLD))
    board.output = lambda line: None
    lines: list[dict[str, Any]] = []
    for expected in shipped:
        kept = ERAS.kept_lines(board)
        board.step()
        line = ERAS.interval_line(board, kept, 0.0)
        ERAS.volume_residuals(lines[-1] if lines else None, line)
        lines.append(line)
        found, stamped = dict(line), dict(expected)
        found.pop("seconds"), stamped.pop("seconds")
        assert json.loads(json.dumps(found)) == stamped, line[
            "interval"
        ]  # (6) the log is the world's own


def test_the_bare_torus_is_seeded_with_light_bangs_and_births_the_pairs_at_the_first_meeting(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """(11) The folded sentences on the small bare torus, the 3-cube with the one world's universe at nature's den and nothing declared (ALGEBRA.md, The uniform seed is a lay; The board reads itself; 2026-10-24): the seed is light at one quantum on every Node, the level now the drift 189 (189^2 <= 36,000 < 190^2) and the level before 0, 27 quanta on the board and 27 in the books; the bang from the seed, X rising from Gamma at every Node alike while no birth has parted them; the first meeting, where the light's share reads two whole quanta at a Node, births the proton pair there at the senses -1 and 1 (the heaviest pair within the two quanta's own energy, the law's sentence of 2026-10-24: two whole quanta of light at the top's unit W_c carry at least 2 W_c, the proton pair's walls 1.99175 W_c; the former clause, the lightest within the top's threshold, birthed the electron pair here, 2026-10-23 to 2026-10-24) with the click's line naming the Node's x-major index, every Node alike birthing at once (27 pairs), each paying by the hole at its own Node (everything local, the owner's word of 04:2x UTC), the light's levels then 0 at every Node and its count read 0, the proton's 54; the former cap by the books' count (13 pairs in the lattice's order, the light's count 1) was the one non-local act, removed the same day."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    (tmp_path / "u.json").write_text(UNIVERSE.read_text(encoding="utf-8"), encoding="utf-8")
    bare = {"universe": "u.json", "shape": [CUBE] * 3, "intervals": 60}
    (path := tmp_path / "bare.json").write_text(json.dumps(bare), encoding="utf-8")
    lines: list[dict[str, Any]] = []
    board = Lattice(load_world(path), output=lines.append)
    names, light = [family.name for family in board.families], board.world.seed
    assert light is not None and names[light] == "light"
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
    assert all(
        b["children"] == births[0]["children"] and sum(b["senses"]) == 0 and "proton" in b["children"]
        for b in births
    )  # one list at every Node, the heaviest within the two quanta's energy at the top of the band, the proton pair among its children, the senses summing to 0 (N children one record each, 2026-10-24)
    credits = [line for line in lines if line.get("event") == "credit"]
    assert sorted(c["node_detector"] for c in credits) == list(range(CUBE**3))  # the Nodes by index
    assert all(c["absorbed"] == "light" and c["realised"] == "proton" for c in credits)
    spent = board.states[light].lines[0]  # the record's line after the holes
    assert flat(spent.now) == [0] * CUBE**3 and flat(spent.before) == [0] * CUBE**3  # the holes
    assert board.credit.counts[light] == 0 and board.credit.counts[names.index("proton")] == 2 * CUBE**3
