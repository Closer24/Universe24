"""mv1: the measurements of the moving lay on the flagged copy lean_mv1.py (integers only; every reading a quotient with its remainder or a count).
Usage: python measure_mv1.py <world.json> <out.json> <intervals> [back N] [images N]
Readings per interval, from the board: each plane row's share per Node at the vacuum's weight (the count's density), its share centroid along each axis in milli-Links with the torus unwrapped about the last centroid, its peak Node, its lattice momentum P_a = 2 num SUM_i (now_(i+a) before_i - now_i before_(i+a)) over its two lines, its Wronskian sum and absolute sum (the charge), its count (share div unit, remainder), the content's range, the census; the velocity as the integer least-squares slope of the centroid over the run and over windows of 10; the run back by hash; the 48 images (the seed's centres and waves carried through each signed permutation, the plane rows' lines and the volume and light rows compared through the image at the last interval, the births mapped)."""
import sys, os, json, hashlib, itertools, copy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from lean_mv1 import Lean, load_world, wronskian, AXES
from event_universe.core import paces


def momentum(b, r):
    """The lattice momentum of a shape-2 row over its two lines, per axis: 2 num SUM_i (now_(i+a) before_i - now_i before_(i+a)) (ALGEBRA.md, The lattice momentum), a reading."""
    num = r.pair[0]; found = []
    for a in range(3):
        total = 0
        for l in r.lines:
            up_now = np.roll(l.now, -1, axis=a); up_before = np.roll(l.before, -1, axis=a)
            total += int(sum(int(x) for x in (up_now * l.before - l.now * up_before).reshape(-1)))
        found.append(2 * num * total)
    return found


def shares(b, r):
    c = b.content(); factors = b.link_factors(); rule = b.rule_of(r, c, factors)
    re, im = r.lines
    return b.share(re, rule, vacuum=True) + b.share(im, rule, vacuum=True)


def deviation_shares(b, r):
    """The massless row's packet read against the sea: the lines less their board means (the sea's drift is uniform and a gauge; P_a is blind to it), the share of the deviation."""
    c = b.content(); factors = b.link_factors(); rule = b.rule_of(r, c, factors)
    from lean_mv1 import Line
    lines = []
    for l in r.lines:
        flat = l.now.reshape(-1); n = len(flat); mean_now = sum(int(x) for x in flat) // n
        flatb = l.before.reshape(-1); mean_before = sum(int(x) for x in flatb) // n
        lines.append(Line(l.now - mean_now, l.before - mean_before, None, l.wall))
    return b.share(lines[0], rule, vacuum=True) + b.share(lines[1], rule, vacuum=True)


