"""Retired large-divisor background calibration. Public calibrated initial-data routines fail explicitly; polynomial inspection remains available for research."""
from __future__ import annotations

import numpy as np

from ..core.engine import OBJ, Engine, State


def lapse_source_sum(engine: Engine, state: State, field: str, bg: str | None) -> int:
    """Retired initial-data formula; no fixed-divisor replacement is established."""
    raise NotImplementedError("This preparation depended on the removed divisor scale; supply explicit integer initial data instead")


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
    """Retired initial-data formula; no fixed-divisor replacement is established."""
    raise NotImplementedError("This preparation depended on the removed divisor scale; supply explicit integer initial data instead")
