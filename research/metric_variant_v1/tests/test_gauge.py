"""B1-GAUGE acceptance tests G1-G9 (pre-registered in NOTES_gauge.md, 09:34:28 UTC). Each test writes
results/gauge/<test>.json with its own `date -u`-equivalent UTC stamp.

Run (from the repository root):
    OMP_NUM_THREADS=2 nice -n 10 python -m unittest research.metric_variant_v1.tests.test_gauge -v
The long spring runs (G6) are opt-in: set GAUGE_LONG=1 (they take minutes).
"""
from __future__ import annotations

import json
import os
import random
import time
import unittest
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from ..core.engine import OBJ, Engine, State
from ..core.reciprocity import check_reciprocity
from ..core.reversors import GearwiseMap, uniform
from ..core.tensor import compose
from ..layers.gauge import ALGEBRAS, DEFAULT_Q, build_gauge, default_gauge_blocks
from ..layers.links import build_c1_weights, build_c2
from ..layers.reference import build_reference
from ..observe.audit import frozen_equivalence
from ..observe.gauge import C2View, GaugeView, joint_mirror, layer_census
from ..prepare import vacuum_state
from ..prepare.gauge import random_gauge_state

OUT = Path(__file__).resolve().parent.parent / "results" / "gauge"
Q0 = (1 << 19) + 1                      # 524289, odd
D0 = 6 * Q0


def params(group, use_P=True, lam=2, Q=Q0):
    D = 6 * Q
    return dict(group=group, Q=Q, A=256, kappa=(Q - 1) // 512, mass=Q + 3, lam=lam, use_P=use_P,
                kappa_P=256 if use_P else 0, c_P=0, beta=(D - (1 << 19)) if use_P else 0, name=group)


def stamp():
    return datetime.now(timezone.utc).strftime("%a %b %d %H:%M:%S UTC %Y")


def write(name, data):
    OUT.mkdir(parents=True, exist_ok=True)
    data = dict(data)
    data["stamp_utc"] = stamp()
    (OUT / f"{name}.json").write_text(json.dumps(data, indent=1, default=str))


def layer(group, use_P=True, lam=2):
    blk = build_gauge(**params(group, use_P, lam))
    T = compose(blk)
    return blk, T, Engine(T, blk.Q), GaugeView(T, blk.params, blk.name)


def random_ref_state(T, Q, L, seed, amp=20, sparse=None):
    """Reference gears random (r on the Q-lattice), every other gear at its vacuum (0, 0, 3Q-1)."""
    rng = random.Random(seed)
    N = L ** 3
    a = np.zeros((T.G, N), dtype=object)
    b = np.zeros((T.G, N), dtype=object)
    r = np.full((T.G, N), 3 * Q - 1, dtype=object)
    for i, nm in enumerate(T.names):
        if nm.startswith("ref."):
            r[i] = [2 * Q] * N
            for n in range(N):
                if sparse is None or rng.random() < sparse:
                    a[i, n] = rng.randint(-amp, amp)
                    b[i, n] = rng.randint(-amp, amp)
                    r[i, n] = Q * rng.randrange(6)
    return State(L, a, b, r)


