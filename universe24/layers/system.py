"""Fixed-divisor-six system assembly.

The default is the 48-channel cube-group reference tensor. The previous
large-divisor field assembly is retired: its calibration is not silently
rounded into integer coefficients. Optional blocks may be composed explicitly.
"""
from __future__ import annotations
from dataclasses import dataclass, field
import hashlib
from pathlib import Path
from ..core.tensor import Block
BODY_SIGNS_DEFAULT = (1, -1, 1)
P_GRAV, K_GRAV = (1, 0)
HOP, WILSON, MASS_DEFAULT = (1, 0, 2)
MASS_PROPOSED = MASS_DEFAULT
E1_PARAMS = {'g_phi': 1, 'g_A': 1, 'sigma': 1}
E1D_SIGMA = 1
C2_PARAMS = {'A': 1, 'lam': 0}
C2_DEFAULT = False
ROOT = Path(__file__).resolve().parent.parent
LAYER_FILES = ('layers/reference.py', 'core/tensor.py', 'core/engine.py', 'core/reversors.py')

@dataclass
class System:
    """Fixed tensor blocks and construction metadata; no divisor parameter."""
    blocks: tuple
    info: dict = field(default_factory=dict)

    def by_name(self, name: str) -> Block:
        for block in self.blocks:
            if block.name == name:
                return block
        raise KeyError(name)

def with_vacuum(block: Block, value: int, params_extra: dict | None=None) -> Block:
    if type(value) is not int or not 0 <= value < 6:
        raise ValueError('fixed-six remainder must lie in 0..5')
    return Block(block.gears, block.terms, name=block.name, vacuum={name: value for name in block.vacuum}, params={**block.params, **(params_extra or {})}, doc=block.doc)

def file_hashes() -> dict:
    return {rel: hashlib.sha256((ROOT / rel).read_bytes()).hexdigest() for rel in LAYER_FILES}

def default_system(*, body_signs=BODY_SIGNS_DEFAULT, label: str='official', extra_blocks: tuple=(), **retired_options) -> System:
    """Build the explicit 48-channel baseline, with optional declared blocks.

    Old field-assembly options are rejected; they cannot preserve their former
    dynamics at divisor six. No electromagnetic or gravitational claim is
    attached to this baseline.
    """
    if retired_options:
        raise ValueError('retired large-divisor assembly options: ' + ', '.join(sorted(retired_options)) + '; compose validated fixed-six blocks explicitly')
    from .reference import build_reference
    reference = build_reference(body_signs=body_signs, name='ref', label=label)
    if any((not isinstance(block, Block) for block in extra_blocks)):
        raise TypeError('extra_blocks must contain validated Block values')
    if any((block.name == 'ref' for block in extra_blocks)):
        raise ValueError('reference namespace is reserved')
    info = {'D': 6, 'body_signs': tuple(body_signs), 'implementation': 'fixed-six-reference', 'reference_label': label, 'default_gear_count': 48, 'scope': 'cube-group integer reference automaton; no emergent physics asserted', 'retired_large_divisor_assembly': True, 'file_hashes': file_hashes()}
    return System((reference,) + tuple(extra_blocks), info)
__all__ = ['System', 'default_system', 'with_vacuum', 'file_hashes', 'P_GRAV', 'K_GRAV', 'HOP', 'WILSON', 'MASS_DEFAULT', 'MASS_PROPOSED', 'E1_PARAMS', 'E1D_SIGMA', 'BODY_SIGNS_DEFAULT', 'C2_PARAMS', 'C2_DEFAULT']
