"""The shortfall's first-order derivation in integers (eq2, item 1): the carrier's time line is a Rule3 line with the write, so its second difference per interval is the write's quotient, 4 X p_0 (forms) / (Gamma^2 T) (held_numerator over held_wall(54, den, Gamma, 4, T) with the trace 0 on a uniform board); the sea's part of the forms is the product of its two momenta's roundings, u_in u_out = v^2 to the rounding (u = odd_rounded(2 P + 1, 2 w X), P = (w div 2)(X_b + X_n) v + r - half), v the gap-0 re line's now - before (the drift 189 at the seed). A body's click at the interval m takes s levels off v at every Node (take_at: now toward before) and the fall does not give them back; after the mirror of m the fall's source is short by 4 X p_0 (v^2 - (v - s)^2) / (Gamma^2 T) per interval against the rise, over the m intervals down to the mirror of the seed, so the carrier's level at the seed's mirror is short by about SUM over the clicks of 4 X p_0 s (2 v - s) m (m + 1) / (2 Gamma^2 T), with X p_0 / Gamma^2 near 1 over the last intervals: D1 = SUM 2 s (2 v - s) m (m + 1) div T, in thousandths here. Usage: shortfall.py <record.json>: the clicks' (m, s, v) read from the record's first cycle, D1 against the measured parting at the seed's mirror and the bottom."""
import json
import sys
from collections import Counter

sys.set_int_max_str_digits(0)
run = json.load(open(sys.argv[1], encoding="utf-8"))
T, gamma = int(run["T"]), int(run["gamma"])
lines = run["nodes"]
n = len(lines[0]["X"])
m = {int(l["i"]): sum(int(x) for x in l["X"]) // n for l in lines}
top = [int(l["i"]) for l in lines if len(l["turned"]) == n][0]
credits = [c for c in run["log"] if c["event"] == "credit" and int(c["i"]) < top]
per_node = Counter(tuple(c["node"]) for c in credits)
at = min(per_node)  # one Node's clicks, every Node alike
clicks = sorted((int(c["i"]), int(c["levels"]), int(c["frame"]["re_start_now"] if False else 0)) for c in credits if tuple(c["node"]) == at)
# the sea's velocity before each click from the taker's levels: taken_now_was - before
v_before = {int(c["i"]): int(c["taker"][0]) - int(c["taker"][1]) for c in credits if tuple(c["node"]) == at}
rows = []
thousandths = 0
for i, s, _ in clicks:
    v = v_before[i]
    d1 = 2 * s * (2 * v - s) * i * (i + 1) * 1000 // T
    thousandths += d1
    rows.append({"interval m": i, "levels s": s, "v before": v, "v after": v - s, "v^2 lost": s * (2 * v - s), "D1 (thousandths)": d1})
mirror_seed = 2 * top - 2
parting = [(k, m[k], m[2 * top - 2 - k], m[2 * top - 2 - k] - m[k]) for k in range(0, 16) if k in m]
bottom = min((m[k], k) for k in m if top < k < 2 * top + 12)
print(json.dumps({
    "record": sys.argv[1], "top": top, "clicks at one Node in the rise (m, s)": [(i, s) for i, s, _ in clicks],
    "rows": rows, "D1 first order (thousandths)": thousandths,
    "measured: X(seed's mirror) = X(2 top - 2)": m[mirror_seed], "measured shortfall at the seed's mirror": gamma - m[mirror_seed],
    "measured bottom (X, interval)": bottom, "measured shortfall at the bottom": gamma - bottom[0],
    "the parting (k, X_rise(k), X_fall(mirror k), fall - rise)": parting,
    "levels taken per Node in the rise": sum(s for _, s, _ in clicks), "credits in the rise": len(credits),
}, indent=1))
