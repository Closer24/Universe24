"""Sofer's word (b) (#2187 6540070751 item 3): the law of the three clicks where an edge lies on two triangles. The
proof L0 to L9 never uses C^T C = 3 I, so it should hold on any structure with B C = 0, with the triangles' teeth
turned by the whole matrix K = C^T C (eta += K tau, then tau += K eta, between the carries; the same in reverse after).
This toy reads it on two structures at one Node-clock, in whole numbers and Rule3's carry alone:
  - two triangles sharing an edge: clocks 0 to 3, edges 01, 02, 12, 13, 23, triangles 012 and 123;
  - four clocks pairwise joined (every edge on two triangles, and C with a kernel: the four faces' boundary).
The dial is the click world's key times 3, then 3 again (3D), as mode 11's. The passings are stand-ins, steady, edge e
passing (9 + 3 e) m with m = D div 50, the Boss's toy's m; each is named a stand-in, not a world's.

Read, for K = C^T C and for K = 3 I (the turn without the triangles' coupling):
  L0 B C = 0; L1 each edge's two ends; L2 one hidden unit in triangle 0's twin moves no clock's line;
  L3 per clock, exactly: 3 (D (its line's sum) - (its swept passing)) = (B (g at the start - g at the end)) at that clock;
  L7 and L9 the end alone runs back to the start: flip the twins, carry the negated passings in reverse order, flip;
  and, measured not proved, the circulation's landings on each triangle: after one the next, against independent.

Usage: python3 -I shared.py <src> [rounds, 200000 unless given]
"""
import sys

sys.path.insert(0, sys.argv[1])
from tensor24.algebra.carry import carry  # noqa: E402

ROUNDS = int(sys.argv[2]) if len(sys.argv) > 2 else 200000
KEY = 50811429  # the click world's key, odd, as its universe file holds it
D = 3 * KEY
D3 = 3 * D
B3, _ = carry(D3 - 1, 2, 0)
M, _ = carry(D, 50, 0)


def structure(edges):
    nv = 1 + max(max(e) for e in edges)
    tris = [(i, j, k) for i in range(nv) for j in range(i + 1, nv) for k in range(j + 1, nv)
            if (i, j) in edges and (i, k) in edges and (j, k) in edges]
    B = [[(1 if a == v else -1 if b == v else 0) for (a, b) in edges] for v in range(nv)]
    C = [[0] * len(tris) for _ in edges]
    for f, (i, j, k) in enumerate(tris):
        C[edges.index((j, k))][f] += 1
        C[edges.index((i, k))][f] -= 1
        C[edges.index((i, j))][f] += 1
    return nv, tris, B, C


def cen(v):
    _, r = carry(v + B3, D3, 0)
    return r - B3


def step(K, C, fl, gs, ts, es, hidden_w=None):
    nf, ne = len(ts), len(gs)
    ys = [sum(C[e][f] * fl[e] for e in range(ne)) for f in range(nf)]
    p = [3 * fl[e] - sum(C[e][f] * ys[f] for f in range(nf)) for e in range(ne)]
    es = [B3 + cen(es[f] - B3 + sum(K[f][u] * (ts[u] - B3) for u in range(nf))) for f in range(nf)]
    ts = [B3 + cen(ts[f] - B3 + sum(K[f][u] * (es[u] - B3) for u in range(nf))) for f in range(nf)]
    Q = [0] * ne
    for e in range(ne):
        Q[e], gs[e] = carry(p[e], D3, gs[e])
    W = [0] * nf
    for f in range(nf):
        W[f], ts[f] = carry(ys[f], D3, ts[f])
    ts = [B3 + cen(ts[f] - B3 + sum(K[f][u] * (es[u] - B3) for u in range(nf))) for f in range(nf)]
    es = [B3 + cen(es[f] - B3 + sum(K[f][u] * (ts[u] - B3) for u in range(nf))) for f in range(nf)]
    q = [Q[e] + sum(C[e][f] * W[f] for f in range(nf)) for e in range(ne)]
    return q, W, gs, ts, es


def flip(es):
    return [B3 + cen(-(v - B3)) for v in es]


def run(K, C, B, flows, rounds, hidden):
    ne, nf, nv = len(flows), len(K), len(B)
    gs, ts, es = [B3] * ne, [B3] * nf, [B3] * nf
    if hidden:
        es[0] = B3 + cen(es[0] - B3 + 1)
    start = (list(gs), list(ts), list(es))
    lines, sides, lands = [], [], [[] for _ in range(nf)]
    for _ in range(rounds):
        q, W, gs, ts, es = step(K, C, flows, gs, ts, es)
        sides.append(q)
        lines.append([sum(B[v][e] * q[e] for e in range(ne)) for v in range(nv)])
        for f in range(nf):
            lands[f].append(W[f])
    end = (list(gs), list(ts), list(es))
    g2, t2, e2 = list(gs), list(ts), flip(es)
    neg = [-x for x in flows]
    for _ in range(rounds):
        _, _, g2, t2, e2 = step(K, C, neg, g2, t2, e2)
    back = (g2, t2, flip(e2)) == start
    return start, end, lines, sides, lands, back


def memory(ws):
    on = [1 if w else 0 for w in ws]
    n1, pairs = sum(on), sum(on[i] * on[i + 1] for i in range(len(on) - 1))
    ind, _ = carry(n1 * n1, len(on), 0)
    return n1, pairs, ind


for name, edges in (("two triangles sharing edge 12", [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)]),
                    ("four clocks pairwise joined", [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)])):
    nv, tris, B, C = structure(edges)
    BC = [[sum(B[v][e] * C[e][f] for e in range(len(edges))) for f in range(len(tris))] for v in range(nv)]
    CtC = [[sum(C[e][f] * C[e][u] for e in range(len(edges))) for u in range(len(tris))] for f in range(len(tris))]
    flows = [(9 + 3 * e) * M for e in range(len(edges))]
    print(f"{name}: edges {edges}, triangles {tris}; B C = 0: {all(v == 0 for r in BC for v in r)}; C^T C = {CtC}")
    eye3 = [[3 if f == u else 0 for u in range(len(tris))] for f in range(len(tris))]
    for kname, K in (("K = C^T C", CtC), ("K = 3 I", eye3)):
        s0, e0, L, Sd, W, back = run(K, C, B, flows, ROUNDS, False)
        s1, e1, LH, SH, WH, backh = run(K, C, B, flows, ROUNDS, True)
        moved_lines = sum(1 for t in range(ROUNDS) for v in range(nv) if L[t][v] != LH[t][v])
        moved_sides = sum(1 for t in range(ROUNDS) for e in range(len(edges)) if Sd[t][e] != SH[t][e])
        l3 = []
        for v in range(nv):
            line = sum(L[t][v] for t in range(ROUNDS))
            swept = ROUNDS * sum(B[v][e] * flows[e] for e in range(len(edges)))
            teeth = sum(B[v][e] * (s0[0][e] - e0[0][e]) for e in range(len(edges)))
            l3.append(3 * (D * line - swept) == teeth)
        print(f"  {kname}, {ROUNDS} rounds: L3 exact at every clock {all(l3)}; the end alone runs back to the start"
              f" {back} (with the hidden unit {backh}); one hidden unit in triangle 0's twin: {moved_lines} clock lines"
              f" move, {moved_sides} sides move")
        for f in range(len(tris)):
            n1, pairs, ind = memory(W[f])
            print(f"    triangle {tris[f]}: {n1} rounds with a landing; after one the next {pairs} against {ind}"
                  f" independent")
