"""ob2's probe of David's toy (tools/derivations/open_items/H-Everything-The-Clicks-Show-2/toy, never edited): the toy's Node is imported and driven; every reading an integer (a quotient at a named scale, a count, a bit length, a sign).

Modes (sys.argv[1]):
  bodies <world.json> <intervals> <back> <out.jsonl>   the bodies' seed: per interval and per record the z-profile (the record's weight re^2 + im^2 summed over x and y per z-plane), its peaks (local maxima along z), its centroid in thousandths of a Link, its lattice momentum per axis as the board reads it (SUM over Links of (now_i+a before_i - now_i before_i+a) per line), the light's momentum change at every close (the momentum across the click), the counts; the run back's exactness.
  coulomb <cube> <intervals> <out.jsonl>               the force's sign: the sea laid, then two one-quantum records of the heavy lift laid by the law's quarter-turn lay at adjacent Nodes along z, (i) unlike senses, (ii) like senses, (iii) one record alone (the control); every 10 intervals the centroid along z of the weight standing in the low half and in the high half of the axis, in thousandths, and the two records' own centroids where they are two records.
  sea <world.json> <intervals> <out.jsonl>             the hole seed: the light's momentum change at every close per axis, the births' senses, the credits' running cosine per axis with the current's sign, their sums.
"""
import json
import math
import os
import sys

sys.set_int_max_str_digits(0)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'toy'))
import numpy as np  # noqa: E402
import lean_full as lf  # noqa: E402
from event_universe.core import paces  # noqa: E402

AXES = lf.AXES  # (axis, side) in the toy's Port order


def Q_axis(line, axis, cube):
    """The lattice momentum's board reading along one axis for one line: SUM_i (now_(i+a) before_i - now_i before_(i+a)) on the torus, an integer (the current F over num, halved)."""
    shifted_now = np.roll(line.now, -1, axis=axis); shifted_before = np.roll(line.before, -1, axis=axis)
    return int(sum(int(x) for x in (shifted_now * line.before - line.now * shifted_before).reshape(-1)))


def weight_of(re, im):
    return re.now * re.now + im.now * im.now


def centroid_thousandths(w, axis, mask=None):
    """The centroid along one axis in thousandths of a Link, a quotient (the remainder dropped); None where no weight stands."""
    idx = np.indices(w.shape)[axis]
    if mask is not None: w = np.where(mask, w, 0)
    total = int(sum(int(x) for x in w.reshape(-1)))
    if total == 0: return None, 0
    return int(sum(int(a) * int(b) for a, b in zip(w.reshape(-1), idx.reshape(-1)))) * 1000 // total, total


def profile(w, axis):
    other = tuple(a for a in range(3) if a != axis)
    return [int(x) for x in np.sum(np.sum(w, axis=other[1]), axis=other[0]).reshape(-1)]


def peaks(prof):
    """The local maxima along the axis on the torus (a plane above both neighbours, or above one and equal to the other and above 0)."""
    n = len(prof); out = []
    for i in range(n):
        a, b, c = prof[(i - 1) % n], prof[i], prof[(i + 1) % n]
        if b > 0 and ((b > a and b >= c) or (b >= a and b > c)): out.append(i)
    return out


