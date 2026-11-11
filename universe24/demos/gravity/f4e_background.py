"""F4d (pre-registered in NOTES_gravity.md): the WAVE lapse with R-a realised as a prescribed background gear
(u_F += -b_B, B holding the declared uniform k = 0 value Ebar) plus the k = 0 offset; self-consistent reciprocal load and
noisy light. Usage: OMP_NUM_THREADS=1 nice -n 10 python universe24/demos/gravity/f4d_background.py"""
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

from universe24.core import Block, Engine, GearType, compose
from universe24.core.engine import OBJ, State
from universe24.core.reversors import reversor_check, uniform
from universe24.layers import gravity as gr
from universe24.observe import gravity as og
from universe24.prepare import gravity as pg
from universe24.prepare import vacuum_state

OUT = Path("runs/demos/gravity")
RA_WHY = ("R-a: the declared uniform k = 0 background (-kappa E/N per node, Study 6 D(d)) as a prescribed static gear "
          "B feeding -b_B into the lapse field; B holds its value and does not feel F (data, one-way)")


def stamp():
    return subprocess.run(["date", "-u"], capture_output=True, text=True).stdout.strip()


def main(L=32, T=700, U3=0.005, seed=7, tag="F4e"):
    started = stamp()
    P, k = 2 ** 20, 24
    Q = gr.gravity_Q(P, k)
    c = (L // 2,) * 3
    load = gr.load_pair_spec("load", 2 * P * 3)
    light = gr.light_spec("light", Q)
    bgk = Block((GearType("B", "audit"),),
                tuple(gr.gradient_terms(gr.wave_potential("B", 0, 6 * Q))) +
                (("metric.h00", -1, (("bgk.B", (0, 0, 0), "b"),), {"designated_one_way": RA_WHY}),),
                name="bgk", vacuum={"B": 3 * Q - 1}, Q=Q)
    blocks = [gr.build_metric(Q=Q, components=("h00",)), gr.build_test_matter(load, Q=Q),
              gr.build_test_matter(light, Q=Q), gr.build_lapse(Q=Q, P=P, field="metric.h00", matters=[load, light]),
              bgk]
    Tn = compose(*blocks)
    eng = Engine(Tn, Q)
    s = vacuum_state(Tn, Q, L, *blocks)
    R = 2.5
    prof = sum((1 - (d / (R + 1)) ** 2) ** 2 for _, d in pg.ball(L, c, R))
    amp = int(math.sqrt(U3 * 8 * math.pi * P * (Q - 1) * 3 / (3 * prof)))
    s = pg.with_load(s, Tn, "load", Q, 2 * P * 3, c, R, amp)
    rng = np.random.default_rng(seed)
    a, b, r = s.a.astype(OBJ), s.b.astype(OBJ), s.r.astype(OBJ)
    gl = Tn.gear_index("light.L")
    a[gl] = np.array([int(v) for v in rng.integers(-256, 257, L ** 3)], dtype=object)
    b[gl] = np.array([int(v) for v in rng.integers(-256, 257, L ** 3)], dtype=object)
    s = State(L, a, b, r)
    src = og.sources(eng, s, ["metric.h00"])["metric.h00"]       # the matter source (B still 0)
    S = int(src.sum())
    N = L ** 3
    Ebar, res = divmod(S, N)
    Bv = np.array([Ebar + (1 if n < res else 0) for n in range(N)], dtype=object)
    a, b, r = s.a.astype(OBJ), s.b.astype(OBJ), s.r.astype(OBJ)
    gB = Tn.gear_index("bgk.B")
    a[gB], b[gB] = Bv.copy(), Bv.copy()
    s = State(L, a, b, r)
    Fs = pg.static_field(L, Q, src)
    C0 = -min(Fs.reshape(-1))
    s = pg.with_field(s, Tn, "metric.h00", Fs + C0)
    s_prep = s
    gF = Tn.gear_index("metric.h00")
    meanU0 = int(sum(int(v) for v in s.b[gF])) / N / (2 * P)
    l0 = int(np.max(np.abs(s.b[gl].astype(np.int64))))
    rows = []
    t0 = time.time()
    for t in range(1, T + 1):
        s = eng.step(s)
        if t % 10 == 0:
            if s.max_abs().bit_length() > 60:
                rows.append({"t": t, "exploded": True})
                break
            h = s.b[gF]
            rows.append({"t": t, "meanU-meanU0": int(sum(int(v) for v in h)) / N / (2 * P) - meanU0,
                         "minU": int(h.min()) / (2 * P), "maxU": int(h.max()) / (2 * P),
                         "max|light|": int(np.max(np.abs(s.b[gl].astype(np.int64))))})
    good = [x for x in rows if "minU" in x]
    mir = reversor_check(uniform(Tn, Q, "Mp"), eng, [s_prep], 10)
    out = {"started": started, "Q": Q, "P": P, "L": L, "T": T, "S": S, "Ebar": Ebar, "residue": res,
           "C0/(2P)": C0 / (2 * P), "max|meanU drift|": max(abs(x["meanU-meanU0"]) for x in good),
           "minU_over_run": min(x["minU"] for x in good), "maxU_over_run": max(x["maxU"] for x in good),
           "light_growth_max": max(x["max|light|"] for x in good) / l0,
           "exploded_at": next((x["t"] for x in rows if x.get("exploded")), None),
           "mirror_Mp_n10": mir, "rows_every_100": [x for x in rows if x["t"] % 100 == 0],
           "elapsed_s": time.time() - t0, "written_utc": stamp()}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{tag}.json").write_text(json.dumps(out, indent=1, default=str) + "\n")
    print(json.dumps({k_: v for k_, v in out.items() if k_ != "rows_every_100"}, indent=1, default=str))


if __name__ == "__main__":
    main()
