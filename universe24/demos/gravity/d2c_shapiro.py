"""Demo D2c (pre-registered in NOTES_gravity.md): Shapiro diagnostic separating dispersion (carrier k), second order
(load strength) and the closed-board zero mode (control: uniform source with the same total S and offset).

Usage: OMP_NUM_THREADS=1 nice -n 10 python universe24/demos/gravity/d2c_shapiro.py
Writes runs/demos/gravity/D2c.json.
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

from universe24.core import Engine, Tensor, compose
from universe24.core.engine import OBJ, State, extract_clicks
from universe24.layers import gravity as gr
from universe24.prepare import gravity as pg
from universe24.prepare import vacuum_state

OUT = Path("runs/demos/gravity")


def stamp():
    return subprocess.run(["date", "-u"], capture_output=True, text=True).stdout.strip()


def one(kind, kcar, U3, L=40, sig=8.0):
    P, k = 2 ** 20, 24
    Q = gr.gravity_Q(P, k)
    c = (L // 2,) * 3
    lg, l11 = gr.light_spec("lightGR", Q), gr.light_spec("light1911", Q)
    blocks = [gr.build_metric(Q=Q, components=("h00",)), gr.build_static_load(Q=Q, field="metric.h00", name="load"),
              gr.build_test_matter(lg, Q=Q), gr.build_test_matter(l11, Q=Q),
              gr.build_lapse(Q=Q, P=P, field="metric.h00", matters=[lg], gamma="GR", name="lapseGR"),
              gr.build_lapse(Q=Q, P=P, field="metric.h00", matters=[l11], gamma="1911", name="lapse1911")]
    Tn = compose(*blocks)
    eng = Engine(Tn, Q)
    s = vacuum_state(Tn, Q, L, *blocks)
    R = 2.5
    prof = sum((1 - (d / (R + 1)) ** 2) ** 2 for _, d in pg.ball(L, c, R))
    amp = int(math.sqrt(U3 * 8 * math.pi * P * (Q - 1) * 3 / prof))
    loc = pg.with_static_load(s, Tn, "load", c, R, amp)
    src = pg.static_load_source(loc, Tn, "load", 1)
    Fs = pg.static_field(L, Q, src)
    C0 = -min(Fs.reshape(-1))
    if kind == "loaded":
        s = pg.with_field(loc, Tn, "metric.h00", Fs + C0)
    elif kind == "control":
        S = int(src.sum())
        nu = int(round(math.sqrt(S / L ** 3)))
        a, b, r = s.a.astype(OBJ), s.b.astype(OBJ), s.r.astype(OBJ)
        g = Tn.gear_index("load.n")
        a[g] = np.full(L ** 3, nu, dtype=object)
        b[g] = np.full(L ** 3, nu, dtype=object)
        s = State(L, a, b, r)
        s = pg.with_field(s, Tn, "metric.h00", np.full((L, L, L), C0, dtype=object))
    for gname in ("lightGR.L", "light1911.L"):
        s = pg.with_light_pulse(s, Tn, gname, Q, (c[0] - 15, c[1], c[2]), 0, kcar, sig, 2 ** 12)
    w = pg.light_dispersion(Q, kcar)
    vg = (Q - 1) / (3 * Q) * math.sin(kcar) / math.sin(w)
    t_exp = 30 / vg
    st = sig / vg
    T = int(t_exp + 4 * st) + 2
    dets = {f"F{b_}": s.lattice.index(c[0] + 15, c[1] + b_, c[2]) for b_ in (4, 6)}
    gi = [Tn.gear_index("lightGR.L"), Tn.gear_index("light1911.L")]
    sums = {(g, n): [0.0, 0.0] for g in range(2) for n in dets.values()}
    for t in range(T):
        s1 = eng.step(s)
        if abs(t - t_exp) <= 3 * st:
            for gg, g in enumerate(gi):
                for n in dets.values():
                    if (s1.a[g, n] != s.a[g, n]) or (s1.b[g, n] != s.b[g, n]) or (s1.r[g, n] != s.r[g, n]):
                        q = float(int(s1.b[g, n]) + int(s.a[g, n]))
                        sums[(gg, n)][0] += t * q * q
                        sums[(gg, n)][1] += q * q
        s = s1
    out = {}
    for name, n in dets.items():
        for gg, lab in ((0, "GR"), (1, "1911")):
            a_, b_ = sums[(gg, n)]
            out[f"{name}_{lab}"] = a_ / b_ if b_ else None
    out["t_exp"] = t_exp
    out["U_offset"] = C0 / (2 * P)
    return out


def main():
    started = stamp()
    t0 = time.time()
    res = {"started": started, "configs": {}}
    for kcar, U3 in ((0.8, 0.08), (0.4, 0.08), (0.4, 0.04), (0.4, 0.02)):
        runs = {kind: one(kind, kcar, U3) for kind in ("loaded", "control", "twin")}
        row = {"runs": runs}
        for b_ in (4, 6):
            for ref in ("control", "twin"):
                dG = runs["loaded"][f"F{b_}_GR"] - runs[ref][f"F{b_}_GR"]
                d1 = runs["loaded"][f"F{b_}_1911"] - runs[ref][f"F{b_}_1911"]
                row[f"b{b_}_vs_{ref}"] = {"delay_GR": dG, "delay_1911": d1, "ratio": dG / d1 if d1 else None}
        res["configs"][f"k{kcar}_U{U3}"] = row
        print(kcar, U3, {kk: v for kk, v in row.items() if kk != "runs"}, flush=True)
    res["elapsed_s"] = time.time() - t0
    res["written_utc"] = stamp()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "D2c.json").write_text(json.dumps(res, indent=1, default=str) + "\n")


if __name__ == "__main__":
    main()
