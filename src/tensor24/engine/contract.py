"""The contraction: the coupling rows' products of two readings into their targets, through the 24's tables."""

import numpy as np

from tensor24.algebra.carry import Z
from tensor24.engine.state import Plan


def contract(plan: Plan, readings: Z, gears: Z) -> Z:
    """Every gear's source J in the gears' shape, Python integers on any gears: a gather, a product, a scattered sum."""
    first, second, factor, target = plan
    source = np.zeros_like(gears, dtype=object)
    np.add.at(source, target, factor[:, None] * readings[first] * readings[second])
    return source
