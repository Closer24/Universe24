"""The contraction: the coupling rows' products of two readings into their targets, through the 24's tables."""

from typing import NamedTuple

from tensor24.algebra.carry import Z


class Plan(NamedTuple):
    """The coupling rows expanded at load over the kinds' tables: per term its two readings, its whole factor, its target."""

    first: Z  # (terms,): the row of the readings that enters first
    second: Z  # (terms,): the row that enters second
    factor: Z  # (terms,): the strength times the table's entry
    target: Z  # (gears, terms): 1 where the term lands


def contract(plan: Plan, readings: Z) -> Z:
    """Every gear's source J: one gather, one product and one scattered sum; a product the 24 forbid holds no term."""
    first, second, factor, target = plan
    return target @ (factor[:, None] * readings[first] * readings[second])
