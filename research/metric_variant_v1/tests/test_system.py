"""INTEGRATOR exactness suite X1-X10 on the composed default system (pre-registered in NOTES_system.md 10:40:50 UTC;
v2 default and modes: "PRE-REGISTRATION v2 DEFAULT", 11:20 UTC; R1 matter lapse C + contrast mode: 11:48 UTC).

Run from the repository root (CPU saturated: one thread, nice):
    OMP_NUM_THREADS=1 nice -n 10 python -m unittest research.metric_variant_v1.tests.test_system -v
Each mode writes results/system/<mode>.json.
"""
from __future__ import annotations

import json
import time
import unittest
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from ..core.engine import Engine
from ..core.tensor import compose
from ..layers.system import Q_DEFAULT, default_system
from ..observe import em as oem
from ..observe.audit import frozen_equivalence
from ..observe.gauge import GaugeView
from ..observe.gravity import od2_constants
from ..observe.system import (census, collisions, designation_report, dressed_continuity_residual, joint_mirror,
                              mirror_check)
from ..prepare.system import random_reference_state, random_system_state, system_vacuum

OUT = Path(__file__).resolve().parent.parent / "results" / "system"
Q = Q_DEFAULT
L = 3


def stamp():
    return datetime.now(timezone.utc).strftime("%a %b %d %H:%M:%S UTC %Y")


def write(name, data):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{name}.json").write_text(json.dumps({**data, "stamp_utc": stamp()}, indent=1, default=str))


def nz(x) -> int:
    return int(np.count_nonzero(np.asarray(x, dtype=object) != 0))


def em_identities(hist, T, D, matter, em):
    out = {"continuity": 0, "lorenz_constant": 0, "gauss_step": 0, "noether_global": 0, "node_updates": 0}
    for s0, s1 in zip(hist[:-1], hist[1:]):
        out["continuity"] += nz(oem.continuity_residual(s0, s1, T, D, matter.params))
        out["lorenz_constant"] += nz(np.asarray(oem.lorenz_C(s1, T), dtype=object) -
                                     np.asarray(oem.lorenz_C(s0, T), dtype=object))
        out["gauss_step"] += nz(oem.gauss_step_residual(s0, s1, T, em.params))
        tot = (np.asarray(oem.charge_density(s1, T, D), dtype=object).sum()
               - np.asarray(oem.charge_density(s0, T, D), dtype=object).sum()
               - np.asarray(oem.remainder_term(s0, s1, T), dtype=object).sum())
        out["noether_global"] += int(tot != 0)
        out["node_updates"] += s0.N
    return out


