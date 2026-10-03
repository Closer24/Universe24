"""The count is the record's share (ALGEBRA.md #the-count-is-the-records-share): the share e_i = 3 den (now^2 + before^2) - num now S_6(before) changes over one step of Rule3 by exactly SUM_j F_ij, F_ij = num (now_i before_j - before_i now_j), at the pair the step started from, in rationals; in integers the identities carry Rule3's remainder term and the reader's own floor, the audit's exact witnesses pinned (#1582, #1583, #1579); the engine reads the same currents from the record and a node_reader's click is its net front inflow, never a Node; the exact bands (ALGEBRA.md #rule3): 2 cos omega an integer gives the periods 6, 4 and 3 with no remainder."""

from fractions import Fraction

import numpy as np

from event_universe import credit, node, share
from event_universe.core import paces, ports
from event_universe.core.ports import Wrap
from event_universe.core.rule3 import coefficients, form_term, rule3
from event_universe.features.read import edge_squared, guard
from event_universe.game_board import GameBoard
from event_universe.loader.derived import family_rules
from event_universe.loader.world import kind_of
from event_universe.reports import inflow
from event_universe.world_files import load_world
from tests.laws import EVENTS, real_rows

RING, HERE, GAMMA = Wrap(True, True, True), (1, 1, 1), 6000  # the witnesses at the rule's Gamma


