"""F6: the light as the Mesh's link, its kind and its gauge (draft F; root V items 20 and 22).

Exact integers and Fractions only, no float. Run: python3 -I F6_link.py [MUTANT]
MUTANT: none (default), current (the hands' centred lead as the link's source), curl (one sign of the
plaquette flipped), unit (a Gaussian integer of norm 2 admitted as a turn). Each mutant must make at
least one check FAIL.

 A. the six Spokes under the 24: 6 = A1 + E + T1; a gear on the Mesh, odd under the Mesh's reversal
    (A_(-j)(x + e_j) = -A_j(x)), is the T1 part: the link variable's kind is T1;
 B. the lattice's complex on the torus of side 3 and 4 (integer matrices): grad (Node-clocks to Meshes),
    curl (Meshes to plaquettes): curl grad = 0 exactly; rank grad = N - 1, rank curl = 2N - 2, so the
    3N link gears are N - 1 pure gauge (gradients of an A1 gauge function at the Node-clocks), 2N - 2
    transverse (two per wave number k != 0, the light's two polarizations) and 3 harmonic (the torus's
    three loops); and curl^T curl + grad grad^T = -LAPLACIAN on the Meshes, so on the transverse gears the
    one formula's own pull is Maxwell's;
 C. the 24 act on the link gears and commute with grad and with curl^T curl;
 D. Gauss's law kept: hands on the one formula, the link gears in the temporal gauge
    A+ = 2A - A- - (1/3) curl^T curl A + J with J the Mesh's flux of the sweep: div E - rho is the same at
    every Node-clock and tick, where E = -(A - A-) and rho the sweep;
 E. the only Gaussian integers of norm 1 are 1, i, -1, -i: a hand's exact turn across a Mesh by one
    Gaussian integer is a Z4 link (Creutz, Jacobs and Rebbi 1979: for Z_N with N <= 4 no Coulomb phase in
    four Euclidean dimensions).
"""

import itertools
import random
import sys
from fractions import Fraction as Fr

MUT = sys.argv[1] if len(sys.argv) > 1 else "none"
FAILS = []


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (" : " + detail if detail else ""))
    if not ok:
        FAILS.append(name)


# ---------------------------------------------------------------- A. the Spokes' kinds
def det3(m):
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


G24 = []
for p in itertools.permutations(range(3)):
    for sg in itertools.product((1, -1), repeat=3):
        m = [[0] * 3 for _ in range(3)]
        for i in range(3):
            m[p[i]][i] = sg[i]
        m = tuple(tuple(r) for r in m)
        if det3(m) == 1:
            G24.append(m)


def apply(g, v):
    return tuple(sum(g[i][j] * v[j] for j in range(3)) for i in range(3))


SPOKES = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]


def chi(kind, g):
    tr = g[0][0] + g[1][1] + g[2][2]
    perm = tuple(next(j for j in range(3) if g[j][i] != 0) for i in range(3))
    sgn = 1
    for i in range(3):
        for j in range(i + 1, 3):
            if perm[i] > perm[j]:
                sgn = -sgn
    fixed = sum(1 for i in range(3) if perm[i] == i)
    return {"A1": 1, "A2": sgn, "E": fixed - 1, "T1": tr, "T2": sgn * tr}[kind]


def mult(char):
    return {k: Fr(sum(char(g) * chi(k, g) for g in G24), 24) for k in ("A1", "A2", "E", "T1", "T2")}


perm6 = mult(lambda g: sum(1 for s in SPOKES if apply(g, s) == s))
odd3 = mult(lambda g: sum(g[a][a] for a in range(3)))  # e_a -> +-e_a on the odd combination A_(+a) - A_(-a)
even3 = mult(lambda g: sum(1 for a in range(3) if g[a][a] != 0))
check("A1 the six Spokes are A1 + E + T1", perm6 == {"A1": 1, "A2": 0, "E": 1, "T1": 1, "T2": 0}, str({k: int(v) for k, v in perm6.items()}))
check("A2 the Mesh's odd gear (reversed with the Mesh) is T1; the even part A1 + E",
      odd3 == {"A1": 0, "A2": 0, "E": 0, "T1": 1, "T2": 0} and even3 == {"A1": 1, "A2": 0, "E": 1, "T1": 0, "T2": 0})


