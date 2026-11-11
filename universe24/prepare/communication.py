"""Complete message initial data only; no injection during a run."""
from __future__ import annotations

from ..core import State, Tensor
from ..core.lattice import DIRECTIONS
from ..layers.communication import LANES, NAMESPACE


def message_seed(state: State, tensor: Tensor, packets, *, namespace: str = NAMESPACE) -> State:
    """Replace lane initial data with (lane, (x,y,z), integer payload) packets.

    Packets at the same address add exactly. a is the preceding translated
    snapshot, not an independent clock. Other gears and all remainders are
    retained. Coordinates must be canonical lattice addresses.
    """
    if state.G != tensor.G:
        raise ValueError('state and tensor gear counts differ')
    indices = [tensor.gear_index(f'{namespace}.{lane}') for lane in LANES]
    a, b, r = (array.astype(object).copy() for array in (state.a, state.b, state.r))
    a[indices] = 0
    b[indices] = 0
    for lane, xyz, payload in packets:
        if lane not in LANES:
            raise ValueError(f'unknown communication lane {lane!r}')
        xyz = tuple(xyz)
        if len(xyz) != 3 or any(type(v) is not int or not 0 <= v < state.L for v in xyz):
            raise ValueError('packet coordinates must be three integers inside the lattice')
        if type(payload) is not int:
            raise TypeError('message payload must be an exact Python int')
        g = indices[LANES.index(lane)]
        b[g, state.lattice.index(*xyz)] += payload
    for g, direction in zip(indices, DIRECTIONS):
        a[g] = b[g, state.lattice.shift_index(direction)]
    return State(state.L, a, b, r)