class G1Build(unittest.TestCase):
    def test_G1_build_reciprocity_locality(self):
        rows = []
        for group in ("u1", "su2", "su3"):
            for use_P in (False, True):
                for lam in (0, 2):
                    blk = build_gauge(**params(group, use_P, lam))
                    T = compose(blk)
                    rep = check_reciprocity(T)
                    cen = T.census()
                    supp = T.support_violations()
                    supp_targets = sorted({T.names[m.target].split(".")[1].split("_")[0] for m in supp})
                    rows.append({"group": group, "use_P": use_P, "lam": lam, "G": T.G, "monomials": len(T),
                                 "rank": T.rank, "reciprocal": rep.ok, "checked": rep.checked,
                                 "designated": len(rep.designated), "census": cen, "b_only": T.b_only,
                                 "constants": T.has_constant, "support_violations": len(supp),
                                 "support_violation_targets": supp_targets, "P0": blk.params["P0"],
                                 "c_U": blk.params["c_U"]})
                    self.assertTrue(rep.ok)
                    self.assertEqual(len(rep.designated), 0)
                    self.assertTrue(T.b_only)
                    self.assertFalse(T.has_constant)
                    if lam == 0:
                        self.assertEqual(cen["by_degree"][3], 0)      # rank 4 only through the spring
                    else:
                        self.assertEqual(T.rank, 4)
                    if not use_P:
                        self.assertEqual(len(supp), 0)
        # c2 / c1
        for Q in (4095, Q0):
            for algebra in ("ZQ8", "H"):
                ref = build_reference(Q=Q)
                c2 = build_c2(Q=Q, kappa=Q, lam=Q, algebra=algebra)
                T = compose(ref, c2, q_lattice=("ref.*",))
                rep = check_reciprocity(T)
                cen = T.census()
                rows.append({"block": f"c2-{algebra}", "Q": Q, "G": T.G, "monomials": len(T), "rank": T.rank,
                             "reciprocal": rep.ok, "checked": rep.checked, "census": cen,
                             "q_lattice_violations": len(T.q_lattice_violations(("ref.*",))),
                             "support_violations": len(T.support_violations()), "b_only": T.b_only,
                             "constants": T.has_constant})
                self.assertTrue(rep.ok)
                self.assertEqual(T.q_lattice_violations(("ref.*",)), [])
                self.assertEqual(len(T.support_violations()), 0)
                self.assertFalse(T.has_constant)
        ref = build_reference(Q=4095)
        c1 = build_c1_weights(Q=4095, kappa=4095, lam=4095)
        T = compose(ref, c1, q_lattice=("ref.*",))
        rep = check_reciprocity(T)
        rows.append({"block": "c1-port-weights", "Q": 4095, "G": T.G, "monomials": len(T), "rank": T.rank,
                     "reciprocal": rep.ok, "support_violations": len(T.support_violations())})
        self.assertTrue(rep.ok)
        # integer generators: antisymmetric on matter (n x n) and on links (left and right multiplication)
        gen_rows = []
        for group, alg in ALGEBRAS.items():
            for lab, X in alg.generators:
                Mm, Lm, Rm = alg.act_matrix(X), alg.left_matrix(X), alg.right_matrix(X)
                anti = all(Mm[i][j] == -Mm[j][i] for i in range(alg.n) for j in range(alg.n)) and \
                    all(Lm[i][j] == -Lm[j][i] and Rm[i][j] == -Rm[j][i] for i in range(alg.m) for j in range(alg.m))
                gen_rows.append({"group": group, "generator": lab, "integer_antisymmetric": anti,
                                 "matter_matrix": Mm if group == "su3" else None})
                self.assertTrue(anti)
        # the integer gauge groups are closed (exact subgroups) and unitary (X^dag X = 1)
        for group, alg in ALGEBRAS.items():
            els = {tuple(g) for g in alg.group}
            closed = all(tuple(alg.prod(list(g), list(h))) in els for g in alg.group for h in alg.group)
            unitary = all(alg.prod(alg.dagger(list(g)), list(g)) == list(alg.one) for g in alg.group)
            gen_rows.append({"group": group, "integer_subgroup_order": len(els), "closed": closed, "unitary": unitary})
            self.assertTrue(closed and unitary)
        write("G1", {"rows": rows, "generators_and_groups": gen_rows})
        # census (ARCH R3/R4/R6): monomials targeting each block's gears
        cen = {}
        for group in ("u1", "su2", "su3"):
            for use_P in (False, True):
                for lam in (0, 2):
                    cen[f"{group}{'+P' if use_P else ''} lam={lam}"] = layer_census(
                        compose(build_gauge(**params(group, use_P, lam))), group + ".")
        for blk in default_gauge_blocks():
            cen[f"DEFAULT {blk.name} (regime F, lam=4, 2-path)"] = layer_census(compose(blk), blk.name + ".")
        Q = 4095
        ref = build_reference(Q=Q)
        for algebra in ("ZQ8", "H"):
            for lam in (0, Q):
                T = compose(ref, build_c2(Q=Q, kappa=Q, lam=lam, algebra=algebra), q_lattice=("ref.*",))
                cen[f"c2-{algebra} lam={lam}: links"] = layer_census(T, "c2.")
                cen[f"c2-{algebra} lam={lam}: L0 rows"] = layer_census(T, "ref.")
        T = compose(ref, build_c1_weights(Q=Q, kappa=Q, lam=Q), q_lattice=("ref.*",))
        cen["c1 lam=Q: links"] = layer_census(T, "c1.")
        cen["c1 lam=Q: L0 rows"] = layer_census(T, "ref.")
        cen["reference alone: L0 rows"] = layer_census(compose(ref), "ref.")
        for k, v in cen.items():
            self.assertEqual(v["a_read_monomials"], 0)
            self.assertEqual(v["constants"], 0)
        write("census", cen)


