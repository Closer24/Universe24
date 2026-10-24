"""The NodeDetector (ALGEBRA.md, The NodeDetector is one declaration kind for every world; the owner's words of 2026-10-03, a NodeDetector with Nodes alone is never on one Node and a NodeDetector with a record of its own may stand on one; src/event_universe/meeting.py, loader/node_detector_declaration.py, loader/world.py): a record declared a NodeDetector over a connected region, laid in the weights' proportion, its outer Links cut and its inner Links open, absorption and emission at one drawn Node of the region, every click a click line naming the reader and never a Node, the write's Node in the LATTICE lay and face lines beside it."""

import json
import math
from fractions import Fraction

import numpy as np

from event_universe import board_readings, credit, digits, meeting, node_detector, reports, world_files
from event_universe.core import paces
from event_universe.core.rule3 import division_forward
from event_universe.features.click import amplitude, squared
from event_universe.lattice import Lattice
from event_universe.loader.derived import count_wall
from event_universe.world_files import load_world
from tests.laws import (
    PACKET,
    TOOL,
    chain_body_world,
    own_lines,
    refused,
    shares_of,
    slit_world,
)
from tests.laws_content import (
    ZENO_4,
    ZENO_ATOM,
    opened,
    with_content,
)
from tests.laws_read import redeclared


