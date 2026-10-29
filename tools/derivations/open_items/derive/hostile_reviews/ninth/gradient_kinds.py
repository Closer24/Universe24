"""Probe: the gradient on a train of two kinds whose A1 is not first, and of a two-kind train's T1, and the lay's fine
tooth: files no test of 927071a14 holds, on which mutants N1, N3 and N4 (new_mutants.py) differ from the code.

1. trains [T1, A1] (part 1) and [T1]: the gradient of the first train's A1 (kind 1) dotted with the T1 train into the
   A1, against the load test's own naive sum (tests/test_the_tensor24_load.py naive, which reads the kind it is given).
2. the potential [A1, T1]: a gradient of its T1 (kind 1) must be refused, as the spin's is.
3. a gear laid with a fine tooth of 3 must leave r = 3 at its row and site.
usage: python -I gradient_kinds.py <worktree> <src dir to test (the worktree's src, or a mutant copy's)>"""

import inspect
import sys

WT, SRC = sys.argv[1], sys.argv[2]
sys.path[:0] = [SRC, WT]
import numpy as np  # noqa: E402

from tensor24.engine.contract import Plan, contract  # noqa: E402
from tensor24.main import made  # noqa: E402
from tensor24.runner.files import OPERANDS  # noqa: E402
from tensor24.runner.load import load  # noqa: E402
from tests.test_the_tensor24_load import naive, row  # noqa: E402

ks, c = made((8, 1, 1))
labels = tuple(name.upper() for name in ks._fields)
grad = OPERANDS.index("gradient")
u = {"trains": [{"name": "mixed", "kinds": ["T1", "A1"], "part": 1}, {"name": "spin", "kinds": ["T1"], "part": 1}],
     "couplings": [row(train=0, kind=1, operand=grad, with_train=1, target=0, target_kind=1, strength=3)]}
held, found = load(u, {"gears": []}, 8, ks, c)
rows = 3 + 1 + 3  # [T1, A1] on one gear, then [T1]
readings = np.random.default_rng(5).integers(-1 << 30, 1 << 30, ((len(OPERANDS) + 2) * rows, 8)).astype(object)
gears = [held.state[0]][: len(inspect.signature(contract).parameters) - 2]  # the gears' shape where contract takes it (after the ninth's changes)
same = held is not None and (contract(Plan(*held.plan), readings, *gears) == naive(u, c, readings, labels)).all()
print(f"1. a gradient of the A1 at kind 1 of [T1, A1]: named {found}; the plan equals the naive sum: {bool(same)}")

u2 = {"trains": [{"name": "potential", "kinds": ["A1", "T1"], "part": 2}, {"name": "spin", "kinds": ["T1"], "part": 1}],
      "couplings": [row(train=0, kind=1, operand=grad, with_train=1, target=1)]}
held2, found2 = load(u2, {"gears": []}, 8, ks, c)
print(f"2. a gradient of the potential's T1 (kind 1): refused {held2 is None}, named {found2}")

u3 = {"trains": u["trains"], "couplings": []}  # the gear's row 6: the spin's component 2, after the mixed train's 4 rows
held3, found3 = load(u3, {"gears": [[1, 2, 5, 7, 8, 3]]}, 8, ks, c)
a, b, r, *_ = held3.state
print(f"3. a gear laid with the fine tooth 3: a {a[6, 5]}, b {b[6, 5]}, r {r[6, 5]} (want 7, 8, 3)")
print("the code right on all three:", bool(same) and held2 is None and (a[6, 5], b[6, 5], r[6, 5]) == (7, 8, 3))
