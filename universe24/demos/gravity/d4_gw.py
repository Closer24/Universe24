"""Demo D4 (pre-registered in NOTES_gravity.md): gravitational waves of the spatial metric gears from an oscillating
quadrupole stress (MECHANISM: prescribed oscillator source, the 0mu components omitted; their 1/R parts are gauge).
Two TT polarizations, front speed vs c_Q (fraction-of-peak arrival; taxicab |x|_1 bound reported), 1/R decay.

Usage (repository root): OMP_NUM_THREADS=1 nice -n 10 python universe24/demos/gravity/d4_gw.py
Writes results/gravity/D4.json.
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

from universe24.core import Block, Engine, GearType, compose
from universe24.core.engine import OBJ, State
from universe24.layers import gravity as gr
from universe24.prepare import vacuum_state

OUT = ROOT / "universe24/results/gravity"
WHY = "MECHANISM: prescribed oscillating quadrupole stress (GW demo D4)"


def stamp():
    return subprocess.run(["date", "-u"], capture_output=True, text=True).stdout.strip()


def build(Q, mu, kappa, rotating):
    comps = ("hxx", "hyy", "hzz", "hxy", "hxz", "hyz")
    met = gr.build_metric(Q=Q, components=comps)
    osc = gr.build_test_matter(gr.MatterSpec("osc", ("O1", "O2"), 2, {}, {("O1", "O1"): -mu, ("O2", "O2"): -mu},
                                             {}, (), "audit"), Q=Q)
    o = (0, 0, 0)
    terms = [("metric.hxx", kappa, (("osc.O1", o, "b"),), {"designated_one_way": WHY}),
             ("metric.hyy", -kappa, (("osc.O1", o, "b"),), {"designated_one_way": WHY})]
    if rotating:
        terms.append(("metric.hxy", kappa, (("osc.O2", o, "b"),), {"designated_one_way": WHY}))
    src = Block((), tuple(terms), name="gwsrc", Q=Q)
    return [met, osc, src]


def run(rotating, L=64, T=96):
    Q = gr.gravity_Q(2 ** 10, 4)
    w0 = 0.35
    mu = int(round(6 * Q * (1 - math.cos(w0))))
    w0 = math.acos(1 - mu / (6 * Q))
    blocks = build(Q, mu, 2 ** 8, rotating)
    Tn = compose(*blocks)
    eng = Engine(Tn, Q)
    s = vacuum_state(Tn, Q, L, *blocks)
    c = (L // 2,) * 3
    n0 = s.lattice.index(*c)
    a, b, r = s.a.astype(OBJ), s.b.astype(OBJ), s.r.astype(OBJ)
    A = 2 ** 20
    g1, g2 = Tn.gear_index("osc.O1"), Tn.gear_index("osc.O2")
    a[g1, n0], b[g1, n0] = int(round(A * math.cos(-w0))), A
    a[g2, n0], b[g2, n0] = int(round(A * math.sin(-w0))), 0
    s = State(L, a, b, r)
    Rs = (6, 9, 12, 15, 18, 21, 24)
    probes = {f"z{R}": (c[0], c[1], c[2] + R) for R in Rs}
    probes.update({f"x{R}": (c[0] + R, c[1], c[2]) for R in Rs})
    probes.update({f"d{R}": (c[0] + round(R / math.sqrt(3)),) * 3 for R in (9, 15)})
    idx = {k: s.lattice.index(*p) for k, p in probes.items()}
    gi = {n: Tn.gear_index(f"metric.{n}") for n in ("hxx", "hyy", "hzz", "hxy", "hxz", "hyz")}
    rec = {k: {n: [] for n in gi} for k in probes}
    for t in range(T):
        s = eng.step(s)
        for k, n in idx.items():
            for nm, g in gi.items():
                rec[k][nm].append(int(s.b[g, n]))
    return rec, {"Q": Q, "w0": w0, "mu": mu, "L": L, "T": T, "c_Q": math.sqrt((Q - 1) / (3 * Q))}


def analyse(rec, meta):
    T = meta["T"]
    out = {}
    cQ = meta["c_Q"]
    for k, d in rec.items():
        R = int(k[1:]) if k[0] in "xz" else None
        if k[0] == "z":
            hp = [(x - y) / 2 for x, y in zip(d["hxx"], d["hyy"])]
            hc = d["hxy"]
        elif k[0] == "x":
            hp = [(x - y) / 2 for x, y in zip(d["hyy"], d["hzz"])]
            hc = d["hyz"]
        else:
            continue
        peak = max(abs(v) for v in hp) or 1
        t_arr = next((t for t, v in enumerate(hp) if abs(v) >= 0.1 * peak), None)
        # late window after the arrival: one source period ~ 2 pi / w0
        win = slice(t_arr + 8 if t_arr is not None else 0, T)
        amp_p = max((abs(v) for v in hp[win]), default=0)
        amp_c = max((abs(v) for v in hc[win]), default=0)
        lo = (t_arr if t_arr is not None else 0) + 10
        seg = hp[lo:lo + 36]
        amp_rms = math.sqrt(2 * sum(v * v for v in seg) / len(seg)) if seg and len(seg) == 36 else None
        out[k] = {"R": R, "arrival_10pct": t_arr, "amp_plus": amp_p, "amp_cross": amp_c,
                  "R*amp_plus": R * amp_p if R else None, "amp_rms2": amp_rms,
                  "R*amp_rms2": R * amp_rms if (R and amp_rms) else None}
    return out


def main():
    started = stamp()
    t0 = time.time()
    res = {}
    for rot in (False, True):
        rec, meta = run(rot)
        res["rotating" if rot else "linear"] = analyse(rec, meta)
    res["meta"] = meta
    # front speed: fit arrival vs R on the z axis (linear source)
    lin = res["linear"]
    pts = [(v["R"], v["arrival_10pct"]) for k, v in lin.items() if k.startswith("z") and v["arrival_10pct"]]
    R_ = np.array([p[0] for p in pts], float)
    t_ = np.array([p[1] for p in pts], float)
    slope = float(np.polyfit(R_, t_, 1)[0])
    res["front_speed_fit"] = 1 / slope
    res["c_Q"] = meta["c_Q"]
    res["taxicab_bound_speed_axis"] = 1.0
    zz = [(v["R"], v["R*amp_plus"]) for k, v in lin.items() if k.startswith("z")]
    res["R_times_amp_plus_z"] = zz
    res["R_times_amp_rms2_z"] = [(v["R"], v["R*amp_rms2"]) for k, v in lin.items() if k.startswith("z")]
    res["cross_over_plus_linear_z"] = {k: v["amp_cross"] / v["amp_plus"] for k, v in lin.items()
                                        if k.startswith("z") and v["amp_plus"]}
    rot = res["rotating"]
    res["cross_over_plus_rotating_z"] = {k: v["amp_cross"] / v["amp_plus"] for k, v in rot.items()
                                          if k.startswith("z") and v["amp_plus"]}
    res["elapsed_s"] = time.time() - t0
    res["started"] = started
    res["written_utc"] = stamp()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / ("D4b.json" if len(sys.argv) > 1 else "D4.json")).write_text(json.dumps(res, indent=1, default=str) + "\n")
    print(json.dumps({k: res[k] for k in ("front_speed_fit", "c_Q", "R_times_amp_plus_z", "R_times_amp_rms2_z",
                                          "cross_over_plus_linear_z", "cross_over_plus_rotating_z")}, indent=1))


if __name__ == "__main__":
    main()
