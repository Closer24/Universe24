"""The read, its own folder (ALGEBRA.md #the-paces): the content as it is, no floor, the reads summed at their weights; the axis content rounded at the read; the guard at load on squares (the checkerboard factor at -2) admits and refuses by name, and the read in the interval carries no guard. The write's folder and the held write's (ALGEBRA.md #the-primitives, a family's write is one act; the row "the held write"): (numerator + r) div wall at every Node by Rule3's carried division, the remainder kept at the Node, forward then back exact, over many intervals the written total the numerator's within one unit; a held part gains the same division each interval and loses it back; the refusals by name. The start, its own folder (ALGEBRA.md #the-generator (g), the start): a held family's rest is the division act iterated from nothing until the levels repeat, 6 den b = num S_6(b) + 3 den sigma at the fine unit from the width, the levels its nearest integers; the refusals by name."""

import json
from fractions import Fraction

import numpy as np

from event_universe import flux, node, records
from event_universe.core import paces
from event_universe.core.ports import Wrap
from event_universe.core.rule3 import coefficients
from event_universe.features.held_write import held_write
from event_universe.features.read import (
    content_of,
    edge_squared,
    link_tension,
    paces_guard,
    stability_bound,
)
from event_universe.features.start.rests import read_content
from event_universe.features.write import carried
from event_universe.loader.derived import held_write_of, readers_of, weight_of
from event_universe.loader.universe import universe_of
from tests.laws import CHARGED, UNIVERSE, refused

GAMMA, SHAPE = 10_000, (3, 3, 3)
OWN = {"own_weight": 1, "intervals": paces.COUNT_POWER}  # a row reading its own level at 1, a count


def test_a_hill_enters_as_it_is_and_the_guard_refuses_a_pace_beyond_the_edge_by_name():
    """No floor and no clamp: a hill of 150 on [800, 850] (the edge's square 2 den Gamma^2 div (den + num) between 10,150^2 and 10,151^2) takes the clock's square to 10,151^2 and the load refuses it naming the Node; 75 passes as it is, the content -75, and the read alone never refuses; the same hill on one Link's content alone is caught on that Port as an integer pace; for den = num the edge is p <= Gamma exactly: a content of -1 refuses by name, a content at Gamma div 2 at both ends of every Link (the Link's pace at 0) refuses on the lower side and Gamma div 2 - 1 passes; for a negative numerator the band's lowest mode is at wave number 0 and the edge's square is 2 den Gamma^2 div (den + |num|), 21 for the pair [-1, 2] at Gamma = 4, so the audit's witness (#1583 B2), the content -1 with the clock's square 26 and 2 cos omega = -23 / 8 at k = 0, is refused by name where the edge of den + num (64) admitted it, and the vacuum of that pair passes. Three reads (2 a - 3 b + 4 c) sum per Node exactly; no reads give the integer 0 (the plain rule at Gamma); the Link's tension is SUM over the reads of (weight x (aa_i + aa_j) + 1) div 2, the mean of its two ends' parts, one division per read per Link: the ends 7 and 7 at the weight 1 give 7 and -7 and -7 give -7 (the Node's own part in a uniform level), the ends 7 and -7 give 0 and a second read of the ends 3 and 4 beside it 0 + 4. Forward the quotient and the remainder of numerator + r; back from the remainder after, the same quotient and the remainder before (the held write's write forward and back on numerators of both signs, the declaration's test below); a wall below 1 and a direction other than +1 or -1 are refused by name. The held write's write forward and back, with its weights, is the declaration's test below; a wall below 1 is refused by name."""
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
    refused("wall E_s T is from 1", held_write, 0, 1, 0, 0)


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
SIGN = {
    "name": "sign",
    "pair": [1, 1],
    "reads": {},
    "held": {"sources": ["wronskian"], "level_weight": 1},
}
TUBE, TURN = "charged", "turning"  # the charged universes at examples/events/, the tests' alone


