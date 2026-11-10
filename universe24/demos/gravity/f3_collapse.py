"""Finding F3 threshold data (pre-registered in NOTES_gravity.md): a SELF-GRAVITATING reciprocal load (circulating clock
pairs feeling their own lapse) with a prescribed static anti-load at the antipode (MECHANISM, only to cancel the
closed-board zero mode). Records max U at the centre and the runaway time versus the load strength.

Usage: OMP_NUM_THREADS=1 nice -n 10 python universe24/demos/gravity/f3_collapse.py
Writes results/gravity/F3.json.
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
from universe24.prepare import gravity as pg
from universe24.prepare import vacuum_state

OUT = ROOT / "universe24/results/gravity"


def stamp():
    return subprocess.run(["date", "-u"], capture_output=True, text=True).stdout.strip()


def run(U3, L=32, T=600):
    P, k = 2 ** 20, 24
    Q = gr.gravity_Q(P, k)
    c = (L // 2,) * 3
    load = gr.load_pair_spec("load", 2 * P * 3)
    blocks = [gr.build_metric(Q=Q, components=("h00",)), gr.build_test_matter(load, Q=Q),
              gr.build_static_load(Q=Q, field="metric.h00", coeff=-1, name="anti"),
              gr.build_lapse(Q=Q, P=P, field="metric.h00", matters=[load])]
    Tn = compose(*blocks)
    eng = Engine(Tn, Q)
    s = vacuum_state(Tn, Q, L, *blocks)
    R = 2.5
    prof = sum((1 - (d / (R + 1)) ** 2) ** 2 for _, d in pg.ball(L, c, R))
    amp = int(math.sqrt(U3 * 8 * math.pi * P * (Q - 1) * 3 / (3 * prof)))
    s = pg.with_load(s, Tn, "load", Q, 2 * P * 3, c, R, amp)
    # anti-load amplitude: equal total source (static density gear, source -n^2): n^2 = 3 (X^2 + Y^2) summed
    s = pg.with_static_load(s, Tn, "anti", (0, 0, 0), R, int(round(amp * math.sqrt(3))))
    gF = Tn.gear_index("metric.h00")
    n0 = s.lattice.index(*c)
    rows, run_t = [], None
    for t in range(1, T + 1):
        s = eng.step(s)
        if t % 10 == 0:
            bits = s.max_abs().bit_length()
            if bits > 60:
                run_t = t
                break
            rows.append((t, int(s.b[gF, n0]) / (2 * P), bits))
    return {"U3_target": U3, "amp": amp, "runaway_t": run_t, "U_centre_max": max(r[1] for r in rows),
            "U_centre_first_100": [r[1] for r in rows[:10]], "U_centre_last": rows[-1][1] if rows else None,
            "rows_every_50": rows[4::5]}


def main():
    started = stamp()
    t0 = time.time()
    res = {"started": started, "runs": [run(U3) for U3 in (0.02, 0.04, 0.08)]}
    res["elapsed_s"] = time.time() - t0
    res["written_utc"] = stamp()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "F3.json").write_text(json.dumps(res, indent=1, default=str) + "\n")
    for r in res["runs"]:
        print(r["U3_target"], "runaway_t", r["runaway_t"], "U_centre_max", round(r["U_centre_max"], 3),
              "U_last", r["U_centre_last"])


if __name__ == "__main__":
    main()
