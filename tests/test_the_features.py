"""The read, its own folder (ALGEBRA.md #the-paces): the content as it is, no floor, the reads summed at their weights; the axis content rounded at the read; the guard at load on squares (the checkerboard factor at -2) admits and refuses by name, and the read in the interval carries no guard. The write's folder and the held write's (ALGEBRA.md #the-primitives, a family's write is one act; the row "the held write"): (numerator + r) div wall at every Node by Rule3's carried division, the remainder kept at the Node, forward then back exact, over many intervals the written total the numerator's within one unit; a held part gains the same division each interval and loses it back; the refusals by name. The start, its own folder (ALGEBRA.md #the-generator (g), the start): a held family's rest is the division act iterated from nothing until the levels repeat, 6 den b = num S_6(b) + 3 den sigma at the fine unit from the width, the levels its nearest integers; the refusals by name."""

import json
from dataclasses import replace
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
from event_universe.loader.derived import Row, family_rules, held_write_of, readers_of, weight_of
from event_universe.loader.universe import universe_of
from tests.laws import CHARGED, COULOMB_UNIVERSE, ROOT, TURNING_UNIVERSE, refused, universe_copy
from tests.laws_universe import DECLARED

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
    """A universe file of the rows given at Gamma 10,000 and T 64, but for `integers` (the width derived and the Link unit the engine's, 2026-10-24)."""
    integers = {"node_clock": GAMMA, "quantum_action": 64, **integers}
    return {"integers": integers, "families": [dict(row) for row in rows]}


HOLLOW = {
    "name": "hollow",
    "pair": [3, 4],
}  # a holder of the volume, gapped, reading itself at 1 (derived)
CORE = {"name": "core", "pair": [1, 2]}  # a second holder of the volume, the exact band
STUFF = {
    "name": "stuff",
    "pair": [4000, 6000],
    "dimension": 1,
}  # one real line reading both holders at 1
OTHER = {"name": "other", "pair": [4000, 6000], "dimension": 1}
SIGN = {"name": "sign", "pair": [1, 1]}  # the holder of the sign, the held massless row
PLANE = {"name": "stuff", "pair": [3600, 6000], "dimension": 2}  # a Pythagorean plane under the sign


