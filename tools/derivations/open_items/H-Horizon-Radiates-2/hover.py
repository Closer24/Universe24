"""hr2: the hover at every Node that ever froze, from a streamed record: per release (a frozen line followed by an unfrozen one) the X at the freeze, the velocity at the first unfrozen interval (X_next - X_frozen, the reflection), the second difference of X per interval while unfrozen (the net push: the write's q with the Link term and the mass term, in X-levels per interval squared), the intervals to the next freeze, the content's minimum between; the per-Node summary: releases, the mean gap (integer quotient and remainder), the min content reached, the largest |second difference| and its mean while unfrozen, the number of intervals the Node was within 1 content of the horizon. Integers only. Usage: hover.py <stream.jsonl> [max nodes]"""
import json, sys
sys.set_int_max_str_digits(0)
ls = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
maxn = int(sys.argv[2]) if len(sys.argv) > 2 else 6
ever = []
for l in ls:
    for k in l["frozen"]:
        if k not in ever: ever.append(k)
fc = 3793
for k in ever[:maxn]:
    f0 = next(j for j, l in enumerate(ls) if k in l["frozen"])
    seq = ls[f0:]
    xs = [l["X_ever"][str(k)] for l in seq]; cs = [l["content_ever"][str(k)] for l in seq]; fz = [k in l["frozen"] for l in seq]
    vel = [xs[j + 1] - xs[j] for j in range(len(xs) - 1)]
    acc = [vel[j + 1] - vel[j] for j in range(len(vel) - 1)]
    rels = [j for j in range(len(fz) - 1) if fz[j] and not fz[j + 1]]
    gaps = []
    for j in rels:
        nxt = next((m for m in range(j + 1, len(fz)) if fz[m]), None)
        gaps.append((nxt - j) if nxt is not None else None)
    acc_unfrozen = [a for j, a in enumerate(acc) if not fz[j] and not fz[j + 1] and not fz[j + 2]]
    near = sum(1 for c in cs if c >= fc - 1)
    g = [x for x in gaps if x is not None]
    print("node", k, "first freeze i", seq[0]["i"], "lines", len(seq), "frozen", sum(fz), "releases", len(rels), "gaps mean", (sum(g) // len(g), sum(g) % len(g), len(g)) if g else None, "gap max", max(g, default=None), "content min", min(cs), "within 1 of horizon", near, "of", len(cs))
    print("   first release: X frozen", xs[rels[0]] if rels else None, "X next", xs[rels[0] + 1] if rels else None, "v after", vel[rels[0]] if rels else None, "contents after", cs[rels[0]:rels[0] + 8] if rels else None)
    if acc_unfrozen:
        print("   second difference while unfrozen: max |a|", max(abs(a) for a in acc_unfrozen), "sum", sum(acc_unfrozen), "count", len(acc_unfrozen), "mean", sum(acc_unfrozen) // len(acc_unfrozen), "first 8", acc_unfrozen[:8])
    print("   X at the freezes (first 6)", [xs[j] for j in range(len(xs)) if fz[j]][:6], "velocity before each freeze (first 6)", [vel[j - 1] for j in range(1, len(xs)) if fz[j]][:6])
