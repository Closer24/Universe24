"""The summary of a tq1_torque.py output: the record's terms, the identity's count, the quiet intervals' terms."""
import json, sys
from fractions import Fraction
sys.set_int_max_str_digits(0)
for path in sys.argv[1:]:
    d = json.load(open(path)); s = d["summary"]; per = d["per_interval"]
    print("==", path.split("/")[-1], "cube", s["cube"], "intervals", s["intervals"], "identity_misses", s["identity_misses"], "line_misses", s["line_misses"], "ms", s["ms"])
    print("  2L_end", s["2L_end"], "P_end", s["P_end"])
    print("  sum|term| per component (integers rounded down):")
    for t, v in s["sum_abs_over_record"].items():
        print("    %-10s" % t, [str(int(Fraction(x))) for x in v])
    for t, v in s["sum_abs_int"].items():
        print("    %-10s" % t, [str(x) for x in v])
    print("  rounding bound", s["rounding_bound_2L_total"], "rounding/bound percent", s["rounding_bound_ratio_percent"])
    quiet = [r for r in per if r["clicks"] == 0 and r["births"] == 0 and r["turned"] == 0]
    print("  intervals with no click and no swap:", len(quiet), "of", len(per), "; with a click or a birth:", sum(1 for r in per if r["clicks"] or r["births"]), "; with a swap:", sum(1 for r in per if r["turned"]))
    zero_div = sum(1 for r in per if all(x == 0 for x in r["dL2_divisions"]))
    zero_terms = sum(1 for r in per if all(Fraction(x) == 0 for t in r["terms"] for x in r["terms"][t]))
    print("  intervals with the divisions' dL2 = 0:", zero_div, "; with every term 0:", zero_terms, "; swap dL2 = 0:", sum(1 for r in per if all(x == 0 for x in r["dL2_swap"])), "; lays dL2 = 0:", sum(1 for r in per if all(x == 0 for x in r["dL2_lays"])))
    # the largest term by name per interval
    from collections import Counter
    c = Counter()
    for r in per:
        best = max(((t, max(abs(Fraction(x)) for x in v)) for t, v in r["terms"].items()), key=lambda z: z[1])
        if best[1] > 0:
            c[best[0]] += 1
    print("  the largest term of the divisions, by interval:", dict(c))
    sw = sum(1 for r in per if max(abs(x) for x in r["dL2_swap"]) > max(abs(Fraction(x)) for t, v in r["terms"].items() for x in v))
    print("  intervals where the swap's change exceeds every division term:", sw)
