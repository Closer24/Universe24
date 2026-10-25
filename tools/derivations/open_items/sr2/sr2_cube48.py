"""sr2: the 48 on the spinor row's clicks and levels (integers; the 48 lifts as exact rationals in the plane basis).

The base world (cube48_base.json): a spinor packet spin-up along x of 40 quanta, width 2, laid at a fixed amplitude
(a multiple of 8, so that the lay's floors are exact and every image lay is exactly M(g) times the base's levels),
in the held gradient field; 20 intervals. For each of the 48 elements of the double cover (the lifts of the 24
rotations, two per rotation, g and -g) and for the 48 Pin lifts of the reflections (Gamma_a times the rotations'
lifts, g and -g: 96 in all over the 48 signed permutations, each twice): the image world is the signed permutation
applied to the lay's centre and to the field's lines (a vector: the line, the axes across and along, the signs into
B0 and b), the spin state M(g) chi (times 2 where M(g) has halves, with the amplitude halved: the same levels), run
20 intervals; compared: (a) the clicks: the credits (interval, Node, record, sense, the component signs along the
three axes carried as an axial vector, det(g) times the signed permutation) and the births, through the image; (b) the
spinor row's levels at the end through M(g) (now and before, every Node), the count of Node-lines off and the largest
departure. Expected by derivation: the clicks 48 of 48 (rotations) and 48 of 48 (reflections, the Pin lift); the
levels exact for the 16 monomial lifts (the binary dihedral group of the z axis in the plane basis) and kept to the
floors for the 32 others (sr2_algebra.py (3), (7): no basis of lines carries all 48 as signed permutations).
Usage: python sr2_cube48.py <worlds/cube48_base.json> <out.json> [intervals]
"""
import sys, os, json, copy, itertools
from fractions import Fraction as Fr
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from lean_sr2 import Lean, load_world

# ---- Q(zeta) and the 48 lifts as 8 x 8 rationals in the plane basis (as sr2_algebra.py)
def zmul(a, b):
    c = [Fr(0)] * 8
    for i in range(4):
        for j in range(4): c[i + j] += a[i] * b[j]
    for k in range(7, 3, -1): c[k - 4] -= c[k]; c[k] = Fr(0)
    return tuple(c[:4])
def zadd(a, b): return tuple(x + y for x, y in zip(a, b))
def zneg(a): return tuple(-x for x in a)
ZERO, ONE = (Fr(0),) * 4, (Fr(1), Fr(0), Fr(0), Fr(0)); I_ = (Fr(0), Fr(0), Fr(1), Fr(0)); INV_SQRT2 = (Fr(0), Fr(1, 2), Fr(0), Fr(-1, 2))
def mmul(A, B):
    return (zadd(zmul(A[0], B[0]), zmul(A[1], B[2])), zadd(zmul(A[0], B[1]), zmul(A[1], B[3])), zadd(zmul(A[2], B[0]), zmul(A[3], B[2])), zadd(zmul(A[2], B[1]), zmul(A[3], B[3])))
IDENT = (ONE, ZERO, ZERO, ONE); SX = (ZERO, ONE, ONE, ZERO); SY = (ZERO, zneg(I_), I_, ZERO); SZ = (ONE, ZERO, ZERO, zneg(ONE))
def lift(S): return tuple(zmul(INV_SQRT2, zadd(e, zmul(I_, s))) for e, s in zip(IDENT, S))
def closure(gens):
    seen = {IDENT: ''}; frontier = [IDENT]
    while frontier:
        nxt = []
        for A in frontier:
            for name, G in gens:
                B = mmul(G, A)
                if B not in seen: seen[B] = name + seen[A]; nxt.append(B)
        frontier = nxt
    return seen
def lines_of(v): return [v[0][0], v[0][2], v[0][1], v[0][3], v[1][0], v[1][2], v[1][1], v[1][3]]
def vec_of(l): return ((l[0], l[2], l[1], l[3]), (l[4], l[6], l[5], l[7]))
def apply(A, v): return (zadd(zmul(A[0], v[0]), zmul(A[1], v[1])), zadd(zmul(A[2], v[0]), zmul(A[3], v[1])))
def real8(A):
    cols = []
    for c in range(8):
        e = [Fr(0)] * 8; e[c] = Fr(1); cols.append(lines_of(apply(A, vec_of(e))))
    return [[cols[c][r] for c in range(8)] for r in range(8)]