def run_suite(mode: str, n: int = 6, **kw) -> dict:
    t0 = time.time()
    S = default_system(Q, **kw)
    res = {"mode": mode, "kwargs": {k: str(v) for k, v in kw.items()}, "info": S.info}
    legacy = S.info["l0_offset"] == 0 and not S.info.get("l0_lapse")
    T = compose(*S.blocks, q_lattice=("ref.*",) if legacy else ())      # the q-lattice rule is retired (decision 1)
    E = Engine(T, Q)
    Evac = Engine(T, Q)
    res["X1_one_Q"] = {"tensor_Q": T.Q, "blocks_Q": sorted({b.Q for b in S.blocks}), "pass": T.Q == Q and
                       {b.Q for b in S.blocks} == {Q}}
    res["X2_q_lattice_violations"] = len(T.q_lattice_violations(("ref.*",)))
    res["X2_validator_applied"] = legacy
    res["structure"] = {"G": T.G, "monomials": len(T), "rank": T.rank,
                        "stages": [[T.names[i] for i in st][:4] + (["..."] if len(st) > 4 else []) for st in T.stages]}
    # X3 vacuum + frozen
    vac = system_vacuum(S, T, L)
    s = vac
    changed = 0
    for _ in range(20):
        s1 = Evac.step(s)
        changed += int(not s1.same_as(s))
        s = s1
    ref = S.blocks[0]
    Tref = compose(ref)
    off = S.info["l0_offset"]
    base = random_reference_state(Q, Tref, L, seed=3, amp=20, offset=off)
    fr = frozen_equivalence((ref,), tuple(S.blocks[1:]), Q, base, 20)
    emb = None
    if off and not S.info.get("l0_lapse"):
        Er = Engine(Tref, Q)
        b0 = random_reference_state(Q, Tref, L, seed=3, amp=20, offset=0)
        s_off, s_on = base, b0
        ok = True
        for _ in range(20):
            s_off, s_on = Er.step(s_off), Er.step(s_on)
            ok &= bool(np.array_equal(s_off.a, s_on.a) and np.array_equal(s_off.b, s_on.b)
                       and np.all(s_off.r.astype(object) - s_on.r.astype(object) == off))
        emb = ok
    res["X3_vacuum_frozen"] = {"vacuum_changed_updates": changed, "frozen": fr, "offset_embedding_ok": emb}
    # X4 rewind, X5 joint mirror, X6 identities
    s0 = random_system_state(S, T, L, seed=11)
    hist = E.run(s0, n, history=True)
    res["X4_rewind"] = E.rewind(hist[-1], n).same_as(s0)
    hands_on = isinstance(S.info.get("chiral"), dict)
    if hands_on:                      # RC2 batch 4: T_phys of the chiral layer composed with E1 and M' elsewhere
        from ..observe.system import joint_mirror_hands_on
        X, N = joint_mirror_hands_on(S, T)
    else:
        X, N = joint_mirror(S, T)
    mir = [mirror_check(E, X, N, random_system_state(S, T, L, seed=sd), n) for sd in (21, 22)]
    Xp, Np = joint_mirror(S, T, dirac="Mp")
    res["X5_joint_mirror"] = {"map": getattr(X, "name", "X"), "declared_X_FnXFn_eq_N": mir,
                              "X_fixes_vacuum": X(vac).same_as(vac),
                              "N_fixes_vacuum": N(vac).same_as(vac),
                              "control_plain_Mp_on_matter": mirror_check(E, Xp, Np, random_system_state(S, T, L, seed=21),
                                                                         n)}
    x6 = {}
    for g in ("su2", "su3", "u1"):
        if any(b.name == g for b in S.blocks):
            V = GaugeView(T, S.by_name(g).params, g)
            x6[g] = V.gauss_check(hist)
    if any(b.name == "od2" for b in S.blocks):
        Cs = [od2_constants(T, "od2", hist[t], hist[t + 1]) for t in range(len(hist) - 1)]
        x6["od2_constants_changed"] = sum(nz(np.asarray(Cs[t + 1][c], dtype=object) - np.asarray(Cs[t][c], dtype=object))
                                          for t in range(len(Cs) - 1) for c in range(4))
    if S.info.get("em") == "e1":
        x6["e1_with_gravity"] = em_identities(hist, T, 6 * Q, S.by_name("matter"), S.by_name("em"))
    if S.info.get("em") == "e1d":
        m, e = S.by_name("matter"), S.by_name("em")
        dd = {"dressed_continuity": 0, "gauss_step": 0, "lorenz_constant": 0, "noether_global": 0, "node_updates": 0,
              "free_continuity_for_contrast": 0}
        for a0, a1 in zip(hist[:-1], hist[1:]):
            dd["dressed_continuity"] += nz(dressed_continuity_residual(a0, a1, T, 6 * Q, m.params, P=S.info["P"],
                                                                       lapse=S.info["lapse_field"]))
            dd["free_continuity_for_contrast"] += nz(oem.continuity_residual(a0, a1, T, 6 * Q, m.params))
            dd["gauss_step"] += nz(oem.gauss_step_residual(a0, a1, T, e.params))
            dd["lorenz_constant"] += nz(np.asarray(oem.lorenz_C(a1, T), dtype=object) -
                                        np.asarray(oem.lorenz_C(a0, T), dtype=object))
            tot = (np.asarray(oem.charge_density(a1, T, 6 * Q), dtype=object).sum()
                   - np.asarray(oem.charge_density(a0, T, 6 * Q), dtype=object).sum()
                   - np.asarray(oem.remainder_term(a0, a1, T), dtype=object).sum())
            dd["noether_global"] += int(tot != 0)
            dd["node_updates"] += a0.N
        x6["e1d_with_gravity"] = dd
    res["X6_identities"] = x6
    res["X7_reciprocity"] = designation_report(T)
    res["X8_B3"] = {"composed": True, "support_violations": len(T.support_violations())}
    res["X9_census"] = census(T)
    res["X10_collisions"] = collisions(S, T)
    res["int64_headroom"] = {"vacuum_run": dict(Evac.stats), "random_state_runs": dict(E.stats),
                             "random_state_amplitudes": "prepare.system.random_system_state defaults"}
    res["seconds"] = round(time.time() - t0, 1)
    write(mode, res)
    return res


def run_e1_without_gravity(n: int = 6) -> dict:
    S = default_system(Q, em="e1", gravity=False, gauge=False, choice=False, l0_lapse=None, chiral=False,
                       electroweak=False)
    T = compose(*S.blocks, q_lattice=("ref.*",))
    E = Engine(T, Q)
    hist = E.run(random_system_state(S, T, L, seed=11), n, history=True)
    out = {"e1_without_gravity": em_identities(hist, T, 6 * Q, S.by_name("matter"), S.by_name("em"))}
    write("e1_without_gravity", out)
    return out


MODES = {
    "v2_default": {},                                                    # +-+, off Q-1, form C, e1d, wave + bgk
    "v2_ppp": {"body_signs": (1, 1, 1)},
    "v2_noL0lapse": {"l0_lapse": None},
    "v2_W_split_contrast": {"l0_lapse": "W_split"},
    "v2_od2_variant": {"lapse": "od2"},
    "v2_compact": {"em": "compact"},
    "v2_e1_undressed": {"em": "e1"},
    "v2_P2p16": {"P": 1 << 16},
    "v2_c2_on": {"c2": True},
    "v2_handsOFF": {"chiral": False, "electroweak": False},                # the R1 default before decision 5
    "v2_matter_split_contrast": {"matter_lapse": "split", "chiral": False, "electroweak": False},   # R1 contrast
    "v2_beta_marginal_contrast": {"beta_form": "marginal"},               # pre-GRAV-FIX beta (B1-GRAV build_beta)
    "legacy_ppp_off0": {"body_signs": (1, 1, 1), "l0_offset": 0, "l0_lapse": None},
}


