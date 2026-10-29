"""Locality and purity of stage 7a's full act (J on, every coefficient parted), forward and run back.

Usage: PYTHONPATH=<worktree>/src:<worktree> python -P local_pure.py
Locality: at every site, every state entry beyond the site and its six neighbours (and, for the run back, every out
entry beyond them) is replaced by a fresh world's; the site's new state and out must not move. Purity: the inputs
frozen, two worlds asked in turn of the same functions answer as the first asking did.
"""

import numpy as np

from tensor24.engine import step
from tests.test_the_tensor24_act import draw, varied, world


def same(xs, ys):
    return all(np.array_equal(x, y) for x, y in zip(xs, ys, strict=True))


def flat(result):
    s, o = result
    return [*s, *o]


def local(seed):
    rng = np.random.default_rng(seed)
    layout = varied(rng)
    s, mask = world(rng, layout), draw(rng, 0, 2, (1, layout.nb.shape[1]))
    nb = layout.nb
    out = flat(step.tick(layout, s, mask))
    now, o = step.tick(layout, s, mask)
    back = list(step.untick(layout, now, o))
    bad_f = bad_b = 0
    for site in range(nb.shape[1]):
        far = ~np.isin(np.arange(nb.shape[1]), [site, *nb[1:, site]])
        fresh = world(rng, layout)
        moved = flat(step.tick(layout, type(s)(*(np.where(far, f, x) for f, x in zip(fresh, s, strict=True))), np.where(far, 1 - mask, mask)))
        bad_f += not same([p[:, site] for p in moved], [p[:, site] for p in out])
        fresh_now, fresh_o = step.tick(layout, fresh, mask)
        now_m = type(now)(*(np.where(far, f, x) for f, x in zip(fresh_now, now, strict=True)))
        o_m = type(o)(*(np.where(far, f, x) for f, x in zip(fresh_o, o, strict=True)))
        undone = list(step.untick(layout, now_m, o_m))
        bad_b += not same([p[:, site] for p in undone], [p[:, site] for p in back])
    return bad_f, bad_b, nb.shape[1]


def pure(seed):
    rng = np.random.default_rng(seed)
    layout = varied(rng)
    worlds = [world(rng, layout) for _ in range(2)]
    mask = draw(rng, 0, 2, (1, layout.nb.shape[1]))
    frozen = [layout.nb, layout.meshes, layout.grip, *layout.gearing, *layout.plan, layout.rate, mask, *worlds[0], *worlds[1]]
    for x in frozen:
        if isinstance(x, np.ndarray):
            x.flags.writeable = False
    first = [flat(step.tick(layout, w, mask)) for w in worlds]
    again = [flat(step.tick(layout, worlds[i % 2], mask)) for i in range(4)]
    backs = [list(step.untick(layout, *step.tick(layout, w, mask))) for w in worlds]
    return all(same(again[i], first[i % 2]) for i in range(4)) and all(same(b, w) for b, w in zip(backs, worlds, strict=True))


for seed in range(4):
    f, b, n = local(seed)
    print(f"seed {seed}: locality forward {n - f} of {n} sites hold, run back {n - b} of {n} sites hold")
print("purity (inputs frozen, worlds asked in turn, run back exact):", all(pure(s) for s in range(4)))
