"""Complete integer histories for the optional compact null-wave sector."""
import numpy as np

from universe24.algebra.null_covector import integer_array
from universe24.core import State
from universe24.core.lattice import lattice
from universe24.layers.null_wave import PLUS_Z


def prepare(tensor, profile, *, L, remainders=None):
    """Encode a flattened node profile as b=(F,F), a=(S_plus F,F).

    Remainders are independent retained data, frozen by this tensor. They do
    not translate with F and cannot be recovered from the geometric readout.
    """
    lat = lattice(L)
    if tensor.names != ('profile.X', 'profile.Y'):
        raise ValueError('Expected the standalone two-channel null-wave tensor')
    values = integer_array(profile)
    if values.shape != (lat.N,):
        raise ValueError(f'Expected one profile value per node: shape ({lat.N},)')
    b = np.stack((values, values))
    a = np.stack((values[lat.shift_index(PLUS_Z)], values))
    r = np.zeros_like(b) if remainders is None else integer_array(remainders)
    if r.shape != b.shape or np.any(r < 0) or np.any(r >= 6):
        raise ValueError('Remainders must have shape (2,N) and lie in [0,6)')
    return State(L, a, b, r)
