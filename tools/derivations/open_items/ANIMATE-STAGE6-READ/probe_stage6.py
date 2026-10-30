"""Stage 6 read independently (Animate): the 24, the five kinds, the 125 tables, the plan and the contraction.

usage: python -I probe_stage6.py <worktree at the head>   (run here at fc8c810ff: probe_stage6.txt)

Nothing here is taken from the head but what is checked: the 24 are made by closing two quarter turns, A2 is the sign of
the permutation a turn makes of the cube's four body diagonals (S4's sign), the characters are checked against O's table
written from the literature, the multiplicities come from the characters, and each table the head makes is checked for
equivariance on the 24, for being 0 exactly off the channels, primitive with its first entry positive, and equal to the
table made here by averaging every seed over the 24. The plan is contracted on random universes against a naive sum
written from the plan's own words (TENSOR24_PLAN.md: the part runs fastest; value, the gradient's three planes, pull).
"""

import itertools
import random
import sys
from fractions import Fraction
from math import gcd
from pathlib import Path

import numpy as np

WT = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(WT / "src"))
from tensor24 import main  # noqa: E402
from tensor24.engine import contract as C  # noqa: E402
from tensor24.engine import kinds as K  # noqa: E402
from tensor24.runner import load as L  # noqa: E402

# 1. The 24 by closure of two quarter turns.
RZ = ((0, -1, 0), (1, 0, 0), (0, 0, 1))
RX = ((1, 0, 0), (0, 0, -1), (0, 1, 0))


def mul(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)) for i in range(3))


group = {((1, 0, 0), (0, 1, 0), (0, 0, 1))}
frontier = list(group)
while frontier:
    g = frontier.pop()
    for h in (RZ, RX):
        n = mul(g, h)
        if n not in group:
            group.add(n)
            frontier.append(n)
G = sorted(group)
assert len(G) == 24, len(G)

matrix, weight = K.turns(K.axes(3))
head24 = sorted(
    tuple(tuple(int(x) for x in row) for row in m) for m, w in zip(matrix, weight, strict=True) if w == 1
)
assert head24 == G, "the head's weight-1 candidates are not the 24"
assert set(int(w) for w in weight) == {0, 1}
print(
    f"1. the 24: closure of two quarter turns gives {len(G)}; the head's weight picks the same {len(head24)} of {len(weight)}"
)

# 2. A2 as S4's sign on the four body diagonals; the classes; O's character table.
DIAGS = [(1, 1, 1), (1, 1, -1), (1, -1, 1), (-1, 1, 1)]


def line_of(v):
    return DIAGS.index(v) if v in DIAGS else DIAGS.index(tuple(-x for x in v))


def s4_sign(g):
    perm = [line_of(tuple(sum(g[i][k] * d[k] for k in range(3)) for i in range(3))) for d in DIAGS]
    sign, seen = 1, set()
    for start in range(4):
        if start in seen:
            continue
        length, j = 0, start
        while j not in seen:
            seen.add(j)
            j = perm[j]
            length += 1
        sign *= -1 if length % 2 == 0 else 1
    return sign


def cls(g):
    tr = g[0][0] + g[1][1] + g[2][2]
    if tr == 3:
        return "E"
    if tr == 0:
        return "8C3"
    if tr == 1:
        return "6C4"
    diagonal = all(g[i][j] == 0 for i in range(3) for j in range(3) if i != j)
    return "3C2" if diagonal else "6C2'"


TABLE = {  # O's characters: E, 8C3, 3C2, 6C4, 6C2'
    "A1": (1, 1, 1, 1, 1),
    "A2": (1, 1, 1, -1, -1),
    "E": (2, -1, 2, 0, 0),
    "T1": (3, 0, -1, 1, -1),
    "T2": (3, 0, -1, -1, 1),
}
CLASSES = ("E", "8C3", "3C2", "6C4", "6C2'")
counts = {c: sum(cls(g) == c for g in G) for c in CLASSES}
assert counts == {"E": 1, "8C3": 8, "3C2": 3, "6C4": 6, "6C2'": 6}, counts

