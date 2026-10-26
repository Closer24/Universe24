"""The torque's terms summed over a record, to the integer (the quotient of each exact fraction, the remainder named as a fraction of one): the term carrying the torque named. Usage: python tq2_summary.py out/*.json"""
import json, sys
from fractions import Fraction as Fr

def fr(x):
    n, _, d = x.partition("/")
    return Fr(int(n), int(d or 1))

def ip(q):
    return q.numerator // q.denominator if q >= 0 else -((-q.numerator) // q.denominator)

def main(argv):
    sys.set_int_max_str_digits(0)
    for path in argv[1:]:
        o = json.load(open(path))
        per = o["per_interval"]
        print(f"== {o['world']} cube {o['cube']} intervals {o['intervals']} ms {o['ms']} counts births {o['counts']['births']} turns {o['counts']['turns']} body_clicks {o['counts']['body_clicks']}")
        print(f"   REST not 0 on {o['intervals_with_REST_not_0']} of {len(per)} intervals (the identity's check)")
        print(f"   L2 end {o['L2_end']}  P end {o['P_end']}")
        print(f"   phases summed: step {o['sum_phases']['step']} write {o['sum_phases']['write']} swap {o['sum_phases']['swap']} click {o['sum_phases']['click']}")
        for k, v in o["sum_terms"].items():
            a = o["sum_abs_terms"][k]
            print(f"   {k:11s} sum {[ip(fr(x)) for x in v]}  sum|.| {[ip(fr(x)) for x in a]}")
        n_sw = sum(1 for r in per if any(r["dL2_swap"])); n_st = sum(1 for r in per if any(r["dL2_step"]))
        n_asym = sum(1 for r in per if any(fr(x) != 0 for x in r["terms"]["LINKS_ASYM"]))
        n_sym = sum(1 for r in per if any(fr(x) != 0 for x in r["terms"]["LINKS_SYM"]))
        n_own = sum(1 for r in per if any(fr(x) != 0 for x in r["terms"]["OWN"]))
        n_round = sum(1 for r in per if any(fr(x) != 0 for x in r["terms"]["ROUND"]))
        n_cl = sum(1 for r in per if any(r["dL2_click"]))
        n_wr = sum(1 for r in per if any(r["dL2_write"]))
        print(f"   intervals with dL2_step not 0: {n_st}; swap not 0: {n_sw}; click not 0: {n_cl}; write not 0: {n_wr}; LINKS_ASYM not 0: {n_asym}; LINKS_SYM not 0: {n_sym}; OWN not 0: {n_own}; ROUND not 0: {n_round}")
        # the largest single interval per term
        for k in ("LINKS_SYM", "LINKS_ASYM", "OWN", "ROUND", "RIDE", "TURN", "CURL"):
            best = max(per, key=lambda r: max(abs(fr(x)) for x in r["terms"][k]))
            m = max(abs(fr(x)) for x in best["terms"][k])
            print(f"   largest {k:11s} at interval {best['i']}: {ip(m)}")
        first = next((r for r in per if any(r["dL2_step"])), None)
        if first:
            print(f"   first interval with a step change, {first['i']}: dL2_step {first['dL2_step']}, terms " + ", ".join(f"{k} {[ip(fr(x)) for x in v]}" for k, v in first["terms"].items()))

if __name__ == "__main__":
    main(sys.argv)
