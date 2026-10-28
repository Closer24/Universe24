"""David's check for stage 6: the five kinds of the 24 from the Spokes alone, and the contraction as a group sum.

usage: python3 -I p11_kinds.py   (no worktree needed; exact integers)
The 24 are the signed permutations of the three axes of determinant +1 (the frame's turns()). From them alone:
  T1(g) = g, the Spokes' own 3 x 3 matrix;
  A2(g) = the sign of the axes' permutation, the determinant of |g| (the axes as the three pairs of opposite Spokes);
  E(g)  = the axes' permutation on the plane where the three sum to 0, in the whole basis (e1 - e2, e2 - e3);
  T2(g) = A2(g) T1(g);  A1(g) = 1.
Checks:
  (1) each is a representation: rho(g h) = rho(g) rho(h) on all 576 pairs;
  (2) the characters on the five classes (identity, third turns, face half turns, quarter turns, edge half turns),
      against Sofer's table; their orthonormality, sum over g of chi_i chi_j = 24 delta_ij, in all 25 sums;
  (3) the six Spokes' permutation character is A1 + E + T1, and the axes' is A1 + E;
  (4) the product table by characters, every multiplicity 0 or 1 (no product holds a kind twice);
  (5) the contraction C[i, k -> m] = sum over g of rho_m(g) S (rho_i(g^-1) x rho_k(g^-1)) from a seed S: it is
      equivariant for all 24, and it is 0 exactly where the table holds no m in i x k; T1 x T1 -> A1 is the dot,
      -> T1 the cross, A2 x T1 -> T2 the plain product, up to one whole factor each. C is built from each
      elementary seed in turn, the first group sum that is not 0; one fixed seed can be orthogonal to a channel,
      which the two controls show (all ones; a polynomial with no symmetry between the operands).
"""
import itertools
from fractions import Fraction


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def det3(m):
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


def turns():
    for order in itertools.permutations(range(3)):
        for signs in itertools.product((1, -1), repeat=3):
            m = [[0] * 3 for _ in range(3)]
            for i in range(3):
                m[i][order[i]] = signs[i]
            if det3(m) == 1:
                yield m


G = list(turns())
assert len(G) == 24
I3 = [[1 if i == j else 0 for j in range(3)] for i in range(3)]


def key(m):
    return tuple(map(tuple, m))


INDEX = {key(g): n for n, g in enumerate(G)}
INV = [INDEX[key([[g[j][i] for j in range(3)] for i in range(3)])] for g in G]  # g^-1 = g transposed (orthogonal)


def perm_part(g):
    return [[abs(x) for x in row] for row in g]


def rho_A1(g):
    return [[1]]


def rho_A2(g):
    return [[det3(perm_part(g))]]


def rho_T1(g):
    return g


def rho_T2(g):
    s = det3(perm_part(g))
    return [[s * x for x in row] for row in g]


# E: the axes' permutation P = |g| acts on R^3; on the plane sum = 0 with basis f1 = e1 - e2, f2 = e2 - e3.
# P f = (coefficients in f1, f2): a vector v = (v1, v2, v3) with sum 0 is c1 f1 + c2 f2 with c1 = v1, c2 = v1 + v2.
def rho_E(g):
    p = perm_part(g)
    cols = []
    for f in ((1, -1, 0), (0, 1, -1)):
        v = [sum(p[i][j] * f[j] for j in range(3)) for i in range(3)]
        cols.append((v[0], v[0] + v[1]))
    return [[cols[0][0], cols[1][0]], [cols[0][1], cols[1][1]]]


KINDS = {"A1": rho_A1, "A2": rho_A2, "E": rho_E, "T1": rho_T1, "T2": rho_T2}
fails = {}

# (1) homomorphisms
fails["rep"] = sum(
    matmul(rho(g), rho(h)) != rho(G[INDEX[key(matmul(g, h))]]) for rho in KINDS.values() for g in G for h in G
)


def trace(m):
    return sum(m[i][i] for i in range(len(m)))


