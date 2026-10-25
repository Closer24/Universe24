"""sp1: the batch of Stern-Gerlach runs (sp1_sg.run on each configuration), the outputs under out/, one summary table in integers.
Usage: python sp1_batch.py <cube> <intervals> <back>"""
from __future__ import annotations
import sys, os, json, argparse, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sp1_sg

cube, intervals, back = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
configs = []
for sense in (1, -1, 0):
    configs.append(('control_s%+d' % sense, dict(sense=sense, odd='none', strength=0, held=False)))
    configs.append(('uniform200_s%+d' % sense, dict(sense=sense, odd='uniform', strength=200, held=False)))
    configs.append(('grad50_set_s%+d' % sense, dict(sense=sense, odd='gradient', strength=50, held=False)))
    configs.append(('grad50_held_s%+d' % sense, dict(sense=sense, odd='gradient', strength=50, held=True)))
    configs.append(('grad200_held_s%+d' % sense, dict(sense=sense, odd='gradient', strength=200, held=True)))
os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
table = []
for name, cfg in configs:
    args = argparse.Namespace(universe='universe_middle.json', cube=cube, intervals=intervals, row=2, width=3, quanta=218, sense=cfg['sense'], odd=cfg['odd'], strength=cfg['strength'],
                              line_axis=0, vary_axis=1, held=cfg['held'], sea=1, back=back, every=10, images48=False, out=None)
    t0 = time.monotonic_ns()
    found, b = sp1_sg.run(args, None, False)
    ms = (time.monotonic_ns() - t0) // 1000000
    json.dump(found, open(os.path.join(HERE, 'out', 'sg_%s.json' % name), 'w'))
    cr = found['credits']
    by_sense = {s: [c for c in cr if c['sense'] == s] for s in (1, -1)}
    def centroid(cs):
        if not cs: return None
        return [sum(c['node'][a] for c in cs) * 1000 // len(cs) for a in range(3)]
    def spread_y(cs):
        if not cs: return None
        ys = sorted(c['node'][1] for c in cs); return [ys[0], ys[-1], len(set(ys))]
    first, last = found['rows'][1]['reader'], found['rows'][-1]['reader']
    row = {'run': name, 'ms': ms, 'credits': len(cr), 'credits_s+1': len(by_sense[1]), 'credits_s-1': len(by_sense[-1]),
           'credits_centroid_milli_s+1': centroid(by_sense[1]), 'credits_centroid_milli_s-1': centroid(by_sense[-1]),
           'credits_y_min_max_distinct_s+1': spread_y(by_sense[1]), 'credits_y_min_max_distinct_s-1': spread_y(by_sense[-1]),
           'credits_x_min_max_s+1': ([min(c['node'][0] for c in by_sense[1]), max(c['node'][0] for c in by_sense[1])] if by_sense[1] else None),
           'credits_x_min_max_s-1': ([min(c['node'][0] for c in by_sense[-1]), max(c['node'][0] for c in by_sense[-1])] if by_sense[-1] else None),
           'births': len(found['births']), 'births_senses_sum': sum((w > 0) - (w < 0) for e in found['births'] for w in e['W_children']),
           'reader_end_W>0_centroid': last['W>0'].get('centroid_milli'), 'reader_end_W<0_centroid': last['W<0'].get('centroid_milli'), 'reader_end_W>0_weight': last['W>0']['weight'], 'reader_end_W<0_weight': last['W<0']['weight'],
           'W_total_start_end': [found['rows'][0]['reader']['W_total'], last['W_total']], 'count_units_start_end': [found['rows'][0]['reader']['count_units'], last['count_units']],
           'taken_booked': [found['counts']['taken'], found['counts']['booked']], 'turns': found['counts']['turns'], 'refused_lay': found['counts']['refused_lay'],
           'run_back': found.get('run_back'), 'integers': found['integers'], 'max_bits': found['max_bits'], 'max_transient_bits': found['max_transient_bits']}
    table.append(row); print(json.dumps(row), flush=True)
json.dump(table, open(os.path.join(HERE, 'out', 'sg_table_c%d_i%d.json' % (cube, intervals)), 'w'))
