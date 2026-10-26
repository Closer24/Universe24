"""The 48 and the conjugation on the clicks of the lean toy, hand pa2 (ALGEBRA.md, The click's parity; The cube's symmetry; the owner's word of 2026-10-25: Wu's parity checked in the clicks).

For a world and an orientation mode, the toy runs from the seed and from each of its 48 images (the signed permutations about the origin); the whole record (the credit lines alone: the births with the two children's Nodes and the take, the bodies' credits with point, row, sense, beat, the take and the sign of the momentum vector read from the credit's frame) is compared through the image: equal, equal with the senses exchanged (every record's two senses swapped, the momentum negated: the conjugate record), or neither. The conjugation is tested by the same comparison with the identity image and the senses exchanged (the seed, light alone, is its own conjugate). The readings in the clicks: the charge (the senses' sum over the births and over the credits), the take (taken against booked on every birth and credit), Wu's correlation as the brief words it (the child's sense times the sign of its momentum along the Link from the - child to the + child, at its first credit), the per-axis sense x sign(p_a), and the twist of a child's momentum about its birth Link between two of its credits; the swap's effect on the senses at the turned Nodes; the state's integers and bits; the run back exact at the end of the base run (N intervals back, the state hashed).
Usage: python pa2_48.py <world.json> <cube> <intervals> <mode: current|twist|label> <out.json> [back N]
Integers only: every mean a pair [sum, count]."""
import sys, os, json, copy, itertools, hashlib, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, 'toy'))
import numpy as np
from lean_pa2 import LeanPa2, axis_of
from lean_full import Lean, load_world, AXES

sys.set_int_max_str_digits(0)


def signed_permutations():
    axes = range(3)
    return [np.array([[s[a] if pi[a] == b else 0 for a in axes] for b in axes]) for pi in itertools.permutations(axes) for s in itertools.product((1, -1), repeat=3)]


def image(m, node, cube):
    v = m @ np.array(node, dtype=int)
    return tuple(int(x) % cube for x in v)


def world_image(world, m, cube):
    w = copy.deepcopy(world); w['shape'] = [cube, cube, cube]
    for lay in w.get('seed', []):
        for key in ('at', 'centre'):
            if key in lay: lay[key] = list(image(m, tuple(lay[key]), cube))
    w['detectors'] = [list(image(m, tuple(d), cube)) for d in w.get('detectors', [])]
    return w


def momentum_of(credit):
    """The record's momentum vector at the credited Node from the credit line's frame alone: p_a = re0 (im(+a) f+ - im(-a) f-) - im0 (re(+a) - re(-a)), the start's levels, the neighbours' im read in the Node's frame (the toy's plane_current at one Node); a polar vector, negated for the conjugate record."""
    f = credit['frame']; re0, im0 = f['re_start_now'], f['im_start_now']
    ren, imn, fr = f['re_neighbours_start'], f['im_neighbours_start'], f['frames']
    p = []
    for a in range(3):
        dz_re = ren[2 * a] - ren[2 * a + 1]; dz_im = fr[2 * a] * imn[2 * a] - fr[2 * a + 1] * imn[2 * a + 1]
        p.append(re0 * dz_im - im0 * dz_re)
    return p


def sgn(x): return 1 if x > 0 else -1 if x < 0 else 0


