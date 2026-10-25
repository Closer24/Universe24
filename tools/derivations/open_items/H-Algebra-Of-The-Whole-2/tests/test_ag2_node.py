"""ag2's one-Node tests on the engine's Node (the brief's items 1c, 3, 4b, 5 and 6), integers only, each on a 3-cube or a 5-cube under 15 s: the step's reach one Link; LC-S1's pace-weighted Links' sum 0 exactly on three seeds with the plain sum's lift measured; the mean wall's momentum form (the state and the momentum one bijection); the exchange an involution with the charge even; CK-S1's crossing even under the negation; the fourth form's amplitude the least whose share exceeds the quanta; the uniform board's flux 0 (the one-Node line). Room: tests/test_the_node.py and tests/test_the_board.py."""

from __future__ import annotations

import copy

import numpy as np

from event_universe import gram, readings, seed
from event_universe.core.ports import AXES, PORTS, across
from event_universe.core.rule3 import division_forward, half
from event_universe.rows import CARRIER, PLANE, Line
from tests.laws import node_of, run_back_exact, state_of


def lines_at(node, at):
    return [(int(l.now[at]), int(l.before[at]), int(l.rem[at]), None if l.wr is None else int(l.wr[at])) for l in node.all_lines()]


def test_the_step_reaches_one_link_and_the_close_may_reach_two() -> None:
    """One Link: a level changed two Links from the Node (at (1, 1, 0) from (0, 0, 0) on the 3-torus) leaves every integer of the Node's rows after the interval's acts before the close; the close's reach is the ledger's crowded lay (two Links), named and not asserted."""
    a = node_of("world_node.json")
    b = copy.deepcopy(a)
    light = b.row(PLANE, gap=0).lines[0]
    light.now[1, 1, 0] = int(light.now[1, 1, 0]) + 5
    far = (1, 1, 0)
    near = (1, 0, 0)
    for node in (a, b):
        from event_universe.interval import Interval
        it = Interval(node, 1)
        it.walled_act(); it.forces(); it.kicks(); it.carrier_act(); it.divisions(); it.writes()
        node.set_rows(it.out)
    assert lines_at(a, (0, 0, 0)) == lines_at(b, (0, 0, 0))
    assert lines_at(a, near) != lines_at(b, near)
    assert lines_at(a, far) != lines_at(b, far)


def weighted_and_plain(node):
    """LC-S1 at an interval's start: the pace-weighted sum SUM_i (1 / p_i^2) SUM_j R_ij (X_j - X_i) = SUM_i SUM_j 2 num Q_ij G^2 (X_j - X_i) and the plain sum SUM_i SUM_j R_ij (X_j - X_i), both as integers over the board on the carrier's time line, and the factors' symmetry read from both ends."""
    c = node.content()
    _p0, pi = readings.paces_of(node, c)
    factors = node.link_factors(None, readings.frozen_of(node, c))
    x = node.row(CARRIER).lines[0].now
    num = node.row(CARRIER).pair[0]
    weighted = plain = 0
    symmetric = True
    for port in range(PORTS):
        diff = across(x, port) - x
        reach = 2 * pi * pi * factors[port] * num
        weighted += int(np.sum(2 * num * factors[port] * node.G * node.G * diff))
        plain += int(np.sum(reach * node.G * node.G * diff))
        back = port + 1 if port % 2 == 0 else port - 1
        symmetric = symmetric and bool(np.all(across(factors[back], port) == factors[port]))
    return weighted, plain, symmetric


def test_lc_s1_the_pace_weighted_links_sum_is_zero_on_three_seeds() -> None:
    """LC-S1: the weighted sum 0 exactly in the integers at every interval read, the Link's factor the same from both ends; the plain sum the lift, its size recorded (0 on the uniform seed, nonzero where the paces differ)."""
    found = {}
    for name, steps in (("world_hole.json", 12), ("world_chiral.json", 12), ("world_sea_3.json", 30)):
        node = node_of(name)
        lifts = []
        for _ in range(steps):
            weighted, plain, symmetric = weighted_and_plain(node)
            assert weighted == 0 and symmetric
            lifts.append(plain)
            node.step()
        found[name] = lifts
    assert all(x == 0 for x in found["world_sea_3.json"])
    assert any(x != 0 for x in found["world_hole.json"])
    print("ag2 lc_s1 plain sums (the lift):", {k: [x.bit_length() for x in v] for k, v in found.items()})


def test_the_mean_wall_division_is_a_bijection_through_the_momentum() -> None:
    """The kick and the division at the mean wall: the riding line's state (a_now, a_before, r) at the wall W and its momentum P = W (a_now - a_before) + r - W div 2 determine each other (r in [0, W)); the division a_next = a_now + (P_out + W_out div 2) div W_out with the remainder kept writes P_out into the new state exactly, so P_in read from the post state equals P_out, the carried quantity of the act (interval.kicks, interval.divisions)."""
    import random

    rng = random.Random(5)
    for _ in range(3000):
        w_in, w_out = rng.randrange(2, 10**12), rng.randrange(2, 10**12)
        a, b, r = rng.randrange(-10**9, 10**9), rng.randrange(-10**9, 10**9), rng.randrange(0, w_in)
        p_in = w_in * (a - b) + r - half(w_in)
        v, r_back = division_forward(p_in + half(w_in), w_in, 0)
        assert (v, r_back) == (a - b, r)
        kick = rng.randrange(-10**15, 10**15)
        p_out = p_in + kick
        v2, r2 = division_forward(p_out, w_out, half(w_out))
        a_next = a + v2
        assert w_out * (a_next - a) + r2 - half(w_out) == p_out
        assert 0 <= r2 < w_out


