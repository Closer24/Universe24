"""Hand ob1: the two bodies and the force's sign on David's lean toy, read in integers (2026-10-25).

Usage: ob1_run.py <world.json> <intervals> <back> <out.json> [single <row_index> <x,y,z> <width> <quanta> <sense>]...

The toy is imported from the copy under tools/derivations/open_items/H-Everything-The-Clicks-Show-1/toy/ and never edited: the world file lays the toy's own seeds
(sea, hole, at); every `single` argument lays ONE record of one sense (this hand's lay, fed by hand before the first
interval as the toy's one_node_test.py feeds a Node), the same raised-cosine envelope and the same amplitude search as the
toy's `lay_packet`, so that two records of equal or of opposite sense stand at two Nodes (the force's sign, Coulomb).
Per interval the readings, every one an integer or a pair of integers:
- per plane record (row, sense): the peak Node of re^2 + im^2, the weight at the two lay centres and at the Nodes between
  them, the centroid per axis in thousandths of a Link, the record's share at the vacuum's weight over the board as
  (quotient, remainder) of its unit, the Wronskian summed over the board (the charge), the lattice momentum per axis
  P_a = 2 num SUM_i (now_(i+a) before_i - now_i before_(i+a)) over the two lines;
- the light's share over the board in W_c (quotient, remainder) and its lattice momentum;
- the credit lines of the interval, each with the running cosine per axis read from the frame alone
  (2 cos k_a = (re_(+a) + re_(-a)) / re_i as a reduced pair) and the beat;
- the run back: `back` intervals undone at the end, the state's digest compared bit for bit.
"""
import sys, os, json, math, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'toy'))
import numpy as np
from lean_full import Lean, load_world, Line, Z, across, AXES, wronskian

sys.set_int_max_str_digits(0)


