"""SEED tests SD1-SD5 (pre-registered in NOTES_system.md 11:08:22 UTC; run on the v2 default: handed class, form C,
l0_offset = Q - 1, Q = 2^33 + 1; addendum in NOTES_system.md). A = 2^12 is an EXACTNESS test amplitude (the weak-field
rule amplitude x field >= D/(8 g_phi) concerns physics demos, not these identities).
Run: OMP_NUM_THREADS=1 nice -n 10 python -m unittest research.metric_variant_v1.tests.test_seed -v
Writes results/system/SEED.json.
"""
from __future__ import annotations

import json
import time
import unittest
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from ..core.engine import OBJ, Engine
from ..core.tensor import compose
from ..layers.system import default_system
from ..observe import em as oem
from ..observe.seed import non_vacuum_count, r_star
from ..prepare.seed import (k0_offset, l0_dark_seed, l0_rstar_vector, m0_band_vector, node_rstar, ra_background,
                           s2_star)
from ..prepare.system import system_vacuum

OUT = Path(__file__).resolve().parent.parent / "results" / "system"
L = 6
A = 1 << 12
X0 = (2, 2, 2)


def stamp():
    return datetime.now(timezone.utc).strftime("%a %b %d %H:%M:%S UTC %Y")


def nz(x) -> int:
    return int(np.count_nonzero(np.asarray(x, dtype=object) != 0))


def seeds(S, T, vac):
    """R*-fixed seeds (RC2 BATCH 1: the L0 dark seeds are S-symmetrised, S = L0's signed relabelling)."""
    c_link = (2 * X0[0], 2 * X0[1] + 1, 2 * X0[2])
    c_node = tuple(2 * x for x in X0)
    bs = S.info["body_signs"]
    vb = None
    for band in range(9):                       # the lowest M0 band with a nonzero S-invariant vector
        try:
            vb = l0_rstar_vector(bs, m0_band_vector(bs, band, 64))
            break
        except (ValueError, IndexError):
            continue
    BAND_USED[0] = band
    return {"S2*": (s2_star(vac, T, X0, A), c_link),
            "node_R*": (node_rstar(vac, T, X0, A), c_node),
            "L0_rstar_e0": (l0_dark_seed(vac, T, X0, A, v=l0_rstar_vector(bs)), c_node),
            "L0_rstar_band": (l0_dark_seed(vac, T, X0, 1, v=vb), c_node)}


BAND_USED = [None]