held = K.kinds(matrix)
names = ("A1", "A2", "E", "T1", "T2")
index = {tuple(tuple(int(x) for x in row) for row in m): n for n, m in enumerate(matrix)}
rho = {name: {g: np.array(held[k][index[g]], dtype=object) for g in G} for k, name in enumerate(names)}
for name in names:
    for g in G:
        for h in G:
            assert (rho[name][mul(g, h)] == rho[name][g].dot(rho[name][h])).all(), (name, g, h)
    chars = {cls(g): int(np.trace(rho[name][g])) for g in G}
    assert tuple(chars[c] for c in CLASSES) == TABLE[name], (name, chars)
for g in G:
    assert int(rho["A2"][g][0, 0]) == s4_sign(g)
    assert (rho["T1"][g] == np.array(g, dtype=object)).all()
    assert (rho["T2"][g] == s4_sign(g) * np.array(g, dtype=object)).all()
    assert int(rho["A1"][g][0, 0]) == 1
print(
    "2. the five kinds: each a representation on all 576 pairs, characters O's table at the five classes;"
)
print("   A1 = 1, A2 = S4's sign on the body diagonals, T1 = the turn, T2 = A2 T1 at all 24")


# 3. Multiplicities from the characters; the channels.
def mult(i, k, m):
    total = sum(TABLE[i][n] * TABLE[k][n] * TABLE[m][n] * counts[c] for n, c in enumerate(CLASSES))
    return Fraction(total, 24)


mults = {(i, k, m): mult(i, k, m) for i in names for k in names for m in names}
assert all(v in (0, 1) for v in mults.values())
channels = sum(v == 1 for v in mults.values())
print(f"3. multiplicities from the characters: every one 0 or 1, the channels {channels}")

# 4. The head's tables: equivariant, nonzero exactly on the channels, primitive, first entry positive, and equal to the
#    table made here from every seed averaged over the 24.
_, tables = main.made((5, 5, 5))
dims = {name: rho[name][G[0]].shape[0] for name in names}


def inv(g):
    return tuple(tuple(g[j][i] for j in range(3)) for i in range(3))


def mine(i, k, m):
    """The first seed whose average over the 24 is not 0, primitive with its first entry positive (my own loop)."""
    for y, p, q in itertools.product(range(dims[m]), range(dims[i]), range(dims[k])):
        avg = np.zeros((dims[m], dims[i], dims[k]), dtype=object)
        for g in G:
            gi = inv(g)
            avg += np.einsum("x,a,b->xab", rho[m][g][:, y], rho[i][gi][p, :], rho[k][gi][q, :])
        flat = [int(x) for x in avg.flatten()]
        if any(flat):
            d = 0
            for x in flat:
                d = gcd(d, x)
            out = avg // d
            first = next(x for x in out.flatten() if x)
            return out if first > 0 else -out
    return np.zeros((dims[m], dims[i], dims[k]), dtype=object)


bad = []
for (ni, nk, nm), table in sorted(tables.items()):
    i, k, m = names[ni], names[nk], names[nm]
    t = np.array(table, dtype=object)
    nonzero = bool(t.any())
    if nonzero != (mults[(i, k, m)] == 1):
        bad.append(("channel", i, k, m))
    for g in G:
        left = np.einsum("xy,yab->xab", rho[m][g], t)
        right = np.einsum("xpq,pa,qb->xab", t, rho[i][g], rho[k][g])
        if not (left == right).all():
            bad.append(("equivariance", i, k, m))
            break
    if nonzero:
        d = 0
        for x in t.flatten():
            d = gcd(d, int(x))
        first = next(int(x) for x in t.flatten() if x)
        if d != 1 or first <= 0:
            bad.append(("primitive", i, k, m, d, first))
    if "E" not in (i, k, m) and not (mine(i, k, m) == t).all():
        bad.append(("differs from mine", i, k, m))
print(f"4. the head's 125 tables: {len(bad)} departures {bad[:5]}")
print(
    f"   nonzero at {sum(bool(np.array(t, dtype=object).any()) for t in tables.values())}, the channels {channels}"
)
eps = np.zeros((3, 3, 3), dtype=object)
for a, b, c in itertools.permutations(range(3)):
    eps[a, b, c] = np.linalg.det(np.eye(3)[[a, b, c]]).round().astype(int)
