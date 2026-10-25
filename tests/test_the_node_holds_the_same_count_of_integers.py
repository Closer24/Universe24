"""The generic Node's integers (ALGEBRA.md, The Node; the owner's three constants of 2026-10-25: a Node always holds the same count of integers, always does the same acts, every integer within 128 bits in the state and in every transient, and no den of nature), the gate of the generic Node plan's stage 0: read from the lattice's arrays by tools/node_integers.py loaded by its path and derived from the loader's rows on the bare 3-cube at den 1,021 and at the top tier's den of 26 points, never the shipped file (37 s to factor its den); every Node holds the same count, 35 before the first birth; the two deviations kept by name, the count growing at a birth by 52 per record born and the shipped den's half wall 6 den Gamma^2 G^2 div 2 above 128 bits."""

import json
from dataclasses import fields

import numpy as np
import pytest

from event_universe import registry, world_files
from event_universe.core.ports import AXES, LINK_UNIT
from event_universe.core.rule3 import division_forward, wall_of
from event_universe.lattice import Lattice
from event_universe.records import Record
from event_universe.world_files import load_world
from tests.laws import ROOT, load_file
from tests.laws_universe import GAMMA, SMALL, UNIVERSE

TOOL = load_file("node_integers", ROOT / "tools" / "node_integers.py")
LEVELS = len(
    fields(Record)
)  # a line's integers at a Node: the level now, the level before, the remainder
BITS = 128  # the width the owner's principle names, the one number this test carries
TOP_DEN = 1166991900949580266237  # the top tier's den, three primes 1 mod 4, 26 points, three lifts, factored in a blink
SHIPPED_DEN = json.loads(UNIVERSE.read_text(encoding="utf-8"))["integers"]["den"]  # read, never typed


def bare_board(tmp_path, monkeypatch, den, intervals):  # type: ignore[no-untyped-def]
    """The tests' small universe at `den` on the bare 3-cube torus for `intervals`, the births kept in `born_at`."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    universe = {"integers": {**SMALL["integers"], "den": den}}
    (tmp_path / "u.json").write_text(json.dumps(universe), encoding="utf-8")
    world = {"universe": "u.json", "shape": [3, 3, 3], "intervals": intervals}
    (tmp_path / "bare.json").write_text(json.dumps(world), encoding="utf-8")
    return Lattice(load_world(tmp_path / "bare.json"))


def at_the_start(board):  # type: ignore[no-untyped-def]
    """The count from the rows: per family the lines its state is born with (the loader's; the free row alone for the holder of the sign; none for a point, `registry.start_records`) times a line's three, plus one write remainder per held line."""
    found = 0
    for index, family in enumerate(board.families):
        rows = registry.start_records(board.families, index)
        lines = family.lines if rows is None else rows * family.parts * family.width
        found += LEVELS * lines + (lines if family.held else 0)
    return found


def per_point(board, index):  # type: ignore[no-untyped-def]
    """The growth per point born, from the rows: its records' lines times three, and per record one row of the sign, its lines times three with one write remainder each and the phase row's lines (a pair per axis, a count per axis, the Node's phase row) times three."""
    family = board.families[index]
    sign = board.families[next(r.family for r in family.reads if board.families[r.family].wronskian)]
    row = LEVELS * sign.width + sign.width + LEVELS * (2 * AXES + AXES + 1)
    return family.records * (LEVELS * family.parts * family.width + row)


@pytest.mark.parametrize(("den", "intervals"), [(SMALL["integers"]["den"], 4), (TOP_DEN, 8)])
def test_every_node_holds_the_same_count_of_integers_and_the_count_grows_by_a_point_at_a_birth(
    tmp_path, monkeypatch, den, intervals
):  # type: ignore[no-untyped-def]
    """Before the first birth the tool reads the rows' count at every Node (16 of the volume holder, 16 of the sign holder's free row, 3 of the massless family, 0 of every point: 35, derived and not typed), every array of the board's shape and every line's remainder born at the half wall; at the first birth, the interval 4 at both dens, the count grows by the point's records times 52 each (6 of a record's two lines, 46 of its row of the sign), every array still of the board's shape, the deviation kept by name; at the top tier's den the three lifts are born by the interval 8, the count the start's plus the three points'; the largest bit length of any state integer stands within 128 at both dens, where the shipped den's half wall 6 den Gamma^2 G^2 div 2 alone stands above 128 bits, the second deviation kept by name."""
    board = bare_board(tmp_path, monkeypatch, den, intervals)
    start = TOOL.line_of(board)
    assert start["same_at_every_node"] and TOOL.same_shape(board)
    assert start["integers"] == TOOL.total_of(board) == at_the_start(board)
    assert {np.asarray(a).shape for _label, a in TOOL.arrays_of(board)} == {tuple(board.shape)}
    half = int(division_forward(wall_of(den, GAMMA, LINK_UNIT), 2, 0)[0])
    for index in board.order:
        assert all(
            np.array_equal(line.remainder, np.full(board.shape, half, dtype=object))
            for line in board.states[index].lines
        )
    while not board.born_at:
        board.step()
    born = board.born_at[board.interval]
    after = TOOL.line_of(board)
    assert board.interval == 4 and len(born) == 1 and after["same_at_every_node"]
    assert after["integers"] == start["integers"] + per_point(board, born[0])
    for _ in range(intervals - board.interval):
        board.step()
    points = [index for at in sorted(board.born_at) for index in board.born_at[at]]
    assert len(points) == (1 if den == SMALL["integers"]["den"] else 3)
    assert TOOL.total_of(board) == start["integers"] + sum(per_point(board, index) for index in points)
    assert TOOL.same_shape(board)
    assert start["largest_bit_length"] <= after["largest_bit_length"] <= BITS
    assert TOOL.largest_bits(board)[0] <= BITS
    shipped = int(division_forward(wall_of(SHIPPED_DEN, GAMMA, LINK_UNIT), 2, 0)[0])
    assert shipped.bit_length() > BITS >= half.bit_length()
    print(
        json.dumps(
            {
                "den": den,
                "start": start["integers"],
                "after": after["integers"],
                "end": TOOL.line_of(board),
            }
        )
    )
