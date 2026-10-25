"""pm1's readings on the board under the flagged copy: a world run step by step (the flag from its key), and every `every` intervals,
per row, the board's sums of the share at the three weights (the vacuum's 4 Gamma^2 G^2, the frame's 4 p_i^2 G^2 = the carrier's unit,
the clock's 4 p_0^2 G^2), the content's min and max, the carrier's level X max, the counts; at the end the identity (Gamma / p_i)^2
against X / Gamma at every distinct content met (quotient, remainder, deviation per mille) and the per-row factor at the Node of the
largest content. Integers only. Usage: python pm1_shares.py <world.json> <every> <out.json>"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'src_pm1'))
import numpy as np
from event_universe import readings
from event_universe.core import paces as P
from event_universe.loader.world import read_world
from event_universe.node import Node
from event_universe.features import volume

sys.set_int_max_str_digits(0)
where, every, out_path = sys.argv[1], int(sys.argv[2]), sys.argv[3]
world = json.loads(open(where).read())
readings.WEIGHT = world.pop('pm1_weight', 'default')
universe = json.loads(open(os.path.join(os.path.dirname(where), world['universe'])).read())
read_world(world, universe)
node = Node(universe, world)
ints = lambda a: [int(x) for x in np.asarray(a, dtype=object).reshape(-1)]


def sums():
    c = node.content()
    node.start_content = c
    factors = node.link_factors()
    pace = P.link_pace_of(node.gamma, c)
    p0 = P.clock_of(node.gamma, c)
    found = []
    for rec, r in enumerate(node.records()):
        rr = node.rule_of(r, c, factors)
        re, im = r.lines
        row = {}
        for tag, sq_pace in (('vacuum', None), ('link', pace), ('clock', p0)):
            if tag == 'vacuum':
                s = node.share(re, rr, pace, vacuum=True) + node.share(im, rr, pace, vacuum=True)
            else:
                keep = readings.WEIGHT
                readings.WEIGHT = 'link'
                s = node.share(re, rr, sq_pace, vacuum=False) + node.share(im, rr, sq_pace, vacuum=False)
                readings.WEIGHT = keep
            v = ints(s)
            row[tag] = {'sum': sum(v), 'max': max(v), 'whole_nodes': sum(1 for x in v if x >= node.units[rec])}
        found.append(row)
    cs = ints(c)
    return {'i': node.interval, 'content_min_max': [min(cs), max(cs)], 'X_max': max(ints(node.row(10).lines[0].now)),
            'rows': found, 'counts': dict(node.counts)}

marks = [sums()]
for t in range(int(world['intervals'])):
    node.step()
    if node.interval % every == 0:
        marks.append(sums())
        print(json.dumps(marks[-1]), flush=True)
# the identity (Gamma / p_i)^2 against X / Gamma at every distinct content met
seen = sorted(set(x for m in marks for x in range(m['content_min_max'][0], m['content_min_max'][1] + 1)))
seen = [c for c in seen if c >= 0][:: max(1, len(seen) // 40)]
identity = []
for c in seen:
    pi = P.link_pace(node.gamma, c)
    p0 = P.clock(node.gamma, c)
    X = int(np.asarray(volume.volume_of(node.gamma, np.array([c], dtype=object)), dtype=object).reshape(-1)[0])
    if pi == 0:
        identity.append({'content': c, 'p_i': 0, 'X_over_Gamma': [X // node.gamma, X % node.gamma]}); continue
    lhs = (node.gamma * node.gamma) // (pi * pi), (node.gamma * node.gamma) % (pi * pi)
    rhs = X // node.gamma, X % node.gamma
    dev = ((lhs[0] - rhs[0]) * 1000) // max(1, rhs[0])
    identity.append({'content': c, 'p_0': p0, 'p_i': pi, 'Gamma2_over_pi2': list(lhs), 'X_over_Gamma': list(rhs), 'dev_per_mille': dev, 'clock_Gamma2_over_p02': [(node.gamma * node.gamma) // (p0 * p0)]})
json.dump({'pm1_weight': readings.WEIGHT, 'marks': marks, 'identity': identity}, open(out_path, 'w'))
print(json.dumps({'identity': identity}))