def centroid(sh, ref, cube):
    """The share-weighted centroid in milli-Links about the reference Node (offsets wrapped into (-cube/2, cube/2]), and the peak Node, with the total share."""
    total = int(sum(int(x) for x in sh.reshape(-1)))
    if total <= 0: return None, None, 0
    idx = np.indices(sh.shape); found = []
    for a in range(3):
        off = (idx[a] - ref[a] + cube // 2) % cube - cube // 2
        weighted = int(sum(int(w) * int(d) for w, d in zip(sh.reshape(-1), off.reshape(-1))))
        found.append(ref[a] * 1000 + (weighted * 1000) // total)
    flat = [int(x) for x in sh.reshape(-1)]; peak = int(np.argmax(np.array(flat, dtype=object)))
    peak_node = tuple(int(x) for x in np.unravel_index(peak, sh.shape))
    return found, peak_node, total


def slope(xs):
    """The integer least-squares slope of xs (milli-Links) against the interval: the quotient and the remainder of (n SUM t x - SUM t SUM x) over (n SUM t^2 - (SUM t)^2)."""
    n = len(xs); ts = list(range(n))
    num = n * sum(t * x for t, x in zip(ts, xs)) - sum(ts) * sum(xs); den = n * sum(t * t for t in ts) - sum(ts) ** 2
    if den == 0: return None
    return [num // den, num % den, den]


def unwrap(prev_ref, cen, cube):
    return tuple(int((c + 500) // 1000) % cube for c in cen)


def readings(b, world, track, refs):
    out = {'i': b.interval, 'content min/max': None, 'rows': {}}
    c = b.content(); cs = [int(x) for x in c.reshape(-1)]; out['content min/max'] = [min(cs), max(cs)]
    p = paces.link_pace_of(b.gamma, c); ps = [int(x) for x in np.asarray(p, dtype=object).reshape(-1)]; out['pace min/max'] = [min(ps), max(ps)]
    for rec, r in enumerate(b.records()):
        if rec not in track: continue
        sh = deviation_shares(b, r) if r.gap == 0 else shares(b, r)
        ref = refs.get(rec, track[rec])
        cen, peak, total = centroid(sh, ref, b.cube)
        if cen is not None: refs[rec] = unwrap(ref, cen, b.cube)
        W = wronskian(*r.lines); Wsum = int(sum(int(x) for x in W.reshape(-1))); Wabs = int(sum(abs(int(x)) for x in W.reshape(-1)))
        unit = b.units[rec]
        out['rows'][str(rec)] = {'centroid milli': cen, 'peak': peak, 'share': total, 'count': [total // unit, total % unit], 'P': momentum(b, r), 'W sum': Wsum, 'W abs': Wabs,
                                 'nodes above unit': int(sum(1 for x in sh.reshape(-1) if int(x) >= unit)), 'nodes with share': int(sum(1 for x in sh.reshape(-1) if int(x) > 0))}
    n, bits = b.census(); out['integers'] = n; out['bits'] = bits; out['transient bits'] = b.max_transient
    out['counts'] = dict(b.counts)
    return out


def run(universe, world, intervals, back=0, track=None):
    b = Lean(universe, world)
    track = track if track is not None else {}
    for lay in world.get('seed', []):
        if lay.get('lay') == 'at' and 'width' in lay or (lay.get('lay') == 'at' and 'wave' in lay):
            rec = b.records().index(b.by_index[int(lay['row'])]); track.setdefault(rec, tuple(int(x) for x in lay['centre']))
    refs = {}
    rows = [readings(b, world, track, refs)]
    hashes = []
    for t in range(intervals):
        if back and t >= intervals - back: hashes.append(b.state_hash())
        b.step(); rows.append(readings(b, world, track, refs))
    lays = [e for e in b.log if e['event'] == 'lay']; births = [e for e in b.log if e['event'] == 'birth']; credits = [e for e in b.log if e['event'] == 'credit']
    result = {'world': world, 'intervals': intervals, 'lays': lays, 'births': births, 'credits': credits, 'rows': rows, 'counts': dict(b.counts), 'band_pair': [str(x) for x in getattr(b, 'band_pair', ())], 'n_edge': getattr(b, 'n_edge', None), 'X': b.X}
    for rec in track:
        xs = [row['rows'][str(rec)]['centroid milli'] for row in rows if row['rows'][str(rec)]['centroid milli'] is not None]
        vel = {}
        for a in range(3):
            series = [x[a] for x in xs]
            vel['axis %d whole' % a] = slope(series)
            vel['axis %d windows of 10' % a] = [slope(series[k:k + 11]) for k in range(0, len(series) - 10, 10)]
            vel['axis %d positions' % a] = series
        result['velocity row %d' % rec] = vel
    if back:
        exact = 0; first_bad = None
        for k in range(back):
            b.step_back()
            if b.state_hash() == hashes[back - 1 - k]: exact += 1
            elif first_bad is None: first_bad = back - 1 - k
        result['run back'] = {'intervals': back, 'exact': exact, 'first mismatch': first_bad}
    return result, b


def signed_permutations():
    axes = range(3)
    return [np.array([[s[a] if pi[a] == bb else 0 for a in axes] for bb in axes]) for pi in itertools.permutations(axes) for s in itertools.product((1, -1), repeat=3)]


def image(m, node, cube):
    v = m @ np.array(node, dtype=int)
    return tuple(int(x) % cube for x in v)


def world_image(world, m, cube):
    w = copy.deepcopy(world)
    for lay in w.get('seed', []):
        for key in ('at', 'centre'):
            if key in lay: lay[key] = list(image(m, tuple(lay[key]), cube))
        if 'wave' in lay: lay['wave'] = [int(x) for x in (m @ np.array(lay['wave'], dtype=int))]
    return w


def events(b):
    return sorted((e['i'], tuple(e['node']), e['line_pair'], tuple(e['minus']), tuple(e['plus'])) for e in b.log if e['event'] == 'birth')


def images_test(universe, world, intervals):
    cube = int(world['shape'][0])
    base = Lean(universe, world)
    for _ in range(intervals): base.step()
    evs = events(base); held = 0; apart = []; swapped = []
    for m in signed_permutations():
        other = Lean(universe, world_image(world, m, cube))
        for _ in range(intervals): other.step()
        mapped = sorted((i, image(m, at, cube), s_, image(m, mi, cube), image(m, pl, cube)) for i, at, s_, mi, pl in evs)
        same_events = events(other) == mapped
        same_rows = True
        lines = [l for r in base.rows_ if r.wall is None for l in r.lines[:2]] ; lines_o = [l for r in other.rows_ if r.wall is None for l in r.lines[:2]]
        for lb, lo in zip(lines, lines_o):
            for at in np.ndindex(cube, cube, cube):
                if int(lb.now[at]) != int(lo.now[image(m, at, cube)]) or int(lb.before[at]) != int(lo.before[image(m, at, cube)]): same_rows = False; break
            if not same_rows: break
        exchanged = (not same_events) and same_rows and events(other) == sorted((i, at, s_, pl, mi) for i, at, s_, mi, pl in mapped)
        if same_events and same_rows: held += 1
        elif exchanged: swapped.append(int(round(np.linalg.det(m))))
        else: apart.append((m.tolist(), 'events' if not same_events else 'rows'))
    return {'intervals': intervals, 'births': len(evs), 'images holding': held, 'of': 48, 'senses exchanged (rotations, reflections)': [swapped.count(1), swapped.count(-1)], 'apart': apart[:6]}


if __name__ == '__main__':
    sys.set_int_max_str_digits(0)
    universe, world = load_world(sys.argv[1]); intervals = int(sys.argv[3])
    back = int(sys.argv[sys.argv.index('back') + 1]) if 'back' in sys.argv else 0
    result, b = run(universe, world, intervals, back)
    if 'images' in sys.argv: result['images'] = images_test(universe, world, int(sys.argv[sys.argv.index('images') + 1]))
    json.dump(result, open(sys.argv[2], 'w'))
    brief = {k: v for k, v in result.items() if k not in ('rows', 'world', 'births', 'credits')}
    brief['lays'] = result['lays']; brief['last'] = result['rows'][-1]; brief['first'] = result['rows'][0]
    print(json.dumps(brief, default=str))
