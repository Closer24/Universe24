"""Complete initial histories of the optional homogeneous FLRW sector."""
import numpy as np
from universe24.core import State
from universe24.core.lattice import lattice
from universe24.layers.conformal_flrw import NAMES, resolution, build


def prepare(*, L=3, Q=1, q0=2, dust=(1, 1, 1), radiation=1, remainders=None):
    Q = resolution(Q)
    lattice(L)
    dust = tuple(dust)
    if len(dust) != 3 or any(type(v) is not int or v < 0 for v in dust):
        raise ValueError('dust must contain three nonnegative Python integers')
    if type(radiation) is not int or radiation < 0:
        raise ValueError('radiation must be a nonnegative Python integer')
    if type(q0) is not int or q0 < 2:
        raise ValueError('q0 >= 2 keeps both initial histories beyond the bang')
    A, B = sum(dust), radiation
    if A == B == 0:
        raise ValueError('this big-bang sector requires a nonzero source')

    def history(q):
        return [q, A*q*q+B*Q*q, 2*A*q**3+3*B*Q*q*q,
                6*A*A*q**5+15*A*B*Q*q**4+10*B*B*Q*Q*q**3,
                *dust, B]

    a, b = (np.repeat(np.array(history(q), dtype=object)[:, None], L**3, axis=1)
            for q in (q0-1, q0))
    r = np.arange(len(NAMES)*L**3).reshape(len(NAMES), L**3) % 6 if remainders is None else remainders
    state = State(L, a, b, r)
    if np.any(state.r < 0) or np.any(state.r >= 6):
        raise ValueError('remainders must lie in [0,6)')
    return build(Q), state