def mm(A, B): return [[sum(A[r][k] * B[k][c] for k in range(8)) for c in range(8)] for r in range(8)]
def mT(A): return [[A[c][r] for c in range(8)] for r in range(8)]
def mv(A, v): return [sum(A[r][c] * v[c] for c in range(8)) for r in range(8)]
def msc(s, A): return [[s * x for x in row] for row in A]
def monomial(M): return all(sum(1 for x in row if x != 0) == 1 for row in M) and all(abs(x) in (0, 1) for row in M for x in row)
GROUP = closure([('x', lift(SX)), ('y', lift(SY)), ('z', lift(SZ))])
SIG = {0: real8(SX), 1: real8(SY), 2: real8(SZ)}
def perm_of(M):
    """The signed permutation of the axes the lift carries: sigma_a -> s sigma_b, as a 3 x 3 integer matrix P with P[b][a] = s."""
    P = [[0] * 3 for _ in range(3)]; Minv = mT(M)
    for a in range(3):
        conj = mm(mm(M, SIG[a]), Minv)
        for b_ in range(3):
            if conj == SIG[b_]: P[b_][a] = 1
            elif conj == msc(-1, SIG[b_]): P[b_][a] = -1
    return P


def image_node(P, node, cube, centre):
    """A Node carried by the signed permutation about the board's centre Node (the lay's centre), the torus wrapped."""
    d = [node[a] - centre[a] for a in range(3)]
    v = [sum(P[b_][a] * d[a] for a in range(3)) for b_ in range(3)]
    return tuple((centre[b_] + v[b_]) % cube for b_ in range(3))


def image_axis(P, a):
    b_ = next(k for k in range(3) if P[k][a] != 0); return b_, P[b_][a]


def image_world(world, P, M, cube):
    w = copy.deepcopy(world); centre = tuple(int(x) for x in [s for s in w['seed'] if s.get('lay') == 'at'][0]['centre'])
    for lay in w['seed']:
        if lay.get('lay') == 'at':
            lay['centre'] = list(image_node(P, tuple(lay['centre']), cube, centre))
            if 'spin' in lay:
                chi = mv(M, [Fr(x) for x in lay['spin']])
                if all(x.denominator == 1 for x in chi): lay['spin'] = [int(x) for x in chi]
                else:
                    lay['spin'] = [int(2 * x) for x in chi]; lay['amplitude'] = int(lay['amplitude']) // 2  # the same levels: A (M chi) = (A / 2)(2 M chi)
    for h_ in w.get('control', {}).get('held_potential', []):
        h_['at'] = list(image_node(P, tuple(h_['at']), cube, centre))
        line, s_line = image_axis(P, int(h_['line']) - 1); across, s_across = image_axis(P, int(h_['across'])); along, s_along = image_axis(P, int(h_['along']))
        h_['line'] = line + 1; h_['across'] = across; h_['along'] = along
        h_['B0'] = s_line * s_across * int(h_['B0']); h_['b'] = s_line * s_across * s_along * int(h_['b'])  # F'(g x) on the line g(line) = s_line F(x): -(s_across d')(B0 + b s_along d') times s_line
    return w


def run(universe, world, n, image=None):
    """The world run n intervals; with `image` = (base board, P, M, centre) the spinor row's state is the exact image of the base's: lines(g x) = M lines(x), now and before, laid directly (the loader's own rounding of a signed weight is not odd, so the lay's image is built from the base's levels and not re-laid); None where the image is no integer state."""
    if image is None:
        b = Lean(universe, world)
    else:
        base, P, M, centre = image
        w = copy.deepcopy(world); w['seed'] = [s for s in w['seed'] if s.get('lay') != 'at']
        b = Lean(universe, w); spin_rec = next(k for k, r in enumerate(base.records()) if r.shape == 8)
        lines_b = base.records()[spin_rec].lines; lines_o = b.records()[spin_rec].lines
        for at in np.ndindex(*base.shape):
            gx = image_node(P, at, b.cube, centre)
            for slot in ('now', 'before'):
                v = mv(M, [Fr(int(getattr(l, slot)[at])) for l in lines_b])
                if any(x.denominator != 1 for x in v): return None
                for l_, x in zip(lines_o, v): getattr(l_, slot)[gx] = int(x)
    for _ in range(n): b.step()
    return b


def clicks(b, P, det, cube, centre, M=None):
    """The credits and births as tuples through the image: (interval, Node, record, sense, the component signs as an axial vector) and (interval, take Node, lift, - Node, + Node)."""
    out = []
    for e in b.log:
        if e['event'] == 'credit':
            s = e['spin']['s_D'] if 'spin' in e else None
            if s is not None:
                sg = [0 if x == 0 else (1 if x > 0 else -1) for x in s]
                s_img = [det * sum(P[b_][a] * sg[a] for a in range(3)) for b_ in range(3)]
            else: s_img = None
            out.append(('credit', e['i'], image_node(P, tuple(e['node']), cube, centre), e['line'], e['sense'], tuple(s_img) if s_img else None))
        elif e['event'] == 'birth':
            out.append(('birth', e['i'], image_node(P, tuple(e['node']), cube, centre), e['line_pair'], image_node(P, tuple(e['minus']), cube, centre), image_node(P, tuple(e['plus']), cube, centre)))
    return sorted(out, key=str)