class G2Vacuum(unittest.TestCase):
    def test_G2_vacuum(self):
        out = {}
        L = 4
        for group in ("u1", "su2", "su3"):
            blk, T, E, V = layer(group)
            vac = vacuum_state(T, blk.Q, L, blk)
            s = vac
            changed = clicks = 0
            for _ in range(50 if group != "su3" else 20):
                s1 = E.step(s)
                changed += int(not s1.same_as(s))
                clicks += len(E.clicks(s, s1, stream="raw"))
                s = s1
            out[group] = {"updates": 50 if group != "su3" else 20, "changed_updates": changed, "raw_clicks": clicks}
            self.assertEqual(changed, 0)
            self.assertEqual(clicks, 0)
        # reference + su2 + c2 (kappa = Q): the composed vacuum stays the reference vacuum x Q
        Q = Q0
        ref = build_reference(Q=Q)
        su2 = build_gauge(**params("su2"))
        c2 = build_c2(Q=Q, kappa=Q, lam=Q)
        T = compose(ref, su2, c2, q_lattice=("ref.*",))
        E = Engine(T, Q)
        vac = vacuum_state(T, Q, 3, ref, su2, c2)
        s = E.run(vac, 30)
        out["ref+su2+c2"] = {"updates": 30, "unchanged": s.same_as(vac)}
        self.assertTrue(s.same_as(vac))
        write("G2", out)


class G3Noether(unittest.TestCase):
    def test_G3_gauss_identity(self):
        out = {}
        for group, L, T_, amp in (("u1", 4, 40, 64), ("su2", 4, 40, 64), ("su3", 3, 20, 64)):
            for use_P in (False, True):
                blk, T, E, V = layer(group, use_P)
                vac = vacuum_state(T, blk.Q, L, blk)
                s0 = random_gauge_state(T, blk, vac, seed=11, amp_matter=amp, amp_noise=8, amp_path=16)
                hist = E.run(s0, T_, history=True)
                g = V.gauss_check(hist)
                # colour flow: matter-only vs total (generator 0)
                lab, X = V.alg.generators[0]
                mat = [int(sum(V.charge(h, X, "matter"))) for h in hist[1:]]
                tot = [int(sum(V.charge(h, X, "all"))) for h in hist[1:]]
                scale = max(1, max(abs(v) for v in mat))
                rec = {"L": L, "updates": T_, "generators": [l for l, _ in V.alg.generators], **g,
                       "matter_total_charge_swing_rel": (max(mat) - min(mat)) / scale,
                       "total_charge_drift_rel": (max(tot) - min(tot)) / scale,
                       "stats": dict(E.stats)}
                out[f"{group}{'+P' if use_P else ''}"] = rec
                self.assertEqual(g["failures"], 0)
                self.assertGreater(g["checks"], 0)
        write("G3", out)


