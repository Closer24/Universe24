"""F4b (pre-registered in NOTES_gravity.md): F4 re-run on the OD2 board with BOTH closed-board data:
R-a (the mean-subtracted Hamiltonian constraint: the k = 0 part of the source is the declared uniform background) and
the k = 0 constant of the potential (C0 = -min F_s: U >= 0, N <= 1). h00 is the OD2 rounding-free accumulator, so
Sum_x h00 is exactly frozen. Self-consistent first-order matter (stress -> hij -> h0i -> h00) with noise, headroom light
with noise, a clock-pair load; light and load read b(h00) one-way (designated test reads).

Usage: OMP_NUM_THREADS=1 nice -n 10 python universe24/demos/gravity/f4b_background.py
Writes results/gravity/F4b.json.
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

from universe24.core import Block, Engine, compose
from universe24.core.engine import OBJ, State
from universe24.layers import gravity as gr
from universe24.observe import gravity as og
from universe24.prepare import gravity as pg
from universe24.prepare import vacuum_state

OUT = ROOT / "universe24/results/gravity"
WHY = ("F4b test read of the OD2 accumulator lapse b(h00) (one-way: the accumulator stays rounding-free; the energy "
       "enters through the prepared Hamiltonian-constraint data R-a and the stress chain)")


def stamp():
    return subprocess.run(["date", "-u"], capture_output=True, text=True).stdout.strip()


def oneway_read(Q, P, spec, field):
    spec = gr._resolve_carriers(spec, Q)
    pot = gr.lapse_potential(field, P, [spec], "GR")
    terms = gr.gradient_terms(pot, only=[spec.q(g) for g in spec.gears], designation=WHY, what="f4b read")
    return Block((), tuple(terms), name=f"read_{spec.name}", Q=Q)


def main(L=32, T=700, U3=0.02, seed=11, kappa=2, whi=16, tag="F4b"):
    started = stamp()
    P, k = 2 ** 20, 24
    Q = gr.gravity_Q(P, k)
    c = (L // 2,) * 3
    w = gr.weyl_spec("dir", s=4 * P * 8, m=4 * P * 4, wilson=4 * P)
    light = gr.light_spec("light", Q)
    load = gr.load_pair_spec("load", 2 * P * 3)
    blocks = [gr.build_od2(Q=Q, stress=(gr.od2_hop_stress("dir", w, kappa=kappa) if kappa else ()),
                           reads=gr.od2_centred_lapse_read("od2", w, P, Q, g00=1))] + \
        [gr.build_test_matter(m, Q=Q) for m in (w, light, load)] + \
        [oneway_read(Q, P, light, "od2.h00"), oneway_read(Q, P, load, "od2.h00")]
    Tn = compose(*blocks)
    eng = Engine(Tn, Q)
    s = vacuum_state(Tn, Q, L, *blocks)
    R = 2.5
    prof = sum((1 - (d / (R + 1)) ** 2) ** 2 for _, d in pg.ball(L, c, R))
    amp = int(math.sqrt(U3 * 8 * math.pi * P * (Q - 1) * 3 / (3 * prof)))
    s = pg.with_load(s, Tn, "load", Q, 2 * P * 3, c, R, amp)
    rng = np.random.default_rng(seed)
    a, b, r = s.a.astype(OBJ), s.b.astype(OBJ), s.r.astype(OBJ)
    for gname, hi in (("light.L", 256), ("dir.X", whi), ("dir.Y", whi)):
        g = Tn.gear_index(gname)
        a[g] = np.array([int(v) for v in rng.integers(-hi, hi + 1, L ** 3)], dtype=object)
        b[g] = np.array([int(v) for v in rng.integers(-hi, hi + 1, L ** 3)], dtype=object)
    s = State(L, a, b, r)
    src = pg.load_source(s, Tn, "load", 2 * P * 3, P)          # T^00 of the load in the lapse-source units
    Fs = pg.static_field(L, Q, src)                              # R-a: mean-subtracted Poisson solution
    C0 = -min(Fs.reshape(-1))
    s = pg.with_field(s, Tn, "od2.h00", Fs + C0)
    gh = Tn.gear_index("od2.h00")
    gl, gx, gy = Tn.gear_index("light.L"), Tn.gear_index("dir.X"), Tn.gear_index("dir.Y")
    sum0 = int(sum(int(v) for v in s.b[gh]))
    l0 = int(np.max(np.abs(s.b[gl].astype(np.int64))))
    w0 = max(int(np.max(np.abs(s.b[gx].astype(np.int64)))), int(np.max(np.abs(s.b[gy].astype(np.int64)))))
    rows = []
    t0 = time.time()
    sum_ok = True
    for t in range(1, T + 1):
        s = eng.step(s)
        if t % 10 == 0:
            bits = s.max_abs().bit_length()
            if bits > 60:
                rows.append({"t": t, "exploded": True, "bits": bits})
                break
            h = s.b[gh]
            sm = int(sum(int(v) for v in h))
            sum_ok &= (sm == sum0)
            rows.append({"t": t, "sum_h00": sm, "minU": int(h.min()) / (2 * P), "maxU": int(h.max()) / (2 * P),
                         "max|light|": int(np.max(np.abs(s.b[gl].astype(np.int64)))),
                         "max|weyl|": max(int(np.max(np.abs(s.b[gx].astype(np.int64)))),
                                          int(np.max(np.abs(s.b[gy].astype(np.int64))))), "bits": bits})
    good = [x for x in rows if "minU" in x]
    out = {"started": started, "L": L, "T": T, "U3": U3, "Q": Q, "P": P, "C0/(2P)": C0 / (2 * P),
           "sum_h00_initial": sum0, "sum_h00_constant_every_sample": sum_ok,
           "minU_over_run": min(x["minU"] for x in good), "maxU_over_run": max(x["maxU"] for x in good),
           "light_growth_max": max(x["max|light|"] for x in good) / l0,
           "weyl_growth_max": max(x["max|weyl|"] for x in good) / w0,
           "exploded_at": next((x["t"] for x in rows if x.get("exploded")), None),
           "rows_every_100": [x for x in rows if x["t"] % 100 == 0], "elapsed_s": time.time() - t0,
           "written_utc": stamp()}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{tag}.json").write_text(json.dumps(out, indent=1, default=str) + "\n")
    print(json.dumps({k_: v for k_, v in out.items() if k_ != "rows_every_100"}, indent=1, default=str))


if __name__ == "__main__":
    main(kappa=int(sys.argv[1]), whi=int(sys.argv[2]), tag=sys.argv[3]) if len(sys.argv) > 1 else main()
