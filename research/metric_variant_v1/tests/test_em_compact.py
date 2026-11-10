"""Compact-U(1) EM candidate tests EM-C1 ... EM-C3 (pre-registered in NOTES_em.md §4 before any run).

Run from the repository root:
    OMP_NUM_THREADS=2 nice -n 10 python -m unittest research.metric_variant_v1.tests.test_em_compact -v
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np

from research.metric_variant_v1.core import Engine, State, check_reciprocity, compose
from research.metric_variant_v1.core.reversors import uniform
from research.metric_variant_v1.layers.em_compact import default_compact
from research.metric_variant_v1.observe import em as oem
from research.metric_variant_v1.observe import em_compact as oc
from research.metric_variant_v1.prepare import vacuum_state
from research.metric_variant_v1.prepare import em as pem
from research.metric_variant_v1.prepare import em_compact as pc
from research.metric_variant_v1.tests.test_em import count_nz, record

Q0 = (1 << 29) + 1
D = 6 * Q0


def system(kw=0):
    m, links, c = default_compact(Q0, kw=kw)
    T = compose(m, links, c)
    return (m, links, c), T, Engine(T, Q0)


def gauss_fail(hist, T, links):
    f = 0
    glob = 0
    for s0, s1 in zip(hist[:-1], hist[1:]):
        res = oc.gauss_step_residual(s0, s1, T, links.params, D)
        f += count_nz(res)
        glob += int(res.sum() != 0)
    return f, glob


class TestCompact(unittest.TestCase):
    def test_C2_reciprocity_and_structure(self):
        out = {}
        ok = True
        for kw in (0, 1 << 10):
            blocks, T, _ = system(kw)
            rep = check_reciprocity(T)
            out[f"kw={kw}"] = dict(ok=rep.ok, checked=rep.checked, designated=len(rep.designated),
                                   skipped_two_time=rep.skipped_two_time, rank=T.rank, G=T.G, monomials=len(T),
                                   census=T.census(), support_violations=len(T.support_violations()),
                                   b_only=T.b_only, constants=T.has_constant)
            ok &= rep.ok and len(rep.designated) == 0 and T.b_only and not T.has_constant
        record("EM-C2", dict(out, verdict="PASS" if ok else "FAIL"))
        self.assertTrue(ok, out)

    def test_C1_C3_gauss_rewind_mirror(self):
        out = {}
        allok = True
        rng = np.random.default_rng(21)
        for kw in (0, 1 << 10):
            blocks, T, eng = system(kw)
            L, steps = 4, 30
            N = L ** 3
            vac = vacuum_state(T, Q0, L, *blocks)
            fvac = eng.step(vac).same_as(vac)
            Mp = uniform(T, Q0, "Mp")
            mvac = Mp(vac).same_as(vac)
            a = rng.integers(-2 ** 10, 2 ** 10 + 1, (T.G, N))
            b = rng.integers(-2 ** 10, 2 ** 10 + 1, (T.G, N))
            r = rng.integers(0, D, (T.G, N))
            s0 = State(L, a, b, r)
            hist = eng.run(s0, steps, history=True)
            gf, gglob = gauss_fail(hist, T, blocks[1])
            rew = eng.rewind(hist[-1], steps).same_as(s0)
            z = Mp(hist[-1])
            for _ in range(steps):
                z = eng.step(z)
            mir = Mp(z).same_as(s0)
            ok = gf == 0 and gglob == 0 and rew and mir and fvac and mvac
            allok &= ok
            out[f"random_kw={kw}"] = dict(gauss_failures=gf, global_failures=gglob, node_updates=N * steps,
                                          rewind_exact=rew, Mp_mirror_30_30=mir, F_vac_fixed=fvac, Mp_vac_fixed=mvac,
                                          max_abs=hist[-1].max_abs(), stats=dict(eng.stats), ok=ok)
        # (b) moving pair with Gauss-prepared links
        blocks, T, eng = system(0)
        m, links, c = blocks
        L, steps = 6, 40
        vac = vacuum_state(T, Q0, L, *blocks)
        ap, bp, _ = pem.dirac_packet(m.params, L, +1, 1.3, 2 ** 9, kc=(0.4, 0, 0), center=(1, 3, 3))
        an, bn, _ = pem.dirac_packet(m.params, L, +1, 1.3, 2 ** 9, kc=(-0.4, 0, 0), center=(4, 3, 3))
        s0 = pem.set_matter(vac, T, "matter", ap + pem.c_image(an), bp + pem.c_image(bn))
        rho = oem.charge_density(s0, T, D)
        s0 = pc.gauss_links(s0, T, rho, links.params["A"], D)
        G0 = oc.gauss_G(s0, T, links.params, D)
        hist = eng.run(s0, steps, history=True)
        gf, gglob = gauss_fail(hist, T, links)
        rew = eng.rewind(hist[-1], steps).same_as(s0)
        rel0 = float(np.abs(np.asarray(G0, float)).max() / max(np.abs(np.asarray(rho, float)).max(), 1))
        ok = gf == 0 and gglob == 0 and rew
        allok &= ok
        out["pair_prepared"] = dict(gauss_failures=gf, global_failures=gglob, node_updates=L ** 3 * steps,
                                    rewind_exact=rew, initial_gauss_residual_rel=rel0,
                                    link_norm_dev_final=oc.link_norm_dev(hist[-1], T, links.params), ok=ok)
        record("EM-C1_C3", dict(out, verdict="PASS" if allok else "FAIL"))
        self.assertTrue(allok, out)


if __name__ == "__main__":
    unittest.main()
