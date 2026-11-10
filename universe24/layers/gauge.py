"""Compact gauge layers as tensor blocks: SU(2) (weak, vector-like), SU(3) (strong, colour) and compact U(1).

EVERYTHING here is data: one integer potential Phi per layer, written in physical variables, shifted to deviation
form, differentiated into tensor terms u_t = dPhi/db_t (so every force block is reciprocal by construction: one
potential, field sign +1 for every gear). No state, no run, no observation (layers/ contract).

Gears per node (D = 6Q for every gear; Q must be ODD; new-gear vacuum remainder r0 = 3Q - 1, the fixed point of
R'(r) = D-2-r / D-r, so the sign-flip parts of the integer gauge maps fix the vacuum):
  matter  psi_c                 n real components (SU(2): integer quaternion = doublet, n = 4;
                                SU(3): colour triplet Z[i]^3, n = 6; U(1): Gaussian integer, n = 2)
  links   U<axis>_c             m real components per positive face link, stored at the BASE node (Yee axis
                                metadata k = 0, 1, 2): SU(2) integer quaternion m = 4, SU(3) integer complex 3x3
                                matrix m = 18, U(1) Gaussian integer m = 2
  2-path  P<k1><k2>_c           (optional) one algebra element per ordered pair k1 != k2, stored at the node;
                                it couples to U(x, k1) U(x + e_k1, k2) (plaquette half; Wilson term in the stiff limit)

Physical potential (sum over nodes x implicit; <.,.> = Euclidean = Re Tr(A^dagger B)):
  Phi = kappa  sum_k <psi(x), U(x,k) psi(x+e_k)>                       matter hops THROUGH the link   (rank 3)
      + (mass/2) |psi(x)|^2                                             on-site matter                 (rank 2)
      + ((D - c_U)/2) sum_k |U(x,k)|^2                                  link inertia (free zero mode if c_U = 0)
      - (lam/4) sum_k Tr((U^dagger U - A^2)^2)                          OD4 on-link SPRING (minus sign; rank 4;
                                                                        quaternion/complex: (|U|^2 - A^2)^2)
      + kappa_P sum_{k1 != k2} <P(x;k1,k2), U(x,k1) U(x+e_k1,k2)>       2-path gears                   (rank 3)
      + (c_P/2) |P|^2 + beta sum_{k1<k2} <P(x;k1,k2), P(x;k2,k1)>       on-site 2-path (Wilson cross term)
Vacuum: psi = 0, U = A*1, P = P0*1 with P0 = kappa_P A^2 / (D - c_P - beta) (must be an integer) and c_U = 4 kappa_P P0
(each link sits in four 2-paths; c_U balances their static pull so that U = A*1 is static). Deviation form:
gears store psi, W = U - A*1 and P~ = P - P0*1; Phi~ = Phi(X0 + X~) - D X0.X~ - const has no linear term (asserted),
so every term targeting a new gear vanishes in the vacuum and the composed vacuum is the reference board bit for bit.

Gauge invariance (polynomial identity, by construction): psi(x) -> g(x) psi(x), U(x,k) -> g(x) U g(x+e_k)^dagger,
P(x;k1,k2) -> g(x) P g(x+e_k1+e_k2)^dagger leaves Phi invariant for every g in the unit group of the algebra; the
integer subgroups (Q8; Z4; for SU(3) the DECLARED 96-element monomial subgroup, entries +-1/+-i and det 1 -- NOT
Delta(27), whose omega phases are not in Z[i]) act by signed
permutations (+ an integer affine shift in deviation form): bit-exact covariance. The integer anti-Hermitian
generators (quaternion units; i; i*lambda_1..7 and i*diag(1,1,-2) [+ i*1 for U(3)]) give the exact discrete Noether
(Gauss) identities, read by observe/gauge.py.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import permutations

from ..core.tensor import Block, GearType

ZERO = (0, 0, 0)
AXES = ("x", "y", "z")
UNIT = ((1, 0, 0), (0, 1, 0), (0, 0, 1))


# ============================================================================ polynomials (construction-time only)
class Poly:
    """Sparse polynomial with Fraction coefficients; a variable is (gear_name, offset)."""
    __slots__ = ("t",)

    def __init__(self, t=None):
        self.t = t if t is not None else {}

    @staticmethod
    def const(c) -> "Poly":
        return Poly({(): Fraction(c)}) if c else Poly()

    @staticmethod
    def var(name: str, off=ZERO, shift=0) -> "Poly":
        p = Poly({((name, tuple(off)),): Fraction(1)})
        if shift:
            p.t[()] = Fraction(shift)
        return p

    def copy(self) -> "Poly":
        return Poly(dict(self.t))

    def __add__(self, o):
        if not isinstance(o, Poly):
            o = Poly.const(o)
        t = dict(self.t)
        for k, c in o.t.items():
            v = t.get(k, 0) + c
            if v:
                t[k] = v
            else:
                t.pop(k, None)
        return Poly(t)

    __radd__ = __add__

    def __neg__(self):
        return Poly({k: -c for k, c in self.t.items()})

    def __sub__(self, o):
        return self + (-o if isinstance(o, Poly) else Poly.const(-o))

    def __mul__(self, o):
        if not isinstance(o, Poly):
            o = Fraction(o)
            return Poly({k: c * o for k, c in self.t.items()}) if o else Poly()
        t: dict = {}
        for k1, c1 in self.t.items():
            for k2, c2 in o.t.items():
                k = tuple(sorted(k1 + k2))
                v = t.get(k, 0) + c1 * c2
                if v:
                    t[k] = v
                else:
                    t.pop(k, None)
        return Poly(t)

    __rmul__ = __mul__

    @property
    def degree(self) -> int:
        return max((len(k) for k in self.t), default=0)


def vec_add(X, Y):
    return [x + y for x, y in zip(X, Y)]


def vec_scale(s, X):
    return [x * s for x in X]


def vec_dot(X, Y) -> Poly:
    out = Poly()
    for x, y in zip(X, Y):
        out = out + x * y
    return out


# ============================================================================ algebras (integer structure constants)
@dataclass(frozen=True)
class Algebra:
    """Real form of an integer algebra (links) acting on an integer module (matter).

    mul[(a, b)] = (c, s): e_a e_b = s e_c (single-term products, absent = 0); act[(a, j)] = (i, s): e_a v_j = s v_i;
    adj[a] = (a', s): (e_a)^dagger = s e_a'; one = components of the unit; generators = integer anti-Hermitian
    elements (label, vector) used by the Noether identities; group = the integer unit subgroup used for bit-exact
    local covariance (vectors with entries in {0, +-1})."""
    name: str
    m: int
    n: int
    mul: dict
    act: dict
    adj: tuple
    one: tuple
    generators: tuple
    group: tuple
    comp: tuple
    mcomp: tuple

    # ---- operations on vectors (any ring: ints, Fractions, Poly)
    def prod(self, X, Y):
        out = [0] * self.m
        for (a, b), (c, s) in self.mul.items():
            xa, yb = X[a], Y[b]
            if isinstance(xa, int) and xa == 0 or isinstance(yb, int) and yb == 0:
                continue
            out[c] = out[c] + (xa * yb) * s
        return out

    def apply(self, X, v):
        out = [0] * self.n
        for (a, j), (i, s) in self.act.items():
            xa, vj = X[a], v[j]
            if isinstance(xa, int) and xa == 0 or isinstance(vj, int) and vj == 0:
                continue
            out[i] = out[i] + (xa * vj) * s
        return out

    def dagger(self, X):
        out = [0] * self.m
        for a, (a2, s) in enumerate(self.adj):
            out[a2] = X[a] * s
        return out

    def left_matrix(self, X):
        """Integer m x m matrix of Y -> X Y."""
        M = [[0] * self.m for _ in range(self.m)]
        for (a, b), (c, s) in self.mul.items():
            if X[a]:
                M[c][b] += s * X[a]
        return M

    def right_matrix(self, X):
        """Integer m x m matrix of Y -> Y X."""
        M = [[0] * self.m for _ in range(self.m)]
        for (b, a), (c, s) in self.mul.items():
            if X[a]:
                M[c][b] += s * X[a]
        return M

    def act_matrix(self, X):
        """Integer n x n matrix of v -> X v."""
        M = [[0] * self.n for _ in range(self.n)]
        for (a, j), (i, s) in self.act.items():
            if X[a]:
                M[i][j] += s * X[a]
        return M


def _quaternion() -> Algebra:
    # e0 = 1, e1 = i, e2 = j, e3 = k ; products of basis units
    table = {(0, 0): (0, 1), (0, 1): (1, 1), (0, 2): (2, 1), (0, 3): (3, 1),
             (1, 0): (1, 1), (1, 1): (0, -1), (1, 2): (3, 1), (1, 3): (2, -1),
             (2, 0): (2, 1), (2, 1): (3, -1), (2, 2): (0, -1), (2, 3): (1, 1),
             (3, 0): (3, 1), (3, 1): (2, 1), (3, 2): (1, -1), (3, 3): (0, -1)}
    units = []
    for a in range(4):
        for s in (1, -1):
            v = [0, 0, 0, 0]
            v[a] = s
            units.append(tuple(v))
    gens = (("i", (0, 1, 0, 0)), ("j", (0, 0, 1, 0)), ("k", (0, 0, 0, 1)))
    return Algebra("H", 4, 4, table, dict(table), ((0, 1), (1, -1), (2, -1), (3, -1)), (1, 0, 0, 0), gens,
                   tuple(units), ("1", "i", "j", "k"), ("1", "i", "j", "k"))


def _gaussian() -> Algebra:
    table = {(0, 0): (0, 1), (0, 1): (1, 1), (1, 0): (1, 1), (1, 1): (0, -1)}
    units = ((1, 0), (-1, 0), (0, 1), (0, -1))
    return Algebra("C", 2, 2, table, dict(table), ((0, 1), (1, -1)), (1, 0), (("i", (0, 1)),), units,
                   ("re", "im"), ("re", "im"))


def m3_index(i: int, j: int, p: int) -> int:
    return 2 * (3 * i + j) + p


def _m3c() -> Algebra:
    mul, act = {}, {}
    for i in range(3):
        for j in range(3):
            for l in range(3):
                for p in range(2):
                    for q in range(2):
                        s = -1 if (p and q) else 1
                        mul[(m3_index(i, j, p), m3_index(j, l, q))] = (m3_index(i, l, (p + q) % 2), s)
                        act[(m3_index(i, j, p), 2 * j + q)] = (2 * i + (p + q) % 2, s)
    adj = [None] * 18
    for i in range(3):
        for j in range(3):
            for p in range(2):
                adj[m3_index(i, j, p)] = (m3_index(j, i, p), -1 if p else 1)
    one = [0] * 18
    for i in range(3):
        one[m3_index(i, i, 0)] = 1

    def el(entries):
        v = [0] * 18
        for (i, j, p), val in entries.items():
            v[m3_index(i, j, p)] = val
        return tuple(v)
    gens = (("ilam1", el({(0, 1, 1): 1, (1, 0, 1): 1})),
            ("ilam2", el({(0, 1, 0): 1, (1, 0, 0): -1})),
            ("ilam3", el({(0, 0, 1): 1, (1, 1, 1): -1})),
            ("ilam4", el({(0, 2, 1): 1, (2, 0, 1): 1})),
            ("ilam5", el({(0, 2, 0): 1, (2, 0, 0): -1})),
            ("ilam6", el({(1, 2, 1): 1, (2, 1, 1): 1})),
            ("ilam7", el({(1, 2, 0): 1, (2, 1, 0): -1})),
            ("ilam8x", el({(0, 0, 1): 1, (1, 1, 1): 1, (2, 2, 1): -2})),   # i*diag(1,1,-2) = sqrt(3) i lambda_8
            ("i1_u1", el({(0, 0, 1): 1, (1, 1, 1): 1, (2, 2, 1): 1})))      # the U(1) of U(3) (Phi is U(3)-invariant)
    # integer subgroup: monomial matrices with entries in {+-1, +-i} and det = 1 (96 elements)
    group = []
    for perm in permutations(range(3)):
        sgn = 1
        for x in range(3):
            for y in range(x + 1, 3):
                if perm[x] > perm[y]:
                    sgn = -sgn
        for ph in [(a, b, c) for a in range(4) for b in range(4) for c in range(4)]:
            # det = sgn * i^(a+b+c) must be 1
            tot = (sum(ph) + (0 if sgn == 1 else 2)) % 4
            if tot != 0:
                continue
            ent = {}
            for row in range(3):
                col = perm[row]
                e = ph[row] % 4          # i^e = 1, i, -1, -i
                ent[(row, col, e % 2)] = 1 if e in (0, 1) else -1
            group.append(el(ent))
    comp = tuple(f"{i}{j}{'ri'[p]}" for i in range(3) for j in range(3) for p in range(2))
    mcomp = tuple(f"{i}{'ri'[p]}" for i in range(3) for p in range(2))
    return Algebra("M3C", 18, 6, mul, act, tuple(adj), tuple(one), gens, tuple(group), comp, mcomp)


ALGEBRAS = {"su2": _quaternion(), "u1": _gaussian(), "su3": _m3c()}


# ============================================================================ potential -> deviation-form terms
def deviation_terms(phi: Poly, D: int, x0: dict) -> list:
    """phi = the PHYSICAL potential written in deviation variables (physical = x0 + stored). Returns the terms of
    u = dPhi~/db with Phi~ = phi - sum_g D x0_g X~_g(0) - const. Raises if the shifted potential keeps a linear term
    (the vacuum would not be static) or if a u-coefficient is not an integer."""
    t = dict(phi.t)
    t.pop((), None)
    for g, v in x0.items():
        if v:
            key = ((g, ZERO),)
            val = t.get(key, 0) - D * v
            if val:
                t[key] = val
            else:
                t.pop(key, None)
    lin: dict = {}
    for k, c in t.items():
        if len(k) == 1:
            lin[k[0][0]] = lin.get(k[0][0], 0) + c
    bad = {g: c for g, c in lin.items() if c}
    if bad:
        raise ValueError(f"deviation form failed: linear potential terms remain (vacuum not static): {bad}")
    terms: dict = {}
    for k, c in t.items():
        if len(k) <= 1:
            continue
        for v in sorted(set(k)):
            n = k.count(v)
            g, off = v
            rest = list(k)
            rest.remove(v)
            fac = tuple(sorted((h, (o[0] - off[0], o[1] - off[1], o[2] - off[2])) for h, o in rest))
            key = (g, fac)
            terms[key] = terms.get(key, 0) + c * n
    out = []
    for (g, fac), c in sorted(terms.items()):
        if c == 0:
            continue
        if c.denominator != 1:
            raise ValueError(f"non-integer u-coefficient {c} for target {g} factors {fac}")
        out.append((g, int(c), tuple((h, o, "b") for h, o in fac)))
    return out


# ============================================================================ the compact gauge layer
def gear_names(group: str, use_P: bool):
    alg = ALGEBRAS[group]
    matter = [f"psi_{c}" for c in alg.mcomp]
    links = {k: [f"U{AXES[k]}_{c}" for c in alg.comp] for k in range(3)}
    paths = {}
    if use_P:
        for k1 in range(3):
            for k2 in range(3):
                if k1 != k2:
                    paths[(k1, k2)] = [f"P{AXES[k1]}{AXES[k2]}_{c}" for c in alg.comp]
    return matter, links, paths


def two_path_vacuum(Q: int, A: int, kappa_P: int, c_P: int, beta: int) -> tuple[int, int]:
    """(P0, c_U) of the static vacuum: P0 = kappa_P A^2/(D - c_P - beta) (integer), c_U = 4 kappa_P P0."""
    D = 6 * Q
    dP = D - c_P - beta
    if kappa_P == 0:
        return 0, 0
    if dP <= 0 or (kappa_P * A * A) % dP:
        raise ValueError(f"2-path vacuum P0 = kappa_P A^2/(D - c_P - beta) = {kappa_P * A * A}/{dP} is not a positive "
                         "integer; choose kappa_P, c_P, beta accordingly")
    P0 = kappa_P * A * A // dP
    return P0, 4 * kappa_P * P0


def build_gauge(*, group: str, Q: int, A: int, kappa: int, mass: int, lam: int = 0, use_P: bool = False,
                kappa_P: int = 0, c_P: int = 0, beta: int = 0, name: str = "su2",
                matter_label: str = "official", field_label: str = "audit") -> Block:
    """Compact gauge layer block (see the module docstring for Phi).

    Parameters (keyword-only, all integers):
      group   "su2" (integer quaternion doublet + quaternion links), "su3" (Z[i]^3 triplet + integer complex 3x3
              links) or "u1" (Gaussian-integer matter + Gaussian-integer links);
      Q       divisor scale (ODD), D = 6Q for every gear;      A  link vacuum norm (U = A*1);
      kappa   matter hopping through the link (kappa*A = vacuum hopping);   mass  on-site matter coefficient;
      lam     OD4 spring strength (lam > 0: Phi -= (lam/4) Tr((U^dag U - A^2)^2); lam = 0: no rank-4 term);
      use_P, kappa_P, c_P, beta   2-path gears (P0 = kappa_P A^2/(D - c_P - beta) must be an integer).
    Vacuum remainders: 3Q - 1 for every gear (Block.vacuum). Labels: matter official, links and 2-paths audit (OD1).
    """
    if group not in ALGEBRAS:
        raise ValueError(f"group must be one of {sorted(ALGEBRAS)}")
    for nm, v in (("Q", Q), ("A", A), ("kappa", kappa), ("mass", mass), ("lam", lam), ("kappa_P", kappa_P),
                  ("c_P", c_P), ("beta", beta)):
        if type(v) is not int:
            raise TypeError(f"{nm} must be a Python int")
    if Q < 1 or Q % 2 == 0:
        raise ValueError("Q must be ODD (new-gear vacuum r0 = 3Q - 1 is the R' fixed point only for odd Q)")
    if lam < 0:
        raise ValueError("the spring enters with a MINUS sign and lam >= 0 (OD4)")
    alg = ALGEBRAS[group]
    D = 6 * Q
    matter, links, paths = gear_names(group, use_P)
    P0, c_U = two_path_vacuum(Q, A, kappa_P, c_P, beta) if use_P else (0, 0)
    x0 = {}
    for k in range(3):
        for c, g in enumerate(links[k]):
            x0[g] = A * alg.one[c]
    for key, names in paths.items():
        for c, g in enumerate(names):
            x0[g] = P0 * alg.one[c]

    def psi(off):
        return [Poly.var(g, off) for g in matter]

    def U(k, off):
        return [Poly.var(g, off, x0[g]) for g in links[k]]

    def P(k1, k2, off):
        return [Poly.var(g, off, x0[g]) for g in paths[(k1, k2)]]

    phi = Poly()
    p0 = psi(ZERO)
    for k in range(3):
        phi = phi + vec_dot(p0, alg.apply(U(k, ZERO), psi(UNIT[k]))) * kappa
    phi = phi + vec_dot(p0, p0) * Fraction(mass, 2)
    for k in range(3):
        Uk = U(k, ZERO)
        phi = phi + vec_dot(Uk, Uk) * Fraction(D - c_U, 2)
        if lam:
            N = alg.prod(alg.dagger(Uk), Uk)
            N = [N[c] - A * A * alg.one[c] for c in range(alg.m)]
            phi = phi - vec_dot(N, N) * Fraction(lam, 4)
    if use_P:
        for (k1, k2) in paths:
            Pk = P(k1, k2, ZERO)
            phi = phi + vec_dot(Pk, alg.prod(U(k1, ZERO), U(k2, UNIT[k1]))) * kappa_P
            phi = phi + vec_dot(Pk, Pk) * Fraction(c_P, 2)
            if k1 < k2:
                phi = phi + vec_dot(Pk, P(k2, k1, ZERO)) * beta
    terms = deviation_terms(phi, D, x0)
    gears = [GearType(g, matter_label) for g in matter]
    for k in range(3):
        gears += [GearType(g, field_label, link=k) for g in links[k]]
    for key in paths:
        gears += [GearType(g, field_label) for g in paths[key]]
    r0 = 3 * Q - 1
    params = {"group": group, "Q": Q, "A": A, "kappa": kappa, "mass": mass, "lam": lam, "use_P": use_P,
              "kappa_P": kappa_P, "c_P": c_P, "beta": beta, "P0": P0, "c_U": c_U,
              "X0": {g: v for g, v in x0.items() if v}, "r0": r0,
              "reversor": {"new gears": "Mp (b, a, R'(r)); fixes r0 = 3Q-1 (odd Q only: for even Q no remainder is "
                                        "fixed by R', so no mirror-fixed vacuum exists)",
                           "also exact": "M (b, a, D-1-r), not vacuum-fixing", "a-read gears": "none (b-only block)",
                           "J/JR/JM": "not used: the rank-3 couplings give quadratic inputs, even under negation, so the block is not J-odd"}}
    doc = (f"compact {group.upper()} gauge layer: matter {alg.n}/node, links {alg.m}/axis (stored at the base node), "
           f"{'2-path gears 6x' + str(alg.m) + '/node, ' if use_P else ''}spring lam = {lam}; deviation form "
           f"(U = A*1 + W, A = {A}{', P = P0*1 + P~, P0 = ' + str(P0) if use_P else ''})")
    return Block(tuple(gears), tuple(terms), name=name, vacuum={g.name: r0 for g in gears}, params=params, doc=doc,
                 Q=Q)


def build_su2(*, Q, A, kappa, mass, lam=0, use_P=False, kappa_P=0, c_P=0, beta=0, name="su2") -> Block:
    """Weak (vector-like) SU(2): integer-quaternion doublets + integer-quaternion links (4 gears per link)."""
    return build_gauge(group="su2", Q=Q, A=A, kappa=kappa, mass=mass, lam=lam, use_P=use_P, kappa_P=kappa_P,
                       c_P=c_P, beta=beta, name=name)


def build_su3(*, Q, A, kappa, mass, lam=0, use_P=False, kappa_P=0, c_P=0, beta=0, name="su3") -> Block:
    """Strong SU(3): colour triplets in Z[i]^3 + integer complex 3x3 links (18 gears per link)."""
    return build_gauge(group="su3", Q=Q, A=A, kappa=kappa, mass=mass, lam=lam, use_P=use_P, kappa_P=kappa_P,
                       c_P=c_P, beta=beta, name=name)


def build_u1(*, Q, A, kappa, mass, lam=0, use_P=False, kappa_P=0, c_P=0, beta=0, name="u1") -> Block:
    """Compact U(1): Gaussian-integer matter + Gaussian-integer links (2 gears per link); exact local Z4."""
    return build_gauge(group="u1", Q=Q, A=A, kappa=kappa, mass=mass, lam=lam, use_P=use_P, kappa_P=kappa_P,
                       c_P=c_P, beta=beta, name=name)


# ============================================================================ shipped defaults
# Chosen by the SPRING DEFAULT RULE pre-registered in NOTES_gauge.md (09:50:00 UTC) from selection run S1
# (results/gauge/S1_spring_default.json): regime F, lam = 4 for su2, su3, u1 (all with 2-path gears). ONE Q for all.
DEFAULT_Q = (1 << 25) + 1
DEFAULT_REGIME = {"Q": DEFAULT_Q, "A": 4096, "kappa": (DEFAULT_Q - 1) // (2 * 4096), "mass": DEFAULT_Q + 3,
                  "use_P": True, "kappa_P": 256, "c_P": 0, "beta": 6 * DEFAULT_Q - (1 << 25)}
DEFAULT_LAM = {"su2": 4, "su3": 4, "u1": 4}


def default_regime(Q: int = DEFAULT_Q) -> dict:
    """The shipped default family for Q = 2^(2n+1) + 1 (odd): A = kappa = 2^n (kappa*A = (Q-1)/2), mass = Q + 3,
    2-path kappa_P = 256, c_P = 0, beta = 6Q - 2^(2n+1) (P0 = 128), and lam = 4 (key "lam"). It keeps every
    dimensionless ratio of the selected regime F (n = 12, Q = 2^25+1); verified at Q = 2^29+1 by run S2."""
    m = Q - 1
    if Q < 3 or m & (m - 1) or (m.bit_length() - 1) % 2 == 0:
        raise ValueError("default_regime needs Q = 2^(2n+1) + 1 (e.g. 2^25+1, 2^29+1)")
    n = (m.bit_length() - 2) // 2
    A = 1 << n
    return {"Q": Q, "A": A, "kappa": A, "mass": Q + 3, "use_P": True, "kappa_P": 256, "c_P": 0,
            "beta": 6 * Q - (1 << (2 * n + 1)), "lam": 4}


def build_default(group: str, *, Q: int = DEFAULT_Q, name: str | None = None) -> Block:
    """The shipped default block of one compact gauge layer (default family at this Q; lam = 4; 2-path gears)."""
    reg = default_regime(Q)
    lam = reg.pop("lam")              # = DEFAULT_LAM[group] = 4 for every group (S1 / S2)
    return build_gauge(group=group, lam=lam, name=name or group, **reg)


def default_gauge_blocks() -> tuple:
    """(su2, su3, u1) default blocks, ONE Q. The c2 dynamic base links are NOT included (DEFAULT OFF, manager ruling)
    and c1 is not adopted."""
    return tuple(build_default(g) for g in ("su2", "su3", "u1"))


__all__ = ["Poly", "Algebra", "ALGEBRAS", "deviation_terms", "gear_names", "two_path_vacuum", "build_gauge",
           "build_su2", "build_su3", "build_u1", "m3_index", "DEFAULT_Q", "DEFAULT_REGIME", "DEFAULT_LAM",
           "build_default", "default_gauge_blocks", "default_regime"]
