"""cl1's reader of a run (the record run_cl1.py wrote): the two bodies' centroid distance over the run on the board (milli Links) and in the
clicks (the credit lines alone: the credits' Nodes per body per window), the velocity and the acceleration as integer pairs [numerator,
denominator] in milli Links per interval and per interval squared (the second difference d(T) - 2 d(T div 2) + d(0), a = 4 D2 / T^2),
the charge at every credit (the senses per body), the births' senses summed, the momentum booked (dP_take summed per body per axis),
the take (taken against levels on every credit), the run back, the census and the bits. Integers only.
Usage: python read_cl1.py <out.json> [<out.json> ...]; with two files named d3 and d6 the ratio a(d3) / a(d6) per 10^9 is printed."""
import json
import sys

WINDOWS = 6
BILLION = 10 ** 9


def distance_of(c, axis):
    a, b = c["bodies"]
    if a["centroid_milli"] is None or b["centroid_milli"] is None:
        return None
    return b["centroid_milli"][axis] - a["centroid_milli"][axis]


def read(path):
    rec = json.load(open(path))
    cs = rec["centroids"]
    axis = cs[0]["axis"]
    T = rec["intervals"]
    d = [distance_of(c, axis) for c in cs]
    marks = [0, T // 4, T // 2, 3 * T // 4, T]
    d2 = d[T] - 2 * d[T // 2] + d[0]
    found = {
        "run": path,
        "cube": rec["cube"], "intervals": T, "axis": axis,
        "d_milli at 0, T/4, T/2, 3T/4, T": [d[m] for m in marks],
        "d_milli min, max": [min(d), max(d)],
        "d(T) - d(0) milli": d[T] - d[0],
        "velocity milli per interval [num, den]": [d[T] - d[0], T],
        "D2 = d(T) - 2 d(T/2) + d(0) milli": d2,
        "acceleration milli per interval^2 [num, den]": [4 * d2, T * T],
        "W per body at 0": [b["W"] for b in cs[0]["bodies"]],
        "W per body at T": [b["W"] for b in cs[T]["bodies"]],
        "weight per body at 0 and T": [[b["weight"] for b in cs[0]["bodies"]], [b["weight"] for b in cs[T]["bodies"]]],
        "sign level min, max at T": cs[T]["sign_level_min_max"],
        "sign level extreme over run": max(max(abs(x) for x in c["sign_level_min_max"]) for c in cs),
        "run back": rec["run_back"], "counts": rec["counts"], "census [integers, bits]": rec["census"],
        "max bits (rows)": max(r["max bits"] for r in rec["rows"]),
        "max transient bits": max(r["max transient bits"] for r in rec["rows"]),
        "seconds": None,
    }
    # the clicks: the credit lines alone
    za, zb = [b["centroid_milli"][axis] // 1000 for b in cs[0]["bodies"]]
    mid2 = za + zb  # twice the midpoint
    credits = [e for e in rec["log"] if e["event"] == "credit"]
    births = [e for e in rec["log"] if e["event"] == "birth"]
    per_body = [[], []]
    for e in credits:
        per_body[0 if 2 * e["node"][axis] < mid2 else 1].append(e)
    found["credits per body"] = [len(p) for p in per_body]
    found["credit senses per body [sum, count, +1, -1, 0]"] = [
        [sum(e["sense"] for e in p), len(p), sum(e["sense"] == 1 for e in p), sum(e["sense"] == -1 for e in p), sum(e["sense"] == 0 for e in p)] for p in per_body]
    found["dP_take summed per body [x, y, z]"] = [[sum(e["dP_take"][a] for e in p) for a in range(3)] for p in per_body]
    found["take: taken >= levels on every credit"] = all(e["taken"] >= 0 and e["levels"] >= 1 for e in credits)
    found["take: sum taken, sum levels"] = [sum(e["taken"] for e in credits), sum(e["levels"] for e in credits)]
    found["births, senses summed over births"] = [len(births), sum(sum(1 if w > 0 else -1 if w < 0 else 0 for w in e["W_children"]) for e in births)]
    found["beats on credits (min, max)"] = [min((e["beat"] for e in credits), default=None), max((e["beat"] for e in credits), default=None)]
    windows = []
    span = T // WINDOWS
    for k in range(WINDOWS):
        lo, hi = k * span + 1, (k + 1) * span
        cz = []
        for p in per_body:
            sel = [e["node"][axis] for e in p if lo <= e["i"] <= hi]
            cz.append(sum(sel) * 1000 // len(sel) if sel else None)
        windows.append({"intervals": [lo, hi], "credit centroid z milli per body": cz,
                        "distance milli": None if None in cz else cz[1] - cz[0], "credits": [len([e for e in p if lo <= e["i"] <= hi]) for p in per_body]})
    found["clicks: credit centroids per window"] = windows
    first = next((w["distance milli"] for w in windows if w["distance milli"] is not None), None)
    last = next((w["distance milli"] for w in reversed(windows) if w["distance milli"] is not None), None)
    found["clicks: distance last window - first window milli"] = None if first is None or last is None else last - first
    return found


def main(argv):
    sys.set_int_max_str_digits(0)
    reads = {}
    for path in argv[1:]:
        r = read(path)
        reads[path] = r
        print(json.dumps(r))
    d3 = [r for p, r in reads.items() if "d3" in p]
    d6 = [r for p, r in reads.items() if "d6" in p]
    for a in d3:
        for b in d6:
            if ("like" in a["run"]) == ("like" in b["run"]) and ("opposite" in a["run"]) == ("opposite" in b["run"]):
                n3, n6 = a["D2 = d(T) - 2 d(T/2) + d(0) milli"], b["D2 = d(T) - 2 d(T/2) + d(0) milli"]
                v3, v6 = a["d(T) - d(0) milli"], b["d(T) - d(0) milli"]
                print(json.dumps({"ratio": [a["run"], b["run"]],
                                  "a(d3) / a(d6) per 10^9 (second differences)": None if n6 == 0 else (BILLION * n3) // n6,
                                  "v(d3) / v(d6) per 10^9 (the runs' displacements)": None if v6 == 0 else (BILLION * v3) // v6,
                                  "nature 1 / d^2": 4 * BILLION}))


if __name__ == "__main__":
    main(sys.argv)
