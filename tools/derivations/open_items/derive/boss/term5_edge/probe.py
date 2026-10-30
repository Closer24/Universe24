"""Term 5, the metric's push in its first-order form on the edge, measured on the act in whole numbers (the Boss's
code writer, 2026-10-30; a local draft): the example universe (light, A1 of two parts; the metric family, the
four-vector's square) on a cube of 3, the push's strength CHOSEN here as the probe's own, no file's.

Clock: the matter's momentum, the whole count with the tooth on the edge, read in whole turns of the rest dial, winds
the clock's own train: the 00 slot rises where the matter moves, the ii slots fall by a twelfth of it, and a hand at
rest winds nothing.
Algebra: J = 2T - eta T from the momenta in and out and the gradients, +12 J00 on the 00 slot and -J on the others;
the mirror swaps and negates the momenta, so the push is the same both ways and the round runs back.
Board: 12 rows at 27 sites; the 00 slot moving under the push, so the edge's dial moves with it.
Clicks: n/a: the probe reads the board from outside.

Run: .venv/bin/python tools/derivations/open_items/derive/boss/term5_edge/probe.py; its output is probe.txt beside it.
"""

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[6]
sys.path.insert(0, str(ROOT / "src"))

from tensor24 import main  # noqa: E402
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import kinds, step  # noqa: E402
from tensor24.engine.state import State  # noqa: E402
from tensor24.runner import load as loading  # noqa: E402
from tensor24.runner.files import sites_of  # noqa: E402

SHAPE = [3, 3, 3]
ROUNDS = 40
UNIVERSE = json.loads((ROOT / "examples" / "tensor24" / "universe.json").read_text(encoding="utf-8"))
GRIP = UNIVERSE["integers"]["den"] * UNIVERSE["integers"]["full_rate"] * UNIVERSE["integers"]["full_rate"]
STRENGTH, _ = carry(GRIP, 1000, 0)  # the probe's own CHOSEN strength, a thousandth of a grip: about 40 counts a round on the 00 slot


def recurrence(seed):
    """Whole numbers from a fixed recurrence, each step one carry: no random module."""
    v = seed
    while True:
        _, v = carry(v * 6364136223846793005 + 1442695040888963407, 1 << 64, 0)
        yield v


def drawn(src, low, high):
    """A whole number in [low, high] from the recurrence's high bits, by two carries."""
    top, _ = carry(next(src), 1 << 33, 0)
    _, x = carry(top, high - low + 1, 0)
    return low + x


def world(strength, lay, seed=6):
    """The example universe at the strength given on the cube, its gears laid by `lay(train, component, site, src)`."""
    universe = json.loads(json.dumps(UNIVERSE))
    universe["chosen"]["push"] = strength
    sites = sites_of(SHAPE)
    made = main.made(loading.star(len(SHAPE)))
    empty, _ = loading.load(universe, {"version": 1, "gears": []}, sites, *made)
    src = recurrence(seed)
    gears = []
    for t in range(len(empty.trains)):
        train = empty.trains[t]
        for component in range(train.rows()):
            for x in range(sites):
                a, b, r = lay(train, component, x, src)
                gears.append([t, component, x, a, b, r])
    held, laid = loading.load(universe, {"version": 1, "gears": gears}, sites, *made)
    assert not laid, laid
    return held, main.layout(universe, SHAPE, held), State(*held.state)


def at_rest(train, component, x, src):
    """A hand at rest: the light's first component at a count, both slots alike, its tooth 0; the metric at 0."""
    return (10**6, 10**6, 0) if (not train.square and component == 0) else (0, 0, 0)


def moving(train, component, x, src):
    """A hand moving: the light's components drawn with strides in [-30, 30] counts a round; the metric at 0."""
    if train.square:
        return 0, 0, 0
    a = drawn(src, -1000, 1000)
    return a, a - drawn(src, -30, 30), 0


def gliding(train, component, x, src):
    """A hand gliding alike at every site, no gradient: the light's first component at a stride of 30 a round."""
    return (10**6, 10**6 - 30, 0) if (not train.square and component == 0) else (0, 0, 0)


def same(s, t):
    return all(bool(np.array_equal(x, y)) for x, y in zip(s, t, strict=True))


def slots(held):
    """The square's rows: 00, the three 0i, the three ii, the three jk."""
    first = next(int(held.trains[t].first) for t in range(len(held.trains)) if held.trains[t].square)
    return first, [first + 1 + i for i in range(3)], [first + 4 + i for i in range(3)], [first + 7 + i for i in range(3)]


