"""Passive incoming-message readout; never a trigger for state evolution."""
from __future__ import annotations

from ..core import State, Tensor
from ..core.lattice import DIRECTIONS
from ..layers.communication import LANES, NAMESPACE


def incoming_messages(before: State, tensor: Tensor, *, namespace: str = NAMESPACE) -> list[dict]:
    """Report the old-snapshot payloads read on each directed face edge.

    These are message records, not the arithmetic official-click definition.
    No global time, phase or node age is needed to determine a reception.
    """
    if before.G != tensor.G:
        raise ValueError('state and tensor gear counts differ')
    rows = []
    for lane, direction in zip(LANES, DIRECTIONS):
        g = tensor.gear_index(f'{namespace}.{lane}')
        for node in (before.b[g] != 0).nonzero()[0]:
            source = before.lattice.coords(int(node))
            target = tuple((x + dx) % before.L for x, dx in zip(source, direction))
            rows.append({'lane': lane, 'source': list(source), 'target': list(target),
                         'payload': int(before.b[g, node])})
    return rows
