"""ONE seed (Study 22, ONE-A): INITIAL DATA ONLY (AGENTS item 9). Nothing here runs the engine or touches a running
state; every function returns a NEW State on the joint vacuum (0, 0, 3Q - 1).

ONE seed = one package bang + the cosmic data, all R*-fixed about ONE centre c2 (observe.seed.r_star_hands_on):
  package bang  "jpure": prepare.chiral.jpure_seed (rng 31, width 6), NORM-MATCHED as in s17E/EMERGE-N_work/emerge_run.py
                (probe at 2^16, A_J = 2^round(16 - log2(ratio)/2)), centre c2 = (0, 0, 0);
                "s2star": prepare.seed.s2_star(x0 = 0, A = 2^16), centre c2 = (0, 1, 0); "none": no package bang.
  hand          Theta = Theta0 at rest at every node, INCLUDING the remainder (r = 3Q - 1, R'-fixed) (s15 E2).
  cosmic matter the CC-A neutral packet, R*-fixed about c2: b(M1, x0) = A_c, a(M1, c2 - x0) = A_c, b(M2, x0 + e_x) = A_c,
                a(M2, c2 - x0 - e_x) = A_c (x0 = 0), r = 3Q - 1.
  Born loads    b_Lp = a_Lp = p_x, b_Lm = a_Lm = S_L - p_x (static), S_L = 3Q/c_pair (layers.one), p_x in [S_L/8, 7S_L/8)
                from rng, p(c2 - x) = p(x); p_x / S_L is the target quotient-weight fraction, not a derived probability of official click records.
  tokens        r_dp = r_dm = tok_x (shared remainder), tok_x uniform in [0, D) from rng, tok(c2 - x) = R'(tok_x); on a
                self-mirror node tok is a fixed point of R' (3Q - 1 or 3Q). a = b = 0 on the pair.
The rng seed changes ONLY loads and tokens (outcomes), never the hand, the matter or the package data.
"""
from __future__ import annotations

import math

import numpy as np

from ..core.engine import OBJ, State
from ..core.lattice import lattice
from ..core.reversors import remainder_map
from ..layers.one import A_COSMIC_DEFAULT, COSMIC_NS, THETA0_DEFAULT
from . import vacuum_state

CENTRES = {"jpure": (0, 0, 0), "s2star": (0, 1, 0), "none": (0, 0, 0)}


def _mirror_index(lat, c2, n: int) -> int:
    x, y, z = lat.coords(n)
    L = lat.L
    return lat.index((c2[0] - x) % L, (c2[1] - y) % L, (c2[2] - z) % L)


def package_bang(system, tensor, L: int, kind: str = "jpure") -> tuple[State, dict]:
    """The package bang on the joint vacuum of ``system`` (all blocks, the cosmic one included). Data only."""
    from ..prepare.chiral import jpure_seed
    from ..prepare.seed import s2_star
    Q = system.Q
    vac = vacuum_state(tensor, Q, L, *system.blocks)
    if kind == "none":
        return vac, {"kind": "none"}
    if kind == "s2star":
        A = 1 << 16
        return s2_star(vac, tensor, (0, 0, 0), A), {"kind": "S2*", "A": A, "x0": (0, 0, 0), "i": 0, "axis": 1}
    if kind != "jpure":
        raise ValueError("kind must be 'jpure', 's2star' or 'none'")
    mi = [b.name for b in system.blocks].index("matter")
    mrows = [tensor.gear_index(f"matter.{n}") for n in [f"X{i}" for i in range(8)] + [f"Y{i}" for i in range(8)]]
    probe, _ = jpure_seed(tensor, system.blocks, Q, L, A=1 << 16, matter_block=mi)
    bm = np.asarray(probe.b[mrows], dtype=float)
    ratio = float((bm ** 2).sum()) / float((1 << 16) ** 2)
    AJ = 1 << int(round(16 - 0.5 * math.log2(ratio)))
    s0, rep = jpure_seed(tensor, system.blocks, Q, L, A=AJ, matter_block=mi)
    return s0, {"kind": "J-pure (prepare.chiral.jpure_seed, rng 31, width 6), norm-matched (emerge_run)",
                "norm_ratio_at_2^16": ratio, "A_J": AJ, "report": rep}


