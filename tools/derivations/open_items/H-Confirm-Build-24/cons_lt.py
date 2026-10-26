"""LT-S1 on a record's log: every booking of the close (the credits' takes, the laid-back credits, the births' takes and the two lay ends) checked per axis as the identity carry_was - carry - dP p_0^2 = recoil x (trace den Gamma^2 T) (the sign -dP, the Boss's correction) and as the +dP form beside it; the count held of N and the bookings' sum per axis."""
import json, sys
sys.set_int_max_str_digits(0)
r = json.load(open(sys.argv[1]))
u = r["universe"]["integers"] if "integers" in r.get("universe", {}) else r["universe"]
def I(k):
    for d in (r, u):
        if k in d:
            return int(d[k])
    raise KeyError(k)
trace, den, gamma, T = I("trace"), I("den"), I("gamma"), I("T")
wall = trace * den * gamma * gamma * T
minus = plus = total = 0
dp_sum, recoil_sum = [0, 0, 0], [0, 0, 0]
kinds = {}
for e in r["log"]:
    if e["event"] not in ("birth", "credit"):
        continue
    bookings = [(t, "take") for t in e.get("takes", [e]) if "recoil" in t]
    if e["event"] == "birth" and "clock_ends" in e:
        bookings += [({k: e[k + "_ends"][j] for k in ("clock", "recoil", "carry_was", "carry")} | {"dP_take": e["dP_lay_ends"][j]}, "end") for j in range(2)]
    for t, kind in bookings:
        dp = t["dP_take"]
        for a in range(3):
            total += 1
            kinds[kind] = kinds.get(kind, 0) + 1
            lhs = int(t["carry_was"][a]) - int(t["carry"][a])
            minus += lhs - int(dp[a]) * int(t["clock"]) ** 2 == int(t["recoil"][a]) * wall
            plus += lhs + int(dp[a]) * int(t["clock"]) ** 2 == int(t["recoil"][a]) * wall
            dp_sum[a] += int(dp[a]); recoil_sum[a] += int(t["recoil"][a])
print(sys.argv[1].split("/")[-1], "wall bits", wall.bit_length(), "axis-bookings", total, "by kind", kinds, "-dP identity held", minus, "+dP form held", plus, "dP summed", dp_sum, "recoil levels summed", recoil_sum)
