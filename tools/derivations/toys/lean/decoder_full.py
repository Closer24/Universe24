"""The decoder of the full lean toy, integers only (the owner's word of 05:08: no float anywhere, every reading a quotient with its remainder or a count over a span).
Reads the run's log alone (credits, births, refusals; the rows of the board's course), holds den's circle and the names, and gives every gate of UNIVERSE24 a verdict with its numbers.
Two views (the owner's word of 05:05): the whole view (every click on the board) and the one-place view (a body found from its clicks alone at one Node, its clock read against another body's)."""
import sys, os, json
from collections import Counter, defaultdict
from functools import cmp_to_key
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', 'src'))
from event_universe.core import paces, rule3
from event_universe.core.paces import sine_den
run = json.load(open(sys.argv[1])); den = int(run['den'])
gamma, G, T = run['gamma'], run['G'], run['T']
lifts = sorted([(sine_den(int(num), den), int(num)) for _v, num, _s in run['lifts']])  # the lifts by their legs (T sin omega): the decoder's names, never the Node's
NL = len(lifts)
names = ['electron', 'proton', 'neutron'] if NL == 3 else ['lift %d' % k for k in range(NL)]
NAMES = {num: (name, leg) for (leg, num), name in zip(lifts, names)}
line_num = [int(run['lifts'][i][1]) for i in range(NL)]
log = run['log']; credits = [l for l in log if l['event'] == 'credit']; births = [l for l in log if l['event'] == 'birth']; refused = [l for l in log if l['event'] == 'refused']
rows = run['rows']; turns = run.get('turns', [])
out = {}
MIL = 1000000  # readings in parts per million


def quot(a, b, scale=1):
    """The integer reading of a / b: the quotient of the scaled numerator (the remainder dropped)."""
    return None if b == 0 else (a * scale) // b


def cmp_rat(p, q):
    """Order two rationals (n, d) with d > 0 by cross multiplication."""
    s = p[0] * q[1] - q[0] * p[1]
    return (s > 0) - (s < 0)


