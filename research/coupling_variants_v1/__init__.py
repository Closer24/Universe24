"""Explicitly separate candidate couplings for Universe24 (not the reference model).

A 2O-covariant, reciprocal six-port table is chosen before the run and then
fixed; every channel is updated by the reference Rule3 primitive imported from
``universe24.core.rule3``. With one of the eight reference tables the executor
equals the native Engine bit for bit. Results with any other table carry
``VariantCoupling.label``. See README.md.

    from research.coupling_variants_v1 import VariantCoupling, VariantEngine
    engine = VariantEngine(VariantCoupling.axial("axial-017", m=(0, 1, 7)))
"""
from .config import (CHECKPOINT_FORMAT, INIT_FORMAT, VariantExperiment, checkpoint_data, from_dict,
                     init_data, load, read_checkpoint, write_init)
from .coupling import (AXIAL_PAIRS, COUPLING_FORMAT, SIGN_TRIPLES, VariantCoupling, axial_actions,
                       character, covariant_family, pairing, partner)
from .engine import VariantEngine
from .gauge import chi_gauge_state, staggered_state

__all__ = ["AXIAL_PAIRS", "CHECKPOINT_FORMAT", "COUPLING_FORMAT", "INIT_FORMAT", "SIGN_TRIPLES",
           "VariantCoupling", "VariantEngine", "VariantExperiment", "axial_actions", "character",
           "checkpoint_data", "chi_gauge_state", "covariant_family", "from_dict", "init_data", "load",
           "pairing", "partner", "read_checkpoint", "staggered_state", "write_init"]
