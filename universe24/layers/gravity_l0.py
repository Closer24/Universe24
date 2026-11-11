"""Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly."""
from __future__ import annotations
from fractions import Fraction
from ..core.tensor import Block, GearType
from . import gravity as gr
from .reference import build_reference
ZERO = (0, 0, 0)
L0_READ_WHY = 'L0-EP clock TEST read (one-way): a static prescribed lapse gear read by L0 / matter clocks; the reciprocal block (oneway=False) is checked separately'

def l0_hops(body_signs=(1, 1, 1), ns: str='ref') -> list[tuple]:
    """Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly."""
    ref = build_reference(body_signs=body_signs, name=ns)
    spec = gr.spec_from_block(ref, order=1, carrier={g.name: 0 for g in ref.gears})
    return list(spec.hops)

def build_l0_weight(*, body_signs=(1, 1, 1), name: str='ref') -> Block:
    """Retired normalization-dependent calibration; no fixed-six equivalence is asserted."""
    raise NotImplementedError('this automatic large-divisor calibration was removed; supply an explicit fixed-six tensor instead')

def l0_lapse_potential(P: int, field: str, ns: str='ref', gamma: str='GR', body_signs=(1, 1, 1)) -> list:
    """Retired normalization-dependent calibration; no fixed-six equivalence is asserted."""
    raise NotImplementedError('this automatic large-divisor calibration was removed; supply an explicit fixed-six tensor instead')

def build_l0_lapse(*, P: int, field: str, ns: str='ref', gamma: str='GR', body_signs=(1, 1, 1), oneway: bool=False, name: str='lapseL0') -> Block:
    """Retired normalization-dependent calibration; no fixed-six equivalence is asserted."""
    raise NotImplementedError('this automatic large-divisor calibration was removed; supply an explicit fixed-six tensor instead')
