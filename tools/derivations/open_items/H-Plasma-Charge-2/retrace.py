"""pl2's retrace instrument: a world run `intervals` forward on the engine PYTHONPATH names (src or src_pl2 under its flags), the whole
state of the Node (0, 0, 0) kept at every interval (every line's now, before, rotation remainder, write remainder and wall, in the
acts' order), the board's X spread, each gapped record's Wronskian at the Node; then, for every top where the whole board turned, the
fall compared with the mirror of the rise line by line: S(top + k) against E(S(top - 1 - k)), E the exchange and the conjugation with
the remainders mirrored by the one rule (node.exchange), the first k that parts and the lines that part at it with their integers;
the bottoms, the exact returns to Gamma at every Node, the credits and the laid-back count, the run back of `back` intervals by the
state hash (through the top where the run ends after one), the census (integers, bits). Integers only; the record written as JSON.
Usage: retrace.py <world.json> <intervals> <back> <out.json>"""
import json
import os
import sys
import time

sys.set_int_max_str_digits(0)
import numpy as np

from event_universe import gram
from event_universe.core.rule3 import mirrored
from event_universe.loader.world import load_world
from event_universe.node import Node
from event_universe.rows import CARRIER, PLANE

ORIGIN = (0, 0, 0)


def names_of(node):
    found = []
    for r in node.rows_:
        tag = f"shape {r.shape}" + ("" if r.pair is None else f" gap {min(int(r.gap), 10**6)}") + (" (walled)" if r.wall is not None else "")
        for j in range(len(r.lines)):
            found.append(f"{tag} line {j}")
    return found


def at0(a):
    return int(np.asarray(a)[ORIGIN]) if np.ndim(a) else int(a)


def state_of(node):
    """Every line at the origin: [now, before, rem, wall, wr, wwall] (wr, wwall None where the line writes not)."""
    found = []
    for r in node.rows_:
        for line in r.lines:
            found.append([at0(line.now), at0(line.before), at0(line.rem), at0(line.wall),
                          None if line.wr is None else at0(line.wr), None if line.wr is None else int(line.wwall)])
    return found


def exchanged(node, state):
    """The exchange and the conjugation of a kept state, by node.exchange's rule (the flag PL2_SIGN_ODD read as the copy reads it)."""
    found = []
    i = 0
    odd = os.environ.get("PL2_SIGN_ODD", "") == "1"
    for r in node.rows_:
        k = gram.conjugation(r.shape)
        if odd and r.shape == 4 and r.wall is None:
            k = [list(x) for x in k]
            k[0][0] = -1
        n = len(r.lines)
        nows = [state[i + j][0] for j in range(n)]
        befores = [state[i + j][1] for j in range(n)]
        for j in range(n):
            now = sum(k[j][c] * befores[c] for c in range(n))
            before = sum(k[j][c] * nows[c] for c in range(n))
            rem = mirrored(state[i + j][2], state[i + j][3], 1 + (k[j][j] < 0))
            wr = None if state[i + j][4] is None else mirrored(state[i + j][4], state[i + j][5], 1 + (k[j][j] < 0) if odd else 1)
            found.append([now, before, rem, state[i + j][3], wr, state[i + j][5]])
        i += n
    return found