# ---------------------------------------------------------------- B. the lattice's complex
def build(L):
    sites = list(itertools.product(range(L), repeat=3))
    ix = {x: i for i, x in enumerate(sites)}
    N = len(sites)
    E3 = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]

    def sh(x, a, k=1):
        return tuple((x[i] + k * E3[a][i]) % L for i in range(3))

    grad = [[0] * N for _ in range(3 * N)]
    for x in sites:
        for a in range(3):
            grad[3 * ix[x] + a][ix[sh(x, a)]] += 1
            grad[3 * ix[x] + a][ix[x]] -= 1
    curl = [[0] * (3 * N) for _ in range(3 * N)]
    flip = -1 if MUT == "curl" else 1
    for x in sites:
        for c in range(3):
            a, b = (c + 1) % 3, (c + 2) % 3
            row = 3 * ix[x] + c
            curl[row][3 * ix[sh(x, a)] + b] += 1
            curl[row][3 * ix[x] + b] -= 1
            curl[row][3 * ix[sh(x, b)] + a] -= flip
            curl[row][3 * ix[x] + a] += 1
    lap = [[0] * (3 * N) for _ in range(3 * N)]
    for x in sites:
        for a in range(3):
            r = 3 * ix[x] + a
            for b in range(3):
                lap[r][3 * ix[sh(x, b)] + a] += 1
                lap[r][3 * ix[sh(x, b, -1)] + a] += 1
                lap[r][r] -= 2
    return sites, ix, N, grad, curl, lap, sh


def matmul(A, B):
    Bt = list(zip(*B))
    return [[sum(a * b for a, b in zip(row, col) if a and b) for col in Bt] for row in A]


def transpose(A):
    return [list(r) for r in zip(*A)]


def rank(M):
    rows = [[Fr(v) for v in r] for r in M if any(r)]
    rk, ncol = 0, len(M[0])
    col = 0
    while rk < len(rows) and col < ncol:
        piv = next((i for i in range(rk, len(rows)) if rows[i][col] != 0), None)
        if piv is None:
            col += 1
            continue
        rows[rk], rows[piv] = rows[piv], rows[rk]
        pv = rows[rk][col]
        for i in range(rk + 1, len(rows)):
            if rows[i][col] != 0:
                f = rows[i][col] / pv
                rows[i] = [u - f * w for u, w in zip(rows[i], rows[rk])]
        rk += 1
        col += 1
    return rk


for L in (3, 4):
    sites, ix, N, grad, curl, lap, sh = build(L)
    cg = matmul(curl, grad)
    rg, rc = rank(grad), rank(curl)
    check(f"B1 [side {L}] curl grad = 0 exactly", all(v == 0 for r in cg for v in r))
    check(f"B2 [side {L}] rank grad = N - 1 = {N - 1}, rank curl = 2N - 2 = {2 * N - 2}: per wave number k != 0 one gauge and two transverse",
          rg == N - 1 and rc == 2 * N - 2, f"{rg} and {rc}")
    check(f"B3 [side {L}] the harmonic gears ker curl / im grad: 3N - rank curl - rank grad = 3 (the torus's three loops)",
          3 * N - rc - rg == 3)
    ctc = matmul(transpose(curl), curl)
    ggt = matmul(grad, transpose(grad))
    ident = all(ctc[i][j] + ggt[i][j] == -lap[i][j] for i in range(3 * N) for j in range(3 * N))
    check(f"B4 [side {L}] curl^T curl + grad grad^T = -LAPLACIAN on the Meshes (so on transverse gears Maxwell = the one formula's pull)", ident)

# ---------------------------------------------------------------- C. the 24 on the link gears
L = 3
sites, ix, N, grad, curl, lap, sh = build(L)
E3 = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]


def act_site(g, f):
    return {tuple(v % L for v in apply(g, x)): val for x, val in f.items()}


def act_link(g, A):
    out = {}
    for (x, a), val in A.items():
        y = tuple(v % L for v in apply(g, x))
        d = apply(g, E3[a])
        b = next(i for i in range(3) if d[i] != 0)
        if d[b] == 1:
            out[(y, b)] = val
        else:
            out[(tuple((y[i] - E3[b][i]) % L for i in range(3)), b)] = -val
    return out


def grad_f(lam):
    return {(x, a): lam[sh(x, a)] - lam[x] for x in sites for a in range(3)}