class G4Covariance(unittest.TestCase):
    def test_G4_local_covariance(self):
        out = {}
        for group, L, T_ in (("u1", 4, 30), ("su2", 4, 30), ("su3", 3, 15)):
            blk, T, E, V = layer(group, True)
            vac = vacuum_state(T, blk.Q, L, blk)
            s0 = random_gauge_state(T, blk, vac, seed=21, amp_matter=64, amp_noise=8, amp_path=16)
            res = []
            for seed in (1, 2):
                rng = random.Random(seed)
                gf = [rng.choice(V.alg.group) for _ in range(L ** 3)]
                FT = E.run(s0, T_)
                lhs = E.run(V.gauge_map(s0, gf), T_)
                rhs = V.gauge_map(FT, gf)
                w_ok = all(bool(np.all(V.wilson(FT, k1, k2) == V.wilson(rhs, k1, k2)))
                           for k1, k2 in ((0, 1), (1, 2), (0, 2)))
                vac_fixed = V.gauge_map(vac, [V.alg.one] * (L ** 3)).same_as(vac)
                res.append({"seed": seed, "covariant": lhs.same_as(rhs), "wilson_invariant": w_ok,
                            "identity_map_fixes_vacuum": vac_fixed})
                self.assertTrue(lhs.same_as(rhs))
                self.assertTrue(w_ok)
            out[group] = {"L": L, "updates": T_, "group_order": len(V.alg.group), "runs": res}
        write("G4", out)


class G5Reversors(unittest.TestCase):
    def test_G5_rewind_mirror(self):
        out = {}
        for group, L, T_ in (("u1", 4, 40), ("su2", 4, 40), ("su3", 3, 15)):
            blk, T, E, V = layer(group, True)
            vac = vacuum_state(T, blk.Q, L, blk)
            s0 = random_gauge_state(T, blk, vac, seed=31, amp_matter=64, amp_noise=8, amp_path=16)
            sT = E.run(s0, T_)
            rew = E.rewind(sT, T_).same_as(s0)
            M = uniform(T, blk.Q, "M")
            Mp = uniform(T, blk.Q, "Mp")
            mirror_M = M(E.run(M(sT), T_)).same_as(s0)
            mirror_Mp = Mp(E.run(Mp(sT), T_)).same_as(s0)
            vac_Mp = Mp(vac).same_as(vac)
            vac_M = M(vac).same_as(vac)
            out[group] = {"rewind": rew, "M_FMF": mirror_M, "Mp_FMpF": mirror_Mp, "Mp_fixes_vacuum": vac_Mp,
                          "M_fixes_vacuum": vac_M, "updates": T_, "L": L}
            self.assertTrue(rew and mirror_M and mirror_Mp and vac_Mp)
        # joint mirror for ref + c2 (kappa = Q): rhoL0 on ref.*, Mp on the links
        Q = 4095
        ref = build_reference(Q=Q)
        c2 = build_c2(Q=Q, kappa=Q, lam=Q)
        T = compose(ref, c2, q_lattice=("ref.*",))
        E = Engine(T, Q)
        L = 3
        s0 = random_ref_state(T, Q, L, seed=5, amp=1, sparse=0.05)
        choices = {nm: ("rhoL0" if nm.startswith("ref.") else "Mp") for nm in T.names}
        X = GearwiseMap(T, Q, choices)
        n = 12
        sT = E.run(s0, n)
        joint = X(E.run(X(sT), n)).same_as(s0)
        vac = vacuum_state(T, Q, L, ref, c2)
        out["ref+c2"] = {"joint_mirror_exact": joint, "joint_mirror_fixes_vacuum": X(vac).same_as(vac),
                         "rewind": E.rewind(sT, n).same_as(s0), "M_exact": uniform(T, Q, "M")(
                             E.run(uniform(T, Q, "M")(sT), n)).same_as(s0), "updates": n}
        self.assertTrue(joint and X(vac).same_as(vac))
        write("G5", out)


class G7LinksFrozen(unittest.TestCase):
    def test_G7_frozen(self):
        out = {}
        for Q in (4095, Q0):
            ref = build_reference(Q=Q)
            base = random_ref_state(compose(ref), Q, 4, seed=7, amp=20)
            for algebra in ("ZQ8", "H"):
                c2f = build_c2(Q=Q, kappa=0, lam=0, algebra=algebra)
                fr = frozen_equivalence((ref,), (c2f,), Q, base, 50)
                c2c = build_c2(Q=Q, kappa=Q, lam=Q, algebra=algebra)
                ctl = frozen_equivalence((ref,), (c2c,), Q, base, 2)
                out[f"Q{Q}-{algebra}"] = {"frozen": fr, "control_kappa_Q": ctl}
                self.assertTrue(fr["frozen"])
                self.assertFalse(ctl["frozen"])
        write("G7", out)


