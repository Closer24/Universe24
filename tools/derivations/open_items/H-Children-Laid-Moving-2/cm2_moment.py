"""cm2's reader of a record's births: per birth the P balance (dP_take plus the ends' lay momenta), the J balance about the origin (the arm times the momentum booked at each Node, the one-Node theorem), the pair's relative L about the Link's midpoint (coordinates doubled), the along-Link remainder, the moving integer; summed over the record; the course against a cached record. Usage: cm2_moment.py <record.json> [cached.json] > summary"""
import json
import sys

sys.set_int_max_str_digits(0)


def cross3(r, p):
    return [r[1] * p[2] - r[2] * p[1], r[2] * p[0] - r[0] * p[2], r[0] * p[1] - r[1] * p[0]]


def add(a, b):
    return [x + y for x, y in zip(a, b)]


rec = json.load(open(sys.argv[1]))
cube = int(rec["cube"]) if "cube" in rec else None
log = rec["log"]
births = [e for e in log if e["event"] == "birth"]
credits = [e for e in log if e["event"] == "credit"]
P_sum, J_sum, L_sum = [0, 0, 0], [0, 0, 0], [0, 0, 0]
P_exact = J_exact = L_zero = along_exact = w_zero = 0
rows = []
worst_p, worst_rem, max_a, max_levels = 0, 0, 0, 0
for e in births:
    dpt = [int(x) for x in e["dP_take"]]
    ends = e.get("dP_lay_ends")
    at, minus, plus = e["node"], e["minus"], e["plus"]
    if ends is None:
        ends = [[0, 0, 0], [int(x) for x in e["dP_lay"]]]  # the head books the lay per Link: read at the + end for want of the per-end key
    ends = [[int(x) for x in v] for v in ends]
    p = add(dpt, add(ends[0], ends[1]))
    j = add(cross3(at, dpt), add(cross3(minus, ends[0]), cross3(plus, ends[1])))
    # the Link's axis and the midpoint doubled
    axis = next(b for b in range(3) if minus[b] != plus[b])
    mid2 = add(minus, plus)
    arm_m = [2 * minus[b] - mid2[b] for b in range(3)]
    arm_p = [2 * plus[b] - mid2[b] for b in range(3)]
    l2 = add(cross3(arm_m, ends[0]), cross3(arm_p, ends[1]))  # twice the relative L
    rem_along = p[axis]
    P_sum, J_sum, L_sum = add(P_sum, p), add(J_sum, j), add(L_sum, l2)
    P_exact += p == [0, 0, 0]
    J_exact += j == [0, 0, 0]
    L_zero += l2 == [0, 0, 0]
    along_exact += rem_along == 0
    w_zero += sum(int(x) for x in e["W_children"]) == 0
    mv = e.get("moving", [0, 0])
    max_a = max(max_a, max(abs(int(x)) for x in mv))
    max_levels = max(max_levels, abs(int(e["levels"])))
    take_along = dpt[axis]
    permille = None if take_along == 0 else (1000 * abs(rem_along)) // abs(take_along)
    worst_rem = max(worst_rem, permille or 0)
    worst_p = max(worst_p, max(abs(x) for x in p))
    rows.append({"i": e["i"], "node": at, "axis": axis, "moving": mv, "dP_take": dpt, "ends": ends, "P_balance": p, "J_balance": j, "L_rel_x2": l2, "along_remainder_permille": permille, "booked": e["booked"], "taken": e["taken"], "levels": e["levels"], "W_children": e["W_children"]})
summary = {
    "births": len(births), "credits": len(credits), "counts": rec.get("counts"), "run_back": rec.get("run_back"),
    "P_exact": P_exact, "J_exact": J_exact, "L_rel_zero": L_zero, "along_exact": along_exact, "W_sum_zero": w_zero,
    "P_sum": P_sum, "J_sum": J_sum, "L_rel_x2_sum": L_sum, "worst_P_component": worst_p, "worst_along_remainder_permille": worst_rem,
    "max_moving": max_a, "max_levels": max_levels,
    "bits_max_level": max((abs(int(x)).bit_length() for e in births for x in (e["booked"], e["taken"], *e["dP_take"])), default=0),
}
if len(sys.argv) > 2:
    cached = json.load(open(sys.argv[2]))
    cl = cached["log"]
    summary["against_cached"] = {"births": [len(births), sum(1 for e in cl if e["event"] == "birth")], "credits": [len(credits), sum(1 for e in cl if e["event"] == "credit")], "log_lengths": [len(log), len(cl)], "first_apart": next((k for k, (a, b) in enumerate(zip(log, cl)) if a != b), None), "keys_equal": {k: rec.get(k) == cached.get(k) for k in sorted(set(rec) | set(cached))}}
    cb = [e for e in cl if e["event"] == "birth"]
    summary["cached_births_P_lay_zero"] = sum(1 for e in cb if [int(x) for x in e["dP_lay"]] == [0, 0, 0])
print(json.dumps({"summary": summary, "rows": rows}, default=str))
