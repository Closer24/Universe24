"""Prepare complete histories for the experimental paired-frame map."""
import numpy as np

from universe24.algebra.frame_equations import FIELDS, sampled
from universe24.algebra.null_covector import integer_array
from universe24.core import State
from universe24.core.lattice import lattice


def flat_values(L):
    values = np.zeros((24, lattice(L).N), dtype=object)
    for i in range(3):
        values[FIELDS.index(f'B{i}{i}')] = 1
    return values


def increment(program, values, lat):
    rhs, _, _ = sampled(integer_array(values), lat, program.dx)
    rows = [np.broadcast_to(2*program.dt*rhs[name], (lat.N,)) for name in FIELDS]
    values = np.array(rows, dtype=object)
    # Fractions with denominator one are exact, not rounded physical values.
    if any(getattr(v, 'denominator', 1) != 1 for v in values.flat):
        raise ValueError('Noninteger increment outside the compiled integer sector')
    return np.array([int(v) for v in values.flat], dtype=object).reshape(values.shape)


def prepare(program, previous, current, *, L, remainders=None):
    """b=(x,y), a=R^-1(b)=(y-F(x),x), with all remainders retained.

    Constraint-compatible individual slices need not be a temporally
    consistent Einstein pair. This function enforces encoding, not physics.
    """
    lat = lattice(L)
    x, y = integer_array(previous), integer_array(current)
    if x.shape != (24, lat.N) or y.shape != x.shape:
        raise ValueError('Expected two arrays of shape (24,L^3)')
    b = np.concatenate((x, y))
    a = np.concatenate((y-increment(program, x, lat), x))
    r = np.zeros_like(b) if remainders is None else integer_array(remainders)
    if r.shape != b.shape or np.any(r < 0) or np.any(r >= 6):
        raise ValueError('Expected remainders of shape (48,L^3) in [0,6)')
    return State(L, a, b, r)
