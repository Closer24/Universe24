"""G9 (c2 stability, report) and the EXPLORATORY c1 curved-vacuum stability test. Exact integers.

Run from the repository root:
    OMP_NUM_THREADS=2 nice -n 10 python -m research.metric_variant_v1.demos.gauge.links_stability
Writes demos/gauge/G9_c2_stability.json and demos/gauge/C1_stability.json.
"""
from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from ...core.engine import Engine, State
from ...core.lattice import lattice
from ...core.tensor import compose
from ...layers.links import build_c1_weights, build_c2
from ...layers.reference import build_reference
from ...prepare import vacuum_state

HERE = Path(__file__).resolve().parent


def stamp():
    return datetime.now(timezone.utc).strftime("%a %b %d %H:%M:%S UTC %Y")


def bits(arr) -> int:
    return max((abs(int(v)).bit_length() for v in np.asarray(arr).ravel()), default=0)


def run_track(E, s, steps, ref_rows, link_rows, cap_bits=4000):
    rows = []
    hit = None
    for t in range(steps):
        s = E.step(s)
        rb, lb = bits(s.b[ref_rows]), bits(s.b[link_rows]) if len(link_rows) else 0
        if t < 20 or t % 50 == 49:
            rows.append((t + 1, rb, lb))
        if max(rb, lb) > cap_bits:
            hit = t + 1
            break
    return s, rows, hit


def c2_stability():
    out = {}
    Q, L = 4095, 4
    for lam_mult in (1, 2):
        for label, seed_vals in (("single_quantum_b1", [("ref.R00", (1, 1, 1), (0, 1))]),
                                 ("three_quanta", [("ref.R00", (1, 1, 1), (0, 1)), ("ref.R17", (2, 1, 1), (1, 0)),
                                                   ("ref.R33", (1, 2, 2), (0, -1))])):
            for kappa in (0, Q):
                ref = build_reference(Q=Q)
                c2 = build_c2(Q=Q, kappa=kappa, lam=lam_mult * Q if kappa else 0)
                T = compose(ref, c2, q_lattice=("ref.*",))
                E = Engine(T, Q)
                s = vacuum_state(T, Q, L, ref, c2)
                lat = lattice(L)
                a, b = s.a.astype(object), s.b.astype(object)
                for nm, xyz, (va, vb) in seed_vals:
                    a[T.gear_index(nm), lat.index(*xyz)] = va
                    b[T.gear_index(nm), lat.index(*xyz)] = vb
                s = State(L, a, b, s.r)
                ref_rows = [T.gear_index(f"ref.R{g:02d}") for g in range(48)]
                link_rows = [i for i, n in enumerate(T.names) if n.startswith("c2.")]
                t0 = time.time()
                sf, rows, hit = run_track(E, s, 2000, ref_rows, link_rows)
                out[f"{label}:kappa={'Q' if kappa else 0}:lam={lam_mult}Q"] = {
                    "bits_ref_link_first20_then_every50": rows, "blow_up_at(>4000 bits)": hit,
                    "final_ref_bits": bits(sf.b[ref_rows]), "final_link_bits": bits(sf.b[link_rows]),
                    "nonzero_link_gears_final": int(np.sum(sf.b[link_rows] != 0)), "seconds": round(time.time() - t0, 1)}
    return out


def c1_stability():
    out = {}
    Q, L = 4095, 4
    ref = build_reference(Q=Q)
    for lam_mult in (1, 2):
        c1 = build_c1_weights(Q=Q, kappa=Q, lam=lam_mult * Q)
        T = compose(ref, c1, q_lattice=("ref.*",))
        E = Engine(T, Q)
        lat = lattice(L)
        vac = vacuum_state(T, Q, L, ref, c1)
        link_rows = [i for i, n in enumerate(T.names) if n.startswith("c1.")]
        ref_rows = [T.gear_index(f"ref.R{g:02d}") for g in range(48)]
        out[f"lam={lam_mult}Q:vacuum_fixed_200"] = E.run(vac, 200).same_as(vac)
        # (ii) weight pulse on one link, reference at vacuum
        a, b = vac.a.astype(object), vac.b.astype(object)
        for g in (0, 5, 17):
            b[T.gear_index(f"c1.Vx_{g:02d}"), lat.index(1, 1, 1)] = 1
        s = State(L, a, b, vac.r)
        sf, rows, hit = run_track(E, s, 2000, ref_rows, link_rows)
        out[f"lam={lam_mult}Q:weight_pulse"] = {"bits_ref_link": rows[:25], "blow_up_at": hit,
                                                "final_ref_bits": bits(sf.b[ref_rows]),
                                                "final_link_bits": bits(sf.b[link_rows])}
        # (iii) single reference quantum with dynamic weights vs frozen weights (kappa = 0)
        for kappa in (Q, 0):
            c1k = build_c1_weights(Q=Q, kappa=kappa, lam=lam_mult * Q if kappa else 0)
            Tk = compose(ref, c1k, q_lattice=("ref.*",))
            Ek = Engine(Tk, Q)
            s = vacuum_state(Tk, Q, L, ref, c1k)
            a, b = s.a.astype(object), s.b.astype(object)
            b[Tk.gear_index("ref.R00"), lat.index(1, 1, 1)] = 1
            s = State(L, a, b, s.r)
            rr = [Tk.gear_index(f"ref.R{g:02d}") for g in range(48)]
            lr = [i for i, n in enumerate(Tk.names) if n.startswith("c1.")]
            sf, rows, hit = run_track(Ek, s, 2000, rr, lr)
            out[f"lam={lam_mult}Q:single_quantum:kappa={'Q' if kappa else 0}"] = {
                "bits_ref_link": rows, "blow_up_at": hit, "final_ref_bits": bits(sf.b[rr]),
                "final_link_bits": bits(sf.b[lr]) if lr else 0}
    return out


