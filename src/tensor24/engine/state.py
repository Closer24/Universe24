"""Clock: what a Node-clock holds: each gear's count now and before, the tooth of the edge between them, its drive's fine tooth, and the click tooth of every side of an edge between two trains.
Algebra: whole-number arrays a, b, r, r_d and k, and the layout's coefficients and plans, read once at load.
Board: the state of every Node-clock at one round, and the layout every round reads: the neighbours, the Meshes, the grips, J's plan on the value legs, the clocks' plan, term 11 on the edges with the edge key, the metric's push, term 5's plan on the stretches and the momenta, and the plan's terms with a Mesh leg, the gradient vertex, each laid by the loader.
Clicks: n/a: these hold the board, not its shadow.
"""

from typing import NamedTuple

from tensor24.algebra.carry import Z


class State(NamedTuple):
    """Per gear its now and before slots, the tooth of the edge between them and its drive's fine tooth; per side of every edge between two trains its click tooth."""

    a: Z
    b: Z
    r: Z  # the tooth of the edge between the two slots, within [-D, D), D = W(b) + W(a): what the momentum's split leaves
    rd: Z  # the drive's fine tooth, within [0, T_d): the remainder its carry keeps, as r is the gear's
    k: Z  # ((1 + Spokes) x trains x trains, sites): every edge side's click tooth at every reach, within [0, key), born at (key - 1) div 2


class Plan(NamedTuple):
    """J's terms over the kinds' tables, laid at load: per term the rows of the readings it multiplies, any number of them, the unit where it reads fewer, its whole factor, its target; the loader lays three: the plan on the value legs (term 9's notch, term 6's held spring and its tie, the hands' tie), the metric's push (term 5) and the Mesh plan (term 6's gradient vertex), a train that lacks a term taking it at the factor 0."""

    legs: Z  # (readings, terms): each term's rows of the readings, one row of legs per reading it multiplies; the unit, the readings' last row, where a term reads fewer
    factor: (
        Z  # (terms,): the strength times the table's entry, Python integers, so that no product wraps
    )
    target: Z  # (terms,): the gear's row where the term lands


class Read(NamedTuple):
    """The grips' linear read, the stretch's (mesh.gripped gathers it; the clocks read a Plan since ONELAW3's widened step): per term the row read, its whole factor, the Spoke it lands on."""

    first: Z  # (terms,): the row read
    factor: Z  # (terms,): its whole factor
    target: Z  # (terms,): the gear's row whose teeth it lands in (the clock's), or the Spoke whose grip (the grips')


class Click(NamedTuple):
    """Term 11 on the edges, laid at load (runner/plans.py's edging and crossing): per term of J's plan on the value legs, in the plan's order, its weight on every train, 0 on a train its monomial has no value leg in, and the train of the leg it pushes; every edge side's key at every reach, its own Node-clock and across each Spoke, the edge key: the universe file's CHOSEN key times kappa / two, the same for every side; and the Mesh's edges, term 6's gradient vertex split by the Spoke it reads across, per pair of rows their coupling and the side it books on."""

    weight: Z  # (terms, trains): the leg's share of its monomial's flow, kappa (L - l) / L, onto each other train of the monomial
    train: Z  # (terms,): the train of the leg the term pushes, the side's first train
    # ((1 + Spokes) x trains x trains, 1): the key each side (t, u) at each reach carries its passing at, odd
    key: Z
    across: Z  # (Spokes, rows, rows): the Mesh edge's coupling of row r here with row p across the Spoke, times kappa / two
    onto: Z  # (Spokes, rows, rows): the side (Spoke trains + t) trains + u that the pair books on, t r's train, u p's


class Gearing(NamedTuple):
    """Every gear's coefficients, per gear row or per Node-clock: 1 for a divisor and 0 for a term where a train has none."""

    rest: Z  # the teeth at rest: a gear's W = W+ is its rest and its clock's count at the now slot
    stretch: Z  # s, the impulse's factor on the force and the kick
    kick: Z  # T_k, the kick's teeth: 1 on the force's path
    drive: Z  # T_d, the drive's teeth, at least 1: 1 on the force's path, where the drive's fine tooth stays 0
    parity: Z = 1  # the row's parity under time's reversal: 1 for an even row, a count the reversal pivots on, 0 for an odd one, the metric's 0i slots, whose index pair holds one time index


class Layout(NamedTuple):
    """The board read once: the neighbours, the Spokes' directions, each Spoke's Mesh, the grips, the gearing, J's plan on the value legs, the clocks and the grips' read, the click's passing, the metric's push, and the plan's terms with a Mesh leg."""

    nb: Z  # (6, N): +x, -x, +y, -y, +z, -z, each the other's opposite (the load makes the relation symmetric)
    spokes: Z  # (6, d): each Spoke's direction on the board's axes, a unit vector or its opposite, in nb's order
    meshes: Z  # (6, N): the Mesh each Spoke holds, its two ends paired by the load (load.geometry); a grip its own conjugate
    grip: Z  # (rows or 1, Meshes): a gear row's grip on each Mesh, once per Mesh; a train's rows alike from 7b's load
    gearing: Gearing
    plan: Plan  # J's terms on the readings: the value, the centred difference along each axis, the force, the unit last
    clock: Plan  # every gear's teeth: its rest and what this plan lands on its row from the counts given first, the tick's weight
    stretch: Read  # every Spoke's grip: its rest and what this read lands on the Spoke, a row read at both ends of its Mesh
    click: Click  # term 11 on the edges: each term of J's plan weighed onto the other trains of its monomial, the Mesh's edges, the edge key
    push: Plan  # term 5, the metric's push in the books' form, every slot pushed by -dH / d slot of the act's energy H = W v_in v_out / 2 + SUM_Mesh grip Delta^2 / 2 with W = rest + k0 c00: terms on the push's readings (the six stretches per row, the momenta in and out, the unit last), k0 sigma_in sigma_out of every row on the force's path (the sourcing trains' rows and the square's 0i and jk rows) onto the 00 slot, every row's two Meshes' stretches squared at -1 onto the ii slot of their axis, nothing onto the jk and 0i slots, no strength; the drive's dial senses on the square's 00 and ii rows takes the half
    mesh: Plan  # the plan's terms with a Mesh leg, term 6's gradient vertex V = mesh x SUM_i C_ji M_j D_i L between an A1 row L of the board's wave (a train neither the square nor the held hand) and a tied hand's rows M, on the same readings as the plan, laid by the loader as its two pushes (L's difference onto M's row, M's difference onto L's row; the factor 0 at mesh 0 or where no channel stands), and the drive reads them, the passing too, split by the Spoke on the Mesh's edges
