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
    """Every gear's force, its pull, and its source J: the plan on the value, the differences, the force."""
    nb, _, _, _, plan, _ = layout
    force = pull(layout, a)
    near = seen(a, nb)
    rows, _, sites = near.shape
    ends = near.reshape(rows, -1, 1 + 1, sites)
    gradient = np.moveaxis(ends[:, :, 0] - ends[:, :, 1], 1, 0)
    readings = np.concatenate((np.expand_dims(a, 0), gradient, np.expand_dims(force, 0)))
    return force, contract(plan, readings.reshape(-1, sites), a)


def driven(gearing: Gearing, force: Z, q: Z) -> Z:
    """The push on every gear, s F + K with the kick K = T_k s q: the force, and every source through the drive."""
    _, stretch, kick, _ = gearing
    return stretch * (force + kick * q)


# W = W+ holds a round's teeth fixed, so a round runs back exactly wherever W is at least 1 and every fine tooth stands
# within [0, W), and a run while every kept tooth stands below the teeth of the round that reads it: only a falling
# clock can break that. Wherever a clock moves, rising or falling, W = W+ drops the term (d_t W)(d_t a) of
# d_t (W d_t a) = F. Every run the files make keeps the clock's own gear at 0 as laid, no source moving it; the
# metric's stage (G2) owes both by design, with no promise in the round.
def weight(gearing: Gearing, clock: Read, a: Z) -> Z:
    """Every gear's teeth W = W+: its rest and what the clocks' read lands on it at the now slot, by no table and with no bound on the read."""
    rest, _, _, _ = gearing
    return rest + read(clock, a)


def tick(layout: Layout, s: State) -> State:
    """One round: every gear steps on its sources at the teeth it reads at the now slot, in one pass."""
    _, _, _, gearing, _, clock = layout
    a, b, r, rd = s
    force, j = sources(layout, a)
    _, _, _, teeth = gearing
    q, kept = drive(j, teeth, rd)
    a1, b1, r1 = gear(a, b, r, weight(gearing, clock, a), driven(gearing, force, q))
    return State(a1, b1, r1, kept)


def mirror(layout: Layout, s: State) -> State:
    """The state mirrored, time's reversal: the slots swapped, each fine tooth flipped in the teeth it was kept at, the before slot's."""
    _, _, _, gearing, _, clock = layout
    a, b, r, rd = s
    _, _, _, teeth = gearing
    return State(b, a, flip(r, weight(gearing, clock, b)), flip(rd, teeth))


def untick(layout: Layout, s: State) -> State:
    """The round run back, the tick on the mirrored state mirrored: exact where every fine tooth it ran from stood within its teeth, of at least 1."""
    return mirror(layout, tick(layout, mirror(layout, s)))
