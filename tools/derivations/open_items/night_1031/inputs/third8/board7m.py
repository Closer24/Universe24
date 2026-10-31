"""THIRD7's memory reading at the board's own varying rate, with its power stated. First: are the click world's 27
Node-clocks one clock triangle 27 times over (every Node-clock's flows alike at every round)? If so the board's power is
one Node-clock's, and the reading runs at Node-clock 0 alone over longer stretches. Second: Big Pic's laid stand-in
(edgeclick.board_lay, VARY1's, labelled so: the hands laid apart below the key by the board's coordinates), whose
Node-clocks differ, at all 27. Per stream (the path's landings, each clock's line, each edge's side) and form (the
member, the member unturned, the first click): clicks, clicks in two rounds running and in three, against fresh draws at
each round's own rate from the board's own flow (exact means and variances; z^2 per mille), and the lives against fresh-
draw replicas (a whole-number generator, the stand-in's). argv: src, lay (click or laid), rounds, replicas, sites (one or
all)."""
import sys
from pathlib import Path

SRC, LAYW, ROUNDS, REPL, SITES = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import tri7  # noqa: E402

tri7.setup(SRC)
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import step  # noqa: E402

W64 = 1 << 64


def per_mille(n, d):
    return carry(1000 * n, d, 0)[0] if d else None


def fresh_dist(v, M):
    k, rho = carry(v, M, 0)
    out = {k: M - rho}
    out[k + 1] = out.get(k + 1, 0) + rho
    return out


def convolve(d1, d2, s2):
    out = {}
    for a, wa in d1.items():
        for b, wb in d2.items():
            z = a + s2 * b
            out[z] = out.get(z, 0) + wa * wb
    return out


def nonzero(d):
    return sum(w for z, w in d.items() if z)


def moments(n, d):
    T = len(n)
    e1 = sum(n)
    v1 = sum(a * (d - a) for a in n)
    e2 = sum(n[t] * n[t + 1] for t in range(T - 1))
    v2 = sum(n[t] * n[t + 1] * d * d - n[t] * n[t] * n[t + 1] * n[t + 1] for t in range(T - 1))
    v2 += 2 * sum(n[t] * n[t + 1] * n[t + 2] * (d - n[t + 1]) for t in range(T - 2))
    e3 = sum(n[t] * n[t + 1] * n[t + 2] for t in range(T - 2))
    v3 = sum(n[t] * n[t + 1] * n[t + 2] * d * d * d - (n[t] * n[t + 1] * n[t + 2]) ** 2 for t in range(T - 2))
    v3 += 2 * sum(n[t] * n[t + 1] * n[t + 2] * n[t + 3] * (d * d - n[t + 1] * n[t + 2]) for t in range(T - 3))
    v3 += 2 * sum(n[t] * n[t + 1] * n[t + 2] * n[t + 3] * n[t + 4] * (d - n[t + 2]) for t in range(T - 4))
    return e1, v1, e2, v2, e3, v3


def lives(gaps):
    k, s1, s2 = len(gaps), sum(gaps), sum(g * g for g in gaps)
    return per_mille(k * s2 - s1 * s1, s1 * s1) if s1 else None


def z2(obs, e, v, dk):
    return per_mille((obs * dk - e) ** 2, v) if v else None


