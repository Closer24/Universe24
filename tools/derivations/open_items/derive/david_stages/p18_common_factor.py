"""David's probe for the Boss's 6486246054 item 1: is stage 7a's act the same when W, W+ and s carry one common factor?

usage: python3 -I p18_common_factor.py <tensor24 worktree>/src
At the vacuum under the ruler, light's coefficients are the head's times Gamma^3 alike (W = T Gamma^4 and s = Gamma^4
for T Gamma and Gamma). On 7a's own step: a world at (W, W+, s) against the same world at (L W, L W+, L s), the grips
and the source's teeth unchanged, the fine tooth mapped by r' = L (r - home(W, go)) + home(L W, go). Exact integers:
  (1) the notches a and b and the dial, equal at every round, and the fine tooth mapped at every round;
  (2) the scaled world run back to its own start;
  (3) the same with no map, the fine tooth laid at the scaled home instead of mapped, for the size of the miss.
"""
import sys

sys.path.insert(0, sys.argv[1])
import numpy as np  # noqa: E402

from tensor24.algebra.carry import home  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.engine.state import Gearing, Layout, Plan, State  # noqa: E402

GAMMA = 9


def board(shape):
    xyz, sides = np.indices(shape).reshape(3, -1), np.array(shape)[:, None]
    steps = [sign * axis for axis in np.eye(3, dtype=int) for sign in (1, -1)]
    return np.stack([np.ravel_multi_index(tuple((xyz + s[:, None]) % sides), shape) for s in steps])


def meshes_of(nb):
    axes, n = np.arange(len(nb)) // 2, nb.shape[1]
    own, theirs = axes[:, None] * n + np.arange(n)[None, :], axes[:, None] * n + nb
    return np.where((np.arange(len(nb)) % 2 == 0)[:, None], own, theirs)


def obj(x):
    return np.asarray(x, dtype=object)


def worlds(seed, scale, mapped=True, rounds=40, alternate=True):
    """Two rows (a hand's re and im) on a (4, 4, 4) board, grips W / 6 per Mesh. Alternating W and W+ every round,
    every clock ticks every round (the full rate), so each tick's W is the gear's last W+; else W = W+ throughout,
    the rates parted and the rounds under random masks."""
    rng = np.random.default_rng(seed)
    nb = board((4, 4, 4))
    n = nb.shape[1]
    w = 6 * int(rng.integers(1, 9))
    wp = 6 * int(rng.integers(1, 9)) if alternate else w
    s0 = int(rng.integers(1, 4))
    plan = Plan(np.array([0], np.intp), np.array([4 + 1], np.intp), obj([1]), np.array([1], np.intp))  # J_1 = a_0 F_1
    grip = obj(np.full((1, 3 * n), w // 6))
    rate = obj(np.full((1, n), GAMMA)) if alternate else obj(rng.integers(0, GAMMA + 1, (1, n)))
    a = obj(rng.integers(-50, 50, (2, n)))
    b = a - obj(rng.integers(-3, 4, (2, n)))
    go = obj(rng.integers(0, 2, (2, n)))
    r = obj(rng.integers(0, w, (2, n)))
    zero = obj(np.zeros((1, n), int))
    out = []
    for lam in (1, scale):
        layout = Layout(nb, meshes_of(nb), grip, Gearing(obj(lam * w), obj(lam * wp), lam * s0, 0, 1, 3), plan, rate, GAMMA)
        laid = lam * (r - home(w, go)) + home(lam * w, go) if mapped else home(lam * w, go) + 0 * r
        s = State(a, b, laid, go, obj(np.zeros((2, n), int)), zero, zero, zero)
        start, path, outs = s, [], []
        for t in range(rounds):
            # the wears alternate W and W+ so each tick's W is the last tick's W+, as 7b's load keeps it
            ws = (lam * w, lam * wp) if t % 2 == 0 else (lam * wp, lam * w)
            layout = layout._replace(gearing=layout.gearing._replace(w=obj(ws[0]), wp=obj(ws[1])))
            draw = obj(np.ones((1, n), int)) if alternate else obj(rng.integers(0, 2, (1, n)))
            mask = draw if lam == 1 else masks[t]
            if lam == 1:
                masks.append(mask)
            s, o = step.tick(layout, s, mask)
            path.append((s, ws))
            outs.append((layout, o))
        back = s
        for layout_t, o in reversed(outs):
            back = step.untick(layout_t, back, o)
        out.append((path, all(np.array_equal(x, y) for x, y in zip(back, start, strict=True))))
    return out


masks = []
L = GAMMA**3
for alternate, label in ((True, "W and W+ parted, alternating, every clock ticking"),
                         (False, "W = W+, the rates parted, random masks")):
    held = mapped_teeth = back = at_home = 0
    for seed in range(20):
        masks.clear()
        (plain, back1), (scaled, back2) = worlds(seed, L, alternate=alternate)
        held += all(np.array_equal(p.a, q.a) and np.array_equal(p.b, q.b) and np.array_equal(p.ph, q.ph)
                    for (p, _), (q, _) in zip(plain, scaled, strict=True))
        # after each tick the fine tooth stands at that tick's W+
        mapped_teeth += all(np.array_equal(q.r, L * (p.r - home(wp, p.go)) + home(L * wp, p.go))
                            for (p, (_, wp)), (q, _) in zip(plain, scaled, strict=True))
        back += back1 and back2
        masks.clear()
        (rest, _), (rest_scaled, _) = worlds(seed, L, mapped=False, alternate=alternate)
        at_home += all(np.array_equal(p.a, q.a) for (p, _), (q, _) in zip(rest, rest_scaled, strict=True))
    print(f"{label}, L = Gamma^3 = {L}, 20 worlds of 40 rounds:")
    print(f"  (1) the notches and the dials equal at every round in {held} of 20; the fine tooth mapped in {mapped_teeth} of 20")
    print(f"  (2) both worlds run back to their own starts in {back} of 20")
    print(f"  (3) each laid at its own home, the stride in the notches alone: the notches equal in {at_home} of 20")
