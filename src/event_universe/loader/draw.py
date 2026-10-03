"""The draw's declaration (ALGEBRA.md, The NodeReader is one declaration kind for every experiment: a seed, its draw; #the-click-is-the-meeting, the pair's form and the GHZ gate): on the world the `draw`, the window in intervals after which the NodeReaders over regions draw and write their click, the seed and the generator's multiplier and increment (x <- (multiplier x + increment) mod 2^width, the width the file's), every one the file's and none the engine's (`Draw`, `draw_of`); a body with a probe among its transitions (a transition of a part into itself) declares its generator alone (`Generator`, `generator_of`), its window bounded by the probe's lays at its Node (ALGEBRA.md, The pulsed gate); and on a node_reader's region its setting `basis` (p, q), the coefficients of its credit, and its parts' `pattern`, one integer pair [alpha_k, beta_k] per part of the record it reads, the + port reading the part k as e_k(+) = alpha_k p + beta_k q and the - port as e_k(-) = alpha_k (-q) + beta_k p (the pair's pattern [[1, 0], [0, 1]], the ports (p, q) and (-q, p); `ports_of`, the two ports exactly orthogonal with equal norms, refused by name otherwise), read by the reader (`tools/bell_gate.py`) and by the draw through the root in the run; every defect refused by name and no default written."""

from __future__ import annotations

from dataclasses import dataclass

from event_universe.core.integer import MAX_WORK_INT
from event_universe.loader.derived import FamilyRule
from event_universe.loader.keys import integer, keyed

Pattern = tuple[tuple[int, int], ...]  # per part [alpha_k, beta_k], the part's read of the setting
Ports = tuple[tuple[int, ...], tuple[int, ...]]  # a side's two ports, + then -, one coefficient per part
GENERATOR_KEYS = (
    "seed",
    "multiplier",
    "increment",
)  # a draw's generator: the keys of a body whose window is bounded by its probe's lays
DRAW_KEYS = (
    "window",
    *GENERATOR_KEYS,
)  # the draw with its window: the world's and a body's without a probe


@dataclass(frozen=True)
class Generator:
    """A draw's generator as the files declare it: the seed and the generator's multiplier and increment, x <- (multiplier x + increment) mod 2^width (features/click); a body with a probe among its transitions declares this alone under `instrument`, its window bounded by the probe's lays at its Node, the world's schedule (ALGEBRA.md, The pulsed gate; the two hands of 2026-10-03)."""

    seed: int
    multiplier: int
    increment: int


@dataclass(frozen=True)
class Draw(Generator):
    """A draw with its declared window beside the generator's three keys: the world's (the intervals after which every node_reader's window closes and the instrument draws and writes), a record converted whole's (its table's rate per window) and a body's without a probe (its window standing by name as the probe that is not laid)."""

    window: int


def generator_of(value: object, label: str) -> Generator:
    """A body's `instrument` where a probe stands among its transitions: the generator's three keys, the seed and the increment from 0 and the multiplier from 1; a `window` refused by name, the window of a body with a probe being bounded by the probe's lays at its Node, the world's schedule and no number of the body's (ALGEBRA.md, The pulsed gate; the two hands of 2026-10-03, #1572 comments 5967783614 and 5967913000); every other key refused by name."""
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


def draw_of(value: object, label: str) -> Draw:
    """The world's `instrument`, and a body's without a probe: its four keys, the window from 1, the seed and the increment from 0 and the multiplier from 1, every other key refused by name."""
    found = keyed(value, label, DRAW_KEYS, DRAW_KEYS)
    return Draw(
        integer(found["seed"], f"{label}.seed", 0),
        integer(found["multiplier"], f"{label}.multiplier", 1),
        integer(found["increment"], f"{label}.increment", 0),
        integer(found["window"], f"{label}.window", 1),
    )


def ports_of(basis: tuple[int, ...], pattern: Pattern) -> Ports:
    """A side's two ports from its declared setting (p, q) and its parts' pattern [[alpha_k, beta_k], ...]: e_k(+) = alpha_k p + beta_k q and e_k(-) = alpha_k (-q) + beta_k p, the - port the + port's with the setting turned a quarter (the pair's pattern [[1, 0], [0, 1]] gives (p, q) and (-q, p)); refused by name: a setting of other than two coefficients, no pattern, and two ports not orthogonal with equal norms, which is no instrument of two outcomes."""
    if len(basis) != 2 or not pattern:
        raise ValueError(
            "a side declares its setting (p, q) as `basis` and one pair [alpha, beta] per part as "
            f"`pattern`, got {basis} and {list(pattern)}"
        )
    p, q = basis
    plus = tuple(alpha * p + beta * q for alpha, beta in pattern)
    minus = tuple(beta * p - alpha * q for alpha, beta in pattern)
    crossed = sum(u * v for u, v in zip(plus, minus, strict=True))
    if crossed or sum(u * u for u in plus) != sum(v * v for v in minus):
        raise ValueError(
            f"the pattern {list(pattern)} at the setting {basis} gives the ports {plus} and {minus}, "
            "not orthogonal with equal norms: no instrument of two outcomes"
        )
    return plus, minus


def basis_of(value: object, label: str) -> tuple[int, ...]:
    """A node_reader's declared basis, its setting: a list of integers not all 0 (the pair's (p, q)); refused by name otherwise."""
    if not isinstance(value, list) or not value or not any(value):
        raise ValueError(f"{label} must be a list of integers, the setting's coefficients, not all 0")
    return tuple(integer(v, f"{label}[{i}]", -MAX_WORK_INT) for i, v in enumerate(value))


def pattern_of(value: object, label: str, basis: tuple[int, ...]) -> Pattern:
    """A node_reader's declared pattern: a list of integer pairs [alpha_k, beta_k], one per part of the record it reads, none [0, 0] (a part read with no coefficient at either port is no part of the read), on a setting of two coefficients (p, q); refused by name otherwise."""
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
    """A declared pattern reads one record of several parts, one pair per part: its length is the parts of a family of several parts the world lays (its messages' and its bodies' families, `laid`, by their indexes); refused by name where the lengths differ or the world lays no such record."""
    parts = sorted({families[index].parts for index in laid if families[index].parts > 1})
    for name, pattern in patterns:
        if pattern and len(pattern) not in parts:
            raise ValueError(
                f"node_reader {name!r} declares a pattern of {len(pattern)} parts, and the world lays "
                + (
                    f"records of {parts} parts, one pair per part"
                    if parts
                    else "no record of several parts"
                )
            )
