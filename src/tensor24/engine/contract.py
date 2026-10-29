"""The contraction: the coupling rows' products of two readings into their targets, through the 24's tables."""

from typing import NamedTuple

import numpy as np

from tensor24.algebra.carry import Z


class Plan(NamedTuple):
    """The coupling rows expanded at load over the kinds' tables: per term its two readings, its whole factor, its target."""

    first: Z  # (terms,): the row of the readings that enters first
    second: Z  # (terms,): the row that enters second
    factor: Z  # (terms,): the strength times the table's entry
    target: Z  # (terms,): the gear's row where the term lands


def contract(plan: Plan, readings: Z, gears: Z) -> Z:
    """Every gear's source J in the gears' shape, Python integers on any gears: a gather, a product, a scattered sum."""
    first, second, factor, target = plan
    source = np.zeros_like(gears, dtype=object)
    np.add.at(source, target, factor[:, None] * readings[first] * readings[second])
    return source
