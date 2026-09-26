"""THE RECOIL, THE CLICK'S STORE OF A HELD BODY'S MOMENTUM (ALGEBRA.md 9.117 item 2,
the row "the recoil"; 9.117 item 5; 9.84 (2); 9.91 (4); 9.111 items 1 and 2; 9.116
item 5; the Boss's record 2224).

THE AMOUNT IS FROM THE RULE 9.57 (1) AND THE CLICK: the rule is translation-invariant,
so its form's momentum is conserved (9.84 (1)), and the taker gains what the record
lost; THE STORE BELOW ONE INTEGER IS BEYOND THE RULE (S): the rule keeps at a Node its
two levels and one remainder and nothing on a body, so the fraction of a hop a click
leaves is a declared store on the body's record (9.113 item 3 (b)).

THE LINE. At a click the body's momentum gains, per axis, the taken quantum's
momentum over the body's own energy, on the body's wall:

  n_a += sigma_a x (W x P_body) div (M x lambda_q),

sigma_a the sign of the click's tally on axis a (the flux booked through the
detector's -a face minus through its +a face: the taken quantum's direction of
travel, 9.111 item 1), W = 3 Q M the body's wall, P_body the body's rotation
period in intervals, M its quanta, lambda_q the quantum's wavelength in Links.
THE STORE: the remainder is kept on the body's record WITH ITS DIVISOR, the two
in lowest terms, so that clicks whose divisors differ (another family's lambda_q,
another M) add exactly: the store r / e and the click's a / d are brought to the
least common divisor L, n gains (a L / d + r L / e) div L and the store keeps the
remainder over L in lowest terms; the sum of the whole parts over any clicks is
the exact floor of the sum of the fractions. With W = 3 Q M the click's fraction
reduces to 3 Q P_body / lambda_q, so the store's divisor divides the least common
multiple of the wavelengths the world declares, a fixed integer of the world; a
divisor beyond the bound is refused by name. A GIVING is the same line with the
opposite sign, its tally the outward flux through the body's Ports over the
window; a symmetric emitter's tallies cancel. The body knows nothing: not whether
it rests or moves, not whether it is a tool (a tool declares its true quanta and
recoils below every band, 9.84 (3)).

The place: (iv), the word after the step, with the click's other writes, entered at
t + 1 (9.111 item 6). Writes: a body's momentum n and a body's remainders (the store,
the writer's own record, colliding with no one). Order on n at (iv): 2, after the
giving's bulk share (1). No `bind`: the loop has no recoil today, so the register holds
the row with its `apply` and a term naming it waits for the loop's cut to call it. The bounds of 9.91 (4): W x P_body, M x lambda_q and
the store's divisor at most 10^9, the wall from 1; a term outside is refused by
name. A sourced body's store is another primitive, the recoil's accumulator at (v)
(9.109 item 2 (b)). Integers only.
"""

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
    """The click's declaration for the recoil: the body's period P_body (its
    `period`, the generator's integer), its quanta M (the live content, the sum of
    its M_k), the record's wavelength lambda_q in Links (the emitter's declared
    `wavelength`) and the sense, TAKING (+1) or GIVING (-1)."""

    period: int
    quanta: int
    wavelength: int
    sense: int = TAKING


@dataclass(frozen=True)
class RecoilStart:
    """What the click booked: the tally per axis (the -a face minus the +a face of
    the detector for a taking; the outward flux through the +a Ports minus the -a
    Ports for a giving) and the body's wall W = 3 Q M."""

    tally: tuple[int, int, int]
    wall: int


@dataclass(frozen=True)
class RecoilOwn:
    """The body's record: its momentum n per axis and the recoil's store per axis,
    a remainder with its divisor in lowest terms, kept between clicks."""

    momentum: tuple[int, int, int]
    remainders: tuple[Store, Store, Store] = (NO_STORE, NO_STORE, NO_STORE)


@dataclass(frozen=True)
class RecoilWrites:
    """The body's momentum and its stores after the click."""

    momentum: tuple[int, int, int]
    remainders: tuple[Store, Store, Store]


def sign_of(value: int) -> int:
    """sigma: -1, 0 or 1, the direction of travel, never the size (9.111 item 1)."""
    return (value > 0) - (value < 0)


def check(term: RecoilTerm, start: RecoilStart, own: RecoilOwn) -> None:
    """The refusals by name: the period, the quanta, the wavelength and the wall from 1,
    the sense +1 or -1, the two products within the bound of 9.91 (4), each store a
    remainder below its divisor in lowest terms."""
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
    """The exact sum amount / divisor + store: the whole part (the floor) and the new
    store in lowest terms. The click's fraction is reduced first, so with W = 3 Q M its
    divisor divides lambda_q; the two fractions are brought to their least common
    divisor L, which is refused beyond the bound."""
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
    """The primitive: per axis, n_a += sense x sigma_a x (W x P_body) div (M x lambda_q)
    with the store carried on the body's record; an axis with no tally is untouched,
    its store kept."""
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
