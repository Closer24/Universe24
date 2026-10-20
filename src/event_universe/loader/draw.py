"""The draw's declaration (ALGEBRA.md, The NodeDetector is one declaration kind for every experiment: a seed, its draw; #the-click-is-the-meeting, the pair's form and the GHZ gate): on the world the `draw`, the window in intervals after which the NodeDetectors over regions draw and write their click, the seed and the generator's multiplier and increment (x <- (multiplier x + increment) mod 2^width, the width the file's), every one the file's and none the engine's (`Draw`, `draw_of`), and the run back's reach (`reach`, `cone` or `board`; ALGEBRA.md, The meeting's reading, the run back's reach; the owner's words of 2026-10-19 and 2026-10-20): there is one meeting, the click that writes at the record's birth, the sides reading in the order of their closes (`meeting_back`, `lists.readings`), so the key `meeting` is refused by name (2026-10-20); a body with a probe among its transitions (a transition of a part into itself) declares its generator alone (`Generator`, `generator_of`), its window bounded by the probe's lays at its Node (ALGEBRA.md, The pulsed gate), and no body's `node_detector` admits the meeting, the world's draw's word; and on a node_detector's region its setting `basis` (p, q), the coefficients of its credit, and its parts' `pattern`, one integer pair [alpha_k, beta_k] per part of the record it reads, the + port reading the part k as e_k(+) = alpha_k p + beta_k q and the - port as e_k(-) = alpha_k (-q) + beta_k p (the pair's pattern [[1, 0], [0, 1]], the ports (p, q) and (-q, p); `ports_of`, the two ports exactly orthogonal with equal norms, refused by name otherwise), read by the reader (`tools/bell_gate.py`) and by the sides' draws in the run (`meeting_back.coefficients_of`); every defect refused by name and no default written."""

from __future__ import annotations

import itertools
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from math import gcd
from typing import Any

from event_universe.core.integer import MAX_WORK_INT
from event_universe.core.rule3 import division_forward
from event_universe.loader.derived import FamilyRule
from event_universe.loader.keys import integer, keyed

Gauss = tuple[
    int, int
]  # a Gaussian integer (re, im), a part's coefficient: an integer where im is 0, a quarter turn's unit on a plane's second component (the two-term plane GHZ, 2026-10-20)
Pattern = tuple[tuple[int, int], ...]  # per part [alpha_k, beta_k], the part's read of the setting
Ports = tuple[
    tuple[Gauss, ...], tuple[Gauss, ...]
]  # a side's two ports, + then -, one coefficient per part
UNITS: tuple[Gauss, ...] = ((1, 0), (0, 1), (-1, 0), (0, -1))  # i^turn, the azimuth in quarter turns
TURN = "turn"  # a plane side's key beside `axis`: the azimuth in quarter turns, 0 to 3
GENERATOR_KEYS = (
    "seed",
    "multiplier",
    "increment",
)  # a draw's generator: the keys of a body whose window is bounded by its probe's lays
DRAW_KEYS = (
    "window",
    *GENERATOR_KEYS,
)  # the draw with its window: the world's and a body's without a probe
MEETING = "meeting"  # a key of the world's draw refused by name (`draw_of`): there is one meeting
REACH = "reach"  # the back mode's key: the run back's reach, the owner's word of 2026-10-19
BOARD, CONE = "board", "cone"  # its two words: the whole board, the record's light cone (the default)
REACHES = (BOARD, CONE)
WORLD_DRAW_KEYS = (
    *DRAW_KEYS,
    MEETING,
    REACH,
)  # the world's draw alone declares the meeting and its reach


@dataclass(frozen=True)
class Generator:
    """A draw's generator as the files declare it: the seed and the generator's multiplier and increment, x <- (multiplier x + increment) mod 2^width (features/click); a body with a probe among its transitions declares this alone under `node_detector`, its window bounded by the probe's lays at its Node, the world's schedule (ALGEBRA.md, The pulsed gate; the two hands)."""

    seed: int
    multiplier: int
    increment: int


