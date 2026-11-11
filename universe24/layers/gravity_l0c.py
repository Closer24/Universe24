"""Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly."""
from __future__ import annotations
from fractions import Fraction
from ..core.tensor import Block
from . import gravity as gr
from .gravity_l0 import l0_hops
from .reference import build_reference
ZERO = (0, 0, 0)
L0C_READ_WHY = 'form-C L0 clock TEST read (one-way): a static prescribed lapse gear read by L0 clocks; the reciprocal block (oneway=False) is checked separately'

def build_l0c(*, body_signs=(1, -1, 1), name: str='ref', label: str='official') -> Block:
    """Retired normalization-dependent calibration; no fixed-six equivalence is asserted."""
    raise NotImplementedError('this automatic large-divisor calibration was removed; supply an explicit fixed-six tensor instead')

def m0_matrix(body_signs=(1, -1, 1)):
    """L0's mass matrix M0 = 6*1 - Sum_d W_d (integer 48 x 48, symmetric), from universe24's coupling (read-only)."""
    import numpy as np
    from universe24.algebra.coupling import coupling
    C = coupling(tuple(body_signs))
    S0 = np.zeros((48, 48), dtype=np.int64)
    for d in range(6):
        for g in range(48):
            S0[C.ports[d][g], g] += C.weights[d][g]
    return 6 * np.eye(48, dtype=np.int64) - S0

def l0c_lapse_potential(P: int, field: str, ns: str='ref', body_signs=(1, -1, 1)) -> list:
    """Retired normalization-dependent calibration; no fixed-six equivalence is asserted."""
    raise NotImplementedError('this automatic large-divisor calibration was removed; supply an explicit fixed-six tensor instead')

def build_l0c_lapse(*, P: int, field: str, ns: str='ref', body_signs=(1, -1, 1), oneway: bool=False, name: str='lapseL0') -> Block:
    """Retired normalization-dependent calibration; no fixed-six equivalence is asserted."""
    raise NotImplementedError('this automatic large-divisor calibration was removed; supply an explicit fixed-six tensor instead')
__all__ = ['build_l0c', 'build_l0c_lapse', 'l0c_lapse_potential', 'm0_matrix', 'L0C_READ_WHY']
