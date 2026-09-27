"""The spin's step: S_next = S_before + (span [(Omega x S_now) + mu x B_q] + carry) div (W Gamma), the leapfrog over the row's span, Omega from a read whose dipole is the spin ((c_num x factor x curl V + (t_num ((grad c) x n)) div W) div (span x den), the two weights the read family's row spins_step, the span the bodies' family's spins_step.span), B_q from a read whose dipole is the moment (weight x curl V_q div span); the curl and the gradient Rule3's read acts on the six neighbours' levels, every division Rule3's division act with its remainder on the body (ALGEBRA.md 9.117 the row "the spin's step", 9.78 (5), 9.104 (2), 9.119 item 2)."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from event_universe.core.register import Declaration
from event_universe.core.rule3 import NO_READ, THE_ADVANCE, THE_INVERSE, Key, carried, rule3
from event_universe.core.schema import Integer, ListOf, ObjectOf, Schema

ACTS = (THE_ADVANCE, THE_INVERSE)
SPIN = "spin"
MOMENT = "moment"
KEYS = ("gradc", "omega", "bq", "spin")  # the body's remainders of this step, by their first word
Vector = tuple[int, int, int]
Pair = tuple[int, int]
# a level at the six neighbours of the Node in the Ports' order +x, -x, +y, -y, +z, -z; None where the Node has no read there
Neighbours = tuple[int | None, int | None, int | None, int | None, int | None, int | None]


@dataclass(frozen=True)
class SpinRead:
    """One read of the body's family at the body's Node: its position in the family's reads, the read family's dipole (spin or moment), its factor on the body (the weight, or minus Q times the weight by q), its weight, the read family's vector part at the six neighbours (three components, each at the six Ports; None beyond an open face, on an axis of extent 1 or on a silent part), and for a spin's read its time part at the six neighbours and its row's two weights of the turn over one denominator, the curl's and the tidal term's (None on a moment's read)."""

    position: int
    dipole: str
    factor: int
    weight: int
    vector: tuple[Neighbours, Neighbours, Neighbours]
    time: Neighbours | None
    turn: tuple[Pair, Pair] | None


@dataclass(frozen=True)
class SpinStepTerm:
    """The body's declaration: its moment mu, the Node clock Gamma and the span of the turn, the central difference's two Links and the leapfrog's two intervals, read from the bodies' family's row (spins_step.span; ALGEBRA.md 9.78 (5))."""

    moment: Vector
    gamma: int
    span: int


@dataclass(frozen=True)
class SpinStepStart:
    """The interval's reading at (v): the act (the advance or the inverse), the reads with the neighbours' levels, the body's momentum n, its wall W, its spin S_now (the leapfrog's middle: the spin forward, the spin before backward) and the pair (spin, spin_before) it holds."""

    act: str
    reads: tuple[SpinRead, ...]
    momentum: Vector
    wall: int
    spin: Vector
    spin_before: Vector


@dataclass(frozen=True)
class SpinStepOwn:
    """The body's remainders of the spin's step: the values and carries of its carried divisions by key (("gradc", position, i), ("omega", position, i), ("bq", position, i), ("spin", i))."""

    values: Mapping[Key, int]
    carries: Mapping[Key, int]


@dataclass(frozen=True)
class SpinStepWrites:
    """The step's writes: Omega, the torque, the step per axis, the body's spin and spin before after the act, the remainders after."""

    omega: Vector
    torque: Vector
    steps: Vector
    spin: Vector
    spin_before: Vector
    own: SpinStepOwn


def cross(a: Vector, b: Vector) -> Vector:
    """a x b, the booking of ALGEBRA.md 9.121 item 2 (c): products of two levels' components, read and never written."""
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def read_act(coefficients: Vector, levels: Vector, self_coefficient: int, here: int) -> int:
    """Rule3's read act over the wall 1: the coefficients on three levels and the self coefficient on the Node's own, exact (ALGEBRA.md 9.119 item 1 (a))."""
    return int(rule3(coefficients, levels, self_coefficient, 1, here, 0, 0)[0])


