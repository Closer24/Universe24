"""THIRD7's toy: one triangle of three alike clocks 0, 1, 2 (edges (0, 1), (0, 2), (1, 2); the triangle (ga, ab, gb) =
((0, 1), (1, 2), (0, 2)), C = +1, +1, -1), the member (tri7.Member, the board's own code) at the click world's dial, read
from the star and the world's key; steady passings x_ga, x_gb, x_ab in whole m = D div 50 (the Boss's stand-ins, a toy's
pick, never the board's). Whole numbers only; every division the carry.

Read: the same act on the mirrored state every round; each clock's exact identity every round; the swap of clocks 1 and
2 and every one of the six relabellings draw by draw; per stream (the path's landings, each clock's line, each edge's
side) after one click the next and after two in a row a third, against independent clicks at the stream's fresh-draw
rate (every tooth drawn fresh each round, the passing given; exact) and at its measured rate, z^2 per mille; the lives
against the geometric law at the fresh-draw rate; R2 within one record (does the last L values ever repeat with a
different next value). argv: src, rounds, lay (birth or standin), x_ga, x_gb, x_ab (in m), checks (all or mem)."""
import json
import sys
from pathlib import Path

SRC, R, LAY = sys.argv[1], int(sys.argv[2]), sys.argv[3]
XM = [int(v) for v in sys.argv[4:7]]
CHECKS = sys.argv[7] if len(sys.argv) > 7 else "all"
VARIANT = sys.argv[8] if len(sys.argv) > 8 else "member"  # member; tooth (the half's other order); k1 (K = 1)
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import tri7  # noqa: E402

tri7.setup(SRC)
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.runner import load as loading  # noqa: E402

world = Path(SRC).parent.joinpath("examples", "tensor24-click")
key = json.loads(world.joinpath("universe.json").read_text())["chosen"]["key"]
axes = len(json.loads(world.joinpath("piece.json").read_text())["shape"])
spokes = len(loading.star(axes))
senses = carry(spokes, axes, 0)[0]
D = carry(spokes, senses, 0)[0] * key
m50 = carry(D, 50, 0)[0]
PAIRS = [(0, 1), (0, 2), (1, 2)]
IDX = {p: i for i, p in enumerate(PAIRS)}
TRI = [(IDX[(0, 1)], IDX[(1, 2)], IDX[(0, 2)])]
X = [0] * 3
X[IDX[(0, 1)]], X[IDX[(0, 2)]], X[IDX[(1, 2)]] = XM[0] * m50, XM[1] * m50, XM[2] * m50
class Variant(tri7.Member):
    """The member, or a named contrast: 'tooth' runs the half's other order (tau's shear first, then eta's); 'k1' turns
    the pair at the bare unit K = 1 (road 3's coupling) in place of K = G."""

    def __init__(self, *a, variant="member"):
        super().__init__(*a)
        self.variant = variant
        self.k = [1 for _ in self.G] if variant == "k1" else list(self.G)

    def shear(self, dst, src, t):
        b = self.tborn[t]
        return b + self.cen(dst - b + self.k[t] * (src - b), t)

    def step(self, x, f, tau, eta, turned=True):
        if self.variant != "tooth":
            return super().step(x, f, tau, eta, turned)
        carry_ = self.carry
        y = [sum(sg * x[e] for e, sg in col) for col in self.C]
        p = [self.g[e] * x[e] - sum(sg * y[t] for t, sg in self.on[e]) for e in range(self.n)]
        for t in range(len(self.C)):
            tau[t] = self.shear(tau[t], eta[t], t)
            eta[t] = self.shear(eta[t], tau[t], t)
        q = [0] * self.n
        for e in range(self.n):
            q[e], f[e] = carry_(p[e], self.dial[e], f[e])
        w = []
        for t, col in enumerate(self.C):
            wt, tau[t] = carry_(y[t], self.tdial[t], tau[t])
            w.append(wt)
            for e, sg in col:
                q[e] += sg * wt
        for t in range(len(self.C)):
            eta[t] = self.shear(eta[t], tau[t], t)
            tau[t] = self.shear(tau[t], eta[t], t)
        return q, w


M = Variant(3, TRI, D, senses, variant=VARIANT)
BV = {v: [(e, 1 if p[0] == v else -1) for e, p in enumerate(PAIRS) if v in p] for v in range(3)}
W64 = 1 << 64


def per_mille(n, d):
    return carry(1000 * n, d, 0)[0] if d else None


def lay():
    f, tau, eta = M.birth()
    if LAY == "standin":
        r = 17
        vals = []
        for d in M.dial + M.tdial + M.tdial:
            r = carry(r * 6364136223846793005 + 1442695040888963407, W64, 0)[1]
            vals.append(carry(r * d, W64, 0)[0])
        f, tau, eta = vals[:3], vals[3:4], vals[4:5]
    return f, tau, eta


