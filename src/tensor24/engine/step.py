"""Clock: every round every gear moves once: its neighbours pull it, the coupling pushes it, and its momentum, the velocity's whole count with the tooth kept on the edge between its two slots, is carried to the next edge and split there in one dial of both slots' teeth; the drive carries the coupling's push the same way, and each train's click tooth carries the area the kick moves into the train.
Algebra: D_in = W(b) + W(a); N = 2 (D_in (a - b) + 2 (s F + K)) + s; q, s+ = split(N, 2 D_out), D_out = W(a) + W(a+), n = q 2D + s with |s| <= D and the edge |s| = D taken at an even q; a+ = a + q; b+ = a; q_d, r_d+ = carry(J, T_d, r_d); K = s T_k q_d; q_c, k+ = carry(tau, key, k); the mirror is (b, a, -s), and the run back is the tick on the mirrored state, mirrored.
Board: one pass at every Node-clock alike, reading only its own gears and its six Meshes at the now slot; W is the rest plus the metric family's 00 slot here, the 00 row's own teeth at rest, so W(a+) is the 00 row's own carry, given first; the 2 is the two senses of an axis, read from the star; the click pushes nothing into a, b, s or r_d.
Clicks: a whole click is the click tooth's quotient, one quantum taken (+1) or given back (-1), left for the record from G5; a deeper 00 slot is a slower clock, read in the clicks as proper time, and the momentum W (a - b), not the velocity, is what a clock keeps as its teeth move.
"""

import numpy as np

from tensor24.algebra.carry import Z, carry, flip, lit
from tensor24.engine.contract import contract, read
from tensor24.engine.mesh import held, pull, seen
from tensor24.engine.state import Click, Gearing, Layout, Read, State


def split(n: Z, d: Z, senses: Z) -> tuple[Z, Z]:
    """The centred split of n at the edge's dial, both slots' teeth D in half-teeth: n = q (senses D) + s with the tooth s within [-D, D], counted from the dial's middle, and where s lands on the dial's edge the count q is taken even; two carries and the zero test, no if."""
    dial = senses * d
    q, r = carry(n + d, dial, 0)
    _, odd = carry(q, senses, 0)
    moved = (1 - lit(r)) * odd
    return q - moved, r - d + moved * dial


def gear(a: Z, b: Z, s: Z, d_in: Z, d_out: Z, push: Z, senses: Z) -> tuple[Z, Z, Z]:
    """A gear's tick on the edge: its momentum N = 2 (D_in (a - b) + 2 push) + s, carried from the edge it was kept on to the next edge and split at its dial 2 D_out, (q, s+); a+ = a + q, b+ = a."""
    n = senses * (d_in * (a - b) + senses * push) + s
    q, kept = split(n, d_out, senses)
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


# The tooth lives on the edge between the two slots and is read on the edge it was kept on, so a change of the teeth
# moves no tooth: a round runs back exactly wherever both slots' teeth are at least 1, the clock rising or falling,
# and d_t (W d_t a) = F holds with W on the edge, the momentum kept and the velocity re-split as the teeth move.
def weight(gearing: Gearing, clock: Read, a: Z) -> Z:
    """Every gear's teeth W = W+: its rest and what the clocks' read lands on it at the now slot, by no table and with no bound on the read."""
    rest, _, _, _ = gearing
    return rest + read(clock, a)


def halves(layout: Layout) -> Z:
    """The two halves of a tooth, the edge's half-teeth: the senses of an axis, its + and its -, read from the star."""
    _, spokes, _, _, _, _, _, _, _ = layout
    senses, _ = carry(spokes.shape[0], spokes.shape[1], 0)
    return senses


def dials(layout: Layout, s: State) -> tuple[Z, Z]:
    """Every gear's teeth at the state's two slots, W(a) and W(b), as its round reads them: the edge's dial is their sum, the promise's measure, read from outside."""
    _, _, _, _, gearing, _, clock, _, _ = layout
    a, b, _, _, _ = s
    return weight(gearing, clock, a), weight(gearing, clock, b)


def grips(layout: Layout, s: State) -> Z:
    """Every Spoke's grip at every gear and site at the state's now slot, as its round reads them: the window's measure, read from outside."""
    a, _, _, _, _ = s
    return held(layout, a)


def act(layout: Layout, s: State) -> tuple[State, Z]:
    """One round and its clicks, in one pass: every gear carries its momentum from the edge it reads to the next edge, whose dial reads the 00 slot's next count, the 00 row's own carry at its standing teeth, through the clocks' read; every train's click tooth carries the area the kick moves into the train at the key; the clicks are that carry's quotients, (the state reached, the clicks)."""
    _, _, _, _, gearing, _, clock, _, click = layout
    a, b, tooth, rd, k = s
    force, j = sources(layout, a)
    _, _, _, teeth = gearing
    _, _, _, _, key = click
    q, kept = drive(j, teeth, rd)
    kicks = kick(gearing, q)
    senses, push = halves(layout), driven(gearing, force, kicks)
    wa, wb = dials(layout, s)
    # the count the split gives at the edge's own dial: the 00 row's, whose teeth read no row, so its dial is its own
    first, _, _ = gear(a, b, tooth, wa + wb, wa + wb, push, senses)
    a1, b1, s1 = gear(a, b, tooth, wa + wb, wa + weight(gearing, clock, first), push, senses)
    clicks, k1 = carry(area(click, a, kicks, k), key, k)
    return State(a1, b1, s1, kept, k1), clicks


def tick(layout: Layout, s: State) -> State:
    """One round: the state the act reaches, its clicks left for the record."""
    moved, _ = act(layout, s)
    return moved


def mirror(layout: Layout, s: State) -> State:
    """The state mirrored, time's reversal: the slots swapped and the edge's tooth negated, read in no teeth, the drive's tooth flipped in its teeth and the click tooth in its key; its own inverse on any clock, standing or moving."""
    _, _, _, _, gearing, _, _, _, click = layout
    a, b, tooth, rd, k = s
    _, _, _, teeth = gearing
    _, _, _, _, key = click
    return State(b, a, -tooth, flip(rd, teeth), flip(k, key))


def untick(layout: Layout, s: State) -> State:
    """The round run back, the tick on the mirrored state mirrored: tick's inverse wherever both slots' teeth are at least 1 and every tooth stands within its edge's dial, the clock standing or moving; n rounds run back by n unticks, or by one mirror about n ticks, the two alike since the mirror is its own inverse."""
    return mirror(layout, tick(layout, mirror(layout, s)))
