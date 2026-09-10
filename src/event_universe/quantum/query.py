"""Fixed-size integer query records; no world access and no outcome sampling."""

from dataclasses import dataclass

from event_universe.core.state import Address, checked

from .postulates import ORACLE_COST, OracleCost
from .state import Amplitude, checked_address


@dataclass(frozen=True, slots=True)
class QuantumQuery:
    """Ask about an explicit local history node, not whether a particle exists.

    `tick` is the calling world's timestamp, not a host evaluation clock.
    Immutable roots let repeated read-only queries return the same information.
    """

    root: int
    address: Address
    tick: int

    def __post_init__(self) -> None:
        checked(self.root)
        checked_address(self.address)
        checked(self.tick)
        if self.root < 0 or self.tick < 0:
            raise ValueError("query root and world tick must be non-negative")


@dataclass(frozen=True, slots=True)
class QuantumReply:
    """Unnormalized amplitude/weight, not a selected physical measurement outcome."""

    request: QuantumQuery
    amplitude: Amplitude
    weight: int
    evaluation_nodes: int
    cache_hit: int

    @property
    def cost(self) -> OracleCost:
        return ORACLE_COST


@dataclass(frozen=True, slots=True)
class QuantumQueryStats:
    """Successful calls only. Node evaluations are not CPU instructions or time."""

    successful_queries: int = 0
    host_evaluated_nodes: int = 0
    cache_hits: int = 0

    @property
    def model_cost_units(self) -> int:
        return self.successful_queries

    @property
    def elapsed_world_ticks(self) -> int:
        return ORACLE_COST.world_ticks