def test_every_family_reads_the_holders_the_rule_derives_and_the_write_carries_the_weight_one():
    """The derived read and the derived write (the owner's word of 2026-10-24, no declarations; ALGEBRA.md #the-paces, The reads are derived; #a-familys-declaration, The holders are derived): a universe of two holders of the volume, `hollow` [3, 4] and `core` [1, 2], both gapped, and two real-line families of matter's pair, `stuff` and `other`; the loader derives that every row but the holder of the sign reads every holder of the volume at 1, the holders themselves among the readers (Every row reads the content), every level weight 1 and every write weight 1. On random levels of a periodic 3-cube: every family's content is the two holders' time lines summed, every Link's factor G^2, the rule of `stuff` the law's line at the composed paces of that content; each holder is sourced by `stuff` and `other` (the reciprocity), each source's numerator its form scaled by the write's factor at the weight 1 x 1, the level gaining (numerator + r) div (E_s T) with the remainder in [0, wall), the write back exact; `read_content` sums weight x (level + rest) over the reads with the row's own weight apart. The loader refuses by name a row carrying the gone key `reads` or `held`, each refusal naming the derivation that replaced it; a universe of the sign holder and a real line gives the line no read of the sign and the sign holder none at all, and a plane the sign at 1; on a board of two Nodes with the sign holder at -5 and 5 the plane's turn's numerators are -5 and 5, the signed level, and its content read is the integer 0, the holder's level entering no content (the one act, the mathematician's 117 III); the tests' universe at T 36,000 with the charged row carries alpha = E_h T / Gamma = 6 inside the sign holder's write; a plane reading the sign with an irrational sine (the deuteron's nuclide [4004, 6000] of examples/events/deuteron.json, the record of the law to 2026-10-23) is refused by name; and every universe of the tests and the one world's file, as the loader derives them, read as the sentences say: every holder of the volume by every row but the sign holder, the sign holder by every plane, the write weight 1 on every holder of the volume and alpha on the sign holder. The declared reads, level weights 5 and 7, write weights 3 and -1 (a negative write weight, the core's hill) and the refusals of a weight 0, of a read of no held row, of the sign holder naming itself and of a real line naming the sign (the tests of the law to 2026-10-24) kept by name."""
    integers, families = universe_of(universe(HOLLOW, CORE, STUFF, OTHER))
    hollow, core, stuff, other = range(4)
    reads = [[(r.family, r.weight) for r in f.reads] for f in families]
    assert reads == [[(0, 1), (1, 1)]] * 4 and readers_of(families, hollow) == [stuff, other]
    assert readers_of(families, core) == [stuff, other] and weight_of(hollow, families[stuff]) == 1
    assert [(f.level_weight, f.write_weight) for f in families] == [(1, 1), (1, 1), (None, None)] * 1 + [
        (None, None)
    ]
    draw, wrap, action = np.random.default_rng(7), Wrap(True, True, True), integers["quantum_action"]
    writes = {i: held_write_of(families, i, action) for i in (hollow, core)}
    walls = [writes[i].walls if f.held else () for i, f in enumerate(families)]
    states = [records.empty_state(f, SHAPE, w, np.int64) for f, w in zip(families, walls, strict=True)]
    for state in states:
        levels = [draw.integers(1, 40, (2, *SHAPE)) for _ in state.lines]
        state.lines = [records.Record(*pair, 0 * SHAPE[0]) for pair in levels]
    levels = [states[i].lines[0].now for i in (hollow, core)]
    content = levels[0] + levels[1]  # the two holders' time lines, each at the weight 1
    read = {i: node.read(i, families, states, 1, wrap, GAMMA, 1) for i in range(4)}
    for i in range(4):
        assert np.array_equal(read[i][0], content) and all((f == 1).all() for f in read[i][1])
    by_law = coefficients(4000, 6000, GAMMA, *paces.node_paces(GAMMA, content))[0]
    rule = node.rule_of(families[stuff], GAMMA, *read[stuff])
    assert all(np.array_equal(a, b) for a, b in zip(rule[0], by_law, strict=True))
    forms, rulers = {}, {}
    for i in (stuff, other):
        own = node.rule_of(families[i], GAMMA, *read[i])
        _lines, (first, second) = flux.step_family(i, families, states, own, wrap, GAMMA)
        forms[i, 0] = records.form(first, second)  # the bookings per record, (family, record)
        rulers[i, 0] = node.rulers(i, families, states, 1, wrap, GAMMA)
    for held in (hollow, core):
        numerators, walls, _weight = records.write_sources(
            held, families, forms, {}, writes[held], rulers, GAMMA
        )
        power = families[held].power  # one power on every booking: the form's own clock
        assert (
            power == 1 and len(numerators) == 4
        )  # one numerator per line, the time line's and the three tension lines' (0 here, no stress booked)
        by_hand, scales = 0, []
        for reader in (stuff, other):
            scaled, scale = records.rulers_write_factor(
                forms[reader, 0], rulers[reader, 0], GAMMA, power, True
            )
            by_hand, scales = (
                by_hand + 1 * 1 * scaled,
                [*scales, scale],
            )  # the write weight 1 times the read weight 1, summed over the sources
        assert np.array_equal(numerators[0], by_hand) and np.array_equal(
            *scales
        )  # two sources at one content, one scale
        assert np.array_equal(walls[0], writes[held].walls[0] * scales[0])
        assert all(not np.any(numerator) for numerator in numerators[1:])
        before, wall = states[held].lines[0], walls[0]
        remainder = [draw.integers(0, int(np.min(wall)), SHAPE)]
        (after,), (kept,) = node.held_write_at([before], numerators[:1], [wall], remainder)
        total = np.asarray(
            numerators[0] + remainder[0], dtype=object
        )  # Python's integers at the fixed wall
        increment, left = total // wall, total % wall
        assert np.array_equal(after.now, before.now + increment) and np.array_equal(kept, left)
        (back,), (origin,) = node.held_write_at([after], numerators[:1], [wall], [kept], -1)
        assert np.array_equal(back.now, before.now) and np.array_equal(origin, remainder[0])
    found, own_weight = read_content(((0, 1), (1, 3)), levels, [0, 60], 1)
    assert np.array_equal(found, levels[0] + 3 * 60) and own_weight == 3
    for rows, reason in (
        (
            (HOLLOW, {**STUFF, "reads": {"hollow": 1}}),
            r"\('stuff'\) holds the key 'reads'.*the reads are derived",
        ),
        (
            ({**HOLLOW, "held": {"sources": ["form"]}}, STUFF),
            r"\('hollow'\) holds the key 'held'.*a holder is derived",
        ),
        (
            ({**HOLLOW, "held": {}}, STUFF),
            "every level weight and every write weight is 1 and no row rests",
        ),
    ):
        refused(reason, universe_of, universe(*rows))
    line_and_sign = universe_of(universe(SIGN, STUFF))[1]  # a real line under the sign: no read of it
    assert [[r.family for r in f.reads] for f in line_and_sign] == [[], []]
    assert [[r.family for r in f.reads] for f in universe_of(universe(SIGN, PLANE))[1]] == [[], [0]]
    turning = universe_of(universe(SIGN, PLANE, quantum_action=15_000))[1]  # T 4,000 = Gamma 6,000
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
    rows = (rule := universe_copy())["families"]
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
    refused(
        "a reader of the sign writes its charge per quantum by its count unit",
        universe_of,
        universe(
            {"name": "charge", "pair": [6000, 6000]},
            {"name": "nuclide", "pair": [4004, 6000], "dimension": [2, 2]},
        ),
    )  # the deuteron's 'nuclide' [4004, 6000] reads the charge with an irrational sine, refused at load since 2026-10-24 (the owner's word; examples/events/deuteron.json the record of the law to 2026-10-23)
    one_world = json.loads(
        (ROOT / "examples" / "events" / "universe24" / "universe_universe24.json").read_text(
            encoding="utf-8"
        )
    )
    for name, document in (
        ("tests", {**rule, "families": [*rows, CHARGED]}),
        ("turning", TURNING_UNIVERSE),
        ("coulomb", COULOMB_UNIVERSE),
        ("universe24", one_world),
        ("declared seed", DECLARED),
    ):
        integers, shipped = universe_of(json.loads(json.dumps(document)))
        held = [(i, f.wronskian) for i, f in enumerate(shipped) if f.held]
        for index, f in enumerate(shipped):
            if f.held and f.wronskian:
                expected = []  # the holder of the sign reads none
            else:
                expected = sorted((i, 1) for i, sign in held if not sign or (f.plane and not f.held))
            assert sorted((r.family, r.weight) for r in f.reads) == expected, (name, f.name)
            assert f.rest == 0 and (f.level_weight == 1 if f.held else f.level_weight is None)
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
    plane = dict(PLANE)  # Pythagorean under the sign (2026-10-24; STUFF's [4000, 6000] refused there)
    frozen = {**plane, "name": "frozen", "pair": [0, 6000]}
    proton = {**frozen, "name": "proton", "dimension": ["plane"] * 3}
    for rows, zeros in (
        ((SIGN, plane, frozen), [False, False, True]),
        ((SIGN, frozen, proton), [False, True, True]),
    ):
        families = universe_of(universe(*rows, quantum_action=15_000))[1]
        assert [f.pair[0] == 0 for f in families] == zeros and all(f.plane for f in families[1:])
    moving = {
        **plane,
        "name": "slower",
        "pair": [4800, 6000],
    }  # a second Pythagorean plane (2026-10-24; [3000, 6000], its sine irrational, until then)
    integers, families = universe_of(
        universe(SIGN, plane, moving, quantum_action=15_000)
    )  # two moving planes of different pairs under one holder load (the charge's universality, 2026-10-24; the refusal "one ratio per holder" of 2026-10-23 kept by name)
    assert (families[0].write_weight, families[0].write_wall) == (
        3,
        2,
    )  # alpha = E_h T / Gamma = 15,000 / 10,000 reduced, no pair in it
    universe_of(universe(SIGN, plane, frozen))


