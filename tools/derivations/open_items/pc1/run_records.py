"""pc1: the records on the flagged toy copy, each form a subprocess with the flag in its environment (no shell loop): the hole seed 60, the chiral seed 300, the bodies' seed 120, with the run back; the records' counts compared between the forms (David's memo against the carried clock) and the logs' differences by name.
Usage: python run_records.py <out_dir> <form,form,...> <world:intervals:back,...>
"""
import sys, os, json, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
TOY = os.path.join(HERE, 'toy_pc1')


def world_at(world, intervals, out_dir):
    """The world file with its intervals set (the Boss ran the chiral seed at 300 though its file says 60): a copy beside the toy's files so the universe path resolves."""
    w = json.load(open(os.path.join(TOY, world)))
    w['intervals'] = intervals
    path = os.path.join(TOY, 'pc1_%s_%d.json' % (world[:-5], intervals))
    json.dump(w, open(path, 'w'))
    return path


def run_one(form, world, intervals, back, out_dir):
    path = world_at(world, intervals, out_dir)
    out = os.path.join(out_dir, '%s_%d_%s.json' % (world[:-5], intervals, form))
    env = dict(os.environ, PC1_CLOCK=form)
    t0 = time.time()
    log = subprocess.run([sys.executable, os.path.join(TOY, 'lean_full.py'), path, out, 'back', str(back)], env=env, capture_output=True, text=True)
    seconds = int(time.time() - t0)
    open(out + '.log', 'w').write(log.stdout + log.stderr)
    if log.returncode != 0:
        return {'error': log.stderr[-2000:]}
    rec = json.load(open(out))
    last = rec['rows'][-1]
    return {'seconds': seconds, 'counts': rec['counts'], 'run_back': rec['run_back'], 'turns': len(rec['turns']), 'max bits': last['max bits'], 'max transient bits': last['max transient bits'], 'integers': last['integers'],
            'transient class': rec.get('transient_class (pc1)'), 'paces memo bits': rec.get('paces_memo_bits (pc1)'), 'contents visited': len(rec.get('contents_visited (pc1)', [])),
            'content visited min/max': [min(rec['contents_visited (pc1)']), max(rec['contents_visited (pc1)'])], 'content max at end': last['content min/mean/max'][2],
            'log events': {k: sum(1 for e in rec['log'] if e['event'] == k) for k in ('lay', 'birth', 'credit', 'refused', 'detector')}, 'out': out}


def differences(a, b):
    """The two records' logs compared line by line by kind: the first interval at which the logs differ, the counts of births and credits per interval that differ."""
    la, lb = json.load(open(a))['log'], json.load(open(b))['log']
    ka = [(e['i'], e['event'], tuple(e['node'])) for e in la if e['event'] != 'lay']
    kb = [(e['i'], e['event'], tuple(e['node'])) for e in lb if e['event'] != 'lay']
    first = next((k for k, (x, y) in enumerate(zip(ka, kb)) if x != y), None)
    return {'lines a': len(ka), 'lines b': len(kb), 'first differing line': first, 'at interval': ka[first][0] if first is not None and first < len(ka) else None, 'identical': ka == kb}


if __name__ == '__main__':
    out_dir = sys.argv[1]; os.makedirs(out_dir, exist_ok=True)
    forms = sys.argv[2].split(',')
    runs = [tuple(x.split(':')) for x in sys.argv[3].split(',')]
    found = {}
    for world, intervals, back in runs:
        intervals, back = int(intervals), int(back)
        key = '%s at %d' % (world, intervals)
        found[key] = {}
        for form in forms:
            found[key][form] = run_one(form, world, intervals, back, out_dir)
            print(json.dumps({key: {form: {k: v for k, v in found[key][form].items() if k != 'out'}}}), flush=True)
        if len(forms) > 1 and all('out' in found[key][f] for f in forms):
            found[key]['differences %s vs %s' % (forms[0], forms[1])] = differences(found[key][forms[0]]['out'], found[key][forms[1]]['out'])
            print(json.dumps({key: found[key]['differences %s vs %s' % (forms[0], forms[1])]}), flush=True)
    json.dump(found, open(os.path.join(out_dir, 'records_summary.json'), 'w'), indent=1)
