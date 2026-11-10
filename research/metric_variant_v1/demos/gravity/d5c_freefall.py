"""Demo D5b (pre-registered in NOTES_gravity.md): free fall of a KG test packet in a DRIFT-FREE settled field
(prescribed load + anti-load, offset C0 >= 0), packet prepared at the LOCAL frequency; centroids weighted by the
two-time EVENT energy and by the two-size CLICK energy.

Usage: OMP_NUM_THREADS=1 nice -n 10 python research/metric_variant_v1/demos/gravity/d5b_freefall.py
Writes results/gravity/D5b.json.
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
from research.metric_variant_v1.prepare import gravity as pg
from research.metric_variant_v1.prepare import vacuum_state

OUT = ROOT / "research/metric_variant_v1/results/gravity"


def stamp():
    return subprocess.run(["date", "-u"], capture_output=True, text=True).stdout.strip()


def main(L=32, T=70, r0=6, sigma=3.0, U3=0.03):
    started = stamp()
    P, k = 2 ** 20, 24
    Q = gr.gravity_Q(P, k)
    c = (L // 2,) * 3
    mu = 2 * P * 6
    kg = gr.kg_spec("kg", Q, mu)
    blocks = [gr.build_metric(Q=Q, components=("h00",)), gr.build_static_load(Q=Q, field="metric.h00", name="load"),
              gr.build_static_load(Q=Q, field="metric.h00", coeff=-1, name="anti"),
              gr.build_test_matter(kg, Q=Q), gr.build_lapse(Q=Q, P=P, field="metric.h00", matters=[kg])]
    Tn = compose(*blocks)
    eng = Engine(Tn, Q)
    s = vacuum_state(Tn, Q, L, *blocks)
    R = 2.5
    prof = sum((1 - (d / (R + 1)) ** 2) ** 2 for _, d in pg.ball(L, c, R))
    amp = int(math.sqrt(U3 * 8 * math.pi * P * (Q - 1) * 3 / prof))
    s = pg.with_static_load(s, Tn, "load", c, R, amp)
    s = pg.with_static_load(s, Tn, "anti", (0, 0, 0), R, amp)
    Fs = pg.static_field(L, Q, pg.static_load_source(s, Tn, "load", 1) + pg.static_load_source(s, Tn, "anti", -1))
    F0 = Fs - min(Fs.reshape(-1))
    s = pg.with_field(s, Tn, "metric.h00", F0)
    gk = Tn.gear_index("kg.K")
    a, b, r = s.a.astype(OBJ), s.b.astype(OBJ), s.r.astype(OBJ)
    xyz = s.lattice.all_coords()
    centre = np.array([c[0] + r0, c[1], c[2]])
    d2 = ((xyz - centre) ** 2).sum(axis=1)
    A = 2 ** 14
    Ff = np.array([float(v) for v in F0.reshape(-1)])
    for n in np.flatnonzero(d2 <= (4 * sigma) ** 2):
        e = math.exp(-d2[n] / (2 * sigma ** 2))
        cw = 1 - mu * (1 - Ff[n] / P) / (6 * Q)          # local k = 0 frequency (clock factor N^2 on the mass)
        b[gk, n] = int(round(A * e))
        a[gk, n] = int(round(A * e * cw))
    s = State(L, a, b, r)
    xs = xyz[:, 0].astype(float)
    cw0 = 1 - mu / (6 * Q)
    ev, ck = [], []
    q_prev = None
    t0 = time.time()
    for t in range(T):
        s1 = eng.step(s)
        b0 = s.b[gk].astype(float)
        bm = s.a[gk].astype(float)
        q = (s1.b[gk].astype(object) + s.a[gk].astype(object)).astype(float)
        changed = (s1.a[gk] != s.a[gk]) | (s1.b[gk] != s.b[gk]) | (s1.r[gk] != s.r[gk])
        q = np.where(changed, q, 0.0)
        wE = b0 * b0 + bm * bm - 2 * cw0 * b0 * bm
        ev.append(float((xs * wE).sum() / wE.sum()))
        if q_prev is not None:
            wC = q * q + q_prev * q_prev - 2 * cw0 * q * q_prev
            ck.append(float((xs * wC).sum() / wC.sum()))
        else:
            ck.append(float("nan"))
        q_prev = q
        s = s1
    tt = np.arange(5, T, dtype=float)
    pe = np.polyfit(tt, np.array(ev[5:]), 2)
    pc = np.polyfit(tt, np.array(ck[5:]), 2)
    dif = np.abs(np.array(ck[5:]) - np.array(ev[5:]))
    out = {"started": started, "L": L, "T": T, "r0": r0, "sigma": sigma, "U3": U3, "Q": Q, "P": P,
           "x_event_every5": ev[::5], "x_click_every5": ck[::5], "accel_event": 2 * pe[0], "accel_click": 2 * pc[0],
           "accel_ratio_click/event-1": pc[0] / pe[0] - 1, "v0_event": pe[1], "max_|x_click-x_event|_t>=5": float(dif.max()),
           "fall_distance_event": ev[-1] - ev[0], "elapsed_s": time.time() - t0, "written_utc": stamp()}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "D5c.json").write_text(json.dumps(out, indent=1, default=str) + "\n")
    print(json.dumps({k_: out[k_] for k_ in ("accel_event", "accel_click", "accel_ratio_click/event-1", "v0_event",
                                             "max_|x_click-x_event|_t>=5", "fall_distance_event")}, indent=1))


if __name__ == "__main__":
    main()
