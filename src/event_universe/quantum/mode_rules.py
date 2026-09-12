"""Fixed local mode labels and exact additive-sector guards.

The labels are declared observables, not inferred mass, momentum or species.
Every nonzero matrix entry must stay within every declared sector. This checks
each possible transition, rather than repairing an expectation after a run.
"""

from dataclasses import dataclass

from event_universe.core.state import Address, checked

from .event_rules import Matrix
from .state import Amplitude


@dataclass(frozen=True, slots=True)
class Mode:
    name: str
    address: Address
    quantities: tuple[int, ...]


def occupation_totals(bits: int, quantities: tuple[tuple[int, ...], ...]) -> tuple[int, ...]:
    totals = [0] * len(quantities[0])
    for site, values in enumerate(quantities):
        if (bits >> site) & 1:
            for i, value in enumerate(values):
                totals[i] = checked(totals[i] + value)
    return tuple(totals)


def validate_sectors(matrix: Matrix, quantities: tuple[tuple[int, ...], ...]) -> None:
    """At most four local modes and eight additive quantities per invocation."""
    if not 1 <= len(quantities) <= 4 or len(matrix) != 1 << len(quantities):
        raise ValueError("sector labels and matrix dimension disagree")
    if not 1 <= len(quantities[0]) <= 8:
        raise ValueError("one to eight declared quantities required")
    if any(len(row) != len(quantities[0]) for row in quantities):
        raise ValueError("quantity dimensions disagree")
    for values in quantities:
        for quantity in values:
            checked(quantity)
    sectors = tuple(occupation_totals(bits, quantities) for bits in range(len(matrix)))
    for row, coefficients in enumerate(matrix):
        for column, value in enumerate(coefficients):
            if value != (0, 0) and sectors[row] != sectors[column]:
                raise ValueError("local transition violates a declared conserved sector")


ZERO = Amplitude(0, 0)
ONE = Amplitude(1, 0)
IDENTITY = ((ONE, ZERO), (ZERO, ONE))