def level(ports: Neighbours, port: int) -> int:
    """A neighbour's level, 0 where the Node has no read there."""
    found = ports[port]
    return 0 if found is None else found


def curl(vector: tuple[Neighbours, Neighbours, Neighbours]) -> Vector:
    """The curl of a vector part at the Node from its six neighbours, each component one read act: (curl V)_x = V_z(+y) - V_z(-y) - V_y(+z) + V_y(-z) and cyclic, the coefficients +1, -1, -1 on three neighbours and the self coefficient +1 on the fourth; a neighbour the Node lacks reads 0 (ALGEBRA.md 9.77 (3), 9.91 (8) (v))."""
    found = []
    for y, z in ((1, 2), (2, 0), (0, 1)):
        found.append(
            read_act(
                (1, -1, -1),
                (level(vector[z], 2 * y), level(vector[z], 2 * y + 1), level(vector[y], 2 * z)),
                1,
                level(vector[y], 2 * z + 1),
            )
        )
    return (found[0], found[1], found[2])


def gradient(time: Neighbours) -> Vector:
    """The gradient of the time part at the Node, per axis the read act with +1 on the neighbour ahead and the self coefficient -1 on the one behind over the wall 1; 0 on an axis where either neighbour is missing, beyond an open face or on an axis of extent 1 (ALGEBRA.md 9.78 (5))."""
    found = []
    for axis in range(3):
        ahead, behind = time[2 * axis], time[2 * axis + 1]
        found.append(
            0 if ahead is None or behind is None else read_act((1, 0, 0), (ahead, 0, 0), -1, behind)
        )
    return (found[0], found[1], found[2])


def division_now(
    act: str, key: Key, numerator: int, wall: int, values: dict[Key, int], carries: dict[Key, int]
) -> int:
    """This interval's value of a carried division: forward the division advanced; backward the value the forward wrote, the state then stepped back, so the inverse subtracts the same term the step added."""
    if act == THE_ADVANCE:
        return carried(THE_ADVANCE, key, numerator, wall, values, carries)[0]
    value = values.get(key, 0)
    carried(THE_INVERSE, key, numerator, wall, values, carries)
    return value


def load(level_now: int, amount: int) -> int:
    """Rule3's load act: the level plus the amount, the line with the self coefficient 1 over the wall 1 and the amount as the carry (ALGEBRA.md 9.119 item 1 (d))."""
    return int(rule3(NO_READ, NO_READ, 1, 1, level_now, 0, amount)[0])


def spin_wall(wall: int, gamma: int) -> int:
    """The spin's wall W_S = W Gamma, the momentum's declared wall times the Node clock (ALGEBRA.md 9.78 (5))."""
    return wall * gamma


def spin_read(read: SpinRead) -> tuple[Neighbours, tuple[Pair, Pair]]:
    """A spin's read's time part at the six neighbours and its row's two weights, refused by name where either is missing or the weights stand over two denominators or below 1."""
    if read.time is None or read.turn is None:
        raise ValueError(
            f"the spin's read at position {read.position} needs the time part at the six "
            "neighbours and its row's two weights (spins_step: curl and tidal)"
        )
    (_, c_den), (_, t_den) = read.turn
    if c_den < 1 or c_den != t_den:
        raise ValueError(
            f"the spin's step's weights {read.turn[0]} and {read.turn[1]} stand over one "
            "denominator from 1"
        )
    return read.time, read.turn


def check(term: SpinStepTerm, start: SpinStepStart) -> None:
    """The refusals by name: the act, the wall and Gamma from 1, each read's dipole spin or moment, a spin's read with its time part and its two weights over one denominator from 1."""
    if start.act not in ACTS:
        raise ValueError(f"the spin's step's act is one of {list(ACTS)}, got {start.act!r}")
    if start.wall < 1 or term.gamma < 1 or term.span < 1:
        raise ValueError(
            f"the spin's step needs the wall W = {start.wall}, Gamma = {term.gamma} and the span "
            f"{term.span} from 1"
        )
    for read in start.reads:
        if read.dipole not in (SPIN, MOMENT):
            raise ValueError(
                f"the read at position {read.position} has the dipole {read.dipole!r}: spin or moment"
            )
        if read.dipole == SPIN:
            spin_read(read)


