"""sp2: runs a set of worlds through the flagged copy (lean_sp2.py) and reads the clicks in integers.

usage: run_set.py <prefix> [back N]   (the worlds worlds/<prefix>*.json; the outputs outputs/<name>.json and
outputs/<prefix>_table.md)

Readings (integers only): per lay its amplitude, share, unit, the quanta read (share div unit) and the sense; the share
at the centre Node per record at the start in units (div) and in thousandths of a unit; per record the credits over the
run: the count, the count per sense, the distinct Nodes, the centroid of the credits' Nodes in thousandths of a Link per
axis (the sum of coordinates times 1000 div the count), the least and greatest z, the beats and their counts, the first
and the last credit's interval; the births, the refusals by cause, the turns; the run back (exact of N); the integers
per Node and the largest integer's bits; the board's total Wronskian at the end; the reader's final centroid per plane.
"""
import json, os, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lean_sp2 as L

OUT = os.path.join(HERE, 'outputs'); os.makedirs(OUT, exist_ok=True)


def centre_shares(b, centre):
    """Each record's share at the centre Node at the start, at the vacuum's weight, in units: the quotient and the remainder in thousandths."""
    c = b.content(); factors = b.link_factors(); found = {}
    for rec, r_ in enumerate(b.records()):
        if r_.gap == 0: continue
        r = b.rule_of(r_, c, factors); re, im = r_.lines
        sh = b.share(re, r, vacuum=True) + b.share(im, r, vacuum=True)
        at = int(sh[tuple(centre)]); total = int(sum(int(x) for x in sh.reshape(-1))); u = b.units[rec]
        found['record %d' % rec] = {'centre share div unit': at // u, 'centre share thousandths of a unit': (at * 1000) // u, 'board share thousandths of a unit': (total * 1000) // u,
                                   'nodes at or above one unit': int(sum(1 for x in sh.reshape(-1) if int(x) >= u))}
    return found


