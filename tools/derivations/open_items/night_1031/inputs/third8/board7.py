"""THIRD7 on the board: the member (the triangle's own tooth pair, tri7.Member) against the first click, on the click
world, its swap (the giver and the taker exchanged in the files, together) and its name swap (the two cards' names
exchanged, their order kept), node-live 1794d474b's act unchanged (third6_frozen/c5n/src). Whole numbers only.

Read, in this order:
1. the owner's seed test: (i) from the end seed alone, nothing saved, the board by untick (each round's passing read
   again from the board running back) and the teeth by the same act on the mirrored state reach the start seed;
   (ii) one hidden unit in the triangle's twin at Node-clock 0: equal lines at every clock, sides apart only at that
   Node-clock, the same end board; (iii) the first click from the same start reaches the same end board;
2. the same act on the mirrored state at every Node-clock round;
3. the swap and the name swap, line by line and side by side;
4. each clock's booked total against its own swept passing, and the exact identity G D Q = G X + (teeth at the birth
   less at the end), beside each edge's net and the path's;
5. memory per clock (lines), per edge (sides) and of the path (the triangle's landings) against fresh draws at each
   round's own rate from the board's own flow (every tooth drawn fresh and uniform each round, the round's passing
   given): clicks, clicks in two rounds running and in three, each with its exact mean and variance, and z^2 per mille;
   the lives against the same fresh draws (R replicas by a whole-number generator, the stand-in's);
6. Big Pic's bench (bp/circ.py, bp/edgeclick.py from 8a718332f) on the same world: the record's digest.
argv: src, rounds, replicas."""
import sys
from pathlib import Path

SRC, ROUNDS, REPL = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import tri7  # noqa: E402

tri7.setup(SRC)
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import step  # noqa: E402

EX = Path(SRC).parent.joinpath("examples")
WORLDS = {"click": EX.joinpath("tensor24-click"), "swap": EX.joinpath("tensor24-click-swap"),
          "names": HERE.joinpath("worlds", "tensor24-click-names")}


def per_mille(n, d):
    return carry(1000 * n, d, 0)[0] if d else None


class Run:
    """One world: the board forward (each round's flows per Node-clock), and the teeth runs on those flows."""

    def __init__(self, name):
        self.universe, self.shape, self.held, self.lay, self.s0, self.world, self.star = tri7.load_world(SRC, WORLDS[name])
        self.rows, self.sites = self.s0.a.shape
        self.key = int(self.lay.click.key[0, 0])
        self.pairs, self.triangles = tri7.edge_set(self.world)
        self.D = self.star["half"] * self.key  # (Spokes div senses) x key
        self.member = tri7.Member(len(self.pairs), self.triangles, self.D, self.star["senses"])
        self.first = tri7.First(len(self.pairs), self.D, self.star["senses"])
        self.trains = self.world.trains

    def flows_at(self, s, s1, x, check=None):
        b = [int(s.b[r, x]) for r in range(self.rows)]
        a = [int(s.a[r, x]) for r in range(self.rows)]
        a1 = [int(s1.a[r, x]) for r in range(self.rows)]
        fl = self.world.split_flows(0, b, a, a1)
        if check is not None:
            check[0] += int(fl != self.world.split_flows_david(0, b, a, a1))
        return [fl.get(pr, 0) for pr in self.pairs]

    def forward(self, form, hidden=None, check=None):
        """From the start seed: the board by step.act, the teeth by the form; hidden: (site, 'eta' or 'edge', index)."""
        s = self.s0
        teeth = [self.member.birth() if form in ("member", "unturned") else (self.first.birth(),) for _ in range(self.sites)]
        if hidden is not None:
            x, which, i = hidden
            if which == "eta":
                teeth[x][2][i] = self.member.tborn[i] + self.member.cen(teeth[x][2][i] - self.member.tborn[i] + 1, i)
            else:
                f = teeth[x][0]
                d = self.member.dial[i] if form == "member" else self.D
                f[i] = carry(f[i] + 1, d, 0)[1]
        lines, sides, paths, flows = [], [], [], []
        for t in range(ROUNDS):
            s1, _ = step.act(self.lay, s)
            rf = []
            for x in range(self.sites):
                xs = self.flows_at(s, s1, x, check)
                rf.append(xs)
                if form == "member":
                    q, w = self.member.step(xs, *teeth[x])
                    paths += [(t, x, i, v) for i, v in enumerate(w) if v]
                elif form == "unturned":
                    q, w = self.member.step(xs, *teeth[x], turned=False)
                    paths += [(t, x, i, v) for i, v in enumerate(w) if v]
                else:
                    q = self.first.step(xs, teeth[x][0])
                sides += [(t, x, e, c) for e, c in enumerate(q) if c]
                lines += tri7.lines_of(self.pairs, self.trains, t, x, q)
            flows.append(rf)
            s = s1
        return {"end": s, "teeth": teeth, "lines": lines, "sides": sides, "paths": paths, "flows": flows}

    def backward(self, form, s_end, teeth_end):
        """From the end seed alone: the board by untick, each round's passing read again from the board running back,
        the teeth by the same act on the mirrored state (the twins flipped, every passing negated)."""
        m = self.member
        if form == "member":
            back = [(list(f), list(tau), m.flip(eta)) for f, tau, eta in teeth_end]
        else:
            back = [(list(tt[0]),) for tt in teeth_end]
        s = s_end
        for _ in range(ROUNDS):
            sp = step.untick(self.lay, s)
            for x in range(self.sites):
                xs = self.flows_at(sp, s, x)
                if form == "member":
                    m.step([-v for v in xs], *back[x])
                else:
                    self.first.step([-v for v in xs], back[x][0])
            s = sp
        if form == "member":
            back = [(f, tau, m.flip(eta)) for f, tau, eta in back]
        return s, back