@dataclass(frozen=True)
class Draw(Generator):
    """A draw with its declared window beside the generator's three keys: the world's (the intervals after which every node_detector's window closes and the NodeDetector draws and writes), a record converted whole's (its table's rate per window) and a body's without a probe (declared where a drive's lay has no end, derived from the lays' passage over the body otherwise, `loader/window.py`, 2026-10-19); and the run back's reach of the world's draw alone, `cone` or `board` (`REACHES`, `meeting_back`), None where the file declares none, which the engine reads as the record's light cone (`credit.Books.reach`, the owner's word of 2026-10-19), written nowhere."""

    window: int
    reach: str | None = None


def generator_of(value: object, label: str) -> Generator:
    """A body's `node_detector` where a probe stands among its transitions: the generator's three keys, the seed and the increment from 0 and the multiplier from 1; a `window` refused by name, the window of a body with a probe being bounded by the probe's lays at its Node, the world's schedule and no number of the body's (ALGEBRA.md, The pulsed gate; the two hands); every other key refused by name, the meeting's reading among them (`keyed`: a body's generator admits no `meeting`, the world's draw's word)."""
    if isinstance(value, dict) and "window" in value:
        raise ValueError(
            f"{label} declares a window beside a probe, and the window of a body with a probe is bounded by the "
            f"probe's lays at its Node, the world's schedule (ALGEBRA.md, The pulsed gate); its keys are "
            f"{list(GENERATOR_KEYS)}"
        )
    found = keyed(value, label, GENERATOR_KEYS, GENERATOR_KEYS)
    return Generator(
        integer(found["seed"], f"{label}.seed", 0),
        integer(found["multiplier"], f"{label}.multiplier", 1),
        integer(found["increment"], f"{label}.increment", 0),
    )


def draw_of(value: object, label: str, world: bool = False) -> Draw:
    """The world's `draw` (`world`), a record converted whole's `node_detector` and a body's that declares its window (`body_draw_of`): its four keys, the window from 1, the seed and the increment from 0 and the multiplier from 1; on the world's draw alone the run back's reach, `reach`: `board` (the whole board stepped back to the birth and forward to the close) or `cone` (the record's light cone, the engine's reading where the key is absent); `books` and any other value refused by name; `meeting` refused by name, there being one meeting; every other key refused by name, a body's `meeting` and `reach` among them (`keyed` on `DRAW_KEYS`)."""
    found = keyed(value, label, WORLD_DRAW_KEYS if world else DRAW_KEYS, DRAW_KEYS)
    reach = found.get(REACH)
    if MEETING in found:
        raise ValueError(
            f"{label}.{MEETING} is declared: there is one meeting, the click that writes at the record's birth, "
            "the sides reading in the order of their closes; the key is refused"
        )
    if reach is not None and reach not in REACHES:
        reason = (
            "the click that runs back writes at the birth and runs; the reaches are 'cone' and 'board'"
            if reach == "books"
            else f"the run back's reach is {CONE!r} or {BOARD!r}"
        )
        raise ValueError(f"{label}.{REACH} is {reach!r}: {reason}")
    return Draw(
        integer(found["seed"], f"{label}.seed", 0),
        integer(found["multiplier"], f"{label}.multiplier", 1),
        integer(found["increment"], f"{label}.increment", 0),
        integer(found["window"], f"{label}.window", 1),
        None if reach is None else str(reach),
    )


def body_draw_of(value: object, label: str) -> Generator:
    """A body's `node_detector` without a probe: the generator's three keys and, where the declaration carries it, its `window` (`Draw`, `draw_of`), else the generator alone (`Generator`, `generator_of`); the window of a body whose drives are laid with an end is derived at the end of the load from the lays' passage over it, where the key is refused by name, and declared, the instrument's cadence, where a drive is laid with no end or nowhere (`loader/window.windowed`, the atom branch, 2026-10-19)."""
    found = keyed(value, label, DRAW_KEYS, GENERATOR_KEYS)
    return draw_of(found, label) if "window" in found else generator_of(found, label)


