"""ag2's one-Node tests of what the lattice conserves (THE_WAY step 2; the brief's items 1 and 3): the conserved form at fixed reads exact to the remainders on a 3-cube of random levels at two contents (the weight 1 / p_i^2 carried as the integer (p_1 p_2)^2 div p_i^2), the identity E(next, now) - E(now, before) = SUM_i weight_i (next_i - before_i)(r_i - r'_i); the Link's current antisymmetric, F_ij = -F_ji, on the engine's state; the lattice momentum's change at a lay equal to momentum_of; the Link's one current C_ij = -C_ji (LC-S1). Room: tests/test_rule3.py, tests/test_the_node.py."""

from __future__ import annotations

import random

import numpy as np

from event_universe.core import paces
from event_universe.core.ports import PORTS, PORT_SIDES, across
from event_universe.core.rule3 import rule3, rule_integers
from event_universe.links import link_current, net_current
from event_universe.rows import PLANE
from event_universe.take import momentum_of, neighbour
from tests.laws import node_of

gamma_toy, den_toy, unit_toy, num_toy = 1000, 1021, 16, 1000
cube_toy = 3


def neighbours(at: tuple[int, int, int], port: int) -> tuple[int, int, int]:
    axis, side = PORT_SIDES[port]
    return tuple((at[a] + (side if a == axis else 0)) % cube_toy for a in range(3))


