"""Where a mirror of the toy's run breaks: the run from a seed and from its image under one signed permutation, compared interval by interval through the image (the even rows by value, the odd lines along a negated axis by sign, the planes by |z|^2 and by W), the first interval and the first quantity apart named.
Usage: python mirror_diag.py <world.json> <cube> <intervals> <sx,sy,sz> [perm as pi0,pi1,pi2]"""
import sys, os, copy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from lean_full import Lean, load_world

universe, world0 = load_world(sys.argv[1]); cube, n = int(sys.argv[2]), int(sys.argv[3])
signs = [int(x) for x in sys.argv[4].split(",")]
perm = [int(x) for x in sys.argv[5].split(",")] if len(sys.argv) > 5 else [0, 1, 2]
m = np.zeros((3, 3), dtype=int)
for a in range(3): m[perm[a], a] = signs[a]  # e_a -> s_a e_pi(a)
def image(node): return tuple(int(x) % cube for x in (m @ np.array(node, dtype=int)))
def world_image(mm):
    w = copy.deepcopy(world0); w['shape'] = [cube, cube, cube]
    for lay in w.get('seed', []):
        for key in ('at', 'centre'):
            if key in lay: lay[key] = [int(x) % cube for x in (mm @ np.array(lay[key], dtype=int))]
    return w

a = Lean(universe, world_image(np.eye(3, dtype=int))); b = Lean(universe, world_image(m))
nodes = list(np.ndindex(cube, cube, cube))

def compare():
    apart = []
    for name, la, lb in (('metric', a.row(10).lines[0], b.row(10).lines[0]), ('massless', a.row(2, gap=0).lines[0], b.row(2, gap=0).lines[0]), ('potential', a.row(4).lines[0], b.row(4).lines[0]), ('phase', a.walled().lines[0], b.walled().lines[0])):
        for at in nodes:
            if int(la.now[at]) != int(lb.now[image(at)]) or int(la.before[at]) != int(lb.before[image(at)]): apart.append((name, at, 'level')); break
            if int(la.rem[at]) != int(lb.rem[image(at)]): apart.append((name, at, 'rem', int(la.rem[at]), int(lb.rem[image(at)]))); break
    for ax in range(3):
        for name, rows, odd in (('metric axes', (a.row(10).lines[1:4], b.row(10).lines[1:4]), False), ('potential odd lines', (a.row(4).lines[1:4], b.row(4).lines[1:4]), True)):
            la, lb = rows[0][ax], rows[1][perm[ax]]; sg = signs[ax] if odd else 1
            for at in nodes:
                if int(la.now[at]) != sg * int(lb.now[image(at)]): apart.append((name, ax, at, 'level', int(la.now[at]), int(lb.now[image(at)]))); break
    det = int(round(np.linalg.det(m)))
    for rec in range(2 * a.nl):
        ra, ia = a.records()[rec].lines; rb, ib = b.records()[rec].lines
        for at in nodes:
            za = int(ra.now[at]) ** 2 + int(ia.now[at]) ** 2; zb = int(rb.now[image(at)]) ** 2 + int(ib.now[image(at)]) ** 2
            if za != zb: apart.append(('plane |z|^2', rec, at, za, zb)); break
            wa = int(ra.now[at]) * int(ia.before[at]) - int(ia.now[at]) * int(ra.before[at]); wb = int(rb.now[image(at)]) * int(ib.before[image(at)]) - int(ib.now[image(at)]) * int(rb.before[image(at)])
            if wa != det * wb and wa != wb: apart.append(('plane W', rec, at, wa, wb)); break
    return apart

for t in range(1, n + 1):
    a.step(); b.step()
    apart = compare()
    births_a = [(e['i'], tuple(e['node']), e['line_pair']) for e in a.log if e['event'] == 'birth' and e['i'] == t]
    births_b = [(e['i'], tuple(e['node']), e['line_pair']) for e in b.log if e['event'] == 'birth' and e['i'] == t]
    same_births = sorted((i, image(at), s_) for i, at, s_ in births_a) == sorted(births_b)
    if apart or not same_births:
        print({'first apart at interval': t, 'apart': apart[:4], 'births a': births_a[:4], 'births b': births_b[:4], 'turned a': int(a.turned.sum()), 'turned b': int(b.turned.sum())}); break
else:
    print({'intervals': n, 'apart': 'none', 'births': a.counts['births']})