def run_all() -> dict:
    t0 = time.time()
    S = default_system(chiral=False, electroweak=False)      # hands OFF: R* knows L0's relabelling, not the chiral maps
    Q, D = S.Q, 6 * S.Q
    T = compose(*S.blocks)
    E = Engine(T, Q)
    vac = system_vacuum(S, T, L)
    res = {"Q": Q, "L": L, "A": A, "x0": X0, "default": {k: S.info[k] for k in ("body_signs", "l0_offset", "l0_lapse",
                                                                                   "em", "lapse")}}
    off = S.info["l0_offset"]
    sd = {}
    for name, (s0, c2) in seeds(S, T, vac).items():
        row = {"non_vacuum_integers": non_vacuum_count(s0, vac)}
        row["lorenz_C_nonzero"] = nz(oem.lorenz_C(s0, T))
        row["charge_density_nonzero"] = nz(oem.charge_density(s0, T, D))
        s1 = E.step(s0)
        row["E1_after_one_update_nonvacuum"] = sum(nz(s1.a[T.gear_index(f"em.{g}")]) + nz(s1.b[T.gear_index(f"em.{g}")])
                                                   for g in ("A_x", "A_y", "A_z", "Phi"))
        row["gauss_Y_nonzero"] = nz(oem.gauss_Y(s0, T, S.by_name("em").params)) if hasattr(oem, "gauss_Y") else None
        row["R*_fixed"] = r_star(s0, T, Q, c2, l0_offset=off, body_signs=S.info["body_signs"]).same_as(s0)
        h = E.run(s0, 10)
        row["rewind10"] = E.rewind(h, 10).same_as(s0)
        sd[name] = row
    res["SD1_SD2_SD3"] = sd
    # SD6 (RC2 BATCH 1): bounce on the FULL v2 default with the L0 signed relabelling composed into R*
    bs = S.info["body_signs"]
    sd6 = {}
    for name, (s0, c2) in seeds(S, T, vac).items():
        if name == "node_R*":
            continue
        new, old = [], []
        fwd, bwd = s0, s0
        for t in range(1, 7):
            fwd, bwd = E.step(fwd), E.inverse_step(bwd)
            new.append(bwd.same_as(r_star(fwd, T, Q, c2, l0_offset=off, body_signs=bs)))
            old.append(bwd.same_as(r_star(fwd, T, Q, c2, l0_offset=off)))
        sd6[name] = {"F^-t = R* F^t (with L0 relabelling), t = 1..6": new,
                     "OLD declared R* (no relabelling), t = 1..6 (report)": old}
    one = l0_dark_seed(vac, T, X0, A)
    sd6["L0_one_channel_e0 (report)"] = {"R*_fixed_with_relabelling": r_star(one, T, Q, (4, 4, 4), l0_offset=off,
                                                                              body_signs=bs).same_as(one)}
    from ..observe.seed import l0_relabelling
    rel = l0_relabelling(bs)
    sd6["L0_relabelling"] = {"order": rel["order"], "fixed_dim": rel["fixed_dim"], "n_solutions": rel["n_solutions"],
                             "P": rel["P"], "chi": rel["chi"]}
    sd6["L0_rstar_band_index"] = BAND_USED[0]
    res["SD6_bounce_full_default"] = sd6
    # REPORT (batch 3): the hands-ON default (chiral + electroweak) with the integrator's R* (no chiral maps)
    SH = default_system()
    TH = compose(*SH.blocks)
    EH = Engine(TH, Q)
    vh = system_vacuum(SH, TH, L)
    s0 = s2_star(vh, TH, X0, A)
    c2l = (2 * X0[0], 2 * X0[1] + 1, 2 * X0[2])
    fwd, bwd, okh = s0, s0, []
    for t in range(1, 4):
        fwd, bwd = EH.step(fwd), EH.inverse_step(bwd)
        okh.append(bwd.same_as(r_star(fwd, TH, Q, c2l, l0_offset=off, body_signs=SH.info["body_signs"])))
    from ..observe.seed import r_star_hands_on
    RH = r_star_hands_on(SH, TH, c2l, L)
    fwd, bwd, okon = s0, s0, []
    for t in range(1, 7):
        fwd, bwd = EH.step(fwd), EH.inverse_step(bwd)
        okon.append(bwd.same_as(RH(fwd)))
    vl = l0_dark_seed(vh, TH, X0, A, v=l0_rstar_vector(SH.info["body_signs"]))
    RHn = r_star_hands_on(SH, TH, tuple(2 * x for x in X0), L)
    fwd, bwd, okl = vl, vl, []
    for t in range(1, 7):
        fwd, bwd = EH.step(fwd), EH.inverse_step(bwd)
        okl.append(bwd.same_as(RHn(fwd)))
    res["SD7_handsON"] = {"S2*": {"R*_on_fixed": RH(s0).same_as(s0), "F^-t = R*_on F^t, t = 1..6": okon},
                          "L0_rstar_e0 (report)": {"R*_on_fixed": RHn(vl).same_as(vl),
                                                   "F^-t = R*_on F^t, t = 1..6": okl}}
    res["REPORT_handsON_S2star"] = {"R*_fixed": r_star(s0, TH, Q, c2l, l0_offset=off,
                                                       body_signs=SH.info["body_signs"]).same_as(s0),
                                    "F^-t = R* F^t, t = 1..3 (integrator R*, no chiral maps)": okh,
                                    "legal_lorenz_C_nonzero": nz(oem.lorenz_C(s0, TH)),
                                    "rewind10": EH.rewind(EH.run(s0, 10), 10).same_as(s0)}
    # SD4: bounce on the matter + E1 subsystem (gravity, gauge, choice off; e1 = the subsystem's E1)
    S4 = default_system(em="e1", gravity=False, gauge=False, choice=False, l0_lapse=None, chiral=False, electroweak=False)
    T4 = compose(*S4.blocks)
    E4 = Engine(T4, Q)
    vac4 = system_vacuum(S4, T4, L)
    bounce = {}
    for name, builder, c2 in (("S2*", s2_star, (2 * X0[0], 2 * X0[1] + 1, 2 * X0[2])),
                              ("node_R*", node_rstar, tuple(2 * x for x in X0))):
        s0 = builder(vac4, T4, X0, A)
        ok = []
        fwd, bwd = s0, s0
        for t in range(1, 7):
            fwd, bwd = E4.step(fwd), E4.inverse_step(bwd)
            ok.append(bwd.same_as(r_star(fwd, T4, Q, c2, l0_offset=S4.info["l0_offset"])))
        bounce[name] = {"R*_fixed": r_star(s0, T4, Q, c2, l0_offset=S4.info["l0_offset"]).same_as(s0),
                        "F^-t = R* F^t, t = 1..6": ok}
    res["SD4_bounce_matter_E1"] = bounce
    # SD5: R-a datum and k = 0 offset (data checks)
    v, c0 = 1000, 77
    sb = ra_background(vac, T, v)
    gB = T.gear_index("bgk.B")
    s5 = E.run(sb, 5)
    res["SD5"] = {"bgk_static_5": bool(np.all(s5.a[gB].astype(OBJ) == v) and np.all(s5.b[gB].astype(OBJ) == v)),
                  "offset_rows_changed": sorted({T.names[g] for g in range(T.G)
                                                 if nz(k0_offset(vac, T, c0).a[g].astype(OBJ) - vac.a[g].astype(OBJ))
                                                 or nz(k0_offset(vac, T, c0).b[g].astype(OBJ) - vac.b[g].astype(OBJ))})}
    res["seconds"] = round(time.time() - t0, 1)
    res["stamp_utc"] = stamp()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "SEED.json").write_text(json.dumps(res, indent=1, default=str))
    return res