def main():
    universe, shape, held, lay, s0, world, star = tri7.load_world(SRC, Path(SRC).parent.joinpath("examples", "tensor24-click"))
    if LAYW == "laid":
        sys.path.insert(0, str(HERE.joinpath("bp")))
        import edgeclick as E

        s0 = E.board_lay(s0, shape, world)
    rows, sites = s0.a.shape
    key = int(lay.click.key[0, 0])
    pairs, triangles = tri7.edge_set(world)
    D = star["half"] * key
    m = tri7.Member(len(pairs), triangles, D, star["senses"])
    fc = tri7.First(len(pairs), D, star["senses"])
    xs_sites = [0] if SITES == "one" else list(range(sites))
    flows = {x: [] for x in xs_sites}
    alike_rounds = 0
    s = s0
    for t in range(ROUNDS):
        s1, _ = step.act(lay, s)
        per = []
        for x in range(sites) if (t < 200 or SITES == "all") else xs_sites:
            b = [int(s.b[r, x]) for r in range(rows)]
            a = [int(s.a[r, x]) for r in range(rows)]
            a1 = [int(s1.a[r, x]) for r in range(rows)]
            fl = world.split_flows(0, b, a, a1)
            per.append([fl.get(pr, 0) for pr in pairs])
            if x in flows:
                flows[x].append(per[-1])
        if t < 200:
            alike_rounds += int(all(p == per[0] for p in per))
        s = s1
    print(f"board7m: the {LAYW} lay, {ROUNDS} rounds, Node-clocks read {len(xs_sites)}; every Node-clock's flows alike"
          f" at {alike_rounds} of {min(ROUNDS, 200)} rounds")
    pos = {tr: [(e, 1 if pr[0] == tr else -1) for e, pr in enumerate(pairs) if tr in pr] for tr in world.trains}
    pos = {tr: v for tr, v in pos.items() if v}
    seed = 17
    for form in ("member", "unturned", "first"):
        ev = {}
        nums = {}
        dens = {}
        for x in xs_sites:
            teeth = m.birth() if form != "first" else (fc.birth(),)
            for t in range(ROUNDS):
                xv = flows[x][t]
                if form == "first":
                    q = fc.step(xv, teeth[0])
                    w = []
                else:
                    q, w = m.step(xv, *teeth, turned=(form == "member"))
                for e, c in enumerate(q):
                    if c:
                        ev.setdefault(("edge", pairs[e]), set()).add((t, x))
                for tr, es in pos.items():
                    if sum(sg * q[e] for e, sg in es):
                        ev.setdefault(("clock", tr), set()).add((t, x))
                for i, v in enumerate(w):
                    if v:
                        ev.setdefault(("path", i), set()).add((t, x))
                # the fresh-draw rate of each stream this round
                if form == "first":
                    de = [fresh_dist(xv[e], D) for e in range(len(pairs))]
                    dd = [D] * len(pairs)
                    path = []
                else:
                    y = [sum(sg * xv[e] for e, sg in col) for col in m.C]
                    p = [m.g[e] * xv[e] - sum(sg * y[tt] for tt, sg in m.on[e]) for e in range(len(pairs))]
                    de = [fresh_dist(p[e], m.dial[e]) for e in range(len(pairs))]
                    dd = list(m.dial)
                    path = [fresh_dist(y[tt], m.tdial[tt]) for tt in range(len(m.C))]
                for e in range(len(pairs)):
                    if form == "first" or not m.on[e]:
                        d, den = de[e], dd[e]
                    else:
                        tt, sg = m.on[e][0]
                        d, den = convolve(de[e], path[tt], sg), dd[e] * m.tdial[tt]
                    k = ("edge", pairs[e])
                    dens[k] = den
                    nums.setdefault(k, {}).setdefault(x, []).append(nonzero(d))
                for tr, es in pos.items():
                    d, den = {0: 1}, 1
                    for e, sg in es:
                        d, den = convolve(d, de[e], sg), den * dd[e]
                    k = ("clock", tr)
                    dens[k] = den
                    nums.setdefault(k, {}).setdefault(x, []).append(nonzero(d))
                for tt in range(len(path)):
                    k = ("path", tt)
                    dens[k] = m.tdial[tt]
                    nums.setdefault(k, {}).setdefault(x, []).append(nonzero(path[tt]))
        for k in sorted(nums, key=str):
            d = dens[k]
            e1 = v1 = e2 = v2 = e3 = v3 = 0
            for x, nn in nums[k].items():
                a = moments(nn, d)
                e1, v1, e2, v2, e3, v3 = e1 + a[0], v1 + a[1], e2 + a[2], v2 + a[3], e3 + a[4], v3 + a[5]
            evs = ev.get(k, set())
            by = {}
            for t, x in evs:
                by.setdefault(x, set()).add(t)
            n1 = sum(len(v) for v in by.values())
            n2 = sum(1 for v in by.values() for t in v if t + 1 in v)
            n3 = sum(1 for v in by.values() for t in v if t + 1 in v and t + 2 in v)
            gaps = []
            for v in by.values():
                st = sorted(v)
                gaps += [b - a_ for a_, b in zip(st, st[1:])]
            # replicas
            r = seed
            lv_r = []
            for _ in range(REPL):
                g_r = []
                for x, nn in nums[k].items():
                    last = None
                    for t, a in enumerate(nn):
                        r = carry(r * 6364136223846793005 + 1442695040888963407, W64, 0)[1]
                        if carry(r * d, W64, 0)[0] < a:
                            if last is not None:
                                g_r.append(t - last)
                            last = t
                lv = lives(g_r)
                lv_r.append(-1 if lv is None else lv)
            seed = r
            lv_r.sort()
            lo, mid, hi = lv_r[carry(REPL, 20, 0)[0]], lv_r[carry(REPL, 2, 0)[0]], lv_r[REPL - 1 - carry(REPL, 20, 0)[0]]
            print(f"  {form} {k[0]} {k[1]}: clicks {n1} against {carry(e1, d, 0)[0]} fresh (z^2 {z2(n1, e1, v1, d)} per"
                  f" mille); two running {n2} against {carry(e2, d * d, 0)[0]} (z^2 {z2(n2, e2, v2, d * d)}); three {n3}"
                  f" against {carry(e3, d ** 3, 0)[0]} (z^2 {z2(n3, e3, v3, d ** 3)}); lives {lives(gaps)} per mille over"
                  f" {len(gaps)} gaps, fresh draws' {mid} (90 per cent of {REPL} within {lo} to {hi})")


main()
