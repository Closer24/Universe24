"""The Link-record identity of the lay as the take reversed (H-Lay-As-The-Take-Reversed-2), read from a record's birth lines: per birth and per Link (the take's Node and each of its six neighbours j) the taken row's record change R_j = d before_j, the children's return sense A q_j, the unweighted identity R_j + sense A q_j (its magnitude below A where the division is exact to its remainder) and the weighted one num_taken R_j + num_children sense A q_j; the kit's balance dP_take + dP_lay_ends per axis; 2J about the board's centre and about the take's Node from the per-Link momenta (doubled coordinates); the far lays' levels and bits. Integers only. Usage: lt2_moment.py <record.json> [out.json]"""
import json
import sys

sys.set_int_max_str_digits(0)

AXES = 3


def unwrap(where, at, cube):
    out = []
    for w, a in zip(where, at, strict=True):
        d = (w - a) % cube
        d = d - cube if d > cube // 2 else d
        out.append(a + d)
    return out


def cross(u, v):
    return [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]]


def main(argv):
    record = json.load(open(argv[1]))
    cube = int(record["cube"]) if "cube" in record else int(record["world"]["shape"][0])
    rows = record["universe"]["rows"]
    nums = [int(r["pair"][0]) for r in rows if "pair" in r]
    births = [e for e in record["log"] if e["event"] == "birth" and "lay_far" in e]
    all_births = [e for e in record["log"] if e["event"] == "birth"]
    a_, b_ = (int(x) for x in all_births[0]["amplitude"]) if all_births else (0, 0)
    links_total = links_exact = links_below_a = 0
    weighted_exact = 0
    balance_births = 0
    j2_centre_zero = j2_node_zero = 0
    max_abs_unweighted = 0
    max_q = 0
    max_bits = 0
    ratio_num = []
    centre2 = [cube - 1] * AXES
    for e in births:
        at = e["node"]
        which = 0 if e["minus"] == at else 1
        sense = which + which - 1
        s = int(e["line_pair"])
        rec = int(e["taken_row"])
        num_s = nums[s] if s < len(nums) else None
        num_t = nums[rec] if rec < len(nums) else None
        ratio_num.append([num_t, num_s])
        p_links = []
        for where, r_j, q, rem_was, rest in e["lay_far"]:
            r_j, q = int(r_j), int(q)
            unweighted = r_j + sense * a_ * q
            weighted = (num_t or 0) * r_j + (num_s or 0) * sense * a_ * q
            links_total += 1
            links_exact += unweighted == 0
            links_below_a += abs(unweighted) < a_
            weighted_exact += weighted == 0
            max_abs_unweighted = max(max_abs_unweighted, abs(unweighted))
            max_q = max(max_q, abs(q))
            max_bits = max(max_bits, abs(q).bit_length(), abs(int(rest)).bit_length(), abs(r_j).bit_length())
            j_un = unwrap(where, at, cube)
            axis = [k for k in range(AXES) if j_un[k] != at[k]][0]
            side = 1 if j_un[axis] > at[axis] else -1
            p_take = [0] * AXES
            p_lay = [0] * AXES
            p_take[axis] = -side * 2 * (num_t or 0) * r_j
            p_lay[axis] = -side * 2 * (num_s or 0) * sense * a_ * q
            mid2 = [at[k] + j_un[k] for k in range(AXES)]
            p_links.append((mid2, p_take, p_lay))
        take = [int(x) for x in e["dP_take"]]
        ends = e["dP_lay_ends"]
        bal = [take[k] + int(ends[0][k]) + int(ends[1][k]) for k in range(AXES)]
        balance_births += bal == [0] * AXES
        j_c = [0] * AXES
        j_n = [0] * AXES
        for mid2, p_take, p_lay in p_links:
            arm_c = [m - c for m, c in zip(mid2, centre2, strict=True)]
            arm_n = [m - 2 * x for m, x in zip(mid2, at, strict=True)]
            p = [x + y for x, y in zip(p_take, p_lay, strict=True)]
            j_c = [x + y for x, y in zip(j_c, cross(arm_c, p), strict=True)]
            j_n = [x + y for x, y in zip(j_n, cross(arm_n, p), strict=True)]
        j2_centre_zero += j_c == [0] * AXES
        j2_node_zero += j_n == [0] * AXES
    found = {
        "record": argv[1],
        "births": len(all_births),
        "births with the far lay": len(births),
        "A, B": [a_, b_],
        "links read": links_total,
        "links with R_j + sense A q_j = 0 (the unweighted identity exact)": links_exact,
        "links with |R_j + sense A q_j| < A (exact to the division's remainder)": links_below_a,
        "max |R_j + sense A q_j|": max_abs_unweighted,
        "links with num_taken R_j + num_children sense A q_j = 0 (the weighted identity)": weighted_exact,
        "births with the kit's balance dP_take + dP_lay_ends = 0": balance_births,
        "births with 2J about the centre 0 from the per-Link momenta (weighted)": j2_centre_zero,
        "births with 2J about the take's Node 0 from the per-Link momenta (weighted)": j2_node_zero,
        "max |q_j| (the far lay's levels)": max_q,
        "max bits among q, rest, R_j": max_bits,
        "num taken, num children (first birth)": ratio_num[0] if ratio_num else None,
    }
    print(json.dumps(found))
    if len(argv) > 2:
        json.dump(found, open(argv[2], "w"), indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