def test_the_integer_identities_carry_their_remainder_terms_and_the_readers_floor():
    """The share's change is the currents at the pair the step started from (issue #1495 finding 6; the paper writer's finding, #1538 comment 5921398465) and not at the pair it left, and the audit's exact witnesses, each the engine's own integers against the law's rational identity, so that an exact-equality wording cannot return (#1582; #1583 B1 to B3; #1579). (a) At equal paces (pair [1, 1], Gamma 5, the content 1, the Node at -3 / -3 with its three + neighbours at -3) the integer share goes 54 to 26: the currents -27, Rule3's remainder term -3 (next - before) (r' - r) / P^2 = -2 / 3, and the reader's own floor residual, frac(q(now, before)) - frac(q(next, now)) = -1 / 3 with q the weighted Node term before its floor, strictly between -1 and 1 per Node and level pair, the identity exact with it. (b) The vacuum witness, pair [2, 3] at Gamma 6,000 from now 1 and before 0: next 1 with r' = 216,000,000, the share 9 to 6 with no current, Rule3's term rho = (r - r') / (2 Gamma^2) = -3 (over Gamma^2 alone it would read -6), the line 6 den Gamma^2 (next + before) = 2 num Gamma^2 S_6(now) + r - r' exact. (c) The Wronskian under the integer step (#1579): at [2, 3] the parts (1, 3) from zeros step to (1, 4) and W from 0 to -1, exactly the remainder term eps_re im_now - eps_im re_now with eps = (r - r') / w, under |re_now| + |im_now| per Node and interval, the inverse exact; at [1, 2] the parts stand and W stays 0 (the divisible control): the integer W is conserved up to that term and no quadratic form of the levels and remainders is conserved exactly (the second mathematician, #1572 comment 5932042343), so every test of a conserved quantity asserts a bound, never exactness. (d) The band's edge (B2): light's checkerboard at wave number pi on every axis reads 2 cos omega = -2 exactly, a repeated root the guard admits at p = Gamma, and the line grows it linearly, (-1)^t (t + 1) with the remainder 0, so the guard excludes exponential growth and does not bound the record; the same checkerboard with before = -now has the share 0 at every Node, a null mode that is no static uniform record. (e) The conserved form's domain (B1): at Node-isotropic paces the weighted form E with the Node weights 1 / p_i^2 is conserved exactly by the unrounded line, on the audit's 2 x 1 x 1 light board at Gamma 2 with the paces 2 and 1 (M = [[4 / 3, 2 / 3], [1 / 6, 11 / 6]]) E standing at 6 while the unweighted D falls from 1 to 11 / 12, and on the 2 x 2 x 1 square with p_x(A) = 2 among paces 1 the product of M_ij / M_ji around the square is 4, so no positive Node weight symmetrises a read booked per Node per axis. The exact bands beside them: a Node at rest in the vacuum turns by 2 cos omega = 2 num / den, the three integer rotations 1, 0 and -1 closing in 6, 4 and 3 intervals with the remainder 0 at every step. The corner's reads carry the x Links' factor 4 at the pace 1 against the plain reads."""
    zero, ones = np.zeros((3, 3, 3), dtype=np.int64), np.ones((3, 3, 3), dtype=np.int64)
    rule = coefficients(1, 1, 5, *paces.node_paces(5, 1))  # the clock 4, the pace 3: R 18, S 192, w 150
    now, before = zero.copy(), zero.copy()
    now[1, 1, 1] = now[2, 1, 1] = now[1, 2, 1] = now[1, 1, 2] = before[1, 1, 1] = -3
    after = node.step(record := node.Record(now, before, zero), rule, RING)
    weight = 2 * paces.link_pace(5, 1) ** 2  # the share's wall 2 p_i^2 G^2 = 18 at the Node's pace 3
    shares = [int(share.share((1, 1), r, RING, 5, 1)[HERE]) for r in (record, after)]
    currents = sum(int(f[HERE]) for f in node.currents_of(1, [record], RING))
    nxt, carried = int(after.now[HERE]), int(after.remainder[HERE])
    unfloored = [Fraction(form_term(rule[1], rule[2], a, -3), weight) for a in (-3, nxt)]
    residual = unfloored[0] % 1 - unfloored[1] % 1
    assert (nxt, carried, shares, currents, residual) == (-2, 12, [54, 26], -27, Fraction(-1, 3))
    assert sum(int(f[HERE]) for f in node.currents_of(1, [after], RING)) != currents  # not the pair left
    assert shares[1] - shares[0] == currents + Fraction(-(nxt + 3) * carried, weight) + residual
    record, rule = node.Record(ones, zero, zero), coefficients(2, 3, GAMMA, GAMMA, GAMMA)
    after = node.step(record, rule, RING)
    nxt, carried = int(after.now[HERE]), int(after.remainder[HERE])
    shares = [int(share.share((2, 3), r, RING, GAMMA)[HERE]) for r in (record, after)]
    assert (nxt, carried, rule[2], shares) == (1, 216_000_000, 648_000_000, [9, 6])
    assert not any(f[HERE] for f in node.currents_of(2, [record], RING))
    assert Fraction(-carried, 2 * GAMMA**2) == shares[1] - shares[0] == -3
    assert rule[2] * (nxt + 0) == 2 * 2 * GAMMA**2 * 6 + 0 - carried
    for pair, levels, turned in (((2, 3), [1, 4], -1), ((1, 2), [1, 3], 0)):
        rule = coefficients(*pair, GAMMA, GAMMA, GAMMA)
        lines = [node.Record(ones, zero, zero), node.Record(3 * ones, zero, zero)]
        after = [node.step(line, rule, RING) for line in lines]
        eps = [Fraction(-int(a.remainder[HERE]), rule[2]) for a in after]  # (r - r') / w from r = 0
        found = int(node.wronskian(after, True)[HERE])
        assert ([int(a.now[HERE]) for a in after], found) == (levels, turned)
        assert found == eps[0] * 3 - eps[1] * 1 and abs(found) < 1 + 3
        back = [node.step(a, rule, RING, -1) for a in after]
        assert [int(b.now[HERE]) for b in back] == [1, 3] and not any(b.remainder.any() for b in back)
    rule = coefficients(1, 1, GAMMA, GAMMA, GAMMA)
    assert Fraction(rule[1] - 6 * rule[0][0], rule[2]) == -2 and edge_squared((1, 1), GAMMA) == GAMMA**2
    guard((1, 1), GAMMA, 1, 0, (1,) * 6, "light")  # the edge admitted: the clock and the paces at Gamma
    record = node.Record(parity := (-1) ** np.indices((2, 2, 2)).sum(0), 0 * parity, 0 * parity)
    for t in range(1, 7):
        record = node.step(record, rule, RING)
        assert np.array_equal(record.now, (-1) ** t * (t + 1) * parity) and not record.remainder.any()
    assert not share.share((1, 1), node.Record(parity, -parity, 0 * parity), RING, GAMMA).any()
    at = (2, 1)  # Gamma 2: the Node's pace 2 at A and 1 at B on a chain of two, the clock 2
    rules = [coefficients(1, 1, 2, 2, p) for p in at]
    wall, reads, selfs = rules[0][2], [r[0][0] for r in rules], [r[1] for r in rules]
    own = [Fraction(selfs[i] + 4 * reads[i], wall) for i in range(2)]  # M_ii, four self reads
    link = [Fraction(2 * reads[i], wall) for i in range(2)]  # M_ij, the two reads of the neighbour
    assert (own, link) == ([Fraction(4, 3), Fraction(11, 6)], [Fraction(2, 3), Fraction(1, 6)])
    states = [([Fraction(1), Fraction(0)], [Fraction(0), Fraction(0)])]  # (now, before) at A and B
    for _ in range(2):
        x, y = states[-1]
        states.append(([own[i] * x[i] + link[i] * x[1 - i] - y[i] for i in range(2)], x))
    for k, (unweighted, weighted) in enumerate(((1, 6), (Fraction(11, 12), 6))):  # D falls, E stands
        (x, y), (nxt, _) = states[k], states[k + 1]
        node_terms = [Fraction(form_term(selfs[i], wall, x[i], y[i]), at[i] ** 2) for i in range(2)]
        assert sum(a * a for a in x) - sum(a * b for a, b in zip(nxt, y, strict=True)) == unweighted
        assert sum(node_terms) - 2 * sum(x[i] * (4 * y[i] + 2 * y[1 - i]) for i in range(2)) == weighted
    corner, rest = (coefficients(1, 1, 2, 2, 1, f)[0] for f in ((4, 4, 1, 1, 1, 1), (1,) * 6))
    assert Fraction(corner[0], rest[0]) * Fraction(rest[2], corner[2]) == 4  # around the square
    for pair, period in (((1, 2), 6), ((0, 1), 4), ((-1, 2), 3)):
        (read, *_), self_coefficient, wall = coefficients(*pair, GAMMA, GAMMA, GAMMA)
        before, now = 0, 1_000
        for _ in range(period):
            nxt, carry = rule3((read,) * 3, (2 * now,) * 3, self_coefficient, wall, now, before, 0)
            assert carry == 0
            before, now = now, nxt
        assert (before, now) == (0, 1_000)


