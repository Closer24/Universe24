"""Matter's birth from light, N records of the write step, one per child of the list the law selects (ALGEBRA.md, Matter's birth from light, the clause of 2026-10-24 on the owner's word, "the pair is n born, no? several can be born"): two quanta of the massless family meeting at one Node birth the list the law selects as written, the heaviest conjugate pair within their energy (`conversion.birth_of`, `act.born_table`; the selection among longer lists open, `conversion.lists_of` the general enumeration), each child one whole quantum laid on its own record of its family at the list's sense (`act.born_items`, `take.Item.record`, `emission.laid_by_count`), so that each born record carries its Wronskian, two children of opposite sense opposite Wronskians, and the holder of the sign is sourced by every charged child (the defect named: one record carrying both children read W = 0 on 1b670aaf2 and 4568f64af, the holder unsourced; one sense laid with the other the books' deficit on 9fa5ef2b4); the run back exact through the births."""

from __future__ import annotations

import json

import numpy as np

from event_universe import conversion, credit, records, registry, seed, world_files
from event_universe.act import born_items, born_table, click
from event_universe.emission import laid_by_count
from event_universe.features.click import amplitude
from event_universe.lattice import Lattice
from event_universe.lay import laid
from event_universe.loader.circle import lift_points
from event_universe.loader.derived import count_wall
from event_universe.loader.universe import SIGN
from event_universe.world_files import load_world
from tests.laws_universe import SMALL, small_universe, uniform_sea

TOP_UNIVERSE = '{"integers": {"den": 1166991900949580266237, "node_clock": 1000, "quantum_action": 36000}}'  # the top tier's den, 649,421 x 13,586,597 x 132,260,701, three primes 1 mod 4 and 26 points, factored in a blink


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
    assert [item.record for item in items] == [0, 1, 0, 1]
    assert [item.sense for item in items] == [-1, 1, -1, 1]
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
        for r in range(registry.records_of(board.families[charge], board.states[charge].lines))
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
        for r in range(registry.records_of(board.families[charge], board.states[charge].lines))
    ]
    assert rows[0] == 0 and sum(1 for row in rows[1:] if row) == len(children)


def born_here(board, at, table=None):  # type: ignore[no-untyped-def]
    """The birth's own path at one Node of a fresh board, the content 0 everywhere (`meeting_board.closed` without the meeting's read): the seed's record at the Node to the state of a Node with no level through the one lay act, the hole, then the list `table`, the heaviest pair within two light quanta where none is given, laid by the one click act (`act.born_table`, `act.born_items`, `act.click`); returns the children's family."""
    light, here, action = board.world.seed, board.mask((at,)), board.world.quantum_action
    span = records.record_slice(board.families[light], 0)
    for number in range(span.start, span.stop):
        line = board.states[light].lines[number]
        change = (np.where(here, -line.now, 0), np.where(here, -line.before, 0))
        laid(board, light, number, change, None, None, here)
    wall = count_wall(board.families[light], action)
    table = table or born_table(board.families, light, action, 2 * wall, 1)
    click(board, born_items(board.families, table, (at,)))
    return table[0][0]


def test_a_born_child_carries_the_two_light_quantas_energy_and_the_charge_t_div_2(tmp_path, monkeypatch):  # type: ignore[no-untyped-def]
    """The lay of a born child is the law's at every den (ALGEBRA.md, Matter's birth from light, the clause of 2026-10-24 on the owner's ruling): at den 1,021 and at the shipped den a child laid by the birth's own path at one Node of the bare 3-cube carries the share 6 den A^2 with A = isqrt(T div 2), the two light quanta's energy conserved at the birth to the rounding of T div 2 to the largest square, the Wronskian +-A^2, T div 2 to the same rounding, and the charge one per child (`credit.count_of`); in the child's own unit W_rec = 3 T s the pair reads 12 den A^2 over W_rec, E over m c^2, the Lorentz factor of a child born from light of that energy (3 at the point of sine 0.763, 2 at the heaviest point of the shipped den, 5,467,162,541 at its least leg at the PeV tier, 3,677 at the top tier's), the same energy read in two units standing in the points' mass ratio."""
    at, read = (1, 1, 1), {}
    for shipped in (False, True):
        board = bare_board(tmp_path, monkeypatch, 1, [])
        if shipped:  # the top tier's den written in the small universe's place (the PeV den factored by the loader's circle test alone, 2026-10-24)
            (tmp_path / "u.json").write_text(TOP_UNIVERSE, encoding="utf-8")
            board = Lattice(load_world(tmp_path / "bare.json"))
        action, child = board.world.quantum_action, born_here(board, at)
        den, light = board.families[child].pair[1], board.families[board.world.seed]
        size, unit = amplitude(1, action, light.pair, 1), board.credit.units[child]
        assert den == light.pair[1] and size * size <= action // 2 < (size + 1) * (size + 1)
        share = int(board.share_of(child)[0][at])
        assert share == 12 * den * size * size and 2 * count_wall(light, action) - share == 6 * den * (
            action - 2 * size * size
        )
        assert [
            int(np.asarray(records.wronskian(board.lines_of(child, r), True), dtype=object)[at])
            for r in range(2)
        ] == [-size * size, size * size]
        assert credit.count_of(board, child) == board.credit.counts[child] == 2
        read[den] = (int(board.quanta(child)[0][at]), unit)
        assert (
            read[den][0] == (share + unit // 2) // unit == (12 * den * size * size + unit // 2) // unit
        )
    assert (
        read[1021][0] == 3 and read[den][0] == 2
    )  # 2 den over s to the lay's rounding: 2.62 at den 1,021 (the lift (779, 660)) and 2.000 at the top tier (the neutron's lift under the selector, s_n = 0.99766 den; the point nearest the top before it)
    lightest = min(
        (k for k, f in enumerate(board.families) if f.plane),
        key=lambda k: count_wall(board.families[k], action),
    )
    born_here(board, (0, 0, 1), ((lightest, -1), (lightest, 1)))
    quanta, unit = int(board.quanta(lightest)[0][0, 0, 1]), board.credit.units[lightest]
    legs = sorted(
        sine for _vector, _num, sine in lift_points(den)
    )  # the lifts' legs s from the loader, the least first: the units 3 T s stand in the legs' ratio
    assert (
        quanta == (12 * den * size * size + unit // 2) // unit > (legs[-1] // legs[0]) * read[den][0]
    )  # E over m c^2: the heaviest lift's leg over the least, the two children's units' ratio (1838.68 at the top tier), times the heaviest child's quanta
    assert abs(quanta * unit - read[den][0] * read[den][1]) <= read[den][1]  # one energy, two units
