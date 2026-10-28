"""David's probe: T S T = S^-1 on the board under the probe's lin of derive/asynchronous_read, and under past.

usage: python3 -I p8_lin_reversal.py <worktree>/src
T on every gear: slots exchanged, w - 1 - r, the going advanced; one synchronous round; T again; against untick's
gears (untick undoes past; for lin the round is run back by T, so the check is that T S T S returns the start).
30 seeds, side 5, two gears, rates parted (and, as the control, every dial at the full rate).
"""
import sys

sys.path.insert(0, sys.argv[1])
import numpy as np  # noqa: E402

from tensor24.algebra.carry import carry, choose, nonneg  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.engine.state import Layout, State  # noqa: E402

GAMMA = 9
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


def state_of(**fields):
    """The State of either head: with the before slot's time tb where the State holds it (to 0970b0deb), else without
    (13672be1e on, the out carrying the replaced now-slot time)."""
    return State(**{key: value for key, value in fields.items() if key in State._fields})


def times_of(s):
    """The slots' times a State holds, to carry onto another of the same head."""
    return {key: getattr(s, key) for key in ("tb", "tn") if key in State._fields}

def board(side):
    xyz = np.indices((side,) * 3).reshape(3, -1)
    steps = [sign * axis for axis in np.eye(3, dtype=int) for sign in (1, -1)]
    return np.stack([np.ravel_multi_index(tuple((xyz + s[:, None]) % side), (side,) * 3) for s in steps])


def lin_pull(layout, s):
    nb, grip = layout.nb, grips(layout)
    a, b, _, _, _, c, tb, tn = s
    span = tn[:, nb] - tb[:, nb]
    line = b[:, nb] + carry((a[:, nb] - b[:, nb]) * (c[:, None, :] - tb[:, nb]), span, 0)[0]
    seen = choose(nonneg(c[:, None, :] - tn[:, nb]), a[:, nb], line)
    return ((seen - a[:, None, :]) * grip).sum(axis=1)


def T(layout, s):
    return s._replace(a=s.b, b=s.a, r=layout.w - 1 - s.r, go=1 - s.go)


def trial(read, rates, seed):
    rng = np.random.default_rng(seed)
    nb, n = board(5), 125
    w = obj(rng.integers(1, 20, size=(2, n)))
    rate = obj(rng.integers(1, GAMMA + 1, size=(1, n))) if rates == "parted" else obj(np.full((1, n), GAMMA))
    layout = layout_of(nb, obj(np.ones((6, n), dtype=int)), w, rate, GAMMA)
    a, b = obj(rng.integers(-10**5, 10**5, size=(2, n))), obj(rng.integers(-10**5, 10**5, size=(2, n)))
    r = obj(rng.integers(0, 1 << 20, size=(2, n))) % w
    go, ph = obj(rng.integers(0, 2, size=(2, n))), obj(rng.integers(0, GAMMA, size=(1, n)))
    zero = obj(np.zeros((1, n), dtype=int))
    s = state_of(a=a, b=b, r=r, go=go, ph=ph, c=zero, tb=zero - 1, tn=zero)
    ones = obj(np.ones((1, n), dtype=int))
    saved = step.pull
    step.pull = read
    try:
        for _ in range(6):
            s, _ = step.tick(layout, s, ones)
        s1, _ = step.tick(layout, s, ones)
        # the reversed round at the same counts and slots' times, every dial's phase as at the start
        t1, _ = step.tick(layout, T(layout, s1)._replace(c=s.c, ph=s.ph, **times_of(s)), ones)
        rev = T(layout, t1)
    finally:
        step.pull = saved
    return all(np.array_equal(x, y) for x, y in zip((rev.a, rev.b, rev.r), (s.a, s.b, s.r)))


for name, read in (("past", step.pull), ("lin", lin_pull)):
    if name == "lin" and "tb" not in State._fields:
        print("lin : not run, the State holds no tb (13672be1e on), and lin reads it")
        continue
    for rates in ("equal", "parted"):
        held = sum(trial(read, rates, 300 + k) for k in range(30))
        print(f"{name:4s}, dials {rates:6s}: T S T returns the start in {held} of 30")
