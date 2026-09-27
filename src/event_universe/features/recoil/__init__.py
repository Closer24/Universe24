"""The recoil of a click on a held body's momentum (ALGEBRA.md #the-primitives, the row "the recoil"): n_a += sense x sigma_a x 3 Q P_body x (L div lambda_q) div L per axis, the giver with the opposite sign, the store one remainder per axis on the universe's wall L (the least common multiple of the world's declared wavelengths, every lambda_q dividing it), so that clicks of every wavelength add exactly; the fraction W P_body / (M lambda_q) with W = 3 Q M, the body's quanta cancelled; the division Rule3's division act with the remainder carried."""

from __future__ import annotations

from dataclasses import dataclass

from event_universe.core.integer import MAX_WORK_INT
from event_universe.core.register import Declaration
from event_universe.core.rule3 import division_forward

TAKING = 1
GIVING = -1
THREE = 3  # the momentum's wall W = 3 Q M (ALGEBRA.md #the-primitives, the row "the recoil")

# the word of ALGEBRA.md 9.117 item 5 for this primitive
THE_WORD = "from the rule 9.57 (1) and the click, the store a remainder of the division on the record"


@dataclass(frozen=True)
class RecoilTerm:
    """The click's declaration: the body's period P_body, the record's wavelength lambda_q, the sense (a taking +1, a giving -1), the universe's wall L (the least common multiple of the declared wavelengths) and its momentum unit Q."""

    period: int
    wavelength: int
    sense: int
    wall: int
    unit: int


@dataclass(frozen=True)
class RecoilStart:
    """What the click booked: the tally per axis."""

    tally: tuple[int, int, int]


@dataclass(frozen=True)
class RecoilOwn:
    """The body's record: its momentum n per axis and the store per axis, a remainder on the wall L."""

    momentum: tuple[int, int, int]
    remainders: tuple[int, int, int]


@dataclass(frozen=True)
class RecoilWrites:
    """The body's momentum and its stores after the click."""

    momentum: tuple[int, int, int]
    remainders: tuple[int, int, int]


def sign_of(value: int) -> int:
    """sigma: -1, 0 or 1, the direction of travel and never the size (ALGEBRA.md 9.111 item 1)."""
    return (value > 0) - (value < 0)


def check(term: RecoilTerm, own: RecoilOwn) -> None:
    """The refusals by name: the period, the wavelength, the wall and the unit from 1, the sense +1 or -1, the wavelength dividing the wall, the click's amount within the width, each store a remainder below the wall."""
    if term.period < 1 or term.wavelength < 1 or term.wall < 1 or term.unit < 1:
        raise ValueError(
            f"the recoil needs a period, a wavelength, a wall and a unit from 1, got P_body = "
            f"{term.period}, lambda_q = {term.wavelength}, L = {term.wall}, Q = {term.unit}"
        )
    if term.sense not in (TAKING, GIVING):
        raise ValueError(f"the recoil's sense is +1 (a taking) or -1 (a giving), got {term.sense}")
    share, rest = division_forward(term.wall, term.wavelength, 0)
    if rest:
        raise ValueError(
            f"the recoil's wall L = {term.wall} is not a multiple of the wavelength lambda_q = "
            f"{term.wavelength}: L is the least common multiple of the declared wavelengths"
        )
    if THREE * term.unit * term.period * share > MAX_WORK_INT:
        raise ValueError(
            f"the recoil's amount 3 Q P_body (L div lambda_q) = {THREE * term.unit * term.period * share} "
            f"reaches the width {MAX_WORK_INT}: the click is refused"
        )
    for axis, remainder in enumerate(own.remainders):
        if not 0 <= remainder < term.wall:
            raise ValueError(
                f"the recoil's store on axis {axis} is {remainder}: a remainder below the wall L = {term.wall}"
            )


def apply(term: RecoilTerm, start: RecoilStart, own: RecoilOwn) -> RecoilWrites:
    """The primitive: per axis with a tally, n_a += sense x sigma_a x 3 Q P_body (L div lambda_q) div L with the store carried on L (ALGEBRA.md #the-primitives, the row "the recoil")."""
    check(term, own)
    share, _ = division_forward(term.wall, term.wavelength, 0)
    amount = THREE * term.unit * term.period * share
    momentum = list(own.momentum)
    stores = list(own.remainders)
    for axis in range(len(momentum)):
        sigma = sign_of(start.tally[axis])
        if sigma == 0:
            continue
        whole, stores[axis] = division_forward(term.sense * sigma * amount, term.wall, stores[axis])
        momentum[axis] += whole
    return RecoilWrites((momentum[0], momentum[1], momentum[2]), (stores[0], stores[1], stores[2]))


DECLARATION = Declaration(
    name="the recoil",
    place="(iv)",
    reads=(
        "the click's tally (sigma_a, the direction of travel)",
        "the momentum unit Q",
        "the body's period P_body",
        "the record's wavelength lambda_q",
        "the universe's wall L",
        "the giving's outward tally with the opposite sign",
    ),
    writes=("a body's momentum n", "a body's remainders"),
    function=apply,
    section=THE_WORD
    + " (9.117 item 5); 9.117 item 2, the row 'the recoil'; 9.84 (2); 9.91 (4); 9.111 items 1 and 2",
    word="after the step",
)
