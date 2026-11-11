"""ONE MATTER CONTENT, option (A) (manager ruling 10:5x; INTEGRATOR): ONE multiplet, ONE unified link algebra.

TENSOR BLOCKS ONLY. Matter = colour triplet (x) B1-EM Dirac pair: three copies q0, q1, q2 of layers.matter.build_matter
(imported read-only; 16 channels each, 48 per node). The complex structure is the Dirac carrier J8 on the 8-block; the
pair index (X, Y) carries C^2 with the matrix units E_00 = diag(1,0), E_01 = [[0,1],[0,0]], ... as REAL matrices, so
colour (x) pair = C^6. Link algebra: M6(C) (72 integers per positive face link, stored at the base node):
    rho(E_kl) = E_kl (x) 1_8,  rho(i E_kl) = E_kl (x) J8      on (6-index k = 2 c + s) (x) (8-block)
Potential (deviation form U = A*1 + W; the vacuum part A*N_d is the matter blocks' own hopping):
    Phi_c = sum_x sum_d Psi(x)^T rho(W(x,d)) (1_6 (x) N_d) Psi(x + e_d),   N_d = kd P_d^T - kw W0   (rank 3)
    Phi_U = (D/2) |U|^2 (zero mode)  -  (lam/4) (|U|^2 - 6 A^2)^2  (optional Frobenius OD4 spring, rank 4)
Exact local U(6) covariance: Psi(x) -> rho(g(x)) Psi(x), U(x,d) -> g(x) U g(x+e_d)^dag (rho is an algebra
homomorphism and commutes with 1 (x) N_d because J8 commutes with P_d and W0). U(6) CONTAINS SU(3)_colour (x) 1_2,
1_3 (x) SU(2)_pair (EM = J' = 1_3 (x) eps (x) 1_8 = 1_3 (x) i sigma_y: Georgi-Glashow), and U(1) (i 1_6 = the carrier
number, C-even); it is LARGER than SU(3) x SU(2) x U(1) (36 generators: colour-isospin "leptoquark" ones too). How
it breaks to the standard group is an OPEN design question (not decided here).
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from ..core.tensor import Block, GearType
from .gauge import UNIT, Algebra, Poly, deviation_terms
AXES = ('x', 'y', 'z')
N6 = 6

def mn_index(k: int, l: int, p: int, n: int=N6) -> int:
    return 2 * (n * k + l) + p

def _j8():
    from .matter import J8
    return [[int(v) for v in row] for row in J8]

def _signed_perm_apply(M):
    """For a signed permutation matrix M: list of (row i, sign) per column j."""
    out = []
    n = len(M)
    for j in range(n):
        (i, s), = [(i, M[i][j]) for i in range(n) if M[i][j]]
        out.append((i, s))
    return out

def algebra_u6() -> Algebra:
    """M6(C) acting on the 48 matter channels ch = 8 k + j (k = 2 c + s, j = 8-block channel)."""
    n = N6
    mul, act = ({}, {})
    J8cols = _signed_perm_apply(_j8())
    for k in range(n):
        for l in range(n):
            for m in range(n):
                for p in range(2):
                    for q in range(2):
                        s = -1 if p and q else 1
                        mul[mn_index(k, l, p), mn_index(l, m, q)] = (mn_index(k, m, (p + q) % 2), s)
            for p in range(2):
                for j in range(8):
                    i, s = (j, 1) if p == 0 else J8cols[j]
                    act[mn_index(k, l, p), 8 * l + j] = (8 * k + i, s)
    adj = [None] * (2 * n * n)
    for k in range(n):
        for l in range(n):
            for p in range(2):
                adj[mn_index(k, l, p)] = (mn_index(l, k, p), -1 if p else 1)
    one = [0] * (2 * n * n)
    for k in range(n):
        one[mn_index(k, k, 0)] = 1

    def el(entries):
        v = [0] * (2 * n * n)
        for (k, l, p), val in entries.items():
            v[mn_index(k, l, p)] = v[mn_index(k, l, p)] + val
        return tuple(v)

    def colour(entries3):
        e = {}
        for (a, b, p), val in entries3.items():
            for s in range(2):
                e[2 * a + s, 2 * b + s, p] = e.get((2 * a + s, 2 * b + s, p), 0) + val
        return el(e)

    def pair(entries2):
        e = {}
        for (s, t, p), val in entries2.items():
            for c in range(3):
                e[2 * c + s, 2 * c + t, p] = e.get((2 * c + s, 2 * c + t, p), 0) + val
        return el(e)
    gens = (('c_ilam1', colour({(0, 1, 1): 1, (1, 0, 1): 1})), ('c_ilam2', colour({(0, 1, 0): 1, (1, 0, 0): -1})), ('c_ilam3', colour({(0, 0, 1): 1, (1, 1, 1): -1})), ('c_ilam4', colour({(0, 2, 1): 1, (2, 0, 1): 1})), ('c_ilam5', colour({(0, 2, 0): 1, (2, 0, 0): -1})), ('c_ilam6', colour({(1, 2, 1): 1, (2, 1, 1): 1})), ('c_ilam7', colour({(1, 2, 0): 1, (2, 1, 0): -1})), ('c_ilam8x', colour({(0, 0, 1): 1, (1, 1, 1): 1, (2, 2, 1): -2})), ('w_isx', pair({(0, 1, 1): 1, (1, 0, 1): 1})), ('w_isy_EM_Jprime', pair({(0, 1, 0): 1, (1, 0, 0): -1})), ('w_isz', pair({(0, 0, 1): 1, (1, 1, 1): -1})), ('u1_i1', el({(k, k, 1): 1 for k in range(n)})), ('lq_mix_a', el({(0, 3, 1): 1, (3, 0, 1): 1})), ('lq_mix_b', el({(1, 4, 0): 1, (4, 1, 0): -1})))
    comp = tuple((f"{k}{l}{'ri'[p]}" for k in range(n) for l in range(n) for p in range(2)))
    mcomp = tuple((f"c{k // 2}{'XY'[k % 2]}{j}" for k in range(n) for j in range(8)))
    return Algebra('M6C', 2 * n * n, 8 * n, mul, act, tuple(adj), tuple(one), gens, (), comp, mcomp)

def matter_gears(names=('q0', 'q1', 'q2')) -> list[str]:
    """Qualified matter gear names in channel order ch = 8 k + j, k = 2 c + s (s = 0: X block, 1: Y block)."""
    from .matter import matter_names
    loc = matter_names('pair')
    out = []
    for c in range(3):
        for s in range(2):
            for j in range(8):
                out.append(f'{names[c]}.{loc[8 * s + j]}')
    return out

def link_names(name: str='u6') -> dict:
    return {k: [f'{name}.W{AXES[k]}_{c}' for c in algebra_u6().comp] for k in range(3)}

def build_matter_triplet(*, hop: int, mass: int, wilson: int, names=('q0', 'q1', 'q2')) -> tuple:
    """Three colour copies of B1-EM's Dirac pair (layers.matter.build_matter, read-only)."""
    from .matter import build_matter
    return tuple((build_matter(hop=hop, mass=mass, wilson=wilson, species='pair', name=nm) for nm in names))

