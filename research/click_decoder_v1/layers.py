"""Click-log -> click-log transforms that make a separate observer layer (decoder v1.1).

Both read only ``step``, ``address``, ``kind`` and ``quotient`` of the input records. Their output
is a click log in the same record form, decoded as its own layer and never merged with others.

* ``diff(a, b)``: records of log A whose (step, address) is absent from log B. With A the change
  observer and B the native log it gives r08's l = 0 ("dark-clock") layer.
* ``quotient_field(events, side, window, centre, r_range)``: r24's ``quotient_field_v1``: per site the
  signed sum of quotients over a declared window; Qbar = sum / (48 T) with T the window length; with
  a declared centre, the profile over Euclidean shells (rounded radius; empty sites count in each
  shell's population) and a least-squares fit a/r + c. The output is a field, not a click log.
* ``peak_arrival(events, w, window)``: r14's ``peak_arrival_click_v1`` (spec: r14/REPORT_WAVE2.md
  section 1; reference implementation ``PeakArrival`` in r14/peak_arrival.py). Per site
  Q_s(t) = sum of |quotient| at (site, t); a candidate is a step with Q_s(t) > 0, t + w <= the last
  step, and Q_s(t) >= Q_s(t') for every t' in [t - w, t + w] (inside the window); the site's event
  is the largest candidate, the earliest on ties. The record carries the channel with the largest
  |q| (smallest g on ties), that click's kind and quotient, ``weight`` = Q_s(t*) and ``observer``.
"""
from __future__ import annotations

from collections import Counter, defaultdict
import json
import math
from pathlib import Path

PEAK = "peak_arrival_click_v1"
FIELD = "quotient_field_v1"


def _records(path):
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.strip():
            yield line, json.loads(line)


def diff(a, b, out):
    """Write the records of log ``a`` whose (step, address) is not in log ``b``; returns their number."""
    keys = {(d["step"], tuple(d["address"])) for _, d in _records(b)}
    kept = 0
    with Path(out).open("x", encoding="utf-8") as fh:
        for line, d in _records(a):
            if (d["step"], tuple(d["address"])) not in keys:
                fh.write(line + "\n")
                kept += 1
    return kept


def peak_arrival(events, w=8, window=None):
    """events: (t, x, y, z, g, kind, quotient) tuples. Returns the peak-arrival records, sorted."""
    Q, best = defaultdict(dict), defaultdict(dict)
    t_first = t_last = None
    for t, x, y, z, g, k, q in events:
        if window and not window[0] <= t <= window[1]:
            continue
        s = (x, y, z)
        Q[s][t] = Q[s].get(t, 0) + abs(q)
        cand = (abs(q), -g, k, q, g)
        if t not in best[s] or cand[:2] > best[s][t][:2]:
            best[s][t] = cand
        t_first = t if t_first is None else min(t_first, t)
        t_last = t if t_last is None else max(t_last, t)
    if t_last is None:
        return []
    lo_all, hi_all = (window[0], window[1]) if window else (t_first, t_last)
    out = []
    for s, series in Q.items():
        top = None
        for t, v in series.items():
            if t + w > hi_all:
                continue
            if all(series.get(u, 0) <= v for u in range(max(lo_all, t - w), t + w + 1)):
                if top is None or v > top[1] or (v == top[1] and t < top[0]):
                    top = (t, v)
        if top is not None:
            t, v = top
            _, _, k, q, g = best[s][t]
            out.append({"step": t, "address": [*s, g], "kind": k, "quotient": q, "weight": v, "observer": PEAK})
    out.sort(key=lambda e: (e["step"], e["address"]))
    return out


def write_peak_arrival(events, out, w=8, window=None):
    recs = peak_arrival(events, w, window)
    with Path(out).open("x", encoding="utf-8") as fh:
        for r in recs:
            fh.write(json.dumps(r, separators=(",", ":")) + "\n")
    return len(recs)


def _mi(d, L):
    d %= L
    return min(d, L - d)


def quotient_field(events, side, window=None, centre=None, r_range=None):
    """r24's quotient_field_v1 on click events; window = [t0, t1] (default [1, last step])."""
    last = max((e[0] for e in events), default=0)
    t0, t1 = window or (1, last)
    T = t1 - t0 + 1
    qsum = defaultdict(int)
    for t, x, y, z, g, k, q in events:
        if t0 <= t <= t1:
            qsum[(x, y, z)] += q
    out = {"observer": FIELD, "window": [t0, t1], "sites": len(qsum), "total": sum(qsum.values()),
           "sum": {"%d,%d,%d" % s: v for s, v in sorted(qsum.items())}}
    if centre is None:
        return out
    L = side

    def rad(s):
        return int(round(math.sqrt(sum(_mi(s[i] - centre[i], L) ** 2 for i in range(3)))))
    shells, pop = defaultdict(float), Counter()
    for s, v in qsum.items():
        shells[rad(s)] += v / (48 * T)
    for x in range(L):
        for y in range(L):
            for z in range(L):
                pop[rad((x, y, z))] += 1
    prof = {r: shells.get(r, 0.0) / pop[r] for r in sorted(pop)}
    out["centre"] = list(centre)
    out["profile_Qbar"] = {str(r): v for r, v in prof.items()}
    lo, hi = r_range or (1, L // 2)
    pts = [(1 / r, v) for r, v in prof.items() if lo <= r <= hi and r > 0]
    if len(pts) >= 3:
        n = len(pts)
        sx, sy = sum(p[0] for p in pts), sum(p[1] for p in pts)
        sxx, sxy = sum(p[0] ** 2 for p in pts), sum(p[0] * p[1] for p in pts)
        den = n * sxx - sx * sx
        if den:
            a = (n * sxy - sx * sy) / den
            c = (sy - a * sx) / n
            rms = math.sqrt(sum((v - a * x - c) ** 2 for x, v in pts) / n)
            out["fit_a_over_r_plus_c"] = {"a": a, "c": c, "rms": rms, "r_range": [lo, hi], "shells": n}
    return out