class G8C2Exactness(unittest.TestCase):
    def test_G8_c2(self):
        out = {}
        Q = 4095
        L = 3
        for algebra in ("ZQ8", "H"):
            ref = build_reference(Q=Q)
            c2 = build_c2(Q=Q, kappa=Q, lam=Q, algebra=algebra)
            T = compose(ref, c2, q_lattice=("ref.*",))
            E = Engine(T, Q)
            V = C2View(T, c2.params)
            s0 = random_ref_state(T, Q, L, seed=9, amp=1, sparse=0.05)
            # small link excitations too
            rng = random.Random(3)
            for k in range(3):
                for i in V.links[k]:
                    for n in range(L ** 3):
                        s0.a[i, n] = rng.randint(-1, 1) if rng.random() < 0.2 else 0
                        s0.b[i, n] = rng.randint(-1, 1) if rng.random() < 0.2 else 0
            s0 = State(L, s0.a, s0.b, s0.r)
            n = 10
            hist = E.run(s0, n, history=True)
            g = V.gauss_check(hist)
            rec = {"gauss": g, "rewind": E.rewind(hist[-1], n).same_as(s0),
                   "M": uniform(T, Q, "M")(E.run(uniform(T, Q, "M")(hist[-1]), n)).same_as(s0),
                   "max_abs_value_bits": int(hist[-1].max_abs()).bit_length(), "max_bits_per_update": [int(h.max_abs()).bit_length() for h in hist]}
            self.assertEqual(g["failures"], 0)
            self.assertTrue(rec["rewind"] and rec["M"])
            names = ("1", "i", "j", "k", "-1", "-i", "-j", "-k")
            if algebra == "ZQ8":
                for seed in (1, 2):
                    rr = random.Random(seed)
                    kf = [rr.choice(names) for _ in range(L ** 3)]
                    ok = E.run(V.gauge_map_zq8(s0, kf), n).same_as(V.gauge_map_zq8(hist[-1], kf))
                    rec[f"local_Q8_seed{seed}"] = ok
                    self.assertTrue(ok)
            else:
                for kname in ("i", "j", "k", "-1"):
                    kf = [kname] * (L ** 3)
                    ok = E.run(V.gauge_map_h(s0, kf, False), n).same_as(V.gauge_map_h(hist[-1], kf, False))
                    rec[f"global_{kname}"] = ok
                    self.assertTrue(ok)
                rr = random.Random(4)
                kf = [rr.choice(("1", "-1")) for _ in range(L ** 3)]
                ok = E.run(V.gauge_map_h(s0, kf, True), n).same_as(V.gauge_map_h(hist[-1], kf, True))
                rec["local_centre"] = ok
                self.assertTrue(ok)
                try:
                    kf = [rr.choice(("1", "i")) for _ in range(L ** 3)]
                    V.gauge_map_h(s0, kf, False)
                    rec["local_noncentral_integer"] = True
                except ValueError:
                    rec["local_noncentral_integer"] = False
            out[algebra] = rec
        write("G8", out)


if __name__ == "__main__":
    unittest.main()


