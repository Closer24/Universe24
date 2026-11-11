"""Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly."""
from __future__ import annotations
from fractions import Fraction
from ..core.tensor import Block, GearType
from . import gravity as gr

def build_beta_detuned(*, P: int, k: int, field: str, num: int=1, den: int=2, name: str='beta', gear: str='G', r0: int | None=None) -> Block:
    """The automatic normalization-dependent calibration is retired."""
    raise NotImplementedError('calibration removed; choose an explicit integral fixed-six tensor')

def replace_beta(blocks, fixed: Block):
    """Return the block tuple with the block named fixed.name replaced (composition order kept)."""
    out, hit = ([], False)
    for b in blocks:
        if b.name == fixed.name:
            out.append(fixed)
            hit = True
        else:
            out.append(b)
    if not hit:
        raise KeyError(fixed.name)
    return tuple(out)
