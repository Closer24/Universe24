"""FORM C clock test (pre-registered in NOTES_system.md, "PRE-REGISTRATION v2 DEFAULT", FORM C TEST C2/C3; R1 + R2
re-registration "PRE-REGISTRATION R1 + R2": the default's own matter lapse (Wilson in difference form) and the OWN-FRAME
tick reading of observe/readout.py).

L0 clocks read from L0 CLICKS (sign changes of the click size l = b' + a of one L0 gear, interpolated crossings;
observe.gravity.crossing_times / rate_from_crossings, as B1-GRAV's L0-EP) under a uniform static prescribed lapse gear
F = 2P U0 (read ONE-WAY, designated), against the F = 0 twin, on EVERY massive band at k = 0 of both sign classes.
Contrast: B1-GRAV's site/hop split (build_l0_weight + build_l0_lapse) on the same modes. Universality: the default
Dirac matter's rest clock under B1-GRAV's matter lapse reading the same F (demodulated pi/2 law cos w = N cos w0).
Run from the repository root:
    OMP_NUM_THREADS=1 nice -n 10 python -m unittest universe24.tests.test_l0c -v
Writes results/system/L0C_clock.json. C1/C4 (reciprocity, vacuum, rewind, mirror) are X3-X7 of tests/test_system.py.
"""
from __future__ import annotations

import json
import math
import time
import unittest
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from ..core.engine import OBJ, Engine, State
from ..core.tensor import Block, GearType, compose
from ..layers import gravity as gr
from ..layers.gravity_l0 import build_l0_lapse, build_l0_weight
from ..layers.gravity_l0c import build_l0c, build_l0c_lapse, m0_matrix
from ..layers.gravity_select import build_lapse_oneway
from ..layers.matter import algebra, build_matter, matter_names
from ..layers.system import HOP, MASS_DEFAULT, P_GRAV, Q_DEFAULT, WILSON
from ..layers.matter_lapse_c import build_matter_lapse_c
from ..observe import gravity as og
from ..observe.readout import carrier_from_law, own_frame_series, tick_rate
from ..prepare import vacuum_state

OUT = Path("runs/tests") / "system"
Q, P = Q_DEFAULT, P_GRAV
D = 6 * Q
L = 3
T_RUN = 2000
AMP = 1 << 20
U0_TARGET = 0.01


def stamp():
    return datetime.now(timezone.utc).strftime("%a %b %d %H:%M:%S UTC %Y")


def bands(bs):
    """Distinct eigenvalues of M0 and one unit eigenvector each (float; rounded when placed)."""
    M0 = m0_matrix(bs).astype(float)
    vals, vecs = np.linalg.eigh(M0)
    out = []
    for v in sorted(set(np.round(vals, 9))):
        idx = int(np.argmin(np.abs(vals - v)))
        out.append((float(vals[idx]), vecs[:, idx]))
    return out


def blocks_for(form, bs, F_on, mlapse="C"):
    bg = Block((GearType("F", "audit"),), tuple(gr.gradient_terms(gr.wave_potential("F", 0, 6 * Q))), name="bg",
               vacuum={"F": 3 * Q - 1}, Q=Q)
    if form == "C":
        l0 = build_l0c(Q=Q, body_signs=bs, name="ref")
        lap = build_l0c_lapse(Q=Q, P=P, field="bg.F", body_signs=bs, oneway=True, name="lapseL0")
    else:
        l0 = build_l0_weight(Q=Q, body_signs=bs, name="ref")
        lap = build_l0_lapse(Q=Q, P=P, field="bg.F", body_signs=bs, oneway=True, name="lapseL0")
    m = build_matter(Q=Q, hop=HOP, mass=MASS_DEFAULT, wilson=WILSON, species="pair", name="matter")
    if mlapse == "C":
        mread = build_matter_lapse_c(Q=Q, P=P, field="bg.F", matter=m, oneway=True, name="mread")
    else:
        spec = gr.spec_from_block(m, Q=Q, order=1)
        mread = build_lapse_oneway(Q=Q, P=P, field="bg.F", matters=[spec], name="mread")
    return [l0, bg, lap, m, mread]


