"""B1-GAUGE demos D1-D3 (pre-registered in NOTES_gauge.md 09:34:28 UTC). Exact integers; floats only in the report.

Run from the repository root:
    OMP_NUM_THREADS=2 nice -n 10 python -m research.metric_variant_v1.demos.gauge.run_demos
Writes demos/gauge/D1.json, D2.json, D3.json.
"""
from __future__ import annotations

import json
import random
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from ...core.engine import Engine, State
from ...core.lattice import lattice
from ...core.tensor import compose
from ...layers.gauge import ALGEBRAS, build_gauge
from ...observe.gauge import GaugeView
from ...prepare import vacuum_state
from ...prepare.gauge import set_link, set_matter

HERE = Path(__file__).resolve().parent
QF = (1 << 25) + 1            # fine demo regime: A = 4096, kappa*A = (Q-1)/2


def stamp():
    return datetime.now(timezone.utc).strftime("%a %b %d %H:%M:%S UTC %Y")


def fine(group, lam=1, use_P=False):
    D = 6 * QF
    return build_gauge(group=group, Q=QF, A=4096, kappa=(QF - 1) // (2 * 4096), mass=QF + 3, lam=lam, use_P=use_P,
                       kappa_P=256 if use_P else 0, c_P=0, beta=(D - (1 << 25)) if use_P else 0, name=group)


def matter_vec(V, s, node, field="b"):
    return [int(getattr(s, field)[i, node]) for i in V.matter]


def isospin_at(V, s, node):
    """Matter-only isospin/colour charges at one node (exact ints), one per generator."""
    out = []
    for _, X in V.alg.generators:
        out.append(int(V.charge(s, X, "matter")[node]))
    return out


# ------------------------------------------------------------------------------------------------ D3 witness
def d3_witness():
    res = {}
    L = 4
    Apsi = 1 << 16
    x0 = (1, 1, 1)
    for group in ("su2", "u1"):
        blk = fine(group)
        T = compose(blk)
        E = Engine(T, blk.Q)
        V = GaugeView(T, blk.params, blk.name)
        A = blk.params["A"]
        alg = V.alg
        lat = lattice(L)
        if group == "su2":
            first, second = (0, A, 0, 0), (0, 0, A, 0)          # A*i, A*j
        else:
            first, second = (0, A), (-A, 0)                       # A*i, A*(-1): commuting
        configs = {"same_order": (first, second), "swapped_order": (second, first)}
        for cname, (c, d) in configs.items():
            s = vacuum_state(T, blk.Q, L, blk)
            ex = (x0[0] + 1, x0[1], x0[2])
            ey = (x0[0], x0[1] + 1, x0[2])
            s = set_link(s, T, blk, x0, 0, (first, first))       # path A: x then y
            s = set_link(s, T, blk, ex, 1, (second, second))
            s = set_link(s, T, blk, x0, 1, (c, c))               # path B: y then x
            s = set_link(s, T, blk, ey, 0, (d, d))
            psi0 = [0] * alg.n
            psi0[0] = Apsi
            s = set_matter(s, T, blk, x0, [0] * alg.n, psi0)
            h = E.run(s, 2, history=True)
            far = lat.index(x0[0] + 1, x0[1] + 1, x0[2])
            vec = matter_vec(V, h[2], far)
            res[f"{group}:{cname}"] = {"far_corner_b(t=2)": vec, "max_abs": max(abs(v) for v in vec),
                                       "wilson_xy_at_x0": int(V.wilson(h[0], 0, 1)[lat.index(*x0)])}
    s_same = res["su2:same_order"]["max_abs"]
    s_swap = res["su2:swapped_order"]["max_abs"]
    res["verdict"] = {"su2_same_over_swapped": (s_same / max(1, s_swap)),
                      "u1_same_equals_swapped": res["u1:same_order"]["far_corner_b(t=2)"] ==
                      res["u1:swapped_order"]["far_corner_b(t=2)"],
                      "PASS": s_swap <= 2 and s_same >= 100 * max(1, s_swap) and res["u1:swapped_order"]["max_abs"] > 0}
    res["note"] = ("same link multiset on the plaquette; only the ORDER along path B differs. SU(2): (j i + i j) = 0 -> "
                   "the two paths cancel at the far corner; U(1) phases commute, swapping changes nothing. "
                   "Wilson loop (gauge-invariant integer) shown for each configuration.")
    return res


