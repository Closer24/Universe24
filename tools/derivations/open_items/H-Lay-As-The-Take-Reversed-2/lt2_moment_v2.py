"""The Link-record identity of the lay as the take reversed, the mended form (v2, one carried division per far Node per close), read from a record's birth lines: per close the births' reads far_records (the six Link records R_j and numerators per birth) and the one write per Node lay_far on the close's last birth line (s, j, total, q, remainder before, remainder after); per far Node the exact sum S_j = SUM over the close's births of -sense R_j and the identity |A q_j - S_j| < A; per close the momentum balance SUM dP_take + SUM dP_lay_ends + dP_far per axis (num-weighted, the kit's quantities) and its residual; 2J about the take's Nodes from the per-Link momenta where one birth owns the Node. Integers only. Usage: lt2_moment_v2.py <record.json> [out.json]"""
import json
import sys

sys.set_int_max_str_digits(0)

AXES = 3


def main(argv):
    record = json.load(open(argv[1]))
    nums = [int(r["pair"][0]) for r in record["universe"]["rows"] if "pair" in r]
    births = [e for e in record["log"] if e["event"] == "birth"]
    a_ = int(births[0]["amplitude"][0]) if births else 0
    by_close = {}
    for e in births:
        by_close.setdefault(int(e["i"]), []).append(e)
    nodes_written = nodes_exact = nodes_below_a = 0
    max_abs = 0
    closes = closes_balanced = 0
    max_residual = 0
    births_far = 0
    max_q = max_bits = 0
    shared = 0
    weighted_equal_num = 0
    for i in sorted(by_close):
        entries = by_close[i]
        sums = {}
        owners = {}
        for e in entries:
            if "far_records" not in e:
                continue
            births_far += 1
            s = int(e["line_pair"])
            sense = -1 if e["minus"] == e["node"] else 1
            for where, r_j, _total in e["far_records"]:
                key = (s, tuple(where))
                sums[key] = sums.get(key, 0) - sense * int(r_j)
                owners[key] = owners.get(key, 0) + 1
        far = []
        for e in entries:
            far += e.get("lay_far", [])
        for s, where, _total, q, _rem_was, rest in far:
            key = (s, tuple(where))
            q = int(q)
            residual = a_ * q - sums.get(key, 0)
            nodes_written += 1
            nodes_exact += residual == 0
            nodes_below_a += abs(residual) < a_
            max_abs = max(max_abs, abs(residual))
            max_q = max(max_q, abs(q))
            max_bits = max(max_bits, abs(q).bit_length(), abs(int(rest)).bit_length())
            shared += owners.get(key, 0) > 1
        if far:
            closes += 1
            bal = [0] * AXES
            for e in entries:
                take = [int(x) for x in e["dP_take"]]
                ends = e["dP_lay_ends"]
                for k in range(AXES):
                    bal[k] += take[k] + int(ends[0][k]) + int(ends[1][k])
                for k in range(AXES):
                    bal[k] += int(e.get("dP_far", [0, 0, 0])[k])
            closes_balanced += bal == [0] * AXES
            max_residual = max(max_residual, max(abs(x) for x in bal))
        for e in entries:
            if "far_records" in e:
                weighted_equal_num += nums[int(e["taken_row"])] == nums[int(e["line_pair"])]
    found = {
        "record": argv[1],
        "births": len(births),
        "births with the far reads": births_far,
        "births whose taken row and children's record share one num": weighted_equal_num,
        "A": a_,
        "far Nodes written (one carried division each)": nodes_written,
        "far Nodes shared by two or more births of one close": shared,
        "far Nodes with A q_j = S_j (exact)": nodes_exact,
        "far Nodes with |A q_j - S_j| < A (exact to the remainder)": nodes_below_a,
        "max |A q_j - S_j|": max_abs,
        "closes with the far lay": closes,
        "closes with SUM dP_take + SUM dP_lay_ends + dP_far = 0 (num-weighted)": closes_balanced,
        "max |residual| of that balance": max_residual,
        "max |q_j|": max_q,
        "max bits among q and the remainders": max_bits,
    }
    print(json.dumps(found))
    if len(argv) > 2:
        json.dump(found, open(argv[2], "w"), indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
