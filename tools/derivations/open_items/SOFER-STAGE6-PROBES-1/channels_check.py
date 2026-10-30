"""Sofer's own check of David's stage 6 table (6481240750, item 4), built from the groups' definitions alone, not from his p11:
the 24, the five kinds as matrices (T1 = g, A2 = sign of the axes' permutation, E = that permutation on the plane summing to 0
in the whole basis (e1 - e2, e2 - e3), T2 = A2 T1), the channels C[i, k -> m] as the Reynolds sums of the elementary seeds.
Run: python -I channels_check.py"""
import itertools
from fractions import Fraction

IDX = range(3)


def det3(m):
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


def mm(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def perm_sign(p):
    return (-1) ** sum(1 for i in IDX for j in IDX if i < j and p[i] > p[j])


turns = []
for perm in itertools.permutations(IDX):
    for signs in itertools.product((1, -1), repeat=3):
        m = [[0] * 3 for _ in IDX]
        for i in IDX:
            m[i][perm[i]] = signs[i]
        if det3(m) == 1:
            turns.append((perm, m))
assert len(turns) == 24


def rep_E(perm):
    # |g| as the permutation of axes, acting on w (sum 0); coordinates of w in (b1, b2) are (w1, w1 + w2)
    p = [[1 if perm[i] == j else 0 for j in IDX] for i in IDX]
    cols = []
    for b in ([1, -1, 0], [0, 1, -1]):
        w = [sum(p[i][j] * b[j] for j in IDX) for i in IDX]
        assert sum(w) == 0
        cols.append([w[0], w[0] + w[1]])
    return [[cols[0][0], cols[1][0]], [cols[0][1], cols[1][1]]]


KINDS = {
    "A1": lambda perm, m: [[1]],
    "A2": lambda perm, m: [[perm_sign(perm)]],
    "E": lambda perm, m: rep_E(perm),
    "T1": lambda perm, m: [row[:] for row in m],
    "T2": lambda perm, m: [[perm_sign(perm) * x for x in row] for row in m],
}
REP = {k: [f(perm, m) for perm, m in turns] for k, f in KINDS.items()}
DIM = {k: len(REP[k][0]) for k in KINDS}
# inverse index: the turn that is the inverse of g (so rho(g)^-1 = rho(g^-1), whole)
key = {tuple(map(tuple, m)): n for n, (perm, m) in enumerate(turns)}
inv = []
for n, (perm, m) in enumerate(turns):
    t = [[m[j][i] for j in IDX] for i in IDX]  # signed permutation: inverse = transpose
    inv.append(key[tuple(map(tuple, t))])

# each is a representation on all 576 pairs
prod_idx = {}
for a, (pa, ma) in enumerate(turns):
    for b, (pb, mb) in enumerate(turns):
        prod_idx[(a, b)] = key[tuple(map(tuple, mm(ma, mb)))]
bad = 0
for k in KINDS:
    for (a, b), c in prod_idx.items():
        bad += mm(REP[k][a], REP[k][b]) != REP[k][c]
print("representations: failures", bad, "of", 5 * 576)


def kron(a, b):
    return [[a[i][j] * b[k][l] for j in range(len(a[0])) for l in range(len(b[0]))] for i in range(len(a)) for k in range(len(b))]


def reynolds(i, k, m, seed):
    """sum over g of rho_m(g^-1) seed (rho_i(g) x rho_k(g)); whole entries, 24 times the projector's image."""
    rows, cols = DIM[m], DIM[i] * DIM[k]
    total = [[0] * cols for _ in range(rows)]
    for g in range(24):
        t = mm(mm(REP[m][inv[g]], seed), kron(REP[i][g], REP[k][g]))
        for r in range(rows):
            for c in range(cols):
                total[r][c] += t[r][c]
    return total


def rank(vectors):
    rows = [[Fraction(x) for x in v] for v in vectors]
    r = 0
    for c in range(len(rows[0]) if rows else 0):
        pivot = next((n for n in range(r, len(rows)) if rows[n][c] != 0), None)
        if pivot is None:
            continue
        rows[r], rows[pivot] = rows[pivot], rows[r]
        for n in range(len(rows)):
            if n != r and rows[n][c] != 0:
                f = rows[n][c] / rows[r][c]
                rows[n] = [x - f * y for x, y in zip(rows[n], rows[r])]
        r += 1
    return r


names = list(KINDS)
channels, multiples, ones_zero, first_missing, equivariant_bad = [], [], [], [], 0
firsts = {}
for i in names:
    for k in names:
        for m in names:
            images = []
            first = None
            for r in range(DIM[m]):
                for c in range(DIM[i] * DIM[k]):
                    seed = [[0] * (DIM[i] * DIM[k]) for _ in range(DIM[m])]
                    seed[r][c] = 1
                    img = reynolds(i, k, m, seed)
                    flat = [x for row in img for x in row]
                    images.append(flat)
                    if first is None and any(flat):
                        first = (r, c, img)
            mult = rank(images)
            if mult:
                channels.append((i, k, m))
                if mult > 1:
                    multiples.append((i, k, m, mult))
                # the first elementary seed with a nonzero group sum is equivariant: rho_m(h) C = C (rho_i(h) x rho_k(h)) for all h
                C = first[2]
                for h in range(24):
                    if mm(REP[m][h], C) != mm(C, kron(REP[i][h], REP[k][h])):
                        equivariant_bad += 1
                firsts[(i, k, m)] = first[:2]
                ones = [[1] * (DIM[i] * DIM[k]) for _ in range(DIM[m])]
                if not any(x for row in reynolds(i, k, m, ones) for x in row):
                    ones_zero.append((i, k, m))
            elif first is not None:
                first_missing.append((i, k, m))
print("channels:", len(channels), "; any multiplicity above 1:", multiples, "; nonzero sum where rank 0:", first_missing)
print("the first elementary seed with a nonzero group sum is equivariant under all 24 at every channel: failures", equivariant_bad)
print("one seed of all ones loses", len(ones_zero), "of", len(channels), ":", ", ".join(f"{i} x {k} -> {m}" for i, k, m in ones_zero))
print("the cross (T1 x T1 -> T2? or A2-twisted) among the lost:", ("T1", "T1", "T2") in ones_zero, ("T1", "T1", "T1") in ones_zero)
# the kinds' characters on the five classes: identity, third turns, face half turns, quarter turns, edge half turns
def trace(mat):
    return sum(mat[n][n] for n in range(len(mat)))
classes = {}
for n, (perm, m) in enumerate(turns):
    tr = trace(m)
    ab = sum(abs(m[i][i]) for i in IDX)  # fixed axes count (abs diagonal)
    kind = {3: "identity"}.get(tr)
    if kind is None:
        if tr == 0:
            kind = "third turns"
        elif tr == -1:
            kind = "face half turns"
        elif tr == 1:
            kind = "quarter turns"
        else:
            kind = "edge half turns"
    classes.setdefault((kind, tr), []).append(n)
# edge half turns have trace -1 as do face half turns: separate by the axes' permutation (edge: a transposition, sign -1)
cls = {"identity": [], "third turns": [], "face half turns": [], "quarter turns": [], "edge half turns": []}
for n, (perm, m) in enumerate(turns):
    tr = trace(m)
    s = perm_sign(perm)
    if tr == 3:
        cls["identity"].append(n)
    elif tr == 0:
        cls["third turns"].append(n)
    elif tr == -1 and s == 1:
        cls["face half turns"].append(n)
    elif tr == 1:
        cls["quarter turns"].append(n)
    else:
        cls["edge half turns"].append(n)
print("class sizes:", {k: len(v) for k, v in cls.items()})
for k in names:
    row = [trace(REP[k][v[0]]) for v in cls.values()]
    ok_const = all(trace(REP[k][n]) == trace(REP[k][v[0]]) for v in cls.values() for n in v)
    print(f"  {k}: {row} constant on classes: {ok_const}")


# the scale of the first nonzero group sum: its content (gcd of entries) against the channel's primitive tensor
from math import gcd
from functools import reduce


def content(img):
    return reduce(gcd, (abs(x) for row in img for x in row), 0)


def primitive(img):
    g = content(img)
    flat = [x // g for row in img for x in row]
    first = next(x for x in flat if x)
    return tuple(x if first > 0 else -x for x in flat)


spread = {}
firsts_content = {}
prim_same = True
for (i, k, m) in channels:
    contents, prims = [], set()
    first_c = None
    for r in range(DIM[m]):
        for c in range(DIM[i] * DIM[k]):
            seed = [[0] * (DIM[i] * DIM[k]) for _ in range(DIM[m])]
            seed[r][c] = 1
            img = reynolds(i, k, m, seed)
            if any(x for row in img for x in row):
                contents.append(content(img))
                prims.add(primitive(img))
                if first_c is None:
                    first_c = content(img)
    prim_same &= len(prims) == 1
    spread[(i, k, m)] = sorted(set(contents))
    firsts_content[(i, k, m)] = first_c
print("every nonzero seed of a channel gives the same primitive tensor up to sign:", prim_same)
multi = {ch: s for ch, s in spread.items() if len(s) > 1}
print("channels whose nonzero seeds give more than one content:", len(multi), "of", len(channels))
print("the first seed's content over the 43 channels:", sorted(set(firsts_content.values())))
ex = list(multi.items())[:4]
for ch, s in ex:
    print("  e.g.", " x ".join(ch[:2]), "->", ch[2], "contents of the nonzero seeds", s, "first seed", firsts_content[ch])


# the six Spokes' and the three axes' permutation characters against the five kinds (inner products over the 24)
spokes = [2 * sum(1 for i in IDX if m[i][i] == 1) for perm, m in turns]
axes = [sum(1 for i in IDX if perm[i] == i) for perm, m in turns]
for label, ch in (("six Spokes", spokes), ("three axes", axes)):
    parts = {k: Fraction(sum(ch[n] * trace(REP[k][n]) for n in range(24)), 24) for k in names}
    print(f"{label}: {', '.join(f'{k} x {v}' for k, v in parts.items() if v)}")
print("all channels with more than one content:", {" x ".join(ch[:2]) + " -> " + ch[2]: s for ch, s in multi.items()})
from collections import Counter
print("first seed's content by channel count:", dict(sorted(Counter(firsts_content.values()).items())))
