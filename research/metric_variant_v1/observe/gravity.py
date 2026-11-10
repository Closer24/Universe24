"""Read-only observables and exact-identity checks for the gravity layer (AGENTS item 10: nothing here changes a
state that is fed back into a run). Also the OD2 STAGGERED REVERSOR candidate, an AUDIT map (like Engine.mirror):
it builds a new state for a separate audit run, never a stage of a forward evolution.

All identities are exact integer statements; they read complete snapshots (a, b, r) and the engine's inputs.
Rule3 identity used: 6Q (b(t+1) + b(t-1)) = 2u(t) + r(t) - r(t+1), b(t-1) = a(t).
Box operator: Box_t X := 6Q (X(t+1) - 2X(t) + X(t-1)) - 2(Q-1) Lap X(t); a headroom gear obeys
Box_t h = 2 s(t) + r(t) - r(t+1), s = its input minus its stencil.
"""
from __future__ import annotations

import math

import numpy as np

from ..core.engine import OBJ, State
from ..core.tensor import Tensor

AXES = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
SPATIAL = ("x", "y", "z")


def arr(state: State, tensor: Tensor, name: str, fld: str = "b") -> np.ndarray:
    """(L, L, L) object array (exact Python ints) of one gear type's field a, b or r."""
    g = tensor.gear_index(name)
    L = state.L
    return getattr(state, fld)[g].astype(OBJ).reshape(L, L, L)


def sh(X: np.ndarray, off) -> np.ndarray:
    """sh(X, o)[x] = X[x + o] (periodic)."""
    out = X
    for ax, o in enumerate(off):
        if o:
            out = np.roll(out, -o, axis=ax)
    return out


def lap(X):
    return sum(sh(X, e) + sh(X, tuple(-v for v in e)) for e in AXES) - 6 * X


def sum6(X):
    return sum(sh(X, e) + sh(X, tuple(-v for v in e)) for e in AXES)


def box(Q, Xm, X0, Xp):
    return 6 * Q * (Xp - 2 * X0 + Xm) - 2 * (Q - 1) * lap(X0)


def sources(engine, state: State, names) -> dict:
    """s_g(x) = u_g(x) - [(Q-1) Sum_6 b_g + 6 b_g] for headroom gears g (exact, read-only)."""
    Q = engine.Q
    u = engine.inputs(state)
    L = state.L
    out = {}
    for n in names:
        g = engine.tensor.gear_index(n)
        b = arr(state, engine.tensor, n)
        out[n] = u[g].astype(OBJ).reshape(L, L, L) - ((Q - 1) * sum6(b) + 6 * b)
    return out


# ------------------------------------------------------------------ Lorenz / harmonic identity (10-gear metric)
def comp(ns, i, j):
    """Name of hbar^{ij} (i, j in 0..3, 0 = time) in namespace ns."""
    if i == 0 and j == 0:
        return f"{ns}.h00"
    if i == 0 or j == 0:
        return f"{ns}.h0{SPATIAL[max(i, j) - 1]}"
    a, b = sorted((i - 1, j - 1))
    return f"{ns}.h{SPATIAL[a]}{SPATIAL[b]}"


def div_spatial(F, nu):
    """Sum_i grad_i X^{i nu} at the Yee position of C^nu, for a dict F[(i, nu)] -> (L,L,L) arrays:
    nu = 0 (node): X^{i0} = h0i on links -> backward difference; nu = j: X^{jj} nodes -> forward, X^{ij} (i != j)
    plaquettes stored at x -> backward in i."""
    out = 0
    for i in range(1, 4):
        e = AXES[i - 1]
        X = F[(i, nu)]
        if nu == 0 or i != nu:
            out = out + X - sh(X, tuple(-v for v in e))
        else:
            out = out + sh(X, e) - X
    return out


def lorenz_C(tensor, ns, s_t: State, s_t1: State) -> list:
    """C^nu(t) = h^{0 nu}(t+1) - h^{0 nu}(t) + Div_nu hbar(t), nu = 0..3 (exact integers)."""
    out = []
    for nu in range(4):
        F = {(i, nu): arr(s_t, tensor, comp(ns, i, nu)) for i in range(1, 4)}
        out.append(arr(s_t1, tensor, comp(ns, 0, nu)) - arr(s_t, tensor, comp(ns, 0, nu)) + div_spatial(F, nu))
    return out