t1 = names.index("T1")
dot = np.array(tables[(t1, t1, names.index("A1"))], dtype=object)
cross = np.array(tables[(t1, t1, t1)], dtype=object)
a2t1 = np.array(tables[(names.index("A2"), t1, names.index("T2"))], dtype=object)
print(
    "   the dot is delta:",
    (dot[0] == np.eye(3, dtype=int)).all(),
    "| the cross is epsilon (u x v):",
    (cross == eps).all(),
    "| A2 x T1 -> T2 is delta:",
    (a2t1[:, 0, :] == np.eye(3, dtype=int)).all(),
)

# 5. The plan contracted against a naive sum from the plan's words, on random universes.
OPS = ("value", "gradient", "pull")
labels = tuple(n.upper() for n in held._fields)


def universe(rng):
    trains = []
    for _ in range(rng.randint(1, 4)):
        kinds = [rng.choice(("A1", "A2", "T1", "T2")) for _ in range(rng.randint(1, 3))]
        trains.append({"kinds": kinds, "part": rng.choice((1, 2))})
    couplings = []
    for _ in range(rng.randint(1, 8)):
        row = []
        for _side in range(2):
            t = rng.randrange(len(trains))
            k = rng.randrange(len(trains[t]["kinds"]))
            p = rng.randrange(trains[t]["part"])
            ops = [0, 2] + ([1] if trains[t]["kinds"][k] == "A1" else [])
            row += [t, k, p, rng.choice(ops)]
        t = rng.randrange(len(trains))
        row += [t, rng.randrange(len(trains[t]["kinds"])), rng.randrange(trains[t]["part"])]
        row.append(rng.choice((1, -1)) * rng.randrange(1, 2**70))
        couplings.append(row)
    return trains, couplings


def naive(trains, couplings, readings, sites):
    """J from the plan's words: rows by train, kind, component, part fastest; planes value, gradient x y z, pull."""
    starts, rows = [], 0
    for t in trains:
        starts.append(rows)
        rows += sum(dims[k] for k in t["kinds"]) * t["part"]

    def row(t, k, c, p):
        tr = trains[t]
        return starts[t] + (sum(dims[x] for x in tr["kinds"][:k]) + c) * tr["part"] + p

    def side(t, k, p, o):
        kind = trains[t]["kinds"][k]
        if o == 1:  # the gradient: a T1 of the A1's three planes
            return "T1", [readings[(1 + axis) * rows + row(t, k, 0, p)] for axis in range(3)]
        plane = 0 if o == 0 else 4
        return kind, [readings[plane * rows + row(t, k, c, p)] for c in range(dims[kind])]

    J = [[0] * sites for _ in range(rows)]
    for t, k, p, o, t2, k2, p2, o2, T, TK, TP, s in couplings:
        a, one = side(t, k, p, o)
        b, two = side(t2, k2, p2, o2)
        m = trains[T]["kinds"][TK]
        table = np.array(tables[(names.index(a), names.index(b), names.index(m))], dtype=object)
        for x in range(dims[m]):
            for y in range(dims[a]):
                for z in range(dims[b]):
                    if table[x, y, z]:
                        for site in range(sites):
                            J[row(T, TK, x, TP)][site] += (
                                s * int(table[x, y, z]) * one[y][site] * two[z][site]
                            )
    return J, rows


rng = random.Random(20261029)
runs, terms, refused = 0, 0, 0
for _ in range(300):
    trains, couplings = universe(rng)
    held_trains, found = L.trains_of(trains, labels, tuple(dims[n] for n in names))
    assert not found, found
    plan, named = L.plan(couplings, held_trains, tables, labels, 3)
    sites = rng.randint(1, 4)
    rows = sum(t.rows() for t in held_trains)
    readings = [[rng.randrange(-(2**66), 2**66) for _ in range(sites)] for _ in range(7 * rows)]
    want, rows_naive = naive(trains, couplings, readings, sites)
    assert rows == rows_naive
    if named:
        refused += 1  # a channel the 24 forbid: the load names it; the naive sum gives it no term either
    got = C.contract(
        C.Plan(*plan), np.array(readings, dtype=object), np.zeros((rows, sites), dtype=np.int64)
    )
    assert got.dtype == object
    assert [[int(v) for v in r] for r in got] == want
    runs += 1
    terms += len(plan[0])
print(
    f"5. the plan contracted equals the naive sum on {runs} random universes ({terms} terms, strengths and readings"
)
print(
    f"   past 64 bits, int64 gears given; {refused} universes hold a forbidden channel, named by the load)"
)