# ------------------------------------------------------------------------------------------------ D1 isospin
def d1_isospin():
    res = {}
    L = 4
    blk = fine("su2")
    T = compose(blk)
    E = Engine(T, blk.Q)
    V = GaugeView(T, blk.params, blk.name)
    A = blk.params["A"]
    lat = lattice(L)
    # (a) transport through one link: vacuum link vs a 90-degree isospin rotation q ~ A (1 + k)/sqrt2
    c = 2896                                   # 2896^2 * 2 = 16773632 ~ 4096^2 = 16777216
    x0 = (1, 1, 1)
    x1 = (2, 1, 1)
    Apsi = 1 << 14
    out = {}
    for name, q in (("vacuum_link", (A, 0, 0, 0)), ("rotated_link", (c, 0, 0, c))):
        s = vacuum_state(T, blk.Q, L, blk)
        s = set_link(s, T, blk, x0, 0, (q, q))
        s = set_matter(s, T, blk, x0, [Apsi, 0, 0, 0], [0, Apsi, 0, 0])     # (a, b) = Apsi (1, i): isospin along i
        h = E.run(s, 2, history=True)
        out[name] = {"isospin_x0_t0": isospin_at(V, h[0], lat.index(*x0)),
                     "isospin_x1_t2": isospin_at(V, h[2], lat.index(*x1))}
    v0 = np.array(out["vacuum_link"]["isospin_x1_t2"], dtype=float)
    v1 = np.array(out["rotated_link"]["isospin_x1_t2"], dtype=float)
    cosang = float(v0 @ v1 / (np.linalg.norm(v0) * np.linalg.norm(v1)))
    cross = np.cross(v0, v1)
    res["a_transport"] = {**out, "cos_angle_between_arrivals": cosang,
                          "rotation_axis": (cross / np.linalg.norm(cross)).tolist(),
                          "note": "the link q = (2896,0,0,2896) ~ A exp(k pi/4) rotates the transported isospin "
                                  "vector by 90 degrees about the 3-axis (cos -> 0, axis +-e3)"}
    # (b) exchange: two packets with orthogonal isospin, dynamical links, total exact
    rng = random.Random(1)
    s = vacuum_state(T, blk.Q, L, blk)
    a = s.a.astype(object)
    b = s.b.astype(object)
    Ap = 2000
    for n in range(lat.N):
        x, y, z = lat.coords(n)
        w = 1.0 if x == 0 else (0.5 if x in (1, L - 1) else 0.0)
        if w:      # packet 1 near x = 0: isospin along i : (a, b) ~ (1, i)
            amp = int(Ap * w)
            a[V.matter[0], n], b[V.matter[1], n] = amp, amp
        w2 = 1.0 if x == 2 else 0.0
        if w2:     # packet 2 at x = 2: isospin along j : (a, b) ~ (1, j)
            a[V.matter[0], n], b[V.matter[2], n] = Ap, Ap
    s = State(L, a, b, s.r)
    hist = E.run(s, 60, history=True)
    rows = []
    gens = V.alg.generators
    for t in range(1, len(hist), 5):
        st = hist[t]
        row = {"t": t}
        for side, xs in (("left", (0, 1)), ("right", (2, 3))):
            mask = np.array([lat.coords(n)[0] in xs for n in range(lat.N)])
            row[side] = [int(sum(V.charge(st, X, "matter")[mask])) for _, X in gens]
        row["matter_total"] = [int(sum(V.charge(st, X, "matter"))) for _, X in gens]
        row["links_total"] = [int(sum(V.charge(st, X, "links"))) for _, X in gens]
        row["total"] = [int(sum(V.charge(st, X, "all"))) for _, X in gens]
        rows.append(row)
    rem = []
    for t in range(len(hist) - 1):
        rem.append([int(sum(V.remainder_term(hist[t], hist[t + 1], X))) for _, X in gens])
    cum = np.cumsum(np.array(rem, dtype=object), axis=0)
    tot0 = rows[0]["total"]
    exact = all(
        [r["total"][a_] - tot0[a_] for a_ in range(3)] == [int(cum[r["t"] - 1][a_] - cum[0][a_]) for a_ in range(3)]
        for r in rows)
    g = V.gauss_check(hist)
    scale = max(abs(v) for r in rows for v in r["matter_total"]) or 1
    res["b_exchange"] = {"rows_every_5": rows, "gauss": g,
                         "total_change_equals_summed_remainder_terms": exact,
                         "max_total_drift_over_matter_scale": max(abs(r["total"][a_] - tot0[a_])
                                                                  for r in rows for a_ in range(3)) / scale,
                         "max_matter_swing_over_scale": max(abs(r["matter_total"][a_] - rows[0]["matter_total"][a_])
                                                            for r in rows for a_ in range(3)) / scale,
                         "max_link_norm_rel": float(max(int(v) for v in V.link_norm2(hist[-1]).ravel()) ** 0.5 / A)}
    return res


