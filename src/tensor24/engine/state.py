"""The engine's records: the Node-clocks' state, the layout read once at load, J's plan, and what a round puts out."""

from typing import NamedTuple

import numpy as np

from tensor24.algebra.carry import Z


class State(NamedTuple):
    """Per gear its now and before slots, fine tooth, going and drive's fine tooth; per Node-clock its dial, count and time."""

    a: Z
    b: Z
    r: Z
    go: Z
    rd: Z  # the drive's fine tooth, within [0, T_d): the remainder its carry keeps, as r is the gear's
    ph: Z
    c: Z
    tn: Z


class Plan(NamedTuple):
    """The coupling rows expanded at load over the kinds' tables: per term its two readings, its whole factor, its target."""

    first: Z  # (terms,): the row of the readings that enters first
    second: Z  # (terms,): the row that enters second
    factor: (
        Z  # (terms,): the strength times the table's entry, Python integers, so that no product wraps
    )
    target: Z  # (terms,): the gear's row where the term lands


class Gearing(NamedTuple):
    """Every gear's coefficients, per gear row or per Node-clock: 1 for a divisor and 0 for a term where a train has none."""

    w: Z  # W, the teeth the impulse reads the stride at
    wp: Z  # W+, the teeth of the gear's carry
    stretch: Z  # s, the impulse's factor on the force and the kick: 1 on a gear's own teeth
    spring: Z  # D
    kick: Z  # T_k, the kick's teeth: 1 on the force's path
    drive: Z  # T_d, the drive's teeth, at least 1: 1 on the force's path, where the drive's fine tooth stays 0


class Ruler(NamedTuple):
    """The clock's ruler, the rate line walked once at load and read at the time gear's own counts (David's table, #2187 6488192915): a reading row's W is Z_b + Z_n, its W+ Z_n + Z_+, its spring its factor times Y_n^2."""

    row: Z  # the time gear's row, laid by the load at every Node-clock
    last: Z  # the table's last count, the clock's last rate: a count past it reads there, a count below 0 reads at 0
    teeth: Z  # (counts,): Z(c) = T Y(c)^4 div Gamma^4, so Z(0) = T
    square: Z  # (counts,): Y(c)^2, by which a reading row's spring factor is its spring
    reads: Z  # (rows, 1): 1 on a row that reads the ruler; 0 on the time gear's, and on every row of a layout as laid
    spring: Z  # (rows, 1): a reading row's spring factor, 12 (rim - pinion) G^2


LAID = Ruler(
    0, 0, np.zeros(1, dtype=object), np.zeros(1, dtype=object), 0, 0
)  # read by no row: the gearing as laid


class Layout(NamedTuple):
    """The board read once: the neighbours, each Spoke's Mesh, the grips, the gearing, J's plan, the rates, the full rate."""

    nb: Z  # (6, N): +x, -x, +y, -y, +z, -z, each the other's opposite (the load makes the relation symmetric)
    meshes: Z  # (6, N): the Mesh each Spoke holds, its two ends paired by runner/board.py; a grip its own conjugate
    grip: Z  # (rows or 1, Meshes): a gear row's grip on each Mesh, once per Mesh; a train's rows alike from 7b's load
    gearing: Gearing
    plan: Plan  # J's terms on the readings: the value, the centred difference along each axis, and the force
    rate: Z  # from 0 to the full rate, so the beat's k is a bit (the load's promises name one past it, from stage 7b)
    gamma: Z
    ruler: Ruler = LAID  # the time gear's ruler, from stage 7b's load; a layout as laid reads none


class Out(NamedTuple):
    """What a round puts out: where it fired, where it ticked, and the now slot's time before the round."""

    fire: Z
    k: Z
    tn: Z
