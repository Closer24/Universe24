"""The Node-clock's step: every gear's impulse, drive and carry at the teeth its clock gives it, in one pass every round, and the run back as the step on the mirrored state."""

import numpy as np

from tensor24.algebra.carry import Z, carry, flip
from tensor24.engine.contract import contract, read
from tensor24.engine.mesh import pull, seen
from tensor24.engine.state import Gearing, Layout, Read, State


def gear(a: Z, b: Z, r: Z, w: Z, push: Z) -> tuple[Z, Z, Z]:
    """A gear's tick at its teeth W: (q, r+) the carry of W (a - b) + push with its fine tooth r, and a+ = a + q."""
    q, kept = carry(w * (a - b) + push, w, r)
    return a + q, a, kept


def drive(j: Z, teeth: Z, rd: Z) -> tuple[Z, Z]:
    """The drive: (q, r_d+), the carry of the source J at the drive's teeth T_d; on the force's path, T_d = 1, q is J."""
    return carry(j, teeth, rd)


def sources(layout: Layout, a: Z) -> tuple[Z, Z]:
    """Every gear's force, its pull, and its source J: the plan on the value, the differences along each axis, the force, and the unit."""
    nb, spokes, _, _, _, plan, _, _ = layout
    force = pull(layout, a)
    # each axis's + neighbour less its - neighbour: the neighbours summed with their Spokes' directions
    gradient = np.tensordot(spokes, seen(a, nb), axes=(0, 1))
    readings = np.concatenate((np.expand_dims(a, 0), gradient, np.expand_dims(force, 0)))
    # the unit, the readings' last row, for each reading a term lacks of three
    flat = np.concatenate((readings.reshape(-1, a.shape[-1]), np.ones_like(a[:1], dtype=object)))
    return force, contract(plan, flat, a)


def driven(gearing: Gearing, force: Z, q: Z) -> Z:
    """The push on every gear, s F + K with the kick K = T_k s q: the force, and every source through the drive."""
    _, stretch, kick, _ = gearing
    return stretch * (force + kick * q)


# W = W+ holds a round's teeth fixed, so a round runs back exactly wherever W is at least 1 and every fine tooth stands
# within [0, W), and a run while every kept tooth stands below the teeth of the round that reads it: only a falling
# clock can break that. Wherever a clock moves, rising or falling, W = W+ drops the term (d_t W)(d_t a) of
# d_t (W d_t a) = F. No source moves the metric family before G2, but a setting may lay it moving: the runner reads
# the promise from outside before every round and names the round where it breaks; the metric's stage (G2) owes both
# by design.
def weight(gearing: Gearing, clock: Read, a: Z) -> Z:
    """Every gear's teeth W = W+: its rest and what the clocks' read lands on it at the now slot, by no table and with no bound on the read."""
    rest, _, _, _ = gearing
    return rest + read(clock, a)


def teeth(layout: Layout, s: State) -> Z:
    """Every gear's teeth at the state's now slot, as its round reads them: the promise's measure, read from outside."""
    _, _, _, _, gearing, _, clock, _ = layout
    a, _, _, _ = s
    return weight(gearing, clock, a)


def tick(layout: Layout, s: State) -> State:
    """One round: every gear steps on its sources at the teeth it reads at the now slot, in one pass."""
    _, _, _, _, gearing, _, clock, _ = layout
    a, b, r, rd = s
    force, j = sources(layout, a)
    _, _, _, teeth = gearing
    q, kept = drive(j, teeth, rd)
    a1, b1, r1 = gear(a, b, r, weight(gearing, clock, a), driven(gearing, force, q))
    return State(a1, b1, r1, kept)


def mirror(layout: Layout, s: State) -> State:
    """The state mirrored, time's reversal at fixed teeth: the slots swapped, each fine tooth flipped in the teeth it was kept at, the before slot's; mirrored twice, r moves by W(a) - W(b), so the mirror is its own inverse only where the clock stands still."""
    _, _, _, _, gearing, _, clock, _ = layout
    a, b, r, rd = s
    _, _, _, teeth = gearing
    return State(b, a, flip(r, weight(gearing, clock, b)), flip(rd, teeth))


def untick(layout: Layout, s: State) -> State:
    """The round run back, the tick on the mirrored state mirrored: tick's inverse from the states whose fine teeth stand within the now slot's teeth, of at least 1, onto those whose fine teeth stand within the before slot's; n rounds run back by n unticks, not by one mirror about n ticks, which departs from the second round where the clock moves."""
    return mirror(layout, tick(layout, mirror(layout, s)))