# ------------------------------------------------------------------------------------------------ D2 colour flow
def d2_colour():
    L = 3
    blk = fine("su3")
    T = compose(blk)
    E = Engine(T, blk.Q)
    V = GaugeView(T, blk.params, blk.name)
    lat = lattice(L)
    rng = random.Random(2)
    s = vacuum_state(T, blk.Q, L, blk)
    a = s.a.astype(object)
    b = s.b.astype(object)
    Ap = 2000
    # a red-ish quark at one node, an anti-red-ish at another (colour-rotating states, exact ints)
    for n, sgn in ((lat.index(0, 0, 0), 1), (lat.index(1, 1, 1), -1)):
        for i in V.matter:
            a[i, n] = rng.randint(-Ap, Ap)
            b[i, n] = rng.randint(-Ap, Ap)
    s = State(L, a, b, s.r)
    hist = E.run(s, 40, history=True)
    gens = V.alg.generators
    rows = []
    for t in range(1, len(hist)):
        st = hist[t]
        rows.append({"t": t, "matter": [int(sum(V.charge(st, X, "matter"))) for _, X in gens],
                     "links": [int(sum(V.charge(st, X, "links"))) for _, X in gens],
                     "total": [int(sum(V.charge(st, X, "all"))) for _, X in gens]})
    rem = np.array([[int(sum(V.remainder_term(hist[t], hist[t + 1], X))) for _, X in gens]
                    for t in range(1, len(hist) - 1)], dtype=object)
    cum = np.cumsum(rem, axis=0)
    exact = all([rows[t]["total"][g] - rows[0]["total"][g] for g in range(len(gens))] ==
                [int(cum[t - 1][g]) for g in range(len(gens))] for t in range(1, len(rows)))
    g = V.gauss_check(hist)
    scale = max(abs(v) for r in rows for v in r["matter"]) or 1
    labels = [l for l, _ in gens]
    swing = {lab: (max(r["matter"][i] for r in rows) - min(r["matter"][i] for r in rows)) / scale
             for i, lab in enumerate(labels)}
    drift = {lab: (max(r["total"][i] for r in rows) - min(r["total"][i] for r in rows)) / scale
             for i, lab in enumerate(labels)}
    return {"generators": labels, "rows": rows[::4], "gauss": g, "total_change_equals_summed_remainder_terms": exact,
            "matter_swing_over_scale": swing, "total_drift_over_scale": drift,
            "max_link_unitarity_dev": V.link_unitarity(hist[-1]),
            "note": "matter-only colour flows into the links (gluon colour) and back; the total changes only by the "
                    "exact remainder term"}


if __name__ == "__main__":
    which = sys.argv[1:] or ["D3", "D1", "D2"]
    for w in which:
        t0 = time.time()
        res = {"D3": d3_witness, "D1": d1_isospin, "D2": d2_colour}[w]()
        res["stamp_utc"] = stamp()
        res["seconds"] = round(time.time() - t0, 1)
        (HERE / f"{w}.json").write_text(json.dumps(res, indent=1, default=str))
        print(w, "done", res["seconds"], "s")