def records(b, m, cube, conj):
    """The record through the image m, conjugated (the senses exchanged: the two records of a lift swapped, the sense negated, the momentum negated, the children's Nodes swapped) where conj."""
    births = []; credits = []
    for e in b.log:
        if e['event'] == 'birth':
            mi, pl = image(m, tuple(e['minus']), cube), image(m, tuple(e['plus']), cube)
            if conj: mi, pl = pl, mi
            births.append((e['i'], image(m, tuple(e['node']), cube), e['line_pair'], mi, pl, e['taken'], e['booked'], e['levels']))
        elif e['event'] == 'credit':
            rec = e['line']; sense = e['sense']; p = momentum_of(e)
            pm = [int(x) for x in (m @ np.array(p, dtype=object))]
            if conj: rec = rec ^ 1; sense = -sense; pm = [-x for x in pm]
            credits.append((e['i'], image(m, tuple(e['node']), cube), rec, sense, e['beat'], tuple(sgn(x) for x in pm)))
    # the credits' takes as a multiset per (interval, Node): where two records close at one Node in one interval the toy takes in the records' index order, a label that pairs the first take with the record's index and not with its sense; the multiset is the order-free reading
    takes = sorted((e['i'], image(m, tuple(e['node']), cube), e['taken'], e['levels']) for e in b.log if e['event'] == 'credit')
    return sorted(births), sorted(credits) + [('takes',)] + takes


