"""Demo D7 (pre-registered in NOTES_gravity.md): "gravity only slows" - the k = 0 constant of the lapse potential is
chosen in the PREPARATION so that U >= 0 (N <= 1) everywhere; dynamic test with a SELF-CONSISTENT (reciprocal) load and
a noisy headroom light field; control without the offset.

Usage: OMP_NUM_THREADS=1 nice -n 10 python research/metric_variant_v1/demos/gravity/d7_slows.py
Writes results/gravity/D7.json.
"""
from __future__ import annotations

import json
import math
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))

import numpy as np

from research.metric_variant_v1.core import Engine, compose
from research.metric_variant_v1.core.engine import OBJ, State
from research.metric_variant_v1.layers import gravity as gr
from research.metric_variant_v1.observe import gravity as og
from research.metric_variant_v1.prepare import gravity as pg
from research.metric_variant_v1.prepare import vacuum_state

OUT = ROOT / "research/metric_variant_v1/results/gravity"


def stamp():
    return subprocess.run(["date", "-u"], capture_output=True, text=True).stdout.strip()


def green_min(L):
    """g_L = -L * min G_L, G_L the zero-mean lattice Green function (-Lap G = delta - 1/L^3), float diagnostic."""
    s = np.zeros((L, L, L))
    s[0, 0, 0] = 1.0
    kk = 2 * np.pi * np.fft.fftfreq(L)
    lam = (2 * np.cos(kk)[:, None, None] + 2 * np.cos(kk)[None, :, None] + 2 * np.cos(kk)[None, None, :] - 6)
    lam[0, 0, 0] = 1.0
    Gk = np.fft.fftn(s - s.mean()) / (-lam)
    Gk[0, 0, 0] = 0
    G = np.real(np.fft.ifftn(Gk))
    return -L * G.min(), G[0, 0, 0]


def run(offset_factor, L=32, T=600, U3=0.02, seed=7):
    P, k = 2 ** 20, 24
    Q = gr.gravity_Q(P, k)
    c = (L // 2,) * 3
    load = gr.load_pair_spec("load", 2 * P * 3)
    light = gr.light_spec("light", Q)
    blocks = [gr.build_metric(Q=Q, components=("h00",)), gr.build_test_matter(load, Q=Q),
              gr.build_test_matter(light, Q=Q), gr.build_lapse(Q=Q, P=P, field="metric.h00", matters=[load, light])]
    Tn = compose(*blocks)
    eng = Engine(Tn, Q)
    s = vacuum_state(Tn, Q, L, *blocks)
    R = 2.5
    prof = sum((1 - (d / (R + 1)) ** 2) ** 2 for _, d in pg.ball(L, c, R))
    amp = int(math.sqrt(U3 * 8 * math.pi * P * (Q - 1) * 3 / (3 * prof)))
    s = pg.with_load(s, Tn, "load", Q, 2 * P * 3, c, R, amp)
    rng = np.random.default_rng(seed)
    a, b, r = s.a.astype(OBJ), s.b.astype(OBJ), s.r.astype(OBJ)
    gl = Tn.gear_index("light.L")
    a[gl] = np.array([int(v) for v in rng.integers(-256, 257, L ** 3)], dtype=object)
    b[gl] = np.array([int(v) for v in rng.integers(-256, 257, L ** 3)], dtype=object)
    s = State(L, a, b, r)
    # total source S at t = 0 (read-only evaluation of the tensor's F input minus its stencil, before the run)
    src = og.sources(eng, s, ["metric.h00"])["metric.h00"]
    S = int(src.sum())
    Fs = pg.static_field(L, Q, src)
    Cmin = -min(Fs.reshape(-1))
    C0 = int(math.ceil(offset_factor * Cmin))
    s = pg.with_field(s, Tn, "metric.h00", Fs + C0)
    gF = Tn.gear_index("metric.h00")
    rows = []
    light0 = int(np.max(np.abs(s.b[gl].astype(np.int64))))
    t0 = time.time()
    for t in range(1, T + 1):
        s = eng.step(s)
        if t % 10 == 0:
            if s.max_abs().bit_length() > 60:
                rows.append({"t": t, "exploded": True, "bits": s.max_abs().bit_length()})
                break
            Fb = s.b[gF]
            rows.append({"t": t, "minF/P": int(Fb.min()) / P, "maxF/P": int(Fb.max()) / P,
                         "max|light|": int(max(int(s.b[gl].max()), -int(s.b[gl].min()))),
                         "bits": s.max_abs().bit_length()})
            if s.max_abs().bit_length() > 200:
                break
    gL, G0 = green_min(L)
    return {"offset_factor": offset_factor, "S": S, "Cmin/P": Cmin / P, "C0/P": C0 / P,
            "U_offset_bound": Cmin / (2 * P),
            "U_offset_formula g_L S/(2P(Q-1)L)": gL * S / (2 * P * (Q - 1) * L), "g_L": gL,
            "min_over_run_minF/P": min(x["minF/P"] for x in rows if "minF/P" in x), "light0": light0,
            "max_light_growth": max(x["max|light|"] for x in rows if "max|light|" in x) / light0,
            "rows": rows[::5] + rows[-2:],
            "first_negative_t": next((x["t"] for x in rows if x.get("minF/P", 0) < 0), None),
            "exploded_at": next((x["t"] for x in rows if x.get("exploded")), None),
            "t_star_U=1/4_formula sqrt(3 Q L^3 P / S)": math.sqrt(3 * Q * L ** 3 * P / S),
            "elapsed_s": time.time() - t0}


def main():
    started = stamp()
    res = {"started": started}
    res["offset_1.5"] = run(1.5)
    res["control_0"] = run(0.0)
    res["written_utc"] = stamp()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "D7.json").write_text(json.dumps(res, indent=1, default=str) + "\n")
    for k_ in ("offset_1.5", "control_0"):
        v = res[k_]
        print(k_, {x: v[x] for x in ("Cmin/P", "U_offset_bound", "U_offset_formula g_L S/(2P(Q-1)L)", "g_L",
                                     "min_over_run_minF/P", "max_light_growth", "first_negative_t", "exploded_at",
                                     "t_star_U=1/4_formula sqrt(3 Q L^3 P / S)", "elapsed_s")})


if __name__ == "__main__":
    main()
