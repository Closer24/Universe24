"""cp1's reader of a record's births under the packet form: per birth the P balance on three axes (dP_take plus the two packets' booked momenta), the J balance about the take's Node (the take's moment 0 there by the one-Node theorem; each packet's moment about its own centre plus its arm times its momentum) and about the origin, the pair's relative L about the Link's midpoint (coordinates doubled; the packets' own moments included), the remainder per axis in per mille of the take's component, the wave numbers and the band's cap, the packets' charges summed, the cost against the cached head record (booked and taken per birth, in order). Usage: cp1_moment.py <record.json> <out.json> [cached.json]"""
import json
import sys

sys.set_int_max_str_digits(0)


def cross3(r, p):
    return [r[1] * p[2] - r[2] * p[1], r[2] * p[0] - r[0] * p[2], r[0] * p[1] - r[1] * p[0]]


def add(a, b):
    return [x + y for x, y in zip(a, b)]


def permille(part, whole):
    return None if whole == 0 else (1000 * abs(part)) // abs(whole)


rec = json.load(open(sys.argv[1]))
world = rec.get("world", {})
cube = int(world["shape"][0]) if isinstance(world, dict) and "shape" in world else None
log = rec["log"]
births = [e for e in log if e["event"] == "birth"]
credits = [e for e in log if e["event"] == "credit"]
den = None
if isinstance(rec.get("universe"), dict):
    den = int(rec["universe"]["integers"]["den"])
cap = None
if den is not None:
    sq = (den * den) // 2
    cap = int(sq**0.5)
    while cap * cap > sq:
        cap -= 1
    while (cap + 1) * (cap + 1) <= sq:
        cap += 1
P_sum, J_at_sum, J_o_sum, L_sum = [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]
P_exact = J_at_exact = J_o_exact = L_zero = w_zero = packets = 0
rows = []
worst = {"P_permille": 0, "J_at_permille": 0, "W_permille": 0}
within = {k: 0 for k in (1, 2, 5, 10, 20, 50, 100)}
within_j = {k: 0 for k in (1, 2, 5, 10, 20, 50, 100)}
capped_axes = 0
bits = 0
for e in births:
    dpt = [int(x) for x in e["dP_take"]]
    at, minus, plus = [int(x) for x in e["node"]], [int(x) for x in e["minus"]], [int(x) for x in e["plus"]]
    ends = e.get("dP_lay_ends")
    moments = e.get("moment_ends", [[0, 0, 0], [0, 0, 0]])
    if ends is None:
        ends = [[0, 0, 0], [int(x) for x in e["dP_lay"]]]
    ends = [[int(x) for x in v] for v in ends]
    moments = [[int(x) for x in v] for v in moments]
    axis = next((b for b in range(3) if minus[b] != plus[b]), 0)
    arms = []
    for end in (minus, plus):
        if end == at:
            arms.append([0, 0, 0])
        else:
            d = end[axis] - at[axis]
            if cube is not None and abs(d) > 1:
                d = 1 if d < 0 else -1
            arm = [0, 0, 0]
            arm[axis] = d
            arms.append(arm)
    p = add(dpt, add(ends[0], ends[1]))
    j_at = add(add(cross3(arms[0], ends[0]), moments[0]), add(cross3(arms[1], ends[1]), moments[1]))
    j_o = add(j_at, cross3(at, p))
    mid2 = add(arms[0], arms[1])
    l2 = [0, 0, 0]
    for k in range(2):
        l2 = add(l2, add(cross3([2 * arms[k][b] - mid2[b] for b in range(3)], ends[k]), [2 * m for m in moments[k]]))
    w = [int(x) for x in e["W_children"]]
    w_sum = w[0] + w[1]
    waves = e.get("waves", [[0, 0, 0], [0, 0, 0]])
    capped = [a for v in waves for a, x in enumerate(v) if cap is not None and abs(int(x)) == cap]
    capped_axes += len(capped)
    P_sum, J_at_sum, J_o_sum, L_sum = add(P_sum, p), add(J_at_sum, j_at), add(J_o_sum, j_o), add(L_sum, l2)
    P_exact += p == [0, 0, 0]
    J_at_exact += j_at == [0, 0, 0]
    J_o_exact += j_o == [0, 0, 0]
    L_zero += l2 == [0, 0, 0]
    w_zero += w_sum == 0
    packets += "waves" in e
    pm = [permille(p[a], dpt[a]) for a in range(3)]
    pm_max = max((x for x in pm if x is not None), default=0)
    # the J balance about the take's Node in per mille of the take's moment about the Link's midpoint (half the arm times the transverse recoil): 2 |J_at| against |e x dP_take|
    e_axis = [0, 0, 0]
    e_axis[axis] = 1
    take_moment2 = cross3(e_axis, dpt)
    jm = max((permille(2 * j_at[a], take_moment2[a]) for a in range(3) if take_moment2[a] != 0), default=0)
    wm = permille(w_sum, w[1]) if w[1] else None
    worst["P_permille"] = max(worst["P_permille"], pm_max)
    worst["J_at_permille"] = max(worst["J_at_permille"], jm)
    worst["W_permille"] = max(worst["W_permille"], wm or 0)
    for k in within:
        within[k] += pm_max <= k
        within_j[k] += jm <= k
    bits = max(bits, *(abs(int(x)).bit_length() for x in (e["booked"], e["taken"], *dpt, *p, *j_o, *l2, *(int(y) for v in waves for y in v))))
    rows.append({"i": e["i"], "node": at, "axis": axis, "minus": minus, "plus": plus, "waves": waves, "capped_axes": capped, "dP_take": dpt, "ends": ends, "moment_ends": moments, "P_balance": p, "P_permille": pm, "J_at_balance": j_at, "J_at_permille": jm, "J_origin_balance": j_o, "L_rel_x2": l2, "W_children": w, "W_sum": w_sum, "W_permille": wm, "booked": int(e["booked"]), "taken": int(e["taken"]), "levels": int(e["levels"]), "amplitude_packets": e.get("amplitude_packets"), "packet_nodes": e.get("packet_nodes")})
