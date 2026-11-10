"""CHIRAL-BUILDER acceptance tests CH1-CH9 (pre-registered in NOTES_chiral.md, 12:01:28 UTC, before these runs).
Each test writes results/chiral/<test>.json with its UTC stamp.

Run (from the repository root, ONE core):
    OMP_NUM_THREADS=1 nice -n 19 python -m unittest research.metric_variant_v1.tests.test_chiral -v
"""
from __future__ import annotations

import json
import unittest
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from ..core.engine import Engine
from ..core.reciprocity import check_reciprocity
from ..core.reversors import Composite, is_fixed, reversor_check
from ..core.tensor import compose
from ..layers.chiral import (CHIRAL_DEFAULT_ON, HIGGS, Q_DEFAULT, check_chiral_algebra, chiral_blocks,
                             compose_with_default)
from ..observe.chiral import ChiralView
from ..prepare import vacuum_state
from ..prepare.chiral import (chiral_system, gear_groups, j_minus_fraction, jpure_seed, random_chiral_state,
                              standard_maps)

OUT = Path(__file__).resolve().parent.parent / "results" / "chiral"
Q = Q_DEFAULT
L = 3


def stamp():
    return datetime.now(timezone.utc).strftime("%a %b %d %H:%M:%S UTC %Y")


def write(name, data):
    OUT.mkdir(parents=True, exist_ok=True)
    data = dict(data, written=stamp(), Q=Q)
    (OUT / f"{name}.json").write_text(json.dumps(data, indent=1, default=str))


_CACHE = {}


def alone():
    if "alone" not in _CACHE:
        T, blocks = chiral_system(Q)
        _CACHE["alone"] = (T, blocks, Engine(T, Q))
    return _CACHE["alone"]


def composed():
    if "composed" not in _CACHE:
        from ..layers.system import default_system
        base = default_system(Q, chiral=False, electroweak=False)
        sysc = compose_with_default(base, on=True)
        Tb, Tc = compose(*base.blocks), compose(*sysc.blocks)
        _CACHE["composed"] = (base, sysc, Tb, Tc, Engine(Tb, Q), Engine(Tc, Q))
    return _CACHE["composed"]


