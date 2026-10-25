"""bg2: the course of the mean volume decomposed at the Node, integers only (2026-10-25).

The engine is imported and never changed: two methods are wrapped from outside (Interval.kicks and Node.write)
to read, at every interval, what the carrier's time line receives: the mass pull of its own pair (D X_now div w,
the gapped carrier's restoring term, 2 p_0^2 X div Gamma^3), the write's quotient on the time line (keyed by the
line's write wall 54 den Gamma^4 T, the carrier's time line alone), and the write's source `forms` split by row
kind: the gap-0 plane (the sea), the gapped planes (the lifts, the bodies), the shape-4 row (the potential).

Usage: bg2_course.py <world.json> <out.json> [every]
Prints one line per `every` intervals; writes every interval to <out.json>.
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.environ.get("BG2_SRC", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "src")))

from event_universe import interval as interval_module  # noqa: E402
from event_universe.core import paces  # noqa: E402
from event_universe.core.rule3 import held_wall, quotient  # noqa: E402
from event_universe.core.ports import across  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402
from event_universe.rows import CARRIER, PLANE, POTENTIAL, TRACE  # noqa: E402


def tot(a):
    return int(np.sum(np.asarray(a, dtype=object)))


LOG = {"forms": {}, "write": 0, "mass": 0}

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
    spread = 0
    for port in range(6):
        d_ = np.abs(np.asarray(self.x_now, dtype=object) - across(self.x_now, port))
        spread = max(spread, int(np.max(d_)))
    LOG["spread"] = spread
    LOG["p0_mean"] = tot(self.p0)


def write(self, line, numerator, direction):
    before = line.now
    _write(self, line, numerator, direction)
    if line.wwall == held_wall(TRACE, self.den, self.gamma, self.T, 4):
        LOG["write"] = tot(line.now - before)


interval_module.Interval.kicks = kicks
Node.write = write


def main(argv):
    sys.set_int_max_str_digits(0)
    universe, world = load_world(argv[1])
    every = int(argv[3]) if len(argv) > 3 else 100
    node = Node(universe, world)
    n = 1
    for x in node.shape:
        n *= x
    x_line = node.row(CARRIER).lines[0]
    rows = []
    print(json.dumps({"nodes": n, "gamma": node.gamma, "den": node.den, "T": node.T}))
    prev_turns = 0
    for t in range(int(world["intervals"])):
        x_line = node.row(CARRIER).lines[0]
        x_before, x_now = x_line.before.copy(), x_line.now.copy()
        node.step()
        x_next = node.row(CARRIER).lines[0].now
        acc = tot(x_next - 2 * x_now + x_before)
        row = {
            "i": node.interval,
            "X sum": tot(x_now), "X min": int(np.min(x_now)), "X max": int(np.max(x_now)),
            "content mean": int(tot(node.content())) // n,
            "p0 sum": LOG.get("p0_mean", 0),
            "X'' sum": acc,
            "mass pull sum": LOG["mass"],
            "links sum": LOG.get("links", 0),
            "neighbour spread max": LOG.get("spread", 0),
            "write sum": LOG["write"],
            "forms gap0": LOG["forms"].get("gap0", 0),
            "forms gapped": LOG["forms"].get("gapped", 0),
            "forms potential": LOG["forms"].get("potential", 0),
            "turns at i": node.counts["turns"] - prev_turns,
            "births": node.counts["births"],
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
