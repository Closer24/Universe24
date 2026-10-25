"""cs6: the retrace read on a record: for every top of the mean with the whole board turning, X(top + k) against X(top - k), the first k where they differ and the X course around the mirror of the clicks; the clicks' intervals (births, credits) listed. Usage: python mirror.py <record.json> [top ...]"""
import json, sys
sys.set_int_max_str_digits(0)
rec = json.load(open(sys.argv[1]))
diag = {d["i"]: d for d in rec["diag"]}
n = int(rec["intervals"])
log = rec["log"]
clicks = sorted({(e["i"], e["event"]) for e in log if e["event"] in ("birth", "credit")})
by = {}
for i, ev in clicks:
    by.setdefault(ev, []).append(i)
print("clicks by kind (intervals):", {k: v[:12] for k, v in by.items()})
tops = [int(x) for x in sys.argv[2:]] or [i for i in range(2, n) if diag[i]["X_mean"] >= diag[i - 1]["X_mean"] and diag[i]["X_mean"] > diag[i + 1]["X_mean"] and diag[i + 1]["turned"] == rec["cube"] ** 3]
for t in tops:
    first = None
    for k in range(1, min(t, n - t) + 1):
        if diag[t + k]["X_mean"] != diag[t - k]["X_mean"] or diag[t + k]["X_min"] != diag[t - k]["X_min"]:
            first = k
            break
    print(f"top {t} (X {diag[t]['X_mean']}, turned at {t + 1}: {diag[t + 1]['turned']}): X(top + k) == X(top - k) for k < {first}; the mirror {t + first if first else None} of the interval {t - first if first else None}")
    if first:
        for k in range(max(1, first - 2), first + 12):
            if t + k <= n and t - k >= 0:
                print(f"   k {k}: i {t - k} X {diag[t - k]['X_mean']} | i {t + k} X {diag[t + k]['X_mean']} ({diag[t + k]['X_min']}..{diag[t + k]['X_max']}) share {diag[t + k]['light_share_min_max_hundredths']} gapped whole {diag[t + k]['gapped_whole_nodes']} turned {diag[t + k]['turned']}")
    lo = min(range(t, min(n, t + 2 * t) + 1), key=lambda i: diag[i]["X_mean"])
    print(f"   the bottom after the top: i {lo} X {diag[lo]['X_mean']} ({diag[lo]['X_min']}..{diag[lo]['X_max']}); velocity X(i) - X(i - 1) at the mirror points:", [(i, diag[i]["X_mean"] - diag[i - 1]["X_mean"]) for i in range(max(1, t + (first or 1) - 1), min(n, lo + 2) + 1, 1) if i > t][:20])