def lorenz_identity_residual(engine, ns, states) -> int:
    """Max |residual| of Box_t C^nu = 2 D_mu s^{mu nu}(t) + D_mu (r(t) - r(t+1)) over nu and nodes, for the window
    states = [s(t-1), s(t), s(t+1), s(t+2)] (D_0 X^{0 nu} := X^{0nu}(t+1) - X^{0nu}(t)). 0 means exact."""
    T = engine.tensor
    Q = engine.Q
    sm, s0, s1, s2 = states
    C = [lorenz_C(T, ns, a, b) for a, b in ((sm, s0), (s0, s1), (s1, s2))]
    names = [comp(ns, i, j) for i in range(4) for j in range(i, 4)]
    src0, src1 = sources(engine, s0, names), sources(engine, s1, names)

    def dr(a, b, n):
        return arr(a, T, n, "r") - arr(b, T, n, "r")
    worst = 0
    for nu in range(4):
        lhs = box(Q, C[0][nu], C[1][nu], C[2][nu])
        n0 = comp(ns, 0, nu)
        rhs = 2 * (src1[n0] - src0[n0]) + (dr(s1, s2, n0) - dr(s0, s1, n0))
        S = {(i, nu): 2 * src0[comp(ns, i, nu)] + dr(s0, s1, comp(ns, i, nu)) for i in range(1, 4)}
        rhs = rhs + div_spatial(S, nu)
        worst = max(worst, int(np.max(np.abs((lhs - rhs).astype(OBJ)))))
    return worst


def source_divergence(engine, ns, s0: State, s1: State) -> int:
    """max |D_mu s^{mu nu}(t)| (exact) for the metric sources at t (s0) and t+1 (s1)."""
    T = engine.tensor
    names = [comp(ns, i, j) for i in range(4) for j in range(i, 4)]
    src0, src1 = sources(engine, s0, names), sources(engine, s1, names)
    worst = 0
    for nu in range(4):
        d = src1[comp(ns, 0, nu)] - src0[comp(ns, 0, nu)] + div_spatial({(i, nu): src0[comp(ns, i, nu)]
                                                                         for i in range(1, 4)}, nu)
        worst = max(worst, int(np.max(np.abs(d))))
    return worst


# ------------------------------------------------------------------ Gauss law (lapse field)
def box_mask(L, centre, h):
    m = np.zeros((L, L, L), dtype=bool)
    c = centre
    idx = [np.arange(c[i] - h, c[i] + h + 1) % L for i in range(3)]
    m[np.ix_(*idx)] = True
    return m


def flux(F, mask):
    """Sum over x in R of Lap F(x) = the outward face flux through dR (exact)."""
    return int(np.sum(lap(F)[mask]))


def gauss_residual(engine, F_name, states, mask) -> int:
    """|6Q Sum_R (F(t+1) - 2F(t) + F(t-1)) - 2(Q-1) Flux_dR F(t) - 2 Sum_R s(t) - Sum_R (r(t) - r(t+1))| for the
    window states = [s(t-1), s(t), s(t+1)]."""
    T, Q = engine.tensor, engine.Q
    sm, s0, s1 = states
    Fm, F0, F1 = (arr(s, T, F_name) for s in (sm, s0, s1))
    src = sources(engine, s0, [F_name])[F_name]
    lhs = 6 * Q * int(np.sum((F1 - 2 * F0 + Fm)[mask])) - 2 * (Q - 1) * flux(F0, mask)
    rhs = 2 * int(np.sum(src[mask])) + int(np.sum((arr(s0, T, F_name, "r") - arr(s1, T, F_name, "r"))[mask]))
    return abs(lhs - rhs)


# ------------------------------------------------------------------ OD2 harmonic constants
def od2_constants(tensor, ns, s_t: State, s_t1: State) -> list:
    """C^0, C^x, C^y, C^z of the OD2 chain at t (exact): C^i = h0i(t+1) - h0i(t) + Div_i(t) (links),
    C^0 = h00(t+1) - h00(t) + Sum_i [h0i(x) - h0i(x - e_i)](t)."""
    def g(s, n, f="b"):
        return arr(s, tensor, f"{ns}.{n}", f)

    def hij(s, i, j):
        a, b = sorted((i, j))
        return g(s, "h" + SPATIAL[a] + SPATIAL[b])
    out = []
    div0 = sum(g(s_t, f"h0{SPATIAL[i]}") - sh(g(s_t, f"h0{SPATIAL[i]}"), tuple(-v for v in AXES[i])) for i in range(3))
    out.append(g(s_t1, "h00") - g(s_t, "h00") + div0)
    for i in range(3):
        d = sh(hij(s_t, i, i), AXES[i]) - hij(s_t, i, i)
        for j in range(3):
            if j != i:
                d = d + hij(s_t, j, i) - sh(hij(s_t, j, i), tuple(-v for v in AXES[j]))
        out.append(g(s_t1, f"h0{SPATIAL[i]}") - g(s_t, f"h0{SPATIAL[i]}") + d)
    return out