def report():
    out = []

    def say(line):
        print(line)
        out.append(line)

    say("Term 5 on the edge (step.act), whole numbers: the example universe on a cube of 3, 12 rows at 27 sites")
    say(f"the grip at rest den Gamma^2 = {GRIP}, the rest teeth 6 grips; the probe's strength {STRENGTH}")
    # 1. a hand at rest sources nothing
    held, layout, s = world(STRENGTH, at_rest)
    s00, s0i, sii, sjk = slots(held)
    moved = 0
    for _ in range(ROUNDS):
        s = step.tick(layout, s)
        moved += int((s.a[[s00, *s0i, *sii, *sjk]] != 0).sum())
    say(f"1. a hand at rest (count 10^6, no stride, tooth 0), {ROUNDS} rounds: metric slots moved from 0: {moved} of"
        f" {10 * 27 * ROUNDS} slot-rounds (a hand at rest sources nothing)")
    # 2. a gliding hand (dust, no gradient): the 00 slot up, each ii slot down by a twelfth; then a hand with gradients
    held, layout, s0 = world(STRENGTH, gliding)
    s = step.tick(layout, s0)
    wa, wb = step.dials(layout, s)
    p = ((wa + wb) * (s.a - s.b) * 2 + s.r).sum(axis=1)  # the momentum the push landed on, 4 x the push exactly
    up, down = int(p[s00]), [-int(p[r]) for r in sii]
    q, rem = carry(up, down[0], 0)
    say(f"2. a hand gliding alike everywhere (dust, stride 30, no gradient), one round: the momentum the push landed on"
        f" the 00 row, summed over the board, {up} (up), on each ii row {down} (down): the ratio {q} remainder {rem},"
        f" against 12 exactly (the 00 slot in teeth, each ii slot in grips at both ends: rest / (grip / 2) = 12, gamma = 1);"
        f" the counts after one round: the 00 slot's sum {int(s.a[s00].sum())}, each ii slot's {[int(s.a[r].sum()) for r in sii]},"
        f" the 0i and jk slots' {int(abs(s.a[[*s0i, *sjk]]).sum())}")
    held, layout, s0 = world(STRENGTH, moving)
    s = step.tick(layout, s0)
    push00 = s.a[s00] - s0.a[s00]
    pushii = [s.a[r] - s0.a[r] for r in sii]
    say(f"   a hand drawn site by site (gradients far above its strides), one round: the 00 slot rose at"
        f" {int((push00 > 0).sum())} of 27 sites and fell at {int((push00 < 0).sum())}; the three ii slots fell at"
        f" {[int((x < 0).sum()) for x in pushii]} sites (the gradients' pressure enters J_ii with both signs, as 2T - eta T has it)")
    # 3. the run back with the push on, the clock moving under it, the 24, the momentum
    states = [s0]
    for _ in range(ROUNDS):
        states.append(step.tick(layout, states[-1]))
    wa0, _ = step.dials(layout, s0)
    wa1, _ = step.dials(layout, states[-1])
    end = states[-1]
    back = sum(same(step.untick(layout, states[n + 1]), states[n]) for n in range(ROUNDS))
    for _ in range(ROUNDS):
        end = step.untick(layout, end)
    twice = sum(same(step.mirror(layout, step.mirror(layout, st)), st) for st in states)
    say(f"3. the moving hand, {ROUNDS} rounds under the push: the 00 slot's board sum from {int(s0.a[s00].sum())} to"
        f" {int(states[-1].a[s00].sum())}, W on the light's rows from {int(wa0[0, 0])} to {int(wa1[0, 0])} at site 0"
        f" (the clock moving under its matter); untick(tick s) = s in {back} of {ROUNDS} rounds; the {ROUNDS} rounds"
        f" rewound bit for bit: {same(end, s0)}; mirror twice the identity at {twice} of {ROUNDS + 1} states")
    # the matter's momentum kept (its pushes sum to 0 on the torus), the metric's moved by its pushes
    def momentum(st):
        wa, wb = step.dials(layout, st)
        return ((wa + wb) * (st.a - st.b) * 2 + st.r).sum(axis=1)
    p0 = momentum(s0)
    light_rows = [r for r in range(s0.a.shape[0]) if r not in (s00, *s0i, *sii, *sjk)]
    kept = sum(bool((momentum(st)[light_rows] == p0[light_rows]).all()) for st in states)
    say(f"   the light rows' board sums of P = 2 D_in (a - b) + s kept exactly in {kept} of {ROUNDS + 1} states;"
        f" the metric rows' moved by their pushes (the 00 row's P at the end {int(momentum(states[-1])[s00])})")
    # the 24 under the push
    from tests import frame
    from tests.test_the_tensor24_run import turned

    sys.path.insert(0, str(ROOT))
    held24 = [0] * 6
    for m in frame.turns():
        t = turned(m, layout, held, s0, SHAPE)
        for n in range(6):
            t = step.tick(layout, t)
            held24[n] += same(t, turned(m, layout, held, states[n + 1], SHAPE))
    say(f"   the 24 under the push, rounds 1 to 6: {held24}")
    # 4. a mutant: the push with the 0i rows' parity even (the mirror not negating their counts): the run back breaks
    even = layout._replace(gearing=layout.gearing._replace(parity=0 * layout.gearing.parity + 1))
    broke = sum(same(step.untick(even, step.tick(even, st)), st) for st in states[:12])
    say(f"4. the mutant, the 0i slots' parity taken even (their counts not negated by the mirror): untick(tick s) = s in"
        f" {broke} of 12 rounds (the 0i push is odd under time's reversal, so the rows it lands on must be)")
    Path(__file__).with_name("probe.txt").write_text("\n".join(out) + "\n", encoding="utf-8")


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT))
    report()