chi = {k: [trace(r(g)) for g in G] for k, r in KINDS.items()}


# classes by order and trace of g: identity; third turns (trace 0); face half turns (trace -1, diagonal);
# quarter turns (trace 1, not identity); edge half turns (trace -1, not diagonal)
def klass(g):
    t = trace(g)
    diagonal = all(g[i][j] == 0 for i in range(3) for j in range(3) if i != j)
    if g == I3:
        return 0
    if t == 0:
        return 1
    if t == -1 and diagonal:
        return 2
    if t == 1:
        return 3
    return 4


classes = [klass(g) for g in G]
sizes = [classes.count(c) for c in range(5)]
table = {k: [chi[k][classes.index(c)] for c in range(5)] for k in KINDS}
sofer = {"A1": [1, 1, 1, 1, 1], "A2": [1, 1, 1, -1, -1], "E": [2, -1, 2, 0, 0], "T1": [3, 0, -1, 1, -1],
         "T2": [3, 0, -1, -1, 1]}
fails["classes"] = int(sizes != [1, 8, 3, 6, 6] or table != sofer)
fails["orthonormal"] = sum(
    sum(x * y for x, y in zip(chi[i], chi[j])) != (24 if i == j else 0) for i in KINDS for j in KINDS
)

# (3) the Spokes' and the axes' permutation characters
spokes = [(axis, sign) for axis in range(3) for sign in (1, -1)]


def act(g, spoke):
    axis, sign = spoke
    v = [g[i][axis] * sign for i in range(3)]
    i = next(i for i in range(3) if v[i])
    return (i, v[i])


chi_spokes = [sum(act(g, s) == s for s in spokes) for g in G]
chi_axes = [trace(perm_part(g)) for g in G]
fails["spokes"] = int(chi_spokes != [a + e + t for a, e, t in zip(chi["A1"], chi["E"], chi["T1"])])
fails["axes"] = int(chi_axes != [a + e for a, e in zip(chi["A1"], chi["E"])])

# (4) the product table
products, multi = {}, 0
for i, k in itertools.combinations_with_replacement(list(KINDS), 2):
    parts = []
    for m in KINDS:
        n = Fraction(sum(chi[i][g] * chi[k][g] * chi[m][g] for g in range(24)), 24)
        multi += n not in (0, 1)
        if n:
            parts.append(m)
    products[(i, k)] = parts
fails["multiplicity"] = multi

# (5) the contraction as a group sum, from a seed of ones; equivariance and zeros
DIM = {"A1": 1, "A2": 1, "E": 2, "T1": 3, "T2": 3}


def seed(dm, di, dk, symmetric):
    """A seed tensor: with no symmetry between the two operands, or (the control) symmetric in them."""
    if symmetric:
        return [[[1] * dk for _ in range(di)] for _ in range(dm)]
    return [[[(1 + 2 * y + 5 * p + 11 * q + 7 * y * p + 13 * p * q + 17 * q * y + 3 * y * p * q) ** 2 % 101
              for q in range(dk)] for p in range(di)] for y in range(dm)]


def averaged(i, k, m, s0):
    """The group sum of one seed: sum over g of rho_m(g) s0 (rho_i(g^-1) x rho_k(g^-1)), equivariant by construction."""
    di, dk, dm = DIM[i], DIM[k], DIM[m]
    c = [[[0] * dk for _ in range(di)] for _ in range(dm)]
    for n, g in enumerate(G):
        gi = KINDS[i](G[INV[n]])
        gk = KINDS[k](G[INV[n]])
        gm = KINDS[m](g)
        for x in range(dm):
            for a in range(di):
                for b in range(dk):
                    c[x][a][b] += sum(gm[x][y] * s0[y][p][q] * gi[p][a] * gk[q][b] for y in range(dm)
                                      for p in range(di) for q in range(dk))
    return c


