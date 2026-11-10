"""S1: the SPRING DEFAULT selection run (rule pre-registered in NOTES_gauge.md, 09:50:00 UTC). Exact integers.
Run from the repository root:
    OMP_NUM_THREADS=1 nice -n 10 python -m research.metric_variant_v1.demos.gauge.spring_select
Writes results/gauge/S1_spring_default.json (rows per seed + the per-candidate summary)."""
from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path

from ...core.engine import Engine
from ...core.tensor import compose
from ...layers.gauge import build_gauge
from ...observe.gauge import GaugeView
from ...prepare import vacuum_state
from ...prepare.gauge import random_gauge_state

OUT = Path(__file__).resolve().parent.parent.parent / "results" / "gauge" / "S1_spring_default.json"
REG = {"C": dict(Q=(1 << 19) + 1, A=256, amp=64, dP=1 << 19), "F": dict(Q=(1 << 25) + 1, A=4096, amp=1000, dP=1 << 25)}
CANDS = {"C": (4, 8, 16), "F": (2, 3, 4)}


def arm(group, regime, lam, seed, L, steps=2000):
    R = REG[regime]
    Q, A, D = R["Q"], R["A"], 6 * R["Q"]
    blk = build_gauge(group=group, Q=Q, A=A, kappa=(Q - 1) // (2 * A), mass=Q + 3, lam=lam, use_P=True, kappa_P=256,
                      c_P=0, beta=D - R["dP"], name=group)
    T = compose(blk)
    E = Engine(T, Q)
    V = GaugeView(T, blk.params, group)
    s = random_gauge_state(T, blk, vacuum_state(T, Q, L, blk), seed=seed, amp_matter=R["amp"], amp_noise=8,
                           amp_path=16, unit_links=False)
    A2 = A * A * sum(V.alg.one)
    worst, run, gc, gf = 0.0, None, 0, 0
    for t in range(steps):
        s1 = E.step(s)
        if t % 100 == 0:
            g = V.gauss_check([s, s1])
            gc += g["checks"]
            gf += g["failures"]
        s = s1
        n2 = V.link_norm2(s)
        hi, lo = max(int(v) for v in n2.ravel()), min(int(v) for v in n2.ravel())
        worst = max(worst, abs((hi / A2) ** 0.5 - 1), abs((lo / A2) ** 0.5 - 1))
        if (hi / A2) ** 0.5 > 4:
            run = t + 1
            break
    return {"group": group, "regime": regime, "lam": lam, "seed": seed, "L": L, "worst": worst, "runaway_at": run,
            "gauss_checks": gc, "gauss_failures": gf, "cfl_2lamA2_over_D": 2 * lam * A * A / D, "P0": blk.params["P0"]}


def main():
    rows, t0 = [], time.time()
    for group, L in (("su2", 4), ("su3", 3), ("u1", 4)):
        for regime in ("C", "F"):
            for lam in CANDS[regime]:
                for seed in (51, 52, 53):
                    rows.append(arm(group, regime, lam, seed, L))
    summary = {}
    for group in ("su2", "su3", "u1"):
        for regime in ("C", "F"):
            for lam in CANDS[regime]:
                rs = [r for r in rows if r["group"] == group and r["regime"] == regime and r["lam"] == lam]
                w = max(r["worst"] for r in rs)
                q = (w <= 0.30 and all(r["gauss_failures"] == 0 and r["runaway_at"] is None for r in rs)
                     and rs[0]["cfl_2lamA2_over_D"] <= 2 / 3 + 1e-12)
                summary[f"{group}:{regime}:lam={lam}"] = {"worst_over_seeds": w, "qualifies": q,
                                                          "cfl": rs[0]["cfl_2lamA2_over_D"]}
    OUT.write_text(json.dumps({"rows": rows, "summary": summary, "seconds": round(time.time() - t0, 1),
                               "stamp_utc": datetime.now(timezone.utc).strftime("%a %b %d %H:%M:%S UTC %Y")},
                              indent=1))
    for k, v in summary.items():
        print(k, v)


def s2():
    """S2 (NOTES_gauge.md 09:56:09): the default family at Q = 2^29 + 1 (A = 16384), u1 and su2 with 2-path gears."""
    from ...layers.gauge import default_regime
    Q = (1 << 29) + 1
    reg = default_regime(Q)
    lam = reg.pop("lam")
    rows, t0 = [], time.time()
    for group, L in (("u1", 4), ("su2", 4)):
        for seed in (51, 52, 53):
            blk = build_gauge(group=group, lam=lam, name=group, **reg)
            T = compose(blk)
            E = Engine(T, Q)
            V = GaugeView(T, blk.params, group)
            s = random_gauge_state(T, blk, vacuum_state(T, Q, 4, blk), seed=seed, amp_matter=4000, amp_noise=8,
                                   amp_path=16, unit_links=False)
            A2 = reg["A"] ** 2 * sum(V.alg.one)
            worst, run, gc, gf = 0.0, None, 0, 0
            for t in range(2000):
                s1 = E.step(s)
                if t % 100 == 0:
                    g = V.gauss_check([s, s1])
                    gc += g["checks"]
                    gf += g["failures"]
                s = s1
                n2 = V.link_norm2(s)
                hi, lo = max(int(v) for v in n2.ravel()), min(int(v) for v in n2.ravel())
                worst = max(worst, abs((hi / A2) ** 0.5 - 1), abs((lo / A2) ** 0.5 - 1))
                if (hi / A2) ** 0.5 > 4:
                    run = t + 1
                    break
            rows.append({"group": group, "seed": seed, "worst": worst, "runaway_at": run, "gauss_checks": gc,
                         "gauss_failures": gf, "P0": blk.params["P0"], "int64_steps": E.stats["int64_steps"],
                         "pyint_steps": E.stats["pyint_steps"]})
            print(rows[-1], flush=True)
    summary = {g: {"worst_over_seeds": max(r["worst"] for r in rows if r["group"] == g),
                   "qualifies": all(r["worst"] <= 0.30 and r["runaway_at"] is None and r["gauss_failures"] == 0
                                    for r in rows if r["group"] == g)} for g in ("u1", "su2")}
    out = {"Q": Q, "regime": {**reg, "lam": lam}, "rows": rows, "summary": summary, "seconds": round(time.time() - t0, 1),
           "stamp_utc": datetime.now(timezone.utc).strftime("%a %b %d %H:%M:%S UTC %Y")}
    (OUT.parent / "S2_default_family_Q2p29.json").write_text(json.dumps(out, indent=1))
    print(summary)


if __name__ == "__main__":
    import sys
    s2() if sys.argv[1:] == ["S2"] else main()