def build_u6_links(*, A: int, lam: int=0, spring: str='frobenius', name: str='u6', label: str='audit') -> Block:
    """The M6(C) link gears (72 per axis), zero mode (D/2)|U|^2 and the optional OD4 spring (minus sign):
    spring="frobenius": -(lam/4)(|U|^2 - 6A^2)^2 (pins |U|_F only; radial stiffness 12 lam A^2);
    spring="matrix":    -(lam/4) Tr((U^dag U - A^2)^2) (pins every Hermitian mode of U^dag U; stiffness 2 lam A^2)."""
    alg = algebra_u6()
    D = 6
    loc = {k: [f'W{AXES[k]}_{c}' for c in alg.comp] for k in range(3)}
    x0 = {}
    phi = Poly()
    for k in range(3):
        U = []
        for c, g in enumerate(loc[k]):
            x0[g] = A * alg.one[c]
            U.append(Poly.var(g, (0, 0, 0), x0[g]))
        n2 = Poly()
        for u in U:
            n2 = n2 + u * u
        phi = phi + n2 * Fraction(D, 2)
        if lam and spring == 'frobenius':
            N = n2 - 6 * A * A
            phi = phi - N * N * Fraction(lam, 4)
        elif lam and spring == 'matrix':
            Nm = alg.prod(alg.dagger(U), U)
            Nm = [Nm[c] - A * A * alg.one[c] for c in range(alg.m)]
            sq = Poly()
            for v in Nm:
                if isinstance(v, Poly):
                    sq = sq + v * v
            phi = phi - sq * Fraction(lam, 4)
        elif lam:
            raise ValueError("spring must be 'frobenius' or 'matrix'")
    terms = deviation_terms(phi, D, x0)
    gears = [GearType(g, label, link=k) for k in range(3) for g in loc[k]]
    r0 = 2
    return Block(tuple(gears), tuple(terms), name=name, vacuum={g.name: r0 for g in gears}, params={'A': A, 'lam': lam, 'spring': spring, 'X0': {g: v for g, v in x0.items() if v}, 'r0': r0, 'reversor': 'Mp on every gear (b-only); Kramers variant: Mp on Re W, JM on Im W'}, doc='M6(C) link gears (one unified link algebra, option A)')

