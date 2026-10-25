"""sr1: the one-Node tests of the spinor row as runnable checks (python sr1_onenode.py), on the flagged copy, integers (exact fractions named).

T1 the pair's beat kept: the row (spin up along z) and a plane of the same pair laid alike (width 2, N quanta, one sense) on a
   3-cube, one interval: the invariant ratio cos omega = N.G.B / N.G.N of the row at the centre against the plane's
   (re re' + im im') / (re^2 + im^2), for the three Port turns none / half / quarter; the pair's num / den beside.
T3 the 2 pi turn: the lay with the spin vector v and with -v (the 2 pi turn's -I on the lines): the share, W and s equal, the
   credits over 30 intervals equal line for line.
T6 the 48 on the lines: one interval under the held curl with the Pauli term, the lay carried by each of the 48 lifts M(g)
   (the field as a polar vector): M(g) x_stepped(x) against x_stepped(g x) at every Node and line: the count equal, the
   largest difference (the roundings of the carried division, which the 8 x 8 mixing does not commute with).
"""
from __future__ import annotations
import sys, os, json, itertools
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
from lean_sr1 import Lean, SR1, gform8, matvec8
from sr1_measure import world, held, run, UNI, ROW8, signed_perms
sys.set_int_max_str_digits(0)
OUT = os.path.join(HERE, 'out')
NUM, DEN, GAMMA = 506298091, 1655909141, 1000


