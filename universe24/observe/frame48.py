"""Passive constraint and geometry checks; never repairs frame48 states."""
import numpy as np
import sympy as sp

from universe24.algebra.frame_equations import FIELDS, sampled
from universe24.algebra.null_covector import integer_array
from universe24.core.lattice import lattice


def bank_values(state, bank='Y'):
    if state.G != 48 or bank not in ('X', 'Y'):
        raise ValueError('Extract a 48-channel frame component and select X or Y')
    start = 0 if bank == 'X' else 24
    return state.b[start:start+24].astype(object).copy()


def diagnostics(values, *, L, dx=1):
    """Report defects of the declared finite differences, not continuum errors."""
    _, constraints, _ = sampled(values, lattice(L), dx)
    arrays = {name: np.broadcast_to(value, (L**3,)) for name, value in constraints.items()}
    B = np.asarray(values[:9], dtype=object).T.reshape(L**3, 3, 3)
    det = (B[:, 0, 0]*(B[:, 1, 1]*B[:, 2, 2]-B[:, 1, 2]*B[:, 2, 1])
           - B[:, 0, 1]*(B[:, 1, 0]*B[:, 2, 2]-B[:, 1, 2]*B[:, 2, 0])
           + B[:, 0, 2]*(B[:, 1, 0]*B[:, 2, 1]-B[:, 1, 1]*B[:, 2, 0]))
    return {'peak_constraints': {name: str(max(abs(v) for v in row)) for name, row in arrays.items()},
            'all_discrete_constraints_zero': all(not any(row) for row in arrays.values()),
            'singular_nodes': int(np.count_nonzero(det == 0)),
            'minimum_abs_det_B': str(min(abs(v) for v in det))}


def inverse_metric_at(values, node=0):
    """Polynomial contravariant metric diag(-1,B^T B); no ratio readout.

    Synchronous lapse=1 fixes coordinate proper time for normal observers.
    It does not create a ticking clock or test gravitational redshift.
    """
    values = integer_array(values)
    if values.ndim != 2 or values.shape[0] != 24 or not 0 <= node < values.shape[1]:
        raise ValueError('Expected 24 fields and a valid node')
    B = sp.Matrix([[values[FIELDS.index(f'B{a}{i}'), node] for i in range(3)] for a in range(3)])
    if B.det() == 0:
        raise ValueError('Degenerate frame; no physical metric readout')
    return sp.diag(-1, B.T*B)
