"""The contraction: J's terms, products of three readings into their targets through the 24's tables, and the clocks' linear read."""

import numpy as np

from tensor24.algebra.carry import Z
from tensor24.engine.state import Plan, Read


def contract(plan: Plan, readings: Z, gears: Z) -> Z:
    """Every gear's source J in the gears' shape, Python integers on any gears: a gather, a product of three readings, a scattered sum; a spring reads one, a three-leg vertex two, a four-leg term three."""
    first, second, third, factor, target = plan
    source = np.zeros_like(gears, dtype=object)
    np.add.at(source, target, factor[:, None] * readings[first] * readings[second] * readings[third])
    return source


def read(plan: Read, gears: Z) -> Z:
    """What a linear read lands on every gear, in the gears' shape: a gather of the now counts, a product, a scattered sum."""
    first, factor, target = plan
    landed = np.zeros_like(gears, dtype=object)
    np.add.at(landed, target, factor[:, None] * gears[first])
    return landed
