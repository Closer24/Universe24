"""bb2: the course of the carrier's time line decomposed at the Node, integers only (2026-10-25), extended from bg2_course.py (open_items/bg2): the same wrap of Interval.kicks and Node.write, with the neighbours' spread read per Link in thousandths (1000 |X_j - X_i| div min(X_i, X_j)), the count of Links at or above the threshold given, the mean, and the exact return (every Node at the seed's X).

Usage: bb2_course.py <world.json> <out.json> [every] [threshold_thousandths]
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.environ.get("BB2_SRC", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "src")))

from event_universe import interval as interval_module  # noqa: E402
from event_universe.core import paces  # noqa: E402
from event_universe.core.rule3 import held_wall, quotient  # noqa: E402
from event_universe.core.ports import across  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402
from event_universe.rows import CARRIER, POTENTIAL, TRACE  # noqa: E402


def tot(a):
    return int(np.sum(np.asarray(a, dtype=object)))


LOG = {"forms": {}, "write": 0, "mass": 0}
THRESHOLD = 63

_kicks = interval_module.Interval.kicks
_write = Node.write


def kicks(self):
    _kicks(self)
    node = self.node
    d = 2 * node.w * self.x_now
    found = {"gap0": 0, "gapped": 0, "potential": 0}
    for r in self.riders:
        k = self.where[id(r)]
        kind = "potential" if r.shape == POTENTIAL else ("gap0" if r.gap == 0 else "gapped")
        w_side = self.mean_wall()
        p_side = [w_side * (line.now - line.before) + line.rem - (w_side // 2) for line in self.rows[k]]
        p_other = [p + self.direction * self.x_now * f for p, f in zip(p_side, self.force[k])]
        s = 0
        for a, f, p1, p2 in zip(self.starts[k], self.force[k], p_side, p_other):
            s = s + paces.odd_rounded(2 * p1 + 1, d) * paces.odd_rounded(2 * p2 + 1, d) + quotient(-a * f, node.w)
        found[kind] += tot(s)
    LOG["forms"] = found
    rule = node.rule_of(self.carrier, self.c, self.factors)
    LOG["mass"] = tot(quotient(rule.mass * self.x_now, node.w))
    arrivals = node.arrivals([self.x_now], rule, None)[0]
    LOG["links"] = tot(quotient(arrivals - sum(rule.reaches) * self.x_now, node.w))
    x = np.asarray(self.x_now, dtype=object)
    e_max = 0
    above = 0
    e_sq_sum = 0
    for port in (0, 2, 4):
        y = across(x, port)
        for xi, yi in zip(x.reshape(-1), y.reshape(-1)):
            xi, yi = int(xi), int(yi)
            lo = min(xi, yi)
            e = (1000 * abs(xi - yi)) // lo if lo > 0 else 10 ** 9
            e_max = max(e_max, e)
            e_sq_sum += e * e
            if e >= THRESHOLD:
                above += 1
    LOG["e_max"] = e_max
    LOG["links_above"] = above
    LOG["e_sq_sum"] = e_sq_sum
    LOG["p0_sum"] = tot(self.p0)


def write(self, line, numerator, direction):
    before = line.now
    _write(self, line, numerator, direction)
    if line.wwall == held_wall(TRACE, self.den, self.gamma, self.T, 4):
        LOG["write"] = tot(line.now - before)


interval_module.Interval.kicks = kicks
Node.write = write


def main(argv):
    global THRESHOLD
    sys.set_int_max_str_digits(0)
    universe, world = load_world(argv[1])
    every = int(argv[3]) if len(argv) > 3 else 100
    THRESHOLD = int(argv[4]) if len(argv) > 4 else 63
    node = Node(universe, world)
    n = 1
    for x in node.shape:
        n *= x
    seed_x = [int(v) for v in np.asarray(node.row(CARRIER).lines[0].now, dtype=object).reshape(-1)]
    rows = []
    print(json.dumps({"nodes": n, "gamma": node.gamma, "den": node.den, "T": node.T, "seed X": [min(seed_x), max(seed_x)], "threshold": THRESHOLD}))
    prev_turns = 0
    for t in range(int(world["intervals"])):
        x_line = node.row(CARRIER).lines[0]
        x_before, x_now = x_line.before.copy(), x_line.now.copy()
        node.step()
        x_next = node.row(CARRIER).lines[0].now
        acc = tot(x_next - 2 * x_now + x_before)
        xs = [int(v) for v in np.asarray(x_next, dtype=object).reshape(-1)]
        row = {
            "i": node.interval,
            "X sum": tot(x_now), "X min": int(np.min(x_now)), "X max": int(np.max(x_now)),
            "X mean": tot(x_now) // n,
            "X next mean": sum(xs) // n,
            "at seed": sum(1 for a, b in zip(xs, seed_x) if a == b),
            "content mean": int(tot(node.content())) // n,
            "p0 sum": LOG.get("p0_sum", 0),
            "X'' sum": acc,
            "mass pull sum": LOG["mass"],
            "links sum": LOG.get("links", 0),
            "write sum": LOG["write"],
            "e max": LOG.get("e_max", 0),
            "links above": LOG.get("links_above", 0),
            "e sq sum": LOG.get("e_sq_sum", 0),
            "forms gap0": LOG["forms"].get("gap0", 0),
            "forms gapped": LOG["forms"].get("gapped", 0),
            "forms potential": LOG["forms"].get("potential", 0),
            "turns at i": node.counts["turns"] - prev_turns,
            "births": node.counts["births"],
            "refused_lay": node.counts["refused_lay"],
            "body_clicks": node.counts["body_clicks"],
        }
        prev_turns = node.counts["turns"]
        rows.append(row)
        if node.interval % every == 0 or node.interval <= 3:
            print(json.dumps(row), flush=True)
    with open(argv[2], "w") as f:
        json.dump(rows, f)
    print(json.dumps({"counts": {k: str(v) for k, v in node.counts.items()}, "census": node.census()}))


if __name__ == "__main__":
    main(sys.argv)
