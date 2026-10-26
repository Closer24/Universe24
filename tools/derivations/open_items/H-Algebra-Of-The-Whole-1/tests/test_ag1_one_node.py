"""ag1's one-Node tests of the algebra of the whole (ready for tests/: the room tests/test_the_algebra_of_the_whole.py), each under a
few seconds, integers only, every claim a clause of docs/ALGEBRA.md by name:
 - The line and The direction: the flux form identity and the carried division's inverse (core/rule3);
 - The conserved form: the weighted form changes by SUM c_i (a_next - a_before)(r - r') alone (node.Node.rotate);
 - The one rule of the remainder: the mirror w - 1 - r and the odd rounding;
 - The paces compose: the clock against the exact power, the Link's pace the clock twice;
 - The symmetric ride (8a to 8c) and LC-S1: the riding line's momentum form and the pace-weighted Links' sum 0 on an interval;
 - The swap at the top: the exchange an involution and W even under C T_0 at every turned Node;
 - The click: taken at or above booked on every take, the light credited never (The light no body), the laid-back take restoring
   the taken line (EQ-S1), CK-S1's crossing even under the negation;
 - The seed: the fourth form's amplitude the least whose share exceeds the quanta's unit; the uniform board's course free of the
   cube's size; The direction: the run back exact.
Run: PYTHONPATH=src python -m pytest tools/derivations/open_items/H-Algebra-Of-The-Whole-1/tests -q
"""

from __future__ import annotations

import random
import sys
from pathlib import Path

import numpy as np

sys.set_int_max_str_digits(0)

from event_universe import gram, seed  # noqa: E402
from event_universe.core import paces, rule3  # noqa: E402
from event_universe.core.ports import PORTS, across  # noqa: E402
from event_universe.core.rule3 import carried_division, half, mirrored, rule_integers  # noqa: E402
from event_universe.interval import Interval  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402
from event_universe.rows import CARRIER, PLANE, Line  # noqa: E402

WORLDS = Path(__file__).resolve().parents[4] / "tests" / "worlds"
DEN, GAMMA = 1021, 1000  # the toy den 30^2 + 11^2 with its one circle point (779, 660)


def node_of(name: str, **changes):
    universe, world = load_world(WORLDS / name)
    return Node(universe, {**world, **changes})


def test_the_flux_form_is_the_first_form_and_the_division_inverts() -> None:
    """The line; The direction: w a_next + r' = SUM R m + S a_now - w a_before + r == w (2 a_now - a_before) - D a_now + SUM R (m - a_now) + r."""
    rng = random.Random(1)
    unit = rule3.link_unit_of(GAMMA)
    for _ in range(300):
        num = rng.choice([DEN, 779, 1020])
        c = rng.randint(0, 1500)
        factors = tuple(rule3.link_factor(GAMMA, unit, rng.randint(0, 200)) for _ in range(PORTS))
        r = rule_integers(num, DEN, GAMMA, paces.clock(GAMMA, c), paces.link_pace(GAMMA, c), factors, unit)
        assert r.self_coefficient == 2 * r.wall - r.mass - sum(r.reaches)
        now, before = rng.randint(-4000, 4000), rng.randint(-4000, 4000)
        m = [rng.randint(-4000, 4000) for _ in range(PORTS)]
        rem = rng.randint(0, r.wall - 1)
        first = carried_division(sum(a * b for a, b in zip(r.reaches, m, strict=True)) + r.self_coefficient * now - r.wall * before, r.wall, rem, 1)
        flux = sum(a * (b - now) for a, b in zip(r.reaches, m, strict=True))
        nxt, rem2 = rule3.rule3(flux, r.mass, r.wall, now, before, rem, 1)
        assert first == (nxt, rem2) and 0 <= rem2 < r.wall
        assert r.wall * (nxt - 2 * now + before) + rem2 - rem == flux - r.mass * now
        assert rule3.rule3(flux, r.mass, r.wall, now, nxt, rem2, -1) == (before, rem)


