"""The NodeDetector (ALGEBRA.md, The NodeDetector is one declaration kind for every world; the owner's words of 2026-10-03, a NodeDetector with Nodes alone is never on one Node and a NodeDetector with a record of its own may stand on one; src/event_universe/meeting.py, loader/node_detector_declaration.py, loader/world.py): a record declared a NodeDetector over a connected region, laid in the weights' proportion, its outer Links cut and its inner Links open, absorption and emission at one drawn Node of the region, every click a click line naming the reader and never a Node, the write's Node in the LATTICE lay and face lines beside it."""

import ast
import json
import math
from fractions import Fraction

import numpy as np

from event_universe import board_readings, credit, digits, meeting, node_detector, reports, world_files
from event_universe.core import paces
from event_universe.core.rule3 import division_forward
from event_universe.features.click import amplitude, spread, squared
from event_universe.lattice import Lattice
from event_universe.loader.derived import count_wall
from event_universe.loader.node_detector_declaration import node_detector_of
from event_universe.loader.universe import universe_of
from event_universe.loader.world import bodies_of
from event_universe.world_files import load_world
from tests.laws import (
    BACK,
    PACKET,
    ROOT,
    TOOL,
    TOP,
    booked,
    chain_body_world,
    own_lines,
    refused,
    shares_of,
    slit_world,
)
from tests.laws_content import (
    ION_UNIVERSE,
    ONE_PHOTON,
    TWO_ATOMS,
    ZENO_4,
    ZENO_ATOM,
    content_world,
    ion_world,
    opened,
    with_content,
)
from tests.laws_read import redeclared

TOP_PAIR = (TOP[0], TOP[1])  # the band's top as a resonance, cos Omega = 0


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


