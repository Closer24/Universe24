"""hr2: the hover over every Node that ever froze, in aggregate, from a streamed record: the releases, the gaps to the next freeze (their distribution: 1, 2 to 10, 11 to 50, 51 to 200, over 200; the max), the intervals every ever-frozen Node spent within one content of the horizon against below it (after its first freeze), the minimum content any released Node reached and where, the largest X at any freeze against fr1's bound 2 X_f + q (X_f the horizon's level 4,268,834,097), the velocity at the first release (its min, max over Nodes) and the write's push (the second difference of X at the first unfrozen interval after the first release, min and max over Nodes), the number of Nodes frozen at the last interval. Integers only. Usage: hover_all.py <stream.jsonl>"""
import json, sys
sys.set_int_max_str_digits(0)
ls = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
XF = 4268834097
ever = []
for l in ls:
    for k in l["frozen"]:
        if k not in ever: ever.append(k)
gaps = {"1": 0, "2-10": 0, "11-50": 0, "51-200": 0, ">200": 0}
gmax, within, below, releases, cmin, cmin_at, xmax, xmax_at = 0, 0, 0, 0, 10**9, None, 0, None
v_first, q_first = [], []
for k in ever:
    f0 = next(j for j, l in enumerate(ls) if k in l["frozen"])
    seq = ls[f0:]
    xs = [l["X_ever"][str(k)] for l in seq]; cs = [l["content_ever"][str(k)] for l in seq]; fz = [k in l["frozen"] for l in seq]
    for j in range(len(fz) - 1):
        if fz[j] and not fz[j + 1]:
            releases += 1
            nxt = next((m for m in range(j + 1, len(fz)) if fz[m]), None)
            if nxt is not None:
                g = nxt - j; gmax = max(gmax, g)
                gaps["1" if g == 1 else "2-10" if g <= 10 else "11-50" if g <= 50 else "51-200" if g <= 200 else ">200"] += 1
    within += sum(1 for c in cs if c >= 3792); below += sum(1 for c in cs if c < 3792)
    m = min(cs)
    if m < cmin: cmin, cmin_at = m, (k, seq[cs.index(m)]["i"])
    for j in range(len(xs)):
        if fz[j] and xs[j] > xmax: xmax, xmax_at = xs[j], (k, seq[j]["i"])
    r0 = next((j for j in range(len(fz) - 1) if fz[j] and not fz[j + 1]), None)
    if r0 is not None and r0 + 3 < len(xs):
        v_first.append(xs[r0 + 1] - xs[r0]); q_first.append(xs[r0 + 3] - 2 * xs[r0 + 2] + xs[r0 + 1])
print(json.dumps({"intervals": ls[-1]["i"], "ever frozen": len(ever), "releases": releases, "gaps": gaps, "gap max": gmax, "intervals within one content of the horizon (content >= 3792) after first freeze": within, "below": below, "min content of a released Node": cmin, "at (node, i)": cmin_at, "max X at a freeze": xmax, "at": xmax_at, "fr1 bound 2 X_f": 2 * XF, "velocity at first release min/max": [min(v_first), max(v_first)] if v_first else None, "write push at first release (second difference) min/max": [min(q_first), max(q_first)] if q_first else None, "frozen at the last interval": len(ls[-1]["frozen"]), "frozen count per interval max": max(len(l["frozen"]) for l in ls)}))
