"""The runs' summary: per world and phase, the intervals whose change of L2 (about the centre, doubled) or P is not 0, the largest |change|, and the step's split into the remainders' part and the rational part; the end about the centroid."""
import json, sys
from fractions import Fraction
sys.set_int_max_str_digits(0)
def fr(s): 
    n, d = s.split("/"); return Fraction(int(n), int(d))
for path in sys.argv[1:]:
    r = json.load(open(path))
    per = r["per_interval"]
    out = {"world": r["world"].split("/")[-1], "cube": r["cube"], "intervals": len(per), "rows": r["rows"], "counts": {k: r["counts"][k] for k in ("births", "body_clicks", "turns")}}
    for key in ("dL2_step", "dL2_write", "dL2_swap", "dL2_click", "dP_step", "dP_write", "dP_swap", "dP_click"):
        nz = [p for p in per if any(x != 0 for x in p[key])]
        out[key] = {"intervals not 0": len(nz), "max abs": max((abs(x) for p in per for x in p[key]), default=0)}
    rem = [sum(abs(fr(s)) for s in p["dL2_step_remainders"]) for p in per]
    rat = [sum(abs(fr(s)) for s in p["dL2_step_rational"]) for p in per]
    tot = [sum(abs(x) for x in p["dL2_step"]) for p in per]
    out["step: sum |dL2| over the run"] = sum(tot)
    out["step: remainders' part, sum |.| over the run (rounded)"] = int(round(sum(rem)))
    out["step: rational part, sum |.| over the run (rounded)"] = int(round(sum(rat)))
    out["step: intervals with the rational part 0"] = sum(1 for x in rat if x == 0)
    out["step: intervals with the remainders' part 0"] = sum(1 for x in rem if x == 0)
    out["L2 at the end"] = per[-1]["L2_end"]; out["P at the end"] = per[-1]["P_end"]
    out["L2 max abs over the run"] = max(abs(x) for p in per for x in p["L2_end"])
    cl = [p for p in per if p["clicks"] or p["births"]]
    out["closes with clicks or births"] = len(cl)
    out["closes with clicks or births and dL2_click 0"] = sum(1 for p in cl if all(x == 0 for x in p["dL2_click"]))
    sw = [p for p in per if p["turned"]]
    out["intervals with turns"] = len(sw)
    out["intervals with turns and dL2_swap 0"] = sum(1 for p in sw if all(x == 0 for x in p["dL2_swap"]))
    out["end about centroid"] = r["end_about_centroid"]
    print(json.dumps(out, indent=None))
    print()