def test_the_weighted_form_changes_by_the_remainders_alone() -> None:
    """The conserved form: F(next, now) - F(now, before) == SUM_i c_i (next_i - before_i)(r_i - r'_i), c_i = L / p_i^2, K_ij symmetric."""
    rng = random.Random(2)
    unit = rule3.link_unit_of(GAMMA)
    shape = (3, 3, 3)
    for num in (DEN, 779):
        contents = np.array([rng.choice([0, 7]) for _ in range(27)], dtype=object).reshape(shape)
        pace = paces.link_pace_of(GAMMA, contents)
        tension = [np.array([rng.randint(0, 150) for _ in range(27)], dtype=object).reshape(shape) for _ in range(3)]
        factors = []
        for port in range(PORTS):
            axis, side = divmod(port, 2)
            tt = tension[axis] if side == 0 else across(tension[axis], port)
            factors.append(np.vectorize(lambda x: int(rule3.link_factor(GAMMA, unit, int(x))), otypes=[object])(tt))
        r = rule_integers(num, DEN, GAMMA, paces.clock_of(GAMMA, contents), pace, tuple(factors), unit)
        line = Line(
            np.array([rng.randint(-3000, 3000) for _ in range(27)], dtype=object).reshape(shape),
            np.array([rng.randint(-3000, 3000) for _ in range(27)], dtype=object).reshape(shape),
            np.array([rng.randint(0, r.wall - 1) for _ in range(27)], dtype=object).reshape(shape),
            r.wall,
        )
        held = line.copy()
        node = Node.__new__(Node)
        node.max_transient, node.X, node.gamma = 0, 0, GAMMA
        (stepped,) = Node.rotate(node, [line], r, None, 1, None, None)
        L = 1
        for v in {int(x) for x in (pace * pace).reshape(-1)}:
            L = L * v // rule3.lattice(L, v)
        c = np.vectorize(lambda v: L // int(v), otypes=[object])(pace * pace)

        def form(x, y):
            own = c * (r.wall * (x * x + y * y) - r.self_coefficient * x * y)
            link = sum((c * reach * x * across(y, port) for port, reach in enumerate(r.reaches)), start=0)
            return int(np.sum(own - link))

        drift = int(np.sum(c * (stepped.now - held.before) * (held.rem - stepped.rem)))
        assert form(stepped.now, stepped.before) - form(held.now, held.before) == drift
        assert max(int(x) for x in np.abs(c * r.wall * 3000 * 3000 * 2).reshape(-1)).bit_length() <= 128
        (back,) = Node.rotate(node, [stepped], r, None, -1, None, None)
        assert bool(np.all(back.now == held.now)) and bool(np.all(back.before == held.before)) and bool(np.all(back.rem == held.rem))


def test_the_one_rule_of_the_remainder() -> None:
    """The mirror w - 1 - r commutes with the floor; two mirrors the identity; the odd rounding is sign(x) rounded(|x|)."""
    rng = random.Random(3)
    for _ in range(1000):
        w, u, r = rng.randint(2, 10**9), rng.randint(-10**12, 10**12), 0
        r = rng.randint(0, w - 1)
        assert (w - 1 - u) // w == -(u // w)
        assert mirrored(r, w, 1) == w - 1 - r and mirrored(mirrored(r, w, 1), w, 1) == r and mirrored(r, w, 2) == r
    for wall in (1, 2, 7, 1000, 36000):
        for x in range(-3 * wall - 2, 3 * wall + 3):
            s = 1 if x >= 0 else -1
            assert int(paces.odd_rounded(x, wall)) == s * int(paces.rounded(s * x, wall)) == -int(paces.odd_rounded(-x, wall))


def test_the_paces_compose() -> None:
    """The clock the exact power rounded half up (the oracle within 128 bits); the Link's pace the clock twice; the frozen content."""
    for c in range(0, 12):
        assert paces.clock(GAMMA, c) == (2 * GAMMA * (GAMMA - 1) ** c + GAMMA**c) // (2 * GAMMA**c)
    frozen = paces.frozen_content(GAMMA)
    assert frozen == 3793 and paces.certified(GAMMA) == frozen
    for c in range(0, frozen + 1):
        p0 = paces.clock(GAMMA, c)
        assert paces.link_pace(GAMMA, c) == int(paces.rounded(p0 * p0, GAMMA))
    assert paces.link_pace(GAMMA, frozen) == 0 and paces.link_pace(GAMMA, frozen - 1) == 1


def test_the_riding_lines_momentum_form_and_lc_s1_on_an_interval() -> None:
    """The symmetric ride: W_out (a_next - a_now) - W_in (a_now - a_before) + r' - r - (W_out - W_in) div 2 == X_now F on every
    riding line; LC-S1: SUM over the Links of 2 num Q G^2 (X_j - X_i) == 0; the exchange at the top an involution and W even."""
    node = node_of("world_node.json")
    exact = total = 0
    turned_seen = False
    for _ in range(6):
        iv = Interval(node, 1)
        iv.walled_act()
        iv.forces()
        iv.kicks()
        iv.carrier_act()
        iv.divisions()
        k_c = iv.where[id(iv.carrier)]
        w_in = iv.w_half * (iv.held[k_c][0].before + iv.held[k_c][0].now)
        for r in iv.riders:
            k = iv.where[id(r)]
            s = iv.scales[k]
            for a0, lh, ln, f in zip(iv.starts[k], iv.held[k], iv.out[k], iv.force[k], strict=True):
                left = s * iv.w_div * (ln.now - a0) - s * w_in * (a0 - lh.before) + ln.rem - lh.rem - half(s * iv.w_div) + half(s * w_in)
                total += left.size
                exact += int(np.sum(left == iv.x_now * f))
        rule = node.rule_of(node.row(CARRIER), iv.c, iv.factors)
        weighted = 0
        for port, reach in enumerate(rule.reaches):
            weighted += int(np.sum((reach // (iv.pi * iv.pi)) * (across(iv.x_now, port) - iv.x_now)))
        assert weighted == 0
        iv.writes()
        node.set_rows(iv.out)
        iv.rest()
        top = node.swap(iv.held, iv.frozen)
        if top.any():
            turned_seen = True
            for r in node.records():
                wb, wa = gram.charge(r.shape, iv.held[node.rows_.index(r)]), gram.charge(r.shape, r.lines)
                assert bool(np.all(wb[top] == wa[top]))
            saved = [[line.copy() for line in row] for row in node.rows()]
            node.exchange(top, [[line.copy() for line in row] for row in saved])
            for a, b in zip(node.all_lines(), [line for row in iv.held for line in row], strict=True):
                assert bool(np.all(a.now[top] == b.now[top])) and bool(np.all(a.rem[top] == b.rem[top]))
            node.set_rows(saved)
        node.click(iv.plane_starts, iv.held)
        node.stack.append({"turned": top, "counters": ([], [], []), "log_from": len(node.log), "frozen": iv.frozen})
    assert exact == total == 6 * 27 * 12 and turned_seen


def test_the_close_takes_at_least_what_it_books_and_the_light_is_no_body() -> None:
    """The click (the former take, kept by name): taken >= booked on every take; the gap-0 record credited never; EQ-S1: a laid-back
    credit leaves the taken line's level as it stood; CK-S1's crossing even under the negation."""
    node = node_of("world_pair_3.json", intervals=12)
    rec0 = node.records().index(node.row(PLANE, gap=0))
    for _ in range(3):
        node.step()
    # the fourth interval act by act: the taken line before the close against after it, every credit laid back (EQ-S1)
    iv = Interval(node, 1)
    iv.walled_act()
    iv.forces()
    iv.kicks()
    iv.carrier_act()
    iv.divisions()
    iv.writes()
    node.set_rows(iv.out)
    iv.rest()
    top = node.swap(iv.held, iv.frozen)
    light = node.records()[rec0].lines[0]
    stood = light.now.copy()
    node.click(iv.plane_starts, iv.held)
    node.stack.append({"turned": top, "counters": ([], [], []), "log_from": len(node.log), "frozen": iv.frozen})
    credits = [e for e in node.log if e["event"] == "credit"]
    assert len(credits) == 27 and all(e["line"] != rec0 and "laid_back" in e and e["laid_back"] == e["levels"] > 0 for e in credits)
    assert bool(np.all(light.now == stood))
    assert all(e["taken"] >= node.units[e["line"]] for e in credits)
    assert sum(e["taken"] - node.units[e["line"]] for e in credits) > 0  # the excess of the former take, no remainder kept

    def crossing(b: int, n: int) -> int:
        return 1 if (b * n < 0 or (b == 0) != (n == 0)) else 0

    text = (Path(__file__).resolve().parents[4] / "src" / "event_universe" / "bodies.py").read_text(encoding="utf-8")
    assert "lambda b, n: 1 if (int(b) * int(n) < 0 or (int(b) == 0) != (int(n) == 0)) else 0" in text
    for b in range(-5, 6):
        for n in range(-5, 6):
            assert crossing(b, n) == crossing(-b, -n) == crossing(n, b)
    assert crossing(0, 3) == crossing(0, -3) == 1 and crossing(0, 0) == 0


def test_the_fourth_form_lays_the_least_amplitude_above_the_target_and_the_cube_enters_nowhere() -> None:
    """The seed: the fourth form's amplitude by the search by comparisons (share(amplitude) > n unit >= share(amplitude - 1)); the
    uniform board's X course the same on the 3-cube and the 4-cube (the one-Node line); the run back exact."""
    node = node_of("world_pair_3.json", intervals=1)
    lays = [e for e in node.log if e["event"] == "lay" and e.get("quanta") is not None]
    assert len(lays) == 1
    lay = lays[0]
    row = node.records()[lay["line_pair"]]
    rule = node.rule(row.pair, node.start_content, node.link_factors())
    target = lay["quanta"] * lay["unit"]
    above = seed.share_at_node(node, row, seed.uniform_levels(node, row, lay["amplitude"], lay["sense"]), rule)
    below = seed.share_at_node(node, row, seed.uniform_levels(node, row, lay["amplitude"] - 1, lay["sense"]), rule)
    assert above == lay["share"] > target >= below
    three, four = node_of("world_sea_3.json"), node_of("world_sea_3.json", shape=[4, 4, 4])
    for _ in range(40):
        three.step()
        four.step()
        xs3 = {int(x) for x in three.row(CARRIER).lines[0].now.reshape(-1)}
        xs4 = {int(x) for x in four.row(CARRIER).lines[0].now.reshape(-1)}
        assert len(xs3) == 1 and xs3 == xs4
    kept = [three.state_hash()]
    for _ in range(5):
        three.step()
        kept.append(three.state_hash())
    for k in range(5):
        three.step_back()
        assert three.state_hash() == kept[4 - k]