def test_every_family_reads_the_holders_its_declaration_names_and_the_write_carries_its_weight():
    """The declaration's read (ALGEBRA.md, the owner's decision of 2026-10-02: every family reads the holders its declaration names, at the weights it names, and sources each at the weight it reads with) and the write weight (the holder's declared coefficient sits in the write): a universe of two holders of the content, `hollow` [1, 1] at the level weight 5 and the write weight 3 reading itself at 1, `core` [3, 4] at 7 and -1 reading nothing, and two real-line families of matter's pair, `stuff` reading `hollow` at 2 and `other` reading `core` at 1. On random levels of a periodic 3-cube: `stuff`'s content is 2 x hollow's time line and `other`'s core's, `core` reads 0 (the plain rule at Gamma) and every Link's factor is G^2; the rule of `stuff` is the law's line at the composed paces of 2 L; `hollow` is sourced by `stuff` alone and `core` by `other` alone (the reciprocity), each write's numerator the write weight times the reader's weight times its form scaled by the write's factor, 3 x 2 x D' and -1 x 1 x D', negative at some Node over the random levels, and the level gains (numerator + r) div (E_s T) with the remainder in [0, wall), a negative numerator absorption the level down by the floor, the write back exact (a negative level read into a pace is the hill of the guard's test above, the clock Gamma (1 - 1 / Gamma)^c above Gamma for c below 0, admitted as it is within the edge). The start: `read_content` sums weight x (level + rest) over the reads with the row's own weight apart. The loader refuses by name a family without `reads` and a held row without `write_weight`, naming the family, a weight 0, a read of no held row, the holder of the sign naming itself and a real-line family naming a holder under the rotation; the energy line's gate (E_h T num = k_w Gamma den per plane family reading a holder under the rotation, the read weight cancelling under the reciprocity; the advisor's hand, #1563 comment 5945592281): a plane reading the holder at E_h = 1 and k_w = 1 is refused at T = 64 (1 x 64 x 4000 against 1 x Gamma x 6000) and passes at T = Gamma x 6000 / 4000 (every plane family of one universe sharing num / den, or the gate refuses the one out of the line by name); on a board of two Nodes with the sign holder at -5 and 5 the plane reading it at 1 under the act pace reads 5 at both, the size of the level, a hollow whatever its sense (ALGEBRA.md row (f); the advisor's hand, #1563 comment 5945859368), and under the rotation its turn's numerators are -5 and 5, the signed level, and its content read is the integer 0, the holder's level entering no content (the one declared act, the mathematician's 117 III); the rule's own universe at T 32,768 is not gated with the tests' charged row under the plain read, refused with it under the rotation at the write weight 1 and admitted at the advisor's k_w = 4 and T = 36,000; the shipped universe files restate the one read the loader derived before this round, every family of quanta reading every holder of the content at 1, a plane the holders of the sign at 1 too, a holder of the content itself among its reads and the holder of the sign none of the sign, every write weight 1 but the charged-body universes' sign holder at the energy line's 4 E_h."""
    integers, families = universe_of(universe(HOLLOW, CORE, STUFF, OTHER))
    hollow, core, stuff, other = range(4)
    reads = [[(r.family, r.weight) for r in f.reads] for f in families]
    assert reads == [[(0, 1)], [], [(0, 2)], [(1, 1)]] and readers_of(families, hollow) == [stuff]
    assert readers_of(families, core) == [other] and weight_of(hollow, families[stuff]) == 2
    draw, wrap, action = np.random.default_rng(7), Wrap(True, True, True), integers["quantum_action"]
    writes = {i: held_write_of(families, i, action) for i in (hollow, core)}
    walls = [writes[i].walls if f.held else () for i, f in enumerate(families)]
    states = [records.empty_state(f, SHAPE, w, np.int64) for f, w in zip(families, walls, strict=True)]
    for state in states:
        levels = [draw.integers(1, 40, (2, *SHAPE)) for _ in state.lines]
        state.lines = [records.Record(*pair, 0 * SHAPE[0]) for pair in levels]
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
        _lines, (first, second) = flux.step_family(i, families, states, own, wrap, GAMMA)
        forms[i, 0] = records.form(first, second)  # the bookings per record, (family, record)
        rulers[i, 0] = node.rulers(i, families, states, 1, wrap, GAMMA)
    for held, reader, weights in ((hollow, stuff, 3 * 2), (core, other, -1 * 1)):
        numerators, walls, _weight = records.write_sources(
            held, families, forms, {}, writes[held], rulers, GAMMA
        )
        power = families[held].power  # one power on every booking: the form's own clock
        assert power == 1
        scaled, scale = records.rulers_write_factor(
            forms[reader, 0], rulers[reader, 0], GAMMA, power, True
        )
        by_hand = weights * scaled  # the carried factor: the product over the factor's wall at the Node
        assert len(numerators) == 1 and np.array_equal(numerators[0], by_hand) and (by_hand < 0).any()
        assert np.array_equal(walls[0], writes[held].walls[0] * scale)
        before, wall = states[held].lines[0], walls[0]
        remainder = [draw.integers(0, int(np.min(wall)), SHAPE)]
        (after,), (kept,) = node.held_write_at([before], numerators, [wall], remainder)
        total = np.asarray(by_hand + remainder[0], dtype=object)  # Python's integers at the fixed wall
        increment, left = total // wall, total % wall
        assert np.array_equal(after.now, before.now + increment) and np.array_equal(kept, left)
        (back,), (origin,) = node.held_write_at([after], numerators, [wall], [kept], -1)
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
    ):
        refused(reason, universe_of, universe(*rows))
    turning = universe_of(universe(SIGN, plane, quantum_action=15_000))[1]  # T 4,000 = Gamma 6,000
    two, level = np.zeros((2, 1, 1), dtype=np.int64), np.array([[[-5]], [[5]]], dtype=np.int64)
    board = [records.empty_state(f, (2, 1, 1), (), np.int64) for f in turning]
    board[0].lines[0] = records.Record(level, level, two)
    paced_read = node.read(1, turning, board, 1, wrap, GAMMA, 1)[0]
    turn = node.turning(1, turning, board, 1)
    assert np.asarray(turn[0]).ravel().tolist() == [
        -5,
        5,
    ]  # the turn by L, the holder of the sign's one act
    assert paced_read == 0  # the rotation: no level in the content
    rows = (rule := json.loads(UNIVERSE.read_text(encoding="utf-8")))["families"]
    rule["integers"]["quantum_action"] = (
        36_000  # T at which the law's alpha E_h T / Gamma is 6 (the charge's universality, 2026-10-24; E_h T num / (Gamma den) = 4 under the sentence of 2026-10-23, kept by name)
    )
    charge = next(
        f for f in universe_of({**rule, "families": [*rows, CHARGED]})[1] if f.name == "charge"
    )
    assert (charge.write_weight, charge.write_wall) == (
        6,
        1,
    )  # alpha carried inside the write, no pair in it, no gate
    for name in ("rule", "light", "pair", "deuteron", TUBE, TURN):
        integers, shipped = universe_of(json.loads((UNIVERSE.parent / f"{name}.json").read_text()))
        held = [(i, f.wronskian) for i, f in enumerate(shipped) if f.held]
        for index, f in enumerate(shipped):
            expected = sorted((i, 1) for i, sign in held if f.plane or not sign)
            assert sorted((r.family, r.weight) for r in f.reads) == expected, (name, f.name)
            if not (f.held and f.wronskian):
                assert f.write_weight == (1 if f.held else None), (name, f.name)
                continue
            planes = any(  # the planes reading the holder of the sign: one alpha per holder with any pairs under it (the charge's universality, 2026-10-24; E_h T num / (Gamma den) of 2026-10-23 kept by name)
                g.plane and any(r.family == index for r in g.reads) for g in shipped
            )
            alpha = Fraction(1)
            if planes:
                alpha = Fraction(f.level_weight * integers["quantum_action"], integers["node_clock"])
            assert Fraction(f.write_weight, f.write_wall) == alpha, (
                name,
                f.name,
            )  # E_h T / Gamma, no pair in it