def solve(c):
    """The species from the frame in exact integers: the same turned arrivals the Node formed (the phase pair over X and the odd tangent, half-up divisions), Rule3's line solved for x = num / den; returned as the rational (N, D) with D > 0, x = N / D."""
    f = c['frame']; cont = c['content']
    p0 = paces.clock(gamma, cont); pi = paces.link_pace(gamma, cont)
    w = rule3.wall_of(den, gamma, G); D1 = 12 * den * p0 * p0 * G * G
    zb = (f['re_start_before'], f['im_start_before']); zn = (f['re_start_now'], f['im_start_now']); zx = (f['re_now'], f['im_now'])
    # the turn (the swap at the top): the turned Node ends the interval at its pre-state exchanged, the step's output discarded; the record names the stepped level, the solve reads it
    if 're_stepped' in f: zx = (f['re_stepped'], f['im_stepped'])
    elif c.get('turned') and 're_before' in f: zx = (f['re_before'], f['im_before'])  # the former toy's swap (the post-state exchanged)
    if zn == (0, 0): return None
    X = f.get('X'); phs = f.get('phases'); odd = f.get('odd'); Wl = 4 * gamma
    def add(a, b): return (a[0] + b[0], a[1] + b[1])
    def sub(a, b): return (a[0] - b[0], a[1] - b[1])
    def sc(k, a): return (k * a[0], k * a[1])
    numer = add(sc(w, sub(add(zx, zb), sc(2, zn))), sc(D1, zn))
    denom = sc(D1, zn)
    fr = f.get('frames')
    for port, (a, b) in enumerate(zip(f['re_neighbours_start'], f['im_neighbours_start'])):
        m = (a, (fr[port] if fr else 1) * b)  # the neighbour read in the Node's frame (conjugated where the frames differ)
        if phs:
            c_, s_ = phs[port]
            m = ((2 * (c_ * m[0] - s_ * m[1]) + X) // (2 * X), (2 * (s_ * m[0] + c_ * m[1]) + X) // (2 * X))
            n = odd[port]; tc, ts, tw = Wl * Wl - n * n, 2 * Wl * n, Wl * Wl + n * n
            m = ((2 * (tc * m[0] - ts * m[1]) + tw) // (2 * tw), (2 * (ts * m[0] + tc * m[1]) + tw) // (2 * tw))
        Q = f['factors'][port] if f.get('factors') else G * G
        R1 = 2 * den * pi * pi * Q
        denom = sub(denom, sc(R1, sub(zn, m)))
    dd = denom[0] * denom[0] + denom[1] * denom[1]
    if dd == 0: return None
    # x = Re(numer / denom) = (nr dr + ni di) / |d|^2, an exact rational
    return (numer[0] * denom[0] + numer[1] * denom[1], dd)


def nearest(x):
    """The name whose num / den lies nearest the rational x = (N, D): the smallest |N den - num D|, all integers."""
    N, D = x
    return min(NAMES.items(), key=lambda kv: abs(N * den - kv[0] * D))[1][0]


# gate 8 and 19: the species from the frame (the whole view); the mass ratios from den's legs
# the one-click floor: the Node's own line is known up to its two remainders (re, im), each |r - r'| < w, so the solve's
# numerator is known within w sqrt 2 and x within w sqrt 2 / |denom|; a credit's residual beyond that is a fold the decoder
# does not reproduce, within it is the law's own uncertainty of one click (the track resolves it)
w_ = rule3.wall_of(den, gamma, G)
decoded = []; right = 0; within = 0; floor_mil = []
for c in credits:
    x = solve(c)
    if x is None: continue
    name = nearest(x)
    truth = NAMES[line_num[c['line'] // 2]][0]; right += (name == truth); decoded.append((c, name, x))
    N, D = x; num = line_num[c['line'] // 2]
    res2 = (N * den - num * D) ** 2; bound2 = 2 * (w_ * den) ** 2 * D
    within += (res2 <= bound2)
    # the floor of this click in parts per million of x: (w sqrt 2 / |denom|) / (num / den) -> squared, exact integers, then the root
    floor_mil.append(rule3.largest_below((2 * w_ * w_ * den * den * MIL * MIL) // (D * num * num)) if num else None)
# the species over a body's track (the one-place view): the credits of one line at one Node, the middle solve in order
tr = defaultdict(list); conf = Counter()
for c, name, x in decoded:
    tr[(tuple(c['node']), c['line'])].append(x); conf[(NAMES[line_num[c['line'] // 2]][0], name)] += 1
track_right = 0; track_n = 0
for (node, line), xs in tr.items():
    xs.sort(key=cmp_to_key(cmp_rat)); k = len(xs)
    # the median as an exact rational: the middle solve, or the two middles' mean (ad + cb) / (2 b d)
    xm = xs[k // 2] if k % 2 else (xs[k // 2 - 1][0] * xs[k // 2][1] + xs[k // 2][0] * xs[k // 2 - 1][1], 2 * xs[k // 2 - 1][1] * xs[k // 2][1])
    track_n += 1; track_right += (nearest(xm) == NAMES[line_num[line // 2]][0])
out['8b species over the track (one-place view: the middle solve of the body\'s track)'] = {'tracks': track_n, 'decoded right': track_right, 'confusion (truth->decoded) per credit': {f'{a}->{b}': n for (a, b), n in conf.items() if a != b}}
out['8 families forming (whole view)'] = {'credits': len(credits), 'species readable': len(decoded), 'decoded right per credit': right, 'credits within the one-click floor': within, 'tracks right': [track_right, track_n], 'births by species (decoder)': dict(Counter(NAMES[line_num[b['line_pair']]][0] for b in births)), 'verdict': 'SHOWN (every credit within the one-click floor, every track read right)' if within == len(decoded) and track_right == track_n and len(set(NAMES[line_num[b['line_pair']]][0] for b in births)) >= 3 else ('SHOWN in part: every credit within the floor, tracks right %d of %d' % (track_right, track_n) if within == len(decoded) else 'NOT SHOWN: %d credits beyond the floor' % (len(decoded) - within))}
legs = {v[0]: v[1] for v in NAMES.values()}; num_of = {v[0]: k for k, v in NAMES.items()}
ordered = sorted(legs.items(), key=lambda kv: kv[1])
out['19 mass ratios (parts per million)'] = {'%s/%s' % (nm, ordered[0][0]): quot(leg, ordered[0][1], MIL) for nm, leg in ordered[1:]} | {'verdict': 'SHOWN as a fit of den (the legs), read from the decoded points'}
# gate 17 charge
sense_sum = sum(s for b in births for s in b['senses'])
out['17 charge conservation'] = {'senses sum over births': sense_sum, 'verdict': 'SHOWN' if sense_sum == 0 else 'NOT SHOWN'}
# gate 15 conservation at the click
booked = sum(b['booked'] for b in births); taken_b = sum(b['taken'] for b in births)
out['15 conservation at the click'] = {'births': len(births), 'taken per booked at the births (hundredths)': quot(taken_b, booked, 100), 'verdict': 'SHOWN as the identity taken >= booked on every birth; NOT SHOWN exact (the excess below one level of light, the known item)' if all(b['taken'] >= b['booked'] for b in births) else 'NOT SHOWN'}
# gate 10 dilation (one-place view): a body's proper count against the intervals it stood, deep against shallow
if len(decoded) > 10:
    pairs = [(c['content'], c['proper'], c['i']) for c, _n, _x in decoded]  # the reader's view alone
    med = sorted(p[0] for p in pairs)[len(pairs) // 2]
    lo = [p for p in pairs if p[0] <= med]; hi = [p for p in pairs if p[0] > med]
    rate_lo = (sum(p[1] for p in lo), sum(p[2] for p in lo)); rate_hi = (sum(p[1] for p in hi), sum(p[2] for p in hi))
    out['10 gravitational time dilation'] = {'reader\'s view (the board\'s interval, which no Node has): proper per thousand intervals, shallow / deep': [quot(*rate_lo, 1000), quot(*rate_hi, 1000)], 'verdict': ('SHOWN in the reader\'s view' if cmp_rat(rate_hi, rate_lo) < 0 else 'NOT SHOWN in the reader\'s view') + '; NOT READ in the one-place view: two bodies\' clocks compare only through the light between them (gate 7)'}
# gate 2 the Links lengthening in the clicks (one-place view): the spacing of a body's credits longer where the content is deeper
by_node = defaultdict(list)
for c in credits: by_node[tuple(c['node'])].append(c)
spans = []
for node, cs in by_node.items():
    cs.sort(key=lambda c: c['i'])  # the reader's view alone
    for a, b in zip(cs, cs[1:]):
        if b['i'] > a['i']: spans.append(((a['content'] + b['content']) // 2, b['i'] - a['i']))
if len(spans) > 20:
    med = sorted(s[0] for s in spans)[len(spans) // 2]
    lo = [s[1] for s in spans if s[0] <= med]; hi = [s[1] for s in spans if s[0] > med]
    out['2 the Links lengthening in the clicks'] = {'reader\'s view: spans': len(spans), 'spacing in hundredths of a board interval, shallow / deep': [quot(sum(lo), len(lo), 100), quot(sum(hi), len(hi), 100)], 'verdict': ('SHOWN in the reader\'s view' if quot(sum(hi), len(hi), 100) > quot(sum(lo), len(lo), 100) else 'NOT SHOWN in the reader\'s view') + '; NOT READ in the one-place view (the light between two bodies, gate 7)'}
# gates 1, 3, 5, 6: the board's course from the rows (whole view): the mean volume's rises and falls, the turns
course = [(r['i'], int(r['volume mean']), r['births']) for r in rows]
vel = [(b[0], b[1] - a[1]) for a, b in zip(course, course[1:])]
falls = [i for i, v in vel if v < 0]
out['1 recurring bangs / 3 shortening then lengthening / 6 contraction (board, the reader\'s view)'] = {'volume mean course (interval, mean)': [(i, v) for i, v, _b in course[:: max(1, len(course) // 8)]], 'intervals with the mean volume falling': falls[:6], 'turns (Node swaps) total': int(run['counts']['turns']), 'verdict': 'contraction SHOWN at the board' if falls else 'NOT SHOWN: the mean volume rises throughout (the pump); the turns are local'}
# gate 4 era of matter
half = run['intervals'] // 2
# the era of matter in the Nodes' own clocks: at every Node with a birth and a body's credit, the credits go on past the last birth in that Node's proper count
last_birth = {}; last_credit = {}
for b in births: last_birth[tuple(b['node'])] = max(last_birth.get(tuple(b['node']), 0), b['proper'])
for c in credits: last_credit[tuple(c['node'])] = max(last_credit.get(tuple(c['node']), 0), c['proper'])
both = [n for n in last_birth if n in last_credit]
past = sum(1 for n in both if last_credit[n] > last_birth[n])
out['4 an era of matter'] = {'Nodes with a birth and a body credit': len(both), 'of them with credits past the last birth in the Node\'s own clock': past, 'births': len(births), 'body credits': len(credits), 'verdict': 'SHOWN' if both and past == len(both) else ('SHOWN in part: %d of %d' % (past, len(both)) if past else 'NOT SHOWN')}
# gate 14 horizon
frozen = paces.frozen_content(gamma)
fr = [c for c in credits if c['content'] >= frozen]
cmax = max(int(r['content min/mean/max'][2]) for r in rows)
out['14 the horizon'] = {'frozen content': frozen, 'max content in the rows': cmax, 'credits at frozen Nodes': len(fr), 'verdict': 'SHOWN as silence (no credit at a frozen Node)' if cmax >= frozen and not fr else ('NOT REACHED' if cmax < frozen else 'NOT SHOWN')}
# gate 16 the uncertainty floor: one click reads the species within w sqrt 2 / |denom| (the two remainders of the Node's own line); the floor falls as 1 / |z| (the amplitude) and the track of many clicks resolves it
fl = sorted(f for f in floor_mil if f is not None)
if fl:
    out['16 uncertainty floor (one click)'] = {'floor on x per credit, parts per million: min / middle / max': [fl[0], fl[len(fl) // 2], fl[-1]], 'species spacing of the two heaviest, parts per million': quot(abs(num_of[ordered[-1][0]] - num_of[ordered[-2][0]]), num_of[ordered[-1][0]], MIL) if NL >= 2 else None, 'credits beyond the floor': len(decoded) - within, 'verdict': 'SHOWN as the law\'s floor: no credit reads beyond it; one click cannot split p from n where the floor exceeds their spacing, the track can (not calibrated to h-bar / 2)' if within == len(decoded) else 'NOT SHOWN'}
# gate 9 and 13: tracks
tracks = defaultdict(list)
for c, n, _x in decoded: tracks[(tuple(c['node']), n)].append(c['proper'])
longest = max((len(v) for v in tracks.values()), default=0)
# a body's track: its record's credits by line; a move is a credit of the same line at a neighbouring Node after the last (read from the record)
by_line = defaultdict(list)
for c in credits: by_line[c['line']].append((c['proper'], tuple(c['node'])))
moves = 0
for line, cs in by_line.items():
    cs.sort(); nodes_seen = {cs[0][1]}
    for (_i, at) in cs[1:]:
        if at not in nodes_seen: moves += 1; nodes_seen.add(at)
out['9 collisions / 13 free fall'] = {'tracks (node, species)': len(tracks), 'longest track credits': longest, 'lines credited at a new Node after their first': moves, 'verdict': 'NOT SHOWN: no line is credited at a second Node (the bodies stand)' if moves == 0 else 'read: %d lines credited at a new Node; the predicate (the tail falls, adjacent peaks collide) is the sentence W-S4/W-S5 of the owner, not read here' % moves}
beats_by_line = defaultdict(list)
for c in credits: beats_by_line[(tuple(c['node']), c['line'])].append((c['proper'], c['beat'], c['proper']))
light_credits = [l for l in log if l['event'] == 'light']
if light_credits:
    # the detector's clock: the spacing of its light credits in its own proper count (the middle spacing); the bodies' clocks: the spacing of a record's clicks in its proper count at its Node; the ratio against the two Nodes' contents (the volume's level)
    by_det = defaultdict(list)
    for l in light_credits: by_det[tuple(l['node'])].append(l['proper'])
    det_rows = {}
    for det, ps in by_det.items():
        ps.sort(); gaps = sorted(b - a for a, b in zip(ps, ps[1:]) if b > a)
        det_rows[str(det)] = {'light credits': len(ps), 'middle spacing in the detector\'s proper count': gaps[len(gaps) // 2] if gaps else None, 'content at the credits (min/max)': [min(l['content'] for l in light_credits if tuple(l['node']) == det), max(l['content'] for l in light_credits if tuple(l['node']) == det)]}
    body_gaps = []
    for key, cs in beats_by_line.items():
        cs.sort()
        body_gaps += [(p2 - p1, c2) for (i1, b1, p1), (i2, b2, p2) in zip(cs, cs[1:]) if p2 > p1 for c2 in [key]]
    bg = sorted(g for g, _k in body_gaps)
    out['7 light with its redshift / 11 / 12'] = {'detectors': det_rows, 'bodies: middle click spacing in proper count': bg[len(bg) // 2] if bg else None, 'bodies: click pairs': len(bg), 'verdict': 'read: the light credited at the detector (W-S1 on); the redshift ratio is the detector spacing against the body spacing at their two contents, read above, the predicate to the owner'}
else:
    out['7 light with its redshift / 11 / 12'] = {'light credits in the record': 0, 'verdict': 'NOT SHOWN: the record holds no light credit'}
rb = run.get('run_back')
out['18 the arrow of time'] = {'run back on the record': rb, 'verdict': ('SHOWN: the run back exact bit for bit, %d of %d intervals' % (rb['exact'], rb['intervals']) if rb['exact'] == rb['intervals'] else 'NOT SHOWN: %d of %d' % (rb['exact'], rb['intervals'])) if rb else 'NOT READ: the record carries no run back (run lean_full.py with back N)'}
# the conservations in the clicks (the owner's word of 06:2x: what the lattice conserves is shown conserved in the clicks)
cons = {}
cons['charge: the senses summed over the births'] = sense_sum
cons['count: taken against booked over the births (hundredths)'] = quot(taken_b, booked, 100)
changes = []; same = 0; total_pairs = 0
for key, cs in beats_by_line.items():
    cs.sort()
    for (i1, b1, p1), (i2, b2, p2) in zip(cs, cs[1:]):
        if b1 > 0 and b2 > 0: total_pairs += 1; same += (b1 == b2); changes.append(abs(b2 - b1))
cons['energy: the beat (intervals per period) of a body unchanged from one click to the next'] = {'click pairs': total_pairs, 'unchanged': same, 'changed by one': sum(1 for d in changes if d == 1), 'changed by more': sum(1 for d in changes if d > 1)}
cons['momentum: the credits running cosine'] = 'NOT READ in this toy'
out['the conservations in the clicks'] = cons
counts_seen = sorted({r['integers'] for r in rows}); state_bits = max(r['max bits'] for r in rows); transient_bits = max(r['max transient bits'] for r in rows)
out['the three constants'] = {'integers per Node': counts_seen, 'max state bits': state_bits, 'max transient bits': transient_bits, 'first interval past the width': next((r['i'] for r in rows if r['max transient bits'] > 128 or r['max bits'] > 128), None),
                              'verdict': ('SHOWN: the count constant, every integer and transient within 128' if len(counts_seen) == 1 and state_bits <= 128 and transient_bits <= 128 else 'NOT SHOWN: ' + ('the count changes; ' if len(counts_seen) != 1 else '') + ('the state past 128 bits; ' if state_bits > 128 else '') + ('a transient past 128 bits' if transient_bits > 128 else ''))}
out['the decoder'] = {'floats used': 0, 'readings': 'quotients at a named scale, counts, bit lengths; rationals compared by cross multiplication'}
for k, v in out.items(): print(json.dumps({k: v}))
