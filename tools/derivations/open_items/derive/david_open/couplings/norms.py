"""The 43 tables' invariant norms in the act's basis: C C^T = lambda I where Schur's lemma holds in that basis.

Each table C[m; i, k] (load.tables, made primitive by the gcd of its entries) is read as a matrix from the pairs
(i, k) to m, and C C^T is printed. Where the three kinds' matrices are orthogonal on the 24 (A1 and A2, T1 and T2: signed
permutations), Schur gives C C^T = lambda I. E's matrices are not orthogonal in the act's basis (e1 - e2, e2 - e3),
whose Gram matrix is [[2, -1], [-1, 2]], so every table through E but the ones whose norm the A1 leg fixes has no
scalar norm: E has no whole basis that the 24 permute.

The integrality point: the scalar norms are 1, 2, 3 and 10, and one strength for every table would scale each by
sqrt(Lambda / lambda); no integer k_t gives k_t^2 lambda_t one value for lambda_t = 1 and 2 at once (sqrt 2 is
irrational). So one Schur lambda for all 43 is no integer rule on the act's tables.

Usage: python3 -I norms.py <src of tensor24-review>
"""

import sys

import numpy as np

sys.path.insert(0, sys.argv[1])
from tensor24.engine import kinds as kinds_module  # noqa: E402
from tensor24 import main  # noqa: E402

held, tables = main.made((3, 3, 3))
_, weight = kinds_module.turns(kinds_module.axes(3))
labels = tuple(n.upper() for n in held._fields)
print("kinds", labels, "dims", tuple(k.shape[-1] for k in held), "turns weighed 1:", int(sum(weight)))
for lab, k in zip(labels, held):
    mats = [np.array(m, dtype=object) for m, wt in zip(k, weight) if wt]
    ortho = all((m.dot(m.T) == np.eye(m.shape[0], dtype=object)).all() for m in mats)
    print(f"  {lab}: orthogonal on the 24 in the act's basis: {ortho}")
plane = np.array([[1, -1, 0], [0, 1, -1]], dtype=object)
print("  E's basis (e1 - e2, e2 - e3), its Gram matrix:", plane.dot(plane.T).tolist())
count, scalars = 0, set()
for (i, k, m), c in sorted(tables.items()):
    c = np.array(c, dtype=object)
    if not c.any():
        continue
    count += 1
    flat = c.reshape(c.shape[0], -1)
    cct = flat.dot(flat.T)
    lam = cct[0, 0]
    scalar = (cct == lam * np.eye(c.shape[0], dtype=object)).all()
    if scalar:
        scalars.add(int(lam))
    print(f"  C[{labels[m]}; {labels[i]}, {labels[k]}]: "
          + (f"C C^T = {lam} I" if scalar else f"C C^T not scalar: {cct.tolist()}"))
print("tables not 0:", count, "; the scalar norms:", sorted(scalars))
both = [(a, b) for a in range(1, 200) for b in range(1, 200) if a * a == 2 * b * b]
print("integer k_1, k_2 with k_1^2 * 1 = k_2^2 * 2, for k up to 199:", both or "none")
