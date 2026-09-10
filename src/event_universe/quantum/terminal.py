"""Opt-in exact terminal TWO-OUTPUT readout trial, not a general measurement engine.

Caller supplies a uniform integer ticket. Equal amplitude scales and complete,
absorbing outputs are input assumptions. One experiment per owner; no RNG here.
"""

from dataclasses import dataclass

from event_universe.core.state import Address, checked, checked_work

from .postulates import ORACLE_COST, OracleCost

TERMINAL_TRIAL_ID = "terminal-two-output-trial-v1"


@dataclass(frozen=True, slots=True)
class TerminalSetup:
    root_a: int
    root_b: int
    tick: int

    def __post_init__(self) -> None:
        for value in (self.root_a, self.root_b, self.tick):
            checked(value)
        if min(self.root_a, self.root_b, self.tick) < 0:
            raise ValueError("terminal roots and tick must be non-negative")
        if self.root_a == self.root_b:
            raise ValueError("terminal outputs must be distinct")


@dataclass(frozen=True, slots=True)
class TerminalRecord:
    """Immutable quantum result, not an Engine event."""

    tick: int
    detector: int
    address: Address
    root: int
    weight_a: int
    weight_b: int
    ticket: int


@dataclass(frozen=True, slots=True)
class TerminalReply:
    record: TerminalRecord
    evaluation_nodes: int
    repeated: int

    @property
    def cost(self) -> OracleCost:
        return ORACLE_COST


def choose_output(weight_a: int, weight_b: int, ticket: int) -> int:
    for value in (weight_a, weight_b, ticket):
        checked(value)
    if min(weight_a, weight_b, ticket) < 0:
        raise ValueError("weights and ticket must be non-negative")
    total = checked(checked_work(weight_a + weight_b))
    if total == 0:
        raise ValueError("zero total weight cannot define a terminal measurement")
    if ticket >= total:
        raise ValueError("ticket must be smaller than total weight")
    return 0 if ticket < weight_a else 1
