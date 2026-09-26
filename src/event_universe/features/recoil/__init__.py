"""The recoil of a click on a held body's momentum: n_a += sigma_a x (W x P_body) div (M x lambda_q) per axis, the giver with the opposite sign, the store a remainder with its divisor in lowest terms so that clicks of different divisors add exactly (ALGEBRA.md 9.117 item 2 the row "the recoil" and item 5, 9.84 (2), 9.91 (4)); the amount from the rule, the store beyond (S)."""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd

from event_universe.core.register import Declaration

# the bounds of the products and of the store's divisor (ALGEBRA.md 9.91 (4)): no overflow
PRODUCT_BOUND = 10**9

TAKING = 1
GIVING = -1

# the two words of ALGEBRA.md 9.113 item 1 and 9.117 item 5, one per piece of this primitive
THE_WORD = "the amount from the rule 9.57 (1) and the click, the store below one integer beyond (S)"

Store = tuple[int, int]  # a remainder with its divisor, in lowest terms, 0 <= remainder < divisor
NO_STORE: Store = (0, 1)


@dataclass(frozen=True)
class RecoilTerm:
    """The click's declaration: the body's period P_body, its quanta M, the record's wavelength lambda_q, the sense (a taking +1, a giving -1)."""

    period: int
    quanta: int
    wavelength: int
    sense: int = TAKING


@dataclass(frozen=True)
class RecoilStart:
    """What the click booked: the tally per axis and the body's wall W = 3 Q M."""

    tally: tuple[int, int, int]
    wall: int


@dataclass(frozen=True)
class RecoilOwn:
    """The body's record: its momentum n per axis and the store per axis, a remainder with its divisor in lowest terms."""

    momentum: tuple[int, int, int]
    remainders: tuple[Store, Store, Store] = (NO_STORE, NO_STORE, NO_STORE)


@dataclass(frozen=True)
class RecoilWrites:
    """The body's momentum and its stores after the click."""

    momentum: tuple[int, int, int]
    remainders: tuple[Store, Store, Store]


def sign_of(value: int) -> int:
    """sigma: -1, 0 or 1, the direction of travel and never the size (ALGEBRA.md 9.111 item 1)."""
    return (value > 0) - (value < 0)


def check(term: RecoilTerm, start: RecoilStart, own: RecoilOwn) -> None:
    """The refusals by name: the period, the quanta, the wavelength and the wall from 1, the sense +1 or -1, the products within the bound of ALGEBRA.md 9.91 (4), each store a remainder below its divisor in lowest terms."""
    if term.period < 1 or term.quanta < 1 or term.wavelength < 1:
        raise ValueError(
            f"the recoil needs a period, quanta and a wavelength from 1, got P_body = {term.period}, "
            f"M = {term.quanta}, lambda_q = {term.wavelength} (ALGEBRA.md 9.91 (4))"
        )
    if start.wall < 1:
        raise ValueError(f"the recoil needs a wall from 1, got W = {start.wall} (ALGEBRA.md 9.96 (1))")
    if term.sense not in (TAKING, GIVING):
        raise ValueError(f"the recoil's sense is +1 (a taking) or -1 (a giving), got {term.sense}")
    if start.wall * term.period > PRODUCT_BOUND or term.quanta * term.wavelength > PRODUCT_BOUND:
        raise ValueError(
            f"the recoil's products exceed the bound: W x P_body = {start.wall * term.period}, "
            f"M x lambda_q = {term.quanta * term.wavelength}, at most {PRODUCT_BOUND} each "
            "(ALGEBRA.md 9.91 (4))"
        )
    for axis, (remainder, divisor) in enumerate(own.remainders):
        if divisor < 1 or not 0 <= remainder < divisor or gcd(remainder, divisor) != 1:
            raise ValueError(
                f"the recoil's store on axis {axis} is {remainder} / {divisor}: a remainder below "
                "its divisor, the two in lowest terms (0 / 1 for none)"
            )


def add_to_store(amount: int, divisor: int, store: Store) -> tuple[int, Store]:
    """The exact sum amount / divisor + store: the whole part and the new store in lowest terms, the two fractions brought to their least common divisor, which is refused beyond the bound."""
    reduce = gcd(abs(amount), divisor)
    amount, divisor = amount // reduce, divisor // reduce
    remainder, kept = store
    common = divisor * kept // gcd(divisor, kept)
    if common > PRODUCT_BOUND:
        raise ValueError(
            f"the recoil's store would need the divisor {common} (the click's {divisor} with the "
            f"store's {kept}), beyond the bound {PRODUCT_BOUND} (ALGEBRA.md 9.91 (4))"
        )
    whole, remainder = divmod(amount * (common // divisor) + remainder * (common // kept), common)
    reduce = gcd(remainder, common)
    return whole, (remainder // reduce, common // reduce)


def apply(term: RecoilTerm, start: RecoilStart, own: RecoilOwn) -> RecoilWrites:
    """The primitive: per axis with a tally, n_a += sense x sigma_a x (W x P_body) div (M x lambda_q) with the store carried (ALGEBRA.md 9.84 (2))."""
    check(term, start, own)
    divisor = term.quanta * term.wavelength
    momentum = list(own.momentum)
    stores = list(own.remainders)
    for axis in range(3):
        sigma = sign_of(start.tally[axis])
        if sigma == 0:
            continue
        whole, stores[axis] = add_to_store(
            term.sense * sigma * start.wall * term.period, divisor, stores[axis]
        )
        momentum[axis] += whole
    return RecoilWrites((momentum[0], momentum[1], momentum[2]), (stores[0], stores[1], stores[2]))


DECLARATION = Declaration(
    "the recoil",
    "(iv)",
    (
        "the click's tally (sigma_a, the direction of travel)",
        "the wall W",
        "the body's period P_body",
        "its quanta M",
        "the record's wavelength lambda_q",
        "the giving's outward tally with the opposite sign",
    ),
    ("a body's momentum n", "a body's remainders"),
    2,
    apply,
    THE_WORD + " (9.117 item 5); 9.117 item 2, the row 'the recoil'; 9.84 (2); 9.91 (4); "
    "9.111 items 1 and 2",
    word="after the step",
)
