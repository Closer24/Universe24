"""Memory in the third click's turn, on one triangle with steady passings (the Boss's toy, #2187 6539448771 item 2,
rebuilt here in whole numbers): the dial 3 K at the click world's key, born at the middle; x_ga = x_gb = 9 m and
x_ab = 12 m with m = D div 50; per edge, after one click the next, and after two in a row a third, against the
counts that independent draws at the edge's own rate would give; the lives' variance over their mean squared against
the geometric law's 1 - p; the swap draw by draw and the same act on the mirrored state.

Modes: 0 no turn; 4 C C^T off its diagonal; 5 road 3, C C^T's diagonal; 6 the THIRD deriver's coupled member of five
blocks (the smallest largest entry), for the cross-check.

Usage: python3 -I toymem.py <src> [rounds, 200000 unless given] [modes, 0456 unless given] [memonly]
"""
import sys

sys.path.insert(0, sys.argv[1])
sys.path.insert(0, ".")
import edgeclick as E  # noqa: E402
from tensor24.algebra.carry import carry  # noqa: E402

ROUNDS = int(sys.argv[2]) if len(sys.argv) > 2 else 200000
MODES = E.modes_of("0456" if len(sys.argv) <= 3 else sys.argv[3])
universe, shape, held, lay, s, world = E.load_world(sys.argv[1], "tensor24-click")
ed = E.Edges(world, int(lay.click.key[0, 0]), 1, [t["kinds"] for t in universe["trains"]])
D, B = ed.dial, ed.born
ga, ab, gb = ed.triangles[0]
m, _ = carry(D, 50, 0)
X = {ga: 9 * m, gb: 9 * m, ab: 12 * m}
n = len(ed.pairs)
G1, G2, G3 = ("g", ga), ("g", gb), ("g", ab)
H1, H2, H3 = ("h", ga), ("h", gb), ("h", ab)
FIVE = [(G1, H1, 1), (G2, H2, 1), (G1, H3, 1), (G2, H3, -1), (G3, H1, 1), (G3, H2, -1), (H1, G2, 1), (H2, G1, 1), (H3, G3, -1)]
NAMES = {0: "no turn", 4: "C C^T off its diagonal", 5: "road 3, C C^T's diagonal", 6: "the THIRD deriver's five blocks",
         7: "the circulation, h += C C^T off its diagonal of g", 8: "the circulation, h += C C^T g",
         9: "mode 7 with the shears' quotients booked", 10: "the full C C^T with the shears' quotients booked",
         11: "the triangle's own tooth, one whole circulation per quantum"}


def order(mode):
    return [] if mode == 0 else (FIVE if mode == 6 else ed.forward(mode))


def run11(flows, rounds):
    import circ

    st = circ.Stepper(ed)
    state = st.born()
    return [st.step(list(flows), *state) for _ in range(rounds)]


def run(mode, flows, rounds, u=None, w=None):
    if mode == 11:
        return run11(flows, rounds), None, None
    u = [B] * n if u is None else u
    w = [B] * n if w is None else w
    fw = order(mode)
    bw = list(reversed(fw))
    qs = []
    for _ in range(rounds):
        book = [0] * n if mode >= 9 else None
        ed.shear_all(u, w, fw, book)
        row = []
        for e in range(n):
            q, u[e] = carry(flows[e], D, u[e])
            row.append(q)
        ed.shear_all(u, w, bw, book)
        if book is not None:
            row = [r + b for r, b in zip(row, book)]
        qs.append(row)
    return qs, u, w


def per_mille(a, b):
    return carry(1000 * a, b, 0)[0] if b else None


print(f"dial {D} (3 K, K the click world's key), born {B}, m = D div 50 = {m}; steady passings {[X[e] for e in range(n)]} on {ed.pairs}; {ROUNDS} rounds")
flows = [X[e] for e in range(n)]
MEMONLY = len(sys.argv) > 4 and sys.argv[4] == "memonly"
for mode in MODES:
    qs, u, w = run(mode, flows, ROUNDS)
    if MEMONLY:
        print(f" {NAMES[mode]}:")
    # the swap draw by draw: P exchanges ga and gb and reads ab from its other end
    if not MEMONLY:
        pf = list(flows)
        pf[ga], pf[gb], pf[ab] = flows[gb], flows[ga], -flows[ab]
        ps, _, _ = run(mode, pf, ROUNDS)
        swap_bad = sum(1 for a, b in zip(qs, ps) if (b[ga], b[gb], b[ab]) != (a[gb], a[ga], -a[ab]))
        # the same act on the mirrored state, every passing negated, then the mirror again: it must reach the lay
        mu, mw = list(u), [B + ed.cen(-(v - B)) for v in w]
        run(mode, [-f for f in flows], ROUNDS, mu, mw)
        back = mu == [B] * n and [B + ed.cen(-(v - B)) for v in mw] == [B] * n
        print(f" {NAMES[mode]}: the swap draw by draw fails at {swap_bad} of {ROUNDS} rounds; the same act on the mirrored state runs back to the lay: {back}")
    tri = sorted({t for e in (ga, ab, gb) for t in ed.pairs[e]})
    lines = {tr: [sum(row[e] * ((ed.pairs[e][0] == tr) - (ed.pairs[e][1] == tr)) for e in range(n)) for row in qs] for tr in tri}
    for tr in tri:
        c = [int(v != 0) for v in lines[tr]]
        n1 = sum(c)
        n11 = sum(1 for t in range(1, ROUNDS) if c[t] and c[t - 1])
        n111 = sum(1 for t in range(2, ROUNDS) if c[t] and c[t - 1] and c[t - 2])
        e11, _ = carry(n1 * n1, ROUNDS, 0)
        e111, _ = carry(n11 * n1, ROUNDS, 0)
        net = sum(lines[tr])
        print(f"   clock {tr}'s line: {n1} rounds with a click (net {net} quanta); after one the next {n11} against {e11} independent;"
              f" after two in a row a third {n111} against {e111}")
    for e in (ga, ab, gb):
        c = [row[e] for row in qs]
        n1 = sum(c)
        n11 = sum(1 for t in range(1, ROUNDS) if c[t] and c[t - 1])
        n111 = sum(1 for t in range(2, ROUNDS) if c[t] and c[t - 1] and c[t - 2])
        e11, _ = carry(n1 * n1, ROUNDS, 0)
        e111, _ = carry(n11 * n1, ROUNDS, 0)
        lives, last = [], None
        for t in range(ROUNDS):
            if c[t]:
                if last is not None:
                    lives.append(t - last)
                last = t
        k, s1, s2 = len(lives), sum(lives), sum(d * d for d in lives)
        vm = per_mille(k * s2 - s1 * s1, s1 * s1)
        geo = 1000 - per_mille(n1, ROUNDS)
        print(f"   edge {ed.pairs[e]}: {n1} clicks; after one click the next {n11} against {e11} independent;"
              f" after two in a row a third {n111} against {e111}; lives' variance over mean squared {vm} per mille, the geometric law's {geo}")
