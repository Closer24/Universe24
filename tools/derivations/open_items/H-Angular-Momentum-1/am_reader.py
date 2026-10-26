"""H-Angular-Momentum-1: a reader of the orbital angular momentum L_c and the spin density over a world's run (no act).
The row's momentum density on the Link i -> i+a (MV-S1's integers): p_a(i) = 2 num (now_(i+a) before_i - now_i before_(i+a)) = -2 num F_(i,i+a), summed over the row's lines.
The Link sits at the doubled position 2 r_i + e_a; about a centre z (Node coordinates) by the minimum image on the torus, d in [-N, N) per axis (doubled units).
2 L_c = SUM over Links d x p (an integer; L in half-Link units). P_a = SUM over Links p_a(i).
Usage: python am_reader.py <world.json> <out.json> [intervals N] [centre x y z]."""
from __future__ import annotations

import json
import sys

from event_universe import gram
from event_universe.core.ports import AXES, across
from event_universe.links import link_current
from event_universe.loader.world import load_world
from event_universe.node import Node


def ints(a):
    return [int(x) for x in a.reshape(-1)]


def positions(shape, centre):
    """Doubled minimum-image offsets of every Node from the centre, per axis, flattened in the board's order."""
    import numpy as np

    idx = np.indices(shape)
    out = []
    for a in range(len(shape)):
        n = shape[a]
        d = [((2 * x - 2 * centre[a] + n) % (2 * n)) - n for x in ints(idx[a])]
        out.append(d)
    return out


def row_p(row, num):
    """p_a(i) on the Link i -> i+a per axis, summed over the row's lines (plain sum: the Gram of a plane is I)."""
    found = []
    for a in range(AXES):
        f = sum((link_current(line, 2 * a) for line in row.lines), start=0)
        found.append([-2 * num * x for x in ints(f)])
    return found


def seam(shape, centre, axis):
    """The Nodes whose +axis Link crosses the minimum-image seam about the centre (the arm jumps by N)."""
    import numpy as np

    idx = ints(np.indices(shape)[axis])
    n = shape[axis]
    far = (centre[axis] + n // 2) % n  # the antipode's coordinate along the axis... the Link from far-1... to far
    return [k for k, x in enumerate(idx) if (x + 1) % n == far or (n % 2 == 0 and x == far)]


def moment(p, d, shape):
    """2 L = SUM over Links (d_link x p); d_link doubled = d_node + e_a (the Link's midpoint), minimum image kept per Node."""
    L = [0, 0, 0]
    P = [0, 0, 0]
    bound = [0, 0, 0]
    for a in range(AXES):
        pa = p[a]
        for k, v in enumerate(pa):
            if v == 0:
                continue
            arm = [d[0][k], d[1][k], d[2][k]]
            arm[a] += 1
            # cross arm x (v e_a)
            b, c = (a + 1) % 3, (a + 2) % 3
            L[c] += arm[a] * 0 + arm[b] * v if False else 0
            # components: (arm x e_a)_b = arm_c * e_a_a ... use the explicit cross
            e = [0, 0, 0]
            e[a] = v
            L[0] += arm[1] * e[2] - arm[2] * e[1]
            L[1] += arm[2] * e[0] - arm[0] * e[2]
            L[2] += arm[0] * e[1] - arm[1] * e[0]
            P[a] += v
            bound[0] += abs(arm[1] * e[2] - arm[2] * e[1])
            bound[1] += abs(arm[2] * e[0] - arm[0] * e[2])
            bound[2] += abs(arm[0] * e[1] - arm[1] * e[0])
    return L, P, bound


def main(argv):
    sys.set_int_max_str_digits(0)
    universe, world = load_world(argv[1])
    intervals = int(argv[argv.index("intervals") + 1]) if "intervals" in argv else int(world["intervals"])
    shape = tuple(int(x) for x in world["shape"])
    centre = (
        [int(argv[argv.index("centre") + 1 + k]) for k in range(3)]
        if "centre" in argv
        else [n // 2 for n in shape]
    )
    node = Node(universe, world)
    d = positions(shape, centre)
    rows_out = []
    prev = None

    def read():
        recs = node.records()
        per_row = []
        total_L = [0, 0, 0]
        total_P = [0, 0, 0]
        total_W = 0
        total_S = [0, 0, 0]
        for rec, row in enumerate(recs):
            num = int(row.pair[0])
            p = row_p(row, num)
            L, P, bound = moment(p, d, shape)
            W = sum(ints(gram.charge(row.shape, row.lines)))
            nows = [line.now for line in row.lines]
            S = [sum(ints(s)) for s in gram.density(row.shape, nows)] if row.shape == 8 else None
            per_row.append({"row": rec, "shape": row.shape, "2L": L, "P": P, "bound_2L": bound, "W": W, "spin": S})
            for k in range(3):
                total_L[k] += L[k]
                total_P[k] += P[k]
                if S:
                    total_S[k] += S[k]
            total_W += W
        return per_row, total_L, total_P, total_W, total_S

    def snapshot(label):
        nonlocal prev
        per_row, L, P, W, S = read()
        births = int(node.counts["births"])
        clicks = int(node.counts["body_clicks"])
        turns = int(node.counts["turns"])
        row = {
            "i": node.interval,
            "births": births,
            "body_clicks": clicks,
            "turns": turns,
            "2L": L,
            "P": P,
            "W": W,
            "spin": S,
            "rows": per_row,
        }
        if prev is not None:
            row["d2L"] = [L[k] - prev["2L"][k] for k in range(3)]
            row["dP"] = [P[k] - prev["P"][k] for k in range(3)]
            row["dW"] = W - prev["W"]
            row["new_births"] = births - prev["births"]
            row["new_clicks"] = clicks - prev["body_clicks"]
            row["new_turns"] = turns - prev["turns"]
            row["bound_2L"] = [sum(r["bound_2L"][k] for r in per_row) for k in range(3)]
        prev = row
        rows_out.append(row)

    snapshot("start")
    for _t in range(intervals):
        node.step()
        snapshot("step")
    out = {"world": argv[1], "centre": centre, "shape": list(shape), "intervals": intervals, "rows": rows_out}
    with open(argv[2], "w", encoding="utf-8") as f:
        json.dump(out, f)
    # the summary
    quiet = [r for r in rows_out[1:] if r["new_births"] == 0 and r["new_clicks"] == 0 and r["new_turns"] == 0]
    loud = [r for r in rows_out[1:] if r not in quiet]
    def maxabs(rs, key):
        return max((max(abs(x) for x in r[key]) for r in rs), default=0)
    print(json.dumps({
        "world": argv[1], "intervals": intervals, "centre": centre,
        "2L start": rows_out[0]["2L"], "2L end": rows_out[-1]["2L"], "P start": rows_out[0]["P"], "P end": rows_out[-1]["P"],
        "W start": rows_out[0]["W"], "W end": rows_out[-1]["W"],
        "quiet intervals": len(quiet), "max |d2L| quiet": maxabs(quiet, "d2L"), "max |dP| quiet": maxabs(quiet, "dP"),
        "max bound_2L": maxabs(rows_out[1:], "bound_2L"),
        "loud intervals": len(loud), "max |d2L| loud": maxabs(loud, "d2L"), "max |dP| loud": maxabs(loud, "dP"),
        "births": rows_out[-1]["births"], "clicks": rows_out[-1]["body_clicks"], "turns": rows_out[-1]["turns"],
        "spin end": rows_out[-1]["spin"],
    }))


if __name__ == "__main__":
    main(sys.argv)
