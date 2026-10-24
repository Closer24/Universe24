"""The flux form of Rule3 and the linear sum L (ALGEBRA.md, the flux form; `linear_sum`, `linear_exchange` and `weighted_linear_sum` of tests/laws.py, the tests' own instruments): the one line w a_next + r' = SUM R_ij m_ij + S a_now - w a_before + r, written as w (a_next - 2 a_now + a_before) + r' - r = SUM_j R_ij (m_ij - a_now) - D a_now with D = 2 w - S - SUM_j R_ij, holds at every Node, line, family and interval of the small shipped worlds with the arrivals the step used (the neighbour's number, the fill beyond a face, the face's value where one is presented), checked in one subtraction: the step's total w a_next + r' less w (2 a_now - a_before) + r against the flux and the mass; and the linear sum of a line of light changes only by its exchange through the board's faces and the lays the run reports, so that a level written outside Rule3's line shows as a jump not accounted for."""

import json
import math

import numpy as np

from event_universe import flux, meeting, node, records, world_files
from event_universe.core import paces
from event_universe.core.rule3 import Rule
from event_universe.features.click import presented
from event_universe.lattice import Lattice
from event_universe.plane import NO_FACE
from event_universe.readings import ports
from event_universe.records import record_slice
from event_universe.world_files import load_world
from tests.laws import linear_exchange, linear_sum, universe_beside, weighted_linear_sum
from tests.laws_interval import light_torus, volume_universe


def whole(a):  # type: ignore[no-untyped-def]
    return np.asarray(a, dtype=object)


def faces_of(board: Lattice, index: int):  # type: ignore[no-untyped-def]
    """The faces the step from this interval will present to a family's lines (the interval incremented first)."""
    found = {}
    for face in board.credit.faces.get(board.interval + 1, []):
        if face.family == index:
            found.setdefault(face.line, ([], board.offset))[0].append(face)
    return found


def rules_of(board: Lattice, index: int):  # type: ignore[no-untyped-def]
    """Per record of a family the rule the step uses, (reads, S, w) from the record's read, and its lines' span."""
    family, gamma, unit = board.families[index], board.world.node_clock, board.unit
    for record in range(family.records):
        content, factors = board.read(index, 1, record)
        yield node.rule_of(family, gamma, content, factors, unit), record_slice(family, record)


def step_alone(board: Lattice):  # type: ignore[no-untyped-def]
    """Per family and line the step of the interval alone as the engine takes it (`flux.step_records`), with the rule
    and the arrivals it used; the flux form's two sides for every Node, the left the step's total in one subtraction."""
    gamma, unit, found = board.world.node_clock, board.unit, []
    for index, family in enumerate(board.families):
        faces, cuts = faces_of(board, index), meeting.cut(board, index)
        stepped, _ = flux.step_records(
            index, board.families, board.states, board.wrap, gamma, unit, 1, cuts, faces, board.amplitude
        )
        for (reads, self_coefficient, wall, own), span in rules_of(board, index):
            reads, wall = [whole(r) for r in reads], whole(wall)
            mass = 2 * wall - (sum(reads) + whole(self_coefficient))
            for number in range(span.start, span.stop):
                if (
                    family.held
                    and not family.wronskian
                    and family.axes
                    and 1 <= number % family.width <= 3
                ):
                    continue  # a holder's tension lines step as the shear's momentum (flux.step_momentum), outside the flux form
                line, after = board.states[index].lines[number], stepped[number]
                a, b, r = whole(line.now), whole(line.before), whole(line.remainder)
                fill = (
                    (family.fill or family.rest or 0) if number == 0 else 0
                )  # the rest's volume where the row carries it
                arrivals = tuple(whole(m) for m in ports(a, board.wrap, fill))
                faced = faces.get(number, NO_FACE)
                if faced[0]:
                    arrivals = presented(
                        arrivals,
                        Rule(tuple(reads), whole(self_coefficient), wall, whole(own)),
                        a,
                        b,
                        r,
                        *faced,
                        1,
                    )
                total = wall * whole(after.now) + whole(
                    after.remainder
                )  # the step's total, w a_next + r'
                lhs = total - (wall * (2 * a - b) + r)
                rhs = sum(read * (m - a) for read, m in zip(reads, arrivals, strict=True)) - mass * a
                found.append((family.name, number, lhs - rhs))
    return found


