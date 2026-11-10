"""GRAV-FIX T1/T2/T3/T4 runner (pre-registered in NOTES_gravity.md): the v2 default + S2* (A = 2^16, L = 6) with the
default beta or a detuned beta (layers/gravity_beta_fix.py), R-a background 0 or the two-time datum
(prepare/gravity_ra.py). Passive readouts every `every` updates: U_mean, corner projections |G_pi|, |F_pi|, max|G|,
max bit length per namespace. Usage: python gfix_mech.py VARIANT(default|A|B) BG(zero|twotime) T EVERY TAG"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))

import numpy as np

from research.metric_variant_v1.core import Engine, compose
from research.metric_variant_v1.core.engine import OBJ
from research.metric_variant_v1.layers.gravity_beta_fix import build_beta_detuned, replace_beta
from research.metric_variant_v1.layers.system import default_system
from research.metric_variant_v1.prepare.gravity_ra import ra_two_time
from research.metric_variant_v1.prepare.seed import ra_background, s2_star
from research.metric_variant_v1.prepare.system import system_vacuum

OUT = ROOT / "research/metric_variant_v1/results/gravity"


def stamp():
    return subprocess.run(["date", "-u"], capture_output=True, text=True).stdout.strip()


def main(variant="default", bg="zero", T=700, every=50, tag="GFIX", L=6, A=1 << 16):
    started = stamp()
    S = default_system()
    Q, P, k = S.Q, S.info["P"], S.info["k"]
    blocks = S.blocks
    if variant in ("A", "B"):
        num, den = (1, 2) if variant == "A" else (3, 4)
        blocks = replace_beta(blocks, build_beta_detuned(Q=Q, P=P, k=k, field=S.info["lapse_field"], num=num,
                                                         den=den))
    Tn = compose(*blocks)
    eng = Engine(Tn, Q)
    vac = system_vacuum(S, Tn, L)
    s = s2_star(vac, Tn, (0, 0, 0), A)
    ra_info = None
    if bg == "zero":
        s = ra_background(s, Tn, 0)
    else:
        s, ra_info = ra_two_time(eng, s)
    ns = [n.split(".", 1)[0] for n in Tn.names]
    rows_ns = {kk: np.array([i for i, n in enumerate(ns) if n == kk]) for kk in sorted(set(ns))}
    gF, gG = Tn.gear_index("metric.h00"), Tn.gear_index("beta.G")
    xyz = s.lattice.all_coords()
    sign = np.where((xyz.sum(axis=1) % 2) == 0, 1, -1).astype(object)
    rows = []
    t0 = time.time()
    horizon = None
    for t in range(1, T + 1):
        s = eng.step(s)
        if t % every == 0:
            b = s.b.astype(OBJ)
            F, G = b[gF], b[gG]
            bits = {kk: max(abs(int(b[r].max())), abs(int(b[r].min()))).bit_length() for kk, r in rows_ns.items()}
            row = {"t": t, "U_mean": float(sum(int(v) for v in F) / len(F) / (2 * P)),
                   "G_pi": abs(int(sum(G * sign))) / len(G), "F_pi": abs(int(sum(F * sign))) / len(F),
                   "maxG": max(abs(int(G.max())), abs(int(G.min()))), "maxF": max(abs(int(F.max())), abs(int(F.min()))),
                   "bits": {kk: v for kk, v in bits.items() if v}, "pyint": eng.stats["pyint_steps"],
                   "elapsed": round(time.time() - t0, 1)}
            rows.append(row)
            print(json.dumps(row), flush=True)
            if max(bits.values()) > 60:
                horizon = t
                break
    out = {"started": started, "variant": variant, "bg": bg, "T": T, "L": L, "A": A, "Q": Q, "P": P, "k": k,
           "ra": ra_info, "horizon_first_gt60bits": horizon, "rows": rows, "written_utc": stamp()}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{tag}.json").write_text(json.dumps(out, indent=1, default=str) + "\n")


if __name__ == "__main__":
    a = sys.argv[1:]
    main(a[0], a[1], int(a[2]), int(a[3]), a[4])
