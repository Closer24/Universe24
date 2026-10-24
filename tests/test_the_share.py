"""The count is the record's share (ALGEBRA.md #the-count-is-the-records-share): the share e_i = 3 den (now^2 + before^2) - num now S_6(before) changes over one step of Rule3 by exactly SUM_j F_ij, F_ij = num (now_i before_j - before_i now_j), at the pair the step started from, in rationals; in integers the identities carry Rule3's remainder term and the reader's own floor, the audit's exact witnesses pinned (#1582, #1583, #1579); the engine reads the same currents from the record and a node_detector's click is its net front inflow, never a Node; the exact bands (ALGEBRA.md #rule3): 2 cos omega an integer gives the periods 6, 4 and 3 with no remainder."""

import json
from fractions import Fraction

import numpy as np

from event_universe import flux, readings, records, share, world_files
from event_universe.core import paces
from event_universe.core.ports import Wrap
from event_universe.core.rule3 import coefficients, form_term, rule_integers
from event_universe.features.read import edge_squared, paces_guard
from event_universe.lattice import Lattice
from event_universe.loader.derived import family_rules
from event_universe.loader.world import kind_of
from event_universe.world_files import load_world
from tests.laws import arrivals_rule3, real_rows, universe_beside


def law(num, den, gamma, clock, pace, factors=None, unit=1):  # type: ignore[no-untyped-def]
    """The rule a line steps by, (the reaches, S, w, the mass D), as `node.rule_of` gives it."""
    return rule_integers(num, den, gamma, clock, pace, factors, unit)


RING, HERE, GAMMA = Wrap(True, True, True), (1, 1, 1), 6000  # the witnesses at the rule's Gamma


