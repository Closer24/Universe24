"""BC verifier, part 4: which two-twin states can an equivariant fitting lay from an A1 source?
A two-twin state is a 2x2 Gaussian tensor Psi (Psi[i][j] the amplitude of e_i (x) e_j); an element M of the 24's
double cover acts as Psi -> M Psi M^T.  An A1 (invariant) source can only feed the states with M Psi M^T = det(M) Psi
for every M (Schur).  Exhaustive over entries in [-2, 2] + i[-2, 2]: (a) under the 8 half turns (+-1, +-i, +-j, +-k,
exact on the twins' gears), (b) under all 48.  Run: python3 -I -B v4_kind.py
"""
import importlib.util, os
from itertools import product
here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("v1", os.path.join(here, "v1_algebra.py"))
v1 = importlib.util.module_from_spec(spec); spec.loader.exec_module(v1)
gm, ga, gs = v1.gm, v1.ga, v1.gs

def qmat(a, b, c, d): return [[(a, b), (c, d)], [(-c, d), (a, -b)]]
def mul(A, B): return [[ga(gm(A[i][0], B[0][j]), gm(A[i][1], B[1][j])) for j in range(2)] for i in range(2)]
def tr(A): return [[A[0][0], A[1][0]], [A[0][1], A[1][1]]]
def mdet(M): return gs(gm(M[0][0], M[1][1]), gm(M[0][1], M[1][0]))
def scal(k, A): return [[gm(k, A[i][j]) for j in range(2)] for i in range(2)]

half = [qmat(*v) for v in ([1, 0, 0, 0], [-1, 0, 0, 0], [0, 1, 0, 0], [0, -1, 0, 0], [0, 0, 1, 0], [0, 0, -1, 0], [0, 0, 0, 1], [0, 0, 0, -1])]
units = []
for i in range(4):
    for s_ in (1, -1):
        v = [0] * 4; v[i] = s_; units.append(v)
for sg in product((1, -1), repeat=4):
    units.append(list(sg))
for i in range(4):
    for j in range(i + 1, 4):
        for s1 in (1, -1):
            for s2 in (1, -1):
                v = [0] * 4; v[i] = s1; v[j] = s2; units.append(v)
all48 = [qmat(*v) for v in units]

vals = [(x, y) for x in range(-2, 3) for y in range(-2, 3)]
for name, G in (("8 half turns", half), ("all 48", all48)):
    inv = []
    for e in product(vals, repeat=4):
        P = [[e[0], e[1]], [e[2], e[3]]]
        if all(x == (0, 0) for x in e):
            continue
        if all(mul(mul(M, P), tr(M)) == scal(mdet(M), P) for M in G):
            inv.append(P)
    eps_like = all(P[0][0] == (0, 0) and P[1][1] == (0, 0) and P[0][1] == (-P[1][0][0], -P[1][0][1]) for P in inv)
    print(f"{name}: {len(inv)} invariant states of {len(vals) ** 4 - 1}; every one a multiple of eps: {eps_like}")
