"""sr2: one world run through the flagged copy, with the spinor row's readings (integers only).

Readings: at every interval the spinor record's lines 0 and 4 (re of the two components' first planes) at the lay's
centre, their upward crossings counted over the run (the beat per component: the Zeeman doublet as two crossing
counts against one); the credits of every record with, for the shape-8 record, the component's sign along the
reading axis (sign of s_D[comp]) and the per-position counts along the gradient's axis, the centroids per component
(thousandths of a Link), the beats' histogram per component, the senses; the board's W total; the counts (births,
taken, booked, clicks, refusals); the census (integers per Node, bits, the transient); the share at the centre at the
start in units of the row (the pile); the run back (hashes compared bit for bit).
Usage: python sr2_run.py <world.json> <out.json> [back N] [axis A] [comp C]   (A the gradient's axis for the per-position counts, default 2; C the component axis read, default 2)
"""
import sys, os, json, hashlib, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from lean_sr2 import Lean, load_world, row_wronskian, pairs
from event_universe.core import paces


def arg(name, default):
    return int(sys.argv[sys.argv.index(name) + 1]) if name in sys.argv else default


def main():
    sys.set_int_max_str_digits(0)
    universe, world = load_world(sys.argv[1]); out_path = sys.argv[2]
    back = arg('back', 0); axis = arg('axis', 2); comp = arg('comp', 2)
    b = Lean(universe, world); n = int(world['intervals'])
    recs = b.records(); spin_recs = [k for k, r in enumerate(recs) if r.shape == 8]; plane_recs = [k for k, r in enumerate(recs) if r.shape == 2 and r.gap > 0]
    lays = [s for s in world['seed'] if s.get('lay') == 'at' and 'width' in s]
    centre = tuple(int(x) for x in lays[0]['centre']) if lays else tuple(x // 2 for x in b.shape)
    # the share at the centre at the start, per record, in units (the pile's reading): the sum over the row's lines at the vacuum's weight
    c0 = b.content(); f0 = b.link_factors(); pace0 = paces.link_pace_of(b.gamma, c0)
    start_share = {}
    for k, r in enumerate(recs):
        rr = b.rule_of(r, c0, f0); tot = 0
        for l in r.lines: tot = tot + b.share(l, rr, pace0, vacuum=True)
        start_share[k] = {'share at centre': int(tot[centre]), 'units at centre (thousandths)': int(tot[centre]) * 1000 // b.units[k], 'board units (thousandths)': int(sum(int(x) for x in tot.reshape(-1))) * 1000 // b.units[k], 'unit': b.units[k]}
    crossings = {}; traces = {}
    watched = [(k, 0) for k in spin_recs] + [(k, 4) for k in spin_recs] + [(k, 0) for k in plane_recs]
    for k, l in watched: crossings[(k, l)] = 0; traces[(k, l)] = []
    crossing_intervals = {k: [] for k in watched}
    def h(): return hashlib.sha256(b.state_bytes() + str(b.interval).encode()).hexdigest()
    hashes = []; t0 = time.monotonic_ns(); maxbits = 0
    for t in range(n):
        if back and t >= n - back: hashes.append(h())
        b.step(); maxbits = max(maxbits, b.census()[1])
        for k, l in watched:
            line = recs[k].lines[l]; now, before = int(line.now[centre]), int(line.before[centre])
            if before < 0 <= now: crossings[(k, l)] += 1; crossing_intervals[(k, l)].append(b.interval)
            if t < 40 or t % 20 == 0: traces[(k, l)].append(now)
    ms = (time.monotonic_ns() - t0) // 1000000
    kept_log = list(b.log)
    # the credits per record
    credits = {}
    for k in range(len(recs)):
        cs = [e for e in kept_log if e['event'] == 'credit' and e['line'] == k]
        entry = {'credits': len(cs), 'senses': {str(s): sum(1 for e in cs if e['sense'] == s) for s in (-1, 0, 1)}, 'beats': {}}
        for e in cs: entry['beats'][str(e['beat'])] = entry['beats'].get(str(e['beat']), 0) + 1
        if cs and recs[k].shape == 8:
            for label, pick in (('component +', lambda e: e['spin']['s_N'][comp] > 0), ('component -', lambda e: e['spin']['s_N'][comp] < 0), ('component 0', lambda e: e['spin']['s_N'][comp] == 0)):
                sel = [e for e in cs if pick(e)]
                per = {}
                for e in sel: per[str(e['node'][axis])] = per.get(str(e['node'][axis]), 0) + 1
                cen = [sum(e['node'][a] for e in sel) * 1000 // len(sel) for a in range(3)] if sel else None
                beats = {}
                for e in sel: beats[str(e['beat'])] = beats.get(str(e['beat']), 0) + 1
                entry[label] = {'credits': len(sel), 'per position along axis %d' % axis: dict(sorted(per.items())), 'centroid (thousandths)': cen, 'beats': beats, 'senses': {str(s): sum(1 for e in sel if e['sense'] == s) for s in (-1, 0, 1)}}
            entry['s_D sums over credits'] = [sum(e['spin']['s_D'][a] for e in cs) for a in range(3)]
            entry['s_W sums over credits'] = [sum(e['spin']['s_W'][a] for e in cs) for a in range(3)]
        if cs and recs[k].shape == 2:
            per = {}
            for e in cs: per[str(e['node'][axis])] = per.get(str(e['node'][axis]), 0) + 1
            entry['per position along axis %d' % axis] = dict(sorted(per.items()))
            entry['centroid (thousandths)'] = [sum(e['node'][a] for e in cs) * 1000 // len(cs) for a in range(3)]
        credits[k] = entry
    births = [e for e in kept_log if e['event'] == 'birth']
    W_rows = {k: int(sum(int(x) for x in row_wronskian(r.lines).reshape(-1))) for k, r in enumerate(recs)}
    W_births = [sum(e['W_children']) for e in births]
    spinor_births = [e for e in births if recs[e['line_pair']].shape == 8]
    integers, bits = b.census()
    # the run back
    run_back = None
    if back:
        exact = 0
        for k in range(back):
            b.step_back(); exact += (h() == hashes[back - 1 - k])
        run_back = {'intervals': back, 'exact': exact}
    result = {'world': os.path.basename(sys.argv[1]), 'cube': b.cube, 'intervals': n, 'milliseconds': ms, 'records (index: shape, gap)': {k: [r.shape, r.gap] for k, r in enumerate(recs)}, 'centre': list(centre),
              'crossings at the centre (record, line): count': {'%d,%d' % k: v for k, v in crossings.items()}, 'crossing intervals (record, line)': {'%d,%d' % k: v for k, v in crossing_intervals.items()}, 'traces (record, line): line 0 values early and every 20th': {'%d,%d' % k: v for k, v in traces.items()},
              'start share per record': start_share, 'credits per record': credits, 'counts': {k: str(v) for k, v in b.counts.items()}, 'taken >= booked': int(b.counts['taken']) >= int(b.counts['booked']),
              'births': len(births), 'spinor births': len(spinor_births), 'W of the children at every birth (sum)': W_births, 'W of the children sum 0 at every birth': all(w == 0 for w in W_births),
              'spinor births: chi and axis': [[e.get('chi'), e.get('axis')] for e in spinor_births][:12], 'W total per record at the end': W_rows, 'integers per Node': integers, 'max bits': maxbits, 'max transient bits': b.max_transient, 'turns': b.counts['turns'], 'run back': run_back}
    json.dump(result, open(out_path, 'w'), indent=1)
    print(json.dumps({'world': result['world'], 'ms': ms, 'credits': {k: v['credits'] for k, v in credits.items()}, 'crossings': result['crossings at the centre (record, line): count'], 'births': len(births), 'spinor births': len(spinor_births), 'run back': run_back, 'integers': integers, 'bits': maxbits, 'transient': b.max_transient, 'taken>=booked': result['taken >= booked']}))


if __name__ == '__main__':
    main()
