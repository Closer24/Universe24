"""bb2: the reader of a course file (bb2_course.py or sub_drift.py): the runs of the mean, the exact returns, the e course, the Links' sum against the second-order prediction SUM_Links E^2 isqrt(Gamma X mean) div (6 x 10^6), the count of intervals with a negative Links' sum. Integers only.
Usage: read_course.py <course.json> [gamma] [nodes, for the list form of bb2_course.py]
"""
import json
import math
import sys


def main(argv):
    sys.set_int_max_str_digits(0)
    r = json.load(open(argv[1]))
    gamma = int(argv[2]) if len(argv) > 2 else 1000
    rows = r["rows"] if isinstance(r, dict) else r
    n = r["nodes"] if isinstance(r, dict) else (int(argv[3]) if len(argv) > 3 else None)
    if not isinstance(r, dict):
        r = {}
    means = [(x["i"], x.get("X next mean", x.get("X mean")), x["X min"], x["X max"]) for x in rows]
    runs, direction, start = [], 0, means[0]
    for k in range(1, len(means)):
        d = (means[k][1] > means[k - 1][1]) - (means[k][1] < means[k - 1][1])
        if d != 0 and d != direction:
            if direction != 0:
                runs.append((("rise" if direction > 0 else "fall"), start[0], start[1], means[k - 1][0], means[k - 1][1]))
            direction, start = d, means[k - 1]
    runs.append((("rise" if direction > 0 else "fall"), start[0], start[1], means[-1][0], means[-1][1]))
    long_runs = [x for x in runs if x[3] - x[1] >= 5]
    marks = (1, 2, 3, 5, 10, 20, 40, 58, 80, 100, 115, 130, 150, 173, 200, 230, 260, 288, 300, 345, 400)
    e_course = [(x["i"], x["e max"], x["links above"]) for x in rows if x["i"] in marks]
    lift = []
    negatives = 0
    for x in rows:
        if x["links sum"] < 0:
            negatives += 1
        if x["i"] in marks:
            xm = x.get("X mean", x.get("X next mean"))
            pred = x["e sq sum"] * math.isqrt(gamma * xm) // (6 * 10 ** 6)
            lift.append((x["i"], x["links sum"], pred, x["mass pull sum"], x["write sum"], x["e max"]))
    at_seed = [x["i"] for x in rows if x.get("at seed", 0) == (n or 0) and n]
    all_turn = [x["i"] for x in rows if n and x["turns at i"] == n]
    print(json.dumps({
        "L": r.get("L"), "long runs (kind, from i, X, to i, X)": long_runs[:14],
        "exact returns": at_seed[:12], "all Nodes turned at": all_turn[:12],
        "e max / Links above 63 at marks": e_course, "e max over the run": max(x["e max"] for x in rows),
        "first i with e >= 63": next((x["i"] for x in rows if x["e max"] >= 63), None),
        "Links' sum: (i, measured, predicted second order, mass, write, e max)": lift,
        "intervals with the Links' sum below 0": negatives, "intervals": len(rows),
        "mean at 115 / 230 / 345 (min, max)": [(m[0], m[1], m[2], m[3]) for m in means if m[0] in (115, 230, 345)],
        "births": rows[-1]["births"], "refused_lay": rows[-1]["refused_lay"], "body_clicks": rows[-1]["body_clicks"],
        "run back": r.get("run back"), "census": r.get("census"), "max transient bits": r.get("max transient bits"),
        "max bits over the run": max(x.get("max bits", 0) for x in rows),
    }))


if __name__ == "__main__":
    main(sys.argv)
