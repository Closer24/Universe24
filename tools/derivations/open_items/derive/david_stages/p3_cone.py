"""David's probe: the cone in counts under past and under the hybrid lin, on the stage 3 engine.

usage: python3 -I p3_cone.py <worktree>/src
A change at site 0's now slot at count 0; two runs under one schedule (the counts do not depend on the gears).
For every site, the first count at which its now slot differs is compared with its Mesh distance from site 0:
the cone in counts holds where no site differs at a count below its distance. 20 seeds, rates parted, masks.
"""
import sys

sys.path.insert(0, sys.argv[1])
import numpy as np  # noqa: E402

from tensor24.algebra.carry import carry, choose, nonneg  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.engine.state import Layout, State  # noqa: E402

SIDE, GAMMA = 7, 9
obj = lambda x: np.asarray(x, dtype=object)  # noqa: E731



def layout_of(nb, grips6, w, rate, gamma):
    """The Layout of either head: one grip per Mesh read through the meshes table where the Layout holds it
    (81521e0f4 on), else a grip per Spoke; grips6 is read the same from the Mesh's two ends."""
    if "meshes" not in Layout._fields:
        return Layout(nb, grips6, w, rate, gamma)
    n = nb.shape[1]
    meshes = np.empty((6, n), dtype=int)
    grip = np.empty(3 * n, dtype=object)
    for axis in range(3):
        meshes[2 * axis] = axis * n + np.arange(n)
        meshes[2 * axis + 1] = axis * n + nb[2 * axis + 1]
        grip[axis * n + np.arange(n)] = grips6[2 * axis]
    return Layout(nb, meshes, grip, w, rate, gamma)


def grips(layout):
    """Each Spoke's grip, (6, N), on either head."""
    return layout.grip[layout.meshes] if "meshes" in Layout._fields else layout.grip

def board(side):
    xyz = np.indices((side,) * 3).reshape(3, -1)
    steps = [sign * axis for axis in np.eye(3, dtype=int) for sign in (1, -1)]
    return np.stack([np.ravel_multi_index(tuple((xyz + s[:, None]) % side), (side,) * 3) for s in steps]), xyz


def lin_pull(layout, s):
    nb, grip = layout.nb, grips(layout)
    a, b, _, _, _, c, tb, tn = s
    span = tn[:, nb] - tb[:, nb]
    line = b[:, nb] + carry((a[:, nb] - b[:, nb]) * (c[:, None, :] - tb[:, nb]), span, 0)[0]
    seen = choose(nonneg(c[:, None, :] - tn[:, nb]), a[:, nb], line)
    return ((seen - a[:, None, :]) * grip).sum(axis=1)


def run(read, seed, rounds=60):
    rng = np.random.default_rng(seed)
    nb, xyz = board(SIDE)
    n = SIDE**3
    dist = np.minimum(xyz, SIDE - xyz).sum(axis=0)
    w = obj(rng.integers(1, 20, size=(1, n)))
    rate = obj(rng.integers(1, GAMMA + 1, size=(1, n)))
    layout = layout_of(nb, obj(np.ones((6, n), dtype=int)), w, rate, GAMMA)
    a, b = obj(rng.integers(-99, 99, size=(1, n))), obj(rng.integers(-99, 99, size=(1, n)))
    r = obj(rng.integers(0, 1 << 20, size=(1, n))) % w
    go, ph = obj(rng.integers(0, 2, size=(1, n))), obj(rng.integers(0, GAMMA, size=(1, n)))
    zero = obj(np.zeros((1, n), dtype=int))
    u = State(a, b, r, go, ph, zero, zero - 1, zero)
    a2 = a.copy()
    a2[0, 0] += 10**6
    v = u._replace(a=a2)
    first = np.full(n, 10**9)
    saved = step.pull
    step.pull = read
    try:
        for _ in range(rounds):
            mask = obj(rng.integers(0, 2, size=(1, n)))
            u, _ = step.tick(layout, u, mask)
            v, _ = step.tick(layout, v, mask)
            differ = np.asarray(u.a[0] != v.a[0], dtype=bool) & (first == 10**9)
            # the now slot was written at count tn; the change is seen in a slot written at that count
            first[differ] = np.asarray(u.tn[0], dtype=int)[differ]
    finally:
        step.pull = saved
    early = (first < dist) & (dist > 0)
    return int(early.sum()), int((first < 10**9).sum())


for name, read in (("past", step.pull), ("hybrid lin", lin_pull)):
    early = reached = 0
    for seed in range(20):
        e, rch = run(read, seed)
        early, reached = early + e, reached + rch
    print(f"{name}: sites whose slot changed at a count below their Mesh distance: {early} of {reached} reached (20 seeds)")
