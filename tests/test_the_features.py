"""The read, its own folder (ALGEBRA.md #the-paces): the content as it is, no floor, the reads summed at their weights; the axis content rounded at the read; the guard at load on squares (the checkerboard factor at -2) admits and refuses by name, and the read in the interval carries no guard. The write's folder and the hold's (ALGEBRA.md #the-primitives, a family's write is one act; the row "the hold"): (numerator + r) div wall at every Node by Rule3's carried division, the remainder kept at the Node, forward then back exact, over many intervals the written total the numerator's within one unit; a held part gains the same division each interval and loses it back; the refusals by name. The start, its own folder (ALGEBRA.md #the-generator (g), the start): a held family's rest is the division act iterated from nothing until the levels repeat, 6 den b = num S_6(b) + 3 den sigma at the fine unit from the width, the levels its nearest integers; the refusals by name."""

import json

import numpy as np
from scipy.sparse import diags, kronsum
from scipy.sparse.linalg import spsolve

from event_universe import node
from event_universe.core import paces
from event_universe.core.integer import MAX_WORK_INT
from event_universe.core.ports import Wrap
from event_universe.core.rule3 import coefficients
from event_universe.features.hold import hold
from event_universe.features.read import content_of, edge_squared, guard, link_tension, stability_bound
from event_universe.features.start import arrivals, read_content, rest, scaled_source
from event_universe.features.write import carried
from event_universe.loader.derived import held_write, readers_of, weight_of
from event_universe.loader.universe import universe_of
from tests.laws import CHARGED, UNIVERSE, refused