def wu_readings(b, cube):
    """The readings in the clicks from the log alone (the credit lines): integers, every mean a pair [sum, count]."""
    births = [e for e in b.log if e['event'] == 'birth']; credits = [e for e in b.log if e['event'] == 'credit']
    out = {}
    out['charge: senses summed over births'] = sum(s for e in births for s in e['senses'])
    out['charge: W of the pair at the lay, summed'] = sum(e['W_pair'] for e in births)
    out['charge: senses summed over credits'] = sum(e['sense'] for e in credits)
    out['take: births with taken >= booked'] = [sum(1 for e in births if e['taken'] >= e['booked']), len(births)]
    out['take: credits with taken >= booked'] = [sum(1 for e in credits if e['taken'] >= b.units[e['line'] // 2]), len(credits)]
    out['orientation: + child downstream of the current'] = [sum(1 for e in births if e['plus_downstream'] == 1), len(births)]
    # Wu as the brief words it: the child's sense x sign(p . e), e the unit Link vector from the - child's Node to the + child's, p at the child's first credit after its birth (at its own Node, its own record)
    first = {}
    for e in credits:
        key = (e['line'], tuple(e['node']))
        first.setdefault(key, []).append(e)
    lit = [0, 0]; by_axis = [[0, 0] for _ in range(3)]; twist_axis = [0, 0]
    for e in births:
        mi, pl = tuple(e['minus']), tuple(e['plus']); a = axis_of(mi, pl, cube)
        step = (pl[a] - mi[a]) % cube; ea = 1 if step == 1 else -1  # e from - to +, along the axis a, the torus wrapped
        for sense, rec, where in ((-1, 2 * e['line_pair'], mi), (1, 2 * e['line_pair'] + 1, pl)):
            later = [c for c in first.get((rec, where), []) if c['i'] > e['i']]
            if not later: continue
            later.sort(key=lambda c: c['i'])
            p = momentum_of(later[0]); q = sense * sgn(p[a] * ea)
            if q != 0: lit[0] += q; lit[1] += 1
            if len(later) > 1:  # the twist of the child's momentum about the birth Link: e . (p1 x p2), a pseudoscalar; C-odd through e, p1, p2 all odd
                p1, p2 = p, momentum_of(later[1]); cross = [p1[1] * p2[2] - p1[2] * p2[1], p1[2] * p2[0] - p1[0] * p2[2], p1[0] * p2[1] - p1[1] * p2[0]]
                x = sgn(ea * cross[a])
                if x != 0: twist_axis[0] += x; twist_axis[1] += 1
    for c in credits:
        p = momentum_of(c)
        for a in range(3):
            q = c['sense'] * sgn(p[a])
            if q != 0: by_axis[a][0] += q; by_axis[a][1] += 1
    out['Wu (brief): sense x sign(p . e_minus_to_plus) at the first credit [sum, count]'] = lit
    out['sense x sign(p_a) over credits, per axis [sum, count]'] = by_axis
    out['twist of a child momentum about its birth Link, e . (p1 x p2) [sum, count]'] = twist_axis
    out['credits'] = len(credits); out['births'] = len(births)
    return out


def main():
    world_path, cube, n, mode, out_path = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5]
    back = int(sys.argv[sys.argv.index('back') + 1]) if 'back' in sys.argv else 0
    universe, world0 = load_world(world_path)
    identity = np.eye(3, dtype=int)
    t0 = time.monotonic_ns()
    base = LeanPa2(universe, world_image(world0, identity, cube), mode)
    hashes = []
    def state_hash(b): return hashlib.sha256(b.state_bytes() + str(b.interval).encode()).hexdigest()
    for t in range(n):
        if back and t >= n - back: hashes.append(state_hash(base))
        base.step()
    integers, bits = base.census()
    result = {'world': world_path, 'cube': cube, 'intervals': n, 'mode': mode, 'counts': {k: int(v) for k, v in base.counts.items()}, 'counts_twist': dict(base.counts_twist), 'sense_at_swap': dict(base.sense_at_swap), 'integers per Node': integers, 'max state bits': bits}
    result['readings in the clicks (base run)'] = wu_readings(base, cube)
    # David's path bit for bit: the mode 'current' against David's own class on the same world
    if mode == 'current':
        david = Lean(universe, world_image(world0, identity, cube))
        for _ in range(n): david.step()
        result['David path bit for bit (state hash equal)'] = state_hash(david) == state_hash(base)
    # the conjugation: the seed is light alone, its own conjugate; the run's record against its conjugate
    bb, cb = records(base, identity, cube, False); bc, cc = records(base, identity, cube, True)
    only = lambda rows: [x for x in rows if len(x) == 6]  # the credits' rows (the takes' rows follow the marker)
    result['conjugation'] = {'records equal to their conjugate': (bb == bc and cb == cc), 'births with the + child at the other end in the conjugate': sum(1 for x, y in zip(bb, bc) if x != y), 'of births': len(bb), 'credits with the sense exchanged in the conjugate': sum(1 for x, y in zip(only(cb), only(cc)) if x != y), 'of credits': len(only(cb))}
    # the 48
    equal = []; exchanged = []; neither = []
    for m in signed_permutations():
        other = LeanPa2(universe, world_image(world0, m, cube), mode)
        for _ in range(n): other.step()
        ob, oc = records(other, identity, cube, False)
        mb, mc = records(base, m, cube, False); xb, xc = records(base, m, cube, True)
        det = int(round(np.linalg.det(m)))
        tag = {'det': det, 'm': m.tolist(), 'births': len(ob), 'credits': len(oc)}
        if ob == mb and oc == mc: equal.append(tag)
        elif ob == xb and oc == xc: exchanged.append(tag)
        else:
            tag['births equal'] = ob == mb; tag['births exchanged'] = ob == xb; tag['credits equal'] = oc == mc; tag['credits exchanged'] = oc == xc
            tag['first birth apart'] = next(((a, b_) for a, b_ in zip(mb, ob) if a != b_), None)
            neither.append(tag)
    result['the 48'] = {'equal': len(equal), 'equal rotations': sum(1 for t in equal if t['det'] == 1), 'equal reflections': sum(1 for t in equal if t['det'] == -1), 'senses exchanged': len(exchanged), 'exchanged rotations': sum(1 for t in exchanged if t['det'] == 1), 'exchanged reflections': sum(1 for t in exchanged if t['det'] == -1), 'neither': len(neither), 'neither detail': neither[:6]}
    if back:
        exact = 0
        for k in range(back):
            base.step_back(); exact += (state_hash(base) == hashes[back - 1 - k])
        result['run back'] = {'intervals': back, 'exact': exact}
    result['seconds'] = (time.monotonic_ns() - t0) // 10 ** 9
    json.dump(result, open(out_path, 'w'), indent=1)
    print(json.dumps(result, indent=1))


if __name__ == '__main__':
    main()