def test_the_engine_reads_the_currents_from_the_record_through_the_six_ports():
    """The currents the engine reads (`node.currents_of`) are F_ij = num (now_i before_j - before_i now_j) through each Port, both level pairs added, on the record as it stands and nothing kept beside it. The click (ALGEBRA.md #the-count-is-the-records-share; the owner's word of 2026-09-30, no click names a Node): a node_reader's Nodes are one region; its report is the net current into it through the Ports leading in from the declared board outside the region, signed, in the current's units, and none through a Port between two of its Nodes (a hop inside the region is no entry) nor through a Port beyond the board. On the chain of three with every Node declared and none grown: +x from Node 2 is outside the region; -x from Node 0 inside it is a hop, no entry; +y beyond the board has no boundary Port."""
    (quanta,) = family_rules(real_rows(("quanta", (5, 7), 1, None)))
    draw, shape, wrap = np.random.default_rng(2), (3, 3, 3), Wrap(True, True, True)
    zero = node.zeros(shape, kind_of(63))
    real, second = (node.Record(*draw.integers(-50, 50, (2, *shape)), zero) for _ in range(2))
    through = node.currents_of(quanta.pair[0], [real, second], wrap)
    for port, (axis, side) in enumerate((a, s) for a in range(3) for s in (1, -1)):
        rolled = [(r, *(np.roll(a, -side, axis) for a in (r.now, r.before))) for r in (real, second)]
        expected = sum(5 * (r.now * before - r.before * now) for r, now, before in rolled)
        assert np.array_equal(through[port], expected)
    nodes, board = np.array([True, True, False]).reshape(3, 1, 1), np.ones((3, 1, 1), dtype=bool)
    wrap, zero = Wrap(False, False, False), np.zeros((3, 1, 1), dtype=np.int64)
    inward = np.array([0, 40, 0]).reshape(3, 1, 1)  # a current into Node 1 through one Port
    through = [tuple(inward if p == port else zero for p in range(6)) for port in range(3)]
    assert [inflow(nodes, t, wrap, nodes, board) for t in through] == [40, 0, 0]


