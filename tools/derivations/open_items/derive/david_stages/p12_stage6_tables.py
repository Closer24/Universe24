"""David's probe of stage 6's tables (83a0b214a, 3fbbd1cd0): the kinds and C as main.made builds them, against the groups.

usage: python3 -I p12_stage6_tables.py <worktree>/src
Checks on the engine's own kinds and the load's own tables, exact integers:
  (1) the weight picks 24 of the 216 candidates, and on them each kind is a representation (576 pairs);
  (2) the characters on the five classes and their orthonormality;
  (3) every C[i, k -> m] equivariant under the 24, nonzero exactly where the characters hold m in i x k (43);
  (4) every nonzero C primitive (its entries' gcd 1), and its sign: whether its first nonzero entry, in C's own
      index order (the target, then the two sides), is positive;
  (5) the dot (T1 x T1 -> A1), the cross (T1 x T1 -> T1) and A2 x T1 -> T2 as the plain ones, up to their sign;
  (6) the order of the seeds: the head's own load.tables run again with a projector whose elementary seeds come in
      the reverse order, and in 20 random orders: which tables move;
  (7) the rule "the first nonzero entry positive" laid on top: which of the head's tables it turns over, and whether
      the tables of every order then agree.
"""
import inspect
import itertools
import sys
from fractions import Fraction
from math import gcd

sys.path.insert(0, sys.argv[1])
import numpy as np  # noqa: E402

from tensor24 import main  # noqa: E402
from tensor24.engine import kinds as K  # noqa: E402
from tensor24.runner import load  # noqa: E402

held, tables = main.made((3, 3, 3))
axes = K.axes(3)
matrix, weight = K.turns(axes)
group = [n for n in range(len(weight)) if weight[n] == 1]
names = [f.upper() for f in held._fields]
reps = [np.asarray(getattr(held, f)) for f in held._fields]
fails = {}
fails["24"] = int(len(group) != 24 or len(weight) != 216)


def key(m):
    return tuple(int(x) for x in np.asarray(m).reshape(-1))


index = {key(matrix[n]): n for n in group}
pairs = 0
bad = 0
for g in group:
    for h in group:
        gh = index[key(np.asarray(matrix[g]).dot(np.asarray(matrix[h])))]
        for r in reps:
            pairs += 1
            bad += not np.array_equal(np.asarray(r[g]).dot(np.asarray(r[h])), np.asarray(r[gh]))
fails["representation"] = bad


def trace(m):
    return int(sum(np.asarray(m)[i, i] for i in range(np.asarray(m).shape[0])))


chi = {names[n]: [trace(reps[n][g]) for g in group] for n in range(5)}
fails["orthonormal"] = sum(
    sum(x * y for x, y in zip(chi[a], chi[b])) != (24 if a == b else 0) for a in names for b in names
)
held_channels = {}
for i, k, m in itertools.product(names, repeat=3):
    n = Fraction(sum(chi[i][g] * chi[k][g] * chi[m][g] for g in range(24)), 24)
    held_channels[(i, k, m)] = n
nonzero_ok = equi = prim = 0
negative = []


def kinds_of(matrices):
    """The five kinds on each matrix, on either head: the unit passed where kinds takes it (to 91226e796), else made
    inside (927071a14 on)."""
    if len(inspect.signature(K.kinds).parameters) > 1:
        return K.kinds(matrices, axes)
    return K.kinds(matrices)


inv = kinds_of(K.inverse(matrix))
rng = np.random.default_rng(12)


def ordered(orders):
    """The projector with its elementary seeds (the last three indices, flattened) taken in the given orders by count."""

    def projector(weight, m, i, k):
        p = np.asarray(K.projector(weight, m, i, k))
        n = int(np.prod(p.shape[:3]))
        return p.reshape(n, n)[:, orders(n)].reshape(p.shape)

    return projector


def signed(c):
    """C with its first nonzero entry made positive (C 0 left as it is)."""
    first = next((int(x) for x in np.asarray(c).reshape(-1) if x), 1)
    return np.asarray(c) * (1 if first > 0 else -1)


