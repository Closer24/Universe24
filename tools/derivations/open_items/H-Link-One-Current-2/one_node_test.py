"""lc2's one-Node test (under 15 s): the 3-cube sea with the centre fed one quantum (two contents on the board). Under LC2_REACH=harmonic (the copy) the reach from the centre to a neighbour equals the reach from that neighbour to the centre on every row and every Port (R_ij = R_ji exactly, one integer per Link), the Link's pace squared equals Gamma^3 over the Link's mean volume to the rounding (|P_ij (X_i + X_j) - 2 Gamma^3| within (X_i + X_j) + 2 Gamma^3 div 500, the pace table's own rounding), the board's plain Links' sum on the carrier's time line is 0 exactly at every interval over 20, the vacuum's rule is bit for bit the default's (the reach 2 num Gamma^2 G^2 Q at p_i = p_j = Gamma), the run back 10 of 10; under the default (the flag absent) the two ends differ at every Link with a gradient and the plain sum is positive. Run: PYTHONPATH=src_lc2 LC2_REACH=harmonic python one_node_test.py; and without the flag."""
import json
import os
import sys
import time

import numpy as np

from event_universe import readings
from event_universe.core.ports import PORTS, PORT_SIDES, across
from event_universe.loader.world import read_world
from event_universe.node import Node
from event_universe.rows import CARRIER

t0 = time.monotonic_ns()
universe = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "universe_toy.json")))
world = {"universe": "universe_toy.json", "shape": [3, 3, 3], "intervals": 20, "seed": [{"lay": "sea", "row": 0}, {"lay": "at", "row": 0, "centre": [1, 1, 1], "quanta": 1}]}
universe, world = read_world(world, universe)
node = Node(universe, world)
form = os.environ.get("LC2_REACH", "default")
gamma = node.gamma
equal_ports = 0
links_with_gradient = 0
sums = []
pace_checks = [0, 0]
hashes = []
for t in range(20):
    if t >= 10:
        hashes.append(node.state_hash())
    carrier = node.row(CARRIER)
    x = carrier.lines[0].now
    c = node.content()
    frozen = readings.frozen_of(node, c)
    factors = node.link_factors(None, frozen)
    rules = [node.rule_of(r, c, factors) for r in node.rows_ if r.wall is None]
    total = 0
    for rule in rules:
        for port in range(PORTS):
            axis, side = PORT_SIDES[port]
            back_port = port + 1 if side == 1 else port - 1
            r_ij = rule.reaches[port]
            r_ji = across(rule.reaches[back_port], port)
            grad = (across(x, port) != x)
            links_with_gradient += int(np.sum(grad))
            equal_ports += int(np.sum((r_ij == r_ji) & grad))
            if rule is rules[0]:
                pass
    rule_c = node.rule_of(carrier, c, factors)
    for port in range(PORTS):
        total += int(np.sum(rule_c.reaches[port] * (across(x, port) - x)))
    sums.append(total)
    # the Link's pace squared against Gamma^3 over the mean volume (the carrier's row, num = den - den div Gamma, Q = G^2 on the sea's Links)
    num = carrier.pair[0]
    for port in range(PORTS):
        p_sq = rule_c.reaches[port] // (2 * num * factors[port])
        xs = x + across(x, port)
        for a, b in zip(np.asarray(p_sq, dtype=object).reshape(-1), np.asarray(xs, dtype=object).reshape(-1)):
            pace_checks[1] += 1
            if abs(int(a) * int(b) - 2 * gamma ** 3) <= int(b) + 2 * gamma ** 3 // 500:
                pace_checks[0] += 1
    node.step()
exact = 0
for k in range(len(hashes)):
    node.step_back()
    exact += node.state_hash() == hashes[len(hashes) - 1 - k]
# the vacuum's rule bit for bit the default's: the reach at p_i = p_j = Gamma
from event_universe.core import rule3
vac = node.rule((node.den, node.den), np.full(node.shape, 0, dtype=object), node.link_factors())
vac_default = rule3.rule_integers(node.den, node.den, gamma, np.full(node.shape, gamma, dtype=object), np.full(node.shape, gamma, dtype=object), node.link_factors(), node.G)
vac_same = all(bool(np.all(a == b)) for a, b in zip(vac.reaches, vac_default.reaches)) and bool(np.all(vac.self_coefficient == vac_default.self_coefficient))
print(json.dumps({
    "form": form,
    "ports with a gradient (20 intervals, every riding row and the carrier)": links_with_gradient,
    "of them with R_ij == R_ji": equal_ports,
    "plain Links' sum per interval (carrier)": sums,
    "Links' sum 0 at every interval": all(s == 0 for s in sums),
    "Links' sum positive at every interval": all(s > 0 for s in sums),
    "P_ij (X_i + X_j) within the rounding of 2 Gamma^3 (checks passed / made)": pace_checks,
    "vacuum rule bit for bit the default": vac_same,
    "run back": [exact, len(hashes)],
    "census (integers, bits)": list(node.census()),
    "seconds": (time.monotonic_ns() - t0) // 1000000000,
}))
