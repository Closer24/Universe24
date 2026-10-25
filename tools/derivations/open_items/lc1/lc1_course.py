"""lc1: the Link's current read on the board at every interval, integers only (2026-10-25).

The engine (David's src, or the flagged copy named by LC1_SRC) is imported and never changed: Interval.kicks is wrapped
from outside to read, after the kick, what every Link gives at its two ends, and Node.write to read the carrier's time
line's write. Per interval:
  the carrier's time line: the Links' numerator SUM_i SUM_j R_ij (X_j - X_i) (an exact integer; 0 by identity when
  R_ij = R_ji), its absolute sum SUM_i |SUM_j R_ij (X_j - X_i)|, the per-Node quotients' sum SUM_i (that div w)
  (bg2's "links sum", the lift in X'' with the roundings' residue), the volume-weighted numerator
  SUM_i X_i SUM_j R_ij (X_j - X_i) (the law's conserved current, 0 to the rounding of X_i p_i^2 against Gamma^3),
  the mass pull SUM_i (D X div w), the write on the time line, the forms by row kind;
  the gap-0 line (the sea): the Links' part of the kick, SUM_i X_i (SUM_j R_ij a_j - SUM_j R_ij a_i) on the re line,
  exact, and its absolute sum: the riding momentum's Link current (one number from both ends when X_i R_ij = X_j R_ji);
  the board: X sum / min / max, the content mean, the spread e of the neighbours in thousandths
  (e^2 = 10^6 SUM_Links (X_j - X_i)^2 div SUM_Links X_i X_j, e = largest_below), the largest Link spread in thousandths,
  the turned Nodes (count and indices while few), births and body credits (cumulative).
Usage: lc1_course.py <world.json> <out.json> [every]; LC1_SRC the src folder; LC1_FLAG the copy's flag.
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.environ.get("LC1_SRC", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "src")))

from event_universe import interval as interval_module  # noqa: E402
from event_universe.core import paces  # noqa: E402
from event_universe.core.ports import PORTS, across  # noqa: E402
from event_universe.core.rule3 import held_wall, largest_below, quotient  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402
from event_universe.rows import CARRIER, PLANE, POTENTIAL, TRACE  # noqa: E402


def tot(a):
    return int(np.sum(np.asarray(a, dtype=object)))


def tot_abs(a):
    return int(np.sum(np.abs(np.asarray(a, dtype=object))))


LOG = {}

_kicks = interval_module.Interval.kicks
_write = Node.write


def link_part(node, levels, rule):
    """SUM_j R_ij (m_j - a_i) at every Node for a plain line: the arrivals less the reaches' sum times the level."""
    arrivals = node.arrivals([levels], rule, None)[0]
    return arrivals - sum(rule.reaches) * levels


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
    x = np.asarray(self.x_now, dtype=object)
    rule = node.rule_of(self.carrier, self.c, self.factors)
    LOG["mass"] = tot(quotient(rule.mass * x, node.w))
    links = link_part(node, x, rule)
    LOG["c_links_num"] = tot(links)
    LOG["c_links_abs"] = tot_abs(links)
    LOG["c_links_quot"] = tot(quotient(links, node.w))
    LOG["c_links_wnum"] = tot(x * links)
    LOG["c_links_wabs"] = tot_abs(x * links)
    # the identity X_i p_i^2 = Gamma^3 to the rounding: the residue over the board
    pace = np.asarray(self.pi, dtype=object)
    ident = x * pace * pace - node.gamma ** 3
    LOG["ident_abs_sum"] = tot_abs(ident)
    LOG["ident_max"] = int(np.max(np.abs(ident)))
    # the sea's re line: the riding momentum's Link current, X_i SUM_j R_ij (a_j - a_i)
    gap0 = self.gap0
    rule0 = node.rule_of(gap0, self.c, self.factors)
    a_re = np.asarray(self.starts[self.where[id(gap0)]][0], dtype=object)
    kick = x * link_part(node, a_re, rule0)
    LOG["sea_kick_num"] = tot(kick)
    LOG["sea_kick_abs"] = tot_abs(kick)
    # the spread of the neighbours
    s2, sp, emax = 0, 0, 0
    for port in range(0, PORTS, 2):
        xj = across(x, port)
        dd = xj - x
        s2 += tot(dd * dd)
        sp += tot(x * xj)
        lo = np.minimum(x, xj)
        e_link = np.vectorize(lambda a, b: (1000 * abs(int(a))) // int(b), otypes=[object])(dd, lo)
        emax = max(emax, int(np.max(e_link)))
    LOG["e2"] = (1000000 * s2) // sp if sp else 0
    LOG["e"] = largest_below(LOG["e2"])
    LOG["e_max"] = emax
    LOG["p0_sum"] = tot(self.p0)


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
    every = int(argv[3]) if len(argv) > 3 else 50
    node = Node(universe, world)
    n = 1
    for x in node.shape:
        n *= x
    print(json.dumps({"nodes": n, "gamma": node.gamma, "den": node.den, "T": node.T, "flag": os.environ.get("LC1_FLAG", ""), "seed X sum": tot(node.row(CARRIER).lines[0].now)}))
    rows = []
    prev_turns, prev_births, prev_credits = 0, 0, 0
    for t in range(int(world["intervals"])):
        x_line = node.row(CARRIER).lines[0]
        x_before, x_now = x_line.before.copy(), x_line.now.copy()
        node.step()
        x_next = node.row(CARRIER).lines[0].now
        turned = [i for i, v in enumerate(node.turned.reshape(-1).tolist()) if v]
        row = {
            "i": node.interval,
            "X sum": tot(x_now), "X min": int(np.min(x_now)), "X max": int(np.max(x_now)),
            "content mean": tot(node.content()) // n,
            "p0 sum": LOG["p0_sum"],
            "X'' sum": tot(x_next - 2 * x_now + x_before),
            "mass pull sum": LOG["mass"],
            "carrier links num": LOG["c_links_num"], "carrier links abs": LOG["c_links_abs"],
            "carrier links quot": LOG["c_links_quot"],
            "carrier links wnum": LOG["c_links_wnum"], "carrier links wabs": LOG["c_links_wabs"],
            "ident abs sum": LOG["ident_abs_sum"], "ident max": LOG["ident_max"],
            "sea kick num": LOG["sea_kick_num"], "sea kick abs": LOG["sea_kick_abs"],
            "e": LOG["e"], "e max": LOG["e_max"],
            "write sum": LOG.get("write", 0),
            "forms gap0": LOG["forms"]["gap0"], "forms gapped": LOG["forms"]["gapped"], "forms potential": LOG["forms"]["potential"],
            "turns at i": len(turned), "turned": turned if len(turned) <= 4 else [],
            "births": node.counts["births"], "body_clicks": node.counts["body_clicks"],
            "births at i": node.counts["births"] - prev_births, "credits at i": node.counts["body_clicks"] - prev_credits,
            "frozen": int(sum(1 for p in np.asarray(paces.link_pace_of(node.gamma, node.content()), dtype=object).reshape(-1) if int(p) == 0)),
        }
        prev_turns, prev_births, prev_credits = node.counts["turns"], node.counts["births"], node.counts["body_clicks"]
        rows.append(row)
        if node.interval % every == 0 or node.interval <= 2:
            print(json.dumps(row), flush=True)
    with open(argv[2], "w") as f:
        json.dump(rows, f)
    print(json.dumps({"counts": {k: str(v) for k, v in node.counts.items()}, "census": list(node.census())}))


if __name__ == "__main__":
    main(sys.argv)
