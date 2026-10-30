"""Clock: a vertex couples a Node-clock's gears: each term of one potential pushes every one of its legs by the others.
Algebra: each monomial f x_a x_b x_c x_d pushes each leg by -f times the other three, the unit for a leg it lacks, summed into J; read is the clocks' linear read.
Board: at every Node-clock alike, on its own readings at the now slot: the value, the three gradients, the force, then the unit.
Clicks: the rest beat a spring gives is read as a mass; the strengths are open (G3).
"""

import numpy as np

from tensor24.algebra.carry import Z
from tensor24.engine.state import Plan, Read


def pushes(factor: Z, legs: tuple[Z, Z, Z, Z]) -> Plan:
    """J's terms from one potential, the sum of each monomial's whole factor times its four legs' readings, the unit (the readings' last row, -1) for a leg it lacks: every leg pushed by minus the factor times the other three, so each vertex pushes all its legs and keeps one energy; a push on the unit lands on the source's own unit row, which no gear reads."""
    a, b, c, d = legs
    return Plan(
        np.concatenate((b, c, d, a)),
        np.concatenate((c, d, a, b)),
        np.concatenate((d, a, b, c)),
        -np.concatenate((factor, factor, factor, factor)),
        np.concatenate((a, b, c, d)),
    )


def contract(plan: Plan, readings: Z, gears: Z) -> Z:
    """Every gear's source J in the gears' shape, Python integers on any gears: a gather, a product of three readings, a scattered sum; a spring reads one, a three-leg vertex two, a four-leg term three."""
    first, second, third, factor, target = plan
    source = np.concatenate((0 * gears, 0 * gears[:1]))  # the gears' rows and the unit's, last
    np.add.at(source, target, factor[:, None] * readings[first] * readings[second] * readings[third])
    return source[:-1]


def read(plan: Read, gears: Z) -> Z:
    """What a linear read lands on every gear, in the gears' shape: a gather of the now counts, a product, a scattered sum."""
    first, factor, target = plan
    landed = np.zeros_like(gears, dtype=object)
    np.add.at(landed, target, factor[:, None] * gears[first])
    return landed