def label(key):
    return f"{names[key[0]]}x{names[key[1]]}->{names[key[2]]}"


reverse = load.tables(held, inv, weight, ordered(lambda n: np.arange(n)[::-1]))
randoms = []
for _ in range(20):
    perms = {}
    randoms.append(load.tables(held, inv, weight, ordered(lambda n: perms.setdefault(n, rng.permutation(n)))))
moved_reverse = [label(key) for key in tables if not np.array_equal(reverse[key], tables[key])]
moved_any = [label(key) for key in tables if any(not np.array_equal(r[key], tables[key]) for r in [reverse, *randoms])]
turned = [label(key) for key in tables if not np.array_equal(signed(tables[key]), tables[key])]
signed_moved = [
    label(key) for key in tables if any(not np.array_equal(signed(r[key]), signed(tables[key])) for r in [reverse, *randoms])
]
for (a, b, c), table in tables.items():
    i, k, m = names[a], names[b], names[c]
    t = np.asarray(table)
    nonzero = bool(t.any())
    nonzero_ok += nonzero != bool(held_channels[(i, k, m)])
    if not nonzero:
        continue
    for g in group:
        rm, ri, rk = (np.asarray(reps[x][g]) for x in (c, a, b))
        # C(ri u, rk v) = rm C(u, v) for all u, v: as tensors, rm C = C (ri x rk)
        lhs = np.einsum("xy,yab->xab", rm, t)
        rhs = np.einsum("xpq,pa,qb->xab", t, ri, rk)
        equi += not np.array_equal(lhs, rhs)
    entries = [int(x) for x in t.reshape(-1)]
    prim += gcd(*[abs(x) for x in entries if x]) != 1
    if next(x for x in entries if x) < 0:
        negative.append(f"{i}x{k}->{m}")
fails["nonzero exactly on the channels"] = nonzero_ok
fails["equivariant"] = equi
fails["primitive"] = prim
print(f"channels held: {sum(1 for v in held_channels.values() if v)}; tables not 0: {sum(1 for t in tables.values() if np.asarray(t).any())}")
for k_, v in fails.items():
    print(f"{k_}: failures {v}")
print(f"the sign: {len(negative)} of the nonzero tables have a negative first entry ({', '.join(negative)})")
plain = [x for x in moved_reverse if "E" not in x]
print(f"the order: the seeds in the reverse order move {len(moved_reverse)} tables ({', '.join(moved_reverse)});"
      f" {len(plain)} of them with no E ({', '.join(plain)})")
print(f"  the reverse order and 20 random orders move {len(moved_any)} tables in all")
print(f"the rule, the first nonzero entry positive, laid on top: it turns {len(turned)} of the head's tables over"
      f" ({', '.join(turned)}); under it the 21 orders move {len(signed_moved)}")
dot = np.asarray(tables[(names.index('T1'), names.index('T1'), names.index('A1'))]).reshape(3, 3)
cross = np.asarray(tables[(names.index('T1'),) * 3])
eps = np.zeros((3, 3, 3), dtype=int)
for x, p, q in itertools.permutations(range(3)):
    eps[x, p, q] = 1 if (x, p, q) in ((0, 1, 2), (1, 2, 0), (2, 0, 1)) else -1
a2t1 = np.asarray(tables[(names.index('A2'), names.index('T1'), names.index('T2'))]).reshape(3, 3)
print("the dot:", "plain" if np.array_equal(dot, np.eye(3, dtype=int)) else "negated" if np.array_equal(dot, -np.eye(3, dtype=int)) else "other",
      "; the cross:", "plain" if np.array_equal(cross, eps) else "negated" if np.array_equal(cross, -eps) else "other",
      "; A2 x T1 -> T2:", "plain" if np.array_equal(a2t1, np.eye(3, dtype=int)) else "negated" if np.array_equal(a2t1, -np.eye(3, dtype=int)) else "other")