def vec_of(A):
    return [A[(x, a)] for x in sites for a in range(3)]


def link_of(v):
    return {(x, a): v[3 * ix[x] + a] for x in sites for a in range(3)}


ctc = matmul(transpose(curl), curl)


def ctc_f(A):
    v = vec_of(A)
    return link_of([sum(ctc[i][j] * v[j] for j in range(3 * N) if ctc[i][j]) for i in range(3 * N)])


rng = random.Random(9)
lam = {x: rng.randint(-9, 9) for x in sites}
A = {(x, a): rng.randint(-9, 9) for x in sites for a in range(3)}
ok_g = ok_m = True
for g in G24:
    ok_g = ok_g and grad_f(act_site(g, lam)) == act_link(g, grad_f(lam))
    ok_m = ok_m and ctc_f(act_link(g, A)) == act_link(g, ctc_f(A))
check("C1 the 24 commute with the gauge's gradient on the Meshes", ok_g)
check("C2 the 24 commute with the transverse operator curl^T curl: the link light keeps the 24", ok_m)

# ---------------------------------------------------------------- D. Gauss's law kept
L = 4
sites, ix, N, grad, curl, lap, sh = build(L)
ctc = matmul(transpose(curl), curl)


def im_cx(a, b):
    return a[0] * b[1] - a[1] * b[0]


def hand_step(now, before, mu):
    out = {}
    for x in sites:
        s0 = s1 = Fr(0)
        for a in range(3):
            for k in (1, -1):
                y = sh(x, a, k)
                s0 += now[y][0]
                s1 += now[y][1]
        out[x] = (mu * s0 - before[x][0], mu * s1 - before[x][1])
    return out


mu = Fr(1, 3)
zn = {x: (Fr(rng.randint(-9, 9)), Fr(rng.randint(-9, 9))) for x in sites}
zb = {x: (Fr(rng.randint(-9, 9)), Fr(rng.randint(-9, 9))) for x in sites}
An = {(x, a): Fr(rng.randint(-9, 9)) for x in sites for a in range(3)}
Ab = {(x, a): Fr(rng.randint(-9, 9)) for x in sites for a in range(3)}


def divergence(F):
    return {x: sum(F[(x, a)] - F[(sh(x, a, -1), a)] for a in range(3)) for x in sites}


def gauss(An, Ab, zn, zb):
    Ef = {k: -(An[k] - Ab[k]) for k in An}
    dv = divergence(Ef)
    return {x: dv[x] - im_cx(zb[x], zn[x]) for x in sites}


g0 = gauss(An, Ab, zn, zb)
same = True
for t in range(10):
    if MUT == "current":
        J = {(x, a): -mu * Fr(1, 2) * (im_cx(zn[x], zn[sh(x, a)]) - im_cx(zn[x], zn[sh(x, a, -1)])) for x in sites for a in range(3)}
    else:
        J = {(x, a): -mu * im_cx(zn[x], zn[sh(x, a)]) for x in sites for a in range(3)}  # the sweep's flux out of x on +a
    v = vec_of(An)
    cc = link_of([sum(ctc[i][j] * v[j] for j in range(3 * N) if ctc[i][j]) for i in range(3 * N)])
    Anext = {k: 2 * An[k] - Ab[k] - mu * cc[k] + J[k] for k in An}  # A+ = 2A - A- - mu curl^T curl A + J (Ampere: dE/dt = curl B - J)
    znext = hand_step(zn, zb, mu)
    Ab, An = An, Anext
    zb, zn = zn, znext
    same = same and gauss(An, Ab, zn, zb) == g0
check("D1 Gauss's law kept: div E - rho the same at every Node-clock over 10 ticks (the source the Mesh's flux of the sweep)", same)

# ---------------------------------------------------------------- E. the hand's exact turns
units = [(a, b) for a in range(-5, 6) for b in range(-5, 6) if a * a + b * b == 1]
if MUT == "unit":
    units.append((1, 1))
check("E1 the Gaussian integers of norm 1 are exactly 1, i, -1, -i: a hand's exact turn across a Mesh is a Z4 link",
      sorted(units) == sorted([(1, 0), (0, 1), (-1, 0), (0, -1)]), str(units))

print("RESULT:", "ALL PASS" if not FAILS else "FAILED " + ", ".join(FAILS))