def test_a_frozen_row_stands_outside_the_energy_line_and_two_moving_planes_still_share_their_pair():
    """The frozen row's exemption (ALGEBRA.md, the atom round's reading: the frozen-row nucleus [0, den] beside the electron's pair, the energy line's constraint that the plane families of one world share num / den lifted for num = 0 by name, the advisor's #1572 comment 5966780505 and the mathematician's 236 and 242, two hands): a universe of the sign holder under the rotation, a plane of matter's pair on the line (E_h T num = k_w Gamma den at T = 15,000) and a frozen plane [0, 6000] reading the holder at 1 loads, the frozen row's record never moving (R_ij = 2 num p^2 Q = 0 on every Link) and emission no light; the frozen row of three planes (the frozen proton's row) alike; a second moving plane whose num / den differs, [3000, 6000], is refused by name as before, and a frozen row under the plain read (the act `pace`) was never gated."""
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
    integers, families = universe_of(
        universe(SIGN, plane, moving, quantum_action=15_000)
    )  # two moving planes of different pairs under one holder load (the charge's universality, 2026-10-24; the refusal "one ratio per holder" of 2026-10-23 kept by name)
    assert (families[0].write_weight, families[0].write_wall) == (
        3,
        2,
    )  # alpha = E_h T / Gamma = 15,000 / 10,000 reduced, no pair in it
    universe_of(universe({**SIGN, "held": {**SIGN["held"]}}, plane, frozen))


