"""Residuals of the species solve against the line's own num: is the per-credit error within the remainder bound |r - r'| < w (the rounding of the Node's own line), or beyond it (a fold the decoder does not reproduce)?"""
import sys, os, json, importlib.util
from collections import Counter
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', 'src'))
spec = importlib.util.spec_from_file_location('dec', sys.argv[1]); 
# reuse decoder pieces by exec of its head
src = open(sys.argv[1]).read().split('# gate 8 and 19')[0]
sys.argv = [sys.argv[0], sys.argv[2]]
g = {}; exec(src, g)
solve, credits, NAMES, line_num, den, gamma, G = g['solve'], g['credits'], g['NAMES'], g['line_num'], g['den'], g['gamma'], g['G']
from event_universe.core import paces, rule3
w = rule3.wall_of(den, gamma, G)
bins = Counter(); worst = []
for c in credits:
    x = solve(c)
    if x is None: continue
    N, D = x; num = line_num[c['line'] // 2]
    # residual in units of the remainder bound: |N den - num D| / (w den) ... the bound: |numer error| < w  => |x error| < w / |denom|; D = |denom|^2 so x error bound = w |denom| / D ... use |N den - num D| vs w den sqrt(D) -> compare squares
    res2 = (N * den - num * D) ** 2; bound2 = 2 * (w * den) ** 2 * D  # the two lines' remainders (re, im), each |r - r'| < w: |error| < w sqrt 2
    ratio_mil = (res2 * 1000) // bound2 if bound2 else None  # (res/bound)^2 in thousandths
    f = c['frame']; zn2 = f['re_start_now'] ** 2 + f['im_start_now'] ** 2
    turned = any(p != [f['X'], 0] for p in f['phases']) or any(o != 0 for o in f['odd'])
    key = ('turned' if turned else 'flat', 'within' if res2 <= bound2 else 'beyond')
    bins[key] += 1
    if res2 > bound2: worst.append((ratio_mil, c['i'], c['node'], c['line'], zn2.bit_length(), turned))
print(dict(bins))
worst.sort(reverse=True)
print('beyond, worst (res/bound)^2 thousandths, i, node, line, bits of |zn|^2, turned:', worst[:8])
print('amplitude |zn| bits histogram', Counter((c['frame']['re_start_now'] ** 2 + c['frame']['im_start_now'] ** 2).bit_length() // 2 for c in credits))
# the turn: are the credits beyond the bound the turned Nodes'?
cross = Counter()
for c in credits:
    x = solve(c)
    if x is None: continue
    N, D = x; num = line_num[c['line'] // 2]
    res2 = (N * den - num * D) ** 2; bound2 = 2 * (w * den) ** 2 * D  # the two lines' remainders (re, im), each |r - r'| < w: |error| < w sqrt 2
    cross[('turned' if c['turned'] else 'not turned', 'beyond' if res2 > bound2 else 'within')] += 1
print('turn x bound:', dict(cross))