GAMMA, SHAPE, OWN = 10_000, (3, 3, 3), {"own_weight": 1}  # a row reading its own level at 1


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
    guard((800, 850), GAMMA, 16, hill(74), plain, "matter")
    axis, hollow, deep = plain[0].copy(), flat.copy(), flat.copy()
    axis[2, 0, 1], hollow[0, 1, 0] = 264, -1  # 264: the tension -153, a hill
    deep[1, 1, 1] = paces.frozen_content(GAMMA)  # the Link's zero, 49,545 at Gamma 10,000
    edge, light, hill_pair = r"squared is 103042801 at the Node \(1, 1, 1\) at load", "light", (800, 850)
    port, closed = (*plain[:4], axis, plain[5]), (plain[0], 0 * plain[0], *plain[2:])
    for match, pair, content, factors, name in (
        (rf"the clock\) {edge}", hill_pair, hill(150), plain, "matter"),
        (rf"the Node\) {edge}", hill_pair, hill(75), plain, "matter"),
        (r"the Port 4\) squared is 26400000000 in the unit G\^2 = 256", hill_pair, flat, port, "matter"),
        (r"squared is 100020001 at the Node \(0, 1, 0\) at load, above", (1, 1), hollow, plain, light),
        (r"is 49545 at the Node \(1, 1, 1\) at load, at or beyond 49545", (1, 1), deep, plain, light),
        (r"factor of 'light' \(the Port 1\) is 0 at the Node \(0, 0, 0\)", (1, 1), flat, closed, light),
    ):
        refused(match, guard, pair, GAMMA, 16, content, factors, name)
    deep[1, 1, 1] -= 1
    guard((1, 1), GAMMA, 16, deep, plain, "light")
    assert (stability_bound((-1, 2), 4), edge_squared((-1, 2), 4)) == ((3, 64), 21)  # [-1, 2] at Gamma 4
    witness = r"the clock\) squared is 25 at the Node \(0, 0, 0\) at load, above the stability edge's square 21"
    refused(witness, guard, (-1, 2), 4, 1, flat - 1, (1,) * 6, "quarks")  # the content -1, a hill
    guard((-1, 2), 4, 1, flat, (1,) * 6, "quarks")  # the pair's vacuum, 2 cos omega = -1 at k = 0
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
    """On a chain and a box, at [1, 1], at the binding holder's pair [2400, 2401] (a periodic box too, the screening its sink) and at short-range pairs, with sources of one sign and of both (a box with one open face, its sink): one more act of the line returns the fine levels (the first repeat is a fixed point), the line's residual at the row's own composed paces, (6 (den - num) p_0^2 + 6 num p_i^2) b - num p_i^2 S_6(b) - 3 den Gamma^2 sigma with sigma scaled per proper volume and per proper interval, is within one act's floor (0 to the divisor), and the levels are the fine levels over the unit to the nearest integer, of the sources' sign at the sources (a negative source beside a positive one at 0 at most) and, with one sign, never below 0. The binding holder's pair of the tests' universe at its level weight on a closed box of 21^3 with one source of 100 quanta per interval at the centre (the fine unit 485; at 1,000 the unit 48 leaves the floored iteration two levels off the exact line): the level at the six neighbours is one number (an isotropic rest, the vector test of the two rows), the level falls along each axis all the way to the face (the screened well of the six Ports, whose reach is the pair's, ALGEBRA.md #the-well), and at every Node, the far ones among them, the level is within one unit of the self-consistent line at the row's own composed paces with the source scaled as the write scales it, solved sparse. A board periodic on its every axis at [1, 1] gives the sources no sink; a level weight below 1 is refused. The self-consistent line at the row's own paces, solved sparse at those paces, returns the levels. A one-Node source of 24,576 quanta on an open 11-cube at Gamma 6,000 under the binding pair: the levels re-read from their own rounding swing between two states 10,071 apart at the Node, no fixed point and no rounding tie, refused by name."""
    chain = np.zeros((40, 1, 1), dtype=np.int64)
    chain[10:13, 0, 0], chain[25, 0, 0], box = 30, 12, np.zeros((6, 5, 4), dtype=np.int64)
    box[1:3, 1:3, 1] = 9
    mixed = box.copy()
    mixed[4, 2:4, 2], mixed[1, 1, 1] = -13, -9  # sources of both signs, the tension and the senses
    cases = [(chain, OPEN_CHAIN, pair, 7) for pair in ((1, 1), (2400, 2401), (1, 4))]
    cases += [(box, OPEN_CHAIN, (1, 1), 7)] + [(mixed, OPEN_CHAIN, pair, 7) for pair in ((1, 1), (1, 2))]
    cases += [(box, Wrap(True, True, True), (2400, 2401), 1), (box, Wrap(True, True, True), (3, 4), 7)]
    for counts, faces, (num, den), level_weight in cases:
        found = rest(counts, (num, den), faces, level_weight, MAX_WORK_INT, 3 * den, GAMMA, **OWN)
        fine, own = found.fine.astype(object), found.content.astype(object)
        side = counts.astype(object) * (3 * den * found.unit) // level_weight * GAMMA**2
        clock, pace = paces.node_paces(GAMMA, own)  # the row's own level in its composed paces
        side = paces.write_factor(side, pace, pace, pace, clock, GAMMA, 2)  # per proper volume
        divisor = 6 * (den - num) * clock**2 + 6 * num * pace**2
        left = divisor * fine - num * pace**2 * sum(arrivals(fine, faces)) - side
        assert ((0 >= left) & (left > -divisor)).all(), (num, den, faces)
        assert (found.levels == (fine + found.unit // 2) // found.unit).all() and found.iterations > 1
        assert (found.levels[counts > 0] > 0).all() and (found.levels[counts < 0] <= 0).all()
        assert (found.levels < 0).any() != (counts >= 0).all()  # only negative sources sink below 0
        assert found.remainder == (3 * den - 1) // 2
    rows = json.loads(UNIVERSE.read_text(encoding="utf-8"))["families"]
    row = next(entry for entry in rows if entry["name"] == "binding")
    (num, den), weight = row["pair"], row["held"]["level_weight"]
    counts = np.pad(np.full((1, 1, 1), 100), 10)  # one source of 100 quanta at the centre of the 21-cube
    found = rest(counts, (num, den), OPEN_CUBE, weight, MAX_WORK_INT, 3 * den, GAMMA, **OWN)
    levels = found.levels
    near = {int(np.moveaxis(levels, a, 0)[10 + s, 10, 10]) for a in range(3) for s in (1, -1)}
    assert len(near) == 1 and 0 < near.pop() < int(levels[10, 10, 10])
    for axis in range(3):
        along = [int(np.moveaxis(levels, axis, 0)[10 + r, 10, 10]) for r in range(11)]
        assert along == sorted(along, reverse=True) and along[10] >= 0
    own_paces = paces.node_paces(GAMMA, found.content)  # the row's own composed paces
    clock, pace = (np.asarray(p).astype(float) for p in own_paces)
    path = diags([1.0, 1.0], [-1, 1], shape=(21, 21))  # the open cube's Links, one axis then the three
    links = kronsum(kronsum(path, path), path)
    divisor = 6 * (den - num) * clock**2 + 6 * num * pace**2  # the Node's term, the Links' -num p^2
    operator = (diags(divisor.ravel()) - diags((num * pace**2).ravel()) @ links).tocsr()
    scaled = scaled_source(counts * (3 * den * found.unit) // weight * GAMMA**2, *own_paces, GAMMA, 2)
    exact = spsolve(operator, (scaled / found.unit).ravel().astype(float))
    assert (np.abs(levels - np.rint(exact).reshape(21, 21, 21)) <= 1).all()
    deep = np.pad(np.full((1, 1, 1), 24_576), 5)  # one Node of an 11-cube: open, the re-read swings
    refused("needs a sink", rest, deep, (1, 1), Wrap(True, True, True), 1, MAX_WORK_INT, 3, GAMMA, **OWN)
    refused("is from 1", rest, deep, (1, 2), OPEN_CHAIN, 0, MAX_WORK_INT, 6, GAMMA, **OWN)
    refused(
        "no fixed point", rest, deep, (num, den), OPEN_CUBE, weight, MAX_WORK_INT, 3 * den, 6000, **OWN
    )


def universe(*rows: dict, **integers: int) -> dict:  # type: ignore[type-arg]
    """A universe file of the rows given at Gamma 10,000, T 64, the width 63 and the Link unit 1, but for `integers`."""
    integers = {"node_clock": GAMMA, "quantum_action": 64, "width": 63, "link_unit": 1, **integers}
    return {"integers": integers, "families": [dict(row) for row in rows]}


HELD = {"sources": ["form"], "level_weight": 5, "write_weight": 3}
HOLLOW = {"name": "hollow", "pair": [1, 1], "reads": {"hollow": 1}, "held": HELD}  # reading itself at 1
CORE = {"name": "core", "pair": [3, 4], "reads": {}}
CORE["held"] = {**HELD, "level_weight": 7, "write_weight": -1}
STUFF = {"name": "stuff", "pair": [4000, 6000], "reads": {"hollow": 2}, "dimension": 1}
OTHER = {"name": "other", "pair": [4000, 6000], "reads": {"core": 1}, "dimension": 1}
SIGN = {"name": "sign", "pair": [1, 1], "reads": {}, "held": {**HELD, "sources": ["wronskian"]}}
SIGN["held"].update(level_weight=1, write_weight=1, act="rotation")
SHIPPED = ("rule", "light", "pair", "nuclide/deuteron", "charge/charged", "like_or_unlike/turning")
WRITES = {("charge/charged", "charge"): 4, ("like_or_unlike/turning", "charge"): 400}  # k_w = 4 E_h


def test_every_family_reads_the_holders_its_declaration_names_and_the_write_carries_its_weight():
    """The declaration's read (ALGEBRA.md, the owner's decision of 2026-10-02: every family reads the holders its declaration names, at the weights it names, and sources each at the weight it reads with) and the write weight (the holder's declared coefficient sits in the write): a universe of two holders of the content, `hollow` [1, 1] at the level weight 5 and the write weight 3 reading itself at 1, `core` [3, 4] at 7 and -1 reading nothing, and two real-line families of matter's pair, `stuff` reading `hollow` at 2 and `other` reading `core` at 1. On random levels of a periodic 3-cube: `stuff`'s content is 2 x hollow's time line and `other`'s core's, `core` reads 0 (the plain rule at Gamma) and every Link's factor is G^2; the rule of `stuff` is the law's line at the composed paces of 2 L; `hollow` is sourced by `stuff` alone and `core` by `other` alone (the reciprocity), each write's numerator the write weight times the reader's weight times its form scaled by the write's factor, 3 x 2 x D' and -1 x 1 x D', negative at some Node over the random levels, and the level gains (numerator + r) div (E_s T) with the remainder in [0, wall), a negative numerator taking the level down by the floor, the write back exact (a negative level read into a pace is the hill of the guard's test above, the clock Gamma (1 - 1 / Gamma)^c above Gamma for c below 0, admitted as it is within the edge). The start: `read_content` sums weight x (level + rest) over the reads with the row's own weight apart. The loader refuses by name a family without `reads` and a held row without `write_weight`, naming the family, a weight 0, a read of no held row, the holder of the sign naming itself and a real-line family naming a holder under the rotation; the energy line's gate (E_h T num = k_w Gamma den per plane family reading a holder under the rotation, the read weight cancelling under the reciprocity; the advisor's hand, #1563 comment 5945592281): a plane reading the holder at E_h = 1 and k_w = 1 is refused at T = 64 (1 x 64 x 4000 against 1 x Gamma x 6000) and passes at T = Gamma x 6000 / 4000 (every plane family of one universe sharing num / den, or the gate refuses the one out of the line by name); on a board of two Nodes with the sign holder at -5 and 5 the plane reading it at 1 under the act pace reads 5 at both, the size of the level, a hollow whatever its sense (ALGEBRA.md row (f); the advisor's hand, #1563 comment 5945859368), and under the rotation its turn's numerators are -5 and 5, the signed level, and its content read is the integer 0, the holder's level entering no content (the one declared act, the mathematician's 117 III); the rule's own universe at T 32,768 is not gated with the tests' charged row under the plain read, refused with it under the rotation at the write weight 1 and admitted at the advisor's k_w = 4 and T = 36,000; the shipped universe files restate the one read the loader derived before this round, every family of quanta reading every holder of the content at 1, a plane the holders of the sign at 1 too, a holder of the content itself among its reads and the holder of the sign none of the sign, every write weight 1 but the charged-body universes' sign holder at the energy line's 4 E_h."""
    integers, families = universe_of(universe(HOLLOW, CORE, STUFF, OTHER))
    hollow, core, stuff, other = range(4)
    reads = [[(r.family, r.weight) for r in f.reads] for f in families]
    assert reads == [[(0, 1)], [], [(0, 2)], [(1, 1)]] and readers_of(families, hollow) == [stuff]
    assert readers_of(families, core) == [other] and weight_of(hollow, families[stuff]) == 2
    draw, wrap, action = np.random.default_rng(7), Wrap(True, True, True), integers["quantum_action"]
    writes = {i: held_write(families, i, action) for i in (hollow, core)}
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
        by_hand = weights * node.written(forms[reader, 0], rulers[reader, 0], GAMMA, 2)
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
    unweighted = {**HOLLOW, "held": {"sources": ["form"], "level_weight": 5}}
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
    for name in SHIPPED:
        shipped = universe_of(json.loads((UNIVERSE.parent / f"{name}.json").read_text()))[1]
        held = [(i, f.wronskian) for i, f in enumerate(shipped) if f.held]
        for f in shipped:
            expected = sorted((i, 1) for i, sign in held if f.plane or not sign)
            assert sorted((r.family, r.weight) for r in f.reads) == expected, (name, f.name)
            assert f.write_weight == (WRITES.get((name, f.name), 1) if f.held else None), (name, f.name)