def run(name, back):
    path = os.path.join(HERE, 'worlds', name + '.json')
    universe, world = L.load_world(path)
    b = L.Lean(universe, world); intervals = int(world['intervals'])
    centre = next(e['centre'] for e in world['seed'] if e['lay'] == 'at')  # the first packet's centre (the sea lay comes first)
    start = {'centre shares': centre_shares(b, centre), 'lays': [dict(e) for e in b.log if e['event'] == 'lay']}
    t0 = time.monotonic_ns(); hashes = []; maxbits = 0
    for t in range(intervals):
        if back and t >= intervals - back: hashes.append(b.state_hash())
        b.step(); maxbits = max(maxbits, b.census()[1])
    ms = (time.monotonic_ns() - t0) // 1000000
    final_reading = L.reading(b, maxbits)
    log = list(b.log)
    exact = 0
    for k in range(back):
        b.step_back(); exact += (b.state_hash() == hashes[back - 1 - k])
    # the beam's credits: the births lay children (one quantum, both senses) of any record elsewhere on the board, which click too; a credit is the beam's when its record was laid by the world and its Node is no child's Node and lies within 2 Links of the lay's centre on the two axes across the gradient (x, y)
    children = {(e['line_pair'], tuple(e['minus'])) for e in log if e['event'] == 'birth'} | {(e['line_pair'], tuple(e['plus'])) for e in log if e['event'] == 'birth'}
    cube = b.cube
    def near(node, a): d = (node[a] - centre[a]) % cube; return min(d, cube - d) <= 2
    laid_records = {e['line_pair'] for e in log if e['event'] == 'lay'}
    all_credits = [e for e in log if e['event'] == 'credit']
    credits = [e for e in all_credits if e['line'] in laid_records and (e['line'], tuple(e['node'])) not in children and near(e['node'], 0) and near(e['node'], 1)]
    per_record = {}
    for rec in sorted({e['line'] for e in credits}):
        cs = [e for e in credits if e['line'] == rec]; n = len(cs)
        nodes = [tuple(e['node']) for e in cs]
        beats = {}
        for e in cs: beats[e['beat']] = beats.get(e['beat'], 0) + 1
        per_record['record %d' % rec] = {
            'credits': n, 'by sense': {s: sum(1 for e in cs if e['sense'] == s) for s in (-1, 0, 1)},
            'distinct nodes': len(set(nodes)),
            'centroid thousandths': [sum(nd[a] for nd in nodes) * 1000 // n for a in range(3)],
            'z min max': [min(nd[2] for nd in nodes), max(nd[2] for nd in nodes)], 'y min max': [min(nd[1] for nd in nodes), max(nd[1] for nd in nodes)], 'x min max': [min(nd[0] for nd in nodes), max(nd[0] for nd in nodes)],
            'beats': {str(k): v for k, v in sorted(beats.items())}, 'first last interval': [cs[0]['i'], cs[-1]['i']],
            'credits per sense per z': {str(s): {str(z): sum(1 for e in cs if e['sense'] == s and e['node'][2] == z) for z in sorted({e['node'][2] for e in cs})} for s in (-1, 1)},
            'turned credits': sum(1 for e in cs if e.get('turned'))}
    refused = {}
    for e in log:
        if e['event'] == 'refused': refused[e['cause']] = refused.get(e['cause'], 0) + 1
    found = {'world': name, 'file': world, 'start': start, 'per record': per_record, 'all credits': len(all_credits), 'beam credits': len(credits), 'children credits': sum(1 for e in all_credits if (e['line'], tuple(e['node'])) in children), 'births': b.counts['births'], 'body_clicks': b.counts['body_clicks'], 'refused': refused, 'turns': b.counts['turns'],
             'taken': str(b.counts['taken']), 'booked': str(b.counts['booked']), 'run back': {'intervals': back, 'exact': exact}, 'integers per node': b.census()[0], 'max bits': maxbits, 'max transient bits': b.max_transient,
             'final reading': {k: final_reading[k] for k in ('packets (reader)', 'W total', 'W abs sum', 'sign level max', 'odd max bits', 'content min/mean/max', 'links at the wall')}, 'milliseconds': ms,
             'credits': [{'i': e['i'], 'node': e['node'], 'line': e['line'], 'sense': e['sense'], 'beat': e['beat']} for e in credits]}
    json.dump(found, open(os.path.join(OUT, name + '.json'), 'w'))
    return found


def table(rows, prefix):
    lines = ['| world | lays (quanta read at the lay) | centre share (units, thousandths) | record | credits | by sense -1 / +1 | distinct Nodes | centroid (thousandths) | z min..max | beats | births | refused | turns | run back | bits |', '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for f in rows:
        lays = '; '.join('row %d x%d sense %s A %d read %d' % (e['line_pair'], e['quanta'], e.get('sense'), e['amplitude'], e['share'] // e['unit']) for e in f['start']['lays'])
        cs = '; '.join('%s: %d (%d)' % (k[7:], v['centre share div unit'], v['centre share thousandths of a unit']) for k, v in f['start']['centre shares'].items() if v['board share thousandths of a unit'] > 0)
        if not f['per record']:
            lines.append('| %s | %s | %s | - | 0 | - | - | - | - | - | %d | %s | %d | %d of %d | %d |' % (f['world'], lays, cs, f['births'], json.dumps(f['refused']), f['turns'], f['run back']['exact'], f['run back']['intervals'], f['max bits']))
        for rec, p in f['per record'].items():
            lines.append('| %s | %s | %s | %s | %d | %d / %d | %d | %s | %d..%d | %s | %d | %s | %d | %d of %d | %d |' % (
                f['world'], lays, cs, rec, p['credits'], p['by sense']['-1'] if '-1' in p['by sense'] else p['by sense'][-1], p['by sense']['1'] if '1' in p['by sense'] else p['by sense'][1], p['distinct nodes'], p['centroid thousandths'], p['z min max'][0], p['z min max'][1], json.dumps(p['beats']), f['births'], json.dumps(f['refused']), f['turns'], f['run back']['exact'], f['run back']['intervals'], f['max bits']))
    open(os.path.join(OUT, prefix + '_table.md'), 'w').write('\n'.join(lines) + '\n')
    print('\n'.join(lines))


if __name__ == '__main__':
    sys.set_int_max_str_digits(0)
    prefix = sys.argv[1]; back = int(sys.argv[sys.argv.index('back') + 1]) if 'back' in sys.argv else 10
    names = sorted(n[:-5] for n in os.listdir(os.path.join(HERE, 'worlds')) if n.startswith(prefix) and n.endswith('.json'))
    rows = []
    for name in names:
        f = run(name, back); rows.append(f)
        print(json.dumps({'world': name, 'ms': f['milliseconds'], 'credits': {k: v['credits'] for k, v in f['per record'].items()}, 'births': f['births'], 'run back': f['run back']}), flush=True)
    table(rows, prefix)
