"""pa1: Wu's parity in the clicks on the lean toy copy (lean_pa1.py): the run from a seed and from each of its 48 images, the click records (the birth lines: the two children's Nodes and senses, the lift, the take's integers; the credit lines: Node, record, sense, beat) compared through the image: equal, the senses exchanged, or neither; the three asymmetries read from the birth lines alone (Wu's as the brief defines it, sense x the momentum's sign along the Link from the - child to the + child; the pseudoscalar sign(d . A), the chirality's axial reading along the born dipole; the C-odd sign of the light's current along the dipole), each a sum of signs with its count; the charge (the senses' sum; the board's Wronskian per record at the end), the exact take, the census (integers per Node, bits), the run back of the base run, and the one-Link reach of a birth (a change two Links from both ends of a birth Link, the birth line compared bit for bit).
Usage: python pa1_clicks48.py <world.json> <cube> <intervals> <orient: current|chirality|label> <out.json>
Integers only; no float."""
import sys, os, itertools, copy, json, hashlib, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from lean_pa1 import Lean, load_world

sys.set_int_max_str_digits(0)


def signed_permutations():
    axes = range(3)
    return [np.array([[s[a] if pi[a] == b else 0 for a in axes] for b in axes]) for pi in itertools.permutations(axes) for s in itertools.product((1, -1), repeat=3)]


def det(m):
    return int(m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0]) + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


def image(m, node, cube):
    v = m @ np.array(node, dtype=int)
    return tuple(int(x) % cube for x in v)


def world_image(world, m, cube):
    w = copy.deepcopy(world); w['shape'] = [cube, cube, cube]
    for lay in w.get('seed', []):
        for key in ('at', 'centre'):
            if key in lay: lay[key] = list(image(m, tuple(lay[key]), cube))
    return w


def run(universe, world, n, orient, hashes=False):
    b = Lean(universe, world); b.orient = orient
    kept = []
    def state_hash(): return hashlib.sha256(b.state_bytes() + str(b.interval).encode()).hexdigest()
    for _ in range(n):
        if hashes: kept.append(state_hash())
        b.step()
    return b, kept, state_hash


def births(b):
    """The birth records as the clicks carry them: interval, lift, the two children (Node, sense), the take's integers."""
    return [(e['i'], e['line_pair'], frozenset(((tuple(e['minus']), -1), (tuple(e['plus']), 1))), e['taken'], e['booked'], e['levels'], e['amplitude']) for e in b.log if e['event'] == 'birth']


def credits(b):
    return [(e['i'], tuple(e['node']), e['line'], e['sense'], e['beat'], e['taken'], e['levels']) for e in b.log if e['event'] == 'credit']


def mapped(evs, m, cube, exchange):
    # the records compared as the clicks carry them: interval, lift, the two children (Node, sense); the take's integers (taken, booked, levels, amplitude) are read at the + end and so move with it under an exchange of the senses: they are compared in `takes` for the equal case alone
    found = []
    for i, s_, children, taken, booked, levels, A in evs:
        kids = frozenset((image(m, node, cube), -sense if exchange else sense) for node, sense in children)
        found.append((i, s_, kids))
    return sorted(found, key=repr)


def takes(evs):
    return sorted((i, s_, taken, booked, levels, A) for i, s_, children, taken, booked, levels, A in evs)


def mapped_credits(evs, m, cube, exchange):
    found = []
    for i, node, line, sense, beat, taken, levels in evs:
        line2 = (line ^ 1) if exchange else line  # the partner record of the lift (2 s + 0 the - record, 2 s + 1 the + record)
        found.append((i, image(m, node, cube), line2, -sense if exchange else sense, beat, taken, levels))
    return sorted(found)


def asymmetries(b):
    """The three sums of signs over the birth lines alone, with their counts (integers)."""
    bl = [e for e in b.log if e['event'] == 'birth']
    wu = sum(e['p_sign']['plus'] * 1 + e['p_sign']['minus'] * -1 for e in bl)  # sense x the momentum's sign along e_pm, summed over the two children
    pseudo = sum(e['A_pm'] for e in bl)  # sign(d . A): the chirality's axial reading along the born dipole
    codd = sum(e['F_pm'] for e in bl)  # the sign of the light's current along the born dipole (C-odd, P-even)
    return {'births': len(bl), 'wu_brief_sum': wu, 'wu_brief_count': 2 * len(bl), 'pseudoscalar_sum': pseudo, 'pseudoscalar_count': len(bl), 'c_odd_sum': codd, 'c_odd_count': len(bl), 'A_pm_zero': sum(1 for e in bl if e['A_pm'] == 0)}


def charge(b):
    found = []
    for rec, (re, im) in enumerate(b.planes):
        found.append(int(sum(int(x) for x in (re.now * im.before - im.now * re.before).reshape(-1))))
    return found


def distance(node, origin, cube):
    return sum(min(abs(node[k] - origin[k]), cube - abs(node[k] - origin[k])) for k in range(3))


