"""The drift (THIRD6's OPEN 3, #2187 6539589459 item 3): each train's booked quanta against its swept passing, and each
edge's, over the run: the most the running difference reaches, in whole dials, and where it ends. The first click holds
every edge within one dial (dial q = k_before + x - k_after, the teeth between); a turn that moves the edge teeth only
along each triangle's circulation holds every train within its teeth too, since a circulation's boundary is 0, while
the edges drift along the circulation alone.

Usage: python3 -I drift.py <src> <world> <rounds> [modes, 047 unless given] [laid]
"""
import sys

src, world, rounds = sys.argv[1], sys.argv[2], int(sys.argv[3])
modes = [int(m) for m in ((sys.argv[4] if len(sys.argv) > 4 else "047").split(",") if "," in (sys.argv[4] if len(sys.argv) > 4 else "") else (sys.argv[4] if len(sys.argv) > 4 else "047"))]
laid = len(sys.argv) > 5 and "laid" in sys.argv[5]
sys.path.insert(0, src)
sys.path.insert(0, ".")
import edgeclick as E  # noqa: E402
from tensor24.algebra.carry import carry  # noqa: E402

for mode in modes:
    a = E.run(src, world, rounds, mode, laid=laid)
    dial, pairs, sites = a["dial"], a["pairs"], a["sites"]
    q = {(t, x, e): c for (t, x, e, c) in a["sides"]}
    trains = sorted({tr for p in pairs for tr in p})
    edge_max, edge_end = [0] * len(pairs), [0] * len(pairs)
    train_max, train_end = {tr: 0 for tr in trains}, {tr: 0 for tr in trains}
    for x in range(sites):
        run_e = [0] * len(pairs)
        run_t = {tr: 0 for tr in trains}
        for t in range(rounds):
            for e, (u, v) in enumerate(pairs):
                gap = dial * q.get((t, x, e), 0) - a["flows"][t][x][e]
                run_e[e] += gap
                run_t[u] += gap
                run_t[v] -= gap
                edge_max[e] = max(edge_max[e], abs(run_e[e]))
            for tr in trains:
                train_max[tr] = max(train_max[tr], abs(run_t[tr]))
        for e in range(len(pairs)):
            edge_end[e] = max(edge_end[e], abs(run_e[e]))
        for tr in trains:
            train_end[tr] = max(train_end[tr], abs(run_t[tr]))

    def dials(v):
        return carry(1000 * v, dial, 0)[0]

    print(f"{world}{', laid' if laid else ''}, {E.NAMES[mode]}, {rounds} rounds: books open {a['books_open']} of {a['places']}; run back {a['runback']}")
    print("   per edge, booked less swept at most (at the end), per mille of a dial: "
          + ", ".join(f"{pairs[e]} {dials(edge_max[e])} ({dials(edge_end[e])})" for e in range(len(pairs))))
    print("   per train, booked less swept at most (at the end), per mille of a dial: "
          + ", ".join(f"{tr} {dials(train_max[tr])} ({dials(train_end[tr])})" for tr in trains))