def lines_of(q):
    return [sum(sg * q[e] for e, sg in BV[v]) for v in range(3)]


def run(x, f, tau, eta, rounds, mirror=False, books=False):
    """The record (sides, lines, landings per round); with mirror, the same act on the mirrored state checked each
    round; with books, each clock's identity checked each round."""
    S, L, Wl = [], [], []
    fails = bad = 0
    f0 = list(f)
    Q = [0, 0, 0]
    Xc = [0, 0, 0]
    for _ in range(rounds):
        if mirror:
            pre = (list(f), list(tau), list(eta))
        q, w = M.step(x, f, tau, eta)
        if mirror:
            bf, bt, be = list(f), list(tau), M.flip(eta)
            bq, bw = M.step([-v for v in x], bf, bt, be)
            fails += int((bf, bt, M.flip(be)) != pre or bq != [-c for c in q] or bw != [-c for c in w])
        ln = lines_of(q)
        if books:
            for v in range(3):
                Q[v] += ln[v]
                Xc[v] += sum(sg * x[e] for e, sg in BV[v])
                g = M.g[BV[v][0][0]]
                lhs = g * D * Q[v] + sum(sg * f[e] for e, sg in BV[v])
                rhs = sum(sg * f0[e] for e, sg in BV[v]) + g * Xc[v]
                bad += int(lhs != rhs)
        S.append(q)
        L.append(ln)
        Wl.append(w[0])
    return S, L, Wl, fails, bad


def fresh_dist(v, Md):
    k, rho = carry(v, Md, 0)
    out = {k: Md - rho}
    out[k + 1] = out.get(k + 1, 0) + rho
    return out


def convolve(d1, d2, s2):
    out = {}
    for a, wa in d1.items():
        for b, wb in d2.items():
            z = a + s2 * b
            out[z] = out.get(z, 0) + wa * wb
    return out


def fresh_rates(x):
    """Each stream's fresh-draw rate of 'a click this round', exact: (numerator, denominator)."""
    y = sum(sg * x[e] for e, sg in M.C[0])
    p = [M.g[e] * x[e] - sum(sg * y for t, sg in M.on[e]) for e in range(3)]
    de = [fresh_dist(p[e], M.dial[e]) for e in range(3)]
    dp = fresh_dist(y, M.tdial[0])
    out = {"path": (sum(w for z, w in dp.items() if z), M.tdial[0])}
    for e in range(3):
        sg = M.on[e][0][1]
        d = convolve(de[e], dp, sg)
        out[f"edge {PAIRS[e]}"] = (sum(w for z, w in d.items() if z), M.dial[e] * M.tdial[0])
    for v in range(3):
        d, den = {0: 1}, 1
        for e, sg in BV[v]:
            d, den = convolve(d, de[e], sg), den * M.dial[e]
        out[f"clock {v}"] = (sum(w for z, w in d.items() if z), den)
    return out, y


def memory(vals, a, d):
    S = [v != 0 for v in vals]
    n = len(S)
    c = sum(S)
    one = sum(1 for t in range(1, n) if S[t - 1])
    after1 = sum(1 for t in range(1, n) if S[t - 1] and S[t])
    two = sum(1 for t in range(2, n) if S[t - 1] and S[t - 2])
    three = sum(1 for t in range(2, n) if S[t - 1] and S[t - 2] and S[t])
    z1 = per_mille((after1 * d - one * a) ** 2, one * a * (d - a)) if one and a and d - a else None
    z2 = per_mille((three * d - two * a) ** 2, two * a * (d - a)) if two and a and d - a else None
    m1 = carry(one * c, n, 0)[0]
    m2 = carry(two * c, n, 0)[0]
    idx = [t for t in range(n) if S[t]]
    g = [b - a_ for a_, b in zip(idx, idx[1:])]
    s1, s2 = sum(g), sum(z * z for z in g)
    lv = per_mille(len(g) * s2 - s1 * s1, s1 * s1) if s1 else None
    return {"clicks": c, "fresh_rate_pm": per_mille(a, d), "after1": after1, "one": one,
            "after1_fresh": carry(one * a, d, 0)[0], "after1_measured": m1, "z1_pm": z1, "after2": three, "two": two,
            "after2_fresh": carry(two * a, d, 0)[0], "after2_measured": m2, "z2_pm": z2, "lives_pm": lv,
            "geometric_pm": per_mille(d - a, d), "net": sum(vals)}


