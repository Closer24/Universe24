"""THIRD5's pick: the triangle's carried form against the draw form (G5's draw from the state picking against the same
weights, entering each taker's carry as its remainder; a measurement form, not lawful, THIRD5 1.7), on the first test's
world: the run back, the 24, and Big Pic's two readings on the board: landings against the last (the lag-1 correlation
of the first taker's landing over the rounds a quantum moves) and the lives (the gaps between the first taker's
landings: their mean, their variance against the mean squared, 1 for the exponential law and 0 for a fixed life).
Whole numbers only; Rule3's carry the one division; paths by joinpath."""
import json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import numpy as np
import world_load
import third5
from tensor24.algebra.carry import carry
from tensor24.engine.state import State
universe, piece, setting, loaded, layout, start = world_load.world("world")
roles = world_load.roles(loaded, setting)
c4 = json.loads(HERE.joinpath("world", "third.json").read_text(encoding="utf-8"))["chosen4"]
c5 = json.loads(HERE.joinpath("world", "third.json").read_text(encoding="utf-8"))["chosen5"]
cfg = third5.Third(c5["strength"], c4["dial"], tuple(c4["weights"]), c4["share_dial"])
third5.TRIANGLE_DIAL[0] = c5["triangle_dial"]
out = HERE.joinpath(sys.argv[1] if len(sys.argv) > 1 else "probe5d.txt").open("w", encoding="utf-8")
say = lambda *w: (out.write(" ".join(str(x) for x in w) + "\n"), out.flush())  # noqa: E731
same = lambda x, y: all(np.array_equal(p, q) for p, q in zip(x, y))  # noqa: E731
zr = 0 * start.a[roles.giver]
x0 = (zr, np.stack([zr] * roles.takers.shape[0]))
kinds_, _, _ = world_load.made(3)
t1m = kinds_.t1
turns = [gg for gg in range(t1m.shape[0]) if int((t1m[gg] * t1m[gg]).sum()) != 0]
tr = loaded.trains
gset = set(roles.giver.tolist())
def turned(gg, s, x):
    a, bb, r_, rdd, k = (y.copy() for y in s)
    na, nb_, nr = a.copy(), bb.copy(), r_.copy()
    r3, rw = x
    nr3, nrw = r3.copy(), rw.copy()
    for ti in range(len(tr)):
        train = tr[ti]
        at = train.first
        for kind, dim in zip(train.kinds, train.dims):
            m = [kinds_.a1, kinds_.a2, kinds_.e, kinds_.t1, kinds_.t2][kind][gg]
            for i in range(dim):
                for jj in range(dim):
                    e = int(m[i, jj])
                    if e:
                        na[at + i] = e * a[at + jj]; nb_[at + i] = e * bb[at + jj]
                        nr[at + i] = r_[at + jj] if e == 1 else -1 - r_[at + jj]
                        if at + i in gset:
                            gi, gj = at + i - roles.giver[0], at + jj - roles.giver[0]
                            nrw[:, gi] = rw[:, gj] if e == 1 else third5.TRIANGLE_DIAL[0] - 1 - rw[:, gj]
            at += dim
    return State(na, nb_, nr, rdd, k), (nr3, nrw)
for who in ("triangle", "draw"):
    s, x = start, x0
    for _ in range(3000):
        s, x, _, _ = third5.act5(layout, roles, cfg, s, x, who)
    warm, warmx = s, x
    fail, first = 0, None
    for r in range(1, 1001):
        s1, x1, _, rd = third5.act5(layout, roles, cfg, s, x, who)
        b, bx, _, _ = third5.untick5(layout, roles, cfg, s1, x1, who)
        bad = not (same(b, s) and same(bx, x)); fail += int(bad); first = r if (first is None and bad) else first
        s, x = s1, x1
    good = 0
    for gg in turns:
        s, x = warm, warmx
        u, ux = turned(gg, warm, warmx)
        ok = True
        for _ in range(200):
            s, x, c, rd = third5.act5(layout, roles, cfg, s, x, who)
            u, ux, cu, rdu = third5.act5(layout, roles, cfg, u, ux, who)
            ts, tx = turned(gg, s, x)
            ok = ok and same(ts, u) and np.array_equal(c, cu)
        good += int(ok)
    # Big Pic's readings over 20,000 rounds from the warm board
    s, x = warm, warmx
    ys, land_rounds, quanta = [], [], 0
    acc, land_acc = 0, []  # the first taker's accumulated source on the x row, |k a_giver s_1| summed: its share's own time
    for r in range(1, 20001):
        ag = int(s.a[roles.giver[0], 0])
        s, x, _, rd = third5.act5(layout, roles, cfg, s, x, who)
        acc += abs(cfg.strength * ag * int(rd["sizes"][0, 0]))
        if np.any(rd["delta"] != 0):
            quanta += 1
            y = int(np.any(rd["lam"][0] != 0))
            ys.append(y)
            if y:
                land_rounds.append(r)
                land_acc.append(acc)
    nq = len(ys)
    m1 = sum(ys)
    pairs = sum(ys[i] * ys[i - 1] for i in range(1, nq))
    # the lag-1 correlation: (E[y y'] - p^2) / (p - p^2), with p = m1 / nq, in thousandths, whole numbers
    num = pairs * nq * nq - m1 * m1 * (nq - 1)
    den = (m1 * nq - m1 * m1) * (nq - 1)
    corr, _ = carry(num * 1000, den, 0) if den else (0, 0)
    gaps = [land_rounds[i] - land_rounds[i - 1] for i in range(1, len(land_rounds))]
    g = len(gaps); sg = sum(gaps); sg2 = sum(v * v for v in gaps)
    mean, _ = carry(sg, g, 0)
    ratio, _ = carry((sg2 * g - sg * sg) * 1000, sg * sg, 0)  # the variance over the mean squared, in thousandths
    sgaps = [land_acc[i] - land_acc[i - 1] for i in range(1, len(land_acc))]
    h = len(sgaps); sh = sum(sgaps); sh2 = sum(v * v for v in sgaps)
    smean, _ = carry(sh * 1000, h * third5.TRIANGLE_DIAL[0], 0)
    sratio, _ = carry((sh2 * h - sh * sh) * 1000, sh * sh, 0)
    say(f"{who}: in the share's own time (the accumulated |source| between the first taker's landings): mean {smean} thousandths of the dial D, variance over mean squared {sratio} thousandths (1,000 the exponential law, 0 a fixed life)")
    say(f"{who}: the one-round run back fails at {fail} of 1000 rounds (first at {first}); the 24 over 200 rounds at {good} of {len(turns)} turns; over 20,000 rounds {quanta} rounds moving a quantum, the first taker in {m1}; the lag-1 correlation of the first taker's landing {corr} thousandths; the first taker's gaps: {g}, mean {mean} rounds, variance over mean squared {ratio} thousandths (1,000 the exponential law, 0 a fixed life)")
say("done")
