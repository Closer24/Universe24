"""The read, its own folder (ALGEBRA.md #the-paces): the content as it is, no floor, the reads summed at their weights; the axis content rounded at the read; the guard at load on squares (the checkerboard factor at -2) admits and refuses by name, and the read in the interval carries no guard. The write's folder and the hold's (ALGEBRA.md #the-primitives, a family's write is one act; the row "the hold"): (numerator + r) div wall at every Node by Rule3's carried division, the remainder kept at the Node, forward then back exact, over many intervals the written total the numerator's within one unit; a held part gains the same division each interval and loses it back; the refusals by name. The start, its own folder (ALGEBRA.md #the-generator (g), the start): a held family's rest is the division act iterated from nothing until the levels repeat, 6 den b = num S_6(b) + 3 den sigma at the fine unit from the width, the levels its nearest integers; the refusals by name."""

import json

import numpy as np
import pytest
from scipy.sparse import diags, kronsum
from scipy.sparse.linalg import spsolve

from event_universe import node
from event_universe.core import paces
from event_universe.core.integer import MAX_WORK_INT
from event_universe.core.ports import Wrap
from event_universe.core.rule3 import coefficients
from event_universe.features.hold import hold
from event_universe.features.read import (
    content_of,
    edge_squared,
    link_tension,
    paces_guard,
    stability_bound,
)
from event_universe.features.start import arrivals, read_content, rest, scaled_source
from event_universe.features.write import carried
from event_universe.loader.derived import held_write_of, readers_of, weight_of
from event_universe.loader.universe import universe_of
from tests.laws import CHARGED, ROOT, UNIVERSE, refused

GAMMA, SHAPE = 10_000, (3, 3, 3)
OWN = {"own_weight": 1, "intervals": paces.COUNT_POWER}  # a row reading its own level at 1, a count


def test_a_hill_enters_as_it_is_and_the_guard_refuses_a_pace_beyond_the_edge_by_name():
    """No floor and no clamp: a hill of 150 on [800, 850] (the edge's square 2 den Gamma^2 div (den + num) between 10,150^2 and 10,151^2) takes the clock's square to 10,151^2 and the load refuses it naming the Node; 75 passes as it is, the content -75, and the read alone never refuses; the same hill on one Link's content alone is caught on that Port as an integer pace; for den = num the edge is p <= Gamma exactly: a content of -1 refuses by name, a content at Gamma div 2 at both ends of every Link (the Link's pace at 0) refuses on the lower side and Gamma div 2 - 1 passes; for a negative numerator the band's lowest mode is at wave number 0 and the edge's square is 2 den Gamma^2 div (den + |num|), 21 for the pair [-1, 2] at Gamma = 4, so the audit's witness (#1583 B2), the content -1 with the clock's square 26 and 2 cos omega = -23 / 8 at k = 0, is refused by name where the edge of den + num (64) admitted it, and the vacuum of that pair passes. Three reads (2 a - 3 b + 4 c) sum per Node exactly; no reads give the integer 0 (the plain rule at Gamma); the Link's tension is SUM over the reads of (weight x (aa_i + aa_j) + 1) div 2, the mean of its two ends' parts, one division per read per Link: the ends 7 and 7 at the weight 1 give 7 and -7 and -7 give -7 (the Node's own part in a uniform level), the ends 7 and -7 give 0 and a second read of the ends 3 and 4 beside it 0 + 4. Forward the quotient and the remainder of numerator + r; back from the remainder after, the same quotient and the remainder before (the hold's write forward and back on numerators of both signs, the declaration's test below); a wall below 1 and a direction other than +1 or -1 are refused by name. The hold's write forward and back, with its weights, is the declaration's test below; a wall below 1 is refused by name."""
    (left, right), edge = stability_bound((800, 850), GAMMA), edge_squared((800, 850), GAMMA)
    assert (left, right) == (1_650, GAMMA * GAMMA * 1_700) and edge == right // left
    assert 10_150**2 <= edge < 10_151**2 and GAMMA % 2 == 0
    flat = np.zeros(SHAPE, dtype=np.int64)

    def hill(depth: int) -> np.ndarray:
        return content_of([(-1, np.pad(np.array([[[depth]]]), 1))])

    plain = (np.full(SHAPE, 256),) * 6  # the six Links' factors with no tension, G^2 at G = 16
    assert int(hill(74)[1, 1, 1]) == -74 and int(hill(150)[1, 1, 1]) == -150  # the read carries no guard
    paces_guard((800, 850), GAMMA, 16, hill(74), plain, "matter")
    axis, hollow, deep = plain[0].copy(), flat.copy(), flat.copy()
    axis[2, 0, 1], hollow[0, 1, 0] = 264, -1  # 264: the tension -153, a hill
    deep[1, 1, 1], zero = paces.frozen_content(4), paces.frozen_content(4)  # the Link's zero at Gamma 4
    edge, light, hill_pair = r"squared is 103042801 at the Node \(1, 1, 1\) at load", "light", (800, 850)
    port, closed = (*plain[:4], axis, plain[5]), (plain[0], 0 * plain[0], *plain[2:])
    for match, pair, content, factors, name in (
        (rf"the clock\) {edge}", hill_pair, hill(150), plain, "matter"),
        (rf"the Node\) {edge}", hill_pair, hill(75), plain, "matter"),
        (r"the Port 4\) squared is 26400000000 in the unit G\^2 = 256", hill_pair, flat, port, "matter"),
        (r"squared is 100020001 at the Node \(0, 1, 0\) at load, above", (1, 1), hollow, plain, light),
        (r"factor of 'light' \(the Port 1\) is 0 at the Node \(0, 0, 0\)", (1, 1), flat, closed, light),
    ):
        refused(match, paces_guard, pair, GAMMA, 16, content, factors, name)
    at_zero = rf"is {zero} at the Node \(1, 1, 1\) at load, at or beyond {zero}"  # the Link's zero
    refused(at_zero, paces_guard, (1, 1), 4, 16, deep, plain, light)
    deep[1, 1, 1] -= 1
    paces_guard((1, 1), 4, 16, deep, plain, "light")  # one below the Link's zero passes
    assert (stability_bound((-1, 2), 4), edge_squared((-1, 2), 4)) == ((3, 64), 21)  # [-1, 2] at Gamma 4
    witness = r"the clock\) squared is 25 at the Node \(0, 0, 0\) at load, above the stability edge's square 21"
    refused(witness, paces_guard, (-1, 2), 4, 1, flat - 1, (1,) * 6, "quarks")  # the content -1, a hill
    paces_guard((-1, 2), 4, 1, flat, (1,) * 6, "quarks")  # the pair's vacuum, 2 cos omega = -1 at k = 0
    shape, a = (2, 1, 1), np.array([[[5]], [[7]]], dtype=np.int64)
    b, c = np.array([[[1]], [[-2]]], dtype=np.int64), np.array([[[3]], [[0]]], dtype=np.int64)
    assert content_of([(2, a), (-3, b), (4, c)]).tolist() == [[[10 - 3 + 12]], [[14 + 6]]]
    level, full = np.array([[[7]], [[-7]]], dtype=np.int64), np.full(shape, 3)
    assert content_of([]) == 0 and link_tension([]) == 0
    assert link_tension([(1, level, level)]).ravel().tolist() == [7, -7]
    assert link_tension([(1, level, -level), (1, full, full + 1)]).ravel().tolist() == [4, 4]
    refused("wall is from 1", carried, 5, 0, 0), refused("direction", carried, 5, 3, 0, 2)
    refused("wall E_s T is from 1", hold, 0, 1, 0, 0)