def test_the_integer_identities_carry_their_remainder_terms_and_the_readers_floor():
    """The share's change is the currents at the pair the step started from (issue #1495 finding 6; the paper writer's finding, #1538 comment 5921398465) and not at the pair it left, and the audit's exact witnesses, each the engine's own integers against the law's rational identity, so that an exact-equality wording cannot return (#1582; #1583 B1 to B3; #1579). (a) At equal paces (pair [1, 1], Gamma 5, the content 1, the Node at -3 / -3 with its three + neighbours at -3) the frame's integer share goes 13 to 12 (ALGEBRA.md, The booking is the frame's, 2026-10-23; the plain term's 54 to 26, the share to that day, read beside it as the lines' own read): the frame's current 0, the plain current -27 less the Links' level terms' change -27 (`readings.gauge_terms`), Rule3's remainder term -3 (next - before) (r' - r) / P^2 = -2 / 3, and the frame reading's own floor residual, frac(E(now, before)) - frac(E(next, now)) = -1 / 3 with E the frame's term before its floor, strictly between -1 and 1 per Node and level pair, the identity exact with it; the plain identity on the plain term with the plain current -27 and its residual -1 / 3 as before. (b) The vacuum witness, pair [2, 3] at Gamma 6,000 from now 1 and before 0: next 1 with r' = 216,000,000, the share 9 to 6 with no current, Rule3's term rho = (r - r') / (2 Gamma^2) = -3 (over Gamma^2 alone it would read -6), the line 6 den Gamma^2 (next + before) = 2 num Gamma^2 S_6(now) + r - r' exact. (c) The Wronskian under the integer step (#1579): at [2, 3] the parts (1, 3) from zeros step to (1, 4) and W from 0 to -1, exactly the remainder term eps_re im_now - eps_im re_now with eps = (r - r') / w, under |re_now| + |im_now| per Node and interval, the inverse exact; at [1, 2] the parts stand and W stays 0 (the divisible control): the integer W is conserved up to that term and no quadratic form of the levels and remainders is conserved exactly (the second mathematician, #1572 comment 5932042343), so every test of a conserved quantity asserts a bound, never exactness. (d) The band's edge (B2): light's checkerboard at wave number pi on every axis reads 2 cos omega = -2 exactly, a repeated root the guard admits at p = Gamma, and the line grows it linearly, (-1)^t (t + 1) with the remainder 0, so the guard excludes exponential growth and does not bound the record; the same checkerboard with before = -now has the share 0 at every Node, a null mode that is no static uniform record. (e) The conserved form's domain (B1): at Node-isotropic paces the weighted form E with the Node weights 1 / p_i^2 is conserved exactly by the unrounded line, on the audit's 2 x 1 x 1 light board at Gamma 2 with the paces 2 and 1 (M = [[4 / 3, 2 / 3], [1 / 6, 11 / 6]]) E standing at 6 while the unweighted D falls from 1 to 11 / 12, and on the 2 x 2 x 1 square with p_x(A) = 2 among paces 1 the product of M_ij / M_ji around the square is 4, so no positive Node weight symmetrises a read booked per Node per axis. The exact bands beside them: a Node at rest in the vacuum turns by 2 cos omega = 2 num / den, the three integer rotations 1, 0 and -1 closing in 6, 4 and 3 intervals with the remainder 0 at every step. The corner's reads carry the x Links' factor 4 at the pace 1 against the plain reads."""
    zero, ones = np.zeros((3, 3, 3), dtype=np.int64), np.ones((3, 3, 3), dtype=np.int64)
    rule = law(1, 1, 5, *paces.node_paces(5, 1))  # the clock 4, the pace 3: R 18, S 192, w 150
    now, before = zero.copy(), zero.copy()
    now[1, 1, 1] = now[2, 1, 1] = now[1, 2, 1] = now[1, 1, 2] = before[1, 1, 1] = -3
    after = flux.step_line(record := records.Record(now, before, zero), rule, RING)
    weight = 2 * paces.link_pace(5, 1) ** 2  # the share's wall 2 p_i^2 G^2 = 18 at the Node's pace 3
    shares = [int(share.share((1, 1), r, RING, 5, 1)[HERE]) for r in (record, after)]
    plain = [int(share.share((1, 1), r, RING, 5, 1, as_read=r)[HERE]) for r in (record, after)]
    currents = sum(int(f[HERE]) for f in readings.currents_of(1, [record], RING))
    nxt, carried = int(after.now[HERE]), int(after.remainder[HERE])

    def unfloored(
        r,
    ):  # the frame's term before its floor: the plain term doubled less the Links' products
        now, before = int(r.now[HERE]), int(r.before[HERE])
        at = [
            (np.roll(r.now, -s, a)[HERE], np.roll(r.before, -s, a)[HERE])
            for a in range(3)
            for s in (1, -1)
        ]
        term = form_term(rule[1], rule[2], now, before) - now * sum(
            rule[0][k] * b for k, (_n, b) in enumerate(at)
        )
        links = sum(rule[0][k] * (before - b) * (now + n) for k, (n, b) in enumerate(at))
        return Fraction(int(2 * term - links), 2 * weight), Fraction(int(term), weight)

    residual = unfloored(record)[0] % 1 - unfloored(after)[0] % 1
    assert (nxt, carried, shares, plain, currents) == (-2, 12, [13, 12], [54, 26], -27)
    assert residual == Fraction(
        -1, 3
    )  # the level terms' clause left with readings.gauge_terms, 2026-10-24
    assert (
        sum(int(f[HERE]) for f in readings.currents_of(1, [after], RING)) != currents
    )  # not the pair left
    plain_residual = unfloored(record)[1] % 1 - unfloored(after)[1] % 1
    assert plain[1] - plain[0] == currents + Fraction(-(nxt + 3) * carried, weight) + plain_residual
    record, rule = records.Record(ones, zero, zero), law(2, 3, GAMMA, GAMMA, GAMMA)
    after = flux.step_line(record, rule, RING)
    nxt, carried = int(after.now[HERE]), int(after.remainder[HERE])
    shares = [int(share.share((2, 3), r, RING, GAMMA)[HERE]) for r in (record, after)]
    assert (nxt, carried, rule[2], shares) == (1, 216_000_000, 648_000_000, [9, 6])
    assert not any(f[HERE] for f in readings.currents_of(2, [record], RING))
    assert Fraction(-carried, 2 * GAMMA**2) == shares[1] - shares[0] == -3
    assert rule[2] * (nxt + 0) == 2 * 2 * GAMMA**2 * 6 + 0 - carried
    for pair, levels, turned in (((2, 3), [1, 4], -1), ((1, 2), [1, 3], 0)):
        rule = law(*pair, GAMMA, GAMMA, GAMMA)
        lines = [records.Record(ones, zero, zero), records.Record(3 * ones, zero, zero)]
        after = [flux.step_line(line, rule, RING) for line in lines]
        eps = [Fraction(-int(a.remainder[HERE]), rule[2]) for a in after]  # (r - r') / w from r = 0
        found = int(records.wronskian(after, True)[HERE])
        assert ([int(a.now[HERE]) for a in after], found) == (levels, turned)
        assert found == eps[0] * 3 - eps[1] * 1 and abs(found) < 1 + 3
        back = [flux.step_line(a, rule, RING, -1) for a in after]
        assert [int(b.now[HERE]) for b in back] == [1, 3] and not any(b.remainder.any() for b in back)
    rule = law(1, 1, GAMMA, GAMMA, GAMMA)
    assert Fraction(rule[1] - 6 * rule[0][0], rule[2]) == -2 and edge_squared((1, 1), GAMMA) == GAMMA**2
    paces_guard((1, 1), GAMMA, 1, 0, (1,) * 6, "light")  # the edge admitted at the paces Gamma
    record = records.Record(parity := (-1) ** np.indices((2, 2, 2)).sum(0), 0 * parity, 0 * parity)
    for t in range(1, 7):
        record = flux.step_line(record, rule, RING)
        assert np.array_equal(record.now, (-1) ** t * (t + 1) * parity) and not record.remainder.any()
    assert not share.share((1, 1), records.Record(parity, -parity, 0 * parity), RING, GAMMA).any()
    at = (2, 1)  # Gamma 2: the Node's pace 2 at A and 1 at B on a chain of two, the clock 2
    rules = [law(1, 1, 2, 2, p) for p in at]
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
            nxt, carry = arrivals_rule3(
                (read,) * 3, (2 * now,) * 3, self_coefficient, wall, now, before, 0
            )
            assert carry == 0
            before, now = now, nxt
        assert (before, now) == (0, 1_000)