# ------------------------------------------------------------------ T^{mu nu} two-time identities (KG test matter)
def tmunu_residuals(Q, W, c0, s_m: State, s0: State, s1: State, s2: State, tensor, name) -> tuple[int, int]:
    """s3 A10-1 for the KG gear u = W Sum_6 b + c0 b (D = 6Q), from four consecutive snapshots (times t-1..t+2 of b):
    energy: D[e(t+1) - e(t)] + Sum_e D J_{x,x+e}(t) = (b(t+1) - b(t-1))(r(t) - r(t+1)),
      D e(t) = D(b(t)^2 + b(t-1)^2) - 2 b(t-1)(W Sum_6 b(t) + c0 b(t)),
      D J_{x,x+e}(t) = 2W [b_x(t) b_{x+e}(t+1) - b_x(t+1) b_{x+e}(t)];
    momentum (every axis e): D[p_e(t+1) - p_e(t)] + Dm_e T^ee + Sum_{j != e} Dm_j T^ej = b_x g_{x+e} - b_{x+e} g_x,
      p_e(x,t) = b_x(t-1) b_{x+e}(t) - b_x(t) b_{x+e}(t-1), D T^ee = -2W (b_x b_{x+2e} - b_{x+e}^2),
      D T^ej = -2W (b_x b_{x+e+j} - b_{x+e} b_{x+j}) (symmetric plaquette stress), g = r(t) - r(t+1).
    Returns (max |energy residual|, max |momentum residual|)."""
    D = 6 * Q
    bm1, b0, bp1 = (arr(s, tensor, name) for s in (s_m, s0, s1))
    bp2 = arr(s2, tensor, name)
    g0 = arr(s0, tensor, name, "r") - arr(s1, tensor, name, "r")

    def De(bt, btm1):
        return D * (bt * bt + btm1 * btm1) - 2 * btm1 * (W * sum6(bt) + c0 * bt)
    DJ = sum(2 * W * (b0 * sh(bp1, s) - bp1 * sh(b0, s)) for e in AXES for s in (e, tuple(-v for v in e)))
    res_e = De(bp1, b0) - De(b0, bm1) + DJ - (bp1 - bm1) * g0
    worst_p = 0
    for ax, e in enumerate(AXES):
        def p(bt, btm1):
            return btm1 * sh(bt, e) - bt * sh(btm1, e)
        e2 = tuple(2 * v for v in e)
        Tee = -2 * W * (b0 * sh(b0, e2) - sh(b0, e) ** 2)
        lhs = D * (p(bp1, b0) - p(b0, bm1)) + Tee - sh(Tee, tuple(-v for v in e))
        for j in range(3):
            if j != ax:
                ej = AXES[j]
                Tej = -2 * W * (b0 * sh(sh(b0, e), ej) - sh(b0, e) * sh(b0, ej))
                lhs = lhs + Tej - sh(Tej, tuple(-v for v in ej))
        rhs = b0 * sh(g0, e) - sh(b0, e) * g0
        worst_p = max(worst_p, int(np.max(np.abs(lhs - rhs))))
    return int(np.max(np.abs(res_e))), worst_p


# ------------------------------------------------------------------ clocks from clicks
def crossing_times(series_t, series_q) -> list[float]:
    """Sign-change times of a click-size sequence (t, quotient), linear interpolation between consecutive click
    rows (click space: sizes and update counts only)."""
    out = []
    for (t0, q0), (t1, q1) in zip(zip(series_t, series_q), zip(series_t[1:], series_q[1:])):
        if q0 == 0 or q1 == 0:
            continue
        if (q0 > 0) != (q1 > 0):
            out.append(t0 + (t1 - t0) * q0 / (q0 - q1))
    return out


