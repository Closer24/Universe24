"""Matter's birth from light, N children one record each (ALGEBRA.md, Matter's birth from light, the clause of 2026-10-24 on the owner's word, "the pair is n born, no? several can be born"): two quanta of the massless family meeting at one Node birth the heaviest exact list of children whose summed walls fit within their energy (`conversion.lists_of`, `act.born_table`), each child one whole quantum laid on its own record of its family at the list's sense (`act.born_items`, `take.Item.record`, `emission.laid_by_count`), so that each born record carries its Wronskian, two children of opposite sense opposite Wronskians, and the holder of the sign is sourced by every charged child (the defect named: one record carrying both children read W = 0 on 1b670aaf2 and 4568f64af, the holder unsourced; one sense laid with the other the books' deficit on 9fa5ef2b4); the run back exact through the births."""

from __future__ import annotations

import importlib.util
import json

import numpy as np

from event_universe import conversion, records, world_files
from event_universe.lattice import Lattice
from event_universe.lay import laid
from event_universe.loader.derived import count_wall
from event_universe.world_files import load_world
from tests.laws import ROOT

UNIVERSE = ROOT / "examples" / "events" / "universe24" / "universe_universe24.json"


def bare_board(tmp_path, monkeypatch, intervals, births):  # type: ignore[no-untyped-def]
    """The one universe file on the bare 3-cube torus, the births kept."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    (tmp_path / "u.json").write_text(UNIVERSE.read_text(encoding="utf-8"), encoding="utf-8")
    world = {"universe": "u.json", "shape": [3, 3, 3], "intervals": intervals}
    (tmp_path / "bare.json").write_text(json.dumps(world), encoding="utf-8")
    keep = lambda line: births.append(line) if line.get("event") == "birth" else None  # noqa: E731
    return Lattice(load_world(tmp_path / "bare.json"), output=keep)


def test_the_lists_two_light_quanta_make_are_exact_kept_and_ordered_by_their_walls(
    tmp_path, monkeypatch
):  # type: ignore[no-untyped-def]
    """Every list is exact (the children's points at their senses multiply to the identity), keeps the senses' sum 0, holds at most 2 + BEYOND children, and the lists stand lightest first by their summed walls; the conjugate pair of each plane family is among them."""
    board = bare_board(tmp_path, monkeypatch, 1, [])
    families, light = board.families, board.world.seed
    tables = conversion.birth_of(families, light)
    assert tables and all(conversion.conjugate_exact(families, table) for table in tables)
    assert all(sum(sense for _out, sense in table) == 0 for table in tables)
    assert all(2 <= len(table) <= 2 + conversion.BEYOND for table in tables)
    walls = [sum(count_wall(families[out], 1) for out, _sense in table) for table in tables]
    assert walls == sorted(walls) and len(set(walls)) == len(walls)
    planes = [k for k, f in enumerate(families) if f.plane and conversion.gaussian(f.pair)]
    assert all(((k, -1), (k, 1)) in tables for k in planes)


def test_the_uniform_cube_births_the_list_one_record_per_child_each_at_its_sense(tmp_path, monkeypatch):  # type: ignore[no-untyped-def]
    """At the first meeting every Node births the one list: the records holding levels number the list's children, each born record's Wronskian carries its child's sense at every Node and equals the opposite child's in size, the books count one quantum per child, and the holder of the sign's row of every charged record is written after the birth."""
    births: list[dict] = []  # type: ignore[type-arg]
    board = bare_board(tmp_path, monkeypatch, 40, births)
    names = [f.name for f in board.families]
    while not births:
        board.step()
    assert len(births) == int(np.prod(board.shape))
    children, senses = births[0]["children"], births[0]["senses"]
    assert len(children) >= 2 and sum(senses) == 0
    born = {}
    for name in set(children):
        index = names.index(name)
        standing = [
            r
            for r in range(board.families[index].records)
            if any(np.asarray(line.now, dtype=object).any() for line in board.lines_of(index, r))
        ]
        assert len(standing) == children.count(name)
        assert board.credit.counts[index] == children.count(name) * len(births)
        for record, sense in zip(
            standing, [s for c, s in zip(children, senses, strict=True) if c == name], strict=True
        ):
            w = np.asarray(records.wronskian(board.lines_of(index, record), True), dtype=object)
            assert (np.sign(w.astype(float)) == sense).all()
            born[(name, sense)] = int(w.reshape(-1)[0])
    for (name, sense), w in born.items():
        assert born[(name, -sense)] == -w != 0
    board.step()
    charge = names.index("charge")
    width = board.families[charge].width
    rows = [
        int(np.abs(np.asarray(board.states[charge].lines[r * width].now, dtype=object)).max())
        for r in range(board.families[charge].records)
    ]
    assert rows[0] == 0 and sum(1 for row in rows[1:] if row) == len(children)


def test_the_holes_board_runs_back_exact_through_its_births(tmp_path, monkeypatch):  # type: ignore[no-untyped-def]
    """The sea with a hole, 20 intervals forward through its births and back: MATCH (the lays of N records logged per line, each undone)."""
    spec = importlib.util.spec_from_file_location("back", ROOT / "tools" / "back_in_time.py")
    assert spec is not None and spec.loader is not None
    back = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(back)
    births: list[dict] = []  # type: ignore[type-arg]
    board = bare_board(tmp_path, monkeypatch, 30, births)
    light, here = board.world.seed, board.mask(((0, 0, 0),))
    span = records.record_slice(board.families[light], 0)
    for number in range(span.start, span.stop):
        line = board.states[light].lines[number]
        change = (np.where(here, -line.now, 0), np.where(here, -line.before, 0))
        laid(board, light, number, change, None, None, here)
    found = back.verdict(board, 20)
    assert found["verdict"] == "MATCH" and births, found
