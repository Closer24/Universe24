"""Stage 4 unchanged: the same random worlds run on 610fef782's engine ("old") and on 9e5233d7f's under neutral gearing ("new").

Usage: PYTHONPATH=<src of the engine> python -I stage4_alike.py old|new <worlds>
Prints one digest per world: every round's state and out, then the rewind to the start, entry by entry; the rd array
of the new engine is checked to stay 0 and left out of the digest, so the two digests compare the stage 4 fields alone.
"""

import hashlib
import sys

import numpy as np

from tensor24.engine import step
from tensor24.engine.state import State
from tensor24.runner.board import board

MODE, WORLDS = sys.argv[1], int(sys.argv[2])
if MODE == "new":
    from tensor24.engine.state import Gearing, Layout, Plan
else:
    from tensor24.engine.state import Layout


def wide(rng, size, bits):
    limbs = [rng.integers(0, 1 << 62, size).astype(object) << (62 * k) for k in range(bits // 62 + 1)]
    return sum(limbs) - (1 << (bits - 1))


def lay(nb, meshes, grip, w, rate, gamma):
    if MODE == "old":
        return Layout(nb, meshes, grip, w, rate, gamma)
    none = np.zeros(0, dtype=np.intp)
    return Layout(
        nb, meshes, grip.reshape(1, -1), Gearing(w, w, 1, 0, 1, 1), Plan(none, none, none.astype(object), none), rate, gamma
    )


def state(a, b, r, go, ph, c, tn):
    return State(a, b, r, go, ph, c, tn) if MODE == "old" else State(a, b, r, go, 0 * a, ph, c, tn)


def fields(s):
    s = tuple(s)
    if MODE == "new":
        assert not s[4].any(), "the drive's tooth moved under neutral gearing"
        s = s[:4] + s[5:]
    return [x.tolist() for x in s]


def one(seed):
    rng = np.random.default_rng(seed)
    shape = tuple(int(x) for x in rng.integers(1, 6, 3))
    nb, meshes = board(shape)
    n = nb.shape[1]
    rows = int(rng.integers(1, 5))
    gamma = int(rng.integers(1, 13))
    per_row = bool(rng.integers(0, 2))
    w = rng.integers(1, 40, size=(rows if per_row else 1, n)).astype(object)
    rate = rng.integers(0, gamma + 1, size=(1, n)).astype(object)
    rate[0, rng.integers(0, n)] = 0  # one stopped clock
    grip = rng.integers(-6, 7, size=3 * n).astype(object)
    layout = lay(nb, meshes, grip, w, rate, gamma)
    a, b = wide(rng, (rows, n), 300), wide(rng, (rows, n), 300)
    r = rng.integers(0, 1 << 30, size=(rows, n)).astype(object) % w
    go = rng.integers(0, 2, size=(rows, n)).astype(object)
    ph = rng.integers(0, gamma, size=(1, n)).astype(object)
    c = rng.integers(0, 3, size=(1, n)).astype(object)
    tn = c - rng.integers(0, 2, size=(1, n)).astype(object)
    s0 = state(a, b, r, go, ph, c, tn)
    s, rec = s0, []
    outs = []
    for _ in range(int(rng.integers(1, 9))):
        mask = rng.integers(0, 2, size=(1, n)).astype(object) if rng.integers(0, 3) else np.ones((1, n), dtype=object)
        s, out = step.tick(layout, s, mask)
        outs.append(out)
        rec.append(fields(s) + [x.tolist() for x in out])
    back = s
    for out in reversed(outs):
        back = step.untick(layout, back, out)
    rec.append(fields(back))
    exact = all(np.array_equal(x, y) for x, y in zip(back, s0, strict=True))
    ticked = sum(int(o[1].sum()) for o in outs)
    return hashlib.sha256(repr(rec).encode()).hexdigest()[:16], exact, ticked


for seed in range(WORLDS):
    digest, exact, ticked = one(seed)
    print(seed, digest, "exact" if exact else "NOT EXACT", ticked)