class TestChiral(unittest.TestCase):
    def test_CH1_algebra(self):
        res = check_chiral_algebra()
        write("CH1_algebra", {"checks": res, "default_on": CHIRAL_DEFAULT_ON})
        self.assertTrue(all(res.values()))
        self.assertFalse(CHIRAL_DEFAULT_ON)

    def test_CH2_tensor(self):
        T, blocks, _ = alone()
        rep = check_reciprocity(T)
        names = T.names
        groups = gear_groups(T, blocks)
        fam = {}
        for k in range(3):
            for g in groups["links"][k]:
                fam[T.gear_index(g)] = ("link", k)
        for key, gl in groups["paths"].items():
            for g in gl:
                fam[T.gear_index(g)] = ("path", key)
        for g in groups["higgs"]:
            fam[T.gear_index(g)] = ("higgs",)
        deg3 = [m for m in T.monomials if m.degree == 3]
        bad4 = [m for m in deg3 if not (m.target in fam and all(fam.get(f.gear) == fam[m.target]
                                                                  and f.offset == (0, 0, 0) for f in m.factors))]
        res = {"reciprocity_ok": rep.ok, "designated": len(T.designations), "rank": T.rank,
               "rank4_monomials": len(deg3), "rank4_not_spring": len(bad4), "census": T.census(), "G": T.G,
               "monomials": len(T.monomials), "b_only": T.b_only, "fingerprint": T.dynamics_fingerprint,
               "blocks": [(b.name, len(b.gears), len(b.terms)) for b in blocks]}
        write("CH2_tensor", res)
        self.assertTrue(rep.ok)
        self.assertEqual(len(T.designations), 0)
        self.assertLessEqual(T.rank, 4)
        self.assertEqual(len(bad4), 0)
        self.assertTrue(T.b_only)

    def test_CH2b_composed(self):
        base, sysc, Tb, Tc, _, _ = composed()
        res = {"base_designations": len(Tb.designations), "composed_designations": len(Tc.designations),
               "base_G": Tb.G, "composed_G": Tc.G, "added_blocks": [b.name for b in sysc.blocks[len(base.blocks):]],
               "chiral_info": sysc.info.get("chiral"), "composed_rank": Tc.rank,
               "same_designation_texts": sorted(map(str, Tb.designations.values())) ==
               sorted(map(str, Tc.designations.values())) or "partner lapse adds the default's own designation type"}
        write("CH2b_composed", res)
        self.assertGreaterEqual(len(Tc.designations), len(Tb.designations))

    def test_CH3_vacuum(self):
        T, blocks, E = alone()
        v0 = vacuum_state(T, Q, L, *blocks)
        s = v0
        fixed = True
        for _ in range(20):
            s = E.step(s)
            fixed &= s.same_as(v0)
        # one-step identity of the matter inputs at W = phi = 0 vs build_matter's free pair
        Tf = compose(blocks[0], blocks[1])
        Ef = Engine(Tf, Q)
        rng = np.random.default_rng(3)
        rows_c = [T.gear_index(n) for n in Tf.names]
        ident = True
        for _ in range(3):
            st = random_chiral_state(T, Q, L, rng, matter_amp=1 << 20, field_amp=0, groups=gear_groups(T, blocks),
                                     vacuum_r=True)
            # zero every non-matter deviation (W = phi = 0)
            a, b = st.a.copy(), st.b.copy()
            for g in range(T.G):
                if g not in rows_c:
                    a[g] = 0
                    b[g] = 0
            from ..core.engine import State
            st = State(L, a, b, st.r)
            sf = State(L, a[rows_c], b[rows_c], st.r[rows_c])
            uc = E.inputs(st)[rows_c]
            uf = Ef.inputs(sf)
            ident &= bool((uc.astype(object) == uf.astype(object)).all())
        res = {"alone_vacuum_fixed_20": bool(fixed), "alone_matter_input_identity_3_states": ident}
        # composed
        base, sysc, Tb, Tc, Eb, Ec = composed()
        vb = vacuum_state(Tb, Q, L, *base.blocks)
        vc = vacuum_state(Tc, Q, L, *sysc.blocks)
        rows_b = [Tc.gear_index(n) for n in Tb.names]
        sb, sc = vb, vc
        cfix = True
        for _ in range(5):
            sb, sc = Eb.step(sb), Ec.step(sc)
            cfix &= sc.same_as(vc) and sb.same_as(vb)
        from ..prepare.system import random_system_state
        rs = random_system_state(base, Tb, L, seed=11)
        from ..core.engine import State
        a = vc.a.astype(object).copy(); b = vc.b.astype(object).copy(); r = vc.r.astype(object).copy()
        a[rows_b], b[rows_b], r[rows_b] = rs.a.astype(object), rs.b.astype(object), rs.r.astype(object)
        rc = State(L, a, b, r)
        one = Ec.step(rc)
        oneb = Eb.step(rs)
        one_ident = bool((one.a[rows_b].astype(object) == oneb.a.astype(object)).all() and
                         (one.b[rows_b].astype(object) == oneb.b.astype(object)).all() and
                         (one.r[rows_b].astype(object) == oneb.r.astype(object)).all())
        res.update({"composed_vacuum_fixed_5": bool(cfix), "composed_one_step_identity_on_default_gears": one_ident})
        write("CH3_vacuum", res)
        self.assertTrue(fixed and ident and cfix and one_ident)

    def test_CH4_rewind(self):
        T, blocks, E = alone()
        rng = np.random.default_rng(5)
        s0 = random_chiral_state(T, Q, L, rng, groups=gear_groups(T, blocks))
        s = s0
        for _ in range(6):
            s = E.step(s)
        back = E.rewind(s, 6)
        ok_alone = back.same_as(s0)
        base, sysc, Tb, Tc, Eb, Ec = composed()
        from ..prepare.system import random_system_state
        from ..core.engine import State
        vc = vacuum_state(Tc, Q, L, *sysc.blocks)
        rows_b = [Tc.gear_index(n) for n in Tb.names]
        rs = random_system_state(base, Tb, L, seed=12)
        a = vc.a.astype(object).copy(); b = vc.b.astype(object).copy(); r = vc.r.astype(object).copy()
        a[rows_b], b[rows_b], r[rows_b] = rs.a.astype(object), rs.b.astype(object), rs.r.astype(object)
        rc = State(L, a, b, r)
        s = rc
        for _ in range(2):
            s = Ec.step(s)
        ok_comp = Ec.rewind(s, 2).same_as(rc)
        write("CH4_rewind", {"alone_T6": ok_alone, "composed_T2": ok_comp, "stats_alone": dict(E.stats),
                             "stats_composed": dict(Ec.stats)})
        self.assertTrue(ok_alone and ok_comp)

    def test_CH5_noether(self):
        T, blocks, E = alone()
        view = ChiralView(T, blocks[3], blocks[2])
        rng = np.random.default_rng(7)
        s = random_chiral_state(T, Q, L, rng, groups=gear_groups(T, blocks))
        hist = [s]
        for _ in range(6):
            hist.append(E.step(hist[-1]))
        res = view.gauss_check(hist)
        write("CH5_noether", res)
        self.assertEqual(res["failures"], 0)
        self.assertGreater(res["max_abs_matter_only_change"], 0)

    def test_CH6_discrete(self):
        T, blocks, E = alone()
        maps = standard_maps(T, blocks, Q, L)
        rng = np.random.default_rng(9)
        states = [random_chiral_state(T, Q, L, rng, groups=gear_groups(T, blocks)) for _ in range(2)]
        out = {}
        out["R*"] = reversor_check(maps["R*"], E, states, 4)
        Xt = maps["T_phys"]
        Z = Composite([Xt, Xt])
        out["T_phys"] = reversor_check(Xt, E, states, 4, central=[("X^2 (Kramers)", Z)])
        out["boardT"] = reversor_check(maps["boardT"], E, states, 4)
        fwd = {}
        for nm in ("CP", "P", "C"):
            X = maps[nm]
            okc = True
            for s in states:
                t1 = X(s)
                t2 = s
                for _ in range(4):
                    t1 = E.step(t1)
                    t2 = E.step(t2)
                okc &= t1.same_as(X(t2))
            fwd[nm] = "EXACT" if okc else "BROKEN"
        out["forward"] = fwd
        write("CH6_discrete", out)
        self.assertTrue(out["R*"]["ok"])
        self.assertTrue(out["T_phys"]["ok"] and out["T_phys"]["central"]["X^2 (Kramers)"] == len(states))
        self.assertFalse(out["boardT"]["ok"])
        self.assertEqual(fwd, {"CP": "EXACT", "P": "BROKEN", "C": "BROKEN"})

    def test_CH7_jpure_seed(self):
        T, blocks, E = alone()
        Ls = 6
        maps = standard_maps(T, blocks, Q, Ls)
        reps = {}
        for A in (1 << 10, 1 << 14):
            seed, rep = jpure_seed(T, blocks, Q, Ls, A=A)
            rep["full_state_Rstar_fixed"] = is_fixed(maps["R*"], seed)
            view = ChiralView(T, blocks[3], blocks[2])
            rep["N_J_view"] = view.j_number(seed)
            s = seed
            hist = [s]
            for _ in range(3):
                s = E.step(s)
                hist.append(s)
            rep["N_J_after_3"] = view.j_number(s)
            rep["J_minus_fraction_after_3"] = j_minus_fraction(s, T, blocks, Q)
            rep["W_J_first_updates"] = view.click_wronskian(hist[0], hist[1], hist[2])
            reps[f"A=2^{A.bit_length() - 1}"] = rep
        r10, r14 = reps["A=2^10"], reps["A=2^14"]
        ratio = r10["J_minus_fraction"] / max(r14["J_minus_fraction"], 1e-300)
        out = {"seeds": reps, "ratio_Jminus_2^10_over_2^14": ratio,
               "legality": "ALONE: no constraint gears (legal). COMPOSED with E1: Gauss legality needs prepared fields "
                           "(rho(x) = -rho(-x) is not zero node by node): reported, not claimed."}
        write("CH7_jpure_seed", out)
        self.assertTrue(r10["exact_Rstar_fixed_matter"] and r14["exact_Rstar_fixed_matter"])
        self.assertTrue(r10["full_state_Rstar_fixed"] and r14["full_state_Rstar_fixed"])
        self.assertLess(r10["J_minus_fraction"], 1e-5)
        self.assertGreater(ratio, 100)
        self.assertNotEqual(r10["N_J"], 0)

    def test_CH8_int64(self):
        T, blocks, _ = alone()
        E = Engine(T, Q)
        v0 = vacuum_state(T, Q, L, *blocks)
        s = v0
        for _ in range(20):
            s = E.step(s)
        rng = np.random.default_rng(13)
        s = random_chiral_state(T, Q, L, rng, groups=gear_groups(T, blocks))
        for _ in range(10):
            s = E.step(s)
        res = {"stats": dict(E.stats), "max_abs_state_after_10": s.max_abs()}
        write("CH8_int64", res)
        self.assertEqual(E.stats["pyint_steps"], 0)

    def test_CH9_lapse_independence(self):
        T, blocks, _ = alone()
        names = T.names
        lapse_refs = [n for n in names if n.startswith(("metric.", "beta.", "od2.", "mlapse", "bgk."))]
        chiral_terms_ref = set()
        for blk in blocks[1:]:
            for t in blk.terms:
                for f in t[2]:
                    chiral_terms_ref.add(blk.qualify(f[0]))
        bad = [r for r in chiral_terms_ref if r.split(".")[0] in ("metric", "beta", "od2", "mlapse", "bgk")]
        from ..layers.system import default_system
        okC = okS = None
        try:
            sC = compose_with_default(default_system(Q, matter_lapse="C", chiral=False, electroweak=False), on=True)
            compose(*sC.blocks)
            okC = True
        except Exception as e:  # noqa: BLE001
            okC = repr(e)
        try:
            sS = compose_with_default(default_system(Q, matter_lapse="split", chiral=False, electroweak=False), on=True)
            compose(*sS.blocks)
            okS = True
            split_note = sS.info["chiral"].get("partner_lapse")
        except Exception as e:  # noqa: BLE001
            okS = repr(e)
            split_note = None
        res = {"alone_lapse_gears": lapse_refs, "chiral_blocks_read_lapse": bad, "compose_matter_lapse_C": okC,
               "compose_matter_lapse_split": okS, "split_partner_lapse_note": split_note}
        write("CH9_lapse_independence", res)
        self.assertEqual(bad, [])
        self.assertIs(okC, True)
        self.assertIs(okS, True)


if __name__ == "__main__":
    unittest.main()