def ports_of(basis: tuple[int, ...], pattern: Pattern, turn: int = 0) -> Ports:
    """A side's two ports from its declared setting (p, q) and its parts' pattern [[alpha_k, beta_k], ...]: e_k(+) = alpha_k p + beta_k q and e_k(-) = alpha_k (-q) + beta_k p, the - port the + port's with the setting turned a quarter (the pair's pattern [[1, 0], [0, 1]] gives (p, q) and (-q, p)); refused by name: a setting of other than two coefficients, no pattern, and two ports not orthogonal with equal norms, which is no setting of two outcomes. With a quarter turn on a plane side (`turn`, u = i^turn on the second component; the two-term plane GHZ, 2026-10-20): e_k(+) = alpha_k p + beta_k u q and e_k(-) = alpha_k (-conj(u) q) + beta_k p, Gaussian integers, the two ports orthogonal in the Hermitian form, SUM_k conj(e_k(+)) e_k(-) = 0, with equal norms, exact in the integers; at turn 0 the integers as before with 0 behind them."""
    if len(basis) != 2 or not pattern:
        raise ValueError(
            "a side declares its setting (p, q) as `basis` and one pair [alpha, beta] per part as "
            f"`pattern`, got {basis} and {list(pattern)}"
        )
    p, q = basis
    (u_re, u_im), (c_re, c_im) = UNITS[turn], (UNITS[turn][0], -UNITS[turn][1])  # u and conj(u)
    plus = tuple((alpha * p + beta * u_re * q, beta * u_im * q) for alpha, beta in pattern)
    minus = tuple((beta * p - alpha * c_re * q, -alpha * c_im * q) for alpha, beta in pattern)
    crossed = (
        sum(a[0] * b[0] + a[1] * b[1] for a, b in zip(plus, minus, strict=True)),
        sum(a[0] * b[1] - a[1] * b[0] for a, b in zip(plus, minus, strict=True)),
    )  # SUM conj(e(+)) e(-)
    if crossed != (0, 0) or sum(norm(a) for a in plus) != sum(norm(b) for b in minus):
        raise ValueError(
            f"the pattern {list(pattern)} at the setting {basis} gives the ports {plus} and {minus}, "
            "not orthogonal with equal norms: no setting of two outcomes"
        )
    return plus, minus


def basis_of(value: object, label: str) -> tuple[int, ...]:
    """A node_detector's declared basis, its setting: a list of integers not all 0 (the pair's (p, q)); refused by name otherwise."""
    if not isinstance(value, list) or not value or not any(value):
        raise ValueError(f"{label} must be a list of integers, the setting's coefficients, not all 0")
    return tuple(integer(v, f"{label}[{i}]", -MAX_WORK_INT) for i, v in enumerate(value))


def times(a: Gauss, b: Gauss) -> Gauss:
    """The product of two Gaussian integers, (a_re b_re - a_im b_im, a_re b_im + a_im b_re), exact; the integers' product where both im are 0 (ALGEBRA.md, The click is the meeting of the future with the past, the Gaussian clause of 2026-10-20)."""
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def norm(a: Gauss) -> int:
    """The norm of a Gaussian integer, re^2 + im^2, the square where im is 0: the coefficient's weight in the record's scale."""
    return a[0] * a[0] + a[1] * a[1]


