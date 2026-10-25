"""pl1's reader of a driver record (pl1_run.py): the whole-board tops, the bottoms (the local minima of the mean X with the value against Gamma and whether every Node is at Gamma), the retrace of the carrier X(top + k) = X(top - 2 - k) with the first k that parts and the integer, and the retrace of EVERY LINE of the Node (0, 0, 0): the state after top + k steps against the exchange's image of the state after top - 1 - k steps (now' = K before, before' = K now, rem' mirrored once per reversal by the one rule, wr' mirrored once; K the row's conjugation, -I on the shape-4 row under --odd), the first k and the first field at which each line parts, with the values. Also W per record and the Node's total per interval, and the sign row's time line (level, write remainder) interval by interval around the first top. Usage: read_retrace.py <record.json> [--odd] [--kmax N]"""
import json
import sys

sys.set_int_max_str_digits(0)


def mirrored(r, wall, reversals):
    return r if reversals % 2 == 0 else wall - 1 - r


def read(path, odd, kmax):
    run = json.load(open(path, encoding="utf-8"))
    gamma, cube = int(run["gamma"]), int(run["cube"])
    nodes = cube ** 3
    diags = run["diag"]
    states = run["states"]
    means = [d["X mean/min/max"][0] for d in diags]
    spread = [d["X mean/min/max"][2] - d["X mean/min/max"][1] for d in diags]
    tops = [d["i"] for d in diags if d["turned"] == nodes]
    partial = [(d["i"], d["turned"]) for d in diags if 0 < d["turned"] < nodes]
    bottoms = [(k, means[k], means[k] - gamma, spread[k] == 0) for k in range(1, len(means) - 1) if means[k] <= means[k - 1] and means[k] < means[k + 1]]
    exact = [k for k in range(len(means)) if means[k] == gamma and spread[k] == 0 and k > 0]
    out = {
        "record": path, "cube": cube, "intervals": run["intervals"], "laid": [{k: v for k, v in l.items() if k != "event"} for l in run["laid"]],
        "summary": run["summary"], "alike (spread 0) of intervals": [sum(1 for s in spread if s == 0), len(spread)],
        "tops (every Node turning)": tops, "partial turns": partial[:8],
        "bottoms (i, mean X, X - Gamma, alike)": bottoms, "intervals at Gamma exactly at every Node": exact,
        "W total (Node 0) at 0, 1, 2, 10, 50, top, 2top-2, 400": None,
    }
    wt = [d["W total (Node 0)"] for d in diags]
    wr_rows = [d["W per record (Node 0)"] for d in diags]
    marks = [0, 1, 2, 10, 50] + ([tops[0], 2 * tops[0] - 2] if tops else []) + [len(wt) - 1]
    out["W total (Node 0) at 0, 1, 2, 10, 50, top, 2top-2, 400"] = [(m, wt[m], wr_rows[m]) for m in marks if m < len(wt)]
    out["W total: intervals where W(t) != W(t+1) in the first cycle"] = sum(1 for t in range(0, (tops[0] if tops else len(wt) - 1)) if wt[t] != wt[t + 1])
    out["W total: least / largest over the run"] = [min(wt), max(wt)]
    rows = run["rows"]
    # the line index -> (row, line in row)
    lines = []
    for r_i, r in enumerate(rows):
        for l in range(int(r["shape"])):
            lines.append((r_i, l))
    sign_row = next(i for i, r in enumerate(rows) if r["is_potential"])
    sign_line = lines.index((sign_row, 0))
    if tops:
        top = tops[0]
        out["X retrace about the first top: X(top + k) against X(top - 2 - k)"] = None
        first_x = None
        equal_x = 0
        table = []
        for k in range(1, min(top - 2, len(means) - 1 - top) + 1):
            a, b = means[top + k], means[top - 2 - k]
            if a == b:
                equal_x += 1
            elif first_x is None:
                first_x = (k, top + k, a, top - 2 - k, b, a - b)
            if k <= 14 or (first_x and k <= first_x[0] + 4):
                table.append((k, a, b, a - b))
        out["X retrace about the first top: X(top + k) against X(top - 2 - k)"] = {"top": top, "equal k": equal_x, "first parting (k, i_fall, X_fall, i_rise, X_rise, fall - rise)": first_x, "table (k, X_fall, X_rise, diff)": table}
        # every line of the Node: S(top + k) against M(S(top - 1 - k))
        per_line = []
        for li, (r_i, l) in enumerate(lines):
            r = rows[r_i]
            k_diag = r["K"][l][l]
            if odd and r["is_potential"]:
                k_diag = -k_diag
            first = None
            held = 0
            for k in range(0, min(top - 1, len(states) - 1 - top) + 1):
                s = states[top + k][li]
                h = states[top - 1 - k][li]
                now_m, before_m = k_diag * h[1], k_diag * h[0]
                rem_m = mirrored(h[2], h[3], 1 + (k_diag < 0))
                wr_m = None if h[4] is None else mirrored(h[4], h[5], 1)
                fields = [("now", s[0], now_m), ("before", s[1], before_m), ("rem", s[2], rem_m), ("wall", s[3], h[3])]
                if h[4] is not None:
                    fields.append(("wr", s[4], wr_m))
                bad = [(f, a, b, a - b) for f, a, b in fields if a != b]
                if not bad:
                    held += 1
                elif first is None:
                    first = {"k": k, "i_fall": top + k, "i_rise_mirror": top - 1 - k, "fields parting": bad}
                    if k > kmax:
                        break
            per_line.append({"row": r_i, "shape": r["shape"], "line": l, "K": k_diag, "is_potential": r["is_potential"], "is_carrier": r["is_carrier"], "is_gap0": r["is_gap0"], "is_walled": r["is_walled"], "is_record": r["is_record"], "k held": held, "first parting": first})
        out["lines' retrace about the first top (each line of the Node 0: S(top + k) against the exchange's image of S(top - 1 - k))"] = per_line
        earliest = sorted([p for p in per_line if p["first parting"]], key=lambda p: p["first parting"]["k"])
        out["the first lines to part (k ascending)"] = [(p["row"], p["shape"], p["line"], p["first parting"]["k"], p["first parting"]["fields parting"]) for p in earliest[:6]]
        # the sign row's time line around the top: level, before, wr, and W total
        out["sign row time line (i, now, before, wr, W total) from top - 12 to top + 12"] = [(i, states[i][sign_line][0], states[i][sign_line][1], states[i][sign_line][4], wt[i]) for i in range(max(0, top - 12), min(len(states), top + 13))]
        out["sign row time line at 0..6"] = [(i, states[i][sign_line][0], states[i][sign_line][1], states[i][sign_line][4], wt[i]) for i in range(0, min(7, len(states)))]
    credits = [e for e in run["log"] if e.get("event") == "credit"]
    out["credits"] = len(credits)
    out["credits laid back"] = sum(1 for c in credits if "laid_back" in c)
    from collections import Counter
    out["credit intervals (i: count)"] = sorted(Counter(int(c["i"]) for c in credits).items())[:14]
    out["refusals by cause"] = dict(Counter(e.get("cause") for e in run["log"] if e.get("event") == "refused"))
    return out


if __name__ == "__main__":
    odd = "--odd" in sys.argv
    kmax = int(sys.argv[sys.argv.index("--kmax") + 1]) if "--kmax" in sys.argv else 400
    print(json.dumps(read(sys.argv[1], odd, kmax), indent=1, default=str))