def spring_run(group, use_P, lam, L, steps, amp_matter, seed=41, gauss_every=100, stop_factor=4.0):
    """One G6 arm: max relative link-norm deviation over the run, runaway time, sampled Gauss checks."""
    blk, T, E, V = layer(group, use_P, lam)
    vac = vacuum_state(T, blk.Q, L, blk)
    s = random_gauge_state(T, blk, vac, seed=seed, amp_matter=amp_matter, amp_noise=8, amp_path=16,
                           unit_links=False)
    dim = sum(V.alg.one)                 # |1|^2: 1 (H, C) or 3 (M3)
    A2 = blk.params["A"] ** 2 * dim
    worst = 0.0
    runaway = None
    g_checks = g_fail = 0
    series = []
    t0 = time.time()
    for t in range(steps):
        s1 = E.step(s)
        if gauss_every and t % gauss_every == 0:
            g = V.gauss_check([s, s1])
            g_checks += g["checks"]
            g_fail += g["failures"]
        s = s1
        n2 = V.link_norm2(s)
        hi = max(int(v) for v in n2.ravel())
        lo = min(int(v) for v in n2.ravel())
        dev = max(abs((hi / A2) ** 0.5 - 1.0), abs((lo / A2) ** 0.5 - 1.0))
        worst = max(worst, dev)
        if t % 100 == 99:
            series.append((t + 1, round(dev, 4), round((hi / A2) ** 0.5, 4)))
        if (hi / A2) ** 0.5 > stop_factor:
            runaway = t + 1
            break
    mat = max(abs(int(v)) for i in V.matter for v in s.b[i])
    return {"group": group, "use_P": use_P, "lam": lam, "L": L, "amp_matter": amp_matter,
            "steps_run": t + 1, "worst_rel_norm_dev": worst, "runaway_at": runaway,
            "gauss_sampled_checks": g_checks, "gauss_sampled_failures": g_fail,
            "final_max_matter_b": mat, "series_every_100": series, "seconds": round(time.time() - t0, 1),
            "int64_steps": E.stats["int64_steps"], "pyint_steps": E.stats["pyint_steps"]}


@unittest.skipUnless(os.environ.get("GAUGE_LONG"), "long spring runs: set GAUGE_LONG=1")
class G6SpringLong(unittest.TestCase):
    def test_G6_spring(self):
        rows = []
        arms = [("su2", True, 4), ("su3", False, 3)]
        for group, use_P, L in arms:
            for lam in (1, 2, 4, 0):
                rows.append(spring_run(group, use_P, lam, L, 2000, 256))
                write("G6_partial", {"rows": rows})
        (OUT / "G6_partial.json").unlink(missing_ok=True)
        write("G6", {"rows": rows, "criterion": "PASS iff worst_rel_norm_dev < 0.5 for every lam >= 1 and 0 sampled "
                                                "Gauss failures"})
        for r in rows:
            self.assertEqual(r["gauss_sampled_failures"], 0)
            if r["lam"] >= 1:
                self.assertIsNone(r["runaway_at"])
                self.assertLess(r["worst_rel_norm_dev"], 0.5)


def spring_run_fine(lam, steps, amp_matter, seed=43, L=4):
    """G6c arm: fine regime Q = 2^25 + 1, A = 4096 (see NOTES_gauge.md)."""
    Q = (1 << 25) + 1
    D = 6 * Q
    blk = build_gauge(group="su2", Q=Q, A=4096, kappa=(Q - 1) // 8192, mass=Q + 3, lam=lam, use_P=True,
                      kappa_P=256, c_P=0, beta=D - (1 << 25), name="su2")
    T = compose(blk)
    E = Engine(T, Q)
    V = GaugeView(T, blk.params, "su2")
    vac = vacuum_state(T, Q, L, blk)
    s = random_gauge_state(T, blk, vac, seed=seed, amp_matter=amp_matter, amp_noise=8, amp_path=16,
                           unit_links=False)
    A2 = 4096 ** 2
    worst, runaway, gc, gf, series = 0.0, None, 0, 0, []
    for t in range(steps):
        s1 = E.step(s)
        if t % 100 == 0:
            g = V.gauss_check([s, s1])
            gc += g["checks"]
            gf += g["failures"]
        s = s1
        n2 = V.link_norm2(s)
        hi, lo = max(int(v) for v in n2.ravel()), min(int(v) for v in n2.ravel())
        dev = max(abs((hi / A2) ** 0.5 - 1), abs((lo / A2) ** 0.5 - 1))
        worst = max(worst, dev)
        if t % 100 == 99:
            series.append((t + 1, round(dev, 4)))
        if (hi / A2) ** 0.5 > 4:
            runaway = t + 1
            break
    return {"group": "su2-fine", "use_P": True, "lam": lam, "L": L, "amp_matter": amp_matter, "steps_run": t + 1,
            "worst_rel_norm_dev": worst, "runaway_at": runaway, "gauss_sampled_checks": gc,
            "gauss_sampled_failures": gf, "series_every_100": series, "P0": blk.params["P0"]}