def r2_within(vals, Ls=(1, 2, 3, 4, 6, 8, 12, 16)):
    """For each L: whether some last-L history is followed by two different next values (the past does not fix the
    landing), and the number of histories seen."""
    out = []
    for Lh in Ls:
        nxt = {}
        for t in range(Lh, len(vals)):
            h = tuple(vals[t - Lh:t])
            nxt.setdefault(h, set()).add(vals[t])
        out.append((Lh, any(len(s) > 1 for s in nxt.values()), len(nxt)))
    return out


def relabel(pi, x, f, tau, eta):
    """The world relabelled by pi (old clock v becomes pi[v]): flows, teeth and the triangle's pair mapped; returns the
    new state and the maps (edge e -> (e', o_e)), sigma (the triangle's orientation)."""
    emap = {}
    x2, f2 = [0] * 3, [0] * 3
    for e, (i, j) in enumerate(PAIRS):
        a, b = pi[i], pi[j]
        e2, o = (IDX[(a, b)], 1) if a < b else (IDX[(b, a)], -1)
        emap[e] = (e2, o)
        x2[e2] = o * x[e]
        f2[e2] = f[e] if o == 1 else M.dial[e] - 1 - f[e]
    mapped = [0] * 3
    for e, sg in M.C[0]:
        e2, o = emap[e]
        mapped[e2] = o * sg
    new_c = [0] * 3
    for e, sg in M.C[0]:
        new_c[e] = sg
    sigma = 1 if mapped == new_c else -1
    assert mapped == [sigma * v for v in new_c]
    tau2 = list(tau) if sigma == 1 else [M.tdial[0] - 1 - tau[0]]
    eta2 = list(eta) if sigma == 1 else [M.tdial[0] - 1 - eta[0]]
    return x2, f2, tau2, eta2, emap, sigma


def main():
    f, tau, eta = lay()
    rates, y = fresh_rates(X)
    print(f"toy7: dial D = {D} (the star: Spokes {spokes}, senses {senses}; key {key}), m = D div 50 = {m50}; C {M.C},"
          f" G {M.G}, the edges' dial {M.dial}, the triangle's {M.tdial}; passings (ga, gb, ab) = {XM} m, so y = C^T x ="
          f" {y} ({carry(y * 1000, M.tdial[0], 0)[0]} per mille of the triangle's dial); {R} rounds from the {LAY} lay;"
          f" the form: {VARIANT} (the pair's coupling {M.k})")
    S, L, Wl, fails, bad = run(X, list(f), list(tau), list(eta), R, mirror=CHECKS == "all", books=True)
    if CHECKS == "all":
        print(f"  the same act on the mirrored state fails at {fails} of {R} rounds; each clock's identity fails at {bad}"
              f" of {3 * R} clock rounds")
        for pi in ((0, 1, 2), (0, 2, 1), (1, 0, 2), (2, 1, 0), (1, 2, 0), (2, 0, 1)):
            x2, f2, t2, e2, emap, sigma = relabel(pi, X, f, tau, eta)
            S2, L2, W2, _, _ = run(x2, f2, t2, e2, R)
            bad_s = sum(1 for a, b in zip(S, S2) if any(b[emap[e][0]] != emap[e][1] * a[e] for e in range(3)))
            bad_l = sum(1 for a, b in zip(L, L2) if any(b[pi[v]] != a[v] for v in range(3)))
            bad_w = sum(1 for a, b in zip(Wl, W2) if b != sigma * a)
            print(f"  relabelled by {pi} (orientation {sigma:+d}): rounds apart in sides {bad_s}, in lines {bad_l}, in"
                  f" landings {bad_w}, of {R}")
    else:
        print(f"  each clock's identity fails at {bad} of {3 * R} clock rounds")
    streams = {"path": Wl}
    for v in range(3):
        streams[f"clock {v}"] = [ln[v] for ln in L]
    for e in range(3):
        streams[f"edge {PAIRS[e]}"] = [q[e] for q in S]
    for name, vals in streams.items():
        a, d = rates[name]
        mm = memory(vals, a, d)
        print(f"  {name}: {mm['clicks']} clicks (net {mm['net']}), fresh-draw rate {mm['fresh_rate_pm']} per mille; after"
              f" one the next {mm['after1']} of {mm['one']} against {mm['after1_fresh']} fresh ({mm['after1_measured']}"
              f" at the measured rate; z^2 {mm['z1_pm']} per mille); after two a third {mm['after2']} of {mm['two']}"
              f" against {mm['after2_fresh']} fresh ({mm['after2_measured']}; z^2 {mm['z2_pm']}); lives {mm['lives_pm']}"
              f" per mille, the geometric law's {mm['geometric_pm']}")
        if CHECKS == "all":
            print(f"     R2 within one record (L, the past leaves the landing open, histories): {r2_within(vals)}")


main()
