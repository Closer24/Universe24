"""Mode 11, the triangle's own tooth (#2187 6539806523 item 3; THIRD7's road; the owner's word of 06:0x UTC that the
third click is never seen alone): the circulation lands one whole quantum around the triangle at once.

- Each triangle's circulating passing is y = c . x, c the triangle's boundary (+1, +1, -1). The passing splits by the
  structure with no division: 3 x = (3 x - C C^T x) + C C^T x.
- Each edge tooth carries 3 x_e - (C C^T x)_e, unturned, at the dial 3D (D the edge dial, 3 the triangle's edge count,
  C^T C); a lone edge carries 3 x_e there, which is the first click at the dial D exactly (born 3 born + 1).
- Each triangle has its own tooth tau, kept by the mirror, and its twin eta, flipped, both born at the dial 3D's middle.
  Each round they turn by the palindrome at K = C^T C = 3 (eta += 3 tau, tau += 3 eta; the carries; tau += 3 eta,
  eta += 3 tau), and tau carries y. Each quantum W it lands books c_e W on every edge e of the triangle in the same
  round: +W, +W and -W along the boundary.
- So each clock's line is the carry of its own passing alone: Sum_e B_ie (3 x_e - c_e y) = 3 Sum_e B_ie x_e, as B c = 0,
  and the circulation's quantum cancels in every clock's line: no clock sees it alone. An idle triangle (y = 0) lands
  none. The choice is the path: which way round each quantum goes, read in the sides.

hidden=(site, e) lays one unit in the twin of the first triangle that edge e lies on, at that site (the hidden part).
"""
import hashlib
import sys

if __name__ == "__main__":
    sys.path.insert(0, sys.argv[1])
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import step  # noqa: E402


class Stepper:
    """One Node-clock's teeth under mode 11: the edge teeth at the dial 3D, each triangle's tooth and its twin."""

    def __init__(self, ed):
        self.ed = ed
        self.n = len(ed.pairs)
        self.D3 = 3 * ed.dial
        self.B3, _ = carry(self.D3 - 1, 2, 0)
        self.sign = [{ga: 1, ab: 1, gb: -1} for ga, ab, gb in ed.triangles]

    def cen(self, v):
        _, r = carry(v + self.B3, self.D3, 0)
        return r - self.B3

    def shear(self, dst, src, k):
        return self.B3 + self.cen(dst - self.B3 + k * (src - self.B3))

    def born(self):
        return [self.B3] * self.n, [self.B3] * len(self.sign), [self.B3] * len(self.sign)

    def flip(self, es):
        return [self.B3 + self.cen(-(v - self.B3)) for v in es]

    def step(self, fl, gs, ts, es):
        """One round's teeth for the passings fl (one per edge); returns each edge's quanta booked."""
        sign, n, D3 = self.sign, self.n, self.D3
        ys = [sum(sg * fl[e] for e, sg in sign[t].items()) for t in range(len(sign))]
        p = [3 * fl[e] - sum(sign[t].get(e, 0) * ys[t] for t in range(len(sign))) for e in range(n)]
        for t in range(len(sign)):
            es[t] = self.shear(es[t], ts[t], 3)
            ts[t] = self.shear(ts[t], es[t], 3)
        qe = [0] * n
        for e in range(n):
            qe[e], gs[e] = carry(p[e], D3, gs[e])
        self.last_w = []
        for t in range(len(sign)):
            w, ts[t] = carry(ys[t], D3, ts[t])
            self.last_w.append(w)
            for e, sg in sign[t].items():
                qe[e] += sg * w
        for t in range(len(sign)):
            ts[t] = self.shear(ts[t], es[t], 3)
            es[t] = self.shear(es[t], ts[t], 3)
        return qe


