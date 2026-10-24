"""The flux form of Rule3 and the linear sum L (ALGEBRA.md, the flux form; `linear_sum`, `linear_exchange` and `weighted_linear_sum` of tests/laws.py, the tests' own instruments): the one line w a_next + r' = SUM R_ij m_ij + S a_now - w a_before + r, written as w (a_next - 2 a_now + a_before) + r' - r = SUM_j R_ij (m_ij - a_now) - D a_now with D = 2 w - S - SUM_j R_ij, holds at every Node, line, family and interval of the small shipped worlds with the arrivals the step used (the neighbour's number, the fill beyond a face, the face's value where one is presented), checked in one subtraction: the step's total w a_next + r' less w (2 a_now - a_before) + r against the flux and the mass; and the linear sum of a line of light changes only by its exchange through the board's faces and the lays the run reports, so that a level written outside Rule3's line shows as a jump not accounted for."""

import json
import math

import numpy as np

from event_universe import flux, node, records, world_files
from event_universe.core import paces
from event_universe.lattice import Lattice
from event_universe.readings import ports
from event_universe.world_files import load_world
from tests.laws import linear_sum, universe_beside, weighted_linear_sum


def whole(a):  # type: ignore[no-untyped-def]
    return np.asarray(a, dtype=object)


def test_the_linear_sum_of_light_is_constant_on_a_closed_board(tmp_path, monkeypatch):
    """A board periodic on every axis with one family of light (the rule's universe with its holders dropped and matter's pair made 6000 over 6000), no body, no reader, a pattern laid by hand: L = SUM [w (now - before) + r] is the same whole number after every one of 40 intervals, the Link terms of the flux form pairing off Link by Link and the mass term 0; an exact linear invariant of Rule3 on a closed board at one rate, remainders included."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    universe_beside(tmp_path, drop=("gravity", "charge", "binding"), matter=[6000, 6000])
    world = dict(shape=[7, 7, 7], intervals=40, bodies=[], universe="u.json")
    (path := tmp_path / "closed.json").write_text(json.dumps(world), encoding="utf-8")
    board = Lattice(load_world(path))
    now = records.zeros(board.shape, board.kind)
    now[3, 3, 3], now[2, 3, 3], now[4, 3, 3], now[3, 2, 3] = 1000, 500, 500, -300
    board.states[0].lines[0] = records.Record(now, now // 2, records.zeros(board.shape, board.kind))
    wall = 6 * board.families[0].pair[1] * board.world.node_clock**2 * board.unit**2
    first = linear_sum(wall, board.states[0].lines[0])
    for _ in range(40):
        board.step()
        assert linear_sum(wall, board.states[0].lines[0]) == first, board.interval
    assert (
        first == wall * 850 and board.states[0].lines[0].remainder.any()
    )  # the lay's w SUM (now - before); the remainders moved


def test_the_rate_weighted_linear_sum_of_light_is_constant_at_a_fixed_content(tmp_path, monkeypatch):
    """The smallest hand-laid well: a ring of 60 Nodes with one family of light (the rule's universe with its holders dropped and matter's pair made 6000 over 6000, Gamma 6,000), the content 0 on the Nodes 0 to 39 and 600 on 40 to 59, laid by hand and never stepped (the paces 6,000 and 4,912; the scale lcm(6000^2, 4912^2) = 3,392,964,000,000, the weights 94,249 and 140,625), one pulse of height 10^6 and 16 Nodes crest to crest laid on the empty side, 200 intervals by the engine's own `flux.step_line` with the rule `node.rule_of` gives at that content: L'' = SUM weight_i [w (now - before) + r] is the same whole number after every interval, while L moves by the pairing term SUM over the Links of (R_ij - R_ji)(a_j - a_i), nonzero only while the pulse straddles the two Links between the paces."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    universe_beside(tmp_path, drop=("gravity", "charge", "binding"), matter=[6000, 6000])
    world = dict(shape=[60, 1, 1], intervals=200, bodies=[], universe="u.json")
    (path := tmp_path / "ring.json").write_text(json.dumps(world), encoding="utf-8")
    board = Lattice(load_world(path))
    family, gamma, unit = board.families[0], board.world.node_clock, board.unit
    content = np.zeros(board.shape, dtype=object)
    content[40:, 0, 0] = 600
    rule = node.rule_of(family, gamma, content, None, unit)
    reads = [whole(r) for r in rule[0]]
    squared = np.asarray(paces.node_paces(gamma, content)[1], dtype=object) ** 2
    scale = math.lcm(*{int(v) for v in squared.ravel()})
    weights = np.vectorize(lambda v: scale // int(v), otypes=[object])(squared)
    assert scale == 3_392_964_000_000 and {int(v) for v in weights.ravel()} == {94_249, 140_625}
    now = records.zeros(board.shape, board.kind)
    for k in range(16):  # one wavelength of a cosine, 16 Nodes crest to crest, on the empty side
        now[8 + k, 0, 0] = round(1_000_000 * math.cos(2 * math.pi * k / 16))
    line = records.Record(now, now.copy(), records.zeros(board.shape, board.kind))
    wall = 6 * family.pair[1] * gamma**2 * unit**2
    first, moved = weighted_linear_sum(wall, line, weights), []
    for _ in range(200):
        a = whole(line.now)
        pairing = sum(
            int((read * (whole(m) - a)).sum())
            for read, m in zip(reads, ports(a, board.wrap), strict=True)
        )
        before = linear_sum(wall, line)
        line = flux.step_line(line, rule, board.wrap)
        assert (
            linear_sum(wall, line) - before == pairing
        )  # L moves by the pairing term alone, the mass 0
        moved.append(pairing != 0)
        assert weighted_linear_sum(wall, line, weights) == first
    assert any(moved) and not all(moved)  # L moves only while the pulse straddles the two boundary Links