def pattern_of(value: object, label: str, basis: tuple[int, ...]) -> Pattern:
    """A node_detector's declared pattern: a list of integer pairs [alpha_k, beta_k], one per part of the record it reads, none [0, 0] (a part read with no coefficient at either port is no part of the read), on a setting of two coefficients (p, q); refused by name otherwise."""
    if len(basis) != 2:
        raise ValueError(
            f"{label} reads the setting (p, q) of two coefficients into the parts, and the basis has {len(basis)}"
        )
    if not isinstance(value, list) or not value:
        raise ValueError(f"{label} must list one pair [alpha, beta] per part of the record it reads")
    found = []
    for index, entry in enumerate(value):
        if not isinstance(entry, list) or len(entry) != 2:
            raise ValueError(
                f"{label}[{index}] must be a pair [alpha, beta]: e(+) = alpha p + beta q, e(-) = alpha (-q) + beta p"
            )
        alpha = integer(entry[0], f"{label}[{index}][0]", -MAX_WORK_INT)
        beta = integer(entry[1], f"{label}[{index}][1]", -MAX_WORK_INT)
        if alpha == 0 and beta == 0:
            raise ValueError(
                f"{label}[{index}] is [0, 0]: a part read with no coefficient at either port is no part of the read"
            )
        found.append((alpha, beta))
    return tuple(found)


def patterns_of_the_law(
    patterns: list[tuple[str, Pattern]], laid: list[int], families: tuple[FamilyRule, ...]
) -> None:
    """A declared pattern reads one record of several parts, one pair per part: its length is the parts of a family of several parts the world lays (its packets' and its bodies' families, `laid`, by their indexes); refused by name where the lengths differ or the world lays no such record; and a laid family declaring the antisymmetric sign under exchange, where a side's pattern reads its parts, is read by two sides exactly, the determinant of two sides' parts (`meeting_back.coefficients_of`, `credit.terms_of`, the family's declaration), another count of sides refused by name at load, generic for N sides otherwise (the owner's word of 2026-10-19); read at no side, the sign is the shell's and the lists' own (`lists.absorption`) and nothing is asked."""
    parts = sorted({families[index].parts for index in laid if families[index].parts > 1})
    for name, pattern in patterns:
        if pattern and len(pattern) not in parts:
            raise ValueError(
                f"node_detector {name!r} declares a pattern of {len(pattern)} parts, and the world lays "
                + (
                    f"records of {parts} parts, one pair per part"
                    if parts
                    else "no record of several parts"
                )
            )
    for index in sorted({index for index in laid if families[index].exchange < 0}):
        sides = sum(1 for _name, pattern in patterns if len(pattern) == families[index].parts)
        if sides and sides != 2:  # read at no side, the sign is the shell's and the lists' alone
            raise ValueError(
                f"{families[index].name!r} declares the antisymmetric sign under exchange and {sides} side(s) read "
                "its parts: the antisymmetric record's determinant is two sides', and another count of sides is a "
                "declaration the law has not made (ALGEBRA.md, Spin, closed for the paper as a route)"
            )


def setting_of(row: Mapping[str, object], label: str) -> tuple[tuple[int, ...], tuple[int, ...], int]:
    """A node_detector's setting from its row, (basis, axis), each () where the key is absent: `basis`, the setting's coefficients (p, q) for a record of real-line parts, or `axis`, the half-angle pair (c, s) of the detector's axis for a record of planes (the spin branch, 2026-10-19), one of the two; refused by name where both stand, and where a region declares a setting with no `pattern` to read it with (a setting is read by the pattern alone; a body's node_detector refuses a setting by its own line). With `turn`, the azimuth in quarter turns 0 to 3 on a plane side beside its `axis` (the two-term plane GHZ, 2026-10-20), refused by name beside `basis` or without `axis`, and outside 0 to 3 (`integer`); 0 where the key is absent."""
    basis = basis_of(row["basis"], f"{label}.basis") if "basis" in row else ()
    axis = basis_of(row["axis"], f"{label}.axis") if "axis" in row else ()
    if axis and basis:
        raise ValueError(
            f"{label} declares both `axis` and `basis`: a side's setting is one of the two, `basis` the setting's "
            "coefficients (p, q) for a record of real-line parts and `axis` the half-angle pair (c, s) for planes"
        )
    if (axis or basis) and "pattern" not in row and "block" not in row:
        raise ValueError(
            f"{label} declares a setting and no `pattern` to read it with: a setting is read by the pattern alone"
        )
    turn = integer(row[TURN], f"{label}.{TURN}", 0, 3) if TURN in row else 0
    if TURN in row and not axis:
        raise ValueError(
            f"{label}.{TURN} is declared without `axis`: the quarter turn is a plane side's azimuth, declared "
            "beside its `axis` (a real-line side's `basis` carries none)"
        )
    return basis, axis, turn