def run_circ(lay, s, world, rounds, hidden=None, kinds_of=None, E=None):
    rows, sites = s.a.shape
    key = int(lay.click.key[0, 0])
    ed = E.Edges(world, key, sites, kinds_of)
    st = Stepper(ed)
    n = st.n
    teeth = [st.born() for _ in range(sites)]
    if hidden is not None:
        x, e = hidden
        on = [t for t in range(len(st.sign)) if e in st.sign[t]]
        for t in on[:1]:
            teeth[x][2][t] = st.B3 + st.cen(teeth[x][2][t] - st.B3 + 1)
    lay_state = [tuple(list(v) for v in tt) for tt in teeth]
    lines, sides, flows = [], [], []
    books_open = places = 0
    for t_ in range(rounds):
        s1, _ = step.act(lay, s)
        round_flows = []
        for x in range(sites):
            b = [int(s.b[r, x]) for r in range(rows)]
            a = [int(s.a[r, x]) for r in range(rows)]
            a1 = [int(s1.a[r, x]) for r in range(rows)]
            fl_d = world.split_flows(0, b, a, a1)
            fl = [fl_d.get(pr, 0) for pr in ed.pairs]
            round_flows.append(fl)
            qe = st.step(fl, *teeth[x])
            q = {tr: 0 for tr in world.trains}
            for e, pr in enumerate(ed.pairs):
                q[pr[0]] += qe[e]
                q[pr[1]] -= qe[e]
                if qe[e]:
                    sides.append((t_, x, e, qe[e]))
            if any(q.values()):
                places += 1
                books_open += int(sum(q.values()) != 0)
            for tr, v in q.items():
                if v:
                    lines.append((t_, x, tr, v))
        flows.append(round_flows)
        s = s1
    # the run back by the board's law: the same act on the mirrored state (twins flipped, every passing negated)
    back = [(list(gs), list(ts), st.flip(es)) for gs, ts, es in teeth]
    for t_ in range(rounds - 1, -1, -1):
        for x in range(sites):
            st.step([-f for f in flows[t_][x]], *back[x])
    back = [(gs, ts, st.flip(es)) for gs, ts, es in back]
    runback = back == lay_state
    digest = hashlib.sha256(repr((lines, sides)).encode()).hexdigest()
    return {"sites": sites, "trains": world.trains, "pairs": ed.pairs, "triangles": ed.triangles, "key": key,
            "dial": ed.dial, "tooth_dial": st.D3, "born": st.B3, "rounds": rounds, "turned": 11, "lines": lines,
            "sides": sides, "flows": flows, "places": places, "books_open": books_open, "runback": runback,
            "digest": digest, "mirror": runback}


if __name__ == "__main__":
    # the circulation's own quanta in the Boss's toy (#2187 6539448771 item 2: the dial 3K, steady passings 9m, 9m
    # and 12m, m = D div 50): after one landing the next, after two a third, against independent landings at the
    # circulation's own rate; and the lives against the geometric law
    sys.path.insert(0, ".")
    import edgeclick as E

    rounds = int(sys.argv[2]) if len(sys.argv) > 2 else 200000
    universe, shape, held, lay, s0, world = E.load_world(sys.argv[1], "tensor24-click")
    ed = E.Edges(world, int(lay.click.key[0, 0]), 1, [t["kinds"] for t in universe["trains"]])
    st = Stepper(ed)
    m, _ = carry(ed.dial, 50, 0)
    ga, ab, gb = ed.triangles[0]
    fl = [0] * st.n
    fl[ga], fl[gb], fl[ab] = 9 * m, 9 * m, 12 * m
    state = st.born()
    ws = []
    for _ in range(rounds):
        st.step(fl, *state)
        ws.append(st.last_w[0])
    c = [int(w != 0) for w in ws]
    n1 = sum(c)
    n11 = sum(1 for t in range(1, rounds) if c[t] and c[t - 1])
    n111 = sum(1 for t in range(2, rounds) if c[t] and c[t - 1] and c[t - 2])
    e11, _ = carry(n1 * n1, rounds, 0)
    e111, _ = carry(n11 * n1, rounds, 0)
    lives, last = [], None
    for t in range(rounds):
        if c[t]:
            if last is not None:
                lives.append(t - last)
            last = t
    k, s1, s2 = len(lives), sum(lives), sum(d * d for d in lives)
    vm, _ = carry(1000 * (k * s2 - s1 * s1), s1 * s1, 0)
    geo = 1000 - carry(1000 * n1, rounds, 0)[0]
    print(f"the circulation's quanta, {rounds} rounds, y = {fl[ga] + fl[ab] - fl[gb]} at the dial {st.D3}: {n1} landings"
          f" (net {sum(ws)}); after one the next {n11} against {e11} independent; after two in a row a third {n111}"
          f" against {e111}; lives' variance over mean squared {vm} per mille, the geometric law's {geo}")