def run_rc2_checks() -> dict:
    """RC2 BATCH 1: readout labels follow the tensor (F-R); the chiral switch builds, keeps the vacuum and rewinds."""
    from ..observe.readout import dark_l0_violations, readout_class
    from ..prepare.system import random_system_state as rss
    out = {}
    for bsname, bs in (("pmp", (1, -1, 1)), ("ppp", (1, 1, 1))):
        S = default_system(Q, body_signs=bs)
        T = compose(*S.blocks)
        cls = {n: readout_class(T, n) for n in T.names}
        out[f"readout_{bsname}"] = {"n_audit": sum(c == "audit" for c in cls.values()),
                                    "n_official": sum(c == "official" for c in cls.values()),
                                    "dark_l0_violations": dark_l0_violations(S, T),
                                    "ref_labels": sorted({cls[n] for n in T.names if n.startswith("ref.")})}
    S = default_system(Q, chiral=True, electroweak=False)
    T = compose(*S.blocks)
    E = Engine(T, Q)
    vac = system_vacuum(S, T, L)
    s = vac
    for _ in range(3):
        s = E.step(s)
    s0 = random_system_state(S, T, L, seed=11)
    out["chiral"] = {"blocks": [b.name for b in S.blocks], "G": T.G, "monomials": len(T),
                     "vacuum_fixed_3": s.same_as(vac), "rewind_3": E.rewind(E.run(s0, 3), 3).same_as(s0),
                     "info": S.info.get("chiral")}
    try:
        default_system(Q, chiral=False, electroweak=True)
        out["electroweak_without_chiral_raises"] = False
    except ValueError:
        out["electroweak_without_chiral_raises"] = True
    S = default_system(Q, chiral=True, electroweak=True)
    T = compose(*S.blocks)
    E = Engine(T, Q)
    vac = system_vacuum(S, T, L)
    s = vac
    for _ in range(3):
        s = E.step(s)
    s0 = random_system_state(S, T, L, seed=11)
    out["electroweak"] = {"blocks": [b.name for b in S.blocks], "G": T.G, "monomials": len(T),
                          "vacuum_fixed_3": s.same_as(vac), "rewind_3": E.rewind(E.run(s0, 3), 3).same_as(s0),
                          "info": S.info.get("electroweak")}
    write("rc2_batch1_checks", out)
    return out


class X1toX10(unittest.TestCase):
    def test_modes(self):
        for mode, kw in MODES.items():
            with self.subTest(mode=mode):
                r = run_suite(mode, **kw)
                self.assertTrue(r["X1_one_Q"]["pass"])
                if r["X2_validator_applied"]:
                    self.assertEqual(r["X2_q_lattice_violations"], 0)
                self.assertEqual(r["X3_vacuum_frozen"]["vacuum_changed_updates"], 0)
                if not r["info"].get("l0_lapse"):   # with an L0 lapse, L0 is a gravity SOURCE: frozen not expected
                    self.assertTrue(r["X3_vacuum_frozen"]["frozen"]["frozen"])
                self.assertTrue(r["X4_rewind"])
                self.assertTrue(r["X7_reciprocity"]["ok"])
                hands_on = bool(r["info"].get("chiral"))
                self.assertTrue(r["X5_joint_mirror"]["X_fixes_vacuum"])
                if kw.get("lapse", "wave") == "wave" and kw.get("em") != "compact":
                    self.assertTrue(all(r["X5_joint_mirror"]["declared_X_FnXFn_eq_N"]))   # od2: C8; compact: reported
                x6 = r["X6_identities"]
                for g in ("su2", "su3", "u1"):
                    if g in x6:
                        self.assertEqual(x6[g]["failures"], 0)
                if "e1d_with_gravity" in x6 and not hands_on:      # hands ON: reported (EW changes the current)
                    d = x6["e1d_with_gravity"]
                    self.assertEqual(d["dressed_continuity"] + d["gauss_step"] + d["lorenz_constant"] +
                                     d["noether_global"], 0)

    def test_rc2_batch1(self):
        r = run_rc2_checks()
        for k in ("readout_pmp", "readout_ppp"):
            self.assertEqual(r[k]["dark_l0_violations"], [])
        self.assertEqual(r["readout_pmp"]["ref_labels"], ["audit"])
        self.assertTrue(r["chiral"]["vacuum_fixed_3"])
        self.assertTrue(r["chiral"]["rewind_3"])
        self.assertTrue(r["electroweak_without_chiral_raises"])
        self.assertTrue(r["electroweak"]["vacuum_fixed_3"])
        self.assertTrue(r["electroweak"]["rewind_3"])

    def test_e1_without_gravity(self):
        r = run_e1_without_gravity()
        e = r["e1_without_gravity"]
        self.assertEqual(e["continuity"] + e["lorenz_constant"] + e["gauss_step"] + e["noether_global"], 0)


if __name__ == "__main__":
    unittest.main()
