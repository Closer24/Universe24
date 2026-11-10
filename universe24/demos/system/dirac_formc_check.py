"""DIRAC-C exploratory check (pre-registered in NOTES_system.md, "PRE-REGISTRATION DIRAC-C"): the C3 universality setup
of tests/test_l0c.py with the matter lapse in the Wilson difference form (layers/matter_lapse_c.py, PROPOSAL).
Run: OMP_NUM_THREADS=1 nice -n 10 python -m universe24.demos.system.dirac_formc_check
Writes results/system/DIRAC_C.json."""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

from ...core.engine import OBJ, Engine, State
from ...core.reciprocity import check_reciprocity
from ...core.tensor import Block, GearType, compose
from ...layers import gravity as gr
from ...layers.gravity_l0c import build_l0c, build_l0c_lapse
from ...layers.matter import algebra, build_matter, matter_names
from ...layers.matter_lapse_c import build_matter_lapse_c
from ...layers.system import HOP, MASS_DEFAULT, P_GRAV, Q_DEFAULT, WILSON
from ...observe import gravity as og
from ...prepare import vacuum_state
from ...tests.test_l0c import AMP, L, T_RUN, U0_TARGET, bands

Q, P, D = Q_DEFAULT, P_GRAV, 6 * Q_DEFAULT
OUT = Path(__file__).resolve().parents[2] / "results" / "system"


def run(bs, mu, v, F0):
    bg = Block((GearType("F", "audit"),), tuple(gr.gradient_terms(gr.wave_potential("F", 0, 6 * Q))), name="bg",
               vacuum={"F": 3 * Q - 1}, Q=Q)
    l0 = build_l0c(Q=Q, body_signs=bs, name="ref")
    lap = build_l0c_lapse(Q=Q, P=P, field="bg.F", body_signs=bs, oneway=True, name="lapseL0")
    m = build_matter(Q=Q, hop=HOP, mass=MASS_DEFAULT, wilson=WILSON, species="pair", name="matter")
    mlc = build_matter_lapse_c(Q=Q, P=P, field="bg.F", matter=m, oneway=True)
    blocks = [l0, bg, lap, m, mlc]
    Tn = compose(*blocks)
    eng = Engine(Tn, Q)
    s = vacuum_state(Tn, Q, L, *blocks)
    a, b, r = s.a.astype(OBJ), s.b.astype(OBJ), s.r.astype(OBJ)
    N = L ** 3
    gF = Tn.gear_index("bg.F")
    a[gF] = np.full(N, F0, dtype=object)
    b[gF] = np.full(N, F0, dtype=object)
    vv = v / np.max(np.abs(v))
    c0 = 1 - (Q - 1) * mu / (6 * Q)
    for h in range(48):
        g = Tn.gear_index(f"ref.R{h:02d}")
        b[g] = np.full(N, int(round(AMP * vv[h])), dtype=object)
        a[g] = np.full(N, int(round(AMP * vv[h] * c0)), dtype=object)
    W0 = algebra("pair")["W0"].astype(float)
    wv, wvec = np.linalg.eigh(W0)
    vm = wvec[:, int(np.argmax(wv))]
    vm = vm / np.max(np.abs(vm))
    mn = matter_names("pair")
    for i in range(16):
        g = Tn.gear_index(f"matter.{mn[i]}")
        b[g] = np.full(N, int(round(AMP * vm[i])), dtype=object)
        a[g] = np.full(N, int(round(AMP * vm[i] * MASS_DEFAULT / D)), dtype=object)
    s = State(L, a, b, r)
    gl = Tn.gear_index(f"ref.R{int(np.argmax(np.abs(vv))):02d}")
    gm = Tn.gear_index(f"matter.{mn[int(np.argmax(np.abs(vm)))]}")
    ser = {"L0": ([], []), "dirac": ([], [])}
    for t in range(T_RUN):
        s1 = eng.step(s)
        for key, g in (("L0", gl), ("dirac", gm)):
            q = int(s1.b[g, 0]) + int(s.a[g, 0])
            if q != 0:
                ser[key][0].append(t)
                ser[key][1].append(q)
        s = s1
    return {k: og.rate_from_crossings(og.crossing_times(*ser[k])) for k in ser}


def main():
    F0 = int(round(2 * P * U0_TARGET))
    U0 = F0 / (2 * P)
    out = {"U0": U0, "rows": []}
    m = build_matter(Q=Q, hop=HOP, mass=MASS_DEFAULT, wilson=WILSON, species="pair", name="matter")
    bg = Block((GearType("F", "audit"),), tuple(gr.gradient_terms(gr.wave_potential("F", 0, 6 * Q))), name="bg",
               vacuum={"F": 3 * Q - 1}, Q=Q)
    rep = check_reciprocity(compose(m, bg, build_matter_lapse_c(Q=Q, P=P, field="bg.F", matter=m, oneway=False)))
    out["reciprocal_block"] = {"ok": rep.ok, "checked": rep.checked, "designated": len(rep.designated)}
    for name, bs in (("pmp", (1, -1, 1)), ("ppp", (1, 1, 1))):
        mu, v = [bv for bv in bands(bs) if abs(bv[0] - 2.0) < 1e-6][0]
        w0, w1 = run(bs, mu, v, 0), run(bs, mu, v, F0)
        NL = math.sin(w1["L0"] / 2) / math.sin(w0["L0"] / 2)
        Nd = math.cos(w1["dirac"]) / math.cos(w0["dirac"])
        row = {"class": name, "mu": mu, "N_L0": NL, "N_dirac_demod": Nd, "dev_dirac_vs_1-U0": Nd / (1 - U0) - 1,
               "gap": NL - Nd, "pass": abs(Nd - (1 - U0)) <= 1e-4 and abs(NL - Nd) <= U0 ** 2 / 2 + 1e-4,
               "N_dirac_half_angle": math.sin(w1["dirac"] / 2) / math.sin(w0["dirac"] / 2)}
        out["rows"].append(row)
        print(row, flush=True)
    print(out["reciprocal_block"])
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "DIRAC_C.json").write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
