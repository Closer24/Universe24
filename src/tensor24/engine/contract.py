"""Clock: a vertex couples a Node-clock's gears: each term of one potential pushes every one of its legs by the others.
Algebra: each monomial f x_1 ... x_k, of any number k of legs, pushes each leg by -f times the other k - 1, the unit for a leg it lacks, summed into J.
Board: at every Node-clock alike, on its own readings at the now slot: the value, the three gradients, the force, then the unit.
Clicks: the rest beat a spring gives is read as a mass; the strengths are open (G3).
"""

import numpy as np

from tensor24.algebra.carry import Z
from tensor24.engine.state import Plan


def pushes(factor: Z, legs: tuple[Z, ...]) -> Plan:
    """J's terms from one potential, the sum of each monomial's whole factor times its legs' readings, any number of legs, the unit (the readings' last row, -1) for a leg it lacks: every leg pushed by minus the factor times the other legs, read round the monomial from the leg after it, so each vertex pushes all its legs and keeps one energy; the legs round from each one are their circulant, the legs tiled once more than their count and folded, so that row j holds the legs from j on; a push on the unit lands on the source's own unit row, which no gear reads."""
    held = np.stack(legs)  # (legs, monomials)
    count, monomials = held.shape
    turned = np.tile(held, (count + 1, 1)).reshape(count, count + 1, monomials)[:, :count]
    return Plan(
        np.moveaxis(turned[:, 1:], 1, 0).reshape(count - 1, count * monomials),
        -np.tile(factor, count),
        held.reshape(count * monomials),
    )


def joined(narrow: Plan, wide: Plan) -> Plan:
    """Two plans as one, the narrow's terms first, each reading the unit for the legs it reads fewer of than the wide's (J's two blocks by their legs' count, so no push on the unit is laid: MIN2's item 2)."""
    legs, factor, target = narrow
    more, also, onto = wide
    lacking = np.broadcast_to(0 * legs[:1] - 1, (more.shape[0] - legs.shape[0], legs.shape[1]))
    return Plan(
        np.concatenate((np.concatenate((legs, lacking)), more), axis=1),
        np.concatenate((factor, also)),
        np.concatenate((target, onto)),
    )


def contract(plan: Plan, readings: Z, gears: Z) -> Z:
    """Every gear's source J in the gears' shape, Python integers on any gears: a gather of each term's legs, their product with the factor first (so a term at the factor 0 multiplies no count), a scattered sum; a spring reads one, a three-leg vertex two, a k-leg monomial's term k - 1."""
    legs, factor, target = plan
    zero = np.zeros_like(gears, dtype=object)  # Python integers whatever the gears hold
    source = np.concatenate((zero, zero[:1]))  # the gears' rows and the unit's, last
    first = factor[None, :, None] + 0 * readings[-1:, None]  # the factor at every site, before the legs
    np.add.at(source, target, np.prod(np.concatenate((first, readings[legs])), axis=0))
    return source[:-1]
