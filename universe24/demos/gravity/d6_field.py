"""Demo D6 (pre-registered in NOTES_gravity.md): the board BUILDS the static field of a prescribed load from F = 0
(no prepared field): 1/r profile inside the no-image window and the Gauss law (flux through boxes vs enclosed source).

Usage (repository root): OMP_NUM_THREADS=1 nice -n 10 python universe24/demos/gravity/d6_field.py
Writes results/gravity/D6.json.
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
from universe24.layers import gravity as gr
from universe24.observe import gravity as og
from universe24.prepare import gravity as pg
from universe24.prepare import vacuum_state

OUT = ROOT / "universe24/results/gravity"


def stamp():
    return subprocess.run(["date", "-u"], capture_output=True, text=True).stdout.strip()


def main(L=64, T=64, w0=48):
    started = stamp()
    P, k = 2 ** 20, 24
    Q = gr.gravity_Q(P, k)
    c = (L // 2,) * 3
    blocks = [gr.build_metric(Q=Q, components=("h00",)), gr.build_static_load(Q=Q, field="metric.h00", name="load")]
    Tn = compose(*blocks)
    eng = Engine(Tn, Q)
    s = vacuum_state(Tn, Q, L, *blocks)
    R = 2.5
    prof = sum((1 - (d / (R + 1)) ** 2) ** 2 for _, d in pg.ball(L, c, R))
    amp = int(math.sqrt(0.08 * 8 * math.pi * P * (Q - 1) * 3 / prof))
    s = pg.with_static_load(s, Tn, "load", c, R, amp)
    src = pg.static_load_source(s, Tn, "load", 1).astype(float)
    S = float(src.sum())
    gF = Tn.gear_index("metric.h00")
    acc = np.zeros((L, L, L))
    nacc = 0
    t0 = time.time()
    for t in range(T):
        s = eng.step(s)
        if t >= w0:
            acc += s.b[gF].astype(float).reshape(L, L, L)
            nacc += 1
    F = acc / nacc
    rs = list(range(3, 12))
    Fax = [F[c[0] + r, c[1], c[2]] for r in rs]
    slope = float(np.polyfit(np.log(rs), np.log(Fax), 1)[0])
    # infinite-lattice prediction F = S G(r)/(Q-1) with G ~ 1/(4 pi r): ratio F r 4 pi (Q-1) / S
    ratio = {r: F[c[0] + r, c[1], c[2]] * r * 4 * math.pi * (Q - 1) / S for r in rs}
    gauss = {}
    for h in (4, 6, 8):
        m = og.box_mask(L, c, h)
        flux = float(og.lap(F)[m].sum())
        gauss[h] = -(Q - 1) * flux / S
    out = {"started": started, "L": L, "T": T, "window": [w0, T], "Q": Q, "P": P, "S_source": S,
           "log_slope_r3_11": slope, "F_r_4pi(Q-1)/S": ratio, "gauss_-(Q-1)flux/S_by_halfwidth": gauss,
           "no_image_ok_for_r_le": (L - 12) * 0 + int(L - T * math.sqrt((Q - 1) / (3 * Q))),
           "elapsed_s": time.time() - t0, "written_utc": stamp()}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "D6.json").write_text(json.dumps(out, indent=1, default=str) + "\n")
    print(json.dumps(out, indent=1, default=str))


if __name__ == "__main__":
    main()
