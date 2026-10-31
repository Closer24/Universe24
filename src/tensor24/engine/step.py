"""Clock: every round every gear moves once: its neighbours pull it, the coupling pushes it, and its momentum, the velocity's whole count with the tooth kept on the edge between its two slots, is carried to the next edge and split there in one dial of both slots' teeth; the drive carries the coupling's push the same way, the metric's slots taking what the rows that read them give up (term 5, the books' form), and every edge side's click tooth carries the passing of the round's window between its two trains, the before, the now and the next: each term of J's work over the window, booked on the edge as a pair flow (David's split), its given on one side and its taken on the other; the passing is a record: it reads the gears and moves none.
Algebra: D_in = W(b) + W(a); N = 2 (D_in (a - b) + 2 (s F + K)) + s; q, s+ = split(N, 2 D_out), D_out = W(a) + W(a+), n = q 2D + s with -D <= s < D by one carry from the dial's half; a+ = a + q; b+ = a; J = J1 + J5, J1 the plan and the Mesh plan on the now slot's readings and J5 the metric's push on the six stretches per row, the momenta M_in = 2 D_in (a - b) + s and M_out = M_in + 4 (s F + K1) read in whole turns of the rest dial, and the unit, every slot pushed by -dH / d slot, H = W v_in v_out / 2 + SUM_Mesh grip Delta^2 / 2 with W = rest + k0 c00 and grip = grip_rest + ii at both ends: the 00 slot by k0 SUM sigma_in sigma_out over the rows on the force's path and each ii slot by -SUM over the rows of its two Meshes' stretches squared, the plan's factors k0 and -1, the half in -dH / d slot taken once, by the drive's dial T_d = 2 on those rows with the remainder kept in r_d, and the jk and 0i slots by nothing; q_d, r_d+ = carry(J, T_d, r_d); K = s T_k q_d; W_i = J_i(a) (a+ - b) for every term i of J's plan on the value legs, J_i(a) its push at the now slot, minus its factor times its other legs, on its leg's count from the before slot to the next; P(t, u) = SUM_i ([leg i in t] - [leg i in u]) w_i W_i over the monomials with value legs in both trains, w_i the leg's weight kappa (L - l) / L, so P(u, t) = -P(t, u); q_c, k+ = carry(P, key, k) on every side at the edge key; the mirror is (b, a, -1 - s) on an even row, the law's (iii) on the dial 2D, and (-b, -a, s) on an odd one, every click tooth kept, and the run back is the tick on the mirrored state, mirrored, where the push reads the momenta of no row it lands on (hypothesis (d)).
Board: one pass at every Node-clock alike, reading only its own gears and its six Meshes at the now slot, and for the passing its own counts at the before slot and the next and, on the Mesh's edges, its partner's across one Mesh at the before slot, the now slot and the next; W is the rest plus the clocks' plan on this Node-clock's own counts, monomials of any number of legs (today the metric family's 00 slot alone, k0 c00 with k0 = Spokes x senses as the loader lays it), every row the plan reads standing at its rest teeth, so W(a+) reads those rows' own carries, given first (the widened step: ONELAW3 3.4's seven gears for det(gt) L^4, ten with the cross terms, against today's one 00 row); the 2 is the two senses of an axis, read from the star; the drive's teeth T_d are senses on the square's 00 and ii rows, where the push lands, and 1 on the force's path, as the loader lays them; the click pushes nothing into a, b, s or r_d; the passing reads J's terms at the now slot and each leg's count at the before slot and at the count the round produces, no push kept from a round to the next; it reads the value legs' plan at a Node-clock and the Mesh plan split by the Spoke across the Meshes, so the Mesh flux is counted by the Mesh edges' clicks, while the metric's push J5 enters no side's passing: the sourcing trains' exchange with the metric is booked by no click (open).
Clicks: a click is a click tooth's quotient, a whole number of quanta, taken where above 0 and given where below 0, left for the record (its size the key's, which the owner's batch holds); an edge's two sides carry P and -P at one key from teeth born summing to key - 1, so their quotients sum to 0 at every place by the carry's law, and a train's click is the sum of its sides'; the Mesh's edges, term 6's gradient vertex split by the Spoke it reads across, carry term 11's own form on the edge, c (x_r y_p - y_r x_p) over the window, its two ends one coupling, at the same key; the passing is odd under the window's reversal, so the mirror keeps the tooth and the run back is the same act on the mirrored state, its quotients negated (COUNT5, item M1); a deeper 00 slot is a slower clock, read in the clicks as proper time: the sourcing trains' momenta deepen it and their stretches slacken the grips about it, their books and the metric's closed with no strength (gravity; gamma owed to the click world, the board's wave read at the clocks' read factor k0 = Spokes x senses, the loader's frame), and the momentum W (a - b), not the velocity, is what a clock keeps as its teeth move.
"""