def seed_test(run, form):
    out = {}
    fw = run.forward(form)
    start, end = tri7.board_digest(run.s0), tri7.board_digest(fw["end"])
    s_back, t_back = run.backward(form, fw["end"], fw["teeth"])
    birth = [run.member.birth() if form == "member" else (run.first.birth(),) for _ in range(run.sites)]
    out["i_board"] = tri7.board_digest(s_back) == start
    out["i_teeth"] = [tuple(list(v) for v in tt) for tt in t_back] == [tuple(list(v) for v in tt) for tt in birth]
    hid = (0, "eta", 0) if form == "member" else (0, "edge", 0)
    hw = run.forward(form, hidden=hid)
    lines_d = set(hw["lines"]) ^ set(fw["lines"])
    sides_d = set(hw["sides"]) ^ set(fw["sides"])
    out["ii_lines"] = len(lines_d)
    out["ii_sides"] = len(sides_d)
    out["ii_at"] = sorted({z[1] for z in sides_d} | {z[1] for z in lines_d})
    out["ii_first"] = min([z[0] for z in sides_d], default=None)
    out["ii_board"] = tri7.board_digest(hw["end"]) == end
    fc = run.forward("first")
    out["iii_board"] = tri7.board_digest(fc["end"]) == end
    out["start"], out["end"] = start[:16], end[:16]
    out["n_lines"], out["n_sides"] = len(fw["lines"]), len(fw["sides"])
    return out, fw


def mirror_each(run, flows):
    """The same act on the mirrored state at every Node-clock round: it must return the mirrored pre-state, every
    click negated."""
    m = run.member
    fails = 0
    teeth = [m.birth() for _ in range(run.sites)]
    for t in range(ROUNDS):
        for x in range(run.sites):
            f, tau, eta = teeth[x]
            pre = (list(f), list(tau), list(eta))
            q, w = m.step(flows[t][x], f, tau, eta)
            bf, btau, beta = list(f), list(tau), m.flip(eta)
            bq, bw = m.step([-v for v in flows[t][x]], bf, btau, beta)
            fails += int((bf, btau, m.flip(beta)) != pre or bq != [-c for c in q] or bw != [-c for c in w])
    return fails


def fresh_dist(v, M):
    """The carry's quotient of v at the dial M, its tooth drawn uniform on [0, M): {k: M - rho, k + 1: rho} over M."""
    k, rho = carry(v, M, 0)
    out = {k: M - rho}
    out[k + 1] = out.get(k + 1, 0) + rho
    return out


