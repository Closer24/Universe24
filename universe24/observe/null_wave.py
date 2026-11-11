"""Passive geometry of coherent compact pp-wave snapshots, ell=dt-dz."""
import numpy as np

from universe24.algebra.null_covector import NullCoframe
from universe24.layers.null_wave import PLUS_Z


def geometry(state, *, P=256):
    """Read a prepared macro snapshot; reject staggered/off-sector histories.

    Only ell=dt-dz is paired with this +z transport law. Other null covectors
    supported by the algebra helper are not alternative transport solutions.
    """
    if state.G != 2:
        raise ValueError('Extract the two-channel null-wave component first')
    x, y = state.b.astype(object)
    if (not np.array_equal(x, y)
            or not np.array_equal(state.a[0], y[state.lattice.shift_index(PLUS_Z)])
            or not np.array_equal(state.a[1], x)):
        raise ValueError('Expected a coherent prepared macro snapshot')
    return NullCoframe(P).decode(x)
