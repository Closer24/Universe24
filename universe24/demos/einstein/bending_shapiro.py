"""E4 T5 (Study 28, pre-registered in s28/EINF-A_NOTES.md §2): light bending (2x Newton) and Shapiro delay on the board.

System (tensor only; run loop = Engine.step only): the 10-gear metric in the DeWitt basis (layers.einstein.dewitt_metric_block of
layers.gravity.build_metric), a prescribed static DUST load sourcing metric.h00 (layers.gravity.build_static_load: MECHANISM,
designated one-way; T^ij = 0 so a1 = a2 = a3 stay exactly 0), and three one-way TEST lights on the ONE headroom stencil:
  lf  "full":  link factor 1 - (h_00 + h_dd)|link  (the Einstein reader; with a = 0 this is 1 - 2 h_00 = 1 - 4U)
  lc  "h00":   link factor 1 - h_00|link            (CONTROL: lapse only, the 1911 value)
  ln  "none":  no metric read                       (CONTROL: must be bit-identical with and without the load)
The field is BUILT BY THE BOARD from F = 0 (no preparation). Seed = initial data only: the load values and an exactly right-moving
plane-front light pulse along +x (rounded; same pulse in all three lights and both runs). Twin run: the same without the load.
Readout (read-only, float): arrival time at detector nodes (x_d, c + b, c) = centroid in t of the two-time energy
e = b^2 + a^2 - 2 cos(w) a b; delay(b) = t_load(b) - t_twin(b). Shapiro: delay ratio full/control; bending: ratio of the delay
SLOPES d delay/d b (the wavefront tilt = deflection angle / c). Criteria (pre-registered): delay ratio in [1.8, 2.2] at b = 4, 6, 8;
slope ratio in [1.7, 2.3]. Usage (mirror only): python -m universe24.demos.einstein.bending_shapiro OUT.json
"""
from __future__ import annotations

import json
import math
import sys
import time

import numpy as np

from ...core.engine import Engine, State
from ...core.tensor import compose
from ...layers import gravity as gr
from ...layers.einstein import build_test_light, dewitt_metric_block
from ...layers.system import P_GRAV, Q_DEFAULT


def build_system(Q: int, P: int, with_load: bool):
    blocks = [dewitt_metric_block(gr.build_metric(Q=Q))]
    blocks.append(gr.build_static_load(Q=Q, field="metric.h00", coeff=1, name="sload"))   # same tensor in both runs
    blocks += [build_test_light(Q=Q, P=P, mode="full", name="lf"), build_test_light(Q=Q, P=P, mode="h00", name="lc"),
               build_test_light(Q=Q, P=P, mode="none", name="ln")]
    return compose(*blocks)


