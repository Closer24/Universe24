"""pm1's read of the gap-0 row's own credits under the flag (the owner's word of 15:0x UTC: does light click?): the world run in-process
with close.click wrapped; at every credit of the gap-0 row: (a) a Link of the Node had both ends at a whole quantum of the gap-0 row at the
interval's start (the meeting's condition: a PAIR met, and the close birthed there or refused by name: the refusals logged at that Node
that interval counted by cause), or (b) no neighbour whole (ONE quantum standing alone). Also the sense (the Wronskian's sign: 0 the drift),
the beat and the content. Integers only. Usage: python analyze_light.py <world.json> <out.json>"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'src_pm1'))
import numpy as np
from event_universe import close, readings
from event_universe.core import paces
from event_universe.loader.world import read_world
from event_universe.node import Node
from event_universe.rows import PLANE
from event_universe.take import neighbour

sys.set_int_max_str_digits(0)
where, out_path = sys.argv[1], sys.argv[2]
world = json.loads(open(where).read())
readings.WEIGHT = world.pop('pm1_weight', 'default')
universe = json.loads(open(os.path.join(os.path.dirname(where), world['universe'])).read())
read_world(world, universe)
node = Node(universe, world)
gap0 = node.row(PLANE, gap=0)
rec0 = node.records().index(gap0)
found = []
original = close.click

def wrapped(node, plane_starts, held):
    c = node.start_content
    factors = node.link_factors()
    pace = paces.link_pace_of(node.gamma, c)
    shares = []
    for rec, r in enumerate(node.records()):
        rr = node.rule_of(r, c, factors)
        re0, im0 = plane_starts[rec]
        shares.append(node.share(re0, rr, pace, vacuum=True) + node.share(im0, rr, pace, vacuum=True))
    log_from = len(node.log)
    original(node, plane_starts, held)
    new = node.log[log_from:]
    for e in new:
        if e['event'] == 'credit':
            at = tuple(e['node'])
            sh, unit = shares[e['line']], node.units[e['line']]
            whole_here = int(sh[at]) >= unit
            whole_neighbours = sum(1 for port in range(6) if int(sh[neighbour(node, at, port)]) >= unit)
            refusals = {}
            for r in new:
                if r['event'] == 'refused' and tuple(r['node']) == at:
                    refusals[r['cause']] = refusals.get(r['cause'], 0) + 1
            births_here = sum(1 for r in new if r['event'] == 'birth' and (tuple(r['node']) == at or tuple(r['minus']) == at or tuple(r['plus']) == at))
            found.append({'row': e['line'], 'gap': node.records()[e['line']].gap, 'i': e['i'], 'node': list(at), 'sense': e['sense'], 'beat': e['beat'], 'content': e['content'],
                          'share_over_unit': int(sh[at]) // unit, 'whole_here': whole_here, 'whole_neighbours': whole_neighbours,
                          'kind': 'a_pair_met' if whole_neighbours > 0 else 'b_one_standing', 'refusals_at_node': refusals, 'births_touching': births_here,
                          're_now': e['frame']['re_now'], 'im_now': e['frame']['im_now'], 'taken': e['taken']})

close.click = wrapped
for t in range(int(world['intervals'])):
    node.step()
kinds = {}
for f in found:
    k = str(f['row']) + ' gap ' + str(f['gap']) + ' ' + f['kind']
    kinds[k] = kinds.get(k, 0) + 1
by_interval = {}
for f in found:
    by_interval[f['i']] = by_interval.get(f['i'], 0) + 1
nodes = {}
for f in found:
    nodes[str(f['node'])] = nodes.get(str(f['node']), 0) + 1
senses = {}
for f in found:
    senses[f['sense']] = senses.get(f['sense'], 0) + 1
refused_total = {}
for f in found:
    for k, v in f['refusals_at_node'].items():
        refused_total[k] = refused_total.get(k, 0) + v
summary = {'weight': readings.WEIGHT, 'gap0_credits': len(found), 'kinds': kinds, 'senses': senses, 'records_order_gaps': [r.gap for r in node.records()], 'gap0_index': rec0, 'first_last_interval': [found[0]['i'], found[-1]['i']] if found else None,
           'distinct_nodes': len(nodes), 'top_nodes': sorted(nodes.items(), key=lambda kv: -kv[1])[:8], 'intervals_with_credits': len(by_interval),
           'refusals_at_credit_nodes': refused_total, 'births_touching_total': sum(f['births_touching'] for f in found),
           'beat_min_max': [min(f['beat'] for f in found), max(f['beat'] for f in found)] if found else None,
           'content_min_max': [min(f['content'] for f in found), max(f['content'] for f in found)] if found else None,
           'share_over_unit_min_max': [min(f['share_over_unit'] for f in found), max(f['share_over_unit'] for f in found)] if found else None,
           'whole_neighbours_hist': {str(k): sum(1 for f in found if f['whole_neighbours'] == k) for k in range(7)},
           'counts': dict(node.counts)}
json.dump({'summary': summary, 'credits': found}, open(out_path, 'w'))
print(json.dumps(summary))