def rate_from_crossings(times: list[float]) -> float:
    """Angular frequency from equally spaced half-period crossings (least-squares slope; pi per crossing)."""
    n = len(times)
    if n < 3:
        return float("nan")
    xs = list(range(n))
    mx, my = sum(xs) / n, sum(times) / n
    slope = sum((x - mx) * (y - my) for x, y in zip(xs, times)) / sum((x - mx) ** 2 for x in xs)
    return math.pi / slope


def click_series(logs, gear_index: int, node: int):
    """(t, quotient) rows of one gear instance from a list of ClickLog (official stream)."""
    ts, qs = [], []
    for lg in logs:
        sel = np.flatnonzero((lg.gear == gear_index) & (lg.node == node))
        if sel.size:
            ts.append(lg.step)
            qs.append(int(lg.quotient[sel[0]]))
    return ts, qs


# ------------------------------------------------------------------ OD2 staggered reversor (AUDIT map)
def od2_staggered_reversor(tensor, Q, ns, matter_map: dict, field_gears=None):
    """Candidate STAGGERED time reversor X for the OD2 chain (S4-M M_grav_mirror structure, P-vii(c')):
    hij: M (b, a, D-1-r); h0i: (a, b) -> (-h0i(t+1), -b), r kept; h00: (a, b) -> (h00(t+2), h00(t+1)), r kept;
    matter gears: per-gear maps given in ``matter_map`` {qualified name: map name} (e.g. "M") or a callable on the
    state. h0i(t+1), h00(t+1), h00(t+2) are the accumulator look-aheads (exact, from the snapshot). Audit only."""
    from ..core.reversors import GearwiseMap
    D = 6 * Q
    hij = [f"{ns}.h{SPATIAL[a]}{SPATIAL[b]}" for a in range(3) for b in range(a, 3)]

    def X(state: State) -> State:
        L = state.L
        a = state.a.astype(OBJ).copy()
        b = state.b.astype(OBJ).copy()
        r = state.r.astype(OBJ).copy()

        def g(n, f="b"):
            return arr(state, tensor, f"{ns}.{n}", f)

        def hijv(i, j, f):
            x, y = sorted((i, j))
            return g("h" + SPATIAL[x] + SPATIAL[y], f)

        def div_i(i, f):
            d = sh(hijv(i, i, f), AXES[i]) - hijv(i, i, f)
            for j in range(3):
                if j != i:
                    d = d + hijv(j, i, f) - sh(hijv(j, i, f), tuple(-v for v in AXES[j]))
            return d
        h0n = {}
        for i in range(3):
            n = f"h0{SPATIAL[i]}"
            h0n[i] = 2 * g(n) - g(n, "a") - (div_i(i, "b") - div_i(i, "a"))
        div0_b = sum(g(f"h0{SPATIAL[i]}") - sh(g(f"h0{SPATIAL[i]}"), tuple(-v for v in AXES[i])) for i in range(3))
        div0_a = sum(g(f"h0{SPATIAL[i]}", "a") - sh(g(f"h0{SPATIAL[i]}", "a"), tuple(-v for v in AXES[i]))
                     for i in range(3))
        div0_n = sum(h0n[i] - sh(h0n[i], tuple(-v for v in AXES[i])) for i in range(3))
        h00n = 2 * g("h00") - g("h00", "a") - (div0_b - div0_a)
        h00nn = 2 * h00n - g("h00") - (div0_n - div0_b)
        for n in hij:
            k = tensor.gear_index(n)
            a[k], b[k], r[k] = state.b[k].astype(OBJ), state.a[k].astype(OBJ), (D - 1) - state.r[k].astype(OBJ)
        for i in range(3):
            k = tensor.gear_index(f"{ns}.h0{SPATIAL[i]}")
            a[k], b[k] = (-h0n[i]).reshape(-1), (-state.b[k].astype(OBJ))
        k = tensor.gear_index(f"{ns}.h00")
        a[k], b[k] = h00nn.reshape(-1), h00n.reshape(-1)
        out = State(L, a, b, r)
        if callable(matter_map):
            return matter_map(out)
        if matter_map:
            mm = GearwiseMap(tensor, Q, matter_map)
            # apply matter maps only to matter gears (others identity by default)
            out = mm(out)
        return out
    return X


def support_report(tensor) -> dict:
    """Tensor.support_violations() grouped by (target, factor gears) names: design facts (not failures)."""
    out = {}
    for m in tensor.support_violations():
        key = (tensor.names[m.target], tuple(sorted({tensor.names[f.gear] for f in m.factors})))
        out[key] = out.get(key, 0) + 1
    return out
