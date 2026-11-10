"""IQ (pre-registered in NOTES_gravity.md): the DEFAULT gravity blocks at the integrator's Q = 2^29 + 1, P = 2^20,
k = 2^8. Usage: OMP_NUM_THREADS=1 python research/metric_variant_v1/demos/gravity/integrator_check.py"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))

import numpy as np

from research.metric_variant_v1.core import Engine, State, check_reciprocity, compose
from research.metric_variant_v1.layers import build_reference
from research.metric_variant_v1.layers import gravity as gr
from research.metric_variant_v1.prepare import vacuum_state

OUT = ROOT / "research/metric_variant_v1/results/gravity"


def main():
    P, k = 2 ** 20, 2 ** 8
    Q = gr.gravity_Q(P, k)
    assert Q == 2 ** 29 + 1
    at = gr.atom_spec("at", 2 * P * 31)
    li = gr.light_spec("light", Q)
    w = gr.weyl_spec("dir", s=4 * P * 8, m=4 * P * 4, wilson=4 * P)
    blocks = [build_reference(Q=Q), gr.build_metric(Q=Q)] + [gr.build_test_matter(m, Q=Q) for m in (at, li, w)] + \
        [gr.build_lapse(Q=Q, P=P, field="metric.h00", matters=[at, li, w]),
         gr.build_beta(Q=Q, P=P, k=k, field="metric.h00", matters=[at]),
         gr.build_od2(Q=Q, stress=gr.od2_hop_stress("dir", w, kappa=2),
                      reads=gr.od2_centred_lapse_read("od2", w, P, Q, g00=1))]
    T = compose(*blocks, q_lattice=("ref.*",))
    eng = Engine(T, Q)
    L = 4
    v = vacuum_state(T, Q, L, *blocks)
    s = v
    for _ in range(10):
        s = eng.step(s)
    vac_ok = s.same_as(v)
    rng = np.random.default_rng(5)
    a, b = np.zeros((T.G, L ** 3), dtype=np.int64), np.zeros((T.G, L ** 3), dtype=np.int64)
    for g, gt in enumerate(T.gears):
        hi = 20 if gt.name.startswith("ref.") else (4 if gt.label == "audit" else 16)
        a[g], b[g] = rng.integers(-hi, hi + 1, L ** 3), rng.integers(-hi, hi + 1, L ** 3)
    s0 = State(L, a, b, rng.integers(0, 6 * Q, (T.G, L ** 3)))
    s = eng.run(s0, 10)
    back = eng.rewind(s, 10)
    rep = check_reciprocity(T)
    out = {"Q": Q, "P": P, "k": k, "G": T.G, "monomials": len(T), "rank": T.rank, "stages": len(T.stages),
           "vacuum_fixed_10": vac_ok, "rewind_10_exact": back.same_as(s0), "engine_stats": dict(eng.stats),
           "reciprocity_ok": rep.ok, "checked": rep.checked, "designated": len(rep.designated),
           "two_time_skipped": rep.skipped_two_time,
           "written_utc": subprocess.run(["date", "-u"], capture_output=True, text=True).stdout.strip()}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "IQ.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