def convolve(d1, s1, d2, s2):
    out = {}
    for a, wa in d1.items():
        for b, wb in d2.items():
            z = s1 * a + s2 * b
            out[z] = out.get(z, 0) + wa * wb
    return out


def nonzero(d):
    return sum(w for z, w in d.items() if z)


def streams(run, flows, form):
    """Per Node-clock, the fresh-draw numerators of 'a click this round' per stream, with each stream's denominator."""
    m, D = run.member, run.D
    held = {tr: [(e, 1 if pr[0] == tr else -1) for e, pr in enumerate(run.pairs) if tr in pr] for tr in run.trains}
    held = {tr: v for tr, v in held.items() if v}
    out = {}
    for x in range(run.sites):
        for t in range(ROUNDS):
            xs = flows[t][x]
            if form == "first":
                de = {e: fresh_dist(xs[e], D) for e in range(len(run.pairs))}
                dens = {e: D for e in de}
                path = None
            else:
                y = [sum(sg * xs[e] for e, sg in col) for col in m.C]
                p = [m.g[e] * xs[e] - sum(sg * y[tt] for tt, sg in m.on[e]) for e in range(len(run.pairs))]
                de = {e: fresh_dist(p[e], m.dial[e]) for e in range(len(run.pairs))}
                dens = {e: m.dial[e] for e in de}
                path = [fresh_dist(y[tt], m.tdial[tt]) for tt in range(len(m.C))]
            for e in range(len(run.pairs)):
                if form == "first" or not m.on[e]:
                    d, den = de[e], dens[e]
                else:
                    tt, sg = m.on[e][0]
                    d, den = convolve(de[e], 1, path[tt], sg), dens[e] * m.tdial[tt]
                out.setdefault(("edge", run.pairs[e]), (den, {}))[1].setdefault(x, []).append(nonzero(d))
            for tr, es in held.items():
                d, den = {0: 1}, 1
                for e, sg in es:
                    d, den = convolve(d, 1, de[e], sg), den * dens[e]
                out.setdefault(("clock", tr), (den, {}))[1].setdefault(x, []).append(nonzero(d))
            if path is not None:
                for tt in range(len(m.C)):
                    out.setdefault(("path", tt), (m.tdial[tt], {}))[1].setdefault(x, []).append(nonzero(path[tt]))
    return out


def moments(nums, d):
    """Exact fresh-draw means and variances of the clicks N1, the pairs in two rounds running N2 and the triples N3,
    as numerators over d, d^2 (mean), d^2, d^4 (variance N2), d^3, d^6 (N3)."""
    T = len(nums)
    n = nums
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


def observed(events):
    """events: the set of (round, Node-clock) with a click on one stream: N1, N2, N3 and the pooled gaps."""
    by = {}
    for t, x in events:
        by.setdefault(x, set()).add(t)
    n1 = n2 = n3 = 0
    gaps = []
    for x, ts in by.items():
        n1 += len(ts)
        n2 += sum(1 for t in ts if t + 1 in ts)
        n3 += sum(1 for t in ts if t + 1 in ts and t + 2 in ts)
        st = sorted(ts)
        gaps += [b - a for a, b in zip(st, st[1:])]
    return n1, n2, n3, gaps


def lives(gaps):
    k, s1, s2 = len(gaps), sum(gaps), sum(g * g for g in gaps)
    return per_mille(k * s2 - s1 * s1, s1 * s1) if s1 else None


def z2(obs, e, v, dk):
    """(obs - e / dk)^2 over (v / dk^2), per mille: the deviation in standard errors, squared."""
    return per_mille((obs * dk - e) ** 2, v) if v else None


W64 = 1 << 64


def replicas(nums_by_x, d, R, seed):
    """Fresh draws: each round's click by a whole-number generator (Knuth's MMIX constants, the stand-in's) at the
    round's own rate n_t / d; per replica the pooled lives and N2; returns the sorted lives and N2."""
    r = seed
    out_l, out_2 = [], []
    for _ in range(R):
        gaps, n2 = [], 0
        for x, nums in nums_by_x.items():
            last, prev = None, False
            for t, a in enumerate(nums):
                r = carry(r * 6364136223846793005 + 1442695040888963407, W64, 0)[1]
                u = carry(r * d, W64, 0)[0]
                hit = u < a
                if hit:
                    if last is not None:
                        gaps.append(t - last)
                    last = t
                    n2 += int(prev)
                prev = hit
        lv = lives(gaps)
        out_l.append(-1 if lv is None else lv)
        out_2.append(n2)
    return sorted(out_l), sorted(out_2), r


