"""The phase act reaches one Link (ALGEBRA.md, Only local; The sign holder rotates the two-part record; node.phased): on the bare 3-cube torus of the one universe file the charge holder's time level is kicked at one Node and the phase act taken once on two boards, kicked and unkicked: of every row's phase lines the pairs that differ are, per axis, the two Links touching the Node, its own +a Link and its -a neighbour's (the cosine and the sine line and the count line of that axis), and the Node's own phase row at the Node alone; nothing beyond one Link."""

from pathlib import Path

import numpy as np
import pytest

from event_universe import node, records, world_files
from event_universe.lattice import Lattice
from event_universe.loader.universe import SIGN
from event_universe.world_files import load_world
from tests.laws_universe import CUBE, bare_torus

AT, KICK = (1, 1, 1), 200


def test_the_phase_act_reaches_one_link(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    path = bare_torus(tmp_path, CUBE)
    boards = [Lattice(load_world(path)), Lattice(load_world(path))]
    for board in boards:  # every point standing, its rows of the sign born (2026-10-24, the point rows born at the first birth)
        for index in range(len(board.families)):
            board.born_point(index)
    charge = [family.name for family in boards[0].families].index(SIGN)
    gamma = boards[0].world.node_clock
    free = boards[1].states[charge].lines[0]
    level = np.asarray(free.now, dtype=object).copy()
    level[AT] += KICK
    boards[1].states[charge].lines[0] = records.Record(level, level.copy(), free.remainder)
    plain, kicked = (node.phased(charge, b.families, b.states, 1, gamma) for b in boards)
    touched = 0
    for row, (lines, others) in enumerate(zip(plain, kicked, strict=True)):
        for number, (a, c) in enumerate(zip(lines, others, strict=True)):
            apart = {
                tuple(int(x) for x in found)
                for found in np.argwhere(
                    np.asarray(a.now != c.now, dtype=bool)
                    | np.asarray(a.before != c.before, dtype=bool)
                    | np.asarray(a.remainder != c.remainder, dtype=bool)
                )
            }
            if number == node.PHI:
                expected = {AT}  # the Node's own phase row
            else:  # the axis's cosine and sine lines, then its count line: the two Links touching the Node
                axis = number // 2 if number < 2 * 3 else number - 2 * 3
                neighbour = list(AT)
                neighbour[axis] -= 1
                expected = {AT, tuple(neighbour)}
            assert apart == expected, (row, number, apart)
            touched += 1
    assert touched == sum(len(lines) for lines in plain) > 0