def strong_runs():
    """G9b / C1b (shipped kappa = Q forms) and G9c (fine c2, EXPLORATORY, DECLARED off-lattice, not shipped)."""
    import random
    from fractions import Fraction
    from ...observe.gauge import C2View
    Q, L = 4095, 4
    lat = lattice(L)
    ref = build_reference(Q=Q)
    out = {}
    cases = [("G9b c2 ZQ8 kappa=Q lam=Q", lambda: build_c2(Q=Q, kappa=Q, lam=Q), True),
             ("C1b c1 kappa=Q lam=Q", lambda: build_c1_weights(Q=Q, kappa=Q, lam=Q), True),
             ("frozen (kappa=lam=0)", lambda: build_c2(Q=Q, kappa=0, lam=0), True)]
    for alg in ("H", "ZQ8"):
        for lam in (1, 2):
            cases.append((f"G9c EXPLORATORY DECLARED off-lattice c2 {alg} kappa=65 lam={lam}",
                          (lambda alg=alg, lam=lam: build_c2(Q=Q, kappa=65, lam=lam, algebra=alg,
                                                             declare_off_lattice=True)), False))
    for label, mk, on_lattice in cases:
        blk = mk()
        T = compose(ref, blk, q_lattice=("ref.*",) if on_lattice else ())
        E = Engine(T, Q)
        rng = random.Random(8)
        s = vacuum_state(T, Q, L, ref, blk)
        a, b, r = s.a.astype(object), s.b.astype(object), s.r.astype(object)
        for g in range(48):
            i = T.gear_index(f"ref.R{g:02d}")
            for n in range(lat.N):
                if rng.random() < 0.1:
                    a[i, n] = rng.randint(-3, 3)
                    b[i, n] = rng.randint(-3, 3)
                    r[i, n] = Q * rng.randrange(6)
        s = State(L, a, b, r)
        rr = [T.gear_index(f"ref.R{g:02d}") for g in range(48)]
        lr = [i for i, nm in enumerate(T.names) if not nm.startswith("ref.")]
        sf, rows, hit = run_track(E, s, 500, rr, lr)
        out[label] = {"q_lattice_violations": len(T.q_lattice_violations(("ref.*",))), "blow_up_at": hit,
                      "bits_ref_link": rows[:40]}
    return out


if __name__ == "__main__":
    t0 = time.time()
    res = {"c2": c2_stability(), "stamp_utc": stamp()}
    res["seconds"] = round(time.time() - t0, 1)
    (HERE / "G9_c2_stability.json").write_text(json.dumps(res, indent=1, default=str))
    print("G9 done", res["seconds"])
    t0 = time.time()
    res = {"c1": c1_stability(), "stamp_utc": stamp()}
    res["seconds"] = round(time.time() - t0, 1)
    (HERE / "C1_stability.json").write_text(json.dumps(res, indent=1, default=str))
    print("C1 done", res["seconds"])
    t0 = time.time()
    res = {"strong": strong_runs(), "stamp_utc": stamp(),
           "note": "G9c rows are EXPLORATORY and DECLARED off the Q-lattice (kappa = 65 is not = 0 mod Q): not shipped"}
    res["seconds"] = round(time.time() - t0, 1)
    (HERE / "G9b_C1b_G9c_strong.json").write_text(json.dumps(res, indent=1, default=str))
    print("strong done", res["seconds"], {k: v["blow_up_at"] for k, v in res["strong"].items()})
