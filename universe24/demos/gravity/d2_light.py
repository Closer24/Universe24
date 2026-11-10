"""Demo D2 (pre-registered in NOTES_gravity.md): Shapiro delay of light with the GR link factor vs the 1911 lapse-only
CONTROL, and redshift via light; MECHANISM load + prepared static field.

Usage (repository root): OMP_NUM_THREADS=2 nice -n 10 python universe24/demos/gravity/d2_light.py
Writes results/gravity/D2.json.
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
from universe24.core.engine import State, extract_clicks
from universe24.layers import gravity as gr
from universe24.observe import gravity as og
from universe24.prepare import gravity as pg
from universe24.prepare import vacuum_state

OUT = ROOT / "universe24/results/gravity"


def stamp():
    return subprocess.run(["date", "-u"], capture_output=True, text=True).stdout.strip()


def build(Q, P, k):
    at = gr.atom_spec("at", 2 * P * 24)
    lg, l11 = gr.light_spec("lightGR", Q), gr.light_spec("light1911", Q)
    blocks = [gr.build_metric(Q=Q, components=("h00",)), gr.build_static_load(Q=Q, field="metric.h00", name="load")] + \
        [gr.build_test_matter(m, Q=Q) for m in (at, lg, l11)] + \
        [gr.build_lapse(Q=Q, P=P, field="metric.h00", matters=[at, lg], gamma="GR", name="lapseGR"),
         gr.build_lapse(Q=Q, P=P, field="metric.h00", matters=[l11], gamma="1911", name="lapse1911")]
    return blocks


def run(loaded, L=40, T=120, TL=110, U3=0.08, kcar=0.8, sig=8.0):
    P, k = 2 ** 20, 24
    Q = gr.gravity_Q(P, k)
    c = (L // 2,) * 3
    blocks = build(Q, P, k)
    Tn = compose(*blocks)
    eng = Engine(Tn, Q)
    s = vacuum_state(Tn, Q, L, *blocks)
    R = 2.5
    prof = sum((1 - (d / (R + 1)) ** 2) ** 2 for _, d in pg.ball(L, c, R))
    amp = int(math.sqrt(U3 * 8 * math.pi * P * (Q - 1) * 3 / prof))
    if loaded:
        s = pg.with_static_load(s, Tn, "load", c, R, amp)
        src = pg.static_load_source(s, Tn, "load", 1)
        Fst = pg.static_field(L, Q, src)
        fmin = min(Fst.reshape(-1))
        s = pg.with_field(s, Tn, "metric.h00", Fst - fmin)
    for g in ("lightGR.L", "light1911.L"):
        s = pg.with_light_pulse(s, Tn, g, Q, (c[0] - 15, c[1], c[2]), 0, kcar, sig, 2 ** 12)
    dets = {}
    for b in (4, 6):
        dets[f"N{b}"] = (c[0], c[1] + b, c[2])
        dets[f"F{b}"] = (c[0] + 15, c[1] + b, c[2])
    s = pg.with_clocks(s, Tn, "at.c", Q, 2 * P * 24, list(dets.values()), 2 ** 12)
    lat = s.lattice
    nodes = {kk: lat.index(*p) for kk, p in dets.items()}
    gidx = [Tn.gear_index(g) for g in ("lightGR.L", "light1911.L", "at.c")]
    sub = Tensor([Tn.gears[g] for g in gidx], [])
    series = {(g, n): ([], []) for g in range(3) for n in nodes.values()}
    gF = Tn.gear_index("metric.h00")
    Fsum = {n: 0 for n in nodes.values()}
    for t in range(T):
        s1 = eng.step(s)
        lg_ = extract_clicks(sub, eng.D, State._raw(L, s.a[gidx], s.b[gidx], s.r[gidx]),
                             State._raw(L, s1.a[gidx], s1.b[gidx], s1.r[gidx]), step=t)
        for g, n, q in zip(lg_.gear, lg_.node, lg_.quotient):
            key = (int(g), int(n))
            if key in series:
                series[key][0].append(t)
                series[key][1].append(int(q))
        for n in nodes.values():
            Fsum[n] += int(s1.b[gF, n])
        s = s1
    out = {}
    for kk, n in nodes.items():
        row = {"Fbar/P": Fsum[n] / T / P}
        for g, nm in ((0, "GR"), (1, "1911")):
            ts, qs = series[(g, n)]
            sel = [(t_, q_) for t_, q_ in zip(ts, qs) if t_ < TL]
            wsum = sum(q_ * q_ for _, q_ in sel)
            row[f"arrival_{nm}"] = sum(t_ * q_ * q_ for t_, q_ in sel) / wsum if wsum else None
            big = max((abs(q_) for _, q_ in sel), default=0)
            selb = [(t_, q_) for t_, q_ in sel if abs(q_) > 0.2 * big]
            times = og.crossing_times([x for x, _ in selb], [y for _, y in selb])
            row[f"w_light_{nm}"] = og.rate_from_crossings(times)
        ts, qs = series[(2, n)]
        times = og.crossing_times(ts, qs)
        row["w_atom"] = og.rate_from_crossings(times)
        row["atom_crossings"] = len(times)
        w0 = math.acos(1 - 2 * 2 ** 20 * 24 / (6 * gr.gravity_Q(2 ** 20, 24)))
        row["N_atom_half_angle"] = math.sin(row["w_atom"] / 2) / math.sin(w0 / 2)
        out[kk] = row
    return out, {"Q": Q, "P": P, "k": k, "L": L, "T": T, "load_amp": amp if loaded else 0}


def main(U3=0.08, kcar=0.8, sig=8.0, tag="D2"):
    started = stamp()
    t0 = time.time()
    loaded, meta = run(True, U3=U3, kcar=kcar, sig=sig)
    twin, _ = run(False, U3=U3, kcar=kcar, sig=sig)
    meta.update({"U3": U3, "kcar": kcar, "sigma": sig})
    res = {"started": started, "meta": meta, "loaded": loaded, "twin": twin}
    summ = {}
    for b in (4, 6):
        F_ = f"F{b}"
        dGR = loaded[F_]["arrival_GR"] - twin[F_]["arrival_GR"]
        d11 = loaded[F_]["arrival_1911"] - twin[F_]["arrival_1911"]
        N_ = f"N{b}"
        rs = {}
        for nm in ("GR", "1911"):
            rs[nm] = (loaded[N_][f"w_light_{nm}"] / loaded[N_]["w_atom"]) / (loaded[F_][f"w_light_{nm}"] /
                                                                             loaded[F_]["w_atom"])
        pred = math.sqrt((1 - loaded[F_]["Fbar/P"]) / (1 - loaded[N_]["Fbar/P"]))
        ha = loaded[F_]["N_atom_half_angle"] / loaded[N_]["N_atom_half_angle"]
        summ[f"b{b}"] = {"delay_GR": dGR, "delay_1911": d11, "ratio_GR/1911": dGR / d11 if d11 else None,
                         "freq_conservation_GR_N/F-1": loaded[N_]["w_light_GR"] / loaded[F_]["w_light_GR"] - 1,
                         "redshift_via_light_GR": rs["GR"], "redshift_via_light_1911": rs["1911"],
                         "redshift_pred_lapse": pred,
                         "redshift_dev_GR": rs["GR"] / pred - 1,
                         "redshift_half_angle_atoms_N_F/N_N": ha, "half_angle_dev": ha / pred - 1}
    res["summary"] = summ
    res["elapsed_s"] = time.time() - t0
    res["written_utc"] = stamp()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{tag}.json").write_text(json.dumps(res, indent=1, default=str) + "\n")
    print(json.dumps(summ, indent=1))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), sys.argv[4])
    else:
        main()
