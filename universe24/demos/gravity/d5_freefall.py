"""Demo D5 (pre-registered in NOTES_gravity.md): free fall of a KG test packet toward a static load (MECHANISM load
with prepared settled field), read from CLICKS (quotient-size centroid) and from EVENTS (b^2 centroid).

Usage (repository root): OMP_NUM_THREADS=1 nice -n 10 python universe24/demos/gravity/d5_freefall.py
Writes runs/demos/gravity/D5.json.
"""
from __future__ import annotations

import json
import math
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

import numpy as np

from universe24.core import Engine, compose
from universe24.core.engine import OBJ, State
from universe24.layers import gravity as gr
from universe24.prepare import gravity as pg
from universe24.prepare import vacuum_state

OUT = Path("runs/demos/gravity")


def stamp():
    return subprocess.run(["date", "-u"], capture_output=True, text=True).stdout.strip()


def main(L=32, T=60, r0=8, sigma=2.5):
    started = stamp()
    P, k = 2 ** 20, 24
    Q = gr.gravity_Q(P, k)
    c = (L // 2,) * 3
    kg = gr.kg_spec("kg", Q, 2 * P * 6)
    blocks = [gr.build_metric(Q=Q, components=("h00",)), gr.build_static_load(Q=Q, field="metric.h00", name="load"),
              gr.build_test_matter(kg, Q=Q), gr.build_lapse(Q=Q, P=P, field="metric.h00", matters=[kg])]
    Tn = compose(*blocks)
    eng = Engine(Tn, Q)
    s = vacuum_state(Tn, Q, L, *blocks)
    R = 2.5
    prof = sum((1 - (d / (R + 1)) ** 2) ** 2 for _, d in pg.ball(L, c, R))
    amp = int(math.sqrt(0.08 * 8 * math.pi * P * (Q - 1) * 3 / prof))
    s = pg.with_static_load(s, Tn, "load", c, R, amp)
    Fst = pg.static_field(L, Q, pg.static_load_source(s, Tn, "load", 1))
    s = pg.with_field(s, Tn, "metric.h00", Fst - min(Fst.reshape(-1)))
    # KG packet at rest at x = c + r0 (k = 0), vacuum frequency (a slight mismatch with the local lapse is allowed)
    mu = 2 * P * 6
    cw = 1 - mu / (6 * Q)          # k = 0: b' + a = 2(1 - mu/(6Q)) b  -> cos w0 = 1 - mu/(6Q)
    w0 = math.acos(cw)
    gk = Tn.gear_index("kg.K")
    a, b, r = s.a.astype(OBJ), s.b.astype(OBJ), s.r.astype(OBJ)
    xyz = s.lattice.all_coords()
    centre = np.array([c[0] + r0, c[1], c[2]])
    d2 = ((xyz - centre) ** 2).sum(axis=1)
    A = 2 ** 14
    env = np.exp(-d2 / (2 * sigma ** 2))
    b[gk] = np.array([int(round(A * e)) for e in env], dtype=object)
    a[gk] = np.array([int(round(A * e * math.cos(w0))) for e in env], dtype=object)
    s = State(L, a, b, r)
    xs = xyz[:, 0].astype(float)
    ev, ck = [], []
    t0 = time.time()
    for t in range(T):
        s1 = eng.step(s)
        bb = s1.b[gk].astype(float)
        q = (s1.b[gk].astype(object) + s.a[gk].astype(object)).astype(float)     # click quotient of this update
        changed = (s1.a[gk] != s.a[gk]) | (s1.b[gk] != s.b[gk]) | (s1.r[gk] != s.r[gk])
        q = np.where(changed, q, 0.0)
        ev.append(float((xs * bb * bb).sum() / (bb * bb).sum()))
        ck.append(float((xs * q * q).sum() / (q * q).sum()))
        s = s1
    tt = np.arange(T, dtype=float)
    pe = np.polyfit(tt, np.array(ev), 2)
    pc = np.polyfit(tt, np.array(ck), 2)
    out = {"started": started, "L": L, "T": T, "r0": r0, "sigma": sigma, "Q": Q, "P": P,
           "x_event": ev[::5], "x_click": ck[::5], "accel_event": 2 * pe[0], "accel_click": 2 * pc[0],
           "accel_ratio_click/event-1": (pc[0] / pe[0] - 1) if pe[0] else None,
           "max_|x_click-x_event|": float(np.max(np.abs(np.array(ck) - np.array(ev)))),
           "fall_distance_event": ev[-1] - ev[0], "elapsed_s": time.time() - t0, "written_utc": stamp()}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "D5.json").write_text(json.dumps(out, indent=1, default=str) + "\n")
    print(json.dumps({k_: out[k_] for k_ in ("accel_event", "accel_click", "accel_ratio_click/event-1",
                                             "max_|x_click-x_event|", "fall_distance_event")}, indent=1))


if __name__ == "__main__":
    main()
