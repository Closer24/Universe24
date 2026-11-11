"""Passive source-coordinate view of the node/link experiment.

This map is deliberately many-to-one: it omits the extra physical U registers
and uses H for each former source link coordinate. It is NOT a full state,
inverse, assertion of dynamical equivalence, or extra runtime operation.
"""
from ..core import State
from ..layers.strict_edge import EdgeRealization


def source_coordinate_view(state: State, realization: EdgeRealization) -> State:
    if state.G != realization.tensor.G:
        raise ValueError('state does not match the extended tensor')
    remap = dict(realization.link_mediators)
    rows = [remap.get(i, i) for i in range(realization.source_gears)]
    return State(state.L, *(getattr(state,field)[rows].copy() for field in ('a','b','r')))