@unittest.skipUnless(os.environ.get("GAUGE_LONG"), "long spring runs: set GAUGE_LONG=1")
class G6bSpringCalibrated(unittest.TestCase):
    def test_G6b_spring(self):
        rows = []
        for group, use_P, L in (("su2", True, 4), ("su3", False, 3)):
            for lam in (1, 2, 4, 0):
                rows.append(spring_run(group, use_P, lam, L, 2000, 64))
                write("G6b_partial", {"rows": rows})
        for lam in (1, 2, 0):
            rows.append(spring_run_fine(lam, 2000, 1000))
            write("G6b_partial", {"rows": rows})
        for lam in (1, 2, 4, 0):                      # G6d: SU(3) with 2-path gears
            rows.append(spring_run("su3", True, lam, 3, 2000, 64))
            write("G6b_partial", {"rows": rows})
        (OUT / "G6b_partial.json").unlink(missing_ok=True)
        write("G6b", {"rows": rows, "criterion": "PASS iff worst_rel_norm_dev < 0.5 for every lam >= 1 and 0 sampled "
                                                 "Gauss failures (G6b: A_psi = 64; G6c: fine regime A_psi = 1000)"})
        for r in rows:
            self.assertEqual(r["gauss_sampled_failures"], 0)
            if r["lam"] >= 1:
                self.assertIsNone(r["runaway_at"])
                self.assertLess(r["worst_rel_norm_dev"], 0.5)


class G10DefaultSystem(unittest.TestCase):
    def test_G10_default_system(self):
        Q = DEFAULT_Q
        ref = build_reference(Q=Q)
        blocks = default_gauge_blocks()
        T = compose(ref, *blocks, q_lattice=("ref.*",))
        E = Engine(T, Q)
        rep = check_reciprocity(T)
        out = {"Q": T.Q, "G": T.G, "monomials": len(T), "reciprocal": rep.ok, "designated": len(rep.designated),
               "c2_or_c1_gears": sum(1 for n in T.names if n.startswith(("c2.", "c1."))),
               "q_lattice_violations": len(T.q_lattice_violations(("ref.*",))), "lam": [b.params["lam"] for b in blocks]}
        self.assertEqual(T.Q, Q)
        self.assertTrue(rep.ok)
        self.assertEqual(out["c2_or_c1_gears"], 0)
        L = 3
        vac = vacuum_state(T, Q, L, ref, *blocks)
        out["vacuum_fixed_20"] = E.run(vac, 20).same_as(vac)
        self.assertTrue(out["vacuum_fixed_20"])
        s0 = random_ref_state(T, Q, L, seed=12, amp=20)
        for i, blk in enumerate(blocks):
            s0 = random_gauge_state(T, blk, s0, seed=100 + i, amp_matter=1000, amp_noise=8, amp_path=16,
                                    unit_links=False)
        n = 10
        hist = E.run(s0, n, history=True)
        views = [GaugeView(T, b.params, b.name) for b in blocks]
        g_all = {}
        for V in views:
            g = V.gauss_check(hist)
            g_all[V.name] = g
            self.assertEqual(g["failures"], 0)
        out["gauss"] = g_all
        out["rewind"] = E.rewind(hist[-1], n).same_as(s0)
        X = joint_mirror(T, Q)
        out["joint_mirror"] = X(E.run(X(hist[-1]), n)).same_as(s0)
        out["joint_mirror_fixes_vacuum"] = X(vac).same_as(vac)
        rng = random.Random(77)
        gfs = [[rng.choice(V.alg.group) for _ in range(L ** 3)] for V in views]

        def G(state):
            for V, gf in zip(views, gfs):
                state = V.gauge_map(state, gf)
            return state
        out["local_covariance_all_three"] = E.run(G(s0), n).same_as(G(hist[-1]))
        base = random_ref_state(compose(ref), Q, L, seed=12, amp=20)
        fr = frozen_equivalence((ref,), tuple(blocks), Q, base, 20)
        out["reference_sector_unchanged_by_gauge_layers"] = fr
        for k in ("rewind", "joint_mirror", "joint_mirror_fixes_vacuum", "local_covariance_all_three"):
            self.assertTrue(out[k])
        self.assertTrue(fr["frozen"])
        write("G10", out)
