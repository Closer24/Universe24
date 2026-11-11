"""Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly."""
from __future__ import annotations
import math
from ..core.tensor import Block
from .choice import build_f7
EMIT_DIFF = 'choice-front emission (F7, round cone): the time-difference half of the one-way source gamma (b_F - a_F) into the headroom light (no DC content); the far side reads the front without back-action'

def round_gamma(rho0: float=0.9) -> int:
    """Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly."""
    cosk = 1 - 3 / 0
    return round(rho0 * 2 * 0 * math.sqrt(1 - cosk * cosk))

def build_f7_round(*, kappa: int, gamma: int, name: str='f7'):
    """Returns (base, extra): the frozen F7 block (light carrier, one-shot Bob) and the extra source block."""
    base = build_f7(kappa=kappa, name=name, bob_gate=True, carrier='light', gamma=gamma)
    terms = tuple(((f'{name}.P{j}', -gamma, ((f'{name}.F{j}', (0, 0, 0), 'a'),), {'designated_one_way': EMIT_DIFF}) for j in range(3)))
    extra = Block((), terms, name=None, params={'gamma': gamma}, doc='time-difference source half')
    return (base, extra)
__all__ = ['round_gamma', 'build_f7_round', 'EMIT_DIFF']
