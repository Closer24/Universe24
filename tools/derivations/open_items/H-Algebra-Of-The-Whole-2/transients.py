"""The transients' census beyond rotate's totals (the record's 'max transient bits' reads rotate alone): the share's product (o + o - s) X before its division (gram.share), the carrier's write numerator (held_numerator), the kick's products u_in (G u_out) and the pulls, the emission's numerator, the sign row's write 2 W, and the take's fall numerator x (w (now^2 - (now + s)^2) - s pull), each the largest bit length over the Nodes per interval, the maxima over the run; integers only; the engine's own Interval driven act by act (a reader of its readings, the state as the engine leaves it)."""
import json
import sys

import numpy as np

from event_universe import gram, interval as interval_module
from event_universe.core.rule3 import held_numerator
from event_universe.rows import TRACE, CARRIER
from tests.laws import node_of

sys.set_int_max_str_digits(0)


def bits(a):
    return max(abs(int(v)).bit_length() for v in np.asarray(a, dtype=object).reshape(-1))


for name, n in (("world_hole.json", 60), ("world_chiral.json", 60), ("world_bodies.json", 40)):
    node = node_of(name)
    found = {}
    for t in range(n):
        it = interval_module.Interval(node, 1)
        it.walled_act()
        it.forces()
        it.kicks()
        it.carrier_act()
        it.divisions()
        it.writes()
        node.set_rows(it.out)
        it.rest()
        # the share's product before its division, at every record at its unscaled rule
        c, factors = node.start_content, node.start_factors
        share_bits = 0
        for r in node.records():
            rule = node.rule(r.pair, c, factors)
            lines = r.lines
            g = gram.gram(len(lines))
            nows, befores = [l.now for l in lines], [l.before for l in lines]
            own = [rule.wall * (nn + bb) - rule.self_coefficient * nb for nn, bb, nb in zip(gram.weighted(g, nows, nows), gram.weighted(g, befores, befores), gram.weighted(g, nows, befores), strict=True)]
            share_bits = max(share_bits, max(bits((o + o) * node.start_x) for o in own))
        kick_bits = max(bits(it.forms), max(bits(f) for k in it.force for f in it.force[k]))
        numerator = held_numerator(TRACE, it.x_now, it.forms, it.trace, it.p0, node.den, node.gamma)
        emission_bits = bits(it.emission)
        sign_bits = bits(2 * it.w_after)
        for key, value in (("share product (o + o) X", share_bits), ("forces and forms", kick_bits), ("carrier write numerator", bits(numerator)), ("emission numerator", emission_bits), ("sign write 2 W", sign_bits), ("mean wall W", bits(it.w_div)), ("rotate totals (the record's)", node.max_transient)):
            found[key] = max(found.get(key, 0), value)
        it.close()
    found["state (census)"] = node.census()[1]
    print(json.dumps({"world": name, "intervals": n, "bits": found}))
