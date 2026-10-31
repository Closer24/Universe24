"""The three clicks read on the real act's records, per edge at every Node-clock: the booked quanta against the swept
flow, e_t = dial q_t - x_t (the tooth's change, r_before - r_after, for the first click; the turn's share for the
third), its running sum (bounded within one dial for the first click, wandering for the third), its lag-1
correlation, and the record run twice."""
import sys, json, hashlib
src, world, rounds = sys.argv[1], sys.argv[2], int(sys.argv[3])
sys.path.insert(0, src); sys.path.insert(0, ".")
import edgeclick as E
from tensor24.algebra.carry import carry

def permille(n, d):
    return carry(1000 * n, d, 0)[0] if d else 0
for mode in (0, 1):
    a = E.run(src, world, rounds, mode); b = E.run(src, world, rounds, mode)
    dial = a["dial"]; ne = len(a["pairs"]); sites = a["sites"]
    q = {}
    for (t, x, e, c) in a["sides"]:
        q[(t, x, e)] = c
    out = []
    for e in range(ne):
        maxrun = 0; lag_num = lag_den = 0; spread_end = []
        for x in range(sites):
            run_ = 0; prev = None
            for t in range(rounds):
                ee = dial * q.get((t, x, e), 0) - a["flows"][t][x][e]
                run_ += ee; maxrun = max(maxrun, abs(run_))
                if prev is not None: lag_num += prev * ee; lag_den += ee * ee
                prev = ee
            spread_end.append(abs(run_))
        out.append((a["pairs"][e], permille(maxrun, dial), permille(lag_num, lag_den), permille(max(spread_end), dial)))
    print(f"{world} {'third click (turned)' if mode else 'first click (carried)'}, {rounds} rounds: run twice byte for byte {a['digest'] == b['digest']};"
          f" books open {a['books_open']} of {a['places']}; run back {a['runback']}")
    for pr, mx, lag, end in out:
        print(f"   edge {pr}: booked less swept, its running sum at most {mx} per mille of a dial (at the end at most {end}); lag-1 correlation of the per-round gap {lag} per mille")