def clock_run(form, bs, mu, v, F0, mlapse="C"):
    blocks = blocks_for(form, bs, F0 != 0, mlapse)
    Tn = compose(*blocks)
    eng = Engine(Tn, Q)
    s = vacuum_state(Tn, Q, L, *blocks)
    a, b, r = s.a.astype(OBJ), s.b.astype(OBJ), s.r.astype(OBJ)
    N = L ** 3
    gF = Tn.gear_index("bg.F")
    a[gF] = np.full(N, F0, dtype=object)
    b[gF] = np.full(N, F0, dtype=object)
    vv = v / np.max(np.abs(v))
    if form == "C":
        c0 = 1 - (Q - 1) * mu / (6 * Q)                  # 4 sin^2(w0/2) = (Q-1) mu/(3Q)
    else:
        c0 = (Q - 1) / Q * (6 - mu) / 6                  # split W: 2 cos w0 = (Q-1)/(3Q) (6 - mu)
    for h in range(48):
        g = Tn.gear_index(f"ref.R{h:02d}")
        b[g] = np.full(N, int(round(AMP * vv[h])), dtype=object)
        a[g] = np.full(N, int(round(AMP * vv[h] * c0)), dtype=object)
    # Dirac rest clock: an eigenvector of W0 with eigenvalue +1 (u = mass W0 b at k = 0; P_d + P_d^T = 0)
    W0 = algebra("pair")["W0"].astype(float)
    wv, wvec = np.linalg.eigh(W0)
    vm = wvec[:, int(np.argmax(wv))]
    vm = vm / np.max(np.abs(vm))
    cm = MASS_DEFAULT / D
    mn = matter_names("pair")
    for i in range(16):
        g = Tn.gear_index(f"matter.{mn[i]}")
        b[g] = np.full(N, int(round(AMP * vm[i])), dtype=object)
        a[g] = np.full(N, int(round(AMP * vm[i] * cm)), dtype=object)
    s = State(L, a, b, r)
    gl = Tn.gear_index(f"ref.R{int(np.argmax(np.abs(vv))):02d}")
    gm = Tn.gear_index(f"matter.{mn[int(np.argmax(np.abs(vm)))]}")
    ser = {"L0": ([], []), "dirac": ([], [])}
    full = {"L0": [], "dirac": []}
    for t in range(T_RUN):
        s1 = eng.step(s)
        for key, g in (("L0", gl), ("dirac", gm)):
            q = int(s1.b[g, 0]) + int(s.a[g, 0])
            full[key].append(q)
            if q != 0:
                ser[key][0].append(t)
                ser[key][1].append(q)
        s = s1
    w = {k: og.rate_from_crossings(og.crossing_times(*ser[k])) for k in ser}
    # R2: carriers FROM THE LAW (tensor), then the own-frame tick rates
    car = {"L0": carrier_from_law(Tn, [f"ref.R{h:02d}" for h in range(48)], "bg.F", D),
           "dirac": carrier_from_law(Tn, [f"matter.{x}" for x in mn], "bg.F", D)}
    for k in ("L0", "dirac"):
        w[f"{k}_own"] = tick_rate(own_frame_series(full[k], car[k]["carrier"]))
    w["carriers"] = car
    return w, dict(eng.stats)


def ratio_pred_L0(w0, U0):
    return 2 * math.asin(math.sqrt(1 - 2 * U0) * math.sin(w0 / 2)) / w0


def ratio_pred_dirac(wd0, U0):
    return math.asin((1 - U0) * math.sin(wd0)) / wd0