def torus(tmp_path, monkeypatch, output=None):  # type: ignore[no-untyped-def]
    """The 3-cube light torus of tests/laws_interval.py over 3 intervals: matter laid uniform at the band's rest rotation, light's plane wave along x, gravity's held row carrying the volume; the smallest board that carries the flux form at a Node (the three shipped worlds over their intervals, 39 s and 35 s on the suite's clock, left on 2026-10-24)."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    volume_universe(tmp_path)
    return Lattice(load_world(light_torus(tmp_path, "flux", 400, intervals=3)), output)


def test_the_flux_form_holds_at_every_node_line_family_and_interval(tmp_path, monkeypatch):
    """At every interval of the 3-cube light torus the step's total at every Node of every line of every family, w a_next + r' less w (2 a - b) + r, is the flux form's right side, the six Links' R_ij (m_ij - a) less the mass term, with the arrivals the step used (`step_alone`): the flux form of Rule3 holds exactly, with no residual, on every line."""
    board, checked = torus(tmp_path, monkeypatch), 0
    for _ in range(board.world.intervals):
        for family, number, residual in step_alone(board):
            assert not residual.any(), (board.interval, family, number, int(np.abs(residual).max()))
            checked += residual.size
        board.step()
        assert board.ended is None
    stepped = sum(
        1
        for family, state in zip(board.families, board.states, strict=True)
        for number in range(len(state.lines))
        if not (family.held and not family.wronskian and family.axes and 1 <= number % family.width <= 3)
    )
    assert checked == board.world.intervals * 27 * stepped and stepped >= 3


def test_the_linear_sum_of_matter_moves_by_the_mass_term_alone(tmp_path, monkeypatch):
    """On the same torus every line of a family of quanta with num < den (matter, no sign holder) changes its linear sum over an interval by the mass term -SUM_i D_i a_i with D_i = 2 w - S_i - SUM_j R_ij from the step's own coefficients (`linear_exchange` 0 on the wrapped board), exactly, at every interval without a lay or a click of its family."""
    lines: list[dict[str, object]] = []
    board, checked = torus(tmp_path, monkeypatch, lines.append), 0
    gamma, square = board.world.node_clock, board.unit * board.unit
    matter = [
        (index, 6 * family.pair[1] * gamma * gamma * square)
        for index, family in enumerate(board.families)
        if family.pair[0] < family.pair[1] and not family.held
    ]
    assert matter
    for _ in range(board.world.intervals):
        before, predicted = {}, {}
        for index, wall in matter:
            before[index] = [linear_sum(wall, line) for line in board.states[index].lines]
            predicted[index] = []
            for (reads, self_coefficient, w, _mass), span in rules_of(board, index):
                mass = 2 * whole(w) - (sum(whole(r) for r in reads) + whole(self_coefficient))
                for line in board.states[index].lines[span]:
                    predicted[index].append(
                        -int((mass * whole(line.now)).sum()) + linear_exchange(reads, line, board.wrap)
                    )
        begun = len(lines)
        board.step()
        new = lines[begun:]
        for index, wall in matter:
            family = board.families[index].name
            if any(x["family"] == family and x["event"] in ("credit", "lay", "face") for x in new):
                continue
            for number, line in enumerate(board.states[index].lines):
                change = linear_sum(wall, line) - before[index][number]
                assert change == predicted[index][number], (board.interval, family, number)
                checked += 1
    assert checked == board.world.intervals * sum(len(board.states[i].lines) for i, _w in matter)


def test_the_linear_sum_of_light_is_constant_on_a_closed_board(tmp_path, monkeypatch):
    """A board periodic on every axis with one family of light (the rule's universe with its holders dropped and matter's pair made 6000 over 6000), no body, no reader, a pattern laid by hand: L = SUM [w (now - before) + r] is the same whole number after every one of 40 intervals, the Link terms of the flux form pairing off Link by Link and the mass term 0; an exact linear invariant of Rule3 on a closed board at one rate, remainders included."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    universe_beside(tmp_path, drop=("gravity", "charge", "binding"), matter=[6000, 6000])
    world = dict(shape=[7, 7, 7], face_depth=1, intervals=40, node_detectors=[], bodies=[])
    world.update(boundary=dict(x="periodic", y="periodic", z="periodic"), universe="u.json")
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
    world = dict(shape=[60, 1, 1], face_depth=1, intervals=200, node_detectors=[], bodies=[])
    world.update(boundary=dict(x="periodic", y="periodic", z="periodic"), universe="u.json")
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
