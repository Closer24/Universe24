"""MIN2: each build item's test against a mutant of it, whole numbers only. argv: tree mode rounds [variant folder].
mode s1: like monomials combined keeping the first factor, not the sum (well): the run against the engine's.
mode unit: the unit-row pruning off by one leg (a value-leg term dropped in place of the unit's) (click).
mode laid: the (a)+(b) pruning taken from the as-laid factors in place of the structure's, run on the world with every
  CHOSEN strength but the key at 1 (click): the structural pruning against it, both against the engine there.
mode side: one live own side dropped (read as the birth) (mesh at file key 7): the teeth and the record lines.
mode flip: D1's read-back without the flip (the partner read as the held tooth) (click): the teeth and the lines."""
import copy
import json
import sys
from pathlib import Path

here = Path(sys.argv[0]).resolve().parent
sys.path.insert(0, str(here))
import world as W  # noqa: E402

tree, mode, rounds = Path(sys.argv[1]), sys.argv[2], int(sys.argv[3])
variant = Path(sys.argv[4]) if len(sys.argv) > 4 else None
W.tree_on(tree)
import numpy as np  # noqa: E402
from tensor24 import main  # noqa: E402
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.engine.state import Plan  # noqa: E402
from tensor24.runner import files, plans  # noqa: E402
from tensor24.runner import load as L  # noqa: E402
from tensor24.runner import run as R  # noqa: E402

world = {"s1": "tensor24-well", "unit": "tensor24-click", "laid": "tensor24-click", "side": "tensor24-mesh",
         "flip": "tensor24-click"}[mode]
u0, st, shape, kinds, ld0, lay0, s0 = W.loaded(tree, variant if variant else tree.joinpath("examples", world))
T = len(ld0.trains)
K = int(lay0.click.key[0, 0])


def text(x):
    return json.dumps([np.asarray(y).tolist() for y in x])


def cut(plan, keep):
    legs, factor, target = plan
    return Plan(legs[:, keep], factor[keep], target[keep])


def cut_j(lay, keep):
    cl = lay.click._replace(weight=lay.click.weight[keep], train=lay.click.train[keep])
    return lay._replace(plan=cut(lay.plan, keep), click=cl)


def race(la, lb, s, n):
    """The first round two layouts' runs part, in state or clicks, from one state; None if they never do."""
    sa = sb = s
    for at in range(1, n + 1):
        sa, ca = step.act(la, sa)
        sb, cb = step.act(lb, sb)
        if text(sa) != text(sb) or text([ca]) != text([cb]):
            return at
    return None


def combined(pot, keep_sum):
    factor, legs = pot
    key_of, keep, f2 = {}, [], []
    for i in range(len(factor)):
        canon = tuple(sorted(int(x[i]) for x in legs))
        if canon in key_of:
            if keep_sum:
                f2[key_of[canon]] = f2[key_of[canon]] + factor[i]
            elif int(f2[key_of[canon]]) == 0:
                f2[key_of[canon]] = factor[i]
        else:
            key_of[canon] = len(keep)
            keep.append(i)
            f2.append(factor[i])
    keep = np.asarray(keep, dtype=np.intp)
    return (np.asarray(f2, dtype=object), tuple(x[keep] for x in legs))


def relaid(u, ld, keep_sum):
    pot = combined(ld.potential, keep_sum)
    click = plans.edging(ld.trains, pot, u["chosen"]["key"], lay0.spokes)
    return main.layout(u, shape, ld._replace(potential=pot, click=click))


if mode == "s1":
    good, bad = relaid(u0, ld0, True), relaid(u0, ld0, False)
    print("S1 on", world, rounds, "rounds: the sum parts at", race(lay0, good, s0, rounds), "; the mutant (first factor kept) parts at",
          race(lay0, bad, s0, rounds))
