"""Matter's birth from light, N records of the write step, one per child of the list the law selects (ALGEBRA.md, Matter's birth from light, the clause of 2026-10-24 on the owner's word, "the pair is n born, no? several can be born"): two quanta of the massless family meeting at one Node birth the list the law selects as written, the heaviest conjugate pair within their energy (`conversion.birth_of`, `act.born_table`; the selection among longer lists open, `conversion.lists_of` the general enumeration), each child one whole quantum laid on its own record of its family at the list's sense (`act.born_items`, `take.Item.record`, `emission.laid_by_count`), so that each born record carries its Wronskian, two children of opposite sense opposite Wronskians, and the holder of the sign is sourced by every charged child (the defect named: one record carrying both children read W = 0 on 1b670aaf2 and 4568f64af, the holder unsourced; one sense laid with the other the books' deficit on 9fa5ef2b4); the run back exact through the births."""

from __future__ import annotations

import importlib.util
import json

import numpy as np

from event_universe import conversion, records, seed, world_files
from event_universe.act import born_items
from event_universe.emission import laid_by_count
from event_universe.features.click import amplitude
from event_universe.lattice import Lattice
from event_universe.lay import laid
from event_universe.loader.circle import lift_points
from event_universe.loader.universe import SIGN
from event_universe.world_files import load_world
from tests.laws import ROOT
from tests.laws_universe import SMALL, small_universe, uniform_sea


def bare_board(tmp_path, monkeypatch, intervals, births, den=None):  # type: ignore[no-untyped-def]
    """The tests' small universe on the bare 3-cube torus (den 1,021, its two points, one the lift; 2026-10-24, the family-less file), the births kept; `den` another den in its place (1,105 = 5 x 13 x 17, three lifts)."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    small_universe(tmp_path)
    if den is not None:
        (tmp_path / "u.json").write_text(
            json.dumps({"integers": {**SMALL["integers"], "den": den}}), "utf-8"
        )
    world = {"universe": "u.json", "shape": [3, 3, 3], "intervals": intervals}
    (tmp_path / "bare.json").write_text(json.dumps(world), encoding="utf-8")
    keep = lambda line: births.append(line) if line.get("event") == "birth" else None  # noqa: E731
    return Lattice(load_world(tmp_path / "bare.json"), output=keep)


def test_the_lists_two_light_quanta_make_are_the_conjugate_pairs_and_the_general_enumeration_a_function(
    tmp_path, monkeypatch
):  # type: ignore[no-untyped-def]
    """The law as written selects among the conjugate pairs of the lifts, one plane family at the senses -1 and 1 (L188; the selector, 2026-10-24, 13:xx UTC): `birth_of` gives exactly those, each exact (the children's points at their senses multiply to the identity) and kept (the senses' sum 0), lightest first by their summed walls, at den 1,021 the one lift point 2 (779, 660) and not its swap point -2 (the former list, every plane, kept by name); the general enumeration `lists_of` is a function with the caller's bound and enters no birth: at the bound 4 on this file every multiset of conjugate pairs of at most four children over every plane, five lists, the lift's pair among them."""
    board = bare_board(tmp_path, monkeypatch, 1, [])
    families, light = board.families, board.world.seed
    planes = [k for k, f in enumerate(families) if f.plane and conversion.gaussian(f.pair)]
    pairs = conversion.birth_of(families, light)
    lifts = {num for _vector, num, _sine in lift_points(families[light].pair[1])}
    assert (
        pairs == [((k, -1), (k, 1)) for k in planes if families[k].pair[0] in lifts] and len(pairs) == 1
    )
    assert all(conversion.conjugate_exact(families, table) for table in pairs) and len(planes) == 2
    general = conversion.lists_of(families, 2, 4)
    assert len(general) >= len(planes) and all(table in general for table in pairs)
    assert all(
        conversion.conjugate_exact(families, table) and sum(s for _o, s in table) == 0
        for table in general
    )
    assert max(len(table) for table in general) == 4 and len(conversion.lists_of(families, 2, 2)) == 2


def test_a_list_of_four_children_lays_four_records_through_the_same_path(tmp_path, monkeypatch):  # type: ignore[no-untyped-def]
    """A list of any length lays its children one record each (`act.born_items`, `emission.laid_by_count`): a four-child list, the proton pair with the electron pair, handed to the path at one Node lays two records of each family, each born record's Wronskian its child's sense, and after one interval the holder of the sign's four reader rows are written and no other (at den 1,105, three lifts with two records each, the 23 other points one, since the selector of 2026-10-24, 13:xx UTC; den 1,021 has one lift)."""
    board = bare_board(tmp_path, monkeypatch, 2, [], 1105)
    names = [f.name for f in board.families]
    _neutron, proton, electron = sorted(
        (k for k, f in enumerate(board.families) if f.records == 2),
        key=lambda k: board.families[k].pair[0],
    )  # the lifts, the heavier first: (425, 1020), (663, 884), (975, 520)
    table = ((proton, -1), (proton, 1), (electron, -1), (electron, 1))
    items = born_items(board.families, table, ((1, 1, 1),))
    assert [item.record for item in items] == [0, 1, 0, 1] and [item.sense for item in items] == [
        -1,
        1,
        -1,
        1,
    ]
    for item in items:
        laid_by_count(board, item)
    for item in items:
        w = np.asarray(records.wronskian(board.lines_of(item.family, item.record), True), dtype=object)
        assert (
            int(w[1, 1, 1]) == item.sense * amplitude(1, board.world.quantum_action, item.pair, 1) ** 2
        )
    board.step()
    charge = names.index(SIGN)
    width = board.families[charge].width
    rows = [
        int(np.abs(np.asarray(board.states[charge].lines[r * width].now, dtype=object)).max())
        for r in range(board.families[charge].records)
    ]
    assert rows[0] == 0 and sum(1 for row in rows[1:] if row) == len(items)  # the four reader rows


def test_the_uniform_cube_births_the_list_one_record_per_child_each_at_its_sense(tmp_path, monkeypatch):  # type: ignore[no-untyped-def]
    """At the first meeting every Node births the one list the law selects, the conjugate pair of the heaviest plane family within the two quanta's energy: the records holding levels number the list's children, each born record's Wronskian carries its child's sense at every Node and equals the opposite child's in size, the books count one quantum per child, and the holder of the sign's row of every charged record is written after the birth."""
    births: list[dict] = []  # type: ignore[type-arg]
    monkeypatch.setattr(
        seed, "uniform_seed", uniform_sea
    )  # the uniform cube, the law's seed to 2026-10-24, by name: the sentence is every Node's alike
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
    charge = names.index(SIGN)
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
