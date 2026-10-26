"""tw2's probe of the held write's two sources (the forms and the stress's trace) at the interval's start, under the
flagged copy: a world is loaded, stepped `after` intervals, and the next interval's readings are taken through the
Node's own acts (Interval: the readings, the walled row's act, the forces, the kicks) and summed over the board:
F = SUM forms den Gamma^2 and Q = SUM trace p_0^2 (the two terms of the time line's numerator at the weight 1),
so the weight t at which the time line's write would vanish on the board's sum is t_b = Q / F, printed in
thousandths by the division act (integers only), with the per-Node least and greatest of the same ratio where
forms is not 0, the count of Nodes whose write at the head's 54 is negative, and the traceless parts' sum of
squares. Usage: probe_tw2.py <world.json> <after>"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "src_tw2"))

import numpy as np  # noqa: E402

from event_universe import interval as iv  # noqa: E402
from event_universe.core.rule3 import quotient  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402

THOUSAND = 1000


def thousandths(num, den):
    """num / den in thousandths by the division act, the sign kept."""
    if den == 0:
        return None
    sign = 1 if (num >= 0) == (den > 0) else -1
    return sign * int(quotient(abs(num) * THOUSAND, abs(den)))


def main(argv):
    sys.set_int_max_str_digits(0)
    universe, world = load_world(argv[1])
    after = int(argv[2])
    node = Node(universe, world)
    for _ in range(after):
        node.step()
    it = iv.Interval(node, 1)
    it.walled_act()
    it.forces()
    it.kicks()
    den, gamma = node.den, node.gamma
    forms = [int(x) for x in it.forms.reshape(-1)]
    trace = [int(x) for x in it.trace.reshape(-1)]
    p0 = [int(x) for x in np.asarray(it.p0, dtype=object).reshape(-1)]
    x_now = [int(x) for x in np.asarray(it.x_now, dtype=object).reshape(-1)]
    f_terms = [f * den * gamma * gamma for f in forms]
    q_terms = [q * p * p for q, p in zip(trace, p0)]
    F, Q = sum(f_terms), sum(q_terms)
    ratios = [thousandths(q, f) for q, f in zip(q_terms, f_terms) if f != 0]
    negative_54 = sum(1 for f, q in zip(f_terms, q_terms) if 54 * f - q < 0)
    positive_54 = sum(1 for f, q in zip(f_terms, q_terms) if 54 * f - q > 0)
    traceless_sq = sum(int(v) * int(v) for a in it.traceless for v in a.reshape(-1))
    out = {
        "world": os.path.basename(argv[1]),
        "after": after,
        "nodes": len(forms),
        "nodes with forms": sum(1 for f in forms if f != 0),
        "nodes with trace": sum(1 for q in trace if q != 0),
        "forms sum": sum(forms),
        "trace sum": sum(trace),
        "forms min/max": [min(forms), max(forms)],
        "trace min/max": [min(trace), max(trace)],
        "p0 min/max": [min(p0), max(p0)],
        "X min/max": [min(x_now), max(x_now)],
        "F = SUM forms den Gamma^2": str(F),
        "Q = SUM trace p0^2": str(Q),
        "t_b = Q / F (thousandths)": thousandths(Q, F),
        "per-Node Q / F (thousandths) least/greatest": [min(ratios), max(ratios)] if ratios else None,
        "Nodes whose write at 54 is negative/positive": [negative_54, positive_54],
        "traceless sum of squares bits": traceless_sq.bit_length(),
        "lay log": [e for e in node.log if e.get("event") == "lay"][:3],
    }
    print(json.dumps(out))


if __name__ == "__main__":
    main(sys.argv)
