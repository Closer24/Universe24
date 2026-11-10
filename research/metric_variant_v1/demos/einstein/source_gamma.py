"""E4 T4 + T9 (Study 28, pre-registered in s28/EINF-A_NOTES.md §2): the field of a REAL board source (L0, reciprocal), gamma_eff,
and the conservation defect of the board's metric source (THEOREM: not exact, G-NOGO-a; here quantified).

System (tensor only; run loop = Engine.step only): L0 in form C (ref), the 10-gear metric in the DeWitt basis, today's form-C
lapse on L0 (lapseL0: the F part) and the NEW einL0 block (the a1, a2, a3 part). CONTROL: the same without einL0 (gamma encoded).
Seed (data only): a localized L0 lump, Gaussian envelope (sigma 2) x a fixed random 48-vector, a = b, at the centre.
Readouts (read-only): gamma_eff,d(r) = h_dd/h_00 = 1 + Delta_d/F on the axes at r = 3..7 (time mean over the last 20 updates);
the PREDICTION from the time-integrated sources, 1 + Sum_x Sum_t Delta_d-source / Sum_x Sum_t F-source (same Green function);
the same with the uniform (k = 0) modes removed (the closed-board F4 drift dominates the raw field on a small torus);
the conservation defect max |D_mu s^{mu nu}| / max |s| (observe.einstein.conservation_defect) at 5 times; the oscillation of the
total F source (2w). Report only (no pass band, pre-registered).
Usage (mirror only): python -m research.metric_variant_v1.demos.einstein.source_gamma OUT.json
"""
from __future__ import annotations

import json
import sys
import time

import numpy as np

from ...core.engine import Engine, State
from ...core.tensor import compose
from ...layers import gravity as gr
from ...layers.einstein import DELTA, build_l0_dewitt, dewitt_metric_block
from ...layers.gravity_l0c import build_l0c, build_l0c_lapse
from ...layers.system import P_GRAV, Q_DEFAULT
from ...observe.einstein import conservation_defect, source_of_stored


def system(Q, P, with_ein=True, body_signs=(1, -1, 1)):
    blocks = [build_l0c(Q=Q, body_signs=body_signs, name="ref", label="audit"), dewitt_metric_block(gr.build_metric(Q=Q)),
              build_l0c_lapse(Q=Q, P=P, field="metric.h00", body_signs=body_signs)]
    if with_ein:
        blocks.append(build_l0_dewitt(Q=Q, P=P, body_signs=body_signs))
    return compose(*blocks)


def seed(T, Q, L, A, sigma, rng_seed=3):
    G, N = T.G, L ** 3
    c = L // 2
    rng = np.random.default_rng(rng_seed)
    v = rng.normal(size=48)
    v /= np.sqrt((v * v).sum())
    xs = np.arange(L)
    X, Y, Z = np.meshgrid(xs, xs, xs, indexing="ij")
    env = np.exp(-((X - c) ** 2 + (Y - c) ** 2 + (Z - c) ** 2) / (2.0 * sigma ** 2)).ravel()
    a = np.zeros((G, N), dtype=np.int64)
    b = np.zeros((G, N), dtype=np.int64)
    for i in range(48):
        g = T.gear_index(f"ref.R{i:02d}")
        b[g] = np.rint(A * v[i] * env).astype(np.int64)
        a[g] = b[g]
    return State(L, a, b, np.full((G, N), 3 * Q - 1, dtype=np.int64))


def run(L=20, T_steps=60, A=1 << 18, sigma=2.0, Q=Q_DEFAULT, P=P_GRAV):
    out = {"L": L, "T": T_steps, "A": A, "sigma": sigma}
    c = L // 2
    for label, with_ein in (("einstein", True), ("control_no_einL0", False)):
        T = system(Q, P, with_ein)
        E = Engine(T, Q)
        s = seed(T, Q, L, A, sigma)
        s0 = s.copy()
        gi = {g: T.gear_index(f"metric.{g}") for g in ("h00", "a1", "a2", "a3")}
        acc = {g: np.zeros(L ** 3) for g in gi}
        src_tot = {g: 0 for g in gi}
        srcF_series = []
        defects = []
        prev = s
        t0 = time.time()
        for t in range(1, T_steps + 1):
            srcs = source_of_stored(E, s)
            for g in gi:
                src_tot[g] += int(np.sum(srcs[g]))
            srcF_series.append(int(np.sum(srcs["h00"])))
            s1 = E.step(s)
            if t in (10, 20, 30, 40, 50):
                defects.append({"t": t, **conservation_defect(E, s, s1)})
            s = s1
            if t > T_steps - 20:
                for g in gi:
                    acc[g] += s.b[gi[g]].astype(float)
        sec = time.time() - t0
        mean = {g: (acc[g] / 20.0).reshape(L, L, L) for g in gi}
        gam, gam_k = {}, {}
        for d, e in enumerate(((1, 0, 0), (0, 1, 0), (0, 0, 1))):
            Dd = sum(m * mean[g] for g, m in DELTA[d].items())
            Fk = mean["h00"] - mean["h00"].mean()            # zero mode removed (the closed-board F4 drift)
            Ddk = Dd - Dd.mean()
            row, rowk = {}, {}
            for r_ in range(3, 8):
                p = tuple((c + r_ * ee) % L for ee in e)
                F = mean["h00"][p]
                row[r_] = float(1 + Dd[p] / F) if F else None
                rowk[r_] = float(1 + Ddk[p] / Fk[p]) if Fk[p] else None
            gam["xyz"[d]] = row
            gam_k["xyz"[d]] = rowk
        pred = {}
        for d in range(3):
            Ds = sum(m * src_tot[g] for g, m in DELTA[d].items())
            pred["xyz"[d]] = 1 + Ds / src_tot["h00"] if src_tot["h00"] else None
        sF = np.array(srcF_series, dtype=float)
        out[label] = {"seconds": round(sec, 1), "gamma_eff_axes_r3_7": gam, "gamma_pred_from_integrated_sources": pred,
                      "gamma_eff_axes_r3_7_zero_mode_removed": gam_k,
                      "U_mean_final_window": float(mean["h00"].mean()) / (2 * P),
                      "integrated_sources": {g: str(v) for g, v in src_tot.items()},
                      "F_source_total_min_max_mean": [float(sF.min()), float(sF.max()), float(sF.mean())],
                      "conservation_defect": defects, "U_axis_r3_7": {r_: float(mean["h00"][(c + r_) % L, c, c]) / (2 * P)
                                                                         for r_ in range(3, 8)},
                      "bits": s.max_abs().bit_length(), "int64_steps": E.stats["int64_steps"],
                      "pyint_steps": E.stats["pyint_steps"],
                      "rewind_exact": bool(E.rewind(s, T_steps).same_as(s0))}
    return out


if __name__ == "__main__":
    res = run()
    with open(sys.argv[1], "w") as fh:
        json.dump(res, fh, indent=1)
    for k in ("einstein", "control_no_einL0"):
        print(k, json.dumps(res[k]["gamma_eff_axes_r3_7"]), json.dumps(res[k]["gamma_eff_axes_r3_7_zero_mode_removed"]),
              json.dumps(res[k]["gamma_pred_from_integrated_sources"]),
              res[k]["rewind_exact"], res[k]["seconds"])
