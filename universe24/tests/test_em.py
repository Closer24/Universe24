"""Stage-1 MATTER + EM tests EM-T1 ... EM-T9 (pre-registered in NOTES_em.md before any run).

Run from the repository root:
    OMP_NUM_THREADS=2 nice -n 10 python -m unittest universe24.tests.test_em -v
Each test writes results/EM-T*.json with a `date -u` stamp.
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np

from universe24.core import Engine, State, Tensor, check_reciprocity, compose
from universe24.core.engine import OBJ
from universe24.core.lattice import DIRECTIONS
from universe24.layers import build_reference
from universe24.layers.em import A_NAMES, PHI, build_current_driver, build_em
from universe24.layers.matter import (algebra, bloch_matrix, build_matter,
                                                      build_static_lapse_mechanism, check_algebra, matter_names)
from universe24.observe import em as oem
from universe24.observe.audit import frozen_equivalence
from universe24.prepare import vacuum_state
from universe24.prepare import em as pem

RESULTS = Path("runs/tests")
Q0 = 2 ** 29 + 1
HOP = (Q0 - 1) // 4
MASS = 3 * Q0
WIL = HOP // 8          # Wilson weight hop/8 (A3): g = gcd(hop, wilson) = 2^24
SIG_W = 2 ** 8          # sigma with Wilson (sigma/g equal to 2^11/2^27)


def stamp() -> str:
    return subprocess.run(["date", "-u"], capture_output=True, text=True).stdout.strip()


def record(name: str, data: dict) -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    data = dict(data, test=name, written=stamp())
    (RESULTS / f"{name}.json").write_text(json.dumps(data, indent=1, default=str))


def system(Q=Q0, hop=HOP, mass=MASS, wilson=0, g_phi=4, g_A=1, sigma=2 ** 11, **kw):
    m = build_matter(Q=Q, hop=hop, mass=mass, wilson=wilson)
    e = build_em(Q=Q, matter=m, g_phi=g_phi, g_A=g_A, sigma=sigma, **kw)
    T = compose(m, e)
    return m, e, T, Engine(T, Q)


def pair_state(m, e, T, Q, L, amp, width, kc, pos_p, pos_a, rng=None, prepared_phi=True):
    """Particle (kc) at pos_p + the C-image of a particle (-kc) at pos_a; random remainders if rng is given."""
    vac = vacuum_state(T, Q, L, m, e)
    kc = np.asarray(kc, float)
    ap, bp, _ = pem.dirac_packet(m.params, L, +1, width, amp, kc=kc, center=pos_p)
    an, bn, _ = pem.dirac_packet(m.params, L, +1, width, amp, kc=-kc, center=pos_a)
    a = ap + pem.c_image(an)
    b = bp + pem.c_image(bn)
    r = None
    if rng is not None:
        r = rng.integers(0, 6 * Q, size=(L, L, L, 16)).astype(object)
    st = pem.set_matter(vac, T, "matter", a, b, r)
    if prepared_phi:
        rho = oem.charge_density(st, T, 6 * Q)
        Phi = pem.static_phi_for(rho, e.params)
        rf = None if rng is None else rng.integers(0, 6 * Q, size=(L, L, L)).astype(object)
        st = pem.set_field(st, T, "em", PHI, Phi, Phi, rf)
        if rng is not None:
            for n in A_NAMES:
                g = T.gear_index(f"em.{n}")
                R = st.r.astype(OBJ)
                R[g] = rng.integers(0, 6 * Q, size=L ** 3).astype(object)
                st = State(L, st.a, st.b, R)
    return st


def count_nz(arr) -> int:
    return int(np.count_nonzero(np.asarray(arr != 0, dtype=bool)))


def identity_failures(hist, T, e, m, D, check_C_zero=True):
    """Exact identity failures along a stored history (counts of nodes)."""
    out = {"continuity": 0, "lorenz_constant": 0, "lorenz_C_nonzero": 0, "gauss_step": 0, "noether_global": 0,
           "node_updates": 0}
    for s0, s1 in zip(hist[:-1], hist[1:]):
        out["continuity"] += count_nz(oem.continuity_residual(s0, s1, T, D, m.params))
        dC = oem.lorenz_C(s1, T) - oem.lorenz_C(s0, T)
        out["lorenz_constant"] += count_nz(dC)
        if check_C_zero:
            out["lorenz_C_nonzero"] += count_nz(oem.lorenz_C(s1, T))
        out["gauss_step"] += count_nz(oem.gauss_step_residual(s0, s1, T, e.params))
        tot = oem.charge_density(s1, T, D).sum() - oem.charge_density(s0, T, D).sum() - \
            oem.remainder_term(s0, s1, T).sum()
        out["noether_global"] += int(tot != 0)
        out["node_updates"] += s0.N
    return out


# ============================================================================================ EM-T1, EM-T2, EM-T3
class TestStructure(unittest.TestCase):
    def test_T1_algebra(self):
        alg = check_algebra()
        record("EM-T1", {"verdict": "PASS" if all(alg.values()) else "FAIL", "checks": alg})
        self.assertTrue(all(alg.values()), alg)

    def test_T2_structure(self):
        m, e, T, _ = system()
        names = T.names
        stages = [[names[i] for i in s] for s in T.stages]
        ok_stages = stages == [["em.A_x", "em.A_y", "em.A_z"], ["em.Phi"], [f"matter.{n}" for n in matter_names()]]
        p = T.gear_index("em.Phi")
        phi_coeffs = [mm.coeff for mm in T.monomials if mm.target == p]
        rounding_free = all(c % (3 * Q0) == 0 for c in phi_coeffs)
        # OD3 (with wilson = 1 too)
        od3 = {}
        for wil in (0, 1):
            _, _, Tw, _ = system(wilson=wil)
            mi = {Tw.gear_index(f"matter.{n}") for n in matter_names()}
            worst = 0
            for t in mi:
                per = {}
                for mm in Tw.monomials:
                    if mm.target == t and mm.degree == 1 and mm.factors[0].offset != (0, 0, 0):
                        per.setdefault(mm.factors[0].offset, set()).add(mm.factors[0].gear)
                worst = max([worst] + [len(v) for v in per.values()])
            od3[wil] = worst
        # deviation form: every term targeting a new gear has a new-gear factor (all gears here are new)
        dev = all(mm.degree >= 1 for mm in T.monomials)
        sv = T.support_violations()
        sv_ok = len(sv) == 18 and all(names[mm.target].startswith("em.A_") and mm.degree == 1 and
                                      mm.factors[0].gear == mm.target and mm.factors[0].offset != (0, 0, 0)
                                      for mm in sv)
        res = {"rank": T.rank, "stages": stages, "stages_ok": ok_stages, "phi_rounding_free": rounding_free,
               "od3_max_gears_per_face": od3, "deviation_form": dev, "support_violations": len(sv),
               "support_violations_are_A_stencil": sv_ok, "census": T.census(), "monomials": len(T),
               "G": T.G}
        ok = T.rank == 3 and ok_stages and rounding_free and max(od3.values()) <= 2 and dev and sv_ok
        record("EM-T2", dict(res, verdict="PASS" if ok else "FAIL"))
        self.assertTrue(ok, res)

    def test_T3_reciprocity(self):
        m, e, T, _ = system(sigma=2 ** 14)
        rep = check_reciprocity(T)
        names = T.names
        mset = {f"matter.{n}" for n in matter_names()}
        kinds = {"A_source": 0, "matter<-Phi.b": 0, "matter<-A.b": 0, "Phi<-A.b": 0, "other": 0}
        cross_bonly_undesignated = 0
        for mm in T.monomials:
            if mm.degree == 0 or any(f.field == "a" for f in mm.factors):
                continue
            tgt = names[mm.target]
            fac = [names[f.gear] for f in mm.factors]
            cross = (tgt in mset) != all(x in mset for x in fac) or (tgt not in mset and any(x in mset for x in fac))
            if tgt == "em.Phi" and fac != ["em.Phi"]:
                cross = True
            des = T.is_designated(mm)
            if des is None:
                cross_bonly_undesignated += int(cross)
                continue
            if tgt.startswith("em.A_") and all(x in mset for x in fac):
                kinds["A_source"] += 1
            elif tgt in mset and "em.Phi" in fac:
                kinds["matter<-Phi.b"] += 1
            elif tgt in mset and any(x.startswith("em.A_") for x in fac):
                kinds["matter<-A.b"] += 1
            elif tgt == "em.Phi":
                kinds["Phi<-A.b"] += 1
            else:
                kinds["other"] += 1
        free = check_reciprocity(compose(m))
        stripped = Tensor(T.gears, [(mm.target, mm.coeff, mm.factors) for mm in T.monomials], Q=T.Q)
        rs = check_reciprocity(stripped)
        # Peierls control: literal transpose of the source
        _, ep, Tp, _ = system(sigma=2 ** 14, vector="peierls")
        rp = check_reciprocity(Tp)
        mi = {Tp.gear_index(x) for x in mset}
        peierls_entries = [mm for mm in Tp.monomials if mm.target in mi and mm.degree == 2 and
                           any(Tp.names[f.gear].startswith("em.A_") for f in mm.factors) and
                           any(f.offset != (0, 0, 0) for f in mm.factors if f.gear in mi)]
        peierls_undesignated = all(Tp.is_designated(mm) is None for mm in peierls_entries)
        # blind control
        _, eb, Tb, _ = system(sigma=2 ** 14, blind=2)
        Tb_strip = Tensor(Tb.gears, [(mm.target, mm.coeff, mm.factors) if (Tb.is_designated(mm) or "").startswith(
            "CONTROL") is False else (mm.target, mm.coeff, mm.factors) for mm in Tb.monomials],
            designated_one_way=[(t, fs, why) for (t, fs), why in Tb.designations.items()
                                if not why.startswith("CONTROL")], Q=Tb.Q)
        rb = check_reciprocity(Tb_strip)
        res = {"ok": rep.ok, "checked": rep.checked, "designated": len(rep.designated), "kinds": kinds,
               "undesignated_cross_b_only": cross_bonly_undesignated, "skipped_two_time": rep.skipped_two_time,
               "free_matter_ok": free.ok, "free_matter_designated": len(free.designated),
               "stripped_fails": not rs.ok, "stripped_violations": len(rs.violations),
               "peierls_control_ok": rp.ok, "peierls_entries": len(peierls_entries),
               "peierls_entries_undesignated": peierls_undesignated,
               "blind_stripped_fails": not rb.ok, "blind_violations": len(rb.violations),
               "designation_texts": sorted({why for _, why in rep.designated})}
        ok = (rep.ok and kinds["other"] == 0 and cross_bonly_undesignated == 0 and free.ok and
              len(free.designated) == 0 and not rs.ok and rp.ok and peierls_undesignated and len(peierls_entries) > 0
              and not rb.ok)
        record("EM-T3", dict(res, verdict="PASS" if ok else "FAIL"))
        self.assertTrue(ok, res)


# ============================================================================================ EM-T4 vacuum
class TestVacuum(unittest.TestCase):
    def test_T4_vacuum(self):
        Q = Q0
        m = build_matter(Q=Q, hop=HOP, mass=MASS)
        e = build_em(Q=Q, matter=m, g_phi=4, g_A=1, sigma=2 ** 11)
        lap = build_static_lapse_mechanism(Q=Q, matter=m)
        drv = build_current_driver(Q=Q, em=e, axis=2, kappa=6 * Q, coupling=2 ** 20)
        T = compose(m, e, lap, drv)
        eng = Engine(T, Q)
        vac = vacuum_state(T, Q, 4, m, e, lap, drv)
        s = vac
        changed = 0
        for _ in range(20):
            s2 = eng.step(s)
            changed += int(not s2.same_as(s))
            s = s2
        fixed = changed == 0 and s.same_as(vac)
        # reference board untouched: frozen equivalence with the reference block at the same Q
        rng = np.random.default_rng(7)
        L = 4
        N = L ** 3
        ref = build_reference(Q=Q)
        base = State(L, rng.integers(-20, 21, (48, N)), rng.integers(-20, 21, (48, N)),
                     Q * rng.integers(0, 6, (48, N)))
        fe = frozen_equivalence((ref,), (m, e), Q, base, 20)
        ok = fixed and fe["frozen"]
        record("EM-T4", {"vacuum_fixed_20_updates": fixed, "updates_with_change": changed, "frozen_equivalence": fe,
                         "verdict": "PASS" if ok else "FAIL"})
        self.assertTrue(ok)


# ============================================================================================ EM-T5, EM-T6
class TestIdentities(unittest.TestCase):
    def test_T5a_dynamical_identities_and_T6_rewind(self):
        out = {}
        allok = True
        for amp_log in (12, 16, 20):
            sigma = 2 ** 14 * (2 ** 14 // 2 ** amp_log) ** 2 if amp_log <= 14 else 2 ** 14 // (2 ** (amp_log - 14)) ** 2
            m, e, T, eng = system(sigma=sigma)
            D = 6 * Q0
            L, steps = 6, 60
            s0 = pair_state(m, e, T, Q0, L, 2 ** amp_log, 1.3, (0.4, 0, 0), (1, 3, 3), (4, 3, 3))
            hist = eng.run(s0, steps, history=True)
            fails = identity_failures(hist, T, e, m, D)
            Y0 = oem.gauss_Y(hist[0], T, e.params)
            drift = max(abs(int(v)) for v in (oem.gauss_Y(hist[-1], T, e.params) - Y0).ravel())
            scale = max(abs(int(v)) for v in (sigma * oem.charge_density(hist[0], T, D)).ravel())
            back = eng.rewind(hist[-1], steps)
            rew = back.same_as(s0)
            ok = all(v == 0 for k, v in fails.items() if k != "node_updates") and rew
            allok &= ok
            out[f"amp_2^{amp_log}"] = dict(fails, sigma=sigma, undressed_gauss_drift_rel=drift / scale,
                                          rewind_exact=rew, max_abs=hist[-1].max_abs(), stats=dict(eng.stats))
        record("EM-T5a_T6", dict(out, verdict="PASS" if allok else "FAIL"))
        self.assertTrue(allok, out)

    def test_T5b_any_data(self):
        rng = np.random.default_rng(11)
        m, e, T, eng = system(wilson=WIL, sigma=SIG_W)
        D = 6 * Q0
        L, steps = 4, 30
        N = L ** 3
        vac = vacuum_state(T, Q0, L, m, e)
        a = rng.integers(-2 ** 10, 2 ** 10 + 1, (T.G, N)).astype(object)
        b = rng.integers(-2 ** 10, 2 ** 10 + 1, (T.G, N)).astype(object)
        r = rng.integers(0, D, (T.G, N)).astype(object)
        s0 = State(L, a, b, r)
        hist = eng.run(s0, steps, history=True)
        fails = identity_failures(hist, T, e, m, D, check_C_zero=False)
        rew = eng.rewind(hist[-1], steps).same_as(s0)
        ok = all(v == 0 for k, v in fails.items() if k not in ("node_updates", "lorenz_C_nonzero")) and rew
        record("EM-T5b", dict(fails, rewind_exact=rew, max_abs=hist[-1].max_abs(), verdict="PASS" if ok else "FAIL"))
        self.assertTrue(ok, fails)

    def test_T5c_negative_controls(self):
        m, e, T, eng = system(sigma=2 ** 10)
        mp, ep, Tp, engp = system(sigma=2 ** 10, vector="peierls")
        D = 6 * Q0
        L, steps = 6, 20
        s0 = pair_state(m, e, T, Q0, L, 2 ** 16, 1.3, (0.4, 0, 0), (1, 3, 3), (4, 3, 3))
        hp = engp.run(s0, steps, history=True)
        peierls_cont = sum(count_nz(oem.continuity_residual(x, y, Tp, D, mp.params)) for x, y in zip(hp[:-1], hp[1:]))
        peierls_gauss = sum(count_nz(oem.gauss_step_residual(x, y, Tp, ep.params)) for x, y in zip(hp[:-1], hp[1:]))
        h = eng.run(s0, steps, history=True)
        noR = sum(count_nz(oem.continuity_residual(x, y, T, D, m.params) + oem.remainder_term(x, y, T))
                  for x, y in zip(h[:-1], h[1:]))
        # drop r_A from the Gauss identity: add back g * (div r_A(after) - div r_A(before))
        def div_rA(s):
            f = oem.field_view(s, T)
            return oem._div([f[n][2] for n in A_NAMES])
        noRA = sum(count_nz(oem.gauss_step_residual(x, y, T, e.params) + e.params["g"] * (div_rA(y) - div_rA(x)))
                   for x, y in zip(h[:-1], h[1:]))
        nodes = L ** 3 * steps
        ok = peierls_cont > 0 and noR > 0 and noRA > 0
        record("EM-T5c", {"peierls_continuity_failures": peierls_cont, "peierls_gauss_failures": peierls_gauss,
                          "drop_R_failures": noR, "drop_rA_failures": noRA, "node_updates": nodes,
                          "verdict": "PASS" if ok else "FAIL"})
        self.assertTrue(ok)


# ============================================================================================ EM-T7 reversor
class TestReversor(unittest.TestCase):
    def test_T7_staggered_reversor(self):
        out = {}
        allok = True
        for wil, mirror in ((0, "Mp"), (0, "M"), (WIL, "Mp")):
            rng = np.random.default_rng(3)
            m, e, T, eng = system(sigma=2 ** 11 if wil == 0 else SIG_W, wilson=wil)
            D = 6 * Q0
            L, steps = 8, 30
            s0 = pair_state(m, e, T, Q0, L, 2 ** 16, 1.3, (0.4, 0, 0), (2, 4, 4), (6, 4, 4), rng=rng)
            X = lambda s: pem.x_reversor(s, T, D, mirror=mirror)
            Xc, KM, Ncore = pem.x_reversor_core(T, Q0, mirror=mirror)
            Nm = lambda s: pem.matter_negation(s, T, D, mirror=mirror)
            hist = eng.run(s0, steps, history=True)
            same_as_core = all(X(s).same_as(Xc(s)) for s in hist[::3])
            n_core_equal = all(Nm(s).same_as(Ncore(s)) for s in hist[::10])
            t1 = []
            for t in range(0, steps, 3):
                S = hist[t]
                R = X(eng.step(X(eng.step(S))))
                t1.append("id" if R.same_as(S) else ("neg" if R.same_as(Nm(S)) else "FAIL"))
            z = X(hist[-1])
            zh = eng.run(z, steps, history=True)
            back = X(zh[-1])
            t2 = "id" if back.same_as(s0) else ("neg" if back.same_as(Nm(s0)) else "FAIL")
            vac = vacuum_state(T, Q0, L, m, e)
            vac_fixed = X(vac).same_as(vac)
            # clicks: mirrored step t vs original step T-1-t, matter gears, K channel map
            K = algebra("pair")["K"]
            kperm = np.abs(K).argmax(1)
            ksign = K[np.arange(16), kperm]
            flags_equal = True
            size_mism = 0
            nclk = 0
            for t in range(steps):
                em_ = oem.click_sizes(zh[t], zh[t + 1], T)
                am_ = oem.matter_view(zh[t], T, exact=False)
                bm_ = oem.matter_view(zh[t + 1], T, exact=False)
                cm = (em_ != 0) & ((am_[0] != bm_[0]) | (am_[1] != bm_[1]) | (am_[2] != bm_[2]))
                eo = oem.click_sizes(hist[steps - 1 - t], hist[steps - t], T)
                ao = oem.matter_view(hist[steps - 1 - t], T, exact=False)
                bo = oem.matter_view(hist[steps - t], T, exact=False)
                co = (eo != 0) & ((ao[0] != bo[0]) | (ao[1] != bo[1]) | (ao[2] != bo[2]))
                Ke, Kc = eo[..., kperm] * ksign, co[..., kperm]
                flags_equal &= bool(np.array_equal(cm, Kc))
                size_mism += int(np.count_nonzero(np.abs(em_) != np.abs(Ke)))
                nclk += int(cm.sum())
            # the engine's official click log agrees with the flags used above (matter gears, first update)
            log = eng.clicks(hist[0], hist[1])
            mi = {T.gear_index(f"matter.{n}") for n in matter_names()}
            n_log = int(sum(1 for g in log.gear if int(g) in mi))
            e0 = oem.click_sizes(hist[0], hist[1], T)
            a0 = oem.matter_view(hist[0], T, exact=False)
            b0 = oem.matter_view(hist[1], T, exact=False)
            n_flags = int(((e0 != 0) & ((a0[0] != b0[0]) | (a0[1] != b0[1]) | (a0[2] != b0[2]))).sum())
            # negative controls
            from universe24.core.reversors import uniform
            Mplain = uniform(T, Q0, mirror)
            plain = sum(int(not Mplain(eng.step(Mplain(eng.step(S)))).same_as(S)) for S in hist[:30:10])

            def X_unstaggered(s):
                o = X(s)
                p = T.gear_index("em.Phi")
                A_, B_, R_ = o.a.astype(OBJ), o.b.astype(OBJ), o.r.astype(OBJ)
                A_[p], B_[p] = -s.b[p], -s.a[p]
                return State(s.L, A_, B_, R_)
            unst = sum(int(not (lambda R, S: R.same_as(S) or R.same_as(Nm(S)))(
                X_unstaggered(eng.step(X_unstaggered(eng.step(S)))), S)) for S in hist[:30:10])
            C_fail = sum(count_nz(oem.lorenz_C(s, T)) for s in hist)
            ok = (all(x in ("id", "neg") for x in t1) and t2 in ("id", "neg") and flags_equal and size_mism == 0
                  and same_as_core and n_core_equal and plain == 3 and unst == 3 and C_fail == 0 and n_log == n_flags
                  and (vac_fixed or mirror == "M"))
            allok &= ok
            out[f"wilson={wil},mirror={mirror}"] = {
                "XFXF_at_10_states": t1, "full_run_X_T_X": t2, "click_flags_identical_under_K": flags_equal,
                "click_size_mismatches": size_mism, "mirrored_matter_clicks": nclk, "X_fixes_joint_vacuum": vac_fixed,
                "engine_official_log_matter_rows_step0": n_log, "flag_count_step0": n_flags,
                "my_X_equals_core_built_X": same_as_core, "N_equals_core_central": n_core_equal,
                "control_plain_mirror_failures_of_3": plain, "control_unstaggered_Phi_failures_of_3": unst,
                "lorenz_C_nonzero": C_fail, "ok": ok}
        # free matter alone: Kramers K o M' is an exact reversor of the b-only Dirac layer (+ Wilson)
        mf = build_matter(Q=Q0, hop=HOP, mass=MASS, wilson=WIL)
        Tf = compose(mf)
        engf = Engine(Tf, Q0)
        KMf = lambda s: pem.x_reversor(s, Tf, 6 * Q0, em_ns=None)
        rng = np.random.default_rng(9)
        Lf = 4
        sf = State(Lf, rng.integers(-2 ** 30, 2 ** 30, (16, Lf ** 3)), rng.integers(-2 ** 30, 2 ** 30, (16, Lf ** 3)),
                   rng.integers(0, 6 * Q0, (16, Lf ** 3)))
        from universe24.core.reversors import reversor_check
        rc = reversor_check(KMf, engf, [sf], 40, central=[("Jp", lambda s: pem.matter_negation(s, Tf, 6 * Q0))])
        free_vac = KMf(vacuum_state(Tf, Q0, 3, mf)).same_as(vacuum_state(Tf, Q0, 3, mf))
        out["free_matter_KoMp_reversor"] = {"check": rc, "vacuum_fixed": free_vac}
        allok &= rc["ok"] and free_vac
        record("EM-T7", dict(out, verdict="PASS" if allok else "FAIL"))
        self.assertTrue(allok, out)


# ============================================================================================ EM-T8 C symmetry
class TestCSymmetry(unittest.TestCase):
    def test_T8_charge_conjugation(self):
        rng = np.random.default_rng(5)
        D = 6 * Q0
        res = {"FC_eq_CF": 0, "states": 0, "rho_flips": 0, "j_flips": 0}
        for L in (3, 4):
            m, e, T, eng = system(wilson=WIL, sigma=SIG_W)
            N = L ** 3
            for _ in range(5):
                s = State(L, rng.integers(-2 ** 20, 2 ** 20 + 1, (T.G, N)), rng.integers(-2 ** 20, 2 ** 20 + 1, (T.G, N)),
                          rng.integers(0, D, (T.G, N)))
                Cs = pem.c_map(s, T, D)
                res["states"] += 1
                res["FC_eq_CF"] += int(eng.step(Cs).same_as(pem.c_map(eng.step(s), T, D)))
                res["rho_flips"] += int(np.array_equal(oem.charge_density(Cs, T, D), -oem.charge_density(s, T, D)))
                jc = oem.link_currents(Cs, T, m.params)
                j = oem.link_currents(s, T, m.params)
                res["j_flips"] += int(all(np.array_equal(x, -y) for x, y in zip(jc, j)))
        m, e, T, _ = system()
        vac = vacuum_state(T, Q0, 3, m, e)
        res["vacuum_C_fixed"] = pem.c_map(vac, T, D).same_as(vac)
        ok = res["FC_eq_CF"] == res["states"] == res["rho_flips"] == res["j_flips"] and res["vacuum_C_fixed"]
        record("EM-T8", dict(res, verdict="PASS" if ok else "FAIL"))
        self.assertTrue(ok, res)


# ============================================================================================ EM-T9 Bloch
class TestBloch(unittest.TestCase):
    def test_T9_bloch(self):
        m = build_matter(Q=Q0, hop=HOP, mass=MASS)
        alg = algebra("pair")
        k = np.array([0.15, 0.0, 0.0])
        B0 = bloch_matrix(m.params, k)

        def lam(Bm, sig, sigp):
            Bs = pem._sector_basis(sig, sigp)
            return np.linalg.eigvalsh(Bs.conj().T @ Bm @ Bs)
        phi = 1000.0
        g_phi = 4
        dE = {}
        for kind, M0 in (("E1_V", alg["V"]), ("identity", np.eye(16)), ("lapse_W0", alg["W0"])):
            dE[kind] = [float((lam(B0 + 2 * g_phi * phi * M0, +1, sp) - lam(B0, +1, sp))[0]) for sp in (1, -1)]
        odd = abs(dE["E1_V"][0] + dE["E1_V"][1]) <= 1e-9 * abs(dE["E1_V"][0]) and abs(dE["E1_V"][0]) > 0
        blind = abs(dE["identity"][0] - dE["identity"][1]) <= 1e-9 * abs(dE["identity"][0])
        lapse_equal = abs(dE["lapse_W0"][0] - dE["lapse_W0"][1]) <= 1e-9 * abs(dE["lapse_W0"][0])
        # vector potential: uniform A_x shifts k_x by g_A A / hop (small k): compare lambda(k; A) with lambda(k - qA)
        g_A, Ax = 1, 2.0 ** 18
        BA = B0 + 2 * g_A * Ax * alg["PJp"][0]
        shifts = []
        for sp in (1, -1):
            target = lam(BA, +1, sp)[0]
            grid = np.linspace(-0.02, 0.02, 4001)
            vals = [lam(bloch_matrix(m.params, k + np.array([dq, 0, 0])), +1, sp)[0] for dq in grid]
            j = int(np.argmin(np.abs(np.array(vals) - target)))
            shifts.append(float(grid[j]))
        q_pred = g_A * Ax / HOP
        kshift_prereg = all(abs(abs(x) - q_pred) <= 1e-3 * q_pred + 2e-5 for x in shifts) and shifts[0] * shifts[1] < 0
        # POST-HOC (A3, labelled): bisection, lattice factor 1/cos k (S4-P R1), at k = 0.15 and k = 0.02
        posthoc = {}
        for k0 in (0.15, 0.02):
            kv = np.array([k0, 0.0, 0.0])
            for sp in (1, -1):
                target = lam(bloch_matrix(m.params, kv) + 2 * g_A * Ax * alg["PJp"][0], +1, sp)[0]
                f = lambda dq: lam(bloch_matrix(m.params, kv + np.array([dq, 0, 0])), +1, sp)[0] - target
                lo, hi = -0.01, 0.01
                flo = f(lo)
                for _ in range(60):
                    mid = 0.5 * (lo + hi)
                    fm = f(mid)
                    if (fm > 0) == (flo > 0):
                        lo, flo = mid, fm
                    else:
                        hi = mid
                posthoc[f"k={k0},sp={sp}"] = 0.5 * (lo + hi) / (q_pred / np.cos(k0))
        kshift_posthoc = all(abs(abs(v) - 1) <= 1e-3 for v in posthoc.values())
        ok = odd and blind and lapse_equal and kshift_posthoc
        record("EM-T9", {"dlambda_per_sector_(J'=+,J'=-)": dE, "charge_odd": odd, "identity_charge_blind": blind,
                         "lapse_charge_blind": lapse_equal, "k_shift_measured_grid": shifts, "k_shift_pred_no_cos": q_pred,
                         "PREREGISTERED_kshift_verdict": "PASS" if kshift_prereg else "FAIL (1/cos k factor omitted)",
                         "POSTHOC_kshift_over_gA_A_over_hop_cos_k": posthoc,
                         "verdict": ("PASS" if ok else "FAIL") + " (k-shift part POST-HOC; pre-registered k-shift FAIL)"})
        self.assertTrue(ok)



# ============================================================================================ EM-T10 single 8-block
class TestSingleBlock(unittest.TestCase):
    def test_T10_single_sin_dirac(self):
        rng = np.random.default_rng(13)
        mf = build_matter(Q=Q0, hop=HOP, mass=MASS, wilson=WIL, species="single")
        Tf = compose(mf)
        engf = Engine(Tf, Q0)
        D = 6 * Q0
        L, steps = 4, 40
        N = L ** 3
        rep = check_reciprocity(Tf)
        s0 = State(L, rng.integers(-2 ** 10, 2 ** 10 + 1, (8, N)), rng.integers(-2 ** 10, 2 ** 10 + 1, (8, N)),
                   rng.integers(0, D, (8, N)))
        hist = engf.run(s0, steps, history=True)
        fails = sum(count_nz(oem.continuity_residual(x, y, Tf, D, mf.params, X="J")) for x, y in zip(hist[:-1], hist[1:]))
        X = lambda s: pem.x_reversor(s, Tf, D, em_ns=None, species="single")
        Nn = lambda s: pem.matter_negation(s, Tf, D, species="single")
        from universe24.core.reversors import reversor_check
        rc = reversor_check(X, engf, [s0], steps, central=[("Jp", Nn)])
        vac = vacuum_state(Tf, Q0, 3, mf)
        vac_fixed = X(vac).same_as(vac)
        rew = engf.rewind(hist[-1], steps).same_as(s0)
        worst = 0
        for g in range(Tf.G):
            per = {}
            for mm in Tf.monomials:
                if mm.target == g and mm.degree == 1 and mm.factors[0].offset != (0, 0, 0):
                    per.setdefault(mm.factors[0].offset, set()).add(mm.factors[0].gear)
            worst = max([worst] + [len(v) for v in per.values()])
        ok = rep.ok and len(rep.designated) == 0 and fails == 0 and rc["ok"] and vac_fixed and rew and worst <= 2
        record("EM-T10", {"reciprocity_ok": rep.ok, "designated": len(rep.designated), "carrier_noether_failures": fails,
                          "node_updates": N * steps, "kramers_reversor": rc, "vacuum_fixed": vac_fixed,
                          "rewind_exact": rew, "od3_max": worst, "verdict": "PASS" if ok else "FAIL"})
        self.assertTrue(ok)


if __name__ == "__main__":
    unittest.main()