def settings_of_the_law(
    sides: list[tuple[str, tuple[int, ...], tuple[int, ...], Pattern]],
    laid: list[int],
    families: tuple[FamilyRule, ...],
) -> None:
    """A side's setting is `basis` for a record of real-line parts, the setting's coefficients (p, q) at the full angle (the pair's and the GHZ's polarizations), and `axis` for a record of plane parts, the half-angle pair (c, s) of the detector's axis, the spinor read of a two-plane record (the spin branch, 2026-10-19; ALGEBRA.md, Spin, closed for the paper as a route: the half angle is the detector's declared basis and no property of the record under the 48): per side with a pattern, the laid families of as many parts as the pattern name the kind; refused by name where the side declares the other kind or where the laid records are of both kinds. The two ports' arithmetic is one (`ports_of`): e_k(+) = alpha_k c + beta_k s, e_k(-) = beta_k c - alpha_k s."""
    for name, axis, basis, pattern in sides:
        if not pattern:
            continue
        planes = {families[index].plane for index in laid if families[index].parts == len(pattern)}
        if len(planes) == 2:
            raise ValueError(
                f"node_detector {name!r} reads records of planes and of real lines with one pattern: a side's "
                "setting is one kind's, `axis` for planes and `basis` for real lines"
            )
        if planes == {True} and basis:
            raise ValueError(
                f"node_detector {name!r} declares `basis` for a record of planes, whose sides declare `axis`, the "
                "half-angle pair (c, s) of the detector's axis"
            )
        if planes == {False} and axis:
            raise ValueError(
                f"node_detector {name!r} declares `axis` for a record of real lines, whose sides declare `basis`, "
                "the setting's coefficients (p, q)"
            )


def reduced_write(written: Sequence[Gauss], coefficients: Sequence[Gauss]) -> list[Gauss]:
    """The click's write as the law's arithmetic (the reader's ruling of 2026-10-20; ALGEBRA.md, The click is the meeting of the future with the past: at the root it writes): the realised port's coefficients on the record's surviving parts, a part surviving while its cumulative coefficient `written` is other than 0 (every part before any write), divided by their greatest common divisor, the direction's least integers; where they are one value on every surviving part (a scaling, a global sign included) the write is the identity, 1 on every part; a part written 0 before keeps 1 here, its lines at 0; the gcd Euclid's and the reduction the division act with no remainder (`math.gcd`, `division_forward`); read at the click (`credit.reduced`) and at load by the bound gate (`compounding_of_the_law`). The cumulative coefficients (`credit.Books.written`), the product of the per-write reduced vectors, may carry a common factor no single port had ((2, 3) then (3, 2) gives (6, 6)): it is not reduced later, since between two writes the parts walk under Rule3 and are no longer exact multiples, so a later division would not be exact; it costs the amplitude bound alone, which the load gate accounts for (`compounding_of_the_law`; the Boss's decision on the reader's W2 and Q1, 2026-10-20). On Gaussian integers (the two-term plane GHZ, 2026-10-20): a part survives while its cumulative pair is other than (0, 0), the common factor is the gcd of every re and im of the surviving coefficients (the rational integers' gcd: a common Gaussian factor that is no integer, (1, 1) on ((1, 1), (1, -1)), is not reduced and costs the bound alone, which the load gate accounts for), the identity (1, 0) on every part where one pair stands on every surviving part (a scaling or a global unit, a quarter turn of the whole record being a phase and no direction)."""
    surviving = [k for k, w in enumerate(written) if w != (0, 0)]
    common = 0
    for k in surviving:
        common = gcd(gcd(common, abs(int(coefficients[k][0]))), abs(int(coefficients[k][1])))
    if common == 0:
        return [(1, 0)] * len(written)
    found = [
        (int(division_forward(int(c[0]), common, 0)[0]), int(division_forward(int(c[1]), common, 0)[0]))
        if k in surviving
        else (1, 0)
        for k, c in enumerate(coefficients)
    ]
    return [(1, 0)] * len(written) if len({found[k] for k in surviving}) == 1 else found


