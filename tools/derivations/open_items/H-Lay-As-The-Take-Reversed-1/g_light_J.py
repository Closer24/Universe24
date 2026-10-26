"""(g) The light's own angular momentum read as the Link's record under the slot, on the board run by the engine (the flagged copy, LT1_RECOIL=1): per interval, for the gap-0 plane (the light), the current F(i, i + a) on the +a Link of every Node from the record's two slots (links.link_current), the Link's momentum p = -2 num F along its axis; (1) the moment of the six Links' records about the Node, SUM over the Node's six Links of (2 r_link) x (p e_a) with 2 r_link = +-e_a (an integer vector; 0 by the geometry: a Link's record lies along the Link), counted at every Node; (2) 2J of the light about the board's centre Node, SUM_i 2 (r_i - c) x P_i with P_i(a) = p(i, i + a) (the Node's own +a Links), in the unit num (every p a multiple of 2 num), its remainders modulo T div 2 (the charge's unit) and modulo den; (3) the Node's one pseudo-vector, the curl of the shape-4 row's three odd lines (gram.curl, the sign current's curl), summed over the board and its largest entry; (4) the emission's lays (counts laid, laid_nodes). Usage: g_light_J.py <world.json> <intervals> <out.json>"""
import json
import os
import sys

for path in reversed(os.environ.get("PYTHONPATH", "").split(":")):
    if path:
        sys.path.insert(0, path)
sys.set_int_max_str_digits(0)

import numpy as np  # noqa: E402

from event_universe import gram  # noqa: E402
from event_universe.core.ports import AXES, port_of  # noqa: E402
from event_universe.links import link_current  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402
from event_universe.rows import POTENTIAL  # noqa: E402


def cross3(r, p):
    return [r[1] * p[2] - r[2] * p[1], r[2] * p[0] - r[0] * p[2], r[0] * p[1] - r[1] * p[0]]


u, w = load_world(sys.argv[1])
node = Node(u, w)
intervals = int(sys.argv[2])
emitter = node.emitter()
num = emitter.pair[0]
half_t = node.T // 2
cube = node.cube
c = [cube // 2] * AXES
rows = []
moment_nonzero = 0
moment_count = 0
for t in range(intervals):
    node.step()
    line = emitter.lines[0]
    f_plus = [link_current(line, port_of(a, 0)) for a in range(AXES)]
    f_minus = [link_current(line, port_of(a, 1)) for a in range(AXES)]
    j2 = [0, 0, 0]
    p_sum = [0, 0, 0]
    for idx in np.ndindex(node.shape):
        p_plus = [-2 * num * int(f_plus[a][idx]) for a in range(AXES)]
        p_minus = [-2 * num * int(f_minus[a][idx]) for a in range(AXES)]
        # (1) the moment about the Node of its six Links' records
        m = [0, 0, 0]
        for a in range(AXES):
            e = [0, 0, 0]
            e[a] = 1
            m = [x + y for x, y in zip(m, cross3(e, [p_plus[a] * v for v in e]))]
            m = [x + y for x, y in zip(m, cross3([-v for v in e], [p_minus[a] * v for v in e]))]
        moment_count += 1
        moment_nonzero += m != [0, 0, 0]
        # (2) 2J about the centre Node, the Node's own +a Links as its momentum
        arm = [2 * (((idx[a] - c[a] + cube // 2) % cube) - cube // 2) for a in range(AXES)]
        j2 = [x + y for x, y in zip(j2, cross3(arm, p_plus))]
        p_sum = [x + y for x, y in zip(p_sum, p_plus)]
    odd = [line_.now for line_ in node.row(POTENTIAL).lines[1 : 1 + AXES]]
    curl = gram.curl(odd)
    curl_sum = [int(np.sum(cv)) for cv in curl]
    curl_max = max(int(abs(int(v))) for cv in curl for v in cv.reshape(-1))
    j2_num = [x // (2 * num) for x in j2]
    rows.append(
        {
            "i": node.interval,
            "P of the light per axis (unit 2 num)": [x // (2 * num) for x in p_sum],
            "2J of the light about the centre (unit 2 num)": j2_num,
            "2J mod T div 2": [x % half_t for x in j2_num],
            "2J mod den": [x % node.den for x in j2_num],
            "curl of the odd lines summed": curl_sum,
            "curl largest entry": curl_max,
            "W total of the light": int(np.sum(gram.charge(emitter.shape, emitter.lines))),
        }
    )
out = {
    "world": sys.argv[1],
    "intervals": intervals,
    "num": num,
    "den": node.den,
    "T div 2": half_t,
    "moment of the six Links' records about the Node: Node-intervals with a nonzero moment": [moment_nonzero, moment_count],
    "emission lays (counts laid, laid_nodes)": [node.counts["laid"], node.counts["laid_nodes"]],
    "births": node.counts["births"],
    "rows at the first, middle and last interval": [rows[0], rows[len(rows) // 2], rows[-1]],
    "intervals with 2J of the light 0 on three axes": sum(1 for r in rows if r["2J of the light about the centre (unit 2 num)"] == [0, 0, 0]),
    "intervals with 2J a multiple of T div 2 on three axes": sum(1 for r in rows if r["2J mod T div 2"] == [0, 0, 0]),
    "intervals with the curl summed 0 on three axes": sum(1 for r in rows if r["curl of the odd lines summed"] == [0, 0, 0]),
}
with open(sys.argv[3], "w") as f:
    json.dump({"summary": out, "rows": rows}, f)
print(json.dumps(out, default=str))
