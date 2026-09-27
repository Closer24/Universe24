"""The self-source: Sigma_self = (SUM over the six Links, the family's records and their levels of (a_j - a_i)^2) div P_2 at every Node, each difference Rule3's read act on the Link's value against the Node's own level over the wall 1, its square a booking of the family's own levels, the sum divided by P_2 by Rule3's division act with the remainder not kept, the write w Sigma_self off the step's right side (ALGEBRA.md 9.117 the row "the self-source", 9.91 (5), 9.78 (3), 9.119 item 2)."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from event_universe.core.integer import MAX_WORK_INT
from event_universe.core.register import Declaration
from event_universe.core.rule3 import rule3

NO_READ = (0, 0, 0)


@dataclass(frozen=True)
class OwnLevel:
    """One level of the family at the Node (a record's first or second level, a held part's) and its values across the six Ports in the order +x, -x, +y, -y, +z, -z, as the send put them on the Links."""

    here: Any
    links: tuple[Any, ...]


@dataclass(frozen=True)
class SelfSourceTerm:
    """The family's declaration: the self-source's unit P_2 (from 1; 0 is the line off and never called) and the amplitude bound A of its levels."""

    unit: int
    amplitude: int


@dataclass(frozen=True)
class SelfSourceStart:
    """The interval's reading at (i): every level of the family at the Node with its six Links (now forward, before backward)."""

    levels: tuple[OwnLevel, ...]


@dataclass(frozen=True)
class SelfSourceWrites:
    """The line's writes: Sigma_self, the load off the step's right side, and the sum of the squares it divided."""

    source: Any
    total: Any


def difference(here: Any, arrived: Any) -> Any:
    """The Link's value less the Node's own level, Rule3's read act with the coefficient 1 on the arrival and -1 on the level over the wall 1, exact (ALGEBRA.md 9.119 item 1 (a))."""
    return rule3((1, 0, 0), (arrived, 0, 0), -1, 1, here, 0, 0)[0]


def bound(term: SelfSourceTerm, levels: int) -> int:
    """The largest sum the line reaches with every level at A: six squared differences of 2 A per level (ALGEBRA.md 9.57 (2))."""
    return 6 * levels * 4 * term.amplitude * term.amplitude


def check(term: SelfSourceTerm, start: SelfSourceStart) -> None:
    """The refusals by name: P_2 from 1, six Links per level, the sum within int64."""
    if term.unit < 1:
        raise ValueError(
            f"the self-source's unit P_2 is {term.unit}: from 1 (0 is the line off, never called)"
        )
    for index, level in enumerate(start.levels):
        if len(level.links) != 6:
            raise ValueError(f"the level {index} carries {len(level.links)} Links, not six")
    if bound(term, len(start.levels)) > MAX_WORK_INT:
        raise ValueError(
            f"the self-source of {len(start.levels)} levels at A = {term.amplitude} reaches the sum "
            f"{bound(term, len(start.levels))}, beyond int64: the run is refused"
        )


def apply(term: SelfSourceTerm, start: SelfSourceStart) -> SelfSourceWrites:
    """The primitive at (i): the six differences of every level squared and summed, the sum divided by P_2 by Rule3's division act, the remainder not kept (ALGEBRA.md 9.117 the row "the self-source")."""
    check(term, start)
    total: Any = 0
    for level in start.levels:
        for arrived in level.links:
            found = difference(level.here, arrived)
            total = total + found * found
    source, _ = rule3(NO_READ, NO_READ, total, term.unit, 1, 0, 0)
    return SelfSourceWrites(source, total)


DECLARATION = Declaration(
    "the self-source",
    "(i)",
    ("the family's own levels", "P_2", "the structure table"),
    ("a family's level at a Node",),
    None,
    apply,
    "9.78 (3); 9.88 (2); 9.91 (5); 9.119 item 2, the row 'the self-source'",
    word="the right side",
)


def bind(loop: Any) -> Callable[..., object]:
    """The loop's method `_self_source`, whose array `apply` gives bit for bit, until the loop calls `apply`."""
    return loop._method("_self_source")  # type: ignore[no-any-return]
