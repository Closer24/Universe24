"""pc2, item 3: every pair of successive credits of one line at one Node in the bodies' record (the counted beat b = the interval spacing, the content c1 at the first and c2 at the second) against the law's standing beat at the middle content (c1 + c2) div 2 (the content rises within the period, so the counted beat is the law's beat integrated over the period: the middle content to first order), and against the law's beat at c2 alone (the credit's own content, as a one-click reading would take it). Counts within one interval; the ratio in thousandths. Integers only."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.set_int_max_str_digits(0)
from collections import defaultdict
from event_universe.core import paces as E
from event_universe.core.rule3 import wall_of, mass as mass_of
MIL = 1000
rec = json.load(open(sys.argv[1])); gamma, G, den = int(rec['gamma']), int(rec['G']), int(rec['den'])
planes = [int(x) for x in rec['planes']]
memo = {}


def law_beat(num, c, intervals=20000):
    key = (num, c)
    if key in memo: return memo[key]
    p0 = E.clock(gamma, c); w = wall_of(den, gamma, G); D = mass_of(num, den, p0, G)
    A = 10 ** 6; now, before, r = A, (A * num) // den, w // 2
    crossings = 0; first = last = None
    for t in range(intervals):
        total = (2 * w - D) * now - w * before + r; nxt = total // w; r = total - w * nxt
        if now < 0 <= nxt:
            crossings += 1
            if first is None: first = t
            last = t
        before, now = now, nxt
    memo[key] = (last - first) * MIL // (crossings - 1) if crossings > 1 else None
    return memo[key]


tracks = defaultdict(list)
for e in rec['log']:
    if e['event'] == 'credit': tracks[(tuple(e['node']), e['line'])].append((e['i'], e['content'], e['beat']))
pairs = []
for (node, line), cs in tracks.items():
    cs.sort()
    for (i1, c1, b1), (i2, c2, b2) in zip(cs, cs[1:]):
        if i2 > i1: pairs.append((i2 - i1, c1, c2, planes[line]))
within_mid = within_end = 0; ratios_mid = []; ratios_end = []; rows = []
for b, c1, c2, num in pairs:
    mid = (c1 + c2) // 2
    Bm = law_beat(num, mid); Be = law_beat(num, c2)
    within_mid += abs(b * MIL - Bm) <= MIL; within_end += abs(b * MIL - Be) <= MIL
    ratios_mid.append(b * MIL * MIL // Bm); ratios_end.append(b * MIL * MIL // Be)
    if len(rows) < 16 or b > 20: rows.append([b, c1, c2, Bm, Be])
ratios_mid.sort(); ratios_end.sort()
out = {'pairs': len(pairs), 'counted beat within one interval of the law at the middle content': within_mid, 'within one interval of the law at the end content': within_end,
       'ratio counted / law at middle (thousandths): min, lower quartile, middle, upper quartile, max': [ratios_mid[0], ratios_mid[len(ratios_mid) // 4], ratios_mid[len(ratios_mid) // 2], ratios_mid[3 * len(ratios_mid) // 4], ratios_mid[-1]],
       'ratio counted / law at end content (thousandths): min, middle, max': [ratios_end[0], ratios_end[len(ratios_end) // 2], ratios_end[-1]],
       'rows (counted b, c1, c2, law at middle, law at end), the first 16 and every beat above 20': rows}
for k, v in out.items(): print(json.dumps({k: v}))
