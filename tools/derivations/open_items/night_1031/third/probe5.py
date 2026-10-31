"""THIRD5's probe: WHO by the takers' present squares (the right triangle's rule, carried at the dial L = SUM a^2)
beside THIRD4's CHOSEN weights, on THIRD4's act otherwise: the run back round by round and as a window, the rounds where
a kept share tooth stands outside its round's dial, the 24, C5's books with the readers' five mutants, and how the
landings follow s_i / L. Whole numbers only; Rule3's carry the one division; paths by joinpath."""
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
universe, piece, setting, loaded, layout, start = world_load.world("world")
roles = world_load.roles(loaded, setting)
c4 = json.loads(HERE.joinpath("world", "third.json").read_text(encoding="utf-8"))["chosen4"]
cfg = third5.Third(c4["strength"], c4["dial"], tuple(c4["weights"]), c4["share_dial"])
c5 = json.loads(HERE.joinpath("world", "third.json").read_text(encoding="utf-8"))["chosen5"]
third5.TRIANGLE_DIAL[0] = c5["triangle_dial"]
FORMS = tuple(sys.argv[2].split(",")) if len(sys.argv) > 2 else ("chosen", "squares")
out = HERE.joinpath(sys.argv[1] if len(sys.argv) > 1 else "probe5.txt").open("w", encoding="utf-8")
say = lambda *w: (out.write(" ".join(str(x) for x in w) + "\n"), out.flush())  # noqa: E731
same = lambda x, y: all(np.array_equal(p, q) for p, q in zip(x, y))  # noqa: E731
zr = 0 * start.a[roles.giver]
for who in FORMS:
    x0 = (zr, np.stack([zr] * (roles.takers.shape[0] - (0 if who == "triangle" else 1))))
    s, x = start, x0
    for _ in range(3000):
        s, x, _, _ = third5.act5(layout, roles, cfg, s, x, who)
    warm, warmx = s, x
    fail, quanta, first, outside = 0, 0, None, 0
    land1, exp1, n_q = 0, 0, 0
    for r in range(1, 2001):
        s1, x1, _, rd = third5.act5(layout, roles, cfg, s, x, who)
        outside += rd["outside"]
        if np.any(rd["delta"] != 0):
            quanta += 1
            lam1 = int((rd["lam"][0, :, 0] * rd["delta"][:, 0]).sum())
            land1 += int(lam1 != 0)
            e, _ = carry(int(rd["sizes"][0, 0]) * 1000, int(rd["sizes"][:, 0].sum()), 0)
            exp1 += e
        b, bx, _, _ = third5.untick5(layout, roles, cfg, s1, x1, who)
        bad = not (same(b, s) and same(bx, x))
        fail += int(bad); first = r if (first is None and bad) else first
        s, x = s1, x1
    for r in range(2000):
        s, x, _, _ = third5.untick5(layout, roles, cfg, s, x, who)
    whole = int(same(s, warm) and same(x, warmx))
    if who == "triangle":
        s2, x2 = warm, warmx
        src_acc = [0, 0]; land = [0, 0]; nets = [0, 0]
        for r in range(1, 2001):
            s3, x3, _, rd3 = third5.act5(layout, roles, cfg, s2, x2, who)
            for i in range(2):
                sz = int(rd3["sizes"][i, 0]); ag = int(s2.a[roles.giver[0], 0])
                src_acc[i] += ag * sz
                li = int(rd3["lam"][i, 0, 0]); land[i] += int(li != 0); nets[i] += li
            s2, x2 = s3, x3
        idq = [carry(src_acc[i] + int(warmx[1][i, 0, 0]) - int(x2[1][i, 0, 0]), third5.TRIANGLE_DIAL[0], 0) for i in range(2)]
        say(f"triangle: the carry's identity, D SUM lam_i = SUM source_i + r_i(start) - r_i(end), on the x row over 2000 rounds: net landed {nets}, (SUM source + r0 - r_end) div D = {[q for q, _ in idq]} with remainder {[rr for _, rr in idq]}; landings per taker {land}")
    say(f"{who}: {quanta} rounds moving a quantum in 2000 from the warm board; the one-round run back fails at {fail} rounds, first at {first}; the window exact {whole}; rounds where a kept share tooth stands outside its round's dial: {outside}; the first taker landed {land1} of {quanta}, against SUM s_1 / L = {carry(exp1, 1000, 0)[0]}")
    # the 24
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
        L = (s.a[roles.takers] ** 2).sum(axis=1).sum(axis=0)[None, :]
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
                                nr3[gi] = r3[gj] if e == 1 else cfg.dial - 1 - r3[gj]
                                dial = L if who == "squares" else (third5.TRIANGLE_DIAL[0] if who == "triangle" else cfg.share_dial)
                                nrw[:, gi] = rw[:, gj] if e == 1 else dial - 1 - rw[:, gj]
                at += dim
        return State(na, nb_, nr, rdd, k), (nr3, nrw)
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
    say(f"{who}: the 24 over 200 rounds at {good} of {len(turns)} turns (the gears and the clicks; the share teeth turned at their dial)")
    # C5's books with the readers' five mutants, q the gears' move projected on delta
    hands = [ti for ti in range(len(tr)) if int(tr.tied[ti]) == 1]
    rows_of = {ti: np.arange(int(tr.first[ti]), int(tr.first[ti] + tr.size[ti]), dtype=np.intp) for ti in hands}
    files = [(p, p.read_text(encoding="utf-8")) for p in (HERE.joinpath("world", n) for n in world_load.NAMES)]
    for variant in ("", "no_take", "no_give", "double", "gear_lost", "unapplied"):
        s, x = start, x0
        lines = []
        for r in range(1, 1501):
            s1, x1, _, rd = third5.act5(layout, roles, cfg, s, x, who, variant)
            for ti in hands:
                qq = int(((s1.a[rows_of[ti], 0] - rd["a0"][rows_of[ti], 0]) * rd["delta"][:, 0]).sum())
                if qq != 0:
                    lines.append({"kind": "click", "round": r, "site": 0, "train": ti, "q": qq, "tooth": [0, 0], "quantum": 1})
            s, x = s1, x1
        path = HERE.joinpath(f"rec5_{who}_{variant or 'true'}.jsonl")
        head = R.header(path, files, universe, piece["shape"], kinds_, loaded, layout)
        endl = {"kind": "end", "rounds": 1500, "digest": R.digest(R.stated(s)), "undone": 0, "exact": 0}
        path.write_text("".join(json.dumps(y) + "\n" for y in [head, *lines, endl]), encoding="utf-8")
        rec, cause = records.read(str(path))
        v = shadow.shadow(rec)["the books at each click"] if rec is not None else None
        say(f"{who} {variant or 'true'}: 1,500 rounds from the lay, {len(lines)} lines; C5 books: {v['kind'] if v else 'NOT READ ' + cause}: {v['cause'] if v else ''}")
say("done")