def main():
    sys.set_int_max_str_digits(0)
    universe, world0 = load_world(sys.argv[1]); out_path = sys.argv[2]; n = int(sys.argv[3]) if len(sys.argv) > 3 else int(world0['intervals'])
    cube = int(world0['shape'][0]); centre = tuple(int(x) for x in [s for s in world0['seed'] if s.get('lay') == 'at'][0]['centre'])
    ID3 = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    lay0 = [s for s in world0['seed'] if s.get('lay') == 'at'][0]
    if 'amplitude' not in lay0:  # the base's lay at the amplitude the search gives, rounded down to a multiple of 8: the lay's floors exact (the envelope's weights 8, 4, 2, 1 at width 2), so every image lay is exactly M(g) times the base's levels
        probe = Lean(universe, world0); A0 = [e['amplitude'] for e in probe.log if e['event'] == 'lay'][0]
        w0 = {2: 8, 3: 64}[int(lay0.get('width', 2))]; lay0['amplitude'] = (A0 // w0) * w0; print(json.dumps({'base amplitude from the search': A0, 'laid at': lay0['amplitude']}), flush=True)
    base0 = Lean(universe, world0)  # the base at the lay, the images' source
    base = run(universe, world0, n); spin_rec = next(k for k, r in enumerate(base.records()) if r.shape == 8)
    base_clicks = clicks(base, ID3, 1, cube, centre)
    print(json.dumps({'base': {'credits': sum(1 for c in base_clicks if c[0] == 'credit'), 'births': sum(1 for c in base_clicks if c[0] == 'birth'), 'turns': base.counts['turns'], 'amplitude': [e['amplitude'] for e in base.log if e['event'] == 'lay']}}), flush=True)
    results = {'rotations': [], 'reflections': []}
    elements = [(GROUP[A], real8(A)) for A in GROUP]
    for kind, lifts in (('rotations', [(w, M) for w, M in elements]), ('reflections', [('G2.' + w, mm(SIG[2], M)) for w, M in elements])):
        for word, M in lifts:
            P = perm_of(M); det = round(np.linalg.det(np.array(P, dtype=float)))  # +1 a rotation, -1 a reflection (the integer determinant of a signed permutation)
            det = 1 if det > 0 else -1
            other = run(universe, image_world(world0, P, M, cube), n, image=(base0, P, M, centre))
            if other is None:
                results[kind].append({'word': word, 'det': det, 'perm': P, 'monomial': monomial(M), 'clicks equal through the image': None, 'node-lines off': None, 'largest departure (x2 to an integer)': None, 'no integer image of the lay': True}); print(json.dumps(results[kind][-1]), flush=True); continue
            same_clicks = clicks(other, ID3, 1, cube, centre) == [(c[0], c[1], c[2], c[3], c[4], c[5]) for c in clicks(base, P, det, cube, centre)]
            # the levels through M(g): other's spinor lines at g x against M times base's at x, now and before
            off = 0; worst = 0
            lines_b = base.records()[spin_rec].lines; lines_o = other.records()[spin_rec].lines
            Mi = [[int(x) if x.denominator == 1 else None for x in row] for row in M]
            for at in np.ndindex(*base.shape):
                gx = image_node(P, at, cube, centre)
                for slot in ('now', 'before'):
                    vb = [Fr(int(getattr(l, slot)[at])) for l in lines_b]
                    expected = mv(M, vb)
                    for l_, e_ in zip(lines_o, expected):
                        got = Fr(int(getattr(l_, slot)[gx]))
                        if got != e_: off += 1; worst = max(worst, abs(got - e_))
            results[kind].append({'word': word, 'det': det, 'perm': P, 'monomial': monomial(M), 'clicks equal through the image': same_clicks, 'node-lines off': off, 'largest departure (x2 to an integer)': int(2 * worst)})
            print(json.dumps(results[kind][-1]), flush=True)
    summary = {}
    for kind in results:
        rs = results[kind]
        done = [r for r in rs if r['node-lines off'] is not None]
        summary[kind] = {'elements': len(rs), 'with an integer image of the lay': len(done), 'clicks equal': sum(1 for r in done if r['clicks equal through the image']), 'levels exact': sum(1 for r in done if r['node-lines off'] == 0), 'monomial lifts': sum(1 for r in rs if r['monomial']), 'monomial and exact': sum(1 for r in done if r['monomial'] and r['node-lines off'] == 0), 'monomial and clicks equal': sum(1 for r in done if r['monomial'] and r['clicks equal through the image']),
                         'non-monomial with an image: clicks equal': sum(1 for r in done if not r['monomial'] and r['clicks equal through the image']), 'largest departure over the non-monomial (x2)': max([r['largest departure (x2 to an integer)'] for r in done if not r['monomial']] + [0]), 'node-lines off, max': max([r['node-lines off'] for r in done] + [0]), 'node-lines compared': 2 * 8 * cube ** 3}
    json.dump({'summary': summary, 'results': results}, open(out_path, 'w'), indent=1)
    print(json.dumps(summary))


if __name__ == '__main__':
    main()