import numpy as np

from tensor24.algebra.carry import Z, carry, flip
from tensor24.engine.contract import contract
from tensor24.engine.mesh import held, pull, seen, stretches
from tensor24.engine.state import Click, Gearing, Layout, Plan, State


def split(n: Z, d: Z, senses: Z) -> tuple[Z, Z]:
    """The split of n at the edge's dial, both slots' teeth D in half-teeth, from the dial's half: n = q (senses D) + s with the tooth s within [-D, D), one carry of Rule3 and nothing else (the half-open convention, the owner's decision of 17:0x UTC)."""
    q, r = carry(n + d, senses * d, 0)
    return q, r - d


def gear(a: Z, b: Z, s: Z, d_in: Z, d_out: Z, push: Z, senses: Z) -> tuple[Z, Z, Z]:
    """A gear's tick on the edge: its momentum N = 2 (D_in (a - b) + 2 push) + s, carried from the edge it was kept on to the next edge and split at its dial 2 D_out, (q, s+); a+ = a + q, b+ = a."""
    n = senses * (d_in * (a - b) + senses * push) + s
    q, kept = split(n, d_out, senses)
    return a + q, a, kept


def drive(j: Z, teeth: Z, rd: Z) -> tuple[Z, Z]:
    """The drive: (q, r_d+), the carry of the source J at the drive's teeth T_d; on the force's path, T_d = 1, q is J."""
    return carry(j, teeth, rd)


def readings(layout: Layout, a: Z) -> tuple[Z, Z]:
    """Every gear's force, its pull, and the readings flat: the value, the differences along each axis, the force, and the unit last."""
    nb, spokes, _, _, _, _, _, _, _, _, _ = layout
    force = pull(layout, a)
    # each axis's + neighbour less its - neighbour: the neighbours summed with their Spokes' directions
    gradient = np.tensordot(spokes, seen(a, nb), axes=(0, 1))
    read = np.concatenate((np.expand_dims(a, 0), gradient, np.expand_dims(force, 0)))
    # the unit, the readings' last row, for each reading a term lacks of three
    return force, np.concatenate((read.reshape(-1, a.shape[-1]), np.ones_like(a[:1], dtype=object)))


def sources(layout: Layout, a: Z) -> tuple[Z, Z]:
    """Every gear's force, its pull, and its source J1: the plan on the readings at the now slot, and the plan's terms with a Mesh leg on the same readings (the gradient vertex), which the drive carries and the passing reads split by the Spoke, on the Mesh's edges."""
    _, _, _, _, _, plan, _, _, _, _, mesh = layout
    force, flat = readings(layout, a)
    return force, contract(plan, flat, a) + contract(mesh, flat, a)


def stress(layout: Layout, s: State, push: Z) -> Z:
    """The metric's push J5 (term 5, the books' form): the push's plan on the Node-clock's six stretches per row (Spoke s, row r at the plane s rows + r, the Spokes in the star's order), the two momenta in whole turns of the rest dial, M_in = 2 D_in (a - b) + s at the plane Spokes rows + r and M_out = M_in + 4 push at (Spokes + 1) rows + r, each read by the centred split, and the unit last at (Spokes + 2) rows; so a hand at rest gives the 00 slot nothing, its stretches alone pushing the ii slots. M_out is read at the first push, s F + K1 with K1 the drive's quotient on J1 alone: the round's own momentum out on a row J5 does not land on, and a stride the round does not take on a row it does; so the mirror swaps and negates the momenta a plan reads, and the round runs back, only where the plan reads the momenta of no row the push lands on (hypothesis (d), which the loader's plan keeps by reading the rows on the force's path alone); a plan reading a pushed row's momenta breaks the run back."""
    _, _, _, _, gearing, _, _, _, _, plan, _ = layout
    rest, _, _, _, _ = gearing
    a, b, tooth, _, _ = s
    senses = halves(layout)
    wa, wb = dials(layout, s)
    m_in = senses * (wa + wb) * (a - b) + tooth
    m_out = m_in + senses * senses * push
    sigma_in, _ = split(m_in, senses * rest, senses)
    sigma_out, _ = split(m_out, senses * rest, senses)
    planes = stretches(layout, a).swapaxes(0, 1).reshape(-1, a.shape[-1])
    unit = np.ones_like(a[:1], dtype=object)
    return contract(plan, np.concatenate((planes, sigma_in, sigma_out, unit)), a)