def t1(cube=3, N=20):
    c = cube // 2; cen = (c,) * 3; table = {'cos omega_0 = num / den (milli)': NUM * 1000 // DEN}
    for turn in ('none', 'half', 'quarter'):
        b = Lean(UNI, world(cube, 1, [{'lay': 'at', 'row': ROW8, 'centre': list(cen), 'width': 2, 'quanta': N, 'sense': 1, 'spin': 'spin_up_z'}], {'spinor_turn': turn, 'pauli': False}))
        rec = b.records().index(b.by_index[ROW8]); G = SR1['G']
        def ratio():
            ls = b.records()[rec].lines; Nn = [l.now for l in ls]; B = [l.before for l in ls]; nn = int(gform8(G, Nn, Nn)[cen]); nb = int(gform8(G, Nn, B)[cen])
            return str(Fr(nb, nn)) if nn else None, (nb * 1000 // nn) if nn else None
        at_lay = ratio(); b.step(); after1 = ratio(); b.step(); after2 = ratio()
        table['row, turn ' + turn] = {'cos omega at the lay (fraction, milli)': at_lay, 'after 1 interval': after1, 'after 2': after2}
    b = Lean(UNI, world(cube, 1, [{'lay': 'at', 'row': 2, 'centre': list(cen), 'width': 2, 'quanta': N, 'sense': 1}], {}))
    def pratio():
        re, im = b.records()[b.records().index(b.by_index[2])].lines
        nn = int((re.now * re.now + im.now * im.now)[cen]); nb = int((re.now * re.before + im.now * im.before)[cen])
        return str(Fr(nb, nn)) if nn else None, (nb * 1000 // nn) if nn else None
    p0 = pratio(); b.step(); p1 = pratio(); b.step(); p2 = pratio()
    table['plane of the same pair'] = {'at the lay': p0, 'after 1': p1, 'after 2': p2}
    print(json.dumps({'T1': table})); return table


def t3(cube=5, intervals=30, N=60):
    c = cube // 2; cen = (c,) * 3; v = SR1['spin_up_z'][0]; found = {}
    for name, spin in (('v', v), ('-v (the 2 pi turn)', [-x for x in v])):
        w = world(cube, intervals, [{'lay': 'at', 'row': ROW8, 'centre': list(cen), 'width': 3, 'quanta': N, 'sense': 1, 'spin': spin}], {'pauli': True})
        b = Lean(UNI, w); rec = b.records().index(b.by_index[ROW8]); r = b.rule(b.records()[rec].pair, b.content(), b.link_factors()); b.start_content = b.content()
        sh = b.share8(b.records()[rec].lines, r, vacuum=True); W, s, sw = b.bilinears8(b.records()[rec].lines)
        o, _ = run(w, 5, cen, ROW8, complement=(name != 'v'))
        found[name] = {'share total': int(sum(int(x) for x in sh.reshape(-1))), 'W total': int(sum(int(x) for x in W.reshape(-1))), 's total': [int(sum(int(x) for x in sa.reshape(-1))) for sa in s], 'lines at the centre at the lay': [int(l.now[cen]) for l in b.records()[rec].lines],
                       'credits': sorted((e['i'], tuple(e['node']), e['line'], e['sense'], tuple(e.get('spin_sign', [0, 0, 0]))) for e in o['credits']), 'run_back': o['run_back']}
    eq = found['v']['credits'] == found['-v (the 2 pi turn)']['credits']
    out = {'share equal': found['v']['share total'] == found['-v (the 2 pi turn)']['share total'], 'W equal': found['v']['W total'] == found['-v (the 2 pi turn)']['W total'], 's equal': found['v']['s total'] == found['-v (the 2 pi turn)']['s total'],
           'lines negated': found['v']['lines at the centre at the lay'] == [-x for x in found['-v (the 2 pi turn)']['lines at the centre at the lay']], 'credits': len(found['v']['credits']), 'credits equal line for line': eq, 'run_back': [found['v']['run_back'], found['-v (the 2 pi turn)']['run_back']]}
    print(json.dumps({'T3': out})); return out


def t6(cube=5, N=60, B0=200, bgrad=100):
    c = cube // 2; cen = (c,) * 3; spin0 = [1, -1, 0, 0, 2, 0, 0, 0]
    perm_of = SR1['perm48']
    def R_of(p):
        R = np.zeros((3, 3), dtype=int)
        for a, (bb, s) in p.items(): R['xyz'.index(bb)]['xyz'.index(a)] = s
        return R
    lifts = {}
    for key, p in perm_of.items(): lifts.setdefault(json.dumps(R_of(p).tolist()), []).append(key)
    def stepped(spin, ctrl):
        b = Lean(UNI, world(cube, 1, [{'lay': 'at', 'row': ROW8, 'centre': list(cen), 'width': 3, 'quanta': N, 'spin': spin}], ctrl)); b.step()
        rec = b.records().index(b.by_index[ROW8]); return [l.now for l in b.records()[rec].lines], b
    base_ctrl = held(1, cen, B0, bgrad, 1, 2); base_ctrl['pauli'] = True; base_ctrl['spinor_turn'] = 'none'
    base, b0 = stepped(spin0, base_ctrl)
    exact = 0; worst = 0; per = []
    for g in signed_perms():
        det = int(round(np.linalg.det(g))); grot = g * det
        for key in lifts[json.dumps(grot.tolist())]:
            M = SR1['M48'][key]; spin_g = [sum(M[r][k] * spin0[k] for k in range(8)) for r in range(8)]
            la, ac, al = [int(np.nonzero(g[:, k])[0][0]) for k in range(3)]
            ctrl = {'held_potential': [{'line': 1 + la, 'at': list(cen), 'field': 'sg_image', 'across': ac, 'along': al, 'B0': B0, 'b': bgrad, 's_line': int(g[la, 0]), 's_across': int(g[ac, 1]), 's_along': int(g[al, 2])}], 'pauli': True, 'spinor_turn': 'none'}
            other, _ = stepped(spin_g, ctrl)
            # M(g) applied to the base's stepped lines, carried to the image Node
            Mbase = matvec8(M, base); diff_max = 0; unequal = 0
            for node in np.ndindex(*b0.shape):
                gx = tuple(int(x) % cube for x in (g @ (np.array(node, dtype=int) - np.array(cen)) + np.array(cen)))
                for k in range(8):
                    d = abs(int(other[k][gx]) - int(Mbase[k][node])); diff_max = max(diff_max, d); unequal += (d != 0)
            exact += (unequal == 0); worst = max(worst, diff_max); per.append({'g': g.tolist(), 'det': det, 'lift': key, 'unequal node-lines': unequal, 'max diff': diff_max})
    total = len(per)
    out = {'lifts tested (48 g x 2 lifts of the rotation part, both signs)': total, 'exact bit for bit': exact, 'largest level difference (the roundings mixed by M)': worst, 'node-lines compared per lift': cube ** 3 * 8, 'examples': per[:6]}
    json.dump(per, open(os.path.join(OUT, 'onenode_48_lines.json'), 'w'))
    print(json.dumps({'T6': out})); return out


if __name__ == '__main__':
    found = {'T1': t1(), 'T3': t3(), 'T6': t6()}
    json.dump(found, open(os.path.join(OUT, 'onenode.json'), 'w'), indent=1)
