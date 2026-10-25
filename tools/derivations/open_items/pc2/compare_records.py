"""pc2: two records of the toy compared by name: the counts, the rows (the reader's table), the log line by line (births: interval, node, lift, the two ends; credits: interval, node, line, beat, content, taken), the first interval where the logs part, the contents the credits and births visit and at which of them the carried clock differs from the memo, the light's take in quanta on every click line, the light credits ('detector' lines), the run back, the integers and the bits, the transient's row.
Usage: PYTHONPATH=src python compare_records.py <a.json> <b.json> [gamma]. Integers only."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.set_int_max_str_digits(0)
import pc2_paces as P
from event_universe.core import paces as E

a = json.load(open(sys.argv[1])); b = json.load(open(sys.argv[2])); gamma = int(a['gamma'])
out = {}
out['files'] = [os.path.basename(sys.argv[1]), os.path.basename(sys.argv[2])]
out['counts a'] = a['counts']; out['counts b'] = b['counts']
out['run back a, b'] = [a.get('run_back'), b.get('run_back')]
last = lambda r: r['rows'][-1]
for key in ('integers', 'max bits', 'max transient bits', 'transient where (bits, row shape, interval)', 'content min/mean/max', 'volume mean', 'turns', 'light share quanta max', 'nodes with light at or above one quantum', 'massless im abs max', 'light velocity max'):
    out['last row %s (a, b)' % key] = [last(a).get(key), last(b).get(key)]
def births(r): return [(e['i'], tuple(e['node']), e['line_pair'], tuple(e['minus']), tuple(e['plus'])) for e in r['log'] if e['event'] == 'birth']
def credits(r): return [(e['i'], tuple(e['node']), e['line'], e['beat'], e['content']) for e in r['log'] if e['event'] == 'credit']
ba, bb = births(a), births(b); ca, cb = credits(a), credits(b)
out['births a, b; equal as sets; first birth differing'] = [len(ba), len(bb), sorted(ba) == sorted(bb), next(((x, y) for x, y in zip(sorted(ba), sorted(bb)) if x != y), None)]
out['credits a, b; equal as sets; common; a only; b only'] = [len(ca), len(cb), sorted(ca) == sorted(cb), len(set(ca) & set(cb)), len(set(ca) - set(cb)), len(set(cb) - set(ca))]
out['first interval where the logs part'] = next((i for i in range(1, max(a['intervals'], b['intervals']) + 1) if sorted(x for x in ba + ca if x[0] == i) != sorted(x for x in bb + cb if x[0] == i)), None)
out['whole log equal line for line'] = (a['log'] == b['log'])
# the contents visited by the clicks, and the carried clock against the memo there
visited = sorted({e['content'] for r in (a, b) for e in r['log'] if e['event'] in ('birth', 'credit') and 'content' in e})
E.clear_memo(); P.clear_memo()
differ = [c for c in visited if P.carried_clock(gamma, c) != E.clock(gamma, c)]
differ_link = [c for c in visited if P.carried_link_pace(gamma, c) != E.link_pace(gamma, c)]
out['contents visited by the clicks: count, min, max; contents where the carried clock differs from the memo (clock; link pace)'] = [len(visited), visited[0] if visited else None, visited[-1] if visited else None, differ, differ_link]
# the content range of the board from the rows (the reader's table) and the clock differences inside it
cmin = min(int(r['content min/mean/max'][0]) for r in a['rows'] + b['rows']); cmax = max(int(r['content min/mean/max'][2]) for r in a['rows'] + b['rows'])
d_in = [c for c in range(cmin, cmax + 1) if P.carried_clock(gamma, c) != E.clock(gamma, c)]
out['board content range (rows) and the contents in it where the two clocks differ'] = [cmin, cmax, len(d_in), d_in[:40]]
# the light's take in quanta on every click line (the birth and the credit), from the log alone
def unit_of(r):
    den = int(r['den']); T = int(r['T']); return 3 * T * den  # W_c = 3 T den, the massless plane's quantum (the toy's unit_gap0)
for name, r in (('a', a), ('b', b)):
    W = unit_of(r)
    bt = [e['taken'] for e in r['log'] if e['event'] == 'birth']; ct = [e['taken'] for e in r['log'] if e['event'] == 'credit']
    det = [e for e in r['log'] if e['event'] == 'detector']
    q = lambda xs: [sum(xs) // W, (sum(xs) % W) * 1000 // W] if xs else None
    out['light taken %s: births (count, quanta taken, thousandths), credits (count, quanta taken, thousandths), per birth min/max in thousandths of a quantum, per credit min/max in thousandths, detector lines (light credits), W-S1 light laid' % name] = [len(bt), q(bt), len(ct), q(ct), [min(x * 1000 // W for x in bt), max(x * 1000 // W for x in bt)] if bt else None, [min(x * 1000 // W for x in ct), max(x * 1000 // W for x in ct)] if ct else None, len(det), r['counts'].get('light_laid')]
for k, v in out.items(): print(json.dumps({k: v}))