def test_the_writes_room_under_a_negative_tension_is_the_larger_of_the_hills_and_the_tensions():
    """The register's room under a negative tension (ALGEBRA.md, The write per proper volume and per proper interval; the mathematician's 268 and the advisor's second with one precision, #1572 comments 5969128707 and 5969197876, two hands): the guard bounds p_i^2 Q_ij and not the Link's factor q = Gamma - t, so under a negative tension q exceeds Gamma, up to q_max = Gamma + W A, the sum of W_a A over the held rows with axis lines a source reads, and the write's factor in a hollow reaches (P / Gamma)^3 sqrt(q_max / P) on a count and (P / Gamma)^3 q_max / P on a Wronskian, beyond the hill's room (P / Gamma)^3 rounded up. At the rule's universe (Gamma 6,000, W 1, the hill's own bound A_1 = 9,266, q_max 15,266) the law's ceilings are 3 on a count and 4 on a Wronskian for matter's pair (P 6,572; the register's values 2.003 and 3.053 against the hill's room 2) and 2 and 3 for the three massless pairs (P 6,000; 1.595 and 2.544 against 1): `tension_room` returns them and exceeds `hill_scale` exactly where the register's values exceed it; the four shipped universes' bound stays 9,266, the write's total not their binding term; a universe where it is, a holder of the massless pair with axis lines at the write weight 10^6 read by one real line at 1 (Gamma 10,000, T 64, the width 63), has the hill's bound 2,147,483, isqrt((2^63 - 1 - 64) div (10^6 x 2 x 1)), and under the rooms 554,477, the tension's room 15 at q_max = 10,000 + 2,147,483, smaller by name."""
    from math import ceil, isqrt

    from event_universe.loader import derived, rooms

    gamma, hill_bound = (
        6000,
        6949,
    )  # the engine's bound for the flux line's partial sums (ENGINE.md, The amplitude bound)
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
        assert [round(v, 3) for v in values] == ([1.845, 2.589] if matter else [1.469, 2.158])
        assert (hill, count, wronskian) == ((2, 2, 3) if matter else (1, 2, 3))
        assert all(value > hill - 1 for value in values) and rooms.hill_scale(pair, gamma) == hill
        assert (
            rooms.tension_room(pair, gamma, q_max, False) == count >= hill
        )  # equal at matter's pair at A = 6,949
        assert rooms.tension_room(pair, gamma, q_max, True) == wronskian > hill
    for name in ("rule", "light", "ghz", "pair"):
        integers, families = universe_of(json.loads((UNIVERSE.parent / f"{name}.json").read_text()))
        keys = ("node_clock", "quantum_action", "width", "link_unit")
        assert derived.amplitude_bound(families, *(integers[key] for key in keys)) == hill_bound, name
    axes = {"sources": ["form", "tensions"], "level_weight": 1, "write_weight": 10**6}
    well = {"name": "well", "pair": [1, 1], "reads": {"well": 1}, "held": axes}
    deep = {**well, "name": "deep", "reads": {"deep": 1}, "held": {**axes, "write_weight": 1}}
    line = {"name": "line", "pair": [1, 1], "reads": {"well": 1}, "dimension": 1}
    families = universe_of(universe(well, line))[1]
    largest, wall, room = (
        2**63 - 1,
        1 * 64,
        10**6 * 1 * 2 * 2 * 1,
    )  # E_s T; k_w x W x two products x the centred difference's 2 x the hill's 1 (The stress is the Links', 2026-10-23: the tension's part the centred difference squared at the doubled wall; 10^6 x 2 before)
    under_the_hill = isqrt((largest - wall) // room)
    tension = ceil(
        Fraction(GAMMA**2 * (GAMMA + under_the_hill), GAMMA**3)
    )  # one power: the factor q_max itself
    under_the_rooms = isqrt((largest - wall) // (room * tension))
    assert (under_the_hill, tension, under_the_rooms) == (
        1_518_500,
        153,
        122_763,
    )  # (2_147_483, 216, 146_117) before the Links' stress
    assert derived.bound_under_rooms(families, GAMMA, 64, 63, 1, None) == under_the_hill
    assert (
        derived.amplitude_bound(families, GAMMA, 64, 63) == 173_613 < under_the_hill
    )  # as read under the Links' stress (2026-10-23); the hand's formula gives under_the_rooms 122,763 (146,117 before), the room's re-derivation under the doubled wall open
    two = universe_of(universe(well, deep, {**line, "reads": {"well": 1, "deep": 2}}))[1]
    assert rooms.factor_bound(two, 2, GAMMA, 7) == GAMMA + (1 + 2) * 7  # the two rows read, summed
