"""Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly."""
from __future__ import annotations
import math
from fractions import Fraction
from ..core.tensor import Block
from . import gravity as gr
from .gravity_l0c import l0c_lapse_potential
from .matter import algebra, matter_names
from .matter_lapse_c import matter_lapse_c_potential
ZERO = (0, 0, 0)
HYB_WHY = 'HYBRID gravity source (Study 10, owner decision 2, 13:09): two-time density (L0 Board-Noether energy / Dirac carrier-number Wronskian) read with a-reads; no b-only quadratic quantity is conserved under Rule3 (G-NOGO-a = G1), so an exactly conserved source has no reciprocal partner: designated one-way'
HYB_ACT_WHY = 'HYBRID: the lapse ACTION on L0 / the Dirac pair (form C, R1) kept; its reciprocal b-only source is replaced by the two-time hybrid source (one-way)'

def rho_g_default(matter: Block, P: int) -> int:
    """Retired normalization-dependent calibration; no fixed-six equivalence is asserted."""
    raise NotImplementedError('this automatic large-divisor calibration was removed; supply an explicit fixed-six tensor instead')

def hybrid_source_terms(*, P: int, field: str, ref: Block, matter: Block, g: int | None=None, l0: bool=True, dirac: bool=True) -> list:
    """Retired normalization-dependent calibration; no fixed-six equivalence is asserted."""
    raise NotImplementedError('this automatic large-divisor calibration was removed; supply an explicit fixed-six tensor instead')

def build_hybrid_source(*, P: int, field: str, ref: Block, matter: Block, g: int | None=None, l0: bool=True, dirac: bool=True, name: str='hsrc') -> Block:
    """Retired normalization-dependent calibration; no fixed-six equivalence is asserted."""
    raise NotImplementedError('this automatic large-divisor calibration was removed; supply an explicit fixed-six tensor instead')

def oneway_matter_lapse(*, P: int, field: str, matter: Block, name: str='mlapse') -> Block:
    """Retired normalization-dependent calibration; no fixed-six equivalence is asserted."""
    raise NotImplementedError('this automatic large-divisor calibration was removed; supply an explicit fixed-six tensor instead')

def oneway_l0_lapse(*, P: int, field: str, body_signs, ns: str='ref', name: str='lapseL0') -> Block:
    """Retired normalization-dependent calibration; no fixed-six equivalence is asserted."""
    raise NotImplementedError('this automatic large-divisor calibration was removed; supply an explicit fixed-six tensor instead')

def detuned_h00_metric(metric: Block, gear: str='h00', num: int=1, den: int=2) -> Block:
    """Retired normalization-dependent calibration; no fixed-six equivalence is asserted."""
    raise NotImplementedError('this automatic large-divisor calibration was removed; supply an explicit fixed-six tensor instead')

def apply_hybrid(system, *, g: int | None=None, beta_fix: bool=True, detune_h00: bool=False):
    """Retired normalization-dependent calibration; no fixed-six equivalence is asserted."""
    raise NotImplementedError('this automatic large-divisor calibration was removed; supply an explicit fixed-six tensor instead')

def hybrid_system(*, g: int | None=None, beta_fix: bool=True, detune_h00: bool=False, **kw):
    """Retired normalization-dependent calibration; no fixed-six equivalence is asserted."""
    raise NotImplementedError('this automatic large-divisor calibration was removed; supply an explicit fixed-six tensor instead')
__all__ = ['HYB_WHY', 'HYB_ACT_WHY', 'rho_g_default', 'hybrid_source_terms', 'build_hybrid_source', 'oneway_matter_lapse', 'oneway_l0_lapse', 'detuned_h00_metric', 'apply_hybrid', 'hybrid_system']
