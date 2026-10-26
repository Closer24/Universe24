"""cm1's reader of a record's birth lines: per birth the P balance dP_take + dP_lay (0 where the children carry the recoil), its part along the pair's Link and transverse, the J2 balance about the centre in doubled coordinates (2 r_at x dP_take + SUM_end 2 r_end x dP_lay_end, the per-end booking), the pair's relative L2 about its midpoint (d x (p_plus - p_minus)), the children's Q, the fixed point reached, W summing 0, the widest integer in bits; summed over the record. Usage: cm1_moment.py <record.json>"""
import json
import sys

sys.set_int_max_str_digits(0)


def cross(u, v):
    return [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]]


def add(u, v):
    return [a + b for a, b in zip(u, v, strict=True)]


def dipole(minus, plus, cube):
    d = [(p - m) % cube for p, m in zip(plus, minus, strict=True)]
    return [x - cube if x > cube // 2 else x for x in d]


def read(record):
    log = record["log"]
    cube = int(record["cube"])
    c2 = [cube - 1] * 3
    z = [0, 0, 0]
    n = {"births": 0, "mergers": 0, "P balance 0": 0, "P balance 0 along the Link": 0, "P along the Link within half the lay's quantum 4 num A": 0,
         "transverse recoil carried": 0, "J2 balance 0": 0, "J2 balance 0 where at is the + end": 0, "taker at the + end": 0,
         "relative L2 0": 0, "fixed point reached": 0, "Q 0": 0, "W summing 0": 0, "dP_lay_ends present": 0}
    P_take, P_lay, J_take, J_lay, L_rel = list(z), list(z), list(z), list(z), list(z)
    worst_p, worst_j, bits, qs = 0, 0, 0, []
    for e in log:
        if e.get("event") != "birth":
            continue
        if "takes" in e:
            n["mergers"] += 1
            continue
        n["births"] += 1
        at, minus, plus = e["node"], e["minus"], e["plus"]
        dpt = [int(x) for x in e["dP_take"]]
        dpl = [int(x) for x in e["dP_lay"]]
        ends = e.get("dP_lay_ends")
        if ends is None:
            ends = [z, dpl]
        else:
            n["dP_lay_ends present"] += 1
        ends = [[int(x) for x in v] for v in ends]
        d = dipole(minus, plus, cube)
        ax = [a for a in range(3) if d[a] != 0][0]
        bal = add(dpt, dpl)
        n["P balance 0"] += bal == z
        n["P balance 0 along the Link"] += bal[ax] == 0
        n["transverse recoil carried"] += all(bal[b] == 0 for b in range(3) if b != ax) and any(dpt[b] != 0 for b in range(3) if b != ax)
        q = int(e.get("cm1_q", [0, 0])[1])
        c_ax = dpl[ax] // q if q else 0
        n["P along the Link within half the lay's quantum 4 num A"] += q != 0 and abs(bal[ax]) + abs(bal[ax]) <= abs(c_ax)
        r_at = [2 * x - c for x, c in zip(at, c2, strict=True)]
        jt = cross(r_at, dpt)
        jl = list(z)
        for where, p in zip((minus, plus), ends, strict=True):
            jl = add(jl, cross([2 * x - c for x, c in zip(where, c2, strict=True)], p))
        jb = add(jt, jl)
        n["J2 balance 0"] += jb == z
        n["taker at the + end"] += list(at) == list(plus)
        n["J2 balance 0 where at is the + end"] += jb == z and list(at) == list(plus)
        lr = cross(d, [a - b for a, b in zip(ends[1], ends[0], strict=True)])
        n["relative L2 0"] += lr == z
        n["fixed point reached"] += bool(e.get("cm1_fixed"))
        qs.append(q)
        n["Q 0"] += q == 0
        n["W summing 0"] += sum(int(w) for w in e["W_children"]) == 0
        P_take, P_lay, J_take, J_lay, L_rel = add(P_take, dpt), add(P_lay, dpl), add(J_take, jt), add(J_lay, jl), add(L_rel, lr)
        worst_p = max(worst_p, max(abs(x) for x in bal))
        worst_j = max(worst_j, max(abs(x) for x in jb))
        for v in dpt + dpl + [int(e["taken"]), int(e["booked"]), int(e["room"])] + [q]:
            bits = max(bits, abs(int(v)).bit_length())
    return {"counts": n, "P take summed": P_take, "P lay summed": P_lay, "P balance summed": add(P_take, P_lay),
            "J2 take summed": J_take, "J2 lay summed": J_lay, "J2 balance summed": add(J_take, J_lay), "relative L2 summed": L_rel,
            "worst |P balance| at a birth": worst_p, "worst |J2 balance| at a birth": worst_j, "Q min max": [min(qs), max(qs)] if qs else None,
            "bits (log integers)": bits}


if __name__ == "__main__":
    rec = json.load(open(sys.argv[1]))
    found = read(rec)
    found["record"] = sys.argv[1].split("/")[-1]
    found["counts_record"] = rec.get("counts")
    found["run_back"] = rec.get("run_back")
    print(json.dumps(found, indent=1, default=str))
