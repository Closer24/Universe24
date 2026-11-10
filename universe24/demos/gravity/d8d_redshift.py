"""Demo D8 (pre-registered in NOTES_gravity.md): redshift VIA LIGHT. An emitter atom near a static load drives the
headroom light through the reciprocal on-site bilinear Phi_e = -g b_E b_L; the light's click frequency far away is
compared with a co-located receiver atom (CLICK space). MECHANISM static load, prepared field >= 0.

Usage: OMP_NUM_THREADS=1 nice -n 10 python universe24/demos/gravity/d8_redshift.py
Writes results/gravity/D8.json.
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

from universe24.core import Block, Engine, Tensor, compose
from universe24.core.engine import OBJ, State, extract_clicks
from universe24.layers import gravity as gr
from universe24.observe import gravity as og
from universe24.prepare import gravity as pg
from universe24.prepare import vacuum_state

OUT = ROOT / "universe24/results/gravity"


def stamp():
    return subprocess.run(["date", "-u"], capture_output=True, text=True).stdout.strip()


def main(L=48, T=420, U3=0.04, w_lo=180, g=2 ** 20, tag="D8d"):
    started = stamp()
    P, k = 2 ** 20, 24
    Q = gr.gravity_Q(P, k)
    c = (L // 2,) * 3
    mu = 2 * P * 24
    at, em, li = gr.atom_spec("at", mu), gr.atom_spec("em", mu), gr.light_spec("light", Q)
    emit = Block((), (("em.c", -g, (("light.L", (0, 0, 0), "b"),)), ("light.L", -g, (("em.c", (0, 0, 0), "b"),))),
                 name="emit", Q=Q, doc="reciprocal emitter coupling Phi_e = -g b_E b_L (on-site)")
    blocks = [gr.build_metric(Q=Q, components=("h00",)), gr.build_static_load(Q=Q, field="metric.h00", name="load"),
              gr.build_static_load(Q=Q, field="metric.h00", coeff=-1, name="anti")] + \
        [gr.build_test_matter(m, Q=Q) for m in (at, em, li)] + \
        [gr.build_lapse(Q=Q, P=P, field="metric.h00", matters=[at, em, li]), emit]
    Tn = compose(*blocks)
    eng = Engine(Tn, Q)
    s = vacuum_state(Tn, Q, L, *blocks)
    R = 2.5
    prof = sum((1 - (d / (R + 1)) ** 2) ** 2 for _, d in pg.ball(L, c, R))
    amp = int(math.sqrt(U3 * 8 * math.pi * P * (Q - 1) * 3 / prof))
    s = pg.with_static_load(s, Tn, "load", c, R, amp)
    s = pg.with_static_load(s, Tn, "anti", (0, 0, 0), R, amp)
    Fs = pg.static_field(L, Q, pg.static_load_source(s, Tn, "load", 1) + pg.static_load_source(s, Tn, "anti", -1))
    s = pg.with_field(s, Tn, "metric.h00", Fs - min(Fs.reshape(-1)))
    Nn, Fn = (c[0], c[1] + 4, c[2]), (c[0] + 15, c[1] + 4, c[2])
    s = pg.with_clocks(s, Tn, "at.c", Q, mu, [Nn, Fn], 2 ** 12)
    s = pg.with_clocks(s, Tn, "em.c", Q, mu, [Nn], 2 ** 16)
    lat = s.lattice
    nN, nF = lat.index(*Nn), lat.index(*Fn)
    gi = [Tn.gear_index(x) for x in ("at.c", "em.c", "light.L")]
    sub = Tensor([Tn.gears[x] for x in gi], [])
    keys = {(0, nN): "atN", (0, nF): "atF", (1, nN): "em", (2, nF): "lightF", (2, nN): "lightN"}
    series = {v: ([], []) for v in keys.values()}
    gF = Tn.gear_index("metric.h00")
    Fser = {"N": [], "F": []}
    t0 = time.time()
    for t in range(T):
        s1 = eng.step(s)
        lg = extract_clicks(sub, eng.D, State._raw(L, s.a[gi], s.b[gi], s.r[gi]),
                            State._raw(L, s1.a[gi], s1.b[gi], s1.r[gi]), step=t)
        for gg, n, q in zip(lg.gear, lg.node, lg.quotient):
            kk = keys.get((int(gg), int(n)))
            if kk:
                series[kk][0].append(t)
                series[kk][1].append(int(q))
        Fser["N"].append(int(s1.b[gF, nN]))
        Fser["F"].append(int(s1.b[gF, nF]))
        s = s1
    wl = pg.light_dispersion(Q, 1.0)
    w0 = math.acos(1 - mu / (6 * Q))
    # retardation: group velocity of light at the emitter frequency (axis estimate)
    kk_ = math.acos(1 - (1 - math.cos(w0)) * 3 * Q / (Q - 1))
    vg = (Q - 1) / (3 * Q) * math.sin(kk_) / math.sin(w0)
    tau = int(round(15 / vg))

    def rate(name, lo, hi):
        ts, qs = series[name]
        sel = [(t_, q_) for t_, q_ in zip(ts, qs) if lo <= t_ < hi]
        return og.rate_from_crossings(og.crossing_times([x for x, _ in sel], [y for _, y in sel]))
    w_atF, w_LF = rate("atF", w_lo, T), rate("lightF", w_lo, T)
    w_em_ret = rate("em", w_lo - tau, T - tau)
    w_atN = rate("atN", w_lo, T)
    w_em = rate("em", w_lo, T)
    w_atN_ret = rate("atN", w_lo - tau, T - tau)
    NF = np.mean([math.sqrt(1 - f / P) for f in Fser["F"][w_lo:T]])
    NN_ret = np.mean([math.sqrt(1 - f / P) for f in Fser["N"][w_lo - tau:T - tau]])
    pred = NF / NN_ret
    out = {"started": started, "L": L, "T": T, "U3": U3, "window": [w_lo, T], "tau_retardation": tau, "vg": vg,
           "w_atF": w_atF, "w_lightF": w_LF, "w_emitter_retarded": w_em_ret, "w_atN": w_atN,
           "freq_conservation_w_LF/w_E-1": w_LF / w_em_ret - 1,
           "redshift_via_light w_atF/w_LF": w_atF / w_LF, "prediction <N_F>/<N_N>_ret": pred,
           "redshift_dev": (w_atF / w_LF) / pred - 1,
           "half_angle_reading": (math.sin(w_atF / 2) / math.sin(w_LF / 2)) / pred - 1,
           "g": g, "w_emitter": w_em, "w_atN_retarded": w_atN_ret,
           "R_light (w_atF/w_LF)(w_E/w_atN), retarded": (w_atF / w_LF) * (w_em_ret / w_atN_ret),
           "R_light_dev": (w_atF / w_LF) * (w_em_ret / w_atN_ret) / pred - 1,
           "R_light_half_angle_dev": (math.sin(w_atF / 2) / math.sin(w_LF / 2))
                                     * (math.sin(w_em_ret / 2) / math.sin(w_atN_ret / 2)) / pred - 1,
           "light_crossings_F": len(og.crossing_times(*series["lightF"])), "elapsed_s": time.time() - t0,
           "written_utc": stamp()}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{tag}.json").write_text(json.dumps(out, indent=1, default=str) + "\n")
    print(json.dumps(out, indent=1, default=str))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(g=int(sys.argv[1]), tag=sys.argv[2])
    else:
        main()