def seed(T, Q, L, with_load, N0, sigma_load, k0, sigma_x, A, x0):
    G = T.G
    N = L ** 3
    c = L // 2
    a = np.zeros((G, N), dtype=np.int64)
    b = np.zeros((G, N), dtype=np.int64)
    r = np.full((G, N), 3 * Q - 1, dtype=np.int64)
    xs = np.arange(L)
    X, Y, Z = np.meshgrid(xs, xs, xs, indexing="ij")
    if with_load:
        rr2 = (X - c) ** 2 + (Y - c) ** 2 + (Z - c) ** 2
        n = np.rint(N0 * np.exp(-rr2 / (2.0 * sigma_load ** 2))).astype(np.int64)
        n[rr2 > 36] = 0
        gi = T.gear_index("sload.n")
        a[gi] = n.ravel()
        b[gi] = n.ravel()
    # exactly right-moving pulse (per Fourier mode, exact lattice frequency), uniform in y, z
    c2 = (Q - 1) / (3 * Q)
    kk = 2 * np.pi * np.fft.fftfreq(L)
    dx = ((xs - x0 + L // 2) % L) - L // 2
    f = A * np.exp(-dx ** 2 / (2.0 * sigma_x ** 2)) * np.cos(k0 * dx)
    fh = np.fft.fft(f)
    w = np.arccos(1 - c2 * (1 - np.cos(kk)))
    fh_pos = np.where(kk >= 0, 1.0, 0.0)
    # build analytic right-mover: keep the sign of k so that each mode moves in +x: phase(k x - w t)
    bt0 = np.real(np.fft.ifft(fh))
    btm1 = np.real(np.fft.ifft(fh * np.exp(1j * np.sign(kk) * w)))
    _ = fh_pos
    b1 = np.rint(bt0).astype(np.int64)
    a1 = np.rint(btm1).astype(np.int64)
    for nm in ("lf.L", "lc.L", "ln.L"):
        gi = T.gear_index(nm)
        b[gi] = np.broadcast_to(b1[:, None, None], (L, L, L)).ravel()
        a[gi] = np.broadcast_to(a1[:, None, None], (L, L, L)).ravel()
    return State(L, a, b, r)


def run(L=56, T_steps=100, N0=31_000_000, sigma_load=1.5, k0=0.5, sigma_x=5.0, A=1 << 20, x0_off=-18, xd_off=14,
        Q=Q_DEFAULT, P=P_GRAV, rewind=True):
    c = L // 2
    out = {"L": L, "T": T_steps, "N0": N0, "sigma_load": sigma_load, "k0": k0, "sigma_x": sigma_x, "A": A,
           "x0": c + x0_off, "x_detector": c + xd_off, "Q": Q, "P": P}
    c2 = (Q - 1) / (3 * Q)
    w0 = math.acos(1 - c2 * (1 - math.cos(k0)))
    bs = list(range(0, L // 2))
    rec = {}
    for with_load in (True, False):
        T = build_system(Q, P, with_load)
        E = Engine(T, Q)
        s = seed(T, Q, L, with_load, N0, sigma_load, k0, sigma_x, A, c + x0_off)
        s0 = s.copy()
        idx = {nm: T.gear_index(nm) for nm in ("lf.L", "lc.L", "ln.L", "metric.h00", "metric.a1", "metric.a2",
                                               "metric.a3")}
        lat_idx = [((c + xd_off) * L + (c + bb)) * L + c for bb in bs]
        series = {nm: [] for nm in ("lf.L", "lc.L", "ln.L")}
        amax = 0
        Fmin = 0
        t0 = time.time()
        for t in range(1, T_steps + 1):
            s = E.step(s)
            for nm in series:
                g = idx[nm]
                bb_ = s.b[g, lat_idx].astype(float)
                aa_ = s.a[g, lat_idx].astype(float)
                series[nm].append(bb_ * bb_ + aa_ * aa_ - 2 * math.cos(w0) * aa_ * bb_)
            amax = max([amax] + [max(abs(int(s.b[idx[g]].max())), abs(int(s.b[idx[g]].min())))
                                 for g in ("metric.a1", "metric.a2", "metric.a3")])
            Fmin = min(Fmin, int(s.b[idx["metric.h00"]].min()))
        F = s.b[idx["metric.h00"]].reshape(L, L, L)
        prof = {r_: float(F[(c + r_) % L, c, c]) / (2 * P) for r_ in range(0, 13)}
        res = {"seconds": round(time.time() - t0, 1), "a123_max_abs": amax, "F_min_over_run": Fmin,
               "U_axis_final": prof, "bits": s.max_abs().bit_length(), "int64_steps": E.stats["int64_steps"],
               "pyint_steps": E.stats["pyint_steps"]}
        tt = np.arange(1, T_steps + 1, dtype=float)
        arr = {}
        for nm, ser in series.items():
            M = np.array(ser)                       # (T, nb)
            arr[nm] = (tt[:, None] * M).sum(0) / M.sum(0)
        res["arrival"] = {nm: [float(v) for v in arr[nm]] for nm in arr}
        res["ln_series_hash"] = float(np.array(series["ln.L"]).sum())
        if rewind and with_load:
            back = E.rewind(s, T_steps)
            res["rewind_exact"] = bool(back.same_as(s0))
        rec["load" if with_load else "twin"] = res
    out["runs"] = rec
    d = {nm: [rec["load"]["arrival"][nm][i] - rec["twin"]["arrival"][nm][i] for i in range(len(bs))]
         for nm in ("lf.L", "lc.L", "ln.L")}
    out["delay"] = d
    out["b"] = bs
    out["delay_ratio_full_over_control"] = {b_: (d["lf.L"][b_] / d["lc.L"][b_] if d["lc.L"][b_] else None)
                                            for b_ in bs}
    slopes = {}
    for (b1, b2) in ((2, 6), (4, 8), (6, 10), (4, 12)):
        sf = (d["lf.L"][b2] - d["lf.L"][b1]) / (b2 - b1)
        sc = (d["lc.L"][b2] - d["lc.L"][b1]) / (b2 - b1)
        slopes[f"{b1}-{b2}"] = {"full": sf, "control": sc, "ratio": (sf / sc if sc else None)}
    out["slopes"] = slopes
    crit_delay = all(1.8 <= out["delay_ratio_full_over_control"][b_] <= 2.2 for b_ in (4, 6, 8))
    crit_slope = all(v["ratio"] is not None and 1.7 <= v["ratio"] <= 2.3 for k_, v in slopes.items() if k_ in ("2-6", "4-8"))
    out["verdict"] = {"shapiro_delay_ratio_in_[1.8,2.2]_at_b=4,6,8": crit_delay,
                      "bending_slope_ratio_in_[1.7,2.3]_(2-6,4-8)": crit_slope,
                      "none_light_identical": all(abs(v) < 1e-12 for v in d["ln.L"]),
                      "a123_exactly_zero": rec["load"]["a123_max_abs"] == 0}
    return out


if __name__ == "__main__":
    path = sys.argv[1]
    res = run()
    with open(path, "w") as fh:
        json.dump(res, fh, indent=1)
    print(json.dumps(res["verdict"]), json.dumps({k: res["delay_ratio_full_over_control"][k] for k in (2, 4, 6, 8, 10)}),
          json.dumps(res["slopes"]))