def build_u6_coupling(*, matter: tuple, links: Block, kd: int, kw: int, name: str='cu6') -> Block:
    """Phi_c = sum Psi(x)^T rho(W(x,d)) (1 (x) N_d) Psi(x+e_d): the W part of the matter hop (rank 3, one potential).
    Requires every matter block's hop = A*kd and wilson = A*kw (A = links.params["A"])."""
    from .matter import P8, W08
    A = links.params['A']
    for m in matter:
        if m.params['hop'] != A * kd or m.params['wilson'] != A * kw:
            raise ValueError('Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly.')
    alg = algebra_u6()
    J8 = _j8()
    mg = matter_gears(tuple((m.name for m in matter)))
    lg = {k: [f'{links.name}.W{AXES[k]}_{c}' for c in alg.comp] for k in range(3)}
    phi = Poly()
    t = phi.t
    for d in range(3):
        Nd = [[int(kd * P8[d][j][i] - kw * W08[i][j]) for j in range(8)] for i in range(8)]
        JN = [[sum((J8[i][q] * Nd[q][j] for q in range(8))) for j in range(8)] for i in range(8)]
        e = UNIT[d]
        for k in range(N6):
            for l in range(N6):
                for p in range(2):
                    M = Nd if p == 0 else JN
                    w = (lg[d][mn_index(k, l, p)], (0, 0, 0))
                    for i in range(8):
                        for j in range(8):
                            c = M[i][j]
                            if c:
                                key = tuple(sorted((w, (mg[8 * k + i], (0, 0, 0)), (mg[8 * l + j], e))))
                                t[key] = t.get(key, 0) + Fraction(c)
    terms = deviation_terms(phi, 6, {})
    return Block((), tuple(terms), name=name, vacuum={}, params={'kd': kd, 'kw': kw, 'A': A, 'matter': tuple((m.name for m in matter)), 'links': links.name, 'reversor': "Mp per gear (b-only); Kramers: K o M' on matter, M' on Re W, JM on Im W"}, doc='ONE-matter U(6) coupling (option A), reciprocal, rank 3')

@dataclass
class OneMatter:
    blocks: tuple
    alg: Algebra

def build_one_matter(*, lam: int=0, A: int, kd: int, kw: int, mass: int, spring: str='frobenius') -> OneMatter:
    """Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly."""
    matter = build_matter_triplet(hop=A * kd, mass=mass, wilson=A * kw)
    links = build_u6_links(A=A, lam=lam, spring=spring)
    coup = build_u6_coupling(matter=matter, links=links, kd=kd, kw=kw)
    return OneMatter(matter + (links, coup), algebra_u6())
__all__ = ['algebra_u6', 'matter_gears', 'link_names', 'build_matter_triplet', 'build_u6_links', 'build_u6_coupling', 'build_one_matter', 'OneMatter', 'mn_index']
