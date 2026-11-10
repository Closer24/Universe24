"""Weak-field rounding-lock check of the default mass (pre-registered in NOTES_system.md, "PRE-REGISTRATION LOCK").
Method of R-P1's review/phys1/stage1em/p1e_weakfield_lock.py (own script, default parameters at Q = 2^33 + 1).
Run: OMP_NUM_THREADS=1 nice -n 10 python -m universe24.demos.system.mass_lock_check
Writes results/system/mass_lock.json."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from ...core import Engine, compose
from ...layers import matter as LM
from ...layers.em import build_em
from ...layers.matter import build_matter, matter_names
from ...layers.system import HOP, MASS_DEFAULT, Q_DEFAULT, WILSON
from ...prepare import vacuum_state, with_gears

Q = Q_DEFAULT
D = 6 * Q
G_PHI = 4
OUT = Path(__file__).resolve().parents[2] / "results" / "system"


def joint_vec():
    W0, V = LM.W016, LM.V16
    for i in range(16):
        e = np.zeros(16, dtype=np.int64)
        e[i] = 1
        for sw in (1, -1):
            for sv in (1, -1):
                v = (e + sw * (W0 @ e))
                v = v + sv * (V @ v)
                if np.any(v):
                    return v, sw, sv
    raise RuntimeError


def run(mass, Am, Phi0, T=3000, L=3):
    m = build_matter(Q=Q, hop=HOP, mass=mass, wilson=WILSON)
    e = build_em(Q=Q, matter=m, g_phi=G_PHI, g_A=1, sigma=0)
    Tn = compose(m, e)
    E = Engine(Tn, Q)
    s = vacuum_state(Tn, Q, L, m, e)
    v, sw, sv = joint_vec()
    names = matter_names("pair")
    vals = {}
    for x in range(L):
        for y in range(L):
            for z in range(L):
                for i, vi in enumerate(v):
                    if vi:
                        vals[(f"matter.{names[i]}", (x, y, z))] = (0, int(Am * vi), 3 * Q - 1)
                vals[("em.Phi", (x, y, z))] = (Phi0, Phi0, 3 * Q - 1)
    s = with_gears(s, Tn, vals)
    mi = [Tn.gear_index(f"matter.{n}") for n in names]
    pi = Tn.gear_index("em.Phi")
    p, static = [], True
    for t in range(T):
        p.append(float(np.dot(v, s.b[mi, 0].astype(float))))
        s = E.step(s)
        if t % 500 == 0 and not (np.all(s.b[pi] == Phi0) and np.all(s.a[pi] == Phi0)):
            static = False
    p = np.array(p)
    return float(np.sum(p[1:-1] * (p[2:] + p[:-2])) / (2 * np.sum(p[1:-1] ** 2))), sw, sv, static


def main():
    rows = []
    for label, mass in (("MASS_DEFAULT 4915*2^22", MASS_DEFAULT), ("3Q control", 3 * Q)):
        Am = 1 << 20
        c0, sw, sv, _ = run(mass, Am, 0)
        for Phi0 in (256, 3072, 6144):
            c1, sw, sv, st = run(mass, Am, Phi0)
            pred = 2 * G_PHI * Phi0 * sv / D
            rows.append({"mass": label, "cos_w0_meas": c0, "W0_eig": sw, "V_eig": sv, "Phi0": Phi0,
                         "shift_quanta_per_update": 2 * 2 * G_PHI * Phi0 * Am / D, "dcos_meas": c1 - c0,
                         "dcos_pred": pred, "ratio": (c1 - c0) / pred, "Phi_static": st})
            print(rows[-1], flush=True)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "mass_lock.json").write_text(json.dumps({"rows": rows}, indent=1))


if __name__ == "__main__":
    main()