def memory_table(run, rec, form, R, seed):
    st = streams(run, rec["flows"], form)
    ev = {}
    for (t, x, e, c) in rec["sides"]:
        ev.setdefault(("edge", run.pairs[e]), set()).add((t, x))
    for (t, x, tr, v) in rec["lines"]:
        ev.setdefault(("clock", tr), set()).add((t, x))
    for (t, x, i, v) in rec["paths"]:
        ev.setdefault(("path", i), set()).add((t, x))
    rows = []
    for key in sorted(st, key=str):
        d, by_x = st[key]
        e1 = v1 = e2 = v2 = e3 = v3 = 0
        for x, nums in by_x.items():
            a = moments(nums, d)
            e1, v1, e2, v2, e3, v3 = e1 + a[0], v1 + a[1], e2 + a[2], v2 + a[3], e3 + a[4], v3 + a[5]
        n1, n2, n3, gaps = observed(ev.get(key, set()))
        lv, l2, seed = replicas(by_x, d, R, seed)
        lo, mid, hi = lv[carry(R, 20, 0)[0]], lv[carry(R, 2, 0)[0]], lv[R - 1 - carry(R, 20, 0)[0]]
        rows.append((key, n1, carry(e1, d, 0)[0], z2(n1, e1, v1, d), n2, carry(e2, d * d, 0)[0], z2(n2, e2, v2, d * d),
                     n3, carry(e3, d ** 3, 0)[0], z2(n3, e3, v3, d ** 3), lives(gaps), len(gaps), lo, mid, hi,
                     l2[carry(R, 2, 0)[0]]))
    return rows, seed


def books(run, rec, form):
    """Each clock's booked total less floor(its swept passing / D), per Node-clock pooled, and the exact identity;
    each edge's net; the path's; the largest running |D booked - swept| per mille of a dial."""
    m, D = run.member, run.D
    pos = {tr: [(e, 1 if pr[0] == tr else -1) for e, pr in enumerate(run.pairs) if tr in pr] for tr in run.trains}
    pos = {tr: v for tr, v in pos.items() if v}
    sides = {}
    for (t, x, e, c) in rec["sides"]:
        sides[(t, x, e)] = c
    paths = {}
    for (t, x, i, v) in rec["paths"]:
        paths[(t, x, i)] = v
    clock_b = {tr: 0 for tr in pos}
    clock_s = {tr: 0 for tr in pos}
    edge_b = [0] * len(run.pairs)
    edge_s = [0] * len(run.pairs)
    path_b, path_s = [0] * len(m.C), [0] * len(m.C)
    run_c, run_e = {tr: 0 for tr in pos}, [0] * len(run.pairs)
    ident_bad = 0
    for x in range(run.sites):
        rc = {tr: 0 for tr in pos}
        re_ = [0] * len(run.pairs)
        qc = {tr: 0 for tr in pos}
        xc = {tr: 0 for tr in pos}
        for t in range(ROUNDS):
            xs = rec["flows"][t][x]
            for e in range(len(run.pairs)):
                c = sides.get((t, x, e), 0)
                edge_b[e] += c
                edge_s[e] += xs[e]
                re_[e] += D * c - xs[e]
                run_e[e] = max(run_e[e], abs(re_[e]))
            for tr, es in pos.items():
                c = sum(sg * sides.get((t, x, e), 0) for e, sg in es)
                sw = sum(sg * xs[e] for e, sg in es)
                clock_b[tr] += c
                clock_s[tr] += sw
                qc[tr] += c
                xc[tr] += sw
                rc[tr] += D * c - sw
                run_c[tr] = max(run_c[tr], abs(rc[tr]))
            if form != "first":
                y = [sum(sg * xs[e] for e, sg in col) for col in m.C]
                for i in range(len(m.C)):
                    path_b[i] += paths.get((t, x, i), 0)
                    path_s[i] += y[i]
        # the exact identity at this Node-clock: (dial) Q + (oriented end teeth) = (oriented birth teeth) + (factor) X
        f_end = rec["teeth"][x][0]
        for tr, es in pos.items():
            if form == "first":
                lhs = D * qc[tr] + sum(sg * f_end[e] for e, sg in es)
                rhs = sum(sg * run.first.born for e, sg in es) + xc[tr]
            else:
                g = m.g[es[0][0]]
                lhs = g * D * qc[tr] + sum(sg * f_end[e] for e, sg in es)
                rhs = sum(sg * m.born[e] for e, sg in es) + g * xc[tr]
            ident_bad += int(lhs != rhs)
    bk = {tr: clock_b[tr] - carry(clock_s[tr], D, 0)[0] for tr in pos}
    ek = [edge_b[e] - carry(edge_s[e], D, 0)[0] for e in range(len(run.pairs))]
    pk = [path_b[i] - carry(path_s[i], m.tdial[i], 0)[0] for i in range(len(m.C))] if form != "first" else None
    return {"clock_less_swept": bk, "clock_run_max_pm": {tr: per_mille(v, D) for tr, v in run_c.items()},
            "identity_fails": ident_bad, "edge_booked": edge_b, "edge_less_swept": ek,
            "edge_run_max_pm": [per_mille(v, D) for v in run_e], "path_booked": path_b, "path_less_swept": pk,
            "teeth_hold": 2 * run.sites}