def run_all() -> dict:
    t0 = time.time()
    F0 = int(round(2 * P * U0_TARGET))
    U0 = F0 / (2 * P)
    res = {"Q": Q, "P": P, "L": L, "T": T_RUN, "amp": AMP, "F0": F0, "U0": U0,
           "pred": {"form_C_half_angle_N": math.sqrt(1 - 2 * U0), "dirac_demod_N": 1 - U0,
                    "gap": math.sqrt(1 - 2 * U0) - (1 - U0)}, "classes": {}}
    for name, bs in (("pmp", (1, -1, 1)), ("ppp", (1, 1, 1))):
        rows = []
        for mu, v in bands(bs):
            if mu < 1e-9:
                continue                                  # the +++ massless band: light (k = 0 is not a clock)
            w0a = 2 * math.asin(math.sqrt((Q - 1) * mu / (12 * Q)))
            row = {"mu": mu, "w0_analytic": w0a}
            for form, ml in (("C", "C"), ("split", "split")):
                w0, st0 = clock_run(form, bs, mu, v, 0, ml)
                w1, st1 = clock_run(form, bs, mu, v, F0, ml)
                w0L = w0["L0"] if w0["L0"] == w0["L0"] else (w0a if form == "C" else float("nan"))
                NL = math.sin(w1["L0"] / 2) / math.sin(w0L / 2)
                row[form] = {"w0": w0["L0"], "w0_used": w0L, "w": w1["L0"], "N_click_half_angle": NL,
                             "dev_vs_sqrt(1-2U0)": NL / math.sqrt(1 - 2 * U0) - 1,
                             "N_cos_ratio(demod)": math.cos(w1["L0"]) / math.cos(w0L), "stats": st1}
                wd0, wd = math.pi / 2 - w0["dirac"], math.pi / 2 - w1["dirac"]
                own0, own1 = w0["dirac_own"], w1["dirac_own"]
                row[form]["dirac"] = {"w_raw0": w0["dirac"], "w_raw": w1["dirac"],
                                      "N_demod(cos ratio)": math.cos(w1["dirac"]) / math.cos(w0["dirac"]),
                                      "raw_rate_ratio": w1["dirac"] / w0["dirac"],
                                      "N_half_angle(official raw)": math.sin(w1["dirac"] / 2) / math.sin(w0["dirac"] / 2),
                                      "own_rate0": own0, "own_rate": own1, "own_ratio": own1 / own0,
                                      "own_ratio_pred": ratio_pred_dirac(wd0, U0),
                                      "own_dev": (own1 / own0) / ratio_pred_dirac(wd0, U0) - 1,
                                      "carrier_F0": w0["carriers"]["dirac"], "carrier_F": w1["carriers"]["dirac"]}
                own0L = w0["L0_own"] if w0["L0_own"] == w0["L0_own"] else w0L
                row[form]["L0_own"] = {"own_rate0": own0L, "own_rate": w1["L0_own"],
                                       "own_ratio": w1["L0_own"] / own0L, "own_ratio_pred": ratio_pred_L0(own0L, U0),
                                       "own_dev": (w1["L0_own"] / own0L) / ratio_pred_L0(own0L, U0) - 1,
                                       "carrier": w1["carriers"]["L0"]}
                row[form]["universality_NL0_minus_Ndirac_demod"] = NL - row[form]["dirac"]["N_demod(cos ratio)"]
            rows.append(row)
            print(name, round(mu, 4), "C dev", row["C"]["dev_vs_sqrt(1-2U0)"], "C univ",
                  row["C"]["universality_NL0_minus_Ndirac_demod"], "dirac own dev", row["C"]["dirac"]["own_dev"],
                  "L0 own dev", row["C"]["L0_own"]["own_dev"], "split univ",
                  row["split"]["universality_NL0_minus_Ndirac_demod"], flush=True)
        res["classes"][name] = rows
    res["seconds"] = round(time.time() - t0, 1)
    res["stamp_utc"] = stamp()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "L0C_clock.json").write_text(json.dumps(res, indent=1, default=str))
    return res


class FormC(unittest.TestCase):
    def test_half_angle_universality_own_frame(self):
        r = run_all()
        U0 = r["U0"]
        for cls, rows in r["classes"].items():
            for row in rows:
                C = row["C"]
                with self.subTest(cls=cls, mu=row["mu"]):
                    self.assertLessEqual(abs(C["dev_vs_sqrt(1-2U0)"]), 1e-4)                               # C2
                    self.assertLessEqual(abs(C["dirac"]["N_demod(cos ratio)"] - (1 - U0)), 1e-4)            # C3 (R1)
                    self.assertLessEqual(abs(C["universality_NL0_minus_Ndirac_demod"]), U0 ** 2 / 2 + 1e-4)  # C3 (R1)
                    self.assertLessEqual(abs(C["dirac"]["own_dev"]), 1e-4)                                  # R2 Dirac
                    self.assertLessEqual(abs(C["L0_own"]["own_dev"]), 1e-4)                                 # R2 L0
                    self.assertEqual(C["dirac"]["carrier_F"]["carrier"], math.pi / 2)                        # R2 law
                    self.assertEqual(C["L0_own"]["carrier"]["carrier"], 0.0)
                    self.assertLess(C["dirac"]["carrier_F"]["residual"], 1e-9)
                    self.assertLess(C["L0_own"]["carrier"]["residual"], 1e-9)


if __name__ == "__main__":
    unittest.main()