elif mode == "unit":
    tgt = np.asarray(lay0.plan.target)
    good = cut_j(lay0, np.flatnonzero(tgt != -1))
    live_value = [i for i in range(len(tgt)) if tgt[i] != -1 and int(lay0.plan.factor[i]) != 0]
    keep_bad = np.asarray([i for i in range(len(tgt)) if tgt[i] != -1 or i == live_value[0] - 1 + 1 - 1] , dtype=np.intp)
    keep_bad = np.asarray([i for i in range(len(tgt)) if i != live_value[0] and (tgt[i] != -1)], dtype=np.intp)
    bad = cut_j(lay0, keep_bad)
    print("unit-row pruning on", world, rounds, "rounds: the pruning parts at", race(lay0, good, s0, rounds),
          "; the mutant (one live value-leg term dropped) parts at", race(lay0, bad, s0, rounds))
elif mode == "laid":
    u1 = copy.deepcopy(u0)
    for nm in u1["chosen"]:
        if nm != "key":
            u1["chosen"][nm] = 1
    kinds_, tables, square, lifted = main.ENGINE.made(files.star(len(shape)))
    ld1, found = L.load(u1, st, files.sites_of(shape), kinds_, tables, square, lifted)
    assert not found
    lay1 = main.ENGINE.layout(u1, shape, ld1)
    s1 = W.loaded(tree, tree.joinpath("examples", world))[-1]

    def keep(f):
        return np.flatnonzero(np.asarray(f, dtype=object) != 0)

    def pruned(lay, by):
        out = cut_j(lay, np.intersect1d(keep(by.plan.factor), np.flatnonzero(np.asarray(lay.plan.target) != -1)))
        return out._replace(mesh=cut(lay.mesh, keep(by.mesh.factor)), push=cut(lay.push, keep(by.push.factor)),
                            clock=cut(lay.clock, keep(by.clock.factor)))

    good, bad = pruned(lay1, lay1), pruned(lay1, lay0)
    print("pruning on", world, "with every CHOSEN strength but the key at 1,", rounds, "rounds: by the structure parts at",
          race(lay1, good, s1, rounds), "; the mutant (by the as-laid factors) parts at", race(lay1, bad, s1, rounds),
          "; the mutant on the world as laid parts at", race(lay0, pruned(lay0, lay0), s0, rounds))
else:
    nb = lay0.nb
    p0 = R.joined(lay0.click, T)
    own = sorted({(min(t, v), max(t, v)) for t, ps in enumerate(p0) for v in ps})
    t, v = own[0]
    s = s0
    first_k = first_lines = None
    ks = s0.k.copy()
    for at in range(1, rounds + 1):
        before = s
        s, c = step.act(lay0, s)
        lines = json.dumps(R.clicked(at, before, s, c, p0, nb))
        mk, mc = s.k.copy(), c.copy()
        kk, cc = mk.reshape(-1, T, T, mk.shape[-1]), mc.reshape(-1, T, T, mc.shape[-1])
        bk = ks.reshape(-1, T, T, mk.shape[-1])
        if mode == "side":  # the mutant holds the side (t, v) at its birth: its partner and its clicks from it
            q_, kept = carry(0 * kk[0, t, v], K, bk[0, t, v])
            kk[0, t, v], cc[0, t, v] = s0.k.reshape(-1, T, T, mk.shape[-1])[0, t, v], 0 * cc[0, t, v]
            kk[0, v, t], cc[0, v, t] = K - 1 - kk[0, t, v], -cc[0, t, v]
        else:  # the mutant reads the partner as the held tooth, not as key - 1 less it
            kk[0, v, t] = kk[0, t, v]
            cc[0, v, t] = -cc[0, t, v]
        mlines = json.dumps(R.clicked(at, State_ := before._replace(k=ks), s._replace(k=mk), mc, p0, nb))
        ks = mk
        if first_k is None and text([mk]) != text([s.k]):
            first_k = at
        if first_lines is None and mlines != lines:
            first_lines = at
    print(f"mode {mode} on {world}{' ' + variant.name if variant else ''}, side {(t, v)}, {rounds} rounds: the teeth part at",
          first_k, "; the record's click lines part at", first_lines)
print("END")
