"""Clock: what a Node-clock holds: each gear's count now and before, the tooth of the edge between them, its drive's fine tooth, and each train's click tooth.
Algebra: whole-number arrays a, b, r, r_d and k, and the layout's coefficients and plans, read once at load.
Board: the state of every Node-clock at one round, and the layout every round reads: the neighbours, the Meshes, the grips, J's plan, the clocks' read and the click's cross with its key.
Clicks: n/a: these hold the board, not its shadow.
"""

from typing import NamedTuple

from tensor24.algebra.carry import Z


class State(NamedTuple):
    """Per gear its now and before slots, the tooth of the edge between them and its drive's fine tooth; per train its click tooth."""

    a: Z
    b: Z
    r: Z  # the tooth of the edge between the two slots, within [-D, D], D = W(b) + W(a): what the momentum's split leaves
    rd: Z  # the drive's fine tooth, within [0, T_d): the remainder its carry keeps, as r is the gear's
    k: Z  # (trains, sites): the click tooth, within [0, key): the remainder the train's click keeps, born at (key - 1) div 2


class Plan(NamedTuple):
    """J's terms over the kinds' tables, laid at load: per term its three readings, the unit where it reads fewer, its whole factor, its target; none until the coupling family's one plan (G3)."""

    first: Z  # (terms,): the row of the readings that enters first
    second: Z  # (terms,): the row that enters second
    third: Z  # (terms,): the row that enters third: the unit, the readings' last row, where a term reads two or fewer
    factor: (
        Z  # (terms,): the strength times the table's entry, Python integers, so that no product wraps
    )
    target: Z  # (terms,): the gear's row where the term lands


class Read(NamedTuple):
    """A linear read of the gears' now counts: per term the row read, its whole factor, the row or Spoke it lands on."""

    first: Z  # (terms,): the row read
    factor: Z  # (terms,): its whole factor
    target: Z  # (terms,): the gear's row whose teeth it lands in (the clock's), or the Spoke whose grip (the grips')


class Click(NamedTuple):
    """The whole click's cross, laid at load: per term the row whose now count enters, the row whose kick it crosses, the A1 table's entry signed by the way round, the train the area moves into; and every train's key, CHOSEN in the universe file."""

    first: Z  # (terms,): the row read at the now slot
    second: Z  # (terms,): the row whose kick the term crosses it with
    factor: Z  # (terms,): the table's entry, + the one way round and - the other, Python integers
    target: Z  # (terms,): the train whose area the term moves
    key: Z  # (trains, 1): the key each train's click tooth carries at, at least 1


class Gearing(NamedTuple):
    """Every gear's coefficients, per gear row or per Node-clock: 1 for a divisor and 0 for a term where a train has none."""

    rest: Z  # the teeth at rest: a gear's W = W+ is its rest and its clock's count at the now slot
    stretch: Z  # s, the impulse's factor on the force and the kick
    kick: Z  # T_k, the kick's teeth: 1 on the force's path
    drive: Z  # T_d, the drive's teeth, at least 1: 1 on the force's path, where the drive's fine tooth stays 0


class Layout(NamedTuple):
    """The board read once: the neighbours, the Spokes' directions, each Spoke's Mesh, the grips, the gearing, J's plan, the clocks and the grips' read, and the click's cross."""

    nb: Z  # (6, N): +x, -x, +y, -y, +z, -z, each the other's opposite (the load makes the relation symmetric)
    spokes: Z  # (6, d): each Spoke's direction on the board's axes, a unit vector or its opposite, in nb's order
    meshes: Z  # (6, N): the Mesh each Spoke holds, its two ends paired by the load (load.geometry); a grip its own conjugate
    grip: Z  # (rows or 1, Meshes): a gear row's grip on each Mesh, once per Mesh; a train's rows alike from 7b's load
    gearing: Gearing
    plan: Plan  # J's terms on the readings: the value, the centred difference along each axis, the force, the unit last
    clock: Read  # every gear's teeth: its rest and what this read lands on its row, the tick's weight
    stretch: Read  # every Spoke's grip: its rest and what this read lands on the Spoke, a row read at both ends of its Mesh
    click: Click  # every train's swept area as the cross of its parts with the kick through the A1 table, and its key