def reach(universe, world, orient, n, cube):
    """The one-Link reach of the first birth: the run to the interval before it, a copy with one level of light added at a Node two or more Links from both ends of the birth Link, one interval forward on both, the birth line compared bit for bit, and the differing Nodes by distance."""
    base, _h, _f = run(universe, world, n, orient)
    firsts = [e for e in base.log if e['event'] == 'birth']
    if not firsts: return {'births': 0}
    e0 = firsts[0]; t = e0['i']; minus, plus = tuple(e0['minus']), tuple(e0['plus'])
    far = max(np.ndindex(cube, cube, cube), key=lambda nd: min(distance(nd, minus, cube), distance(nd, plus, cube)))
    dmin = min(distance(far, minus, cube), distance(far, plus, cube))
    a = Lean(universe, world); a.orient = orient
    for _ in range(t - 1): a.step()
    b = copy.deepcopy(a); b.light.now[far] = b.light.now[far] + 1
    a.step(); b.step()
    la = [x for x in a.log if x['event'] == 'birth' and x['i'] == t and tuple(x['minus']) == minus and tuple(x['plus']) == plus]
    lb = [x for x in b.log if x['event'] == 'birth' and x['i'] == t and tuple(x['minus']) == minus and tuple(x['plus']) == plus]
    diffs = {}
    for ra, rb in zip(a.rows(), b.rows()):
        for la_, lb_ in zip(ra, rb):
            for slot in ('now', 'before', 'rem'):
                xa, xb = getattr(la_, slot), getattr(lb_, slot)
                for node in zip(*np.nonzero(np.asarray(xa != xb))):
                    node = tuple(int(x) for x in node); diffs[distance(node, far, cube)] = diffs.get(distance(node, far, cube), 0) + 1
    return {'first birth interval': t, 'link': [list(minus), list(plus)], 'changed node': list(far), 'distance of the change from the nearer end': dmin, 'birth line equal bit for bit': la == lb and len(la) == 1, 'births at that interval a/b': [len([x for x in a.log if x['event'] == 'birth' and x['i'] == t]), len([x for x in b.log if x['event'] == 'birth' and x['i'] == t])], 'differing lines by distance from the change': diffs}


if __name__ == '__main__':
    world_path, cube, n, orient, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5]
    universe, world0 = load_world(world_path)
    t0 = time.monotonic_ns()
    identity = np.eye(3, dtype=int)
    base, hashes, state_hash = run(universe, world_image(world0, identity, cube), n, orient, hashes=True)
    evs, crs = births(base), credits(base)
    integers, bits = base.census()
    result = {'world': world0.get('seed'), 'cube': cube, 'intervals': n, 'orient': orient, 'counts': {k: str(v) for k, v in base.counts.items()}, 'base asymmetries': asymmetries(base), 'charge: senses sum over births': sum(s for e in base.log if e['event'] == 'birth' for s in e['senses']), 'charge: board W per record at the end': charge(base), 'take: births with taken >= booked': sum(1 for e in evs if e[3] >= e[4]), 'census: integers per Node, max bits': [integers, bits], 'max transient bits': base.max_transient, 'credits': len(crs)}
    # the run back of the base run
    exact = 0
    for k in range(n):
        base.step_back(); exact += (state_hash() == hashes[n - 1 - k])
    result['run back exact'] = [exact, n]
    # the 48
    per = []; equal = exchanged = neither = 0; rot_equal = refl_equal = rot_exch = refl_exch = 0
    plain_sorted = sorted(evs, key=repr); plain_credits = sorted(crs)
    for m in signed_permutations():
        other, _h, _f = run(universe, world_image(world0, m, cube), n, orient)
        o_births = births(other); o_cr = sorted(credits(other))
        o_ev = sorted([(i, s_, kids) for i, s_, kids, taken, booked, levels, A in o_births], key=repr)
        same = (o_ev == mapped(evs, m, cube, False)) and (o_cr == mapped_credits(crs, m, cube, False)) and (takes(o_births) == takes(evs))
        swapped = (o_ev == mapped(evs, m, cube, True)) and (o_cr == mapped_credits(crs, m, cube, True))
        d = det(m.tolist())
        kind = 'equal' if same else ('exchanged' if swapped else 'neither')
        if same: equal += 1; rot_equal += (d == 1); refl_equal += (d == -1)
        elif swapped: exchanged += 1; rot_exch += (d == 1); refl_exch += (d == -1)
        else: neither += 1
        asy = asymmetries(other)
        per.append({'element': m.tolist(), 'det': d, 'records': kind, 'take integers equal (exchanged case)': takes(o_births) == takes(evs), 'births': len(o_ev), 'credits': len(o_cr), 'pseudoscalar_sum': asy['pseudoscalar_sum'], 'wu_brief_sum': asy['wu_brief_sum'], 'c_odd_sum': asy['c_odd_sum']})
    base_asy = result['base asymmetries']
    result['the 48'] = {'equal': equal, 'exchanged': exchanged, 'neither': neither, 'rotations equal': rot_equal, 'reflections equal': refl_equal, 'rotations exchanged': rot_exch, 'reflections exchanged': refl_exch,
                        'pseudoscalar sum: elements with the image sum = det x base': sum(1 for p in per if p['pseudoscalar_sum'] == p['det'] * base_asy['pseudoscalar_sum']),
                        'wu_brief sum: elements with the image sum = base': sum(1 for p in per if p['wu_brief_sum'] == base_asy['wu_brief_sum']),
                        'c_odd sum: elements with the image sum = base': sum(1 for p in per if p['c_odd_sum'] == base_asy['c_odd_sum'])}
    result['per element'] = per
    result['reach'] = reach(universe, world_image(world0, identity, cube), orient, n, cube)
    result['milliseconds'] = (time.monotonic_ns() - t0) // 1000000
    json.dump(result, open(out, 'w'), indent=1)
    print(json.dumps({k: v for k, v in result.items() if k != 'per element'}))
