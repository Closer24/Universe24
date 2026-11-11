"""Initial data for the single-edge experiment. Never used inside a run loop."""
import numpy as np

from ..core import State
from ..layers.strict_edge import EdgeRealization


def lift_seed(source_state: State, realization: EdgeRealization) -> State:
    """Keep every source register; initialize each new H from its U's a,b,r.

    This is only a preparation convention. H and U are independent dynamical
    registers, and their equality is not imposed or expected after the seed.
    """
    if source_state.G != realization.source_gears:
        raise ValueError('seed gear count does not match the source tensor')
    rows = list(range(source_state.G)) + [g for g, _ in realization.link_mediators]
    arrays = [np.asarray(getattr(source_state, f))[rows].copy() for f in ('a', 'b', 'r')]
    return State(source_state.L, *arrays)
