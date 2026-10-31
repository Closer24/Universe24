"""THIRD5's three takers: the triangle form (third5.act5, who "triangle") on a world of one giver and three takers at one
Node-clock (world3/: the first test's world with a third taker laid at -2 x 10^5, every hand tied to every other):
the run back round by round and as a window from the warm board; the 24, every tooth turned; each taker's landings
against its present square's share SUM s_i / L over the rounds a quantum moves; C5's books with the readers' mutants.
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
from tensor24.runner import run as R
from tensor24.decoder import records, shadow
universe, piece, setting, loaded, layout, start = world_load.world("world3")
roles = world_load.roles(loaded, setting, "world3")
c4 = json.loads(HERE.joinpath("world3", "third.json").read_text(encoding="utf-8"))["chosen4"]
c5 = json.loads(HERE.joinpath("world3", "third.json").read_text(encoding="utf-8"))["chosen5"]
cfg = third5.Third(c5["strength"], c4["dial"], tuple(c4["weights"]), c4["share_dial"])
third5.TRIANGLE_DIAL[0] = c5["triangle_dial"]
out = HERE.joinpath(sys.argv[1] if len(sys.argv) > 1 else "probe5n3.txt").open("w", encoding="utf-8")
say = lambda *w: (out.write(" ".join(str(x) for x in w) + "\n"), out.flush())  # noqa: E731
same = lambda x, y: all(np.array_equal(p, q) for p, q in zip(x, y))  # noqa: E731
n = roles.takers.shape[0]
say(f"world3: {n} takers; the giver's rows {roles.giver.tolist()}; the takers' rows {roles.takers.tolist()}")
zr = 0 * start.a[roles.giver]
x0 = (zr, np.stack([zr] * n))
s, x = start, x0
for _ in range(3000):
    s, x, _, _ = third5.act5(layout, roles, cfg, s, x, "triangle")
warm, warmx = s, x
fail, first, quanta = 0, None, 0
land = [0] * n
expect = [0] * n
big = 0
for r in range(1, 2001):
    s1, x1, _, rd = third5.act5(layout, roles, cfg, s, x, "triangle")
    big = max(big, int(np.abs(rd["lam"]).max()))
    if np.any(rd["delta"] != 0):
        quanta += 1
        total = int(rd["sizes"][:, 0].sum())
        for i in range(n):
            land[i] += int(np.any(rd["lam"][i] != 0))
            e, _ = carry(int(rd["sizes"][i, 0]) * 1000, total, 0)
            expect[i] += e
    b, bx, _, _ = third5.untick5(layout, roles, cfg, s1, x1, "triangle")
    bad = not (same(b, s) and same(bx, x)); fail += int(bad); first = r if (first is None and bad) else first
    s, x = s1, x1
for r in range(2000):
    s, x, _, _ = third5.untick5(layout, roles, cfg, s, x, "triangle")
whole = int(same(s, warm) and same(x, warmx))
say(f"run back: {quanta} rounds moving a quantum in 2000 from the warm board; the one-round run back fails at {fail}, first at {first}; the window exact {whole}; the largest |lam| {big}")
say(f"each taker's landings against its present square's share (SUM s_i / L, in thousandths, over the rounds a quantum moves): landed {land}, expected {[carry(e, 1000, 0)[0] for e in expect]}")
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
good = 0
for gg in turns:
    s, x = warm, warmx
    u, ux = turned(gg, warm, warmx)
    ok = True
    for _ in range(200):
        s, x, c, rd = third5.act5(layout, roles, cfg, s, x, "triangle")
        u, ux, cu, rdu = third5.act5(layout, roles, cfg, u, ux, "triangle")
        ts, tx = turned(gg, s, x)
        ok = ok and same(ts, u) and same(tx, ux) and np.array_equal(c, cu)
    good += int(ok)
say(f"the 24 over 200 rounds at {good} of {len(turns)} turns, the gears, the clicks and every tooth")
hands = [ti for ti in range(len(tr)) if int(tr.tied[ti]) == 1]
rows_of = {ti: np.arange(int(tr.first[ti]), int(tr.first[ti] + tr.size[ti]), dtype=np.intp) for ti in hands}
files = [(pp, pp.read_text(encoding="utf-8")) for pp in (HERE.joinpath("world3", nm) for nm in world_load.NAMES)]
for variant in ("", "no_take", "no_give", "double", "gear_lost", "unapplied"):
    s, x = start, x0
    lines = []
    for r in range(1, 1501):
        s1, x1, _, rd = third5.act5(layout, roles, cfg, s, x, "triangle", variant)
        u = rd["delta"][:, 0]
        for ti in hands:
            qq = int(((s1.a[rows_of[ti], 0] - rd["a0"][rows_of[ti], 0]) * u).sum())
            if qq != 0:
                lines.append({"kind": "click", "round": r, "site": 0, "train": ti, "q": qq, "tooth": [int(s.k[ti, 0]), int(s1.k[ti, 0])]})
        s, x = s1, x1
    path = HERE.joinpath(f"rec5n3_{variant or 'true'}.jsonl")
    head = R.header(path, files, universe, piece["shape"], kinds_, loaded, layout)
    endl = {"kind": "end", "rounds": 1500, "digest": R.digest(R.stated(s)), "undone": 0, "exact": 0}
    path.write_text("".join(json.dumps(y) + "\n" for y in [head, *lines, endl]), encoding="utf-8")
    rec, cause = records.read(str(path))
    v = shadow.shadow(rec)["the books at each click"] if rec is not None else None
    per = {t: tuple(z) for t, z in v.get("trains", {}).items()} if v else None
    say(f"C5 books, {variant or 'true'}: 1,500 rounds from the lay, {len(lines)} lines: {v['kind'] if v else 'NOT READ ' + cause}: {v['cause'] if v else ''}; per train (lines, given, taken, net) {per}")
say("done")