class Seeds(unittest.TestCase):
    def test_sd(self):
        r = run_all()
        for name, row in r["SD1_SD2_SD3"].items():
            with self.subTest(seed=name):
                if name in ("S2*", "node_R*"):
                    self.assertEqual(row["non_vacuum_integers"], 2)                        # SD1
                self.assertEqual(row["lorenz_C_nonzero"], 0)                              # SD1
                self.assertEqual(row["charge_density_nonzero"], 0)                        # SD1 (Gauss source)
                if row["gauss_Y_nonzero"] is not None:
                    self.assertEqual(row["gauss_Y_nonzero"], 0)                           # SD1
                self.assertTrue(row["R*_fixed"])                                          # SD2
                self.assertTrue(row["rewind10"])                                          # SD3
        for name in ("S2*", "L0_rstar_e0", "L0_rstar_band"):
            with self.subTest(sd6=name):
                self.assertTrue(all(r["SD6_bounce_full_default"][name][
                    "F^-t = R* F^t (with L0 relabelling), t = 1..6"]))                    # SD6
        self.assertTrue(r["SD7_handsON"]["S2*"]["R*_on_fixed"])                          # SD7 (batch 4)
        self.assertTrue(all(r["SD7_handsON"]["S2*"]["F^-t = R*_on F^t, t = 1..6"]))
        self.assertTrue(r["SD5"]["bgk_static_5"])
        self.assertEqual(r["SD5"]["offset_rows_changed"], ["metric.h00"])


if __name__ == "__main__":
    unittest.main()