def contraction(i, k, m, how="elementary"):
    """C[i, k -> m]: the group sum from each elementary seed in turn, the first that is not 0 (the load's way);
    or, as controls, from one fixed seed: all ones, or a polynomial with no symmetry between the operands."""
    di, dk, dm = DIM[i], DIM[k], DIM[m]
    if how != "elementary":
        return averaged(i, k, m, seed(dm, di, dk, how == "ones"))
    for y, p, q in itertools.product(range(dm), range(di), range(dk)):
        s0 = [[[int((yy, pp, qq) == (y, p, q)) for qq in range(dk)] for pp in range(di)] for yy in range(dm)]
        c = averaged(i, k, m, s0)
        if any(x for plane in c for row in plane for x in row):
            return c
    return averaged(i, k, m, [[[0] * dk for _ in range(di)] for _ in range(dm)])


def apply(c, u, v):
    return [sum(c[x][a][b] * u[a] * v[b] for a in range(len(u)) for b in range(len(v))) for x in range(len(c))]


def rmul(m, v):
    return [sum(m[i][j] * v[j] for j in range(len(v))) for i in range(len(m))]


zero_ok = equi = 0
named = {}
for i, k in itertools.product(KINDS, repeat=2):
    for m in KINDS:
        c = contraction(i, k, m)
        nonzero = any(x for plane in c for row in plane for x in row)
        held = m in products[tuple(sorted((i, k), key=list(KINDS).index))]
        zero_ok += nonzero != held
        if nonzero:
            for g in G:
                for trial in range(2):
                    u = [((7 * a + 3 * trial) % 5) - 2 for a in range(DIM[i])]
                    v = [((5 * b + 2 * trial) % 7) - 3 for b in range(DIM[k])]
                    lhs = apply(c, rmul(KINDS[i](g), u), rmul(KINDS[k](g), v))
                    rhs = rmul(KINDS[m](g), apply(c, u, v))
                    equi += lhs != rhs
            named[(i, k, m)] = c
fails["zeros"] = zero_ok
lost = [f"{i} x {k} -> {m}" for (i, k, m) in named if not any(x for plane in contraction(i, k, m, "ones") for row in plane for x in row)]
lost_poly = [f"{i} x {k} -> {m}" for (i, k, m) in named if not any(x for plane in contraction(i, k, m, "polynomial") for row in plane for x in row)]
fails["equivariant"] = equi


# the classical channels, up to one whole factor
def factor_of(c, ref):
    flat_c = [x for plane in c for row in plane for x in row]
    flat_r = [x for plane in ref for row in plane for x in row]
    ratios = {Fraction(x, y) for x, y in zip(flat_c, flat_r) if y}
    return len(ratios) == 1 and all((x == 0) == (y == 0) for x, y in zip(flat_c, flat_r))


dot = [[[1 if a == b else 0 for b in range(3)] for a in range(3)]]
cross = [[[(1 if (x, a, b) in ((0, 1, 2), (1, 2, 0), (2, 0, 1)) else -1 if (x, a, b) in ((0, 2, 1), (1, 0, 2), (2, 1, 0)) else 0)
           for b in range(3)] for a in range(3)] for x in range(3)]
plain = [[[1 if a == x else 0 for a in range(3)]] for x in range(3)]  # A2 x T1 -> T2: (s, v) -> s v
fails["channels"] = int(not (factor_of(named[("T1", "T1", "A1")], dot) and factor_of(named[("T1", "T1", "T1")], cross)
                             and factor_of([[[row[0] for row in plane]] for plane in
                                            [[[named[("A2", "T1", "T2")][x][0][a]] for a in range(3)] for x in range(3)]],
                                           [[[1 if a == x else 0] for a in range(3)] for x in range(3)]) ))
for k, v in fails.items():
    print(f"{k}: failures {v}")
print("control: one seed of all ones loses", len(lost), "of", len(named), "channels:", ", ".join(lost))
print("control: one polynomial seed with no symmetry loses", len(lost_poly), "of", len(named), "channels:", ", ".join(lost_poly))
print("the products:", {f"{i} x {k}": " + ".join(v) for (i, k), v in products.items()})
