"""sp1 (2026-10-25): Stern-Gerlach in the clicks on David's lean toy (the copy under toy/, run and never edited).

A plane packet of ONE lift and ONE sense (the toy's own `at` lay lays the conjugate pair, the im lines cancelling; here the
same envelope and the same amplitude search, one sense alone) is laid at rest at the centre of a sea of light, and the
shape-4 row's odd lines (the potential's A_a) are hand-set across the beam: `none` (the control), `uniform` (A_x = n0 at
every Node, a static solution of the massless line), `gradient` (A_x = n0 (y - c), the linear profile, its seam at the
torus edge). With `--held` the profile is re-imposed at every interval's start (an external magnet held by the apparatus,
outside the law's acts; the overwritten levels are kept by this script and restored on the run back, so MATCH is measured
on the held runs too). Every reading is an integer: the reader's centroids in thousandths of a Link (the weights
re^2 + im^2 of the Nodes, split by the sign of the Node's Wronskian), the record's W total, the count in units, the credits
(Node, sense, beat, interval) and the births; the run back exact over `--back` intervals; the census (integers, bits).

Usage: python sp1_sg.py --cube 9 --intervals 60 --sense 1 --odd gradient --strength 200 [--held] --back 10 --out out/x.json
       python sp1_sg.py ... --images48 : the 48 signed permutations of the axes applied to the seed AND to the odd
       profile as a vector (A'_a'(g x) = s_a A_a(x)); the credits' (Node, sense) and the births compared through the image.
"""
from __future__ import annotations
import sys, os, json, hashlib, argparse, itertools, copy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'toy'))
import numpy as np
from lean_full import Lean, load_world, wronskian, Z, AXES
from event_universe.core.paces import sine_den

sys.set_int_max_str_digits(0)


def one_sense_packet(b, rec, at, h, n, sense):
    """The toy's `lay_packet` with one sense: the raised cosine's envelope of the half-width h, the largest amplitude A at which
    the one record's share at the vacuum's weight, summed over the packet, is at most n quanta of its unit; the lines at the
    band's rest rotation: re_now = A w_i div w_0, re_before = re_now num div den, im_now = 0, im_before = sense re_now s div den."""
    weights = {2: (2, 1), 3: (4, 3, 1)}[h]
    r_ = b.records()[rec]; num = r_.pair[0]; sn = sine_den(num, b.den); w0 = weights[0] ** 3
    envelope = Z(b.shape)
    for j in np.ndindex(*(2 * h - 1,) * 3):
        off = [x - (h - 1) for x in j]
        envelope[tuple((at[a] + off[a]) % b.cube for a in range(3))] += weights[abs(off[0])] * weights[abs(off[1])] * weights[abs(off[2])]
    c = b.content(); factors = b.link_factors(); r = b.rule_of(r_, c, factors); b.start_content = c
    def record(A):
        re_now = (A * envelope) // w0
        return re_now, (re_now * num) // b.den, Z(b.shape), sense * ((re_now * sn) // b.den)
    def share_of(A):
        re_now, re_before, im_now, im_before = record(A)
        from lean_full import Line
        re = Line(re_now, re_before, None, b.w); im = Line(im_now, im_before, None, b.w)
        return int(sum(int(x) for x in (b.share(re, r, vacuum=True) + b.share(im, r, vacuum=True)).reshape(-1)))
    target = n * b.units[rec]
    high = 1
    while share_of(high) <= target: high = high + high
    low = 0
    while high - low > 1:
        middle = (low + high) // 2
        if share_of(middle) <= target: low = middle
        else: high = middle
    b.lay(rec, Ellipsis, record(low))
    return low, share_of(low)


def profile_of(b, mode, strength, line_axis, vary_axis, centre):
    """The odd line's hand-set profile as an array: A_{line_axis} as a function of the coordinate along vary_axis."""
    arr = Z(b.shape)
    if mode == 'none': return None
    for node in np.ndindex(*b.shape):
        if mode == 'uniform': arr[node] = strength
        elif mode == 'gradient': arr[node] = strength * (node[vary_axis] - centre)
        else: raise ValueError(mode)
    return arr


def impose(b, line_axis, arr):
    """Set the shape-4 row's odd line `line_axis` (lines 1..3) to the profile in both levels; returns the levels overwritten."""
    line = b.row(4).lines[1 + line_axis]
    saved = (line.now.copy(), line.before.copy())
    line.now = arr.copy(); line.before = arr.copy()
    return saved


def restore(b, line_axis, saved):
    line = b.row(4).lines[1 + line_axis]
    line.now, line.before = saved[0].copy(), saved[1].copy()


