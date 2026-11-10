"""Joint click statistics between declared detector regions (read only from click events).

A detector declaration (JSON) names regions of the board; it is part of the experiment,
not of the decoder, and must be fixed before the run::

    {"detectors": {"A": {"box": [[x0, x1], [y0, y1], [z0, z1]]},
                   "B": {"sites": [[x, y, z], ...], "channels": [0, 14], "kinds": [1, 2]}},
     "bin": 1, "window": [t0, t1], "max_lag": 8,
     "pairs": [["A", "B"]],
     "sides": {"left": ["A+", "A-"], "right": ["B+", "B-"]}}

``box`` bounds are inclusive and taken modulo the side. ``channels`` and ``kinds``
optionally restrict which clicks count. Per time bin a detector "fires" if it has at
least one counted click. For a pair, a = +1 when A fires and -1 otherwise (same for b);
E = <a b>. For ``sides`` (two detectors per side) the outcome of a bin is +1 if only
the first fires, -1 if only the second fires, and undefined otherwise; E is taken over
bins where both sides have an outcome. ``chsh`` combines four E values from four runs.
"""
from __future__ import annotations

from collections import Counter


def _member(det, side):
    sites = {tuple(s) for s in det.get("sites", [])}
    box = det.get("box")
    chans = set(det["channels"]) if det.get("channels") is not None else None
    kinds = set(det["kinds"]) if det.get("kinds") is not None else None

    def inside(e):
        s = e[1:4]
        if sites and s not in sites:
            return False
        if box and not all(box[k][0] <= s[k] <= box[k][1] for k in range(3)):
            return False
        return (chans is None or e[4] in chans) and (kinds is None or e[5] in kinds)
    return inside


def correlations(events, spec, horizon, side):
    dets = spec["detectors"]
    binw = int(spec.get("bin", 1))
    t0, t1 = spec.get("window", [1, horizon])
    nb = (t1 - t0) // binw + 1
    fired, counts, kinds, first = {}, {}, {}, {}
    for name, det in sorted(dets.items()):
        inside = _member(det, side)
        sel = [e for e in events if t0 <= e[0] <= t1 and inside(e)]
        fired[name] = sorted({(e[0] - t0) // binw for e in sel})
        counts[name] = len(sel)
        kinds[name] = dict(sorted(Counter(f"C{e[5]}" for e in sel).items()))
        first[name] = min((e[0] for e in sel), default=None)
    out = {"bins": nb, "bin": binw, "window": [t0, t1],
           "detectors": {k: {"clicks": counts[k], "bins_fired": len(fired[k]), "first_click": first[k],
                             "kinds": kinds[k], "rate": round(len(fired[k]) / nb, 6)} for k in sorted(dets)},
           "pairs": [], "sides": None}
    lag = int(spec.get("max_lag", 0))
    for a, b in spec.get("pairs", []):
        A, B = set(fired[a]), set(fired[b])
        n11 = len(A & B)
        n10, n01 = len(A) - n11, len(B) - n11
        n00 = nb - n11 - n10 - n01
        E = (n11 + n00 - n10 - n01) / nb
        pa, pb = len(A) / nb, len(B) / nb
        cov = n11 / nb - pa * pb
        den = (pa * (1 - pa) * pb * (1 - pb)) ** 0.5
        cross = {str(k): len({x + k for x in A} & B) for k in range(-lag, lag + 1)}
        out["pairs"].append({"pair": [a, b], "n11": n11, "n10": n10, "n01": n01, "n00": n00,
                             "E": round(E, 6), "covariance": round(cov, 6),
                             "pearson": round(cov / den, 6) if den else None, "coincidences_by_lag": cross})
    sides = spec.get("sides")
    if sides:
        (ln, (lp, lm)), (rn, (rp, rm)) = sorted(sides.items())

        def outcome(p, m, k):
            fp, fm = k in set(fired[p]), k in set(fired[m])
            return 1 if fp and not fm else (-1 if fm and not fp else 0)
        prod = [outcome(lp, lm, k) * outcome(rp, rm, k) for k in range(nb)]
        defined = [x for x in prod if x]
        out["sides"] = {"sides": [ln, rn], "trials": len(defined), "same": prod.count(1), "different": prod.count(-1),
                        "E": round(sum(defined) / len(defined), 6) if defined else None}
    return out


def chsh(e_ab, e_abp, e_apb, e_apbp):
    """S = E(a,b) - E(a,b') + E(a',b) + E(a',b'). |S| <= 2 for local responses with
    setting-independent preparation weights; the quantum bound is 2*sqrt(2)."""
    return e_ab - e_abp + e_apb + e_apbp
