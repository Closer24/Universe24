"""L8, the label rule, read where an edge lies on two triangles (with shared.py; #2187 6540070751 item 3 and David's
6540137404 item 2). A relabelling of the clocks maps each edge to an edge, its sign s_e = -1 where the order of its
ends turns over, and each triangle to a triangle with its sign. The relabelled run starts from the relabelled teeth
(each tooth read from its other end, where its sign is -1, is its centred negation; the birth is its own) and carries
the relabelled passings s_e x_e. The rule holds when every side of every round is the relabelled side, s_e q_e.

Usage: python3 -I sharedlabel.py <src> [rounds, 20000 unless given]
"""
import sys

sys.path.insert(0, sys.argv[1])
from tensor24.algebra.carry import carry  # noqa: E402

ROUNDS = int(sys.argv[2]) if len(sys.argv) > 2 else 20000
KEY = 50811429
D = 3 * KEY
D3 = 3 * D
B3, _ = carry(D3 - 1, 2, 0)
M, _ = carry(D, 50, 0)


def structure(edges):
    nv = 1 + max(max(e) for e in edges)
    tris = [(i, j, k) for i in range(nv) for j in range(i + 1, nv) for k in range(j + 1, nv)
            if (i, j) in edges and (i, k) in edges and (j, k) in edges]
    C = [[0] * len(tris) for _ in edges]
    for f, (i, j, k) in enumerate(tris):
        C[edges.index((j, k))][f] += 1
        C[edges.index((i, k))][f] -= 1
        C[edges.index((i, j))][f] += 1
    K = [[sum(C[e][f] * C[e][u] for e in range(len(edges))) for u in range(len(tris))] for f in range(len(tris))]
    return tris, C, K


def cen(v):
    _, r = carry(v + B3, D3, 0)
    return r - B3


def sides(K, C, fl, gs, ts, es, rounds):
    nf, ne = len(ts), len(gs)
    out = []
    for _ in range(rounds):
        ys = [sum(C[e][f] * fl[e] for e in range(ne)) for f in range(nf)]
        p = [3 * fl[e] - sum(C[e][f] * ys[f] for f in range(nf)) for e in range(ne)]
        es = [B3 + cen(es[f] - B3 + sum(K[f][u] * (ts[u] - B3) for u in range(nf))) for f in range(nf)]
        ts = [B3 + cen(ts[f] - B3 + sum(K[f][u] * (es[u] - B3) for u in range(nf))) for f in range(nf)]
        Q, W = [0] * ne, [0] * nf
        for e in range(ne):
            Q[e], gs[e] = carry(p[e], D3, gs[e])
        for f in range(nf):
            W[f], ts[f] = carry(ys[f], D3, ts[f])
        ts = [B3 + cen(ts[f] - B3 + sum(K[f][u] * (es[u] - B3) for u in range(nf))) for f in range(nf)]
        es = [B3 + cen(es[f] - B3 + sum(K[f][u] * (ts[u] - B3) for u in range(nf))) for f in range(nf)]
        out.append([Q[e] + sum(C[e][f] * W[f] for f in range(nf)) for e in range(ne)])
    return out


for name, edges in (("two triangles sharing edge 12", [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)]),
                    ("four clocks pairwise joined", [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)])):
    tris, C, K = structure(edges)
    flows = [(9 + 3 * e) * M for e in range(len(edges))]
    for pname, pi in (("clocks 0 and 1 swapped", [1, 0, 2, 3]), ("the four clocks turned round", [1, 2, 3, 0])):
        img = [(pi[a], pi[b]) for (a, b) in edges]
        edges2 = sorted(tuple(sorted(e)) for e in img)
        emap = [edges2.index(tuple(sorted(e))) for e in img]
        sgn = [1 if a < b else -1 for (a, b) in img]
        tris2, C2, K2 = structure(edges2)
        fmap, fsg = [], []
        for f, (i, j, k) in enumerate(tris):
            f2 = tris2.index(tuple(sorted((pi[i], pi[j], pi[k]))))
            e = edges.index((i, j))
            fmap.append(f2)
            fsg.append(C2[emap[e]][f2] * sgn[e] * C[e][f])
        flows2 = [0] * len(edges)
        for e in range(len(edges)):
            flows2[emap[e]] = sgn[e] * flows[e]
        for hidden in (False, True):
            es = [B3] * len(tris)
            es2 = [B3] * len(tris)
            if hidden:
                es[0] = B3 + cen(1)
                es2[fmap[0]] = B3 + cen(fsg[0])
            a = sides(K, C, flows, [B3] * len(edges), [B3] * len(tris), es, ROUNDS)
            b = sides(K2, C2, flows2, [B3] * len(edges), [B3] * len(tris), es2, ROUNDS)
            bad = sum(1 for t in range(ROUNDS) for e in range(len(edges)) if b[t][emap[e]] != sgn[e] * a[t][e])
            print(f"{name}, {pname}{', a hidden unit in triangle 0' if hidden else ''}: {ROUNDS} rounds,"
                  f" {sum(1 for t in range(ROUNDS) for e in range(len(edges)) if a[t][e])} sides with a click;"
                  f" sides not the relabelled side: {bad}")
