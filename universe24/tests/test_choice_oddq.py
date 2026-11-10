"""TC.18 (pre-registration 8, NOTES_choice.md 10:38:03 UTC): the near-matched router at the integrator's odd Q = 2^29+1.

    OMP_NUM_THREADS=2 nice -n 10 python -m unittest universe24.tests.test_choice_oddq -v
"""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from fractions import Fraction as Fr
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np  # noqa: E402

from universe24.core import Engine, compose  # noqa: E402
from universe24.layers.choice import build_clock_ring  # noqa: E402
from universe24.layers.choice_oddq import (build_odd_q_router, near_matched_kappa,  # noqa: E402
                                                            predicted_non_detection)
from universe24.observe.choice import click_flags  # noqa: E402
from universe24.prepare.choice import Prep, ring_state  # noqa: E402

RES = Path("runs/tests") / "choice"


def stamp():
    return subprocess.run(["date", "-u"], capture_output=True, text=True).stdout.strip()


class TestChoiceOddQ(unittest.TestCase):
    def test_TC18_router_at_integrator_q(self):
        t0 = stamp()
        Q, A = 2 ** 29 + 1, 1
        D = 6 * Q
        kappa = near_matched_kappa(Q, A)
        self.assertEqual(kappa, 3 * 2 ** 26)
        self.assertEqual(predicted_non_detection(Q, A), Fr(1, Q))
        a1 = build_clock_ring(Q=Q, prefix="X", name="arm1")
        a2 = build_clock_ring(Q=Q, prefix="X", name="arm2")
        X1 = tuple(f"arm1.X{j}" for j in range(3))
        X2 = tuple(f"arm2.X{j}" for j in range(3))
        rt = build_odd_q_router(Q=Q, A=A, arm1=X1, arm2=X2, name="router")
        T = compose(a1, a2, rt)
        eng = Engine(T, Q)
        rng = np.random.default_rng(29)
        rows, rew, bad = [], True, 0
        for s in range(6):
            Ip = sum((p + q) ** 2 for (_, p), (_, q) in zip(ring_state(A, 0), ring_state(A, s)))
            Im = 8 * A * A - Ip
            Kp, Km = 2 * kappa * Ip, 2 * kappa * Im
            edges = [0, Km, D - Kp, D - 1]
            toks = sorted({t for e in edges for t in range(e - 8, e + 9) if 0 <= t < D}
                          | {int(v) for v in rng.integers(0, D, 20000)})
            n = len(toks)
            L = 3
            while L ** 3 < n:
                L += 1
            pr = Prep(T, Q, L, a1, a2, rt)
            nodes = np.arange(n)
            for arm, ph in ((X1, 0), (X2, s)):
                for j, (av, bv) in enumerate(ring_state(A, ph)):
                    pr.set(arm[j], nodes, a=av, b=bv)
            lam = np.array(toks, dtype=object)
            pr.set("router.dP", nodes, r=lam)
            pr.set("router.dM", nodes, r=lam)
            s0 = pr.state()
            s1 = eng.step(s0)
            rew &= eng.inverse_step(s1).same_as(s0)
            fl = click_flags(T, D, s0, s1)
            cp, cm = fl[T.gear_index("router.dP")][nodes], fl[T.gear_index("router.dM")][nodes]
            for i, t in enumerate(toks):
                want_p, want_m = t >= D - Kp, t < Km
                bad += (bool(cp[i]) != want_p) or (bool(cm[i]) != want_m)
            none_toks = [t for i, t in enumerate(toks) if not cp[i] and not cm[i]]
            self.assertFalse(bool((cp & cm).any()))
            self.assertTrue(all(Km <= t < D - Kp for t in none_toks))
            rows.append({"s": s, "I+": Ip, "K+": Kp, "K-": -Km, "tokens_checked": n, "none_tokens": len(none_toks),
                         "arc_P(none)": str(Fr(D - Kp - Km, D)),
                         "arc_P(+|detected)": str(Fr(Kp, Kp + Km))})
        RES.mkdir(parents=True, exist_ok=True)
        (RES / "TC.18.json").write_text(json.dumps({"Q": Q, "D": D, "kappa": kappa, "S": 16 * kappa * A * A,
                                                    "pred_P(none)": str(predicted_non_detection(Q, A)), "rows": rows,
                                                    "mismatches_vs_arc_law": bad, "rewind": rew, "_started": t0,
                                                    "_finished": stamp()}, indent=1))
        self.assertEqual(bad, 0)
        self.assertTrue(rew)
        self.assertEqual([r["arc_P(+|detected)"] for r in rows], ["1", "3/4", "1/4", "0", "1/4", "3/4"])
        self.assertEqual({r["arc_P(none)"] for r in rows}, {str(Fr(1, Q))})


if __name__ == "__main__":
    unittest.main()
