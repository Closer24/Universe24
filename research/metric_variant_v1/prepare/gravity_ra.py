"""GRAV-FIX T3: the R-a background datum (Study 6 D(d)) computed from the initial snapshot. INITIAL DATA ONLY: the
tensor polynomial is EVALUATED on the snapshot (no update is run). NEW file.

R-a: the uniform k = 0 background -Ebar per node in the lapse source cancels the k = 0 source. For a b-only quadratic
source of pi/2-carrier matter (the Dirac pair, L0) the time mean of b^2 is (b^2 + a^2)/2 at first order, so the mean
source is S = (S(b) + S(a))/2, S(.) = Sum_x [u_F - stencil(F) + b_B] evaluated on the snapshot and on its a <-> b swap.
Integer data: Ebar = floor(S/N), residue +1 on the first (S mod N) nodes (the residue's k != 0 part is O(1) per node)."""
from __future__ import annotations

import numpy as np

from ..core.engine import OBJ, Engine, State


def lapse_source_sum(engine: Engine, state: State, field: str, bg: str | None) -> int:
    T, Q = engine.tensor, engine.Q
    L = state.L
    g = T.gear_index(field)
    u = engine.inputs(state)[g].astype(OBJ).reshape(L, L, L)
    F = state.b[g].astype(OBJ).reshape(L, L, L)
    s6 = sum(np.roll(F, s, ax) for ax in range(3) for s in (1, -1))
    src = u - ((Q - 1) * s6 + 6 * F)
    total = int(sum(int(v) for v in src.ravel()))
    if bg is not None:
        total += int(sum(int(v) for v in state.b[T.gear_index(bg)]))
    return total


def ra_two_time(engine: Engine, state: State, field: str = "metric.h00", bg: str = "bgk.B") -> tuple[State, dict]:
    """Copy of ``state`` with the background gear set to the two-time mean source (a = b = Ebar (+1 residue))."""
    T = engine.tensor
    swapped = State(state.L, state.b, state.a, state.r)
    Sb = lapse_source_sum(engine, state, field, bg)
    Sa = lapse_source_sum(engine, swapped, field, bg)
    S = (Sb + Sa) // 2
    N = state.N
    Ebar, res = divmod(S, N)
    vals = np.array([Ebar + (1 if n < res else 0) for n in range(N)], dtype=OBJ)
    a, b, r = state.a.astype(OBJ).copy(), state.b.astype(OBJ).copy(), state.r.astype(OBJ).copy()
    gb = T.gear_index(bg)
    a[gb], b[gb] = vals.copy(), vals.copy()
    return State(state.L, a, b, r), {"S_b": Sb, "S_a": Sa, "S_mean": S, "Ebar": Ebar, "residue": res}


def _linear_and_source(tensor, field: str):
    """Gears that source ``field`` quadratically (degree-2 b-only monomials), their free linear operator (degree-1
    monomials among them) and the source quadratic form, as monomial lists."""
    names = tensor.names
    gF = tensor.gear_index(field)
    src = [m for m in tensor.monomials if m.target == gF and m.degree == 2 and all(f.field == "b" for f in m.factors)
           and all(f.gear != gF for f in m.factors)]
    gs = sorted({f.gear for m in src for f in m.factors})
    gset = set(gs)
    lin = [m for m in tensor.monomials if m.target in gset and m.degree == 1 and m.factors[0].field == "b"
           and m.factors[0].gear in gset]
    return gs, lin, src


def ra_free_mean(engine: Engine, state: State, field: str = "metric.h00", bg: str = "bgk.B",
                 t_avg: int = 4000) -> tuple[State, dict]:
    """R-a datum = the TIME MEAN of the lapse source over the FREE linear evolution of the sourcing gears, computed
    exactly in Fourier space from the initial (b, a) (per k: eigenmodes of the 2cos w = eigenvalue recursion; float
    arithmetic used only to compute this ONE initial number). Returns the state with the background gear set
    (a = b = Ebar, residue +1 on the first nodes) and the diagnostics."""
    T, Q, L = engine.tensor, engine.Q, state.L
    N = state.N
    gs, lin, src = _linear_and_source(T, field)
    idx = {g: i for i, g in enumerate(gs)}
    n = len(gs)
    kk = 2 * np.pi * np.fft.fftfreq(L)
    KX, KY, KZ = np.meshgrid(kk, kk, kk, indexing="ij")
    kvec = np.stack([KX.ravel(), KY.ravel(), KZ.ravel()], axis=1)            # (N, 3), same flat order as FFT
    M = np.zeros((N, n, n), dtype=complex)
    for m in lin:
        f = m.factors[0]
        M[:, idx[m.target], idx[f.gear]] += m.coeff * np.exp(1j * kvec @ np.array(f.offset, dtype=float))
    A = M / (3 * Q)
    S = np.zeros((N, n, n), dtype=complex)
    for m in src:
        f1, f2 = m.factors
        ph = np.exp(1j * kvec @ (np.array(f2.offset, dtype=float) - np.array(f1.offset, dtype=float)))
        S[:, idx[f1.gear], idx[f2.gear]] += m.coeff * ph
    bh = np.stack([np.fft.fftn(state.b[g].astype(float).reshape(L, L, L)).ravel() for g in gs], axis=1)
    ah = np.stack([np.fft.fftn(state.a[g].astype(float).reshape(L, L, L)).ravel() for g in gs], axis=1)
    total = 0.0
    inst = 0.0
    for q in range(N):
        Aq = (A[q] + A[q].conj().T) / 2
        mu, V = np.linalg.eigh(Aq)
        x0, x1 = V.conj().T @ bh[q], V.conj().T @ ah[q]
        w = np.arccos(np.clip(mu / 2, -1 + 1e-15, 1 - 1e-15))
        e = np.exp(1j * w)
        Pc = (x0 * e - x1) / (e - 1 / e)
        Rc = x0 - Pc
        Sq = V.conj().T @ ((S[q] + S[q].conj().T) / 2) @ V
        # time mean of x(t)^H Sq x(t): pairs with equal frequencies only (degenerate groups kept exactly)
        ww = np.round(w, 12)
        for wv in np.unique(ww):
            sel = np.flatnonzero(ww == wv)
            sub = Sq[np.ix_(sel, sel)]
            total += float(np.real(Pc[sel].conj() @ sub @ Pc[sel] + Rc[sel].conj() @ sub @ Rc[sel]))
        inst += float(np.real(bh[q].conj() @ ((S[q] + S[q].conj().T) / 2) @ bh[q]))
    Smean = int(round(total / N))
    Sinst = int(round(inst / N))
    Ebar, res = divmod(Smean, N)
    vals = np.array([Ebar + (1 if nn < res else 0) for nn in range(N)], dtype=OBJ)
    a, b, r = state.a.astype(OBJ).copy(), state.b.astype(OBJ).copy(), state.r.astype(OBJ).copy()
    gb = T.gear_index(bg)
    a[gb], b[gb] = vals.copy(), vals.copy()
    return State(L, a, b, r), {"S_free_mean": Smean, "S_instant_check": Sinst, "Ebar": Ebar, "residue": res,
                               "n_source_gears": n, "n_lin": len(lin), "n_src": len(src)}