def apply(term: SpinStepTerm, start: SpinStepStart, own: SpinStepOwn) -> SpinStepWrites:
    """The primitive at (v): the curl of each read's vector part and the gradient of a spin's read's time part by the read acts, Omega from the curl and the tidal term at the row's weights over the span, the torque from a moment's read's curl over the span, the turn (Omega x S_now) + mu x B_q over the two intervals divided by W Gamma per axis, the leapfrog forward or back by the load act (ALGEBRA.md 9.117 the row "the spin's step")."""
    check(term, start)
    values, carries = dict(own.values), dict(own.carries)
    spin_now = start.spin if start.act == THE_ADVANCE else start.spin_before
    omega = [0, 0, 0]
    torque = [0, 0, 0]
    for read in start.reads:
        if read.dipole == SPIN:
            if read.factor == 0:
                continue
            time, ((c_num, denominator), (t_num, _)) = spin_read(read)
            found = curl(read.vector)
            tidal_cross = cross(gradient(time), start.momentum)
            for i in range(3):
                tidal = division_now(
                    start.act,
                    ("gradc", read.position, i),
                    t_num * tidal_cross[i],
                    start.wall,
                    values,
                    carries,
                )
                omega[i] += division_now(
                    start.act,
                    ("omega", read.position, i),
                    c_num * read.factor * found[i] + tidal,
                    term.span * denominator,
                    values,
                    carries,
                )
        else:
            if read.weight == 0:
                continue
            found = curl(read.vector)
            for i in range(3):
                torque[i] += division_now(
                    start.act,
                    ("bq", read.position, i),
                    read.weight * found[i],
                    term.span,
                    values,
                    carries,
                )
    turn = cross((omega[0], omega[1], omega[2]), spin_now)
    twist = cross(term.moment, (torque[0], torque[1], torque[2]))
    steps = [0, 0, 0]
    spin, before = list(start.spin), list(start.spin_before)
    for i in range(3):
        steps[i] = division_now(
            start.act,
            ("spin", i),
            term.span * (turn[i] + twist[i]),
            spin_wall(start.wall, term.gamma),
            values,
            carries,
        )
        if start.act == THE_ADVANCE:
            spin[i], before[i] = load(start.spin_before[i], steps[i]), start.spin[i]
        else:
            spin[i], before[i] = start.spin_before[i], load(start.spin[i], -steps[i])
    return SpinStepWrites(
        (omega[0], omega[1], omega[2]),
        (torque[0], torque[1], torque[2]),
        (steps[0], steps[1], steps[2]),
        (spin[0], spin[1], spin[2]),
        (before[0], before[1], before[2]),
        SpinStepOwn(values, carries),
    )


DECLARATION = Declaration(
    name="the spin's step",
    place="(v)",
    reads=(
        "S_now",
        "the read families' vector parts and time parts at the body's six neighbours",
        "the spin's family's two weights of the turn and the bodies' family's span (spins_step)",
        "mu",
        "n",
        "W",
        "Gamma",
    ),
    writes=("a body's spin S", "a body's remainders"),
    function=apply,
    section="9.117 item 2, the row 'the spin's step'; 9.78 (5); 9.104 (2); 9.119 item 2",
    word="after the step",
    schema=Schema(
        {
            "a family's entry": ObjectOf(
                {
                    "spins_step": ObjectOf(
                        {
                            "curl": ListOf(Integer(least=1), 2),
                            "tidal": ListOf(Integer(least=1), 2),
                            "span": Integer(least=1),
                        },
                        frozenset({"curl", "tidal", "span"}),
                    )
                },
                frozenset({"spins_step"}),
            )
        }
    ),
)
