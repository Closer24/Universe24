"""prepare/: INITIAL DATA ONLY (AGENTS item 9). Functions here build states before a run; nothing here runs the
engine or touches a running state."""
from __future__ import annotations

import numpy as np

from ..core.engine import OBJ, State
from ..core.lattice import lattice
from ..core.tensor import Block, Tensor, vacuum_map


def vacuum_state(tensor: Tensor, Q: int, L: int, *blocks: Block, default: int | None = None) -> State:
    """Every gear at (0, 0, r0) with r0 from the blocks' vacuum data (qualified names); ``default`` for the rest."""
    if tensor.Q is not None and tensor.Q != Q:
        raise ValueError(f"ONE divisor: the tensor was built with Q = {tensor.Q}, vacuum_state was given Q = {Q}")
    for blk in blocks:
        if blk.Q is not None and blk.Q != Q:
            raise ValueError(f"ONE divisor: block {blk.name!r} was built with Q = {blk.Q}, not {Q}")
    r0 = vacuum_map(*blocks)
    D = 6 * Q
    vals = []
    for name in tensor.names:
        v = r0.get(name, default)
        if v is None:
            raise ValueError(f"no vacuum remainder for gear {name!r}")
        if type(v) is not int or not 0 <= v < D:
            raise ValueError(f"vacuum remainder of {name!r} must be in 0..D-1")
        vals.append(v)
    N = lattice(L).N
    z = np.zeros((tensor.G, N), dtype=OBJ)
    r = np.repeat(np.array(vals, dtype=OBJ)[:, None], N, axis=1)
    return State(L, z, z.copy(), r)


def with_gears(state: State, tensor: Tensor, values: dict) -> State:
    """Copy of ``state`` with some gears set: ``values[(gear_name, (x, y, z))] = (a, b, r)``. Data only."""
    a, b, r = state.a.astype(OBJ), state.b.astype(OBJ), state.r.astype(OBJ)
    lat = lattice(state.L)
    for (name, xyz), (va, vb, vr) in values.items():
        g, n = tensor.gear_index(name), lat.index(*xyz)
        a[g, n], b[g, n], r[g, n] = va, vb, vr
    return State(state.L, a, b, r)
