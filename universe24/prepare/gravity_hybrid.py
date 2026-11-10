"""DATA for the HYBRID gravity source (layers/gravity_hybrid.py; Study 10 port, ST-2). NEW FILE; data only (AGENTS item 9):
the exact R-a datum of the hybrid source. No step is run here."""
from __future__ import annotations

import numpy as np

from ..core.engine import OBJ, Engine, State
from ..core.tensor import Tensor


def hybrid_source_total(state: State, tensor: Tensor, Q: int, field: str = "metric.h00", bgk: str = "bgk.B") -> int:
    """Sum_x of the hybrid source on this snapshot: u_F evaluated with F = 0 and the background B = 0 (the hybrid block
    is then the only input of F). Read-only."""
    a, b, r = state.a.astype(OBJ).copy(), state.b.astype(OBJ).copy(), state.r
    for nm in (field, bgk):
        g = tensor.gear_index(nm)
        a[g] = 0
        b[g] = 0
    u = np.asarray(Engine(tensor, Q).inputs(State(state.L, a, b, r)), dtype=OBJ)
    return int(np.sum(u[tensor.gear_index(field)]))


def with_hybrid_datum(state: State, tensor: Tensor, Q: int, field: str = "metric.h00", bgk: str = "bgk.B") -> State:
    """Set the R-a background gear so that Sum_x B = Sum_x (hybrid source) EXACTLY: B = floor(S/N) everywhere plus 1 on
    the first S - N floor(S/N) nodes (a = b = B: the gear holds its value)."""
    S = hybrid_source_total(state, tensor, Q, field, bgk)
    N = state.N
    q, res = divmod(S, N)
    vals = [q + (1 if n < res else 0) for n in range(N)]
    a, b = state.a.astype(OBJ).copy(), state.b.astype(OBJ).copy()
    g = tensor.gear_index(bgk)
    a[g] = vals
    b[g] = vals
    return State(state.L, a, b, state.r)


__all__ = ["hybrid_source_total", "with_hybrid_datum"]
