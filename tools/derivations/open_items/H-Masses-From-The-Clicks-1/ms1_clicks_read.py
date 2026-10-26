"""ms1: what a far reader has from the credit lines alone (integers only): per plane, the credits, the senses, the beats (intervals per period), the decoded point's middle (the decoder's solve, a rational), the leg of the middle point and the legs' ratios per 10^9 against the file's legs; per birth, the two children's W and |W| per plane (the charge in the clicks).
Usage: python ms1_clicks_read.py <record.json>"""
import json
import sys
from collections import Counter, defaultdict
from functools import cmp_to_key

sys.set_int_max_str_digits(0)

from event_universe import decoder as D  # noqa: E402
from event_universe.core.paces import sine_den  # noqa: E402
from event_universe.core.rule3 import largest_below  # noqa: E402

G9 = 10**9


def leg_ratio(x1, x0):
    """sqrt((D1^2 - N1^2) D0^2 / ((D0^2 - N0^2) D1^2)) per 10^9 by one search, no root on a float."""
    (n1, d1), (n0, d0) = x1, x0
    num = (d1 * d1 - n1 * n1) * d0 * d0 * G9 * G9
    den = (d0 * d0 - n0 * n0) * d1 * d1
    return largest_below(num // den) if den else None


def main():
    run = json.load(open(sys.argv[1]))
    rec = D.Record(run)
    out = {"record": sys.argv[1], "planes (num)": rec.line_num, "den": rec.den}
    births = defaultdict(list)
    for b in rec.births:
        births[b["line_pair"]].append(tuple(b["W_children"]))
    out["births per plane: count, |W| of the children (distinct), W summed"] = {
        str(k): [len(v), sorted({abs(w) for pair in v for w in pair}), sum(w for pair in v for w in pair)]
        for k, v in sorted(births.items())
    }
    all_w = sorted({abs(w) for v in births.values() for pair in v for w in pair})
    out["|W| over every child of every plane (distinct values)"] = all_w
    if len(all_w) > 1:
        out["|W| largest over least per 1e9"] = all_w[-1] * G9 // all_w[0]
    decoded, right, within, floors = D.decoded_credits(rec)
    per = defaultdict(list)
    for c, name, x in decoded:
        per[c["line"]].append(x)
    credits = defaultdict(list)
    for c in rec.credits:
        credits[c["line"]].append(c)
    table = {}
    mids = {}
    for line in sorted(credits):
        cs = credits[line]
        xs = sorted(per[line], key=cmp_to_key(D.cmp_rat))
        mid = D.middle(xs) if xs else None
        mids[line] = mid
        num = rec.line_num[line]
        table[str(line)] = {
            "credits": len(cs),
            "senses": dict(Counter(c["sense"] for c in cs)),
            "beats (intervals per period: count)": dict(sorted(Counter(c["beat"] for c in cs).items())),
            "decoded middle x per 1e9": (mid[0] * G9 // mid[1]) if mid else None,
            "file's num/den per 1e9": num * G9 // rec.den,
            "file's leg per 1e9": sine_den(num, rec.den) * G9 // rec.den,
            "decoded right": sum(1 for c, n, x in decoded if c["line"] == line and n == rec.NAMES[num][0]),
        }
    out["credits per plane"] = table
    lines = [k for k in sorted(mids) if mids[k] is not None]
    if len(lines) >= 2:
        base = lines[0]
        out["legs' ratios from the decoded middles per 1e9 (plane k over plane %d)" % base] = {
            str(k): leg_ratio(mids[k], mids[base]) for k in lines[1:]
        }
        out["legs' ratios from the file per 1e9"] = {
            str(k): sine_den(rec.line_num[k], rec.den) * G9 // sine_den(rec.line_num[base], rec.den)
            for k in lines[1:]
        }
    print(json.dumps(out))


if __name__ == "__main__":
    main()
