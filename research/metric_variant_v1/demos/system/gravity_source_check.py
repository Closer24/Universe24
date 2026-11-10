"""R1 gravity-source check (pre-registered in NOTES_system.md, "PRE-REGISTRATION R1 + R2"): the lapse field's source
implied by the reciprocal matter lapse, form C (Wilson difference) vs B1-GRAV's split, on free matter (F = 0).
(i) exact two-time Noether energy E = D(|a|^2 + |b|^2) - 2 a^T H b: E(t+1) - E(t) = (b' - a).(r - r') per update;
(ii) the b-only source total Sum_x S(t), S = dPhi_int/dF: not conserved (relative oscillation reported);
(iii) k = 0 (uniform state): the C source is the mass energy only (no 6 w |psi|^2 term).
Run: OMP_NUM_THREADS=1 nice -n 10 python -m research.metric_variant_v1.demos.system.gravity_source_check
Writes results/system/gravity_source.json."""
from __future__ import annotations

import json
import random
from pathlib import Path

import numpy as np

from ...core.engine import OBJ, Engine, State
from ...core.tensor import Block, GearType, compose
from ...layers import gravity as gr
from ...layers.matter import build_matter, matter_names
from ...layers.matter_lapse_c import build_matter_lapse_c
from ...layers.system import HOP, MASS_DEFAULT, P_GRAV, Q_DEFAULT, WILSON
from ...prepare import vacuum_state

Q, P, D = Q_DEFAULT, P_GRAV, 6 * Q_DEFAULT
L, T = 4, 200
OUT = Path(__file__).resolve().parents[2] / "results" / "system"


def source_total(Tn, s, gF):
    """Sum_x u_F(x) of the lapse terms targeting the field gear F (b-only; evaluated with the engine's inputs)."""
    return int(np.asarray(Engine(Tn, Q).inputs(s), dtype=object)[gF].sum())


def main():
    m = build_matter(Q=Q, hop=HOP, mass=MASS_DEFAULT, wilson=WILSON, species="pair", name="matter")
    # F as a pure audit gear with NO dynamics of its own except the source (u_F = source); F stays 0 because its own
    # input is read here only through Engine.inputs, never stepped (the matter evolves with F = 0 exactly: we step the
    # matter alone)
    bg = Block((GearType("F", "audit"),), (), name="bg", vacuum={"F": 3 * Q - 1}, Q=Q)
    spec = gr.spec_from_block(m, Q=Q, order=1)
    lapC = build_matter_lapse_c(Q=Q, P=P, field="bg.F", matter=m, oneway=False, name="lapC")
    lapS = gr.build_lapse(Q=Q, P=P, field="bg.F", matters=[spec], name="lapS")
    Tm = compose(m)
    Em = Engine(Tm, Q)
    TC, TS = compose(m, bg, lapC), compose(m, bg, lapS)
    rng = random.Random(7)
    s = vacuum_state(Tm, Q, L, m)
    a = np.array([[rng.randint(-1000, 1000) for _ in range(L ** 3)] for _ in range(16)], dtype=object)
    b = np.array([[rng.randint(-1000, 1000) for _ in range(L ** 3)] for _ in range(16)], dtype=object)
    s = State(L, a, b, s.r.astype(OBJ))
    names = matter_names("pair")
    # H: the matter's linear operator, applied through the engine's inputs: u = H b (b-only, linear)
    def Hb(state):
        return np.asarray(Em.inputs(State(L, np.zeros_like(state.a), state.b, state.r)), dtype=object)

    def energy(state):
        u = Hb(state).astype(OBJ)
        a, b = state.a.astype(OBJ), state.b.astype(OBJ)
        return int(D * (np.sum(a * a) + np.sum(b * b)) - 2 * np.sum(a * u))

    def with_F(Tn, state):
        vs = vacuum_state(Tn, Q, L, m, bg)
        A = vs.a.astype(OBJ); B = vs.b.astype(OBJ); R = vs.r.astype(OBJ)
        for i, nm in enumerate(names):
            g = Tn.gear_index(f"matter.{nm}")
            A[g], B[g], R[g] = state.a[i], state.b[i], state.r[i]
        return State(L, A, B, R)

    fails, SC, SS = 0, [], []
    gC, gS = TC.gear_index("bg.F"), TS.gear_index("bg.F")
    for t in range(T):
        s1 = Em.step(s)
        dE = energy(s1) - energy(s)
        rem = int(np.sum((s1.b.astype(OBJ) - s.a.astype(OBJ)) * (s.r.astype(OBJ) - s1.r.astype(OBJ))))
        fails += int(dE != rem)
        SC.append(source_total(TC, with_F(TC, s), gC))
        SS.append(source_total(TS, with_F(TS, s), gS))
        s = s1
    def osc(x):
        x = np.array(x, dtype=float)
        return float((x.max() - x.min()) / max(abs(x.mean()), 1e-300)), float(x.mean())
    # (iii) uniform state: C source vs mass energy only
    u_state = State(L, np.zeros((16, L ** 3), dtype=object),
                    np.array([[rng.randint(-1000, 1000)] * (L ** 3) for _ in range(16)], dtype=object),
                    vacuum_state(Tm, Q, L, m).r.astype(OBJ))
    from ...layers.matter import algebra
    W0 = algebra("pair")["W0"]
    bb = u_state.b[:, 0].astype(object)
    mass_energy = int(sum(int(W0[i, j]) * bb[i] * bb[j] for i in range(16) for j in range(16)))   # b^T W0 b
    sC = source_total(TC, with_F(TC, u_state), gC)
    sS = source_total(TS, with_F(TS, u_state), gS)
    out = {"L": L, "T": T, "noether_energy_identity_failures": fails,
           "source_total_C": {"rel_oscillation": osc(SC)[0], "mean": osc(SC)[1]},
           "source_total_split": {"rel_oscillation": osc(SS)[0], "mean": osc(SS)[1]},
           "uniform_state": {"source_C_per_node": sC / L ** 3, "source_split_per_node": sS / L ** 3,
                             "-(m/(4P)) b^T W0 b": -MASS_DEFAULT * mass_energy / (4 * P),
                             "-((m + 6w)/(4P) - 12 w/(4P)) b^T W0 b": -(MASS_DEFAULT - 6 * WILSON) * mass_energy / (4 * P)}}
    print(json.dumps(out, indent=1))
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "gravity_source.json").write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