def test_the_exchange_is_an_involution_and_the_charge_is_even_under_it() -> None:
    """The swap at the top: node.exchange at a mask applied twice returns every integer of the state; the records' charge at the turned Nodes is unchanged by one exchange (W even under C T_0), the im line's rotation remainder kept and the re line's mirrored."""
    node = node_of("world_chiral.json")
    for _ in range(8):
        node.step()
    held = [[line.copy() for line in row] for row in node.rows()]
    mask = np.zeros(node.shape, dtype=bool)
    mask[0, 0, 0] = mask[2, 3, 1] = mask[4, 4, 4] = True
    charges_before = [gram.charge(r.shape, r.lines).copy() for r in node.records()]
    before = state_of(node)
    node.exchange(mask, held)
    once = state_of(node)
    assert once != before
    for r, w0 in zip(node.records(), charges_before, strict=True):
        assert np.all(gram.charge(r.shape, r.lines) == w0)
    for r in node.records():
        re, im = r.lines
        for at in ((0, 0, 0), (2, 3, 1), (4, 4, 4)):
            k = node.rows_.index(r)
            assert int(re.rem[at]) == int(held[k][0].wall if np.ndim(held[k][0].wall) == 0 else held[k][0].wall[at]) - 1 - int(held[k][0].rem[at])
            assert int(im.rem[at]) == int(held[k][1].rem[at])
    held2 = [[line.copy() for line in row] for row in node.rows()]
    node.exchange(mask, held2)
    assert state_of(node) == before


def test_ck_s1_the_crossing_is_even_under_the_negation_of_the_line() -> None:
    """CK-S1: the crossing read as b n < 0 or exactly one of b, n is 0 is even under (b, n) -> (-b, -n) on every pair of levels in [-4, 4]; a touch of zero a crossing from either side alike; (0, 0) no crossing."""
    def crossing(b: int, n: int) -> int:
        return 1 if (b * n < 0 or (b == 0) != (n == 0)) else 0

    for b in range(-4, 5):
        for n in range(-4, 5):
            assert crossing(b, n) == crossing(-b, -n)
            assert crossing(b, n) == crossing(n, b)
    assert crossing(0, 0) == 0 and crossing(0, 3) == 1 and crossing(-3, 0) == 1 and crossing(2, 3) == 0


def test_the_fourth_forms_amplitude_is_the_least_whose_share_exceeds_the_quanta() -> None:
    """The fourth form (MA-S1, seed.lay_uniform): the amplitude found is the least A with share(A) > n units at the vacuum's weight; share(A - 1) <= n units; whether share(A - 1) = n units exactly (where the letter 'at or above' and the code 'above' would part) is recorded for the toy's three gapped rows."""
    node = node_of("world_sea_3.json")
    found = {}
    for rec, row in enumerate(node.records()):
        if not row.gap:
            continue
        rule = node.rule(row.pair, node.content(), node.link_factors())
        target = 1 * node.units[rec]
        fresh = node_of("world_sea_3.json")
        seed.lay_uniform(fresh, rec, 1, 1)
        amplitude = fresh.log[-1]["amplitude"]
        s_at = seed.share_at_node(node, row, seed.uniform_levels(node, row, amplitude, 1), rule)
        s_below = seed.share_at_node(node, row, seed.uniform_levels(node, row, amplitude - 1, 1), rule)
        assert s_at > target >= s_below
        found[rec] = (amplitude, s_at - target, target - s_below)
    print("ag2 fourth form (amplitude, share - target, target - share below):", found)
    assert all(v[2] > 0 for v in found.values())


def test_the_uniform_board_is_the_one_node_line_and_returns_exactly() -> None:
    """The uniform board (BB-S1, MA-S1): every arrival equals the Node's level, so SUM_j R_j (m_j - a) = 0 at every row and the step is the one-Node line w (a_next - 2 a_now + a_before) + r' - r = -D a_now; the 3-cube's bare sea returns to X = Gamma at every Node at the intervals 115 and 116 and the state at 116 equals the state at 1 in the carrier's levels; the run back exact."""
    node = node_of("world_sea_3.json")
    returns = []
    alike = True
    for t in range(1, 121):
        node.step()
        x = node.row(CARRIER).lines[0]  # the rows' lines are replaced at every interval (set_rows)
        nows = {int(v) for v in x.now.reshape(-1)}
        alike = alike and len(nows) == 1
        if nows == {node.gamma}:
            returns.append(t)
    assert alike
    assert returns[:2] == [114, 115], returns  # X = Gamma after the intervals 114 and 115 (the record's Node lines i = 114, 115)
    assert run_back_exact(node_of("world_sea_3.json"), 6) == 6
