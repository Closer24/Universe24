"""cp2's reader of a record's births: per birth the P balance on three axes (dP_take plus the two packets' lay momenta), the J balance on three axes about the take's Node from the per-Link bookings (the take's six Links and every lay act's, 2J in Link-halves, coordinates unwrapped about the taker), each packet's own moment about its centre (the axial datum), the pair's relative L about the Link's midpoint (the orbit), the remainder of the wave number's division, the wave numbers, the packets' whole charge W summed over their Nodes (packet_levels recomputed from A, B, den), the course against a cached record. Usage: cp2_moment.py <src> <record.json> [cached.json] > summary"""
import json
import os
import sys

sys.path.insert(0, sys.argv[1])
sys.set_int_max_str_digits(0)
os.environ["CP2_FORM"] = "1"
from event_universe import close as close_  # noqa: E402


def cross3(r, p):
    return [r[1] * p[2] - r[2] * p[1], r[2] * p[0] - r[0] * p[2], r[0] * p[1] - r[1] * p[0]]


def add(a, b):
    return [x + y for x, y in zip(a, b)]


class Stub:
    def __init__(self, rec):
        self.A, self.B = (int(x) for x in rec["log"][0].get("amplitude", [0, 0])) if False else (None, None)
        self.den, self.cube = int(rec["den"]), int(rec["cube"])
        self.shape = (self.cube,) * 3


rec = json.load(open(sys.argv[2]))
cube = int(rec["cube"])
log = rec["log"]
births = [e for e in log if e["event"] == "birth"]
stub = Stub(rec)
P_sum, J_sum, L_sum, S_sum = [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]
P_exact = J_exact = L_zero = w_zero = w_pair_zero = 0
rows = []
max_rem_permille, max_h = 0, 0


def rel(n, at):
    return [((n[a] - at[a] + cube // 2) % cube) - cube // 2 for a in range(3)]


def moment_of_links(acts, at):
    """2J about `at` of a list of [node, [[down, up] x 3]] bookings: the up Link's lower end the Node, the down Link's the Node less e_a."""
    j2 = [0, 0, 0]
    for n, per in acts:
        r = rel(n, at)
        for a in range(3):
            e = [0, 0, 0]
            e[a] = 1
            down, up = int(per[a][0]), int(per[a][1])
            arm_up = [2 * r[b] + e[b] for b in range(3)]
            arm_down = [2 * r[b] - e[b] for b in range(3)]
            j2 = add(j2, add(cross3(arm_up, [up * x for x in e]), cross3(arm_down, [down * x for x in e])))
    return j2


for e in births:
    dpt = [int(x) for x in e["dP_take"]]
    at, minus, plus = e["node"], e["minus"], e["plus"]
    ends = [[int(x) for x in v] for v in e.get("dP_lay_ends", [[0, 0, 0], [int(x) for x in e["dP_lay"]]])]
    p = add(dpt, add(ends[0], ends[1]))
    take_links = e.get("take_links")
    acts = e.get("lay_acts", [])
    j2 = [0, 0, 0]
    if take_links is not None:
        j2 = add(moment_of_links([[at, take_links]], at), moment_of_links(acts, at))
    n_acts = len(acts) // 2
    spin = [[0, 0, 0], [0, 0, 0]]
    if acts:
        spin[0] = moment_of_links(acts[:n_acts], minus)
        spin[1] = moment_of_links(acts[n_acts:], plus)
    mid2 = add(minus, plus)
    arm_m = [2 * minus[b] - mid2[b] for b in range(3)]
    arm_p = [2 * plus[b] - mid2[b] for b in range(3)]
    l2 = add(cross3(arm_m, ends[0]), cross3(arm_p, ends[1]))
    stub.A, stub.B = (int(x) for x in e["amplitude"])
    waves = e.get("wave", [None, None])
    w_whole = []
    for where, sense, wv in ((minus, -1, waves[0]), (plus, 1, waves[1])):
        total = 0
        for _n, (rn, rb, inow, ib) in close_.packet_levels(stub, tuple(where), sense, wv):
            total += rn * ib - rb * inow
        w_whole.append(total)
    rem = e.get("remainder", [0, 0, 0])
    scale = max(1, max(abs(x) for x in dpt))
    permille = max(abs(int(x)) for x in p) * 1000 // scale
    max_rem_permille = max(max_rem_permille, permille)
    for wv in waves:
        if wv:
            max_h = max(max_h, max(abs(int(x)) for x in wv))
    P_sum, J_sum, L_sum = add(P_sum, p), add(J_sum, j2), add(L_sum, l2)
    S_sum = add(S_sum, add(spin[0], spin[1]))
    P_exact += p == [0, 0, 0]
    J_exact += j2 == [0, 0, 0]
    L_zero += l2 == [0, 0, 0]
    w_zero += sum(int(x) for x in e["W_children"]) == 0
    w_pair_zero += sum(w_whole) == 0
    rows.append({"i": e["i"], "at": at, "minus": minus, "plus": plus, "dP_take": dpt, "dP_lay_ends": ends, "P_balance": p, "P_balance_permille": permille,
                 "2J_balance_about_taker": j2, "2L_relative": l2, "2S_packets": spin, "wave": waves, "remainder": rem, "passes": e.get("passes"),
                 "W_centres": e["W_children"], "W_packets": w_whole, "W_sum": sum(w_whole), "levels": e["levels"], "booked": e["booked"], "taken": e["taken"]})
summary = {"record": sys.argv[2], "births": len(births), "P_exact": P_exact, "J_exact_about_taker": J_exact, "L_relative_zero": L_zero, "W_centres_sum_zero": w_zero,
           "W_packets_sum_zero": w_pair_zero, "P_sum": P_sum, "2J_sum": J_sum, "2L_sum": L_sum, "2S_sum": S_sum, "max_P_balance_permille_of_recoil": max_rem_permille, "max_|h|": max_h,
           "den": rec["den"], "counts": rec.get("counts"), "run_back": rec.get("run_back")}
if len(sys.argv) > 3:
    cached = json.load(open(sys.argv[3]))
    cb = [e for e in cached["log"] if e["event"] == "birth"]
    summary["course"] = {"births_head": len(cb), "births_flag": len(births), "intervals_head": sorted({e["i"] for e in cb}), "intervals_flag": sorted({e["i"] for e in births}),
                         "counts_head": cached.get("counts"), "stops_head": cached.get("counts", {}).get("refused_stop"), "stops_flag": rec.get("counts", {}).get("refused_stop")}
print(json.dumps({"summary": summary, "births": rows}, default=str))
