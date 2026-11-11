"""L0-EP (pre-registered in NOTES_gravity.md): the universal lapse ON L0 under the ONE-VACUUM embedding; L0 clock rate
from L0 CLICKS vs the lapse; universality L0 vs a first-order matter clock; second-order atom reported.

Usage: OMP_NUM_THREADS=1 nice -n 10 python universe24/demos/gravity/l0_ep.py
Writes runs/demos/gravity/L0_EP.json.
"""
from __future__ import annotations

import json
import math
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

import numpy as np

from universe24.core import Block, Engine, GearType, State, check_reciprocity, compose
from universe24.core.engine import OBJ
from universe24.layers import build_reference
from universe24.layers import gravity as gr
from universe24.layers import gravity_l0 as gl0
from universe24.observe import gravity as og
from universe24.prepare import vacuum_state

OUT = Path("runs/demos/gravity")
READ_WHY = "L0-EP clock TEST read of the static prescribed lapse gear (one-way)"


def stamp():
    return subprocess.run(["date", "-u"], capture_output=True, text=True).stdout.strip()


def oneway(Q, P, spec, field):
    spec = gr._resolve_carriers(spec, Q)
    pot = gr.lapse_potential(field, P, [spec], "GR")
    return Block((), tuple(gr.gradient_terms(pot, only=[spec.q(g) for g in spec.gears], designation=READ_WHY,
                                             what="l0ep read")), name=f"read_{spec.name}", Q=Q)


def l0_block(Q, mode):
    if mode == "W":
        return gl0.build_l0_weight(Q=Q)
    ref = build_reference(Q=Q)
    return Block(ref.gears, ref.terms, name="ref", vacuum={g.name: 3 * Q - 1 for g in ref.gears},
                 params={**ref.params, "l0_offset": Q - 1, "reversor": {g.name: "Mp" for g in ref.gears}}, Q=Q)


def system(Q, P, mode):
    w1 = gr.weyl_spec("w1", s=0, m=4 * P * 8)
    at = gr.atom_spec("at", 2 * P * 4)
    bg = Block((GearType("F", "audit"),), tuple(gr.gradient_terms(gr.wave_potential("F", 0, 6 * Q))), name="bg",
               vacuum={"F": 3 * Q - 1}, Q=Q)
    blocks = [l0_block(Q, mode), bg, gr.build_test_matter(w1, Q=Q), gr.build_test_matter(at, Q=Q),
              gl0.build_l0_lapse(Q=Q, P=P, field="bg.F", oneway=True), oneway(Q, P, w1, "bg.F"),
              oneway(Q, P, at, "bg.F")]
    return blocks


def l0_mode_vector(Q, mu=4.0):
    """Uniform (k = 0) L0 eigenvector of S = Sum_d W_d with eigenvalue mu (float; rounded when placed)."""
    S = np.zeros((48, 48))
    for t, s, ax, c in gl0.l0_hops(Q):
        w = c // Q
        i, j = int(t[1:]), int(s[1:])
        S[i, j] += w
        S[j, i] += w
    vals, vecs = np.linalg.eigh(S)
    idx = int(np.argmin(np.abs(vals - mu)))
    return vals[idx], vecs[:, idx], vals


def run(Q, P, mode, U0, T=600, L=4, A=2 ** 20):
    blocks = system(Q, P, mode)
    Tn = compose(*blocks)
    eng = Engine(Tn, Q)
    s = vacuum_state(Tn, Q, L, *blocks)
    a, b, r = s.a.astype(OBJ), s.b.astype(OBJ), s.r.astype(OBJ)
    F0 = int(round(2 * P * U0))
    gF = Tn.gear_index("bg.F")
    a[gF] = np.full(L ** 3, F0, dtype=object)
    b[gF] = np.full(L ** 3, F0, dtype=object)
    mu, v, _ = l0_mode_vector(Q)
    v = v / np.max(np.abs(v))
    wfac = (Q - 1) / Q if mode == "W" else 1.0
    c0 = mu / 6 * wfac
    for h in range(48):
        g = Tn.gear_index(f"ref.R{h:02d}")
        b[g] = np.full(L ** 3, int(round(A * v[h])), dtype=object)
        a[g] = np.full(L ** 3, int(round(A * v[h] * c0)), dtype=object)
    m = 4 * P * 8
    cw = m / (6 * Q)
    gx = Tn.gear_index("w1.X")
    b[gx] = np.full(L ** 3, A, dtype=object)
    a[gx] = np.full(L ** 3, int(round(A * cw)), dtype=object)
    ga = Tn.gear_index("at.c")
    ca = 1 - 2 * P * 4 / (6 * Q)
    b[ga] = np.full(L ** 3, A, dtype=object)
    a[ga] = np.full(L ** 3, int(round(A * ca)), dtype=object)
    s = State(L, a, b, r)
    hbig = int(np.argmax(np.abs(v)))
    gl = Tn.gear_index(f"ref.R{hbig:02d}")
    ser = {"L0": ([], []), "weyl": ([], []), "atom": ([], [])}
    s_init = s
    for t in range(T):
        s1 = eng.step(s)
        for key, g in (("L0", gl), ("weyl", gx), ("atom", ga)):
            q = int(s1.b[g, 0]) + int(s.a[g, 0])
            changed = (s1.a[g, 0] != s.a[g, 0]) or (s1.b[g, 0] != s.b[g, 0]) or (s1.r[g, 0] != s.r[g, 0])
            if q != 0 and changed:
                ser[key][0].append(t)
                ser[key][1].append(q)
        s = s1
    w = {k: og.rate_from_crossings(og.crossing_times(*ser[k])) for k in ser}
    back = eng.rewind(s, 40) if T >= 40 else None
    return w, {"mu": mu, "F0": F0, "U0": F0 / (2 * P), "L0_channel": hbig, "stats": dict(eng.stats)}


