"""Clock: every round every gear moves once: its neighbours pull it, the coupling pushes it, it turns by what its teeth carry and keeps the rest; the drive carries the coupling's push the same way, and each train's click tooth carries the area the kick moves into the train.
Algebra: q, r+ = carry(W (a - b) + s F + K, W, r); a+ = a + q; b+ = a; q_d, r_d+ = carry(J, T_d, r_d); K = s T_k q_d; q_c, k+ = carry(tau, key, k), tau the cross of a train's two parts with the kick through the A1 table; the run back is the tick on the mirrored state, mirrored.
Board: one pass at every Node-clock alike, reading only its own gears and its six Meshes at the now slot; W is the rest plus the metric family's 00 slots here; the click pushes nothing into a, b, r or r_d.
Clicks: a whole click is the click tooth's quotient, one quantum taken (+1) or given back (-1), left for the record from G5; a deeper 00 slot is a slower clock, read in the clicks as proper time.
"""

import numpy as np

from tensor24.algebra.carry import Z, carry, flip
from tensor24.engine.contract import contract, read
from tensor24.engine.mesh import held, pull, seen
from tensor24.engine.state import Click, Gearing, Layout, Read, State


def gear(a: Z, b: Z, r: Z, w: Z, push: Z) -> tuple[Z, Z, Z]:
    """A gear's tick at its teeth W: (q, r+) the carry of W (a - b) + push with its fine tooth r, and a+ = a + q."""
    q, kept = carry(w * (a - b) + push, w, r)
    return a + q, a, kept


def drive(j: Z, teeth: Z, rd: Z) -> tuple[Z, Z]:
    """The drive: (q, r_d+), the carry of the source J at the drive's teeth T_d; on the force's path, T_d = 1, q is J."""
    return carry(j, teeth, rd)


def sources(layout: Layout, a: Z) -> tuple[Z, Z]:
    """Every gear's force, its pull, and its source J: the plan on the value, the differences along each axis, the force, and the unit."""
    nb, spokes, _, _, _, plan, _, _, _ = layout
    force = pull(layout, a)
    # each axis's + neighbour less its - neighbour: the neighbours summed with their Spokes' directions
    gradient = np.tensordot(spokes, seen(a, nb), axes=(0, 1))
    readings = np.concatenate((np.expand_dims(a, 0), gradient, np.expand_dims(force, 0)))
    # the unit, the readings' last row, for each reading a term lacks of three
    flat = np.concatenate((readings.reshape(-1, a.shape[-1]), np.ones_like(a[:1], dtype=object)))
    return force, contract(plan, flat, a)


def kick(gearing: Gearing, q: Z) -> Z:
    """The kick on every gear, K = T_k s q_d: the drive's whole turns at the kick's teeth, stretched."""
    _, stretch, teeth, _ = gearing
    return stretch * teeth * q


def driven(gearing: Gearing, force: Z, kicks: Z) -> Z:
    """The push on every gear, s F + K: the force stretched, and the kick the gear takes."""
    _, stretch, _, _ = gearing
    return stretch * force + kicks


def area(click: Click, a: Z, kicks: Z, k: Z) -> Z:
    """Every train's swept area tau in the trains' shape, the click tooth's: the cross of its two parts with the kick through the A1 table, a gather of the now counts and the kicks, a product, a scattered sum."""
    first, second, factor, target, _ = click
    moved = 0 * k
    np.add.at(moved, target, factor[:, None] * a[first] * kicks[second])
    return moved


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
    _, _, _, _, gearing, _, clock, _, _ = layout
    a, _, _, _, _ = s
    return weight(gearing, clock, a)


def grips(layout: Layout, s: State) -> Z:
    """Every Spoke's grip at every gear and site at the state's now slot, as its round reads them: the window's measure, read from outside."""
    a, _, _, _, _ = s
    return held(layout, a)


def act(layout: Layout, s: State) -> tuple[State, Z]:
    """One round and its clicks, in one pass: every gear steps on its sources at the teeth it reads at the now slot, and every train's click tooth carries the area the kick moves into the train at the key; the clicks are that carry's quotients, (the state reached, the clicks)."""
    _, _, _, _, gearing, _, clock, _, click = layout
    a, b, r, rd, k = s
    force, j = sources(layout, a)
    _, _, _, teeth = gearing
    _, _, _, _, key = click
    q, kept = drive(j, teeth, rd)
    kicks = kick(gearing, q)
    a1, b1, r1 = gear(a, b, r, weight(gearing, clock, a), driven(gearing, force, kicks))
    clicks, k1 = carry(area(click, a, kicks, k), key, k)
    return State(a1, b1, r1, kept, k1), clicks


def tick(layout: Layout, s: State) -> State:
    """One round: the state the act reaches, its clicks left for the record."""
    moved, _ = act(layout, s)
    return moved


def mirror(layout: Layout, s: State) -> State:
    """The state mirrored, time's reversal at fixed teeth: the slots swapped, each fine tooth flipped in the teeth it was kept at, the before slot's, the drive's in its teeth and the click tooth in its key; mirrored twice, r moves by W(a) - W(b), so the mirror is its own inverse only where the clock stands still."""
    _, _, _, _, gearing, _, clock, _, click = layout
    a, b, r, rd, k = s
    _, _, _, teeth = gearing
    _, _, _, _, key = click
    return State(b, a, flip(r, weight(gearing, clock, b)), flip(rd, teeth), flip(k, key))


def untick(layout: Layout, s: State) -> State:
    """The round run back, the tick on the mirrored state mirrored: tick's inverse from the states whose fine teeth stand within the now slot's teeth, of at least 1, onto those whose fine teeth stand within the before slot's; n rounds run back by n unticks, not by one mirror about n ticks, which departs from the second round where the clock moves."""
    return mirror(layout, tick(layout, mirror(layout, s)))
