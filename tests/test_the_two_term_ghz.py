"""The two-term plane GHZ (the reader's design verdict of 2026-10-20, Part B; ALGEBRA.md, The meeting's identity, the Gram theorem's identity case; The click is the meeting of the future with the past): the Gaussian clause of the write, a side's quarter turn on a plane record, and the record of two terms of planes read at three sides; and first the byte-for-byte test of every real-port world the branch ships, recorded by this test at the eighth commit as pushed (5efd3b4d7), the real path before the Gaussian pairs (the eighth's own tests pin none of them; the reader's run at that commit confirms every one), so that the real path's identity is a test and no claim."""

import json

import numpy as np
import pytest

from event_universe import meeting_back
from event_universe.lattice import Lattice
from event_universe.loader.draw import UNITS, Gauss, norm, ports_of, setting_of, times
from event_universe.world_files import load_world
from tests.laws import TOOL
from tests.laws_spin import (
    IDENTITY,
    SINGLET,
    spin_world,
)


def conj_times(a: Gauss, b: Gauss) -> Gauss:
    """conj(a) b on Gaussian integers, the Hermitian product of two coefficients."""
    return times((a[0], -a[1]), b)


def test_the_quarter_turn_makes_the_hermitian_ports_and_the_loader_refuses_it_by_name(
    tmp_path, monkeypatch
):  # type: ignore[no-untyped-def]
    """The key `turn` (B2 of the reader's design): at the turn 0 the ports are the eighth's integers with 0 behind them; at the turn 3 the identity pattern at the setting [1, 1] reads (1, -i) and (-i, 1), orthogonal in the Hermitian form with equal norms; every quarter turn's ports orthogonal with equal norms on the identity and on a general pattern; the loader refuses by name `turn` without `basis` and a turn outside 0 to 3 (and a turn on a record of real lines at the end of the load, tests/test_the_spin.py), and admits the key on a plane side (the singlet chain's sides at the turn 3 load and run)."""
    identity = tuple(tuple(pair) for pair in IDENTITY)
    plus, minus = ports_of((1, 1), identity)
    assert (plus, minus) == (
        ((1, 0), (1, 0)),
        ((-1, 0), (1, 0)),
    )  # the eighth's (1, 1) and (-1, 1) as pairs
    plus, minus = ports_of((1, 1), identity, 3)
    assert (plus, minus) == (((1, 0), (0, -1)), ((0, -1), (1, 0)))  # (1, -i) and (-i, 1)
    for turn in range(4):
        for setting, pattern in (
            ((1, 1), identity),
            ((3, 5), tuple(tuple(pair) for pair in SINGLET)),
            ((12, 5), identity),
        ):
            plus, minus = ports_of(setting, pattern, turn)
            crossed = (0, 0)
            for a, b in zip(plus, minus, strict=True):
                product = conj_times(a, b)
                crossed = (crossed[0] + product[0], crossed[1] + product[1])
            assert crossed == (0, 0) and sum(map(norm, plus)) == sum(map(norm, minus)), (
                turn,
                setting,
                pattern,
            )
    assert UNITS == ((1, 0), (0, 1), (-1, 0), (0, -1))
    sides = {"left": ((1, 1), IDENTITY), "right": ((1, 1), IDENTITY)}
    path = spin_world(tmp_path / "turned", monkeypatch, sides, both=True, amplitude=64)
    world = json.loads(path.read_text(encoding="utf-8"))
    for turned, text in (
        ({"turn": 3, "basis": None}, "without `basis`"),
        ({"turn": 5}, "from 0 through 3"),
        ({"turn": -1}, "from 0 through 3"),
    ):
        row = {k: v for k, v in {**world["node_detectors"][0], **turned}.items() if v is not None}
        with pytest.raises(ValueError, match=text):  # the loader's reading of the row's setting
            setting_of(row, "node_detectors[0]")
    world["node_detectors"][1]["turn"] = 3
    (good := tmp_path / "turned" / "spin_turned.json").write_text(
        json.dumps(world) + "\n", encoding="utf-8"
    )
    TOOL.main(["--input", str(good)])
    board = Lattice(load_world(good))
    assert board.world.node_detectors[1].turn == 3 and board.credit.sides[1][1] == ports_of(
        (1, 1), identity, 3
    )


def test_the_patterns_gram_is_real_for_every_quarter_turn():
    """The plan's algebra, asserted: for a side's two ports (c, u s) and (-conj(u) s, c) with |u| = 1 the Hermitian sum over the ports, SUM_p conj(e_k(p)) e_m(p), is (p^2 + q^2)(alpha_k alpha_m + beta_k beta_m) for every quarter turn, the azimuth's cross terms cancelling, so `gram_of` reads the pattern alone and stays real (B1's identity case: G = I on the identity pattern, no pattern of another side entering a read)."""
    for turn in range(4):
        for (p, q), pattern in (
            ((1, 1), ((1, 0), (0, 1))),
            ((3, 5), tuple(tuple(pair) for pair in SINGLET)),
            ((12, 5), ((1, 0), (0, 1))),
        ):
            ports = ports_of((p, q), pattern, turn)
            gram = meeting_back.gram_of([pattern], 2)
            for k in range(2):
                for m in range(2):
                    total = (0, 0)
                    for port in ports:
                        product = conj_times(port[k], port[m])
                        total = (total[0] + product[0], total[1] + product[1])
                    assert total == ((p * p + q * q) * gram[k][m], 0), (turn, p, q, k, m)


def test_a_unit_coefficient_turns_a_planes_two_lines_bit_for_bit_and_a_global_unit_writes_nothing(
    tmp_path, monkeypatch
):  # type: ignore[no-untyped-def]
    """The write on planes (B2 iii): a plane part whose port coefficient is the unit i carries the overlap conj(i) = -i, its two lines moved together, re' = im and im' = -re, bit for bit through the one lay act, the other part untouched; a global unit on every surviving part, (i, i), is the identity and writes nothing (`credit.reduced` on pairs); the written coefficients and the scale read the pairs' norms."""
    sides = {"left": ((1, 1), IDENTITY), "right": ((1, 1), IDENTITY)}
    board = Lattice(
        load_world(spin_world(tmp_path / "unit", monkeypatch, sides, both=True, amplitude=64))
    )
    spin = [f.name for f in board.families].index("spin")  # the write at the birth, the lay's interval 0
    before = [np.asarray(line.now).copy() for line in board.states[spin].lines]
    befores = [np.asarray(line.before).copy() for line in board.states[spin].lines]
    meeting_back.realised(board, spin, [(1, 0), (0, 1)])
    lines = board.states[spin].lines
    assert (np.asarray(lines[0].now) == before[0]).all() and (
        np.asarray(lines[1].now) == before[1]
    ).all()
    assert (np.asarray(lines[2].now) == before[3]).all() and (
        np.asarray(lines[3].now) == -before[2]
    ).all()
    assert (np.asarray(lines[2].before) == befores[3]).all() and (
        np.asarray(lines[3].before) == -befores[2]
    ).all()
    assert board.credit.written[spin] == [(1, 0), (0, -1)] and board.credit.scale[spin] == 2
    turned = [np.asarray(line.now).copy() for line in lines]
    meeting_back.realised(board, spin, [(0, 1), (0, 1)])  # a global unit: the identity, nothing written
    assert all(
        (np.asarray(line.now) == was).all()
        for line, was in zip(board.states[spin].lines, turned, strict=True)
    )
    assert board.credit.written[spin] == [(1, 0), (0, -1)] and board.credit.scale[spin] == 2