def main():
    started = stamp()
    t0 = time.time()
    P, k = 2 ** 10, 4
    Q = gr.gravity_Q(P, k)
    out = {"started": started, "Q": Q, "P": P, "k": k}
    # reciprocity of the RECIPROCAL L0 lapse (mode R) and integrality refusal of build_lapse on weight-Q L0
    ref = build_reference(Q=Q)
    bgF = Block((GearType("F", "audit"),), tuple(gr.gradient_terms(gr.headroom_potential("F", Q))), name="bg",
                vacuum={"F": 3 * Q - 1}, Q=Q)
    rep = check_reciprocity(compose(ref, bgF, gl0.build_l0_lapse(Q=Q, P=P, field="bg.F")))
    out["reciprocal_L0_lapse"] = {"ok": rep.ok, "checked": rep.checked, "designated": len(rep.designated)}
    try:
        spec = gr.spec_from_block(ref, Q=Q, order=1, carrier={g.name: 0 for g in ref.gears})
        gr.build_lapse(Q=Q, P=P, field="bg.F", matters=[spec])
        out["build_lapse_on_weightQ_L0"] = "accepted (unexpected)"
    except ValueError as exc:
        out["build_lapse_on_weightQ_L0"] = f"refused: {str(exc)[:120]}"
    for mode in ("R", "W"):
        U0 = 0.05
        w1, meta1 = run(Q, P, mode, U0)
        w0, meta0 = run(Q, P, mode, 0.0)
        U = meta1["U0"]
        NL0 = math.cos(w1["L0"]) / math.cos(w0["L0"])
        Nw = math.cos(w1["weyl"]) / math.cos(w0["weyl"])
        Na = math.sin(w1["atom"] / 2) / math.sin(w0["atom"] / 2)
        predL0 = 1 - U * (Q - 1) / Q if mode == "R" else 1 - U
        out[f"mode_{mode}"] = {"U0": U, "w": w1, "w_at_U0=0": w0, "N_click_L0": NL0, "N_pred_L0": predL0,
                               "dev_L0": NL0 / predL0 - 1, "N_click_weyl": Nw, "dev_weyl_vs_1-U": Nw / (1 - U) - 1,
                               "universality_L0/weyl-1": NL0 / Nw - 1, "N_click_atom(half-angle)": Na,
                               "atom_vs_sqrt(1-2U)-1": Na / math.sqrt(1 - 2 * U) - 1,
                               "atom_vs_L0 (U^2/2 expected)": Na / NL0 - 1, "meta": meta1}
    # deviation form / vacuum and rewind (mode R full system, short)
    blocks = system(Q, P, "R")
    Tn = compose(*blocks)
    eng = Engine(Tn, Q)
    v = vacuum_state(Tn, Q, 4, *blocks)
    out["vacuum_fixed_10"] = eng.run(v, 10).same_as(v)
    rng = np.random.default_rng(3)
    a = rng.integers(-50, 51, (Tn.G, 64))
    b = rng.integers(-50, 51, (Tn.G, 64))
    s0 = State(4, a, b, rng.integers(0, 6 * Q, (Tn.G, 64)))
    out["rewind_20_exact"] = eng.rewind(eng.run(s0, 20), 20).same_as(s0)
    out["elapsed_s"] = time.time() - t0
    out["written_utc"] = stamp()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "L0_EP.json").write_text(json.dumps(out, indent=1, default=str) + "\n")
    print(json.dumps(out, indent=1, default=str))


if __name__ == "__main__":
    main()
