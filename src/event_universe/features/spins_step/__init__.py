"""The spin's step: S_next = S_before + (2 [(Omega x S_now) + mu x B_q] + carry) div (W Gamma), Omega from a read whose dipole is the spin (factor x curl V + 3 ((grad c) x n) div W, div 8) and B_q from a read whose dipole is the moment (weight x curl V_q div 2), the curls and the gradient the loop's reads at the body's Node, every division Rule3's division act with its remainder on the body (ALGEBRA.md 9.117 the row "the spin's step", 9.78 (5), 9.104 (2), 9.119 item 2)."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any

from event_universe.core.integer import bounded_gcd
from event_universe.core.register import Declaration
from event_universe.core.rule3 import NO_READ, THE_ADVANCE, THE_INVERSE, Key, carried, rule3

ACTS = (THE_ADVANCE, THE_INVERSE)
SPAN = 2  # the central difference's two Links and the leapfrog's two intervals, the lattice's own integer (ALGEBRA.md 9.78 (5))
SPIN = "spin"
MOMENT = "moment"
Vector = tuple[int, int, int]


@dataclass(frozen=True)
class SpinRead:
    """One read of the body's family at the body's Node: its position in the family's reads, the read family's dipole (spin or moment), its factor on the body (the weight, or minus Q times the weight by q), its weight, the curl of the read's vector part, and the gradient of its time part for a spin's read (None for a moment's)."""

    position: int
    dipole: str
    factor: int
    weight: int
    curl: Vector
    gradient: Vector | None


@dataclass(frozen=True)
class SpinStepTerm:
    """The body's declaration: its moment mu, the Node clock Gamma, and the family's row's two weights of the spin's turn as pairs, the curl's (1 / 4 in the levels' unit) and the tidal term's (3 / 4), Schiff's 1 / 2 and 3 / 2 (ALGEBRA.md 9.78 (5))."""

    moment: Vector
    gamma: int
    curl_weight: tuple[int, int]
    tidal_weight: tuple[int, int]


@dataclass(frozen=True)
class SpinStepStart:
    """The interval's reading at (v): the act (the advance or the inverse), the reads with their curls and gradients, the body's momentum n, its wall W, its spin S_now (the leapfrog's middle: the spin forward, the spin before backward) and the pair (spin, spin_before) it holds."""

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
    """a x b, a booking of two vectors' components (ALGEBRA.md 9.78 (5))."""
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def division_now(
    act: str, key: Key, numerator: int, wall: int, values: dict[Key, int], carries: dict[Key, int]
) -> int:
    """This interval's value of a carried division: forward the division advanced; backward the value the forward wrote, the state then stepped back, so the inverse subtracts the same term the step added."""
    if act == THE_ADVANCE:
        return carried(THE_ADVANCE, key, numerator, wall, values, carries)[0]
    value = values.get(key, 0)
    carried(THE_INVERSE, key, numerator, wall, values, carries)
    return value


def load(level: int, amount: int) -> int:
    """Rule3's load act: the level plus the amount, the line with the self coefficient 1 over the wall 1 and the amount as the carry (ALGEBRA.md 9.119 item 1 (d))."""
    return int(rule3(NO_READ, NO_READ, 1, 1, level, 0, amount)[0])


def spin_wall(wall: int, gamma: int) -> int:
    """The spin's wall W_S = W Gamma, the momentum's declared wall times the Node clock (ALGEBRA.md 9.78 (5))."""
    return wall * gamma


def check(term: SpinStepTerm, start: SpinStepStart) -> None:
    """The refusals by name: the act, the wall and Gamma from 1, the two weights' denominators from 1, each read's dipole spin or moment, a spin's read with its gradient."""
    if start.act not in ACTS:
        raise ValueError(f"the spin's step's act is one of {list(ACTS)}, got {start.act!r}")
    if start.wall < 1 or term.gamma < 1:
        raise ValueError(
            f"the spin's step needs the wall W = {start.wall} and Gamma = {term.gamma} from 1"
        )
    if term.curl_weight[1] < 1 or term.tidal_weight[1] < 1:
        raise ValueError(
            f"the spin's step's weights {term.curl_weight} and {term.tidal_weight} need denominators from 1"
        )
    for read in start.reads:
        if read.dipole not in (SPIN, MOMENT):
            raise ValueError(
                f"the read at position {read.position} has the dipole {read.dipole!r}: spin or moment"
            )
        if read.dipole == SPIN and read.gradient is None:
            raise ValueError(
                f"the spin's read at position {read.position} needs the gradient of its time part"
            )


def apply(term: SpinStepTerm, start: SpinStepStart, own: SpinStepOwn) -> SpinStepWrites:
    """The primitive at (v): Omega from the curl and the tidal term at the declared weights over the span, the torque from the charge's curl over the span, the turn (Omega x S_now) + mu x B_q over the two intervals divided by W Gamma per axis, the leapfrog forward or back by the load act (ALGEBRA.md 9.117 the row "the spin's step")."""
    check(term, start)
    values, carries = dict(own.values), dict(own.carries)
    (c_num, c_den), (t_num, t_den) = term.curl_weight, term.tidal_weight
    common = c_den * t_den // bounded_gcd(c_den, t_den)  # the weights' least common denominator
    spin_now = start.spin if start.act == THE_ADVANCE else start.spin_before
    omega = [0, 0, 0]
    torque = [0, 0, 0]
    for read in start.reads:
        if read.dipole == SPIN:
            if read.factor == 0:
                continue
            assert read.gradient is not None
            tidal_cross = cross(read.gradient, start.momentum)
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
                    c_num * (common // c_den) * read.factor * read.curl[i] + (common // t_den) * tidal,
                    SPAN * common,
                    values,
                    carries,
                )
        else:
            if read.weight == 0:
                continue
            for i in range(3):
                torque[i] += division_now(
                    start.act,
                    ("bq", read.position, i),
                    read.weight * read.curl[i],
                    SPAN,
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
            SPAN * (turn[i] + twist[i]),
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
    "the spin's step",
    "(v)",
    (
        "S_now",
        "the curls at the body's Node (V gravity's vector part, c its t part, B_q the charge's curl)",
        "mu",
        "n",
        "W",
        "Gamma",
    ),
    ("a body's spin S", "a body's remainders"),
    None,
    apply,
    "9.117 item 2, the row 'the spin's step'; 9.78 (5); 9.104 (2); 9.119 item 2",
    word="after the step",
)


def bind(loop: Any) -> Callable[..., object]:
    """The loop's method `_body_step`, whose divisions `apply` gives bit for bit, until the loop calls `apply`."""
    return loop._method("_body_step")  # type: ignore[no-any-return]
