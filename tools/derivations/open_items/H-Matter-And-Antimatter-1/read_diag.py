"""ma1's reader of a record's readings (<prefix>_diag.json): the mean's course (the tops where the turned count is the board's, the returns where the mean equals Gamma), e per 40 intervals, the first turn of fewer Nodes than the board, the counts, the merger premise summed, the gap-0 share's peak and the current's peak, the invariance held at the end. Integers only."""
import json, sys

sys.set_int_max_str_digits(0)
d = json.load(open(sys.argv[1]))
diags = d["diag"]
s = d["summary"]
nodes = len(json.load(open(sys.argv[1].replace("_diag.json", "_record.json")))["nodes"][0]["X"]) if len(sys.argv) < 3 else int(sys.argv[2])
gamma = 1000
means = [(x["i"], x["X mean/min/max"][0]) for x in diags]
tops_all = [(x["i"], x["X mean/min/max"][0]) for x in diags if x["turned"] == nodes]
partial = [(x["i"], x["turned"]) for x in diags if 0 < x["turned"] < nodes]
returns = [x["i"] for x in diags if x["X mean/min/max"][0] == gamma and x["i"] > 0]
peak = max(means, key=lambda t: t[1])
e_marks = [(x["i"], x["e max (thousandths)"]) for x in diags if x["i"] % 40 == 0]
e_first = next((x["i"] for x in diags if x["e max (thousandths)"] > 0), None)
share_peak = max(diags[1:], key=lambda x: x["gap0 share max (units, rem)"][0] * (10 ** 30) + x["gap0 share max (units, rem)"][1])
f_peak = max(diags, key=lambda x: x["F max"])
h_peak = max(diags, key=lambda x: x["twist max"])
whole_last = max((x["i"] for x in diags if x["mergers"]["whole"] > 0), default=None)
w_tot = sorted(set(x["W total"] for x in diags))
print(json.dumps({
    "laid": d["laid"],
    "intervals": diags[-1]["i"],
    "mean at the marks": [m for m in means if m[0] % 50 == 0 or m[0] in (58, 115, 116, 173, 230, 231, 288, 345, 346)],
    "mean's peak (i, X)": peak,
    "tops with every Node turning (i, X)": tops_all[:8],
    "turns of fewer than every Node (i, count), first 6": partial[:6],
    "returns to Gamma (i)": returns[:8],
    "e at every 40th": e_marks,
    "first interval with e > 0": e_first,
    "gap0 share peak (i, units, rem)": [share_peak["i"], share_peak["gap0 share max (units, rem)"]],
    "nodes at one unit of light, max": max(x["nodes at one unit"] for x in diags[1:]),
    "F max peak (i, F)": [f_peak["i"], f_peak["F max"]],
    "twist max peak (i, h)": [h_peak["i"], h_peak["twist max"]],
    "W total values": w_tot[:6] + (["..."] if len(w_tot) > 6 else []),
    "mergers summed": s["mergers summed over the intervals"],
    "last interval with a whole massive Link": whole_last,
    "counts": s["counts"],
    "run back": s["run back"],
    "integers": s["integers"], "max bits": s["max bits"], "transient bits": s["max transient bits"],
    "48 at the end": s["48"],
    "invariance at the end": s["invariance at the end"],
    "invariance checks": [(x["i"], x["invariance"]) for x in diags if "invariance" in x][:9],
}))