def lay_single(b, s_, at, h, n, sense):
    """One record of one sense laid at rest over the toy's raised-cosine envelope (the toy's lay_packet for one sense)."""
    weights = {2: (2, 1), 3: (4, 3, 1)}[h]
    num = b.pairs[s_][0]; sn = b.lifts[s_][2]; w0 = weights[0] ** 3
    envelope = Z(b.shape)
    for j in np.ndindex(*(2 * h - 1,) * 3):
        off = [x - (h - 1) for x in j]
        envelope[tuple((at[a] + off[a]) % b.cube for a in range(3))] += weights[abs(off[0])] * weights[abs(off[1])] * weights[abs(off[2])]
    c = b.content(); factors = b.link_factors(); r = b.rule(b.pairs[s_], c, factors); b.start_content = c

    def record(A):
        re_now = (A * envelope) // w0
        return Line(re_now, (re_now * num) // b.den, None, b.w), Line(Z(b.shape), sense * ((re_now * sn) // b.den), None, b.w)

    def share_of(A):
        re, im = record(A)
        return int(sum(int(x) for x in (b.share(re, r, vacuum=True) + b.share(im, r, vacuum=True)).reshape(-1)))

    target = n * b.units[s_]
    high = 1
    while share_of(high) <= target: high = high + high
    low = 0
    while high - low > 1:
        middle = (low + high) // 2
        if share_of(middle) <= target: low = middle
        else: high = middle
    re, im = record(low)
    pr, pi = b.planes[2 * s_ + (1 if sense > 0 else 0)]
    pr.now = pr.now + re.now; pr.before = pr.before + re.before; pi.before = pi.before + im.before
    b.log.append({'event': 'lay', 'i': 0, 'node': list(at), 'line_pair': s_, 'sense': sense, 'width': h, 'quanta': n, 'amplitude': low, 'share': share_of(low), 'unit': b.units[s_]})
    return low


def ints(a): return [int(x) for x in np.asarray(a, dtype=object).reshape(-1)]


def momentum(num, lines):
    """The lattice momentum per axis of a row's lines: 2 num SUM_i (now_(i+a) before_i - now_i before_(i+a))."""
    found = []
    for a in range(3):
        total = 0
        for l in lines:
            total += int(sum(int(x) for x in (across(l.now, 2 * a) * l.before - l.now * across(l.before, 2 * a)).reshape(-1)))
        found.append(2 * num * total)
    return found


def centroid(weight, shape):
    total = int(sum(int(x) for x in weight.reshape(-1)))
    if total == 0: return None, 0
    idx = np.indices(shape)
    return [int(sum(int(w) * int(x) for w, x in zip(weight.reshape(-1), idx[a].reshape(-1)))) * 1000 // total for a in range(3)], total


def peak(weight):
    flat = ints(weight); k = max(range(len(flat)), key=lambda i: (flat[i], -i))
    return [int(x) for x in np.unravel_index(k, weight.shape)], flat[k]


def reduced(n, d):
    if d == 0: return None
    g = math.gcd(abs(n), abs(d)) or 1
    if d < 0: n, d = -n, -d
    return [n // g, d // g]


def readings(b, centres, mids):
    c = b.content(); factors = b.link_factors(); row = {'i': b.interval, 'records': {}}
    for rec in range(2 * b.nl):
        s_ = rec // 2; sense = 1 if rec % 2 else -1; re, im = b.planes[rec]
        weight = re.now * re.now + im.now * im.now
        if int(sum(int(x) for x in weight.reshape(-1))) == 0: continue
        r = b.rule(b.pairs[s_], c, factors)
        share = int(sum(int(x) for x in (b.share(re, r, vacuum=True) + b.share(im, r, vacuum=True)).reshape(-1)))
        cen, total = centroid(weight, b.shape); pk, pkw = peak(weight)
        row['records']['row %d sense %d' % (s_, sense)] = {
            'peak': pk, 'peak weight bits': pkw.bit_length(),
            'weight at centres': [int(weight[tuple(x)]) for x in centres], 'weight between': [int(weight[tuple(x)]) for x in mids],
            'centroid milli': cen, 'share (quotient, remainder) of unit': [share // b.units[s_], share % b.units[s_]],
            'W total': int(sum(int(x) for x in wronskian(re, im).reshape(-1))), 'P (lattice momentum)': momentum(b.pairs[s_][0], [re, im])}
    r_l = b.rule((b.den, b.den), c, factors)
    light = int(sum(int(x) for x in b.share(b.light, r_l, vacuum=True).reshape(-1)))
    row['light share (quotient, remainder) of W_c'] = [light // b.unit_light, light % b.unit_light]
    row['light P'] = momentum(b.den, [b.light])
    row['content min/max'] = [min(ints(c)), max(ints(c))]
    row['sign level at centres'] = [int(b.sign.now[tuple(x)]) for x in centres]
    row['W board'] = sum(int(x) for re, im in b.planes for x in wronskian(re, im).reshape(-1))
    return row


def credit_reading(e):
    f = e['frame']; found = {'i': e['i'], 'node': e['node'], 'line': e['line'], 'sense': e['sense'], 'beat': e['beat'], 'proper': e['proper'], 'content': e['content'], 'taken': e['taken']}
    for a in range(3):
        found['cos pair x2 axis %d (re)' % a] = reduced(f['re_neighbours_start'][2 * a] + f['re_neighbours_start'][2 * a + 1], f['re_start_now'])
        found['cos pair x2 axis %d (im)' % a] = reduced(f['im_neighbours_start'][2 * a] + f['im_neighbours_start'][2 * a + 1], f['im_start_now'])
    return found


def main():
    world_path, intervals, back, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    universe, world = load_world(world_path)
    b = Lean(universe, world)
    singles = []; args = sys.argv[5:]
    while args:
        assert args[0] == 'single'; s_ = int(args[1]); at = tuple(int(x) for x in args[2].split(',')); h = int(args[3]); n = int(args[4]); sense = int(args[5])
        A = lay_single(b, s_, at, h, n, sense); singles.append({'row': s_, 'at': list(at), 'width': h, 'quanta': n, 'sense': sense, 'amplitude': A}); args = args[6:]
    centres = [tuple(l['centre']) for l in world.get('seed', []) if l.get('lay') == 'at' and tuple(l['row']) != (b.den, b.den)] + [tuple(s['at']) for s in singles]
    mids = []
    if len(centres) >= 2:
        a, c2 = centres[0], centres[1]
        for a_ in range(3):
            if a[a_] != c2[a_]:
                lo, hi = sorted((a[a_], c2[a_]))
                for k in range(lo + 1, hi):
                    m = list(a); m[a_] = k; mids.append(tuple(m))
    def digest(): return hashlib.sha256(b.state_bytes() + str(b.interval).encode()).hexdigest()
    rows = [readings(b, centres, mids)]; credits = []; hashes = []
    for t in range(intervals):
        if back and t >= intervals - back: hashes.append(digest())
        n0 = len(b.log); b.step()
        for e in b.log[n0:]:
            if e['event'] == 'credit': credits.append(credit_reading(e))
        rows.append(readings(b, centres, mids))
        if b.interval % 10 == 0 or b.interval <= 3:
            print(json.dumps({'i': b.interval, 'records': {k: {'peak': v['peak'], 'centroid milli': v['centroid milli'], 'weight at centres': v['weight at centres'], 'weight between': v['weight between'], 'share': v['share (quotient, remainder) of unit'][0], 'W': v['W total'], 'P': v['P (lattice momentum)']} for k, v in rows[-1]['records'].items()}, 'light W_c': rows[-1]['light share (quotient, remainder) of W_c'][0], 'light P': rows[-1]['light P'], 'content': rows[-1]['content min/max'], 'W board': rows[-1]['W board'], 'credits so far': len(credits), 'births': b.counts['births'], 'turns': b.counts['turns']}), flush=True)
    exact = 0
    for k in range(back):
        b.step_back(); exact += (digest() == hashes[back - 1 - k])
    n_int, bits = b.census()
    summary = {'world': world_path, 'intervals': intervals, 'singles': singles, 'centres': [list(x) for x in centres], 'between': [list(x) for x in mids], 'run back': {'intervals': back, 'exact': exact}, 'integers per Node': n_int, 'max state bits': bits, 'max transient bits': b.max_transient, 'counts': {k: str(v) for k, v in b.counts.items()}}
    print(json.dumps(summary), flush=True)
    json.dump({'summary': summary, 'rows': rows, 'credits': credits, 'log': [e for e in b.log if e['event'] != 'credit']}, open(out, 'w'))


if __name__ == '__main__':
    main()