def state_hash(b): return hashlib.sha256(b.state_bytes() + str(b.interval).encode()).hexdigest()


def reader(b, rec):
    """The reader's row for one record: the weights re^2 + im^2 split by the sign of the Node's W; the centroids in thousandths
    of a Link; the record's W total and |W| sum; the count in units of the record (the share at the vacuum's weight over the unit)."""
    re, im = b.records()[rec].lines
    wgt = re.now * re.now + im.now * im.now; W = wronskian(re, im)
    idx = np.indices(b.shape)
    out = {}
    for name, mask in (('all', None), ('W>0', W > 0), ('W<0', W < 0), ('W=0', W == 0)):
        m = wgt if mask is None else np.where(mask, wgt, 0)
        total = int(sum(int(x) for x in m.reshape(-1)))
        if total == 0: out[name] = {'weight': 0}; continue
        cen = [int(sum(int(w) * int(x) for w, x in zip(m.reshape(-1), idx[a].reshape(-1)))) * 1000 // total for a in range(3)]
        out[name] = {'weight': total, 'centroid_milli': cen, 'nodes': int(sum(1 for x in m.reshape(-1) if int(x) > 0))}
    out['W_total'] = int(sum(int(x) for x in W.reshape(-1))); out['W_abs'] = int(sum(abs(int(x)) for x in W.reshape(-1)))
    c = b.content(); factors = b.link_factors(); r = b.rule_of(b.records()[rec], c, factors); b.start_content = c
    sh = b.share(re, r, vacuum=True) + b.share(im, r, vacuum=True)
    tot = int(sum(int(x) for x in sh.reshape(-1)))
    out['share_total'] = tot; out['count_units'] = tot // b.units[rec]; out['count_rem'] = tot % b.units[rec]
    out['nodes_at_or_above_one_unit'] = int(sum(1 for x in sh.reshape(-1) if int(x) >= b.units[rec]))
    return out


def build(args, image=None):
    universe = json.load(open(os.path.join(HERE, 'toy', args.universe)))
    cube = args.cube; centre = (cube // 2,) * 3
    world = {'universe': args.universe, 'shape': [cube, cube, cube], 'intervals': args.intervals, 'seed': ([{'lay': 'sea', 'row': 0}] if args.sea else [])}
    b = Lean(universe, world)
    rec = b.records().index(b.by_index[args.row])
    at = centre
    if image is not None: at = tuple(int(x) % cube for x in (image @ np.array(at, dtype=int)))
    A, share = one_sense_packet(b, rec, at, args.width, args.quanta, args.sense) if args.sense != 0 else (None, None)
    if args.sense == 0:
        A1, s1 = one_sense_packet(b, rec, at, args.width, args.quanta, 1); A2, s2 = one_sense_packet(b, rec, at, args.width, args.quanta, -1); A, share = (A1, A2), (s1, s2)
    prof = None
    if args.odd != 'none':
        if image is None:
            prof = {args.line_axis: profile_of(b, args.odd, args.strength, args.line_axis, args.vary_axis, cube // 2)}
        else:
            # the odd lines carried as a vector under the signed permutation g: A'_{a'}(g x) = s_a A_a(x), a' the image axis of a
            base = profile_of(b, args.odd, args.strength, args.line_axis, args.vary_axis, cube // 2)
            col = image[:, args.line_axis]; a_img = int(np.nonzero(col)[0][0]); s_a = int(col[a_img])
            arr = Z(b.shape)
            for node in np.ndindex(*b.shape):
                gx = tuple(int(x) % cube for x in (image @ np.array(node, dtype=int)))
                arr[gx] = s_a * base[node]
            prof = {a_img: arr}
    return b, rec, A, share, prof


def run(args, image=None, verbose=True):
    b, rec, A, share, prof = build(args, image)
    hashes = []; saved_stack = []
    rows = []
    def impose_all():
        saved = {}
        if prof is not None:
            for la, arr in prof.items(): saved[la] = impose(b, la, arr)
        return saved
    # the hand-set profile is part of the seed (set once) or held (re-imposed at every interval)
    if prof is not None and not args.held: impose_all()
    rows.append({'i': 0, 'reader': reader(b, rec)})
    for t in range(args.intervals):
        if args.back and t >= args.intervals - args.back: hashes.append(state_hash(b))
        if args.held: saved_stack.append(impose_all())
        b.step()
        if (b.interval % args.every) == 0 or b.interval == args.intervals: rows.append({'i': b.interval, 'reader': reader(b, rec)})
    credits = [{'i': e['i'], 'node': e['node'], 'line': e['line'], 'sense': e['sense'], 'beat': e['beat'], 'taken': e['taken'], 'turned': e['turned']} for e in b.log if e['event'] == 'credit']
    births = [{'i': e['i'], 'node': e['node'], 'line_pair': e['line_pair'], 'W_children': e['W_children'], 'minus': e['minus'], 'plus': e['plus'], 'taken': e['taken'], 'booked': e['booked']} for e in b.log if e['event'] == 'birth']
    n_int, bits = b.census()
    out = {'args': vars(args), 'record_index': rec, 'unit': b.units[rec], 'amplitude': A, 'share_laid': share, 'rows': rows, 'credits': credits, 'births': births,
           'counts': {k: int(v) for k, v in b.counts.items()}, 'integers': n_int, 'max_bits': bits, 'max_transient_bits': b.max_transient}
    if args.back:
        exact = 0
        for k in range(args.back):
            b.step_back()
            if args.held:
                saved = saved_stack.pop()
                for la, sv in saved.items(): restore(b, la, sv)
            exact += (state_hash(b) == hashes[args.back - 1 - k])
        out['run_back'] = {'intervals': args.back, 'exact': exact}
    return out, b


def signed_permutations():
    axes = range(3)
    return [np.array([[s[a] if pi[a] == bb else 0 for a in axes] for bb in axes]) for pi in itertools.permutations(axes) for s in itertools.product((1, -1), repeat=3)]


def images48(args):
    """The 48: the seed and the odd profile carried through each signed permutation; the credits' (interval, Node, line, sense)
    and the births' (interval, Node, pair, minus, plus) compared through the image; the senses kept counted against exchanged."""
    args.back = 0
    base, _b = run(args, None, False)
    def creds(o): return sorted((c['i'], tuple(c['node']), c['line'], c['sense']) for c in o['credits'])
    def birth_set(o): return sorted((e['i'], tuple(e['node']), e['line_pair'], tuple(e['minus']), tuple(e['plus'])) for e in o['births'])
    def img(m, node): return tuple(int(x) % args.cube for x in (m @ np.array(node, dtype=int)))
    held = 0; exchanged = 0; apart = []; dets = []
    for m in signed_permutations():
        other, _o = run(args, m, False)
        mc = sorted((i, img(m, n), l, s) for i, n, l, s in creds(base)); mcx = sorted((i, img(m, n), l, -s) for i, n, l, s in creds(base))
        mb = sorted((i, img(m, n), l, img(m, mi), img(m, pl)) for i, n, l, mi, pl in birth_set(base))
        oc = creds(other); ob = birth_set(other)
        det = int(round(np.linalg.det(m)))
        if oc == mc and ob == mb: held += 1
        elif oc == mcx and ob == mb: exchanged += 1
        else: apart.append({'m': m.tolist(), 'det': det, 'credits_equal': oc == mc, 'births_equal': ob == mb, 'credits_base': len(mc), 'credits_other': len(oc)})
        dets.append(det)
    return {'base_credits': len(base['credits']), 'base_births': len(base['births']), 'images_senses_kept': held, 'images_senses_exchanged': exchanged, 'apart': apart[:8], 'apart_count': len(apart)}


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--universe', default='universe_middle.json'); p.add_argument('--cube', type=int, default=9); p.add_argument('--intervals', type=int, default=60)
    p.add_argument('--row', type=int, default=2); p.add_argument('--width', type=int, default=3); p.add_argument('--quanta', type=int, default=218); p.add_argument('--sense', type=int, default=1)
    p.add_argument('--odd', default='none'); p.add_argument('--strength', type=int, default=0); p.add_argument('--line-axis', type=int, default=0); p.add_argument('--vary-axis', type=int, default=1)
    p.add_argument('--held', action='store_true'); p.add_argument('--sea', type=int, default=1); p.add_argument('--back', type=int, default=0); p.add_argument('--every', type=int, default=10)
    p.add_argument('--images48', action='store_true'); p.add_argument('--out', default=None)
    args = p.parse_args()
    if args.images48:
        found = images48(args); print(json.dumps(found))
    else:
        found, b = run(args)
        summary = {'credits': len(found['credits']), 'credits_by_sense': {s: sum(1 for c in found['credits'] if c['sense'] == s) for s in (-1, 0, 1)}, 'births': len(found['births']), 'counts': found['counts'],
                   'integers': found['integers'], 'max_bits': found['max_bits'], 'max_transient_bits': found['max_transient_bits'], 'run_back': found.get('run_back'), 'amplitude': found['amplitude'], 'share_laid': found['share_laid'], 'unit': found['unit']}
        print(json.dumps(summary))
        for row in found['rows']: print(json.dumps(row))
    if args.out:
        json.dump(found, open(args.out, 'w'))
