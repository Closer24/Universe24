"""Demo D1 (pre-registered in NOTES_gravity.md): clocks read from CLICKS around a static load, universality of two
species, beta = 1 atoms, field profile; MECHANISM load (prepared circulating clock pairs + anti-load at the antipode).

Usage (repository root):  OMP_NUM_THREADS=2 nice -n 10 python universe24/demos/gravity/d1_clocks.py
Writes runs/demos/gravity/D1.json.
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
from universe24.observe import gravity as og
from universe24.prepare import gravity as pg
from universe24.prepare import vacuum_state

OUT = Path("runs/demos/gravity")


def stamp():
    return subprocess.run(["date", "-u"], capture_output=True, text=True).stdout.strip()


def main(L=32, T=1300, t0=300, rewind=True):
    started = stamp()
    P, k = 2 ** 20, 24
    Q = gr.gravity_Q(P, k)
    c = (L // 2,) * 3
    atA, atB, atC = gr.atom_spec("atA", 2 * P * 1), gr.atom_spec("atB", 2 * P * 4), gr.atom_spec("atC", 2 * P * 1)
    mats = [atA, atB, atC]
    blocks = [gr.build_metric(Q=Q, components=("h00",)),
              gr.build_static_load(Q=Q, field="metric.h00", coeff=1, name="load"),
              gr.build_static_load(Q=Q, field="metric.h00", coeff=-1, name="anti")] + \
             [gr.build_test_matter(m, Q=Q) for m in mats] + \
             [gr.build_lapse(Q=Q, P=P, field="metric.h00", matters=mats),
              gr.build_beta(Q=Q, P=P, k=k, field="metric.h00", matters=[atC], reciprocal_source=False)]
    Tn = compose(*blocks)
    eng = Engine(Tn, Q)
    s = vacuum_state(Tn, Q, L, *blocks)
    # load amplitude for U(3) ~ 0.08 (continuum estimate; the measured field is used afterwards)
    R = 2.5
    prof = sum((1 - (d / (R + 1)) ** 2) ** 2 for _, d in pg.ball(L, c, R))
    amp = int(math.sqrt(0.08 * 8 * math.pi * P * (Q - 1) * 3 / prof))
    s = pg.with_static_load(s, Tn, "load", c, R, amp)
    s = pg.with_static_load(s, Tn, "anti", (0, 0, 0), R, amp)
    # MECHANISM preparation of settled fields: F = static lattice solution of the (zero-net) load source, G = F^2/(2P)
    Fst = pg.static_field(L, Q, pg.static_load_source(s, Tn, "load", 1) + pg.static_load_source(s, Tn, "anti", -1))
    s = pg.with_field(s, Tn, "metric.h00", Fst)
    s = pg.with_field(s, Tn, "beta.G", np.vectorize(lambda v: (v * v) // (2 * P), otypes=[object])(Fst))
    pos = {f"ax{r}": (c[0] + r, c[1], c[2]) for r in (3, 4, 5, 6, 8, 10, 12)}
    pos.update({f"dg{d}": (c[0] + d, c[1] + d, c[2] + d) for d in (2, 3, 4)})
    A_at = 2 ** 12
    for g, mu in (("atA.c", 2 * P), ("atB.c", 8 * P), ("atC.c", 2 * P)):
        s = pg.with_clocks(s, Tn, g, Q, mu, list(pos.values()), A_at)
    s_init = s
    lat = s.lattice
    nodes = {k_: lat.index(*p) for k_, p in pos.items()}
    atom_g = [Tn.gear_index(g) for g in ("atA.c", "atB.c", "atC.c")]
    sub = Tensor([Tn.gears[g] for g in atom_g], [])
    series = {(g, n): ([], []) for g in range(3) for n in nodes.values()}
    gF, gG = Tn.gear_index("metric.h00"), Tn.gear_index("beta.G")
    Fsum = {n: 0 for n in nodes.values()}
    Gsum = {n: 0 for n in nodes.values()}
    Nsum = {n: [0.0, 0.0, 0.0] for n in nodes.values()}     # event: <sqrt(1-F/P)>, <sqrt(1-F/P+G/P)>, <sqrt(1-F/P+F^2/2P^2)>
    nwin = 0
    Fmean_field = np.zeros(L ** 3, dtype=float)
    src_mean = np.zeros(L ** 3, dtype=float)
    nsrc = 0
    tt = time.time()
    hist_tail = None
    for t in range(T):
        s1 = eng.step(s)
        before = State._raw(L, s.a[atom_g], s.b[atom_g], s.r[atom_g])
        after = State._raw(L, s1.a[atom_g], s1.b[atom_g], s1.r[atom_g])
        lg = extract_clicks(sub, eng.D, before, after, step=t, stream="official")
        for g, n, q in zip(lg.gear, lg.node, lg.quotient):
            key = (int(g), int(n))
            if key in series:
                series[key][0].append(t)
                series[key][1].append(int(q))
        if t >= t0:
            for n in nodes.values():
                Fv, Gv = int(s1.b[gF, n]), int(s1.b[gG, n])
                Fsum[n] += Fv
                Gsum[n] += Gv
                Nsum[n][0] += math.sqrt(1 - Fv / P)
                Nsum[n][1] += math.sqrt(1 - Fv / P + Gv / P)
                Nsum[n][2] += math.sqrt(1 - Fv / P + Fv * Fv / (2 * P * P))
            nwin += 1
            Fmean_field += s1.b[gF].astype(float)
            if t % 20 == 0:
                u = eng.inputs(s1)[gF].astype(object)
                b = og.arr(s1, Tn, "metric.h00").reshape(-1)
                stencil = ((Q - 1) * og.sum6(og.arr(s1, Tn, "metric.h00")) + 6 * og.arr(s1, Tn, "metric.h00")).reshape(-1)
                src_mean += (u - stencil).astype(float)
                nsrc += 1
        s = s1
    elapsed = time.time() - tt
    Fmean_field /= nwin
    src_mean /= nsrc
    # ---- click readout
    res = {}
    w0 = {0: math.acos(1 - 2 * P / (6 * Q)), 1: math.acos(1 - 8 * P / (6 * Q)), 2: math.acos(1 - 2 * P / (6 * Q))}
    names = {0: "A", 1: "B", 2: "C"}
    worst_a, worst_univ, worst_c = 0.0, 0.0, 0.0
    betas = []
    for key, n in nodes.items():
        Fb, Gb = Fsum[n] / nwin, Gsum[n] / nwin
        U = Fb / (2 * P)
        row = {"Fbar/P": Fb / P, "U": U, "Gbar/(Fbar^2/2P)": (Gb / (Fb * Fb / (2 * P))) if Fb else None}
        Nc = {}
        for g in range(3):
            ts, qs = series[(g, n)]
            sel = [(t_, q_) for t_, q_ in zip(ts, qs) if t_ >= t0]
            times = og.crossing_times([x for x, _ in sel], [y for _, y in sel])
            w = og.rate_from_crossings(times)
            Nc[g] = math.sin(w / 2) / math.sin(w0[g] / 2)
            row[f"w_{names[g]}"] = w
            row[f"N_click_{names[g]}"] = Nc[g]
            row[f"crossings_{names[g]}"] = len(times)
        Npred = Nsum[n][0] / nwin                      # event <N(t)> (the field is not perfectly static)
        NpredC = Nsum[n][1] / nwin
        Nbeta1 = Nsum[n][2] / nwin
        row["N_pred_lapse"] = Npred
        row["N_pred_C_own"] = NpredC
        row["beta_eff_click"] = (Nc[2] - Nc[0]) / (Nbeta1 - Npred) if Nbeta1 != Npred else None
        row["beta_eff_event"] = (NpredC - Npred) / (Nbeta1 - Npred) if Nbeta1 != Npred else None
        row["dev_A"] = Nc[0] / Npred - 1
        row["dev_B"] = Nc[1] / Npred - 1
        row["univ_A/B-1"] = Nc[0] / Nc[1] - 1
        row["raw_w_ratio_dev"] = (row["w_A"] / row["w_B"]) / (w0[0] / w0[1]) - 1
        row["dev_C_own"] = Nc[2] / NpredC - 1
        if U > 0:
            row["beta_C"] = (Nc[2] ** 2 - 1 + 2 * U) / (2 * U * U)
            row["beta_A_control"] = (Nc[0] ** 2 - 1 + 2 * U) / (2 * U * U)
            if U > 0.03:
                betas.append((row["beta_eff_click"], row["beta_A_control"], row["beta_C"]))
        worst_a = max(worst_a, abs(row["dev_A"]), abs(row["dev_B"]))
        worst_univ = max(worst_univ, abs(row["univ_A/B-1"]))
        worst_c = max(worst_c, abs(row["dev_C_own"]))
        res[key] = row
    # ---- field vs exact static lattice solution of the time-mean source (float FFT, labelled diagnostic)
    sm = src_mean.reshape(L, L, L)
    kk = 2 * np.pi * np.fft.fftfreq(L)
    lam = (2 * np.cos(kk)[:, None, None] + 2 * np.cos(kk)[None, :, None] + 2 * np.cos(kk)[None, None, :] - 6)
    sk = np.fft.fftn(sm - sm.mean())
    lam[0, 0, 0] = 1.0
    Fk = -sk / ((Q - 1) * lam) * (-1)          # 2(Q-1) Lap F + 2 s = 0  ->  F = -s/((Q-1) Lap)
    Fk = sk / ((Q - 1) * -lam)
    Fk[0, 0, 0] = 0
    Fstat = np.real(np.fft.ifftn(Fk))
    Fm = Fmean_field.reshape(L, L, L)
    prof = []
    for r in (2, 3, 4, 5, 6, 8, 10):
        x = (c[0] + r, c[1], c[2])
        meas = Fm[x] - Fm.mean()
        prof.append({"r": r, "Fbar/P": Fm[x] / P, "ratio_to_lattice_static": meas / Fstat[x]})
    rr = np.array([p_["r"] for p_ in prof[:5]], dtype=float)
    ff = np.array([Fm[(c[0] + int(r), c[1], c[2])] for r in rr])
    slope = float(np.polyfit(np.log(rr), np.log(ff), 1)[0])
    out = {"started": started, "finished_run": stamp(), "L": L, "T": T, "window": [t0, T], "P": P, "k": k, "Q": Q,
           "load_amp": amp, "elapsed_s": elapsed, "engine_stats": dict(eng.stats), "atoms": res,
           "criteria": {"a_max_|N_click/N_pred-1|": worst_a, "b_max_univ": worst_univ,
                        "c_max_|N_C/<sqrt(1-F/P+G/P)>-1|": worst_c,
                        "c_beta_eff_click_mean(U>0.03)": float(np.mean([b_[0] for b_ in betas])) if betas else None,
                        "c_beta_mean_C_from_meanU(U>0.03)": float(np.mean([b_[2] for b_ in betas])) if betas else None,
                        "c_beta_mean_control_A(U>0.03)": float(np.mean([b_[1] for b_ in betas])) if betas else None,
                        "c_beta_values": betas},
           "field_profile": prof, "log_slope_r2_6": slope}
    if rewind:
        tr = time.time()
        back = s
        for _ in range(T):
            back = eng.inverse_step(back)
        out["e_rewind_exact"] = back.same_as(s_init)
        out["rewind_s"] = time.time() - tr
    out["written_utc"] = stamp()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "D1.json").write_text(json.dumps(out, indent=1, default=str) + "\n")
    print(json.dumps(out["criteria"], indent=1, default=str))
    print("profile", prof, "slope", slope, "rewind", out.get("e_rewind_exact"))


if __name__ == "__main__":
    args = [int(a) for a in sys.argv[1:]]
    main(*args)