def compounding_of_the_law(
    rows: Sequence[Any],
    laid: list[int],
    families: tuple[FamilyRule, ...],
    packets: Sequence[Any],
    bound: int,
) -> None:
    """The amplitude bound read from the file's own patterns at load (the reader's ruling of 2026-10-20, precision two; ALGEBRA.md, The click is the meeting of the future with the past): two or more rotated sides on a record of two or more parts compound to the direction's least integers, which no gcd reduces (the singlet under (12, 5) then (-12, 5) on its two terms ends at (-144, 25)), so for every family of several parts the world lays with a declared amplitude (the largest of its packets', `packets` the world's packet rows; `rows` the node_detector rows, each read for its setting, `axis` or `basis`, and its `pattern`), over every combination of the sides' ports in every order of the sides (the engine writes in the order of the closes, and the magnitude depends on the order where the identity rule fires at another step: (1, 0) then (3, 5) ends at (1, 0), (3, 5) then (1, 0) at (3, 0); the reader's W3; the first side's coefficients the determinant's for the antisymmetric record), the coefficients standing after the writes (`reduced_write`) are read for their largest magnitude, and the world is refused by name where that magnitude times the lay's amplitude passes the bound A, the product, the amplitude and A named; a record born of a body, with no declared amplitude, is read at its write alone (`meeting_back.realised`)."""
    amplitudes = {
        f: max(int(p.amplitude) for p in packets if p.family == f) for f in {p.family for p in packets}
    }
    for index in sorted(set(laid)):
        family = families[index]
        sides = [
            ports_of(d.axis or d.basis, d.pattern, d.turn)
            for d in rows
            if len(d.pattern) == family.parts
        ]
        if family.parts < 2 or not sides or index not in amplitudes:
            continue
        orders = [
            list(o) for o in itertools.permutations(range(len(sides)))
        ]  # the engine writes in the closes' order
        for order, combination in itertools.product(
            orders, itertools.product(range(2), repeat=len(sides))
        ):
            written: list[Gauss] = [(1, 0)] * family.parts
            for k, (ports, port) in enumerate(zip([sides[o] for o in order], combination, strict=True)):
                coefficients = list(ports[port])
                if k == 0 and family.exchange < 0 and family.parts == 2:  # the determinant's lambdas
                    coefficients = [coefficients[1], (-coefficients[0][0], -coefficients[0][1])]
                written = [
                    times(w, c)
                    for w, c in zip(written, reduced_write(written, coefficients), strict=True)
                ]
            largest = max(
                abs(w[0]) + abs(w[1]) for w in written
            )  # the bound of (a, b) on a level, |a| + |b|
            if largest * amplitudes[index] > bound:
                raise ValueError(
                    f"the sides' patterns compound on the record of {family.name!r} to the coefficient {largest} (the "
                    f"ports {list(combination)} of the sides in the order {order}, reduced), times the lay's amplitude "
                    f"{amplitudes[index]}: {largest * amplitudes[index]} passes the amplitude bound A = {bound}; "
                    "lower the amplitude or the settings' integers"
                )
