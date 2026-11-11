"""Complete paired initial data; no constraint solving or hidden repair."""
import numpy as np

from universe24.algebra.frame_matter import FIELDS, sampled
from universe24.algebra.null_covector import integer_array
from universe24.core import State
from universe24.core.lattice import lattice
from universe24.prepare.frame48 import flat_values as vacuum_flat_values


def flat_values(L):
    return np.concatenate((vacuum_flat_values(L), np.zeros((11, lattice(L).N), dtype=object)))


def increment(program, values, lat):
    rhs, _, _ = sampled(values, lat, program.dx, program.mass_squared)
    rows = [np.broadcast_to(2*program.dt*rhs[name], (lat.N,)) for name in FIELDS]
    values = np.array(rows, dtype=object)
    if any(getattr(v, 'denominator', 1) != 1 for v in values.flat):
        raise ValueError('Noninteger increment outside the compiled sector')
    return np.array([int(v) for v in values.flat], dtype=object).reshape(values.shape)


def prepare(program, previous, current, *, L, remainders=None):
    lat = lattice(L)
    x, y = integer_array(previous), integer_array(current)
    if x.shape != (35, lat.N) or y.shape != x.shape:
        raise ValueError('Expected two arrays of shape (35,L^3)')
    b = np.concatenate((x, y))
    a = np.concatenate((y-increment(program, x, lat), x))
    r = np.zeros_like(b) if remainders is None else integer_array(remainders)
    if r.shape != b.shape or np.any(r < 0) or np.any(r >= 6):
        raise ValueError('Expected remainders of shape (70,L^3) in [0,6)')
    return State(L, a, b, r)