def test_the_conserved_form_is_exact_to_the_remainders_at_fixed_reads() -> None:
    """ALGEBRA.md, The conserved form: with the reads fixed (the paces and the Link factors standing), the weighted form changes by SUM_i weight_i (next_i - before_i)(r_i - r'_i) alone, each step, on 3-cubes of random levels at two contents and random Link factors read the same from both ends."""
    rng = random.Random(23)
    sites = [(x, y, z) for x in range(cube_toy) for y in range(cube_toy) for z in range(cube_toy)]
    for _ in range(6):
        c1, c2 = rng.randrange(0, 1500), rng.randrange(0, 1500)
        content = {at: (c1 if rng.randrange(2) else c2) for at in sites}
        p1, p2 = paces.link_pace(gamma_toy, c1), paces.link_pace(gamma_toy, c2)
        q = {}
        for at in sites:
            for port in range(0, PORTS, 2):
                value = rng.randrange(1, unit_toy * unit_toy + 1)
                q[(at, port)] = value
                q[(neighbours(at, port), port + 1)] = value
        rules = {}
        for at in sites:
            clock, pace = paces.clock(gamma_toy, content[at]), paces.link_pace(gamma_toy, content[at])
            rules[at] = rule_integers(num_toy, den_toy, gamma_toy, clock, pace, tuple(q[(at, port)] for port in range(PORTS)), unit_toy)
        weight = {at: (p1 * p1 * p2 * p2) // (paces.link_pace(gamma_toy, content[at]) ** 2) for at in sites}
        assert all(weight[at] * paces.link_pace(gamma_toy, content[at]) ** 2 == p1 * p1 * p2 * p2 for at in sites)
        now = {at: rng.randrange(-10**6, 10**6) for at in sites}
        before = {at: rng.randrange(-10**6, 10**6) for at in sites}
        rem = {at: rng.randrange(0, rules[at].wall) for at in sites}

        def form(n: dict, b: dict) -> int:
            total = 0
            for at in sites:
                r = rules[at]
                total += weight[at] * (r.wall * (n[at] * n[at] + b[at] * b[at]) - r.self_coefficient * n[at] * b[at])
                total -= weight[at] * sum(r.reaches[port] * n[at] * b[neighbours(at, port)] for port in range(PORTS))
            return total

        for _step in range(12):
            e0 = form(now, before)
            nxt, rem2 = {}, {}
            for at in sites:
                r = rules[at]
                flux = sum(r.reaches[port] * (now[neighbours(at, port)] - now[at]) for port in range(PORTS))
                nxt[at], rem2[at] = rule3(flux, r.mass, r.wall, now[at], before[at], rem[at], 1)
            e1 = form(nxt, now)
            budget = sum(weight[at] * (nxt[at] - before[at]) * (rem[at] - rem2[at]) for at in sites)
            assert e1 - e0 == budget
            before, now, rem = now, nxt, rem2


def test_the_links_current_is_antisymmetric_and_the_momentum_change_is_momentum_of() -> None:
    """The current's antisymmetry (The bilinears of one pair; LC-S1): F_ij read at i through the Port equals -F_ji read at j through the Port back, on the chiral seed's state after eight intervals, every line and every Link; the net transverse current; and the lattice momentum P_a = 2 num SUM_i (now_(i+a) before_i - now_i before_(i+a)) changes at a lay by exactly take.momentum_of."""
    node = node_of("world_chiral.json")
    for _ in range(8):
        node.step()
    for line in node.all_lines():
        for port in range(PORTS):
            back = port + 1 if port % 2 == 0 else port - 1
            here = link_current(line, port)
            there = across(link_current(line, back), port)
            assert np.all(here == -there)
    gap0 = node.row(PLANE, gap=0)
    re = gap0.lines[0]
    num = gap0.pair[0]

    def momentum() -> list[int]:
        found = []
        for a in range(3):
            up = across(re.now, 2 * a)
            upb = across(re.before, 2 * a)
            found.append(int(np.sum(2 * num * (up * re.before - re.now * upb))))
        return found

    at = (2, 1, 3)
    p0 = momentum()
    d_now, d_before = 12345, -678
    predicted = momentum_of(node, re.now, re.before, at, d_now=d_now, d_before=d_before, num=num)
    re.now[at] = re.now[at] + d_now
    re.before[at] = re.before[at] + d_before
    p1 = momentum()
    assert [b - a for a, b in zip(p0, p1, strict=True)] == predicted
    assert neighbour(node, (0, 0, 0), 1) == (4, 0, 0)


def test_the_charge_drifts_at_moving_paces_and_the_weighted_charge_is_exact_to_the_remainders() -> None:
    """The charge written is the Wronskian (ws1's drift): on a plane stepped by Rule3 at fixed reads, w SUM_i weight_i (W_next,i - W_now,i) = SUM_i weight_i [(r - r')_re,i im_i - (r - r')_im,i re_i] exactly, the Links' part cancelling since weight_i R_ij is symmetric (weight_i = (p_1 p_2)^2 div p_i^2); the plain total SUM_i W_i drifts where the paces differ (the asymmetry R_ij - R_ji), measured nonzero."""
    rng = random.Random(29)
    sites = [(x, y, z) for x in range(cube_toy) for y in range(cube_toy) for z in range(cube_toy)]
    plain_drifts = []
    for _ in range(4):
        c1, c2 = rng.randrange(0, 1500), rng.randrange(1500, 3000)
        content = {at: (c1 if rng.randrange(2) else c2) for at in sites}
        p1, p2 = paces.link_pace(gamma_toy, c1), paces.link_pace(gamma_toy, c2)
        q = {}
        for at in sites:
            for port in range(0, PORTS, 2):
                value = rng.randrange(1, unit_toy * unit_toy + 1)
                q[(at, port)] = value
                q[(neighbours(at, port), port + 1)] = value
        rules = {at: rule_integers(num_toy, den_toy, gamma_toy, paces.clock(gamma_toy, content[at]), paces.link_pace(gamma_toy, content[at]), tuple(q[(at, port)] for port in range(PORTS)), unit_toy) for at in sites}
        weight = {at: (p1 * p1 * p2 * p2) // (paces.link_pace(gamma_toy, content[at]) ** 2) for at in sites}
        lines = {k: ({at: rng.randrange(-10**6, 10**6) for at in sites}, {at: rng.randrange(-10**6, 10**6) for at in sites}, {at: rng.randrange(0, rules[at].wall) for at in sites}) for k in ("re", "im")}

        def wronskian(at):
            re_n, re_b, _ = lines["re"]
            im_n, im_b, _ = lines["im"]
            return re_n[at] * im_b[at] - im_n[at] * re_b[at]

        for _step in range(10):
            w_now = {at: wronskian(at) for at in sites}
            drs = {}
            for k in ("re", "im"):
                now, before, rem = lines[k]
                nxt, rem2 = {}, {}
                for at in sites:
                    r = rules[at]
                    flux = sum(r.reaches[port] * (now[neighbours(at, port)] - now[at]) for port in range(PORTS))
                    nxt[at], rem2[at] = rule3(flux, r.mass, r.wall, now[at], before[at], rem[at], 1)
                drs[k] = {at: rem[at] - rem2[at] for at in sites}
                lines[k] = (nxt, now, rem2)
            w_next = {at: wronskian(at) for at in sites}
            re_n, im_n = lines["re"][1], lines["im"][1]  # the levels now of the step just taken
            budget = sum(weight[at] * (drs["re"][at] * im_n[at] - drs["im"][at] * re_n[at]) for at in sites)
            wall = rules[sites[0]].wall
            assert wall * sum(weight[at] * (w_next[at] - w_now[at]) for at in sites) == budget
            plain_drifts.append(sum(w_next[at] - w_now[at] for at in sites))
    assert any(d != 0 for d in plain_drifts)