def main(argv):
    world_path, intervals, back, out_path = argv[1], int(argv[2]), int(argv[3]), argv[4]
    universe, world = load_world(world_path)
    node = Node(universe, world)
    names = names_of(node)
    gamma = node.gamma
    states, xs, spreads, charges, exact, turns = {0: state_of(node)}, {}, {}, {}, {}, []
    hashes = []
    t0 = time.monotonic_ns()
    for t in range(intervals):
        if back and t >= intervals - back:
            hashes.append(node.state_hash())
        node.step()
        i = node.interval
        states[i] = state_of(node)
        x = [int(v) for v in node.row(CARRIER).lines[0].now.reshape(-1)]
        xs[i] = sum(x) // len(x)
        spreads[i] = max(x) - min(x)
        exact[i] = min(x) == max(x) == gamma
        charges[i] = [at0(gram.charge(r.shape, r.lines)) for r in node.gapped]
        if node.turned.any():
            turns.append((i, int(node.turned.sum())))
    forward_ms = (time.monotonic_ns() - t0) // 1000000
    count = int(node.cube) ** 3
    tops = [i for i, n in turns if n == count]
    ks = sorted(xs)
    bottoms = [(k, xs[k]) for k in ks[1:-1] if xs[k] <= xs[k - 1] and xs[k] < xs[k + 1]]
    exact_at = [k for k in ks if exact[k]]
    retrace = []
    for top in tops:
        first = None
        same = 0
        for k in range(1, top):
            if top + k > intervals:
                break
            mirror = exchanged(node, states[top - 1 - k])
            if states[top + k] == mirror:
                same += 1
                continue
            parted = []
            for name, a, b in zip(names, states[top + k], mirror, strict=True):
                if a != b:
                    parted.append({"line": name, "fall [now, before, rem, wall, wr, wwall]": a, "mirror of the rise": b})
            first = {"k": k, "fall interval": top + k, "mirrored rise interval": top - 1 - k, "X fall": xs[top + k], "X rise mirror": xs[top - 2 - k] if top - 2 - k in xs else None, "lines parted": len(parted), "parted": parted[:8]}
            break
        # the levels alone (every line's now and before): the first k where a level parts, with the lines
        level_first = None
        for k in range(1, top):
            if top + k > intervals:
                break
            mirror = exchanged(node, states[top - 1 - k])
            off = [{"line": nm, "fall [now, before]": a[:2], "mirror": b[:2]} for nm, a, b in zip(names, states[top + k], mirror, strict=True) if a[:2] != b[:2]]
            if off:
                level_first = {"k": k, "fall interval": top + k, "lines": off[:6]}
                break
        # X alone: the first k where X(top + k) differs from X(top - 2 - k)
        x_first = None
        for k in range(0, top - 2):
            if top + k > intervals:
                break
            if xs[top + k] != xs[top - 2 - k]:
                x_first = {"k": k, "X fall": xs[top + k], "X rise": xs[top - 2 - k]}
                break
        window = {str(j): charges[j] for j in range(max(1, (first["mirrored rise interval"] if first else top) - 3), min(intervals, (first["mirrored rise interval"] if first else top) + 3) + 1)}
        retrace.append({"top": top, "equal k before the parting": same, "first parting (state)": first, "first parting (levels)": level_first, "first parting (X)": x_first, "W per gapped record at the origin around the mirrored rise interval": window})
    credits = [e for e in node.log if e["event"] == "credit"]
    back_exact = 0
    for k in range(len(hashes)):
        node.step_back()
        back_exact += node.state_hash() == hashes[len(hashes) - 1 - k]
    n_ints, bits = node.census()
    out = {
        "world": world_path, "engine": os.environ.get("PYTHONPATH", ""), "flags": {k: v for k, v in os.environ.items() if k.startswith(("PL2_", "CS7_"))},
        "intervals": intervals, "forward ms": forward_ms, "cube": node.cube, "gamma": gamma, "T": node.T,
        "uniform (spread 0) of intervals": [sum(1 for k in ks if spreads[k] == 0), len(ks)],
        "turns (interval, count)": turns, "tops": tops, "bottoms (interval, mean X)": bottoms, "exact at Gamma at every Node": exact_at,
        "X at marks": {str(k): xs[k] for k in ks if k % 25 == 0 or k in (1, 2, 3)},
        "credits": len(credits), "laid back": sum(1 for c in credits if "laid_back" in c), "credits in the first rise": sum(1 for c in credits if tops and c["i"] < tops[0]),
        "counts": {k: int(v) for k, v in node.counts.items()},
        "sign level at the origin at marks": {str(k): states[k][[j for j, nm in enumerate(names) if nm.startswith("shape 4") and "walled" not in nm][0]][0] for k in ks if k % 25 == 0},
        "W per gapped record at the origin at marks": {str(k): charges[k] for k in ks if k % 25 == 0 or k == 1},
        "retrace": retrace, "run back": {"intervals": len(hashes), "exact": back_exact}, "integers": n_ints, "bits": bits,
    }
    json.dump(out, open(out_path, "w"), indent=1)
    print(json.dumps({k: out[k] for k in ("world", "flags", "tops", "bottoms (interval, mean X)", "exact at Gamma at every Node", "credits", "laid back", "run back", "integers", "bits", "forward ms")}))
    for r in retrace:
        print(json.dumps({"top": r["top"], "equal k": r["equal k before the parting"], "state parting": None if r["first parting (state)"] is None else {k: v for k, v in r["first parting (state)"].items() if k != "parted"}, "level parting": r["first parting (levels)"], "X parting": r["first parting (X)"]}))


if __name__ == "__main__":
    main(sys.argv)