def kick(gearing: Gearing, q: Z) -> Z:
    """The kick on every gear, K = T_k s q_d: the drive's whole turns at the kick's teeth, stretched."""
    _, stretch, teeth, _, _ = gearing
    return stretch * teeth * q


def driven(gearing: Gearing, force: Z, kicks: Z) -> Z:
    """The push on every gear, s F + K: the force stretched, and the kick the gear takes."""
    _, stretch, _, _, _ = gearing
    return stretch * force + kicks


def valued(x: Z) -> Z:
    """The readings of the value legs alone: a Node-clock's own counts with the unit last, so a plan whose legs are value rows or the unit reads on it what it reads on the act's readings, and nothing across a Mesh."""
    return np.concatenate((x, np.ones_like(x[:1], dtype=object)))


def passing(click: Click, plan: Plan, b: Z, a: Z, a1: Z) -> Z:
    """Every edge side's passing (t, u) in the click teeth's shape, at t trains + u: the work of each term of J's plan on the value legs over the round's window, W_i = J_i(a) (a+ - b), its push at the now slot on its leg's move from the before slot to the next (David's split in the work form), weighed onto each other train of its monomial and summed into its leg's train, the side (t, u) passing the weighed work on t's legs less that on u's, a take where it is above 0, so P(u, t) = -P(t, u), the diagonal 0; a gather of each term's readings, a product, a scattered sum. The passing is a record: it reads the gears and moves none, so every count, promise and runaway is the board's whatever it passes; the window reversed, (a+, a, b) on the mirrored counts, negates every W_i, so P is odd under the mirror."""
    legs, factor, target = plan
    weight, train, _, _, _ = click
    va, vb, va1 = valued(a), valued(b), valued(a1)
    first = factor[None, :, None] + 0 * va[-1:, None]  # the factor at every site, before the legs
    work = np.prod(np.concatenate((first, va[legs])), axis=0) * (va1[target] - vb[target])
    trains = weight.shape[-1]
    given = np.zeros((trains, trains, a.shape[-1]), dtype=object)
    np.add.at(given, train, weight[:, :, None] * work[:, None, :])
    return (given - given.swapaxes(0, 1)).reshape(trains * trains, a.shape[-1])


def crossing(click: Click, nb: Z, b: Z, a: Z, a1: Z) -> Z:
    """Every Mesh edge side's passing, the side (t, u) across each Spoke, at (Spoke trains + t) trains + u: term 11's own form on the edge, P(x, y) = c (x_r y_p - y_r x_p) and S = P(a, b) + P(a+, a) = c (a_p (a+_r - b_r) - a_r (a+_p - b_p)), r a row here, p a row at the Node-clock across the Spoke and c the edge's coupling (runner/plans.py's crossing), summed into the side of r's train and p's; the far end reads the same coupling across the opposite Spoke and passes the negative, exactly; a gather across the Spokes as the pull reads the neighbours, a product, a scattered sum. A record as the passing is: it reads the gears and moves none, its partner's counts at the before slot, the now slot and the next, across one Mesh."""
    weight, _, _, across, onto = click
    trains, moved = weight.shape[-1], a1 - b
    far, gone = seen(a, nb).swapaxes(0, 1), seen(moved, nb).swapaxes(0, 1)  # each row across each Spoke
    ends = across[..., None] * (moved[None, :, None] * far[:, None] - a[None, :, None] * gone[:, None])
    sides = np.zeros((across.shape[0] * trains * trains, a.shape[-1]), dtype=object)
    np.add.at(sides, np.broadcast_to(onto, ends.shape[:-1]), ends)
    return sides


# The tooth lives on the edge between the two slots and is read on the edge it was kept on, so a change of the teeth
# moves no tooth: a round runs back exactly wherever both slots' teeth are at least 1, the clock rising or falling,
# and d_t (W d_t a) = F holds with W on the edge, the momentum kept and the velocity re-split as the teeth move.
def weight(gearing: Gearing, clock: Plan, a: Z) -> Z:
    """Every gear's teeth W = W+: its rest and what the clocks' plan lands on it from the counts a, monomials of any number of legs on the value legs (the 3+1 split's dial det(gt) L^4 among them, ONELAW3 3.2: OPEN until the flat and the units are ruled, so the loader lays today's one-leg read), by no table and with no bound on the read."""
    rest, _, _, _, _ = gearing
    return rest + contract(clock, valued(a), a)


