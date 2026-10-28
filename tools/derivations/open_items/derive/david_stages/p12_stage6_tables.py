"""David's probe of stage 6's tables (83a0b214a): the kinds and C as main.made builds them, against the groups.

usage: python3 -I p12_stage6_tables.py <worktree>/src
Checks on the engine's own kinds and the load's own tables, exact integers:
  (1) the weight picks 24 of the 216 candidates, and on them each kind is a representation (576 pairs);
  (2) the characters on the five classes and their orthonormality;
  (3) every C[i, k -> m] equivariant under the 24, nonzero exactly where the characters hold m in i x k (43);
  (4) every nonzero C primitive (its entries' gcd 1), and its sign: whether its first nonzero entry, in C's own
      index order, is positive; and whether that sign stays when the elementary seeds are tried in another order;
  (5) the dot (T1 x T1 -> A1) and the cross (T1 x T1 -> T1) as the plain dot and cross, up to their sign;
  (6) the sign fixed by the rule "the first nonzero entry, in C's own index order, positive": whether C then stands
      under the seeds in the reverse order and in 20 random orders, and which of the head's tables it turns over.
"""
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
negative, reordered, fixed_moved, turned = [], [], [], []
inv = K.kinds(K.inverse(matrix), axes)
rng = np.random.default_rng(12)


def primitive(seeds, order):
    """The first seed not 0 in the given order, its entries' gcd divided out, as the load does."""
    s = next(seeds[n] for n in order if seeds[n].any())
    g = load.common(s)
    return np.asarray([x // g for x in s])


def signed(c):
    """C with its first nonzero entry made positive."""
    first = next(int(x) for x in c.reshape(-1) if x)
    return c * (1 if first > 0 else -1)


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
    first = next(x for x in entries if x)
    label = f"{i}x{k}->{m}"
    if first < 0:
        negative.append(label)
    # the same projector, the elementary seeds tried in the reverse order and in 20 random orders
    seeds = K.projector(weight, reps[c], np.asarray(getattr(inv, held._fields[a])), np.asarray(getattr(inv, held._fields[b])))
    seeds = np.asarray(seeds).reshape(int(np.prod(t.shape)), -1).T
    orders = [list(range(len(seeds)))[::-1]] + [list(rng.permutation(len(seeds))) for _ in range(20)]
    tried = [primitive(seeds, order).reshape(t.shape) for order in orders]
    if not np.array_equal(tried[0], t):
        reordered.append(label)
    if any(not np.array_equal(signed(x), signed(t)) for x in tried):
        fixed_moved.append(label)
    if not np.array_equal(signed(t), t):
        turned.append(label)
fails["nonzero exactly on the channels"] = nonzero_ok
fails["equivariant"] = equi
fails["primitive"] = prim
print(f"channels held: {sum(1 for v in held_channels.values() if v)}; tables not 0: {sum(1 for t in tables.values() if np.asarray(t).any())}")
for k_, v in fails.items():
    print(f"{k_}: failures {v}")
print(f"the sign: {len(negative)} of the nonzero tables have a negative first entry ({', '.join(negative)})")
print(f"  the seeds in the reverse order turn {len(reordered)} of them over ({', '.join(reordered)})")
plain = [x for x in reordered if "E" not in x]
print(f"  of those, with no E (a stage 6 file can name them): {len(plain)} ({', '.join(plain)})")
print(f"the sign fixed by the first nonzero entry: the reverse order and 20 random orders move {len(fixed_moved)} of the 43;"
      f" the rule turns {len(turned)} of the head's tables over ({', '.join(turned)})")
dot = np.asarray(tables[(names.index('T1'), names.index('T1'), names.index('A1'))]).reshape(3, 3)
cross = np.asarray(tables[(names.index('T1'),) * 3])
eps = np.zeros((3, 3, 3), dtype=int)
for x, p, q in itertools.permutations(range(3)):
    eps[x, p, q] = 1 if (x, p, q) in ((0, 1, 2), (1, 2, 0), (2, 0, 1)) else -1
a2t1 = np.asarray(tables[(names.index('A2'), names.index('T1'), names.index('T2'))]).reshape(3, 3)
print("the dot:", "plain" if np.array_equal(dot, np.eye(3, dtype=int)) else "negated" if np.array_equal(dot, -np.eye(3, dtype=int)) else "other",
      "; the cross:", "plain" if np.array_equal(cross, eps) else "negated" if np.array_equal(cross, -eps) else "other",
      "; A2 x T1 -> T2:", "plain" if np.array_equal(a2t1, np.eye(3, dtype=int)) else "negated" if np.array_equal(a2t1, -np.eye(3, dtype=int)) else "other")
