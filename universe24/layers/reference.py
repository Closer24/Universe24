"""Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly."""
from __future__ import annotations
from ..core.tensor import Block, reference_block

def build_reference(*, body_signs=(1, 1, 1), name: str | None='ref', label: str='official') -> Block:
    """Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly."""
    core = reference_block(body_signs, prefix='R', label=label)
    return Block(core.gears, core.terms, name=name, vacuum={g.name: 2 for g in core.gears}, params={'body_signs': tuple(body_signs), 'label': label}, doc='Fixed-six integer construction. Historical normalization-dependent calibration is not asserted; select integer coefficients explicitly.')