def halves(layout: Layout) -> Z:
    """The two halves of a tooth, the edge's half-teeth: the senses of an axis, its + and its -, read from the star."""
    _, spokes, _, _, _, _, _, _, _, _, _ = layout
    senses, _ = carry(spokes.shape[0], spokes.shape[1], 0)
    return senses


def dials(layout: Layout, s: State) -> tuple[Z, Z]:
    """Every gear's teeth at the state's two slots, W(a) and W(b), as its round reads them: the edge's dial is their sum, the promise's measure, read from outside."""
    _, _, _, _, gearing, _, clock, _, _, _, _ = layout
    a, b, _, _, _ = s
    return weight(gearing, clock, a), weight(gearing, clock, b)


def grips(layout: Layout, s: State) -> Z:
    """Every Spoke's grip at every gear and site at the state's now slot, as its round reads them: the window's measure, read from outside."""
    a, _, _, _, _ = s
    return held(layout, a)


def act(layout: Layout, s: State) -> tuple[State, Z]:
    """One round and its clicks, in one pass: the sources J1 at the now slot (the plan and the Mesh plan on the readings) give every gear its first push, whose momenta, with the six stretches per row, source the metric's push J5; the drive carries J = J1 + J5; every gear carries its momentum from the edge it reads to the next edge, whose dial reads the 00 slot's next count, the 00 row's own carry at its standing teeth, through the clocks' read; every edge side's click tooth carries its passing of the round's window at the edge key, P(t, u) = SUM_i ([leg i in t] - [leg i in u]) w_i J_i(a) (a+ - b) over the terms of J's plan on the value legs, read at the before slot, the now slot and the next count alike (on the Mesh's edges the partner's across one Mesh too; no push kept from a round to the next); the clicks are that carry's quotients, one per side, (the state reached, the clicks)."""
    nb, _, _, _, gearing, plan, clock, _, click, _, _ = layout
    a, b, tooth, rd, k = s
    force, j1 = sources(layout, a)
    _, _, _, teeth, _ = gearing
    _, _, key, _, _ = click
    first, _ = drive(j1, teeth, rd)
    j = j1 + stress(layout, s, driven(gearing, force, kick(gearing, first)))
    q, kept = drive(j, teeth, rd)
    kicks = kick(gearing, q)
    senses, push = halves(layout), driven(gearing, force, kicks)
    wa, wb = dials(layout, s)
    # the counts the split gives at the edge's own dial, given first: the rows the clocks' plan reads stand at their
    # rest teeth, so each one's is its own next count, and W(a+) reads them (a one-pass D_out = 2 W(a) would break the
    # edge's dial the run back shares)
    first, _, _ = gear(a, b, tooth, wa + wb, wa + wb, push, senses)
    a1, b1, s1 = gear(a, b, tooth, wa + wb, wa + weight(gearing, clock, first), push, senses)
    # every edge side's passing of the window (b, a, a+), at its own Node-clock and across each Spoke, at the edge key
    passed = np.concatenate((passing(click, plan, b, a, a1), crossing(click, nb, b, a, a1)))
    clicks, k1 = carry(passed, key, k)
    return State(a1, b1, s1, kept, k1), clicks


def tick(layout: Layout, s: State) -> State:
    """One round: the state the act reaches, its clicks left for the record."""
    moved, _ = act(layout, s)
    return moved


def mirror(layout: Layout, s: State) -> State:
    """The state mirrored, time's reversal: on an even row the slots swapped, the edge's tooth flipped on its dial, s -> -1 - s (the law's (iii), read in no teeth), and the drive's fine tooth flipped in its teeth; on an odd row the counts negated and swapped and both teeth kept, as the source the drive carries is negated there (the carry's sign law: n + r = q T + r' and -n + r' = -q T + r); every side's click tooth kept, as the passing it carries is negated under the window's reversal, by the same sign law; its own inverse on any clock, standing or moving."""
    _, _, _, _, gearing, _, _, _, _, _, _ = layout
    a, b, tooth, rd, k = s
    _, _, _, teeth, even = gearing
    tau = halves(layout) * even - 1
    return State(
        tau * b,
        tau * a,
        tooth - even * (halves(layout) * tooth + 1),
        rd + even * (flip(rd, teeth) - rd),
        k,
    )


def untick(layout: Layout, s: State) -> State:
    """The round run back, the tick on the mirrored state mirrored: tick's inverse wherever both slots' teeth are at least 1 and every tooth stands within its edge's dial, the clock standing or moving, and the push's plan reads the momenta of no row the push lands on (hypothesis (d), stress); n rounds run back by n unticks, or by one mirror about n ticks, the two alike since the mirror is its own inverse."""
    return mirror(layout, tick(layout, mirror(layout, s)))
