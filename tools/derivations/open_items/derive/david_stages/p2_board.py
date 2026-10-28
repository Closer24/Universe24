"""David's probe of stages 2 and 3 (engine/step.py, mesh.py) on the review branch's own functions.

usage: python3 -I p2_board.py <worktree>/src
Exact integers (Python ints in object arrays). Boards 5 x 5 x 5 (the frame's side) and 4 x 4 x 4, teeth 1..19 per gear
(both parities), goings both, rates 0..Gamma with one clock stopped:
  (a) the rewind: untick after tick returns the state, 30 seeds x 30 rounds under random masks;
  (b) the counts: under every schedule two neighbours' counts differ by at most 1, and k is 0 or 1;
  (c) the cone in rounds: a change at one site leaves every site at Mesh distance > t unchanged after t rounds,
      synchronous and under masks (past); the cone in counts, finer, is p3_cone.py;
  (d) T S T = S^-1 on the whole board where every dial is at the full rate: T on every gear (slots exchanged,
      w-1-r, the going advanced), one synchronous round, T again, equals untick, 30 seeds;
      with the rates parted the same check fails under past (the price item (u) names);
  (e) Sofer's promise: a rate of twice the full rate gives k = 2 somewhere (the bit read as a bit fails).
"""
import sys

sys.path.insert(0, sys.argv[1])
import numpy as np  # noqa: E402

from tensor24.engine import step  # noqa: E402
from tensor24.engine.state import Layout, State  # noqa: E402

GAMMA = 9



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
    return np.stack([np.ravel_multi_index(tuple((xyz + s[:, None]) % side), (side,) * 3) for s in steps]), xyz


def world(seed, side=5, rates="parted", gears=2):
    rng = np.random.default_rng(seed)
    nb, xyz = board(side)
    n = side**3
    obj = lambda x: np.asarray(x, dtype=object)  # noqa: E731
    w = obj(rng.integers(1, 20, size=(gears, n)))
    if rates == "parted":
        rate = obj(rng.integers(0, GAMMA + 1, size=(1, n)))
        rate[0, 3] = 0
    else:
        rate = obj(np.full((1, n), GAMMA))
    grip = obj(rng.integers(1, 5, size=(6, n)))
    # the grip read the same from both ends: grip at (x, +j) equals grip at (x + j, -j)
    for j in (0, 2, 4):
        grip[j + 1] = grip[j][nb[j + 1]]
    layout = layout_of(nb, grip, w, rate, GAMMA)
    a = obj(rng.integers(-10**6, 10**6, size=(gears, n)))
    b = obj(rng.integers(-10**6, 10**6, size=(gears, n)))
    r = obj(rng.integers(0, 1 << 30, size=(gears, n))) % w
    go = obj(rng.integers(0, 2, size=(gears, n)))
    ph = obj(rng.integers(0, GAMMA, size=(1, n)))
    zero = obj(np.zeros((1, n), dtype=int))
    return layout, state_of(a=a, b=b, r=r, go=go, ph=ph, c=zero, tb=zero - 1, tn=zero), rng, xyz


def same(s, t):
    return all(np.array_equal(np.asarray(x, dtype=object), np.asarray(y, dtype=object)) for x, y in zip(s, t))


fails = {"rewind": 0, "counts": 0, "kbit": 0, "cone_past": 0, "tst_equal": 0}
cases = {"rewind": 0, "cone": 0, "tst": 0}
for seed in range(30):
    layout, s, rng, _ = world(seed)
    outs, states = [], [s]
    for _ in range(30):
        mask = np.asarray(rng.integers(0, 2, size=(1, s.c.shape[1])), dtype=object)
        s, out = step.tick(layout, s, mask)
        outs.append(out)
        states.append(s)
        c = np.asarray(s.c[0], dtype=object)
        fails["counts"] += int(any(abs(c[layout.nb[j]] - c).max() > 1 for j in range(6)))
        fails["kbit"] += int(not set(np.asarray(out.k).ravel().tolist()) <= {0, 1})
    for i in range(30, 0, -1):
        back = step.untick(layout, states[i], outs[i - 1])
        cases["rewind"] += 1
        fails["rewind"] += not same(back, states[i - 1])

# (c) the cone, in counts: perturb site 0's now slot of gear 0, compare with the unperturbed run
for seed in range(10):
    for masked in (False, True):
        layout, s, rng, xyz = world(100 + seed)
        dist = np.minimum(xyz, 5 - xyz).sum(axis=0)  # L1 distance on the torus from site 0
        a2 = s.a.copy()
        a2[0, 0] = a2[0, 0] + 1000
        s2 = s._replace(a=a2)
        u, v = s, s2
        for t in range(1, 7):
            mask = (np.asarray(rng.integers(0, 2, size=(1, s.c.shape[1])), dtype=object) if masked
                    else np.asarray(np.ones((1, s.c.shape[1]), dtype=int), dtype=object))
            u, _ = step.tick(layout, u, mask)
            v, _ = step.tick(layout, v, mask)
            far = dist > t
            cases["cone"] += 1
            fails["cone_past"] += int(not (np.array_equal(u.a[:, far], v.a[:, far]) and np.array_equal(u.b[:, far], v.b[:, far])))


# (d) T S T = S^-1 on the whole board
def T(layout, s):
    w = layout.w
    return s._replace(a=s.b, b=s.a, r=w - 1 - s.r, go=1 - s.go)


tst_parted_fail = 0
for seed in range(30):
    for rates in ("equal", "parted"):
        layout, s, rng, _ = world(200 + seed, rates=rates)
        ones = np.asarray(np.ones((1, s.c.shape[1]), dtype=int), dtype=object)
        # run a few rounds first so that the slots' times are the run's own
        for _ in range(5):
            s, _ = step.tick(layout, s, ones)
        s1, out = step.tick(layout, s, ones)
        back = step.untick(layout, s1, out)
        # T, one round, T: compare the gears with untick's
        t1, _ = step.tick(layout, T(layout, s1)._replace(c=s.c, **times_of(s)), ones)
        rev = T(layout, t1)
        ok = all(np.array_equal(x, y) for x, y in zip((rev.a, rev.b, rev.r, rev.go), (back.a, back.b, back.r, back.go)))
        if rates == "equal":
            cases["tst"] += 1
            fails["tst_equal"] += not ok
        else:
            tst_parted_fail += not ok

# (e) Sofer's promise
layout, s, rng, _ = world(7)
rate = layout.rate.copy()
rate[0, 0] = 2 * GAMMA
layout2 = layout._replace(rate=rate)
ks = set()
for _ in range(5):
    s, out = step.tick(layout2, s, np.asarray(np.ones((1, s.c.shape[1]), dtype=int), dtype=object))
    ks |= set(np.asarray(out.k).ravel().tolist())

print(f"(a) the rewind: untick after tick returns the state in {cases['rewind'] - fails['rewind']} of {cases['rewind']} rounds (30 seeds x 30 rounds, masks, rates parted, one clock stopped)")
print(f"(b) neighbours' counts more than 1 apart in {fails['counts']} of 900 rounds; k outside {{0, 1}} in {fails['kbit']} of 900")
print(f"(c) the cone in rounds (past): a change reached beyond t Meshes after t rounds in {fails['cone_past']} of {cases['cone']} checks")
print(f"(d) T S T = S^-1 on the board, every dial at the full rate: {cases['tst'] - fails['tst_equal']} of {cases['tst']}; with the rates parted (past): fails on {tst_parted_fail} of 30")
print(f"(e) one clock at twice the full rate: k takes {sorted(ks)}")