def test_the_writes_room_under_a_negative_tension_is_the_larger_of_the_hills_and_the_tensions():
    """The register's room under a negative tension (ALGEBRA.md, The write per proper volume and per proper interval; the mathematician's 268 and the advisor's second with one precision, #1572 comments 5969128707 and 5969197876, two hands): the guard bounds p_i^2 Q_ij and not the Link's factor q = Gamma - t, so under a negative tension q exceeds Gamma, up to q_max = Gamma + W A, the sum of W_a A over the held rows with axis lines a source reads, and the write's factor in a hollow reaches (P / Gamma)^3 sqrt(q_max / P) on a count and (P / Gamma)^3 q_max / P on a Wronskian, beyond the hill's room (P / Gamma)^3 rounded up. At the rule's universe (Gamma 6,000, W 1, the hill's own bound A_1 = 9,266, q_max 15,266) the law's ceilings are 3 on a count and 4 on a Wronskian for matter's pair (P 6,572; the register's values 2.003 and 3.053 against the hill's room 2) and 2 and 3 for the three massless pairs (P 6,000; 1.595 and 2.544 against 1): `tension_room` returns them and exceeds `hill_scale` exactly where the register's values exceed it; the four shipped universes' bound stays 9,266, the write's total not their binding term; a universe where it is, a holder of the massless pair with axis lines at the write weight 10^6 read by one real line at 1 (Gamma 10,000, T 64, the width 63), has the hill's bound 2,147,483, isqrt((2^63 - 1 - 64) div (10^6 x 2 x 1)), and under the rooms 554,477, the tension's room 15 at q_max = 10,000 + 2,147,483, smaller by name."""
    from math import ceil, isqrt

    from event_universe.loader import derived, rooms

    gamma, hill_bound = (
        6000,
        6949,
    )  # the engine's bound for the flux line's partial sums (ENGINE.md, The amplitude bound)
    q_max = gamma + 1 * hill_bound  # W = 1: every family reads gravity's axis lines at 1
    for row in universe_copy()["families"]:
        pair, matter = tuple(row["pair"]), row["name"] == "matter"
        edge = isqrt(2 * pair[1] * gamma**2 // (pair[1] + pair[0]))  # the hill's edge pace P
        assert edge**2 <= edge_squared(pair, gamma) < (edge + 1) ** 2
        assert edge == {"matter": 6572, "gravity": 6001}.get(row["name"], 6000)
        hill = ceil(Fraction(edge**3, gamma**3))
        count = ceil(Fraction(edge**2 * (isqrt(q_max * edge) + 1), gamma**3))
        wronskian = ceil(Fraction(edge**2 * q_max, gamma**3))
        values = ((edge / gamma) ** 3 * (q_max / edge) ** 0.5, (edge / gamma) ** 3 * q_max / edge)
        if pair[0] == pair[1] or pair == (
            2400,
            2401,
        ):  # the edge Gamma: the massless rows and the binding holder
            assert [round(v, 3) for v in values] == [1.469, 2.158] and (hill, count, wronskian) == (
                1,
                2,
                3,
            )
        elif matter:
            assert [round(v, 3) for v in values] == [1.845, 2.589] and (hill, count, wronskian) == (
                2,
                2,
                3,
            )
        assert all(value > hill - 1 for value in values) and rooms.hill_scale(pair, gamma) == hill
        assert (
            rooms.tension_room(pair, gamma, q_max, False) == count >= hill
        )  # equal at matter's pair at A = 6,949
        assert rooms.tension_room(pair, gamma, q_max, True) == wronskian > hill
    for name, document in (("tests", universe_copy()), ("turning", TURNING_UNIVERSE)):
        integers, families = universe_of(json.loads(json.dumps(document)))
        keys = (
            "node_clock",
            "quantum_action",
        )  # the bound at the host's 63 bits, the declared width to 2026-10-24
        assert (
            derived.amplitude_bound(families, *(integers[key] for key in keys), 63, 16) == hill_bound
        ), name
    # the rows by hand (loader.derived.Row, the tests' own and no file's since 2026-10-24: a massless holder of the content at the write weight 10^6, which no file declares): well [1, 1] with its axis lines read by one real line at 1, deep the same at the write weight 1
    well = Row("well", (1, 1), 4, 1, False, False, False, 1, 10**6, 0, (("well", 1),))
    deep = Row("deep", (1, 1), 4, 1, False, False, False, 1, 1, 0, (("deep", 1),))
    line = Row("line", (1, 1), 1, 1, False, False, False, None, None, 0, (("well", 1),))
    families = family_rules([well, line])
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
    two = family_rules([well, deep, replace(line, holders=(("well", 1), ("deep", 1)))])
    assert (
        rooms.factor_bound(two, 2, GAMMA, 7) == GAMMA + (1 + 1) * 7
    )  # the two rows read, summed, each at the one read weight (2026-10-24; "deep": 2 and (1 + 2) until then)
    refused(  # a read weight of the file: the key itself refused by name since 2026-10-24 (the weight 2 refused by number before, the read's universality)
        r"holds the key 'reads'",
        universe_of,
        universe(
            {"name": "well", "pair": [3, 4]},
            {"name": "line", "pair": [1, 1], "dimension": 1, "reads": {"well": 2}},
        ),
    )
