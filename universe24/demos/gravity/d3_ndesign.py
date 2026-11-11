"""Demo D3 (pre-registered in NOTES_gravity.md): the static all-orders N-design at field level (nonlinear lapse vs the
exact isotropic Schwarzschild lapse) plus clocks reading A; MECHANISM source (prescribed static density gear n).

Usage (repository root): OMP_NUM_THREADS=1 nice -n 10 python universe24/demos/gravity/d3_ndesign.py
Writes runs/demos/gravity/D3.json.
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


def main(L=48, T=60, M_target=1.0, Rl=2.0):
    started = stamp()
    P, k = 2 ** 12, 80
    Q = gr.gravity_Q(P, k)
    clocks = [gr.atom_spec("at", 2 * P * 24)]
    blocks = [gr.build_test_matter(m, Q=Q) for m in clocks] + \
        [gr.build_ndesign(Q=Q, P=P, k=k, sigma0=1, w_a2=Q - 1, w_c=7 * (Q - 1) // 10, w_lam=(Q - 1) // 2,
                          clocks=clocks, lights=[])]
    Tn = compose(*blocks)
    eng = Engine(Tn, Q)
    s = vacuum_state(Tn, Q, L, *blocks)
    c = (L // 2,) * 3
    # density lump: n_phys = sigma0 n / (8 pi k P); sum n_phys ~ M (weak-field estimate)
    gn = Tn.gear_index("nd.n")
    xyz = s.lattice.all_coords()
    d2 = ((xyz - np.array(c)) ** 2).sum(axis=1)
    prof = np.exp(-d2 / (2 * Rl * Rl))
    n0 = M_target * 8 * math.pi * k * P / prof.sum()
    a, b, r = s.a.astype(OBJ), s.b.astype(OBJ), s.r.astype(OBJ)
    nvals = np.array([int(round(n0 * p)) for p in prof], dtype=object)
    a[gn], b[gn] = nvals.copy(), nvals.copy()
    s = State(L, a, b, r)
    atpos = {r_: (c[0] + r_, c[1], c[2]) for r_ in (6, 10)}
    s = pg.with_clocks(s, Tn, "at.c", Q, 2 * P * 24, list(atpos.values()), 2 ** 10)
    g_at = Tn.gear_index("at.c")
    sub = Tensor([Tn.gears[g_at]], [])
    series = {n: ([], []) for n in (s.lattice.index(*p) for p in atpos.values())}
    gnu = Tn.gear_index("nd.nu")
    hist_nu = []
    t0 = time.time()
    for t in range(T):
        s1 = eng.step(s)
        lg = extract_clicks(sub, eng.D, State._raw(L, s.a[[g_at]], s.b[[g_at]], s.r[[g_at]]),
                            State._raw(L, s1.a[[g_at]], s1.b[[g_at]], s1.r[[g_at]]), step=t)
        for n, q in zip(lg.node, lg.quotient):
            if int(n) in series:
                series[int(n)][0].append(t)
                series[int(n)][1].append(int(q))
        if t >= T - 10:
            hist_nu.append(s1.b[gnu].astype(float).reshape(L, L, L))
        s = s1
    nu = np.mean(hist_nu, axis=0)
    rs = np.arange(3, 15)
    Nax = np.array([1 + nu[c[0] + r_, c[1], c[2]] / P for r_ in rs])
    Ndg = [1 + nu[c[0] + d, c[1] + d, c[2] + d] / P for d in (3, 4, 5)]
    fit = (rs >= 6) & (rs <= 10)

    def iso(M, r_):
        return (1 - M / (2 * r_)) / (1 + M / (2 * r_))
    # fit M (exact isotropic) by bisection on the mean residual over r = 6..10; and linear 1 - M/r
    Ms = np.linspace(0.05, 3.0, 5901)
    err_iso = [np.max(np.abs(iso(M, rs[fit]) - Nax[fit])) for M in Ms]
    Miso = float(Ms[int(np.argmin(err_iso))])
    err_lin = [np.max(np.abs(1 - M / rs[fit] - Nax[fit])) for M in Ms]
    Mlin = float(Ms[int(np.argmin(err_lin))])
    clocks_out = {}
    for r_, p in atpos.items():
        n = s.lattice.index(*p)
        ts, qs = series[n]
        w = og.rate_from_crossings(og.crossing_times(ts[20:], qs[20:]))
        w0 = math.acos(1 - 2 * P * 24 / (6 * Q))
        Nclick = math.sin(w / 2) / math.sin(w0 / 2)
        Nev = 1 + nu[p] / P
        clocks_out[f"r{r_}"] = {"N_click(half-angle)": Nclick, "N_event": float(Nev),
                                "N_click/N_event-1": Nclick / float(Nev) - 1}
    out = {"started": started, "L": L, "T": T, "P": P, "k": k, "Q": Q, "lump_R": Rl, "n0": n0,
           "elapsed_s": time.time() - t0, "N_axis": {int(r_): float(v) for r_, v in zip(rs, Nax)},
           "N_diag_d3_4_5": [float(v) for v in Ndg], "N_min_axis": float(Nax.min()),
           "M_fit_isotropic": Miso, "max_dev_isotropic_r6_10": float(min(err_iso)),
           "M_fit_linear": Mlin, "max_dev_linear_r6_10": float(min(err_lin)),
           "isotropic_minus_board": {int(r_): float(iso(Miso, r_) - v) for r_, v in zip(rs, Nax)},
           "clocks": clocks_out, "engine_stats": dict(eng.stats), "written_utc": stamp()}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "D3.json").write_text(json.dumps(out, indent=1, default=str) + "\n")
    print(json.dumps({k_: out[k_] for k_ in ("M_fit_isotropic", "max_dev_isotropic_r6_10", "M_fit_linear",
                                             "max_dev_linear_r6_10", "N_min_axis", "clocks")}, indent=1))


if __name__ == "__main__":
    main()
