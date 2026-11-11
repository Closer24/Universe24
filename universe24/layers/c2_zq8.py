"""Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly."""
from __future__ import annotations
from fractions import Fraction
from ..core.tensor import Block, GearType
from .gauge import UNIT, Poly, deviation_terms, vec_dot
from .links import Q8_LABEL, Q8_ORDER, _link_names, right_perm
CHARACTERS = {'eps0': (1, 1, 1, 1, 1, 1, 1, 1), 'eps_i': (1, 1, -1, -1, 1, 1, -1, -1), 'eps_j': (1, -1, 1, -1, 1, -1, 1, -1), 'eps_k': (1, -1, -1, 1, 1, -1, -1, 1)}
H_PAIRS = ((0, 4), (1, 5), (2, 6), (3, 7))

def _coupling(body_signs):
    from universe24.algebra.coupling import coupling
    return coupling(tuple(body_signs))

def components(U):
    """(chi values dict, |h|^2) of one link's 8 coefficients (Python ints or Polys)."""
    chis = {n: sum((s * u for s, u in zip(sig, U))) for n, sig in CHARACTERS.items()}
    h2 = sum(((U[p] - U[m]) * (U[p] - U[m]) for p, m in H_PAIRS))
    return (chis, h2)

def build_c2_zq8(*, kappa: int, lam: int, body_signs=(1, -1, 1), port_weight: int | None=None, ref: str='ref', name: str='c2', field_label: str='audit') -> Block:
    """Retired normalization-dependent calibration; no fixed-six equivalence is asserted."""
    raise NotImplementedError('this automatic large-divisor calibration was removed; supply an explicit fixed-six tensor instead')

def q8_gauge_map_names():
    """Q8 element names in links.py's component order (for the covariance check)."""
    return (Q8_ORDER, Q8_LABEL)
__all__ = ['build_c2_zq8', 'CHARACTERS', 'H_PAIRS', 'components']