def cosmic_data(state: State, tensor, Q: int, c2, *, load_sum: int, theta0: int = THETA0_DEFAULT,
                A_c: int = A_COSMIC_DEFAULT, rng_seed: int = 13, ns: str = COSMIC_NS) -> tuple[State, dict]:
    """Copy of ``state`` with the cosmic hand, packet, loads and tokens set (module docstring). Data only."""
    D = 6 * Q
    L = state.L
    lat = lattice(L)
    N = lat.N
    a, b, r = state.a.astype(OBJ), state.b.astype(OBJ), state.r.astype(OBJ)
    g = {k: tensor.gear_index(f"{ns}.{k}") for k in ("Th", "M1", "M2", "Lp", "Lm", "dp", "dm")}
    r0 = 3 * Q - 1
    a[g["Th"]] = theta0
    b[g["Th"]] = theta0
    r[g["Th"]] = r0
    for k in ("M1", "M2", "Lp", "Lm"):
        r[g[k]] = r0
    x0 = (0, 0, 0)
    n0 = lat.index(*x0)
    n1 = lat.index(1 % L, 0, 0)
    b[g["M1"], n0] = A_c
    a[g["M1"], _mirror_index(lat, c2, n0)] = A_c
    b[g["M2"], n1] = A_c
    a[g["M2"], _mirror_index(lat, c2, n1)] = A_c
    rng = np.random.default_rng(rng_seed)
    p = [None] * N
    tok = [None] * N
    for n in range(N):
        if p[n] is not None:
            continue
        m = _mirror_index(lat, c2, n)
        pv = int(rng.integers(load_sum // 8, 7 * load_sum // 8))
        if m == n:
            tv = (r0, r0 + 1)[int(rng.integers(0, 2))]          # the two fixed points of R': 3Q - 1 and 3Q
            p[n], tok[n] = pv, tv
        else:
            tv = int(rng.integers(0, D))
            p[n] = p[m] = pv
            tok[n] = tv
            tok[m] = int(remainder_map("Mp", np.array([tv], dtype=OBJ), D)[0])
    a[g["Lp"]] = p
    b[g["Lp"]] = p
    a[g["Lm"]] = [load_sum - v for v in p]
    b[g["Lm"]] = [load_sum - v for v in p]
    r[g["dp"]] = tok
    r[g["dm"]] = tok
    a[g["dp"]] = 0
    b[g["dp"]] = 0
    a[g["dm"]] = 0
    b[g["dm"]] = 0
    rep = {"c2": tuple(c2), "theta0": theta0, "A_c": A_c, "rng_seed": rng_seed, "x0": x0,
           "packet": {"M1": {"b": [x0], "a": [lat.coords(_mirror_index(lat, c2, n0))]},
                      "M2": {"b": [lat.coords(n1)], "a": [lat.coords(_mirror_index(lat, c2, n1))]}},
           "sum_I0": 2 * A_c * A_c, "load_sum": load_sum,
           "loads": "p in [S_L/8, 7 S_L/8), p(c2 - x) = p(x)", "tokens": "tok(c2 - x) = R'(tok(x))"}
    return State(L, a, b, r), rep


def one_seed(system, tensor, L: int, *, bang: str = "jpure", rng_seed: int = 13, A_c: int = A_COSMIC_DEFAULT,
             theta0: int | None = None) -> tuple[State, dict]:
    """THE ONE seed: package bang + cosmic data about the bang's centre c2. Returns (state, report)."""
    cp = system.info["one"]["cosmic_params"]
    if theta0 is None:
        theta0 = cp["theta0"]
    s, rep_b = package_bang(system, tensor, L, bang)
    c2 = CENTRES[bang]
    s, rep_c = cosmic_data(s, tensor, system.Q, c2, load_sum=cp["load_sum"], theta0=theta0, A_c=A_c, rng_seed=rng_seed)
    return s, {"bang": rep_b, "cosmic": rep_c, "c2": c2}


__all__ = ["CENTRES", "package_bang", "cosmic_data", "one_seed"]
