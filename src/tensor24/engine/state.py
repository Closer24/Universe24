"""The engine's records: the Node-clocks' state, the layout read once at load, J's plan, and what a round puts out."""

from typing import NamedTuple

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
    factor: Z  # (terms,): the strength times the table's entry
    target: Z  # (terms,): the gear's row where the term lands


class Gearing(NamedTuple):
    """Every gear's coefficients, per gear row or per Node-clock: 1 for a divisor and 0 for a term where a train has none."""

    w: Z  # W, the teeth the impulse reads the stride at
    wp: Z  # W+, the teeth of the gear's carry
    stretch: Z  # s, the impulse's factor on the force and the kick: 1 on a gear's own teeth
    spring: Z  # D
    kick: Z  # T_k, the kick's teeth: 1 on the force's path
    drive: Z  # T_d, the drive's teeth, at least 1: 1 on the force's path, where the drive's fine tooth stays 0


class Layout(NamedTuple):
    """The board read once: the neighbours, each Spoke's Mesh, the grips, the gearing, J's plan, the rates, the full rate."""

    nb: Z  # (6, N): +x, -x, +y, -y, +z, -z, each the other's opposite (the load makes the relation symmetric)
    meshes: Z  # (6, N): the Mesh each Spoke holds, its two ends paired by runner/board.py; a grip its own conjugate
    grip: Z  # (rows or 1, Meshes): a train's grip on each Mesh, once per Mesh
    gearing: Gearing
    plan: Plan  # J's terms on the readings: the value, the centred difference along each axis, and the force
    rate: Z  # from 0 to the full rate, so the beat's k is a bit (the load's promises name one past it, from stage 7)
    gamma: Z


class Out(NamedTuple):
    """What a round puts out: where it fired, where it ticked, and the now slot's time before the round."""

    fire: Z
    k: Z
    tn: Z