def main():
    run = Run("click")
    print(f"THIRD7 board7: {ROUNDS} rounds, {run.sites} Node-clocks; the star: {run.star}; key {run.key}; D = (Spokes div"
          f" senses) x key = {run.D}; edges {run.pairs}, triangles {run.triangles}; C per triangle {run.member.C};"
          f" G = C^T C {run.member.G}; edge dials {run.member.dial} (born {run.member.born}); the triangle's dial"
          f" {run.member.tdial} (born {run.member.tborn})")
    check = [0]
    # 1. the owner's seed test, member and control
    seeds = {}
    recs = {}
    for form in ("member", "first"):
        out, rec = seed_test(run, form)
        seeds[form] = out
        recs[form] = rec
    for form in ("member", "first"):
        o = seeds[form]
        print(f"SEED {form}: start board {o['start']} end board {o['end']}; {o['n_lines']} lines, {o['n_sides']} sides;"
              f" (i) from the end seed alone: board back {o['i_board']}, every tooth and twin back {o['i_teeth']};"
              f" (ii) one hidden unit ({'the twin eta' if form == 'member' else 'edge 0 tooth'}) at Node-clock 0: lines"
              f" apart {o['ii_lines']}, sides apart {o['ii_sides']} from round {o['ii_first']}, at Node-clocks"
              f" {o['ii_at']}, the same end board {o['ii_board']}; (iii) the first click's end board the same"
              f" {o['iii_board']}")
    rec = recs["member"]
    fl = rec["flows"]
    # the star-read split against David's, at every Node-clock round
    chk = [0]
    s = run.s0
    for t in range(ROUNDS):
        s1, _ = step.act(run.lay, s)
        for x in range(run.sites):
            run.flows_at(s, s1, x, chk)
        s = s1
    print(f"SPLIT: the split read from the star (half {run.star['half']}, third {run.star['third']}) against David's"
          f" own (KAPPA 6 div 2, div 3): Node-clock rounds apart {chk[0]} of {ROUNDS * run.sites}")
    unt = run.forward("unturned")
    print(f"UNTURNED (the member with its twin left out, a control): lines apart from the member's"
          f" {len(set(unt['lines']) ^ set(rec['lines']))}; sides apart {len(set(unt['sides']) ^ set(rec['sides']))};"
          f" landings apart {len(set(unt['paths']) ^ set(rec['paths']))}")
    # 2. the mirror at every Node-clock round
    print(f"MIRROR: the same act on the mirrored state fails at {mirror_each(run, fl)} of {ROUNDS * run.sites} Node-clock"
          f" rounds")
    # 3. the swap and the name swap
    SW = {3: 4, 4: 3}
    for wname in ("swap", "names"):
        r2 = Run(wname)
        for form in ("member", "first"):
            ro = run.forward(form) if form == "first" else rec
            rs = r2.forward(form)
            if wname == "swap":
                ml = sorted((t, x, SW.get(tr, tr), v) for (t, x, tr, v) in ro["lines"])
                emap = {}
                for e, pr in enumerate(run.pairs):
                    a, b = SW.get(pr[0], pr[0]), SW.get(pr[1], pr[1])
                    emap[e] = (r2.pairs.index((a, b)), 1) if a < b else (r2.pairs.index((b, a)), -1)
                ms = sorted((t, x, emap[e][0], emap[e][1] * c) for (t, x, e, c) in ro["sides"])
                mp = sorted((t, x, i, -v) for (t, x, i, v) in ro["paths"])
            else:
                ml, ms, mp = sorted(ro["lines"]), sorted(ro["sides"]), sorted(ro["paths"])
            dl = len(set(ml) ^ set(rs["lines"]))
            ds = len(set(ms) ^ set(rs["sides"]))
            dp = len(set(mp) ^ set(rs["paths"]))
            print(f"{'SWAP' if wname == 'swap' else 'NAMES'} {form}: lines apart {dl} of {len(ro['lines'])}; sides apart"
                  f" {ds} of {len(ro['sides'])}; landings apart {dp} of {len(ro['paths'])}; the trains' names in the"
                  f" world's order {[t['name'] for t in r2.universe['trains']]}")
    # 4. the books
    for form in ("member", "first"):
        b = books(run, recs[form], form)
        print(f"BOOKS {form}: each clock's booked total less floor(swept / D) {b['clock_less_swept']} (two teeth at 27"
              f" Node-clocks hold under {b['teeth_hold']}); the largest running |D booked - swept| at one Node-clock, per"
              f" mille of a dial {b['clock_run_max_pm']}; the exact identity fails at {b['identity_fails']} of"
              f" {3 * run.sites}; edges booked {b['edge_booked']}, less floor(swept / D) {b['edge_less_swept']}, running"
              f" at most {b['edge_run_max_pm']} per mille of a dial; the path booked {b['path_booked']}, less floor(its"
              f" circulating passing / G D) {b['path_less_swept']}")
    # 5. memory and lives against fresh draws
    seed = 17
    for form, r_ in (("member", rec), ("unturned", unt), ("first", recs["first"])):
        rows, seed = memory_table(run, r_, "first" if form == "first" else "member", REPL, seed)
        for row in rows:
            (key, n1, e1, z1, n2, e2, z2_, n3, e3, z3, lv, ng, lo, mid, hi, m2) = row
            print(f"MEMORY {form} {key[0]} {key[1]}: clicks {n1} against {e1} fresh (z^2 {z1} per mille); two rounds"
                  f" running {n2} against {e2} (z^2 {z2_}); three {n3} against {e3} (z^2 {z3}); lives {lv} per mille"
                  f" over {ng} gaps, fresh draws' {mid} (90 per cent of {REPL} replicas within {lo} to {hi}); the"
                  f" replicas' median two-running {m2}")
    # 6. Big Pic's bench
    sys.path.insert(0, str(HERE.joinpath("bp")))
    import edgeclick as E

    for mode, form in ((11, "member"), (0, "first")):
        bp = E.run(SRC, "tensor24-click", ROUNDS, mode)
        mine = tri7.digest((recs[form]["lines"], recs[form]["sides"]))
        print(f"BIGPIC mode {mode}: his digest {bp['digest'][:16]}, mine {mine[:16]}, alike {bp['digest'] == mine};"
              f" his run back {bp['runback']}")
    # where the path shows
    land = rec["paths"]
    by_x = {}
    for (t, x, i, v) in land:
        by_x.setdefault(x, []).append(v)
    ups = sum(1 for z in land if z[3] > 0)
    downs = sum(1 for z in land if z[3] < 0)
    gross = [sum(abs(c) for (t, x, e, c) in recs[f]["sides"] if e == i) for f in ("member", "first") for i in range(3)]
    print(f"PATH: {len(land)} landings at {len(by_x)} Node-clocks over {ROUNDS} rounds, {ups} one way round (+) and"
          f" {downs} the other (-); per mille of the Node-clock rounds {per_mille(len(land), ROUNDS * run.sites)};"
          f" the sides' gross quanta per edge, member {gross[:3]}, first click {gross[3:]}")


main()