OPEN_CHAIN, OPEN_CUBE = Wrap(False, True, True), Wrap(False, False, False)


def test_the_rest_is_the_lines_own_fixed_point_on_a_chain_and_a_box():
    """On a chain and a box, at [1, 1], at the binding holder's pair [2400, 2401] and at short-range pairs (a periodic box too, at [24, 25], the screening its sink: the sink's rule is any screened pair's, and the long range converges in 170,000 passes), with sources of one sign and of both (a box with one open face, its sink): one more act of the line returns the fine levels (the first repeat is a fixed point), the line's residual at the row's own composed paces, (6 (den - num) p_0^2 + 6 num p_i^2) b - num p_i^2 S_6(b) - 3 den Gamma^2 sigma with sigma scaled per proper volume and per proper interval, is within one act's floor (0 to the divisor), and the levels are the fine levels over the unit to the nearest integer, of the sources' sign at the sources (a negative source beside a positive one at 0 at most) and, with one sign, never below 0. A point source of 3,000 quanta at the centre of the open 11-cube and of 30 at the centre of the open chain of 49 Nodes (odd, so the centre is centred), the massless row and the binding holder's pair of the tests' universe: the level at the six neighbours is one number (an isotropic rest, the vector test of the two rows), the level falls along each axis all the way to the face (the screened well of the six Ports, whose reach is the pair's, ALGEBRA.md #the-well), at every Node, the far ones among them, the level is within one unit of the self-consistent line at the row's own composed paces with the source scaled as the write scales it, solved sparse, and the exact line's ratio binding over massless at 0 to 4 Links, the pair's reach, is pinned; the ratio at 12 Links is the 25-cube's reading in ENGINE.md, section 8, and no assertion (a test runs under 30 seconds, the owner's word of 2026-10-03). A board periodic on its every axis at [1, 1] gives the sources no sink; a level weight below 1 is refused. The self-consistent line at the row's own paces, solved sparse at those paces, returns the levels. A one-Node source of 24,576 quanta on an open 11-cube at Gamma 6,000 under the binding pair: the levels re-read from their own rounding swing between two states 10,071 apart at the Node, no fixed point and no rounding tie, refused by name."""
    chain, box = np.zeros((40, 1, 1), dtype=np.int64), np.zeros((6, 5, 4), dtype=np.int64)
    chain[10:13, 0, 0], chain[25, 0, 0], box[1:3, 1:3, 1] = 30, 12, 9
    mixed = box.copy()
    mixed[4, 2:4, 2], mixed[1, 1, 1] = -13, -9  # sources of both signs, the tension and the senses
    cases = [(chain, OPEN_CHAIN, pair, 7) for pair in ((1, 1), (2400, 2401), (1, 4))]
    cases += [(box, OPEN_CHAIN, (1, 1), 7)] + [(mixed, OPEN_CHAIN, pair, 7) for pair in ((1, 1), (1, 2))]
    cases += [(box, Wrap(True, True, True), (24, 25), 1), (box, Wrap(True, True, True), (3, 4), 7)]
    for counts, faces, (num, den), level_weight in cases:
        found = rest(counts, (num, den), faces, level_weight, MAX_WORK_INT, 3 * den, GAMMA, **OWN)
        fine, own = found.fine.astype(object), found.content.astype(object)
        side = counts.astype(object) * (3 * den * found.unit) // level_weight * GAMMA**2
        clock, pace = paces.node_paces(GAMMA, own)  # the row's own level in its composed paces
        side = paces.write_factor(side, pace, pace, pace, clock, GAMMA, 2)  # per proper volume
        divisor = 6 * (den - num) * clock**2 + 6 * num * pace**2
        left = divisor * fine - num * pace**2 * sum(arrivals(fine, faces)) - side
        assert (np.abs(left) < 2 * divisor).all(), (num, den, faces)  # a fine unit off the line at most
        assert (found.levels == (fine + found.unit // 2) // found.unit).all() and found.iterations > 1
        assert (found.levels[counts > 0] > 0).all() and (found.levels[counts < 0] <= 0).all()
        assert (found.levels < 0).any() != (counts >= 0).all()  # only negative sources sink below 0
        assert found.remainder == (3 * den - 1) // 2
    rows = json.loads(UNIVERSE.read_text(encoding="utf-8"))["families"]
    row = next(entry for entry in rows if entry["name"] == "binding")
    (num, den), weight, exact = row["pair"], row["held"]["level_weight"], {}
    for shape, wrap, q in (((11, 11, 11), OPEN_CUBE, 3000), ((49, 1, 1), OPEN_CHAIN, 30)):  # the source
        counts, c = np.zeros(shape, dtype=np.int64), tuple(n // 2 for n in shape)
        counts[c] = q  # q quanta at the centre at the divisor 1 (a chain's rest a tent, so a hundredth)
        for pair in ((6000, 6000), (num, den)):
            found = rest(counts, pair, wrap, 1, MAX_WORK_INT, 3 * pair[1], 6000, **OWN)
            clock, pace = paces.node_paces(6000, found.content)  # the row's own composed paces
            paths = [diags([1.0, 1.0], [-1, 1], shape=(n, n)) if n > 1 else [[2.0]] for n in shape]
            links = kronsum(kronsum(paths[0], paths[1]), paths[2])  # a folded axis its Node twice
            divisor = 6 * (pair[1] - pair[0]) * clock**2 + 6 * pair[0] * pace**2  # the Node's term
            operator = (diags(divisor.ravel()) - diags((pair[0] * pace**2).ravel()) @ links).tocsr()
            scaled = scaled_source(counts * 3 * pair[1] * found.unit * 6000**2, clock, pace, 6000, 2)
            exact[shape[0], pair] = spsolve(operator, scaled.ravel() / found.unit).reshape(shape)
            assert (np.abs(found.levels - exact[shape[0], pair]) <= 1).all(), (shape, pair)
            long = [(a, s) for a in range(3) if shape[a] > 1 for s in (1, -1)]  # the long axes' Ports
            at = {int(np.moveaxis(found.levels, a, 0)[(c[0] + s, *c[1:])]) for a, s in long}  # isotropy
            assert len(at) == 1 and 0 < at.pop() < found.levels[c]
            assert (np.diff(fall := found.levels[c[0] :, c[1], c[2]]) <= 0).all() and fall[-1] >= 0
    ratio = (exact[11, (num, den)] / exact[11, (6000, 6000)])[5:10, 5, 5]  # 0 to 4 Links
    assert np.allclose(ratio, [0.9982, 0.9949, 0.9907, 0.9869, 0.9841], 0, 1e-4), ratio
    deep = np.pad(np.full((1, 1, 1), 24_576), 5)  # one Node of an 11-cube: open, the re-read swings
    refused("needs a sink", rest, deep, (1, 1), Wrap(True, True, True), 1, MAX_WORK_INT, 3, GAMMA, **OWN)
    refused("is from 1", rest, deep, (1, 2), OPEN_CHAIN, 0, MAX_WORK_INT, 6, GAMMA, **OWN)
    refused("a cycle", rest, deep, (num, den), OPEN_CUBE, weight, MAX_WORK_INT, 3 * den, 6000, **OWN)


def universe(*rows: dict, **integers: int) -> dict:  # type: ignore[type-arg]
    """A universe file of the rows given at Gamma 10,000, T 64, the width 63 and the Link unit 1, but for `integers`."""
    integers = {"node_clock": GAMMA, "quantum_action": 64, "width": 63, "link_unit": 1, **integers}
    return {"integers": integers, "families": [dict(row) for row in rows]}


HELD = {"sources": ["form"], "level_weight": 5, "write_weight": 3, "act": "pace"}
HOLLOW = {"name": "hollow", "pair": [1, 1], "reads": {"hollow": 1}, "held": HELD}  # reading itself at 1
CORE = {"name": "core", "pair": [3, 4], "reads": {}}
CORE["held"] = {**HELD, "level_weight": 7, "write_weight": -1}
STUFF = {"name": "stuff", "pair": [4000, 6000], "reads": {"hollow": 2}, "dimension": 1}
OTHER = {"name": "other", "pair": [4000, 6000], "reads": {"core": 1}, "dimension": 1}
SIGN = {"name": "sign", "pair": [1, 1], "reads": {}, "held": {**HELD, "sources": ["wronskian"]}}
SIGN["held"].update(level_weight=1, write_weight=1, act="rotation")
TUBE, TURN = "charged", "turning"  # the charged universes at examples/events/, the tests' alone
WRITES = {(TUBE, "charge"): 4, (TURN, "charge"): 400}  # k_w = 4 E_h


def test_every_family_reads_the_holders_its_declaration_names_and_the_write_carries_its_weight():
    """The declaration's read (ALGEBRA.md, the owner's decision of 2026-10-02: every family reads the holders its declaration names, at the weights it names, and sources each at the weight it reads with) and the write weight (the holder's declared coefficient sits in the write): a universe of two holders of the content, `hollow` [1, 1] at the level weight 5 and the write weight 3 reading itself at 1, `core` [3, 4] at 7 and -1 reading nothing, and two real-line families of matter's pair, `stuff` reading `hollow` at 2 and `other` reading `core` at 1. On random levels of a periodic 3-cube: `stuff`'s content is 2 x hollow's time line and `other`'s core's, `core` reads 0 (the plain rule at Gamma) and every Link's factor is G^2; the rule of `stuff` is the law's line at the composed paces of 2 L; `hollow` is sourced by `stuff` alone and `core` by `other` alone (the reciprocity), each write's numerator the write weight times the reader's weight times its form scaled by the write's factor, 3 x 2 x D' and -1 x 1 x D', negative at some Node over the random levels, and the level gains (numerator + r) div (E_s T) with the remainder in [0, wall), a negative numerator taking the level down by the floor, the write back exact (a negative level read into a pace is the hill of the guard's test above, the clock Gamma (1 - 1 / Gamma)^c above Gamma for c below 0, admitted as it is within the edge). The start: `read_content` sums weight x (level + rest) over the reads with the row's own weight apart. The loader refuses by name a family without `reads` and a held row without `write_weight`, naming the family, a weight 0, a read of no held row, the holder of the sign naming itself and a real-line family naming a holder under the rotation; the energy line's gate (E_h T num = k_w Gamma den per plane family reading a holder under the rotation, the read weight cancelling under the reciprocity; the advisor's hand, #1563 comment 5945592281): a plane reading the holder at E_h = 1 and k_w = 1 is refused at T = 64 (1 x 64 x 4000 against 1 x Gamma x 6000) and passes at T = Gamma x 6000 / 4000 (every plane family of one universe sharing num / den, or the gate refuses the one out of the line by name); on a board of two Nodes with the sign holder at -5 and 5 the plane reading it at 1 under the act pace reads 5 at both, the size of the level, a hollow whatever its sense (ALGEBRA.md row (f); the advisor's hand, #1563 comment 5945859368), and under the rotation its turn's numerators are -5 and 5, the signed level, and its content read is the integer 0, the holder's level entering no content (the one declared act, the mathematician's 117 III); the rule's own universe at T 32,768 is not gated with the tests' charged row under the plain read, refused with it under the rotation at the write weight 1 and admitted at the advisor's k_w = 4 and T = 36,000; the shipped universe files restate the one read the loader derived before this round, every family of quanta reading every holder of the content at 1, a plane the holders of the sign at 1 too, a holder of the content itself among its reads and the holder of the sign none of the sign, every write weight 1 but the charged-body universes' sign holder at the energy line's 4 E_h."""
    integers, families = universe_of(universe(HOLLOW, CORE, STUFF, OTHER))
    hollow, core, stuff, other = range(4)
    reads = [[(r.family, r.weight) for r in f.reads] for f in families]
    assert reads == [[(0, 1)], [], [(0, 2)], [(1, 1)]] and readers_of(families, hollow) == [stuff]
    assert readers_of(families, core) == [other] and weight_of(hollow, families[stuff]) == 2
    draw, wrap, action = np.random.default_rng(7), Wrap(True, True, True), integers["quantum_action"]
    writes = {i: held_write_of(families, i, action) for i in (hollow, core)}
    walls = [writes[i].walls if f.held else () for i, f in enumerate(families)]
    states = [node.empty_state(f, SHAPE, w, np.int64) for f, w in zip(families, walls, strict=True)]
    for state in states:
        levels = [draw.integers(1, 40, (2, *SHAPE)) for _ in state.lines]
        state.lines = [node.Record(*pair, 0 * SHAPE[0]) for pair in levels]
    levels = [states[i].lines[0].now for i in (hollow, core)]
    read = {i: node.read(i, families, states, 1, wrap, GAMMA, 1) for i in range(4)}
    assert np.array_equal(read[stuff][0], 2 * levels[0]) and np.array_equal(read[other][0], levels[1])
    assert np.array_equal(read[hollow][0], levels[0]) and read[core] == (0, (1,) * 6)
    by_law = coefficients(4000, 6000, GAMMA, *paces.node_paces(GAMMA, 2 * levels[0]))[0]
    rule = node.rule_of(families[stuff], GAMMA, *read[stuff])
    assert all(np.array_equal(a, b) for a, b in zip(rule[0], by_law, strict=True))
    forms, rulers = {}, {}
    for i in (stuff, other):
        own = node.rule_of(families[i], GAMMA, *read[i])
        _lines, (first, second) = node.step_family(i, families, states, own, wrap, GAMMA)
        forms[i, 0] = node.form(first, second)  # the bookings per record, (family, record)
        rulers[i, 0] = node.rulers(i, families, states, 1, wrap, GAMMA)
    for held, reader, weights in ((hollow, stuff, 3 * 2), (core, other, -1 * 1)):
        numerators = node.write_sources(held, families, forms, {}, writes[held], rulers, GAMMA)
        by_hand = weights * node.rulers_write_factor(forms[reader, 0], rulers[reader, 0], GAMMA, 2)
        assert len(numerators) == 1 and np.array_equal(numerators[0], by_hand) and (by_hand < 0).any()
        before, wall = states[held].lines[0], writes[held].walls[0]
        remainder = [draw.integers(0, wall, SHAPE)]
        (after,), (kept,) = node.held_write([before], numerators, [wall], remainder)
        increment, left = np.divmod(by_hand + remainder[0], wall)
        assert np.array_equal(after.now, before.now + increment) and np.array_equal(kept, left)
        (back,), (origin,) = node.held_write([after], numerators, [wall], [kept], -1)
        assert np.array_equal(back.now, before.now) and np.array_equal(origin, remainder[0])
    found, own_weight = read_content(((0, 1), (1, 3)), levels, [0, 60], 1)
    assert np.array_equal(found, levels[0] + 3 * 60) and own_weight == 3
    missing = {k: v for k, v in STUFF.items() if k != "reads"}
    unweighted = {**HOLLOW, "held": {"sources": ["form"], "level_weight": 5, "act": "pace"}}
    plane = {**STUFF, "dimension": 2, "reads": {"sign": 1}}
    for rows, reason in (
        ((HOLLOW, missing), r"families\[1\] \('stuff'\) lacks the key 'reads'"),
        ((unweighted, STUFF), r"\('hollow'\).held lacks the key 'write_weight'"),
        ((HOLLOW, {**STUFF, "reads": {"hollow": 0}}), r"reads\['hollow'\] is 0"),
        ((HOLLOW, {**STUFF, "reads": {"hollow": 2, "stuff": 1}}), "no held row of that name"),
        (({**SIGN, "reads": {"sign": 1}},), "never reads its own level"),
        ((SIGN, {**STUFF, "reads": {"sign": 1}}), "no plane"),
        ((SIGN, plane), "energy line fails for 'stuff'"),
    ):
        refused(reason, universe_of, universe(*rows))
    turning = universe_of(universe(SIGN, plane, quantum_action=15_000))[1]  # T 4,000 = Gamma 6,000
    paced = universe_of(universe({**SIGN, "held": {**SIGN["held"], "act": "pace"}}, plane))[1]
    two, level = np.zeros((2, 1, 1), dtype=np.int64), np.array([[[-5]], [[5]]], dtype=np.int64)
    for rows, found in ((paced, [5, 5]), (turning, [-5, 5])):  # |L| into the pace; the turn by L
        board = [node.empty_state(f, (2, 1, 1), (), np.int64) for f in rows]
        board[0].lines[0] = node.Record(level, level, two)
        paced_read = node.read(1, rows, board, 1, wrap, GAMMA, 1)[0]
        turn = node.turning(1, rows, board, 1, GAMMA)
        assert np.asarray(paced_read if rows is paced else turn[0]).ravel().tolist() == found
        assert rows is paced or paced_read == 0  # the rotation: no level in the content
    rows = (rule := json.loads(UNIVERSE.read_text(encoding="utf-8")))["families"]
    charge = next(row for row in rows if row["name"] == "charge")["held"]
    universe_of({**rule, "families": [*rows, CHARGED]})  # the plain read: not gated
    charge["act"] = "rotation"
    refused("fails for 'charged'", universe_of, {**rule, "families": [*rows, CHARGED]})
    charge["write_weight"], rule["integers"]["quantum_action"] = 4, 36_000  # the advisor's one line
    universe_of({**rule, "families": [*rows, CHARGED]})
    for name in ("rule", "light", "pair", "nuclide/deuteron", TUBE, TURN):
        shipped = universe_of(json.loads((UNIVERSE.parent / f"{name}.json").read_text()))[1]
        held = [(i, f.wronskian) for i, f in enumerate(shipped) if f.held]
        for f in shipped:
            expected = sorted((i, 1) for i, sign in held if f.plane or not sign)
            assert sorted((r.family, r.weight) for r in f.reads) == expected, (name, f.name)
            assert f.write_weight == (WRITES.get((name, f.name), 1) if f.held else None), (name, f.name)


def test_a_frozen_row_stands_outside_the_energy_line_and_two_moving_planes_still_share_their_pair():
    """The frozen row's exemption (ALGEBRA.md, the atom round's reading: the frozen-row nucleus [0, den] beside the electron's pair, the energy line's constraint that the plane families of one world share num / den lifted for num = 0 by name, the advisor's #1572 comment 5966780505 and the mathematician's 236 and 242, two hands): a universe of the sign holder under the rotation, a plane of matter's pair on the line (E_h T num = k_w Gamma den at T = 15,000) and a frozen plane [0, 6000] reading the holder at 1 loads, the frozen row's record never moving (R_ij = 2 num p^2 Q = 0 on every Link) and giving no light; the frozen row of three planes (the frozen proton's row) alike; a second moving plane whose num / den differs, [3000, 6000], is refused by name as before, and a frozen row under the plain read (the act `pace`) was never gated."""
    plane = {**STUFF, "dimension": 2, "reads": {"sign": 1}}
    frozen = {**plane, "name": "frozen", "pair": [0, 6000]}
    proton = {**frozen, "name": "proton", "dimension": ["plane"] * 3}
    for rows, zeros in (
        ((SIGN, plane, frozen), [False, False, True]),
        ((SIGN, frozen, proton), [False, True, True]),
    ):
        families = universe_of(universe(*rows, quantum_action=15_000))[1]
        assert [f.pair[0] == 0 for f in families] == zeros and all(f.plane for f in families[1:])
    moving = {**plane, "name": "slower", "pair": [3000, 6000]}
    refused("fails for 'slower'", universe_of, universe(SIGN, plane, moving, quantum_action=15_000))
    universe_of(universe({**SIGN, "held": {**SIGN["held"], "act": "pace"}}, plane, frozen))


def test_the_rests_room_is_the_sources_own_bound_where_the_tent_leaves_no_unit():
    """The fine unit of a rest (`unit_of`): under the tent where the tent leaves a unit, as every shipped world has it; where it leaves none, on a board with no folded axis, under the source's own bound, the source total over its wall plus one, since a point source's rest on the cubic lattice peaks at 3 G(0) of its source over the wall, below one (the mathematician's 249 with the advisor's second, two hands: the tent over-bounds a point source by 2 (L + 1), which held the atom's Node clock at a fiftieth of its reach). A point source on an open cube: at a Node clock the tent admits, the tent's unit; at one it refuses, the bound's unit, the levels the same rest within one level (the rest in levels is the clock's own at the vacuum's paces), its peak under the bound; at a clock the bound refuses too, the refusal by name; a chain, its axes folded, and a tube with two periodic axes keep the tent and the refusal (the mathematician's 260: a periodic axis folds the source's images onto it)."""
    from event_universe.features.start import source_bound, tent_of, unit_from_bound, unit_of

    counts, chain = np.zeros((9, 9, 9), dtype=np.int64), np.zeros((40, 1, 1), dtype=np.int64)
    counts[4, 4, 4], chain[20, 0, 0], pair, width = 1000, 1000, (6000, 6000), MAX_WORK_INT
    admitted, refused_by_the_tent, refused_by_both = 60_000, 70_000, 300_000
    assert unit_from_bound(tent_of(counts, 1), pair, width, admitted) >= 1
    assert unit_from_bound(tent_of(counts, 1), pair, width, refused_by_the_tent) == 0
    assert unit_of(counts, pair, 1, width, admitted, OPEN_CUBE) == unit_from_bound(
        tent_of(counts, 1), pair, width, admitted
    )
    assert unit_of(counts, pair, 1, width, refused_by_the_tent, OPEN_CUBE) == unit_from_bound(
        source_bound(counts, 1), pair, width, refused_by_the_tent
    )
    sign = {"own_weight": 0, "intervals": paces.COUNT_POWER}  # the holder of the sign, a count source
    by_the_tent = rest(counts, pair, OPEN_CUBE, 1, width, 3 * pair[1], admitted, **sign)
    by_the_bound = rest(counts, pair, OPEN_CUBE, 1, width, 3 * pair[1], refused_by_the_tent, **sign)
    assert by_the_bound.unit >= 1 and by_the_tent.unit >= 1  # the bound's unit where the tent's is none
    assert int(np.abs(by_the_bound.levels - by_the_tent.levels).max()) <= 1
    assert int(by_the_bound.levels.max()) < source_bound(counts, 1) < tent_of(counts, 1)
    with pytest.raises(ValueError, match="no fine unit"):
        unit_of(counts, pair, 1, width, refused_by_both, OPEN_CUBE)
    with pytest.raises(ValueError, match="no fine unit"):
        unit_of(chain, pair, 1, width, refused_by_the_tent, OPEN_CHAIN)
    tube = np.zeros((2, 2, 40), dtype=np.int64)  # two periodic axes fold the source's images onto it
    tube[0, 0, 20] = 1000
    with pytest.raises(ValueError, match="no fine unit"):  # the slab's rest above the bound (260)
        unit_of(tube, pair, 1, width, refused_by_the_tent, Wrap(True, True, False))


def test_the_writes_room_under_a_negative_tension_is_the_larger_of_the_hills_and_the_tensions():
    """The register's room under a negative tension (ALGEBRA.md, The write per proper volume and per proper interval; the mathematician's 268 and the advisor's second with one precision, #1572 comments 5969128707 and 5969197876, two hands): the guard bounds p_i^2 Q_ij and not the Link's factor q = Gamma - t, so under a negative tension q exceeds Gamma, up to q_max = Gamma + W A, the sum of W_a A over the held rows with axis lines a source reads, and the write's factor in a hollow reaches (P / Gamma)^3 sqrt(q_max / P) on a count and (P / Gamma)^3 q_max / P on a Wronskian, beyond the hill's room (P / Gamma)^3 rounded up. At the rule's universe (Gamma 6,000, W 1, the hill's own bound A_1 = 9,266, q_max 15,266) the law's ceilings are 3 on a count and 4 on a Wronskian for matter's pair (P 6,572; the register's values 2.003 and 3.053 against the hill's room 2) and 2 and 3 for the three massless pairs (P 6,000; 1.595 and 2.544 against 1): `tension_room` returns them and exceeds `hill_scale` exactly where the register's values exceed it; the four shipped universes' bound stays 9,266, the write's total not their binding term; a universe where it is, a holder of the massless pair with axis lines at the write weight 10^6 read by one real line at 1 (Gamma 10,000, T 64, the width 63), has the hill's bound 2,147,483, isqrt((2^63 - 1 - 64) div (10^6 x 2 x 1)), and under the rooms 554,477, the tension's room 15 at q_max = 10,000 + 2,147,483, smaller by name."""
    from fractions import Fraction
    from math import ceil, isqrt

    from event_universe.loader import derived

    gamma, hill_bound = 6000, 9266
    q_max = gamma + 1 * hill_bound  # W = 1: every shipped family reads gravity's axis lines at 1
    for row in json.loads(UNIVERSE.read_text(encoding="utf-8"))["families"]:
        pair, matter = tuple(row["pair"]), row["name"] == "matter"
        edge = isqrt(2 * pair[1] * gamma**2 // (pair[1] + pair[0]))  # the hill's edge pace P
        assert edge**2 <= edge_squared(pair, gamma) < (edge + 1) ** 2 and edge == (
            6572 if matter else 6000
        )
        hill = ceil(Fraction(edge**3, gamma**3))
        count = ceil(Fraction(edge**2 * (isqrt(q_max * edge) + 1), gamma**3))
        wronskian = ceil(Fraction(edge**2 * q_max, gamma**3))
        values = ((edge / gamma) ** 3 * (q_max / edge) ** 0.5, (edge / gamma) ** 3 * q_max / edge)
        assert [round(v, 3) for v in values] == ([2.003, 3.053] if matter else [1.595, 2.544])
        assert (hill, count, wronskian) == ((2, 3, 4) if matter else (1, 2, 3))
        assert all(value > hill for value in values) and derived.hill_scale(pair, gamma) == hill
        assert derived.tension_room(pair, gamma, q_max, False) == count > hill
        assert derived.tension_room(pair, gamma, q_max, True) == wronskian > hill
    for name in ("rule", "light", "ghz", "pair"):
        integers, families = universe_of(json.loads((UNIVERSE.parent / f"{name}.json").read_text()))
        keys = ("node_clock", "quantum_action", "width", "link_unit")
        assert derived.amplitude_bound(families, *(integers[key] for key in keys)) == hill_bound, name
    axes = {"sources": ["form", "tensions"], "level_weight": 1, "write_weight": 10**6, "act": "pace"}
    well = {"name": "well", "pair": [1, 1], "reads": {"well": 1}, "held": axes}
    deep = {**well, "name": "deep", "reads": {"deep": 1}, "held": {**axes, "write_weight": 1}}
    line = {"name": "line", "pair": [1, 1], "reads": {"well": 1}, "dimension": 1}
    families = universe_of(universe(well, line))[1]
    largest, wall, room = (
        2**63 - 1,
        1 * 64,
        10**6 * 1 * 2 * 1,
    )  # E_s T; k_w x W x two products x the hill's 1
    under_the_hill = isqrt((largest - wall) // room)
    tension = ceil(Fraction(GAMMA**2 * (isqrt((GAMMA + under_the_hill) * GAMMA) + 1), GAMMA**3))
    under_the_rooms = isqrt((largest - wall) // (room * tension))
    assert (under_the_hill, tension, under_the_rooms) == (2_147_483, 15, 554_477)
    assert derived.bound_under_rooms(families, GAMMA, 64, 63, 1, None) == under_the_hill
    assert derived.amplitude_bound(families, GAMMA, 64, 63) == under_the_rooms < under_the_hill
    two = universe_of(universe(well, deep, {**line, "reads": {"well": 1, "deep": 2}}))[1]
    assert (
        derived.factor_bound(two, 2, GAMMA, 7) == GAMMA + (1 + 2) * 7
    )  # the sum over the two rows read


def test_the_engines_numbers_are_written_from_the_ports_and_the_levels_names():
    """No number in the engine (ENGINE.md, the start; ALGEBRA.md, the ledger's row 5 and The giving): the start's fine unit under a bound equals the former 2 x 2 x |num| x 6 x L x Gamma^2 form, the six reads at the vacuum's paces taken twice for the two levels; on three open chains the rest of a point source peaks at the discrete parabola's top 3 S c (n + 1 - c) / (n + 1) within one level, under the tent; the miss bound is (6 div 2) ((n + 2) div 2)^2 + 1 on a chain, a slab and a cube of the same extent, the six reads over the axis's two Ports and no three of the axes; the rest's `intervals` is keyword-only, the two powers by name in its two callers, 2 on a count and 1 on a Wronskian, the write's factor p^3 / (p_0 Gamma^2) and p^3 / (p_0^2 Gamma); the radiated total within one of (2 / 3) T sin k at two T and two resonances; and `PORTS` is defined once under src/, in core/ports.py."""
    from event_universe.features.start import bound_of, tent_of, unit_from_bound
    from event_universe.giving import radiated_total
    from event_universe.loader.lay import least_action

    gamma, width, source = 6000, MAX_WORK_INT, 1000
    former = width // (2 * 2 * 3 * 6 * source * gamma * gamma)  # 24 |num| L Gamma^2 at num = 3, L = 1000
    assert unit_from_bound(source, (3, 4), width, gamma) == former > 0
    reads, divisor = (gamma * gamma,) * 3, np.int64(6 * gamma * gamma)  # the massless line's
    count = {"intervals": paces.COUNT_POWER}
    for n in (5, 9, 17):
        counts, c = np.zeros((n, 1, 1), dtype=np.int64), (n + 1) // 2
        counts[c - 1] = source  # the point source at the chain's centre Node c, 1 to n
        field = rest(counts, (1, 1), OPEN_CHAIN, 1, width, 3, gamma, own_weight=0, **count)
        peak = (
            3 * source * c * (n + 1 - c) // (n + 1)
        )  # 2 b_x - b_(x-1) - b_(x+1) = 3 sigma, b_0 = b_(n+1) = 0
        assert abs(int(field.levels.max()) - peak) <= 1 < tent_of(counts, 1) - peak
        for shape in ((n, 1, 1), (n, n, 1), (n, n, n)):
            wrap = Wrap(False, shape[1] == 1, shape[2] == 1)
            assert (
                bound_of(np.zeros(shape, dtype=np.int64), wrap, reads, divisor)
                == 3 * ((n + 2) // 2) ** 2 + 1
            )
    with pytest.raises(TypeError):
        rest(counts, (1, 1), OPEN_CHAIN, 1, width, 3, gamma, 0, 2, own_weight=0)  # no positional power
    assert (paces.COUNT_POWER, paces.WRONSKIAN_POWER) == (2, 1)
    powers = (paces.COUNT_POWER, paces.WRONSKIAN_POWER)
    assert [int(paces.write_factor(np.int64(1), 6, 6, 6, 3, 6, k)) for k in powers] == [
        2,
        4,
    ]  # 216 / (36 x 3), 216 / (6 x 9)
    text = (ROOT / "src" / "event_universe" / "features" / "start" / "__init__.py").read_text(
        encoding="utf-8"
    )
    assert [text.count(f"intervals=paces.{k}") for k in ("COUNT_POWER", "WRONSKIAN_POWER")] == [1, 1]
    for action, (num, den) in ((32768, (2, 3)), (15000, (2, 3)), (32768, (4, 5)), (15000, (4, 5))):
        cos_k = (3 * num - 2 * den) / den  # the guide's wave number at the resonance
        assert abs(radiated_total(action, (num, den)) - 2 * action * (1 - cos_k**2) ** 0.5 / 3) <= 1
    budget = [least_action((2, 3), 400, 50, (1, 100), k2) for k2 in ((32, 1), (8, 1), (32, 4))]
    assert (
        budget[0] == 4 * budget[1] == 4 * budget[2] and budget[0] & (budget[0] - 1) == 0
    )  # T grows with k^2
    sources = (ROOT / "src").rglob("*.py")
    defined = [
        p.name
        for p in sources
        if any(x.startswith("PORTS =") for x in p.read_text(encoding="utf-8").splitlines())
    ]
    assert defined == ["ports.py"]  # one definition of the six Ports under src/