summary = {
    "births": len(births), "births_as_packets": packets, "credits": len(credits), "counts": rec.get("counts"), "run_back": rec.get("run_back"),
    "P_exact": P_exact, "J_at_exact": J_at_exact, "J_origin_exact": J_o_exact, "L_rel_zero": L_zero, "W_sum_zero": w_zero,
    "P_within_permille": within, "J_at_within_permille": within_j, "worst": worst, "capped_axes": capped_axes, "cap": cap,
    "P_sum": P_sum, "J_at_sum": J_at_sum, "J_origin_sum": J_o_sum, "L_rel_x2_sum": L_sum, "bits_max": bits,
    "booked_sum": sum(int(e["booked"]) for e in births), "taken_sum": sum(int(e["taken"]) for e in births),
}
if len(sys.argv) > 3:
    cached = json.load(open(sys.argv[3]))
    cl = cached["log"]
    cb = [e for e in cl if e["event"] == "birth"]
    summary["against_cached"] = {
        "births": [len(births), len(cb)], "credits": [len(credits), sum(1 for e in cl if e["event"] == "credit")], "log_lengths": [len(log), len(cl)],
        "first_apart": next((k for k, (a, b) in enumerate(zip(log, cl)) if a != b), None),
        "keys_equal": {k: rec.get(k) == cached.get(k) for k in sorted(set(rec) | set(cached))},
        "booked_sum": [summary["booked_sum"], sum(int(e["booked"]) for e in cb)], "taken_sum": [summary["taken_sum"], sum(int(e["taken"]) for e in cb)],
        "birth_intervals": [[e["i"] for e in births], [e["i"] for e in cb]],
        "cost_per_birth_permille": [permille(int(a["booked"]) - int(b["booked"]), int(b["booked"])) for a, b in zip(births, cb)],
    }
json.dump({"summary": summary, "rows": rows}, open(sys.argv[2], "w"), default=str)
print(json.dumps(summary, default=str))