def test_the_steps_shortened_reads_equal_the_full_reads_bit_for_bit():
    """The step's speed (the owner's word of 2026-10-03, 15:12 Israel, in the Boss's session, "let them do it"; #1745 item 10; branch step-speed: the node_readers' regions and fronts read once per interval for every family, the share at the Nodes where a level stands, the write factor in the hardware's integers where its product stays inside the width, the Port's fill on the one layer beyond a face; no integer moved): every shortened read equals the full read it replaced, bit for bit. (i) `share.share` at its default mask equals the share at every Node, and `GameBoard.quanta` at the instrument's Nodes equals the full reading there, on the Zeno box, the resonance world, the shelved ion and the anticoincidence world over 24 intervals, every family. (ii) `paces.write_factor` in the hardware's integers, where `within_width` admits the product, equals the rounding in Python's integers on counts around the width's edge, both branches taken. (iii) `ports.shifted` with the fill on the face layer equals the shift with a full fill on every axis, sign and wrap, and a folded axis returns the array."""
    worlds = (("zeno", "zeno_1"), ("resonance", "resonant"), ("shelved_ion", "shelved_ion"))
    for folder, name in (*worlds, ("anticoincidence", "one_photon")):
        board = GameBoard(load_world(EVENTS / folder / f"{name}.json"))
        for _ in range(24):
            board.step()  # the board may grow beyond a receding face: the masks at its shape now
            union, everywhere = credit.node_reader_nodes(board), np.ones(board.shape, dtype=bool)
            for index in range(len(board.families)):
                full, frozen = board.share_of(index, 1, everywhere)
                short, frozen_short = board.share_of(index)
                assert np.array_equal(full, short) and np.array_equal(frozen, frozen_short), name
                whole, at_union = board.quanta(index)[0], board.quanta(index, union)[0]
                assert np.array_equal(np.where(union, whole, 0), at_union), name
    kind, wall = kind_of(63), 6000**3  # Gamma^2 p_0 at the vacuum's clock, the write's wall
    counts = np.array([1, 2_000_000, 21_000_000, 22_000_000, 2**31], dtype=kind)
    reference = paces.rounded(np.asarray(counts, dtype=object) * 5999 * 5999 * 5999, wall)
    assert paces.within_width(kind, wall, counts[:2], 5999, 5999, 5999)  # the hardware's branch
    assert not paces.within_width(kind, wall, counts, 5999, 5999, 5999)  # Python's beyond the width
    found = paces.write_factor(counts, 5999, 5999, 5999, 6000, 6000, 2)
    assert found.dtype == kind and np.array_equal(found, np.asarray(reference).astype(kind))
    spread = np.full(counts.shape, 5999, dtype=kind)
    assert np.array_equal(paces.write_factor(counts, spread, spread, 5999, 6000, 6000, 2), found)
    a = np.random.default_rng(3).integers(-9, 9, size=(3, 4, 5)).astype(kind)
    for axis in range(3):
        for sigma in (-1, 1):
            rolled = np.roll(a, -sigma, axis=axis)  # out[i] = a[i + sigma]
            assert np.array_equal(ports.shifted(a, axis, sigma, True, 7), rolled)
            beyond = [slice(None)] * 3
            beyond[axis] = slice(-1, None) if sigma == 1 else slice(None, 1)
            rolled[tuple(beyond)] = 7
            assert np.array_equal(ports.shifted(a, axis, sigma, False, 7), rolled)
    assert ports.shifted(a[:1], 0, 1, False, 7) is a[:1] or np.array_equal(
        ports.shifted(a[:1], 0, 1, False, 7), a[:1]
    )