def test_a_count_is_one_quantum_of_the_invariant_in_the_familys_own_wall(tmp_path, monkeypatch):
    """A count is one quantum of the invariant, the form T sin omega_0 of the family's gap (the two hands' word on #1793's R8): the taker's lay carries 2 A^2 sin omega = T per quantum per line to the unit, the family's wall is W_c sin omega_0 by one root on the whole product and 3 den T for a massless family, the [1, 1299] amplitude is unchanged, and the generator lays a body's declared count in that unit (the books' count of a bound body at the lay is the share at the Nodes' paces under its own well, a reading above the declaration on main before this branch, 13 for 6 on the tests' chain, and no part of this change)."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    world = chain_body_world(
        tmp_path, TOOL, 8
    )  # a body of 8: at the declared rest 60 the lay of 7 cycles
    board = Lattice(load_world(world))
    names, action = [family.name for family in board.families], board.world.quantum_action
    matter, light = board.families[names.index("matter")], board.families[names.index("charge")]
    num, den = matter.pair
    gap, laid = den * den - num * num, squared(1, action, matter.pair)
    assert (
        laid == squared(1, action, (2, 3)) == 21981 and action == 32768
    )  # T / (2 sin omega_0) to the unit
    assert (
        action - 2 <= 2 * laid * math.isqrt(gap) // den <= action
    )  # 2 A^2 sin omega = T, two roots' units
    assert (
        squared(1, action, (1, 1299)) == 16384 and amplitude(1, action, (1, 1299)) == 128
    )  # bit for bit
    assert count_wall(light, action) == 3 * 6000 * action  # the bolometer's W_c for a massless family
    assert (
        count_wall(matter, action) == math.isqrt(9 * action**2 * gap) == 439628852
    )  # W_c sin omega_0 to the unit
    laid_body = json.loads(world.with_suffix(".mode.json").read_text(encoding="utf-8"))["bodies"][0]
    assert (
        laid_body["count"] == laid_body["carried"] == 8
    )  # the generator lays the declaration in that unit


def test_the_node_detector_books_the_conserved_forms_own_current_through_its_front(
    tmp_path, monkeypatch
):
    """The credit's booking (ALGEBRA.md #the-click-is-the-meeting; the owner's word of 2026-10-04, 11:54 UTC, the mathematician's derivation with the advisor's second, two hands; since 2026-10-23 the frame's, ALGEBRA.md, The booking is the frame's, the owner's word of that day): a NodeDetector books through each front Port the frame's current J_ij, the plain current num (q_ij / Gamma)^2 (now_i before_j - before_i now_j), the Link's factor squared the one weight, less the step's change of the Link's level term num Q_ij (before_i - before_j)(now_i + now_j) / 2, summed in the unit G^2 and divided once at the close by W_rec G^2. A light packet crosses a declared region of two Nodes on the tests' chain whose front Links carry a tension written into the content holder's x axis line (300 behind the region, 200 and 100 across it at the start: the tension 250 on the Link entered, Q - G^2 = -21, and 50 on the Link left, -4, the line then moving under Rule3); at every step the region's share in the frame's form changes by the booked inflow over G^2 plus Rule3's remainder term within the division act's unit per Node, the derived tolerance, two units here, on the tension's board and on its twin without alike, while the plain inflow misses it by far more on the tension's board; the twin's booked window is read by `quanta_through` as the floor over W_rec G^2 with the remainder below one quantum beside it in the unit G^2 (the floor and the remainder's draw, 2026-10-21; the half-up rounding before). To 2026-10-23 the booked number was the plain current times Q_ij, the twin's the plain current times G^2 exactly, the former reading."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    region, draw = [[13, 0, 0], [14, 0, 0]], {}
    packet = {**PACKET, "top": {"x": [8, 8], "y": [0, 0], "z": [0, 0]}, "edge": {"x": 4, "y": 0, "z": 0}}
    chain = dict(shape=[24, 1, 1], boundary=dict(x="open", y="periodic", z="periodic"), faces=[])
    readers = [{"name": "near", "positions": region}]
    world = slit_world(
        tmp_path, TOOL, "chain", packets=[packet], node_detectors=readers, draw=draw, **chain
    )
    boards = [Lattice(load_world(world)) for _ in (0, 1)]  # the tension's board and its twin without
    names, square = [f.name for f in boards[0].families], boards[0].unit ** 2
    light, gravity = names.index("charge"), names.index("gravity")
    axis = boards[0].states[gravity].lines[1]  # the content holder's x axis line, the tension's read
    for x, level in ((slice(0, 13), 300), (13, 200), (14, 100)):
        axis.now[x], axis.before[x] = level, level
    at, gamma = boards[0].mask(region), boards[0].world.node_clock
    facing = reports.front(at, boards[0].wrap, at, boards[0].declared_board())
    misses, totals = [], [[0, 0], [0, 0]]
    for _interval in range(8):
        for k, b in enumerate(boards):
            read, flow = (
                b.read(light),
                [np.asarray(c, dtype=object) for c in board_readings.currents(b)[light]],
            )
            factors = [np.broadcast_to(np.asarray(q, dtype=object), b.shape) for q in read[1]]
            weighed = [q * c for q, c in zip(factors, flow, strict=True)]
            plain, weighted = (
                int(reports.entering(facing, f).sum(dtype=object)) for f in (flow, weighed)
            )
            fronts = [
                int(q[tuple(n)]) - square
                for q, f in zip(factors, facing, strict=True)
                for n in np.argwhere(f)
            ]
            assert (min(fronts) < 0) == (k == 0) and len(fronts) == 2  # tension on the front Links
            was, lines = (
                sum(map(sum, b.credit.intake.get((light, "near"), {}).values())),
                own_lines(b, light),
            )
            start = int(shares_of(b, light, read, lines)[at].sum())
            squares = np.broadcast_to(np.asarray(paces.link_pace_of(gamma, read[0])) ** 2, b.shape)[at]
            b.step()
            moved, remainder = own_lines(b, light), Fraction(0)
            booked_now = sum(map(sum, b.credit.intake.get((light, "near"), {}).values())) - was
            for a, z in zip(lines, moved, strict=True):  # Rule3's remainder term per Node of the region
                step = (z.now.astype(object) - a.before.astype(object))[at]  # next - before
                carried = (z.remainder.astype(object) - a.remainder.astype(object))[at]  # r' - r
                remainder -= sum(
                    Fraction(int(n), 2 * int(d) * square)
                    for n, d in zip(step * carried, squares, strict=True)
                )
            change = int(shares_of(b, light, read, moved)[at].sum()) - start - remainder
            print(
                f"interval {b.interval}, Q - G^2 on the front Links {fronts}: plain {plain}, plain weighted {weighted} (plain x G^2 {plain * square}), booked {booked_now}, the region's share change less the remainder term {float(change):.3f}, the identity's residual {float(change - Fraction(booked_now, square)):.3f}"
            )
            assert (
                abs(change - Fraction(booked_now, square)) < 2
            )  # one unit per Node: the frame's current
            misses.append((k, abs(change - plain)))
            totals[k][0], totals[k][1] = totals[k][0] + plain, totals[k][1] + booked_now
    assert max(m for k, m in misses if k == 0) > 2
    assert (
        totals[1][1] != totals[1][0] * square
    )  # the twin: the frame's current, not the plain one times G^2
    twin, unit = boards[1], boards[1].credit.units[light]
    booked_count, booked_rest = (int(n) for n in division_forward(totals[1][1], unit * square, 0))
    through, rest, _unit = credit.quanta_through(twin.credit, light, totals[1][1], twin.unit)
    assert (through, rest) == (booked_count, booked_rest) and booked_count > 0


def test_a_reader_with_its_own_record_stands_on_one_node(tmp_path, monkeypatch):
    """The relation seen from its two ends (ALGEBRA.md, The NodeDetector is one declaration kind for every world), restored and re-pinned 2026-10-20 under the content of the born universe (the reader's F3; the Zeno n = 4 world deleted at the ninth, its declaration `ZENO_4` inlined, the box opened along x as the content's sink): the reader declared at one Node alone is admitted by the loader; its lay is the whole amplitude, A_1 = A, and its norm A, so the resonant turn reads the drive's level at the Node exactly, (|d| A + A div 2) div A = |d| (`node_detector.arriving`); its six Links are cut; the record alone rotates in the uniform mode at cos omega_0 = num / den, Chebyshev's recurrence within one level over a window (read at the content 0 on the periodic box, where the record turns at the vacuum's clock); its window is the lay's passage derived at load, 18 over its one Node (21 over the two-Node body; the declared 12, Zeno's n, refused by name on the opened box); at its first close, 18, the click's read of the board carries the draw under the content: what the body reads (its Node and, within one Link, the Nodes where each record it reads stands off the origin, the reader's G2) stands at 246 bits on the eve against the absorption's total of 54 bits, the labels' unit, so the one-Node reader draws, the quantum passing at this close (at the content 0 the same read stood at 50 bits below the total and was refused by name, the run ending there: the case the law named, more Nodes read); a NodeDetector with Nodes alone at one Node is still refused by name, since through one Node what enters leaves and the net current over a passing wave is about 0."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    world = redeclared(json.loads(json.dumps(ZENO_4)))
    world["bodies"][0]["nodes"] = world["bodies"][0]["nodes"][:1]  # the reader at one Node
    at = tuple(world["bodies"][0]["nodes"][0]["node"])
    record = {k: v for k, v in world["bodies"][0].items() if k in ("family", "nodes", "parts")}

    def under_the_content(**changes):  # type: ignore[no-untyped-def]
        found = opened(json.loads(json.dumps(world)))
        found.update(universe="u.json", **changes)
        return found

    files = {"one": under_the_content(), "plain": under_the_content(bodies=[record])}
    files["bare"] = under_the_content(
        bodies=[], node_detectors=[{"name": "bare", "positions": [list(at)]}]
    )
    files["alone"] = {
        **json.loads(json.dumps(world)),
        "bodies": [record],
        "packets": [],
        "universe": "z.json",
    }
    (tmp_path / "u.json").write_text(json.dumps(with_content(ZENO_ATOM)), encoding="utf-8")
    (tmp_path / "z.json").write_text(
        json.dumps(ZENO_ATOM), encoding="utf-8"
    )  # the content 0: the record alone
    paths = {name: tmp_path / f"{name}.json" for name in files}
    for name, content in files.items():
        paths[name].write_text(json.dumps(content), encoding="utf-8")
    bare = paths["bare"]  # a NodeDetector with Nodes alone at one Node: still refused by name
    refused("never one Node", lambda: (TOOL.main(["--input", str(bare)]), load_world(bare)))
    for name in ("one", "plain", "alone"):
        TOOL.main(["--input", str(paths[name])])
    board = Lattice(load_world(paths["one"]), (lines := []).append)
    plain, alone = Lattice(load_world(paths["plain"])), Lattice(load_world(paths["alone"]))
    names = [f.name for f in board.families]
    atom, drv = names.index("atom"), names.index("pulse")
    (num, den), action = board.families[atom].pair, board.world.quantum_action
    here, reader = tuple(np.add(at, board.offset)), board.credit.bodies[0]
    one = amplitude(1, action, (num, den))  # A = isqrt(T den^2 div (2 (den^2 - num^2)))
    assert (list(reader.amplitudes), reader.norm, one) == ([one], one, 128)  # A_1 = A, the whole lay
    assert int(board.states[atom].lines[0].now[here]) == one
    cuts = meeting.cut(board, atom)
    assert cuts is not None and all(int(c.sum()) == 2 and c[here] for c in cuts)  # six Links cut
    quiet_at = tuple(np.add(at, alone.offset))
    quiet = [f.name for f in alone.families].index("atom")
    levels = [int(alone.states[quiet].lines[0].now[quiet_at])]
    for _ in range(12):
        alone.step()
        levels.append(int(alone.states[quiet].lines[0].now[quiet_at]))
    residues = [den * (levels[t + 1] + levels[t - 1]) - 2 * num * levels[t] for t in range(1, 12)]
    assert max(map(abs, residues)) <= den  # the uniform mode at the cut Node, cos omega_0 = num / den
    window = reader.declared.draw.window
    assert window == 18 and not [x for x in lines if x["event"] == "credit"]  # none before the close
    for _ in range(window - 1):
        board.step(), plain.step()
        level = int(plain.states[drv].lines[0].now[here])  # d, the drive's level at the Node
        assert node_detector.arriving(plain, reader, drv) == level  # the turn reads |d| exactly, signed
    reads = digits.reads_of(board, [drv, atom], board.mask(reader.nodes))
    number, _moduli = digits.read_of(board, reads, "the test")  # the eve's
    draws, real_draw = [], node_detector.drawn_from

    def spied(read, weights, label, moduli):  # type: ignore[no-untyped-def]
        draws.append((read, [int(w) for w in weights]))
        return real_draw(read, weights, label, moduli)

    monkeypatch.setattr(node_detector, "drawn_from", spied)
    board.step()  # the close: under the content the one Node's digits carry the draw
    read, total = draws[0][0], sum(draws[0][1])  # the close's own read and the absorption's total
    closes = [
        (x["interval"], x["before"], x["realised"], x["absorbed"])
        for x in lines
        if x["event"] == "credit"
    ]
    print(
        f"the one-Node reader's digits {number.bit_length()} bits, the absorption's total {total.bit_length()}"
    )
    assert read >= total and number >= total and (number.bit_length(), total.bit_length()) == (246, 54)
    assert closes == [
        (18, "g", "g", None)
    ]  # the draw made, the quantum passing at this close (2026-10-20)