def reduced(num, den):
    g = math.gcd(abs(num), abs(den)) or 1
    return [num // g, den // g]


class Probe(lf.Lean):
    """The toy's Node with two readings added at the close: the light's momentum before and after the close, and the running cosine at every credit (the credit line's momentum, [sign, num, den] per axis)."""

    def __init__(self, universe, world):
        super().__init__(universe, world)
        self.dq_light = []  # per close: [interval, [dQ_x, dQ_y, dQ_z]]
        self.credit_momenta = []

    def light_Q(self):
        return [Q_axis(self.light, a, self.cube) for a in range(3)]

    def close(self, start):
        q0 = self.light_Q()
        super().close(start)
        q1 = self.light_Q()
        self.dq_light.append([self.interval, [b - a for a, b in zip(q0, q1)]])

    def credit(self, rec, at, start, fall, levels, light_was):
        line = super().credit(rec, at, start, fall, levels, light_was)
        re0, im0 = start['planes'][rec]
        mom = []
        for axis in range(3):
            plus = tuple((at[a] + (1 if a == axis else 0)) % self.cube for a in range(3))
            minus = tuple((at[a] - (1 if a == axis else 0)) % self.cube for a in range(3))
            n_i = int(re0.now[at]); n_p = int(re0.now[plus]); n_m = int(re0.now[minus])
            # the current's antisymmetric term along the axis at the start, on the re line: F(i, i-a) - F(i, i+a) with F_ij = now_i before_j - before_i now_j
            b_i = int(re0.before[at]); b_p = int(re0.before[plus]); b_m = int(re0.before[minus])
            f = (n_i * b_m - b_i * n_m) - (n_i * b_p - b_i * n_p)
            sign = 1 if f > 0 else -1 if f < 0 else 0
            pair = reduced(n_p + n_m, 2 * n_i) if n_i != 0 else None
            mom.append([sign, pair])
        line['ob2_momentum'] = mom
        self.credit_momenta.append([self.interval, list(at), rec, mom])
        return line


def state_hash(b):
    import hashlib
    return hashlib.sha256(b.state_bytes() + str(b.interval).encode()).hexdigest()


def run_bodies(world_path, intervals, back, out_path):
    universe, world = lf.load_world(world_path)
    b = Probe(universe, world)
    out = open(out_path, 'w')
    out.write(json.dumps({'mode': 'bodies', 'world': world, 'den': b.den, 'units': b.units, 'unit_light': b.unit_light, 'lay': [e for e in b.log if e['event'] == 'lay']}) + '\n')
    hashes = []
    def reading():
        recs = {}
        for rec in range(2 * b.nl):
            re, im = b.planes[rec]; w = weight_of(re, im)
            total = int(sum(int(x) for x in w.reshape(-1)))
            if total == 0: continue
            prof = profile(w, 2)
            recs['lift %d sense %+d' % (rec // 2, 1 if rec % 2 else -1)] = {
                'z profile (weight per z-plane)': prof, 'peaks z': peaks(prof), 'centroid z thousandths': centroid_thousandths(w, 2)[0],
                'nodes with weight': int(sum(1 for x in w.reshape(-1) if int(x) > 0)), 'weight bits': total.bit_length(),
                'Q per axis (re+im)': [Q_axis(re, a, b.cube) + Q_axis(im, a, b.cube) for a in range(3)]}
        return recs
    out.write(json.dumps({'i': 0, 'records': reading(), 'light Q': b.light_Q()}) + '\n')
    for t in range(intervals):
        if back and t >= intervals - back: hashes.append(state_hash(b))
        b.step()
        if b.interval <= 10 or b.interval % 10 == 0 or b.interval == intervals:
            row = {'i': b.interval, 'records': reading(), 'light Q': b.light_Q(), 'counts': {k: int(v) for k, v in b.counts.items()}, 'closes with dQ_light nonzero': sum(1 for _i, d in b.dq_light if any(d)), 'closes': len(b.dq_light), 'sum dQ_light': [sum(d[a] for _i, d in b.dq_light) for a in range(3)], 'content min/max': [min(int(x) for x in b.content().reshape(-1)), max(int(x) for x in b.content().reshape(-1))], 'integers per Node': b.census()[0], 'max bits': b.census()[1]}
            out.write(json.dumps(row) + '\n'); out.flush()
    exact = 0
    for k in range(back):
        b.step_back(); exact += (state_hash(b) == hashes[back - 1 - k])
    senses = [sum(1 for _i, _a, rec, _m in b.credit_momenta if rec % 2) , sum(1 for _i, _a, rec, _m in b.credit_momenta if not rec % 2)]
    sign_sums = [sum(m[a][0] for _i, _at, _r, m in b.credit_momenta) for a in range(3)]
    out.write(json.dumps({'run back': {'intervals': back, 'exact': exact}, 'credits': len(b.credit_momenta), 'credits by sense (+, -)': senses, 'credits running-cosine sign sums per axis': sign_sums, 'closes': len(b.dq_light), 'closes with dQ_light nonzero': sum(1 for _i, d in b.dq_light if any(d)), 'sum dQ_light per axis': [sum(d[a] for _i, d in b.dq_light) for a in range(3)], 'max |dQ_light| per close': max([max(abs(x) for x in d) for _i, d in b.dq_light] or [0])}) + '\n')
    out.close()


def lay_one(b, s_, at, sense):
    """The law's lay of one quantum of a lift at one Node (the birth's quarter turn: re_now + A, im_before + sense A), A the toy's own lay_amplitude at the Node's paces."""
    c = b.content(); factors = b.link_factors(); pace = paces.link_pace_of(b.gamma, c); b.start_content = c
    A = b.lay_amplitude(s_, at, c, factors, pace)
    rec = 2 * s_ + (1 if sense > 0 else 0)
    re, im = b.planes[rec]
    re.now[at] = re.now[at] + A; im.before[at] = im.before[at] + sense * A
    return A


def run_coulomb(cube, intervals, out_path):
    universe_path = os.path.join(HERE, 'toy', 'universe_middle.json')
    universe = json.load(open(universe_path))
    heavy = max(range(len([r for r in universe['rows'] if r['shape'] == 2])), key=lambda k: 0)  # the heavy lift chosen below by the pair's gap
    out = open(out_path, 'w')
    cases = {'unlike': [(-1, 0), (1, 1)], 'like': [(1, 0), (1, 1)], 'single': [(1, 0)]}
    mid = cube // 2
    A_node = (mid, mid, mid); B_node = (mid, mid, mid + 1)
    nodes = [A_node, B_node]
    for name, lays in cases.items():
        world = {'universe': universe_path, 'shape': [cube] * 3, 'intervals': intervals, 'seed': [{'lay': 'sea', 'row': [universe['integers']['den']] * 2}]}
        b = Probe(universe, world)
        # the heavy lift: the pair with the largest gap den - num
        s_ = max(range(b.nl), key=lambda k: b.den - b.pairs[k][0])
        amps = [lay_one(b, s_, nodes[k], sense) for sense, k in lays]
        low = np.indices(b.shape)[2] <= mid; high = np.indices(b.shape)[2] > mid
        def reading():
            row = {}
            for rec in range(2 * b.nl):
                re, im = b.planes[rec]; w = weight_of(re, im)
                total = int(sum(int(x) for x in w.reshape(-1)))
                if total == 0: continue
                cl, wl = centroid_thousandths(w, 2, low); ch, wh = centroid_thousandths(w, 2, high); cz, _t = centroid_thousandths(w, 2)
                row['sense %+d' % (1 if rec % 2 else -1)] = {'centroid z': cz, 'centroid z low half': cl, 'centroid z high half': ch, 'weight low half (thousandths)': wl * 1000 // total, 'weight bits': total.bit_length(), 'Q_z (re+im)': Q_axis(re, 2, b.cube) + Q_axis(im, 2, b.cube)}
            return row
        out.write(json.dumps({'case': name, 'lift': s_, 'pair': b.pairs[s_], 'unit': b.units[s_], 'nodes': nodes[:len(lays)], 'senses': [s for s, _k in lays], 'amplitudes': amps, 'i': 0, 'reading': reading()}) + '\n')
        for t in range(intervals):
            b.step()
            if b.interval % 10 == 0 or b.interval <= 3:
                out.write(json.dumps({'case': name, 'i': b.interval, 'reading': reading(), 'sign level max': max(abs(int(x)) for x in b.sign.now.reshape(-1)), 'W total': sum(int(x) for re, im in b.planes for x in (re.now * im.before - im.now * re.before).reshape(-1)), 'counts': {k: int(v) for k, v in b.counts.items()}, 'content min/max': [min(int(x) for x in b.content().reshape(-1)), max(int(x) for x in b.content().reshape(-1))], 'turns': int(b.counts['turns'])}) + '\n'); out.flush()
    out.close()


def run_sea(world_path, intervals, out_path):
    universe, world = lf.load_world(world_path)
    b = Probe(universe, world)
    out = open(out_path, 'w')
    for t in range(intervals): b.step()
    births = [e for e in b.log if e['event'] == 'birth']
    credits = [e for e in b.log if e['event'] == 'credit']
    senses_births = sum(sum(e['senses']) for e in births)
    sign_sums = [sum(m[a][0] for _i, _at, _r, m in b.credit_momenta) for a in range(3)]
    nz = sum(1 for _i, d in b.dq_light if any(d))
    out.write(json.dumps({'mode': 'sea', 'world': world, 'intervals': intervals, 'births': len(births), 'senses summed over the births': senses_births, 'credits': len(credits), 'credits running-cosine sign sums per axis': sign_sums, 'credits with sign 0 on every axis': sum(1 for _i, _at, _r, m in b.credit_momenta if all(x[0] == 0 for x in m)), 'closes': len(b.dq_light), 'closes with dQ_light nonzero': nz, 'sum dQ_light per axis over the run': [sum(d[a] for _i, d in b.dq_light) for a in range(3)], 'max |dQ_light| per close': max([max(abs(x) for x in d) for _i, d in b.dq_light] or [0]), 'light Q at the end': b.light_Q(), 'records Q at the end (sum over records, per axis)': [sum(Q_axis(l, a, b.cube) for rec in b.planes for l in rec) for a in range(3)], 'first 12 closes dQ': b.dq_light[:12], 'counts': {k: int(v) for k, v in b.counts.items()}}) + '\n')
    for e in credits[:40]:
        out.write(json.dumps({'credit': {'i': e['i'], 'node': e['node'], 'line': e['line'], 'sense': e['sense'], 'beat': e['beat'], 'proper': e['proper'], 'ob2_momentum': e['ob2_momentum']}}) + '\n')
    out.close()

def displacement_thousandths(w, axis, z0, cube):
    """The record's centre read from its own start Node z0 along the axis on the torus: d(z) = ((z - z0 + cube div 2) mod cube) - cube div 2 in -cube div 2 .. cube div 2, the weighted mean in thousandths (integer division). A spread symmetric about z0 reads exactly 0: the null of the force's sign."""
    idx = np.indices(w.shape)[axis]
    d = ((idx - z0 + cube // 2) % cube) - cube // 2
    total = int(sum(int(x) for x in w.reshape(-1)))
    if total == 0: return None
    num = int(sum(int(x) for x in (w * d).reshape(-1)))
    return (num * 1000) // total if num >= 0 else -((-num * 1000) // total)


def run_coulomb2(cube, intervals, out_path, novol=False):
    """The force's sign with a null control and two separable records per case: 'heavy' the lift of the largest gap, 'light' the lift of the smallest; a record is one plane per sense per lift, so two records of ONE sense need two lifts. Cases: single3/single4 (one record, the null), unlike (heavy +1 at z0, heavy -1 at z0+1), unlike2 (heavy +1 at z0, light -1 at z0+1), like2 (heavy +1 at z0, light +1 at z0+1), unlike2r (heavy -1 at z0, light +1 at z0+1), like2m (heavy -1 at z0, light -1 at z0+1). Read: each record's displacement from its own start Node along z (thousandths of a Node), positive toward larger z, every 10 intervals."""
    universe_path = os.path.join(HERE, 'toy', 'universe_middle.json')
    universe = json.load(open(universe_path))
    out = open(out_path, 'w')
    mid = cube // 2
    nodes = [(mid, mid, mid), (mid, mid, mid + 1)]
    cases = {
        'single3': [(1, 0, 'heavy')], 'single4': [(1, 1, 'heavy')], 'single4light': [(1, 1, 'light')],
        'unlike': [(1, 0, 'heavy'), (-1, 1, 'heavy')],
        'unlike2': [(1, 0, 'heavy'), (-1, 1, 'light')], 'like2': [(1, 0, 'heavy'), (1, 1, 'light')],
        'unlike2r': [(-1, 0, 'heavy'), (1, 1, 'light')], 'like2m': [(-1, 0, 'heavy'), (-1, 1, 'light')],
    }
    for name, lays in cases.items():
        world = {'universe': universe_path, 'shape': [cube] * 3, 'intervals': intervals, 'seed': [{'lay': 'sea', 'row': [universe['integers']['den']] * 2}]}
        if novol: world['control'] = {'well': {'at': [0, 0, 0], 'levels': 0, 'radius': 0, 'held': True}}  # the toy's own control: the volume held flat, no gravity; the sign row and the planes act
        b = Probe(universe, world)
        heavy = max(range(b.nl), key=lambda k: b.den - b.pairs[k][0]); light = min(range(b.nl), key=lambda k: b.den - b.pairs[k][0])
        lift_of = {'heavy': heavy, 'light': light}
        amps = [lay_one(b, lift_of[lift], nodes[k], sense) for sense, k, lift in lays]
        recs = [(2 * lift_of[lift] + (1 if sense > 0 else 0), nodes[k][2], sense, lift) for sense, k, lift in lays]
        def reading():
            row = {}
            for rec, z0, sense, lift in recs:
                re, im = b.planes[rec]; w = weight_of(re, im)
                total = int(sum(int(x) for x in w.reshape(-1)))
                row['%s %+d at z=%d' % (lift, sense, z0)] = {'displacement z (thousandths)': displacement_thousandths(w, 2, z0, b.cube), 'displacement x': displacement_thousandths(w, 0, mid, b.cube), 'displacement y': displacement_thousandths(w, 1, mid, b.cube), 'weight bits': total.bit_length(), 'Q_z (re+im)': Q_axis(re, 2, b.cube) + Q_axis(im, 2, b.cube)}
            return row
        out.write(json.dumps({'case': name, 'lays': [[s, list(nodes[k]), l, lift_of[l], b.pairs[lift_of[l]]] for s, k, l in lays], 'amplitudes': amps, 'i': 0, 'reading': reading()}) + '\n')
        for t in range(intervals):
            b.step()
            if b.interval % 10 == 0 or b.interval <= 3:
                out.write(json.dumps({'case': name, 'i': b.interval, 'reading': reading(), 'sign level max': max(abs(int(x)) for x in b.sign.now.reshape(-1)), 'sign level at the two Nodes': [int(b.sign.now[n]) for n in nodes], 'W total': sum(int(x) for re, im in b.planes for x in (re.now * im.before - im.now * re.before).reshape(-1)), 'births': int(b.counts['births']), 'body_clicks': int(b.counts['body_clicks']), 'light_laid': int(b.counts['light_laid'])}) + '\n'); out.flush()
    out.close()


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'bodies': run_bodies(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5])
    elif mode == 'coulomb': run_coulomb(int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])
    elif mode == 'sea': run_sea(sys.argv[2], int(sys.argv[3]), sys.argv[4])
    elif mode == 'coulomb2': run_coulomb2(int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])
    elif mode == 'coulomb2novol': run_coulomb2(int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], novol=True)
    else: raise SystemExit('a mode of no name')