def test_a_record_declared_a_reader_over_two_nodes_takes_gives_and_stays(tmp_path, monkeypatch):
    """The reader over a region (ALGEBRA.md, The NodeDetector is one declaration kind for every world; the owner's words of 2026-10-03), restored and re-pinned 2026-10-20 under the content of the born universe (the reader's F3; the worlds it ran, the shelved ion's, the Zeno and the anticoincidence worlds, deleted at the ninth, their declarations inlined in tests.laws_content): the ion's three-part record declared over two adjacent Nodes in equal counts on the ion-like box of 8 by 6 by 5 (`ion_world`: the holders of the content prepended, the box opened along x as the content's sink, the ion's window the drive's passage derived at load, 21; the telegraph's counter dropped, its second close refused by name under the content, tests/test_the_lay.py), the lay A_n^2 = A^2 / n at each, the share credited 1 by the count's rounding (under the content the share read at each Node rounds to one quantum, two over the region, the books' count 1), the loader admitting it and refusing a region in pieces by name, the outer Links cut and the inner Link open (`meeting.cut`), the uniform mode at cos omega_0 = num / den to the bit over one window on the record alone at the content 0 (a periodic box with no holder needs no sink; under the content the record turns at the body's own clock), the absorption's hole at a Node of the region and the emission's lay at one drawn by the record's share at the body's Nodes (`node_detector.drawn_node`, `share_weights`). (i) The loader: the parts' count in two parts, a transition naming no part, a weight of 0 and a rate without the draw are refused by name; the generator lays the drive and no entry for the record. (ii) The lay: the record's share reads 1 at its Nodes in the S lines alone, and its Links cut it stays there (the twin without the draw MATCH over 30 intervals back to the lay). (iii) The clicks under the content: the first click takes the drive's quantum into P at the body's first close, the drive's record standing bit for bit as the twin's (the undepleted beam: a record of several quanta per Node is read in the books and not written, no face and no front, its deficit 1 in the books' line) and its count in the books down by one, the record's P lines carrying the count and the S lines 0, the two boards differing at the region's Nodes alone; every click of the reader is one credit line, the one click line kind (the absorption's and the emission's alike: the reader `body 0`, the family, the part before and after, the count moved and left, the family taken from or given to, the reader's clock and the window; the emission's lines carry the read's bias bound beside, `features/click.bias_bound`, booked where the draw read the board's digits, none on the absorption's certain draw), carrying no Node, the Node written read from the LATTICE lay lines of the write; the null window's re-lays that changed a level leave the same line labelled LATTICE at the count 0. (iv) The acts from outside the Node as lines (the mathematician's 193 and 195 with the advisor's second, two hands): every line a lay changed at the Node writes one LATTICE-labelled `lay` line with its levels and remainder before and after (the absorption's four ion lines, the emission's light line, the null windows'), every face presented writes one `face` line carrying the value the books hold (none in this world: the drive is a beam and the light is never taken); the back-in-time gate (tools/back_in_time.py) reads MATCH over the whole run across the absorptions, the emissions, the null windows and the credit, the lays undone from their lines. (v) The booking identity per act at every step on the ion, the drive and the light (tests/laws.py, `booked`): the share identity within the floors plus the face term at every shell of the light's front, and the lays' change of the share form local to the Node and its six neighbours, exact. (vi) The count-0 record's wave after the click, on the one-photon world's declaration under the content (`ONE_PHOTON` on the two atoms' universe, the click at 63): run with the front and without it over 170 intervals, the read's one outcome alike in both, the taken packet's remnant erased by the front in the one run and standing in the other. (vii) Every function of the engine that assigns a record's lines is Rule3's step, the lay act's one write step or the inverse's crossing, by the engine's own text. The generator's sentences of this test before the ninth (its draws counted per click, the seeds, the anticoincidence world's generator states) left with the generator; the conversion's list through the one act left with the conversion's code (the reader's H2); the Zeno gate's MATCH stands in tests/test_the_meeting.py's dense record."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    path = ion_world(tmp_path, TOOL, intervals=120, counter=False)
    world = json.loads(path.read_text(encoding="utf-8"))
    universe = json.loads((tmp_path / "u.json").read_text(encoding="utf-8"))
    record = world["bodies"][0]
    nodes, parts = record["nodes"], record["parts"]
    at, beside = (
        nodes[0]["node"],
        nodes[1]["node"],
    )  # the region: two Nodes adjacent along x, in equal counts
    twin = {k: v for k, v in world.items() if k != "draw"}
    twin["bodies"] = [{k: v for k, v in record.items() if k in ("family", "nodes", "parts")}]
    (plain := tmp_path / "t.json").write_text(json.dumps(twin), encoding="utf-8")
    TOOL.main(["--input", str(plain)])
    assert json.loads(path.with_suffix(".mode.json").read_text(encoding="utf-8"))["bodies"] == []
    families, names = universe_of(universe)[1], [f["name"] for f in universe["families"]]
    quanta = {
        n: names.index(n) for n in ("ion", "strong_drive", "fluorescence")
    }  # the content's holders first
    own = names.index("ion")
    wrong = {"one part": {**record, "parts": [{**p, "count": 1} for p in parts]}}
    wrong["parts are"] = {**record, "transitions": [{**record["transitions"][0], "to": "X"}]}
    wrong["weight"] = {**record, "transitions": [{**record["transitions"][0], "weight": 0}]}
    wrong["no `node_detector`"] = {k: v for k, v in record.items() if k != "node_detector"}
    edge = {**record["transitions"][0], "resonance": [1, 4]}  # cos Omega below 1 / 3: cos k below -1
    wrong["above the axis band's top"] = {**record, "transitions": [edge]}
    for word, body in wrong.items():
        refused(word, node_detector_of, body, "bodies[0]", families, own, quanta, 1)
    node_detector_of(
        {**record, "transitions": [{**edge, "resonance": [1, 3]}]}, "bodies[0]", families, own, quanta, 1
    )  # 3 num = den: the band's edge, cos k = -1, admitted
    apart = {**record, "nodes": [nodes[0], {"node": [3, 5, 2], "weight": 1}]}  # in pieces
    action = universe["integers"]["quantum_action"]
    counted = {**record, "nodes": [{"node": at, "count": 1}, nodes[1]]}  # a count on a reader's Node
    for word, body in (("in pieces", apart), ("unknown key 'count'", counted)):
        refused(word, bodies_of, [body], None, "", families, (6, 6, 4), 9000, (), action)
    alone = {**twin, "packets": [], "node_detectors": [], "universe": "v.json"}  # the record alone
    alone["boundary"] = {
        axis: "periodic" for axis in "xyz"
    }  # at the content 0: no holder, no sink needed
    alone.pop("face_depth", None)
    (tmp_path / "v.json").write_text(json.dumps(ION_UNIVERSE), encoding="utf-8")
    (rest := tmp_path / "r.json").write_text(json.dumps(alone), encoding="utf-8")
    TOOL.main(["--input", str(rest)])
    quiet, pair = Lattice(load_world(rest)), ION_UNIVERSE["families"][0]["pair"]
    one_node = amplitude(
        1, action, (pair[0], pair[1])
    )  # A = isqrt(A^2), A^2 = T den^2 div (2 (den^2 - num^2))
    spread_to = spread(squared(1, action, (pair[0], pair[1])), (1, 2))  # A_n = isqrt(A^2 div 2)
    assert (pair, one_node, spread_to) == ([1, 1299], 128, 90)  # the ion's pair: A^2 = T div 2 = 16,384
    at_two_three = (amplitude(1, 32768, (2, 3)), spread(squared(1, 32768, (2, 3)), (1, 2)))
    assert at_two_three == (
        148,
        104,
    )  # one quantum of the invariant, A^2 = T / (2 sin omega) = 21,981 at [2, 3]
    assert 2 * 104**2 == 21632 < 21981 == squared(1, 32768, (2, 3))  # the two Nodes' squares under A^2
    there, next_to = tuple(at), tuple(beside)
    levels = [[int(quiet.states[0].lines[0].now[n]) for n in (there, next_to)]]
    assert levels[0] == [spread_to, spread_to]  # the lay over the two Nodes in equal counts
    wall_c = count_wall(quiet.families[0], action)
    laid_share = int(quiet.share_of(0)[0][[there[0], next_to[0]], 3, 2].sum())
    assert (quiet.credit.counts[0], 1000 * laid_share // wall_c) == (
        1,
        977,
    )  # 0.977 W_c over two, credited 1
    cuts = meeting.cut(quiet, 0)
    assert cuts is not None and [int(c.sum()) for c in cuts] == [
        2,
        2,
        4,
        4,
        4,
        4,
    ]  # the boundary's 10 Links
    assert not cuts[0][there] and not cuts[1][next_to]  # the inner Link open from both ends
    assert (
        cuts[1][there] and cuts[0][next_to] and cuts[0][2, 3, 2] and cuts[1][5, 3, 2]
    )  # outer, both ends
    for _ in range(
        18
    ):  # one window: the uniform mode at cos omega_0 = num / den, Chebyshev's recurrence
        quiet.step()
        levels.append([int(quiet.states[0].lines[0].now[n]) for n in (there, next_to)])
    assert all(a == b for a, b in levels)  # the two Nodes alike, the mode uniform
    num, den = pair  # Chebyshev's recurrence of the uniform mode, den (l_(t+1) + l_(t-1)) = 2 num l_t
    residues = [
        den * (levels[t + 1][0] + levels[t - 1][0]) - 2 * num * levels[t][0] for t in range(1, 18)
    ]
    assert (
        max(map(abs, residues)) <= den
    )  # within one level of the division act: cos omega_0 = num / den
    board, other = Lattice(load_world(path), (lines := []).append), Lattice(load_world(plain))
    names = [f.name for f in board.families]
    ion, drv, light = (names.index(n) for n in ("ion", "strong_drive", "fluorescence"))
    region = (there, next_to)
    assert (
        board.credit.counts[ion] == 1 and int(board.quanta(ion)[0].sum()) == 2
    )  # one quantum read at each Node
    assert all(
        int(line.now[tuple(np.add(n, board.offset))]) == 0
        for line in board.states[ion].lines[2:]
        for n in region
    )
    assert BACK.verdict(Lattice(load_world(plain)), 30)["verdict"] == "MATCH"
    node_draws, real_node = [], node_detector.drawn_node  # the write's Node draws

    def noted_node(b, books, weights):  # type: ignore[no-untyped-def]
        found = real_node(b, books, weights)
        node_draws.append((board.interval, list(weights), found))
        return found

    monkeypatch.setattr(node_detector, "drawn_node", noted_node)
    while not (clicks := [x for x in lines if x["event"] == "credit" and x["label"] == "NODEDETECTOR"]):
        booked(board, monkeypatch, ion, drv, light), other.step()  # the booking identity at every act
    reader = board.credit.bodies[
        0
    ]  # the turn's read: the drive projected on the reader's normalised mode
    read = [int(other.states[drv].lines[0].now[tuple(np.add(n, board.offset))]) for n in region]
    total = sum(d * a for d, a in zip(read, reader.amplitudes, strict=True))
    assert (list(reader.amplitudes), reader.norm) == ([90, 90], 127)  # A_i = 90, A = isqrt(2 x 90^2)
    assert node_detector.arriving(other, reader, drv) == (1 if total >= 0 else -1) * (
        (abs(total) + 63) // 127
    )
    first, click = clicks[0], ("P", "S", "strong_drive", None, 1, "body 0")
    words = ("realised", "before", "absorbed", "emitted", "count", "node_detector")
    assert (
        tuple(first[k] for k in words) == click
        and first["interval"] == board.interval == reader.declared.draw.window
    )  # the first click at the first close of the reader's window, derived at load as the drive's passage over its two Nodes (21 here under the swap reading the gapped time line alone, 2026-10-23; 42 read before it, when the swap still fired on this massless board at the body's neighbours; the declared window was 21 before the derivation)
    assert "node" not in first and first["left"] == board.credit.counts[drv]  # the click names no Node
    assert (
        set(first) - {"bias_bound"}
        == set(
            credits_keys
            := "event label interval family node_detector window proper windows before realised kept count left absorbed emitted momentum fan lost source recoil".split()
        )
    )  # at the derived window the reader's click is a read's first draw and carries its bound (2026-10-23)
    assert len(node_draws) == 1 and tuple(node_draws[0][2]) in region  # the hole's one drawn Node
    assert not any(
        f.family == drv for f in board.credit.faces.get(board.interval + 1, [])
    )  # dense: no face
    written = {
        tuple(x["node"]["at"]) for x in lines if x["event"] == "lay" and x["interval"] == board.interval
    }
    assert written == set(region)  # the LATTICE lay lines of the write name the Nodes, the click none
    was, now = (dict(p for f in BACK.snapshot(b) for p in f) for b in (other, board))
    written_at = {tuple(np.add(n, board.offset)) for n in region}
    nearby = {
        tuple(np.add(n, step))
        for n in written_at
        for step in np.vstack((np.eye(3, dtype=int), -np.eye(3, dtype=int)))
    }
    differing = {tuple(map(int, w)) for k in was for w in np.argwhere(was[k] != now[k])}
    assert written_at <= differing <= written_at | nearby, (
        differing - written_at
    )  # the one Node's write: the written Nodes differ, and nothing beyond one Link of them, where a held row's time line reads the written levels (the region and its six neighbours alike to 2026-10-23, when the swap still fired on this massless board at the body's neighbours; the written Nodes alone under the swap reading the gapped time line alone; the region alone before the one Node)
    here = tuple(np.add(node_draws[0][2], board.offset))
    assert board.credit.counts[drv] == other.credit.counts[drv] - 1
    in_s, in_p = (
        any(
            int(x.now[tuple(np.add(n, board.offset))])
            for x in board.states[ion].lines[k : k + 2]
            for n in region
        )
        for k in (0, 2)
    )
    assert board.credit.counts[ion] == 1 and in_p and not in_s
    p_re, p_im = (int(now[f"ion.lines[{k}].now"][here]) for k in (2, 3))  # the part entered, after
    size = spread(squared(1, board.world.quantum_action, board.families[ion].pair), (1, 2))  # P over two
    assert abs(p_re * p_re + p_im * p_im - size * size) <= 2 * size and (p_re, p_im) != (size, 0)
    assert int(now["ion.lines[2].remainder"][here]) == board.half_wall(
        ion
    )  # the taker at the lay's origin
    [booked(board, monkeypatch, ion, drv, light) for _ in (0, 1)]  # two more acts, nothing on the drive
    other.step(), other.step()
    for key in ("now", "before", "remainder"):  # the undepleted beam: the drive the twin's bit for bit
        assert np.array_equal(
            getattr(board.states[drv].lines[0], key), getattr(other.states[drv].lines[0], key)
        )
    assert board.credit.deficits[drv] == 1 and board.books()[names[drv]]["deficit"] == 1
    still = Lattice(load_world(path))  # the same run without the front: its fronts dropped each step
    [still.step() for _ in range(still.interval, board.interval)]
    for _ in range(board.interval, 120):
        booked(board, monkeypatch, ion, drv, light), still.step(), still.credit.fronts.clear()
        for found in board.credit.fronts:  # the theorem: nothing differs beyond the ball
            index, origin, since = found.family, found.origin, found.since
            gap = np.abs(np.indices(board.shape) - np.reshape(origin, (3, 1, 1, 1)))
            far = (
                np.minimum(gap, np.reshape(board.shape, (3, 1, 1, 1)) - gap).sum(0)
                > board.interval - since
            )
            for a, b in zip(board.states[index].lines, still.states[index].lines, strict=True):
                assert (a.now[far] == b.now[far]).all() and (a.before[far] == b.before[far]).all()
    given = [line for line in lines if line["event"] == "credit" and line["emitted"]]
    nulls = [line for line in lines if line["event"] == "credit" and line["label"] == "LATTICE"]
    assert all(n["realised"] == n["before"] and n["count"] == 0 and "node" not in n for n in nulls)
    assert all(  # the one line kind, with the read's bias bound where the draw read the board's digits
        set(g) - {"bias_bound"} == set(credits_keys) and "bias_bound" in g for g in given
    ), [sorted(set(g) ^ set(credits_keys)) for g in given]
    assert all("node" not in g and g["node_detector"] == "body 0" for g in given)
    gave_at = {
        tuple(x["node"]["at"])
        for x in lines
        if x["event"] == "lay"
        and given
        and x["interval"] == given[0]["interval"]
        and x["family"] == "fluorescence"
    }
    assert len(gave_at) == len(given[:1]) and gave_at <= set(
        region
    )  # the emission's quantum laid at one Node
    erased = [line for line in lines if line["event"] == "erasure"]
    print(f"the ion's emissions by {board.interval}: {[(g['interval'], g['before']) for g in given]}")
    assert all(g["before"] == "P" for g in given) and board.credit.counts[light] == len(given)
    stands_in_p = any(
        int(x.now[tuple(np.add(n, board.offset))]) for x in board.states[ion].lines[2:4] for n in region
    )
    assert given or stands_in_p  # the read's realisation: the ion gives within the run, or stands in P
    assert erased == []  # no region declared: nothing credits the light, no front begins
    lays, faces = [x for x in lines if x["event"] == "lay"], [x for x in lines if x["event"] == "face"]
    kinds = {
        t: {(x["family"], x["line"]) for x in lays if x["interval"] == t}
        for t in {x["interval"] for x in lays}
    }
    assert kinds[first["interval"]] == {
        ("ion", k) for k in range(4)
    }  # the absorption: two parts, four lines
    assert all(
        ("fluorescence", 0) in kinds[g["interval"]] for g in given
    )  # every emission laid its quantum
    assert {x["label"] for x in lays} == {"LATTICE"} and board.credit.counts[light] == len(given)
    key, kept = ("line", "ports", "interval", "value"), sum(board.credit.faces.values(), [])
    faced = {(f.family, f.at, *(getattr(f, k) for k in key)) for f in kept}
    logged = {
        (
            names.index(x["family"]),
            tuple(x["node"]["at"]),
            *(tuple(x[k]) if k == "ports" else x[k] for k in key),
        )
        for x in faces
    }
    assert logged == {f for f in faced if f[4] <= board.interval} == set()  # no face: the drive a beam
    assert BACK.verdict(Lattice(load_world(path)), 120)["verdict"] == "MATCH"  # every act crossed
    photon = content_world(tmp_path / "photon", "one_photon", ONE_PHOTON, TWO_ATOMS)
    runs = []  # the count-0 record's wave after the click: erased by the front, or standing without it
    for front in (True, False):
        b = Lattice(load_world(photon), (sl := []).append)
        [(b.step(), front or b.credit.fronts.clear()) for _ in range(170)]
        ph, b_at = [f.name for f in b.families].index("photon"), [90, 0, 0]  # the taken packet's remnant
        absorbed = [
            (x["interval"], x["node_detector"]) for x in sl if x["event"] == "credit" and x["absorbed"]
        ]
        level = int(b.states[ph].lines[0].now[tuple(np.add(b_at, b.offset))])
        runs.append((absorbed, b.credit.counts[ph], level))
    assert (
        runs[0][:2] == runs[1][:2] and [t for t, _body in runs[0][0]] == [60]
    )  # the read's one outcome at the derived window's close 60 (63 at the declared window before 2026-10-23)
    assert (
        runs[0][1] == 0 and runs[0][2] == 0 != runs[1][2]
    )  # the count-0 wave erased by the front or standing
    writers = set()  # every function of the engine that assigns a record's lines
    for module in (ROOT / "src" / "event_universe").rglob("*.py"):
        for f in ast.walk(ast.parse(module.read_text(encoding="utf-8"))):
            for n in (n for n in ast.walk(f) if isinstance(n, (ast.Assign, ast.AugAssign))):
                targets = n.targets if isinstance(n, ast.Assign) else [n.target]
                if isinstance(f, ast.FunctionDef) and any(".lines" in ast.unparse(t) for t in targets):
                    writers.add((module.stem, f.name))
    rule3 = {("lattice", "step"), ("lattice", "step_inverse"), ("lattice", "held_write")}
    rule3 |= {
        ("shear", "written"),
        ("shear", "stepped"),
        ("swap", "swapped"),
    }  # the one Node's own acts on the lines: the tension lines' split write and step (the shear's momentum) and the swap at the top (2026-10-23)
    lay = {("lattice", "start"), ("bookings", "booked_sources"), ("growth", "resized")}
    lay |= {("lay", "written")}  # the one lay act's write step, every door's (ALGEBRA.md, the principle)
    lay |= {("meeting_back", "crossed")}  # the lay act's lines crossed back and forward by the run back
    lay |= {
        ("cone", "written_back")
    }  # the cone stepped alone: the ball's results written back after Rule3's step
    assert writers == rule3 | lay  # nothing writes a NodeState but Rule3, the lay and the face


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