def test_the_engine_reads_the_currents_from_the_record_through_the_six_ports():
    """The currents the engine reads (`readings.currents_of`) are F_ij = num (now_i before_j - before_i now_j) through each Port, both level pairs added, on the record as it is and nothing kept beside it."""
    (quanta,) = family_rules(real_rows(("quanta", (5, 7), 1, None)))
    draw, shape, wrap = np.random.default_rng(2), (3, 3, 3), Wrap(True, True, True)
    zero = records.zeros(shape, kind_of(63))
    real, second = (records.Record(*draw.integers(-50, 50, (2, *shape)), zero) for _ in range(2))
    through = readings.currents_of(quanta.pair[0], [real, second], wrap)
    for port, (axis, side) in enumerate((a, s) for a in range(3) for s in (1, -1)):
        rolled = [(r, *(np.roll(a, -side, axis) for a in (r.now, r.before))) for r in (real, second)]
        expected = sum(5 * (r.now * before - r.before * now) for r, now, before in rolled)
        assert np.array_equal(through[port], expected)


def test_under_the_rotation_the_share_reads_the_level_before_turned_as_the_step_reads_it(
    tmp_path, monkeypatch
):
    """Under the rotation the share reads the level pair as the step reads it (ALGEBRA.md, The share's change is the currents; the mathematician's line, #1793 comment 5981866600 K3; the advisor's breaker, 5981736108 K3): on a ring of 48 Nodes the rule's charge row under `act: rotation` (the energy line's T 36,000 and k_w 4) read by the charged plane alone, the plane at random levels within 6,000 at the Link unit 1 (the amplitude bound 1,271,114; at G = 16 the record's own sign row, written from its Wronskian, reaches the bound 4,963 within twenty intervals above the amplitude 600), the holder's free row, the one the record reads, at the level L, tan(theta / 2) = L / (2 Gamma). (a) Where no family turns (`act: pace`, the untouched integers) `Lattice.share_of` is the plain form of the levels by hand at every Node, bit for bit, and under the rotation at L = 0 the turned read is the plain read bit for bit over the run. (b) At every Node and interval under a uniform level the step's identity is exact in the integers with its three named walk terms, wall (e_flat(v, z_now) - e(z_now, u)) = wall SUM_j F_ij(z_now, u) - SUM over the two lines of (v - u) (r' - r) + w (u^2 - z_before^2): u the plain level before and v the stepped level (the booking's second), the currents from the plain pair, Rule3's remainder term, wall = 2 p_i^2 G^2 (under the temporal gauge the time Link carries no phase and the share reads the plain pair, features/phase, Part C). (c) Over 40 intervals at a uniform L of 960, 2,400 and 4,920 (L theta_0 0.16, 0.40 and 0.82) the engine's total moves by at most 5 x 10^-4 of itself, the integer walk (10^-4 at L = 0), and the plain read drifts by nothing: a uniform level does nothing, as a uniform potential does (the mathematician's item 6; the time shear's plain read drifted +0.64, +3.5 and +12.4 percent). (d) Under a ramp of L along the ring, 0 to the top and back, the Links' phase pairs turn by the two ends' difference and the share moves by the gradient's work, a few 10^-3 at the tops 2,400 and 4,920 (5.5 x 10^-3 measured), no rounding, the plain identity of (b) not read there; LATTICE readings, printed."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    universe_beside(tmp_path, drop=("gravity", "binding"), charged=True)
    rows = json.loads((tmp_path / "u.json").read_text(encoding="utf-8"))
    rows["integers"]["quantum_action"] = (
        36_000  # T at which the law's alpha E_h T num / (Gamma den) is 4
    )
    (tmp_path / "turn.json").write_text(json.dumps(rows), encoding="utf-8")
    world = dict(shape=[48, 1, 1], intervals=40)
    paths = {"turn": tmp_path / "turn_ring.json"}
    paths["turn"].write_text(json.dumps({**world, "universe": "turn.json"}), encoding="utf-8")

    def ring(path, level, amplitude=6000):  # the plane at random levels, the free row at the level
        board, draw = Lattice(load_world(path)), np.random.default_rng(10)
        charged, sign = ([f.name for f in board.families].index(n) for n in ("charged", "charge"))
        half = np.full(board.shape, board.half_wall(charged), dtype=board.kind)
        for line in range(2):
            now, before = draw.integers(-amplitude, amplitude, (2, *board.shape)).astype(board.kind)
            board.states[charged].lines[line] = records.Record(now, before, half)
        held = np.asarray(level, dtype=board.kind).reshape(board.shape)
        board.states[sign].lines[0] = records.Record(held, held.copy(), half)
        return board, charged

    turned = Lattice(load_world(paths["turn"]))
    assert turned.turning == [
        [f.name for f in turned.families].index("charged")
    ]  # the holder of the sign rotates

    def run(level, label, exact=True):
        board, charged = ring(paths["turn"], level)
        family, read = board.families[charged], board.read(charged)
        gamma, unit = board.world.node_clock, board.unit
        w = coefficients(*family.pair, gamma, *paces.node_paces(gamma, read[0]), read[1], unit)[2]
        wall = 2 * paces.link_pace_of(gamma, read[0]) ** 2 * unit * unit

        def shares(lines, turned=None):
            found = share.family_share(family, lines, board.wrap, gamma, *read, unit, None, turned)
            return found.astype(object)

        start, drifts = board.total_share(charged)[0], []
        plain_start = int(shares(board.lines_of(charged, 0)).sum())
        for _ in range(40):
            lines = board.lines_of(charged, 0)
            turned = None  # the plain pair: under the temporal gauge the time Link carries no phase
            flows = sum(
                c.astype(object) for c in readings.currents_of(family.pair[0], lines, board.wrap)
            )
            first, second = board.stepped(charged, 1)[1][0]
            terms = (
                wall * (shares(second, second) - shares(lines, lines)) - wall * flows
            )  # the plain term, the lines as their own read: the frame's term stands beside it since 2026-10-23, its change the frame's currents ((a) above)
            for k in range(2):
                u, v = first[k].before.astype(object), second[k].now.astype(object)
                before, carried = lines[k].before.astype(object), lines[k].remainder.astype(object)
                terms += (v - u) * (second[k].remainder.astype(object) - carried)
                terms -= w * (u * u - before * before)
            assert (
                not exact or not terms.any()
            )  # the step's identity exact at every Node, the plain pairs
            assert level.any() or np.array_equal(shares(lines, turned), shares(lines))  # L = 0
            board.step()
            plain = int(shares(board.lines_of(charged, 0)).sum()) - plain_start
            drifts.append((board.total_share(charged)[0] - start, plain))
        moved, plain = max(abs(d) for d, _ in drifts) / start, drifts[-1][1] / plain_start
        print(
            f"LATTICE {label}: the share {start}, the turned read's largest |drift| {moved:.1e} of it, the plain read's drift at the end {plain:+.2%}"
        )
        return moved, plain

    x = np.arange(48)
    assert run(np.zeros(48, dtype=int), "the level 0")[0] < 1e-4
    for top in (
        960,
        2400,
        4920,
    ):  # the temporal gauge: a uniform level does nothing, the plain read exact
        label = f"the uniform level {top}, L theta_0 {top / 6000:.2f}"
        moved, plain = run(np.full(48, top), label)
        assert moved < 5e-4 and abs(plain) < 1e-4, (top, moved, plain)
        if top > 960:
            moved, plain = run(np.minimum(x, 48 - x) * top // 24, f"the ramp 0 to {top} and back", False)
            print(f"  the ramp's drift {moved:.1e}, the plain read's {plain:+.2%}")  # the Links phased
            assert moved < 2e-2, (top, moved, plain)  # the gradient's work on the share, no rounding
